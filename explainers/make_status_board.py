#!/usr/bin/env python3
"""The Crispy Fried Chicken status board, 1 November 2026: the a0 law alone. Plot only.

The owner's rule of 23 October: the board shows the current best theory only. The owner retired route E's cold sector on
1 November (rebuild_2026_10_22/OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md), so that theory is now the law,
g_N = g^2/(g + a0), a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED. The last fold before this was v3s (24 October); the
board never carried route E. Every tile is rebuilt from FG1's C4 and alt rows and the lanes PAPER67 cites.

A colour restates a recorded verdict, and check_law() holds it there:
  * a tile naming an FG1 line takes its colour from FG1's README, read at build time, one colour per footing; NOT GRADED
    must be grey, and the eleven lines must all be on the board;
  * footings are never pooled: a tile whose footings differ is drawn in two halves;
  * green needs a passing FG1 row, or a VERIFIED_GREEN entry (lane, result commit, rerun);
  * every tile names lanes in SOURCES, each with a committed file, and each quoted number is checked against that file;
  * a verdict colour can't rest on a lane that computed only v3 or v3s (V3S_ONLY);
  * no tile of the v3s board vanishes: it is here (LAW_RENAMES), or in LAW_RETIRED with its old colour and a reason;
  * grey is for a tile with no graded number for the law, and it must give its reason.

status_board_v3s_2026_10_24.py is the v3s generator, kept. make_flavor_boards.py and Y1 read TILES, ARCHIVE, check and
friends through this module, and those names still mean v3s, so their v3 rows don't silently become the law. The law's
own names start with LAW_.

Run:  OMP_NUM_THREADS=1 python3 explainers/make_status_board.py            (writes explainers/img/status_board.png)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --mutate   (strips one tile's lane; must FAIL, writes nothing)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --selftest (broken cases; every one must be caught)
      OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --md       (prints the tile table for the board's md)
One core, seconds, < 0.3 GB.

kappa = 1/2 is FITTED; footings never pooled; the theory is not closed; nothing here says the data favour the framework.
"""
import copy
import os
import re
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from status_board_v3s_2026_10_24 import (ARCHIVE, COL, COLUMNS, INK, LAB, PREVIOUS_BOARD, RECIPE, TILES, _box, _fit,  # noqa: F401
                                         check)

REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "img", "status_board.png")
LAW_LAB = dict(LAB, STALE="no graded number for the law")
LAW_COLUMNS = ["Relativity (the law has no action)", "Isolated galaxies", "Where the law misses",
               "a0 over time, the CMB, dated tests", "The deep 'why'; tiles not regraded"]
LAW_RECIPE = ("Crispiest recipe (the a₀ law): g_N = g²/(g + a₀), a₀ = κ c √(G ρ_DE), κ = ½ fitted. Nothing else: no "
              "action, no screen, no dust term. The simple form is Milgrom's; the tie to dark energy was proposed earlier.")

_Q, _C, _P = "rebuild_2026_10_22/", "campaign_fresh_gravity/", "qwen_claude_field_theory/papers_2026/"
FG1_README = _Q + "FG1_final_grade/README.md"
# lane -> the committed file(s) its numbers are checked against
SOURCES = {
    "FG1": FG1_README, "NR2": _Q + "NR2_low_mass_ng80/README.md", "ND1": _Q + "ND1_native_dwarfs/README.md",
    "RF2": _Q + "RF2_ic1613_inclination_footing/README.md", "RF5": _Q + "RF5_growth_native_yardstick/README.md",
    "X5": _Q + "X5_mw_joint_baryons/README.md", "CS2": _Q + "CS2_core_law_out_of_sample/README.md",
    "HO1": _Q + "HO1_xcop_hotgas_heldout/README.md", "HS1": _Q + "HS1_hsb_lsb_residual_slope/README.md",
    "UL1": (_Q + "UL1_measured_upsilon_test/README.md", _Q + "UL1_measured_upsilon_test/ul1.out"),
    "OD1": _Q + "OD1_old_disc_ruler/README.md", "BL1": _Q + "BL1_blue_lens_halo_mass/README.md",
    "S1": _Q + "S1_v3_hosted_small/README.md", "S2": _Q + "S2_v3_lowg_lensing/README.md",
    "S3": _Q + "S3_v3_mw_seals/README.md", "S4": _Q + "S4_v3_muK_clusters/README.md",
    "P4": _Q + "P4_v3_galaxy_tiles/README.md", "U1": _Q + "U1_v3_dust_content/README.md",
    "F1": _Q + "F1_cluster_cores/README.md", "DR1": _Q + "DR1_density_term_law/README.md",
    "LW1-CRITERIA": _Q + "LW1_law_scorecard/FROZEN_CRITERIA.md", "AC1": _Q + "AC1_alma_condor_predictions/README.md",
    "SP1": _Q + "SP1_sealed_lensing_step/README.md", "SP2": _Q + "SP2_sealed_basin_lensing/README.md",
    "LEDGER": _Q + "CLOSING_LEDGER_2026-11-01_DRAFT.md", "OWNER-11-01": _Q + "OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md",
    "V3S-VERDICT": "covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md",
    "E2": "doors_push_2026_10_22/E2_field_equation/README.md", "D10": "doors_push_2026_10_22/D10_native_Lstar/README.md",
    "CFG303": _C + "CFG303_lcdm_free_inputs/README.md", "CFG307": _C + "CFG307_aless122_stress_test/README.md",
    "CFG308": _C + "CFG308_cristal_stress_test/README.md", "CFG528": _C + "CFG528_sluggs_centrals_mechanism/README.md",
    "CFG576": _C + "CFG576_diskmass_sigz/README.md", "CFG577": _C + "CFG577_diskmass_grid/README.md",
    "CFG687": _C + "CFG687_erass1_shear_stack/README.md", "CFG689": _C + "CFG689_native_ruler_bao/README.md",
    "CFG829": _C + "CFG829_lensing_low_g_vs_dwarf_excess/README.md", "CFG894": _C + "CFG894_kappa_campaign_ledger/README.md",
    "CFG956": _C + "CFG956_a0z_wave_bound/README.md", "CFG957": _C + "CFG957_a0z_wave_models_observables/README.md",
    "MI-PROFILE": "real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out",
    "DR4-PREREG": "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md",
    "PAPER60": _P + "PAPER60_scope_of_the_screened_theory_2026.tex",
    "PAPER67": _P + "PAPER67_DRAFT_galaxy_law_and_what_it_leaves_2026.tex",
}
# Lanes that computed only v3 or v3s: a grey tile may name them for the record; a verdict colour may not rest on them.
V3S_ONLY = {"U1", "S1", "S3", "S4", "D10", "V3S-VERDICT"}
FG1_LINES = ("S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC")
FG1_COLOUR = {"PASS": "PASS", "FAIL": "FAIL", "NOT GRADED": "STALE"}
# Greens from outside FG1: tile -> (lane, result commit, how it was verified, stated as it is). FG1's own greens rest on
# 1c8d43d901 and on CRG1's regrade 83002f24a2, which recomputed C4's S, Tl, LT, G and Ln (mainly a test of code).
VERIFIED_GREEN = {
    "Surface brightness at fixed speed": ("HS1", "573bc465e9", "frozen class FLAT, MUTATE twin caught, literals in PAPER67's audit; "
                                          "NOT rerun on 11-01: its chain wouldn't run outside its own folder"),
    "Local a0 from MeerKAT": ("P4", "6c0249a8bc", "coordinator rerun 2026-10-23, read in PAPER60's audit"),
}
MUST_STAY_RED = ["The law vs Cassini (unscreened)", "MW vertical force", "MW outer slope (Gaia)", "IC 1613",
                 "Local Group dwarfs (five classes)", "Cluster cores (318 eRASS1)", "Cluster keys (15, old template)"]
