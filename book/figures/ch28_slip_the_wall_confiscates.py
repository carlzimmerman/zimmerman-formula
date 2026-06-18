import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

fig, ax = plt.subplots(figsize=(7,4.3))

# x-axis: baryonic acceleration in units of a0 (a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2)
# plotted from low (deep-MOND, galaxy/cluster outskirts) to high (Newtonian, Solar System)
x = np.logspace(-2, 2, 400)           # g_N / a0

# The slip the framework's modified-INERTIA matter action NAIVELY wants:
# matter feels Phi (grad Phi = g_N); moves by modified inertia a = sqrt(g_N^2 + g_N a0);
# light feels Phi+Psi -> slip gamma = Psi/Phi = 2 sqrt(1 + a0/g_N) - 1.
gamma_fw = 2.0*np.sqrt(1.0 + 1.0/x) - 1.0   # framework's would-be slip

# What general covariance + c_T=c + ghost-freedom FORCE the relativistic (AeST-class) host to:
# Phi = Psi everywhere -> gamma = 1, NO slip.
gamma_wall = np.ones_like(x)

ax.plot(x, gamma_fw, color=C_FW, lw=2.4,
        label=r"slip the matter action wants:  $\gamma=2\sqrt{1+a_0/g_N}-1$")
ax.plot(x, gamma_wall, color=C_NEWTON, ls="--", lw=2.2,
        label=r"the no-slip wall (AeST-class host):  $\gamma=1$, $\Phi=\Psi$")

# mark the regimes
ax.axvline(1.0, color=C_MOND, lw=1.0, alpha=0.5)
ax.text(1.05, 14, r"$g_N=a_0$", color=C_MOND, fontsize=9, rotation=90, va="top")

# annotate the tabulated values from the framework's slip note
for xv, gv in [(0.01,19.1),(0.1,5.63),(1.0,1.83),(100,1.01)]:
    ax.plot([xv],[gv], "o", color=C_FW, ms=5)
ax.annotate(r"$\gamma\to 2\sqrt{a_0/g_N}$ (deep-MOND)", xy=(0.02,17), xytext=(0.06,12),
            color=C_FW, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.1))
ax.annotate("Newtonian /\nSolar-System\n(Cassini-tested)", xy=(80,1.0), xytext=(15,5.5),
            color=C_NEWTON, fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="->", color=C_NEWTON, lw=1.1))

# shade the gap the theorem confiscates
ax.fill_between(x, gamma_wall, gamma_fw, color=C_FW, alpha=0.08)
ax.text(0.025, 9.5, "the slip the no-go\ntheorem forbids", color=C_FW, fontsize=9, style="italic")

ax.set_xscale("log")
ax.set_xlabel(r"baryonic acceleration  $g_N / a_0$  (low $\to$ high)")
ax.set_ylabel(r"gravitational slip  $\gamma=\Psi/\Phi$")
ax.set_ylim(0, 20)
ax.set_xlim(x.min(), x.max())
ax.set_title("What the lensing wall takes away: the slip that cannot survive covariantly")
ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.text(0.99, 0.02, "framework-computed, a0=9.36e-11 m/s^2", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#999999")
fig.tight_layout(); fig.savefig("ch28_slip_the_wall_confiscates.png", bbox_inches="tight"); print("ok")
