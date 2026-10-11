# CFG624: NO COLD ENERGY. Removing it fixes nothing that is in tension. It breaks clusters, the Bullet Cluster, Local Group timing and cosmic shear.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (803cef306).
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled. The kernel is the repaired ν_mono, with no EFE. No particle of any kind is added. Not "theory closed". This lane runs IN ADDITION to the candidate-B (cold-energy settling) programme and changes no existing lane.
- **Model (NCE):** baryons plus the law a₀ = κc√(Gρ_DE), with the phantom acting as gravity (QUMOND form).
  - It has no supply edge, catchment, cap or compensation.
  - The background is open: Ω_b 0.0493, Ω_Λ 0.68623 (ρ_DE held, so a₀ keeps its footings), Ω_k +0.2645, age 17.77 Gyr.
- **Scripts (run from the repository root):**
  - `cfg624_static.py`: G1, G2, G4 (≈ 20 s).
  - `cfg624_merger.py`: G3 (≈ 25 min, one thread).
  - `cfg624_pm.py` with the launcher `run_624.py`: the G5 PM.
  - `cfg624_shear.py`: G5 scoring.
  - `cfg624_cmb.py`: G6 context.
  - Every M-* control is run inside these scripts, and all of them pass.
- **Outputs:**
  - `*_results.json` and `*.out` for each script.
  - `runs/` holds compact copies of the PM spectra JSONs and the NCE merger time series. The full work files are in `../_external_data/cfg624_work`.

## The identity, declared before any run
Inside galaxies, candidate B's settled cold energy IS the law's phantom inside the census edge. For f_ret ≈ 0.1 that edge lies beyond every R_HI. So NCE and B are identical for:
- SPARC;
- central ellipticals (SLUGGS);
- the MW outer slope;
- the isolated-lens inner mass.

**Removing cold energy cannot touch the galaxy-scale tensions.** G1 confirms this numerically (Δrms = 0).

## Per-gate results

| gate | NCE (no cold energy) | candidate B (record, same pipeline) | raw data | NCE verdict |
|---|---|---|---|---|
| G1 SPARC RAR (rotmod, Υ 0.61) | rms 0.1003 / 0.1013 dex; A3 = 1.00 | 0.1003 / 0.1013 (census edge, CFG515) | 175 galaxies | **PASS** (identical to B) |
| G2 X-COP, 12 clusters at 0.80 R500 (ν_mono) | η = M_HSE/M_NCE = **1.82 ± 0.23 / 1.68 ± 0.22**; missing **3.09 / 2.75 M_b** (15σ / 13σ); NCE gives 0.55 / 0.60 of the measured mass | identity reading 0.946 ± 0.080 (CFG4) | corrected hydrostatic audit | **FAIL** |
| G3 Bullet (CFG621 machinery, phantom untruncated) | lensing peak on the stripped gas: f = 1.029 / 1.031, **Z_B +7.87 / +7.88** (stable, spread 17–20 kpc) | α = ∞ EXCLUDED (+7.86 / +8.06); α = 0 UNDETERMINED (CFG621); v4 VOID | Clowe+06 offset f_obs 0.045 ± 0.125 | **EXCLUDED** |
| G4a LG timing (deep-MOND two-body, NCE age) | v_r **−208 / −225 km/s**; z_meas +22 / +26; **z_full +4.90 / +6.35** | shared catchment M1: z_full −0.11 / −0.10 (strict radial +4.4) | −109.3 ± 4.4 km/s | **FAIL** (too fast) |
| G4b groups, Tian+26 BFJR (N 63) | mean +0.010 / −0.010 dex (Z +0.31 / −0.31) | P2 consistent supply +0.060 / +0.043 (Z 1.65 / 1.20) | Tian+26 | **PASS** |
| G5 cosmic shear, NCE-S (law in bound regions), 256³ canonical | the switch never turns on (f_sw volume 0 at every epoch), so this is Newtonian baryons. σ8 = 0.014; model ξ± ≈ **5e-7 (KiDS) / 3e-6 (DES)** of the data; χ² 226 / 162 on 51 / 12 points (p 7e-24 / 2e-28) | B on the same 20 KiDS points: χ² 40.0 vs NCE 157 | KiDS-1000, DES Y3 ξ± | **FAIL** |
| G5 NCE-E (law everywhere), 128³ canonical, POST-HOC, reported only | runaway growth: σ8 particle 6.3, gravitating 39.8 (relative to mean baryons); model/data **×13.7 (KiDS), ×6.3 (DES)** on the kept points; χ² ≈ 5e4 | B χ² 38 / 27 on the same intersections | same | would FAIL (no verdict weight) |
| G6 CMB | UNTESTABLE framework-native (no derived early-universe law). Context only: with A5 read literally (GR + baryons, CAMB, inherited), the first peak sits at ℓ ≈ 612 with height 13,800 μK², and the next at ℓ ≈ 1750 | (B keeps CDM-like cold energy at z ~ 1100) | recalled Planck: first peak ℓ ≈ 220, about 5,700 μK² (PROVISIONAL; raw TT not on disk) | **UNTESTABLE** |

