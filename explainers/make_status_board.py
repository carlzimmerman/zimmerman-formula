#!/usr/bin/env python3
"""The Crispy Fried Chicken status board, 22 October 2026 (evening). Plot only.

Every tile restates a verdict recorded in campaign_fresh_gravity/LEDGER.md, THEORY_CANONICAL_2026-10-18.md, or a
committed lane of 22 October (doors_push_2026_10_22/, covariant_push_2026_10_22/, summarised in
covariant_push_2026_10_22/THEORY_V3_DRAFT.md). Layout and colours follow the 21 October board
(campaign_fresh_gravity/closure_map/status_picture_2026_10_21.py, left unedited).

Re-scoring rule for this board: a tile changes colour only if a committed 22 October lane changes it; nothing turns
green without a committed lane that passes it; unresolved reds stay red. Each tile records its 21 October colour
(`prev`, None for a tile new on this board) so the checks below can enforce that rule.

kappa = 1/2 is FITTED; footings never pooled; cold energy is real gravitating mass, not a particle species;
the theory is not closed.

Run:  OMP_NUM_THREADS=1 python3 explainers/make_status_board.py            (writes explainers/img/status_board.png)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --mutate   (strips one tile's evidence lane; the
                                                                            checks must FAIL and nothing is written)
One core, seconds, < 0.3 GB.
"""
import copy
import os
import re
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img", "status_board.png")

COL = {"PASS": "#2f8f5b", "COND": "#d9a521", "OPEN": "#8a94a0", "FAIL": "#c4452f", "UNDEC": "#5b7fb4"}
LAB = {"PASS": "pass", "COND": "conditional", "OPEN": "open", "FAIL": "fails", "UNDEC": "not decidable yet"}
COLUMNS = ["Relativistic theory (the chassis)", "Galaxies", "The excess family (open)",
           "Cosmology and a0 over time", "The deep 'why' and the parent"]
# Lane ids committed on 22 October (doors push D*/E*, covariant push C*, CFG960 amendment A6, rebuild brief F*).
LANE_22 = re.compile(r"^(C[1-8]|D\d+[a-d]?|E[1-6]|CFG960|F[1-4])$")


def T(col, name, st, note, lanes, prev, lab=None, new22=False):
    """One tile: column index, label, colour (status), note, evidence lane ids, 21 October colour."""
    return dict(col=col, name=name, st=st, note=note, lanes=list(lanes), prev=prev, lab=lab, new22=new22)


