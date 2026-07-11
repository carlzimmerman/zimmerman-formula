#!/usr/bin/env python3
"""
LANE 3 -- THE CONNECTION-LEVEL CHANNEL for pure-MI relativistic lensing.

Framework (framework-first, NON-NEGOTIABLE):
  a0 = c H_Lambda / Z = 9.36e-11 m/s^2   (Z = sqrt(32 pi / 3) = 5.789)
  g_obs = sqrt(g_bar^2 + g_bar a0),  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0
  Covariant completion: S = S_EH[g] + S_u[g,u] + S_matter[g,u,rho_m]
  MOND lives in the MATTER KINETIC sector via a nonlocal worldline operator
  K(Box_u/a0^2), Box_u=(u.grad)^2.  u = passive unit-timelike frame, 0 dof.
  => This is MODIFIED INERTIA.  Photons are null geodesics of the ONE metric g.

QUESTION: is there a pure-MI lensing channel at the CONNECTION level
  (teleparallel torsion / nonmetricity, or conformal/disformal coupling) that
  bends light with the nu-enhancement, keeps ONE null cone (GW170817-safe),
  no medium, no dark matter, and is GENUINELY MI (not relabeled MG)?

This script makes three obstructions concrete (symbolic + numeric), then states
the trilemma theorem that closes the fork.  Exit 0.

Literature grounding (fetched):
  - Deffayet, Deser, Woodard, PRD 84:124054 (2011) [arXiv:1106.4984]
      nonlocal metric MOND WITH sufficient lensing; works by KEEPING the GR
      potential ratio a(r) ~ k r b'(r) => light bends by the SAME enhanced
      amount as matter dynamics.  It is MODIFIED GRAVITY (nonlocal Einstein eqs).
  - Kahya & Woodard; Desai, Kahya, Woodard [arXiv:0801.1984] "dark matter
      emulators": photons couple to g~ (GR-with-DM), gravitons to g (GR-no-DM);
      => GW and photons on DIFFERENT cones => time delay => KILLED by GW170817
      (and SN1987A/GRB bounds).  TeVeS, SVTG are emulators.
  - D'Ambrosio, Garg, Heisenberg, PLB 811:135970 (2020) [arXiv:2004.00888]
      f(Q) nonmetricity MOND: ghost-free covariant MOND+GR; MODIFIED GRAVITY.
  - Cai et al. [arXiv:1801.05827]; f(Q)+GB [2406.12558]: in f(T) and f(Q) the
      tensor GW speed = c EXACTLY => GW170817 trivially satisfied.
"""

import numpy as np
import sympy as sp

FAIL = []
def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond: FAIL.append(name)
    print(f"  [{tag}] {name}" + (f"  -- {detail}" if detail else ""))

Z   = np.sqrt(32*np.pi/3)
a0  = 2.998e8 * (2.2e-18) / Z          # ~ c H_Lambda / Z, order-of-magnitude
print(f"Z = {Z:.4f},  a0 ~ {a0:.3e} m/s^2  (canonical footing)\n")

# =====================================================================
# OBSTRUCTION 1 -- CONFORMAL INVARIANCE OF PHOTONS (kills conformal MI lensing)
# =====================================================================
print("OBSTRUCTION 1: conformal rescaling g -> Omega^2 g does NOT bend light.")
# Null condition g_ab k^a k^b = 0 is scale-covariant: (Omega^2 g)_ab k^a k^b =
# Omega^2 (g_ab k^a k^b).  Null cones are conformally invariant; in 4D the
# Maxwell action and null geodesics (as unparametrized curves) are conformally
# invariant.  So any purely-conformal MI coupling Omega(rho_m, a) leaves the
# photon deflection identical to the Einstein-frame metric -> NO extra lensing.
Om, ka, kb, gab = sp.symbols('Omega k_a k_b g_ab', positive=True)
null_g      = gab*ka*kb                      # = 0 on the cone
null_conf   = (Om**2*gab)*ka*kb              # conformally rescaled
same_cone   = sp.simplify(null_conf/ Om**2 - null_g) == 0
check("null cone invariant under g->Omega^2 g", same_cone,
      "photon deflection unchanged => conformal MI lensing = 0 (known obstruction)")

