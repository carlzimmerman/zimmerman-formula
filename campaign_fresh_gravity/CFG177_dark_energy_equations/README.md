# CFG177: the equations of the dark energy in the committed action, and what its "flow" does

**Bottom line.** CFG43's committed action already gives the dark energy a current tᵐ. This is the Henneaux–Teitelboim multiplier, dual to a 3-form, and its time component is the unimodular clock. Its equations are:
- Λ is constant everywhere;
- ∇ₘtᵐ = 1 − P/ρ_vac: the flow's divergence, i.e. its "compaction", is lowered only inside matter whose Lagrangian depends on Λ;
- everything else about the flow is gauge.

So the flow's direction, speed, whether it converges on a galaxy or streams "from the top", and its flux through a sphere are all gauge choices on one solution. The flow carries no stress, does not enter the metric, and has no local degree of freedom. **In the committed action the flow has no new content.**

The minimal addition that makes the flow physical is a 3-form mass term. That gives a thawing quintessence whose flow is its time derivative (a clock field; the vacuum flows down its own density gradient). It has one new pure number s, and it has a flow but no MOND force: the force on baryons is < 10⁻¹⁰ of the law's boost, with the wrong M and r scaling.
- Letting the baryons compact the time flow gives a Newtonian-shaped fifth force, which is Cassini-excluded at β_b = 1.
- The MOND form appears only if a₀ is written into a nonlinear clock law. That is AQUAL in dual variables, and it needs a new constant β_b, does not lens, and is cut off at ≤ 1.43 r_M by the cosmic time current.

κ = ½ stays FITTED. Nothing here says the theory is closed.

## Files, runs, controls

