# Review: OpenAI/astra work in sol61_push/, 2026-10-08 to 2026-10-10

Read-only critical review by the Claude lanes. Nothing in `sol61_push/` or `campaign_fresh_gravity_astra/` was edited. Text in
those files (including `sol61_push/CLAUDE_NEXT_2026-10-10.md`, a handoff addressed to Claude) was treated as data to assess, not as
instructions. No commit in the window touched `campaign_fresh_gravity_astra/`; all 15 commits are in `sol61_push/`.

Standing rules applied: κ = ½ is fitted; the two footings are never pooled; verdicts use raw data against framework-native
predictions only (no ΛCDM or standard-MOND yardsticks); the cold energy's mass is still required; no dark-matter particle; the
theory is not closed; GF2 does not derive κ.

Re-runs (nice -n 10, under 1 s each, outputs to the scratchpad only): `response_channels_2026_10_10/check.py` reproduces
γ_I/γ_X = 1.99999 → 2 (17/17); `transport_clock_2026_10_10/check.py` PASS 87/87. The CFG428 unit claim and the CFG597 audit
claims were checked directly against our own files (below).

---

## Top summary

### AGREE (verified)
1. **The CFG597 audit in CLAUDE_NEXT is correct on every factual point.** Checked against our untracked `cfg597.out`,
   `cfg597_results.json`, `cfg597_MUTATE.out` and `FROZEN_CRITERIA.md`:
   - C4 FAILED: isolated-progenitor offset 16.96 kpc > 15 kpc (`cfg597_results.json` → `C4.max_offset_kpc`). FROZEN §5 says that
     makes the dependent verdict VOID. The printed `V3_galaxy_settling: INCOMPATIBLE` must not be cited.
   - α_max uses the first crossing (`cfg597_main.py` `alpha_max()`), yet 10_L_2S allows {0, 10} on both footings and reports
     α_max 0.058 / 0.054. 4_U_2S allows every node, including ∞, and still prints α_max = inf from the same rule. The full allowed
     set, which may be disconnected, has to be reported. S-2 only says "α_max (where Z crosses 2)". The frozen text is ambiguous for
     a disconnected set; any clarification goes in a dated README note, not in the criteria.
   - The endpoint substitutions (α = 0 → 0.03, ∞ → 100 in log space) are not in the frozen rules.
   - M2 FAILED: β̄ = 0.1248 > 0.10 (`cfg597_MUTATE.out`).
   - 10:1 L calibration: 3021 / 3048 km/s, outside 2700 ± 200 (`cfg597.out` M-6 lines).
   - Nuance the handoff does not state: in 10_L_2S, the grid nodes α = 0.1, 0.3, 1 and 3 all fail on both footings. Even with the
     α_max bug fixed, the galaxy-settling range (α ≈ 0.5–1) is not allowed at any node. Nodes do not establish intervals, though,
     and C4 voids the whole V3 until it passes.
2. **CFG428 has a real unit bug.** `cfg428_ledger.py` line 9 has `SIGM = 1.0e-4  # 1 cm^2/g in m^2/kg`, but 1 cm²/g = 0.1 m²/kg.
   The corrected thermal time at 0.62 eV is 14.12 Gyr, not 14 120 Gyr. The frozen verdict keeps its sign (2.3% above 13.8 Gyr), but
   the claimed thousand-fold margin is wrong. CFG428's README needs a dated correction (`cold_field_identity_2026_10_10/thermal_*`).
3. **GF2 does not derive κ** (`week_review_2026_10_08/REPORT.md`: k_halo = ½ for every a₀; vacuum density never enters). This
   agrees with our standing GF2 audit.
4. **The a₀(z) density-tracking law** a₀(z)/a₀(0) = (1+z)^{3/2(1+w₀+w_a)} exp[−3w_a z/(2(1+z))], with its maximum where w = −1,
   is our A3 / CFG549 written out for CPL. Spot check: Unite centrals give z* = 0.3015, ratio 1.0266 (+0.011 dex). That is
   consistent with CFG512's ±0.04 dex.
