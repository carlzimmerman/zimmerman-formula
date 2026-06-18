import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# DESI DR2 evolving-dark-energy central values (arXiv:2503.14738)
w0, wa = -0.75, -0.86

def rho_ratio(z):
    a = 1.0/(1.0+z)
    return a**(-3.0*(1.0+w0+wa)) * np.exp(-3.0*wa*(1.0-a))

z = np.linspace(0.0, 3.0, 600)
rho = rho_ratio(z)                  # rho_DE(z)/rho_DE,0
a0r = np.sqrt(rho)                  # a0(z)/a0   propto sqrt(rho_DE)
dV  = (a0r**0.25 - 1.0)*100.0       # % offset in rotation speed at fixed M:  V propto (M a0)^(1/4)

fig, (axT, axB) = plt.subplots(2, 1, figsize=(7.0, 5.6), sharex=True,
                               gridspec_kw={"height_ratios":[1.0, 1.0]})

# --- top: a0(z)/a0 ---
axT.axhline(1.0, color=C_NEWTON, ls="--", lw=1.3, label=r"constant $\Lambda$ (no evolution)")
axT.plot(z, a0r, color=C_FW, lw=2.4, label=r"$a_0(z)/a_0=\sqrt{\rho_{\rm DE}(z)/\rho_{\rm DE,0}}$")
# mark the z~0.4 bump and the z=3 endpoint
zb = 0.405; axT.plot(zb, np.sqrt(rho_ratio(zb)), "o", color=C_DATA, ms=6, zorder=5)
axT.annotate("phantom-divide bump\n"+r"$z\!\approx\!0.4$", xy=(zb, np.sqrt(rho_ratio(zb))),
             xytext=(0.75, 1.085), fontsize=9, color=C_DATA,
             arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.0))
axT.plot(3.0, np.sqrt(rho_ratio(3.0)), "o", color=C_FW, ms=6, zorder=5)
axT.annotate(r"$\approx 0.74$ at $z=3$", xy=(3.0, np.sqrt(rho_ratio(3.0))),
             xytext=(2.05, 0.80), fontsize=9, color=C_FW)
axT.set_ylabel(r"$a_0(z)\,/\,a_0$")
axT.set_ylim(0.70, 1.12)
axT.set_title("The framework's distinctive prediction: $a_0$, and galaxy spin, track dark energy")
axT.legend(frameon=False, fontsize=9, loc="lower left")

# --- bottom: BTFR rotation-speed offset ---
axB.axhline(0.0, color=C_NEWTON, ls="--", lw=1.3, label="local Tully-Fisher line ($z=0$)")
axB.plot(z, dV, color=C_FW, lw=2.4, label=r"$\Delta V/V=(a_0(z)/a_0)^{1/4}-1$")
axB.fill_between(z, dV, 0.0, where=(dV<0), color=C_FW, alpha=0.10)
axB.fill_between(z, dV, 0.0, where=(dV>0), color=C_DATA, alpha=0.10)
axB.plot(3.0, dV[-1], "o", color=C_FW, ms=6, zorder=5)
axB.annotate(r"$\approx -7\%$ (spin SLOW) at $z=3$", xy=(3.0, dV[-1]),
             xytext=(1.30, -5.8), fontsize=9, color=C_FW,
             arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.0))
axB.text(0.45, 2.0, "early bump:\ngalaxies a touch FAST", fontsize=8.5, color=C_DATA, ha="center")
axB.set_xlabel("redshift  $z$  (look-back into the early universe $\\rightarrow$)")
axB.set_ylabel(r"BTFR offset $\Delta V/V$  (%)")
axB.set_ylim(-9, 4)
axB.set_xlim(0, 3)
axB.legend(frameon=False, fontsize=9, loc="lower left")

axB.text(0.99, 0.04, "framework-computed; DESI DR2 (w0=-0.75, wa=-0.86)",
         transform=axB.transAxes, ha="right", va="bottom", fontsize=7.5, color="#94a3b8")

fig.tight_layout()
fig.savefig("ch26_a0z_btfr_offset.png", bbox_inches="tight")
print("ok")
