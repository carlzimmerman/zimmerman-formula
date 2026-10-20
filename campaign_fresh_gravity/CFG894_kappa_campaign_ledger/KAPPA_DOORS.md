# κ doors: what is genuinely untried (CFG894, 2026-10-20)

**Bottom line.** I could find only five genuinely untried derivation routes, all low prior. The record holds about 440 earlier
attempts (see `KAPPA_ATTEMPTS_LEDGER.md`), and four structural walls now constrain any new one. A list of 10–20 would have to
relabel closed doors, so this file gives:
- **5 prerequisites:** lanes that are registered but unrun, or record conflicts that must be settled first;
- **5 new doors**, ranked;
- **17 excluded candidates**, each with the reason, so that nobody spends a lane on them.

κ = ½ is FITTED. No door below is expected to produce ½. Each one is written so that it closes cleanly if it fails.

## The four walls (any route aimed at κ must clear all of them)

1. **c is required** (CFG893, 131bedf33).
   - {a₀, G, ρ} have no dimensionless group.
   - The c-free cold-energy system is invariant under S_λ (x → λx, M → λ³M, a₀ → λa₀). Any c-free balance therefore makes a₀
     depend on galaxy mass or holds for every a₀.
   - c must enter through a horizon, the background expansion, a relativistic completion of the action, lensing or causal
     propagation.
2. **π-parity** (CFG263, L4/LN5, RT-12).
   - A route built from a₀ and H alone gives κ² ∈ ℚ·π^odd, so never ½. The same holds for any dS-invariant vacuum, which
     enters only through Λ = 8πGρ/c².
   - Such a route can still land on an O(1) value such as 0.461 (Z = 2π). Today's data cannot tell that from ½.
3. **ħ-freedom** (RT-18, CFG264). a₀ carries no ħ. The Bekenstein–Hawking ¼ carries ħ⁻¹ and cancels only inside ratios of
   entropies.
4. **The zero mode and reparametrisation.**
   - In a local classical action the vacuum constant can be shifted freely (k01, AS067, ARGON01, the sol61 non-selection Lean),
     so something named must fix it.
   - A monotone one-parameter map is a probe, not a derivation (RT-12).

**What the walls imply (a structural observation, not a theorem).** An exact ½ would need a π-free coupling, through c, of the
dark-energy density into the a₀ sector. No GR equation supplies one: Einstein's 8πG, or Poisson's 4πG, is always left over. So
it would have to come from one of two places:
- a dynamical dark-energy field with a non-Einstein portal;
- an identity in which π cancels between two sectors.

A route that cannot reach ½ but derives a data-consistent value (e.g. 0.461) is still worth having. It would replace a fitted
number with a derived one, but under the rules it is CONSISTENT, not significant. Door D3 is designed to test the
observation above.

## Prerequisites (do these before any new door that overlaps them)

| id | what | why first | cost |
|---|---|---|---|
| P1 | Run **p63-C1/C1b/C2/C3** (sonnet55_push/puzzle_32pi/p63_a0_field_coupling/; criteria 2a36f4ae5, errata 5e5a10e33 and a1e430de1; script written, untracked), normal and MUTATE=1, then commit | Already frozen and c-involving: C1 is the cosmic bound charge with saturated 4πGP⁰ = a₀; C3 is the Kaloper–Sorbo ħ audit; C2 is the flux lattice, which is MENU class. Any four-form or a₀-as-field door duplicates it until it has run | light, after the 1024³ chain |
| P2 | Run **p62** (GF1 pin audit, untracked) | Formally closes GF1's "n = 2.000 ± 0.017" (circular: A₀ is the footing value) | light |
| P3 | **KAPPA_LOGIC_2026_10_20.lean** compile | Belongs to the 32π chat. Do not duplicate; wait for it | n/a |
| P4 | Settle **RT-17 versus RT-19**. Reproduce reviews/mi_kernel_measure_from_desitter_2026.py (KMS w↔x, gives κ = 0.4607) and reviews/mi_dsunruh_kernel_package_2026.py (withdraws it for a 4π error, gives a₀ = 2cH_Λ) side by side and locate the factor. Option space {0.4607, 0.921, 0.230, 2.894, 5.79}, declared now | PAPER6 (F04), AS066 and notes still present 0.4607 as a coefficient-free horizon value. If RT-19 stands, the "dS tie gives 0.461" sentence must go everywhere; if RT-17 stands, it is the record's one determinate H-type value inside the window | light, one script |
| P5 | Write one audit note covering Q010, G031, glm53's README and the gemini38 chain, citing AUDIT_GF2 (a755b66ca) and H061 | Four "κ derived" claims were never audited against the standing audits | text only |

