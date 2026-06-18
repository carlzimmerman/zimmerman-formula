import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.6))

# A log ladder of accelerations, all computed from elementary formulas / hardcoded constants.
G=6.674e-11; Msun=1.989e30; AU=1.496e11; c=2.998e8; H0=2.27e-18  # H0 ~ 70 km/s/Mpc in 1/s
g_apple   = 9.8
g_es      = G*Msun/AU**2               # Earth's acceleration toward the Sun
g_pioneer = 8.7e-10                     # (illustrative famous small anomaly)
g_gal     = G*(5e10*Msun)/(20*3.086e19)**2  # outer galaxy field, point-mass approx
a0        = 1.2e-10
cH0       = c*H0

labels = ["apple\nfalling on Earth", "Earth orbiting\nthe Sun",
          "a star at the\nedge of a galaxy", r"$a_0$ (MOND scale)", r"$cH_0$ (cosmic)"]
vals   = [g_apple, g_es, g_gal, a0, cH0]
cols   = [C_NEWTON, C_NEWTON, C_DATA, C_FW, C_MOND]
y = np.arange(len(vals))[::-1]
ax.barh(y, np.log10(vals), color=cols, alpha=0.85, height=0.55)
for yi, v, lab in zip(y, vals, labels):
    ax.text(np.log10(v)+0.3 if v<1 else np.log10(v)+0.3, yi, f"{v:.1e} m/s$^2$",
            va="center", ha="left", fontsize=9)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.5)
ax.axvline(np.log10(a0), color=C_FW, ls=":", lw=1.4, alpha=0.7)
ax.set_xlim(-11, 4)
ax.set_xlabel(r"acceleration  $\log_{10}(a\,/\,\mathrm{m\,s^{-2}})$")
ax.set_title(r"How small is small: $a_0$ sits ~11 orders of magnitude below an apple")
ax.grid(axis="y", alpha=0)
ax.text(0.99, 0.02, "framework-computed", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch17_acceleration_ladder.png", bbox_inches="tight"); print("ok")
