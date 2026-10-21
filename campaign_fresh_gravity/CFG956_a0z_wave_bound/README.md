# CFG956: how large can a wave in a0(z) be? The expansion bound from CFG689's own likelihood

The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21).

**Frozen design:**
- criteria 707cdf4cb4;
- amendment A1 8debb62336, added after the criteria and before any result. A1 holds the damped family, the "on the way down now"
  phase constraint, the rising/falling question, and the instruction that the sketch is illustrative only.

**Code and results:** aaa000a458. The four modes ran on 2026-10-21 on one core, each under 0.29 GB:

| mode | run time |
|---|---|
| K | 1.3 min |
| MUTATE | 0.6 min |
| MAIN | 6.4 min |
| DAMPED | 7.8 min |

**Standing wording:**
- κ = ½ FITTED. Footings never pooled.
- A constant ρ_DE is ΛCDM's background, so nothing here favours the framework over ΛCDM.
- A bound on a wave is not evidence for a wave.
- Not a closed theory.
- Scope: the expansion bound only. Physical models, growth, CMB and high-z galaxies belong to CFG957.

## What was bounded

The law is a0(z) = κ c √(G ρ_DE(z)), so a wave in a0 is a wave in ρ_DE, squared. The family (base §3, A1.2) is

  a0(z)/a0(0) = A(z) · [1 + ε0 (1+z)^β sin(2π ln(1+z)/P + φ)] / [1 + ε0 sin φ].

- **Plain wave:** β = 0, with φ free.
- **Damped wave:** β ∈ {0, 0.5, 1, 2}, with φ restricted so that a0 is falling today (d a0/dz > 0 at z = 0).
- **A(z):**
  - branch S: CFG689's best-fit native background (shape fixed);
  - branch C: constant ρ_DE;
  - branch N: six free nodes, reported only.
- **Likelihood:** CFG689's primary likelihood, re-implemented line for line (DESI DR2 BAO with the native ruler r_d = 147.07 Mpc,
  plus Pantheon+, curvature free). The present-day amplitude, ω_k, ω_b, ω_c and the SN offset are all profiled. θ* is not used
  (CFG689 held it back after K9).
- **Bound:** for each period P (19 values, 0.05–3 in ln(1+z)), the 95% upper bound on ε comes from Δχ² = 3.84, with φ profiled.
- **Footings:** every bound is on the ratio a0(z)/a0(0), with κ fitted per footing. So each number below is the same on the
  canonical (9.3603e-11) and alt (1.1312e-10) footings. The footing only scales the absolute a0 (figure panel d).

## 1. The allowed region

### Plain wave (β = 0): ε_95 by period (cfg956.json)

| P in ln(1+z) | 0.05 | 0.1 | 0.25 | 0.5 | 1.0 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| branch S (CFG689 background) | 0.048 | 0.045 | 0.046 | 0.037 | 0.044 | 0.141 | 0.353 |
| branch C (constant ρ_DE) | 0.055 | 0.045 | 0.044 | 0.032 | 0.061 | 0.147 | 0.421 |
| branch N (free nodes, reported) | 0.050 | 0.054 | 0.054 | 0.123 | 0.417 | 0.836 | ≥ 1 (no bound) |

- **Short and middle periods.** For every P ≤ 1.5 the bound is **ε ≤ 0.032–0.08**. That is a0 wobbles of at most about 3–8%.
  - The range over the full grid is 0.035–0.353 in branch S and 0.032–0.421 in branch C.
- **Long periods (P ≳ 2).** The bound loosens to ε ≈ 0.14 at P 2 and ≈ 0.35–0.42 at P 3.
  - Over z ≤ 2.33, a P = 3 wave is less than half a cycle. It acts as a smooth tilt, the same freedom CFG689's own band already has
    (√X at z 2.33: [0.33, 1.21], 68%).
  - At its bound the P = 3 wave runs from 1.01 (S) / 1.00 (C) at z 0.5 to 0.53 (S) / 0.57 (C) at z 2.33.
- **Branch N** frees the six-node shape, so long-period waves are absorbed (no bound at P = 3). Short periods stay bounded at 0.05.
- **Envelope at the bound, branch S** (a0(z)/a0(0) at z = 0.5 / 1 / 1.5 / 2.33):

  | P | allowed range |
  |---|---|
  | 0.5 | 1.02–1.10 / 0.88–0.95 / 0.91–0.98 / 0.88–0.95 |
  | 3 | 0.68–1.43 / 0.59–1.24 / 0.61–1.28 / 0.59–1.24 |

  Each envelope is A(z)(1 ± ε_95). The exact wave at the bound's own phase lies inside it.

