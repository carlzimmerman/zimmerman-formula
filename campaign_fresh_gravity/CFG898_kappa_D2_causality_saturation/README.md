# CFG898: κ door D2, saturating the drift-causality bound. NOT A SELECTION

**Bottom line.** Making the gated drift exactly luminal at a declared locus does not select κ.
- **The mass-free cells form a MENU of misses.** Saturating CFG893's ceiling at loci defined by ρ_DE alone gives κ = 2.89 to 10.95
  over the 18 declared cells. All of them miss the data window on both footings: p_data = 0 and p_exact = 0.
- **The real drift never comes near the ceiling there.** With the field actually present at those loci, the drift reaches only
  10⁻⁴ to 10⁻³ c. Saturation would then need a relativistic rotation speed, and the implied κ depends on galaxy mass (∝ M_b⁻¹,
  10¹¹ to 10¹⁷): MASS-DEPENDENT, EXCLUDED.
- **α is not fixed from first principles.**
  - The Israel–Stewart closure sets no bound on α at all.
  - The record's α ≲ 1 depends on the convention β = 1.
  - A one-relaxation-time hypothesis gives 1 or 1/√2, depending on the collision model.

**Against the three requirements:**
- (i) A pure number: per cell only.
- (ii) Free of galaxy mass and of density choices: **no**. The κ value depends on which locus, kernel and α are chosen, and the
  realized field is mass-dependent.
- (iii) A second independent prediction: **no**, as declared before computing.

**Outcome class: MENU (every entry a MISS).** The α source is a TRADE in β. The realized branches are MASS-DEPENDENT. κ = ½ stays
FITTED.

## Standing facts

- κ = ½ is FITTED. CFG493 measured κ_Λ = 0.417 ± 0.095 (ρ_DE footing) and κ_crit = 0.345 ± 0.078 (ρ_crit footing).
- The footings, 9.3603e-11 and 1.1312e-10, are never pooled.
- No de Sitter–Unruh argument is used. GF2's ½ is the SIS ratio, not κ.
- Cold energy is real gravitating mass; no particle species is involved.
- This lane does not claim "theory closed" and runs no knob scan: the 18 cells were declared before any computation.

## Files and runs

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (6e61f00b7).
- **Script:** `cfg898.py` (sympy, numpy and scipy; one process, about 10 s, 117 MB peak).
  - `OMP_NUM_THREADS=1 nice -n 10 python3 cfg898.py` writes `cfg898.out` and `cfg898_results.json`. 19/19 checks pass, exit 0.
  - `CFG898_MUTATE=1 …` writes `cfg898_MUTATE.out` and `cfg898_results_MUTATE.json`. All 5 teeth bite, exit 1 by design.
- **Read-only input:** CFG893's results JSON, for c_ν, the structure of the R12 table and f_b. f_b enters only K3.
- Nothing was downloaded, and no other lane was edited.

## What was computed

**Mechanism.** CFG893's ceiling is |v_s|/c ≤ α c_ν κ √(ρ_DE/(4π ρ_loc)). Setting it equal to 1 at a declared locus ρ* gives

  κ = √(4π ρ*/ρ_DE) / (α* c_ν),

where c_ν = 0.64761 for ν_mono (at y = 2.540) and 1 for the simple kernel.

**The declared choices:**
- **Loci:**
  - L1: ρ* = ρ_DE.
  - L2: ρ* = 2ρ_DE, the zero-gravity surface (equivalently, the maximum turnaround radius).
  - L2b: ρ* = 2ρ_DE/3, the local density at that surface for an r⁻² profile.
- **α\*:**
  - A: the record's causal bound, saturated at α* = 1.
  - B1: a Fokker–Planck one-relaxation-time hypothesis, α* = 1.
  - B2: a BGK collision model with τ_c = τ_π, α* = 1/√2.

| α* | L1 ν_mono | L1 simple | L2 ν_mono | L2 simple | L2b ν_mono | L2b simple |
|---|---|---|---|---|---|---|
| 1 (A, B1) | 5.474 | 3.545 | **7.741** | 5.013 | 4.469 | 2.894 |
| 1/√2 (B2) | 7.741 | 5.013 | 10.948 | 7.090 | 6.321 | 4.093 |

- **Spread and window.** The spread is 8.05, against a window width of 0.380 on ρ_DE and 0.312 on ρ_crit, so the set is a MENU on
  both footings.
- **The ρ_crit footing.** Relabelling the loci in ρ_crit units gives the same numbers. Converting at the end with κ√Ω_Λ gives 2.40 to
  9.06. Both have p_data = 0.