Footing pairs are given as canonical / alt.

## Missing mass where NCE fails
- **Clusters:** the law on baryons supplies 55% / 60% of the hydrostatic mass. The missing mass is 3.1 / 2.75 × the baryons. A positive hydrostatic bias makes it worse: η 2.27 / 2.10 at b = 0.2.
- **Bullet:** the lensing needs a collisionless mass at the galaxies of 4.6× / 4.9× the aperture baryons (CFG4 H5). NCE has only the stars.
- **Shear:**
  - With the switch kept, the lensing power is about 10⁵–10⁶ too low, because baryon-only seeds stay linear and Newtonian.
  - With the law everywhere, it is ×6–14 too high on the kept points.
  - Neither branch works, and no unforced rule lies between them. Choosing one would be a knob.
- **LG:** this one fails the other way. The law between two baryonic galaxies over 17.8 Gyr is too strong, giving −208 km/s against −109.
  - Even at the 13.8 Gyr age, z_full is +2.6 / +3.8 (CFG522 M3, reproduced).
  - **Correction to F68:** the record's "baryons-only LG reaches −109 km/s" was computed with FP9's H_Y separator law, not the current law.

## MUTATE and controls (all pass)
- **M-G1:** the census row reproduces CFG515 (Δrms 0). With a₀ → 0 (Newtonian baryons) the rms is 0.397, so G1 fails as it should. The harness rms0 equals CFG39's.
- **M-G2:** CFG4's η and identity reading (cold energy restored) are reproduced to 1e-9. With a₀ → 0, η = 6.73.
- **M-G3:** the edge-kept code path reproduces CFG621's α = ∞ cell exactly (f 1.027185, Z_B 7.857480).
- **M-G4:** at 13.80 Gyr, CFG522 M3 is reproduced to < 0.01 km/s. With a₀ → 0 there is no timing solution.
- **M-G5a:** this lane's general projection code reproduces CFG592's χ²_F for CFG530 LR L100 N512 (40.02 / 45.52 can, 46.21 / 46.87 alt) to < 0.001.
- **M-G5b:** the a₀ → 0 PM run was not run (see the memory constraint below). NCE-S has f_sw ≡ 0, so it already IS the Newtonian-baryon run.
- **M-G6:** the peak finder recovers the ω_c = 0.120 control peaks (ℓ 221 / 537 / 816).

## Disclosures
- **Memory constraint (orchestrator, mid-lane).** The CFG596 1024³ P1 run had been aborted at 10:56 by its swap guard. At 12:10 the orchestrator asked lanes to run no new job above about 3 GB RSS, and at most 2 processes, until P1 is running again. So:
  - the G5 queue was stopped after T1 canonical 256³;
  - S1 canonical 256³ was killed 5 s after it started;
  - NOT RUN, deferred: T1 alt 256³, S1 both footings at 256³, the S0 a₀ → 0 run, and every 512³ run.
  - The NCE-E number above comes from a POST-HOC 128³ run with NSEED 128 (1.8 GB). It used a different white-noise realisation and resolution, so it carries no verdict weight.
  - G5 therefore has a frozen-rule verdict for **NCE-S canonical only**. Alt is deferred (its switch criterion is the same, so f_sw ≡ 0 is expected, but this is not run).
- **G5 support.** NCE's spectrum is so different from B's that the CFG592 support rule keeps 51 / 12 points at 256³, where B's boxes kept 0.
- **G3.**
  - Without the r_t truncation, the gridded phantom is not renormalised up to the 4000-kpc profile mass (that would pack mass from outside the grid into it); it is only capped.
  - The progenitor gas uses CFG599's hydrostatic setup, which includes the cold mass, so under NCE it is over-pressured. This follows from G2.
  - The Harvey β̄ is unscorable (β̄ ≈ 1.03, gas-dominated windows).
- **G6.** The peak-finder range was widened from ℓ ≤ 1400 to ≤ 2450 after the first run, which found only one NCE peak. Context only.
- **CAMB** (G5 ICs, G6) is inherited GR-linear machinery and is flagged.
- **A flat no-cold-energy universe** (Ω_Λ 0.951) would raise a₀ by ×1.18 and break both fitted footings. It was not run.

## Reading
Removing cold energy helps nowhere that is in tension. The galaxy-scale tensions are untouched by construction:
- central ellipticals;
- the MW outer slope;
- the isolated-lens inner mass.

Galaxies and the Tian+26 groups pass exactly as before; groups do marginally better than B (+0.01 vs +0.06 dex).

Everything that depends on mass beyond the law fails, and fails decisively:
- **Clusters:** short by ×1.7–1.8 (13–15σ).
- **Bullet:** lensing stays on the gas (Z_B ≈ +7.9).
- **Cosmic shear:** off by orders of magnitude either way, depending on whether the law is switched or global.
- **Local Group:** the pair now attracts too strongly (z_full +4.9 / +6.4), which also corrects the record's F68 −109 km/s claim.

The tensions that motivated the test live in the profile and settling of cold energy inside the edge, not in its existence. On this evidence the cold energy's mass is still required.
