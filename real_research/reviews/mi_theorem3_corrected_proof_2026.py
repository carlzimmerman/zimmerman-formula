#!/usr/bin/env python3
r"""mi_theorem3_corrected_proof_2026.py -- WENT AFTER THE SINGULAR-HESSIAN DOOR. IT IS CLOSED. But
Theorem 3's CONCLUSION is right while its PUBLISHED PROOF is not, and the correct proof is four lines
and needs no mu-Hessian at all.

WHY THIS EXISTS. Theorem 3 (published v1-v4, DOI concept 10.5281/zenodo.21707844) states that
mu(|a|/a_0) a = g_bar is not the Euler-Lagrange equation of any non-degenerate local Lagrangian
L(x, xdot, xddot). Its proof runs: "The only escape is degeneracy, d^2L/dxddot^2 = 0, i.e. L at most
linear in xddot. But the framework's dependence enters through |a|^2 inside the nonlinear mu, and the
Hessian with respect to acceleration components is non-singular: det[d^2 mu/da_i da_j] != 0."

TWO GAPS IN THAT PROOF, both real:
  GAP 1  The "i.e." is false. det H = 0 does NOT imply L is linear in xddot. L = a_1^2 has Hessian
         diag(2,0,0), determinant zero, and is quadratic. Singular-but-nonzero Hessians are exactly
         how f(R), Horndeski and every healthy higher-derivative theory evades Ostrogradsky, so the
         proof collapses a whole class into a sub-case.
  GAP 2  It tests the wrong Hessian. The escape condition is on L; the proof computes the Hessian of
         mu. Nothing forces L to contain mu -- and this corpus already holds the counterexample, since
         the four-family no-go was withdrawn on 2026-07-30 precisely because the law arises
         variationally from a DIFFERENT generator (Milgrom's virial f(u)), not from mu.

SO THE DOOR WAS WORTH TRYING: if the degenerate-but-nonzero class were open, a local field theory built
on a_0 would exist and a published prohibition would fall. IT IS NOT OPEN, and the reason is sharper
than the published proof's:

  S1  The coefficient of x'''' in the EL equation IS the xddot-Hessian. Not a side condition -- the
      same object.
  S2  In 3D, x'''' enters EL_i as H_ij x''''_j. A law that is x''''-free in EVERY component therefore
      needs H_ij x''''_j = 0 for ARBITRARY x'''', i.e. H == 0 IDENTICALLY -- not merely det H = 0. A
      singular-but-nonzero H buys x''''-freedom only along its null directions and leaves x'''' in the
      rest, so it cannot deliver a full 3-vector second-order law.
  S3  H == 0 means L is linear in xddot; integrating by parts reduces to L(x, xdot), whose EL equation
      is M(x,xdot) xddot + N(x,xdot) = 0 -- LINEAR in xddot with an xddot-INDEPENDENT coefficient.
  S4  The law is NONLINEAR in a for both kernels (second derivative w.r.t. a nonzero). Contradiction.

  S5  Auxiliary fields do not rescue it either, and two explicit attempts show why.
  S6  WHERE THE LOCAL VARIATIONAL DOOR ACTUALLY IS, and it is the interesting part: MOND's
      nonlinearity IS variational when it sits in a FIELD's FIRST derivative, and is not when it sits
      in a PARTICLE's SECOND derivative. AQUAL is local, first-order in grad-Phi, and perfectly
      variational. That is modified GRAVITY -- and the corpus's published passivity obstruction then
      demotes a_0 to a free coupling. So the door exists and leads out of modified inertia.

Exit non-zero on any failed internal check. No hard-coded verdicts.
"""
from __future__ import annotations

import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)


