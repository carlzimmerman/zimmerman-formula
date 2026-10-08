# CFG463: does the ultra-faints' bare-law excess rise with later infall? (per-object test of CFG344)

**Verdict (frozen rule): NOT DIAGNOSTIC.** The correlation has the WRONG sign for CFG344 in every reading, but none reaches 2σ, and the sample cannot see CFG344's own predicted slope (power 5 % / 18 %).

> κ = ½ is FITTED. No dark-matter particle is added; the cold fluid's MASS is still required. Nothing here says the theory is closed or that the data favour the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone as **e201f79eb** before the script existed and before any infall time was computed.
- **Data on disk only, nothing downloaded:**
  - Fritz et al. 2018 (A&A 619, A103) Tables 1–3, from CFG433's arXiv source (sha256 checked against its FETCH_LOG);
  - the LVD Milky Way table, for positions, the dispersions and the S4 (EDR3) motions;
  - CFG344's committed MAH code and JSON;
  - FG001's estimator, exec'd read-only.

## The question

CFG344 explains the +0.32 dex bare-law excess of the Milky Way ultra-faints by cold accretion onto reionisation fossils that stops at infall. With one formation epoch, a later infaller carries more cold mass, so its excess x = log10(σ_obs/σ_law) should be larger. CFG344's prediction is therefore that ρ = Spearman(x, infall lookback) **< 0**.

## Result

S1 is the verdict sample: the 21 resolved ultra-faints with Fritz+18 3D motions. The infall boundary is R_200c(z) of the MW's growing collapse mass. Statistics: Z = atanh(ρ)·√((N−3)/1.06); f_pos is the fraction of 300 error draws with ρ > 0.

| host | footing | ρ | Z | p (perm.) | f_pos | role |
|---|---|---|---|---|---|---|
| L6: law, M_b 6.0e10 grown | canonical | **+0.334** | **+1.43** | 0.14 | 0.91 | load-bearing |
| L6 | alt | **+0.274** | **+1.16** | 0.24 | 0.91 | load-bearing |
| L7: law, M_b 7.3e10 grown | canonical | **+0.253** | **+1.07** | 0.28 | 0.88 | load-bearing |
| L7 | alt | **+0.286** | **+1.21** | 0.22 | 0.87 | load-bearing |
| L6s: law, M_b fixed | canonical / alt | +0.286 / +0.256 | +1.21 / +1.08 | | 0.88 / 0.89 | sign condition |
| N: Newtonian NFW 9.82e11 grown | both | +0.373 | +1.61 | 0.10 | 0.94 | sign condition |
| S4: L6, LVD EDR3 motions, N = 31 | canonical / alt | +0.163 / +0.138 | +0.84 / +0.71 | 0.38 / 0.46 | 0.83 / 0.75 | data veto |

**Reported rows** (L6, canonical / alt):
- S2, adding 5 upper limits (N = 26): +0.276 / +0.244.
- S3, no LMC candidates (N = 15): +0.325 / +0.271.
- B300, a fixed 300 kpc boundary: +0.327 / +0.182. About half the objects are censored here.
- Every reading has the same sign.

**Reading.**
- CONTRADICTED's sign conditions all hold: f_pos ≥ 0.84 on both footings, L6s and N positive, and no veto.
- Only its 2σ bar fails (Z +1.07 to +1.43, against 2).
- SUPPORTED fails its 2σ bar, its error-Monte-Carlo condition (f_neg 0.09) and its sign conditions. The veto is not triggered.

**Power.** If CFG344 is right, these 21 objects would show its predicted slope at ≥ 2σ only 5 % of the time (NFW cold-mass profile) or 18 % of the time (SIS profile). The median predicted ρ is −0.07 and −0.27. The test therefore could not have supported CFG344 even if it is right.

## What drives the positive lean: mostly luminosity selection

- **Fainter ultra-faints have larger excesses:** ρ(x, M_V) = +0.52.
- **The fainter ones are found nearby and fell in early:** ρ(t, M_V) = +0.38, and ρ(t, log r_GC) = −0.75.
- **Partial correlation of x with infall time at fixed M_V:** +0.175 (Z +0.71) canonical and +0.10 (Z +0.41) alt. At fixed log r_GC: +0.21 / +0.11.
- So most of the raw positive ρ is the selection. What remains at fixed luminosity is small, but it is still not negative.
- CFG344 itself predicts a luminosity trend: one M_c for all fossils means cold mass dominates more in the faintest. So this trend is not evidence against CFG344.

**POST-HOC consistency with CFG344's own slope** (`cfg463_posthoc.py`; no verdict depends on it):
- **P3, raw ρ:** the observed Z is reached by 3.2 % of the NFW-profile mocks and 0.25 % of the SIS-profile mocks. **Do not quote P3.** Its mocks permute x, which drops CFG344's own luminosity term, so it is biased against CFG344.
- **P4, at fixed M_V (the fair version):**
  - NFW-profile prediction: P(Z_mock ≥ Z_obs) = **0.19**, fully consistent.
  - SIS-profile prediction: P = **0.029**, a mild lean against the steeper slope.
  - Power of the fixed-M_V test: 2 % and 12 %.

