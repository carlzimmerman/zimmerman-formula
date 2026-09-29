# CFG48 -- Gap 1 (the switch as a legal action term): GATES FROZEN BEFORE ANY SCRIPT (written first, then never edited)

kappa = 1/2 is FITTED. Both a0 footings (9.3603e-11 / 1.1312e-10 m/s^2); scripts use the canonical footing unless a line says otherwise.
Nothing here says the theory is closed. The empirical gates in closure_map/GATES.md are not touched or moved; this file freezes only the
*action-level* acceptance tests for the object that Gap 1 names.

## Scope (after two deconfliction messages, recorded here because it changed the plan)
- Original brief: any legal switch term. Deconfliction: another session (CFG49) covers a *dynamical gate scalar chi sourced by a baryon-only
  invariant*, and CFG50 a tidal-tensor fluid tested for reciprocity. **This lane does not build either.**
- This lane: (1) ownership / boundness as a NONLOCAL or HISTORY functional (energy boundness, Bernoulli-type invariant, turnaround/accretion
  history variable, nested top-level detection); (2) hierarchical top-level detection ("why a satellite does not own its own phantom") as an
  action term; (3) CFG44's non-adiabatic enclosed-mass exchange C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r) written as an explicit nonlocal
  action and checked for causality and reciprocity; plus (4) the six back-of-envelope leads from the calculation-owner session, treated as
  UNVERIFIED hypotheses to be verified or refuted by script.
- The nonlocal-functional gate stiffness (enclosed-mass and global functionals reading baryons) is in scope as a nonlocal functional; a dynamical
  gate FIELD is not.

## The object being sought (candidate B, closure_map/ACTIONS_AND_NOGOS.md sec. 3, Gap 1)
A gate that is a term in ONE action and equals "inside a turned-around, TOP-LEVEL bound system with M_b >= M_*": bound-only, top-level-owned,
baryon-reading (never carrier or curvature; MS1), frame-covariant, with a source-confined edge at x_e in [0.31, 0.48] r_ta.
Layers and units for stability tests are DE12's transition() (24 layers: z in {0.25, 1, 2.5, 4} x M_b in {1e10, 1e11, 1e12} x 2 footings) with
its gate widths w = 0.25 (the M* gate) and w = 1 (the broad gate), loaded unedited and read-only.

## The gates (pass criteria fixed here). A candidate PASSES the lane only if it passes ALL of GA-GG. Failing any is reported as FAIL.
GA  LEGAL ACTION TERM. (a) A Lagrangian density term built from declared fields (metric, khronon/foliation, matter fields, constrained
    Poisson-type auxiliary fields), with its Euler-Lagrange equations derived; (b) no prescribed spatial mask, no external function of position
    or of past time; (c) any nonlocality enters only through a constrained auxiliary field or an explicit kernel, so the variation is defined;
    (d) the gate is VARIED (its own variation is included in every stability test). A history functional passes GA only if the discrete action
    has an Euler-Lagrange residual at time t that depends only on data at times <= t + one step (banded residual, no advanced dependence); a
    prescribed initial label is scored PARTIAL (ownership as initial data), never PASS.
GB  VARIED STABILITY (DE12/DE13 standard, unchanged). For every gate variable that depends on the baryon density: the second variation of the
    gas+gate energy on each of DE12's 24 layers, at both w, gas at 1e6 K (c_s = 117 km/s; 1e5 K is stricter and not needed to fail), must have NO
    negative mode supported inside the layer: DE13's criterion, Dirichlet windows half the layer wide in t (five windows) AND the full layer,
    counted exactly by Sylvester inertia. Equivalent statement for a local reading: c_gate <= c_s. Growth rate Gamma/H of the fastest mode is
    reported, not gated. A gate that reads no baryon density (a conserved label) is exempt from GB but then must pass GG(i).
GC  READS BARYONS ONLY (MS1). The gate variable may depend on rho_b and on fields slaved to rho_b alone (psi_b: lap psi_b = 4 pi G rho_b).
    It may not depend on rho_c (the carrier), on the total-metric curvature, or on the khronon K alone. Tested as a symbolic dependence check.
GD  COVARIANCE. The gate variable is defined from scalar invariants of the metric / foliation / matter 4-velocity or of constrained auxiliary
    fields, with no origin, centre or "system radius" coordinate. A construction defined only through a spherical centre is scored FAIL unless a
    covariant definition is stated AND reduces to it (script: invariance under translation of the origin, checked numerically where applicable).
GE  SOURCE-CONFINED EDGE + GAUSS. The enclosed dynamical mass beyond the edge, M_dyn(2 r_e), must be within 10% of the target's
    M_law(r_e) = M_b sqrt(1 + (r_e/r_M)^2) (P2 point mass; real mass, GR, T5 at the edge), for M_b = 1e10, 1e11, 1e12 Msun, with no negative
    shell. r_e = 0.40 r_ta (the declared centre of the window; r_ta from M_col = M_b(1 + Omega_c/Omega_b), Delta_ta = 11.81, Omega_m = 0.3153,
    h = 0.6736, z = 0). The edge width must be <= 0.3 r_e.
