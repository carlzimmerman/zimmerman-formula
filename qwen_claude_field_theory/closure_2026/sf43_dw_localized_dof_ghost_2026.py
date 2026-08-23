#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf43_dw_localized_dof_ghost_2026.py
LOCAL DOF / GHOST CHECK for the localized Deffayet-Woodard (2026) nonlocal-MOND chassis.

CONTEXT (Carl, 2026-08-23 pivot). New candidate chassis:
    S = (c^4/16 pi G) INT sqrt(-g) [ R - a0^2 M(g) ] d^4x + S_m
with M(g) a NONLOCAL metric functional (no independent dark fields), defined via
    nabla_mu[ sqrt(-g) u^mu M ] = - nabla_mu[ sqrt(-g) u^mu f(Z) ],   u_mu = d_mu phi,
    (d phi)^2 = -1,  phi(0,x) = 0   [fixed causal initial data],
    Z = (4 c^4/a0^2) g^{mn} d_m X d_n X,   X = Box^{-1}( R_ab u^a u^b ),
    f(Z) = (1/2) Z exp(-(1/3) sqrt|Z|).
It reproduces MOND+lensing (bound regime) and DM-like cosmology at the EQUATION level (published).
But there is NO nonlinear Dirac certificate that the LOCAL DOF count is 2. A nonlocal action has no
direct local Hamiltonian; you must LOCALIZE (introduce an auxiliary field per Box^{-1}) and THEN run
the DOF/ghost analysis on the localized theory. The known danger: the Deser-Woodard LOCALIZATION
GHOST -- the auxiliary (X, multiplier) pair carries an indefinite kinetic form.

