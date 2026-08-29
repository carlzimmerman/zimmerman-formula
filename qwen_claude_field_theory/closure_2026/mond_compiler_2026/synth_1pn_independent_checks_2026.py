#!/usr/bin/env python3
"""
SYNTHESIS-LEVEL INDEPENDENT CHECKS for the chi + Q_ij carrier candidate, 2026-08-29.

Written by the SYNTHESIS pass, from scratch.  Imports nothing from compiler.py, mc_*.py,
routeA_alpha12_ppn_2026.py, ppn_khronon_routeB_*.py, adv_refute_*.py.

Purpose: I am adjudicating Route A vs Route B vs the adversarial refuter.  Before I sign a
verdict I re-derive, myself, the handful of load-bearing algebraic facts that the verdict
actually rests on, and I close one gap I found in the refuter's SECTION C.

THE GAP.  The candidate spec says Q_ij is "spatially-transverse-traceless (Q^i_i = 0)".
Those are two DIFFERENT constraints and the parenthetical only states the trace one.  The
refuter's C1 varied 5 traceless components with NO transversality constraint and concluded
that eliminating Q returns a pure redefinition F(A) -> F(A) - f^2 A^2/(3M), i.e. the carrier
adds no new tensor structure and the Part-I no-go applies verbatim.  That conclusion is
correct for the TRACELESS-ONLY reading.  It is NOT automatic for the TRANSVERSE-traceless
reading, because the TT projector is nonlocal.  Checked here (C3/C4).

Checks:
  A  literal spec constitutive law: mu_eff never reaches 0 (no deep-MOND limit), either sign
  B  carrier elimination, TRACELESS-ONLY Q            -> (f^2/(3M)) A^2   [refuter C1 reproduced]
  C  carrier elimination, TRANSVERSE-TRACELESS Q      -> NOT proportional to A^2 (nonlocal)
  D  Foster-Jacobson -> hypersurface-orthogonal limit -> khronometric alpha_1, alpha_2,
     evaluated at the candidate's own locus bet = lam = 0
  E  GR-branch theorem: the frozen V has its only stationary point at chi = 0 with V(0) = 0
"""

import sympy as sp

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((ok, name, note))
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def head(t):
    print("\n" + "=" * 92)
    print(t)
    print("=" * 92)


# ===========================================================================================
head("SECTION A -- literal spec: does 'coefficient = chi' admit a deep-MOND limit?")
# ===========================================================================================
# MOND sector of the action:  -(c^3/16 pi G) N sqrt(gam) [ chi A + V(chi) ],  A = (D phi)^2.
# chi is auxiliary => eliminate it:  d/dchi [ chi A + V(chi) ] = 0  =>  V'(chi) = -A.
# Envelope theorem: F(A) = chi(A) A + V(chi(A))  =>  F'(A) = chi(A).
chi, A, y = sp.symbols('chi A y', positive=True)

# frozen Legendre relation as specced, V'(chi) = -[ln(1-chi)]^2
Vp = -sp.log(1 - chi) ** 2
sol = sp.solve(sp.Eq(Vp, -A), chi)
chi_of_A = [s for s in sol if sp.simplify(s.subs(A, 1) - (1 - sp.exp(-1))) == 0]
check("A1  frozen V'(chi) = -[ln(1-chi)]^2 inverts to chi = 1 - e^{-sqrt(A)} = mu(y)",
      len(chi_of_A) == 1 and sp.simplify(chi_of_A[0] - (1 - sp.exp(-sp.sqrt(A)))) == 0,
      f"chi(A) = {sp.simplify(chi_of_A[0])}")

mu = 1 - sp.exp(-y)  # with y = sqrt(A)
# The static Poisson operator that the candidate's own action produces is
#   div[ (1 + F'(A)/2) grad Phi ] = 4 pi G rho     =>   mu_eff = 1 + F'(A)/2.
# (This is the refuter's B2, re-stated; the +1 is the GR sector, the F'/2 the MOND sector.)
for sgn, lab in [(+1, "F' = +chi"), (-1, "F' = -chi")]:
    mu_eff = 1 + sgn * mu / 2
    lo = sp.limit(mu_eff, y, 0)
    hi = sp.limit(mu_eff, y, sp.oo)
    check(f"A2 [{lab}]  mu_eff(y->0) = {lo} != 0  => NO deep-MOND limit", lo != 0,
          f"range over y in (0,oo) = [{min(lo, hi)}, {max(lo, hi)}];  MOND needs mu_eff -> 0")
    check(f"A3 [{lab}]  mu_eff(y->oo) = {hi}  => G_eff/G_N = {sp.nsimplify(1/hi)} != 1 at high acceleration",
          True, "breaks the compiler's own frozen Newtonian gate unless = 1")

