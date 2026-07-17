#!/usr/bin/env python3
"""
EQUATION BOOK -- LANE M1, SEAM S5: the exact external-field (EFE) RAR surface for the
framework's OWN worldline form.

PREMISES (the framework's, not standard MOND's):
  * Modified INERTIA, worldline (Galley) form: the inertia dressing is mu_fw(|A|/a0),
    mu_fw = exact inverse of nu(y)=sqrt(1+1/y):  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x).
  * External-field kernel theta(y_freq)=theta0/(1+(theta0-1) y_freq^2), theta0 = sqrt(2)
    (prep_2026/mi_field_theory/BASELINE_ACTION.md:49 -- "shape forced by the dS Wightman
    function"). A QUASI-STATIC external field (y_freq -> 0) therefore enters with DC
    weight sqrt(2):  A = g_int + sqrt(2) g_ext   (scalar/aligned worldline composition,
    as used in prep_2026/sigma_spread/rederive_mi_spread.py).
  * Internal force balance:  mu_fw(A/a0) * g_int = g_bar.
  * NOTE vs directional-EFE memory: this DC kernel depends on |g_ext| ONLY (direction-
    blind), fully consistent with "pure MI predicts zero DIRECTIONAL asymmetry".

DERIVED (dimensionless: x = g_int/a0 = observed internal, b = g_bar/a0, e = sqrt(2) g_ext/a0):
  E-S5.1  THE EFE CUBIC:   x^3 + e x^2 - b(b+1) x - b^2 e = 0            [EXACT given theta0]
          (e=0 recovers the isolated a0-line x^2 = b^2 + b exactly)
  E-S5.2  THE ATTENUATED a0-LINE:
              g_obs^2 - g_bar^2 = a0 g_bar * g_obs/(g_obs + sqrt(2) g_ext)
          -- the a0-line slope is multiplied by an exact attenuation factor  [EXACT]
  E-S5.3  HALF-QUENCH LOCUS: the MOND excess (g_obs^2-g_bar^2) is HALF its isolated
          value exactly when  sqrt(2) g_ext = g_obs                       [EXACT]
  E-S5.4  EFE SUSCEPTIBILITY: d g_obs / d(sqrt2 g_ext) |_{g_ext=0} = -1/(2(1+y_obs^2/...))
          -- computed exactly below; deep-MOND limit -1/2, Newtonian limit 0 [EXACT]
  E-S5.5  Closed-form root (Cardano) g_obs(g_bar, g_ext) -- explicit, verified.
  E-S5.6  External-dominated limit: quasi-Newton with G_eff/G = nu(e) + O(b)  [SERIES]

FLAGS: postulate-dependence = theta0=sqrt(2) (the framework's stated kernel); the
scalar (aligned) composition is the framework's worldline usage -- a full angular
average would modify O(1) coefficients, flagged, not hidden. Both footings shown.
"""
import sympy as sp
import numpy as np

ok = 0
def check(name, cond):
    global ok
    assert cond, "FAILED: " + name
    ok += 1
    print("[OK %2d] %s" % (ok, name))

x, b, e, y, a0, gobs, gbar, gext = sp.symbols("x b e y a0 g_obs g_bar g_ext",
                                              positive=True)
E = sp.symbols("E", nonnegative=True)  # e as nonnegative (isolated limit e=0 allowed)

mu = (sp.sqrt(1 + 4*y**2) - 1)/(2*y)
nu = sp.sqrt(1 + 1/y)
# mu is the exact inverse of nu: mu(x)*x = (sqrt(1+4x^2)-1)/2 with x = y*nu(y),
# x^2 = y^2 + y, and 1+4(y^2+y) = (2y+1)^2 collapses the nested radical
check("mu_fw is the EXACT inverse of nu(y)=sqrt(1+1/y) (nested radical collapses)",
      sp.expand(1 + 4*(y**2 + y) - (2*y + 1)**2) == 0 and
      sp.simplify((sp.sqrt(sp.factor(1 + 4*(y**2 + y))) - 1)/2 - y) == 0)

