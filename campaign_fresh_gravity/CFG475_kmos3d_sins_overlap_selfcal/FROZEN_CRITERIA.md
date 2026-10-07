# CFG475: can the 5 KMOS3D × SINS overlap galaxies support a self-calibrated a₀(z ≈ 2) test? Pre-flight. FROZEN before any script exists

Owner chat 10-07 ("keep working"); taken with the orchestrating session's go (CFG386 follow-up). κ = ½ fitted; both footings. No DM particle.

**Mandatory conditions** (CFG385 self-calibration, plus the lesson from the neutrinos chat's CFG400–402 on Genzel+2017). Self-calibration frees only the baryonic normalisation per disc, so an assumed exponential baryon shape makes a₀ absorb the shape mismatch (a 3-dex spread; CFG400 INVALID). A galaxy qualifies only if ON DISK it has all of:
- (Q1) per-radius rotation velocities at ≥ 4 radii spanning g_obs by ≥ 6.4× (CFG385/386);
- (Q2) a RESOLVED gas surface-density profile (CO or HI maps; not an assumed exponential, and not Hα, which traces star formation, not gas mass);
- (Q3) a resolved stellar-mass profile.

**Data checked.** `data_assembly/kmos3d_cubes/k3d_C1_sins_overlap.csv` (the 5 overlaps), the KMOS3D fit tables (`k3d_fits_main_final.csv`), CFG280's SINS AO table, and any CO/HI product for these IDs under `real_research/data/`.

**Verdict.** RUNNABLE if ≥ 1 galaxy meets Q1–Q3 (score it only if ≥ 5 do). NOT POSSIBLE otherwise, with the count meeting each condition.

**Control.** The script must find the 5 overlap rows (K1).

**MUTATE.** Pretend every galaxy has a gas profile (Q2 forced true). The verdict must change only if Q1 and Q3 also pass. Report what it returns; exit 1 if the counts change.
