#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M1, SEAM S1: algebraic consequences of the framework law
    g_obs = nu(y) g_bar,  nu(y) = sqrt(1+1/y),  y = g_bar/a0
    equivalently  g_obs^2 = g_bar^2 + a0 g_bar   (the a0-line, squared form)

Framework: Carl Zimmerman's dS-Unruh MODIFIED-INERTIA law, judged on ITS OWN terms.
Footings: BOTH always -- a0_can = 9.36e-11 (cH_Lambda/Z), a0_alt = 1.13e-10 (rho_total/cH0).

Derived here (all sympy-verified, exit 0, no hard-coded checks):
  E-S1.1  Exact inversion:      g_bar = ( sqrt(a0^2 + 4 g_obs^2) - a0 ) / 2          [EXACT]
  E-S1.2  Baryon-mass predictor: M_bar(<r) = (r^2/2G) ( sqrt(a0^2+4 v^4/r^2) - a0 )   [EXACT law,
          spherical-equivalent M interpretation approximate for disks -- flagged]
  E-S1.3  Per-radius velocity identity: v_obs^4(r) - v_bar^4(r) = a0 G M_bar(r)       [EXACT]
          => exact finite-radius BTFR:  v^4 = G M a0 + (G M / r)^2  (point mass)
  E-S1.4  RAR log-log slope:    sigma(y) = (2y+1)/(2(y+1))                            [EXACT]
  E-S1.5  RAR log-log curvature: C(y) = y/(2(y+1)^2); maximal EXACTLY at y=1
          (g_bar = a0), where sigma = 3/4 and C = 1/8 -- pure-number landmark         [EXACT]
  E-S1.6  Reciprocity symmetry:  C(1/y) = C(y)  -- the RAR curvature is an exactly
          even function of ln(g_bar/a0)                                               [EXACT]
  E-S1.7  Slope sum rule:        sigma(y) + sigma(1/y) = 3/2  for ALL y               [EXACT]
  E-S1.8  Anchor point:          g_obs(g_bar=a0) = sqrt(2) a0                          [EXACT]
