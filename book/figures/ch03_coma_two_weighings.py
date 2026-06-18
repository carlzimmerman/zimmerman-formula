import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# --- Dynamical mass from the chapter's Worked Example (virial M = 3 sigma^2 R / G) ---
sigma = 1.0e6          # m/s  (1000 km/s)
R     = 1.5*3.086e22   # m    (1.5 Mpc)
G     = 6.67e-11
Msun  = 1.989e30       # kg
M_dyn = 3.0*sigma**2*R/G / Msun   # ~1e15 Msun

# --- Baryonic ledger, in solar masses, using the chapter's round ratios ---
M_stars = 3.0e12               # 'a few times 1e12 Msun' of stars
M_gas   = 4.0*M_stars          # hot X-ray gas a few times the stars
M_bary  = M_stars + M_gas      # stars + gas

labels = ["Stars\n(1933 light\ncensus)", "Stars + hot\nX-ray gas\n(all baryons)",
          "Dynamical mass\nfrom motion\n(virial $\\sigma^2R/G$)"]
vals   = [M_stars, M_bary, M_dyn]
cols   = [C_DATA, C_MOND, C_FW]
x = np.arange(3)
bars = ax.bar(x, vals, color=cols, width=0.62, edgecolor="white")
ax.set_yscale("log")
ax.set_ylim(8e11, 4e15)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("mass enclosed  ($M_\\odot$)")
ax.set_title("Coma cluster: the gap, and what closes it")

for xi,v in zip(x,vals):
    _mm,_ee=f"{v:.0e}".split("e"); ax.text(xi, v*1.18, rf"${int(_mm)}\times10^{{{int(_ee)}}}$", ha="center", va="bottom", fontsize=9)


# annotate the two factors that matter
f_total = M_dyn/M_stars
f_resid = M_dyn/M_bary
ax.annotate(f"Zwicky's gap\n$\\sim{f_total:.0f}\\times$",
            xy=(2,M_dyn), xytext=(0.15,M_dyn),
            ha="center", va="center", fontsize=9.5, color=C_FW,
            arrowprops=dict(arrowstyle="-|>", color=C_FW, lw=1.3,
                            connectionstyle="arc3,rad=-0.25"))
ax.annotate(f"residual after ALL\nordinary matter:\n$\\sim{f_resid:.0f}\\times$ — survives",
            xy=(2,M_dyn*0.9), xytext=(1.05,7e13),
            ha="center", va="center", fontsize=9.5, color=C_MOND,
            arrowprops=dict(arrowstyle="-|>", color=C_MOND, lw=1.3,
                            connectionstyle="arc3,rad=0.2"))

ax.text(0.99,0.02,"virial $M=3\\sigma^2R/G$; baryon ratios per chapter text",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#888")
fig.tight_layout(); fig.savefig("ch03_coma_two_weighings.png", bbox_inches="tight"); print("ok")
