#!/usr/bin/env python3
"""Per-flavor status boards and a comparison grid (23 October 2026). Plot only; no physics is computed here.

The owner's request: "build per-flavor boards for v3, v4, canonical rules and plain MOND, plus a comparison grid (rows =
tests, columns = flavors, grey where not computed for that flavor); v3 stays the main board", and "add acdm too".

Flavors (one line each in RECIPES):
  v3          the current best theory. Its tiles are imported unchanged from make_status_board.py (TILES); that board
              and its image are not touched here (main() checks that its guard still passes).
  v4          AeST + gamma_L + capped F (THEORY_V3_DRAFT section 1b).
  canonical   the pre-covariant framework (THEORY_CANONICAL v2 / DSF-21's stiffened action): the law on baryons plus the
              settling, supply, round, capture and ownership rules and the QUMOND phantom.
  plain_mond  AQUAL with mu = x/(1+x), no screening, no dust, kappa = 1/2 fitted. No cosmology.
  lcdm        GR + Lambda + cold dark matter particles. A reference column only.

Honesty guards (check()):
  * a cell takes a colour only from a lane that computed that flavor (LANES[lane]['flavors']). A verdict computed for
    another flavor (or for the Newtonian / GR limit, pseudo-flavor 'newton') is reused only with a REUSE entry whose
    justification cites a file and line establishing that the computation is the same;
  * no cell is better than its lane's own verdict (VERDICTS, each with the file:line where the lane states it);
  * a green needs VERIFIED_GREEN_F (lane, result commit, a rerun or independent reproduction) naming the same lane, or,
    for the canonical rules only, a green the 23 October afternoon board already drew (make_status_board.PREVIOUS_BOARD);
  * plain MOND has no cosmology (COSMO_ROWS stay grey); LCDM rows that need galaxy-formation modelling the record never
    ran (LCDM_GREY_ROWS) stay grey; every lane cited must be in LANES;
  * the v3 column equals the main board, and the main board's own check() returns no error.

Run:  OMP_NUM_THREADS=1 python3 explainers/make_flavor_boards.py            (writes the four flavor boards, the grid)
      OMP_NUM_THREADS=1 python3 explainers/make_flavor_boards.py --mutate   (drops one REUSE justification; the checks
                                                                            must FAIL and nothing is written)
      OMP_NUM_THREADS=1 python3 explainers/make_flavor_boards.py --selftest (broken cases; every one must be caught)
One core, seconds, < 0.3 GB.

kappa = 1/2 is FITTED; footings never pooled; the framework adds no dark-matter particle (the LCDM column has one and is
a reference only); the theory is not closed; nothing here says the data favour any flavor, including LCDM.
"""
import copy
import os
import re
import sys
import textwrap

import make_status_board as msb   # the main v3 board: imported, never edited or redrawn here

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
OUT_BOARD = {"v4": "status_board_v4.png", "canonical": "status_board_canonical_rules.png",
             "plain_mond": "status_board_plain_mond.png", "lcdm": "status_board_lcdm.png"}
OUT_GRID = "flavor_comparison_grid.png"

FLAVORS = ["v3", "v4", "canonical", "plain_mond", "lcdm"]
TITLE = {"v3": "v3", "v4": "v4", "canonical": "canonical rules", "plain_mond": "plain MOND", "lcdm": "ΛCDM"}
RECIPES = {
    "v3": "General relativity plus a preferred cosmic time (Khronon) and one extra field giving the simple MOND law "
          "(AQUAL, external-field effect included, κ fitted), switched off within L★ ≥ 22 pc, plus fitted cold dust; "
          "no settling or supply rules.",
    "v4": "AeST (Skordis–Złośnik) with C1's capped free function (static limit = the law μ = x/(1+x)) plus the same "
          "stiffness term γ_L; AeST's own dust; κ fitted. Not the best theory: ill-posed where the aether twists (I1).",
    "canonical": "The pre-covariant framework (THEORY_CANONICAL v2; DSF-21's stiffened action): the law on baryons "
                 "(QUMOND phantom, ν_mono / algebraic) plus cold-energy rules for settling, catchment supply, round "
                 "enclosed mass, capture and ownership; κ fitted.",
    "plain_mond": "AQUAL with μ = x/(1+x) on baryons, external-field effect included; no screening, no dust, no "
                  "cosmology; κ = ½ fitted.",
    "lcdm": "GR + Λ + cold dark matter particles (6 fitted cosmological parameters; halos from simulations). It has a "
            "dark-matter particle, which this framework's owner rules out for the framework itself; a reference only.",
}
PSEUDO = {"newton"}   # the Newtonian / GR limit some lanes compute as a row; never a column of its own

COL, LAB, COLUMNS = msb.COL, msb.LAB, msb.COLUMNS
GREY = "#dcdfe2"
RANK = {"FAIL": 0, "UNDEC": 1, "COND": 2, "PASS": 3}

# Tiles that are the same test under different names share one grid row.
ROW_OF = {
    "Leaf problem well-posed": "Well-posed (leaf / Cauchy problem)",
    "v4 well-posedness": "Well-posed (leaf / Cauchy problem)",
    "Linear growth, v3 Khronon": "Linear growth",
    "Linear growth, v4 AeST": "Linear growth",
    "Linear growth (dust limit, ΛCDM refit)": "Linear growth",
    "MW vertical force (round rule)": "MW vertical force",
    "MW vertical force (AQUAL disc)": "MW vertical force",
    "Cluster cores (326 eRASS1)": "Cluster cores (eRASS1 × KiDS)",
    "Cluster cores (318 eRASS1)": "Cluster cores (eRASS1 × KiDS)",
    "Native CMB (patched CLASS)": "Native CMB",
    "Native CMB (plik-lite refit)": "Native CMB",
    "Native CMB (C7 patched CLASS)": "Native CMB",
    "Dwarf satellites vs screened law": "Dwarf satellites (MW / M31)",
    "Dwarf satellites (AQUAL, host EFE)": "Dwarf satellites (MW / M31)",
    "Dwarf satellites (Moster+13 + NFW route)": "Dwarf satellites (MW / M31)",
    "Outer globulars: L* floor": "Outer globular clusters",
    "Outer globulars (Newton)": "Outer globular clusters",
    "Tidal dwarfs (Newton)": "Tidal dwarfs, NGC 1052-DF2/DF4",
}
COSMO_ROWS = {"Native CMB", "Linear growth", "Cosmic shear, native inputs", "Cosmic shear, 1024³ PM vs raw KiDS",
              "Native shear rerun (CFG960)", "CMB lensing (Planck PR4)", "a0(z): native band vs a0 ~ H(z)",
              "Growth, zero-knob supply rule", "Structure growth, chassis alone", "The owner's wave a0(z) idea"}
# LCDM rows that would need galaxy-formation, feedback or halo modelling the record never ran: never coloured.
LCDM_GREY_ROWS = {"Rotation curves (SPARC RAR)", "Local a0 from MeerKAT", "Galaxy groups (BFJR)", "MW vertical force",
                  "MW outer slope (Gaia)", "Central ellipticals (SLUGGS)", "High-z on halo-free inputs",
                  "CRISTAL z~5 / ALESS 122.1", "Coma ultra-diffuse galaxies", "Cluster cores (eRASS1 × KiDS)",
                  "Isolated-galaxy lensing, inner", "Isolated-galaxy lensing, all radii", "Red (early-type) lenses",
                  "ALMA U4 (6 Nov), GS4 (28 Nov)", "a0(z): native band vs a0 ~ H(z)", "Why kappa = 1/2",
                  # G2's Moster+NFW route is PAPER36 eq. 1 (M_dark = M_ph + f_ex(1 - f_b) M_NFW, G2 README L45) scored
                  # under the framework's law; ΛCDM's own satellite prediction (Newtonian dynamics in a tidally evolved
                  # subhalo) was never computed
                  "Dwarf satellites (MW / M31)"}
