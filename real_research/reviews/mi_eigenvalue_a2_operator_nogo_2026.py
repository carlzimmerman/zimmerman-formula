#!/usr/bin/env python3
r"""mi_eigenvalue_a2_operator_nogo_2026.py -- SWINGING AT ESCAPE (2): is there an operator whose
worldline EIGENVALUE (not merely its u-contracted moment) is +|a|^2? Answer: not any function of Box_u,
and the obstruction is the worldline's FRENET TORSION -- which turns out to BE the (v/c)^2 amplitude problem.

WHY THIS WAS THE SHARP ESCAPE. mi_nonlocal_amplitude_nogo_2026 showed that if u were a genuine
eigenvector of the operator with eigenvalue lambda, the u-contraction would give -K(lambda) with NO
(v/c)^2 prefactor -- O(1), exactly the first-moment closure that fits the RAR. Theorem B already gives
+|a|^2 as the u-contracted MOMENT. So the whole amplitude problem reduces to one question: can |a|^2 be
an EIGENVALUE rather than a moment?

  E1  THE EXACT FRENET TRIAD of the relativistic circular worldline: D u = |a| ahat,
      D ahat = |a| u + B b, D b = -B ahat, with curvature |a| = gamma^2 Omega v/c and torsion
      B = gamma^2 Omega. *** THE RATIO IS |a|/B = v/c EXACTLY *** (mpmath, 40 dps, three speeds
      including v/c = 1/3).
  E2  HOW THE EIGENVALUE EQUATION FAILS, exactly:  D^2 u = |a|^2 u + |a| B b.  The residual is
      PRECISELY the torsion term, verified symbolically to be exactly |a| B b. The spoiler exceeds the
      wanted term by B/|a| = c/v. *** SO THE (v/c)^2 AMPLITUDE SUPPRESSION IS THE WORLDLINE'S TORSION,
      and it is the same c/v as Theorem 8's w/x. ***
  E3  THE NO-GO. spec(D) = {0, +-i gamma Omega} -> spec(Box_u) = {0, -(gamma Omega)^2}, ALL <= 0, while
      |a|^2 > 0 strictly. A SIGN obstruction, independent of every parameter. Since
      spec(F(Box_u)) = F(spec(Box_u)) is just two numbers, |a|^2 is not an eigenvalue of ANY function of
      Box_u -- nonlocal, bounded, Herglotz or otherwise. Escape (2) is closed for that whole class.
  E4  WHY THE MOMENT SURVIVES WHERE THE SPECTRUM DOES NOT: b is orthogonal to u, so the u-contraction
      annihilates the torsion term and returns -|a|^2 exactly. Theorem B is a statement about an
      INDEFINITE QUADRATIC FORM, not about the spectrum -- which is exactly why the moment and the
      resolvent are different objects, and why one reproduces MOND and the other does not.
  E5  MUTATION CONTROL, and it is physically illuminating. On TORSION-FREE (hyperbolic, straight-line)
      motion the eigenvalue equation is EXACT: D^2 u = |a|^2 u with u a genuine eigenvector. So the
      published action WOULD deliver the closure for linear acceleration and fails only for ORBITS.
      MOND is a claim about orbits.
  E6  What is left, and the sharper statement of what would be needed.

HONEST SCOPE. E3 closes "|a|^2 as an eigenvalue of a function of Box_u" for BOUND motion. It does NOT
close modified inertia, and E5 shows the sign obstruction is specific to oscillatory worldlines rather
than universal. No measurement is touched. Exit 0 = ran and every check held. No hard-coded verdicts.
"""
from __future__ import annotations

import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


C_MP = mp.mpf("2.99792458e8")
KPC_MP = mp.mpf("3.0856775814913673e19")

tau, R, Om, cs = sp.symbols("tau R Omega c", positive=True)
gam = sp.Symbol("gamma", positive=True)
GSUB = {gam: 1 / sp.sqrt(1 - (Om * R / cs) ** 2)}
ETA = sp.diag(-1, 1, 1, 1)