### Damped wave, on the way down today (cfg956_DAMPED.json)

ε0_95 is the amplitude today. Branch C first, then S.

| β (a0 ≥ 0 cap on ε0) | P 0.05 | 0.1 | 0.25 | 0.5 | 1.0 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|---|
| 0 (1) | 0.061 / 0.049 | 0.045 / 0.045 | 0.044 / 0.046 | 0.019 / 0.037 | 0.055 / 0.044 | 0.147 / 0.141 | 0.421 / 0.353 |
| 0.5 (0.53) | 0.063 / 0.047 | 0.044 / 0.041 | 0.042 / 0.043 | 0.021 / 0.032 | 0.049 / 0.036 | 0.128 / 0.112 | 0.342 / 0.259 |
| 1 (0.29) | 0.064 / 0.044 | 0.040 / 0.036 | 0.039 / 0.038 | 0.019 / 0.027 | 0.043 / 0.028 | 0.107 / 0.085 | 0.254 / 0.177 |
| 2 (0.082) | 0.062 / 0.035 | 0.030 / 0.024 | 0.028 / 0.026 | 0.019 / 0.018 | 0.031 / 0.016 | 0.067 / 0.046 | ≥ 0.082 (cap) / 0.076 |

### Largest allowed amplitude by redshift

This is ε(z) = ε0_95 (1+z)^β, maximised over P, at z = 0.5 / 1 / 2.33 / 3 / 5. The first number is branch C, the second branch S.

| β | all P (the long periods dominate) | P ≤ 1 only |
|---|---|---|
| 0 | 0.42 / 0.35 at every z | 0.061 / 0.049 at every z |
| 0.5 | 0.42 / 0.48 / 0.62 / 0.68 / 0.84 (C); 0.32 / 0.37 / 0.47 / 0.52 / 0.64 (S) | 0.077 / 0.089 / 0.11 / 0.13 / 0.15 (C) |
| 1 | 0.38 / 0.51 / 0.85 / 1.02 / 1.53 (C); 0.27 / 0.36 / 0.59 / 0.71 / 1.06 (S) | 0.096 / 0.13 / 0.21 / 0.26 / 0.39 (C) |
| 2 | 0.18 / 0.33 / 0.91 / 1.31 / 2.94 (C); 0.17 / 0.30 / 0.84 / 1.21 / 2.73 (S) | 0.14 / 0.25 / 0.69 / 0.99 / 2.23 (C) |

- **z = 3 and z = 5 are not constrained by the expansion data.** Those columns are the family's own extrapolation of a bound set at
  z ≤ 2.33.
- An amplitude above 1 means the formula would put a0 below zero at the troughs. The physical cap is 1.

### The z 3–5 prediction window

This is a0(z)/a0(0) for the allowed damped waves, at z = 3–5. It is the testable high-z statement of the family, and it holds only if
the same (β, P, φ) form continues above the data.

Two windows bracket the true allowed set:
- **outer** (frozen, cfg956_DAMPED.json): ε0 up to ε0_95, at every allowed phase;
- **inner** (post hoc, cfg956_POSTHOC_G1.json): the boundary waves themselves.

| β | outer, branch C | outer, branch S | inner, branch C | inner, branch S |
|---|---|---|---|---|
| 0 | 0.41–2.46 | 0.44–1.92 | 0.42–1.12 | 0.44–1.00 |
| 0.5 | 0.13–2.55 | 0.28–1.88 | 0.16–1.18 | 0.32–1.04 |
| 1 | 0–2.63 | 0–1.88 | 0–1.30 | 0.16–1.16 |
| 2 | 0–3.22 | 0–2.34 | 0–2.39 | 0–2.17 |

- The no-wave prediction there is 1 (branch C) or 0.92 (branch S).
- For β ≥ 1 the extrapolated family can drive a0 to zero by z ≈ 4–5.
- The record's implied-a0 points at z 4.4–5.5 have 68% errors of 0.14–0.74 dex. The tightest is ALPINE 6 pooled, at 0.14 dex.

### Where the bound comes from: z ≤ 2.33, and nothing above z ≈ 2.5

