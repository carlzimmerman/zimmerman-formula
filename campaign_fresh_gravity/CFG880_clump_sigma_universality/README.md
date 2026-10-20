# CFG880 — is the cold clump's velocity dispersion σ_x the same in every dwarf?

Criteria: `FROZEN_CRITERIA.md` (8c1d0b870, committed alone before the script; owner block 880–889).
Run: `OMP_NUM_THREADS=1 nice -n 10 python3 cfg880.py` (about 1 minute, numpy/scipy only).
Controls: `CFG880_MUTATE=scatter|null`. Post-hoc diagnostic: `CFG880_POSTHOC=floor`. Each mode writes its own `.out` / `.json`.
κ = ½ fitted; ν_e; the two footings are never pooled; not theory closed.

## Question
CFG877's finite cold clump fits every dwarf sample's group mean with one σ_x ≈ 7.5 km/s. A fixed-physics origin needs the
same σ_x in every dwarf. CFG878's candidate is the hydrogen-cooling floor, 7.36–8.22 km/s, a ±5.5% bracket. This lane fits the
dwarf-to-dwarf intrinsic scatter s_int of ln σ_x directly.

## Method (as frozen)
- **Sample:** 83 LVD dwarfs (MW, M31 and local field) with a measured σ, r_h and M_V. The rotating / gas-rich set is excluded.
- **Prediction:** Υ_V = 2, and gas inside r12 is counted (CFG874's Wang+16 disc). σ_pred² = σ_law² + G M_x(<r12; σ_x)/(3 r12),
  using CFG877's clump: M_x = min[2σ_x² r³/(G(r² + r_c²)), 81σ_x⁴/(4Ga0)], with r_c = 104 pc.
- **Hierarchy:** ln σ_x,i = ln σ̄ + δ_i, with δ_i ~ N(0, s_int²).
- **Errors and fit:** split-normal LVD errors. δ_i is marginalised on a 0.0025 grid in ln σ_x by FFT. Profile-likelihood
  intervals are Wilks, Δ(−2 ln L) = 1.00 / 3.84.

## Result — CLASS: **NOT UNIVERSAL** (both footings; no qualifier triggered)
| | canonical (a0 = 9.3603e-11) | alt (a0 = 1.1312e-10) |
|---|---|---|
| **ŝ_int** (68%; 95%) | **0.380** (0.326–0.440; **0.281–0.510**) | **0.380** (0.334–0.454; **0.288–0.528**) |
| σ̂̄ hierarchical (95%) | 6.90 km/s (6.05–7.72) | 6.85 km/s (5.93–7.66) |
| σ̄ if forced universal, s_int = 0 (95%) | 8.04 (7.89–8.28) | 8.35 (8.10–8.58) |
| scatter test Λ = 2Δln L vs s_int = 0 | 277.5 (p ~ 1e-62) | 304.2 (p ~ 2e-68) |
| dwarfs whose own 95% σ_x range excludes the universal σ̄ | 12 below, 12 above | 13 below, 12 above |
| power pre-flight: 95% UL on s_int if the truth were 0 (16 nulls) | median 0.072, 84th pct 0.092; ≤ 0.15 in 94% | median 0.071, 84th pct 0.101; ≤ 0.15 in 94% |

The 95% lower limit (0.28 / 0.29) lies well above the 0.15 threshold. A truly universal σ_x would have given an upper limit
near 0.07, so the test had the power to return UNIVERSAL. An intrinsic scatter of 0.38 in ln σ_x means:
- σ_x varies by a factor 1.46 (1σ) between dwarfs, a 68% spread of about 4.7–10.1 km/s;
- through M_cl ∝ σ_x⁴, the clump mass varies by about 0.66 dex. CFG872 found 0.52 dex under H-LINK.

**Variants** (all NOT UNIVERSAL on both footings; ŝ_int and its 95% interval):
| variant | canonical | alt |
|---|---|---|
| V1 Υ_SFH (CFG827, 29 dwarfs) | 0.320 (0.241–0.437) | 0.320 (0.240–0.443) |
| V2 M_V ≤ −6 (N 53) | 0.380 (0.259–0.575) | 0.400 (0.276–0.631) |
| V3 law-over-predicted removed (canonical: Crater II, Fornax, Sagittarius, Cassiopeia III, NGC 147; alt adds Leo I, NGC 185) | 0.340 (0.247–0.456) | 0.320 (0.231–0.439) |
| V4 binary-corrected σ (Arroyo-Polonio+2026: 8 UFDs + Crater II) | 0.400 (0.299–0.547) | 0.420 (0.307–0.569) |
| V5 10% systematic floor on σ | 0.300 (0.214–0.438) | 0.320 (0.212–0.443) |
| V6 law-linked core r_c ∝ σ_x² | 0.480 (0.340–0.677) | 0.480 (0.348–0.706) |

Neither pre-registered qualifier fires: V3 does not change the class, and the result survives a 10% systematic.

**What drives it.** Well-measured dwarfs disagree with each other, not just the extremes. Each dwarf's own σ_x (95%,
canonical):
- Draco 11.05 (10.30–11.81), Ursa Minor 9.73 (9.17–10.51), Canes Venatici I 9.23 (8.45–9.97);
- against Leo II 7.30 (6.20–8.74) and Bootes I 5.57 (4.86–6.31).

