import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs
fig, ax = plt.subplots(figsize=(7,4.3))

# Schematic rotation-curve SHAPES (arbitrary units), illustrating the contrast
# described in the chapter: expected Keplerian decline vs observed flatness.
r = np.linspace(0.01, 12.0, 600)
Rd = 2.5            # bright-disk scale (arbitrary)
vflat = 1.0         # plateau speed (arbitrary units)

# Inner solid-body-like rise that turns over near the bright disk edge,
# then for the point-mass / all-visible-mass-enclosed case falls Keplerian (v ~ r^-1/2).
# Build a smooth curve that rises, peaks near Rd, then declines as r^-1/2.
rise = np.sqrt(r/Rd) * np.exp(-(r/(2.2*Rd))**2)      # rise-then-roll shape
rise = rise/np.max(rise)                              # normalise peak to ~1
kep_tail = vflat*np.sqrt(Rd/np.maximum(r, Rd))        # r^-1/2 beyond the disk
v_expected = np.where(r < Rd, rise*vflat, kep_tail)
# blend the inner rise into the kep tail smoothly
w = 1/(1+np.exp((r-Rd)/0.4))
v_expected = w*(rise*vflat) + (1-w)*kep_tail

# Observed: same inner rise, then stays flat (the curve that would not fall)
v_flat = w*(rise*vflat) + (1-w)*vflat

ax.plot(r, v_flat, color=C_FW, lw=2.6, label="observed: flat (Rubin & Bosma)")
ax.plot(r, v_expected, color=C_NEWTON, lw=2.4, ls="--",
        label=r"expected from visible mass: Keplerian $v\propto r^{-1/2}$")

# Mark the bright stellar disk extent
ax.axvspan(0, 1.6*Rd, color="#f1efe8", alpha=0.8, zorder=0)
ax.text(1.6*Rd*0.5, 0.10, "bright stellar disk", ha="center", va="bottom",
        fontsize=9.5, color="#5f5e5a")
ax.annotate("curves agree\nwhere stars dominate", xy=(Rd*0.9, 0.95), xytext=(Rd*0.9, 1.18),
            ha="center", fontsize=8.5, color="#5f5e5a",
            arrowprops=dict(arrowstyle="-", color="#9ca3af", lw=0.8))
ax.annotate("the gap\n= 'missing mass'", xy=(9.5, 0.55), xytext=(9.2, 0.18),
            ha="center", fontsize=9, color=C_DATA,
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.2))

ax.set_xlim(0, 12); ax.set_ylim(0, 1.35)
ax.set_yticklabels([])
ax.set_xlabel("radius from galaxy centre  (arbitrary units)")
ax.set_ylabel("orbital speed $v(r)$")
ax.set_title("The curves that would not fall: expected vs observed")
ax.legend(frameon=False, loc="lower center", fontsize=9.5)
ax.text(0.99, 0.02, "schematic shapes", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8, color="#b4b2a9")
fig.tight_layout(); fig.savefig("ch04_keplerian_vs_flat.png", bbox_inches="tight"); print("ok")
