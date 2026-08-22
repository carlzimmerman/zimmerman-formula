#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECTION 13 -- FLRW background of the FROZEN ACTION (first-principles, sympy-verified).

Frozen action (c = 1 units here; the prefactor (M_Pl^2 c^3/2) with the repo's
normalisation anchor equals c^4/(16 pi G) -> 1/(16 pi G)):

  S = (1/16 pi G) INT dt d^3x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2
        + eta_K a_i a^i - 2 a0^2 F(X,Y) ]  +  S_m[g, psi_m]

  F(X,Y) = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps X^2/(1+X)^4 Y

WHAT THIS SCRIPT DERIVES AND VERIFIES (all sympy, PASS/FAIL, exit 1 on any FAIL):

  [13.1] Comoving foliation T = t on flat FLRW: u_mu = (-N,0,0,0), u.u = -1,
         acceleration a_mu = 0  =>  X = 0 exactly.                       [DERIVED]
  [13.2] K_ij = H h_ij with H = adot/(N a); K = 3H. Flat slices:
         (3)R_ij = 0 => Rbar_munu = 0 => Y = 0 exactly.                  [DERIVED]
  [13.3] F(0,0) = 0 EXACTLY (the ln term: 2 ln 1 = 0); no constant term in
         the expansion => NO induced cosmological constant. Consequence:
         this action supplies NO dark energy of its own; Lambda, if wanted,
         must be added by hand.                                          [DERIVED]
  [13.4] Modified Friedmann I from the N-variation of the mini-superspace
         action:  3 (3 lam_K - 1) H^2 = 16 pi G eps
         =>  H^2 = (8 pi G_cosmo / 3) eps  with  G_cosmo = 2G/(3 lam_K - 1).
         eta_K does NOT enter (a_i = 0 on the background); the F-term does
         NOT enter (F(0,0)=0 and its first variation multiplies dX, dY which
         are second order in perturbations).                             [DERIVED]
  [13.5] Friedmann II from the a-variation:
         (3 lam_K - 1)(2 addot/a + H^2) = -16 pi G p, same G_cosmo; and
         addot/a = -(4 pi G_cosmo/3)(eps + 3p).                          [DERIVED]
  [13.6] Consistency (Bianchi-type identity of the reparametrisation-invariant
         mini-superspace system):
            d/dt C1 + 3 H C1 = -16 pi G [ eps_dot + 3H(eps+p) ]   on the FII shell,
         C1 := 3(3 lam_K -1)H^2 - 16 pi G eps.
         => constraint + FII force the continuity equation, and the khronon
         equation is REDUNDANT on FLRW (no independent condition).       [DERIVED]
  [13.7] Sign/viability: eps > 0 requires lam_K > 1/3.                   [DERIVED]

STATED, NOT DERIVED:
  * a0 = 9.3619e-11 m/s^2 is a FUNDAMENTAL INPUT of the frozen action. It is
    NOT derived anywhere in this section.                                 [ASSUMED]
  * BBN/CMB expansion-rate constraint (see sec14 script for G_local):
    G_cosmo/G_local = (2 - eta_K)/(3 lam_K - 1) must be 1 within ~13% (BBN,
    Carroll & Lim 2004, PRD 70 123525; modern He-4 abundances tighten this to
    a few %).  IMPORTED(cite) for the numeric bound; the ratio is DERIVED.
