#!/usr/bin/env python3
"""The Crispy Fried Chicken status board, 23 October 2026 (afternoon). Plot only.

Every tile restates a verdict recorded in campaign_fresh_gravity/LEDGER.md, THEORY_CANONICAL_2026-10-18.md, a committed
lane of 22 October (doors_push_2026_10_22/, covariant_push_2026_10_22/, summarised in
covariant_push_2026_10_22/THEORY_V3_DRAFT.md), or a committed rebuild lane of 22-23 October (rebuild_2026_10_22/: F1,
F2, F3, G1, G2, H1, H2, H3 overnight; I1, J1, K1 on 23 October; the v4 candidate is THEORY_V3_DRAFT.md section 1b),
or C7's step N (covariant_push_2026_10_22/C7_aest_class/, committed 23 October). Layout and colours follow the
22 October board (kept as explainers/img/status_board_2026-10-22.png); the 23 October morning board is kept as
explainers/img/status_board_2026-10-23am.png.

Re-scoring rule for this board: a tile changes colour only if a committed 22-23 October lane changes it AND the recolour
is listed in RECOLOURS with that lane as evidence; nothing turns green without a committed lane that passes it;
unresolved reds stay red. Each tile records its 22 October colour (`prev`, None for a tile new on 23 October) and its
23 October morning colour (`am`; defaults to `prev`, None for a tile new this afternoon), so the checks below can
enforce that rule against both earlier boards.

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
# Lane ids with a result committed 22-23 October: rebuild_2026_10_22/ (F1-F3, G1-G2, H1-H3 overnight; I1, J1, K1 on
# 23 October) and C7 (step N, covariant_push_2026_10_22/C7_aest_class/, committed 23 October).
LANE_NEW = re.compile(r"^(F[1-3]|G[12]|H[1-3]|I1|J1|K1|C7)$")
_SAME = object()


def T(col, name, st, note, lanes, prev, lab=None, new=False, am=_SAME):
    """One tile: column index, label, colour (status), note, evidence lane ids, 22 October colour, 23 OCT flag,
    23 October morning colour (defaults to the 22 October colour)."""
    return dict(col=col, name=name, st=st, note=note, lanes=list(lanes), prev=prev, lab=lab, new=new,
                am=prev if am is _SAME else am)


TILES = [
    # ---- column 0: the chassis (Khronon v3; AeST v4 candidate, THEORY_V3_DRAFT section 1b) ----
    T(0, "Gravity waves at light speed", "PASS", "only the 2 tensor modes propagate, at c exactly", ["C5", "C8", "CFG292"], "PASS"),
    T(0, "Health: ghosts, gradients", "COND",
      "Khronon literal form healthy; v4 AeST ghost-free at linear order (H3: the criterion that flagged it also flags "
      "ordinary gravity)", ["C5", "H3"], "COND", new=True),
    T(0, "Leaf problem well-posed", "COND", "weak field: elliptic, unique; strong fields open", ["C8"], "COND"),
    T(0, "Causality: criterion A / B", "COND", "instantaneous constraints; faster-than-light signal ~1e-46 m/s^2", ["C5", "C8"],
      "COND", lab="B met, A violated"),
    T(0, "v4 well-posedness", "FAIL",
      "ill-posed where the aether twists (off symmetry); closed signal loops; no completion found", ["I1"], None,
      new=True, am=None),
    T(0, "Lapse condition, realistic matter", "PASS", "all but extreme GRB jets (older chassis lane)", ["CFG312"], "PASS"),
    T(0, "Binary pulsars + GW170817", "PASS", "no radiative channel; <= 3e-14 of double-pulsar error", ["C8", "CFG291", "CFG311"], "PASS"),
    T(0, "Solar system + Cassini (screened)", "PASS", "Q2 2.8e7-5.1e9 inside bound at L* 24-90 pc; Mars 0.17", ["D7d", "C6"], "PASS"),
    T(0, "Unscreened law vs Cassini", "FAIL", "control: screening switched off; fails 2.4-5.2x, so L* > 0 is required",
      ["E2", "D7c"], "FAIL", lab="fails - control (mechanism off)"),
    T(0, "Strong coupling", "COND", "bounded pass", ["XC1", "XC3"], "COND"),
    T(0, "Matter conservation (G9)", "PASS", "Bianchi identity holds; grad T = 0", ["CFG329"], "PASS"),
    T(0, "Structural order (G0)", "COND", "no ghost; elliptic solvability open", ["CFG329"], "COND"),
    T(0, "Zero-field nonlinear, ungated", "FAIL", "chassis only; B switch off there", ["CFG358"], "FAIL"),
    T(0, "Black holes (EHT, LIGO ringdown)", "COND", "hidden mild inner-horizon defect", ["CFG318", "CFG319"], "COND"),
    # ---- column 1: galaxies ----
    T(1, "Rotation curves (SPARC RAR)", "PASS", "rms 0.101 / 0.099 dex; no rotator has an excess", ["CFG695", "CFG919"], "PASS"),
    T(1, "Local a0 from MeerKAT", "PASS", "0.9-1.4e-10, matches SPARC", ["CFG301", "CFG309"], "PASS"),
    T(1, "Isolated-galaxy lensing, inner", "PASS", "supply suffices <= 0.31 Mpc; blue lenses A 1.016", ["CFG804", "CFG829", "CFG840", "CFG902"], "PASS"),
    T(1, "Isolated-galaxy lensing, all radii", "UNDEC",
      "F2: frozen fail not robust (isolation leaks hosts); old +100 came from the supply edge, which v3/v4 lack",
      ["CFG902", "CFG903", "F2"], "FAIL", new=True, am="UNDEC"),
    T(1, "Tidal dwarfs, NGC 1052-DF2/DF4", "COND", "at Newton, if they captured no cold energy", ["CFG936", "CFG939"], "COND"),
    T(1, "Outer globulars: L* floor", "COND", "L* >= 21.7 / 22.9 pc (SPS M/L); unscreened law excluded", ["D10"], "COND"),
    T(1, "Globulars + ownership rule", "COND", "Newton ~1.6 sigma; 3 of 4 pops", ["CFG332", "CFG333"], "COND"),
    T(1, "Central ellipticals (SLUGGS)", "UNDEC", "~3 sigma with measured tracers", ["CFG528b"], "UNDEC"),
    T(1, "Galaxy groups (BFJR)", "PASS", "consistent supply closes", ["CFG540", "CFG543"], "PASS"),
    T(1, "MW vertical force (round rule)", "PASS", "beats MOND phantom disc 32/32", ["CFG516"], "PASS"),
    T(1, "MW outer slope (Gaia)", "UNDEC", "3-5 sigma steeper; NFW too; DR4 decides", ["CFG532b", "CFG533"], "UNDEC"),
    # ---- column 2: the excess family ----
    T(2, "Dwarf satellites vs screened law", "FAIL",
      "+0.89 dex over screened prediction; G2: pre-infall retention fails natively", ["E3", "E6", "G2"], "FAIL", new=True),
    T(2, "Dwarf cold supply (chemistry)", "COND", "own [Fe/H] gives enough supply, if zeta = 1 winds", ["E6"], "COND"),
    T(2, "Cluster cores (318 eRASS1)", "FAIL",
      "F1 rebuild: real failure, x1.68-1.85 / x1.54-1.70, Z ~ +5-6; H2: AeST dust wrong shape", ["CFG687", "F1", "H2"],
      "FAIL", new=True),
    T(2, "Coma ultra-diffuse galaxies", "UNDEC", "+0.33 dex over the law, 2.4-2.6 sigma, fragile", ["CFG933", "CFG948"], "UNDEC"),
    T(2, "Red (early-type) lenses", "COND", "an IMF alpha-sigma relation removes it, if discs stay near Chabrier",
      ["CFG926"], "COND"),
    T(2, "One selector for the family", "OPEN",
      "J1 potential-depth selector fails; K1 braneworld Weyl term fails (tidal-charge form closest on clusters)",
      ["CFG914", "CFG919", "CFG921", "CFG928", "J1", "K1"], "OPEN", new=True),
    # ---- column 3: cosmology and a0 over time ----
    T(3, "a0(z): native band vs a0 ~ H(z)", "UNDEC", "own BAO ruler band; data cannot decide yet", ["CFG689", "PAPER38"], "UNDEC"),
    T(3, "High-z on halo-free inputs", "UNDEC", "RC100 on the flat line", ["CFG303"], "UNDEC"),
    T(3, "CRISTAL z~5 / ALESS 122.1", "UNDEC", "stress tests: not robust", ["CFG307", "CFG308"], "UNDEC"),
    T(3, "Cosmic shear, native inputs", "COND", "KiDS CONSISTENT on both footings; engine has no parent",
      ["CFG654-A2", "CFG654-A3", "CFG909"], "COND"),
    T(3, "Native shear rerun (CFG960)", "OPEN", "1024^3 running past its old failure point; no verdict", ["CFG960"], "OPEN",
      lab="open: running"),
    T(3, "Native CMB (patched CLASS)", "OPEN", "validated vs CLASS to 2e-6; spectra not yet run", ["C7", "C2"], "OPEN"),
    T(3, "CMB lensing (Planck PR4)", "UNDEC", "SAFE; CONSISTENT only under post-hoc A1; low power", ["CFG917", "CFG927"], "UNDEC"),
    T(3, "Growth, zero-knob supply rule", "FAIL",
      "old settling engine; F3/G1: belongs to the settling rules (not v3/v4); excess grows with resolution",
      ["CFG555", "CFG556", "F3", "G1"], "FAIL", new=True),
    T(3, "Linear growth, v3 Khronon", "FAIL", "F3: J'(0) = -1 removes the linear Newtonian term; empty mu_K window",
      ["F3"], None, new=True, am="FAIL"),
    T(3, "Linear growth, v4 AeST", "FAIL",
      "runs away on FRW (P/P_ΛCDM 10²–10⁴¹ by 10 h/Mpc) for the dust shape tried; early-K escape untested",
      ["C7", "H1", "H3"], None, new=True, am="COND"),
    T(3, "Structure growth, chassis alone", "FAIL", "~7x too fast; CMB lensing excludes", ["L341"], "FAIL"),
    T(3, "ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN", "harness ready, 3 kernels; expected unscorable", ["CFG806-U4", "CFG809", "CFG942", "D4"],
      "OPEN"),
    T(3, "Gaia DR4 wide binaries (Dec)", "OPEN", "screened gamma-1 ~ 8e-6 vs AQUAL 1.167 / 1.199", ["C6", "E2", "D2", "CFG943"], "OPEN"),
    T(3, "Gaia DR4 MW predictions", "OPEN", "sealed 10-10", ["CFG553"], "OPEN"),
    T(3, "The owner's wave a0(z) idea", "OPEN", "being tested, no result yet", ["CFG956", "CFG957"], "OPEN"),
    # ---- column 4: the deep 'why' and the parent ----
    T(4, "Why kappa = 1/2", "OPEN", "fitted, 0.417 ± 0.095; no horizon construction gives it", ["CFG493", "CFG894", "D5"], "OPEN",
      lab="open: fitted"),
    T(4, "Stiffness length L*", "OPEN", "new fitted constant; floor ~22 pc, edge ~90 pc", ["C3", "D10"], "OPEN",
      lab="open: fitted"),
    T(4, "What sets the cold-mass amount", "OPEN", "dust abundance is an initial condition; 5.364 an input",
      ["C2", "C4", "CFG886"], "OPEN", lab="open: fitted"),
    T(4, "Ownership from an action", "OPEN", "the label sector has no action", ["CFG945", "CFG950", "CFG953"], "OPEN"),
    T(4, "Law + a^1 growth + no EFE, local", "FAIL",
      "no-go stands; v4 evades by having an EFE; its growth is linear-conditional (H1)",
      ["CFG941", "CFG944", "CFG946", "CFG947", "F3", "H1"], "FAIL", new=True),
    T(4, "Physical parent of the shear engine", "OPEN", "3 tried: LDT, SCT fail clusters; no kinetic parent",
      ["CFG951", "CFG954", "CFG955"], "OPEN", lab="open: none known"),
    T(4, "Energy books of settling", "OPEN", "not conserved; a repair needs new physics", ["CFG932", "CFG935"], "OPEN"),
    T(4, "Radiative stability (G12)", "COND", "needs UV new physics <~1e9 GeV", ["CFG320"], "COND"),
    T(4, "Covariant completion", "FAIL",
      "trilemma: screening needs γ_L; γ_L well-posed only untwisted; untwisted (v3) fails growth; open: native "
      "nonlinear v3 run", ["I1", "C7", "F3"], None, new=True, am=None),
]

# Reds that must stay red until a committed rebuild lane says otherwise.
# 23 October: "Isolated-galaxy lensing, all radii" was removed from this list because rebuild lane F2
# (rebuild_2026_10_22/F2_outer_lensing/) found its frozen REAL FAILURE not robust (UNDECIDABLE: the old +100 came from
# the supply edge, which v3/v4 lack, and the strict isolated sample leaks hosts). It is recoloured to UNDEC via RECOLOURS.
MUST_STAY_RED = ["Cluster cores (318 eRASS1)", "Growth, zero-knob supply rule", "Law + a^1 growth + no EFE, local",
                 "Dwarf satellites vs screened law", "Linear growth, v3 Khronon", "Linear growth, v4 AeST",
                 "v4 well-posedness", "Covariant completion"]
# Every permitted recolour on this board: tile -> (earlier colour, new colour, evidence lane that justifies it).
# The earlier colour is the 22 October colour (F2, recoloured on the 23 October morning board) or the 23 October morning
# colour (C7, recoloured this afternoon: v4's linear growth runs away on FRW for the dust shape tried).
RECOLOURS = {"Isolated-galaxy lensing, all radii": ("FAIL", "UNDEC", "F2"),
             "Linear growth, v4 AeST": ("COND", "FAIL", "C7")}
WRAP = 56     # characters per note line at fontsize 7.8
MAXL = 3      # note lines per tile


def lane_text(t):
    return "/".join(t["lanes"])


def check(tiles):
    errs = []
    for t in tiles:
        if not t["lanes"] or any(not str(x).strip() for x in t["lanes"]):
            errs.append(f"no evidence lane: {t['name']}")
        if t["st"] not in COL:
            errs.append(f"bad colour {t['st']}: {t['name']}")
        for base in dict.fromkeys(b for b in (t["prev"], t["am"]) if b is not None):   # vs 22 Oct, then 23 Oct am
            if t["st"] == base:
                continue
            if not any(LANE_NEW.match(x) for x in t["lanes"]):
                errs.append(f"colour changed without a 22-23 October lane: {t['name']}")
            rc = RECOLOURS.get(t["name"])
            if rc is None or rc[:2] != (base, t["st"]) or rc[2] not in t["lanes"]:
                errs.append(f"recolour {base}->{t['st']} not listed in RECOLOURS with its evidence lane: {t['name']}")
            if not t["new"]:
                errs.append(f"recoloured tile not flagged 23 OCT: {t['name']}")
        if t["st"] == "PASS" and (t["prev"] != "PASS" or t["am"] != "PASS"):
            errs.append(f"turned green: {t['name']} (needs a committed passing lane; refused on this board)")
        if t["prev"] is None and not t["new"]:
            errs.append(f"new tile not flagged as 23 October: {t['name']}")
        lines = textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)
        if len(lines) > MAXL:
            errs.append(f"note too long ({len(lines)} lines): {t['name']}")
    names = {t["name"]: t for t in tiles}
    for n in MUST_STAY_RED:
        if n not in names or names[n]["st"] != "FAIL":
            errs.append(f"must stay red: {n}")
    for n in RECOLOURS:
        if n not in names or names[n]["st"] != RECOLOURS[n][1]:
            errs.append(f"listed recolour not applied: {n}")
    if len(names) != len(tiles):
        errs.append("duplicate tile names")
    return errs


def draw(tiles, out):
    ncol = len(COLUMNS)
    nmax = max(sum(1 for t in tiles if t["col"] == c) for c in range(ncol))
    W, H = 20.5, 2.6 + 0.94 * nmax                   # inches; each tile ~0.94 in tall as on the 22 October board
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    top_in, bot_in = 1.25, 0.95                      # header and legend bands, inches
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.25, nmax + 0.65); ax.axis("off")
    fig.text(0.015, 1 - 0.55 / H, "The Crispy Fried Chicken Status Board  ·  23 October 2026 (afternoon)", fontsize=24,
             fontweight="bold", color="#16201d")
    fig.text(0.015, 1 - 1.0 / H, "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted; footings 9.3603e-11 / 1.1312e-10 m/s^2 never "
             "pooled.  Chassis: Khronon (v3) or AeST (v4 candidate), screened by L*.  Lane ids on every tile.  "
             "The theory is incomplete.", fontsize=11.0, color="#4d5a56")
    for c, title in enumerate(COLUMNS):
        ax.text(c + 0.03, nmax + 0.4, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
        for k, t in enumerate([t for t in tiles if t["col"] == c]):
            y = nmax - 0.5 - k
            ax.add_patch(FancyBboxPatch((c + 0.03, y - 0.43), 0.93, 0.86, boxstyle="round,pad=0.0,rounding_size=0.05",
                                        facecolor=COL[t["st"]], edgecolor="none", alpha=0.93))
            ax.text(c + 0.065, y + 0.30, t["name"], fontsize=10.4, fontweight="bold", color="white", va="center")
            lab = (t["lab"] or LAB[t["st"]]).upper()
            ax.text(c + 0.065, y + 0.125, lab, fontsize=8.2, color="white", va="center", alpha=0.95)
            if t["new"]:
                ax.text(c + 0.945, y + 0.30, "23 OCT", fontsize=7.6, fontweight="bold", color="white", va="center",
                        ha="right", alpha=0.9)
            for j, ln in enumerate(textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)):
                ax.text(c + 0.065, y - 0.05 - 0.135 * j, ln, fontsize=7.8, color="white", va="center", alpha=0.97)
    lx, ly = 0.015, 0.42 / H
    for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN"):
        fig.patches.append(FancyBboxPatch((lx, ly - 0.01 * 13.2 / H), 0.014, 0.02 * 13.2 / H,
                                          boxstyle="round,pad=0,rounding_size=0.003", facecolor=COL[st], edgecolor="none",
                                          transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.019, ly, LAB[st], fontsize=10.5, va="center", color="#16201d")
        lx += 0.095
    fig.text(0.47, ly + 0.11 / H, "23 OCT = tile added, recoloured or re-annotated on 23 October "
             "(F1-F3, G1-G2, H1-H3, I1, J1, K1, C7 step N).  PAPER59: DOI 10.5281/zenodo.23585319.", fontsize=9.0,
             va="center", color="#4d5a56")
    fig.text(0.47, ly - 0.11 / H, "Cold energy (Omega_c/Omega_b = 5.364, an input) is real gravitating mass, not a particle species.",
             fontsize=9.0, va="center", color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    mutate = "--mutate" in sys.argv[1:]
    tiles = copy.deepcopy(TILES)
    if mutate:
        next(t for t in tiles if t["name"] == "Unscreened law vs Cassini")["lanes"] = []   # strip one tile's lane
    errs = check(tiles)
    print(f"{len(tiles)} tiles; {sum(t['new'] for t in tiles)} added or re-annotated on 23 October; "
          f"{sum(1 for t in tiles if t['prev'] is not None and t['st'] != t['prev'])} recoloured vs 22 October; "
          f"{sum(1 for t in tiles if t['am'] is not None and t['st'] != t['am'])} recoloured vs 23 October morning")
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