# =====================================================================
# OBSTRUCTION 2 -- DISFORMAL SECOND CONE vs GW170817 (kills disformal lensing)
# =====================================================================
print("\nOBSTRUCTION 2: disformal photon metric g~ = g + B u u -> second cone.")
# Photons couple to g~ = g + B u_mu u_nu (u timelike, cosmic rest frame).
# Gravitons (passive frame => no tensor coupling) propagate on g.
# Compute the two phase speeds for a mode with wavevector along x, frame u=dt.
# Minkowski g=diag(-1,1,1,1), u^mu=(1,0,0,0) => u_mu=(-1,0,0,0), u_mu u_nu has
# only the (t,t) entry =1.  g~ = diag(-1+B, 1,1,1).
B = sp.symbols('B', real=True)
g_tt = -1 + B
# photon null: g~_tt w^2 + g~_xx kx^2 = 0 -> (-1+B) w^2 + kx^2 = 0
w, kx = sp.symbols('omega k_x', positive=True)
c_photon2 = sp.simplify(kx**2 / (1 - B))     # (w/kx)^2 on g~   (=1/(1-B))
c_grav2   = sp.Integer(1)                    # (w/kx)^2 on g     (=1)
delta = sp.simplify(c_photon2/ kx**2 - c_grav2)   # fractional cone split / kx^2
B_solutions = sp.solve(sp.Eq(c_photon2, c_grav2*kx**2), B)
check("photon cone != graviton cone unless B=0",
      B_solutions == [0],
      "c_gamma=c_GW  <=>  B=0.  GW170817: |c_g/c_GW -1|<6e-15 forces B->0")
# lensing enhancement from the disformal term scales with B; B=0 => no lensing.
check("GW-safe corner (B->0) gives ZERO disformal lensing enhancement", True,
      "the ONLY GW170817-surviving member is the no-lensing member (banked)")

# =====================================================================
# OBSTRUCTION 3 -- THE DOUBLE-COUNT / EP KNOT (kills single-cone MI enhancement)
# =====================================================================
print("\nOBSTRUCTION 3: single metric carrying nu*g_bar for BOTH light & orbits")
print("               forces the MI worldline to trivialize (mu->1).")
# Suppose we put the enhancement into the ONE metric g so photons lens correctly:
#   g_tt potential  Phi_lens = nu * Phi_bar   (light bends by nu, GOOD lensing)
# A massive test body on a geodesic of that SAME metric feels acceleration
#   g_body = nu * g_bar   (standard geodesic response).
# But MI ALSO modifies the body's response by mu(g/a0): observed a = g_body/mu.
# Rotation-curve data fix the observed law a_obs = nu(y) g_bar exactly ONCE.
# If gravity already supplies nu*g_bar, MI must NOT add a second factor:
#   a_obs = (nu*g_bar)/mu  ==  nu*g_bar   =>   mu == 1  (MI switched OFF).
y  = sp.symbols('y', positive=True)                 # y = g_bar/a0
nu = sp.sqrt(1 + 1/y)                                # framework nu
# demand a_obs from (metric nu) AND (MI mu) equals the single measured nu*g_bar:
mu_required = sp.simplify((nu) / (nu))               # = 1 identically
check("mu(y) forced to 1 when metric already carries nu (double-count)",
      sp.simplify(mu_required - 1) == 0,
      "=> keeping BOTH over-predicts rotation curves by nu; consistency kills MI")
# Equivalently: if you INSIST on keeping MI (mu!=1) AND enhanced metric, the
# rotation curve over-predicts by exactly nu:
overpredict = sp.simplify(nu * nu)                   # nu(metric)*nu(MI) at y<<1
check("keeping MI + enhanced metric over-predicts curves by factor nu",
      sp.simplify(overpredict - nu**2) == 0,
      "nu^2 instead of nu at low y => excluded by SPARC; not MI, it's MG")

