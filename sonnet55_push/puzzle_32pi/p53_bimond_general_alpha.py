"""p53: BIMOND vacuum coefficient for a GENERAL auxiliary-sector coupling alpha (beta = 1) -- the natural home of PREMISE A (the MOND sector's own coupling).
NR Lagrangian (Milgrom 2009 eq 1, varied in p25): flux(phi) = g - m (g - ghat) = g_N, flux(phihat) = alpha ghat + m (g - ghat) = 0, m = M'(z), z = (x*)^2, x* = g - ghat.
=> ghat = -m x*/alpha, g = x*(1 - m/alpha), y = g_N/a0 = x*(1 - m(1 + 1/alpha)), nu = g/g_N = (1 - m/alpha)/(1 - m(1 + 1/alpha)), m = (nu - 1)/(nu + (nu - 1)/alpha).
Vacuum (Milgrom eqs 84-85 at lambda = 1): beta G + q a0^2 M(0) g = 0, alpha G + qhat a0^2 M(0) g = 0, q = (1 + f')/2, qhat = (1 - f')/2 -> consistency q/beta = qhat/alpha
=> f'(1) = (1 - alpha)/(1 + alpha), q = 1/(1 + alpha); Lambda c^4/a0^2 = -q M(0) = J/(1 + alpha), J = int m dz.
Checks: (M) the map reduces to p25 (alpha = 1) and to M' = nu - 1 (alpha = -1); (I) J - I_nu is a total derivative for every alpha (class independence generalises);
(F) hence Lambda c^4/a0^2 = I_nu / (1 + alpha); 32 pi needs I_nu = 32 pi (1 + alpha).
Run: python3 p53_bimond_general_alpha.py  |  MUTATE=1: q = 1/(2 + alpha) (check F must fail)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
al, nu, m, xs, y, nup, fp = sp.symbols("alpha nu m xstar y nuprime fp", real=True)
msol = sp.solve(sp.Eq((1 - m / al) / (1 - m * (1 + 1 / al)), nu), m)[0]
check("M m(nu) = (nu-1)/(nu + (nu-1)/alpha); alpha = 1 gives (nu-1)/(2nu-1) (p25), alpha = -1 gives nu - 1 (Milgrom's main class)",
      sp.simplify(msol - (nu - 1) / (nu + (nu - 1) / al)) == 0 and sp.simplify(msol.subs(al, 1) - (nu - 1) / (2 * nu - 1)) == 0 and sp.simplify(msol.subs(al, -1) - (nu - 1)) == 0)
# J - I integrand: m dz/dy - (nu-1) d(y^2)/dy with z = (y/(1 - m(1+1/alpha)))^2, nu = nu(y), nu' = d nu/dy
den = sp.simplify(1 - msol * (1 + 1 / al))
z = (y / den)**2
Y = sp.Function("nuf")(y)
zz = z.subs(nu, Y); mm = msol.subs(nu, Y)
diffint = sp.simplify(mm * sp.diff(zz, y) - (Y - 1) * 2 * y)
cand = sp.diff(sp.Symbol("cB") * y**2 * (Y - 1)**2, y)
cB = sp.symbols("cB")
sol = sp.solve(sp.Eq(sp.simplify(diffint.subs(sp.Derivative(Y, y), nup) - sp.diff(cB * y**2 * (Y - 1)**2, y).subs(sp.Derivative(Y, y), nup)), 0), cB)
print(f"   J - I integrand = d/dy[ cB y^2 (nu-1)^2 ] with cB = {sol}")
ok_tot = bool(sol) and sp.simplify(diffint - sp.diff(sol[0] * y**2 * (Y - 1)**2, y)) == 0
check("I for every alpha, J - I_nu is the total derivative d[cB(alpha) y^2 (nu-1)^2]: the boundary term vanishes, so J = I_nu (class independence for all alpha)", ok_tot)
q = 1 / (2 + al) if MUTATE else sp.simplify(((1 + fp) / 2).subs(fp, sp.solve(sp.Eq((1 + fp) / 2 / 1, ((1 - fp) / 2) / al), fp)[0]))
check("F vacuum consistency gives q = 1/(1 + alpha), hence Lambda c^4/a0^2 = I_nu/(1 + alpha) (alpha = 1: I/2, p24/p25)", sp.simplify(q - 1 / (1 + al)) == 0)
Isym = sp.symbols("I", positive=True)
print(f"   32 pi needs I_nu = 32 pi (1 + alpha): alpha = 1 -> {sp.N(64*sp.pi,5)} (p22/p26), alpha = 8 pi - 1 -> {sp.N(256*sp.pi**2,5)}, RAR's I = 25.98 -> alpha = {sp.N(25.976/(32*sp.pi) - 1,4)}")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
