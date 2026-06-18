import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, ax = plt.subplots(figsize=(7,4.3))

a0 = 9.36e-11               # framework value, m/s^2
prior_window = 1.0e-9       # honest prior window for a free a0 (worked example)

# precision (fractional) the data pin a0 to, from loose to tight
prec = np.logspace(np.log10(0.20), np.log10(0.005), 400)   # 20% down to 0.5%
post_window = prec * a0
occ_factor = post_window / prior_window      # < 1 ; the penalty the expensive theory pays
disfavor = 1.0 / occ_factor                  # how many-to-1 the cheap theory is favored

ax.plot(prec*100, disfavor, color=C_NEWTON, lw=2.4,
        label="penalty paid by a theory that fits $a_0$ by hand")

# mark the two chapter values
for p, name, col in [(0.05, "5% (chapter)", C_DATA), (0.01, "1% (Question 4)", C_FW)]:
    d = prior_window / (p * a0)
    ax.scatter([p*100], [d], color=col, zorder=5, s=55)
    ax.annotate(f"{name}\n≈ {d:.0f} : 1", (p*100, d),
                textcoords="offset points", xytext=(8, -2), fontsize=9.5, color=col,
                va="center")

# the framework's line: it pays no a0 factor (favored by 1:1 baseline from this knob)
ax.axhline(1.0, color=C_FW, ls=":", lw=1.6)
ax.text(13.5, 1.25, "framework pays no $a_0$ factor (forces it)", color=C_FW, fontsize=9)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(20, 0.5)        # loose on left, tight on right
ax.set_xlabel("how tightly the data pin $a_0$  (fractional precision, %)")
ax.set_ylabel("economy advantage of the\ncheap theory  (odds : 1)")
ax.set_title("Tighter data make 'not fitting $a_0$' worth more")
ax.set_xticks([20,10,5,2,1,0.5]); ax.set_xticklabels(["20","10","5","2","1","0.5"])
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.text(0.99, 0.02, "Occam factor = (posterior window)/(prior window),  prior window $=10^{-9}$ m/s$^2$",
        transform=ax.transAxes, ha="right", fontsize=7.5, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch24_occam_factor_vs_precision.png", bbox_inches="tight"); print("ok")
