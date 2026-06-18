import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
C_KILL="#b91c1c"; C_DISS="#d97706"; C_GOOD="#15803d"

fig, ax = plt.subplots(figsize=(8.2,5.6))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off"); ax.grid(False)

def box(x,y,w,h,text,fc,ec,tc="white",fs=9.5,bold=True):
    p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.06,rounding_size=0.14",
        linewidth=1.6,facecolor=fc,edgecolor=ec,zorder=3)
    ax.add_patch(p)
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc,
        fontweight=("bold" if bold else "normal"),zorder=4)

def arrow(x1,y1,x2,y2,label="",lx=0,ly=0,color="#475569"):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=13,
        linewidth=1.5,color=color,zorder=2)
    ax.add_patch(a)
    if label:
        ax.text((x1+x2)/2+lx,(y1+y2)/2+ly,label,ha="center",va="center",
            fontsize=8.2,color="#334155",style="italic",zorder=4,
            bbox=dict(boxstyle="round,pad=0.12",fc="white",ec="none",alpha=0.85))

# root
box(5.0,9.2,5.3,0.95,"a$_0$ = c$^2\\sqrt{\\Lambda/32\\pi}$ tied to dark energy\nDoes the distinctive a$_0$(z) prediction survive the decade?",
    C_FW,"#5b21b6",fs=9.2)

# first split: does DE evolve?
box(5.0,7.3,3.0,0.8,"Does dark energy\nevolve? (DESI DR3)","#1e293b","#0f172a",fs=9.5)
arrow(5.0,8.72,5.0,7.72)

# Branch A (no -> dissolve)
box(1.7,5.2,2.7,1.15,"BRANCH A\nw → −1 constant\n→ DISSOLUTION\nfolds into MOND",C_DISS,"#b45309",fs=8.8)
arrow(3.55,7.05,2.0,5.85,"no  (modal\noutcome)",lx=-0.15,ly=0.25,color=C_DISS)

# yes -> second split: BTFR sign
box(6.6,5.2,2.9,0.85,"High-z BTFR offset\nsign? (ELT/JWST)","#1e293b","#0f172a",fs=9.2)
arrow(5.7,6.92,6.4,5.72,"yes, DE\nevolves",lx=0.55,ly=0.15,color="#15803d")

# Branch B (kill) and C (support)
box(4.6,2.9,2.6,1.15,"BRANCH B\nflat / wrong sign\n→ KILL\nfalsified",C_KILL,"#7f1d1d",fs=8.8)
box(8.3,2.9,2.6,1.15,"BRANCH C\n~7% slow at z≈3\n→ STRONG SUPPORT\nrisky test passed",C_GOOD,"#14532d",fs=8.6)
arrow(6.0,4.77,4.9,3.48,"fast / none",lx=-0.5,ly=0.05,color=C_KILL)
arrow(7.2,4.77,8.1,3.48,"slow, right size",lx=0.55,ly=0.05,color=C_GOOD)

# side branches D and E (independent fronts)
box(1.7,2.4,2.7,1.5,"BRANCH D (theory)\ncovariant Cassini-safe\nMOND lensing built\n→ major advance\n(whole field)\n\nBRANCH E (rival)\nDM particle detected\n→ rival road wins","#f1f5f9","#94a3b8",tc="#1e293b",fs=7.8,bold=False)
ax.text(1.7,3.55,"independent fronts",ha="center",fontsize=7.6,color="#64748b",style="italic")

ax.text(5.0,0.45,"B and E are the genuine kill conditions · A is the dissolver · C and D are the upside",
    ha="center",fontsize=8.6,color="#334155")
ax.text(9.9,0.05,"schematic of Chapter 32 decision tree",ha="right",fontsize=6.5,color="#94a3b8")
ax.set_title("The framework's decision tree: kill, dissolve, or support",fontsize=12.5,pad=8)
fig.tight_layout(); fig.savefig("ch32_decision_tree.png", bbox_inches="tight"); print("ok")
