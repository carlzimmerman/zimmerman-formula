import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

a0 = 9.36e-11
G  = 6.674e-11
Msun = 1.989e30
kpc = 3.086e19

# Schematic disk galaxy: smooth rising enclosed-mass profile (numpy-only).
# M(<r) = Mtot * [1 - (1 + r/rd) exp(-r/rd)]
Mtot = 6e10*Msun
rd   = 3.0*kpc
r = np.linspace(0.3, 30, 600)*kpc
Menc = Mtot*(1.0 - (1.0 + r/rd)*np.exp(-r/rd))

gN = G*Menc/r**2
g_obs = np.sqrt(gN**2 + gN*a0)
v_newton = np.sqrt(gN*r)/1e3
v_obs    = np.sqrt(g_obs*r)/1e3

fig, (axL, axR) = plt.subplots(1,2, figsize=(10.2,4.5),
                               gridspec_kw={"width_ratios":[1.15,1.0]})

rk = r/kpc
axL.plot(rk, v_newton, color=C_NEWTON, ls="--", lw=2.2,
         label="Newton (baryons only): falls off")
axL.plot(rk, v_obs, color=C_FW, lw=2.8,
         label="both roads: same flat curve")
axL.fill_between(rk, v_newton, v_obs, color=C_DATA, alpha=0.10)
axL.annotate("the 'missing' speed", xy=(22,(v_newton[-100]+v_obs[-100])/2),
             xytext=(13, 60), fontsize=8.6, color="#7a0e0e",
             arrowprops=dict(arrowstyle="->", color="#b03030", lw=1))
axL.set_xlabel("radius  $r$  (kpc)")
axL.set_ylabel("orbital speed  $v$  (km/s)")
axL.set_title("Same observed rotation curve...")
axL.legend(frameon=False, fontsize=8.7, loc="lower right")
axL.set_ylim(0, max(v_obs)*1.18)
axL.text(0.02,0.02,"schematic disk galaxy (smooth $6\\times10^{10}\\,M_\\odot$ profile)",
         transform=axL.transAxes, fontsize=7.2, color="0.55")

axR.axis("off"); axR.set_xlim(0,1); axR.set_ylim(0,1)
axR.set_title("...two different equations to change")
axR.text(0.5,0.95,"galaxies move too fast - change ONE side:",ha="center",
         fontsize=9.5, color="0.2", weight="bold")
axR.add_patch(plt.Rectangle((0.04,0.55),0.92,0.26, fill=True,
              facecolor=C_MOND, alpha=0.12, edgecolor=C_MOND, lw=1.6))
axR.text(0.5,0.755,"MODIFIED GRAVITY",ha="center",fontsize=9.5,color=C_MOND,weight="bold")
axR.text(0.5,0.675, r"change the pull:  $F=\dfrac{GMm}{r^2}\;\to\;$ stronger when weak",
         ha="center", fontsize=8.6, color="0.2")
axR.text(0.5,0.59,"(MOND, AeST) - feels Solar-System tests",
         ha="center", fontsize=7.7, color="0.45")
axR.add_patch(plt.Rectangle((0.04,0.17),0.92,0.27, fill=True,
              facecolor=C_FW, alpha=0.12, edgecolor=C_FW, lw=1.8))
axR.text(0.5,0.385,"MODIFIED INERTIA   (this book)",ha="center",fontsize=9.5,
         color=C_FW,weight="bold")
axR.text(0.5,0.305, r"change the resistance:  $F=m\,a\;\to\;m_{\rm eff}\,a$  when $a<a_0$",
         ha="center", fontsize=8.6, color="0.2")
axR.text(0.5,0.215,"gravity untouched; switches off at high $a$,\nso the Solar System stays safe",
         ha="center", fontsize=7.7, color="0.45")
axR.annotate("", xy=(0.22,0.81), xytext=(0.30,0.90),
             arrowprops=dict(arrowstyle="->", color=C_MOND, lw=1.6))
axR.annotate("", xy=(0.78,0.44), xytext=(0.70,0.90),
             arrowprops=dict(arrowstyle="->", color=C_FW, lw=2.0))
axR.text(0.5,0.05,"both fit the curve on the left;\nthey differ in the Solar System.",
         ha="center", fontsize=8.2, color="0.3", style="italic")

fig.tight_layout(); fig.savefig("ch13_mi_vs_mg_fork.png", bbox_inches="tight"); print("ok")
