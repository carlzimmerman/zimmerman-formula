# XR3 — field-theory closure obligations across the parallel work (2026-09-26)

**What this is.** A read-only cross-thread map: for each of the thirteen requirements of
[`FRIED_CHICKEN_SPEC.md`](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md) (amended operative text,
commit `9092fc0fd`, SHA-256 `851e44ab…0390`), what is established and at what scope, what is open, who is on it,
and what nobody is on. Then the conflicts between the author's 2026-09-26 decisions and the lead track's (astra's)
direction, and the smallest ordered set of calculations that would take **one** branch to "one action, varied,
every gate at one parameter cell". It is a work map, not a result. **The target is OPEN.**

**Snapshot.** 2026-09-26, 15:20–15:42 EDT; HEAD `37edac81b` plus the uncommitted working tree. Astra's
`real_research/closure_push_2026_09_26/` was being written during this review (CONTRACT amended 15:37, README 15:41,
recipe block "Constructive continuation — CD26-2" added about the same time). Statements about it are as of 15:42.
Nothing outside `real_research/cross_thread_review_2026_09_26/XR3_*` was edited, run or moved. The only computation
is [`XR3_checks.py`](XR3_checks.py) (≈1 s, numpy/sympy; output [`XR3_checks.out`](XR3_checks.out)).

**The branch reviewed ("B-νmono").** C-H (`g03_covariant_action_2026/ACTION.md`) + the BPS khronon terms
α_c a² − c₂K² with β = 0 (L340) + the leaf-average λ-term −c₂(K − ⟨K⟩_Σ)² (L350) + ν_mono through the heat filter
(requirement 1, operative) + the L353 subtraction pair + the L361 bound-region kernel + the vacuum gate (L359, pinned
by DE1–DE3 to p = 1, x_c0 = 2.5) + a dark-mass state that is not yet built. Causality by criterion B.
**Declared inputs, kept as inputs:** κ = ½ (measured 0.465 ± 0.076 BTFR, 0.55 ± 0.17 distance-free; provably not
derivable in this action class, `kappa_closure` k01–k03; Z = cH_Λ/a₀ = √(32π/3) = 5.7888 is κ restated), both a₀
footings (9.36×10⁻¹¹ / 1.13×10⁻¹⁰ m s⁻²). **No new dark-matter particle species**: the carrier has to be a state of
the framework's own field. The dark **mass** is still required (CMB, clusters); dropping the particle does not drop
the mass.

---

## 1. The thirteen requirements: established, open, owner, orphaned

Owners, as named by the caller: **astra** CD26-2 routes R1–R6 (R5 and R6 were added at 15:37); **XC** = "Gravity
theory review and progress" (`extra_crispy_2026`, recipe edits); **DE** = "Gravity theory and dark energy"
(`dark_energy_2026`); **GTA** = "Gravity theory advancement" (L353–L364, `acceleration_trigger_2026`);
**RPO** = "RPO work toward closure" (PM lanes L365–L390); **CI** = the merger-lane session (`merger_infall_2026` L370–L373,
`condensate_dust_2026`). "Nobody" means that no live file or contract on the record addresses the item for B-νmono.

| # | Operative requirement | Established (scope; evidence) | Open for B-νmono | On it now | Status |
|---|---|---|---|---|---|
| 1 | ν_mono through the heat filter, QUMOND form | Kernel defined, phantom slope > 0 at every y (L340 A1; Lean XC4 `mono_phantom_increasing`). SPARC indistinguishable from ν_RAR, \|Δχ²\| ≤ 2 (L340 K2). Deep MOND and BTFR unchanged. Solar-System floors ξ ≥ 0.031/0.045 pc (L340 S1). **Scope:** the ungated static C-H equations. | (a) The splice is C^{1,1}, not C²: dC_L/dy jumps from −0.0361 to −0.0014 at y* = 2.3374 (astra `peer_review…/xc1/REVIEW.md`; XR3 K1). Any Taylor-based vertex or symbol needs either a declared C² variant or a nonsmooth argument. (b) Derive the quasistatic law from the **assembled** action (gate + region kernel + subtraction pair), not from C-H alone. (c) Wording: ν_mono = ν_RAR only for y ≤ y* (not up to y_p = 2.540), and the largest deviation is 0.0104 dex at y ≈ 14, not "≤ 0.01" (XR3 K2). | XC (recipe text only) | (a), (b) **ORPHANED** |
| 2 | N_grav = 2; a clock scalar only if counted separately and healthy | Frozen reduced block: exactly one extra scalar with positive kinetic energy for α_c > 0, c₂ > 0 (L340 H2; astra `closure_resume…/recipe_construction_followup.md`). Generic ADM Legendre transform and the λ = 1/3 degeneracy (astra `closure_doors…/action_consistency/RESULT.md`). | Full Dirac classification of the assembled action in three regimes (gate-off FRW plateau, gate-on galaxy plateau, one transition patch). It must cover U, the heat-flow fields W/L, λ₀, the L353 pair, L361's w/ψ/χ, the gate multiplier, the leaf average's global term, k = 0 and the zero-field rank. Under criterion B the khronon is the required global time function. That supports reading it as the spec's permitted clock, but does not replace the count. | nobody (astra's D2 stopped at the generic Legendre step) | **ORPHANED** |
| 3 | Φ = Ψ, both derived | Static leading-order C-H/K block has equal, independently solved potentials (ACTION.md; L340 H5; astra recipe_audit calls it "conditional"). L353: lensing = dynamics for both species (NR). | Redo the derivation with the varied gate's stresses, the region kernel and the covariant subtraction pair. KM2's moving-source amplification (≤ 5 %) is a prediction, not a gate. | nobody | **ORPHANED** |
| 4 | PPN derived, not assumed | β = γ = 1 derived in the reduced static khronometric sector. α₁ = −4α_c, α₂ = α_c(α_c − c₂)/(2c₂), η_N = (11/3)α_c (KM3). α₃, ζᵢ, ξ and the filtered remainder are documentary (KM3 P4, P6). | Full PPN of the assembled action in the Solar System: gate on (x ~ 10⁶), region kernel with M = 0, filtered remainder and δS terms computed rather than documentary. | nobody (KM3 idle since 09-25) | **ORPHANED** (low risk) |
| 5 | ∇_μT^{μν} = 0 for ordinary matter via the Ward identity | Minimal S_m[g,ψ] has its own identity. The diffeomorphism identity including the gate and heat fields is written out, and it shows the gate term cannot be dropped (astra action_consistency). | The identity for the assembled action with f varied. L361's baryon couplings (−fρ_bψ + fρ_bχ) must become minimal coupling to one metric that carries the phantom. The carrier's extra L353 λ-coupling must stay in the dark state. | nobody | **ORPHANED** |
| 6 | c_T = c, GW170817 | β = 0 gives c_T = 1 in the TT sector (L340; L351). The shear-completed gate keeps c_T = 1 on isotropic backgrounds when Z_T = M² + 2(Bf_R + C_R) > 0 (L351; astra `environment_gate/REPORT.md`). | TT modes on anisotropic gate-on MOND backgrounds, with the constitutive term and δS (expected to be tiny; not computed). | nobody | **ORPHANED** (low risk) |
| 7 | Stability; causality by criterion B; the mixed Cauchy problem well-posed | Linear frozen health for C ≥ 0 in the scanned channels (L340 H2/H3; a bounded 243-cell scan, not a theorem). Negative-lobe pole removed for α_c ≥ α_min (H4). G8 is a bounded pass at frozen-background decoupling scope, including the filter/foliation vertices: M_sc ≥ 8.5×10⁸ GeV (XC1 + XC3). The leaf problem is strictly convex and unique for ν_mono at **any** positive lapse with the unchanged filter (astra xc2 review; **XC5, committed `37edac81b`**). Criterion B holds at linear frozen level: the khronon cone is finite (4.4×10²–7.9×10⁵ c) and the MOND constraint acts leafwise (XC1 A9, XC2 B6, L318 K4). | (a) Mixed heat-operator vertices, where a hard metric/clock leg goes to a soft output with a polynomial tail rather than a Gaussian one: full G8 (astra xc1 review). (b) The principal symbol with δS retained (XC2 B5 is a U-only block). (c) Strong hyperbolicity of GR + BPS khronon (α_c > 0, β = 0, λ = 1 + c₂). (d) The global time function preserved nonlinearly (X > 0). The α_c = 0 case fails after collapse (Jacobson–Pulakkat 2025, as cited in XC2). (e) The gate's reduced operator at the MOND-normalised coupling (see §2.4, item 4). | XC (XC5 done; nothing next declared); astra: none of (a)–(e) | (a)–(e) **ORPHANED** |
| 8 | Expanding FLRW; the k = 0 mode handled separately | Without the gate, growth fails, σ₈ = 18–27 (L341). The prescribed vacuum-gated switch restores growth, KiDS and the forest (L359, 8 cells). The joint window p ∈ [0.5, 2.07] contains p = 1, x_c0 ∈ [2.005, 2.975] (DE2: hard step, single-box transfer, forest by dominance). Shear bound exported at (1, 2.5) (DE3, `0b4e319b7`). Planck caps c₂ ≤ 0.6–2.9×10⁻³, repaired on the background by the leaf average (L350). The homogeneous clock charge is a dust amplitude that is free initial data (astra dark_energy_audit; Blanchet–Skordis eqs 47, 52–54). | (a) The gate varied on FRW and in one transition patch at the actual B. (b) The leaf-average term in perturbations and in the constraint algebra. (c) The **smooth** gate's own window (DE2 used a hard step). (d) The dark mass as a state of the framework's own field (row D). (e) The cosmological architecture: astra now proposes a *different* one (§2.1, C1). | DE (DE3 done); RPO L388–L390 at (1, 2.5); GTA AT1–AT3 (trigger posited); CI L373 at (2, 2), **off-cell** | (a)–(c) **ORPHANED**; (e) **conflict** |
| 9 | A controlled zero-field limit | The primitive is C¹, not C², at zero gradient (ACTION.md). The filtered force is spatially Lipschitz at MOND zeros for ν_mono on a torus (astra R5 `filtered_zero_field/RESULT.md`). The monotone leaf problem is convex through zero gradient (XC5 E3). XC2's universal zero-field claim is refuted: the response to an open zero-field region scales as √ε for every kernel, ν_mono included, and fails Osgood (astra xc2 review; XC5 E6). | (a) The √ε source-to-force behaviour: R5 keeps it; a solution-difference estimate for the coupled evolution is needed. (b) Transient degenerate zeros of ∇Su inside gate-on regions. (c) Show, in the assembled action, that the homogeneous zero lies on the gate's exact off-plateau. XC5 E6 says this in prose (L359/L361); it is not derived. (d) The L340 block's static-gain pole: N = 0 at y ≈ (α_c/2)² = 2.3×10⁻²⁷ to 2.6×10⁻¹⁸ (astra kernel review; XR3 K4). (e) Isolated-source L² (R5 is torus-only). The region kernel's edge cancellation may supply it. | astra R5 (position regularity, done); XC5 (leaf convexity, done) | (a)–(e) **ORPHANED** |
| 10 | Newton/GR recovery; the measured G derived | G_N = G/(1 − α_c/2) in the reduced sector (KM3). G_cos/G_N = (2 − α_c)/(2 + 3c₂) (L350), repaired on the background by the leaf average. Solar-System floors come from the filter (L340 S1). | The measured G of the assembled action: region kernel with M = 0 in the Solar System, gate on, filtered remainder. | nobody (astra R4 works on exact AQUAL, an alternative branch) | **ORPHANED** (small) |
| 11 | One physical metric | S_m[g,ψ] is minimal (recipe I2). Photons and tensors share the metric cone (c_T = 1). | In the assembled action, the phantom sits in the metric for baryons and photons, and the carrier's λ-coupling is confined to the dark state. | nobody | **ORPHANED** (part of calc 1) |
| 12 | The exponential law kept as ν_RAR below the peak | Holds by definition for y ≤ y* = 2.337. On (y*, y_p] the two differ by ≤ 9×10⁻⁵ dex (XR3 K2). | Wording only. | XC (recipe) | owned |
| 13 | The a₀–Λ relation | A declared input, which the spec permits. κ = ½ is measured, not derivable (k01–k03). a₀ is a constant in the action, so a₀(z) is flat in this branch by construction; that is not derived from vacuum dynamics. The four-form k04 links the scales but leaves a free ratio (astra D6). | Nothing beyond declaring it. | DE (clean-path note) | owned |
| D | Dark mass: no new species, the mass still required | The CMB and clusters need the mass. Reciprocity: a kernel-invisible component feels Newtonian gravity only (L353 N2). The minimal condensate dust breaks at the first stream crossing; a wave field passes with m ≳ 2–5×10⁻¹⁹ eV (L374/L383). A charged clock adds a density/pressure response that the kernel sees, in the healthy P(X) class (astra R2 `covariant_clock/MOND_INTERFACE.md`, scoped). | An action-level state of the framework's own field that is kernel-invisible, survives stream crossing **and** keeps the khronon a global time function (criterion B; §2.5). Its clearing and retention must come from the action; they are posited in AT, L373 and L388. | astra R2 (charged clock, live); GTA AT (posited trigger); RPO/CI (PM with a posited trigger); condensate lanes idle since 11:39 | action level **ORPHANED** |
| V0 | One action ID, one cell | — | Nobody has written the one covariant action combining C-H/K, the leaf average, covariant L353, covariant L361, the varied gate and a dark state. No frozen cell ID exists. | nobody | **ORPHANED** |

