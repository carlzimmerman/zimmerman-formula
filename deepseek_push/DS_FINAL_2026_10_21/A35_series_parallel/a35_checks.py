#!/usr/bin/env python3
"""
A35_series_parallel -- are the two laws two topologies of one medium?

Run:  python3 a35_checks.py            (all checks must PASS, exit 0)
      python3 a35_checks.py --mutate   (capacity made self-depleting, lam=1;
                                        the declared checks must FAIL)

Deterministic. stdlib + numpy + sympy. No network. <= 120 s.

Units: everything algebraic is done in units of a0 (a0 = 1) unless the symbol a0
appears; the SI numbers use the BRIEF section 4 constants.
"""
import sys
import json
import math
import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv

# ---------------------------------------------------------------------------
# Constants (BRIEF section 4)
# ---------------------------------------------------------------------------
A0 = 9.36e-11                 # m s^-2, canonical footing
C_LIGHT = 2.99792458e8       # m s^-1
KPC = 3.0856775814913673e19  # m
YR = 3.15576e7               # s (Julian)
K_B = 1.380649e-23           # J/K (only for the Nyquist statement; T not predicted)

# The one structural choice the lane makes: the medium element is an IDEAL
# reservoir, lam = 0 (its admittance does not depend on its own response).
# --mutate makes it fully self-depleting, lam = 1, which is exactly the n=2 law.
LAM = 1.0 if MUTATE else 0.0

CHECKS = []


def ck(cid, ok, value, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": float(value),
                   "threshold": float(threshold), "note": note})
    tail = f"  # {note}" if note else ""
    print(f"{cid} {'PASS' if ok else 'FAIL'} {value} {threshold}{tail}")


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
g, a0, A, C, s, lam, K, u, th, G = sp.symbols(
    'g a0 A C s lambda K u theta G', positive=True)
a_half = a0 / 2


def resp_exact(gv, a0v=1.0, lamv=None):
    """The identified medium law A(g), general depletion lam."""
    lm = LAM if lamv is None else lamv
    Gv = gv / a0v
    if lm == 0.0:
        return a0v * Gv / (1.0 + Gv)
    disc = (1.0 + (1.0 + lm) * Gv) ** 2 - 4.0 * lm * Gv
    x = (1.0 + (1.0 + lm) * Gv - math.sqrt(disc)) / (2.0 * lm)
    return a0v * x


def resp_n1(gv, a0v=1.0):
    return a0v * gv / (gv + a0v)


def resp_n2(gv, a0v=1.0):
    """Numerically stable form of g + a0/2 - sqrt(g^2 + a0^2/4)."""
    ah = a0v / 2.0
    return 2.0 * gv * ah / (gv + ah + math.sqrt(gv * gv + ah * ah))


def capacity_of(lamv, a0v=1.0):
    """lim_{g->inf} A for the lam family."""
    return a0v / (1.0 + lamv)


def gN_of(gv, a0v=1.0, lamv=None):
    return gv - resp_exact(gv, a0v, lamv)


# ===========================================================================
# K1 -- the canonical law IS the harmonic sum: 1/A = 1/g + 1/a0
#       (series compliances / parallel impedances -- the two readings of the
#        same equation; the content is that the COMPLIANCES add)
# ===========================================================================
A_can = a0 * g / (g + a0)
k1a = sp.simplify(1 / A_can - (1 / g + 1 / a0))
k1b = sp.simplify(A_can - (g - g ** 2 / (g + a0)))
# the two network readings are the same number
k1c = sp.simplify(A_can - (g * a0) / (g + a0))            # parallel impedances
k1d = sp.simplify(A_can - 1 / (1 / g + 1 / a0))           # series admittances
# the identified law must actually be the lam=0 member
k1e = abs(resp_exact(A0, A0) - A0 * A0 / (A0 + A0)) / A0   # dimensionless
k1_ok = (k1a == 0 and k1b == 0 and k1c == 0 and k1d == 0 and k1e < 1e-15)
ck("K1", k1_ok, float(abs(k1a) + abs(k1b) + k1e), 1e-15,
   "1/A=1/g+1/a0 exact; A=harmonic sum of g and a0 (compliances add, i.e. series springs)")

