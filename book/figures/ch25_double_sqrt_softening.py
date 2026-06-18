import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

w0, wa = -0.75, -0.86
def rho_DE(z):  # CPL closed form, density ratio
    return (1.0+z)**(3*(1.0+w0+wa)) * np.exp(-3*wa*z/(1.0+z))
z = np.linspace(0.0, 3.0, 600)
rho = rho_DE(z)              # the underlying dark-energy density
a0  = np.sqrt(rho)           # first sqrt: a0 = sqrt(rho_DE)
vf  = a0**0.25              # second sqrt-of-sqrt: v_flat ~ a0^(1/4) via BTFR v^4 = G M a0

fig, ax = plt.subplots(figsize=(7,4.3))
ax.plot(z, rho, color=C_DATA, lw=2.2, label=r"1. dark-energy density  $\rho_{\rm DE}(z)/\rho_{\rm DE}(0)$")
ax.plot(z, a0,  color=C_FW,  lw=2.6, label=r"2. acceleration scale  $a_0\propto\sqrt{\rho_{\rm DE}}$")
ax.plot(z, vf,  color=C_MOND, lw=2.2, label=r"3. rotation speed  $v_{\rm flat}\propto a_0^{1/4}$  (BTFR)")
ax.axhline(1.0, color=C_NEWTON, lw=1.2, ls=(0,(4,3)))

# annotate the peak cascade at z~0.4: 13% -> 6% -> 1.5%
zp=0.4
for curve,col,lab in [(rho,C_DATA,"+13%"),(a0,C_FW,"+6%"),(vf,C_MOND,"+1.5%")]:
    yp=np.interp(zp,z,curve)
    pct=(yp-1)*100
    ax.scatter([zp],[yp],color=col,zorder=5,s=28)
ax.annotate("each √ halves the\nfractional swing\n+13% → +6% → +1.5%",
            xy=(0.4,1.07), xytext=(0.85,1.18), fontsize=9, color="#334155",
            arrowprops=dict(arrowstyle="->", color="#334155", lw=1.1))
# z=3 spread
ax.annotate("at z=3:  –26% → –26% (a0=0.74) → only –7% in speed",
            xy=(2.6,0.80), xytext=(1.05,0.55), fontsize=8.5, color="#334155",
            arrowprops=dict(arrowstyle="->", color="#334155", lw=1.0))

ax.set_xlim(0,3); ax.set_ylim(0.5,1.22)
ax.set_xlabel("redshift z")
ax.set_ylabel("ratio relative to today (z = 0)")
ax.set_title("Two square roots in a row: why the observable signal is gentle")
ax.legend(frameon=False, loc="lower left", fontsize=8.5)
ax.text(0.99,0.97,"framework-computed", transform=ax.transAxes, ha="right", va="top",
        fontsize=7.5, color="#94a3b8")
fig.tight_layout(); fig.savefig("ch25_double_sqrt_softening.png", bbox_inches="tight"); print("ok")