TILES = [
    # ---- column 0: the chassis, now the Blanchet-Skordis Khronon theory in its literal form (C4) ----
    T(0, "Gravity waves at light speed", "PASS", "only the 2 tensor modes propagate, at c exactly", ["C5", "C8", "CFG292"], "PASS", new22=True),
    T(0, "Health: ghosts, gradients", "COND", "Khronon literal form healthy; eta > 0 (A33) ill-posed", ["C5"], "COND", new22=True),
    T(0, "Leaf problem well-posed", "COND", "weak field: elliptic, unique; strong fields open", ["C8"], "COND", new22=True),
    T(0, "Causality: criterion A / B", "COND", "instantaneous constraints; faster-than-light signal ~1e-46 m/s^2", ["C5", "C8"], None,
      lab="B met, A violated", new22=True),
    T(0, "Lapse condition, realistic matter", "PASS", "all but extreme GRB jets (older chassis lane)", ["CFG312"], "PASS"),
    T(0, "Binary pulsars + GW170817", "PASS", "no radiative channel; <= 3e-14 of double-pulsar error", ["C8", "CFG291", "CFG311"], "PASS", new22=True),
    T(0, "Solar system + Cassini (screened)", "PASS", "Q2 2.8e7-5.1e9 inside bound at L* 24-90 pc; Mars 0.17", ["D7d", "C6"], "PASS",
      new22=True),
    T(0, "Unscreened law vs Cassini", "FAIL", "fails Cassini by 2.4-5.2x; no unscreened law passes both", ["E2", "D7c"], None, new22=True),
    T(0, "Strong coupling", "COND", "bounded pass", ["XC1", "XC3"], "COND"),
    T(0, "Matter conservation (G9)", "PASS", "Bianchi identity holds; grad T = 0", ["CFG329"], "PASS"),
    T(0, "Structural order (G0)", "COND", "no ghost; elliptic solvability open", ["CFG329"], "COND"),
    T(0, "Zero-field nonlinear, ungated", "FAIL", "chassis only; B switch off there", ["CFG358"], "FAIL"),
    T(0, "Black holes (EHT, LIGO ringdown)", "COND", "hidden mild inner-horizon defect", ["CFG318", "CFG319"], "COND"),
    # ---- column 1: galaxies ----
    T(1, "Rotation curves (SPARC RAR)", "PASS", "rms 0.101 / 0.099 dex; no rotator has an excess", ["CFG695", "CFG919"], "PASS"),
    T(1, "Local a0 from MeerKAT", "PASS", "0.9-1.4e-10, matches SPARC", ["CFG301", "CFG309"], "PASS"),
    T(1, "Isolated-galaxy lensing, inner", "PASS", "supply suffices <= 0.31 Mpc; blue lenses A 1.016", ["CFG804", "CFG829", "CFG840", "CFG902"], "PASS"),
    T(1, "Isolated-galaxy lensing, all radii", "FAIL", "short beyond ~0.4 Mpc; rebuild F2 re-examining", ["CFG902", "CFG903", "F2"], "FAIL"),
    T(1, "Tidal dwarfs, NGC 1052-DF2/DF4", "COND", "at Newton, if they captured no cold energy", ["CFG936", "CFG939"], "COND"),
    T(1, "Outer globulars: L* floor", "COND", "L* >= 21.7 / 22.9 pc (SPS M/L); unscreened law excluded", ["D10"], "COND", new22=True),
    T(1, "Globulars + ownership rule", "COND", "Newton ~1.6 sigma; 3 of 4 pops", ["CFG332", "CFG333"], "COND"),
    T(1, "Central ellipticals (SLUGGS)", "UNDEC", "~3 sigma with measured tracers", ["CFG528b"], "UNDEC"),
    T(1, "Galaxy groups (BFJR)", "PASS", "consistent supply closes", ["CFG540", "CFG543"], "PASS"),
    T(1, "MW vertical force (round rule)", "PASS", "beats MOND phantom disc 32/32", ["CFG516"], "PASS"),
    T(1, "MW outer slope (Gaia)", "UNDEC", "3-5 sigma steeper; NFW too; DR4 decides", ["CFG532b", "CFG533"], "UNDEC"),
    # ---- column 2: the excess family ----
    T(2, "Dwarf satellites vs screened law", "FAIL", "+0.89 dex over screened prediction; no packing mechanism",
      ["E3", "E6", "CFG919"], "FAIL", new22=True),
    T(2, "Dwarf cold supply (chemistry)", "COND", "own [Fe/H] gives enough supply, if zeta = 1 winds", ["E6"], None, new22=True),
    T(2, "Cluster cores (318 eRASS1)", "FAIL", "x1.91 / x1.75 over the law; rebuild F1 re-examining", ["CFG687", "CFG922", "CFG929", "F1"], "FAIL"),
    T(2, "Coma ultra-diffuse galaxies", "UNDEC", "+0.33 dex over the law, 2.4-2.6 sigma, fragile", ["CFG933", "CFG948"], "UNDEC"),
    T(2, "Red (early-type) lenses", "COND", "an IMF alpha-sigma relation removes it, if discs stay near Chabrier",
      ["CFG926"], "COND"),
    T(2, "One selector for the family", "OPEN", "no one-constant selector fits all", ["CFG914", "CFG919", "CFG921", "CFG928"], "OPEN"),
    # ---- column 3: cosmology and a0 over time ----
    T(3, "a0(z): native band vs a0 ~ H(z)", "UNDEC", "own BAO ruler band; data cannot decide yet", ["CFG689", "PAPER38"], "UNDEC"),
    T(3, "High-z on halo-free inputs", "UNDEC", "RC100 on the flat line", ["CFG303"], "UNDEC"),
    T(3, "CRISTAL z~5 / ALESS 122.1", "UNDEC", "stress tests: not robust", ["CFG307", "CFG308"], "UNDEC"),
    T(3, "Cosmic shear, native inputs", "COND", "KiDS CONSISTENT on both footings; engine has no parent",
      ["CFG654-A2", "CFG654-A3", "CFG909"], "COND"),
    T(3, "Native shear rerun (CFG960)", "OPEN", "1024^3 running past its old failure point; no verdict", ["CFG960"], None,
      lab="open: running", new22=True),
    T(3, "Native CMB (patched CLASS)", "OPEN", "validated vs CLASS to 2e-6; spectra not yet run", ["C7", "C2"], None, new22=True),
    T(3, "CMB lensing (Planck PR4)", "UNDEC", "SAFE; CONSISTENT only under post-hoc A1; low power", ["CFG917", "CFG927"], "UNDEC"),
    T(3, "Growth, zero-knob supply rule", "FAIL", "15-19% too clumpy at 512^3; rebuild F3 re-examining", ["CFG555", "CFG556", "F3"], "FAIL"),
    T(3, "Structure growth, chassis alone", "FAIL", "~7x too fast; CMB lensing excludes", ["L341"], "FAIL"),
    T(3, "ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN", "harness ready, 3 kernels; expected unscorable", ["CFG806-U4", "CFG809", "CFG942", "D4"],
      "OPEN", new22=True),
    T(3, "Gaia DR4 wide binaries (Dec)", "OPEN", "screened gamma-1 ~ 8e-6 vs AQUAL 1.167 / 1.199", ["C6", "E2", "D2", "CFG943"], "OPEN",
      new22=True),
    T(3, "Gaia DR4 MW predictions", "OPEN", "sealed 10-10", ["CFG553"], "OPEN"),
    T(3, "The owner's wave a0(z) idea", "OPEN", "being tested, no result yet", ["CFG956", "CFG957"], "OPEN"),
    # ---- column 4: the deep 'why' and the parent ----
    T(4, "Why kappa = 1/2", "OPEN", "fitted, 0.417 ± 0.095; no horizon construction gives it", ["CFG493", "CFG894", "D5"], "OPEN",
      lab="open: fitted", new22=True),
    T(4, "Stiffness length L*", "OPEN", "new fitted constant; floor ~22 pc, edge ~90 pc", ["C3", "D10"], None,
      lab="open: fitted", new22=True),
    T(4, "What sets the cold-mass amount", "OPEN", "dust abundance is an initial condition; 5.364 an input",
      ["C2", "C4", "CFG886"], "OPEN", lab="open: fitted", new22=True),
    T(4, "Ownership from an action", "OPEN", "the label sector has no action", ["CFG945", "CFG950", "CFG953"], "OPEN"),
    T(4, "Law + a^1 growth + no EFE, local", "FAIL", "no-go theorems; rebuild F1-F3 re-examining",
      ["CFG941", "CFG944", "CFG946", "CFG947", "F1", "F2", "F3"], "FAIL"),
    T(4, "Physical parent of the shear engine", "OPEN", "3 tried: LDT, SCT fail clusters; no kinetic parent",
      ["CFG951", "CFG954", "CFG955"], "OPEN", lab="open: none known"),
    T(4, "Energy books of settling", "OPEN", "not conserved; a repair needs new physics", ["CFG932", "CFG935"], "OPEN"),
    T(4, "Radiative stability (G12)", "COND", "needs UV new physics <~1e9 GeV", ["CFG320"], "COND"),
]