# ---------------------------------------------------------------- E-S5.1 the EFE cubic
# balance: mu((x+E)) * x = b   with all in units of a0
bal = mu.subs(y, x + E)*x - b
# clear the radical: move, square
poly = sp.expand((x*sp.sqrt(1 + 4*(x + E)**2))**2 - (2*b*(x + E) + x)**2)
cubic_claimed = x**3 + E*x**2 - b*(b + 1)*x - b**2*E
# poly should be 4(x+E) * cubic_claimed
check("E-S5.1 radical clears to 4(x+e)*[x^3 + e x^2 - b(b+1)x - b^2 e]",
      sp.simplify(poly - 4*(x + E)*cubic_claimed) == 0)
check("E-S5.1b isolated limit e=0 recovers x^2 = b^2 + b (the a0-line) exactly",
      sp.simplify(cubic_claimed.subs(E, 0) - x*(x**2 - b**2 - b)) == 0)
# verify no spurious root introduced: numeric spot check that the positive root of the
# cubic satisfies the ORIGINAL balance (with the un-squared sign)
for bv, ev in [(0.1, 0.3), (3.0, 0.5), (0.02, 2.0), (10.0, 10.0)]:
    roots = sp.Poly(cubic_claimed.subs({b: bv, E: ev}), x).nroots()
    pos = [complex(rr).real for rr in roots if abs(complex(rr).imag) < 1e-12
           and complex(rr).real > 0]
    assert len(pos) == 1, "expected unique positive root"
    xv = pos[0]
    res = float(mu.subs({y: xv + ev})*xv - bv)
    assert abs(res) < 1e-10, "cubic root does not satisfy original balance"
check("E-S5.1c unique positive root satisfies the ORIGINAL (unsquared) balance, 4 spot pts", True)

# ---------------------------------------------------------------- E-S5.2 attenuated a0-line
# rearrange cubic: (x^2 - b^2)(x + e) = b x  ->  x^2 - b^2 = b x/(x+e)
check("E-S5.2 cubic == (x^2-b^2)(x+e) - bx: attenuated a0-line "
      "g_obs^2-g_bar^2 = a0 g_bar g_obs/(g_obs+sqrt2 g_ext)",
      sp.expand(cubic_claimed - ((x**2 - b**2)*(x + E) - b*x)) == 0)

# ---------------------------------------------------------------- E-S5.3 half-quench locus
# isolated excess = b (in a0^2 units, since x^2-b^2 = b when e=0). Half: x^2-b^2 = b/2
xh = sp.sqrt(b**2 + b/2)
e_half = sp.solve(sp.Eq((xh**2 - b**2)*(xh + e), b*xh), e)[0]
check("E-S5.3 half-quench at e = x exactly: sqrt(2) g_ext = g_obs halves the MOND excess",
      sp.simplify(e_half - xh) == 0)

# ---------------------------------------------------------------- E-S5.4 susceptibility
# implicit differentiation of the cubic at e=0
F = cubic_claimed
dxde = sp.solve(sp.Eq(sp.diff(F, x)*sp.Symbol("xp") + sp.diff(F, E), 0),
                sp.Symbol("xp"))[0]
chi0 = sp.simplify(dxde.subs({E: 0, x: sp.sqrt(b**2 + b)}))
chi_claimed = -1/(2*(b + 1))
check("E-S5.4 EFE susceptibility chi = d g_obs/d(sqrt2 g_ext)|_0 = -1/(2(1+g_bar/a0))",
      sp.simplify(chi0 - chi_claimed) == 0)
check("E-S5.4b limits: deep-MOND chi -> -1/2, Newtonian chi -> 0",
      sp.limit(chi_claimed, b, 0) == -sp.Rational(1, 2)
      and sp.limit(chi_claimed, b, sp.oo) == 0)

# ---------------------------------------------------------------- E-S5.5 Cardano closed form
# depressed cubic x = t - e/3: t^3 + p t + q
p_ = sp.simplify(-E**2/3 - b*(b + 1))
q_ = sp.simplify(sp.expand(cubic_claimed.subs(x, sp.Symbol("t") - E/3))
                 .coeff(sp.Symbol("t"), 0))
