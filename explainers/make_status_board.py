#!/usr/bin/env python3
"""The Crispy Fried Chicken status board, 23 October 2026: current theory v3 only. Plot only.

The board shows ONLY the current best theory, v3 (covariant_push_2026_10_22/THEORY_V3_DRAFT.md sections 1-3: the
Blanchet-Skordis Khronon in its literal form + covector P + one stiffness term -(gamma_L/2)(D.P)^2 + BS K(Q) dust; static
limit AQUAL with mu = x/(1+x) and an external-field effect; screening L* >= 21.7 / 22.9 pc; no settling, supply,
catchment, ownership or round rules). Every tile of the 23 October afternoon board was classified against v3 by the
read-only audit rebuild_2026_10_22/N0_board_audit/AUDIT.md (lane N0):

  CURRENT            (15) the evidence lane computed v3 itself: colour and note kept (N0's re-annotations applied);
  STALE              (15) computed for an older model: drawn grey, "NOT YET RECOMPUTED FOR v3"; the old result is kept
                          in the note as "was ...", and the tile names the lane that will recompute it for v3;
  OLD-MODEL ONLY     (16) tested only models v3 does not contain: removed from the board and kept, with their old
                          colours, lanes and retiring reasons, in ARCHIVE (drawn separately as
                          explainers/img/status_board_archive_retired.png);
  DATA-GATED / OPEN  (9)  kept.

23 October (evening): four grey tiles recomputed for v3 by their recompute lanes, each rerun and reproduced by the
coordinator: S1 (rebuild_2026_10_22/S1_v3_hosted_small/) dwarf satellites -> FAIL and Coma's ultra-diffuse galaxies
-> FAIL (v3's AQUAL solved in the host's field); S2 (S2_v3_lowg_lensing/) isolated-galaxy lensing inner -> CONDITIONAL
and red lenses -> CONDITIONAL. Re-annotated, colour kept: isolated lensing at all radii (P2), one selector (M2; T1
running), and the archived dwarf cold-supply tile (P1; it stays archived: v3 has no supply rule). The first v3-only
board (commit a77915b2de, image explainers/img/status_board_2026-10-23eve.png) is V3_BOARD, a fourth baseline: a grey
tile takes a colour only through a RECOLOURS step STALE -> colour naming its own recompute lane (V3_REDO).
Late evening: P4 (P4_v3_galaxy_tiles/) rotation curves -> CONDITIONAL, tidal dwarfs -> FAIL, galaxy groups -> PASS
(the lane's verdict; it was green before it was greyed, so no new green), MeerKAT re-annotated (PASS), and the MW
vertical force back from the archive (V3_ARCHIVED; only its recompute lane may return it) -> FAIL as an AQUAL disc;
Q6 (Q6_v3_class/) native CMB -> FAIL and linear growth re-annotated (FAIL). A new tile ("BBN / radiation era", Q6) is
refused by the guards (a tile on no earlier board) and is not drawn.
Night: S3 MW outer slope -> FAIL; S4's R4 (kernel nu_1) SLUGGS, high-z and CRISTAL / ALESS -> NOT DECIDABLE (classes
unchanged, so their pre-grey colour); H4 health and leaf problem COND -> FAIL; notes from S3, S4, U1, Q7, T1 and the
ALMA addendum F. Coordinator decisions: black holes and strong coupling grey -> CONDITIONAL (P3); tidal dwarfs
FAIL -> PASS (U1) through VERIFIED_GREEN, the one narrow route to a first green (lane, result commit and coordinator
rerun named; the RECOLOURS step into green must name the same lane). Radiative stability stays grey: P3 gives no
replacement for it. Notes may run to four lines (rows 1.10 in tall).

Guards (check()):
  * colours of tiles on the main board cannot change, against the 22 October, 23 October morning, 23 October
    afternoon and first v3-only (V3_BOARD) boards, without a RECOLOURS chain of steps from that colour to the current
    one, the last step's evidence lane on the tile (a CURRENT -> STALE greying is a recolour too, with evidence N0);
    no first green except through VERIFIED_GREEN; no tile of V3_BOARD leaves the board (N0's retirements are closed);
  * a tile leaves the main board only into ARCHIVE, only with N0 as the evidence lane (RETIRE_EVIDENCE), and keeps its
    23 October afternoon colour there; no tile of that board may simply vanish (PREVIOUS_BOARD);
  * every MUST_STAY_RED tile is red on the main board, or grey with "was: fails" (STALE, RECOLOURS FAIL -> STALE, N0),
    or red in ARCHIVE with evidence N0;
  * a STALE tile shows its old colour as `was` (equal to PREVIOUS_BOARD) and names one of the recompute lanes.

Run:  OMP_NUM_THREADS=1 python3 explainers/make_status_board.py            (writes explainers/img/status_board.png and
                                                                            explainers/img/status_board_archive_retired.png)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --mutate   (strips one tile's evidence lane; the
                                                                            checks must FAIL and nothing is written)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --selftest (broken cases for the guards; every one
                                                                            must be caught; nothing is written)
One core, seconds, < 0.3 GB.

kappa = 1/2 is FITTED; footings never pooled; cold energy is real gravitating mass, not a particle species;
the theory is not closed.
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
OUT_ARCHIVE = os.path.join(HERE, "img", "status_board_archive_retired.png")

COL = {"PASS": "#2f8f5b", "COND": "#d9a521", "OPEN": "#8a94a0", "FAIL": "#c4452f", "UNDEC": "#5b7fb4",
       "STALE": "#dcdfe2"}
LAB = {"PASS": "pass", "COND": "conditional", "OPEN": "open", "FAIL": "fails", "UNDEC": "not decidable yet",
       "STALE": "not yet recomputed for v3"}
INK = {"STALE": "#2b3236"}          # text colour on a tile (white unless listed)
COLUMNS = ["Relativistic theory (the chassis)", "Galaxies", "The excess family (open)",
           "Cosmology and a0 over time", "The deep 'why' and the parent"]
# Lane ids with a result committed 22-23 October: rebuild_2026_10_22/ (F1-F3, G1-G2, H1-H3 overnight; I1, J1, K1 and
# the board audit N0 on 23 October) and C7 (step N, covariant_push_2026_10_22/C7_aest_class/, committed 23 October).
# 23 October evening: S1, S2 (N0 recompute batches R1, R2), P1, P2 and M2; late evening: P4 and Q6; night: S3, S4, P3,
# H4, U1, Q7 and T1 (rebuild_2026_10_22/).
LANE_NEW = re.compile(r"^(F[1-3]|G[12]|H[1-4]|I1|J1|K1|C7|N0|S[1-4]|P[1-4]|M2|Q[67]|U1|T1)$")
RETIRE_EVIDENCE = {"N0"}           # the only lane allowed to move a tile off the board into ARCHIVE
# N0's recompute batches (AUDIT.md, "Recompute batches to launch") and the lane id each one runs under.
RECOMPUTE = {"R1": "S1", "R2": "S2", "R3": "S3", "R4": "S4", "R5": "P3", "R6": "S4", "R7": "Q6"}
# tiles whose recompute the coordinator assigned to lane P4 (galaxy tiles), overriding the batch default
REDO_BY_TILE = {"Rotation curves (SPARC RAR)": "P4", "Local a0 from MeerKAT": "P4", "Galaxy groups (BFJR)": "P4",
                "MW vertical force (round rule)": "P4", "Tidal dwarfs, NGC 1052-DF2/DF4": "P4"}
_SAME = object()

# The 23 October afternoon board (commit 1205446ebc; image kept as explainers/img/status_board_2026-10-23pm.png):
# every tile and its colour. Each one must be on this board (possibly renamed, see RENAMES) or in ARCHIVE.
PREVIOUS_BOARD = {
    'Gravity waves at light speed': 'PASS', 'Health: ghosts, gradients': 'COND', 'Leaf problem well-posed': 'COND',
    'Causality: criterion A / B': 'COND', 'v4 well-posedness': 'FAIL', 'Lapse condition, realistic matter': 'PASS',
    'Binary pulsars + GW170817': 'PASS', 'Solar system + Cassini (screened)': 'PASS', 'Unscreened law vs Cassini': 'FAIL',
    'Strong coupling': 'COND', 'Matter conservation (G9)': 'PASS', 'Structural order (G0)': 'COND',
    'Zero-field nonlinear, ungated': 'FAIL', 'Black holes (EHT, LIGO ringdown)': 'COND',
    'Rotation curves (SPARC RAR)': 'PASS', 'Local a0 from MeerKAT': 'PASS', 'Isolated-galaxy lensing, inner': 'PASS',
    'Isolated-galaxy lensing, all radii': 'UNDEC', 'Tidal dwarfs, NGC 1052-DF2/DF4': 'COND',
    'Outer globulars: L* floor': 'COND', 'Globulars + ownership rule': 'COND', 'Central ellipticals (SLUGGS)': 'UNDEC',
    'Galaxy groups (BFJR)': 'PASS', 'MW vertical force (round rule)': 'PASS', 'MW outer slope (Gaia)': 'UNDEC',
    'Dwarf satellites vs screened law': 'FAIL', 'Dwarf cold supply (chemistry)': 'COND',
    'Cluster cores (318 eRASS1)': 'FAIL', 'Coma ultra-diffuse galaxies': 'UNDEC', 'Red (early-type) lenses': 'COND',
    'One selector for the family': 'OPEN', 'a0(z): native band vs a0 ~ H(z)': 'UNDEC',
    'High-z on halo-free inputs': 'UNDEC', 'CRISTAL z~5 / ALESS 122.1': 'UNDEC', 'Cosmic shear, native inputs': 'COND',
    'Native shear rerun (CFG960)': 'OPEN', 'Native CMB (patched CLASS)': 'OPEN', 'CMB lensing (Planck PR4)': 'UNDEC',
    'Growth, zero-knob supply rule': 'FAIL', 'Linear growth, v3 Khronon': 'FAIL', 'Linear growth, v4 AeST': 'FAIL',
    'Structure growth, chassis alone': 'FAIL', 'ALMA U4 (6 Nov), GS4 (28 Nov)': 'OPEN',
    'Gaia DR4 wide binaries (Dec)': 'OPEN', 'Gaia DR4 MW predictions': 'OPEN', "The owner's wave a0(z) idea": 'OPEN',
    'Why kappa = 1/2': 'OPEN', 'Stiffness length L*': 'OPEN', 'What sets the cold-mass amount': 'OPEN',
    'Ownership from an action': 'OPEN', 'Law + a^1 growth + no EFE, local': 'FAIL',
    'Physical parent of the shear engine': 'OPEN', 'Energy books of settling': 'OPEN', 'Radiative stability (G12)': 'COND',
    'Covariant completion': 'FAIL',
}
# Tiles renamed on this board: new name -> (name on the 23 October afternoon board, evidence lane).
RENAMES = {"Cluster cores (326 eRASS1)": ("Cluster cores (318 eRASS1)", "N0")}   # N0 row 28: F1 used 326 clusters
# The first v3-only board (23 October, commit a77915b2de; image kept as explainers/img/status_board_2026-10-23eve.png):
# every tile and its colour ("STALE" = grey, not yet recomputed for v3). No tile of it may leave the board.
V3_BOARD = {
    'Gravity waves at light speed': 'PASS', 'Health: ghosts, gradients': 'COND', 'Leaf problem well-posed': 'COND',
    'Causality: criterion A / B': 'COND', 'Binary pulsars + GW170817': 'PASS', 'Solar system + Cassini (screened)': 'PASS',
    'Unscreened law vs Cassini': 'FAIL', 'Strong coupling': 'STALE', 'Matter conservation (G9)': 'PASS',
    'Black holes (EHT, LIGO ringdown)': 'STALE', 'Rotation curves (SPARC RAR)': 'STALE', 'Local a0 from MeerKAT': 'PASS',
    'Isolated-galaxy lensing, inner': 'STALE', 'Isolated-galaxy lensing, all radii': 'UNDEC',
    'Tidal dwarfs, NGC 1052-DF2/DF4': 'STALE', 'Outer globulars: L* floor': 'COND', 'Central ellipticals (SLUGGS)': 'STALE',
    'Galaxy groups (BFJR)': 'STALE', 'MW outer slope (Gaia)': 'STALE', 'Dwarf satellites vs screened law': 'STALE',
    'Cluster cores (326 eRASS1)': 'FAIL', 'Coma ultra-diffuse galaxies': 'STALE', 'Red (early-type) lenses': 'STALE',
    'One selector for the family': 'OPEN', 'a0(z): native band vs a0 ~ H(z)': 'UNDEC', 'High-z on halo-free inputs': 'STALE',
    'CRISTAL z~5 / ALESS 122.1': 'STALE', 'Native CMB (patched CLASS)': 'STALE', 'Linear growth, v3 Khronon': 'FAIL',
    'ALMA U4 (6 Nov), GS4 (28 Nov)': 'OPEN', 'Gaia DR4 wide binaries (Dec)': 'OPEN', 'Gaia DR4 MW predictions': 'OPEN',
    "The owner's wave a0(z) idea": 'OPEN', 'Why kappa = 1/2': 'OPEN', 'Stiffness length L*': 'OPEN',
    'What sets the cold-mass amount': 'OPEN', 'Law + a^1 growth + no EFE, local': 'FAIL', 'Radiative stability (G12)': 'STALE',
    'Covariant completion': 'FAIL',
}
# The recompute lane each grey tile of V3_BOARD named; only that lane may give it a colour.
V3_REDO = {
    'Strong coupling': 'P3', 'Black holes (EHT, LIGO ringdown)': 'P3', 'Rotation curves (SPARC RAR)': 'P4',
    'Isolated-galaxy lensing, inner': 'S2', 'Tidal dwarfs, NGC 1052-DF2/DF4': 'P4', 'Central ellipticals (SLUGGS)': 'S4',
    'Galaxy groups (BFJR)': 'P4', 'MW outer slope (Gaia)': 'S3', 'Dwarf satellites vs screened law': 'S1',
    'Coma ultra-diffuse galaxies': 'S1', 'Red (early-type) lenses': 'S2', 'High-z on halo-free inputs': 'S4',
    'CRISTAL z~5 / ALESS 122.1': 'S4', 'Native CMB (patched CLASS)': 'Q6', 'Radiative stability (G12)': 'P3',
}
# The 16 tiles archived on the first v3-only board. One returns to the board only when its recompute lane
# (REDO_BY_TILE) has computed it for v3: that lane must be on the tile and must be the last RECOLOURS step.
V3_ARCHIVED = {
    'v4 well-posedness', 'Lapse condition, realistic matter', 'Structural order (G0)', 'Zero-field nonlinear, ungated',
    'Globulars + ownership rule', 'MW vertical force (round rule)', 'Dwarf cold supply (chemistry)',
    'Cosmic shear, native inputs', 'Native shear rerun (CFG960)', 'CMB lensing (Planck PR4)',
    'Growth, zero-knob supply rule', 'Linear growth, v4 AeST', 'Structure growth, chassis alone',
    'Ownership from an action', 'Physical parent of the shear engine', 'Energy books of settling',
}


def T(col, name, st, note, lanes, prev, lab=None, new=False, am=_SAME):
    """One CURRENT or DATA-GATED / OPEN tile: column index, label, colour, note, evidence lane ids, 22 October colour,
    23 OCT flag, 23 October morning colour (defaults to the 22 October colour)."""
    return dict(col=col, name=name, st=st, note=note, lanes=list(lanes), prev=prev, lab=lab, new=new,
                am=prev if am is _SAME else am, was=None, redo=None)


def S(col, name, was, old_note, lanes, batch):
    """One STALE tile (N0: computed for an older model): drawn grey; `was` is its old colour, `old_note` its old
    result, `batch` the N0 recompute batch (-> lane id in RECOMPUTE). For all 15 the 22 October, 23 October morning and
    23 October afternoon colours were the same, so prev = am = was; PREVIOUS_BOARD is what check() trusts."""
    return dict(col=col, name=name, st="STALE", note=f"was {LAB[was]}: {old_note}", lanes=list(lanes) + ["N0"],
                prev=was, am=was, lab=None, new=True, was=was, redo=REDO_BY_TILE.get(name, RECOMPUTE.get(batch)), batch=batch)


def A(col, name, st, note, lanes, why, v3, ev="N0"):
    """One ARCHIVED tile (N0: OLD-MODEL ONLY): its 23 October afternoon colour `st`, old note and lanes, the reason it
    left the board (`why`), its v3 counterpart (`v3`) and the evidence lane that retired it (`ev`)."""
    return dict(col=col, name=name, st=st, note=note, lanes=list(lanes), why=why, v3=v3, ev=ev)


TILES = [
    # ---- column 0: the chassis (v3 = Khronon literal form + P + gamma_L + BS dust) ----
    T(0, "Gravity waves at light speed", "PASS", "only the 2 tensor modes propagate, at c exactly", ["C5", "C8", "CFG292"], "PASS"),
    # H4 (23 October night): COND -> FAIL
    T(0, "Health: ghosts, gradients", "FAIL",
      "gradient instability wherever ρ_τ < 0 (every two-body saddle; EFE lobes): Γ = L★k√(2πG|ρ_τ|), unbounded, "
      "driven by the γ_L screening term; Solar System healthy", ["C5", "H4"], "COND", new=True),
    T(0, "Leaf problem well-posed", "FAIL", "ILL-POSED at saddles (H4); C8's leaf result holds only where ρ_τ ≥ 0",
      ["C8", "H4"], "COND", new=True),
    T(0, "Causality: criterion A / B", "COND", "instantaneous constraints; faster-than-light signal ~1e-46 m/s^2", ["C5", "C8"],
      "COND", lab="B met, A violated"),
    T(0, "Binary pulsars + GW170817", "PASS", "no radiative channel; <= 3e-14 of double-pulsar error", ["C8"], "PASS",
      new=True),
    T(0, "Solar system + Cassini (screened)", "PASS",
      "Q2 2.8e7-5.1e9 inside bound at L* 24-90 pc; Mars 0.17; C6's frozen rule UNDECIDED on one rounding check",
      ["C6"], "PASS", new=True),
    T(0, "Unscreened law vs Cassini", "FAIL", "control: screening switched off; fails 2.4-5.2x, so L* > 0 is required",
      ["E2"], "FAIL", lab="fails - control (mechanism off)", new=True),
    # P3 (v3, 23 October night): was grey (old COND: bounded pass, on the filtered C-H/K chassis)
    T(0, "Strong coupling", "COND",
      "estimate: loop factor ≤ 1.3e-3; margin only 1.7× in k at 38.6 μm; sub-5 μm tests would probe it", ["P3"],
      "COND", new=True),
    T(0, "Matter conservation (G9)", "PASS", "Bianchi identity, grad T = 0: holds for any diffeomorphism-invariant "
      "action, v3 included", ["CFG329", "C4"], "PASS", new=True),
    # P3 (v3): was grey (old COND: hidden mild inner-horizon defect, older chassis)
    T(0, "Black holes (EHT, LIGO ringdown)", "COND",
      "PASS for static non-rotating holes (shifts ≤ 3e-11); regular holes need an infalling khronon; rotating/moving "
      "holes open", ["P3"], "COND", new=True),
    # ---- column 1: galaxies ----
    # P4 (recomputed for v3, 23 October late evening): was grey (old result PASS: rms 0.101 / 0.099 dex, algebraic law)
    T(1, "Rotation curves (SPARC RAR)", "COND",
      "one Υ per galaxy, EFE solved (109): rms 0.054/0.054 dex; median Υ 0.52 / 0.44 (alt below the 0.50–0.80 "
      "window); χ² line fails both (63–64% acceptable; ν_mono same)", ["P4"], "PASS", new=True),
    T(1, "Local a0 from MeerKAT", "PASS", "a0 1.31e-10 vs SPARC same recipe 1.21e-10 (+0.033 dex, line 0.15)",
      ["CFG301", "CFG309", "P4"], "PASS", new=True),
    # S2 (recomputed for v3, 23 October evening): was grey (old result PASS: supply suffices <= 0.31 Mpc, A 1.016)
    T(1, "Isolated-galaxy lensing, inner", "COND",
      "v3 blue A 0.88 / 0.80; EFE ≤ 0.004 here; decided by hot CGM and M★; before S4's μ_K² term", ["S2"], "PASS",
      new=True),
    T(1, "Isolated-galaxy lensing, all radii", "UNDEC",
      "spectroscopic isolation (P2): N too small (needs ~22–26k lenses); data favour the catalogue's EFE; "
      "μ_K² to add (S4)",
      ["CFG902", "CFG903", "F2", "P2"], "FAIL", new=True, am="UNDEC"),
    # P4 (v3): was grey (old result COND: at Newton if they captured no cold energy; host EFE untested)
    # U1 (VERIFIED_GREEN): FAIL -> PASS by a new derivation (T3), not a re-scored number
    T(1, "Tidal dwarfs, NGC 1052-DF2/DF4", "PASS",
      "static AQUAL (P4) read −0.59 dex; v3's own dynamics (T3) makes hosted systems dust-free → Newtonian: TDGs "
      "+0.055 ± 0.114 dex, DF2/DF4 +0.30/−0.24 ln; no knob", ["P4", "U1"], "COND",
      lab="pass (U1: v3's own dynamics)", new=True),
    T(1, "Outer globulars: L* floor", "COND", "L* >= 21.7 / 22.9 pc (SPS M/L); unscreened law excluded", ["D10"], "COND"),
    # S4 R4 (v3 kernel nu_1, 23 October night): was grey (old UNDEC: ~3 sigma with measured tracers, nu_mono); class
    # GENUINE TENSION unchanged, drawn in its pre-grey colour
    T(1, "Central ellipticals (SLUGGS)", "UNDEC", "tension 2.8σ → 3.1σ (3.3σ without ownership)", ["CFG528b", "S4"],
      "UNDEC", new=True),
    # P4 (v3): was grey (old result PASS: supply closes; CFG543 no-edge row +0.010 / -0.010, EFE unchecked)
    T(1, "Galaxy groups (BFJR)", "PASS",
      "isolated: +0.010/−0.010 dex (Z ±0.31), no supply rule; ABOVE LAW if g_e ≥ 0.03 a0 (Z 4.7/4.5); no group "
      "field on disk", ["P4"], "PASS", lab="pass (lane verdict, isolated)", new=True),
    # P4 (v3): back from the archive (old result PASS for the round rule, retired by N0), computed for v3 as an AQUAL disc
    T(1, "MW vertical force (round rule)", "FAIL",
      "v3 has no round rule; AQUAL disc K_z,1.1 92.3/96.9 vs 66.4 ± 2.2, χ² 178/251 vs 67.5; all four baryon models",
      ["P4"], "PASS", new=True),
    # S3 (v3, 23 October night): was grey (old result UNDEC: 3-5 sigma steeper; round rule, no AQUAL, no EFE)
    T(1, "MW outer slope (Gaia)", "FAIL",
      "SHAPE EXCLUDED: law slope −0.126/−0.114 vs data −0.325, Z −4.37/−4.62; ALG→ν₁→AQUAL disc→EFE all fail",
      ["S3"], "UNDEC", new=True),
    # ---- column 2: the excess family ----
    # S1 (recomputed for v3, 23 October evening): was grey (old result FAIL: +0.89 dex over the screened law, no EFE)
    T(2, "Dwarf satellites vs screened law", "FAIL",
      "v3, host EFE solved: +1.33/+1.30 dex (L★ floor), +1.72/+1.68 at 90 pc; supply (P1), no binding; U1: the "
      "theorem (T3) that passes the tidal dwarfs leaves them dust-free: +2.00/+1.99 dex; STRUCTURAL",
      ["S1", "P1", "U1"], "FAIL", new=True),
    T(2, "Cluster cores (326 eRASS1)", "FAIL",
      "F1 rebuild: real failure, x1.68-1.85 / x1.54-1.70, Z ~ +5-6; S4: no allowed μ_K fixes them (0 of 1,804 cells); "
      "small μ_K leaves clusters unchanged, large μ_K wrecks galaxies first", ["CFG687", "F1", "S4"], "FAIL", new=True),
    # S1 (v3): was grey (old result UNDEC: +0.33 dex over the isolated law, Coma's field not applied)
    T(2, "Coma ultra-diffuse galaxies", "FAIL",
      "in Coma's field +1.12/+1.08 dex, z +4.3–4.7 / +4.1–4.5; isolated only 1.65/1.45σ off; U1: +1.41 dex, z 5.4 "
      "under v3 dynamics; STRUCTURAL", ["S1", "U1"], "UNDEC",
      new=True),
    # S2 (v3): was grey (old result COND: an IMF alpha-sigma relation removes it, no EFE)
    T(2, "Red (early-type) lenses", "COND", "inventory 1.31/1.20 short; + CFG667 + IMF α–σ → 1.02/0.93",
      ["S2", "CFG667", "CFG926"], "COND", new=True),
    T(2, "One selector for the family", "OPEN",
      "J1, K1, M2 selectors fail; T1: one EFE strength does not fit (p 0.023/0.014); Coma wants weak, P2 lensing "
      "strong; satellites +0.9 dex even at ε = 0", ["CFG914", "CFG919", "CFG921", "CFG928", "J1", "K1", "M2", "T1"],
      "OPEN", new=True),
    # ---- column 3: cosmology and a0 over time ----
    T(3, "a0(z): native band vs a0 ~ H(z)", "UNDEC", "own BAO ruler band; data cannot decide yet", ["CFG689", "PAPER38"], "UNDEC"),
    # S4 R4 (v3 kernel nu_1): was grey (old UNDEC); classes unchanged
    T(3, "High-z on halo-free inputs", "UNDEC", "all six CFG303 classes unchanged; s★ ≤ 0.1 dex", ["CFG303", "S4"],
      "UNDEC", new=True),
    T(3, "CRISTAL z~5 / ALESS 122.1", "UNDEC", "NOT ROBUST / NOT DISCRIMINATING unchanged", ["CFG307", "CFG308", "S4"],
      "UNDEC", new=True),
    # Q6 (v3): was grey (old result OPEN: the patch is AeST (v4); v3 at finite mu_K not run)
    T(3, "Native CMB (patched CLASS)", "FAIL",
      "literal v3: no radiation era (stiff a^-6 term of BS's K); on dust, plik-lite Δχ² vs ΛCDM +13891 at the cap, "
      "+18.7 at μ_K 2542; Q7: BS25's DBI K fixes BBN only, R_B 0.26–0.32; BS ran no Boltzmann code", ["Q6", "Q7"], "OPEN", new=True),
    T(3, "Linear growth, v3 Khronon", "FAIL",
      "Boltzmann σ8 0.061 at the cap (F3 ODE 0.391); 5% growth needs μ_K > 2542; cause is the BS cap (M1); Q7: BS25's "
      "DBI K fixes BBN only; growth R_B 0.26–0.32; BS ran no Boltzmann code", ["F3", "M1", "Q6", "Q7"], None,
      new=True, am="FAIL"),
    T(3, "ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN",
      "harness ready, expected unscorable; v3 kernel sealed as AG4e; addendum F filed (f6f0ba66a4): v3 AQUAL-disc "
      "reading; harness v3aq MOCK-tested",
      ["CFG806-U4", "CFG809", "CFG942", "D4", "AG4e"], "OPEN", new=True),
    T(3, "Gaia DR4 wide binaries (Dec)", "OPEN", "screened gamma-1 ~ 8e-6 vs AQUAL 1.167 / 1.199", ["C6", "E2", "CFG943"],
      "OPEN", new=True),
    T(3, "Gaia DR4 MW predictions", "OPEN",
      "v3 sealed: SEALED_V3_MW_DR4.json (15b7e6ff…); new observable: EFE-driven V_c asymmetry 3/5/8 % at 20/30/60 "
      "kpc; round-rule seal (10-10) kept", ["CFG553", "S3"], "OPEN", new=True),
    T(3, "The owner's wave a0(z) idea", "OPEN", "being tested, no result yet", ["CFG956", "CFG957"], "OPEN"),
    # ---- column 4: the deep 'why' and the parent ----
    T(4, "Why kappa = 1/2", "OPEN",
      "fitted; no horizon construction gives it; S3 AQUAL discs: κ_Λ 0.499 ± 0.116, κ_crit 0.413 ± 0.096: consistent, "
      "not discriminating", ["CFG493", "CFG894", "D5", "S3"], "OPEN", lab="open: fitted", new=True),
    T(4, "Stiffness length L*", "OPEN", "new fitted constant; floor ~22 pc, edge ~90 pc", ["C3", "D10"], "OPEN",
      lab="open: fitted"),
    T(4, "What sets the cold-mass amount", "OPEN",
      "dust abundance is an initial condition; 5.364 an input; U1: held dust ≤ phantom (theorem T1); hosted systems "
      "carry none (T3)", ["C2", "C4", "CFG886", "U1"], "OPEN", lab="open: fitted", new=True),
    T(4, "Law + a^1 growth + no EFE, local", "FAIL",
      "no-go stands; v3 pays the no-EFE leg with an EFE, and its linear growth fails (F3)",
      ["CFG941", "CFG944", "CFG946", "CFG947", "F3"], "FAIL", new=True),
    S(4, "Radiative stability (G12)", "COND", "needs UV new physics <~1e9 GeV (filtered chassis)", ["CFG320"], "R5"),
    T(4, "Covariant completion", "FAIL",
      "trilemma: screening needs γ_L; γ_L well-posed only untwisted; untwisted (v3) fails growth; open: native "
      "nonlinear v3 run", ["I1", "C7", "F3"], None, new=True, am=None),
]

# The 16 OLD-MODEL ONLY tiles (N0), retired from the board with their 23 October afternoon colours.
ARCHIVE = [
    A(0, "v4 well-posedness", "FAIL", "ill-posed where the aether twists; closed signal loops", ["I1"],
      "v4 (AeST + γ_L) is not the best theory", "leaf problem well-posed (C8)"),
    A(0, "Lapse condition, realistic matter", "PASS", "all but extreme GRB jets", ["CFG312"],
      "lapse kernel of the filtered C-H/K chassis", "inside C8's convex leaf functional (optional check, P3)"),
    A(0, "Structural order (G0)", "COND", "no ghost; elliptic solvability open", ["CFG329"],
      "G0 gate of the filtered C-H/K chassis (a duplicate)", "health (C5) + leaf problem (C8)"),
    A(0, "Zero-field nonlinear, ungated", "FAIL", "chassis only; B switch off there", ["CFG358"],
      "ungated nu_mono chassis on open FRW", "L1's native nonlinear run"),
    A(1, "Globulars + ownership rule", "COND", "Newton ~1.6 sigma; 3 of 4 pops", ["CFG332", "CFG333"],
      "ownership classes; v3 has no ownership", "outer globulars, L* floor (D10)"),
    A(2, "Dwarf cold supply (chemistry)", "COND",
      "own [Fe/H] supply if zeta = 1 winds; P1 MDF test: supply confirmed for the median, not 2σ-robust", ["E6", "P1"],
      "catchment supply; v3's dust has no supply or capture rule", "dust capture into satellites (L1)"),
    A(3, "Cosmic shear, native inputs", "COND", "KiDS CONSISTENT on both footings; engine has no parent",
      ["CFG654-A2", "CFG654-A3", "CFG909"], "theory-v2 engine (switch, catchment, edge, settling)",
      "F3's linear S8 and L1's native run"),
    A(3, "Native shear rerun (CFG960)", "OPEN", "SCT-M engine; since scored: SC1x FAILS, KiDS excluded, dchi2 +47.28",
      ["CFG960"], "the SCT-M engine, not v3", "L1's native run"),
    A(3, "CMB lensing (Planck PR4)", "UNDEC", "SAFE; CONSISTENT only under post-hoc A1; low power",
      ["CFG917", "CFG927"], "theory-v2 runs", "C_L^phiphi from the v3 CLASS patch (Q6)"),
    A(3, "Growth, zero-knob supply rule", "FAIL", "old settling engine; excess grows with resolution",
      ["CFG555", "CFG556", "F3", "G1"], "the settling engine; v3 has no settling", "linear growth, v3 Khronon (on board)"),
    A(3, "Linear growth, v4 AeST", "FAIL", "runs away on FRW for the dust shape tried", ["C7", "H1", "H3"],
      "v4 is not the best theory", "linear growth, v3 Khronon (on board)"),
    A(3, "Structure growth, chassis alone", "FAIL", "~7x too fast; CMB lensing excludes", ["L341"],
      "C-H/K chassis with an unfloored boost", "linear growth, v3 Khronon (on board)"),
    A(4, "Ownership from an action", "OPEN", "the label sector has no action", ["CFG945", "CFG950", "CFG953"],
      "label sector; v3 has no ownership and needs none", "none needed"),
    A(4, "Physical parent of the shear engine", "OPEN", "3 tried: LDT, SCT fail clusters; no kinetic parent",
      ["CFG951", "CFG954", "CFG955"], "parent of the theory-v2 engine; v3 is not it", "none needed"),
    A(4, "Energy books of settling", "OPEN", "not conserved; a repair needs new physics", ["CFG932", "CFG935"],
      "v3 has no settling", "none needed"),
]

# Reds that must stay red until a committed lane says otherwise. 23 October (afternoon): "Isolated-galaxy lensing, all
# radii" left this list on the morning board (F2, recoloured to UNDEC via RECOLOURS). 23 October (v3 only, N0):
# "Growth, zero-knob supply rule", "Linear growth, v4 AeST" and "v4 well-posedness" test only retired models, so they
# are satisfied by sitting red in ARCHIVE with N0 as the evidence lane; "Dwarf satellites vs screened law" is STALE
# (grey, "was: fails", RECOLOURS FAIL -> STALE with N0); "Cluster cores" is renamed to 326 clusters (RENAMES, N0).
# 23 October (evening): "Dwarf satellites vs screened law" is red again on the board, recomputed for v3 by S1.
MUST_STAY_RED = ["Cluster cores (326 eRASS1)", "Growth, zero-knob supply rule", "Law + a^1 growth + no EFE, local",
                 "Dwarf satellites vs screened law", "Linear growth, v3 Khronon", "Linear growth, v4 AeST",
                 "v4 well-posedness", "Covariant completion"]
# Every permitted recolour, as an ordered chain of steps per tile: [(earlier colour, new colour, evidence lane), ...].
# F2 (23 October morning) and C7 (23 October afternoon; that tile is now in ARCHIVE, red), then N0's 15 STALE tiles,
# then (23 October evening) the four grey tiles recomputed for v3 by their recompute lanes S1 and S2, then (late
# evening) P4's four grey tiles and the MW vertical force back from the archive, and Q6's native CMB; then (night) S3's
# MW outer slope, S4's three R4 tiles (classes unchanged, so back to their pre-grey colour) and H4's health and leaf.
RECOLOURS = {"Isolated-galaxy lensing, all radii": [("FAIL", "UNDEC", "F2")],
             "Linear growth, v4 AeST": [("COND", "FAIL", "C7")],
             "Strong coupling": [("COND", "STALE", "N0"), ("STALE", "COND", "P3")],
             "Black holes (EHT, LIGO ringdown)": [("COND", "STALE", "N0"), ("STALE", "COND", "P3")],
             "Rotation curves (SPARC RAR)": [("PASS", "STALE", "N0"), ("STALE", "COND", "P4")],
             "Isolated-galaxy lensing, inner": [("PASS", "STALE", "N0"), ("STALE", "COND", "S2")],
             # U1: static AQUAL (P4) read -0.59 dex; v3's own dynamics (T3) makes hosted systems dust-free -> Newtonian
             "Tidal dwarfs, NGC 1052-DF2/DF4": [("COND", "STALE", "N0"), ("STALE", "FAIL", "P4"), ("FAIL", "PASS", "U1")],
             "Central ellipticals (SLUGGS)": [("UNDEC", "STALE", "N0"), ("STALE", "UNDEC", "S4")],
             "Galaxy groups (BFJR)": [("PASS", "STALE", "N0"), ("STALE", "PASS", "P4")],
             "MW vertical force (round rule)": [("PASS", "FAIL", "P4")],
             "MW outer slope (Gaia)": [("UNDEC", "STALE", "N0"), ("STALE", "FAIL", "S3")],
             "Dwarf satellites vs screened law": [("FAIL", "STALE", "N0"), ("STALE", "FAIL", "S1")],
             "Coma ultra-diffuse galaxies": [("UNDEC", "STALE", "N0"), ("STALE", "FAIL", "S1")],
             "Red (early-type) lenses": [("COND", "STALE", "N0"), ("STALE", "COND", "S2")],
             "High-z on halo-free inputs": [("UNDEC", "STALE", "N0"), ("STALE", "UNDEC", "S4")],
             "CRISTAL z~5 / ALESS 122.1": [("UNDEC", "STALE", "N0"), ("STALE", "UNDEC", "S4")],
             "Health: ghosts, gradients": [("COND", "FAIL", "H4")],
             "Leaf problem well-posed": [("COND", "FAIL", "H4")],
             "Native CMB (patched CLASS)": [("OPEN", "STALE", "N0"), ("STALE", "FAIL", "Q6")],
             "Radiative stability (G12)": [("COND", "STALE", "N0")]}
# The only first greens allowed: tile -> (lane, result commit, coordinator rerun note). A tile may turn green for the
# first time ONLY if it is listed here AND its RECOLOURS step into PASS names the same lane; every other first green is
# refused. 23 October (night): the tidal dwarfs, by U1's derivation that held dust is weightless in its host (T3).
VERIFIED_GREEN = {"Tidal dwarfs, NGC 1052-DF2/DF4": (
    "U1", "54ee83e54e", "coordinator rerun 2026-10-23: main 15/16 and A2 6/6 reproduced, runtime/RSS-only diffs")}
RECIPE = ("Crispiest recipe (v3): General relativity plus a preferred cosmic time (Khronon) and one extra field giving "
          "the simple MOND law (AQUAL, external-field effect included, κ fitted), switched off within L★ ≥ 22 pc, "
          "plus fitted cold dust; no settling or supply rules.")
WRAP = 56     # characters per note line at fontsize 7.8
MAXL = 4      # note lines per board tile (4 since the 23 October night board; rows 1.10 in tall)
WRAP_A, MAXL_A = 56, 4   # archive tiles


def lane_text(t):
    return "/".join(t["lanes"])


def note_lines(t):
    return textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)


def archive_lines(a):
    return textwrap.wrap(f"was: {a['note']} · {lane_text(a)}", WRAP_A) + \
        textwrap.wrap(f"retired ({a['ev']}): {a['why']}; v3: {a['v3']}", WRAP_A)


def _chain(chain, base, st):
    """The RECOLOURS steps that lead from `base` to `st`, taken in order; None if the chain does not get there."""
    cur, i, used = base, 0, []
    while cur != st:
        k = next((k for k in range(i, len(chain)) if chain[k][0] == cur), None)
        if k is None:
            return None
        used.append(chain[k]); cur, i = chain[k][1], k + 1
    return used


def check(tiles, archive, recolours=None, verified=None):
    recolours = RECOLOURS if recolours is None else recolours
    verified = VERIFIED_GREEN if verified is None else verified
    errs = []
    names = {t["name"]: t for t in tiles}
    arch = {a["name"]: a for a in archive}
    old_of = {new: old for new, (old, _ev) in RENAMES.items()}
    for new, (old, ev) in RENAMES.items():
        if ev not in RETIRE_EVIDENCE or old not in PREVIOUS_BOARD:
            errs.append(f"rename without N0 evidence or unknown old name: {old} -> {new}")
    for t in tiles:
        n = t["name"]
        if not t["lanes"] or any(not str(x).strip() for x in t["lanes"]):
            errs.append(f"no evidence lane: {n}")
        if t["st"] not in COL:
            errs.append(f"bad colour {t['st']}: {n}")
        pm = PREVIOUS_BOARD.get(old_of.get(n, n))
        v3 = V3_BOARD.get(n)
        # 22 Oct, 23 Oct am, 23 Oct pm, first v3-only board
        for base in dict.fromkeys(b for b in (t["prev"], t["am"], pm, v3) if b is not None):
            if t["st"] == base:
                continue
            if not any(LANE_NEW.match(x) for x in t["lanes"]):
                errs.append(f"colour changed without a 22-23 October lane: {n}")
            used = _chain(recolours.get(n, []), base, t["st"])
            if not used or used[-1][2] not in t["lanes"] or any(not LANE_NEW.match(s[2]) for s in used):
                errs.append(f"recolour {base}->{t['st']} not listed in RECOLOURS with its evidence lane: {n}")
            if not t["new"]:
                errs.append(f"recoloured tile not flagged 23 OCT: {n}")
        if v3 == "STALE" and t["st"] != "STALE":
            used = _chain(recolours.get(n, []), "STALE", t["st"])
            if not used or used[0][2] != V3_REDO.get(n):
                errs.append(f"grey tile recoloured by a lane other than its recompute lane {V3_REDO.get(n)}: {n}")
        # no new green: a grey tile may return to green only if every earlier verdict was green (the recompute lane
        # check above makes the step out of grey its own lane); grey itself is not a verdict
        if t["st"] == "PASS" and any(b != "PASS" for b in (t["prev"], t["am"], pm, v3) if b != "STALE"):
            vg = verified.get(n)
            into = [s_ for s_ in recolours.get(n, []) if s_[1] == "PASS"]
            if vg is None or not into or into[-1][2] != vg[0] or vg[0] not in t["lanes"] or not vg[1] or not vg[2]:
                errs.append(f"turned green: {n} (a first green needs a VERIFIED_GREEN entry whose lane is its "
                            f"RECOLOURS step; refused on this board)")
        if n in V3_ARCHIVED:
            lane = REDO_BY_TILE.get(n)
            rc = recolours.get(n) or [(None, None, None)]
            if lane is None or lane not in t["lanes"] or rc[-1][2] != lane or not t["new"]:
                errs.append(f"archived tile back on the board without being recomputed by its lane {lane}: {n}")
        if t["st"] == "STALE":
            if pm is None or t["was"] != pm:
                errs.append(f"STALE tile's 'was' colour is not its 23 October afternoon colour: {n}")
            if "N0" not in t["lanes"] or not t["note"].startswith("was "):
                errs.append(f"STALE tile without N0 or without its old result ('was ...'): {n}")
            if t["redo"] not in set(RECOMPUTE.values()) | set(REDO_BY_TILE.values()):
                errs.append(f"STALE tile without a recompute lane: {n}")
        elif t["was"] is not None or t["redo"] is not None:
            errs.append(f"'was'/recompute lane on a tile that is not STALE: {n}")
        if pm is None and v3 is None and t["prev"] is None and t["am"] is None:
            errs.append(f"tile not on any earlier board (new tiles need a committed v3 lane and a board edit): {n}")
        if t["prev"] is None and not t["new"]:
            errs.append(f"new tile not flagged as 23 October: {n}")
        if len(note_lines(t)) > MAXL:
            errs.append(f"note too long ({len(note_lines(t))} lines): {n}")
    for a in archive:
        n = a["name"]
        if a["ev"] not in RETIRE_EVIDENCE:
            errs.append(f"retired to the archive without N0 as the evidence lane: {n}")
        if n not in PREVIOUS_BOARD or a["st"] != PREVIOUS_BOARD[n]:
            errs.append(f"archived tile does not keep its 23 October afternoon colour: {n}")
        if n in names:
            errs.append(f"tile both on the board and in the archive: {n}")
        if not a["lanes"] or not a["why"].strip() or not a["v3"].strip():
            errs.append(f"archived tile without lanes, retiring reason or v3 counterpart: {n}")
        if len(archive_lines(a)) > MAXL_A:
            errs.append(f"archive note too long ({len(archive_lines(a))} lines): {n}")
    on_board = {old_of.get(n, n) for n in names}
    for n in PREVIOUS_BOARD:
        if n not in on_board and n not in arch:
            errs.append(f"tile dropped from the board without being archived: {n}")
    for n in V3_BOARD:
        if n not in names:
            errs.append(f"tile of the first v3-only board left the board (N0's retirements are closed): {n}")
    for n in MUST_STAY_RED:
        if n in names:
            t = names[n]
            ok = t["st"] == "FAIL" or (t["st"] == "STALE" and t["was"] == "FAIL"
                                       and recolours.get(n, [None])[-1] == ("FAIL", "STALE", "N0"))
        elif n in arch:
            ok = arch[n]["st"] == "FAIL" and arch[n]["ev"] in RETIRE_EVIDENCE
        else:
            ok = False
        if not ok:
            errs.append(f"must stay red: {n}")
    for n in verified:
        if n not in names or names[n]["st"] != "PASS":
            errs.append(f"VERIFIED_GREEN entry not applied (tile not green on the board): {n}")
    for n, rc in recolours.items():
        held = names.get(n) or arch.get(n)
        if held is None or not rc or held["st"] != rc[-1][1]:
            errs.append(f"listed recolour not applied: {n}")
    if len(names) != len(tiles) or len(arch) != len(archive):
        errs.append("duplicate tile names")
    return errs


def _box(ax, x, y, w, h, st, dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.05", facecolor=COL[st],
                                edgecolor="#7b838b" if dashed else "none", linewidth=1.3 if dashed else 0,
                                linestyle=(0, (4, 3)) if dashed else "solid", alpha=1.0 if dashed else 0.93))


def _fit(fig, x, y, s, size, **kw):
    """Single-line figure text, shrunk until it fits inside the figure width."""
    txt = fig.text(x, y, s, fontsize=size, **kw)
    r = fig.canvas.get_renderer()
    while txt.get_window_extent(r).x1 > 0.99 * fig.bbox.width and size > 7:
        size -= 0.2
        txt.set_fontsize(size)
    return txt


def draw(tiles, out):
    ncol = len(COLUMNS)
    nmax = max(sum(1 for t in tiles if t["col"] == c) for c in range(ncol))
    W, H = 20.5, 3.05 + 1.10 * nmax                   # inches; each row 1.10 in tall (four note lines)
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    top_in, bot_in = 1.70, 0.95                      # header and legend bands, inches
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.25, nmax + 0.65); ax.axis("off")
    fig.text(0.015, 1 - 0.50 / H, "The Crispy Fried Chicken Status Board  ·  23 October 2026 — current theory v3 only",
             fontsize=24, fontweight="bold", color="#16201d")
    _fit(fig, 0.015, 1 - 0.95 / H, RECIPE, 12.0, color="#16201d", fontstyle="italic")
    fig.text(0.015, 1 - 1.30 / H, "a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted; footings 9.3603e-11 / 1.1312e-10 "
             "m/s^2 never pooled.  Every tile is scored for v3, or drawn grey until it is recomputed for v3.  Lane ids on "
             "every tile.  The theory is incomplete.", fontsize=10.5, color="#4d5a56")
    for c, title in enumerate(COLUMNS):
        ax.text(c + 0.03, nmax + 0.4, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
        for k, t in enumerate([t for t in tiles if t["col"] == c]):
            y = nmax - 0.5 - k
            stale = t["st"] == "STALE"
            ink = INK.get(t["st"], "white")
            _box(ax, c + 0.03, y - 0.46, 0.93, 0.90, t["st"], dashed=stale)
            ax.text(c + 0.065, y + 0.33, t["name"], fontsize=10.4, fontweight="bold", color=ink, va="center")
            lab = (f"NOT YET RECOMPUTED FOR v3  ·  RECOMPUTE: {t['redo']}" if stale
                   else (t["lab"] or LAB[t["st"]]).upper())
            ax.text(c + 0.065, y + 0.18, lab, fontsize=8.2, color=ink, va="center", alpha=0.95,
                    fontweight="bold" if stale else "normal")
            if t["new"]:
                ax.text(c + 0.945, y + 0.33, "23 OCT", fontsize=7.6, fontweight="bold", color=ink, va="center",
                        ha="right", alpha=0.9)
            for j, ln in enumerate(note_lines(t)):
                ax.text(c + 0.065, y + 0.03 - 0.1154 * j, ln, fontsize=7.8, color=ink, va="center", alpha=0.97)
    lx, ly = 0.015, 0.68 / H
    for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN", "STALE"):
        stale = st == "STALE"
        fig.patches.append(FancyBboxPatch((lx, ly - 0.01 * 13.2 / H), 0.014, 0.02 * 13.2 / H,
                                          boxstyle="round,pad=0,rounding_size=0.003", facecolor=COL[st],
                                          edgecolor="#7b838b" if stale else "none", linewidth=1.0 if stale else 0,
                                          linestyle=(0, (3, 2)) if stale else "solid",
                                          transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.019, ly, LAB[st], fontsize=10.5, va="center", color="#16201d")
        lx += 0.095
    fig.text(0.65, ly, "23 OCT = added, recoloured or re-annotated on 23 October.  PAPER59: DOI 10.5281/zenodo.23585319.",
             fontsize=9.0, va="center", color="#4d5a56")
    fig.text(0.015, 0.40 / H, "Grey, dashed = computed for an older model (board audit N0): the old result is shown as "
             "'was', and the tile names its recompute lane (S1-S4, P3, P4, Q6).  The tiles that tested only retired "
             "models are archived in img/status_board_archive_retired.png.", fontsize=9.0, va="center", color="#4d5a56")
    fig.text(0.015, 0.18 / H, "Cold energy (Omega_c/Omega_b = 5.364, an input) is real gravitating mass, not a particle "
             "species.", fontsize=9.0, va="center", color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def draw_archive(archive, out):
    ncol = len(COLUMNS)
    nmax = max(sum(1 for a in archive if a["col"] == c) for c in range(ncol))
    W, H = 20.5, 2.3 + 1.08 * nmax
    fig = plt.figure(figsize=(W, H), dpi=110)
    fig.patch.set_facecolor("#f1f1ee")
    top_in, bot_in = 1.25, 0.35
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.1, nmax * 1.08 + 0.55); ax.axis("off")
    fig.text(0.015, 1 - 0.50 / H, "Archived: retired models  ·  23 October 2026", fontsize=22, fontweight="bold",
             color="#16201d")
    fig.text(0.015, 1 - 0.92 / H, "These tiles tested only models that the current theory (v3) does not contain "
             "(board audit N0). Their old colours are kept for the record; they are not verdicts on v3. Each names "
             "its v3 counterpart.", fontsize=11, color="#4d5a56")
    for c, title in enumerate(COLUMNS):
        ax.text(c + 0.03, nmax * 1.08 + 0.3, title, fontsize=12.5, fontweight="bold", color="#16201d", va="center")
        for k, a in enumerate([a for a in archive if a["col"] == c]):
            y = nmax * 1.08 - 0.54 - 1.08 * k
            ax.add_patch(FancyBboxPatch((c + 0.03, y - 0.5), 0.93, 1.0, boxstyle="round,pad=0.0,rounding_size=0.05",
                                        facecolor=COL[a["st"]], edgecolor="none", alpha=0.55))
            ax.text(c + 0.065, y + 0.36, a["name"], fontsize=10.4, fontweight="bold", color="#16201d", va="center")
            ax.text(c + 0.065, y + 0.20, f"WAS: {LAB[a['st']].upper()}  ·  RETIRED", fontsize=8.2, color="#16201d",
                    va="center")
            for j, ln in enumerate(archive_lines(a)):
                ax.text(c + 0.065, y + 0.04 - 0.13 * j, ln, fontsize=7.8, color="#16201d", va="center")
    fig.savefig(out, dpi=110, facecolor=fig.get_facecolor())
    plt.close(fig)


def _by(seq, name):
    return next(x for x in seq if x["name"] == name)


def broken_cases():
    """Each case breaks one guard; check() must report at least one error for every case. A case gets the tiles, the
    archive and a copy of RECOLOURS (r)."""
    def c1(t, a, r, v):   # retire a MUST_STAY_RED tile with an evidence lane other than N0
        _by(a, "Linear growth, v4 AeST")["ev"] = "C7"

    def c2(t, a, r, v):   # retire a tile that is not in the archive list at all (silent drop)
        a.remove(_by(a, "v4 well-posedness"))

    def c3(t, a, r, v):   # drop a board tile without archiving it
        t.remove(_by(t, "Local a0 from MeerKAT"))

    def c4(t, a, r, v):   # recolour a main-board tile with no RECOLOURS entry
        _by(t, "Leaf problem well-posed")["st"] = "UNDEC"; _by(t, "Leaf problem well-posed")["new"] = True

    def c5(t, a, r, v):   # grey a CURRENT tile as STALE with no RECOLOURS entry
        x = _by(t, "Health: ghosts, gradients")
        x.update(st="STALE", was="COND", redo="P3", note="was conditional: " + x["note"]); x["lanes"].append("N0")

    def c6(t, a, r, v):   # STALE tile whose 'was' hides its old colour
        _by(t, "Radiative stability (G12)")["was"] = "PASS"

    def c7(t, a, r, v):   # STALE tile with no recompute lane
        _by(t, "Radiative stability (G12)")["redo"] = None

    def c8(t, a, r, v):   # a must-stay-red tile on the board turned blue
        _by(t, "Cluster cores (326 eRASS1)")["st"] = "UNDEC"

    def c9(t, a, r, v):   # archived tile repainted (its old red hidden)
        _by(a, "Growth, zero-knob supply rule")["st"] = "OPEN"

    def c10(t, a, r, v):  # a tile kept on the board and also archived
        t.append(dict(_by(a, "Energy books of settling"), prev="OPEN", am="OPEN", lab=None, new=False, was=None,
                      redo=None))

    def c11(t, a, r, v):  # a recomputed grey tile turned green although it was not green before greying
        r["Tidal dwarfs, NGC 1052-DF2/DF4"][-1] = ("STALE", "PASS", "P4")
        _by(t, "Tidal dwarfs, NGC 1052-DF2/DF4")["st"] = "PASS"

    def c12(t, a, r, v):  # retire a tile with no retiring reason
        _by(a, "Structural order (G0)")["why"] = " "

    def c13(t, a, r, v):  # rename a tile without a RENAMES entry
        _by(t, "Outer globulars: L* floor")["name"] = "Outer globulars (renamed)"

    def c14(t, a, r, v):  # give a grey tile a colour with no RECOLOURS step out of grey
        x = _by(t, "Radiative stability (G12)")
        x.update(st="COND", was=None, redo=None, note="recomputed", lanes=["P3"], new=True)

    def c15(t, a, r, v):  # a recomputed grey tile that does not carry its recompute lane
        _by(t, "Coma ultra-diffuse galaxies")["lanes"] = ["CFG933"]

    def c16(t, a, r, v):  # a grey tile recoloured by a lane other than its own recompute lane (S2 for an S1 tile)
        r["Coma ultra-diffuse galaxies"][-1] = ("STALE", "FAIL", "S2")
        _by(t, "Coma ultra-diffuse galaxies")["lanes"] = ["S2"]

    def c17(t, a, r, v):  # a recomputed grey tile not flagged 23 OCT
        _by(t, "Red (early-type) lenses")["new"] = False

    def c18(t, a, r, v):  # must-stay-red dwarf satellites recomputed to conditional, with a matching RECOLOURS step
        r["Dwarf satellites vs screened law"][-1] = ("STALE", "COND", "S1")
        _by(t, "Dwarf satellites vs screened law")["st"] = "COND"

    def c19(t, a, r, v):  # retire a tile of the first v3-only board to the archive after N0's audit
        t.remove(_by(t, "Red (early-type) lenses"))
        a.append(A(2, "Red (early-type) lenses", "COND", "inventory short", ["S2"], "late retirement", "none"))

    def c20(t, a, r, v):  # a recomputed tile that still carries its grey 'was' and recompute lane
        _by(t, "Isolated-galaxy lensing, inner").update(was="PASS", redo="S2")

    def c21(t, a, r, v):  # bring an archived tile back to the board unchanged (not recomputed for v3)
        x = a.pop(a.index(_by(a, "Ownership from an action")))
        t.append(dict(x, prev="OPEN", am="OPEN", lab=None, new=True, was=None, redo=None))

    def c22(t, a, r, v):  # the MW vertical force back from the archive without its recompute lane P4
        _by(t, "MW vertical force (round rule)")["lanes"] = ["CFG516"]

    def c23(t, a, r, v):  # a STALE tile turned green with no recompute (its old green kept)
        x = _by(t, "Galaxy groups (BFJR)"); x.update(lanes=["CFG540", "CFG543"])
        r["Galaxy groups (BFJR)"].pop()

    def c24(t, a, r, v):  # a first green listed in RECOLOURS but with no VERIFIED_GREEN entry
        r["Black holes (EHT, LIGO ringdown)"].append(("COND", "PASS", "P3"))
        _by(t, "Black holes (EHT, LIGO ringdown)")["st"] = "PASS"

    def c25(t, a, r, v):  # a VERIFIED_GREEN entry whose lane differs from the RECOLOURS step into green
        v["Tidal dwarfs, NGC 1052-DF2/DF4"] = ("P4",) + v["Tidal dwarfs, NGC 1052-DF2/DF4"][1:]

    def c26(t, a, r, v):  # a VERIFIED_GREEN entry for a tile that is not green
        v["Rotation curves (SPARC RAR)"] = ("P4", "6c0249a8bc", "rerun")

    return [("archive a must-stay-red tile with evidence C7, not N0", c1),
            ("silently drop an archived red tile", c2),
            ("drop a board tile without archiving it", c3),
            ("recolour a board tile without RECOLOURS", c4),
            ("grey a CURRENT tile without RECOLOURS", c5),
            ("STALE 'was' not the afternoon colour", c6),
            ("STALE tile without recompute lane", c7),
            ("must-stay-red board tile turned blue", c8),
            ("archived red repainted", c9),
            ("tile on board and in archive", c10),
            ("recomputed grey tile turned green, was not green", c11),
            ("archived without a retiring reason", c12),
            ("rename without RENAMES", c13),
            ("grey tile coloured without a RECOLOURS step", c14),
            ("recomputed grey tile without its lane", c15),
            ("grey tile recoloured by the wrong recompute lane", c16),
            ("recomputed grey tile not flagged 23 OCT", c17),
            ("must-stay-red grey tile recomputed to conditional", c18),
            ("v3-board tile retired after N0", c19),
            ("recomputed tile keeps 'was'/recompute lane", c20),
            ("archived tile back on the board unchanged", c21),
            ("archived tile back without its recompute lane", c22),
            ("grey tile back to its old green with no recompute", c23),
            ("first green with no VERIFIED_GREEN entry", c24),
            ("VERIFIED_GREEN lane differs from the RECOLOURS step", c25),
            ("VERIFIED_GREEN entry for a tile that is not green", c26)]


def selftest():
    base = check(copy.deepcopy(TILES), copy.deepcopy(ARCHIVE))
    print(f"clean board: {len(base)} errors")
    bad = 1 if base else 0
    td = _by(TILES, "Tidal dwarfs, NGC 1052-DF2/DF4")
    ok = td["st"] == "PASS" and not any("Tidal dwarfs" in e for e in base)
    print(f"  {'ALLOWED' if ok else 'BLOCKED'}: the tidal-dwarf verified green (VERIFIED_GREEN, U1) passes the checks")
    bad += 0 if ok else 1
    for label, fn in broken_cases():
        t, a, r, v = copy.deepcopy(TILES), copy.deepcopy(ARCHIVE), copy.deepcopy(RECOLOURS), copy.deepcopy(VERIFIED_GREEN)
        fn(t, a, r, v)
        e = check(t, a, r, v)
        print(f"  {'CAUGHT' if e else 'MISSED'}: {label}" + (f"  ->  {e[0]}" if e else ""))
        bad += 0 if e else 1
    print("SELFTEST PASS: every broken case caught; nothing written." if not bad else "SELFTEST FAIL")
    sys.exit(0 if not bad else 1)


def main():
    if "--selftest" in sys.argv[1:]:
        selftest()
    mutate = "--mutate" in sys.argv[1:]
    tiles, archive = copy.deepcopy(TILES), copy.deepcopy(ARCHIVE)
    if mutate:
        next(t for t in tiles if t["name"] == "Unscreened law vs Cassini")["lanes"] = []   # strip one tile's lane
    errs = check(tiles, archive)
    cnt = {k: sum(1 for t in tiles if t["st"] == k) for k in COL}
    print(f"{len(tiles)} tiles on the v3 board (" + ", ".join(f"{LAB[k]} {v}" for k, v in cnt.items())
          + f"); {len(archive)} archived (N0); {sum(t['new'] for t in tiles)} flagged 23 OCT")
    if errs:
        for e in errs:
            print("CHECK FAIL:", e)
        print("MUTATE: checks failed as required; nothing written." if mutate else "nothing written.")
        sys.exit(1)
    if mutate:
        print("MUTATE: checks did NOT catch the stripped lane")
        sys.exit(2)
    draw(tiles, OUT)
    draw_archive(archive, OUT_ARCHIVE)
    print("all checks PASS; wrote", os.path.relpath(OUT, os.path.dirname(HERE)), "and",
          os.path.relpath(OUT_ARCHIVE, os.path.dirname(HERE)))


if __name__ == "__main__":
    main()