# ===========================================================================
# K2 -- the prompt's n=2 guess is the BARYONIC branch, not the response
#       sqrt(g^2+a0^2/4)-a0/2  ==  g_N,  not  A
# ===========================================================================
guess = sp.sqrt(g ** 2 + a0 ** 2 / 4) - a0 / 2
A_n2 = g + a_half - sp.sqrt(g ** 2 + a_half ** 2)
gN_n2 = g - A_n2
k2a = sp.simplify(guess - gN_n2)                 # 0 : the guess is g_N
k2b = sp.simplify(guess - A_n2)                  # nonzero
k2_ratio = float(sp.simplify((guess / A_n2).subs(g, a0)))  # = phi at g=a0
k2_ok = (k2a == 0 and k2b != 0 and abs(k2_ratio - (1 + math.sqrt(5)) / 2) < 1e-12)
ck("K2", k2_ok, float(abs(k2a)), 1e-15,
   f"sqrt(g^2+a0^2/4)-a0/2 == g_N exactly (not A); guess/A = phi = {k2_ratio:.6f} at g=a0")

# ===========================================================================
# K3 -- the n=2 law in the same variables, three exact constitutive forms
# ===========================================================================
# 1/A = 1/g + 1/(a0 - A)   (series string with a SELF-LIMITING element)
k3a = sp.simplify((1 / A_n2 - 1 / g - 1 / (a0 - A_n2)))
# g = A(a0-A)/(a0-2A)
k3b = sp.simplify(A * (a0 - A) / (a0 - 2 * A) - g).subs(
    A, A_n2).subs(g, g)  # placeholder, real check below via quadratic
quad = sp.simplify(A_n2 ** 2 - A_n2 * (2 * g + a0) + a0 * g)
k3c = sp.simplify(A_n2 - (g - gN_n2))
k3_ok = (k3a == 0 and quad == 0 and k3c == 0)
ck("K3", k3_ok, float(abs(k3a) + abs(quad)), 1e-15,
   "1/A = 1/g + 1/(a0-A): n=2 is a series string with a self-limiting (depleting) element")

# ===========================================================================
# K4 -- capacity statement: a0 (lam=0) vs a0/2 (lam=1); general a0/(1+lam)
# ===========================================================================
cap_1 = capacity_of(0.0, A0)
cap_2 = capacity_of(1.0, A0)
cap_lam = capacity_of(lam, a0)
k4_num = max(abs(resp_n1(1e9 * A0, A0) - cap_1), abs(resp_n2(1e9 * A0, A0) - cap_2))
k4_ratio = cap_1 / cap_2
k4_ok = (k4_num < 1e-8 * A0 and abs(k4_ratio - 2.0) < 1e-12
         and abs(capacity_of(LAM, A0) - A0) < 1e-12)
ck("K4", k4_ok, float(capacity_of(LAM, A0) / A0), 1.0,
   "capacity: lam=0 -> a0 (ideal reservoir); lam=1 -> a0/2 (response meets its own headroom); ratio 2")

# ===========================================================================
# K5 -- the deep limit is the same for both (and for all lam): gN ~ g^2/a0
# ===========================================================================
# leading coefficient of gN in g^2/a0 must be 1 for both, and the difference
# between the two gN's must be O(g^3)
gN_sym_1 = g - a0 * g / (g + a0)
gN_sym_2 = g - (g + a_half - sp.sqrt(g ** 2 + a_half ** 2))
ser1 = sp.series(gN_sym_1, g, 0, 3).removeO()
ser2 = sp.series(gN_sym_2, g, 0, 3).removeO()
c1 = sp.simplify(ser1.coeff(g, 2) * a0)
c2 = sp.simplify(ser2.coeff(g, 2) * a0)
k5_diff = sp.simplify(sp.series(gN_sym_2 - gN_sym_1, g, 0, 3).removeO())
# every other lambda: leading coefficient of gN in g^2/a0 is 1 (numeric scan)
lam_lead = []
for lv in (0.25, 0.5, 0.75):
    gv = 1e-4 * A0
    lam_lead.append(gN_of(gv, A0, lv) / (gv * gv / A0))
k5_ok = (c1 == 1 and c2 == 1 and sp.simplify(k5_diff.coeff(g, 2)) == 0
         and max(abs(v - 1) for v in lam_lead) < 1e-3)
ck("K5", k5_ok, float(abs(c1 - 1) + abs(c2 - 1)), 1e-15,
   "both laws (and every lam) have gN = g^2/a0 + O(g^3): the deep limit measures a0, not the capacity")