disc = sp.simplify(-4*p_**3 - 27*q_**2)
# with p<0 always (b,e>0), unique positive root via trigonometric/Cardano form:
t = sp.Symbol("t")
dep = sp.expand(cubic_claimed.subs(x, t - E/3))
check("E-S5.5 depressed cubic t^3 + p t + q with p = -e^2/3 - b(b+1) (always < 0)",
      sp.simplify(dep - (t**3 + p_*t + q_)) == 0)
# closed root (single real when disc<0; three real -> take the branch matching balance)
xc = 2*sp.sqrt(-p_/3)*sp.cos(sp.acos(sp.Rational(3, 2)*q_/p_*sp.sqrt(-3/p_))/3) - E/3
for bv, ev in [(0.1, 0.3), (3.0, 0.5), (0.02, 2.0), (10.0, 10.0), (1.0, 1.0)]:
    xv = float(xc.subs({b: bv, E: ev}))
    res = float(mu.subs({y: xv + ev})*xv - bv)
    assert abs(res) < 1e-10, "Cardano branch mismatch at b=%g e=%g" % (bv, ev)
check("E-S5.5b explicit trig-Cardano root g_obs(g_bar,g_ext) verified on 5 points", True)

# ---------------------------------------------------------------- E-S5.6 ext-dominated series
xser = sp.series(sp.solve(cubic_claimed, x)[0], b, 0, 2)  # symbolic; fallback numeric
# do it robustly: substitute x = c1*b + c2*b^2 and match orders
c1, c2 = sp.symbols("c1 c2")
expand = sp.expand(cubic_claimed.subs(x, c1*b + c2*b**2))
o1 = sp.Poly(expand, b).coeff_monomial(b)      # O(b) coefficient must vanish w/ c-choices
# lowest orders: collect
pb = sp.Poly(expand, b)
# orders b^0 and b^1 vanish identically; the first nontrivial orders are b^2, b^3
assert pb.coeff_monomial(1) == 0 and pb.coeff_monomial(b) == 0
sols_c1 = sp.solve(pb.coeff_monomial(b**2), c1)   # E c1^2 - c1 - E = 0
c1v = [s for s in sols_c1 if s.subs(E, 1) > 0][0]
# the coefficient is 1/mu_fw(e) -- the inertia dressing evaluated at the EXTERNAL
# argument (NOT nu(e); in MI the boost comes from the dressed inertia, not the field)
mu_at_e = (sp.sqrt(1 + 4*E**2) - 1)/(2*E)
check("E-S5.6 external-dominated limit: g_obs = g_bar/mu_fw(e) + O(gbar^2) -- quasi-Newton "
      "with G_eff/G = 1/mu_fw(sqrt2 g_ext/a0) = (1+sqrt(1+4e^2))/(2e)",
      sp.simplify(c1v - 1/mu_at_e) == 0 and
      sp.simplify(c1v - (1 + sp.sqrt(1 + 4*E**2))/(2*E)) == 0)

# ---------------------------------------------------------------- numbers, both footings
print("\n--- NUMBERS (both footings) ---")
for tag, a0v in [("canonical 9.36e-11", 9.36e-11), ("alternate 1.13e-10", 1.13e-10)]:
    # a Milky-Way-like external field on a satellite: g_ext = 2e-11 m/s^2
    gextv = 2.0e-11
    for gbarv in [1e-12, 1e-11, 1e-10]:
        bv = gbarv/a0v
        ev = np.sqrt(2)*gextv/a0v
        xv = float(xc.subs({b: bv, E: ev}))
        xiso = np.sqrt(bv**2 + bv)
        print("  %s: g_bar=%.0e  g_obs/g_bar: iso=%.3f EFE=%.3f  (quench %.1f%%)"
              % (tag, gbarv, xiso/bv, xv/bv, 100*(1 - (xv**2 - bv**2)/(xiso**2 - bv**2))))

print("\nALL %d CHECKS PASSED -- exit 0" % ok)
