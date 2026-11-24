#!/bin/env bash

export VIRTUAL_ENV_DISABLE_PROMPT=1
# Activate the container's venv when it exists; outside the container (running
# format.sh from the repo root on the host) it's absent -- use the caller's env.
# Every path below is RELATIVE to the repo root, so format.sh runs identically
# in the container (cd /mvp) and on the host (cd <repo>) -- see the .extrabashrc
# exit hook, which cd's to the project root before calling it.
[ -f /venv/bin/activate ] && source /venv/bin/activate

# Fail-on-any-step (2026-07-09): every step runs (so one pass reports ALL
# the red, not just the first), and the script exits nonzero if ANY step
# failed.  Before this, the exit code was the LAST command's alone, so the
# gate could report green off the final ty check while earlier steps were
# red -- which is exactly how 79 src diagnostics hid for weeks (see
# tasks/archive/2026/07/09/src-ty-diagnostics-after-ty-bump.md).
status=0
run() { "$@" || status=1; }

run ruff check assignments --fix
run ruff check src --fix
run ruff check tests --fix
run ruff format assignments
run ruff format src
run ruff format tests
run ty check src
run ty check tests

exit $status
