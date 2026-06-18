import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Physical constants (hardcoded, published)
hbar = 1.054571817e-34      # J s
c    = 2.99792458e8         # m/s
kB   = 1.380649e-23         # J/K
H_L  = 1.8e-18              # s^-1, dark-energy expansion rate (chapter value)
a0   = 9.36e-11             # m/s^2, framework a0 = c^2 sqrt(Lambda/32pi)

a_dS = c*H_L                # de Sitter floor acceleration scale = c H_Lambda ~ 5.4e-10
pref = hbar/(2*np.pi*c*kB)  # converts an acceleration to a temperature

# acceleration axis spanning many decades around the floor
a = np.logspace(-13, -7, 600)   # m/s^2
T_unruh = pref*a                                   # ordinary flat-space Unruh
T_eff   = pref*np.sqrt(a**2 + a_dS**2)             # Deser-Levin quadrature
T_floor = pref*a_dS                                 # the floor T_Lambda

fig, ax = plt.subplots(figsize=(7,4.3))
ax.loglog(a, T_eff,   color=C_FW,     lw=2.6, label=r"$T_{\rm eff}=\frac{\hbar}{2\pi c k_B}\sqrt{a^2+(cH_\Lambda)^2}$  (Deser-Levin)")
ax.loglog(a, T_unruh, color=C_NEWTON, lw=1.8, ls="--", label=r"ordinary Unruh $\;T\propto a$  (no floor)")
ax.axhline(T_floor, color=C_DATA, lw=1.4, ls=":", label=r"floor $T_\Lambda\approx 2.2\times10^{-30}\,$K")
ax.axvline(a_dS, color=C_MOND, lw=1.2, ls="-.", alpha=0.8)
ax.axvline(a0,   color=C_FW,   lw=1.2, ls="-",  alpha=0.5)

# annotate the two acceleration markers
ax.annotate(r"$cH_\Lambda\approx5.4\times10^{-10}$", xy=(a_dS, pref*a_dS*0.06),
            xytext=(a_dS*1.4, pref*a_dS*0.012), color=C_MOND, fontsize=9)
ax.annotate(r"$a_0=9.36\times10^{-11}$", xy=(a0, pref*a0*30),
            xytext=(a0*0.02, pref*a0*120), color=C_FW, fontsize=9)
ax.text(2e-13, pref*a_dS*1.6, "vacuum cannot get colder\nthan the floor", fontsize=9, color=C_DATA)
ax.text(2e-8, pref*2e-8*0.18, "hard accel.:\nNewton recovered", fontsize=9, color=C_NEWTON, ha="right")

ax.set_xlabel(r"proper acceleration $a$  (m/s$^2$)")
ax.set_ylabel(r"effective vacuum temperature  $T_{\rm eff}$  (K)")
ax.set_title("The de Sitter-Unruh temperature floor")
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
ax.text(0.99,0.02,"framework-computed",transform=ax.transAxes,ha="right",va="bottom",fontsize=7,color="#999")
fig.tight_layout(); fig.savefig("ch21_desitter_unruh_temperature_floor.png", bbox_inches="tight"); print("ok")
