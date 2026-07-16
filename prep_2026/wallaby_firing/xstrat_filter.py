#!/usr/bin/env python3
"""
LANE W3 -- x-STRATIFIED MATCHED FILTER for the directional-EFE test
====================================================================
Banked 2026-07-16, BEFORE any WALLABY per-side data touches this file.

FIREWALL (applies to every number this script prints):
  At WALLABY scale (N~237 per-side-capable) the achieved sensitivity at AQUAL
  amplitude will be ~1-1.5 sigma (n=16 gave 0.32 sigma; sqrt(237/16)=3.85x).
  NEITHER pre-registered kill condition (3-sigma AQUAL-vs-BranchB separation,
  N~1157 canonical / ~1424 alt footing) can trigger at N~237. Kill-condition
  language appears here ONLY as "cannot trigger". Anything this filter returns
  on N~237 is EXPLORATORY.

============================ FROZEN STRATA ============================
Pre-declared BEFORE data. Ratio r = x/e = g_bar/g_ext (a0-independent; the
stratum assignment therefore does NOT move between the two a0 footings, but
DOES move between the two clustering brackets because e_N changes).

  DEEP        r <  1.0      banked-map sign REVERSED (attractor side SLOWER)
  TRANSITION  1.0 <= r < 5.0  positive sign, crossing-adjacent suppression +
                              the map's amplitude peak (peak at r ~ 2)
  OUTER       r >= 5.0      clean positive sign (attractor side FASTER),
                            amplitude monotone-declining in r

JUSTIFICATION (computed below from the banked laneA map, asserted at runtime):
The lane brief proposed deep: x < 2e. The banked A_fw_gamma0_pct map
(laneA_predictions_results.json, FROZEN repo) actually crosses zero at
  x*/e = 0.72 - 0.97  (four independent crossings on the banked grid:
   along e at x=0.2, 0.1, 0.05 -> x*/e = 0.81, 0.72, 0.75 [linear in e];
   along log-x at e=0.1, 0.2, 0.3 -> x*/e = 0.79, 0.76, 0.97),
so a deep boundary at 2e would MIX both predicted signs inside "deep".
ADJUSTED: the deep boundary is frozen at r = 1.0, the conservative outer
envelope of the banked crossings. The transition/outer boundary stays at
r = 5.0: by r ~ 5 the map is past its r~2 amplitude peak and sign-clean.
The banked verbal statement "attractor side faster for x >~ 2e" is the
same map: 2e sits inside TRANSITION where the sign is already positive.
=======================================================================

SIGN TRAP (must be re-verified on every new data source):
  PRE-REGISTERED convention: A_i = 2(v_rec - v_appr)/(v_rec + v_appr), tied to
  the RECEDING side, with psi measured from the RECEDING-side kinematic major
  axis, so p_i > 0 predicts attractor-side-FASTER for r >~ 2.
  WALLABY's perside_extractor.py pilot printout used the OPPOSITE ordering,
  A = 2(v_app - v_rec)/(v_app + v_rec). Any WALLABY feed into this filter MUST
  be converted (A_prereg = -A_extractor) and the conversion verified BY HAND on
  at least one galaxy from the raw mom1 map before a stratified number is
  quoted. A silent flip inverts the deep-stratum physics conclusion exactly.

WHAT THIS FILE BANKS:
  1. stratify(x, e): the frozen stratum assignment.
  2. Stratified matched filter: the identical pre-registered stack
     Ahat_S = sum_{i in S}(A_i p_i / s^2) / sum_{i in S}(p_i^2 / s^2)
     computed separately per stratum S, with the same bootstrap + isotropic-
     direction permutation null as the banked n=16 firing (reused verbatim by
     importing fire_aligned_n16; no re-implementation, no convention drift).
     E[Ahat_S] = 1 in EVERY stratum under AQUAL (the signed map already
     carries the reversal); = w = 0.304 (natural; 0.24 Cassini-max) in every
     stratum under Branch B; = 0 in every stratum under pure MI / null.
     The DEEP stratum is the discriminator: Ahat_deep > 0 requires the data
     to follow the REVERSED sign -- an MG fingerprint no isotropic systematic
     (and no rigid attractor-side-faster contaminant) can fake.
  3. Joint 2-parameter (amplitude alpha, reversal-depth beta) fit spec:
     model  A_i = alpha * p_i(beta),
     p_i(beta) = A_map(x_i, beta*e_i)/100 * G(gamma_i) * cos(psi_i),
     so beta rescales the effective external field and slides the crossing to
     x* ~ 0.8*beta*e. chi2(alpha,beta) = sum((A_i - alpha p_i(beta))^2)/s^2,
     alpha profiled analytically, beta on a frozen log grid [0.25, 4.0] x 33.
     Theory targets: AQUAL (alpha=1, beta=1); Branch B (alpha=w=0.304 natural
     / 0.24 Cassini-max, beta=1); pure MI (alpha=0, beta unidentified).
     beta is identifiable ONLY with deep+transition coverage; on an
     outer-dominated sample the beta profile is flat (reported, expected).

FOOTINGS (both, everywhere): a0 canonical 9.36e-11 (cH_Lambda/Z) primary,
alt 1.13e-10. Clustering brackets: Chae max-clustering (primary), no-clustering.

Smoke test: the banked n=16 aligned-firing sample (expected: nearly all OUTER
-- that is fine and is said out loud; the deep stratum is what WALLABY adds).
Exit 0.
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ALIGNED = "/Users/carlzimmerman/new_physics/prep_2026/aligned_firing"
DEFE = ("/Users/carlzimmerman/new_physics/zimmerman-formula/"
        "real_research/reviews/directional_efe_2026")

# ------------------------- FROZEN CONSTANTS (pre-data) -----------------------
R_DEEP = 1.0        # r = x/e below this: DEEP (reversed sign)
R_OUTER = 5.0       # r at/above this: OUTER (clean positive)
CROSSING_BRACKET = (0.70, 1.00)   # banked-map zero-crossings must land here
BETA_GRID = np.logspace(math.log10(0.25), math.log10(4.0), 33)  # frozen
W_NATURAL = 0.304   # Branch B suppression (banked laneA w_natural)
W_CASSINI = 0.24    # Branch B Cassini-max variant
STRATA = ("DEEP", "TRANSITION", "OUTER")

FIREWALL = ("FIREWALL: N~237 gives ~1-1.5 sigma at AQUAL amplitude; neither "
            "pre-registered kill condition (3-sigma AQUAL-vs-BranchB, N~1157 "
            "canonical / ~1424 alt) can trigger. EXPLORATORY only.")

SIGN_TRAP = ("SIGN TRAP: pre-registered A = 2(v_rec-v_appr)/(v_rec+v_appr) "
             "(receding side first); perside_extractor.py pilot used the "
             "OPPOSITE ordering -- convert (A_prereg = -A_extractor) and "
             "verify by hand on >=1 raw mom1 map before quoting any number.")


def stratify(x, e):
    """Frozen stratum assignment from r = x/e (a0-footing-independent)."""
    r = x / e
    if r < R_DEEP:
        return "DEEP"
    if r < R_OUTER:
        return "TRANSITION"
    return "OUTER"


# --------------- import the banked n=16 firing machinery verbatim ------------
def load_base():
    spec = importlib.util.spec_from_file_location(
        "fire_aligned_n16", os.path.join(ALIGNED, "fire_aligned_n16.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)   # module-level: loads banked map + sample
    return mod


BASE = load_base()
assert BASE.SIGN_BANKED == "attractor_side_faster"


# --------------- verify the frozen boundaries against the banked map ---------
def banked_crossings():
    """Zero-crossings x*/e of the banked A_fw map, both grid directions:
    linear in e along each x-row (the interpolator's e-rule), linear in log x
    down each e-column (the interpolator's x-rule)."""
    with open(os.path.join(DEFE, "laneA_predictions_results.json")) as f:
        d = json.load(f)
    E, X = d["E_GRID"], sorted(d["X_GRID"])
    M = {float(k): v for k, v in d["A_fw_gamma0_pct"].items()}
    out = []
    for x in X:                      # along e at fixed x
        row = M[x]
        for k in range(len(E) - 1):
            a, b = row[k], row[k + 1]
            if a > 0 > b:
                e_star = E[k] + (E[k + 1] - E[k]) * a / (a - b)
                out.append(("along_e", x, x / e_star))
    for j, e in enumerate(E):        # along log-x at fixed e
        colv = [M[x][j] for x in X]
        for k in range(len(X) - 1):
            a, b = colv[k], colv[k + 1]
            if b > 0 > a:            # X ascending: negative below, positive above
                t = -a / (b - a)     # fraction from X[k] toward X[k+1], log space
                x_star = math.exp(math.log(X[k]) +
                                  t * (math.log(X[k + 1]) - math.log(X[k])))
                out.append(("along_logx", e, x_star / e))
    return out


CROSSINGS = banked_crossings()
_ratios = [r for _, _, r in CROSSINGS]
assert _ratios, "banked map shows no sign reversal?!"
assert all(CROSSING_BRACKET[0] <= r <= CROSSING_BRACKET[1] for r in _ratios), (
    f"banked crossings {_ratios} escape the frozen bracket {CROSSING_BRACKET};"
    " the frozen R_DEEP=1.0 justification would be void -- STOP")


# ----------------------- the stratified matched filter -----------------------
def stratified_fire(rows, a0, ebr, sig, nboot=4000, nperm=4000):
    """Per-stratum Ahat via the banked run_config (verbatim import). Strata
    with n<2 are reported EMPTY/UNDERSIZED, no number fabricated."""
    buckets = {s: [] for s in STRATA}
    for r in rows:
        x = r["gbar"] / a0
        leN = r["leN_max"] if ebr == "maxclu" else r["leN_no"]
        e = 10.0 ** leN * BASE.GDAGGER_CHAE / a0
        buckets[stratify(x, e)].append(r)
    out = {}
    for s in STRATA:
        b = buckets[s]
        if len(b) < 2:
            out[s] = dict(n=len(b), status="EMPTY" if not b else "UNDERSIZED",
                          names=[r["name"] for r in b])
            continue
        res = BASE.run_config(b, a0, ebr, sig, nboot=nboot, nperm=nperm)
        res["status"] = "OK"
        res["names"] = [r["name"] for r in b]
        out[s] = res
    return out


# ------------------- joint (amplitude, reversal-depth) fit --------------------
def joint_fit(rows, a0, ebr, sig):
    """chi2(alpha, beta) with alpha profiled analytically per frozen beta-grid
    point. Returns the profile + best point + delta-chi2 to the theory targets.
    On an outer-dominated sample the beta profile is expected FLAT."""
    A = np.array([r["A"] for r in rows])
    prof = []
    for beta in BETA_GRID:
        p = np.empty(len(rows))
        for i, r in enumerate(rows):
            x = r["gbar"] / a0
            leN = r["leN_max"] if ebr == "maxclu" else r["leN_no"]
            e = 10.0 ** leN * BASE.GDAGGER_CHAE / a0
            Apct, _ = BASE.A_aqual_pct(x, beta * e)
            p[i] = (Apct / 100.0) * r["Ggam"] * math.cos(math.radians(r["psi"]))
        sp2 = float(np.sum(p * p))
        alpha = float(np.sum(A * p) / sp2) if sp2 > 0 else np.nan
        chi2 = float(np.sum((A - alpha * p) ** 2) / sig ** 2)
        # chi2 at the fixed theory amplitudes (beta as given)
        chi2_t = {name: float(np.sum((A - a_th * p) ** 2) / sig ** 2)
                  for name, a_th in (("AQUAL_alpha1", 1.0),
                                     ("BranchB_w_natural", W_NATURAL),
                                     ("BranchB_w_cassini", W_CASSINI),
                                     ("pureMI_alpha0", 0.0))}
        prof.append(dict(beta=float(beta), alpha_hat=alpha,
                         sig_alpha=float(sig / math.sqrt(sp2)) if sp2 > 0
                         else np.nan,
                         chi2=chi2, chi2_theory=chi2_t))
    best = min(prof, key=lambda q: q["chi2"])
    chi2_span = max(q["chi2"] for q in prof) - best["chi2"]
    return dict(profile=prof, best=best,
                beta_profile_span_dchi2=float(chi2_span),
                beta_identifiable=bool(chi2_span > 1.0),
                note=("beta profile flat (span dchi2 <= 1): reversal depth "
                      "unconstrained -- expected on an outer-dominated sample"
                      if chi2_span <= 1.0 else
                      "beta carries information (span dchi2 > 1)"))


# --------------------------------- smoke test ---------------------------------
def main():
    W = 88
    print("=" * W)
    print("LANE W3: x-STRATIFIED MATCHED FILTER -- bank + n=16 smoke test")
    print(FIREWALL)
    print(SIGN_TRAP)
    print("=" * W)

    print("\n[frozen strata]  DEEP r<%.1f | TRANSITION %.1f<=r<%.1f | OUTER "
          "r>=%.1f   (r = x/e = g_bar/g_ext)" % (R_DEEP, R_DEEP, R_OUTER,
                                                 R_OUTER))
    print("[banked-map zero-crossings, computed from the frozen JSON]")
    for kind, at, ratio in CROSSINGS:
        lab = "x=%.2f" % at if kind == "along_e" else "e=%.2f" % at
        print(f"  {kind:<11} {lab:<7} x*/e = {ratio:.3f}")
    print(f"  all inside the frozen bracket {CROSSING_BRACKET} -> R_DEEP=1.0 "
          f"(conservative envelope) VERIFIED; the lane-brief 2e boundary was "
          f"ADJUSTED (2e would mix signs inside DEEP)")
    print("[sign predictions per stratum]  (E[Ahat_S]; signed map carries the "
          "reversal, so Ahat_S=+1 in DEEP means the data FOLLOWS the reversal)")
    print("  theory        DEEP(r<1)              TRANSITION          OUTER")
    print("  AQUAL/QUMOND  +1 (attr side SLOWER)  +1 (suppressed amp) +1 (attr side FASTER)")
    print("  Branch B      +0.30 (0.24 Cass-max)  +0.30               +0.30  (same reversal, w-suppressed)")
    print("  pure MI       0                      0                   0")
    print("  isotropic systematic: cannot produce the DEEP sign flip (MG fingerprint)")

    sample = BASE.sample
    n = len(sample)
    print(f"\n[smoke test] banked n={n} aligned-firing sample "
          f"(sigma_A = {BASE.SIG_A:.4f}, pre-registered convention -- this "
          f"sample is WHISP-derived and already convention-correct; the sign "
          f"trap applies to FUTURE WALLABY feeds)")

    results = {}
    for fn, a0 in BASE.FOOTINGS.items():
        for ebr in BASE.EBRACKETS:
            key = f"{fn} | {ebr}"
            strat = stratified_fire(sample, a0, ebr, BASE.SIG_A)
            results[key] = strat
            counts = {s: strat[s].get("n", 0) for s in STRATA}
            print(f"\n  config: {key}   stratum counts {counts}")
            for s in STRATA:
                r = strat[s]
                if r.get("status") != "OK":
                    print(f"    {s:<11} n={r['n']}  {r['status']} -- no "
                          f"number fabricated ({', '.join(r['names']) or '-'})")
                else:
                    print(f"    {s:<11} n={r['n']:>2}  Ahat={r['Ahat']:+7.2f} "
                          f"boot_sd={r['boot_std']:6.2f} "
                          f"sig_an={r['sig_analytic']:6.2f} Z={r['Z']:+5.2f} "
                          f"p2={r['p_perm_two']:.3f}")

    print("\n[joint 2-parameter (alpha, beta) fit -- spec exercised on n=16]")
    print("  model A_i = alpha * p_i(beta), p_i(beta) uses A_map(x, beta*e); "
          "crossing slides to x* ~ 0.8*beta*e")
    print("  targets: AQUAL(1,1); BranchB(0.304 nat / 0.24 Cass-max, 1); "
          "pureMI(0, beta unidentified)")
    fits = {}
    for fn, a0 in BASE.FOOTINGS.items():
        for ebr in BASE.EBRACKETS:
            key = f"{fn} | {ebr}"
            f = joint_fit(sample, a0, ebr, BASE.SIG_A)
            fits[key] = f
            b = f["best"]
            print(f"  {key:<38} alpha_hat={b['alpha_hat']:+.2f}"
                  f"+-{b['sig_alpha']:.2f} @ beta={b['beta']:.2f}  "
                  f"beta-span dchi2={f['beta_profile_span_dchi2']:.3f}  "
                  f"[{f['note'].split(':')[0]}]")

    out = dict(
        FIREWALL=FIREWALL, SIGN_TRAP=SIGN_TRAP,
        frozen=dict(R_DEEP=R_DEEP, R_OUTER=R_OUTER,
                    crossing_bracket=CROSSING_BRACKET,
                    beta_grid=[float(b) for b in BETA_GRID],
                    w_natural=W_NATURAL, w_cassini=W_CASSINI),
        banked_crossings=[dict(kind=k, at=a, x_over_e=r)
                          for k, a, r in CROSSINGS],
        smoke_n=n, stratified=results, joint_fit=fits,
        conventions=dict(BASE_IMPORT="fire_aligned_n16.py verbatim (predictor,"
                         " stack, permutation null, sample, noise)",
                         A="2(v_rec-v_appr)/(v_rec+v_appr) [pre-registered]"),
    )
    with open(os.path.join(HERE, "xstrat_filter_results.json"), "w") as fjs:
        json.dump(out, fjs, indent=1)
    print(f"\n  results JSON -> "
          f"{os.path.join(HERE, 'xstrat_filter_results.json')}")
    print("=" * W)
    print("LANE W3 BANKED (exit 0): strata frozen from the banked map's own "
          "zero-crossing; smoke test = outer-dominated as expected; kill "
          "conditions CANNOT TRIGGER at N~237.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