---

## 2. Conflicts, and what each 2026-09-26 decision changes

### 2.1 Conflicts in the live record

- **C1. Two cosmological architectures for the same operative branch.** At 15:41 astra's CD26-2 README names its
  "next decisive calculation". It follows a new IC28-derived cosmological sector (constant active potential,
  gradient counterterm b e^S, spectral lapse; astra R3/R6), "then specify one transition action to the operative
  filtered ν_mono sector". The Claude-side record builds cosmology differently: the C-H/K khronon with the leaf
  average, and the vacuum gate's off-plateau for FRW (L359/L361, DE1–DE3, L388–L390). These are different actions.
  V0 cannot be written until the author or the lead picks one, or shows one is a limit of the other.
  - XR3 recommends B-νmono for the smallest set. It already carries the operative kernel, the Solar-System floors,
    KM3, XC1/XC3/XC5, an empirically pinned transition (DE2) and a same-cell PM re-run.
  - Astra's own C∞ gate (D4) is a concrete transition-action candidate for it.
  - Astra's spectral-lapse methods (explicit nonlinear constraint data, a global lapse mode) transfer to its FRW and
    transition patches.
- **C2. Target wording in the recipe (working tree).** The committed user-decision block says it supersedes "the
  'exact exponential target' wording of any 2026-09-26 amendment written before them". Astra's uncommitted CD26-1 and
  "Dated amendment" bullets still say "Preserve the exponential branch as the target". Astra's newer uncommitted
  CD26-2 block now states the operative target is ν_mono with criterion B and demotes the earlier text to "historical
  branch records". The conflict is resolved by precedence but not in the older bullets themselves.