# Lanes allowed to carry a ΛCDM (or GR) arm, with the file:line where that arm is stated. Any other lane registered for
# 'lcdm' is refused; a ΛCDM cell may reuse only the Newtonian limit, never a framework-law flavor.
LCDM_ARMS = {
    "C2": "covariant_push_2026_10_22/C2_aest_cosmology/README.md:L172 (ΛCDM refit to plik-lite)",
    "C7": "covariant_push_2026_10_22/C7_aest_class/README.md:L161 (the same ΛCDM refit, pristine CLASS)",
    "Q6": "rebuild_2026_10_22/Q6_v3_class/README.md:L21, L131 (ΛCDM refit; DUST reproduces ΛCDM)",
    "F3": "rebuild_2026_10_22/F3_growth_audit/README.md:L25, L75 (GR + dust on the ΛCDM refit)",
    "CFG596": "campaign_fresh_gravity/CFG596_lean_pm_1024/README.md:L116-L121, L141 (S0 arm: GR + Newtonian dust, "
              "ΛCDM-inherited ICs and background)",
}


def row_of(name):
    return ROW_OF.get(name, name)


# ---------------------------------------------------------------------------------------------------------------------
# Lanes: which flavors each one computed (and where that is stated). 'newton' = the lane computes a Newtonian/GR row.
R, CP, DP, CF = "rebuild_2026_10_22/", "covariant_push_2026_10_22/", "doors_push_2026_10_22/", "campaign_fresh_gravity/"
TV3 = CP + "THEORY_V3_DRAFT.md"
N0 = R + "N0_board_audit/AUDIT.md"
LANES = {}


def L(lane, flavors, where):
    LANES[lane] = dict(flavors=set(flavors), where=where)


# v4 lanes
L("I1", {"v4"}, R + "I1_gammaL_causality/README.md:L1")
L("H1", {"v4"}, R + "H1_aest_F/README.md:L1")
L("H2", {"v4"}, R + "H2_aest_clusters/README.md:L1")
L("H3", {"v4"}, R + "H3_jeans_control/README.md:L1")
L("C2", {"v4", "lcdm"}, CP + "C2_aest_cosmology/README.md:L1 (AeST background); L172 (ΛCDM refit)")
L("C7", {"v4", "lcdm"}, CP + "C7_aest_class/README.md:L13-L14 (AeST runs); L161 (ΛCDM refit)")
L("M1", {"v3", "v4"}, R + "M1_trilemma/README.md:L3-L9")
L("C5", {"v3", "v4", "canonical"}, TV3 + ":L13, L17 (η > 0 = DSF-21's A33), L26")
# canonical-rules lanes (the 23 October afternoon board's old-model lanes, classified by N0)
for lane, row in [("CFG695", 15), ("CFG919", 15), ("CFG301", 16), ("CFG309", 16), ("CFG804", 17), ("CFG829", 17),
                  ("CFG840", 17), ("CFG902", 17), ("CFG903", 18), ("CFG936", 19), ("CFG939", 19), ("CFG332", 21),
                  ("CFG333", 21), ("CFG528b", 22), ("CFG540", 23), ("CFG543", 23), ("CFG516", 24), ("CFG532b", 25),
                  ("CFG533", 25), ("E6", 27), ("CFG687", 28), ("CFG933", 29), ("CFG948", 29), ("CFG926", 30),
                  ("CFG914", 31), ("CFG921", 31), ("CFG928", 31), ("CFG689", 32), ("PAPER38", 32), ("CFG303", 33),
                  ("CFG307", 34), ("CFG308", 34), ("CFG654-A2", 35), ("CFG654-A3", 35), ("CFG909", 35),
                  ("CFG960", 36), ("CFG917", 38), ("CFG927", 38), ("CFG555", 39), ("CFG556", 39),
                  ("CFG806-U4", 43), ("CFG809", 43), ("CFG942", 43), ("CFG553", 45), ("CFG493", 47), ("CFG894", 47),
                  ("CFG886", 49), ("CFG945", 50), ("CFG950", 50), ("CFG953", 50), ("CFG941", 51), ("CFG944", 51),
                  ("CFG946", 51), ("CFG947", 52), ("CFG951", 52), ("CFG954", 52), ("CFG955", 52), ("CFG932", 53),
                  ("CFG935", 53)]:
    L(lane, {"canonical"}, f"{N0}:L{80 + row} (N0 row {row}: the lane's model)")
L("CFG815", {"canonical"}, CF + "THEORY_CANONICAL_2026-10-16.md:L22-L27")
L("D7b", {"canonical"}, DP + "D7b_cassini_Q2/README.md:L1-L8 (the canonical law, unscreened)")
L("D7c", {"canonical"}, DP + "D7c_q2_rar_gate/README.md:L1-L9 (the record's unscreened law family)")
L("D7d", {"canonical"}, DP + "D7d_screened_q2/README.md:L1-L6 (the stiffened DSF-21 action)")
L("D6", {"canonical"}, DP + "D6_u_mechanism/README.md:L1-L8")
L("P1", {"canonical"}, R + "P1_dwarf_chemistry/README.md:L1-L6 (E6's catchment supply)")
L("G1", {"canonical"}, TV3 + ":L67 (the old engine's growth excess)")
L("G2", {"canonical"}, R + "G2_preinfall_retention/README.md:L1-L23 (PAPER36's rule)")
L("CFG596", {"canonical", "lcdm"}, CF + "CFG596_lean_pm_1024/README.md:L116-L142 (F arm = settling rules; S0 arm = "
  "GR + Newtonian dust with ΛCDM-inherited ICs and background)")
L("F1", {"v3", "canonical"}, R + "F1_cluster_cores/README.md:L59-L75 (addendum: the record's settled c* = 0.40)")
L("F2", {"v3", "canonical"}, TV3 + ":L65 (the record's Δχ² +100 is the catchment edge's)")
L("F3", {"v3", "canonical", "lcdm"}, R + "F3_growth_audit/README.md:L8, L25, L75 (settling rules; dust limit on "
  "the ΛCDM refit)")
# plain-MOND lanes: rows computed at L★ = 0 are plain MOND itself
L("E2", {"v3", "plain_mond"}, DP + "E2_field_equation/README.md:L1-L11 (AQUAL μ = x/(1+x), L★ = 0)")
L("D10", {"v3", "plain_mond", "newton"}, DP + "D10_native_Lstar/README.md:L18 (L★ = 0 row and Newton row)")
L("S1", {"v3", "plain_mond"}, R + "S1_v3_hosted_small/README.md:L36-L37, L77 (L★ = 0 rows)")
L("U1", {"v3", "newton"}, R + "U1_v3_dust_content/README.md:L12, L135 (B0 = dust-free Newtonian)")
for lane in ("P4", "S2", "S3", "S4", "P2"):
    L(lane, {"v3"}, R + {"P4": "P4_v3_galaxy_tiles", "S2": "S2_v3_lowg_lensing", "S3": "S3_v3_mw_seals",
                        "S4": "S4_v3_muK_clusters", "P2": "P2_spec_isolated_lensing"}[lane] + "/README.md:L1")
L("Q6", {"v3", "lcdm"}, R + "Q6_v3_class/README.md:L21, L131 (ΛCDM refit; DUST = ΛCDM)")

# ---------------------------------------------------------------------------------------------------------------------
# What each lane itself concluded: (lane, flavor computed, row) -> (colour, file:line where the lane states it).
VERDICTS = {}


def V(lane, comp, row, st, where):
    VERDICTS[(lane, comp, row)] = (st, where)


