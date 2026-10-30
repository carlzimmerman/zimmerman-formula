#!/usr/bin/env python3
"""X76 lensing, reported only: X53's AMENDMENT A1 profile run on the fair-share source; the profiled shift is the log budget
multiplier on M_b,tot (grid -0.5..1.7, step 0.05). Also MUTATE: m = +1 must raise Delta Sigma at 100 kpc.
kappa = 1/2 FITTED; not theory closed.    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_lens_profile.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); sys.path.insert(0, HERE)
import numpy as np, x76_patch as XP
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos")
src = XP.patch(open(os.path.join(X53D, "x53_outer_lensing.py")).read())
d = open(os.path.join(X53D, "x53_diag_A1.py")).read()
for a, b in (('T = open(SRC).read()', 'T = PATCHED'),
             ('NS = {"__file__": SRC, "__name__": "x53_ro"}', 'NS = {"__file__": SRC, "__name__": "x53_ro"}; NS.update(X76G)'),
             ('SH = np.round(np.arange(-0.3, 1.2001, 0.05), 2)', 'SH = np.round(np.arange(-0.5, 1.7001, 0.05), 2)'),
             ('os.path.join(HERE, "x53_diag_A1.out")', repr(os.path.join(HERE, "x76_lens_profile.out"))),
             ('os.path.join(HERE, "x53_diag_A1_results.json")', repr(os.path.join(HERE, "x76_lens_profile_results.json")))):
    assert d.count(a) == 1, a[:40]; d = d.replace(a, b)
g = {"__file__": os.path.join(X53D, "x53_diag_A1.py"), "__name__": "__main__", "PATCHED": src, "X76G": XP.ns_globals(True, 0.285)}
exec(compile(d, g["__file__"], "exec"), g)
NS = g["NS"]; HP = dict(NS["H_PRIMARY"]); Rn = NS["Rn"]
m0 = NS["stack_H"]("canonical", HP)[0]; m1 = NS["stack_H"]("canonical", dict(HP, dlM=1.0))[0]
i100 = [int(np.argmin(np.abs(Rn[b] - 0.1))) for b in range(4)]
up = all(m1[b, i100[b]] > m0[b, i100[b]] for b in range(4))
line = f"MUTATE m=+1 raises Delta Sigma near 100 kpc in all bins: {'PASS' if up else 'FAIL'} ({[round(float(m1[b, i100[b]] / m0[b, i100[b]]), 2) for b in range(4)]})"
print(line); open(os.path.join(HERE, "x76_lens_profile.out"), "a").write(line + "\n")
R = json.load(open(os.path.join(HERE, "x76_lens_profile_results.json"))); R["mutate_m1_up"] = up
json.dump(R, open(os.path.join(HERE, "x76_lens_profile_results.json"), "w"), indent=1, default=float)
