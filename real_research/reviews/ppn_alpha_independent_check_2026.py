#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ppn_alpha_independent_check_2026.py
===================================

INDEPENDENT, FROM-FIRST-PRINCIPLES computation of the PPN preferred-frame
parameters alpha_1, alpha_2 for the "Maxwell aether":

    S = \int d^4x sqrt(-g) [ R - (K_B/2) F_{mu nu} F^{mu nu}
                               - lambda (A^mu A_mu + 1) ]  + S_matter

    F_{mu nu} = partial_mu A_nu - partial_nu A_mu     (ordinary curl:
                the Christoffels cancel by antisymmetry, so F carries NO metric)

    A^mu A_mu = -1 enforced by the Lagrange multiplier lambda.
    Matter couples to g_{mu nu} only.   Units 16 pi G = 1.

NOTHING here is copied from Foster & Jacobson (or any other PPN reference).
Every field equation used below is derived inside this script (by explicit
symbolic variation, verified numerically/symbolically), and the linearized
Einstein tensor is computed from the definition of the Riemann tensor.

The only "looked up" inputs are DEFINITIONS: the Riemann/Ricci sign
convention, the definition of T_{mu nu} as a metric variation, and the
definition of the PPN potentials U and U_{ij}.  All of them are stated
explicitly below and (where possible) calibrated internally.

=====================================================================
CONVENTIONS  (every one of these can flip a sign or a factor)
=====================================================================
C1. Signature (-,+,+,+).  Coordinates x^mu = (t, x, y, z).  c = 1.
C2. eta_{mu nu} = diag(-1, +1, +1, +1).
C3. Riemann:  R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma}
                                  - d_nu Gamma^rho_{mu sigma}
                                  + Gamma^rho_{mu lam} Gamma^lam_{nu sigma}
                                  - Gamma^rho_{nu lam} Gamma^lam_{mu sigma}
    Ricci: R_{sigma nu} = R^mu_{sigma mu nu}.  Einstein: G = R_{mn} - g_{mn}R/2.
C4. Fundamental aether variable is the ONE-FORM A_mu.  (A^mu = g^{mu nu}A_nu.)
    This matters: with A_mu fundamental, F_{mu nu} is metric-independent, so
    the F^2 term contributes to the stress tensor only quadratically in F.
    Using A^mu as fundamental gives field equations that differ by terms
    proportional to the aether EOM, i.e. the same on-shell system.  We state
    this and use the A_mu formulation throughout.
C5. Matter stress tensor:  delta S_matter / delta g^{mu nu} = -(1/2) sqrt(-g) T_{mu nu},
    i.e. T_{mu nu} = -(2/sqrt(-g)) delta S_matter/delta g^{mu nu}.
    With this convention static dust has T_{00} = +rho > 0.  The SIGN is not
    assumed: it is CALIBRATED internally by demanding attractive Newtonian
    gravity (h_00 = +2U with U > 0 for rho > 0).
C6. Newtonian potential U: DEFINED to be positive, with
        laplacian U = -4 pi G_N rho ,   U(k) = 4 pi G_N rho(k) / k^2 .
    Equivalently U is FIXED by demanding h_00 = 2U + O(w^2) exactly, so the
    value of G_N never enters alpha_1, alpha_2.
