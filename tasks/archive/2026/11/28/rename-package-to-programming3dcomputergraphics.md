# Renamed `intro3dgraphics` to `programming3dcomputergraphics`: the package, image and mount path match the repository

**Done 2026-11-28** (agent. Created 2026-11-25 by William Emerison Six <billsix@gmail.com>; his go-ahead
2026-11-28: "make a branch, temporarily turn gpg signing off, and implement that task … do the work, commit
it, archive it, and tell me when it's ready to merge").

## What changed

`programming3dcomputergraphics` is now the one name for the Python package (`src/programming3dcomputergraphics/`),
the distribution in `pyproject.toml`, the image (`CONTAINER_NAME`, and with it `ghcr.io/billsix/<name>`), the
in-container repository path (`/programming3dcomputergraphics`), the output directory, the book's file name
(`latex_documents` in `book/docs/conf.py`) and the release artifacts. Behaviour is unchanged. The name was
`intro3dgraphics` since 2026-11-24 and `modelviewprojection` before that
(`tasks/archive/2026/11/24/rename-package-modelviewprojection-to-intro3dgraphics.md`).

- **Directory:** `git mv src/intro3dgraphics src/programming3dcomputergraphics` (89 files moved).
- **The word:** `tasks/adhoc/rename-package-to-programming3dcomputergraphics/rename.py` replaced it in 119
  tracked text files (imports, path strings, `pyproject.toml`, `pytest.ini`, `Makefile`, `Dockerfile`, the
  entrypoint scripts, the 21 book chapters, `mathhomework1.rst` and `api.rst`, the tests and tools, `.gitignore`, `README.md`,
  `CLAUDE.md`, the live reference docs and open tasks). A second run changed nothing. The worklog of every
  line before the change was `data/before.txt` beside it (686 lines in 125 files); the script, its
  `discover.sh` and the worklog are deleted with the archive commit.
- **Reflowed:** seven files under `src/` where the longer name pushed a comment or docstring past 80 columns
  (the "is imported from …" comments of demos 22 to 24, `export_scene.py`, `util/shading.py`), each paragraph
  reflowed whole, and one comment in `entrypoint/format.sh`. `ruff format` wrapped the two import lines and
  the one string argument that no longer fit.

## Decisions (William Emerison Six <billsix@gmail.com>, 2026-11-25: "yes to all three recommendations")

1. The book and project title stays "Introduction to 3D Computer Graphics"; only the technical name changed.
2. The full name `programming3dcomputergraphics`, not a short form. It is lowercase and unhyphenated because
   Python module names and image names cannot hold capitals.
3. The three mentions of the GitHub Pages path `billsix.github.io/intro3dgraphics` are left to
   `tasks/release-book-github-pages-decision.md`.

## Left unchanged, on purpose

`tasks/archive/` (history); `entrypoint/dotfiles/` (vendored); the "Historical copy" reference docs (none of
them held the word); the three Pages-path mentions above; `ms.MatrixStack.modelviewprojection`, the GLSL
built-in `gl_ModelViewProjectionMatrix`, the URLs of the old repository, the `mvpvisualization/` directory
and `modelviewperspectiveprojection.py`, none of which contain the renamed word.

## Verification (2026-11-28, nested, in an image built that day under the new name)

- **Before the change**, on `master` with the existing image: `format.sh`, the type-check steps, `pytest`
  (55 passed) and `tools/check_doc_regions.py` all passed.
- **After:** the same four pass in the new image (full flags): format, `ty` over `src` and `tests` with
  `tools/check_local_annotations.py --include-module`, `pytest` (55 passed), and the doc-region check.
- `make docs`: the book built as HTML, PDF and EPUB into `output/programming3dcomputergraphics/`, with
  `programming3dcomputergraphics.pdf`.
- `tools/verify_render.sh` on `demos/demo05.py`, `demos/demo22/demo22.py` and `assignments/assignment1.py`:
  PASS each, under Xvfb.
- `make release-artifacts RELEASE_VERSION=0.0.3`: `dist/programming3dcomputergraphics-0.0.3.tar.gz`, `.pdf`,
  `.epub` and `-html.zip`.
- In the image, `import programming3dcomputergraphics.mathutils` resolves to
  `/programming3dcomputergraphics/src/…` and `import intro3dgraphics` raises `ModuleNotFoundError`.
- `git grep -i intro3dgraphics` outside `tasks/archive` finds the word only in `CLAUDE.md` (the sentence
  that records the old names) and the three Pages-path mentions.
- CI's own commands, `make check-format type-check BUILD_DOCS=0 USE_EMACS=0 USE_JUPYTER=0 USE_X_WINDOWS=0`,
  run nested against a lean image built for the check under a throwaway tag (`CONTAINER_NAME=p3d-lean-check`,
  so the full image kept its name): both pass. The first run failed at `check-format`'s closing
  `git diff --exit-code` only because this record was edited and not yet staged.

## Found on the way

- **A stale PDF in the output directory.** `output/programming3dcomputergraphics/` also holds an
  `intro3dgraphics.pdf`: the book build copies every PDF out of the gitignored `book/docs/_build/latex/`,
  which still held the PDF of an earlier build in this working copy. A clean checkout has no such file, and
  the release target takes the PDF by its exact name. The old gitignored `output/intro3dgraphics/` directory
  is left in place too. Both are the maintainer's to delete.
- **No `CHANGELOG.md`** exists in the repository, so none was written.

## Not done, the maintainer's

- Rebuild the image on the host (`make image`): the host's image is still named `intro3dgraphics`, and the
  old tag can be removed with `podman rmi intro3dgraphics`.
- The registry name becomes `ghcr.io/billsix/programming3dcomputergraphics`. Nothing was ever pushed under
  the old name, so there is nothing to migrate.
- The display checks of the demos stay his; the render check proves three scripts draw, headlessly.
