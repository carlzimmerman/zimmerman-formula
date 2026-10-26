# CA1_covariant_self_coupling — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25. Question (PAPER61 OPEN item): is there a covariant field theory for the cold dark energy whose
self-interaction produces the core law, and do a₀ or Λ fix its scales with no new constant? κ = ½ FITTED. Footings
canonical a₀ = 9.3603e-11 / alt 1.1312e-10 m s⁻², graded separately, never pooled. Cold dark energy is a field component
paired with dark energy; where scattering is discussed it is scattering of the field's excitations on its mass shell
(CFG723 B / D5), never a dark-matter particle. Nothing here says the data favour the framework or ΛCDM. Not "theory closed".

## 0. Record read before writing (what this lane inherits)

- **OS1** (71873e76d3): q_f = 0.892 / 0.748 on SPARC alone ⇒ n = 2q − 1 = **0.784 / 0.496** (LN2 `os1_n_values`).
  OS1's rms(q) curve is flat near q_f; OS1 reported clusters at q_f ± 0.05 with the same single miss.
- **LN2**: core condition ρ₀ (s v) t = 1, v = (4/√π)σ, s v = K σ^(1−n), K = 9 σ_ref^(1+n)/(4πG t Σ_a0²),
  Σ_a0 = a₀/(2πG), σ_ref = 70.50 km/s; Kn closed form; DW1 uses t = 13.8 Gyr and Kn > 1 as the long-mean-free-path line.
- **CFG723**: any viable carrier has a mass shell; condensate needs m ≤ 16–143 eV and σ/m ≥ 0.10–0.82 cm²/g to thermalise.
- **CFG725**: merger bound σ/m ≤ 0.708 cm²/g (both footings) at merger speed; CFG725 assumed contact (velocity-
  independent) scattering, which OS1's n > 0 now contradicts.
- **CFG122**: superfluid (Berezhiani–Khoury) door scoped no-go; thermal phase needs m ≥ 1e4 eV, condensed core m ≤ 10 eV.
- **CFG119**: wave-field growth needs m ≥ 1.28e-20 eV.
- **PH1**: no phase criterion from {κ, a₀, G, c, Λ, L★} gives every class its phase.
- Grep of LEDGER / CFG894 / rebuild for Yukawa, mediator, 1/r^p, Born regime: no earlier lane derives a velocity-dependent
  self-coupling for the cold sector.

## 1. Target (fixed by the record; per footing)

The cross-section per mass s(σ) as a function of 1-D dispersion σ, defined through the core condition:

    s(σ) ≡ ⟨σ_T v_rel⟩ / ⟨v_rel⟩,   Maxwellian relative speeds f(v) ∝ v² exp(−v²/4σ²),   ⟨v_rel⟩ = 4σ/√π,
    target  s★(σ) = (√π/4) K σ^(−n),  K = 9 σ_ref^(1+n) / (4πG t Σ_a0²),  t = 13.8 Gyr.

σ_T is the momentum-transfer cross-section (declared convention).

## 2. Frozen candidate menu (nothing added after the run)

| id | covariant interaction (with the dark-energy sector S_DE[φ] alongside) | microscopic σ_T(v) |
|---|---|---|
| C0 | complex or real scalar χ, −λ|χ|⁴ (contact) | constant (s-wave) |
| C1a | Yukawa mediator (scalar g φ|χ|² or vector g A_μ J^μ) with range **tied to a₀ / Λ**: m_φ = ħa₀/c³ (range c²/a₀) and m_φ = ħ√(Gρ_Λ)/c², ρ_Λ = a₀²/(κ²c²G) | Born and classical (attractive / repulsive) |
| C1b | the same Yukawa with **free** m_φ, m_χ, α | Born; classical attractive / repulsive (Tulin–Yu–Zurek fits); Hulthén s-wave (reported only) |
| C2 | **pair exchange of dark-energy quanta** of Hubble range (m_φ ≤ ħ√(Gρ_Λ)/c², so the potential is a pure power law on halo scales): V = C_p / r^p, p fixed by the operator: p = 3 (g|χ|²φ², non-derivative scalar pair), p = 5 (current–current (1/M²) J_χ^μ ψ̄γ_μψ to a light DE fermion pair), p = 7 (shift-symmetric (1/M²)|χ|²(∂φ)², derivative scalar pair); reported only: p = 6 (London) | classical σ_T = A_p (C_p/E)^(2/p), E = μv²/2, for v above the quantum crossover |
| C3 | superfluid / condensate phase of χ (λ|χ|⁴ condensate, phonon-mediated) | condensate hydrodynamics |

Literature formulas (Tulin–Yu–Zurek fits, Hulthén phase, pair-exchange coefficients c_3 = 1/(64π³), c_5 = c_7 = 1/(4π³))
are recalled from memory and PROVISIONAL; they enter only amplitudes and the reported-only rows, never a slope gate of C0,
C1a or C2 (those slopes are exact scaling results certified in Lean).

## 3. Gates (per candidate, per footing)

