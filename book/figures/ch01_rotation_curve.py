import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# Schematic: exponential-disk baryons -> Keplerian falloff vs observed flat curve.
# Enclosed baryonic mass of a razor-thin exponential disk, scale length Rd.
G=6.674e-11; kpc=3.086e19; Msun=1.99e30
Rd=3.0            # disk scale length (kpc)
Mdisk=6e10*Msun   # total baryonic mass ~ Milky-Way-like
r=np.linspace(0.3,30,400)        # kpc
x=r/Rd
# fraction of mass enclosed for exponential disk: 1-(1+x)e^{-x}
fenc=1.0-(1.0+x)*np.exp(-x)
Menc=Mdisk*fenc
v_bar=np.sqrt(G*Menc/(r*kpc))/1e3   # km/s, Newtonian from baryons only

# Observed flat curve: rises then plateaus (schematic shape), plateau ~200 km/s
v_flat=200.0
v_obs=v_flat*np.sqrt(1.0-np.exp(-r/2.0))   # smooth rise to flat plateau

ax.plot(r, v_obs, color=C_DATA, lw=2.6, label="observed (flat) — what galaxies do")
ax.plot(r, v_bar, color=C_NEWTON, lw=2.2, ls="--",
        label="Keplerian from visible matter — what Newton predicts")
ax.axhline(v_flat, color=C_DATA, lw=0.8, ls=":", alpha=0.5)
ax.annotate("speed stays high\nfar out in the dark",
            xy=(26,198), xytext=(17,150),
            arrowprops=dict(arrowstyle="->",color=C_DATA,lw=1.3), color=C_DATA, fontsize=9.5)
ax.annotate("$v\\propto r^{-1/2}$\nthe edge should slow",
            xy=(24,v_bar[np.argmin(abs(r-24))]), xytext=(10,55),
            arrowprops=dict(arrowstyle="->",color=C_NEWTON,lw=1.3), color=C_NEWTON, fontsize=9.5)

ax.set_xlim(0,30); ax.set_ylim(0,240)
ax.set_xlabel("distance from galaxy center  $r$  (kiloparsecs)")
ax.set_ylabel("orbital speed  $v$  (km/s)")
ax.set_title("The flat rotation curve: the central mystery")
ax.legend(frameon=False, loc="lower right", fontsize=9.5)
ax.text(0.012,0.02,"schematic shapes; baryon curve from an exponential-disk model",
        transform=ax.transAxes, fontsize=7, color="#888")
fig.tight_layout(); fig.savefig("ch01_rotation_curve.png", bbox_inches="tight"); print("ok")
