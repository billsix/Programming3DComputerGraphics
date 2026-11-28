"""Rename the package ``intro3dgraphics`` to ``programming3dcomputergraphics``.

One-shot sweep for ``tasks/rename-package-to-programming3dcomputergraphics.md``.
One rule: the word ``intro3dgraphics`` becomes ``programming3dcomputergraphics``
in every tracked text file, except where it follows ``github.io/`` (the GitHub
Pages path, which ``tasks/release-book-github-pages-decision.md`` decides).

Skipped on purpose: ``tasks/archive`` (history), ``entrypoint/dotfiles``
(vendored), ``book/docs/_static``, the "Historical copy" reference docs, this
directory, the task document of this change and binary files. Idempotent: a
second run changes nothing. The directory move itself is ``git mv
src/intro3dgraphics src/programming3dcomputergraphics`` (done first, skipped if
already done).

Usage (from anywhere):
    python3 tasks/adhoc/rename-package-to-programming3dcomputergraphics/rename.py
"""

import pathlib
import re
import subprocess

REPO: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]

OLD_PACKAGE: str = "intro3dgraphics"
NEW_PACKAGE: str = "programming3dcomputergraphics"
SKIP_PREFIXES: tuple[str, ...] = (
    "tasks/archive/",
    "entrypoint/dotfiles/",
    "book/docs/_static/",
    "tasks/adhoc/rename-package-to-programming3dcomputergraphics/",
)
SKIP_FILES: frozenset[str] = frozenset(
    {"tasks/rename-package-to-programming3dcomputergraphics.md"}
)
PACKAGE: re.Pattern[str] = re.compile(r"(?<!github\.io/)" + OLD_PACKAGE)


def tracked_files() -> list[str]:
    """List the tracked files, with the old package directory already moved.

    Returns:
        Repo-relative paths from ``git ls-files``.
    """
    old: pathlib.Path = REPO / "src" / OLD_PACKAGE
    if old.exists():
        subprocess.run(
            ["git", "mv", f"src/{OLD_PACKAGE}", f"src/{NEW_PACKAGE}"],
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
        if path.startswith("tasks/") and historical_copy(before):
            continue
        after: str = PACKAGE.sub(NEW_PACKAGE, before)
        if after != before:
            target.write_text(after)
            changed.append(path)
    print(f"changed {len(changed)} files")


if __name__ == "__main__":
    main()
