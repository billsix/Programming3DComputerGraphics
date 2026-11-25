# Apply the 2026-11-06 naming and scope rules across this repository

**Status:** done and archived 2026-11-25
**Created:** 2026-11-06 (William Emerison Six <billsix@gmail.com>): asked for the geometricalgebra survey
task ("search through all of geometricalgebra and see if there is programming advice that we added that
should be applied to the codebase, to refactor it"), then "add a similar task to every other python
project in opt".

## What this did

Five rules entered the shared Python standard on 2026-11-06 (github.com/billsix/runClaudeInContainer,
`tasks/reference/python-coding-standard.md`: "Inline a value used once, and name it in a comment instead of a
binding" and "What earns an extraction"). The task surveyed this repository's Python for breaks of them, then
refactored without changing behaviour:

1. inline a binding used once, with a comment above the expression naming it;
2. a binding used twice does not automatically earn a name (check whether one expression absorbs the uses);
3. declare a name at the point of use;
4. nest a helper with one caller inside that caller;
5. when nesting, shadow deliberately and check that the helper never needs the outer value.

Scope: `src/intro3dgraphics/`, `tests/`, `tools/`, `assignments/` (minus the three files with a deliberate
exercise hole). `ports/` and `pgzero_gl` had moved to other repositories, so they were out.

## Decisions, in order

All decisions by William Emerison Six <billsix@gmail.com> unless marked as the agent's.

- **2026-11-24: survey first, then use discretion and apply.** A one-caller helper that a test imports stays at
  module level (the discovery script skips any helper whose name appears in `tests/`).
- **2026-11-24: survey.** `discover.py` walked the in-scope files with `ast` and wrote a worklog of 716 leads
  (340 single-use, 282 double-use, 35 declared far from first use, 59 one-caller). Most leads were noise: it also
  flags single assignments that are deliberate.
- **2026-11-24: first batch.** `draw_unit_axes` in `util/axes.py`: the four size bindings moved down to the block
  that first uses them (rule 3). The agent left the big demo files alone, on the stated ground that the book
  includes them by `doc-region` marker. **That ground was false** (found 2026-11-25, below).
- **2026-11-25: `tools/` and `tests/`.** Inlined `raw`, `scratch`, `background`, `text`, `occurrences`,
  `begin_needle`, `end_needle`, `stripped`, `is_marker`, `tree` and moved `root` down, across the four `tools/`
  files. Every `tests/` lead was left alone: each is a named test input, expected value or case table, and the name
  is what the reader scans for in an assertion.
- **2026-11-25: the 2026-11-24 coarse triage was wrong.** `classify_regions.py` showed that `demo22`, `demo22a`,
  `demo22b`, `export_scene.py`, `demo23`, `demo24` and the `mvpvisualization/` programs have no `doc-region` marker
  and no `literalinclude` names them. Only 6 of the 722 leads sit inside a published region (5 in `mathutils.py`,
  1 in `assignments/assignment1.py`), so nearly all leads were fair game.
- **2026-11-25: inline batch** (`apply_inlines.py`, exact-text edits, idempotent): single-use locals in `demo22`,
  `demo22b`, `export_scene.py`, `grapher3d.py`, the `mvpvisualization/` programs, `sampling.py`, `nbplotutils.py`
  and `wxapp.py`; then `mvp_loc`, `model_loc`, `sm`, `step`, `window_name`, `fmt`, `internal`, `lw`; then `mode` in
  `export_scene.read_glb`.
- **2026-11-25: `FAR` leads.** `morph` (twice), `inv` and `hbox` moved to the block that first uses them.
- **2026-11-25: `TWICE` leads (about 290):** triaged by category and left alone. They are GL handles, widgets, loop
  state, the cos/sin pair of one angle, and an `epi` result whose `None` gates a block; no
  `x if x is not None else y` or `getattr` shape remained to collapse.
- **2026-11-25: shared-standard wording.** The maintainer asked for the sharper wording to go into the shared
  standard. The agent added "A name that documents what it holds keeps its binding" (test inputs and case tables,
  tables of rows and named corners, slices of a packed array named for their layout, side-effecting calls, a value
  computed before a later statement changes its inputs) to the three byte-identical copies in
  runClaudeInContainer and runCrushInContainer. It left out a one-caller sentence it had drafted, because that
  contradicted the standard (next entry).
- **2026-11-25: one-caller helpers.** The agent first left all 61 at module level, citing "the rule nests only a
  helper that closes over the caller's parameters". That misread the standard, whose "What earns an extraction"
  nests every one-caller helper (the global `CLAUDE.md` states only the closes-over condition, so the two disagree).
  **The maintainer decided to nest per the standard.**
- **2026-11-25: nesting mechanics** (`nest_one_caller.py`, idempotent): moves a helper, with its decorators and the
  comment lines above it, to the start of its caller's body; cascades (a helper becomes single-caller once its
  sibling nests). It skips a helper with a doctest (`doctest` does not collect a nested function), one named by an
  import or attribute access in another file (`git grep -w`), one with a triple-quoted string other than a
  docstring, and one that reads a name its caller rebinds. The deeper indent put 18 comment and docstring lines over
  80 columns; they were reflowed as whole paragraphs, not one line at a time.
- **2026-11-25: the cascade in `modelviewperspectiveprojection.py`** put `_place`, `_warp`,
  `_epilogue_ndc_to_fb`, `grid_matrix` and `graph_panel` inside `frame`, which is now long. **The maintainer chose
  to keep it.**
- **2026-11-25: verification outside the agent's gates.** The maintainer ran `demo22b` on the host and in the
  container, and `wxapp.py` on the host. `wxapp.py` failed in the container on its backend (parked, not part of this
  task; see "Owed").

## Result

- **Applied:** the inlines, moves and nestings in the decisions above; the nesting batch touched 17 files.
  Behaviour is unchanged.
- **Left alone, with the reason:** tests (named inputs and tables); `TWICE` leads (handles, widgets, loop state,
  trig pairs); data tables and named corners (`faces`, `corners`, `edges`, `uvs`, `p00`..`p11`); packed-array slices
  (`positions`, `normals`, `texcoords`); the `vs`/`fs` shader pairs (the file handle closes before
  `compileProgram`); `wxapp.py` `dt` (`last_time` is overwritten between its definition and use, so inlining
  changes the result), `vbo` and `mask`; `demo21.py` `font_loader` and `_default_vao`; the accumulators declared
  before their loop (`out`, `errors`); `mathutils.py` (public, book-documented API with teaching comments).
- **Not nested:** helpers with a doctest (`mathutils.find_normal`, `mathutils.ortho`,
  `check_local_annotations.iter_py`, `check_local_annotations.display_path`), and helpers that other files or the
  tests use (the `build_*` mesh builders and `read_glb` in `export_scene.py`, `make_vao` and `make_vbo` in
  `demo22`/`demo22b`, `_region_is_empty` and `_dead_marker_report` in `check_doc_regions.py`).

## Verification

Containerized, with the image already built (`make -o image <target>`): `format`, `type-check`, `check-regions` and
`test` (55 passed) exit 0 after every batch. `tools/verify_render.sh` (5 frames, Xvfb) passed for `demo19e`,
`demo21`, `demo22`, `demo24` and the `mvpvisualization/` programs. `render_probe.py` cannot run `demo22b` (its
sibling `import export_scene` fails under the probe, which predates this task); the maintainer checked it by hand.
The menubar helpers `_focus` and `rebuild_framebuffer` run on a click and were not exercised by the agent.

## Afterwards (2026-11-25, William Emerison Six <billsix@gmail.com> approved the agent's recommendation)

- **Promoted** `nest_one_caller.py` to `tools/nest_one_caller.py`: the repository root comes from
  `git rev-parse --show-toplevel`, it has `argparse` options (`--dry-run`, `--keep NAME ...`), the `mathutils`
  special case is gone (a doctest or another file's import already protects public API), and it reports every
  nesting a dry run would make. It was run on itself, which nested its own 14 helpers (the standard applies to
  it too). Checked by re-nesting the pre-nesting versions of `axes.py`, `stencillens.py`, `sampling.py`,
  `pushmatrix.py` and `modelviewperspectiveprojection.py` from the earlier commit in a scratch repository: the first
  four came out AST-identical to the committed result; the fifth matched ignoring the order of the nested
  definitions and the reflowed docstrings. Not wired into any gate. `tasks/reference/python-coding-standard-mvp.md`
  points to it.
- **Removed** the one-shot `discover.py`, `classify_regions.py`, `apply_inlines.py` and `data/` (the survey is
  cheap to regenerate and `classify_regions.py` depends on this repository's `doc-region` markers). They stay in
  the history of the earlier work commits.
- **Still owed, outside this repository:** the shared-standard edit is staged, not committed, in
  runClaudeInContainer and runCrushInContainer; `wxapp.py` in the container is parked on the work stack; the
  six other repositories that carry this task (`epix-mirror`, `geometricalgebra`, `hanoi`, `mathnotebooks`,
  `methodfinder`, `multivariate-math`) can use `tools/nest_one_caller.py`, copied.
