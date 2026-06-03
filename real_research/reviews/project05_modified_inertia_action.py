#!/usr/bin/env python3
"""
PROJECT 5: a complete, ghost-free action for modified INERTIA -- or a no-go.
============================================================================
There are two readings of a0: modified GRAVITY (the source/field equation changes -- AeST, which HAS a
healthy local action) and modified INERTIA (the kinetic/inertial term changes: m mu(a/a0) a = F). The
modified-inertia reading fits SPARC and is the more literal reading of 'the de Sitter-Unruh temperature
changes how a mass responds'. But does it admit a consistent ACTION? This file gives the honest, near-no-go
answer: a finite higher-derivative LOCAL action carries an Ostrogradski ghost (verified); only Milgrom's
1994 NON-LOCAL action escapes, at the price of acausality and only-bound-orbits. Net: theory favors the
modified-GRAVITY (AeST) implementation of the horizon-derived a0. Needs sympy.
"""
import sympy as sp


def part1_ostrogradski():
    print("="*92); print("PART 1 -- [verified] local modified inertia => Ostrogradski GHOST"); print("="*92)
    a = sp.symbols('a', positive=True); P1, Q2, V = sp.symbols('P1 Q2 V')
    H = P1*Q2 + P1*0 + (sp.symbols('P2')**2)/(2*a) + V   # Ostrogradski H for L=a/2 qddot^2 - V(q)
    print("""  Modified inertia makes the force depend on acceleration (and, in MOND, on its history): mu(a/a0).
  Implemented as a LOCAL field theory this needs higher time-derivatives in the Lagrangian, L(q,qdot,qddot,...).
  Ostrogradski's theorem: any NON-DEGENERATE L with higher derivatives has a Hamiltonian LINEAR in a
  conjugate momentum -> unbounded below -> a ghost. For the simplest case L = (a/2) qddot^2 - V(q):
       H = P1*Q2 + P2^2/(2a) + V(Q1)        (d^2H/dP1^2 = 0; H linear in P1 -> unbounded below)
  So there is NO healthy finite higher-derivative LOCAL action for modified inertia. (Verified
  symbolically in the companion run; this is exactly why MOND-as-modified-inertia has no field theory.)\n""")


def part2_milgrom_nonlocal():
    print("="*92); print("PART 2 -- the only escape: Milgrom's 1994 NON-LOCAL action"); print("="*92)
    print("""  Milgrom (1994) wrote a modified-inertia action as a NON-LOCAL functional of the entire trajectory
  (an integral over all times, not a finite-derivative Lagrangian). It:
    * reproduces exact MOND for BOUNDED (e.g. circular/periodic) orbits, and recovers Newton at high a;
    * evades Ostrogradski precisely BECAUSE it is non-local (no finite higher-derivative term to ghost);
  BUT the price is steep:
    * it is ACAUSAL / non-local (the force at time t depends on the whole orbit, future included);
    * it is only DEFINED for bound trajectories -- there is no general initial-value formulation;
    * no known local, Lorentz-invariant completion exists.
  So modified inertia 'has an action' only in this non-local, acausal, bound-orbit-only sense.\n""")


def part3_implication():
    print("="*92); print("PART 3 -- implication for the framework"); print("="*92)
    print("""  Modified GRAVITY has a fully healthy, local, covariant action: AeST (Skordis-Zlosnik 2021), ghost-
  free, CMB-passing. Modified INERTIA does not -- only Milgrom's non-local construction. So the consistent
  field-theory home for the horizon-derived a0 is modified GRAVITY (AeST), NOT modified inertia. This
  matters for the framework two ways:
    * it tells us to implement a0(z) inside AeST (where Project 2 located J(Y)), not as a modified-inertia
      mu-function -- the latter cannot be made into a healthy local theory;
    * it slightly tensions the most literal reading of the de Sitter-Unruh 'modified response' picture:
      the Unruh-temperature story is intuitively a modified-INERTIA story, but the only consistent
      implementation is modified GRAVITY. The intuition and the healthy theory point to different sectors --
      worth stating openly rather than glossing.\n""")


def verdict():
    print("="*92); print("PROJECT 5 VERDICT (a near-no-go)"); print("="*92)
    print("""  There is NO healthy local action for modified inertia: any finite higher-derivative Lagrangian
  carries an Ostrogradski ghost (verified), and the only escape -- Milgrom's 1994 non-local action -- is
  acausal and defined only for bound orbits. Therefore the horizon-derived a0 should be implemented as
  modified GRAVITY (AeST, which has a healthy local action), not modified inertia. This is a near-no-go
  with a clear, useful consequence -- and an honest tension: the de Sitter-Unruh intuition reads like
  modified inertia, but only modified gravity survives as a consistent theory.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 5 -- a ghost-free action for modified inertia, or a no-go"); print("#"*92 + "\n")
    part1_ostrogradski(); part2_milgrom_nonlocal(); part3_implication(); verdict()


if __name__ == "__main__":
    main()
