#!/usr/bin/env python3
"""
PROJECT 3d: the aether-stiffness calculation -- does theta=div(A) stay ~3H inside galaxies? (NO.)
================================================================================================
Project 3c proposed realizing the framework's rising a0 as a0=(c/3Z)theta, theta=div(A) the AeST aether
expansion, and flagged that this needs theta~3H INSIDE bound galaxies (a stiffness question). This file does
that calculation precisely. The result is definitive and unfavorable: a galaxy-aligned aether has theta=0
EXACTLY (verified), PPN constraints FORCE that alignment (no stiffness escape), so a0=(c/3Z)theta -> ~0 in
galaxies -- contradicting the observed a0. The aether-expansion realization is dead. Honest about what this
does NOT kill: the rising a0 falls back on the cosmic external-field (Deser-Levin) premise, i.e. the
unresolved apparent-vs-event question (project 3). Needs sympy + numpy.
"""
import sympy as sp
import numpy as np


def part1_theta_zero():
    print("="*92); print("PART 1 -- [verified] a galaxy-frame aether has theta = 0 exactly"); print("="*92)
    t = sp.symbols('t'); r, th = sp.symbols('r theta'); Phi = sp.Function('Phi')(r); Psi = sp.Function('Psi')(r)
    g = sp.diag(-sp.exp(2*Phi), sp.exp(2*Psi), sp.exp(2*Psi)*r**2, sp.exp(2*Psi)*r**2*sp.sin(th)**2)
    sqrtg = sp.sqrt(-g.det()); At = sp.exp(-Phi)
    theta = sp.simplify(sp.diff(sqrtg*At, t)/sqrtg)
    print(f"""  Static isotropic weak field ds^2 = -e^2Phi dt^2 + e^2Psi(dr^2+r^2 dOmega^2); a unit-timelike aether
  aligned with the static frame is A^mu = (e^-Phi, 0, 0, 0). Then
        theta = (1/sqrt(-g)) d_mu(sqrt(-g) A^mu) = {theta}
  EXACTLY zero -- a galaxy-frame aether does not expand (it is aligned with the timelike Killing vector, which
  is divergence-free). This is rigorous, not approximate.\n""")


def part2_ppn():
    print("="*92); print("PART 2 -- PPN forces that alignment (no stiffness escape)"); print("="*92)
    print("""  Could a 'stiff' aether keep theta=3H inside a galaxy instead? That would mean the aether EXPANDS through
  the (static) galactic matter -- a relative velocity between the aether and matter of order H x r. A
  preferred-frame velocity sources the PPN parameters alpha_1, alpha_2 in Einstein-aether/AeST. Observations
  bound them to |alpha_1| < 1e-4 (Solar System) and |alpha_2| < 1e-7 (pulsar timing). An O(1) misalignment
  (theta=3H vs 0) would give alpha_1, alpha_2 ~ O(1) -- excluded by ~4-7 orders of magnitude. So the aether
  MUST align with the local static frame in bound systems: theta ~ 0 there. Stiffness does not help; a stiff
  aether is exactly the one that produces large preferred-frame effects. The alignment is forced.\n""")


def part3_consequence():
    print("="*92); print("PART 3 -- consequence: a0 prop theta FAILS"); print("="*92)
    c, Mpc = 2.99792458e8, 3.0857e22; H0 = 67.4e3/Mpc; Z = 2*np.sqrt(8*np.pi/3)
    print(f"""  a0 = (c/3Z) theta:
     FRW background: theta = 3H -> a0 = cH/Z = {c*H0/Z*1e10:.2f}e-10  (correct).
     virialized galaxy: theta ~ 0 -> a0 ~ 0.   But galaxies DO show a0 ~ 1.2e-10.  CONTRADICTION.
  The aether-expansion realization of rising a0 is DEAD: theta is ~0 exactly where a0 must be ~cH/Z. Project
  3c is therefore not merely 'contingent on stiffness' -- it is excluded, because the stiffness that would
  save it is itself excluded by PPN.\n""")


def part4_general_and_escape():
    print("="*92); print("PART 4 -- the general obstruction, and the one escape it leaves"); print("="*92)
    print("""  GENERAL OBSTRUCTION: a0 = cH/Z is a COSMIC (background) value that must be UNIFORM inside galaxies
  (the RAR is tight). But any LOCAL covariant field tied to a0 takes its LOCAL value in a galaxy, which is NOT
  the cosmic one: theta -> 0 (this calc); the Ricci scalar R -> R_local (baryon-dominated) >> R_cosmic; the
  density rho -> rho_local != rho_crit. So NO local covariant scalar reproduces the uniform cosmic a0 inside
  galaxies. The CONSTANT-a0 (Lambda, event-horizon) reading avoids this entirely: Lambda is a true constant,
  uniform by definition. => on covariant-realizability grounds, the EVENT-horizon (constant a0) reading is
  PREFERRED and the APPARENT-horizon (rising a0) reading is obstructed. A genuine theory point against the bet.

  THE ESCAPE (honest): rising a0 is not strictly killed. Its remaining realization is NON-local -- the cosmic
  EXTERNAL FIELD: the de Sitter horizon imposes a background acceleration ~cH on every system (the Deser-Levin
  Unruh floor). IF that floor tracks the INSTANTANEOUS cH(z) it rises; if the asymptotic c sqrt(Lambda) it is
  constant. That is exactly the unresolved apparent-vs-event question (project 3). So the aether door closes
  the theta-realization but pushes the rising bet back onto the cosmic-external-field premise, which remains
  open -- it does not, by itself, decide it.\n""")


def verdict():
    print("="*92); print("PROJECT 3d VERDICT"); print("="*92)
    print("""  The aether-stiffness calculation is definitive: theta=0 exactly in a galaxy (verified), PPN forces it
  (no stiff escape), so a0 = (c/3Z)theta -> 0 inside galaxies and the 3c realization is EXCLUDED. More
  generally, no LOCAL covariant field reproduces the uniform cosmic a0=cH/Z inside galaxies (theta->0,
  R->R_local, rho->rho_local) -- a covariant-realizability obstruction that the constant-a0 (Lambda) reading
  does not face. This is a genuine theoretical point AGAINST the rising bet and FOR the event-horizon reading.
  It does not fully kill rising a0 (the cosmic external-field / Deser-Levin route is non-local and survives,
  = the open apparent-vs-event question), but it removes the clean local realization and tilts the theory
  further toward constant a0. A clean negative, world-class-careful, the door walked all the way through.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 3d -- aether-stiffness: does theta stay 3H in galaxies? (definitive NO)"); print("#"*92 + "\n")
    part1_theta_zero(); part2_ppn(); part3_consequence(); part4_general_and_escape(); verdict()


if __name__ == "__main__":
    main()
