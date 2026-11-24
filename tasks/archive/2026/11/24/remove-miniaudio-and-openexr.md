# Remove miniaudio and OpenEXR from the dependencies

**Done:** 2026-11-24 (work commit; the archive move follows). Source: the maintainer (William Emerison Six <billsix@gmail.com>, 2026-11-24)
asked for this follow-up to `tasks/archive/2026/11/24/copy-history-without-ports.md`.

## What was done

`miniaudio==1.71` and `OpenEXR==3.5.4` (with their comments) were deleted from `requirements.txt`, and `constraints.txt` was re-resolved with
`make update-pins`. The diff of `constraints.txt` is exactly the two pins, their `# via -r /tmp/requirements.txt` lines, and the `miniaudio` entry in
`argon2-cffi-bindings`' `# via` list. A grep confirmed first that nothing under `src`, `tests`, `tools`, `assignments` or `notebooks` imports either
package. The four reference docs that mention them (`code-the-classics-tightening.md`, `design-decisions.md`, `notable-subsystems.md`,
`gl-and-imgui-gotchas.md`) were left as written: the first and fourth carry a "Historical copy" banner, and the others describe the audio mixer
and the EXR reader as part of the moved code.

## Verification (container, default flags, 2026-11-24)

`make image` rebuilt; `make check-format` exit 0; `make type-check` exit 0; `make test` 55 passed. Image size: 6.8 GB before, 6.79 GB after, so the
removal saves almost nothing (both packages are small); the gain is a shorter dependency list and no source build of `miniaudio` on the newest Python.

## Owed (optional, was open question 1)

Whether to drop the system packages that may have been installed only to build `miniaudio` from source (`gcc-g++`, `python3-devel` in
`entrypoint/01-install-base.sh`) was **not** answered and **not** done. Find out who else needs them (wxPython and the other distro packages
have their own reasons), remove them in a separate commit, and prove it with a clean `make image`. `imageio-ffmpeg` and `PyOpenGL-accelerate` are
worth the same question.
