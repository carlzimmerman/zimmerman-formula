# CFG525 FROZEN CRITERIA: the KiDS census-edge miss on the alt footing (CFG515 (a1): +3.20 canonical PASS / +8.84 alt FAIL). Mechanism, or data/assumption error?

Committed alone, before any CFG525 script exists (2026-10-09). kappa = 1/2 is FITTED. Footings 9.3603e-11 (canonical) and
1.1312e-10 (alt) are scored separately and never pooled; a0 flat. Kernel nu_mono (FP1 table, cfg100_lib). Candidate B; "cold energy"
= its cold component, whose MASS is still required (no particle). On-disk data only, no downloads, nice 10, <= 4 worker processes.
Not "theory closed"; nothing here says the data favour the framework. No knob is fitted to rescue anything; every "f_ret needed"
or "multiplier needed" is post hoc, labelled, and carries no verdict weight.

## 0. Objects and the statistic
- Census edge (CFG515 lib, imported read-only): r_edge = r_M(M_b) / ln(1 + f_ret f_b/(1 - f_b)), r_M = sqrt(G M_b / a0), f_b = 0.02237/0.14237,
  f_ret = CFG416 `fret_of` solved self-consistently (`fret_census`). Model: nu_mono phantom of the group's present baryons M_gal, fully
  settled to min(r_edge, r_ta), frozen beyond, plus the baryon point mass (CFG503 `kids_Md`/`kids_fin`, read-only).
- Reference family (per harness, per footing, per sample): CFG413's sharp edge at x r_ta on a fixed node grid
  x in {0.06, 0.08, 0.10, ..., 0.30 (step 0.02), 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90, 1.00};
  best-x = min chi2 over nodes with x >= 0.20 (CFG413's rule). Statistic: **Delta_H = chi2_H(model) - chi2_H(best-x)**, same harness,
  sample, footing. PASS iff Delta_H <= 4. Sigma reported as sqrt(Delta_H) (one placement parameter profiled).
- Any edge that is not a node is evaluated by cubic interpolation in log x of each group's 15-bin vector across the nodes (x >= 1
  -> the x = 1 node, the r_ta cap). Lens weight with x < 0.06 must be 0 for any interpolated row, else the row is computed directly.
- Harnesses (data: CFG377 stack P, 181,477 lenses, 15 bins, 50-patch jackknife, Hartlap):
  - **H1** CFG413 / CFG515 (a1): free R^-0.8 two-halo amplitude profiled, 15 bins. THE MISS lives here.
  - **H2** H1 restricted to the 9 bins Brouwer+21 trust (R <= 0.445 Mpc), free amplitude profiled on those bins.
  - **H3** CFG503's environment (E = halofit xi_NL x Tinker zeta, leaked-satellite stripping W10, SHMR rank-one, Moster primary)
    with the leaked-satellite fraction rescaled to the MEASURED 0.2234 (CFG519) exactly as CFG520 part B (s_M = 0.2234/0.18056,
    s_B = 0.2234 / Behroozi stack-weighted f; f' in E AND in the own-profile mixing). No free amplitude. 15 bins primary; inner-9 reported
    as H3i. With this input CFG503's LCDM passes its G1 gate (CFG520: 26.13/15, p 0.037); G3 not re-scored (label carried).
  - **H4** (reported only) H1 with the R^-0.8 template replaced by the stack of H3's E vector as a shape, amplitude free (profiled).

## 1. Data / assumption re-check (each item both footings; edge-only variants keep the stack and the baryon model fixed and change
only the M_b entering r_M and fret_census; this is a partial derivative, declared)
- **D1 stellar-mass scale.** lr_lenses logM = LePhare MASS_MED + 0.15 dex (fluxscale, logged as unverified). Variants delta = -0.15 (no
  fluxscale), -0.10, -0.05, +0.05, +0.10, +0.15 dex on M_gal (edge only). Declared PLAUSIBLE range: |delta| <= 0.10 (fluxscale 0.10-0.20 plus
  SPS/IMF ~0.1 dex, not added in quadrature to be generous). Derived expectation (stated before scoring): x_edge ~ M^{1/2}/r_ta(M), weak.
