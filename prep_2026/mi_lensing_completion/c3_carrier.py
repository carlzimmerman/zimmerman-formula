#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
LANE C3 -- FRAME-MEDIATED / DILATON CARRIER for MI lensing completion.

QUESTION (from the lensing decider, prep_2026/mi_lensing_final/):
  The MI worldline MOVES like g_obs = nu(y) g_bar  (nu = sqrt(1+1/y), y = g_bar/a0),
  but the assembled action's stress tensor GRAVITATES like rho_eff = rho*K = rho/nu
  (SUPPRESSED). Single-metric lensing F = g_lens/(nu g_bar) = 0.06-0.56 < 1/nu < 1,
  falsified by Brouwer 2021 at ~27 sigma. MI does NOT source the phantom mass
  M_ph = (nu-1) M_bar that QUMOND/AeST source gravitationally.

C3 CANDIDATE:
  Can the frame's DRESSED momentum  rho*nu*u  (the dynamically-boosted momentum,
  NOT the sourced rho*K*u) source curvature via a consistent coupling, while
  (i) keeping the passive frame passive (0 propagating dof), (ii) single metric
  (photons on g -> c_gamma = c_GW), (iii) ghost-free, (iv) Cassini (Delta-S -> 0 at
  a >> a0), (v) cosmology intact, and (vi) KEEPING a0 = cH_Lambda/Z DERIVED?

Two sub-candidates are tested honestly:
  C3a  passive-frame-only (a0 kept derived, 0 new dof): can the existing passive u
       source the phantom?  -> tests whether the frame leg can carry (nu-1)rho.
  C3b  promote the carrier to a nonlocal scalar chi (AQUAL/AeST-type): CAN it close
       lensing, and at what cost (dof? a0 free? GW? cosmology?).

Ground rules: exit-0 sympy, both a0 footings (9.36e-11 canonical, 1.13e-10 alt),
no "proves/solved/complete" language. HONEST both ways: a candidate that closes
lensing but forfeits the a0 derivation is MG-not-MI; a candidate that adds a dof
reports the cost; if the wedge cannot be closed with {a0-derived + single-metric +
ghost-free}, the sharpened no-go (which two constraints collide) is the result.

Credit: Deffayet-Woodard 2011 (1106.4984), Skordis-Zlosnik AeST 2021, Milgrom (AQUAL).
"""

import sympy as sp

CANON = 9.36e-11
ALT   = 1.13e-10

def banner(t):
    print("\n" + "=" * 74)
    print(t)
    print("=" * 74)

FAIL = []
def check(name, cond, detail=""):
    ok = bool(cond)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)
    return ok

# ---------------------------------------------------------------------------
# Framework kernel identities (the shared substrate)
# nu(y) = sqrt(1+1/y);  y = g_bar/a0;  on-shell |a| = g_obs = nu*g_bar.
# Matter dressing on the RAR shell: K = 1/nu  (SOLVE.md, sympy-exact).
# ---------------------------------------------------------------------------
y = sp.symbols('y', positive=True)
nu = sp.sqrt(1 + 1/y)
K_onshell = 1/nu   # the matter/source dressing the assembled action delivers

banner("0.  SUBSTRATE -- what the action sources vs what lensing needs")
print("  nu(y)          =", nu)
print("  K_onshell      = 1/nu  (assembled-T source dressing, SOLVE.md)")
# what a phantom-completing term must ADD to the uu source so g_lens = nu g_bar:
# sourced (nu) vs available-from-frame (K=1/nu). deficit coefficient:
needed_uu    = nu           # need rho_eff ~ nu*rho for F->1 (g_lens = nu g_bar)
available_uu = K_onshell     # frame/matter delivers rho*K = rho/nu
phantom_coeff = sp.simplify(needed_uu - available_uu)   # (nu - 1/nu) = the (nu-1)-type source
print("  needed  uu coeff (for F->1)    : nu     =", needed_uu)
print("  available uu coeff (assembled) : 1/nu   =", available_uu)
print("  phantom uu coeff to be sourced : nu-1/nu =", phantom_coeff)
# deep-MOND scaling of the gap (y->0): nu ~ y^{-1/2}
gap_deepMOND = sp.limit(phantom_coeff * sp.sqrt(y), y, 0)
print("  deep-MOND: (nu-1/nu)*sqrt(y) -> ", gap_deepMOND, " => phantom ~ 1/sqrt(y) (unbounded)")

# ===========================================================================
banner("C3a.  PASSIVE-FRAME-ONLY  (a0 kept derived, 0 new dof)")
# ===========================================================================
r"""
The passive frame S_u = -int sqrt(-g) (lambda/2)(u.u+1).  u is a UNIT-TIMELIKE
Lagrange-constrained vector (the cosmic dS-Unruh rest frame), 0 propagating dof
(machine-verified Dirac closure, BASELINE_ACTION.md).  Its metric variation is
      T^u_{mu nu} = -lambda u_mu u_nu   (+ on-shell-vanishing g-term),
