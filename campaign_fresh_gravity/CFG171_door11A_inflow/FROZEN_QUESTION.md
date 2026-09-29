# CFG171 — Door 11A (radial inflow, the CONTROL reading): frozen question, criteria and pass lines

Written 2026-09-29 before any CFG171 script or number. Governing file: `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md` (gates G1–G8, rules, Addendum 1). Under Addendum 1, 11A (inflow from all around) is the **control reading**; 11B′ is primary and is not tested here. The menu of candidate flow laws below was written knowing the target (CFG44) and the ten-door result (a missing object must carry an acceleration scale); it is not a blind sample. κ = ½ is FITTED. Nothing here says the theory is closed.

## The frozen question

Is there a **dynamical law** for a steady radial inflow of a Λ-tied medium into each bound system (equation of motion for the medium, or a field equation for the flow, with a source term localised on the baryons as "the boost on crossing matter") whose steady solution gives the law's total acceleration, with a₀ = κ c √(Gρ_Λ) and no other constant? A prescribed v(r) with v² = 2∫g dr is a restatement and fails G1-as-mechanism.

## Target and a flagged inconsistency

- Target: the record's P2, g = √(g_N² + a₀ g_N), ν(y) = √(1 + 1/y) (as implemented in `CFG44_fluid_target/Bcommon.nu_p2` and `real_research/derivation_chain_2026/FP1_static_sector.py`); point mass ⇒ M_dyn = M_b √(1 + x²), x = r/r_M, r_M = √(GM_b/a₀). ν_mono reported (Bcommon.nu_mono, read-only import).
- Flag: the DOOR11 file's parenthetical "ν = ½ + √(¼ + a₀/g_N)" is the "simple" ν, not the record's P2 (they differ by ~14% at x = 1 and in the high-g tail, a₀ vs a₀/2). The orchestrator's instruction and CFG44 both use √(g_N² + a₀g_N); that is primary here. The simple-ν difference is reported, never scored.

## Hypotheses (all steps)

Spherical, steady, Newtonian (v ≪ c, g ≪ c²/r). **PG postulate:** test bodies are carried by the flow, so their acceleration is the flow parcels' acceleration Dv/Dt = ∂_t v + (v·∇)v; for a steady radial flow the inward acceleration is g = −d(v²/2)/dr. Λ tie per footing: H_foot = Z a₀/c with Z = √(32π/3) = 5.7888 (κ = ½), canonical a₀ = 9.3603e-11 (H_Λ), alt a₀ = 1.1312e-10 (H₀). ρ_Λ = 3H_Λ²/(8πG).

## Step 1 claims (sympy; verify, do not assume)

- 1a. PG–de Sitter (Schwarzschild–de Sitter in PG form): v² = 2GM/r + Λc²r²/3 exactly, no cross term; the PG congruence (lapse 1) is geodesic with d²r/dτ² = v v′.
- 1b. Linear velocity superposition v = v_N + v_Λ: the cross-term acceleration ∝ r^(−½), rotation speed ∝ r^(¼), not deep-MOND r^(−1).
- 1c. (added) No algebraic superposition term v_N^a v_Λ^b c^(2−a−b) gives the deep-MOND force (∝ √M / r): the exponents forced by √M and 1/r give an r-independent term with zero force.
- 1d. (added) A pure Λ-vacuum (P = −ρc²) has T^μν independent of any u^μ: it has no velocity, so "the Λ-vacuum flows" needs a medium that is not exactly Λ.
- 1e. (added) A conserved barotropic medium in steady radial inflow outside its sink produces an inward acceleration falling slower than r^(−5) only if c_s² < 0 (gradient instability).
- 1f. (added) A negative-c_s² isothermal medium in the supersonic regime gives g = 2|c_s²|/r (a flat curve with V_c² fixed by the medium, not the BTFR).
- 1g. (added) For a potential flow obeying the Hamilton–Jacobi (Bernoulli) law ∂_tχ + |∇χ|²/2 = −Φ, D(∇χ)/Dt = −∇Φ identically (the flow parcels are just test particles; Galilean-invariant).
- 1h. (added) P2's AQUAL form is elliptic: d(μ(z) z)/dz > 0.

## Candidate flow laws (the search menu, each scored separately, never pooled)

- **L0** GR's own river (PG–Schwarzschild–de Sitter): v²/2 = −Φ_N + H²r²/2. Control.
- **L1** linear velocity superposition v = −√(2GM(<r)/r)·(Newtonian river) + H r (the Λ/Hubble outflow), system's own frame.
- **L2** conserved incompressible Λ-medium (inertial density ρ_Λ/c²), sink on the baryons, its flow added to the river in v² (L2a) or in v (L2b). Free sink amplitude.
- **L3** conserved barotropic compressible medium: L3a with the Λ-like EOS P = wρc² (w ∈ (−1, 0)); L3b isothermal with c_s² = −K < 0 (supersonic branch).
- **L4** flow-potential field equation: AQUAL/QUMOND written for Ψ = v²/2, ∇·[μ(|∇Ψ|/a₀)∇Ψ] = −4πGρ_b, scale read as P_cap = (κ²/8π)ρ_Λc² = a₀²/(8πG). **Declared in advance to be a restatement** (the flow is a relabelled potential); its G1 can only be "p*".
- Flow normalisation for L4 (my choice, disclosed): the minimal one, v = 0 at the zero-gravity radius r* where g_law(r*) = H² r*; v = −√(2Ψ) inside, +√(2Ψ) outside (Hubble outflow).

