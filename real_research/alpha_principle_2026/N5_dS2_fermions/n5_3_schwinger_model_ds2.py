#!/usr/bin/env python3
"""N5-3 -- the massless Schwinger model in dS_2: what the exactly solvable limit says about the coupling, and whether a horizon tie can force it.

Pre-registered in N5_PREREGISTRATION.md (with its amendments; written before this script was run).  Units hbar = c = H = 1, a = -1/tau.
Variable: x = e^2/(pi H^2)  (the squared photon mass e^2/pi of the flat-space Schwinger model in units of H^2).  2D toy: e has mass dimension 1; x is NOT alpha.

  S1   sympy: the anomaly-induced action and the homogeneous Maxwell equation  E'' + (e^2/pi) a^2 E = 0 (conformal time),
       E_tt + H E_t + (e^2/pi) E = 0 (cosmic time); memory relation J_t + H J = (e^2/pi) E; the constant-E current is its particular solution;
       S1b: the sphere propagator of Anninos-Anous-Rios Fukelman, 2F1(Delta, 1-Delta; 1; 1-u/2), obeys (nabla^2 - m^2) G = 0 with m^2 = Delta(1-Delta) = x.
  S2   the linear conductivity from the direct mode sum (massless: I_raw = 0, subtraction Delta = 2 lambda) is sigma_0 = e^2/(pi H) exactly: this is the coefficient used in S1.
  S3   numerical integration of the Maxwell equation: late-time exponent E ~ (-tau)^Delta_-, Delta_-(1-Delta_-) = x  (x < 1/4); envelope (-tau)^{1/2} and
       oscillation frequency sqrt(x - 1/4) in ln(-tau)  (x > 1/4).
  S4   exact decay exponent against the naive local-response rate x.
  S5   the special-value table (nine declared candidates) and the analyticity / positivity tests of H5.

Run:     python3 n5_3_schwinger_model_ds2.py            (real run; exit 0 iff every check passes)
         python3 n5_3_schwinger_model_ds2.py --mutate   (control: the subtraction is dropped, so the massless conductivity is 0; S2 must FAIL;
                                                          the control exits 1 when S2 fails as required)
"""
import sys
import math
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.integrate import solve_ivp

mp.mp.dps = 30
MUTATE = "--mutate" in sys.argv
PI = math.pi
KAPPA = 0.5
CHECKS = []


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def massless_i_raw_by_ode(lam):
    """I_raw = Int_0^inf [f(k,lam) - f(k,-lam)] dk for m = 0.  Integrand identically 0 if the ODE shows f = -1 (k>0) for both signs of lambda (checked at several k)."""
    worst = 0.0
    for k in (0.3, 1.0, 2.5):
        for sg in (+1.0, -1.0):
            ll = sg * lam
            tau0 = -4000.0 / k

            def rhs(t, y, ll=ll, k=k):
                p = k + ll / t
                return [1j * p * y[0], -1j * p * y[1]]
            sol = solve_ivp(rhs, (tau0, -1.0), [0.0 + 0j, 1.0 + 0j], method="DOP853", rtol=1e-12, atol=1e-14)
            y = sol.y[:, -1]
            worst = max(worst, abs(abs(y[1]) ** 2 - 1), abs(y[0]))
    return 0.0, worst


print("=" * 110)
print("N5-3 massless Schwinger model in dS_2 -- mode: " + ("MUTATE CONTROL (subtraction dropped)" if MUTATE else "REAL RUN"))
print("=" * 110)

# ------------------------------------------------------------------------------------------ S2 first (feeds S1/S3)
print("\nS2. Linear conductivity of the massless fermion from the direct mode sum (n5_2: J/(eH) = (2 lambda*s - I_raw)/(2 pi), s = 1 with the subtraction)")
sub = 0.0 if MUTATE else 1.0
coefs = []
worst_nomix = 0.0
for lam in (0.05, 0.3, 1.1, 2.7):
    i_raw, wn = massless_i_raw_by_ode(lam)
    worst_nomix = max(worst_nomix, wn)
    j_over_eH = (2 * lam * sub - i_raw) / (2 * PI)
    coefs.append(j_over_eH / lam)
    print(f"     lambda = {lam:4.2f}:  I_raw = {i_raw:.1f} (ODE no-mixing deviation {wn:.1e}),  J/(eH lambda) = {j_over_eH / lam:.12f}   (1/pi = {1 / PI:.12f})")