**Plain reading:**
- The per-object infall test does not support CFG344, and it does not refute it.
- The data lean the other way, but that lean is mostly the faint-and-nearby selection.
- At fixed luminosity, the weaker (NFW-profile) form of CFG344's slope is untested, and the steeper (SIS-profile) form is mildly disfavoured (post hoc, about 1.9σ one-sided).

## Per-object values (S1, canonical; t_inf = median lookback in Gyr, L6 host; L = LMC candidate)

| object | x | t_inf | object | x | t_inf | object | x | t_inf |
|---|---|---|---|---|---|---|---|---|
| Eridanus II | +0.355 | 0.00 | Ursa Major I | +0.571 | 5.30 | Coma Berenices | +0.322 | 9.44 |
| Pisces II | +0.371 | 0.12 | Carina II L | +0.303 | 7.57 | Ursa Major II | +0.587 | 9.45 |
| Leo V | +0.313 | 0.23 | Carina III L | +0.736 | 8.00 | Bootes I | +0.229 | 9.72 |
| Leo IV | +0.251 | 0.31 | Horologium I L | +0.580 | 8.22 | Reticulum II L | +0.475 | 10.62 |
| Canes Venatici II | +0.432 | 0.36 | Hercules | −0.000 | 8.53 | Willman 1 | +0.646 | 11.04 |
| Grus I | +0.215 | 0.41 | Hydrus I L | +0.188 | 8.98 | Segue 1 | +0.698 | 11.21 |
| Aquarius II | +0.466 | 0.53 | Tucana II L | +0.436 | 9.13 | | | |
| Bootes II | +0.218 | 0.63 | | | | | | |

16–84 % ranges, the alt footing, the other hosts and the limits are in `cfg463_ufd_infall.out` and the JSON.

**Bimodal infall times.** Several poorly measured systems have bimodal infall posteriors: either a first infall within the last Gyr or an early one. Examples are Aquarius II [0.30, 6.59], Bootes II, CVn II, Grus I, Carina III and UMa I. Bootes II's median flips between modes across footings (0.63 vs 6.65 Gyr).

## Method (as frozen)

- **Excess:** FG001's isolated law of the stars (`sigma_pred`, efe=False; Υ_V 2; r = 4/3 r_half; σ² = g r/3). Each footing is used separately.
- **Phase space:**
  - RA/Dec from the LVD; distance modulus from Fritz Table 1 (error ⊕ 0.1 mag);
  - proper motions from Fritz Table 2 (statistical ⊕ systematic, with the correlation C on the statistical part); V_LOS from Table 2;
  - Fritz's frame (R0 8.2 kpc, v_sun (11, 248, 7.3) km/s, z_sun 25 pc);
  - 300 Gaussian draws plus the central values (seed 463).
- **Orbits:** in-plane kick-drift-kick leapfrog, backward, dt 0.5 Myr, to the lookback at z_f = 8 (13.16 Gyr).
- **Hosts:** spherical. The law field is ν_mono(g_N/a0)·g_N from point-mass baryons (softened at 0.5 kpc).
- **Growth:** h(z) is CFG344's own Correa+15 MAH evaluated at the record's MW collapse mass 9.82e11 (CFG286). Values: α 0.212, β −0.717, z_1/2 1.20.
- **NFW variant:** M_200c(z) = 9.82e11 h(z), with c from Dutton–Macciò 2014 (c 8.4 at z = 0).
- **Infall:** the largest lookback at which r ≤ R_200c(z) of 9.82e11 h(z). R_200c is 210 kpc at z = 0 and 118 / 67 / 41 kpc at z = 1 / 2 / 3.
  - This R_200c boundary is where the MW's cold fluid has collapsed; the cold fluid is operationally CDM (CFG474).
  - An object that was never inside gets t_inf = 0. Each object's value is the median over its 301 orbits.

## Controls

