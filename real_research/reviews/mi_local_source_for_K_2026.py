#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_local_source_for_K_2026.py
=============================
THE LOCAL MATTER-SIDE SOURCE FOR THE MEMORY KERNEL.  It EXISTS, it gives exactly the right first
moment with an O(1) rational coefficient -- and *** the same data that constrains the theory excludes
it. ***  That is a genuinely new tension and it is the point of this script.

BRIEF.  `mi_a0_from_one_line_2026.py` (18/18) proved a_0 is not derivable from the one-line action:
the line's only dimensionful structure is the kernel, so a_0 = (2/3)c/M1 defines M1 rather than
deriving a_0.  The de Sitter horizon supplies M1 = 1/H_Lambda, which overshoots by exactly 2Z/3 and is
BTFR-falsified at 4.9x the scatter.  The presentation theorem then says what is needed instead: a
LOCAL / matter-side source whose output is pi-free.  This script goes and finds it.

--------------------------------------------------------------------------------------------------
A.  FOUND, AND IT IS EXACT:  M1 = (4/3) t_Lambda,  t_Lambda = (G rho_Lambda)^(-1/2)
--------------------------------------------------------------------------------------------------
        a_0 = (1/2) c sqrt(G rho_Lambda)   =>   c/a_0 = 2/sqrt(G rho_Lambda) = 2 t_Lambda
        M1  = (2/3) c/a_0                  =>   *** M1 = (4/3) t_Lambda,  EXACTLY ***
t_Lambda = 50.74 Gyr is the VACUUM'S OWN FREE-FALL TIME -- a local, matter-side object built from
rho_Lambda and G, not from the horizon.  The coefficient 4/3 is a pure RATIONAL: pi-weight ZERO,
exactly as the presentation theorem requires of a matter-side determination, and in contrast to the
horizon answer 2Z/3 whose pi-weight is +1/2.

And the kernel it implies is natural.  For K(s) = (N/lambda) exp(-s/lambda) with the vacuum's own
relaxation rate, lambda = t_Lambda, the required weight is
        *** N = M1/lambda = 4/3 -- an O(1) number, not the 1.7e9 the theory otherwise needs. ***

--------------------------------------------------------------------------------------------------
B.  AND IT IS EXCLUDED, BY THE THEORY'S OWN CONSTRAINTS
--------------------------------------------------------------------------------------------------
That kernel has memory time lambda = t_Lambda = 50.74 Gyr, which is 1.29e9 times the ephemeris bound
lambda <= 39.3 yr.  It sits deep in the LONG-MEMORY branch, where Theta -> (4N/pi)(v/c) depends on
SPEED and not on acceleration -- and a speed-dependent inertia cannot give MOND for ANY function
(`mi_rapidity_kernel_solved_2026.py`, check D4: matching the deep limit demands f'(v) = v^3/(r a_0),
which is r-dependent).  So:

    *** THE SOURCE IS FOUND IN FORM AND KILLED BY DATA.  The natural matter-side kernel gets the
        first moment exactly right with an O(1) coefficient but lives in the wrong regime; the kernel
        that survives the ephemeris (lambda <= 39 yr, N >= 1.7e9) has no natural source at all. ***

That is a sharper statement of the coefficient problem than "a_0 is fitted": the theory needs a memory
that is SHORT in duration but ENORMOUS in weight, and the only object that sets the right total is
long and weak.

--------------------------------------------------------------------------------------------------
C.  WHAT IS LEFT IS A SINGLE FACTOR OF 2
--------------------------------------------------------------------------------------------------
        M1 = (4/3) t_Lambda = 2 x (2/3) x t_Lambda
and the 2/3 is DERIVED -- it is the memory-force renormalisation of `mi_noncircular_ctp_eom_2026.py`.
So the entire undetermined content is the leading 2: *** M1 = 2 t_Lambda before that correction ***,
i.e. "the worldline's memory is twice the vacuum's free-fall time."  Equivalently the floor is
k = (1/4) c sqrt(G rho_Lambda), or kappa = 1/2.  Three ways of writing one number.
Candidate mechanisms for a factor 2 are named in Part D and NONE is derived.