BANNED = ("theory closed", "cold dark matter", "cdm-like", "cold energy", "5.364", "favour the framework", "zimmerman")
WRAP, MAXL = 56, 5


def L(col, name, st, note, lanes, q, fg1=None, alt=None, lab=None):
    """One tile. q: [(fragment in the note, lane, literal in that lane's file), ...]. fg1: the FG1 line it restates.
    alt: the alt footing's colour, only where it differs from canonical's."""
    return dict(col=col, name=name, st=st, note=note, lanes=list(lanes), q=list(q), fg1=fg1, alt=alt, lab=lab)


_NOACT = ("no action", "PAPER67", "None is selected")
LAW_TILES = [
    # ---- column 0: relativity. No action means no number; the v3s results were that model's. ----
    L(0, "The law vs Cassini (unscreened)", "FAIL",
      "Q₂ 2.44–4.59× the 2σ line, alt 2.85–5.19×. Not a control any more: the law as written needs a screen it "
      "doesn't contain",
      ["E2", "PAPER67"],
      [("2.44–4.59×", "E2", "**2.44–4.59×**"), ("2.85–5.19×", "E2", "**2.85–5.19×**"),
       ("needs a screen", "PAPER67", "needs a screen it doesn't contain")], lab="fails, both footings"),
    L(0, "An action", "STALE", "no action selected; the covariant attempt (v3s) is closed and the a₀ sector's action "
      "stays open. Not a pass and not a fail: an unanswered gap",
      ["PAPER67", "OWNER-11-01", "V3S-VERDICT"],
      [("no action", "PAPER67", "None is selected"), ("covariant attempt (v3s) is closed", "PAPER67",
       "covariant attempt (v3s) is closed"), ("stays open", "OWNER-11-01", "The a₀ sector's action stays open")],
      lab="no action, no number"),
    L(0, "Gravity waves at light speed", "STALE", "no action, so no wave equation to test. v3s's pass was that "
      "model's", ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Binary pulsars + GW170817", "STALE", "no action, so no radiative sector to test. v3s's pass was that "
      "model's", ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Health: ghosts, gradients", "STALE", "no action, so no modes to check. v3s's conditional was that "
      "model's", ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Causality: criterion A / B", "STALE", "no action, so no signal speeds to read. v3s's reading was that "
      "model's", ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Strong coupling", "STALE", "no action, so no cutoff to estimate. v3s's estimate was that model's",
      ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Radiative stability (G12)", "STALE", "no action, so nothing to renormalise. It stayed grey on v3s too",
      ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    L(0, "Matter conservation (G9)", "STALE", "the Bianchi argument needs a diffeomorphism-invariant action, and the "
      "law has none", ["PAPER67", "V3S-VERDICT"], [("has none", "PAPER67", "None is selected")],
      lab="no action, no number"),
    L(0, "Black holes (EHT, LIGO ringdown)", "STALE", "no action, so no strong-field solution. v3s's conditional was "
      "that model's", ["PAPER67", "V3S-VERDICT"], [_NOACT], lab="no action, no number"),
    # ---- column 1: isolated galaxies ----
    L(1, "Rotation curves (SPARC RAR)", "PASS",
      "canonical Υ 0.52, rms 0.0541; alt Υ 0.44, rms 0.0537, below the 0.50–0.80 line. That line's lower edge is a "
      "population model's value. χ² line fails both (P4)",
      ["FG1", "NR2", "PAPER67", "P4"],
      [("Υ 0.52, rms 0.0541", "FG1", "U 0.52/0.52, rms 0.0541/0.0541"), ("Υ 0.44, rms 0.0537", "FG1",
       "U 0.44/0.44, rms 0.0537/0.0537"), ("lower edge", "PAPER67", "its lower edge is a population model's central value"),
       ("χ² line fails both", "P4", "The χ² line FAILS on both footings")], fg1="S", alt="FAIL"),
    L(1, "Tilt with speed", "PASS", "+0.02, alt −0.02", ["FG1", "NR2"],
      [("+0.02", "FG1", "+0.02/+0.02"), ("−0.02", "FG1", "-0.02/-0.02")], fg1="Tl"),
    L(1, "LITTLE THINGS dwarfs", "PASS", "median E −0.025, alt −0.064", ["FG1", "NR2"],
      [("−0.025", "FG1", "-0.025/-0.025"), ("−0.064", "FG1", "-0.064/-0.064")], fg1="LT"),
    L(1, "Surface brightness at fixed speed", "PASS",
      "slope −0.016 ± 0.061, alt −0.023 ± 0.063 per dex at 60–120 km/s, 47 galaxies: FLAT, frozen; stays flat on the "
      "post-result cuts. Separates the law from the retired halos only",
      ["HS1", "PAPER67"],
      [("−0.016 ± 0.061", "HS1", "**−0.016**"), ("−0.023 ± 0.063", "HS1", "−0.023 | ±0.063"), ("47 galaxies", "HS1",
       "from 47 galaxies"), ("flat on the", "HS1", "The law stays flat on every cut"), ("retired halos only", "PAPER67",
       "between the law and these halos only")], lab="pass, both footings"),
    L(1, "Galaxy groups (BFJR)", "PASS",
      "63 groups, Z +0.31, alt −0.31, isolated. Above the law if g_e reaches 0.03 a₀ (P4); no group field on disk",
      ["FG1", "NR2", "PAPER67", "P4"],
      [("Z +0.31", "FG1", "Z +0.31"), ("−0.31", "FG1", "Z -0.31"), ("63 groups", "PAPER67", "63 groups"),
       ("0.03 a₀", "P4", "ABOVE LAW at g_e = 0.03 a₀")], fg1="G"),
    L(1, "Local a0 from MeerKAT", "PASS",
      "a₀ 1.31e-10 against SPARC's same recipe 1.21e-10: +0.032 dex, line 0.15. A fit of a₀ itself, so one number",
      ["PAPER60", "P4", "PAPER67"],
      [("+0.032 dex, line 0.15", "PAPER60", "+0.032$\\,dex (line 0.15)"), ("1.31e-10", "P4", "**1.31e-10**"),
       ("1.21e-10", "P4", "1.21e-10")], lab="pass"),
    L(1, "Isolated-galaxy lensing, shape", "PASS",
      "ENV2H−H2H −463.6, alt −492.9 against the retired halos; the rule's first term is zero by construction. Shape "
      "only: no tested model fits these profiles in absolute terms",
      ["FG1", "NR2", "PAPER67"],
      [("−463.6", "FG1", "ENV2H-H2H -463.6"), ("−492.9", "FG1", "ENV2H-H2H -492.9"), ("zero by construction", "FG1",
       "zero by construction"), ("no tested model fits", "PAPER67", "No tested model fits these profiles")],
      fg1="Ln", lab="pass as frozen: shape, not amplitude"),
    L(1, "Isolated-galaxy lensing, inner", "COND",
      "blue A 1.016 ± 0.086 (CFG829); 0.878 / 0.802 with a hot gas inventory (BL1). The amplitude depends on that "
      "inventory; S2's class",
      ["CFG829", "BL1", "S2", "PAPER67"],
      [("1.016 ± 0.086", "CFG829", "**1.016 ± 0.086**"), ("0.878 / 0.802", "BL1", "0.878 / 0.802"),
       ("depends on", "PAPER67", "amplitude depends on colour and on the baryon inventory")]),
    L(1, "Red (early-type) lenses", "COND",
      "A 1.587 (CFG829); 1.313 / 1.200 with hot gas (BL1): short. Only CFG667 + an IMF α–σ relation reach 1.020 / "
      "0.933 (S2)",
      ["CFG829", "BL1", "S2", "PAPER67"],
      [("1.587", "CFG829", "1.587 ± 0.076"), ("1.313 / 1.200", "BL1", "1.313 / 1.200"), ("1.020 /", "S2", "1.020 / 0.933")]),
    # ---- column 2: where the law misses ----
    L(2, "MW vertical force", "FAIL",
      "7 of 175 cells pass (alt 4), wide priors, short disc only; those have K_z 76.7–80.9 against 66.4 ± 2.2, +4.7 to "
      "+6.6σ. X5 stands in for RF1, which has no law row",
      ["FG1", "X5"],
      [("7 of 175", "FG1", "7 of 175 cells (alt 4)"), ("+4.7 to +6.6σ", "FG1", "K_z +4.7 to +6.6 sigma"),
       ("76.7–80.9", "X5", "76.7–80.9 against 66.4 ± 2.2"), ("stands in", "FG1", "X5's AQUAL row stands in")], fg1="MW"),
    L(2, "MW outer slope (Gaia)", "FAIL", "SHAPE EXCLUDED ROBUST: Z −3.88, alt −4.09, on the short-disc cells too",
      ["X5", "PAPER67"], [("Z −3.88", "X5", "Z −3.88"), ("−4.09", "X5", "Z −4.09"), ("short-disc cells", "PAPER67",
                                                                                     "leave the outer slope excluded")],
      lab="fails, both footings"),
    L(2, "IC 1613", "FAIL",
      "E −0.593, Z −7.9 on both footings; fails under every halo-free inclination. One galaxy: disfavoured, not excluded",
      ["FG1", "ND1", "RF2"],
      [("E −0.593, Z −7.9", "FG1", "E -0.593 (Z -7.9)"), ("every halo-free inclination", "RF2",
       "FAILS under every halo-free inclination"), ("disfavoured, not excluded", "RF2", "disfavoured, not excluded")], fg1="IC"),
    L(2, "Local Group dwarfs (five classes)", "FAIL",
      "Z MW ultra-faint +5.22, bright M31 +2.20, M31 others +2.29, MW classical +1.69, field +0.57; alt +4.87, +1.81, "
      "+2.12, +1.42, +0.08. No external-field term",
      ["FG1", "NR2"],
      [("+5.22", "FG1", "MW ultra-faint +5.22; bright M31 +2.20; M31 others +2.29; MW classical +1.69; LG field +0.57"),
       ("+4.87", "FG1", "MW ultra-faint +4.87; bright M31 +1.81; M31 others +2.12; MW classical +1.42; LG field +0.08"),
       ("No external-field term", "FG1", "no external-field term in X51's path")], fg1="Dw"),
    L(2, "Measured stellar masses", "FAIL",
      "60–150 km/s: law Υ 0.62, 0.65 against GSWLC 0.277, 0.304; Z +3.4, +5.6, alt +2.8, +4.6. Estimators against W1, "
      "not a 3.6 μm measurement",
      ["UL1", "PAPER67"],
      [("0.62, 0.65", "UL1", "| law canonical | 0.62 | 0.65 |"), ("0.277, 0.304", "UL1", "| GSWLC (W1 chain) | 0.277 | 0.304 |"),
       ("+3.4, +5.6", "UL1", "| Z GSWLC | +3.4 | +5.6 |"), ("+2.8, +4.6", "UL1", "GSWLC: Z +2.8 +4.6 +0.7 +1.3 +1.7"),
       ("not a 3.6", "PAPER67", "not a 3.6\\,$\\mu$m measurement")], lab="fails the frozen gate, both footings"),
    L(2, "Cluster cores (318 eRASS1)", "FAIL",
      "A 1.91 ± 0.12, alt 1.75 ± 0.11 at 0.5–1.2 Mpc; rebuilt, 1.68–1.72, alt 1.54–1.58 (F1). At 1.2–3 Mpc 1.01 ± 0.09, "
      "alt 0.93 ± 0.08. No account from the law",
      ["CFG687", "F1", "PAPER67"],
      [("1.91 ± 0.12", "CFG687", "**1.91 ± 0.12**"), ("1.75 ± 0.11", "CFG687", "**1.75 ± 0.11**"),
       ("1.68–1.72", "F1", "1.68–1.72 ± 0.12"), ("1.54–1.58", "F1", "1.54–1.58 ± 0.11"),
       ("1.01 ± 0.09", "CFG687", "**1.01 ± 0.09**"), ("0.93 ± 0.08", "CFG687", "**0.93 ± 0.08**")],
      lab="fails, both footings"),
    L(2, "Cluster keys (15, old template)", "FAIL",
      "6 of 15 fail, alt 10; worst G-MID-T3 +4.46, alt +4.11, on f★ 0.20 with no gas tail. DR1's plain law on measured "
      "gas: 10 of 15 pass, G-OUT-M3 +4.76",
      ["FG1", "NR2", "DR1"],
      [("6 of 15", "FG1", "9 of 15, over 2 in either h"), ("alt 10", "FG1", "5 of 15, over 2 in either h"),
       ("+4.46", "FG1", "G-MID-T3 +4.46"), ("+4.11", "FG1", "G-MID-T3 +4.11"), ("no gas tail", "FG1", "f★ 0.20 with no gas tail"),
       ("10 of 15 pass, G-OUT-M3 +4.76", "DR1", "| **+0.467, 0.476** | **10** | **+4.76** |")], fg1="K"),
    L(2, "Outer shear against gas mass", "FAIL",
      "ΔΣ_OUTER ∝ M_gas^s, s 0.90 ± 0.21 against the law's 0.47 and Newton's 0.84. The amplitude match is an average "
      "over a slope the law misses",
      ["CFG687", "PAPER67"],
      [("s 0.90 ± 0.21", "CFG687", "s = 0.90 ± 0.21 vs the law's s = 0.47 and Newton's 0.84"),
       ("a slope the law misses", "PAPER67", "over a slope the law misses")], lab="fails as frozen (T2)"),
    L(2, "X-COP", "STALE",
      "FG1 shows CS2's −0.151, rms 0.205, numbers only; that row carries a Burkert core, so it isn't the plain law. "
      "DR1's plain-law row: +0.467, 0.476. No grade",
      ["FG1", "CS2", "DR1", "LW1-CRITERIA"],
      [("numbers only", "FG1", "-0.151, 0.205 [READ HO1, numbers only]"),
       ("Burkert core", "LW1-CRITERIA", "CS2's mc is a Burkert core law"), ("+0.467, 0.476", "DR1", "**+0.467, 0.476**")],
      fg1="X", lab="not graded by FG1"),
    L(2, "DiskMass", "STALE",
      "r 1.250 (alt 1.212), 1.342 on the exact integral; target 0.90–1.10. Lanes frozen inconclusive and their ν isn't "
      "the law's, so no grade; OD1: NOT SEPARATED",
      ["FG1", "CFG576", "CFG577", "OD1", "LW1-CRITERIA"],
      [("r 1.250 (alt 1.212), 1.342", "FG1", "r 1.250 (alt 1.212) CFG576, 1.342 CFG577"),
       ("frozen inconclusive", "FG1", "both lanes are frozen INCONCLUSIVE"), ("isn't", "LW1-CRITERIA", "CFG576/577 use a different nu"),
       ("NOT SEPARATED", "OD1", "NOT SEPARATED")],
      fg1="DM", lab="not graded by FG1"),
    # ---- column 3: a0 over time, the CMB, dated tests ----
    L(3, "a0(z): native band vs a0 ~ H(z)", "UNDEC",
      "0.91 [0.76, 1.03] at z 1, 0.94 [0.71, 1.12] at z 1.5; rival 1.76, 2.35. Needs 0.055 dex at z 1; best sample "
      "0.4–0.5. The band uses a CMB cold mass, a retired input",
      ["CFG689", "PAPER67"],
      [("0.91 [0.76, 1.03]", "CFG689", "0.91 [0.76, 1.03]"), ("0.94 [0.71, 1.12]", "CFG689", "0.94 [0.71, 1.12]"),
       ("1.76", "CFG689", "| 1.76 |"), ("2.35", "CFG689", "| 2.35 |"), ("0.055 dex", "CFG689", "0.055 / 0.072 / 0.074 / 0.084 dex"),
       ("0.4–0.5", "CFG689", "best 0.4–0.5 dex"), ("retired input", "PAPER67", "isn't free of the retired sector's input")]),
    L(3, "CMB", "STALE",
      "a₀ is absent from the linear FRW equations, so the law can't act there. The record has no CMB pass without a "
      "dust-like term; the law offers none. Open, unanswered",
      ["RF5", "PAPER67", "OWNER-11-01"],
      [("absent from the linear FRW", "RF5", "a₀ is absent from the linear FRW equations"),
       ("no CMB pass", "PAPER67", "no CMB pass without a dust-like component"), ("offers none", "PAPER67", "The law offers no replacement"),
       ("unanswered", "OWNER-11-01", "open and unanswered")], lab="no account from the law"),
    L(3, "Linear growth", "STALE",
      "the law can't act on linear FRW. The window z_on 3e4–1e6 belongs to a dust component it doesn't have; v3's red "
      "tile is on the kept board",
      ["RF5", "PAPER67"],
      [("linear FRW", "RF5", "a₀ is absent from the linear FRW equations"), ("3e4–1e6", "RF5", "z_on ∈ [3e4, 1e")],
      lab="no account from the law"),
    L(3, "High-z on halo-free inputs", "STALE",
      "S4's classes were not decidable with the law's kernel swapped in, on v3's board; not in FG1 or PAPER67, so not "
      "regraded here", ["CFG303", "S4"], [("classes", "S4", "keep their classes")], lab="not regraded for the law"),
    L(3, "CRISTAL z~5 / ALESS 122.1", "STALE",
      "S4's classes were not robust, not discriminating; not in FG1 or PAPER67, so not regraded here",
      ["CFG307", "CFG308", "S4"], [("classes", "S4", "keep their classes")], lab="not regraded for the law"),
    L(3, "ALMA U4 (6 Nov), GS4 (28 Nov)", "OPEN",
      "U4_28473, public 2026-11-06 02:42:31 UTC: tests its mass budget, not a₀(z); one disc excludes no model. "
      "GS4_24110 2026-11-28 by earlier metadata, ≤ 0.51σ on n = 1 vs 2",
      ["LEDGER", "AC1", "PAPER67"],
      [("02:42:31 UTC", "LEDGER", "U4_28473, CO(3-2), public 2026-11-06 02:42:31 UTC"),
       ("one disc excludes no model", "LEDGER", "one disc excludes no model"), ("2026-11-28", "LEDGER", "2026-11-28 by earlier metadata"),
       ("0.51σ", "PAPER67", "at or below 0.51$\\sigma$")], lab="open: dated"),
    L(3, "Gaia DR4 wide binaries (Dec)", "OPEN",
      "Newton 1.000, AQUAL point 1.137, MOND's benchmark 1.33. The bare law has no gate, so Newton at 2–30 kAU would "
      "count against it: a reading, not a frozen line",
      ["DR4-PREREG", "PAPER67"],
      [("1.137", "DR4-PREREG", "1.137 (computed 1.1389)"), ("1.33", "DR4-PREREG", "| conventional-MOND benchmark | 1.33"),
       ("count against it", "PAPER67", "would count against it"), ("not a frozen line", "PAPER67", "Reading, not a frozen line")],
      lab="open: dated"),
    L(3, "Gaia DR4 MW predictions", "OPEN",
      "sealed files scored as frozen, v3's among them; no seal reopened or edited. Their rows are not the bare law's",
      ["OWNER-11-01", "S3"],
      [("scored as frozen", "OWNER-11-01", "Scored as frozen"), ("no seal", "OWNER-11-01", "No seal is reopened or edited")],
      lab="open: dated"),
    L(3, "The owner's wave a0(z) idea", "STALE",
      "the lanes ran: a bound from the expansion data and a model list. A bound on a wave is not evidence for a wave; "
      "not in FG1 or PAPER67",
      ["CFG956", "CFG957"], [("A bound on a wave", "CFG956", "A bound on a wave is not evidence for a wave")],
      lab="not regraded for the law"),
    # ---- column 4: the deep 'why', and tiles not regraded ----
    L(4, "Why kappa = 1/2", "OPEN",
      "fitted; 537 attempts, none derives it. SPARC best fit 1.0766e-10: κ = ½ Δχ² 63.90 (1.82σ), alt 7.04 (0.60σ), "
      "Milgrom's cH₀/2π 5.34 (0.53σ), which fits at least as well",
      ["PAPER67", "CFG894", "MI-PROFILE"],
      [("537 attempts", "PAPER67", "537 attempts"), ("1.0766e-10", "MI-PROFILE", "1.0766e-10"),
       ("63.90 (1.82σ)", "MI-PROFILE", "0.9361   0.8696    63.90     7.99     1.82"),
       ("7.04 (0.60σ)", "MI-PROFILE", "1.1300   1.0496     7.04     2.65     0.60"), ("5.34 (0.53σ)", "PAPER67", "5.34 (0.53$\\sigma$)")],
      lab="open: fitted"),
    L(4, "The matter term", "STALE",
      "ρ_DE comes from an expansion history whose matter term is several times the baryons. The law doesn't explain "
      "it, and it has no replacement for the retired sector",
      ["PAPER67", "OWNER-11-01"],
      [("several times the baryons", "PAPER67", "several times the baryons")], lab="no account from the law"),
    L(4, "Tidal dwarfs, NGC 1052-DF2/DF4", "STALE",
      "v3's green came from its dust theorem (U1), gone with v3. P4 read −0.59 / −0.62 dex and −1.66 / −1.74 ln, FAIL "
      "there, but with a screen on; not in FG1 or PAPER67",
      ["P4", "U1"],
      [("−0.59 / −0.62 dex", "P4", "**−0.59 / −0.62 dex**"), ("−1.66 / −1.74 ln", "P4", "**−1.66 / −1.74 ln**"),
       ("dust theorem", "U1", "T3")], lab="not regraded for the law"),
    L(4, "Central ellipticals (SLUGGS)", "STALE",
      "S4 read 2.8σ → 3.1σ with the law's kernel, on v3's board; not in FG1 or PAPER67, so not regraded here",
      ["CFG528", "S4"], [("2.8σ → 3.1σ", "S4", "the tension rises from 2.8σ to 3.1σ")], lab="not regraded for the law"),
    L(4, "Coma ultra-diffuse galaxies", "STALE",
      "S1 read +1.12 / +1.08 dex in Coma's field, with v3's screen on; not in FG1 or PAPER67, so not regraded here",
      ["S1"], [("+1.12 / +1.08 dex", "S1", "+2.581 (+1.121)"), ("+1.12 / +1.08 dex", "S1", "+2.481 (+1.078)")],
      lab="not regraded for the law"),
    L(4, "Outer globulars", "STALE",
      "D10 measured v3's screening length, not the bare law. The law has no screen; not in FG1 or PAPER67, so not "
      "regraded here",
      ["D10"], [("screening length", "D10", "the L★ floor measured")], lab="not regraded for the law"),
]
LAW_EXTRA_TILES = {"Tilt with speed", "LITTLE THINGS dwarfs", "Surface brightness at fixed speed", "IC 1613",
                   "Measured stellar masses", "Cluster keys (15, old template)", "Outer shear against gas mass", "X-COP",
                   "DiskMass"}
# v3s tile -> its name here, where the name was about a retired model.
LAW_RENAMES = {
    "Unscreened law vs Cassini": "The law vs Cassini (unscreened)", "Covariant completion": "An action",
    "Isolated-galaxy lensing, all radii": "Isolated-galaxy lensing, shape", "MW vertical force (round rule)": "MW vertical force",
    "Dwarf satellites vs screened law": "Local Group dwarfs (five classes)", "Cluster cores (326 eRASS1)": "Cluster cores (318 eRASS1)",
    "Native CMB (patched CLASS)": "CMB", "Linear growth, v3 Khronon": "Linear growth",
    "What sets the cold-mass amount": "The matter term", "Outer globulars: L* floor": "Outer globulars",
}
# Tiles of the v3s board that test something the law doesn't contain: old colour, why, the law's counterpart.
LAW_RETIRED = {
    "Leaf problem well-posed": ("COND", "v3s's (P, lapse) field problem; the law has no such fields", "An action"),
    "Solar system + Cassini (screened)": ("PASS", "tested v3s's screen; the law has none", "The law vs Cassini (unscreened)"),
    "One selector for the family": ("OPEN", "chose who gets v3's cold component; the law has none", "none needed"),
    "Stiffness length L*": ("OPEN", "v3s's fitted constant", "none needed"),
    "Law + a^1 growth + no EFE, local": ("FAIL", "a no-go on law + cold component + growth; PAPER67 keeps its question "
                                         "as an open gap", "CMB; Linear growth"),
}


def lane_text(t):
    return "/".join(t["lanes"])


def note_lines(t):
    return textwrap.wrap(f"{t['note']} · {lane_text(t)}", WRAP)


def read_fg1_c4(text=None):
    """FG1's C4 verdict per line and footing, read from the frozen table: {line: (canonical, alt)}."""
    text = open(os.path.join(REPO, FG1_README), encoding="utf-8").read() if text is None else text
    out = {}
    for k, head in enumerate(("| Line | C3 basin split, canonical | C4 the law alone, canonical |", "| Line | C3 alt | C4 alt |")):
        for row in text.split(head, 1)[1].split("\n\n", 1)[0].splitlines()[2:]:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            line = cells[0].split()[0]
            out.setdefault(line, [None, None])[k] = re.match(r"\*\*(PASS|FAIL|NOT GRADED)\*\*", cells[2]).group(1)
    return {k: tuple(v) for k, v in out.items()}


def _src(lane):
    s = SOURCES[lane]
    return (s,) if isinstance(s, str) else s


def _read(lane, cache={}):
    if lane not in cache:
        cache[lane] = "\n".join(open(os.path.join(REPO, f), encoding="utf-8", errors="replace").read() for f in _src(lane))
    return cache[lane]


def check_law(tiles, retired=None, verified=None, fg1=None):
    retired = LAW_RETIRED if retired is None else retired
    verified = VERIFIED_GREEN if verified is None else verified
    fg1 = read_fg1_c4() if fg1 is None else fg1
    errs = []
    names = {t["name"]: t for t in tiles}
    if len(names) != len(tiles):
        errs.append("duplicate tile names")
    for t in tiles:
        n, st = t["name"], t["st"]
        if st not in COL:
            errs.append(f"bad colour {st}: {n}")
        if not t["lanes"]:
            errs.append(f"no source lane: {n}")
        for x in t["lanes"]:
            if x not in SOURCES:
                errs.append(f"lane not in SOURCES: {x} on {n}")
            elif not all(os.path.exists(os.path.join(REPO, f)) for f in _src(x)):
                errs.append(f"lane's file is missing: {x} on {n}")
        if not t["q"]:
            errs.append(f"no number or reason checked against a source: {n}")
        for frag, lane, lit in t["q"]:
            if frag not in t["note"]:
                errs.append(f"quoted fragment not in the note: {frag!r} on {n}")
            if lane not in t["lanes"]:
                errs.append(f"quote from a lane the tile doesn't name: {lane} on {n}")
            elif lane in SOURCES and lit not in _read(lane):
                errs.append(f"literal not in {lane}'s file: {lit!r} on {n}")
        if t["alt"] is not None and (t["alt"] == st or t["alt"] not in COL):
            errs.append(f"split colour where the footings agree: {n}")
        if t["fg1"] is not None:
            canon, alt = fg1.get(t["fg1"], (None, None))
            want = FG1_COLOUR.get(canon)
            want_alt = FG1_COLOUR.get(alt)
            if st != want:
                errs.append(f"colour {st} is not FG1's {canon}: {n}")
            if (t["alt"] or st) != want_alt:
                errs.append(f"alt colour is not FG1's {alt} (footings never pooled): {n}")
        if "PASS" in (st, t["alt"]) and t["fg1"] is None:
            vg = verified.get(n)
            if vg is None or vg[0] not in t["lanes"] or not vg[1] or not vg[2]:
                errs.append(f"green with no FG1 row and no VERIFIED_GREEN entry: {n}")
        if st in ("PASS", "FAIL", "COND", "UNDEC") and V3S_ONLY & set(t["lanes"]):
            errs.append(f"verdict colour resting on a v3/v3s lane: {n}")
        if st == "STALE" and not (t["lab"] and t["note"].strip()):
            errs.append(f"grey tile without its reason: {n}")
        if any(b in f"{n} {t['note']} {t['lab'] or ''}".lower() for b in BANNED):
            errs.append(f"banned wording: {n}")
        if len(note_lines(t)) > MAXL:
            errs.append(f"note too long ({len(note_lines(t))} lines): {n}")
    missing = set(FG1_LINES) - {t["fg1"] for t in tiles}
    if missing:
        errs.append(f"FG1 lines not on the board: {sorted(missing)}")
    v3s = {t["name"]: t["st"] for t in TILES}
    for n, st in v3s.items():
        here = LAW_RENAMES.get(n, n)
        if n in retired:
            if retired[n][0] != st or not retired[n][1].strip() or not retired[n][2].strip():
                errs.append(f"retired tile must keep its colour, reason and counterpart: {n}")
            if here in names:
                errs.append(f"tile both on the board and retired: {n}")
        elif here not in names:
            errs.append(f"tile of the v3s board vanished: {n}")
    came = {LAW_RENAMES.get(n, n) for n in v3s}
    for n in names:
        if n not in came and n not in LAW_EXTRA_TILES:
            errs.append(f"new tile not listed in LAW_EXTRA_TILES: {n}")
    for n in MUST_STAY_RED:
        if n not in names or names[n]["st"] != "FAIL":
            errs.append(f"must stay red: {n}")
    for n in verified:
        if n not in names or names[n]["st"] != "PASS":
            errs.append(f"VERIFIED_GREEN entry not applied: {n}")
    return errs


def tally(tiles, alt=False):
    return {k: sum(1 for t in tiles if ((t["alt"] or t["st"]) if alt else t["st"]) == k) for k in COL}


def _tile(ax, x, y, w, h, t):
    st = t["st"]
    dashed = st == "STALE"
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.05", facecolor=COL[st], linewidth=1.3 if dashed else 0,
                       edgecolor="#7b838b" if dashed else "none", linestyle=(0, (4, 3)) if dashed else "solid",
                       alpha=1.0 if dashed else 0.93)
    ax.add_patch(p)
    if t["alt"]:
        half = Rectangle((x + w / 2, y), w / 2, h, facecolor=COL[t["alt"]], edgecolor="none", alpha=0.93)
        ax.add_patch(half)
        half.set_clip_path(p)


