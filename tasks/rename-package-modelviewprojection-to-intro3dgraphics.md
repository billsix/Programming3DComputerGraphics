# Rename the package `modelviewprojection` to `intro3dgraphics` (and the container, the title, and the other uses of the name)

**Status:** proposed — needs go-ahead (filed 2026-11-24; every open question answered 2026-11-24)
**Priority:** 6
**Difficulty:** 5
**Created:** 2026-11-24
**Source:** the maintainer (William Emerison Six <billsix@gmail.com>, 2026-11-24) asked for the package rename, the container-name
change, and a searched list of recommendations for every other use of the name. Follow-up to
`tasks/archive/2026/11/24/copy-history-without-ports.md`.

## BLUF

The repository is now `Programming3DComputerGraphics`; the Python package, the image and several paths still say `modelviewprojection`
(or its nickname `mvp`). Rename the package to **`intro3dgraphics`** (`src/modelviewprojection/` → `src/intro3dgraphics/`, 87 tracked
files, every import), the container image to `intro3dgraphics`, and the book's and project's title to **"Introduction to 3D Computer
Graphics"**, in one sweep proved by the gates. Several uses of the word
must **not** change (below). Done means: `git grep -i modelviewprojection` outside `tasks/archive` and the files listed under "Leave alone"
finds nothing, `make image`, `make check-format`, `make type-check`, `make test` and `make docs` pass, and the book builds with the new
paths.

## Context: every use of the name, searched 2026-11-24 (cleaned tip, branch `tip-cleanup`), with a recommendation

Counts are `git grep -I -i modelviewprojection` hits; the totals are 359 in `tasks/archive`, 348 in `book`, 166 in `src`, 53 in
`tasks/reference`, 46 in open `tasks`, 13 in `entrypoint`, 11 in `assignments`, and a few each in config, docs and tools.

