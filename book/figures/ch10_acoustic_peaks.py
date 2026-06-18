import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# SCHEMATIC sheet-music of the acoustic peaks. This is a smooth illustrative MODEL of
# D_ell = ell(ell+1)C_ell/2pi, NOT a fit to data. Peaks are placed at the textbook
# multipoles (ell ~ 220, 540, 810, ...) with hand-set heights to show the
# odd-enhanced / even-suppressed pattern that cold dark matter imprints.
ell = np.linspace(2, 1400, 2000)

# large-scale Sachs-Wolfe plateau (gentle rise into the first peak)
plateau = 1.0 / (1 + (ell/90.0)**(-1.3))

# acoustic peaks as damped Gaussians on top of the plateau
def peak(l0, amp, w):
    return amp*np.exp(-0.5*((ell-l0)/w)**2)

# odd peaks (compression) tall; even peaks (rarefaction) shorter -> the CDM signature
D = 0.95*plateau \
  + peak(220, 5.4, 70)   \
  + peak(535, 2.4, 75)   \
  + peak(810, 2.5, 80)   \
  + peak(1130,1.1, 90)
# Silk damping roll-off at small scales
D *= np.exp(-(ell/1500.0)**1.6)

fig, ax = plt.subplots(figsize=(7.4,4.4))
ax.plot(ell, D, color=C_FW, lw=2.4, label="acoustic-peak model (schematic)")

# (label, peak-ell, color, text-x, text-y)  -- text placed by hand to avoid the top axis
labels = [("1st peak\n(compression)", 220, "#7c3aed", 250, 6.45),
          ("2nd peak\n(rarefaction)", 535, C_MOND,   535, 3.7),
          ("3rd peak\n(compression)", 810, "#7c3aed", 700, 3.4)]
for txt, l0, col, tx, ty in labels:
    yi = D[np.argmin(np.abs(ell-l0))]
    ax.annotate(txt, xy=(l0, yi), xytext=(tx, ty),
                ha="center", fontsize=8.5, color=col,
                arrowprops=dict(arrowstyle="-", color=col, lw=0.8))

# odd/even shading note
ax.text(220, 0.4, "ODD", ha="center", fontsize=8, color="#7c3aed", weight="bold")
ax.text(535, 0.4, "EVEN", ha="center", fontsize=8, color=C_MOND, weight="bold")
ax.text(810, 0.4, "ODD", ha="center", fontsize=8, color="#7c3aed", weight="bold")

ax.annotate("cold dark matter raises ODD peaks,\nlowers EVEN peaks  -> 3rd-peak height\nis the CDM thermometer",
            xy=(810, D[np.argmin(np.abs(ell-810))]), xytext=(905, 4.5),
            fontsize=8.5, color=C_DATA,
            arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1))

ax.set_xlabel(r"multipole $\ell$   (large patches $\leftarrow$    $\rightarrow$ small patches)")
ax.set_ylabel(r"fluctuation power  $\mathcal{D}_\ell=\ell(\ell+1)C_\ell/2\pi$  (arb.)")
ax.set_title("The universe's sheet music: the CMB acoustic peaks")
ax.set_xlim(0, 1400); ax.set_ylim(0, 7.0)
ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(0.99, 0.99))
# secondary top axis: approximate angular size
secax = ax.secondary_xaxis('top', functions=(lambda l: 180.0/np.maximum(l,1),
                                              lambda a: 180.0/np.maximum(a,1e-6)))
secax.set_xlabel("approx. angular size  (degrees)", fontsize=9)
secax.set_xticks([2,1,0.5,0.25,0.15])
ax.text(0.99, 0.02, "schematic - peak positions textbook, heights illustrative",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch10_acoustic_peaks.png", bbox_inches="tight"); print("ok")
