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

# CKN coefficient vs g_*: the energy-bound family scales as ~ g_*^(-1/4).
# CORRECTED 2026-08-02: this was hard-coded to 0.5 with the comment "normalized so the single-dof
# (g_*=1) geometric limit lands at exactly 1/2". That normalization was FALSE and load-bearing --
# the g_*=1 CKN energy coefficient is (3/8pi)^(1/4) = 0.5877875, which this chapter prints itself,
# so substituting 1/2 was a 17.56% change that manufactured the figure's punchline. As coded the SM
# point sat at 0.1555, BELOW this figure's own annotated 0.18-0.41 band; corrected it is 0.1829,
# on the band edge. See real_research/reviews/mi_efe_escape_and_ch23_withdrawn_2026.py (E3a).
CKN1 = (3.0 / (8.0 * np.pi))**0.25   # = 0.5877875, the g_*=1 geometric limit. NOT 1/2.
g = np.logspace(0, 2.2, 400)
ckn_energy  = CKN1 * g**(-0.25)   # energy-bound bookkeeping, g_*=1 -> (3/8pi)^(1/4)
ckn_entropy = CKN1 * g**(-1.0/3)  # entropy-bound bookkeeping (steeper)
ax.plot(g, ckn_energy, color="#0891b2", lw=2.2,
        label=r"CKN coefficient $\sim g_*^{-1/4}$ (energy bookkeeping)")
ax.plot(g, ckn_entropy, color="#0891b2", lw=1.6, ls="-.",
        label=r"CKN coefficient $\sim g_*^{-1/3}$ (entropy bookkeeping)")

# The framework's kappa = 1/2 : a constant, particle-content-independent
ax.axhline(0.5, color=C_FW, lw=2.4, label=r"framework $\kappa=\frac{1}{2}$  (pure geometry, $g_*$-independent)")

# g_*=1 single-dof limit. CORRECTED 2026-08-02: the CKN coefficient there is (3/8pi)^(1/4) = 0.5878,
# NOT 1/2, and the two "roads" are NOT independent -- sqrt(2/Z) = sqrt(2*kappa)*(3/8pi)^(1/4)
# identically, so the framework's slot equals this geometric limit IFF kappa = 1/2. The agreement is
# the INPUT, not a coincidence: d ln(slot)/d ln(kappa) = 1/2, so kappa does not cancel.
ax.plot([1],[CKN1], marker="*", ms=20, color=C_FW, zorder=6)
ax.annotate("single-dof limit  "+r"$g_*\!\to\!1$"+":"+"\n"+r"CKN coefficient $=(3/8\pi)^{1/4}=0.588$"
            +"\n"+r"(NOT $\frac{1}{2}$; matching it *requires* $\kappa=\frac{1}{2}$)",
            xy=(1,CKN1), xytext=(1.25,0.28), fontsize=8.6, color=C_FW,
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
