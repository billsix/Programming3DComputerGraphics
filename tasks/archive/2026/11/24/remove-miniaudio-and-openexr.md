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

## Follow-up: the build-only system packages (open question 1, answered "yes, drop them" on 2026-11-24)

`gcc-g++` and `python3-devel` are gone from `entrypoint/01-install-base.sh`. The clean `make image` that the plan required before dropping them showed
who still needs them: with both removed the build failed in the ePiX layer, `fatal error: Python.h: No such file`, because ePiX's Python front-end is a
nanobind extension. So the compiler and the headers were never build-only for `miniaudio`; they belong to the layers that compile something. The
change that was made:

- `python3-devel` moved into `entrypoint/epix/install-epix-deps.sh` (which already installs `gcc-c++` for the same layer), and that script's header
  comment now says what each layer provides.
- `gcc-g++` was dropped outright: the docs layer (`02-install-docs.sh`) installs `g++` and `gcc` itself, and the ePiX layer installs `gcc-c++`.
- The main venv layer needed neither: `PyOpenGL-accelerate`, `mathjax` and `pyyaml` installed in a build without them.

Verification (container, 2026-11-24): the full image (default flags) built; `make check-format`, `make type-check`, `make test`, `make check-regions` and
`make docs` (which renders the ePiX figures) all exit 0; and the CI configuration (`BUILD_DOCS=0 USE_EMACS=0 USE_JUPYTER=0 USE_X_WINDOWS=0`, ePiX
still on) also builds and passes `check-format`, `type-check` and `test`. Not tried: `USE_EPIX=0` together with the other flags off.

`imageio-ffmpeg` was not looked at (nothing in this task depended on it).
