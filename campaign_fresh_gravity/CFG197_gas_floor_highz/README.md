# CFG197 — a gas-floor bound on a₀(z) from z > 3.5 discs (phase 1: lemma, frozen criteria, pre-flight)

- **Criteria:** `../CFG197_FROZEN_CRITERIA.md`. It was written before any dynamical-mass, velocity or dispersion value was used, and before the pre-flight ran. It is not yet committed; the orchestrator reviews it first.
- **Scripts:**
  - `CFG197_bound.py` (sympy, about 1.5 s) → `CFG197_bound.out`. 21 of 21 checks pass.
  - `CFG197_preflight.py` (about 5 s) → `CFG197_preflight.out` / `_results.json`. 11 of 11 checks pass, exit 0.
  - `MUTATE=1` → `CFG197_preflight_MUTATE.out` / `_results.json`. C6 and C7 fail as required, exit 1.
- **Phase 1 uses no M_dyn, V, σ or f_DM.** The pre-flight's loader refuses those columns; check C0 lists every column read.

## Bottom line

- **The lemma holds for both of the framework's kernels.**
  - For P2 and ν_mono, adding gas can only raise the predicted M_dyn/M★. So the gas-free value ν(g★/a₀) is a floor whatever the gas.
  - It is in fact at least ν + μ.
- **At z > 3.5 the test can separate the rival from the flat law, but only if the discs are gas-poor inside r_e.**
  - A gas-free population sitting on the flat floor would need the rival's M★ cut by 0.53 dex (canonical) or 0.58 dex (alt). That is beyond the frozen −0.30 line. The rule's verdict is CAN.
  - With gas equal to the stars inside r_e (μ = 1), that shortfall drops to 0.07 / 0.12 dex, and the rival would not be disfavoured. The CRISTAL paper reports gas fractions near 50% (μ ≈ 1).
- **It is a one-sided test of the rival.**
  - The rival can never be less constrained than the flat law (L4).
  - At z > 3.5 the flat law's "disfavoured" line (M_dyn/M★ ≈ 0.73–0.91) sits within about 0.1 of the point where Newton itself fails (0.79).
  - So the flat law can hardly lose here unless the M_dyn/M★ scale itself is broken.
- **The lower-z comparison bins cannot separate the laws.** MSA-3D is CANNOT; KURVS is MARGINAL.

## The lemma (`CFG197_bound.py`)

- **Setup.** At radius r:
  - x = g★/a₀;
  - μ = g_gas/g★;
  - the predicted ratio is F(μ; x) = (1 + μ)ν((1 + μ)x) = Φ((1 + μ)x)/x, with Φ = yν(y).
- **L0.** dF/dμ = Φ′((1 + μ)x), for any kernel. So ν(x) is a floor for any gas amount if and only if Φ is non-decreasing. For a general law the floor is inf over y ≥ x of Φ(y)/x.
- **P2.** Φ = √(y² + y), so Φ′ = (2y + 1)/(2√(y² + y)) > 1.
- **ν_mono.** Φ′ = 1 + max(h′_RAR, 0.05 H_P/(y + Y_P)) > 1. This is shown symbolically, and numerically on the committed table (Φ strictly increasing from y = 1e-12 to 1e12).
- **Corollary.** F ≥ ν(x) + μ. This is the record's own C_L = Φ′ − 1 > 0 health condition (FP1 B4).
  - ν_RAR satisfies the floor but not the corollary: min C_L = −0.032 at y = 6.6.
- **L4, the M★ rescaling each law requires.** s_req = Φ⁻¹(xR)/x, where R is the observed ratio.
  - Newton: s_req = R.
  - P2: s_req = 2xR²/(√(1 + 4x²R²) + 1).
  - s_req rises with x. So on the same data the rival (x/E) always needs a smaller s_req than the flat law.
- **L5, where the bound fails.** Take a switch law with phantom 1/(1 + (y/y_c)ⁿ).
  - It has Φ′(y_c) = 1 − n/(4y_c).
  - At n = 8, y_c = 1, adding gas lowers the predicted ratio by up to 0.078 dex.
  - Any candidate whose boost the baryons switch off must be checked for this before the floor is applied to it.

## Pre-flight (M★, r, z only)

Primary variant (sphere, mass follows light), P2. Values are canonical / alt footing.

- D0 is the rival's required M★ cut for a gas-free population on the flat floor.
- D1 is the same with gas equal to the stars inside r.
- The floor separation is log ν(x_rival) − log ν(x_flat).

| bin | N | median z (E) | floor, flat | floor, rival | floor separation (dex) | D0 | D1 | frozen rule |
|---|---|---|---|---|---|---|---|---|
| **z > 3.5 pooled** | 53 | 4.41 (7.1) | 1.33 / 1.39 | 2.55 / 2.76 | 0.29 / 0.31 | 0.53 / 0.58 | 0.07 / 0.12 | **CAN** |
| Hα (Danhaive) | 41 | 4.17 (6.7) | 1.33 / 1.39 | 2.54 / 2.75 | 0.28 / 0.30 | 0.52 / 0.56 | 0.07 / 0.11 | CAN |
| Hα, σ₀ detected (V-lim) | 24 | 4.17 | 1.25 / 1.30 | 2.31 / 2.50 | 0.27 / 0.29 | 0.47 / 0.52 | 0.01 / 0.05 | CAN |
| [CII] (CRISTAL) | 12 | 5.19 (8.7) | 1.41 / 1.48 | 3.00 / 3.27 | 0.33 / 0.34 | 0.61 / 0.65 | 0.16 / 0.20 | CAN |
| MSA-3D (z 0.6–1.7) | 30 | 1.14 (1.9) | 2.32 / 2.51 | 3.15 / 3.43 | 0.11 / 0.11 | 0.19 / 0.21 | −0.15 / −0.14 | CANNOT |
| MSA-3D golden | 23 | 1.10 | 2.37 / 2.56 | 3.35 / 3.65 | 0.12 / 0.12 | 0.20 / 0.22 | −0.14 / −0.13 | MARGINAL |
| KURVS (r = R_eff) | 10 | 1.53 (2.4) | 1.62 / 1.72 | 2.22 / 2.40 | 0.13 / 0.14 | 0.23 / 0.25 | −0.14 / −0.12 | MARGINAL |
| KURVS at 3 R_D | 10 | 1.53 | 2.05 / 2.21 | 2.98 / 3.24 | 0.16 / 0.16 | 0.29 / 0.30 | −0.07 / −0.06 | MARGINAL |