- **Every bound above is set by data at z ≤ 2.33:** the DESI tracers up to Lyα at 2.33, and Pantheon+.
- **Above z ≈ 2.5 the expansion data place no bound.**
  - K5: a wave confined to z > 2.5, even at ε = 1, changes the CFG689 χ² by exactly 0 for every period. So does a wave confined to
    z > 2.34.
  - At the CFG689 best fit, ρ_DE carries only 4.1% / 2.0% / 1.1% of H² at z 2.5 / 3.5 / 4.5. Even an ε = 1 peak would move H(z) by
    only +6.0% / +2.9% / +1.6% there.
  - The only CFG689 datum that reaches beyond 2.5 is θ*, and it is held back.

### Wave preference

| branch | largest Δχ²_0 (2 dof, local) | at P | class |
|---|---|---|---|
| S | 1.96 | 0.25 | NO WAVE PREFERRED |
| N | 2.34 | 1.0 | NO WAVE PREFERRED |
| C | 6.03 (1.97σ) | 1.0 | LOCAL HINT |
| damped C | 6.0–7.0 | 1.0 | LOCAL HINT |

- The branch-C hint is **CFG689's own z ≈ 0.7 bump, not a wave.** A constant background cannot fit the bump, and a P ≈ 1 wave with
  ε ≈ 0.03 mimics it. Branch S already contains the bump, and there the preference vanishes.
- The hint is uncorrected for 19 periods. With Bonferroni ×19, p ≈ 0.9.

### Does CFG689 prefer a0 rising or falling toward today? (A1.3)

**Falling** (larger in the past), weakly.
- **Slope at z = 0.** The best fit has w(0.4) − w(0) = +0.013. The profile Δχ² of the tied fit is 0.37, so +0.61σ. The posterior
  gives P(w(0.4) > w(0)) = 0.71.
- **Down from the z ≈ 0.7 peak.** w(0.7) − w(0) = +0.081. The profile gives +1.77σ, and the posterior P = 0.96.
- **For comparison only (not framework-native):** the record's DESI DR2 CPL chains (sonnet55_push/puzzle_32pi/p13c, w0 > −1 in all
  four fits) say ρ_DE is decreasing today, so a0 is on the way down:

  | fit | (1 + w0)/σ |
  |---|---|
  | DESI+CMB | +2.8 |
  | +Pantheon+ | +2.9 |
  | +Union3 | +3.8 |
  | +DESY5 | +4.4 |

  These are marginal-w0 statements from external chains.
- **Effect of the "on the way down" constraint.** It does not bind in branch S at β = 0: the bounds are identical to the plain wave.
  In branch C it tightens some periods (P 0.5: 0.032 → 0.019).

## 2. Galaxy-side check (reported only; CFG957 owns this)

| check | what it measures | result |
|---|---|---|
| G2 | the effect on the implied-a0 points themselves, through distances (δlog a0 ≈ −2 δlog D_A) | at most 0.022 dex, below every point's error (0 of 21) |
| G1, frozen | the shift of the *predicted* a0(z) at each point's z, conservatively over every phase | exceeds the 68% statistical error for 12 of 21 points |
| G1, post hoc | the same shift, for the boundary waves themselves | exceeds it for 7 of 21 points |

- **The expectation "no" was wrong for G1.** The allowed long-period waves (P ≳ 2) move the predicted a0 at z ≈ 2 by about
  0.2–0.24 dex.
- **Points that could see this, on statistical errors alone:** RC100 corr Q4 (σ 0.076 dex, 3.1σ), ALPINE 6 pooled (2.3–2.7σ), the
  CFG223 CRISTAL fit rows (1.7–2.2σ), RC100 corr Q3 (1.9σ) and MeerKAT HI (1.3σ, from short periods).
- **Caveats:** baryon-mass systematics are not in these errors, and the record calls these points calibration-limited. The 0.2 dex is
  the same tilt freedom that CFG689's own band already has (0.43–0.54 dex wide at z 2–2.3).
- The damped family at z > 2.5 is extrapolation (cfg956_POSTHOC_G1.out).

## 3. Illustrative sketch (the owner's rough drawing; not the hypothesis)

**The curve.** A PCHIP curve in ln(1+z) through a0/a0(0) = 1, 2, 0.3, 3 at z = 0, 0.5, 2.5, 4.5. In it ρ_DE(0.5) = 4 ρ_DE(0).

**Implied H(0.5).**
- **+44.0%** at fixed present-day parameters (CFG689 best fit: 91.5 → 131.8 km/s/Mpc).
- D_H/r_d at z 0.51 would then be 15.43, against DESI LRG1's 21.86 ± 0.43: a −15σ pull on that one datum.