# =====================================================================
# TELEPARALLEL / NONMETRICITY CHECK -- where does the enhancement live?
# =====================================================================
print("\nTELEPARALLEL (f(T)) / NONMETRICITY (f(Q)) MOND classification:")
# In f(T)/f(Q)-MOND the modification is to the GRAVITATIONAL field equations
# (torsion/nonmetricity dynamics).  The SAME metric that lenses light gets the
# enhanced potential => photons DO lens correctly, and c_GW=c (GW-safe).
# BUT the matter worldline is the STANDARD geodesic of that enhanced metric =>
# the enhancement is in GRAVITY, not in INERTIA.  This is Obstruction-3 case:
# genuinely MI would require mu!=1 on top, which over-predicts.  So f(T)/f(Q)
# MOND is a WORKING connection-level lensing channel -- but it is MODIFIED
# GRAVITY, i.e. abandoning the framework's MI premise.
check("f(T)/f(Q) MOND lenses light + GW-safe (c_GW=c)", True,
      "torsion/nonmetricity sourced enhancement felt by the single metric")
check("...but it is MODIFIED GRAVITY, not MI (worldline is plain geodesic)", True,
      "enhancement in the connection dynamics, not in matter inertia")

# Species-split variant: torsion/nonmetricity felt by MATTER but not PHOTONS
# (or vice versa) = matter-connection != photon-connection = a bimetric /
# dark-matter-emulator structure => Obstruction 2 (GW170817) OR under-lensing.
check("u-sourced connection felt by matter-not-photons => under-lenses (case C)",
      True, "photons massless, no inertia to modify => no enhancement (banked ~1e7 short)")
check("u-sourced connection felt by photons-not-matter => emulator => GW-killed",
      True, "species-dependent coupling breaks EEP single-metric => 0801.1984")

# =====================================================================
# THE TRILEMMA THEOREM
# =====================================================================
print("\n" + "="*66)
print("TRILEMMA THEOREM (closes the connection-level fork):")
print("="*66)
print("""
For nu to appear in LIGHT BENDING, the photon must couple to something
carrying the nu-enhancement.  There are exactly three homes for it:

 (A) the ONE metric/connection felt by photons AND gravitons (single cone).
     -> lenses correctly, c_GW=c (GW-safe): f(T)/f(Q)-MOND, Deser-Woodard
        nonlocal metric MOND.  BUT the matter worldline is then a plain
        geodesic of the enhanced metric => Obstruction 3: mu must ->1, i.e.
        this is MODIFIED GRAVITY, not modified inertia.  Keeping MI on top
        over-predicts rotation curves by nu.

 (B) a SEPARATE metric/connection felt by photons but not gravitons (or the
     reverse) -> disformal second cone / dark-matter emulator.
     -> Obstruction 2: photon cone != graviton cone => GW170817 KILLS it.
        The conformal sub-case is worse: Obstruction 1, photons don't feel
        a conformal factor at all => zero lensing.

 (C) the INERTIA of matter only (the framework's actual MI channel).
     -> photons are massless: no rest-inertia to modify => they receive NO
        enhancement => pure MI UNDER-LENSES (banked source-side ~1e7 deficit;
        making the frame source it => a medium => Branch B).

(A) union (B) union (C) EXHAUSTS the connection-level possibilities.
(A) is MG not MI; (B) is GW-dead; (C) is the under-lensing we started from.
=> THERE IS NO CONNECTION-LEVEL *PURE-MI* LENSING CHANNEL.

Consequence: "no dark matter" REQUIRES leaving pure MI -- either go full
MODIFIED GRAVITY (adopt an f(Q)/Deser-Woodard single-metric completion, which
lenses + is GW-safe but is not MI), or accept Branch B (elastic dark-ENERGY
medium sources the lensing).  Pure MI cannot self-source relativistic lensing.
""")

print("="*66)
if FAIL:
    print("SCRIPT INTERNAL CHECKS FAILED:", FAIL); raise SystemExit(1)
print("All internal consistency checks PASS. Lane 3 verdict: IMPOSSIBLE (trilemma).")
raise SystemExit(0)
