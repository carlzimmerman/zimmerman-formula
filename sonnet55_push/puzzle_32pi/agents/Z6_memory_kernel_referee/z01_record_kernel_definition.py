#!/usr/bin/env python3
"""z01: WHAT IS THE RECORD'S MEMORY KERNEL?  Re-derive, from the record's own action, the support, the normalisation,
the moments M0 and M1, the closed forms, the two regimes, and the (2/3) in M1 = (2/3) c/a0.  This fixes the object that lane X3 identified with
Sciama's kernel.  Sources read (record): opus_48_extended_research/papers/RAPIDITY_GAP_MI_ACTION.md (v6, eqs 1-15, 22-23),
real_research/reviews/mi_a0_from_one_line_2026.py, mi_N_count_and_kappa_iff_2026.py, mi_kernel_localisation_2026.py, mi_local_source_for_K_2026.py.
The record's action:  S = -m c^2 Int[ mu(Theta) dtau + (1-mu(Theta)) dt ],   Theta(tau) = Int_0^inf ds K(s) arccosh(-u(tau).u(tau-s)/c^2).
K has dimension 1/time, s is PROPER-TIME LAG ALONG THE PARTICLE'S OWN WORLDLINE; there is no G, no matter density, no spatial integral in the action."""
import sympy as sp
from sympy import pi, sqrt, Rational as Rat, symbols
import mpmath as mp
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    """a control PASSES (is 'rejected' = ok) when the mutated claim is FALSE"""
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


def zero(e): return sp.simplify(e) == 0


mp.mp.dps = 30
s, tau, w, Om, lam, N, T = symbols('s tau w Omega lambda N T', positive=True)

print("== K1: the rapidity gap and its short-lag limit (record eqs 3-6) ==")
# circular worldline, c = 1, rapidity parametrisation v = tanh w, gamma = cosh w
minus1 = sp.sinh(w) ** 2 * (1 - sp.cos(sp.cosh(w) * Om * s))            # = -u.u' - 1
theta = 2 * sp.asinh(sp.sqrt(minus1 / 2))
chk("cosh(theta) - 1 = -u.u' - 1 exactly (definition of the rapidity gap)", zero(sp.cosh(theta) - 1 - minus1))
th_ser = sp.series(2 * sp.asinh(sp.sinh(w) * sp.sin(sp.cosh(w) * Om * s / 2)), s, 0, 2).removeO()
a_proper = sp.cosh(w) * sp.sinh(w) * Om                                   # |a| = gamma^2 Omega v
chk("theta(s) -> |a| s as s -> 0 with |a| = gamma^2 Omega v (proper acceleration = rate of rapidity accumulation)", zero(th_ser - a_proper * s))

print("\n== K2: support, normalisation and moments of the record's kernel ==")
Kexp = N / lam * sp.exp(-s / lam)                                         # the record's minimal kernel (eq. before 8)
M0 = sp.integrate(Kexp, (s, 0, sp.oo)); M1 = sp.integrate(s * Kexp, (s, 0, sp.oo))
print("   (declared, not a check) support: s in (0, inf) in PROPER-TIME lag along the particle's own worldline (causal by fiat); dimension of K = 1/time because Theta is dimensionless")
chk("zeroth moment M0 = int K ds = N (a free dimensionless weight, NOT fixed to 1)", zero(M0 - N))
chk("first moment  M1 = int s K ds = N lambda (record: M1 = N lambda; N = M1/lambda)", zero(M1 - N * lam))
# record's other two shapes (gamma-2, box), normalised to the SAME M1 and the same M0 = N
K_g2 = N * s / lam ** 2 * sp.exp(-s / lam)
K_box = N / T * sp.Piecewise((1, s <= T), (0, True))
chk("gamma-2 kernel N s e^{-s/lam}/lam^2: M0 = N, M1 = 2 N lam", zero(sp.integrate(K_g2, (s, 0, sp.oo)) - N) and zero(sp.integrate(s * K_g2, (s, 0, sp.oo)) - 2 * N * lam))
chk("box kernel N/T on [0,T]: M0 = N, M1 = N T/2", zero(sp.integrate(N / T, (s, 0, T)) - N) and zero(sp.integrate(s * N / T, (s, 0, T)) - N * T / 2))

