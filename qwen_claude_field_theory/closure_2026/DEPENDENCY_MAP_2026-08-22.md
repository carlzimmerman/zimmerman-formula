# DEPENDENCY MAP — Field-Theory Certification Program (a₀ / MOND completion)

**Date:** 2026-08-22
**Scope:** dependency map only — no new theory. For each of the program's 10 primary objectives:
current best status, the backing (with the committed script that verifies it), and the SPECIFIC
open calculation that would certify (or refute) it. Then the master claim list, then the critical path.

**STATUS vocabulary (exactly one per claim):** PROVED (rigorous math) · DERIVED (from an action, not asserted) ·
NUMERICALLY_VERIFIED (green committed script) · SUPPORTED (evidence, not proof) · CONJECTURED · UNRESOLVED ·
FALSE · RETRACTED. Quantity tags: DERIVED / FITTED / ASSUMED / MEASURED.

**One-line standing:** The program has a *coherent skeleton* (2+0 DOF at a unique point, a₀(z)∝H(z),
c_T=1, BTFR theorem) plus a set of genuine *no-gos* (local-disformal lensing, L-closure). It is **NOT a
complete theory.** The single DECISIVE open gate is the **causal IVP of the elliptic-QUMOND lensing
carrier** (coupled Dirac + characteristic/Cauchy analysis of S_York+S_Q+S_m, not done). Cassini-Q₂ and
γ_PPN=1 are unresolved live liabilities; κ=½ and Z are FITTED, never derived.

---

## OBJECTIVE-BY-OBJECTIVE DEPENDENCY MAP

### (1) GR limit recovered
- **Status:** DERIVED (NUMERICALLY_VERIFIED at the selection point).
- **Backing:** Metric-sector G_eff = 2G/(2ξ−η); c_T²=ξ. c_T=1 forces ξ=1; metric-G_eff=G then forces
  η=0. The unique 2+0 point is (ξ=1, η=0, λ free). Sympy static weak-field limit in
  `york/frozen_dirac_degeneracy_2026.py` (all checks pass); `york/FROZEN_DIRAC_VERDICT.md §2`.
- **Depends on / assumption:** the spatially-covariant operator basis
  {K_ijK^ij − λK² + ξ ³R + η a_i a^i} is a CHOSEN ansatz (ASSUMED), not derived. Coefficients FIXED
  (not fitted) once c_T=1 and G_eff=G are imposed.
- **Open calc to certify:** prove the operator basis is forced (no additional admissible operators
  re-open the count), OR accept it as an EFT ansatz. Nothing owed for GR-limit itself.

### (2) CMC clock without an extra propagating scalar
- **Status:** NUMERICALLY_VERIFIED (conditional) at η=0; the FROZEN action is 2+1 (FAIL).
- **Backing:** η=0 York-global-gauge-fixed theory = 2 tensor + 0 scalar. Second-class (P_Φ,C_Φ) pair,
  det Δ=(N√h·2P(Y))², P(Y)=√y(y+2)/(1+y)^{3/2}>0. `york/eta0_direct_dirac_2026.py` (70/70),
  `york/eta0_cubic_quartic_2026.py` (34/34, no strong-coupling mode cubic/quartic),
  cross-checks `york/dof_deformed_cmc_2026.py`, `york/york_step2_closure_2026.py`.
  `york/ETA0_CERTIFICATION_VERDICT.md`.
- **CRITICAL CAVEAT:** the *frozen minimal action as literally written* (η a_i a^i + LOCAL Λ_CMC(K−q))
  is **2+1 — a khronon PROPAGATES** (`york/frozen_dirac_hamiltonian_2026.py` 14/14,
  `frozen_dirac_sectors_2026.py`, `FROZEN_DIRAC_VERDICT.md`). 2+0 holds ONLY for the amended
  η=0 GLOBAL-York-gauge-fixing (=GR+CMC). The LOCAL-multiplier vs GLOBAL-York distinction is
  load-bearing: local = 3 DOF, global = 2. The DOF PRECEDENT spine
  (`theory_2026/exact/THREE_DOF_GATE.md`, published CPC-2026 theorem doi 10.1088/1674-1137/ae2ab0)
  independently says bolting K=q + auxiliary MOND scalar onto GR does NOT remove the scalar without
  two nonlinear degeneracy conditions.
- **ASSUMED, not proved (flagged in the verdict itself):** (i) the full infinite-dimensional H_perp
  bracket is NOT brute-forced — closure rides on ultralocality of the MOND density in h + standard
  Dirac-DeWitt (rank-deciding pieces ARE computed); (ii) York-Hamiltonian gauge-fixing ≡ a covariant
  standalone theory is ASSUMED, not proven.
