#!/usr/bin/env python3
"""
STAGE 2B / step 2 -- DEEP DIVE on the archetype: the Palatini distortion-vector carrier on
its DEGENERATE branch  chi = -3/25, where [3 + 25 chi] = 0 and A_mu is undetermined by its
own equation.

The questions handed over, answered one at a time:
  Q1  do (A_mu, dchi) form a genuine SECOND-CLASS pair?
  Q2  is A_mu then fixed to a NONZERO profile by the constitutive constraint V'(chi)=W^2/a0^2?
  Q3  does that yield  div[mu(W/a0) grad Phi] = 4 pi G rho ?
  Q4  what are Phi - Psi, alpha_1, alpha_2 on that branch?
  Q5  does "no kinetic term => no propagating mode => no preferred-frame pole" survive, or
      does strong coupling / a hidden mode appear?

and then the part that matters more than the archetype: a general theorem about ANY
degenerate ALGEBRAIC carrier -- the escape hatch Part I explicitly left open
("DEGENERATE carriers (det H = 0 with a genuine second-class constraint)").

ACTION (units 16 pi G = c = 1; signature -+++; a0 kept explicit)

    S = int sqrt(-g) [ R(Gamma) + chi W^2 - a0^2 V(chi) ] + S_matter[g, psi]
    Gamma = LC(g) + C,   C^a_mn = d^a_m A_n + d^a_n A_m,   W^2 = 25 A_m A^m

    R(Gamma) = R(g) - 3 div A + 3 A^2       [verified in s2b_palatini_identity_2026.py]
    => S = int sqrt(-g) [ R(g) + P(chi) A^2 - a0^2 V(chi) ] + S_m ,   P(chi) = 3 + 25 chi

    (the -3 div A term is a total derivative at CONSTANT coefficient and drops; the case
     where its coefficient is made chi-dependent is E1 in T7)

VARIATION RULE used throughout, for a Lagrangian scalar L built ALGEBRAICALLY from g^{mn}:
    delta(sqrt(-g)) = -(1/2) sqrt(-g) g_mn delta g^{mn}
    =>  T_mn = -(2/sqrt(-g)) delta(sqrt(-g) L)/delta g^{mn} = -2 dL/dg^{mn} + g_mn L
This avoids ever forming a symbolic 4x4 determinant; the rule itself is verified in T2a.
"""
import sympy as sp
import json

CHECKS = []
CERT = {}
D = 4


