# GH8_ksz_velocity_hardened

**Question.** GH7's kSZ shortfall was void because its control missed. With hardened velocities and the control run first, is Zhang's gas continuing to about 1.8 R_vir (route E's need on KiDS lensing, GH2) present around MW-mass centrals?
ACT DR6.02 NILC T × 326,253 DESI DR1 centrals, log M★ 10.6–11.0. Criteria 5626f97373; every change after that is in `AMENDMENTS.md`.

## Verdict: BELOW ROUTE E'S NEED (frozen class), and limited by the mass scale

The class agrees across all three R values. **Read it as a strong lean, not an exclusion**, because a stellar-mass offset of about 0.2 dex would remove it, and the control only just passed after three fixes.

| matched amplitude (A = 1 is Zhang's gas), R_fm = 1.01 | k = 1 | k = 1.8 | k = 3 |
|---|---|---|---|
| all centrals | +0.55 ± 0.34 | **+0.26 ± 0.19** | +0.23 ± 0.16 |
| passive (212,568) | +0.68 ± 0.40 | +0.38 ± 0.24 | +0.34 ± 0.22 |
| star-forming (113,685) | +0.12 ± 0.67 | −0.06 ± 0.36 | −0.04 ± 0.27 |
| north (171,586) | +0.43 ± 0.44 | +0.22 ± 0.25 | +0.19 ± 0.20 |
| south (154,667) | +0.72 ± 0.59 | +0.36 ± 0.34 | +0.36 ± 0.29 |

- R_cut 1.05 and R_ctx 0.99 give A(1.8) 0.25 and 0.27. Jackknife σ is 0.18, the same as the shuffle σ.
- **No detection:** null χ² 10.9/8, shuffle p 0.21; A(1.8) shuffle p 0.077.
- **Gas ending at R_vir is not excluded** (1.3σ below 1), and **extent is not measured:** S(1.8 − 1) is 2.4–2.6, under the gate of 3.
- Gas to 1.8 R_vir sits about 3.9σ below A = 1, on statistics alone.

| Control (all BGS, blank pixels dropped) | N | A | S/N | shuffled S/N |
|---|---|---|---|---|
| log M★ > 10.5 | 862,078 | 0.58 ± 0.14 | **4.27** | +0.67 |
| log M★ > 11 | 289,467 | 0.79 ± 0.24 | 3.32 | −2.08 |
| log M★ > 11.25 | 91,159 | 1.95 ± 0.62 | 3.14 | −1.55 |

## How it could be wrong

1. **Stellar-mass scale (the main limiter).** The model scales with M★, and CIGALE masses are not Zhang's. If CIGALE is 0.2 dex high, A(1.8) becomes about 0.41 ± 0.30 and A + 2σ reaches 1. I did not measure this offset.
2. **Control is marginal, after fixes.** It went S/N 3.81 (GH7) → 168 (broken, discarded) → 4.05 → 4.27. All fixes followed from failed checks or odd nulls, but they were made after seeing results, and 4.27 clears a threshold of 4 as the best of three samples.
3. **β is inherited.** A scales as 0.44/β_true. Reaching A + 2σ = 1 needs β_true ≈ 0.28 (b ≈ 2.4 at f 0.66), or lower native growth, whose value I did not derive here.
4. **Velocities are imperfect.** Raw v_rec has large coherent radial means per z shell, a systematic of the survey selection. These were removed, but data rms is 194 km/s against the mock's 264. K2 fails (P(k) off by 16.7 %). R_cut barely tests the low-k excess.
5. **Things that lower A without removing gas:** miscentring, satellites leaking into centrals through fibre incompleteness. **What raises it:** two-halo gas, which makes the shortfall firmer.

## For the theory

- GH2's route needed Zhang's gas to continue to about 1.8 R_vir. tSZ (GH5) lacked it at 0.22 keV; this temperature-free column also comes out low. Cool gas no longer readily rescues that need, subject to the limits above.
- This does not say the law wins. GH2 already found the law fits KiDS better, and neither model is confirmed here. Route E's lensing gap, about 0.3–0.5 dex in M200, remains unsolved. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Disclosures

- **Not blind:** GH7's MW-mass number was seen first. One round only was frozen; there were no further hardening rounds.
- **Discarded runs:** the first control (S/N 168, MUTATE failed) and the first MW-mass run (null offset; passive 0.47 with p 0.08). Their defects, blank map regions and mean CAP × mean v, were real and are in `AMENDMENTS.md`; GH7 also has the blank-region defect.
- **Frozen text corrected afterward:** the β direction.
- **Memory:** `gh8_vel.py` peaked at 6.6–7.1 GB (limit 6 GB) while other zoom jobs ran.

## Checks

- **PASS:** K1 iteration no worse (r 0.756 vs 0.737); K3 r_mock 0.756; K4 injection 1.0000 on all control samples; MUTATE: control shuffled |S/N| < 3 and flip exact; MW-mass flip exact, shuffled p 0.32.
- **FAIL:** K2.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENTS.md`, `gh8_vel.py`, `gh8_control.py`, `gh8_mw.py` with `.out` and `.json`. Run in that order after GH6's and GH7's caches, with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`. Work files are in `_external_data/gh8_work/` (not committed).

**Forward note (GH9_cigale_chen_mass_offset):** the offset is measured: CIGALE is about 0.19 dex below the Chen-method masses. The class survives (A(1.8) 0.24 ± 0.19) and is worded "below Zhang-normalised gas at every extent". Limit 1 above is superseded: its 0.2 dex and 0.41 ± 0.30 were a linear rescaling; rebuilt break-even is about +0.27 dex.
