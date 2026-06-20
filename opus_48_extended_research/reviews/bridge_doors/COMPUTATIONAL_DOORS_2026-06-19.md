# Bridge DOORS — concrete runnable computational analyses tied to people/connections/gaps
Date 2026-06-19. Both-ways + quarantine (a0/Z/kappa/I0 NEVER asserted derived). DM-particle people skipped.

Synthesizes the 5 bridge_scout notes + banked GHOST_CONDENSATE / AEST_EMBEDDING / DARK_MATTER_ILLUSION.
A DOOR = a CALCULATION with a definite PASS/KILL or NUMBER, the TOOL, the INPUTS, the BOTH-WAYS outcome.
NOT "read more papers." All inputs are in-repo (ghost_condensate/ scripts hold the P(X) bilinear coeffs)
or pulled from a named arXiv equation.

================================================================================
THE CONNECTION MAP (verified, arXiv IDs)
================================================================================
GHOST-CONDENSATE SPINE (GAP-1/2):
  ACLM 2004 (hep-th/0312099, Arkani-Hamed–Cheng–Luty–Mukohyama) = the framework's Q-sector P(X) identity
    -> Verwayen–Skordis–Zlosnik 2024 Eq.7 K(Q)=mu^2(Q-1)^2 cites ACLM (the AUTHORS' OWN identification)
    -> Blanchet–Skordis Khronon 2404.06584 / 2507.00912: SAME K(Q)=mu^2(Q-1)^2 POSTULATED (Skordis himself)
    -> Lim–Sawicki–Vikman "Ghost Dark Matter" 1001.4634: GC scalar redshifts a^-3 (the Q-mode dust)
    -> Mersini-Houghton 2502.08894: phantom-DE => time-crystal STABILITY THEOREM (g'<0,g''>0,rho>=0)
POSITIVITY/CAUSALITY (tests GAP-1's wrong-sign-then-stabilized P(X)):
  Grall–Melville 2102.05683 (boost-free positivity, NO LI-UV required — APPLIES to a ghost condensate)
  Serra–Trombetta 2412.19745 (IR bound v^2 <= c_s^2 = 1/2 — but their explicit realization REQUIRES an
    LI/conformal UV, so this is the family that does NOT cleanly apply to a GC; flagged both ways below)
  Creminelli–Janssen–Senatore 2207.14224 (REQUIRES conformal UV => INAPPLICABLE to GC; do not mis-cite as kill)
  Deffayet–Fathe Jalali–Held–Mukohyama–Vikman 2604.21823 (quantum-stable ghost: unitary, pure-point spectrum)
dS-QFT / THE SO(4,1) GATE (GAP-2):
  Sengor 2205.11550 (principal/complementary series at dS late-time boundary) + 2510.05735 (LADDER OPERATORS
    of the dS algebra: SCT C_i lowers Delta by 1, translations T_i raise Delta by 1; massless/shift-symmetric
    scalar = DISCRETE SERIES, lowest-weight states |0,0> and |3,0> on dS4)
  CLPW 2206.10780 + Anninos 1109.4942 + Chen-Xu 2511.00622 (static-patch OBSERVER breaks SO(4,1)->SO(3)xR)
  Kiritsis 1207.2325 (LV couplings MUST be gravitational-sector fields)
MOND-LAGRANGIAN / a0<->Lambda (GAP-3):
  Blanchet–Seraille 2502.14686 (non-Abelian YM graviphoton: INDEPENDENT a0 ∝ sqrt(Lambda), Lambda~a0^2/c^4)
LAMBDA/DESI (a0(z) hostage, GAP-3 side): Lodha–Calderon 2503.14743 (rho_DE non-monotonic hump z~0.5)

================================================================================
DOOR LEDGER — 8 concrete runnable computations
================================================================================

--- DOOR 1 (GAP-1) POSITIVITY OF THE STABILIZED GHOST: Grall–Melville boost-free bound on mu^2(Q-1)^2 ---
PERSON: Grall–Melville 2102.05683 (+ Creminelli line). TOOL: sympy/numpy (extends ghost_condensate/
  expand_PX_around_condensate.py, which already has the bilinear coeffs time=P'+2X0 P'', space=-P').
WHAT TO COMPUTE: build the 2->2 pi-pi forward amplitude for P(X)=mu^2(Q-1)^2 expanded at X0 (P'(X0)=0,
  P''(X0)=2mu^2>0); evaluate the boost-free positivity arc-integral d^2 A/d omega^2 >= 0 at fixed spatial
  momentum, AND the higher-derivative (nabla^2 pi)^2/M^2 coefficient sign. The framework's coeffs:
  time-kinetic 2X0 P''>0 (healthy), ordinary-grad -P'=0, leading spatial = +(alpha/M^2)k^4. Check the
  sign of the k^4 coefficient and the 4-pt contact term against the Grall–Melville lower bound.
INPUTS: P''(X0)=2mu^2, X0=c^2, the framework's M~0.04-1 eV (banked seesaw). In-repo coeffs + the 2102.05683
  inequality (fetch the explicit arc bound from the PDF/HTML — flagged: abstract-only on first fetch).
BOTH-WAYS: PASS (k^4 coeff & contact term obey the bound) = the wrong-sign-then-stabilized P(X) is
  positivity-CONSISTENT, a real consistency win (the #1 "ghosts are sick" worry retired for this P).
  KILL (a coefficient violates the bound) = the specific mu^2(Q-1)^2 is positivity-EXCLUDED => GAP-1's
  postulated shape is ruled out, forcing a different K(Q) — a KILL as valuable as a bridge.
FEASIBILITY: needs-setup (must pull the exact 2102.05683 arc inequality; the amplitude build is in-repo).
IMPACT: high. NOTE both ways: Serra–Trombetta's v^2<=1/2 needs an LI-UV the GC lacks, so it does NOT
  cleanly bind — DOOR 1 must use the boost-free (Grall–Melville) family, not the conformal-UV family.

--- DOOR 2 (GAP-1) ACOUSTIC-CAUSALITY CHECK: Serra–Trombetta gapped-slower-than-gapless on the Q-mode ---
PERSON: Serra–Trombetta 2412.19745. TOOL: sympy/numpy (dispersion-relation algebra).
WHAT TO COMPUTE: the framework has TWO scalar excitations — the gapless k^4/M^2 GC pi-mode and the gapped
  AeST potential-mass mode mu (k_J=M^2/(sqrt2 M_Pl)). Compute both dispersion relations omega(k) from the
  AeST quadratic action, extract the low-k group/phase speeds, and test the IR inequality v_gapped^2 <=
  v_gapless^2 below the gap. (Honest caveat: ST's bound was DERIVED assuming an LI-UV; treat the result as
  a CONSISTENCY DIAGNOSTIC, not a theorem-grade kill, since the GC has no LI-UV.)
INPUTS: AeST quadratic-action coeffs {K_B, K_2, mu, lambda_s} (in aest_embedding/ + cluster_aest scripts),
  the framework's M.
BOTH-WAYS: PASS (gapped slower) = causally-consistent IR structure, corroborates DOOR 1. FAIL (gapped
  faster) = an IR-causality red flag on the joint AeST+GC spectrum, a concrete tension to report.
FEASIBILITY: ready-now (all coeffs in-repo). IMPACT: medium (diagnostic, UV-caveated).

--- DOOR 3 (GAP-1) QUANTUM-STABILITY MAP: Deffayet–Mukohyama–Vikman stable-ghost criterion on K(Q) ---
PERSON: Deffayet–Fathe Jalali–Held–Mukohyama–Vikman 2604.21823 (+ 2305.09631 classical). TOOL: sympy.
WHAT TO COMPUTE: reduce the framework's Q-sector to the DMV reference system (a ghost DOF polynomially
  coupled to a positive-energy DOF) and test for their conserved positive-spectrum integral of motion I.
  Concretely: write the framework's pi (ghost-condensate, negative bare kinetic) + the AeST tensor/scalar
  positive modes as a coupled-oscillator Hamiltonian; search (sympy) for a quadratic invariant J with
  positive-definite spectrum that commutes with H. If found => DMV's unitarity/pure-point/bounded-<q^2>
  theorem transfers; if not => the framework's ghost is NOT in the proven-stable class.
INPUTS: the coupled quadratic Hamiltonian from the AeST bilinear action (aest_embedding/), DMV's
  invariant-construction recipe (2604.21823 + 2604.21348 "operator conservation law").
BOTH-WAYS: FOUND invariant = the framework's stabilized ghost is QUANTUM-stable in the DMV sense (a
  genuine GAP-1 health result — the postulated wrong-sign term is unitarily benign). NOT FOUND = the
  framework's ghost sits OUTSIDE the proven-stable class => a real open quantum-consistency question,
  honestly flagged (not a kill, but not the comfort the classical dS-Jeans-cure gives).
FEASIBILITY: hard (the invariant search is nontrivial; toy-model in 2604.21823 is single-oscillator).
IMPACT: high (directly addresses the deepest GAP-1 worry).

--- DOOR 4 (GAP-2) SO(4,1) IRREP DECOMPOSITION of the preferred-frame term via Sengor ladder operators ---
PERSON: Sengor 2510.05735 (ladder ops) + 2205.11550 (series classification). TOOL: sympy (Lie-algebra
  rep theory: so(4,1) generators D, P_i, C_i, M_ij as matrices/commutators).
WHAT TO COMPUTE: (a) build the so(4,1) algebra in sympy (10 generators, verified commutators incl.
  [D,C_i]=-C_i, [D,T_i]=+T_i from 2510.05735). (b) Express the framework's preferred-frame condensate
  gradient u^mu = <d^mu phi>/|..| as a weight-vector / lowest-weight state and act with the ladder ops:
  does the SHIFT-symmetric Q-mode land in a DISCRETE-SERIES rep (massless scalar: lowest-weight |0,0> and
  |3,0> on dS4, per 2510.05735)? (c) Decompose the aether bilinear (K_B/2)F^2 / the s_munu SME background
  into SO(4,1) irreps and ASK: is there an irrep a condensate background SELECTS that a dS-invariant vacuum
  cannot — a GROUP-THEORETIC statement of the gate-evasion?
INPUTS: the so(4,1) commutators + ladder normalizations N_T=a*Delta+b*l, N_C=-2 Delta_s/(a Delta_s+b l_s)
  (2510.05735); the framework's u^mu and Y/Q invariants (one_field_both_roles.py has Y-Q^2=(grad phi)^2).
BOTH-WAYS: A rep-theoretic DERIVATION (the discrete-series shift-charge / a lowest-weight condition FORCES
  the frame-selecting weight) = a group-theory CLOSING of GAP-2 (the frame falls out of SO(4,1) rep theory,
  not postulated). NOTHING (every condensate config decomposes into the same dS-invariant principal-series
  content the vacuum already carries) = the gate stays EVADED-not-CLOSED, now with a SHARP group-theoretic
  reason (Sengor's UIRs codify the wall). Either way produces a definite rep-label statement.
FEASIBILITY: needs-setup (algebra build is standard sympy; the physics map u^mu->weight-vector is the
  research content). IMPACT: high (this is the GAP-2 keystone).

--- DOOR 5 (GAP-2) STATIC-PATCH OBSERVER BREAKING: SO(4,1)->SO(3)xR generator count + dS-Unruh T_eff ---
PERSON: CLPW 2206.10780 + Anninos 1109.4942 + Chen-Xu 2511.00622. TOOL: sympy (subalgebra projection).
WHAT TO COMPUTE: in the same so(4,1) sympy build, project onto the static-patch observer's unbroken
  subalgebra SO(3)xR (rotations + the single timelike boost = worldline time-translation). Verify it is
  EXACTLY the stabilizer of the framework's u^mu (10 -> 4 generators), and compute the dS-Unruh/Gibbons-
  Hawking temperature of that worldline (Deser-Levin T_eff) symbolically to confirm it equals the a0-founding
  temperature cH_Lambda/(2pi)-class. This makes the "frame = static-patch observer worldline" identification
  a sympy-checked subgroup statement, the dS-QFT NAME for the GC break-by-background.
INPUTS: so(4,1) generators (DOOR 4), u^mu, the banked dS-Unruh T_eff=hbar a/(2pi c k_B)|_{a=cH_Lambda...}.
BOTH-WAYS: the stabilizer matches SO(3)xR AND T_eff matches the a0 temperature = the framework's frame is
  the static-patch observer's, dS-QFT-named (credit: confirms the escape route's dS-QFT home; but it is a
  GAUGE/relational frame per Chen-Xu 2511.00622, NOT a dynamical aether — so NO derivation of the kinetic
  term, gate still not closed). MISMATCH = the identification fails, a both-ways negative.
FEASIBILITY: ready-now (subalgebra projection + a known T_eff). IMPACT: medium (names, does not close).

--- DOOR 6 (GAP-1) FORCING TEST: does the Mersini-Houghton phantom-DE=>time-crystal theorem FORCE mu^2(Q-1)^2? ---
PERSON: Mersini-Houghton 2502.08894 (+ Cline 2502.19448 instability caveat). TOOL: sympy.
WHAT TO COMPUTE: take MH's claimed near-theorem — a stable non-canonical scalar acting as phantom DE
  (w<=-1, c_s^2>0, rho>=0) NECESSARILY has g'(X)<0, g''(X)>0 and phidot!=0 at the turning point (a
  ghost-condensate/time-crystal). Plug the framework's P(X)=mu^2(Q-1)^2 (in the X=Q-variable) and TEST the
  three inequalities at the condensate point: is g'<0 in the relevant branch, g''>0, c_s^2=g'/(g'+2X g'')>0,
  rho>=0? If the framework's K(Q) is the UNIQUE shape satisfying MH's conditions in a neighborhood, that is
  a derivation-grade ORIGIN argument for GAP-1; if it merely SATISFIES them (non-unique), it is corroboration.
INPUTS: K(Q)=mu^2(Q-1)^2, the EoS split from condensate_postulate_and_eos.py (w=-1 at min, w=0 off-min),
  MH's inequalities. ALSO run Cline's 2502.19448 negative-rho instability check on the same shape.
BOTH-WAYS: FORCES (unique) = the strongest GAP-1 result available — the kinetic term is no longer postulated
  but selected by phantom-DE stability. SATISFIES-but-not-unique = partial origin (corroboration), GAP-1
  stays open. FAILS an inequality / hits Cline's negative-rho = the framework's specific shape is in tension
  with the stability theorem (a real both-ways negative). 
FEASIBILITY: ready-now (all algebra in-repo + 3 inequalities). IMPACT: high.

--- DOOR 7 (GAP-3) INDEPENDENT a0∝sqrt(Lambda): reproduce Blanchet–Seraille Lambda~a0^2/c^4 + compare coefficient ---
PERSON: Blanchet–Seraille 2502.14686. TOOL: numpy/sympy.
WHAT TO COMPUTE: from the YM-graviphoton universality relation a0 ~ c^2/alpha and Lambda ~ a0^2/c^4,
  solve for the dimensionless coefficient that their mechanism predicts in a0 = (coeff)*c^2 sqrt(Lambda),
  and compare to the framework's coeff = sqrt(1/32pi) = 0.0997 (a0=c^2 sqrt(Lambda/32pi)). Does an
  independent fundamental gauge theory land the SAME O(1)? This tests whether kappa=1/2/Z=sqrt(32pi/3) is
  mechanism-specific or convergent across independent a0∝sqrt(Lambda) constructions.
INPUTS: 2502.14686 Eqs for a0(alpha) and Lambda(a0); the framework's a0=c^2 sqrt(Lambda/32pi)=9.3624e-11.
BOTH-WAYS: COEFFICIENTS AGREE (within O(1)) = a genuine cross-mechanism corroboration of GAP-3's FORM and
  a hint the coefficient is less arbitrary than banked (still not a derivation — two mechanisms agreeing is
  not a proof). DISAGREE = confirms the coefficient is mechanism-specific (kappa stays a free input, as
  banked) — the honest null. Quarantine: this NEVER asserts kappa derived, just measures convergence.
FEASIBILITY: ready-now (two algebraic relations). IMPACT: medium (GAP-3 is the hardest, banked-closed door;
  this is a convergence MEASUREMENT, not a re-opening).

--- DOOR 8 (GAP-4) DISCRETE-SERIES SHIFT-CHARGE: can Sengor's discrete-series tachyon fix I0? ---
PERSON: Sengor/Gazeau discrete series (2510.05735, 2410.19041) — the shift-symmetric scalar's dS home.
TOOL: sympy (dS mode functions + shift-charge integral).
WHAT TO COMPUTE: the framework's free amount I0 = the conserved shift-charge (a^3 K'(Q)=I0). The Q-mode is
  shift-symmetric => its dS-QFT home is the DISCRETE SERIES (Sengor). Compute the discrete-series scalar's
  shift charge / zero-mode normalization on the dS static patch and ask: does the discrete-series UIR
  QUANTIZE or fix the zero-mode amplitude (the MEAN of the flat direction), or only its fluctuation VARIANCE
  (as the banked PIN_I0_THERMAL proved: d rho_dust/dLambda=0, thermal sets variance not mean)?
INPUTS: discrete-series weight (massless scalar lowest-weight |0,0>,|3,0> on dS4, 2510.05735); the banked
  structural result I0 = mean of a shift-symmetric flat direction (gc_consequences/pin_I0_thermal.py).
BOTH-WAYS: the discrete-series rep CONSTRAINS the zero-mode (a quantization condition on I0) = a route to
  pin GAP-4 (would be a major result). It does NOT (the discrete-series only labels the rep, the shift-charge
  stays a free Casimir/boundary datum) = GAP-4 confirmed robustly free with a dS-QFT REASON (the rep label
  is not a dynamics) — matches the banked null, now group-theoretically grounded.
FEASIBILITY: hard (discrete-series mode functions on the static patch are subtle). IMPACT: medium-high
  (GAP-4 is proven free; this tests whether rep theory is the one missing lever — expected null, valuable).

================================================================================
PRIORITY (impact x feasibility): DOOR 6 (ready-now, high) and DOOR 4 (the GAP-2 keystone) FIRST;
then DOOR 1 (positivity, the real GAP-1 consistency test) and DOOR 2 (ready-now). DOOR 3/8 are hard.
DOOR 7 is a quick convergence measurement. ALL both-ways: a KILL (DOOR 1 positivity-excludes the P(X);
DOOR 6 fails MH/hits Cline; DOOR 2 gapped-faster) is reported at full weight, equal to a bridge.

QUARANTINE held: no door asserts a0/Z/kappa/I0 derived; DOOR 4/8 are rep-LABELS until a dynamics is shown;
DOOR 7 measures convergence, never claims the coefficient proven. Both-ways enforced throughout.
