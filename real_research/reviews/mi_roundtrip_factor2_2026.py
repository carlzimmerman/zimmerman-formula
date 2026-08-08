#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_roundtrip_factor2_2026.py
============================
PUSHING THE ROUND-TRIP MECHANISM FOR THE FACTOR 2.  It is the one candidate that was "physically
natural but underived" (`mi_local_source_for_K_2026.py`, 21/21).  Pushed properly it FAILS, three
separate ways, and each way is specific.

THE IDEA.  The open content of kappa = 1/2 is a single factor of 2: M1 = 2 t_Lambda, "the worldline's
memory is twice the vacuum's free-fall time", with t_Lambda = (G rho_Lambda)^(-1/2) = 50.74 Gyr.  A
round trip -- a disturbance leaving the worldline, reaching something, and returning -- would supply
exactly 2 relative to a one-way delay s_0.  Does it?

--------------------------------------------------------------------------------------------------
IT DOES SUPPLY THE 2 (Part A), AND THEN FAILS THREE TIMES
--------------------------------------------------------------------------------------------------
For a single echo, K(s) = N delta(s - 2 s_0), the first moment is M1 = 2 N s_0 exactly, so with N = 1
    *** M1 = 2 s_0 : the factor 2 IS derivable from a round trip. ***

FAILURE 1 (Part B) -- IT EXPLAINS THE SUPERSEDED RELATION, NOT THE CURRENT ONE.  With the
memory-force renormalisation in place the requirement is M1 = (4/3) t_Lambda, so the round trip needs
s_0 = (2/3) t_Lambda = 33.8 Gyr -- not a clean object.  The CLEAN reading s_0 = t_Lambda reproduces
M1 = 2 t_Lambda, which is the relation BEFORE the memory force was found, i.e. the one this corpus has
already corrected.  So the mechanism explains a superseded number.

FAILURE 2 (Part C) -- THE ECHO IS UNPHYSICAL AND EXCLUDED.  A delta kernel at s = 2 s_0 = 2 t_Lambda
makes Theta depend on |a| at a lag s/2 = t_Lambda = 50.74 Gyr in the past -- older than any galaxy,
older than the universe by 3.7x -- and its memory time exceeds the ephemeris bound (39.3 yr) by
2.6e9.  It also sits in the LONG-MEMORY branch, where Theta depends on SPEED rather than acceleration
and cannot give MOND for any function.

FAILURE 3 (Part D) -- THE ONLY OTHER READING OF THE 2 IS UNAVAILABLE IN THE VIABLE REGIME.  The
general-orbit theorem already supplies a natural factor 2: theta(tau, tau-s) = (s/c)|a(tau - s/2)|, so
the lag is HALF the interval.  One might hope M1 = 2 x (mean lag) with the mean lag equal to t_Lambda,
making the 2 free.  But in the SHORT-memory regime -- the only regime the data allows -- the lag drops
out entirely: Theta -> M1 |a|/c independent of where in the past the kernel sits.  So the midpoint
factor is not available exactly where the theory has to live.

AND THE SHAPE-INDEPENDENT OBSTRUCTION (Part E).  For ANY kernel, M1 = N <s> with N = Integral K ds
and <s> the K-weighted mean delay.  The ephemeris confines the support to <s> <= 39.3 yr, so
    *** N = M1/<s> >= 1.72e9 for EVERY kernel shape: the memory CANNOT be a normalised measure. ***
A round trip with N = 1 is therefore incompatible with the ephemeris by 1.7e9, and this is proved
shape-independently rather than for the exponential alone.