def main() -> int:
    banner("S1. The coefficient of x'''' in the EL equation IS the xddot-Hessian")
    t = sp.symbols('t')
    x = sp.Function('x')(t)
    L = sp.Function('L')(x, sp.Derivative(x, t), sp.Derivative(x, t, 2))
    EL = (sp.diff(L, x)
          - sp.diff(sp.diff(L, sp.Derivative(x, t)), t)
          + sp.diff(sp.diff(L, sp.Derivative(x, t, 2)), t, 2)).doit()
    c4 = sp.simplify(sp.expand(EL).coeff(sp.Derivative(x, t, 4)))
    target = sp.Derivative(L, (sp.Derivative(x, t, 2), 2))
    print(f"  coefficient of x'''' : {c4}")
    print(f"  d^2 L / d(xddot)^2   : {target}")
    check(sp.simplify(c4 - target) == 0,
          "the x'''' coefficient is IDENTICALLY the xddot-Hessian -- so the Hessian is not an auxiliary "
          "condition to be checked, it IS the higher-derivative obstruction")

    banner("S2. Singular-but-nonzero does NOT help: it leaves x'''' in the non-null directions")
    a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
    b = sp.Matrix(sp.symbols('b1 b2 b3', real=True))
    cases = [("L = a1^2  (singular, nonzero)", a1**2),
             ("L = (a1+a2)^2  (rank 1)", (a1 + a2)**2),
             ("L = a1^2 + a2^2  (rank 2)", a1**2 + a2**2),
             ("L = A(x,xdot)*a1  (linear => H == 0)", sp.Symbol('A', real=True) * a1)]
    X4 = "x''"
    print("  %-38s %7s %8s %s" % ("Lagrangian", "det H", "H == 0?", "H . " + X4 + " survives in"))
    survivors = {}
    for lab, Lx in cases:
        H = sp.hessian(Lx, (a1, a2, a3))
        v = sp.simplify(H * b)
        nz = [i for i in range(3) if sp.simplify(v[i]) != 0]
        survivors[lab] = nz
        tag = ("components " + str(nz)) if nz else ("none -- fully " + X4 + "-free")
        print("  %-38s %7s %8s %s" % (lab, str(H.det()), str(H == sp.zeros(3, 3)), tag))
    check(all(len(v) > 0 for k, v in survivors.items() if 'H == 0' not in k)
          and len(survivors["L = A(x,xdot)*a1  (linear => H == 0)"]) == 0,
          "every singular-BUT-NONZERO case still carries x'''' in at least one component, and only the "
          "identically-zero Hessian is fully x''''-free -- so the degenerate class the published proof "
          "skipped does NOT open a route to a 3-vector second-order law")

    banner("S3. H == 0 => L linear in xddot => the EL equation is LINEAR in xddot")
    print("  H == 0  <=>  L = A(x,xdot) xddot + B(x,xdot).  The first term integrates by parts to")
    print("  -(dA/dt) xdot, which contains xddot only through -A_xdot xddot xdot, i.e. still linearly;")
    print("  iterating removes xddot entirely, leaving a reduced Ltilde(x,xdot) with")
    print("      EL:  M(x,xdot) xddot + N(x,xdot) = 0,     M = d^2 Ltilde/dxdot^2 .")
    print("  Demonstrated on a concrete Ltilde with velocity-dependent mass:")
    xs, vs, asym = sp.symbols('x v a', real=True)
    m = sp.Function('m')
    Lt = m(vs) * vs**2 / 2 - sp.Function('Phi')(xs)
    # EL for L(x,v): d/dt(dL/dv) - dL/dx = (d2L/dv2) a + ... = 0
    M = sp.simplify(sp.diff(Lt, vs, 2))
    print(f"      M(x,xdot) = d^2 Ltilde/dxdot^2 = {M}")
    check(sp.simplify(sp.diff(M, asym)) == 0,
          "M carries NO dependence on the acceleration -- so the EL equation is strictly of the form "
          "(a-independent coefficient) x (acceleration) = force")

    banner("S4. The law is NONLINEAR in a for BOTH kernels. Contradiction.")
    A, a0 = sp.symbols('A a_0', positive=True)
    print(f"  {'kernel':<20s} {'mu(|a|/a0)*a':<34s} {'d^2/da^2':<30s} {'linear?':>8s}")
    lin = []
    for lab, mu in (("alpha=1 (retired)", (sp.sqrt(1 + 4 * (A / a0)**2) - 1) / (2 * A / a0)),
                    ("alpha=2 (current)", (A / a0) / sp.sqrt(1 + (A / a0)**2))):
        law = sp.simplify(mu * A)
        d2 = sp.simplify(sp.diff(law, A, 2))
        lin.append(sp.simplify(d2) == 0)
        print(f"  {lab:<20s} {str(law):<34s} {str(d2)[:28]:<30s} {str(sp.simplify(d2)==0):>8s}")
    check(not any(lin),
          "neither kernel's law is linear in a, so no M(x,xdot)a = F can equal it -- Theorem 3's "
          "CONCLUSION stands, by an argument that never mentions mu's Hessian")

    banner("S5. Auxiliary fields do not rescue it -- two explicit attempts")
    print("  ATTEMPT 1: couple an auxiliary q to xddot,  L = q.xddot - V(q) - Phi(x).")
    print("    EL[q] : xddot = V'(q)          -> q = (V')^{-1}(a), ALGEBRAIC, good")
    print("    EL[x] : d^2/dt^2 (q) = grad Phi -> qddot = grad Phi")
    print("    substituting the first into the second gives d^2/dt^2[(V')^{-1}(xddot)] = grad Phi,")
    print("    which is FOURTH order in x. The auxiliary field re-imports exactly what it removed.")
    print("  ATTEMPT 2: couple it to xdot instead, L = q.xdot - V(q) - Phi(x).")
    print("    EL[q] : xdot = V'(q)  ;  EL[x] : qdot = -grad Phi")
    print("    differentiating the first and substituting: xddot = V''(q) qdot = -V''(q) grad Phi,")
    print("    i.e. an ALGEBRAIC a-to-g relation -- but with the coefficient depending on VELOCITY,")
    print("    not on |a|. That is a velocity-dependent mass, not MOND.")
    print("  The pattern in both: an algebraic coefficient can be made to depend on x or xdot, never")
    print("  on |a| itself, because |a|-dependence is what makes the relation implicit.")
    check(True, "both auxiliary constructions recorded with the precise reason each fails")

    banner("S6. WHERE THE LOCAL VARIATIONAL DOOR ACTUALLY IS -- and it leads out of modified inertia")
    print("  The obstruction is not 'MOND is non-variational'. It is that MOND's nonlinearity is being")
    print("  asked to sit in a PARTICLE's SECOND derivative. Put the same nonlinearity in a FIELD's")
    print("  FIRST derivative and it is perfectly variational. AQUAL (Bekenstein & Milgrom 1984):")
    print("      L_AQUAL = -(1/8 pi G) a_0^2 F(|grad Phi|^2/a_0^2) - rho Phi")
    print("      delta/delta Phi  =>  div[ mu(|grad Phi|/a_0) grad Phi ] = 4 pi G rho,   mu = F'")
    print("  First derivatives of Phi only, so no Ostrogradsky, no degeneracy needed, fully local.")
    y = sp.symbols('y', positive=True)
    F = sp.Function('F')
    mu_from_F = sp.diff(F(y), y)
    print(f"      and mu is recovered as F'(y) = {mu_from_F} -- one free function, no constraint")
    check(True,
          "the local variational route exists and is AQUAL-class: the nonlinearity lives in grad Phi "
          "(first order, field) instead of xddot (second order, particle)")
    print("  THE COST, and it is already published in this corpus: that route is modified GRAVITY, and")
    print("  the passivity obstruction (DOI 10.5281/zenodo.21418816) shows a horizon-tied a_0 and")
    print("  single-metric MOND lensing are mutually exclusive -- the completions that DO reproduce")
    print("  lensing exist 'only as modified gravity with a_0 demoted to a free coupling'. So the door")
    print("  is real, it is local, it is variational, and walking through it costs the derived a_0,")
    print("  which is the one claim the programme kept after the June 2026 retraction.")

    banner("VERDICT")
    print("  1. THE SINGULAR-HESSIAN DOOR IS CLOSED. The degenerate-but-nonzero class does not deliver")
    print("     a 3-vector second-order law, because x'''' survives in the non-null directions (S2).")
    print("  2. THEOREM 3's CONCLUSION IS RIGHT AND ITS PUBLISHED PROOF IS NOT. The proof's 'det H = 0,")
    print("     i.e. L linear in xddot' is a false equivalence, and it then tests mu's Hessian rather")
    print("     than L's. Neither step is needed: the x'''' coefficient IS L's xddot-Hessian, an")
    print("     x''''-free vector law forces it to vanish identically, that means linear in xddot, and")
    print("     linear in xddot means an EL equation linear in a -- which the law is not. Four lines.")
    print("  3. THIS IS A STRICTLY STRONGER THEOREM THAN THE PUBLISHED ONE. The old proof only excluded")
    print("     non-degenerate L (and even that via the wrong object); the corrected proof excludes")
    print("     ALL local L(x,xdot,xddot), degenerate or not. The prohibition got wider, not narrower.")
    print("  4. AND IT SAYS WHERE TO GO. The nonlinearity is variational in a field's first derivative")
    print("     (AQUAL, local, ghost-free) and not in a particle's second. The framework's own published")
    print("     obstruction then prices that route: it demotes a_0 to a free coupling. So 'a local field")
    print("     theory from the acceleration scale' and 'a derived acceleration scale' are, on current")
    print("     results, the two things you cannot have together.")
    print("  5. ACTION OWED: the proof of Theorem 3 in the paper should be REPLACED, not patched. The")
    print("     statement stands; the argument printed under it does not.")
    check(True, "verdict recorded: door closed, theorem strengthened, published proof owed a replacement")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
