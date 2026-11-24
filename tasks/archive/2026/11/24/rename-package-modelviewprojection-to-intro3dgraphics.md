# The package `modelviewprojection` is now `intro3dgraphics`, the container too, and the book is retitled

**Done:** 2026-11-24 (work commit; the archive move follows). Source: the maintainer (William Emerison Six <billsix@gmail.com>, 2026-11-24).
Follow-up to `tasks/archive/2026/11/24/copy-history-without-ports.md`. The maintainer answered all six questions the same day: the package,
container and mount-path renames, keeping `mvpvisualization/` and `modelviewperspectiveprojection.py`, leaving the version at `0.0.3` with no
`CHANGELOG.md`, leaving history-recording docs alone, and (the one change from my recommendation) retitling the book and project
**"Introduction to 3D Computer Graphics"**.

## What was done

- **Package:** `git mv src/modelviewprojection src/intro3dgraphics` (87 files) and every import, config path, book reference and doc path, by
  `tasks/adhoc/rename-package-modelviewprojection-to-intro3dgraphics/rename.py` (117 files; second run: 0 changes; removed in the archive commit).
  It skips `tasks/archive`, `entrypoint/dotfiles`, the "Historical copy" reference docs, `README.md` and `CLAUDE.md`, and it does not touch
  `ms.MatrixStack.modelviewprojection` (gacalc's enum member, still used by `demo21`, `demo22`, `demo22b` and `util/shaderutils.py`) or URLs of
  the old repository.
- **Container and paths:** `CONTAINER_NAME = intro3dgraphics` (the image is `localhost/intro3dgraphics`), the mount path `/mvp` is `/intro3dgraphics`
  everywhere it was live (`Makefile`, `Dockerfile`, `entrypoint/*.sh`, `tools/`, `CLAUDE.md`), and the build output directory is
  `output/intro3dgraphics/`. The three stale `emacs src/…/mathutils{1,2,3}d.py` shell-history lines in the `Dockerfile` (the files no longer exist) were deleted; the
  `mathutils.py` line stays.
- **Title:** `book/docs/conf.py` `project`, the `index.rst` title and header, `README.md`, the `pyproject.toml` description, the `mathutils.py`
  docstring, and the 35 window titles (`"Introduction to 3D Computer Graphics Demo N"`). The ch01 joke about the old title now reads "this book is
  about the model, the view, and the projection. :-)". The rule that moved titles made five lines in `demo19a`–`19e` longer than 80 columns;
  `ruff format` wrapped them (arguments one per line).
- **Found by the release check, not by the plan:** `make release-book-assets` copies `output/$(CONTAINER_NAME)/$(CONTAINER_NAME).pdf`, which had only
  matched because the old project title happened to produce `modelviewprojection.pdf`. After the retitle Sphinx named the PDF
  `introductionto3dcomputergraphics.pdf`, so the release would have failed with "book PDF … missing". `book/docs/conf.py` now sets
  `latex_documents` to `intro3dgraphics.tex`, and the `Makefile` comment says so. The EPUB is `Introductionto3DComputerGraphics.epub` (the release
  step globs `*.epub`).
- **Docs:** `CLAUDE.md` and `README.md` (title, package, paths), the titles and project-name prose of `tasks/README.md` and six reference docs
  (`architecture-overview`, `design-decisions`, `python-coding-standard-mvp`, `tests-and-gates`, `notable-subsystems`,
  `library-not-framework-authorship-style`).

## Verification (container, default flags, 2026-11-24)

- `make check-format` exit 0 (after the wrap above), `make type-check` exit 0, `make test` 55 passed, `make check-regions` OK.
- `make docs` exit 0; Sphinx's three warnings are the same kinds that were there before (two duplicate toctree entries, one short title underline),
  none about an unresolved `intro3dgraphics` role or reference; no `modelviewprojection` appears in the log.
- In the rebuilt image `import intro3dgraphics.mathutils` works and `import modelviewprojection` raises `ModuleNotFoundError`.
- `tools/verify_render.sh` PASS on `demo05`, `demo22` and `assignments/assignment1.py` (Xvfb).
- `make release-artifacts RELEASE_VERSION=0.0.3`: `dist/intro3dgraphics-0.0.3.{tar.gz,pdf,epub}` and `-html.zip` were produced.
- `git grep -i modelviewprojection` outside `tasks/archive` and `entrypoint/dotfiles` now finds only: the three enum uses above and the
  `gl_ModelViewProjectionMatrix` GLSL built-in (both correct), the old-repository URLs and "successor of" sentences, the "Historical copy" reference
  docs, `book/docs/mvp_dict.pws` (a spelling dictionary), and `tasks/github-actions-release-ci.md` (it describes the old registry name).

## Not done, and consequences

- **The release registry name changes:** `IMAGE_REF` is `ghcr.io/billsix/$(CONTAINER_NAME)`, so `make image-push` will now publish
  `ghcr.io/billsix/intro3dgraphics`, a new package (private by default, as `tasks/github-actions-release-ci.md` describes). `make image-push` itself
  was not run (it pushes). That task document still names the old registry and tarball.
- **`mvp` as a word:** 116 mentions in 40 files remain outside `tasks/archive` (mostly open tasks and reference docs, where it names the repository);
  only the titles and obvious project-name sentences were changed (plan row 10 asked for the repository nickname in `CLAUDE.md`, `README.md` and
  open docs). `book/docs/mvp_dict.pws` is unchanged. The `/mvp` path remains in `tasks/reference/tests-and-gates.md` (a historical-copy doc).
- No display run of a demo or assignment beyond the headless render gate; `make docs` and the release were run with the working tree staged but
  not committed (the tarball uses `git archive HEAD`, so its source content is the previous commit, only its names and layout are proved).

## Owed

The maintainer merges the branch `remove-deps-and-rename` (it is cut from `tip-cleanup`, so that branch merges first) and rebuilds the image.
Nothing else in other repositories needs to change (checked 2026-11-24: none imports the package or calls the image).
