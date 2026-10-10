# CFG593: is there one halo profile that fits both cosmic shear and KiDS galaxy lensing? Frozen verdict: NO OVERLAP on both footings. Post-hoc: an overlap opens only if the KiDS lenses carry the ΛCDM SHMR catchment mass, and even then it contains no fully settled law profile

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (433d42278). Date: 2026-10-10.
- **This is DIAGNOSTIC and DATA-DRIVEN.** It asks which total profiles the data allow. Any profile it finds is what the data require. It is NOT a framework derivation. Only the record-rule rows below speak to the framework's own predictions.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled. Flat a0 = κ c √(G ρ_DE); ν_mono; candidate B. The cold energy's MASS is still required; no particle species. Not "theory closed"; nothing here says the data favour the framework. Nothing was downloaded. Other lanes were used read-only.
- **Numbers:** all come from `cfg593_*_results*.json`. Pairs are canonical / alt.

## Scripts (all `nice -n 10`, at most 4 processes with 1 thread each)

| script | what it does | time (shared machine) |
|---|---|---|
| `cfg593_lib.py` | the family, and its evaluation in CFG556's halo model | — |
| `cfg593_shear.py` | constraint (a): CFG556 halo model → CFG590 M1 mapping. `CFG593_MUTATE=1` → MU1/MU2, exit 1 | ~50 min |
| `cfg593_kids.py` | constraint (b): CFG529 f30, constructions A and B, through exact linear operators. `CFG593_MUTATE=1` → MU2, exit 1 | ~17 min |
| `cfg593_side.py` | constraint (c): CFG543 P2 groups and the MW bands. `CFG593_MUTATE=1` → K4 / law member, exit 1 | ~1 min |
| `cfg593_verdict.py` | overlap, convention flags, record rules | seconds |
| `cfg593_posthoc.py`, `cfg593_posthoc_profile.py` | **POST-HOC, not verdict inputs** (dated 2026-10-10): why the KiDS region is empty | ~15 min |

R(k) tables are cached outside git in `_external_data/cfg593_work/`.

## The family (declared before fitting)

The family describes the total profile: baryons + settled cold energy + unsettled cold energy. It has three parameters, the same for every halo. Mass enters only through r_ta(M_ta), r_M and f_ret.

- **x_e:** the settled edge, r_e = x_e r_ta.
- **f:** the fraction of the law's phantom that is settled between r_in and r_e.
- **y:** a full-law core, r_in = y r_M.

Rules:
- The settled cold energy is capped at the supply (1 − f_b) M_ta.
- The unsettled cold energy is NFW-shaped. It is weighted 1 − f inside r_e and 1 beyond.
- Mass is conserved inside r_ta. This fixes the drained-shell depth q; it is not a free parameter.

The grid is x_e from 0.10 to 1.00 (14 values), f from 0 to 1 (11 values) and y ∈ {0, 1, 3, 10}: 574 points per footing.

## Controls (all PASS)

- **K1:** the family code reproduces CFG556's `census|cen` and `census|emg` R(k) to ≤ 8.9e-16.
- **K2:** CFG590's code reproduces its stored A_M1 exactly (|d| = 0).
- **K3 (KiDS):**
  - (i) the linear operator equals CFG504's kids_fin / truncate / window to 2.3e-15;
  - (ii) the lane-convention census edge reproduces CFG529's stored census χ² to |Δχ²| ≤ 0.004 (A 45.57 / 35.84, B 54.10 / 42.43);
  - (iii) CFG529's native ΛCDM gives 22.47 (A) and 22.51 (B), exactly.
- **K4:** the group path reproduces CFG543's P2 mean exactly.
- **KMW:** the f = 1, x_e = 1 member reproduces the law inside 30 kpc (ΔV = 0).
- **K5:** mass is conserved to 3.9e-16.

## Constraint (a): cosmic shear

Rule: |Z| < 2 for both KiDS-1000 and DES Y3 at some log T_AGN in 7.6–8.0. The A_mod values are recalled and PROVISIONAL. R is taken at z = 0.

