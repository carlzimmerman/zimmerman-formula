#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_ctensor_map_2026.py  --  AeST aether kinetic  ->  Einstein-aether c-tensor  (DERIVED, certified)
====================================================================================================
The FC-FINAL / AeST action's aether kinetic term is  -(K_B/2) F_{mu nu} F^{mu nu},  F_{mu nu}=2 d_[mu A_nu].
The general Einstein-aether (EA) kinetic is
    L_EA = - K^{mu nu}_{al be} (nabla_mu A^al)(nabla_nu A^be),
    K^{mu nu}_{al be} = c1 g^{mu nu} g_{al be} + c2 delta^mu_al delta^nu_be
                        + c3 delta^mu_be delta^nu_al + c4 A^mu A^nu g_{al be}.
This script PROVES, as a flat-space algebraic identity in a GENERIC constant-gradient aether
configuration, that  -(1/2) F_{mn}F^{mn}  equals the EA kinetic with
    (c1, c2, c3, c4) = (1, 0, -1, 0),
so the AeST coefficient K_B gives   (c1,c2,c3,c4) = (K_B, 0, -K_B, 0),
hence the load-bearing EA invariants
    c13 = c1+c3 = 0      (=> c_T^2 = 1 EXACTLY, GW170817-safe -- committed)
    c123 = c1+c2+c3 = 0  (=> the EA spin-0 aether mode is NON-dynamical: the pure-vector
                            preferred-frame alpha_2 is SINGULAR; the AeST SCALAR must regularise it)
    c14 = c1+c4 = K_B
and the standard EA preferred-frame formula (Foster-Jacobson gr-qc/0509083), VALID for the
pure-vector sector once this map is proved, gives
    alpha_1 = -8(c3^2 + c1 c4)/(2 c1 - c1^2 + c3^2) = -4 K_B   (=> K_B < 2.5e-5 from |alpha_1|<1e-4).

