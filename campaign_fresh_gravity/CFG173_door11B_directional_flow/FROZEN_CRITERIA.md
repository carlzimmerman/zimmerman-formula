# CFG173 — door 11, variant 11B′: a compressible directional flow of a massless Λ-medium. FROZEN CRITERIA

Written 2026-09-29, before any CFG173 script or number, at the orchestrator's request. The governing file is `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`: gates a2e76b4ad, addendum 1 (4a022adf0), addendum 2 (0802aef82) and erratum 1. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## What was known when this was written

- **Already known:**
  - the target (CFG44, P2);
  - the ten-door result: cold-matter dynamics never give r_M ∝ M^½, and a missing object must carry an acceleration scale;
  - the data chat's literature note (044f3e425): the G6 limits, and no directional-flow MOND model in the literature;
  - CFG171's headline (door 11A, relayed): the only flow law giving P2 is AQUAL/QUMOND, a restatement.
- **The owner's picture (addenda 1 and 2):**
  - the medium flows from ONE direction and is compressed where it crosses matter;
  - it has no rest mass and no particle content;
  - the extra gravity is an effect of the flow;
  - the cold component stays, unless a variant passes G2 without it.
- **I expect a scoped no-go,** for the four reasons written below as hypotheses H-A to H-D. The menu of variants was written knowing these expectations. The scripts decide, and a pass is reported as a pass.

## The kernel and constants (erratum 1)

- **P2 is primary:** g_tot² = g_N² + a₀ g_N. The phantom a_ph = g_tot − g_N tends to a₀/2 for g_N ≫ a₀ and to √(g_N a₀) in the deep regime. For a point mass, a_ph/a₀ = s(x) = (√(1+x²) − 1)/x², with x = r/r_M.
- **Other kernels:** the simple kernel is reported where a result depends on the kernel. ν_mono is reported for G1 only where it enters.
- **Constants:**
  - a₀ = κ c √(Gρ_Λ), κ = ½ FITTED, on the canonical footing (a₀ = 9.36 × 10⁻¹¹ m s⁻²), with the alt footing reported for G1.
  - Both footings, and ρ_Λ, are read from CFG4_common.
  - The Λ-tied scales allowed by G4 are ρ_Λc², P_cap = (κ²/8π)ρ_Λc², √(Gρ_Λ) and c.

## The medium: its stress-energy, stated per variant (addendum 2)

Each variant states whether and how the medium gravitates. In GR, energy and stress gravitate.

- **V1 — vacuum-like, w = −1:** T^μν = −ρ_Λ c² g^μν. Its active density is ρ + 3p/c² = −2ρ_Λ (repulsive).
- **V1′ — a near-vacuum field** (k-essence-like, no particles): w = −1 + ε with ε ∈ (0, 0.1], and rest-frame sound speed c_s² ∈ [10⁻⁴, 1] c².
  - The range is the relayed DESI DR2 + Planck + Union3 value, log₁₀ c_s² = −3.00 (+2.9, −0.99), unverified here.
  - Its inertia (ρ + p/c²) is ερ_Λ.
- **V2 — a null directional flux:** T^μν = (u_F/c²) k^μ k^ν, flowing at c along −ẑ ("from the top").
  - u_F ∈ {ρ_Λc², P_cap}.
  - Its active density is 2u_F/c² along the beam.
- **V3 — a radiation-like fluid** (w = 1/3), whose rest frame streams at U relative to the galaxy.
  - u_R ∈ {ρ_Λc², P_cap}; inertia 4u_R/3c²; active density 2u_R/c².
- **V4 — the granted flux law, the restatement ceiling:**
  - An energy flux J = n(q) q q̂ with ∇·J = −σ_E ρ_b (the baryons absorb or redirect the flow: the "boost"). The force on test bodies is a = β u, with β = b√(Gρ_Λ) (b = 1 is the Λ-tie).
  - The stream is u → U ẑ far away.
  - n(q) is chosen so that the static (U = 0) solution reproduces P2 exactly: F(s) ≡ n q ∝ s²/(1 − 2s), with s = βq/a₀.
  - V4 is declared a RESTATEMENT for G1, because n(q) is reverse-engineered from the kernel. It is used only to measure what a directional stream does to the best possible flow law, and what the boost's energy costs.