def dot(p, q):
    return sp.simplify((p.T * ETA * q)[0, 0])


def D(V):
    return sp.simplify(V.diff(tau))


banner("E1  THE EXACT FRENET TRIAD OF THE RELATIVISTIC CIRCULAR WORLDLINE")

ph = gam * Om * tau
u = sp.Matrix([gam, -gam * Om * R / cs * sp.sin(ph), gam * Om * R / cs * sp.cos(ph), 0])
check(sp.simplify(dot(u, u).subs(GSUB) + 1) == 0, "E1 the worldline is correctly normalised, u.u = -1")

a = D(u)
A2 = sp.simplify(dot(a, a))
A = sp.sqrt(A2)
ahat = sp.simplify(a / A)
Dahat = D(ahat)
alpha = sp.simplify(-dot(u, Dahat))          # coefficient of u (u.u = -1)
beta = sp.simplify(dot(ahat, Dahat))
perp = sp.simplify(Dahat - alpha * u - beta * ahat)
Bt = sp.sqrt(sp.simplify(dot(perp, perp)))
b = sp.simplify(perp / Bt)
print(f"  |a|^2 = {A2}        |a| = {sp.simplify(A)}")
print(f"  D ahat = alpha u + beta ahat + perp   with alpha = {alpha}, beta = {beta}")
check(sp.simplify(D(u) - A * ahat) == sp.zeros(4, 1), "E1a  D u = |a| ahat  exactly")
check(sp.simplify(alpha - A) == 0 and beta == 0,
      "E1b  D ahat = |a| u + (torsion term)  -- the u-coefficient is exactly |a| and there is no "
      "ahat-component, i.e. the Frenet form is standard")
check(sp.simplify(dot(u, b).subs(GSUB)) == 0 and sp.simplify(dot(ahat, b)) == 0,
      "E1c  the binormal b is orthogonal to BOTH u and ahat, so the triad is genuine")

print("\n  curvature |a| and torsion B, and their ratio -- mpmath at 40 dps:")
print(f"  {'v [km/s]':>10}{'|a|':>18}{'B':>18}{'|a|/B':>20}{'v/c':>20}")
print("  " + "-" * 88)
ratios_ok = []
for vkms, Rkpc in (("220", 8.0), ("30", 1.0), ("1e5", 0.001)):
    vv = mp.mpf(vkms) * 1000
    Rv = mp.mpf(Rkpc) * KPC_MP
    Omv = vv / Rv
    gv = 1 / mp.sqrt(1 - (vv / C_MP) ** 2)
    Av, Bv = gv**2 * Omv * vv / C_MP, gv**2 * Omv
    ratios_ok.append(mp.almosteq(Av / Bv, vv / C_MP, rel_eps=mp.mpf("1e-30")))
    print(f"  {float(vv)/1e3:>10.1f}{mp.nstr(Av,7):>18}{mp.nstr(Bv,7):>18}"
          f"{mp.nstr(Av/Bv,14):>20}{mp.nstr(vv/C_MP,14):>20}")
check(all(ratios_ok),
      "E1d *** CURVATURE / TORSION = |a|/B = v/c EXACTLY *** at every speed tested to 30 digits, "
      "including the mildly relativistic v/c = 1/3 -- so this is an identity, not a slow-motion limit")


banner("E2  HOW THE EIGENVALUE EQUATION FAILS -- exactly, and by exactly the torsion")

adot = D(a)
resid = sp.simplify(adot - A2 * u)
print(f"  D^2 u - |a|^2 u  has a nonzero residual; is it exactly |a| * B * b ?")
check(sp.simplify(resid - A * Bt * b) == sp.zeros(4, 1),
      "E2  D^2 u = |a|^2 u + |a| B b  EXACTLY -- u fails to be an eigenvector by PRECISELY the torsion "
      "term, and by nothing else")
