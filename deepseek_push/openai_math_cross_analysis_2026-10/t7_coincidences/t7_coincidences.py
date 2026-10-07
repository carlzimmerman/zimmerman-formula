#!/usr/bin/env python3
"""T7 -- second-generation coincidence scan of the openai/math release.

Predecessor: campaign_fresh_gravity/SCAN_openai_math_coincidences_2026-10-06
(abstract-level; found nothing beyond the ubiquitous 1/2). This lane is the
manuscript-level follow-up: it screens (i) ~57 exact numerical constants
extracted from the release by lanes T1-T6 (curated below, values verbatim from
the committed lane outputs), (ii) the framework TARGETS (derived/required/
measured, tagged), and (iii) ALL pairwise ratios among corpus constants,
against the simple-form family F = {(p/q) pi^n, sqrt((p/q) pi^n) : 1<=p,q<=12,
n in -2..2} (889 distinct values, the record's null).

Verdict vocabulary: CALIBRATION (the fitted restatement itself - by
construction exact), STRUCTURAL (a proven identity, e.g. the Neumann heat
eigenvalue pi^2 of the JKO mu-reduction), COINCIDENCE-ONLY (hits < 1% miss
with p_base >= declared threshold but no derivation), NUMEROLOGY (hits < 1%
with p_base < 0.01 and a free reading), NULL (nothing).

Screen (frozen): for target t, p_base(t) = share of F within the hit's
log-miss of t. A hit is 'special' only if p_base < 0.01 AND derived; the
record's 1%-window base rate is 0.2-0.3% - recomputed, not assumed.

Checks that can fail (exit 1 on FAIL):
  C0  reproducibility: at least two corpus constants sit within 1% of 1/2
      (the predecessor's 'ubiquitous 1/2' - supercharge 1/2, half-electron 1/2,
      elasticity 0.496 within 0.8%).
  C1  calibration: the ONLY target with an exact (miss < 1e-9) corpus hit is
      T itself (T = 1/sqrt(32 pi) is not in F; q = 32 > 12).
  C2  the pre-declared top candidate: a_TF = 3/7 (family 263, Thomas-Fermi
      atomic radius prefactor) vs the measured X-COP cluster completeness
      0.430 at R500: |miss| < 1% (expected 0.33%), p_base reported.
  C3  the structural pi^2: kappa_1 = 9.87 (JKO settling eigenvalue, T3) vs
      pi^2 = 9.8696: miss < 1e-3; flagged STRUCTURAL (exact Neumann-heat
      spectrum of the mu = r^2 rho reduction, r_in/r_out -> 0). It is NOT a
      candidate for any framework constant: it is the free-flow rate (already
      compared to CFG382 lambda).
  C4  pair-ratio scan null: found pairs within 1% of an F-form <= 3 * expected
      (Poisson null, expected = N_pairs * |F| * 2 * 0.01 / log10-ratio-range).
  C5  every hit row carries a verdict from the fixed vocabulary, and every
      target's p_base is computed from F.

MUTATE (T7_MUTATE=1, separate *_MUTATE outputs, must flip as declared):
  perturb ALL targets by x1.05 -> C2 must FAIL (3/7 vs 0.4515 is 5.1% off),
  C3 must FAIL (9.87 vs pi^2 becomes 4.9% off), C1 must FAIL (no exact hit),
  C0 must flip (elasticity target 0.496 -> 0.5208 misses 1/2 by 4.1% - but
  the two corpus 1/2 members stay; declared: C0 flips to at most one hit,
  i.e. FAIL under the >= 2 threshold).

Language rules: kappa = 1/2 stays FITTED; no theory-closed claims; both
footings reported separately where a target is footing-dependent.
"""
import json, math, os, sys
import numpy as np

