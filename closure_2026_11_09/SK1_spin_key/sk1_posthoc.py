#!/usr/bin/env python3
"""SK1 post-freeze diagnostics (NOT graded; written after the FAIL to verify it as hard as a PASS would be).
python3 -I sk1_posthoc.py -> sk1_posthoc.out / .json
Reuses sk1.py's definitions, data load and sample verbatim (exec of the file up to its KA4 block).
P1: every disclosed JAM model (HDU 2-11) x every disclosed IMF reading (Posacki / Chabrier / Salpeter): the most generous corner.
P2: matched on M* only (no g_N), and unmatched medians.  P3: the most generous corner's bootstrap interval.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json
SK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sk1.py")
g = {"__file__": SK, "__name__": "sk1_posthoc"}
exec(compile(open(SK).read().split("# ---- KA4")[0], SK, "exec"), g)
np, A0, build, grade_core, Dstat, boot, mkcell, rho, P, OUT = (g[k] for k in ("np", "A0", "build", "grade_core", "Dstat", "boot", "mkcell", "rho", "P", "OUT"))
n, msr, slow0, lam = g["n"], g["msr"], g["slow0"], g["lam"]
del OUT[:]; R = dict(note="post-freeze diagnostics, not graded; kappa = 1/2 FITTED; not theory closed", foot={})
P("SK1 post-freeze diagnostics (not graded)")
for f, a0 in A0.items():
    grid = {}
    for k in range(10):
        for imf in ("posacki", "chabrier", "salpeter"):
            gd, gN, lmi = build(np.full(n, k), msr, imf); grid[f"HDU{k + 2}_{imf}"] = grade_core(gd, gN, lmi, slow0, a0, bootit=False)["D"]
    best = max(grid, key=lambda x: grid[x]); k = int(best.split("_")[0][3:]) - 2; imf = best.split("_")[1]
    gd, gN, lmi = build(np.full(n, k), msr, imf); bc = grade_core(gd, gN, lmi, slow0, a0, bootit=True)
    gd, gN, lmi = build(g["b1"], msr); m = np.isfinite(gd) & np.isfinite(gN) & (gd > 0) & (gN > 0); r = rho(gd[m], gN[m], a0)
    cM = mkcell(lmi[m], 0.2, np.zeros(m.sum()), 1.0); dM = Dstat(r, slow0[m], cM)[0]; un = float(np.median(r[slow0[m]]) - np.median(r[~slow0[m]]))
    R["foot"][f] = dict(grid=grid, most_generous=best, most_generous_D=bc, n_cells_ge_0p20=int(sum(v >= 0.20 for v in grid.values())),
                        n_cells_ge_0p10=int(sum(v >= 0.10 for v in grid.values())), D_matched_Mstar_only=dM, unmatched_median_diff=un)
    P(f"\n[{f}] P1 grid (30 readings): min {min(grid.values()):+.4f}, max {grid[best]:+.4f} at {best}; readings >= +0.20: {R['foot'][f]['n_cells_ge_0p20']}, >= +0.10: {R['foot'][f]['n_cells_ge_0p10']}")
    P(f"[{f}]    " + "; ".join(f"{k_} {v:+.3f}" for k_, v in grid.items()))
    P(f"[{f}] P3 most generous corner {best}: D {bc['D']:+.4f} [{bc['lo']:+.4f}, {bc['hi']:+.4f}] (cells {bc['cells']})")
    P(f"[{f}] P2 matched on M* only: D {dM:+.4f}; unmatched median slow - fast {un:+.4f}")
open(os.path.join(os.path.dirname(SK), "sk1_posthoc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(os.path.dirname(SK), "sk1_posthoc.json"), "w"), indent=1)