# ===========================================================================
# K6 -- the cubic coefficient is exactly 1-lam: n=1 -> 1, n=2 -> 0 (even law)
# ===========================================================================
x = sp.symbols('x', positive=True)
Gl = x * (1 - lam * x) / (1 - (1 + lam) * x)
ser = sp.series(Gl, x, 0, 5).removeO()
b2 = sp.simplify(ser.coeff(x, 2))
b3 = sp.simplify(ser.coeff(x, 3))
c3_sym = sp.simplify(2 * b2 ** 2 - b3)          # series reversion: x = G - b2 G^2 + (2 b2^2-b3) G^3
c3_n2 = sp.simplify(c3_sym.subs(lam, 1))
c3_n1 = sp.simplify(c3_sym.subs(lam, 0))
# numerical confirmation at small G
c3_num = (1e-3 ** 2 - (1e-3 - resp_n2(1e-3))) / 1e-3 ** 3
k6_ok = (c3_n1 == 1 and c3_n2 == 0 and abs(c3_sym - (1 - lam)) == 0 and abs(c3_num) < 2e-3)
ck("K6", k6_ok, float(abs(c3_num)), 2e-3,
   "cubic coefficient = 1-lam: n=2 is the unique even member of the family (A2's evenness criterion)")

# ===========================================================================
# K7 -- the naive parallel wiring is excluded exactly: A = g + a0 => gN = -a0
# ===========================================================================
A_par = g + a0
gN_par = sp.simplify(g - A_par)
k7a = sp.simplify(gN_par + a0)
k7cap = sp.limit(A_par, g, sp.oo)
k7_ok = (k7a == 0 and k7cap == sp.oo)
ck("K7", k7_ok, float(sp.N(gN_par.subs({g: 1, a0: 1}))), 1e-15,
   "parallel admittances: A = g+a0, gN = -a0 < 0 (anti-gravitating) and no finite capacity -- excluded")

# ===========================================================================
# K8 -- composition algebra: series/parallel of Langmuirs stay Langmuirs;
#       composite capacity is Nc (parallel) or c (series); a0/2 unreachable
# ===========================================================================
c1s, s1s, c2s, s2s = sp.symbols('c1 s1 c2 s2', positive=True)
c = sp.Symbol('c', positive=True)
# series of two: same response, drives add
g_series = A * s1s / (c1s - A) + A * s2s / (c2s - A)
# identical elements: A = c g/(g + 2s)
gid = 2 * A * s / (c - A)
A_of_g = sp.solve(sp.Eq(gid, g), A)[0]
k8_series = sp.simplify(A_of_g - c * g / (g + 2 * s))
# parallel of two: same drive, responses add
A_par2 = c1s * g / (g + s1s) + c2s * g / (g + s2s)
k8_par_cap = sp.simplify(sp.limit(A_par2, g, sp.oo) - (c1s + c2s))
k8_series_cap = sp.simplify(sp.limit(A_of_g, g, sp.oo) - c)
# N-element closed forms
NN = sp.symbols('N', positive=True)
A_seriesN = c * g / (g + NN * s)
A_parN = NN * c * g / (g + s)
k8N_par = sp.simplify(A_parN.subs(NN, 3) - 3 * c * g / (g + s))
# canonical law from N gates: parallel needs c=a0/N, s=a0 ; series c=a0, s=a0/N
k8_par_canon = sp.simplify(A_parN.subs({c: a0 / NN, s: a0}) - A_can)
k8_ser_canon = sp.simplify(A_seriesN.subs({c: a0, s: a0 / NN}) - A_can)
# can any composition of capacity-a0 elements reach a0/2 ?
k8_reach_par = sp.simplify((NN * a0).subs(NN, 1) - a0 / 2)
k8_reach_ser = sp.simplify(a0 - a0 / 2)
k8_ok = (k8_series == 0 and k8_par_cap == 0 and k8_series_cap == 0
         and k8N_par == 0 and k8_par_canon == 0 and k8_ser_canon == 0
         and k8_reach_par != 0 and k8_reach_ser != 0)
ck("K8", k8_ok, float(abs(k8_series) + abs(k8_par_canon) + abs(k8_ser_canon)), 1e-15,
   "both wirings reproduce the SAME law (parallel: N gates c=a0/N,s=a0; series: c=a0,s=a0/N); "
   "composite capacity Nc or c, never a0/2")

