import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"

fig, ax = plt.subplots(figsize=(7,4.6))
ax.grid(False)

# spacetime diagram: x (space) horizontal, t (time) vertical
ax.axhline(0, color="#cbd5e1", lw=0.8)
ax.axvline(0, color="#cbd5e1", lw=0.8)

# light-cone / Rindler horizon: the lines x = |t|
L = 2.6
ax.plot([0, L],[0, L], color=C_DATA, lw=2.2)
ax.plot([0, L],[0,-L], color=C_DATA, lw=2.2)
ax.plot([0,-L],[0, L], color="#fca5a5", lw=1.6, ls="--")
ax.plot([0,-L],[0,-L], color="#fca5a5", lw=1.6, ls="--")

# accelerated (Rindler) worldlines: x = xi cosh(a eta), t = xi sinh(a eta)
eta = np.linspace(-1.35,1.35,200)
for xi,alp in [(0.7,0.45),(1.1,0.7),(1.6,1.0)]:
    x = xi*np.cosh(eta); t = xi*np.sinh(eta)
    ax.plot(x,t, color=C_FW, lw=2.0, alpha=alp)
# label the central accelerated observer
ax.annotate("accelerated\nobserver\n(the diver)", (1.1*np.cosh(0.0),0.0),
            textcoords="offset points", xytext=(10,-26), fontsize=9, color=C_FW)

# the right (accessible) Rindler wedge
ax.fill_between([0,L],[0,L],[0,-L], color=C_FW, alpha=0.06)
ax.text(1.85,0.0,"RIGHT WEDGE\nyou can be reached here", fontsize=8.5,
        color=C_FW, ha="center", va="center")
# the hidden left wedge
ax.fill_between([-L,0],[L,0],[-L,0], color="#94a3b8", alpha=0.12)
ax.text(-1.55,0.0,"LEFT WEDGE\nhidden behind\nthe horizon", fontsize=8.5,
        color="#475569", ha="center", va="center")

# horizon label
ax.annotate("Rindler horizon  $x=|t|$", (L*0.78, L*0.78),
            textcoords="offset points", xytext=(-6,8), fontsize=9, color=C_DATA, ha="right")

# the consequence chain, as a caption strip inside the figure
chain = r"acceleration $\rightarrow$ horizon $\rightarrow$ hidden wedge $\rightarrow$ thermal vacuum at $T=\hbar a/2\pi c$"
ax.text(0.5,-0.16, chain, transform=ax.transAxes, ha="center", va="top",
        fontsize=9.5, color="#334155")

ax.set_xlim(-L-0.1,L+0.1); ax.set_ylim(-L-0.1,L+0.1)
ax.set_aspect("equal")
ax.set_xlabel("space  $x$"); ax.set_ylabel("time  $t$")
ax.set_title("How acceleration makes a horizon — and a horizon makes warmth")
ax.text(0.99,0.01,"schematic (Rindler geometry)", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=7.5, color="#9ca3af")
fig.tight_layout(); fig.savefig("ch14_rindler_horizon_schematic.png", bbox_inches="tight"); print("ok")
