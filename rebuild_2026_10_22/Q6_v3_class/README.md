# Q6_v3_class: v3's own linear CMB and P(k), from a Khronon variant of C7's patched CLASS

## Verdict: CRISP FINDING

**1. Literal v3 has no radiation era.** v3's literal BS K(Q) = μ_K²(Q−1)² carries the stiff a⁻⁶ partner (C4 K7; L137
found the same for AeST's quadratic K).
- At every grid μ_K (14.8–2542 h/Mpc) the stiff term exceeds radiation before z = 1854–3.2×10⁵.
- At T = 1 MeV the K sector is 10⁸–10¹³ × radiation (ΔN_eff,equiv 2.6×10⁹ to 7.7×10¹³).
- The khronon CLASS refuses every literal run at its own start test (Ω_r(a_ini) = 3×10⁻²² to 5×10⁻¹⁷).
- BBN (ΔN_eff,equiv(1 MeV) ≤ 0.5) needs μ_K ≥ **1.84×10⁸ h/Mpc**, which is **1.24×10⁷ × BS's cap** of 14.8 h/Mpc.
- Frozen reading at all six grid points: **NO RADIATION ERA (BBN-EXCLUDED).**

**2. On F3's dust background, the Boltzmann calculation confirms F3's linear-growth failure, and the failure is
stronger than F3 found.** The model is LOB: dust background with the literal perturbation equations (A2).
- At the BS cap (14.8 h/Mpc) σ₈ is 0.061: R_B = σ₈/σ₈(dust) = **0.073**.
- F3's ODE gave 0.391 (start a_i = 1e-3) and 0.203 (a_i = 1e-4). Frozen reading: **CONFIRMED**.
- R_B is 0.17 / 0.34 / 0.53 / 0.74 / 0.88 at 50 / 150 / 361 / 1000 / 2542 h/Mpc.
- σ₈ within 5 % of the dust limit needs μ_K **beyond the grid, > 2542 h/Mpc**. F3's ODE said 361–2542.