def draw(tiles, out):
    ncol = len(LAW_COLUMNS)
    nmax = max(sum(1 for t in tiles if t["col"] == c) for c in range(ncol))
    row_in = 1.30
    W, H = 20.5, 3.05 + row_in * nmax
    fig = plt.figure(figsize=(W, H), dpi=150)
    fig.patch.set_facecolor("#f6f7f5")
    top_in, bot_in = 1.70, 0.95
    ax = fig.add_axes([0.012, bot_in / H, 0.976, 1 - (top_in + bot_in) / H])
    ax.set_xlim(0, ncol); ax.set_ylim(-0.25, nmax + 0.65); ax.axis("off")
    fig.text(0.015, 1 - 0.50 / H, "The Crispy Fried Chicken Status Board  ·  1 November 2026 — the a₀ law alone",
             fontsize=24, fontweight="bold", color="#16201d")
    _fit(fig, 0.015, 1 - 0.95 / H, LAW_RECIPE, 12.0, color="#16201d", fontstyle="italic")
    fig.text(0.015, 1 - 1.30 / H, "κ = ½ fitted; footings 9.3603e-11 / 1.1312e-10 m/s² never pooled (a tile in two halves: "
             "left canonical, right alt).  Route E's cold sector retired by the owner, 1 November.  Colours restate FG1 "
             "and the lanes named.  The theory is incomplete.", fontsize=10.5, color="#4d5a56")
    dy = 0.127 / row_in                                 # one note line, in row units
    for c, title in enumerate(LAW_COLUMNS):
        ax.text(c + 0.03, nmax + 0.4, title, fontsize=13, fontweight="bold", color="#16201d", va="center")
        for k, t in enumerate([t for t in tiles if t["col"] == c]):
            y = nmax - 0.5 - k
            ink = INK.get(t["st"], "white")
            _tile(ax, c + 0.03, y - 0.46, 0.93, 0.90, t)
            ax.text(c + 0.065, y + 0.34, t["name"], fontsize=10.4, fontweight="bold", color=ink, va="center")
            lab = t["lab"] or (f"canonical {LAW_LAB[t['st']]}  ·  alt {LAW_LAB[t['alt']]}" if t["alt"] else LAW_LAB[t["st"]])
            ax.text(c + 0.065, y + 0.22, lab.upper(), fontsize=8.2, color=ink, va="center", alpha=0.95,
                    fontweight="bold" if t["st"] == "STALE" else "normal")
            for j, ln in enumerate(note_lines(t)):
                ax.text(c + 0.065, y + 0.10 - dy * j, ln, fontsize=7.8, color=ink, va="center", alpha=0.97)
    lx, ly = 0.015, 0.68 / H
    for st in ("PASS", "COND", "UNDEC", "FAIL", "OPEN", "STALE"):
        stale = st == "STALE"
        fig.patches.append(FancyBboxPatch((lx, ly - 0.01 * 13.2 / H), 0.014, 0.02 * 13.2 / H,
                                          boxstyle="round,pad=0,rounding_size=0.003", facecolor=COL[st],
                                          edgecolor="#7b838b" if stale else "none", linewidth=1.0 if stale else 0,
                                          linestyle=(0, (3, 2)) if stale else "solid",
                                          transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.019, ly, LAW_LAB[st], fontsize=10.5, va="center", color="#16201d")
        lx += 0.095
    fig.text(0.015, 0.40 / H, "Grey, dashed = no graded number for the law, with the reason on the tile. NOT GRADED is not a "
             "pass.  Earlier model: img/status_board_2026-10-24v3s.png.  Green is FG1's frozen line or a named lane's frozen class; "
             "FG1 is not blind, and its clean-room regrade is mainly a test of code.", fontsize=9.0, va="center", color="#4d5a56")
    fig.text(0.015, 0.18 / H, "Sources: rebuild_2026_10_22/FG1_final_grade, PAPER67 draft (not deposited).  The retired sector "
             "was called cold dark energy, never a particle.  Nothing here says the data favour this framework.", fontsize=9.0,
             va="center", color="#4d5a56")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)