GF  CONSTANTS. Zero new constants beyond kappa and Omega_c. Every dimensionless or dimensionful number, free function or hand-set integration
    constant in the realisation is counted and listed in README.md; declared shapes (nu, x_e = 0.4, M_*) are B's own items and are listed, not
    counted as new. PASS iff the new count is zero.
GG  OWNERSHIP AND CASSINI. (i) HISTORY: two configurations with the SAME instantaneous baryon state (density, velocity) but different ownership
    (accreted satellite vs tidal dwarf formed embedded, CFG7's classes) must receive different gate values; therefore the gate must contain a
    variable that is not a function of the baryon state, and that variable must pass GA. (ii) Cassini: the Solar System (embedded) gets no phantom
    of its own while the host phantom tide keeps the CFG7 margin (>= 2.0e4 below the ceiling Q2 <= 5.2e-27 s^-2), with no screening constant.
GH  EXCHANGE ACTION: CAUSALITY AND RECIPROCITY (task 3). The nonlocal exchange written as an action must have (a) a linearised operator that is
    symmetric (action-derived) with no negative mode on the declared spherical test profiles, (b) reaction on the baryons <= 0.10 g_law at every
    radius x = r/r_M in [0.3, 30] (CFG44's fail line was >= 0.5 g_law; 0.10 is frozen here as the pass line, the SPARC-scatter scale), and
    (c) a principal symbol unchanged by the nonlocal term (a lower-order Volterra or compact perturbation): no signal faster than the
    declared characteristics. The energy the exchange must supply to the fluid, E_c(<r_e) against the baryons' binding energy, is REPORTED, not
    gated (the source of the energy is ambiguous).

## Pre-declared status of the six leads (each is verified or refuted; none is assumed)
L1 Gauss: for any shift-symmetric action whose only source of the potential is rho_b, the enclosed dynamical mass beyond a source-free gated
   region equals M_b exactly. HOLDS iff the numerical profile gives M_dyn(> r_e) = M_b to 1e-6 relative and the sympy flux identity has zero
   residual, for AQUAL- and QUMOND-gated forms; and if it holds, GE FAILS for every field-only gate.
L2 Noether: d_j sigma_ij = rho_b d_i Phi + DeltaL d_i W, DeltaL = (a0^2/8 pi G)(y - F(y)). HOLDS iff the sympy divergence identity has zero
   residual; the numerical size of DeltaL grad W on DE12's layers against rho_b g is reported.
L3 Edge stress: baryons at the edge can supply at most ~f_b P_c. NOT assumed: the script computes P_b,max / P_c(r_e) with baryon gas at the
   enclosed mean density (and at the isothermal edge density) and sigma^2 = V_c^2/2, and the lead HOLDS iff that ratio is <= 0.25 for every
   M_b in 1e9-1e13.
L4 Mediator: needed relative strength alpha_req = a0/(2 g_N(r_e)) >= 1e2 for M_b >= 1e10 and >= 1e6 times the Cassini bound 3e-5. HOLDS iff both.
L5 Bistable edge balance (kinematic exponent only; no gate field is built): a wall balance DeltaV + 2 sigma_w/r_e = P_c(r_e) keeps x_e inside
   [0.31, 0.48] over at most 1.2 decades of M_b, hence cannot serve >= 4 decades. HOLDS iff the maximal window width over all DeltaV,
   sigma_w >= 0 is <= 1.2 decades.

## MUTATE controls (each must exit rc = 1; each names the claim it falsifies)
G1 (Gauss/Noether): the gate is given a fluid source term (a second source beyond rho_b) -> L1's "M_dyn = M_b" must fail.
G2 (boundness): the baryon potential is replaced by the phantom-inclusive one -> the "boundness edge sits at 2 r_M" claim must fail.
G3 (history): the memory variable is replaced by a local (memory-free) gate -> the advanced-dependence claim must fail.
G4 (exchange): the exchange is made non-reciprocal (baryons feel no reaction) -> the "reaction >= 0.1 g_law" claim must fail; the symmetry check
   of the operator must fail as well.
G5 (edge stress, mediator, wall): baryon fraction set to 1 (all mass baryonic) -> L3's shortfall must fail; wall target replaced by a
   mass-independent pressure -> L5's narrow window must fail.
G6 (nonlocal gate stiffness): the gate energy scale B is set to zero -> the negative-mode count must be zero and the "fails everywhere" claim fail.

## Reporting rule
Each gate is reported as PASS / FAIL / PARTIAL exactly as computed. A scoped no-go is a valid result. No knob is scanned; every number that
enters is listed in README.md with its status (DERIVED / POSTULATED / FITTED / OPEN). Scripts exit 1 only when a control or a stated claim is false.
