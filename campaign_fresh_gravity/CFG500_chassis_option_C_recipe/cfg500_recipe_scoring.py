#!/usr/bin/env python3
"""CFG500: chassis option C as a full track. Candidate B as an explicit recipe.

Scores the recipe (RECIPE.md) against every status-board tile, recounts its constants against CFG469's 15, lists what
is lost by dropping the relativistic chassis, and checks pairs of recipe items for conflicts. Frozen rules:
FROZEN_CRITERIA.md (committed alone first, 21b1db999).

Every file is read at HEAD with `git show HEAD:path`, so only committed results can enter. No physics is computed.
kappa = 1/2 is FITTED. The cold energy's mass is required; no dark-matter particle. A recipe has no action: its
relativistic sector is untested, not passed. Not "theory closed".

    python3 campaign_fresh_gravity/CFG500_chassis_option_C_recipe/cfg500_recipe_scoring.py
    CFG500_MUTATE=1 python3 campaign_fresh_gravity/CFG500_chassis_option_C_recipe/cfg500_recipe_scoring.py
"""
import ast
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG500_MUTATE", "") == "1"
TAG = "_MUTATE" if MUTATE else ""
CFG = "campaign_fresh_gravity/"

_cache = {}


def head(path):
    """File content at HEAD (committed only)."""
    if path not in _cache:
        r = subprocess.run(["git", "show", "HEAD:" + path], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            raise FileNotFoundError("not committed at HEAD: " + path)
        _cache[path] = r.stdout
    return _cache[path]


def hjson(path):
    return json.loads(head(path))


CHECKS = []
QUOTES = []  # (path, quote, found)


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


def ev(path, quote):
    """An evidence item. Its quote is verified verbatim at HEAD by control K2."""
    p = path if path.startswith(CFG) or path.startswith("explainers/") else CFG + path
    return (p, quote)


# ===================================================================================================== sources
SP = "closure_map/status_picture_2026_10_03.py"
STD = "STANDING_2026-09-29.md"
GATES = "closure_map/GATES.md"
RGA = "closure_map/RECIPE_GATE_AUDIT_2026-10-03.md"
C469 = "CFG469_chassis_options/README.md"
WM = "WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md"
LED = "LEDGER_failure_mechanisms_2026-10-08/README.md"
H7 = "CFG7_harness_fg097.out"

# ===================================================================================================== 1. the recipe
# status classes: FITTED, DATA, DECLARED FUNCTION, DECLARED CONSTANT, DECLARED RULE, DECLARED DISCRETE CHOICE,
# NUISANCE, DERIVED (given listed inputs; not counted), HYPOTHESIS (the law's form; not counted, as in CFG469),
# OPTIONAL RULE (counted only if used), INHERITED SETTING (counted only if no lane shows insensitivity).
RECIPE = [
    dict(id="LAW", name="the law: a0(t) = kappa c sqrt(G rho_DE(t)); g = nu(g_N/a0) g_N in bound, owned systems",
         status="HYPOTHESIS", c469=None,
         tested_by="SPARC (GATES 1.01), CFG301/309 MeerKAT, CFG6 a0(z), PAPER38 (calibration wall), DR4 prereg",
         ev=[ev(GATES, "| 3.11 | a0 = kappa c sqrt(G rho_Lambda) |"), ev(WM, "It is flat only if w = −1.")]),
    dict(id="F1", name="kappa = 1/2", status="FITTED", c469="kappa = 1/2",
         tested_by="CFG493 (0.417 +- 0.095 canonical / 0.345 +- 0.078 alt: consistent, not discriminating)",
         ev=[ev(C469, "| kappa = 1/2 | FITTED |"), ev("CFG493_kappa_combined/README.md", "κ = 0.417 ± 0.095")]),
    dict(id="F2", name="the cold energy's amount, Omega_c h^2 = 0.12 (S = Omega_c/Omega_b = 5.364)", status="FITTED",
         c469="Omega_c h^2 = 0.12",
         tested_by="CMB by construction (GATES 3.01); CFG288 / CFG360 / CFG496 (no derivation, no clue)",
         ev=[ev(C469, "| Omega_c h^2 = 0.12 | FITTED (as in LCDM) |"), ev(STD, "No cold–dark energy clue (CFG496)")]),
    dict(id="D1", name="rho_DE(t) entering a0(t) (flat a0 only if w = -1)", status="DATA", c469="rho_DE(t)",
         tested_by="CFG439 (DE-tracking a0 growth 512^3); CFG6 branches; PAPER38",
         ev=[ev(C469, "| rho_DE(t) in a0(t) = kappa c sqrt(G rho_DE(t)) | DATA |")]),
    dict(id="D2", name="f_b = Omega_b/Omega_m", status="DATA", c469="f_b",
         tested_by="enters the edge (CFG423/424) and the supply (CFG494/497)",
         ev=[ev(C469, "| f_b | DATA |")]),
    dict(id="K1", name="kernel nu_mono (nu_RAR to y* = 2.3374, monotone log splice)", status="DECLARED FUNCTION",
         c469="nu_mono",
         tested_by="GATES 1.01/1.05 (SPARC, P2 ~2 sigma), CFG468 (frozen, no committed result), CFG493 (kernel moves kappa)",
         ev=[ev("CFG5_common.py", "nu_RAR up to y* = 2.3374, then the monotone log splice with delta = 0.05"),
             ev("CFG493_kappa_combined/README.md", "Switching ν_mono to the quadrature form moves every route by +0.06 to +0.09 dex (κ_Λ 0.417 → 0.489)")]),
    dict(id="K1a", name="the splice shape constant delta = 0.05 (y* follows from delta by tangency)",
         status="DECLARED CONSTANT", c469="(inside the nu_mono row)",
         tested_by="none separately (XC4 choice)",
         ev=[ev("CFG5_common.py", "yp = _bq(dh, 1.0, 5.0); hp = _h_rar(yp); delta = 0.05")]),
    dict(id="S1", name="bound-only switch: the law acts only in bound regions; exactly off on FRW", status="DECLARED RULE",
         c469="bound-only switch",
         tested_by="CFG4_switch (CMB lensing 1.000, forest 0.00); CFG487 (switch exactly off on FRW; Gap 1 open)",
         ev=[ev(C469, "| bound-only switch | DECLARED RULE |"),
             ev("CFG487_settled_fraction_switch/README.md", "The switch is exactly OFF on FRW and in linear parcels, and it never flickers.")]),
    dict(id="S2", name="ownership: each system carries its own phantom; the Sun carries none; globulars class E; no EFE",
         status="DECLARED RULE", c469="ownership",
         tested_by="GATES 4.01 (Cassini Q2), CFG332/333/465 (globulars), CFG491 (SPARC EFE slope +1.8 sigma lean), DR4 Arm C",
         ev=[ev(C469, "| ownership (the Sun carries no phantom; globulars class E) | DECLARED RULE |"),
             ev(GATES, "PASS via ownership: host-phantom tide 1.6-2.6e-31 s^-2")]),
    dict(id="E1", name="KiDS density edge x_e = 0.4 (phantom support for isolated-lens lensing)", status="DECLARED CONSTANT",
         c469="KiDS density edge x_e = 0.4",
         tested_by="GATES 3.05 (KiDS PASS at declared x_e = 0.4), CFG413 (x = 0.3-0.5 window), GATES 3.09 (not derived)",
         ev=[ev(C469, "| KiDS density edge x_e = 0.4 | DECLARED CONSTANT |"), ev(H7, "declared edge x_e = 0.4, max rule (T5)")]),
    dict(id="E2", name="supply postulate: each galaxy settles S x M_b (its original baryons' cosmic share) inside its edge",
         status="DECLARED RULE", c469="(inside the growth-edge row)",
         tested_by="six failed derivations: CFG461, CFG462, CFG488, CFG490, CFG494, CFG497 (STANDING 10-08)",
         ev=[ev(STD, "NOT DERIVABLE on six attacks"),
             ev("CFG497_binding_energy_selection/README.md", "NOT DERIVED (0 of 10 candidates)")]),
    dict(id="E3", name="growth edge r_edge = r_M/ln(1/(1-f_b)) = 5.85 r_M", status="DERIVED", c469="(inside the growth-edge row)",
         tested_by="CFG423/424 (given E2, the law and f_b, it has no further choice)",
         ev=[ev("CFG424_turnaround_catchment/README.md", "The phantom excess lives inside the mass-conserving edge r_M/ln(1/(1−f_b))")]),
    dict(id="E4", name="per-catchment mass conservation: the excess is drawn from the same halo's turnaround catchment "
                       "(LCDM spherical-collapse Delta_ta(z)), in proportion to its cold density",
         status="DECLARED RULE", c469="(inside the growth-edge row)",
         tested_by="CFG424 (MUTATE no compensation: TENSION), CFG425, CFG426, CFG427, CFG439, CFG460",
         ev=[ev("CFG424_turnaround_catchment/README.md", "so the added source sums to zero on every catchment")]),
    dict(id="E5", name="max rule T5: dark mass = max(phantom, cosmic share) (clusters)", status="DECLARED RULE",
         c469=None,
         tested_by="GATES 2.01 X-COP identity 0.946 +- 0.080; CFG379 (supply limit does not set the cluster level)",
         ev=[ev(GATES, "dark mass = max(phantom, cosmic share)"), ev(H7, "LEDGER: fitted 2 (kappa, Omega_c h^2); declared 5; tied 1; derived 1")]),
    dict(id="R1", name="the cold energy relaxes toward the phantom target at rate Gamma (bookkeeping; no force derived)",
         status="DECLARED RULE", c469="cold fluid relaxes toward the phantom target at rate Gamma",
         tested_by="CFG464 (lambda = 1 t_dyn rate NOT EXCLUDED), CFG431 (one clock not universal), CFG461 (no class sets sigma^4)",
         ev=[ev(C469, "| cold fluid relaxes toward the phantom target at rate Gamma (bookkeeping) | DECLARED RULE |"),
             ev("CFG464_tdyn_rate_corrected_ledger/README.md", "NOT EXCLUDED (robust)")]),
    dict(id="R1c", name="OPTIONAL: settling clock m with Dm/Dt = Gamma L (1 - m), Gamma = sqrt(4 pi G rho_X) (lambda = 1); "
                        "V1 reads the cold energy (MS1 exception), V2 reads baryons",
         status="OPTIONAL RULE", c469=None,
         tested_by="CFG487 (both versions FAIL with the 5.85 r_M edge; V1 alone passes KiDS + SPARC, overdraws growth), CFG498 PENDING",
         ev=[ev("CFG487_settled_fraction_switch/README.md", "**Both versions FAIL, on SPARC (alt footing only) and on KiDS.**")]),
    dict(id="L1", name="lensing = GR lensing of the effective dark density", status="DECLARED RULE",
         c469="lensing = GR lensing of the effective dark density",
         tested_by="KiDS (GATES 3.05), SLACS (GATES 1.19), CFG495 (drawdown, KiDS cannot test)",
         ev=[ev(C469, "| lensing = GR lensing of the effective dark density | DECLARED RULE |")]),
    dict(id="B1", name="background cosmology GR + CDM at z >~ 10 (BBN, CMB standard by declaration)", status="DECLARED RULE",
         c469="background cosmology GR + CDM",
         tested_by="GATES 3.01 (met by construction), 3.04 (BAO unchanged by construction), 3.13 (BBN standard by T4)",
         ev=[ev(C469, "| background cosmology GR + CDM at z >~ 10 | DECLARED RULE |"), ev(GATES, "BBN standard by T4 per CHARTER")]),
    dict(id="G1", name="the baryon field includes gas pressure", status="DECLARED RULE", c469="baryon field includes gas pressure",
         tested_by="CFG372 (withdrawn pass), CFG427 (MIX-A vs MIX-B insensitive)",
         ev=[ev(C469, "| baryon field includes gas pressure | DECLARED MODELLING RULE |")]),
    dict(id="FT", name="footing: rho in the law is rho_Lambda (canonical) or rho_crit (alt); two parallel recipes, never pooled",
         status="DECLARED DISCRETE CHOICE", c469=None,
         tested_by="every lane reports both; CFG493 (kappa 0.42 / 0.35)",
         ev=[ev(GATES, "**Footings:** canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2 (CHARTER)")]),
    dict(id="N1", name="stellar M/L", status="NUISANCE", c469="stellar M/L",
         tested_by="per data set (GATES 1.01: one global Upsilon_disk 0.5-0.8)",
         ev=[ev(C469, "| stellar M/L | NUISANCE (per data set) |")]),
    dict(id="X1", name="G = measured G (CFG469: no alpha_c/2 correction)", status="RETIRED UNDER C", c469="G = measured G",
         tested_by="vacuous without the chassis: there is no alpha_c, so Newton's measured G enters as in every theory",
         ev=[ev(C469, "| G = measured G (no alpha_c/2 correction) | DECLARED |")]),
    dict(id="I1", name="growth-engine inherited setting: T1 switch epsilon = 0.077 in the peak finder", status="INHERITED SETTING",
         c469=None, tested_by="CFG427: epsilon x0.5 / x2 give 0.0273 / 0.0273 (insensitive)",
         ev=[ev("CFG427_zero_knob_inherited_settings/README.md", "So neither inherited setting carries the pass.")]),
    dict(id="I2", name="growth-engine inherited setting: MIX-A gas filter", status="INHERITED SETTING", c469=None,
         tested_by="CFG427: MIX-B 0.0262, HOT1 0.0311 (insensitive)",
         ev=[ev("CFG424_turnaround_catchment/README.md", "the T1 switch ε and the MIX-A filter (inherited, not tuned here)")]),
]
if MUTATE:
    RECIPE = [r for r in RECIPE if r["id"] != "E4"]
RID = {r["id"]: r for r in RECIPE}

COUNTED = ["FITTED", "DATA", "DECLARED FUNCTION", "DECLARED CONSTANT", "DECLARED RULE", "DECLARED DISCRETE CHOICE", "NUISANCE"]

# CFG469's 15, exactly as its table lists them (K4)
C469_ROWS = [("kappa = 1/2", "FITTED"), ("rho_DE(t)", "DATA"), ("nu_mono", "DECLARED FUNCTION"),
             ("bound-only switch", "RULE/CONST"), ("KiDS density edge x_e = 0.4", "RULE/CONST"),
             ("growth edge 5.85 r_M with the turnaround catchment", "RULE/CONST"), ("f_b", "DATA"),
             ("Omega_c h^2 = 0.12", "FITTED"), ("relaxation at rate Gamma", "RULE/CONST"), ("ownership", "RULE/CONST"),
             ("lensing = GR lensing", "RULE/CONST"), ("background GR + CDM", "RULE/CONST"),
             ("gas pressure", "RULE/CONST"), ("stellar M/L", "NUISANCE"), ("G = measured G", "RULE/CONST")]

RECONCILE = [
    ("+1", "delta = 0.05 split out of the nu_mono row (CFG469 wrote 'DECLARED FUNCTION (+ shape constant delta)')"),
    ("+1", "the growth-edge row is split: supply postulate (DECLARED RULE) + per-catchment conservation (DECLARED RULE); "
           "the 5.85 r_M edge itself is DERIVED given them, kappa and f_b"),
    ("+1", "max rule T5 added: in CFG7's B ledger ('declared 5'), carries the X-COP pass, omitted from CFG469's table"),
    ("+1", "footing choice added: the law has two readings of rho, run as two recipes (DECLARED DISCRETE CHOICE)"),
    ("-1", "G = measured G retired: without the chassis there is no alpha_c/2 renormalisation to declare away"),
]

# ===================================================================================================== 2. the board
CHASSIS_ONLY = "chassis-only"
# For each tile: status under C, the recipe items it depends on, the chassis flag, a note, evidence.
T = {}


def tile(name, under_c, deps, note, evid, chassis=False, parts=None):
    T[name] = dict(under_c=under_c, deps=deps, note=note, ev=evid, chassis=chassis, parts=parts)


# Column 1: the relativistic chassis (CFG469's 12 untested tiles; zero-field and growth-alone are MOOT)
tile("Gravity waves at light speed", "UNTESTED", [], "c_T = 1 is a property of the khronon action (CFG292); a recipe has no tensor sector",
     [ev(SP, "c_T = 1 exact · CFG292"), ev(C469, "gravity waves at light speed;")], chassis=True)
tile("Equations well-posed (high freq.)", "UNTESTED", [], "no field equations to pose",
     [ev(C469, "high-frequency well-posedness;")], chassis=True)
tile("Full nonlinear well-posedness", "UNTESTED", [], "no field equations to pose",
     [ev(C469, "full nonlinear well-posedness;")], chassis=True)
tile("Lapse condition, realistic matter", "UNTESTED", [], "no lapse",
     [ev(C469, "the lapse condition;")], chassis=True)
tile("Binary pulsars", "UNTESTED", [], "dipole radiation / alpha-hat need the khronon; margin 490,000x is a chassis result",
     [ev(SP, "margin 490,000x · CFG291/311"), ev(C469, "binary pulsars;")], chassis=True)
tile("Strong coupling", "UNTESTED", [], "no field theory, no cutoff", [ev(C469, "strong coupling;")], chassis=True)
tile("Solar system (PPN + Cassini Q2)", "PARTIAL", ["S2"],
     "Cassini Q2 PASS via ownership (GATES 4.01, margin 2.0e4-3.3e4); gamma, alpha1, alpha2 UNTESTED; bare nu_mono is NOT "
     "Solar-System safe (CFG185), so the pass rests on the ownership rule alone",
     [ev(GATES, "PASS via ownership: host-phantom tide 1.6-2.6e-31 s^-2"),
      ev(C469, "B keeps GATES 4.01 through ownership, but alpha1, alpha2 and gamma become untested;")],
     chassis=True, parts={"Cassini Q2 (ownership)": "PASS", "PPN gamma, alpha1, alpha2": "UNTESTED"})
tile("Matter conservation (G9)", "UNTESTED", [], "no Bianchi identity without an action; the relaxation rule R1 has no force",
     [ev(C469, "matter conservation G9;")], chassis=True)
tile("Structural order (G0)", "UNTESTED", [], "no action to order", [ev(C469, "structural order G0;")], chassis=True)
tile("Zero-field nonlinear, ungated", "MOOT", [], "a FAIL of the ungated chassis; the recipe retires that object (moot, not passed)",
     [ev(C469, "the zero-field FAIL, which becomes moot, not passed;"), ev(LED, "for B it is **untested**")], chassis=True)
tile("Black holes (EHT, LIGO ringdown)", "UNTESTED", [], "no strong-field sector; CFG467 alpha_c tension and CFG319 UH defect vanish with it",
     [ev(C469, "black holes;")], chassis=True)
# Column 2: galaxies and clusters (no chassis-only ingredient: CFG469 dependency audit)
tile("Rotation curves (SPARC RAR)", "PASS", ["LAW", "F1", "K1", "K1a", "N1", "G1"],
     "0.1003 dex with nu_mono; holds only while the 5.85 r_M edge is NOT applied to SPARC galaxies "
     "(CFG487: alt dwarfs A3 0.864 < 0.90 with it): see conflict C1",
     [ev(GATES, "PASS. nu_mono 0.1003 (U .61) / 0.0991 (.57)"),
      ev("CFG487_settled_fraction_switch/README.md", "**FAIL**: alt dwarfs A3 0.864 < 0.90 (canonical 0.945)")])
tile("Local a0 from MeerKAT", "PASS", ["LAW", "F1", "K1"], "a0 0.9-1.4e-10 matches SPARC; kernel-dependent like kappa (CFG493)",
     [ev(SP, "0.9-1.4e-10, matches SPARC · CFG301/309")])
tile("Weak lensing (KiDS)", "PASS", ["S1", "E1", "L1", "LAW"],
     "passes with the declared x_e = 0.4; FAILS with the growth edge 5.85 r_M (CFG487 +60.5 / +70.6): see conflict C1",
     [ev(GATES, "PASS at declared x_e = 0.4, A <= 2: P2 -10.7 / -10.9, nu_mono -12.4 / -11.3")])
tile("Clusters, Bullet Cluster", "PASS", ["E5", "F2", "L1"],
     "X-COP identity 0.946 +- 0.080 through the max rule; Bullet needs the cold mass. The supply limit does not set the "
     "cluster level (CFG379 FAILS; CFG497 bonus: FAIL by 0.007 / 0.008): a tension of the supply rule, not of this tile",
     [ev(GATES, "PASS 0.946 ± 0.080 both footings"), ev(GATES, "| 2.02 | Bullet Cluster (Clowe+06) |")])
tile("Andromeda + Local Volume dwarfs", "PASS", ["LAW", "S2"], "law alone, native inputs (CFG313)",
     [ev(SP, "law alone, native inputs · CFG313")])
tile("Globulars + ownership rule", "COND", ["S2"],
     "CFG465: tile FRAGILE (Pal 3 unsourced); on sourced inputs Newton fits; law-applied exclusion ROBUST",
     [ev("CFG465_globular_inputs_audit/README.md", "**Tile: FRAGILE.**"),
      ev(STD, "The law-applied exclusion is ROBUST, as B's ownership rule expects.")])
tile("Milky Way ultra-faint dwarfs", "COND", ["LAW", "S2", "F2"],
     "CFG344 RESOLVES narrowly and conditionally (post-reionisation cold accretion, LCDM-calibrated assembly)",
     [ev("CFG344_postreion_cold_accretion/README.md", "RESOLVES, but narrowly and conditionally.")])
tile("Massive ellipticals (SLUGGS)", "UNDEC", ["LAW", "S2"],
     "sample not significant; the four centrals are a ROBUST FAIL with stars only (CFG466), a known board sub-fail",
     [ev(SP, "not significant; 4 centrals fail · CFG323/330/331"), ev(STD, "SLUGGS centrals (CFG466): ROBUST FAIL with stars only.")])
# Column 3: cosmology and a0 over time
tile("Constant a0 vs a0 ~ H(z)", "UNDEC", ["LAW", "D1"], "calibration wall (PAPER38); a0 tracks rho_DE, flat only if w = -1",
     [ev(SP, "calibration wall · PAPER38")])
tile("High-z on halo-free inputs", "UNDEC", ["LAW"], "RC100 on the flat line (CFG303)", [ev(SP, "RC100 on the flat line · CFG303")])
tile("CRISTAL z~5 / ALESS 122.1", "UNDEC", ["LAW"], "stress tests not robust (CFG307/308)", [ev(SP, "stress tests: not robust · CFG307/308")])
tile("Gaia DR4 wide binaries", "OPEN", ["S2"], "pre-registered Arm C (ownership, no EFE): gamma-hat = 1.000; decides 2 Dec 2026",
     [ev(GATES, "Arm C (B's rule): 1.000, dead at >= 1.084")])
tile("Structure growth, candidate B", "COND", ["S1", "E2", "E3", "E4", "F1", "D2", "F2", "R1"],
     "zero-knob edge + per-catchment conservation, 16/16 runs incl. 512^3 x2 seeds, both footings, DE-tracking; "
     "condition: bookkeeping cold energy, supply postulate an input, convergence beyond 512^3 untested; the edge clashes with lensing (C1)",
     [ev(STD, "the zero-knob rule passes 16/16 runs"), ev(SP, "zero-knob edge, 512^3 · PAPER45 v2")])
tile("Structure growth, chassis alone", "MOOT", [], "a FAIL of the ungated chassis (law on everywhere); retired with it, not passed",
     [ev(SP, "~7x too fast; CMB lensing excludes · L341"), ev(LED, "**chassis only** (all matter feels ν_mono)")], chassis=True)
# Column 4: the deep why
tile("Why kappa = 1/2 (the 32 pi)", "OPEN", ["F1"],
     "stays OPEN, with one lead fewer: the khronon-class tie kappa = 2 sqrt(8 pi)/(3 beta) is lost",
     [ev(WM, "κ = ½ ⟺ β = 6.684, where β is not derived")])
tile("What sets the cold-mass amount", "OPEN", ["F2"], "an input (FITTED); CFG496: 0/15 cold-dark energy clues",
     [ev(SP, "free in every build · CFG288")])
tile("Ownership from an action", "DECLARED", ["S2"], "under C there is no action to derive it from: the question is retired and "
     "ownership is a DECLARED RULE (not passed, not open)", [ev(SP, "scoped no-gos · CFG242-245")])
tile("Radiative stability (G12)", "UNTESTED", [], "no quantum field theory to run loops on", [ev(C469, "radiative stability G12.")], chassis=True)

# GATES §4/§5 rows that are relativistic predictions and become unavailable (in addition to the tiles)
UNAVAILABLE = [
    ("GW speed c_T = c and GW dispersion / polarisations", "GATES 4.02, 5.07; tile 'Gravity waves at light speed'",
     ev(GATES, "| 4.02 | GW170817 speed |")),
    ("PPN gamma, beta, alpha1, alpha2, alpha3, zeta_i, xi", "GATES 4.04; only Cassini Q2 survives, via ownership",
     ev(GATES, "| 4.04 | full PPN beta, alpha1-3 |")),
    ("binary pulsars (dipole radiation, alpha-hat), neutron-star sensitivities", "CFG291/311; tile 'Binary pulsars'",
     ev(SP, "margin 490,000x · CFG291/311")),
    ("BBN and the CMB", "GATES 3.01 / 3.13: standard BY DECLARATION (rule B1), not predicted",
     ev(GATES, "BBN standard by T4 per CHARTER")),
    ("black holes: EHT shadows, ringdown, moving holes, the universal horizon", "CFG318/319, CFG467, CFG469 option A",
     ev(LED, "No fully regular moving black hole exists for any α_c > 0")),
    ("strong field / compact objects, collapse", "CFG318; RECIPE_GATE_AUDIT G11", ev(RGA, "| **G11** | Compact objects, BHs, caustics |")),
    ("lensing = dynamics (Phi = Psi) as a derivation", "GATES 4.03 (declared instead: rule L1)",
     ev(C469, "lensing = dynamics as a derivation, measured G derived, the DOF / ghost count, and the Cauchy problem")),
    ("preferred-frame effects (a0 vs CMB-frame speed)", "GATES 4.08 (KM1): neither tested nor threatened",
     ev(GATES, "a0 would track CMB-frame speed")),
    ("well-posedness, Cauchy problem, DOF / ghost count, strong coupling, radiative stability", "GATES 5.02-5.05; G12",
     ev(GATES, "| 5.04 | Cauchy problem / causality by criterion B (req 7) |")),
]

# results LOST by dropping the chassis (none of them is a pass of B)
LOST = [
    ("CFG373 khronon lapse carrier", "LEAD (mechanism)",
     "G1 PASS symbolic with zero constants: the phantom target is a local functional of the lapse field; overall CONDITIONAL",
     [ev("CFG373_lapse_channel/README.md", "PASS (symbolic, zero constants)"), ev("CFG373_lapse_channel/README.md", "**Verdict: CONDITIONAL.**")]),
    ("CFG381 khronon reaction sink", "LEAD (mechanism, +1 constant)",
     "the khronon does not produce K ~ Gamma/c; a direct fluid-khronon coupling lambda_x would (+1 constant)",
     [ev("CFG381_khronon_K_response/README.md", "**Verdict: DOES NOT PRODUCE.**"), ev("CFG381_khronon_K_response/README.md", "CONDITIONAL, +1 constant")]),
    ("CFG462 lapse settling edge", "FAIL (no loss of a pass)",
     "the lapse has no f_b and cannot stop settling at 5.85 r_M",
     [ev("CFG462_lapse_settling_edge/README.md", "EXHAUSTION ONLY (FAIL); the energy sink is NOT SUPPLIED")]),
    ("CFG483 khronon-boundary settling class (C7)", "LEAD (derivation given the cosmic budget)",
     "sigma^4 = G M_b a0/4 exact given M_c = nu M_b, edge 4.02 r_M (not 5.85); falsifier UNDECIDED at 256^3; not on STANDING, unaudited",
     [ev("CFG483_khronon_boundary_settling/cfg483.out", "sigma^4 = G M_b a0/4 exact by construction"),
      ev("CFG483_khronon_boundary_settling/cfg483.out", "FALSIFIER UNDECIDED at 256^3")]),
    ("khronon-class a0 <-> rho_Lambda tie", "TIE (not a derivation)",
     "kappa = 2 sqrt(8 pi)/(3 beta); kappa = 1/2 iff beta = 6.684, beta not derived",
     [ev(WM, "κ = ½ ⟺ β = 6.684, where β is not derived")]),
    ("the chassis's own passes and conditions", "BOARD TILES -> UNTESTED",
     "c_T = 1, lapse W <= 0, pulsars 490,000x, PPN filter, G9 Bianchi, G0, G8, G11, G12 (CFG292/294/312/291/311/357/329/318/319/320)",
     [ev(C469, "Twelve status-board tiles:")]),
    ("CFG469 option A / CFG467 alpha_c window", "MOOT",
     "the alpha_c sliver and the lenient-BH reading concern the chassis only",
     [ev("CFG467_alpha_c_sign_tension/README.md", "## Verdict: TENSION (frozen rule)")]),
]

# MOOT ranks with FAIL (moot is not passed): a retired FAIL is never read as raised (README disclosure 2)
ORDER = {"FAIL": 0, "MOOT": 0, "TENSION": 1, "UNSUPPORTED": 1, "UNDEC": 2, "OPEN": 2, "UNTESTED": 2, "DECLARED": 2,
         "PARTIAL": 3, "COND": 3, "PASS": 4}


def main():
    print("=" * 118)
    print(f"CFG500: chassis option C, candidate B as a recipe. MODE = {'MUTATE (per-catchment mass conservation REMOVED)' if MUTATE else 'main'}")
    print("kappa = 1/2 FITTED. Cold energy's mass required; no dark-matter particle. Untested is not passed. Not 'theory closed'.")
    print("Every number below is read at HEAD (git show). CFG498 has no committed result: PENDING.")
    print("=" * 118)

    # ------------------------------------------------------------------ board tiles from the status picture (K1)
    tree = ast.parse(head(CFG + SP))
    groups = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "groups" for t in node.targets):
            groups = ast.literal_eval(node.value)
    board = [(g, name, st, lab) for g, tiles in groups for (name, st, lab) in tiles]

    # ------------------------------------------------------------------ numbers from committed JSON (K5)
    print("\n[committed numbers]")
    j424 = hjson(CFG + "CFG424_turnaround_catchment/cfg424_results.json")
    j425 = hjson(CFG + "CFG425_turnaround_catchment_confirm/cfg425_results.json")
    j439 = hjson(CFG + "CFG439_zero_knob_alt_512/cfg439_results.json")
    j460 = hjson(CFG + "CFG460_zero_knob_512_second_seed/cfg460_results.json")
    j487d = hjson(CFG + "CFG487_settled_fraction_switch/cfg487_data_results.json")
    j487g = hjson(CFG + "CFG487_settled_fraction_switch/cfg487_growth_results.json")
    j414 = hjson(CFG + "CFG414_confined_switch_512/cfg414_results.json")
    j413 = hjson(CFG + "CFG413_on_radius_kids_vs_growth/cfg413_kids_results.json")
    N = {}
    N["424_mut_pdev"] = j424["MUTATE (no compensation)"]["pdev"]
    N["424_mut_s8"] = j424["MUTATE (no compensation)"]["s8"]
    N["424_mut_verdict"] = j424["MUTATE (no compensation)"]["verdict"]
    N["425_R3"] = j425["R3 512^3 seed 359"]["pdev"]
    N["439_alt"] = j439["A FLAT alt"]["pdev"]
    N["439_de"] = j439["B DE canonical"]["pdev"]
    N["460"] = j460["pdev"]
    zk_runs = [j424["TA-can"], j424["TA-alt"], j425["R1 256^3 seed 360"], j425["R2 256^3 seed 361"], j425["R3 512^3 seed 359"],
               j439["A FLAT alt"], j439["B DE canonical"]]
    N["zk_all_ok"] = all(r["verdict"] == "GROWTH OK" for r in zk_runs) and j460["cut"] == "GROWTH OK"
    N["zk_max_pdev"] = max([r["pdev"] for r in zk_runs] + [j460["pdev"]])
    for f in ("canonical", "alt"):
        rows = j487d["kids"][f]["rows"]
        N[f"487_E1_{f}"] = rows["V1_E1"]["d_vs_best"]
        N[f"487_noedge_{f}"] = rows["V1_noedge"]["d_vs_best"]
        N[f"487_V2noedge_{f}"] = rows["V2_noedge"]["d_vs_best"]
        N[f"487_E2_{f}"] = rows["V1_E2"]["d_vs_best"]
    N["487_sparc_V1"] = j487d["sparc_pass_V1"]
    N["487_sparc_V2"] = j487d["sparc_pass_V2"]
    gr = j487g["runs"]
    N["487_catch_can"] = gr["POST-HOC V1-CATCH canonical"]["pdev"]
    N["487_catch_alt"] = gr["POST-HOC V1-CATCH alt"]["pdev"]
    N["487_catch_verdicts"] = [gr["POST-HOC V1-CATCH canonical"]["verdict"], gr["POST-HOC V1-CATCH alt"]["verdict"]]
    N["487_edge_growth_ok"] = all(gr[k]["verdict"] == "GROWTH OK" for k in ("V1 canonical", "V1 alt", "V2 canonical", "V2 alt"))
    N["414_can"] = j414["canonical"]["pdev"]
    N["414_alt"] = j414["alt"]["pdev"]
    N["414_ok"] = j414["canonical"]["verdict"] == "GROWTH OK" and j414["alt"]["verdict"] == "GROWTH OK"
    for f in ("canonical", "alt"):
        d = j413["primary"][f]
        best = min(v["free"]["chi2"] for v in d.values())
        N[f"413_x04_{f}"] = d["0.4"]["free"]["chi2"] - best
    for k, v in N.items():
        print(f"  {k:24s} = {v if not isinstance(v, float) else round(v, 4)}")

    # ------------------------------------------------------------------ section 1: the recipe and its count
    print("\n" + "=" * 118 + "\n1. THE RECIPE: items, status, tests\n" + "=" * 118)
    for r in RECIPE:
        print(f"  {r['id']:4s} [{r['status']}] {r['name']}")
        print(f"        tested by: {r['tested_by']}")
    counts = {c: [r["id"] for r in RECIPE if r["status"] == c] for c in COUNTED}
    total = sum(len(v) for v in counts.values())
    opt = [r["id"] for r in RECIPE if r["status"] == "OPTIONAL RULE"]
    inh = [r["id"] for r in RECIPE if r["status"] == "INHERITED SETTING"]
    print("\n  COUNT (rule: FROZEN_CRITERIA §2):")
    for c in COUNTED:
        print(f"    {c:26s} {len(counts[c]):2d}  {counts[c]}")
    print(f"    {'TOTAL':26s} {total:2d}   (+{len(opt)} optional settling clock if used; {len(inh)} inherited engine settings "
          f"not counted: CFG427 shows the pass insensitive to both)")
    print("  Not counted: the law's form (HYPOTHESIS); the 5.85 r_M edge (DERIVED given E2, kappa, f_b); G, c (measured).")
    c469 = {"FITTED": 0, "DATA": 0, "DECLARED FUNCTION": 0, "RULE/CONST": 0, "NUISANCE": 0}
    for _, s in C469_ROWS:
        c469[s] += 1
    print(f"\n  RECONCILIATION with CFG469's 15 ({c469}):")
    delta = 0
    for sgn, why in RECONCILE:
        delta += int(sgn)
        print(f"    {sgn}  {why}")
    print(f"    15 {delta:+d} = {15 + delta}  (this lane's total: {total})")

    # ------------------------------------------------------------------ section 2: scorecard
    print("\n" + "=" * 118 + "\n2. SCORECARD: every status-board tile under option C\n" + "=" * 118)
    score = []
    for g, name, st, lab in board:
        t = T.get(name)
        if t is None:
            score.append(dict(group=g, tile=name, board=st, under_c="UNSCORED", note="", deps=[], chassis=None, ev=[]))
            continue
        under = t["under_c"]
        missing = [d for d in t["deps"] if d not in RID]
        note = t["note"]
        flag = None
        if missing:
            # missing-rule flag: the committed result for the object without that item, else UNSUPPORTED
            if "E4" in missing and name == "Structure growth, candidate B":
                under = N["424_mut_verdict"]  # read from the committed JSON
                flag = (f"MISSING RULE E4 -> committed CFG424 'MUTATE (no compensation)': sigma8 {N['424_mut_s8']:.4f}, "
                        f"max|P-1| {N['424_mut_pdev']:.3f} > 0.10 -> {N['424_mut_verdict']}")
            else:
                under = "UNSUPPORTED"
                flag = f"MISSING RULE(S) {missing}: no committed result for the object without them"
            note = flag + " | " + note
        score.append(dict(group=g, tile=name, board=st, under_c=under, note=note, deps=t["deps"], chassis=t["chassis"],
                          parts=t["parts"], ev=t["ev"], flag=flag))
    cur = None
    for s in score:
        if s["group"] != cur:
            cur = s["group"]
            print(f"\n  -- {cur}")
        print(f"  {s['tile']:36s} board {s['board']:5s} -> C: {s['under_c']:11s} {'[chassis]' if s['chassis'] else ''}")
        if s.get("parts"):
            for k, v in s["parts"].items():
                print(f"        part: {k}: {v}")
        print(f"        {s['note']}")
    tally = {}
    for s in score:
        tally[s["under_c"]] = tally.get(s["under_c"], 0) + 1
    btally = {}
    for s in score:
        btally[s["board"]] = btally.get(s["board"], 0) + 1
    print(f"\n  Board tally: {btally}")
    print(f"  Under C   : {tally}")

    print("\n  RELATIVISTIC PREDICTIONS THAT BECOME UNAVAILABLE:")
    for what, where, _ in UNAVAILABLE:
        print(f"    - {what}  [{where}]")
    print("\n  RESULTS LOST BY DROPPING THE CHASSIS (none is a pass of B):")
    for what, kind, detail, _ in LOST:
        print(f"    - {what} [{kind}]: {detail}")

    # ------------------------------------------------------------------ section 3: consistency
    print("\n" + "=" * 118 + "\n3. INTERNAL CONSISTENCY (pairs of recipe items)\n" + "=" * 118)
    conflicts, tensions, consistent = [], [], []
    present = lambda *ids: all(i in RID for i in ids)
    # C1 lensing-edge clash
    if present("E1", "E2", "E3"):
        kids_fail = N["487_E1_canonical"] > 4 and N["487_E1_alt"] > 4
        sparc_fail = (not N["487_sparc_V1"]) and (not N["487_sparc_V2"])
        res_x04 = (N["413_x04_canonical"] <= 4 and N["413_x04_alt"] <= 4 and N["414_ok"])
        c1 = dict(id="C1", pair="E1 (KiDS edge x_e = 0.4) vs E2/E3(/E4) (supply postulate -> 5.85 r_M growth edge)",
                  established=kids_fail and sparc_fail,
                  evidence=(f"5.85 r_M on real lenses: KiDS chi2 - best +{N['487_E1_canonical']:.1f} / +{N['487_E1_alt']:.1f} "
                            f"(> 4, CFG487); SPARC alt dwarfs FAIL (CFG487 A3 0.864); early-type levels chi2 30.5 / 38.1 vs "
                            f"<= 12.59 (CFG485 R8, CFG494 K4, CFG497 K5). Growth needs the edge + conservation (CFG424-460, 16/16)."),
                  resolutions=[
                      ("HAND-SET, NON-CONSERVING", res_x04,
                       f"one support x = 0.4 r_ta for both: KiDS +{N['413_x04_canonical']:.2f} / +{N['413_x04_alt']:.2f} vs best "
                       f"(CFG413), growth 512^3 {N['414_can']:.4f} / {N['414_alt']:.4f} (CFG414, alt knife-edge by 0.0004), SPARC "
                       f"untouched for x >= 0.16 (CFG487 E2 row), early types pass with any extended edge (CFG494). Costs: x hand-set "
                       f"(owner 10-07: 'nothing chosen by hand'; CFG414 calls itself a diagnostic), CFG414 runs the RES rule "
                       f"with hand-set R_c = 3 Mpc/h (+1 constant) and no per-catchment conservation"),
                      ("ZERO-KNOB clock taper, no edge (CFG487 V1)", False,
                       f"passes KiDS +{N['487_noedge_canonical']:.2f} / +{N['487_noedge_alt']:.2f} and SPARC, but growth TENSION "
                       f"(post-hoc V1-CATCH max|P-1| {N['487_catch_can']:.3f} / {N['487_catch_alt']:.3f}); V1 is an MS1 exception"),
                      ("PENDING: CFG498 clock taper + capped per-catchment conservation", None,
                       "criteria d9c739010 committed; no committed result"),
                  ])
        status = "PENDING / RESOLVED ON RECORD only HAND-SET" if res_x04 else "PENDING"
        c1["status"] = status if c1["established"] else "NOT ESTABLISHED"
        (conflicts if c1["established"] else consistent).append(c1)
    # C2 clock without the edge vs growth (only if the optional clock replaces the edge)
    if present("R1c"):
        c2 = dict(id="C2", pair="R1c (settling clock as the support, no edge) vs growth's need for confinement",
                  established=all(v == "TENSION" for v in N["487_catch_verdicts"]),
                  evidence=(f"CFG487 POST-HOC V1-CATCH: max|P-1| {N['487_catch_can']:.3f} / {N['487_catch_alt']:.3f}, overdraw 26% / 52% "
                            f"-> TENSION. With the edge, the clock is NOT DIAGNOSTIC for growth (FRW-firing control also passes)."),
                  status="CONDITIONAL on using the clock as the support; CFG498 PENDING")
        (conflicts if c2["established"] else consistent).append(c2)
    # C3 V1 clock vs MS1 (bound-only switch reads baryons only)
    if present("R1c", "S1"):
        tensions.append(dict(id="C3", pair="R1c-V1 (cold-energy clock) vs MS1 (the switch reads baryons, never the carrier)",
                             evidence=(f"CFG487: V1 is an MS1 EXCEPTION, NOT ADMISSIBLE under original MS1; V2 (strict MS1) alone "
                                       f"fails KiDS +{N['487_V2noedge_canonical']:.1f} / +{N['487_V2noedge_alt']:.1f}"),
                             status="RULE-LEVEL CONFLICT only if the V1 clock is adopted; the owner relaxed MS1 for testing (CFG351, 10-08 'test both')"))
    # C4 supply limit vs cluster levels
    if present("E2", "E5"):
        tensions.append(dict(id="C4", pair="E2 (supply-limited settling) vs E5 (max rule; cluster levels)",
                             evidence="CFG379 FAILS (supply limit does not set the X-COP / group / MW levels); CFG497 bonus: clusters "
                                      "FAIL by 0.007 / 0.008 at b = 0 for every supply >= nu - 1. The X-COP identity tile itself passes "
                                      "through E5.",
                             status="TENSION (level prediction fails); no board tile flips"))
    # C5 switch vs background rule
    if present("S1", "B1"):
        consistent.append(dict(id="C5", pair="S1 (bound-only switch) vs B1 (GR + CDM background)",
                               evidence="CFG487: the switch is exactly OFF on FRW and in linear parcels; CMB lensing 1.000 and forest "
                                        "0.00 with the bound-only switch (GATES 3.02 / 3.12)",
                               status="CONSISTENT"))
    # C6 kernel vs kappa
    if present("K1", "F1"):
        tensions.append(dict(id="C6", pair="K1 (kernel) vs F1 (kappa)",
                             evidence="CFG493: switching nu_mono to the quadrature form moves every route by +0.06 to +0.09 dex "
                                      "(kappa 0.417 -> 0.489), more than the 1/2 vs 1/sqrt(pi) gap; CFG468 frozen, no committed result",
                             status="DEPENDENCY, not a conflict: kappa must be refitted with the kernel; the recipe fixes nu_mono"))
    # C7 relaxation without a force vs conservation of the cold energy
    if present("R1", "E4"):
        tensions.append(dict(id="C7", pair="R1 (relaxation with no force) vs E4 (mass conservation)",
                             evidence="mass is conserved per catchment (CFG424 source sum ~4e-4 of Sigma e), but energy and momentum of "
                                      "settling are not tracked: G9 is UNTESTED under C, and the settling force is not derived "
                                      "(working model open piece 1; CFG461)",
                             status="UNTESTED consistency (bookkeeping), not a demonstrated conflict"))
    for c in conflicts:
        print(f"\n  CONFLICT {c['id']}: {c['pair']}")
        print(f"    evidence: {c['evidence']}")
        for lab_, ok, txt in c.get("resolutions", []):
            print(f"    resolution [{lab_}] -> {'passes both' if ok else ('PENDING' if ok is None else 'does not pass both')}: {txt}")
        print(f"    status: {c['status']}")
    for c in tensions:
        print(f"\n  TENSION/DEPENDENCY {c['id']}: {c['pair']}\n    evidence: {c['evidence']}\n    status: {c['status']}")
    for c in consistent:
        print(f"\n  CONSISTENT {c['id']}: {c['pair']}\n    evidence: {c['evidence']}\n    status: {c['status']}")

    # ------------------------------------------------------------------ controls
    print("\n" + "=" * 118 + "\nCONTROLS\n" + "=" * 118)
    names_board = [b[1] for b in board]
    # The frozen text says "33 parsed tiles"; the board has 11 + 8 + 6 + 4 = 29. The literal check is kept and fails
    # (README disclosure 1); K1b scores the rule's intent: every parsed tile scored once, none invented.
    check("K1 tile coverage (literal: 33 tiles)", len(board) == 33,
          f"{len(board)} board tiles parsed (frozen text said 33: a counting error in the criteria, kept)")
    check("K1b tile coverage (every parsed tile scored once, none invented)",
          set(names_board) == set(T) and len(names_board) == len(set(names_board)) and all(s["under_c"] != "UNSCORED" for s in score),
          f"{len(board)} parsed; {len(T)} scored; extra {sorted(set(T) - set(names_board))}; missing {sorted(set(names_board) - set(T))}")
    allev = [e for r in RECIPE for e in r["ev"]] + [e for t in T.values() for e in t["ev"]] + \
            [u[2] for u in UNAVAILABLE] + [e for l in LOST for e in l[3]]
    bad = []
    for p, q in allev:
        try:
            ok = q in head(p)
        except FileNotFoundError:
            ok = False
        QUOTES.append((p, q, ok))
        if not ok:
            bad.append((p, q))
    check("K2 provenance (quotes verbatim at HEAD)", not bad, f"{len(allev) - len(bad)}/{len(allev)} found" +
          ("" if not bad else f"; missing: {bad}"))
    up = [s["tile"] for s in score if ORDER.get(s["under_c"], 0) > ORDER.get(s["board"], 0)]
    check("K3 no upgrade", not up, f"tiles raised: {up}")
    c469_tiles = ["Gravity waves at light speed", "Equations well-posed (high freq.)", "Full nonlinear well-posedness",
                  "Lapse condition, realistic matter", "Binary pulsars", "Strong coupling", "Solar system (PPN + Cassini Q2)",
                  "Matter conservation (G9)", "Structural order (G0)", "Zero-field nonlinear, ungated",
                  "Black holes (EHT, LIGO ringdown)", "Radiative stability (G12)"]
    chas = [s["tile"] for s in score if s["chassis"]]
    check("K4 CFG469 reproduction", set(c469_tiles) <= set(chas) and len(C469_ROWS) == 15 and
          (c469["FITTED"], c469["DATA"], c469["DECLARED FUNCTION"], c469["RULE/CONST"], c469["NUISANCE"]) == (2, 2, 1, 9, 1),
          f"12/12 CFG469 tiles flagged chassis ({len(chas)} incl. growth-alone); CFG469 rows {c469}")
    k5 = [(round(N["424_mut_pdev"], 3), 0.154), (round(N["487_E1_canonical"], 1), 60.5), (round(N["487_E1_alt"], 1), 70.6),
          (round(N["487_noedge_canonical"], 2), 2.05), (round(N["487_noedge_alt"], 2), 0.71), (round(N["414_alt"], 4), 0.0996),
          (round(N["425_R3"], 3), 0.033), (round(N["439_alt"], 3), 0.040), (round(N["439_de"], 3), 0.033), (round(N["460"], 3), 0.040)]
    check("K5 JSON numbers reproduce README values", all(a == b for a, b in k5), str(k5))
    reads498 = [p for p in _cache if "CFG498" in p and not p.endswith("FROZEN_CRITERIA.md")]
    check("K6 pending-lane guard (no CFG498 result read)", not reads498, f"CFG498 files read: {reads498}")

    # ------------------------------------------------------------------ verdict (frozen §5)
    known_board_fail = {s["tile"] for s in score if s["board"] == "FAIL"}
    new_bad = [s for s in score if s["under_c"] in ("FAIL", "TENSION", "UNSUPPORTED") and s["tile"] not in known_board_fail]
    unresolved = [c for c in conflicts if not c["status"].startswith("PENDING") and not c["status"].startswith("CONDITIONAL")
                  and "RESOLVED" not in c["status"]]
    if new_bad or unresolved:
        verdict = "C NOT VIABLE"
        why = ([f"tile '{s['tile']}' {s['board']} -> {s['under_c']} ({s.get('flag') or 'scored'})" for s in new_bad] +
               [f"unresolved conflict {c['id']}" for c in unresolved])
    elif conflicts:
        verdict = "C VIABLE WITH CONFLICTS"
        why = [f"{c['id']}: {c['pair']} [{c['status']}]" for c in conflicts]
    else:
        verdict = "C VIABLE AS RECIPE"
        why = ["no conflict; no new FAIL"]
    print("\n" + "=" * 118)
    print(f"VERDICT (frozen rule): {verdict}")
    for w in why:
        print(f"  - {w}")
    print(f"  Constants: {total} counted (2 fitted, 2 data, 1 declared function, {len(counts['DECLARED CONSTANT'])} declared constants, "
          f"{len(counts['DECLARED RULE'])} declared rules, 1 discrete choice, 1 nuisance)" if not MUTATE else f"  Constants: {total}")
    print(f"  Untested under C: {tally.get('UNTESTED', 0)} tiles + PPN part of the Solar-System tile; moot: {tally.get('MOOT', 0)}; "
          f"plus the GATES 4.02-4.04 / 4.08 / 5.02-5.05 relativistic rows. Untested is not passed.")
    print("  kappa FITTED; cold energy's mass required; no particle; supply postulate an input; not 'theory closed'.")
    print("=" * 118)

    ctrl_ok = all(ok for _, ok, _ in CHECKS)
    print(f"Controls: {sum(ok for _, ok, _ in CHECKS)}/{len(CHECKS)} pass" + ("" if ctrl_ok else
          " -> exit 1 (frozen §7: main exits 0 iff K1-K6 pass; the K1 literal failure is a criteria counting error, disclosed)"))
    mut = None
    if MUTATE:
        g = [s for s in score if s["tile"] == "Structure growth, candidate B"][0]
        flagged = bool(g.get("flag")) and g["under_c"] in ("TENSION", "FAIL")
        changed = verdict != "C VIABLE WITH CONFLICTS"
        mut = dict(growth_flagged=flagged, growth_status=g["under_c"], verdict_changed=changed)
        print(f"MUTATE: growth tile flagged = {flagged} ({g['under_c']}); verdict changed from the main expectation = {changed}")
        print("MUTATE: TEETH DETECTED" if (flagged and changed) else "MUTATE: TEETH NOT DETECTED")

    out = dict(lane="CFG500", mode="MUTATE" if MUTATE else "main", frozen="21b1db999",
               recipe=[{k: r[k] for k in ("id", "name", "status", "c469", "tested_by")} for r in RECIPE],
               count=dict(total=total, by_class={c: counts[c] for c in COUNTED}, optional=opt, inherited_not_counted=inh,
                          cfg469=c469, reconcile=RECONCILE),
               scorecard=[{k: s.get(k) for k in ("group", "tile", "board", "under_c", "note", "deps", "chassis", "parts", "flag")}
                          for s in score],
               tally_board=btally, tally_under_c=tally,
               unavailable=[(a, b) for a, b, _ in UNAVAILABLE], lost=[(a, b, c) for a, b, c, _ in LOST],
               conflicts=[{k: (v if k != "resolutions" else [(x, y, z) for x, y, z in v]) for k, v in c.items()} for c in conflicts],
               tensions=tensions, consistent=consistent, numbers=N, verdict=verdict, verdict_reasons=why,
               checks=[(a, b, c) for a, b, c in CHECKS], quotes_checked=len(QUOTES), mutate=mut)
    with open(os.path.join(HERE, f"cfg500_results{TAG}.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    if MUTATE:
        return 1  # by design (frozen §6); the printed line says whether the teeth were detected
    return 0 if ctrl_ok else 1


if __name__ == "__main__":
    sys.exit(main())
