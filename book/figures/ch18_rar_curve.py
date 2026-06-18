import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

a0 = 1.2e-10  # RAR best-fit scale, m/s^2 (McGaugh, Lelli & Schombert 2016)
gbar = np.logspace(-13, -8, 400)

# McGaugh interpolating function (the published RAR fit form) -- plotted as a MODEL
gobs_rar = gbar / (1.0 - np.exp(-np.sqrt(gbar / a0)))
# Newtonian baseline: gobs = gbar
gobs_newton = gbar
# deep-MOND square-root tail
gobs_deep = np.sqrt(gbar * a0)

fig, ax = plt.subplots(figsize=(7, 4.6))

# illustrative, model-generated points hugging the RAR with stated synthetic scatter
rng = np.random.default_rng(2016)
gb_pts = 10**rng.uniform(-12.0, -8.3, 320)
mean = gb_pts / (1.0 - np.exp(-np.sqrt(gb_pts / a0)))
scatter_dex = 0.11  # the observed ~0.11 dex scatter quoted in the chapter
go_pts = mean * 10**(rng.normal(0, scatter_dex, gb_pts.size))
ax.scatter(gb_pts, go_pts, s=7, color=C_DATA, alpha=0.30, lw=0,
           label="illustrative points (model + 0.11 dex scatter)")

ax.plot(gbar, gobs_newton, color=C_NEWTON, ls="--", lw=2,
        label=r"Newton:  $g_{\rm obs}=g_{\rm bar}$")
ax.plot(gbar, gobs_deep, color=C_MOND, ls=":", lw=2,
        label=r"deep-MOND tail:  $\sqrt{g_{\rm bar}\,a_0}$")
ax.plot(gbar, gobs_rar, color=C_FW, lw=2.6,
        label="RAR fitting function (McGaugh+ 2016)")

# mark the bend at a0
ax.axvline(a0, color="black", lw=1, alpha=0.4)
ax.annotate(r"the bend sits at $a_0\approx1.2\times10^{-10}\,$m/s$^2$",
            xy=(a0, a0), xytext=(2.5e-12, 4e-9),
            fontsize=9.5, color="black",
            arrowprops=dict(arrowstyle="->", color="black", alpha=0.6))

ax.text(3.2e-9, 1.3e-9, "high-accel:\nNewton holds", fontsize=8.5,
        color=C_NEWTON, ha="center")
ax.text(8e-13, 1.5e-10, "low-accel:\nmissing-mass\nlift-off", fontsize=8.5,
        color=C_MOND, ha="center")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(5e-13, 1e-8); ax.set_ylim(1e-12, 1e-8)
ax.set_xlabel(r"baryonic acceleration  $g_{\rm bar}=GM/R^2$   (m/s$^2$)")
ax.set_ylabel(r"observed acceleration  $g_{\rm obs}=V^2/R$   (m/s$^2$)")
ax.set_title("The Radial-Acceleration Relation: one curve, every galaxy")
ax.legend(frameon=False, fontsize=8.6, loc="lower right")
ax.text(0.005, 0.005, "points illustrative / model-generated, not real SPARC data",
        transform=ax.transAxes, fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("ch18_rar_curve.png", bbox_inches="tight"); print("ok")
