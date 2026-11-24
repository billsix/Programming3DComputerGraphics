# Book: link each chapter to the assignment that exercises it

**Done 2026-11-24**, with the book build still to be run on the host (below). Split out 2026-09-09 from
`tasks/archive/2026/09/09/assignments-1-and-2-review.md`.

## Decisions (William Emerison Six <billsix@gmail.com>, 2026-11-24, "your discretion")

- **The two unpublished assignments get prose, not pages.** A page would put the code in the book under
  the `doc-region` regime, and two of the files carry a deliberate hole that is to stay untouched
  (`CLAUDE.md`, "Assignments"); adding markers to them is the edit to avoid. The earlier recommendation
  to give `assignment2-screenspace` a page was not taken for that reason.
- **Wording is the plain "Try it yourself"**, not the "Programming Project" / "Math Homework" vocabulary.
  The two published pages keep their titles.

## What changed (`book/docs/`)

- `ch02.rst`: an Exercise bullet pointing at `:doc:programmingproj1`.
- `ch03.rst`: a "Try it yourself" section on `assignments/assignment2-screenspace.py`, the second answer
  to the non-square-window problem (map NDC to screen space yourself, with `KEEP_ASPECT_RATIO`).
- `ch05.rst`: a "Try it yourself" section pointing at `:doc:mathhomework1`.
- `ch18.rst`: a "Try it yourself" section on `assignments/assignment3-strafe.py`, demo18 with the strafe
  removed.

## Still owed (required before relying on the links)

`make html` on the host: confirm the two `:doc:` targets resolve (a bad one is a warning, not an error)
and that the new sections render in light and dark furo. The sandbox could not build the book (its image
does not rebuild here; see `tasks/sphinx-docstrings-google-and-rendering.md`). A docutils parse of the
four chapters showed no problem beyond Sphinx-only directives it does not know.
