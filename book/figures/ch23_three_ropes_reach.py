import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# The unforceability theorem as a "how far each rope reaches" diagram.
# Three principles; a shared ladder of what could be constrained, ending at kappa.
fig, ax = plt.subplots(figsize=(7.8,4.7))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off"); ax.grid(False)

# The ladder of constrainable things, left to right (increasing "reach")
stops = ["signs", "ratios", "the SCALE\n"+r"$a_0\sim cH_\Lambda$", "the FRACTION\n"+r"$\kappa=\frac{1}{2}$"]
xstop = [1.6, 3.6, 5.9, 8.6]
ax.text(5,9.55,"The unforceability theorem:  how far each rope reaches",
        ha="center",fontsize=12.5,color="#1e293b",fontweight="bold")
# baseline ladder
for i,(s,x) in enumerate(zip(stops,xstop)):
    col = C_FW if i==3 else "#334155"
    ax.plot([x],[8.2],marker="o",ms=9,color=col,zorder=5)
    ax.text(x,8.65,s,ha="center",va="bottom",fontsize=9.5,
            color=col,fontweight="bold")
ax.plot([xstop[0]-0.3,xstop[-1]],[8.2,8.2],color="#cbd5e1",lw=2,zorder=1)
ax.text(xstop[-1]+0.05,7.75,"  <-- the one\n  free number",ha="left",va="top",
        fontsize=9,color=C_FW,style="italic")

# Three ropes as horizontal bars that STOP at their reach
ropes = [
    ("Ghost-freedom",  "#0e7490", 1, 6.5,
     "checks the SIGN of every mode's energy.\nAn overall +scale flips no signs -> blind."),
    ("Unitarity",      "#0891b2", 2, 4.7,
     "polices RATIOS so probabilities sum to 1.\nAn overall +scale cancels in every ratio -> blind."),
    ("Holography",     "#7c3aed", 2.6, 2.9,
     "ties "+r"$a_0$"+" to the cosmic horizon -> sets the SCALE.\nAn order-of-magnitude rope: stops before the coefficient."),
]
for name,col,reach_idx,y,desc in ropes:
    x0 = xstop[0]-0.3
    x1 = xstop[int(np.floor(reach_idx))] if reach_idx==int(reach_idx) else \
         xstop[int(np.floor(reach_idx))] + (xstop[int(np.floor(reach_idx))+1]-xstop[int(np.floor(reach_idx))])*(reach_idx-int(reach_idx))
    p=FancyBboxPatch((x0,y-0.28),x1-x0,0.56,boxstyle="round,pad=0.0,rounding_size=0.14",
                     fc=col,ec="none",alpha=0.85)
    ax.add_patch(p)
    ax.text(x0+0.12,y,name,ha="left",va="center",color="white",
            fontsize=10.5,fontweight="bold")
    # the "knot" where it stops
    ax.plot([x1],[y],marker="|",ms=20,color="#1e293b",mew=3,zorder=6)
    ax.text(x1+0.12,y+0.45,"stops here",ha="left",va="center",fontsize=8,
            color="#1e293b",style="italic")
    ax.text(x0+0.12,y-0.62,desc,ha="left",va="top",fontsize=8.3,color="#475569")
    # dashed continuation showing it never reaches kappa
    ax.plot([x1,xstop[-1]],[y,y],color=col,ls=":",lw=1.3,alpha=0.6,zorder=2)

# kappa marker column
ax.axvline(xstop[-1],ymin=0.10,ymax=0.86,color=C_FW,ls="--",lw=1.4,alpha=0.7)
ax.plot([xstop[-1]],[0.95],marker="*",ms=22,color=C_FW,zorder=7)
ax.text(xstop[-1]-0.25,0.95,"no rope\nreaches "+r"$\kappa$",ha="right",va="center",
        fontsize=10,color=C_FW,fontweight="bold")

ax.text(0.1,0.02,"schematic of the unforceability theorem",ha="left",va="bottom",
        fontsize=7.5,color="#94a3b8")
fig.tight_layout(); fig.savefig("ch23_three_ropes_reach.png", bbox_inches="tight"); print("ok")