**3. Fits to plik-lite + low-ℓ** (free: ω_K FITTED, ω_b, θ_s, A_s, n_s, τ, A_planck; C7's Gauss–Newton). Δχ² vs the
ΛCDM refit (χ² 1003.47), numbers only:
- 14.8 h/Mpc: **+13 891** (not converged). The frozen 4-iteration optimiser was still falling by ~1000 per iteration, so the
  minimum may be lower.
- 50: +5 583 (not converged, same reason).
- 150: +1 164. 361: +329. 1000: +88.0. 2542: +18.7.
- Best-fit S₈ is 0.034 / 0.145 / 0.390 / 0.542 / 0.654 / 0.755 (ΛCDM 0.846).

**a₀ is absent at linear order.** J_x enters the second-order action only through J(0) = Λ and J′(0) = −1; a₀ first
appears at O(Y^{3/2}) (D0). So these numbers test v3's dust sector and its J′(0) = −1 hold, not the galactic law, and
the two footings do not enter. κ = ½ is FITTED and does not enter. The dust abundance ω_K is a FITTED initial condition.
No dark-matter particle is involved. Not "theory closed". Never "the framework fits the CMB".

## 1. Step D: the linear equations, derived from the action (`q6_derive.py`, 19/19 PASS; MUTATE 18/19)

**Source.** BS24 (arXiv:2404.06584) Eq. 6 as transcribed by C4 via WebFetch. The paper is **not on disk**
(PROVISIONAL). Only Eqs. 1–7 and 39 are used, and every equation below is re-derived from the quoted action with sympy.

**The setup.**
- Metric h₀₀, h₀ₓ, hₓₓ, h_yy = h_zz; khronon τ = τ̄(η) + ϑ.
- Extra-sector Lagrangian √−g[−2j₁Y + 2K(Q)], with j₁ = J′(0).

**What the derivation gives.**
- **The khronon sector is exactly a fluid, with no anisotropic stress (D2).**
  - The congruence's acceleration is A_x = ∂ₓΞ, with Ξ = Ψ − π′ − ℋπ (gauge-invariant; π = ϑ/τ̄′). It has no shift
    dependence.
  - 8πGδρ = Q̄K″δQ + 2j₁(k/a)²Ξ, 8πGδp = K′δQ, 8πG(ρ+p)θ = k²K′Q̄π, δQ = −Q̄Ξ + Q̄′π.
  - Eliminating Ξ gives δp = c_s²δρ_rest − 3ℋc_a²(ρ+p)θ/k².
  - The rest-frame sound speed is **c_s² = Q̄K′/(Q̄²K″ − 2j₁k²/a²)**, with c_a² = K′/(Q̄K″).
  - With j₁ = −1 the J term makes c_s² fall as 1/k² above aμ_K. That is the "hold".
- **Background (D1).** 8πGρ̄ = Q̄K′ − K, 8πGp̄ = K, a³K′ = I₀. J is absent from the background, so G_cosmo = G.
- **Consistency checks.**
  - D3: the gauge map is exact for both the exact system and LO.
  - D4: ∇_μT^{μν} = 0 holds on the shell of the τ equation, in both gauges.
  - D6: the dust limit K″ → ∞ gives CDM for any j₁.
  - D7: on Minkowski space the τ mode has ω = 0 (a double root), BS24's "non-propagating" mode, which checks the
    transcription.
- **The link to F3 (D5).** In the quasi-static sub-horizon limit the khronon's net self-force kernel is **exactly**
  F3/BSK2's s = a²μ²/(k² + a²μ²) for j₁ = −1, and exactly the Jeans kernel 1 − k²/(a²μ²) for j₁ = 0.
- **Why the run model is LOB (D10; AMENDMENT A2).**
  - The frozen LO sound speed K′/(K″ + 2k²/a²) tends to ε = Q̄ − 1 at small k, so it is superluminal wherever ε > 1.
  - At CLASS's start, ε ≫ 1 for every grid μ_K.
  - The fluid identity X′ = −θ − h′/2 + 3(ℋ′ − ℋ²)θ/k² (X = δ_rest) then gives a stiff super-horizon mode with
    ω² = 3(ℋ² − ℋ′)c_s².
  - LOB keeps the literal c_s² (with Q̄ = 1 + ε) on a dust background, and that c_s² is ≤ ε/(1+ε) < 1.
- **Initial conditions.**
  - IC1–IC3 pass. The coded IC is CLASS's own fluid formula (1004.5509) with w = 0 and c_s²(k, τ_ini) (IC_fld).
  - C7's IC block assumes c_s² = c_a² and fails here (IC_C7, reported). That triggered the frozen fallback: an IC edit.
- **Mutate.** Flipping j₁ → −j₁ in the exported J term breaks D5.

## 2. Step P: the patch (`q6_make_patch.py` → `khronon.patch`)

- **Build.** Pristine CLASS v3.3.4, then C7's `aest.patch` (it applies cleanly), then only three things replaced:
  - `background_aest_K()`;
  - `perturbations_aest_rhs()`;
  - the sector's IC block (the A2 fallback).
- **Model switch.** `aest_K_type` 0 = DUST, 3 = LIT, 4 = LOB. `aest_K2` = μ_K² in Mpc⁻². `aest_lambda_c` carries j₁.
- **Checks.**
  - V_prov checks that the built tree equals pristine + `khronon.patch`.
  - It also checks that the tree differs from C7's only inside those three spans.
- Builds, hashes and paths are in `PROVENANCE.md`. No download.

## 3. Step V: validation (`q6_validate.py`; 8/12, exit 1 because of the frozen gates; MUTATE 2/12)

| check | result | line |
|---|---|---|
| V0 sector off vs pristine | bit-identical | identical |
| **V1 dust limit (μ_K → ∞, J′(0) → 0), synchronous / Newtonian** | ≤ 4.1e-6 every spectrum; θ_s 0, r_drag 6.8e-9 | ≤ 1e-4; ≤ 1e-6 |
| V1 reported: DUST with j₁ = −1; LOB at 10⁶ h/Mpc with j₁ = −1 / 0 | 4.1e-6; ≤ 9.5e-4 / ≤ 1.2e-3 (both completed) | — |
| frozen V2 convergence (LOB 361) | **FAIL**: P(k) 0.45 | ≤ max(2e-3, 2 × vanilla) |
| frozen V3 gauge (LOB 361 / 14.8) | **FAIL**: P(k) 8e-2 / 29; φφ 7.4e-3 at 14.8. TT/TE/EE ≤ 8.5e-5 (vanilla ≤ 8.1e-5) | ≤ max(1e-3, 3 × vanilla) |
| frozen V5 IC attractor (LOB 361) | **FAIL**: TT 5.3e-4 at ℓ ≈ 14 | ≤ vanilla + 1e-4 |
| A3 V2b same-k-grid convergence | PASS: P(k) 6.5e-6, φφ 6.9e-3 (vanilla 8.8e-3) | in ΛCDM units, as V2 |
| A3 V3b gauge in ΛCDM units, LOB 361 / 14.8 | PASS: ≤ 8.2e-5 / ≤ 5.8e-4 | as V3 |
| A3 V5b start × 0.25 vs × 0.125 | PASS: TT 2.1e-5 (vanilla 2.5e-5) | vanilla + 1e-4 |
| MUTATE (metric-source sign in δ′) | breaks V1 (TT 1.2e5) and V3b | must break V1 or V3 |

**The frozen V2, V3 and V5 gates FAILED. The native numbers rest on the post-result gates of AMENDMENT A3.** The scratch
diagnostics behind A3 (not scored) showed four things:
- LOB's matter transfer function passes through a node near k ≈ 0.5–1 Mpc⁻¹, where P/P_ΛCDM falls to 3×10⁻⁶. V2's 45 %
  comes from interpolating across the two precisions' different k grids through that node.
- On the same k grid, default and high precision agree to ≤ 1.2e-3 for k ≤ 1 Mpc⁻¹.
- The V3 mismatches sit where LOB's own spectrum is 10⁻³ to 10⁻⁸ of ΛCDM's.
- V5's change converges as τ_ini² (5.25e-4 for ×1 → ×0.5; 1.38e-4 for ×0.5 → ×0.25). It is the same at high precision.
  Every native run therefore starts at × 0.25.

## 4. Step B: the literal background (frozen reading NO RADIATION ERA at every grid μ_K)

| μ_K (h/Mpc) | z at ε = 1 (w = 1/3) | z where stiff = radiation | ρ_K/ρ_r at 1 MeV | ΔN_eff,equiv (1 MeV) | ε at recombination | CLASS |
|---|---|---|---|---|---|---|
| 14.8 | 1705 | 1854 | 1.25e13 | 7.7e13 | 0.26 | refuses |
| 50 | 3840 | 6267 | 1.1e12 | 6.7e12 | 0.023 | refuses |
| 150 | 7989 | 1.88e4 | 1.2e11 | 7.5e11 | 2.6e-3 | refuses |
| 361 | 1.44e4 | 4.53e4 | 2.1e10 | 1.3e11 | 4.4e-4 | refuses |
| 1000 | 2.83e4 | 1.25e5 | 2.7e9 | 1.7e10 | 5.7e-5 | refuses |
| 2542 | 5.27e4 | 3.19e5 | 4.3e8 | 2.6e9 | 8.9e-6 | refuses |

μ_K,BBN (ΔN_eff,equiv(1 MeV) = 0.5) is 1.84×10⁸ h/Mpc (μ⁻¹ ≈ 0.008 pc ≈ 1.7×10³ AU physical). The window [BBN floor, BS cap] is empty by
a factor of 1.2×10⁷. That gap is far larger than F3's growth gap of 24–172×.

## 5. Steps N and C: v3's native spectra (LOB, j₁ = −1) at C7's ΛCDM refit parameters

| μ_K (h/Mpc) | χ² (ΛCDM 1003.47) | σ₈ | S₈ | **R_B** | R_F3 (a_i = 1e-3 / 1e-4) | P/P_dust at k = 0.1 / 0.3 / 1 h/Mpc | TT/TT_dust at ℓ = 220 / 540 / 1000 |
|---|---|---|---|---|---|---|---|
| 14.8 | 170 501 | 0.061 | 0.062 | **0.073** | 0.391 / 0.203 | 2.4e-3 / 2.1e-5 / 4.8e-7 | 1.55 / 1.89 / 1.41 |
| 50 | 41 691 | 0.142 | 0.145 | 0.172 | 0.625 / 0.330 | 6.3e-3 / 3.8e-4 / 2.8e-6 | 1.19 / 1.39 / 1.26 |
| 150 | 8 966 | 0.285 | 0.291 | 0.344 | 0.844 / 0.502 | 0.16 / 9.0e-4 / 1.5e-7 | 1.04 / 1.18 / 1.12 |
| 361 | 3 024 | 0.441 | 0.451 | 0.533 | 0.950 / 0.668 | 0.45 / 0.053 / 3.2e-4 | 1.006 / 1.10 / 1.05 |
| 1000 | 1 395 | 0.616 | 0.630 | 0.745 | 0.991 / 0.847 | 0.78 / 0.27 / 0.017 | 0.998 / 1.03 / 1.03 |
| 2542 | 1 071 | 0.731 | 0.747 | 0.883 | 0.999 / 0.950 | 0.93 / 0.58 / 0.13 | 0.999 / 1.009 / 1.012 |

DUST reproduces ΛCDM at these parameters: σ₈ ratio 1.000000, χ² 1003.58. No model is RUNAWAY: LOB only suppresses.
R_F3 is F3's own ODE (copied verbatim) run at these parameters. Copied, it reproduces F3's K4 exactly (K0b: 0.39080,
0.20260, 0.12055).

**Why the Boltzmann suppression is much stronger than F3's ODE (read off the equations; an explanation, not a scored
check).** F3 let baryons and khronon grow as GR dust (δ ∝ a) until a_i, then switched the hold on. In the Boltzmann
calculation two things differ:
- **The khronon never clusters early.** Where ε > 1 its literal rest-frame sound speed is ≈ ε/(1+ε) → 1, so it behaves
  like k-essence. Afterwards it is held on k > aμ_K. At recombination that is k > 0.014 h/Mpc at the cap (ℓ ≳ 130) and
  k > 0.33 h/Mpc at 361 h/Mpc.