# Reds that must stay red until a committed rebuild lane says otherwise.
MUST_STAY_RED = ["Cluster cores (318 eRASS1)", "Isolated-galaxy lensing, all radii", "Growth, zero-knob supply rule",
                 "Law + a^1 growth + no EFE, local"]
WRAP = 52  # characters per note line at fontsize 8.4


def lane_text(t):
    return "/".join(t["lanes"])


def check(tiles):
    errs = []
    for t in tiles:
        if not t["lanes"] or any(not str(x).strip() for x in t["lanes"]):
            errs.append(f"no evidence lane: {t['name']}")
        if t["st"] not in COL:
            errs.append(f"bad colour {t['st']}: {t['name']}")
        changed = t["prev"] is not None and t["st"] != t["prev"]
        if changed and not any(LANE_22.match(x) for x in t["lanes"]):
            errs.append(f"colour changed without a 22 October lane: {t['name']}")
        if t["st"] == "PASS" and t["prev"] != "PASS":
            errs.append(f"turned green: {t['name']} (needs a committed passing lane; refused on this board)")
        if t["prev"] is None and not t["new22"]:
            errs.append(f"new tile not flagged as 22 October: {t['name']}")
        lines = textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)
        if len(lines) > 2:
            errs.append(f"note too long ({len(lines)} lines): {t['name']}")
    names = {t["name"]: t for t in tiles}
    for n in MUST_STAY_RED:
        if n not in names or names[n]["st"] != "FAIL":
            errs.append(f"must stay red: {n}")
    if len(names) != len(tiles):
        errs.append("duplicate tile names")
    return errs