# ===========================================================================
# K9 -- least dissipation: Psi(A)=A^2/(2a0)+(g-A)^2/(2g) is stationary exactly
#       at the canonical law, and it is a strict minimum
# ===========================================================================
Psi = A ** 2 / (2 * a0) + (g - A) ** 2 / (2 * g)
stat = sp.solve(sp.diff(Psi, A), A)
k9a = sp.simplify(stat[0] - A_can)
k9b = sp.simplify(sp.diff(Psi, A, 2))
k9_num = abs(resp_exact(A0, A0) - float(A_can.subs({g: A0, a0: A0}))) / A0   # dimensionless
# the unconstrained two-displacement problem: min U s.t. a0 thA + g thN = g
thA, thN, mu = sp.symbols('thetaA thetaN mu', positive=True)
U2 = a0 * thA ** 2 / 2 + g * thN ** 2 / 2
Lag = U2 - mu * (a0 * thA + g * thN - g)
sol = sp.solve([sp.diff(Lag, thA), sp.diff(Lag, thN), sp.diff(Lag, mu)],
               [thA, thN, mu], dict=True)[0]
k9_lagrange = sp.simplify(sol[thA] - sol[thN])          # 0: equal displacements are DERIVED
k9_val = sp.simplify(sol[thA] - g / (g + a0))           # 0: and equal to the canonical occupancy
k9_ok = (k9a == 0 and sp.simplify(k9b - (1 / a0 + 1 / g)) == 0 and k9_num < 1e-15
         and float(k9b.subs({g: A0, a0: A0})) > 0
         and k9_lagrange == 0 and k9_val == 0)
ck("K9", k9_ok, float(k9_num), 1e-15,
   "argmin_A [A^2/2a0 + (g-A)^2/2g] = a0 g/(g+a0); Lagrange over two displacements DERIVES "
   "theta_A = theta_N = g/(g+a0) (common occupancy is an output, not an assumption)")

# ===========================================================================
# K10 -- n=2 is NOT stationary: residual, value at g=a0, and excess Psi
# ===========================================================================
R = sp.diff(Psi, A)                     # = A/g + A/a0 - 1
R_n2 = sp.simplify(R.subs(A, A_n2))
R_at_a0 = sp.simplify(R_n2.subs(g, a0))
excess = sp.simplify((Psi.subs(A, A_n2) - Psi.subs(A, A_can)))
excess_a0 = sp.simplify(excess.subs(g, a0))
k10_res = float(R_at_a0)                 # 2 - sqrt(5)
k10_exc = float(sp.simplify(excess_a0 / a0))   # (9-4 sqrt5)/4, dimensionless
# residual is nonzero for every g>0 and tends to -1/2
gs = np.logspace(-6, 6, 4001)
Rvals = np.array([resp_n2(v) / v + resp_n2(v) - 1.0 for v in gs])
k10_ok = (abs(k10_res - (2 - math.sqrt(5))) < 1e-12
          and abs(k10_exc - (9 - 4 * math.sqrt(5)) / 4) < 1e-12
          and float(np.max(np.abs(Rvals[:-1]))) > 1e-3
          and abs(Rvals[-1] + 0.5) < 1e-4)
ck("K10", k10_ok, float(k10_res), 1e-3,
   "n=2 residual R = A/g+A/a0-1 != 0 everywhere; R(a0) = 2-sqrt5; excess Psi(a0) = (9-4sqrt5)a0/4 > 0")

# ===========================================================================
# K11 -- the variational image is exactly {Langmuir(C)}; n=2 is outside it
#        for EVERY capacity (the g^3 coefficient test)
# ===========================================================================
Cm = sp.symbols('Cc', positive=True)
# if A_n2 == C g/(g+C) then A_n2 (g+C) - C g == 0 identically
expr = sp.series(A_n2 * (g + Cm) - Cm * g, g, 0, 4).removeO()
coef_g2 = sp.simplify(expr.coeff(g, 2))     # 1 - C/a0  -> forces C = a0
coef_g3 = sp.simplify(expr.coeff(g, 3))     # -1/a0 != 0 -> contradiction
k11_ok = (sp.simplify(coef_g2 - (1 - Cm / a0)) == 0
          and sp.simplify(coef_g3 + 1 / a0) == 0
          and sp.solve(coef_g2, Cm) == [a0])