- **The baryons do not help before z ≈ 1100**, because they are locked to the photons.

So at the cap the acoustic peaks see no CDM-like potential wells above ℓ ≈ 130 (TT/TT_dust = 1.89 at ℓ = 540). The matter
transfer function then follows baryon-only growth after decoupling, with a node near k ≈ 0.5–1 Mpc⁻¹.

### Fits (plik-lite TTTEEE + low-ℓ TT + low-ℓ EE; C2 likelihood; C7's Gauss–Newton, 4 iterations, start at C7's ΛCDM refit)

| model | Δχ² vs ΛCDM refit | converged? | H₀ | σ₈ | Ω_m | S₈ | ω_K (FITTED) | n_s | P/P_ΛCDM (best fits) at k = 0.1 / 0.3 / 1 h/Mpc |
|---|---|---|---|---|---|---|---|---|---|
| ΛCDM (pristine) | 0 (χ² 1003.47, plik 582.40) | yes | 67.55 | 0.828 | 0.313 | 0.846 | 0.1206 (ω_c) | 0.962 | — |
| LOB 14.8 | +13 891 | **no** (−1121 at iteration 4) | 90.3 | 0.051 | 0.131 | 0.034 | 0.0783 | 1.112 | 3.6e-4 / 1.4e-6 / 1.8e-7 |
| LOB 50 | +5 583 | **no** (−909 at iteration 4) | 65.7 | 0.132 | 0.364 | 0.145 | 0.1298 | 0.928 | 8.5e-3 / 9.5e-5 / 1.9e-6 |
| LOB 150 | +1 164 | yes (−0.4) | 57.9 | 0.293 | 0.531 | 0.390 | 0.1527 | 0.872 | 0.24 / 9.2e-4 / 3.8e-7 |
| LOB 361 | +328.8 | yes | 61.7 | 0.455 | 0.426 | 0.542 | 0.1382 | 0.907 | 0.54 / 0.067 / 3.8e-4 |
| LOB 1000 | +88.0 | yes | 66.1 | 0.618 | 0.336 | 0.654 | 0.1242 | 0.940 | 0.79 / 0.28 / 0.017 |
| LOB 2542 | +18.7 | yes | 66.9 | 0.729 | 0.322 | 0.755 | 0.1217 | 0.950 | 0.93 / 0.58 / 0.13 |