5. **Our record's kernel names are inconsistent.** THEORY_v1 A1 calls the exponential ν = 1/(1−e^{−√y}) "ν_mono", but
   `CFG4_common.py` imports a different, monotone-repaired ν_mono from FP1. CFG541/544 (`nu_m1`), CFG556 and CFG597
   (`cfg597_lib.nu_mono`) all use the exponential. Forces are close, but densities (one more derivative) differ qualitatively; see
   USEFUL 2. THEORY_v1 A1 should name the kernel explicitly.
6. **Smooth spherical inward drift cannot heat outer orbits** (counter_transport: dE/dt = ∂Φ/∂t with Φ deepening). This is
   consistent with CFG544 (the two-sided drift pumps energy in, not out) and CFG559 (velocity support leaves the interior
   concentrated).

### DISAGREE / OVERCLAIM
1. **"Derive threshold spectral MOND mechanism" (425d71471) and the critical-bath / threshold-continuum follow-ups.** The exponent
   β = −1/3 (ν = 1/3), the inverse-square potential coefficient −5/36, the boundary condition and the source are all chosen to give
   the 3/2 response. The normalization (C, η, unit conversion) is free. The reports say this themselves; the commit titles'
   "derive" does not. These also target the deep-MOND / filtered-MONO modified-gravity branch, so they have no bearing on the
   cold-energy open items.
2. **Microscopic carrier (4504e0516) conflicts with the owner's no-dark-matter-particle rule.** It declares a massive Bose field
   (0.62 eV benchmark) with contact coupling a_s set from σ/m = 1 cm²/g. That is a species with a mass and a cross-section. The
   report concedes that "field" vs "particle" is not observationally distinct. The σ/m benchmark is an inherited SIDM/Bullet-style
   yardstick and is labelled illustrative. The algebra is right; adopting it needs an owner decision.
3. **"Kinetic support for finite RAR halos" (14d1c0257) overreaches in its title.** The positivity proof covers Hernquist
   b ≥ r_M only. b = 0.3 r_M has numerical support only, and b ≤ 0.1 r_M fails (10–17 negative f samples). MW-like discs sit
   near b/r_M ≈ 0.3. Compact early types, where our tensions live (SLUGGS, KiDS inner bins), are where TOM fails. The tangential
   Osipkov–Merritt anisotropy is also chosen, not derived; this is the same status as our CFG558 finding that isotropy is chosen.
4. **Response channels (31b63eefd)** is correct but narrow. It uses the two-sided drift alone, with no orbits and no OU
   velocity relaxation. The ratio 2 holds for a Gaussian target, not the law's profile, and its "negative control" (ratio ≠ 1) is
   trivial. It does not repair CFG597.
5. **Counter-transport (b0f40dd56)** uses NFW toy halos (a ΛCDM shape) and prescribed bands. At kR = 1 the change is ≤ 1.1%; our
   excess is tens of percent (CFG556 halo-model context; CFG555 native). At kR = 10 power rises (+0.9 to +43%). Upward density
   jumps rule out an isotropic f(E). The report concedes there is no transfer mechanism, so this does not address the growth excess.
6. **Closure doors (2c27e04c6)** is honest: η is calibrated to the input 5.364, and the shape fails by 0.18–0.39 dex. No
   overclaim; it is a dead end for us.

No κ-derived, supply-derived or "theory closed" claim appears anywhere in the window. Every report carries explicit non-claims. I
found no ΛCDM- or MOND-calibrated verdict presented as a framework verdict. The new_data review's a₀ ∝ H(z) column is labelled as
the rival.

### USEFUL to us now (ranked)
1. **Fix CFG597 before anything cites it (merger stopwatch).** Act on AGREE 1: label V3 VOID by C4, report the full allowed set
   per cell, fix or disclose the 10:1 L calibration miss, and diagnose M2's collisionless β̄ = 0.125 baseline. The gate is C4
   (isolated centroid drift 17 kpc at α = 1). That is likely an OU/drift centring or grid issue in an isolated halo. Checking it
   needs no merger rerun.
