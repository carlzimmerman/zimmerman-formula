import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
r=np.linspace(0.05,2.0,400)
eta=1.0+1.0*np.exp(-(r/0.55))
ax.plot(r,eta,color=C_MOND,lw=2.6,label=r"MOND residual $\eta(r)=M_{dyn}/M_{MOND}$")
ax.axhline(1.0,color=C_NEWTON,ls="--",lw=1.6,label=r"$\eta=1$ (no residual, MOND closes it)")
ax.fill_between(r,1.0,eta,color=C_MOND,alpha=0.10)
ax.axhline(5.5,color=C_DATA,ls=":",lw=1.6,label=r"no modification: $\eta\sim5$–6 (full missing mass)")
ax.annotate(r"$\eta\sim2$ at the center"+"\n(stubborn residual)",xy=(0.07,1.93),xytext=(0.55,3.0),
            fontsize=9,color=C_MOND,arrowprops=dict(arrowstyle="->",color=C_MOND,lw=1.2))
ax.annotate("outskirts:\nMOND does fine",xy=(1.7,1.04),xytext=(1.15,1.9),fontsize=9,color=C_NEWTON,
            arrowprops=dict(arrowstyle="->",color=C_NEWTON,lw=1.0))
ax.set_xlim(0,2.0);ax.set_ylim(0.5,6.2)
ax.set_xlabel(r"radius  ($r/r_{500}$)")
ax.set_ylabel(r"residual mass ratio  $\eta$")
ax.set_title("The cluster loss: MOND does most of the work, but a factor ~2 remains")
ax.legend(frameon=False,loc="upper right",fontsize=8.5)
ax.text(0.02,0.03,"illustrative profile, schematic of Sanders 1999 / Pointecouteau & Silk 2005",
        transform=ax.transAxes,ha="left",fontsize=7,color=C_NEWTON,alpha=0.7)
fig.tight_layout(); fig.savefig("ch19_cluster_eta.png", bbox_inches="tight"); print("ok")
