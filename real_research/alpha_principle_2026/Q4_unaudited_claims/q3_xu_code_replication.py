#!/usr/bin/env python3
"""q3_xu_code_replication.py -- lane Q4: replicate the published Listing 1 of Xu (Research Square rs-7426700 v1, 2025), 'First-Principles Derivation of the
Fine Structure Constant ... Lorentz-Covariant Tensor Fields and Self-Consistent Harmonic Cascades', at reduced precision for small harmonic order m.

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q3_xu_code_replication.py            -> exit 0 iff (a) the listing as printed does not import,
              (b) the minimally repaired listing's output tracks the hard-coded baseline one-for-one (d output / d baseline = 1 to 1e-9), and
              (c) the repaired output does NOT reproduce the paper's Table 1 entries for m = 2, 4, 6, 8 to 1e-9 (declared in Q4_PREREGISTRATION.md).
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q3_xu_code_replication.py --mutate   -> the 'baseline-removed control' run (baseline 137.0, which must change the output
              by exactly the baseline change) is fed the CODATA baseline back, so the measured slope d output/d baseline becomes 0 instead of 1: check (b) fails, exit 1.
The repair is the minimum needed to run: mpmath 1.3.0 has no sphericaljn (defined here as sqrt(pi/(2x)) J_{n+1/2}(x)) and no factorial2 (mpmath.fac2 used).
Nothing else in the listing is changed (the adaptive integral, Gamma_m, harmonic_correction*1e-12, delta_EBT_vac, the baseline line). Precision is 40 digits, not 20000.
"""
import sys
sys.dont_write_bytecode = True
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "D_calibration_bar"))
import mpmath as mp
import bar_lib as B   # lane D (imported unmodified): target and CODATA sigma

MUTATE = "--mutate" in sys.argv
mp.mp.dps = 40
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# (a) the import line exactly as printed in Listing 1 (line 2)
try:
    exec("from mpmath import mpf , quad , sphericaljn , besseljzero")
    imp_ok = True
except ImportError as e:
    imp_ok = False
    P("(a) printed import line fails:", e)
if imp_ok:
    P("(a) printed import line succeeded (unexpected)")

from mpmath import mpf, quad, besseljzero
def sphericaljn(n, x):
    return mp.sqrt(mp.pi / (2 * x)) * mp.besselj(n + mp.mpf(1) / 2, x)

def adaptive_integral(f, a, b, tol=mpf("1e-22"), depth=0):
    I1, err1 = mp.quad(f, [a, b], error=True, maxdegree=6)
    mid = (a + b) / 2
    I2_left, e2l = mp.quad(f, [a, mid], error=True, maxdegree=6)
    I2_right, e2r = mp.quad(f, [mid, b], error=True, maxdegree=6)
    I2 = I2_left + I2_right
    if abs(I1 - I2) < tol or depth > 6:
        return I2
    return adaptive_integral(f, a, mid, tol / 2, depth + 1) + adaptive_integral(f, mid, b, tol / 2, depth + 1)

def Gamma_m_analytical(m, mu1, lambda0):
    factor = mp.fac2(2 * m + 1) / mp.factorial(m)         # mp.factorial2 does not exist in mpmath
    return ((-1) ** (m + 1) * factor * (lambda0 * mu1 / (2 * m + 1)) ** 0.5)

def ebt_vacuum_correction_new():
    mu1 = besseljzero(1, 1)
    I7 = adaptive_integral(lambda r: sphericaljn(1, mu1 * r) ** 2 * r ** 2, 0, 1)
    I4 = adaptive_integral(lambda r: sphericaljn(1, mu1 * r) ** 4 * r ** 2, 0, 1)
    beta = I7 / I4 ** 2.5
    integrand = lambda r: sphericaljn(1, mu1 * r) ** 2 * r ** 2
    return beta * adaptive_integral(integrand, 0, mpf("0.1"))

