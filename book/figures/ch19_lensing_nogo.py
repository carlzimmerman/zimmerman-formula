import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.6))
ax.axis("off");ax.set_xlim(0,10);ax.set_ylim(0,10)
ax.set_title("After GW170817 ($c_T=c$): the relativistic-MOND lensing no-go",fontsize=12)
def box(x,y,w,h,txt,fc,ec,tc,fs=9,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.18",
                fc=fc,ec=ec,lw=1.6))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=tc,
            fontweight="bold" if bold else "normal")
box(1.4,8.2,7.2,1.3,r"GW170817 (2017):  $|c_T-c|/c\ \lesssim\ 10^{-15}$"+"\ngravitational waves travel at the speed of light",
    "#fde8e8",C_DATA,"#7f1d1d",fs=9.5,bold=True)
box(2.6,5.7,4.8,1.5,"Covariant relativistic MOND must:\n• reproduce MOND dynamics\n• match the observed lensing\n• stay safe in the Solar System",
    "#eef2ff",C_NEWTON,"#334155",fs=8.5)
ax.add_patch(FancyArrowPatch((5,8.1),(5,7.25),arrowstyle="-|>",mutation_scale=18,color=C_DATA,lw=2))
ax.text(5.15,7.65,"kills the\nvector/scalar\nlensing trick",fontsize=7.5,color=C_DATA,va="center")
ax.add_patch(FancyArrowPatch((4.0,5.6),(2.7,4.3),arrowstyle="-|>",mutation_scale=16,color=C_FW,lw=1.8))
ax.add_patch(FancyArrowPatch((6.0,5.6),(7.3,4.3),arrowstyle="-|>",mutation_scale=16,color=C_MOND,lw=1.8))
box(0.4,2.6,4.3,1.6,"Escape 1: preferred frame\n(break local Lorentz invariance)\n"+r"$\Rightarrow$ the framework of this book",
    "#f3effe",C_FW,"#4c1d95",fs=8.5,bold=False)
box(5.3,2.6,4.3,1.6,"Escape 2: free lensing function\n(light-bending fit, not derived)\n"+r"$\Rightarrow$ AeST (Skordis–Zlosnik 2021)",
    "#e6f6fb",C_MOND,"#0e4f5c",fs=8.5,bold=False)
box(0.4,0.5,9.2,1.3,"Both routes are honest costs, not solutions. The framework takes the preferred-frame route\n"
    "AND inherits an AeST-class free function — its lensing is irreducibly phenomenological (Ch. 28).",
    "#f8fafc","#cbd5e1","#475569",fs=8.5)
ax.text(9.6,9.7,"schematic",ha="right",fontsize=7,color=C_NEWTON,alpha=0.7)
fig.tight_layout(); fig.savefig("ch19_lensing_nogo.png", bbox_inches="tight"); print("ok")
