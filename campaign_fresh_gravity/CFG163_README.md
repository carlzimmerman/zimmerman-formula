# CFG163 — KURVS-15's cold gas from archival ALMA: the 1.32-mm dust continuum

- **Plan:** frozen in `CFG163_FROZEN_CRITERIA.md` (9ec06b770), with its addendum for the 1.32-mm continuum (5fc3c4d8e). Both were committed before any file was downloaded or read.
- **Data:** the data chat downloaded, with its user's go, the Ibar Band 6 continuum image and its primary-beam response (e58f0d75b, header facts only). They are 0.4 MB, outside the repository.
  - The CO(2-1) cubes (6.6 GB) were not downloaded, because the plan's power row found them non-diagnostic at both break-evens. **The CO channel was not run.**
- **Script:** `CFG163_kurvs15_dust.py`; seconds per run.
- **Runs:**
  - The main run passes all six checks and exits 0.
  - MUTATE=1 injects a source with μ_dust = 8 at KURVS-15. It reads "detected, > 2.14" (7.9 recovered), as required; exit 0.
  - MUTATE=2 moves the off-source values to the source position. It reads "not detected", as required; exit 0.
  - The two pinned controls move the classification in opposite directions.

## Bottom line

**KURVS-15 is not detected in the 1.32-mm dust continuum. Its dust-traced gas is below 1.90 M* at the nominal calibration: 3σ, Scoville et al. 2016, T_d = 25 K, MAGPHYS M*.**

- **The frozen outcome is "not detected, limit 0.65–2.14".** At the nominal gas-to-dust ratio this excludes flat a₀'s P4 break-even (μ = 2.14) for this disc. It cannot reach the rival's (0.65).
- **The measurement:**
  - The pixel at KURVS-15, which sits at the phase centre (pb = 1.000), reads −5.4 μJy/beam, or −0.1σ.
  - The 1.0″ aperture sum is +28.6 μJy.
- **The noise,** by the frozen rule (a 3–10″ annulus, pb ≥ 0.5, sources masked, robust MAD): 40.3 μJy/beam. The plain std is 40.2. This lies between the archive's two readings (≈ 32 averaged over four windows; 64.6 per window).
- **The power gate passed:** the 3σ limit in μ_dust is 1.90, below 2.14. So the source pixel was read, after the gate, as the plan requires.
- **The limit under the declared variants:**

  | calibration | 3σ limit on μ |
  |---|---|
  | 25 K, nominal | 1.90 |
  | 35 K | 1.75 |
  | gas-to-dust × 2 (sub-solar metallicity) | 3.79 |
  | M* 0.2 dex lower | 3.01 |

  **Only at the nominal calibration does the limit fall below flat's break-even.**

## Reading

- **This is one disc,** so it is a statement about the gas prior of CFG160/CFG162, not an a₀ test. It re-scores nothing.
- **At the nominal gas-to-dust ratio,** KURVS-15's dust-traced gas is below the ~2.1 M* that flat a₀ needs under Kretschmer's pressure correction. Its gas sits where CFG162's map leans rival or holds both within 2σ (μ ≲ 1.9 at s = 1).
- **Three things undo this reading:**
  - a gas-to-dust ratio twice the nominal (sub-solar metallicity at log M* = 10.07 and z = 1.6 is plausible);
  - a lower M*;
  - an HI reservoir that dust does not trace.
  - Under any of these the limit rises to 3–3.8 M*, and it then excludes neither break-even.
- **What would settle it:**
  - CO(2-1) at a depth reaching μ_mol ≈ 1: the archival cubes reach only μ_mol ≳ 5.5;
  - a metallicity for KURVS-15;
  - HI, which no instrument will measure at z = 1.6 before the SKA.

## Controls

- **C0:** both files match the data chat's sha256.
- **C2 (continuum form):** 227.291 GHz, one plane, header beam 1.429″ × 0.850″ (47.6 pixels).
- **C3:** the robust and plain noise estimates agree (40.3 against 40.2 μJy/beam).
- **C1 (injection):** a 10σ point source injected 6″ off-source is recovered at 0.996.
- **C4:** the conversion reproduces CFG142's pre-data value for KURVS-15 (0.2218 mJy at 272.5 GHz).
- **MUTATE:** both pinned controls behave as required.

## Disclosures

- **The first main run crashed before the power gate,** on a type error in the WCS conversion (0-d arrays). It read no source pixel and wrote no output. The fix is a type conversion only.
- **The frozen plan's checks were written for the CO cube,** as C1 injection, C2 frequency axis and C3 noise agreement. They are applied here in their continuum form, which is the only channel run.
- **The injection ignores the beam position angle** (a declared simplification). It tests the measurement code, not the noise.
- **The beam is 1.43″ × 0.85″ per the header,** not the 1.0″ the archive listed. A disc of this size is close to unresolved at this beam.

## Untested (declared)

- HI;
- gas-to-dust beyond the ×2 bracket;
- T_d beyond 25–35 K;
- the dust spectral index (β = 1.8, as in Scoville);
- the CO lines (not downloaded);
- the other nine discs.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.
