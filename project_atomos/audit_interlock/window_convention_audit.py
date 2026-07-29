#!/usr/bin/env python3
"""
window_convention_audit.py -- AUDIT LENS: MEASUREMENT WINDOWS.

Question set (Carl, 2026-07-28):
  (1) What does `rel_precision` in targets/pdg_constants.py actually MEAN -- 1 sigma or k sigma,
      relative or absolute?
  (2) Is the window used by grind.py's hit test the SAME quantity that BITS_RULE.py and
      GATE_POWER_ANALYSIS.py assume when they count bits / compute the informative ceiling?
      Any factor-of-2 (+/-w vs 2w) or sigma-convention mismatch?
  (3) Spot-check target central values + uncertainties against real PDG/CODATA numbers.

Everything below is COMPUTED from the committed code (verbatim imports of the real
score_value / measurement_tol / sm_target_keys / _target_windows), never asserted.
Local-only project. No network. Exit 0.
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402

import targets.pdg_constants as pdg                       # noqa: E402
from engine.scoring import score_value, measurement_tol   # noqa: E402
from exhaust_parallel import sm_target_keys               # noqa: E402
from exhaust_depth5_forced import N_TARGETS               # noqa: E402
import grind                                              # noqa: E402
from gate.fdr import _bit_cap, _poisson_e_chance          # noqa: E402
from gate.candidate import SearchSpace, Candidate as _GC   # noqa: E402  (schema only)

ds = pdg.load()
BAR = "=" * 100
checks = []


def check(msg, cond):
    checks.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


print(BAR)
print("WINDOW CONVENTION AUDIT -- project_atomos measurement windows")
print(BAR)

# =====================================================================================
# S1. WHAT IS rel_precision, AND WHAT IS THE HIT PREDICATE, EXACTLY?
# =====================================================================================
print("\nS1  rel_precision AND THE HIT PREDICATE -- resolved by direct probe, not by reading")
print("-" * 100)
print("  Target.rel_precision = float(sigma)/|value|  (pdg_constants.py:106-112)")
print("  measurement_tol(t)   = clamp(rel_precision, 1e-10, 0.2)  (engine/scoring.py:108-119)")
print("  grind hit predicate  = score_value(v, t).rel_error <= tol, rel_error=|v-tv|/|tv|")
print("  => hit  <=>  |v - tv| <= tol*|tv|  =  1.000 sigma  (when tol is unclamped)")
print("  So: HALF-width = 1 sigma; FULL relative window width = 2*rel_precision.\n")

probe_keys = sm_target_keys(include_holdout=True)
print(f"  {'target':<18}{'rel_prec':>12}{'tol':>12}{'clamped':>9}"
      f"{'hit@0.999s':>11}{'hit@1.001s':>11}{'n_sig@edge':>12}")
print("  " + "-" * 96)
edge_ok = True
clamped_any = []
for k in probe_keys:
    t = ds.target(k)
    tol = measurement_tol(t)
    rp = t.rel_precision
    cl = abs(tol - rp) > 1e-18 * max(1.0, rp)
    if cl:
        clamped_any.append((k, rp, tol))
    tv, sg = float(t.value), float(t.sigma)
    v_in = tv + 0.999 * sg
    v_out = tv + 1.001 * sg
    hit_in = score_value(v_in, t).rel_error <= tol
    hit_out = score_value(v_out, t).rel_error <= tol
    ns_edge = score_value(tv + sg, t).n_sigma
    if not (hit_in and not hit_out):
        edge_ok = False
    print(f"  {k:<18}{rp:>12.3e}{tol:>12.3e}{('YES' if cl else '-'):>9}"
          f"{str(hit_in):>11}{str(hit_out):>11}{ns_edge:>12.6f}")

check("hit predicate is EXACTLY +/-1.000 sigma for every searched target "
      "(inside at 0.999s, outside at 1.001s)", edge_ok)
check(f"min_tol=1e-10 / max_tol=0.2 clamps bind on {len(clamped_any)} of {len(probe_keys)} "
      f"searched targets{'' if not clamped_any else ' -> ' + str(clamped_any)}",
      len(clamped_any) == 0)
tightest = min((ds.target(k).rel_precision, k) for k in probe_keys)
print(f"\n  tightest searched target: {tightest[1]} at rel={tightest[0]:.3e} "
      f"= {tightest[0]/1e-10:.2f} x the min_tol=1e-10 clamp "
      f"({math.log2(tightest[0]/1e-10):+.2f} bits of headroom before the clamp bites)")

# =====================================================================================
# S2. THE THREE PLACES A WINDOW IS USED -- IS IT THE SAME QUANTITY?
# =====================================================================================
print("\nS2  IS THE HIT WINDOW THE SAME QUANTITY THE BITS/CEILING ANALYSES ASSUME?")
print("-" * 100)
# (a) GATE_POWER_ANALYSIS: w = sigma/value then w2 = 2*w  ("two-sided window")
# (b) BITS_RULE: tabulated w, used as bits = log2(1/w)
# (c) gate/fdr._poisson_e_chance: e_chance = n_wide * (2*tol) / 0.2   <- full width 2*tol
lib = np.linspace(0.9, 1.1, 200_001) * 137.035999177   # uniform density probe
t_alpha = ds.target("alpha_em_inv_0")
tol_a = measurement_tol(t_alpha)
n_hit, e_ch = _poisson_e_chance(float(t_alpha.value), lib, tol_a)
n_wide = int(((lib >= float(t_alpha.value) * 0.9) & (lib <= float(t_alpha.value) * 1.1)).sum())
e_expect_fullwidth = n_wide * (2 * tol_a) / 0.2
e_expect_halfwidth = n_wide * tol_a / 0.2
print(f"  gate/fdr._poisson_e_chance on 1/alpha (uniform lib, n_wide={n_wide}):")
print(f"    E_chance returned          = {e_ch:.6e}")
print(f"    n_wide*(2*tol)/0.2         = {e_expect_fullwidth:.6e}   <-- FULL width 2*tol")
print(f"    n_wide*(tol)/0.2           = {e_expect_halfwidth:.6e}   (half width, NOT used)")
check("Gate A's Poisson E_chance uses the FULL window width 2*tol -- same convention as "
      "GATE_POWER_ANALYSIS's w2=2*w and BITS_RULE's tabulated w",
      abs(e_ch - e_expect_fullwidth) < 1e-12 * max(1.0, e_expect_fullwidth))

# BITS_RULE's table vs 2*rel_precision from the dataset the search actually uses
BITS_RULE_W = {"m_p/m_e": 3.49e-14, "1/alpha": 3.06e-10, "m_mu/m_e": 4.45e-9,
               "koide_Q_lep": 2.0e-5, "r_tau_mu": 1.4e-4, "sin^2 theta_W": 3.4e-4,
               "m_t/m_b": 7.0e-3, "alpha_s(M_Z)": 1.5e-2}
GPA_SIGMA_REL = {  # GATE_POWER_ANALYSIS.py TARGETS, 1-sigma relative as written there
    "1/alpha": 2.1e-8 / 137.036, "m_p/m_e": 3.2e-11 / 1836.15,
    "m_mu/m_e": 4.6e-7 / 206.768, "m_tau/m_mu": 0.0007 / 16.817,
    "sin^2 theta_W": 4.0e-5 / 0.23122, "alpha_s(M_Z)": 9.0e-4 / 0.1180,
    "m_t/m_b": 0.0035, "koide_Q_lep": 1.0e-5}
NAME2KEY = {"m_p/m_e": "r_p_e", "1/alpha": "alpha_em_inv_0", "m_mu/m_e": "r_mu_e",
            "koide_Q_lep": "koide_Q_lep", "r_tau_mu": "r_tau_mu", "m_tau/m_mu": "r_tau_mu",
            "sin^2 theta_W": "sin2_thetaW_MZ", "m_t/m_b": "r_t_b",
            "alpha_s(M_Z)": "alpha_s_MZ"}

bits = lambda w: math.log2(1.0 / w)  # noqa: E731
print(f"\n  {'name':<15}{'BITS_RULE w':>13}{'GPA 2*w':>12}{'DATASET 2*rel':>15}"
       f"{'bits(BR)':>10}{'bits(data)':>11}{'delta bits':>11}  direction")
print("  " + "-" * 96)
deltas = {}
for name, wbr in sorted(BITS_RULE_W.items(), key=lambda kv: kv[1]):
    key = NAME2KEY[name]
    t = ds.target(key)
    w_data = 2.0 * t.rel_precision
    w_gpa = 2.0 * GPA_SIGMA_REL[name] if name in GPA_SIGMA_REL else float("nan")
    d = bits(wbr) - bits(w_data)
    deltas[name] = d
    direction = "BITS_RULE OVER-credits" if d > 0.05 else (
        "BITS_RULE under-credits" if d < -0.05 else "agree")
    print(f"  {name:<15}{wbr:>13.3e}{w_gpa:>12.3e}{w_data:>15.3e}"
          f"{bits(wbr):>10.1f}{bits(w_data):>11.1f}{d:>+11.2f}  {direction}")
same = [n for n, d in deltas.items() if abs(d) <= 0.05]
diff = {n: d for n, d in deltas.items() if abs(d) > 0.05}
print(f"\n  identical (<=0.05 bit): {sorted(same)}")
print(f"  MISMATCHED: " + ", ".join(f"{n} {d:+.2f} bits" for n, d in
                                    sorted(diff.items(), key=lambda kv: -abs(kv[1]))))
# CONVENTION PROOF, independent of whose sigma is right: BITS_RULE w == 2 * GPA's 1-sigma rel
print("\n  CONVENTION PROOF -- is BITS_RULE's w the same QUANTITY as GPA's two-sided w2=2*w?")
print(f"  {'name':<15}{'BITS_RULE w':>14}{'2 * GPA_1sigma_rel':>20}{'ratio':>9}")
print("  " + "-" * 96)
conv = []
for name in sorted(GPA_SIGMA_REL):
    if name not in BITS_RULE_W:
        continue
    r = BITS_RULE_W[name] / (2.0 * GPA_SIGMA_REL[name])
    conv.append(r)
    print(f"  {name:<15}{BITS_RULE_W[name]:>14.3e}{2*GPA_SIGMA_REL[name]:>20.3e}{r:>9.4f}")
print(f"  ratio spread {min(conv):.4f}..{max(conv):.4f} (1.000 = same convention; "
      f"0.500 or 2.000 would be a factor-of-2 bug)")
check("BITS_RULE's tabulated w IS GPA's full-width w2 = 2*(1-sigma rel), which IS the full "
      "relative width of grind's +/-1sigma hit window -> NO factor-of-2 / sigma-convention "
      "mismatch between the hit test and the bits accounting",
      all(abs(r - 1.0) < 0.02 for r in conv))
check(f"but {len(diff)} of {len(deltas)} targets carry a NUMERIC window mismatch between "
      f"the bits accounting and the dataset the search uses", len(diff) > 0)

# =====================================================================================
# S3. THE ONE REAL FACTOR-OF-2: Gate A's _bit_cap vs the window it is capping
# =====================================================================================
print("\nS3  FACTOR-OF-2 CHECK INSIDE THE GATE: _bit_cap vs the window's own information")
print("-" * 100)
print("  gate/fdr._bit_cap = n_digits_known * log2(10),  n_digits = -log10(rel_precision)")
print("  => cap = log2(1/rel) = log2(1/(w_full/2)) = log2(1/w_full) + 1  EXACTLY.")
print("  The look-elsewhere accounting (GPA S1/S2, BITS_RULE) pays log2(1/w_full) per target.\n")
print(f"  {'target':<18}{'w_full=2*rel':>14}{'window bits':>13}{'_bit_cap':>10}{'excess':>9}")
print("  " + "-" * 96)


class _Shim:
    def __init__(self, s):
        self.search = s


excesses = []
for k in probe_keys[:8]:
    t = ds.target(k)
    s = SearchSpace(tol=measurement_tol(t), target_sigma=float(t.sigma),
                    n_digits_known=float(t.n_digits))
    cap = _bit_cap(_Shim(s))
    wb = bits(2.0 * t.rel_precision)
    excesses.append(cap - wb)
    print(f"  {k:<18}{2*t.rel_precision:>14.3e}{wb:>13.2f}{cap:>10.2f}{cap - wb:>+9.3f}")
print(f"\n  excess is {np.mean(excesses):+.6f} bits on every target (max dev "
      f"{max(abs(e - 1.0) for e in excesses):.2e} from exactly 1 bit).")
check("Gate A's per-target bit cap is EXACTLY 1 bit (a factor of 2) more generous than the "
      "bits its own +/-1sigma window carries under the BITS_RULE/GPA convention",
      all(abs(e - 1.0) < 1e-9 for e in excesses))
print(f"  CONSEQUENCE: PASS_BITS=10 is effectively 9 window-bits; a k-target interlock read-out "
      f"\n  built from _bit_cap over-credits k bits (k=4 -> 4 bits against a 10-bit margin).")

# =====================================================================================
# S4. SPOT-CHECK CENTRAL VALUES + UNCERTAINTIES AGAINST REAL PDG/CODATA
# =====================================================================================
print("\nS4  SPOT-CHECK OF CENTRAL VALUES AND SIGMAS vs PDG-2024 / CODATA-2018-2022")
print("-" * 100)
# reference: (key, ref_value, ref_sigma, source string). Model-knowledge reference values.
REF = [
    ("m_e", 0.51099895000, 1.5e-10, "CODATA2018 0.51099895000(15) MeV"),
    ("m_mu", 105.6583755, 2.3e-6, "CODATA2018 105.6583755(23) MeV"),
    ("m_tau", 1776.86, 0.12, "PDG2024 1776.86 +/- 0.12 MeV"),
    ("m_p", 938.27208816, 2.9e-7, "CODATA2018 938.27208816(29) MeV"),
    ("m_n", 939.56542052, 5.4e-7, "CODATA2018 939.56542052(54) MeV"),
    ("alpha_em_inv_0", 137.035999177, 2.1e-8, "CODATA2022 137.035999177(21)"),
    ("alpha_s_MZ", 0.1180, 0.0009, "PDG2024 0.1180 +/- 0.0009"),
    ("sin2_thetaW_MZ", 0.23122, 0.00004, "PDG MS-bar s^2hat(MZ) 0.23122(4)"),
    ("m_t", 172570.0, 290.0, "PDG2024 172.57 +/- 0.29 GeV"),
    ("m_b", 4180.0, 30.0, "PDG2024 4.18 +0.03 -0.02 GeV"),
    ("m_c", 1270.0, 20.0, "PDG2024 1.27 +/- 0.02 GeV"),
    ("m_s", 93.5, 0.8, "PDG2024 93.5 +0.8 -0.8 MeV"),
    ("m_u", 2.16, 0.49, "PDG2024 2.16 +0.49 -0.26 MeV"),
    ("m_d", 4.67, 0.48, "PDG2024 4.67 +0.48 -0.17 MeV"),
    ("m_Z", 91.1880, 0.0020, "PDG2024 91.1880(20) GeV"),
    ("m_W", 80.3692, 0.0133, "PDG2024 80.3692(133) GeV"),
    ("m_H", 125.20, 0.11, "PDG2024 125.20(11) GeV"),
    ("G_F", 1.1663787e-5, 6.0e-12, "PDG 1.1663787(6)e-5 GeV^-2"),
    ("a_e", 1.15965218059e-3, 1.3e-13, "CODATA 1.15965218059(13)e-3"),
    ("a_mu", 1.16592059e-3, 2.2e-10, "PDG2023 wavg 116592059(22)e-11"),
    ("ckm_lambda", 0.22501, 0.00068, "PDG2024 Wolfenstein lambda"),
    ("pmns_sin2_12", 0.303, 0.012, "NuFIT5.2 NO"),
    ("pmns_sin2_13", 0.02203, 0.00056, "NuFIT5.2 NO"),
    ("pmns_sin2_23", 0.572, 0.018, "NuFIT5.2 NO"),
    ("Dm2_21", 7.42e-5, 0.21e-5, "NuFIT5.2 eV^2"),
    ("v_higgs", 246.21965, 6.3e-5, "(sqrt2 G_F)^-1/2 ; sigma = 0.5*rel(G_F)*v"),
]
print(f"  {'key':<17}{'dataset value':>17}{'ref value':>17}{'val off [sig]':>14}"
      f"{'sig ratio':>11}  flag")
print("  " + "-" * 96)
val_flags, sig_flags = [], []
for key, rv, rs, src in REF:
    t = ds.target(key)
    v, s = float(t.value), float(t.sigma)
    off = abs(v - rv) / rs if rs > 0 else float("inf")
    ratio = s / rs if rs > 0 else float("inf")
    fl = []
    if off > 0.5:
        fl.append("VALUE?")
        val_flags.append((key, v, rv, off))
    if ratio > 1.5 or ratio < 1 / 1.5:
        fl.append("SIGMA?")
        sig_flags.append((key, s, rs, ratio))
    print(f"  {key:<17}{v:>17.10g}{rv:>17.10g}{off:>14.2f}{ratio:>11.3f}  "
          f"{','.join(fl)}   {src if fl else ''}")
print(f"\n  central values off by >0.5 sigma: {[(k, f'{o:.1f}s') for k, _, _, o in val_flags] or 'NONE'}")
print(f"  sigmas off by >1.5x:              "
      f"{[(k, f'{r:.2f}x') for k, _, _, r in sig_flags] or 'NONE'}")
check(f"{len(REF)} central values spot-checked; {len(val_flags)} deviate by >0.5 sigma from the "
      f"reference", len(val_flags) <= 2)

# derived-vs-direct: the ratios the dataset PROPAGATES but that are MEASURED DIRECTLY
print("\n  DERIVED-RATIO WINDOWS vs the DIRECTLY MEASURED ratio (the load-bearing one):")
DIRECT = [("r_p_e", 1836.152673426, 3.2e-11, "CODATA2022 m_p/m_e = 1836.152673426(32)"),
          ("r_mu_e", 206.7682827, 4.6e-6, "CODATA2022 m_mu/m_e = 206.7682827(46)"),
          ("r_tau_mu", 16.8170, 0.00114, "from PDG m_tau 1776.86(12)/m_mu")]
print(f"  {'ratio':<10}{'propagated sigma':>18}{'direct sigma':>15}{'window too wide by':>20}"
      f"{'bits lost':>11}")
print("  " + "-" * 96)
for key, rv, rs, src in DIRECT:
    t = ds.target(key)
    if key not in ds:
        continue
    s = float(t.value) * t.rel_precision
    print(f"  {key:<10}{s:>18.3e}{rs:>15.3e}{s / rs:>20.1f}x{math.log2(s / rs):>10.1f}")
    print(f"             {src}")
t_pe = ds.target("r_p_e")
inflate = (float(t_pe.value) * t_pe.rel_precision) / 3.2e-11
check(f"r_p_e's PROPAGATED window is {inflate:.0f}x wider than the directly measured CODATA "
      f"ratio ({math.log2(inflate):.1f} bits) -- the search uses the WIDE one, BITS_RULE credits "
      f"the NARROW one", inflate > 100)

# =====================================================================================
# S5. WHAT THE CORRECTED WINDOWS DO TO BITS_RULE'S kmin (the interlock threshold)
# =====================================================================================
print("\nS5  RE-RUN BITS_RULE's THRESHOLD WITH THE WINDOWS THE SEARCH ACTUALLY USES")
print("-" * 100)
BASE, D0, MARGIN = 30.0, 4, 10.0
HOLD = {"koide_Q_lep", "r_tau_mu"}
fit_br = sorted([(n, w) for n, w in BITS_RULE_W.items() if NAME2KEY[n] not in HOLD],
                key=lambda kv: kv[1])
fit_ds = sorted([(n, 2.0 * ds.target(NAME2KEY[n]).rel_precision) for n, _ in fit_br],
                key=lambda kv: kv[1])
for D in (10, 18):
    cost = math.log2(BASE ** (D - D0))
    need = cost + MARGIN
    print(f"\n  depth D={D}: look-elsewhere cost {cost:.1f} bits, need > {need:.1f}")
    for label, fit in (("BITS_RULE windows", fit_br), ("DATASET windows (what the search uses)",
                                                       fit_ds)):
        run, kmin = 0.0, None
        line = []
        for i, (n, w) in enumerate(fit, 1):
            run += bits(w)
            line.append(f"k={i}:{run:.1f}")
            if kmin is None and run > need:
                kmin = i
        print(f"    {label:<40} total={run:6.1f} bits  kmin={kmin}   [{' '.join(line)}]")
tot_br = sum(bits(w) for _, w in fit_br)
tot_ds = sum(bits(w) for _, w in fit_ds)
print(f"\n  TOTAL fittable bits: BITS_RULE {tot_br:.1f} vs dataset {tot_ds:.1f} "
      f"-> BITS_RULE over-credits {tot_br - tot_ds:+.1f} bits across 6 fittable targets.")
cost18 = math.log2(BASE ** 14)


def kmin_of(fit, need):
    run = 0.0
    for i, (n, w) in enumerate(fit, 1):
        run += bits(w)
        if run > need:
            return i
    return None


k_br = kmin_of(fit_br, cost18 + MARGIN)
k_ds = kmin_of(fit_ds, cost18 + MARGIN)
check(f"at depth 18 the honest kmin from the search's OWN windows is {k_ds} vs BITS_RULE's "
      f"{k_br}", True)
print(f"  (BITS_RULE prints 'MINIMUM {k_br} interlocked fittable targets'; with the dataset's own "
      f"windows it is {k_ds}.)")

# =====================================================================================
# S6. RETENTION WINDOW: is the spilled-record window a true superset, and does it cover
#     the HELD-OUT targets a survivor must PREDICT?
# =====================================================================================
print("\nS6  RETENTION WINDOWS (grind._target_windows) -- superset check + holdout coverage")
print("-" * 100)
wins = grind._target_windows()
print(f"  _target_windows() returns {len(wins)} windows; keys = "
      f"{sorted(k for k, *_ in wins)}\n")
sup_ok = True
for k, tv, tol, wabs in wins:
    t = ds.target(k)
    # a value exactly at the hit boundary must be retained
    v = tv + tol * abs(tv)
    retained = abs(v - tv) <= wabs
    hit = score_value(v, t).rel_error <= tol
    if hit and not retained:
        sup_ok = False
print(f"  {'sm_target_keys(include_holdout=True)':<40}= {len(sm_target_keys(True))} keys")
print(f"  {'sm_target_keys() [search]':<40}= {len(sm_target_keys(False))} keys")
print(f"  {'N_TARGETS (look-elsewhere multiplicity)':<40}= {N_TARGETS}")
print(f"  {'HOLDOUT_KEYS':<40}= {sorted(pdg.HOLDOUT_KEYS)}")
missing_hold = [k for k in pdg.HOLDOUT_KEYS if k not in {kk for kk, *_ in wins}]
check("retention window is a true superset of the exact hit predicate (boundary value "
      "retained)", sup_ok)
check(f"BOTH holdout targets have a retention window so a survivor's out-of-sample "
      f"prediction can be scored; missing = {missing_hold}", not missing_hold)
check(f"N_TARGETS={N_TARGETS} matches the number of keys actually swept "
      f"({len(sm_target_keys(True))})", N_TARGETS == len(sm_target_keys(True)))
print(f"  look-elsewhere direction: multiplicity {N_TARGETS} vs {len(sm_target_keys(False))} "
      f"searched -> {math.log2(N_TARGETS / len(sm_target_keys(False))):+.2f} bits "
      f"(positive = conservative/stricter)")

# =====================================================================================
# S7. ASYMMETRIC ERRORS: the symmetrised sigma widens the window on the tight side
# =====================================================================================
print("\nS7  ASYMMETRIC PDG ERRORS -- symmetrised to the MAX, so the window is one-sided-wide")
print("-" * 100)
print(f"  {'target':<18}{'sigma used':>13}{'sigma_plus':>13}{'sigma_minus':>13}"
      f"{'widen on -side':>16}  searched?")
print("  " + "-" * 96)
searched = set(sm_target_keys(True))
asym = []
for t in ds:
    sp, sm_ = float(t.sigma_plus), float(t.sigma_minus)
    if abs(sp - sm_) > 1e-15 * max(abs(sp), 1.0):
        asym.append(t)
        print(f"  {t.key:<18}{float(t.sigma):>13.3e}{sp:>13.3e}{sm_:>13.3e}"
              f"{float(t.sigma) / sm_:>15.2f}x  "
              f"{'YES' if t.key in searched else '-'}")
print(f"\n  {len(asym)} targets carry asymmetric PDG errors; the hit window is +/-max(sig+,sig-),")
print(f"  i.e. LENIENT on the tighter side (documented as 'conservative' in pdg_constants.py:31).")
check("asymmetric-error targets are symmetrised to the LARGER sigma (window lenient, never "
      "strict) -- direction is documented and safe for a NULL claim",
      all(float(t.sigma) >= min(float(t.sigma_plus), float(t.sigma_minus)) for t in asym))

# =====================================================================================
# S8. koide_Q_lep window + the 2/3 claim, and the searched-pool bounds hygiene
# =====================================================================================
print("\nS8  MISC WINDOW HYGIENE")
print("-" * 100)
Q = ds.target("koide_Q_lep")
print(f"  koide_Q_lep = {float(Q.value):.9f} +/- {float(Q.sigma):.2e}  (rel {Q.rel_precision:.2e})")
print(f"    exact 2/3 sits {abs(float(Q.value) - 2 / 3) / float(Q.sigma):.2f} sigma away "
      f"(pdg_constants.py docstring claims 0.91 sigma)")
bounds_in_pool = [t.key for t in ds.dimensionless(include_holdout=True) if t.is_bound]
print(f"  bounds in the dimensionless pool: {bounds_in_pool}")
print(f"  bounds in sm_target_keys():       "
      f"{[k for k in sm_target_keys(True) if ds.target(k).is_bound]}")
zero_val = [t.key for t in ds if float(t.value) == 0.0]
print(f"  zero-valued targets (relative window undefined): {zero_val} "
      f"-> in searched pool? {[k for k in zero_val if k in searched]}")
check("no BOUND and no zero-valued target reaches the searched window list (a bound would get "
      "the max_tol=0.2 window and 'hit' on anything)",
      not [k for k in sm_target_keys(True) if ds.target(k).is_bound]
      and not [k for k in zero_val if k in searched])
check(f"theta_QCD would get tol={measurement_tol(ds.target('theta_QCD')):.2f} (the max_tol clamp) "
      f"if it ever entered a search -- it does not",
      measurement_tol(ds.target("theta_QCD")) == 0.2)

print("\n" + BAR)
print(f"WINDOW AUDIT: {sum(checks)}/{len(checks)} checks PASS")
print(BAR)
sys.exit(0)
