#!/usr/bin/env python3
"""V1 -- acceptance harness for 'exact to many decimals', and what the measurements permit today.  Pre-registered in V1_PREREGISTRATION.md.

Measured values are RECALLED (see the pre-registration); they are inputs.
Usage:  python3 v1_exactness_harness.py                       (selftest + measurement table; exit 0 iff the declared checks pass)
        python3 v1_exactness_harness.py --candidate "expr"     (evaluate an mpmath expression for alpha^-1 and grade it; exit 0 always, informational)
        python3 v1_exactness_harness.py --mutate               (control: shifts the CODATA-2022 reference by +5 sigma; the selftest must then FAIL and exit 1)
"""
import sys
import mpmath as mp

mp.mp.dps = 60
MUT = "--mutate" in sys.argv
M = {   # alpha^-1 central value, absolute 1-sigma uncertainty
    "CODATA 2022": (mp.mpf("137.035999177"), mp.mpf("0.000000021")),
    "CODATA 2018": (mp.mpf("137.035999084"), mp.mpf("0.000000021")),
    "Cs recoil (Parker 2018)": (mp.mpf("137.035999046"), mp.mpf("0.000000027")),
    "Rb recoil (Morel 2020)": (mp.mpf("137.035999206"), mp.mpf("0.000000011")),
    "electron g-2 (2023)": (mp.mpf("137.035999166"), mp.mpf("0.000000015")),
}
if MUT:
    M["CODATA 2022"] = (M["CODATA 2022"][0] + 5 * M["CODATA 2022"][1], M["CODATA 2022"][1])
CH = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def grade(value):
    print("candidate alpha^-1 =", mp.nstr(value, 40))
    print("  measurement                        offset (sigma)   rel. uncertainty (ppb)")
    ok = []
    for k, (c, s) in M.items():
        off = (value - c) / s
        ok.append(abs(off) < 2)
        print(f"  {k:34s} {mp.nstr(off, 5):>14s}   {mp.nstr(s / c * 1e9, 4):>10s}")
    n = sum(ok)
    verdict = "consistent with ALL" if n == len(ok) else ("consistent with SOME (%d of %d)" % (n, len(ok)) if n else "inconsistent with ALL")
    print("  joint verdict (|offset| < 2 sigma):", verdict)
    return n, len(ok)


print("V1: how precisely is alpha known, and what does 'exact' mean today?  (measured values RECALLED; MUTATE=%s)" % MUT)
print("  measurement                        alpha^-1                    sigma (abs)     sigma (ppb)")
for k, (c, s) in M.items():
    print(f"  {k:34s} {mp.nstr(c, 13):>22s}   {mp.nstr(s, 3):>12s}   {mp.nstr(s / c * 1e9, 4):>10s}")

cs, csu = M["Cs recoil (Parker 2018)"]
rb, rbu = M["Rb recoil (Morel 2020)"]
diff = rb - cs
comb = mp.sqrt(csu ** 2 + rbu ** 2)
print(f"\nCs-Rb: difference = {mp.nstr(diff, 4)} ({mp.nstr(diff / cs * 1e9, 4)} ppb) = {mp.nstr(diff / comb, 4)} combined sigma")
chk("A1 the Cs and Rb atom-interferometer values disagree by more than 5 combined sigma", diff / comb > 5, f"({mp.nstr(diff / comb, 4)} sigma)")

# digits established jointly: largest d such that all measurements, rounded, agree within their errors
best_rel = min(s / c for c, s in M.values())
digits_ppb = -mp.log10(best_rel)
allc = [c for c, _ in M.values()]
spread = max(allc) - min(allc)
print(f"best single relative uncertainty = {mp.nstr(best_rel * 1e9, 4)} ppb -> a claim beyond ~{mp.nstr(digits_ppb, 3)} significant digits cannot be tested by the best single measurement")
print(f"full spread of the central values = {mp.nstr(spread, 4)} in alpha^-1 = {mp.nstr(spread / mp.mpf('137.036') * 1e9, 4)} ppb")
chk("A2 all central values agree only to about 8-9 significant digits (spread between 1e-9 and 1e-8 relative)", mp.mpf("1e-9") < spread / mp.mpf("137.036") < mp.mpf("1e-8"),
    f"(relative spread {mp.nstr(spread / mp.mpf('137.036'), 3)})")
chk("A3 the best single measurement tests at most 10 significant digits (uncertainty > 5e-11 relative)", best_rel > mp.mpf("5e-11"), f"(best {mp.nstr(best_rel, 3)})")

print("\nselftest of the grader on the CODATA-2022 centre:")
n, tot = grade(mp.mpf("137.035999177"))
off0 = (mp.mpf("137.035999177") - M["CODATA 2022"][0]) / M["CODATA 2022"][1]
chk("B1 a candidate placed at the published CODATA-2022 centre has zero offset from the CODATA-2022 reference (the mutated reference is shifted by +5 sigma, so this FAILS there)",
    abs(off0) < mp.mpf("1e-30"), f"(offset {mp.nstr(off0, 4)} sigma)")
chk("B2 a candidate at the CODATA-2022 centre is NOT within 2 sigma of ALL five measurements (the atom-interferometer values disagree with one another, so no single number satisfies all)", n < tot, f"(consistent with {n} of {tot})")

if "--candidate" in sys.argv:
    expr = sys.argv[sys.argv.index("--candidate") + 1]
    print("\ngrading the supplied candidate (expression evaluated with mpmath at 60 digits; names: pi, e, sqrt, log, exp, zeta):")
    ns = dict(pi=mp.pi, e=mp.e, sqrt=mp.sqrt, log=mp.log, exp=mp.exp, zeta=mp.zeta, mpf=mp.mpf)
    val = eval(expr, {"__builtins__": {}}, ns)
    grade(mp.mpf(val))
    print("  NOTE: agreement within these uncertainties tests at most ~9-10 digits; digits beyond that are untestable today and would be a PREDICTION;")
    print("        the campaign bar (real_research/alpha_principle_2026/D_calibration_bar) additionally requires P < 1e-3 after look-elsewhere, zero fitted reals, and the scale stated.")

ok = all(CH)
print("\nVERDICT: %s" % ("declared checks pass" if ok else "a declared check FAILED"))
if MUT:
    print("MUTATE CONTROL:", "FAILED as required -- the control works (exit 1)" if not ok else "DID NOT FAIL -- the check has no power")
sys.exit(0 if ok else 1)
