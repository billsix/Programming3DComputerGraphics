# Notebook: the image-sampling problem (virtual pixels & texels)

**Done 2026-11-24**, with the book build still to be run on the host (below). Started 2026-08-27
(William Emerison Six <billsix@gmail.com>). The maintainer's idea, verbatim: *"Make a notebook example
which shows the problem of sampling for images, with virtual pixels, and virtual texels, have them at
first be an image scaling, with one to one, then have a scaling non-one to one. Then have a rotation,
then have a rotation and a scaling."*

## Decisions (William Emerison Six <billsix@gmail.com>, 2026-11-24, "your discretion")

1. **Toctree position:** right after `ndc` in `book/docs/index.rst`, with the other detour notebooks
   (`framebuffer`, `ndc`). No chapter teaches texturing (`grep -il texture book/docs/ch*.rst` is empty;
   `demo22a` has no chapter), so there is no later neighborhood to join.
2. **Pure numpy and matplotlib**, like the framebuffer notebook, with no OpenGL. The sampling problem
   needs only the pixel-to-texel map, which is the book's own idea: the inverse of an invertible function.
3. **Relation to `demo22a`:** none in the text. The closing paragraph names bilinear filtering and
   mipmaps as the fixes real texture units use, starting from the same inverse map.

## What was built

- `src/intro3dgraphics/notebooksrc/sampling.py` (jupytext percent format): an 8x8 texel texture and a
  `sample` function that inverts `texel_to_pixel` at each pixel center and takes the texel containing the
  result (nearest sampling), counting how many pixels chose each texel. Five figures, each showing the
  texture, the picture and the per-texel counts:
  1 scale 1 (every texel chosen once), 2a scale 2.5 (4 to 9 pixels per texel), 2b scale 0.4 (55 of 64
  texels never chosen), 3 rotation by 30 degrees (8 texels never chosen), 4 rotation 30 degrees with
  scale 1.7 (up to 4 per texel).
- The prose was drafted by the agent in neutral voice; the maintainer may want to rework it.
- Wired into `book/docs/index.rst` and `entrypoint/entrypoint.sh` (the two `jupytext --to notebook`
  lines, as for `ndc`), and listed in `tasks/reference/notebook-sphinx-integration.md`.

## Verification

In the `modelviewprojection` image: `entrypoint/format.sh`, `ty check src` and the annotation checker are
clean; the notebook converts with `jupytext` and executes under `jupyter nbconvert --execute` with 9 code
cells, 5 figures and 0 errors; the stage-3 figure was viewed.

## Still owed

`make docs` on the host to confirm the page builds into the book and renders in light and dark furo (the
sandbox's project image does not rebuild; see `tasks/sphinx-docstrings-google-and-rendering.md`).
