# S4_v3_muK_clusters: v3's μ_K²ψ term on the cluster cores and on isolated-galaxy lensing (N0 batch R6), and the kernel-only swaps (R4)

## Verdict: SCOPED NO-GO (R6). The R4 tiles are verdict-safe.

- **Frozen rule** (f167979b09): UNDECIDED, because the frozen K5 and K7 lines fail (neither is about the physics; see Checks).
- **Under AMENDMENT A1** (e30bd93c3c, written after test runs and before production): **CANNOT**, on both footings.
  - v3's μ_K²ψ term cannot supply F1's cluster-core excess for any μ_K that BS24 Eq. 39 allows. That holds with or
    without a fitted zero point.
  - No allowed (μ_K, Δ) passes even one cluster cell: 0 of 1,804 cell-rows. The isolated-galaxy guard fails for every
    μ_K ≥ 0.1 Mpc⁻¹.
- **The named obstruction** has two parts:
  - **Shape.** The hydrostatic dust ramps up, and then oscillates once ψ changes sign. The ramp grows outward, so it boosts
    OUTER more than MID.
  - **Ordering.** The oscillation sets in at r_C ∝ (r_M/μ_K²)^{1/3} ∝ M^{1/6}. Isolated galaxies are therefore hit at
    about 0.3–0.4 of the cluster radius, which is the reverse of what F1 and F2 need.
- **R4.** The v3 kernel ν₁ leaves every recomputed tile's class unchanged:
  - SLUGGS centrals: the tension rises from 2.8σ to 3.1σ, and to 3.3σ without ownership.
  - CFG303's six high-z scripts, CFG307 (ALESS 122.1) and CFG308 (CRISTAL) keep their classes.
  - The largest shifts are up to 0.1 dex in s★ (RC100 Q3).

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework.

## 1. The Khronon term is H2's AeST term (the identity, checked)

**The equation.** v3's static equation is BS24 Eq. 35, re-derived from the action in C4 K1 with residual 0:

    ∇·[μ(|∇ψ|/a₀)∇ψ] + μ_K²ψ = 4πGρ_b,   μ = x/(1+x),   ϕ = ψ.

- In spherical symmetry this is r²μ(|ψ′|/a₀)ψ′ = G(M_b + M_K), with M_K′ = −μ_K² r² ψ/G.
- That is term for term H2's AeST system with μ → μ_K.
- **The sign is the same:** +μ²ψ on the left. That is a Helmholtz sign, and the hydrostatic dust is
  δρ_K = −μ_K²ψ/(4πG): positive inside the potential well, negative where ψ > 0.

**The check.** My solver and projector were written independently: RK4 in r, an exact shell projection, and a Khronon
zero point imposed with the same integrator.
- They reproduce F1's PRIMARY to 3e-4 (K1).
- They reproduce H2's per-bin AeST/law ratios at μ = 0.1–1 Mpc⁻¹ to **0.0058** (K2).

**So the Khronon version does not differ in sign or in profile.** The only difference is the allowed range:
- BS24 Eq. 39 (μ_K⁻¹ ≥ 100 kpc) allows μ_K up to **10 Mpc⁻¹**, which is 14.8 h/Mpc at F3's h.
- That is ten times beyond AeST's μ ≤ 1 Mpc⁻¹.
- In the extra range, the oscillation moves into the cores.

## 2. Clusters (tile 28): old → v3

The setup:
- F1's 326-cluster PRIMARY stack and F1's measurement cache (sha256 961ea4fc…e720).
- Annulus-averaged projector P3, the graded one. P3 − P1 is +0.012 in A_MID at μ_K = 0, from bin-averaging.
- Δ = 0 is VSZ's zero point, as in H2; the h 0.686 cells are in `.out`.
- "Old" is F1's PRIMARY: A_MID **1.68 / 1.54**, A_OUTER **0.95 / 0.87**, profile χ² **33.4 / 27.3** (canonical / alt,
  h 0.672). The pass line is χ² ≤ 11.07.