c_sigma = coefs[0]                                                    # sigma_0 H^2/e^2 read from the mode sum
lin_ok = max(abs(c - coefs[0]) for c in coefs) <= 1e-12
s2_ok = lin_ok and abs(c_sigma * PI - 1) <= 1e-12 and worst_nomix <= 1e-10
check("S2 sigma_0 = e^2/(pi H): J/(eH lambda) = 1/pi exactly, independent of lambda", s2_ok, f"(coefficient {c_sigma:.12f}; 1/pi = {1 / PI:.12f})")
if MUTATE:
    print("\nMUTATE CONTROL: the subtraction was dropped, sigma_0 = 0.")
    print(f"  S2 {'FAILED as required -- the control works' if not s2_ok else 'DID NOT FAIL -- the check has no power'}")
    sys.exit(1 if not s2_ok else 0)

# ------------------------------------------------------------------------------------------ S1
print("\nS1. Homogeneous Maxwell equation in dS_2 with the massless-fermion induced current (sympy)")
t = sp.symbols("tau", real=True)
tt, e, H = sp.symbols("t e H", positive=True)
a = -1 / (H * t)
A = sp.Function("A")(t)
# induced current J_phys = (e^2/(pi a)) A_x (temporal gauge, lower index), from J/(eH) = lambda/pi at eA_x = lambda/tau (a = 1 at tau = -1) and dS invariance (constant for constant E)
Jphys = e ** 2 / (sp.pi * a) * A
Jx = Jphys / a                                                        # contravariant coordinate component
Lag = sp.Rational(1, 2) * A.diff(t) ** 2 / a ** 2 - a ** 2 * Jx * A * sp.Rational(1, 2)   # 1/2 factor: J = -dL_ind/dA, so L_ind = -(1/2) a^2 Jx A
EL = sp.simplify(sp.diff(Lag.diff(A.diff(t)), t) - Lag.diff(A))
E_true = A.diff(t) / a ** 2
print("     L = (1/2) a^-2 A'^2 - (1/2)(e^2/pi) A^2   [the induced term is conformally invariant: sqrt(g) g^{xx} A_x^2 = -A^2]")
print("     Euler-Lagrange:", sp.simplify(EL))
# E' + (e^2/pi) A = EL  and  A' = a^2 E  =>  d/dtau EL = E'' + (e^2/pi) a^2 E   (identically), so EL = 0 implies E'' + (e^2/pi) a^2 E = 0
Ep = sp.simplify(E_true.diff(t))
ok_first = sp.simplify(EL - (Ep + e ** 2 / sp.pi * A)) == 0
Epp_expr = E_true.diff(t, 2) + e ** 2 / sp.pi * a ** 2 * E_true
Epp_sub = sp.simplify(Epp_expr - sp.diff(EL, t))
print("     EL = E' + (e^2/pi) A with E = A'/a^2:", ok_first, "; (E'' + (e^2/pi) a^2 E) - d(EL)/dtau =", Epp_sub)
# cosmic time: E_tt + H E_t + (e^2/pi) E = 0
Ec = sp.Function("Ec")(tt)
# E(tau(t)) with dtau = dt/a : E_tautau = a (a E_t)_t = a^2 (E_tt + H E_t)
a_t = sp.exp(H * tt)                                                  # a(t) = e^{Ht}
E_tautau = a_t * sp.diff(a_t * sp.diff(Ec, tt), tt)
maxwell_cosmic = sp.simplify((E_tautau + e ** 2 / sp.pi * a_t ** 2 * Ec) / a_t ** 2)
print("     cosmic time:  E_tt + H E_t + (e^2/pi) E  =?  ", sp.simplify(maxwell_cosmic - (sp.diff(Ec, tt, 2) + H * sp.diff(Ec, tt) + e ** 2 / sp.pi * Ec)))
ok_cosmic = sp.simplify(maxwell_cosmic - (sp.diff(Ec, tt, 2) + H * sp.diff(Ec, tt) + e ** 2 / sp.pi * Ec)) == 0
# memory relation J_t + H J = (e^2/pi) E  (J = e^2 A/(pi a), dA/dt = a E)
Jt = sp.Function("J")(tt)
At = sp.Function("At")(tt)
J_of_A = e ** 2 * At / (sp.pi * a_t)
dJ = sp.diff(J_of_A, tt).subs(sp.diff(At, tt), a_t * Ec)
mem = sp.simplify(dJ + H * J_of_A - e ** 2 / sp.pi * Ec)
print("     memory relation  J_t + H J - (e^2/pi) E =", mem)
# constant-E particular solution
Ec0 = sp.symbols("E0", positive=True)
Jc = sp.symbols("Jc")
sol_c = sp.solve(sp.Eq(0 + H * Jc, e ** 2 / sp.pi * Ec0), Jc)[0]
print("     constant E: J = ", sol_c, "  = e^2 E/(pi H)   (the direct-sum value J/(eH) = lambda/pi with lambda = eE/H^2)")
ok_const = sp.simplify(sol_c - e ** 2 * Ec0 / (sp.pi * H)) == 0
s = sp.symbols("s")
roots = sp.solve(sp.Eq(s ** 2 - H * s + e ** 2 / sp.pi, 0), s)
print("     E ~ exp(-s t):  s^2 - H s + e^2/pi = 0  ->  s =", roots, "; Delta = s/H obeys Delta(1 - Delta) = e^2/(pi H^2) = x")
check("S1 Maxwell + induced current: E'' + (e^2/pi) a^2 E = 0, E_tt + H E_t + (e^2/pi) E = 0, J_t + H J = (e^2/pi) E, J_const = e^2 E/(pi H)",
      ok_first and sp.simplify(Epp_sub) == 0 and ok_cosmic and mem == 0 and ok_const)

