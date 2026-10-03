# CFG303 — Addendum 3 to the frozen criteria (52976ec22), written before either replacement below was evaluated

**What had been seen when this was written:** the outputs of the R1/R2, KURVS, MUSE-DARK, CFG274 and X-COP runs, and the S5 post hoc. Also:
- CFG90's README and its RC100 loader lines: it reads `real_research/data/rc100_nestorshachar2023_table3.csv` and uses `logMbar_Msun`, the joint-fit posterior (LCDM-MODEL), in a thin-disc g_bar;
- CFG213's NOEMA3D loader (Z1.4 bin: `logMstar_SED`, `logMgas_CO_P1`, `Re_disk_fixed_kpc`, `Vc_at_Re_disk_kms`, `sigma0_kms`, and the LCDM-MODEL `fDM_Re_disk` / `logMbary_dyn`).

No native CFG90 or NOEMA3D number had been computed.

## A3.1 CFG90 (the CFG52 re-derivation; STANDING §4's pooled z ≥ 1.5 line and CFG289's shift)
- **Replacement:** in a second scratch mirror, the file CFG90 reads is overwritten with the corrected table (CFG289's six-field values), with `logMbar_Msun` replaced by R1's sample-B native log M_bar = log10[M★,SED (1 + μ_t18)]. M★,SED is RC100 Table 3 column 6 (transcribed, gates T1–T2 passed); μ_t18 is CFG217's function.
- **Run:** `cfg90.py` unmodified. Its outputs are copied back as `cfg90_LCDMFREE*`.
- **Reported:** the pooled z ≥ 1.5 flat and rival offsets and the RC100 counts, set against the committed run and against CFG289's corrected-file run, if that is on disk; otherwise against a corrected-file run made the same way in the mirror.
- **C-ii:** the unmodified original file in the mirror reproduces the committed `cfg90_results.json` numbers.
- **C-i:** the corrected file with `logMbar_Msun` left as the posterior reproduces the corrected-file run.

## A3.2 NOEMA3D (CFG213's Z1.4 bin)
- **Native rows:** g_bar = (M★,SED + M_gas,CO) × `disc_v2(1, R_e, R_e)`/R_e, with R_e = `Re_disk_fixed_kpc` (photometric, held fixed in the authors' fit) and CFG216's `disc_v2`. g_obs is exactly CFG213's Z1.4 construction, (V_c² − (3.36 − α) σ₀²)/R_e at α = 3.36 and 1.68 (V_c is MODEL-OTHER, `halo_in_fit = yes`).
- **Estimator:** CFG213's `deltas`, `med_ci` and `verdict`, with its bootstrap state as committed (BINS loop exec'd), and its robust rule.
- **C-ii:** this is CFG213's committed Z1.4 entries, already reproduced in the R1/R2 run.
- **C-i:** the committed g_bar through the native formula reproduces the committed Z1.4 fit-route cells.
