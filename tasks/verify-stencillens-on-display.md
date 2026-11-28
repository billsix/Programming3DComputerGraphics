# Run `stencillens.py` on a real display

**Status:** blocked **Priority:** 8 **Difficulty:** 1
**Blocked on:** the maintainer running the demo on a real display (the sandbox only rendered it headless under Xvfb).
**Recheck:** run `python src/programming3dcomputergraphics/mvpvisualization/stencillens.py` on the host; cleared when the lens follows the arrow keys, Page Up/Down resize it, and `s` shows the creature everywhere.
**Created:** 2026-11-25 (William Emerison Six <billsix@gmail.com>)
**Source:** `tasks/archive/2026/11/24/stencil-ocarina-of-time-image.md` (its "Verification not done" gap).

## BLUF

`src/programming3dcomputergraphics/mvpvisualization/stencillens.py` and the ch15 "stencil buffer as a mask" section were verified only by headless renders. Done = one run on a real display with the controls working; then archive this task.

## Context

The demo requests an 8-bit stencil buffer with `glfw.window_hint(glfw.STENCIL_BITS, 8)`. Controls: arrows move the lens, Page Up/Down resize it, `s` toggles the stencil test. The two ch15 screenshots (`book/docs/_static/screenshots/stencil_lens.png`, `stencil_lens_no_mask.png`) came from `tools/verify_render.sh`. If a real driver gives no stencil bits, the lens will not mask; check `glGetIntegerv(GL_STENCIL_BITS)` first.