Draco and Leo II have similar size and luminosity (r12 258 vs 197 pc, M_V −8.9 vs −9.5) but need σ_x 11.1 against 7.3. At
the ends:
- the brightest dwarfs (Fornax < 5.0, Leo I < 5.4, NGC 147 < 8.4) want little or no clump, because the law alone already
  over-predicts them;
- the tiniest ultra-faints (Segue 1 ≈ 20, Willman 1 ≈ 23, r12 ≈ 26 pc) want a large σ_x, because a 104-pc core puts
  little clump mass inside their r12.

Removing either end (V2, V3) or correcting binaries (V4) does not remove the scatter. Correcting binaries raises it.

## Hydrogen-cooling comparison (POST-HOC label, CFG878 candidate (i); not graded)
- **Interval overlap:** both the hierarchical σ̂̄ interval (6.05–7.72) and the forced-universal one (7.89–8.28) overlap the
  bracket [7.36, 8.22] (alt also OVERLAPS).
- **Upper limit:** the 95% upper limit on s_int is not ≤ 0.055, the bracket's half-width.
- **Reading:** a typical clump σ near the cooling floor is allowed. A single fixed velocity in every dwarf is not, unless
  something else accounts for the scatter.

## Post-hoc diagnostic (added after the pre-registered run; `cfg880_POSTHOC_floor.out`)
How large an unmodelled per-dwarf systematic in σ would hide the scatter? The diagnostic adds it in quadrature to both error
sides:
| systematic floor on σ | 10% | 15% | 20% | 25% | 30% |
|---|---|---|---|---|---|
| class | NOT UNIVERSAL | NOT UNIVERSAL | UNDECIDED | UNDECIDED | UNDECIDED |
| ŝ_int, canonical (95%) | 0.30 (0.21–0.44) | 0.28 (0.17–0.41) | 0.24 (0.11–0.39) | 0.20 (0–0.36) | 0.15 (0–0.34) |

The alt footing is the same to ±0.02. Losing the result takes a systematic of about 20% in σ in every dwarf, which is about
40% in dynamical mass. The scan never reaches UNIVERSAL: the 95% upper limit stays ≥ 0.31. At floors ≥ 25% the hierarchical
σ̄ drifts to 5.7–6.4 km/s, with a 95% upper edge of 6.85–7.23, just below the bracket's lower end (7.36).

## Controls
- **K1 PASS:** at s_int = 0 and σ̄ = V_x/√2, the script reproduces all five CFG877 group means on both footings (max
  |diff| 5.6e-17).
- **K2 PASS:** the FFT-marginalised per-dwarf ln L agrees with a direct 40001-node quadrature at s_int = 0.3 (max |Δ ln L|
  3.3e-5, all 83 dwarfs). The FFT dynamic-range fallback (direct log-space evaluation of the same discrete convolution)
  never triggered within 10 of the maximum.
- **MUTATE scatter** (synthetic s_int = 0.4, seed 880): it recovers 0.420 (0.337–0.559) canonical and 0.440 (0.338–0.571) alt,
  so NOT UNIVERSAL on both. The control behaves.
- **MUTATE null** (synthetic s_int = 0): it gives 0.075 (0–0.164) and 0.085 (0–0.174), UNDECIDED, not NOT UNIVERSAL. The control
  behaves. This realization's upper limit falls just above 0.15, which happens in about 6% of draws (pre-flight).

## Reading (per the pre-registered rule)
- **The rule:** s_int absorbs all scatter that the quoted σ errors do not cover. NOT UNIVERSAL therefore means: the dwarfs
  carry scatter beyond their errors, and if all of it is the clump's, σ_x varies by about ×1.46 per dwarf.
- **What it does not prove:** that the clump itself varies. Unmodelled tides, external field, anisotropy, Υ spread or binaries
  could share the load. The post-hoc scan says they would need about 20% in σ in every dwarf.
- **For CFG877:** one clump σ describes group means, as CFG877 found, but not individual dwarfs. That counts against any
  origin that fixes one universal clump velocity, such as a single cooling-floor temperature, under CFG877's clump form.
- **What it leaves open:** the scatter is partly structured: the brightest dwarfs need no clump and the tiniest need a large
  σ_x. So the clump's shape (fixed r_c), not only its σ, may be what is wrong. V6's scaling core makes the scatter larger,
  not smaller.

## Disclosures
- **Not blind:** all 83 dispersions were used in earlier lanes, and σ_x ≈ 7.53 was calibrated (CFG870) on a subset of this
  sample. The finite-clump form was chosen post-hoc (CFG877).
- **Not modelled:** external field, tides, binaries (except V4) and per-dwarf Υ (except V1).
- **Post-hoc material:** the floor scan was added after the pre-registered run and is not graded. It sits in the script behind
  `CFG880_POSTHOC`, and the pre-registered output was re-run and is byte-identical. The hydrogen-cooling comparison is a
  post-hoc label.
- **Compute:** light single-core run alongside the 1024³ job, as allowed by the owner.
