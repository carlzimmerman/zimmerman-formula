#!/usr/bin/env python3
"""AUDIT A2 (read-only): CFG429 (zero-constant t_dyn settling, lambda = 1) was scored on T15's ledger rows, committed
~1.5 h BEFORE CFG453 showed that T15's group/cluster deficits are CFG382 definition-A numbers (excess beyond the law per
cosmic cold share) while T15's ledger needs x = (M_tot - M_b)/M_b.  This script re-scores CFG429 with
 (a) the group/cluster x on T15's own definition (medians from CFG453's committed output), and
 (b) the MW-30 row with a consistent M_b (CFG429 takes x = 1.8 -- i.e. M_b = 1e11 -- but S at M_b = 7e10),
 at T15's a0 = 1.2e-10 and at both footings.  CFG429's own frozen rule: EXCLUDED iff every row is negative."""
import math, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
G, MS, KPC = 6.674e-11, 1.989e30, 3.086e19
def S(Mb, Rk, a0): return 1 / (math.exp(math.sqrt(G * Mb * MS / a0) / KPC / Rk) - 1)   # CFG429's kernel supply, verbatim form
def x_mw(V, Mb, R=30.0): return (V * 1e3) ** 2 * R * KPC / G / MS / Mb - 1               # x = (M_tot - M_b)/M_b
X453 = {"groups_b0": 10.845, "groups_b03": 15.922, "clusters_b0": 5.118, "clusters_b03": 7.739}   # CFG453 x_T15 medians (a0-free)
XA = {"groups_b0": 0.79, "groups_b03": 1.76, "clusters_b0": 0.41, "clusters_b03": 0.91}             # what CFG429 used
GEOM = {"groups": (6e12, 554), "clusters": (2.8e13, 985)}
out, L = {}, []
for a0 in (1.2e-10, 9.3603e-11, 1.1312e-10):
    L.append(f"a0 = {a0:.4e}  (lambda = 1 -> f = 1 everywhere, as CFG429)")
    rows = {}
    for k in X453:
        Mb, R = GEOM[k.split("_")[0]]; s = S(Mb, R, a0)
        rows[k] = dict(S=s, Mcold_as_committed=XA[k] - s, Mcold_T15_definition=X453[k] - s)
    for Mb_x, Mb_s, tag in ((1e11, 7e10, "as committed (x at 1e11, S at 7e10)"), (7e10, 7e10, "consistent M_b 7e10"), (1e11, 1e11, "consistent M_b 1e11")):
        for V in (188, 200):
            x = x_mw(V, Mb_x); s = S(Mb_s, 30, a0); rows[f"MW30_V{V} {tag}"] = dict(x=x, S=s, Mcold=x - s)
    for k, r in rows.items():
        if "Mcold" in r: L.append(f"  {k:46s} x {r['x']:.2f}  S {r['S']:.2f}  M_cold/M_b {r['Mcold']:+.2f}")
        else: L.append(f"  {k:46s} S {r['S']:.2f}  committed {r['Mcold_as_committed']:+.2f}  on T15 definition {r['Mcold_T15_definition']:+.2f}")
    gc = [rows[k]["Mcold_T15_definition"] for k in X453]
    L.append(f"  -> groups/clusters on T15's definition: {sum(m >= 0 for m in gc)}/4 rows FEASIBLE at lambda = 1; "
             f"CFG429's all-rows-negative rule gives {'EXCLUDED' if all(m < 0 for m in gc) else 'NOT EXCLUDED'}")
    out[f"{a0:.4e}"] = rows
json.dump(out, open(os.path.join(HERE, "a2_cfg429_rescore.json"), "w"), indent=1)
print("\n".join(L)); open(os.path.join(HERE, "a2_cfg429_rescore.out"), "w").write("\n".join(L) + "\n")