# v4
V("H3", "v4", "Health: ghosts, gradients", "COND", TV3 + ":L26-L30")
V("I1", "v4", "Well-posed (leaf / Cauchy problem)", "FAIL", R + "I1_gammaL_causality/README.md:L3-L14")
V("I1", "v4", "Causality: criterion A / B", "FAIL", R + "I1_gammaL_causality/README.md:L5-L14")
V("H1", "v4", "Solar system + Cassini (screened)", "PASS", R + "H1_aest_F/README.md:L95; " + TV3 + ":L22-L25")
V("H2", "v4", "Cluster cores (eRASS1 × KiDS)", "FAIL", R + "H2_aest_clusters/README.md:L3-L11")
V("C7", "v4", "Linear growth", "FAIL", TV3 + ":L72")
V("C7", "v4", "Native CMB", "FAIL", CP + "C7_aest_class/README.md:L13-L14; " + TV3 + ":L72")
V("I1", "v4", "Covariant completion", "FAIL", TV3 + ":L37; " + R + "M1_trilemma/README.md:L5-L9")
V("C2", "v4", "What sets the cold-mass amount", "OPEN", CP + "C2_aest_cosmology/README.md:L8-L13")
# canonical rules: the colour the 23 October afternoon board drew for the lane, unless a rebuild lane changed it
for row, lane, st in [
        ("Rotation curves (SPARC RAR)", "CFG695", "PASS"), ("Local a0 from MeerKAT", "CFG301", "PASS"),
        ("Isolated-galaxy lensing, inner", "CFG804", "PASS"),
        ("Tidal dwarfs, NGC 1052-DF2/DF4", "CFG936", "COND"), ("Globulars + ownership rule", "CFG332", "COND"),
        ("Central ellipticals (SLUGGS)", "CFG528b", "UNDEC"), ("Galaxy groups (BFJR)", "CFG540", "PASS"),
        ("MW vertical force", "CFG516", "PASS"), ("MW outer slope (Gaia)", "CFG532b", "UNDEC"),
        ("Dwarf cold supply (chemistry)", "E6", "COND"), ("Coma ultra-diffuse galaxies", "CFG933", "UNDEC"),
        ("Red (early-type) lenses", "CFG926", "COND"), ("One selector for the family", "CFG914", "OPEN"),
        ("a0(z): native band vs a0 ~ H(z)", "CFG689", "UNDEC"), ("High-z on halo-free inputs", "CFG303", "UNDEC"),
        ("CRISTAL z~5 / ALESS 122.1", "CFG307", "UNDEC"), ("Cosmic shear, native inputs", "CFG909", "COND"),
        ("CMB lensing (Planck PR4)", "CFG917", "UNDEC"), ("Growth, zero-knob supply rule", "CFG555", "FAIL"),
        ("ALMA U4 (6 Nov), GS4 (28 Nov)", "CFG806-U4", "OPEN"), ("Gaia DR4 MW predictions", "CFG553", "OPEN"),
        ("Why kappa = 1/2", "CFG493", "OPEN"), ("What sets the cold-mass amount", "CFG886", "OPEN"),
        ("Ownership from an action", "CFG945", "OPEN"), ("Law + a^1 growth + no EFE, local", "CFG946", "FAIL"),
        ("Physical parent of the shear engine", "CFG951", "OPEN"), ("Energy books of settling", "CFG932", "OPEN")]:
    V(lane, "canonical", row, st, "explainers/make_status_board.py PREVIOUS_BOARD (23 October afternoon); "
      + LANES[lane]["where"])
# all radii: the 22 October board drew CFG902/903's frozen fail (TILES prev); F2 traces the +100 to the catchment edge
V("CFG902", "canonical", "Isolated-galaxy lensing, all radii", "FAIL",
  "explainers/make_status_board.py TILES prev = FAIL (22 October board); " + TV3 + ":L65")
V("C5", "canonical", "Health: ghosts, gradients", "FAIL", TV3 + ":L13, L17")
V("D7d", "canonical", "Solar system + Cassini (screened)", "PASS", DP + "D7d_screened_q2/README.md:L3-L6")
V("D7b", "canonical", "Unscreened law vs Cassini", "FAIL", DP + "D7b_cassini_Q2/README.md:L3-L8")
V("G2", "canonical", "Dwarf satellites (MW / M31)", "FAIL", R + "G2_preinfall_retention/README.md:L1-L10")
V("CFG815", "canonical", "Cluster cores (eRASS1 × KiDS)", "FAIL", CF + "THEORY_CANONICAL_2026-10-16.md:L22-L27")
V("CFG596", "canonical", "Cosmic shear, 1024³ PM vs raw KiDS", "FAIL", CF + "CFG596_lean_pm_1024/README.md:L131-L141")
V("CFG960", "canonical", "Native shear rerun (CFG960)", "FAIL", N0 + ":L116")
# plain MOND (computed at L★ = 0, or reused from v3 lanes where screening and dust are absent: see REUSE)
V("E2", "plain_mond", "Unscreened law vs Cassini", "FAIL", DP + "E2_field_equation/README.md:L8")
V("D10", "plain_mond", "Outer globular clusters", "FAIL", DP + "D10_native_Lstar/README.md:L18")
V("E2", "plain_mond", "Gaia DR4 wide binaries (Dec)", "OPEN", DP + "E2_field_equation/README.md:L11; " + TV3 + ":L92")
V("S1", "plain_mond", "Dwarf satellites (MW / M31)", "FAIL", R + "S1_v3_hosted_small/README.md:L37")
V("S1", "plain_mond", "Coma ultra-diffuse galaxies", "FAIL", R + "S1_v3_hosted_small/README.md:L77")
for row, lane, st, where in [
        ("Rotation curves (SPARC RAR)", "P4", "COND", "P4_v3_galaxy_tiles/README.md:L16"),
        ("Local a0 from MeerKAT", "P4", "PASS", "P4_v3_galaxy_tiles/README.md:L17"),
        ("Galaxy groups (BFJR)", "P4", "PASS", "P4_v3_galaxy_tiles/README.md:L18"),
        ("MW vertical force", "P4", "FAIL", "P4_v3_galaxy_tiles/README.md:L19"),
        ("Tidal dwarfs, NGC 1052-DF2/DF4", "P4", "FAIL", "P4_v3_galaxy_tiles/README.md:L20"),
        ("Isolated-galaxy lensing, inner", "S2", "COND", "S2_v3_lowg_lensing/README.md:L3"),
        ("Red (early-type) lenses", "S2", "COND", "S2_v3_lowg_lensing/README.md:L3"),
        ("Isolated-galaxy lensing, all radii", "P2", "UNDEC", "P2_spec_isolated_lensing/README.md:L1"),
        ("MW outer slope (Gaia)", "S3", "FAIL", "S3_v3_mw_seals/README.md:L5-L6"),
        ("Why kappa = 1/2", "S3", "OPEN", "S3_v3_mw_seals/README.md:L1"),
        ("Central ellipticals (SLUGGS)", "S4", "UNDEC", "S4_v3_muK_clusters/README.md:L180"),
        ("High-z on halo-free inputs", "S4", "UNDEC", "S4_v3_muK_clusters/README.md:L181-L187"),
        ("CRISTAL z~5 / ALESS 122.1", "S4", "UNDEC", "S4_v3_muK_clusters/README.md:L187-L188")]:
    V(lane, "v3", row, st, R + where)
V("F1", "v3", "Cluster cores (eRASS1 × KiDS)", "FAIL", TV3 + ":L66")
# LCDM and the Newtonian rows
V("C2", "lcdm", "Native CMB", "PASS", CP + "C2_aest_cosmology/README.md:L172")
V("F3", "lcdm", "Linear growth", "PASS", R + "F3_growth_audit/README.md:L8, L75")
V("CFG596", "lcdm", "Cosmic shear, 1024³ PM vs raw KiDS", "COND", CF + "CFG596_lean_pm_1024/README.md:L131, L141-L142")
V("U1", "newton", "Tidal dwarfs, NGC 1052-DF2/DF4", "PASS", R + "U1_v3_dust_content/README.md:L135")
V("D10", "newton", "Outer globular clusters", "COND", DP + "D10_native_Lstar/README.md:L18, L21")

