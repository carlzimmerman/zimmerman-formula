import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# The chapter's "cleanest empirical discriminator": does the missing mass track
# an acceleration scale? We plot the radial-acceleration plane g_obs vs g_bar.
a0 = 9.36e-11  # framework value (m/s^2); the MOND value 1.2e-10 sits essentially on top here

# x-axis: baryonic (visible-matter, Newtonian) acceleration
gbar = np.logspace(-13, -8, 400)

# Newtonian baseline: g_obs = g_bar (no missing mass) -- the "books balance" line
g_newton = gbar

# Modified-dynamics prediction: a SINGLE universal curve pinned to a0.
# Use the framework's own de Sitter-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0).
g_md = np.sqrt(gbar**2 + gbar*a0)

fig, ax = plt.subplots(figsize=(7,4.6))

# Newtonian "no discrepancy" reference
ax.plot(gbar, g_newton, color=C_NEWTON, ls="--", lw=2,
        label="Newton: $g_{\\rm obs}=g_{\\rm bar}$ (books balance)")

# The single universal modified-dynamics relation
ax.plot(gbar, g_md, color=C_FW, lw=2.6,
        label="Modified dynamics: one universal curve, pinned to $a_0$")

# Illustrative, model-generated "particle-halo scatter": a halo has no reason to
# respect an acceleration scale, so the discrepancy at a given g_bar varies galaxy
# to galaxy. We draw model points = the universal curve TIMES random per-galaxy
# boosts that grow in the weak field (no a0 structure) -> visible vertical scatter.
rng = np.random.default_rng(7)
gb_pts = 10**rng.uniform(-12.3, -8.5, 320)
g_md_pts = np.sqrt(gb_pts**2 + gb_pts*a0)
# per-point multiplicative scatter that widens toward weak gravity (halo idiosyncrasy)
weak = np.clip(np.log10(a0/gb_pts), 0, None)        # 0 in strong field, grows when gbar<<a0
sigma = 0.05 + 0.11*weak                              # dex of scatter, history-driven
g_halo_pts = g_md_pts * 10**(rng.normal(0, 1, gb_pts.size)*sigma)
ax.scatter(gb_pts, g_halo_pts, s=10, color=C_DATA, alpha=0.35, edgecolors="none",
           label="Uncorrelated particle halos: scatter (illustrative, model-generated)")

# mark a0 on the x-axis
ax.axvline(a0, color="0.4", lw=1, ls=":")
ax.text(a0*1.15, 3e-13, "$g_{\\rm bar}=a_0$", rotation=90, va="bottom", ha="left",
        fontsize=9, color="0.35")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e-13, 1e-8); ax.set_ylim(1e-13, 3e-8)
ax.set_xlabel("$g_{\\rm bar}$  —  acceleration from visible matter alone  (m/s$^2$)")
ax.set_ylabel("$g_{\\rm obs}$  —  acceleration actually needed  (m/s$^2$)")
ax.set_title("The discriminator: does the missing mass track an acceleration scale?")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.text(0.99, 0.02, "curves: framework eqs;  points: model-generated illustration",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="0.55")
fig.tight_layout(); fig.savefig("ch05_discriminator_rar.png", bbox_inches="tight"); print("ok")