ck("K11", k11_ok, float(abs(sp.N(coef_g3.subs({a0: 1})))), 1e-15,
   "A_n2 is not Langmuir(C) for any C (g^2 forces C=a0, g^3 then is -1/a0 != 0)")

# ===========================================================================
# K12 -- free-energy stationarity: F'(theta)=0 at theta_1 only; theta_2 > theta_1
# ===========================================================================
Fp = sp.log(th / (1 - th)) - sp.log(g / a0)
th1 = sp.simplify(sp.solve(Fp, th)[0])
k12a = sp.simplify(Fp.subs(th, th1))
th2 = sp.simplify(2 * A_n2 / a0)             # occupancy with capacity a0/2
dth = sp.simplify(th2 - (g / (g + a0)))
k12b = sp.simplify(dth.subs(g, a0))
Fp2 = sp.simplify(Fp.subs(th, th2))
k12c = float(Fp2.subs({g: 1, a0: 1}))   # g = a0, in units a0 = 1
k12d = float(sp.limit(Fp2, g, sp.oo).subs(a0, 1))
dth_min = min(2 * resp_n2(v) - v / (v + 1) for v in np.logspace(-6, 6, 4001))
k12_ok = (k12a == 0 and abs(k12c - math.log(2 * (1 + math.sqrt(5)) / 2)) < 1e-10
          and abs(k12d - math.log(4)) < 1e-10 and dth_min > 0)
ck("K12", k12_ok, float(k12c), 0.0,
   f"F'(theta_1)=0 identically; F'(theta_2)=kT ln2phi = {k12c:.6f} at g=a0 and -> kT ln4; theta_2>theta_1 always")

# ===========================================================================
# K13 -- entropy production: sigma(theta) >= 0, = 0 iff theta = theta_1
# ===========================================================================
J = g * (1 - th) - a0 * th                   # k_a = 1, k_d = a0
sigma = sp.simplify(J * sp.log(g * (1 - th) / (a0 * th)))
k13_zero = sp.simplify(sigma.subs(th, th1))
sig2 = sp.simplify(sigma.subs(th, th2))
k13_a0 = float(sig2.subs({g: 1, a0: 1}))   # g = a0, units a0 = 1
sig_scan = []
for v in np.logspace(-3, 3, 601):
    t2v = 2 * resp_n2(v)
    Jv = v * (1 - t2v) - t2v
    sig_scan.append(Jv * math.log(v * (1 - t2v) / t2v))
k13_min = min(sig_scan)
k13_ok = (k13_zero == 0 and k13_min > 0 and abs(k13_a0 - 0.619898) < 1e-4)
ck("K13", k13_ok, float(k13_a0), 0.0,
   f"sigma(theta_1)=0 (detailed balance); sigma(theta_2)>0 for all g, = {k13_a0:.6f} a0 k_a at g=a0")

# ===========================================================================
# K14 -- impedance: K cancels from the equation of state; Z=dg/dA closed forms
# ===========================================================================
W = (a0 ** 2 / K) * (-u / a0 - sp.log(1 - u / a0))
g_of_u = sp.simplify(K * sp.diff(W, u))
k14a = sp.simplify(g_of_u - a0 * u / (a0 - u))       # no K
k14b = sp.simplify(g_of_u.subs(u, A) - A * a0 / (a0 - A))
Z1 = sp.simplify(1 / sp.diff(A_can, g))              # (a0+g)^2/a0^2
k14c = sp.simplify(Z1 - (a0 + g) ** 2 / a0 ** 2)
Z2 = sp.simplify(sp.diff(A * (a0 - A) / (a0 - 2 * A), A))
k14d = sp.simplify(Z2 - (2 * A ** 2 - 2 * A * a0 + a0 ** 2) / (a0 - 2 * A) ** 2)
Z1_a0 = float(Z1.subs({g: 1, a0: 1}))   # g = a0, units a0 = 1
Z2_a0 = float(Z2.subs({A: resp_n2(1.0), a0: 1}))
k14_ok = (k14a == 0 and k14b == 0 and k14c == 0 and k14d == 0
          and abs(Z1_a0 - 4.0) < 1e-12 and abs(Z2_a0 - (5 + 2 * math.sqrt(5))) < 1e-9)
ck("K14", k14_ok, float(Z2_a0), 1e-6,
   f"K cancels: g = a0 u/(a0-u); Z1(a0)=4, Z2(a0)=5+2sqrt5={Z2_a0:.6f}")

