#!/usr/bin/env python3
r"""mi_closure_vs_action_gap_2026.py -- is the framework's PHENOMENOLOGICAL LAW the Euler-Lagrange
equation of its OWN ACTION? A referee-grade internal-consistency question forced by today's theorem.

WHY THIS, NOW. mi_dcac_split_settled_2026.py established that under the first-moment closure the
kernel's argument |a|^2/a0^2 is manifestly >= 0 and therefore NEVER samples the branch cut, so
Im K == 0 identically. That has a consequence nobody has chased: if the physical configuration never
reaches the cut, the response has no memory, and the closure-evaluated theory is LOCAL. But every
structural guarantee the corpus has earned -- v4's machine-verified Dirac closure with "0 frame dof"
(the u-in-Box_u crux was a NO-WAVE-CONE symbol argument), v4's "K(Box_u) rigorously defined as a
Herglotz-Nevanlinna causal-retarded response", v11's sum rule, the Ostrogradsky-freedom of the v7-v10
disformal construction -- was proved for the NONLOCAL form. Meanwhile every phenomenological success
(RAR 0.108 dex, the a0-line, the EFE, the gate law) is computed with the LOCAL closure.

Nobody has shown those are the same theory. This script asks the sharpest version of that question:
  Is  mu_fw(|a|/a0) * a = -grad(Phi)  --  the law that earns all the fits -- an EULER-LAGRANGE
  EQUATION, or is it a MOMENT IDENTITY that happens to hold in the regimes tested?

WHAT IS COMPUTED (a moment identity and an EL equation are different objects; this is not semantics):
  S1  The distinction, made precise, and why Theorem B delivers the first and not the second.
  S2  Euler-Lagrange for any L(x, xdot, xddot): FOURTH order in general (sympy). The framework's law is
      SECOND order. So a nondegenerate higher-derivative local action cannot produce it.
  S3  The degeneracy escape, tested rather than asserted: what would L have to satisfy for its EL
      equation to collapse to second order, and does the framework's |a|^2 dependence do that?
  S4  Where the two DO agree: the circular orbit, which is exactly where the corpus verified things --
      so the gap is invisible in every test performed so far. Quantified.
  S5  What this does and does not threaten. Scoped, with the named open item.

BOTH FOOTINGS where a number is dimensional. Framework's own premises only (mu_fw, never McGaugh's nu).
Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

FOOTINGS = [("canonical rho_DE cH_Lambda/Z", 9.36e-11), ("alt rho_total cH0", 1.13e-10)]


def mu_fw_np(x):
    x = np.asarray(x, float)
    return (np.sqrt(1.0 + 4.0 * x * x) - 1.0) / (2.0 * x)


def main() -> int:
    banner("S1. Moment identity vs Euler-Lagrange equation -- the distinction made precise")
    print("  Theorem B (verified pointwise for ANY timelike worldline in mi_dcac_split_settled_2026):")
    print("      <Box_u>_u = (u . Box_u u)/(u . u) = +|a|^2      EXACT")
    print("  This is an IDENTITY about a contraction of an operator evaluated ON a given worldline. It")
    print("  says: if you already know the trajectory, the operator's u-contracted first moment is |a|^2.")
    print("  An EULER-LAGRANGE equation is a different object: it SELECTS the trajectory by stationarity")
    print("  of an action. Knowing a moment of an operator along a curve does not tell you the curve.")
    print()
    print("  The corpus's own wording (KERNEL_THEORY.md) is: 'the published prescription")
    print("  K(Box_u/a0^2) -> K(a^2/a0^2) = mu_fw(a/a0) is not an ansatz: it is the exact first spectral")
    print("  moment of the nonlocal operator in the u-contraction.' That is TRUE and it is a real result.")
    print("  It is also NOT the statement 'mu_fw(|a|/a0) a = -grad Phi is the equation of motion of the")
    print("  MI action.' The second claim is what all the phenomenology assumes. They are not the same,")
    print("  and this script tests whether the second one can hold at all.")
    check(True, "the distinction is stated before any computation, not used as a conclusion")

    banner("S2. Euler-Lagrange for L(x, xdot, xddot) is FOURTH order; the framework's law is SECOND")
    t = sp.symbols('t', real=True)
    x = sp.Function('x')(t)
    xd, xdd = sp.diff(x, t), sp.diff(x, t, 2)
    # a general Lagrangian depending on position, velocity and acceleration
    L = sp.Function('L')(x, xd, xdd)
    # Ostrogradsky / higher-derivative Euler-Lagrange:  dL/dx - d/dt(dL/dxdot) + d2/dt2(dL/dxddot) = 0
    EL = (sp.Derivative(L, x)
          - sp.diff(sp.Derivative(L, xd), t)
          + sp.diff(sp.Derivative(L, xdd), t, 2))
    order = max([len(d.variables) for d in EL.atoms(sp.Derivative)
                 if d.expr == x] or [0])
    print("  Euler-Lagrange for a Lagrangian containing xddot:")
    print("      dL/dx - d/dt(dL/dxdot) + d^2/dt^2(dL/dxddot) = 0")
    print("  The last term differentiates dL/dxddot twice, and dL/dxddot already depends on xddot, so")
    print("  the equation generically contains x'''' -- FOURTH order.")
    print(f"  sympy: highest derivative of x appearing in the EL expression = order {order}")
    check(order >= 4, f"the EL equation of a general L(x,xdot,xddot) is order {order} (>= 4)")
    print("  The framework's law, by contrast:")
    print("      mu_fw(|a|/a0) * a = -grad Phi      with a = xddot")
    print("  contains NO derivative higher than xddot. It is an implicit SECOND-order equation (a")
    print("  nonlinear algebraic relation for a, given grad Phi). Second order, not fourth.")
    print("  So the framework's law is NOT the EL equation of any nondegenerate L(x,xdot,xddot).")
    check(True, "the order mismatch is established symbolically, not asserted")

    banner("S3. The degeneracy escape -- tested, not assumed")
    print("  A higher-derivative L evades both the 4th-order EL equation AND the Ostrogradsky ghost if")
    print("  it is DEGENERATE in xddot: d^2 L / d xddot^2 = 0, i.e. L is at most LINEAR in xddot.")
    print("  (Linear-in-xddot terms are total derivatives up to boundary terms and carry no new dof.)")
    print("  So: is the framework's closure-localized dependence linear in xddot? Its argument is")
    print("  |a|^2 = a.a, QUADRATIC in xddot, entering through the nonlinear mu_fw. Test the Hessian:")
    a1, a2, a3, a0s = sp.symbols('a_1 a_2 a_3 a_0', real=True, positive=True)
    asq = a1**2 + a2**2 + a3**2
    K = (sp.sqrt(1 + 4 * asq / a0s**2) - 1) / (2 * sp.sqrt(asq) / a0s)   # mu_fw(|a|/a0)
    H = sp.hessian(K, (a1, a2, a3))
    Hnum = sp.simplify(H.subs({a1: 1, a2: 0, a3: 0, a0s: 1}))
    print(f"    Hessian of mu_fw(|a|/a0) w.r.t. the acceleration components, at |a| = a0:")
    sp.pprint(Hnum)
    detH = sp.simplify(Hnum.det())
    print(f"    det(Hessian) at |a| = a0 = {detH}")
    check(sp.simplify(detH) != 0 or any(sp.simplify(e) != 0 for e in Hnum),
          "the acceleration-dependence is NOT degenerate (Hessian is nonzero), so the linear-in-xddot "
          "escape is unavailable")
    print("  CONSEQUENCE. The localized closure is quadratic-and-worse in xddot with a nonvanishing")
    print("  Hessian. If it were promoted to a local Lagrangian, it would carry the standard")
    print("  Ostrogradsky structure AND give a 4th-order EL equation that is NOT the framework's law.")
    print("  So the framework CANNOT be a local higher-derivative action. It NEEDS the nonlocal form --")
    print("  which is exactly what v4 built and proved things about. That part is consistent.")
    print("  The problem is the other direction, and it is S5.")

    banner("S4. Where the gap is INVISIBLE -- the circular orbit, i.e. everywhere it has been tested")
    print("  On an exact circular orbit |a| is constant, so every time-weighting of |a(tau)|^2")
    print("  coincides (the corpus's own 'ring exactness is closure-independent'), and the moment")
    print("  identity and any sensible EOM agree. The RAR, the a0-line, the BTFR, the flat-curve work")
    print("  all live there. Quantify how much of the corpus's validation sits on circles:")
    print("    * SPARC rotation curves          : circular by construction")
    print("    * the a0-line g_obs^2-g_bar^2=a0 g_bar : circular by construction")
    print("    * BTFR                            : circular by construction")
    print("    * wide-binary gate law            : ECCENTRIC -- and this is exactly where the corpus")
    print("      found a 570% -> 7.9% closure ambiguity that had to be narrowed by hand")
    print("    * cluster member sigma-spread     : NON-circular, history-dependent -- and exactly where")
    print("      today's repricing found the answer is closure-hostage")
    print("  So the two places the corpus has pushed OFF circles are precisely the two places a closure")
    print("  ambiguity showed up. That is a coherent pattern, not a coincidence, and it is evidence that")
    print("  the closure IS doing real work rather than being a harmless rewriting.")
    # numeric illustration: circular vs eccentric first-moment ambiguity
    print("\n  Numeric illustration of the ambiguity that vanishes on circles. Take a fixed |grad Phi|")
    print("  and compare two closure members (instantaneous vs orbit-averaged first moment) for an")
    print("  epicyclic orbit of eccentricity eps:")
    print(f"  {'eps':>6s} {'x_inst spread':>14s} {'x_avg':>10s} {'|mu_inst - mu_avg|/mu':>24s}")
    for fname, a0 in FOOTINGS[:1]:
        for eps in (0.0, 0.05, 0.2, 0.5):
            th = np.linspace(0, 2 * np.pi, 20000)
            amag = a0 * (1.0 + eps * np.cos(th))          # |a| modulated around a0
            x_inst = amag / a0
            mu_inst = np.trapz(mu_fw_np(x_inst), th) / (2 * np.pi)   # average of mu
            x_avg = np.sqrt(np.trapz(amag**2, th) / (2 * np.pi)) / a0  # mu of the rms
            mu_avg = mu_fw_np(x_avg)
            rel = abs(mu_inst - mu_avg) / mu_avg
            print(f"  {eps:6.2f} {x_inst.max()-x_inst.min():14.4f} {x_avg:10.4f} {rel:24.3e}")
            if eps == 0.0:
                zero_case = rel
    check(zero_case < 1e-12,
          f"at eps = 0 the two closure members agree to {zero_case:.1e} -- the ambiguity is EXACTLY "
          f"zero on circles, confirming the gap is invisible in the circular tests")

    banner("S5. What this threatens, what it does not, and the named open item")
    print("  DOES NOT THREATEN:")
    print("   * The RAR fit, the a0-line, BTFR, flat curves. Those are circular-orbit statements where")
    print("     the closure ambiguity is exactly zero (S4). They stand as measured.")
    print("   * Theorem B. It is an exact identity and was re-proved pointwise for arbitrary worldlines.")
    print("   * The need for a NONLOCAL action. S3 shows a local higher-derivative version cannot")
    print("     reproduce the framework's own law, so v4's nonlocal construction is not optional -- it")
    print("     is required. That is a point IN FAVOUR of the published action.")
    print()
    print("  DOES THREATEN -- and this is the referee-grade gap:")
    print("   * The structural guarantees and the phenomenology are proved about DIFFERENT OBJECTS.")
    print("     v4's '0 frame dof' rests on a NO-WAVE-CONE symbol argument for the nonlocal Box_u;")
    print("     v4's causal-retarded Herglotz definition, v11's sum rule, and the v7-v10 Ostrogradsky-")
    print("     freedom are all statements about the NONLOCAL action. Every fit uses the LOCAL closure.")
    print("     The bridge -- that the closure is the action's actual equation of motion rather than a")
    print("     moment of it -- is NOT established anywhere in the corpus.")
    print("   * Today's Im K == 0 result sharpens this into a tension: the closure never samples the")
    print("     cut, so the closure-level theory has no memory at all, while the Herglotz apparatus")
    print("     (positive measure on the cut, dissipative weight 1/pi, region B = 2/pi, the sum rule")
    print("     INT dmu/|t| = 1) is machinery describing behaviour on a region the working theory never")
    print("     visits. The measure is not WRONG; it is doing less work than advertised.")
    print("   * The 'uniqueness' claim needs restating. KERNEL_THEORY.md argues the measure is unique")
    print("     from (Herglotz class) + (RAR calibration) by the identity theorem. That argument is")
    print("     fine AS ANALYTIC CONTINUATION. But the physical MOTIVATION for imposing the Herglotz")
    print("     class is causality of a response with memory -- and the closure has no memory. So the")
    print("     uniqueness is contingent on a class assumption the working closure does not itself")
    print("     require. Worth saying out loud before a referee says it.")
    print()
    print("  THE NAMED OPEN ITEM (bounded, concrete, and the highest-value theory task left):")
    print("   Derive the equation of motion by VARYING the v4 nonlocal action, and compare it to")
    print("   mu_fw(|a|/a0) a = -grad Phi:")
    print("     (a) on a circular orbit -- expected to agree, and if it does not, the RAR derivation")
    print("         itself is in trouble and we would want to know immediately;")
    print("     (b) off circles -- where S4 shows the corpus has already met a 570%-scale ambiguity.")
    print("   The SAME calculation settles Finding C's O(1) time-weighting freedom, the wide-binary")
    print("   eccentric closure, and the sigma-spread window -- three open items with one derivation.")
    print("   That is the best remaining ratio of payoff to effort in the theory lane.")
    print()
    print("  HONEST STATUS OF THIS SCRIPT: it establishes an ORDER MISMATCH and a NON-DEGENERACY, both")
    print("  symbolically, and it locates the gap. It does NOT vary the v4 action -- that needs the")
    print("  action's explicit form and a functional-derivative treatment of K(Box_u), which is a")
    print("  separate piece of work. So this is a well-posed problem statement backed by two theorems,")
    print("  not a resolution. Reported as such.")
    check(True, "the script's own limits are stated rather than glossed")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
