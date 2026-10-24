# X14_caustic_completion: are caustics generic for v3s's khronon dust, and is there a caustic-free completion with no new scale?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` + `LITERATURE_MAP.md` (68bf6e379d, committed alone before any script or
derivation result; the class list C1–C9 frozen there). Amendment: **A1 POST-RESULT** (check code only, below). Launched from the
open rows "Soft-side caustics in v3s" and "Dynamical state of moving subsystems" of V3_FULL_PICTURE §6 (X8, X10, X12).
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". No data
comparison; nothing here says the data favour the framework.

## Verdicts

**(i) CAUSTICS GENERIC (shown analytically).** Every condition of FROZEN §5(i) holds (`verdict_i`; 24/24 checks).
- v3s's khronon flow is exactly irrotational, and in the zero-charge limit it is mimetic (geodesic) dust (X-D2). For that
  limit, finite-time focusing is the known theory-level property of pressureless single-stream scalar dust: Raychaudhuri
  focusing, Zel'dovich/Arnold caustics, and the mimetic, k-essence and BR17 results (LITERATURE_MAP A1–A7, PROVISIONAL).
- From v3s's own PN equations (X3's `L1`), the lane derives the planar and spherical Lagrangian dynamics exactly, up to the
  first crossing. A cold stream crossing a mass folds in finite time; negative-charge (soft) elements fold for every initial
  datum; positive-charge (stiff) elements fold above a threshold or by phase mixing.
- None of v3s's own terms prevents it at the X8/X10 fold locations:
  - the self term does not grow with k;
  - the stiffness is a genuinely nonlinear pressure at Mach ≥ 280;
  - K(Q) is inert at the fold scale for every μ_K that S4 allows.

**(ii) EVERY COMPLETION NEEDS A NEW SCALE.**
- **No zero-constant class qualifies.**
  - C3, the native K(Q) pressure, is inert at the fold scale.
  - C9, adhesion, has no scale, but it is non-variational, and with v3s's sign-indefinite charge it can create energy.
- **One class survives the frozen tests with a new constant: C1**, the K² / (□φ)² operator. This is the mimetic γ(□φ)², the
  ghost condensate, projectable Hořava λ ≠ 1, and the record's khronon β.
  - It needs β (a velocity scale c√β) in a window: 2.0e-6 (canonical) / 2.2e-6 (alt) ≤ β ≤ 1.0e-5 at μ_K = 0.1 Mpc⁻¹, or
    ≤ 1.1e-4 at μ_K = 0.03.
  - Its fold removal is only FT-COND: subsonic compression in linear theory. Nonlinear smoothness is not shown.
  - The literature says this class always carries a ghost or a gradient instability. Here that is C5's IR band, tolerated
    only because its rate stays ≤ H₀.
- **The one published caustic-free completion, C5** (a complex scalar, Babichev & Ramazanov 2017), is **incompatible with
  v3s.** It needs ρ_τ ≥ 0, it is singular where ρ_τ crosses zero, and it adds a degree of freedom.

## The completion table (`classes[<C>]`; grades from FROZEN §3)

