"""Rename the package ``modelviewprojection`` to ``intro3dgraphics`` and retitle the project.

One-shot sweep for ``tasks/rename-package-modelviewprojection-to-intro3dgraphics.md``. Four rules, each over its own file set:

* PACKAGE: the word ``modelviewprojection`` becomes ``intro3dgraphics`` in code, configuration, the book and the container
  files, except where it names something else: ``MatrixStack.modelviewprojection`` (gacalc's enum member, preceded by a dot), a
  GitHub URL of the old repository (preceded by ``billsix/``), and any longer word.
* PACKAGE-STRICT: in ``tasks/`` (open tasks and reference docs) only the path, import and dotted-module forms change, never the
  bare word, which there often names the old repository.
* MOUNT: the container mount path ``/mvp`` becomes ``/intro3dgraphics``.
* TITLE: the window-title string ``"ModelViewProjection ...`` becomes ``"Introduction to 3D Computer Graphics ...``.

Skipped on purpose: ``tasks/archive`` (history), ``entrypoint/dotfiles`` (vendored), the "historical copy" reference docs, ``README.md``
and ``CLAUDE.md`` (edited by hand), the two task documents of this change, and binary files. Idempotent: a second run changes nothing.
The directory move itself is ``git mv src/modelviewprojection src/intro3dgraphics`` (done first, skipped if already done).

Usage (from anywhere):
    python3 tasks/adhoc/rename-package-modelviewprojection-to-intro3dgraphics/rename.py
"""

import pathlib
import re
import subprocess

REPO: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]

SKIP_PREFIXES: tuple[str, ...] = (
    "tasks/archive/",
    "entrypoint/dotfiles/",
    "book/docs/_static/",
    "tasks/adhoc/rename-package-modelviewprojection-to-intro3dgraphics/",
)
SKIP_FILES: frozenset[str] = frozenset(
    {
        "README.md",
        "CLAUDE.md",
        "book/docs/mvp_dict.pws",
        "tasks/rename-package-modelviewprojection-to-intro3dgraphics.md",
        "tasks/remove-miniaudio-and-openexr.md",
    }
)
PACKAGE: re.Pattern[str] = re.compile(
    r"(?<![\w.])(?<!billsix/)modelviewprojection(?!\w)"
)
PACKAGE_STRICT: re.Pattern[str] = re.compile(
    r"(?<![\w.])(?<!billsix/)modelviewprojection(?=/|\.\w|\b(?<=import modelviewprojection)|\b(?<=from modelviewprojection))"
)
MOUNT: re.Pattern[str] = re.compile(r"(?<![\w/.-])/mvp(?![\w-])")
TITLE: re.Pattern[str] = re.compile(r'(?<=")ModelViewProjection(?= )')
NEW_PACKAGE: str = "intro3dgraphics"
NEW_TITLE: str = "Introduction to 3D Computer Graphics"
TITLE_ROOTS: tuple[str, ...] = ("src/", "assignments/", "tools/")


def tracked_files() -> list[str]:
    """List the tracked files, with the old package directory already moved.

    Returns:
        Repo-relative paths from ``git ls-files``.
    """
    old: pathlib.Path = REPO / "src" / "modelviewprojection"
    if old.exists():
        subprocess.run(
            ["git", "mv", "src/modelviewprojection", f"src/{NEW_PACKAGE}"],
            cwd=REPO,
            check=True,
        )
    listing: str = subprocess.run(
        ["git", "ls-files"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout
    return listing.splitlines()


def historical_copy(text: str) -> bool:
    """Say whether a reference doc carries the "Historical copy" banner.

    Args:
        text: The document text.

    Returns:
        True when the banner appears in its first lines.
    """
    return "Historical copy (2026-11-24)" in "\n".join(text.splitlines()[:6])


def rewrite(path: str, text: str) -> str:
    """Apply every rule that covers ``path`` to ``text``.

    Args:
        path: The repo-relative path.
        text: The file's current text.

    Returns:
        The rewritten text.
    """
    if path.startswith("tasks/"):
        if historical_copy(text):
            return text
        text = PACKAGE_STRICT.sub(NEW_PACKAGE, text)
        return MOUNT.sub("/" + NEW_PACKAGE, text)
    text = PACKAGE.sub(NEW_PACKAGE, text)
    text = MOUNT.sub("/" + NEW_PACKAGE, text)
    if path.startswith(TITLE_ROOTS):
        text = TITLE.sub(NEW_TITLE, text)
    return text


def main() -> None:
    """Rewrite every covered tracked text file and report the counts."""
    changed: list[str] = []
    for path in tracked_files():
        if path in SKIP_FILES or path.startswith(SKIP_PREFIXES):
            continue
        target: pathlib.Path = REPO / path
        try:
            before: str = target.read_text()
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        after: str = rewrite(path, before)
        if after != before:
            target.write_text(after)
            changed.append(path)
    print(f"changed {len(changed)} files")


if __name__ == "__main__":
    main()