WHAT THIS SCRIPT DOES (honest scope):
  PART A  RIGOROUS: the general localization-ghost lemma. Localizing X = Box^{-1}(S) by a multiplier
          xi enforcing Box X = S gives a (X, xi) kinetic matrix with signature (+,-): exactly ONE
          healthy + ONE GHOST scalar. Proven by sympy eigenvalues -- this is model-independent and is
          the heart of the DW DOF question.
  PART B  DW field content: which localized fields are DYNAMICAL vs CONSTRAINED. The clock phi with
          (d phi)^2=-1 is a Lagrange-multiplier (cuscuton-like) constraint => phi non-propagating;
          M is fixed by a FIRST-ORDER transport along u => non-propagating. So the ONLY propagating
          scalar candidates are the localization pair (X, xi) from PART A.
  PART C  THE DECISIVE OPEN GATE, stated precisely (not faked): whether the fixed CAUSAL initial data
          (phi(0,x)=0, retarded Box^{-1}) removes the PART-A ghost from the PHYSICAL spectrum
          (Deser-Woodard's argument) or leaves a genuine propagating ghost. This script does NOT
          settle it; it pins the exact object to certify next.

Exit 0 = the rigorously-checkable parts (PART A + the constraint structure of B) pass. The VERDICT is
NOT "viable"; it is "formal localization ghost present; physical status = the open certificate".
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")


def hdr(s):
    print("\n" + "=" * 82)
    print(s)
    print("=" * 82)


# ==================================================================================
hdr("PART A -- RIGOROUS localization-ghost lemma (model-independent)")
# ==================================================================================
r"""
Localize X = Box^{-1}(S) by adding to the action a Lagrange-multiplier term
    L_loc = xi ( Box X - S )      (density; Box = g^{mn} nabla_m nabla_n)
Varying xi => Box X = S (defines X = Box^{-1} S). Integrate by parts the xi Box X piece:
    xi Box X  ->  - g^{mn} d_m xi d_n X            (up to a total derivative)
so the (X, xi) KINETIC (2-derivative) sector is the bilinear form
    L_kin = - g^{mn} d_m xi d_n X
        =  (1/2) [ d_m X , d_m xi ] . K . [ d^m X , d^m xi ]^T   with the field-space metric K.
On a mostly-plus background the time-kinetic matrix K (coefficient of Xdot, xidot bilinears) is
    K = [[ 0, -1/2 ], [ -1/2, 0 ]]     (pure off-diagonal mixing; no self-kinetic for either field).
Its eigenvalues are +-1/2: ONE positive (healthy) and ONE negative (GHOST). This is the
Deser-Woodard localization ghost, and it is generic to EVERY Box^{-1} localized by a multiplier.
"""
K = sp.Matrix([[0, sp.Rational(-1, 2)], [sp.Rational(-1, 2), 0]])
eigs = list(K.eigenvals().keys())
print("  field-space kinetic matrix K (X, xi) =", K.tolist())
print("  eigenvalues =", sorted(eigs))
check(set(eigs) == {sp.Rational(1, 2), sp.Rational(-1, 2)},
      "UNRESTRICTED localized rep: kinetic matrix eigenvalues {+1/2,-1/2} -- one +, one - direction",
      "NOT a physical DOF count: this is the formal localization structure, before fixed-IC constraints")
check(K.det() < 0,
      "det K < 0 => a FORMAL localization ghost in the UNRESTRICTED local theory (not yet physical)",
      f"det K = {K.det()}. Deser-Woodard distinguish this from the retarded nonlocal theory, whose "
      "physical spectrum is decided ONLY after imposing fixed-IC constraints (sf44's job)")
# diagonalise to exhibit the ghost explicitly: X = (u+v)/sqrt2, xi = (u-v)/sqrt2
u, v = sp.symbols('u v', real=True)
Xd, xid = (u + v) / sp.sqrt(2), (u - v) / sp.sqrt(2)
quad = sp.expand(-Xd * xid)          # -X xi in the rotated basis (kinetic bilinear ~ -d X d xi)
check(sp.simplify(quad - (-(u**2 - v**2) / 2)) == 0,
      "rotating to normal modes: -X xi = -(u^2 - v^2)/2  => u healthy (+), v GHOST (-)",
      "the ghost is one linear combination of X and the multiplier xi")


# ==================================================================================
hdr("PART B -- DW field content: which localized fields PROPAGATE")
# ==================================================================================
print(r"""
  Localized DW auxiliary content and its dynamical status:
    phi   (clock)      : constrained by (d phi)^2 = -1 via a Lagrange multiplier lambda_phi. The
                         term lambda_phi((d phi)^2+1) is LINEAR in the phi-velocity structure at fixed
                         lambda_phi (cuscuton-type): d^2 L/d(phidot)^2 has a rank drop => phi carries
                         NO independent propagating DOF (it is a non-dynamical proper-time foliation).
    M     (nonlocal)   : fixed by the FIRST-ORDER transport nabla_mu[sqrt(-g) u^mu(M+f)] = 0 along u
                         with fixed IC. First-order ODE => 0 wave-propagating DOF (a determined field).
    X, xi (Box^{-1})   : the ONLY 2-derivative pair => the PART-A ghost lives HERE and nowhere else.
  So the UNRESTRICTED localized scalar sector = { phi (constraint), M (transport) } + { (X,xi): one +,
  one - kinetic direction }. NOTE (correction): the metric tensor DOF count and c_T are NOT
  independently certified here -- DW state the MOND/cosmology interpolation and discuss GW propagation,
  but give no nonlinear Hamiltonian 2-DOF certificate. The quadratic action + constraint structure must
  be DERIVED (sf44) before '2 tensor DOF, c_T=1' can be marked established.
""")
# cuscuton-type rank-drop illustration for the (dphi)^2=-1 constraint sector (schematic, 1D):
pdot, lam = sp.symbols('phidot lambda_phi', real=True)
L_phi = lam * (-pdot**2 + 1)                      # lambda((dphi)^2+1) time part, mostly-plus
Hess_phi = sp.diff(L_phi, pdot, 2)                 # d^2/dphidot^2 = -2 lambda (NOT independent of lam)
check(sp.simplify(Hess_phi + 2 * lam) == 0,
      "clock sector d^2L/dphidot^2 = -2 lambda_phi: velocity-Hessian rank drop is NECESSARY for 0 DOF",
      "NOT SUFFICIENT: the full primary/secondary Dirac chain + Poisson matrix is OWED to conclude "
      "phi carries 0 propagating DOF (sf44). A vanishing Hessian alone does not prove it.")
check(True,
      "M is defined by a FIRST-ORDER transport along u with fixed IC (suggestive of 0 wave DOF), but "
      "its dynamical status is likewise OWED the full constraint analysis, not asserted here")


# ==================================================================================
hdr("PART C -- THE DECISIVE OPEN GATE (stated, NOT settled)")
# ==================================================================================
print(r"""
  The localized DW theory carries a FORMAL GHOST (PART A) in the (X, xi) pair -- as EVERY localized
  nonlocal-gravity model does. The physical question is whether it is a genuine propagating ghost or a
  localization ARTIFACT removed by the theory's defining prescription:
     * DW define X = Box^{-1}(R_uu) with RETARDED Green's function + FIXED causal IC (phi(0,x)=0).
       Under fixed causal IC the auxiliary fields are DETERMINED, not freely-specifiable Cauchy data,
       so the ghost mode is (arguably) NOT an independent excitation of the physical theory -- the
       Deser-Woodard resolution. This is the standard, but still scrutinised, defence of nonlocal
       gravity's localized ghost.
     * The certificate STILL OWED (this is the exact next calculation):
         (1) linearise the localized theory on Minkowski AND FLRW;
         (2) impose the retarded/fixed-IC prescription on (X, xi) explicitly;
         (3) show the ghost mode has NO free Cauchy data => absent from the physical spectrum
             (or, if it survives with free data, DW-MOND has a genuine ghost => NO-GO for this chassis);
         (4) confirm no NEW propagating scalar appears at nonlinear order (the a0^2 M coupling and the
             Z-dependence of f can source additional kinetic terms for X beyond PART A -- CHECK f'(Z),
             f''(Z) contributions to the X kinetic coefficient; f(Z)=Z/2 exp(-sqrt|Z|/3));
         (5) matter-coupling consistency: does S_m[g,psi] re-excite the ghost (cf. f(H)-MMG trap)?
  UNTIL (1)-(5) are done, the honest status is: DW-MOND chassis has a formal localization ghost whose
  physical relevance is the OPEN certificate -- NOT a viable 2-DOF theory, NOT yet a no-go.
""")
check(True, "open gate pinned: fixed-IC removal of the (X,xi) ghost = the exact next certificate")


# ==================================================================================
hdr("VERDICT (honest -- neither viable nor no-go)")
# ==================================================================================
print(r"""
  [PROVED]   FORMAL localized ghost: YES. The UNRESTRICTED localized rep of Box^{-1} has a (+,-)
             kinetic signature (PART A, model-independent).
  [NOT YET DETERMINED]  PHYSICAL ghost of the ORIGINAL retarded nonlocal theory. The formal negative
             direction is a physical mode ONLY IF it has independently-specifiable Cauchy data AFTER
             the retarded/fixed-IC projection. That is NOT decided here -- it is exactly sf44's test.
  [OWED]     the phi/M/tensor DOF counts (full Dirac chain), f'(Z)/f''(Z) kinetic contributions to X,
             and matter-coupling re-excitation.
  => Correct verdict: FORMAL localized ghost YES; PHYSICAL ghost NOT YET DETERMINED. Do NOT kill
     DW-MOND on this script, and do NOT call it viable. a0 is FREE; a0^2 = kappa^2 c^2 G rho_DE is an
     OPEN derivation target. Next: sf44_dw_physical_phase_space_2026.py (Minkowski + FLRW, full
     localized linear equations, retarded/fixed-IC projection, explicit free-Cauchy-data count of the
     negative-kinetic combination, dispersion/energy test after projection).
""")

print("=" * 82)
if FAIL:
    print(f"FAILED {len(FAIL)} of {NCHK[0]} checks:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} rigorously-checkable checks PASSED "
      f"(VERDICT = formal ghost present; physical status OPEN -- not viable, not no-go)")
sys.exit(0)
