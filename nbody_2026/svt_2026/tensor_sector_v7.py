#!/usr/bin/env python3
"""
TENSOR SECTOR of the v7 THE_COMPLETION action (AeST + factorised F(Y,Q) + v7 promotion
A(Q) = kappa^2 G (-K(Q)), K(Q) = -M^4 sqrt(1 - mu^2 (Q-Q0)^2 / M^4)).

Gauge / conventions:
  signature (-,+,+,+); cosmic time; ds^2 = -dt^2 + a^2(t) (delta_ij + h_ij) dx^i dx^j
  h_ij transverse-traceless, single Fourier direction z:
     h_ij = [ h_p(t,z)   h_x(t,z)  0 ]
            [ h_x(t,z)  -h_p(t,z)  0 ]
            [    0          0      0 ]
  (both polarisations; propagation along z, trace = 0, del^i h_ij = 0 identically
   because the only z-row/column is zero and fields depend on t,z only).
  eps = formal perturbation-order parameter; every quantity truncated at O(eps^2).

Fields: aether A^mu (background (1,0,0,0)), khronon phi = phibar(t) (no tensor part:
h_ij is helicity-2, a scalar has none), metric TT h_ij.

We expand EVERY term of the action to O(h^2) by explicit component computation:
  (1/16piG)[ R - 2 Lambda - (K_B/2) F^2 + lam (A.A + 1) ]
  + (A(Q)/8piG) F_Y(Y/A(Q)) + K(Q) + A_b B(Y/A(Q)) (Q-Q0)^2
  + L_matter (perfect fluid, on-shell L_m = p_m(t): volume coupling only, ASSUMED standard)
"""
import sympy as sp
from sympy import Rational, sqrt, pi, Function, Derivative, simplify, expand

t, zz, eps, k = sp.symbols('t z epsilon k', real=True)
x1, x2 = sp.symbols('x y', real=True)
G, Lam, KB, lam_m, pm = sp.symbols('G Lambda K_B lambda p_m', real=True)
a = Function('a', positive=True)(t)
hp = Function('h_p', real=True)(t, zz)
hx = Function('h_x', real=True)(t, zz)
phib = Function('phibar', real=True)(t)
Kf = Function('Kbg', real=True)(t)   # K(Qbar(t)) as a background function of t
coords = [t, x1, x2, zz]

def trunc(e, n=2):
    """Drop all powers of eps above n."""
    e = sp.expand(e)
    p = sp.Poly(e, eps)
    out = 0
    for (m,), c in p.terms():
        if m <= n:
            out += c * eps**m
    return out

# ---------------- metric ----------------
h = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
g = sp.zeros(4, 4)
g[0, 0] = -1
for i in range(3):
    for j in range(3):
        g[i+1, j+1] = a**2 * (sp.eye(3)[i, j] + eps*h[i, j])

print("CHECK 0: TT conditions")
print("  trace delta^ij h_ij =", sp.simplify(h.trace()))
div = [sum(sp.diff(h[i, j], coords[j+1]) for j in range(3)) for i in range(3)]
print("  del^j h_ij =", [sp.simplify(d) for d in div])
assert h.trace() == 0 and all(sp.simplify(d) == 0 for d in div)

detg = sp.factor(g.det())
print("\nCHECK 1: det g (EXACT):", detg)
sqrtmg_exact = sqrt(-detg)
sqrtmg = trunc(sp.series(sqrtmg_exact, eps, 0, 3).removeO())
print("  sqrt(-g) to O(eps^2):", sqrtmg)

ginv_exact = g.inv()
ginv = ginv_exact.applyfunc(lambda e: trunc(sp.series(sp.together(e), eps, 0, 3).removeO()))
print("\nCHECK 2: g^{00} EXACT =", sp.simplify(ginv_exact[0, 0]),
      " g^{0i} EXACT =", [sp.simplify(ginv_exact[0, i+1]) for i in range(3)])
assert sp.simplify(ginv_exact[0, 0] + 1) == 0
assert all(sp.simplify(ginv_exact[0, i+1]) == 0 for i in range(3))

# ---------------- Christoffels, Ricci, R ----------------
def christoffels(gmat, ginvmat):
    Gam = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(4):
            for rho in range(nu, 4):
                s = 0
                for sig in range(4):
                    if ginvmat[mu, sig] == 0:
                        continue
                    s += ginvmat[mu, sig]*(sp.diff(gmat[sig, rho], coords[nu])
                                           + sp.diff(gmat[sig, nu], coords[rho])
                                           - sp.diff(gmat[nu, rho], coords[sig]))
                s = trunc(Rational(1, 2)*s)
                Gam[mu][nu][rho] = s
                Gam[mu][rho][nu] = s
    return Gam

