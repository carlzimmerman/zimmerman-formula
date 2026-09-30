# CFG197 — a gas-floor bound on a₀(z) from z > 3.5 discs

- **Criteria:** `../CFG197_FROZEN_CRITERIA.md`, committed in bb91eeb23 before any phase-2 script existed. It was written before any dynamical-mass, velocity or dispersion value was used.
- **Phase 1 scripts** (these use no M_dyn, V, σ or f_DM):
  - `CFG197_bound.py` → `CFG197_bound.out`. 21 of 21 checks pass.
  - `CFG197_preflight.py` → `.out` / `_results.json`. 11 of 11 pass, exit 0.
  - Its `MUTATE=1` run fails C6 and C7 as required, and exits 1.
- **Phase 2 script:** `CFG197_phase2.py` (about 5 s) → `CFG197_phase2.out` / `_results.json`. 10 of 10 checks pass, exit 0.
  - The first run is kept as `CFG197_phase2_firstrun.*`. The script was not changed after it ran, so the copies are byte-identical to the final run.
  - `MUTATE=1` → `CFG197_phase2_MUTATE.out` / `_results.json`. It exits 1 (see below).

## Phase 2 bottom line

- **The gas floor does not separate the flat law from the rival in any bin.**
- **In the pooled z > 3.5 bin both laws are CONSISTENT.** Both verdicts survive the robustness rule: every variant, both footings, and P2 and ν_mono alike.
- **The reason is that the discs sit far above both floors.**
  - The median M_dyn(<r_e)/M★(<r_e) is 5.1.
  - The floors are about 1.33 (flat) and 2.55 (rival).
  - So the floor has nothing to bite on.
- **CONSISTENT is not evidence for either law.**
  - A CONSISTENT verdict here is the survival of a one-sided bound (L4). It carries no evidential weight for either law.
  - Both laws still need mass beyond the stars inside r_e: gas or other unseen mass. This one-sided test cannot say whether the measured gas supplies it.
- **Nowhere does a law come out DISFAVOURED. No bin is ESTIMATOR-LIMITED.** Newton is CONSISTENT in every bin and variant.

## Phase 2 verdicts per bin (frozen labels; P2 is the headline kernel)

"Median log s_req" is the bin median in the primary estimator and variant, for the canonical / alt footing. R_obs = M_dyn(<r)/M★(<r).

| bin | N | Newton median log R_obs (R_obs) | flat, median log s_req | rival, median log s_req | **flat headline** | **rival headline** | ν_mono headlines |
|---|---|---|---|---|---|---|---|
| **z > 3.5 pooled** | 53 | +0.71 (5.1) | +0.69 / +0.68 | +0.53 / +0.49 | **CONSISTENT** | **CONSISTENT** | same |
| Hα sub-bin (Danhaive) | 41 | +0.74 (5.4) | +0.70 / +0.69 | +0.58 / +0.56 | CONSISTENT | CONSISTENT | same |
| [CII] sub-bin (CRISTAL) | 12 | +0.64 (4.4) | +0.60 / +0.59 | +0.34 / +0.30 | CONSISTENT | **NON-DIAGNOSTIC** (primary only) | same |
| MSA-3D (z 0.6–1.7) | 30 | +1.06 (11.4) | +0.93 / +0.92 | +0.86 / +0.84 | CONSISTENT | CONSISTENT | same |
| KURVS (z ≈ 1.5) | 10 | +0.60 (4.0) | +0.52 / +0.50 | +0.41 / +0.37 | CONSISTENT | CONSISTENT | same |
| MSA-3D golden (reported) | 23 | +1.08 (12.0) | +0.97 / +0.95 | +0.89 / +0.85 | CONSISTENT | CONSISTENT | same |

**Robustness.**

- Every CONSISTENT headline above holds in all declared variants and both footings.
- The exception is the rival in the [CII] sub-bin.
  - It is CONSISTENT in the primary.
  - It is NON-DIAGNOSTIC in 12 of the 24 variant × footing cells, mostly compact-stars, thin-disc and moderate-pressure cells.
  - Their medians run from +0.08 to −0.20. Either the median falls below −0.10 or the bootstrap 5th percentile falls below −0.30.
  - None of the 24 cells is DISFAVOURED.
  - So its headline is NON-DIAGNOSTIC ("primary only").
- In the pooled bin, the rival's lowest variant median is +0.02 (moderate pressure, thin disc, compact stars, alt footing), still CONSISTENT.

**The other rules.**

- **Pooling rule:** the sub-bins are never opposite.
- **ESTIMATOR-LIMITED:** never triggered.
- **External field:** nothing to report, because no primary verdict is DISFAVOURED.
- **Separation outcome** ("rival DISFAVOURED, flat CONSISTENT"): none.
- **Flat-law failure against Newton:** none.

**Galaxies below a floor even at 1σ** (primary, canonical, pooled z > 3.5):

- Newton 3/53, flat 3/53, rival 5/53.
- The five are CRISTAL-23b and four Danhaive galaxies whose catalogue M_dyn is below M★ (R_obs 0.02–0.43): 1082948, 1009935, 1015956 and 1085659.
  - The Danhaive paper discusses 1082948 by name.
  - The paper says five systems lie on or above its one-to-one line, but gives no IDs in the text.