- **Not duplicated:** 11C's vector or khronon stress (CFG172).

## The force on test bodies (declared readings; each variant is scored under each reading that applies)

- **T1 — gravity of the flow:** the flow's energy and stress gravitate. Weak field: ∇²Φ = 4πG(T⁰⁰ + Σᵢ Tⁱⁱ)/c².
- **T2 — push:** the flow transfers momentum to matter by absorption or scattering, with a universal opacity k per unit mass. The equivalence principle requires k to be universal.
  - For V2 and V3, "compression" is the depletion or focusing of the flux behind absorbing matter.
- **T3 — flow force** (V4 only): a = βu.
- **The compaction mechanisms:**
  - gravitational focusing: null geodesics (V2); hydrostatic compression and Bondi–Hoyle focusing of a slow stream (V3, V1′);
  - absorption shadows (T2);
  - the sink (V4).

## Hypotheses (expectations written before any script)

- **H-A — no flow for Λ.** For w = −1:
  - T^μν is invariant under every boost;
  - T⁰ⁱ = 0 in every frame;
  - the projected relativistic Euler equation forces ∇⊥p = 0.
  - So there is no rest frame, no energy or momentum flux, and no compression.
- **H-B — the flow's own gravity is far too weak.** The compaction needed for the flow's own gravity to supply the phantom is
  - C_req(x, M) = a_ph(x) / [(4π/3) G ρ_act r], over the G1 grid, with ρ_act the active density.
  - It is compared with what each mechanism can achieve:
    - the lensing magnification of a null flux behind a point lens, A(u) − 1 with u = b/R_E(z) and R_E² = 4GMz/c²; zero upstream;
    - V3's hydrostatic compression, δu/u = 4GM/(c²r);
    - V1′'s, δρ/ρ = εGM/(c_s² r), at the most compressible corner (ε = 0.1, c_s² = 10⁻⁴ c²).
- **H-C — push is Le Sage.**
  - A directional flux's T2 force vanishes on the upstream side and scales linearly with M.
  - The absorbed power exceeds the G3 energy line.
  - Stars and planets are optically thick (kΣ ≫ 1), so the push is not proportional to mass: the equivalence principle is broken.
- **H-D — the granted law cannot host a stream.**
  - With Λ-tied constants, the sink's power fails G3.
  - The stream linearises the law beyond x_U ≈ κc/(bU): this affects G1 at large x, G7 and G8.
  - No value of b satisfies both G1-with-stream and G3.
  - The medium's sound speed, from its Bernoulli relation, is imaginary (G5).

## Gates and pass lines (DOOR11 G1–G8; values declared now)

- **G1 — the law.**
  - The flow's force on test bodies must reproduce g_tot (P2) within 10% at every point of the grid:
    - x on a log grid over [0.1, 30];
    - M ∈ {10⁹, 10¹⁰, 10¹¹, 10¹²} M☉;
    - point mass, and CFG44's compact exponential sphere (ρ ∝ e^(−r/h), h = 2 kpc at every mass);
    - directions θ ∈ {0°, 45°, 90°, 135°, 180°} from the upstream axis;
    - with the same constants at every mass.
  - A variant with a free constant may fix it once: at M = 10¹¹, x = 1, at its most favourable direction (declared). It is then scored everywhere.
  - The mass-scaling test is the ratio F(x; 10¹²)/F(x; 10⁹) against 1, since the target is universal in x.
  - A restatement (V4) fails G1-as-mechanism by rule; its G1-with-stream is still computed.
- **G2 — cosmology.**
  - A Λ-tied flow with w ≠ −1 must not change the CMB: FAIL if its energy density at z = 1100 exceeds 1% of the matter density.
  - V1′'s growth effect is estimated as ε Ω_Λ/Ω_m: PASS if ≤ 0.05; otherwise UNDECIDED (no Boltzmann code).
  - Perturbations are stated, or the row is marked UNDEFINED.
