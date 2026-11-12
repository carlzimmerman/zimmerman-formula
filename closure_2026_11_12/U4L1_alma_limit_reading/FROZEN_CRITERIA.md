# U4L1 FROZEN CRITERIA: reading the ALMA upper limit on U4_27928 against the sealed gas requirement

Committed alone, 2026-11-12, before any script and before any difference between the limit and a
requirement was formed. TEST lane with no verdict weight. Adopts nothing. kappa = 1/2 FITTED; not
theory closed.

## What this is and is not

The governing plan for this galaxy is `campaign_fresh_gravity/CFG806_u4_27928_scoring/` (owner
decision 2026-10-20). Its clarification A-U6 says that on a non-detection "No Delta_m is formed,
because there is no V_c". The release-day record (`finish_2026_11_04/FN2_dated_tests/
RESULT_2026-11-06.md`, row A) therefore scored nothing, and that stands. One disc excludes no model.

This lane is the secondary reading the owner's decision allows beside the governing plan: what the
limit says **if** the galaxy's circular speed is the one inferred from its H-alpha kinematics before
the data. It changes no score and edits no frozen file.

## Post hoc, disclosed

Both sides are already on record and have been looked at: the limit (S dv < 0.511 Jy km/s; log
M_gas < 10.88 at alpha_CO 4.36, < 10.24 at 1.0) and the requirement table computed before the release
(`rebuild_2026_10_22/AC1_alma_condor_predictions/ac1_results.json`, key `A`, committed 2026-11-01,
sha256 bfdfed6806020ce61586c084006a43f04a2efe33e366aef229886ecd1da042d9). By eye the requirement at
the higher speed cases (10.8 to 11.2) is near or above the limit. What is frozen here is the reading
rule, so that no branch is chosen by its outcome.

## Inputs (all fixed before the release)

- **Limit:** three sigma, S dv < 0.511 Jy km/s, circular aperture of radius 0.98 arcsec (2 R_e =
  8.271 kpc), +-500 km/s (CFG806 A-U3, A-U5). Conversion as CFG806 section 3.3: r21 = 0.77,
  alpha_CO = 4.36 primary, 1.0 branch.
- **Speed cases** (AC1 Part A, from the KMOS3D H-alpha fit: v_rot 226.1, sigma_0 77.8, R_d 2.46 kpc):
  **a** P0, 226.1 km/s; **b** P0 with CFG99's median 28 per cent slow-bias correction, 314.1;
  **c** P-B, pressure support added, 302.9; **d** P-B on b, 373.2. CFG806 names P-B its primary
  pressure branch and P0 its branch; b and d are AC1's additions and are population-median
  corrections. None is a CO measurement.
- **Requirement:** total gas mass, per case, kernel (n = 1 primary as in AC1, nu_mono, n = 2), footing
  (canonical, alt), a0 reading (F-flat and F-DESI are the framework; R-H and L-fb are the rivals
  CFG571 coded) and gas scale (R_g = R_d primary, 1.5 R_d), read from the file above. FLOOR cells
  (stars alone exceed what the model allows) are **not tested** by a non-detection.
- **Scaling-relation gas mass** for comparison: 10.51 (the same file).

## Reading rule

- **Aperture.** The requirement is the total mass of an exponential gas disc; the limit covers
  8.271 kpc. The fraction inside is f = 1 - (1 + x) exp(-x), x = 8.271 kpc / R_g, for a face-on thin
  disc. An inclined disc puts more of its flux inside a circular aperture, so face-on is the most
  lenient correction and no correction is the strictest. Both are computed:
  **matched** D = log L - (log M_req + log f); **as printed** D = log L - log M_req.
- **Cell label,** from D: **ALLOWED** if D >= 0; **MARGINAL** if -0.30 <= D < 0 (the requirement is
  above the three-sigma limit by no more than twice the plan's 0.15 dex systematic floor);
  **IN TENSION** if D < -0.30 (CFG806 section 4's reading, applied one-sidedly). The label is taken
  from the matched reading and marked FRAGILE if the as-printed reading gives a different label.
- **Never pooled:** every case, kernel, footing, a0 reading, gas scale and alpha_CO branch is printed.
- **Lane label,** on the framework cells (F-flat and F-DESI) at the primary kernel and gas scale, both
  footings:
  - **TENSION AT THE PLAN'S PRIMARY BRANCH** if at alpha_CO 4.36, case c, all four are IN TENSION;
  - **NO TENSION** if at alpha_CO 4.36 none of the four is IN TENSION at case a or at case c, in
    either aperture reading;
  - **CONDITIONAL** otherwise, naming the branches under which tension appears.
- **NOT DISCRIMINATING** is added for any case and alpha_CO branch in which the rival cells that are
  not FLOOR carry the same label as the framework cells.

Reported, not graded: the atomic or CO-dark gas mass that would lift each primary cell to ALLOWED;
the alpha_CO at which the limit equals each primary requirement; the scaling-relation gas mass
against both limits; counts of labels over all kernels and gas scales.

## Known-answer checks (all before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | the limit, recomputed independently in SI from 0.511 Jy km/s (standard line-luminosity formula, flat LambdaCDM H0 70, Omega_m 0.3, z 1.41933) | 10.88 and 10.24, each within 0.03 dex |
| KA2 | the requirement, recomputed with an independent implementation (closed-form inversion of the n = 1 and n = 2 kernels, own Freeman-disc routine) for F-flat and F-DESI at all four cases, both footings, R_g = R_d | every non-FLOOR value within 0.01 dex of the file; FLOOR flags equal |
| KA3 | provenance | the file's sha256 equals the one above and its first commit predates 2026-11-06 02:42 UTC |
| KA4 | aperture fraction | closed form equals a numerical integral of the exponential disc to 1e-6; f = 0.849 +- 0.002 at R_g = 2.46 kpc |

## Mutations (each must bite)

| id | mutation | must give |
|---|---|---|
| M1 | the limit raised by 1 dex | no non-FLOOR cell IN TENSION |
| M2 | the limit lowered by 1 dex | every non-FLOOR cell at cases b, c and d IN TENSION |

Mutation runs write `u4l1_mut.out`.

## What a label will and will not mean

The reading is conditional three times over: on the H-alpha speed being the circular speed of the
gas, on the CO conversion factor, and on CO tracing all the gas (atomic gas is not seen). A halo model
needs no gas to make the speed and is untouched by any outcome here. A tension would say that this
galaxy, at that speed and conversion, has less molecular gas than a law without a halo needs; it
would not be an exclusion.