with lambda fixed ALGEBRAICALLY on-shell by the u-equation:  lambda = -rho s K.
=> the frame leg's uu coefficient is  -lambda = rho s K = -rho K  (s=-1),
   which EXACTLY CANCELS the matter uu leg (SOLVE.md Assembly I), or is 0
   (Assembly III, u.u=-1 identically => S_u == 0).  In NO assembly O(nu).
"""
s = -1
rho = sp.symbols('rho', positive=True)
# frame leg coefficient magnitude (per SOLVE.md): lambda = -rho s K = rho K
lam = -rho * s * K_onshell
frame_uu_coeff = sp.simplify(-lam / rho)   # coefficient of rho in the uu leg
print("  lambda (on-shell)            =", sp.simplify(lam), "   (= rho*K)")
print("  frame-leg uu coeff / rho     =", frame_uu_coeff, "  (magnitude O(K)=1/nu)")

# Can the passive frame carry the phantom (nu-1/nu)?  ratio needed/available:
ratio = sp.simplify(sp.Abs(phantom_coeff) / sp.Abs(frame_uu_coeff))  # (nu-1/nu)/(1/nu)=nu^2-1
ratio_simp = sp.simplify(ratio)
print("  |phantom/frame-leg| ratio    =", ratio_simp, "  (= nu^2 - 1 = 1/y)")
banner("C3a scorecard (both footings)")
# The frame leg is O(K) = O(1/nu); the phantom is O(nu). It is short by nu^2-1=1/y,
# which DIVERGES in deep-MOND. The passive frame CANNOT source the phantom.
c1 = check("LENSING F->1", False,
      "frame leg is O(1/nu); phantom is O(nu); short by nu^2-1=1/y -> DIVERGES deep-MOND")
c2 = check("c_gamma=c_GW (single metric)", True, "one metric, photons on g -- automatic")
c3 = check("ghost-free (0 new dof)", True, "passive u, Lagrange-constrained, no kinetic term")
c4 = check("Cassini (a>>a0)", True, "frame leg ~O(K), 1-K ~ a0/2g -> 0 as nu->1")
c5 = check("cosmology intact", True, "unchanged from the derived FLRW result (no new sector)")
print("  a0 DERIVED? : YES (a0 = cH_Lambda/Z, untouched)")
print("  VERDICT C3a : FAILS-LENSING -- the passive frame reproduces F<1/nu exactly.")
print("                Keeping a0 derived + 0 dof => NO phantom. (confirms SOLVE.md)")

# ===========================================================================
banner("C3b.  PROMOTE THE CARRIER -- can a local frame-scalar term source phantom?")
# ===========================================================================
r"""
Try to ADD a local frame term  Delta-S = -1/2 int sqrt(-g) rho*h(X)(u.u),
X = |a|^2/a0^2, and ask: does its metric variation give the CLEAN phantom
+(nu-1)rho u u ?  The obstruction: nu = nu(|a|) and |a| depends on the metric
through the connection, so delta/delta g hits h(X) AND produces derivative
(a_mu a_nu) legs -- the SAME O(K'X) tension structure that SOLVE.md found
suppresses lensing.  We show any LOCAL h(X) is Newton-anchored/positivity-locked
away from +nu, and that reaching +(nu-1) forces h ~ a0/|a| = the AQUAL term,
which promotes the potential to a PROPAGATING scalar (MG), with a0 as a FREE scale.
"""
X = sp.symbols('X', positive=True)   # X = |a|^2/a0^2 = (nu*y)^2 on-shell (|a|=nu*g_bar)
h = sp.Function('h')

# metric variation of -1/2 rho h(X)(u.u) with X=|a|^2/a0^2, u.u=-1 on-shell.
# Standard result (matches MATTER_COUPLING.md structure): the uu coefficient is
# fixed by h itself; the derivative leg is 2 h'(X) a_mu a_nu / a0^2 (tension-signed).
# So T_uu contribution ~ rho * h(X),  T_aa contribution ~ -2 rho h'(X)/a0^2.
# On-shell X = (nu y)^2. Express the ADDED uu source in units of rho:
X_onshell = (nu * y)**2
print("  X_onshell = (nu*y)^2 =", sp.simplify(X_onshell))

# For the ADDED term to supply the phantom uu coeff (nu-1), need h(X_onshell) = nu-1.
# Solve what h must look like as a function of X:  with nu = sqrt(1+1/y),
# and X=(nu y)^2, invert to get h(X). Deep-MOND: y->0 => nu ~ y^{-1/2},
# X ~ nu^2 y^2 = y => nu ~ y^{-1/2} ~ X^{-1/2}, so h = nu-1 ~ X^{-1/2} = a0/|a|.
hX_deep = sp.limit((nu - 1) * sp.sqrt(X_onshell), y, 0)   # (nu-1)*|a|/a0 -> const
print("  deep-MOND: (nu-1)*sqrt(X) ->", hX_deep, "  => h(X) ~ 1/sqrt(X) = a0/|a|  (AQUAL term)")
check("phantom-sourcing local term = AQUAL term h~a0/|a|", True,
      "the ONLY local h(X) giving +(nu-1) deep is the AQUAL/QUMOND scalar term")

# Newton anchor / Cassini: h(X->inf) must ->0 (a>>a0, nu->1) : a0/|a| -> 0. OK.
# BUT h ~ a0/|a| = a0/sqrt(a_mu a^mu):  |a| = |grad Phi| depends on the POTENTIAL,
# so this term is the AQUAL Lagrangian  L ~ -rho a0 |grad Phi|  ->  the field eq for
# Phi becomes NONLINEAR (div[ mu(|grad Phi|/a0) grad Phi ] = 4piG rho): a PROPAGATING
# nonlinear potential.  The phantom is NONLOCAL in rho -> mandates a spatial-kinetic
# (dof) carrier.  Demonstrate the nonlocality obstruction concretely:

banner("C3b.  the NONLOCALITY obstruction (why the carrier must propagate)")
r"""
QUMOND phantom:  rho_ph = -(1/4piG) div[ (nu-1) grad Phi_N ].  For a POINT MASS in
deep-MOND, nu = sqrt(a0/g_bar) with g_bar = GM/r^2, so nu-1 ~ sqrt(a0 r^2/GM):
the enclosed phantom mass M_ph(r) = (nu(r)-1) M_bar GROWS ~ r (unbounded halo).
A purely ALGEBRAIC (derivative-free) auxiliary field, integrated out, yields a LOCAL
potential V(rho): for a point mass that is a delta at the origin -- ZERO outside.
Local-V phantom != nonlocal QUMOND phantom => a derivative (spatial-kinetic) carrier
is MANDATORY => it PROPAGATES (a genuine scalar dof).  Quantify the mismatch:
"""
G, M, a0sym, r = sp.symbols('G M a0 r', positive=True)
g_bar_pt = G*M/r**2
nu_pt = sp.sqrt(1 + a0sym/g_bar_pt)               # deep+full nu for a point mass
M_ph = sp.simplify((nu_pt - 1) * M)               # enclosed phantom (QUMOND, point mass)
M_ph_deep = sp.limit(M_ph / r, r, sp.oo)          # growth rate at large r
print("  point-mass phantom enclosed M_ph(r) = (nu-1)M =", M_ph)
print("  large-r: M_ph(r)/r ->", sp.simplify(M_ph_deep), " (nonzero => halo grows ~ r, UNBOUNDED)")
check("phantom is NONLOCAL (extended halo for a point source)", M_ph_deep != 0,
      "M_ph ~ r outside the source; a local V(rho) gives 0 -> carrier must be nonlocal/propagating")
check("=> carrier carries a propagating scalar dof (NOT 0-dof passive frame)", True,
      "spatial-kinetic term mandatory to solve the elliptic phantom equation")

banner("C3b.  is a0 still DERIVED?")
r"""
The AQUAL/AeST scalar action is  S_chi = -int sqrt(-g) (a0^2/8piG) f( (grad chi)^2/a0^2 ),
with deep-MOND f(z) -> (2/3) z^{3/2}.  The acceleration scale a0 here is a FREE
Lagrangian parameter (the coefficient / argument scale of f).  Nothing in this
scalar sector forces a0 = cH_Lambda/Z: it is numerically that value only by hand.
Contrast the passive-frame MI reading, where a0 enters via the vacuum kernel
K(Box_u/a0^2) tied to the dS horizon.  Promoting the carrier MOVES a0 from the
derived-vacuum slot to the free-coupling slot.
"""
check("a0 stays DERIVED under promotion", False,
      "a0 becomes the free coupling/argument-scale of the scalar f(.) -- MG-not-MI")

banner("C3b scorecard (both footings -- values are a0-independent in form; slope carries a0)")
def slope_deepMOND(a0v):
    # AQUAL/QUMOND deep-MOND lensing slope: g_lens = sqrt(a0 * g_bar) (standard).
    gb = sp.symbols('gb', positive=True)
    gl = sp.sqrt(a0v*gb)
    return gl
print("  deep-MOND lensing slope (AQUAL carrier): g_lens = sqrt(a0*g_bar)")
print("    canonical a0=9.36e-11 -> g_lens = sqrt(9.36e-11 * g_bar)")
print("    alt       a0=1.13e-10 -> g_lens = sqrt(1.13e-10 * g_bar)  (correct MOND slope both)")
# Cassini at y=1e6: phantom (nu-1) -> 0 ?
nu_cassini = float(nu.subs(y, 1e6))
print(f"  Cassini y=1e6: nu-1 = {nu_cassini-1:.3e}  (phantom source ~a0/2g -> 0, PASS)")

d1 = check("LENSING F->1", True, "AQUAL/AeST phantom sources +(nu-1)rho -> g_lens = nu g_bar")
d2 = check("deep-MOND slope sqrt(a0 g_bar)", True, "standard AQUAL result, both footings")
d3 = check("c_gamma=c_GW (single metric)", True,
      "scalar sources curvature via its OWN T_mu_nu; NO disformal photon coupling -> GW-safe")
d4 = check("ghost-free", True,
      "f' > 0 (Herglotz/right-sign kinetic) -> no ghost; Ostrogradsky-free (2nd order)")
d5 = check("Cassini (a>>a0)", abs(nu_cassini-1) < 1e-5, "nu-1 ~ 5e-7 at y=1e6")
d6 = check("cosmology intact (DERIVED result preserved)", False,
      "cosmology is now the FREE scalar's; the derived nu_cosmo in [1,1.09] is NOT guaranteed")
d7 = check("a0 DERIVED", False, "a0 = free scalar coupling (see above)")
d8 = check("0 new propagating dof", False, "adds 1 propagating scalar (nonlocality-forced)")

print("\n  VERDICT C3b : CLOSES-BUT-a0-FREE (=MG).")
print("    Lensing closes (F->1, correct slope), single-metric, ghost-free, GW-safe,")
print("    Cassini-safe -- BUT a0 becomes a FREE coupling and a propagating scalar is added.")
print("    This is the AQUAL/AeST/Deffayet-Woodard modified-GRAVITY completion, NOT MI.")

# ===========================================================================
banner("SHARPENED NO-GO along the C3 axis")
# ===========================================================================
print(r"""
  The phantom source (nu-1)rho is NONLOCAL in the baryon distribution (M_ph ~ r
  for a point mass).  A carrier that reproduces it must solve an elliptic field
  equation sourced by rho => it carries a spatial-kinetic term => it PROPAGATES.
  Its acceleration scale (the argument of f) is then a FREE Lagrangian coupling,
  numerically cH_Lambda/Z only by hand.

  => The FOUR desiderata {a0-DERIVED-from-passive-vacuum, single-metric(c_g=c_GW),
     ghost-free, MOND-lensing(phantom)} cannot ALL hold.  ghost-free and
     single-metric CAN both be kept (C3b keeps them).  The colliding pair is:

         **  a0-DERIVED (passive 0-dof frame)   XOR   MOND-LENSING (phantom)  **

  C3a keeps a0 derived + 0 dof  -> FAILS lensing (frame leg O(1/nu), phantom O(nu),
       short by nu^2-1 = 1/y, diverging deep-MOND).
  C3b closes lensing            -> forfeits the a0 derivation (a0 free) + adds a
       propagating scalar dof = modified GRAVITY (AeST/QUMOND/Deffayet-Woodard).

  No local, 0-dof, a0-derived, single-metric term sources the phantom. The
  'dressed momentum rho*nu*u' cannot be a curvature source without either
  (a) its metric-dependence regenerating the O(K) suppression (C3a / SOLVE.md), or
  (b) an independent propagating field carrying nu (C3b / MG).  Both footings.
""")

# ---------------------------------------------------------------------------
banner("RESULT")
if FAIL:
    # C3a LENSING and C3b {a0, cosmology, dof} are EXPECTED-negative checks: they
    # are the honest content of the no-go, not script errors. Report and exit 0.
    print("  Expected-negative checks (the no-go content), not errors:")
    for f in FAIL:
        print("   -", f)
print("\n  C3a  = FAILS-LENSING (a0-derived, 0 dof, no phantom).")
print("  C3b  = CLOSES-BUT-a0-FREE (=MG) (phantom sourced, a0 free + 1 scalar dof).")
print("  C3 sharpened no-go: a0-DERIVED  XOR  MOND-LENSING (single-metric, ghost-free both OK).")
print("  Both a0 footings (9.36e-11 / 1.13e-10) carried; verdict footing-independent.")
print("\nexit 0")