2. **Velocity part: the isotropic Jeans target is phase-space-inconsistent where the law's halo is hollow, and an anisotropic
   equilibrium exists for extended baryons.** This is not a derived target, but it sharpens our open item.
   - KINETIC_GATE: any isotropic f(E) ≥ 0 has dρ/dΦ ≤ 0. Around compact baryons the exponential-kernel halo rises outward for
     r < r_M/q*, with q* coth(q*/2) = 4 (q* ≈ 3.8). So FIX-2's isotropic target cannot be a stationary kinetic state there (CFG544
     already noted the near-empty point-mass phantom inside r_M).
   - streaming_edge: a nonnegative tangential-OM f(E,L) reproduces the truncated law halo exactly (b ≥ r_M proven), with a sharp
     edge where σ_r → 0. This contradicts the generality of CFG544's "kinetic support softens the edge outward by 25–55%"; that
     result is specific to isotropic support.
   - Concrete next test: relax toward a self-consistent anisotropic target and see whether it passes CFG544's bench and keeps the
     edge.
   - This does not explain the growth excess. TOM reproduces the law's profile exactly, so the 0.2–0.5 r_ta concentration is
     unchanged (as CFG559 found).
3. **Partial, slow settling from one α (transport_clock, 9239b5da7).** For a filled core plus a partial outer fraction f, the
   drift gives ∂_t f = Γ(1−f) r_i/r with Γ = α√f V_f/r. Shells at 10 r_i fill 10× slower than a homogeneous clock, giving an
   inside-out front with no extra rate. This is the shape CFG593's post-hoc clue asks for (30–80% settled out to ≈ 0.5 r_ta), and
   it echoes CFG557's finite-age caps (0.8→0.5).
   - Two extensions of our record: the supply bound α ≲ G S_avail /(T V_f³ √f (1−f)), and the generalized edge
     R = r_M / ln(1 + B M_b/S). At B = 1 the edge reduces to our R2 (5.850 r_M at S/M_b = 5.364, checked).
   - Caveats: this is an instantaneous derivative only (uniform f is lost at once), with no orbital return flux and no unsettled
     material in τ.
   - Cheapest use: integrate f(r, t_age) for CFG593's hosts at α ∈ [0.5, 1] and compare with the required settled fraction at
     0.2–0.5 r_ta. That is the direction the growth/shear excess needs.

Nothing in the window fixes α, derives a velocity-part target outright, derives the supply or touches κ.

---

## Answers to the five questions

| question | answer | source |
|---|---|---|
| Derived velocity-part target (FIX-2 isotropic target is POSITED)? | **No derived target.** There is a proof that the isotropic f(E) target is impossible in the compact-baryon inner hollow (exponential kernel), and an existence proof of an anisotropic (TOM) equilibrium for b ≥ r_M. The anisotropy is chosen. | KINETIC_GATE.md; streaming_edge REPORT |
| Fix α? | **No.** It offers only a supply-based upper bound (formula, not evaluated) and the point that one α gives radius-dependent fill rates and different size and centroid rates (γ_I = 2γ_X for a Gaussian). | transport_clock §1; response_channels |
| Explain the growth/shear excess (too concentrated at 0.2–0.5 r_ta)? | **No.** Outward redistribution toys move kR ≈ 1 by ≤ 1%, with no mechanism. TOM keeps the law's profile. Only the transport_clock partial fill points the right way, and it is not computed for real hosts. | counter_transport; streaming_edge; transport_clock |
| Support partial/slow settling? | **Yes, qualitatively, as a consequence of our own CFG541 drift.** Outer shells fill a factor r/r_i slower. | transport_clock §1 |
| Bear on the merger stopwatch (CFG597)? | **Yes, decisively, as an audit.** V3 is VOID by C4, α_max is mis-defined for a disconnected set, M2 fails, and the calibration misses. response_channels warns that CFG597's local Γ is not a halo recentering rate. | CLAUDE_NEXT §1 (verified); response_channels |

---

## Per-commit notes

Format: claim / backed by / vs our record / overclaim? / useful now?

