import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# The chapter's bookkeeping of the cluster central mass-discrepancy ratio eta(R500)
# and how it shrinks as the analysis is corrected. Bars and bands are the chapter's
# stated ranges (NOT a new measurement): Newtonian ~5-10; constant-a0 MOND ~2-3;
# +XRISM trims non-thermal mass ~1.3-2.0; +density-dependent a0 ~1.0-1.3.
labels = ["Newtonian\n(baryons only)", "constant-$a_0$\nMOND boost",
          "+ XRISM trims\nnon-thermal mass", "+ density-dependent\n$a_0$ (framework)"]
eta_lo  = np.array([5.0, 2.0, 1.3, 1.0])
eta_hi  = np.array([10.0,3.0, 2.0, 1.3])
eta_mid = 0.5*(eta_lo+eta_hi)
cols    = [C_NEWTON, C_MOND, "#0e7490", C_FW]

fig, ax = plt.subplots(figsize=(7,4.3))
xpos = np.arange(len(labels))
yerr = np.vstack([eta_mid-eta_lo, eta_hi-eta_mid])
ax.bar(xpos, eta_mid, width=0.6, color=cols, alpha=0.85,
       yerr=yerr, capsize=6, ecolor="#333", error_kw=dict(lw=1.4))

ax.axhline(1.0, color="k", lw=1.4, ls="--")
ax.text(len(labels)-0.5, 1.08, r"$\eta=1$: fully accounted for",
        ha="right", va="bottom", fontsize=9)

for i,(m,lo,hi) in enumerate(zip(eta_mid,eta_lo,eta_hi)):
    ax.text(i, hi+0.25, f"{lo:.0f}-{hi:.0f}" if i==0 else f"{lo:.1f}-{hi:.1f}",
            ha="center", va="bottom", fontsize=8.5, color=cols[i])

ax.set_xticks(xpos); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylim(0, 11)
ax.set_ylabel(r"central mass discrepancy  $\eta(R_{500})=M_{\rm HSE}/M_{\rm theory}$")
ax.set_title("The cluster residual shrinks as the analysis improves - but not to zero")
ax.text(0.99,0.97,"bands are the chapter's stated ranges",
        transform=ax.transAxes, ha="right", va="top", fontsize=7, color="#999")
fig.tight_layout(); fig.savefig("ch29_eta_residual_corrections.png", bbox_inches="tight"); print("ok")