- **The canonical cell** (L2, ν_mono, α* = 1) gives κ = 7.741, a MISS by a factor of 15.5 in a₀.
- **What a window landing would need:**
  - either α ≥ 4.8–12.8, above the record's causal maximum of 1.186;
  - or a luminal locus at ρ* = 0.004–0.020 ρ_DE.
  With the simple kernel and α = 1, κ = ½ would need ρ* = ρ_DE/(16π), which is just G ρ_DE c² = 4a₀² (the target) restated.

## Why it fails: three structural reasons

### 1. The ceiling is attained only deep inside galaxies, never at a ρ_DE locus

CFG893's mass-free ceiling replaces the drift field |∇ψ| by its global maximum, c_ν a₀. That maximum is reached only at
y = g_N/a₀ = 2.540, inside the baryonic galaxy, where ρ_loc ≫ ρ_DE.

At a locus defined by ρ_DE, the deep-regime field gives (K7, sympy):
- v/c = α V_f/c at L1 and L2b;
- v/c = α V_f/(√3 c) at L2;
- where V_f⁴ = G M_b a₀.

In the saturated relation a₀ = c⁴/(α⁴ G M_b) (9c⁴/(α⁴ G M_b) at L2), **ρ_DE and κ both cancel**. So luminal drift at a ρ_DE locus
means V_f = c/α: a system with a relativistic rotation speed, i.e. a Hubble-mass object.

- **Exact kernels (point mass).** κ_sat = 3.3e11 to 1.2e17 over M_b = 1e8 … 1e12 M_⊙, with d ln κ/d ln M_b = −1.0000 in every
  branch. That is MASS-DEPENDENT and EXCLUDED.
- **At the fitted κ** (report-only), the realized drift at the loci is v/c = 6.4e-5 to 1.1e-3. That is 6e-4 to 1.2e-2 of the ceiling
  there, at radii of 0.5 to 6 Mpc and y = 4e-7 to 6e-5. The exact kernels agree with the deep form to 1.5e-3 (K8).
- **L3** (ρ* = ρ_ph at y = 2.540) gives a₀ = 16π² c⁴ h²/(α⁴ c_ν⁴ G M_b), with h = 0.16426. This is κ-free and mass-dependent; the
  implied κ is 7.9e12 to 7.9e16.

### 2. At loci defined by ρ_DE, saturation is an H-type relation

- **Rewriting** (post-freeze, report-only). With H_Λ² = 8πGρ_DE/3 used only as a rewriting, the saturated relations are
  a₀ = N c H_Λ/(α* c_ν), with N = √6/2 (L1), √3 (L2) and 1 (L2b).
  - So door D2 at such loci is the familiar "a₀ ~ cH" identification (excluded class X3), with the O(1) factor set by the choice of
    locus.
  - It is also of the c × free-fall-rate family X7: a₀ = c√(4πGρ*)/(α* c_ν).
- **π-parity rules out ½.** With the simple kernel, κ² ∈ ℚ·π¹ (odd); with ν_mono, c_ν is transcendental (class cont). Exact ½ is
  impossible in every cell (I8).
- **An identity, not an input.** The L2b/simple ceiling at the fitted κ prints as 0.1727. That number is κ/√(8π/3) = a₀/(cH_Λ) by
  construction.

### 3. α is not fixed by the Israel–Stewart closure

- **No IS bound on α.** In CFG638's IS form, α enters only the relaxation source. The characteristic speeds are u and u ± √(3P/ρ),
  with dA/dα = 0. At large k the phase speeds are ±1.732051 σ for α = 0.03, 1 and 30. The IS shear front speed² is
  η/(ρτ_π) = p/ρ (K4).
- **The record's "α ≲ 1" comes from the damped-ψ causal completion.** Routh–Hurwitz gives Γτ_ψ < 1, i.e. αβq < 1, so
  α_max = 1/(βq) (K3; 1.18642 at q = 1 − f_b reproduces CFG542 K9). α* = 1 needs the convention β = 1 together with q → 1, so
  source A is a TRADE in β (dα_max/dβ ≠ 0).
- **Kinetic one-relaxation-time hypotheses** (K6):
  - If the drift is the overdamped response to −∇ψ under friction in the baryon frame, the mobility is 1/γ.
  - Fokker–Planck (γ = α/τ) then gives α* = 1 (B1).
  - BGK with τ_c = τ_π = τ/2α gives α* = 1/√2 (B2).
  - Both are added hypotheses. CFG638's own operator relaxes toward the cold energy's own mean velocity, which gives no mobility.
  - Without such a hypothesis α is FREE: the Fokker–Planck stationary state does not depend on the mobility (K5, reproducing
    CFG542 K5).

