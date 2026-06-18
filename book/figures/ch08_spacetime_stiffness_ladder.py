import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Dimensionless curvature |Phi|/c^2 = G M / (R c^2) at each object's own surface.
# Everything computed from the formula; masses/radii are hardcoded published constants (SI).
G=6.674e-11; c=3.00e8
objects=[
    ("Apple (held)", 0.1, 0.03),          # m, r in meters
    ("Earth",        5.972e24, 6.371e6),
    ("Jupiter",      1.898e27, 6.99e7),
    ("Sun",          1.989e30, 6.96e8),
    ("White dwarf",  1.4*1.989e30, 7.0e6),
    ("Neutron star", 1.4*1.989e30, 1.2e4),
    ("Black hole\n(at horizon)", 1.4*1.989e30, 2*G*1.4*1.989e30/c**2),
]
names=[o[0] for o in objects]
phi=np.array([G*M/(R*c**2) for (_,M,R) in objects])

fig, ax = plt.subplots(figsize=(7.4,4.5))
y=np.arange(len(objects))[::-1]
bars=ax.barh(y, phi, color=C_FW, alpha=0.85, height=0.6)
ax.set_xscale("log")
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlim(1e-19, 5)
ax.set_xlabel(r"dimensionless curvature  $|\Phi|/c^2 = GM/(Rc^2)$  (log scale)")
ax.set_title("Spacetime is staggeringly 'stiff': it takes a star to dent it noticeably")

# annotate each bar with its value
for yi, p in zip(y, phi):
    ax.text(p*1.6, yi, f"{p:.1e}", va="center", fontsize=9, color="#222")

# the Sun-at-Earth value from the worked example, marked as a reference line
phi_sun_earth = G*1.989e30/(1.496e11*c**2)   # ~9.9e-9
ax.axvline(phi_sun_earth, color=C_DATA, ls=":", lw=1.6)
ax.text(phi_sun_earth, len(objects)-0.35, "  Sun's well at\n  Earth's orbit\n  (~1e-8)",
        color=C_DATA, fontsize=8.5, va="top")

# regime label
ax.text(2e-18, 0.0, "weak field\n(Newton works)", fontsize=8.5, color=C_NEWTON, ha="left")
ax.text(0.25, 5.7, "strong field\n(full GR)", fontsize=8.5, color="#333", ha="center")

ax.text(0.99,0.02,"framework-computed from Φ/c² = GM/(Rc²)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#999")
fig.tight_layout(); fig.savefig("ch08_spacetime_stiffness_ladder.png", bbox_inches="tight"); print("ok")