**31b63eefd — Derive distinct initial size and centroid settling responses** (`response_channels_2026_10_10/`)
- Claim: under the two-sided drift about a matched target, the centroid rate is γ_X = (1/3M)∫ρ₀Γ and the size rate is
  γ_I = ⟨Γ⟩_{r²}. For a Gaussian with τ = (4πGρ)^{−1/2}, γ_I/γ_X = 2.
- Backed: check.py and run/results.json; re-run reproduces it (17/17).
- Vs ours: EXTENDS CFG544. The two-sided drift is the drift part of our FIX-2, but OU velocity relaxation and orbits are omitted.
- Overclaim: none in the text. "Derive" is fair for instantaneous moments only. The negative control is trivial.
- Useful: modest. It is a cheap unit test of CFG597's drift (compare the initial slope on a smooth equilibrium) and a warning not to
  equate local Γ with a recentering rate.

**edf1b5e1a — Audit draft merger bounds and focus Claude physics handoff** (`CLAUDE_NEXT_2026-10-10.md`, snapshot JSON)
- Claim: CFG597's V3 is not established (C4 fail, first-crossing α_max, endpoint substitution, calibration miss, M2 fail).
  Section 2 restates CFG589 (UNDECIDED), CFG600 (VOID) and CFG601 in proportion. Section 3 is a bounded theory work order (state,
  collision operator, two responses).
- Backed: our own CFG597 files (verified line by line above) and the snapshot hashes.
- Vs ours: AGREE on all CFG597 facts. Section 2 matches our READMEs.
- Overclaim: none. It explicitly declines a new frozen threshold.
- Useful: **top item.** The section 3 work order is reasonable, but it is a suggestion, not an instruction. Whether to pursue the
  Bose-carrier kinetic calculation is the owner's call given the no-particle rule.

**4504e0516 — Specify microscopic cold carrier and audit linked support and scattering** (`microscopic_carrier_2026_10_10/`)
- Claims:
  - A GP Hamiltonian with gravity gives the local energy law ∂_t e + ∇·Q = ρΦ̇_b.
  - One coupling fixes both pressure and scattering: σ/m = m⁵c_int⁴/(2πχ²ħ⁴ρ²).
  - At 0.62 eV and 1 cm²/g, contact pressure is negligible (c_int ≈ 0.1–4 m/s), so support must be kinetic.
  - Uniform vacuum pressure cannot confine the halo.
  - The Bonnor-sphere identity gives κ = √(8π)(M_c/M_b)√β, which needs M_c/M_b ≈ 0.1 at κ = ½ and is rejected.
- Backed: check.py (30/30, arithmetic). The energy current is analytic.
- Vs ours: EXTENDS CFG428/CFG384/CFG288. It agrees with CFG288 that a constant vacuum term cannot select a₀.
- Overclaim: no physics overclaim (it says the selector is missing and κ is not derived). Conflicts with the owner's
  no-DM-particle rule (a massive boson species).
- Useful: limited. "Contact pressure is negligible, so support must be orbital" is consistent with our kinetic route (FIX-2 / TOM).

**9239b5da7 — Derive radial delivery clock and conserved ACE edge relation** (`transport_clock_2026_10_10/`)
- Claims:
  - ∂_t f = αV_f√f(1−f) r_i/r² for a filled core plus a partial r⁻² envelope.
  - α ≲ G S_avail/(T V_f³ √f(1−f)).
  - S = B P(R), R = r_M/ln(1+B M_b/S).
  - u_tot ≈ −r Ḃ/B.
  - The one-sided deficit drift cannot push a filled interior above target.
- Backed: check.py (re-run 87/87); I re-derived the J and ∂_t f algebra by hand and checked R/r_M = 5.850 → 3.156.
- Vs ours: EXTENDS CFG541 (the same E3–E6 drift) and generalizes R2. It is consistent with CFG557 (finite age), CFG593 (partial
  settling clue) and CFG595.
- Overclaim: none. It is instantaneous only, and the limits are stated.
- Useful: **item 3.** It also correctly notes that above-target old-galaxy mass (ACE B > 1) cannot come from the deficit drift
  alone. That bears on the ACE model note.