## Gates, pass lines and how each is computed

- **G1** max over x ∈ [0.1, 30] (400 log points) of |g_model/g_target − 1| ≤ 0.10, M_b ∈ {1e9, 1e10, 1e11, 1e12} M☉, point mass and exponential sphere with h = {2, 3, 4, 5} kpc (CFG118's HEXP, primary) and h = 0.5 r_M (CFG124, secondary), the SAME constants at every mass. For laws with a free amplitude (L2, L3b) I report the smallest max-residual achievable by ANY single amplitude shared across the four masses (a bound, never adopted as a value); G1 fails if that bound exceeds 0.10. L4 is a restatement: PASS only as "p*", FAIL as mechanism.
- **G2** background: |v/(H r) − 1| ≤ 0.05 at r = 10 r* (reduces to the Hubble/de Sitter flow). Growth and CMB: UNDEFINED unless perturbation equations exist; expected UNDEFINED (11A is defined per bound system, i.e. it carries a switch, Gap 1).
- **G3** reaction ≤ 0.10 g_law for x ∈ [0.3, 30]; energy ≤ ½ M_b V_f² (V_f² = √(GM_b a₀)) supplied within r_e = 0.4 r_ta over t = 1/H_foot, in both r_ta conventions: (A) CFG48 Gcommon (collapse mass M_b(1 + Ω_c/Ω_b), Δ_ta = 11.81), (B) CFG4-style (the P2 point-mass M_dyn at the same Δ_ta ρ_m; control: B/A must fall in the referee's 1.7–3.6). For L4 two readings: potential (no medium; reaction 0, energy 0, p*) and literal medium (inertia ρ_Λ/c²): (i) the fraction of the medium's required creation/destruction |s| = |r⁻²(r² ρ_m v)′| lying where ρ_b < 1e-3 ρ_b(0) (exp sphere) must be ≤ 0.10 for "the boost is localised on the baryons"; (ii) reaction |s v|/(ρ_b g_law) on x ∈ [0.3, 30] if the destroyed momentum lands on the baryons; (iii) the kinetic-energy flux 4πr_e² ρ_m v³/2 × (1/H) vs ½M_bV_f².
- **G4** count every constant beyond κ and Ω_c h²; a free amplitude, sound speed or sink rate is a FAIL unless tied to Λ in the same law.
- **G5** monopole anomaly at Earth (1 AU) and Mars (1.5237 AU) against the record's Sereno–Jetzer 2σ inversion (their Eq 9, Table 1, as in `real_research/reviews/mi_alpha1_solar_system_2026.py`; control: reproduce Earth 3.66e-14, Mars 3.72e-14 m/s² and the record's 1278× for a₀/2); Q₂ ≤ 5.2e-27 s⁻² (GATES 4.01): with the Sun owning its own inflow (11A's literal "each bound system") the strict-law Q₂ is cited from GATES 4.01 (4.0–5.7× the ceiling, not recomputed); with the Sun owning none, the host tide reproduced from CFG7 H1 (1.56e-31 to 2.56e-31). Well-posedness: sign of c_s² (L3), AQUAL ellipticity (L4); causality of an elliptic Newtonian flow law: OPEN (11C's job).
- **G7** fractional change of the radial force at x = 1 and x = 10 for a system moving at w ∈ [0, 600] km/s relative to the flow's frame; pass ≤ 0.10. L0 (GR, covariant), L1 (literal v superposition: the −∇(v_N r̂·w) term), L2 (ratio w/|v|), L4 (identity 1g).
- **G6** (preferred-frame PPN) and **G8** (11B only) are not scored here; say so.

## MUTATE controls (each must change the headline; outputs named by mode; failures kept)

- S1 (symbolic): insert a linear-superposition cross term into the SdS metric function ⇒ claim 1a must fail ⇒ exit 1.
- S2 (G1), mode a: L4 with μ ≡ 1 (the GR river) against the P2 target ⇒ L4's G1 row must flip to FAIL; mode b: target replaced by GR's g_N − H²r ⇒ L0's G1 row must flip to PASS.
- S3 (G2/G3/G5/G7), mode a: the target kernel replaced by the α = 2 kernel ν = [(1 + √(1 + 4/y²))/2]^(½) ⇒ L4's Solar-System monopole row must flip to PASS.

## Honest expected outcome (declared now)

A scoped no-go. Expected: L0 is Newton plus a repulsive, negligible Λ term; L1 has the wrong shape (r^(−½)), a tiny amplitude and a catastrophic frame dependence; L2/L3 give r^(−5)-type forces or need c_s² < 0; the only law that reproduces P2 is L4, which is AQUAL/QUMOND with Ψ renamed v²/2 — a restatement whose interpolating function is postulated, whose flow does no work, and whose literal-medium reading needs the medium created/destroyed throughout space, not on the baryons. P2's own α = 1 tail fails the planets whatever the flow does. If any genuine flow law passes G1 as a mechanism, an independent re-derivation is requested before any claim.