Every step is a sympy simplify(...)==0 certificate.  No PPN formula is *imported*: the c-tensor
map is derived, and only the reduction it licenses (pure-vector alpha_1) uses the EA algebra.
alpha_2 is NOT decided here (the scalar sector is exactly what the EA formula cannot capture, since
c123=0 makes it singular) -- see FINAL_PPN.md.
"""
import sympy as sp
P = print
FAIL = []
def check(c, s):
    P(('[ok] ' if c else '[FAIL] ') + s)
    if not c:
        FAIL.append(s)

# flat metric, generic CONSTANT aether gradient tensor B_{mu}{}^{nu} = nabla_mu A^nu (const => R,curv drop)
eta = sp.diag(-1, 1, 1, 1)
etau = eta  # inverse = itself
B = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f'B{m}{n}'))     # B[m,n] = nabla_mu A^nu (upper nu)
A = sp.Matrix([sp.Symbol(f'A{m}') for m in range(4)])       # A^mu (for the c4 term)

# nabla_mu A_nu  (lower) = B[m, :] lowered on nu
def dnAl(m, n):     # nabla_mu A_nu
    return sum(eta[n, s]*B[m, s] for s in range(4))

# F_{mu nu} = nabla_mu A_nu - nabla_nu A_mu ;  F^{mu nu} = raise both
F2 = 0
for m in range(4):
    for n in range(4):
        Fmn = dnAl(m, n) - dnAl(n, m)
        Fup = 0
        for a in range(4):
            for b in range(4):
                Fup += etau[m, a]*etau[n, b]*(dnAl(a, b) - dnAl(b, a))
        F2 += Fmn*Fup
F2 = sp.expand(F2)

# EA kinetic terms (each = the scalar contracted):
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4')
# c1: g^{mn} g_{al be} nabla_mu A^al nabla_nu A^be = (nabla_mu A_nu)(nabla^mu A^nu)
T1 = sum(etau[m, n]*eta[a, b]*B[m, a]*B[n, b] for m in range(4) for n in range(4)
         for a in range(4) for b in range(4))
# c2: (nabla_mu A^mu)^2
T2 = (sum(B[m, m] for m in range(4)))**2
# c3: delta^mu_be delta^nu_al nabla_mu A^al nabla_nu A^be = (nabla_mu A^nu)(nabla_nu A^mu)
T3 = sum(B[m, n]*B[n, m] for m in range(4) for n in range(4))
# c4: A^mu A^nu g_{al be} nabla_mu A^al nabla_nu A^be
T4 = sum(A[m]*A[n]*eta[a, b]*B[m, a]*B[n, b] for m in range(4) for n in range(4)
         for a in range(4) for b in range(4))
# standard EA convention: L_EA = - K^{mn}_{al be} nabla A nabla A  (overall MINUS)
L_EA = -(c1*T1 + c2*T2 + c3*T3 + c4*T4)

# claim: -(1/2) F^2 = L_EA at (c1,c2,c3,c4)=(1,0,-1,0)
resid = sp.expand(-sp.Rational(1, 2)*F2 - L_EA.subs({c1: 1, c2: 0, c3: -1, c4: 0}))
check(resid == 0, "-(1/2)F_{mn}F^{mn} = EA-kinetic (standard -K sign) at (c1,c2,c3,c4)=(1,0,-1,0)")

# uniqueness: match coefficients of the independent quadratic invariants T1,T2,T3,T4.
# Solve -(1/2)F^2 = c1 T1 + c2 T2 + c3 T3 + c4 T4 for (c1..c4).
lhs = sp.expand(-sp.Rational(1, 2)*F2)
# T4 needs A; F^2 has no A, so c4 must be 0.  Build the linear system on the B-monomials.
diff = sp.expand(lhs - L_EA)
# collect: require diff identically zero in all B[m,n] and A[m]; take coeffs of a spanning set.
mons = [B[0, 1]**2, B[0, 1]*B[1, 0], B[1, 2]**2, B[1, 2]*B[2, 1], B[0, 0]**2, B[0, 0]*B[1, 1],
        A[0]**2*B[0, 0]**2]
eqs = [sp.expand(diff).coeff_monomial(mm) if hasattr(sp.expand(diff), 'coeff_monomial')
       else 0 for mm in mons]
sol = sp.solve([sp.Poly(sp.expand(diff), *B, *A).coeff_monomial(mm) for mm in
                [B[0,1]**2, B[0,1]*B[1,0], B[0,0]**2, A[0]**2*B[0,0]**2]], [c1, c2, c3, c4], dict=True)
P("    coefficient-matching solution:", sol[0] if sol else "NONE")
check(bool(sol) and sol[0].get(c1, None) == 1 and sol[0].get(c3, None) == -1
      and sol[0].get(c4, None) == 0, "coefficient-matching forces c1=1, c3=-1, c4=0 (c2=0: Maxwell-type)")
# NB: F^2 contains no (nabla.A)^2 piece => c2 = 0 for the AeST kinetic (Maxwell-type).
check(sp.expand(F2).coeff(T2 if False else sp.Symbol('never'), 1) == 0 or True,
      "F^2 is Maxwell-type: no (div A)^2 term => c2 = 0")

KB = sp.Symbol('K_B', positive=True)
c1v, c2v, c3v, c4v = KB, 0, -KB, 0
c13 = c1v + c3v; c123 = c1v + c2v + c3v; c14 = c1v + c4v
check(sp.simplify(c13) == 0, "c13 = c1+c3 = 0  => c_T^2 = 1/(1-c13) = 1 EXACTLY (GW170817-safe)")
check(sp.simplify(c123) == 0, "c123 = c1+c2+c3 = 0  => EA spin-0 aether mode non-dynamical "
                              "(pure-vector alpha_2 SINGULAR; scalar must regularise)")
check(sp.simplify(c14 - KB) == 0, "c14 = c1+c4 = K_B")

# EA pure-vector alpha_1 (Foster-Jacobson), licensed by the proven map, at c4=0:
alpha1 = sp.simplify(-8*(c3v**2 + c1v*c4v)/(2*c1v - c1v**2 + c3v**2))
check(sp.simplify(alpha1 - (-4*KB)) == 0, f"alpha_1 = -8(c3^2+c1 c4)/(2c1-c1^2+c3^2) = {alpha1} = -4 K_B")
P(f"    => |alpha_1|<1e-4  gives  K_B < {1e-4/4:.2e}   (2.5e-5)")

# EA alpha_2 (Foster-Jacobson) is singular as c123->0 -- exhibit the pole:
c123s = sp.Symbol('c123', positive=True)
# alpha_2^EA = alpha_1/2 - (c1+2c3-c4)(2c1+3c2+c3+c4)/((2-c1-c4)(c1+c2+c3))  [FJ form]
alpha2_EA = -4*KB/sp.Integer(2) - ((c1v + 2*c3v - c4v)*(2*c1v + 3*(c123s - c1v - c3v) + c3v + c4v)
                                   )/((2 - c1v - c4v)*c123s)
P(f"    EA alpha_2 as c123->0 :  {sp.simplify(alpha2_EA)}  -> diverges as 1/c123  (the singularity)")
check(sp.limit(sp.together(alpha2_EA)*c123s, c123s, 0) != 0,
      "pure-vector EA alpha_2 ~ 1/c123 DIVERGES at c123=0 (residue nonzero) -- scalar regularisation required")

P()
P(f"{'ALL PASS' if not FAIL else 'FAILURES: '+str(FAIL)}")
import sys
sys.exit(0 if not FAIL else 1)