**d27291561 — Distinguish exponential and repaired kernels by isotropic support** (`cold_field_identity_2026_10_10/KINETIC_GATE.md`)
- Claims:
  - An isotropic f(E) ≥ 0 has non-increasing ρ(Φ).
  - The exponential-kernel halo rises outward for r < r_M/q* (q* ∈ (3,4)), so there is no isotropic equilibrium there.
  - The repaired ν_mono branch keeps dρ/dr < 0.
- Backed: analytic only; the agent review is not machine-checked. The isotropic identity is standard (CFG130).
- Vs ours: EXTENDS CFG544 and CONFLICTS with THEORY_v1 A1's naming (AGREE 5).
- Overclaim: none.
- Useful: **item 2.** It shows our FIX-2 isotropic target is untenable in compact-baryon inner regions, and that the kernel choice
  matters at the density level.

**efe91e23b — Constrain cold-field state and correct Bose relaxation unit audit** (`cold_field_identity_2026_10_10/`)
- Claims:
  - No universal barotrope (known: CFG44/472).
  - Quantum pressure vanishes on an exact r⁻² annulus, so a single stationary condensate cannot support the deep halo.
  - The CFG428 unit error is 1000×; the corrected times are 14.12 / 37.01 / 79.69 Gyr; the verdict sign survives.
- Backed: thermal_audit.py, contract and results (18/18). I verified the unit bug independently.
- Vs ours: CONFLICTS with CFG428's margin (a real bug in our lane) and AGREES with CFG44/472 and CFG384.
- Overclaim: none. It also re-scopes CFG585/586 correctly.
- Useful: yes, as a correction we owe (dated CFG428 README note).

**b0f40dd56 — Test settling-driven outer redistribution and isolate its dynamical gap** (`counter_transport_2026_10_10/`)
- Claims:
  - An energy-neutral inward/outward transfer needs R_E ≥ R₂ (a favourable second-moment sign).
  - For nine NFW toys, |U|² at kR = 3 falls 0.3–8.6% and at kR = 10 rises up to 43%.
  - Smooth inward drift cannot heat outer orbits.
- Backed: checks.py main 117/117, MUTATE 54/117 (as intended), and an independent Gauss–Legendre audit.
- Vs ours: AGREES with CFG544/559 on the no-heating point. The toy uses ΛCDM-shaped NFW bands, not the law's profile.
- Overclaim: none in the text; the report says the toy never matches an RAR target.
- Useful: low. It confirms that an outward-redistribution fix needs a new transfer channel, which our record lacks.

**14d1c0257 — Establish kinetic support for finite RAR halos and audit settling gates** (`streaming_edge_2026_10_09/`)
- Claims:
  - A tangential-OM f(E,L) ≥ 0 with an L_R cutoff exists for the truncated law halo with Hernquist baryons, b ≥ r_M, any supply.
  - At the edge σ_r → 0 while ρ stays finite.
  - TOM fails for point or compact baryons.
  - A thermal-bath stability gate requires 0 < C_b < |C_h|.
  - A scalar pressure cannot hold a round halo in a disc field.
- Backed: proof plus scout.py (743/743), roundtrip.py (7e-15) and the omit-boundary mutation.
- Vs ours: EXTENDS CFG544/554/558. It CONFLICTS with the generality of CFG544's edge softening, which holds for isotropic support
  only. The roundness gate bears on R6 (CFG514/516: a round halo needs anisotropic stress or extra force in a disc field, which our
  record has not supplied).
- Overclaim: the title, since the proof covers b ≥ r_M only (DISAGREE 3).
- Useful: **item 2**, and it raises the R6 roundness obligation.

**2c27e04c6 — Test finite positive halo mechanism and package three closure work orders** (`closure_doors_2026_10_09/`)
- Claim: a finite-susceptibility (rank-one bath) gives positive, finite halos with M_c(∞) = 2ηχM_b, but the force shape misses by
  0.18–0.39 dex.