print("\n== K3: the two regimes of Theta on a circular orbit (record eq 8; non-relativistic theta = 2 (v/c)|sin(Omega s/2)|) ==")
x = symbols('x', positive=True)


def theta_quad(Nv, lamv, Omv, vv):
    """Theta = int_0^inf (N/lam) e^{-s/lam} 2 v |sin(Om s/2)| ds, by quadrature with breakpoints at the zeros of sin"""
    f = lambda ss: (Nv / lamv) * mp.e ** (-ss / lamv) * 2 * vv * abs(mp.sin(Omv * ss / 2))
    period = 2 * mp.pi / Omv
    tot = mp.mpf(0); a = mp.mpf(0)
    jmax = int(min(400, max(4, 60 * lamv / period)))
    for j in range(1, jmax + 1):
        b = j * period
        tot += mp.quad(f, [a, (a + b) / 2, b]); a = b
    return tot


def theta_closed(Nv, lamv, Omv, vv):
    xx = lamv * Omv
    return 4 * Nv * vv * xx * mp.coth(mp.pi / xx) / (4 + xx ** 2)


ok = True
for xv in (mp.mpf("0.05"), mp.mpf(1), mp.mpf(3)):
    q = theta_quad(mp.mpf(1), xv, mp.mpf(1), mp.mpf("0.001")); cl = theta_closed(mp.mpf(1), xv, mp.mpf(1), mp.mpf("0.001"))
    ok = ok and abs(q / cl - 1) < 1e-12
    print(f"   x = {mp.nstr(xv, 3):>5s}: quadrature {mp.nstr(q, 12)}  closed form (8) {mp.nstr(cl, 12)}")
chk("closed form (8) Theta = (4 N v/c) x coth(pi/x)/(4 + x^2) reproduced by direct quadrature of the kernel against the exact rapidity gap (x = 0.05, 1, 3)", ok)
mp.mp.dps = 30
xs, cs = symbols('xs cs', positive=True)
short = sp.limit(4 * xs * sp.coth(sp.pi / xs) / (4 + xs ** 2) / xs, xs, 0, '+')
chk("short memory x -> 0: Theta -> N lambda Omega v/c = M1 |a|/c  (only M1 survives)", short == 1)
long_ = sp.limit(4 * xs * sp.coth(sp.pi / xs) / (4 + xs ** 2), xs, sp.oo)
chk("long memory x -> oo: Theta -> (4 N/pi)(v/c) (a function of SPEED; only M0 = N survives)", zero(long_ - 4 / pi))
ctrl("mutation: long-memory limit 2N/pi instead of 4N/pi", zero(long_ - 2 / pi))
# a wrong closed form must be detected by the quadrature
wrong = lambda Nv, lamv, Omv, vv: 4 * Nv * vv * (lamv * Omv) * mp.coth(mp.pi / (lamv * Omv)) / (2 + (lamv * Omv) ** 2)
ctrl("mutation: closed form with (2 + x^2) in the denominator agrees with the quadrature",
     abs(theta_quad(mp.mpf(1), mp.mpf(1), mp.mpf(1), mp.mpf("0.001")) / wrong(mp.mpf(1), mp.mpf(1), mp.mpf(1), mp.mpf("0.001")) - 1) < 1e-6)

print("\n== K4: where the (2/3) in M1 = (2/3) c/a0 comes from: the memory-force renormalisation of the ACTION (not of the kernel) ==")
Y = symbols('Y', positive=True)
mu2 = sqrt((-1 + sqrt(1 + 4 * Y ** 4)) / 2) / Y                              # record eq (14)
mueff = mu2 + Y * sp.diff(mu2, Y) / 2                                        # record eq (12): g_bar = g_obs [mu + (Y/2) mu']
lim_mu = sp.limit(mu2 / Y, Y, 0, '+'); lim_eff = sp.limit(mueff / Y, Y, 0, '+')
chk("deep limit: mu_2 -> Y (deep MOND) and mu_eff = mu + (Y/2) mu' -> (3/2) Y, hence g_obs^2 = (2/3) a0 g_bar", lim_mu == 1 and lim_eff == Rat(3, 2))
ctrl("mutation: without the memory force (mu_eff = mu) the deep-limit coefficient is 3/2", lim_mu == Rat(3, 2))
chk("newtonian limit preserved: mu_eff -> 1 as Y -> oo", sp.limit(mueff, Y, sp.oo) == 1)
a0s, cc = symbols('a0 c', positive=True)
M1_req = Rat(2, 3) * cc / a0s
chk("the renormalised requirement is M1 = (2/3) c/a0 [a0_eff = (2/3) c/M1 must equal a0]; the pre-correction requirement (record v1/v2) was M1 = c/a0", zero(M1_req * 3 / 2 - cc / a0s))

