import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs
fig, ax = plt.subplots(figsize=(7,4.3))

# The radial-acceleration relation: g_obs vs g_bar.
# a0: the literature RAR scale quoted in the chapter, and the framework value.
a0_rar = 1.2e-10                                   # chapter's quoted RAR scale
c_light = 2.998e8; Lam = 1.1e-52
a0_fw = c_light**2*np.sqrt(Lam/(32*np.pi))         # framework: a0 = c^2 sqrt(Lambda/32pi) ~ 9.4e-11

gbar = np.logspace(-13, -8, 400)

# Newtonian one-to-one line
gN = gbar
# Framework's OWN de Sitter-Unruh interpolation: g_obs = sqrt(g_bar^2 + g_bar*a0)
gfw = np.sqrt(gbar**2 + gbar*a0_fw)
# Low-acceleration MOND limit g_obs = sqrt(g_bar a0) (deep-MOND asymptote)
gdeep = np.sqrt(gbar*a0_rar)

ax.plot(gbar, gN, color=C_NEWTON, lw=2.0, ls="--", label=r"Newton: $g_{\rm obs}=g_{\rm bar}$")
ax.plot(gbar, gdeep, color=C_MOND, lw=1.8, ls=":",
        label=r"deep-MOND limit: $\sqrt{g_{\rm bar}\,a_0}$")
ax.plot(gbar, gfw, color=C_FW, lw=2.6,
        label=r"framework dS-Unruh: $\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$")

# mark a0
for a0,lab,col,dy in [(a0_fw, r"$a_0=9.4\times10^{-10}$ wait",C_FW,0)]:
    pass
ax.axvline(a0_fw, color=C_FW, lw=0.9, ls="-", alpha=0.5)
ax.text(a0_fw*1.15, 3e-13, r"$a_0\!\approx\!9.4\times10^{-11}$"+"\n(framework)",
        fontsize=8.5, color=C_FW, ha="left", va="bottom")

ax.annotate("above $a_0$: ordinary gravity,\nno dark matter needed",
            xy=(3e-9, 3e-9), xytext=(8e-12, 4.5e-9),
            fontsize=8.5, color="#5f5e5a", ha="left",
            arrowprops=dict(arrowstyle="->", color="#9ca3af", lw=0.9))
ax.annotate("below $a_0$: missing-mass\nregime appears",
            xy=(3e-13, np.sqrt(3e-13*a0_fw)), xytext=(2e-13, 8e-11),
            fontsize=8.5, color=C_DATA, ha="left",
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=0.9))

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e-13, 1e-8); ax.set_ylim(1e-13, 1e-8)
ax.set_xlabel(r"$g_{\rm bar}$  =  acceleration from visible matter  (m s$^{-2}$)")
ax.set_ylabel(r"$g_{\rm obs}$  =  measured acceleration  (m s$^{-2}$)")
ax.set_title("The quiet clue: the radial-acceleration relation")
ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.text(0.01, 0.97, "models / relations, not data", transform=ax.transAxes,
        ha="left", va="top", fontsize=8, color="#b4b2a9")
fig.tight_layout(); fig.savefig("ch04_radial_acceleration_relation.png", bbox_inches="tight"); print("ok")