- **G1 slope.** n_eff = secant −Δln s/Δln σ. G1a over the SPARC span σ = 20 → 200 km/s; G1b over the cluster span
  σ = 400 → 1300 km/s (KT ≈ 1–10 keV). Pass iff |n_eff − n| ≤ **δn = 0.10** on both spans. Derivation of δn: OS1 reported
  the out-of-sample cluster grade unchanged at q_f ± 0.05, so δn = 2 δq = 0.10. Both spans are required because OS1's
  clusters passed at the SPARC q, so the law must continue to cluster speeds.
- **G2 normalisation.** s(σ_ref) / s★(σ_ref) ∈ [1/2, 2]. The factor 2 covers declared order-unity conventions: σ_T vs σ_V
  vs σ_tot, and LN2's "rate × age = 1" (SC1's half-age variant moves the anchor by √2).
- **G3 no new constant.** After imposing G1 and G2, every scale of the candidate (m_χ, m_φ, coupling, C_p, M) must follow
  from {G, c, ħ, a₀, ρ_Λ = a₀²/(κ²c²G), t} with order-unity numbers (integers, small rationals, powers of π, the operator's
  integer p). A required free scale counts as one new constant. A monomial such as c·(a₀t/c)^k with |k| ≥ 2 picked to hit a
  number is numerology and counts as a new constant. For C2 a frozen **no-new-constant assignment menu** is graded:
  M ∈ {E_Λ, E_Pl} × m_χc² ∈ {E_Λ, E_Pl, √(E_Λ E_Pl)}, E_Λ = (ρ_Λ c² (ħc)³)^(1/4), E_Pl = √(ħc⁵/G), couplings = 1;
  G3 passes only if some cell meets G2.
- **G4 Knudsen.** Kn(σ) = (4/√π) t √(4πG ρ₀) with ρ₀ = 1/(s v t) from the candidate's own s, evaluated at σ = 5, 10, 20,
  70.5, 1000 km/s; pass iff Kn > 1 at all (DW1's line). For C3 the condensate needs a hydrodynamic core (Kn < 1 and Γt ≫ 1),
  so C3 passes G4 only if the target's own Kn < 1.
- **G5 merger.** σ_T/m at v_rel = 4700 km/s ≤ 0.708 cm²/g (CFG725).
- **G6 regime validity.** The σ_T formula used must hold over 10–1500 km/s: Born needs α m_χ/m_φ < 0.1; classical needs
  m_χ v/(2ħ) · b ≥ 10 at the deflection impact parameter (reported as the m_χ lower bound it implies); the de Broglie length
  at 10 km/s must be < 30 pc (0.1 of a 300 pc dwarf core); C1a / C2 need the mediator range ≫ 1 Mpc.

C1b shapes depend on one dimensionless variable each (Born: v/v★, v★ = m_φc/m_χ; classical: β_ref); the lane solves for the
set of shape variables that meets G1 (a feasibility solve, not a fit of a theory constant to data). If that set is non-empty,
the required v★ or β_ref is one new constant (G3 FAIL) unless it is given by §3's rule.

## 4. Lane classes (the verdict needs both footings to agree, else UNDECIDED)

| class | rule |
|---|---|
| CA1 CANDIDATE | one candidate passes G1–G6 on both footings |
| CA1 SHAPE ONLY (amplitude needs a new constant) | some candidate passes G1, G4, G5, G6; none passes G3 |
| CA1 FOOTINGS SPLIT | the candidates passing G1 differ between footings (stated alongside the class) |
| CA1 NONE | no candidate passes G1 on a footing |

## 5. Checks

- **K1** s★ at σ_ref reproduces LN2's Kn_ref = (4/(3√π))(2a₀t/σ_ref) to 1e-6 through the G4 formula.
- **K2** For a pure power law σ_T ∝ v^(−k), the thermal average gives n_eff = k to 1e-6 on both spans.
- **K3** Born Yukawa: n_eff → 0 for v ≪ v★ and → 4 (within 0.3) for v ≫ v★.
- **K4** Peak RSS < 1 GB, one thread.
- **MUTATE=1** (separate outputs `_MUTATE`): shift the target n → n + 0.6 (1.384 / 1.096). It bites iff the C2 power selected
  by G1 changes on both footings. Exit 1 if it bites.

## 6. Disclosed before freezing (hand expectations, not results)

- C0 gives n = 0 and C1a gives n ≈ 4 (Coulomb limit), expected G1 FAIL. C2 gives n = 4/p exactly; the integer windows are
  p = 5 for canonical and p ∈ {7,…,10} for alt, so the footings are expected to split.
- Dimensional analysis: from {G, c, a₀, ρ_Λ, t} the only velocities are c·(a₀t/c)^d (Gρ_Λt²)^a, so no halo velocity
  (~70 km/s) appears without a large power. G3 is expected to fail for every candidate; the C2 assignment menu is expected to
  miss by many orders of magnitude.
- C3: LN2's Kn ≈ 650–2000 ≫ 1 is expected to rule out a hydrodynamic condensate core.
- Lean 4 + Mathlib certificates planned: n = 4/p scaling, contact and Coulomb slopes, the integer p windows and their empty
  intersection, the velocity-monomial solution set. MUTATE Lean file changes statements and must fail to compile.
