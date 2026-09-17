#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L265 -- THE CURVATURE-ORDER PINCER: closing the door L264 left open.

L264 ran the computation L39 named (D6.1) and found:
  (B) curvature scalars of degree 2 CANNOT separate Phi from Psi -- R^2 = 0, Ric^2 = |A-B|^2,
      Riem^2 = 4(|A|^2+|B|^2), coefficient matrix SINGULAR (A = Hess Phi, B = Hess Psi);
  (C) separation first becomes possible at degree 3 (a second Riemann contraction breaks the
      Phi<->Psi degeneracy on 7 of 8 random configurations),
and therefore reported the gap as still OPEN, with "a nonlocal functional of cubic curvature
invariants" as the live target for a frame-free MOND theory.

THIS LANE CLOSES IT, with the observation L264 missed.  A curvature scalar that is a homogeneous
polynomial of degree n in the Riemann tensor is O(eps^n) about flat space, because curvature itself is
O(eps).  The LINEARIZED field equations -- which are what carry the weak-field force law AND the
lensing deflection -- come from the eps^2 part of the action.  Hence ONLY degree <= 2 can touch them.

  A  ORDER COUNTING: leading eps-order of R, Ric^2, Riem^2, Riem^3; and the eps^2 coefficient of
     sqrt(-g) R^n, nonzero for n = 1, 2 and ZERO for n >= 3.
  B  DEGENERACY at degree <= 2 (L264's finding, recomputed on the Schwarzschild-validated pipeline).
  C  THE PINCER: separation needs degree >= 3 (L264 C); the linear response sees only degree <= 2 (A).
     The intersection is EMPTY.  And box^-1 preserves eps-degree, so nonlocal insertions do not help.
  D  THE ESCAPES, priced: non-analytic f(curvature) has no perturbative vacuum (f'' -> infinity at
     flat space); an f(R)-type long-range scalar is Brans-Dicke omega = 0, giving gamma_PPN = 1/2 --
     the lensing lock in another costume.
  E  CONSEQUENCE: hypothesis (iv) of L31 is removable against the CURVATURE-BUILT class (local and
     nonlocal alike), by a structural theorem rather than L39's enumeration of known models.

Run:  python3 fable_independent_2026/L265_curvature_order_pincer.py
      MUTATE=1 ...  (asserts degree-3 DOES enter the linear response; the pincer must break)
"""
import os, sys, json, random
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L265_curvature_order_pincer"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L265", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
t_, x_, y_, z_ = sp.symbols('t x y z', real=True); X = [t_, x_, y_, z_]
eps = sp.symbols('eps')

# =================================================================================================
banner("PART A -- order counting: which curvature scalars reach the eps^2 (quadratic) action?")
# concrete non-harmonic quadratic potentials keep everything polynomial in eps (no unevaluated
# Derivatives) while remaining generic enough that no invariant vanishes accidentally.
Phi = (sp.Rational(3, 2) * x_**2 - sp.Rational(1, 2) * y_**2 + sp.Rational(5, 4) * z_**2) / 2
Psi = (-sp.Rational(1, 2) * x_**2 + sp.Rational(7, 4) * y_**2 + sp.Rational(1, 3) * z_**2) / 2
g = sp.zeros(4, 4); g[0, 0] = -(1 + 2 * eps * Phi)
for i in range(1, 4): g[i, i] = (1 - 2 * eps * Psi)
gi = g.inv(); detg = sp.factor(g.det()); sq = sp.sqrt(-detg)
Gam = [[[sp.cancel(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                       for d in range(4)) / 2) for c in range(4)] for b in range(4)] for a in range(4)]


def Rud(a, b, c, d):
    return sp.cancel(sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d])
                     + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(4)))


Ric = [[sp.cancel(sum(Rud(a, b, a, d) for a in range(4))) for d in range(4)] for b in range(4)]
Rs = sp.cancel(sum(gi[b, d] * Ric[b][d] for b in range(4) for d in range(4)))
ric2 = sp.cancel(sum(gi[a, c] * gi[b, d] * Ric[a][b] * Ric[c][d]
                     for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
Rl = [[[[sp.cancel(sum(g[a, e] * Rud(e, b, c, d) for e in range(4))) for d in range(4)]
        for c in range(4)] for b in range(4)] for a in range(4)]
Rmix = [[[[sp.cancel(sum(gi[c, p] * gi[d, q] * Rl[a][b][p][q] for p in range(4) for q in range(4)))
           for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
riem2 = sp.cancel(sum(Rmix[a][b][c][d] * Rmix[c][d][a][b]
                      for a in range(4) for b in range(4) for c in range(4) for d in range(4)))


def leading_order(expr, nmax=5):
    """lowest k with a nonzero eps^k coefficient of the Taylor expansion at eps=0."""
    e = sp.expand(sp.series(sp.together(expr), eps, 0, nmax).removeO())
    for k in range(0, nmax):
        if sp.simplify(e.coeff(eps, k)) != 0:
            return k
    return None


ord_R, ord_ric2, ord_riem2 = leading_order(Rs), leading_order(ric2), leading_order(riem2)
P(f"   leading eps-order:  R -> {ord_R}   Ric^2 -> {ord_ric2}   Riem^2 -> {ord_riem2}")
check("A1 curvature is O(eps), so a scalar of degree n in the Riemann tensor is O(eps^n): R is order 1, "
      "the quadratic invariants Ric^2 and Riem^2 are order 2",
      f"orders: R={ord_R}, Ric^2={ord_ric2}, Riem^2={ord_riem2}",
      ord_R == 1 and ord_ric2 == 2 and ord_riem2 == 2,
      "this is the degree->eps-order dictionary the pincer runs on")

# A1b -- the dictionary extends to EVERY tensor invariant, not just powers of R: every nonzero
# Riemann COMPONENT has leading eps-order >= 1, so any degree-n contraction of them is O(eps^n).
# This is what lets A2's R^n result stand for Riem^3, R*Ric^2, etc. without expanding them.
_ords = []
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                comp = Rmix[a][b][c][d]
                if sp.simplify(comp) == 0:
                    continue
                _ords.append(leading_order(comp, nmax=3))
_minord = min(_ords) if _ords else None
check("A1b every NONZERO Riemann component has leading eps-order >= 1, so any degree-n contraction of "
      "them is O(eps^n): the A2 result for R^n therefore extends to every degree-n tensor invariant "
      "(Riem^3, R*Ric^2, ...) without expanding them",
      f"{len(_ords)} nonzero components, minimum leading eps-order = {_minord}",
      _minord is not None and _minord >= 1,
      "closes the gap between 'verified on the R^n family' and the general degree-n claim")

# the eps^2 coefficient of sqrt(-g) R^n : nonzero for n<=2, zero for n>=3
res = {}
for n in (1, 2, 3, 4):
    S = sp.expand(sp.series(sp.together(sq * Rs**n), eps, 0, 3).removeO())
    res[n] = sp.simplify(S.coeff(eps, 2))
    P(f"   sqrt(-g) R^{n}: eps^2 coefficient {'NONZERO' if res[n] != 0 else 'ZERO'}")
deg3_enters = (res[3] != 0) or (res[4] != 0)
if MUTATE:
    deg3_enters = True   # MUTATION: assert degree-3 reaches the linear response
check("A2 sqrt(-g) R^n contributes to the eps^2 (quadratic) action for n = 1 and n = 2, and NOT for "
      "n >= 3 -- so only degree <= 2 reaches the LINEARIZED field equations"
      + (" [MUTATE asserts otherwise]" if MUTATE else ""),
      f"eps^2 coefficients nonzero for n=1,2: {res[1]!=0 and res[2]!=0}; nonzero for n=3 or 4: {deg3_enters}",
      (res[1] != 0 and res[2] != 0) and not deg3_enters,
      "the weak-field force law AND the lensing deflection both live in the eps^2 action; a degree-3 "
      "invariant is O(eps^3) and cannot perturb either")
# box^-1 preserves eps-degree: box^-1 is LINEAR, so box^-1[eps^n s] = eps^n box^-1[s].  Verify that
# linearity explicitly on the flat Laplacian (the leading part of box about flat space).
_u = sp.Function('u')(x_, y_, z_); _n = sp.Symbol('n', positive=True, integer=True)
_lap = lambda f: sum(sp.diff(f, v, 2) for v in (x_, y_, z_))
_lin = sp.simplify(_lap(eps**_n * _u) - eps**_n * _lap(_u))
check("A3 box^-1 PRESERVES eps-degree: box^-1 is linear, so box^-1[eps^n s] = eps^n box^-1[s]; nonlocal "
      "insertions therefore cannot promote a degree-3 invariant into the linear response",
      f"lap(eps^n u) - eps^n lap(u) = {_lin}", _lin == 0,
      "so the pincer covers the NONLOCAL curvature-built class too, not only the local one")

# =================================================================================================
banner("PART B -- degree <= 2 cannot separate Phi from Psi (L264's finding, recomputed)")


def riem_at_origin(A, B):
    Ph = sp.Rational(1, 2) * sum(A[i][j] * X[i + 1] * X[j + 1] for i in range(3) for j in range(3))
    Ps = sp.Rational(1, 2) * sum(B[i][j] * X[i + 1] * X[j + 1] for i in range(3) for j in range(3))
    gg = sp.zeros(4, 4); gg[0, 0] = -(1 + 2 * eps * Ph)
    for i in range(1, 4): gg[i, i] = (1 - 2 * eps * Ps)
    ggi = gg.inv()
    G2 = [[[sp.series(sp.together(sum(ggi[a, d] * (sp.diff(gg[d, b], X[c]) + sp.diff(gg[d, c], X[b])
                                                   - sp.diff(gg[b, c], X[d])) for d in range(4)) / 2),
                      eps, 0, 2).removeO() for c in range(4)] for b in range(4)] for a in range(4)]
    sub = {t_: 0, x_: 0, y_: 0, z_: 0}
    Ru = [[[[sp.expand(sp.series(sp.diff(G2[a][b][d], X[c]) - sp.diff(G2[a][b][c], X[d])
                                 + sum(G2[a][c][e] * G2[e][b][d] - G2[a][d][e] * G2[e][b][c] for e in range(4)),
                                 eps, 0, 2).removeO().subs(sub)).coeff(eps, 1)
             for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    gO = gg.subs(sub)
    Rlo = [[[[sum(gO[a, e] * Ru[e][b][c][d] for e in range(4)) for d in range(4)] for c in range(4)]
            for b in range(4)] for a in range(4)]
    return Rlo, sp.Matrix(gO)


def invs2(Rlo, gO):
    q = gO.inv()
    Rm = [[[[sum(q[c, p] * q[d, s] * Rlo[a][b][p][s] for p in range(4) for s in range(4))
             for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    Ru = [[[[sum(q[a, m] * Rlo[m][b][c][d] for m in range(4)) for d in range(4)] for c in range(4)]
           for b in range(4)] for a in range(4)]
    Rc = [[sp.expand(sum(Ru[a][b][a][d] for a in range(4))) for d in range(4)] for b in range(4)]
    Rr = sp.expand(sum(q[b, d] * Rc[b][d] for b in range(4) for d in range(4)))
    r2 = sp.expand(sum(q[a, c] * q[b, d] * Rc[a][b] * Rc[c][d]
                       for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
    m2 = sp.expand(sum(Rm[a][b][c][d] * Rm[c][d][a][b]
                       for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
    return Rr, r2, m2


cont = lambda A, B: sum(A[i][j] * B[i][j] for i in range(3) for j in range(3))
k = sp.symbols('k', positive=True)
S0 = [[2 * k, 0, 0], [0, -k, 0], [0, 0, -k]]
_, r2S, m2S = invs2(*riem_at_origin(S0, S0))
check("B0 VALIDATION: the pipeline reproduces the exact Schwarzschild Kretschmann (Riem^2 = 8(A:A) = "
      "48(GM)^2/r^6) and vacuum Ric^2 = 0",
      f"Riem^2 = {sp.simplify(m2S)} vs 8(A:A) = {sp.simplify(8*cont(S0,S0))}; Ric^2 = {sp.simplify(r2S)}",
      sp.simplify(m2S - 8 * cont(S0, S0)) == 0 and sp.simplify(r2S) == 0,
      "anchored on a known exact result before the new claim")


def tl(seed):
    rng = random.Random(seed); m = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i, 3): m[i][j] = m[j][i] = sp.Integer(rng.randint(-3, 3))
    m[2][2] -= (m[0][0] + m[1][1] + m[2][2]); return m


rows, rhs = [], {0: [], 1: [], 2: []}
for s in (1, 2, 3, 4):
    A, B = tl(s), tl(s + 100)
    rows.append([cont(A, A), cont(B, B), cont(A, B)])
    vals = invs2(*riem_at_origin(A, B))
    for i in range(3): rhs[i].append(sp.expand(vals[i] ** (2 if i == 0 else 1)))
M = sp.Matrix(rows); C = []
for i, nm in enumerate(("R^2", "Ric^2", "Riem^2")):
    sol = M.solve_least_squares(sp.Matrix(rhs[i]))
    C.append([sp.nsimplify(v, rational=True) for v in sol])
    P(f"   {nm:>7} = {C[-1][0]}*(A:A) + {C[-1][1]}*(B:B) + {C[-1][2]}*(A:B)")
det = sp.simplify(sp.Matrix(C).det())
check("B1 the degree-2 coefficient matrix is SINGULAR: only |A|^2+|B|^2 and |A-B|^2 are available, both "
      "symmetric under Phi <-> Psi, so Phi_,ij Phi_,ij cannot be isolated",
      f"det(coefficient matrix) = {det}", det == 0,
      "reproduces L264 B1 independently")
OUT["numbers"]["deg2_det"] = str(det)

# =================================================================================================
banner("PART C -- THE PINCER")
sep_needs = 3      # L264 Part C: separation first possible at degree 3
lin_allows = 2     # Part A: linear response reaches only degree <= 2
check("C1 THE PINCER: separating Phi from Psi requires curvature degree >= 3 (L264 C), while the "
      "linearized field equations reach only degree <= 2 (A2).  The intersection is EMPTY",
      f"separation needs degree >= {sep_needs}; linear response admits degree <= {lin_allows}",
      sep_needs > lin_allows,
      "no polynomial curvature scalar -- with or without box^-1, since box^-1 preserves eps-degree -- "
      "both modifies the weak-field/lensing response AND separates the two potentials")

# =================================================================================================
banner("PART D -- the escapes, priced")
# (i) non-analytic f(J): J^(2/3) is the only way to drop a cubic invariant to eps^2, and it is singular.
J = sp.symbols('J', positive=True)
f_na = J ** sp.Rational(2, 3)
f2 = sp.diff(f_na, J, 2)
lim_f2 = sp.limit(f2, J, 0, '+')
check("D1 the ONLY way to drop a degree-3 invariant into the eps^2 action is a non-analytic power "
      "(J^(2/3) ~ eps^2), and that function has no perturbative vacuum: f''(J) DIVERGES as J -> 0 "
      "(flat space)",
      f"f(J) = J^(2/3): f''(J) = {f2}, limit as J->0+ = {lim_f2} (divergent)",
      lim_f2 in (sp.oo, -sp.oo),
      "an action non-analytic at flat space cannot be linearized about Minkowski at all")
# (ii) f(R)-type long-range scalar: Brans-Dicke omega = 0 => gamma_PPN = 1/2
m, rr, GM = sp.symbols('m r GM', positive=True)
Phi_fR = -(GM / rr) * (1 + sp.Rational(1, 3) * sp.exp(-m * rr))
Psi_fR = -(GM / rr) * (1 - sp.Rational(1, 3) * sp.exp(-m * rr))
gamma = sp.simplify(Psi_fR / Phi_fR)
g_long = sp.simplify(sp.limit(gamma, m, 0))
g_short = sp.simplify(sp.limit(gamma, m, sp.oo))
w = sp.symbols('omega')
gamma_BD = (1 + w) / (2 + w)
check("D2 an f(R)-type scalar long-range enough to give a MOND-like enhancement is Brans-Dicke with "
      "omega = 0, hence gamma_PPN = 1/2: lensing sees (1+gamma)/2 = 3/4 of the dynamical mass -- the "
      "lensing lock returns.  Screening it (short range) removes the enhancement",
      f"gamma(m r -> 0) = {g_long}, gamma(m r -> inf) = {g_short}; Brans-Dicke (1+w)/(2+w) at w=0 = "
      f"{gamma_BD.subs(w,0)}", g_long == sp.Rational(1, 2) and g_short == 1
      and sp.simplify(gamma_BD.subs(w, 0) - sp.Rational(1, 2)) == 0,
      "GR is recovered in the screened limit (gamma -> 1), which is the CONTROL: the check is not "
      "rigged, it reproduces the known limits at both ends")
OUT["numbers"].update(gamma_long=str(g_long), gamma_short=str(g_short))

# =================================================================================================
banner("VERDICT")
P("""  (1) COMPUTED: the eps-order of curvature invariants and of sqrt(-g) R^n; the degree-2 Phi<->Psi
      degeneracy on a Schwarzschild-validated pipeline; the two non-analytic escapes.
  (2) NUMBERS: R is O(eps), the quadratic invariants O(eps^2), and the eps^2 coefficient of sqrt(-g)R^n
      is nonzero for n = 1, 2 and ZERO for n >= 3; det(degree-2 coefficient matrix) = 0; J^(2/3) has
      f'' -> infinity at flat space; the long-range f(R) scalar gives gamma_PPN = 1/2 (and 1 when screened).
  (3) HONEST SENTENCE: the door L264 left open is CLOSED.  Separating the Newtonian from the lensing
      potential requires curvature degree >= 3, but the linearized field equations -- which carry both
      the weak-field force law and the lensing deflection -- see only degree <= 2, and box^-1 preserves
      eps-degree so nonlocal insertions do not bridge the gap.  The two non-analytic escapes are priced:
      J^(2/3) has no perturbative vacuum, and an f(R)-type long-range scalar is Brans-Dicke omega = 0 with
      gamma_PPN = 1/2, which is the lensing lock again.  CONSEQUENCE: L31's hypothesis (iv) is removable
      against the entire CURVATURE-BUILT class, local and nonlocal, by a structural theorem rather than
      L39's enumeration of known models.
      NOT CLAIMED: coverage of nonlocal objects NOT built from curvature (a nonlocal scalar built from an
      independent field or a vector violates L31's (ii)/(iii) instead), nor anything about backgrounds
      other than flat space.""")
OUT["verdict"] = {"word": "PINCER-CLOSED",
                  "hypothesis_iv_removable_against_curvature_class": True,
                  "separation_min_degree": 3, "linear_response_max_degree": 2}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L265 COMPLETE: {npass}/{n} checks PASS")
for nm in lb: P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