| μ_K [Mpc⁻¹] (μ_K⁻¹) | canonical A_MID / A_OUT / χ² | alt A_MID / A_OUT / χ² | v3/law, stacked, bins 0–7 (0.15–3 Mpc; canonical) | min χ² over Δ (can / alt) |
|---|---|---|---|---|
| 0, law (P3) | 1.69 / 0.95 / 33.6 | 1.55 / 0.87 / 27.6 | 1 | — |
| 0.0156 (64 Mpc; BS24's own) | 1.69 / 0.95 / 34 | 1.55 / 0.87 / 28 | 1.00 … 1.00 | 33.4 / 27.5 |
| 0.03 (33 Mpc) | 1.69 / 0.94 / 33 | 1.55 / 0.86 / 28 | 1.00 … 1.01 | 33.0 / 27.5 |
| 0.1 (10 Mpc) | 1.67 / 0.88 / 32 | 1.53 / 0.80 / 28 | 1.00 1.00 1.00 1.00 1.01 1.02 1.05 1.10 | 32.0 / 28.2 |
| 0.3 (3.3 Mpc) | 1.50 / 0.62 / 50 | 1.37 / 0.56 / 62 | 1.01 1.01 1.02 1.04 1.08 1.17 1.36 1.61 | 33.3 / 33.3 |
| 0.5 (2 Mpc) | 1.30 / 0.88 / 60 | 1.18 / 0.97 / 81 | 1.02 1.03 1.05 1.10 1.21 1.40 1.65 0.77 | 53.7 / 62.2 |
| 0.7 (1.4 Mpc) | 1.17 / −3.95 / 267 | 1.06 / −1.94 / 288 | 1.03 1.05 1.09 1.18 1.35 1.57 1.14 −0.99 | 119 / 151 |
| **1 (1 Mpc)** | 1.33 / −1.31 / 211 | 1.37 / −1.45 / 231 | 1.07 1.10 1.17 1.31 1.48 1.14 −0.76 −0.70 | 211 / 212 |
| 2 (0.5 Mpc) | −2.47 / 16.6 / 277 | −2.29 / 17.8 / 298 | 1.18 1.22 1.22 0.56 −0.81 −0.98 0.35 −0.10 | 199 / 203 |
| **3.333 (0.3 Mpc)** | −3.84 / 14.4 / 344 | −3.15 / 18.2 / 388 | 0.73 0.02 −0.90 −1.92 0.03 −0.26 −0.04 0.12 | 206 / 216 |
| 5 (0.2 Mpc) | 4.17 / −5.23 / 204 | 3.42 / −4.88 / 196 | −1.02 −2.08 −3.03 −0.86 1.10 0.40 −0.83 0.17 | 178 / 176 |
| **10 (0.1 Mpc; cap)** | −9.86 / 21.7 / 218 | −7.11 / 7.36 / 220 | −7.09 −8.70 0.86 1.16 0.98 −1.19 0.07 0.03 | 158 / 160 |
| needed | 1 / 1 / ≤ 11.07 | 1 / 1 / ≤ 11.07 | ~1.7 1.7 1.7, then ~1 ~1 | ≤ 11.07 |

- The best profile χ² anywhere on the allowed grid is the law's own: 27.5 alt, 33.0 canonical, at μ_K ≤ 0.03.
- **Only one (μ_K, Δ) has both band amplitudes within 2σ in all four cells: μ_K = 0.7 with the fitted zero point
  Δ = −0.5.**
  - There A_MID is 1.06 / 0.96 and A_OUT is 0.88 / 1.05 (canonical / alt, h 0.672).
  - But the bands hide the shape: bins 5, 6 and 7 are ×1.80, ×2.24 and ×0.45. The OUTER band sum cancels, as in H2's A1.
  - The profile χ² is 119–155, and the galaxy guard fails there by ×4.5.
- r_max 30 → 60 Mpc changes the ratios by ≤ 0.002.

## 3. Isolated galaxies (tile 18): old → v3 (F2 Track A, B21 Fig. 3, released covariance)

"Old" is F2:
- y_e = 0: χ²_all 160.7 / 127.6; A_in 1.13 / 1.03; A_O1 1.39 / 1.26; A_O2 1.04 / 0.95.
- T_central (y_e = noclu): 428.0 / 382.8; A_O1 2.01 / 1.83; A_O2 4.45 / 4.06.

The v3 baseline, annulus-averaged with r_max 30 Mpc:
- y_e = 0: 164.6 / 129.3; A_O1 1.41 / 1.28; A_O2 1.05 / 0.96.
- noclu: 435.2 / 388.8; A_O2 4.52 / 4.12.

The guard line is |v3/law − 1| ≤ 0.14 at R ≤ 1.1 Mpc in all four mass bins.

| μ_K [Mpc⁻¹] | y_e = 0, exact: χ²_all (Δχ² vs law), can / alt | A_O1 (can) | A_O2 (can) | noclu, approx.: A_O1 / A_O2 (can) | max \|v3/law − 1\|: R ≤ 1.1 / all R | guard |
|---|---|---|---|---|---|---|
| 0.0156 | 167 (+2.5) / 134 (+4.3) | 1.41 ± 0.06 | 1.02 ± 0.07 | 2.05 / 4.46 | 0.003 / 0.11 | OK |
| 0.03 | 176 (+12) / 149 (+20) | 1.40 | 0.92 | 2.05 / 4.31 | 0.02 / 0.41 | OK |
| 0.1 | 274 (+110) / 319 (+190) | 1.33 | 0.60 | 2.02 / 3.35 | 0.29 / 2.9 | FAIL |
| 0.3 | 2022 (+1858) / 2587 (+2458) | 0.94 | −0.18 | 1.77 / −1.58 | 1.2 / 4.6 | FAIL |
| 1 | 2544 (+2379) / 2954 (+2825) | −0.06 | 0.29 | 0.09 / 1.21 | 4.3 / 4.3 | FAIL |
| 10 | 3792 (+3627) / 4328 (+4199) | 0.04 | −0.54 | −0.09 / −5.3 | 4.3 / 4.3 | FAIL |

- **The window where galaxies survive (μ_K ≤ 0.03) leaves the clusters untouched** (ratios 1.00).
- **Every μ_K that moves the clusters (≥ 0.3) wrecks isolated-galaxy lensing** (Δχ² ≥ +1,858).
- μ_K,gal = 0.1 Mpc⁻¹ on both footings.
- The noclu rows multiply by F2's point-mass EFE ratio. That is a labelled approximation: a uniform external field is not
  a solution of the μ_K equation, since μ_K²x_e z ≠ 0.

## 4. The coordinator's questions (M2 follow-up)

**Dust profile, cluster vs isolated galaxy.** The cluster is the median cluster at h 0.672, canonical. The galaxy is
B21 bin 2's mean lens, log M★ = 10.50.

- **μ_K⁻¹ = 1 Mpc.**
  - Cluster:
    - M_K/M_b = +0.09, +0.19, +0.24, +0.17, −0.28, −1.71, −2.17 at r = 0.05, 0.3, 0.5, 0.7, 1, 1.5, 2 Mpc.
    - The lensing mass is ×1.05–1.13 out to 0.5 Mpc, ×0.84 at 1 Mpc and ×−0.83 at 1.5 Mpc.
    - ψ changes sign at 0.63 Mpc (the dust density turns negative), M_K at 0.86 Mpc and M_L at 1.26 Mpc.
  - Galaxy:
    - ×1.00–1.11 out to 0.3 Mpc, then ×−0.63 (0.5), −1.70 (0.7), +1.43 (1.0) and −2.34 (1.5 Mpc).
    - ψ changes sign at 0.26 Mpc and M_L at 0.47 Mpc.
- **μ_K⁻¹ = 0.3 Mpc.**
  - Cluster: with Δ = 0, ψ > 0 already at the centre. VSZ's point-mass λ_max, transplanted to an extended cluster, does
    that once μ_K r_M ≳ 1.
    - So the dust is negative from the centre: M_K/M_b = −0.6 (0.05 Mpc) down to −2.3 (0.5 Mpc).
    - The lensing mass is ×0.62 → −1.17 over 0.05–0.5 Mpc, and then oscillates.
  - Galaxy: ψ changes sign at 0.12 Mpc, and the profile oscillates at ×±2–4 beyond.
- **μ_K⁻¹ = 0.1 Mpc (the cap).**
  - Cluster: M_K/M_b ≈ −17 inside 0.2 Mpc (the dust over-cancels the gas). The lensing mass is ×−5 to −6 there and
    oscillates at ±2.5 beyond.
  - Galaxy: ψ changes sign at 0.056 Mpc, and the profile oscillates at ±3–5 beyond 0.1 Mpc.

**Is any allowed μ_K "×1.4–1.8 at 0.3–1 Mpc, ≈ 1 beyond, ≈ 1 around galaxies"? No.**
- **At Δ = 0**, the largest MID ratio is 1.45 (μ_K = 0.7). Bins 6–7 are then 1.14 / −0.99.
- **With the free zero point**, R_MID ∈ [1.4, 1.8] does occur, at μ_K = 0.3–3.3. In every such case:
  - the outer bins are far from 1 (e.g. μ_K = 0.5, Δ = −1.25: R_MID 1.42, R₆ 2.15, R₇ 2.87);
  - the galaxies are off by 4.9–17× (max |v3/law − 1|).

**Sign and oscillation.** The sign is positive, i.e. attractive, wherever ψ < 0. That gives the ramp. Then ψ crosses zero,
the dust goes negative, and the profile oscillates. This is the same as H2's AeST version.

The oscillation onset scales as M^{1/6}. The ψ-zero radius is:
- galaxy vs cluster 0.26 vs 0.63 Mpc at μ_K = 1;
- 0.58 vs 2.0 Mpc at 0.3;
- 1.2 vs 4.2 Mpc at 0.1.

So **the dust switches on around isolated galaxies first**.

**Negative absolute dust.** The fraction of the median cluster's volume (0.15–3 Mpc) where δρ_K < −ρ̄_K (Ω_K from model
B) is:
- 0 for μ_K ≤ 0.1;
- 0.66 / 0.89 / 0.78 / 0.46 at μ_K = 0.3 / 0.5 / 0.7 / 1;
- about 0.5 above that.