## Phase 2: the Roman-Oliveira gas-only over-prediction check (lower side only)

The frozen label is OVER-PREDICTS: the margin (log g_obs − log g_floor)/σ is below −2 in the primary and in every variant (ring radius × f_g × α × footing).

| source | V_ext, σ_ext (km/s) | Newton margin (primary; range) | flat, P2 | rival, P2 | label |
|---|---|---|---|---|---|
| BRI1335-0417 | 125, 57 | −1.49 (−1.65 to −0.22) | −1.72 (−1.88 to −0.53) | **−2.63** (−2.78 to −1.65) | none OVER-PREDICTS; the rival falls below −2 only in some variants |
| J081740 | 249, 33 | −0.14 | −0.21 | −0.56 (−0.75 to +0.22) | none OVER-PREDICTS |
| SGP38326-1 | 548, 46 | +0.95 | +0.94 | +0.86 | none OVER-PREDICTS |
| SGP38326-2 | 409, 40 | +0.51 | +0.50 | +0.42 | none OVER-PREDICTS |

- **No source is labelled OVER-PREDICTS for any law.**
- **BRI1335-0417 is the one near-miss, for the rival.**
  - The rival's gas-only floor sits 2.6σ above the observed acceleration in the primary (2.9σ with ν_mono), but not in every variant.
  - Newton itself is at −1.5σ there: V_ext of 125 km/s is below even the Newtonian gas-only speed of about 229 km/s.
  - So most of that tension is between this quasar host's CO gas mass and its [CII] V_ext, which is shared by every law. It is not a rival-specific result.
  - The paper models only its approaching side.

## Phase 2 MUTATE (R_obs = 1 everywhere; RO unchanged)

- **The control bites.** V1–V3 (the identities tying R_obs to the catalogues) fail, and the run exits 1.
- **C2 holds at scale.** With R_obs = 1, every galaxy is below both laws' floors in every variant, and Newton is exactly 0.
- **The frozen expectation fails, and is kept as written.** The criteria said every bin would come out DISFAVOURED for both laws. It fails for the flat law at z > 3.5.
  - There the flat law is NON-DIAGNOSTIC.
  - Across all bins, 18 of the 24 primary cells are DISFAVOURED. The six that are not are the flat law in the three z > 3.5 bins, in both footings.
  - The KURVS flat headline is also NON-DIAGNOSTIC, although its primary is DISFAVOURED.
  - The phase-1 threshold table predicted this: at z > 3.5 the flat law's DISFAVOURED line is R_obs 0.73–0.91, below 1.
- **The test can fail the flat law.** At MSA-3D's low accelerations, R_obs = 1 does make both laws DISFAVOURED ("both disfavoured", with Newton CONSISTENT).

## Phase 2 readings of the frozen text, departures and wrong expectations

**Readings of the frozen text** (none changes a headline):

1. **ESTIMATOR-LIMITED uses the primary variant's Newton median.** This is moot: Newton is CONSISTENT in every variant of every bin.
2. **The robustness set includes every declared sensitivity:**
   - Danhaive recomputed at the paper's pressure 3.36;
   - Danhaive recomputed at the moderate 1.68;
   - V-lim;
   - both KURVS 3 R_D pressures (6.0 and 3.0).
   - In the pooled bin, each of these pairs the 24 σ₀-detected Danhaive rows with CRISTAL at the matching pressure.
   - MSA-3D golden is reported as its own bin, not as part of MSA-3D's robustness set.
3. **The pooling rule** is applied to the two sub-bins' primary P2 verdicts, per footing.
4. **Bootstrap:** one index matrix per bin and estimator variant (seed 197), shared across laws, geometries and footings, so the comparisons are paired.
5. **Per-galaxy errors.**
   - 14 missing tabulated errors (13 MSA-3D fields, and KURVS 21's e_fDM) are set to 0.
   - MSA-3D and KURVS have no M★ error column, so they get the 0.2 dex the criteria assign to CRISTAL.
   - These errors affect only the per-galaxy below-floor flags.
6. **Roman-Oliveira.**
   - SGP38326-1/2 have no quoted gas error; 0.3 dex stands in for it, and the α_CO 0.3 dex is added on top.
   - Outcomes short of the frozen OVER-PREDICTS are described in plain words, not given a new label.
   - 3DBarolo's ring convention could not be checked: the only Barolo folder on disk (arXiv:2309.04541) holds PNGs only. Both ring conventions ran as variants.

**Recomputed vs paper M_dyn (reported).** The recomputed Danhaive ratio at α = 3.36 matches the paper's own M_dyn to a median of +0.008 dex (range −0.040 to +0.045) over the 24 rows.

**Wrong expectations, kept:**

- **The frozen phase-2 MUTATE expectation** (above).
- **The orchestrator note expected NON-DIAGNOSTIC unless the discs are gas-poor.** The outcome is CONSISTENT for both laws.
  - It is still no separation, as expected.
  - But the label differs, because the discs are far above both floors rather than near them.
  - The pre-flight's D0 and D1 framing implicitly assumed populations near the floors.

## Phase 1 bottom line (pre-flight)

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