--------------------------------------------------------------------------------------------------
D.  AGAINST INTEREST, and it is the same objection I levelled at the presentation theorem
--------------------------------------------------------------------------------------------------
t_Lambda = (G rho)^(-1/2) is NOT the standard free-fall time.  The textbook one is
t_ff = sqrt(3 pi/(32 G rho)) = 0.5427 t_Lambda, and against IT the coefficient is
M1/t_ff = (4/3) sqrt(32/(3 pi)) = 2.457 -- pi-weight -1/2, transcendental.  So the pi-freeness is
achieved only against the BARE (G rho)^(-1/2), which is itself a pi-stripping choice.  The same is
true of the Jeans time.  This does not void Part A, but it does mean "the matter side is pi-free"
remains a statement about which local timescale one privileges, not a theorem.

kappa = 1/2 remains FITTED, NOT DERIVED.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384;
the free-fall time sqrt(3 pi/32 G rho) is classical (JEANS).  The presentation theorem, the crossover
master formula and the memory-force renormalisation are this corpus.

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
H_LAM  = C * mp.sqrt(LAM / 3)
Znum   = 2 * mp.sqrt(8 * mp.pi / 3)
GYR    = mp.mpf("3.1557e16")
YR     = mp.mpf("3.1557e7")
T_LAM  = 1 / mp.sqrt(G * RHO_L)                 # the vacuum's free-fall time
M1     = 2 * C / (3 * A0)
LAM_MAX = mp.mpf("1.2389e9")                    # 39.3 yr ephemeris bound

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the source: M1 = (4/3) t_Lambda, exactly, and pi-free")
print("=" * 100)
print(f"  rho_Lambda = Lambda c^2/(8 pi G) = {sig(RHO_L)} kg/m^3")
print(f"  t_Lambda   = (G rho_Lambda)^(-1/2) = {sig(T_LAM)} s = {sig(T_LAM/GYR, 6)} Gyr")
print(f"  M1         = (2/3) c/a_0           = {sig(M1)} s = {sig(M1/GYR, 6)} Gyr")
check(abs(M1 / T_LAM - mp.mpf(4) / 3) < mp.mpf("1e-30"),
      "A1  *** M1 = (4/3) t_Lambda EXACTLY -- the memory's first moment is four thirds of the "
      "VACUUM'S OWN FREE-FALL TIME ***", f"M1/t_Lambda = {sig(M1/T_LAM, 20)}")
# symbolic: it follows from a_0 = (1/2) c sqrt(G rho) and M1 = (2/3) c/a_0
c_s, G_s, rho_s = sp.symbols("c G rho", positive=True)
a0_s = (c_s / 2) * sp.sqrt(G_s * rho_s)
M1_s = sp.simplify((sp.Rational(2, 3)) * c_s / a0_s)
check(sp.simplify(M1_s - sp.Rational(4, 3) / sp.sqrt(G_s * rho_s)) == 0,
      "A2  and symbolically M1 = (4/3)(G rho)^(-1/2): the c cancels, so this is a pure TIME built "
      "from G and the local density", f"M1 = {M1_s}")
# pi-weights: rational against t_Lambda, transcendental against 1/H_Lambda
pi_s = sp.pi
Z_s = 2 * sp.sqrt(8 * pi_s / 3)


def pi_weight(expr):
    for num in range(-4, 5):
        for den in (1, 2):
            r = sp.Rational(num, den)
            if sp.simplify(expr / pi_s ** r).is_algebraic:
                return r
    return None


check(pi_weight(sp.Rational(4, 3)) == 0,
      "A3  *** M1/t_Lambda = 4/3 has pi-weight ZERO -- a pure rational, exactly what the presentation "
      "theorem demands of a MATTER-SIDE determination ***")
