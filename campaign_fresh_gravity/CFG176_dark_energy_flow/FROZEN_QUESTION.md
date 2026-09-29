# CFG176 — the nature of dark energy in the owner's flowing-vacuum picture (frozen before any script, 2026-09-29T20:42Z)

Door 11 (`closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, addenda 1–2): the dark-energy vacuum flows from one direction, is compacted as it pushes through matter, and the extra gravity is a boosted effect of the flow. Readings: 11A inflow (control), 11B′ directional compressible flow (primary), 11C "the top" = the time direction. CFG174 added an accumulation reading (a₀(z) ∝ t(z)). This lane asks only what the picture implies for the dark energy's **stress-energy, equation of state and w(z)**, and whether that is consistent with (i) ΛCDM's background (w = −1) and (ii) the DESI DR2 evolving-dark-energy fits already committed in CFG6. It is not a mechanism for the galaxy law and does not score G1.

**Seen before writing this.** CFG6's README, `CFG6_common.py` and its results JSON (the DESI DR2 CPL central values, the B5 crossing numbers, the posterior-conditioned thawing nodes); CFG174's README, frozen question, script and results (R = 0.293 / 0.354; a₀(2.5) = −0.72 dex under accumulation); CFG43's README (HT: Λ is a global integration constant). The expectations below come from hand algebra done after reading those files, with no probe code run.

## Q1 — can a moving medium stay vacuum-like (w = −1)?

Perfect fluid T^{μν} = (ρ + p) u^μ u^ν + p g^{μν} (signature −+++, c = 1 in the algebra).
- **1a (sympy).** T(u) is the same for every timelike u, and invariant under every boost, **iff ρ + p = 0**; for ρ + p = 0 every timelike vector is an eigenvector of T^μ_ν (no Landau rest frame); the CMB-frame momentum density of a fluid moving at β is T^{0i} = (ρ + p) γ² β, zero for β ≠ 0 iff w = −1.
- **1b (sympy).** The exact energy equation u·∇ρ = −(ρ + p) ∇·u: compaction along the flow is ∝ (1 + w); for T ∝ g, ∇_μT^{μν} = 0 forces ∂ρ = 0 (a Λ-vacuum cannot be compacted anywhere); for constant w, ρ ∝ n^{1+w} (n the volume-compression density).
- **1c (sympy, any stress).** For any T obeying the null energy condition, the momentum density along n satisfies |T^{0n}| ≤ (T^{00} + T^{nn})/2, i.e. g/ρ ≤ (1 + w_∥)/2. A w = −1 medium given an energy flux q ≠ 0 has complex eigenvalues (Hawking–Ellis type IV) and violates the NEC.
- **1d (sympy, FRW).** A homogeneous flow of a w-fluid relative to the CMB frame conserves a⁴(ρ + p)γ²v, so γ²v ∝ a^{3w−1} (≈ a^{−4} near w = −1): a steady flow needs continuous driving, force density (1 − 3w) H g.
- **1e (numbers).** Minimum departure from w = −1 for a flow that carries CFG174's column fraction R (0.293 canonical / 0.354 alt) over t₀: any NEC-respecting medium needs 1 + w_∥ ≥ 2R (≈ 0.59 / 0.71); a perfect fluid moving at β needs CMB-frame 1 + w_eff = R(1/β + β/3) ≥ 4R/3 (≈ 0.39 / 0.47, reached only as β → 1, with anisotropic stress Δ = Rβ) and rest-frame 1 + w = R(1 − β²)/[β(1 − Rβ)]; a slow flow (u ≈ 600 km/s) would need 1 + w ≈ R/β ≫ 2 (violates the dominant energy condition). Table over β.
- **1f (numbers).** In GR the flow's extra pull comes from its active density T^{00} + ΣT^{ii} (= ρ(1 + 3w) at rest): a compacted w ≈ −1 medium **repels**; attraction at rest needs w > −1/3, or relativistic flow above a threshold speed (computed). If the flow is to present the law's phantom density at r_M (ρ_c = a₀/(4√2 πG r_M), P2 point mass, 10⁹–10¹² M☉), the contrast C = ρ_c/ρ_Λ is expected ~10³–10⁵ (∝ M^{−1/2}); a DE-like medium reaches it only by volume compression C^{1/(1+w)}.

**Expected.** Every flow observable (momentum, energy flux, compaction) is ∝ (1 + w): a Λ-vacuum's flow has no physical content. Carrying CFG174's column needs 1 + w_∥ ≳ 0.6, above every committed DESI w₀.

## Q2 — the 11C time-direction reading

- **2a.** If the dark energy is Lorentz-invariant (T = −ρ_Λ g), identifying the flow with the Hubble flow adds nothing (1a): ΛCDM background, w = −1, a₀ flat (CFG6 branch A). Expected: **no new content**.
- **2b (sympy minisuperspace).** If the flow is a dynamical unit timelike vector (Einstein-aether terms c₁…c₄) aligned with the Hubble flow, the Friedmann equation is expected to become (1 + β/2)·3H² = 8πG(ρ_m + ρ_Λ), β = c₁ + 3c₂ + c₃: the flow's energy tracks H² (w_flow = w_total), a rescaled cosmological G, not a w(z) of the dark energy (w_DE = −1 exactly in the shape of H(z)).
- **2c (numbers, scoped).** The "compaction = the flow's expansion rate θ changed by matter" channel at background level: stopping the expansion inside a bound region changes the aether's energy by at most (|β|/2)ρ_crit, so presenting the phantom density at r_M needs |β| ≥ 2CΩ_Λ (expected ≳ 10³). Scoped to the θ² term only; gradient terms around masses (the generalized-aether MOND route, CFG172's lane) are not scored.

## Q3 — the CFG174 accumulation reading

- **3-I (density tie).** a₀ ∝ t with a₀ = κc√(Gρ_DE) means ρ_DE ∝ t², so 1 + w = −2/(3Ht) < 0: phantom at every z. Solved self-consistently (flat, Ω_m = 0.3111, H₀ = 67.66 as CFG174). Expected w₀ ≈ −1.7, w → −2 at high z, outside every committed DESI chain (weighted fraction with w₀ ≤ the model's < 10⁻³).
- **3-II (the vacuum pays).** The deposit grows ∝ t per comoving volume, drawn from a decaying vacuum (ρ̇_V = −Q; not the HT constant of CFG43, so the tie then holds only today): 1 + w_eff = Q/(3Hρ_V) > 0, rising into the past, so CPL wa > 0, opposite in sign to every DESI fit (expected weighted p(wa > 0) < 0.05). f_dep = ρ_dep,0/ρ_V,0 ∈ {0.01, 0.1, 0.3, 1}.
- Both give a₀(2.5)/a₀(0) ≈ t(2.5)/t₀, expected ≈ −0.7 dex, more than 0.3 dex below CFG6's band (all DE branches, 16–84%, expected about −0.14 to +0.2 dex). This is judged against the committed dark-energy fits only; KURVS/KROSS stay with the calculation chat's frozen pipeline (CFG174).

## Q4 — what bounds 1 + w today, and so the flow

Committed CFG6 numbers: DESI DR2 CPL w₀ = −0.752 / −0.838 / −0.667 (1 + w₀ = 0.248 / 0.162 / 0.333), wa = −0.86 / −0.62 / −1.09, crossing w = −1 at z ≈ 0.36–0.44 in 99.8–100% of the posterior; posterior-conditioned healthy thawing w₀,eff −0.88 to −0.95. Computed here from the committed thinned chains (no download): percentiles of 1 + w₀ and wa, p(w₀ < −1), p(wa > 0); the NEC-limited flow momentum today g/ρ_DE ≤ (1 + w₀)/2 (isotropic) or ≤ 3(1 + w₀)/4 (perfect fluid at β → 1, anisotropic); the time-integrated carried column ∫½(1 + w)₊ ρ_DE dt/(ρ_DE,0 t₀) per chain sample, against R. Also the Bianchi-I shear σ/H₀ that the anisotropic stress needed to make up the shortfall would imply (derived; the observational shear bound is not in the record and is not scored). Expected: the carried fraction is ≤ ~0.05, well below R, for every combination; ΛCDM gives exactly 0.

## Checks, controls, rules

- **Load-bearing:** the sympy identities (1a–1d, 2b, the boosted-fluid formulas, Bianchi I); H1 (a w = −1 flow carries zero momentum); H2 (the time-integrated carried column is below R at the 97.5th percentile for every combination and footing, even with the perfect-fluid bound); H3 (3-I phantom, w₀ < −1.3, outside the chains); H4 (accumulation a₀(2.5) > 0.3 dex below CFG6's band); H5 (11C: w_DE = −1, G rescaled only).
- **Reported (not load-bearing):** 3-II's wa sign vs the chains, the compaction factors, the θ-channel |β|, the shear numbers, the flow-speed table.
- **Controls:** CFG174's R and a₀(z) reproduce from its committed JSON; CFG6's B5 crossing fractions reproduce from the chains.
- **MUTATE=1:** the flow's momentum inertia (ρ + p) is replaced by ρ (dust-like, the assumption implicit in CFG174's "swept column"); H1 and H2 must fail (rc = 1). **MUTATE=2:** the accumulation reading is replaced by a steady deposit (a₀ constant); H3 and H4 must fail (rc = 1). Mutation runs write separate outputs.
- A scoped no-go or "no new content" is a valid answer. κ = ½ stays FITTED. Nothing here says the theory is closed.

## Addendum 1 (2026-09-29T20:45Z, received from the coordinator after the body above was drafted and before any script; relays the owner's clarification committed as Addendum 2 of the door-11 gates file)

The owner specified: the flowing medium has **no rest mass and is not a particle**; the extra gravity is an effect of the flow, not of mass it carries. "No mass" is read as no rest mass / no particle content, not as no energy. Added before any script:

**Q5 — which stress-energy each reading needs, and the bound on it.** Four classes of medium without particle content, each with its derived w and its bound:
- **M1** Lorentz-invariant vacuum (Λ): T = −ρg, trace −4ρ, w = −1. It has no flow and no momentum (1a). Bound: this is ΛCDM.
- **M2** massless-quanta or conformal medium (T^μ_μ = 0). Sympy: tracelessness forces the isotropic w_eff = 1/3 in every frame. A null flow (null dust Φkk) has w_∥ = 1, w_⊥ = 0, g = e (NEC-saturating); in FRW it dilutes as a^{−4}, and its active density is +2e. Expected: it cannot be the dark energy (w = 1/3 decelerates). A null flow carrying the column today at c needs Ω_null,0 = RΩ_Λ ≈ 0.2, so it would dominate matter before z ≈ Ω_m/(RΩ_Λ) − 1 ≈ 0.5 (H(z) computed against ΛCDM). Its size relative to the CMB radiation density is reported (T_CMB and N_eff are standard values, not committed; not scored).
- **M3** a flowing field with ρ + p ≠ 0 (quintessence or k-essence gradient flow, a condensate without particles). w > −1, momentum ≤ (1 + w)/2 ρ (NEC). Bound: Q4's DESI numbers.
- **M4** a preferred-frame vacuum whose background stress is still ∝ g (a ghost-condensate or khronon/aether sector plus Λ). The frame is real, but the momentum is zero and w = −1; its content is only a G rescaling (Q2) and perturbations or couplings (PPN, door gate G6; not scored here).

**The readings mapped (expected):** 11A (river/PG) with M1 = GR with Λ; the PG flow is a frame choice, not a medium. 11B′ (momentum plus compaction) needs M2 or M3: M2 fails as dark energy and on H(z), and M3 is bounded by Q4. 11C needs M1 or M4: w = −1, ΛCDM background. CFG174's accumulation needs transport (M2/M3) or a non-HT decaying vacuum (Q3). Q1f's active-density sign applies to every class: M1 repels, M2 attracts (2e), and M3 attracts only for w > −1/3 or relativistic flow. The Addendum-2 note that the compacted vacuum is not the dark mass is respected: Q1f's contrast C is the active density the flow must *present* in GR to mimic the phantom, not deposited stuff.
