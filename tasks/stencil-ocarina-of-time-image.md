# Stencil-buffer example — the Lens-of-Truth reveal from the Ocarina of Time boss-theme video

**Done 2026-11-24**, with the book build still to be run on the host (below). Asked for 2026-08-29 by
William Emerison Six <billsix@gmail.com> after watching "The Most INSANE Boss Theme Ever Written For A
Zelda Game" (https://www.youtube.com/watch?v=egayquppRZM), whose boss, Bongo Bongo, is invisible except
through the Lens of Truth.

## Decisions (William Emerison Six <billsix@gmail.com>, 2026-08-29)

1. The effect is the Lens-of-Truth reveal: a circular stencil mask inside which an otherwise-invisible
   object is drawn.
2. It lands in the **book**, as a section on the stencil test with a screenshot, not as a numbered demo.
   The recorded Ship of Harkinian gameplay (github.com/HarbourMasters/Shipwright) and a RenderDoc or
   apitrace frame capture are optional enrichment and not part of done; the gameplay capture needs the
   game assets, a display and a player, so it is the maintainer's to produce.

## What was built (2026-11-24)

- `src/intro3dgraphics/mvpvisualization/stencillens.py`: a flat program in the demo-era style, placed with
  the other pedagogical aids because decision 2 rules out a numbered demo. It draws a room (floor and three
  pillars), then writes a circle into the stencil buffer with colour and depth writes off, then draws a
  creature built from spheres with `glStencilFunc(GL_EQUAL, 1, 0xFF)`. The keys: arrows move the lens,
  Page Up and Page Down resize it, `s` switches the stencil test off. The three-step frame sits inside a
  `doc-region` named `stencil lens frame`. The plumbing (`glfw.STENCIL_BITS`, clear, enable, ops) is the
  same as `demo24`'s planar shadows, with a different role for the stencil value (mask, not a counter).
- No Nintendo assets: the creature and room are the repository's own geometry.
- `book/docs/ch15.rst`: a new subsection "The stencil buffer as a mask", after the stencil-buffer
  description, with the two screenshots, the three steps and a `literalinclude` of the marked region.
  Screenshots: `book/docs/_static/screenshots/stencil_lens.png` (lens on) and
  `stencil_lens_no_mask.png` (stencil test off).

## Verification

Headless under Xvfb via `tools/verify_render.sh` (software GL, in the `modelviewprojection` image, since the
project image would not rebuild here): both renders PASS, five distinct colours each, and the two frames
differ (lens on: the creature is cut to a circle; test off: the whole creature, 60,000 creature-coloured
pixels against 19,000 for the smaller lens); both PNGs were viewed. `tools/check_doc_regions.py` reports
all anchors resolve, with no collisions; `pytest` (55 passed), `ty check src`, the annotation checker and
`entrypoint/format.sh` are clean.

## Still owed (required before relying on the section)

`make docs` on the host: the figures and the new `literalinclude` in `ch15` have not gone through Sphinx,
and a real-display run of `stencillens.py` (the lens keys, `s`) has not been done. The sandbox's project
image does not rebuild; see `tasks/sphinx-docstrings-google-and-rendering.md`.
