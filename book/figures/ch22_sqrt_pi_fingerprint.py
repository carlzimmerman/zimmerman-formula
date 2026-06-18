import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Figure 22.3 -- the sqrt(pi) fingerprint. Two routes to the SAME form c^2 sqrt(Lambda) leave
# DIFFERENT powers of pi: thermal (2pi's cancel) -> pi^0; gravitational-density (square-roots
# Einstein's 8pi) -> pi^(1/2). Only the density route lands on the framework/galaxy value.
c=2.998e8; G=6.674e-11; Lam=1.09e-52
rho_DE = Lam*c**2/(8*np.pi*G)
a0_density = 0.5*c*np.sqrt(G*rho_DE)          # = c^2 sqrt(Lam/32pi), carries pi^(1/2), kappa=1/2
a0_thermal = c*c*np.sqrt(Lam/3.0)             # = c H_Lambda, carries pi^0 (the 2pi's cancel)
a0_milgrom = 1.2e-10

fig, ax = plt.subplots(figsize=(7.4,4.6))

vals  = [a0_thermal, a0_density]
labs  = ["Thermal route\n$a_0\\sim c^2\\sqrt{\\Lambda/3}$\n(de Sitter $=$ Unruh, $2\\pi$'s cancel)",
         "Gravitational-density route\n$a_0=\\frac{c}{2}\\sqrt{G\\rho_{\\rm DE}}=c^2\\sqrt{\\Lambda/32\\pi}$\n(square-roots Einstein's $8\\pi$)"]
cols  = [C_MOND, C_FW]
pies  = ["$\\pi^{0}$", "$\\pi^{1/2}$"]
xpos  = [0,1]
ax.bar(xpos, vals, width=0.5, color=cols, edgecolor="white", zorder=3)
ymax = max(vals)*1.30
for x,v,p in zip(xpos,vals,pies):
    ax.text(x, v+ymax*0.055, f"power of $\\pi$:  {p}", ha="center", va="bottom",
            fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))
    ax.text(x, v*0.5, f"{v:.2e}\nm/s$^2$", ha="center", va="center",
            color="white", fontsize=9.5, fontweight="bold")

ax.axhline(a0_milgrom, color=C_DATA, ls="--", lw=1.8, zorder=2,
           label=f"Milgrom $a_0\\approx1.2\\times10^{{-10}}$ (galaxies)")
ax.axhline(a0_density, color=C_FW, ls=":", lw=1.3, alpha=0.7, zorder=1,
           label="framework value $9.36\\times10^{-11}$")

ax.set_xticks(xpos); ax.set_xticklabels(labs, fontsize=8.5)
ax.set_ylabel("acceleration scale  (m/s$^2$)")
ax.set_title("The $\\sqrt{\\pi}$ fingerprint: same form, different power of $\\pi$")
ax.set_ylim(0, ymax)
ax.legend(frameon=False, loc="center right", fontsize=8.5)
ax.text(0.5,-0.30,"Only the $\\pi^{1/2}$ (density) route lands on the data; the $\\pi^0$ thermal route overshoots by the kernel $Z\\!=\\!5.789$.",
        ha="center", va="top", fontsize=8.5, style="italic", color=C_NEWTON, transform=ax.transAxes)
ax.text(0.99,0.97,"framework-computed (Ch. 22)", ha="right", va="top",
        fontsize=7, color=C_NEWTON, alpha=0.6, transform=ax.transAxes)
fig.tight_layout(); fig.savefig("ch22_sqrt_pi_fingerprint.png", bbox_inches="tight"); print("ok")