def draw(tiles, out):
    ncol = len(COLUMNS)
    nmax = max(sum(1 for t in tiles if t["col"] == c) for c in range(ncol))
    W, H = 20.5, 2.6 + 0.94 * nmax                   # inches; each tile ~0.94 in tall as on the 21 October board
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    top_in, bot_in = 1.25, 0.95                      # header and legend bands, inches
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.25, nmax + 0.65); ax.axis("off")
    fig.text(0.015, 1 - 0.55 / H, "The Crispy Fried Chicken Status Board  ·  22 October 2026 (evening)", fontsize=24,
             fontweight="bold", color="#16201d")
    fig.text(0.015, 1 - 1.0 / H, "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted; footings 9.3603e-11 / 1.1312e-10 m/s^2 never "
             "pooled.  Chassis = Blanchet-Skordis Khronon, literal form, screened by L*.  Lane ids on every tile.  "
             "The theory is incomplete.", fontsize=11.0, color="#4d5a56")
    for c, title in enumerate(COLUMNS):
        ax.text(c + 0.03, nmax + 0.4, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
        for k, t in enumerate([t for t in tiles if t["col"] == c]):
            y = nmax - 0.5 - k
            ax.add_patch(FancyBboxPatch((c + 0.03, y - 0.43), 0.93, 0.86, boxstyle="round,pad=0.0,rounding_size=0.05",
                                        facecolor=COL[t["st"]], edgecolor="none", alpha=0.93))
            ax.text(c + 0.065, y + 0.27, t["name"], fontsize=10.4, fontweight="bold", color="white", va="center")
            lab = (t["lab"] or LAB[t["st"]]).upper()
            ax.text(c + 0.065, y + 0.07, lab, fontsize=8.2, color="white", va="center", alpha=0.95)
            if t["new22"]:
                ax.text(c + 0.945, y + 0.27, "22 OCT", fontsize=7.6, fontweight="bold", color="white", va="center",
                        ha="right", alpha=0.9)
            for j, ln in enumerate(textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)):
                ax.text(c + 0.065, y - 0.13 - 0.19 * j, ln, fontsize=8.4, color="white", va="center", alpha=0.97)
    lx, ly = 0.015, 0.42 / H
    for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN"):
        fig.patches.append(FancyBboxPatch((lx, ly - 0.01 * 13.2 / H), 0.014, 0.02 * 13.2 / H,
                                          boxstyle="round,pad=0,rounding_size=0.003", facecolor=COL[st], edgecolor="none",
                                          transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.019, ly, LAB[st], fontsize=10.5, va="center", color="#16201d")
        lx += 0.095
    fig.text(0.49, ly + 0.11 / H, "22 OCT = tile added or re-annotated from a 22 October lane.  F1-F3 = rebuild_2026_10_22 "
             "lanes re-examining the reds.", fontsize=9.0, va="center", color="#4d5a56")
    fig.text(0.49, ly - 0.11 / H, "Cold energy (Omega_c/Omega_b = 5.364, an input) is real gravitating mass, not a particle species.",
             fontsize=9.0, va="center", color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    mutate = "--mutate" in sys.argv[1:]
    tiles = copy.deepcopy(TILES)
    if mutate:
        tiles[7]["lanes"] = []                       # strip one tile's evidence lane: the checks must fail
    errs = check(tiles)
    print(f"{len(tiles)} tiles; {sum(t['new22'] for t in tiles)} from 22 October lanes; "
          f"{sum(1 for t in tiles if t['prev'] is not None and t['st'] != t['prev'])} recoloured vs 21 October")
    if errs:
        for e in errs:
            print("CHECK FAIL:", e)
        print("MUTATE: checks failed as required; nothing written." if mutate else "nothing written.")
        sys.exit(1)
    if mutate:
        print("MUTATE: checks did NOT catch the stripped lane")
        sys.exit(2)
    draw(tiles, OUT)
    print("all checks PASS; wrote", os.path.relpath(OUT, os.path.dirname(HERE)))


if __name__ == "__main__":
    main()