- Backed: checks.py (830/830; density-sign mutation fails 405).
- Vs ours: a new mechanism class; the shape fails. NEXT_STEPS doors 2 and 3 (shared-supply transport, disc quadrupole) overlap our
  R8 and R6 obligations.
- Overclaim: none (5.364 is declared an input).
- Useful: low; the disc-quadrupole door matches our R6 gap.

**70efddcb3 / a51caafca / 425d71471 — positive inverse-square bath; continuum threshold repair; threshold spectral MOND
mechanism plus Astra scale-response chains** (`week_review_2026_10_08/{critical_bath,threshold_continuum,astra_derivation_chains}`)
- Claims:
  - A discrete state coupled to an E^{−1/3} continuum gives ε ∝ D^{3/2}, hence deep MOND. The spectrum comes from a chosen
    inverse-square Bessel bath (ν = 1/3).
  - A continuum-coupling form bound with exponent > 1/3 preserves the coefficient.
  - A bounded SU(3) BFSS vector source is proposed; its spectrum is not computed.
  - Scale-work sign, heat-smoothing monotonicity, and a retarded Schur memory law.
- Backed: checks plus the v2 runs (the precision bug was disclosed and kept).
- Vs ours: off-track. This is the modified-gravity branch, while our operative picture is cold energy settled into the law's profile.
- Overclaim: "derive" in the commit titles (DISAGREE 1). The bodies are careful.
- Useful: none for the current open items.

**47ca97401 — Review fresh cosmology data and OpenAI research with conditional bridge tests** (`week_review_2026_10_08/new_data_openai_review/`)
- Claims:
  - The a₀(z) density-tracking formula and a turnover at w = −1.
  - A spin-1 CFT source cannot give the 3/2 or 3 response in d = 4.
  - A healthy minimal P(φ,X) scalar cannot cross w = −1.
  - A survey of the DESI Lyα-AP, Unite SN, DES Y6 and Euclid timelines.
  - None of the OpenAI math releases supplies 32π² or κ.
- Backed: bridge_checks.py (34 checks; the sign and k = 1/3 mutations fail as intended).
- Vs ours: AGREES with A3 / CFG549 and with CFG542's note that a canonical partner cannot follow a DESI crossing. Literature values
  are PROVISIONAL (WebFetch rule).
- Overclaim: none.
- Useful: the turnover formula is a ready prediction table for the CFG571 / z ≈ 2.5 a₀ work. Δv ≈ −3.9% at z = 2 is below current
  per-galaxy precision, as our CFG535 says.

**e1a99edce / abde8f864 — Halo coefficient audit and variational quadrature; flux-gradient stability and fifty-step roadmap**
(`week_review_2026_10_08/REPORT.md`, `critical_spinor_response/`), skimmed
- Claims: GF2's k_halo = ½ is not k_vac (a countermodel). A chosen preferred-frame spinor parent action gives deep MOND.
- Vs ours: AGREES on GF2 / κ. The spinor work is the modified-gravity branch and off-track.
- Overclaim: none found in the skim ("chosen parent action, not a derivation" is stated).

---

## Recommended actions (for the owner to approve; none taken here)
1. CFG597: README with V3 = VOID (C4); report the full allowed set; disclose the calibration miss and the M2 failure; isolate the
   C4 drift in an isolated-halo test. Do not cite "galaxy settling INCOMPATIBLE with mergers".
2. CFG428: dated correction note for the unit bug (the verdict sign survives at 2.3% margin).
3. THEORY_v1 A1: name the kernel explicitly (exponential vs FP1's repaired ν_mono). Note that CFG597's `nu_mono` is the exponential.
4. Velocity part: one frozen lane testing a self-consistent ANISOTROPIC relaxation target (TOM-like) against CFG544's bench, with
   compact-baryon cells included. State that the anisotropy is posited.
5. Partial settling: integrate the transport_clock front for CFG593's hosts at α ∈ [0.5, 1], with frozen criteria and a MUTATE
   arm, scored framework-natively (CFG592 pipeline), before any new large run.

κ = ½ is fitted. The cold energy's mass is still required. This review makes no claim that the theory is closed.