Over those volumes, the hydrostatic branch needs Q < 1, i.e. a negative K(Q) energy density.

## 5. F3's growth-motivated μ_K (EXCLUDED by Eq. 39; reported, never graded)

At μ_K = 243.8, 277.8 and 1718 Mpc⁻¹ (μ_K⁻¹ = 4.1, 3.6 and 0.58 kpc), every observed radius is beyond the dust's Jeans
length. In the static branch:
- **The hydrostatic dust cancels the baryons.** The stacked v3/law ratios beyond 0.3 Mpc are 0 ± 0.12. The resolution is
  ±0.04: under halving, the growth leg moves by 0.040.
- **What is left is a standing wave set by the free zero point.** Bins 0–1 are −4.1 / +4.5 at 244, +7.2 / −1.9 at 278
  and +1.7 / +0.2 at 1718.
- The profile χ² is 189–285, against the law's 27–41 (P2).
- A_MID is meaningless (±50 to ±4,000).
- 50 % of the volume has negative absolute dust.

This is the Jeans-unstable branch, not a prediction. The physical (collapsed) dust needs L1's native run.

## 6. R4: kernel-only recomputes (ν_mono → ν₁ = (1 + √(1 + 4/y))/2)

Every listed script runs unchanged in a fresh child process. The wrapper does four things:
- It swaps the record's ν_mono, held by `CFG4_common` and `CFG2_common`, for ν₁ before the script imports it.
- It redirects every file the script writes into `r4_out/<script>/<variant>/`.
- It runs any multiprocessing pool serially, in one process.
- It hashes the record's lanes before and after the run.

