import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
a0=1.2e-10
gbar=np.logspace(-13,-8,400)
gobs_rar=gbar/(1-np.exp(-np.sqrt(gbar/a0)))
gobs_fw=np.sqrt(gbar**2+gbar*a0)
ax.plot(gbar,gbar,ls="--",color=C_NEWTON,lw=2,label="Newton: $g_{obs}=g_{bar}$")
ax.plot(gbar,gobs_rar,color=C_MOND,lw=2.6,label="RAR fit (McGaugh+ 2016)")
ax.plot(gbar,gobs_fw,color=C_FW,lw=2,ls=(0,(4,2)),label=r"framework dS–Unruh $\sqrt{g_{bar}^2+g_{bar}a_0}$")
ax.axvline(a0,color=C_DATA,lw=1,alpha=0.6)
ax.text(a0*1.3,1e-12,r"$a_0$ hinge",color=C_DATA,fontsize=9,rotation=90,va="bottom")
ax.set_xscale("log");ax.set_yscale("log")
ax.set_xlabel(r"$g_{bar}$ from visible matter  (m s$^{-2}$)")
ax.set_ylabel(r"$g_{obs}$ from rotation  (m s$^{-2}$)")
ax.set_title("The radial-acceleration relation: one law, hundreds of galaxies")
ax.legend(frameon=False,loc="upper left",fontsize=9)
ax.text(0.98,0.03,"curves are models, not data",transform=ax.transAxes,ha="right",fontsize=7,color=C_NEWTON,alpha=0.7)
fig.tight_layout(); fig.savefig("ch19_rar.png", bbox_inches="tight"); print("ok")
