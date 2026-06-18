import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# SCHEMATIC: the chapter's central logical contrast, written on the Einstein equation.
# Road one (dark matter): change the SOURCE T, keep the law.
# Road two (modified dynamics): change the LAW (G-side / inertia), keep the source.
fig, ax = plt.subplots(figsize=(7.4,4.8))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis("off"); ax.grid(False)

def box(x,y,w,h,fc,ec,lw=1.8):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.18",
                     fc=fc,ec=ec,lw=lw); ax.add_patch(b)

# The shared fork at the top
box(3.0,8.4,4.0,1.25,"#f5f3ff",C_NEWTON)
ax.text(5.0,9.35,"The cosmic ledger does not balance",ha="center",va="center",
        fontsize=10.5,fontweight="bold")
ax.text(5.0,8.78,"motions need more gravity than visible matter gives",
        ha="center",va="center",fontsize=8.5,color="0.3")

# The Einstein equation as the shared starting point
ax.text(5.0,7.55,r"$G_{\mu\nu}\;=\;\dfrac{8\pi G}{c^4}\,T_{\mu\nu}$",
        ha="center",va="center",fontsize=15)
ax.text(2.55,7.55,"geometry\n(the law)",ha="center",va="center",fontsize=7.5,color=C_FW)
ax.text(7.5,7.55,"source\n(the ledger)",ha="center",va="center",fontsize=7.5,color=C_DATA)

# two arrows down to the two roads (straight down; each box names which side it edits)
ax.add_patch(FancyArrowPatch((4.4,6.85),(2.6,5.7),arrowstyle="-|>",mutation_scale=16,
             lw=1.6,color=C_DATA))
ax.add_patch(FancyArrowPatch((5.6,6.85),(7.4,5.7),arrowstyle="-|>",mutation_scale=16,
             lw=1.6,color=C_FW))

# LEFT road: dark matter -- change the source
box(0.2,2.75,4.3,2.85,"#fef2f2",C_DATA)
ax.text(2.35,5.22,"ROAD 1 — Dark matter",ha="center",va="center",
        fontsize=10.5,fontweight="bold",color=C_DATA)
ax.text(2.35,4.62,"a hidden asset",ha="center",va="center",fontsize=8.5,style="italic",color="0.3")
ax.text(2.35,3.95,r"$T_{\mu\nu}=T^{\rm bar}_{\mu\nu}+\mathbf{T^{\rm DM}_{\mu\nu}}$",
        ha="center",va="center",fontsize=12)
ax.text(2.35,3.18,"change the SOURCE,\nkeep the law",ha="center",va="center",
        fontsize=9,fontweight="bold",color=C_DATA)

# RIGHT road: modified dynamics -- change the law
box(5.5,2.75,4.3,2.85,"#f5f3ff",C_FW)
ax.text(7.65,5.22,"ROAD 2 — Modified dynamics",ha="center",va="center",
        fontsize=10.5,fontweight="bold",color=C_FW)
ax.text(7.65,4.62,"a wrong rule",ha="center",va="center",fontsize=8.5,style="italic",color="0.3")
ax.text(7.65,3.95,r"$G_{\mu\nu}\!\to\,?$   or   $F=ma\,\nu(a/a_0)$",
        ha="center",va="center",fontsize=10.5)
ax.text(7.65,3.18,"change the LAW,\nkeep the source",ha="center",va="center",
        fontsize=9,fontweight="bold",color=C_FW)

# the common trigger: below a0
ax.text(5.0,2.15,"the switch that turns the rule on:  gravity below  $a_0\\approx10^{-10}$ m/s$^2$",
        ha="center",va="center",fontsize=8.5,color="0.3")
ax.add_patch(FancyArrowPatch((6.6,2.55),(5.4,2.35),arrowstyle="-|>",mutation_scale=11,
             lw=1.1,color="0.55"))

# bottom strip: the discriminator they disagree on
box(1.6,0.55,6.8,1.05,"#f0fdfa",C_MOND)
ax.text(5.0,1.28,"Discriminator (Fig. 5.1):  does the missing mass track an acceleration scale?",
        ha="center",va="center",fontsize=8.8,fontweight="bold",color=C_MOND)
ax.text(5.0,0.82,"a particle halo has no reason to — a modified law is built around one",
        ha="center",va="center",fontsize=8,color="0.3")

ax.set_title("Two roads from the fork — change the source, or change the law",pad=8)
ax.text(0.99,0.005,"schematic",transform=ax.transAxes,ha="right",va="bottom",
        fontsize=7.5,color="0.6")
fig.tight_layout(); fig.savefig("ch05_two_roads.png", bbox_inches="tight"); print("ok")
