import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Light bending at the Sun's limb: GR full value vs the Newtonian 'falling photon' half value.
# theta = (factor) * G M / (c^2 R).  Newtonian factor 2, GR factor 4 (time + space curvature).
G=6.674e-11; c=3.00e8; Msun=1.989e30; Rsun=6.96e8
arcsec=206265.0
theta_GR    = 4*G*Msun/(c**2*Rsun)*arcsec    # ~1.75"
theta_Newt  = 2*G*Msun/(c**2*Rsun)*arcsec    # ~0.87"

fig, ax = plt.subplots(figsize=(7.2,4.4))
labels=["Newtonian\n(time-warp only,\nfactor 2)", "General Relativity\n(time + space warp,\nfactor 4)"]
vals=[theta_Newt, theta_GR]
cols=[C_NEWTON, C_FW]
x=np.arange(2)
bars=ax.bar(x, vals, color=cols, width=0.55, alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("deflection of starlight grazing the Sun  (arcseconds)")
ax.set_title("The factor of two: why light bends by 1.75″, not 0.87″")
ax.set_ylim(0,2.35)

for xi,v in zip(x,vals):
    ax.text(xi, v+0.05, f"{v:.2f}″", ha="center", fontsize=12, fontweight="bold", color="#222")

# 1919 Eddington eclipse measurements (real historical values), drawn as an observation band
sobral=(1.98,0.16); principe=(1.61,0.40)
ax.axhspan(principe[0]-principe[1], sobral[0]+sobral[1], color=C_DATA, alpha=0.10)
ax.axhline(sobral[0], color=C_DATA, ls="--", lw=1.3)
ax.axhline(principe[0], color=C_DATA, ls=":", lw=1.3)
ax.text(1.46, sobral[0], f"  Eddington 1919, Sobral: {sobral[0]:.2f}±{sobral[1]:.2f}″",
        color=C_DATA, fontsize=8.5, va="bottom", ha="left")
ax.text(1.46, principe[0], f"  Eddington 1919, Príncipe: {principe[0]:.2f}±{principe[1]:.2f}″",
        color=C_DATA, fontsize=8.5, va="top", ha="left")

# the 'doubling' arrow
ax.annotate("", xy=(1,theta_GR), xytext=(1,theta_Newt),
            arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))
ax.text(0.62, (theta_GR+theta_Newt)/2, "space-curvature\ndoubles it", fontsize=8.5,
        color="#333", ha="center")

ax.text(0.99,0.02,"GR θ = 4GM/(c²R); Newtonian half = 2GM/(c²R)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#999")
fig.tight_layout(); fig.savefig("ch08_light_bending_factor_two.png", bbox_inches="tight"); print("ok")
