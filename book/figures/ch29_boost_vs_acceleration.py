import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

a0 = 9.36e-11  # m/s^2, framework scale a0 = c^2 sqrt(Lambda/32pi)

# Gravity boost = effective gravitating mass / baryonic mass = g_obs / g_bar.
# Framework dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0) -> boost = sqrt(1 + a0/g_bar).
# Deep-MOND limiting boost: sqrt(a0/g_bar).
x = np.logspace(-2.3, 1.3, 400)          # g_bar / a0
g_bar = x * a0
boost_fw   = np.sqrt(1.0 + a0/g_bar)     # framework's own interpolation
boost_deep = np.sqrt(a0/g_bar)           # deep-MOND limit

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(x, boost_fw,   color=C_FW,   lw=2.4, label=r"framework boost $\sqrt{1+a_0/g_{\rm bar}}$")
ax.plot(x, boost_deep, color=C_MOND, lw=1.8, ls=":", label=r"deep-MOND limit $\sqrt{a_0/g_{\rm bar}}$")
ax.axhline(1.0, color=C_NEWTON, lw=1.6, ls="--", label="Newtonian (no boost)")

# mark the cluster-core regime from the chapter's worked example: g_N ~ 0.12 a0, boost ~ 3
g_core = 1.2e-11/a0
ax.scatter([g_core],[np.sqrt(1+a0/(g_core*a0))], color=C_DATA, zorder=5, s=55)
ax.annotate("cluster core\n"+r"$g_{\rm bar}\!\approx\!0.12\,a_0$, boost $\approx$3",
            xy=(g_core, np.sqrt(1+a0/(g_core*a0))), xytext=(0.045, 6.0),
            fontsize=9, color=C_DATA,
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.2))
ax.axvspan(1.0, x.max(), color=C_NEWTON, alpha=0.07)
ax.text(4.0, 2.4, "high-$g$ inner core:\nboost fades to 1,\nhelp is least",
        fontsize=8.5, color=C_NEWTON, ha="center", va="center")
ax.text(0.013, 1.18, "low-$g$ outskirts:\nfull MOND glory", fontsize=8.5,
        color=C_MOND, ha="left")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(x.min(), x.max()); ax.set_ylim(0.9, 18)
ax.set_xlabel(r"baryonic acceleration  $g_{\rm bar}/a_0$")
ax.set_ylabel(r"gravity boost  $g_{\rm obs}/g_{\rm bar}$")
ax.set_title("Why the boost is weakest where clusters need it most")
ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.text(0.5,0.02,"$a_0$=9.36e-11 m/s$^2$ (framework dS-Unruh $\\nu$)",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=7, color="#999")
fig.tight_layout(); fig.savefig("ch29_boost_vs_acceleration.png", bbox_inches="tight"); print("ok")
