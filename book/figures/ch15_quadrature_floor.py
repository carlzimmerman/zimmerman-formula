import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# de Sitter floor as an acceleration: cH_Lambda ~ 5.4e-10 m/s^2
c = 2.998e8
H_L = 1.8e-18          # de Sitter Hubble rate, s^-1 (worked example, ch.15)
cH = c * H_L           # acceleration form of the temperature floor

a = np.logspace(-12, -7, 600)          # observer's own acceleration (m/s^2)
a_eff = np.sqrt(a**2 + cH**2)          # quadrature -> effective accel scale
unruh = a                              # bare Unruh limit (a_eff = a)
floor = np.full_like(a, cH)            # bare Gibbons-Hawking floor

fig, ax = plt.subplots(figsize=(7,4.3))
ax.loglog(a, a_eff, color=C_FW, lw=2.6, label=r"quadrature  $\sqrt{a^2+(cH_\Lambda)^2}$")
ax.loglog(a, unruh, color=C_NEWTON, ls="--", lw=1.8, label=r"bare Unruh  ($a$)")
ax.loglog(a, floor, color=C_DATA, ls=":", lw=1.8, label=r"de Sitter floor  $cH_\Lambda$")

ax.axvline(cH, color="0.5", lw=1.0, alpha=0.6)
ax.annotate(r"threshold $a=cH_\Lambda$", xy=(cH, cH), xytext=(cH*1.6, cH*0.16),
            fontsize=9.5, color="0.35")
ax.annotate("floor wins\n(temperature bottoms out)", xy=(3e-12, cH),
            xytext=(1.3e-12, cH*2.4), fontsize=8.5, color=C_DATA)
ax.annotate("acceleration wins\n(plain Unruh)", xy=(3e-8, 3e-8),
            xytext=(6e-9, 5e-9), fontsize=8.5, color=C_NEWTON)

ax.set_xlim(1e-12, 1e-7)
ax.set_ylim(2e-11, 1e-7)
ax.set_xlabel(r"observer's acceleration  $a$   (m/s$^2$)")
ax.set_ylabel(r"effective scale  $2\pi k_B T_{\rm eff}/\hbar c$   (m/s$^2$)")
ax.set_title("The de Sitter–Unruh quadrature: a temperature floor")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.text(0.99,0.02,"computed from the framework's equations", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="0.6")
fig.tight_layout(); fig.savefig("ch15_quadrature_floor.png", bbox_inches="tight"); print("ok")
