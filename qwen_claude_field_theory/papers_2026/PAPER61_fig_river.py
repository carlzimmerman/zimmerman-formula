#!/usr/bin/env python3
"""PAPER61 figure: the cosmic river map (illustrative, not evidence).

Reads the committed MAP1 output rebuild_2026_10_22/MAP1_cosmic_river/map1_cosmic_river.json (commit 3f9b3ae361) and draws
the smoothed Cosmicflows-4 peculiar-velocity field in the supergalactic slice |SGZ| < 25 Mpc, R < 160 Mpc, with the SPARC
galaxies and the nearby eRASS1 clusters that fall in the slice. No fit, no computation beyond plotting.
Writes PAPER61_fig_river.pdf and PAPER61_fig_river.png next to this script.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 PAPER61_fig_river.py
kappa = 1/2 FITTED; this map makes no claim about the theory."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "rebuild_2026_10_22", "MAP1_cosmic_river", "map1_cosmic_river.json")
CLIP = 1000.0

d = json.load(open(SRC))
xs = np.array(d["grid"]["x"]); ys = np.array(d["grid"]["y"])
field = np.array([[np.nan if v is None else v for v in row] for row in d["grid"]["field"]], dtype=float)
field = np.clip(field, -CLIP, CLIP)
zcut = d["slice"]["sgz"]; R = d["slice"]["R"]
sp = [s for s in d["sparc"] if abs(s[3]) < zcut]
cl = [c for c in d["clusters"] if abs(c[3]) < zcut]
assert len(sp) == 153 and len(cl) == 74, (len(sp), len(cl))

plt.rcParams.update({"font.size": 9, "font.family": "serif"})
fig, ax = plt.subplots(figsize=(6.4, 6.4))
dx = xs[1] - xs[0]
ext = [xs[0] - dx / 2, xs[-1] + dx / 2, ys[0] - dx / 2, ys[-1] + dx / 2]
im = ax.imshow(field, origin="lower", extent=ext, cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0, vmin=-CLIP, vmax=CLIP),
               interpolation="nearest")
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(R * np.cos(t), R * np.sin(t), color="0.55", lw=0.6)
ax.scatter([s[1] for s in sp], [s[2] for s in sp], s=14, marker="o", facecolor="#1a9850", edgecolor="white", linewidth=0.6,
           zorder=3, label=f"SPARC galaxies in the slice ({len(sp)}): pools where $a_0$ sets the core")
ax.scatter([c[1] for c in cl], [c[2] for c in cl], s=34, marker="s", facecolor="#ffd92f", edgecolor="black", linewidth=0.6,
           zorder=4, label=f"eRASS1 clusters, $z<0.037$, in the slice ({len(cl)}): drains still filling by infall")
ax.plot([0], [0], marker="*", ms=10, color="black", zorder=5, label="Milky Way")
ax.set_xlim(-R - 5, R + 5); ax.set_ylim(-R - 5, R + 5); ax.set_aspect("equal")
ax.set_xlabel("SGX (Mpc, redshift distance $cz/H$)"); ax.set_ylabel("SGY (Mpc)")
ax.set_title(r"Cosmicflows-4 peculiar flow, supergalactic slice $|{\rm SGZ}|<25$ Mpc (illustrative)", fontsize=9)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label(r"smoothed $v_{\rm pec}$ (km s$^{-1}$; $\sigma=10$ Mpc; clipped at $\pm1000$)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), fontsize=7, frameon=False, ncol=1)
ax.grid(False)
fig.tight_layout()
for ext_ in ("pdf", "png"):
    fig.savefig(os.path.join(HERE, f"PAPER61_fig_river.{ext_}"), dpi=200, metadata={"CreationDate": None} if ext_ == "pdf" else None)
print(f"PAPER61_fig_river: {len(sp)} SPARC, {len(cl)} clusters, field cells {int(np.isfinite(field).sum())}, written")
