# DPR1 FROZEN CRITERIA: distinctive, dated predictions of form B

Frozen 2026-11-13 (UTC), committed alone, before any script of this lane exists and before any number of this lane
is computed. TEST lane. Registers nothing, edits no registry, pre-registration or frozen file. Footings never pooled
(canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2). kappa = 1/2 FITTED; not theory closed. Cold dark energy is a
gravitating field component, never a particle.

## 1. Question

Is there a statistic, on data with a public date that has not landed, for which form B as adopted
(`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`; PAPER72 Section 7.1, rules 1-6) predicts a value that
differs from both rivals by a margin the dated data can resolve? Separately, and labelled CONDITIONAL ON THE JOINT: the
same question for the candidate joint "the law's layout only inside R_set = R_fold" (FZS1, SRH1, FLD1).

## 2. The three predictions compared

- **B:** form B as adopted. Galaxies: the law's halo (no external field effect from a host; real mass), with the
  counted-once share (PD1's rule: share 59.49 / 59.50 M_b, truncated where the law's halo holds it, as used by KO2 and
  FLD1). Hot systems: 5.41 times the baryons that fell in. Cosmology: the cold reference's rows as computed (CO1, CO2),
  with the 1-halo redistribution of FRZ1 / FRZ3 / FRZ3R where a statistic sees it. The Milky Way: the actual-field
  reading (owner decision 2026-11-12).
- **R1:** Newtonian gravity with a standard cold halo: the record's cold reference layout (NFW-type haloes on the
  record's halo list or the published NFW fit named per candidate), with its ordinary scatter and its own modelling
  spread (for example baryonic feedback) included in its band.
- **R2:** the a0 law alone as a modified force law with an external field effect, no cold component. Where R2 needs an
  external field, the record's EFC1 literature readings (actual field 0.01 and 0.03 a0) bracket it; for hosted systems,
  the host's field.

Where the record carries more than one value for a prediction on the same statistic (two layouts, two builds, brackets
the record keeps), that prediction is a BAND: the envelope of those values. Separations are measured between band edges
(nearest edges). A value marked by its own lane as resting on a known error (for example a smoothing scale four times the
published one) is reported but does not set an edge, and this is said where it is used.

## 3. The definition of DISTINCTIVE (frozen number)

A candidate is **DISTINCTIVE** on a footing if and only if all of the following hold on that footing:

1. **Dated:** the deciding data have a public release date on or before 2027-12-31 stated in the record (A6, the
   scorecard section 8, `forecasts/`, the DR4 map) or, if not in the record, on a release page (then PROVISIONAL), and the
   statistic can be computed from that release, either by machinery committed in the record or by a product the release
   itself names. A release with no date ("early 2027" is accepted only as PROVISIONAL and dated 2027-03-31 for ranking) or a
   statistic that needs a third-party analysis with no date does not qualify.
2. **Computed:** the values of B, R1 and R2 on the same statistic are each computed (record file and commit, or this
   lane's script with the model stated). A rival value that is not computed makes the candidate NOT ESTABLISHED, never
   distinctive.
3. **Resolvable:** |B - R1| >= 3 sigma_D and |B - R2| >= 3 sigma_D, nearest band edges, where sigma_D is the expected
   1-sigma error of the dated measurement of that statistic: the survey's own published forecast if one exists (PROVISIONAL
   if read from the web), otherwise the record's measured error on the same statistic, scaled to the new data by a rule
   stated per candidate. The default scaling for shape-noise-limited lensing is sigma proportional to (area x n_eff)^(-1/2)
   applied to the statistical part only, with any systematic floor the record adds (for example KO2's 0.05) kept unscaled.
4. **Single-valued enough:** B's band is narrower than 6 sigma_D (otherwise the data cannot confirm it even if both rivals
   fail).

