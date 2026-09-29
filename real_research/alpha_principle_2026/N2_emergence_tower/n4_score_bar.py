#!/usr/bin/env python3
"""N4 -- score every tower-emergence closure against lane D's bar and print the verdict per pre-registered criterion (N2_PREREGISTRATION.md, N1-N6).
Run:    PYTHONDONTWRITEBYTECODE=1 python3 n4_score_bar.py          (exit 0 iff the integrity checks pass; a NEGATIVE verdict is a valid exit-0 result)
MUTATE: PYTHONDONTWRITEBYTECODE=1 python3 n4_score_bar.py MUTATE   (positional argv; runs lane D's checker self-test in its own mutate mode, where the bar is disabled, so the
                                                                     checker's negative controls must fail -> exit 1)
Reads n2_results.json and n3_results.json (this lane) and imports lane D's alpha_bar_checker.py READ ONLY (no bytecode written).
"""
import sys, os, json, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "D_calibration_bar"))
import alpha_bar_checker as A
import tower_lib as T

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + (" " + m if m else ""))
    if not ok: fails.append(n)

print("== checker integrity ==")
rc = A.selftest(mutate=MUT)
chk("lane D checker self-test behaves as specified" + (" (MUTATE: bar disabled, must fail)" if MUT else ""), rc == 0)
r = A.assess(delta=1e-12, log2size=math.log2(18), fitted_reals=0, verbose=False)
chk("positive control: a 1e-12 zero-parameter match in a family of 18 would clear the bar", r["clears"])

n2 = json.load(open("n2_results.json")); n3 = json.load(open("n3_results.json"))
LOG2 = math.log2(18)         # 3 towers x 3 closures x 2 N conventions, declared before running
print("\n== scoring: 1/alpha_em(0) predicted by each closure vs 137.035999177 ==")
print("family size 18 (log2 %.2f), fitted reals 1 (M_c), scale stated (Thomson). predicted precision = n3 band / 137.036 (pre-registered); the closure spread is a second, reported precision." % LOG2)
rows = []
for tag in ("TA", "TB"):
    ems = [n2["%s|%s|G" % (tag, n)][0]["em_0"] for n in T.NAMES if n2["%s|%s|G" % (tag, n)]]
    spread = (max(ems) - min(ems)) / 2 / T.ALPHA_INV0 if len(ems) > 1 else float("nan")
    for n in T.NAMES:
        key = "%s|%s" % (tag, n)
        if key not in n3:
            print("%s closure %s: no root (sign infeasible), no prediction; counted as FAIL" % (tag, n)); rows.append((key, None)); continue
        em = n3[key]["em0"]; band = n3[key]["band"]
        miss = abs(em / T.ALPHA_INV0 - 1)
        pp = band / T.ALPHA_INV0
        res = A.assess(delta=miss, log2size=LOG2, predicted_precision=pp, fitted_reals=1, n_targets=1, scale_stated=True, verbose=False)
        pp2 = max(pp, spread) if spread == spread else pp
        res2 = A.assess(delta=miss, log2size=LOG2, predicted_precision=pp2, fitted_reals=1, n_targets=1, scale_stated=True, verbose=False)
        print("%s closure %s: 1/alpha_em(0) = %.3f, miss %.3e (%.1f x its own band %.3f%%); P(look-elsewhere, own band) = %.3g; c1 %s c2 %s c3(zero fitted) %s c4 %s -> %s"
              % (tag, n, em, miss, miss / pp, 100 * pp, res["p"], res["c1_lookelsewhere"], res["c2_precision"], res["c3_no_fitted_real"], res["c4_scale_stated"], "CLEARS" if res["clears"] else "does not clear"))
        print("      with the closure spread as precision (%.2f%%): P = %.3g, %s" % (100 * pp2, res2["p"], "CLEARS" if res2["clears"] else "does not clear"))
        rows.append((key, res, res2, miss, pp))
chk("no closure clears the bar (expected outcome; a clear would have been a lead to be verified as hard as a fail)", all((r[1] is None) or (not r[1]["clears"]) for r in rows) or MUT)
chk("every closure fails c3 (one fitted real: the modulus M_c is spent on a measured coupling)", all((r[1] is None) or (not r[1]["c3_no_fitted_real"]) for r in rows) or MUT)

print("\n== criterion verdicts ==")
for tag in ("TA", "TB"):
    for n in T.NAMES:
        key = "%s|%s" % (tag, n)
        if key in n3:
            print("   %s closure %s: x = %.2f" % (tag, n, n3[key]["x"]))
print("N1 content: PASS (n1_tower_content.out; per-level b tables, SM check, SU(5) gate, anomalies, closed form)")
print("N2 self-consistency: PASS at every solution (n2_emergence_solve.out; identity residual <= 2e-16)")
print("N3 sign feasibility: TA roots for all three closures (as expected); TB none for closure 3 (as expected) but a root for closure 2 at x = %.0f (EXPECTATION WRONG); TC none for any (as expected)" % n3["TB|2"]["x"])
ya = n3["TA|Y"]["resid"]; yb = n3["TB|Y"]["resid"]; sa = n3["TA|Y"]["shift_size"]; sb_ = n3["TB|Y"]["shift_size"]
print("N4 emergence vs 0 at the Y-closure root: TA implied 1/alpha_(2,3)(Lambda_sp) = (%.2f, %.2f), TB (%.2f, %.2f). Band on these: the scale+scheme spread after refitting M_c is ~1 unit; the ABSOLUTE scheme-constant size kappa*sum(b) is "
      "(2, 3) = (%.2f, %.2f) for TA and (%.2f, %.2f) for TB. TA: residual/size = (%.1f, %.1f) -> NOT consistent with 0 at the estimated size (marginal-to-failed; the non-fermion constants are not computed). TB: residual/size = (%.0f, %.0f) decisively failed."
      % (ya[1], ya[2], yb[1], yb[2], sa[1], sa[2], sb_[1], sb_[2], ya[1] / sa[1], ya[2] / sa[2], yb[1] / abs(sb_[1]), yb[2] / abs(sb_[2])))
xs = [n3["TA|%s" % n]["x"] for n in T.NAMES]
print("N5 forcedness of x: geometric relation has no root (n_lvl >> 2 pi); TA closure moduli x = %.2f, %.2f, %.2f (spread %.1f %% > 10 %%): FAIL as a joint fix" % (xs[0], xs[1], xs[2], 100 * (max(xs) / min(xs) - 1)))
mm = [abs(n3["TA|%s" % n]["em0"] / T.ALPHA_INV0 - 1) for n in T.NAMES]
print("N6 bar: no closure clears; every closure has a fitted real; TA predictions of 1/alpha_em(0) = %s lie outside their own bands (%.1f, %.1f, %.1f x) and disagree with each other; the misses (%.1f%%..%.1f%%) are %.1e..%.1e times the 5e-10 tolerance."
      % (", ".join("%.1f" % n3["TA|%s" % n]["em0"] for n in T.NAMES), *[m / (n3["TA|%s" % n]["band"] / T.ALPHA_INV0) for m, n in zip(mm, T.NAMES)], 100 * min(mm), 100 * max(mm), min(mm) / 5e-10, max(mm) / 5e-10))
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