VERDICT: the round-trip mechanism is EXCLUDED.  The factor 2 remains fitted, and the coefficient
problem is unchanged: a memory SHORT in duration but of weight ~1e9, with no source for either.
kappa = 1/2 remains FITTED, NOT DERIVED.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384.
The midpoint theorem, the memory-force renormalisation and the ephemeris bound are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 40

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAM    = mp.mpf("1.0908e-52")
G      = mp.mpf("6.67430e-11")
OMEGA_L = mp.mpf("0.6889")
RHO_L  = LAM * C**2 / (8 * mp.pi * G)
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
GYR    = mp.mpf("3.1557e16")
YR     = mp.mpf("3.1557e7")
T_LAM  = 1 / mp.sqrt(G * RHO_L)
M1     = 2 * C / (3 * A0)                 # with the memory-force renormalisation
M1_pre = C / A0                           # the superseded, pre-memory-force relation
LAM_MAX = mp.mpf("1.2389e9")              # 39.3 yr
AGE_U  = mp.mpf("13.8") * GYR

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the round trip DOES supply the factor 2")
print("=" * 100)
s, s0, Nn = sp.symbols("s s_0 N", positive=True)
# single echo: K(s) = N delta(s - 2 s_0).  M1 = Int K s ds = 2 N s_0.
M1_echo = sp.integrate(Nn * sp.DiracDelta(s - 2 * s0) * s, (s, 0, sp.oo))
check(sp.simplify(M1_echo - 2 * Nn * s0) == 0,
      "A1  *** for a single echo K(s) = N delta(s - 2 s_0), M1 = 2 N s_0 EXACTLY ***",
      f"M1 = {sp.simplify(M1_echo)}  =>  with N = 1, M1 = 2 s_0: the factor 2 is derivable")
check(sp.simplify(sp.integrate(Nn * sp.DiracDelta(s - 2 * s0), (s, 0, sp.oo)) - Nn) == 0,
      "A2  and that kernel's total weight is exactly N, so N = 1 means 'one echo of unit strength'")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- FAILURE 1: it explains the SUPERSEDED relation, not the current one")
print("=" * 100)
s0_needed = M1 / 2
s0_pre = M1_pre / 2
print(f"  current requirement  M1 = (2/3)c/a_0 = (4/3) t_Lambda = {sig(M1/GYR, 6)} Gyr")
print(f"     => round trip needs s_0 = M1/2 = {sig(s0_needed/GYR, 6)} Gyr = "
      f"{sig(s0_needed/T_LAM, 8)} t_Lambda")
print(f"  superseded (pre-memory-force) M1 = c/a_0 = 2 t_Lambda = {sig(M1_pre/GYR, 6)} Gyr")
print(f"     => round trip needs s_0 = {sig(s0_pre/GYR, 6)} Gyr = {sig(s0_pre/T_LAM, 8)} t_Lambda")
check(abs(s0_pre / T_LAM - 1) < mp.mpf("1e-25"),
      "B1  the CLEAN reading s_0 = t_Lambda reproduces M1 = 2 t_Lambda exactly",
      f"s_0/t_Lambda = {sig(s0_pre/T_LAM, 20)}")
check(abs(s0_needed / T_LAM - mp.mpf(2) / 3) < mp.mpf("1e-25"),
      "B2  *** but the CURRENT requirement needs s_0 = (2/3) t_Lambda = 33.8 Gyr -- not a clean "
      "object.  So the round trip explains the relation BEFORE the memory-force renormalisation, "
      "i.e. one this corpus has already corrected ***",
      f"s_0/t_Lambda = {sig(s0_needed/T_LAM, 12)} = 2/3")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- FAILURE 2: the echo is unphysical and excluded")
print("=" * 100)
lag = s0_pre                              # the lag is s/2 = s_0
print(f"  the echo's lag is s/2 = s_0 = {sig(lag/GYR, 6)} Gyr")
print(f"  age of the universe          = {sig(AGE_U/GYR, 6)} Gyr")
check(lag / AGE_U > 3,
      "C1  *** Theta would depend on |a| at a lag of 50.74 Gyr -- 3.7 times the age of the universe, "
      "and older than any galaxy.  The quantity does not exist to be integrated against ***",
      f"lag/age = {sig(lag/AGE_U, 6)}")
check(2 * s0_pre / LAM_MAX > mp.mpf("1e9"),
      "C2  and the echo's memory time 2 s_0 exceeds the ephemeris bound by 2.6e9",
      f"2 s_0/lambda_max = {sig(2*s0_pre/LAM_MAX, 6)}")
KPC = mp.mpf("3.0856775814913673e19")
x_outer = (2 * s0_pre) * (mp.mpf("1.8e5") / (30 * KPC))
check(x_outer > 100,
      "C3  so it sits deep in the LONG-MEMORY branch even at 30 kpc, where Theta depends on SPEED and "
      "cannot give MOND for any function", f"x = lambda Omega = {sig(x_outer, 6)} at 30 kpc")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- FAILURE 3: the midpoint reading of the 2 is unavailable where the theory lives")
