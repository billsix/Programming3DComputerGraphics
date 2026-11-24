export VIRTUAL_ENV_DISABLE_PROMPT=1
source /venv/bin/activate
cd /intro3dgraphics/
uv pip install --no-deps --no-index --no-build-isolation -e . --python $(which python)
