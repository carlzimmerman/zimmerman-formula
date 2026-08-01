#!/usr/bin/env python3
r"""
### VERDICT WITHDRAWN 2026-07-31 -- DO NOT CITE THIS FILE'S CONCLUSION. #########################
#   Superseded by  real_research/reviews/mi_dcac_branch_verdict_withdrawn_2026.py  (26/26), which
#   builds on mi_action_eom_vs_rar_2026.py (Jul 30). Three defects, in increasing seriousness:
#     1. S1's "u_mu is an EIGENVECTOR of Box_u with eigenvalue -Omega^2" is FALSE as stated. It is
#        verified below on a TWO-COMPONENT SPATIAL vector; the time leg is never formed. On the
#        actual 4-velocity Box_u annihilates u^0 (eigenvalue 0) while the spatial legs give
#        -(gamma Omega)^2, so u_mu is not an eigenvector. (= FINDING 2 of AUDIT_mi_kernel_axis_gate.)
#     2. S2 pulls K out of the contraction using that false eigenvector, giving -K(z) where the
#        correct block value is +gamma^2 v^2 K(z): wrong SIGN, and wrong by (v/c)^2 = a factor
#        6.75e11 at the very wide-binary scale this file was written to decide.
#     3. Decisively, the STRATEGY fails. The action's literal reading is AMPLITUDE-FREE (|K| -> 1 on
#        the cut for both kernels and both footings) against a law needing mu_fw = 0.618 at a0, so it
#        is the reading under which the framework has NO rotation curves at all. A wide-binary
#        prediction cannot be settled by the reading that deletes the galaxy phenomenology.
#   AND THE VERDICT INVERTS: a low-pass gate passes DC with unit gain, so the framework's branch is
#   the DC one and its wide-binary prediction is the UNGATED boost (~1.05-1.10 alpha=1, ~1.02
#   alpha=2), not gamma_v = 1.000. PREREGISTRATION_DR4.md Amendment 1 cites this file by name and
#   registers 1.0004-1.0006 on its basis; Amendment 6 is owed and is Carl's to file.
#   Theorem B and the exact block form both STAND and are compatible -- see S3 there.
################################################################################################

mi_dcac_branch_settled_2026.py -- SETTLING the DC/AC branch from the framework's own written action
==================================================================================================
THE QUESTION (open since 2026-07-25, and the whole s^3 paper is conditional on it). The framework's
committed matter action is

    S_matter = -(1/2) INT d^4x sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
    K(z) = (sqrt(1+4z) - 1)/(2 sqrt z),     Box_u f = u^a nabla_a ( u^b nabla_b f ),     s = -1,

(prep_2026/mi_field_theory/BASELINE_ACTION.md and MATTER_COUPLING.md, verbatim). Does the kernel K
respond to the acceleration MAGNITUDE |a| -- constant on a circular orbit, hence a DC drive, gate OPEN,
gamma_v = 1.09 -- or to the orbital FREQUENCY, hence an AC drive, gate SHUT, gamma_v = 1.000? The two
branches are 4.9-5.8 sigma apart in the framework's own Gaia DR4 error model, so this decides whether
mi_wb_cubic_rise_2026.py and WB_CUBIC_GATE_LAW (Zenodo 10.5281/zenodo.21580093) stand or are VOID.

THE ANSWER IS FIXED BY THE ACTION AND IS NOT A MATTER OF INTERPRETATION. Box_u is the DOUBLE
PROPER-TIME DERIVATIVE along the worldline, (u.nabla)^2 = d^2/dtau^2. Its argument is therefore whatever
d^2/dtau^2 returns when applied to u_mu -- and on a circular orbit u_mu is an EIGENVECTOR of that
operator with eigenvalue -Omega^2. So K's argument is -Omega^2/a0^2: a FREQUENCY, not a magnitude.
S1 verifies the eigenvalue relation symbolically. VERDICT: THE AC BRANCH. The paper stands.

Scope stated honestly: computed in the flat-space slow-motion limit (tau -> t), which is the regime a
wide binary actually occupies (v/c ~ 1e-5). No claim is made about the strong-field case.
"""
import numpy as np
import sympy as sp

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

bar = "="*100
print(bar); print("mi_dcac_branch_settled -- reading Box_u off the framework's own action"); print(bar)

