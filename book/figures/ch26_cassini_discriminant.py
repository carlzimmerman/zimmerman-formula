import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

a0 = 9.36e-11  # m/s^2

# framework interpolation mu_fw(x) = (sqrt(1+4x^2)-1)/(2x), x=g/a0 ; departure from Newton = 1 - mu_fw
def one_minus_mu(x):
    return 1.0 - (np.sqrt(1.0+4.0*x**2) - 1.0)/(2.0*x)

x = np.logspace(-2, 7, 800)          # g/a0 from deep-MOND to deep-Newton
dep = one_minus_mu(x)                # framework's fractional anomaly 1 - mu_fw

# Saturn point
g_sat = 6.5e-5                       # m/s^2, Sun's pull at Saturn
x_sat = g_sat/a0                     # ~7e5
dep_sat = one_minus_mu(x_sat)        # 7.2e-7
cassini = 2.3e-5                     # |gamma-1| bound

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 4.3),
                               gridspec_kw={"width_ratios":[1.45, 1.0]})

# ---------- LEFT: the effect switches itself off as acceleration rises ----------
axL.loglog(x, dep, color=C_FW, lw=2.4,
           label=r"framework $1-\mu_{\rm fw}(g/a_0)$")
axL.axhline(cassini, color=C_DATA, lw=1.6, ls="--",
            label=r"Cassini bound $|\gamma-1|<2.3\times10^{-5}$")
axL.fill_between(x, cassini, 1e0, color=C_DATA, alpha=0.07)
# Saturn marker
axL.plot(x_sat, dep_sat, "o", color=C_FW, ms=8, zorder=6)
axL.annotate(f"Saturn:\n$g/a_0\\approx7\\times10^5$\n$1-\\mu_{{\\rm fw}}=7.2\\times10^{{-7}}$",
             xy=(x_sat, dep_sat), xytext=(2.5e3, 4e-6), fontsize=8.5, color=C_FW,
             arrowprops=dict(arrowstyle="->", color=C_FW, lw=1.0))
axL.axvline(1.0, color=C_NEWTON, lw=1.0, ls=":")
axL.text(1.3, 1.2e-7, "$g=a_0$", fontsize=8, color=C_NEWTON, rotation=90, va="bottom")
axL.text(2e-2, 0.45, "deep-MOND\n(galaxy outskirts)", fontsize=8, color=C_MOND)
axL.text(3e4, 0.30, "Newtonian\n(Solar System)", fontsize=8, color=C_NEWTON, ha="left")
axL.set_xlabel(r"acceleration ratio $g/a_0$")
axL.set_ylabel(r"departure from Newton  $1-\mu_{\rm fw}$")
axL.set_ylim(1e-7, 2.0)
axL.set_title("Modified inertia switches OFF where acceleration is high")
axL.legend(frameon=False, fontsize=8.5, loc="lower left")

# ---------- RIGHT: predicted vs allowed at Saturn ----------
labels = ["framework\npredicts", "Cassini\nallows"]
vals   = [dep_sat, cassini]
cols   = [C_FW, C_DATA]
ypos   = [0, 1]
bars = axR.barh(ypos, vals, color=cols, alpha=0.85, height=0.5)
axR.set_yticks(ypos); axR.set_yticklabels(labels, fontsize=9)
axR.set_xscale("log")
axR.set_xlim(1e-7, 1e-4)
axR.set_xlabel("fractional anomaly at Saturn's orbit")
axR.set_title(r"$\sim$30$\times$ margin: a clean pass")
for yp, v in zip(ypos, vals):
    axR.text(v*1.25, yp, f"{v:.1e}", va="center", ha="left", fontsize=9,
             color=cols[yp])
axR.annotate("", xy=(cassini, 0.5), xytext=(dep_sat, 0.5),
             arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.2))
axR.text(np.sqrt(dep_sat*cassini), 0.62, "30$\\times$", ha="center", fontsize=10,
         color="#475569", fontweight="bold")
axR.invert_yaxis()
axR.grid(axis="y", alpha=0)

fig.text(0.99, 0.01, "framework-computed (mu_fw interpolation); Cassini bound: published value",
         ha="right", va="bottom", fontsize=7.5, color="#94a3b8")
fig.tight_layout(rect=[0,0.03,1,1])
fig.savefig("ch26_cassini_discriminant.png", bbox_inches="tight")
print("ok")
