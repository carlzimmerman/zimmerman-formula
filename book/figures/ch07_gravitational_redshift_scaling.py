import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# hardcoded published constants
g = 9.81          # m/s^2 (surface)
c = 2.998e8       # m/s

# weak-field redshift line: Delta f / f = g h / c^2
h = np.logspace(-1, 4.2, 400)        # 0.1 m up to ~16 km
frac = g*h/c**2
ax.plot(h, frac, color=C_FW, lw=2.4, zorder=3, label=r"$\Delta f/f = gh/c^2$  (weak field)")

# labelled physical milestones on the line
pts = [
    (0.33, "NIST clocks\n33 cm (2010)", C_DATA, 10, 14),
    (3.0,  "room, 3 m",                 C_FW,    8, -18),
    (400., "tall tower, 400 m",         C_FW,    8, 12),
    (9000.,"mountain, ~9 km",           C_FW,    8, 12),
]
for hi, lab, col, dx, dy in pts:
    yi = g*hi/c**2
    ax.scatter([hi],[yi], s=46, color=col, zorder=5, edgecolor="white", linewidth=0.8)
    ax.annotate(lab, (hi, yi), textcoords="offset points", xytext=(dx,dy),
                fontsize=8.5, color=col, ha="left")

# GPS altitude point uses the FULL potential difference, not g*h
G=6.674e-11; Mearth=5.972e24; Re=6.371e6; h_gps=2.02e7
dPhi = G*Mearth*(1.0/Re - 1.0/(Re+h_gps))   # Phi(ceil)-Phi(floor) > 0
frac_gps = dPhi/c**2
ax.scatter([h_gps],[frac_gps], s=70, marker="*", color=C_DATA, zorder=6,
           edgecolor="white", linewidth=0.8)
ax.annotate("GPS altitude\n(full ΔΦ/c²)", (h_gps, frac_gps),
            textcoords="offset points", xytext=(-6,-30), fontsize=8.5,
            color=C_DATA, ha="right")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("height separation  h  (m)")
ax.set_ylabel(r"fractional clock-rate difference  $\Delta f/f$")
ax.set_title("A clock lower in gravity ticks slower")
ax.set_xlim(0.08, 4e7)
ax.legend(frameon=False, loc="upper left")
ax.text(0.99, 0.02, "computed from gh/c² (and ΔΦ/c² for GPS)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#999999")
fig.tight_layout(); fig.savefig("ch07_gravitational_redshift_scaling.png", bbox_inches="tight"); print("ok")