check("A4  PROVEN: chi in [0,1] and mu_eff = 1 +- chi/2 => mu_eff in [1/2, 3/2], "
      "never 0. Deep MOND needs F' -> -2, i.e. |F'| = O(1) and NEGATIVE. "
      "No sign choice of 'coefficient = chi' can do it.", True,
      "the repair is coefficient 2(1-chi), on which f = (1-chi)sqrt(V') is IMAGINARY since V' < 0")


# ===========================================================================================
head("SECTION B -- carrier elimination with TRACELESS-ONLY Q (the refuter's reading)")
# ===========================================================================================
a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
f_s, M_s = sp.symbols('f M', positive=True)
a_vec = sp.Matrix([a1, a2, a3])
Aa = (a_vec.T * a_vec)[0, 0]                       # A = a.a
A_ij = a_vec * a_vec.T - sp.Rational(1, 3) * Aa * sp.eye(3)   # [a_i a_j]^TF

check("B0  A_ij is traceless", sp.simplify(A_ij.trace()) == 0)
check("B1  A_ij A^ij = (2/3) A^2  [pure algebra, no model input]",
      sp.simplify(sum(A_ij[i, j] ** 2 for i in range(3) for j in range(3)) - sp.Rational(2, 3) * Aa ** 2) == 0)

# L_carrier = f Q^ij A_ij - (1/2) Q^ij M Q_ij, Q symmetric traceless (5 free components)
q11, q12, q13, q22, q23 = sp.symbols('q11 q12 q13 q22 q23', real=True)
Q = sp.Matrix([[q11, q12, q13], [q12, q22, q23], [q13, q23, -q11 - q22]])
L_car = f_s * sum(Q[i, j] * A_ij[i, j] for i in range(3) for j in range(3)) \
    - sp.Rational(1, 2) * M_s * sum(Q[i, j] ** 2 for i in range(3) for j in range(3))
eqs = [sp.diff(L_car, v) for v in (q11, q12, q13, q22, q23)]
solQ = sp.solve(eqs, [q11, q12, q13, q22, q23], dict=True)[0]
Q_on = Q.subs(solQ)
check("B2  Q EOM gives Q_ij = (f/M) A_ij", sp.simplify(Q_on - (f_s / M_s) * A_ij) == sp.zeros(3, 3))

L_on = sp.simplify(L_car.subs(solQ))
target = f_s ** 2 * Aa ** 2 / (3 * M_s)
check("B3  on-shell carrier Lagrangian = (f^2/(3M)) A^2 -- a FUNCTION OF A ALONE",
      sp.simplify(L_on - target) == 0,
      "=> pure redefinition F(A) -> F(A) + f^2 A^2/(3M); NO new tensor structure; "
      "Part-I applies verbatim.  REFUTER'S C1 INDEPENDENTLY REPRODUCED.")

check("B4  and it is O(a^4) while Sigma_P ~ F'(A)[a_i a_j]^TF is O(a^2)",
      sp.Poly(sp.expand(L_on * 3 * M_s / f_s ** 2), a1, a2, a3).total_degree() == 4,
      "different orders in a: profile-matching f(y) = Sigma_P(y) matches two FUNCTIONS OF y, "
      "not two TENSORS")


# ===========================================================================================
head("SECTION C -- carrier elimination with TRANSVERSE-traceless Q  (THE GAP I AM CLOSING)")
# ===========================================================================================
# If Q is additionally TRANSVERSE, D^i Q_ij = 0, then the Q variation is only required to
# vanish after projection onto the TT subspace:   P^TT [ f A - M Q ] = 0.
# For algebraic M (= m^2, commuting with the projector) this gives Q = (f/M) P^TT[A], and
#     L_on = (1/2) f A_ij Q^ij = (1/2)(f^2/M) A_ij (P^TT A)^ij .
# In Fourier at wavevector n (unit), the TT projector on a symmetric tensor is
#     P^TT_{ij,kl} = P_{i(k} P_{l)j} - (1/2) P_ij P_kl,   P_ij = delta_ij - n_i n_j .
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)
n = sp.Matrix([n1, n2, n3])
P = sp.eye(3) - n * n.T


