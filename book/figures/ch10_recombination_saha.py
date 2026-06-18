import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# FRAMEWORK-INDEPENDENT but fully COMPUTED from the Saha equation the chapter quotes.
# Free-electron fraction x_e(T) for a hydrogen plasma:
#   x_e^2/(1-x_e) = (1/n_b) (m_e kB T / 2 pi hbar^2)^(3/2) exp(-B / kB T)
# with baryon density n_b = eta * n_gamma, n_gamma = 0.2436 (kB T/ hbar c)^3.
kB=1.380649e-23; me=9.1093837e-31; hbar=1.054571817e-34
c=2.99792458e8; B=13.605693*1.602176634e-19; eta=6.1e-10; Tcmb0=2.725

z   = np.linspace(800, 1700, 1500)
T   = Tcmb0*(1+z)
ng  = 0.2436*(kB*T/(hbar*c))**3
nb  = eta*ng
rhs = (1.0/nb)*(me*kB*T/(2*np.pi*hbar**2))**1.5*np.exp(-B/(kB*T))
rhs = np.clip(rhs, 0, 1e30)
xe  = (-rhs + np.sqrt(rhs**2 + 4*rhs))/2.0     # physical root of x^2/(1-x)=rhs
xe  = np.clip(xe, 0, 1)

fig, ax = plt.subplots(figsize=(7.2,4.3))
ax.plot(z, xe, color=C_FW, lw=2.6, label="Saha free-electron fraction $x_e$")

# Saha gives a slightly hot midpoint; the full (Peebles) non-equilibrium treatment,
# which the chapter quotes as the careful answer, refines this to z~1100, T~3000 K.
ix = np.argmin(np.abs(xe-0.5))
ax.axvline(z[ix], color=C_DATA, ls="--", lw=1.4)
ax.annotate("Saha half-ionized\n(full treatment refines\nto z~1100, T~3000 K)",
            xy=(z[ix], 0.5), xytext=(z[ix]+95, 0.66),
            fontsize=8.5, color=C_DATA,
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1))

# opaque / transparent shading
ax.axvspan(z[ix], z.max(), color=C_NEWTON, alpha=0.08)
ax.axvspan(z.min(), z[ix], color=C_MOND,   alpha=0.06)
ax.text(z.max()-40, 0.40, "OPAQUE plasma\n(light trapped, scatters\noff free electrons)",
        ha="left", va="top", fontsize=8.5, color=C_NEWTON)
ax.text(z.min()+30, 0.55, "TRANSPARENT\nneutral atoms\n(the fog lifts -> CMB\nstreams free)",
        ha="left", va="top", fontsize=8.5, color="#0e7490")

ax.set_xlabel("redshift  z   (earlier / hotter  <--      -->  later / cooler)")
ax.set_ylabel("free-electron fraction  $x_e$")
ax.set_title("Recombination: the fog lifts when electrons bind to nuclei")
ax.set_xlim(z.max(), z.min())     # hotter on the left
ax.set_ylim(-0.02, 1.02)

# top axis in temperature
secax = ax.secondary_xaxis('top',
        functions=(lambda zz: Tcmb0*(1+zz), lambda TT: TT/Tcmb0 - 1))
secax.set_xlabel("temperature  T  (K)", fontsize=9)
secax.set_xticks([4500,4000,3500,3000,2500])

ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 0.04))
ax.text(0.99, 0.93, "computed from the Saha equation (Ch. 10 Deeper Dive)",
        transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch10_recombination_saha.png", bbox_inches="tight"); print("ok")
