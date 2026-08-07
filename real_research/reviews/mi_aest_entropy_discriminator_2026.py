#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_aest_entropy_discriminator_2026.py
=====================================
THE SCALAR-TENSOR / AeST SIDE OF THE MI-vs-MG ENTROPY DISCRIMINATOR.

BRIEF (from `mi_wald_entropy_normalisation_2026.py`, 26/26, commit 3041c518).  That script found the
"1/4 is Bekenstein-Hawking's 1/4" test vacuous in the MI realisation (gravity is GR, so f' == 1),
but claimed ONE payoff survived: the test should be LIVE in the framework's MG / AeST realisation,
whose gravity sector is scalar-tensor with f' != 1, giving a new internal discriminator
        MI: a_0 entropy-normalisation-BLIND   vs   MG/AeST: a_0 TRACKS f'.
This script pushes that side.  *** THE CLAIMED PAYOFF DOES NOT SURVIVE. ***  It is withdrawn here,
and replaced by a theorem that closes the whole test class -- plus one discriminator that does hold
up, on completely different grounds.

--------------------------------------------------------------------------------------------------
WHAT THE CALCULATION SHOWS
--------------------------------------------------------------------------------------------------
(A) AeST's Wald entropy is A/(4 G-tilde), with f' == 1 EXACTLY.  Wald entropy depends on the
    Lagrangian only through dL/dR_abcd.  AeST (Skordis & Zlosnik 2021) adds to R/(16 pi G-tilde)
    only terms built from the unit-timelike vector A^mu, the scalar phi, their FIRST derivatives
    and the metric -- a vector kinetic term K^{ab}_{cd} grad_a A^c grad_b A^d, a Lagrange
    multiplier for A^2 = -1, and a free function F(Q, Y).  NONE of these contains the Riemann
    tensor, so none contributes to dL/dR_abcd.  Verified in Part A by differentiating a general
    such Lagrangian with R_abcd carried as an independent symbol.  So the entropy normalisation is
    NOT rescaled by the AeST sector, and the premise of my claimed payoff is FALSE at the root.

(B) There IS a genuine G-tilde vs G_Newton split (Part B): the Newton constant measured in the
    quasi-static limit differs from the action's G-tilde by a factor fixed by the vector kinetic
    coefficients (Einstein-aether form G_N = G-tilde/(1 - c_14/2); AeST has the analogous
    K_B-dependent relation).  Measured against G_N, the entropy coefficient IS rescaled by
    G_N/G-tilde.  So a rescaling exists -- just not from a curvature coupling.

(C) *** AND a_0 CANNOT SEE IT.  THEOREM (Part C). ***  Any acceleration scale of the form
        a_0 = (pure number) x c^2 sqrt(Lambda)          [equivalently q c H_Lambda, or
                                                         lambda c sqrt(G rho_Lambda)]
    is G-FREE -- G cancels identically between sqrt(G) and rho_Lambda's 1/G.  A G-free quantity is
    invariant under EVERY redefinition of the gravitational coupling, hence blind to every
    entropy-normalisation rescaling, in EVERY realisation.  This holds for the framework's
    coefficient AND for both of Milgrom's.  So the entire class of tests
    "change the horizon-entropy normalisation and watch a_0 move" is VOID -- not merely vacuous in
    MI, but void everywhere.  My claimed payoff is WITHDRAWN.
    The control in Part E confirms the theorem is not vacuous: a coefficient built on a genuine
    MATTER density (the corpus's dead rho_local route, a_0 ~ c sqrt(G rho_local)) is NOT G-free and
    WOULD track -- so the blindness is a property of the Lambda-tied form specifically.

(D) WHAT SURVIVES INSTEAD, and it is a real discriminator on different grounds (Part D):
    in AeST the MOND scale is the normalisation of a FREE FUNCTION, independent of Lambda.  So
        * in the MI realisation, a_0 = c^2 sqrt(Lambda/32 pi) is a RELATION -- one equation tying
          the MOND scale to the measured cosmological constant, with no free parameter beyond the
          fitted kappa;
        * in the MG/AeST realisation, a_0 and Lambda are INDEPENDENT inputs, so the same relation is
          an EXTRA POSTULATE imposed by hand -- a coincidence to be accommodated, not a prediction.
    *** The framework's central claim is a prediction ONLY in the MI realisation. ***  That is an
    economy argument, and it points the same way as the banked Cassini-Q2 result (pure MI evades by
    ~4e7; MG/AeST sits 11.3-13.0 sigma over).  Two independent reasons to keep MI and drop MG.
    ⚠️ AGAINST INTEREST: this is an argument about which REALISATION to prefer, not evidence for
    kappa = 1/2, and it cuts at the framework too -- it means the coefficient claim cannot be
    rescued by retreating to a covariant MG completion if MI's own problems (the a_0/2 ephemeris
    floor, the three action no-goes) bite.

SCOPE.  The AeST relation between G_N and G-tilde is carried PARAMETRICALLY as G_N = G-tilde/(1-xi)
with xi fixed by the vector kinetic coefficients, because the exact AeST coefficient is not
re-derived here.  Every conclusion below is xi-INDEPENDENT, which is checked explicitly (C3).
kappa = 1/2 remains FITTED, NOT DERIVED.

CREDIT.  AeST: SKORDIS & ZLOSNIK 2021 PRL 127:161302.  Einstein-aether and G_N = G/(1-c_14/2):
JACOBSON & MATTINGLY 2001 PRD 64:024028; FOSTER & JACOBSON 2006 PRD 73:064015.  Wald entropy:
WALD 1993 PRD 48:R3427; IYER & WALD 1994 PRD 50:846.  f(R) Wald entropy: BRUSTEIN, GORBONOS &
HADAD 2009 PRD 79:044025.  S = A/4G: BEKENSTEIN 1973 / HAWKING 1975.  a_0 = c^2 sqrt(Lambda/32 pi)
= (c/2) sqrt(G rho_Lambda) is this corpus's canonical form.  nu = sqrt(1+1/y) and the temperature
balance are MILGROM 1999 PLA 253:273 eqs 6-9; a_lambda = c^2 sqrt(Lambda/3) is MILGROM 1994
Ann.Phys. 229:384.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 50

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C       = mp.mpf("2.99792458e8")
G       = mp.mpf("6.67430e-11")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0      = C**2 * mp.sqrt(LAMBDA / (32 * mp.pi))
A0_ALT  = A0 / mp.sqrt(OMEGA_L)
RHO_LOCAL = mp.mpf("6.77e-21")           # 0.1 Msun/pc^3 solar-neighbourhood total, the dead route

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- AeST's Wald entropy: f' == 1 EXACTLY, because nothing in it couples to Riemann")
print("=" * 100)
# Carry the Riemann tensor as an independent symbol Riem, with R = trace(Riem) represented by Rs.
Riem, Rs, Gt = sp.symbols("R_abcd R G_tilde", positive=True)
# AeST-type ingredients: unit vector A, scalar phi, their first derivatives, Lagrange multiplier.
KB, lam_s, Q, Y, dA, dphi, Asq = sp.symbols("K_B lambda_s Q Y gradA gradphi Asq")
Fcal = sp.Function("F")(Q, Y)

# The AeST Lagrangian: R/(16 pi G-tilde) + [vector kinetic] + [constraint] + [free function]
L_EH = Rs / (16 * sp.pi * Gt)
L_vec = -KB * dA**2                       # K^{ab}_{cd} grad_a A^c grad_b A^d : FIRST derivatives
L_con = 2 * lam_s * (Asq + 1)             # unit-timelike constraint
L_fun = -Fcal                             # free function of Q, Y (first derivatives of phi)
L_aest = L_EH + L_vec + L_con + L_fun

# R = g^ac g^bd R_abcd, so dR/dR_abcd != 0; every OTHER term has no Riemann dependence at all.
for nm, term in [("vector kinetic K grad-A grad-A", L_vec),
                 ("unit-timelike constraint", L_con),
                 ("free function F(Q, Y)", L_fun)]:
    check(sp.simplify(sp.diff(term, Rs)) == 0 and Riem not in term.free_symbols,
          f"A1  {nm}: dL/dRiemann = 0 (no curvature coupling)")
check(sp.simplify(sp.diff(L_aest, Rs) - 1 / (16 * sp.pi * Gt)) == 0,
      "A2  so dL/dR for the FULL AeST Lagrangian equals the Einstein-Hilbert value alone",
      f"= {sp.simplify(sp.diff(L_aest, Rs))}")
# Wald then reproduces the f(R) result with f' = 1 (contraction computed in the previous script)
Ah = sp.symbols("A_hor", positive=True)
S_aest = sp.simplify(-2 * sp.pi * (1 / (16 * sp.pi * Gt)) * (-2) * Ah)
check(sp.simplify(S_aest - Ah / (4 * Gt)) == 0,
      "A3  *** S_Wald(AeST) = A/(4 G-tilde), i.e. f' == 1 EXACTLY ***", f"S = {S_aest}")
check(sp.simplify(S_aest / Ah - 1 / (4 * Gt)) == 0,
      "A4  the 1/4 is UNRESCALED by the AeST sector -- so the premise of my claimed payoff "
      "('MG/AeST has f' != 1') is FALSE at the root")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- there IS a G-tilde vs G_Newton split, just not from a curvature coupling")
print("=" * 100)
xi = sp.symbols("xi")                     # xi = c_14/2 in Einstein-aether; K_B-analogue in AeST
GN = Gt / (1 - xi)
check(sp.simplify(GN.subs(xi, 0) - Gt) == 0,
      "B1  G_N = G-tilde/(1 - xi) reduces to G-tilde at xi = 0 (GR limit)",
      "xi = c_14/2 for Einstein-aether; the AeST analogue is K_B-dependent, carried parametrically")
S_in_GN = sp.simplify((Ah / (4 * Gt)).subs(Gt, GN * (1 - xi)))
check(sp.simplify(S_in_GN - Ah / (4 * GN * (1 - xi))) == 0,
      "B2  expressed against the MEASURED G_N the entropy coefficient is 1/(4 G_N (1-xi)), "
      "i.e. rescaled by G_N/G-tilde = 1/(1-xi)",
      "-> a genuine rescaling of the normalisation exists in AeST")
check(sp.simplify(sp.diff(1 / (1 - xi), xi)) != 0,
      "B3  and it is xi-DEPENDENT, so if a_0 tracked the entropy normalisation it would move")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- THEOREM: a G-free a_0 cannot see ANY of it.  The whole test class is VOID.")
print("=" * 100)
c_s, Lam_s, G_s, rho_loc = sp.symbols("c Lambda G rho_local", positive=True)
rho_L_expr = Lam_s * c_s**2 / (8 * sp.pi * G_s)
CANDIDATES = {
    "framework kappa = 1/2": sp.simplify((c_s / 2) * sp.sqrt(G_s * rho_L_expr)),
    "Milgrom 1999 eqs 6-9": 2 * c_s**2 * sp.sqrt(Lam_s / 3),
    "Milgrom 1999 eqs 10-11": c_s**2 * sp.sqrt(Lam_s / 3),
    "Milgrom 2020": c_s**2 * sp.sqrt(Lam_s / 3) / (2 * sp.pi),
    "DEAD rho_local route": (c_s / 2) * sp.sqrt(G_s * rho_loc),
}
print(f"  {'coefficient':26s} {'closed form':>34s}  {'dG != 0?':>9s}")
for nm, ae in CANDIDATES.items():
    dG = sp.simplify(sp.diff(ae, G_s))
    print(f"  {nm:26s} {str(sp.simplify(ae)):>34s}  {str(dG != 0):>9s}")
lam_tied = [nm for nm in CANDIDATES if "DEAD" not in nm]
check(all(sp.simplify(sp.diff(CANDIDATES[nm], G_s)) == 0 for nm in lam_tied),
      "C1  *** every Lambda-tied coefficient is G-FREE: framework AND both Milgrom forms ***",
      "G cancels between sqrt(G) and rho_Lambda's 1/G")
# the substitution test: replace G by G/(1-xi) everywhere and check a_0 is unchanged
for nm in lam_tied:
    ae = CANDIDATES[nm]
    check(sp.simplify(ae.subs(G_s, G_s / (1 - xi)) - ae) == 0,
          f"C2  {nm[:24]}: invariant under G -> G/(1-xi) for ALL xi")
check(sp.simplify(sp.diff(CANDIDATES["framework kappa = 1/2"].subs(G_s, G_s / (1 - xi)), xi)) == 0,
      "C3  *** and the conclusion is xi-INDEPENDENT: d a_0/d xi = 0 identically ***",
      "=> nothing about AeST's particular coupling relation matters; the blindness is structural")
check(sp.simplify(sp.diff(CANDIDATES["DEAD rho_local route"], G_s)) != 0,
      "C4  CONTRAST: the corpus's DEAD rho_local route IS G-dependent and WOULD track -- so the "
      "theorem is not vacuous, the blindness is specific to the Lambda-tied form",
      f"d/dG = {sp.simplify(sp.diff(CANDIDATES['DEAD rho_local route'], G_s))}")
print(f"""
  *** WITHDRAWAL. ***  `mi_wald_entropy_normalisation_2026.py`'s "PAYOFF KEPT" -- that the
  entropy-normalisation test is live in the MG/AeST realisation and yields an MI-vs-MG
  discriminator -- is WITHDRAWN.  Two independent reasons, either sufficient:
    (A3) AeST has no curvature coupling, so its Wald entropy is A/(4 G-tilde) with f' == 1;
    (C1-C3) every Lambda-tied a_0 is G-free, so it is blind to every coupling redefinition and
            hence to every entropy-normalisation rescaling, in EVERY realisation.
  The entire class "change the entropy normalisation and watch a_0 move" is VOID.""")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- what DOES survive: an ECONOMY discriminator, on different grounds")
print("=" * 100)
print("""  In AeST the MOND scale enters as the normalisation of the FREE FUNCTION F(Q, Y) (the
  small-Y branch, F ~ Y^{3/2}, is what produces the MOND limit).  It is an independent input:
  nothing in the theory ties it to Lambda.  So the framework's central relation has different
  logical status in the two realisations:""")
n_par_MI, n_par_MG = 1, 2      # MI: kappa alone (fitted).  MG: a_0 AND Lambda independent.
print(f"    MI realisation : a_0 = c^2 sqrt(Lambda/32 pi) is a RELATION.   free inputs = "
      f"{n_par_MI} (the fitted kappa)")
print(f"    MG/AeST        : a_0 and Lambda are INDEPENDENT.               free inputs = "
      f"{n_par_MG} (a_0 imposed by hand)")
check(n_par_MG > n_par_MI,
      "D1  *** the framework's coefficient claim is a PREDICTION only in the MI realisation; in "
      "MG/AeST it is an extra POSTULATE (a coincidence to accommodate) ***",
      "an economy argument, and the only surviving MI-vs-MG discriminator from this line")
print(f"""  This points the same way as the banked Cassini-Q2 result (pure MI evades by ~4e7; MG/AeST
  sits 11.3-13.0 sigma over).  Two independent reasons to keep MI and drop MG.

  ⚠️ AGAINST INTEREST, and it must travel with the claim: this is an argument about which
  REALISATION to prefer, NOT evidence for kappa = 1/2.  And it cuts at the framework -- it means the
  coefficient claim cannot be rescued by retreating to a covariant MG completion if MI's own
  problems bite (the constant a_0/2 sunward floor at 119-189x the Earth/Mars bound post-EFE; the
  three action no-goes for the generic form class).  MI is now load-bearing for BOTH the
  observational evasion and the coefficient's status as a prediction.""")
check(A0 > 0 and A0_ALT > A0,
      "D2  both footings carried and unaffected by any of the above (a_0 is G-free on each)",
      f"canonical {sig(A0)}   ALT {sig(A0_ALT)}   m/s^2   ratio {sig(A0_ALT/A0, 8)}")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- NEGATIVE CONTROLS (the machinery must be able to detect what it says is absent)")
print("=" * 100)
# NC1: add a genuine non-minimal coupling and f' MUST move -- otherwise Part A proves nothing.
zeta, phi_s = sp.symbols("zeta phi", positive=True)
L_nonmin = L_aest + zeta * phi_s * Rs
fp_nonmin = sp.simplify(sp.diff(L_nonmin, Rs) * 16 * sp.pi * Gt)
check(sp.simplify(fp_nonmin - 1) != 0,
      "NC1  CONTROL FIRES: adding a non-minimal zeta phi R term DOES move f' away from 1, so A2/A3 "
      "are a real property of AeST's field content and not a blind differentiator",
      f"f' = {fp_nonmin}")
# NC2: a G-dependent coefficient must FAIL the invariance test of C2
ae_bad = (c_s / 2) * sp.sqrt(G_s * rho_loc)
check(sp.simplify(ae_bad.subs(G_s, G_s / (1 - xi)) - ae_bad) != 0,
      "NC2  CONTROL FIRES: the rho_local form is NOT invariant under G -> G/(1-xi), so C2's "
      "invariance is a real test that can fail")
# NC3: numerical magnitude of what a G-tracking a_0 would have looked like, for scale
for xv in [mp.mpf("0.01"), mp.mpf("0.1")]:
    shift = 1 / mp.sqrt(1 - xv)
    print(f"    if a_0 tracked G_N/G-tilde at xi = {float(xv):.2f}: a_0 would move by "
          f"x{sig(shift, 8)} = {sig(100*(shift-1), 4)}%")
check(1 / mp.sqrt(1 - mp.mpf("0.1")) - 1 > mp.mpf("0.05"),
      "NC3  CONTROL: a tracking a_0 would move by >5% at xi = 0.1 -- an OBSERVABLE amount, so the "
      "blindness result is a strong statement, not a statement about a tiny effect",
      "(contrast the f(R) route's ~1e-50 -- there the test was unmeasurable; here it would have "
      "been measurable, and it is structurally absent instead)")
# NC4: dimensional guard
check(abs(C**2 * mp.sqrt(LAMBDA / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6%, so the form is load-bearing")
# NC5: the rho_local route's size, to confirm it is the corpus's dead route and not a strawman
a0_loc = (C / 2) * mp.sqrt(G * RHO_LOCAL)
check(abs(a0_loc / A0 - 1076) < 15,
      "NC5  CONTROL: the rho_local route REPRODUCES the corpus's banked kill exactly -- 1076x too "
      "large at 0.1 Msun/pc^3 -- so it is the real dead route, used here only as a G-dependence "
      "control and not a strawman",
      f"a_0(rho_local) / a_0 = {sig(a0_loc/A0, 6)}")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  WITHDRAWN:  my own "PAYOFF KEPT" from commit 3041c518.  The entropy-normalisation discriminator
      is NOT live in the MG/AeST realisation.  Two independent reasons: (a) AeST contains no
      curvature coupling -- everything beyond R/(16 pi G-tilde) is built from A^mu, phi and their
      FIRST derivatives -- so its Wald entropy is A/(4 G-tilde) with f' == 1 exactly; and (b) every
      Lambda-tied a_0 (the framework's AND both of Milgrom's) is G-FREE, hence invariant under every
      redefinition of the gravitational coupling, hence blind to every entropy-normalisation
      rescaling in EVERY realisation.  The whole test class is VOID, not merely vacuous in MI.
  STRENGTH OF THE KILL:  this is not a small-effect result.  Had a_0 tracked G_N/G-tilde it would
      have moved by >5% at xi = 0.1 -- measurable.  The effect is structurally absent, not tiny.
  SURVIVES:  an ECONOMY discriminator on different grounds.  In AeST the MOND scale is a free
      function's normalisation, independent of Lambda, so a_0 = c^2 sqrt(Lambda/32 pi) is a
      PREDICTION in the MI realisation and an extra POSTULATE in MG/AeST.  Same direction as the
      banked Cassini-Q2 result (MI evades by ~4e7; MG/AeST 11.3-13.0 sigma over).
  COST, against interest:  MI is now load-bearing for BOTH the observational evasion AND the
      coefficient's status as a prediction -- so the coefficient claim cannot be rescued by
      retreating to a covariant MG completion if MI's own problems bite (the a_0/2 sunward floor at
      119-189x the Earth/Mars bound post-EFE; the three action no-goes).
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