- **D2 cold gas / M/L.** M_gal = M*(1 + f_cold), log f_cold = -0.69 log M* + 6.63. Variants: stars only (f_cold = 0); f_cold x 2. Edge only.
  Declared PLAUSIBLE: f_cold x 2 and stars-only both count (scatter of the scaling relation ~0.3 dex).
- **D3 the f_ret input.** (a) Provenance: CFG416's 0.10 floor below log M_ta 12.5 is a declared step built from the Shull+12 cosmic census
  (recalled, PROVISIONAL, not re-fetched). (b) Phase matching (assumption check, derived from the edge definition): the supply is the cold
  share of the ORIGINAL baryons, M_b,now / f_ret, so f_ret must count the same phases as M_b,now. KiDS M_b,now = stars + cold gas, i.e. the
  census GALAXY phase, 0.07 +- 0.02 (Shull+12, recalled, PROVISIONAL; CFG365's "galaxies only"). Rows: constant f_ret = 0.05, 0.07, 0.09.
  (c) Conflict test: the record's other object at this mass with the SAME baryon definition is the Local Group pair (CFG522, M_b = stars +
  gas). The LG full statistic at a common f_ret is read from CFG522's committed post-hoc scan (canonical; linear interpolation in f;
  f = 0.07 extrapolated linearly from 0.08 / 0.10, labelled). D3 counts toward DATA-ISSUE only if f = 0.07 passes H1 on both footings AND
  |z_full,LMC(LG, f = 0.07)| <= 3; otherwise D3 is reported as "CONFLICTED" (or "no effect").
- **D4 measured leaked-satellite fraction.** CFG413's H1 has no satellite term (free template); 0.2234 enters through H3. Report Delta_H3 and
  Delta_H3i for the census edge, plus chi2 minus H3's LCDM (reported).
- **D5 two-halo treatment.** H2 (trusted bins) and H4 (physical E shape, free amplitude), census edge, Delta per footing.
- **D6 lens redshift.** Derived: r_edge does not depend on z_l; z_l enters the model only through the r_ta cap. Check: lens weight with
  r_edge >= r_ta (CFG515: 0). If 0, lens-z errors cannot move the census model (no computation needed beyond the check).
- **D7 isolation selection.** f30 (W = 30 Mpc strict isolation, cfg96_isoflags, 57,265 lenses; CFG413 S1): census edge Delta_H1 vs best-x
  on the f30 sample, both footings.