**The z > 3.5 verdict is robust.**

- D0 stays at 0.38–0.58 in the pooled bin across all six geometry and radius variants and both footings.
- The smallest value in any z > 3.5 sub-bin is 0.31 (V-lim, thin disc, compact stars).
- ν_mono gives the same picture: pooled D0 0.52 / 0.55, D1 0.12 / 0.15.

**Why D0 (about 0.5 dex) exceeds the floor separation (about 0.3 dex).** Lowering M★ also lowers x, which raises the floor. In the deep regime s_req ∝ R², so the M★ cut roughly doubles the ratio shortfall.

**Where the frozen lines fall** (reported; approximate, at each bin's median x):

| law | "disfavoured" if R_obs = M_dyn(<r)/M★(<r) is below | "consistent" if R_obs is at least |
|---|---|---|
| rival, z > 3.5 (P2) | about 1.55–2.19 | about 2.0–2.8 |
| flat, z > 3.5 (P2) | about 0.73–0.91 | about 1.04–1.24 |
| Newton ("estimator-limited" line) | 0.79 | — |

- Danhaive's own M_dyn/M★ equals 0.9 R_obs in the primary sphere geometry.
- So the pre-flight predicts what phase 2 can find:
  - rival disfavoured if the discs' median M_dyn/M★ comes out below about 1.5–2;
  - both laws consistent if the discs carry roughly their stellar mass again in gas or dark mass inside r_e;
  - a flat-law failure only if M_dyn/M★ < 1, where Newton/ΛCDM fails too.

**Roman-Oliveira (measured CO gas).**

- None of the four kinematic sources has a stellar mass on disk. The only M★ in the paper's text is AzTEC1's, and AzTEC1 has no kinematics (a likely merger).
- So the two-sided test as briefed cannot run.
- The frozen lower side needs no M★: the gas-only predicted minimum circular speed at the last-two-ring radius.
- At f_g = 0.5 (primary), canonical footing:

| source | Newton (km/s) | flat (km/s) | rival (km/s) |
|---|---|---|---|
| BRI1335-0417 | 229 | 241 | 291 |
| J081740 | 265 | 272 | 305 |
| SGP38326-1 | 340 | 347 | 384 |
| SGP38326-2 | 317 | 320 | 340 |

- The rival/flat ratio is 1.06–1.21 (primary ring radius).
- These are high-acceleration systems: g_gas is 4–21 a₀.
- The sources are compared with V_ext only in phase 2.

## What phase 2 would compute (on the orchestrator's go)

- R_obs per galaxy with each paper's own estimator:
  - Danhaive: 1.111 × 10^(logMdyn − logMstar) in the sphere geometry;
  - CRISTAL and MSA-3D: V_rot(R_e)² + 3.36 σ₀² over R_e;
  - KURVS: 1.667/(1 − f_DM) against the thin disc.
- The frozen sensitivities: recomputed from V and σ with α ∈ {3.36, 1.68}; three geometries; compact stars; V-lim; both footings; both kernels.
- log s_req per galaxy for flat, rival and Newton; bin medians with a 4000-draw bootstrap; the frozen DISFAVOURED / CONSISTENT / NON-DIAGNOSTIC lines.
- The robustness, ESTIMATOR-LIMITED and pooling rules.
- For any DISFAVOURED bin, the external field that would restore consistency (reported only).
- The Roman-Oliveira over-prediction check against V_ext (and σ_ext).
- A MUTATE run with R_obs set to 1 everywhere.
- The upper (under-prediction) side of the Roman-Oliveira test needs literature stellar masses for BRI1335-0417, SGP38326-1 and SGP38326-2. That is a look-up that needs the owner's go. RO say J081740 has none.

## Disclosed departures and exposure

1. **The threshold block was added after the first pre-flight run.** This is the "where the frozen lines fall" table (reported; no rule changed).
   - The first run is kept as `CFG197_preflight_firstrun.out` / `_results.json`.
   - Its bin summary and bottom line are byte-identical to the final run's.
2. **The Roman-Oliveira radius was corrected before commit.** The criteria's first draft used the outermost ring, which does not match V_ext's definition (the average of the last two rings).
   - It is now the last-two-ring mean, (N − 1) RADSEP, with (N − 1.5) RADSEP as a variant.
   - The change was made after the first pre-flight run, which used no velocity, and before any velocity was seen.
   - 3DBarolo's ring-centre convention is assumed, not verified on disk.
3. **Inadvertent exposure.** While checking how limits are encoded, greps printed:
   - five raw Danhaive rows, including log M_dyn and σ₀ limits;
   - the first columns of the CRISTAL dynamics table, plus V_rot for three rows.
   - No computation used them. The test is not blind in any case: the papers' own conclusions are listed in the criteria.
4. **CRISTAL's radius is R_e,disk,** a DysmalPy fit output with a [CII]-size prior, not a stellar-light radius. This is declared in the criteria.

κ = ½ stays FITTED. Nothing here is a result about a₀(z); it is a design and power check.
