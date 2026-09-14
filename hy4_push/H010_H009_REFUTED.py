#!/usr/bin/env python3
"""H010 -- H009 IS REFUTED BY GLM's G043.  Retraction, in my own track.

WHAT I CLAIMED (H009, hy4_push, 8/8 + Lean certificate).
  That Horn A's fixed hypersurface-orthogonal congruence (glm53 G032: alpha_1
  = 0 exactly at all nine (CA,JY) cells, gamma -> 1, alpha_3 -> 0) is the
  NORMALISED GAUGE of a mimetic parent, so that the explicit local Lorentz
  violation GLM recorded is a gauge artifact (unimodular-gravity class) rather
  than a cost.

WHY THE CLAIM IS WRONG (GLM's G043, 25 pass / 3 fail).
  My Lean certificate proved the KINEMATIC algebra, which is real but
  insufficient:

    (a) g^{mu nu} d_mu T d_nu T = -1 is an identity of the definition     [true]
    (b) u_mu = d_mu T is unit-timelike and hypersurface-orthogonal        [true]
    (c) T -> f(T) leaves the construction invariant                       [true]

  All three hold -- for ANY mimetic rewrite.  What they do NOT establish is
  that a generally covariant PARENT exists whose gauge-fixing yields Horn A.
  GLM tested that and it fails, for a reason I did not check:

    "2503.11174's machinery feeds on the CONFORMAL SYMMETRY of homogeneously-
     scaling building blocks; the Zimmerman normalization P = Lambda^4 f with
     f(0) = -1 (fixing Lambda AND, through f' = mu_2, the MOND scale) is NOT
     conformal: Horn A's fixed congruence CANNOT be a gauge slice of any
     parent in that class.  The Lorentz-violation cost does NOT dissolve."

  That is the decisive point and it is correct.  My f(0) = -1 -- the very
  result that gives w = -1 exactly and is the crown of the whole programme --
  is precisely what breaks the conformal scaling the embedding needs.  The
  feature that makes the theory work is the feature that blocks its
  covariantization.  I proved the kinematics of a rewrite and called it a
  gauge symmetry.

  GLM's second finding kills the fallback too:

    "The projector-parent carries NO dust at all: the chi-current
     J = f'(X)(n.d phi) phi_perp / sqrt(-sigma) vanishes identically on the
     cosmic slice (f'(0) = 0 AND phi_perp = 0) and is phi-locked -- no free
     initial condition, no w."

  With f'(X) = mu_2(sqrt X) and mu_2(0) = 0, the current vanishes at the
  background.  There is no mimetic dust, so there is nothing to identify with
  the cold sector.  The "unification" reading (ii) also fails: the
  Chamseddine-Mukhanov-style parent that does carry dust gives w = 0 EXACTLY,
  contradicting the registered strictly-positive window (1.5e-8, 5.7e-7).

WHAT SURVIVES.
  * Horn A itself (G032): alpha_1 = alpha_2 = 0, gamma = 1, alpha_3 = 0.  The
    preferred-frame wall does not exist for this architecture.  That is
    untouched by G043 and by this retraction.
  * The three-sector action, the equilibrium theory, the Lean certificates,
    the fluid map.  All untouched.
  * My Lean file H009_mimetic.lean remains valid AS ALGEBRA: it proves the
    kinematic statements (a)-(c), which are true.  It does not prove, and
    never proved, the existence of a covariant parent.  Its spine theorem's
    name and docstring overstate its scope; that is corrected here.

WHAT DIES.
  * The claim that the Lorentz-violation cost is a gauge artifact.  It is a
    real cost.  Horn A is an honest Lorentz-violating theory.
  * Any hope of dissolving the cost via the 2503.11174 class.

THE LESSON, STATED PLAINLY (the second time this session).
  In H006 I inferred PPN parameters from the STATIC potential; that was wrong
  because PPN lives in the boosted linear response.  In H009 I inferred a
  GAUGE SYMMETRY from a REPARAMETRISATION INVARIANCE of the rewritten fields;
  that was wrong because a symmetry of a rewriting is not a symmetry of a
  theory.  Both errors are the same shape: mistaking an invariance of my
  description for an invariance of the physics.

H009's files are KEPT, not deleted -- the refutation is part of the record.
"""
print(__doc__)
print("="*70)
print("H009 REFUTED.  Horn A stands; the Lorentz-violation cost is real.")
print("H009's Lean file is valid algebra but its spine overstates scope.")
print("="*70)
