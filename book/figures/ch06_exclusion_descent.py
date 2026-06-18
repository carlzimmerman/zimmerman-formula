import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Figure 6.1 -- The descending tide of WIMP direct-detection exclusion (SCHEMATIC).
# Stylized exclusion-curve SHAPES (the characteristic valley, with a minimum near a few tens of
# GeV and a steep low-mass turn-up where recoils fall below threshold). Curve values are
# illustrative model shapes, NOT digitized data -- but the chapter's published anchor numbers are
# honored: ~1e-41 cm^2 (1990s), ~1e-48 cm^2 (modern LZ/XENONnT/PandaX-4T near tens of GeV),
# eight orders of magnitude of descent, neutrino floor ~1e-49 cm^2.

fig, ax = plt.subplots(figsize=(7,4.6))
m = np.logspace(np.log10(5), np.log10(1000), 400)   # WIMP mass GeV

def exclusion(mmin, sigma_min, m):
    lm = np.log10(m); lc = np.log10(mmin)
    low_rise  = 1.8*np.maximum(0.0, (lc-lm))**1.7    # steep low-mass kinematic turn-up
    high_rise = 0.55*np.maximum(0.0, (lm-lc))         # gentle high-mass rise (~1/m density)
    return np.log10(sigma_min) + low_rise + high_rise

curves = [
    (1995, 50, 1e-41, "#cbd5e1"),
    (2005, 50, 1e-43, "#94a3b8"),
    (2013, 45, 1e-45, "#64748b"),
    (2020, 40, 1e-47, "#475569"),
    (2024, 35, 1e-48, C_DATA),
]
for yr, mmin, smin, col in curves:
    ls = exclusion(mmin, smin, m)
    lbl = f"{yr}" if yr<2024 else "2024 (LZ / XENONnT / PandaX-4T)"
    ax.plot(m, 10**ls, color=col, lw=2.4 if yr==2024 else 1.6, label=lbl)

nf = exclusion(40, 8e-50, m) - 0.15*np.maximum(0,(np.log10(m)-np.log10(40)))
ax.fill_between(m, 1e-51, 10**nf, color=C_MOND, alpha=0.18, zorder=0)
ax.plot(m, 10**nf, color=C_MOND, lw=1.6, ls=(0,(4,2)), label="neutrino floor / fog (irreducible)")

ax.axhspan(2e-40, 2e-39, color=C_FW, alpha=0.10, zorder=0)
ax.text(6.5, 6e-40, "WIMP-miracle\ntarget region", color=C_FW, fontsize=8.5, va="center")

ax.annotate("eight orders of\nmagnitude in 30 yr",
            xy=(35, 1e-48), xytext=(120, 3e-44),
            fontsize=8.5, color="#334155",
            arrowprops=dict(arrowstyle="->", color="#334155", lw=1.0))

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(5,1000); ax.set_ylim(1e-50, 1e-39)
ax.set_xlabel(r"WIMP mass  $m_\chi$  (GeV)")
ax.set_ylabel(r"WIMP-nucleon cross-section  $\sigma_{\chi N}$  (cm$^2$)")
ax.set_title("The descending tide: WIMP direct-detection exclusion (schematic)")
ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.text(0.99,0.01,"schematic shapes; anchor values from text",transform=ax.transAxes,
        ha="right",va="bottom",fontsize=7,color="#94a3b8")
fig.tight_layout(); fig.savefig("ch06_exclusion_descent.png", bbox_inches="tight"); print("ok")