## 2. Mechanisms (derived, no new knob)
- **M-i shared catchments (CFG522 M1 rule).** Where lenses share a turnaround sphere, apply the census ONCE to the catchment:
  f_sh = fret_census(M_sum), M_sum = M_lens + neighbour baryons inside the lens's turnaround sphere; each object keeps the supply
  5.364 M_own / f_sh (supply partitioned by own baryons, as CFG522). Derived consequence, stated before scoring: fret_census is
  non-decreasing in M_b, so f_sh >= f and the edge can only move IN; M-i cannot raise the KiDS phantom. Computed anyway:
  - (a) photometric neighbours: KiDS-bright pool exactly as lr_esd_remeasure builds it (r < 20, 0.1 < z_phot < 0.5, unmasked, logM
    MASS_MED + 0.15, M_gal with f_cold), projected separation < r_ta (per lens, comoving r_ta(1+z)/chi), |d chi| < 10 Mpc (the W10
    isolation window), self excluded. Local background from the annulus 2.5-3.5 Mpc (comoving, same window), area-scaled. Primary:
    the group-mean background-subtracted neighbour mass added to each group's M_gal. Upper variant: per-lens RAW (unsubtracted) sum.
  - (b) leaked satellites: the measured 22.34% of the lens weight are satellites whose host (more massive, by CFG519's definition) is
    inside their turnaround sphere; minimal host M_host = M_lens, so for that weight M_sum = 2 M_lens (a lower bound on the effect).
  - (a)+(b) combined is the M-i row. Also reported, as the FORBIDDEN counter-case: double-counted supply (each lens gets the whole
    catchment supply 5.364 M_sum / f_sh). It is expected to move the edge OUT; it is excluded by CFG522's derivation and cannot be a
    rescue.
- **M-ii level or shape.** Uniform multiplier s on the census edge, s in {0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.4},
  H1 both footings. LEVEL problem iff min_s chi2 - chi2(best-x) <= 1 on that footing (the census edge's per-lens mass scaling fits as well
  as the best sharp edge once placed) AND s = 1 fails; SHAPE problem iff min_s chi2 - chi2(best-x) > 4. Report s_best and the s range with
  Delta <= 4. Also the derived footing ratio x_alt/x_can = (a0_can/a0_alt)^{1/2} r_ta,can/r_ta,alt (lens-weighted), compared with the
  ratio of the two footings' s_best x_census.
- **M-iii anything else derivable.** Candidates considered before scoring: (1) partial settling (CFG485 R5: 9-14% unsettled at a census
  edge) - NOT derivable here (no settling history in the record), scope only; (2) photometric-mass scatter (Eddington) - its size follows
  from D1 (x ~ M^{1/6}-ish), reported through D1; (3) stripping of leaked satellites - carried by H3. No other derived mechanism is declared;
  if one is found after scoring it is reported post hoc and cannot change the verdict.

## 3. Post hoc (reported only, no verdict weight)
f_ret scan, constant per lens, f in {0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.14, 0.16, 0.18, 0.20}, H1 both footings: the
largest f with Delta_H1 <= 4 (linear interpolation in f) = "f_ret the alt footing would need". Same for canonical.

## 4. Verdict (ordered; first that applies)
1. **MECHANISM FOUND** iff a derived mechanism row (M-i; any M-iii declared above) gives Delta_H1 <= 4 on BOTH footings.
2. **DATA-ISSUE** iff any of: a D1 variant inside |delta| <= 0.10 or a D2 variant gives Delta_H1 <= 4 on both footings; D3(b) passes both
   footings without the D3(c) conflict; D7 (f30) passes both footings; D4: Delta_H3 <= 4 on both footings (the miss then belongs to the
   free R^-0.8 template, an assumption).
3. **NOT DIAGNOSTIC** iff alt Delta_H2 <= 4 AND H3 cannot place the edge on alt (max - min chi2_H3 over nodes x in [0.2, 1] <= 4).
4. **GENUINE TENSION** otherwise, quoted as sqrt(Delta_H1 alt) sigma and sqrt(Delta_H3 alt) sigma.
The verdict is stated per footing as well; canonical's status is reported beside every row.

## 5. Controls (load-bearing; the run exits 1 if any fails)
- K1 direct census rows reproduce CFG515 (a1) chi2 12.145 / 18.613 within 0.01, and its a2 inner-9 58.54 / 36.85 within 0.01 (H3 with f unscaled).
- K2 interpolated census (from the node tables) reproduces the direct census H1 chi2 within 0.05 on both footings.
- K3 nodes x = 0.5 and 1.0 reproduce CFG413's committed chi2 (8.948 / 9.770; 24.50 / 23.44) within 0.01; f30 x = 0.3 reproduces CFG413 S1
  within 0.01.
- K4 H3 with LCDM own tables reproduces CFG520 part B's scaled LCDM 15-bin chi2 (26.13) within 0.01.
- K5 the neighbour pool reproduces lr_lenses (every stack-P lens is found in the pool at zero separation with identical logM).

## 6. MUTATE (`CFG525_MUTATE=1`, outputs `*_MUTATE.*`; must be DETECTED, else exit 1)
- T1 f_ret = 1 must FAIL H1 on both footings and reproduce CFG515 M1 (+60.48 / +70.57) within 0.1.
- T2 f_ret = 0.01 must FAIL H1 on both footings (CFG515 M2: +15.6 / +13.7; edge capped at r_ta).
- T3 neighbour finder with lens positions displaced by +1 deg in Dec: the background-subtracted mean neighbour mass must be consistent with
  zero (|mean| < 3 sigma of a 50-patch jackknife, or < 20% of the primary's mean).

## 7. Outputs
Scripts, `.out`, `_MUTATE.out`, results JSON, a plain README. `git add` this lane folder only, specific paths; commit locally; no push.
Departures after this commit are dated in the README; this file is never edited.