- **G3 — reaction and energy.**
  - (a) The net force the flow exerts on the galaxy's own baryons must be ≤ 0.10 g_law over x ∈ [0.3, 30].
  - (b) The energy the flow must supply (absorbed or redirected) over a Hubble time must be ≤ the baryons' orbital energy ½ M_b v_f², with v_f = (G M_b a₀)^(1/4).
  - For a steady power, the ratio does not depend on the r_ta convention (CFG48 G4). This is stated rather than recomputed.
- **G4 — constants.** Count every constant.
  - Allowed: κ, Ω_c h², and the Λ-tied scales above.
  - k, b ≠ 1, ε and c_s are each a G4 FAIL unless tied.
  - U is environmental, not a constant.
- **G5 — well-posedness and the Solar System.**
  - (a) Stability: no imaginary sound speed and no ghost.
  - (b) Cassini (γ − 1), and the ephemeris bounds: Q₂ ≤ 5.2 × 10⁻²⁷ s⁻², and anomalous acceleration ≤ 3.7 × 10⁻¹⁴ m s⁻² at Mars (the record's value).
  - (c) The equivalence principle: any Solar-System body with kΣ ≥ 1 is a FAIL.
- **G6 — preferred frame.** The frame-dependent anomalous acceleration at 1 AU, for w = 370 km/s, is compared with the two PPN-implied scales:
  - α₂-type: (α₂/2)(w/c)² GM☉/r², with α₂ = 1.6 × 10⁻⁹ (Shao et al. 2013; strong field), giving 7 × 10⁻¹⁸ m s⁻²;
  - α₁-type: (α₁/2)(w v⊕/c²) GM☉/r², with |α₁| = 3.5 × 10⁻⁵ (Shao & Wex 2012), giving 1.3 × 10⁻¹⁴ m s⁻².
  - PASS below the α₂ scale; FAIL above the α₁ scale; UNDECIDED between. A non-metric force maps onto PPN only in order of magnitude, as declared.
- **G7 — frame dependence of a₀.** The monopole (angle-averaged) force at fixed x must change by ≤ 10% for U ∈ [0, 600] km/s, over x ∈ [0.1, 30].
- **G8 — anisotropy.**
  - (a) Azimuthally averaged: the RMS scatter in log g at fixed g_bar, induced by the flow's orientation and by U ∈ [0, 600] km/s, must be ≤ 0.048 dex. That is the RAR's 95% intrinsic-scatter ceiling (CFG4 H4). This bound is declared independently of CFG182.
  - (b) Side to side (ℓ = 1): the approaching-minus-receding rotation-velocity asymmetry induced at U = 600 km/s, in the galaxy's free-falling frame. PASS ≤ 0.02; FAIL > 0.10; UNDECIDED between.
  - The 0.10 is the commonly reported ~10% level of kinematic lopsidedness in HI discs. Its source is being verified. If the verified statistic differs, the README reports G8b against it as a disclosed departure; no G8b number is read before that.

## What the script computes (declared)

- **S1 (H-A, V1; sympy):**
  - η is invariant under boosts;
  - T⁰ⁱ(w) = (1 + w) ρ_Λ c² γ² vⁱ/c, which is 0 at w = −1 for every v;
  - the projected Euler equation at ρ + p = 0 reduces to h^μν ∂_ν p = 0.
- **S2 (H-B, T1 for V1′, V2, V3):**
  - C_req over the G1 grid, for both kernels and both footings, with ρ_act = 2ρ_Λ (V2, V3) and 2ερ_Λ for V1′'s compression;
  - the achievable compaction of each mechanism at the same points;
  - the headline number: the minimum over the grid of C_req/C_achieved, and whether any grid point passes.
- **S3 (H-C, T2 for V2 and V3):**
  - V2's shadow geometry: the upstream force (zero) and the downstream force proportional to the column density Σ(b); G1 point by point.
  - The opacity k₀ that normalises the downstream push to the target at M = 10¹¹, x = 1, θ = 180°.
  - The mass scaling at fixed x; the absorbed power against G3.
  - The optical depths of the Sun and the Earth (G5c).
  - V3's isotropic-bath push (the mutual-shadowing 1/r² force, proportional to M): the G1 mass scaling; the absorbed power.
  - If electromagnetic, V3's bath temperature (u_R = aT⁴), reported only.
  - G2 for V2 and V3: Ω_flow/Ω_m at z = 1100 for w = 1/3.
- **S4 (H-D, V4):**
  - The first-order stream perturbation δψ = U f(r) cos θ solves (x² F_s f′)′ − 2 (F/s) f = 0.
    - It starts from the regular core solution f ∝ x³, is integrated outward, and is normalised to f → x (the uniform stream) at large x.
    - The coefficient of the 1/x term is B.
    - The P2 and simple constitutive laws are both done.
  - The second-order monopole ⟨δs⟩₂/s from the exact flux constraint (the sink flux through every sphere is independent of U). This is algebraic in f, derived in sympy in the script. It gives G7 and the ℓ = 0 part of G8a.
  - The second-order ℓ = 2 part, from its ODE with the first-order source. The declared boundary conditions are regular at the core and carry no homogeneous growing term. It gives the orientation part of G8a.
  - The first-order ℓ = 1 relative dipole in the free-falling frame, λ_U (f′ − ⟨f′⟩_baryons)/s, with λ_U = bU/(κc). It gives G8b.
  - All of these for U ∈ {150, 300, 370, 600} km/s at b = 1.
  - The exclusion window in b: b_max from G1/G7 at x = 30 and U = 600 km/s, against b_min from G3.
  - The sink power per unit baryon mass, σ_E = 4π c² √(Gρ_Λ)/b for n₁ = ρ_Λc², and × κ²/8π for P_cap.
  - G5a: c_s² = −q²/L, with L = d ln n/d ln q.
  - G6 at 1 AU, from the ℓ = 1 solution in the Sun's field.
  - G3a: the momentum the sink absorbs from the stream.
- **The gate matrix:** each variant × G1–G8, as PASS, FAIL, UNDECIDED, UNDEFINED or NOT REACHED. A gate that is not reached (because an earlier gate fails structurally) is still computed where the door requires it (G6–G8 for 11B′).

## Controls and MUTATE (each must change its section's headline; declared control failures are kept)

- **C1:** P2's s(x) and F(s) satisfy F(s(x)) x² = 1 for the point mass (sympy, and numerically to 10⁻¹²).
- **C2:** the ℓ = 1 ODE in the deep regime (F = s², s = 1/x) has exactly the solutions x and 1/x (sympy).
- **C3:** the lensing magnification reduces to 1 + 2/u⁴ for u ≫ 1, and to the point-lens formula (u² + 2)/(u √(u² + 4)).
- **C4:** S3's k₀ reproduces the target at its normalisation point to 10⁻⁶.
- **MUTATE=A:** w = −0.9. S1's "no flow" checks must fail.
- **MUTATE=B:** the achievable compaction is multiplied by 10¹². S2's headline must flip.
- **MUTATE=C:** V2's flux is made isotropic. S3's zero-upstream check must fail.
- **MUTATE=D:** V4's constitutive law is replaced by its deep-regime form F = s² everywhere, with no stiff core. The first-order dipole must vanish, because a uniform stream is then an exact solution. S4's G8b row must change.

## Readings (declared)

- **A scoped no-go is the expected and valid answer.** "Scoped" means for the variants V1–V4 and the readings T1–T3 written here.
- **If any variant passes G1 as a mechanism,** it is reported as such, and an independent re-derivation is requested before anyone calls it a result.
- **A no-go here does not touch candidate B.** B's law, its a₀ = κc√(Gρ_Λ) tie and the cold component are unchanged. It says that this door, as written, does not supply B's missing mechanism.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed, or that the data favour any model.
