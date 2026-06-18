import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# DESI DR2 evolving-dark-energy CPL fit (working numbers from the chapter)
w0, wa = -0.75, -0.86
Om, OL = 0.31, 0.69  # flat LCDM background for the rising rival

def R_fw(z):
    # framework signature: a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)), CPL closed form, ratio is parameter-free
    return (1.0+z)**(1.5*(1.0+w0+wa)) * np.exp(-1.5*wa*z/(1.0+z))

def E(z):
    # rising rival: scale tracks cH(z) ~ E(z)=H(z)/H0 (equivalently sqrt of TOTAL density)
    return np.sqrt(Om*(1.0+z)**3 + OL)

z = np.linspace(0.0, 3.0, 600)
fw = R_fw(z)
rival = E(z)

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(z, fw, color=C_FW, lw=2.6, label=r"Framework: $a_0\propto\sqrt{\rho_{\rm DE}(z)}$  (DESI DR2 CPL)")
ax.axhline(1.0, color=C_MOND, lw=2.0, ls=(0,(4,3)), label=r"Textbook MOND: $a_0$ constant")
ax.plot(z, rival, color=C_DATA, lw=2.0, ls=(0,(1,1)), label=r"Rising rival: $a_0\propto cH(z)$")

# mark the predicted peak and the three worked-example epochs
zpk = z[np.argmax(fw)]; Rpk = fw.max()
ax.scatter([zpk],[Rpk], color=C_FW, zorder=5, s=42)
ax.annotate(f"peak +{(Rpk-1)*100:.1f}%  at z≈{zpk:.2f}\n(phantom-divide crossing)",
            xy=(zpk,Rpk), xytext=(0.62,1.18), fontsize=9, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.2))
for zp in [0.4,1.0,3.0]:
    yp=R_fw(zp); ax.scatter([zp],[yp], color=C_FW, edgecolor="white", zorder=6, s=30)
ax.annotate(f"z=3: {R_fw(3.0):.2f}\n(≈26% below today)", xy=(3.0,R_fw(3.0)),
            xytext=(2.05,0.55), fontsize=9, color=C_FW,
            arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.2))
ax.annotate(f"≈{E(3.0)/R_fw(3.0):.0f}× gap\nat z=3", xy=(3.0, (E(3.0)+R_fw(3.0))/2),
            xytext=(2.35,3.2), fontsize=9, color=C_DATA)

ax.set_xlim(0,3); ax.set_ylim(0.4,4.8)
ax.set_xlabel("redshift z  (further back in cosmic time →)")
ax.set_ylabel(r"$a_0(z)\,/\,a_0(0)$")
ax.set_title("The signature curve: a bump, then a long decline")
ax.legend(frameon=False, loc="upper left", fontsize=8.5)
ax.text(0.99,0.02,"framework-computed; parameter-free ratio", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7.5, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch25_a0z_signature_curve.png", bbox_inches="tight"); print("ok")
