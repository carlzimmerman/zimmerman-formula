# WT-09 FROZEN CRITERIA: a stiffness term with gravitational waves at exactly c that keeps the static L* stiffness?

Lane WT-09 of `what_is_time/` (owner, 2026-10-21: "what is time in my framework?", then "figure it out from first principles").
Written 2026-10-21, before any script or number of this lane. κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s²
(CFG4_common), scored separately and never pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is
added. Framework-native quantities only. Not "theory closed". Nothing here says the data favour the framework. Anything that
holds by construction is flagged and gets no verdict weight. Parallel lanes WT-07 (forced time structure) and WT-08 (repaired
parent) are not read, run or edited; where this lane needs a repaired constraint it declares its own variant (P_int, §1).

## 0. Question

CFG938's stiffness −(3γ/4K²) τ_μν τ^μν (τ = traceless projected Hessian of χ, γ = K L*²/2) contains Christoffel², so
δ(c_T²/c²) = +1.5 L*²u²/c⁴ inside a medium with gradient u (WT-02 (e)). Can the stiffness be written so that tensor waves travel
at exactly c on every background while the static stiffness (PAPER49 / CFG938 E[M_c], hence CFG820's L* ≥ 24 pc) is kept?
- (a) Enumerate the candidates (§2).
- (b) δ(c_T²/c²) for linear TT waves, all angles and both polarisations, on Minkowski with ∇χ ≠ 0 and on FRW with ∇χ ≠ 0;
  extra time derivatives (Ostrogradsky).
- (c) The static spherical (and weak-field) stiffness of each; same static equation as CFG938? Does CFG820's bound move?
- (d) EXISTS / APPROXIMATE / NO-GO (§5).

## 1. Inputs (read only) and notation

| input | file | commit |
|---|---|---|
| parent action, S1d (D²χ̄ = −3Hχ̄′ ⇒ C ≡ u·∂χ̄ = −Kρ̄_c c/(3H)), E[M_c], S2d (flat-space identity), K1 | `campaign_fresh_gravity/CFG938_medium_continuum_eft/{DERIVATION.md,cfg938.py}` | 92606e049b |
| WT-02 (e): δ(c_T²/c²) = +1.5 L*²u²/c⁴, wall numbers 4.5e-19 / 7.7e-16 (can.), 6.5e-19 / 1.1e-15 (alt); MU3 intrinsic Laplacian | `what_is_time/WT-02_preferred_time/{README.md,FROZEN_CRITERIA.md}` | 9b3d77382a (criteria b85749d1c) |
| CFG961 (orchestrator check; MU3 = ∂∂χ inside τ) | `campaign_fresh_gravity/CFG961_wt02_verification/FROZEN_CRITERIA.md` | 83b04219e2 |
| FRW tensor coefficient Q_T = 1 − 3γC²/K (c = 1) for ττ; BBN-epoch Q_T < 0 if the medium exists then; α = 1 operator τ + αCσ and its restricted longitudinal kinetic coefficient ½[ρ − C²/K − γα²C²k²/K²] | `sol61_push/cold_covariant_audit_2026_10_20/{RESULT.md,formation/TT_ADVERSARIAL_CHECK.md,formation/REPAIR_SCOPE.md}` | a67f9ed9cf |
| exact one-field action, γ = K L*²/2, L* ≥ 24 pc | `qwen_claude_field_theory/papers_2026/PAPER49_DEPOSIT.md` | 77b39b9fcd |
| L* ≥ 24 pc (screening S(s), ℓ_γ = L*²/(2 r_M)); MUTATE S := 1 gives no allowed L* | `campaign_fresh_gravity/CFG820_stiffness_from_globulars/README.md` | a57fe156ef |
| dSphs want L* ≤ 22 pc (INCONSISTENT, conditional) | `campaign_fresh_gravity/CFG821_stiffness_from_dsph/README.md` | ac7002034a |
| universal screening equation (vector Laplacian of u) | `campaign_fresh_gravity/CFG691_stiffness_window/README.md` | d7c9b9a252 |
| footings | `campaign_fresh_gravity/CFG4_common.py` | 3409d12da0 |
| NGC 3198 (Υ = 0.61, 43 radii) | `real_research/data/sparc_data/NGC3198_rotmod.dat` | 999f94dfee |
| c_T = c results of the record (CFG512 chassis β = 0; DHOST c_T = c ⇒ A1 = 0; fried-chicken case 3a/3c: couplings that touch the TT kinetic or gradient coefficient shift c_T) | `campaign_fresh_gravity/CFG512_gravitational_waves/README.md`; `opus_48_extended_research/reviews/ROUTE1_DHOST_PURE_SLIP_VERDICT_2026-06-17.md`; `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_VERDICT_2026-09-01.md` | 7fc665e187; 60c4885cb3; a18c15cfba |

Cosmology for FRW numbers: CFG938's declared Ω_b = 0.0493, Ω_c/Ω_b = 5.364, H₀ = 67.4 km/s/Mpc, flat, Ω_Λ = 1 − Ω_m, radiation
neglected; z ∈ {0, 10}. The BBN-epoch tensor numbers are quoted from the sol61 audit, not recomputed.

**Notation.** Signature (−+++), K = 4πG, x⁰ = ct, c = 1 in the algebra and restored for numbers. Medium frame u^μ,
h^{μν} = g^{μν} + u^μu^ν, θ = ∇·u, K_μν = h_μ^α h_ν^β ∇_α u_β (symmetric part), σ_μν its traceless part. A_μν ≡ ∇_μ∇_νχ.
C ≡ u^μ∂_μχ (the medium-frame clock rate of χ). D_μD_νχ ≡ h_μ^α h_ν^β A_αβ (projected Hessian, CFG938), D²χ ≡ h^{μν}A_μν.
Ȟ_μν ≡ h_μ^α h_ν^β ∇_α(h_β^γ ∂_γχ) (intrinsic Hessian; for hypersurface-orthogonal u it is the leaf Hessian; its symmetric
part is used), with Ȟ = D D χ + K C. Δ_uχ ≡ h^{μν}Ȟ_μν = D²χ + θC (the intrinsic leaf Laplacian, defined also when u has
vorticity). TL = traceless part w.r.t. h. u = |Dχ| in the static medium; spatial gradient V⃗ = u n̂.

**Parents (constraint used to reduce on shell).**
- **P938:** λ(D²χ − Kmn), exactly as CFG938 writes it.
- **P_int:** λ(Δ_uχ − K(mn − ρ̄_ref)) with ρ̄_ref unperturbed at k ≠ 0 (WT-02's MU3 operator plus a mean subtraction). This is a
  declared variant for this lane only. It is not WT-08's parent, which this lane does not use.

## 2. Candidates (a)

Each is normalised so that its static spherical Newtonian limit equals the record's, wherever that is possible. Normalisations
are fixed now.

| id | term in the action |
|---|---|
| (i) | −(3γ/4K²) τ_μν τ^μν, τ = TL(DDχ) (CFG938; control) |
| (ii) | −(γ/2K²)(□χ)² |
| (iii) | −(γ/2K²)(D²χ)² |
| (iv) | −(γ/2K²) Ȟ_(μν)Ȟ^(μν) (full intrinsic Hessian) |
| (iv′) | −(3γ/4K²) τ̌_μν τ̌^μν, τ̌ = TL(sym Ȟ) (= sol61's α = 1 operator) |
| (v) | −(γ/2K²)(Δ_uχ)² (intrinsic leaf Laplacian squared) |
| (vi) | β family −(3γ/4K²) |TL(DDχ + βKC)|², β ∈ {0, ½, 1} (0 = (i), 1 = (iv′)); (vi-b) −(γ/2K²) C² σ_μνσ^μν (clock-weighted shear of the medium slices) |
| (vii) | −(γ/2K²)[(□χ)² − A_μνA^μν] (Horndeski-L4-type, = R_μν∇^μχ∇^νχ + div) |
| (viii) | −(γ/2K²)[(Δ_uχ)² − Ȟ_(μν)Ȟ^(μν)] (leaf Galileon; = ³R_ij D^iχD^jχ + div on leaves) |
| (ix) | −(γ/2) m²n² (CFG938's local-EoS realisation (a)) |
| (x) | general isotropic family a(Δ_uχ)² + b|TL(DDχ + β_s K C)|² (theorem L2 and the P938 floor) |
| (xi) | general quadratic form in the medium-frame Hessian blocks with coefficients allowed to depend on n̂ (theorem L1) |

Record alternatives listed and not computed:
- S2's (γ/2)|∇P|² with P built from labels. It needs an origin (CFG938 §3.2, rejected there).
- A solid shear modulus μ ∝ ρ². It gives the wrong nonlinear spherical energy (CFG938 §3.3).
- ∂∂χ in place of ∇∇χ (CFG961 MU3). It is not a tensor and depends on the coordinates, so it is excluded by covariance. It is
  noted only because it gives c_T = c trivially.

## 3. Computations (one script `wt09.py`; sympy + numpy/scipy)

### B. Tensor speed and extra time derivatives
- **B1, local uniform background, exact in V.**
  - Background: Minkowski, medium at rest, χ̄ = V_μx^μ with V_μ = (C, u sinθ, 0, u cosθ). k is along z, and θ is the angle
    between k and the spatial gradient.
  - Perturbations: TT h (+, ×), ξ (3), δχ, δλ, as Fourier plane waves e^{i(kz−ωt)}.
  - Every Hessian-type background quantity vanishes here, so each candidate at second order is its quadratic form of
    first-order blocks: A^(1) = −kkδχ − Γ^(1)·V; u^(1)i = ξ̇^i; θ^(1); K^(1) = ∂ξ̇ + ½ḣ; Ȟ^(1) = DD^(1) + C K^(1); b_i = A^(1)_0i.
  - Included: the Einstein–Hilbert term (normalisation from K4), dust ½ρ₀|ξ̇|², the parent's constraint at first order, and the
    candidate.
  - Omitted, declared, by power counting: W_full and the scalar metric potentials. W has no derivative of h and at most one of
    δχ; gravity is O(k⁰). Both are O(k⁰) relative to the k² terms that set c_T, and relative to the k²ω² kinetic coefficient
    of H.
  - **B1a.** Direct 2×2 TT block. Give the exact roots v² = ω²/k², and the first-order coefficient δ(c_T²/c²) = C_T(θ, pol; u, C)
    in units of L*²/c⁴. Use symbolic θ and a θ grid of 0…π in 13 steps.
  - **B1b.** Schur complement over (ξ, δχ, δλ) in each parent, at leading order in k (ω = vk, k → ∞).
    - Done symbolically where tractable.
    - Otherwise with exact rational arithmetic at ≥ 5 random parameter points.
    - Output: the principal δ(c_T²) including medium mixing.
  - **B1c (Ostrogradsky).** The highest power of ω in each diagonal entry, and in the ξ sector after the parent's constraint. A
    power > 2 means extra time derivatives.
  - **B1d (clock health H).** Set h = 0, eliminate δχ and δλ with the parent's constraint, and take the matrix multiplying ω²k²
    in the ξ sector.
    - Report its eigenvalues for the longitudinal and transverse parts.
    - If one is negative, report the kL* at which the total kinetic coefficient (with ½ρ₀) crosses zero. Use ρ₀ = ρ̄_c and the
      S1d value C = Kρ̄_c c/(3H) at z = 0 and 10.
- **B2, exact FRW.**
  - Metric g = −dt² + a²(t)(δ_ij + h_ij), comoving medium, χ = χ̄(t); a, χ̄ and TT h(t, z) are arbitrary functions.
  - Compute √−g L at O(h²) for EH and each candidate, then the Euler–Lagrange equation for h. Read the coefficients of ∂_t²h
    and ∂_z²h, giving c_T²/c² relative to EH.
  - Also print the background value of each candidate on FRW and whether it is a square of a quantity that vanishes there
    (test F).
  - Evaluate δc_T/c at z = 0 and 10, L* = 24 pc and 1 kpc, with C from S1d.
  - These are reported only. The GW170817 path average belongs to CFG961 (b3) and is not scored here.

### C. Static stiffness
- **C1 (symbolic, spherical, flat leaves, Newtonian order).** Static means θ = C = b = 0. Write each candidate's static energy
  density in terms of u = χ′, and compare its Euler–Lagrange operator with that of the record's (γ/2K²)(Δχ)² = (γ/2)ρ_c²
  (CFG938's E[M_c] form). Output the difference: either ≡ 0, a constant multiple (an effective γ ratio), or a different form.
- **C2 (NGC 3198).**
  - Setup: 43 radii, Υ = 0.61, both footings, L* = 24 pc and 1 kpc.
  - Profile: the γ → 0 law state u(r) from u²/(a₀ − u) = g_N (CFG938), on a cubic spline.
  - Statistic: max over r of |EL_cand − EL_rec| / |EL_rec|.
- **C3 (non-spherical, flat).** Does the Euler operator with respect to χ(x, y, z) of [candidate_static − (γ/2K²)(Δχ)²] vanish
  identically? (Null-Lagrangian test.)
- **C4 (report only, no weight).** The post-Newtonian (Bochner) difference between (i) and (v) on curved static leaves:
  1.5 ³R_rr u²/(K²ρ_c²), with ³R_rr = (2g′ + 2g/r)/c² on the law state of NGC 3198 (both footings). Report the maximum and
  median.
- **C5 (CFG820 consequence).**
  - Identical EL ⇒ bound unchanged (identity).
  - Zero static stiffness ⇒ no screening, so CFG820's MUTATE (S := 1, no L* allowed) applies (cited, not rerun).
  - A constant multiple f ⇒ L* rescales by √f.

### L. Theorems (sympy)
- **L1.** Take the general quadratic form in the medium-frame Hessian blocks:
  - spatial invariants I1 = (tr A)², I2 = |A|², I3 = |n̂An̂|², I4 = Re(n̂An̂ · tr A*), I5 = |An̂|²;
  - mixed invariants J1 = |b|², J2 = |n̂·b|², J3 = Re(n̂·b · n̂An̂*), J4 = Re(n̂·b · tr A*), J5 = Re(b·(An̂)*).

  Impose T at C = 0 (B1a TT image on the light cone, all θ, both polarisations). Then impose T at C ≠ 0 for the projected
  Hessian, and S (C1). Solve for the family.
  - Report the n̂-independent subfamily.
  - Report the n̂-dependent remainder. It is singular where the spatial gradient vanishes (FRW, galaxy centres).
- **L2.** Within (x): add F (vanishing, with its first variation, on S1d's FRW), O and H[P].
  - Is the solution unique?
  - In P938, give the floor min δ(c_T²/c²) at C = 0, in units of L*²u²/c⁴, subject to S, F, O and H[P938].

### N. Numbers
- For each candidate: δc_T/c at the wall (u = a₀; both footings; L* = 24 pc and 1 kpc), and on FRW (B2, z = 0, 10).
- For an EXISTS term: an order-of-magnitude bound on the O(k⁰) remainder at f = 100 Hz, |δv/c| ≲ L*²(Kρ_c)²/(k²c⁴), using
  NGC 3198's largest ρ_c, plus W's a₀u/(k²c⁴). Reported only.

## 4. Per-candidate labels
- **T:** the principal δ(c_T²) ≡ 0 symbolically, in B1a and in B1b (both parents) and in B2.
- **S:** C1 ≡ 0 and C2 ≤ 1e-9 in all four footing × L* combinations.
- **F:** the term and its first variation vanish on S1d's FRW, i.e. it is a sum of squares of quantities that vanish there.
- **O:** no ω-degree > 2 after the parent's constraint, and no ∂_t²h beyond EH in B2.
- **H[P]** (P ∈ {P938, P_int}): the ω²k² eigenvalues from B1d are ≥ 0 (tolerance 1e-12 relative), and the tensor Q_T > 0
  from B2 at z = 0 and 10 for both L* ends.

## 5. Verdict rules (orchestrator's classes; frozen)
- **EXISTS** iff at least one candidate, or a member of the L1/L2 families that is smooth in the background fields (no n̂
  dependence), has T ∧ S ∧ F ∧ O.
  - Name the term. If there are several, the minimal one has the fewest terms and uses only objects already in CFG938's action.
    Uniqueness comes from L1/L2.
  - **Mandatory health qualifier (same prominence).** Print EXISTS followed by "HEALTHY in {parents}". If it is healthy in none,
    print "EXISTS (UNHEALTHY: …)".
  - If the EXISTS term is not H[P938], also print the P938 floor from L2 as **APPROXIMATE[P938]** with its number.
- **APPROXIMATE** iff nothing has T ∧ S ∧ F ∧ O, but something has S ∧ F ∧ O. The floor is the minimum over those of
  max over θ and polarisation of |δ(c_T²/c²)| / (L*²u²/c⁴) at C = 0, with wall numbers.
- **NO-GO** iff L1/L2 prove T ∧ S ∧ F ∧ O incompatible. The theorem's assumptions are listed: local; quadratic in second
  derivatives of χ; built from g, u, χ; smooth in the background.
- n̂-dependent members never count for EXISTS. If they pass T ∧ S, they are reported as a loophole.

## 6. Controls (all must pass for the main run to be read; exit 0 iff all pass)
- **K1:** candidate (i) gives δ(c_T²/c²) = +1.5 L*²u²/c⁴ at C = 0 for every θ on the grid and both polarisations (B1a, first
  order, exact symbolic). This reproduces WT-02 E1.
- **K2:** γ = 0 gives the roots v² = 1 exactly for every candidate (B1a and B2).
- **K3:** (i)'s static spherical EL equals CFG938's E[M_c] stiffness EL symbolically, and the NGC 3198 γ → 0 law reduction gives
  max|g/g_law − 1| ≤ 1e-12 on both footings (CFG938 K1: 2.2e-16).
- **K4:** EH normalisation. For a TT plane wave in Minkowski, √−g R at O(h²) averages to ¼(ω² − k²)A² (c = 1; off shell).
- **K5:** (i) on exact FRW (B2) reproduces Q_T = 1 − 3γC²/K (the sol61 audit's formula) symbolically.
- **K6:** flat-space null Lagrangians: EL_χ[|∂∂χ|² − (Δχ)²] ≡ 0 and EL_χ[τ² − ⅔(Δχ)²] ≡ 0 for a general χ(x, y, z)
  (CFG938 S2d).

## 7. MUTATE (`WT09_MUTATE=1`; separate outputs `*_MUTATE`; exit 1 iff every tooth bites, else 2)
- **MU1 (c_T tooth):** (v) + 0.01 × (3γ/4K²) ττ. Bites iff B1a reports δ(c_T²/c²) = 0.015 L*²u²/c⁴ (C = 0) and the term loses T.
- **MU2 (F tooth):** (v) with Δ_uχ → D²χ + 0.9 θC. Bites iff its FRW background value ≠ 0 and the term loses F.
- **MU3 (S tooth):** (v) with coefficient γ/K² (×2). Bites iff C2 gives a relative difference of 1.0 and the term loses S.
- **MU4 (FRW T tooth):** (v) + (vi-b) on exact FRW. Bites iff B2 reports c_T ≠ c.
- **MU5 (H tooth, inverse):** C = 0 in B1d. Bites iff (v)'s ω²k² eigenvalue becomes ≥ 0 (health PASS), showing that H is not
  hard-wired.
- The MUTATE verdict line must differ from main wherever a tooth acts.

## 8. Outputs
`DERIVATION.md`, `wt09.py`, `wt09.out`, `wt09_results.json`, `wt09_MUTATE.out`, `wt09_results_MUTATE.json`, `README.md`. All are
left uncommitted for orchestrator review. Changes after the freeze go only in appended amendments; this text is not edited.

## 9. Compute and hygiene
- One process, `OMP_NUM_THREADS=1 nice -n 10`, minutes. `/usr/bin/time -l` peak RSS < 1 GB.
- In-script guard: exit 75 above 0.9 GB RSS.
- If a 1024³ PM job (`*_pm.py`) is live: run only short jobs, and exit 75 if swap use grows by more than 1 GB over its start
  value or if free + inactive drops below 8 GB.
- Before each run, check that free + inactive ≥ 12 GB (or ≥ 8 GB with the watchdog when a PM job is live). Wait if two other
  `wt0*.py` processes are running.
- No downloads. No other lane's files are edited, staged or run. No personal names or home paths. Explicit-path commits only;
  no push.

## 10. Blindness disclosure (not blind)
Before freezing I read:
- WT-02's README and criteria;
- CFG961's criteria (hand expectation (b): the FRW clock term through Γ⁰_ij C);
- CFG938's DERIVATION, plus cfg938.py K1;
- PAPER49's deposit note; CFG820, CFG821 and CFG691's heads;
- the DHOST / fried-chicken / KGB notes;
- the sol61 audit (RESULT, TT_ADVERSARIAL_CHECK, REPAIR_SCOPE), which already derived Q_T = 1 − 3γC²/K on FRW, the BBN-epoch
  Q_T < 0, the α = 1 operator (= (iv′)), and its negative restricted longitudinal kinetic coefficient −γα²C²k²/K².

Without running anything I derived by hand, and expect:
1. (i): δ(c_T²/c²) = 1.5 L*²(u² + C² + 2uC cosθ)/c⁴ at first order. The cross term depends on direction.
2. Every trace-only term ((ii), (iii), (v), (ix)) has no principal TT coupling, because g^{ij}δΓ^k_ij = ∂_jh_jk − ½∂_kh = 0 for
   TT waves. So c_T = c exactly at principal order.
3. (iii) on shell is the local EoS (γ/2)ρ² and fails F (BBN, CFG938 S2d3). (ii) fails F and O.
4. (v):
   - passes T;
   - passes S by construction (static ⇒ θ = 0 ⇒ Δ_uχ = D²χ = Kρ_c);
   - passes F by construction (Δ_uχ̄ = 0 on FRW) and passes O.
   - In P938 it carries −(γ/2K²)C²(δθ)², a negative medium kinetic term. Its sign flips at kL* = √(12/Ω_c(z)) ≈ 6.7 (z = 0)
     and 3.8 (z = 10).
   - In P_int its on-shell form is (γ/2)δρ², with no clock term.
5. (iv) / (iv′):
   - The spatial-gradient c_T shift remains: +1.0 (iv) and +1.5 (iv′) × L*²u²/c⁴.
   - The clock part moves into a wrong-sign medium shear kinetic term.
   - Mixing with transverse ξ can change the angular dependence at high k.
6. (vii), (viii) and (vi-b) give zero static stiffness.
7. L1: T at C = 0 forces the |A|² coefficient to zero. S then leaves only (tr A)² among the isotropic forms, and F selects
   Δ_uχ, so (v) is unique. An n̂-dependent family should survive T at C = 0 and S, but it is singular at V⃗ = 0.
8. L2 / P938 floor: health forces a ≤ 0 and β_s = 0, so b ≥ 3γ/(4K²). The floor is (i)'s own 1.5 L*²u²/c⁴.
9. C4 should be about Φ/c² ~ 1e-6.

So I expect "EXISTS: −(γ/2K²)(Δ_uχ)², HEALTHY in P_int only; APPROXIMATE[P938] floor = 1.5". The rules above decide either way.
The teeth MU1–MU5 check that T, F, S and H can fail. Expectation 4's health sign is the result most at risk of being wrong, and it
is tested by B1d with the full parent constraint, not by my reduction.
