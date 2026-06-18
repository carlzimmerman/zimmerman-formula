import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# x = a/a0; plot the interpolation function mu(x) that joins the two regimes.
x = np.logspace(-2.0, 2.0, 500)
mu_simple   = x / (1 + x)              # 'simple' form
mu_standard = x / np.sqrt(1 + x**2)    # 'standard' form
# The framework's g_obs = sqrt(gN^2 + gN a0) implies an effective mu via x = mu(y) y, y=a/a0.
# Parametrically: write nu(gN/a0) then invert. Easiest: a/a0 from g_obs as function of gN, then mu=gN/a.
gN = np.logspace(-3.5, 2.5, 4000)      # in units of a0
a  = np.sqrt(gN**2 + gN)               # a/a0  (since g_obs and a coincide on circular orbits)
mu_fw = gN / a                          # mu = g_N / a, as a function of x=a/a0=a
# resample mu_fw onto the same x grid
mu_fw_x = np.interp(x, a, mu_fw)

ax.plot(x, mu_simple,   color=C_MOND, lw=2.2, label=r"'simple'  $\mu=\dfrac{x}{1+x}$")
ax.plot(x, mu_standard, color=C_NEWTON, ls="--", lw=2.0, label=r"'standard'  $\mu=\dfrac{x}{\sqrt{1+x^2}}$")
ax.plot(x, mu_fw_x, color=C_FW, lw=2.6, label=r"framework  $g_{\rm obs}=\sqrt{g_N^2+g_N a_0}$")

# The two FIXED limits the data pin down
ax.plot(x[x<0.2], x[x<0.2], color=C_DATA, ls=":", lw=1.6)
ax.axhline(1.0, color=C_DATA, ls=":", lw=1.6)
ax.text(2.2e-2, 4.5e-2, r"$\mu\to x$  (deep-MOND, fixed)", color=C_DATA, fontsize=8.5, rotation=30)
ax.text(8, 1.04, r"$\mu\to 1$  (Newtonian, fixed)", color=C_DATA, fontsize=8.5, ha="right")
ax.axvspan(0.3, 3.0, color="#fde68a", alpha=0.25)
ax.text(1.0, 0.16, "shape here\nis FREE", ha="center", fontsize=8.5, color="#b45309")

ax.set_xscale("log")
ax.set_xlim(1e-2, 1e2)
ax.set_ylim(0, 1.15)
ax.set_xlabel(r"$x = a/a_0$   (acceleration in units of the scale $a_0$)")
ax.set_ylabel(r"interpolation function  $\mu(x)$")
ax.set_title("Fixed limits, free middle: the interpolation functions of MOND")
ax.legend(frameon=False, fontsize=9, loc="lower right")
ax.text(0.01, 0.02, "framework-computed", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=7, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch17_interpolation_functions.png", bbox_inches="tight"); print("ok")