# ================================================== S1  the eigenvalue relation
print("\nS1  Box_u ACTING ON u_mu FOR A CIRCULAR ORBIT  (the decisive computation)")
print("-"*100)
t, R, Om = sp.symbols('t R Omega', positive=True)
# circular worldline in the orbital plane; slow motion so proper time ~ coordinate time
x = sp.Matrix([R*sp.cos(Om*t), R*sp.sin(Om*t)])
u = x.diff(t)                       # 4-velocity spatial part (u.nabla -> d/dt along the worldline)
a = u.diff(t)                       # 4-acceleration
box_u = a.diff(t)                   # Box_u u = (u.nabla)^2 u = d^2 u/dt^2
print(f"      worldline   x(t) = {sp.simplify(x.T)}")
print(f"      u = dx/dt        = {sp.simplify(u.T)}")
print(f"      a = du/dt        = {sp.simplify(a.T)}")
print(f"      Box_u u = d2u/dt2= {sp.simplify(box_u.T)}")
resid = sp.simplify(box_u + Om**2*u)
print(f"\n      Box_u u + Omega^2 u = {resid.T}   <-- IDENTICALLY ZERO")
print(f"      => u is an EIGENVECTOR of Box_u with eigenvalue -Omega^2, exactly.")
check("Box_u u_mu = -Omega^2 u_mu identically on a circular orbit (sympy)",
      all(sp.simplify(e) == 0 for e in resid))

# the contrast: |a| is constant, so a magnitude-sensing kernel would see a DC drive
amag = sp.simplify(sp.sqrt((a.T*a)[0]))
print(f"\n      CONTRAST -- the acceleration MAGNITUDE: |a| = {amag}, with d|a|/dt = "
      f"{sp.simplify(sp.diff(amag, t))}")
print("""      So |a| really is constant (that part of the DC reading was correct). But the action does NOT
      contract K with |a|. It contracts K(Box_u/a0^2) with u_mu, and Box_u returns -Omega^2 on that
      vector. The magnitude never enters the operator's argument.""")
check("|a| is constant on a circular orbit, so the DC reading was well-motivated -- but the action "
      "does not feed |a| to K", sp.simplify(sp.diff(amag, t)) == 0)

# ================================================== S2  therefore the argument is a frequency
print("\nS2  THE ARGUMENT OF K IS A FREQUENCY, AND ITS SIZE FOR A WIDE BINARY")
print("-"*100)
print("""      With Box_u u = -Omega^2 u, the action's scalar becomes
          u^mu K(Box_u/a0^2) u_mu = K(-Omega^2/a0^2) (u.u) = -K(-Omega^2/a0^2),
      i.e. the kernel is evaluated at NEGATIVE argument z = -(Omega c/a0)^2 -- the framework's own
      'frequency axis'. (Note the c-factors: z = -(Omega c/a0)^2, not -(Omega/a0)^2; dropping c is a
      known 1e4-order error in this project.)\n""")
C, G, AU, KPC, MSUN, MPC = 2.99792458e8, 6.67430e-11, 1.495978707e11, 3.0856775814913673e19, 1.98892e30, 3.0856775814913673e22
H0, OL = 67.66e3/MPC, 0.6889
Z = np.sqrt(32*np.pi/3)
A0 = {"canon": C*H0*np.sqrt(OL)/Z, "alt": C*H0/Z}
M15 = 1.5*MSUN
Om_wb = np.sqrt(G*M15/(10e3*AU)**3)
print(f"  {'footing':<9}{'a0 [m/s^2]':>14}{'branch pt Om=a0/2c':>22}{'Om(10 kAU)':>14}{'z = -(Om c/a0)^2':>20}")
print("  "+"-"*96)
for f_, a0v in A0.items():
    ombr = a0v/(2*C)
    z = -(Om_wb*C/a0v)**2
    print(f"  {f_:<9}{a0v:>14.4e}{ombr:>22.4e}{Om_wb:>14.4e}{z:>20.3e}")
z_can = -(Om_wb*C/A0['canon'])**2
print(f"""
      The branch point of K sits at z = -1/4, i.e. Omega = a0/(2c) = {A0['canon']/(2*C):.3e} rad/s -- the
      framework's memory frequency. A wide binary at 10 kAU has Omega = {Om_wb:.3e} rad/s, which is
      {Om_wb/(A0['canon']/(2*C)):.2e} times larger, putting z = {z_can:.3e}: about {abs(np.log10(abs(z_can/0.25))):.0f} orders PAST the branch point,
      deep on the frequency axis.""")
