import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# Mass discrepancy M_dyn/M_bar vs radius for a Milky-Way-like model.
# M_dyn = v_flat^2 r / G (flat curve). M_bar from exponential disk that saturates.
G=6.674e-11; kpc=3.086e19; Msun=1.99e30
Rd=3.0
Mdisk=6e10*Msun
v_flat=200e3
r=np.linspace(1.0,40,400)
x=r/Rd
Mbar=Mdisk*(1.0-(1.0+x)*np.exp(-x))     # enclosed baryonic mass (kg)
Mdyn=v_flat**2*(r*kpc)/G                 # mass the motion demands (kg)
ratio=Mdyn/Mbar

ax.plot(r, ratio, color=C_FW, lw=2.6, label="$M_{\\rm dyn}/M_{\\rm bar}$  (demanded / seen)")
ax.axhline(1.0, color=C_NEWTON, lw=1.6, ls="--", label="ratio = 1  (no discrepancy)")

# mark the worked-example point: r=20 kpc -> ~3
i20=np.argmin(abs(r-20))
ax.plot([20],[ratio[i20]],"o",color=C_DATA,ms=8,zorder=5)
ax.annotate(f"worked example:\n$r=20$ kpc, ratio $\\approx${ratio[i20]:.1f}",
            xy=(20,ratio[i20]), xytext=(8,7.5),
            arrowprops=dict(arrowstyle="->",color=C_DATA,lw=1.3),color=C_DATA,fontsize=9.5)

ax.fill_between(r, 1.0, ratio, color=C_FW, alpha=0.07)
ax.annotate("bright center:\nseen ≈ demanded", xy=(2.5,1.25), xytext=(2.5,4.0),
            arrowprops=dict(arrowstyle="->",color="#555",lw=1.1),color="#555",fontsize=9)
ax.annotate("faint outskirts:\ngrip far exceeds the light", xy=(36,ratio[np.argmin(abs(r-36))]),
            xytext=(20,11.5),arrowprops=dict(arrowstyle="->",color=C_FW,lw=1.2),color=C_FW,fontsize=9.5)

ax.set_xlim(0,40); ax.set_ylim(0,14)
ax.set_xlabel("distance from galaxy center  $r$  (kiloparsecs)")
ax.set_ylabel("mass discrepancy  $M_{\\rm dyn}/M_{\\rm bar}$")
ax.set_title("Putting a number on the problem: the mass discrepancy")
ax.legend(frameon=False, loc="upper left", fontsize=9.5)
ax.text(0.012,0.02,"model: flat-curve $M_{\\rm dyn}$ vs exponential-disk baryons (Milky-Way-like)",
        transform=ax.transAxes, fontsize=7, color="#888")
fig.tight_layout(); fig.savefig("ch01_mass_discrepancy.png", bbox_inches="tight"); print("ok")
