#!/usr/bin/env python3
"""V1 -- acceptance harness for 'exact to many decimals', and what the measurements permit today.  Pre-registered in V1_PREREGISTRATION.md.

Measured values are RECALLED (see the pre-registration); they are inputs.
Usage:  python3 v1_exactness_harness.py                       (selftest + measurement table; exit 0 iff the declared checks pass)
        python3 v1_exactness_harness.py --candidate "expr"     (evaluate an mpmath expression for alpha^-1 and grade it; exit 0 always, informational)
        python3 v1_exactness_harness.py --mutate               (control: parses candidates through a float (the bug found by the independent re-run); exit 1 iff EXACTLY check B1 fails, exit 3 if the control is broken)
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
CH = []
FAILED = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    if not ok:
        FAILED.append(tag)


def parse_candidate(expr):
    """A numeric literal is parsed exactly by mpmath (no float round-trip); anything else is evaluated as an mpmath expression.
    The --mutate control forces the float route, which loses all digits beyond ~16 (the defect found by the independent re-run)."""
    try:
        return mp.mpf(float(expr)) if MUT else mp.mpf(expr)
    except (ValueError, TypeError):
        ns = dict(pi=mp.pi, e=mp.e, sqrt=mp.sqrt, log=mp.log, exp=mp.exp, zeta=mp.zeta, mpf=mp.mpf)
        return mp.mpf(eval(expr, {"__builtins__": {}}, ns))


def common_sig_digits(strings):
    """Number of leading significant digits shared by all the given decimal strings (the decimal point is ignored)."""
    ds = [s.replace(".", "") for s in strings]
    n = 0
    for chars in zip(*ds):
        if len(set(chars)) == 1:
            n += 1
        else:
            break
    return n
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

LITERALS = ["137.035999177", "137.035999084", "137.035999046", "137.035999206", "137.035999166"]
dj = common_sig_digits(LITERALS)
chk("A4 the five central values share exactly 8 or 9 leading significant digits (declared: about 8-9)", dj in (8, 9), f"({dj} digits: {LITERALS[0][:dj + 1]}...)")

print("\nselftest of the grader on the CODATA-2022 centre:")
n, tot = grade(parse_candidate("137.035999177"))
chk("B1 a bare decimal candidate is parsed EXACTLY (no float round-trip): parse_candidate('137.035999177') equals mpf('137.035999177') to 1e-40",
    abs(parse_candidate("137.035999177") - mp.mpf("137.035999177")) < mp.mpf("1e-40"))
chk("B2 a candidate at the CODATA-2022 centre is NOT within 2 sigma of ALL five measurements (the atom-interferometer values disagree with one another, so no single number satisfies all)", n < tot, f"(consistent with {n} of {tot})")
d_int = grade(parse_candidate("137"))[0]
chk("B3 the decoy candidate 137 is inconsistent with ALL five measurements", d_int == 0)

if "--candidate" in sys.argv:
    expr = sys.argv[sys.argv.index("--candidate") + 1]
    print("\ngrading the supplied candidate (expression evaluated with mpmath at 60 digits; names: pi, e, sqrt, log, exp, zeta):")
    grade(parse_candidate(expr))
    print("  NOTE: agreement within these uncertainties tests at most ~9-10 digits; digits beyond that are untestable today and would be a PREDICTION;")
    print("        the campaign bar (real_research/alpha_principle_2026/D_calibration_bar) additionally requires P < 1e-3 after look-elsewhere, zero fitted reals, and the scale stated.")

ok = all(CH)
print("\nVERDICT: %s" % ("declared checks pass" if ok else "a declared check FAILED"))
if MUT:
    works = [t.split()[0] for t in FAILED] == ["B1"]
    print("MUTATE CONTROL: failed checks:", FAILED, "->", "the control works (exit 1)" if works else "CONTROL BROKEN (exit 3): it must fail exactly B1")
    sys.exit(1 if works else 3)
sys.exit(0 if ok else 1)