### Loci tied to ρ̄_m

These are the cosmic mean, the present-day turnaround and the catchment edge. They give κ = 2√π √(Δ Ω_m/Ω_Λ)/(α* c_ν), which:
- needs the forbidden Ω_m/Ω_Λ (X13);
- runs as (1 + z)^(3/2), failing S8.
They are VOID as selections. CFG893's table already gives their numbers (1–12).

## Second prediction (S4)

There is none. Beyond κ, saturation fixes only:
- the luminal density, which is the chosen locus by construction;
- the drift-speed profile v/c = √(ρ*/ρ_loc).
The cold-energy drift is not observed directly, so neither can be tested. S4 was declared FAILED in the frozen criteria, which
capped the outcome below EXACT CANDIDATE.

## Checks and MUTATE

**19/19 PASS.**

K-tests:
- K1: c_ν = 0.64761024 at y = 2.5396, matching CFG893 (tolerance 1e-6); the simple kernel's supremum is 1.
- K2: the CFG893 R12 table scales as √Δ/c_ν, with a relative spread of 2e-16.
- K3: Routh–Hurwitz and 1.186.
- K4: the IS characteristics do not depend on α.
- K5: the stationary state does not depend on the mobility.
- K6: B1 = 1, B2 = 1/√2.
- K7: the deep realized loci, with ρ_DE cancelling and mass exponent −1.
- K8: exact kernels versus the deep form, 1.5e-3.
- K9: the phantom-density closed forms (1e-12), and L3.
- K10: dimensions.
- K11: classifier controls.

Identity checks:
- I1: no forbidden constant appears in the script.
- I2: κ = 2√π √r/(α* c_ν), with zero dependence on G, c, ρ_DE and ħ.
- I3: invariant under scaling.
- I4: renaming the law's κ to 0.4 leaves every cell unchanged (no cell is near 0.4; the smallest is 2.894).
- I5–I7: no Friedmann relation, the declared footing only, no ħ.
- I8: π-weights.

**MUTATE: 5/5 teeth bite, exit 1.**
- M1, α* → 2α*: every cell scales by 0.5.
- M2, ν_mono → simple: the ν_mono cells scale by c_ν.
- M3, 4πG → 8πG: every cell scales by √2.
- M4, w = −0.9: L2 and L2b scale by √0.85, and L1 does not move.
- M5, D = 5: L1 scales by √(4/3), L2 by √(2/3), and L2b stays at 1, as declared.
- The mutated ranges are 1.45–15.5, and all of them have p_data = 0.

## Disclosures

- **Edits before the first run.** The script was edited before it was first run:
  - overflow guards were added to the ν_mono functions;
  - K4's linearised relaxation matrix was written cleanly;
  - the lower end of the realized-branch bracket was set to κ = 0.1, where the L1 locus exists;
  - an I1 hit was removed: a print of the measured κ in the script header.
- **Two additions after the first complete run, neither changing a verdict number:**
  - the summary line now computes the realized κ range from the data. The hard-coded "1e11–1e15" was wrong; the actual range is
    3.3e11 to 1.2e17.
  - the H-type reading (§2) was added. It is labelled post-freeze and report-only.
- **K9's test acceleration** is an arbitrary 3.0e-10 m/s², not a footing value.
- **Inherited assumption.** The ceiling assumes the one-sided deficit in spherical symmetry (CFG893's assumption). With the
  two-sided deficit, |∇ψ| is not bounded by c_ν a₀, which leaves the saturation principle even less defined.

## Suggested register row (for the orchestrator; CFG894's register was not edited)

`K5xx,CFG898,CAUS,campaign_fresh_gravity/CFG898_kappa_D2_causality_saturation/cfg898.py,"door D2: saturate drift-causality
ceiling at rho_DE-defined loci; alpha* from causal bound / one-relaxation-time",,2.894;3.545;4.093;4.469;5.013;5.474;6.321;7.090;7.741;10.948,menu,0,"MENU all MISS
(p_data 0, p_exact 0); alpha TRADE in beta; realized field MASS-DEPENDENT (kappa ~ M^-1, 1e11-1e17); H-type a0 = N cH_L",<commit>`

κ = ½ is FITTED. Not theory closed.
