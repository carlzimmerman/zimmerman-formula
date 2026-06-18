import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# The framework: a0(z)/a0 = sqrt(rho_DE(z)/rho_DE0).
# Two dark-energy scenarios for rho_DE(z):
#  (A) DESI DR2 evolving DE, CPL w0=-0.75, wa=-0.86  -> the distinctive bump+decline
#  (B) a pure cosmological constant w=-1            -> a0(z) goes FLAT (the "hostage")
w0, wa = -0.75, -0.86
def rho_de_ratio_cpl(z):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

z = np.linspace(0, 3.2, 400)
a0_evolving = np.sqrt(rho_de_ratio_cpl(z))   # framework under evolving DE
a0_const = np.ones_like(z)                    # framework under a true Lambda

fig, ax = plt.subplots(figsize=(7,4.3))

ax.plot(z, a0_evolving, color=C_FW, lw=2.4,
        label="framework, DESI evolving DE ($w_0,w_a$)")
ax.plot(z, a0_const, color=C_NEWTON, lw=2.0, ls="--",
        label="framework if DE is a true constant (flat)")

# the +6% bump near z~0.4 and the -26% point at z=3
zp = z[np.argmax(a0_evolving)]
ax.scatter([zp],[a0_evolving.max()], color=C_FW, zorder=5, s=30)
ax.annotate(f"+6% bump near $z\\approx0.4$\n(phantom-divide crossing)",
            xy=(zp, a0_evolving.max()), xytext=(0.75, 1.105),
            fontsize=8.6, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.0))
ax.scatter([3.0],[np.sqrt(rho_de_ratio_cpl(3.0))], color=C_FW, zorder=5, s=30)
ax.annotate("$\\approx0.74$ of today's $a_0$\n($-26\\%$) by $z=3$",
            xy=(3.0, np.sqrt(rho_de_ratio_cpl(3.0))), xytext=(1.9, 0.80),
            fontsize=8.6, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.0))

# shade the testable high-z window (ELT/JWST/ALMA, ~2028+) as illustrative
ax.axvspan(2.0, 3.2, color=C_DATA, alpha=0.06)
ax.text(2.6, 0.705, "high-$z$ test window\n(ELT/JWST/ALMA, ~2028+)",
        ha="center", va="center", fontsize=7.8, color=C_DATA)

ax.axhline(1.0, color="#bbb", lw=0.8, zorder=0)
ax.set_xlabel("redshift  $z$  (look-back / cosmic time $\\rightarrow$)")
ax.set_ylabel("$a_0(z)\\,/\\,a_0$  (today $=1$)")
ax.set_ylim(0.66, 1.14)
ax.set_xlim(0, 3.2)
ax.set_title("The DESI hostage: the sharp prediction exists only if dark energy evolves")
ax.legend(frameon=False, fontsize=8.8, loc="lower left")
ax.text(0.985,0.965,"framework: $a_0(z)\\propto\\sqrt{\\rho_{DE}(z)}$",
        transform=ax.transAxes, ha="right", va="top", fontsize=7.8, color="#888")
fig.tight_layout(); fig.savefig("ch31_a0z_hostage.png", bbox_inches="tight"); print("ok")
