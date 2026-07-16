# ONE-LOOP FINITE PARTS -- LANE S: BASE VERIFICATION + COMPUTATION DEFINITION
Date: 2026-07-16. Repo `~/new_physics/zimmerman-formula` FROZEN (read-only). All outputs live here.
Re-run log: `base_rerun.log` (this directory). All 9 published scripts re-ran **exit 0** in place.

All file paths below are relative to
`/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/reviews/` unless absolute.

---

## PART 1 -- WHAT THE PUBLISHED BASE ACTUALLY ESTABLISHES (verified by re-run, not trusted)

### 1.0 A scope correction to this workflow's own briefing
The briefing said finite parts were "explicitly left open by v11." That is **stale**: commit
`89d03112` (v12, 2026-07-09) already computed the *stability-relevant* finite structure
(`mi_formal_completion_2026/twoloop_laneA_finite.py`, misleadingly named -- it is the ONE-loop
finite lane) and the all-orders additive a0 protection (`twoloop_laneC_a0.py`,
`twoloop_aether_resolution.py`). What v12 did **not** compute -- its own words,
`twoloop_laneA_finite.py:348-349`: "Full closed-form finite action NOT computed (only the
stability-relevant structure)" -- is exactly this workflow's target: the finite, H-dependent
correction to the effective kernel, i.e. a candidate deformation delta-nu(y). That question is
genuinely open. Everything below is scoped against the v12 base, not the v11 one.

### 1.1 The action, kernel, and measure (the fixed inputs)
- Action and kernel: `mi_formal_completion_2026/oneloop_laneA_divergences.py:5-9`
  S_m = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],  s = -1,
  K(z) = (sqrt(1+4z)-1)/(2 sqrt z),  Box_u f = (u.grad)^2 f.  u non-dynamical (0 dof,
  curved Dirac closure banked in `mi_formal_completion_2026/constraint_structure.py` /
  `A10_dirac_block.py`): **there is NO frame propagator**. Loop quanta are matter
  (+gravitons). "Frame self-energy" = the 1PI two-point function of delta_u as an
  EXTERNAL background leg.
- Herglotz measure (the kernel insertion): `oneloop_laneA_divergences.py:24-26` and
  `mi_formal_completion_2026/operator_definition.py:124-133`:
  K(z) = a + INT_cut [ 1/(t-z) - t/(1+t^2) ] dmu(t), dmu = rho dt,
  rho_A = (1-sqrt(1-4|t|))/(2 pi sqrt|t|) on -1/4 < t < 0, rho_B = 1/(2 pi sqrt|t|) on t < -1/4.
  Re-run: additive constant a = 0.65411134, z-independence spread 2.38e-11; reconstruction
  error < 1e-6 (`base_rerun.log:38-44`).
