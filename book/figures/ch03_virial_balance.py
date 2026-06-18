import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":False,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis("off")

# --- balance beam pivot ---
pivot=(5,3.4)
ax.plot([pivot[0]],[pivot[1]],marker="^",ms=18,color="#334155")
ax.plot([1.4,8.6],[pivot[1]+0.55,pivot[1]+0.55],color="#334155",lw=3)
ax.plot([pivot[0],pivot[0]],[pivot[1],pivot[1]+0.55],color="#334155",lw=3)

# left pan: 2T (motion)
ax.add_patch(plt.Rectangle((1.6,4.35),2.0,0.9,color=C_DATA,alpha=0.85))
ax.text(2.6,4.8,r"$2\langle T\rangle$",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
ax.text(2.6,5.55,"motion\n(flings apart)",ha="center",va="center",fontsize=9.5,color=C_DATA)

# right pan: |U| (binding) twice as tall
ax.add_patch(plt.Rectangle((6.4,4.35),2.0,1.8,color=C_FW,alpha=0.85))
ax.text(7.4,5.25,r"$|\langle U\rangle|$",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
ax.text(7.4,6.45,"binding\n(holds together)",ha="center",va="center",fontsize=9.5,color=C_FW)

# the locked relation
ax.text(5,2.55,r"$2\langle T\rangle + \langle U\rangle = 0$",ha="center",va="center",
        fontsize=15,fontweight="bold",color="#334155")
ax.text(5,1.95,r"binding $=$ exactly twice the motion",ha="center",va="center",
        fontsize=10,color="#64748b")

# the lesson arrow
ax.annotate("",xy=(8.7,1.15),xytext=(1.3,1.15),
            arrowprops=dict(arrowstyle="-|>",color=C_MOND,lw=2))
ax.text(5,0.62,r"faster swarm ($\sigma\uparrow$, so $T\uparrow$)  $\Rightarrow$  need more binding  $\Rightarrow$  more mass  ($|U|\sim GM^2/R$)",
        ha="center",va="center",fontsize=9.6,color=C_MOND)

ax.text(5,6.85,"The virial balance of a steady self-gravitating swarm",
        ha="center",va="center",fontsize=12,fontweight="bold",color="#334155")
fig.savefig("ch03_virial_balance.png", bbox_inches="tight"); print("ok")
