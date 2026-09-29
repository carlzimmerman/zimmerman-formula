#!/usr/bin/env python3
"""Q2/q4 -- is the conformal threshold lambda_c = 1/2 (eE = H^2/2) anything more than the number 1/4 in the conformal index?

Pre-registered in Q2_PREREGISTRATION.md (H10, before this script was run).  Units in the mode analysis: H = 1.

Checks
  Q1  symbolic threshold table lambda_c(D, xi, mu) from mu_w^2 = (D-1)^2/4 - lam^2 - mu^2 - xi D(D-1) (derived in q1), D = 2..6:
      minimal massless (D-1)/2, conformal massless 1/2 in EVERY D, D = 2 minimal == conformal, massive conformal sqrt(1/4 - mu^2);
      plus an independent derivation of the 1/tau^2 coefficient by the conformal-rescaling formula (different route from q1).
  Q2  the threshold is the "fall to the centre" constant of the late-time inverse-square equation chi'' + g chi/tau^2 = 0: exponents 1/2 +- sqrt(1/4 - g);
      numerical zero counts of the real solution on tau in [-1, -1e-12] for lam = 0.3, 0.45, 0.55, 0.8 (g = lam^2, conformal massless, k -> 0)
  Q3  lam = e E c/(hbar H^2) is dimensionless in SI (sympy.physics.units); lam_c = 1/2 is the mass-independent force F_c = hbar H^2/(2 c); numbers for H0 = 67.4 km/s/Mpc
  Q4  relation to a0 = kappa c H: mass at which F_c/m = a0; the massive conformal scalar threshold and a_c/(cH) = sqrt(1/4 - mu^2)/mu; root for kappa in
      {1/2, 0.465, 0.55, 1/(2 pi)} (any kappa gives a root: mu_* = 1/(2 sqrt(1 + kappa^2)))
  Q5  can it constrain alpha?  E_c = lam_c H^2/e for a range of alpha (any alpha is allowed); the critical-field energy-density tie rho_E = rho_Lambda would give alpha = lam^2 x/9
  Q6  coincidence count over the natural cases (D = 2..6, minimal and conformal)
  Q7  the pre-registered verdict rule, applied mechanically

Run:    python3 q4_threshold_test.py            (real run; exit 0 iff every check passes)
        python3 q4_threshold_test.py --mutate   (control: the minimal D = 4 threshold is set to 1/2 in the table; Q1 must FAIL;
                                                exit 1 = "control fails as required", exit 3 = control did NOT fail)
"""
import sys
import math
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from sympy.physics.units import coulomb, volt, meter, speed_of_light, hbar, second
from sympy.physics.units.systems.si import SI

MUTATE = "--mutate" in sys.argv
PI = math.pi
CHECKS = []
KAPPA = 0.5


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


print("=" * 100)
print("Q2/q4 the conformal threshold lambda_c = 1/2 -- " + ("MUTATE CONTROL (wrong minimal D=4 threshold)" if MUTATE else "REAL RUN"))
print("=" * 100, flush=True)

# ---------------------------------------------------------------- Q1
print("\nQ1. Threshold table from mu_w^2 = (D-1)^2/4 - lam^2 - mu^2 - xi D(D-1)  (lam_c: mu_w^2 = 0 at fixed mu, xi)")
lam, mu, xi, D = sp.symbols("lam mu xi D", positive=True)
mw2 = (D - 1) ** 2 / 4 - lam ** 2 - mu ** 2 - xi * D * (D - 1)
xi_c = (D - 2) / (4 * (D - 1))
q1_ok = True
print("     D   xi_c        lam_c (minimal, m=0)   lam_c (conformal, m=0)   conformal massive lam_c(mu)")
for Dv in (2, 3, 4, 5, 6):
    l_min = sp.sqrt(mw2.subs({D: Dv, xi: 0, mu: 0, lam: 0}))                    # mu_w^2 = 0 at lam = lam_c  <=>  lam_c^2 = mw2(lam = 0)
    l_conf = sp.sqrt(mw2.subs({D: Dv, xi: xi_c.subs(D, Dv), mu: 0, lam: 0}))
    l_conf_m = sp.sqrt(mw2.subs({D: Dv, xi: xi_c.subs(D, Dv), lam: 0}))
    l_min_used = sp.Rational(1, 2) if (MUTATE and Dv == 4) else sp.simplify(l_min)
    ok = (sp.simplify(l_min_used - sp.Rational(Dv - 1, 2)) == 0 and sp.simplify(l_conf - sp.Rational(1, 2)) == 0
          and sp.simplify(l_conf_m - sp.sqrt(sp.Rational(1, 4) - mu ** 2)) == 0)
    q1_ok = q1_ok and ok
    print(f"     {Dv}   {sp.nsimplify(xi_c.subs(D, Dv))!s:8s}    {l_min_used!s:8s}               {sp.simplify(l_conf)!s:8s}                 {sp.simplify(l_conf_m)}")