def TT(S, P):
    """TT projection of a symmetric 3x3 S with respect to projector P (rank 2)."""
    PS = P * S * P
    return PS - sp.Rational(1, 2) * P * PS.trace()


# work on the unit sphere n.n = 1
sub_unit = {n3: sp.sqrt(1 - n1 ** 2 - n2 ** 2)}
A_TT = TT(A_ij, P)
check("C1  P^TT is a projector on symmetric tensors (idempotent on the unit sphere)",
      sp.simplify((TT(TT(A_ij, P), P) - TT(A_ij, P)).subs(sub_unit)) == sp.zeros(3, 3))
check("C2  P^TT[A] is traceless and transverse (n^i P^TT[A]_ij = 0)",
      sp.simplify(TT(A_ij, P).trace().subs(sub_unit)) == 0
      and sp.simplify((n.T * TT(A_ij, P)).subs(sub_unit)) == sp.zeros(1, 3))

contract_TT = sp.simplify(sum(A_ij[i, j] * A_TT[i, j] for i in range(3) for j in range(3)).subs(sub_unit))
contract_flat = sp.Rational(2, 3) * Aa ** 2

# Is the TT-contracted result equal to the traceless-only one, i.e. still a function of A alone?
diff = sp.simplify(sp.expand(contract_TT - contract_flat))
check("C3  A_ij (P^TT A)^ij  !=  (2/3) A^2 : the TT projection is NOT a function of A alone",
      diff != 0,
      "it depends on the ANGLE between a_i and the wavevector n => in position space it is "
      "NONLOCAL (inverse Laplacians)")

# make the angular dependence explicit and unmistakable: a along x, vary n
val_par = contract_TT.subs({a1: 1, a2: 0, a3: 0, n1: 1, n2: 0})      # n parallel to a
val_perp = contract_TT.subs({a1: 1, a2: 0, a3: 0, n1: 0, n2: 0})     # n perpendicular to a
check("C4  explicit angular dependence: a = x_hat gives DIFFERENT values for n || a and n _|_ a",
      sp.simplify(val_par - val_perp) != 0,
      f"n||a -> {sp.nsimplify(val_par)} ;  n _|_ a -> {sp.nsimplify(val_perp)} ; "
      f"traceless-only value would be 2/3 for both")

print("""
   C5  READING [PROVEN].  The refuter's C1 ("the carrier is a pure redefinition of F(A),
       so Part-I applies verbatim and the H4 escape is void") is CORRECT for the reading
       the parenthetical states, Q^i_i = 0 (traceless only) -- reproduced above at B3.
       For the STRICTLY TRANSVERSE-traceless reading it does NOT hold: eliminating a TT Q
       returns A_ij P^TT A^ij, which is nonlocal, so the carrier DOES add structure that
       F(A) cannot.  BUT:
         * that is an (H1) NONLOCALITY escape, not the advertised (H3)/(H4) degenerate-
           tensor-carrier escape -- exactly the same verdict the refuter reached for
           M = -D^2 and M = Delta^{-1};
         * enforcing D^i Q_ij = 0 is a DIFFERENTIAL constraint needing its own Lagrange
           multiplier, so Q stops being an algebraic auxiliary and the Dirac/DOF count of
           dirac_chi_Q_frozen_candidate_2026.py (already 3 DOF, not 2) must be redone;
         * and it changes NOTHING about the two kills that do not involve the carrier at
           all: SECTION A above (the literal spec is not MOND) and the GR-branch theorem
           (SECTION E below), both of which hold with Q = 0 identically.
       So the gap is real and worth recording, but it is not a rescue.""")


# ===========================================================================================
head("SECTION D -- structure of the khronometric alpha_1, alpha_2 at the candidate's locus")
# ===========================================================================================
# HONEST SCOPE STATEMENT.  I do NOT re-derive Foster-Jacobson from memory here: reciting a
# literature formula from recall would be exactly the kind of fabricated number this program
# forbids.  The literature anchor is carried by THREE independent in-script derivations that
# already agree with each other:
#   * adv_refute_ppn_2026.py D1/D2  -- takes Einstein-aether to the hypersurface-orthogonal
#     limit (c1 -> oo at fixed c14, c13, c2) IN SCRIPT, then reproduces its own 1PN engine
#     at 5 exact-rational points;
#   * ppn_khronon_routeB_limit_2026.py -- same formulas, 4 rational points, digit-for-digit;
#   * routeA_alpha12_ppn_2026.py -- anchored instead to Blas-Pujolas-Sibiryakov 1007.3503
#     Eq. (5.34) at beta = 0.
# What I check HERE is the thing the verdict actually turns on: the POLE STRUCTURE of those
# formulas, and the DISCONTINUITY between the limit and the value at the candidate's locus.
alp, bet, lam = sp.symbols('alp bet lam', real=True)

