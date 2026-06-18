import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs
fig, ax = plt.subplots(figsize=(7,4.3))

# Constants (SI) and units
G   = 6.674e-11
kpc = 3.086e19
Msun= 1.989e30
vflat = 2.0e5          # 200 km/s, the chapter's worked example

r_kpc = np.linspace(0.5, 30.0, 400)
r = r_kpc*kpc

# Dynamical (total) enclosed mass demanded by a FLAT curve: M(r)=v^2 r/G  ->  M ~ r
M_dyn = (vflat**2 * r / G)/Msun

# Visible (stars+gas) enclosed mass: exponential disk, M_vis(r)=M_inf*[1-(1+r/Rd)e^{-r/Rd}]
# tends to a CONSTANT as the light runs out.
M_inf = 5.5e10         # ~5.5e10 Msun total visible, per the chapter's worked example
Rd_kpc = 3.0
frac = 1 - (1 + r_kpc/Rd_kpc)*np.exp(-r_kpc/Rd_kpc)
M_vis = M_inf*frac

ax.plot(r_kpc, M_dyn/1e10, color=C_FW, lw=2.6,
        label=r"dynamical, from flat curve:  $M\propto r$")
ax.plot(r_kpc, M_vis/1e10, color=C_NEWTON, lw=2.4, ls="--",
        label="visible (stars+gas): light runs out")
ax.fill_between(r_kpc, M_vis/1e10, M_dyn/1e10, color="#ede9fe", alpha=0.7, zorder=0)

# annotate the factor at 30 kpc
Md30 = (vflat**2 * 30*kpc / G)/Msun
Mv30 = M_inf*(1 - (1+30/Rd_kpc)*np.exp(-30/Rd_kpc))
ratio = Md30/Mv30
ax.annotate(f"factor ~{ratio:.0f} at 30 kpc\n(grows with radius)",
            xy=(30, Md30/1e10), xytext=(19, 24),
            fontsize=9.5, color=C_DATA, ha="center",
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.2))
ax.text(28, Mv30/1e10+0.4, "visible plateau", ha="right", va="bottom",
        fontsize=9, color="#5f5e5a")

ax.set_xlim(0,30); ax.set_ylim(0, 30)
ax.set_xlabel("radius  $r$  (kpc)")
ax.set_ylabel(r"enclosed mass  $M(<r)$  ($10^{10}\,M_\odot$)")
ax.set_title(r"A flat curve demands mass rising linearly with radius")
ax.legend(frameon=False, loc="upper left", fontsize=9.5)
ax.text(0.99, 0.02, r"$v_{\rm flat}=200$ km/s", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8.5, color="#b4b2a9")
fig.tight_layout(); fig.savefig("ch04_enclosed_mass_divergence.png", bbox_inches="tight"); print("ok")
