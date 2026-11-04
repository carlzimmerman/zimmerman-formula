# WG3_bound_only_web_rule: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** WG2 (6856666719) found, under its post-result amendment A2, that the law alone from a baryons-only start misses CMB lensing on both sides:
- off on the web (R0): r 0.0002-0.31;
- QUMOND on the web (R1): r 11-6,900.

WG2's README and the PAPER67 v1.1 draft say "no rule on record lands there". Only R0 and R1 were tried. This lane tests the one web rule the record already has. It is expected to stay near R0, because baryons alone reach turnaround almost nowhere without the law; that expectation is written here before any run.

κ = ½ FITTED. The cold sector stays retired; the T1 rule is borrowed from it as a test, adopting nothing (owner 11-04: test lanes may reopen frozen or retired items). Not theory closed. Nothing here says the data favour the framework. No downloads.

Owner 2026-11-04: "lets go!", after WG2.

## Question
Does the record's bound-only switch land CMB lensing between law off and law on? That switch is CFG354's T1, as run on the mesh in CFG359. It turns the law on only where the tidal tensor says a region has passed turnaround, and leaves it off on the linear web.

## Rule (CFG359 FROZEN_CRITERIA lines 45-57, copied)
- **Deformation tensor:** t_ij = FFT⁻¹[k_i k_j δ_k / k²], eigenvalues l1 ≥ l2 ≥ l3. Here δ is the baryon field, the only clustering matter, with WG2's CIC deconvolution.
- **Switch:** f = clip(½ + (l2 − τ)/(2ε), 0, 1), with ε = 0.077 (CFG354's ε_min).
- **Phantom:** QUMOND's phantom density −div[(ν − 1) g_N] is multiplied by f cell by cell. Newton is unchanged.
- **Threshold:** τ = (Δ_ta − 1)/3, with Δ_ta = 9π²/16 = 5.5517, the EdS value. The record states it as the rational lower bound; CFG354 FROZEN_CRITERIA line 13 and CFG359 line 117.
  - The record's z-dependent Δ_ta comes from a ΛCDM shell ODE. It is not used: it is a ΛCDM input, and any larger Δ_ta only switches the law on less.
- **Rules run:**
  - **T1:** as above. This is the record rule and is graded.
  - **T1V:** T1 with f = 0 where l3 < 0 (CFG359's filament veto). Reported only.
  - **T1τ0:** τ = 0, i.e. any l2 > 0 switches the law on (CFG359's MUTATE setting). Reported only, as a bracket member toward R1.

## Everything else as WG2
- WG2's engine (`wg2_pm.py`), its ICs, backgrounds B1/B2, box, steps, snapshots, projection, PR4 grading and r.
- WG2's engine is imported read only; the T1 rules wrap its potential.
- a0 TIE, canonical footing, z_on 50.

## Run matrix
- **T1:** {B1, B2} × A_s {1e-9, 4e-9}. 4 runs.
- **T1τ0:** {B1, B2} × A_s {1e-9, 4e-9}. 4 runs.
- **T1V:** B2, A_s 2.1e-9. 1 run.
- **K5:** T1, B2, A_s 2.1e-9 at 128³ and 192³. 2 runs.

## Labels
- **Per rule, over its four members:** WG2's thresholds. FAILS LOW if every r < 0.5; FAILS HIGH if every r > 2; WITHIN ×2 if every 0.5 ≤ r ≤ 2; STRADDLES otherwise.
- **T1 is the graded rule.**
  - If T1 FAILS, the record line becomes: "no rule tried lands there: off, QUMOND on, or the record's bound-only switch (T1)".
  - If T1 reads WITHIN ×2, it is reported as a hit to be verified. That requires K5, K8 and a 256³ check, frozen before it is run.
- **T1τ0 and T1V:** reported with their per-run labels.

## Checks (all must PASS before any label is read)
- **WG2's K1-K3.** Re-run on the imported engine, same tolerances. K4b on this lane's T1 B2 A_s 2.1e-9 128³ run, tolerance 10 %.
- **K8, switch code test:**
  - (a) With τ = −10⁹ the T1 potential equals R1's, and with τ = +10⁹ it equals R0's, both to 1e-6 relative, on a random 32³ field.
  - (b) The closed-form eigenvalues equal numpy `eigvalsh` to 1e-5 relative to the largest eigenvalue, on 1,000 random symmetric tensors.
- **K5 resolution:** the 192³ run must give the same single-run label as 128³. If it doesn't, the T1 label carries NOT CONVERGED.
- **MUTATE:** WG2's Poisson-halved K1 must FAIL on the imported engine. Outputs carry `_MUTATE`.
- **Diagnostics:** the volume- and mass-weighted ON fraction, mean f, is reported at each snapshot.

## What this lane can't say
- The mesh is 12.5 h⁻¹ Mpc. Turnaround below the cell scale is invisible to the switch.
- With Silk-damped baryons-only initial conditions there is little sub-cell power to collapse without the law. That is a property of the field, not only of the mesh. K5 checks 8.3 h⁻¹ Mpc.
- Everything WG2 can't say also holds here.

## Output
- `wg3_pm.py`: wraps WG2's engine and adds the T1 rules and K8.
- `wg3_run_all.py`: the 11 runs.
- `wg3_grade.py`: imports WG2's projection and grading; writes `wg3_results.json` and `wg3.out`. MUTATE writes `_MUTATE`.
- `README.md`.