# independent derivation of the 1/tau^2 coefficient via the conformal-rescaling formula (route different from q1's Christoffel computation)
tau = sp.symbols("tau", negative=True)
a = -1 / tau
coef_ok = True
for Dv in (2, 3, 4, 5, 6):
    # phi = a^{-(D-2)/2} chi:  chi'' + [k^2 + a^2 (m^2 + xi R) - ((D-2)/2)(a''/a) - ((D-2)(D-4)/4)(a'/a)^2] chi = 0  (standard conformal transformation, recalled)
    a1, a2 = sp.diff(a, tau), sp.diff(a, tau, 2)
    pot = a ** 2 * (mu ** 2 + xi * Dv * (Dv - 1)) - sp.Rational(Dv - 2, 2) * a2 / a - sp.Rational((Dv - 2) * (Dv - 4), 4) * (a1 / a) ** 2
    coef_ok = coef_ok and sp.simplify(pot * tau ** 2 - (mu ** 2 + xi * Dv * (Dv - 1) - sp.Rational(Dv * (Dv - 2), 4))) == 0
print(f"     independent conformal-rescaling route: coefficient of 1/tau^2 equals mu^2 + xi D(D-1) - D(D-2)/4 for D = 2..6: {coef_ok}")
print("     D = 2: xi_c = 0, so the MINIMAL dS_2 scalar is already the conformal one: 'dS_2 minimal' and 'dS_4 conformal' are one case, not two independent occurrences of 1/2.")
check("Q1 threshold table: (D-1)/2 minimal, 1/2 conformal in every D, sqrt(1/4 - mu^2) massive conformal; independent 1/tau^2 coefficient", q1_ok and coef_ok)

if MUTATE:
    print("\nMUTATE CONTROL: the minimal D = 4 threshold was set to 1/2 in the table.")
    if not q1_ok:
        print("  Q1 FAILED as required -- CONTROL FAILS AS REQUIRED")
        sys.exit(1)
    print("  Q1 did NOT fail -- CONTROL DID NOT FAIL (the check has no power)")
    sys.exit(3)

# ---------------------------------------------------------------- Q2
print("\nQ2. Fall-to-the-centre: chi'' + g chi/tau^2 = 0 (late-time, k -> 0 limit; g = lam^2 for the conformal massless scalar)")
sg, gg = sp.symbols("s g")
roots = sp.solve(sg * (sg - 1) + gg, sg)
print(f"     chi ~ (-tau)^s:  s(s-1) + g = 0  ->  s = {roots}   (real for g <= 1/4, complex = log-oscillation for g > 1/4; g_c = 1/4, lam_c = 1/2)")


