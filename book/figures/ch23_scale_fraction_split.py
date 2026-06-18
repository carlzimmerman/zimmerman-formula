import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Anatomy of a0 = kappa * c * H_Lambda, with kappa the ONE free dial and the
# kernel pieces (Friedmann 3, Einstein 8pi) forced. All values from formulas.
fig, ax = plt.subplots(figsize=(7.6,4.6))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off")
ax.grid(False)

def box(x,y,w,h,fc,ec,txt,tc="white",fs=11,bold=True,alpha=1.0):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.12",
                     fc=fc,ec=ec,lw=1.6,alpha=alpha)
    ax.add_patch(p)
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",color=tc,
            fontsize=fs,fontweight="bold" if bold else "normal")

ax.text(5,9.5,r"$a_0 \;=\; \kappa \;\cdot\; c\,H_\Lambda$",ha="center",
        fontsize=18,color="#1e293b")
ax.text(5,8.75,"one acceleration scale  =  one free dial  ×  one forced cosmic rate",
        ha="center",fontsize=10.5,color="#475569")

# The single free dial (kappa) -- purple, framework
box(0.4,5.6,2.7,2.0,C_FW,"#581c87",r"$\kappa=\frac{1}{2}$"+"\n\nTHE ONE\nFREE DIAL",fs=12)
ax.text(1.75,5.32,"overall normalization,\noutside the root",ha="center",
        va="top",fontsize=8.8,color=C_FW,style="italic")

# multiplication sign
ax.text(3.45,6.6,r"$\times$",ha="center",va="center",fontsize=20,color="#334155")

# The forced kernel -- grey, locked
box(3.8,5.6,5.8,2.0,"#e2e8f0","#94a3b8",
    r"$c\,H_\Lambda=c^2\sqrt{\Lambda/3}\;\approx\;5.4\times10^{-10}\,\mathrm{m/s^2}$",
    tc="#1e293b",fs=11)
ax.text(6.7,5.25,"the dark-energy scale  —  FORCED by holography",ha="center",
        va="top",fontsize=9,color="#475569",style="italic")

# Lock-up: what is forced inside the kernel
ax.text(6.7,4.5,"locked inside the kernel (not adjustable):",ha="center",
        va="center",fontsize=9.5,color="#334155",fontweight="bold")
box(3.9,3.0,1.7,1.0,"#cbd5e1","#94a3b8","3\nFriedmann\n(3-D space)",tc="#1e293b",fs=8.5)
box(5.85,3.0,1.7,1.0,"#cbd5e1","#94a3b8",r"$8\pi$"+"\nEinstein\nfield eqs",tc="#1e293b",fs=8.5)
box(7.8,3.0,1.7,1.0,"#cbd5e1","#94a3b8",r"$\sqrt{\pi}$"+"\nfrom their\nproduct",tc="#1e293b",fs=8.5)

# Bottom: the one wobble -- mirror the "locked inside" header on the right
ax.text(1.75,4.5,"the only adjustable piece:",ha="center",
        va="center",fontsize=9.3,color=C_FW,fontweight="bold")
box(0.55,3.0,2.4,1.0,"#ede9fe",C_FW,
    r"$\kappa$"+" — one free\ndimensionless\nmultiplier",tc=C_FW,fs=9)

# arrow from forced row to result
ax.annotate("",xy=(5,1.85),xytext=(5,2.85),
            arrowprops=dict(arrowstyle="-|>",color="#334155",lw=1.8))
ax.text(5.2,2.35,"plug in  "+r"$\kappa=\frac{1}{2}$",ha="left",va="center",
        fontsize=9.5,color=C_FW)

box(2.7,0.5,4.6,1.3,"#faf5ff",C_FW,
    r"$a_0=c^2\sqrt{\dfrac{\Lambda}{32\pi}}\;\approx\;9.36\times10^{-11}\,\mathrm{m/s^2}$",
    tc=C_FW,fs=12)

ax.text(9.9,0.05,"framework eqns; values computed",ha="right",va="bottom",
        fontsize=7.5,color="#94a3b8")
fig.tight_layout(); fig.savefig("ch23_scale_fraction_split.png", bbox_inches="tight"); print("ok")
