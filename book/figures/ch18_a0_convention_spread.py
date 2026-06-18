import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# The chapter's convention grid: best-fit a0 (1e-10 m/s^2 units) slides with
# {interpolation} x {mass-to-light Upsilon}. Values from the chapter's Deeper Dive:
#  - framework dS-Unruh nu @ Y~0.7  -> optimum ~1.0e-10  (forcing 9.36 costs ~0.5%)
#  - McGaugh nu @ Y~0.7             -> optimum ~7.8e-11  (9.36 looks ~20% high)
#  - McGaugh nu @ Y~0.5 (lit default)-> 9.36 looks ~20% low; opt toward ~1.4-1.8e-10
# Full reasonable spread quoted: ~7.5e-11 .. 1.8e-10.
rows = [
    ("dS-Unruh interp,  $\\Upsilon\\approx0.7$  (framework's own curve)", 1.00, C_FW),
    ("simple interp,    $\\Upsilon\\approx0.7$",                          1.05, C_MOND),
    ("McGaugh $\\nu$,    $\\Upsilon\\approx0.7$",                         0.78, C_NEWTON),
    ("McGaugh $\\nu$,    $\\Upsilon\\approx0.5$  (common literature)",    1.45, C_NEWTON),
    ("simple interp,    $\\Upsilon\\approx0.5$",                          1.55, C_MOND),
]
labels = [r[0] for r in rows]
opt    = np.array([r[1] for r in rows])      # in 1e-10 units
cols   = [r[2] for r in rows]

fig, ax = plt.subplots(figsize=(7.4, 4.6))
y = np.arange(len(rows))[::-1]

# the full convention band 7.5e-11 .. 1.8e-10
ax.axvspan(0.75, 1.80, color="#94a3b8", alpha=0.18, lw=0,
           label="full convention spread  $7.5$ to $18\\times10^{-11}$")

# each convention's best-fit a0 as a marker
ax.scatter(opt, y, s=90, c=cols, zorder=5)
for yi, lab in zip(y, labels):
    ax.text(0.40, yi, lab, va="center", ha="left", fontsize=8.6)

# the framework's fixed prediction 9.36e-11
ax.axvline(0.936, color=C_FW, lw=2.4,
           label=r"framework's $a_0=9.36\times10^{-11}$ (from $\Lambda$)")
# the canonical RAR quote 1.2e-10
ax.axvline(1.20, color="black", lw=1.4, ls="--", alpha=0.7,
           label=r"oft-quoted RAR value $1.2\times10^{-10}$")

ax.set_yticks([]); ax.set_ylim(-0.6, len(rows)-0.4)
ax.set_xlim(0.35, 2.0)
ax.set_xlabel(r"SPARC best-fit $a_0$   ($\times10^{-10}$ m/s$^2$)")
ax.set_title("Where $9.36\\times10^{-11}$ sits: the best-fit $a_0$ is convention-sensitive")
ax.legend(frameon=False, fontsize=8.2, loc="lower right")
ax.text(0.005, 0.005,
        "optima are the chapter's stated convention grid; framework line is the fixed prediction",
        transform=ax.transAxes, fontsize=7, color="gray")
fig.tight_layout(); fig.savefig("ch18_a0_convention_spread.png", bbox_inches="tight"); print("ok")
