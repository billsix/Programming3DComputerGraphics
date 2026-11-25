# Rename `intro3dgraphics` to `programming3dcomputergraphics`, so the package, image and mount path match the repository

**Status:** proposed — needs go-ahead
**Priority:** 5 (cosmetic and cheap while nothing is published under the current name; do after `tasks/fix-ci-lean-image-missing-gcc.md` so CI is green to verify against)
**Difficulty:** 3 (mechanical, 124 files; the earlier rename was one codemod; the extra risk is a 28-character name against the 80-column limit)
**Created:** 2026-11-25 (William Emerison Six <billsix@gmail.com>, from `git config`)

## BLUF

The repository is `github.com/billsix/Programming3DComputerGraphics` but the Python package, image, container mount path, output directory and book paths are all `intro3dgraphics`. Done means every live use of `intro3dgraphics` is `programming3dcomputergraphics` (lowercase, because Python modules and image names must be), the gates and the book build pass in the container, and `git grep -i intro3dgraphics` outside the archive finds nothing live. The earlier rename (`modelviewprojection` to `intro3dgraphics`, commit `e035416e`) is the template, and its codemod can be recovered from git.

## Context

**Why:** the maintainer does not know why the module name differs from the repository name (2026-11-25), and wants them to match. The current name came from the 2026-11-24 rename of the old `modelviewprojection` package, done in the same session that copied history out of github.com/billsix/modelviewprojection (`tasks/archive/2026/11/24/rename-package-modelviewprojection-to-intro3dgraphics.md`, the record of that rename; its "What was done" and "Found by the release check" sections are the checklist this task repeats).

**Read first:**
- `tasks/archive/2026/11/24/rename-package-modelviewprojection-to-intro3dgraphics.md` (method, the traps it found, the verification list).
- The old codemod: `git show e035416e:tasks/adhoc/rename-package-modelviewprojection-to-intro3dgraphics/rename.py` (removed from the tree in `0b488854`). It has four rules over separate file sets, skips `tasks/archive`, `entrypoint/dotfiles`, "Historical copy" reference docs, `README.md` and `CLAUDE.md`, and was run twice to prove idempotency. Copy it to `tasks/adhoc/rename-package-to-programming3dcomputergraphics/`, adapt it, and read the Python coding standard (`python-coding-standard.md` in github.com/billsix/runClaudeInContainer, and `tasks/reference/python-coding-standard-mvp.md`) before editing, because an ad-hoc script is held to it.
- `tasks/fix-ci-lean-image-missing-gcc.md` (the CI fix this follows; both edit `Makefile`/`Dockerfile`-adjacent files, so land that one first).

**Where the name appears now** (counted 2026-11-25 with `git grep -i intro3dgraphics`: 124 tracked files, 669 lines; 5 of those files are under `tasks/archive` and stay as written):

| Area | Files / what changes |
|---|---|
| Package directory | `git mv src/intro3dgraphics src/programming3dcomputergraphics` (about 90 files, 47 of them mention the name); all imports (`from intro3dgraphics.mathutils import ...`), 250 `src/intro3dgraphics` path strings |
| Packaging and tool config | `pyproject.toml` (`name`, the `extra-paths`, per-file ruff ignores for `demos/**`, `wxapp*.py`, `notebooksrc/**`), `pytest.ini` (four `--ignore` paths) |
| Image and paths | `Makefile` (`CONTAINER_NAME`, the mount `-v $(pwd):/intro3dgraphics/`, `REPO_MOUNT`, every `cd /intro3dgraphics`, `IMAGE_REF = ghcr.io/billsix/$(CONTAINER_NAME)` follows automatically), `Dockerfile` (`COPY . /intro3dgraphics`, the editable-install `cd`, the `emacs src/...` history line, comments), `.dockerignore` comment |
| Container scripts | `entrypoint/entrypoint.sh` (20 lines, including `/output/intro3dgraphics/` and the jupytext paths), `format.sh`, `jupyter.sh`, `loadpackages.sh`, `shell.sh`, `spyder.sh` |
| Book | the 21 chapters `book/docs/ch01.rst` to `ch21.rst` plus `mathhomework1.rst` (about 400 `../../src/intro3dgraphics/...` `literalinclude` paths and `intro3dgraphics.mathutils.*` cross-references), `api.rst` (`automodule`), `conf.py` line 47 (`latex_documents` file name `intro3dgraphics.tex`), `book/figures/epix/_scene2d.py` and `_transform_sequence.py` (an import) |
| Tests and tools | `tests/test_mathutils.py` (import), `tests/test_demo22b_gltf_roundtrip.py` (a path), `tools/render_epix_figures.py`, `tools/verify_render.sh` (`localhost/intro3dgraphics`, the `-v ...:/intro3dgraphics` mount, `PYTHONPATH`) |
| Ignore lists | `.gitignore` (the `intro3dgraphics-*.tar` image-export pattern, the generated-artifact comment and `scene.glb` path) |
| Docs | `CLAUDE.md`, `README.md`, 18 reference docs under `tasks/reference/`, 11 open task docs under `tasks/` (the list from `git grep -I -l -i intro3dgraphics -- tasks ':!tasks/archive'`) |
| Release artifacts | file names follow `pyproject.toml` and `CONTAINER_NAME`: `dist/<name>-<version>.{tar.gz,pdf,epub}`, `output/<name>/<name>.pdf` (the `Makefile` `release-book-assets` target expects exactly that path; this is the trap the first rename hit) |

