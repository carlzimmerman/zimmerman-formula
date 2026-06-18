import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# The chapter's own 'bare' combination and the linear a0(kappa) relation (Worked Example, Steps 1-4).
bare = 1.87e-10          # c^2 sqrt(Lambda/6pi), m/s^2 (chapter value)
kappa = np.linspace(0.0, 1.0, 400)
a0 = kappa * bare        # a0 is LINEAR in kappa: double kappa, double a0

# Galactic window the data permit (chapter: 7e-11 to 13e-11 m/s^2)
win_lo, win_hi = 7e-11, 13e-11
ax.axhspan(win_lo, win_hi, color=C_DATA, alpha=0.12, lw=0,
          label="galactic window data permit (7-13 x10$^{-11}$)")

# the framework line
ax.plot(kappa, a0*1e11, color=C_FW, lw=2.4, label=r"$a_0(\kappa)=\kappa\,c^2\sqrt{\Lambda/6\pi}$ (linear)")

# kappa band that lands inside the window: ~0.37 to 0.69
k_lo, k_hi = win_lo/bare, win_hi/bare
ax.axvspan(k_lo, k_hi, color=C_FW, alpha=0.10, lw=0)
ax.axvline(0.5, color=C_FW, ls=":", lw=1.6)

# mark the geometric posit kappa=1/2 -> a0=9.36e-11
ax.plot([0.5],[9.36e-11*1e11], "o", color=C_FW, ms=9, zorder=5)
ax.annotate(r"geometric posit $\kappa=\frac{1}{2}$" + "\n" + r"$a_0\approx 9.36\times10^{-11}$",
            xy=(0.5, 9.36e-11*1e11), xytext=(0.52, 4.2),
            fontsize=9.5, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.2))

# Milgrom classic a0 = 1.2e-10 as a second observational anchor
ax.axhline(1.2e-10*1e11, color=C_NEWTON, ls="--", lw=1.3)
ax.text(0.015, 1.2e-10*1e11+0.18, "Milgrom classic $a_0=1.2\\times10^{-10}$",
        fontsize=8.5, color=C_NEWTON)

ax.text(k_lo+0.005, 17.5, r"$\kappa\in[0.37,0.69]$ stays in window",
        fontsize=9, color=C_FW, rotation=0)

ax.set_xlim(0,1); ax.set_ylim(0,18.7)
ax.set_xlabel(r"geometric posit $\kappa$ (the one un-derived input)")
ax.set_ylabel(r"$a_0$  ($\times10^{-11}\,$m/s$^2$)")
ax.set_title("Geometry proposes $\\kappa=\\frac{1}{2}$; galaxies only permit a band around it")
ax.legend(frameon=False, loc="upper left", fontsize=8.6)
ax.text(0.99,0.02,"a$_0$'s FORM forced; VALUE rests on the posit κ", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7.5, color="#999999")
fig.tight_layout(); fig.savefig("ch27_kappa_band_a0.png", bbox_inches="tight"); print("ok")
