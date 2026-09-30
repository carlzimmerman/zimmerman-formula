#!/usr/bin/env python3
"""CFG222 figure: where the data sit against each law's expectation, for the flat law, the LambdaCDM effective-a0 PROXY and the rival H(z), on every data row.
x: z = (observed - expected) / bootstrap sd against the law's OWN expectation (filled) and against the FLAT-true expectation (open).
*** LambdaCDM has no a0: the proxy is an effective-a0 scale from halo structure (Z1's lcdm_native), not LambdaCDM; a fair LambdaCDM test uses simulated galaxies. ***
Reads cfg222_lcdm_proxy_results.json.   Run: python3 campaign_fresh_gravity/CFG222_lcdm_proxy/cfg222_plot.py -> cfg222_z_table.png
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg222_lcdm_proxy_results.json")))["main"]
rows = list(R)
LAW = (("FLAT", "#1f6fd1", "flat law"), ("LCDM-PROXY", "#6a4c93", "LCDM effective-a0 PROXY (not LCDM)"), ("H(z)", "#d1541f", "rival a0 ~ E(z)"))
CAV = {"RC100": "fit (prior-anchored)", "fit route": "fit (1-dex prior)", "independent": "SED + dust gas"}
fig, ax = plt.subplots(figsize=(15.5, 6.4))
for k, law in enumerate(LAW):
    off = (k - 1) * 0.22
    y = np.arange(len(rows))[::-1] + off
    zo = [R[r][law[0]]["z_own"] for r in rows]; zf = [R[r][law[0]]["z_flat"] for r in rows]
    ax.scatter(zo, y, s=80, color=law[1], label=f"{law[2]}: z vs its own expectation", zorder=3)
    ax.scatter(zf, y, s=80, facecolors="white", edgecolors=law[1], linewidths=2, label=f"{law[2]}: z vs the flat-true expectation", zorder=3)
    for a, b, yy in zip(zo, zf, y):
        ax.plot([a, b], [yy, yy], color=law[1], lw=1, alpha=0.5, zorder=2)
ax.axvspan(-2, 2, color="0.93", zorder=0); ax.axvspan(-3, 3, color="0.97", zorder=0)
ax.axvline(0, color="0.2", lw=1.2)
ax.set_yticks(np.arange(len(rows))[::-1]); ax.set_yticklabels([f"{r}\n[{('fit route' if 'fit' in r or 'RC100' in r else 'independent: SED + dust gas')}]" for r in rows], fontsize=8.6)
ax.set_xlabel("z = (observed - expected) / bootstrap sd        (shading: |z| < 2 and < 3)")
ax.set_title("CFG222: flat vs a LCDM effective-a0 PROXY vs H(z), on the data in hand (every row is conditional on its gas route)", fontsize=11)
h, l = ax.get_legend_handles_labels()
ax.legend(h, l, fontsize=8.3, loc="upper left", bbox_to_anchor=(1.01, 1.0), ncol=1, frameon=True)
ax.grid(alpha=0.25, axis="x")
fig.text(0.01, 0.008, "LambdaCDM has no a0: the proxy is Z1's lcdm_native (Dutton-Maccio 2014 halo-structure rise, x2.16 at z = 2.5; EXTRAPOLATED above z = 5 at CRISTAL's redshifts). A fair LCDM test uses simulated galaxies.\n"
         "RC100 rows: Theil-Sen slope of delta on z; CRISTAL rows: median delta. Author decompositions, not a direct a0 measurement; kappa = 1/2 fitted; no sentence says the data favour a framework.", fontsize=8, color="0.3")
plt.tight_layout(rect=(0, 0.06, 1, 1))
out = os.path.join(HERE, "cfg222_z_table.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
