#!/usr/bin/env python3
"""a05_flux_and_vacuum_audit.py -- adversarial audit of p08 (Gauss-law form) and p09 (vacuum self-consistency).

 F1  independent recomputation of the S^4 volume and the four-form flux; the coefficient of Lambda Vol_4 for framework / Milgrom / Verlinde:
     A_a0 = pi Z^2 L^2 and Lambda Vol_4 = 8 pi^2 L^2  =>  A_a0/(Lambda Vol_4) = Z^2/(8 pi):  4/3 (framework), pi/2 (Milgrom Z = 2 pi), 9/(2 pi) (Verlinde Z = 6).
     README section 10 says '27/(2 pi)' for Verlinde: wrong by a factor 3 (the sentence is not scripted in p08).
 F2  p08 check 4 tests only that Phi ~ L^3 (a scaling), not the label 'contains NO relation between a0 and Lambda'; the claim is an argument, not a computation.
 V1  p09's no-go is normalisation-dependent.  With V(phi) = (a0^2/G) W(phi) (energy density in units of a0^2/G, no Poisson 1/(8 pi)),
     the puzzle G rho_v = 4 a0^2 is W_v = 4, an ALGEBRAIC number: a local algebraic potential reaches it (explicit potential below).  The 'U_v = 32 pi' form arises only
     because p09 normalises the potential by the Poisson factor a0^2/(8 pi G) (U = 8 pi W).  Which normalisation is 'natural' is a convention; the pi is in the convention.
 V2  a LOCAL effective potential does not have algebraic coefficients in general: the one-loop Coleman-Weinberg term carries 1/(64 pi^2); the stationary value then lies in
     a field containing pi (and logs).  Demonstrate with a tree + one-loop potential: U_v is not algebraic (integer-relation search) although the action is local.
 V3  the algebraic-value check itself (p09 3a) is the statement 'a real root of a polynomial with algebraic coefficients is algebraic' -- true and trivial (algebraic numbers form a field);
     p09's own remark 'close to trivial' is right; the substantive step is the (convention-dependent) reduction to U_v = 32 pi.
Exit 0 = the audit's checks held.
"""
import math, sys
import sympy as sp
import mpmath as mp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- F1
L = sp.symbols('L', positive=True)
Vol4 = sp.Rational(8, 3) * sp.pi**2 * L**4
# independent: Vol(S^n) = 2 pi^((n+1)/2)/Gamma((n+1)/2) ; n = 4
chk("F1a Vol(S^4_L) = 2 pi^(5/2)/Gamma(5/2) L^4 = (8 pi^2/3) L^4 (Gamma-function route, independent of p08's sin-integrals)",
    sp.simplify(2 * sp.pi**sp.Rational(5, 2) / sp.gamma(sp.Rational(5, 2)) * L**4 - Vol4) == 0)
Lam = 3 / L**2
def coef(Z):
    return sp.simplify(sp.pi * Z**2 * L**2 / (Lam * Vol4))
Zfw = sp.sqrt(32 * sp.pi / 3)
c_fw, c_mi, c_ve = coef(Zfw), coef(2 * sp.pi), coef(6)
print("   A_a0/(Lambda Vol_4): framework %s ; Milgrom %s ; Verlinde %s" % (c_fw, c_mi, c_ve))
chk("F1b coefficients: framework 4/3, Milgrom pi/2, Verlinde 9/(2 pi) -- the README's '27/(2 pi)' for Verlinde is wrong (factor 3)",
    sp.simplify(c_fw - sp.Rational(4, 3)) == 0 and sp.simplify(c_mi - sp.pi / 2) == 0 and sp.simplify(c_ve - 9 / (2 * sp.pi)) == 0 and sp.simplify(c_ve - 27 / (2 * sp.pi)) != 0)