**Must NOT change** (the earlier rename left these, for the same reasons): `ms.MatrixStack.modelviewprojection` (gacalc's enum member) and the `gl_ModelViewProjectionMatrix` GLSL built-in; URLs and "successor of" sentences that name the old repository `github.com/billsix/modelviewprojection`; `tasks/archive/` (history); the "Historical copy" reference docs; `entrypoint/dotfiles/` (vendored); and the `mvpvisualization/` directory and `modelviewperspectiveprojection.py` (kept deliberately by the maintainer, 2026-11-24).

**Other repositories:** none imports the package or calls the image (checked 2026-11-25 across the mounted repos: `geometricalgebra`, `CodeTheClassics`, `OpenGLSuperBibleV4Code`, `dotfiles`, `runClaudeInContainer`, `runCrushInContainer`, `multivariate-math`, `hanoi`, `modelviewprojection`; no match).

**Not yet published under the current name:** `ghcr.io/billsix/intro3dgraphics` has never been pushed (the stack's "container-registry rename" check is pending), and the `0.0.3` tarball was only built locally, so renaming now costs nothing downstream. Three places do mention the GitHub Pages path `billsix.github.io/intro3dgraphics`; they are covered by the existing decision task `tasks/release-book-github-pages-decision.md`.

## Goal

Make `programming3dcomputergraphics` the single name for the Python package, the distribution in `pyproject.toml`, the image (`CONTAINER_NAME`), the in-container repo path (`/programming3dcomputergraphics`), the output directory and release artifact names, and every book and test reference, so a reader of the repository name finds the same string in the code. Nothing about behaviour changes.

## Plan

- [ ] Land `tasks/fix-ci-lean-image-missing-gcc.md` first, and note the baseline: `make format`, `make type-check`, `make test` and `make check-regions` green on `master` with default flags.
- [ ] Recover the old codemod from `e035416e`, adapt its four rules to the new name, save it under `tasks/adhoc/rename-package-to-programming3dcomputergraphics/` with a `discover.sh` and a worklog under `data/`, and keep it idempotent (second run: 0 changes).
- [ ] `git mv src/intro3dgraphics src/programming3dcomputergraphics`, then run the codemod over code, config, book, tests, tools and entrypoint scripts. Leave every "must not change" item above untouched.
- [ ] Update the `Makefile` (`CONTAINER_NAME`, the mount, `REPO_MOUNT`, the `cd` lines), the `Dockerfile` and `tools/verify_render.sh`; check the `ARG`/`--build-arg` pairs still agree.
- [ ] Set `conf.py` `latex_documents` to `programming3dcomputergraphics.tex` so `output/<name>/<name>.pdf` still exists; check `release-book-assets` against the built output.
- [ ] Reformat: run `make format`; ruff wraps code lines the longer name pushes past 80 columns (the name grew 13 characters; a count of 2026-11-25 found 11 `src`/`tests` lines that would cross 80). Then reflow every comment, docstring and `E501` paragraph whole, never leaving an orphaned word. Do not reflow `literalinclude` paths or generated markers.
- [ ] Check each `doc-region-begin`/`doc-region-end` marker the move touched (`make check-regions`).
- [ ] Update `CLAUDE.md`, `README.md`, and the live reference and open task docs. Leave `tasks/archive` and "Historical copy" docs. Add a `CHANGELOG.md` entry only if the repository has one by then (it did not on 2026-11-24).
- [ ] Gates, containerized, default flags, and the lean CI flags: `make check-format`, `make type-check`, `make test`, `make check-regions`, `make docs`, and `tools/verify_render.sh` on `demo05`, `demo22` and `assignments/assignment1.py`; then `make release-artifacts RELEASE_VERSION=0.0.3` and confirm the artifact names.
- [ ] Check `git grep -i intro3dgraphics` outside `tasks/archive`: nothing live remains. In the rebuilt image `import programming3dcomputergraphics.mathutils` works and `import intro3dgraphics` raises `ModuleNotFoundError`.
- [ ] Stage by path and stop; at archive, `git rm` the codemod and its data. Note owed items: rebuild the host image, and tell the maintainer the `ghcr.io/billsix/` name changes before the first push.

## Notes / decisions

- 2026-11-25, `William Emerison Six <billsix@gmail.com>`: scope is the package, `pyproject.toml`, the Dockerfile, the Makefile and image name, the in-container default path, the book references, the tests, and "everything", using the earlier rename's diff to find the parts.
- The name stays lowercase and unhyphenated: Python module names and OCI image names cannot hold capitals, and `Programming3DComputerGraphics` is the repository's display spelling.
- The earlier rename found, only at the release check, that the PDF name came from the project title. The title is not changing here, but the `latex_documents` file name has to move with the package.

## Decisions (answered 2026-11-25, William Emerison Six <billsix@gmail.com>, "yes to all three recommendations")

1. Keep the book and project title "Introduction to 3D Computer Graphics"; only the technical name changes.
2. Use the full module name `programming3dcomputergraphics`, not a short form.
3. Leave the three `billsix.github.io/intro3dgraphics` mentions to `tasks/release-book-github-pages-decision.md`.

## Open questions

None open. The status stays `proposed — needs go-ahead` because the maintainer asked for the task, not yet for the rename itself.
