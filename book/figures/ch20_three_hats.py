import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# --- constants (cosmos only; no galaxy data) ---
c     = 2.998e8          # m/s
G     = 6.674e-11        # m^3 kg^-1 s^-2
H0    = 67.4*1e3/3.086e22  # s^-1  (67.4 km/s/Mpc)
OmL   = 0.685
H_L   = H0*np.sqrt(OmL)            # pure-Lambda Hubble rate
Lam   = 3.0*H_L**2/c**2           # m^-2
rho_DE= Lam*c**2/(8*np.pi*G)      # kg/m^3
Z     = np.sqrt(32*np.pi/3.0)     # 5.789...

# --- the three algebraically identical hats ---
hat1 = c**2*np.sqrt(Lam/(32*np.pi))   # curvature form
hat2 = (c/2.0)*np.sqrt(G*rho_DE)      # density form
hat3 = c*H_L/Z                        # rate form
vals = np.array([hat1, hat2, hat3])
S    = 1e10                           # plot everything in units of 1e-10 m/s^2

labels = [r"Hat 1   $a_0=c^2\sqrt{\dfrac{\Lambda}{32\pi}}$",
          r"Hat 2   $a_0=\dfrac{c}{2}\sqrt{G\,\rho_{\rm DE}}$",
          r"Hat 3   $a_0=\dfrac{c\,H_\Lambda}{Z}$"]
colors = [C_FW, C_MOND, "#2563eb"]

fig, ax = plt.subplots(figsize=(7.8,4.3))
y = np.arange(len(vals))[::-1]
ax.barh(y, vals*S, color=colors, alpha=0.85, height=0.55, zorder=3)
for yi, v in zip(y, vals):
    ax.text(v*S+0.015, yi, f"{v*1e11:.2f}"+r"$\times10^{-11}$", va="center", ha="left",
            fontsize=9.5, fontweight="bold", color="#1e293b")

# observed RAR band (the scale galaxies show: ~0.9 to 1.3 e-10) and MOND-tradition line
ax.axvspan(0.9, 1.3, color=C_DATA, alpha=0.10, zorder=0)
ax.axvline(1.2, color=C_DATA, lw=1.4, ls=":", zorder=2)
ax.text(1.205, 2.30, "MOND-tradition\n$1.2\\times10^{-10}$", color=C_DATA,
        fontsize=8.0, va="top", ha="left")
ax.text(1.10, -0.66, "observed rotation-curve band  $\\sim(0.9$\u2013$1.3)\\times10^{-10}$",
        color=C_DATA, fontsize=8.0, ha="center", va="center")

ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=10.5)
ax.set_xlim(0, 1.45); ax.set_ylim(-1.0, 2.75)
ax.set_xlabel(r"$a_0$  ($\times10^{-10}$ m/s$^2$)")
ax.set_title("One number, three equivalent forms \u2014 all from the cosmos, none from galaxies",
             fontsize=11.5)
ax.text(0.50, 2.0, "all three identical:\n$9.36\\times10^{-11}$ m/s$^2$",
        fontsize=9, ha="center", va="center", color="#5b21b6",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f3e8ff", ec=C_FW, alpha=0.9))
fig.subplots_adjust(left=0.30, right=0.97, top=0.90, bottom=0.13)
fig.savefig("ch20_three_hats.png", bbox_inches="tight"); print("ok")
