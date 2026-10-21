#!/usr/bin/env python3
"""One-picture status board of the framework, 2026-10-21. Plot only: every tile restates a verdict recorded in
campaign_fresh_gravity/LEDGER.md or in the dated notes of THEORY_CANONICAL_2026-10-18.md (lane ids printed on each tile).
Copied from status_picture_2026_10_03.py (the 10-10 board, left unedited) and updated to the record of 2026-10-21.
kappa = 1/2 is FITTED; footings never pooled; cold energy is real gravitating mass, not a particle species; not theory closed.
Run: OMP_NUM_THREADS=1 python3 status_picture_2026_10_21.py  (one core, seconds, < 0.3 GB)."""
import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
COL = {"PASS": "#2f8f5b", "COND": "#d9a521", "OPEN": "#8a94a0", "FAIL": "#c4452f", "UNDEC": "#5b7fb4"}
LAB = {"PASS": "pass", "COND": "conditional", "OPEN": "open", "FAIL": "fails", "UNDEC": "not decidable yet"}

# (name, status, note[, label override]). Notes end with the lane ids the colour restates.
groups = [
    ("Relativistic theory (the chassis)", [          # unchanged since the 10-10 board
        ("Gravity waves at light speed", "PASS", "c_T = 1 exact · CFG292"),
        ("Equations well-posed (high freq.)", "COND", "iff alpha_c > 0, beta = 0; open/cond. · CFG292"),
        ("Full nonlinear well-posedness", "COND", "local in time; A1-A5 assumed · CFG294"),
        ("Lapse condition, realistic matter", "PASS", "all but extreme GRB jets · CFG312"),
        ("Binary pulsars", "PASS", "margin 490,000x · CFG291/311"),
        ("Strong coupling", "COND", "bounded pass · XC1/XC3"),
        ("Solar system (PPN + Cassini Q2)", "PASS", "filter evades Q2 tension at kappa 1/2 · CFG291/357"),
        ("Matter conservation (G9)", "PASS", "Bianchi identity holds; grad T = 0 · CFG329"),
        ("Structural order (G0)", "COND", "no ghost; elliptic solvability open · CFG329"),
        ("Zero-field nonlinear, ungated", "FAIL", "chassis only; B switch off there · CFG358"),
        ("Black holes (EHT, LIGO ringdown)", "COND", "hidden mild inner-horizon defect · CFG318/319"),
    ]),
    ("Galaxies", [
        ("Rotation curves (SPARC RAR)", "PASS", "rms 0.101 / 0.099 dex; no rotator has an excess · CFG695/919"),
        ("Local a0 from MeerKAT", "PASS", "0.9-1.4e-10, matches SPARC · CFG301/309"),
        ("Isolated-galaxy lensing, inner", "PASS", "supply suffices <= 0.31 Mpc; blue lenses A 1.016 ± 0.086 · CFG804/829/840/902"),
        ("Isolated-galaxy lensing, all radii", "FAIL", "falls short beyond ~0.4 Mpc; two-halo term closes 57-59% · CFG902/903"),
        ("Tidal dwarfs, NGC 1052-DF2/DF4", "COND", "at Newton, if they captured no cold energy · CFG936/939"),
        ("Globulars + ownership rule", "COND", "Newton ~1.6 sigma; 3 of 4 pops · CFG332/333"),
        ("Central ellipticals (SLUGGS)", "UNDEC", "~3 sigma with measured tracers · CFG528b"),
        ("Galaxy groups (BFJR)", "PASS", "consistent supply closes · CFG540/543"),
        ("MW vertical force (round rule)", "PASS", "beats MOND phantom disc 32/32 · CFG516"),
        ("MW outer slope (Gaia)", "UNDEC", "3-5 sigma steeper; NFW too; DR4 decides · CFG532b/533"),
    ]),
    ("The excess family (open)", [
        ("Local Group dwarfs (83)", "FAIL", "+0.37 / +0.33 dex over the law; no mechanism in the record · CFG919/925/930"),
        ("Cluster cores (318 eRASS1)", "FAIL", "x1.91 / x1.75 over the law (outskirts on it); real mass · CFG687/922/929"),
        ("Coma ultra-diffuse galaxies", "UNDEC", "+0.33 dex over the law, 2.4-2.6 sigma, fragile · CFG933/948"),
        ("Red (early-type) lenses", "COND", "an IMF alpha-sigma relation removes it, if discs stay near Chabrier · CFG926"),
        ("One selector for the family", "OPEN", "no one-constant selector fits all · CFG914/919/921/928"),
    ]),
    ("Cosmology and a0 over time", [
        ("a0(z): native band vs a0 ~ H(z)", "UNDEC", "own BAO ruler band; data cannot decide yet · CFG689/PAPER38"),
        ("High-z on halo-free inputs", "UNDEC", "RC100 on the flat line · CFG303"),
        ("CRISTAL z~5 / ALESS 122.1", "UNDEC", "stress tests: not robust · CFG307/308"),
        ("Cosmic shear, native inputs", "COND", "KiDS CONSISTENT on both footings; engine has no parent · CFG654-A2/A3/909"),
        ("CMB lensing (Planck PR4)", "UNDEC", "SAFE; CONSISTENT only under post-hoc A1; low power · CFG917/927"),
        ("Growth, zero-knob supply rule", "FAIL", "15-19% too clumpy at 512^3 (gravitating) · CFG555/556"),
        ("Structure growth, chassis alone", "FAIL", "~7x too fast; CMB lensing excludes · L341"),
        ("ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN", "original frozen plans govern; one disc excludes no model · CFG806-U4/809/942"),
        ("Gaia DR4 wide binaries (Dec)", "OPEN", "Newtonian; kills iff R-1 >= max(0.01, 3 sigma_R) · CFG740/943"),
        ("Gaia DR4 MW predictions", "OPEN", "sealed 10-10 · CFG553"),
        ("The owner's wave a0(z) idea", "OPEN", "being tested, no result yet · CFG956/957"),
    ]),
    ("The deep 'why' and the parent", [
        ("Why kappa = 1/2", "OPEN", "fitted; measured 0.417 ± 0.095; not derived · CFG493/894"),
        ("What sets the cold-mass amount", "OPEN", "5.364 and f_ret are inputs, not derived · CFG886"),
        ("Ownership from an action", "OPEN", "the label sector has no action · CFG945/950/953"),
        ("Law + a^1 growth + no EFE, local", "FAIL", "no local theory gives all three (no-go theorems) · CFG941/944/946/947"),
        ("Physical parent of the shear engine", "OPEN", "3 tried: LDT, SCT fail clusters; no kinetic parent · CFG951/954/955",
         "open: none known"),
        ("Energy books of settling", "OPEN", "not conserved; a repair needs new physics · CFG932/935"),
        ("Radiative stability (G12)", "COND", "needs UV new physics <~1e9 GeV · CFG320"),
    ]),
]

