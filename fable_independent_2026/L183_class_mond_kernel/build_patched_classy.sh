#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
if [ ! -d src/classy-3.3.4.0 ]; then
  cp ../L152_class_running_cs2/src/classy-3.3.4.0.tar.gz src/ 2>/dev/null || pip download classy==3.3.4.0 --no-binary :all: --no-deps -d src
  tar xzf src/classy-3.3.4.0.tar.gz -C src
  python3 apply_mond_kernel_patch.py src/classy-3.3.4.0
  python3 apply_nuprime_patch.py src/classy-3.3.4.0
fi
rm -rf site; pip install --no-deps --no-build-isolation --target site ./src/classy-3.3.4.0 > build.log 2>&1 && echo BUILD_OK || (tail -30 build.log; exit 1)
