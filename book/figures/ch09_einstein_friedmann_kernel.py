import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Schematic 'genealogy' diagram: where the 8pi and the 3 come from, and how
# they marry into the sqrt(8pi/3) kernel the chapter promises to pick up later.
fig, ax = plt.subplots(figsize=(7,4.3))
ax.set_axis_off()
ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.grid(False)

def box(x,y,w,h,text,fc,ec,fs=10,tc="k"):
    from matplotlib.patches import FancyBboxPatch
    p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.08,rounding_size=0.18",
                     fc=fc,ec=ec,lw=1.8,mutation_scale=8)
    ax.add_patch(p)
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc,zorder=5)

def arrow(x1,y1,x2,y2,col="#444444"):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),
                arrowprops=dict(arrowstyle="-|>",color=col,lw=2.0))

# Two parents
box(2.6,8.4,4.0,1.5,"EINSTEIN's $8\\pi$\n(Ch. 8 field equations:\nmatching GR to Newton)",
    "#ede9fe",C_FW,fs=9.5)
box(7.4,8.4,4.0,1.5,"FRIEDMANN's $3$\n(this chapter: volume of a\n3-D ball, $\\frac{4}{3}\\pi r^3$)",
    "#cffafe",C_MOND,fs=9.5)

# Middle: the Friedmann coefficient
box(5.0,5.6,4.6,1.4,"Friedmann coefficient\n$H^2=\\frac{8\\pi G}{3}\\,\\rho+\\dots$",
    "white","#444444",fs=11)

arrow(2.9,7.65,4.3,6.3)
arrow(7.1,7.65,5.7,6.3)

# Note the flip -> critical density
box(8.6,5.6,2.6,1.2,"flip it:\n$\\rho_{\\rm crit}=\\frac{3H_0^2}{8\\pi G}$",
    "#fef2f2",C_DATA,fs=9)
arrow(7.3,5.6,7.3,5.6)  # tiny; replaced below
ax.annotate("",xy=(7.3,5.6),xytext=(7.3,5.6))
ax.annotate("",xy=(7.3,5.6),xytext=(7.3,5.6))
ax.annotate("",xy=(7.35,5.6),xytext=(7.3,5.6))
ax.annotate("",xy=(7.4,5.6),xytext=(7.3,5.6))
# clean connector for the flip
ax.annotate("",xy=(7.3,5.6),xytext=(7.3,5.6))
arrow(7.3,5.6,7.3,5.6)
ax.plot([7.3,7.3],[5.6,5.6])
ax.annotate("",xy=(7.3,5.6),xytext=(7.3,5.6))
# (use a single visible connector)
arrow(7.3,5.6,7.25,5.6)

# Bottom: the kernel the book promises
box(5.0,2.6,5.2,1.6,"the Einstein-Friedmann kernel\n$\\sqrt{\\frac{8\\pi}{3}}$\n(picked up in Ch. 22 / Ch. 23)",
    "#ede9fe",C_FW,fs=11,tc="#4c1d95")
arrow(5.0,4.9,5.0,3.4)

# honesty footnote
ax.text(5.0,0.7,"FORCED in form by standard GR + cosmology.  The value of $a_0$ is NOT thereby derived;\n"
                "the lone free knob is $\\kappa=\\frac{1}{2}$ (Ch. 23).",
        ha="center",va="center",fontsize=8,color="#666666",style="italic")

ax.set_title("Where the two numbers come from — and where they marry",fontsize=12)
fig.tight_layout(); fig.savefig("ch09_einstein_friedmann_kernel.png", bbox_inches="tight"); print("ok")
