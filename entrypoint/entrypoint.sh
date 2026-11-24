#!/bin/env bash

export VIRTUAL_ENV_DISABLE_PROMPT=1
source /venv/bin/activate

cd /intro3dgraphics/ && pytest --exitfirst --disable-warnings || exit

cd /intro3dgraphics/
jupytext --to notebook src/intro3dgraphics/notebooksrc/plot2d.py --output  assignments/demo02/plot2d.ipynb
jupytext --to notebook src/intro3dgraphics/notebooksrc/plot2d.py --output book/docs/plot2d.ipynb

jupytext --to notebook src/intro3dgraphics/notebooksrc/framebuffer.py --output notebooks/framebuffer.ipynb
jupytext --to notebook src/intro3dgraphics/notebooksrc/framebuffer.py --output book/docs/framebuffer.ipynb

jupytext --to notebook src/intro3dgraphics/notebooksrc/ndc.py --output notebooks/ndc.ipynb
jupytext --to notebook src/intro3dgraphics/notebooksrc/ndc.py --output book/docs/ndc.ipynb

# Install into the ACTIVE venv (which has setuptools/wheel, seeded by the
# Dockerfile), not --system: --system targets /usr, which has no setuptools, so
# the editable build fails.  The package must be importable for the ePiX figures,
# which drive intro3dgraphics.mathutils.  Matches loadpackages.sh.
uv pip install --no-deps --no-index --no-build-isolation -e . --python "$(which python)"

# Render the book's ePiX figures (book/figures/epix/*.py) into _static/epix/ before
# Sphinx runs.  These replaced the old gnuplot + matplotlib book figures; they need
# the package installed above (they drive mathutils) and ePiX in the image
# (USE_EPIX=1, the default).  The graphviz (.dot) and texExpToPng (.tex) figures are
# still built by book/docs/_static/Makefile during the Sphinx make below.
python tools/render_epix_figures.py || exit

# Populate the docs-only gacalc source tree (baked into the image at
# /opt/gacalc-src by the Dockerfile) so the book's literalinclude directives can
# reference gacalc's doc-region markers.  Gitignored, docs-only, never imported.
mkdir -p /intro3dgraphics/book/docs/_gacalc_src
cp /opt/gacalc-src/*.py /intro3dgraphics/book/docs/_gacalc_src/

# Now that the gacalc source is present, verify every book doc-region anchor
# resolves (and no name collisions) before building -- a broken anchor renders
# an empty listing silently, so fail the build loudly instead.
cd /intro3dgraphics && python tools/check_doc_regions.py || exit

cd /intro3dgraphics/book/docs
make html
make latexpdf
make epub

# copy the files over
mkdir -p /output/intro3dgraphics

# fix issues that github has for displaying the pages for me
cp -r _build/html/ /output/intro3dgraphics/
cp -r _build/latex/*pdf /output/intro3dgraphics/
cp -r _build/epub/*epub /output/intro3dgraphics/
# see if this fixes github issue with unscores in
# filenames created by sphinx
touch /output/intro3dgraphics/.nojekyll
