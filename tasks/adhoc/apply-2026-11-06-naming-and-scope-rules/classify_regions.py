"""Split the survey leads by whether the binding sits inside a published doc-region.

Reads ``data/candidates.txt`` (written by ``discover.py``) and, for each lead,
checks whether its line lies between a ``# doc-region-begin NAME`` marker and the
next ``# doc-region-end NAME`` marker in the same file.  The book includes such
lines verbatim, so a lead inside a region changes published text; a lead outside
one does not.  Writes ``data/candidates_outside_regions.txt`` and prints the
per-file counts.  Idempotent: it only rewrites its own output.

Run from anywhere: ``python3 tasks/adhoc/<slug>/classify_regions.py``.
"""

import collections
import pathlib
import re

REPO_ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parents[3]
DATA: pathlib.Path = pathlib.Path(__file__).resolve().parent / "data"
LEAD: re.Pattern[str] = re.compile(r"^(?P<kind>\S+)\s+(?P<path>[^:\s]+):(?P<line>\d+) ")
BEGIN: re.Pattern[str] = re.compile(r"^\s*#\s*doc-region-begin (?P<name>.+?)\s*$")
END: re.Pattern[str] = re.compile(r"^\s*#\s*doc-region-end (?P<name>.+?)\s*$")


def region_lines(path: pathlib.Path) -> set[int]:
    """The 1-based line numbers of ``path`` that lie inside any doc-region."""
    inside: set[int] = set()
    open_at: dict[str, int] = {}
    number: int
    text: str
    for number, text in enumerate(path.read_text().splitlines(), start=1):
        begin: re.Match[str] | None = BEGIN.match(text)
        end: re.Match[str] | None = END.match(text)
        if begin is not None:
            open_at[begin.group("name")] = number
        elif end is not None and end.group("name") in open_at:
            inside.update(range(open_at.pop(end.group("name")), number + 1))
    return inside


def main() -> None:
    cache: dict[str, set[int]] = {}
    outside: list[str] = []
    inside_count: collections.Counter[str] = collections.Counter()
    outside_count: collections.Counter[str] = collections.Counter()
    row: str
    for row in (DATA / "candidates.txt").read_text().splitlines():
        match: re.Match[str] | None = LEAD.match(row)
        if match is None:
            continue
        path: str = match.group("path")
        if path not in cache:
            cache[path] = region_lines(REPO_ROOT / path)
        if int(match.group("line")) in cache[path]:
            inside_count[path] += 1
        else:
            outside.append(row)
            outside_count[path] += 1
    (DATA / "candidates_outside_regions.txt").write_text("\n".join(outside) + "\n")
    path_name: str
    for path_name in sorted(set(inside_count) | set(outside_count)):
        print(f"{outside_count[path_name]:4d} outside  {inside_count[path_name]:4d} inside  {path_name}")


if __name__ == "__main__":
    main()
