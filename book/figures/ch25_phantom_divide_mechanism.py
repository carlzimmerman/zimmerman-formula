import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

w0, wa = -0.75, -0.86
def w_of_z(z):
    a = 1.0/(1.0+z)
    return w0 + wa*(1.0 - a)               # CPL equation of state
def rho_DE(z):
    return (1.0+z)**(3*(1.0+w0+wa)) * np.exp(-3*wa*z/(1.0+z))
z = np.linspace(0.0, 1.6, 600)
ww = w_of_z(z)
rho = rho_DE(z)

# find the w = -1 crossing (= density peak)
zc = z[np.argmin(np.abs(ww + 1.0))]

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(z, ww, color=C_DATA, lw=2.4, label=r"equation of state  $w(z)=w_0+w_a\frac{z}{1+z}$")
ax.axhline(-1.0, color=C_NEWTON, lw=1.3, ls=(0,(4,3)))
ax.text(1.45,-1.0," phantom divide  w = −1", color=C_NEWTON, va="center", ha="right", fontsize=8.5)
ax.fill_between(z, -1.0, ww, where=(ww<-1.0), color=C_DATA, alpha=0.08)
ax.text(1.0,-1.06,"phantom (w<−1):\ndensity grew", color=C_DATA, fontsize=8.5, ha="center")
ax.text(0.18,-0.90,"today w₀=−0.75\n(w>−1: diluting)", color=C_DATA, fontsize=8.5, ha="center")
ax.set_xlabel("redshift z")
ax.set_ylabel(r"equation of state  $w(z)$", color=C_DATA)
ax.tick_params(axis="y", labelcolor=C_DATA)
ax.set_xlim(0,1.6); ax.set_ylim(-1.12,-0.70)

# second axis: the density, peaking exactly at the crossing
ax2 = ax.twinx()
ax2.spines["top"].set_visible(False)
ax2.plot(z, rho, color=C_FW, lw=2.6, label=r"density  $\rho_{\rm DE}(z)/\rho_{\rm DE}(0)$")
ax2.set_ylabel(r"$\rho_{\rm DE}(z)/\rho_{\rm DE}(0)$", color=C_FW)
ax2.tick_params(axis="y", labelcolor=C_FW)
ax2.set_ylim(0.95,1.16)
ax2.grid(False)
ax2.axvline(zc, color="#334155", lw=1.0, ls=":")
ax2.scatter([zc],[rho_DE(zc)], color=C_FW, zorder=6, s=42)
ax2.annotate(f"density peak at the crossing\nz ≈ {zc:.2f}  →  a₀ peaks here too",
             xy=(zc, rho_DE(zc)), xytext=(0.45,1.005), fontsize=8.8, color=C_FW,
             arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.2))

lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
ax.legend(lines, [l.get_label() for l in lines], frameon=False, loc="lower right", fontsize=8.5)
ax.set_title("Why the bump sits at z ≈ 0.4: the phantom-divide crossing")
fig.tight_layout(); fig.savefig("ch25_phantom_divide_mechanism.png", bbox_inches="tight"); print("ok")
