import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

x = np.logspace(-2, 2, 600)
mu = (np.sqrt(1+4*x**2)-1)/(2*x)      # framework interpolation function mu_fw(x)

fig, ax = plt.subplots(figsize=(7,4.3))
ax.semilogx(x, mu, color=C_FW, lw=2.6, label=r"$\mu_{\rm fw}(x)=\dfrac{\sqrt{1+4x^2}-1}{2x}$")
ax.semilogx(x, np.minimum(x,1.0), color=C_MOND, ls="--", lw=1.6,
            label=r"deep-MOND limit  $\mu\to x$")
ax.axhline(1.0, color=C_NEWTON, ls=":", lw=1.6, label=r"Newtonian limit  $\mu\to 1$")
ax.axvline(1.0, color="0.6", lw=1.0, alpha=0.6)
ax.text(1.15, 0.30, r"threshold $x=a/cH_\Lambda=1$", fontsize=9, color="0.35")

ax.annotate("rotation curves go flat\n(galaxy outskirts)", xy=(0.04, 0.04),
            xytext=(0.012, 0.30), fontsize=8.5, color=C_MOND,
            arrowprops=dict(arrowstyle="->", color=C_MOND, lw=1.0))
ax.annotate("standard inertia restored\n(Solar System, lab)", xy=(40, 0.985),
            xytext=(3.0, 0.58), fontsize=8.5, color=C_NEWTON,
            arrowprops=dict(arrowstyle="->", color=C_NEWTON, lw=1.0))

ax.set_xlim(1e-2, 1e2); ax.set_ylim(0, 1.08)
ax.set_xlabel(r"acceleration in units of the floor   $x = a/cH_\Lambda$")
ax.set_ylabel(r"interpolation function  $\mu_{\rm fw}(x)$")
ax.set_title("From the quadrature to a parameter-free interpolation")
ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.text(0.01,0.02,"computed from the framework's equations", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=7, color="0.6")
fig.tight_layout(); fig.savefig("ch15_interpolation_mu_fw.png", bbox_inches="tight"); print("ok")
