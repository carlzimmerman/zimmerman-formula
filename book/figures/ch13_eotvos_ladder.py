import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Published ladder of equivalence-principle (Eotvos-parameter) upper limits.
exps = [
    ("Newton\n(pendulums)",          1686, 1e-3),
    (u"Eötvös\ntorsion balance",     1909, 1e-9),
    (u"Eöt-Wash\n(U. Washington)",   2008, 1e-13),
    ("MICROSCOPE\nsatellite",        2022, 2.3e-15),
]
labels = [e[0] for e in exps]
years  = np.array([e[1] for e in exps])
bounds = np.array([e[2] for e in exps])
x = np.arange(len(exps))

fig, ax = plt.subplots(figsize=(7.4,4.6))
ax.set_yscale("log")
ax.bar(x, bounds, width=0.55, color=C_DATA, alpha=0.85, zorder=3,
       edgecolor="white", label=r"measured upper bound on $|\eta|$")
blabels = [r"$\leq 10^{-3}$", r"$\leq 10^{-9}$", r"$\leq 10^{-13}$", r"$\leq 2.3\times10^{-15}$"]
for xi, b, yr, bl in zip(x, bounds, years, blabels):
    ax.text(xi, b*1.9, bl, ha="center", va="bottom", fontsize=8.6, color="#7a0e0e")
    ax.text(xi, 1.4e-16, str(yr), ha="center", va="bottom", fontsize=8, color="0.45")
ax.axhline(2.3e-15, color=C_FW, ls="--", lw=1.8, zorder=2,
           label="present floor a modified-inertia theory must respect")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(7e-17, 5e-2)
ax.set_ylabel(r"Eotvos parameter upper limit  $|\eta|$")
ax.set_title("How precisely we know inertial mass = gravitational mass")
ax.legend(frameon=False, loc="upper right", fontsize=8.6)
ax.text(0.99,-0.16,"published bounds; shorter bar = tighter test",
        transform=ax.transAxes, fontsize=7.5, color="0.55", ha="right")
fig.tight_layout(); fig.savefig("ch13_eotvos_ladder.png", bbox_inches="tight"); print("ok")