Discriminator check (numeric, honest): the landmark values for McGaugh's nu and the
MOND 'simple' nu are computed, NOT asserted -- they differ from (1, 3/4, 1/8) and
break the sum rule/symmetry, so E-S1.5/6/7 are nu-diagnostic.
"""
import sympy as sp
import numpy as np

ok = 0
def check(name, cond):
    global ok
    assert cond, "FAILED: " + name
    ok += 1
    print("[OK %2d] %s" % (ok, name))

a0, gbar, gobs, r, G, v, M, y, x = sp.symbols(
    "a0 g_bar g_obs r G v M y x", positive=True)

law = sp.Eq(gobs, sp.sqrt(gbar**2 + a0*gbar))
nu = sp.sqrt(1 + 1/y)

# ---------------------------------------------------------------- E-S1.1 inversion
sols = sp.solve(sp.Eq(gobs**2, gbar**2 + a0*gbar), gbar)
inv = [s for s in sols if s.subs({a0: 1, gobs: 1}) > 0][0]
inv_claimed = (sp.sqrt(a0**2 + 4*gobs**2) - a0)/2
check("E-S1.1 inversion g_bar = (sqrt(a0^2+4g_obs^2)-a0)/2 (unique positive root)",
      sp.simplify(inv - inv_claimed) == 0)
# round trip
check("E-S1.1 round trip: law(inv(g_obs)) == g_obs identically",
      sp.simplify(sp.sqrt(inv_claimed**2 + a0*inv_claimed) - gobs) == 0)

# ---------------------------------------------------------------- E-S1.2 M_bar predictor
# circular orbit: g_obs = v^2/r ; spherical-equivalent g_bar = G M / r^2
Mbar = (r**2/(2*G))*(sp.sqrt(a0**2 + 4*v**4/r**2) - a0)
gbar_from_M = G*Mbar/r**2
check("E-S1.2 M_bar(<r) predictor satisfies the law with g_obs=v^2/r exactly",
      sp.simplify(sp.sqrt(gbar_from_M**2 + a0*gbar_from_M) - v**2/r) == 0)

# ---------------------------------------------------------------- E-S1.3 velocity identity
# v_obs^2 = g_obs r , v_bar^2 = g_bar r = G M(r)/r  (definitional in SPARC)
vobs2 = gobs*r
vbar2 = gbar*r
ident = sp.simplify((vobs2**2 - vbar2**2).subs(gobs, sp.sqrt(gbar**2 + a0*gbar))
                    - a0*r*vbar2.rewrite(sp.Pow))
check("E-S1.3 v_obs^4 - v_bar^4 = a0 r v_bar^2 = a0 G M_bar(r) at EVERY radius",
      sp.simplify((gobs**2 - gbar**2)*r**2 - a0*gbar*r**2) ==
      sp.simplify((gobs**2 - gbar**2 - a0*gbar)*r**2) and
      sp.simplify(((sp.sqrt(gbar**2+a0*gbar))**2 - gbar**2)*r**2 - a0*gbar*r**2) == 0)
# exact finite-radius BTFR, point mass
v4 = sp.expand((sp.sqrt((G*M/r**2)**2 + a0*G*M/r**2)*r)**2)
check("E-S1.3b exact BTFR: v^4 = G M a0 + (G M/r)^2 (finite-y correction is exactly (GM/r)^2)",
      sp.simplify(v4 - (G*M*a0 + (G*M/r)**2)) == 0)

# ---------------------------------------------------------------- E-S1.4 log-log slope
lg = sp.log(sp.sqrt(y**2 + y))          # ln(g_obs/a0) as function of ln y
ell = sp.symbols("ell")                  # ell = ln y
sigma = sp.simplify(sp.diff(lg, y)*y)    # d ln g_obs / d ln g_bar
sigma_claimed = (2*y + 1)/(2*(y + 1))
check("E-S1.4 slope sigma(y) = (2y+1)/(2(y+1))", sp.simplify(sigma - sigma_claimed) == 0)
check("E-S1.4b limits: sigma->1 (Newton), sigma->1/2 (deep)",
      sp.limit(sigma, y, sp.oo) == 1 and sp.limit(sigma, y, 0) == sp.Rational(1, 2))

# ---------------------------------------------------------------- E-S1.5 curvature landmark
C = sp.simplify(sp.diff(sigma, y)*y)     # d sigma / d ln g_bar
C_claimed = y/(2*(y + 1)**2)
check("E-S1.5 curvature C(y) = y/(2(y+1)^2)", sp.simplify(C - C_claimed) == 0)
crit = sp.solve(sp.diff(C, y), y)
crit = [c for c in crit if c.is_positive]
check("E-S1.5b curvature maximal EXACTLY at y = 1 (g_bar = a0)",
      len(crit) == 1 and crit[0] == 1)
check("E-S1.5c landmark values: sigma(1) = 3/4, C(1) = 1/8 (pure numbers)",
      sigma.subs(y, 1) == sp.Rational(3, 4) and sp.simplify(C.subs(y, 1)) == sp.Rational(1, 8))

# ---------------------------------------------------------------- E-S1.6 reciprocity symmetry
check("E-S1.6 C(1/y) == C(y): curvature exactly EVEN in ln(g_bar/a0)",
      sp.simplify(C.subs(y, 1/y) - C) == 0)

# ---------------------------------------------------------------- E-S1.7 slope sum rule
check("E-S1.7 sigma(y) + sigma(1/y) = 3/2 for all y",
      sp.simplify(sigma + sigma.subs(y, 1/y) - sp.Rational(3, 2)) == 0)

# ---------------------------------------------------------------- E-S1.8 anchor point
check("E-S1.8 anchor: g_obs(a0) = sqrt(2) a0",
      sp.simplify(sp.sqrt(a0**2 + a0*a0) - sp.sqrt(2)*a0) == 0)

# ================================================================ discriminator (numeric)
print("\n--- nu-DISCRIMINATOR (numeric, computed not asserted) ---")
def landmarks(nu_fn, name):
    """local log-log slope+curvature of g_obs=y*nu(y)*a0 vs g_bar=y*a0, numeric."""
    ly = np.linspace(-6, 6, 24001)
    yv = np.exp(ly)
    lgobs = np.log(yv*nu_fn(yv))
    sig = np.gradient(lgobs, ly)
    Cv = np.gradient(sig, ly)
    ipk = np.argmax(Cv[100:-100]) + 100
    ypk, spk, cpk = yv[ipk], sig[ipk], Cv[ipk]
    # sum rule at x=3 and x=10
    def s_at(yq): return np.interp(np.log(yq), ly, sig)
    sr3 = s_at(3.0) + s_at(1/3.0)
    sr10 = s_at(10.0) + s_at(0.1)
    # symmetry deviation: C(3 ypk) vs C(ypk/3)
    def c_at(yq): return np.interp(np.log(yq), ly, Cv)
    asym = c_at(3*ypk) - c_at(ypk/3)
    print("  %-28s y_peak=%.4f  sigma_pk=%.4f  C_pk=%.4f  sumrule(3)=%.4f "
          "sumrule(10)=%.4f  C-asym=%.2e" % (name, ypk, spk, cpk, sr3, sr10, asym))
    return ypk, spk, cpk, sr3, sr10, asym

fw = landmarks(lambda t: np.sqrt(1 + 1/t), "framework sqrt(1+1/y)")
mcg = landmarks(lambda t: 1/(1 - np.exp(-np.sqrt(t))), "McGaugh 1/(1-e^-sqrt(y))")
smp = landmarks(lambda t: 0.5 + np.sqrt(0.25 + 1/t), "MOND 'simple' nu")

check("framework numeric landmarks reproduce the exact (1, 3/4, 1/8) to <1e-3",
      abs(fw[0]-1) < 2e-3 and abs(fw[1]-0.75) < 1e-3 and abs(fw[2]-0.125) < 1e-3)
check("framework sum rule holds numerically at x=3 and x=10 (<1e-6)",
      abs(fw[3]-1.5) < 1e-6 and abs(fw[4]-1.5) < 1e-6)
check("McGaugh nu BREAKS at least one landmark (peak loc, sum rule, or symmetry)",
      abs(mcg[0]-1) > 0.05 or abs(mcg[3]-1.5) > 1e-3 or abs(mcg[5]) > 1e-3)
check("simple nu BREAKS at least one landmark",
      abs(smp[0]-1) > 0.05 or abs(smp[3]-1.5) > 1e-3 or abs(smp[5]) > 1e-3)

# both footings: the landmark LOCATION in physical units
for tag, a0v in [("canonical cH_Lambda/Z", 9.36e-11), ("alternate rho_tot/cH0", 1.13e-10)]:
    print("  footing %-24s -> curvature peak at g_bar = %.3e m/s^2, "
          "g_obs = sqrt(2) a0 = %.3e m/s^2" % (tag, a0v, np.sqrt(2)*a0v))

print("\nALL %d CHECKS PASSED -- exit 0" % ok)
