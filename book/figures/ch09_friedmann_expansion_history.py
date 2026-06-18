import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

fig, ax = plt.subplots(figsize=(7,4.3))

# The Friedmann 'engine' of the chapter:
#   (H(a)/H0)^2 = Om_r a^-4 + Om_m a^-3 + Om_k a^-2 + Om_Lambda
# with the flat LCDM inventory quoted in the chapter.
Om_r = 9.0e-5
Om_m = 0.31
Om_L = 0.69
Om_k = 1.0 - (Om_r + Om_m + Om_L)  # ~0, flat by construction

# scale factor from just after the Big Bang to several e-folds into the future
a = np.logspace(-4, 1.0, 1400)

def E2(a, om_r, om_m, om_k, om_L):
    return om_r*a**-4 + om_m*a**-3 + om_k*a**-2 + om_L

# Total expansion rate (normalized to H0)
Etot = np.sqrt(E2(a, Om_r, Om_m, Om_k, Om_L))

# The two dominant single-component pieces, drawn to show the crossover the
# chapter's last 'Questions' problem asks about: matter (a^-3) vs Lambda (const).
matter_term = np.sqrt(Om_m*a**-3)
lambda_term = np.sqrt(Om_L)*np.ones_like(a)

ax.loglog(a, Etot, color=C_FW, lw=2.6, label=r"$H(a)/H_0$  (total, flat $\Lambda$CDM)")
ax.loglog(a, matter_term, color=C_NEWTON, ls="--", lw=1.8,
          label=r"matter only  $\propto a^{-3/2}$")
ax.loglog(a, lambda_term, color=C_DATA, ls=":", lw=2.0,
          label=r"dark energy only  (constant)")

# matter / dark-energy equality: Om_m a^-3 = Om_L  ->  a_eq = (Om_m/Om_L)^(1/3)
a_eq = (Om_m/Om_L)**(1.0/3.0)
ax.axvline(a_eq, color=C_MOND, lw=1.4, alpha=0.8)
z_eq = 1.0/a_eq - 1.0
ax.annotate(r"matter = dark energy" + "\n" + rf"$a\approx{a_eq:.2f}$  ($z\approx{z_eq:.2f}$)",
            xy=(a_eq, np.sqrt(2*Om_L)), xytext=(a_eq*1.25, 9),
            color=C_MOND, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=C_MOND, lw=1.2))

# mark 'today'
ax.axvline(1.0, color="k", lw=1.0, alpha=0.5)
ax.annotate("today\n$a=1$", xy=(1.0, 1.0), xytext=(1.35, 1.7),
            fontsize=9, color="k",
            arrowprops=dict(arrowstyle="->", color="k", lw=1.0, alpha=0.7))
ax.scatter([1.0],[1.0], color="k", zorder=5, s=28)

ax.set_xlabel(r"scale factor  $a$   (Big Bang $\to$ left,  future $\to$ right)")
ax.set_ylabel(r"expansion rate  $H(a)/H_0$")
ax.set_title("The Friedmann engine: expansion rate vs. cosmic size")
ax.set_xlim(1e-4, 1e1)
ax.set_ylim(0.5, 2e6)
ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.text(0.012, 0.62, "flat $\\Lambda$CDM: $\\Omega_r{=}9\\!\\times\\!10^{-5},\\ \\Omega_m{=}0.31,\\ \\Omega_\\Lambda{=}0.69$",
        transform=ax.transAxes, fontsize=7.5, color="#666666")

fig.tight_layout(); fig.savefig("ch09_friedmann_expansion_history.png", bbox_inches="tight"); print("ok")