# ---------------------------------------------------------------------------------------------------------------------
# A verdict computed for one flavor reused for another: (flavor, row) -> (flavor computed, lane, justification).
REUSE = {
    ("plain_mond", "Rotation curves (SPARC RAR)"): ("v3", "P4",
        "P4 README L22, L36: values at L★ 24 and 90 pc agree (L★ 90 moves the SPARC rms < 0.0002), so screening is "
        "inert at these radii; L108: no μ_K²ψ (dust) term. P4's v3 is AQUAL μ = x/(1+x) + EFE on baryons = plain MOND"),
    ("plain_mond", "Local a0 from MeerKAT"): ("v3", "P4", "P4 README L22, L108: screening inert, no dust term"),
    ("plain_mond", "Galaxy groups (BFJR)"): ("v3", "P4", "P4 README L22, L108: screening inert, no dust term"),
    ("plain_mond", "MW vertical force"): ("v3", "P4", "P4 README L19, L22, L108: every L★ and EFE; no dust term"),
    ("plain_mond", "Tidal dwarfs, NGC 1052-DF2/DF4"): ("v3", "P4",
        "P4 README L20, L22, L108: static AQUAL in the host field, no dust term (U1's dust-free reading is v3's own)"),
    ("plain_mond", "Isolated-galaxy lensing, inner"): ("v3", "S2",
        "S2 README L39: screening l_g/R ≤ 2e-4 (unscreened); L3, L83: no μ_K²ψ term"),
    ("plain_mond", "Red (early-type) lenses"): ("v3", "S2", "S2 README L39, L83: unscreened, no μ_K²ψ term"),
    ("plain_mond", "Isolated-galaxy lensing, all radii"): ("v3", "P2",
        "P2 README L116: no dust term; N0 AUDIT L98: F2's (and P2's) v3 is its own AQUAL μ = x/(1+x) solver"),
    ("plain_mond", "MW outer slope (Gaia)"): ("v3", "S3",
        "S3 README L50: the galaxy is unscreened at every radius; L52, L152: the μ_K² term is not solved"),
    ("plain_mond", "Why kappa = 1/2"): ("v3", "S3", "S3 README L50, L152: AQUAL discs unscreened, no dust term"),
    ("plain_mond", "Cluster cores (eRASS1 × KiDS)"): ("v3", "F1",
        "THEORY_V3_DRAFT L66: F1 is the law on baryons (AQUAL); N0 AUDIT L108: v3's μ_K²ψ term not included"),
    ("plain_mond", "Central ellipticals (SLUGGS)"): ("v3", "S4",
        "S4 README L170-L180: a kernel-only swap to ν₁ with no screening, ownership or dust in the R4 scripts"),
    ("plain_mond", "High-z on halo-free inputs"): ("v3", "S4", "S4 README L170-L187: kernel-only swap to ν₁"),
    ("plain_mond", "CRISTAL z~5 / ALESS 122.1"): ("v3", "S4", "S4 README L170-L188: kernel-only swap to ν₁"),
    ("lcdm", "Tidal dwarfs, NGC 1052-DF2/DF4"): ("newton", "U1",
        "U1 README L135: B0 is the dust-free Newtonian prediction for the 19 TDGs; G2 README L25: data +0.08 ± 0.10 "
        "dex vs Newton. ΛCDM's tidal dwarfs carry no dark matter, so its prediction is the same Newtonian computation"),
    ("lcdm", "Outer globular clusters"): ("newton", "D10",
        "D10 README L18: Newton row (Δχ²_Newton ≤ 2.5; 9000 Newton solves, L55). ΛCDM's outer globulars carry no "
        "dark matter, so its prediction is that Newtonian row"),
}
FILE_LINE = re.compile(r"(README|THEORY|AUDIT|\.md|\.py).{0,40}L\d+")

# A first green: (flavor, row) -> (lane, result commit, rerun or independent reproduction).
VERIFIED_GREEN_F = {
    ("v4", "Solar system + Cassini (screened)"): ("H1", "1654b84f78",
        "reproduced by the coordinator (THEORY_V3_DRAFT §1b L21: lanes H1-H3 all reproduced)"),
    ("plain_mond", "Local a0 from MeerKAT"): ("P4", "6c0249a8bc",
        "coordinator rerun 2026-10-23: P4 identical except peak RSS"),
    ("plain_mond", "Galaxy groups (BFJR)"): ("P4", "6c0249a8bc",
        "coordinator rerun 2026-10-23: P4 identical except peak RSS"),
    ("lcdm", "Native CMB"): ("C2", "5e93769089",
        "the ΛCDM refit is reproduced independently by C7 K1 (README L161: 1003.48 vs C2's 1003.20) and Q6 "
        "(README L21: 1003.47)"),
}
# Greens a lane earned but the guard withholds (no rerun or independent reproduction on record): drawn one step down,
# labelled. Listed so the md can say so.
WITHHELD_GREEN = {("lcdm", "Linear growth"): "F3's dust-limit KiDS comparison has no rerun on record"}


# ---------------------------------------------------------------------------------------------------------------------
def C(flavor, col, name, st, note, lanes, ev=None, comp=None, lab=None):
    """One cell of a flavor board. ev = the lane whose verdict sets the colour; comp = the flavor that lane computed
    (defaults to this flavor; anything else needs a REUSE entry)."""
    return dict(flavor=flavor, col=col, name=name, row=row_of(name), st=st, note=note, lanes=list(lanes),
                ev=ev or lanes[0], comp=comp or flavor, lab=lab)


def v3_cells():
    out = []
    for t in msb.TILES:
        out.append(dict(flavor="v3", col=t["col"], name=t["name"], row=row_of(t["name"]),
                        st=None if t["st"] == "STALE" else t["st"], note=t["note"], lanes=list(t["lanes"]),
                        ev=None, comp="v3", lab=t["lab"]))
    return out