def _by(seq, name):
    return next(x for x in seq if x["name"] == name)


def broken_cases():
    """Each case breaks one guard; check_law() must report an error for every one. A case gets the tiles, LAW_RETIRED
    and VERIFIED_GREEN copies, and the FG1 table."""
    def c1(t, r, v, f):
        _by(t, "X-COP").update(st="PASS")

    def c2(t, r, v, f):
        _by(t, "DiskMass").update(st="PASS")

    def c3(t, r, v, f):
        _by(t, "Rotation curves (SPARC RAR)").update(alt=None)

    def c4(t, r, v, f):
        _by(t, "Local Group dwarfs (five classes)").update(st="PASS")

    def c5(t, r, v, f):
        f["Tl"] = ("FAIL", "FAIL")

    def c6(t, r, v, f):
        _by(t, "Binary pulsars + GW170817").update(st="PASS")

    def c7(t, r, v, f):
        _by(t, "Tidal dwarfs, NGC 1052-DF2/DF4").update(st="PASS", lab="pass (U1)")

    def c8(t, r, v, f):
        _by(t, "Red (early-type) lenses").update(st="PASS")

    def c9(t, r, v, f):
        v["Local a0 from MeerKAT"] = ("HS1",) + v["Local a0 from MeerKAT"][1:]

    def c10(t, r, v, f):
        _by(t, "Tilt with speed")["lanes"] = []

    def c11(t, r, v, f):
        _by(t, "Tilt with speed")["lanes"].append("NOSUCH")

    def c12(t, r, v, f):
        _by(t, "IC 1613")["q"][0] = ("E −0.593, Z −7.9", "FG1", "E -0.594 (Z -7.9)")

    def c13(t, r, v, f):
        _by(t, "IC 1613")["note"] = "E −0.5, one galaxy"

    def c14(t, r, v, f):
        _by(t, "IC 1613")["q"] = []

    def c15(t, r, v, f):
        t.remove(_by(t, "Causality: criterion A / B"))

    def c16(t, r, v, f):
        r["Solar system + Cassini (screened)"] = ("FAIL",) + r["Solar system + Cassini (screened)"][1:]

    def c17(t, r, v, f):
        del r["Stiffness length L*"]

    def c18(t, r, v, f):
        _by(t, "Cluster cores (318 eRASS1)").update(st="UNDEC")

    def c19(t, r, v, f):
        _by(t, "Health: ghosts, gradients").update(lab=None)

    def c20(t, r, v, f):
        _by(t, "CMB")["note"] += " favour the framework"

    def c21(t, r, v, f):
        _by(t, "Tilt with speed").update(fg1=None, st="PASS")

    def c22(t, r, v, f):
        _by(t, "CMB")["note"] += " x" * 200

    def c23(t, r, v, f):
        _by(t, "MW vertical force").update(lanes=["FG1", "X5", "S3"])

    def c24(t, r, v, f):
        _by(t, "Tilt with speed").update(alt="PASS")

    return [("NOT GRADED X-COP coloured a pass", c1), ("NOT GRADED DiskMass coloured a pass", c2),
            ("SPARC's footings pooled (alt half dropped)", c3), ("FG1's failing dwarfs coloured a pass", c4),
            ("FG1 row changed under a green tile", c5), ("v3s green carried over with no law number", c6),
            ("v3's dust-theorem green restored", c7), ("first green with no FG1 row or verified entry", c8),
            ("VERIFIED_GREEN entry names a lane not on the tile", c9), ("tile with no source lane", c10),
            ("lane not in SOURCES", c11), ("quoted literal not in its source", c12), ("quoted fragment not in the note", c13),
            ("tile with nothing checked against a source", c14), ("v3s tile vanished", c15), ("retired tile repainted", c16),
            ("retired tile dropped silently", c17), ("must-stay-red tile turned blue", c18), ("grey tile with no reason", c19),
            ("banned wording", c20), ("FG1 line off the board", c21), ("note too long", c22),
            ("verdict colour on a v3-only lane", c23), ("split colour where footings agree", c24)]


