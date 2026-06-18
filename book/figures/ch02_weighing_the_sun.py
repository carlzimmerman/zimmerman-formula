import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))
G=6.674e-11; Msun=1.989e30; AU=1.496e11
names=["Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]
a_AU=np.array([0.387,0.723,1.000,1.524,5.203,9.537,19.19,30.07])
v_obs=np.array([47.4,35.0,29.8,24.1,13.1,9.7,6.8,5.4])  # known mean orbital speeds, km/s
rr=np.linspace(0.3,32,400)*AU
vv=np.sqrt(G*Msun/rr)/1000
ax.plot(rr/AU, vv, color=C_NEWTON, lw=2.2, ls="--",
        label=r"$v=\sqrt{GM_\odot/r}$  (the scale, $M_\odot=1.99\times10^{30}$ kg)")
ax.scatter(a_AU, v_obs, color=C_DATA, s=46, zorder=5, label="measured planet speeds")
for n,x,y in zip(names,a_AU,v_obs):
    off=(6,4) if n not in ("Venus","Saturn") else (6,-12)
    ax.annotate(n,(x,y),textcoords="offset points",xytext=off,fontsize=8,color="#555")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("distance from Sun  (AU)")
ax.set_ylabel("orbital speed  (km/s)")
ax.set_title("Testing the scale: the Sun's gravity reads off every planet's speed")
ax.legend(frameon=False, loc="upper right")
ax.text(0.01,0.02,"curve: framework/Newton formula - points: known orbital speeds",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=7, color="#aaa")
fig.tight_layout(); fig.savefig("ch02_weighing_the_sun.png", bbox_inches="tight"); print("ok")
