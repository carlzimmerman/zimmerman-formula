import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"font.size":11,
    "axes.grid":True,"grid.alpha":0.25,"axes.spines.top":False,"axes.spines.right":False,
    "axes.titlesize":12,"figure.facecolor":"white","axes.facecolor":"white"})
C_FW="#7c3aed"; C_NEWTON="#64748b"; C_MOND="#0891b2"; C_DATA="#dc2626"  # framework / Newton / MOND / data-or-obs

# Schematic: the four tests, each a fixed-size card in its own column, connected by a
# leader line to its date on the time axis. Gating logic shown by arrows between cards.
fig, ax = plt.subplots(figsize=(9.4, 5.2))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)

ax.text(50, 96, "Putting the four tests on one gated timeline",
        ha="center", fontsize=13, fontweight="bold")
ax.text(2, 88.5, "Cassini is already passed; DESI DR3 is the gate that opens (or closes) the galaxy tests.",
        ha="left", fontsize=8.8, color="#334155", style="italic")

# ----- time axis -----
ax_y = 14
ax.annotate("", xy=(98, ax_y), xytext=(3, ax_y),
            arrowprops=dict(arrowstyle="-|>", color="#334155", lw=1.6))
# map calendar year -> x in [5,95] over 2004..2036
def yx(year):
    return 5 + (year-2004)/(2036-2004)*90
for yr in [2005, 2010, 2015, 2020, 2025, 2030, 2035]:
    ax.plot([yx(yr), yx(yr)], [ax_y-1.2, ax_y+1.2], color="#334155", lw=1.0)
    ax.text(yx(yr), ax_y-4.2, str(yr), ha="center", va="center", fontsize=8.5, color="#334155")

# ----- four cards in fixed columns -----
def card(cx, cy, w, h, color, title, sub, status, date_year):
    box = FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                         boxstyle="round,pad=0.6,rounding_size=1.2",
                         linewidth=1.7, edgecolor=color, facecolor=color, alpha=0.13)
    ax.add_patch(box)
    ax.text(cx, cy+h*0.27, title, ha="center", va="center", fontsize=9.6,
            fontweight="bold", color=color)
    ax.text(cx, cy-h*0.02, sub, ha="center", va="center", fontsize=7.7, color="#334155")
    ax.text(cx, cy-h*0.30, status, ha="center", va="center", fontsize=7.5,
            style="italic", color="#64748b")
    # leader from card bottom to the date marker on the axis
    mx = yx(date_year)
    ax.plot(mx, ax_y, "o", color=color, ms=7, zorder=6)
    ax.annotate("", xy=(mx, ax_y+1.8), xytext=(cx, cy-h/2),
                arrowprops=dict(arrowstyle="-", color=color, lw=1.0, ls=":", alpha=0.7))

cw, ch = 21, 24
cy = 52
xs = [16, 39.5, 62.5, 85]   # four column centers
card(xs[0], cy, cw, ch, C_MOND, "CASSINI",
     "Solar-System safe\n"+r"$7.2\!\times\!10^{-7}\!<\!2.3\!\times\!10^{-5}$",
     "DONE (passed)", 2010.5)
card(xs[1], cy, cw, ch, C_DATA, "DESI DR3",
     r"Does $\rho_{\rm DE}$ evolve?"+"\n(the GATE)",
     "~2026-2027", 2026.5)
card(xs[2], cy, cw, ch, C_FW, "ALMA",
     "Offset SIGN:\ndistant galaxies\nspin slow?",
     "~2028-2030", 2029)
card(xs[3], cy, cw, ch, C_FW, "ELT/HARMONI",
     r"$a_0(z)$ SHAPE:"+"\n"+r"the $z\!\approx\!0.4$ bump",
     "early-mid 2030s", 2033)

# ----- gating arrows between cards -----
def between(i, j):
    arr = FancyArrowPatch((xs[i]+cw/2, cy), (xs[j]-cw/2, cy), arrowstyle="-|>",
                          mutation_scale=15, color="#334155", lw=1.7)
    ax.add_patch(arr)
between(1, 2)
between(2, 3)
ax.text((xs[1]+xs[2])/2, cy+ch/2+2.0, "only if evolving", ha="center",
        fontsize=7.6, color="#334155")
ax.text((xs[2]+xs[3])/2, cy+ch/2+2.0, "stays alive", ha="center",
        fontsize=7.6, color="#334155")

# Cassini stands alone (already done)
ax.text(xs[0], cy+ch/2+2.4, "stands alone\n(already in the bank)", ha="center",
        fontsize=7.4, color=C_MOND)

# the "gate closes" branch under DESI
ax.annotate(r"if $(w_0,w_a)\!\to\!(-1,0)$", xy=(xs[1], cy-ch/2),
            xytext=(xs[1], cy-ch/2-7), ha="center", va="top", fontsize=7.8,
            color="#64748b",
            arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=1.1, ls=":"))
ax.text(xs[1], cy-ch/2-15.5, "galaxy tests go silent;\nframework = fixed-$a_0$ MOND",
        ha="center", va="top", fontsize=7.4, color="#64748b")

ax.text(98, 1.5, "schematic timeline (illustrative)", ha="right",
        fontsize=7.5, color="#94a3b8")

fig.tight_layout()
fig.savefig("ch26_test_timeline_gate.png", bbox_inches="tight")
print("ok")