| # | Use | Where (count) | Recommendation |
|---|---|---|---|
| 1 | **The package directory** | `src/modelviewprojection/` (87 tracked files) | `git mv` to `src/intro3dgraphics/`. |
| 2 | **Imports** (`from modelviewprojection…`, `import modelviewprojection…`) | `src`: 124 lines in 43 files; `assignments`: 3 files; `tests`: `test_mathutils.py`; docstring mentions in `tools/render_epix_figures.py` | Rewrite every one to `intro3dgraphics`. |
| 3 | **Packaging and tool config** | `pyproject.toml` (`name`, `extra-paths`, four per-file-ignore globs, description), `pytest.ini` (four `--ignore` paths), `.gitignore` (4), `entrypoint/loadpackages.sh` installs the package editable | Rename the paths and the project `name`; keep `setup.py` (it has no name). Reinstall editable in the image; delete any stale `*.egg-info`. |
| 4 | **The book's file references** | `book/docs`: 314 occurrences in 21 files (`literalinclude:: ../../src/modelviewprojection/demos/demoNN.py`, `:caption:`, "Load src/… in Spyder") | Rewrite the paths. The `doc-region` markers are by name, so listings do not move. |
| 5 | **The book's API cross-references** | `api.rst` `automodule:: modelviewprojection.mathutils`; `:py:meth:` / `:class:` roles and doctests (`>>> from modelviewprojection.mathutils import rotate`): 30 occurrences in 7 files | Rewrite; then `make docs` and read the Sphinx warnings (an unresolved role is silent in HTML). |
| 6 | **Image / container name** | `Makefile:22` `CONTAINER_NAME = modelviewprojection` (the Dockerfile itself carries no image name; its four hits are `~/.bash_history` lines), `tools/verify_render.sh` default `localhost/modelviewprojection`, `.gitignore` `modelviewprojection-*.tar` (`make image-export`) | Rename to `intro3dgraphics`. The four Dockerfile `emacs src/modelviewprojection/mathutils3d.py` history lines name files that no longer exist (`mathutils1d/2d/3d.py`): delete them rather than rename. |
| 7 | **Container mount path `/mvp`** | `Makefile` (12), `Dockerfile` (4), `entrypoint/*.sh` (`entrypoint.sh`, `shell.sh`, `spyder.sh`, `loadpackages.sh`, `jupyter.sh`, `format.sh`), `tools/verify_render.sh`, `tools/verify_dockerfile_permutations.sh`: 30 occurrences in 9 files | Rename to `/intro3dgraphics` in the same sweep (question 2). Other repositories' scripts that call this image by path (none found; see row 14) would need the same. |
| 8 | **Build output directory and release names** | `entrypoint/entrypoint.sh` `/output/modelviewprojection/{html,pdf,epub}` and `.nojekyll`; `.github/workflows/release.yml` and `tasks/github-actions-release-ci.md` (`output/modelviewprojection/`, `dist/modelviewprojection-<version>.tar.gz`) | Rename to `intro3dgraphics`; the release workflow and the Makefile `release-*` targets must agree, so change them together and run the workflow's steps locally. |
| 9 | **The book's and project's title** | `book/docs/conf.py` `project = "Model View Projection"` (Sphinx derives the PDF, EPUB and HTML titles and file names from it), `README.md` title "ModelViewProjection", `pyproject.toml` description, `book/docs/ch01.rst:376` ("the book is called ModelViewProjection :-)"), window titles `"ModelViewProjection Demo N"` (35 strings in 35 files across `src` and `assignments`) | **Retitle to "Introduction to 3D Computer Graphics"** (maintainer's decision, question 3). Window titles become `"Introduction to 3D Computer Graphics Demo N"` (say so if a shorter window title is wanted). The ch01 sentence is a joke about the old name and needs rewriting, not replacing. Expect the built PDF and EPUB file names to change; check `release.yml` globs (`dist/*.pdf`, `dist/*.epub`) still match. |
| 10 | **The nickname `mvp`** | `CLAUDE.md` title "MVP — context for Claude", about 100 mentions in open tasks and reference docs, `book/docs/mvp_dict.pws` (spelling dictionary), a few comments in `src` and `tests` | Replace the nickname for the *repository* ("the course repository", or the new name) in `CLAUDE.md`, `README.md` and open docs; leave the spelling dictionary alone unless the term leaves the book. |
| 11 | **`src/…/mvpvisualization/` and `modelviewperspectiveprojection.py`** | 48 references in 21 files, plus 14 for the module `modelviewperspectiveprojection` | **Keep** (question 4). "MVP" here is the graphics acronym for the model-view-projection pipeline, which the visualization teaches; it is not the repository name. |
| 12 | **`MatrixStack.modelviewprojection`** | `ms.get_current_matrix(ms.MatrixStack.modelviewprojection)` in `demo21`, `demo22`, `demo22b` (4 hits) | **Do NOT change.** It is gacalc's enum member naming the OpenGL matrix; a blind replace would break these demos at run time. The codemod must skip it. |
| 13 | **Docs that cite the old repository** | `CLAUDE.md` and `README.md` (the "successor of `github.com/billsix/modelviewprojection`" sentences), `tools/check_local_annotations.py` docstring URL, `tasks/archive` (359 hits in 112 files), the eight historical-copy reference docs | **Leave alone**: these name the old repository on purpose or record history. Update the URL in `tools/check_local_annotations.py` only if it points at the old repository for a reason other than provenance. |
| 14 | **Other repositories** | `geometricalgebra` (66 mentions, e.g. `CLAUDE.md`, `tasks/reference/design-decisions.md`), `multivariate-math` (`src/crossproduct/_labels.py` docstring), `impo`, `imps`, `hanoi`, `runClaudeInContainer`, `runCrushInContainer`, `dotfiles`, `OpenGLSuperBibleV4Code`, `CodeTheClassics`, `sb7code` | Checked 2026-11-24: **none imports the package or calls the image** (all are comments or history). No coordinated change is needed; do not touch them in this task. |

**Gotchas for the sweep**
- Row 9 is a different string from the package name (`ModelViewProjection`, `Model View Projection`): handle it with its own list, not the
  package codemod, and keep `modelviewperspectiveprojection` and `MatrixStack.modelviewprojection` untouched.
- Replace the *package* name with word boundaries and skip row 12; never run a blanket `sed s/modelviewprojection/…/` over the tree (it would
  also rewrite `tasks/archive`, the `entrypoint/dotfiles` vendored tree and gacalc's enum).
- Save the codemod under `tasks/adhoc/rename-package-modelviewprojection-to-intro3dgraphics/` (annotated Python, idempotent: a second
  run changes nothing), over an explicit file list built from rows 2 to 8, 10 (repository nickname only) and the open docs.
- The image has the package installed editable; a stale install keeps importing `modelviewprojection` from `/venv` and hides a missed
  import. After the rename run `make image` (not a cached shell) and `python -c "import modelviewprojection"` must fail.
- `book/docs` generated notebooks (`*.ipynb` from jupytext) are produced by `entrypoint/entrypoint.sh` from `src/…/notebooksrc/`; regenerate,
  do not edit.
- This is a breaking rename for anyone who pins `modelviewprojection==0.0.3` from the old repository; none of the other repositories do
  (row 14). See question 5 for the version.

## Plan (each phase is a staging boundary)

1. Do `tasks/remove-miniaudio-and-openexr.md` first (smaller, and it touches `requirements.txt` and `pyproject.toml` too).
2. Write the codemod; run it; prove idempotency (second run: zero changes); `git diff --stat` shows only the expected paths.
3. Apply rows 3, 6, 7, 8 by hand (config, Makefile, Dockerfile, entrypoints, workflow); delete the four stale Dockerfile history lines.
4. `make image`; then `make check-format`, `make type-check`, `make test`, `make check-regions`, `make docs` (read every warning), and the
   release workflow's `make release-*` steps locally.
5. Run a demo and an assignment on a display (they import the package) and the headless render gate `tools/verify_render.sh` on two demos.
6. Update `CLAUDE.md`, `README.md`, open tasks and reference docs (rows 10 and 13 apply); record the final `git grep` result in the done-record.
7. Stage; the maintainer commits.

## Open questions

All answered 2026-11-24 by the maintainer, William Emerison Six <billsix@gmail.com> ("what you recommend except for 3"):

1. Package `intro3dgraphics`; container name = `CONTAINER_NAME` in the `Makefile` (yes).
2. Rename the mount path `/mvp` to `/intro3dgraphics` in the same sweep (yes).
3. **Not the recommendation:** the title becomes "Introduction to 3D Computer Graphics" (row 9), instead of keeping "Model View Projection".
4. Keep `mvpvisualization/` and `modelviewperspectiveprojection.py` (yes).
5. Leave the version at `0.0.3` and start no `CHANGELOG.md` (yes).
6. Leave the history-recording docs naming the old package (yes).
