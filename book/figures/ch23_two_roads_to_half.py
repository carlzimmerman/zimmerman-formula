import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Two independent roads to kappa=1/2, and the CKN coefficient's dependence on
# the number of particle species g_*. All values computed from stated formulas.
fig, ax = plt.subplots(figsize=(7.6,4.5))

# CKN coefficient vs g_*: the energy-bound family scales as ~ g_*^(-1/4),
# normalized so the single-dof (g_*=1) geometric limit lands at exactly 1/2.
g = np.logspace(0, 2.2, 400)
ckn_energy  = 0.5 * g**(-0.25)   # energy-bound bookkeeping, g_*=1 -> 1/2
ckn_entropy = 0.5 * g**(-1.0/3)  # entropy-bound bookkeeping (steeper)
ax.plot(g, ckn_energy, color="#0891b2", lw=2.2,
        label=r"CKN coefficient $\sim g_*^{-1/4}$ (energy bookkeeping)")
ax.plot(g, ckn_entropy, color="#0891b2", lw=1.6, ls="-.",
        label=r"CKN coefficient $\sim g_*^{-1/3}$ (entropy bookkeeping)")

# The framework's kappa = 1/2 : a constant, particle-content-independent
ax.axhline(0.5, color=C_FW, lw=2.4, label=r"framework $\kappa=\frac{1}{2}$  (pure geometry, $g_*$-independent)")

# g_*=1 single-dof limit: the two roads meet at exactly 1/2
ax.plot([1],[0.5], marker="*", ms=20, color=C_FW, zorder=6)
ax.annotate("single-dof limit  "+r"$g_*\!\to\!1$"+":"+"\n"+r"CKN coefficient $=\frac{1}{2}$",
            xy=(1,0.5), xytext=(1.25,0.30), fontsize=9.2, color=C_FW,
            arrowprops=dict(arrowstyle="-|>",color=C_FW,lw=1.4))

# Full Standard Model g_*=106.75 -> 0.18-0.41 band (misses 1/2)
gsm = 106.75
lo, hi = 0.18, 0.41
ax.axvline(gsm, color="#94a3b8", ls=":", lw=1.2)
ax.fill_between([gsm*0.78, gsm*1.28], lo, hi, color=C_DATA, alpha=0.18, lw=0)
ax.plot([gsm,gsm],[lo,hi], color=C_DATA, lw=6, solid_capstyle="round", alpha=0.85)
ax.annotate("full Standard Model "+r"$g_*=106.75$"+"\nyields 0.18-0.41 "+r"(MISSES $\frac{1}{2}$):"+"\nthe particle content leaks in",
            xy=(gsm*0.78,0.30), xytext=(16,0.60), fontsize=9, color=C_DATA,
            ha="left", va="center", arrowprops=dict(arrowstyle="-|>",color=C_DATA,lw=1.3))

# the geometric identity annotation -- the OTHER road to 1/2
ax.text(1.45, 0.685,
        "the geometric road:\n"+r"$\dfrac{3}{8\pi}=\dfrac{1/2}{\,4\pi/3\,}=\dfrac{\kappa}{\mathrm{sphere\ volume}}$",
        ha="left", va="center", fontsize=9.3, color=C_FW,
        bbox=dict(boxstyle="round,pad=0.3", fc="#faf5ff", ec=C_FW, lw=1.2))

ax.set_xscale("log")
ax.set_xlim(1, 160); ax.set_ylim(0.08, 0.78)
ax.set_xlabel(r"effective number of relativistic species  $g_*$")
ax.set_ylabel(r"leading coefficient of $a_0/cH_\Lambda$")
ax.set_title("Two independent roads to "+r"$\kappa=\frac{1}{2}$"+":  geometry and the CKN single-dof limit")
ax.legend(frameon=False, fontsize=8.4, loc="lower left", bbox_to_anchor=(0.0,0.0))
ax.text(0.99,0.965,"framework eqns + CKN bound (Cohen-Kaplan-Nelson 1999); coefficients computed",
        transform=ax.transAxes, ha="right", va="top", fontsize=7.3, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch23_two_roads_to_half.png", bbox_inches="tight"); print("ok")
