#!/usr/bin/env python3
"""CFG224b figure: per-galaxy optimised conversion factors (Dunne+22) against redshift with bin means, and ACE's dust-to-CO ratio against metallicity with Stripe82's local relation.
Reads cfg224b_conversion_drift_results.json.  Optimised conversions make the tracer masses agree by construction; conversions as optimised / adopted; no law verdict."""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(LANE, "cfg224b_conversion_drift_results.json")))
P = J["points"]; R = J["primary"]
COL = {"ad": "#1f5fa8", "daX": "#e07b00", "xa": "#2a9d55", "xd": "#7b2cbf"}
BIN = [("B1 z<0.6", 0.25), ("B2 0.6<=z<1.6", 1.0), ("B3 1.6<=z<3.0", 2.2), ("B4 z>=3.0", 4.0)]
fig, axs = plt.subplots(1, 3, figsize=(17, 6.2), gridspec_kw=dict(width_ratios=[1, 1, 1], wspace=0.27))
for ax, fac, ttl, tabs in ((axs[0], "alpha_CO", r"CO: $\log_{10}\alpha_{CO}$ (optimised per galaxy)", ("ad", "daX", "xa")), (axs[1], "X_CI", r"[CI]: $\log_{10}X_{CI}$ (optimised per galaxy)", ("xa", "daX", "xd"))):
    for t in tabs:
        pts = P.get(f"{t}|{fac}", [])
        ax.plot([p["z"] for p in pts], [p["y"] for p in pts], ".", ms=3.5, color=COL[t], alpha=0.25)
    for t in tabs:
        for b, xz in BIN:
            st = R.get(f"{t}|{fac}|{b}")
            if st and st.get("N", 0) >= 3:
                dx = {"ad": 0.0, "daX": 0.06, "xa": -0.06, "xd": 0.1}[t]
                ax.errorbar([xz * (1 + dx)], [st["mean"]], yerr=[[st["se"]], [st["se"]]], fmt="o", ms=7, color=COL[t], mec="k", mew=0.8, capsize=3, zorder=5, label=f"{t} (bin means, SE)" if b.startswith("B1") else None)
    ax.set_xscale("log"); ax.set_xticks([0.05, 0.2, 0.5, 1, 2, 3, 5]); ax.set_xticklabels(["0.05", "0.2", "0.5", "1", "2", "3", "5"]); ax.set_xlim(0.03, 7.5)
    ax.set_xlabel("redshift z", fontsize=11.5); ax.set_title(ttl, fontsize=11.5, loc="left"); ax.grid(True, color="#cccccc", lw=0.5, alpha=0.7); ax.legend(fontsize=8.6, loc="best")
axs[0].set_ylabel("log10 of the optimised factor", fontsize=11)
ax = axs[2]; A = J["ace"]
Zs = np.linspace(8.2, 8.9, 50)
inr = (Zs >= A["s82"]["zmin"]) & (Zs <= A["s82"]["zmax"])
ax.plot(Zs[inr], A["s82"]["a"] + A["s82"]["b"] * Zs[inr], color="#555555", lw=2.4, label=f"Stripe82 OLS (solid: its range {A['s82']['zmin']:.2f} to {A['s82']['zmax']:.2f}; dotted: extrapolation)")
ax.plot(Zs[~inr], A["s82"]["a"] + A["s82"]["b"] * Zs[~inr], color="#555555", lw=2, ls=":")
ax.fill_between(Zs, A["s82"]["a"] + A["s82"]["b"] * Zs - A["s82"]["res_sd"], A["s82"]["a"] + A["s82"]["b"] * Zs + A["s82"]["res_sd"], color="#999999", alpha=0.18)
ax.plot(A["Zace"], A["Race"], "s", ms=8, color="#c0392b", mec="k", label=f"ACE z ~ 2.2 (N = {A['N']})")
ax.set_xlabel("12 + log(O/H)", fontsize=11.5); ax.set_ylabel(r"$R=\log_{10}(M_{dust}/M_{mol,CO})$", fontsize=11.5)
ax.set_title(f"ACE minus Stripe82 at fixed Z: {A['delta']:+.2f} (OLS), {A['posthoc']['delta_noslope']:+.2f} (no slope), {A['posthoc']['delta_slope1']:+.2f} (slope 1)", fontsize=10.2, loc="left")
ax.grid(True, color="#cccccc", lw=0.5, alpha=0.7); ax.legend(fontsize=8.6, loc="lower right")
fig.suptitle("Conversion factors against redshift (Dunne+22, per galaxy) and ACE's dust-to-CO ratio (optimised conversions make the tracer masses agree by construction; no law verdict)", fontsize=12, x=0.055, ha="left", y=0.995)
fig.text(0.055, 0.01, "At fixed L_IR the optimised factors show no z slope beyond about +-0.05 to 0.10 per unit log10(1+z) (the apparent drift in the bin means is mostly the L_IR dependence);\nACE's dust-to-CO ratio sits 0.2 to 0.7 dex below Stripe82's at the same metallicity, depending on the metallicity slope assumed (Stripe82's own slope is -0.49 +- 0.33 over 0.21 dex).", fontsize=8.8, va="bottom", ha="left", linespacing=1.4)
fig.subplots_adjust(left=0.055, right=0.985, top=0.9, bottom=0.17)
out = os.path.join(LANE, "cfg224b_conversion_drift.png")
fig.savefig(out, dpi=150); print("wrote", out)
