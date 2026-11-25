"""Nest each module-level helper that has exactly one caller inside that caller.

The shared Python standard ("What earns an extraction") says a helper with one
caller is nested inside it.  For every top-level function ``H`` in the scanned
files this script finds the top-level functions that reference ``H``; when that is
exactly one function ``C`` it moves ``H`` (its decorators and the comment lines
directly above it included) to the start of ``C``'s body, below ``C``'s docstring.
It skips, and reports, a helper that:

* is referenced anywhere else (module level, another file, a string-free attribute
  access such as ``module.H``) -- found with ``git grep -w``;
* carries a doctest (a nested function is not collected by ``doctest``);
* contains a multi-line string other than its docstring (re-indenting changes it);
* reads a name that ``C`` binds itself (the closure would capture ``C``'s local
  instead of the module-level name);
* is public API (its name has no leading underscore and its module is ``mathutils``).

Helpers nest innermost first (a helper that is itself the caller of another
pending helper waits).  Idempotent: a nested helper is no longer top-level, so a
second run finds nothing.  The formatter reindents long lines afterwards.

Run from anywhere: ``python3 tasks/adhoc/<slug>/nest_one_caller.py [--dry-run] FILE...``
"""

import ast
import pathlib
import re
import subprocess
import sys

REPO_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]

FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef


def top_level_functions(tree: ast.Module) -> dict[str, FunctionNode]:
    """The module's top-level functions by name."""
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def bound_names(fn: FunctionNode) -> set[str]:
    """Names ``fn`` binds in its own scope: parameters, assignments, targets, defs."""
    names: set[str] = {a.arg for a in ast.walk(fn.args) if isinstance(a, ast.arg)}
    node: ast.AST
    for node in ast.walk(fn):
        match node:
            case ast.Name(ctx=ast.Store() | ast.Del()):
                names.add(node.id)
            case ast.FunctionDef() | ast.AsyncFunctionDef() | ast.ClassDef():
                if node is not fn:
                    names.add(node.name)
            case ast.Import() | ast.ImportFrom():
                names.update(
                    (alias.asname or alias.name).split(".")[0] for alias in node.names
                )
            case ast.ExceptHandler(name=str()):
                names.add(node.name)
            case _:
                pass  # every other node binds nothing
    return names