- The fitted parameters move far from ΛCDM where the hold reaches CMB scales: H₀ 58–90, n_s 0.87–1.11.
- Not converged means the true minimum may be lower; the trend with μ_K does not depend on it.
- These are the χ² of the theory's own linear sector against Planck. They are not a statement that any model fits or
  fails "the CMB" in general.

## 6. What this does not show

- **LOB is not the literal theory.** It drops the a⁻⁶ background term, which step B shows is fatal on its own. LOB
  answers F3's question in F3's setting, with the literal perturbation equations.
- **The frozen LO model** (hold law with Q̄ ≡ 1 at all times) was not run. Its early era is superluminal (A2).
- **The early K shape is not fixed by v3.** A different early K — BS25's DBI form (λ_D, not on disk), or SZ21's Cosh with
  a new constant Z₀ — could change both the background and the early sound speed. F3 already named this open door.
  It would be a POSTULATED K shape with at least one new constant. Not scanned (no knob scans).
- **The nonlinear Y^{3/2} term** (a₀) is not linear physics. Whether it restores growth is L1_khronon_pm's question.
- **γ_L** is not in the patch (estimated (kL★)² ≤ 8e-7, ledger).

## 7. Process notes and errors found

- **Frozen-text slip.** The frozen K0 line quotes F3's a_i = 1e-4 ratio as 0.20313. F3's committed value is 0.202602, and
  K0b compares against F3's JSON.