| class | literature (PROVISIONAL) | new constant | P1 static / a₀-line | P2 SS screening | P3 large-k ω² (soft side) | P4 DOF | P5 GW | P6 health | FT | 
|---|---|---|---|---|---|---|---|---|---|
| **C1** K² / (□φ)² | CMV14 §8 (c_s² = γ/(2−3γ)); CR15; ACLM04; MU09 codim-1 (λ ≠ 1); RACMP16; record C5, X3 E2 | **β** | PASS (EL term −(B/K)σ_zzzz = 0 on the static branch) | PASS (static) | n = 2, coefficient B(M_θ − 1) > 0 for both signs; stiff side n = 4 (Bγ_L/K) | 3 (one ω² root + 2; C5 table) | PASS (K is second order in h_TT) | PASS-WITH-BOUND: no Hadamard growth; C5 IR band ≤ H₀ needs β ≤ 1.0e-5 (μ_K 0.1) | **COND, window non-empty** |
| C2 higher-spatial-curvature potential | MU09 higher codimension (an "expectation") | ℓ_* | PASS-WITH-BOUND | PASS-WITH-BOUND | n = 0 (k-independent), both signs s = ±1 | 3 | PASS-WITH-BOUND | s = +1 PASS; s = −1 FAIL (pole at k = 1/ℓ_*) | FAIL (sheet kick unchanged; codim-1 needs λ ≠ 1, i.e. C1) |
| C3 native K(Q) pressure | BS24; record C5 | none | PASS | PASS | n = 0 for k² ≫ M_θμ_K² | 3 | PASS | PASS | FAIL (q_K ≤ 0.017; p ∝ ρ² GNL) |
| C4 DBI / BI; dRM caustic-free set | BS25 (via Q7); dRM17; B16 (BI forms caustics as dust) | λ_D (or Galileon scale) | PASS (K″(1) = 2μ²) | PASS | BS25: n = 0, μ-independent limit | 3 | PASS | BS25 PASS; dRM set FAIL: c_s² = 1 − Q² < 0 on the dust branch | FAIL |
| C5 complex scalar (Madelung) | BR17; WK93; B16 appendix | ν = ℏ/m | PASS-WITH-BOUND (quantum potential in statics) | PASS-WITH-BOUND | **n = 4**, ν²/4 > 0, both signs | **4 (FAIL)** | PASS | **FAIL**: ρ = \|Ψ\|² ≥ 0; Q_ν = ν²/(8z²) diverges where ρ_τ crosses zero | PASS-LIT |
| C6 imperfect-DM f(Y/X², Z/X³) | Gorji 2025 | free function f | FAIL unless f = v3s's J | — | — | OPEN (paper) | — | — | FAIL (foliation vorticity ≡ 0; acceleration = v3s's own J) |
| C7 vector / aether | JM01; Gorji 2025; record v4, DOOR11 | c₁…c₄ | — | — | — | 5 (FAIL) | PASS-WITH-BOUND (c₁₃) | FAIL (v4: C5 negative-energy mode) | FAIL (AeST's cold sector is still a scalar gradient flow) |
| C8 multi-stream / kinetic | ASZ82; record O1 c, e | field multiplicity | — | — | — | ∞ or N (FAIL) | PASS | FAIL (particle-like sector; O1 K6, K11) | PASS-CONSTRUCT |
| C9 adhesion / vanishing viscosity | GSS89; B16 shock prescription | **none** | PASS | PASS | — | non-variational (FAIL) | PASS | **FAIL**: sticky merger ΔE = −m₁m₂(v₁ − v₂)²/(2(m₁ + m₂)) > 0 for m₁m₂ < 0 < m₁ + m₂; v diverges as m₁ + m₂ → 0 | PASS-CONSTRUCT |

Abbreviations: CMV14 Chamseddine–Mukhanov–Vikman; CR15 Capela–Ramazanov; ACLM04 ghost condensation; MU09 Mukohyama;
RACMP16 Ramazanov et al.; dRM17 de Rham–Motohashi; B16 Babichev; BR17 Babichev–Ramazanov; WK93 Widrow–Kaiser; JM01
Jacobson–Mattingly; ASZ82 Arnold–Shandarin–Zel'dovich; GSS89 Gurbatov–Saichev–Shandarin. Full references in `LITERATURE_MAP.md`.

**How each new scale would be fixed** (`classes[<C>].SC`). Nothing in v3s fixes any of them.
- **β (C1).**
  - It is bounded below by subsonic compression at the X8/X10 fold locations. Its lower edge is
    `FT_window.beta_min_conservative(M-1=x)`; with M_θ − 1 = x² + 2x instead it is 0.97e-6 / 1.07e-6.
  - It is bounded above by C5's IR band at the chosen μ_K (`FT_window.beta_max`). At the BS cap (10 Mpc⁻¹) the upper edge
    would be 1.0e-9, which is below β_min.
  - Post-result arithmetic on the frozen formula (no verdict weight): the window exists only for μ_K ≲ 0.22 / 0.21 Mpc⁻¹.
  - At β = β_max(0.1) the khronon's sound speed c_A = c√(β(M_θ − 1)/2) is 160–770 km/s at the fold locations
    (`FT_window.c_A_at_beta_max_mu0.1_km_s`).
- **ℓ_\*, λ_D, ν, c_i:** only external bounds (Newton tests, GW170817, BS25's published sets). None of these classes passes
  anyway.

## The analytic folds (step 3; `F1`–`F5`)

- **F1. Exact planar reduction (μ_K = 0).**
  - The hold flux u(1 − μ(|u|/a₀)) = y inverts to 𝒰(y) = a₀y/(a₀ − |y|), with a **flux cap |y| < a₀** (F1a).
  - 𝒰′ = (1 + x)² = M_L (F1b).
  - Gauss-integrated fields satisfy L1's EL equations, and the khronon column is a Lagrangian invariant (F1c). So before
    the first crossing each label obeys ẍ = 𝒰(KS(q)) − K[S(q) + Σ_b(<x)], and
    **J̈ = −Kρ_b(x)J + Kρ_τ0(q)(M_L(q) − 1)** (F1d, residual 0).
- **F2. A cold stream crossing a sheet (the planar point mass).**
  - With zero charge (the mimetic limit), J = 1 − KΣ_bτ/w exactly, against the explicit trajectory map. It folds at
    **τ_f = w/(KΣ_b)**, half the turnaround time, for every w and Σ_b (`F2.tau_fold`).
  - With charge, J = J_c + (J̇_c − KΣ_bJ_c/w)τ + ½ω_p²τ², with ω_p² = Kρ_τ0(M_L − 1) (`F2.J_post_general`, residual 0).
    - It folds iff ω_p² ≤ (KΣ_b)²/(2w²), i.e. ω_pτ_f ≤ 1/√2.
    - Soft labels (ρ_τ0 < 0) fold for **every** initial datum, at τ_* = [J̇₀ + √(J̇₀² + 2AJ₀)]/A (F2-soft).
- **F3. Phase mixing.** Held planar oscillations obey exactly ξ̈ = −K[Σ_b(<q + ξ) − Σ_b(<q)]. In linear theory
  J = 1 − ξ₀ω′t at quarter phases, so every ω′(q) ≠ 0 gives a fold by t ~ 1/|ξ₀ω′|. This is Dawson's sheet-model breaking
  (`F3`).
- **F4. Spherical shells.** The exact shell equation is r̈ = −G(M_b + m)/r² + 𝒰(Gm/r²) (hold-law residual 0).
  - (a) Zero charge: the cycloid reaches r = 0 at t_ff = (π/2)√(q³/2GM_b).
  - (b) Negative enclosed charge: 𝒰(y) − y = −y²/(a₀ − |y|) < 0, so r̈ ≤ −GM_b/r². Collapse comes within t_ff, or earlier,
    where the flux cap drives the inward force to −∞.
  - (c) Positive charge: a log-divergent wall at r_w = √(Gm/a₀) (𝒰 ≈ a₀/(2ε)) excludes hoop collapse. But held shells
    oscillate at **ω² = 2a₀x²/r**, with d ln ω²/d ln r = −5.0, −3.9, −3.1 at r/r_M = 0.1, 1, 10, so they phase-mix to shell
    crossing.
- **F5. Pressure.**
  - (a) The stiffness p = (γ_L/2)ρ² and K(Q)'s p = Kρ²/(2μ_K²) are genuinely nonlinear (p″(τ_s) = 3γ_L/τ_s⁴ and
    3K/(μ_K²τ_s⁴)): compression ends in a shock (Lax, A11).
  - The Chaplygin (BI-like) gas is linearly degenerate, but the work to reach J = 0 is finite, so it does not stop a fold.
  - (b) A γ = 2 pressure stops a cold fold only at J_* = 1/(1 + 𝓜²).
  - (c) At the fold locations (MW-mass AQUAL phantom 1.4e-24 to 2.9e-22 kg/m³), c₀ = 16–246 m/s. **𝓜 ≥ 311 (canonical) /
    280 (alt)**, so J_* ≤ 1.3e-5 (`F5.numbers`).
  - (d) In P3's χ, ω² → Kρ_τ(M_θ − 1) independently of μ_K for k² ≫ M_θμ_K². The K(Q) correction is
    −KM_θ²μ_K²ρ/(k² + M_θμ_K²). **q_K = √M_θ μ_K ℓ ≤ 0.017 / 0.016** at μ_K = 0.1 Mpc⁻¹ (ℓ ≤ 156 kpc), and up to 1.66 / 1.65
    only at the BS cap.
  - **The condition (stated):** the K(Q) pressure c_s² = (Q̄ − 1)/Q̄ ≈ Kρ_d/μ_K² can halt a fold of scale ℓ and speed w
    only if √M_θ μ_K ℓ ≳ 1 **and** Kρ_d/μ_K² ≳ w². Even then p ∝ ρ² turns the fold into a shock. For S4-allowed μ_K, the
    first condition fails by ×60 or more.

## Checks (`x14_caustic_completion.out`, `_results.json`)

- **Main run: 24/24 PASS, exit 0.** The checks are R0, R1, F1a–F1d, F2, F2-soft, F3, F4a–F4c, F5a–F5d, C1-R, C1-P6a, C1-FT,
  C2-FT, C4-FT, C5-P3, C6-FT and C9.
  - **R0** rebuilds X3's B1-S: ω² = ρ_τ[k²/χ − K] on both sides, residual 0.
  - **R1** rebuilds X3's B2-S continuity, P-equation and Euler identities, plus Poisson for all charge, residual 0.
  - **C1-R:** C1's PN term −(B/2K)σ_zz² reproduces the record's form ρ_τ → ρ_τ + Bk²/K (X3 E2 / C5).
- **MUTATE (`X14_MUTATE=1`): 20/24, exit 1. Exactly the four required checks fail.**
  - m1: 𝒰 → y fails F1b.
  - m2: β → −β fails C1-P6a (−ω² → +∞).
  - m3: a repulsive sheet fails F2 (no fold).
  - m4: dropping C1's term fails C1-FT (n = 0).
  - The verdict lines of the MUTATE run (UNDECIDED / NO COMPLETION COMPATIBLE) are the control's output, not physics.
- 23 s, peak RSS 0.11 GB, one thread, nice 15. No downloads. The heavy queue and other lanes were not touched.

## Amendments and execution history

- **68bf6e379d:** criteria, ledger and literature map, committed alone.
- **A1 (POST-RESULT, check code only).** A development run of a scratchpad copy found two defects. Then the scored runs were
  made. No criterion, threshold, class or input changed.
  - The development run gave 23/24, verdict (i) UNDECIDED. F1b's negative branch failed because a patch I had written was
    never applied: dU/dy was taken as +dU/dy_n instead of −dU/dy_n.
  - Fixed. I also added the ω²-root counts for C2 and C5 to P4. C5's grade is unchanged, because it is graded on BR17's
    field content.
  - Verdict (ii) was the same in the development run.

## What this does not show

- **No nonlinear 2D/3D solution.** F1–F4 are exact only in planar and spherical symmetry, up to the first crossing. The 3D
  statement that caustics are generic rests on catastrophe theory and the literature (A1–A2). The "shock after the fold" for
  pressure terms rests on Lax-type theorems from secondary sources.
- **X10's wake is not reproduced analytically.** Inside a held ball the wind feels little force, so a bare Danby–Camm
  estimate (z_f of a few kpc) is not X10's 76–91 kpc. F2's threshold ω_pτ_f ≤ 1/√2 is not evaluated for X10.
- **The X8/X10 regime numbers use a MW-only point-mass field.** Near the MW–M31 null x is smaller, so C1's β_min rises
  (about ×1.5 at 150 kpc by a rough estimate). C1's effect is ∝ (M_θ − 1), which vanishes at the khronon's nulls.
- **C1 is not shown to work.**
  - Its FT is linear and subsonic. Advective steepening and transonic flow near masses are not tested.
  - C5's IR-band rate formula is C5's own estimate.
  - Preferred-frame PPN (α₁, α₂) at λ − 1 = β ~ 1e-6, and a khronon sound speed of 100s of km/s in galaxies and in the
    Solar System's Galactic khronon, are **not checked**. Velocity screening, held halos and H5 lobes would all change.
  - So C1 is "compatible with the frozen passes at a new constant". It is not a recommended completion.
- **C2, C6 and C7 are graded from their representatives or from the record.** A full Hořava z = 3 analysis, a Hamiltonian
  count for C6 and AeST's DOF are not done.
- **Unpublished variants were not evaluated.** Examples: a two-sided stiffness ∝ s|s|; a kinetic ℓ²(∇K)² term on its own.
  The class list was frozen.
- **All literature look-ups are PROVISIONAL** summaries; no paper was downloaded.

## Suggested fixes elsewhere (not edited here)

- **V3_FULL_PICTURE §6, "Soft-side caustics in v3s" / "Dynamical state of moving subsystems".** Add: "X14 (analytic):
  caustics are generic for v3s's khronon. It is irrotational, mimetic at zero charge, and from L1 a cold stream folds at
  τ_f = w/(KΣ_b). Soft elements fold for every datum; stiff ones fold above ω_pτ_f ≤ 1/√2 or by phase mixing. Stiffness
  Mach ≥ 280. K(Q) is inert at the fold scale (q_K ≤ 0.017). No published zero-constant completion. The surviving class is
  K² / λ ≠ 1 / β, with β ∈ [2e-6, 1e-5] at μ_K = 0.1 Mpc⁻¹, and it is linear and subsonic only. BR17's complex-scalar
  completion needs ρ_τ ≥ 0."
- **X3 E2 / C5's β window "1e-16 ≲ β ≲ 1e-9"** was computed at μ⁻¹ = 100 kpc. At S4-allowed μ_K ≤ 0.1 Mpc⁻¹ the IR edge is
  β ≲ 1e-5.
- **A new structural fact for the PN system: the hold flux is capped, |K P| < a₀.** In spherical symmetry it repels a
  positive enclosed charge (a wall at √(Gm/a₀)). It drives a negative enclosed charge to an infinite inward force in finite
  time. The PN system has no solution beyond the cap. X8 flagged the flux only as "far below the a₀ bound".

## Files and run

| file | contents |
|---|---|
| `x14_caustic_completion.py` | Parts R, F and P and the verdicts (X3's `disp_switched` and `L1` copied with provenance) |
| `x14_caustic_completion.out`, `_results.json` | main run |
| `x14_caustic_completion_MUTATE.out`, `_results_MUTATE.json` | MUTATE run (m1–m4) |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X14_caustic_completion/x14_caustic_completion.py              # exit 0
PYTHONHASHSEED=0 X14_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X14_caustic_completion/x14_caustic_completion.py  # exit 1 by design
```

**Coordinator rerun (2026-10-24).** With `PYTHONHASHSEED=0` both runs reproduce exactly: `.out` files identical apart from timing, all 592 / 603 JSON leaves equal, and MUTATE fails exactly F1b, F2, C1-P6a and C1-FT (23–24 s each). **Run with `PYTHONHASHSEED=0`.** Under a random hash seed (`python3 -I`), one rerun stalled in a C5 `sp.simplify` call for more than 10 min and passed 1 GB RSS before it was stopped. sympy's simplification order depends on the hash seed, so the runtime does; the results did not differ in any completed run.