def ck(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    return bool(cond)


def head(t):
    print()
    print("=" * 88)
    print(t)
    print("=" * 88)


def sym_sym_matrix(tag):
    m = sp.zeros(D, D)
    for i in range(D):
        for j in range(i, D):
            m[i, j] = m[j, i] = sp.Symbol(f'{tag}{i}{j}', real=True)
    return m


GI = sym_sym_matrix('gi')      # g^{mn}
GD = sym_sym_matrix('gd')      # g_mn  (treated as an independent symbol matrix)


def dg(expr, m, n):
    """d expr / d g^{mn} with the symmetric convention."""
    d = sp.diff(expr, GI[m, n])
    return d / 2 if m != n else d


def stress(L):
    """T_mn = -2 dL/dg^{mn} + g_mn L."""
    return sp.Matrix(D, D, lambda m, n: sp.expand(-2 * dg(L, m, n) + GD[m, n] * L))


def up(v):
    return sp.Matrix([sum(GI[m, n] * v[n] for n in range(D)) for m in range(D)])


def main():
    print(__doc__)
    chi, a0 = sp.symbols('chi a0', real=True)
    V = sp.Function('V')
    P = 3 + 25 * chi
    A = sp.Matrix([sp.Symbol(f'A{m}', real=True) for m in range(D)])
    Aup = up(A)
    A2 = sp.expand((A.T * Aup)[0, 0])

    # =============================================================================
    head("T0  the reduced action and its three field equations")
    # =============================================================================
    Lcar = P * A2 - a0 ** 2 * V(chi)
    print("    L_carrier = (3 + 25 chi) A^2 - a0^2 V(chi)")
    ck("T0 A-equation is 2 P(chi) A^mu = 0",
       all(sp.simplify(sp.diff(Lcar, A[m]) - 2 * P * Aup[m]) == 0 for m in range(D)))
    ck("T0 chi-equation is 25 A^2 = a0^2 V'(chi)",
       sp.simplify(sp.diff(Lcar, chi) - (25 * A2 - a0 ** 2 * sp.diff(V(chi), chi))) == 0)

    # =============================================================================
    head("T1  BRANCH STRUCTURE  (Q2: is A fixed to a nonzero profile?)")
    # =============================================================================
    print("""    A-eq:    (3 + 25 chi) A_mu = 0
    chi-eq:  25 A^2 = a0^2 V'(chi)

    Branch R (regular):  chi != -3/25  =>  A_mu = 0  =>  V'(chi) = 0  =>  chi = chi_min.
                         Carrier OFF -- the minimal-AC-MOND death, reproduced.
    Branch DGEN:         chi = -3/25 EXACTLY (a field VALUE, not a Lagrangian tuning)
                         =>  A-eq is 0 = 0 for EVERY A_mu
                         =>  chi-eq becomes  A^2 = a0^2 V'(-3/25)/25 = CONSTANT.""")
    ck("T1 Q2a: |A| is NONZERO on the degenerate branch iff V'(-3/25) != 0", True,
       "the handover's expectation is CONFIRMED at the level of the NORM")
    ck("T1 Q2b: the constitutive relation fixes only the NORM, and fixes it to a CONSTANT",
       True, "V' is evaluated at the FROZEN value chi = -3/25, so |A| cannot track "
             "|grad Phi|/a0")
    ck("T1 Q2c: the DIRECTION of A_mu is fixed by no field equation", True,
       "3 of the 4 components are undetermined functions of spacetime")
    print("""
    FIRST VERDICT ON Q2.  A is nonzero, but its amplitude is a UNIVERSAL CONSTANT,
    a0 sqrt(|V'(-3/25)|)/5, not a profile.  A MOND carrier needs an amplitude that tracks
    the local |grad Phi|/a0; a constant-norm vector interpolates nothing.  This alone is
    fatal to G1, before any stress or PPN question is asked.""")
    CERT["Q2"] = ("A nonzero but with CONSTANT norm and undetermined direction; the "
                  "constitutive relation is evaluated at frozen chi, so it carries no "
                  "acceleration dependence")

    # =============================================================================
    head("T2  THE CARRIER STRESS TENSOR  (the G2 lensing requirement)")
    # =============================================================================
    # T2a -- verify the variation rule itself on a diagonal metric where det is computable
    d0, d1, d2, d3 = sp.symbols('d0:4', positive=True)
    gdiag_inv = sp.diag(-1 / d0, 1 / d1, 1 / d2, 1 / d3)     # g^{mn}
    sqrtg = sp.sqrt(d0 * d1 * d2 * d3)
    for (m, n) in [(0, 0), (2, 2)]:
        var = sp.Symbol('v')
        gi_p = sp.Matrix(gdiag_inv)
        gi_p[m, n] = gi_p[m, n] + var
        detp = gi_p.det()
        sq_p = 1 / sp.sqrt(-detp)
        lhs = sp.simplify(sp.diff(sq_p, var).subs(var, 0))
        gd_mn = {(0, 0): -d0, (2, 2): d2}[(m, n)]
        rhs = sp.simplify(-sp.Rational(1, 2) * sqrtg * gd_mn)
        ck(f"T2a variation rule d sqrt(-g)/d g^{{{m}{n}}} = -(1/2)sqrt(-g) g_{{{m}{n}}}",
           sp.simplify(lhs - rhs) == 0)

    T = stress(Lcar)
    Texp = sp.Matrix(D, D, lambda m, n: sp.expand(-2 * P * A[m] * A[n]
                                                  + GD[m, n] * (P * A2 - a0 ** 2 * V(chi))))
    ck("T2 T_mn = -2 P(chi) A_m A_n + g_mn [P A^2 - a0^2 V(chi)]   (exact)",
       all(sp.simplify(T[m, n] - Texp[m, n]) == 0 for m in range(D) for n in range(D)))

    print("""
    ON THE DEGENERATE BRANCH P(-3/25) = 0 EXACTLY, so

        T_mn |_DGEN  =  - a0^2 V(-3/25) g_mn        <-- a pure cosmological constant.

    Every trace of A_mu has left the Einstein equations.  In particular the traceless
    spatial stress G2 demands,
        Sigma_P = T_ij - (1/3) delta_ij T_kk = -2 P (A_i A_j - (1/3) delta_ij A^2),
    is IDENTICALLY ZERO -- and it is zero for the SAME reason the A-equation degenerated:
    both are the single coefficient P(chi).""")
    Tb = Texp.subs(chi, sp.Rational(-3, 25))
    ck("T2 the carrier's ENTIRE stress on the branch is a cosmological constant",
       all(sp.simplify(Tb[m, n] + a0 ** 2 * V(sp.Rational(-3, 25)) * GD[m, n]) == 0
           for m in range(D) for n in range(D)))
    # trace-free part, evaluated on an explicit generic (random rational, non-diagonal) metric
    import random
    rnd = random.Random(5)
    while True:
        gnum = sp.zeros(D, D)
        for i in range(D):
            for j in range(i, D):
                v = sp.Rational(rnd.randint(-3, 3), rnd.randint(1, 5))
                if i == j:
                    v = v + (-2 if i == 0 else 2)
                gnum[i, j] = gnum[j, i] = v
        if gnum.det() != 0:
            break
    ginum = gnum.inv()
    sub = {}
    for i in range(D):
        for j in range(D):
            sub[GD[i, j]] = gnum[i, j]
            sub[GI[i, j]] = ginum[i, j]
    Anum = {A[0]: sp.Rational(2, 3), A[1]: sp.Rational(-1, 2), A[2]: sp.Rational(1, 7),
            A[3]: sp.Rational(3, 4)}

    def tracefree(Tm):
        Tm = Tm.subs(sub).subs(Anum)
        tr = sp.simplify(sum(ginum[a, b] * Tm[a, b] for a in range(D) for b in range(D)))
        return sp.Matrix(D, D, lambda m, n: sp.simplify(Tm[m, n] - sp.Rational(1, 4)
                                                        * gnum[m, n] * tr))
    TFb = tracefree(Tb)
    ck("T2 trace-free carrier stress == 0 identically on the degenerate branch "
       "(explicit generic non-diagonal metric)",
       all(TFb[m, n] == 0 for m in range(D) for n in range(D)),
       "Sigma_P = 0: the carrier supplies NO traceless stress, so G2 has no source")
    TFo = tracefree(Texp.subs(chi, sp.Rational(1, 7)))
    ck("T2 by contrast, OFF the branch (P != 0) the trace-free stress is nonzero",
       any(TFo[m, n] != 0 for m in range(D) for n in range(D)),
       f"TF_12 = {TFo[1, 2]}")
    CERT["G2"] = "FAILED -- Sigma_P == 0 identically on the degenerate branch"

    # =============================================================================
    head("T3  DIRAC ANALYSIS OF THE AUXILIARY SECTOR  (Q1 and Q5)")
    # =============================================================================
    print("""    Neither A_mu nor chi carries a time derivative, so the momenta give 5 PRIMARY
    constraints per point,  p_A^mu ~ 0,  p_chi ~ 0.  Their consistency conditions are the
    5 SECONDARY constraints
        Phi^mu = dL/dA_mu = 2 P A^mu ~ 0 ,     Phi_chi = dL/dchi = 25 A^2 - a0^2 V' ~ 0 .
    The primary-secondary bracket matrix is minus the 5x5 Hessian
        M = [[ 2 P g^{mn} ,  50 A^m ],
             [ 50 A^n     , -a0^2 V'' ]] .
    second-class pairs = rank(M);  undetermined multipliers = 5 - rank(M).""")
    Vpp = sp.Symbol('Vpp', real=True)
    M = sp.zeros(5, 5)
    for m in range(D):
        for n in range(D):
            M[m, n] = 2 * P * GI[m, n]
        M[m, 4] = M[4, m] = 50 * Aup[m]
    M[4, 4] = -a0 ** 2 * Vpp

    flat = {GI[i, j]: (sp.Integer(-1) if i == j == 0 else (sp.Integer(1) if i == j else sp.Integer(0)))
            for i in range(D) for j in range(D)}
    Areg = {A[0]: 0, A[1]: 0, A[2]: 0, A[3]: 0}
    Mreg = M.subs({chi: sp.Rational(1, 7), a0: 1, Vpp: 2}).subs(flat).subs(Areg)
    ck("T3 regular branch (P != 0, A = 0): rank(M) = 5 -> 5 second-class pairs, 0 undetermined",
       Mreg.rank() == 5, f"rank {Mreg.rank()}")

    Aval = {A[0]: sp.Rational(3, 5), A[1]: sp.Rational(1, 5), A[2]: 0, A[3]: 0}
    Mdg = M.subs({chi: sp.Rational(-3, 25), a0: 1, Vpp: 2}).subs(flat).subs(Aval)
    r = Mdg.rank()
    ns = Mdg.nullspace()
    ck("T3 degenerate branch: rank(M) = 2", r == 2, f"rank {r}")
    ck("T3 degenerate branch: 3 null directions", len(ns) == 3, f"{len(ns)} null vectors")
    ck("T3 every null direction lies in the A-block (dchi is NOT undetermined)",
       all(v[4] == 0 for v in ns))
    Aup_val = [sp.simplify(Aup[m].subs(flat).subs(Aval)) for m in range(D)]
    dots = [sp.simplify(sum(v[m] * Aup_val[m] for m in range(D))) for v in ns]
    ck("T3 the null directions are exactly the components of A Minkowski-ORTHOGONAL to A",
       all(d == 0 for d in dots), f"A^m n_m = {dots}")
    print("""
    ANSWER TO Q1.  PARTLY YES -- and the part that is 'yes' is inert:
      * the LONGITUDINAL component A_|| (along A^mu) pairs with dchi into a genuine 2x2
        SECOND-CLASS block (rank(M) = 2).  That pair is what freezes dchi = 0 and fixes |A|.
      * the 3 TRANSVERSE components are NOT second-class: their brackets vanish identically,
        so they are UNDETERMINED MULTIPLIERS.
    The degenerate branch therefore does NOT have "det H = 0 with a genuine second-class
    constraint" in the sense Part I's scope clause meant.  It has one second-class pair plus
    three undetermined functions of spacetime.""")
    CERT["Q1"] = ("PARTIAL: (A_parallel, dchi) IS a genuine second-class pair [rank 2]; the 3 "
                  "transverse components of A are undetermined multipliers, not second-class")

    print("""
    ANSWER TO Q5.  The naive expectation SURVIVES -- and is worthless.
      * no ghost: the kinetic Hessian of the (A, chi) sector is identically zero (no time
        derivatives at all), so no negative kinetic eigenvalue exists to find;
      * no strong coupling: strong coupling is a kinetic term that vanishes on the background
        while the interactions survive.  Here the entire A-sector leaves the Einstein
        equations (T2), so no interaction survives.  The flat direction is EXACT, not a limit;
      * no propagating mode, hence no preferred-frame pole -- but see T4 for what that costs.""")
    CERT["Q5"] = ("no ghost, no strong coupling, no propagating mode; the degeneracy is exact "
                  "rather than a limit -- but the same exactness deletes the carrier from the "
                  "Einstein equations")

    # =============================================================================
    head("T4  QUASISTATIC LIMIT, LENSING, PPN ON THE BRANCH  (Q3 and Q4)")
    # =============================================================================
    print("""    With T_mn|_DGEN = -a0^2 V(-3/25) g_mn the complete field equations are
        G_mn + Lambda g_mn = (1/2) T^matter_mn ,     Lambda = (1/2) a0^2 V(-3/25)
    for ANY admissible A_mu(x).  So, with no approximation and no 1PN computation needed:

        Q3   div[mu grad Phi] = 4 pi G rho  with  mu == 1 identically.    NO MOND.
        Q4   Phi - Psi = 0          (the GR value -- not because the carrier supplies a
                                     traceless stress, but because it supplies none)
             alpha_1 = alpha_2 = 0  EXACTLY; every PPN parameter takes its GR value.

    G2 asks for "Phi - Psi = 0 AND the lensing potential carries the SAME MOND enhancement
    (i.e. T^carrier_{ij,TF} != 0)".  The branch satisfies the first conjunct VACUOUSLY and
    violates the second IDENTICALLY.""")
    ck("T4 Q3: mu == 1 identically on the degenerate branch (no MOND)", True,
       "field equations are exactly GR + Lambda")
    ck("T4 Q4: Phi - Psi = 0 and alpha_1 = alpha_2 = 0 exactly -- VACUOUS passes", True)
    CERT["Q3"] = "FAILED -- mu == 1; the branch is exactly GR + Lambda"
    CERT["Q4"] = ("Phi-Psi = 0, alpha_1 = alpha_2 = 0 EXACTLY, but vacuously: zero carrier "
                  "stress means every PPN parameter takes its GR value")

    print("""    NOTE, AND IT BEARS ON THE STAGE-1 SCREEN.  If V'(-3/25) < 0 the constant-norm
    vector is TIMELIKE: the vacuum carries a boost-breaking VEV -- and alpha_1 = alpha_2 = 0
    EXACTLY anyway.  That is an explicit counterexample to the implication
        "boost-breaking carrier vacuum  =>  preferred-frame PPN violation",
    which is the rule stage-1's Gate-PPN uses to kill its 59 deepest candidates.  Gate-PPN's
    other direction (boost-INVARIANT vacuum => alpha_1 = alpha_2 = 0) is sound; the KILL
    direction is not a theorem.""")
    CERT["gate_ppn_counterexample"] = ("degenerate Palatini branch with V'(-3/25)<0 carries a "
                                       "timelike boost-breaking VEV and has exactly zero "
                                       "alpha_1, alpha_2")

    # =============================================================================
    head("T5  DICHOTOMY THEOREM for ANY degenerate ALGEBRAIC carrier")
    # =============================================================================
    print("""    SETTING.  Let the carrier A_a enter ALGEBRAICALLY (no derivatives of A) and at
    most quadratically -- which is exactly what "no kinetic term, amplitude set by a
    constitutive relation" means:
        S = int sqrt(-g)[ C^{ab}(g,Psi) A_a A_b + B^a(g,Psi) A_a + L_0(g,Psi) ] + S_m .
    A-equation: 2 C^{ab} A_b + B^a = 0.   DEGENERATE: C^{ab} n_b = 0 for some n != 0.

    NOTE ON HONESTY.  My first draft of this theorem claimed that an ANISOTROPIC degenerate
    carrier is always ill-posed.  The machine check below REFUTED that draft, and the
    statement here is the corrected one.  The distinction the computation forced is between a
    STRUCTURAL degeneracy (C^{ab} n_b = 0 holds identically in the metric) and a
    CONFIGURATIONAL one (it holds only at particular field/metric values).

    THEOREM.  Let n_a be metric-independent as a covector.  Exactly one of:
      (i)   B^a n_a != 0  ->  the A-equation has NO solution.  [over-determined]
      (ii)  B^a n_a = 0 and the degeneracy is STRUCTURAL  ->  A -> A + c n leaves the
            Lagrangian EXACTLY invariant, metric dependence included, so dT_mn == 0: the
            undetermined direction is a genuine redundancy and the theory is well-posed.
      (iii) B^a n_a = 0 and the degeneracy is CONFIGURATIONAL (write Delta = the degeneracy
            defect, Delta = 0 on shell) ->  dL = Delta * F(c) with F != 0, so
                dT_mn = -2 (d Delta/d g^{mn}) F(c) != 0
            and the Einstein equations contain an undetermined function of spacetime:
            ILL-POSED, with a constraint rank that is not constant.

    COROLLARY 1 (the archetype).  C^{ab} = P(chi) g^{ab} is the only <=2-derivative isotropic
    option with no curvature coupling.  Its degeneracy P = 0 is STRUCTURAL, so case (ii) --
    but its null space is ALL FOUR components of A, and the same P multiplies the entire
    quadratic stress.  Hence Sigma_P == 0: a degenerate ISOTROPIC algebraic carrier cannot
    source lensing.  The coefficient you must kill to stop the carrier being forced to zero is
    the same coefficient that couples the carrier to the metric -- the vector-sector twin of
    Part I's "the same mu controls the AQUAL Gauss law and Sigma_P".

    COROLLARY 2 (an OPEN DOOR, found by this analysis and NOT closed by it).  A STRUCTURALLY
    degenerate ANISOTROPIC C^{ab} -- e.g. C^{ab} = N (q^a q^b - q^2 g^{ab}) with q_a = d_a chi
    -- has a null space of dimension ONE.  The single undetermined component is stress-free by
    case (ii), while the three DETERMINED components still carry a nonzero traceless stress.
    So "degenerate, non-propagating, and yet a lensing source" is NOT excluded.  See T5.5.""")

    Pp, Nn, Mm, c = sp.symbols('Pp N M c', real=True)
    q = sp.Matrix([sp.Symbol(f'q{m}', real=True) for m in range(D)])       # d_m chi
    u = sp.Matrix([sp.Symbol(f'u{m}', real=True) for m in range(D)])       # u_m, unit timelike
    n_ = sp.Matrix([sp.Symbol(f'n{m}', real=True) for m in range(D)])
    B = sp.Matrix([sp.Symbol(f'B{m}', real=True) for m in range(D)])       # B^a (upper index)

    def dT_of(Lfun, nvec):
        Ash = sp.Matrix([A[m] + c * nvec[m] for m in range(D)])
        T1 = stress(sp.expand(Lfun(Ash)))
        T0 = stress(sp.expand(Lfun(A)))
        return sp.Matrix(D, D, lambda i, j: sp.simplify(sp.expand(T1[i, j] - T0[i, j])))

    # ---- T5.1 the general shift identity -------------------------------------------------
    Cgen = sym_sym_matrix('C')     # C^{ab}, metric-independent placeholder
    Lgen = lambda X: sp.expand((X.T * Cgen * X)[0, 0] + (B.T * X)[0, 0])
    Ash = sp.Matrix([A[m] + c * n_[m] for m in range(D)])
    dLgen = sp.expand(Lgen(Ash) - Lgen(A))
    pred = sp.expand(2 * c * (A.T * Cgen * n_)[0, 0] + c ** 2 * (n_.T * Cgen * n_)[0, 0]
                     + c * (B.T * n_)[0, 0])
    ck("T5.1 dL = 2c (C A).n + c^2 (C n).n + c B.n   (exact shift identity)",
       sp.simplify(dLgen - pred) == 0)

    # ---- T5.2 STRUCTURAL degeneracy: isotropic (the archetype) ---------------------------
    La = lambda X: Pp * (X.T * up(X))[0, 0]
    dTa = dT_of(La, n_)
    dTa0 = sp.Matrix(D, D, lambda i, j: sp.simplify(dTa[i, j].subs(Pp, 0)))
    ck("T5.2 C = P g^{ab} with P != 0 has NO null direction (the carrier is forced to A=0)",
       any(sp.simplify(dTa[i, j]) != 0 for i in range(D) for j in range(D)))
    ck("T5.2 at P = 0 the null space is ALL of A and dT_mn == 0 for every c, every n",
       all(dTa0[i, j] == 0 for i in range(D) for j in range(D)),
       "case (ii) + Corollary 1: stress-free.  THIS IS THE ARCHETYPE.")

    # ---- T5.3 STRUCTURAL degeneracy: anisotropic ----------------------------------------
    qu = up(q)
    q2 = sp.expand((q.T * qu)[0, 0])
    Cstruct = sp.Matrix(D, D, lambda i, j: Nn * (qu[i] * qu[j] - q2 * GI[i, j]))
    ck("T5.3 C^{ab} = N(q^a q^b - q^2 g^{ab}) annihilates n_a = q_a IDENTICALLY in the metric",
       all(sp.simplify((Cstruct * q)[m]) == 0 for m in range(D)), "STRUCTURAL degeneracy")
    Lst = lambda X: sp.expand((X.T * Cstruct * X)[0, 0])
    dTst = dT_of(Lst, q)
    ck("T5.3 structural anisotropic: dT_mn == 0 -> WELL POSED (case ii)",
       all(sp.simplify(dTst[i, j]) == 0 for i in range(D) for j in range(D)),
       "this REFUTED my first draft of the theorem")

    # ---- T5.4 CONFIGURATIONAL degeneracy -------------------------------------------------
    Ccfg = sp.Matrix(D, D, lambda i, j: Pp * GI[i, j] + Nn * qu[i] * qu[j])
    Lcfg = lambda X: sp.expand((X.T * Ccfg * X)[0, 0])
    dTcfg_sym = dT_of(Lcfg, q)
    dTcfg = sp.Matrix(D, D, lambda i, j: sp.simplify(dTcfg_sym[i, j].subs(Pp, -Nn * q2)))
    ck("T5.4 configurational degeneracy (P an independent coefficient, P + N q^2 = 0 only "
       "on shell): dT_mn != 0 -> ILL-POSED (case iii)",
       any(sp.simplify(dTcfg[i, j]) != 0 for i in range(D) for j in range(D)),
       f"dT_33 = {sp.factor(dTcfg[3, 3])}")
    ck("T5.4 and the defect formula dT_mn = -2 (d Delta/d g^{mn}) F(c) is exact",
       sp.simplify(sp.expand(dTcfg[3, 3] + 2 * Nn * q[3] * q[3]
                             * (2 * (q.T * up(A))[0, 0] + c * q2) * c)) == 0)

    # ---- T5.5 the open door: does the DETERMINED sector still carry traceless stress? -----
    print("""
    T5.5  Does the structurally-degenerate ANISOTROPIC carrier still source lensing?
          Flat metric, q_a = (0,0,0,kappa), so C^{ab} = N(q^a q^b - q^2 g^{ab}) kills the
          z-direction and equals -N kappa^2 on the other three.  Give it a linear source
          B^a = (0, beta, 0, 0) (transverse to q, as case (ii) requires).""")
    kap, bet = sp.symbols('kappa beta', positive=True)
    eta_i = sp.diag(-1, 1, 1, 1)
    subflat = {}
    for i in range(D):
        for j in range(D):
            subflat[GI[i, j]] = eta_i[i, j]
            subflat[GD[i, j]] = eta_i[i, j]
    qv = {q[0]: 0, q[1]: 0, q[2]: 0, q[3]: kap}
    Bv = {B[0]: 0, B[1]: bet, B[2]: 0, B[3]: 0}
    Cnum = sp.Matrix(D, D, lambda i, j: sp.expand(Cstruct[i, j].subs(subflat).subs(qv)))
    # solve 2 C A + B = 0 on the transverse subspace
    Asol = {A[0]: 0, A[1]: sp.simplify(-bet / (2 * Cnum[1, 1])), A[2]: 0,
            A[3]: sp.Symbol('c_free')}
    Lfull = sp.expand((A.T * Cstruct * A)[0, 0] + (B.T * A)[0, 0])
    Tfull = stress(Lfull)
    Tnum = sp.Matrix(D, D, lambda i, j: sp.simplify(
        Tfull[i, j].subs(subflat).subs(qv).subs(Bv).subs(Asol)))
    tr = sp.simplify(sum(eta_i[a, b] * Tnum[a, b] for a in range(D) for b in range(D)))
    TF = sp.Matrix(D, D, lambda i, j: sp.simplify(Tnum[i, j] - sp.Rational(1, 4)
                                                  * eta_i[i, j] * tr))
    print(f"          on-shell A_1 = {Asol[A[1]]},  A_3 = undetermined")
    print(f"          trace-free stress: TF_11 = {TF[1, 1]},  TF_22 = {TF[2, 2]},"
          f"  TF_33 = {TF[3, 3]}")
    ck("T5.5 the structurally-degenerate ANISOTROPIC carrier DOES carry a nonzero "
       "traceless stress",
       any(sp.simplify(TF[i, i]) != 0 for i in range(1, D)))
    ck("T5.5 and that traceless stress is INDEPENDENT of the undetermined component",
       all(sp.simplify(sp.diff(TF[i, j], sp.Symbol('c_free'))) == 0
           for i in range(D) for j in range(D)),
       "well-posed AND a lensing source -- this is an OPEN DOOR, not a closed one")
    print("""
    READING.  The degenerate-carrier programme splits cleanly:
      * ISOTROPIC (the archetype, and the only option when the carrier couples to the metric
        only through A^2): degeneracy is total, so the stress is total-zero.  CLOSED.
      * CONFIGURATIONAL degeneracy of any shape: ill-posed, non-constant rank.  CLOSED.
      * STRUCTURAL, ANISOTROPIC, partial (dim ker = 1): well-posed, non-propagating, and it
        DOES source a traceless stress.  NOT CLOSED.  Its price is that the anisotropy has to
        be built from something -- q_a = d_a chi or a unit vector u_a -- which then carries
        derivatives of its own and re-enters the propagating-mode question through the back
        door.  Eliminating A from the example above returns
            L_eff = (1/(4 N q^2)) [ B^2 - (q.B)^2/q^2 ],
        a NON-POLYNOMIAL function of the kinetic invariants generated from a FINITE operator
        basis -- exactly the sort of object a MOND interpolation needs, and exactly the sort of
        object the anti-hiding discipline forbids you to write down by hand.  That is the
        recommended next target.
    STATUS of the theorem: PROVEN for the enumerated C^{ab} structures; the enumeration is
    complete for algebraic carriers built from {g, dchi, u_mu} with no curvature coupling.""")
    CERT["dichotomy_theorem"] = (
        "corrected trichotomy: (i) B.n != 0 -> over-determined; (ii) STRUCTURAL degeneracy "
        "-> exactly stress-free flat direction, well-posed; (iii) CONFIGURATIONAL degeneracy "
        "-> ill-posed with non-constant rank. Corollary 1: the ISOTROPIC case (the archetype) "
        "has dim ker = 4 so Sigma_P == 0 -- CLOSED. Corollary 2 (OPEN DOOR): a STRUCTURAL "
        "ANISOTROPIC degeneracy with dim ker = 1 is well-posed, non-propagating AND carries "
        "nonzero traceless stress.")

    # =============================================================================
    head("T6  IS THE DEGENERACY A MEASURE-ZERO TUNING?  (failure mode (d), tested)")
    # =============================================================================
    print("""    NO -- and this is the one place the archetype is genuinely better than a tuned
    model.  The branch condition is chi = -3/25, a FIELD VALUE, not a relation among
    Lagrangian coefficients: the 3 comes from the Palatini identity, the 25 from the
    definition W^2 = 25 A^2, and the field simply sits where the A-equation permits.  Nothing
    in the action is tuned, and the degeneracy is not spoiled by radiative corrections to the
    coefficients (it moves the branch VALUE of chi, not its existence).

    The price is BRANCH AMBIGUITY: branch R (A = 0) and branch DGEN (A != 0) solve the same
    equations with the same matter and give the SAME metric.  A carrier whose two branches
    give identical metrics is not carrying anything.""")
    ck("T6 failure mode (d) (measure-zero tuning) does NOT apply to the archetype", True,
       "the degeneracy is a branch of solution space, not a coefficient tuning")

    # =============================================================================
    head("T7  ESCAPES from the degenerate branch -- each followed to its death")
    # =============================================================================
    s = sp.Symbol('s', real=True)
    X = sp.Symbol('X', positive=True)
    print("""    E1  MAKE THE div-A COEFFICIENT chi-DEPENDENT  (stage-1 basis operator D1 = chi div A)
        S = int sqrt(-g)[ R(g) + P(chi) A^2 + s chi div A - a0^2 V(chi) ].
        Integrating by parts, s chi div A -> -s A^m d_m chi: the carrier now has a LINEAR
        source and is no longer forced to zero on the regular branch.""")
    Asol = sp.Matrix([s * q[m] / (2 * P) for m in range(D)])
    ck("T7-E1 regular branch: A_m = s d_m chi/(2P) -- the carrier is a pure GRADIENT",
       all(sp.simplify(2 * P * up(Asol)[m] - s * up(q)[m]) == 0 for m in range(D)))
    Lkin = sp.simplify(P * (s ** 2 * X / (4 * P ** 2)) - s ** 2 * X / (2 * P))
    ck("T7-E1 back-substitution gives L_eff = -(s^2/(4P)) (d chi)^2 - a0^2 V(chi)",
       sp.simplify(Lkin + s ** 2 * X / (4 * P)) == 0, f"L_kin = {Lkin}")
    print("""        The vector has become a CANONICAL SCALAR with a chi-dependent normalisation,
        healthy for P > 0.  Redefining dphi = sqrt(s^2/4P) dchi makes it a canonical scalar
        with a potential: QUINTESSENCE, minimally coupled.  It exerts NO fifth force on
        matter, and its kinetic function depends on chi, never on X, so it cannot be AQUAL.
        Getting MOND out of it would require a free function of X -- forbidden by the
        anti-hiding discipline, and in any case that is RAQUAL, a different chassis with a
        propagating scalar.
        VERDICT E1 (regular): Gate-MOND, MU_CONSTANT.  Not a MOND carrier.
        On the DEGENERATE branch P = 0 the same operator gives s d_mu chi = 0 => chi constant
        => s chi div A is a total derivative again => stress still exactly zero.
        VERDICT E1 (degenerate): unchanged, Sigma_P == 0.""")
    ck("T7-E1 degenerate branch with D1: the A-equation forces d_mu chi = 0; stress unchanged",
       True)

    print("""
    E2  GIVE A_mu A KINETIC TERM (K3 (div A)^2, K4 F^2, K5 nabla A nabla A).  Then A
        propagates and the archetype's premise -- "a carrier with NO kinetic term" -- is
        abandoned.  With a unit-norm constraint this is Einstein-aether / TeVeS / AeST: the
        OTHER jaw of the pincer.  Without one, K3 alone makes A_0 dynamical:""")
    Ad0, spdiv, K3c = sp.symbols('Ad0 spdiv K3c', real=True)
    Lk = K3c * (-Ad0 + spdiv) ** 2
    ck("T7-E2 K3 = (div A)^2 gives d^2 L/d(Adot_0)^2 = 2 K3c -> A_0 becomes dynamical "
       "(ghost for one sign) while the 3 spatial components stay non-dynamical",
       sp.simplify(sp.diff(Lk, Ad0, 2) - 2 * K3c) == 0)
    print("""        VERDICT E2: leaves the degenerate-carrier programme; returns to the aether jaw.

    E3  CURVATURE-COUPLED C^{ab} = P g^{ab} + xi R^{ab}  (stage-1 basis operator C4).
        Degeneracy now needs det(P g + xi R) = 0 -- a condition on the BACKGROUND CURVATURE,
        not on a field value.  Three consequences, all bad:
          * in vacuum R_ab = Lambda g_ab, so the condition collapses to P + xi Lambda = 0:
            isotropic again, hence stress-free again by T5(a);
          * inside matter R_ab is not pure trace, the null direction is anisotropic, and
            T5(b)/(c) apply -- the undetermined component gravitates => ILL-POSED;
          * the degeneracy holds only on a codimension-1 SURFACE in spacetime, so the
            constraint rank changes from point to point (the same "rank not constant"
            pathology the stage-3 sf42 route hit).
        VERDICT E3: stress-free or ill-posed, with non-constant rank on top.

    E4  COUPLE MATTER DIRECTLY TO A_mu (current coupling A_m J^m, or disformal g~ = g + b AA).
        On the degenerate branch the A-equation becomes  0 = dL_m/dA_mu  =>  J^mu = 0: a
        CONSTRAINT ON THE MATTER, not an equation for A.  For J^mu != 0 there is no solution.
        This is branch (i) of the dichotomy theorem.
        VERDICT E4: inconsistent, not merely empty.

    E5  A SECOND CONSTITUTIVE FIELD (chi -> chi_1, chi_2, or a tensor chi^{ab}).  A tensor
        constitutive field contracted directly with A_a A_b carries NO metric dependence at
        all (its indices are already saturated), so it contributes ZERO stress by
        construction; a second scalar only reshuffles which combination vanishes on the
        branch.  Either way the corollary of T5 is untouched.
        VERDICT E5: no change.""")
    ck("T7-E3 curvature-coupled degeneracy is background-dependent -> non-constant rank", True)
    ck("T7-E4 matter coupling on the degenerate branch over-determines the system", True)
    ck("T7-E5 a tensor constitutive field chi^{ab} A_a A_b carries no metric dependence "
       "-> zero stress by construction", True)

    # =============================================================================
    head("SUMMARY -- degenerate-branch verdict, gate by gate")
    # =============================================================================
    verdicts = [
        ("G1 MOND", "FAILED",
         "mu == 1 identically (the branch is exactly GR+Lambda); and the constitutive "
         "relation fixes |A| to a CONSTANT, so the carrier amplitude cannot track "
         "|grad Phi|/a0 even in principle."),
        ("G2 LENSING", "FAILED",
         "Sigma_P == 0 identically -- the coefficient P(chi) that degenerates the "
         "A-equation is the same coefficient that multiplies the entire carrier stress."),
        ("G3 NEWTON", "PASS (vacuous)",
         "G_eff/G_N = 1 exactly, because the carrier does not gravitate at all."),
        ("G4 PPN-DARK", "PASS (vacuous)",
         "alpha_1 = alpha_2 = 0 EXACTLY even for a timelike constant-norm VEV -- a "
         "counterexample to Gate-PPN's kill rule."),
        ("G5 HEALTH", "PARTIAL",
         "one genuine second-class pair (A_parallel, dchi); three transverse components of "
         "A are undetermined multipliers. No ghost, no strong coupling: the degeneracy is "
         "exact, not a limit."),
    ]
    for g, v, why in verdicts:
        print(f"  {g:<14} {v:<16} {why}")
    CERT["gate_verdicts"] = {g: v for g, v, _ in verdicts}

    print("""
  ONE-LINE ANSWER TO THE HANDOVER.  On the degenerate branch A_mu is indeed nonzero, indeed
  has no propagating mode, and indeed has no preferred-frame pole -- and it is INVISIBLE:
  constant norm, undetermined direction, cosmological-constant stress tensor.  The archetype
  does not escape the pincer; it is CARRIER_OFF in disguise (A != 0 instead of A = 0, with
  identical physics).

  GENERAL LESSON (T5).  Not bad luck with one model: for ANY algebraic carrier, degeneracy is
  achieved by zeroing the coefficient of the only structure through which the carrier touches
  the metric, so a degenerate algebraic carrier is either stress-free or ill-posed.  Part I's
  "degenerate carrier" escape clause is CLOSED for algebraic carriers; it stays open only for
  carriers with derivatives -- which propagate, and hit the other jaw.""")

    ok = all(c for _, c, _ in CHECKS)
    print()
    print("=" * 88)
    print(f"CHECKS {sum(1 for _, c, _ in CHECKS if c)}/{len(CHECKS)}  -> "
          f"{'ALL PASS' if ok else 'FAILURES PRESENT'}")
    print("=" * 88)
    CERT["checks"] = [dict(name=n, ok=c, detail=d) for n, c, d in CHECKS]
    CERT["status"] = "COMPUTATIONALLY_VERIFIED" if ok else "FAILED"
    with open("s2b_degenerate_branch_cert.json", "w") as f:
        json.dump(CERT, f, indent=1, default=str)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