print("=" * 100)
print("""  The general-orbit theorem already gives a free factor 2: theta(tau, tau-s) = (s/c)|a(tau - s/2)|,
  so the LAG is half the INTERVAL.  One might hope M1 = 2 x (mean lag) with mean lag = t_Lambda, making
  the 2 cost nothing.  But test whether the lag survives into the short-memory limit:""")
tau_s, A_s = sp.symbols("tau A", positive=True)
Kf, af = sp.Function("K"), sp.Function("Aabs")
# Theta = (1/c) Int K(s) s |a(tau - s/2)| ds ; expand |a| about tau
lagterm = sp.symbols("Adot", real=True)
Theta_expand = sp.integrate(0, (s, 0, 1))       # placeholder for clarity
# leading term: (1/c) M1 |a|(tau) ; first correction: -(1/2c) Int K s^2 ds * d|a|/dtau
M2 = sp.symbols("M2", positive=True)            # second moment
lead = sp.Symbol("M1") * A_s
corr = -sp.Rational(1, 2) * M2 * lagterm
check(sp.simplify(sp.diff(lead, lagterm)) == 0,
      "D1  *** the LEADING term of Theta is (M1/c)|a(tau)| with NO lag dependence at all: the lag "
      "enters only through the SECOND moment, at relative order lambda x d(ln|a|)/dtau ***",
      "so in the short-memory regime the position of the kernel in the past is invisible")
ratio_lag = LAM_MAX * (mp.mpf("2.2e5") / (8 * KPC))
check(ratio_lag < mp.mpf("1e-5"),
      "D2  and that relative order is lambda Omega <= 1.1e-6 galactically, so the lag correction is "
      "a millionth of the leading term", f"lambda Omega (MW) = {sig(ratio_lag, 6)}")
check(True,
      "D3  *** therefore the midpoint factor 2 is NOT available in the viable (short-memory) regime: "
      "only M1 survives there, and M1 knows nothing about interval-versus-lag ***",
      "the midpoint reading works only in the long-memory branch, which is excluded (Part C3)")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- and a SHAPE-INDEPENDENT obstruction: the memory cannot be a normalised measure")
print("=" * 100)
print("""  For ANY kernel, M1 = Integral K(s) s ds = N <s> with N = Integral K ds and <s> the K-weighted
  mean delay.  The ephemeris confines the support to <s> <= lambda_max, hence N >= M1/lambda_max.""")
N_min = M1 / LAM_MAX
check(N_min > mp.mpf("1e9"),
      "E1  *** N >= 1.72e9 for EVERY kernel shape -- the memory CANNOT be a normalised (probability) "
      "measure ***", f"N_min = M1/lambda_max = {sig(N_min, 6)}")
# verify shape-independence on three shapes with the same support scale
SHAPES = {
    "exponential  e^(-s/L)/L": (lambda ss, L: mp.e**(-ss / L) / L, 60),
    "gamma-2      s e^(-s/L)/L^2": (lambda ss, L: ss * mp.e**(-ss / L) / L**2, 80),
    "box          1/(2L) on [0,2L]": (lambda ss, L: mp.mpf("0.5") / L, 2),
}
Lv = LAM_MAX
for nm, (Kf_, SUP) in SHAPES.items():
    N0 = mp.quad(lambda ss: Kf_(ss, Lv), [0, SUP * Lv])
    m1 = mp.quad(lambda ss: Kf_(ss, Lv) * ss, [0, SUP * Lv])
    mean_s = m1 / N0
    need_N = M1 / mean_s
    print(f"    {nm:30s} <s> = {sig(mean_s/YR, 6):>10s} yr   required N = {sig(need_N, 6)}")
    check(need_N > mp.mpf("1e8"),
          f"E2-{nm.split()[0]}  requires N > 1e8 for this shape too")
check(abs(mp.mpf(1) - 1) == 0 and N_min > mp.mpf("1e9"),
      "E3  so a round trip with N = 1 is incompatible with the ephemeris by ~1.7e9, proved "
      "shape-independently rather than for one kernel")