The swap reached every kernel call. The ν₁ call counts match the repro runs' ν_mono counts to within 5 % (root finders
iterate differently).

| tile | script | record (ν_mono) → v3 (ν₁) | class / verdict |
|---|---|---|---|
| 22 SLUGGS centrals | CFG528b | Joint best case J: centrals' mean +0.073 / +0.057 → **+0.073 / +0.064** (can / alt). Measured-tracer row M (stars only): +0.181 / +0.171 → +0.185 / +0.175. **v3 reading without ownership** (R-own → R-bar): J +0.077 / +0.068. | GENUINE TENSION **2.8σ → 3.1σ**, and **3.3σ** without ownership. Cleared 1/4 throughout. Verdict-safe; ν₁ tightens it. |
| 33 high-z | CFG303 amvrosiadis | 7 of 8 discs no root (unchanged). ALESS 075.1 s★ 6.89 → 6.40. | unchanged |
| 33 | CFG303 cfg90_noema | NOEMA3D Z1.4 native: flat −0.007 → −0.021, rival −0.062 → −0.079. CFG90's pooled block runs in a subprocess with CFG90's own ν_RAR, so it is not swapped. | both CONSISTENT (unchanged) |
| 33 | CFG303 kurvs | Primary P2: flat +0.375 → +0.373 (+6.8σ → +6.7σ), rival +0.228 → +0.228. Classes over the 24 cells: 4 / 7 / 13 (unchanged). | "neither" (unchanged) |
| 33 | CFG303 musedark | Native route (iii): 1.210 / 2.110 / 0.660 → 1.206 / 2.045 / 0.651. z3 − z1: −0.263 → −0.268. | unchanged |
| 33 | CFG303 rc100_cristal | RC100 native B s★: Q1 1.48 → 1.37, Q2 1.01 → 0.86, Q3 0.84 → 0.67; Q4 no root. CFG216 outcomes W-mixed (B) and W-none (A, G2). CRISTAL native R_e: 2.01 → 1.76. R_out: 1.95 [95 % ≤ 8.78] → **1.72 [≤ 8.64]**. H(z) at 8.84 stays just outside. | unchanged |
| 33 | CFG303 xcop | η: 1.786 → 1.779 (canonical), 1.648 → 1.642 (alt). Identity / measured: 0.947 ± 0.087. | unchanged |
| 34 ALESS 122.1 | CFG307 | Committed cell s★ 8.82 → **8.42**; 95 % [1.51, 22.6] → [1.14, 22.4]. Grid: f_FLAT,excl 0.270 → 0.233; f_H,excl 0.146 → 0.135; f_noroot 0.437. | NOT ROBUST (unchanged) |
| 34 CRISTAL | CFG308 | Over the 1,008 cells: H(z) excluded 59.4 % → 59.4 %, FLAT excluded 24.0 % → 24.0 %, 432 point no-root cells → 432. R_out six: s★ 1.95 → 1.72. | NOT DISCRIMINATING (unchanged) |

