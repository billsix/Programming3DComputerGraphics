# Remove miniaudio and OpenEXR from the dependencies

**Status:** proposed — needs go-ahead (filed 2026-11-24)
**Priority:** 7
**Difficulty:** 2
**Created:** 2026-11-24
**Source:** follow-up from `tasks/archive/2026/11/24/copy-history-without-ports.md` (the maintainer, William Emerison Six
<billsix@gmail.com>, 2026-11-24, asked for this task).

## BLUF

`miniaudio` and `OpenEXR` were in `requirements.txt` only for the ports that left with `ports/` (the Code the Classics mixer and the
SuperBible `chapt18/texfloat` port). Remove both from `requirements.txt`, re-pin `constraints.txt`, rebuild the image, and run the gates.
Done means: neither name appears in `requirements.txt` or `constraints.txt`, `make image`, `make check-format`, `make type-check` and
`make test` pass, and the image is smaller.

## Context

- **Measured 2026-11-24 on the cleaned tip (branch `tip-cleanup`):** `git grep -n -I -i "miniaudio\|openexr"` outside `tasks/archive`
  finds them in `requirements.txt` (lines 18, 27–29: `miniaudio==1.71`, the `OpenEXR` comment and `OpenEXR==3.5.4`) and
  `constraints.txt` (`miniaudio==1.71`, `openexr==3.5.4`, and the two `# via` comment lines naming them), and in four reference docs
  that describe the moved code (`tasks/reference/code-the-classics-tightening.md`, `design-decisions.md`, `notable-subsystems.md`,
  `gl-and-imgui-gotchas.md`). No file under `src`, `tests`, `tools`, `assignments` or `notebooks` imports either package.
- **`constraints.txt` is generated:** `make update-pins` regenerates it (needs the network). Do not edit it by hand.
- **Possible further removals to check, not assumed:** `miniaudio` has no wheel for the newest Python, so a C++ compiler and the Python
  headers may have been added to the image only to build it (`entrypoint/01-install-base.sh` lists `gcc-g++` and `python3-devel`, and
  wxPython and the other distro `python3-*` packages need their own reasons). Find out why each is there before removing it.
  `imageio-ffmpeg` and `PyOpenGL-accelerate` are also worth a look for the same reason (the question is who imports them).

## Plan

1. Re-run the grep above and confirm nothing imports either package (a failing import is the only thing that would change the plan).
2. Delete the two requirements entries and their comment (`requirements.txt`); run `make update-pins`; read the diff of
   `constraints.txt` (expect exactly those two pins, their comment lines and any transitive pin only they needed).
3. `make image` (full flags), then `make check-format`, `make type-check`, `make test`; compare `podman images` sizes before and after
   and write both in the done-record.
4. Reference docs: leave the four historical passages alone (each file carries a "Historical copy" banner), or add one line where a
   passage says the package is required here. Record which.
5. Stage; the maintainer commits.

## Open questions

1. Also drop the build-only system packages once step 3 shows nothing else needs them (`gcc-g++`, `python3-devel`, and whatever the check in
   Context finds)? Recommend: only after step 3 proves it with a clean `make image`, and as a separate commit so it can be reverted alone.