NCOL = len(groups)
fig = plt.figure(figsize=(20.5, 13.2), dpi=150)
fig.patch.set_facecolor("#f6f7f5")
ax = fig.add_axes([0.012, 0.065, 0.976, 0.835]); ax.set_xlim(0, NCOL); ax.set_ylim(-0.25, 8.2); ax.axis("off")
fig.text(0.015, 0.958, "The Crispy Fried Chicken Status Board  ·  21 October 2026", fontsize=24, fontweight="bold", color="#16201d")
fig.text(0.015, 0.922, "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted; footings 9.3603e-11 / 1.1312e-10 m/s^2 never pooled.  "
         "Each tile restates a verdict in the campaign LEDGER or THEORY_CANONICAL (lane ids on the tiles).  The theory is incomplete.",
         fontsize=11.5, color="#4d5a56")
WRAP = 50                                         # characters per note line at fontsize 8.4
for gi, (title, items) in enumerate(groups):
    x0 = gi
    ax.text(x0 + 0.03, 7.95, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
    st_ = min(1.0, 7.55 / max(len(g[1]) for g in groups))   # one tile height for every column
    for k, item in enumerate(items):
        name, st, note = item[:3]
        lab = item[3] if len(item) > 3 else LAB[st]
        y = 7.45 - k * st_
        ax.add_patch(FancyBboxPatch((x0 + 0.03, y - 0.43 * st_), 0.93, 0.86 * st_, boxstyle="round,pad=0.0,rounding_size=0.05",
                                    facecolor=COL[st], edgecolor="none", alpha=0.93))
        lines = textwrap.wrap(note, WRAP)
        assert len(lines) <= 2, (name, lines)
        ax.text(x0 + 0.065, y + 0.27 * st_, name, fontsize=10.4, fontweight="bold", color="white", va="center")
        ax.text(x0 + 0.065, y + 0.07 * st_, lab.upper(), fontsize=8.2, color="white", va="center", alpha=0.95)
        for j, ln in enumerate(lines):
            ax.text(x0 + 0.065, y - (0.13 + 0.19 * j) * st_, ln, fontsize=8.4, color="white", va="center", alpha=0.97)
# legend
lx = 0.015
for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN"):
    fig.patches.append(FancyBboxPatch((lx, 0.026), 0.014, 0.02, boxstyle="round,pad=0,rounding_size=0.003",
                                      facecolor=COL[st], edgecolor="none", transform=fig.transFigure, figure=fig))
    fig.text(lx + 0.019, 0.036, LAB[st], fontsize=10.5, va="center", color="#16201d")
    lx += 0.105
fig.text(0.55, 0.036, "Cold energy (Omega_c/Omega_b = 5.364, an input) is real gravitating mass, not a particle species.",
         fontsize=9.5, va="center", color="#4d5a56")
out = os.path.join(HERE, "STATUS_PICTURE_2026-10-21.png")
fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
print("wrote", os.path.relpath(out, HERE))
