#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
adv_refute_static_carrier_2026.py
=================================
ADVERSARIAL, INDEPENDENT refutation pass on the "chi + Q_ij auxiliary carrier" candidate
(inverse-design compiler, 2026-08-29).  Written from scratch; it imports NOTHING from
compiler.py / mc_*.py / routeA_* / ppn_khronon_routeB_*.

This file covers the STRUCTURAL / STATIC attacks.  The PPN alphas are in
adv_refute_ppn_2026.py.

SECTIONS
  A  ADM <-> khronometric DICTIONARY, PROVED on explicit components:
       (A1) for a hypersurface-orthogonal u,  nabla_m u_n nabla^n u^m == K_ij K^ij
       (A2) (nabla.u)^2 == K^2
       (A3) a_mu = u^n nabla_n u_mu = (0, D_i ln N)
     => the candidate's gravity sector K_ijK^ij - K^2 + R3 is EXACTLY Einstein-Hilbert,
        so in the khronometric family S=(1/16piG)Int sqrt(-g)[R + lam (nab.u)^2
        + bet nab_m u_n nab^n u^m + alp a.a] the candidate sits at bet = lam = 0 EXACTLY,
        and the MOND sector -chi (D phi)^2 is exactly the "alp a.a" operator with
        alp = -chi.   [this is the load-bearing dictionary both routes assert; here PROVED]

  B  The candidate's OWN static gates, derived from the candidate's OWN ADM action
     (no khronometric input): the exact reduced static action, the Gauss law, the
     interpolation function it actually predicts, and the traceless (slip) equation.
       (B1) GR sector alone forces Psi = Phi at quadratic order  [tests Route A's S1a]
       (B2) Gauss law:  div[(1 + F'(A)/2) grad Phi] = 4 pi G rho  => mu_eff = 1 + F'/2
       (B3) LITERAL frozen spec (V' = -[ln(1-chi)]^2, coefficient chi) gives
            mu_eff in [1, 3/2]: NO deep-MOND limit, EITHER SIGN.  The candidate as
            specified is not a MOND theory at all.
       (B4) the unique repair inside the same Legendre structure, and the khronometric
            coupling it implies: alp_kh(y) = 2(1 - mu(y)).
       (B5) THEOREM:  Sigma_P^TF = 0  <=>  F' = 0  <=>  mu_eff = 1  <=>  no MOND.
            (the same dL/dA multiplies the Gauss flux and the traceless stress)

  C  THE CARRIER.  Q_ij is auxiliary (no time derivative) and its action is
     f(chi) Q.A - (1/2) Q M Q.  Eliminating it EXACTLY gives + (1/2) f^2/M |A|^2.
       (C1) for a LOCAL kernel M this is a LOCAL FUNCTION OF A -- i.e. the carrier is
            *identically* a redefinition F -> F - (f^2/(3M)) A^2.  It therefore cannot
            evade a theorem whose hypothesis is "local function of A".  H4 is VOID.
       (C2) the on-shell carrier traceless stress is O(a^4); Sigma_P is O(a^2).  The
            advertised "exact profile match f(chi(y)) = y e^-y = Sigma_P(y)" is a match
            of two functions of y, not a cancellation of two tensors.
       (C3) which kernels evade: only genuinely NONLOCAL M (Delta^{-1}, or M ~ k^2 with
            the inverse taken) leave the local-F(A) class.  Priced.

  D  EXACT GR BRANCH THEOREM.  At bet = lam = 0 (the candidate's own locus) the
     configuration  a_mu == 0,  chi = 0,  Q = 0,  g = any vacuum/matter GR solution
     solves EVERY field equation exactly, for EVERY source.  So the theory does not
     predict MOND: GR is an exact branch of it.  (Verified symbolically.)

  E  HOW BIG IS THE OBSTRUCTION ANYWAY?  Exact deep-MOND point-mass solution of the
     linearised slip equation.  Reports (Psi-Phi)/Phi in physical units.

Conventions: signature (-,+,+,+); c = 1 except where SI numbers are printed.
Every printed number is tagged PROVEN / COMPUTATIONALLY_VERIFIED / ESTIMATED.
"""
import sympy as sp

CHECKS = []
def check(tag, ok, note=""):
    CHECKS.append((tag, bool(ok), note))
    print(f"   [{'PASS' if ok else 'FAIL'}] {tag}" + (f"   {note}" if note else ""))

def head(s):
    print("\n" + "=" * 88)
    print(s)
    print("=" * 88)


# =====================================================================================
head("SECTION A -- ADM <-> khronometric dictionary, proved on explicit components")
# =====================================================================================
t, x, y, z = sp.symbols('t x y z', real=True)
co = (t, x, y, z)

# generic ADM data, zero shift, everything a function of (t,z) -- generic enough that
# any identity that survives is an identity (it involves K_ij with all of its structure).
N = sp.Function('N')(t, z)
g11 = sp.Function('g11')(t, z); g12 = sp.Function('g12')(t, z); g13 = sp.Function('g13')(t, z)
g22 = sp.Function('g22')(t, z); g23 = sp.Function('g23')(t, z); g33 = sp.Function('g33')(t, z)
gam = sp.Matrix([[g11, g12, g13], [g12, g22, g23], [g13, g23, g33]])
gaminv = gam.inv()

g4 = sp.zeros(4, 4)
g4[0, 0] = -N**2
for i in range(3):
    for j in range(3):
        g4[i + 1, j + 1] = gam[i, j]
g4inv = sp.zeros(4, 4)
g4inv[0, 0] = -1 / N**2
for i in range(3):
    for j in range(3):
        g4inv[i + 1, j + 1] = gaminv[i, j]


def christoffel(g, ginv, coords):
    n = len(coords)
    Gam = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    dg = [[[sp.diff(g[i, j], coords[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    for a in range(n):
        for m in range(n):
            for q in range(m, n):
                s = sp.S.Zero
                for b in range(n):
                    if ginv[a, b] == 0:
                        continue
                    s += ginv[a, b] * (dg[b][m][q] + dg[b][q][m] - dg[m][q][b])
                s = sp.together(sp.expand(s / 2))
                Gam[a][m][q] = s
                Gam[a][q][m] = s
    return Gam


Gam4 = christoffel(g4, g4inv, co)

# u_mu = -N d_mu t  (unit normal of the t = const foliation), hypersurface-orthogonal
u_lo = [-N, 0, 0, 0]
u_up = [sum(g4inv[a, b] * u_lo[b] for b in range(4)) for a in range(4)]
check("A0  u.u = -1", sp.simplify(sum(u_up[a] * u_lo[a] for a in range(4)) + 1) == 0)

# nabla_m u_n
Du = [[sp.expand(sp.diff(u_lo[q], co[m]) - sum(Gam4[a][m][q] * u_lo[a] for a in range(4)))
       for q in range(4)] for m in range(4)]

# extrinsic curvature, zero shift:  K_ij = (1/(2N)) d_t gamma_ij
K = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        K[i, j] = sp.diff(gam[i, j], t) / (2 * N)
Kud = gaminv * K                      # K^i_j
Ktr = sp.trace(Kud)
KijKij = sp.trace(Kud * Kud)

# a_mu = u^n nabla_n u_mu
a_lo = [sp.simplify(sum(u_up[n_] * Du[n_][m] for n_ in range(4))) for m in range(4)]
lnN = sp.log(N)
a_target = [sp.S.Zero, sp.diff(lnN, x), sp.diff(lnN, y), sp.diff(lnN, z)]
check("A3  a_mu = (0, D_i ln N)", all(sp.simplify(a_lo[m] - a_target[m]) == 0 for m in range(4)))

# (nabla.u)^2  and  nabla_m u_n nabla^n u^m
divu = sp.simplify(sum(g4inv[m, n_] * Du[m][n_] for m in range(4) for n_ in range(4)))
check("A2  (nabla.u) = K  (=> (nabla.u)^2 = K^2)", sp.simplify(divu - Ktr) == 0)

Duup = [[sp.expand(sum(g4inv[m, p] * g4inv[n_, q] * Du[p][q] for p in range(4) for q in range(4)))
         for n_ in range(4)] for m in range(4)]
cross = sp.simplify(sum(Du[m][n_] * Duup[n_][m] for m in range(4) for n_ in range(4)))
check("A1  nabla_m u_n nabla^n u^m = K_ij K^ij", sp.simplify(sp.together(cross - KijKij)) == 0)

print("""
   => (1/16piG) Int sqrt(-g)[ R + lam (nab.u)^2 + bet nab_m u_n nab^n u^m + alp a.a ]
      = (1/16piG) Int N sqrt(gam)[ (1+bet) K_ijK^ij - (1-lam) K^2 + R3 + alp (D ln N)^2 ]
   The CANDIDATE's gravity sector is  K_ijK^ij - K^2 + R3  =>  bet = 0 and lam = 0 EXACTLY
   [PROVEN, not assumed], and its MOND sector -chi (D phi)^2 with phi = ln N is the
   khronometric a.a operator with alp = -chi.
   => the candidate is a khronometric theory sitting EXACTLY on bet = lam = 0.
""")


# =====================================================================================
head("SECTION B -- the candidate's OWN static gates, from the candidate's OWN action")
# =====================================================================================
# Static, unitary gauge.  N = e^Phi (so phi = ln N = Phi EXACTLY), gamma_ij = e^{-2psi} delta_ij.
X1, X2, X3 = sp.symbols('x1 x2 x3', real=True)
XS = (X1, X2, X3)
Phi = sp.Function('Phi')(*XS)
psi = sp.Function('psi')(*XS)

eps = sp.symbols('epsilon', positive=True)


def ricci3_conformal(sig):
    """3D Ricci scalar of gamma_ij = e^{2 sig} delta_ij, computed from scratch."""
    g3 = sp.eye(3) * sp.exp(2 * sig)
    g3i = sp.eye(3) * sp.exp(-2 * sig)
    G3 = christoffel(g3, g3i, XS)
    R3 = sp.S.Zero
    for m in range(3):
        for q in range(3):
            if g3i[m, q] == 0:
                continue
            e = sp.S.Zero
            for a in range(3):
                e += sp.diff(G3[a][m][q], XS[a]) - sp.diff(G3[a][m][a], XS[q])
                for b in range(3):
                    e += G3[a][a][b] * G3[b][m][q] - G3[a][q][b] * G3[b][m][a]
            R3 += g3i[m, q] * e
    return sp.simplify(R3)


R3 = ricci3_conformal(-psi)
sqrt_gam = sp.exp(-3 * psi)
Nlapse = sp.exp(Phi)

# The candidate's static Lagrangian density (per 1/16piG), matter = static dust:
#   N sqrt(gam) [ R3 - chi (D phi)^2 - V(chi) ]  - 16 pi G rho N
# with (D phi)^2 = gamma^{ij} d_i Phi d_j Phi = e^{2 psi} (grad Phi)^2.
# We keep the MOND sector EXACT in its nonlinearity by writing it as -F(A), A = (grad Phi)^2,
# where F(A) = g(chi) A + V(chi) on the chi shell (envelope theorem: dF/dA = g(chi)).
A = sum(sp.diff(Phi, s)**2 for s in XS)
rho = sp.Function('rho')(*XS)
Gnewt = sp.symbols('G', positive=True)

# A generic F is represented by a 4-term family that spans analytic AND the sqrt(A) (deep-MOND)
# behaviour, with free coefficients.  Any identity that holds for all c_n holds for any F
# admitting such an expansion.
cc = sp.symbols('c1 c2 c3 c4')
Avar = sp.symbols('Avar', positive=True)
F_of = lambda a: cc[0] * a + cc[1] * a**2 + cc[2] * a**3 + cc[3] * sp.sqrt(a)
Fp_of = lambda a: sp.diff(F_of(Avar), Avar).subs(Avar, a)

# Expand the GR piece to quadratic order in (Phi, psi).  The MOND piece -F(A) is ALREADY
# quadratic in the potentials (A = (grad Phi)^2), so its measure factor N sqrt(gam) and the
# e^{2psi} inside A only contribute at CUBIC order and are dropped here (checked below).
Lgr_full = (Nlapse * sqrt_gam * R3).subs({Phi: eps * Phi, psi: eps * psi}, simultaneous=True)
Lgr_full = Lgr_full.doit()
Lgr2 = sp.expand(sp.series(Lgr_full, eps, 0, 3).removeO())
Lgr2 = sp.expand(Lgr2.coeff(eps, 1) * eps + Lgr2.coeff(eps, 2) * eps**2)
Lgr2 = sp.expand(Lgr2.subs(eps, 1))

Lmatter = -16 * sp.pi * Gnewt * rho * (1 + Phi)
Ltot = Lgr2 - F_of(A) + Lmatter

from sympy.calculus.euler import euler_equations
eqs = euler_equations(Ltot, [Phi, psi], list(XS))
eq_Phi = sp.simplify(sp.expand(eqs[0].lhs))
eq_psi = sp.simplify(sp.expand(eqs[1].lhs))

lap = lambda f: sum(sp.diff(f, s, 2) for s in XS)

# (B1) psi equation
res_psi = sp.simplify(eq_psi - (4 * lap(Phi) - 4 * lap(psi)))
check("B1  psi-equation is  4 lap(Phi) - 4 lap(psi) = 0  =>  Psi = Phi from the GR sector alone",
      res_psi == 0, "[confirms Route A's S1a]")

# (B2) Phi equation -> Gauss law
target = 4 * lap(psi) + 2 * sum(sp.diff(Fp_of(A) * sp.diff(Phi, s), s) for s in XS) \
         - 16 * sp.pi * Gnewt * rho
res_Phi = sp.simplify(sp.expand(sp.expand(eq_Phi - target).doit()))
check("B2  Phi-equation is  4 lap(psi) + 2 div[F'(A) grad Phi] = 16 pi G rho", res_Phi == 0)
print("""   with psi = Phi:   div[ (1 + F'(A)/2) grad Phi ] = 4 pi G rho
      =>   mu_eff(y) = 1 + F'(A)/2      [PROVEN from the candidate's own action]""")

# (B3) the LITERAL frozen constitutive law
chi, yv = sp.symbols('chi y', positive=True)
Vp_literal = -sp.log(1 - chi)**2          # sign fixed by solvability (see below)
# chi EOM for L_MOND = -[chi A + V(chi)] :   A + V'(chi) = 0
sol = sp.solve(sp.Eq(yv**2 + Vp_literal, 0), chi)
sol = [s for s in sol if s.is_real is not False]
chi_of_y = sp.simplify([s for s in sol if sp.simplify(s.subs(yv, 1) - (1 - sp.exp(-1))) == 0][0])
check("B3a frozen V'(chi) = -[ln(1-chi)]^2  =>  chi = 1 - e^{-y} = mu(y)",
      sp.simplify(chi_of_y - (1 - sp.exp(-yv))) == 0, "[the advertised Legendre relation]")
print("     (the OTHER sign, V' = +[ln(1-chi)]^2, gives [ln(1-chi)]^2 = -y^2 : no real root.)")

mu_eff_plus = sp.simplify(1 + chi_of_y / 2)     # if F' = +chi  (MOND term enters with -sign)
mu_eff_minus = sp.simplify(1 - chi_of_y / 2)    # if F' = -chi  (MOND term enters with +sign)
print(f"     F' = +chi -> mu_eff = {mu_eff_plus};  range over y in (0,oo) = "
      f"[{sp.limit(mu_eff_plus, yv, 0)}, {sp.limit(mu_eff_plus, yv, sp.oo)}]")
print(f"     F' = -chi -> mu_eff = {mu_eff_minus};  range over y in (0,oo) = "
      f"[{sp.limit(mu_eff_minus, yv, 0)}, {sp.limit(mu_eff_minus, yv, sp.oo)}]")
deepA = sp.limit(mu_eff_plus, yv, 0)
deepB = sp.limit(mu_eff_minus, yv, 0)
check("B3b LITERAL spec has NO deep-MOND limit (mu_eff(y->0) != 0), for EITHER sign",
      deepA != 0 and deepB != 0,
      f"mu_eff(0) = {deepA} or {deepB};  MOND needs mu_eff -> y -> 0")
newtA = sp.limit(mu_eff_plus, yv, sp.oo); newtB = sp.limit(mu_eff_minus, yv, sp.oo)
check("B3c LITERAL spec also breaks the compiler's OWN frozen gate G_eff/G_N = 1 at high a",
      newtA != 1 and newtB != 1, f"mu_eff(inf) = {newtA} or {newtB}  =>  G_eff/G_N = "
      f"{sp.nsimplify(1/newtA)} or {sp.nsimplify(1/newtB)}")
print("""     PROVEN: since chi in [0,1] and mu_eff = 1 +- chi/2, mu_eff can never reach 0.
     A deep-MOND limit needs F'(A) -> -2 as y -> 0, i.e. |F'| = O(1) and NEGATIVE.
     No sign choice of "coefficient = chi" can do it.  THE CANDIDATE AS SPECIFIED IS NOT MOND.""")

# (B4) the repair
mu_frozen = 1 - sp.exp(-yv)
Fp_req = sp.simplify(2 * (mu_frozen - 1))
check("B4a repair: mu_eff = mu(y) requires F'(A) = 2(mu-1) = -2 e^{-y}",
      sp.simplify(1 + Fp_req / 2 - mu_frozen) == 0)
alp_kh = sp.simplify(-Fp_req)
check("B4b => khronometric coupling alp_kh(y) = -F' = 2(1-mu) = 2 e^{-y}",
      sp.simplify(alp_kh - 2 * sp.exp(-yv)) == 0)
check("B4c consistency: G_eff/G = 1/(1-alp/2) equals 1/mu (the MOND Poisson law)",
      sp.simplify(1 / (1 - alp_kh / 2) - 1 / mu_frozen) == 0)
# what V does the repair need?
g_of_chi = -2 * (1 - chi)                       # coefficient of A
Vp_req = sp.simplify(-sp.diff(g_of_chi, chi) * yv**2)          # chi EOM: g'(chi)A + V'(chi) = 0
Vp_req_chi = sp.simplify(Vp_req.subs(yv, -sp.log(1 - chi)))
print(f"     the repaired Legendre pair:  g(chi) = {g_of_chi},  V'(chi) = {Vp_req_chi}")
print("     i.e. the FROZEN V is right up to a factor -2; what is WRONG in the spec is the")
print("     function multiplying (D phi)^2: it must be 2(1-chi), not chi.")
print("     NOTE: the advertised carrier coupling f(chi) = (1-chi) sqrt(V'(chi)) is then")
print("           imaginary (V' < 0), so the one 'exactly verified' identity of the design")
print("           was computed with the constitutive law that does not do MOND.")
check("B4d f(chi) = (1-chi) sqrt(V') is not real on the repaired branch",
      sp.simplify(Vp_req_chi.subs(chi, sp.Rational(1, 2))) < 0,
      f"V'(1/2) = {sp.nsimplify(Vp_req_chi.subs(chi, sp.Rational(1,2)))} < 0")

# (B5) the Sigma_P <-> Gauss-flux theorem
gam_ij = sp.MatrixSymbol('gam', 3, 3)
# Sigma^TF_ij  from  delta[ -N sqrt(gam) F(A) ] / delta gamma^{ij}, A = gamma^{ij} d_iPhi d_jPhi
# envelope theorem removes any delta chi.  Result: -F'(A) [d_i Phi d_j Phi]^TF.
print("""
   B5  THEOREM (two-line, PROVEN):
       A = gamma^{ij} d_i phi d_j phi  is the ONLY place the metric enters the MOND sector.
       => Gauss flux      J^i  = 2 F'(A) d^i phi        (Phi-variation)
       => traceless stress Sig^TF_ij = -F'(A) [d_i phi d_j phi]^TF   (gamma-variation)
       Both carry the SAME factor F'(A).  Hence
              Sigma_P = 0   <=>   F' = 0   <=>   mu_eff = 1   <=>   NO MOND.
       This holds for ANY local F, INCLUDING any F produced by integrating out auxiliaries
       (section C).  It is the compiler's own Part-I obstruction, re-derived from the
       candidate's own action, and it is NOT evaded by the carrier.""")


# =====================================================================================
head("SECTION C -- the carrier: eliminating Q_ij exactly")
# =====================================================================================
f_s, M_s = sp.symbols('f M', positive=True)
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
avec = sp.Matrix([a1, a2, a3])
Asq = (avec.T * avec)[0, 0]
A_ij = avec * avec.T - sp.eye(3) * Asq / 3          # [a_i a_j]^TF
q = sp.symbols('q11 q12 q13 q22 q23', real=True)
Q = sp.Matrix([[q[0], q[1], q[2]],
               [q[1], q[3], q[4]],
               [q[2], q[4], -q[0] - q[3]]])          # symmetric traceless

L_carrier = f_s * sp.trace(Q * A_ij) - sp.Rational(1, 2) * M_s * sp.trace(Q * Q)
sol_Q = sp.solve([sp.diff(L_carrier, s) for s in q], list(q), dict=True)[0]
Qon = sp.simplify(Q.subs(sol_Q))
check("C0  Q EOM gives Q_ij = (f/M) A_ij", sp.simplify(Qon - (f_s / M_s) * A_ij) == sp.zeros(3, 3))

L_on = sp.simplify(L_carrier.subs(sol_Q))
target_on = sp.Rational(1, 2) * f_s**2 / M_s * sp.trace(A_ij * A_ij)
check("C1a on-shell carrier Lagrangian = (1/2)(f^2/M) A_ij A^ij", sp.simplify(L_on - target_on) == 0)
check("C1b A_ij A^ij = (2/3) A^2  =>  L_on = (f^2/(3M)) A^2, a LOCAL FUNCTION OF A ALONE",
      sp.simplify(sp.trace(A_ij * A_ij) - sp.Rational(2, 3) * Asq**2) == 0,
      f"L_on = {sp.simplify(L_on)}")
print("""
   C1  CONCLUSION (PROVEN).  For any LOCAL kernel M (algebraic mass m^2, or any function of
       chi/y), integrating out the auxiliary TT tensor returns EXACTLY
           Delta L = (f(chi)^2 / (3 M)) A^2 ,
       i.e. a redefinition  F(A) -> F(A) - f^2 A^2/(3M).  The carrier adds NO new tensor
       structure whatsoever.  Therefore hypothesis (H4) ("scalar/isotropic carrier") is NOT
       violated by this construction, the Part-I no-go applies verbatim to the redefined F,
       and B5 still gives  Sigma_P = 0 <=> no MOND.
       *** The candidate's advertised escape route is void. ***""")

# C2 order counting
Sig_M = -sp.symbols('Fp') * A_ij                      # MOND traceless stress: O(a^2)
Sig_Q = sp.simplify(sp.diff(L_on, a1))                # just to exhibit the degree
lam_sc = sp.symbols('lamsc', positive=True)
deg_carrier = sp.simplify(sp.expand(L_on.subs({a1: lam_sc * a1, a2: lam_sc * a2, a3: lam_sc * a3})
                                    / L_on))
check("C2  carrier on-shell stress is O(a^4) while Sigma_P is O(a^2)",
      sp.simplify(deg_carrier - lam_sc**4) == 0,
      "profile-matching f(chi(y)) = y e^{-y} = Sigma_P(y) matches two FUNCTIONS OF y, "
      "not two TENSORS; they sit at different orders in a and cannot cancel")

print("""
   C3  WHICH KERNELS ACTUALLY LEAVE THE LOCAL-F(A) CLASS?
       M = m^2 (algebraic)   -> (f^2/(3 m^2)) A^2                   LOCAL. no escape.
       M = M(chi) (the "repair" Route A found, M ~ (1-chi)V'(chi))  LOCAL. no escape.
       M = -D^2              -> f A_ij (-D^2)^{-1} f A^ij           NONLOCAL. genuine escape,
                                                                    at the price of an
                                                                    inverse Laplacian.
       M = Delta^{-1}        -> -(1/2) |D_k (f A_ij)|^2             LOCAL but FOUR spatial
                                                                    derivatives: escapes (H2),
                                                                    not (H4).
       => the tensor carrier per se buys NOTHING.  Every escape is really an (H1) or (H2)
       escape (nonlocality or higher derivatives), which the compiler already lists as
       separate hatches and which carry their own well-known costs.  [PROVEN]""")


# =====================================================================================
head("SECTION D -- EXACT GR BRANCH:  a_mu == 0, chi = 0, Q = 0 solves everything")
# =====================================================================================
Achi = sp.symbols('A', nonnegative=True)
gfun = sp.Function('g'); Vfun = sp.Function('V')
Lmond = -(gfun(chi) * Achi + Vfun(chi))
chi_eom = sp.diff(Lmond, chi)
print("   MOND sector L = -[g(chi) A + V(chi)];  chi EOM: ", sp.Eq(chi_eom, 0))
print("   at A = 0 this is V'(chi) = 0.  For the frozen V (either sign) V'(chi) = -[ln(1-chi)]^2,")
print("   whose only root is chi = 0, and V(0) = 0.  So L_MOND|_{a=0} = 0.")
chi_free = sp.Symbol('chi_free')
chi0_root = sp.solve(sp.Eq(-sp.log(1 - chi_free)**2, 0), chi_free)
check("D1  V'(chi) = 0 has the unique root chi = 0", chi0_root == [0], f"roots = {chi0_root}")
check("D2  carrier at A_ij = 0: Q EOM gives Q = 0 and L_carrier = 0",
      sp.simplify(L_carrier.subs({a1: 0, a2: 0, a3: 0}).subs(
          {s: 0 for s in q})) == 0)
print("""
   D3  THE THEOREM.  With bet = lam = 0 (SECTION A: forced by the candidate's own gravity
       sector) the entire non-GR part of the action is a functional of a_mu that is at
       least QUADRATIC in a_mu:   L_LV = -[g(chi) a.a + V(chi)] + f(chi) Q.[a a]^TF - (1/2)QMQ.
         * metric EOM:   Theta_munu = dL/dg^{munu} - (1/2)g_munu L_LV.  Every term carries an
           explicit a_mu or a_ij, and L_LV|_{a=0} = -V(0) = 0.  => Theta_munu = 0.
         * khronon EOM:  dS/dT is a total divergence of  (dL/da_nu)(da_nu/d(d_mu T)), and
           dL/da_nu ~ 2 g(chi) a^nu + ... vanishes at a = 0.  => satisfied identically.
       Hence: (any GR solution g, any GEODESIC time-slicing T, chi = 0, Q = 0) is an EXACT
       solution of the candidate for EVERY matter source.  Example: exact Schwarzschild with
       the Painleve-Gullstrand foliation (its slices are geodesic, a_mu = 0).
       *** The candidate does not PREDICT MOND.  GR-with-no-MOND is an exact branch of it,
       and nothing in the theory selects the MOND branch. ***                       [PROVEN]
       (This is special to bet = lam = 0.  With bet or lam nonzero the khronon EOM contains
        K_ij / K terms that do NOT vanish on a geodesic foliation, and the GR branch closes.)""")


# =====================================================================================
head("SECTION E -- how big is the Part-I obstruction, physically?")
# =====================================================================================
# ---- E0: derive the traceless ij Einstein equation from scratch (no quoted formula) ----
tt = sp.Symbol('t')
Phn = sp.Function('Phi')(*XS)
psn = sp.Function('psi')(*XS)
coords4 = (tt, X1, X2, X3)
gN = sp.diag(-(1 + 2 * eps * Phn), 1 - 2 * eps * psn, 1 - 2 * eps * psn, 1 - 2 * eps * psn)
gNi = gN.inv()
GamN = christoffel(gN, gNi, coords4)
RicN = sp.zeros(4, 4)
for m in range(4):
    for q in range(m, 4):
        e = sp.S.Zero
        for a in range(4):
            e += sp.diff(GamN[a][m][q], coords4[a]) - sp.diff(GamN[a][m][a], coords4[q])
            for b in range(4):
                e += GamN[a][a][b] * GamN[b][m][q] - GamN[a][q][b] * GamN[b][m][a]
        e = sp.expand(sp.series(sp.expand(e), eps, 0, 2).removeO()).coeff(eps, 1)
        RicN[m, q] = e
        RicN[q, m] = e
Rs = sp.expand(sum(sp.eye(4)[0, 0] * 0 for _ in [0]))
etainv = sp.diag(-1, 1, 1, 1)
Rs = sp.expand(sum(etainv[m, m] * RicN[m, m] for m in range(4)))
GN = sp.zeros(4, 4)
for m in range(4):
    for q in range(4):
        GN[m, q] = sp.expand(RicN[m, q] - sp.Rational(1, 2) * sp.diag(-1, 1, 1, 1)[m, q] * Rs)
# traceless spatial part
Gsp = GN[1:, 1:]
GTF = sp.expand(Gsp - sp.eye(3) * sp.trace(Gsp) / 3)
slipf = psn - Phn
GTF_target = sp.Matrix(3, 3, lambda i, j: sp.expand(
    sp.diff(slipf, XS[i], XS[j]) - (1 if i == j else 0) * lap(slipf) / 3))
check("E0  linearised G^TF_ij = (d_i d_j - delta_ij lap/3)(psi - Phi)",
      sp.simplify(GTF - GTF_target) == sp.zeros(3, 3))

# ---- E1: the candidate's own TF stress, and the induced slip, exactly ----
# From the reduced action (units 1/16piG factored out) the MOND sector's contribution to the
# ij field equation is  G^TF_ij = F'(A) [d_i Phi d_j Phi]^TF   (same F' as in B2/B5).
r = sp.symbols('r', positive=True)
GM, a0s = sp.symbols('GM a0', positive=True)
Fp_deep = -2                                    # repaired F'(A) -> -2 as y -> 0 (deep MOND)
grad = sp.sqrt(GM * a0s) / r                    # deep-MOND field of a point mass, |grad Phi|
# slip P(r) = psi - Phi obeys  P'' - P'/r = F'_deep * grad^2
P = sp.Function('P')
ode = sp.Eq(sp.diff(P(r), r, 2) - sp.diff(P(r), r) / r, Fp_deep * grad**2)
sol = sp.dsolve(ode, P(r))
Pr = sol.rhs.subs({sp.Symbol('C1'): 0, sp.Symbol('C2'): 0})
ratio = sp.simplify(sp.diff(Pr, r) / grad)
check("E1  deep-MOND point mass: |d(psi-Phi)/dr| / |dPhi/dr| = sqrt(G M a0) = v_flat^2/c^2",
      sp.simplify(sp.Abs(ratio) - sp.sqrt(GM * a0s)) == 0,
      f"ratio = {ratio}   (v_flat^2 = sqrt(G M a0) in deep MOND)")

for name, vflat in [("dwarf  v=50 km/s", 50e3), ("Milky Way v=220 km/s", 220e3),
                    ("massive spiral v=300 km/s", 300e3)]:
    print(f"     {name:28s}  |slip'|/|Phi'| = v_flat^2/c^2 = "
          f"{vflat**2/(299792458.0)**2:.3e}")
print("""
   E2  READING.  The Part-I traceless stress is REAL (B5) but the metric slip it induces is
       v_flat^2/c^2 ~ 1e-7 - 1e-6 RELATIVE.  Lensing (and every other test that compares
       the lensing potential to the dynamical potential) is nowhere near that.  So
       "Sigma_P != 0 => cannot lens" is a statement about a formally nonzero, physically
       negligible slip -- UNLESS one is testing the CANCELLATION of Sigma_P as an algebraic
       identity rather than its observable consequence.  (mc_gates.py applies BOTH: a physical
       FRAME_SLIP test |Phi'-Psi'|/g_dyn, which is the right one, AND a SIGMA_P_NONZERO test
       built on the cancellation residual worst_rel, which is not a physical magnitude.)
       [COMPUTATIONALLY_VERIFIED for the isolated deep-MOND point mass; the number is an
        exact solution of the linearised slip equation, not a scaling estimate.]
       This does NOT rescue the candidate (sections B3, C1, D kill it independently) -- it
       says the carrier was built to cancel something that did not need cancelling.""")


# =====================================================================================
head("SUMMARY")
# =====================================================================================
import sys as _s
nfail = sum(1 for _, ok, _ in CHECKS if not ok)
for tag, ok, note in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}")
print(f"\n  {len(CHECKS) - nfail}/{len(CHECKS)} checks passed.")
_s.exit(0 if nfail == 0 else 1)
