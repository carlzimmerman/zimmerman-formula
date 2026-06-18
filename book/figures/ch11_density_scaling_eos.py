import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Fig 11.2 -- how the cosmic ingredients dilute: rho propto a^{-3(1+w)}.
# Computed directly from the chapter's equation-of-state scaling law for
# matter (w=0), radiation (w=+1/3), and a cosmological constant (w=-1).
# All three normalized to equal density today (a=1).
a = np.logspace(-3, 1.0, 500)     # scale factor; a=1 is today
def rho(w): return a**(-3.0*(1.0+w))

fig, ax = plt.subplots(figsize=(7,4.3))
ax.loglog(a, rho(1/3.), color=C_DATA, ls="-.", lw=2, label=r"radiation  $w=+1/3$,  $\rho\propto a^{-4}$")
ax.loglog(a, rho(0.0), color=C_NEWTON, ls="--", lw=2, label=r"matter  $w=0$,  $\rho\propto a^{-3}$")
ax.loglog(a, rho(-1.0), color=C_FW, lw=2.6, label=r"dark energy ($\Lambda$)  $w=-1$,  $\rho=$ const")

ax.axvline(1.0, color="#cbd5e1", lw=1)
ax.text(1.0, 1e-9, " today", rotation=90, va="bottom", ha="left", fontsize=8, color="#64748b")

ax.set_xlabel("scale factor  a   (size of the universe; a=1 today)")
ax.set_ylabel(r"energy density  $\rho/\rho_0$   (relative to today)")
ax.set_title(r"Why $\rho_{\rm DE}$ wins: matter dilutes, the vacuum does not")
ax.set_ylim(1e-10, 1e10)
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.text(0.01,0.01,r"$\rho\propto a^{-3(1+w)}$ -- chapter equation-of-state law",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=7, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch11_density_scaling_eos.png", bbox_inches="tight"); print("ok")