CELLS = [
    # ---------------- v4 ----------------
    C("v4", 0, "Health: ghosts, gradients", "COND",
      "no ghost at linear order on the Y = 0 vacuum (H3); C5's negative-energy mode is the dust's Jeans mode; growth "
      "rate bounded; γ_L gives no causal cone (open)", ["H3", "H1", "C5"]),
    C("v4", 0, "v4 well-posedness", "FAIL",
      "ILL-POSED where the aether twists, i.e. in every non-symmetric bound system; well posed only on "
      "aether-orthogonal slices; no healthy completion", ["I1"]),
    C("v4", 0, "Causality: criterion A / B", "FAIL",
      "A violated; where the aether twists, relayed signals can close loops in time, so B fails in principle "
      "(loop gains 4 ms–3.9 s around the Galaxy)", ["I1"]),
    C("v4", 0, "Solar system + Cassini (screened)", "PASS",
      "capped F: Q₂ ≤ 7e-8 of Park's bound (static solve); the Sun in the Galaxy's field has no well-posed slice "
      "(I1)", ["H1"]),
    C("v4", 2, "Cluster cores (326 eRASS1)", "FAIL",
      "CANNOT supply the core excess: AeST's static dust has the wrong radial shape; best profile χ² 27.7–39.6 vs "
      "line 11.07 (law alone 27.3–41.8)", ["H2"]),
    C("v4", 3, "Linear growth, v4 AeST", "FAIL",
      "Newtonian term survives on large scales for any F (H1), but on FRW v4 runs away for the Cosh dust shape: "
      "P/P_ΛCDM 1e2–1e41 by 10 h/Mpc (C7)", ["C7", "H1", "H3"]),
    C("v4", 3, "Native CMB (C7 patched CLASS)", "FAIL",
      "Cosh at its physical g = 0.75: plik-lite Δχ² +119 vs the ΛCDM refit, H₀ 55.6; SZ21's benchmarks match only "
      "at g = 1", ["C7"]),
    C("v4", 4, "Covariant completion", "FAIL",
      "trilemma: screening needs γ_L; γ_L is well posed only with an untwisted aether, which v4 is not (I1); no "
      "screening without γ_L tolerates a twist (M1 R2)", ["I1", "M1"]),
    C("v4", 4, "What sets the cold-mass amount", "OPEN",
      "Ω_c is fitted in an AeST-type completion: the dust density is an initial datum (I₀), independent of a₀ and Λ",
      ["C2"]),
    # ---------------- canonical rules ----------------
    C("canonical", 0, "Health: ghosts, gradients", "FAIL",
      "DSF-21's A33 form has η > 0, which C5 shows is ill-posed; the rules themselves have no action (CFG678)",
      ["C5"]),
    C("canonical", 0, "Solar system + Cassini (screened)", "PASS",
      "the stiffened DSF-21 action passes Cassini by 1e7–1e9 at L* = 24–90 pc, in all four Galactic fields", ["D7d"]),
    C("canonical", 0, "Unscreened law vs Cassini", "FAIL",
      "the canonical law, unscreened, fails the Hees 2σ line at every turn-off scale (D7b); no unscreened form passes "
      "both Q₂ and SPARC (D7c)", ["D7b", "D7c"], lab="fails (unscreened form)"),
    C("canonical", 1, "Rotation curves (SPARC RAR)", "PASS", "algebraic law: rms 0.101 / 0.099 dex, one global Υ",
      ["CFG695", "CFG919"]),
    C("canonical", 1, "Local a0 from MeerKAT", "PASS", "0.9–1.4e-10, matches SPARC (ν_mono)", ["CFG301", "CFG309"]),
    C("canonical", 1, "Isolated-galaxy lensing, inner", "PASS",
      "catchment supply suffices ≤ 0.31 Mpc; blue lenses A 1.016 (isolated law, no EFE); FRAGILE under window shifts "
      "(CFG840)", ["CFG804", "CFG829", "CFG840", "CFG902"]),
    C("canonical", 1, "Isolated-galaxy lensing, all radii", "FAIL",
      "frozen fail; F2: the Δχ² +100 is the catchment edge's, and the 'isolated' sample leaks hosts (not robust)",
      ["CFG902", "CFG903", "F2"], lab="fails (frozen; not robust)"),
    C("canonical", 1, "Tidal dwarfs, NGC 1052-DF2/DF4", "COND",
      "Newtonian if they captured no cold energy (capture route); host EFE untested", ["CFG936", "CFG939"]),
    C("canonical", 1, "Globulars + ownership rule", "COND", "owned clusters at Newton: ~1.6σ; 3 of 4 populations",
      ["CFG332", "CFG333"]),
    C("canonical", 1, "Central ellipticals (SLUGGS)", "UNDEC", "~3σ with measured tracers (ν_mono)", ["CFG528b"]),
    C("canonical", 1, "Galaxy groups (BFJR)", "PASS", "consistent supply closes (census edge); EFE unchecked",
      ["CFG540", "CFG543"]),
    C("canonical", 1, "MW vertical force (round rule)", "PASS",
      "the round rule beats the MOND phantom disc 32/32; within +4 of an NFW's χ² in only 6–9 of 16 cells; K_z scale "
      "length missed (baryon model)", ["CFG516"]),
    C("canonical", 1, "MW outer slope (Gaia)", "UNDEC", "3–5σ steeper (round rule, ν_mono, no EFE)",
      ["CFG532b", "CFG533"]),
    C("canonical", 2, "Dwarf satellites vs screened law", "FAIL",
      "pre-infall retention (PAPER36) FAILS on native inputs: +0.92 / +0.89 dex; it closes only with ΛCDM's subhalo "
      "mass put in by hand", ["G2"]),
    C("canonical", 2, "Dwarf cold supply (chemistry)", "COND",
      "catchment supply; P1's MDF test confirms it for the median, not 2σ-robust; supply is not a binding mechanism",
      ["E6", "P1"]),
    C("canonical", 2, "Cluster cores (318 eRASS1)", "FAIL",
      "the expelled-share rule fails the full 318 (middle tercile ×~1.6, Z ≈ +4); F1: the settled c* = 0.40 profile "
      "fixes the core only by breaking 1.2–3 Mpc", ["CFG815", "CFG687", "F1"]),
    C("canonical", 2, "Coma ultra-diffuse galaxies", "UNDEC", "+0.33 dex over the isolated law; Coma's field not "
      "applied (ν_mono)", ["CFG933", "CFG948"]),
    C("canonical", 2, "Red (early-type) lenses", "COND", "an IMF α–σ relation removes it (EFE-free law)", ["CFG926"]),
    C("canonical", 2, "One selector for the family", "OPEN", "excesses graded over the EFE-free ν_mono law",
      ["CFG914", "CFG919", "CFG921", "CFG928"]),
    C("canonical", 3, "a0(z): native band vs a0 ~ H(z)", "UNDEC", "own BAO ruler band; data cannot decide yet",
      ["CFG689", "PAPER38"]),
    C("canonical", 3, "High-z on halo-free inputs", "UNDEC", "RC100 on the flat line (ν_mono)", ["CFG303"]),
    C("canonical", 3, "CRISTAL z~5 / ALESS 122.1", "UNDEC", "stress tests: not robust (ν_mono)", ["CFG307", "CFG308"]),
    C("canonical", 3, "Cosmic shear, native inputs", "COND",
      "theory-v2 engine: KiDS CONSISTENT on both footings; the engine has no parent (CFG947)",
      ["CFG909", "CFG654-A2", "CFG654-A3"]),
    C("canonical", 3, "Cosmic shear, 1024³ PM vs raw KiDS", "FAIL",
      "settling rules + census supply: 19–25 % too much power at k 0.3–1; Δχ² +68.7 vs S0, EXCLUDED (canonical "
      "footing); F3: it belongs to the settling rules", ["CFG596", "F3"]),
    C("canonical", 3, "Native shear rerun (CFG960)", "FAIL", "SCT-M engine: SC1x FAILS, KiDS EXCLUDED, Δχ² +47.28",
      ["CFG960"]),
    C("canonical", 3, "CMB lensing (Planck PR4)", "UNDEC", "SAFE; CONSISTENT only under post-hoc A1; low power",
      ["CFG917", "CFG927"]),
    C("canonical", 3, "Growth, zero-knob supply rule", "FAIL",
      "the settling engine's excess grows with grid resolution (0.040 / 0.077 / 0.163 at 128³–512³, G1)",
      ["CFG555", "CFG556", "F3", "G1"]),
    C("canonical", 3, "ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN", "the governing plan's verdict kernel is ν_mono; "
      "expected unscorable", ["CFG806-U4", "CFG809", "CFG942"]),
    C("canonical", 3, "Gaia DR4 MW predictions", "OPEN", "sealed 10-10 for the round rule (ν_mono, QUMOND phantom "
      "disc, no EFE)", ["CFG553"]),
    C("canonical", 4, "Why kappa = 1/2", "OPEN", "fitted, 0.417 ± 0.095 (routes with ν_mono and algebraic laws)",
      ["CFG493", "CFG894"], lab="open: fitted"),
    C("canonical", 4, "What sets the cold-mass amount", "OPEN", "5.364 an input; the sourcing fraction u has no "
      "mechanism (D6)", ["CFG886", "D6"], lab="open: fitted"),
    C("canonical", 4, "Ownership from an action", "OPEN", "the label sector has no action", ["CFG945", "CFG950",
                                                                                              "CFG953"]),
    C("canonical", 4, "Law + a^1 growth + no EFE, local", "FAIL",
      "no-go: a local field giving the deep law must carry an EFE (CFG946); the class-A engine has no non-local "
      "causal parent (CFG947)", ["CFG946", "CFG947", "CFG941", "CFG944"]),
    C("canonical", 4, "Physical parent of the shear engine", "OPEN", "3 tried: LDT, SCT fail clusters; no kinetic "
      "parent", ["CFG951", "CFG954", "CFG955"]),
    C("canonical", 4, "Energy books of settling", "OPEN", "not conserved; a repair needs new physics",
      ["CFG932", "CFG935"]),
    # ---------------- plain MOND ----------------
    C("plain_mond", 0, "Unscreened law vs Cassini", "FAIL",
      "AQUAL μ = x/(1+x), no screening: Cassini Q₂ 2.44–4.59× / 2.85–5.19× the Hees 2σ line", ["E2"]),
    C("plain_mond", 1, "Rotation curves (SPARC RAR)", "COND",
      "one Υ per galaxy, EFE solved: rms 0.054 / 0.054 dex; median Υ 0.52 / 0.44; χ² line fails both", ["P4"],
      comp="v3"),
    C("plain_mond", 1, "Local a0 from MeerKAT", "PASS", "1.31e-10 vs SPARC same recipe 1.21e-10 (+0.032 dex)", ["P4"],
      comp="v3"),
    C("plain_mond", 1, "Isolated-galaxy lensing, inner", "COND",
      "blue A 0.88 / 0.81 at the primary field; decided by hot CGM and M★", ["S2"], comp="v3"),
    C("plain_mond", 1, "Isolated-galaxy lensing, all radii", "UNDEC",
      "spectroscopic isolation: N too small (needs ~22–26k lenses)", ["P2"], comp="v3"),
    C("plain_mond", 1, "Tidal dwarfs, NGC 1052-DF2/DF4", "FAIL",
      "static AQUAL in the host field: TDGs −0.59 / −0.62 dex, DF2/DF4 −1.66 / −1.74 ln below the law; no dust, so "
      "no dust-free escape", ["P4"], comp="v3"),
    C("plain_mond", 1, "Outer globulars: L* floor", "FAIL",
      "the unscreened law (L★ = 0) is excluded in all 18 cells (Δχ² 4.9–22.8)", ["D10"]),
    C("plain_mond", 1, "Central ellipticals (SLUGGS)", "UNDEC", "tension 3.1σ (ν₁ kernel)", ["S4"], comp="v3"),
    C("plain_mond", 1, "Galaxy groups (BFJR)", "PASS",
      "isolated: +0.010 / −0.010 dex (Z ±0.31); above the law if g_e ≥ 0.03 a₀", ["P4"], comp="v3",
      lab="pass (isolated)"),
    C("plain_mond", 1, "MW vertical force (AQUAL disc)", "FAIL",
      "K_z,1.1 92.3 / 96.9 vs 66.4 ± 2.2; χ² 178 / 251 vs a line of 67.5; every baryon model", ["P4"], comp="v3"),
    C("plain_mond", 1, "MW outer slope (Gaia)", "FAIL",
      "SHAPE EXCLUDED: slope −0.126 / −0.114 vs −0.325, Z −4.37 / −4.62", ["S3"], comp="v3"),
    C("plain_mond", 2, "Dwarf satellites (AQUAL, host EFE)", "FAIL",
      "L★ = 0 with the host field solved: +1.130 / +1.075 dex above the law", ["S1"]),
    C("plain_mond", 2, "Cluster cores (326 eRASS1)", "FAIL",
      "the law on baryons: A_MID 1.68–1.85 / 1.54–1.70, Z ≈ +5–6", ["F1"], comp="v3"),
    C("plain_mond", 2, "Coma ultra-diffuse galaxies", "FAIL",
      "L★ = 0 in Coma's field: +1.12 / +1.08 dex, z_sys 4.28 / 4.11", ["S1"]),
    C("plain_mond", 2, "Red (early-type) lenses", "COND",
      "inventory 1.31 / 1.20 short; + CFG667 + IMF α–σ → 1.02 / 0.93", ["S2"], comp="v3"),
    C("plain_mond", 3, "High-z on halo-free inputs", "UNDEC", "all six CFG303 classes unchanged with ν₁", ["S4"],
      comp="v3"),
    C("plain_mond", 3, "CRISTAL z~5 / ALESS 122.1", "UNDEC", "NOT ROBUST / NOT DISCRIMINATING with ν₁", ["S4"],
      comp="v3"),
    C("plain_mond", 3, "Gaia DR4 wide binaries (Dec)", "OPEN",
      "law-first AQUAL γ_v 1.167 / 1.199 at 20 kAU; Gaia DR4 decides", ["E2"]),
    C("plain_mond", 4, "Why kappa = 1/2", "OPEN", "fitted; AQUAL discs give κ_Λ 0.499 ± 0.116, κ_crit 0.413 ± 0.096",
      ["S3"], comp="v3", lab="open: fitted"),
    # ---------------- ΛCDM (reference) ----------------
    C("lcdm", 3, "Native CMB (plik-lite refit)", "PASS",
      "ΛCDM refit to plik-lite: χ² 582.3 for 613 bins (6 fitted parameters); reproduced with low-ℓ TT/EE by C7 and "
      "Q6 (χ² 1003.47)", ["C2", "C7", "Q6"], lab="pass (reference refit)"),
    C("lcdm", 3, "Linear growth (dust limit, ΛCDM refit)", "COND",
      "S₈ 0.845 / 0.814 (record / native H₀) vs raw KiDS, linear k ≤ 0.3 h/Mpc: CONSISTENT; green withheld, no rerun "
      "on record", ["F3", "Q6"], lab="consistent (linear only); green withheld"),
    C("lcdm", 3, "Cosmic shear, 1024³ PM vs raw KiDS", "COND",
      "S0 arm (GR + Newtonian dust, ΛCDM-inherited ICs): χ² 144.3 on 104 KiDS points, p 0.014; no baryonic feedback; "
      "L100 box", ["CFG596"], lab="marginal (p 0.014)"),
    C("lcdm", 1, "Tidal dwarfs (Newton)", "COND",
      "TDGs at Newton, as ΛCDM's DM-free TDGs: +0.055 ± 0.114 dex (U1), +0.08 ± 0.10 (G2); why DF2/DF4 lack DM needs "
      "formation modelling not run", ["U1", "G2"], comp="newton"),
    C("lcdm", 1, "Outer globulars (Newton)", "COND",
      "Newton is D10's best fit (Δχ² ≤ 2.5 vs every L★); assumes outer globulars carry no DM, as ΛCDM expects",
      ["D10"], comp="newton"),
]