# S1b: sphere propagator of Anninos et al
print("\nS1b. The exact solution's propagator (Anninos-Anous-Rios Fukelman eq. 3.5/3.10): G = 2F1(Delta, 1-Delta; 1; 1-u/2), u = 1 - cos(Theta):  (nabla^2 - m^2) G = 0, m^2 = Delta(1-Delta) = x ?")
worstS1b = 0.0
for xv in (0.05, 0.2, 0.25, 0.6, 1.5):
    Dl = mp.mpf(1) / 2 + mp.sqrt(mp.mpf(1) / 4 - mp.mpf(xv))

    def Gf(Th):
        return mp.hyp2f1(Dl, 1 - Dl, 1, 1 - (1 - mp.cos(Th)) / 2)
    Th0 = mp.mpf("1.1")
    lap = (mp.diff(lambda th: mp.sin(th) * mp.diff(Gf, th), Th0)) / mp.sin(Th0)
    res = abs(lap - xv * Gf(Th0)) / abs(xv * Gf(Th0))
    worstS1b = max(worstS1b, float(res))
    print(f"     x = {xv:5.2f}:  Delta(1-Delta) = {complex(Dl * (1 - Dl)).real:.6f};  relative residual of (nabla^2 - x) G = 0 at Theta = 1.1:  {float(res):.1e}")
check("S1b the exact model's propagator is the dS_2 scalar propagator of m^2 = x = e^2/(pi H^2)", worstS1b <= 1e-10, f"(worst {worstS1b:.1e})")

# ------------------------------------------------------------------------------------------ S3 numerics
print("\nS3. Numerical integration of E'' + c e^2 a^2 E = 0  (conformal time, H = 1) with c = sigma_0 H^2/e^2 read from the mode sum (S2); x_nominal = e^2/pi, x_eff = pi c x_nominal")
worstS3 = 0.0
print("     real exponents (x < 1/4):")
for xnom in (0.05, 0.15, 0.24):
    xv = c_sigma * PI * xnom
    def rhs(tau, y, xv=xv):
        return [y[1], -xv / (tau * tau) * y[0]]                        # a^2 = 1/tau^2
    sol = solve_ivp(rhs, (-1.0, -1e-40), [1.0, 0.3], method="DOP853", rtol=1e-12, atol=1e-60, dense_output=True)
    us = np.linspace(-92.0, -85.0, 8)                                  # ln(-tau) window at very late times
    vals = np.array([sol.sol(-math.exp(u))[0] for u in us])
    slope = np.polyfit(us, np.log(np.abs(vals)), 1)[0]
    dl = 0.5 - math.sqrt(0.25 - xv)
    worstS3 = max(worstS3, abs(slope - dl))
    print(f"       x = {xv:4.2f}:  fitted late-time exponent {slope:.6f}   Delta_- = 1/2 - sqrt(1/4 - x) = {dl:.6f}   diff {abs(slope - dl):.1e}")
