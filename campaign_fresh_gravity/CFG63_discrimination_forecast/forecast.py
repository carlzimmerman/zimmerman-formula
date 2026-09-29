#!/usr/bin/env python3
"""CFG63 -- discrimination forecast for the still-open tests.  See FROZEN_QUESTION.md (written before this script).

WHAT THIS IS.  Bookkeeping on committed numbers only.  For each open test it asks which measurement, at what N or
precision, separates candidate B from (i) the bare MOND-type law and (ii) LCDM, using ONLY the error budgets and
predictions already committed in this repo.  No new physics, no new constants, no tuning.  kappa = 1/2 stays FITTED.

SIGNIFICANCE MODEL (declared in FROZEN_QUESTION.md, item 1).  Two readings differ by Delta.  The measurement has a
statistical variance v1/N and a systematic floor f that does not shrink with N.
    S(N)    = Delta / sqrt(v1/N + f^2)
    N(k)    = v1 / ((Delta/k)^2 - f^2)          (infinite if f >= Delta/k)
    cap     = Delta / f                          (S at N -> infinity)
    f_need  = Delta / k                          (largest floor that still allows k sigma at N -> infinity)

CHECKS (pre-declared).
  C0  every cited (file, line) contains the cited text                                     [load-bearing]
  C1  the committed JSON values used here agree with the values typed in this script      [load-bearing]
  C2  the same algebra reproduces the committed separations (5.8/6.8 sigma_tot, 2.25/1.50 sigma at infinite N,
      12,200 / 45,000 pairs, 2.57 sigma, 1.4 / 15 / 13 objects, 3.77 / -0.41 / 1.26 / 2.46 sigma, 1.80 sigma,
      cost/S 0.59-0.98)                                                                     [load-bearing]
  H1  [HEADLINE; MUTATE must fail] With the committed floors, the tests whose cap is below 3 sigma between B and its
      competitor are exactly {a0(z) B-vs-H(z), a0(z) B-vs-LCDM-native, dwarfs law-vs-rule, groups B-vs-closure};
      the Gaia B-vs-Arm-A separation is above 3 sigma at its cap; Gaia B-vs-LCDM is identical (Delta = 0).

MUTATE=1 (argument `MUTATE`): every systematic floor is set to zero.  H1 and the C2 reproductions of capped numbers
must fail (exit 1).  Outputs are written to separate files (forecast_MUTATE.*).
Exit codes: 0 = all load-bearing checks pass (main run);  1 = at least one load-bearing check fails (expected for MUTATE).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = (len(sys.argv) > 1 and sys.argv[1] == "MUTATE") or os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
INF = float("inf")

LOG = []


def P(s=""):
    LOG.append(s)
    print(s)


def banner(t):
    P("")
    P("=" * 118)
    P(t)
    P("=" * 118)


CHECKS = []


def check(name, detail, ok, load_bearing=True):
    CHECKS.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


# ------------------------------------------------------------------------------------------------ citations
PRE = "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"
CFG = "campaign_fresh_gravity/"
CITES = {
    # Gaia DR4 wide binaries
    "G_SYS": (PRE, 617, "sigma_sys = 0.02"),
    "G_TOT": (PRE, 622, "sigma_tot = sqrt(sigma_fit^2 + 0.02^2)"),
    "G_N": (PRE, 629, "N = 30,000 assumed"),
    "G_SCALE": (PRE, 630, "sigma_fit scales as sqrt(30000/N)"),
    "G_SIGFIT": (PRE, 631, "sigma_fit ≈ 0.019, sigma_tot ≈ 0.028"),
    "G_SEP1": (PRE, 643, "3 sigma needs N ≳ 12,200"),
    "G_SEP2": (PRE, 644, "needs N ≈ 45,000"),
    "G_MOND": (PRE, 646, "MOND benchmark 1.33"),
    "G_CONTAM": (PRE, 658, "contamination biases HIGH"),
    "G_DR3": (PRE, 674, "10,624 pairs): gamma = 1.205 ± 0.035"),
    "G_ARM_A_C": (PRE, 947, "1.1614 ± 0.0175"),
    "G_ARM_A_ALT": (PRE, 948, "1.1917 ± 0.0175"),
    "G_ARM_A_TOPALT": (PRE, 948, "1.2267 ± 0.0200"),
    "G_ALT_GUARD": (PRE, 987, "43–49%"),
    "G_ARMB_CAP1": (PRE, 1267, "2.25σ"),
    "G_ARMB_CAP2": (PRE, 1268, "1.50σ alt at INFINITE N"),
    "G_ARMC_ROW": (PRE, 1335, "1.084 – 1.23"),
    "G_C_VS_A": (PRE, 1338, "5.8σ_tot / 6.8σ_tot above Arm C"),
    "G_CHAIN": (PRE, 1426, "1.0725"),
    "G_CHAIN_ROW": (PRE, 1473, "1.157 (≥ 1.174)"),
    "G_ARMC": (PRE, 1502, "Arm C: 1.000"),
    # a0(z)
    "Z_LCDM": (CFG + "CFG6_README.md", 160, "+0.334 [+0.210,+0.450]"),
    "Z_HZ": (CFG + "CFG6_a0z_evidence.py", 455, "HZ25 = 0.576"),
    "Z_A": (CFG + "CFG6_README.md", 149, "**0.000**"),
    "Z_DTHAW": (CFG + "CFG6_README.md", 158, "**+0.141 [+0.106,+0.181]**"),
    "Z_BAND": (CFG + "CFG6_README.md", 291, "the band is [−0.14, +0.04] dex"),
    "Z_SIG13": (CFG + "CFG6_README.md", 45, "0.13 dex per object the flat law is 2.57σ from ΛCDM-native"),
    "Z_SIGS": (CFG + "CFG6_README.md", 228, "(0.215 / 0.257 / 0.431 dex)"),
    "Z_SIG257": (CFG + "CFG6_a0z_evidence.py", 270, 'SIG_OBJ = {"PAPER7 requirement": 0.13}'),
    "Z_N_LCDM": (CFG + "CFG6_README.md", 251, "| A vs ΛCDM-native | **1.4** | 5.3 | 15 |"),
    "Z_N_BCPL": (CFG + "CFG6_README.md", 252, "| A vs B-CPL | 15 |"),
    "Z_N_THAW": (CFG + "CFG6_README.md", 254, "| A vs C-thaw(w₀) | 13 |"),
    "Z_FLOOR05": (CFG + "CFG6_README.md", 249, "with a 0.05 dex coherent floor"),
    "Z_CAP23": (CFG + "CFG52_a0z_feasibility/README.md", 28, "caps the significance near 2.3σ whatever N is"),
    "Z_GAP": (CFG + "CFG52_a0z_feasibility/README.md", 28, "0.23–0.27 dex in g_obs"),
    "Z_MASS": (CFG + "CFG52_a0z_feasibility/README.md", 28, "correlated** 0.2-dex mass-scale systematic"),
    "Z_NODATA52": (CFG + "CFG52_a0z_feasibility/README.md", 5, "cannot be run on the repo's data"),
    "Z_POOLED": (CFG + "CFG52_a0z_feasibility/README.md", 23, "N = 14"),
    "Z_NODATA54": (CFG + "CFG54_README.md", 11, "N = 0 of 51"),
    "Z_CAP54": (CFG + "CFG54_README.md", 22, "near 2.3σ"),
    # ultra-faint dwarfs
    "U_FLOOR": (CFG + "CFG28_README.md", 33, "0.077 dex"),
    "U_T4": (CFG + "CFG28_README.md", 37, "+0.432 ± 0.056"),
    "U_KM": (CFG + "CFG42_README.md", 29, "+0.325 (3.77σ) / +0.304 (3.55σ) | **−0.059 ± 0.143 (−0.41σ)**"),
    "U_MHFLOOR": (CFG + "CFG42_README.md", 36, "is 0.133 dex, and it is the collapse-mass floor"),
    "U_LCDMSPAN": (CFG + "CFG42_README.md", 41, "every collapse mass from 2 × 10⁸ to 10¹² passes the 2σ criterion"),
    "U_C46": (CFG + "CFG46_README.md", 22, "+0.206 ± 0.164"),
    "U_C46RULE": (CFG + "CFG46_README.md", 24, "−0.151 ± 0.129"),
    "U_C46SHIFT": (CFG + "CFG46_README.md", 30, "−0.104 dex"),
    "U_C46POWER": (CFG + "CFG46_README.md", 34, "The eight-system test has 1.0–1.3σ"),
    "U_C51BOO": (CFG + "CFG51_README.md", 13, "+0.219 ± 0.089 (2.46σ)"),
    "U_C51TUC": (CFG + "CFG51_README.md", 14, "+0.465 ± 0.128 (3.63σ)"),
    "U_C51COLD": (CFG + "CFG51_README.md", 21, "The cold component alone (2.4 km/s) would put Boötes I at +0.007 dex"),
    # X-ray groups
    "X_H1": (CFG + "CFG34_README.md", 33, "M_HSE/M_B = **1.41 → 1.80σ**"),
    "X_H2": (CFG + "CFG34_README.md", 34, "**1.88 → 2.57σ**"),
    "X_R500": (CFG + "CFG34_groups_and_the_ladder_under_b.out", 53, "+0.150 dex) +- 0.084 (groups 0.014, stars 0.023, HSE 0.079)"),
    "X_R2500": (CFG + "CFG34_groups_and_the_ladder_under_b.out", 54, "+0.275 dex) +- 0.107 (groups 0.017, stars 0.070, HSE 0.079)"),
    "X_ALT500": (CFG + "CFG34_groups_and_the_ladder_under_b.out", 55, "the phantom-only law alone 1.33"),
    "X_ALT2500": (CFG + "CFG34_groups_and_the_ladder_under_b.out", 56, "the phantom-only law alone 2.05"),
    "X_LAW": (CFG + "CFG34_groups_and_the_ladder_under_b.out", 74, "canonical R500: law 1.45 vs B 1.41; canonical R2500: law 2.24 vs B 1.88"),
    "X_HSE": (CFG + "CFG34_README.md", 40, "the R500 shortfall of 0.15 dex is carried by the hydrostatic allowance"),
    # KiDS
    "K_SPREAD": (CFG + "CFG27_edge_thread_closure.out", 33, "S_sph (A <= b) 50.2 -> S = 50.2 (the smallest)"),
    "K_COST1": (CFG + "CFG27_edge_thread_closure.out", 34, "budget-vs-KiDS cost 29.4"),
    "K_COST4": (CFG + "CFG27_edge_thread_closure.out", 37, "budget-vs-KiDS cost 49.3"),
    "K_NFW": (CFG + "CFG23_README.md", 38, "**χ² 99.3**, better than the framework's 104.7"),
    "K_NODISC": (CFG + "CFG23_README.md", 71, "KiDS does not discriminate between the framework and standard halos here"),
}

banner("C0  CITATION CHECK: every cited line contains the cited text")
bad = []
for key, (path, line, sub) in CITES.items():
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        ok = line <= len(lines) and sub in lines[line - 1]
    except OSError:
        ok = False
    if not ok:
        bad.append(f"{key} ({path}:{line})")
check("C0 all cited (file, line) pairs contain the cited text", f"{len(CITES)} citations; failures: {bad if bad else 'none'}", not bad)


def cite(key):
    path, line, _ = CITES[key]
    return f"{path}:{line}"


# ------------------------------------------------------------------------------------------------ algebra
def sig_at(delta, v1, f, n):
    return abs(delta) / math.sqrt(v1 / n + f * f)


def n_for(delta, v1, f, k):
    t = (abs(delta) / k) ** 2 - f * f
    return INF if t <= 0 else v1 / t


def cap_of(delta, f):
    return INF if f <= 0 else abs(delta) / f


def fneed(delta, k):
    return abs(delta) / k


def fmt(x, nd=1):
    if x == INF:
        return "inf"
    if x >= 1000:
        return f"{x:,.0f}"
    return f"{x:.{nd}f}"


def flo(f):
    """Floors go to zero under MUTATE."""
    return 0.0 if MUTATE else f


ROWS = []


def row(test, pair, delta, v1, f, unit, note="", ref_n=None, cite_keys=()):
    r = dict(test=test, pair=pair, delta=delta, v1=v1, floor=f, unit=unit,
             cap=cap_of(delta, f), n2=n_for(delta, v1, f, 2.0), n3=n_for(delta, v1, f, 3.0),
             f_need3=fneed(delta, 3.0), f_need2=fneed(delta, 2.0), note=note, cites=[cite(k) for k in cite_keys])
    if ref_n:
        r["sig_ref"] = sig_at(delta, v1, f, ref_n) if delta > 0 else 0.0
        r["ref_n"] = ref_n
    ROWS.append(r)
    return r


def show(r):
    ref = f"  S(N={r['ref_n']:,.0f}) = {r['sig_ref']:.2f}" if "ref_n" in r else ""
    P(f"    {r['pair']:58s} Delta {r['delta']:7.4f}  floor {r['floor']:.4f}  cap {fmt(r['cap'], 2):>6s}  "
      f"N(2s) {fmt(r['n2']):>9s}  N(3s) {fmt(r['n3']):>9s}  floor for 3s <= {r['f_need3']:.4f}{ref}")


# ================================================================================================ TEST 1 Gaia DR4
banner("TEST 1  GAIA DR4 WIDE BINARIES (gamma-hat; frozen estimator; N = 30,000)")
SIGFIT30 = 0.019          # G_SIGFIT
N_FROZEN = 30000          # G_N
SIGSYS = flo(0.02)        # G_SYS
V1_G = SIGFIT30 ** 2 * N_FROZEN                 # sigma_fit^2 = V1_G / N  (G_SCALE)
SIGFIT_DR3, N_DR3 = 0.035, 10624                # G_DR3
V1_G_DR3 = SIGFIT_DR3 ** 2 * N_DR3
sig_tot30 = math.sqrt(SIGFIT30 ** 2 + SIGSYS ** 2)
P(f"  inputs: sigma_fit(N=30,000) = {SIGFIT30} [{cite('G_SIGFIT')}];  sigma_sys = {SIGSYS} [{cite('G_SYS')}];  "
  f"sigma_tot = sqrt(fit^2 + sys^2) = {sig_tot30:.4f} (frozen quote 0.028) [{cite('G_TOT')}]")
P(f"  pessimistic scenario: DR3 dry-run precision, sigma_fit = {SIGFIT_DR3} at N = {N_DR3:,} [{cite('G_DR3')}] "
  f"(v1 = {V1_G_DR3:.3f} vs frozen {V1_G:.3f})")

READ = {  # committed predictions of gamma-hat
    "Newton/LCDM": (1.000, 1.000, "Newtonian wide binaries; LCDM's halo does not act on a 30 kAU pair (PRE Amendment 13(b) line 1502)"),
    "B (Arm C, ownership)": (1.000, 1.000, cite("G_ARMC")),
    "chain ceiling (Amdt 14)": (1.0725, 1.0900, cite("G_CHAIN") + " (canonical / alt; the value at the floor xi, falling to 1.000 for xi >= 0.3 pc)"),
    "Arm A floor (bare MOND + EFE)": (1.1614, 1.1917, cite("G_ARM_A_C") + " / " + cite("G_ARM_A_ALT")),
    "Arm A band top": (1.1814, 1.2267, cite("G_ARM_A_TOPALT")),
}
P("  committed predictions (canonical, alt):")
for k, (c, a, src) in READ.items():
    P(f"    {k:32s} {c:.4f}  {a:.4f}   [{src}]")

G_PAIRS = [
    ("B vs bare MOND-type law (Arm A floor)", "B (Arm C, ownership)", "Arm A floor (bare MOND + EFE)"),
    ("B vs bare MOND-type law (Arm A band top)", "B (Arm C, ownership)", "Arm A band top"),
    ("B vs LCDM/Newton", "B (Arm C, ownership)", "Newton/LCDM"),
    ("chain ceiling vs Newton/B/LCDM", "Newton/LCDM", "chain ceiling (Amdt 14)"),
    ("chain ceiling vs Arm A floor", "chain ceiling (Amdt 14)", "Arm A floor (bare MOND + EFE)"),
]
G_ROW = {}
for foot, idx in (("canonical", 0), ("alt", 1)):
    for scen, v1 in (("frozen sigma_fit", V1_G), ("DR3-like sigma_fit", V1_G_DR3)):
        P(f"\n  -- {foot} footing, {scen}, sigma_sys = {SIGSYS} --")
        for lab, a, b in G_PAIRS:
            d = abs(READ[b][idx] - READ[a][idx])
            r = row("Gaia DR4", f"{lab} [{foot}, {scen}]", d, v1, SIGSYS, "gamma",
                    ref_n=N_FROZEN if scen == "frozen sigma_fit" else N_DR3,
                    cite_keys=("G_SIGFIT", "G_SYS", "G_ARM_A_C", "G_ARMC", "G_CHAIN"))
            G_ROW[(foot, scen, lab)] = r
            show(r)

P("\n  Arm A's own computed band uncertainty (+-0.0175, PRE line 947) as an extra theory error on Arm A (canonical, frozen):")
d = READ["Arm A floor (bare MOND + EFE)"][0] - 1.0
S_with_band = d / math.sqrt(sig_tot30 ** 2 + 0.0175 ** 2)
P(f"    S(B vs Arm A floor) = {d:.4f}/sqrt({sig_tot30:.4f}^2 + 0.0175^2) = {S_with_band:.2f}  (vs {d / sig_tot30:.2f} without)")

P("\n  KILL / REFUTE THRESHOLDS at N = 30,000 (3 sigma_tot, canonical), valid only if the frozen stability requirements pass:")
KILL_G = {}
st = sig_tot30
KILL_G["B/Newton/LCDM killed from above at gamma-hat >="] = 1.0 + 3 * st
KILL_G["chain killed from above at gamma-hat >= (ceiling + 3 sigma)"] = 1.0725 + 3 * st
KILL_G["Arm A (bare MOND) killed from below at gamma-hat <= (floor - 3 sigma)"] = 1.1614 - 3 * st
for k, v in KILL_G.items():
    P(f"    {k:70s} {v:.4f}")
P(f"    frozen-rounded (sigma_tot 0.028): B killed >= {1 + 3 * 0.028:.3f} (PRE:1335 says 1.084); chain >= {1.0725 + 3 * 0.028:.3f} (PRE:1473 says 1.157); "
  f"Arm A <= {1.1614 - 3 * 0.028:.3f}")
P("    Contamination (hidden triples) biases gamma-hat HIGH, never low [" + cite("G_CONTAM") + "]; it is NOT part of sigma_sys.")
P("    So a Newtonian result is contamination-robust (it kills Arm A cleanly); a boost result needs the frozen ladder/NSS/kappa checks.")
P("    The alt-footing Arm A top (1.2267) sits below the 1.23 no-verdict edge; P(guard zone | true alt-top outcome) = 43-49% [" + cite("G_ALT_GUARD") + "].")

# ================================================================================================ TEST 2 a0(z)
banner("TEST 2  a0 AT z ~ 2.5 (mean offset of log a0 from the flat law, dex; per-object sigma on log a0)")
D_HZ, D_LCDM, D_LCDM_LO = 0.576, 0.334, 0.210        # Z_HZ, Z_LCDM (band low edge)
SIG_OBJ = {"0.13 (PAPER7 requirement)": 0.13, "0.257 (IFU + CO gas)": 0.257, "0.431 (IFU only)": 0.431}   # Z_SIG13, Z_SIGS
CAP_CFG52 = 2.3                                       # Z_CAP23: committed cap for flat vs H(z) whatever N
F_EFF = D_HZ / CAP_CFG52                              # a0-space floor implied by CFG52's committed 2.3-sigma cap
F_020 = 0.20                                          # Z_MASS: the lead's / CFG52's correlated mass-scale systematic, taken directly in a0 units
F_005 = 0.05                                          # Z_FLOOR05: CFG6's illustrative optimistic floor
P(f"  Deltas at z = 2.5: H(z) rival {D_HZ} [{cite('Z_HZ')}]; LCDM-native {D_LCDM} (band low edge {D_LCDM_LO}) [{cite('Z_LCDM')}]")
P(f"  B's own evolving-dark-energy band [-0.14, +0.04] [{cite('Z_BAND')}]; the D-thaw(w0) branch reaches +0.141 [{cite('Z_DTHAW')}] (not to be quoted as THE prediction).")
P(f"  floors: (a) CFG52's committed cap {CAP_CFG52} sigma for flat-vs-H(z) [{cite('Z_CAP23')}] implies f_eff = {D_HZ}/{CAP_CFG52} = {F_EFF:.4f} dex in a0 units [DERIVED HERE];")
P(f"          (b) the correlated 0.2 dex mass-scale systematic taken directly in a0 units = {F_020} [{cite('Z_MASS')}];  (c) CFG6's illustrative 0.05 [{cite('Z_FLOOR05')}].")
P("  Headline uses (a), the more conservative of (a) and (b); (b) and (c) are sensitivities.  Caveat: CFG52 works in g_obs (gap 0.23-0.27 dex) and CFG6 in log a0; (a) is the")
P("  only committed number that ties the mass-scale systematic to a significance cap, so it is used as the bridge and the conversion is flagged as derived.")
Z_ROWS = {}
for flab, f in (("f_eff (CFG52 cap 2.3)", flo(F_EFF)), ("f = 0.20", flo(F_020)), ("f = 0.05", flo(F_005))):
    P(f"\n  -- floor {flab} = {f:.4f} --")
    for slab, s in SIG_OBJ.items():
        for lab, d in (("B(flat) vs a0 ~ H(z) rival", D_HZ), ("B(flat) vs LCDM-native", D_LCDM),
                       ("B(flat) vs LCDM-native, band low edge", D_LCDM_LO),
                       ("B(band edge +0.04) vs LCDM-native", D_LCDM - 0.04)):
            r = row("a0(z)", f"{lab} [{flab}, sigma_obj {slab}]", d, s * s, f, "dex", cite_keys=("Z_HZ", "Z_LCDM", "Z_CAP23", "Z_SIG13"))
            Z_ROWS[(flab, slab, lab)] = r
            if slab.startswith("0.13"):
                show(r)
r0 = row("a0(z)", "B(flat) vs bare MOND with CONSTANT a0 (same tie)", 0.0, 0.13 ** 2, flo(F_EFF), "dex",
         note="identical prediction (a0 = kappa c sqrt(G rho_Lambda) is flat); not separable at any N")
P(f"\n  B(flat) vs bare MOND with a constant a0: Delta = 0 -> identical; a0(z) separates B only from an a0 that tracks H(z) or from LCDM-native.")
P("  Data in hand: none usable.  CFG54: N = 0 of 51 under the pre-registered selection [" + cite("Z_NODATA54") + "]; CFG52: no clean z >= 1.5 object with g_bar < 0.3 a0 [" + cite("Z_NODATA52") + "];")
P("  pooled z >= 1.5, g_bar < a0 (N = 14): no discrimination [" + cite("Z_POOLED") + "].")
KILL_Z = {}
f = flo(F_EFF)
for n in (2, 4, 10, 50):
    s = math.sqrt(0.13 ** 2 / n + f * f)
    KILL_Z[n] = dict(sigma_mean=s, rival_killed_2s_if_m_below=D_HZ - 2 * s, lcdm_killed_2s_if_m_below=D_LCDM - 2 * s,
                     flat_killed_2s_if_m_above=2 * s)
P("\n  READING A MEASURED MEAN OFFSET m (dex above flat) at 0.13 dex per object, floor f_eff (2-sigma rule):")
P(f"    {'N':>4s} {'sigma(mean)':>12s} {'flat B killed if m >':>22s} {'H(z) killed if m <':>20s} {'LCDM-native killed if m <':>26s}")
for n, k in KILL_Z.items():
    P(f"    {n:4d} {k['sigma_mean']:12.3f} {k['flat_killed_2s_if_m_above']:22.3f} {k['rival_killed_2s_if_m_below']:20.3f} {k['lcdm_killed_2s_if_m_below']:26.3f}")
P("    (a negative threshold means no measurement can kill that reading at 2 sigma with this floor)")

# ================================================================================================ TEST 3 dwarfs
banner("TEST 3  ULTRA-FAINT DWARFS (median log(sigma_obs/sigma_law), dex): isolated law (bare) vs B's derived cold-mass rule (LCDM-like NFW debris)")
res42 = json.load(open(os.path.join(ROOT, CFG, "CFG42_satellites_rule_results.json")))["numbers"]["UF"]
res46 = json.load(open(os.path.join(ROOT, CFG, "CFG46_ufd_binary_corrected_results.json")))["numbers"]["RES"]
res51 = json.load(open(os.path.join(ROOT, CFG, "CFG51_walker_ufd_results.json")))["numbers"]["RES"]
res28 = json.load(open(os.path.join(ROOT, CFG, "CFG28_ufd_referee_results.json")))["numbers"]["RES"]
LAW_C, RULE_C = res42["canonical|law"]["km"], res42["canonical|rule"]["km"]
LAW_A, RULE_A = res42["alt|law"]["km"], res42["alt|rule"]["km"]
D_CAN, D_ALT = LAW_C - RULE_C, LAW_A - RULE_A
D46_C = res46["canonical|sig_f|law"]["med"] - res46["canonical|sig_f|rule"]["med"]
D46_A = res46["alt|sig_f|law"]["med"] - res46["alt|sig_f|rule"]["med"]
S_ALL = res28["canonical"]["km"][1] * math.sqrt(40)          # bootstrap error of the Kaplan-Meier median x sqrt(40 systems)
S_BOOT46 = res46["canonical|sig_f|law"]["boot"] * math.sqrt(8)
S_BEST = res28["canonical"]["prec"][1] * math.sqrt(res28["canonical"]["prec"][2])     # best-measured 13 systems (error <= 25%)
F_UPS, F_MH, F_BIN = flo(0.077), flo(0.133), flo(0.104)
P(f"  predictions differ by Delta = law - rule = {D_CAN:.3f} (canonical) / {D_ALT:.3f} (alt) on CFG42's 40 systems [{cite('U_KM')}]; "
  f"{D46_C:.3f} / {D46_A:.3f} on CFG46's 8 binary-corrected systems [{cite('U_C46')}, {cite('U_C46RULE')}].")
P(f"  per-system scatter of the median estimator (bootstrap error x sqrt(N), from committed JSON): all 40 systems {S_ALL:.3f} [CFG28]; "
  f"CFG46's 8 systems {S_BOOT46:.3f}; best-measured 13 (error <= 25%) {S_BEST:.3f} [{cite('U_T4')}] = upper bound on the intrinsic scatter.")
P(f"  floors: Upsilon_V {F_UPS} [{cite('U_FLOOR')}]; collapse-mass {F_MH} [{cite('U_MHFLOOR')}]; binary-treatment shift bound {F_BIN} (CFG46 R2, correction range 0.068-0.104) [{cite('U_C46SHIFT')}].")
FLOORSETS = {
    "S1 Upsilon_V only": F_UPS,
    "S2 Upsilon_V + collapse-mass (HEADLINE)": math.hypot(F_UPS, F_MH),
    "S3 S2 + binary-treatment shift": math.sqrt(F_UPS ** 2 + F_MH ** 2 + F_BIN ** 2),
}
U_ROWS = {}
for flab, f in FLOORSETS.items():
    P(f"\n  -- floor set {flab}: f = {f:.4f} --")
    for slab, s in (("s = 0.242 (all 40)", S_ALL), ("s = 0.320 (CFG46's 8)", S_BOOT46), ("s = 0.201 (best-measured 13)", S_BEST)):
        r = row("dwarfs", f"law vs rule, Delta {D_CAN:.3f} [{flab}, {slab}]", D_CAN, s * s, f, "dex", cite_keys=("U_KM", "U_FLOOR", "U_MHFLOOR"))
        U_ROWS[(flab, slab)] = r
        if slab.startswith("s = 0.242"):
            show(r)
r_alt = row("dwarfs", f"law vs rule, alt footing Delta {D_ALT:.3f} [S2, s = 0.242]", D_ALT, S_ALL ** 2, FLOORSETS["S2 Upsilon_V + collapse-mass (HEADLINE)"], "dex")
r_46 = row("dwarfs", f"law vs rule, binary-corrected Delta {D46_C:.3f} [S2, s = 0.242]", D46_C, S_ALL ** 2, FLOORSETS["S2 Upsilon_V + collapse-mass (HEADLINE)"], "dex")
show(r_alt)
show(r_46)
HEAD_U = U_ROWS[("S2 Upsilon_V + collapse-mass (HEADLINE)", "s = 0.242 (all 40)")]

P("\n  PRECISION AXIS (headline floor S2): per-system scatter = sqrt(s_int^2 + e^2), s_int <= 0.201 (upper bound), e = per-system dispersion-measurement error in dex")
P(f"    {'e (dex)':>8s} {'s_tot':>7s} {'N for 2 sigma':>14s} {'N for 3 sigma':>14s}   note")
PREC = []
f2 = FLOORSETS["S2 Upsilon_V + collapse-mass (HEADLINE)"]
for e in (0.0, 0.046, 0.104, 0.135, 0.25, 0.40):
    s = math.hypot(S_BEST, e)
    n2, n3 = n_for(D_CAN, s * s, f2, 2.0), n_for(D_CAN, s * s, f2, 3.0)
    note = {0.0: "perfect dispersions", 0.046: "CFG51 Bootes I error", 0.104: "CFG51 Tucana II error",
            0.135: "matches the 40-system scatter (derived)", 0.25: "poor", 0.40: "very poor"}[e]
    PREC.append(dict(e=e, s_tot=s, n2=n2, n3=n3))
    P(f"    {e:8.3f} {s:7.3f} {fmt(n2):>14s} {fmt(n3):>14s}   {note}")
P(f"    Precision buys at most a factor (0.242/0.201)^2 = {(S_ALL / S_BEST) ** 2:.2f} in N: the scatter BETWEEN systems, not the dispersion error, sets N.")
P("  Usable systems today: 40 with single-epoch dispersions (uncleaned); 8 with a statistical binary correction (CFG46); 2 with multi-epoch cleaning (CFG51: Bootes I, Tucana II).")
P("  LCDM: the rule's NFW debris IS the LCDM-like reading.  Every collapse mass 2e8-1e12 passes 2 sigma and the offset spans +0.05 to -0.35 [" + cite("U_LCDMSPAN") + "]:")
P("        the rule/LCDM reading has a free halo mass and covers the whole range that separates it from the law, so B-rule vs LCDM has Delta = 0 by construction.")
P("  Bare MOND WITH the external field (lower predicted dispersions): no committed number -> not forecastable from committed budgets.")
KILL_U = {}
for n in (2, 8, 40):
    s = math.sqrt(S_ALL ** 2 / n + f2 ** 2)
    KILL_U[n] = dict(sigma_med=s, law_killed_2s_if_m_above=2 * s, rule_killed_2s_if_m_below=D_CAN - 2 * s,
                     law_killed_3s_if_m_above=3 * s, rule_killed_3s_if_m_below=D_CAN - 3 * s)
P("\n  READING A MEASURED MEDIAN OFFSET m (dex above the isolated law), headline floor S2, s = 0.242:")
P(f"    {'N':>4s} {'sigma(m)':>9s} {'law killed (2s) if m >':>24s} {'rule killed (2s) if m <':>25s} {'law killed (3s) if m >':>24s} {'rule killed (3s) if m <':>25s}")
for n, k in KILL_U.items():
    P(f"    {n:4d} {k['sigma_med']:9.3f} {k['law_killed_2s_if_m_above']:24.3f} {k['rule_killed_2s_if_m_below']:25.3f} {k['law_killed_3s_if_m_above']:24.3f} {k['rule_killed_3s_if_m_below']:25.3f}")
P(f"    Current binary-cleaned reading sits at m = +{res46['canonical|sig_f|law']['med']:.3f} (CFG46, 8 systems), +{res51['Bootes I|canonical|clean']['off']:.3f} / +{res51['Tucana II|canonical|clean']['off']:.3f} (CFG51, 2 systems);")
P(f"    the midpoint between the two readings is D/2 = {D_CAN / 2:.3f}: the data sit between them (CFG51 says the same), and Bootes I's cold component alone gives +0.007 [{cite('U_C51COLD')}].")

# ================================================================================================ TEST 4 groups
banner("TEST 4  X-RAY GROUPS (CFG34: median log10(M_HSE/M_pred), dex)")
G4 = {  # from CFG34 .out lines 53-56 and 74:  (log10 ratio B, stat, stars, HSE, ratio B, ratio law)
    "canonical R500": dict(dex=math.log10(1.41), stat=0.014, stars=0.023, hse=0.079, b=1.41, law=1.45),
    "canonical R2500": dict(dex=math.log10(1.88), stat=0.017, stars=0.070, hse=0.079, b=1.88, law=2.24),
    "alt R500": dict(dex=math.log10(1.33), stat=0.014, stars=0.020, hse=0.079, b=1.33, law=1.33),
    "alt R2500": dict(dex=math.log10(1.88), stat=0.016, stars=0.066, hse=0.079, b=1.88, law=2.05),
}
N_GROUPS = 20
P(f"  20 groups (Lovisari+2015 via h7).  Error components in dex from [{cite('X_R500')}], [{cite('X_R2500')}]; the HSE component is a 20% bias allowance = log10(1.2) = {math.log10(1.2):.4f} dex.")
X_ROWS = {}
for k, g in G4.items():
    f_sys = flo(math.hypot(g["stars"], g["hse"]))
    v1 = g["stat"] ** 2 * N_GROUPS
    r = row("groups", f"B vs closure (M_HSE = M_B; an NFW/LCDM halo of free mass closes it) [{k}]", g["dex"], v1, f_sys, "dex", cite_keys=("X_R500", "X_R2500"))
    r["sig_now"] = g["dex"] / math.sqrt(g["stat"] ** 2 + f_sys ** 2)
    X_ROWS[(k, "closure")] = r
    dlaw = abs(math.log10(g["b"] / g["law"]))
    r2 = row("groups", f"B vs bare law (phantom-only) [{k}]", dlaw, v1, f_sys, "dex", cite_keys=("X_LAW",))
    X_ROWS[(k, "law")] = r2
    P(f"    {k}: B shortfall {g['dex']:.4f} dex, S_now = {r['sig_now']:.2f} (committed {'1.80' if k == 'canonical R500' else ('2.57' if k == 'canonical R2500' else ('1.49' if k == 'alt R500' else '2.63'))}); floor {f_sys:.4f}")
    show(r)
    show(r2)
    # the HSE-bias allowance needed for 3 sigma at infinite N (if reachable)
    tgt = g["dex"] / 3.0
    rem = tgt ** 2 - g["stars"] ** 2 - g["stat"] ** 2
    if rem > 0 and not MUTATE:
        hse_dex = math.sqrt(rem)
        P(f"        for 3 sigma the HSE bias allowance must fall to {hse_dex:.4f} dex = {100 * (10 ** hse_dex - 1):.1f}% (from 20%)")
P("  B vs LCDM: LCDM (an NFW halo per group with free mass) reproduces M_HSE by construction, so 'B vs closure' is the only usable separation; it is a test of whether B's shortfall is real, not a")
P("  prediction contrast between two laws.  The cluster-scale baryon-fraction scaling (rho = -0.96, CFG34 H3) is a trend test, not forecastable from a per-group sigma in the committed budget.")
P("  Hydrostatic masses usually run LOW (CFG34 README line 40), which would make B's shortfall larger; the allowance is carried symmetrically.")

# ================================================================================================ TEST 5 KiDS
banner("TEST 5  KiDS BUDGET (CFG24/CFG27: cost in delta-chi2 of the cold budget's edge vs KiDS's own best)")
S_MACH = 50.2
COSTS = {"canonical P2": 29.4, "canonical nu_mono": 32.9, "alt P2": 45.4, "alt nu_mono": 49.3}
RATIO = {k: v / S_MACH for k, v in COSTS.items()}
S_EFF = 0.0 if MUTATE else S_MACH
P(f"  committed: smallest standard-halo spread S = {S_MACH} in delta-chi2 [{cite('K_SPREAD')}]; budget costs {COSTS} [{cite('K_COST1')}, {cite('K_COST4')}].")
P(f"  cost/S = " + ", ".join(f"{k} {v:.2f}" for k, v in RATIO.items()))
P("  Both cost and S are delta-chi2 between fixed models, so both grow in proportion to survey area: the ratio is INVARIANT to N.  No survey size moves cost above S;")
P("  only a better standard-halo model (smaller S) could.  The B-vs-NFW difference is 104.7 - 99.3 = 5.4 [" + cite("K_NFW") + "], which is 0.11 of S.")
P("  => KiDS: not forecastable from committed budgets as an N or precision requirement; capped by the machinery spread, not by statistics.")
KIDS = dict(S=S_MACH, costs=COSTS, ratio=RATIO, b_vs_nfw_dchi2=104.7 - 99.3, b_vs_nfw_over_S=(104.7 - 99.3) / S_MACH)
if MUTATE:
    P("  (MUTATE: machinery spread S set to 0 -> every cost would exceed it, an 'exclusion' at any N: the headline changes)")
KIDS["exclusion_reachable_without_floor"] = all(v > S_EFF for v in COSTS.values())

# ================================================================================================ C1 / C2 controls
banner("C1  CONTROL: committed JSON values used here equal the values typed in this script")
c1 = (abs(LAW_C - 0.3245) < 1e-3 and abs(RULE_C + 0.0586) < 1e-3 and abs(res46["canonical|sig_f|law"]["med"] - 0.206) < 1e-3
      and abs(res51["Bootes I|canonical|clean"]["off"] - 0.219) < 1e-3 and abs(res51["Tucana II|canonical|clean"]["off"] - 0.465) < 1e-3
      and abs(res42["canonical|law"]["f_ups"] - 0.077) < 1e-3 and abs(res42["canonical|rule"]["f_mh"] - 0.133) < 1e-3)
check("C1 CFG28/42/46/51 JSON values match the cited README numbers",
      f"law {LAW_C:+.4f}, rule {RULE_C:+.4f}, CFG46 f-free {res46['canonical|sig_f|law']['med']:+.4f}, CFG51 {res51['Bootes I|canonical|clean']['off']:+.3f}/{res51['Tucana II|canonical|clean']['off']:+.3f}, "
      f"floors {res42['canonical|law']['f_ups']:.4f}/{res42['canonical|rule']['f_mh']:.4f}", c1)

banner("C2  CONTROL: this algebra reproduces the committed separations")
ctl = []
# Gaia (uses the frozen sigma_tot = 0.028 rounding where the pre-registration does)
sg = lambda d, st: d / st
c = abs(sg(1.1614 - 1.0, 0.028) - 5.8) < 0.06 and abs(sg(1.1917 - 1.0, 0.028) - 6.8) < 0.1
check("C2a Arm A floors sit 5.8 / 6.8 sigma_tot above Arm C (sigma_tot = 0.028)", f"{sg(0.1614, 0.028):.2f} / {sg(0.1917, 0.028):.2f} [{cite('G_C_VS_A')}]", c)
# Arm B (old 1.045 / 1.030) capped by sigma_sys at infinite N
capB = (0.045 / SIGSYS if SIGSYS > 0 else INF, 0.030 / SIGSYS if SIGSYS > 0 else INF)
check("C2b the frozen sigma_sys caps the old Arm B (1.045 / 1.030) at 2.25 / 1.50 sigma at infinite N",
      f"{fmt(capB[0], 2)} / {fmt(capB[1], 2)} [{cite('G_ARMB_CAP1')}, {cite('G_ARMB_CAP2')}]",
      abs(capB[0] - 2.25) < 1e-9 and abs(capB[1] - 1.50) < 1e-9)
# Newton vs MI 1.09 at 3 sigma needs N ~ 12,200 (statistical only); MI 1.09 vs MG 1.137 needs ~45,000
n_a, n_b = n_for(0.09, V1_G, 0.0, 3.0), n_for(0.047, V1_G, 0.0, 3.0)
check("C2c frozen separation forecasts (statistical only): N ~ 12,200 and ~ 45,000 pairs",
      f"{n_a:,.0f} / {n_b:,.0f} (within 3%) [{cite('G_SEP1')}, {cite('G_SEP2')}]", abs(n_a / 12200 - 1) < 0.03 and abs(n_b / 45000 - 1) < 0.03)
# a0(z)
n_l = n_for(0.334, 0.13 ** 2, 0.0, 3.0)
n_b2 = n_for(0.101, 0.13 ** 2, 0.0, 3.0)
n_t = n_for(0.106, 0.13 ** 2, 0.0, 3.0)
check("C2d a0(z): 2.57 sigma at 0.13 dex; 3 sigma needs 1.4 / 15 / 13 objects (LCDM-native / B-CPL / C-thaw(w0), no floor)",
      f"{sig_at(0.334, 0.13 ** 2, 0.0, 1):.2f}; {n_l:.1f} / {n_b2:.1f} / {n_t:.1f} [{cite('Z_SIG13')}, {cite('Z_N_LCDM')}, {cite('Z_N_BCPL')}, {cite('Z_N_THAW')}]",
      abs(sig_at(0.334, 0.13 ** 2, 0.0, 1) - 2.57) < 0.01 and abs(n_l - 1.4) < 0.1 and abs(n_b2 - 15) < 1 and abs(n_t - 13) < 1)
# CFG52 cap: with f_eff the flat-vs-H(z) cap is 2.3 by construction; and the a0-space 0.2 floor gives 2.88
capz = cap_of(D_HZ, flo(F_EFF))
check("C2e a0(z): CFG52's committed cap (~2.3 sigma whatever N) for flat vs H(z) is reproduced by the effective floor",
      f"cap = {fmt(capz, 2)} [{cite('Z_CAP23')}]; with f = 0.20 taken in a0 units the cap would be {fmt(cap_of(D_HZ, flo(F_020)), 2)}", abs(capz - 2.3) < 0.01)
# dwarfs
z_law = LAW_C / math.hypot(res42["canonical|law"]["err"], res42["canonical|law"]["f_ups"])
z_rule = RULE_C / res42["canonical|rule"]["tot"]
z46 = res46["canonical|sig_f|law"]["med"] / res46["canonical|sig_f|law"]["tot"]
z51 = res51["Bootes I|canonical|clean"]["off"] / res51["Bootes I|canonical|clean"]["tot"]
check("C2f dwarfs: the committed standings are recomputed from their error components: 3.77 / -0.41 / 1.26 / 2.46 sigma",
      f"{z_law:.2f} / {z_rule:.2f} / {z46:.2f} / {z51:.2f} [{cite('U_KM')}, {cite('U_C46')}, {cite('U_C51BOO')}]",
      abs(z_law - 3.77) < 0.02 and abs(z_rule + 0.41) < 0.02 and abs(z46 - 1.26) < 0.02 and abs(z51 - 2.46) < 0.02)
# groups
g = G4["canonical R500"]
zg = g["dex"] / math.sqrt(g["stat"] ** 2 + g["stars"] ** 2 + g["hse"] ** 2)
check("C2g groups: 1.80 sigma at R500 canonical recomputed from (0.014, 0.023, 0.079)", f"{zg:.2f} [{cite('X_H1')}]", abs(zg - 1.80) < 0.02)
# KiDS
rr = [COSTS["canonical P2"] / S_MACH, COSTS["alt nu_mono"] / S_MACH]
check("C2h KiDS: cost/S = 0.59 ... 0.98", f"{rr[0]:.2f} ... {rr[1]:.2f} [{cite('K_COST1')}, {cite('K_COST4')}]", abs(rr[0] - 0.59) < 0.01 and abs(rr[1] - 0.98) < 0.01)

# ================================================================================================ HEADLINE H1
banner("H1  HEADLINE (pre-declared; MUTATE must fail)")
cap_gaia_A = G_ROW[("canonical", "frozen sigma_fit", "B vs bare MOND-type law (Arm A floor)")]["cap"]
cap_gaia_L = G_ROW[("canonical", "frozen sigma_fit", "B vs LCDM/Newton")]["delta"]
cap_hz = Z_ROWS[("f_eff (CFG52 cap 2.3)", "0.13 (PAPER7 requirement)", "B(flat) vs a0 ~ H(z) rival")]["cap"]
cap_lc = Z_ROWS[("f_eff (CFG52 cap 2.3)", "0.13 (PAPER7 requirement)", "B(flat) vs LCDM-native")]["cap"]
cap_u = HEAD_U["cap"]
cap_x = X_ROWS[("canonical R500", "closure")]["cap"]
capped = {"a0(z) B-vs-H(z)": cap_hz, "a0(z) B-vs-LCDM-native": cap_lc, "dwarfs law-vs-rule": cap_u, "groups B-vs-closure R500": cap_x}
below3 = {k for k, v in capped.items() if v < 3.0}
h1 = (below3 == set(capped) and cap_gaia_A > 3.0 and cap_gaia_L == 0.0)
P("  caps (sigma at infinite N, committed floors): " + "; ".join(f"{k} {fmt(v, 2)}" for k, v in capped.items()))
P(f"  Gaia B vs Arm A floor cap {fmt(cap_gaia_A, 2)} (> 3); Gaia B vs LCDM Delta = {cap_gaia_L} (identical)")
check("H1 [HEADLINE] with the committed floors exactly the four tests are capped below 3 sigma; Gaia B-vs-Arm-A clears 3 sigma; Gaia B-vs-LCDM is identical",
      f"below 3 sigma: {sorted(below3)}; Gaia cap {fmt(cap_gaia_A, 2)}", h1)

# ================================================================================================ RANKED TABLE
banner("RANKED TABLE (headline settings; caps and N are for the pair named)")
TBL = [
    dict(test="Gaia DR4 wide binaries", pair="B (1.000) vs bare MOND Arm A (1.1614 / 1.1917)",
         r=G_ROW[("canonical", "frozen sigma_fit", "B vs bare MOND-type law (Arm A floor)")],
         inhand="N = 30,000 expected (DR3 dry run 10,624); release 2 Dec 2026, pipeline built", n_avail=30000, cls=""),
    dict(test="Gaia DR4 wide binaries", pair="B (1.000) vs LCDM / Newton (1.000)",
         r=G_ROW[("canonical", "frozen sigma_fit", "B vs LCDM/Newton")], inhand="same", cls=""),
    dict(test="Gaia DR4 wide binaries", pair="chain ceiling (1.0725 / 1.0900) vs Newton",
         r=G_ROW[("canonical", "frozen sigma_fit", "chain ceiling vs Newton/B/LCDM")], inhand="needs xi near its floor", n_avail=30000, cls=""),
    dict(test="Dwarfs (ultra-faint)", pair="isolated law vs derived rule / LCDM-like debris",
         r=HEAD_U, inhand="40 uncleaned; 8 statistically corrected; 2 multi-epoch", cls=""),
    dict(test="a0(z) at z ~ 2.5", pair="B flat vs a0 ~ H(z)",
         r=Z_ROWS[("f_eff (CFG52 cap 2.3)", "0.13 (PAPER7 requirement)", "B(flat) vs a0 ~ H(z) rival")], inhand="0 usable discs (0 of 51; 0 clean)", cls=""),
    dict(test="X-ray groups R500", pair="B vs closure (LCDM-like free halo)",
         r=X_ROWS[("canonical R500", "closure")], inhand="20 groups in hand", cls=""),
    dict(test="a0(z) at z ~ 2.5", pair="B flat vs LCDM-native (+0.334)",
         r=Z_ROWS[("f_eff (CFG52 cap 2.3)", "0.13 (PAPER7 requirement)", "B(flat) vs LCDM-native")], inhand="0 usable discs", cls=""),
    dict(test="KiDS budget", pair="B vs standard halos", r=None, inhand="n/a", cls="NOT FORECASTABLE from committed budgets (cost/S 0.59-0.98, N-invariant)"),
]
def classify(r, n_avail=None):
    if r["delta"] == 0:
        return "IDENTICAL PREDICTION (survival test only)"
    if r["cap"] >= 3.0:
        if n_avail is not None and r["n3"] > n_avail:
            return f"cap {r['cap']:.1f} > 3 sigma, but N(3s) exceeds the {n_avail:,.0f} expected"
        return "DISCRIMINATES (cap > 3 sigma)"
    if r["cap"] >= 2.0:
        return f"CAPPED below 3 sigma (cap {r['cap']:.2f})"
    return f"CAPPED below 2 sigma (cap {r['cap']:.2f})"


P(f"  {'test':26s} {'pair':52s} {'Delta':>7s} {'floor':>7s} {'cap':>6s} {'N(2s)':>9s} {'N(3s)':>9s}   class")
for t in TBL:
    r = t["r"]
    if r is None:
        P(f"  {t['test']:26s} {t['pair']:52s} {'--':>7s} {'--':>7s} {'--':>6s} {'--':>9s} {'--':>9s}   {t['cls']}")
    else:
        t["cls"] = classify(r, t.get("n_avail"))
        P(f"  {t['test']:26s} {t['pair']:52s} {r['delta']:7.4f} {r['floor']:7.4f} {fmt(r['cap'], 2):>6s} {fmt(r['n2']):>9s} {fmt(r['n3']):>9s}   {t['cls']}")
P("  In-hand sample: " + "; ".join(f"{t['test']} / {t['pair'].split(' vs ')[0]}: {t['inhand']}" for t in TBL if t['r'] is not None))

# ================================================================================================ VERDICT + files
nfail = [c for c in CHECKS if c["load_bearing"] and not c["ok"]]
banner("SUMMARY")
P(f"  checks: {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} pass; load-bearing failures: {len(nfail)}; MUTATE = {MUTATE}")
if nfail:
    for c in nfail:
        P(f"    FAILED: {c['name']}")
P("  Nothing here says the theory is closed.  kappa = 1/2 stays FITTED.")

OUT = dict(slug="CFG63_forecast" + TAG, mutate=MUTATE,
           summary=dict(n_checks=len(CHECKS), n_pass=sum(c["ok"] for c in CHECKS), load_bearing_failures=len(nfail),
                        failed=[c["name"] for c in nfail]),
           checks=CHECKS, rows=[{k: (None if isinstance(v, float) and v == INF else v) for k, v in r.items()} for r in ROWS],
           kill=dict(gaia=KILL_G, a0z={str(k): v for k, v in KILL_Z.items()}, dwarfs={str(k): v for k, v in KILL_U.items()}),
           precision_axis=PREC, kids=KIDS,
           headline=dict(capped_below_3=sorted(below3), gaia_cap_B_vs_ArmA=None if cap_gaia_A == INF else cap_gaia_A))
with open(os.path.join(HERE, f"forecast{TAG}.out"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
with open(os.path.join(HERE, f"forecast{TAG}_results.json"), "w", encoding="utf-8") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: None if o == INF else str(o))
sys.exit(1 if nfail else 0)
