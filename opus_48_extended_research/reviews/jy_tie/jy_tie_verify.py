#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
jy_tie_verify.py  --  AeST free-function J(Y) <-> Zimmerman framework, BOTH WAYS.

CONTEXT (host, confirmed VERBATIM from arXiv:2507.00912v1, Blanchet-Skordis 2025,
"Khronon-Tensor theory reproducing MOND", Moriond proceedings; HTML full-text fetched):

  Action (Eq.1):  S = (c^3/16 pi G) int d^4x sqrt(-g) [ R - 2 J(Y) + 2 K(Q) ] + S_m
  Free function J(Y), two regimes:
     (Eq.4a)  J = 0                                      for Y >> a0^2/c^4   (Newtonian)
     (Eq.4b)  J = Lambda - Y + (2 c^2/3 a0) Y^{3/2} + O(Y^2)   for Y << a0^2/c^4 (MOND)
  Y = A_mu A^mu / c^4   (Eq.3);  in the quasistatic weak field  Y = |grad phi|^2/c^4 = g^2/c^4.
  Modified Poisson (Eq.13):  div[(1 + J_Y) grad phi] + mu^2 phi = 4 pi G rho + O(c^-2),
     and the paper IDENTIFIES  MU = 1 + J_Y  as the MOND interpolating function
     (acting on the TOTAL acceleration g = |grad phi|).  The mu^2 phi screening
     (K(Q) sector) is negligible in the galactic MOND regime.

  Host coefficient slots:  c_0 = Lambda (Y^0),  c_1 = -1 (Y^1),  c_{3/2} = 2 c^2/(3 a0) (Y^{3/2}),
     O(Y^2) and higher = UNSPECIFIED / FREE (CMB-fit shape).

