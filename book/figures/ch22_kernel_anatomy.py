import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Figure 22.2 -- anatomy of the kernel: forced parts (Einstein's 8pi / Friedmann's 3, square-rooted)
# vs the one POSITED factor kappa = 1/2. Numbers computed from the stated constants.
Z = np.sqrt(32*np.pi/3)          # = 5.789
sqrt_8pi3 = np.sqrt(8*np.pi/3)   # = 2.894
ratio_8pi3 = 8*np.pi/3           # = 8.378

fig, ax = plt.subplots(figsize=(7.6,4.5))
ax.set_axis_off()

def box(x,y,w,h,text,fc,ec,fs=10,fw="normal",tc="black"):
    ax.add_patch(plt.Rectangle((x-w/2,y-h/2),w,h, fc=fc, ec=ec, lw=1.6,
                               transform=ax.transAxes, zorder=3))
    ax.text(x,y,text, ha="center", va="center", fontsize=fs, fontweight=fw,
            color=tc, transform=ax.transAxes, zorder=4)

ax.text(0.5,0.97,"Anatomy of the kernel  $Z=\\sqrt{32\\pi/3}$  in  $a_0=cH_\\Lambda/Z$",
        ha="center", va="top", fontsize=12, fontweight="bold", transform=ax.transAxes)

box(0.22,0.72,0.30,0.16, "Einstein's $8\\pi$\nfield eqns $G_{\\mu\\nu}=\\frac{8\\pi G}{c^4}T_{\\mu\\nu}$\nforced by Newtonian limit",
    "#ede9fe", C_FW, fs=8.5)
box(0.62,0.72,0.30,0.16, "Friedmann's $3$\n$H^2=\\frac{8\\pi G}{3}\\rho$\nforced by 3-D expansion",
    "#ede9fe", C_FW, fs=8.5)

box(0.42,0.49,0.30,0.13, "ratio  $\\frac{8\\pi}{3}\\approx %.3f$" % ratio_8pi3,
    "#ddd6fe", C_FW, fs=11, fw="bold")
ax.annotate("",xy=(0.36,0.555),xytext=(0.22,0.64),
            arrowprops=dict(arrowstyle="-|>",color=C_FW,lw=1.8),transform=ax.transAxes)
ax.annotate("",xy=(0.50,0.555),xytext=(0.62,0.64),
            arrowprops=dict(arrowstyle="-|>",color=C_FW,lw=1.8),transform=ax.transAxes)

box(0.42,0.30,0.34,0.12, "square-rooted by the dynamics\n$\\sqrt{8\\pi/3}\\approx %.3f$" % sqrt_8pi3,
    "#ddd6fe", C_FW, fs=9.5, fw="bold")
ax.annotate("",xy=(0.42,0.365),xytext=(0.42,0.425),
            arrowprops=dict(arrowstyle="-|>",color=C_FW,lw=1.8),transform=ax.transAxes)

box(0.83,0.40,0.26,0.20, "$\\times\\,2$  from  $\\kappa=\\frac{1}{2}$\n\nthe ONE posited\nfactor (Ch. 23)\nNOT forced",
    "#fee2e2", C_DATA, fs=9, tc=C_DATA)
ax.annotate("",xy=(0.70,0.30),xytext=(0.74,0.40),
            arrowprops=dict(arrowstyle="-|>",color=C_DATA,lw=1.8,ls=(0,(3,2))),transform=ax.transAxes)

box(0.42,0.12,0.40,0.11, "$Z=2\\sqrt{8\\pi/3}=\\sqrt{32\\pi/3}\\approx %.3f$" % Z,
    C_FW, C_FW, fs=11, fw="bold", tc="white")
ax.annotate("",xy=(0.42,0.175),xytext=(0.42,0.245),
            arrowprops=dict(arrowstyle="-|>",color=C_FW,lw=1.8),transform=ax.transAxes)

ax.text(0.04,0.40,"FORCED\n(consequence)", color=C_FW, fontsize=9, fontweight="bold",
        rotation=90, ha="center", va="center", transform=ax.transAxes)
ax.text(0.99,0.01,"framework-computed / schematic (Ch. 22)", ha="right", va="bottom",
        fontsize=7, color=C_NEWTON, alpha=0.6, transform=ax.transAxes)
fig.tight_layout(); fig.savefig("ch22_kernel_anatomy.png", bbox_inches="tight"); print("ok")
