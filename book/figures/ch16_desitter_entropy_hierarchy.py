import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, ax = plt.subplots(figsize=(7,4.3))

# constants (SI, hardcoded)
c=2.998e8; G=6.674e-11; hbar=1.055e-34; kB=1.381e-23
lP=np.sqrt(G*hbar/c**3)
Msun=1.989e30

# Bekenstein-Hawking: S/kB = A/(4 lP^2), with A=4 pi r_s^2 and r_s=2GM/c^2
def S_BH_over_kB(M):
    rs=2.0*G*M/c**2
    A=4.0*np.pi*rs**2
    return A/(4.0*lP**2)

# de Sitter horizon: S_dS/kB = pi c^5/(G hbar H^2)
H0=70.0*1000.0/3.086e22
S_dS=np.pi*c**5/(G*hbar*H0**2)   # already in units of kB

labels=["CMB photons\n(~10^88)",
        "solar-mass\nblack hole",
        "all stellar\nblack holes\n(~10^97)",
        "galaxy-center\nblack hole\n(~4e6 Msun)",
        "de Sitter\nhorizon (sky)"]
# values as log10(S/kB)
vals=[88.0,                                   # mainstream CMB photon entropy ~1e88 kB
      np.log10(S_BH_over_kB(Msun)),           # ~10^77
      97.0,                                   # mainstream tally for all stellar BHs ~1e97 kB
      np.log10(S_BH_over_kB(4e6*Msun)),       # SgrA*-scale ~10^90-91
      np.log10(S_dS)]                          # ~10^122
colors=[C_DATA, C_NEWTON, C_MOND, C_NEWTON, C_FW]

y=np.arange(len(vals))
ax.barh(y, vals, color=colors, edgecolor="white", height=0.62)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
for yi,v in zip(y,vals):
    ax.text(v+1.0, yi, f"$10^{{{v:.0f}}}$", va="center", fontsize=9, color="0.25")

ax.set_xlim(0,140)
ax.set_xlabel(r"entropy  $\log_{10}(S/k_B)$")
ax.set_title("Where the universe's hidden information lives")
ax.text(0.99,0.03,"S_dS = pi c^5 / (G hbar H^2);  S_BH = A/4l_P^2",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color="0.5")
fig.tight_layout(); fig.savefig("ch16_desitter_entropy_hierarchy.png", bbox_inches="tight"); print("ok")