- **Checks:** 18/19.
  - **R4-K0 FAILS for rc100_cristal.**
    - 5 of 1,667 leaves differ, all in its `s5/committed` block (MNRAS slope −0.111 → −0.092).
    - That block execs `paper_numbers.py` live. MNRAS v3.2 (d96f177fee, 2026-10-03) switched its S5 input to the journal
      table after CFG303 was committed (2d9bdc1b92, 10-02).
    - This is drift in the record, not in the wrapper. The S5 block uses the paper's own estimator and is untouched by
      the swap.
  - Every other script reproduces its committed JSON exactly (R4-K0).
  - The swap reached the kernel in all nine (R4-K1).
  - No record file changed (R4-K2: 288 hashed).
- **`--mutate`** (ν₁ in the reproduction slot): R4-K0 FAILS for CFG528b and CFG303 xcop (1/3, exit 1), as required.
- Runtime 2,906 s on one thread. CFG308's pool was 12 processes in the record; here it runs serially.
- **Galaxy groups (tile 23)** are lane P4's, and were not touched.

## Checks

- **R6** (`s4_v3_muk_clusters.py`): **8/8 under A1**, exit 0, 1,630 s, one thread, peak RSS 0.84 GB.

  | check | what it tests | value |
  |---|---|---|
  | K1 | F1 reproduction | 3e-4 |
  | K2 | H2 identity | 0.0058 |
  | K3 | Helmholtz homogeneous | 1.1e-10 / 5.1e-9 |
  | K4 | top-hat | 9.8e-13 |
  | K5 (A1) | Plummer projectors: P1 / P3 / P2 | 4.3e-3 / 7.5e-5 / 1.4e-6 |
  | K6 | F2 reproduction | 0.0000 |
  | K7 (A1) | halving at μ_K = 10: cluster / galaxy | 0.0024 / 0.0009 |
  | K8 | peak RSS | 0.84 GB |

  The frozen lines:
  - **K5-frozen FAILS**: P1 is F1's 90-point convention, at 4.3e-3 against 2e-3.
  - **K7-frozen FAILS**: its growth leg is 0.040 against 0.01. At growth μ_K only the oscillation phase is left
    (amendment A1).
- **`--mutate`** (Yukawa sign, on the reduced grids): K2, K3, K4 and K7 FAIL (4/8, exit 1), as required.
- **R4** (`s4_r4_kernel_swaps.py`): 18/19 checks; the one fail is record drift (§6). `--mutate` gives 1/3.

## What this does not show

- **No aspherical solve, no in-field μ_K solve, no Track B.** The noclu galaxy rows are an approximation.
- **The zero point is VSZ's convention, transplanted from a point mass** (H2's H8).
  - Any zero point is covered by the Δ envelope, Δ ∈ [−8, 2] in steps of 0.25: nothing passes anywhere in it.
  - No boundary condition fixes the zero point: every regular solution decays at infinity.
- **The non-static (collapsed) dust branch is not computed.** That needs L1's native run.
- **The quadratic K is BS24's.** A non-quadratic K is not tested here (F3's open door).

## Files

- `FROZEN_CRITERIA.md`: frozen in f167979b09, AMENDMENT A1 in e30bd93c3c.
- `ASSUMPTION_LEDGER.md`.
- `s4_v3_muk_clusters.py` → `.out`, `_results.json`; also `_MUTATE.*`.
- `s4_r4_kernel_swaps.py` → `.out`, `_results.json`, `r4_out/` (every redirected output, per script and variant);
  also `_MUTATE.*`.
- Runs:
  - `OMP_NUM_THREADS=1 nice -n 15 python3 s4_v3_muk_clusters.py <dir holding F1's f1_meas.pkl> [--mutate]`
  - `... python3 s4_r4_kernel_swaps.py [--mutate]`
- After the production run, the only edit to the R6 script was making `--mutate` use the reduced grids. The production
  code path is unchanged.