def selftest():
    fg1 = read_fg1_c4()
    base = check_law(copy.deepcopy(LAW_TILES), copy.deepcopy(LAW_RETIRED), copy.deepcopy(VERIFIED_GREEN), dict(fg1))
    print(f"clean board: {len(base)} errors")
    bad = 1 if base else 0
    for label, fn in broken_cases():
        t, r, v, f = copy.deepcopy(LAW_TILES), copy.deepcopy(LAW_RETIRED), copy.deepcopy(VERIFIED_GREEN), dict(fg1)
        fn(t, r, v, f)
        e = check_law(t, r, v, f)
        print(f"  {'CAUGHT' if e else 'MISSED'}: {label}" + (f"  ->  {e[0]}" if e else ""))
        bad += 0 if e else 1
    print("SELFTEST PASS: every broken case caught; nothing written." if not bad else "SELFTEST FAIL")
    sys.exit(0 if not bad else 1)


def md_table():
    print("| tile | canonical | alt | source lanes | v3s colour |\n|---|---|---|---|---|")
    v3s = {LAW_RENAMES.get(t["name"], t["name"]): t["st"] for t in TILES}
    for c in range(len(LAW_COLUMNS)):
        for t in [t for t in LAW_TILES if t["col"] == c]:
            alt = "" if t["alt"] is None else LAW_LAB[t["alt"]]
            print(f"| {t['name']} | {LAW_LAB[t['st']]} | {alt or 'same'} | {', '.join(t['lanes'])} | "
                  f"{LAB[v3s[t['name']]] if t['name'] in v3s else 'new'} |")


def main():
    if "--selftest" in sys.argv[1:]:
        selftest()
    if "--md" in sys.argv[1:]:
        md_table()
        return
    mutate = "--mutate" in sys.argv[1:]
    tiles = copy.deepcopy(LAW_TILES)
    if mutate:
        _by(tiles, "The law vs Cassini (unscreened)")["lanes"] = []
    errs = check_law(tiles)
    print(f"{len(tiles)} tiles on the law's board. Canonical: " + ", ".join(f"{LAW_LAB[k]} {v}" for k, v in tally(tiles).items()))
    print("Alt: " + ", ".join(f"{LAW_LAB[k]} {v}" for k, v in tally(tiles, alt=True).items()))
    if errs:
        for e in errs:
            print("CHECK FAIL:", e)
        print("MUTATE: checks failed as required; nothing written." if mutate else "nothing written.")
        sys.exit(1)
    if mutate:
        print("MUTATE: checks did NOT catch the stripped lane")
        sys.exit(2)
    draw(tiles, OUT)
    print("all checks PASS; wrote", os.path.relpath(OUT, REPO))


if __name__ == "__main__":
    main()
