import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"
fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.6,4.3))
for a in (axL, axR):
    a.grid(False); a.set_xticks([]); a.set_yticks([])
    a.spines["left"].set_visible(False); a.spines["bottom"].set_visible(False)

# Earth center (well below the frame), used to aim the radial paths
cx, cy = 0.0, -9.0

# ---------- LEFT: horizontal pair -> converge (sideways squeeze) ----------
x0 = np.array([-0.9, 0.9])      # two balls released side by side at top
y_top = 3.0
y_levels = np.linspace(y_top, 0.2, 60)
for xb in x0:
    # straight line toward Earth's center; parametrize by height
    t = (y_top - y_levels)/(y_top - cy)
    px = xb + (cx - xb)*t
    py = y_levels
    axL.plot(px, py, color=C_FW, lw=1.4, alpha=0.55)
# release positions (top) and final positions (bottom)
for xb in x0:
    axL.scatter([xb],[y_top], s=70, color=C_FW, zorder=5, edgecolor="white")
    t = (y_top - 0.2)/(y_top - cy)
    axL.scatter([xb+(cx-xb)*t],[0.2], s=70, color=C_FW, zorder=5, edgecolor="white")
axL.annotate("", xy=(0.25,0.55), xytext=(0.55,0.55),
             arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.4))
axL.annotate("", xy=(-0.25,0.55), xytext=(-0.55,0.55),
             arrowprops=dict(arrowstyle="->", color=C_DATA, lw=1.4))
axL.text(0.0, 0.55, "squeeze", color=C_DATA, ha="center", va="bottom", fontsize=9)
axL.text(0.0, y_top+0.35, "released side by side", ha="center", fontsize=9)
axL.annotate("toward Earth's center", xy=(0.0,-0.2), xytext=(0.0,-0.85),
             ha="center", fontsize=8.5, color=C_NEWTON,
             arrowprops=dict(arrowstyle="->", color=C_NEWTON, lw=1.0))
axL.set_title("Sideways pair  →  converge")
axL.set_xlim(-2.0, 2.0); axL.set_ylim(-1.2, 3.7)

# ---------- RIGHT: vertical pair -> separate (vertical stretch) ----------
# lower ball is closer to Earth, stronger g, falls faster -> gap grows
yU0, yL0 = 2.4, 1.0            # upper and lower start heights
# fall distances ~ g(height) increasing downward; model gap growth schematically
steps = np.linspace(0, 1, 60)
# acceleration grows as you get closer to Earth (1/r^2 toward cy)
def fall(y0):
    # integrate a simple deepening: lower start -> larger drop
    drop = 0.0; y = y0; ys=[y]
    for _ in range(59):
        gloc = 1.0/ (y - cy)**2 * 30.0   # stronger when closer to center
        y = y - 0.018*gloc
        ys.append(y)
    return np.array(ys)
yU = fall(yU0); yL = fall(yL0)
xcol = 0.0
axR.plot(np.full_like(yU, xcol), yU, color=C_FW, lw=1.4, alpha=0.55)
axR.plot(np.full_like(yL, xcol), yL, color=C_FW, lw=1.4, alpha=0.55)
axR.scatter([xcol,xcol],[yU0,yL0], s=70, color=C_FW, zorder=5, edgecolor="white")
axR.scatter([xcol,xcol],[yU[-1],yL[-1]], s=70, color=C_FW, zorder=5, edgecolor="white")
# initial gap bracket vs final gap bracket
axR.annotate("", xy=(0.45,yU0), xytext=(0.45,yL0),
             arrowprops=dict(arrowstyle="<->", color=C_NEWTON, lw=1.2))
axR.text(0.55, (yU0+yL0)/2, "start gap", color=C_NEWTON, fontsize=8.5, va="center")
axR.annotate("", xy=(-0.45,yU[-1]), xytext=(-0.45,yL[-1]),
             arrowprops=dict(arrowstyle="<->", color=C_DATA, lw=1.6))
axR.text(-0.55, (yU[-1]+yL[-1])/2, "larger gap", color=C_DATA, fontsize=8.5,
         va="center", ha="right")
axR.text(0.0, yU0+0.35, "released one above the other", ha="center", fontsize=9)
axR.annotate("toward Earth's center", xy=(0.0, yL[-1]-0.15), xytext=(0.0, yL[-1]-0.7),
             ha="center", fontsize=8.5, color=C_NEWTON,
             arrowprops=dict(arrowstyle="->", color=C_NEWTON, lw=1.0))
axR.set_title("Vertical pair  →  stretch")
axR.set_xlim(-1.5, 1.5); axR.set_ylim(yL[-1]-1.2, yU0+0.9)

fig.suptitle("Tidal forces: the part of gravity you cannot fall away from", fontsize=12.5)
fig.text(0.99, 0.01, "schematic — geodesic deviation", ha="right", va="bottom",
         fontsize=7.5, color="#999999")
fig.tight_layout(rect=[0,0.02,1,0.96])
fig.savefig("ch07_tidal_geodesic_deviation.png", bbox_inches="tight"); print("ok")
