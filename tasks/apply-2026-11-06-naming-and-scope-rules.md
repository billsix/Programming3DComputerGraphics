# Apply the 2026-11-06 naming and scope rules across this repository

**Status:** in progress — survey done and coarsely triaged 2026-11-24; one small batch applied; the per-file triage and the remaining refactors are not done
**Priority:** 5
**Difficulty:** 7
**Created:** 2026-11-06 (William Emerison Six <billsix@gmail.com>): asked for the geometricalgebra survey
task ("search through all of geometricalgebra and see if there is programming advice that we added that
should be applied to the codebase, to refactor it"), then "add a similar task to every other python
project in opt".

## BLUF

Five naming and scope rules were added to the shared Python standard on 2026-11-06, while refactoring
geometricalgebra. This task searches this project's Python for places that break them, records every
candidate in a worklog, and refactors the ones that should change, with no change in behaviour. Done =
every candidate is either refactored or recorded as left alone with its reason, and the gates pass
(containerized `make test`, `make type-check`, `make format`, and `make check-regions`; the CtC gates for any touched game).

## Context (read first)

- **The rules**, in the shared `python-coding-standard.md` (github.com/billsix/runClaudeInContainer
  `tasks/reference/`; mounted at `~/.claude/reference/`), sections "Inline a value used once, and name
  it in a comment instead of a binding" and "What earns an extraction"; the language-agnostic summary is
  `code-style-conventions.md`, "Names: inline what is used once, declare at the point of use, nest and
  shadow":
  1. **Inline a binding used once**, even one that exists to explain the expression; put a comment above
     the inlined subexpression that describes it and gives it its name.
  2. **Two uses do not automatically earn a name**: check whether one expression absorbs them (e.g.
     `getattr(obj, name, fallback)` or `d.get(key, default)` in place of a `None` check plus ternary), or
     whether a cheap expression can be repeated. Keep the name when repeating the expression reads worse
     or recomputes something expensive.
  3. **Declare a name at the point of use**, not many lines earlier.
  4. **Nest a helper with one caller inside that caller.**
  5. **When nesting, shadow deliberately**: the helper's parameter takes the caller's name when it means
     the same thing, and the shadowing is verified (the helper never needs the outer value; none of its
     other names hide an enclosing binding).
- **The worked example to imitate:** github.com/billsix/geometricalgebra
  `tasks/reference/python-coding-standard-gacalc.md`, "Inline once, declare at use, nest and shadow"
  (the 2026-11-06 refactor of `Frame.to_invertible_function`). The same survey for that project is its
  `tasks/apply-2026-11-06-naming-and-scope-rules.md`.
- **Rules that compete with these, and win:** an externally-defined name (a framework override, a
  callback signature, a dunder) is never renamed; "annotate every binding" still applies to every name
  that survives; a public parameter name is part of the API and is out of scope.

## Scope

- **In:** `src/intro3dgraphics/` (the demos, `mathutils.py`, `cayley/`, `mvpvisualization/`,
  `graphingcalculator/`, `pgzero_gl/`), `tests/`, `tools/`, `assignments/`, `ports/codetheclassics/`,
  and `ports/openglsuperbiblev4/`.
- **Out:** the vendored Emacs tree under `entrypoint/`, and the three assignments with a deliberate hole
  (`assignments/assignment2-screenspace.py`, `assignments/assignment3-strafe.py`,
  `assignments/demo02/vec1.py`): leave those files alone.

## Project constraints (these override the rules where they conflict)

- **The demos are deliberately procedural, with module-level globals, so students read top to
  bottom** (`CLAUDE.md`, "mistake-driven development"). The rules apply to function locals and nested
  helpers; do not turn module-level globals into locals, and do not introduce classes or abstractions.
  A module-level name that a later chapter or the book refers to stays.
- **The book includes code by `doc-region` marker** (`CLAUDE.md`, "The book includes code by MARKER").
  Before editing, check whether the text is inside a published region; a refactor that moves marked
  code moves its markers, and a binding the book's prose names stays. Run `make check-regions`.
- **The Code-the-Classics ports are behaviour-faithful** (`tasks/reference/code-the-classics-tightening.md`):
  same RNG, update and draw order. Verify each touched game with `tools/ctc_verify_game.sh` (frame
  pixel identity) and the state-trace tools (`tasks/reference/tests-and-gates.md`).
- mvp's own additions doc: `tasks/reference/python-coding-standard-mvp.md` (line length 80, the wx
  boundary, book-shorthand naming, mvp's inner-function precedents). Read it before triage; where it
  records a precedent that conflicts with these rules, raise it as a question rather than overriding it.

## Plan

1. **Discover with a script, not by reading every file.** Write
   `tasks/adhoc/apply-2026-11-06-naming-and-scope-rules/discover.py`, an `ast` walk over the in-scope paths (repo-relative paths, derived
   from the script's own location) that reports:
   - a local assigned once and loaded once (rule 1), with the line distance between the two (rule 3);
   - a local assigned once and loaded exactly twice, flagged for a look (rule 2);
   - a local whose first load is far from its assignment, e.g. more than 10 lines (rule 3);
   - a module-level or enclosing-scope function called from exactly one function and not imported by a
     test (rule 4);
   - a nested function whose parameter names differ from an enclosing local holding the same kind of
     value, as a lead for rule 5 (a judgment call, so a lead only).
   Write the results to `tasks/adhoc/apply-2026-11-06-naming-and-scope-rules/data/candidates.txt` (a committed snapshot worklog). If the
   geometricalgebra survey has already produced its `discover.py`, copy it and adjust the paths rather
   than rewriting it.
2. **Triage the worklog** into: refactor; leave alone (with the reason, e.g. a loop accumulator, a
   binding a doctest or notebook shows the reader, a name a test asserts on, a public parameter, an
   annotation that carries information the inline form would lose, or a project constraint above); and
   ask the maintainer. Record the counts here.
3. **Refactor in small batches, one module (or a few related ones) at a time**, matching the worked
   example: inline with a naming comment, absorb double uses, move declarations down, nest one-caller
   helpers and verify the shadowing. Run ruff and `ty` after each batch.
4. **Gates:** containerized `make test`, `make type-check`, `make format`, and `make check-regions`; the CtC gates for any touched game.
5. Record what was changed, what was left alone and why, and any rule the survey showed needs a sharper
   wording; feed that back to the shared standard (github.com/billsix/runClaudeInContainer, mirrored in
   github.com/billsix/runCrushInContainer).

## Decisions (William Emerison Six <billsix@gmail.com>, 2026-11-24)

- Question 1: survey first, then use discretion and apply.
- Question 2 (a one-caller helper that a test imports stays at module level): taken as covered by
  "use discretion"; the recommendation (yes) was applied. The discovery script already skips any helper
  whose name appears in `tests/`.
- Scope changed by the repository move: `ports/` and `pgzero_gl` no longer live here, so the survey
  covers `src/intro3dgraphics/`, `tests/`, `tools/` and `assignments/` (minus the three holes).

## Progress (2026-11-24)

- **Survey:** `tasks/adhoc/apply-2026-11-06-naming-and-scope-rules/discover.py` wrote
  `data/candidates.txt`: 716 leads (340 `ONCE`, 282 `TWICE`, 35 `FAR`, 59 `ONE_CALLER`). It also counts
  single-assignment locals the body shows on purpose, so most leads are noise until read.
- **Coarse triage by file (not yet per candidate):** the largest groups sit in the demos and
  their helpers (`demo22b/export_scene.py` 109, `demo22` 76, `demo24` 74, `demo22a` 45, `demo22b` 40,
  `demo23` 38) and in `mvpvisualization/modelviewperspectiveprojection.py` (48): left alone for now
  because the book includes them by `doc-region` marker and their locals feed GL calls the book prose
  names. `mathutils.py` (18) is public, book-documented API with teaching comments: left alone.
  `tools/` (about 90) and `tests/` (about 35) need a read of each lead before touching.
- **Applied:** `src/intro3dgraphics/util/axes.py`, `draw_unit_axes`: the four size bindings moved from
  the top of the function to the polygon-mode block that precedes their first use (rule 3). Gates
  (doctests and `pytest` 55 passed, `ty`, annotation checker, `format.sh`) were clean in the
  `modelviewprojection` image.

## What remains

1. Read the `tools/` and `tests/` leads one by one and apply rules 1–3 where the binding is neither a
   loop accumulator, a doctest-visible name, nor an assertion target.
2. Decide the demo leads against the `doc-region` rule, one demo at a time, running `make check-regions`.
3. `ONE_CALLER` (rule 4) candidates in `util/axes.py` (`_draw_solid_*` called only from
   `draw_unit_axes`): nest them, or leave them module-level because `draw_unit_axes` runs every frame.
   Not decided.
4. Record any sharper rule wording back in the shared standard.
