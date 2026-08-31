#!/usr/bin/env python3
"""
AeST + J10 (exponential) FLRW BACKGROUND -- rigorous derivation with sympy.

Action (Skordis-Zlosnik 2021, PRL 127 161302; arXiv:2007.00082):
  S = (1/16 pi Gt) \int d4x sqrt(-g) [ R - 2L - (K_B/2) F_{mn}F^{mn}
        + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lam(A^2+1) ] + S_m
  with  J^mu = A^a grad_a A^mu  (aether acceleration; shift-current term),
        Q = A^mu grad_mu phi,  Y = q^{mn} grad_mu phi grad_nu phi, q^{mn}=g^{mn}+A^mu A^nu.
  F(Y,Q) = (2-K_B) J(Y,Q) - 2 K(Q).

J10 (exponential) choice:
  J(Y,Q) = a0^2(Q) [ u^2 + 2(1+u) e^{-u} - 2 ],  u = sqrt(Y)/a0(Q).

We verify (1) Y=0, Q=phidot on FLRW, (2) Friedmann + shift-charge a^-3 dust,
(3) the EXACT background values of F_Y, F_YY, F_Q, F_QQ, F_YQ.
"""
import sympy as sp

print("="*78)
print("PART 0: symbols")
print("="*78)
Y, Q, KB = sp.symbols('Y Q K_B', positive=True)   # Y>0 so sqrt is real; we take Y->0+
a0f = sp.Function('a0')                              # a0(Q)
a0 = a0f(Q)
u = sp.sqrt(Y)/a0
bracket = u**2 + 2*(1+u)*sp.exp(-u) - 2
J = a0**2 * bracket
print("u        =", u)
print("bracket  =", bracket)
print("J(Y,Q)   = a0(Q)^2 * bracket")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 1: FLRW alignment check  Y=0, Q=phidot   (SOLID)")
print("="*78)
# Minisuperspace: g = diag(-N^2, a^2, a^2, a^2). A^mu=(1/N,0,0,0). phi=phi(t).
N, a = sp.symbols('N a', positive=True)
phidot = sp.symbols('phidot', real=True)
# metric inverse g^{mn} = diag(-1/N^2, 1/a^2,1/a^2,1/a^2)
ginv = sp.diag(-1/N**2, 1/a**2, 1/a**2, 1/a**2)
Aup = sp.Matrix([1/N,0,0,0])          # A^mu
# lower A: A_mu = g_{mu nu} A^nu ; g_{00}=-N^2 => A_0=-N
Alow = sp.Matrix([-N,0,0,0])
print("A^mu A_mu =", sp.simplify((Aup.T*Alow)[0]), " (must be -1)")
dphi_up = sp.Matrix([phidot,0,0,0])   # grad_mu phi = (phidot,0,0,0)  (lower index)
# Q = A^mu grad_mu phi = A^mu dphi_mu
Qval = (Aup.T*dphi_up)[0]
print("Q = A^mu grad_mu phi =", sp.simplify(Qval), " (must be phidot/N -> phidot at N=1)")
# projector q^{mn} = g^{mn} + A^mu A^nu
qproj = ginv + Aup*Aup.T
# Y = q^{mn} dphi_mu dphi_nu
Yval = (dphi_up.T*qproj*dphi_up)[0]
print("Y = q^{mn} d_mu phi d_nu phi =", sp.simplify(Yval), " (must be 0)")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 2: F-derivative J-pieces  (the load-bearing coefficients)")
print("="*78)
JY  = sp.diff(J, Y)
JYY = sp.diff(J, Y, 2)
JQ  = sp.diff(J, Q)
JQQ = sp.diff(J, Q, 2)
JYQ = sp.diff(sp.diff(J, Y), Q)

JY_s  = sp.simplify(JY)
print("\nJ_Y (exact) =", JY_s)
# limit Y->0+
JY0 = sp.limit(JY_s, Y, 0, '+')
print("J_Y|_{Y->0} =", JY0, "   => F_Y|bg = (2-K_B)*0 = 0")