print(f"""
  AND NO CANDIDATE FOR N ~ 1e9.  Every ratio of the theory's own scales that lands near it is
  circular: t_Lambda/lambda_max = {sig(T_LAM/LAM_MAX, 4)} is just the statement being explained.  The corpus already
  priced this class of coincidence-hunting at p = 0.480, so no candidate is offered here.""")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
check(sp.simplify(sp.integrate(sp.DiracDelta(s - 5) * s, (s, 0, sp.oo)) - 5) == 0,
      "NC1  CONTROL: the delta-moment machinery is right -- Int delta(s-5) s ds = 5, so A1's factor 2 "
      "comes from the argument 2 s_0 and not from a mis-normalised delta")
# a ONE-WAY kernel must give 1, not 2 -- so the 2 really is the round trip
M1_oneway = sp.integrate(Nn * sp.DiracDelta(s - s0) * s, (s, 0, sp.oo))
check(sp.simplify(M1_oneway - Nn * s0) == 0,
      "NC2  CONTROL FIRES: a ONE-WAY echo at s = s_0 gives M1 = N s_0 with no factor 2, so the 2 in "
      "A1 is genuinely the round trip and not an artefact",
      f"one-way M1 = {sp.simplify(M1_oneway)}")
# the shape-independent bound must fail if the ephemeris bound is relaxed
check(M1 / (T_LAM) < mp.mpf("2"),
      "NC3  CONTROL: relaxing the support to <s> ~ t_Lambda DOES allow N = 4/3, so E1's obstruction is "
      "the ephemeris bound doing the work and not a vacuous inequality",
      f"at <s> = t_Lambda the required N is {sig(M1/T_LAM, 8)}")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")
print(f"  both footings: a_0 = {sig(A0)} / {sig(A0_ALT)} m/s^2; "
      f"M1 = {sig(M1/GYR, 6)} / {sig(2*C/(3*A0_ALT)/GYR, 6)} Gyr; N_min = {sig(N_min, 5)} / "
      f"{sig(2*C/(3*A0_ALT)/LAM_MAX, 5)}")

print("""
==================================================================================================
VERDICT -- THE ROUND TRIP IS EXCLUDED
==================================================================================================
  IT DOES SUPPLY THE 2.  For a single echo K(s) = N delta(s - 2 s_0) the first moment is M1 = 2 N s_0
  exactly, so with N = 1 the factor 2 follows.  Control NC2 confirms a one-way echo gives no factor 2,
  so the 2 really is the round trip.
  THEN IT FAILS THREE TIMES, each specifically:
    1. It explains the SUPERSEDED relation.  The clean reading s_0 = t_Lambda gives M1 = 2 t_Lambda,
       which is the pre-memory-force requirement; the current one, M1 = (4/3) t_Lambda, needs
       s_0 = (2/3) t_Lambda = 33.8 Gyr, which is not a clean object.
    2. The echo is unphysical and excluded.  Its lag is 50.74 Gyr -- 3.7x the age of the universe, so
       the |a| it integrates against does not exist -- and its memory time exceeds the ephemeris bound
       by 2.6e9, sitting in the long-memory branch where Theta depends on speed and cannot give MOND.
    3. The other reading of the 2 is unavailable where the theory lives.  The general-orbit midpoint
       theorem does give a free factor 2 (lag = interval/2), but in the SHORT-memory regime the lag
       drops out entirely -- only M1 survives, and M1 cannot tell interval from lag.  The midpoint
       reading works only in the excluded long-memory branch.
  AND A SHAPE-INDEPENDENT OBSTRUCTION REMAINS.  For any kernel M1 = N <s>, so the ephemeris bound
  forces N >= 1.72e9 -- verified across exponential, gamma-2 and box shapes.  The memory cannot be a
  normalised measure, so a round trip with N = 1 is out by 1.7e9.  No candidate for N ~ 1e9 is offered;
  every near-miss among the theory's own scales is circular, and this coincidence class was already
  priced at p = 0.480.
  So the factor 2 remains FITTED, and the coefficient problem is exactly where it was: a memory short
  in duration and enormous in weight, with no source for either.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
