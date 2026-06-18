import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Fig 11.3 -- the chapter's hinge teaser: the SAME rho_DE that dominates the
# cosmic energy budget also sets the galactic acceleration scale a0 ~ c sqrt(G rho_DE).
# LEFT: energy budget today (Planck-2018 fractions). RIGHT: the order-of-magnitude
# bridge from rho_DE to a0, computed from the chapter's own teaser formula.
fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4,4.3),
                               gridspec_kw={"width_ratios":[1,1.15]})

# --- LEFT: donut of the cosmic energy budget ---
axL.grid(False)
fracs = [68.5, 26.5, 5.0]
labels = ["dark energy\n68.5%", "dark matter\n26.5%", "ordinary matter\n5%"]
cols = [C_FW, C_NEWTON, "#cbd5e1"]
wedges,_ = axL.pie(fracs, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
axL.text(0,0, r"$\rho_{\rm DE}$"+"\nprotagonist", ha="center", va="center",
         fontsize=11, color=C_FW, weight="bold")
axL.legend(wedges, labels, frameon=False, fontsize=8.5,
           loc="lower center", bbox_to_anchor=(0.5,-0.18))
axL.set_title("Cosmic energy budget today", fontsize=11)
axL.set(aspect="equal")

# --- RIGHT: the numerical bridge rho_DE -> a0 ---
axR.grid(True, alpha=0.25)
c=2.998e8; G=6.674e-11
rho_de = 6e-27                       # kg/m^3, measured value from the chapter
a0_bridge = c*np.sqrt(G*rho_de)      # chapter teaser estimate ~ 1.9e-10
a0_form   = c**2*np.sqrt(1.1e-52/(32*np.pi))   # framework FORM (the VALUE is an input)
a0_gal    = 1.0e-10                  # quoted galactic scale

xs = [0,1,2]
ys = [a0_bridge, a0_form, a0_gal]
names = [r"$c\sqrt{G\rho_{\rm DE}}$"+"\n(ch. teaser)",
         r"$c^2\sqrt{\Lambda/32\pi}$"+"\n(framework form)",
         "galactic\n$a_0$ (obs.)"]
barcols=[C_DATA, C_FW, C_MOND]
axR.bar(xs, ys, color=barcols, width=0.6, alpha=0.9)
for x,y in zip(xs,ys):
    axR.text(x, y*1.06, f"{y:.1e}", ha="center", va="bottom", fontsize=8.5)
axR.axhline(1e-10, color="#94a3b8", ls=":", lw=1)
axR.set_yscale("log")
axR.set_ylim(3e-11, 5e-10)
axR.set_xticks(xs); axR.set_xticklabels(names, fontsize=8.5)
axR.set_ylabel(r"acceleration  (m s$^{-2}$)")
axR.set_title("Same number, two corners of the cosmos", fontsize=11)
axR.text(0.99,0.02,"order-of-magnitude bridge -- coincidence shared by MOND family",
         transform=axR.transAxes, ha="right", va="bottom", fontsize=7, color="#94a3b8")

fig.suptitle(r"$\rho_{\rm DE}$ sets the galactic acceleration scale $a_0$", fontsize=12.5, y=1.02)
fig.tight_layout(); fig.savefig("ch11_rhoDE_to_a0_bridge.png", bbox_inches="tight"); print("ok")
