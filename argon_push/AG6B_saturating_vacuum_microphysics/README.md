# AG6B: which microscopic medium saturates the vacuum polarization, and does physics pick n? **CANDIDATE: physics does not pick n**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (dbcaeba9e), before any script or number.
- **Settings:** κ = ½ FITTED; both footings, never pooled; no particle species; not theory closed.
- **Runs:** both beside the live 1024³ job.
  - `OMP_NUM_THREADS=1 nice -n 10 python3 ag6b_media.py`: 6 s, 0.13 GB, exit 0. Writes `ag6b_media.out` and
    `ag6b_media_results.json`.
  - `... python3 ag6b_sparc.py`: 3 s, 0.42 GB, exit 0. Writes `ag6b_sparc.out` and `ag6b_sparc_results.json`. Its imports of
    CFG4_common, CFG695, CFG4 and AG4b are read-only.
  - `AG6B_MUTATE=1` makes both scripts exit 1, as designed. Every tooth bites (Mu1–Mu4, Mu6, Mu7 in media; Mu5 in sparc), with
    `_MUTATE` outputs.
- **Controls:** all PASS.
  - K1: the numerical-inversion SPARC solver reproduces CFG695 S2, 0.100908 @ 0.60 and 0.099434 @ 0.55.
  - K2: CFG4 ν_mono is reproduced.
  - K3: the AG4b n=2 scan is reproduced, 0.108272 @ 0.70 and 0.103549 @ 0.65.

