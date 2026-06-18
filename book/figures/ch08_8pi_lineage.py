import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":False,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, ax = plt.subplots(figsize=(7.6,4.6))
ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis("off")

def box(x,y,w,h,text,fc,ec,fs=11,tc="#111"):
    b=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.06,rounding_size=0.12",
                     fc=fc,ec=ec,lw=1.8)
    ax.add_patch(b)
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc)

def arrow(x1,y1,x2,y2,txt=None,col="#333"):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=16,
                      lw=1.8,color=col,shrinkA=4,shrinkB=4)
    ax.add_patch(a)
    if txt:
        ax.text((x1+x2)/2,(y1+y2)/2+0.28,txt,ha="center",va="center",
                fontsize=8.5,color=col,style="italic")

# Top: the source 8pi in the Einstein coupling
box(5,6.1,6.2,1.0,r"Einstein coupling:  $\dfrac{8\pi G}{c^4}\,T_{\mu\nu}$",
    "#ede9fe",C_FW,fs=12)
ax.text(5,5.45,"the 8π lives here, in GR's home",ha="center",fontsize=8.5,color=C_FW)

# Left branch: Newtonian limit -> 4pi (factor of two shed)
box(2.4,3.3,3.6,1.05,r"Newtonian limit:"+"\n"+r"$\nabla^2\Phi = 4\pi G\,\rho$",
    "#f1f5f9",C_NEWTON,fs=11)
arrow(3.9,5.55,2.9,3.95,"weak field +\nslow motion\n(÷2: pressure &\nspace-curvature)",col=C_NEWTON)
ax.text(2.4,2.55,"8π → 4π  (the 8 is the 4, doubled by relativity)",
        ha="center",fontsize=8.5,color=C_NEWTON)

# Right branch: combine with the 3 from Friedmann -> kernel sqrt(8pi/3)
box(7.6,3.3,3.6,1.05,r"framework kernel:"+"\n"+r"$\sqrt{\,8\pi/3\,}\approx 2.894$",
    "#ede9fe",C_FW,fs=11)
arrow(6.1,5.55,7.1,3.95,"same 8π, combined\nwith the 3 from the\nexpansion equations\n(Ch. 9, 22)",col=C_FW)
ax.text(7.6,2.55,"FORM is forced (reuses Einstein's 8π)",
        ha="center",fontsize=8.5,color=C_FW)

# Honesty caveat box at bottom
box(5,1.05,8.8,1.1,
    "Honest caveat: a shared 8π is a structural fact about the kernel's FORM.\n"
    "It is NOT by itself a derivation of the framework's actual numbers (a₀, Λ, Z).",
    "#fff7ed",C_DATA,fs=9.5,tc="#7c2d12")

ax.set_title("Following the 8π: from GR's coupling to Newton's 4π — and into the kernel",
             fontsize=12)
fig.tight_layout(); fig.savefig("ch08_8pi_lineage.png", bbox_inches="tight"); print("ok")