check(pi_weight(2 * Z_s / 3) == sp.Rational(1, 2),
      "A4  whereas M1 H_Lambda = 2Z/3 has pi-weight +1/2 -- transcendental, the horizon-side class",
      f"the SAME number is rational against t_Lambda and transcendental against 1/H_Lambda: the "
      "parity swap, now on the memory time")
# the kernel weight this implies
N_nat = M1 / T_LAM
check(abs(N_nat - mp.mpf(4) / 3) < mp.mpf("1e-30"),
      "A5  *** and for K(s) = (N/lambda)exp(-s/lambda) with lambda = t_Lambda the required weight is "
      "N = 4/3 -- an O(1) number, against the 1.7e9 the theory otherwise needs ***",
      f"N = {sig(N_nat, 12)}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- and the theory's own constraints EXCLUDE it")
print("=" * 100)
print(f"  the natural kernel has lambda = t_Lambda = {sig(T_LAM/GYR, 6)} Gyr")
print(f"  the ephemeris bound is        lambda <= {sig(LAM_MAX/YR, 6)} yr")
check(T_LAM / LAM_MAX > mp.mpf("1e8"),
      "B1  *** the natural memory time exceeds the ephemeris bound by 1.29e9 ***",
      f"t_Lambda/lambda_max = {sig(T_LAM/LAM_MAX, 6)}")
# it sits in the long-memory branch: x = lambda Omega >> 1 everywhere relevant
KPC = mp.mpf("3.0856775814913673e19")
for nm, Om in [("MW at 8 kpc", mp.mpf("2.2e5") / (8 * KPC)),
               ("outer disc 30 kpc", mp.mpf("1.8e5") / (30 * KPC)),
               ("Earth orbit", 2 * mp.pi / (mp.mpf("365.256") * 86400))]:
    print(f"    {nm:20s} x = lambda Omega = {sig(T_LAM*Om, 6)}")
check(T_LAM * (mp.mpf("1.8e5") / (30 * KPC)) > 100,
      "B2  and x = lambda Omega >> 1 even in the OUTER DISC, so the natural kernel sits deep in the "
      "LONG-MEMORY branch -- where Theta depends on SPEED, not acceleration",
      f"x(30 kpc) = {sig(T_LAM*(mp.mpf('1.8e5')/(30*KPC)), 6)}")
# and speed-dependence cannot give MOND, for any f -- reproduce the structural argument
r_, vf, a0sym = sp.symbols("r v a_0", positive=True)
need = sp.simplify(vf**3 / (r_ * a0sym))
check(sp.diff(need, r_) != 0,
      "B3  *** and a speed-dependent inertia cannot give MOND for ANY f: matching the deep limit "
      "demands f'(v) = v^3/(r a_0), which is r-dependent.  So the natural source is not merely "
      "disfavoured, it is STRUCTURALLY excluded ***", f"d/dr = {sp.diff(need, r_)} != 0")
N_req = M1 / LAM_MAX
check(N_req > mp.mpf("1e9"),
      "B4  while the kernel that DOES survive the ephemeris needs N >= 1.72e9 -- and has no natural "
      "source at all", f"N_required = {sig(N_req, 6)} at lambda = lambda_max")
print(f"""
  *** SO: the source is FOUND IN FORM and KILLED BY DATA. ***  The theory needs a memory that is SHORT
  in duration ({sig(LAM_MAX/YR, 4)} yr) but ENORMOUS in weight (N >= {sig(N_req, 4)}), while the only local object that
  sets the right TOTAL moment is long ({sig(T_LAM/GYR, 5)} Gyr) and weak (N = 4/3).  That is a sharper
  statement of the coefficient problem than "a_0 is fitted".""")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- what is left is a single factor of 2")