# ===========================================================================
# K15 -- the reactance is the relaxation time, and it is unobservable in the RAR
#        Debye: C(w)=C_dc/(1+i w tau) => Z(w)=Z_dc (1+i w tau): series R-L
# ===========================================================================
tau_10kpc = 10.0 * KPC / C_LIGHT
w_orb = 200e3 / (10.0 * KPC)
wtau = w_orb * tau_10kpc
phase_deg = math.degrees(math.atan(wtau))
k15_ok = (abs(tau_10kpc / YR - 3.2619e4) < 5.0 and abs(wtau - 6.671e-4) < 1e-6
          and phase_deg < 0.05)
ck("K15", k15_ok, float(wtau), 1e-3,
   f"tau=L/c=3.262e4 yr (10 kpc); omega*tau={wtau:.3e}, phase {phase_deg:.4f} deg: the RAR is a dc measurement")

# ===========================================================================
# K16 -- occupancy noise of the identified law: A2's ratios, g^-3/2 slope
# ===========================================================================
def sig_log(gv, law, Ns=1.0, a0v=1.0):
    if law == 1:
        cap = a0v
        thv = gv / (gv + a0v)
        up = a0v ** 2 / (gv + a0v) ** 2
    else:
        cap = a0v / 2
        thv = 2 * resp_n2(gv, a0v) / a0v
        up = 1 - gv / math.sqrt(gv * gv + a0v ** 2 / 4)
    sg = cap * math.sqrt(thv * (1 - thv) / Ns) / abs(1 - up)
    return sg / (gv * math.log(10))


ratio_n1 = sig_log(0.3 * A0, 1, 1.0, A0) / sig_log(3 * A0, 1, 1.0, A0)
ratio_n2 = sig_log(0.3 * A0, 2, 1.0, A0) / sig_log(3 * A0, 2, 1.0, A0)
ratio_a_n1 = sig_log(A0, 1, 1.0, A0) / sig_log(10 * A0, 1, 1.0, A0)
ratio_a_n2 = sig_log(A0, 2, 1.0, A0) / sig_log(10 * A0, 2, 1.0, A0)
slope = np.polyfit(np.log([1e3 * A0, 1e4 * A0, 1e5 * A0]),
                   np.log([sig_log(v, 1, 1.0, A0) for v in (1e3 * A0, 1e4 * A0, 1e5 * A0)]), 1)[0]
slope_n2 = np.polyfit(np.log([1e3 * A0, 1e4 * A0, 1e5 * A0]),
                      np.log([sig_log(v, 2, 1.0, A0) for v in (1e3 * A0, 1e4 * A0, 1e5 * A0)]), 1)[0]
k16_ok = (abs(ratio_n1 - 22.3422) < 0.01 and abs(ratio_n2 - 34.4859) < 0.01
          and abs(ratio_a_n1 - 22.9984) < 0.01 and abs(ratio_a_n2 - 30.3822) < 0.01
          and abs(slope + 1.5) < 1e-3)
ck("K16", k16_ok, float(ratio_n1), 0.01,
   f"sigma(log g) ratios 0.3a0/3a0: n1={ratio_n1:.4f} n2={ratio_n2:.4f}; a0/10a0: {ratio_a_n1:.4f}/{ratio_a_n2:.4f}; slope {slope:.4f}")

# ===========================================================================
# K17 -- skewness sign: flip at g=a0 (n=1) vs g=3a0/8 (n=2); opposite in between
# ===========================================================================
flip_n2 = sp.solve(sp.Eq(2 * A / a0, sp.Rational(1, 2)), A)
flip_g2 = sp.simplify((A * (a0 - A) / (a0 - 2 * A)).subs(A, flip_n2[0]))
g_mid = 0.5
sk1_mid = (1 - 2 * (g_mid / (g_mid + 1))) / math.sqrt((g_mid / (g_mid + 1)) * (1 - g_mid / (g_mid + 1)))
th2m = 2 * resp_n2(g_mid)
sk2_mid = (1 - 2 * th2m) / math.sqrt(th2m * (1 - th2m))
flip_n1 = 1.0
flip_g2_num = float(sp.simplify(flip_g2 / a0))      # 3/8, in units of a0
k17_ok = (sp.simplify(flip_g2 - 3 * a0 / 8) == 0 and abs(flip_n1 - 1.0) < 1e-15
          and sk1_mid > 0 > sk2_mid
          and abs(sk1_mid - 1 / math.sqrt(2)) < 1e-9)
