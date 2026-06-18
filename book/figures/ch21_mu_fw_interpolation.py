import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# x = |a|/a0 over many decades
x = np.logspace(-3, 3, 700)
mu_fw = (np.sqrt(x**2 + 1.0) - 1.0)/x          # framework interpolation
mu_deep = x/2.0                                  # deep-MOND limit x<<1
mu_newt = np.ones_like(x)                         # Newtonian limit x>>1

fig, ax = plt.subplots(figsize=(7,4.3))
ax.semilogx(x, mu_fw, color=C_FW, lw=2.6,
            label=r"$\mu_{\rm fw}(x)=\dfrac{\sqrt{x^2+1}-1}{x}$")
ax.semilogx(x, mu_newt, color=C_NEWTON, lw=1.8, ls="--",
            label=r"Newtonian limit $\;\mu_{\rm fw}\to1$")
# show the deep-MOND tangent only where it is below 1 (it is the small-x asymptote)
mask = mu_deep <= 1.0
ax.semilogx(x[mask], mu_deep[mask], color=C_MOND, lw=1.8, ls=":",
            label=r"deep-MOND limit $\;\mu_{\rm fw}\to x/2$")

ax.axvline(1.0, color="#999", lw=1.0, ls="-", alpha=0.6)
ax.text(1.15, 0.18, r"$|a|=a_0$", color="#555", fontsize=9)
ax.fill_betweenx([0,1.05], 1e-3, 1.0, color=C_FW, alpha=0.05)
ax.text(3e-3, 0.92, "deep-MOND / galaxy edge\n(harder to push: $\\mu<1$)", fontsize=9, color=C_FW)
ax.text(40, 0.55, "Solar System\n($\\mu\\approx1$, Newton)", fontsize=9, color=C_NEWTON, ha="center")

ax.set_xlim(1e-3, 1e3); ax.set_ylim(0, 1.08)
ax.set_xlabel(r"$x=|a|/a_0$   (object's acceleration in units of $a_0$)")
ax.set_ylabel(r"$\mu_{\rm fw}(x)$   (fraction of Newtonian inertia, $\mu_{\rm fw}\,m\,a=F$)")
ax.set_title("The framework interpolation: how inertia changes near $a_0$")
ax.legend(frameon=False, fontsize=9, loc="center right")
ax.text(0.99,0.02,"framework-computed",transform=ax.transAxes,ha="right",va="bottom",fontsize=7,color="#999")
fig.tight_layout(); fig.savefig("ch21_mu_fw_interpolation.png", bbox_inches="tight"); print("ok")