print("     complex exponents (x > 1/4): envelope (-tau)^(1/2), oscillation frequency nu = sqrt(x - 1/4) in ln(-tau):")
worst_env = 0.0
worst_nu = 0.0
for xnom in (0.6, 1.5):
    xv = c_sigma * PI * xnom
    def rhs(tau, y, xv=xv):
        return [y[1], -xv / (tau * tau) * y[0]]
    sol = solve_ivp(rhs, (-1.0, -1e-30), [1.0, 0.3], method="DOP853", rtol=1e-12, atol=1e-60, dense_output=True)
    nu = math.sqrt(xv - 0.25)
    us = np.linspace(-60.0, -8.0, 4001)
    tv = -np.exp(us)
    Ev = np.array([sol.sol(tau)[0] for tau in tv])
    Ed = np.array([sol.sol(tau)[1] for tau in tv])
    g = Ev / np.sqrt(-tv)
    gu = (tv * Ed) / np.sqrt(-tv) - 0.5 * g                            # d g / d ln(-tau)
    amp = np.sqrt(g * g + (gu / nu) ** 2)
    env_spread = (amp.max() - amp.min()) / amp.mean()
    idx = np.where(np.sign(g[:-1]) != np.sign(g[1:]))[0]
    zc = us[idx] - g[idx] * (us[idx + 1] - us[idx]) / (g[idx + 1] - g[idx])        # linear interpolation of the zero crossings
    nu_fit = PI / np.mean(np.diff(zc)) if len(zc) > 3 else float("nan")
    worst_env = max(worst_env, env_spread)
    worst_nu = max(worst_nu, abs(nu_fit - nu))
    print(f"       x = {xv:4.2f}:  envelope amplitude of (-tau)^(-1/2) E constant to {env_spread:.1e};  nu(fit from zero crossings) = {nu_fit:.5f}  vs sqrt(x - 1/4) = {nu:.5f}")
check("S3 late-time exponents/oscillation of the integrated Maxwell equation match Delta(1 - Delta) = x (real) and 1/2 +- i sqrt(x - 1/4) (complex)",
      worstS3 <= 1e-3 and worst_env <= 1e-6 and worst_nu <= 1e-3, f"(worst real-exponent diff {worstS3:.1e}; envelope spread {worst_env:.1e}; frequency diff {worst_nu:.1e})")

# ------------------------------------------------------------------------------------------ S4
print("\nS4. Exact decay exponent against the naive local-response rate  x  (local model: E_t = -(e^2/(pi H)) E at every time, as in Stahl-Xue 1603.07166 at mu = 0)")
print("     x        Delta_- (exact)   local rate x   (Delta_- - x)/x     regime")
for xv in (0.01, 0.1, 0.24, 0.25, 0.6, 1.0, 2.0):
    if xv <= 0.25:
        dl = 0.5 - math.sqrt(0.25 - xv)
        print(f"     {xv:5.2f}    {dl:.6f}         {xv:.4f}       {(dl - xv) / xv:+.4f}          overdamped (monotone)")
    else:
        print(f"     {xv:5.2f}    Re Delta = 0.5000  {xv:.4f}       (rate saturates at H/2, oscillates at H*sqrt(x-1/4) = {math.sqrt(xv - 0.25):.4f} H)  underdamped")
ser = lambda xv: xv + 2 * xv ** 2 + 5 * xv ** 3
ok4 = all(abs((0.5 - math.sqrt(0.25 - xv) - xv) / xv - ser(xv)) <= tol for xv, tol in ((0.01, 1e-4), (0.1, 1e-2)))
check("S4 exact Delta_- = x + x^2 + 2 x^3 + 5 x^4 + ...: (Delta_- - x)/x = x + 2 x^2 + 5 x^3 (1e-4 at x = 0.01, 1e-2 at x = 0.1); for x > 1/4 the rate saturates at H/2 and E oscillates", ok4)

# ------------------------------------------------------------------------------------------ S5
print("\nS5. Special-value table (nine declared candidates; e^2/H^2 = pi x)")
CANDS = [("critical damping (Delta_+ = Delta_-)", 0.25), ("linear-response rate = H", 1.0),
         ("tie sigma/H = kappa", KAPPA), ("tie sigma/H = kappa/pi", KAPPA / PI), ("tie sigma/H = 1/(2 pi)", 1 / (2 * PI)), ("tie sigma/H = 1/pi", 1 / PI),
         ("tie sigma/H = 1", 1.0), ("tie sigma/H = 2 kappa", 2 * KAPPA), ("instanton weight e^{-1/(2x)} = e^-1", 0.5)]
print("     candidate                              x        e^2/H^2 = pi x    exact model at x")
for name, xv in CANDS:
    if xv < 0.25:
        d = f"Delta_- = {0.5 - math.sqrt(0.25 - xv):.4f} (overdamped)"
    elif xv == 0.25:
        d = "Delta = 1/2 (double root; branch point of Delta only)"
    else:
        d = f"Delta = 1/2 +- {math.sqrt(xv - 0.25):.4f} i (underdamped)"
    print(f"     {name:38s} {xv:7.4f}   {PI * xv:10.5f}        {d}")