"""
import sys
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
lam = sp.Symbol('lambda_K', real=True)
eta = sp.Symbol('eta_K', real=True)
G = sp.Symbol('G', positive=True)
a0 = sp.Symbol('a0', positive=True)
epsY = sp.Symbol('epsilon', real=True)
pi = sp.pi

results = []
def check(name, cond):
    ok = bool(cond)
    results.append(ok)
    print(("PASS: " if ok else "FAIL: ") + name)

# ----------------------------------------------------------------------------
# [13.1]-[13.2] geometry of the comoving foliation on flat FLRW
# ----------------------------------------------------------------------------
coords = [t, x, y, z]
N = sp.Function('N', positive=True)(t)
a = sp.Function('a', positive=True)(t)

g = sp.diag(-N**2, a**2, a**2, a**2)
ginv = g.inv()

def christoffels(gmat, gmatinv, crds):
    n = len(crds)
    Gam = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                expr = sum(gmatinv[l, s]*(sp.diff(gmat[s, m], crds[nu])
                                          + sp.diff(gmat[s, nu], crds[m])
                                          - sp.diff(gmat[m, nu], crds[s]))
                           for s in range(n))/2
                Gam[l][m][nu] = sp.simplify(expr)
    return Gam

Gam = christoffels(g, ginv, coords)

# khronon T = t; u_mu = -grad_mu T / sqrt(-grad T.grad T)
gradT = [sp.S(1), sp.S(0), sp.S(0), sp.S(0)]
norm2 = sum(ginv[i, j]*gradT[i]*gradT[j] for i in range(4) for j in range(4))
u_lo = [sp.simplify(-gradT[m]/sp.sqrt(-norm2)) for m in range(4)]
u_up = [sp.simplify(sum(ginv[m, n_]*u_lo[n_] for n_ in range(4))) for m in range(4)]

check("[13.1] u_mu = (-N,0,0,0) and u^mu = (1/N,0,0,0) from T=t",
      sp.simplify(u_lo[0] + N) == 0 and sp.simplify(u_up[0] - 1/N) == 0
      and all(u_lo[i] == 0 and u_up[i] == 0 for i in (1, 2, 3)))
check("[13.1] u.u = -1 (unit, timelike)",
      sp.simplify(sum(u_up[m]*u_lo[m] for m in range(4)) + 1) == 0)

def nabla_lo(vlo, A, m):
    """nabla_A v_m for a covector field vlo."""
    return sp.diff(vlo[m], coords[A]) - sum(Gam[l][A][m]*vlo[l] for l in range(4))

acc = [sp.simplify(sum(u_up[n_]*nabla_lo(u_lo, n_, m) for n_ in range(4)))
       for m in range(4)]
check("[13.1] acceleration a_mu = u^nu nabla_nu u_mu = 0  =>  X = 0 exactly",
      all(sp.simplify(c) == 0 for c in acc))

h_lo = sp.Matrix(4, 4, lambda i, j: sp.simplify(g[i, j] + u_lo[i]*u_lo[j]))
h_mix = sp.Matrix(4, 4, lambda i, j: sp.simplify(
    sum(ginv[i, kk]*h_lo[kk, j] for kk in range(4))))
K_lo = sp.Matrix(4, 4, lambda m, n_: sp.simplify(
    sum(h_mix[A, m]*h_mix[B, n_]*nabla_lo(u_lo, A, B)
        for A in range(4) for B in range(4))))
H_loc = sp.diff(a, t)/(N*a)
check("[13.2] K_munu = H h_munu with H = adot/(N a)",
      all(sp.simplify(K_lo[i, j] - H_loc*h_lo[i, j]) == 0
          for i in range(4) for j in range(4)))
Ktr = sp.simplify(sum(ginv[i, j]*K_lo[i, j] for i in range(4) for j in range(4)))
check("[13.2] K = 3 adot/(N a)", sp.simplify(Ktr - 3*H_loc) == 0)

# flat slices: h_ij = a(t)^2 delta_ij has NO spatial dependence -> all spatial
# Christoffels vanish -> (3)R_ij = 0 -> Rbar_munu (trace-free part) = 0 -> Y = 0.
h3 = sp.diag(a**2, a**2, a**2)
sp3 = [x, y, z]
check("[13.2] flat slices: d_k h_ij = 0 => (3)R_ij = 0 => Rbar = 0 => Y = 0",
      all(sp.diff(h3[i, j], c3) == 0
          for i in range(3) for j in range(3) for c3 in sp3))

# ----------------------------------------------------------------------------
# [13.3] F(0,0) = 0 exactly; no induced Lambda
# ----------------------------------------------------------------------------
X, Y = sp.symbols('X Y', nonnegative=True)
F = -2*sp.sqrt(X) + 2*sp.log(1 + sp.sqrt(X)) + epsY*X**2/(1 + X)**4*Y
check("[13.3] F(0,0) = 0 EXACTLY (ln term: 2 ln(1+0) = 0)",
      sp.limit(F.subs(Y, 0), X, 0, '+') == 0 and F.subs({X: 0, Y: 0}) == 0)
s = sp.Symbol('s', positive=True)          # s = sqrt(X)
Fs = sp.series(F.subs({Y: 0, X: s**2}), s, 0, 6).removeO().expand()
check("[13.3] no constant term near X=0  =>  NO induced Lambda from the F-term",
      Fs.subs(s, 0) == 0)
check("[13.3] no sqrt(X) term either (the -2sqrt(X) and 2ln cancel at O(s))",
      Fs.coeff(s, 1) == 0)
check("[13.3] leading behaviour F = -X + (2/3) X^(3/2) + ...  (F_X(0) = -1)",
      Fs.coeff(s, 2) == -1 and Fs.coeff(s, 3) == sp.Rational(2, 3))
print("NOTE [13.3]: since X=Y=0 exactly on FLRW at ALL times and F(0,0)=0, the")
print("  F-term contributes EXACTLY ZERO to the background at every epoch: this")
print("  action supplies no dark energy of its own (Lambda must be added by hand),")
print("  and it supplies no dark-matter-like background density either.")

# ----------------------------------------------------------------------------
# [13.4] Friedmann I from the N-variation (mini-superspace)
# ----------------------------------------------------------------------------
pref = 1/(16*pi*G)
adot = sp.diff(a, t)
# K_ij K^ij - lam_K K^2 = 3(1-3 lam_K)(adot/(N a))^2   [verified: K_ij = H h_ij]
kin = sp.simplify(sum(sum(ginv[i, k]*K_lo[k, j] for k in range(4))
                      * sum(ginv[j, l]*K_lo[l, i] for l in range(4))
                      for i in range(4) for j in range(4)) - lam*Ktr**2)
check("[13.4] K_ij K^ij - lam_K K^2 = 3(1-3 lam_K)(adot/(N a))^2",
      sp.simplify(kin - 3*(1 - 3*lam)*(adot/(N*a))**2) == 0)

Lg = pref*N*a**3*kin                       # (3)R = 0, X = Y = 0 on background
rho_e = sp.Function('rho_e', real=True)(a)  # fluid energy density eps(a)
Lm = -N*a**3*rho_e                          # delta S_m / delta N = -sqrt(h) eps
L = Lg + Lm

FI_raw = sp.simplify(sp.diff(L, N).subs(N, 1))
FI_target = 3*(3*lam - 1)*adot**2/a**2 - 16*pi*G*rho_e
check("[13.4] Friedmann I:  3(3 lam_K - 1) H^2 = 16 pi G eps",
      sp.simplify(FI_raw*16*pi*G/a**3 - FI_target) == 0)

Hs = sp.Symbol('H', positive=True)
eps_s = sp.Symbol('eps', positive=True)
H2 = sp.solve(3*(3*lam - 1)*Hs**2 - 16*pi*G*eps_s, Hs**2)[0]
Gc = sp.simplify(H2*3/(8*pi*eps_s))
check("[13.4] G_cosmo = 2 G / (3 lam_K - 1)",
      sp.simplify(Gc - 2*G/(3*lam - 1)) == 0)
check("[13.4] GR limit lam_K = 1: G_cosmo = G", sp.simplify(Gc.subs(lam, 1) - G) == 0)
print("NOTE [13.4]: eta_K does NOT enter the background (a_i = 0 identically);")
print("  the F-term does not enter (F(0,0)=0; dX, dY are 2nd order in perturbations).")
print("NOTE [13.7]: eps > 0 with H^2 > 0 REQUIRES lam_K > 1/3 (else wrong-sign")
print("  Friedmann equation).  [DERIVED]")

# ----------------------------------------------------------------------------
# [13.5] Friedmann II from the a-variation (manual Euler-Lagrange, N=1)
# ----------------------------------------------------------------------------
A, Ad, Add, p_s = sp.symbols('A Ad Add p', real=True)
re = sp.Function('re', real=True)(A)
L1s = pref*3*(1 - 3*lam)*A*Ad**2 - A**3*re
dLdAd = sp.diff(L1s, Ad)
ddt_dLdAd = sp.diff(dLdAd, A)*Ad + sp.diff(dLdAd, Ad)*Add
ELa = sp.expand(ddt_dLdAd - sp.diff(L1s, A))
# continuity defines p:  d eps/d a = -3(eps+p)/a
ELa = ELa.subs(sp.Derivative(re, A), -3*(re + p_s)/A)
FII_target = (3*lam - 1)*(2*Add/A + (Ad/A)**2) + 16*pi*G*p_s
sol1 = sp.solve(ELa, Add)
sol2 = sp.solve(FII_target, Add)
check("[13.5] Friedmann II: (3 lam_K - 1)(2 addot/a + H^2) = -16 pi G p",
      len(sol1) == 1 and len(sol2) == 1 and sp.simplify(sol1[0] - sol2[0]) == 0)

# acceleration equation with the SAME G_cosmo
addot_over_a = sp.simplify(sol2[0]/A)
H2_val = 16*pi*G*eps_s/(3*(3*lam - 1))
acc_target = -(4*pi/3)*(2*G/(3*lam - 1))*(eps_s + 3*p_s)
check("[13.5] addot/a = -(4 pi G_cosmo/3)(eps + 3p)  (same G_cosmo in FI and FII)",
      sp.simplify(addot_over_a.subs(Ad**2, H2_val*A**2) - acc_target) == 0)

# ----------------------------------------------------------------------------
# [13.6] Bianchi-type identity: constraint + FII  <=>  continuity;
#        the khronon equation is redundant on FLRW
# ----------------------------------------------------------------------------
af = sp.Function('a_f', positive=True)(t)
ef = sp.Function('eps_f', real=True)(t)
pf = sp.Function('p_f', real=True)(t)
Hf = sp.diff(af, t)/af
C1 = 3*(3*lam - 1)*Hf**2 - 16*pi*G*ef
FIIf = (3*lam - 1)*(2*sp.diff(af, t, 2)/af + Hf**2) + 16*pi*G*pf
add_sol = sp.solve(FIIf, sp.diff(af, t, 2))[0]
lhs = (sp.diff(C1, t) + 3*Hf*C1).subs(sp.Derivative(af, (t, 2)), add_sol)
rhs = -16*pi*G*(sp.diff(ef, t) + 3*Hf*(ef + pf))
check("[13.6] dC1/dt + 3H C1 = -16 pi G [eps' + 3H(eps+p)] on the FII shell",
      sp.simplify(lhs - rhs) == 0)
print("NOTE [13.6]: so (constraint + Friedmann II) FORCE continuity, and imposing")
print("  continuity preserves the constraint (C1' = -3H C1 => C1 = 0 stays 0).")
print("  The khronon equation of motion adds NO independent condition on FLRW:")
print("  time-reparametrisation invariance of the mini-superspace action makes it")
print("  redundant -- the comoving foliation T = t is automatically a solution.")

# ----------------------------------------------------------------------------
# BBN/CMB constraint (numeric statement; bound IMPORTED, ratio DERIVED here +
# in sec14 script for G_local)
# ----------------------------------------------------------------------------
lam_lo = (1 + 2/1.13)/3
lam_hi = (1 + 2/0.87)/3
print(f"NOTE: G_cosmo/G_local = (2 - eta_K)/(3 lam_K - 1). With |eta_K| << 1")
print(f"  (PPN preferred-frame bounds) and the BBN bound |G_cosmo/G_N - 1| < 0.13")
print(f"  [IMPORTED: Carroll & Lim 2004, PRD 70 123525]:")
print(f"     lam_K in [{lam_lo:.4f}, {lam_hi:.4f}]   (no fitting, direct inversion)")
print(f"  Modern He-4 (few-%) tightens this to lam_K = 1 +/- ~0.03.")
print("STATEMENT: a0 = 9.3619e-11 m/s^2 is a FUNDAMENTAL INPUT here. It is NOT")
print("  derived by this section (or by the frozen action).           [ASSUMED]")

n_fail = results.count(False)
print(f"\n{results.count(True)}/{len(results)} checks passed, {n_fail} failed.")
sys.exit(1 if n_fail else 0)