## Verdict
**CANDIDATE.** Three natural media pass every gate: A1 criticality, A2 deep law, A3 capacity, A4 stability, and A5 the raw-SPARC
C2 line on both footings.
- **Incoherently pumped single-occupancy cells** (Langmuir / Michaelis–Menten) give **n = 1 exactly**: the action's law.
- **The Deser–Levin / relativistic-dispersion quadrature** (Milgrom 1999's ΔT; also mass action) gives **n = 2 exactly**.
- **Critical cells with a maximum-entropy (exponential) capacity spectrum** fall outside the family: n_cap = 2, n₁ = 4/3.

So "a saturating vacuum" does not single out n. The capacity is fixed only once the microscopic process is chosen. None of the
natural media fixes a₀ from Λ: both horizon-tied versions fail SPARC. Not a derivation.

Two attached results:
- **Scoped no-go T-A.** Every analytic dielectric fails: Langevin, Brillouin (including the thermal two-level tanh), Landau
  ferro/paraelectric, Born–Infeld, Euler–Heisenberg, Ginzburg–Landau depairing and the polymer chain. Their deep law is
  g_N ∝ g³ (point-mass V ∝ r^{1/6}, no BTFR). This corrects the "Langevin-type dielectric saturation" analogy in CFG695's reading
  §1, as a proposal only; CFG695 is not edited.
- **Bound T-F2.** In a finite-capacity cell vacuum, every capacity spectrum with non-decreasing hazard (every log-concave one)
  gives n_cap ≥ 2. The action's n = 1 needs a heavy-tailed, decreasing-hazard spectrum with a c⁻³ tail.

## Table: medium → law → n → gates → second prediction
x = g/a₀. "R" is the medium's restoring force (g_N = R(u)); "U" is its polarization at total field g.

| medium (class) | law | n_cap (n₁) | family? | A1–A4 | A5 SPARC (canon / alt) | distinctive second prediction |
|---|---|---|---|---|---|---|
| Langevin, Brillouin J=½,1,3/2, FJC chain (A) | U = 3g_T L(g/g_T) etc., odd analytic | n/a | no | **A2 FAIL**: g_N ∝ g³ | not scored | rising V ∝ r^{1/6} |
| Landau critical, Euler–Heisenberg (A) | R = b u³ | no capacity | no | **A2 FAIL** (g³) | not scored | same |
| Born–Infeld, field-limited branch (A) | U = bg/√(b²+g²): critical and saturates | a₀/b | no | **A2 FAIL** (g³) | not scored | saturates, but the deep law is wrong |
| GL superfluid depairing (A) | U = g(1 − g²/v_c²) | turns over | no | A2, A3, A4 FAIL | not scored | — |
| 1D degenerate Fermi carriers (B) | W ∝ n³ ⇒ R = u²/a₀ (the SI cubic from 1D Pauli) | none | no | A3 FAIL | = CFG690 SI law (FAIL, Υ band) | — |
| 2D / 3D Fermi; massless EH D=4,5 (B) | R ∝ u, u^{2/3}, u ln u, u^{3/2} | none | no | A1 or A2 FAIL | — | — |
| thermal boson zero-mode cubic (B) | R = −(…)u² | none | no | **A4 FAIL** (anti-restoring) | — | — |
| **Langmuir / pumped two-level cells (C-1 = Caughey–Thomas β=1)** | U = a₀g/(a₀+g); R = u²/(a₀−u) | **1 (1)** | **yes** | PASS | **0.1009 @ 0.60 / 0.0994 @ 0.55 PASS** | relaxation Γ ∝ 1 + x; tail a₀/(1+x) |
| Hill h≠1, coherent Rabi pump, CT β≠1 (C) | non-critical or g^{1+β} | — | no | A1 or A2 FAIL | — | — |
| thermal Fermi cell, \|g\|-displaced (C-6) | two scales | 2θ₀/(2θ₀−1) ∈ (2, ∞) | no | PASS | not scored (n free) | — |
| Unruh–Langmuir, a₀ = a_H = Z a₀ (C-5) | C-1 at 5.79 a₀ | 1 | yes | PASS | **0.1786 @ 0.30 / 0.2053 @ 0.30 FAIL** | scale ×Z |
| 1D tight-binding Pauli channels (D-1) | R = 2t(1 − cos πu/u_m) | u_m/(π²t), free | no | PASS | not scored (n free) | hard saturation at finite g_N = 4t |
| **Deser–Levin / relativistic / mass action (E-1)** | g_N = √(g²+m²) − m, with m = a₀/2 from A2 | **2 (2)** | **yes** | PASS | **0.1083 @ 0.70 / 0.1035 @ 0.65 PASS** | relaxation Γ ∝ √(1+4x²); tail ≈ a₀/(8x) |
| Milgrom literal scale, m = a_H (E-2) | E-1 at 11.58 a₀ | 2 | yes | PASS | 0.2665 / 0.3002 FAIL (equation-book control) | scale ×2Z |
| **MaxEnt ⟨c⟩: exponential cells (F-1)** | U = (a₀/2)(1 − e^{−2x}) | **2 (4/3)** | **no** (log wall) | PASS | **0.1031 @ 0.66 / 0.1004 @ 0.61 PASS** | exponential approach to capacity |
| MaxEnt ⟨c²⟩: half-normal cells (F-2) | erfc form | π (2) | no | PASS | 0.1122 @ 0.74 / 0.1063 @ 0.69 **FAIL** | — |
| uniform cells (F-3) | g − g²/a₀, then flat | 4 (2) | no | PASS | 0.1193 @ 0.78 / 0.1121 @ 0.73 **FAIL** | — |
| identical cells (F-4) | min(g, c₀) | — | no | A2 FAIL | — | — |
| in-family spectra as superstatistics (F-5) | Lomax(2) for n=1, half-t₂ for n=2 | 1, 2 | yes | — | inherits | **by construction** (mixing shape chosen) |

## What the computation shows
1. **The law needs a response that is non-analytic in the field vector.**
   - Any isotropic medium analytic in **g** has g − U = −χ₁g³ − χ₂g⁵ − …: odd powers only (T-A, sympy).
   - Criticality then gives g_N ∝ g³, never g²/a₀.
   - Every passer instead responds to the magnitude |g| with an even, quadratic leading correction. The pumped cells fill at a
     rate ∝ |g|. The quadrature is the kinetic energy of "momentum" |g|. The cells clip one-sidedly.
   - Saturation itself is easy; the obstacle is the deep limit.
2. **Inside each natural family, the deep law fixes n with no freedom left.**
   - Langmuir: A1 forces the pump exponent p = 1 (U′(0) = ∞ at p = ½, 0 at p = 2). Criticality then sets capacity = saturation
     field, and A2 sets both to a₀, giving n = 1.
   - Caughey–Thomas: A2 forces β = 1 (deep power 1 + β), again n = 1.
   - Quadrature: A2 forces m = a₀/2, giving n = 2.
   - So n=1 is "two processes in series" (1/u = 1/g + 1/a₀), and n=2 is "addition in quadrature" (relativistic dispersion,
     de Sitter–Unruh temperature, mass action).
3. **Asymmetry, reported with no verdict weight.**
   - The quadrature and the Pauli lattice are critical automatically: kinetic energy and a band bottom have no linear term.
   - The Langmuir, cell and analytic media need their linear susceptibility set to exactly 1. The frozen rule counts this as
     inherited from the action's self-gravity cancellation.
4. **Finite-capacity cells are universal, so they do not by themselves pick anything.**
   - Any admissible law equals a critical clipping ensemble with p(c) = −U″(c) (T-F1).
   - A2 ⇔ p(0) = 2/a₀: a₀ measures the density of nearly-full cells, not the mean capacity.
   - n_cap = 2/(p(0)⟨c⟩).
   - Fixing p by maximum entropy gives exponential cells: n_cap = 2, outside the family, passing SPARC. Fixing ⟨c²⟩ (half-normal,
     π) or using flat cells (4) fails A5 on the canonical footing.
   - The family members are superstatistical mixtures with a chosen shape, so they count as by construction.
5. **The whole family is a queue.** R_n = (u_max²/a₀)·ρ²/(1−ρ), with ρ = u/u_max: the M/M/1 mean queue length. Here n = a₀/u_max is
   a ratio of two scales, which the queue does not fix (T-Q).
6. **Scale.** Tying the saturation field to the horizon acceleration fails SPARC on both footings:
   - Unruh-pumped cells give a₀ = cH_Λ (Z = 5.79 too large).
   - Milgrom's literal quadrature gives 2cH_Λ (2Z = 11.6); this is the equation book's known result, re-run as a control.

   κ stays fitted.

## Discriminating predictions (frozen rule: largest ratio; none TESTABLE NOW)
| pair | static laws differ by (after a₀ rescale) | largest separation | others |
|---|---|---|---|
| n=1 (Langmuir) vs n=2 (quadrature) | ≤ 0.031 dex | high-field tail at g = 10a₀: ×7.3 (0.091 vs 0.0125 a₀) | capacity ×2 (Σ̄_max 214/258 vs 107/129 M☉/pc²); P-wave gap R′ at 10a₀: 120 vs 800; kinetic Γ(10a₀)/Γ(0): 11 vs 20; g_N at 99% capacity: 98 vs 24.5 a₀ |
| n=2 vs MaxEnt exponential | ≤ 0.011 dex | tail power-law vs exponential (×1.2e7 at 10a₀, but both tails ≤ 0.013 a₀) | same capacity; gap R′ at a₀: 8.47 vs 6.39; g_N at 99%: 24.5 vs 1.8 a₀ |
| n=1 vs MaxEnt exponential | ≤ 0.026 dex | tail ×8.8e7 at 10a₀ | capacity ×2 |

- The capacity and tail are measurable in principle, through the inner, high-field phantom of late-type discs. That needs strong
  lenses with kinematic M/L (the AG4c census: not on disk, so NOT diagnostic with SPS M/L).
- The P-wave gap ω₀² = 4πGρ_c R′(u) and the kinetic relaxation law need time-dependent fields, which have no data path now.
- The dynamical predictions carry a free ρ_c or Γ₀. Only their field dependence is predicted.

## Caveats and disclosures
- **Implementation fixes after the first run (frozen checks unchanged).**
  - The A4 numeric check moved from float64 to 40-digit mpmath. Underflow of e^{−2x}, and cancellation in coth differences, had
    faked A4 FAIL for F-1, F-2 and Brillouin.
  - The R-form A2 now tests "achievable" (power 2, positive coefficient), as the criteria define it, instead of a literal 1/a₀.
  - C-6 was re-parameterised by θ₀ (cosmetic).
- **Static-law comparison variable.** It is evaluated at fixed g_N over g_N/a₀ ∈ [0.01, 100]. The criteria wrote "x ∈ [0.01, 100]".
- **T-F2.** The general statement is the hazard-rate argument printed in the output. sympy checks only the equality case; six IFR
  spectra are checked numerically.
- **"Natural" carries modelling choices.**
  - C-1 assumes an incoherent pump ∝ |g| (Unruh-temperature-like), not derived.
  - E-1 uses Milgrom's inertia ∝ ΔT ansatz, which the repo's dS-Unruh review calls unproven.
  - F-1 assumes maximum entropy over capacities.
- **Overlaps cited, not re-run:**
  - CFG690: the SI cubic and its interpolation;
  - CFG695: the saturation, post hoc;
  - the equation book: Milgrom 1999 eq. 9 ↔ n=2, 2cH_Λ excluded;
  - MI_KERNEL_FROM_DSUNRUH: Deser–Levin temperature;
  - the condensate μ-pincer: the Berezhiani–Khoury superfluid and v9 DBI;
  - CFG117: Verlinde;
  - CFG665: Born screening;
  - AG4b/AG4f: n and a₀ are degenerate on SPARC.
- **Not verified in primary texts** (recalled; no web fetch made):
  - the Caughey–Thomas form;
  - the sign of the high-T bosonic cubic;
  - the |eE|^{D/2} massless EH scaling (dimensional analysis);
  - the Stoner–Wohlfarth hard-axis response;
  - superstatistics as named by Beck–Cohen.

  Deser–Levin and Milgrom 1999 were verified earlier in the repo (equation book), not here.
- **Not done here:**
  - C-6 and D-1 have one free dimensionless number each, so they were not scored on SPARC (no knob scans).
  - No ALMA seal for F-1. It sits within 0.011 dex of n=2.
  - Nothing is committed beyond the criteria.
