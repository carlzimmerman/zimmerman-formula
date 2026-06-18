import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# hardcoded published constants (SI)
G   = 6.674e-11      # m^3 kg^-1 s^-2
c   = 2.998e8        # m/s
Msun= 1.989e30       # kg
Rsun= 6.957e8        # m

# light deflection at the solar limb (radians) -> arcseconds
rad_to_arcsec = 180.0/np.pi*3600.0
delta_newton = (2.0*G*Msun)/(c**2*Rsun) * rad_to_arcsec   # ~0.875"
delta_gr     = (4.0*G*Msun)/(c**2*Rsun) * rad_to_arcsec   # ~1.75"

labels = ["Newton\n(time only)", "General Relativity\n(time + space)"]
vals   = [delta_newton, delta_gr]
cols   = [C_NEWTON, C_FW]
x = np.arange(2)
bars = ax.bar(x, vals, width=0.55, color=cols, edgecolor="white", zorder=3)
for xi, v in zip(x, vals):
    ax.text(xi, v+0.04, f"{v:.2f}\"", ha="center", va="bottom", fontweight="bold")

# 1919 Eddington eclipse measurement band (historically reported ~1.6-2.0")
lo, hi = 1.61, 1.98
ax.axhspan(lo, hi, color=C_DATA, alpha=0.16, zorder=1)
ax.axhline((lo+hi)/2.0, color=C_DATA, lw=1.4, ls="-", zorder=2,
           label="Eddington 1919 eclipse (measured)")
ax.text(1.0, hi+0.03, "1919 result lands here", color=C_DATA,
        ha="center", va="bottom", fontsize=9)

# annotate the exact factor of 2
ax.annotate("", xy=(1, delta_gr), xytext=(0, delta_newton),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.1))
ax.text(0.5, (delta_newton+delta_gr)/2.0+0.06, "exactly  x2",
        ha="center", va="bottom", fontsize=10, fontstyle="italic")

ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylim(0, 2.25)
ax.set_ylabel("deflection at Sun's limb  (arcseconds)")
ax.set_title("Bending of starlight grazing the Sun: Newton vs Einstein")
ax.legend(frameon=False, loc="upper left")
ax.text(0.99, 0.02, "computed from 2GM/c²R and 4GM/c²R", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7.5, color="#999999")
fig.tight_layout(); fig.savefig("ch07_light_bending_newton_vs_gr.png", bbox_inches="tight"); print("ok")
