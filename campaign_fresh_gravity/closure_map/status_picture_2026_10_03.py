#!/usr/bin/env python3
"""One-picture status board of the framework, 2026-10-03. Plot only: every tile restates a verdict recorded in
campaign_fresh_gravity/STANDING_2026-09-29.md (lane ids printed on each tile). kappa = 1/2 is FITTED; the cold mass is still required."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"PASS": "#2f8f5b", "COND": "#d9a521", "OPEN": "#8a94a0", "FAIL": "#c4452f", "LOCAL": "#2f8f5b", "UNDEC": "#5b7fb4"}
LAB = {"PASS": "pass", "COND": "conditional", "OPEN": "open", "FAIL": "fails", "UNDEC": "not decidable yet"}

groups = [
    ("Relativistic theory (the chassis)", [
        ("Gravity waves at light speed", "PASS", "c_T = 1 exact · CFG292"),
        ("Equations well-posed (high freq.)", "COND", "iff alpha_c > 0, beta = 0; open/cond. · CFG292"),
        ("Full nonlinear well-posedness", "COND", "local in time; A1-A5 assumed · CFG294"),
        ("Lapse condition, realistic matter", "PASS", "all but extreme GRB jets · CFG312"),
        ("Binary pulsars", "PASS", "margin 490,000x · CFG291/311"),
        ("Strong coupling", "COND", "bounded pass · XC1/XC3"),
        ("Solar-system PPN", "PASS", "gamma, beta, alpha_1-3 · FP2/KM3/CFG291"),
        ("Matter conservation (G9)", "PASS", "Bianchi identity holds; grad T = 0 · CFG329"),
        ("Structural order (G0)", "COND", "no ghost; elliptic solvability open · CFG329"),
        ("Black holes (EHT, LIGO ringdown)", "COND", "hidden mild inner-horizon defect · CFG318/319"),
    ]),
    ("Galaxies and clusters", [
        ("Rotation curves (SPARC RAR)", "PASS", "0.10 dex · nu_mono"),
        ("Local a0 from MeerKAT", "PASS", "0.9-1.4e-10, matches SPARC · CFG301/309"),
        ("Weak lensing (KiDS)", "PASS", "with bound-only switch"),
        ("Clusters, Bullet Cluster", "PASS", "needs the cold mass"),
        ("Andromeda + Local Volume dwarfs", "PASS", "law alone, native inputs · CFG313"),
        ("Milky Way ultra-faint dwarfs", "FAIL", "+0.32 dex, 3.8 sigma (lenient end) · audit"),
        ("Massive ellipticals (SLUGGS)", "UNDEC", "+0.09 dex, not significant; centrals fail · CFG323"),
    ]),
    ("Cosmology and a0 over time", [
        ("Constant a0 vs a0 ~ H(z)", "UNDEC", "calibration wall · PAPER38"),
        ("High-z on halo-free inputs", "UNDEC", "RC100 on the flat line · CFG303"),
        ("CRISTAL z~5 / ALESS 122.1", "UNDEC", "stress tests: not robust · CFG307/308"),
        ("Gaia DR4 wide binaries", "OPEN", "decides 2 Dec 2026 · prereg"),
        ("Structure growth, candidate B", "PASS", "as declared = LCDM growth · CFG324"),
        ("Structure growth, chassis alone", "FAIL", "~7x too fast; CMB lensing excludes · L341"),
    ]),
    ("The deep 'why'", [
        ("Why kappa = 1/2 (the 32 pi)", "OPEN", "fitted, not derived · CFG263/264"),
        ("What sets the cold-mass amount", "OPEN", "free in every build · CFG288"),
        ("Ownership from an action", "OPEN", "scoped no-gos · CFG242-245"),
        ("Radiative stability (G12)", "COND", "needs UV new physics <~1e9 GeV · CFG320"),
    ]),
]

fig = plt.figure(figsize=(15, 10.5), dpi=160)
fig.patch.set_facecolor("#f6f7f5")
ax = fig.add_axes([0.02, 0.06, 0.96, 0.84]); ax.set_xlim(0, 4); ax.set_ylim(0, 8.2); ax.axis("off")
fig.text(0.03, 0.955, "The Crispy Fried Chicken Status Board", fontsize=24, fontweight="bold", color="#16201d")
fig.text(0.03, 0.918, "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted.  Each tile restates a verdict recorded in STANDING (lane ids on the tiles).",
         fontsize=11.5, color="#4d5a56")
for gi, (title, items) in enumerate(groups):
    x0 = gi
    ax.text(x0 + 0.03, 7.95, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
    st_ = min(1.0, 7.9 / len(items))          # vertical step shrinks for long columns
    for k, (name, st, note) in enumerate(items):
        y = 7.45 - k * st_
        ax.add_patch(FancyBboxPatch((x0 + 0.03, y - 0.42 * st_), 0.92, 0.84 * st_, boxstyle="round,pad=0.0,rounding_size=0.06",
                                    facecolor=COL[st], edgecolor="none", alpha=0.92))
        ax.text(x0 + 0.07, y + 0.2 * st_, name, fontsize=10.6, fontweight="bold", color="white", va="center")
        ax.text(x0 + 0.07, y - 0.05 * st_, LAB[st].upper(), fontsize=8.6, color="white", va="center", alpha=0.95)
        ax.text(x0 + 0.07, y - 0.27 * st_, note, fontsize=8.6, color="white", va="center", alpha=0.95)
# legend
lx = 0.03
for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN"):
    fig.patches.append(FancyBboxPatch((lx, 0.025), 0.018, 0.022, boxstyle="round,pad=0,rounding_size=0.003",
                                      facecolor=COL[st], edgecolor="none", transform=fig.transFigure, figure=fig))
    fig.text(lx + 0.024, 0.036, LAB[st], fontsize=10.5, va="center", color="#16201d")
    lx += 0.13
fig.text(0.64, 0.036, "The cold mass (Omega_c h^2 ~ 0.12) is still required; no DM particle added.",
         fontsize=9, va="center", color="#4d5a56")
out = os.path.join(HERE, "STATUS_PICTURE_2026-10-03.png")
fig.savefig(out, dpi=160, facecolor=fig.get_facecolor())
print("wrote", os.path.relpath(out, HERE))