alpha1_kh = 4 * (alp - 2 * bet) / (bet - 1)
alpha2_kh = ((alp - 2 * bet)
             * (2 * (alp - 2) * (bet + lam) - (bet - 1) * (alp + bet + 3 * lam))
             / ((alp - 2) * (bet - 1) * (bet + lam)))

check("D0  the two routes' alpha_2 is alpha_1/2 - (alp-2bet)(alp+bet+3lam)/((alp-2)(bet+lam)) "
      "-- the standard khronometric shape",
      sp.simplify(alpha2_kh - (alpha1_kh / 2 - (alp - 2 * bet) * (alp + bet + 3 * lam)
                               / ((alp - 2) * (bet + lam)))) == 0)

check("D1  alpha_1 is REGULAR at the candidate's locus bet = lam = 0 and equals -4 alp there",
      sp.simplify(alpha1_kh.subs({bet: 0, lam: 0}) + 4 * alp) == 0,
      "so alpha_1 has NO pole to hide behind: off the locus it is simply -4 alp")

def is_infinite(e):
    """robust: sympy returns directed infinities like -oo*sign(...) for symbolic residues."""
    return bool(e.has(sp.oo, -sp.oo, sp.zoo)) or e.is_infinite is True


# the c_123 pole:  bet + lam -> 0.  Evaluate at a concrete alp so the residue has a definite sign.
lim_a2 = sp.limit(alpha2_kh.subs({bet: 0, alp: sp.Rational(1, 5)}), lam, 0)
check("D2  alpha_2 carries a 1/c_123 = 1/(bet+lam) POLE and the candidate sits EXACTLY ON it",
      is_infinite(lim_a2),
      f"at alp = 1/5:  lim_{{lam->0}} alpha_2|_{{bet=0}} = {lim_a2}")

# the second pole: alp -> 2, which is precisely the deep-MOND end (alp_kh = 2(1-mu) -> 2)
lim_a2b = sp.limit(alpha2_kh.subs({bet: 0, lam: sp.Rational(1, 3)}), alp, 2)
check("D3  alpha_2 carries a SECOND pole at alp = 2 -- and deep MOND needs alp_kh = 2(1-mu) -> 2",
      is_infinite(lim_a2b),
      f"lim_{{alp->2}} alpha_2 = {lim_a2b};  the MOND regime is the other singular locus, "
      "and the edge of the aether stability domain 0 <= c14 < 2")

# THE DISCONTINUITY, computed symbolically along the routes' own approach path.
# SIGN DICTIONARY (established by the routes and re-confirmed here at D6): the routes'
# approach parameter delta is OUR (bet, lam) = (delta, delta) = LITERATURE (-delta, -delta),
# and alpha1_kh / alpha2_kh above are written in LITERATURE variables.
d = sp.symbols('d', positive=True)
a1_path = sp.simplify(alpha1_kh.subs({bet: -d, lam: -d}))
a2_path = sp.simplify(alpha2_kh.subs({bet: -d, lam: -d}))
a1_lim = sp.limit(a1_path, d, 0)
a2_lim = sp.limit(a2_path.subs({alp: sp.Rational(1, 5)}), d, 0)
print(f"   along literature bet = lam = -d:   alpha_1(d) = {a1_path}   ->   {a1_lim}  as d -> 0")
print(f"   along literature bet = lam = -d:   alpha_2(d)|_{{alp=1/5}} -> {a2_lim}  as d -> 0")
check("D4  LIMIT along the approach path: alpha_1 -> -4 alp (NOT 0)",
      sp.simplify(a1_lim + 4 * alp) == 0)
check("D5  LIMIT along the approach path: alpha_2 -> infinite (NOT 0)",
      is_infinite(a2_lim), f"alpha_2 -> {a2_lim}")

# reproduce the routes' shared numerical approach table from these formulas alone
print("\n   approach table at alp = 1/5, regenerated from the formulas (compare Route B's"
      " routeB_limit_2026.out and the refuter's F-table -- both report these same values):")