- **Open calc to certify:** the full functional Poisson-bracket closure of {H_perp, K−q} with the
  complete Hamiltonian (the "remaining decisive calculation" named identically in
  `cuscuton/CMC_CONSTRAINED_MOND.md`, `route2cmc/CMC_A2_THEORY.md`, `scg/`). Prove the
  gauge-fixing↔covariant equivalence.

### (3) Dark-energy density & pressure dynamical (w=−1 exact, cold at recombination)
- **Status:** DERIVED (from an action) — but the identification that seeds it is ASSUMED.
- **Backing:** THE PROMOTION 𝒜(𝒬)≡a₀²(𝒬)=κ²G(−K(𝒬)) with offset-DBI kernel K at β=1; p=𝒦, −𝒦=ρ_Λ
  today ⇒ w=−1 exact (`nbody_2026/stage17`, `opt1_cmb_2026.py PART F2`; `closure_2026/STANDING.md`).
  Sound-speed TURNOVER c_ad² ∝ a⁻³ late / a⁺⁶ early ⇒ dust COLD at recombination on both ν₀ readings
  (`superfluid_2026/sf08_soundspeed_turnover_2026.py`, exact sympy). This CORRECTS the retracted
  "c_s²∝a⁻³ always warm" claim.
- **Assumption / tag:** the promotion a₀²=κ²G(−K) is **ASSUMED** (Carl's identification), *never derived
  from an action inside closure_2026 or superfluid_2026*. β=1 SELECTED not derived; Q₀, Λ_D, ν₀
  FREE/pinned externally. So the FORM is derived; the identification and normalization are inputs.
- **Open calc to certify:** derive the promotion 𝒜=κ²G(−K) from a variational principle (not posit it);
  pin Λ_D, Q₀, ν₀ from data or theory rather than fitting. Compute a BIMOND/host Boltzmann C_ℓ — the
  CMB pass currently rests on a Jeans-scale sufficiency argument (`superfluid_2026/sf09`), NOT a C_ℓ.

### (4) a₀² = κ²c²G ρ_DE derived (the flagship coefficient)
- **Status:** CONJECTURED for the coefficient (κ=½); PROVED as an algebraic identity given κ=½.
- **Backing:** a₀=κc√(Gρ_Λ)=cH_Λ/Z=c²√(Λ/32π); κ=½ ⟺ Z=√(32π/3)=5.789 identically
  (`real_research/predictions/factor_of_four.py`, `ledger_master_numbers.py` prints κ=0.5, Z=5.78881
  exact). Number-field no-go: √(32π/3)∉ℚ(π) (valuation-1 zero) so κ is a pure rational thermodynamics
  cannot select (`real_research/COEFFICIENT_DEFINITIVE_VERDICT.md`, 11 routes + 5 no-go, sympy).
- **MEASURED κ:** 0.551±0.043 (distance-free), 0.465±0.076 (BTFR), 0.374±0.063 (gas-dominated) — straddle
  ½, none pins it to the 3.7% needed (`real_research/kappa_gas_dominated_2026.py`,
  `reviews/mi_distance_free_gbar_estimator_sparc_2026.py`). κ_Verlinde=0.4824 alt (3.5% coincidence,
  p≈0.063; `closure_2026/route4_kappa_derivability_2026.py`).
- **Tags:** FORM DERIVED (dimensional, det=2 unique — `nbody_2026/stage43`); VALUE rests on **FITTED κ +
  ASSUMED ρ_Λ-vs-ρ_total footing**. Both footings (9.36e-11 canonical / 1.13e-10 alt) carried on every
  number. **Z-convention trap:** canonical Z=cH_Λ/a₀=5.789 vs York cq/Z=3cH₀/a₀≈21 differ by 3H₀/H_Λ;
  the memory-index "√(32π/3)≈21" conflates them (`reviews/kappa_h0_convention_audit_2026.py`).
- **Open calc to certify:** derive the O(1) rational κ from first principles. PROVED structurally
  unforceable by equilibrium horizon thermodynamics to date; 12 routes RETRACTED
  (`nbody_2026/stage43,46→52`). This is the acknowledged non-derived CORE — "one factor of two."

### (5) MOND interpolation + BTFR
- **Status:** BTFR PROVED (theorem); interpolation SUPPORTED (imported, not forced).
- **Backing:** BTFR v⁴=GM_b a₀ with coefficient 1 from the strictly convex Route-A free function
  (`mi_route_a_field_theory_2026.py` 11/11) — existence, uniqueness, Newton's 3rd law, virial, exact
  BTFR; also yields κ=0.465±0.076. The a₀-line AQUAL free function has the exact closed form
  f(z)=½√z√(1+4z)+¼asinh(2√z)−√z with deep-MOND limit EXACTLY (2/3)z^{3/2} (AeST's own 2/3 coefficient,
  no free constant) — `superfluid_2026/sf01_ansatz_closure_2026.py PART B` (sympy), adjudicated
  `closure_2026/sf12_adjudicate_sf11b_2026.py`. **This is the single strongest genuinely-DERIVED a₀-tie.**
  RAR 0.108 dex on 175 SPARC / 3389 pts at Υ=0.70 (`real_research/rar_framework_a0_mlfit.py`).
- **Assumption / tag:** interpolation μ(x) is a CHOICE carried by the action (via V in the auxiliary
  Legendre pair — `scg/SCG_MOND_PROGRAM.md`, sympy-verified), IMPORTED not forced. The a₀-line itself is
  a FITTED/MEASURED phenomenological relation; the closed form is rigorous GIVEN it. RAR is
  convention-compatible + NON-diagnostic of 9.36e-11 (anchoring COSTS 6%, is CHEAPER not better —
  earlier "anchored fits better" RETRACTED). Υ FITTED, degenerate with a₀.
- **Open calc to certify:** derive (not host) the interpolation shape from the dark-sector action. The
  a₀-line is HOSTED, not derived, in EVERY mechanism tested (B DEAD, E extension, C survivor).

### (6) Lensing without a 2nd metric or superluminal channel
- **Status:** UNRESOLVED (γ_PPN=1 engineered; causal gate of the working carrier OPEN).
- **Backing (what IS settled):**
  - **Local-disformal no-go [DERIVED / NUMERICALLY_VERIFIED]:** {2+0}∩{gap-closing}∩{luminal}=EMPTY for
    a local single-metric foliation-spatial disformal g̃=Cg+D uu. Gap-closing D needs inverse-Laplacian
    (non-local) and GW170817 forces |D/C|≤2e-15 while lensing needs D/C=O(1) (~15 orders).
    `york/gate2_dof_preservation_2026.py`, `gate2_lensing_2026.py`, `gate2_cone_gw170817_2026.py`,
    `gate2_hostile_referee_2026.py` (all green); `york/GATE2_D_VERDICT.md`.
  - **Elliptic-QUMOND carrier [NUMERICALLY_VERIFIED at DOF level]:** ∇²Φ=∇·[ν∇Ψ] supplies ρ_ph=(ν−1)ρ
    at 2+0, single-metric, c_γ=c_GW=1, g_lens=g_dyn; auxiliary sector 0 DOF, det Δ_aux=k¹² robust to
    matter coupling. `york/qumond_coupled_dirac_2026.py`.
- **THE OPEN GATE [UNRESOLVED]:** elliptic-carrier CAUSAL acceptability. The conservative
  `RESULT_york_cmc_mond_and_lensing_nogo.md §4c/§5/§6` + `MASTER_CANDIDATE §Open` label it
  **UNSETTLED — "not proven acausal, not proven causal."** The newer `york/qumond_causality_2026.py`
  OVER-CLAIMS it "CLEARED" via a heuristic 4-point preferred-foliation argument whose own INCOMPLETE
  concedes no covariant Lorentz-invariant completion exists. **Honest status = OPEN** (the 2026-08-22
  retraction of the "superluminal/trilemma-as-established" framing is logged; the *question* is
  unsettled either way).
- **γ_PPN=1 [UNRESOLVED / ASSERTED-NOT-DERIVED]:** the bare gravity action gives
  γ_PPN=log r/(log r−2)≠1 (under-lenses); γ=1 is IMPORTED (TeVeS/AeST), a conformal shift leaves the
  slip invariant so no free φ(Φ) sets it. `york/referee_gateF_2026.py`, `ppn_lensing_cassini_2026.py`,
  `york/FINAL_VERDICT.md Gate F`. (In the AeST-host arm, γ_PPN=1 residual 0.601σ is INHERITED, MOND-shared,
  trivial — but that is the parent theory, not this action.)
- **Open calc to certify:** full nonlinear coupled Dirac + characteristic/Cauchy (hyperbolicity)
  analysis of S_York+S_Q+S_m; and a mechanism that DERIVES γ_PPN=1 rather than engineering the disformal
  slip. This is THE central gate (see Critical Path #1).

### (7) Nonlinear Hamiltonian / Dirac closure
- **Status:** UNRESOLVED (favourable at representative/generic points; full bracket OWED).
- **Backing (York arm):** 2+0 rank algebra certified to cubic/quartic order at η=0
  (`eta0_direct_dirac` 70/70, `eta0_cubic_quartic` 34/34) — but the infinite-dim H_perp bracket is not
  brute-forced.
- **Backing (bimetric+khronon host, closure_2026):** second-classness of {C,Ĉ} shown at a lattice
  representative (=−7.347, `sf21_weak_zero_test_2026.py` 8/8) and in the 1D-reduced CONTINUUM
  (Σ=0.1835, `sf24_continuum_dirac_2026.py` 13/13, GR control recovered exactly). SF18 count 7=2+5 DOF,
  no room for the 8th Boulware-Deser mode (`sf18_step4_structure_2026.py` 11/11) — CONDITIONAL on
  {C,Ĉ} being genuinely second class.
- **CRITICAL GAP:** **the secondary constraint (SF14) was NEVER computed in closure_2026.** LEDGER SF14
  row = "external, not seen — UNVERIFIED"; external SF15 "projectable PASS" REJECTED (script crashes,
  test vacuous). The full Hessian in redefined variables (EH+EH+interaction), the exact GR kinetic
  reduction, and full Dirac consistency are explicitly OWED. Status: NEITHER closed NOR killed
  (`closure_2026/LEDGER.md`). History here is dominated by control-caught reversals (6 logged in
  `RETRACTIONS.md`; a ∂-derivative zero mistaken for a Hessian degeneracy ≥2×).
- **Open calc to certify:** compute the secondary constraint SF14 and evaluate the single
  fully-specified {C,Ĉ} bracket with the full (EH+EH+interaction) Hessian in redefined variables.
  It is a specified calculation, not open-ended — but it is not done.

### (8) Exact DOF count = 2 (tensor) + 0 (scalar)
- **Status:** NUMERICALLY_VERIFIED conditionally (2+0 at the η=0 point, conformal matter map D=0).
- **Backing:** same as (2) — `eta0_direct_dirac_2026.py` (70/70), `eta0_cubic_quartic_2026.py` (34/34),
  `frozen_dirac_degeneracy_2026.py`. A NONZERO foliation-spatial disformal D preserves the 2+0 pair
  (Z_Φ=0, `gate2_dof_preservation_2026.py`); covariant-X coupling revives the scalar (2+1).
- **Conditions / tags:** DERIVED (rank result) CONDITIONAL on (i) the conformal matter map D=0 (disformal
  branch INCOMPLETE), (ii) ultralocality-based H_perp closure (not brute-forced), (iii) η=0 (the frozen
  η≠0 action is 2+1). The DOF PRECEDENT (`exact/THREE_DOF_GATE.md`) and the SCG Hessian no-go
  (`scg/hessian_nogo.out`, `verify_lapse_kinetic_degeneracy.py` — det M=c4·d1−d2²/4 rank-drop) show 2+0
  needs a genuine kinetic-matrix degeneracy, present only in the acceleration-FREE A1/A2 branches.
- **Open calc to certify:** THE BINARY (`scg/hessian_nogo.out`, `exact/THREE_DOF_GATE.md`) — whether the
  GR-compatible cubic A1/A2 branch hosts nonlinear MOND (U_XX≠0) or forbids it (quartic no-go). Proven
  2+0 only through CUBIC order; the two CPC-2026 degeneracy equations were never applied at quartic.

### (9) Causal initial-value problem (well-posed hyperbolic evolution)
- **Status:** UNRESOLVED — **THE single decisive open gate.**
- **Backing:** none complete. The one lensing construction that closes the phantom at 2+0 single-metric
  (elliptic QUMOND) has an INSTANTANEOUS elliptic sector; whether that is causally acceptable under the
  CMC preferred foliation (Hořava-type) or genuinely acausal is UNDECIDED. `RESULT §4c/§5/§6`,
  `MASTER_CANDIDATE §Open item 2`. The local-disformal alternative is a proven no-go (6); the newer
  `qumond_causality_2026.py` heuristic over-claims a clearance its own INCOMPLETE retracts.
- **Open calc to certify:** the full nonlinear coupled Dirac + characteristic/Cauchy analysis of
  S_York+S_Q+S_m — determine the principal symbol / characteristic cones of the coupled system, whether
  the elliptic constraint sector admits a well-posed constrained evolution, and whether any mode
  propagates outside the light cone. **NOT DONE. This gates 6, 7, and the whole completion.**

### (10) PPN / Cassini / GW / cosmology / perturbations
- **Status:** MIXED — GW PROVED-safe; Cassini & γ_PPN FAIL/UNRESOLVED; CMB conditional; α₁,α₂ owed.
- **GW / c_T [PROVED, identity]:** c_T=1 exactly, |c_T−1|<1e-15, because c₁₃=0 for every K_B and any
  free function; α_M=0 identically on FRW+TT (`real_research/reviews/c14_dictionary_validity_2026.py`).
  A confirmed α_M≠0 (LISA/ET) falsifies the class. In the York action c_T²=ξ=1 exactly
  (`stability_taskG_2026.py`, `gate2_cone_gw170817_2026.py`).
- **a₀(z) [DERIVED, Z-independent — the flagship prediction]:** a₀(z)=a₀,₀·H(z)/H₀ from K=q=3H on FLRW
  (`york/cosmology_flrw_2026.py`, Gate D PASS). **FOOTING FORK (unresolved):** the CMC-clock reading
  gives a₀∝3H (RISING); the cuscuton/DE reading a₀∝√ρ_DE gives a₀=CONST for w=−1 (evolves only under
  DE-domination). They agree ONLY under DE-domination; which is "the" prediction is NOT settled
  (`MASTER_CANDIDATE §Open`). **CROSS-SUBSYSTEM INCONSISTENCY:** empirical fits use the √ρ_DE
  (flat/declining) reading, which the repo's own a₀(z) data FAVOUR; the master York candidate DERIVES
  the H(z) (rising) reading, which the same data DISFAVOUR at ~4σ
  (`real_research/A0Z_MODEL_COMPARISON_2026-06-06.md`, χ²/dof 7.10). Also
  a₀(rec)/a₀(0)=0.0060 → MOND OFF at recombination (needs ν₀=2.15e-5, ~9× over RAR ceiling 2.36e-6 —
  a live squeeze; `superfluid_2026/sf07,sf08`).
- **Cassini Q₂ [UNRESOLVED / NUMERICALLY_VERIFIED liability]:** for the theory's own μ=x/√(1+x²),
  Q₂≈15–21e-27 s⁻² ⇒ 3.9–6.0σ (8.3–11.2σ for RAR/MS08) over the (3±3)e-27 bound. a₀ spatially constant
  ⇒ NO DHF Case-B escape. `york/referee_gateF_2026.py` (min favorable 3.87σ), `ppn_lensing_cassini_2026.py`,
  `york/FINAL_VERDICT.md Gate F (FAIL)`, `real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md`. The named fix
  (exponential-approach U kernel) is NOT adopted in the certified RESULT/MASTER action ⇒ live falsification-
  grade liability. **L-CLOSURE no-go (Theorem 8):** the EFE scale L=√(GM/a₀) cannot be a single-valued
  action-determined LOCAL functional of ρ while keeping 2+0 and passing Cassini — the external field is
  an INPUT, not locally derivable (`york/york_Lclosure_{global,local,hierarchy,dirac}_2026.py`,
  `L_CLOSURE_VERDICT.md`). So Cassini's burden is conceded, not discharged.
- **G_eff [NUMERICALLY_VERIFIED FAILURE, structurally patched]:** two-channel additive coupling ⇒
  G_eff=2G (`york/referee_gateE_doublecount_2026.py` 9/9). Cured ONLY by ASSUMING a single physical
  metric / single-potential elliptic carrier (Φ=Ψ) — fixed by construction, contingent on that choice.
- **CMB [NUMERICALLY_VERIFIED conditional]:** CLASS full-Boltzmann Δχ²=1.34 over 4998 multipoles (0.01σ),
  CONDITIONAL on a₀(rec)/a₀(0)≤9.7e-3–3.7e-1 (banked 0.0060 clears) AND an uncomputed response number S
  (clears S≤0.54, clashes S≥20.6 — a hi_class build, not an argument). `nbody_2026/stage19*,stage76`,
  `opt1_cmb_2026.py` (36/36). The AeST 0.01σ pass does NOT transfer to a bimetric host (gravity sector
  differs); a host Boltzmann C_ℓ is OWED.
- **PPN α₁,α₂ [UNRESOLVED]:** the K_B<2.5e-5 bound WITHDRAWN (theory sits at c₁₂₃=0 where the literature
  PPN series is inapplicable); in force K_B∈[2.1e-4,0.25]. Full-theory α₁ with the scalar retained
  (local spin-0 speed vs w_⊙=1.234e-3 c) is the OWED computation gating the PPN front
  (`stage73/74`, `alpha2_*_2026.py`).
- **Open calc to certify:** (a) full α₁,α₂ with scalar retained + local spin-0 speed; (b) the CLASS/hi_class
  build fixing S; (c) a Cassini-safe kernel replacement that survives SPARC (the OWED route6B B8.7 test);
  (d) resolve the a₀(z) footing fork.

---

## MASTER CLAIM LIST (by classification)

### PROVED (rigorous math)
- a₀-line AQUAL free function closed form f(z)=½√z√(1+4z)+¼asinh(2√z)−√z; deep-MOND limit EXACTLY
  (2/3)z^{3/2} (no free constant) — `sf01`, sympy. **[strongest derived a₀-tie]**
- β=1 DBI kernel is analytic at its minimum, supplies only even powers; the 3/2 MOND power is available
  at neither the minimum nor the ½-power wall — `sf01 PART A`, exact.
- "Lapse-affine in ONE lapse ≠ lapse-degeneracy in both": det H=−36β²S²/N̂¹⁴≠0 — `sf12`, exact 2×2 det.
- Double-count theorem: a₀-line + Ω_dm dust + conserved charge ⇒ galactic dark mass over-supplied by
  factor∈[√λ,λ], λ=6.375 ⇒ 0.40–0.80 dex — `route5_double_count_theorem_2026.py` (32/32), 5 kernels +
  control. (Needs a 6th hypothesis — dark mass traces baryons — to bite as written.)
- π-cancellation: κ=½ ⟺ Z=√(32π/3) identically (`stage66 PART C`) — a property of the ADOPTED value,
  NOT evidence for κ=½.
- Number-field no-go: √(32π/3)∉ℚ(π) — `COEFFICIENT_DEFINITIVE_VERDICT.md`, valuation argument.
- c_T=1 exactly (identity, c₁₃=0 ∀K_B) — `c14_dictionary_validity_2026.py`.
- York/CMC geometric DOF: conformal 3-metric + TT momentum = 2 polarizations (York 1971) — pure math;
  application to the deformed action is conditional.
- Cuscuton non-dynamical (bare) — `cuscuton/CUSCUTON_MOND.md`, sympy.

### DERIVED (from an action)
- G_eff=2G/(2ξ−η); c_T=1 & G_eff=G select (ξ=1, η=0) — `frozen_dirac_degeneracy_2026.py`.
- a₀(z)=a₀,₀H(z)/H₀ from K=q=3H (Z-independent) — `cosmology_flrw_2026.py` (Gate D). [footing fork open]
- a₀(z)/a₀(0)=(1+σ²)^{−1/4} promotion law, host-independent — `sf07`, `nbody_2026/stage17`. [ν₀ fitted]
- BTFR v⁴=GM_b a₀ coefficient-1 theorem from convex Route-A free function — `mi_route_a_field_theory_2026.py`.
- DOF PRECEDENT: GR+auxiliary scalar = 3 DOF; 2 needs two nonlinear degeneracy conditions —
  `exact/THREE_DOF_GATE.md` + CPC-2026 theorem.
- SCG Hessian no-go: exact d=2 quadratic branch is linear in Dφ, cannot carry nonlinear MOND (μ'≠0);
  c_T no-go (c_T=1 ∀epoch forces f=const) — `scg/SCG_MOND_PROGRAM.md`.
- MOND via auxiliary Legendre pair (χ,Φ), no kinetic term ⇒ QUMOND + BTFR — `scg/`, sympy.
- Gen-1 tidal-khronon = 3 DOF and GW170817-excluded by ~29 orders; η_K=0 forced twice —
  `first_principles/FIRST_PRINCIPLES_VERDICT.md`.
- a₀²(𝒬)=κ²G(−K) w=−1 exact — `nbody_2026/stage17` (promotion itself ASSUMED).
- Sound-speed turnover ⇒ dust cold at recombination — `sf08`, exact.

### NUMERICALLY_VERIFIED (green committed script)
- η=0 2+0 DOF, cubic/quartic no strong-coupling — `eta0_direct_dirac` (70/70), `eta0_cubic_quartic` (34/34).
- Frozen action is 2+1 (khronon propagates) — `frozen_dirac_hamiltonian` (14/14). [documents the FAIL]
- Elliptic QUMOND carrier 0 aux DOF (det Δ_aux=k¹²) — `qumond_coupled_dirac_2026.py`.
- Foliation-spatial disformal preserves 2+0 — `gate2_dof_preservation_2026.py`.
- L-closure no-go, three legs — `york_Lclosure_{global,local,hierarchy,dirac}_2026.py`.
- G_eff=2G double-count FAILURE — `referee_gateE_doublecount_2026.py` (9/9).
- Cassini Q₂ 3.9–11.2σ liability — `referee_gateF_2026.py`, `ppn_lensing_cassini_2026.py`.
- Second-classness {C,Ĉ}≠0 at lattice (sf21 8/8) and continuum (sf24 13/13) points. [SF14 owed]
- SF18 count 7=2+5, no BD mode — `sf18_step4_structure_2026.py` (11/11). [conditional]
- Mechanism B DEAD as halo carrier — `sf39_mechanismB_promotion_static_2026.py` (47/47).
- Mechanism E khronon carrier: bare form DEAD (scaling), free-function extension VIABLE candidate —
  `sf39_khronon_carrier_2026.py` (54/54).
- lapse-kinetic degeneracy det M rank-drop — `scg/verify_lapse_kinetic_degeneracy.py`.
- Gen-2 tensor GW170817-safe (K_T=1, k² not k⁴) — `gen2/gen2_tensor_numeric_crosscheck_2026.out`.
- RAR 0.108 dex / weak-lensing KiDS χ²/dof=2.03canon-0.94alt parameter-free — `rar_framework_a0_mlfit.py`,
  `nbody_2026/stage12`.
- Solar-system screening (exponential kernel) 1 AU ~1e-3457 m/s² — `opt1_gates_2026.py`.
- κ MEASURED 0.551/0.465/0.374 — `kappa_gas_dominated_2026.py`, `mi_distance_free_gbar_estimator_sparc_2026.py`.
- CMB CLASS Δχ²=1.34 (conditional on S) — `nbody_2026/stage19*`, `opt1_cmb_2026.py` (36/36).
- Environmental fork: ρ_local excluded 13–34σ — BIG-SPARC pipeline.
- INTEGRITY: 320 real_research scripts run clean, zero theatre — `INTEGRITY_AUDIT.md`.

### SUPPORTED (evidence, not proof)
- Locality theorem (only the local field supplies the 1.2–3.4e4 screening contrast) — `sf06`. [candidate
  list completeness ASSUMED — a strong argument, not a proof]
- Mechanism C two-field lock: amplitude IDENTITY derived, but AQUAL Cassini Q₂ +18–20σ; fails
  double-count gate 5 — `closure_2026/LEDGER.md`. [surviving structural candidate]
- Nonlocal-gravity escape clears solar system but cannot host κc√(Gρ_Λ) — `route6B_nonlocal_gravity_2026.py`.
- BIMOND host: R1 pass + ephemeris void, "no COMPUTED kill" — `sf07`. [BD ghost + CMB owed]
- CORE reframing a₀=κc√(Gρ_Λ) — form derived, value on fitted κ + assumed footing.

### CONJECTURED
- κ=½ (FITTED; Bayesian ~6:1 preference, not a measurement).
- Four-auxiliary MMG closes to 2+0 (proposed route; functional bracket not done).
- route2cmc λ=1/3 three-way coincidence ⇒ 2+0 (un-run {H_perp,K−q} bracket).
- κ derivable from entropic counting — NO (κ_V=0.4824, family spans 3.14×).

### UNRESOLVED (open gates)
- **Elliptic-carrier causal IVP — THE decisive gate.**
- γ_PPN=1 / lensing=dynamics (engineered disformal input, not derived).
- Cassini Q₂ 3.9–11.2σ (no environmental escape; named fix not adopted).
- Nonlinear Dirac closure / secondary constraint SF14 (never computed in closure_2026).
- THE BINARY: A1/A2 cubic branch host nonlinear MOND? (quartic not applied).
- Coupled cuscuton+MOND(a_μ) Dirac count.
- a₀(z) footing fork (∝3H vs ∝√ρ_DE) + cross-subsystem inconsistency (~4σ).
- Full α₁,α₂ with scalar retained; CMB response number S.
- Dust problem 2d (collapse endpoint off Sgr A* by ~5e5; all 2nd-field escapes dead).
- Galaxy clusters η(R500)=1.72–2.08 (48% at R500; a₀-bump not derivable from action).
- BD-ghost freedom cosmologically (sf10 two-lapse Hessian INCONCLUSIVE).

### FALSE / RETRACTED
- FALSE: frozen action is clean 2+0 (it is 2+1); York/CMC-MOND is a complete theory (Gates E,F fail);
  a₀ normalization derived (input, Z FITTED); "exact" a₀-line α=1 (ephemeris 1278× — "exact" withdrawn,
  phenomenology survives on exponential kernel); Gen-2 c_T EXACTLY λ_K-independent (ψ-mixing residual);
  Mechanism D phonon a₀-tie (keyed to potential, dies at pinned b); a₀-bump "kernel removes 74–89%"
  (48%); ȧ₀/a₀≈−3e-11/yr (7–8 orders + wrong sign).
- RETRACTED: all SM numerology (m_p/m_e, α⁻¹, sin²θ_W — public 2026-06-23); all 12 κ routes (dS-Unruh
  forces a₀=2cH_Λ excluded 15.6σ, crossover circular, ε_tot TT-kill, Bose-Einstein 11.1σ low, etc.);
  Z²=32π/3 topology derivation; X-ansatz two-sided a₀-tie (sf05/sfD kill); AeST-as-2-DOF (AeST is 6 DOF);
  3×3 rank argument for CMC-MOND; sf10 PART E manufactured win; "c_s²∝a⁻³ always warm"; DESI-CPL a₀-bump
  "+6% at z≈0.4"; AeST action mis-transcription (corrected 2026-08-17, embedding still owed);
  elliptic-carrier "superluminal/trilemma-as-established" (2026-08-22, question now correctly OPEN);
  all dead cluster mechanisms (Helmholtz positive-mass, q-route, charge-abundance, gated Proca, Route A′).

---

## CRITICAL PATH — ordered calculations to reach or refute a complete theory

The central gate is #1; everything downstream is conditional on it. Ordered so each step's prerequisite
precedes it.

1. **Causal IVP of the elliptic-QUMOND lensing carrier (THE central gate).**
   Full nonlinear coupled Dirac + characteristic/Cauchy (hyperbolicity) analysis of S_York+S_Q+S_m:
   principal symbol / characteristic cones of the coupled system; whether the instantaneous elliptic
   constraint sector admits well-posed constrained evolution under the CMC preferred foliation; whether
   any mode propagates outside the light cone. *Refutes the completion if acausal; unblocks 6/9/10 if
   causal.* Currently only a heuristic exists (`qumond_causality_2026.py`, over-claims). **Not done.**

2. **Nonlinear Hamiltonian/Dirac closure — compute the secondary constraint SF14 and the full {C,Ĉ}
   bracket** in redefined variables (EH+EH+interaction Hessian, exact GR kinetic reduction). A single
   fully-specified calculation; certifies (or kills) the 7-DOF / 2+0 count beyond representative points.
   `closure_2026/LEDGER.md` SF14 row = UNVERIFIED. **Not done.**

3. **THE BINARY (scalar sector):** apply the two CPC-2026 quartic degeneracy equations to the
   GR-compatible A1/A2 cubic branch — does U_XX≠0 (nonlinear MOND) survive at 2+0, or does the no-go
   fire? Resolves objective (8) beyond cubic order. `scg/hessian_nogo.out`. **Not done.**

4. **Derive γ_PPN=1 rather than engineer it.** A single-metric coupling that yields lensing=dynamics
   from the action without importing the TeVeS/AeST disformal slip. Gates objective (6). Conditional on #1.

5. **Cassini-safe kernel that still fits SPARC.** Adopt/justify the exponential-approach U kernel (named
   in FINAL_VERDICT but NOT in the certified action) and run the OWED route6B B8.7 SPARC test — does a
   kernel sharp enough to pass Cassini Q₂ still fit RAR? Discharges the standing Cassini liability (10)
   or confirms the L-closure verdict that the external field is an irreducible INPUT.

6. **Full α₁,α₂ with the scalar retained** + local spin-0 speed vs w_⊙=1.234e-3 c. Gates the PPN front;
   the K_B window currently rests on a literature formula inapplicable at c₁₂₃=0. Conditional on #2/#3
   (need the settled DOF/scalar content first).

7. **Host Boltzmann C_ℓ (CLASS/hi_class build) fixing the response number S.** Turns the conditional CMB
   pass (S≤0.54 vs ≥20.6) into a computed result. Also settles the a₀(z) footing fork (∝3H vs ∝√ρ_DE)
   by which reading the perturbations demand. Conditional on #1 (needs the causal, closed action).

8. **Derive the promotion a₀²=κ²G(−K) from a variational principle** (currently ASSUMED) and pin
   Λ_D, Q₀, ν₀. Would upgrade objective (3)/(4) from hosted to derived. The κ=½ coefficient itself is
   PROVED structurally unforceable to date — this is the "one factor of two," treated as an EFT input,
   NOT on the certification critical path unless a new forced kernel appears.

**Residual physics not on the certification path but blocking observational viability:** dust-collapse
problem 2d (Sgr A* by ~5e5, all 2nd-field escapes dead); galaxy clusters (48% at R500, a₀-bump not
derivable); BD-ghost freedom of any bimetric/Hassan-Rosen host cosmologically.

---

## HONEST CEILING

The program is a **candidate EFT-at-a-frontier**, correctly labelled "CANDIDATE, NOT proven" in every
top-level verdict (`RESULT §6`, `MASTER_CANDIDATE`, `FINAL_VERDICT OUTCOME 2`, `LEDGER`). It has ONE
clean derived distinctive prediction — **a₀(z)∝H(z)** (modulo the footing fork) — and TWO genuine no-gos
(local-disformal lensing, L-closure). Its coefficient (κ=½, Z) is FITTED and provably unforced. It is
NOT a complete relativistic MOND theory: the causal lensing gate is OPEN, Cassini and γ_PPN are
unresolved, and the nonlinear Dirac closure (secondary constraint) is owed. No claim above is graded
PROVED/DERIVED without a committed backing script; the causal question is UNRESOLVED, not settled.