print("\n== K5: numbers (record constants) and the iff ==")
C = mp.mpf("2.99792458e8"); LAM = mp.mpf("1.0908e-52"); G = mp.mpf("6.67430e-11")
RHO_L = LAM * C ** 2 / (8 * mp.pi * G); A0 = C ** 2 * mp.sqrt(LAM / (32 * mp.pi)); T_L = 1 / mp.sqrt(G * RHO_L)
GYR = mp.mpf("3.1557e16"); YR = mp.mpf("3.1557e7")
M1n = 2 * C / (3 * A0)
print(f"   a0 = {mp.nstr(A0, 6)} m/s^2 ; t_Lambda = {mp.nstr(T_L/GYR, 6)} Gyr ; M1 = (2/3)c/a0 = {mp.nstr(M1n, 6)} s = {mp.nstr(M1n/GYR, 6)} Gyr ; c/a0 = {mp.nstr(C/A0, 6)} s = {mp.nstr(C/A0/GYR, 6)} Gyr")
chk("M1 = (4/3) t_Lambda exactly (record iff: kappa = 1/2)", abs(M1n / T_L - Rat(4, 3)) < 1e-25)
chk("c/a0 = 2 t_Lambda, i.e. the Rindler distance c^2/a0 = 2 R*, R* = c t_Lambda = c/sqrt(G rho_Lambda)", abs(C / A0 / T_L - 2) < 1e-25)

print("\n== K6: N = M0 is the kernel WEIGHT; reproduce the record's N >= 2.1e6 (ephemeris) to fix the reading of the normalisation ==")
GM = mp.mpf("1.32712440018e20"); AU = mp.mpf("1.495978707e11"); BOUND = mp.mpf("3.66e-14")
PL = {"Mercury": (mp.mpf("0.387098"), mp.mpf("4.7362e4")), "Earth": (mp.mpf("1"), mp.mpf("2.9785e4")),
      "Mars": (mp.mpf("1.523679"), mp.mpf("2.4077e4")), "Saturn": (mp.mpf("9.53667"), mp.mpf("9.68e3"))}
Nmin = {}
for nm, (aau, vp) in PL.items():
    g = GM / (aau * AU) ** 2
    Th_min = (g / (32 * BOUND)) ** mp.mpf("0.25")        # record: Delta = g/(32 Theta^4) <= bound (large-Theta regime, alpha = 2)
    Nmin[nm] = Th_min * mp.pi * C / (4 * vp)             # long memory Theta = (4N/pi)(v/c)
    print(f"   {nm:8s}: g = {mp.nstr(g, 4)} m/s^2, Theta_min = {mp.nstr(Th_min, 5)}, N_min = {mp.nstr(Nmin[nm], 5)}")
Nbind = max(Nmin.values())
chk("tightest planet is Mercury and N_min = 2.1e6 (record: N >= 2.1e6, lambda <= 1.0e12 s = 3.2e4 yr): the record's kernel has weight N = M0 >> 1", max(Nmin, key=Nmin.get) == "Mercury" and abs(Nbind / mp.mpf("2.1e6") - 1) < 0.05, f"N_min(Mercury) = {mp.nstr(Nbind, 6)}")
lam_max = M1n / Nbind
chk("hence lambda_max = M1/N_min = 1.0e12 s = 3.2e4 yr", abs(lam_max / mp.mpf("1.0e12") - 1) < 0.05, f"{mp.nstr(lam_max, 5)} s = {mp.nstr(lam_max/YR, 5)} yr")
ctrl("mutation: unit weight N = 1 would satisfy the ephemeris bound", 1 >= Nbind)

print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
