# The lean CI image has `gcc` and `python3-devel`, so `PyOpenGL-accelerate` builds and the `checks` workflow can run

**Done:** 2026-11-25 (the work is in squash commit `72276ebd`). Source: the maintainer (William Emerison Six <billsix@gmail.com>, 2026-11-25), who asked why CI failed, chose option (a) below, and said "go".

## What was wrong

Every `checks` run on GitHub (`.github/workflows/checks.yml`, jobs `format` and `type`) had failed since the first run on 2026-11-24 (runs 1 to 4, most recent head `f60335fb`). Both jobs failed at the `make` step with only "Process completed with exit code 2", which says nothing, because `make` exits 2 on any failed recipe. GitHub's job logs return 403 to anonymous callers, so the cause was found by reproducing nested in the sandbox with CI's exact command (`make check-format BUILD_DOCS=0 USE_EMACS=0 USE_JUPYTER=0 USE_X_WINDOWS=0`, and the same for `type-check`).

Both ended `make: *** [Makefile:107: image] Error 1` at Dockerfile STEP 13, the `uv pip install` of `requirements.txt` into `/venv`: `Building pyopengl-accelerate==3.1.10` then `error: [Errno 2] No such file or directory: 'gcc'`. The base image is `registry.fedoraproject.org/fedora:45` (Python 3.15), and `PyOpenGL-accelerate==3.1.10` was built from source, so it needed a compiler. Whether PyPI has no wheel for Python 3.15 was inferred from the source build, not checked. `gcc`, `g++` and `make` came only from `entrypoint/02-install-docs.sh`, which the `Dockerfile` runs only when `BUILD_DOCS=1`. CI passes `BUILD_DOCS=0`, so the CI image had no compiler. The default full image has `BUILD_DOCS=1`, which is why local work never saw it. The package was added to `requirements.txt` in `ca565ed0` ("updated build", 2026-11-11); the first CI run after that was the first red one.

Ruled out: the `nameAndScope` merge (runs 1 and 2 predate it and were already red) and the ePiX layer (the build never reached it; `USE_EPIX` defaults on and `checks.yml` does not turn it off, and the layer built fine once the compiler was present).

## Options considered, and the choice

- **(a) Install `gcc` and `python3-devel` in `entrypoint/01-install-base.sh`.** Chosen by the maintainer. The compiler joins the always-installed base, so every flavour (lean, full, nested) can build any sdist-only pin; the lean image grows by the size of `gcc` and the Python headers.
- **(b) Drop `PyOpenGL-accelerate` from `requirements.txt`**, then `make update-pins`. It is an optional speedup, so nothing breaks, but it was added on purpose.
- **(c) Add `BUILD_DOCS=1` to both CI jobs.** Fixes it, but puts TeX Live and Sphinx in CI and defeats the lean image.
- **(d) Pin `PyOpenGL-accelerate` to a release that ships a wheel for the image's Python.** Not investigated.
- **(e) Install `gcc` inline in the CI jobs or behind a new flag.** Breaks "CI is a thin wrapper over make", or adds a fifth knob for one package.

## What was done

- `gcc` and `python3-devel` were added to the alphabetical `dnf install` list in `entrypoint/01-install-base.sh` (mode 755 kept). The edit shipped in the maintainer's squash commit `72276ebd`, together with the task documents.
- `python3-devel` was added together with `gcc` because the build needs `Python.h`; the rebuild showed no further header was missing.

## Verification (nested, 2026-11-25)

- Lean, CI flags: `make check-format` exit 0 and `make type-check` exit 0. The image builds, `PyOpenGL-accelerate` compiles, the ePiX layer builds, `ruff` and `ty` pass, and `git diff --exit-code` is clean.
- Default flags (full image): `make type-check` exit 0.

## Result on GitHub

The `checks` run for `72276ebd` (run 5) passed, both jobs.

## Not done

`checks.yml` still lists four feature flags by hand instead of passing `MINIMAL_IMAGE=1`, so a new feature flag can still leave the lean set out of date; and it still builds ePiX in CI, which neither gate uses. Both were noted, not changed.
