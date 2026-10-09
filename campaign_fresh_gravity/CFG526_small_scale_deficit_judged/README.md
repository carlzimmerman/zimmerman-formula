# CFG526: the small-scale power deficit, judged on the framework's own terms and against data. A: ENGINE ARTEFACT (both footings). B: NOT DIAGNOSTIC (both footings)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (1c31dc2c1).
- **Scripts:**
  - `cfg526_profiles.py` (A). `compute` re-evaluates each saved z = 0 state with the engine's own `forces` (imported unchanged) and caches profiles in `../_external_data/cfg526_work/`. The default run writes `cfg526_profiles.out` / `.json`. `CFG526_MUTATE=1` writes `_MUTATE` (M2 emptied core; exit 1 = detected).
  - `cfg526_data.py` (B). Writes `cfg526_data.out` / `.json`; the `_MUTATE` mode applies 0.5 r and r = 1.
  - `cfg526_posthoc.py` (not gating): the lensing-tracer side of B.
  - `cfg526_results.py` collects everything into `cfg526_results.json`.
- **Settings:** κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; flat a0; ν_mono. The cold energy's MASS is still required. Not "theory closed". No new PM run was made, and nothing was downloaded. All literature values are recalled and PROVISIONAL.

## Engine integrity

The engine's z = 0 state was recomputed from the saved positions, and it reproduces each run's own diagnostics:
- e_sum and q_max agree to ≤ 1.2e-7 relative, and n_catch agrees exactly.
- The other shared diagnostics agree to ≤ 8.5e-6.
- P(k) agrees to ≤ 1e-7.

The total potential was captured exactly. The S0 null holds: δ_grav − δ ≤ 2.4e-7 of the peak. Every gating run passes K1–K3. NOCOMP_L25 "fails" K3 at 1.2e-6 against the 1e-6 limit; this is float32 summation of the mean, and that run is not gating (dated note below).

## A: does the engine's halo match candidate B's law profile?

**The test.** Inside each host's census edge, B's total enclosed mass is M_law = M_b,all + (ν − 1) M_b,ret, built from the run's own baryons and the engine's f_ret map. It is compared with the engine's gravitating mass M_grav (particles + e − comp) in the 100 densest scored hosts.
- **Hosts:** log M_ta 12.4–14.6 at L50, 11.8–14.0 at L25.
- **Edges:** 1.9–3.0 cells.
- **Radii:** all scored radii lie at r/r_M ≈ 6–45, i.e. deep MOND.
- **Columns in the table:**
  - **R** = M_grav / M_law.
  - **D_law** = the law's mass / the matched S0 halo's mass (D_eng: the engine's gravitating mass / S0's).
  - Both are core medians (≤ 2 cells) from `cfg526_profiles.json`.

| run | L50 R | L25 R | L50 D_law | L25 D_law | L50 D_eng | L25 D_eng |
|---|---|---|---|---|---|---|
| census canonical (old draw) | **0.728** | **0.773** | 1.023 | 0.953 | 0.684 | 0.790 |
| census alt | **0.649** | **0.506** | 1.072 | 0.954 | 0.621 | 0.656 |
| K1 (f_ret = 1) | 0.542 | 0.326 | 1.147 | 1.204 | 0.585 | 0.390 |
| NOCOMP (no compensation) | 0.898 | 0.947 | 1.173 | 1.092 | 1.013 | 1.041 |
| CFG524 R2-can / R2-alt | 0.771 / 0.721 | 0.715 / 0.578 | 1.06 / 1.10 | 0.97 / 1.00 | 0.87 / 0.82 | 0.86 / 0.77 |
| L100 canonical / L200 can / L200 alt (reported) | 0.735 (L100) | 0.801 / 0.734 (L200) | 1.103 | 1.163 / 1.252 | 0.781 | 0.929 / 0.916 |

**Frozen verdict, both footings: ENGINE ARTEFACT.** Core R is below 10^-0.1 in both boxes. MUTATE M1 is detected: NOCOMP's core R (0.898 / 0.947) is above the census run's (0.728 / 0.773). MUTATE M2, the emptied core, returns ENGINE ARTEFACT (exit 1).

### What it says