# ---------------------------------------------------------------------------------------------------------------------
def all_cells(cells):
    return v3_cells() + cells


def check(cells, reuse=None, verified=None, lanes=None, verdicts=None, arms=None):
    reuse = REUSE if reuse is None else reuse
    arms = LCDM_ARMS if arms is None else arms
    verified = VERIFIED_GREEN_F if verified is None else verified
    lanes = LANES if lanes is None else lanes
    verdicts = VERDICTS if verdicts is None else verdicts
    errs = []
    main = msb.check(msb.TILES, msb.ARCHIVE)
    if main:
        errs.append(f"the main v3 board's own guard fails: {main[0]}")
    v3_main = {t["name"]: (None if t["st"] == "STALE" else t["st"]) for t in msb.TILES}
    for ln, rec in lanes.items():
        if "lcdm" in rec["flavors"] and not FILE_LINE.search(arms.get(ln, "")):
            errs.append(f"lane {ln} registered for ΛCDM without a cited ΛCDM/GR arm (LCDM_ARMS)")
    seen = set()
    for c in all_cells(cells):
        f, row, st = c["flavor"], c["row"], c["st"]
        if (f, row) in seen:
            errs.append(f"two cells in one grid row for {f}: {row}")
        seen.add((f, row))
        if f == "v3":
            if v3_main.get(c["name"], "missing") != st:
                errs.append(f"v3 column differs from the main board: {c['name']}")
            continue
        if f not in FLAVORS or c["comp"] not in set(FLAVORS) | PSEUDO:
            errs.append(f"unknown flavor: {f} / {c['comp']}: {row}")
            continue
        if st is not None and st not in COL:
            errs.append(f"bad colour {st}: {f} {row}")
        for ln in c["lanes"]:
            if ln not in lanes:
                errs.append(f"lane not in the registry (no committed computation named): {ln} ({f} {row})")
        ev, comp = c["ev"], c["comp"]
        if ev not in c["lanes"]:
            errs.append(f"deciding lane not among the cell's lanes: {f} {row}")
        if st is None:
            continue
        if ev in lanes and comp not in lanes[ev]["flavors"]:
            errs.append(f"lane {ev} did not compute {comp}: {f} {row}")
        if comp != f:
            r = reuse.get((f, row))
            if r is None or r[0] != comp or r[1] != ev or not FILE_LINE.search(r[2] or ""):
                errs.append(f"cross-flavor reuse without a file:line justification: {f} {row} (from {comp}, {ev})")
        vd = verdicts.get((ev, comp, row))
        if vd is None:
            errs.append(f"no recorded verdict of {ev} for {comp} on this row: {f} {row}")
        else:
            vst, where = vd
            if not FILE_LINE.search(where) and "PREVIOUS_BOARD" not in where:
                errs.append(f"verdict without a file:line: {ev} {row}")
            if vst == "OPEN" or st == "OPEN":
                if vst != st:
                    errs.append(f"open/verdict mismatch ({st} vs lane's {vst}): {f} {row}")
            elif RANK[st] > RANK[vst]:
                errs.append(f"colour better than the lane's verdict ({st} > {vst}): {f} {row}")
        if st == "PASS":
            vg = verified.get((f, row))
            earlier = f == "canonical" and msb.PREVIOUS_BOARD.get(c["name"]) == "PASS"
            if not earlier and (vg is None or vg[0] != ev or not vg[1] or not vg[2]):
                errs.append(f"green without verified evidence for {f}: {row}")
        if f == "plain_mond" and row in COSMO_ROWS:
            errs.append(f"plain MOND has no cosmology, so this row must stay grey: {row}")
        if f == "lcdm" and comp not in {"lcdm"} | PSEUDO:
            errs.append(f"ΛCDM cell reused from a framework-law lane ({comp}, {ev}); only the Newtonian limit may be "
                        f"reused: {row}")
        if f == "lcdm" and row in LCDM_GREY_ROWS:
            errs.append(f"ΛCDM row needs modelling the record never ran; it must stay grey: {row}")
    for (f, row), vg in verified.items():
        if not any(c["flavor"] == f and c["row"] == row and c["st"] == "PASS" for c in cells):
            errs.append(f"VERIFIED_GREEN_F entry not applied: {f} {row}")
    for (f, row) in reuse:
        if not any(c["flavor"] == f and c["row"] == row and c["comp"] != f for c in cells):
            errs.append(f"REUSE entry not used by any cell: {f} {row}")
    return errs