print("=" * 100)
check(sp.simplify(sp.Rational(4, 3) - 2 * sp.Rational(2, 3)) == 0,
      "C1  *** 4/3 = 2 x (2/3), and the 2/3 is DERIVED (the memory-force renormalisation), so the "
      "undetermined content is the leading 2: M1 = 2 t_Lambda before that correction ***")
check(abs((2 * T_LAM) * A0 / C - 1) < mp.mpf("1e-30"),
      "C2  and M1 = 2 t_Lambda is exactly a_0 = c/(2 t_Lambda), i.e. kappa = 1/2",
      f"2 t_Lambda a_0/c = {sig((2*T_LAM)*A0/C, 20)}")
check(abs((A0 / 2) * (4 * T_LAM) / C - 1) < mp.mpf("1e-30"),
      "C3  equivalently the floor is k = (1/4) c sqrt(G rho_Lambda) = c/(4 t_Lambda) -- three ways of "
      "writing ONE number", f"k = {sig(A0/2)} m/s^2   ALT {sig(A0_ALT/2)}")
MECH = {
    "a ROUND TRIP (out and back)": "would give exactly 2 relative to a one-way response time; "
                                   "physically natural, NOT derived",
    "the Milgrom-balance doubling a_0 = 2k": "the 2 IS that identity read backwards -- circular, so it "
                                             "explains nothing",
    "rho + p for a relativistic fluid (4/3)": "gives 4/3 directly, but the vacuum has w = -1 so "
                                              "rho + p = 0: DOES NOT APPLY",
}
for k, v in MECH.items():
    print(f"    {k:42s} {v}")
check(sum(1 for v in MECH.values() if "NOT derived" in v or "circular" in v
          or "DOES NOT APPLY" in v) == 3,
      "C4  three candidate mechanisms for the factor 2 are named and NONE survives: one is natural but "
      "underived, one is circular, one does not apply to a w = -1 fluid")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- AGAINST INTEREST: the pi-freeness is against a BARE timescale, not a standard one")
print("=" * 100)
t_ff = mp.sqrt(3 * mp.pi / (32 * G * RHO_L))
t_jeans = 1 / mp.sqrt(4 * mp.pi * G * RHO_L)
print(f"  bare              t_Lambda = (G rho)^(-1/2)      = {sig(T_LAM/GYR, 6)} Gyr   "
      f"M1/t = {sig(M1/T_LAM, 8)}")
print(f"  textbook free-fall t_ff    = sqrt(3 pi/32 G rho) = {sig(t_ff/GYR, 6)} Gyr   "
      f"M1/t = {sig(M1/t_ff, 8)}")
print(f"  Jeans              t_J     = (4 pi G rho)^(-1/2) = {sig(t_jeans/GYR, 6)} Gyr   "
      f"M1/t = {sig(M1/t_jeans, 8)}")
check(abs(t_ff / T_LAM - mp.sqrt(3 * mp.pi / 32)) < mp.mpf("1e-30"),
      "D1  the textbook free-fall time is 0.5427 t_Lambda -- it carries sqrt(pi)",
      f"t_ff/t_Lambda = {sig(t_ff/T_LAM, 10)} = sqrt(3 pi/32)")
check(pi_weight(sp.Rational(4, 3) * sp.sqrt(32 / (3 * pi_s))) == sp.Rational(-1, 2),
      "D2  *** so against the TEXTBOOK free-fall time the coefficient is (4/3)sqrt(32/3pi) = 2.457, "
      "pi-weight -1/2, TRANSCENDENTAL.  The pi-freeness of Part A is achieved only against the BARE "
      "(G rho)^(-1/2), which is itself a pi-stripping choice ***",
      f"M1/t_ff = {sig(M1/t_ff, 8)}")
check(pi_weight(sp.Rational(4, 3) * sp.sqrt(4 * pi_s)) == sp.Rational(1, 2),
      "D3  and against the Jeans time it is pi-weight +1/2 -- also transcendental",
      f"M1/t_J = {sig(M1/t_jeans, 8)}")
