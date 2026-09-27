#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG0 -- THE PARAMETER-REDUCTION MAP: can the framework's own findings fix, tie or remove the free constants of the record's
working constructions?

WHY.  The campaign's rule 0 (CHARTER.md): build on the framework's own findings and reduce the parameter space.  The inventory
of those findings is CFG0_own_findings_inventory.md.  This script takes every free or declared constant of the record's working
constructions -- the derivation chain's knob ledger (real_research/derivation_chain_2026/README.md and CHAIN_STATUS.md) -- and,
for each one, computes whether one of those findings fixes it, ties it to another constant, or makes it unnecessary.  Every
candidate is checked on the gates it touches, on both a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) wherever a0
enters.

RULES APPLIED.
  * kappa = 1/2 is FITTED (Z = c H_Lambda/a0 = sqrt(32 pi/3) = 5.7888 is kappa restated, never ~21); nothing here derives it.
  * A coincidence counts as a reduction ONLY if it passes every gate it touches AND an action-level mechanism for it exists in
    the record.  Otherwise it is reported as numerology, with its look-elsewhere rate.
  * Withdrawn or superseded items are never used as inputs.
  * Only committed files are read, read-only.  Nothing else in the repository is run or written.

INPUTS (committed, read-only):
  real_research/derivation_chain_2026/: README.md, CHAIN_STATUS.md, FP0/FP7/FP12/FP15/FP17/FP19 results JSON;
  real_research/cross_thread_review_2026_09_26/: XR20 (both parts), XR22, XR25 results JSON;
  real_research/dark_fluid_2026/FL1_order_parameter_results.json and FL1_order_parameter.py (text);
  qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2/paper_numbers.json (the measured kappa);
  hunt_2026/h72_where_the_boost_ends.out and .py (text); fable_independent_2026/L274_a0z_theories_chart.out;
  real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md and mi_snia_power_curve_2026.py (text).
  External data used as a gate: Planck 2018's omega_c = 0.1200 +- 0.0012 (TT,TE,EE+lowE+lensing), for the dark amount only.