**Fit (W, ω_k, ω_b, ω_c profiled).**
- χ² 2018.3, so Δχ² = +619 against constant ρ_DE and +630 against the CFG689 node fit (class vs constant: EXCLUDED).
- With ρ_DE(0) held at CFG689's value instead, Δχ² is +4019.
- The fit only gets that close by driving ρ_DE(0) to 0.024 and ω_k to +0.15, which gives H0 56.3.
- Most of the excess is in the SN shape: SN χ² 1728 vs 1385. LRG3+ELG1, ELG2, Lyα and BGS add 39–81 each.

Its z ≈ 4.5 peak is above every datum and costs nothing.

## Checks and controls

**K: PASS** (cfg956_K.out)

| check | result |
|---|---|
| K1 | χ² at CFG689's stored best fit = 1388.342276, exact |
| K2 | the profiler at ε = 0 gives 1388.3423 (S) and 1399.4561 (C), as stored |
| K3 | CFG681 reproduced: 10.5515 / Ω_m 0.29703; 1400.143 / 0.30390 |
| K4 | CFG689's own sampler, rerun here, reproduces its band: √X 68% at z 1.0 / 1.2 / 1.5 / 2.33 = [0.762, 1.027] / [0.762, 1.048] / [0.706, 1.115] / [0.325, 1.212]; node means and stds to 4 decimals; R-hat 1.0007 |
| K5 | the z > 2.5 window gives Δχ² = 0 exactly |

**MUTATE: PASS** (cfg956_MUTATE.out)

| test | injected | recovered | 95% interval | Δχ²_0 |
|---|---|---|---|---|
| MUT-A (plain) | ε 0.3, P 0.5 | ε 0.3000 | [0.263, 0.343] | 506 |
| MUT-D (damped) | β 1, ε0 0.1 | ε0 0.1000 | [0.082, 0.120] | 183 |
| MUT-0 (null mock) | none | – | ε_95 = 0.028 at P 0.5 | 0.00 |

Reported only: fitting the MUT-A mock at the wrong period still detects a wave (P 0.25: Δχ² 164; P 1.0: 235).

## Disclosures

- **Spurious warnings.** numpy's Accelerate backend prints spurious matmul warnings, as disclosed in CFG689. The script filters them;
  K1 reproduces χ² exactly.
  - K was run first without the filter, then rerun with the committed script. The checks were identical.
- **Optimiser.** least squares with 16 φ starts (8 in the damped family), warm-started along the ε grid. ε_95 is found by brentq to
  1e-3. There were no DISJOINT flags and no root failures. NO BOUND cells: branch N at P 3 (reported only), and two damped cells at the
  a0 ≥ 0 cap (β 2, branch C, P 2.5 and 3).
- **Post hoc.** cfg956_posthoc_g1.py (G1 at the boundary waves, and the inner z 3–5 window) was written after the MAIN result. It
  has no verdict weight.
- **Tie to CFG689.** The bound inherits CFG689's choices: the A1 (ω_b, ω_c) pair, the CFG253 ±3% cold-mass rule, and the DR2
  reconstruction. CFG689's brackets B4m/B4p move its high-z band most. They were not rerun here.

## Figure

`cfg956_wave_bound.png`:
- (a) ε_95 vs P for the plain wave, branches S, C and N;
- (b) ε0_95 vs P per β, damped and on the way down;
- (c) the largest allowed amplitude by redshift;
- (d) a0(z)/a0(footing, today), with:
  - CFG689's native band;
  - the largest allowed plain wave (P 3, ±0.353, and the wave at its bound);
  - the z 3–5 window, outer hatched and inner shaded;
  - the "no expansion bound above z ≈ 2.5" region;
  - the record's implied-a0 points on both footings (canonical filled, alt open);
  - the illustrative sketch, drawn faint.

Caption: The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21). Bounds use z ≤ 2.33 data
only; above z ≈ 2.5 the expansion data place no bound. κ = ½ fitted; footings never pooled; a bound on a wave is not evidence for a
wave.

## Files

| file | contents |
|---|---|
| `cfg956_a0z_wave.py` | modes K / MUTATE / MAIN / DAMPED |
| `cfg956_posthoc_g1.py` | post hoc |
| `cfg956_figure.py` | plot only |
| `cfg956_K`, `cfg956_MUTATE`, `cfg956`, `cfg956_DAMPED`, `cfg956_POSTHOC_G1` (.out, .json) | outputs |
| `cfg956_wave_bound.png` | the figure |

Run with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg956_a0z_wave.py MODE`.
