import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# Constants (SI) and a respectable spiral, M = 5e10 solar masses (the chapter's worked example)
G = 6.674e-11; Msun = 1.989e30; a0 = 1.2e-10; kpc = 3.086e19
M = 5e10 * Msun

# Radii out into the flat skirts (point-mass approximation for the outer galaxy)
r = np.linspace(1.0, 35.0, 400) * kpc
gN = G * M / r**2                       # Newtonian field from visible mass alone
v_newton = np.sqrt(gN * r) / 1e3        # Keplerian: declines as 1/sqrt(r)
v_deep   = (G * M * a0)**0.25 + 0*r      # deep-MOND flat line v^4 = G M a0
v_deep   = v_deep / 1e3
gobs = np.sqrt(gN**2 + gN * a0)         # framework interpolation g_obs = sqrt(gN^2 + gN a0)
v_obs  = np.sqrt(gobs * r) / 1e3

rk = r / kpc
ax.plot(rk, v_newton, color=C_NEWTON, ls="--", lw=2.2,
        label="Newton, visible mass only  (Keplerian decline)")
ax.plot(rk, v_obs, color=C_FW, lw=2.6,
        label=r"MOND interpolation  $g_{\rm obs}=\sqrt{g_N^2+g_N a_0}$")
ax.plot(rk, v_deep, color=C_MOND, ls=":", lw=2.0,
        label=r"deep-MOND flat speed  $v^4=GMa_0$")

ax.axhline(168, color=C_DATA, lw=1.0, alpha=0.5)
ax.annotate(r"$v\approx168$ km/s", xy=(31, 168), xytext=(31, 195),
            color=C_DATA, fontsize=9, ha="center")
ax.set_ylim(0, 360)
ax.set_xlim(1, 35)
ax.set_xlabel("radius from galaxy centre  (kpc)")
ax.set_ylabel("orbital speed  (km/s)")
ax.set_title(r"One number flattens the curve: $M=5\times10^{10}\,M_\odot$, $a_0=1.2\times10^{-10}$ m/s$^2$")
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.text(0.99, 0.02, "framework-computed", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch17_flat_rotation_curve.png", bbox_inches="tight"); print("ok")
