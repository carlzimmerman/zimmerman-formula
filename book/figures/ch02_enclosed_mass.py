import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
G=6.674e-11; Msun=1.989e30; kpc=3.086e19
r=np.linspace(1,30,400)
v_flat=180e3
M_dyn=(v_flat**2*(r*kpc)/G)/Msun                # dynamical: M(<r)=v^2 r/G, grows as r
Rd=3.0                                            # exponential-disk scale radius (kpc)
x=r/Rd
M_match=M_dyn[np.argmin(np.abs(r-8.0))]           # tie luminous total to dyn at bright edge
norm=1-(1+8.0/Rd)*np.exp(-8.0/Rd)
M_lum=M_match*(1-(1+x)*np.exp(-x))/norm            # cumulative exponential disk, levels off
M_lum=np.minimum(M_lum,M_match)
ax.plot(r, M_dyn/1e10, color=C_DATA, lw=2.6,
        label=r"dynamical mass the scale reads: $M(<r)=v_{\rm flat}^2 r/G\propto r$")
ax.plot(r, M_lum/1e10, color=C_NEWTON, lw=2.4, ls="--",
        label="luminous mass enclosed (levels off)")
ax.fill_between(r, M_lum/1e10, M_dyn/1e10, where=(M_dyn>=M_lum),
                color=C_FW, alpha=0.13)
ax.text(22, 14, "the gap:\n'missing' mass", color=C_FW, fontsize=9, ha="center")
ax.set_xlabel("radius from galaxy center  (kpc)")
ax.set_ylabel(r"enclosed mass  ($10^{10}\,M_\odot$)")
ax.set_title("More mass keeps being enclosed where the light has stopped")
ax.set_xlim(1,30); ax.set_ylim(0, None)
ax.legend(frameon=False, loc="upper left")
ax.text(0.99,0.02,r"framework-computed: $v_{\rm flat}=180$ km/s", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#aaa")
fig.tight_layout(); fig.savefig("ch02_enclosed_mass.png", bbox_inches="tight"); print("ok")