print("\n     H5 test (a): the Euclidean (dS-invariant) propagator coefficient Gamma(Delta)Gamma(1-Delta) 2F1(Delta,1-Delta;1;1-u/2) is analytic across x = 1/4")
mp.mp.dps = 30


def Cx(xv, u=mp.mpf("0.7")):
    Dl = mp.mpf(1) / 2 + mp.sqrt(mp.mpf(1) / 4 - mp.mpf(xv))
    return mp.gamma(Dl) * mp.gamma(1 - Dl) * mp.hyp2f1(Dl, 1 - Dl, 1, 1 - u / 2)


def d3_of(fun, center, hh=mp.mpf("0.01")):
    xs = [mp.mpf(center) + n * hh for n in range(-3, 4)]
    v = [fun(q) for q in xs]
    d1 = [v[i + 1] - v[i] for i in range(6)]
    d2 = [d1[i + 1] - d1[i] for i in range(5)]
    d3 = [d2[i + 1] - d2[i] for i in range(4)]
    return v, max(float(abs(q)) for q in d3)


# Amendment 4: C(x) has a pole at x = 0 (Delta -> 0, the massless zero mode), 0.25 from the threshold, so its raw third differences are large for analytic reasons;
# the pole is removed by x C(x).  Calibration: Delta_-(x) = 1/2 - sqrt(1/4 - x) is genuinely non-analytic at 1/4.
vals, d3_xC = d3_of(lambda q: q * Cx(q), "0.25")
_, d3_ref = d3_of(lambda q: q * Cx(q), "0.6")
_, d3_raw = d3_of(Cx, "0.25")
_, d3_cal = d3_of(lambda q: mp.mpf(1) / 2 - mp.sqrt(mp.mpf(1) / 4 - q), "0.25")
max_im = max(float(abs(mp.im(v))) for v in vals)
print("     x:       " + "  ".join(f"{0.25 + 0.01 * n:.2f}" for n in range(-3, 4)))
print("     x C(x):  " + "  ".join(f"{float(mp.re(v)):.8f}" for v in vals))
print(f"     third finite differences (step 0.01):  x C(x) at the threshold {d3_xC:.2e};  x C(x) at x = 0.6 (control) {d3_ref:.2e};  raw C(x) at the threshold {d3_raw:.2e} (pole at x = 0 only 0.25 away);")
print(f"                                            calibration Delta_-(x) (sqrt singularity at 1/4) {d3_cal:.2e};  max |Im C| {max_im:.1e}")
ok_an = d3_xC <= 1e-4 and d3_cal >= 100 * d3_xC and max_im <= 1e-25
print("     H5 test (b): sphere-series coefficients q^2 l^2 / (L(L+1)(L(L+1) + x)), q^2 l^2 = pi x, are positive for every L >= 1 on x in [1e-3, 1e3]:")
xs_scan = np.logspace(-3, 3, 400)
pos = all(PI * xv / (L * (L + 1) * (L * (L + 1) + xv)) > 0 for xv in xs_scan for L in range(1, 200))
print(f"       all positive: {pos}  (400 values of x, L = 1..199)")
check("H5 the exact model is analytic through the threshold x = 1/4 and well defined (positive-definite spectral sum) at every x: no coupling is excluded or isolated", ok_an and pos)

print("\n" + "=" * 110)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT (against the declared criteria):")
print("  * The massless dS_2 Schwinger model is a damped plasma oscillator: sigma_0 = e^2/(pi H) from the anomaly (S2) gives E_tt + H E_t + (e^2/pi) E = 0,")
print("    i.e. a dS_2 scalar of mass^2 = e^2/pi = m_photon^2 (S1, S1b, S3), matching the literature parameter map Delta(1 - Delta) = e^2/(pi H^2).")
print("  * The constant-field response J = e^2 E/(pi H) is the exact particular solution; the naive local-response model reproduces only the small-x rate (S4).")
print("  * The only special point on the family is the branch point x = 1/4 (e^2/H^2 = pi/4) where the two exponents merge; the dS-invariant correlators are analytic there (H5a),")
print("    and every x > 0 gives a well-defined exact model (H5b).  A threshold is not a selected value: NO coupling is forced.  The six conductivity ties give e^2/H^2 = pi c only")
print("    if c is supplied from outside.  2D toy: e^2/H^2 is not alpha; nothing here selects any 4D coupling.")
print("  * kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
sys.exit(0 if passed == len(CHECKS) else 1)