E = sp.sqrt(Lam / (4 * sp.pi))
Phi = sp.simplify(E * Vol4)
chk("F1c flux Phi = E Vol = 4 sqrt3 pi^(3/2) L^3/3 with E = sqrt(2 rho), rho = Lambda/(8 pi) (recomputed)", sp.simplify(Phi - 4 * sp.sqrt(3) * sp.pi**sp.Rational(3, 2) * L**3 / 3) == 0)
# F2: what does p08 check 4 actually establish?
chk("F2 p08 check 4 is 'd ln Phi/dL = 3/L': a scaling law. It cannot establish 'no relation between a0 and Lambda' (an argument, not a computation)", sp.simplify(sp.diff(Phi, L) / Phi - 3 / L) == 0)

# ---------------------------------------------------------------- V1 convention dependence of the p09 no-go
phi, a0, G = sp.symbols('phi a0 G', positive=True)
# potential in energy-density units of a0^2/G:  V = (a0^2/G) W(phi),  W = (phi^2 - 1)^2 + 4  (algebraic, minimum W_v = 4)
W = (phi**2 - 1)**2 + 4
crit = [c for c in sp.solve(sp.diff(W, phi), phi) if c.is_real]
vals = {sp.simplify(W.subs(phi, c)) for c in crit}
chk("V1a W(phi) = (phi^2-1)^2 + 4 is a local ALGEBRAIC potential whose vacuum value in units of a0^2/G is exactly 4 (= the puzzle G rho = 4 a0^2); stationary values found: %s" % sorted(vals, key=str), 4 in vals)
rho_v = a0**2 / G * 4
chk("V1b so G rho_v = 4 a0^2 <=> W_v = 4: no transcendental number is required in the energy-density normalisation", sp.simplify(G * rho_v - 4 * a0**2) == 0)
U_v = 8 * sp.pi * 4        # U := 8 pi W (Poisson normalisation a0^2/(8 pi G))
chk("V1c the p09 requirement U_v = 32 pi is W_v = 4 rewritten with U = 8 pi W: the pi is the Poisson-normalisation convention (Lambda = 8 pi G rho), the same 8 pi as in section 1 -- not a property of local potentials", sp.simplify(U_v - 32 * sp.pi) == 0)

# ---------------------------------------------------------------- V2 a local one-loop effective potential is not algebraic
mp.mp.dps = 60
# tree + Coleman-Weinberg:  V(x) = x^4/4 - x^2/2 + (x^4/(64 pi^2)) (ln(x^2) - 3/2) + c0  (x = phi/f, all coefficients rational except the loop factor)
xs = sp.symbols('x', positive=True)
Vcw = xs**4 / 4 - xs**2 / 2 + xs**4 / (64 * sp.pi**2) * (sp.log(xs**2) - sp.Rational(3, 2))
Vf = sp.lambdify(xs, Vcw, 'mpmath')
dV = sp.lambdify(xs, sp.diff(Vcw, xs), 'mpmath')
x0 = mp.findroot(dV, 1.0)
Vv = Vf(x0)
rel = None
for dgr in range(1, 5):
    rel = mp.findpoly(Vv, dgr, maxcoeff=10**4, maxsteps=100000)
    if rel: break
print("   local one-loop potential: stationary x = %s, V_v = %s; small-integer polynomial relation found: %s" % (mp.nstr(x0, 15), mp.nstr(Vv, 20), rel))
chk("V2 a LOCAL (tree + one-loop) potential has a stationary value with no low-degree algebraic relation: 'local action => algebraic value' holds only for tree-level algebraic couplings; README section 11 'a local action cannot answer it' overreaches",
    rel is None)
ctrl = mp.findpoly(mp.mpf(3) * mp.sqrt(2) + 1, 2, maxcoeff=10**3)
chk("V2c control: the same integer-relation search does find 3 sqrt2 + 1 (degree 2)", ctrl is not None)

print("   NOTE V3: p09 3a (algebraic-coefficient potential => algebraic stationary value) is closure of the algebraic numbers under root-finding: true and trivial (p09 says so); nothing is scripted here for it.")
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