1. **The law does not ask for de-concentrated halos.** At resolved radii the law's own halo is as centrally massive as S0's (D_law 0.95–1.17). It is in fact heavier than the run's particles inside the edge: M_p/M_law ≈ 0.71–0.93 per radius in the census runs. In deep MOND, B wants the catchment's cold energy concentrated within the census edge, not drawn out of it. So the deficit against S0 is not the framework's prediction.
2. **The engine removes mass the law needs.**
   - The engine's gravitating core holds only 0.73 / 0.77 (canonical) and 0.65 / 0.51 (alt) of the law's mass.
   - Without the compensation, the engine sits within 0.05 dex of the law (NOCOMP 0.90 / 0.95).
   - The shortfall tracks the grid, not a physical radius. In cell units, core R is 0.80 / 0.74 / 0.73 / 0.77 from L200 to L25 (canonical). At fixed physical radius it deepens with resolution: log R goes −0.112 → −0.266 at r = 0.23 Mpc/h (L50 → L25, canonical) and −0.150 → −0.335 (alt). That is the convergence failure an artefact shows.
   - The L25 side of that comparison has only 10 hosts in the shared mass range.
3. **Attribution: two engine ingredients, not the law.**
   - Against the law applied to the engine's own pressure-filtered MOND input (R_in), the census cores are at or above it: 1.15 / 1.36 canonical and 1.03 / 0.88 alt. The filter puts 54% of the baryons at k_J(10⁶ K) ≈ 0.45 h/Mpc, so the engine's phantom in cores is far below the phantom of the real baryons.
   - The per-catchment draw then takes q·s_c out of those same cores. The draw is the step that pushes the engine below the law; NOCOMP does not go below.
   - K1 is worse (0.54 / 0.33) because its larger draw is spread over the same cores.
4. **Consequence.**
   - The TENSION against S0 at k ≳ 2 should not be read as a failed prediction of B. It is an engine defect, and it sits in the same place CFG521/524 found: the draw.
   - A law-respecting rule would have to leave the in-edge mass at M_law. That means taking the compensation from outside the census edge (the shell out to the turnaround ball), and sourcing the phantom from unfiltered retained baryons. That is a new rule; it is not run here.

## B: against data

**Prediction used.** r = P/P_S0 (particles) at z = 0.5. It is mapped to an A_mod equivalent: A_eq = (r F P_NL − P_L)/(P_NL − P_L), averaged over k = 1, 2, 4.

**Literature (PROVISIONAL):**
- Amon & Efstathiou 2022, KiDS-1000: A_mod = 0.858 ± 0.052.
- Preston, Amon & Efstathiou 2023, DES Y3: 0.82 ± 0.04.
- Feedback bands F(1, 2, 4): fiducial 0.90–0.98 / 0.85–0.95 / 0.80–0.92 (vD20 / BAHAMAS / FLAMINGO, recalled).

| case (z = 0.5, conservative r 1.056 / 0.993 / 0.774 canonical) | A_eff | pull KiDS | pull DES |
|---|---|---|---|
| framework, no feedback (F = 1) | 0.947 | +1.72 | +3.19 |
| framework, fiducial feedback (hi / lo end) | 0.894 / 0.774 | +0.69 / −1.61 | +1.85 / −1.15 |
| LCDM, fiducial feedback (hi / lo end) | 0.940 / 0.813 | +1.58 / −0.86 | +3.01 / −0.17 |

Alt is the same to 0.002.

**Frozen verdict, both footings: NOT DIAGNOSTIC.**
- **Not excluded.** With F = 1 the particle suppression is weaker than the data's A_mod, not stronger.
- **But r is not converged.**
  - Canonical fails at k = 2 and 4: at z = 0.5, k = 4, L100 0.827, L50 0.762, L25 0.774. At z = 0 the old-draw series is 0.893 (L200), 0.804, 0.628, 0.585.
  - Alt has no L100 run, so convergence cannot be verified at any k.
- **The lensing-tracer variant moves A_eff by −0.161 (canonical) and −0.133 (alt),** both beyond the 0.04 limit. The gravitating field is far more suppressed than the particles at z = 0, k = 2 / 4:
  - L50 canonical: 0.519 / 0.328, against 0.799 / 0.628 for the particles.
  - NOCOMP's gravitating field is not cut down by any draw: 1.19 / 0.86, against 1.04 / 0.90 for its particles.