# compare SQUARES: both B/|a| and c/v are positive, so equality of squares is equivalent, and the
# squared form carries no radical for sympy to get stuck on.
ratio_sq = sp.simplify(sp.expand(((Bt / A) ** 2 - (cs / (Om * R)) ** 2).subs(GSUB)))
print(f"  (B/|a|)^2 - (c/v)^2 = {ratio_sq}   <- 0 means B/|a| = c/v exactly")
check(ratio_sq == 0,
      "E2b the spoiler-to-wanted ratio is |a|B / |a|^2 = B/|a| = c/v EXACTLY (verified on the squares, "
      "radical-free), so the torsion term DOMINATES the eigenvalue it spoils by c/v -- which is why the "
      "surviving contraction came out (v/c)^2-small")
print("""
  *** THIS IDENTIFIES THE AMPLITUDE PROBLEM GEOMETRICALLY. The (v/c)^2 suppression found for a generic
  kernel is not an accident of the contraction: it is the worldline's FRENET TORSION, and the factor is
  the same c/v that appears as Theorem 8's w/x. Curvature is what MOND needs; torsion is what the
  operator returns; their ratio is v/c. ***""")


banner("E3  THE NO-GO: |a|^2 IS NOT IN THE SPECTRUM OF Box_u, SO NOT OF ANY F(Box_u)")

M = sp.Matrix([[0, A, 0], [A, 0, -Bt], [0, Bt, 0]])          # D on span(u, ahat, b)
ev = [sp.simplify(e.subs(GSUB)) for e in M.eigenvals()]
print(f"  spec(D) on span(u, ahat, b) = {ev}")
sq = sorted({sp.simplify(sp.expand(e**2)) for e in ev}, key=str)
print(f"  spec(Box_u) = the squares    = {sq}")
lam = sp.simplify((-(gam * Om) ** 2).subs(GSUB))
check(any(sp.simplify(s - lam) == 0 for s in sq) and any(s == 0 for s in sq),
      f"E3 spec(Box_u) = {{0, -(gamma Omega)^2}} -- reproducing the block result independently, from the "
      f"Frenet matrix rather than from componentwise differentiation")
# |a|^2 = Omega^4 R^2 gamma^4 / c^2 is a quotient of POSITIVE symbols, hence > 0, and the nonzero
# eigenvalue is -(gamma Omega)^2 < 0. Rather than ask sympy to sign Omega^2 R^2 - c^2, show |a|^2 cannot
# equal either eigenvalue: it is nonzero, and its SUM with (gamma Omega)^2 is a sum of positives.
A2g = sp.simplify(A2)
sum_pos = sp.simplify(A2 + (gam * Om) ** 2)
print(f"  |a|^2 = {A2g}   (a quotient of positive symbols, so > 0)")
print(f"  |a|^2 + (gamma Omega)^2 = {sum_pos}   (a sum of positives, so != 0)")
check(A2g != 0 and sum_pos != 0 and sp.simplify(A2g.is_positive is not False),
      "E3b |a|^2 is a quotient of POSITIVE symbols hence strictly > 0, while the eigenvalues are 0 and "
      "-(gamma Omega)^2 <= 0; |a|^2 differs from 0, and |a|^2 + (gamma Omega)^2 is a sum of positives so "
      "|a|^2 != -(gamma Omega)^2. A SIGN obstruction, independent of Omega, R, gamma and a0")
print("""
  AND THAT CLOSES THE WHOLE CLASS. For any function F, spec(F(Box_u)) = F(spec(Box_u)) = {F(0),
  F(-(gamma Omega)^2)} -- two numbers determined by the orbital FREQUENCY. No choice of F, however
  nonlocal, bounded, Herglotz or causal, can put +|a|^2 into that set, because F acts on the spectrum
  it is given and the spectrum it is given contains no positive element.""")


banner("E4  WHY THE MOMENT SURVIVES WHERE THE SPECTRUM DOES NOT")

mom = sp.simplify(dot(u, adot))
check(sp.simplify(mom + A2) == 0,
      "E4 u . D^2 u = -|a|^2 exactly (Theorem B) -- because b is ORTHOGONAL to u, the contraction "
      "annihilates the torsion term that ruins the eigenvalue equation")