Gam = christoffels(g, ginv)

def ricci(Gam):
    Ric = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(mu, 4):
            s = 0
            for rho in range(4):
                s += sp.diff(Gam[rho][mu][nu], coords[rho]) - sp.diff(Gam[rho][mu][rho], coords[nu])
                for lamb in range(4):
                    s += Gam[rho][rho][lamb]*Gam[lamb][mu][nu] - Gam[rho][nu][lamb]*Gam[lamb][mu][rho]
            Ric[mu, nu] = trunc(sp.expand(s))
            Ric[nu, mu] = Ric[mu, nu]
    return Ric

Ric = ricci(Gam)
Rscal = trunc(sp.expand(sum(ginv[mu, nu]*Ric[mu, nu] for mu in range(4) for nu in range(4))))

# ---------------- aether sector ----------------
# Tensor sector: A^mu has no helicity-2 part => delta A^mu = 0 (SVT theorem; the explicit
# no-mixing check with helicity-0/1 delta A is done in aether_cross_check.py).
# Unit norm: g_mn A^m A^n = -1 with A = (A0,0,0,0): g00 A0^2 = -1, g00 = -1 EXACT => A0 = 1 EXACT.
A_up = sp.Matrix([1, 0, 0, 0])
norm = sp.simplify(sum(g[m, n]*A_up[m]*A_up[n] for m in range(4) for n in range(4)))
print("\nCHECK 3 (aether): A^mu A_mu EXACT =", norm, " => A^0 = 1 exactly, lam*(A.A+1) = 0 exactly")
assert sp.simplify(norm + 1) == 0
A_dn = sp.Matrix([sum(g[m, n]*A_up[n] for n in range(4)) for m in range(4)])
print("  A_mu EXACT =", list(A_dn))
# F_mn = del_m A_n - del_n A_m  (covariant antisymmetrised = partial antisymmetrised)
F = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        F[m, n] = sp.diff(A_dn[n], coords[m]) - sp.diff(A_dn[m], coords[n])
print("CHECK 4: F_{mu nu} EXACT (all components):", [sp.simplify(F[m, n]) for m in range(4) for n in range(4)])
assert all(sp.simplify(F[m, n]) == 0 for m in range(4) for n in range(4))
F2 = 0   # F^{mn}F_{mn} = 0 EXACTLY, to ALL orders in h => K_B term contributes NOTHING (no dh terms)

# ---------------- dark sector invariants ----------------
dphi = sp.Matrix([sp.diff(phib, c) for c in coords])   # (phibar', 0,0,0)
Q = sp.simplify(sum(A_up[m]*dphi[m] for m in range(4)))
Y = sp.simplify(sum((ginv_exact[m, n] + A_up[m]*A_up[n])*dphi[m]*dphi[n]
                    for m in range(4) for n in range(4)))
print("\nCHECK 5 (dark-sector invariants, EXACT in h):")
print("  Q =", Q, "  (= phibar_dot: NO h-dependence at any order)")
print("  Y =", Y, "  (h^{00} = g^{00}+A^0A^0 = 0 exactly => Y = 0 EXACTLY, all orders in h)")
assert sp.simplify(Q - sp.diff(phib, t)) == 0
assert sp.simplify(Y) == 0

# Consequences (F_Y(0)=0 since F_Y(y) -> (2/3)c y^{3/2}; B(0)=0 since B(y)=y/(1+y)^2):
#   (A(Q)/8piG) F_Y(Y/A) = (A(Qbar)/8piG) * F_Y(0) = 0   -- exactly, all orders in h
#   A_b B(Y/A)(Q-Q0)^2   = A_b * B(0) * u^2        = 0   -- exactly, all orders in h
#   K(Q) = K(Qbar(t))  -- a pure background function; enters ONLY through sqrt(-g)
# The v7 promotion A(Q) = kappa^2 G(-K(Q)) is algebraic in Q, and Q has no h-dependence,
# so the promotion generates NO tensor-sector coupling whatsoever.

