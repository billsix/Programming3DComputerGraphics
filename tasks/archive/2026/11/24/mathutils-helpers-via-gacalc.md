# `mathutils` helpers: which should be re-expressed in gacalc's vocabulary?

**Done 2026-11-24.** Merged 2026-09-08 from `mathutils-angle-helpers-via-gacalc-measures.md` and
`face-normal-vector3d-io.md` (archived at `tasks/archive/2026/09/08/`). Decisions: William Emerison Six
<billsix@gmail.com>, 2026-11-24, "your recs" on all three open questions.

## What changed

- **`sine`** (`src/intro3dgraphics/mathutils.py`) divides `gacalc.measure.signed_area(v1, v2)` by the two
  lengths instead of reading `(v1 ^ v2).coeff_e_12`. The zero-length NaN guard and the rotate-90 teaching
  comment stay; the comment now says gacalc names that number `signed_area`.
- **`abs_sin`** divides `gacalc.measure.area(v1, v2)` by the two lengths. It stays: it is public,
  book-documented API even though no production code calls it.
- **`cosine`** is unchanged on purpose. It returns NaN on a zero-length vector, which
  `framebuffer/softwarerendering.py` relies on; gacalc's `cosine` method raises there.
- **`_face_normal`** (`src/intro3dgraphics/util/shading.py`) keeps tuples in and out. Its callers
  (`demo22a` and `demo23`) hold tuple corners and write the normal into `float32` vertex buffers, so
  `Vector` in and out would only move the conversions into the callers. Its docstring says so.

## Verification

Run in the `modelviewprojection` image (the project image would not rebuild in the sandbox, see
`tasks/sphinx-docstrings-google-and-rendering.md`): `mathutils`, `util` and `tests` doctests plus the
suite (52 passed), `ty check src tests`, `tools/check_local_annotations.py --include-module src tests`
and `entrypoint/format.sh`, all clean. Both rewrites return the same numbers, so the doctests did not
change.
