#!/usr/bin/env python3
"""
ADVERSARIAL INDEPENDENT VERIFICATION of the tensor-sector derivation for the v7 action.

Written from scratch, deliberately different route from tensor_sector_v7.py:
  * EXACT inverse metric and EXACT Christoffels (rational functions of eps) -- series
    expansion happens only at the very end, on the assembled Lagrangian;
  * Riemann tensor computed in full (R^rho_{sig mu nu}), then contracted -- not the
    Ricci-from-Christoffel shortcut of the original script;
  * the aether sector includes the terms the original script OMITTED, with ARBITRARY
    coefficients: cJ * J^mu grad_mu phi (AeST's 2(2-K_B) term, J^mu = A^nu nabla_nu A^mu)
    and cY * Y (AeST's -(2-K_B) term), on top of cF * F^2 and lam*(A.A+1);
  * the F_Y(0) robustness question: the volume term is kept with a SYMBOLIC W(t) =
    A(Qbar) F_Y(0)/8 pi G (not assumed zero) to see whether masslessness survives F_Y(0)!=0;
  * quadratic coefficients extracted by an INDEPENDENT method: substitute explicit Fourier
    profiles hp = f1(t) cos(kz) + f2(t) sin(kz), hx = f3 cos + f4 sin, integrate z over a
    period, then 1-D IBP in t only -- no 2-D IBP bookkeeping shared with the original;
  * background ij equation derived INDEPENDENTLY by mini-superspace Euler-Lagrange in a(t)
    on the zeroth-order Lagrangian (not from G_ij).
"""
import sympy as sp
from sympy import sqrt, pi, Function, Derivative, Rational

t, zz, eps = sp.symbols('t z epsilon', real=True)
k = sp.Symbol('k', positive=True)
x1, x2 = sp.symbols('x1 x2', real=True)
G, Lam, cF, cJ, cY, lam = sp.symbols('G Lambda c_F c_J c_Y lambda', real=True)
pm = sp.Symbol('p_m', real=True)
a = Function('a', positive=True)(t)
hp = Function('hp', real=True)(t, zz)
hx = Function('hx', real=True)(t, zz)
phib = Function('phibar', real=True)(t)
Kbg = Function('Kbg', real=True)(t)     # K(Qbar(t))
W = Function('W', real=True)(t)         # A(Qbar) F_Y(0) / 8 pi G  -- NOT assumed zero
coords = [t, x1, x2, zz]

# ---------- metric: EXACT ----------
hmat = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
g = sp.diag(-1, 0, 0, 0)
g = sp.zeros(4, 4); g[0, 0] = -1
for i in range(3):
    for j in range(3):
        g[i+1, j+1] = a**2 * ((1 if i == j else 0) + eps*hmat[i, j])

ginv = sp.simplify(g.inv())            # EXACT
detg = sp.factor(g.det())              # EXACT

print("== EXACT structure checks ==")
print("g^00 =", sp.simplify(ginv[0, 0]), " g^0i =", [sp.simplify(ginv[0, i+1]) for i in range(3)])
assert sp.simplify(ginv[0, 0] + 1) == 0
assert all(sp.simplify(ginv[0, i+1]) == 0 for i in range(3))
print("det g =", detg)
assert sp.simplify(detg + a**6*(1 - eps**2*(hp**2 + hx**2))) == 0

