# CFG253 — dark energy converted into the cold mass: an interacting vacuum, three readings (frozen criteria, written before any script)

Research direction: this lane was directed by the owner (the repository's author), who proposed the idea and asked for it to be tested.

**Origin.** An owner's idea, recorded as a hypothesis to test, not as evidence: the cold dark mass the CMB needs (Ω_c h² ≈ 0.12) is dark energy "compacted" into a cold fluid, not a particle.

**Framework facts used (not re-derived).**
- a₀ = κ c √(G ρ_DE), κ = ½ FITTED (never derived). a₀ ∝ √ρ_DE, so a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)).
- The framework's distinctive prediction is a FLAT a₀(z) (ρ_DE constant). The rival is a₀ ∝ H(z).
- The mass is still required (no dark-matter particle is added here; the question is where the cold fluid's energy came from).

**What this file was written knowing (not blind).** Read before writing: LEDGER rows CFG131, CFG156, CFG176, CFG177, CFG195, CFG213, CFG220, CFG222, CFG251, CFG252; the READMEs of CFG131, CFG176, CFG195 (first 60 lines), CFG222 and CFG251; `STANDING_2026-09-29.md` §1–5 and appendices; `CFG4_cosmology.out` (Planck ω_c = 0.1200 ± 0.0012 as committed there); the GDM note (`real_research/dark_fluid_2026/README.md`; the particle-vs-mode review `real_research/reviews/mi_particle_vs_mode_2026.py` by its record summary). The committed numbers these quote were seen before the gates were set. No CFG253 number existed when this file was written.

**Scope.** Background (homogeneous) cosmology only, plus the committed perturbation bound from CFG131/CFG156 for coldness. No Boltzmann-code run, no likelihood, no data, no downloads, no edits to existing files, no commit.

## 1. Physics under test (exact hypotheses)

- H1: GR, flat FRW. Components: the dark energy ρ_DE with w = −1 (a Lorentz-invariant vacuum stress T = −ρ_DE g), a cold fluid ρ_c (w = 0), baryons ρ_b ∝ a⁻³, radiation ρ_r ∝ a⁻⁴.
- H2: exchange ρ̇_DE = −Q, ρ̇_c + 3Hρ_c = +Q; Q^μ = Q u_c^μ (CFG131's H3). Q > 0 is the owner's direction (DE → cold).
- H3: baryons and radiation are coupled only through gravity.
- H4: a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) (the framework's tie, applied at each epoch).
- Declared inputs (CFG131's Dcommon values, the same as CFG43): H₀ = 67.4, Ω_c = 0.265, Ω_b = 0.050, Ω_Λ = 0.685, Ω_r = 9.1e-5 today; z_rec = 1090 (L121 as parsed by CFG251). The rival's E(z) and the reference ΛCDM use these values.
- Note (not a gate): a w = −1 vacuum cannot be "compacted" by compression (CFG176 S2: ρ ∝ n^{1+w} is constant). The only way the idea can move vacuum energy into a cold fluid is EXCHANGE, i.e. breaking CFG195's premise P1 (separate conservation). This lane is that exchange.

## 2. Readings (scored separately, never pooled)

**(A) Continuous transfer, ongoing to today.** Three forms, each with one amplitude ξ:
- A1: Q = ξ H ρ_DE;
- A2: Q = ξ H ρ_c;
- A3: Q = ξ H_L ρ_DE, H_L = √(8πGρ_DE/3) (CFG131's only cold-safe form; its flat-a₀ limit |ξ| < 0.0275).
Normalisation: today's Ω_c, Ω_Λ fixed at the declared values (so a₀(0) is the observed anchor). Key derived quantity: **F_made ≡ 1 − (ρ_c a³)_{z_rec}/(ρ_c a³)_0**, the fraction of today's cold mass created after recombination.

**(B) Early transfer, completed before recombination (switches off at z_t > 1100).** After z_t, ρ_DE = ρ_Λ0 (constant), so a₀ is flat at z < z_t. Variants:
- B-inst: an instantaneous transfer at z_t (the minimum-cost bound: every alternative puts more vacuum energy in the pre-transfer era);
- B-exp: an extra vacuum component ρ_X (w = −1) decaying at a constant rate, Q = Γ ρ_X, Γ = H_ΛCDM(z_Γ), beside a separate remnant ρ_Λ0;
- B-pow: a single vacuum with Q = ξ H ρ_DE switched on for z > z_t and off after (ξ < 3), showing whether a power-law transfer can make the mass at all.
z_t grid: 1100, 3423 (z_eq), 1e4, 7e4, 1e5, 1e6, 1e8, 4.3e8, 1e9, 1e10.

**(C) Clusters.** A transfer localised in bound systems supplying the cluster cold mass (6.8× baryons, the record's X-COP-based requirement; memory/cluster standing g04a). Cite CFG131 D1 (vacuum uniform on the fluid's slices) and CFG176/CFG195 (a Λ cannot flow; the NEC column bound 0.078 for a non-Λ medium) where they apply; compute only the volume budget and the inflow fraction a cluster would need.

## 3. Gates (frozen)

- **G1, the CMB cold density history.**
  - (A): PASS if F_made ≤ 0.03 (primary tolerance); sensitivity 0.10. This is a DECLARED convention, not a likelihood: Planck's ω_c = 0.1200 ± 0.0012 is a 1% statement at recombination (CFG4_cosmology.out), and 3% allows a late-vs-early matter-density difference of that order. The owner's idea literally needs F_made ≈ 1 for (A) to BE the cold mass; "makes the cold mass" is declared as F_made ≥ 0.5.
  - (B): PASS if the cold mass created after z_rec is ≤ 3% of today's (by construction for B-inst); reported: the fraction created after z = 7e4 (horizon entry of k = 0.2/Mpc, computed, the smallest Planck scales).
  - Identity to be checked: ρ_c a³ exactly constant from z_rec to today (ΛCDM's history) ⇔ Q = 0 on that interval. So any (A) transfer that passes G1 exactly makes nothing.
- **G2, flat a₀ at z ≤ 5.** Two lines, stated separately:
  - (a) CFG131's line: max_{z≤5} |a₀(z)/a₀(0) − 1| < 0.01.
  - (b) tonight's data band, by PLACEMENT, not re-scoring: define φ(z) = log[a₀(z)/a₀(0)] / log E_ΛCDM(z) (0 = flat, 1 = rival). Labels:
    - FLAT-LIKE: max_{z≤5} |log₁₀ ratio| ≤ 0.05 dex. Inherits the flat law's committed statements: RC100 slope −1.57σ from its own expectation; CRISTAL R_e fit route DISFAVOURED-over (not robust); R_out fit route and the independent route CONSISTENT (CFG213/220/222), each with its gas-route caveat.
    - RIVAL-LIKE: φ ≥ 0.8 at z = 2.5 and z = 5. Inherits the rival's statements: DISFAVOURED-under on the CRISTAL fit route (R_e and R_out), RC100 −4.80σ from its own expectation; CONSISTENT on the independent route; route-limited.
    - BETWEEN: bracketed by committed laws (the ΛCDM proxy of CFG222 sits at φ ≈ 0.59 at z = 2.5 and ≈ 0.77–0.82 at z = 4.5–5.5, computed from its committed F values 2.16 / 4.52 / 6.20); no committed row scores the curve: NON-DIAGNOSTIC.
- **G3, energy / NEC.** PASS if ρ_DE ≥ 0 and ρ_c ≥ 0 over the whole history and the vacuum stress keeps w = −1 (NEC saturated) with Q ≥ 0. Stated with it, not scored: Q ≠ 0 breaks the Henneaux–Teitelboim shift symmetry (CFG131 D2), so no committed action realises it (OPEN).
- **G4, constants.** Count every constant beyond κ and Ω_c (and Λ). A pre-transfer vacuum amount that replaces Ω_c one-for-one counts 0; ξ, z_t, Γ, a switch shape and a separate remnant each count. A tuned endpoint is reported as a tuning ratio.
- **G5, early-universe limits (all bounds from memory, UNVERIFIED; outcomes conditional on them).**
  - EDE: f_DE(z) = ρ_DE/ρ_tot ≤ 0.10 anywhere in 1e3 ≤ z ≤ 1e5 (the scale of the early-dark-energy literature's allowed peak fraction near z ≈ 3500; tighter near z_rec).
  - BBN / N_eff: at z_BBN ≈ 4.3e8 (T ≈ 0.1 MeV), any extra component ≤ 0.040 of the radiation density (ΔN_eff ≤ 0.3 converted with the standard neutrino factor; 0.3 from memory).
- **Coldness (B, and A where relevant).** The created fluid must satisfy c_s² ≤ 4.6e-12 at k = 30/Mpc (CFG131/CFG156). With Q^μ ∥ u_c and Q independent of ρ_c, CFG131 D1 gives c_s² = (ρ + p) Q_ρ/Q = 0 for dust: PASS BY ASSUMPTION (coldness is allowed, not derived). A2 (Q_ρ ≠ 0) inherits CFG131's dust theorem (δρ_com forced to 0) while the transfer runs: flagged.
- **Rules.**
  - Restatement is not a pass: a pass that is CDM (or the framework's constant Λ) renamed is labelled PASS-AS-RESTATEMENT and adds nothing.
  - A reading equal to a scored object is REDUCES-TO and inherits that object's score.
  - Decision labels: PASS, FAIL, PASS-AS-RESTATEMENT, REDUCES-TO, NON-DIAGNOSTIC.
  - κ = ½ FITTED. No "favours" language. Nothing here says the theory is closed.

## 4. The orchestrator's expectation, tested explicitly

E*: "making the cold mass from dark energy turns a₀ into roughly the rival a₀ ∝ H(z)". Labels:
- HOLDS: some reading that passes G1 and makes the cold mass (F_made ≥ 0.5, or B's full mass) has φ ≥ 0.8 at z = 2.5 and 5.
- HOLDS-ONLY-OUTSIDE-G1: φ ≥ 0.8 only in G1-failing cases.
- PARTIAL-SHAPE: a₀ rises with z (same sign as the rival) but φ < 0.8 at z ≤ 5 even at the largest F_made the form allows.
- DOES-NOT-HOLD: φ < 0.1 everywhere.
Both the z ≤ 5 values and the high-z asymptote are reported.

## 5. Hand predictions (before any number; scored as right/wrong, kept either way)

- P1: A1 at F_made = 0.03 needs ξ ≈ 0.035 and gives a₀(5)/a₀(0) ≈ 1.03 (FLAT-LIKE, fails CFG131's 1% line).
- P2: A2 at F_made = 0.03 needs ξ ≈ 0.0042 and gives a₀(5)/a₀(0) ≈ 1.05–1.06 (FLAT-LIKE, fails the 1% line).
- P3: A1 makes all the cold mass after recombination (F_made = 1) at ξ ≈ 0.84; φ(5) ≈ 0.35–0.40.
- P4: B-inst's minimum EDE fraction at z_t: ≈ 0.64 (1100), 0.42 (3423), 0.03 (1e5), 3e-5 (1e8); remnant ratio ρ_Λ0/ρ_DE(z_t) ≈ 1/(0.387 (1+z_t)³): 2e-9 (1100), 3e-24 (1e8).
- P5: B-pow with ξ < 3 creates only ρ_c(z_t) = ξ ρ_Λ0/(3 − ξ), far below the needed ρ_c0 (1+z_t)³: it cannot make the mass.
- P6: E* = PARTIAL-SHAPE (only outside G1); inside G1 every (A) curve is FLAT-LIKE; (B) is exactly flat.
- P7: (B) = PASS-AS-RESTATEMENT on G1 and G2 for z_t ≳ 3e4: CDM with a vacuum origin story, NON-DIAGNOSTIC in linear cosmology (the GDM theorem).
- P8: (C) fails: the vacuum energy inside R500 is ~1e-3 of the cluster's cold mass, and a localised Q is forbidden by CFG131 D1 for a Lorentz-invariant vacuum.

## 6. Script and controls

- `CFG253_dark_energy_to_cold_mass/CFG253_background.py`: sympy checks (closed forms for A1, A2, A3; the G1 identity; B-inst bound; B-pow creation integral), numerical background ODEs for (A) and (B), the (C) budget; writes `CFG253_background.out` and `CFG253_background_results.json`; exit 1 on any load-bearing failure.
- Controls (must pass in the main run): numerics reproduce each closed form to ≤ 1e-7; Q = 0 reproduces ΛCDM; the A3 solver reproduces CFG131's |ξ| = 0.0275 within 5% (normalisations differ: CFG131 anchors ρ_c a³ at z = 999).
- **MUTATE=1** (separate outputs `_MUTATE1`): Q ≡ 0 in every reading. ρ_DE must be constant and a₀ flat to 1e-10 (checked), and the load-bearing claims "the G1-tolerance transfer gives a nonzero a₀ rise" and "B makes the cold mass from the vacuum" must FAIL (exit 1).
- **MUTATE=2** (`_MUTATE2`): the tie replaced by a₀ ∝ H(z). The load-bearing claim "(A) at the G1 tolerance is FLAT-LIKE" must FAIL (exit 1).
