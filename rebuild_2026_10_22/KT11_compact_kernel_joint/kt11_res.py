#!/usr/bin/env python3
"""KT11 reported check: rho_crit p = 1 Cassini at two grid resolutions, to see whether 1.024x is resolved. Not a gate."""
import importlib.util, os, sys
os.environ.pop("KT11_MUTATE", None)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt11.py")).read().split("c, Gv = 2.99792458e8")[0]
ns = {"__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt11.py")}
exec(src, ns)
for nv, nm in ((600, 200), (2400, 800)):
    print(f"rho_crit Cassini at {nv},{nm}: {ns['cassini'](1.1279e-10, ns['nu_p1'], 2.0, None, nv, nm):.4f}x")