FRAMEWORK (Zimmerman):
  a0 = c^2 sqrt(Lambda/(32 pi))    [the framework's a0<->Lambda tie; INPUT, not derived here]
  dS-Unruh interpolation (nu-form):  g = sqrt(g_bar^2 + g_bar a0),  i.e. nu(y)=sqrt(1+1/y), y=g_bar/a0.

JOB:
  TIER 1 -- express the a0-Lambda tie as a relation between host coefficients c_0 and c_{3/2}.
            Pin K in  c_{3/2} = K * c_0^{-1/2}.  Clean/distinctive or restatement?
  TIER 2 -- lift g=sqrt(g_bar^2+g_bar a0) to its IMPLIED J(Y) via MU=1+J_Y, Y=g^2/c^4;
            Taylor-expand (deep-MOND small Y and Newtonian large Y); compare coeff-by-coeff
            to the host Lambda - Y + (2c^2/3a0)Y^{3/2} + O(Y^2).

QUARANTINE: a0/Z/kappa NOT asserted derived.  This is a CONSISTENCY/STRUCTURE test:
  the host coefficients (Lambda, a0) are INPUTS; the framework imposes a RELATION (Tier 1)
  and shows its interpolation POPULATES the host's free function (Tier 2).
"""

import sympy as sp

# ----------------------------------------------------------------------
# symbols
# ----------------------------------------------------------------------
c, a0, Lam, G = sp.symbols('c a0 Lambda G', positive=True)
pi = sp.pi
Y  = sp.symbols('Y', positive=True)          # kinetic scalar Y = g^2/c^4
g, gbar = sp.symbols('g g_bar', positive=True)
x      = sp.symbols('x', positive=True)       # x = g/a0   (AQUAL: MU acts on total g)
y      = sp.symbols('y', positive=True)       # y = g_bar/a0 (nu acts on baryonic g_bar)

print("="*78)
print("TIER 1 -- a0<->Lambda tie as a host-coefficient relation  c_{3/2}=K*c_0^{-1/2}")
print("="*78)

# host coefficient of Y^{3/2}, exactly from Eq.4b
c_32_host = 2*c**2/(3*a0)
c_0_host  = Lam                      # Y^0 coefficient (= Lambda)

# framework tie a0 = c^2 sqrt(Lambda/32pi)  -> substitute into c_{3/2}
a0_fw = c**2 * sp.sqrt(Lam/(32*pi))
c_32_fw = sp.simplify(c_32_host.subs(a0, a0_fw))
print("framework a0 = c^2 sqrt(Lambda/32pi) =", a0_fw)
print("=> c_{3/2} = 2c^2/(3 a0) becomes :", c_32_fw)

# write as K * Lambda^{-1/2}; c^2 must cancel for a c-FREE relation
K = sp.simplify(c_32_fw * sp.sqrt(Lam))      # = c_{3/2} * c_0^{1/2}
print("=> K = c_{3/2} * sqrt(c_0)            :", K, "   (c^2 cancels:", 'YES' if c not in K.free_symbols else 'NO', ")")
K_simpl = sp.nsimplify(sp.simplify(K), [sp.sqrt(2), sp.sqrt(sp.pi)])
print("   K simplified                      :", sp.simplify(K))
print("   K =? (2/3)sqrt(32 pi)             :", sp.simplify(K - sp.Rational(2,3)*sp.sqrt(32*pi)) == 0)
Kval = float(K.evalf())
print("   K numeric                         :", Kval)

# Z-language:  Z = sqrt(32 pi/3);  claim N=(2/3)sqrt(32pi)=2Z/sqrt(3)
Z = sp.sqrt(32*pi/3)
print("   Z = sqrt(32 pi/3)                 :", float(Z.evalf()))
print("   K =? 2 Z / sqrt(3)                :", sp.simplify(K - 2*Z/sp.sqrt(3)) == 0,
      "  (2Z/sqrt3 =", float((2*Z/sp.sqrt(3)).evalf()), ")")

# sanity: plug numbers Lambda, c -> recover a0 = 9.36e-11 ?
c_num   = 2.99792458e8
Lam_num = 1.1056e-52        # m^-2, Planck-ish Lambda (only a sanity check of the tie)
a0_num  = float(a0_fw.subs({c:c_num, Lam:Lam_num}))
print("   sanity a0(Lambda) [m/s^2]         :", a0_num, " (target ~9.36e-11)")

print()
print("TIER 1 verdict: c_{3/2} = K * c_0^{-1/2}, K = (2/3)sqrt(32 pi) ~ 6.6843, c-FREE.")
print("   The host leaves c_0=Lambda and c_{3/2}=2c^2/3a0 INDEPENDENT; the framework ties")
print("   them by ONE host-free equation.  HONEST: this RE-EXPRESSES a0=c^2 sqrt(Lambda/32pi)")
print("   in J-coefficient language -- it pins the exact number but RESTATES the coincidence.")

# ----------------------------------------------------------------------
print()
print("="*78)
print("DICTIONARY check (host J(Y) -> MU=1+J_Y -> deep-MOND limit)")
print("="*78)
# host J(Y) keeping through Y^{3/2}
J_host = Lam - Y + (2*c**2/(3*a0))*Y**sp.Rational(3,2)
JY_host = sp.diff(J_host, Y)
MU_host = sp.simplify(1 + JY_host)           # = (c^2/a0) sqrt(Y)
print("host J(Y)            :", J_host)
print("host J_Y = dJ/dY     :", sp.simplify(JY_host))
print("host MU = 1 + J_Y    :", MU_host)
# with Y = g^2/c^4 -> MU = g/a0  (deep-MOND interpolation)
MU_host_g = sp.simplify(MU_host.subs(Y, g**2/c**4))
print("host MU (Y=g^2/c^4)  :", MU_host_g, "  == g/a0 :", sp.simplify(MU_host_g - g/a0)==0)

# ----------------------------------------------------------------------
print()
print("="*78)
print("TIER 2 -- lift framework g=sqrt(g_bar^2+g_bar a0) to its IMPLIED J(Y)")
print("="*78)

# (i) invert nu-form to get g_bar(g):  g^2 = g_bar^2 + g_bar a0
gbar_sol = sp.solve(sp.Eq(g**2, gbar**2 + gbar*a0), gbar)
gbar_phys = [s for s in gbar_sol if sp.simplify(s.subs(g, a0)) > 0 or True]
# pick the positive root
gbar_of_g = [s for s in gbar_sol if sp.simplify((s.subs({a0:1,g:1})).evalf()) > 0][0]
gbar_of_g = sp.simplify(gbar_of_g)
print("g_bar(g) (physical root):", gbar_of_g)

# (ii) AQUAL interpolation MU_fw(g) = g_bar/g  (MU multiplies grad phi; MU*g = g_bar)
MU_fw = sp.simplify(gbar_of_g/g)
print("MU_fw(g) = g_bar/g      :", MU_fw)
MU_fw_x = sp.simplify(MU_fw.subs({g: x*a0}))   # x=g/a0
print("MU_fw(x), x=g/a0        :", MU_fw_x, "  (=(sqrt(4x^2+1)-1)/(2x))")
print("  limit x->oo (Newton)  :", sp.limit(MU_fw_x, x, sp.oo))
print("  limit x->0  (deepMOND):", sp.simplify(sp.series(MU_fw_x, x, 0, 2).removeO()), " ~ x = g/a0  OK")

# (iii) J_Y = MU_fw - 1, as a function of Y via g = c^2 sqrt(Y)
g_of_Y = c**2*sp.sqrt(Y)
JY_fw = sp.simplify(MU_fw.subs(g, g_of_Y) - 1)
print("J_Y,fw(Y) = MU_fw-1     :", JY_fw)

# (iv) integrate J_Y dY to get J_fw(Y) (closed form, + free constant C0)
C0 = sp.symbols('C0')
J_fw_closed = sp.simplify(sp.integrate(JY_fw, Y)) + C0
print("J_fw(Y) closed form     :")
sp.pprint(J_fw_closed)

# ----------------------------------------------------------------------
print()
print("-"*78)
print("TIER 2(a)+(b) -- DEEP-MOND Taylor expansion of J_fw(Y) about Y=0, compare host")
print("-"*78)

# Expand J_Y,fw in small Y, then integrate term-by-term to get J_fw small-Y series.
# (integrate the series is cleaner / avoids asinh branch bookkeeping)
NORD = 6   # number of half-integer terms to show
JY_series = sp.series(JY_fw, Y, 0, NORD).removeO()
JY_series = sp.expand(JY_series)
print("J_Y,fw small-Y series   :")
sp.pprint(JY_series)

# integrate term-by-term (add C0 for the Y^0 slot of J)
J_fw_series = sp.integrate(JY_series, Y) + C0
J_fw_series = sp.expand(J_fw_series)
print()
print("J_fw(Y) small-Y series  :")
sp.pprint(J_fw_series)

# collect coefficients of Y^{n/2}.  Substitute Y = t^2 so half-powers become
# integer powers of t (sympy .coeff needs integer exponents); coeff of Y^{n/2} = coeff of t^n.
t = sp.symbols('t', positive=True)
J_fw_t = sp.expand(J_fw_series.subs(Y, t**2))
print()
print("Coefficient-by-coefficient (framework implied vs host):")
powers = [sp.Rational(0,1), sp.Rational(1,2), sp.Rational(1,1),
          sp.Rational(3,2), sp.Rational(2,1), sp.Rational(5,2),
          sp.Rational(3,1), sp.Rational(7,2), sp.Rational(9,2)]
host_coeffs = {
    sp.Rational(0,1): Lam,                 # = C0 slot (framework's free constant <-> host Lambda)
    sp.Rational(1,2): sp.Integer(0),
    sp.Rational(1,1): sp.Integer(-1),
    sp.Rational(3,2): 2*c**2/(3*a0),
    # Y^2 and higher: host UNSPECIFIED/FREE
}
def coeffY(expr_t, p):
    """coefficient of Y^p where p may be half-integer, via Y=t^2 -> t^(2p)."""
    n = int(2*p)
    return sp.simplify(expr_t.coeff(t, n))
# expression with C0 replaced so Y^0 coefficient is C0
table = []
for p in powers:
    coeff = coeffY(J_fw_t, p)
    hc = host_coeffs.get(p, None)
    if p == 0:
        fw_str = "C0  (free constant slot)"
        host_str = "Lambda"
        verdict = "MATCH (C0 := Lambda)"
    elif hc is not None:
        match = sp.simplify(coeff - hc) == 0
        fw_str = str(coeff)
        host_str = str(hc)
        verdict = "MATCH" if match else "DIVERGE"
    else:
        fw_str = str(coeff)
        host_str = "FREE (unspecified, O(Y^2) CMB-fit)"
        verdict = "host-FREE (framework PREDICTS this slot)"
    table.append((p, fw_str, host_str, verdict))
    print(f"  Y^{str(p):4s}: fw = {fw_str:28s} | host = {host_str:28s} | {verdict}")

# explicit closed coefficients of the first few framework half-integer terms
print()
print("Framework's predicted higher-order coefficients (exact):")
for p in [sp.Rational(3,2), sp.Rational(5,2), sp.Rational(7,2), sp.Rational(9,2)]:
    print(f"  c_{{{p}}} = ", coeffY(J_fw_t, p))
print("  c_2 (integer Y^2) =", coeffY(J_fw_t, sp.Integer(2)), " (framework predicts ZERO integer-2 term)")

# ----------------------------------------------------------------------
print()
print("-"*78)
print("TIER 2 -- NEWTONIAN (large Y) limit of the framework's J(Y)")
print("-"*78)
# large Y: substitute Y = 1/u, expand about u->0
u = sp.symbols('u', positive=True)
JY_large = sp.simplify(JY_fw.subs(Y, 1/u))
ser_large = sp.series(JY_large, u, 0, 4).removeO()
print("J_Y,fw as Y->oo (u=1/Y->0):")
sp.pprint(sp.simplify(ser_large))
print("  => J_Y -> 0  as Y->oo, so MU=1+J_Y -> 1 (Newtonian).  Host Eq.4a sets J=0 for Y>>a0^2/c^4;")
print("     framework gives J_Y->0 (MU->1) i.e. J->const (Newtonian gravity). Consistent in LIMIT;")
print("     host's exact 'J=0' high-Y branch is a host choice (framework's J asymptotes to a const).")

# ----------------------------------------------------------------------
print()
print("="*78)
print("SUMMARY")
print("="*78)
print("TIER 1: c_{3/2} = (2/3)sqrt(32 pi) * c_0^{-1/2}, c-free, K=%.4f. RESTATES a0=c^2 sqrt(L/32pi)." % Kval)
print("TIER 2: framework's interpolation reproduces host -Y and (2c^2/3a0)Y^{3/2} EXACTLY;")
print("        predicts Y^{1/2}=0, integer Y^2=0, and a specific Y^{5/2}, Y^{7/2}, ... tail;")
print("        host's O(Y^2) is FREE => MATCH (no tension), a host-FREE strengthening above cubic.")
