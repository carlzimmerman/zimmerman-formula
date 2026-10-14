#!/usr/bin/env python3
"""CFG721 POST-HOC (not frozen, no verdict weight): per-galaxy SPARC check of the supply edge. The frozen T-S guard paired the
smallest ladder edge (M_b 1e9) with the largest SPARC last radius (108.3 kpc, a massive galaxy) and so cannot certify SPARC. Here
each of the 175 SPARC galaxies gets its own baryonic mass (0.5 L[3.6] + 1.33 M_HI, Lelli+16 table) and its own last measured radius
(rotmod), and the supply-edge radius is interpolated (log-log) from the ladder at f_cond = 1, z = 0, taking the SMALLEST edge over
both sources, both kernels and both footings. A galaxy is affected iff R_last > r_edge(M_b) or the ladder overflow is non-zero.
Reads ../_external_data/cfg721_work/ladder.json. Writes cfg721_sparc_posthoc.out / .json.
Run from the repository root:  nice -n 10 python3 campaign_fresh_gravity/CFG721_supply_overflow/cfg721_sparc_posthoc.py
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg721_work"))
LAD = [r for r in json.load(open(os.path.join(WORK, "ladder.json"))) if r["fcond"] == 1.0 and r["z"] == 0.0]
lm = np.array(sorted({r["lMb"] for r in LAD}))
edge = np.array([min(r["r_edge_kpc"] for r in LAD if r["lMb"] == m) for m in lm])
resmax = np.array([max(r["res_frac"] for r in LAD if r["lMb"] == m) for m in lm])
T = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    t = l.split()
    if len(t) < 18 or not t[1].isdigit():
        continue
    try:
        T[t[0]] = 1e9 * (0.5 * float(t[7]) + 1.33 * float(t[13]))           # L[3.6] (col 8), M_HI (col 14), 1e9 units
    except ValueError:
        pass
rows = []
for f in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    n = os.path.basename(f).replace("_rotmod.dat", "")
    if n not in T:
        continue
    Rl = float(np.loadtxt(f)[:, 0].max()); Mb = T[n]
    re = float(10 ** np.interp(np.log10(Mb), lm, np.log10(edge)))
    rf = float(np.interp(np.log10(Mb), lm, resmax))
    rows.append(dict(galaxy=n, Mb=Mb, R_last=Rl, r_edge_min=re, ratio=Rl / re, overflow=rf))
aff = [r for r in rows if r["ratio"] >= 1 or r["overflow"] > 0]
worst = max(rows, key=lambda r: r["ratio"])
out = [__doc__.split("Reads")[0].strip(),
       f"  galaxies matched: {len(rows)} of 175; ladder edge (min over cells) at log M_b {lm.tolist()}: " + " ".join(f"{e:.0f}" for e in edge) + " kpc",
       f"  max R_last / r_edge = {worst['ratio']:.3f} ({worst['galaxy']}, log M_b {np.log10(worst['Mb']):.2f}, R_last {worst['R_last']:.1f} kpc, edge {worst['r_edge_min']:.0f} kpc)",
       f"  median R_last / r_edge = {np.median([r['ratio'] for r in rows]):.3f}; max ladder overflow at SPARC masses {max(r['overflow'] for r in rows):.4f}",
       f"  galaxies affected (R_last beyond the edge or overflow > 0): {len(aff)}"
       + (" -> H-OF changes no SPARC point (post-hoc; RAR scatter change exactly 0)" if not aff else " -> SPARC NOT unchanged: " + ", ".join(r["galaxy"] for r in aff[:20]))]
print("\n".join(out))
open(os.path.join(HERE, "cfg721_sparc_posthoc.out"), "w").write("\n".join(out) + "\n")
json.dump(dict(n=len(rows), n_affected=len(aff), worst=worst, rows=rows), open(os.path.join(HERE, "cfg721_sparc_posthoc.json"), "w"), indent=1)