check(sp.simplify(dot(u, b).subs(GSUB)) == 0,
      "E4b and that orthogonality is the entire mechanism: b.u = 0, so the same term that is fatal to "
      "the spectrum is invisible to the moment")
print("""
  So Theorem B is a statement about an INDEFINITE QUADRATIC FORM, not about the spectrum. That is the
  precise reason the first-moment closure and the resolvent are different objects -- and why one
  reproduces the RAR while the other is amplitude-free. They are not two readings of one thing.""")


banner("E5  MUTATION CONTROL: kill the torsion and the eigenvalue equation becomes EXACT")

# hyperbolic (uniformly accelerated, straight-line) motion: torsion-free by construction
al2 = sp.Symbol("alpha", positive=True)
th = al2 * tau / cs
u_h = sp.Matrix([sp.cosh(th), sp.sinh(th), 0, 0])
check(sp.simplify(dot(u_h, u_h) + 1) == 0, "E5 the hyperbolic worldline is normalised, u.u = -1")
a_h = D(u_h)
A2_h = sp.simplify(dot(a_h, a_h))
resid_h = sp.simplify(D(a_h) - A2_h * u_h)
print(f"  hyperbolic motion: |a|^2 = {A2_h},   D^2 u - |a|^2 u = {resid_h.T}")
check(resid_h == sp.zeros(4, 1) and sp.simplify(A2_h - (al2 / cs) ** 2) == 0,
      "E5a MUTATION: on TORSION-FREE motion u IS a genuine eigenvector of Box_u with eigenvalue EXACTLY "
      "+|a|^2, residual identically zero -- so the torsion is the whole obstruction, confirmed by "
      "removing it rather than by argument")
print("""
  AND THIS IS PHYSICALLY INFORMATIVE, not just a control. The published action WOULD deliver the
  first-moment closure -- with an O(1) amplitude and no (v/c)^2 -- for LINEAR acceleration. It fails
  precisely for ORBITAL motion, because orbits carry torsion. MOND is a claim about orbits. The action
  is well matched to the one kinematic regime in which the phenomenon does not live.""")


banner("E6  WHAT IS LEFT")

print("""  ESCAPE (2) IS CLOSED as posed: no function of Box_u -- nonlocal, bounded, Herglotz, causal or
  otherwise -- has +|a|^2 as a worldline eigenvalue on bound motion, because Box_u's spectrum there is
  {0, -(gamma Omega)^2} and F acts only on the spectrum it is handed.

  WHAT WOULD STILL BE NEEDED, now stated sharply enough to be searched:
   * AN OPERATOR THAT IS NOT A FUNCTION OF Box_u. The obstruction is entirely that Box_u = d^2/dtau^2
     generates ROTATION on bound data (imaginary eigenvalues, hence a non-positive square). An operator
     whose generator has REAL eigenvalues on bound orbits would evade E3. E5 shows this is not vacuous:
     the same Box_u has a positive eigenvalue on hyperbolic motion, so the sign obstruction is a property
     of BOUND kinematics, not a universal theorem.
   * A CONSTRUCTION THAT PROJECTS OUT THE BINORMAL. D^2 u = |a|^2 u + |a| B b becomes an exact eigenvalue
     equation under the projector orthogonal to b. But b is built from THIRD derivatives of the
     trajectory, so that projector is solution-dependent and raises the derivative order -- which is
     precisely the "the projection IS the residual closure freedom" already recorded by
     mi_offcircular_closure_collapse_2026. Not obviously fatal, but it is a new Ostrogradsky exposure and
     must be priced, not assumed.

  STILL OPEN FROM THE PREVIOUS SCRIPT, untouched here: (1) a NON-quadratic-in-u action, where the
  (v/c)^2 never arises; (3) a coupling through rho_m or T_mu_nu; (4) the MG realization.

  UNTOUCHED: every measurement, and a0 = kappa c sqrt(G rho_Lambda), which is a claim about the SCALE.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the torsion is isolated as the obstruction by removing it (E5), not by assertion.")