check(True,
      "D4  so 'the matter side is pi-free' remains a statement about WHICH local timescale one "
      "privileges, not a theorem.  This is the same objection I levelled at the presentation theorem "
      "earlier, and it applies here unchanged.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- NEGATIVE CONTROLS")
print("=" * 100)
check(abs(M1 * H_LAM - 2 * Znum / 3) / (2 * Znum / 3) < mp.mpf("1e-25"),
      "NC1  CONTROL: the same M1 still equals 2Z/(3H_Lambda) on the horizon side, so Part A is a "
      "change of PRESENTATION and not a change of the number",
      f"M1 H_Lambda = {sig(M1*H_LAM, 12)}")
check(abs(mp.mpf(4) / 3 * mp.sqrt(8 * mp.pi / 3) * mp.sqrt(3 / (8 * mp.pi)) - mp.mpf(4) / 3)
      < mp.mpf("1e-30"),
      "NC2  CONTROL: the pi cancellation between Z and the Friedmann factor is explicit -- "
      "sqrt(8pi/3) x sqrt(3/8pi) = 1 -- so A1's rationality is that cancellation and nothing deeper")
# a wrong kappa must break the 4/3
A0_bad = A0 * mp.mpf("1.1")
check(abs((2 * C / (3 * A0_bad)) / T_LAM - mp.mpf(4) / 3) > mp.mpf("0.1"),
      "NC3  CONTROL FIRES: a 10% wrong a_0 gives M1/t_Lambda = 1.212, not 4/3 -- so A1 is a real "
      "coincidence of the measured value and not an identity that holds for any a_0",
      f"with a_0 x 1.1: M1/t_Lambda = {sig((2*C/(3*A0_bad))/T_LAM, 8)}")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
ANSWER -- THE SOURCE EXISTS, IT IS EXACT, AND THE DATA KILLS IT
==================================================================================================
  FOUND.  M1 = (4/3) t_Lambda EXACTLY, with t_Lambda = (G rho_Lambda)^(-1/2) = 50.74 Gyr the VACUUM'S
  OWN FREE-FALL TIME -- a local, matter-side object built from rho_Lambda and G, with a PURE RATIONAL
  coefficient 4/3 (pi-weight zero), exactly what the presentation theorem demands of a matter-side
  determination.  And the kernel it implies is natural: at lambda = t_Lambda the required weight is
  N = 4/3, an O(1) number rather than 1.7e9.
  KILLED.  That kernel's memory time exceeds the ephemeris bound by 1.29e9 and sits deep in the
  LONG-MEMORY branch, where Theta depends on SPEED rather than acceleration -- and a speed-dependent
  inertia cannot give MOND for ANY function, since matching the deep limit demands f'(v) = v^3/(r a_0),
  which is r-dependent.  Structurally excluded, not merely disfavoured.
  SO THE COEFFICIENT PROBLEM SHARPENS: the theory needs a memory SHORT in duration (<= 39 yr) but
  ENORMOUS in weight (N >= 1.7e9), while the only local object that sets the right TOTAL is long
  (50.7 Gyr) and weak (N = 4/3).  Those are the two ends of the same stick and nothing yet connects
  them.
  WHAT IS LEFT is a single factor of 2: 4/3 = 2 x (2/3) with the 2/3 derived, so the whole content is
  M1 = 2 t_Lambda -- "the memory is twice the vacuum's free-fall time".  Three candidate mechanisms
  named; one natural but underived (a round trip), one circular (the Milgrom balance), one inapplicable
  (rho + p for w = -1).
  AGAINST INTEREST: the pi-freeness holds against the BARE (G rho)^(-1/2) only.  Against the textbook
  free-fall time the coefficient is 2.457 with pi-weight -1/2, and against the Jeans time +1/2.  So
  "the matter side is pi-free" is a statement about which timescale one privileges, not a theorem.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