PRE-DECLARED HYPOTHESES (written into this docstring before the first run of this script.  They rest on pencil-and-paper
estimates and on reading the committed files above; no exploratory numerics were run before them):
  H1  kappa: no own finding fixes it.  Both measured values lie within 1 sigma of 1/2 (0.465 +- 0.076; 0.547 +- 0.175), and so
      does the horizon coefficient 0.461.  FITTED stays FITTED.
  H2  xi = the Compton length hbar/(m c), for m in [1.9, 5.2]e-19 eV, lies >= 500x below xi's AQUAL floor on both footings.
      FAILS.  (This is the tie the MUTATE adopts.)
  H3  ONE_NEW_THING's mass hbar c/xi, over xi's whole window [floor, 100 pc], is <= 3e-22 eV, >= 500x below the chain's
      dark-mass floor.  The "fuzzy mass" coincidence cannot tie xi to the chain's m.
  H4  de Broglie at the theory's own speed, hbar/(m v_k) with v_k = 575-650 km/s, lies below the AQUAL floor for every allowed m
      on both footings (FP17 B1 reproduced).  FAILS.
  H5  de Broglie at a galaxy speed, hbar/(m x 200 km/s), lies inside xi's window only at the light end of m (m <~ 4e-19 eV).
      200 km/s is no constant of the theory, so the tie trades xi for a declared velocity.  NOT a reduction.
  H6  xi look-elsewhere: of the lengths built from (hbar/m, a0, c, H_Lambda, v_k) with simple exponents, >= 2 land in xi's window,
      and the chance that >= 1 lands is >= 50%.  Every landing is numerology.
  H7  lambda: over lambda in (0, 0.03] every scored observable moves by <= 1.5% (the tracking speed, alpha_2 v^2, sigma_8); the
      tracking gate holds with a margin >= 5; strong coupling stays at ell_sc <= 2 cm.  lambda can be pinned to its inert range:
      KNOB -> REGULATOR (a declared range, not a derivation).
  H8a the full turnaround trigger, R(z) = 1 + delta_ta(z) (LCDM spherical collapse): at z = 2.5, R sits >= 5x below the
      forest/flagship band.  FAILS.  delta_t0 and q are not removed.
  H8b the LCDM turnaround contrast today, 1 + delta_ta(0), lies in [10, 12.5]: below FP15's floor-mass band [12.59, 14.63] and
      below the web's filament line (delta_t0 >= 12.74), but inside XR12's plain-reading band [7.54, 14.6].  As a tie of zeta
      alone (FK1's q = 7/4 kept) it FAILS, narrowly, on the floor-mass reading.
  H8c the turnaround contrast runs the wrong way for q: R_ta(2.5)/R_ta(0) < 1, against the ~4.7 the gates need.
  H9  the turnaround separator as a response gate (MOND on only inside the turned-around region): the chain's own zero-velocity
      radius (FP12/FP11), at the baryonic masses of the four KiDS bins, lies below h72's 3-sigma lower bound on where the boost
      ends, in every bin and on both footings.  FAILS KiDS; L_Lambda is not removed.  (The source-gate version is not decided.)
  H10 L_Lambda: FP19 B1 reproduces (kappa^8 a0/H_Lambda^2 = 3.63 Mpc in [2.65, 4.6]; chances 80% / 31%).  In the sigma_8-tight
      window [2.65, 3.0] no power of kappa or Z lands.  An extended grammar of own lengths lands with chance >= 30%: numerology.
  H11 the dark amount: no committed relation ties Omega_c to (kappa, Omega_Lambda).  In the grammar kappa^a (8 pi/3)^(b/2)
      pi^c Omega_Lambda^d with small exponents the hits within Planck's 1 sigma are consistent with chance (>= 0.5 expected), and
      kappa^2 = 1/4 fails by >= 3 sigma.  The amount stays initial data.
  H12 GDM: at the chain's mass floor the field's GDM parameters are <= 1e-15 (c_s^2) and <= 1e-19 (w at recombination), and the
      record's own CMB bound (w0 <= 2e-14) is met for any m >= 1e-25 eV.  GDM fixes the form (a cold fluid plus an amount), not m.
  H13 the SN-Ia step and the environment null fix no constant and no kernel shape (the step is not an acceleration effect; the
      environment null is shape-blind).  The null does select rho_Lambda over rho_local for P1's density (L0b).
  H14 q = n - 1/4 (n_t ~ L^-2, with H_K1's n = 2) reproduces the data-pinned q = 7/4 exactly.  But the identifications
      n_t ~ L^-k (k = 1, 2, 3) hit the q-window with chance >= 30%, and no action term selects k: numerology, not counted.
  H15 eps: no own finding fixes it.  (hbar a0/m)^(1/3) << v_k (>= 50x); c kappa^9 = 585.5 km/s lands in [575, 650] with chance
      >= 15% (numerology, FP15 E3); and the construction's window is empty (FP16).
  H16 the count: exactly one constant changes class (lambda: KNOB -> REGULATOR); kappa stays FITTED; no constant becomes DERIVED.

CHECKS.  Load-bearing: the controls C1-C12 (committed numbers reproduced), L1 (the constant list confirmed from the record),
N1 (every change to the count -- the record's own moves while this lane ran, re-verified here, and every reduction this lane
adopts -- passes every gate it touches) and N2 (the count's bookkeeping).  Reported: H1-H16, each comparing the computed outcome
with its pre-declared hypothesis; a hypothesis that falls is kept as run.  (N1/N2 were re-worded after the first development run,
when the record's XR18b moved lambda in the ledger itself; the hypotheses were not changed.)

MUTATE=1: the parameter-free tie xi = hbar/(m_floor c) -- the Compton length at the chain's dark-mass floor, 1.9e-19 eV -- is
ADOPTED as a reduction.  N1 must FAIL (the tie fails the Solar-System floor on both footings), and N2 with it: rc = 1.

Run from the repository root:  python3 campaign_fresh_gravity/CFG0_parameter_reduction.py   (MUTATE=1 for the control).
One thread by default; a few seconds.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, re, ast, json, math, time, warnings
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MUTATE = os.environ.get("MUTATE", "0") == "1"
OUTDIR = os.environ.get("CFG0_OUTDIR", HERE)                     # development runs wrote to a scratch directory (disclosed)
SLUG = "CFG0_parameter_reduction"
OUT_TXT = os.path.join(OUTDIR, SLUG + ("_MUTATE" if MUTATE else "") + ".out")
OUT_JSON = os.path.join(OUTDIR, SLUG + ("_results_MUTATE" if MUTATE else "_results") + ".json")
_FH = open(OUT_TXT, "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _FH.write(s + "\n")


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


OUT = {"lane": "CFG0", "mutate": MUTATE, "checks": {}, "numbers": {}, "map": [], "count": {}, "ledger": []}
CH = []


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    tag = "PASS" if ok else "FAIL"
    P(f"  [{tag}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


def rel(a, b):
    return abs(a / b - 1.0) if b != 0 else abs(a)


def load(rel_path):
    with open(os.path.join(REPO, rel_path)) as f:
        return json.load(f)


def text(rel_path):
    with open(os.path.join(REPO, rel_path)) as f:
        return f.read()


P(__doc__.split("CHECKS.")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the Compton tie xi = hbar/(m_floor c) is ADOPTED as a reduction -- N1 and N2 must FAIL (rc = 1) ***")

# ================================================================================================================ inputs
CHAIN = "real_research/derivation_chain_2026/"
HUB = "real_research/cross_thread_review_2026_09_26/"
FP0 = load(CHAIN + "FP0_core_postulates_results.json")
FP7 = load(CHAIN + "FP7_aqual_type_repair_results.json")
FP12 = load(CHAIN + "FP12_local_volume_groups_r0_results.json")
FP15 = load(CHAIN + "FP15_zero_knob_dark_sector_results.json")
FP17 = load(CHAIN + "FP17_screening_without_xi_results.json")
FP19 = load(CHAIN + "FP19_hs_repair_results.json")
XR20 = load(HUB + "XR20_a0_lambda_tie_results.json")
XR20E = load(HUB + "XR20_evolving_de_a0z_results.json")
XR22 = load(HUB + "XR22_prereg_statistic_results.json")
XR25 = load(HUB + "XR25_lambda_regulator_results.json")
XR18B = load(HUB + "XR18b_ramp_lambda_results.json")                 # landed during this lane (3c0cf3c37)
FP20B = load(CHAIN + "FP20b_rescore_fp15_fp16_fp19_results.json")    # landed during this lane (3924bb8c2)
FL1 = load("real_research/dark_fluid_2026/FL1_order_parameter_results.json")
PN = load("qwen_claude_field_theory/papers_2026/mnras_submission_2026_v2/paper_numbers.json")
README_CHAIN = text(CHAIN + "README.md")
STATUS_CHAIN = text(CHAIN + "CHAIN_STATUS.md")

c, G = 299792458.0, 6.67430e-11
PC = 3.0856775814913673e16
MPC, KPC = 1e6 * PC, 1e3 * PC
MSUN = 1.98847e30
HBARC = 1.973269804e-7                       # eV m
MP_C2 = 938.27208816e6                       # eV (proton rest energy; used only to show FP17 M3's stellar-mass numerology)
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153    # the chain's cosmology (FP0)
H0 = H0_KMS * 1e3 / MPC
RHO_C = 3 * H0 ** 2 / (8 * math.pi * G)
RHO_L = OM_L * RHO_C
H_L = H0 * math.sqrt(OM_L)
LAM = 8 * math.pi * G * RHO_L / c ** 2
KAPPA = 0.5
Z_FW = math.sqrt(32 * math.pi / 3)
A0 = {"canonical": KAPPA * c * math.sqrt(G * RHO_L), "alt": KAPPA * c * math.sqrt(G * RHO_C)}
FEET = ("canonical", "alt")
XI_FLOOR = {f: FP7["numbers"]["A4"]["AQUAL_floors"][f]["floor"] for f in FEET}      # pc, FP7 A4 (Saturn monopole binds)
XI_CEIL = 100.0                                                                     # pc, FP14 F14p / FP17
M_FLOOR = (1.9e-19, 5.2e-19)                 # eV: the dark field's mass floor range (FP4 L10f; L383; FP17 M_DARK)
V_KICK = (575e3, 650e3)                      # m/s: FK1's kick window (FP10/FP15 E4)
Y_ADOPT = {}                                 # the reductions this lane adopts: name -> dict(gates=..., ok=...)


def E_of(z):
    return math.sqrt(OM_M * (1 + z) ** 3 + OM_L)


# ================================================================================================================ C controls
banner("C  CONTROLS: committed numbers reproduced")

# ---- C1 the core law, both footings, the uniqueness of its form
a_, b_, d_ = sp.symbols("a b d")
Mdim = sp.Matrix([[3, 1, -3], [-1, 0, 1], [-2, -1, 0]])           # [m, kg, s] of G, c, rho
sol = sp.solve(list(Mdim * sp.Matrix([a_, b_, d_]) - sp.Matrix([1, 0, -2])), [a_, b_, d_], dict=True)
uniq = len(sol) == 1 and sol[0] == {a_: sp.Rational(1, 2), b_: 1, d_: sp.Rational(1, 2)} and abs(Mdim.det()) == 2
kz_id = sp.simplify(sp.Rational(1, 2) * sp.sqrt(32 * sp.pi / 3) - sp.sqrt(8 * sp.pi / 3)) == 0
n0 = FP0["numbers"]
c1_dev = max(rel(A0["canonical"], n0["a0_canonical"]), rel(A0["alt"], n0["a0_rho_total"]), rel(Z_FW, n0["Z"]),
             rel(RHO_L, n0["rho_Lambda"]), rel(H_L, n0["H_Lambda"]))
OUT["numbers"]["C1"] = dict(a0=A0, Z=Z_FW, rho_Lambda=RHO_L, H_Lambda=H_L, Lambda=LAM, max_rel_dev=c1_dev)
check("C1 CONTROL: FP0's a0 (9.3603e-11 canonical / 1.1312e-10 alt), Z = sqrt(32 pi/3), rho_Lambda and H_Lambda reproduced to 1e-12; "
      "the form a0 = xi c sqrt(G rho) is unique (|det| = 2, exponents (1/2, 1, 1/2)); kappa Z = sqrt(8 pi/3) exactly",
      f"a0 {A0['canonical']:.4e} / {A0['alt']:.4e}; Z {Z_FW:.10f}; max rel dev {c1_dev:.1e}; unique {uniq}; kappa Z identity {kz_id}",
      c1_dev < 1e-12 and uniq and kz_id)

# ---- C2 the measured kappa (estimator A = BTFR intercept, estimator B = distance-free shape estimator, corrected)
kA = PN["A_selfconsistency"]["frozen"] / PN["S1"]["A_L"]
sA = 0.076                                                        # estimator A's budget (mi_btfr_intercept_kappa_door_2026.py)
S2 = PN["S2"]
kB = S2["kappa_B"]
sB = math.sqrt(S2["B_budget"]["ml_grid"] ** 2 + S2["B_budget"]["gas"] ** 2 + S2["B_budget"]["stat"] ** 2)
cand = {c_["name"]: c_ for c_ in PN["S3"]["candidates"]}
pull_half = [(0.5 - 0.465) / 0.076, (0.5 - round(kB, 3)) / round(sB, 3)]
k_hor = math.sqrt(8 * math.pi / 3) / (2 * math.pi)
c2_ok = (round(kA, 3) == 0.465 and rel(sB, S2["sigma_B"]) < 1e-12 and (round(kB, 2), round(sB, 2)) == (0.55, 0.17)
         and max(abs(pull_half[i] - cand["1/2 (this paper)"]["pulls"][i]) for i in (0, 1)) < 1e-12
         and rel(k_hor, PN["S3"]["kappa_horizon"]) < 1e-12)
OUT["numbers"]["C2"] = dict(kappa_A=kA, sigma_A=sA, kappa_B=kB, sigma_B=sB, pulls_half=pull_half, kappa_horizon=k_hor)
check("C2 CONTROL: the measured kappa -- estimator A 0.465 (a0 8.7091e-11 / c sqrt(G rho_Lambda)) +- 0.076; estimator B 0.547 +- 0.175 "
      "(= sqrt(ml_grid^2 + gas^2 + stat^2), quoted 0.55 +- 0.17, superseding 0.551 +- 0.043); the pulls of 1/2 and k03's horizon "
      "coefficient 0.461 reproduce paper_numbers.json exactly",
      f"kappa_A {kA:.5f}; kappa_B {kB:.5f} +- {sB:.5f}; pulls of 1/2 {pull_half[0]:+.4f} / {pull_half[1]:+.4f}; horizon {k_hor:.6f}", c2_ok)

# ---- C3 the a0(z) readings: the flat law, the rival E(z), FP0 R3b's sqrt(rho_DE) and XR20's sqrt(V) tracks, L274's chart row
zs_r = ["0.5", "1.0", "2.5", "5.0", "1100.0"]
dev_E = max(rel(E_of(float(z)), n0["a0z_rival_E"][z]) for z in zs_r)
w0, wa = -0.752, -0.86                                          # DESY5 (the pair FP0 R3b reads from L273's committed .out)


def cpl(z, w0_, wa_):
    rho = (1 + z) ** (3 * (1 + w0_ + wa_)) * math.exp(-3 * wa_ * z / (1 + z))
    w = w0_ + wa_ * z / (1 + z)
    return rho, w


def track(z, kind, w0_=w0, wa_=wa):
    rho, w = cpl(z, w0_, wa_)
    if kind == "density":
        return 0.5 * math.log10(rho)
    if kind == "V":
        return 0.5 * math.log10(rho * (1 - w) / (1 - w0_))
    if kind == "pressure":
        return 0.5 * math.log10(rho * w / w0_)
    raise ValueError(kind)


r3b = math.sqrt(cpl(2.5, w0, wa)[0])
dev_r3b = rel(r3b, n0["a0z_desy5_z25"])
e2 = XR20E["numbers"]["E2"]["DESY5"]
dev_e2 = max(abs(track(float(z), k_) - v_) for k_ in ("V", "density", "pressure") for z, v_ in e2[k_].items())
zz = sp.symbols("z", positive=True)
flat_exact = sp.simplify(((1 + zz) ** (3 * (1 + sp.Integer(-1) + 0)) * sp.exp(-3 * 0 * zz / (1 + zz))) - 1) == 0
row25 = [ln for ln in text("fable_independent_2026/L274_a0z_theories_chart.out").splitlines() if re.match(r"^\s*2\.5\s+[+-]", ln)][0]
cols25 = [float(x) for x in re.findall(r"([+-]\d\.\d+)\s+\[", row25)]
own25, lcdm25 = cols25[0], cols25[4]
c3_ok = dev_E < 1e-12 and dev_r3b < 1e-12 and dev_e2 < 1e-12 and flat_exact and own25 == 0.0 and abs(lcdm25 - 0.334) < 1e-9
OUT["numbers"]["C3"] = dict(E=dict((z, E_of(float(z))) for z in zs_r), r3b_desy5_z25=r3b, xr20_E2_max_dev_dex=dev_e2,
                            L274_z25=dict(own=own25, pressure=cols25[1], density=cols25[2], Hz=cols25[3], lcdm_emergent=lcdm25))
check("C3 CONTROL: the flat law (a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0) = 1 exactly for w = -1); the rival E(z) at z = 0.5-1100 "
      "(FP0 R3); FP0 R3b's DESY5 sqrt(rho_DE) = 0.7956 at z = 2.5; XR20 E2's DESY5 sqrt(V) / density / pressure tracks (21 numbers); "
      "PAPER7/L274's z = 2.5 row (own 0.000, LCDM-emergent +0.334 dex)",
      f"E max dev {dev_E:.1e}; R3b {r3b:.10f} (dev {dev_r3b:.1e}); XR20 E2 max dev {dev_e2:.1e} dex; flat {flat_exact}; "
      f"L274 z = 2.5: own {own25:+.3f}, DESI-pressure {cols25[1]:+.3f}, density {cols25[2]:+.3f}, H(z) {cols25[3]:+.3f}, LCDM {lcdm25:+.3f}", c3_ok)

# ---- C4 XR20 T1 (the unimodular tie) and XR30's K_inf form
kap_alt = A0["alt"] / (c * math.sqrt(G * RHO_L))
lam_over_alpha2 = {"canonical": 8 * math.pi / KAPPA ** 2, "alt": 8 * math.pi / kap_alt ** 2}
dev_c3x = max(rel(lam_over_alpha2[f], XR20["numbers"]["controls"]["C3"][f]) for f in FEET)
vac = {f_: 0.5 * math.log10(1 - float(f_)) for f_ in XR20["numbers"]["T1_vacuum"]}
dev_vac = max(abs(vac[f_] - v_) for f_, v_ in XR20["numbers"]["T1_vacuum"].items())
K_inf = math.sqrt(3 * LAM)
a0_xr30 = (KAPPA / math.sqrt(24 * math.pi)) * c ** 2 * K_inf
dev_lam = rel(LAM, XR20["numbers"]["inputs"]["Lambda"])
c4_ok = dev_c3x < 1e-12 and dev_vac < 1e-12 and rel(a0_xr30, A0["canonical"]) < 1e-12 and dev_lam < 1e-12
OUT["numbers"]["C4"] = dict(Lambda_over_alpha2=lam_over_alpha2, kappa_alt=kap_alt, T1_vacuum=vac, a0_xr30=a0_xr30, K_inf=K_inf)
check("C4 CONTROL: XR20 T1's tie -- Lambda/alpha^2 = 8 pi/kappa^2 = 32 pi = 100.531 (alt 68.834, kappa_alt 0.6043), the vacuum-energy "
      "caveat Delta log a0 = (1/2) log10(1 - rho_vac/rho_Lambda) (-0.0229 dex at 0.1), Lambda itself -- and XR30's "
      "a0 = (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda) equal to the canonical a0",
      f"32 pi {lam_over_alpha2['canonical']:.6f}, alt {lam_over_alpha2['alt']:.6f} (dev {dev_c3x:.1e}); vacuum dev {dev_vac:.1e}; "
      f"XR30 a0 {a0_xr30:.6e} (rel dev {rel(a0_xr30, A0['canonical']):.1e}); Lambda dev {dev_lam:.1e}", c4_ok)

# ---- C5 xi's window and FP17 B1/B2's lengths
XI_TAB = {f: np.array([r_["xi"] for r_ in FP7["numbers"]["A4"]["table_2p32"][f]]) for f in FEET}


def fp7_gate(xi_pc, gate, foot):
    """FP7 A4's AQUAL double-filter gate value at xi (g_ext = 2.32e-10), log-log interpolated, clipped (FP17's own rule)."""
    xs = XI_TAB[foot]
    vs = np.array([max(r_["A"][gate], 1e-12) for r_ in FP7["numbers"]["A4"]["table_2p32"][foot]])
    xq = float(np.clip(xi_pc, xs[0], xs[-1]))
    return float(np.exp(np.interp(math.log(xq), np.log(xs), np.log(vs))))


def hbar_over_m(m_eV):                                   # m^2/s
    return HBARC * c / m_eV


DB = {(m, v): hbar_over_m(m) / v / PC for m in M_FLOOR for v in (200e3, 600e3) + V_KICK}
b1 = FP17["numbers"]["B1"]
dev_b1 = max(rel(DB[(m, v)], b1["db_pc"][f"{m}|{v}"]) for (m, v) in DB)
db_kick = max(DB[(m, v)] for m in M_FLOOR for v in V_KICK)
mono_kick = {f: fp7_gate(db_kick, "M", f) for f in FEET}
dev_mono = max(rel(mono_kick[f], b1["monopole_at_kick"][f]) for f in FEET)
LC = {m: HBARC / m / PC for m in M_FLOOR}
XIQ = {(f, m): (hbar_over_m(m) ** 2 / A0[f]) ** (1 / 3) / PC for f in FEET for m in M_FLOOR}
b2 = FP17["numbers"]["B2"]
dev_b2 = max(max(rel(LC[m], b2["lambda_C_pc"][str(m)]) for m in M_FLOOR),
             max(rel(XIQ[(f, m)], b2["xi_q_pc"][f"{f}|{m}"]) for f in FEET for m in M_FLOOR))
m2win = FP17["numbers"]["M2"]["length_window_pc"]
c5_ok = dev_b1 < 1e-12 and dev_b2 < 1e-9 and dev_mono < 1e-9 and rel(XI_FLOOR["canonical"], 0.024281419855163956) < 1e-15
OUT["numbers"]["C5"] = dict(xi_floor_pc=XI_FLOOR, xi_ceiling_pc=XI_CEIL, FP17_M2_length_window_pc=m2win,
                            deBroglie_pc={f"{k[0]}|{k[1]}": v for k, v in DB.items()}, compton_pc=LC,
                            xi_q_pc={f"{k[0]}|{k[1]}": v for k, v in XIQ.items()}, monopole_at_kick=mono_kick)
check("C5 CONTROL: xi's window -- FP7 A4's AQUAL floors 0.02428 / 0.02683 pc (the Saturn monopole binds), ceiling ~100 pc -- and "
      "FP17 B1/B2's lengths (hbar/(m v) for 8 (m, v) cells; the Compton lengths; xi_q = ((hbar/m)^2/a0)^(1/3)) and B1's monopole "
      "ratio at the kick (FP7's table, FP17's interpolation rule) reproduced",
      f"floors {XI_FLOOR['canonical']:.5f} / {XI_FLOOR['alt']:.5f} pc; B1 dev {dev_b1:.1e}; B2 dev {dev_b2:.1e}; monopole at "
      f"{db_kick:.4f} pc: {mono_kick['canonical']:.3f} / {mono_kick['alt']:.3f} (dev {dev_mono:.1e}); FP17 M2's length window "
      f"{m2win['canonical'][0]:.4f}-{m2win['canonical'][1]:.1f} / {m2win['alt'][0]:.4f}-{m2win['alt'][1]:.1f} pc", c5_ok)

# ---- C6 XR25's lambda scalings (c_2 = infinity: lambda_eff = lambda + 3)
L4 = XR25["numbers"]["L4"]
cs0, al0 = L4["cs_track"]["0.0"], L4["alpha2_v2"]["0.0"]
dev_cs = max(rel(cs0 * math.sqrt(3.0 / (float(l_) + 3.0)), v_) for l_, v_ in L4["cs_track"].items())
_lk = sorted(L4["alpha2_v2"], key=float)
_lv, _av = np.array([float(l_) for l_ in _lk]), np.array([L4["alpha2_v2"][l_] for l_ in _lk])
_A, _B = np.polyfit(_lv, _av, 1)
dev_lin = float(np.max(np.abs((_A * _lv + _B) / _av - 1)))
check("C6 CONTROL: XR25 L4's MOND-regime lambda dependence at c_2 = infinity -- the tracking speed c_s(0) sqrt(3/(lambda + 3)) "
      "reproduces all 6 committed entries to 1e-9, and alpha_2 v^2 is affine in lambda to 1e-6 (lambda = 0 ... 274.8)",
      f"c_s max rel dev {dev_cs:.1e} ({cs0:.1f} -> {L4['cs_track']['274.8']:.1f} km/s); alpha_2 v^2 = {_A:.4e} lambda + {_B:.4e}, max rel "
      f"dev {dev_lin:.1e}", dev_cs < 1e-9 and dev_lin < 1e-6)

# ---- C7 FP15 T6d: the natural numbers of spherical collapse and the delta_t0 band
t6d = FP15["numbers"]["T6d"]
nat = {"1 + delta_c (the collapse threshold, FP13's s)": 1 + 1.686, "9 pi^2/16 (turnaround, EdS)": 9 * math.pi ** 2 / 16,
       "18 pi^2 (virialised, EdS)": 18 * math.pi ** 2}
dev_nat = max(rel(nat[k_], t6d["candidates"][k_]["delta_t0"]) for k_ in nat)
BAND = {f: tuple(t6d["band_delta_t0"][f]) for f in FEET}
EDGE74 = FP15["numbers"]["T3b"]["edges"]["1.75"]["edge"]
DT0 = BAND["canonical"][0] / EDGE74                                   # XR12's delta_t0 per unit zeta (5.31)
check("C7 CONTROL: FP15 T6d's natural numbers (1 + delta_c = 2.686, 9 pi^2/16, 18 pi^2) and its delta_t0 band at the floor mass "
      "(canonical [12.59, 14.63], alt [12.59, 22.79]; lower edge = 5.31 x the forest's zeta edge 2.371)",
      f"dev {dev_nat:.1e}; band {BAND['canonical'][0]:.3f}-{BAND['canonical'][1]:.3f} / {BAND['alt'][0]:.3f}-{BAND['alt'][1]:.3f}; "
      f"5.31 recovered as {DT0:.4f}; width x{BAND['canonical'][1] / BAND['canonical'][0]:.3f} (FP15 M1: x1.16)",
      dev_nat < 1e-9 and abs(DT0 - 5.31) < 0.01)

# ---- C8 FP19 B1's census of the separator length
aL = {f: A0[f] / H_L ** 2 / MPC for f in FEET}                        # a0/H_Lambda^2 in Mpc (FP19 uses the canonical one)
LO_W, HI_W, HI_T = 2.65, 4.6, 3.0
hitsK = [k for k in range(20) if LO_W <= aL["canonical"] * KAPPA ** k <= HI_W]
hitsZ = [k for k in range(10) if LO_W <= aL["canonical"] * Z_FW ** (-k) <= HI_W]
rateK, rateZ = math.log(HI_W / LO_W) / math.log(2.0), math.log(HI_W / LO_W) / math.log(Z_FW)
fb1 = FP19["numbers"]["B1"]
c8_ok = (hitsK == fb1["hits_kappa"] and hitsZ == fb1["hits_Z"] and rel(rateK, fb1["rate"]["kappa"]) < 1e-12
         and rel(rateZ, fb1["rate"]["Z"]) < 1e-12 and fb1["window"] == [LO_W, HI_W] and fb1["window_tight"] == [LO_W, HI_T])
check("C8 CONTROL: FP19 B1's separator-length census -- window [2.65, 4.6] Mpc (sigma_8-tight [2.65, 3.0]); a0/H_Lambda^2 kappa^k "
      "hits k = 8 only; Z^-k none; look-elsewhere 80% (kappa) / 31% (Z)",
      f"a0/H_L^2 = {aL['canonical']:.1f} Mpc; hits kappa^{hitsK} ({aL['canonical'] * KAPPA ** 8:.3f} Mpc), Z^-{hitsZ}; rates "
      f"{rateK:.3f} / {rateZ:.3f}", c8_ok)

# ---- C9 FL1 F5: the free order parameter's GDM parameters
HBARC_MPC, H0_EV = 6.3949e-30, 1.4376e-33                             # FL1's own constants (eV Mpc; eV)


def fl1_row(m_eV):
    worst = 0.0
    for kM in (0.1, 1.0):
        for a_s in (1 / 1101.0, 1.0):
            qv = kM * HBARC_MPC / (2 * m_eV * a_s)
            worst = max(worst, qv ** 2 / (1 + qv ** 2))
    H_rec = H0_EV * math.sqrt(0.315 * 1101 ** 3 * (1 + 1101 / 3400.0))
    return worst, (H_rec / m_eV) ** 2, H_rec


rows_f5 = FL1["numbers"]["F5"]["rows"]
dev_f5 = max(max(rel(fl1_row(float(m_))[0], v_["max_cs2"]), rel(fl1_row(float(m_))[1], v_["w_rec"])) for m_, v_ in rows_f5.items())
check("C9 CONTROL: FL1 F5's GDM parameters of the free order parameter (max c_s^2 over k = 0.1-1 Mpc^-1 and recombination..today; "
      "w_rec ~ (H_rec/m)^2) reproduced for m = 2e-19, 5e-19, 1e-15, 1e-6 eV",
      f"max rel dev {dev_f5:.1e}; m = 2e-19: c_s^2 {rows_f5['2e-19']['max_cs2']:.2e}, w_rec {rows_f5['2e-19']['w_rec']:.2e}", dev_f5 < 1e-12)

# ---- C10 h72: the KiDS isolated-lens bounds on where the sqrt boost ends
h72_out = text("hunt_2026/h72_where_the_boost_ends.out")
h72_src = text("hunt_2026/h72_where_the_boost_ends.py")
H72 = {}
for f in FEET:
    ln = [l_ for l_ in h72_out.splitlines() if re.match(rf"^\s*{f}\s+3-sigma lower bounds on r_end:", l_)][0]
    H72[f] = [float(x) for x in re.findall(r">\s*([0-9.]+)\s*Mpc", ln)]
LOGM = ast.literal_eval(re.search(r"LOGM = (\{[^}]*\})", h72_src).group(1))
FGAS = ast.literal_eval(re.search(r"FGAS = (\{[^}]*\})", h72_src).group(1))
MB_BIN = {b: 10 ** LOGM[b] * (1 + FGAS[b]) for b in sorted(LOGM)}
c10_ok = all(H72[f] == [1.67, 2.07, 3.44, 2.77] for f in FEET) and abs(MB_BIN[1] / 1.5e10 - 1) < 1e-9 and abs(MB_BIN[4] / 9.13e10 - 1) < 1e-3
OUT["numbers"]["C10"] = dict(h72_bounds_Mpc=H72, Mb_bins_Msun=MB_BIN)
check("C10 CONTROL: h72's committed 3-sigma lower bounds on where the KiDS sqrt boost ends (Brouwer+2021 isolated lenses, four bins, "
      "full 60x60 covariance): > 1.67 / 2.07 / 3.44 / 2.77 Mpc on both footings, at M_b = 10^logM* (1 + f_gas) = 1.50 / 3.66 / "
      "6.01 / 9.13e10 Msun",
      f"canonical {H72['canonical']}, alt {H72['alt']}; M_b " + ", ".join(f"{MB_BIN[b]:.3e}" for b in MB_BIN), c10_ok)

# ---- C11 the chain's zero-velocity radii (FP12 groups, FP11's Local Group) and the R0 - M_b slope
R0_ROWS = {g: {f: FP12["numbers"]["R1"]["rows"][g][f[:3] if f == "canonical" else "alt"]["true"] for f in FEET}
           for g in ("M81", "CenA", "M83", "IC342")}
MB_ROWS = {g: FP12["numbers"]["M1"][g]["nominal"] for g in R0_ROWS}
m_f11h = re.search(r"R0 at the timing-matched mass: HY/A/canonical ([0-9.]+), HY/A/alt ([0-9.]+)", STATUS_CHAIN)
m_f11c = re.search(r"M_b = ([0-9.e+]+) / ([0-9.e+]+) \(can/alt, conv\. A\)", STATUS_CHAIN)
m_f12a = re.search(r"d log R0/d log M_b = ([0-9.]+)", STATUS_CHAIN)
R0_ROWS["LG (FP11, timing mass)"] = {"canonical": float(m_f11h.group(1)), "alt": float(m_f11h.group(2))}
MB_LG = {"canonical": float(m_f11c.group(1)), "alt": float(m_f11c.group(2))}
SLOPE_R0 = float(m_f12a.group(1))
lm = np.log10([MB_ROWS[g] for g in ("M83", "IC342")])
lr = np.log10([R0_ROWS[g]["canonical"] for g in ("M83", "IC342")])
slope_chk = (lr[1] - lr[0]) / (lm[1] - lm[0])
c11_ok = (abs(R0_ROWS["M81"]["canonical"] - 1.3660316806914028) < 1e-12 and SLOPE_R0 == 0.19 and abs(slope_chk - SLOPE_R0) < 0.03
          and R0_ROWS["LG (FP11, timing mass)"]["canonical"] == 1.53)
OUT["numbers"]["C11"] = dict(R0_Mpc=R0_ROWS, Mb_Msun=MB_ROWS, Mb_LG=MB_LG, slope_committed=SLOPE_R0, slope_M83_IC342=slope_chk)
check("C11 CONTROL: the chain's own zero-velocity radii at z = 0 -- FP12's M81/Cen A/M83/IC 342 rows (1.37/1.35/1.24/1.38 Mpc canonical), "
      "FP11's Local Group (1.53 canonical / 1.52 alt at the timing mass 1.65e11 / 1.37e11), and FP12's committed slope "
      "d log R0/d log M_b = 0.19 (recovered from the M83-IC 342 pair to < 0.03)",
      "; ".join(f"{g}: {R0_ROWS[g]['canonical']:.3f}/{R0_ROWS[g]['alt']:.3f}" for g in R0_ROWS) + f"; slope {SLOPE_R0} (pair {slope_chk:.3f})",
      c11_ok)

# ---- C12 the spherical-collapse solver (LCDM top hat, the framework's own Lambda)


def I_omega(om):
    """time integral of a top-hat shell from R = 0 to turnaround, in units sqrt(R_ta^3/GM): x = sin^2(theta) removes both ends."""
    f = lambda th: 2 * math.sin(th) ** 2 / math.sqrt(2 - om * math.sin(th) ** 2 * (1 + math.sin(th) ** 2))
    if om > 0.99:                          # only the root brackets come here (every root found has omega < 0.4): a log end point,
        with warnings.catch_warnings():    # whose value only fixes the bracket's sign; quad's round-off warning there is expected
            warnings.simplefilter("ignore")
            return quad(f, 0.0, math.pi / 2 - 0.2, epsabs=0, epsrel=1e-12, limit=400)[0] + \
                quad(f, math.pi / 2 - 0.2, math.pi / 2, epsabs=0, epsrel=1e-9, limit=2000)[0]
    return quad(f, 0.0, math.pi / 2, epsabs=0, epsrel=1e-13, limit=400)[0]


def turnaround(om):
    """omega = H_L^2 R_ta^3/(G M) in (0, 1): returns (a_ta, 1 + delta_ta) on the chain's flat LCDM background."""
    y = 1.5 * math.sqrt(om) * I_omega(om)
    S = math.sinh(y) ** 2
    return (OM_M / OM_L * S) ** (1 / 3), 2 * S / om


def omega_at_zta(z):
    return brentq(lambda lo: math.log(turnaround(math.exp(lo))[0]) + math.log(1 + z), math.log(1e-12), math.log(1 - 1e-9),
                  xtol=1e-14, rtol=1e-14)


def t_of_a(a):                                                      # cosmic time in units 1/H_L
    return (2.0 / 3.0) * math.asinh(math.sqrt(OM_L / OM_M) * a ** 1.5)


def a_of_t(t):
    return (OM_M / OM_L) ** (1 / 3) * math.sinh(1.5 * t) ** (2 / 3)


def x_vir(om):                                                      # R_vir/R_ta: 2 om x^3 - (2 + om) x + 1 = 0 (energy + virial)
    return brentq(lambda x: 2 * om * x ** 3 - (2 + om) * x + 1, 0.3, 0.55, xtol=1e-15)


def delta_vir(z_coll):
    """the top hat that collapses at z_coll (t_coll = 2 t_ta), virialised at R_vir = x R_ta: Delta over the mean matter density."""
    t_c = t_of_a(1 / (1 + z_coll))
    om = brentq(lambda lo: math.sqrt(math.exp(lo)) * I_omega(math.exp(lo)) - t_c / 2, math.log(1e-14), math.log(1 - 1e-12),
                xtol=1e-14, rtol=1e-14)
    om = math.exp(om)
    a_ta, one_d = turnaround(om)
    return one_d * ((1 / (1 + z_coll)) / a_ta) ** 3 / x_vir(om) ** 3, om


eds_ta = turnaround(1e-9)[1]                                            # the small-omega (EdS) limit
dv0, om_c0 = delta_vir(0.0)
omz = OM_M / (OM_M + OM_L)
x_bn = omz - 1
dv_bn = (18 * math.pi ** 2 + 82 * x_bn - 39 * x_bn ** 2) / omz                 # Bryan & Norman 1998 fit, used only as a code control
dv_hi, _ = delta_vir(1000.0)
om_ta0 = math.exp(omega_at_zta(0.0))
t_quad = math.sqrt(om_ta0) * I_omega(om_ta0)
def _ev(t, y):
    return y[0] - 1e-4


_ev.terminal, _ev.direction = True, -1
sol_ivp = solve_ivp(lambda t, y: [y[1], -(1 / om_ta0) / y[0] ** 2 + y[0]], (0, 5), [1.0, 0.0], method="DOP853", rtol=1e-12,
                    atol=1e-14, events=_ev)
t_ode = float(sol_ivp.t_events[0][0]) + (2.0 / 3.0) * 1e-4 ** 1.5 * math.sqrt(om_ta0 / 2.0)   # + the Kepler tail from R = 1e-4 to 0
c12_ok = (rel(eds_ta, 9 * math.pi ** 2 / 16) < 1e-6 and rel(dv_hi, 18 * math.pi ** 2) < 2e-3 and rel(dv0, dv_bn) < 0.02
          and rel(t_ode, t_quad) < 1e-6)
OUT["numbers"]["C12"] = dict(eds_turnaround=eds_ta, delta_vir_z0=dv0, delta_vir_BN98=dv_bn, delta_vir_z1000=dv_hi,
                             omega_ta_z0=om_ta0, t_ta_quadrature=t_quad, t_ta_ode=t_ode)
check("C12 CONTROL: the LCDM top-hat solver -- the EdS limits (turnaround 9 pi^2/16, virial 18 pi^2 at z = 1000), the virial contrast "
      "for collapse today against Bryan & Norman 1998's fit (within 2%), and the turnaround time by quadrature against a direct "
      "ODE integration of R'' = -GM/R^2 + H_L^2 R (within 1e-6)",
      f"EdS turnaround {eds_ta:.6f} (9 pi^2/16 = {9 * math.pi ** 2 / 16:.6f}); Delta_vir(z = 1000) {dv_hi:.2f} (18 pi^2 = "
      f"{18 * math.pi ** 2:.2f}); Delta_vir(0) {dv0:.1f} vs BN98 {dv_bn:.1f}; t_ta {t_quad:.8f} vs ODE {t_ode:.8f}", c12_ok)

# ================================================================================================================ L the list
banner("L  THE CONSTANT LIST, READ FROM THE CHAIN'S KNOB LEDGER (README) AND CHAIN_STATUS")
led_txt = README_CHAIN.split("## What is derived, and what is not")[1].split("## Where the theory passes")[0]
LED = []
for ln in led_txt.splitlines():
    m_ = re.match(r"^\|\s*(core|separator|dark)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", ln)
    if m_:
        LED.append(dict(sector=m_.group(1), constant=m_.group(2), status=m_.group(3), lanes=m_.group(4)))


def status_word(s):
    """the ledger's status is the row's LEADING keyword (later words describe alternatives, e.g. 'outside it lambda is a knob')."""
    s_ = s.strip().upper()
    for key, word in (("KNOB", "KNOB"), ("REGULATOR", "REGULATOR"), ("ELIMINATED", "ELIMINATED"), ("DECLARED", "DECLARED"),
                      ("NATURAL", "NATURAL CHOICE"), ("IRREDUCIBLE", "FITTED"), ("FITTED", "FITTED"), ("POSTULATED", "POSTULATED"),
                      ("INITIAL DATA", "INITIAL DATA")):
        if s_.startswith(key):
            return word
    return "?"


WANT = {"kappa": None, "xi": r"^xi", "m": r"zeta \(lambda_0\), q, m", "eps": r"^eps", "zeta": r"^zeta", "q": r"zeta \(lambda_0\), q,", "lambda": r"^lambda",
        "alpha_c": r"^alpha_c", "c_2": r"^c_2", "L_Lambda": r"^L_Lambda", "c_y": r"c_y", "n": r"\bn = 2", "ramp": r"ramp",
        "cross quartic": r"cross quartic", "amount": r"amount", "misalignment": r"misalignment"}
FOUND = {}
for k_, pat in WANT.items():
    if pat is None:
        continue
    rows_ = [r_ for r_ in LED if re.search(pat, r_["constant"])]
    if rows_:
        FOUND[k_] = rows_[0]
kap_fitted = bool(re.search(r"\|\s*FP0\s*\|\s*L0c\s*\|\s*FITTED\s*\|\s*kappa = 1/2", STATUS_CHAIN)) and "kappa = 1/2 accepted" in README_CHAIN
if kap_fitted:
    FOUND["kappa"] = dict(sector="core (input)", constant="kappa", status="FITTED (FP0 L0c; accepted)", lanes="FP0, FP5, FP19")
NOW = {k_: ("FITTED" if k_ == "kappa" else status_word(r_["status"])) for k_, r_ in FOUND.items()}   # the ledger at HEAD
# the ledger when this lane began (README at 08548fc85): the same, except lambda, which then read "a MOND-regime knob across
# (0, 274.4] ... Counts as a knob unless that range is shown free of trouble (XR18b)".  XR18b (3c0cf3c37) landed during this lane.
BEFORE = dict(NOW)
BEFORE["lambda"] = "KNOB"
TASK_LIST = ("kappa", "xi", "m", "eps", "zeta", "q", "lambda", "alpha_c", "L_Lambda", "c_y", "n", "ramp", "amount", "misalignment")
missing = [k_ for k_ in TASK_LIST if k_ not in FOUND]
for k_ in list(WANT):
    if k_ in FOUND:
        P(f"    {k_:14s} [{FOUND[k_]['sector']}] ledger: {FOUND[k_]['status'][:120]}{'...' if len(FOUND[k_]['status']) > 120 else ''}")
OUT["numbers"]["L1"] = dict(baseline_lane_start=BEFORE, ledger_now=NOW, ledger_rows=len(LED))
check("L1 THE CONSTANT LIST IS THE RECORD'S: every constant named for this lane (kappa, xi, m, eps, zeta/delta_t0, q, lambda, alpha_c, "
      "L_Lambda, c_y, n, the ramp, the amount, the misalignment) is found in the chain's knob ledger (README) or CHAIN_STATUS "
      "(kappa: FP0 L0c FITTED); c_2 and the cross quartic are found too",
      f"{len(LED)} ledger rows; found {sorted(FOUND)}; missing {missing}; ledger now: " + ", ".join(f"{k_}={v_}" for k_, v_ in NOW.items())
      + f"; lambda at the lane's start: KNOB (XR18b has since made it {NOW.get('lambda')})",
      not missing and "c_2" in FOUND and "cross quartic" in FOUND and "?" not in NOW.values())

# ================================================================================================================ R reductions
MAP = []


def add_map(const, before, after, basis, numbers, verdict):
    MAP.append(dict(constant=const, before=before, after=after, basis=basis, numbers=numbers, verdict=verdict))
    P(f"    MAP  {const:18s} {before:16s} -> {after:16s} | {verdict}")


# ---------------------------------------------------------------------------------------------------------------- R1 kappa
banner("R1  kappa: can an own finding fix it?")
pulls = {"estimator A (BTFR)": (KAPPA - kA) / sA, "estimator B (distance-free, corrected)": (KAPPA - kB) / sB}
pulls_hor = {"A": (k_hor - kA) / sA, "B": (k_hor - kB) / sB}
k01 = "kappa_closure/k01-k03 (zero-mode theorem; the global constraint misses by 1e5; 0.461 vs 1/2 degenerate with H0)"
P(f"    measured: A {kA:.3f} +- {sA:.3f} (pull of 1/2: {pulls['estimator A (BTFR)']:+.2f}), B {kB:.3f} +- {sB:.3f} "
  f"(pull {pulls['estimator B (distance-free, corrected)']:+.2f}); horizon 0.461 pulls {pulls_hor['A']:+.2f} / {pulls_hor['B']:+.2f}")
P(f"    underivable in the present action class: {k01}; KS01 slot NOT LIVE; channel-count capstone closed; postquantum gravity "
  "(L313-L314) gives 1.30-1.45")
P("    no own finding supplies kappa: the uniqueness theorem fixes the FORM only; the flat a0(z) is exactly kappa-blind; the unimodular "
  "tie carries kappa as its coupling")
h1_ok = all(abs(v_) < 1 for v_ in pulls.values()) and all(abs(v_) < 1 for v_ in pulls_hor.values())
check("H1 kappa: no own finding fixes it; both measurements lie within 1 sigma of 1/2, and the horizon coefficient 0.461 "
      "within 1 sigma of both: FITTED stays FITTED",
      f"pulls of 1/2: {pulls['estimator A (BTFR)']:+.2f} / {pulls['estimator B (distance-free, corrected)']:+.2f}; of 0.461: "
      f"{pulls_hor['A']:+.2f} / {pulls_hor['B']:+.2f}", h1_ok, load_bearing=False)
add_map("kappa", BEFORE["kappa"], "FITTED", "FP0 L0c; k01-k03; KS01; C2",
        dict(kappa_A=kA, kappa_B=kB, sigma_B=sB), "no own finding fixes it; consistent with 1/2; underivable in the present class")

# ---------------------------------------------------------------------------------------------------------------- R2 xi and m
banner("R2  xi (the heat filter's length) and its ties to the dark field's mass m")
XR22_V1 = XR22["numbers"]["V1"]
GAM = {f: sorted((float(k_.split("|")[1]), v_["phys"]) for k_, v_ in XR22_V1.items() if k_.startswith(f + "|")) for f in FEET}


def gamma_hat(xi_pc, foot):
    xs = np.array([x for x, _ in GAM[foot]]); gs = np.array([g for _, g in GAM[foot]])
    if xi_pc < xs[0]:
        return float("nan")
    return float(np.interp(math.log(min(xi_pc, xs[-1])), np.log(xs), gs))


def xi_gates(xi_pc):
    """the gates a value of xi touches: the Solar-System floor (FP7 A4, both footings), the ceiling (~100 pc), and the DR4 prediction
    (XR22's committed gamma_hat table, reported)."""
    out = {}
    for f in FEET:
        out[f] = dict(xi_pc=xi_pc, solar_system=xi_pc >= XI_FLOOR[f], ceiling=xi_pc <= XI_CEIL,
                      monopole_ratio=fp7_gate(xi_pc, "M", f), floor_ratio=xi_pc / XI_FLOOR[f], gamma_hat_DR4=gamma_hat(xi_pc, f))
        out[f]["pass"] = out[f]["solar_system"] and out[f]["ceiling"]
    return out


XIC = {}
for m in M_FLOOR:
    XIC[f"Compton hbar/(m c), m = {m:.1e}"] = dict(xi=HBARC / m / PC, param_free=True, mechanism=False)
    for v in V_KICK:
        XIC[f"hbar/(m v_k), m = {m:.1e}, v_k = {v / 1e3:.0f}"] = dict(xi=hbar_over_m(m) / v / PC, param_free=True, mechanism=False)
        XIC[f"h/(m v_k), m = {m:.1e}, v_k = {v / 1e3:.0f}"] = dict(xi=2 * math.pi * hbar_over_m(m) / v / PC, param_free=True, mechanism=False)
    for v in (100e3, 200e3, 300e3):
        XIC[f"hbar/(m v), m = {m:.1e}, v = {v / 1e3:.0f} (galaxy speed)"] = dict(xi=hbar_over_m(m) / v / PC, param_free=False, mechanism=False)
    for f in FEET:
        XIC[f"xi_q = ((hbar/m)^2/a0)^(1/3), m = {m:.1e}, {f}"] = dict(xi=XIQ[(f, m)], param_free=True, mechanism=False, foot=f)
hbar_SI = HBARC * 1.602176634e-19 / c                                     # J s
m_p = MP_C2 * 1.602176634e-19 / c ** 2                                    # kg
M_CH = (hbar_SI * c / G) ** 1.5 / m_p ** 2
for f in FEET:
    XIC[f"r_M(M_Ch) = sqrt(G M_Ch/a0), M_Ch = (hbar c/G)^(3/2)/m_p^2, {f}"] = dict(xi=math.sqrt(G * M_CH / A0[f]) / PC, param_free=True,
                                                                                  mechanism=False, foot=f)
for k_, v_ in XIC.items():
    v_["gates"] = xi_gates(v_["xi"])
    ft = v_.get("foot")
    ok_feet = [f for f in FEET if (ft is None or f == ft) and v_["gates"][f]["pass"]]
    P(f"    {k_:66s} xi = {v_['xi']:.3e} pc  SS floor x{v_['gates']['canonical']['floor_ratio']:.3g} (can) / "
      f"x{v_['gates']['alt']['floor_ratio']:.3g} (alt); window pass: {ok_feet or 'none'}; DR4 gamma_hat "
      f"{v_['gates']['canonical']['gamma_hat_DR4']:.4f} / {v_['gates']['alt']['gamma_hat_DR4']:.4f}")
OUT["numbers"]["R2_candidates"] = {k_: dict(xi_pc=v_["xi"], gates=v_["gates"], param_free=v_["param_free"]) for k_, v_ in XIC.items()}

# H2: Compton
comp = [v_ for k_, v_ in XIC.items() if k_.startswith("Compton")]
comp_factor = min(XI_FLOOR[f] / v_["xi"] for v_ in comp for f in FEET)
check("H2 xi = hbar/(m c) (the Compton length, m = 1.9-5.2e-19 eV) lies >= 500x below xi's AQUAL floor on both footings: FAILS",
      f"Compton {min(v_['xi'] for v_ in comp):.2e}-{max(v_['xi'] for v_ in comp):.2e} pc; at least {comp_factor:.0f}x below the floor",
      comp_factor >= 500, load_bearing=False)

# H3: ONE_NEW_THING's mass
m_xi = {f: (HBARC / (XI_CEIL * PC), HBARC / (XI_FLOOR[f] * PC)) for f in FEET}
m_xi_003 = HBARC / (0.03 * PC)
m_ratio = min(M_FLOOR) / max(m_xi[f][1] for f in FEET)
P(f"    ONE_NEW_THING: hbar c/xi = {m_xi_003:.2e} eV at xi = 0.03 pc (the memo's 2e-22); over the window: "
  + ", ".join(f"{f} {m_xi[f][0]:.1e}-{m_xi[f][1]:.1e} eV" for f in FEET) + f"; the chain's floor 1.9e-19 eV is {m_ratio:.0f}x above")
check("H3 ONE_NEW_THING's mass hbar c/xi over xi's whole window is <= 3e-22 eV, >= 500x below the chain's dark-mass floor: the "
      "'fuzzy mass' coincidence cannot tie xi to the chain's m",
      f"hbar c/xi <= {max(m_xi[f][1] for f in FEET):.2e} eV; floor/that = {m_ratio:.0f}", max(m_xi[f][1] for f in FEET) <= 3e-22 and m_ratio >= 500,
      load_bearing=False)

# H4: de Broglie at the kick (hbar)
dbk = [v_ for k_, v_ in XIC.items() if k_.startswith("hbar/(m v_k)")]
h4_ok = all(not v_["gates"][f]["solar_system"] for v_ in dbk for f in FEET)
check("H4 de Broglie at the theory's own speed, hbar/(m v_k) (v_k = 575-650 km/s), lies below the AQUAL floor for every "
      "allowed m on both footings (FP17 B1 reproduced): FAILS",
      f"hbar/(m v_k) = {min(v_['xi'] for v_ in dbk):.4f}-{max(v_['xi'] for v_ in dbk):.4f} pc vs floors {XI_FLOOR['canonical']:.4f} / "
      f"{XI_FLOOR['alt']:.4f}; monopole at the largest {mono_kick['canonical']:.2f}x / {mono_kick['alt']:.2f}x the bound", h4_ok,
      load_bearing=False)
dbh = [v_ for k_, v_ in XIC.items() if k_.startswith("h/(m v_k)")]
h_all_pass = all(v_["gates"][f]["pass"] for v_ in dbh for f in FEET)
gam_h = [v_["gates"][f]["gamma_hat_DR4"] for v_ in dbh for f in FEET]
P(f"    the h-version (the full de Broglie wavelength of a kicked daughter), h/(m v_k) = {min(v_['xi'] for v_ in dbh):.4f}-"
  f"{max(v_['xi'] for v_ in dbh):.4f} pc: inside the window for every (m, v_k) on both footings: {h_all_pass}; it would predict DR4 "
  f"gamma_hat = {min(gam_h):.4f}-{max(gam_h):.4f}.  Choosing h over hbar is a factor 2 pi picked after the fact, and no action term "
  "couples the heat filter to the daughters (FP17 B4); the daughters have left the galaxies (FP10: retained ~0 in SPARC discs, FP17 B3)")

# H5: de Broglie at galaxy speeds
g200 = {m: XIC[f"hbar/(m v), m = {m:.1e}, v = 200 (galaxy speed)"] for m in M_FLOOR}
m_edge = {f: hbar_over_m(1.0) / 200e3 / (XI_FLOOR[f] * PC) for f in FEET}          # the m at which hbar/(m 200 km/s) = the floor
h5_ok = (g200[1.9e-19]["gates"]["canonical"]["pass"] and g200[1.9e-19]["gates"]["alt"]["pass"]
         and not g200[5.2e-19]["gates"]["canonical"]["pass"] and max(m_edge.values()) <= 4.5e-19)
check("H5 de Broglie at a galaxy speed, hbar/(m x 200 km/s), lies inside xi's window only at the light end of m (m <~ 4e-19 "
      "eV); 200 km/s is no constant of the theory, so the tie trades xi for a declared velocity: NOT a reduction",
      f"xi = {g200[1.9e-19]['xi']:.4f} pc at 1.9e-19 eV (the task's ~0.05 pc), {g200[5.2e-19]['xi']:.4f} pc at 5.2e-19; the floor is reached "
      f"at m = {m_edge['canonical']:.2e} (can) / {m_edge['alt']:.2e} (alt) eV", h5_ok, load_bearing=False)

# H6: look-elsewhere
FAM = {}
for m in M_FLOOR:
    lamC = HBARC / m                                                        # m
    for f in FEET:
        for qn, qv in (("0", 0.0), ("-1/4", -0.25), ("-1/3", -1 / 3), ("-1/2", -0.5), ("-2/3", -2 / 3), ("-3/4", -0.75), ("-1", -1.0)):
            FAM[f"lambda_C (lambda_C a0/c^2)^({qn}), m = {m:.1e}, {f}"] = (lamC * (lamC * A0[f] / c ** 2) ** qv / PC, f)
        FAM[f"(lambda_C^2 c/H_L)^(1/3), m = {m:.1e}, {f}"] = ((lamC ** 2 * c / H_L) ** (1 / 3) / PC, f)
        for v in V_KICK:
            for fac_n, fac in (("hbar", 1.0), ("h", 2 * math.pi)):
                FAM[f"{fac_n}/(m v_k {v / 1e3:.0f}), m = {m:.1e}, {f}"] = (fac * hbar_over_m(m) / v / PC, f)
inside = {k_: (XI_FLOOR[f] <= v_ <= XI_CEIL) for k_, (v_, f) in FAM.items()}
vals = np.array([v_ for v_, _ in FAM.values()])
span_dec = math.log10(vals.max() / vals.min())
win_dec = math.log10(XI_CEIL / XI_FLOOR["canonical"])
p1 = win_dec / span_dec
N_ind = 7 + 1 + 4                                                   # distinct constructions per (m, footing): 7 exponents, 1 Lambda-mixed, 4 de Broglie
p_any = 1 - (1 - p1) ** N_ind
n_in = sum(inside.values())
P(f"    the family: {len(FAM)} members over {span_dec:.1f} decades; xi's window is {win_dec:.2f} decades; members inside: {n_in}; "
  f"p(one) = {p1:.2f}; p(>= 1 of {N_ind} constructions) = {p_any:.2f}")
P("    inside: " + "; ".join(k_ for k_, v_ in inside.items() if v_ and "canonical" in k_))
check("H6 xi look-elsewhere: of the lengths built from (hbar/m, a0, c, H_Lambda, v_k) with simple exponents >= 2 land in xi's "
      "window, and the chance that >= 1 lands is >= 50%: every landing is numerology",
      f"{n_in} of {len(FAM)} inside; p(one) {p1:.2f}; p(>= 1) {p_any:.2f}", n_in >= 2 and p_any >= 0.5, load_bearing=False)
OUT["numbers"]["R2_lookelsewhere"] = dict(n_members=len(FAM), n_inside=n_in, span_decades=span_dec, window_decades=win_dec,
                                          p_one=p1, p_any=p_any)
add_map("xi", BEFORE["xi"], "KNOB", "FP17 (threshold-mass theorem, B1-B4), FP7 A4, XR22; this lane R2",
        dict(floor_pc=XI_FLOOR, ceiling_pc=XI_CEIL, compton_factor_below=comp_factor, h_over_mvk_pc=[min(v_['xi'] for v_ in dbh), max(v_['xi'] for v_ in dbh)],
             p_any=p_any),
        "no own finding fixes it; every m-tie is numerology (no action couples the filter to the dark field) or fails the floor; "
        "measurable by Gaia DR4 with a separation-resolved statistic (XR22)")
add_map("m", BEFORE["m"], "FITTED", "FP15 M1 (forest vs flagship at the floor), L383, FL1; R2/R13 here",
        dict(floor_eV=M_FLOOR), "pinned near its floor on the canonical footing, bounded on alt; not tied to xi; GDM does not pin it (R13)")

# ---------------------------------------------------------------------------------------------------------------- R3 eps
banner("R3  eps (the splitting; the kick speed v_k)")
v_q = {(f, m): (hbar_over_m(m) * A0[f]) ** (1 / 3) for f in FEET for m in M_FLOOR}
ratio_q = min(V_KICK) / max(v_q.values())
eps_m2 = {v: v ** 2 / (2 * c ** 2 - v ** 2) for v in V_KICK}
k19 = KAPPA ** 19
p_k19 = math.log(eps_m2[V_KICK[1]] / eps_m2[V_KICK[0]]) / math.log(2.0)
p_k9 = math.log(V_KICK[1] / V_KICK[0]) / math.log(2.0)
v_k9 = c * KAPPA ** 9
dev_e3 = rel(p_k19, FP15["numbers"]["E3"]["p_chance"]["kappa"])
M_k = {f: {v: v ** 4 / (G * A0[f]) / MSUN for v in V_KICK} for f in FEET}
fp16_empty = bool(re.search(r"\|\s*FP16\s*\|\s*L16l\s*\|\s*FAILS\s*\|.*EMPTY", STATUS_CHAIN))
P(f"    (hbar a0/m)^(1/3) = {min(v_q.values()) / 1e3:.2f}-{max(v_q.values()) / 1e3:.2f} km/s: {ratio_q:.0f}x below v_k")
P(f"    eps/m^2 = v^2/(2c^2 - v^2) = {eps_m2[V_KICK[0]]:.3e}-{eps_m2[V_KICK[1]]:.3e}; kappa^19 = {k19:.4e} inside (v = c kappa^9 = "
  f"{v_k9 / 1e3:.1f} km/s); chance for kappa powers {p_k19:.2f} (FP15 E3: {FP15['numbers']['E3']['p_chance']['kappa']:.2f}); "
  f"in v alone {p_k9:.2f}")
P(f"    (G M a0)^(1/4) = v_k at M = " + "; ".join(f"{f}: {M_k[f][V_KICK[0]]:.2e}-{M_k[f][V_KICK[1]]:.2e} Msun" for f in FEET)
  + " -- a selection mass (FP4 L10l), not a constant of the theory")
P(f"    the construction's window with re-accretion: EMPTY (FP16 L16l): {fp16_empty}")
check("H15 eps: no own finding fixes it -- (hbar a0/m)^(1/3) << v_k (>= 50x); c kappa^9 = 585.5 km/s lands in [575, 650] with "
      "chance >= 15% (numerology, FP15 E3); the construction's window is empty (FP16)",
      f"ratio {ratio_q:.0f}; c kappa^9 = {v_k9 / 1e3:.1f} km/s, chance {p_k9:.2f} (v) / {p_k19:.2f} (eps/m^2; FP15 E3 dev {dev_e3:.1e}); "
      f"FP16 empty {fp16_empty}", ratio_q >= 50 and 575e3 <= v_k9 <= 650e3 and p_k9 >= 0.15 and fp16_empty, load_bearing=False)
add_map("eps (v_k)", BEFORE["eps"], "FITTED", "FP15 E1-E4, FP4 L10l, FP16; this lane R3",
        dict(eps_over_m2=[eps_m2[V_KICK[0]], eps_m2[V_KICK[1]]], v_hbar_a0_m_kms=[min(v_q.values()) / 1e3, max(v_q.values()) / 1e3],
             kappa19_chance=p_k19),
        "irreducible (the only Z4-odd term) and fitted; kappa^19 is numerology; the construction it belongs to has an empty window (FP16)")

# ---------------------------------------------------------------------------------------------------------------- R4 the turnaround gate
banner("R4  delta_t0 (zeta) and q: can a turnaround gate replace them?")
ZTA = (0.0, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0)
TA = {}
for z in ZTA:
    om = math.exp(omega_at_zta(z))
    a_ta, one_d = turnaround(om)
    TA[z] = dict(omega=om, one_plus_delta=one_d, a_check=a_ta)


def g_run(z, q=1.75):                                        # R(z)/R(0) for FK1's running at fixed zeta: E^(2q + 1/2)/(1 + z)^3
    return E_of(z) ** (2 * q + 0.5) / (1 + z) ** 3


need_ratio = g_run(2.5) / g_run(0.0)
R_band_lo = {z: BAND["canonical"][0] * g_run(z) for z in ZTA}
f_min = 4 * OM_L * OM_M                                      # min over z of E^4/(1+z)^3 (at (1+z)^3 = Omega_L/Omega_m)
web_line = 11.0 / f_min                                      # delta_t0 needed so that 1 + delta = 11 filaments stay below (FP15 T3)
XR12_PLAIN = (1.42 * DT0, BAND["canonical"][1])              # XR12's plain-reading forest bound zeta >= 1.42 (XR19's 7.54)
XR12_SIGMA = 2.77 * DT0                                      # XR12's sqrt(sigma)-modulated forest bound
P("    z_ta   omega      1 + delta_ta   R_band_lo(z) (q = 7/4, FP15 floor)   ratio")
for z in ZTA:
    P(f"    {z:4.1f}  {TA[z]['omega']:.5f}   {TA[z]['one_plus_delta']:8.3f}        {R_band_lo[z]:8.2f}                          "
      f"{TA[z]['one_plus_delta'] / R_band_lo[z]:.3f}")
rta0, rta25 = TA[0.0]["one_plus_delta"], TA[2.5]["one_plus_delta"]
q_ta = (math.log(rta25 / rta0 * (3.5 ** 3)) / math.log(E_of(2.5)) - 0.5) / 2          # the q whose running matches the turnaround's
web_min_full = min(TA[z]["one_plus_delta"] for z in ZTA if z <= 2.0)
P(f"    running: R_ta(2.5)/R_ta(0) = {rta25 / rta0:.3f} vs the {need_ratio:.3f} FK1's q = 7/4 gives; the turnaround's own effective q = {q_ta:.2f} "
  f"(FP15 T3b's window: canonical [1.75] on its grid, alt [1.5, 1.75])")
P(f"    TA-full (R = 1 + delta_ta(z) at every z): forest anchor z = 2.5: {rta25:.2f} vs >= {R_band_lo[2.5]:.1f}; web: min over z <= 2 "
  f"{web_min_full:.2f} vs 11")
P(f"    TA-z0 (delta_t0 = 1 + delta_ta(0) = {rta0:.3f}, FK1's q = 7/4 kept): FP15 floor band [{BAND['canonical'][0]:.2f}, "
  f"{BAND['canonical'][1]:.2f}] (alt top {BAND['alt'][1]:.2f}); web line delta_t0 >= {web_line:.2f} (R_min = {f_min * rta0:.2f} vs 11); "
  f"XR12 plain [{XR12_PLAIN[0]:.2f}, {XR12_PLAIN[1]:.2f}]; XR12 sqrt(sigma) floor {XR12_SIGMA:.2f}")
P(f"    the virialised contrast for collapse today: Delta_vir = {dv0:.1f} (x mean matter) -- far above the flagship cap {BAND['canonical'][1]:.1f}"
  f" / {BAND['alt'][1]:.1f}")
l15r = bool(re.search(r"the forest proxy's ~2x systematic", STATUS_CHAIN))
P(f"    TA-z0 is the one near miss: {abs(rta0 / BAND['canonical'][0] - 1) * 100:.1f}% below the floor-mass band's lower edge, which rests on XR12's "
  f"calibrated forest proxy (its ~2x systematic is OPEN in FP15 L15r: {l15r}); it is inside XR12's plain-reading band.  It is still not a "
  "tie: it keeps FK1's declared q = 7/4 running, which the turnaround contrast does not have (its own running is q_ta above), so the "
  "match holds at one epoch only")
h8a = rta25 <= R_band_lo[2.5] / 5
h8b = 10 <= rta0 <= 12.5 and rta0 < BAND["canonical"][0] and rta0 < web_line and XR12_PLAIN[0] <= rta0 <= XR12_PLAIN[1]
h8c = rta25 / rta0 < 1 and need_ratio > 4
check("H8a the full turnaround trigger R(z) = 1 + delta_ta(z) sits >= 5x below the forest/flagship band at z = 2.5: FAILS; "
      "delta_t0 and q are not removed",
      f"R_ta(2.5) = {rta25:.2f} vs band >= {R_band_lo[2.5]:.1f} (x{R_band_lo[2.5] / rta25:.1f}); web min {web_min_full:.2f} < 11", h8a,
      load_bearing=False)
check("H8b the LCDM turnaround contrast today lies in [10, 12.5]: below FP15's floor-mass band and the web line, inside XR12's "
      "plain band -- as a tie of zeta alone it FAILS narrowly on the floor-mass reading",
      f"1 + delta_ta(0) = {rta0:.3f}; floor band {BAND['canonical'][0]:.2f}-{BAND['canonical'][1]:.2f} ({(rta0 / BAND['canonical'][0] - 1) * 100:+.1f}% "
      f"at the lower edge); web line {web_line:.2f} ({(rta0 / web_line - 1) * 100:+.1f}%); XR12 plain {XR12_PLAIN[0]:.2f}-{XR12_PLAIN[1]:.2f}",
      h8b, load_bearing=False)
check("H8c the turnaround contrast runs the wrong way for q: R_ta(2.5)/R_ta(0) < 1 against the ~4.7 the gates need",
      f"{rta25 / rta0:.3f} vs {need_ratio:.3f}; effective q_ta = {q_ta:.2f}", h8c, load_bearing=False)
OUT["numbers"]["R4"] = dict(turnaround={str(z): v_ for z, v_ in TA.items()}, R_band_lo={str(z): v_ for z, v_ in R_band_lo.items()},
                            need_ratio=need_ratio, q_ta=q_ta, web_line_delta_t0=web_line, f_min=f_min, xr12_plain=XR12_PLAIN,
                            xr12_sqrt_sigma=XR12_SIGMA, delta_vir_z0=dv0)
add_map("zeta (delta_t0)", BEFORE["zeta"], "FITTED", "FP15 M1/T3b/T6d, XR12, XR19; this lane R4 (LCDM turnaround)",
        dict(one_plus_delta_ta_z0=rta0, band=BAND["canonical"], web_line=web_line),
        f"the LCDM turnaround contrast today ({rta0:.2f}) lands {abs(rta0 / BAND['canonical'][0] - 1) * 100:.0f}% below the floor-mass band: "
        "not a tie; the full turnaround gate fails the forest by ~10x")

# ---------------------------------------------------------------------------------------------------------------- R5 q
banner("R5  q (the trigger's running): a tie to the separator's n?")
qwin = FP15["numbers"]["T3b"]["window"]
Q_GRID = sorted(float(q_) for q_ in FP15["numbers"]["T3b"]["scan"])
ids = {k: k * 2 / 2 - 0.25 for k in (1, 2, 3)}                      # n_t ~ L^-k with L ~ Omega_L^(n/2), n = 2: q + 1/4 = k n/2
hit = {k: v_ for k, v_ in ids.items() if v_ in qwin["canonical_fil"]}


def win_width(allowed):
    lo_ = max([q_ for q_ in Q_GRID if q_ < min(allowed)], default=min(allowed))
    hi_ = min([q_ for q_ in Q_GRID if q_ > max(allowed)], default=max(allowed))
    return hi_ - lo_


w_can, w_alt = win_width(qwin["canonical_fil"]), win_width(qwin["alt_fil"])
p_q = {"canonical": min(1.0, w_can / 1.0), "alt": min(1.0, w_alt / 1.0)}
P(f"    identifications n_t ~ L^-k (k = 1, 2, 3; H_K1: L ~ Omega_L^(n/2), n = 2) give q = {list(ids.values())}; the data-pinned window "
  f"(FP15 T3b, forest x A4 x filaments): canonical {qwin['canonical_fil']} (open interval width <= {w_can}), alt {qwin['alt_fil']} "
  f"(<= {w_alt}); hits: {hit}; chance for a unit-spaced family: {p_q['canonical']:.2f} / {p_q['alt']:.2f}")
P("    FP15 T1: the action does not fix the exponent (three inequivalent identifications with H_Y's p' failed the web); nothing selects k = 2; "
  "the normalisation of n_t ~ L^-2 has no own scale (FP15 T1b: a0/(4 pi G L) runs as q = 3/4)")
check("H14 q = n - 1/4 (n_t ~ L^-2, H_K1's n = 2) reproduces the data-pinned q = 7/4 exactly, but the identifications "
      "n_t ~ L^-k hit the q-window with chance >= 30% and no action term selects k: numerology, not counted",
      f"q(k = 2) = {ids[2]}; in window {2 in hit}; chance {p_q['canonical']:.2f} (canonical) / {p_q['alt']:.2f} (alt)",
      2 in hit and min(p_q.values()) >= 0.3, load_bearing=False)
add_map("q", BEFORE["q"], "FITTED", "FP15 T1/T3b; this lane R4 (turnaround running) and R5 (n - 1/4)",
        dict(window=qwin, q_turnaround=q_ta, q_tie=ids[2], chance=p_q),
        "pinned by the forest and the web at 7/4 (canonical); the turnaround gate runs the wrong way; q = n - 1/4 is a post-hoc hit")

# ---------------------------------------------------------------------------------------------------------------- R6 lambda
banner("R6  lambda (the MOND scalar's inertia): pinned to its inert range?")
lam_hi = L4["inert_below"]
cs_lo, cs_hi = L4["cs_track"]["0.0"], L4["cs_track"][str(lam_hi)]
al_lo, al_hi = L4["alpha2_v2"]["0.0"], L4["alpha2_v2"][str(lam_hi)]
s8_spread = float(re.search(r"sigma_8 spread over lambda ([0-9.e+-]+)", XR25["checks"][[k_ for k_ in XR25["checks"] if k_.startswith("L1")][0]]["measured"]).group(1))
l5 = XR25["numbers"]["L5"]["rows"]
ell_worst = max(max(r_["ell_unfiltered"], r_["ell_subxi"]) for r_ in l5)
TRACK_GATE = 1800.0                                            # km/s: 3 x 600 where C^Q <= 100 (FP2 L8c)
xr18b_c = XR18B["checks"]
m_r5 = re.search(r"spread \(lambda <= 0\.03\) ([0-9.e+-]+); spread \(0\.\.274\.4\) ([0-9.e+-]+)", xr18b_c["R5"]["measured"])
m_r6 = re.search(r"1% at lambda = ([0-9.]+) \(tracking\) / ([0-9.]+) \(alpha_2 v\^2\)", xr18b_c["R6"]["measured"])
s8_k1 = float(m_r5.group(1))                                   # XR18b R5: H_K1 at c_2 = infinity, lambda <= 0.03
lam1_track, lam1_alpha = float(m_r6.group(1)), float(m_r6.group(2))
chg = {"tracking speed": abs(cs_hi / cs_lo - 1), "alpha_2 v^2": abs(al_hi / al_lo - 1), "sigma_8 (H_S, XR25 L1)": s8_spread,
       "sigma_8 (H_K1, XR18b R5)": s8_k1}
lam_gates = dict(tracking=min(cs_lo, cs_hi) / TRACK_GATE, strong_coupling_m=ell_worst, changes=chg,
                 bbn="XR26 F1: Omega_phi,0 < 1.7e-25 is a bound on initial data (phidot_0 < 7e-13 H0/sqrt(lambda)); met by phidot = 0 at any lambda > 0",
                 c2_condition="needs c_2 -> infinity (FP14); at FP2's c_2 floor the lambda window is empty (XR25 L2)")
lam_ok = max(chg.values()) <= 0.015 and lam_gates["tracking"] >= 5 and ell_worst <= 0.02
for k_, v_ in chg.items():
    P(f"    over lambda in (0, {lam_hi}]: {k_:40s} moves by {v_:.2e} (fraction)")
P(f"    tracking {cs_hi:.0f}-{cs_lo:.0f} km/s vs the moving-source gate {TRACK_GATE:.0f} (margin x{lam_gates['tracking']:.1f}); worst ell_sc "
  f"{ell_worst * 100:.2f} cm (lambda = 1e-9, sub-xi); {lam_gates['bbn']}; {lam_gates['c2_condition']}")
P(f"    cross-check with XR18b (3c0cf3c37, committed while this lane ran): 1% drift at lambda = {lam1_track} (tracking) / {lam1_alpha} "
  f"(alpha_2 v^2); sigma_8 spread {s8_k1:.1e} for lambda <= 0.03 under H_K1 -- the record now DECLARES lambda <= 0.03 a regulator "
  f"(ledger now: {NOW.get('lambda')}); this lane reproduces that verdict from XR25's committed numbers")
check("H7 lambda: over (0, 0.03] every scored observable moves by <= 1.5%, the tracking gate holds with margin >= 5, strong "
      "coupling stays at ell_sc <= 2 cm: KNOB -> REGULATOR (a declared range, not a derivation)",
      "; ".join(f"{k_} {v_ * 100:.4f}%" for k_, v_ in chg.items()) + f"; margin x{lam_gates['tracking']:.1f}; ell_sc {ell_worst * 100:.2f} cm; "
      f"XR18b: 1% at {lam1_track}/{lam1_alpha}", lam_ok, load_bearing=False)
VERIFIED = {}                                                   # moves the record made during this lane, re-checked here
VERIFIED["lambda"] = dict(new_status="REGULATOR", gates_pass=lam_ok and NOW.get("lambda") == "REGULATOR", gates=lam_gates,
                          by="XR18b (3c0cf3c37), re-verified by CFG0 R6 from XR25's committed numbers")
add_map("lambda", BEFORE["lambda"], NOW.get("lambda", "?"), "XR25 L1-L5, XR18b R4-R6 (the record's move), FP13 R13m, FP19 R19j, XR26 F1; this lane R6",
        dict(range=[0, lam_hi], **{k_: v_ for k_, v_ in chg.items()}, tracking_margin=lam_gates["tracking"], ell_sc_m=ell_worst),
        "a REGULATOR in the declared range (0, 0.03] -- made so by the record's XR18b while this lane ran; verified here: required > 0, "
        "its value moves no scored observable by more than ~1%, with c_2 -> infinity")

# ---------------------------------------------------------------------------------------------------------------- R7 alpha_c, c_2
banner("R7  alpha_c and c_2 (already reduced in the record)")
P("    alpha_c: REGULATOR in [alpha_sc, 3.2e-9] (FP14 F14f; XR25: [8.2e-16, 3.2e-9]); every observable moves <= 1.6e-9; alpha_c > 0 load-bearing")
P("    c_2: ELIMINATED (c_2 -> infinity, a multiplier; FP14 F14h) on Minkowski and FRW; at black-hole universal horizons the limit is "
  "singular at O(alpha_c) (XR25): OPEN")
add_map("alpha_c", BEFORE["alpha_c"], "REGULATOR", "FP14 F14d-F14f, FP2 L6f, XR25", dict(window=[8.2e-16, 3.2e-9]), "unchanged")
add_map("c_2", BEFORE["c_2"], "ELIMINATED", "FP14 F14h-F14k, XR25", {}, "unchanged; OPEN at black-hole universal horizons (XR25)")

# ---------------------------------------------------------------------------------------------------------------- R8 separator
banner("R8  the separator: L_Lambda (and n, the ramp, c_y)")
# (a) the grammar of own lengths against the window
BASES = {}
for f in FEET:
    BASES[f"a0/H_L^2 ({f})"] = aL[f]
BASES["c/H_Lambda (R_dS)"] = c / H_L / MPC
BASES["c/H_0"] = c / H0 / MPC
for v in V_KICK:
    BASES[f"v_k/H_0 ({v / 1e3:.0f})"] = v / H0 / MPC
    BASES[f"v_k/H_Lambda ({v / 1e3:.0f})"] = v / H_L / MPC
    BASES[f"FP16 reach 0.72-0.79 v_k/H_0 ({v / 1e3:.0f})"] = 0.755 * v / H0 / MPC
    BASES[f"Lambda-edge 0.555 v_k/H_Lambda ({v / 1e3:.0f})"] = 0.555 * v / H_L / MPC
for f in FEET:
    BASES[f"sqrt(xi_floor R_dS) ({f})"] = math.sqrt(XI_FLOOR[f] * PC * c / H_L) / MPC
FACT = {"1": 1.0, "2": 2.0, "1/2": 0.5, "pi": math.pi, "1/pi": 1 / math.pi, "2pi": 2 * math.pi, "1/(2pi)": 1 / (2 * math.pi), "3": 3.0, "1/3": 1 / 3}
GRAM = {}
for bn, bv in BASES.items():
    for fn, fv in FACT.items():
        GRAM[f"{fn} x {bn}"] = bv * fv
    for k in range(1, 21):
        GRAM[f"kappa^{k} x {bn}"] = bv * KAPPA ** k
    for k in range(1, 9):
        GRAM[f"Z^-{k} x {bn}"] = bv * Z_FW ** (-k)
WIN_NOW = FP20B["numbers"]["R3_FP19"]["B1_window"]["after"]         # FP20b: [2.8, 4.6] Mpc with the exact KiDS projector
LO_N, HI_N = WIN_NOW
hits_w = {k_: v_ for k_, v_ in GRAM.items() if LO_W <= v_ <= HI_W}
hits_t = {k_: v_ for k_, v_ in GRAM.items() if LO_W <= v_ <= HI_T}           # the window declared in H10 (FP19's committed B1)
hits_tn = {k_: v_ for k_, v_ in GRAM.items() if LO_N <= v_ <= HI_T}          # the record's current sigma_8-tight window [2.8, 3.0]
hits_wn = {k_: v_ for k_, v_ in GRAM.items() if LO_N <= v_ <= HI_N}
pow_t = [k_ for k_ in hits_t if k_.startswith(("kappa^", "Z^-")) and ("a0/H_L^2" in k_ or "c/H_Lambda" in k_)]
pow_wn = [k_ for k_ in hits_wn if k_.startswith(("kappa^", "Z^-")) and ("a0/H_L^2" in k_ or "c/H_Lambda" in k_)]
rng = np.random.default_rng(20260927)
gv = np.log10(np.array(list(GRAM.values())))
width_t = math.log10(HI_T / LO_W)
trials = rng.uniform(0.0, 1.0, 20000)                              # window lower edge placed log-uniformly over 1-10 Mpc
p_t = float(np.mean([np.any((gv >= t_) & (gv <= t_ + width_t)) for t_ in trials]))
width_w = math.log10(HI_W / LO_W)
p_w = float(np.mean([np.any((gv >= t_) & (gv <= t_ + width_w)) for t_ in trials]))
width_tn = math.log10(HI_T / LO_N)
p_tn = float(np.mean([np.any((gv >= t_) & (gv <= t_ + width_tn)) for t_ in trials]))
P(f"    grammar: {len(BASES)} own lengths x ({len(FACT)} simple factors + kappa^1..20 + Z^-1..8) = {len(GRAM)} members")
P(f"    hits in the wide window [2.65, 4.6] Mpc: {len(hits_w)}; in the sigma_8-tight window [2.65, 3.0]: {len(hits_t)} -> "
  + "; ".join(f"{k_} = {v_:.3f}" for k_, v_ in sorted(hits_t.items(), key=lambda kv: kv[1])[:12]))
P(f"    chance that some member lands in a window of the same width placed at random over 1-10 Mpc: tight {p_t:.2f}, wide {p_w:.2f}")
P(f"    the record's CURRENT window (FP20b, exact projector): [{LO_N}, {HI_N}] Mpc, sigma_8-tight [{LO_N}, {HI_T}]: hits {len(hits_wn)} / "
  f"{len(hits_tn)} ({'; '.join(f'{k_} = {v_:.3f}' for k_, v_ in sorted(hits_tn.items(), key=lambda kv: kv[1]))}); pure powers in the "
  f"current wide window: {pow_wn}; chance for the tight width {p_tn:.2f}")
P("    no hit carries a mechanism: the separator's length is not produced by any term of the chain's action (FP19 R19f: zero modes give "
  "only c/H (a0/cH)^p; FP13 R13h: the dark field's scales are sub-kpc)")
check("H10 L_Lambda: FP19 B1 reproduces; in the sigma_8-tight window no power of kappa or Z times a0/H_L^2 or c/H_L lands; the "
      "extended grammar of own lengths lands with chance >= 30%: numerology",
      f"B1 control {c8_ok}; tight-window power hits {pow_t}; grammar hits {len(hits_t)} (tight) / {len(hits_w)} (wide); chance {p_t:.2f} / {p_w:.2f}",
      c8_ok and not pow_t and p_t >= 0.3, load_bearing=False)
# (b) the turnaround separator as a response gate, against h72's bounds
R0_UP = {}
for f in FEET:
    R0_UP[f] = {}
    for b, Mb in MB_BIN.items():
        refs = {g: R0_ROWS[g][f] * (Mb / MB_ROWS[g]) ** SLOPE_R0 for g in MB_ROWS}
        refs["LG"] = R0_ROWS["LG (FP11, timing mass)"][f] * (Mb / MB_LG[f]) ** SLOPE_R0
        R0_UP[f][b] = max(refs.values())
fail_bins = {f: [b for b in MB_BIN if R0_UP[f][b] < H72[f][b - 1]] for f in FEET}
for f in FEET:
    P(f"    {f:9s} chain R0 (z = 0, upper bound on the turned-around region) at the KiDS bins: "
      + ", ".join(f"bin {b} {R0_UP[f][b]:.2f} Mpc vs r_end > {H72[f][b - 1]:.2f} (x{H72[f][b - 1] / R0_UP[f][b]:.2f})" for b in MB_BIN))
P("    a response gate truncates the phantom at the turned-around radius (outside it the field is Newtonian from the baryons, "
  "Gauss); the KiDS lenses sit at z ~ 0.1-0.5 (the chain scores z = 0.25 and 0.4), where the turned-around region was smaller still; the effective band-pass L ~ R/2 "
  f"({min(R0_UP['canonical'].values()) / 2:.2f}-{max(R0_UP['canonical'].values()) / 2:.2f} Mpc) is the LG's corner of the pincer "
  "(FP20: L(0.25) = 0.56 Mpc costs KiDS +254/+260; the KiDS floor is 1.23/1.24 Mpc)")
h9 = all(len(fail_bins[f]) == 4 for f in FEET)
check("H9 the turnaround separator as a response gate: the chain's own zero-velocity radius at the four KiDS bins' baryonic "
      "masses lies below h72's 3-sigma lower bound on where the boost ends, in every bin and on both footings: FAILS KiDS",
      f"failing bins canonical {fail_bins['canonical']}, alt {fail_bins['alt']}; shortfall x" +
      f"{min(H72['canonical'][b - 1] / R0_UP['canonical'][b] for b in MB_BIN):.2f}-{max(H72['canonical'][b - 1] / R0_UP['canonical'][b] for b in MB_BIN):.2f}",
      h9, load_bearing=False)
OUT["numbers"]["R8"] = dict(grammar_size=len(GRAM), hits_tight=hits_t, hits_wide_count=len(hits_w), p_tight=p_t, p_wide=p_w,
                            window_now=WIN_NOW, hits_tight_now=hits_tn, hits_wide_now_count=len(hits_wn), p_tight_now=p_tn,
                            R0_upper_Mpc=R0_UP, h72=H72, failing_bins=fail_bins)
add_map("L_Lambda", BEFORE["L_Lambda"], "DECLARED", "FP19 B1/H6/R19f, FP20b (window 2.8-4.6), FP13 R13a/R13h, h72, FP12/FP11, FP20; this lane R8",
        dict(window_now=WIN_NOW, tight_now=[LO_N, HI_T], grammar_chance_tight=p_t, grammar_chance_tight_now=p_tn, turnaround_fail_bins=fail_bins),
        "no identity fixes it (hits are numerology); the turnaround response gate fails KiDS in every bin; the source-gate version is OPEN")
for k_, basis in (("n", "FP13 R13c (n_eff = 2.06 from the web's running, under H_S), FP19 R19k"), ("ramp", "FP13 C2, FP19 R19k"),
                  ("c_y", "FP19 R19g (the Hamiltonian constraint's normalisation; chosen after scoring)")):
    add_map(k_, BEFORE[k_], "NATURAL CHOICE", basis, {}, "unchanged: a natural choice, no continuous freedom; not derived")

# ---------------------------------------------------------------------------------------------------------------- R9 the dark amount
banner("R9  the dark amount: a framework relation between Omega_c, Omega_Lambda and kappa?")
OMC, SOMC = 0.1200 / (H0_KMS / 100) ** 2, 0.0012 / (H0_KMS / 100) ** 2          # Planck 2018 omega_c at the chain's h
rec_amount = bool(re.search(r"\|\s*FP15\s*\|\s*L15q\s*\|\s*POSTULATED\s*\|\s*the amount", STATUS_CHAIN))
AMT = {}
for a in range(0, 5):
    for b in range(-2, 3):
        for cc_ in range(-2, 3):
            for d in range(-2, 3):
                AMT[(a, b, cc_, d)] = KAPPA ** a * (8 * math.pi / 3) ** (b / 2) * math.pi ** cc_ * OM_L ** d
vals_a = np.array(list(AMT.values()))
distinct = np.unique(np.round(np.log10(vals_a), 12))
hit1 = {k_: v_ for k_, v_ in AMT.items() if abs(v_ - OMC) <= SOMC}
hit2 = {k_: v_ for k_, v_ in AMT.items() if abs(v_ - OMC) <= 2 * SOMC}
dens = np.sum(np.abs(distinct - math.log10(OMC)) <= 0.3) / 0.6                  # distinct members per decade near the target
exp1 = dens * 2 * math.log10(1 + SOMC / OMC)
k2_pull = (KAPPA ** 2 - OMC) / SOMC
P(f"    target Omega_c = {OMC:.4f} +- {SOMC:.4f} (Planck omega_c 0.1200 +- 0.0012 at h = {H0_KMS / 100})")
P(f"    the record: the amount is initial data (FP15 L15q POSTULATED: {rec_amount}); the ghost-condensate reading proves the mean is not set "
  "by thermal/fluctuation physics (the shift-charge theorem); no committed relation to kappa")
P(f"    grammar kappa^a (8 pi/3)^(b/2) pi^c Omega_L^d: {len(AMT)} members ({len(distinct)} distinct); within 1 sigma: {len(hit1)}, 2 sigma: "
  f"{len(hit2)}; expected by chance within 1 sigma: {exp1:.2f}; kappa^2 = 1/4 pulls {k2_pull:+.1f} sigma")
P("    1-sigma hits: " + "; ".join(f"kappa^{k_[0]} (8pi/3)^({k_[1]}/2) pi^{k_[2]} OmL^{k_[3]} = {v_:.4f}" for k_, v_ in list(hit1.items())[:6]))
check("H11 the dark amount: no committed relation ties Omega_c to (kappa, Omega_L); the grammar's 1-sigma hits are consistent "
      "with chance (>= 0.5 expected); kappa^2 fails by >= 3 sigma: initial data stays",
      f"record relation none (L15q {rec_amount}); hits {len(hit1)} vs expected {exp1:.2f}; kappa^2 {k2_pull:+.1f} sigma",
      rec_amount and exp1 >= 0.5 and abs(k2_pull) >= 3, load_bearing=False)
OUT["numbers"]["R9"] = dict(Omega_c=OMC, sigma=SOMC, n_members=len(AMT), n_distinct=len(distinct), hits_1sigma=len(hit1),
                            hits_2sigma=len(hit2), expected_1sigma=exp1, kappa2_pull=k2_pull)
add_map("amount", BEFORE["amount"], "INITIAL DATA", "FP15 N1/N2/L15q; ghost-condensate amount theorem; this lane R9",
        dict(Omega_c=OMC, grammar_hits=len(hit1), expected=exp1), "as LCDM's omega_c; no framework relation; grammar hits are chance")

# ---------------------------------------------------------------------------------------------------------------- R10 misalignment
banner("R10  the misalignment")
th_cap = math.degrees(math.asin(math.sqrt(0.059)))
p_mis = 14.0 / 90.0
P(f"    the flagship's retained-carrier allowance S <= 0.059 (MS2/DE4, XR16) bounds the cold phi_L share: theta <= {th_cap:.2f} deg; "
  f"FK1 declares ~14 deg; FP15 N1's isotropic prior {FP15['numbers']['N1']['p_misalignment']:.4f} (= 14/90: {p_mis:.4f})")
add_map("misalignment", BEFORE["misalignment"], "INITIAL DATA", "FK1, FP15 N1, XR16", dict(theta_max_deg=th_cap, prior=p_mis),
        "bounded by the flagship (theta <~ 14 deg), not fixed; belongs to the construction whose window is empty (FP16)")

# ---------------------------------------------------------------------------------------------------------------- R11 kernel shape, density choice
banner("R11  the SN-Ia step and the environment null: do they fix the kernel's shape or a constant?")
sn_txt = text("real_research/reviews/mi_snia_power_curve_2026.py")
m_sn = re.search(r"partial ~ (-?[0-9.]+) against mass ~ (-?[0-9.]+)", sn_txt)
p_acc, p_mass = float(m_sn.group(1)), float(m_sn.group(2))
se_f = 1 / math.sqrt(449 - 3)
env_txt = text("real_research/reviews/A0_COSMICWEB_ENVIRONMENT_2026-06.md")
m_env = re.search(r"slope \*\*([−-]?[0-9.]+) ± ([0-9.]+)\*\*.*?\*\*([0-9.]+)σ from \+0\.5\*\*", env_txt)       # 5c, 2M++ real space
m_2mrs = re.search(r"= \*\*\+?([−-]?[0-9.]+) ± ([0-9.]+)\*\* — [0-9.]+σ from 0, \*\*([0-9.]+)σ from \+0\.5\*\*", env_txt)  # 5a, 2MRS
_f = lambda s_: float(s_.replace("−", "-"))
s_env, e_env, sig_rec = _f(m_env.group(1)), float(m_env.group(2)), float(m_env.group(3))
s_2m, e_2m, sig_2m_rec = _f(m_2mrs.group(1)), float(m_2mrs.group(2)), float(m_2mrs.group(3))
sig_env = (0.5 - s_env) / e_env
sig_2m = (0.5 - s_2m) / e_2m
m_mds = re.search(r"3σ minimum detectable slope is \*\*~([0-9.]+)\*\*", env_txt)
P(f"    SN-Ia (recorded; no committed output): partial correlation with acceleration at fixed mass {p_acc:+.2f} vs with mass at fixed "
  f"acceleration {p_mass:+.2f}; Fisher SE at N = 449 {se_f:.3f}: the acceleration adds {abs(p_acc) / se_f:.1f} SE -- the step is a mass/age "
  "effect; its location at Sigma_a0 = a0/(2 pi G) stays a coincidence (the null is itself underpowered, ~18%)")
P(f"    environment (recorded): 2MRS slope {s_2m:+.3f} +- {e_2m:.3f} -> {sig_2m:.2f} sigma from the rho_local fork (+0.5; the writeup quotes "
  f"{sig_2m_rec}); 2M++ real-space {s_env:+.3f} +- {e_env:.3f} -> {sig_env:.2f} sigma (writeup {sig_rec}); minimum detectable slope ~{m_mds.group(1)}: rho_local excluded, rho_Lambda kept; the test compares a0 "
  "across environments at fixed kernel -- blind to the kernel's shape")
h13 = abs(p_acc) < 2 * se_f and abs(p_mass) > 3 * se_f and sig_env > 5
check("H13 the SN-Ia step and the environment null fix no constant and no kernel shape; the null selects rho_Lambda over "
      "rho_local for P1's density (L0b)",
      f"SN: acceleration partial {p_acc:+.2f} ({abs(p_acc) / se_f:.1f} SE) vs mass {p_mass:+.2f}; environment {sig_env:.1f} sigma against +0.5",
      h13, load_bearing=False)
add_map("P1's density (L0b, a choice)", "POSTULATED", "DATA-SELECTED vs rho_local", "the environment null (6 density axes); this lane R11",
        dict(slope_2Mpp=s_env, sigma_vs_local=sig_env), "rho_local excluded; rho_Lambda vs cosmic rho_m/rho_total is decided only by a0(z)")
add_map("kernel shape (nu_mono / P2)", "POSTULATED", "POSTULATED", "FP1 L4d, user decision 09-26; this lane R11",
        dict(sn_partial=p_acc), "not fixed by the SN-Ia step (no acceleration dependence) nor by the environment null (shape-blind)")

# ---------------------------------------------------------------------------------------------------------------- R12 GDM
banner("R12  the GDM theorem: does it fix the dark component's form or its mass?")
fl1_src = text("real_research/dark_fluid_2026/FL1_order_parameter.py")
W0_BOUND = 2e-14 if "w0 <= 2e-14" in fl1_src else float("nan")          # the record's CMB bound (mi_particle_vs_mode, quoted in FL1)
w_rec_bound = W0_BOUND * 1101 ** 3
cs_floor, w_floor, H_rec = fl1_row(M_FLOOR[0])
m_gdm = H_rec / math.sqrt(w_rec_bound)
P(f"    at the chain's floor (1.9e-19 eV): max c_s^2 {cs_floor:.2e}, w_rec {w_floor:.2e}; the record's CMB bound w0 <= {W0_BOUND:.0e} "
  f"(w = w0 a^-3) gives w_rec <= {w_rec_bound:.2e}, met for m >= {m_gdm:.1e} eV -- {math.log10(M_FLOOR[0] / m_gdm):.1f} decades below the floor")
P("    the GDM theorem fixes the FORM linear cosmology sees -- a cold fluid (w, c_s^2, c_vis^2) = (0, 0, 0) plus an amount -- and nothing "
  "else: m's floor comes from L383 (dwarf heating) and the forest's minihalos (FP15 M1), not from GDM")
h12 = cs_floor <= 1e-15 and w_floor <= 1e-19 and m_gdm <= 1e-25
check("H12 GDM: at the mass floor the field's GDM parameters are <= 1e-15 (c_s^2) and <= 1e-19 (w_rec); the record's own CMB "
      "bound is met for any m >= 1e-25 eV: GDM fixes the form, not m",
      f"c_s^2 {cs_floor:.2e}, w_rec {w_floor:.2e}; m_min(GDM) {m_gdm:.1e} eV", h12, load_bearing=False)
OUT["numbers"]["R12"] = dict(cs2_floor=cs_floor, w_rec_floor=w_floor, w0_bound=W0_BOUND, m_min_gdm_eV=m_gdm)

# ---------------------------------------------------------------------------------------------------------------- R13 the ties already in the record
banner("R13  ties already in the record (kept)")
P("    a0 <-> Lambda: TIED by the Henneaux-Teitelboim unimodular multiplier (XR20 T1; FP0 L2b); in the khronon's terms a0 = (kappa/sqrt(24 pi)) "
  "c^2 K_inf (XR30); kappa is its coupling, FITTED.  Not a new reduction, but the reason a0 is not counted as a constant.")
P("    the dark component's coupling: FK1 on the Einstein-frame metric g~ = g + (1 - e^-2chi) n n (FP22 L22d): no new field, no new constant")
add_map("a0 (the MOND scale)", "TIED", "TIED", "XR20 T1, FP0 L2b, XR30", dict(a0=A0), "tied to Lambda's integration constant; kappa its coupling")

# ---------------------------------------------------------------------------------------------------------------- MUTATE's adoption
if MUTATE:
    comp_tie = XIC[f"Compton hbar/(m c), m = {M_FLOOR[0]:.1e}"]
    Y_ADOPT["xi -> TIED to hbar/(m_floor c) (MUTATE)"] = dict(constant="xi", new_status="TIED",
                                                              gates_pass=all(comp_tie["gates"][f]["pass"] for f in FEET),
                                                              gates=comp_tie["gates"])
    for r_ in MAP:
        if r_["constant"] == "xi":
            r_["after"] = "TIED (MUTATE)"

# ================================================================================================================ N the count
banner("N  THE COUNT: fitted / declared / tied / derived (plus regulators, eliminated, initial data)")
CLASS = {"FITTED": "fitted", "KNOB": "declared", "DECLARED": "declared", "NATURAL CHOICE": "declared (natural)", "TIED": "tied",
         "DERIVED": "derived", "REGULATOR": "regulator", "ELIMINATED": "eliminated", "INITIAL DATA": "initial data",
         "POSTULATED": "postulated form"}
CONSTS = ("kappa", "xi", "m", "eps", "zeta", "q", "lambda", "alpha_c", "c_2", "L_Lambda", "n", "ramp", "c_y", "amount", "misalignment")


def tally(status_of):
    t_ = {}
    for k_ in CONSTS:
        cl = CLASS[status_of[k_]]
        t_[cl] = t_.get(cl, 0) + 1
    t_["tied"] = t_.get("tied", 0) + 1                             # a0, tied to Lambda (XR20 T1): not a free constant
    return t_


before = {k_: BEFORE[k_] for k_ in CONSTS}                   # the ledger when this lane began (the task's list)
now = {k_: NOW[k_] for k_ in CONSTS}                         # the ledger at HEAD (read live)
after = dict(now)                                            # this lane's result: the record's ledger + this lane's own adoptions
for nm, ad in Y_ADOPT.items():
    after[ad["constant"]] = ad["new_status"]
t_before, t_now, t_after = tally(before), tally(now), tally(after)
for k_ in CONSTS:
    P(f"    {k_:14s} lane start {before[k_]:16s} ledger now {now[k_]:16s} CFG0 {after[k_]}")
fmt = lambda t_: " / ".join(f"{k_} {t_.get(k_, 0)}" for k_ in ("fitted", "declared", "declared (natural)", "tied", "derived", "regulator",
                                                                 "eliminated", "initial data"))
P(f"    LANE START: {fmt(t_before)}")
P(f"    LEDGER NOW: {fmt(t_now)}")
P(f"    CFG0:       {fmt(t_after)}")
moved_rec = [k_ for k_ in CONSTS if before[k_] != now[k_]]    # moves the record made while this lane ran
moved = [k_ for k_ in CONSTS if before[k_] != after[k_]]
P(f"    moved by the record during this lane: {moved_rec} (each re-verified here: "
  + ", ".join(f"{k_} {'pass' if VERIFIED.get(k_, {}).get('gates_pass') else 'NOT VERIFIED'}" for k_ in moved_rec) + ")")
P(f"    adopted by this lane itself: {list(Y_ADOPT) or 'none'}")
OUT["count"] = dict(lane_start=t_before, ledger_now=t_now, cfg0=t_after, status_lane_start=before, status_now=now, status_cfg0=after,
                    moved_by_record=moved_rec, adopted_by_cfg0=list(Y_ADOPT), verified={k_: dict(v_, gates=None) for k_, v_ in VERIFIED.items()})
CHANGES = {k_: dict(gates_pass=VERIFIED.get(k_, {}).get("gates_pass", False), by="record") for k_ in moved_rec}
for nm, ad in Y_ADOPT.items():
    CHANGES[ad["constant"]] = dict(gates_pass=ad["gates_pass"], by="CFG0: " + nm)
n1_ok = all(v_["gates_pass"] for v_ in CHANGES.values())
check("N1 EVERY CHANGE TO THE COUNT PASSES EVERY GATE IT TOUCHES (both footings): the record's moves during this lane are re-verified "
      "here, and every reduction this lane adopts must pass its own gates",
      "; ".join(f"{k_} ({v_['by']}): {'pass' if v_['gates_pass'] else 'FAIL'}" for k_, v_ in CHANGES.items()) or "no changes", n1_ok)
n2_ok = (sorted(moved) == sorted(CHANGES) and n1_ok and after["kappa"] == "FITTED" and t_after.get("derived", 0) == 0
         and sum(t_before.values()) == sum(t_after.values()) == sum(t_now.values()))
check("N2 THE COUNT'S BOOKKEEPING: the constants that change class are exactly the verified record moves plus this lane's adoptions, and "
      "the count credits only those that pass their gates; kappa stays FITTED; no constant is DERIVED; the total is conserved",
      f"moved {moved}; credited {sorted(CHANGES)}; kappa {after['kappa']}; derived {t_after.get('derived', 0)}; totals "
      f"{sum(t_before.values())} / {sum(t_now.values())} / {sum(t_after.values())}", n2_ok)
check("H16 the count: exactly one constant changes class (lambda: KNOB -> REGULATOR); kappa stays FITTED; nothing becomes DERIVED",
      f"moved {moved} (by the record's XR18b during this lane, re-verified here; this lane's own new adoptions: {list(Y_ADOPT) or 'none'})",
      moved == ["lambda"] and after["kappa"] == "FITTED" and t_after.get("derived", 0) == 0, load_bearing=False)

OUT["map"] = MAP
OUT["numbers"]["adopted"] = {nm: dict(constant=ad["constant"], new_status=ad["new_status"], gates_pass=ad["gates_pass"]) for nm, ad in Y_ADOPT.items()}
OUT["numbers"]["verified_record_moves"] = {k_: dict(new_status=v_["new_status"], gates_pass=v_["gates_pass"], by=v_["by"]) for k_, v_ in VERIFIED.items()}

# ================================================================================================================ ledger, verdict
LEDGER = [
    ("R1", "kappa", "FITTED", "no own finding fixes it; 0.465 +- 0.076 / 0.55 +- 0.17 consistent with 1/2; underivable (k01-k03)"),
    ("R2", "xi", "KNOB", "Compton tie fails x721; de Broglie at v_k fails the floor; h/(m v_k), galaxy-speed and xi_q ties are numerology"),
    ("R2", "m", "FITTED", "pinned near its floor (canonical); no tie to xi; GDM leaves it free above ~1e-26 eV"),
    ("R3", "eps", "FITTED", "irreducible; kappa^19 numerology; the construction's window is empty (FP16)"),
    ("R4", "zeta", "FITTED", f"the LCDM turnaround contrast today ({rta0:.2f}) lands just below the floor-mass band; the full turnaround gate fails x{R_band_lo[2.5] / rta25:.0f}"),
    ("R5", "q", "FITTED", f"turnaround runs the wrong way (q_ta = {q_ta:.2f}); q = n - 1/4 is a post-hoc hit (chance {p_q['canonical']:.2f})"),
    ("R6", "lambda", after["lambda"], "REGULATOR in the declared range (0, 0.03] -- the record's move (XR18b) during this lane, re-verified here: <= ~1% on every scored observable, c_2 -> infinity"),
    ("R7", "alpha_c / c_2", "REGULATOR / ELIMINATED", "unchanged (c_2: OPEN at black-hole universal horizons)"),
    ("R8", "L_Lambda", "DECLARED", f"identity hits are numerology (chance {p_t:.2f}); turnaround response gate fails KiDS in 4/4 bins"),
    ("R8", "n / ramp / c_y", "NATURAL CHOICE", "unchanged"),
    ("R9", "amount", "INITIAL DATA", "no framework relation; grammar hits consistent with chance"),
    ("R10", "misalignment", "INITIAL DATA", "bounded (<~ 14 deg), not fixed"),
    ("R11", "P1's density (L0b)", "DATA-SELECTED", "rho_local excluded by the environment null; the kernel shape stays postulated"),
    ("R12", "the dark component's form", "FIXED AS A FLUID", "GDM: cold (0, 0, 0) + amount; m not pinned"),
]
OUT["ledger"] = [dict(part=p_, constant=k_, status=s_, basis=b_) for p_, k_, s_, b_ in LEDGER]
banner("VERDICT")
for p_, k_, s_, b_ in LEDGER:
    P(f"  {p_:4s} {k_:28s} {s_:24s} {b_}")
n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
n_ok = sum(1 for _, ok, _ in CH if ok)
P(f"\n  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   ({time.time() - T_START:.1f} s)")
OUT["n_checks"], OUT["n_pass"], OUT["n_fail_load_bearing"] = len(CH), n_ok, n_lb_fail
OUT["runtime_s"] = time.time() - T_START
with open(OUT_JSON, "w") as f:
    json.dump(OUT, f, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else (float(o) if isinstance(o, np.floating) else str(o)))
rc = 1 if n_lb_fail else 0
P(f"rc = {rc}")
_FH.close()
sys.exit(rc)