- **Lyman-α is not diagnostic.** r(z = 1, k = 4) is already 0.888–0.940 in the small boxes, so the rule flags that a z ≥ 2 snapshot would be needed. None exists.

**Post-hoc, not gating (`cfg526_posthoc.out`).** If shear traced the engine's gravitating field, the crude z = 0.5 estimate with no feedback lands at −3.0 to −3.4σ against both datasets (A_eff 0.685–0.700, L100 and L50, both footings). It lands at −1.1 to −2.2σ in L25, and at −2 to −6σ once any feedback band is added. Read with A, though, this is the engine artefact again: the law's own halo carries more core mass than the engine's. It is not evidence against B. Nothing here says the data favour the framework.

### What would decide B (owner's go needed; nothing downloaded; sizes approximate, PROVISIONAL)

1. **A converged framework P(k, z), computed rather than downloaded.**
   - It needs a law-respecting compensation rule (see A).
   - It needs a run with more dynamic range at k = 1–5 (a 512³ re-run of L50 with that rule, or a zoom), with snapshots at z = 0.3–1 and z ≥ 2.
   - It must output the gravitating field as well as the particles.
2. **Public cosmic-shear likelihood inputs**, so that P(k, z) can be run through the real data instead of the A_mod shortcut:
   - KiDS-1000 ξ± / COSEBIs data vector, covariance and n(z) (KiDS website, about 10–50 MB);
   - DES Y3 cosmic-shear 2pt FITS file with covariance and n(z) (DES data release, about 50–150 MB);
   - a shear-prediction code (CCL or CosmoSIS, pip, about 50 MB).
3. **Optional:** posterior chains for A_mod from Preston+2023 / Amon & Efstathiou 2022 if public (tens of MB); and a Lyman-α P1D table (eBOSS Chabanier+2019 or DESI DR1, < 5 MB) for the z ≥ 2 check.

## Departures and notes (dated)

- **2026-10-09.** NOCOMP JSONs carry none of e_sum / q_max / n_catch / src_sum. K1 was checked on every scalar diagnostic both share (≤ 2.2e-7 relative). S0 runs are gated on K2 and K3.
- **2026-10-09.** NOCOMP_L25 K3: |mean(grav − particles)| = 1.2e-6 > 1e-6. This is the float32 mean of a field whose k = 0 mode is zero by construction; NOCOMP_L50 is 3.2e-7. NOCOMP is not a gating run. It is used only for M1, and its result there does not depend on this.
- **2026-10-09.** The frozen convergence test could be evaluated only at r = 0.23 and 0.39 Mpc/h (canonical) and at 0.23 (alt). The other shared radii have fewer than 10 L25 hosts in log M_ta 12.7–14.3. It fails wherever it was evaluated. The ARTEFACT verdict comes from rule 2 (core R), which needs no convergence.
- **2026-10-09.** K1 runs have fewer scored hosts (41 at L50, 27 at L25), because the f_ret = 1 edge is smaller. They are reported only.

## Caveats

- One seed at 256³. Halo cores are 1–2 cells, and PM forces are softened below about one cell.
- B's law here is the round enclosed-mass rule (CFG516 RM). Baryons are the f_b share of the particles, which trace the matter (there is no cooling or condensation in the PM), and expelled baryons stay in place as gravitating mass (CFG518 convention). The variant without them (R_noexp) raises core R by ≤ 0.1 in the census runs.
- A_mod constraints assume Planck LCDM's linear amplitude. The S0 ICs are Planck-normalised (σ8 = 0.811), and the framework's large-scale σ8 is +1–2%. The A_mod mapping is a shortcut, not a shear likelihood.
- κ, f_b and ρ_Λ are not derived. The cold energy's mass is still required.

## Run

```
nice -n 10 python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_profiles.py compute
python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_profiles.py
CFG526_MUTATE=1 python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_profiles.py
python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_data.py
CFG526_MUTATE=1 python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_data.py
python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_posthoc.py
python3 campaign_fresh_gravity/CFG526_small_scale_deficit_judged/cfg526_results.py
```