# ---------- Christoffels: EXACT ----------
def Gamma_exact():
    Gam = [[[sp.S(0)]*4 for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            for rho in range(nu, 4):
                s = sp.S(0)
                for sig in range(4):
                    if ginv[mu, sig] == 0:
                        continue
                    s += ginv[mu, sig]*(sp.diff(g[sig, rho], coords[nu])
                                        + sp.diff(g[sig, nu], coords[rho])
                                        - sp.diff(g[nu, rho], coords[sig]))
                s = sp.together(s/2)
                Gam[mu][nu][rho] = s
                Gam[mu][rho][nu] = s
    return Gam
Gam = Gamma_exact()

# sanity: Gamma^mu_{00} and Gamma^0_{0mu} exactly zero (needed for J^mu = 0 exactly)
for mu in range(4):
    assert sp.simplify(Gam[mu][0][0]) == 0
    assert sp.simplify(Gam[0][0][mu]) == 0

# ---------- Riemann -> Ricci -> R (full Riemann route) ----------
def riemann_ric():
    Ric = sp.zeros(4, 4)
    for sig in range(4):
        for nu in range(sig, 4):
            s = sp.S(0)
            for rho in range(4):
                # R^rho_{sig rho nu}
                term = sp.diff(Gam[rho][rho][sig], coords[nu]) * (-1) \
                     + sp.diff(Gam[rho][nu][sig], coords[rho])
                for lamb in range(4):
                    term += Gam[rho][rho][lamb]*Gam[lamb][nu][sig] \
                          - Gam[rho][nu][lamb]*Gam[lamb][rho][sig]
                s += term
            # series-truncate each entry to O(eps^2) for tractability (entries derived
            # from EXACT Gammas -- truncation only here, and order-2 is all we need)
            s = sp.series(sp.together(s), eps, 0, 3).removeO()
            Ric[sig, nu] = sp.expand(s)
            Ric[nu, sig] = Ric[sig, nu]
    return Ric
Ric = riemann_ric()
Rscal = sp.S(0)
for m in range(4):
    for n in range(4):
        if Ric[m, n] == 0:
            continue
        Rscal += sp.series(sp.together(ginv[m, n]), eps, 0, 3).removeO() * Ric[m, n]
Rscal = sp.expand(Rscal)
Rscal = sum(c*eps**m for (m,), c in sp.Poly(Rscal, eps).terms() if m <= 2)

R_bg = sp.simplify(Rscal.subs(eps, 0))
print("R(FRW background) =", R_bg, " (expect 6(addot/a + adot^2/a^2))")
assert sp.simplify(R_bg - 6*(sp.diff(a, t, 2)/a + sp.diff(a, t)**2/a**2)) == 0

# ---------- aether sector, EXACT, tensor mode (delta A = 0) ----------
A_up = sp.Matrix([1, 0, 0, 0])
norm = sp.simplify(sum(g[m, n]*A_up[m]*A_up[n] for m in range(4) for n in range(4)))
assert sp.simplify(norm + 1) == 0          # A^0 = 1 EXACT; lam-term = 0 exact
A_dn = sp.Matrix([sp.simplify(sum(g[m, n]*A_up[n] for n in range(4))) for m in range(4)])
assert list(A_dn) == [-1, 0, 0, 0]

F = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        F[m, n] = sp.diff(A_dn[n], coords[m]) - sp.diff(A_dn[m], coords[n])
assert all(sp.simplify(F[m, n]) == 0 for m in range(4) for n in range(4))
print("F_mn = 0 EXACT: yes")

# J^mu = A^nu nabla_nu A^mu = Gamma^mu_{00} = 0 exact (asserted above)
Jup = sp.Matrix([sp.simplify(Gam[mu][0][0]) for mu in range(4)])
assert all(x == 0 for x in Jup)
JdPhi = sp.simplify(sum(Jup[m]*sp.diff(phib, coords[m]) for m in range(4)))
assert JdPhi == 0
print("J^mu grad_mu phi = 0 EXACT: yes  (the AeST 2(2-K_B) term the original OMITTED is safe)")

dphi = sp.Matrix([sp.diff(phib, c) for c in coords])
Q = sp.simplify(sum(A_up[m]*dphi[m] for m in range(4)))
Y = sp.simplify(sum((ginv[m, n] + A_up[m]*A_up[n])*dphi[m]*dphi[n]
                    for m in range(4) for n in range(4)))
print("Q =", Q, "  Y =", Y, " (EXACT)")
assert sp.simplify(Q - sp.diff(phib, t)) == 0 and sp.simplify(Y) == 0
# => cY * Y term (also omitted by the original) contributes 0 exactly in the tensor sector.
# => B(Y/A) u^2 term: B(0) = 0 with B(y)=y/(1+y)^2  => 0 exactly. F_Y term: kept as W(t) below.

# ---------- assemble L to O(eps^2) ----------
sqrtmg = sp.series(sqrt(-detg), eps, 0, 3).removeO()
L_geom = sqrtmg*(Rscal - 2*Lam + cF*sp.S(0) + cJ*JdPhi + cY*Y + lam*(norm + 1))/(16*pi*G)
L_dark = sqrtmg*(Kbg + W)      # K(Qbar) + the F_Y(0) volume term, W NOT assumed 0
L_mat  = sqrtmg*pm             # ASSUMED on-shell perfect-fluid volume coupling (as claimed)
L = sp.expand(L_geom + L_dark + L_mat)
L = sum(c*eps**m for (m,), c in sp.Poly(L, eps).terms() if m <= 2)
L0 = L.coeff(eps, 0); L1 = L.coeff(eps, 1); L2 = L.coeff(eps, 2)

print("\nL1 (should be identically 0, not merely total derivative):", sp.simplify(L1))
assert sp.simplify(L1) == 0

# ---------- INDEPENDENT background ij equation: mini-superspace EL in a(t) ----------
adot, addot = sp.diff(a, t), sp.diff(a, t, 2)
EL_a = sp.diff(L0, a) - sp.diff(sp.diff(L0, adot), t) + sp.diff(sp.diff(L0, addot), t, 2)
EL_a = sp.expand(sp.simplify(EL_a))
bg = sp.simplify(EL_a / (3*a**2/(8*pi*G)))   # normalise
print("\nMini-superspace background eq (independent route):", bg, "= 0")
bg_expected = 2*addot/a + adot**2/a**2 - Lam + 8*pi*G*(Kbg + W + pm)
assert sp.simplify(bg - bg_expected) == 0
print("  == 2 addot/a + H^2 - Lambda + 8 pi G (K + W + p_m): CONFIRMED")

# ---------- INDEPENDENT quadratic-coefficient extraction: Fourier + z-integration ----------
f1 = Function('f1', real=True)(t); f2 = Function('f2', real=True)(t)
f3 = Function('f3', real=True)(t); f4 = Function('f4', real=True)(t)
subs_map = {hp: f1*sp.cos(k*zz) + f2*sp.sin(k*zz),
            hx: f3*sp.cos(k*zz) + f4*sp.sin(k*zz)}
L2f = L2
for fld, expr in subs_map.items():
    L2f = L2f.subs(fld, expr)
L2f = sp.expand(sp.expand_trig(sp.doit(L2f) if hasattr(sp, 'doit') else L2f))
L2f = L2f.doit()
Lred = sp.integrate(L2f, (zz, 0, 2*sp.pi/k))
Lred = sp.expand(sp.simplify(Lred))

# 1-D IBP in t only:  c f fddot -> -c fdot^2 - cdot f fdot ; then c f fdot -> -(1/2) cdot f^2
def ibp_t(Lr):
    Lr = sp.expand(Lr)
    for f in [f1, f2, f3, f4]:
        fd, fdd = Derivative(f, t), Derivative(f, (t, 2))
        c = Lr.coeff(f*fdd)
        if c != 0:
            Lr = sp.expand(Lr - c*f*fdd - c*fd**2 - sp.diff(c, t)*f*fd)
        c = Lr.coeff(f*fd)
        if c != 0:
            Lr = sp.expand(Lr - c*f*fd - Rational(1, 2)*sp.diff(c, t)*f**2)
    return sp.expand(Lr)
Lred = ibp_t(Lred)

print("\n== Independent Fourier-reduced quadratic Lagrangian (per z-period) ==")
coefs = {}
res = Lred
for f in [f1, f2, f3, f4]:
    cK = Lred.coeff(Derivative(f, t)**2)
    cM = Lred.coeff(f**2)
    coefs[f.func.__name__] = (sp.simplify(cK), sp.expand(cM))
    res = res - cK*Derivative(f, t)**2 - cM*f**2
res = sp.simplify(res)
print("  residual (cross terms etc.):", res)
assert res == 0

per = sp.pi/k   # integral of cos^2 or sin^2 over one period
for name, (cK, cM) in coefs.items():
    # claimed: kinetic  a^3/(32 pi G) * per ; mass: [-a k^2/(32 pi G) - a^3/(16 pi G) bg] * per
    kin_claim = a**3/(32*pi*G)*per
    mass_claim = (-a*k**2/(32*pi*G) - a**3/(16*pi*G)*bg_expected)*per
    dK = sp.simplify(cK - kin_claim)
    dM = sp.simplify(sp.expand(cM - mass_claim))
    print(f"  {name}: kinetic - claim = {dK} ; mass - [gradient + (-a^3/16piG)*bg] = {dM}")
    assert dK == 0 and dM == 0

print("\n  => per polarisation: hdot^2 coeff a^3/(32 pi G); gradient k^2 coeff -a/(32 pi G);")
print("     mass coeff = -a^3/(16 pi G) * [background eq INCLUDING W] -> 0 on shell EVEN IF F_Y(0) != 0.")
print("     c_T^2 = (a^3/(32 pi G)) vs (a/(32 pi G)) k^2  => omega^2 = k^2/a^2  => c_T = 1 EXACT.")

# ---------- EOM cross-check ----------
from sympy.calculus.euler import euler_equations
addot_sol = sp.solve(sp.Eq(bg_expected, 0), addot)[0]
eqs = euler_equations(L2, [hp, hx], [t, zz])
for f, e in zip([hp, hx], eqs):
    lhs = sp.expand(e.lhs - e.rhs)
    lhs = sp.expand(sp.simplify(lhs / lhs.coeff(Derivative(f, (t, 2)))))
    lhs = sp.expand(sp.simplify(lhs.subs(addot, addot_sol)))
    resid = sp.simplify(lhs - (Derivative(f, (t, 2)) + 3*sp.diff(a, t)/a*Derivative(f, t)
                               - Derivative(f, (zz, 2))/a**2))
    print(f"  EOM residual for {f.func.__name__}: {resid}")
    assert resid == 0

print("\nALL INDEPENDENT CHECKS PASSED")
