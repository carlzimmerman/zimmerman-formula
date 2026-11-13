# SRJ4 FROZEN CRITERIA: reference-layout cold fraction against the authors' dark fraction (cluster-regime RC100 discs)

**Honesty line.** The authors' dark fraction f_DM(R_e) is a model-dependent decomposition (NFW halo, partly contracted,
three-method average with a prior on M_baryon), not raw data. The word is a reading against that decomposition
(PROVISIONAL input), never a pass of the theory. The regime-split joint is post hoc three times over (FRZ1, FZS1, SRJ1).
TEST lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings canonical / alt, never pooled. Cold dark
energy is a gravitating field component; no particle. Committed alone, before any script and before any model number.
Blind to SRJ3's outcome (its RESULT, RERUN, json and out files are not opened; srj3.py is not run).

## Question and sample

On SRJ2's cluster-regime RC100 discs (expected 31 / 22; K1), does the reference layout's cold fraction inside R_e agree
with the authors' dark fraction? Sample: recomputed by executing SRJ2's `srj2_rc.py` read-only from its own path up to its
`json.dump(RES` line (SRJ3's loader pattern). Data: `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv`
(paper values; columns z, logMbar_Msun, Re_kpc, fDM_within_Re). No per-disc f_DM error is in the CSV.

## Model quantity and its match to the authors' definition

- Halo (SRJ2 / SRJ3 construction, FRZ1's `halo_basics_z`): M_ta = X M_b h / (1 - FB), X = XTAB[foot]["z0.0"] if z < 1
  else ["z1.0"], Duffy concentration and Delta_ta at z; physical radii r / (1 + z) / h. Cold mass inside r:
  C(r) = X M_b m_nfw(r / r_s) / m_nfw(c_ta), r capped at r_ta.
- Baryons (graded): M_b / 2 inside R_e, spherical: V_bar^2 = G M_b / (2 R_e) (DD1's construction).
  Reported bracket: thin exponential disc, R_d = R_e / 1.678, Freeman V^2 at R_e.
- **f_cold(R_e) = V_cold^2 / V_tot^2 = C(R_e) / (C(R_e) + M_b / 2).** The authors define (RC100 eq. 1, provenance README)
  f_DM(R_e) = V_DM^2(R_e) / V_circ^2(R_e), V_circ^2 = V_disk^2 + V_bulge^2 + V_DM^2, NFW halo (Method A averages a plain
  and a contracted NFW). Same ratio of squared speeds at the same radius; differences (disc geometry, bulge, contraction)
  are not converted; the thin-disc baryon bracket is reported to show their size.

## Statistic and line (built here; no earlier frozen dark-fraction line exists)

Grep of FROZEN_CRITERIA.md files for f_DM / dark fraction: CFG215, CFG216, CFG217, CFG210 use f_DM only through
D_obs = 1 / (1 - f_DM) against a law, with no line on a cold halo's fraction; SRJ3 reported f_DM, never graded it.
- Per disc: Delta = f_cold - f_DM(author). Per-disc error e = 0.12: the median of the ten printed f_DM uncertainties
  in the provenance README's random-row check (0.10, 0.11, 0.15, 0.08, 0.06, 0.20, 0.14, 0.06, 0.15, 0.13), from the
  paper's Table 3. No fetch. PROVISIONAL (ten rows, not the sample's own rows).
- Class: off = median(Delta); se = max(1.2533 x 1.4826 MAD(Delta) / sqrt(n), e / sqrt(n)).
- **Line, per footing: |off| <= 0.10 AND |off| <= 3 se.** Reported: count with |Delta| <= e; off in z halves.

## Labels (per footing)

- **REFERENCE FITS THE DECOMPOSITIONS** (line holds): SRJ2's G2 miss is a coverage technicality on these discs.
- **REFERENCE TOO HEAVY** (fails, off > 0): too much cold mass inside R_e; the joint fails on rotation curves for a physical reason.
- **REFERENCE TOO LIGHT** (fails, off < 0): too little cold mass inside R_e; the joint fails on rotation curves for a physical reason.
- **NO VERDICT (no power)**: n < 5, a check fails, or a required twin misses its line.
- **NOT EVALUABLE**: f_DM unreadable for the sample (not expected).

## Power: twins (outputs `srj4_MUTATE_<name>.json / .out`)

Bite line: |off_twin - off| >= 0.05 or the word changes. **Required to bite: TW-H (X -> X / 2), TW-D (X -> 2 X).**
**Required to fail the line: TW-N (no cold component, f_cold = 0).** Any miss -> NO VERDICT (no power).

## Brackets

Graded: the X rule above. Reported (FRAGILE if the word changes): X = z0.0 value for all; X = z1.0 value for all; thin
exponential disc baryons; e = 0.08 and e = 0.20. Concentration: the record holds no range (SRJ2 / SRJ3); not bracketed.

## Checks

- **K1:** 31 / 22 cluster-regime, covered 69 / 78 at f 0.75, 1.00, 1.25, names equal `srj2_rc.json`'s; else stop.
- **K2 (SI, second route):** for the median-z disc of each footing, take FRZ1's M_200m and c, recompute rho_m(z),
  r_200m, r_s, r_ta (own bisection of the turnaround condition) and f_cold in SI; agree to 1 %.

## Hand estimate (before any model number)

Typical primary disc: log M_b ~ 11.1, z ~ 1.5-2, R_e ~ 6 kpc, halo ~ 10^13 Msun, c ~ 4, r_s ~ 50 kpc: cold mass inside
R_e ~ 0.3-0.4 M_b, f_cold ~ 0.4. Massive high-z discs in RC100 have low author dark fractions (paper text; README rows
~0.05-0.45). Expect off ~ +0.1 to +0.2. P(TOO HEAVY) 0.55, P(FITS) 0.30, P(TOO LIGHT) 0.08, P(NO VERDICT) 0.07. Twins
should bite (f(1-f) ln 2 ~ 0.15 for f ~ 0.4). Alt (22, most massive) similar.

## Seen before freezing

- Starting context showed none of SRJ3's offsets, twin shifts, model cold fractions, author dark fractions for these
  discs, or which is larger. Commit subjects it showed: Z200, SRF1, Z199, SRF1R (conductor ticks and SRF1 / SRF1R).
- Read: this brief; SRJ2 RESULT.md; SRJ3 FROZEN_CRITERIA.md and srj3.py (SRJ3's own hand estimate there says "RC100's
  massive discs have low dark fractions (~0.2)"; a prior, not an outcome); the provenance README in full (its ten-row
  check prints f_DM +- error for rows 19, 31, 38, 49, 56, 60, 67, 77, 86, 95, and row 32's f_DM 0.19; whether those rows
  are in the primary sample was not checked); the CSV header and rows 1-3; FRZ1 `halo_basics_z`; grep hits of f_DM in
  CFG210 / 215 / 216 / 217 criteria; git log --oneline -12 filtered of srj3 (lane ids Z200, SRF1, Z199, SRF1R, EUC11).
- No model number for any disc. No f_DM column beyond rows 1-3 (and the README's rows above).