def loaded_names(fn: FunctionNode) -> set[str]:
    """Names ``fn`` reads."""
    return {
        node.id
        for node in ast.walk(fn)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def referencing_functions(
    helper: str, functions: dict[str, FunctionNode], tree: ast.Module
) -> tuple[set[str], int]:
    """The top-level functions that read ``helper``, and the count of reads elsewhere."""
    users: set[str] = set()
    inside: int = 0
    name: str
    fn: FunctionNode
    for name, fn in functions.items():
        if name == helper:
            continue
        count: int = sum(
            1
            for node in ast.walk(fn)
            if isinstance(node, ast.Name) and node.id == helper
        )
        if count:
            users.add(name)
            inside += count
    total: int = sum(
        1 for node in ast.walk(tree) if isinstance(node, ast.Name) and node.id == helper
    )
    own: int = sum(
        1
        for node in ast.walk(functions[helper])
        if isinstance(node, ast.Name) and node.id == helper
    )
    return users, total - inside - own


def referenced_in_other_files(helper: str, path: pathlib.Path) -> list[str]:
    """Lines in other tracked files that mention ``helper`` as a whole word."""
    result: subprocess.CompletedProcess[str] = subprocess.run(
        ["git", "grep", "-nw", helper, "--", "*.py", "*.rst", "*.ipynb"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    own: str = str(path.relative_to(REPO_ROOT))
    uses: re.Pattern[str] = re.compile(
        rf"(\bimport\b.*\b{helper}\b|\.{helper}\b|^\s*{helper},?\s*$)"
    )
    return [
        row
        for row in result.stdout.splitlines()
        if not row.startswith(own + ":")
        and not row.startswith("tasks/")
        and uses.search(row.split(":", 2)[2])
    ]


def has_extra_multiline_string(fn: FunctionNode, lines: list[str]) -> bool:
    """True if ``fn`` holds a triple-quoted string that is not a function docstring."""
    docstrings: set[int] = set()
    node: ast.AST
    for node in ast.walk(fn):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            first: ast.stmt = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstrings.add(id(first.value))
    for node in ast.walk(fn):
        if (
            isinstance(node, (ast.Constant, ast.JoinedStr))
            and id(node) not in docstrings
            and node.end_lineno != node.lineno
        ):
            opening: str = lines[node.lineno - 1][node.col_offset :].lstrip("rbfRBF")
            if opening.startswith(('"' * 3, "'" * 3)):
                return True
    return False


def start_line(fn: FunctionNode, lines: list[str]) -> int:
    """First line (0-based) of ``fn``: decorators and the comment lines above it."""
    first: int = min([d.lineno for d in fn.decorator_list] + [fn.lineno]) - 1
    while first > 0 and lines[first - 1].lstrip().startswith("#"):
        first -= 1
    return first


def nest_once(path: pathlib.Path, dry_run: bool) -> bool:
    """Nest one eligible helper in ``path``; True if the file changed (or would)."""
    source: str = path.read_text()
    tree: ast.Module = ast.parse(source)
    functions: dict[str, FunctionNode] = top_level_functions(tree)
    lines: list[str] = source.splitlines(keepends=True)
    pending: dict[str, str] = {}
    name: str
    for name in functions:
        users: set[str]
        elsewhere: int
        users, elsewhere = referencing_functions(name, functions, tree)
        if len(users) == 1 and elsewhere == 0:
            pending[name] = next(iter(users))
    for name, caller in pending.items():
        if name == "main" or name.startswith("__"):
            continue
        if name in pending.values():
            continue  # it is the caller of a pending helper: that helper nests first
        fn: FunctionNode = functions[name]
        host: FunctionNode = functions[caller]
        reason: str | None = None
        doc: str | None = ast.get_docstring(fn)
        if doc is not None and ">>>" in doc:
            reason = "doctest"
        elif has_extra_multiline_string(fn, lines):
            reason = "multi-line string"
        elif path.name == "mathutils.py" and not name.startswith("_"):
            reason = "public API"
        elif referenced_in_other_files(name, path):
            reason = "named in another file"
        else:
            free: set[str] = loaded_names(fn) - bound_names(fn)
            clash: set[str] = free & bound_names(host)
            if clash:
                reason = f"caller binds {sorted(clash)}"
        if reason is not None:
            print(f"  skip  {path.name}: {name} -> {caller}: {reason}")
            continue
        top: int = start_line(fn, lines)
        end: int = fn.end_lineno or fn.lineno
        block: list[str] = lines[top:end]
        indented: list[str] = [("    " + row if row.strip() else row) for row in block]
        body_first: ast.stmt = host.body[0]
        insert_at: int
        if (
            isinstance(body_first, ast.Expr)
            and isinstance(body_first.value, ast.Constant)
            and isinstance(body_first.value.value, str)
        ):
            insert_at = body_first.end_lineno or body_first.lineno
        else:
            insert_at = body_first.lineno - 1
        print(f"  nest  {path.name}: {name} -> {caller}")
        if dry_run:
            return False
        # remove the helper (and its trailing blank lines), then insert in the host
        rest: list[str] = lines[:top] + lines[end:]
        shift: int = end - top if top < insert_at else 0
        at: int = insert_at - shift
        rest[at:at] = ["\n", *indented, "\n"]
        path.write_text("".join(rest))
        return True
    return False


def main() -> None:
    args: list[str] = sys.argv[1:]
    dry_run: bool = "--dry-run" in args
    files: list[str] = [a for a in args if a != "--dry-run"]
    file: str
    for file in files:
        path: pathlib.Path = (REPO_ROOT / file).resolve()
        print(path.relative_to(REPO_ROOT))
        changed: bool = True
        while changed and not dry_run:
            changed = nest_once(path, dry_run)
        if dry_run:
            nest_once(path, dry_run)


if __name__ == "__main__":
    main()