# ---------------------------------------------------------------------------------------------------------------------
def grid_rows(cells):
    """Rows of the grid: every row name, grouped by board column, in order of first appearance (v3 first)."""
    order, col_of = [], {}
    for f in FLAVORS:
        for c in all_cells(cells):
            if c["flavor"] == f and c["row"] not in col_of:
                col_of[c["row"]] = c["col"]
                order.append(c["row"])
    return [r for k in range(len(COLUMNS)) for r in order if col_of[r] == k], col_of


def counts(cells):
    rows, _ = grid_rows(cells)
    out = {}
    for f in FLAVORS:
        got = {c["row"]: c["st"] for c in all_cells(cells) if c["flavor"] == f}
        k = {s: sum(1 for r in rows if got.get(r) == s) for s in ("PASS", "COND", "FAIL", "UNDEC", "OPEN")}
        k["grey"] = sum(1 for r in rows if got.get(r) is None)
        out[f] = k
    return out


def _notes(c, wrap=56):
    return textwrap.wrap(f"{c['note']} · {'/'.join(c['lanes'])}", wrap)


def draw_board(f, cells, out):
    tiles = [c for c in cells if c["flavor"] == f]
    ncol = len(COLUMNS)
    nmax = max(1, max(sum(1 for t in tiles if t["col"] == k) for k in range(ncol)))
    W, H = 20.5, 2.95 + 1.10 * (nmax + 0.9)          # 1.10 in per row, as on the main board
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    top_in, bot_in = 1.70, 1.25
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.25, nmax + 0.65); ax.axis("off")
    fig.text(0.015, 1 - 0.50 / H, f"Flavor board · {TITLE[f]} · 23 October 2026", fontsize=24, fontweight="bold",
             color="#16201d")
    msb._fit(fig, 0.015, 1 - 0.95 / H, f"Recipe ({TITLE[f]}): {RECIPES[f]}", 12.0, color="#16201d",
             fontstyle="italic")
    fig.text(0.015, 1 - 1.30 / H, "Each tile is a verdict a committed lane computed for this flavor (or reused with a "
             "cited justification). Tests not computed for it are absent here and grey in the comparison grid. "
             "The main board is v3's.", fontsize=10.5, color="#4d5a56")
    for k, title in enumerate(COLUMNS):
        ax.text(k + 0.03, nmax + 0.4, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
        for j, t in enumerate([t for t in tiles if t["col"] == k]):
            y = nmax - 0.5 - j
            msb._box(ax, k + 0.03, y - 0.46, 0.93, 0.90, t["st"])
            ax.text(k + 0.065, y + 0.33, t["name"], fontsize=10.4, fontweight="bold", color="white", va="center")
            lab = (t["lab"] or LAB[t["st"]]).upper()
            if t["comp"] != f:
                lab += "  ·  REUSED (" + t["ev"] + ")"
            ax.text(k + 0.065, y + 0.18, lab, fontsize=8.2, color="white", va="center", alpha=0.95)
            for i, ln in enumerate(_notes(t)):
                ax.text(k + 0.065, y + 0.03 - 0.1154 * i, ln, fontsize=7.8, color="white", va="center", alpha=0.97)
    lx, ly = 0.015, 0.95 / H
    for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN"):
        fig.patches.append(FancyBboxPatch((lx, ly - 0.01 * 13.2 / H), 0.014, 0.02 * 13.2 / H,
                                          boxstyle="round,pad=0,rounding_size=0.003", facecolor=COL[st],
                                          edgecolor="none", transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.019, ly, LAB[st], fontsize=10.5, va="center", color="#16201d")
        lx += 0.095
    foot = ("A cell is a computed verdict for that flavor; grey = not computed; nothing here says the data favour any "
            "flavor, including ΛCDM.")
    if f == "lcdm":
        foot += "  ΛCDM has a dark-matter particle, which the framework rules out for itself: this column is a reference."
    fig.text(0.015, 0.62 / H, foot, fontsize=9.0, va="center", color="#4d5a56")
    fig.text(0.015, 0.36 / H, "κ = ½ fitted; footings 9.3603e-11 / 1.1312e-10 m/s² never pooled. Lanes and reuse "
             "justifications: explainers/crispy_fried_chicken_flavors.md.", fontsize=9.0, va="center", color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


SHORT = {"PASS": "pass", "COND": "cond.", "FAIL": "fails", "UNDEC": "undec.", "OPEN": "open", None: "—"}


def draw_grid(cells, out):
    rows, col_of = grid_rows(cells)
    got = {(c["flavor"], c["row"]): c["st"] for c in all_cells(cells)}
    n = len(rows) + len(COLUMNS)                      # rows + one header line per column group
    rh, W = 0.25, 13.0
    H = 1.85 + rh * n + 1.0
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    ax = fig.add_axes([0.0, 1.0 / H, 1.0, (H - 1.85 - 1.0) / H])
    ax.set_xlim(0, W); ax.set_ylim(n, 0); ax.axis("off")
    fig.text(0.02, 1 - 0.45 / H, "Flavor comparison grid · 23 October 2026", fontsize=19, fontweight="bold",
             color="#16201d")
    fig.text(0.02, 1 - 0.85 / H, "Rows = tests (union of the flavor boards' tiles); columns = flavors. v3 is the main "
             "board. Colour = the verdict a committed lane computed for that flavor.", fontsize=9.5, color="#4d5a56")
    x0, cw = 5.6, 1.45
    for i, f in enumerate(FLAVORS):
        fig.text((x0 + cw * i + cw / 2) / W, 1 - 1.45 / H, TITLE[f], fontsize=11.5, fontweight="bold",
                 ha="center", color="#16201d")
    y, grp = 0, None
    for r in rows:
        if col_of[r] != grp:
            grp = col_of[r]
            ax.text(0.15, y + 0.6, COLUMNS[grp], fontsize=10.5, fontweight="bold", color="#16201d", va="center")
            y += 1
        ax.text(0.25, y + 0.5, r, fontsize=8.6, color="#16201d", va="center")
        for i, f in enumerate(FLAVORS):
            st = got.get((f, r))
            ax.add_patch(Rectangle((x0 + cw * i + 0.04, y + 0.08), cw - 0.08, 0.84,
                                   facecolor=COL[st] if st else GREY, edgecolor="none"))
            ax.text(x0 + cw * i + cw / 2, y + 0.5, SHORT[st], fontsize=8.2, ha="center", va="center",
                    color="white" if st else "#5b6469")
        y += 1
    k = counts(cells)
    line = "   ".join(f"{TITLE[f]}: {k[f]['PASS']}/{k[f]['COND']}/{k[f]['FAIL']}/{k[f]['UNDEC']}/{k[f]['OPEN']}/"
                       f"{k[f]['grey']}" for f in FLAVORS)
    fig.text(0.02, 0.70 / H, "a cell is a computed verdict for that flavor; grey = not computed; nothing here says the "
             "data favour any flavor, including ΛCDM", fontsize=9.5, color="#16201d", fontweight="bold")
    fig.text(0.02, 0.42 / H, "pass / cond. / fails / undec. / open / grey per column — " + line, fontsize=8.2,
             color="#4d5a56")
    fig.text(0.02, 0.17 / H, "ΛCDM has a dark-matter particle, which the framework rules out for itself; its column is "
             "a reference only. κ = ½ fitted. Justifications: crispy_fried_chicken_flavors.md.", fontsize=8.2,
             color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------------------
def _cell(cells, f, row):
    return next(c for c in cells if c["flavor"] == f and c["row"] == row)


def broken_cases():
    """Each case breaks one guard; check() must report at least one error for each."""
    def b1(c, r, v, l, d):   # plain-MOND cell reused from a v3 lane with its REUSE entry removed
        del r[("plain_mond", "Rotation curves (SPARC RAR)")]

    def b2(c, r, v, l, d):   # REUSE justification with no file:line
        r[("plain_mond", "Cluster cores (eRASS1 × KiDS)")] = ("v3", "F1", "same physics, trust me")

    def b3(c, r, v, l, d):   # cross-flavor borrowing: v4 takes P4's v3 rotation-curve verdict, no REUSE
        c.append(C("v4", 1, "Rotation curves (SPARC RAR)", "COND", "borrowed", ["P4"], comp="v3"))

    def b4(c, r, v, l, d):   # cross-flavor borrowing without even declaring it (claims P4 computed v4)
        c.append(C("v4", 1, "Galaxy groups (BFJR)", "COND", "borrowed", ["P4"]))

    def b5(c, r, v, l, d):   # a green with no verified evidence
        del v[("plain_mond", "Local a0 from MeerKAT")]

    def b6(c, r, v, l, d):   # a green whose verification names another lane
        v[("v4", "Solar system + Cassini (screened)")] = ("H2",) + v[("v4", "Solar system + Cassini (screened)")][1:]

    def b7(c, r, v, l, d):   # a cell better than its lane's verdict (P4 says COND)
        _cell(c, "plain_mond", "Rotation curves (SPARC RAR)")["st"] = "PASS"
        v[("plain_mond", "Rotation curves (SPARC RAR)")] = ("P4", "6c0249a8bc", "rerun")

    def b8(c, r, v, l, d):   # unjustified ΛCDM cell: the SPARC RAR from the canonical lane, no REUSE
        c.append(C("lcdm", 1, "Rotation curves (SPARC RAR)", "COND", "from literature", ["CFG695"], comp="canonical"))

    def b9(c, r, v, l, d):   # ΛCDM cell from a literature claim, no lane on record
        c.append(C("lcdm", 0, "Binary pulsars + GW170817", "COND", "GR agrees (literature)", ["LIT"]))

    def b10(c, r, v, l, d):  # ΛCDM Newtonian reuse with its justification stripped of file:line
        r[("lcdm", "Outer globular clusters")] = ("newton", "D10", "Newton is fine")

    def b11(c, r, v, l, d):  # plain MOND given a cosmology verdict (lane and verdict faked so only this guard bites)
        c.append(C("plain_mond", 3, "Linear growth, v3 Khronon", "FAIL", "no cosmology", ["S1"]))
        d[("S1", "plain_mond", "Linear growth")] = ("FAIL", "S1 README L1")

    def b12(c, r, v, l, d):  # a lane registered without the flavor it is used for
        l["H2"] = dict(flavors={"canonical"}, where="x:L1")

    def b13(c, r, v, l, d):  # canonical green the earlier board never drew, no verification (verdict faked to PASS)
        _cell(c, "canonical", "Dwarf cold supply (chemistry)")["st"] = "PASS"
        d[("E6", "canonical", "Dwarf cold supply (chemistry)")] = ("PASS", "E6 README L1")

    def b14(c, r, v, l, d):  # an OPEN cell where the lane's verdict is a fail
        _cell(c, "v4", "Cluster cores (eRASS1 × KiDS)")["st"] = "OPEN"

    def b15(c, r, v, l, d):  # ΛCDM coloured on a galaxy-formation row by a lane with a ΛCDM arm (verdict faked)
        c.append(C("lcdm", 1, "Local a0 from MeerKAT", "PASS", "halo fits", ["C2"]))
        v[("lcdm", "Local a0 from MeerKAT")] = ("C2", "5e93769089", "rerun")
        d[("C2", "lcdm", "Local a0 from MeerKAT")] = ("PASS", "C2 README L172")

    def b16(c, r, v, l, d):  # a ΛCDM green with no verification (the withheld linear growth turned green)
        _cell(c, "lcdm", "Linear growth")["st"] = "PASS"

    def b17(c, r, v, l, d):  # a verdict citation with no file:line
        d[("H2", "v4", "Cluster cores (eRASS1 × KiDS)")] = ("FAIL", "somewhere")

    def b18(c, r, v, l, d):  # ΛCDM satellites from G2's PAPER36 route (framework law), with a cited REUSE entry
        c.append(C("lcdm", 2, "Dwarf satellites (Moster+13 + NFW route)", "FAIL", "PAPER36 eq. 1", ["G2"],
                   comp="canonical"))
        r[("lcdm", "Dwarf satellites (MW / M31)")] = ("canonical", "G2", "G2 README L91")

    def b19(c, r, v, l, d):  # ΛCDM reuses a framework-law verdict on a row not forced grey (only the new guard bites)
        c.append(C("lcdm", 2, "Dwarf cold supply (chemistry)", "COND", "borrowed", ["E6"], comp="canonical"))
        r[("lcdm", "Dwarf cold supply (chemistry)")] = ("canonical", "E6", "E6 README L1")

    def b20(c, r, v, l, d):  # G2 registered as computing ΛCDM directly, with no cited ΛCDM arm
        l["G2"] = dict(flavors={"canonical", "lcdm"}, where="G2 README L91")

    return [("plain-MOND reuse with its REUSE entry removed", b1), ("REUSE justification without file:line", b2),
            ("v4 borrows a v3 verdict without REUSE", b3), ("v4 borrows a v3 lane as if it computed v4", b4),
            ("green without verified evidence", b5), ("green verified by another lane", b6),
            ("cell better than its lane's verdict", b7), ("unjustified ΛCDM cell (canonical lane, no REUSE)", b8),
            ("ΛCDM cell from a literature claim (no lane)", b9), ("ΛCDM Newtonian reuse without file:line", b10),
            ("plain MOND given a cosmology verdict", b11), ("lane registry lacks the flavor", b12),
            ("canonical green the earlier board never drew", b13), ("OPEN where the lane says fails", b14),
            ("ΛCDM coloured on a galaxy-formation row", b15), ("ΛCDM green with no verification", b16),
            ("verdict citation without file:line", b17),
            ("ΛCDM satellites from G2's framework-law route", b18),
            ("ΛCDM reuse of a framework-law verdict", b19), ("lane registered for ΛCDM without a ΛCDM arm", b20)]


def selftest():
    base = check(copy.deepcopy(CELLS))
    print(f"clean flavor boards: {len(base)} errors" + (f"  ->  {base[0]}" if base else ""))
    bad = 1 if base else 0
    for label, fn in broken_cases():
        c, r, v = copy.deepcopy(CELLS), copy.deepcopy(REUSE), copy.deepcopy(VERIFIED_GREEN_F)
        l, d = copy.deepcopy(LANES), copy.deepcopy(VERDICTS)
        fn(c, r, v, l, d)
        e = check(c, r, v, l, d)
        print(f"  {'CAUGHT' if e else 'MISSED'}: {label}" + (f"  ->  {e[0]}" if e else ""))
        bad += 0 if e else 1
    print("SELFTEST PASS: every broken case caught; nothing written." if not bad else "SELFTEST FAIL")
    sys.exit(0 if not bad else 1)


def main():
    if "--selftest" in sys.argv[1:]:
        selftest()
    mutate = "--mutate" in sys.argv[1:]
    cells, reuse = copy.deepcopy(CELLS), copy.deepcopy(REUSE)
    if mutate:
        del reuse[("lcdm", "Tidal dwarfs, NGC 1052-DF2/DF4")]       # strip one REUSE justification
    errs = check(cells, reuse)
    k = counts(cells)
    for f in FLAVORS:
        print(f"{TITLE[f]:>16}: pass {k[f]['PASS']}, cond {k[f]['COND']}, fail {k[f]['FAIL']}, undec {k[f]['UNDEC']}, "
              f"open {k[f]['OPEN']}, grey {k[f]['grey']}")
    print(f"reused cells: {sum(1 for c in cells if c['comp'] != c['flavor'])} (REUSE entries {len(reuse)})")
    if errs:
        for e in errs:
            print("CHECK FAIL:", e)
        print("MUTATE: checks failed as required; nothing written." if mutate else "nothing written.")
        sys.exit(1)
    if mutate:
        print("MUTATE: checks did NOT catch the stripped justification")
        sys.exit(2)
    for f, name in OUT_BOARD.items():
        draw_board(f, cells, os.path.join(IMG, name))
    draw_grid(cells, os.path.join(IMG, OUT_GRID))
    print("all checks PASS; wrote", ", ".join(f"explainers/img/{n}" for n in list(OUT_BOARD.values()) + [OUT_GRID]))


if __name__ == "__main__":
    main()