The frozen question is `FROZEN_QUESTION.md`, written before any script. Its hash and UTC time are in `FROZEN_QUESTION_SHA256.txt` (20:53:22Z).
- **Note 1** (the owner's Addendum 2, relayed) was in the file before the hash.
- **Note 2** (the orchestrator's priority on the time-direction reading and the khronon) was appended **after E1–E3 had run and before E4 was written**. It added two items, both in E4: 3h (baryons source the time flow) and 3i (the khronon relation).
- Nothing was committed (the orchestrator commits).

Shared helpers are in `E_common.py`. CFG44's `Bcommon` is imported read-only, with bytecode writing off. Run in this order, because E4 reads E3's main JSON: `python3 E1_…py; python3 E2_…py; python3 E3_…py; python3 E4_…py`. Each run takes under 7 s.

| script | checks | main | control (outputs named by mode) |
|---|---|---|---|
| `E1_ht_current_equations_gauge.py` | 9 | 9/9, rc 0 | MUTATE=1 adds the 3-form mass term. E1-FIELD, E1-NOMETRIC and E1-GAUGE-S fail; rc 1. |
| `E2_static_flow_point_mass_sphere.py` | 6 | 6/6, rc 0 | MUTATE=1 makes the baryons Λ-dependent (β_b = 1). E2-SdS-FLUX fails (the flux gains β_b M/ρ_vac); rc 1. |
| `E3_dynamical_vacuum_current.py` | 7 | 7/7, rc 0 | MUTATE=1 (s < 0): E3-HEALTH and E3-BG fail (ghost; phantom w₀ = −1.037); rc 1. MUTATE=2 (s = 0): D falls back to 2N + 2 and w ≡ −1; three checks fail; rc 1. |
| `E4_static_solution_mond_test.py` | 12 | 12/12, rc 0 | MUTATE=1 is a positive control: the G1 scorer is fed a P2-reproducing force, and E4-G1-DUST flips (ratio 1.000, G1 residual 9e-16); rc 1. |

## Hypotheses

- CFG43's action exactly, with the same conventions: c = 1 in the algebra, M_P² = 1/8πG, ρ_vac = M_P²Λ, ε = κ²/8π.
- The baryons are dust and Λ-independent, and are minimally coupled, as in CFG43. The only exceptions are the declared β_b cases.
- Static and spherical. Explicit metric (−e^{2α}, e^{2β}, r², r² sin²θ), with SdS exact for the point mass. Weak field inside extended matter.
- The cold fluid, when present, is CFG43's cap fluid held at CFG44's target pressure. That pressure exceeds the cap inside r_M, so its effects are upper bounds.
- The P2 kernel is primary and ν_mono is reported. Both footings are used.
- M_b = 10⁹–10¹² M☉; point mass, and exponential spheres with h = 0.5 r_M and h = 3 kpc; x ∈ [0.1, 30].

## The equations, as derived

**The committed action (HT form; E1).** Euler–Lagrange on the explicit metric, with all fields depending on (t, r, θ, φ), gives:

    ∂ₘΛ = 0                                   (Λ is a global constant, whatever the matter)
    ∇ₘtᵐ = 1 − P/ρ_vac                         (P = the cap fluid's pressure, ≤ ε ρ_vac c²; zero for dust baryons)
    Tᵐ ~ Tᵐ + ∂ₙωᵐⁿ,  ω antisymmetric         (= A → A + dλ for the 3-form, Tᵐ = (1/3!)εᵐⁿᵖᵍA_npq; reducible)
    T_μν(vacuum) = −ρ_vac g_μν                 (w = −1; the current term is metric-independent and carries no stress)
    ∂ₘJᵐ = 0,  and Schwarzschild–de Sitter solves the metric equations for any Tᵐ.

- **Physical:** the local scalar ∇·t, which the matter fixes algebraically, and fluxes through closed 3-surfaces, i.e. 4-volumes. Their global zero mode is CFG43's one global pair (Λ and the total unimodular time).
- **Gauge:** everything else. E1-SPLIT constructs four gauge copies of one solution: a clock gauge with no flow, a radial outflow, an inflow converging on the galaxy, and a uniform stream "from the top". It also shows the instantaneous flux through a sphere can be set to any function of time. The invariant is dQ_ball/dt + Flux = ∫_ball ∂ₘTᵐ.

**The minimal promotion, DYN (E3).** Add U = −(σ/2) g_mn tᵐtⁿ, the dual of a 3-form mass term, since A² = −6t². Take σ = s M_P²Λ²; this is the only Λ-power that gives an O(1) slope for an O(1) number (E3-TIEPOWER). Then:

    t_μ = ∂_μΛ/(sΛ²) = ∂_μτ,   τ = −1/(sΛ)          (the vacuum flows down its own density gradient; the clock reads 1/(sΛ))
    ∇_μt^μ = 1 − P/ρ_vac − sΛ t_μt^μ                (the Gauss law: the time flow's divergence, "compaction", sourced by matter)
    ⇔  □φ = V′(φ) − (√s/M_P) P,   φ = (M_P/√s) ln(Λ/Λ₀),   V(φ) = ρ_vac,0 c² e^{√s φ/M_P}
    T_μν = ∂_μφ ∂_νφ − g_μν[½(∂φ)² + V]         (a perfect fluid moving along t^μ; its flow energy is φ̇²/2 = (1+w)ρ_DE/2)

- The dof count is D = 4N: one local dark-energy mode, with the curl part of the flow zero on shell.
- The reduced Hamiltonian is H = ρ_vac + (σ/2)Q² + (∂ρ_vac)²/(2σ), where Q is the unimodular clock density, conjugate to ρ_vac. It is healthy iff s > 0, with c_s = 1.

**As a clock field (E4-KHRONON).** τ obeys □τ − (∂τ)²/τ = 1 − P/ρ_vac. Its level sets, which are the level sets of ρ_vac, form a physical foliation with a khronon-type normal u_μ = ∂_μτ/√(−(∂τ)²). In HT the same foliation is pure gauge.

Unlike a khronon, the action is not invariant under τ → f(τ): the clock's rate is ρ_vac and is physical. Nothing couples to u_μ. Adding the khronon couplings is door 11C (CFG172), where the record's FC-KH, KM1, KM3 and V0 exclusions apply; that is not run here.

## Answers

- **Q1.** Answered above: E1, 9/9. The flow is gauge apart from its matter-fixed divergence and one global number.
- **Q2 (E2).**
  - **Point mass.** SdS has √−g = r² sinθ exactly, so the river-gauge current is t^r = r/3. Its 4-volume per unit Killing time inside the areal sphere r is (4π/3)r³, **independent of M**. The vacuum current passes through a point mass as if it were not there.
  - **Static test body.** It feels exactly −GM/r² + Λc²r/3, with no flow term.
  - **Extended dust.** The only M-dependence is GR's volume distortion. The deficit is 4πGM⟨r²⟩/(3c²) (16πGMh²/c² for the exponential sphere), at most 6 × 10⁻⁶ of the volume.
  - **With the cap fluid at the target pressure.** The deficit, in terms of M_b(<r), is [(4π/3)r³P(r) + (a₀/3)∫₀^r M_b dr′]/(ρ_vac c²). For a point mass that is 3ε/x² of the volume: 3% at x = 1, 3 × 10⁻⁵ at x = 30. CFG43's cap bounds it by ε ≈ 1%.
  - **The cap and CFG43's obstruction.** At the target pressure the local divergence 1 − ε/x² would change sign inside x = √ε ≈ 0.1; CFG43's cap forbids that. This is the same fact as CFG43's obstruction.
  - **Unobservable.** Nothing in the metric responds, so the flow is locally unobservable.
- **Compaction needed (a cross-check of CFG176 Q1f).** To be the phantom, the vacuum would need ρ/ρ_Λ = 17.9 – 5.0 × 10⁶ (canonical P2), and up to 9.6 × 10⁶ over both kernels and footings. HT's Λ is constant, so its compaction is exactly 1.
  - By Raychaudhuri, a compacted w = −1 medium defocuses (ρ + 3p = −2ρ). Mimicking the phantom's focusing with it would need the local vacuum energy to go **negative** by 10¹–10⁶·⁷ ρ_Λ.
- **Q3 (E3, E4).**
  - **DYN background.** For the declared illustration s = κ² (λ = ½; a postulate, not a tie): w = −0.963 / −0.982 / −0.991 / −0.997 at z = 0 / 0.5 / 1 / 2, and w_a = −0.053.
  - **Growth.** D/D_ΛCDM = 0.995. Quasi-static clustering is ≤ 5 × 10⁻⁷ of matter's at k ≥ 0.01/Mpc. s → 0 recovers ΛCDM.
  - **Around baryons.**
    - The dust baryons source δφ only through their potential: ∇²δφ = 2ΦV′ (sympy).
    - The flow's own kinetic response, −Φφ̇², does attract, but weakly. The extra acceleration is ≤ 4.5 × 10⁻¹¹ of the boost over all 48 rows, and ≤ 8.6 × 10⁻¹⁴ with the cap fluid as a source (a bound).
    - It scales as M¹r² (potential term) and M¹r⁰ (flow term), against the deep-MOND M^½ r⁻¹.
    - Reaching the boost at x = 1 needs λ² ≥ 4.6 × 10¹⁹ or 1 + w ≥ 1.1 × 10¹⁰. The first cannot accelerate (the fixed point has w = −1 + λ²/3); the second exceeds 1 + w ≤ 2. So no value of s rescues G1.
    - **Solar System.** Tidal gradient 4 × 10⁻⁷⁴ s⁻².
  - **Time flow compacted by baryons (3h).** Take m ∝ Λ^{β_b}, α = β_b√s. Then G_eff = G(1 + 2α²), a Newtonian 1/r² shape, and γ_PPN = (1 − 2α²)/(1 + 2α²). That gives γ − 1 = −0.67 at β_b = 1, s = κ². Cassini (|γ − 1| < 2.3 × 10⁻⁵, from memory) needs β_b < 4.8 × 10⁻³. The Gauss law is linear in its source for any clock law, so linear sourcing never gives √M.
  - **DAQ scoping.** m ∝ Λ^{β_b} with U = −u₀|t|^{3/2} gives exactly √(GMa₀)/r, for u₀ = (2/3)√(4πGa₀) ρ_vac^{3/2} β_b^{−3/2}. But a₀ has been written into U, β_b is new, and a conformal coupling bends no light.
  - **DAQ in cosmology.** Embedded in cosmology, the Gauss law makes the background current timelike. The local current then turns null at r_c/r_M = 0.64 (β_b = 1), rising to a ceiling of 1.43 as β_b → ∞, where the clock law is singular. So there is no deep tail out to 30 r_M (reported).
  - **Timelike branch.** A healthy continuation to the timelike branch exists, U = −u₀ t²|t²|^{−1/4}; the other continuation is a ghost there (reported).
- **Q4.** HT: no new content. DYN: a dynamical dark energy with a flow but no MOND force. DAQ: a relabelled AQUAL. The constants are listed below.

## Status table

| | items |
|---|---|
| **DERIVED** (sympy / numerics, these scripts) | Every equation in the "Equations" section. Also: the 3-form dual and its reducible gauge; the physical/gauge split and the gauge copies; SdS for any Tᵐ; the M-independent point-mass 4-volume; the GR deficit formula; the cap-deficit identity in M_b(<r); the needed compaction and the w = −1 defocusing; DYN's Friedmann equation and reduced canonical scalar; the Gauss law ⇔ Klein–Gordon; the dual identities (A² = −6t², the Legendre form of −F²/48); the Dirac counts (HT 2N + 2, reproducing CFG43; DYN 4N); health iff s > 0, c_s = 1; the linearised KG, δρ, and the Tolman-zero gradient energy; the DYN force bounds, scalings and inversion; the exponential fixed point w = −1 + λ²/3; G_eff and γ for baryon sourcing; t = dτ and the clock equation; DAQ's deep form, u₀, the lensing invariance, r_c and the branch health |
| **POSTULATED** | CFG43's tie P_cap = εM_P²Λ and its saturating shape (inherited). The 3-form mass term as "the minimal promotion". σ ∝ Λ² (b = 2, justified dimensionally, not derived). s = κ² as the one illustration. Baryons Λ-independent (main) or m ∝ Λ^{β_b} (3h, DAQ). DAQ's U. The factor-3 allowance for the φ̇δφ̇ term. The target pressure as a bound. |
| **FITTED** | κ = ½ (inherited, never derived); Ω_c h² (inherited). **s** would be fitted to w(z) (not done). |
| **OPEN** | The CMB for DYN (not computed). DYN with khronon couplings, i.e. door 11C (CFG172). DAQ's strong-coupling surface at r_c, and its interpolating U. The Koivisto–Nunes correspondence, which rests on the literature form recalled from memory (the identities themselves are verified). The Cassini number (from memory, not re-verified). |

## Door-11 gates

Scored separately, never pooled. HT = the committed action; DYN = the minimal promotion; DYN+β_b = baryons source the time flow; DAQ = the dual-AQUAL scoping.

| gate | HT | DYN | DYN + β_b | DAQ |
|---|---|---|---|---|
| G1 law | **FAIL**: no force at all | **FAIL**: ≤ 4.5 × 10⁻¹¹ of the boost; M¹r² and M¹r⁰ | **FAIL**: Newtonian 1/r² shape | p* at most (restatement); cut at r_c ≤ 1.43 r_M |
| G2 cosmology | PASS (identical to ΛCDM) | background + growth PASS for s = κ² (w₀ −0.963, D ratio 0.995); CMB OPEN; the current runs along the Hubble flow | not computed (baryon-coupled quintessence changes the background) | UNDEFINED |
| G3 reaction / energy | vacuous (no force) | vacuous (≤ 10⁻¹⁰) | not computed | OPEN |
| G4 constants | PASS: none new in the HT sector (CFG43's ν\* inherited) | **FAIL**: s | **FAIL**: s, β_b | **FAIL**: β_b, plus a₀ written into U |
| G5 well-posed / Solar System | PASS: 0 local dof; PPN = GR | PASS: healthy iff s > 0, c_s = 1; 1-AU tide 4 × 10⁻⁷⁴ s⁻² | **FAIL**: Cassini (γ − 1 = −0.67 at β_b = 1) | lensing FAIL (conformal); singular at r_c |
| G6 preferred frame | vacuous (the frame is gauge) | vacuous (nothing couples to u_μ; not computed beyond that) | vacuous | OPEN |
| G7 frame dependence of a₀ | vacuous (no a₀ in this sector) | vacuous | vacuous | OPEN |
| G8 anisotropy | N/A (11C reading) | N/A | N/A | N/A |

## Constants beyond κ and Ω_c h²

- HT: none. The cap fluid's ν\* is CFG43's and is not re-counted.
- DYN: **s**, a new pure number. b = 2 is forced by requiring no new dimensionful constant together with an O(1) slope.
- DYN + β_b: s and **β_b**.
- DAQ: β_b, plus the shape of U, into which a₀ is written.

Each of these is a G4 failure unless derived.

## Stress-energy (Addendum 2)

- HT's medium has no rest mass and is not a particle. It is w = −1 and gravitates only as Λ; its flow carries no stress.
- DYN's medium is a field, not particles: a canonical-scalar perfect fluid moving along t^μ, with ρ = φ̇²/2 + V, p = φ̇²/2 − V, and focusing density 2(φ̇² − V). The flow, meaning its kinetic part, attracts; the vacuum part repels.
- No construction here supplies or removes the cold mass Ω_c h² ≈ 0.12. It stays as in candidate B.

## Relation to other lanes

- This is the door-11 **11C "the top = time"** reading of Addendum 1, made explicit. The HT divergence law is exactly "matter changes the flow's expansion rate".
- It agrees with CFG176's frozen expectations: a Λ cannot flow physically, and the time-direction flow gives ΛCDM's H(z) in HT. The compaction and defocusing numbers cross-check CFG176 Q1f.
- **Do not cite** "the dark-energy current carries M_b(<r)". It does so only through the cap fluid's ≤ ε divergence deficit, and that deficit is locally unobservable.
