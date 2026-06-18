import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# a0 computed from the cosmos (Hat 1), not assumed
c   = 2.998e8
H0  = 67.4*1e3/3.086e22
OmL = 0.685
H_L = H0*np.sqrt(OmL)
Lam = 3.0*H_L**2/c**2
a0  = c**2*np.sqrt(Lam/(32*np.pi))     # 9.36e-11 m/s^2

# baryonic (Newtonian) gravity spanning weak to strong field
g_bar = np.logspace(-13, -8, 600)      # m/s^2
g_newton = g_bar                                       # pure Newton
g_obs    = np.sqrt(g_bar**2 + g_bar*a0)               # framework's dS-Unruh interpolation
g_deep   = np.sqrt(g_bar*a0)                          # deep-MOND asymptote

fig, ax = plt.subplots(figsize=(7.2,4.6))
ax.loglog(g_bar, g_newton, color=C_NEWTON, lw=2.0, ls="--", label="pure Newton  $g_{\\rm obs}=g_{\\rm bar}$")
ax.loglog(g_bar, g_deep,   color=C_MOND,  lw=1.6, ls=":",  label="deep regime  $g_{\\rm obs}=\\sqrt{g_{\\rm bar}\\,a_0}$")
ax.loglog(g_bar, g_obs,    color=C_FW,    lw=2.6,
          label=r"framework  $g_{\rm obs}=\sqrt{g_{\rm bar}^2+g_{\rm bar}a_0}$")

# mark the transition at g_bar = a0
ax.axvline(a0, color=C_DATA, lw=1.3, ls="-", alpha=0.8)
ax.axhline(a0, color=C_DATA, lw=0.8, ls=":", alpha=0.5)
ax.plot([a0],[np.sqrt(a0**2+a0*a0)], "o", color=C_DATA, ms=6, zorder=5)
ax.text(a0*1.25, 1.5e-13, r"$a_0=9.36\times10^{-11}$"+"\nm/s$^2$", color=C_DATA,
        fontsize=8.6, ha="left", va="bottom")

# regime annotations
ax.text(2e-9, 5e-9, "Newtonian\n(Solar-System safe)", color=C_NEWTON,
        fontsize=8.5, ha="center", va="center")
ax.text(3e-13, 3e-11, "low-acceleration\nboost (galaxy outskirts)", color=C_FW,
        fontsize=8.5, ha="center", va="center")

ax.set_xlim(1e-13, 1e-8); ax.set_ylim(1e-13, 1e-8)
ax.set_xlabel(r"baryonic gravity  $g_{\rm bar}$  (m/s$^2$)")
ax.set_ylabel(r"felt gravity  $g_{\rm obs}$  (m/s$^2$)")
ax.set_title("The framework's own interpolation: $a_0$ is the threshold between two regimes")
ax.legend(frameon=False, loc="upper left", fontsize=8.8)
fig.tight_layout(); fig.savefig("ch20_dsunruh_interpolation.png", bbox_inches="tight"); print("ok")