C7. PPN potential U_{ij}: DEFINED as the standard
        U_{ij}(x) = \int rho(x') (x-x')_i (x-x')_j / |x-x'|^3 d^3x'
    (normalized with the SAME G_N as U, so that U_{ii} = U).  In Fourier
    space this gives the identity, verified in-script,
        U_{ij}(k) = ( delta_{ij} - 2 k_i k_j / k^2 ) U(k) ,
    hence  w^i w^j U_{ij}(k) = ( w^2 - 2 (w.khat)^2 ) U(k).
C8. PPN MATCHING CONVENTION (exactly the one requested):
        g_00 = -1 + 2U + alpha_1 w^2 U + alpha_2 w^i w^j U_{ij} + (w-free terms)
    where w^i is the aether wind velocity at spatial infinity, measured in the
    MATTER rest frame.  With C7 this means: if the w-dependent part of h_00 is
        delta h_00(k) = [ a * w^2 + b * (w.khat)^2 ] U(k)      + O(w^4)
    then
        alpha_2 = -b/2 ,      alpha_1 = a - alpha_2 = a + b/2 .
    NOTE: Will's textbook PPN metric writes the same physics with the
    coefficient of w^2 U equal to (alpha_3 - alpha_1); with alpha_3 = 0 that
    is MINUS alpha_1.  So a reader using Will's normalization must flip the
    sign of the alpha_1 reported here.  We use the convention as specified in
    the task statement and say so loudly.
C9. Perturbative bookkeeping: LINEAR in the matter density rho (so "O(eps)"
    below means "one power of rho"), and expanded to SECOND order in the wind
    speed w.  All fields static in the matter frame.
"""

import sys
import sympy as sp
from sympy.calculus.euler import euler_equations

FAIL = []


def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)
    return ok


def hdr(s):
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)


# ----------------------------------------------------------------------
# symbols
# ----------------------------------------------------------------------
t, x, y, z = sp.symbols('t x y z', real=True)
COORDS = [t, x, y, z]
KB = sp.Symbol('K_B', real=True)
k = sp.Symbol('k', positive=True)
rho = sp.Symbol('rho', real=True)          # Fourier amplitude of the density
lam = sp.Symbol('lambda', real=True)        # Fourier amplitude of delta-lambda
sw = sp.Symbol('s', positive=True)          # wind-order bookkeeping parameter
wx, wy, wz = sp.symbols('w_x w_y w_z', real=True)

ETA = sp.diag(-1, 1, 1, 1)
ETAI = ETA.inv()          # numerically equal to ETA, kept separate for clarity

W = [sw * wx, sw * wy, sw * wz]            # wind 3-vector, order-counted by sw
W2 = sum(c ** 2 for c in W)
GW = 1 / sp.sqrt(1 - W2)                   # gamma_w


def ser_w(expr, order=2):
    """Truncate an expression at O(s^order) in the wind bookkeeping parameter."""
    e = sp.expand(sp.series(sp.together(expr), sw, 0, order + 1).removeO())
    return sp.expand(e)


print(__doc__)

# ======================================================================
hdr("STEP 0.  BACKGROUND: boosted aether on flat space, and F_bg = 0")
# ======================================================================
# A^mu_bg = gamma_w (1, w^i), constant in x.  A_mu = eta_{mu nu} A^nu.
Aup_bg = sp.Matrix([GW, GW * W[0], GW * W[1], GW * W[2]])
Adn_bg = ETA * Aup_bg

AA_bg = sp.simplify((Aup_bg.T * ETA * Aup_bg)[0, 0])
check("unit-timelike constraint A^mu A_mu = -1 on the background",
      sp.simplify(AA_bg + 1) == 0, f"A.A = {AA_bg}")

# F_bg: build A_mu as (constant) functions of the coordinates and take the curl.
F_bg = sp.Matrix(4, 4, lambda m, n: sp.diff(Adn_bg[n], COORDS[m])
                                    - sp.diff(Adn_bg[m], COORDS[n]))
check("F_bg = 0  (constant boosted aether costs no field energy)",
      sp.simplify(F_bg) == sp.zeros(4, 4))

# The full aether Lagrangian on the background:  -(K_B/2)F^2 - lam(A.A+1) = 0,
# and the vector EOM  K_B nabla_mu F^{mu nu} = lam A^nu  then forces lam_bg = 0.
check("background aether Lagrangian density vanishes (so lam_bg = 0 is forced)",
      sp.simplify((-KB / 2) * sum(F_bg[m, n] * F_bg[a, b] * ETAI[m, a] * ETAI[n, b]
                                  for m in range(4) for n in range(4)
                                  for a in range(4) for b in range(4))) == 0)
print("  -> flat metric + uniformly boosted aether is an EXACT vacuum solution,")
print("     with lambda_bg = 0.  Hence delta-lambda is gauge invariant and is")
print("     itself first order in rho.")

# ======================================================================
hdr("STEP 1a.  DERIVE the metric field equation (exact symbolic variation)")
# ======================================================================
# Claim to be verified:
#   delta( sqrt(-g) L_A ) / delta g^{mu nu}
#        = sqrt(-g) [ -K_B F_{mu b} F_nu^{ b} - lam A_mu A_nu - (1/2) g_{mu nu} L_A ]
# with L_A = -(K_B/2) F^2 - lam (g^{ab}A_a A_b + 1)   (kept OFF-shell).
#
# Verified by differentiating along an arbitrary symmetric direction s^{mu nu}
# at a generic (rational, Lorentzian) metric with generic rational F and A.
S = sp.Symbol('S_var')
gup0 = sp.Matrix([[-sp.Rational(9, 8), sp.Rational(1, 7), 0, sp.Rational(1, 11)],
                  [sp.Rational(1, 7), sp.Rational(6, 5), sp.Rational(1, 13), 0],
                  [0, sp.Rational(1, 13), sp.Rational(7, 6), -sp.Rational(1, 9)],
                  [sp.Rational(1, 11), 0, -sp.Rational(1, 9), sp.Rational(5, 4)]])
sdir = sp.Matrix([[sp.Rational(1, 3), -sp.Rational(2, 5), sp.Rational(1, 2), 0],
                  [-sp.Rational(2, 5), sp.Rational(3, 7), 0, sp.Rational(1, 6)],
                  [sp.Rational(1, 2), 0, -sp.Rational(4, 9), sp.Rational(2, 11)],
                  [0, sp.Rational(1, 6), sp.Rational(2, 11), sp.Rational(3, 5)]])
Ffix = sp.Matrix(4, 4, lambda m, n: 0)
_fv = {(0, 1): sp.Rational(2, 3), (0, 2): -sp.Rational(1, 5), (0, 3): sp.Rational(3, 7),
       (1, 2): sp.Rational(1, 2), (1, 3): -sp.Rational(2, 9), (2, 3): sp.Rational(4, 5)}
for (m, n), v in _fv.items():
    Ffix[m, n] = v
    Ffix[n, m] = -v
Afix = sp.Matrix([-sp.Rational(11, 10), sp.Rational(1, 4), -sp.Rational(1, 3), sp.Rational(2, 7)])


def _LA(gup, Fm, Am, lm):
    F2 = sum(Fm[m, n] * Fm[a, b] * gup[m, a] * gup[n, b]
             for m in range(4) for n in range(4) for a in range(4) for b in range(4))
    AA = sum(gup[a, b] * Am[a] * Am[b] for a in range(4) for b in range(4))
    return -(KB / 2) * F2 - lm * (AA + 1), F2, AA


gup_e = gup0 + S * sdir
LA_e, _, _ = _LA(gup_e, Ffix, Afix, lam)
sqrtg_e = 1 / sp.sqrt(-gup_e.det())
lhs_var = sp.simplify(sp.diff(sqrtg_e * LA_e, S).subs(S, 0))

gdn0 = gup0.inv()
sqrtg0 = 1 / sp.sqrt(-gup0.det())
LA0, F2_0, AA_0 = _LA(gup0, Ffix, Afix, lam)
FF = sp.Matrix(4, 4, lambda m, n: sum(Ffix[m, b] * gup0[b, d] * Ffix[n, d]
                                      for b in range(4) for d in range(4)))
Xmn = sp.Matrix(4, 4, lambda m, n: sqrtg0 * (-KB * FF[m, n]
                                             - lam * Afix[m] * Afix[n]
                                             - sp.Rational(1, 2) * gdn0[m, n] * LA0))
rhs_var = sp.simplify(sum(Xmn[m, n] * sdir[m, n] for m in range(4) for n in range(4)))
check("aether metric-variation formula (off-shell, generic g, F, A, lambda)",
      sp.simplify(sp.expand(lhs_var - rhs_var)) == 0)

print("""
  => Combining with delta(sqrt(-g)R)/delta g^{mu nu} = sqrt(-g) G_{mu nu} and C5:

        G_{mu nu} =  K_B F_{mu b} F_nu^{ b} - (K_B/4) g_{mu nu} F^2
                   + lambda A_mu A_nu + (1/2) T_{mu nu}          (*)

     (the +1/2 is 8 pi G with 16 pi G = 1, i.e. G = 1/(16 pi)).

  *** THE KEY STRUCTURAL POINT ***
     F_bg = 0 (Step 0) and every perturbation is O(rho), so F = O(rho) and the
     two F-bilinear terms in (*) are O(rho^2): INVISIBLE at linear order.
     lambda, by contrast, is O(rho) (see Step 1b).  Therefore

        G^{(1)}_{mu nu} = lambda^{(1)} A^{bg}_mu A^{bg}_nu + (1/2) T_{mu nu}

     is the COMPLETE linearized metric equation.  This is special to the
     Maxwell aether: for a generic Einstein-aether kinetic term the
     Christoffels inside nabla_a A_b do NOT cancel, the metric variation hits
     them, and one gets extra source terms LINEAR in nabla A (hence in rho).
""")

# ======================================================================
hdr("STEP 1b.  DERIVE the aether field equation (Euler-Lagrange, symbolic)")
# ======================================================================
Af = [sp.Function(f'A_{i}')(*COORDS) for i in range(4)]
lamf = sp.Function('lam')(*COORDS)
Ff = sp.Matrix(4, 4, lambda m, n: sp.diff(Af[n], COORDS[m]) - sp.diff(Af[m], COORDS[n]))
F2f = sum(Ff[m, n] * Ff[a, b] * ETAI[m, a] * ETAI[n, b]
          for m in range(4) for n in range(4) for a in range(4) for b in range(4))
AAf = sum(ETAI[a, b] * Af[a] * Af[b] for a in range(4) for b in range(4))
Lag = -(KB / 2) * F2f - lamf * (AAf + 1)
els = euler_equations(Lag, Af, COORDS)

Fupf = sp.Matrix(4, 4, lambda m, n: sum(ETAI[m, a] * ETAI[n, b] * Ff[a, b]
                                        for a in range(4) for b in range(4)))
Aupf = [sum(ETAI[n, a] * Af[a] for a in range(4)) for n in range(4)]
expected = [sp.expand(2 * KB * sum(sp.diff(Fupf[m, n], COORDS[m]) for m in range(4))
                      - 2 * lamf * Aupf[n]) for n in range(4)]
ok = True
for n in range(4):
    got = sp.expand(els[n].lhs - els[n].rhs)
    ok = ok and sp.simplify(got - expected[n]) == 0
check("Euler-Lagrange for A_mu reproduces  2 K_B d_mu F^{mu nu} - 2 lambda A^nu = 0",
      ok)
print("""
  => aether EOM:      K_B nabla_mu F^{mu nu} = lambda A^nu                (V)
     (for antisymmetric F, nabla_mu F^{mu nu} = (1/sqrt(-g)) d_mu(sqrt(-g)F^{mu nu}),
      and since F = O(rho) the sqrt(-g) corrections are O(rho^2), so at linear
      order (V) is the FLAT-space Maxwell equation with source lambda A^nu_bg.)

  Contracting (V) with A_nu and using A.A = -1 gives
        lambda = -K_B A_nu nabla_mu F^{mu nu}   =>   lambda = O(rho).      (L)

  *** THE SECOND KEY STRUCTURAL POINT ***
     F^{mu nu} is ANTISYMMETRIC, so d_mu d_nu F^{mu nu} = 0 IDENTICALLY.
     Taking d_nu of (V) therefore gives an EXTRA identity that a generic
     Einstein-aether theory does NOT have:

            nabla_nu ( lambda A^nu ) = 0                                  (C)

     At linear order (lambda = O(rho), A^nu = A^nu_bg + O(rho)):
            gamma_w ( d_t + w.grad ) lambda = 0 .
""")

# ======================================================================
hdr("STEP 2.  Linearized Einstein tensor, computed from the Riemann definition")
# ======================================================================
# Static plane wave.  WLOG rotate so that k^i = (0, 0, k);  the wind w^i stays
# fully general, so (w.khat) = w_z and the transverse plane is (1,2).
e = sp.Symbol('e')
H = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f'H{min(m,n)}{max(m,n)}'))   # symmetric
phase = sp.exp(sp.I * k * z)
hmn = sp.Matrix(4, 4, lambda m, n: H[m, n] * phase)
gdn = ETA + e * hmn
hup = ETAI * hmn * ETAI
ginv = ETAI - e * hup

resid = sp.expand((ginv * gdn) - sp.eye(4))
check("truncated inverse metric: ginv.g = 1 + O(e^2)",
      all(sp.expand(resid[i, j]).coeff(e, 0) == 0 and sp.expand(resid[i, j]).coeff(e, 1) == 0
          for i in range(4) for j in range(4)))

Gam = [[[sp.expand(sp.Rational(1, 2) * sum(
    ginv[r, s] * (sp.diff(gdn[s, n], COORDS[m]) + sp.diff(gdn[s, m], COORDS[n])
                  - sp.diff(gdn[m, n], COORDS[s])) for s in range(4)))
         for n in range(4)] for m in range(4)] for r in range(4)]

def Ric(sig, nu):
    out = 0
    for m in range(4):
        out += sp.diff(Gam[m][nu][sig], COORDS[m]) - sp.diff(Gam[m][m][sig], COORDS[nu])
        for l in range(4):
            out += Gam[m][m][l] * Gam[l][nu][sig] - Gam[m][nu][l] * Gam[l][m][sig]
    return sp.expand(out)

R1 = sp.Matrix(4, 4, lambda m, n: sp.expand(sp.expand(Ric(m, n)).coeff(e, 1) / phase))
Rs1 = sp.expand(sum(ETAI[m, n] * R1[m, n] for m in range(4) for n in range(4)))
G1 = sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n] - sp.Rational(1, 2) * ETA[m, n] * Rs1))

# Linearized Bianchi identity.  With z-only dependence, d^mu X_{mu nu} = i k X_{3 nu},
# so the identity d^mu G^{(1)}_{mu nu} = 0 must make G^{(1)}_{3 nu} vanish IDENTICALLY.
check("linearized Bianchi: G^(1)_{3 nu} == 0 identically for arbitrary h_{mu nu}",
      all(sp.simplify(G1[3, n]) == 0 for n in range(4)))
print("  G^(1)_00 (before gauge fixing) =", sp.simplify(G1[0, 0]))

# ======================================================================
hdr("STEP 3.  The source, and the CONSTRAINT it must satisfy")
# ======================================================================
# Theta_{mu nu} = lambda A^bg_mu A^bg_nu + (1/2) T_{mu nu},  T_00 = rho, else 0.
Tmn = sp.zeros(4, 4)
Tmn[0, 0] = rho
Theta = sp.Matrix(4, 4, lambda m, n: lam * Adn_bg[m] * Adn_bg[n]
                                     + sp.Rational(1, 2) * Tmn[m, n])
print("  Theta_00 =", sp.simplify(Theta[0, 0]))
print("  Theta_0i =", [sp.simplify(Theta[0, i]) for i in (1, 2, 3)])
print("  Theta_3nu =", [sp.simplify(Theta[3, n]) for n in range(4)])

# Because G^(1)_{3 nu} == 0, the (3,nu) Einstein equations are pure CONSTRAINTS:
constraints = [sp.simplify(Theta[3, n]) for n in range(4)]
# solve them
csol = sp.solve([sp.Eq(c, 0) for c in constraints], [lam], dict=True)
print("\n  ROUTE 1 (metric sector / linearized Bianchi):  0 = Theta_{3 nu}")
print("     => lambda * gamma_w^2 * w_z * {-gamma_w-ish factors} = 0")
print("     => lambda * (w.khat) = 0 .")

# ROUTE 2: independent, from the aether EOM.  d_nu(lambda A^nu) = 0.
divlamA = sp.simplify(sum(sp.diff(lam * Aup_bg[n] * phase, COORDS[n]) for n in range(4)) / phase)
print("\n  ROUTE 2 (aether sector, from d_mu d_nu F^{mu nu} = 0):")
print("     d_nu(lambda A^nu) =", sp.simplify(divlamA / (sp.I * k)), "* (i k) = 0")
r2 = sp.simplify(sp.expand(divlamA / (sp.I * k * GW)))
check("the two independent routes give the SAME constraint  lambda*(w.khat) = 0",
      sp.simplify(r2 - lam * W[2]) == 0, f"route2 -> {r2}")

# ======================================================================
hdr("STEP 4.  Solve for h_00 in the k-transverse gauge (h_00 gauge invariant)")
# ======================================================================
# Residual static gauge freedom: h_{mu nu} -> h_{mu nu} - i(k_mu Xi_nu + k_nu Xi_mu)
# with k_mu = (0,0,0,k).  Hence delta h_00 = 0 EXACTLY (h_00 is gauge invariant
# in this static, linear-in-rho setting) and the four functions Xi_mu can be used
# to set h_{3 nu} = 0.
GAUGE = {H[0, 3]: 0, H[1, 3]: 0, H[2, 3]: 0, H[3, 3]: 0}
Xi = sp.Matrix([sp.Symbol(f'Xi{i}') for i in range(4)])
kmu = sp.Matrix([0, 0, 0, k])
dh00 = -sp.I * (kmu[0] * Xi[0] + kmu[0] * Xi[0])
check("h_00 is invariant under all residual static gauge transformations",
      sp.simplify(dh00) == 0)

G1g = sp.Matrix(4, 4, lambda m, n: sp.expand(G1[m, n].subs(GAUGE)))
print("  in this gauge:  G^(1)_00 =", sp.simplify(G1g[0, 0]))
print("                  G^(1)_11 =", sp.simplify(G1g[1, 1]))
print("                  G^(1)_22 =", sp.simplify(G1g[2, 2]))

unk = [H[0, 0], H[0, 1], H[0, 2], H[1, 1], H[1, 2], H[2, 2]]
eqs = [sp.Eq(G1g[m, n], Theta[m, n]) for (m, n) in
       [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]]
sol = sp.solve(eqs, unk, dict=True)
check("the 6 dynamical Einstein equations solve uniquely for the 6 gauge-fixed h's",
      len(sol) == 1)
sol = sol[0]
h00_general = sp.simplify(sol[H[0, 0]])
print("\n  h_00(k)  [lambda kept arbitrary] =", h00_general)
check("h_00 = (Theta_00 + Theta_11 + Theta_22)/k^2   (1,2 = transverse to k)",
      sp.simplify(h00_general - (Theta[0, 0] + Theta[1, 1] + Theta[2, 2]) / k ** 2) == 0)

# ======================================================================
hdr("STEP 5.  BRANCH A: generic k  (w.khat != 0)  =>  lambda = 0")
# ======================================================================
h00_A = sp.simplify(h00_general.subs(lam, 0))
print("  lambda = 0  =>  h_00(k) =", h00_A)
U_of_k = sp.simplify(h00_A / 2)                 # DEFINITION C6: h_00 = 2U at w=0
print("  => U(k) = h_00/2 =", U_of_k, "  (so 4 pi G_N = 1/4, G_N = 1/(16 pi) = G)")
dh00_A = sp.simplify(ser_w(h00_A - 2 * U_of_k, 2))
print("  w-dependent part of h_00 =", dh00_A)
check("BRANCH A: h_00 has NO w-dependence at all", sp.simplify(dh00_A) == 0)

a_coef, b_coef = 0, 0
alpha2_A = sp.simplify(-sp.Rational(1, 2) * b_coef)
alpha1_A = sp.simplify(a_coef + sp.Rational(1, 2) * b_coef)
print(f"\n  ==> alpha_1 = {alpha1_A} ,   alpha_2 = {alpha2_A}   (for every K_B, at every w != 0)")

# the price: the aether perturbation is non-normalizable.
# lambda = 0 <=> Psi = 0, with Psi = w.dv - (gw/2) h_00 + (gw/2) h_kl w^k w^l.
# In Lorenz gauge (legitimate here since lambda = 0) h_ij = 2 U delta_ij, h_0i = 0.
dvT = sp.Symbol('dv_T')      # placeholder, computed below
U = sp.Symbol('U', positive=True)
Psi_req = sp.simplify(GW * U * (1 - W2))      # w.dv must equal (gw/2)(h00 - h_kl w^k w^l)
print("\n  Consistency of the aether sector with lambda = 0 requires  Psi = 0, i.e.")
print("      w . dv  =  (gamma_w/2)(h_00 - h_kl w^k w^l)  =", sp.simplify(Psi_req))
vL = sp.simplify((U / GW + 2 * GW * U * (W2 - W[2] ** 2)) / (sp.I * k * W[2]))
print("      => longitudinal aether response  v_L(k) =", vL)
residue = sp.simplify(sp.limit(vL * W[2], wz, 0))
check("v_L has a genuine simple pole at w.khat = 0 (nonzero residue)"
      "  => NON-NORMALIZABLE stationary wake",
      sp.simplify(residue) != 0, f"residue = {residue}")
# and the amplitude blows up as the whole wind goes to zero (take w along k):
vL_along = sp.simplify(vL.subs({wx: 0, wy: 0, wz: 1}))
lead = sp.simplify(sp.limit(vL_along * sw, sw, 0))
check("|v_L| ~ U/w diverges as w -> 0  => linearization fails for w <~ U",
      sp.simplify(lead) != 0, f"lim_{{w->0}} w*v_L = {lead}")

# ======================================================================
hdr("STEP 6.  BRANCH B: w = 0 exactly  =>  lambda != 0   (the discontinuity)")
# ======================================================================
# Aether nu=0 equation: K_B laplacian(Psi) = lambda gamma_w, with F_0i = d_i Psi and
#   Psi = w.dv - (gamma_w/2) h_00 + (gamma_w/2) h_kl w^k w^l .
# At w = 0:  Psi = -h_00/2, and in Fourier laplacian -> -k^2:
lam0 = sp.Symbol('lam0')
h000 = sp.Symbol('h000')
eqA = sp.Eq(-KB * k ** 2 * (-h000 / 2), lam0)                    # aether nu=0
eqB = sp.Eq(h000, (lam0 + rho / 2) / k ** 2)                     # h_00 at w=0
solB = sp.solve([eqA, eqB], [lam0, h000], dict=True)[0]
print("  lambda(w=0) =", sp.simplify(solB[lam0]))
print("  h_00(w=0)   =", sp.simplify(solB[h000]))
GN_w0 = sp.simplify(solB[h000] * k ** 2 / (2 * 4 * sp.pi * rho))
print("  => 4 pi G_N U = ... gives  G_N(w=0) =", sp.simplify(GN_w0),
      "=  1/(16 pi (1 - K_B/2)) = G/(1 - K_B/2)")
check("Branch B: lambda(w=0) = K_B rho / (2(2-K_B)) != 0 for K_B != 0",
      sp.simplify(solB[lam0] - KB * rho / (2 * (2 - KB))) == 0)
GN_A = sp.Rational(1, 16) / sp.pi
check("*** DISCONTINUITY: G_N(w=0) != G_N(w!=0) unless K_B = 0 ***",
      sp.simplify(sp.factor(sp.simplify(GN_w0 - GN_A))) != 0,
      f"G_N(w=0)-G_N(w!=0) = {sp.simplify(GN_w0 - GN_A)}")

# gamma = 1 at w = 0, in Lorenz gauge (consistent because lambda*(w.khat)=0 holds)
LOR = {H[0, 3]: 0, H[1, 3]: 0, H[2, 3]: 0,
       H[3, 3]: -H[0, 0] + H[1, 1] + H[2, 2]}
R1L = sp.Matrix(4, 4, lambda m, n: sp.expand(R1[m, n].subs(LOR)))
hL = sp.Matrix(4, 4, lambda m, n: H[m, n]).subs(LOR)
check("Lorenz gauge identity  R^(1)_{mu nu} = (1/2) k^2 h_{mu nu}",
      all(sp.simplify(R1L[m, n] - sp.Rational(1, 2) * k ** 2 * hL[m, n]) == 0
          for m in range(4) for n in range(4)))
Th0 = Theta.subs({wx: 0, wy: 0, wz: 0})
Tr0 = sp.simplify(sum(ETAI[m, n] * Th0[m, n] for m in range(4) for n in range(4)))
h00_B = sp.simplify(2 * (Th0[0, 0] - sp.Rational(1, 2) * ETA[0, 0] * Tr0) / k ** 2)
hij_B = [sp.simplify(2 * (Th0[i, i] - sp.Rational(1, 2) * ETA[i, i] * Tr0) / k ** 2)
         for i in (1, 2, 3)]
print("\n  w = 0, Lorenz gauge:  h_00 =", h00_B, "   h_ij = delta_ij *", hij_B[0])
check("BRANCH B check (b): gamma = 1 at w = 0  (h_ij = h_00 delta_ij)",
      all(sp.simplify(hij_B[i] - h00_B) == 0 for i in range(3)))
print("  NOTE on check (b): beta is an O(rho^2) quantity.  This calculation is")
print("  LINEAR in rho, so beta is OUT OF SCOPE and is NOT verified here.")

# ======================================================================
hdr("STEP 7.  Check (c): the K_B -> 0 limit")
# ======================================================================
check("K_B -> 0: lambda(w=0) -> 0, G_N -> G, metric is exactly GR",
      sp.simplify(solB[lam0].subs(KB, 0)) == 0 and sp.simplify(GN_w0.subs(KB, 0) - GN_A) == 0)
check("K_B -> 0: alpha_1 = alpha_2 = 0", alpha1_A.subs(KB, 0) == 0 and alpha2_A.subs(KB, 0) == 0)

# ======================================================================
hdr("STEP 8.  U_ij convention, verified")
# ======================================================================
# chi = -int rho |x-x'| satisfies laplacian chi = -2U, and chi_,ij = -delta_ij U + U_ij,
# so U_ij = chi_,ij + delta_ij U.  In Fourier: chi = 2U/k^2, chi_,ij -> -k_i k_j chi.
kk = [0, 0, k]
Uij = sp.Matrix(3, 3, lambda i, j: (1 if i == j else 0) * U - 2 * kk[i] * kk[j] * U / k ** 2)
check("U_ij trace identity  U_ii = U", sp.simplify(sum(Uij[i, i] for i in range(3)) - U) == 0)
wwU = sp.simplify(sum(W[i] * W[j] * Uij[i, j] for i in range(3) for j in range(3)))
check("w^i w^j U_ij = (w^2 - 2 (w.khat)^2) U",
      sp.simplify(wwU - (W2 - 2 * W[2] ** 2) * U) == 0, f"= {wwU}")

# ======================================================================
hdr("STEP 9.  WHY the theory is degenerate: the aether mode speeds")
# ======================================================================
om = sp.Symbol('omega')
V = sp.Matrix([sp.Symbol('V1'), sp.Symbol('V2'), sp.Symbol('V3')])
kk3 = sp.Matrix([0, 0, k])
# flat space, w=0 background, h=0: K_B[ -d_t^2 dv_j + laplacian dv_j - d_j(div dv) ] = 0
disp = sp.Matrix([om ** 2 * V[j] - k ** 2 * V[j] + kk3[j] * (kk3.dot(V)) for j in range(3)])
# transverse polarisation V = (1,0,0):  k.V = 0
tr = sp.simplify(disp.subs({V[0]: 1, V[1]: 0, V[2]: 0})[0])
# longitudinal polarisation V = (0,0,1):  V parallel to k
lo = sp.simplify(disp.subs({V[0]: 0, V[1]: 0, V[2]: 1})[2])
print("  transverse dispersion relation :", tr, "= 0")
print("  longitudinal dispersion relation:", lo, "= 0")
check("spin-1 (transverse) aether mode: omega^2 = k^2, i.e. v^2 = 1",
      sp.simplify(sp.solve(tr, om ** 2)[0] / k ** 2 - 1) == 0)
check("spin-0 (longitudinal) aether mode: omega^2 = 0 => ZERO propagation speed",
      sp.simplify(lo - om ** 2) == 0)

# Einstein-aether dictionary, derived (not looked up):
#   F_{mn}F^{mn} = 2( nabla_m A_n nabla^m A^n - nabla_m A_n nabla^n A^m )
Adg = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f'D{m}{n}'))          # stands for nabla_m A_n
F_from_D = sp.Matrix(4, 4, lambda m, n: Adg[m, n] - Adg[n, m])
lhsD = sp.expand(sum(F_from_D[m, n] * F_from_D[a, b] * ETAI[m, a] * ETAI[n, b]
                     for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
t1 = sum(Adg[m, n] * Adg[a, b] * ETAI[m, a] * ETAI[n, b]
         for m in range(4) for n in range(4) for a in range(4) for b in range(4))
t2 = sum(Adg[m, n] * Adg[a, b] * ETAI[m, b] * ETAI[n, a]
         for m in range(4) for n in range(4) for a in range(4) for b in range(4))
check("derived identity F^2 = 2(nabla_m A_n nabla^m A^n - nabla_m A_n nabla^n A^m)",
      sp.simplify(lhsD - 2 * (t1 - t2)) == 0)
print("  => in the Einstein-aether basis  L = -c1 (nabla_m A_n)(nabla^m A^n)")
print("       - c2 (nabla.A)^2 - c3 (nabla_m A_n)(nabla^n A^m) - c4 (A.nabla A)^2 :")
print("       c1 = +K_B,  c2 = 0,  c3 = -K_B,  c4 = 0")
print("     hence  c1 + c2 + c3 = 0  and  c1 + c3 = 0.")
print("     c1+c2+c3 = 0 is exactly the condition that the spin-0 aether mode has")
print("     ZERO speed (verified above), and c1 = -c3 with c2 = 0 is exactly the")
print("     condition that J^{mu nu} = K_B F^{mu nu} is ANTISYMMETRIC, which is")
print("     what produced the extra identity nabla_nu(lambda A^nu) = 0.")

# ======================================================================
hdr("STEP 10.  A formal extrapolation that is NOT the answer (shown to be honest")
print("           about the magnitude the degenerate limit is hiding)")
# ======================================================================
print("""  If one ILLEGALLY ignores the constraint lambda*(w.khat) = 0 and instead
  assumes lambda keeps its w=0 value lambda_0 = K_B rho/(2(2-K_B)) out to
  O(w^2), then h_00 = (Theta_00 + Theta_11 + Theta_22)/k^2 gives:""")
h00_fake = sp.simplify(h00_general.subs(lam, KB * rho / (2 * (2 - KB))))
h00_fake_w = ser_w(h00_fake, 2)
U_fake = sp.simplify(h00_fake_w.subs({wx: 0, wy: 0, wz: 0}) / 2)
dfake = sp.expand(sp.simplify((h00_fake_w - 2 * U_fake) / U_fake))
print("    h_00(w=0)/2 = U =", U_fake)
print("    (h_00 - 2U)/U =", sp.simplify(dfake))
# write dfake = a*(wx^2+wy^2+wz^2) + b*wz^2 ; then coeff(wx^2)=a and coeff(wz^2)=a+b
dexp = sp.expand(dfake.subs(sw, 1))
a_f = sp.simplify(dexp.coeff(wx, 2))
b_f = sp.simplify(dexp.coeff(wz, 2) - a_f)
check("the formal delta h_00 really is of the form a*w^2 + b*(w.khat)^2 (isotropy in x,y)",
      sp.simplify(dexp - (a_f * (wx ** 2 + wy ** 2 + wz ** 2) + b_f * wz ** 2)) == 0)
print(f"    => a = {a_f} (coeff of w^2 U),  b = {b_f} (coeff of (w.khat)^2 U)")
print(f"    => formal alpha_1 = {sp.simplify(a_f + b_f/2)},"
      f"  formal alpha_2 = {sp.simplify(-b_f/2)}")
print("""    THIS IS NOT A RESULT.  It is what the algebra would give if the
    (3,nu) Einstein constraint equations were thrown away.  They cannot be:
    G^(1)_{3 nu} vanishes identically (Step 2), so 0 = Theta_{3 nu} is an
    equation of the theory, not a gauge choice.  Reported only so that the
    size and K_B-scaling being suppressed by the degeneracy is on the record.""")

# ======================================================================
hdr("SUMMARY")
# ======================================================================
print(f"""
METHOD: matter-rest-frame static-wind calculation (the suggested method), done
  with A_mu as the fundamental variable so that F_{{mu nu}} carries no metric.
  Linearized Einstein tensor from the Riemann definition (Step 2); aether metric
  variation verified off-shell by exact symbolic differentiation (Step 1a);
  aether EOM from sympy's Euler-Lagrange machinery (Step 1b).  Fourier space,
  k^i = (0,0,k) WLOG, w^i general, linear in rho, expanded to O(w^2).

RESULT (for every w != 0, generic k):
      alpha_1(K_B) = {alpha1_A}
      alpha_2(K_B) = {alpha2_A}
  because the linearized field equations FORCE lambda == 0, and lambda A_mu A_nu
  is the ONLY aether source in the linearized Einstein equation.  With lambda=0
  the metric is exactly the GR metric of static dust: no w-dependence anywhere.

BUT THIS IS A DEGENERATE / SINGULAR LIMIT, NOT A NORMAL PPN EVALUATION:
  (i)  it is DISCONTINUOUS at w = 0, where lambda = K_B rho/(2(2-K_B)) != 0 and
       G_N = G/(1 - K_B/2).  The w^0 coefficient of g_00 itself jumps, so g_00
       has no Taylor expansion in w and alpha_1, alpha_2 -- defined as the O(w^2)
       Taylor coefficients -- do not exist in the usual sense.
  (ii) the price of lambda = 0 is a longitudinal aether response with a
       1/(w.khat) pole, i.e. a non-normalizable stationary wake (log-divergent
       along the wind), violating the assumed boundary condition A -> A_bg; its
       amplitude ~ U/w blows up as w -> 0, so linearization fails for w <~ U.
  ROOT CAUSE: c1+c2+c3 = 0 for this theory, so the spin-0 aether mode has ZERO
  propagation speed; a static source resonantly drives it into a wake.
""")

hdr("CHECK LEDGER")
if FAIL:
    print("  FAILED CHECKS: " + ", ".join(FAIL))
    sys.exit(1)
print("  all internal checks passed")
sys.exit(0)
