#!/usr/bin/env bash
# L152 -- build a PATCHED classy 3.3.4.0 (running fluid sound speed) into ./site, without touching the
# system-wide classy.  The L152_*.py scripts prepend ./site to sys.path.  Needs: pip, a C compiler, make,
# numpy + cython already importable (built with --no-build-isolation so the numpy ABI matches the interpreter).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
mkdir -p src
if [ ! -d src/classy-3.3.4.0 ]; then
  pip download classy==3.3.4.0 --no-binary :all: --no-deps -d src
  tar xzf src/classy-3.3.4.0.tar.gz -C src
  python3 apply_running_cs2_patch.py src/classy-3.3.4.0
fi
rm -rf site
pip install --no-deps --no-build-isolation --target site ./src/classy-3.3.4.0
python3 - <<'PY'
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath("build_patched_classy.sh")), "site"))
from classy import Class
c = Class(); c.set({'output':'tCl','Omega_fld':0.3,'w0_fld':-1e-4,'cs2_fld':1e-6,'cs2_fld_p':3.0,'use_ppf':'no','omega_cdm':0.001}); c.compute()
print("patched classy imports and accepts cs2_fld_p: OK")
PY