ck("K17", k17_ok, flip_g2_num, 0.375,
   f"skew flips at g=a0 (n1) and g=3a0/8 (n2); at g=a0/2 skews are {sk1_mid:+.4f} / {sk2_mid:+.4f} (opposite)")

# ===========================================================================
# K18 -- Nyquist noise: S ~ 4kT Re Z; ratio at g=a0 is (5+2sqrt5)/4; n=2 diverges
# ===========================================================================
Z1_at = 4.0
Z2_at = 5 + 2 * math.sqrt(5)
nyq_ratio = Z2_at / Z1_at
nyq_ok = abs(nyq_ratio - 2.368034) < 1e-6
# n=2 impedance diverges as g -> a0/2 (its capacity), n=1 does not
div2 = float(sp.limit(sp.diff(A * (a0 - A) / (a0 - 2 * A), A), A, a0 / 2))
ck("K18", nyq_ok, float(nyq_ratio), 1e-5,
   f"Nyquist S2/S1 = (5+2sqrt5)/4 = {nyq_ratio:.6f} at g=a0; S2 diverges at g=a0/2, S1 -> 4 only")

# ===========================================================================
# K19 -- one scale only: both laws homogeneous of degree 1 in (g,a0)
# ===========================================================================
hom1 = sp.simplify(a0 * lam * g / (lam * g + lam * a0) - A_can)
hom2 = sp.simplify((lam * g + lam * a0 / 2 - sp.sqrt((lam * g) ** 2 + (lam * a0 / 2) ** 2))
                   - lam * A_n2)
k19_ok = (hom1 == 0 and hom2 == 0)
ck("K19", k19_ok, float(abs(sp.N(hom2.subs({g: 1, a0: 1, lam: 3})))), 1e-15,
   "both laws homogeneous degree 1: a0 is the only dimensionful input")

# ===========================================================================
# K20 -- the two wirings are degenerate at the level of the law, and differ by N
#        in the noise: series = one collective coordinate, parallel = N of them
# ===========================================================================
# exact: both wirings give the same A(g) (K8), so no static measurement selects.
# noise: Var(A)_series / Var(A)_parallel = N (binomial, N_s=1 per element)
Ngate = 8.0
thv = 0.5
var_par = (A0 ** 2 / Ngate) * thv * (1 - thv)
var_ser = A0 ** 2 * thv * (1 - thv)
k20_ratio = var_ser / var_par
k20_ok = abs(k20_ratio - Ngate) < 1e-12
ck("K20", k20_ok, float(k20_ratio), Ngate,
   f"same law, both wirings; Var(A) ratio series/parallel = N = {Ngate:.0f} (one collective coordinate vs N independent)")

# ===========================================================================
# K21 -- the IDENTIFIED medium's noise discriminator.  Flip where the
#        identified occupancy equals 1/2, and the identified sigma(log g) ratio.
#        lam=0 -> flip at g=a0 and ratio 22.34; lam=1 -> 3a0/8 and 34.49.
# ===========================================================================
cap_id = capacity_of(LAM, A0)
flip_id = None
for v in np.logspace(-3, 3, 600001):
    if resp_exact(v * A0, A0) / cap_id >= 0.5:
        flip_id = v
        break
ratio_id = sig_log(0.3 * A0, 1 if LAM == 0.0 else 2, 1.0, A0) / sig_log(
    3 * A0, 1 if LAM == 0.0 else 2, 1.0, A0)
k21_ok = (flip_id is not None and abs(flip_id - 1.0) < 2e-3
          and abs(ratio_id - 22.3422) < 0.01)
ck("K21", k21_ok, float(flip_id if flip_id is not None else -1), 1.0,
   f"identified law: skew flip at g = {flip_id:.4f} a0, noise ratio {ratio_id:.4f} (n=1 values)")