- Sum rule (new in v11): INT dmu/|t| = K(inf) - K(0) = 1 EXACT ("unit resolvent weight --
  nothing spare to feed a tadpole"), `oneloop_laneA_divergences.py:131-143`; re-run value
  1.000000 (`base_rerun.log:223`), mpmath 1e-10 in `twoloop_laneC_a0.py` (`base_rerun.log:682-683`).

### 1.2 Propagators and insertion rules available to build on
- **Matter propagator**: standard massive scalar on dS (Bunch-Davies), proxy rho_m = m^2 phi^2
  (stated honestly as a proxy at `oneloop_laneA_divergences.py:16-19`). The matter kinetic
  operator is P = -Box + m^2(1 + sW), a Laplace-type operator with LOCAL endomorphism:
  **W(x) := u^mu [K(Box_u/a0^2) u_mu](x) is a multiplication operator on the matter field**
  (`oneloop_laneA_divergences.py:11-20`). ALL the framework nonlocality is confined to the
  external/background functional W. This is the single most load-bearing structural fact for
  the finite-part computation (Part 2).
- **Box_u on dS is spatially ULTRALOCAL**: d^2/dtau^2 + 3H d/dtau; the similarity transform
  f = e^{-3H tau/2} g gaps it at -9H^2/4, i.e. IR mass floor M_eff >= 3H/2 for the frame
  sector (`mi_oneloop_desitter.py:29-42`; `twoloop_laneA_finite.py:186-204`; re-run PASS).
- **Vertex structure in delta_u around dS** (u = comoving geodesic, W_dS = 0):
  * Linear vertex ZERO at every resolvent order -- the geodesy theorem
    u.(u.grad)^n V = (u.grad)^n (u.V) with u.du = 0
    (`mi_oneloop_desitter.py:62-89`; explicit dS Christoffel computation
    `oneloop_laneA_divergences.py:258-268`; re-run PASS `base_rerun.log:120`).
  * Quadratic vertex: LONGITUDINAL-only tower; Euclidean symbol F(kappa) = K(kappa^2),
    kappa = k0/a0; the one transverse-looking sandwich collapses to the algebraic mass term
    -H^2 a^2 psi^2 (`oneloop_laneA_divergences.py:270-305`; re-run PASS `base_rerun.log:131`).
  * Curvature commutators are ALGEBRAIC: R_{mu a nu b} u^a u^b = -H^2 P_perp exact;
    commutator insertion converts k0^2 -> H^2, never -> kperp^2
    (`oneloop_laneB_mixing.py:91-123`; characteristic roots all k-independent,
    {0, +/-sqrt(7) H} at n=2, `base_rerun.log:345-399`).
  * TT-graviton x delta_u vertex zero (CAS n=1,2 in laneB; the commit-e37c7144 "all orders n"
    script `open_doors_2026_07/mi_oneloop_tt_vertex_all_n.py` re-runs exit 0 but **its two
    check() calls are hard-coded `True` (lines 56, 66)** -- it is a printed argument, not a
    CAS proof. The honest banked status remains: TT vertex zero CAS-verified n=1,2 only,
    argument (not proof) for all n. Do not lean on "all orders n" beyond that.)

### 1.3 Divergent-and-cancelling vs finite-and-uncomputed (the ledger)
- Divergences (complete matter-loop list, Gilkey a2; `oneloop_laneA_divergences.py:196-216`):
  * O_W = s m^4 W -- same form as tree; absorbed into rho_m normalization; a0/K untouched.
  * O_WW = (s^2 m^4/2) W^2 -- NEW operator, longitudinal-only, O(du^4) around dS.
  * O_RW = -(s/6) m^2 R W -- curvature cross term; O_RW/O_W = 2H^2/m^2 ~ 3e-84 (proton).
  * O_BoxW -- total derivative. NO a0-dependent counterterm; NO transverse (grad_perp u)^2.
- a0 protection: additive = ALL-ORDERS EXACT (shift symmetry T -> T + c proved exact for the
  full nonlinear u[dT], `twoloop_laneC_a0.py:51-100`, re-run PASS); multiplicative = closed at
  two loops matter-sector (sum-rule stability + explicit figure-8/double-bubble tadpoles
  multiplying K(0) = 0; `base_rerun.log:741-778`).
- Dressed KL positivity + KMS: rho_1loop >= 0 everywhere both footings, KMS detailed balance
  to 4.1e-12 (`oneloop_laneC_positivity.py`; re-run `base_rerun.log:801-811`). Ghost control
  flags an O(1) injected ghost (necessary-not-sufficient, blind below integrated weight ~0.15).
- Finite parts ALREADY computed by v12 (`twoloop_laneA_finite.py`):
  * [1] bounded below: |W| <= 1 (Herglotz norm) + s = -1 confine M^2 = m^2(1+sW) to (0, m^2];
    V_CW ~ M^4 ln M^2 -> 0^- at the edge; no runaway (re-run PASS `base_rerun.log:621`).
  * [2] dS IR regulated: frame sector gapped at 3H/2, exponential damping of the proper-time
    tail; massless control diverges (detector non-vacuous). Graviton IR inherited unchanged,
    decoupled from the frame by the zero TT vertex.
  * [3] finite nonlocal form factor L(A) = INT dmu ln(1 - A/t): cut only on A < 0, Im L >= 0
    retarded, Re L finite (sqrt-then-log growth).
- Finite parts NOT computed anywhere (this workflow's target):
  * the finite COEFFICIENT FUNCTION multiplying the frame quadratic form (the dressed kernel
    K_eff(z; H, m, mu)) and whether it deforms nu(y);
  * the finite one-loop effective action on the QUASISTATIC (accelerated-frame, W != 0)
    background -- v12's CW analysis was structural (boundedness), not a delta-nu extraction;
  * the H-dependence of the coincident dS propagator's finite part fed through the vertex;
  * graviton-loop finite parts (out of scope here, consistent with v12's open list).

### 1.4 The agentY_* repo-root files (briefing asked; verified)
`agentY_quasistatic.out`, `agentY_eqs.pkl`, `agentY_gates.out` at repo root are **copies of
`real_research/reviews/toe_law/agentY_*`** (quasistatic.out and eqs.pkl byte-identical; the
root gates.out is a TRUNCATED older copy -- the toe_law one contains the additional [SGB]
channel-routing-wall section). Content: the LENS-ONLY SLIP SECTOR (disformal lensing arc),
not the loop arc: sympy quasistatic derivation (pickle keys eqN, eqM, eqC, eqL, cond_rb1,
cond_rb, rest2, slipgrad, DeltaPsi, Ch2_b, branchPhi1), tensor-sector c_T = 1 exact, FRW
quietness (khronon comoving => a_mu = 0 => slip off on FRW), and numeric gates reproducing
banked slip amplitudes (2nu-1 = 61.2/19.4/6.2 at g_bar = 1e-13/-12/-11) + Cassini margin
x1.3e7. Relevant to this workflow only as the quasistatic-matching REFERENCE: the
renormalization condition below anchors the dressed kernel to the same quasistatic limit
these gates encode. Not a loop input.

---

## PART 2 -- THE FINITE-PART COMPUTATION, DEFINED

### 2.1 The object
The one-loop effective action for the external (u, g) background with the matter loop:
  Gamma_1[u, g] = (1/2) Tr ln P,   P = -Box + m^2(1 + s W[u, g]),  W = u.K(Box_u/a0^2)u.
Deliverable: the FINITE part of Gamma_1 as a functional of the frame background, organized as
  (i)  around exact dS (W = 0 background): the dressed frame quadratic form
       Pi(q0; H, m) x |du|^2  ->  dressed kernel K_eff(z; H) -> candidate delta-nu(y);
  (ii) on the QUASISTATIC accelerated background (W = W(y) != 0): the CW functional
       V_CW(m^2(1 + sW(y))) -> direct y-dependent finite correction.
Route (ii) is where a genuine delta-nu(y) can live; route (i) is where the protection
theorem candidate lives (Sec 2.4).

### 2.2 Diagrams (organized by the exact expansion of Tr ln P in W)
  Gamma_1 = (1/2)Tr ln(-Box + m^2) + (s m^2/2) Tr[G W] - (s^2 m^4/4) Tr[G W G W] + ...
  (G = (-Box + m^2)^{-1} on dS, Bunch-Davies.)
- **D1 (single-vertex tadpole, the ONLY O(du^2) dressing around dS):** (s m^2/2) INT sqrt(g)
  G(x,x) W(x). Because the linear vertex vanishes (geodesy theorem) and W = O(du^2) exactly
  around dS, Tr[GWGW] starts at O(du^4): D1 is the COMPLETE one-loop frame self-energy at
  quadratic order. Banked anticipation: "Momentum structure IDENTICAL to tree
  (multiplicative)" (`oneloop_laneB_mixing.py:264-275`). The finite content is
  [G(x,x)]_fin(m, H) -- the renormalized coincident dS propagator, closed form
  (H^2/16pi^2)[stuff with psi(3/2 +/- nu), nu^2 = 9/4 - m^2/H^2, and ln(m^2/mu^2)].
- **D2 (CW functional on the quasistatic background):** V_CW(M^2(y)), M^2(y) = m^2(1+sW(y)),
  evaluated with the tree quasistatic W(y) (the same object the agentY gates and
  `rar_framework_a0_mlfit.py` phenomenology use). Contains the mu-INDEPENDENT nonanalytic
  piece (m^4/64pi^2)(1+sW)^2 ln(1+sW) -- the sharpest candidate for a scheme-independent
  delta-nu(y).
- **D3 (two-vertex bubble, nonlocal correction to D2):** -(s^2 m^4/4) Tr[G W G W]. O(du^4)
  around dS; on quasistatic backgrounds it corrects D2 at relative order (q0/m)^2 -- make
  this suppression explicit rather than dropping it silently (q0 ~ a0/c ~ 1e-18..1e-15 1/s
  vs m_proton ~ 1.4e24 1/s: (q0/m)^2 ~ 1e-78..1e-84; the local CW limit is exact to that).
- **D4 (graviton loop): OUT OF SCOPE** (declared, consistent with v12's open list), except
  where the computation forces contact; the TT vertex is zero (n = 1, 2 CAS) and the
  constrained h_0i mixing is instantaneous, so no finite frame-sector kernel deformation is
  expected from it at O(du^2) -- but that is NOT computed here and stays open.

### 2.3 Regulator and the PHYSICAL renormalization condition
- **Regulator: dimensional regularization on dS** (d = 4 - eps), evaluated via the standard
  maximally-symmetric closed forms. Justification: (a) it preserves dS invariance, so
  [G(x,x)] stays a CONSTANT -- load-bearing for the protection theorem; (b) it does not
  introduce negative-norm regulator fields, so the dressed-KL-positivity lane
  (`oneloop_laneC_positivity.py`) remains meaningful; Pauli-Villars would inject exactly the
  wrong-sign spectral weight the ghost-control was built to flag. The 1/eps poles must land
  on the v11 counterterm list {O_vac, O_W, O_WW, O_RW} and NOTHING else -- a free
  consistency check on every intermediate step.
- **Renormalization condition (PHYSICAL, condition N -- "Newtonian anchor"):**
  the dressed quasistatic kernel, evaluated on the quasistatic background at reference
  y* = g_bar/a0 in the deep-Newtonian regime, equals the tree kernel:
      K_eff(y*; H) = K_tree(y*),   with y* = 1e11 (solar-system scale; Cassini sits at
      y ~ 1.1e12, banked in agentY gates).
  WHY THIS CONDITION: G_N (equivalently the rho_m normalization, equivalently M/L in the RAR
  fit) is MEASURED at high accelerations; every lab/solar determination lives at y >> 1.
  Anchoring there makes delta-nu(y) := nu_eff(y)/nu_eff(y*) x nu_tree(y*) - nu_tree(y) the
  operationally observable deformation.
  WHAT THE y* CHOICE DOES: for a shape-uniform (multiplicative) correction, delta-nu == 0 for
  EVERY y* -- the anchor choice is irrelevant, which is itself the cleanest signature of full
  absorbability. For a genuine shape deformation, moving y* within the Newtonian window
  (1e10..1e13) shifts delta-nu by O(delta-nu(y*)), second order in the correction; report the
  spread across that window as the anchor-systematic, exactly parallel to the a0-footing fork.
- **Scheme-independent vs scheme-dependent, separated in advance:**
  * scheme-INDEPENDENT: mu-logs' coefficients (the running of c_W, c_WW: known signs,
    s m^4/16pi^2 and s^2 m^4/32pi^2 per the a2 assembly); the nonanalytic ln(1+sW(y))
    y-dependence in D2; the H-dependence of [G(x,x)]_fin through psi(3/2 +/- nu) (for
    m >> H it collapses to an (H^2/m^2)-suppressed series -- the H-dependent, hence
    a0 = cH/Z-dependent, terms the task asks about).
  * scheme-DEPENDENT: the constants c_W(mu*), c_WW(mu*). c_W is fully absorbed by condition
    N. c_WW multiplies a NEW operator with no tree counterpart: its constant is NOT fixed by
    any single matching condition. Honest handling: treat c_WW as an unpinned Wilson
    coefficient; report only its running and the mu-independent ln(1+sW) partner. If the
    finite answer is "everything nonuniform sits in c_WW-like unpinned coefficients," that is
    the "measure freedom EATS the quantum correction" finding, reportable as such.

### 2.4 The protection-theorem candidate (to be PROVED or BROKEN, not assumed)
Claim to test at O(du^2) around dS: the finite one-loop frame self-energy is EXACTLY
shape-uniform, delta-K(z; H) = lambda(m, H, mu) x K(z), hence delta-nu(y) == 0 after
condition N. Mechanism (all three legs already banked at divergence level, now to be run
through the finite part):
  (a) W is a MULTIPLICATION operator on the matter field (all K-nonlocality external)
      => Tr[G W] = INT G(x,x) W(x);
  (b) dS invariance (preserved by dim-reg) => [G(x,x)]_fin is a CONSTANT on dS
      => the correction is [const] x INT W = [const] x (tree form), every z equally;
  (c) linear vertex zero (geodesy theorem) => no other O(du^2) channel exists.
What BREAKS it (state precisely; these are the follow-on lanes):
  (i)  quasistatic background: W(y) != 0 activates the CW nonlinearity (D2) -- the
       y-dependence enters through the BACKGROUND, evading (b) locally; this is the real
       delta-nu(y) channel and is computable;
  (ii) the T_uu / derivative-coupled rho_m variant (disformal): the vertex then carries LOOP
       momentum, evading (a); shape deformation ~ (q0/m)^2 -- compute the coefficient, not
       just the scaling;
  (iii) two loops: Tr[GWGW] at O(du^4) feeds the quadratic form once one W leg is put on the
       quasistatic background -- i.e. at two loops (or one loop on nontrivial backgrounds)
       shape-uniformity has no protection. That is the precise "what breaks it at two loops"
       statement to formalize.
  (iv) graviton loop: evades (a) trivially (graviton couples derivatively); protected only
       by the TT-vertex zero (n = 1, 2) -- out of scope, flagged.

### 2.5 The honesty fork that decides observability (declare it NOW, before computing)
The m^2 phi^2 proxy makes <rho_m>_loop = m^2 [G(x,x)]_fin a VACUUM density coupling through
the MI form factor (banked at divergence level as delta_rho_vac, `oneloop_laneA_divergences.py:199-203`).
At finite level this forks:
  * **Fork P (proxy-literal):** keep the vacuum piece. D2's coefficient is m^4/64pi^2 vs the
    tree rho_m W: for proton-mass matter and galactic rho_m ~ 1e-21 kg/m^3 the naive ratio is
    ~1e40 -- catastrophic, and OBVIOUSLY so. If the computation lands here, the honest
    conclusion indicts the PROXY (rho_m = m^2 phi^2 lets vacuum fluctuations gravitate through
    K), not the framework; it is the cosmological-constant problem imported through the vertex.
  * **Fork C (composite/normal-ordered rho_m):** define rho_m as the normal-ordered rest-mass
    density of the actual matter state (dust of localized particles) -- the physically correct
    reading of the framework's own S_m. Then the W-vertex couples to CONNECTED matter
    fluctuations only; corrections scale with the REAL local density, relative size
    ~ (1/16pi^2) x max[(q0/m)^2, (H/m)^2, T/m ...] ~ <= 1e-78 -- unobservable in any regime
    (deep-MOND galaxies, RAR transition curvature, wide binaries all sit ~78+ orders below).
  Run BOTH forks; the spread IS a finding. Expected honest headline (to be earned, not
  assumed): either exact-zero shape deformation (protection theorem) or double-suppressed
  ((H/m)^2 or (q0/m)^2 x 1/16pi^2) -- with the proxy-literal fork reported as a statement
  about the proxy's domain of validity.

### 2.6 Both footings (mandatory)
Every number on: canonical a0 = 9.36e-11 m/s^2 (H_Lambda = 1.808e-18 1/s) AND alt
a0 = 1.13e-10 (H0 = 2.184e-18). The dimensionless corner w_gap/H = 1/(2Z), Z = cH/a0 = 5.79,
is footing-invariant (verified again in re-run, `base_rerun.log:159-164`); dimensionful
H-dependent terms shift x1.207. Nothing structural is expected to flip; verify anyway.

### 2.7 Deliverable scripts (all exit-0 sympy/mpmath, all in this directory)
  1. `finite_D1_selfenergy.py` -- [G(x,x)]_fin on dS (dim-reg, closed form + mpmath check),
     the D1 dressing, the shape-uniformity proof/breakage at O(du^2), condition N applied.
  2. `finite_D2_quasistatic_dnu.py` -- V_CW(m^2(1+sW(y))) on the quasistatic background,
     both forks (P and C), delta-nu(y) extraction under condition N, y*-window spread,
     both footings; sign, magnitude, y-dependence explicit.
  3. `finite_protection_theorem.py` -- the O(du^2) protection statement (a)+(b)+(c) as
     machine checks, plus the precise two-loop/background breakage statement.
No "proves the framework" language anywhere; a null (all-absorbable) is a reportable
structural finding, not a failure.