**DISTINCTIVE** needs both footings; **DISTINCTIVE ON ONE FOOTING** is reported and not sealed. Candidates that fail are
classed: NOT DISTINCTIVE (B equals a rival within 3 sigma_D), NOT ESTABLISHED (a value missing), NO DATED DATA, or
POST-DICTION (the deciding data already exist; then the record's standing on them is given).

Each candidate is also tagged: already registered (with the registry row), new, or post-diction.

## 4. Dated data considered (dates as in the record; PROVISIONAL where so marked there)

| data | date | source in the record |
|---|---|---|
| ALMA unit vc875 (2022.1.01118.S) | 2026-11-13 19:00 EST | scorecard section 8; `forecasts/noncondor_2026_11_04/` |
| ALMA UDS16442; GS4_24110; remaining condor units | 2026-11-24; 2026-11-28; 2026-12-04, 2026-12-22 | scorecard section 8 |
| ALMA AzTEC-1, BRI1335 excitation; AzTEC/C159 [CII]; C159 excitation | 2027-02-19; 2027-03-04; 2027-07-20; 2027-09-24 | `forecasts/noncondor_2026_11_04/README.md` |
| Gaia DR4 | 2026-12-02 (ESA, provisional) | DR4 map |
| DESI DR2 spectra | "early 2027", PROVISIONAL | A6 |
| Euclid DR1 complete (shear, clustering, higher products) | 2027-06-16 | A6 |
| DESI DR3 / five-year cosmology; JUNO | 2027, no day | scorecard section 8 |
| 4MOST lens source redshifts | no date in the record | (checked during the lane) |

## 5. Candidate families to examine

1. Absence of an external field effect: hosted against isolated dwarfs; wide binaries (Gaia DR4 gamma_v).
2. a0 tied to the dark-energy density, against a0 constant and a0 tracking H(z): high-redshift rotation curves; the ALMA
   units with listed dates.
3. Outer rotation curves and lensing beyond the fold radius (CONDITIONAL ON THE JOINT: a break scaling as M_b^(1/3) and
   shrinking with redshift, FLD1's table).
4. The share 5.41 in groups and clusters out to the turnaround radius.
5. Group-hosted wide lenses of Euclid; Euclid strong-lens source redshifts (4MOST).
6. Euclid calibrated shear: galaxy own-field outer profile by type (KO2 statistic), host-free shape (ONE1 / SRH1R),
   cosmic-shear amplitude and the 1-halo redistribution.
7. DESI DR2 spectra: spectroscopically isolated lenses; the forest at flux level.
8. Gaia DR4 observables other than gamma_v: the Milky Way's enclosed mass and its slope beyond 100 kpc, potential depth
   (escape speed), vertical force near the Sun.
9. Any other found during the lane, listed with how it was found.

## 6. Rules

- Nothing is tuned to data already seen. B's values come from the record's committed outputs or are computed from the
  record's adopted constants (a0 per footing, kappa = 1/2, the 5.41 / 59.5 shares, the census baryons 6.6814e10 Msun) with
  nothing fitted to any measurement. No band is moved after any data are seen. Every post-diction is flagged.
- Rival values are taken from the record where it computed them; otherwise computed here with the model stated. A rival is
  never set so as to make a candidate pass or fail.
- **Sealing:** each candidate that is DISTINCTIVE gets one file `SEALED_<short name>.md` with: the statistic defined
  exactly; the sample; the B, R1, R2 bands per footing; sigma_D and its source; the kill line for B (B is killed if the
  measurement lies more than 3 sigma_D outside B's band); what counts as confirmation (the measurement inside B's band
  and at least 3 sigma_D from both rival bands); the date the data are due; the machinery and its commit. Each sealed file
  is committed alone, before the data exist; the commit time is the seal. Each says "sealed in this lane; not entered in
  any registry: registration needs the owner's word".
- `RESULT.md` is written last: verdict first, at most 100 lines.
- If no candidate meets the definition for data landing before a date, that is the answer.

## 7. Seen before freezing (disclosed)

Read in full or in part before this file: the form-B decision; PAPER72 sections 2-8 (rules, open items, version 1.2
rows); the 2026-11-12 external-field decision; the scorecard of 2026-11-12; the DR4 map; A6; the ALMA governing plans;
FLD1's RESULT (fold radii by mass and redshift); KO2's RESULT (early types 0.487 +- 0.071, late 0.277 +- 0.183 against
form B 0.038 / 0.007 and the law 1.0); SRH1R's RESULT (the host-free gate passes equally with the cold reference, the
law to x_t and f = 0.05); EFC1's RESULT table (the Milky Way line at 200 kpc: 13.7 under the adopted reading, 13.4 and
13.7 under literature fields 0.03 and 0.01 a0, 5.26 under the record's old reading); PLT1's quote of the DESI paper's NFW
extrapolation (7.53 / 9.65 / 11.27 x 10^11 at 100 / 150 / 200 kpc); DR2REV's M200c 1.19e12; ZN4's README; the
`forecasts/noncondor_2026_11_04` README (F-DESI against constant a0 at z 4.55: a0 ratio 0.660; speed differences
5-8 km/s at 5 kpc; "no demonstrated clean discrimination"); RFX1's commit message; CFG314 and CFG590 (KiDS n_eff 6.2 /
6.17 arcmin^-2, PROVISIONAL recall in those files).

## 8. Estimates before computing (disclosed, unverified)

- The lead's (from the brief): few or no distinctive predictions for form B as adopted on data landing in 2026; the
  conditional joint is where distinctive predictions are most likely.
- Mine, from the reading above: inside a galaxy's truncation radius B equals the law with a negligible field, so B and R2
  agree there wherever the host's field is small; on large scales B copies R1. I expect zero or one DISTINCTIVE candidate;
  the most likely is the KO2 own-field statistic on Euclid shear (B near 0, the law near 1), where R1's value has not been
  computed in the record. I expect the conditional joint's break to be invisible to every dated statistic, because the
  fold lies beyond every rotation curve and SRH1R found lensing blind to it.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
