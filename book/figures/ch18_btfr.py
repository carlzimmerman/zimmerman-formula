import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

G  = 6.674e-11           # m^3 kg^-1 s^-2
a0 = 1.2e-10             # m/s^2
Msun = 1.989e30          # kg

# BTFR from the deep-MOND limit:  V^4 = G M a0  ->  V = (G M a0)^(1/4)
M_sun = np.logspace(7, 12, 300)          # 1e7 .. 1e12 solar masses
M_kg  = M_sun * Msun
V_kms = (G * M_kg * a0)**0.25 / 1e3       # km/s

fig, ax = plt.subplots(figsize=(7, 4.6))

# the exact slope-4 BTFR line (framework value a0 = 9.36e-11) for comparison
a0_fw = 9.36e-11
V_fw_kms = (G * M_kg * a0_fw)**0.25 / 1e3
ax.plot(V_kms, M_sun, color=C_MOND, lw=2.6,
        label=r"$V^4=GM\,a_0$, $a_0=1.2\times10^{-10}$ (RAR fit)")
ax.plot(V_fw_kms, M_sun, color=C_FW, lw=2.0, ls="-",
        label=r"$V^4=GM\,a_0$, $a_0=9.36\times10^{-11}$ (framework)")

# a Newtonian "slope 3" comparison curve through the same anchor, to show 4 != 3
anchor_V, anchor_M = 180.0, 6.6e10
V3 = np.logspace(np.log10(20), np.log10(360), 300)
M3 = anchor_M * (V3/anchor_V)**3
ax.plot(V3, M3, color=C_NEWTON, ls="--", lw=1.8,
        label=r"slope-3 reference ($M\propto V^3$)")

# illustrative, model-generated galaxies scattered about the BTFR line
rng = np.random.default_rng(1977)
Mg = 10**rng.uniform(7.2, 11.8, 90) * Msun
Vg = (G * Mg * a0)**0.25 / 1e3
Vg *= 10**(rng.normal(0, 0.026, Vg.size))   # ~0.026 dex in V (tiny scatter)
ax.scatter(Vg, Mg/Msun, s=12, color=C_DATA, alpha=0.40, lw=0,
           label="illustrative galaxies (model + tiny scatter)")

# Milky Way worked example from the chapter
ax.scatter([180], [6.6e10], s=90, marker="*", color="black", zorder=5)
ax.annotate("Milky Way:\n$V\\approx180$ km/s\n$M\\approx6.6\\times10^{10}\\,M_\\odot$",
            xy=(180, 6.6e10), xytext=(70, 8e10),
            fontsize=9, arrowprops=dict(arrowstyle="->", alpha=0.6))

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(18, 380); ax.set_ylim(5e6, 3e12)
ax.set_xlabel(r"flat rotation speed  $V$   (km/s)")
ax.set_ylabel(r"baryonic mass  $M$  (stars + gas)   ($M_\odot$)")
ax.set_title("The Baryonic Tully-Fisher Relation:  $M\\propto V^{4}$, size-independent")
ax.legend(frameon=False, fontsize=8.2, loc="lower right")
ax.text(0.005, 0.005, "lines computed from $V^4=GMa_0$; points illustrative, not real data",
        transform=ax.transAxes, fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("ch18_btfr.png", bbox_inches="tight"); print("ok")
