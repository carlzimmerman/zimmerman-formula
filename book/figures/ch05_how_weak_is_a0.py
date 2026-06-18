import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

# Visualizes the chapter's Worked Example: how absurdly gentle a0 is, by placing it on
# a ladder of familiar accelerations, AND (right panel) where in a galaxy gravity sinks
# to a0. All values are framework-computed / hardcoded textbook constants.
a0      = 9.36e-11   # framework a0 (m/s^2); MOND's 1.2e-10 is the same order
a0_mond = 1.2e-10

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.8, 4.6),
                               gridspec_kw={"width_ratios":[1.05,1.0]})

# ---- LEFT: a ladder of accelerations on a single horizontal log axis ----
# Each item is a point placed at its acceleration; this is a true "ladder", not a bar.
items = [
    ("Rocket launch (~3$g$)",          3*9.8),
    ("Earth gravity $g$",              9.8),
    ("Braking car",                    5.0),
    ("Stellar pull, mid-Galaxy*",      1.9e-8),   # order-of-magnitude
    ("Sun's pull at Pluto",            3.7e-7),    # GM_sun/(39.5 AU)^2
    ("$a_0$  (galaxy edge)",           a0),
]
labels = [t for t,_ in items]
vals   = np.array([v for _,v in items])
y = np.arange(len(vals))[::-1]
cols = [C_NEWTON]*5 + [C_FW]
sizes = [80]*5 + [150]
axL.scatter(vals, y, s=sizes, color=cols, zorder=5, edgecolors="white", linewidths=0.8)
# faint stems to a common baseline at a0 so the gap to a0 is visible
for v, yi, c in zip(vals, y, cols):
    axL.plot([a0, v], [yi, yi], color=c, lw=1.4, alpha=0.45, zorder=1)
for v, yi, lab, c in zip(vals, y, labels, cols):
    axL.text(v*1.6, yi+0.16, lab, va="bottom", ha="left", fontsize=8.3, color="0.2")
axL.axvline(a0, color=C_FW, ls=":", lw=1.4)
axL.set_xscale("log")
axL.set_xlim(3e-11, 1e3)
axL.set_yticks([]); axL.set_ylim(-0.9, len(vals)-0.2)
axL.set_xlabel("acceleration  (m/s$^2$, log scale)")
axL.set_title("$a_0$ on the ladder of accelerations")
axL.text(a0*1.3, -0.78,
         "$a_0\\approx10^{-10}$ m/s$^2$ — about $10^{11}\\times$ feebler than $g$",
         color=C_FW, fontsize=8, ha="left", va="center")

# ---- RIGHT: where in a flat-rotation galaxy does g sink to a0? ----
# Flat-rotation toy: v = const => enclosed-mass Newtonian g_bar(r) = v^2 / r falls as 1/r.
v_flat = 150e3          # 150 km/s, typical outer disk
kpc    = 3.086e19       # m
r = np.linspace(0.5, 60, 500)*kpc
g_bar = v_flat**2 / r   # Newtonian acceleration scale of a flat-curve disk (m/s^2)

axR.plot(r/kpc, g_bar, color=C_NEWTON, lw=2.4, label="visible-matter pull $g_{\\rm bar}(r)\\propto 1/r$")
axR.axhline(a0, color=C_FW, ls="--", lw=2, label="$a_0=9.36\\times10^{-11}$ m/s$^2$ (framework)")
axR.axhline(a0_mond, color=C_MOND, ls=":", lw=1.6, label="$a_0=1.2\\times10^{-10}$ (MOND)")
# crossing radius where g_bar = a0
r_cross = v_flat**2 / a0 / kpc
axR.plot([r_cross],[a0],"o",color=C_FW,ms=7,zorder=5)
axR.annotate(f"books start to fail\nat r $\\approx$ {r_cross:.0f} kpc",
             xy=(r_cross,a0), xytext=(r_cross+6, a0*4),
             fontsize=8.3, color=C_FW,
             arrowprops=dict(arrowstyle="->",color=C_FW,lw=1.1))
axR.set_yscale("log"); axR.set_ylim(2e-11, 5e-9)
axR.set_xlim(0,60)
axR.set_xlabel("radius from galaxy centre  (kpc)")
axR.set_ylabel("acceleration  (m/s$^2$)")
axR.set_title("Where a galaxy's gravity reaches $a_0$")
axR.legend(frameon=False, fontsize=8, loc="upper right")

fig.suptitle("How small is $a_0$? — almost four centuries to reach a walking pace",
             fontsize=12, y=1.0)
fig.text(0.99,0.005,"framework-computed (flat-rotation toy, v=150 km/s)",
         ha="right",va="bottom",fontsize=7.5,color="0.55")
fig.tight_layout(); fig.savefig("ch05_how_weak_is_a0.png", bbox_inches="tight"); print("ok")
