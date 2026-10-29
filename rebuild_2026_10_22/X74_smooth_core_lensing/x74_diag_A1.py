#!/usr/bin/env python3
"""X74 reported-only: X53's AMENDMENT A1 profile (common / per-bin shift in log M200, truncated vs untruncated, with 2h)
run on the smooth-core source, by executing X53's committed x53_diag_A1.py with its source swapped for the X74-patched text.
kappa = 1/2 FITTED; not theory closed.     PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_diag_A1.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos")
src = open(os.path.join(X53D, "x53_outer_lensing.py")).read()
for a, b in (("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n",
              "def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n"),
             ("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n"),
             ("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5")):
    assert src.count(a) == 1; src = src.replace(a, b)
d = open(os.path.join(X53D, "x53_diag_A1.py")).read()
for a, b in (('T = open(SRC).read()', 'T = PATCHED'),
             ('os.path.join(HERE, "x53_diag_A1.out")', repr(os.path.join(HERE, "x74_diag_A1_S.out"))),
             ('os.path.join(HERE, "x53_diag_A1_results.json")', repr(os.path.join(HERE, "x74_diag_A1_S_results.json")))):
    assert d.count(a) == 1; d = d.replace(a, b)
ns = {"__file__": os.path.join(X53D, "x53_diag_A1.py"), "__name__": "__main__", "PATCHED": src}
exec(compile(d, ns["__file__"], "exec"), ns)