- **Allowed:** 122 / 115 points of 574 (188 / 171 over the full 7.3–8.3 band).
- **Shape of the allowed region.** It is a diagonal ridge. At small f, the edge can sit at x_e ≈ 0.4–0.6. As f → 1, the edge must move out to x_e 0.70–0.85 / 0.85–1.0. At those x_e the supply cap binds in all 321 halos, so the effective edge is 0.35–0.50 r_ta, which is the emergent edge.
- **Never allowed:** any edge at x_e ≤ 0.20.
- **Grid detail:** see the `Zmax` tables in `cfg593_shear.out`.

**Record rules, Zmax at the best fiducial T:**

| rule | canonical | alt |
|---|---|---|
| CFG556 / CFG541 census edge | 14.36 | 19.34 |
| CFG557 finite-age supply | 11.01 | 14.38 |
| CFG559 kinetic PRIMARY | 7.52 | 10.73 |
| CFG559 kinetic full supply | 11.60 | 15.95 |
| emergent edge | 2.27 (allowed only in the full band) | 0.41 (allowed) |

## Constraint (b): KiDS f30 galaxy lensing

Rule: p > 0.01 in construction A AND construction B.

- **No point of the family is allowed on either footing, in either KiDS convention.**
- **Best values, max(χ²_A, χ²_B), against a threshold of 30.58:**
  - canonical, total profile: 49.43 (x_e 0.1, f 0, y 1);
  - alt, total profile: 41.99 (x_e 0.4, f 1, y 0);
  - lane convention: 54.07 / 42.41.
- **The NFW member (f = 0) also fails:** 50.63 / 56.93.
- **Native ΛCDM passes** (22.47 / 22.51).

**Record rules on KiDS: all excluded.**
- Census edge: 45.57 / 54.10 (canonical), 35.84 / 42.44 (alt).
- Emergent edge: 45.17 / 54.04 and 35.01 / 41.99.
- CFG557: 59.13 / 66.04 and 50.44 / 55.50.
- CFG559 PRIMARY: 57.77 / 63.97 and 48.80 / 53.61.
- CFG559 full supply: 43.32 / 50.87 and 34.49 / 40.04.

## Side constraints (c)

Total profile, groups and MW both passing: 389 / 395 points. In the lane convention only 7 / 22 points pass, because the groups move high once the unsettled mass is dropped.

## Frozen verdict (sections 4–6)

**NO OVERLAP on canonical. NO OVERLAP on alt.**
- The answer is not CONVENTION-SENSITIVE. It holds under the baryons-to-r_ta halo-model variant, the KiDS lane convention, the full 7.3–8.3 feedback band and the groups lane convention.
- The overlap is empty because constraint (b) alone is empty for this family.
- Closest points, judged inside the shear-allowed set:
  - canonical (x_e 0.3, f 0, y 1): shear Zmax 0.41, KiDS max χ² 49.43;
  - alt (x_e 0.85, f 1, y 0): shear Zmax 0.76, KiDS max χ² 41.99.
- **No record rule predicts an overlap.** The emergent edge is the only rule that passes shear (alt; canonical only in the full band), and it fails KiDS. CFG542 makes no profile prediction, because its switch is an input.

**Plainly: within this family, the framework's settled-halo concept, normalised by the census catchment, is in conflict with the combination of cosmic shear and KiDS galaxy lensing.** This is pending the real shear likelihood (CFG592) and the z-dependent R (CFG591). As the post-hoc diagnostic below shows, the KiDS side of the conflict does not come from the profile shape. It comes from the catchment mass the family assigns to the KiDS lenses.

## Post-hoc diagnostic (dated 2026-10-10; NOT a verdict input; written after the verdict was computed)

- **D1. The catchment is light.** The census catchment for the f30 lenses, M_ta = M_g/(f_ret f_b), is 0.768× the SHMR ΛCDM turnaround mass (lens-weighted median, Moster).
- **D2. A heavier catchment fixes KiDS for the NFW member.** Scaling the catchment mass by λ (r_ta ∝ λ^⅓):
  - λ = 1.4 is allowed (A 20.98 / 24.05, B 23.76 / 27.40);
  - λ = 2.0 is allowed;
  - λ = 0.7 and λ = 3 fail.
- **D3 / D4. Both data sets on one normalisation.** CFG556's halo model already uses each halo's ΛCDM turnaround mass. Putting the KiDS lenses on the SHMR ΛCDM catchment as well:
  - 241 / 280 family points pass KiDS;
  - 45 / 49 of them also pass the frozen shear rule;
  - 31 / 26 of those also pass the frozen side constraints.
