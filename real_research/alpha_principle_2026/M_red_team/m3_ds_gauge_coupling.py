#!/usr/bin/env python3
"""M3 -- what dimensionless coupling does the de Sitter (MacDowell-Mansouri) gauge structure carry?
Action S = c * Int eps_{abcd} F^{ab} ^ F^{cd},  F^{ab} = R^{ab} - a e^a ^ e^b.  Expand: c[ GB - 2a X + a^2 V ],
X = Int eps R e e = 2 R sqrt(g) d^4x (s=+1 sign convention, checked below), V = Int eps e e e e = 24 sqrt(g) d^4x.
Requirement: reproduce (1/16 pi G)(R - 2 Lambda) sqrt(g).  Unknowns (c, a): two equations -> the script SOLVES for a (expected Lambda/3) and c.
Run:    python3 m3_ds_gauge_coupling.py
MUTATE: python3 m3_ds_gauge_coupling.py MUTATE   (uses a = Lambda/2 by hand; the cosmological-term match must fail -> exit 1)
"""
import sys
import sympy as sp
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
fails = []
def chk(n, ok, m=""):
    print(("[PASS] " if ok else "[FAIL] ") + n + " " + m)
    if not ok: fails.append(n)
G, Lam, a = sp.symbols('G Lambda a', positive=True); c = sp.Symbol('c', real=True)
Rs = sp.symbols('R')
# coefficient of R sqrt(g) and of sqrt(g) in c[-2a X + a^2 V]
lhs_R = c * (-2 * a) * 2            # -2 a * (2 R)  ->  coefficient of R
lhs_cc = c * a**2 * 24
rhs_R = 1 / (16 * sp.pi * G)
rhs_cc = -2 * Lam / (16 * sp.pi * G)
if MUT:
    sol = sp.solve([sp.Eq(lhs_R.subs(a, Lam/2), rhs_R)], [c], dict=True)
    csol = sol[0][c]; asol = Lam/2
    print("MUTATED a = Lambda/2, c fixed from the R-term only:", sp.simplify(csol))
else:
    sol = sp.solve([sp.Eq(lhs_R, rhs_R), sp.Eq(lhs_cc, rhs_cc)], [c, a], dict=True)
    print("solutions (c, a):", sol)
    good = [s for s in sol if sp.simplify(s[a] - Lam/3) == 0]
    chk("the two conditions force a = Lambda/3 (the MacDowell-Mansouri value)", len(good) == 1)
    csol = good[0][c]; asol = Lam/3
    chk("c = -3/(64 pi G Lambda)", sp.simplify(csol + 3/(64*sp.pi*G*Lam)) == 0, str(sp.simplify(csol)))
res_cc = sp.simplify((lhs_cc.subs({c: csol, a: asol}) - rhs_cc))
chk("cosmological term matches with the c and a fixed by the R term", res_cc == 0, "residual = %s" % res_cc)

# coupling: 1/g^2 = |c| * kN with kN a normalisation-convention factor (trace / gamma5 / 1/4); scan an absurdly generous range
import mpmath as mp
mp.mp.dps = 20
c_over = 3/(64*mp.pi)          # |c| = c_over / (G Lambda) = c_over / x  in Planck units (x = Lambda l_P^2)
Om, H0 = mp.mpf('0.6847'), mp.mpf('67.4')*1000/mp.mpf('3.0856775814913673e22')
cc, Gn, hb = mp.mpf('299792458'), mp.mpf('6.67430e-11'), mp.mpf('1.054571817e-34')
Lam_SI = 3*Om*H0**2/cc**2
x = Lam_SI * (Gn*hb/cc**3)
print("x = Lambda l_P^2 = %.4e" % x)
alpha = 1/mp.mpf('137.035999177')
for kN in (mp.mpf('0.01'), mp.mpf('0.25'), 1, 4, 100):
    invg2 = c_over/x*kN
    aMM = 1/(4*mp.pi*invg2)
    print("  kN = %-6s  alpha_MM = g^2/(4 pi) = %.3e   ratio to alpha = %.3e" % (kN, aMM, aMM/alpha))
chk("for every normalisation factor in [0.01, 100] alpha_MM < 1e-115 alpha (structure supplies x, not alpha)", all(1/(4*mp.pi*c_over/x*k) < alpha*mp.mpf('1e-115') for k in (mp.mpf('0.01'), 1, 100)))
chk("alpha_MM = (16/3) x / kN (closed form)", abs(1/(4*mp.pi*c_over/x) - mp.mpf(16)/3*x) < mp.mpf('1e-30')*x)
print("READING: the only dimensionless number carried by the SO(4,1) gauge structure is G*Lambda ~ 1e-122; an SO(10)/SO(3,11) extension with the same invariant")
print("inherits the same coefficient, so alpha_GUT ~ 1/25 needs a SEPARATE coefficient/vev = a new input (repo review PARTICLE_PHYSICS_FROM_DESITTER_GAUGE: SM content fitted).")
print("SUMMARY: fails =", fails)
sys.exit(1 if fails else 0)