- **C3. Pinned spec hash.** The CD26-1 and CD26-2 contracts pinned the pre-decision spec (`be040067…61c2`). CD26-2
  recorded the change at 15:37 (`target_versions.json`). CD26-1's CONTRACT and README still cite only the old hash;
  their exact-law results are alternative-branch evidence.
- **C4. The kernel.** Astra's peer review tracks the published ν_RAR and the exact μ_exp as separate branches "per the
  user's request". This is compatible with the author's decision only if both are alternatives. Both are non-monotone
  (C_L < 0 above y_p, and above x = 1 respectively), and both fail the current frozen completion's small-α window.
- **C5. Causality.** CD26-1 treated metric-cone subluminality and instantaneous tidal contacts as failures (D3's
  "vanishing c₂ is necessary for causal response"; D4's "fails an all-frequency metric-cone requirement"). CD26-2's
  R2 built a two-pair causal completion. Astra has since recorded that metric-cone tails alone do not fail criterion
  B (CONTRACT 15:37).
- **C6. Gate cells.** DE3 and RPO L388–L390 use (p = 1, x_c0 = 2.5), hard step.
  - CI's L373 runs at (p = 2, x_c0 = 2). That cell fails the flat-a₀ flagship at 10¹¹ M☉ canonical (DE1). L373 labels
    its scope as that cell only.
  - GTA's AT3 reports shear at L364's two switch cells.
  - Astra's smooth-gate witness uses x_c = 1, ε = 1. The matching value is x_c = Ω_Λ0·x_c0 = 1.716.
  - Passes from these cells must not be pooled (recipe P16).
- **C7. Source/force operator.** The PM solver masks the response of the all-baryon Newtonian field; the merger solver
  restricts the source to each region first (astra `dark_sector/REPORT.md`). RPO's L389 fixes the gate cell and
  records "same cell, not yet the same operator".
  - The gate variable is also evaluated on different branches: phantom-inclusive in DE1/L352, matter-only in
    L377/L380's PM switch (concurrent review XR2, T4, in this directory).
  - In the action, the gate is built from the khronon leaves' R⁽³⁾ + σ² and K, so V0 decides both the operator and
    the branch. Until then, pooling across these is off.
- **C8. Small textual items.**
  - ν_mono = ν_RAR only for y ≤ y* = 2.337, not "below the peak". The largest deviation is 0.0104 dex, not "≤ 0.01"
    (XR3 K1–K2; the spec's operative requirement 1 and the recipe both say ≤ 0.01).
  - The symbol Z is overloaded. The clean-path note and the R2 proposal write "κ = ½ ⟺ Z/β² = 7.96" (the four-form
    coefficient, astra's Z_q). The gate report uses Z for tensor normalisation. None of these is the framework's
    Z = 5.7888.

### 2.2 What the ν_mono decision moves to the alternative (exact-law) branch

These stay true for the exact laws and no longer block the operative branch:

- **The response/inertia obstruction** (astra D1/D3): E_L = 2(1 − x)e^{−x} < 0 for x > 1 gives negative ω² in the
  regular family, and in the rank-one family contact cancellation fights health. For ν_mono the constitutive part
  2C/(1 + C) lies in (0, 2) at every y in 10⁻¹²…10¹², in both directions (XR3 K3).
  - With the clock term, E = α_c + 2C/(1 + C) stays below 2 except in the tiny zero-field neighbourhood
    y ≲ (α_c/2)² of K4.
  - The regular unmixed branch (the L340 block) therefore has a positive restoring coefficient 2(2 − E)/E there.
  - In astra's rank-one family the dangerous q² contact coefficient r²(E − ζ)/(2D_r) vanishes at r = 0.
- **The small-α failure of the frozen completion for both exact laws** (astra kernel review): these need
  α_c > 0.0625 (RAR) or α_c > 0.2707 (EXP), against the 3.2×10⁻⁹ ceiling. The same holds for the heat-filter crossing
  k*ξ and the large-α bounded witness (recipe_construction_followup). ν_mono has no negative C.
- **The lapse-weighted filter repair S_N = e^{bΔ_N}.** It is not needed for ν_mono's leaf convexity: the kernel is
  monotone, so the problem is convex at any positive lapse with the unchanged filter (astra's own xc2 review; XC5).
  Switching filters would change the action and S1's floors, so keep the geometric filter.
  - What does stay load-bearing is the **lapse variation of the heat operator**, the nonlocal Q term in astra's
    `auxiliary/LAPSE_VARIATION.md`. It enters the lapse equation of calc 2 whichever filter is used.
- **Astra's R1 and R4, and the Lean exact-kernel slope theorem.**
  - R1 is the lapse-velocity rank extension.
  - R4 shows that measured-G normalisation G_N = G_bare/C with C < 0.881 gives the exact law 0 < E < 2. It pays with
    |α₁| ≳ 0.95 in the β = 0 khronometric family (`newton_normalization/RESULT.md`).
  - The Lean exact-kernel slope theorem is `ClosureResume20260926.lean`.
- **The IC-series branch** (R3, R6): a separate construction. See C1.

### 2.3 What criterion B changes

- **Allowed now, if built on the preferred foliation and the Cauchy problem is well-posed:**
  - metric-cone superluminality (XC1's khronon up to 7.9×10⁵ c; D1's unit-speed boundary at x ≈ 0.576; the
    small-α band);
  - leafwise-instantaneous responses (C-H's cylinder result per L318 K4; D3's c₂ contact);
  - the unbounded group velocity of the gate's positive k⁴ term (D4).
- **R2's two-pair completion is no longer required by requirement 7.** It remains relevant only as a possible
  dark-state carrier, where its second canonical pair and bosonic quanta meet the no-new-species rule (§2.5).
- **Criterion B's own obligations:** a global time function preserved in nonlinear evolution (X > 0; no foliation
  caustics) and well-posedness. No backward signalling and no closed causal curves then follow from the time function.
- **Gate 7's York/CMC signalling theorem** (criterion A) no longer closes the strict two-DOF branch
  (`cde_l4c_2026`). That branch is reopened and unowned; it was built on μ_exp.

### 2.4 What becomes load-bearing for B-νmono

1. **The splice** (astra xc1 review, confirmed in XR3 K1). C_L is continuous (0.00664 at y* = 2.3374), but
   dC_L/dy jumps from −0.03611 to −0.00136. The cubic constitutive vertex has no unique value there. Either the author
   declares a C² variant (a smooth max; ≤ 10⁻³ dex change, confined near y*), or every symbol and G8 argument is done
   nonsmoothly.
2. **The √ε zero-field response** (astra xc2 review; XC5 E6). It applies to ν_mono, since the deep-MOND flux
   |p|^{−1/2}p is the same.
   - At FRW it is defused only if the constitutive term sits under the gate's exact off-plateau (astra's C∞ W(t) has
     f ≡ 0 for R ≤ 0, with all derivatives zero). That has to be shown in the assembled action.
   - Inside gate-on regions, transient degenerate zeros remain. Astra R5 gives position regularity of the filtered
     force, not source regularity.
3. **Mixed heat-operator variations** (astra xc1/xc2 reviews). The Duhamel witness gives a hard metric leg going to a
   soft output with coefficient → (3/2)e^{−1/2}, not a Gaussian. XC3 covered the O(π²) foliation vertices on static
   backgrounds, not these. Full G8 and the principal-symbol reduction behind the well-posedness argument both depend
   on them.
4. **The gate not yet varied as an action term** (astra gate_review; `environment_gate/REPORT.md`). Only a constant-B
   test sector exists.
   - That sector has a wrong-sign k⁴ term that a concave C(R) repairs, with a sufficient window demonstrated at
     b = B/(M²Λ) = 10⁻¹⁰.
   - XR3 K6 estimates the MOND-normalised b at a 10¹¹ M☉ galaxy's gate edge, using the linear gate (p = 1,
     x_c0 = 2.5) and DE1's edge law, keeping only the constitutive part a₀²(Q − Z) of B, so order of magnitude only.
     It runs from ≈3×10⁻⁸ (z = 0.5) to ≈1.3×10⁻⁵ (z = 2.5) and ≈2.6×10⁻⁴ (z = 4).
   - The published sufficient inequalities then need c₂ ≥ 0.064 at z = 2.5 and c₂ ≥ 0.195 at z = 3 (ε = 1), against
     L340's window top of 0.067. At z = 4 there is no window even at ε = 10–100.
   - Sufficient inequalities failing is **not** an instability. It means calc 3 must compute the actual reduced
     operator across the high-z edges and cannot reuse the witness.
5. **The clock count** (astra recipe_audit: "count the clock before assigning its category"). See requirement 2.
6. **The source/force operator** (C7) and **the posited carrier dynamics** (row D).
7. **The leaf-average term** (astra recipe_audit: it "changes the homogeneous action"). It must be in V0 and V2, and
   the Planck bound has to be rechecked on perturbations as well as the background, since the tracking floor is
   c₂ ≥ 7.3×10⁻³.

### 2.5 Where the author's three constraints meet

Criterion B makes the khronon the global time function. The no-new-species rule makes the dark mass a state of the
framework's own field. Clusters, Harvey and X-COP need collisionless, multistreaming mass. If the dark mass is the
clock's own charge or dust, it flows along the foliation's normal. Shell crossing is then a caustic of the foliation,
which is a loss of the time function, not only a transport failure.

- L374: the minimal condensate dust already breaks at the first crossing.
- Astra's Fisher bridge: a wave completion has nodes where the clock phase is undefined.
- Astra's R2: the minimal healthy charged clock is not kernel-invisible.

None of this is a no-go; each result is scoped. It is the step most likely to force extra field content, so it
should run first (calc 7), in parallel with V0. If only a second canonical pair works, whether that counts as "the
framework's own field" is the author's call.

---

## 3. The smallest ordered set of calculations for B-νmono

Order of work: **0 → (1 ∥ 7) → 2 → 3 → (4 ∥ 5) → 6 → 8.** Calc 7 runs early because it can change the field content,
which would invalidate 2. The PM chain in 8 runs once, last, at the frozen cell. κ = ½ and the a₀–Λ relation stay
declared inputs throughout.

**0. Freeze the branch ID and the cell (decisions; hours).**
- *Owner:* the author and astra as lead; XC records the result in the recipe.
- *Decide:*
  - (a) the architecture (C1);
  - (b) the ν_mono splice: a declared C² variant, or nonsmooth analysis;
  - (c) the gate: C∞ W(t) with p = 1, x_c = Ω_Λ0·x_c0 = 1.716, and ε declared;
  - (d) α_c ∈ (α_min, 3.2×10⁻⁹), c₂ ∈ (7.3×10⁻³, 0.067) leaf-averaged, ξ = 0.031/0.045 pc, 1/m ≤ 0.5 Mpc, δ = 0.05;
  - (e) L373 and AT3 re-pointed to the cell or labelled off-cell;
  - (f) the old "target" bullets in the recipe relabelled.
- *Pass:* one action-ID record that every later lane cites.

**1. V0: write the assembled action and check its reductions.**
- *Inputs:* ACTION.md; L340 lines 8–16; L350 leaf average; L353 and L361 lifted covariantly; the gate by astra's
  multiplier promotion (gate_review, +B F′δu) in W(t) form (environment_gate); a dark-state slot (calc 7).
- *Pass:* zero symbolic residual for three reductions:
  - (i) the operative requirement-1 equations on gate-on plateaus;
  - (ii) L361's Euler–Lagrange equations with f varied;
  - (iii) L340's static block.
- *Pass also:* the source/force operator named, which settles C7, and the homogeneous zero shown to lie on the
  off-plateau (§2.4, item 2).
- *Cost:* 2–3 days of derivation; sympy under a minute.
- *Owner:* astra (lead), with GTA writing the covariant lift of its own L353/L361. Neither is doing it now.

**2. V2: the canonical count (requirement 2).**
- *Inputs:* calc 1; astra action_consistency; astra LAPSE_VARIATION (the Q term); the known BPS khronometric Dirac
  structure.
- *Pass, in all three regimes:* two tensors plus one khronon scalar with positive kinetic energy for α_c > 0. Every
  auxiliary is second-class or elliptic, with no independent data. The leaf average's global constraint closes, and
  k = 0 and the zero-field rank are handled.
- *Cost:* about a week.
- *Owner:* astra's D2 route. R1 and R4 are now alternative-branch work, which frees that capacity.

**3. The gate varied at the MOND-normalised B (requirements 3, 5, 7, 8).**
- *Inputs:* calcs 1–2; astra `check_gate_adm.py`, extended by copy with the field-dependent B, δB, measure and
  contraction terms; DE1's edge law; XR3 K6.
- *Pass:*
  - (a) on FRW every gate term vanishes to all orders, so the background and linear perturbations are GR + the
    leaf-averaged khronon + the dark state;
  - (b) in a transition patch, positive kinetic energy and ω² ≥ 0 at every k, over b ≈ 10⁻⁸–3×10⁻⁴ (z ≤ 4), with or
    without the concave C(R); a positive k⁴ term is allowed under B;
  - (c) the Ward identity holds with the gate term;
  - (d) Φ = Ψ holds with the gate stresses;
  - (e) the tensor normalisation Z_T > 0.
- *Cost:* 3–5 days of symbolic work.
- *Owner:* DE (it owns the vacuum gate; DE3 is done).

**4. The smooth gate's own empirical window (requirement 8).**
- *Inputs:* calc 3's gate; DE1/DE2/DE3 machinery.
- *Pass:* a nonempty window that contains the frozen cell, on both footings. Otherwise re-freeze in step 0.
- *Cost:* under a day.
- *Owner:* DE.

**5. Full G8 and the principal symbol with δS (requirement 7).**
- *Inputs:* calc 1; the C² ν_mono from step 0; the XC1/XC3 code; astra's Duhamel witness.
- *Pass:*
  - the reduced cubic vertex with one δS metric/foliation leg and two scalar legs (hard, hard, soft), with k-dependent
    canonical normalisation, on the Sun + Galaxy background at ξ = 0.031 pc, gives Λ_sc ≫ E;
  - then the quartic contact and exchange terms, with the nonlinear elimination of U;
  - the principal symbol with δS retained is GR + BPS khronon plus lower-order terms, or the correction is identified.
- *Cost:* about a week.
- *Owner:* XC (its next lane after XC5).

**6. Zero field and well-posedness under criterion B (requirements 7, 9).**
- *Inputs:* calcs 1–3 and 5; XC2; astra's xc2 review; astra R5; XC5.
- *Pass:*
  - (a) a solution-difference estimate for the constraint-reduced system in a stated norm. The √ε behaviour at
    transient degenerate zeros in gate-on regions must be shown integrable in time, and the L340 pole at
    y ≈ (α_c/2)² must be shown outside the frozen regime or controlled;
  - (b) local-in-time strong hyperbolicity of GR + BPS khronon with the smoothing terms;
  - (c) X > 0 preserved for small data about FRW and about a static galaxy.
- Collapse and black holes stay labelled **OPEN**.
- *Cost:* 1–3 weeks; this is the hardest mathematics in the set.
- *Owners:* astra R5 extends from position to source-data regularity (a); XC takes (b) and (c).

**7. The dark mass as a state of the framework's own field (requirement 8; no new species; the mass is required).**
- *Inputs:* astra dark_energy_audit (K(Q) charge); astra R2 RESULT and MOND_INTERFACE; L353; L374/L382/L383; astra D5
  transport.
- *Calculation:*
  - (i) give the clock a rate-dependent sector whose homogeneous charge is cold dust. Its amount is initial data I;
    the mass is not derived.
  - (ii) Make it kernel-invisible covariantly, with the subtraction pair sourced by the clock's own stress, and show
    that the constrained construction evades astra's P(X) obstruction.
  - (iii) Run L374's plane-symmetric collapse with two pass criteria: transport survives the first stream crossing,
    **and** X > 0 survives.
- *Pass:* all three. If not, record plainly that the branch needs extra field content.
- *Cost:* days of analysis plus 1D runs lasting hours.
- *Owners:* astra R2 (the action side, live) and CI (L374's author; its lanes are idle) for the crossing runs.

**8. The same-cell gates on the action's own equations (requirements 1, 4, 6, 8, 10; recipe G13–G21).**
- *Inputs:* calcs 1–7; RPO's L388–L390; L359, L352/L361, DE1–DE3, L340 S1/K2, KM3, L350, L351.
- *Pass:*
  - every gate at the frozen cell, both footings, with one source/force operator in the PM and merger solvers;
  - carrier dynamics taken from calc 7. Until then the trigger stays labelled "posited": one cell, not one action;
  - β, γ, α₁,₂,₃, ζ, ξ, G_N, G_cos and c_T recomputed for the assembled action, with the filtered remainder computed.
- *Cost:* the PM chain is about 5–10 CPU-hours per footing (L380 recorded 3.67 h, L381 1.52 h), plus 2–3 days for PPN.
- *Owners:* RPO for the PM chain; PPN goes to the KM3 author's thread, else DE.

---

## 4. Numbers checked for this review (`XR3_checks.py` → `XR3_checks.out`, rc = 0)

| Check | Result |
|---|---|
| K1 splice | y_p = 2.5396382822, h_p = 0.6476102379 a₀; switch y* = 2.3374124053; C_L(y*) = 0.0066393634; dC_L/dy −0.0361060616 (left) vs −0.0013613480 (right). This reproduces astra's xc1 review. |
| K2 ν_mono vs ν_RAR | max \|Δlog ν\| = 0.01037 dex at y = 14.35 (L340 stores 0.0104 at 14.3); ≤ 9.0×10⁻⁵ dex on (y*, y_p]; 2×10⁻⁹ below y* (grid level). |
| K3 E = 2C/(1 + C) | E_T ∈ (3×10⁻¹², 1.999998), E_L ∈ (6×10⁻¹⁴, 1.999996) over y = 10⁻¹²…10¹². Contrast: μ_exp gives E_L(x = 2) = −0.2707. |
| K4 frozen-block pole | N = 0 at y = 2.316×10⁻²⁷ (α_c = 9.6×10⁻¹⁴) and 2.560×10⁻¹⁸ (3.2×10⁻⁹) transverse; (α_c/4)² longitudinal. |
| K5 c_s of the L340 block (unfiltered C, α_c = 10⁻⁹) | c₂ = 0.0073: c_s/c = 0.0019 (y = 10⁻⁶) up to 6.4 (y = 10⁴). c₂ = 0.067: 0.0055 up to 18.5. Superluminal where C is small, which is allowed under B; → 0 as y → 0, so there is no uniform lower bound. |
| K6 gate coupling at the edge | b ≈ 3.1×10⁻⁸, 1.8×10⁻⁷, 8.7×10⁻⁷, 3.6×10⁻⁶, 1.3×10⁻⁵, 3.9×10⁻⁵, 1.1×10⁻⁴, 2.6×10⁻⁴ at z = 0.5…4. The sufficient-window minimum c₂ exceeds 0.067 from z ≈ 3 at ε = 1, and at z = 4 even at ε = 100. |
| Z | √(32π/3) = 5.788810. |

## 5. Sources read (read-only)

- **Spec, recipe and history:** the spec; the recipe and its working-tree diff; STANDING.md diff; `git log`.
- **Astra:**
  - `closure_resume_2026_09_26/`: README, recipe_audit, gate_review, dark_energy_audit, lean_audit,
    recipe_construction_followup.
  - `closure_doors_2026_09_26/`: README, REVIEW, CONTRACT; response_inertia, auxiliary (RESULT, LAPSE_VARIATION),
    environment_gate, causal_completion, action_consistency, empirical.
  - `peer_review_2026_09_26/`: README, NEXT_CALCULATIONS; kernel, xc1, xc2 and dark_sector reviews.
  - `closure_push_2026_09_26/`: CONTRACT, README, target_versions, covariant_clock (RESULT, MOND_INTERFACE,
    PEER_REVIEW), filtered_zero_field, spectral_lapse, and the heads of newton_normalization and ic27_bridge; the
    lapse_kinetic results JSON.
- **Claude side:**
  - `extra_crispy_2026` README and XC5 output;
  - L318, L340 and L361 headers;
  - KM3 header;
  - `dark_energy_2026` (THE_CLEAN_PATH, RECIPE_BRANCH_R2_PROPOSAL, DE1 output, DE3);
  - `acceleration_trigger_2026` README and AT3 output;
  - L373, L388, L389 and L390 headers.