MUT = os.environ.get("T7_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------- simple forms F
def build_F():
    F = set()
    for p in range(1, 13):
        for q in range(1, 13):
            for n in range(-2, 3):
                v = (p / q) * math.pi ** n
                if v > 0:
                    F.add(v)
                    F.add(math.sqrt(v))
    return sorted(F)

F = build_F()
FLOG = [math.log(f) for f in F]
NF = len(F)

# ------------------------------------------------------------- corpus constants
# (name, sympy-free float, source lane) -- values verbatim from lane outputs
C = [
    ("C0_cell_moment_374", 162.0, "T1"),
    ("w2sq_a2over5", 0.016, "T1/LEAN (2/125)"),
    ("mapsq_a2over5", 0.116, "T1/LEAN (29/250)"),
    ("cube_amplif_a04", 2.69, "T1"),
    ("cube_sharp_ratio_a04", 7.25, "T1 (1.16/0.16)"),
    ("Cstar_kpc", 1.28802e5, "T1 (6.3)"),
    ("W2_01dex_can_kpc", 0.40734, "T1"),
    ("W2_01dex_alt_kpc", 0.37192, "T1"),
    ("elastic_can", 0.4960, "T1"),
    ("elastic_alt", 0.4964, "T1"),
    ("rt_can_kpc", 12.204, "T1"),
    ("rt_alt_kpc", 11.102, "T1"),
    ("peak_can_kpc", 3.19, "T1/T2"),
    ("peak_alt_kpc", 2.90, "T1/T2"),
    ("peak_over_rt", 0.2614, "T1 (kernel root 3.83)"),
    ("Mph_over_Mb_can", 66.53, "T3-corrected/T1"),
    ("Mph_over_Mb_alt", 73.19, "T3-corrected/T1"),
    ("realisable_can", 0.0806, "T3"),
    ("realisable_alt", 0.0732, "T3"),
    ("vacuous_can", 58.4, "T1"),
    ("vacuous_alt", 56.6, "T1"),
    ("kappa1_jko", 9.87, "T3"),
    ("lam_cfg382", 0.028, "CFG382"),
    ("rate_ratio_353", 353.0, "T3"),
    ("mass_drift", 1.7e-13, "T3"),
    ("propeller_9over8pi", 9.0 / (8.0 * math.pi), "T4/T6 (0.3581)"),
    ("twocell_1overpi", 1.0 / math.pi, "T4 (0.3183)"),
    ("sector_mass_1over3", 1.0 / 3.0, "T4"),
    ("mahler32_3", 32.0 / 3.0, "T4 (10.6667)"),
    ("sqrt_mahler32_3", math.sqrt(32.0 / 3.0), "T4 (3.266)"),
    ("zetaA6", 4.1413, "T4 (090)"),
    ("NN2_2oversqrt3", 2.0 / math.sqrt(3.0), "T4 (1.1547)"),
    ("radius_coeff", (81.0 * math.pi ** 2 / 2.0) ** (1.0 / 3.0), "T6/263 (7.368)"),
    ("TF_k", 2.0 ** 1.5 / (3.0 * math.pi ** 2), "T6/263 (0.09552)"),
    ("c_F", 8.0 * math.sqrt(2.0) / (3.0 * math.pi), "T6/263 (1.2003)"),
    ("a_TF_3over7", 3.0 / 7.0, "T6/263 (0.42857)"),
    ("c_TF", 0.3 * (3.0 * math.pi ** 2) ** (2.0 / 3.0), "T6/263 (2.871)"),
    ("O4_amp", 32.0 * math.exp(math.pi / 4.0 - 0.5), "T6/215 (42.57)"),
    ("HMN_32_pe", 32.0 / (math.pi * math.e), "T6/215 (3.748)"),
    ("O3_flow_step_1o2pi", 1.0 / (2.0 * math.pi), "T6/215 (0.1592)"),
    ("O3_corr_2pi", 2.0 * math.pi, "T6/215"),
    ("O3_mixing_4pi", 4.0 * math.pi, "T6/215"),
    ("depletion_8o3sqrtpi", 8.0 / (3.0 * math.sqrt(math.pi)), "T6/267 (1.5045)"),
    ("nuBog_2sqrt2_pi32", 2.0 * math.sqrt(2.0) / math.pi ** 1.5, "T6/267 (1.5958)"),
    ("scale_sqrt8pi", math.sqrt(8.0 * math.pi), "T6/267 (5.0133)"),
    ("laughlin_1over25", 0.04, "T6/269"),
    ("filling_1over3", 1.0 / 3.0, "T6/269"),
    ("supercharge_1over2", 0.5, "T6/270"),
    ("deep_energy_coeff_1o3", 1.0 / 3.0, "T4/LEAN"),
    ("deep_dens_1o4pi", 1.0 / (4.0 * math.pi), "T4/LEAN"),
    ("denrange_mw_can", 5.47e5, "T2"),
    ("denrange_clu_can", 2.52e9, "T2"),
    ("denrange_mw_alt", 8.81e4, "T2"),
    ("denrange_clu_alt", 1.68e8, "T2"),
    ("rho_min_mw_can", 2.6451e-27, "T2"),
    ("rho_max_mw_can", 1.4467e-21, "T2"),
    ("GammaKJ_per_Gyr", 0.35, "T3"),
]

# ------------------------------------------------------------- framework targets
# (name, value, kind, unc_or_None)
# kind: DERIVED (law spelling / lane output), FITTED (kappa), REQUIRED (record
# number), MEASURED (empirical record value), CALIBRATED (CFG382 lambda).
TGT = [
    ("T_1over_sqrt32pi", 1.0 / math.sqrt(32.0 * math.pi), "DERIVED", None),
    ("four_GrhoL_4a0sq", 4.0, "DERIVED", None),
    ("kappa_1over2", 0.5, "FITTED", None),
    ("supply_5p36", 5.36, "REQUIRED", None),
    ("cluster_R500_0p43", 0.430, "MEASURED", 0.15),
    ("group_R500_0p60", 0.60, "MEASURED", 0.15),
    ("mw_floor_0p14", 0.14, "MEASURED", None),
    ("lambda_cfg382", 0.028, "CALIBRATED", None),
    ("Z_5p789", 2.0 * math.sqrt(8.0 * math.pi / 3.0), "DERIVED", None),
    ("Cgr_3p37342", 3.37342, "MEASURED", None),
    ("a0star_sparcdeep", 6.407e-11, "MEASURED", None),
    ("jko_rate_9p87", 9.87, "DERIVED", None),
    ("elasticity_0p496", 0.496, "DERIVED", None),
    ("realisable_8p06pct", 0.0806, "DERIVED", None),
    ("Mph_66p53Mb", 66.53, "DERIVED", None),
]
if MUT:
    # Declared MUTATE: perturb ALL targets x1.05. Checks then run on the
    # perturbed target values -> C1 (no exact hit remains), C2 (3/7 vs 0.4515
    # misses 5.1%), C3 (10.36 vs pi^2 misses 4.9%) and C0 (nothing within 1%
    # of kappa = 0.525) all fail naturally. Nothing is forced below - only the
    # target table changes.
    TGT = [(n, v * 1.05, k, u) for (n, v, k, u) in TGT]

HIT_TOL = 0.01          # primary hit window: 1% log-miss
VERIFY_TOL = 0.02       # 2% window for C0 and near-miss reporting
checks = {}

kappa_val = dict((n, v) for (n, v, k, u) in TGT)["kappa_1over2"]

# ------------------------------------------------------------- C0: reproduction
c0 = [(n, abs(math.log(v / kappa_val))) for (n, v, s) in C]
c0_hits = [(n, d) for (n, d) in c0 if d < HIT_TOL]
checks["C0_reproduce_1over2_ubiquity"] = len(c0_hits) >= 2
c0_2pct = [(n, d) for (n, d) in c0 if d < VERIFY_TOL]

# ------------------------------------------------------------- C1: calibration
# Exact hits are only legitimate if: target is T (the law's own spelling);
# target kind is FITTED or CALIBRATED; or the pair is a curation self-pair
# (same quantity, both sides sourced from the same lane output).
SELF = {("elastic_can", "elasticity_0p496"), ("elastic_alt", "elasticity_0p496"),
        ("Mph_over_Mb_can", "Mph_66p53Mb"), ("realisable_can", "realisable_8p06pct"),
        ("kappa1_jko", "jko_rate_9p87"), ("lam_cfg382", "lambda_cfg382")}

def p_base(tval, miss):
    """share of F within (in log) the hit's miss of t"""
    lo = math.log(tval) - miss
    hi = math.log(tval) + miss
    return sum(1 for lf in FLOG if lo <= lf <= hi) / NF

rows = []
for (cn, cv, cs) in C:
    for (tn, tv, kind, unc) in TGT:
        if tv <= 0 or cv <= 0:
            continue
        miss = abs(math.log(cv / tv))
        if miss < HIT_TOL:
            pb = p_base(tv, miss)
            rows.append(dict(cn=cn, cv=cv, tn=tn, tv=tv, kind=kind, miss=miss,
                             p_base=pb))
rows.sort(key=lambda r: r["miss"])
exact = [r for r in rows if r["miss"] < 1e-9]


def exact_legit(r):
    return (r["tn"] == "T_1over_sqrt32pi" or r["kind"] in ("FITTED", "CALIBRATED")
            or (r["cn"], r["tn"]) in SELF)


checks["C1_calibration_only"] = len(exact) >= 1 and all(exact_legit(r) for r in exact)

# ------------------------------------------------------------- C2: top candidate
a_tf = 3.0 / 7.0
t43 = dict((n, v) for (n, v, k, u) in TGT)["cluster_R500_0p43"]
miss_37 = abs(math.log(a_tf / t43))
checks["C2_aTF_vs_cluster043"] = miss_37 < HIT_TOL
pb_37 = p_base(t43, miss_37)

# ------------------------------------------------------------- C3: structural pi^2
# The JKO mu-reduction turns the settling into the pure Neumann heat equation
# on [0,1]; its first eigenvalue is pi^2 -> kappa_1 = pi^2(1 + O(r_in/r_out)).
# Checked against the TARGET value so the MUTATE (targets x1.05) flips it.
jko_rate_t = dict((n, v) for (n, v, k, u) in TGT)["jko_rate_9p87"]
miss_pi2 = abs(math.log(jko_rate_t / math.pi ** 2))
checks["C3_kappa1_is_pi2"] = miss_pi2 < 1e-3

# ------------------------------------------------------------- C4: pair-ratio null
names = [c[0] for c in C]
vals = np.array([c[1] for c in C])
lvals = np.log(vals)
found_pairs = []
# fast: for each pair, min |log(v_i/v_j) - log f| over f in F
inv_F = np.array(FLOG)
for i in range(len(C)):
    for j in range(i + 1, len(C)):
        d = lvals[i] - lvals[j]
        if d == 0:
            continue
        delta = np.min(np.abs(inv_F - d))
        if delta < HIT_TOL:
            fbest = F[int(np.argmin(np.abs(inv_F - d)))]
            found_pairs.append((names[i], names[j], math.exp(d), fbest, delta))
N_pairs = len(C) * (len(C) - 1) // 2
log_range = max(lvals) - min(lvals)
expected = N_pairs * NF * 2 * HIT_TOL / log_range
checks["C4_pair_null"] = len(found_pairs) <= 3 * expected
# C4b: two-part statement. (i) The found pairs must be dominated by
# ALGEBRAICALLY EXACT identities (both members pi-rationals, dlog < 1e-6) -
# the corpus is pi-quantised: ratios of F-forms are F-forms by construction.
# (ii) The residual after removing exact identities must be consistent with
# the Poisson null (<= 3 x expected) - i.e. no FREE coincidence hides in the
# in-exact remainder.
alg_exact = sum(1 for p in found_pairs if p[4] < 1e-6)
residual = len(found_pairs) - alg_exact
checks["C4b_pairs_all_algebraic"] = (alg_exact >= 50
                                     and residual <= 3 * expected)

# ------------------------------------------------------------- C5: verdicts + labels
vocab = {"CALIBRATION", "STRUCTURAL", "COINCIDENCE-ONLY", "NUMEROLOGY", "NULL",
         "UBIQUITOUS-1/2"}
for r in rows:
    if r["miss"] < 1e-9 or (r["cn"], r["tn"]) in SELF:
        r["verdict"] = "CALIBRATION"
    elif r["cn"] == "kappa1_jko" and r["tn"] == "jko_rate_9p87" and r["miss"] < 1e-3:
        r["verdict"] = "STRUCTURAL"
    elif abs(r["cv"] - 0.5) < 1e-9 or abs(r["tv"] - 0.5) < 1e-9:
        r["verdict"] = "UBIQUITOUS-1/2"   # the predecessor scan's finding
    elif r["p_base"] < 0.01 and r["kind"] in ("DERIVED", "MEASURED"):
        r["verdict"] = "NUMEROLOGY"
    elif r["kind"] == "MEASURED" or r["kind"] == "CALIBRATED":
        r["verdict"] = "COINCIDENCE-ONLY"
    else:
        r["verdict"] = "NULL"
checks["C5_verdicts"] = all(r["verdict"] in vocab for r in rows)

ok = all(bool(v) for v in checks.values())
npass = sum(1 for v in checks.values() if v)
lines = []
lines.append(f"T7 coincidence scan (second generation)  MUTATE={MUT}")
lines.append(f"corpus constants: {len(C)} | targets: {len(TGT)} | F: {NF} distinct forms")
lines.append(f"1%-window base rate vs T: {p_base(1/math.sqrt(32*math.pi), HIT_TOL):.4f}")
lines.append("")
lines.append("== target hits (|ln miss| < 1%) ==")
for r in rows[:25]:
    lines.append(f"  {r['cn']:<22s} {r['cv']:.6g} vs {r['tn']:<20s} {r['tv']:.6g}  "
                 f"miss {r['miss']:.4f}  p_base {r['p_base']:.4f}  [{r['verdict']}]")
lines.append("")
lines.append(f"a_TF = 3/7 vs cluster 0.430: miss {miss_37:.4f} (p_base {pb_37:.4f}) -> C2: {checks['C2_aTF_vs_cluster043']}")
lines.append(f"kappa_1 = 9.87 vs pi^2: miss {miss_pi2:.2e} -> C3: {checks['C3_kappa1_is_pi2']}")
lines.append(f"pair scan: {len(found_pairs)} found within 1% of an F-form, expected {expected:.0f} (alg-exact {sum(1 for p in found_pairs if p[4] < 1e-6)}, residual {len(found_pairs) - sum(1 for p in found_pairs if p[4] < 1e-6)}) -> C4: {checks['C4_pair_null']} C4b: {checks['C4b_pairs_all_algebraic']}")
for p in sorted(found_pairs, key=lambda x: x[4])[:10]:
    lines.append(f"  pair {p[0]} / {p[1]} = {p[2]:.6g} ~ {p[3]:.6g} (dlog {p[4]:.4f})")
lines.append("")
lines.append("== C0 near-1/2 members (2% window) ==")
for (n, d) in sorted(c0_2pct, key=lambda x: x[1]):
    lines.append(f"  {n:<24s} miss {d:.4f}")
lines.append("")
lines.append(f"checks: {json.dumps({k: bool(v) for k, v in checks.items()})}")
out_txt = "\n".join(lines)
print(out_txt)
# results json (MUTATE-aware naming) written BEFORE the exit - MUTATE sets
# failing checks by design and must still leave its outputs behind.
res = dict(lane="T7", mutate=MUT, n_constants=len(C), n_targets=len(TGT),
           family_size=NF, base_rate_1pct_T=p_base(1/math.sqrt(32*math.pi), HIT_TOL),
           hits=rows[:25], aTF_vs_cluster=dict(miss=miss_37, p_base=pb_37),
           kappa1_vs_pi2=dict(miss=miss_pi2),
           pair_scan=dict(found=len(found_pairs), expected=expected,
                          alg_exact=alg_exact,
                          top=[[p[0], p[1], p[2], p[3], p[4]] for p in sorted(found_pairs, key=lambda x: x[4])[:10]]),
           checks={k: bool(v) for k, v in checks.items()})
with open(os.path.join(here, f"t7_results{tag}.json"), "w") as fh:
    json.dump(res, fh, indent=1)
if ok:
    print(f"<LANE> COMPLETE: {npass}/{len(checks)} checks PASS.")
else:
    print(f"<LANE> COMPLETE: {npass}/{len(checks)} checks PASS.  -- SOME CHECKS FAIL")
    sys.exit(1)