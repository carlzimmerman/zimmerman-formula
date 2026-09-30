"""s03: field-energy budget of a POINT MASS in deep MOND (declared conventions D0, D1, D2 of PREDECLARED_PRINCIPLES.md).  c = 1, G explicit.

 A  AQUAL: L = -(a0^2/8 pi G) F(y) - rho phi, y = g^2/a0^2, mu = F'.  Field equation div(mu grad phi) = 4 pi G rho; point mass, deep MOND: g = sqrt(G M a0)/r.
    D1 = F-term density, D2 = on-shell localisation (F - 2 y mu), D0 = Poisson-normalised Newtonian form applied to g.
 B  Shell integrals in closed form (sympy) and their divergences: D0 linear in R, D1/D2 logarithmic at BOTH ends (no finite 'out to the horizon' budget without an inner cut).
 C  Ratios: E/M for each convention, the exact bound sup_M E_D1(R; r_in = r_M)/M = a0 R/(3e), and the scale-free identities that contain no rho.
 D  What is / is not scale-free: E_D0/M = a0 R/2 (independent of M); the mass M_a = 1/(G a0) makes E_D0(M_a; R) = R/(2G) for EVERY R and a0 (an identity, no rho).
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 30
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

G, a0, M, r, rin, R, rho = sp.symbols('G a0 M r r_in R rho', positive=True)
y = sp.symbols('y', positive=True)

# ------------------------------------------------------------------ A
F = sp.Rational(2, 3)*y**sp.Rational(3, 2)                      # deep-MOND F (mu = F' = sqrt(y) = g/a0)
mu = sp.diff(F, y)
chk("A1 F = (2/3) y^{3/2}  =>  mu = F' = sqrt(y) = g/a0 (deep-MOND interpolation)", sp.simplify(mu - sp.sqrt(y)) == 0)
g = sp.symbols('g', positive=True)
# field equation for a point mass: 4 pi r^2 mu(g/a0) g = 4 pi G M   (Gauss for div(mu grad phi) = 4 pi G rho)
gsol = sp.solve(sp.Eq((g/a0)*g, G*M/r**2), g)
chk("A2 point mass, deep MOND: mu g = G M/r^2 with mu = g/a0  =>  g = sqrt(G M a0)/r", [sp.simplify(s - sp.sqrt(G*M*a0)/r) for s in gsol] == [0])
gM = sp.sqrt(G*M*a0)/r
# static energy functional E = int [ (a0^2/8 pi G) F + rho phi ];  rho phi = (1/4 pi G) phi div(mu grad phi) = -(1/4 pi G) mu |grad phi|^2 + div(...)
w1 = (a0**2/(8*sp.pi*G))*F.subs(y, g**2/a0**2)
w2_signed = (a0**2/(8*sp.pi*G))*(F - 2*y*mu).subs(y, g**2/a0**2)
chk("A3 D1: (a0^2/8 pi G) F = g^3/(12 pi G a0)", sp.simplify(w1 - g**3/(12*sp.pi*G*a0)) == 0)
chk("A4 D2: on-shell (F - 2 y mu) density = -g^3/(6 pi G a0) (NEGATIVE; magnitude declared as D2)", sp.simplify(w2_signed + g**3/(6*sp.pi*G*a0)) == 0)
# Newton limit of the same construction (F = y): w1 -> +g^2/8 pi G, on-shell -> -g^2/8 pi G
Fn = y
w1n = (a0**2/(8*sp.pi*G))*Fn.subs(y, g**2/a0**2); w2n = (a0**2/(8*sp.pi*G))*(Fn - 2*y*sp.diff(Fn, y)).subs(y, g**2/a0**2)
chk("A5 Newton (F = y): gradient density +g^2/(8 pi G), on-shell density -g^2/(8 pi G) (matches s02)", sp.simplify(w1n - g**2/(8*sp.pi*G)) == 0 and sp.simplify(w2n + g**2/(8*sp.pi*G)) == 0)
w0 = lambda gg: gg**2/(8*sp.pi*G)
# pi-bookkeeping for ANY interpolating function: Gauss's law removes the pi from g(r); the shell measure 4 pi r^2 cancels the 1/(8 pi) of the Poisson normalisation
Fgen = sp.Function('F'); mugen = sp.Function('mu')
w_gen = (a0**2/(8*sp.pi*G))*Fgen(g**2/a0**2)
chk("A6 pi-bookkeeping: for an arbitrary F the shell energy integrand 4 pi r^2 w(g) is pi-free (4 pi cancels 1/(8 pi)), and Gauss's law mu(g/a0) g = G M/r^2 contains no pi: every point-mass field energy is a pi-free function of (M, a0, G, R)",
    not sp.simplify(4*sp.pi*r**2*w_gen).has(sp.pi) and not sp.Eq(mugen(g/a0)*g, G*M/r**2).has(sp.pi))
wD = {0: w0(gM), 1: w1.subs(g, gM), 2: -w2_signed.subs(g, gM)}

# ------------------------------------------------------------------ B
E = {k: sp.simplify(sp.integrate(4*sp.pi*r**2*wD[k], (r, rin, R))) for k in (0, 1, 2)}
chk("B1 D0: E = (M a0/2)(R - r_in)   (linear in R, finite as r_in -> 0)", sp.simplify(E[0] - M*a0*(R - rin)/2) == 0)
chk("B2 D1: E = (1/3) sqrt(G a0) M^{3/2} ln(R/r_in)", sp.simplify(E[1] - sp.sqrt(G*a0)*M**sp.Rational(3, 2)*sp.log(R/rin)/3) == 0)
chk("B3 D2 = 2 x D1 (the (2/3) sqrt(G a0) M^{3/2} coefficient equals Milgrom's exact deep-MOND virial coefficient)", sp.simplify(E[2] - 2*E[1]) == 0)
chk("B4 D1 and D2 diverge logarithmically at r_in -> 0 AND at R -> infinity; D0 diverges linearly at R -> infinity",
    sp.limit(E[1].subs(R, 1), rin, 0, '+') == sp.oo and sp.limit(E[1].subs(rin, 1), R, sp.oo) == sp.oo and sp.limit(E[0].subs(rin, 0), R, sp.oo) == sp.oo)
# numeric cross-check of the closed forms with mpmath (independent quadrature), and a mutation
vals = dict(G=1, a0=1, M=3.7, rin=1.9, R=40.0)
num1 = mp.quad(lambda rr: 4*mp.pi*rr**2*(mp.sqrt(vals['G']*vals['a0']*vals['M'])/rr)**3/(12*mp.pi*vals['G']*vals['a0']), [vals['rin'], vals['R']])
cf1 = float(E[1].subs({G: 1, a0: 1, M: 3.7, rin: 1.9, R: 40.0}))
chk("B5 mpmath quadrature of D1 matches the closed form (%.10f vs %.10f)" % (num1, cf1), abs(num1 - cf1) < 1e-9)
chk("B6 mutation: a wrong coefficient (1/(6 pi) instead of 1/(12 pi)) would not match", abs(2*num1 - cf1) > 1e-3)

# ------------------------------------------------------------------ C
Ma = 1/(G*a0); m = sp.symbols('m', positive=True)                # m = M/M_a
rM = sp.sqrt(G*M/a0)
x = sp.symbols('x', positive=True)                               # x = a0 R (c = 1)
E1_over_M = sp.simplify((E[1]/M).subs(rin, rM))
Eratio = sp.simplify(E1_over_M.subs(M, m*Ma).subs(R, x/a0))
chk("C1 D1 with r_in = r_M: E/M = (1/3) sqrt(m) ln(x/sqrt(m)),  m = M/M_a = G M a0,  x = a0 R", sp.simplify(Eratio - sp.sqrt(m)*sp.log(x/sp.sqrt(m))/3) == 0)
s_ = sp.symbols('s', positive=True)
f_of_s = (s_/3)*sp.log(x/s_)                                     # s = sqrt(m)
ssol = sp.solve(sp.diff(f_of_s, s_), s_)
chk("C2 the maximiser over M is s = x/e (r_M = R/e) with maximum x/(3e)", ssol == [x/sp.E] and sp.simplify(f_of_s.subs(s_, x/sp.E) - x/(3*sp.E)) == 0)
# numerical brute force (control that the analytic sup is right)
import numpy as np
xv = 0.17274707
mm_grid = np.linspace(1e-9, xv**2, 2000001)[1:]
best_val = float(np.max(np.sqrt(mm_grid)*np.log(xv/np.sqrt(mm_grid))/3))
chk("C3 brute-force sup over M (2e6 grid points) equals x/(3e) to 1e-6 relative (x = 0.1727 for illustration only)", abs(best_val/(xv/(3*np.e)) - 1) < 1e-6)
chk("C4 control: at fixed M the ratio depends on M (not scale-free): E_D1/M differs between m = 1e-4 and m = 1e-3 at x = 0.1727",
    abs(float(Eratio.subs({x: 0.1727, m: 1e-4})) - float(Eratio.subs({x: 0.1727, m: 1e-3}))) > 1e-4)
# D0
E0_over_M = sp.simplify(E[0].subs(rin, 0)/M)
chk("C5 D0 (r_in -> 0): E_D0/M = a0 R/2 for EVERY M (scale-free in M, G): the only M-independent budget", sp.simplify(E0_over_M - a0*R/2) == 0)
chk("C6 with r_in = r_M(M): E_D0/M = (a0 R - sqrt(G M a0))/2 (M-dependent again)", sp.simplify(sp.simplify(E[0].subs(rin, rM)/M) - (a0*R - sp.sqrt(G*M*a0))/2) == 0)

# ------------------------------------------------------------------ D  identities with no rho
Ms = 1/(4*G*a0); rsa = 1/(2*a0); Ra = 1/a0
chk("D1 M_a = 1/(G a0): MOND radius r_M(M_a) = 1/a0 = R_a and Schwarzschild radius 2 G M_a = 2 R_a", sp.simplify(rM.subs(M, Ma) - Ra) == 0 and sp.simplify(2*G*Ma - 2*Ra) == 0)
chk("D2 M_s = 1/(4 G a0) (black hole with surface gravity a0): r_M(M_s) = r_s(M_s) = 1/(2 a0) (its Newtonian acceleration at the horizon is a0: no deep-MOND region outside it)",
    sp.simplify(rM.subs(M, Ms) - rsa) == 0 and sp.simplify(2*G*Ms - rsa) == 0 and sp.simplify(G*Ms/rsa**2 - a0) == 0)
chk("D3 E_D0(M_a; 0 -> R) = R/(2G) for EVERY R and a0: field energy of M_a out to R equals the mass that makes R a horizon (pure identity: G M_a a0 = 1, no rho)",
    sp.simplify(E[0].subs(rin, 0).subs(M, Ma) - R/(2*G)) == 0)
chk("D4 E_D0(M; 0 -> R)/M at R = R_a is exactly 1/2 and at R = r_sa exactly 1/4 (no rho, no G): a0-defined lengths give rational identities",
    sp.simplify(E0_over_M.subs(R, Ra) - sp.Rational(1, 2)) == 0 and sp.simplify(E0_over_M.subs(R, rsa) - sp.Rational(1, 4)) == 0)
# sup bound for the rest-energy budget at R = L (uses only a0 L = 1/Z): the needed Z for E/M = 1
print("\nRest-energy budget out to the Hubble radius (x = a0 L = 1/Z):")
print("   sup_M E_D0/M = 1/(2Z),  sup_M E_D1/M = 1/(3 e Z),  sup_M E_D2/M = 2/(3 e Z)")
print("   E/M = 1 is reachable only if a0 L >= 2 (D0), 3e = 8.15 (D1), 3e/2 = 4.08 (D2), i.e. a0 >= 2 H, 8.15 H, 4.08 H  (framework: a0 = H/5.789)")
for name, need in (("D0", 2), ("D1", 3*mp.e), ("D2", 3*mp.e/2)):
    print("   %s: required a0/H = %.4f  => required Z = %.4f, kappa = a0/sqrt(G rho) = (a0/H) sqrt(8 pi/3) = %.4f (framework 0.5)" % (name, need, 1/need, need*mp.sqrt(8*mp.pi/3)))
Zt = mp.sqrt(32*mp.pi/3)      # target Z, used only here as a comparison (end of script)
ratios = [need*Zt for need in (2, 3*mp.e, 3*mp.e/2)]
print("   required a0 divided by the framework a0 = H/Z:", [mp.nstr(q, 5) for q in ratios])
chk("D5 the 'field energy out to the horizon = rest energy' budget needs a0 >= 2 H (D0) / 8.15 H (D1) / 4.08 H (D2): a factor 11.6 / 47.2 / 23.6 above H/Z", all(q > 11 for q in ratios))

print("\nTOTAL", sum(ok), "/", len(ok), "pass;", len(ok) - sum(ok), "fail")