- **Step-B cancellation bug, fixed before the reported run.** A first step-B pass (aborted, not reported) computed I₀ as
  2μ²(√(1+x) − 1). That cancels catastrophically at large μ_K and gave a spurious BBN root of 1.6×10⁴ h/Mpc. The committed
  script uses 6H₀²Ω_K/(√(1+x) + 1).
- **Scratch runs before the scripts (not scored).**
  - Smoke runs: one LOB run at 14.8 h/Mpc (it ran) and one LIT run (CLASS refused it).
  - Validation diagnostics behind A3: start × 0.5 / 0.25 at both precisions; same-grid P(k); the φφ location.
- **Records this affects (not edited; another lane's file).** `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §2 lists
  μ_K as "FREE" with F3's 361–2542 h/Mpc as the growth requirement.
  - The literal K makes every μ_K ≤ 1.8×10⁸ h/Mpc BBN-excluded.
  - On F3's own background the growth requirement is above 2542 h/Mpc.
- **Compute.** Every process ran at `OMP_NUM_THREADS=1 nice -n 19`, with CLASS runs one at a time.
  - Step D: 0.07 GB.
  - Validation: 76 s, 0.29 GB.
  - Native: 238 CLASS runs, 1304 s, peak 0.29 GB.
  - CFG960 was not touched.

## Files and commits

| commit | content |
|---|---|
| 386ab3c2bb | `FROZEN_CRITERIA.md` + assumption ledger, alone, before any script or number |
| c3dac14e6e | AMENDMENT A1 (pre-result): LO definition, IC_C7 reading |
| 25302566ad | AMENDMENT A2 (post-result for step D lines, pre-result for builds and spectra): LOB, IC fallback |
| b2b96c38f4 | AMENDMENT A3 (post-result, after validation; before any native number): supplementary gates V2b/V3b/V5b, start × 0.25 |
| e95753ecfd | step D: `q6_derive.py` + outputs (19/19; MUTATE 18/19) |
| cbd7608e1e | steps P + V: `q6_make_patch.py`, `khronon.patch`, `khronon_MUTATE.patch`, `PROVENANCE.md`, `q6_validate.py` + outputs (8/12, the frozen gates fail; MUTATE 2/12) |
| ed5894d6e1 | steps B/N/C: `q6_native.py` + outputs (6/6; MUTATE 0/2) |
| (this commit) | README |

Run (from this directory, outside-repo builds as in `PROVENANCE.md`):
- `OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_derive.py`
- `python3 -I q6_make_patch.py <pristine> <new dir> [--mutate]`, then `make -j1 class`
- `OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_validate.py`
- `OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_native.py`

`Q6_MUTATE=1` gives the `*_MUTATE.*` files.
