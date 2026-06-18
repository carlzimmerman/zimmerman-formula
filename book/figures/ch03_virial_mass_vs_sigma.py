import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

G=6.67e-11; Msun=1.989e30
R=1.5*3.086e22                       # 1.5 Mpc in m
sig_kms=np.linspace(300,1300,400)    # km/s
sig=sig_kms*1.0e3                    # m/s
M=3.0*sig**2*R/G/Msun                # Msun, virial estimate

ax.plot(sig_kms, M, color=C_FW, lw=2.4, label=r"virial $M=3\sigma^2R/G$  ($R=1.5$ Mpc)")

# stellar floor (a few x 1e12 Msun) for reference
Mstars=3.0e12
ax.axhline(Mstars, color=C_DATA, lw=1.6, ls=":",
           label=r"Coma stars $\sim3\times10^{12}\,M_\odot$ (light census)")

# Coma at 1000 km/s, and the 800 km/s interloper-corrected point (Question 3)
for s0,style,lab in [(1000,dict(mfc=C_FW,mec=C_FW),"Coma, $\\sigma=1000$ km/s"),
                     (800,dict(mfc="white",mec=C_FW),"if interlopers $\\Rightarrow$ $\\sigma=800$ km/s")]:
    Ms=3.0*(s0*1e3)**2*R/G/Msun
    ax.plot(s0,Ms,"o",ms=10,mew=2,**style)
    ax.annotate(lab+f"\n$M\\approx{Ms:.1e}".replace("e+","\\times10^{{")+"}}\\,M_\\odot$".replace(" ",""),
                xy=(s0,Ms), xytext=(s0-15, Ms*(2.1 if s0==1000 else 0.34)),
                ha="right", fontsize=8.6, color=C_FW)

ax.set_yscale("log")
ax.set_xlabel(r"velocity dispersion  $\sigma_{\rm los}$  (km/s)")
ax.set_ylabel(r"inferred dynamical mass  ($M_\odot$)")
ax.set_title(r"Mass scales as $\sigma^2$: why $\sigma$ errors are doubled")
ax.set_xlim(300,1300); ax.set_ylim(1e12,5e15)
ax.legend(frameon=False, loc="lower right", fontsize=8.8)
ax.text(0.01,0.02,"a $20\\%$ drop in $\\sigma$ $\\to$ a $36\\%$ drop in $M$, still $\\gg$ stars",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=7.8, color="#888")
fig.tight_layout(); fig.savefig("ch03_virial_mass_vs_sigma.png", bbox_inches="tight"); print("ok")