| control | result |
|---|---|
| C-X: FG001's committed median reproduced | PASS (0.0) |
| C-DATA: sha256 matches FETCH_LOG; 39 / 39 rows, same order | PASS |
| **C-FRITZ: frame conversion vs Fritz Table 2** | **FAIL, kept.** d_GC within 0.69 kpc and V_tan within 0.16 of its tolerance pass. The V_rad clause (≤ 3 km/s for all 26) fails: max 14.2 km/s, with 9 objects off by more than 3 km/s |
| C-MAH | PASS (h(0) = 1, monotone; R_200c(0) 210.4 kpc; DM14 at z = 0 equals CFG36's to 0) |
| C-ORB (a): static energy drift | PASS (max 4.4e-6 of v0²/2) |
| C-ORB (b): dt halved | PASS (26 of 26 central t_inf identical to 0.000 Gyr) |
| C-SIGN | PASS (ρ = −1) |
| C-NULL: 10,000 shuffles | PASS (P(\|Z\| ≥ 2) = 0.041) |
| MUTATE (`_MUTATE.out`) | PASS: verdict NOT DIAGNOSTIC; Z −0.11 / −0.14 / −0.08 / −0.04 |
| POST-HOC P1: re-integration reproduces the JSON | PASS (0.0) |
| POST-HOC P2: independent DOP853 radial integrator vs leapfrog | max \|Δt_inf\| 0.0003 Gyr |

**Why C-FRITZ fails, and why it does not touch the verdict.**
- All 8 well-measured objects (V_tan error < 30 km/s) agree within 3.0 km/s, and so do the nearby ones. Those are the objects whose V_rad depends most on the frame, so the frame is right.
- The 9 misses are the poorly measured, mostly distant systems (Aquarius II, Bootes II, Eridanus II, Grus I, Leo IV, Leo V, Pisces II, Willman 1, Hydra II). They are off by 5–14 km/s, at most 1.9 of Fritz's own quoted error.
- Our Monte Carlo median does not reproduce Fritz's values either (max 15.3 km/s).
- The most likely cause is that Fritz's table quotes noise-debiased (backward Monte Carlo) values for large-error objects. My 3 km/s tolerance did not allow for that. This is likely, not proven.
- Under the frozen rule the failure blocks SUPPORTED and CONTRADICTED, so the main run exits 1. The verdict would be NOT DIAGNOSTIC without it (all |Z| < 2).

## Hand estimates (frozen), scored

- **Met:**
  - HE1: N 21 / 26 / 15 / 31.
  - HE2: R_200c(0) 210.4 kpc; z_1/2 1.20.
  - HE3: the 2σ line is |ρ| ≥ 0.45.
  - HE4: median t_inf 8.00 Gyr; Eridanus II at 0.
  - HE5: NOT DIAGNOSTIC with a weakly positive ρ.
- **Missed:**
  - HE6, partly. The NFW-profile power of 0.05 is inside < 0.15, but the SIS-profile power of 0.18 is just below my 0.2–0.4.

## Disclosures

- **Dry run of sections 1–4 before the main run.** This covered data, frame and MAH only; no orbit and no statistic was computed. It showed two things:
  - a crash in the FG001 slice marker (fixed: the marker line carries a trailing " reproduced");
  - the C-FRITZ V_rad failure.

  The criterion was not changed. A labelled POST-HOC diagnostic row was added before the main run.
- **Frozen wording made concrete in code:**
  - "relative energy drift" is |E_end − E_0| / (v0²/2);
  - the excess draws ε_k use seed 4630, which the criteria did not name.
- **The MUTATE permutation** has one fixed point (Tucana II).
- **The post-hoc file was run twice.** P4 was added after reading P3, because P3's mocks drop CFG344's luminosity term. P1–P3 are deterministic and unchanged between the two runs.
- **CFG344 record inconsistency.** Its README bracket table gives the SIS (V2) canonical ultra-faint offsets as −0.09 (z_inf 3) and −0.21 (z_inf 1), but its committed JSON gives −0.048 and −0.224. The z_f 6 and 10 rows differ too. This lane uses the JSON.

## Caveats

- **LMC:** the LMC's own potential is ignored. Six of the 21 are LMC candidates, and their infall times move strongly between hosts: for example Carina II is 7.6 Gyr (law) but 0.84 Gyr (NFW). S3, which drops them, has the same sign.
- **Hosts:** they are spherical, smooth and point-mass, with no dynamical friction and no Hubble flow in the backward orbits. The growth is ΛCDM-calibrated: Correa+15 via CFG344, whose formulas CFG344 flags as transcribed from memory.
- **Infall definition:** t_inf depends on the R_200c boundary. The fixed-300 kpc row is about 50 % censored.
- **Motions:** they are Gaia DR2 (Fritz). The EDR3 row (S4, N = 31) has the same sign and is weaker.
- **Predicted slope:** it comes from CFG344's population medians at z_inf 1 / 2 / 3, extrapolated linearly in log M_c. It is not a per-object CFG344 prediction.
- **What would decide it:**
  - a larger or better-measured sample (Gaia DR4);
  - a per-object CFG344 σ prediction that includes its luminosity term;
  - a published infall-time table, which would need the owner's go to download.

## Files and run

`FROZEN_CRITERIA.md`, `cfg463_ufd_infall.py` (`.out`, `_results.json`; `CFG463_MUTATE=1` gives the `_MUTATE` pair), `cfg463_posthoc.py` (`.out`, `_results.json`).

```
python3 campaign_fresh_gravity/CFG463_ufd_infall_order/cfg463_ufd_infall.py                  # ~4.5 min, exits 1 (C-FRITZ)
CFG463_MUTATE=1 python3 campaign_fresh_gravity/CFG463_ufd_infall_order/cfg463_ufd_infall.py  # ~4.5 min
python3 campaign_fresh_gravity/CFG463_ufd_infall_order/cfg463_posthoc.py                     # ~1 min, POST-HOC
```
