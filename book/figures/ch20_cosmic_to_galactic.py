import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# --- the worked example, computed step by step from the cosmos alone ---
c    = 2.998e8
G    = 6.674e-11
H0   = 67.4*1e3/3.086e22
OmL  = 0.685
H_L  = H0*np.sqrt(OmL)
Lam  = 3.0*H_L**2/c**2                 # ~1.09e-52  m^-2
step1 = Lam                            # the cosmological constant (a curvature)
step2 = Lam/(32*np.pi)                 # divide by 32 pi
step3 = np.sqrt(step2)                 # sqrt -> inverse length  (m^-1)
a0    = c**2*step3                     # x c^2 -> acceleration  (m/s^2)

# stages of the cascade: label, value, unit, what-it-is, color
stages = [
    (r"$\Lambda$",                 step1, r"$\mathrm{m^{-2}}$", "cosmological constant\n(a curvature)",            "#0e7490"),
    (r"$\dfrac{\Lambda}{32\pi}$",  step2, r"$\mathrm{m^{-2}}$", "divide by $32\\pi\\approx100.5$",                  "#2563eb"),
    (r"$\sqrt{\dfrac{\Lambda}{32\pi}}$", step3, r"$\mathrm{m^{-1}}$", "square root\n(an inverse length)",          "#7c3aed"),
    (r"$c^2\sqrt{\dfrac{\Lambda}{32\pi}}$", a0,  r"$\mathrm{m/s^2}$", "$\\times\\,c^2 \\Rightarrow a_0$",          C_FW),
]
vals   = np.array([s[1] for s in stages])
expo   = np.floor(np.log10(vals)).astype(int)
mant   = vals/10.0**expo

fig, ax = plt.subplots(figsize=(7.8,4.7))
x = np.arange(len(stages))
# plot the (signed) exponent as the bar height so the cascade reads as a magnitude ladder
ax.bar(x, expo, color=[s[4] for s in stages], alpha=0.85, width=0.62, zorder=3)
for xi, s, e, m in zip(x, stages, expo, mant):
    # value label sits just OUTSIDE the bar tip (always below 0 here)
    ax.text(xi, e-1.4, f"{m:.2f}$\\times10^{{{e}}}$ {s[2]}",
            ha="center", va="top", fontsize=8.6, fontweight="bold", color="#1e293b")
    # short descriptor on a common baseline well below all value labels
    ax.text(xi, -73.0, s[3], ha="center", va="top", fontsize=8.0, color=s[4])

# arrows along the cascade
for xi in range(len(stages)-1):
    ax.annotate("", xy=(xi+0.78, expo[xi+1]), xytext=(xi+0.22, expo[xi]),
                arrowprops=dict(arrowstyle="-|>", color="#94a3b8", lw=1.6))

ax.axhline(0, color="#cbd5e1", lw=1.0, zorder=1)
ax.set_xticks(x); ax.set_xticklabels([s[0] for s in stages], fontsize=12)
ax.set_ylim(-84, 12)
ax.set_yticks([-50,-40,-30,-20,-10,0,10])
ax.set_ylabel(r"order of magnitude  ($\log_{10}$ of value)")
ax.set_title("From the cosmos to the galaxy: building $a_0$ out of $\\Lambda$, $c$, and geometry")
ax.text(0.99,0.04, "final: $a_0\\approx9.36\\times10^{-11}$ m/s$^2$\n(no galaxy data used)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color="#5b21b6",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f3e8ff", ec=C_FW, alpha=0.9))
fig.tight_layout(); fig.savefig("ch20_cosmic_to_galactic.png", bbox_inches="tight"); print("ok")