# ---------------- assemble the Lagrangian density to O(eps^2) ----------------
L_EH   = trunc(sqrtmg * (Rscal - 2*Lam) / (16*pi*G))
L_dark = trunc(sqrtmg * Kf)          # the ONLY surviving dark-sector piece
L_mat  = trunc(sqrtmg * pm)          # on-shell perfect-fluid Lagrangian = pbar (ASSUMED standard)
L_ae   = 0                            # K_B F^2 term and lam constraint term: both EXACTLY zero
L = sp.expand(L_EH + L_dark + L_mat + L_ae)

L0 = L.coeff(eps, 0)
L1 = L.coeff(eps, 1)
L2 = L.coeff(eps, 2)

# CHECK 6: linear order is pure total derivative (Euler operator annihilates it)
from sympy.calculus.euler import euler_equations
eqs1 = euler_equations(L1 if L1 != 0 else sp.Integer(0)*hp, [hp, hx], [t, zz]) if L1 != 0 else []
print("\nCHECK 6: O(eps^1) Lagrangian:", sp.simplify(L1))
if L1 != 0:
    print("  Euler operator on L1:", [sp.simplify(e.lhs - e.rhs) for e in eqs1])
    assert all(sp.simplify(e.lhs - e.rhs) == 0 for e in eqs1)

# ---------------- canonicalise L2 by integration by parts ----------------
fields = [hp, hx]
def ibp_canonical(L2):
    """Reduce quadratic L2 to A f_t^2 + B f_z^2 + C f^2 (+ cross terms if any) via IBP."""
    L2 = sp.expand(L2)
    changed = True
    while changed:
        changed = False
        L2 = sp.expand(L2)
        for f in fields:
            ft, fz = Derivative(f, t), Derivative(f, zz)
            ftt, fzz_, ftz = Derivative(f, (t, 2)), Derivative(f, (zz, 2)), Derivative(f, t, zz)
            # c f f_tt -> -c f_t^2 - c_t f f_t
            c = sp.expand(L2).coeff(f*ftt) if L2.has(ftt) else 0
            if c != 0:
                L2 = sp.expand(L2 - c*f*ftt - c*ft**2 - sp.diff(c, t)*f*ft); changed = True
            c = sp.expand(L2).coeff(f*fzz_) if L2.has(fzz_) else 0
            if c != 0:
                L2 = sp.expand(L2 - c*f*fzz_ - c*fz**2); changed = True
            c = sp.expand(L2).coeff(f*ftz) if L2.has(ftz) else 0
            if c != 0:
                L2 = sp.expand(L2 - c*f*ftz - c*ft*fz); changed = True   # IBP in z (c z-indep)
            c = sp.expand(L2).coeff(f*ft)
            if c != 0:
                # c f f_t = d/dt(c f^2/2) - (1/2) c_t f^2  =>  replace with -(1/2) c_t f^2
                L2 = sp.expand(L2 - c*f*ft - Rational(1, 2)*sp.diff(c, t)*f**2); changed = True
            c = sp.expand(L2).coeff(f*fz)
            if c != 0:
                L2 = sp.expand(L2 - c*f*fz); changed = True              # c z-indep: total deriv
    return sp.expand(L2)

L2c = ibp_canonical(L2)
print("\n================ QUADRATIC TENSOR ACTION (after IBP) ================")
L2c = sp.collect(L2c, [Derivative(hp, t)**2, Derivative(hx, t)**2,
                       Derivative(hp, zz)**2, Derivative(hx, zz)**2, hp**2, hx**2])
print("L2 =", L2c)

cA_p = L2c.coeff(Derivative(hp, t)**2);  cA_x = L2c.coeff(Derivative(hx, t)**2)
cB_p = L2c.coeff(Derivative(hp, zz)**2); cB_x = L2c.coeff(Derivative(hx, zz)**2)
cC_p = L2c.coeff(hp**2);                 cC_x = L2c.coeff(hx**2)
cross = sp.simplify(L2c - cA_p*Derivative(hp, t)**2 - cA_x*Derivative(hx, t)**2
                    - cB_p*Derivative(hp, zz)**2 - cB_x*Derivative(hx, zz)**2
                    - cC_p*hp**2 - cC_x*hx**2)
print("\n  hdot^2 coefficient  (+ pol):", sp.simplify(cA_p), "   (x pol):", sp.simplify(cA_x))
print("  (dz h)^2 coefficient (+ pol):", sp.simplify(cB_p), "   (x pol):", sp.simplify(cB_x))
print("  h^2 coefficient      (+ pol):", sp.simplify(cC_p), "   (x pol):", sp.simplify(cC_x))
print("  residual cross/other terms:", cross)
assert cross == 0, "unexpected cross terms"
assert sp.simplify(cA_p - cA_x) == 0 and sp.simplify(cB_p - cB_x) == 0 and sp.simplify(cC_p - cC_x) == 0