## New doors, ranked by information per unit cost

### D1. The stiffness term's own cosmological vacuum (closure door; c via the expansion)

- **Principle.** The stiffness term that rescues Cassini (CFG770: without it the action fails by about 2600–3100×) needs a
  covariant completion.
  - On FRW with a timelike P^μ, it carries energy of order γ(∂ₜP)²/c² ~ γH²P²/c².
  - If the P sector's background energy is the dark energy, κ follows from γ (i.e. from L*), H and c.
- **Starting equations.**
  - FRAMEWORK_EQUATIONS_2026-10-15.md §1: ℒ ⊃ −|∇Φ − 4πG**P**|²/8πG − (γ/2)|∇**P**|².
  - campaign_fresh_gravity/CFG770_cassini_stiff_action/ (L*, K1).
  - CFG694_combined_construction.
  - CFG695_saturating_vacuum (4πG|P| ≤ a₀).
  - CFG820/CFG821: L* ∈ [24 pc, ≳ 1 kpc], dSphs ≤ 22 pc.
- **First computation (sympy, seconds).**
  - Take three admissible covariant structures, declared now: (a) γ∇_μP_ν∇^μP^ν, (b) γ(∇_μP^μ)², (c) the Maxwell form
    (γ/4)F_μνF^μν.
  - Background: flat FRW with P^μ = (P⁰(t), 0, 0, 0), normalised by 4πG|P| = a₀ (p63 convention) or by the tether.
  - Compute T₀₀ and T_ij, impose T₀₀ = ρ_DE c² with w ≈ −1, and solve for κ. Evaluate it across the independent L* window.
  - MUTATE: drop the stiffness term (CFG770's M1). The result must change.
- **Option space.** {κ ~ O(1)·R_H/L*, identity}. Hand expectation, disclosed:
  - (a) and (b) give κ ~ 10⁶–10⁸, which is EXCLUDED;
  - (c) vanishes for homogeneous P, which is an IDENTITY.
  - So p_exact = 0 and p_data ≈ 0.
- **Cost:** light.
- **Why distinct.** CFG807 revived the kernel vacuum (y_t) inside the stiffened action, and p63-C1 uses the saturated bound
  charge. No lane computed the stiffness term's own FRW energy.
- **Value.** It closes "the stiffness term is the dark energy" for good, and it tests a predicted κ range against an
  independently bounded L* (a test, not a trade).

### D2. Causality saturation of the gated drift, with α from kinetic theory (c via causal propagation)

- **Principle.** CFG893 found the one place where κ enters the cold-energy dynamics at O(1), and there c and galaxy mass both
  cancel: |v_s|/c ≤ α c_ν κ √(ρ_DE / 4πρ_loc). κ would be fixed if two things held:
  - α is a pure number from the Israel–Stewart / collisionless closure;
  - some principle makes the drift null (v_s = c) at a locus defined through ρ_DE alone.
- **Starting equations.**
  - campaign_fresh_gravity/CFG893_kappa_from_cold_energy_structure/README.md (R12; c_ν = 0.64761 for ν_mono, 1 for the simple
    kernel).
  - CFG541_cold_energy_equations_precise (C1 speeds).
  - CFG542_dissipative_action.
  - CFG638_cold_energy_fluid_equations (Kn = √2/4α, Re = 4α).
  - CFG639_deficit_gated_mobility.
- **First computation.**
  - (i) Derive α from the BGK / Chapman–Enskog limit of CFG542's dissipative action, and print whether it is a pure number α*.
  - (ii) Declare the saturation loci before computing: ρ_loc = ρ_DE, ρ_loc = 2ρ_DE (the vacuum's active mass), and the phantom
    density at y = 2.540 (ν_mono's c_ν maximum).
  - (iii) Solve for κ at each locus.
  - MUTATE: α → 2α, and ν_mono → simple.
- **Option space.** κ = √(4πρ*/ρ_DE)/(α* c_ν) over the declared loci. That is `cont`/`menu`: p_data ≈ 0.2 per locus, and
  p_exact = 0 unless α* contains √π.
- **Cost:** light.
- **Prior:** low. It adds two hypotheses (α* derivable; saturation at a forced locus).
- **Why distinct.** CFG893 derived the bound but left α free and did not examine saturation. CFG541's C1 cells reach 0.999 of
  the bound only because they are built at it.
- **Watch.** Saturation at a chosen density is a posit, so the best class available is CONSISTENT unless the locus is forced.

### D3. Census of every place c meets a₀ in the record (closure door / theorem attempt)

- **Principle.** CFG893 closed the c-free sector. What remains is to list every place c meets a₀ in the record and classify
  each one, which directly tests the structural observation above. The classes are:
  - an inequality;
  - an identity in κ;
  - H-type (π-parity forbids ½; record the natural value);
  - ρ-type and π-free (a live candidate).
- **Starting points.**
  - CFG893: dark-energy sink, causality, τ_ψ = c/a₀.
  - CFG775: q = a₀/cH∞ relations.
  - FRAMEWORK_EQUATIONS §4: the event-horizon branch.
  - CFG187 (AeST tie); kappa_closure/k04 and deepseek AS651–658 (four-form); XR20 and CFG43 (unimodular); p63 (a₀ as a field).
  - The sol61 clock lanes (G_cosm vs G_N), KS01 (graviton bath) and CFG807.
- **First computation.** A sympy table giving, for each c-term:
  - the π-weight and ħ-weight of κ²;
  - its dependence on free constants;
  - its class.
  The output is N, the number of live ρ-type π-free c-couplings.
  - **If N = 0,** record the result: "no record equation can produce exact ½; that needs a new π-free c-coupling of a dynamical
    ρ_DE outside Einstein's 8πG". Leave the formal version to the 32π chat's Lean work.
  - **If N > 0,** each live term becomes its own frozen door.
- **Cost:** light. It is bookkeeping, about one page of sympy.
- **Why distinct.** L4/LN5 cover about 60 horizon and vacuum principles, and CFG893 covers the c-free sector. Nobody has
  covered the record's own c-terms together.
- **Value.** High: it either focuses every later lane or finds the one live term.

### D4. The record's nodal fermion medium made Lorentz-invariant (v = c) as the vacuum

- **Principle.** The fermion–polarisation candidate gets its cubic |P|³ term from a Dirac-type band with velocity v. Suppose the
  medium is Lorentz-invariant (v = c) and its filled-band energy is the dark energy.
  - Then a₀ (through K = G a₀) and ρ_DE come from one Hamiltonian, and c enters through v.
  - MASTER_COLD_ENERGY_EQUATIONS.md says explicitly that "no calculation links the independent vacuum energy to the force
    coefficients".
- **Starting equations.**
  - sol61_push/cold_production_2026_10_11/mechanism_2026_10_12/EQUATIONS.md: H(k, P), β = N m* h³/(2πv),
    K = α³v/(2N m* a³h³).
  - NODAL_RING_ORIGIN.md.
  - argon_push/ARGON10_four_gaps_2026-10-16 (D1 parameter count).
- **First computation.**
  - Compute E₀(P) for the filled band with a relativistic dispersion and a Lorentz-invariant regulator.
  - Isolate the cutoff-independent part at the medium's cosmological polarisation.
  - Form κ² = a₀²/(Gρc²) with K = G a₀, and print its dependence on N, m*, h, α, a and the cutoff.
  - ħ must cancel (I7). MUTATE: v = c/2.
- **Option space.** A pure number in the `any` class, or a TRADE.
- **Hand expectation, disclosed:** a TRADE. ARGON10 counts at least 6 free directions, and ħa₀/c is 2e-40 of an MeV.
- **Prior:** low. **Cost:** light.
- **Why distinct.** The VM family's vacua are classical kernel constants. No lane has asked whether this medium's own vacuum
  energy is tied to its own force coefficient.

### D5. Gauged carrier and Festina Lente (speculative; c and H via a de Sitter bound)

- **Principle.**
  - The carrier sector's U(1) ((Φ, X) → (e^{iθ}Φ, e^{2iθ}X)) carries a charge bound E ≥ m|Q|.
  - If that U(1) is gauged, the Festina-Lente bound ties charged states to H: m² ≳ √6 g q M_P H in its usual literature form,
    with the reduced Planck mass. Once H² = ρ/(3M_P²) is used, the 8π cancels against the reduced M_P.
  - If the same carrier also sets K = G a₀, κ would follow.
- **Starting points.**
  - FRAMEWORK_EQUATIONS §3a.
  - sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md Supplement A.
  - project_atomos (FS11, the record's only previous swampland use).
  - The bound's exact form must be checked against its primary paper before use. That is a literature check; nothing is
    downloaded today.
- **First computation.** ħ and π bookkeeping only: can any combination of a Festina-Lente-saturated (m, gq) and K be both
  ħ-free and π-free?
  - If not, the door is a CLOSURE in one page.
  - If so, compute κ. MUTATE: use the non-reduced M_P, under which π returns.
- **Option space:** small and discrete (√6-based rationals × π^k).
- **Prior:** very low. It adds three hypotheses: gauging, a swampland conjecture, and the S_bridge that MASTER leaves
  unspecified.
- **Cost:** light.
- **Why distinct.** No κ lane has used Festina Lente.

## Excluded candidates (do not launch; reasons and ledger rows)

| # | candidate | why excluded |
|---|---|---|
| X1 | any c-free balance (virial, Jeans, gate edge, supply, catchment, clump self-gravity, settling) | CFG893 S_λ no-go (K515) |
| X2 | field-energy density at g = a₀ matched to ρ_DE c² ("slot" W_v = 4, ε_tot = 1/32π) | the convention fixes the answer; T1 fails (K010, K014, K126–K128, K225) |
| X3 | further horizon/thermal identifications (Unruh, Gibbons–Hawking, KMS, equipartition, Tolman–Ehrenfest, modified inertia) | H-type: π-parity rules out exact ½; about 60 tried (L4); values cluster on Z ∈ {1, 2, 2π, 6, ½}. Exception: settling P4 |
| X4 | "attractive 4s": vacuum trace T^μ_μ = 4ρc² (a₀² = G·Tr/16 needs an unexplained 16); quadratic Tolman (ρ+3p)² = 4ρ²; four dimensions or four components of P^μ; the BH quarter; 32π = 8π × 4 | numerology in disguise: which side the 4 lands on is a convention (sol61-13, X1, OR3, RT-18) |
| X5 | κ = 1/n with n a channel or polarisation count | retracted class (H061; PD07, H017, kimik3, gemini38, OA1) |
| X6 | SIS or virial ratios σ²/v² = ½ and relatives | a different quantity (AUDIT_GF2; GF2, Q001, Q007, Q010, deepseek_moa) |
| X7 | free-fall surface gravity c²/2R*, R* = c/√(Gρ) | gives ½ only by positing J = 1; no physical object has that radius (RV-07, RV-25, sol61-69, gemini-solve) |
| X8 | four-form / Bousso–Polchinski flux quantisation | fixes Λ only; κ needs the split (FL1, RR-06, agent A) — p63-C2 pending covers the lattice variant |
| X9 | topological / index / η invariant | forced numbers are 0 or 1 or sit in the wrong slot; theorem-grade (K183, RR-41) |
| X10 | kernel-tail or cutoff vacuum integrals (y_t, T) | a trade; turn-off likely excluded by TNOs (p56); class rejected by Cassini (p58); CFG807 blocked |
| X11 | global or sequestering averages of the a₀ sector | five orders short because of the halo filling factor (k02) |
| X12 | closed-form or grammar searches near ½ or Z | base rates: ½ in 0.94% of 852 forms (p60), 10.8% of ≤3-op numbers in band (KS04), 596 forms within 1% of Z (RT-22) |
| X13 | "selecting" κ with measured Ω_m/Ω_Λ, 5.364, H₀ or w₀ | forbidden input; circular (Q002, G052, CFG417, CFG831-ph) |
| X14 | graviton bath / mode counting | slot not live (KS01); gauge-indeterminate, 161× spread (RV-40) |
| X15 | anything inside the unstiffened QUMOND/BIMOND vacuum class | Cassini: κ < 0.17 at 2σ for that class (p58) |
| X16 | deformed dispersion, modified-inertia temperature root | gives 2cH_Λ (OR19, RR-19) |
| X17 | relativistic completions already run (AeST joint, aether/khronon clocks, unimodular tie, four-form, Horndeski class, k-essence attractor) | each closed (OR6, CFG187, sol61 clock lanes, XR20, k04, gated brute force, W11). A new completion must differ structurally: D1 is the one gap found |

## Launch order

1. **P1** (p63, already frozen).
2. **D1** (stiffness-term vacuum).
3. **D3** (the c-term census).
4. **P4** (KMS conflict).
5. **D2** (drift-causality saturation).
6. **D4** (relativistic nodal medium).

After those: D5, P2, P5.

- Take CFG ids only from a reserved block. In the orchestrator's 890–899 block, 891 and 896–899 were unassigned at
  2026-10-20 00:45; check LEDGER.md first.
- Each door commits FROZEN_CRITERIA.md alone first, follows `KAPPA_CAMPAIGN_RULES.md`, and appends its row to
  `kappa_attempts_register.csv`.