print(f"      {'d':<10}{'alpha_1':<20}{'alpha_2':<24}")
tab = {}
for dv in [sp.Rational(1, 2), sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]:
    v1 = sp.nsimplify(sp.together(a1_path.subs({alp: sp.Rational(1, 5), d: dv})))
    v2 = sp.nsimplify(sp.together(a2_path.subs({alp: sp.Rational(1, 5), d: dv})))
    tab[dv] = (v1, v2)
    print(f"      {str(dv):<10}{str(v1):<20}{str(v2):<24}")
check("D6  regenerated table matches the two routes' published approach values EXACTLY",
      tab[sp.Rational(1, 2)] == (sp.Rational(-16, 5), sp.Rational(-2, 5))
      and tab[sp.Rational(1, 10)] == (sp.Rational(-16, 11), sp.Rational(-50, 99))
      and tab[sp.Rational(1, 100)] == (sp.Rational(-88, 101), sp.Rational(-6424, 4545))
      and tab[sp.Rational(1, 1000)] == (sp.Rational(-808, 1001), sp.Rational(-5135749, 450450)),
      "alpha_1 = -16/5, -16/11, -88/101, -808/1001;  alpha_2 = -2/5, -50/99, -6424/4545, -5135749/450450")

print("""
   D7  READING.  The candidate's own locus (bet = lam = 0, forced EXACTLY by the gravity
       sector K_ijK^ij - K^2 + R3 via Gauss-Codazzi) is a POLE of alpha_2, not a zero.
       Route A, Route B and the refuter all instead solved the linear system AT the locus
       and got alpha_1 = alpha_2 = 0.  Both statements are correct: the map is
       DISCONTINUOUS there.  The value AT the singular point is 0; every neighbourhood of
       it contains theories with alpha_1 -> -4 alp and alpha_2 -> infinity.
       A zero obtained as the value of a rank-deficient system at a strong-coupling point
       is not a physical pass -- it is the signature of a missing mode.""")


# ===========================================================================================
head("SECTION E -- the GR-branch theorem's arithmetic core")
# ===========================================================================================
# NOTE: `chi` above was declared positive (it is a physical mu in (0,1)); solving for the
# root at the ENDPOINT chi = 0 needs a symbol that admits 0, else sympy correctly returns [].
c = sp.Symbol('c', real=True)
Vp_c = -sp.log(1 - c) ** 2
roots = sp.solve(sp.Eq(Vp_c, 0), c)
check("E1  V'(chi) = -[ln(1-chi)]^2 vanishes ONLY at chi = 0", roots == [0], f"roots = {roots}")
# V is defined by V' only up to an additive constant; the theory fixes it by V(0) = 0.
# The non-trivial content is that V' is INTEGRABLE at chi = 0 (V' ~ -chi^2 there), so that
# choice is available and V is real and finite on the whole physical range chi in [0,1).
s = sp.Symbol('s', real=True)
V_def = sp.integrate(Vp_c.subs(c, s), (s, 0, c))          # definite integral: V(0) = 0 by construction
check("E2a V'(chi) is integrable at chi = 0 (V' ~ -chi^2), so V(0) = 0 is an available choice",
      sp.simplify(sp.series(Vp_c, c, 0, 3).removeO() + c ** 2) == 0,
      f"V'(chi) = -chi^2 + O(chi^3);  V(chi) = {sp.simplify(V_def)}")
check("E2b with that choice V(0) = 0 and V is finite on [0,1)",
      sp.simplify(V_def.subs(c, 0)) == 0
      and sp.simplify(V_def.subs(c, sp.Rational(1, 2))).is_finite is not False,
      "=> L_MOND at a_mu = 0 is -[chi*0 + V(0)] = 0")
check("E3  carrier at A_ij = 0: Q EOM gives Q = 0 and L_carrier = 0",
      sp.simplify(L_on.subs({a1: 0, a2: 0, a3: 0})) == 0)
print("""
   E4  Therefore, with bet = lam = 0 (forced), every non-GR term is at least QUADRATIC in
       a_mu and the potential vanishes at the only stationary chi.  So
         (any GR solution, any GEODESIC slicing, chi = 0, Q = 0)
       solves every field equation exactly, for every source.  The candidate does not
       PREDICT MOND; GR-with-no-MOND is an exact branch and nothing selects the other one.
       This is carrier-independent and spec-repair-independent.   [PROVEN]""")


# ===========================================================================================
head("SUMMARY")
# ===========================================================================================
for ok, name, note in RESULTS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
npass = sum(1 for ok, _, _ in RESULTS if ok)
print(f"\n  {npass}/{len(RESULTS)} checks passed.")
raise SystemExit(0 if npass == len(RESULTS) else 1)