def calculate_alpha_inverse(m, base):
    mu1 = besseljzero(1, 1)
    lambda0 = 1 / adaptive_integral(lambda r: sphericaljn(1, mu1 * r) ** 4 * r ** 2, 0, 1)
    mum = besseljzero(m, 1)
    integrand = lambda r: sphericaljn(1, mu1 * r) * sphericaljn(m, mum * r) * r ** 3
    Gamma_m = Gamma_m_analytical(m, mu1, lambda0)
    harmonic_correction = Gamma_m * adaptive_integral(integrand, 0, 1)
    delta_EBT_vac = ebt_vacuum_correction_new()
    return base + harmonic_correction * mpf("1e-12") + delta_EBT_vac, harmonic_correction * mpf("1e-12"), delta_EBT_vac

T = mp.mpf("137.035999177")
table1 = {2: mp.mpf("137.0359985000000"), 4: mp.mpf("137.0359991600000"), 6: mp.mpf("137.0359991770000"), 8: mp.mpf("137.0359991762000")}
P("(b) repaired Listing 1, dps = 40, baseline as printed (137.035999177):")
res = {}
ok_track = True
ok_notrepro = True
for m in (2, 4, 6, 8):
    v, hc, dv = calculate_alpha_inverse(m, T)
    v0, _, _ = calculate_alpha_inverse(m, mp.mpf("137.0"))     # the no-baseline control: baseline removed (set to 137.0)
    if MUTATE:
        v0, _, _ = calculate_alpha_inverse(m, T)               # MUTATE: control fed the CODATA baseline back
    slope = (v - v0) / (T - mp.mpf("137.0"))
    res[m] = (v, hc, dv, v0)
    P("  m=%d : output = %s ; harmonic_correction*1e-12 = %s ; delta_EBT_vac = %s ; |output - baseline| = %s ; paper Table 1 = %s ; |output - Table 1| = %s"
      % (m, mp.nstr(v, 20), mp.nstr(hc, 6), mp.nstr(dv, 6), mp.nstr(abs(v - T), 6), mp.nstr(table1[m], 17), mp.nstr(abs(v - table1[m]), 6)))
    P("        baseline-removed control (baseline 137.0; MUTATE feeds the CODATA baseline) : output = %s ; slope d output / d baseline = %s" % (mp.nstr(v0, 20), mp.nstr(slope, 12)))
    ok_track = ok_track and abs(slope - 1) < mp.mpf("1e-9")
    ok_notrepro = ok_notrepro and abs(v - table1[m]) > mp.mpf("1e-9")
P("(b) output tracks the baseline one-for-one (d output/d baseline = 1 to 1e-9): %s" % ok_track)
P("(c) repaired output reproduces none of Table 1 for m = 2,4,6,8 to 1e-9: %s" % ok_notrepro)
dvs = [res[m][2] for m in res]
P("    the m-independent term delta_EBT_vac = %s dominates the m-dependent harmonic terms (|harmonic_correction*1e-12| <= %s): so the repaired code returns %s, i.e. %s away from its own baseline (%.1e relative); the printed Table 1 is not what this code prints." % (mp.nstr(dvs[0], 8), mp.nstr(max(abs(res[m][1]) for m in res), 4), mp.nstr(res[2][0], 12), mp.nstr(abs(res[2][0] - T), 6), float(abs(res[2][0] - T) / T)))
P("    m = 1024 at 20000 digits (the paper's headline) was NOT run: the paper itself says it is 'extrapolated'; besseljzero(1024, 1) at that precision was not attempted here.")
P("    reference to the paper's 'experiment': Table 2 quotes 137.035999177(11) as a 2025 measurement (relative %.1e); CODATA 2022 sigma_rel = %.1e; the code's 'agreement at 1e-15' is agreement with its own baseline line." % (11e-9 / 137.035999177, B.DELTA_CODATA))
verdict = (not imp_ok) and ok_track and ok_notrepro
if MUTATE:
    P("MUTATE: check (b) %s (a live control fails here) ; exit %d" % ("holds" if ok_track else "FAILS", 0 if verdict else 1))
    open("q3_xu_code_replication_MUTATE.out", "w").write("\n".join(out) + "\n")
    sys.exit(0 if verdict else 1)
P("VERDICT: %s" % ("as declared (exit 0)" if verdict else "NOT as declared (exit 1): see lines above and amend visibly"))
open("q3_xu_code_replication.out", "w").write("\n".join(out) + "\n")
sys.exit(0 if verdict else 1)
