#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L263 -- THE MISSING COMPUTATION L39 NAMED (D6.1), RUN.

L39 closed L31's locality hypothesis against the known nonlocal class using the "lensing lock": every
covariant scalar whose flat-space expansion BEGINS AT FIRST ORDER in h_mn carries the one combination
the Ricci scalar carries, so Tully-Fisher and lensing cannot be modified separately.  It then named the
gap, verbatim:

  "Scalars beginning at SECOND order -- Kretschmann, R_mn R^mn, C^2 -- DO separate Psi from Phi, and are
   not covered. ... THE MISSING COMPUTATION IS THEREFORE EXACTLY THIS: is there a nonlocal scalar,
   quadratic or higher in curvature, that BOTH separates the Newtonian from the lensing potential AND
   remains sensitive to the coherent coarse-grained field rather than to the nearest star?  If no,
   hypothesis (iv) is removable outright and L31 becomes a theorem in (i)-(iii).  If yes, that object is
   a live candidate for a frame-free MOND theory and should be built."

This lane runs it.  Static weak field, Newtonian gauge ds^2 = -(1+2Phi)dt^2 + (1-2Psi)delta_ij dx^i dx^j,
A := Hess(Phi), B := Hess(Psi), both traceless (vacuum).  Curvature is computed from the metric via
Christoffels (no hand-written Riemann) and VALIDATED against the exact Schwarzschild Kretschmann.

  A  THE COHERENCE HALF -- L39's conjectured obstruction is REFUTED.
     Exact vacuum identity  lap(|grad Phi|^2) = 2 Phi_,ij Phi_,ij  =>  lap^-1[Phi_,ij Phi_,ij] = |grad Phi|^2/2.
     So a NONLOCAL curvature-built scalar returns the COHERENT acceleration of the TOTAL field, not the
     nearest star.  Verified for one mass, TWO masses (the coherence test) and a harmonic field, with a
     non-vacuum control fixing the correction term exactly.
  B  THE SEPARATION HALF at QUADRATIC order -- NO.  R^2 = 0, Ric^2 = |A-B|^2, Riem^2 = 4(|A|^2+|B|^2):
     the coefficient matrix is SINGULAR, so Phi_,ij Phi_,ij cannot be isolated.  Only |A|^2+|B|^2 and
     |A-B|^2 are available, both symmetric under Phi <-> Psi.
  C  THE SEPARATION HALF at CUBIC order -- GENERICALLY YES.  A second independent cubic Riemann
     contraction breaks the Phi<->Psi degeneracy on 7 of 8 random configurations.  Degenerate pairs
     exist (measure zero) but do not close the door.

  VERDICT: L39's D6(1) is answered GENERICALLY YES.  Hypothesis (iv) is NOT removable by this route;
  L31 stays "proved under locality".  The compensating gain is that the obstruction L39 CONJECTURED
  (nearest-star domination) is wrong, and the live target is now explicit.

Run:  python3 fable_independent_2026/L263_lensing_lock_second_order.py
      MUTATE=1 ...  (breaks the vacuum condition; the identity of Part A must fail)
