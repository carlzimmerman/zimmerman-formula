import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, axes = plt.subplots(1,2,figsize=(8.4,4.3),sharey=True)

G=6.674e-11; kpc=3.086e19; Msun=1.99e30
Rd=3.0; Mdisk=6e10*Msun; v_flat=200.0
r=np.linspace(0.3,30,400); x=r/Rd
v_bar=np.sqrt(G*(Mdisk*(1-(1+x)*np.exp(-x)))/(r*kpc))/1e3
v_obs=v_flat*np.sqrt(1.0-np.exp(-r/2.0))

for ax in axes:
    ax.plot(r, v_obs, color=C_DATA, lw=2.6, label="observed (flat)")
    ax.plot(r, v_bar, color=C_NEWTON, lw=2.0, ls="--", label="visible matter alone")
    ax.set_xlim(0,30); ax.set_ylim(0,240)
    ax.set_xlabel("radius  $r$  (kpc)")

# LEFT: dark matter fills the gap (extra mass, same Newton law)
v_halo=np.sqrt(np.clip(v_obs**2-v_bar**2,0,None))
axes[0].plot(r, v_halo, color="#475569", lw=1.8, ls=":", label="unseen dark halo")
axes[0].fill_between(r, v_bar, v_obs, color="#94a3b8", alpha=0.18)
axes[0].set_title("Road 1: invisible matter", color="#334155")
axes[0].text(0.5,0.93,"add a dark halo so $M_{\\rm dyn}=M_{\\rm bar}+M_{\\rm dark}$\nkeep $v^2=GM/r$ unchanged",
             transform=axes[0].transAxes, fontsize=8.5, va="top", color="#334155")
axes[0].set_ylabel("orbital speed  $v$  (km/s)")
axes[0].legend(frameon=False, loc="lower right", fontsize=8.5)

# RIGHT: modify the law (same baryons, weak-gravity boost)
a0=9.36e-11
g_bar=(v_bar*1e3)**2/(r*kpc)                 # baryonic accel
g_obs=np.sqrt(g_bar**2+g_bar*a0)             # framework's dS-Unruh interpolation
v_mod=np.sqrt(g_obs*(r*kpc))/1e3
axes[1].plot(r, v_mod, color=C_FW, lw=2.0, label="modified law (same baryons)")
axes[1].fill_between(r, v_bar, v_mod, color=C_FW, alpha=0.10)
axes[1].set_title("Road 2: a modified law of motion", color="#5b21b6")
axes[1].text(0.5,0.93,"no extra matter; below $a_0$ the\nlaw $v^2=GM/r$ itself changes",
             transform=axes[1].transAxes, fontsize=8.5, va="top", color="#5b21b6")
axes[1].legend(frameon=False, loc="lower right", fontsize=8.5)

fig.suptitle("Two roads from one fact: the same flat curve, read two ways", fontsize=12.5)
fig.text(0.012,0.005,"schematic; framework panel uses its own d‐Unruh interpolation, $a_0=9.36\\times10^{-11}$ m/s$^2$",
         fontsize=7, color="#888")
fig.tight_layout(rect=(0,0.02,1,1)); fig.savefig("ch01_two_roads.png", bbox_inches="tight"); print("ok")
