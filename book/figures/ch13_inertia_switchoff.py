import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

a0 = 9.36e-11  # m/s^2, framework's acceleration scale (FORM forced; VALUE is an input)

def mu_fw(x):
    return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

a = np.logspace(-3, 9, 1400) * a0      # 1e-3 a0 .. 1e9 a0
x = a/a0
ratio = mu_fw(x)

fig, ax = plt.subplots(figsize=(7.6,4.5))
ax.set_xscale("log")
ax.plot(a, ratio, color=C_FW, lw=2.6,
        label=r"framework  $m_{\rm eff}/m=\mu_{\rm fw}(a/a_0)$")
ax.axhline(1.0, color=C_NEWTON, ls="--", lw=1.8,
           label="Newton  ($m_{\\rm eff}=m$, inertia unchanged)")
ax.axvline(a0, color="0.6", ls=":", lw=1.4)
ax.text(a0*1.3, 0.30, r"$a_0=9.36\times10^{-11}$ m/s$^2$",
        rotation=90, va="center", fontsize=8.5, color="0.4")
ax.axvspan(1e-3*a0, 1.0*a0, color=C_MOND, alpha=0.08)
ax.axvspan(1e4*a0, 1e9*a0, color=C_NEWTON, alpha=0.08)

a_saturn = 6.5e-5
a_galaxy = 1.0e-11
ax.annotate("galaxy outskirts\n(stars orbit slowly)",
            xy=(a_galaxy, mu_fw(a_galaxy/a0)), xytext=(a_galaxy, 0.55),
            fontsize=8.2, ha="center", color="0.25",
            arrowprops=dict(arrowstyle="->", color="0.45", lw=1))
ax.annotate("Saturn around the Sun\n(Cassini tests live here)",
            xy=(a_saturn, mu_fw(a_saturn/a0)), xytext=(a_saturn, 0.45),
            fontsize=8.2, ha="center", color="0.25",
            arrowprops=dict(arrowstyle="->", color="0.45", lw=1))
ax.annotate("equivalence-principle tests\n(MICROSCOPE, Eot-Wash)",
            xy=(1e6*a0, mu_fw(1e6)), xytext=(2e4*a0, 0.62),
            fontsize=8.2, ha="center", color="0.25",
            arrowprops=dict(arrowstyle="->", color="0.45", lw=1))
ax.text(3e-3*a0, 0.92, "modification AWAKE\n(below $a_0$)", fontsize=8.5,
        color=C_MOND, ha="left", va="top")
ax.text(2e8*a0, 0.92, "modification ASLEEP\n(Solar-System regime)", fontsize=8.5,
        color="#334155", ha="right", va="top")

ax.set_xlabel(r"acceleration of the object  $a$   (m/s$^2$, log scale)")
ax.set_ylabel(r"effective inertia ratio  $m_{\rm eff}/m$")
ax.set_title("Where the modification sleeps and where it wakes")
ax.set_ylim(0, 1.08)
ax.set_xlim(a.min(), a.max())
ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.text(0.01,0.01,"computed from the framework's interpolation function",
        transform=ax.transAxes, fontsize=7.5, color="0.55")
fig.tight_layout(); fig.savefig("ch13_inertia_switchoff.png", bbox_inches="tight"); print("ok")
