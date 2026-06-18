import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

fig, ax = plt.subplots(figsize=(7,4.3))

# Worked example of the chapter: rho_crit = 3 H0^2 / (8 pi G).
G = 6.674e-11          # m^3 kg^-1 s^-2
Mpc = 3.086e22         # m
m_H = 1.6726e-27       # kg, hydrogen atom mass (for the 'atoms per m^3' axis)

H0_kms = np.linspace(64.0, 76.0, 400)          # km/s/Mpc
H0_si  = (H0_kms*1.0e3)/Mpc                     # s^-1
rho_crit = 3.0*H0_si**2/(8.0*np.pi*G)          # kg/m^3

ax.plot(H0_kms, rho_crit*1e27, color=C_FW, lw=2.6,
        label=r"$\rho_{\rm crit}=3H_0^2/8\pi G \propto H_0^2$")

# The two ends of the Hubble tension named in Question 4.
def rc(H0):
    return 3.0*((H0*1e3)/Mpc)**2/(8.0*np.pi*G)
for H0v, lab, col in [(67.0, "Planck CMB\n$H_0\\approx67$", C_DATA),
                      (73.0, "Local (Cepheid)\n$H_0\\approx73$", C_MOND)]:
    y = rc(H0v)*1e27
    ax.scatter([H0v],[y], color=col, zorder=6, s=46)
    ax.annotate(lab, xy=(H0v,y), xytext=(H0v-1.2, y+0.9 if col==C_DATA else y-1.4),
                fontsize=9, color=col, ha="center",
                arrowprops=dict(arrowstyle="->", color=col, lw=1.1))

# The chapter's own worked point at 70.
y70 = rc(70.0)*1e27
ax.scatter([70.0],[y70], color="k", zorder=6, s=40)
ax.annotate(rf"chapter's example\n$H_0{{=}}70 \Rightarrow {y70:.1f}\times10^{{-27}}$".replace("\\n","\n"),
            xy=(70.0,y70), xytext=(70.3, y70-2.3), fontsize=8.5, color="k",
            arrowprops=dict(arrowstyle="->", color="k", lw=1.0, alpha=0.7))

# secondary axis: hydrogen atoms per cubic meter
ax2 = ax.twinx()
ax2.spines.top.set_visible(False)
lo, hi = ax.get_ylim()
ax2.set_ylim(lo*1e-27/m_H, hi*1e-27/m_H)
ax2.set_ylabel("hydrogen atoms per cubic meter", color="#555555")
ax2.grid(False)

ax.set_xlabel(r"Hubble constant  $H_0$  (km s$^{-1}$ Mpc$^{-1}$)")
ax.set_ylabel(r"critical density  $\rho_{\rm crit}$  ($10^{-27}$ kg/m$^3$)")
ax.set_title("Weighing the universe: critical density grows as $H_0^2$")
ax.legend(frameon=False, loc="upper left")
ax.text(0.97, 0.04, "the ~9% Hubble tension $\\to$ ~19% spread in $\\rho_{\\rm crit}$",
        transform=ax.transAxes, ha="right", fontsize=7.5, color="#666666")

fig.tight_layout(); fig.savefig("ch09_critical_density_vs_H0.png", bbox_inches="tight"); print("ok")
