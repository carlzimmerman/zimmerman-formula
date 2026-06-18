import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Hubble tension: two published measurements with 1-sigma error bars.
# Values from the chapter's Deeper Dive box.
fig, ax = plt.subplots(figsize=(7,4.3))

H_cmb, e_cmb = 67.4, 0.5   # Planck 2018 CMB + LCDM extrapolation
H_loc, e_loc = 73.0, 1.0   # SH0ES Cepheid-calibrated distance ladder

ax.errorbar([H_cmb],[1.0], xerr=[e_cmb], fmt='o', color=C_NEWTON, capsize=5, ms=9,
            label="early universe: Planck CMB + ΛCDM  (67.4±0.5)")
ax.errorbar([H_loc],[0.5], xerr=[e_loc], fmt='s', color=C_DATA, capsize=5, ms=9,
            label="late universe: SH0ES distance ladder  (73.0±1.0)")

ax.fill_betweenx([0.3,1.2], H_cmb-e_cmb, H_cmb+e_cmb, color=C_NEWTON, alpha=0.12)
ax.fill_betweenx([0.3,1.2], H_loc-e_loc, H_loc+e_loc, color=C_DATA, alpha=0.12)

gap = H_loc - H_cmb
sig = gap/np.sqrt(e_cmb**2 + e_loc**2)
ax.annotate("", xy=(H_loc,1.0), xytext=(H_cmb,1.0),
            arrowprops=dict(arrowstyle="<->", color="#333", lw=1.3))
ax.text((H_cmb+H_loc)/2, 1.07, f"Δ = {gap:.1f}   (≈{sig:.0f}σ)",
        ha="center", fontsize=10, fontweight="bold")

ax.set_yticks([]); ax.set_ylim(0.2,1.3)
ax.set_xlim(64.5,75.5)
ax.set_xlabel("$H_0$   (km s$^{-1}$ Mpc$^{-1}$)")
ax.set_title("The Hubble tension: the same universe, two answers")
ax.legend(frameon=False, loc="lower center")
ax.text(0.99,0.02,"Planck 2018 / SH0ES published values", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7, color="#888")
fig.tight_layout(); fig.savefig("ch12_hubble_tension.png", bbox_inches="tight"); print("ok")
