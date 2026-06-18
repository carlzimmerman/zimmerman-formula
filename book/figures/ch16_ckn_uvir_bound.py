import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# physical constants (SI, hardcoded published values)
c=2.998e8; G=6.674e-11; hbar=1.055e-34
lP=np.sqrt(G*hbar/c**3)               # Planck length ~1.6e-35 m
H0=70.0*1000.0/3.086e22               # H0=70 km/s/Mpc in s^-1
L_H=c/H0                              # Hubble radius ~1.3e26 m

# CKN collapse ceiling: region of size L cannot hold more than a black hole of size L.
# M_max = L c^2/(2G); rho_E = M_max c^2 / ((4/3) pi L^3) = 3 c^4 / (8 pi G L^2)
def rho_ceiling(L): return 3.0*c**4/(8.0*np.pi*G*L**2)   # J/m^3

# Observed dark-energy density: Lambda = 3 H0^2/c^2, rho_DE(energy) = Lambda c^2/(8 pi G) * c^2
Lam=3.0*H0**2/c**2
rho_DE=Lam*c**2/(8.0*np.pi*G)*c**2     # J/m^3

# Scan L from just above the Planck length up to ~10x the Hubble radius
L=np.logspace(np.log10(lP*10), np.log10(L_H*10), 500)
ax.plot(L, rho_ceiling(L), color=C_FW, lw=2.6,
        label=r"CKN ceiling  $\rho_{\max}=3c^4/8\pi G L^2$")

# Observed dark-energy density (horizontal reference)
ax.axhline(rho_DE, color=C_NEWTON, ls="--", lw=1.8,
           label=r"observed dark-energy density  $\rho_\Lambda$")

# Saturation point at the Hubble radius
ax.scatter([L_H],[rho_ceiling(L_H)], color=C_DATA, zorder=6, s=70,
           label=r"saturation at $L=c/H_0$ (Hubble radius)")
ax.axvline(L_H, color=C_DATA, ls=":", lw=1)
ax.annotate("lands on the\ndark-energy scale", xy=(L_H, rho_ceiling(L_H)),
            xytext=(L_H/3e4, rho_ceiling(L_H)*3e3), color=C_DATA, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.2))

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"size of the region  $L$  (m)  -- IR scale")
ax.set_ylabel(r"max energy density allowed  (J/m$^3$)  -- UV budget")
ax.set_title("CKN UV-IR bound: collapse ceiling vs. region size")
ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.text(0.01,0.02,"the long-distance size L caps the short-distance energy density",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=7.5, color="0.5")
fig.tight_layout(); fig.savefig("ch16_ckn_uvir_bound.png", bbox_inches="tight"); print("ok")