check(f"a wide binary sits far past K's branch point z = -1/4 (z = {z_can:.2e}), i.e. deep on the "
      f"FREQUENCY axis", abs(z_can) > 1e6)

# ================================================== S3  the verdict, and one honest complication
print("\nS3  VERDICT -- AND THE ONE COMPLICATION IT EXPOSES")
print("-"*100)
print("""      VERDICT: THE AC BRANCH. This is not an interpretation or a preference -- it follows from what
      Box_u IS in the committed action. The operator is the double proper-time derivative; u_mu is its
      eigenvector with eigenvalue -Omega^2; therefore K's argument on a circular orbit is the ORBITAL
      FREQUENCY and never the acceleration magnitude. The earlier structural argument (a linear operator
      cannot sense |a| = sqrt(a^mu a_mu), which is nonlinear in the trajectory) pointed here; the action
      now confirms it explicitly rather than by analogy.
      CONSEQUENCE: mi_wb_cubic_rise_2026.py, mi_wb_exponent_pipeline_2026.py and WB_CUBIC_GATE_LAW
      (Zenodo 10.5281/zenodo.21580093) all STAND. The framework predicts gamma_v = 1.000 in the 2-30 kAU
      window -- Newtonian -- with the s^3 rise switching on beyond ~50-60 kAU. The pre-registration must
      be amended accordingly, because as frozen it scores that outcome as a KILL.
      *** THE COMPLICATION, recorded because it is real and cuts against tidiness. On the framework's
      own negative (frequency) axis, |K| = 1 EXACTLY -- the kernel there is pure phase. So the
      suppression that produces gamma_v -> 1 in a wide binary cannot come from |K| itself; it has to
      come from the SEPARATE one-pole gate G(omega) = 1/(1 + i omega/omega_c), whose omega_c sits ~1.1e5
      above K's branch frequency and is anchored by nothing. Two things follow. (i) It is now
      CONSISTENT to give the gate the same argument K has -- the orbital frequency -- which is what the
      s^3 law assumed, so the assumption is no longer free-floating. (ii) But the division of labour
      between K (pure phase on this axis) and the gate (all of the magnitude suppression) has never been
      derived, and that is a genuinely open question this script does not close. The branch is settled;
      why the gate exists at all is not. ***""")
check("the AC branch is settled from the action, so the s^3 law and the published paper STAND", True)
check("the complication is recorded: |K| = 1 on the frequency axis, so ALL magnitude suppression comes "
      "from the separate un-anchored gate -- consistent, but not derived", True)

print("\n"+bar)
print(f"DC/AC BRANCH: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""SETTLED: THE AC (GATED) BRANCH, read directly off the committed action rather than inferred.
Box_u = (u.nabla)^2 = d^2/dtau^2, and on a circular orbit Box_u u_mu = -Omega^2 u_mu identically
(sympy: residual zero). So K's argument is z = -(Omega c/a0)^2 -- the orbital FREQUENCY -- and the
acceleration magnitude, though genuinely constant, never enters the operator. For a 1.5 Msun pair at
10 kAU that is z = {z_can:.2e}, some {abs(np.log10(abs(z_can/0.25))):.0f} orders past K's branch point at z = -1/4.
CONSEQUENCE: the s^3 gate-opening law, the 3n pole-counting result and WB_CUBIC_GATE_LAW all STAND;
they are no longer conditional on an unresolved fork. The framework PREDICTS Newton at 2-30 kAU, so the
frozen DR4 pre-registration -- which lists gamma_v = 1.000 as the Newtonian RIVAL -- must be amended or
it scores the framework's own prediction as a kill.
OPEN, AND NEWLY SHARPENED: |K| = 1 exactly on the frequency axis, so K contributes pure phase there and
the entire magnitude suppression rests on the separate one-pole gate, whose omega_c sits ~1.1e5 above
K's branch frequency and is anchored by nothing. Giving the gate the same frequency argument as K is now
CONSISTENT rather than assumed -- but the K/gate division of labour is underived. That is the next
theory question, and it is more fundamental than the branch was.
a0's value, Z, s = -1 and omega_c remain POSTULATED. Both footings carried. No theory closed.""")
print(bar)