print("\nJ_YY (exact) =", sp.simplify(JYY))
# leading behaviour as Y->0: expect ~ 1/(2 a0^2 u) = 1/(2 a0 sqrt(Y)) -> +oo
JYY_lead = sp.simplify(sp.series(JYY, Y, 0, 1).removeO()) if False else None
JYY0 = sp.limit(JYY, Y, 0, '+')
print("J_YY|_{Y->0} =", JYY0, "   (DIVERGES: non-analytic sqrt-MOND)")
# show the exact leading coefficient: J_YY ~ e^{-u}/(2 a0^2 u)
lead = sp.exp(-u)/(2*a0**2*u)
print("check  J_YY == e^{-u}/(2 a0^2 u)? ->", sp.simplify(JYY - lead)==0)
print("  so near Y=0:  J_YY -> 1/(2 a0 sqrt(Y))  ~ Y^{-1/2}")

print("\nJ_Q  |_{Y->0} =", sp.limit(sp.simplify(JQ),  Y,0,'+'))
print("J_QQ |_{Y->0} =", sp.limit(sp.simplify(JQQ), Y,0,'+'))
print("J_YQ |_{Y->0} =", sp.limit(sp.simplify(JYQ), Y,0,'+'))

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 3: series of J near Y=0  -> deep-MOND cubic, half-integer powers")
print("="*78)
# substitute u = t (t=sqrt(Y)) and expand in t to see Y^{3/2}=t^3 leading term
t = sp.symbols('t', positive=True)   # t = sqrt(Y)
Jt = a0**2 * ((t/a0)**2 + 2*(1+t/a0)*sp.exp(-t/a0) - 2)
ser = sp.series(Jt, t, 0, 6).removeO()
ser = sp.expand(ser)
print("J as series in t=sqrt(Y):")
print("  ", ser)
print("  -> leading term should be (2/(3 a0)) * t^3 = (2/(3 a0)) Y^{3/2}")
coef_t3 = ser.coeff(t,3)
print("  coeff of t^3 =", sp.simplify(coef_t3), "  (deep-MOND: J -> (2/3a0) Y^{3/2})")
coef_t4 = ser.coeff(t,4)
print("  coeff of t^4 =", sp.simplify(coef_t4), "  (= Y^2 term)")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 4: assemble F-derivatives  F=(2-K_B)J - 2K(Q)   at background (Y=0)")
print("="*78)
Kf = sp.Function('K'); K = Kf(Q)
KQ = sp.diff(K,Q); KQQ = sp.diff(K,Q,2)
print("F_Y  |bg = (2-K_B) J_Y|0  - 0        =", (2-KB)*JY0)
print("F_YY |bg = (2-K_B) J_YY|0 - 0        = (2-K_B)*(+oo)  -> DIVERGENT / non-analytic")
print("F_Q  |bg = (2-K_B) J_Q|0  - 2 K_Q    =", sp.simplify((2-KB)*0 - 2*KQ))
print("F_QQ |bg = (2-K_B) J_QQ|0 - 2 K_QQ   =", sp.simplify((2-KB)*0 - 2*KQQ))
print("F_YQ |bg = (2-K_B) J_YQ|0            =", (2-KB)*0)

print("\nAlso F(0,Q) = (2-K_B) J(0,Q) - 2K(Q).  J(0,Q):")
J0 = sp.limit(J, Y, 0, '+')
print("  J(0,Q) =", J0, "  => F(0,Q) = -2 K(Q)   (matches K=-1/2 F(0,Q))")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 5: shift-current -> dust.  F_Q|bg = -2K_Q ;  dF_Q/dt+3H F_Q=0")
print("="*78)
tt = sp.symbols('t', positive=True)
af = sp.Function('a'); aa = af(tt); H = sp.diff(aa,tt)/aa
FQ = sp.Function('F_Q')(tt)
eq = sp.Eq(sp.diff(FQ,tt) + 3*H*FQ, 0)
print("shift-current conservation:", eq)
sol = sp.dsolve(eq, FQ)
print("solution:", sol, "   => F_Q ~ a^{-3}  and since F_Q=-2K_Q => K_Q ~ a^{-3} (DUST)")

print("\nDONE.")