cT2 = sp.simplify(-cB_p/cA_p * a**2)
print("\n  c_T^2 = (-B/A) * a^2 =", cT2)
assert cT2 == 1

# ---------------- the h^2 (mass) coefficient vs the background EOM ----------------
adot, addot = sp.diff(a, t), sp.diff(a, t, 2)
# background ij Einstein equation (derived below in CHECK 8): 2 addot/a + (adot/a)^2 - Lam = -8 pi G p_tot
bgij = 2*addot/a + (adot/a)**2 - Lam + 8*pi*G*(Kf + pm)
ratio = sp.simplify(cC_p / bgij)
print("\nCHECK 7: mass coefficient / background-ij-equation =", ratio)
print("  => C = (that factor) * [background ij Einstein eq] -> 0 ON SHELL; gravitons massless.")
addot_sol0 = sp.solve(sp.Eq(bgij, 0), sp.diff(a, t, 2))[0]
cC_onshell = sp.simplify(cC_p.subs(sp.diff(a, t, 2), addot_sol0))
print("  C on the background shell =", cC_onshell)
assert cC_onshell == 0
assert not ratio.has(sp.Derivative(a, (t, 2)))  # clean proportionality, no leftover addot

# CHECK 8: derive the background ij equation from THIS code (G_ij at eps=0)
G_ij_bg = sp.simplify((Ric[1, 1] - Rational(1, 2)*g[1, 1]*Rscal).subs(eps, 0))
einstein_ij = sp.simplify(G_ij_bg + Lam*g[1, 1].subs(eps, 0) - 8*pi*G*(Kf + pm)*g[1, 1].subs(eps, 0))
# T_ij for L=K(Q)+p_m with Y=0: T_mn = g_mn K + (K' terms) A_m A_n ... spatial part = p g_ij, p = K
print("CHECK 8: background G_ij + Lam g_ij - 8piG p_tot g_ij =", einstein_ij)
print("  setting this = 0 IS the ij Friedmann equation used in CHECK 7:")
print("  ", sp.simplify(sp.expand(einstein_ij / (-a**2))), " = 0  <=> ", sp.simplify(bgij), "= 0")
check8 = sp.simplify(einstein_ij + a**2*bgij)
print("  identity residual:", check8)
assert check8 == 0

# ---------------- EOM route (independent of the IBP bookkeeping) ----------------
eqs = euler_equations(L2, [hp, hx], [t, zz])
print("\nCHECK 9: linear EOM from Euler operator on L2 (then substitute background ij eq):")
for f, e in zip([hp, hx], eqs):
    lhs = sp.expand(e.lhs - e.rhs)
    # normalise by the hddot coefficient
    chdd = lhs.coeff(Derivative(f, (t, 2)))
    lhs_n = sp.expand(sp.simplify(lhs/chdd))
    # impose the background ij equation: solve for addot
    addot_sol = sp.solve(sp.Eq(bgij, 0), addot)[0]
    lhs_os = sp.expand(sp.simplify(lhs_n.subs(addot, addot_sol)))
    lhs_os = sp.collect(lhs_os, [Derivative(f, (t, 2)), Derivative(f, t), Derivative(f, (zz, 2)), f])
    print(f"  {f.func.__name__}:  ", lhs_os, " = 0")
    c_hdd = lhs_os.coeff(Derivative(f, (t, 2)))
    c_hd  = sp.simplify(lhs_os.coeff(Derivative(f, t)))
    c_hzz = sp.simplify(lhs_os.coeff(Derivative(f, (zz, 2))))
    c_h   = sp.simplify(lhs_os.coeff(f))
    print(f"     coeff hddot = {c_hdd},  coeff hdot = {c_hd},  coeff dz^2 h = {c_hzz},  coeff h = {c_h}")
    assert c_hdd == 1
    assert sp.simplify(c_hd - 3*adot/a) == 0
    assert sp.simplify(c_hzz + 1/a**2) == 0
    assert c_h == 0
    # k-space: dz^2 -> -k^2  =>  hddot + 3H hdot + (k^2/a^2) h = 0  =>  c_T^2 = 1 EXACTLY
print("\n  ON SHELL:  hddot + 3H hdot + (k^2/a^2) h = 0   for BOTH polarisations  =>  c_T^2 = 1 EXACT")

print("\nALL ASSERTIONS PASSED")