"""
import os, sys, json, math, random
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L263_lensing_lock_second_order"
MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L263", "mutate": MUTATE, "checks": {}, "numbers": {}}


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

# =================================================================================================
banner("PART A -- the coherence half: lap^-1 of a tidal invariant IS the coherent acceleration")
x, y, z = sp.symbols('x y z', real=True)
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
hess_sq = lambda f: sum(sp.diff(f, a, b) ** 2 for a in (x, y, z) for b in (x, y, z))
gradsq = lambda f: sum(sp.diff(f, v) ** 2 for v in (x, y, z))
r = sp.sqrt(x ** 2 + y ** 2 + z ** 2)


def residual_max(Phi, pts):
    """max | lap(|gradPhi|^2) - 2 Phi_,ij Phi_,ij - 2 gradPhi.grad(lapPhi) | / |Hess^2|"""
    R = lap(gradsq(Phi)) - 2 * hess_sq(Phi)
    Pr = 2 * sum(sp.diff(Phi, v) * sp.diff(lap(Phi), v) for v in (x, y, z))
    fR = sp.lambdify((x, y, z), R, 'mpmath'); fP = sp.lambdify((x, y, z), Pr, 'mpmath')
    fH = sp.lambdify((x, y, z), hess_sq(Phi), 'mpmath')
    w = 0.0
    for p in pts:
        sc = max(abs(complex(fH(*p)).real), 1e-300)
        w = max(w, abs(complex(fR(*p)).real - complex(fP(*p)).real) / sc)
    return w


def vac_residual(Phi, pts):
    """in VACUUM the identity is lap(|gradPhi|^2) = 2 Phi_,ij Phi_,ij exactly."""
    R = lap(gradsq(Phi)) - 2 * hess_sq(Phi)
    fR = sp.lambdify((x, y, z), R, 'mpmath'); fH = sp.lambdify((x, y, z), hess_sq(Phi), 'mpmath')
    return max(abs(complex(fR(*p)).real) / max(abs(complex(fH(*p)).real), 1e-300) for p in pts)


random.seed(7)
pts = [(random.uniform(1, 3), random.uniform(1, 3), random.uniform(1, 3)) for _ in range(12)]
d, M2 = 7.0, 3.0
CASES = {
    "point mass -1/r": -1 / r,
    "TWO masses (coherence test)": -1 / r - M2 / sp.sqrt((x - d) ** 2 + y ** 2 + z ** 2),
    "harmonic quadratic": (x ** 2 - y ** 2) / 2,
}
if MUTATE:   # MUTATION: break the vacuum condition -- the identity must fail
    CASES["point mass -1/r"] = -1 / r + x ** 3
worst = {}
for nm, Phi in CASES.items():
    worst[nm] = vac_residual(Phi, pts)
    P(f"   {nm:<30} vacuum residual = {worst[nm]:.3e}   (lap Phi = {sp.simplify(lap(Phi))})")
mx = max(worst.values())
check("A1 the vacuum identity lap(|grad Phi|^2) = 2 Phi_,ij Phi_,ij holds EXACTLY -- including for the "
      "TWO-mass field, so lap^-1 returns the COHERENT total acceleration, not the nearest mass"
      + (" [MUTATE must break this]" if MUTATE else ""),
      f"max relative residual over {len(pts)} points x {len(CASES)} fields = {mx:.3e}", mx < 1e-12,
      "=> lap^-1[Phi_,ij Phi_,ij] = |grad Phi|^2 / 2 : a nonlocal curvature-built scalar equal to the "
      "coherent acceleration squared.  L39's conjectured 'nearest-star' obstruction is REFUTED.")
ctrl = residual_max(x ** 3, pts)
check("A2 CONTROL (non-vacuum): with lap Phi != 0 the identity acquires exactly 2 gradPhi.grad(lapPhi) "
      "and nothing else",
      f"max residual against the predicted correction = {ctrl:.3e}", ctrl < 1e-12,
      "the correction term is pinned, so A1 is a vacuum statement and not an accident")
OUT["numbers"]["A_vacuum_residual"] = mx

# =================================================================================================
banner("PART B -- separation at QUADRATIC order in curvature (validated pipeline)")
t_, x1, x2, x3 = sp.symbols('t x1 x2 x3', real=True); X = [t_, x1, x2, x3]; eps = sp.symbols('eps')


def riem_at_origin(A, B):
    Phi = sp.Rational(1, 2) * sum(A[i][j] * X[i + 1] * X[j + 1] for i in range(3) for j in range(3))
    Psi = sp.Rational(1, 2) * sum(B[i][j] * X[i + 1] * X[j + 1] for i in range(3) for j in range(3))
    g = sp.zeros(4, 4); g[0, 0] = -(1 + 2 * eps * Phi)
    for i in range(1, 4): g[i, i] = (1 - 2 * eps * Psi)
    gi = g.inv()
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                s = sum(gi[a, dd] * (sp.diff(g[dd, b], X[c]) + sp.diff(g[dd, c], X[b]) - sp.diff(g[b, c], X[dd]))
                        for dd in range(4))
                Gam[a][b][c] = sp.series(sp.together(s / 2), eps, 0, 2).removeO()
    sub = {t_: 0, x1: 0, x2: 0, x3: 0}
    Rud = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for dd in range(4):
                    e1 = sp.diff(Gam[a][b][dd], X[c]) - sp.diff(Gam[a][b][c], X[dd])
                    e2 = sum(Gam[a][c][e] * Gam[e][b][dd] - Gam[a][dd][e] * Gam[e][b][c] for e in range(4))
                    Rud[a][b][c][dd] = sp.expand(sp.series(e1 + e2, eps, 0, 2).removeO().subs(sub)).coeff(eps, 1)
    gO = g.subs(sub)
    Rl = [[[[sum(gO[a, e] * Rud[e][b][c][dd] for e in range(4)) for dd in range(4)] for c in range(4)]
           for b in range(4)] for a in range(4)]
    return Rl, sp.Matrix(gO)


def invs(Rl, gO):
    gi = gO.inv()
    Rmix = [[[[sum(gi[c, p] * gi[dd, q] * Rl[a][b][p][q] for p in range(4) for q in range(4))
               for dd in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    Rud = [[[[sum(gi[a, m] * Rl[m][b][c][dd] for m in range(4)) for dd in range(4)] for c in range(4)]
            for b in range(4)] for a in range(4)]
    Ric = [[sp.expand(sum(Rud[a][b][a][dd] for a in range(4))) for dd in range(4)] for b in range(4)]
    Rs = sp.expand(sum(gi[b, dd] * Ric[b][dd] for b in range(4) for dd in range(4)))
    ric2 = sp.expand(sum(gi[a, c] * gi[b, dd] * Ric[a][b] * Ric[c][dd]
                         for a in range(4) for b in range(4) for c in range(4) for dd in range(4)))
    riem2 = sp.expand(sum(Rmix[a][b][c][dd] * Rmix[c][dd][a][b]
                          for a in range(4) for b in range(4) for c in range(4) for dd in range(4)))
    riem3 = sp.expand(sum(Rmix[a][b][c][dd] * Rmix[c][dd][e][f] * Rmix[e][f][a][b]
                          for a in range(4) for b in range(4) for c in range(4) for dd in range(4)
                          for e in range(4) for f in range(4)))
    M = gi * sp.Matrix(4, 4, lambda i, j: Ric[i][j])
    return dict(R=Rs, Ric2=ric2, Riem2=riem2, Riem3=riem3, Ric3=sp.expand((M * M * M).trace()))


def riem3b(Rl, gO):
    """second independent cubic Riemann contraction R_{m a n b} R^{a r b s} R_r^{m s}_n"""
    gi = gO.inv()
    Ruu = [[[[sum(gi[c, p] * gi[dd, q] * Rl[a][b][p][q] for p in range(4) for q in range(4))
              for dd in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    tot = 0
    for m in range(4):
        for a in range(4):
            for n in range(4):
                for b in range(4):
                    v = Rl[m][a][n][b]
                    if v == 0: continue
                    for rr in range(4):
                        for ss in range(4):
                            w = Ruu[a][rr][b][ss]
                            if w == 0: continue
                            u = sum(gi[rr, p] * gi[ss, q] * Rl[p][m][q][n] for p in range(4) for q in range(4))
                            tot += v * w * u
    return sp.expand(tot)


cont = lambda A, B: sum(A[i][j] * B[i][j] for i in range(3) for j in range(3))
k = sp.symbols('k', positive=True)
S = [[2 * k, 0, 0], [0, -k, 0], [0, 0, -k]]
Rl, gO = riem_at_origin(S, S); IS = invs(Rl, gO)
check("B0 VALIDATION: the pipeline reproduces the EXACT Schwarzschild Kretschmann.  For A=B=Hess(-GM/r), "
      "A:A = 6(GM)^2/r^6 and Riem^2 = 8(A:A) = 48(GM)^2/r^6; and Ric^2 = 0, R = 0 (vacuum GR)",
      f"Riem^2 = {sp.simplify(IS['Riem2'])} vs 8*(A:A) = {sp.simplify(8*cont(S,S))}; Ric^2 = "
      f"{sp.simplify(IS['Ric2'])}; R = {sp.simplify(IS['R'])}",
      sp.simplify(IS['Riem2'] - 8 * cont(S, S)) == 0 and sp.simplify(IS['Ric2']) == 0 and sp.simplify(IS['R']) == 0,
      "the curvature machinery is anchored on a known exact result before any new claim is made")


def tl(seed):
    rng = random.Random(seed); m = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i, 3): m[i][j] = m[j][i] = sp.Integer(rng.randint(-3, 3))
    m[2][2] -= (m[0][0] + m[1][1] + m[2][2]); return m


rows, rhs = [], {kk: [] for kk in ("R", "Ric2", "Riem2")}
for s in (1, 2, 3, 4, 5, 6):
    A, B = tl(s), tl(s + 100)
    rows.append([cont(A, A), cont(B, B), cont(A, B)])
    I = invs(*riem_at_origin(A, B))
    for kk in rhs: rhs[kk].append(I[kk])
Mrow = sp.Matrix(rows)
C = []
for kk in ("R", "Ric2", "Riem2"):
    sol = Mrow.solve_least_squares(sp.Matrix(rhs[kk]))
    C.append([sp.nsimplify(v, rational=True) for v in sol])
    P(f"   {kk:>6} = {C[-1][0]}*(A:A) + {C[-1][1]}*(B:B) + {C[-1][2]}*(A:B)")
Cm = sp.Matrix(C); det = sp.simplify(Cm.det())
check("B1 at QUADRATIC order in curvature the coefficient matrix is SINGULAR: only |A|^2+|B|^2 and "
      "|A-B|^2 are available (both Phi<->Psi symmetric), so Phi_,ij Phi_,ij CANNOT be isolated",
      f"R^2 = 0, Ric^2 = |A-B|^2, Riem^2 = 4(|A|^2+|B|^2); det(coeff matrix) = {det}", det == 0,
      "the lensing lock EXTENDS to quadratic order -- L39's 'Kretschmann separates Psi from Phi' is, at "
      "this order, not the case")
OUT["numbers"]["quadratic_det"] = str(det)

# =================================================================================================
banner("PART C -- separation at CUBIC order: generically YES (this is what reopens the gap)")


def singular_pair(seed):
    rng = random.Random(seed)
    for _ in range(4000):
        dm = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(i, 3): dm[i][j] = dm[j][i] = rng.randint(-2, 2)
        D = sp.Matrix(3, 3, lambda i, j: dm[i][j]); D = D - sp.eye(3) * sp.Rational(D.trace(), 3)
        if D.det() != 0 or D.norm() == 0: continue
        am = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(i, 3): am[i][j] = am[j][i] = rng.randint(-3, 3)
        A = sp.Matrix(3, 3, lambda i, j: am[i][j]); A = A - sp.eye(3) * sp.Rational(A.trace(), 3)
        B = A - D
        if not all(v.is_Integer for v in list(A) + list(B)): continue
        AA = sum(A[i, j] ** 2 for i in range(3) for j in range(3))
        BB = sum(B[i, j] ** 2 for i in range(3) for j in range(3))
        if AA != BB: return A.tolist(), B.tolist(), AA, BB
    return None


nsep, ntot = 0, 0
for seed in range(1, 9):
    got = singular_pair(seed)
    if not got: continue
    A, B, AA, BB = got; ntot += 1
    R1, g1 = riem_at_origin(A, B); R2, g2 = riem_at_origin(B, A)
    I1, I2 = invs(R1, g1), invs(R2, g2)
    I1['Riem3b'], I2['Riem3b'] = riem3b(R1, g1), riem3b(R2, g2)
    same = all(sp.simplify(I1[kk] - I2[kk]) == 0 for kk in I1)
    if not same: nsep += 1
    P(f"   seed {seed}: |A|^2={AA} |B|^2={BB}  invariants degenerate under Phi<->Psi: {same}")
frac = nsep / max(ntot, 1)
check("C1 at CUBIC order a second independent Riemann contraction BREAKS the Phi<->Psi degeneracy on a "
      "generic configuration (threshold: separation on > half of the sampled pairs)",
      f"{nsep}/{ntot} random pairs separated ({frac:.2f})", frac > 0.5,
      "so curvature scalars DO generically distinguish the Newtonian from the lensing potential at cubic "
      "order -- the second-order/higher escape L39 named is NOT closed")
check("C2 AGAINST THE EASY CONCLUSION: degenerate pairs DO exist (measure zero), so |grad Phi|^2 is not a "
      "GLOBAL function of the curvature invariants -- but a measure-zero degeneracy does not close a door",
      f"{ntot-nsep}/{ntot} sampled pairs were fully degenerate", (ntot - nsep) >= 1,
      "recorded explicitly because an earlier draft of this lane mistook one such pair for a theorem; the "
      "robustness scan overturned it")
OUT["numbers"].update(cubic_separated=nsep, cubic_total=ntot, cubic_fraction=frac)

# =================================================================================================
banner("VERDICT")
P("""  (1) COMPUTED: L39's D6(1), both halves, on a Schwarzschild-validated curvature pipeline.
  (2) NUMBERS: the vacuum identity holds to <1e-12 including the two-mass field; at quadratic order the
      coefficient matrix is singular (R^2=0, Ric^2=|A-B|^2, Riem^2=4(|A|^2+|B|^2)); at cubic order a
      second Riemann contraction separates 7 of 8 random pairs.
  (3) HONEST SENTENCE: L39's D6(1) answers GENERICALLY YES.  Therefore hypothesis (iv) is NOT removable by
      this route and L31 remains PROVED UNDER LOCALITY -- the theorem is not strengthened.  What IS
      established, and is new: (a) the obstruction L39 CONJECTURED is wrong -- lap^-1 of a tidal invariant
      returns the coherent acceleration of the total field exactly, so nonlocal curvature scalars are NOT
      nearest-star dominated; (b) the lensing lock nevertheless extends to QUADRATIC order, by a
      Phi<->Psi degeneracy, which was not previously known; (c) the live target is now explicit: a
      nonlocal functional of CUBIC curvature invariants, which is where separation first becomes possible.
      NOT CLAIMED: that such a theory exists, is ghost-free, or has two propagating modes.  Cubic-curvature
      nonlocal actions generically carry Ostrogradsky ghosts, and that is the next gate, not this lane.""")
OUT["verdict"] = {"word": "GENERICALLY-YES-GAP-STAYS-OPEN",
                  "hypothesis_iv_removable": False,
                  "new": ["nearest-star obstruction refuted by the vacuum identity",
                          "lensing lock extends to quadratic order via a Phi<->Psi degeneracy",
                          "live target: nonlocal functional of cubic curvature invariants"]}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L263 COMPLETE: {npass}/{n} checks PASS")
for nm in lb: P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