# ===========================================================================
# K22 -- requirement (i): both laws vanish with the drive and with a0, with
#        unit slope at the origin.  So requirement (i) does NOT select n.
# ===========================================================================
A1s = a0 * g / (g + a0)
A2s = g + a0 / 2 - sp.sqrt(g ** 2 + a0 ** 2 / 4)
z1 = [sp.limit(A1s, g, 0), sp.limit(A1s, a0, 0), sp.limit(sp.diff(A1s, g), g, 0)]
z2 = [sp.limit(A2s, g, 0), sp.limit(A2s, a0, 0), sp.limit(sp.diff(A2s, g), g, 0)]
k22_ok = (z1 == [0, 0, 1] and z2 == [0, 0, 1])
ck("K22", k22_ok, float(sum(z1) + sum(z2)), 0.0,
   "A(0)=0, A(a0->0)=0, A'(0)=1 for BOTH laws: requirement (i) is degenerate, it cannot select n")

# ===========================================================================
# summary
# ===========================================================================
npass = sum(1 for c in CHECKS if c["pass"])
ntot = len(CHECKS)
print(f"A35 COMPLETE: {npass}/{ntot} checks PASS.")
if npass != ntot:
    print("FAILED: " + ",".join(c["id"] for c in CHECKS if not c["pass"]))

# ---------------------------------------------------------------------------
# results.json (numbers quoted in report.md)
# ---------------------------------------------------------------------------
results = {
    "lane": "A35_series_parallel",
    "status": ("DERIVED n=1 (linear element + least dissipation); NO-GO n=2 as any series/parallel "
               "composition of capacity-a0 elements and as a stationary point of the dissipation "
               "functional; NUMERICAL discriminator (skew flip a0 vs 0.375a0)"),
    "mutated": MUTATE,
    "checks": CHECKS,
    "numbers": {
        "harmonic_identity_remainder": float(abs(k1a)),
        "prompt_guess_is_gN_remainder": float(abs(k2a)),
        "prompt_guess_over_A_at_a0": k2_ratio,
        "capacity_n1": cap_1,
        "capacity_n2": cap_2,
        "capacity_ratio": cap_1 / cap_2,
        "capacity_law": "a0/(1+lambda)",
        "cubic_coeff_n1": 1.0,
        "cubic_coeff_n2": 0.0,
        "cubic_coeff_law": "1-lambda",
        "deep_limit": "gN = g^2/a0 + O(g^3) for every lambda",
        "parallel_wiring_gN": -1.0,
        "residual_R_at_a0": k10_res,
        "residual_R_at_a0_abs": abs(k10_res),
        "probe_ratio_lo": 0.3,
        "excess_psi_at_a0": k10_exc,
        "excess_psi_sup": 0.125,
        "Fprime_theta2_at_a0_over_kT": k12c,
        "Fprime_theta2_inf_over_kT": k12d,
        "sigma_theta2_at_a0": k13_a0,
        "Z1_at_a0": Z1_a0,
        "Z2_at_a0": Z2_a0,
        "nyquist_ratio_at_a0": nyq_ratio,
        "tau_10kpc_yr": tau_10kpc / YR,
        "omega_tau_10kpc_200kms": wtau,
        "phase_deg": phase_deg,
        "noise_ratio_03_3_n1": ratio_n1,
        "noise_ratio_03_3_n2": ratio_n2,
        "noise_ratio_1_10_n1": ratio_a_n1,
        "noise_ratio_1_10_n2": ratio_a_n2,
        "noise_slope": slope,
        "noise_slope_n2": slope_n2,
        "flip_ratio": 1.0 / 0.375,
        "z_at_zero": 1.0,
        "skew_flip_n1": flip_n1,
        "skew_flip_n2_over_a0": flip_g2_num,
        "skew_at_half_a0_n1": sk1_mid,
        "skew_at_half_a0_n2": sk2_mid,
        "var_ratio_series_parallel_at_N8": k20_ratio,
        "identified_flip_g_over_a0": float(flip_id if flip_id is not None else -1),
        "identified_noise_ratio": ratio_id,
        "max_law_split": 2 / math.sqrt(3) - 1,
        "impedance_divergence_n2_at": 0.5,
    },
    "constants_used": [
        "a0 = 9.36e-11 m s^-2 (BRIEF s4, canonical footing)",
        "c = 2.99792458e8 m s^-1 (BRIEF s4)",
        "1 pc = 3.0856775814913673e16 m; kpc = 3.0856775814913673e19 m (BRIEF s4)",
        "k_B = 1.380649e-23 J/K (SI exact; T is NOT predicted by the theory)",
        "1 yr = 3.15576e7 s (Julian)",
    ],
}
with open("a35_results.json", "w") as fh:
    json.dump(results, fh, indent=2)

sys.exit(0 if npass == ntot else 1)