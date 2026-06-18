import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Figure 6.2 -- The WIMP miracle on one curve.
# PUBLISHED-RELATION: the standard relic-abundance scaling Omega_chi h^2 ~ 3e-27 / <sigma v>
# (the chapter's Deeper Dive equation) plotted as a model. The measured DM density
# Omega_chi h^2 = 0.12 (Planck 2018) is the horizontal target; the cross-section that hits it,
# ~3e-26 cm^3/s, is the 'miracle' value, which coincides with the weak-scale alpha_W^2/m_W^2.

fig, ax = plt.subplots(figsize=(7,4.4))

sv = np.logspace(-28, -23, 400)            # <sigma v>  cm^3/s
Omega = 3e-27 / sv                          # chapter relic relation
ax.plot(sv, Omega, color=C_FW, lw=2.6,
        label=r"relic relation  $\Omega_\chi h^2 \approx 3\times10^{-27}/\langle\sigma v\rangle$")

Om_obs = 0.12
ax.axhline(Om_obs, color=C_DATA, lw=1.8, ls=(0,(5,2)),
           label=r"observed DM density $\Omega_\chi h^2 = 0.12$ (Planck 2018)")

sv_star = 3e-27 / Om_obs                    # = 2.5e-26 cm^3/s
ax.axvline(sv_star, color="#334155", lw=1.0, ls=":")
ax.plot([sv_star],[Om_obs], "o", color="#334155", ms=7, zorder=5)
ax.annotate("the 'miracle' value\n"+r"$\langle\sigma v\rangle\approx3\times10^{-26}$ cm$^3$/s"+"\n"+r"$\approx\alpha_W^2/m_W^2$",
            xy=(sv_star, Om_obs), xytext=(4e-26, 0.9),
            fontsize=8.5, color="#334155", ha="left",
            arrowprops=dict(arrowstyle="->", color="#334155", lw=1.0))

ax.axvspan(1e-26, 1e-25, color="#0891b2", alpha=0.12, zorder=0)
ax.text(3e-26, 4e-3, "weak-scale\ncross-sections", color=C_MOND, fontsize=8.5, ha="center")

ax.text(2e-28, 3, "anemic annihilators\nfreeze out early\n-> too much DM", fontsize=8, color="#64748b", va="top")
ax.text(3e-24, 2e-3, "eager annihilators\nkeep destroying\n-> too little DM", fontsize=8, color="#64748b", ha="right")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e-28, 1e-23); ax.set_ylim(1e-3, 30)
ax.set_xlabel(r"thermally-averaged annihilation rate  $\langle\sigma v\rangle$  (cm$^3$/s)")
ax.set_ylabel(r"relic dark-matter density  $\Omega_\chi h^2$")
ax.set_title("The WIMP miracle on one curve")
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
fig.tight_layout(); fig.savefig("ch06_wimp_miracle.png", bbox_inches="tight"); print("ok")