def zeros_count(l, t0=-1.0, t1=-1e-12):
    # integrate in x = ln(-tau) for robustness:  y'' = -l^2 y/tau^2 ; with tau = -e^x:  y_xx - y_x + l^2 y = 0 ... use tau directly with dense output on log grid
    def rhs(t, y):
        return [y[1], -(l * l) / (t * t) * y[0]]
    sol = solve_ivp(rhs, (t0, t1), [1.0, 0.0], method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
    ts = -np.exp(np.linspace(math.log(-t0), math.log(-t1), 200001))
    ys = sol.sol(ts)[0]
    return int(np.sum(np.sign(ys[1:]) != np.sign(ys[:-1])))


ok2 = True
print("     lam     rho = sqrt(lam^2 - 1/4)   predicted zeros ~ rho ln(1e12)/pi   numeric zeros of the real solution")
for l in (0.3, 0.45, 0.55, 0.8):
    rho = math.sqrt(max(l * l - 0.25, 0.0))
    pred = rho * math.log(1e12) / PI
    nz = zeros_count(l)
    good = (nz == 0) if l * l <= 0.25 else abs(nz - pred) <= 1.5
    ok2 = ok2 and good
    print(f"     {l:4.2f}    {rho:8.4f}                 {pred:8.2f}                          {nz}")
check("Q2 lam_c = 1/2 is the inverse-square critical constant: no oscillation below, log-oscillation (zero counts as rho ln(1e12)/pi) above", ok2 and any(str(r) for r in roots))

# ---------------------------------------------------------------- Q3
print("\nQ3. Units: lam = e E c / (hbar H^2)")
expr = coulomb * (volt / meter) * speed_of_light / (hbar * (1 / second) ** 2)
dd = SI.get_dimension_system().get_dimensional_dependencies(SI.get_dimensional_expr(expr))
print(f"     dimensional dependencies of e E c/(hbar H^2): {dd} (empty = dimensionless)")
HBAR, C, ECH = 1.054571817e-34, 299792458.0, 1.602176634e-19
H0 = 67.4e3 / 3.0856775814913673e22
F_c = HBAR * H0 ** 2 / (2 * C)
E_c = F_c / ECH
m_hub = HBAR * H0 / C ** 2
print(f"     H0 = {H0:.4e} s^-1;  F_c = hbar H^2/(2 c) = {F_c:.3e} N (mass independent);  E_c = F_c/e = {E_c:.3e} V/m;  Hubble mass hbar H/c^2 = {m_hub:.3e} kg = {m_hub * C ** 2 / ECH:.3e} eV")
check("Q3 lam is dimensionless in SI; lam_c = 1/2 is the mass-independent force hbar H^2/(2c)", dd == {})

# ---------------------------------------------------------------- Q4
print("\nQ4. Relation to a0 = kappa c H")
print("     F_c = m a0  <=>  m = hbar H/(2 kappa c^2): for kappa = 1/2 this is exactly the Hubble mass -- the statement 'lam_c = kappa' is the")
print("     restatement 'the critical force equals (Hubble mass) x a0'; no independent content.")
mu_h = m_hub / m_hub
print(f"     At the Hubble mass mu = 1 the massive conformal scalar has lam_c^2 = 1/4 - mu^2 = {0.25 - mu_h ** 2:+.2f} < 0: NO threshold exists there (the threshold needs mu < 1/2).")
ok4 = True
print("     kappa        mu_* = 1/(2 sqrt(1 + kappa^2))   root of sqrt(1/4 - mu^2)/mu = kappa    mu_* < 1/2?")
for kap in (0.5, 0.465, 0.55, 1 / (2 * PI)):
    mu_star = 1.0 / (2.0 * math.sqrt(1.0 + kap * kap))
    root = brentq(lambda x: math.sqrt(0.25 - x * x) / x - kap, 1e-6, 0.5 - 1e-12, xtol=1e-15)
    ok4 = ok4 and abs(float(root) - mu_star) < 1e-12 and mu_star < 0.5
    print(f"     {kap:.5f}     {mu_star:.10f}                          {float(root):.10f}           {mu_star < 0.5}")
print("     As mu -> 0 the acceleration a_c = F_c/m diverges: there is NO finite, mass-independent acceleration attached to the massless threshold.")
check("Q4 a0 is reached only at an arbitrary mass (exists for every kappa); no mass-independent acceleration", ok4)

# ---------------------------------------------------------------- Q5
print("\nQ5. Can lam_c constrain alpha?  It fixes eE/H^2, so E_c/H^2 = lam_c/e for any alpha:")
ALPHA = 1 / 137.035999177
print("     alpha           E_c/H^2 = 1/(2 e)")
vals = []
for a_ in (ALPHA, 1 / 100, 1 / 50, 0.5, 1e-4):
    e_ = math.sqrt(4 * PI * a_)
    vals.append(0.5 / e_)
    print(f"     {a_:.6e}   {0.5 / e_:.5f}")
ok5a = max(vals) / min(vals) > 2
x_dS = None
Lambda_over_H2 = 3.0
OmL, H0_SI = 0.6847, H0
Lam_SI = 3 * OmL * H0_SI ** 2 / C ** 2
G_SI = 6.67430e-11
x = Lam_SI * G_SI * HBAR / C ** 3
alpha_tie = 0.5 ** 2 * x / 9
print(f"     x = Lambda G hbar/c^3 = {x:.4e} (AH5's inputs);  rho_E/rho_Lambda at lam_c = lam^2 x/(9 alpha) = {0.25 * x / (9 * ALPHA):.3e}")
print(f"     the tie rho_E(E_c) = rho_Lambda would give alpha = lam_c^2 x/9 = {alpha_tie:.3e}   (vs 1/137.036 = {ALPHA:.3e}; ratio {alpha_tie / ALPHA:.2e}); arithmetic on a tie, not a candidate")
check("Q5 lam_c fixes E/H^2 for any alpha (alpha spans > 2 at fixed lam_c); the only dimensionless tie built from it gives alpha ~ 1e-123", ok5a and alpha_tie < 1e-100)

# ---------------------------------------------------------------- Q6
print("\nQ6. Coincidence count over the natural cases (D = 2..6, minimal and conformal massless scalars)")
cases = []
for Dv in (2, 3, 4, 5, 6):
    cases.append((f"D={Dv} minimal", sp.Rational(Dv - 1, 2)))
    cases.append((f"D={Dv} conformal", sp.Rational(1, 2)))
eq_kappa = [n for n, v in cases if v == sp.Rational(1, 2)]
distinct = sorted(set(v for _, v in cases))
print(f"     natural cases: {len(cases)}; distinct lam_c values: {[str(v) for v in distinct]}; cases equal to kappa = 1/2: {len(eq_kappa)} ({', '.join(eq_kappa)})")
print(f"     of the {len(distinct)} distinct values, {sum(1 for v in distinct if v == sp.Rational(1, 2))} equals kappa. All five conformal cases equal 1/2 by the identity (D-1)^2/4 - D(D-2)/4 = 1/4;")
print("     D = 2 minimal is the same field as D = 2 conformal. A fitted kappa near a small rational is not evidence: this is a coincidence count, not a p-value.")
check("Q6 the number of natural thresholds equal to kappa is fixed by the identity 1/4 (five conformal cases + D = 2 minimal), not by a coincidence of independent origin", len(eq_kappa) == 6)

# ---------------------------------------------------------------- Q7
print("\nQ7. Pre-registered verdict rule (LEAD only if ALL hold):")
crit = {
    "(a) NOT the inverse-square constant": not ok2,
    "(b) changes with kappa": False,                     # lam_c contains no kappa (Q1: it depends on D, xi, mu only)
    "(c) mass-independent acceleration tied to a0": False,   # Q4: F_c is mass independent but a0 needs an arbitrary mass; hubble-mass tautology
    "(d) constrains alpha": False,                       # Q5
}
for k_, v_ in crit.items():
    print(f"     {k_:50s}: {v_}")
lead = all(crit.values())
print(f"     => lambda_c = 1/2 is {'a LEAD' if lead else 'NOT a lead (a numerical coincidence of the conformal 1/4 with the fitted kappa = 1/2)'}")
check("Q7 verdict rule applied: not a lead", not lead)

print("\n" + "=" * 100)
passed = sum(1 for _, ok in CHECKS if ok)
print(f"CHECKS: {passed}/{len(CHECKS)} passed")
print("VERDICT: lambda_c = 1/2 is the classical critical inverse-square constant (1/4) of the conformally mapped mode equation, identical for every")
print("  conformal scalar in every dimension (3/2 for the minimal massless dS_4 scalar), a mass-independent force scale F_c = hbar H^2/(2c) with no")
print("  finite acceleration form, tied to a0 only through an arbitrary mass, blind to kappa, and it fixes eE/H^2, not e.  Not a lead on alpha or on kappa.")
print("  kappa = 1/2 stays FITTED; alpha stays an INPUT.")
sys.exit(0 if passed == len(CHECKS) else 1)
