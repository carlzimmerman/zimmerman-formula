import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# The framework's induced, inherited gravitational SME coefficient (Chapter 30).
s_predicted = 4.8e-12                       # ~ inherited from a0; "induces, not derives"

# Published bound LEVELS for the gravitational s_mu_nu sector (orders of magnitude;
# the chapter states most components sit at 1e-9..1e-11, the single tightest near a few x 1e-12).
# These are drawn as illustrative bound *levels*, not as specific tabulated numbers.
bound_levels = [1e-9, 1e-10, 1e-11, 9.6e-12]
bound_labels = ["typical\ncomponents", "many\ncomponents", "good\ncomponents", "tightest\nsingle\ncomponent"]

fig, ax = plt.subplots(figsize=(7,4.3))

xs = np.arange(len(bound_levels))

# Excluded region (above each bar) shaded faintly; the bar marks the bound itself.
ax.bar(xs, bound_levels, width=0.55, color=C_DATA, alpha=0.18, edgecolor=C_DATA, linewidth=1.4,
       label="published bound (excluded above)")

# The framework's prediction as a horizontal line across all components.
ax.axhline(s_predicted, color=C_FW, lw=2.4, label=r"framework prediction  $s_{\rm lab}\approx4.8\times10^{-12}$")

# Annotate the margin against the tightest component (factor ~2).
factor = bound_levels[-1]/s_predicted
ax.annotate("", xy=(xs[-1], bound_levels[-1]), xytext=(xs[-1], s_predicted),
            arrowprops=dict(arrowstyle="<->", color=C_NEWTON, lw=1.3))
ax.text(xs[-1]+0.06, np.sqrt(bound_levels[-1]*s_predicted),
        f"only ~{factor:.0f}x\nbelow", color=C_NEWTON, fontsize=9.5, va="center", ha="left")

# Annotate the comfortable margin against typical bounds.
ax.text(xs[0], s_predicted*1.25, "passes by\n2-3 orders", color=C_FW, fontsize=9.5,
        ha="center", va="bottom")

ax.set_yscale("log")
ax.set_ylim(1e-12, 3e-9)
ax.set_xticks(xs); ax.set_xticklabels(bound_labels, fontsize=9)
ax.set_ylabel(r"SME coefficient magnitude  $|s_{\mu\nu}|$")
ax.set_title("The induced coefficient against the SME bound ladder")
ax.legend(frameon=False, loc="upper right", fontsize=9.5)

ax.text(0.99, 0.02, "framework: induces, does not derive", transform=ax.transAxes,
        fontsize=7.5, color=C_NEWTON, ha="right", va="bottom", alpha=0.7)

fig.tight_layout(); fig.savefig("ch30_sme_bounds_ladder.png", bbox_inches="tight"); print("ok")
