import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4,4.3), gridspec_kw={"width_ratios":[1.05,1]})

# -------- left: the two readings of eta and the unexplained fraction 1 - 1/eta --------
etas = np.linspace(1.0, 2.5, 300)
frac = 1.0 - 1.0/etas          # fraction of lensing signal the theory cannot supply
ax1.plot(etas, 100*frac, color=C_FW, lw=2.4)

# galaxy scale: eta = 1 (PASS, no residual)
ax1.plot([1.0],[0.0], "o", color=C_MOND, ms=8, zorder=5)
ax1.annotate("galaxies: $\\eta=1$\n(lensing RAR PASSES)", xy=(1.0,0), xytext=(1.18,12),
             color=C_MOND, fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color=C_MOND, lw=1.0))

# integrated cluster band eta ~ 1.0-1.3 (milder, XRISM-corrected)
ax1.axvspan(1.0, 1.3, color=C_NEWTON, alpha=0.12)
ax1.text(1.15, 46, "integrated to $R_{500}$\n$\\eta\\sim1.0$-$1.3$\n(milder)",
         ha="center", fontsize=8, color=C_NEWTON)

# central cluster residual eta = 2.3
eta_c = 2.3
frac_c = 1.0 - 1.0/eta_c
ax1.plot([eta_c],[100*frac_c], "o", color=C_DATA, ms=8, zorder=5)
ax1.annotate("cluster center:\n$\\eta\\approx2.3$ -> 57%\nunaccounted",
             xy=(eta_c,100*frac_c), xytext=(1.55,30),
             color=C_DATA, fontsize=8.5,
             arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.0))
ax1.axhline(50, color="#999999", lw=0.8, ls=":")
ax1.text(1.02, 51.5, "half the signal", fontsize=7.5, color="#777777")

ax1.set_xlabel(r"lensing residual  $\eta = M_{\rm lens}/M_{\rm pred}$")
ax1.set_ylabel(r"unexplained fraction  $1-1/\eta$  (%)")
ax1.set_xlim(1.0, 2.5); ax1.set_ylim(0, 65)
ax1.set_title("How big is the hole?", fontsize=11)

# -------- right: mass bookkeeping bar for a central cluster --------
ax2.set_title("Cluster-center mass budget", fontsize=11)
M_pred = 1.0
M_lens = eta_c
ax2.bar([0], [M_pred], width=0.55, color=C_FW, label=r"$M_{\rm pred}$ (baryons + MOND boost)")
ax2.bar([1], [M_pred], width=0.55, color=C_FW)
ax2.bar([1], [M_lens-M_pred], width=0.55, bottom=[M_pred], color=C_DATA, alpha=0.85,
        label=r"unaccounted ($M_{\rm lens}-M_{\rm pred}$)")
ax2.errorbar([1],[M_lens], yerr=[[0.15],[0.15]], fmt="none", ecolor="#333333", capsize=4, lw=1.2)
ax2.text(1, M_lens+0.18, r"$M_{\rm lens}\approx2.3\,M_{\rm pred}$", ha="center", fontsize=8.5, color="#333333")
ax2.set_xticks([0,1]); ax2.set_xticklabels(["framework\npredicts","light\nactually sees"], fontsize=9)
ax2.set_ylabel(r"mass (units of $M_{\rm pred}$)")
ax2.set_ylim(0, 2.9)
ax2.legend(frameon=False, fontsize=8, loc="upper left")
ax2.grid(axis="x")

fig.suptitle("The cluster lensing residual: a real hole, bounded and shared", fontsize=12, y=1.02)
fig.text(0.99, 0.005, "framework-computed; eta~2.3 central, illustrative", ha="right",
         va="bottom", fontsize=7, color="#999999")
fig.tight_layout(); fig.savefig("ch28_cluster_residual_eta.png", bbox_inches="tight"); print("ok")