- **What the post-hoc overlap looks like.**
  - Ranges: x_e 0.35–0.70 / 0.40–1.0, f 0.3–0.8 / 0.3–0.9, y ≤ 3.
  - **It contains no f = 1 point and no f = 0 point.**
  - Closest-to-both point:
    - canonical (x_e 0.5, f 0.6, y 1): Zmax 0.65, χ² A 14.79, B 17.64, groups Z −0.88, MW pass;
    - alt (x_e 0.55, f 0.6, y 3): Zmax 1.02, χ² 14.33 / 17.54.
- **In words:** only about half (30–80%) of the law's phantom is settled. The settled part extends to about 0.5 r_ta, well beyond r200m (0.32–0.33 r_ta). The remaining cold energy stays unsettled and NFW-shaped. The shell beyond the edge is deeply drained (q 0.53–0.95).
  - In the halo model this puts LESS mass than ΛCDM inside 0.3 r_ta: M/M_L 0.35–0.8 at 0.05–0.2 r_ta for log M_ta 13–15.
  - It puts MORE mass than ΛCDM at 0.5 r_ta: M/M_L 1.17–1.34.
- **Does any record rule predict it? No.** Every record rule settles the full law phantom inside its edge (f = 1). The emergent edge is the nearest, and it sits on the shear ridge, but it fails KiDS under both normalisations: D3 SHMR f = 1 gives χ² 45–57 (canonical) and 32–42 (alt).

**What would have to fail to rescue the framework's settled halo:**
1. **The census catchment normalisation of the KiDS lenses.** It would need to be about 1.4–2× heavier, i.e. f_ret about 0.5–0.7× the census value.
2. **AND the "settled = the full law phantom" rule (candidate B's drift-held law profile).** Only a partial settling, f ≈ 0.3–0.9, passes both data sets.

Rescuing it through the recalled A_mod or the KiDS environment model alone is not enough: no family member passes KiDS under the frozen normalisation, in either convention.

## MUTATE (all teeth bite; each MUTATE script exits 1)

- **MU1, the framework's current profile lands outside the shear-allowed region** on both footings:
  - CFG556 census: Zmax 14.36 / 19.34;
  - CFG559 PRIMARY: 7.52 / 10.73, with a minimum over 7.3–8.3 of 5.27 / 8.24. This equals CFG590 (EXCLUDED).
  - The framework census also lands outside the KiDS-allowed region.
- **MU2, ΛCDM lands inside both:**
  - R ≡ 1 gives Zmax 0.86 for shear;
  - CFG529's native ΛCDM gives 22.47 / 22.51 for KiDS.
- **Limitation, reported as declared:** the family's own NFW member (x_e = 1, f = 0) passes shear (Zmax 0.65) but FAILS KiDS (50.63 / 56.93). It carries the census catchment mass and point-mass baryons, not CFG529's SHMR halo. D2 shows the cause is the mass normalisation.

## Disclosures (dated 2026-10-10)

- **Recalled inputs.** A_mod values and survey n(z) are recalled and PROVISIONAL (CFG590's mapping). This is not a real shear likelihood; that is CFG592.
- **z = 0.** R is taken at z = 0, and the KiDS lenses use the z = 0 NFW shape at their census M_ta.
- **Normalisation mismatch.** The frozen family normalises the KiDS lenses by the census catchment (the KiDS lanes' convention) but the halo model by ΛCDM turnaround masses. This mismatch was found post-hoc (D1–D4). The frozen verdict is unchanged by it.
- **Baryon conventions.**
  - Halo model: baryons are truncated at the declared r_e (CFG556 `cen`). The supply cap pulls the settled edge in but does not re-truncate the baryons.
  - KiDS: baryons are point masses, as in the lane.
  - Groups: stellar Hernquist, as in CFG543.
- **Post-hoc operator grid.** The post-hoc KiDS operators use a grid extended to 2× the larger r_ta, so they are coarser than the frozen grid (K3(ii) was checked only on the frozen grid).
- **Untested.** The post-hoc overlap profile (inner mass below ΛCDM for clusters) has not been tested against cluster lensing or X-ray (CFG546 / CFG552). It must not be cited as a solution.
- Spurious floating-point warnings from the CFG556 code under Accelerate are suppressed. They are the known flags (CFG522 / CFG559).
