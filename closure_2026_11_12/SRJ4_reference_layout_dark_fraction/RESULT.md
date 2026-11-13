# SRJ4 RESULT: reference-layout cold fraction against the authors' dark fraction

**NO VERDICT (no power) / NO VERDICT (no power) (canonical / alt), as frozen.** A required twin misses its line on each
footing. TW-H shifts the class offset by -0.031 on canonical. TW-D shifts it by +0.025 on alt. The bite line is 0.05,
or a change of word.

**Honesty line.** The authors' dark fraction is a model-dependent decomposition, not raw data (NFW halo, partly
contracted, a three-method average with an M_baryon prior). Any reading here is against that decomposition (PROVISIONAL
input), never a pass of the theory. The regime-split joint is post hoc three times over. TEST lane. Criteria 9d5d0c31bb
(alone, before any script or number); scripts and outputs 1557b2b679; no amendment. Footings never pooled. Cold dark
energy is a gravitating field component; no particle. Written blind to SRJ3's outcome; SRF1 and SRF1R were not opened.

## Rows (graded rule: X by z, spherical M_b / 2 baryons, e = 0.12)

| row | canonical | alt |
|---|---|---|
| n (cluster-regime discs) | 31 | 22 |
| median f_cold, model / authors | 0.286 / 0.160 | 0.277 / 0.135 |
| class off = median(f_cold - f_DM) | +0.0698 | +0.1120 |
| se (3 se) | 0.0381 (0.114) | 0.0318 (0.095) |
| line abs(off) <= 0.10 and <= 3 se | holds | fails (off > 0) |
| discs with abs(Delta) <= 0.12 | 15 / 31 | 9 / 22 |
| off, z halves (low / high) | +0.035 / +0.085 | +0.070 / +0.122 |
| TW-H (X / 2): off, shift, bites | +0.039, -0.031, **no** | +0.081, -0.031, yes (word) |
| TW-D (2 X): off, shift, bites | +0.103, +0.033, yes (word) | +0.137, +0.025, **no** |
| TW-N (no cold): off, fails line | -0.160, yes | -0.135, yes |
| ungraded reading | REFERENCE FITS THE DECOMPOSITIONS | REFERENCE TOO HEAVY, FRAGILE |
| **frozen word** | **NO VERDICT (no power)** | **NO VERDICT (no power)** |

## Why it came out this way

- **No power.** The frozen twins scale the cold mass's normalisation. Inside R_e (5 to 10 kpc, about 0.1 r_s) the NFW
  cold mass grows only about as M^(1/3), because r_s shrinks as the halo shrinks. Halving X therefore cuts C(R_e) by about
  20 %, not 50 %, and f_cold moves by about 0.03 at the median. A factor-two halo twin cannot reach a 0.05 bite line. My
  estimate of the twins' reach (0.15) treated C as proportional to X, which was wrong. The no-cold twin does fail, so the
  statistic does tell a cold component from none.
- **Direction.** On both footings the reference puts more cold mass inside R_e than the authors' decompositions do. The
  gap is larger at higher z and on alt, whose 22 discs are the most massive. On canonical the gap stays inside the line.
- **Alt is FRAGILE.** With thin exponential-disc baryons (V_bar^2 larger at R_e), off falls to +0.079 (se 0.029) and the
  reading turns to FITS. The X brackets (z0 / z1 values) and the e brackets (0.08 / 0.20) do not change either reading.
  Canonical thin disc: +0.035, FITS.

## What it means for the regime-split joint

As frozen, nothing: neither SRJ2's G2 coverage miss nor a physical rotation-curve fail is decided by this statistic.
Read ungraded, the reference layout is not grossly wrong on these discs: within 0.07 of the authors' fractions on
canonical, and about 0.11 heavier on alt, with that difference inside the baryon-geometry bracket. These are readings
only.

## Checks

- **K1 PASS both:** 31 / 22 cluster-regime, covered 69 / 78 at f 0.75, 1.00, 1.25, names equal `srj2_rc.json`'s.
- **K2 PASS both (SI, second route):** GS4 01529 (z 2.12, canonical): r_s 56.50 vs 56.49 kpc, r_ta 769.9 vs 769.8 kpc,
  f_cold 0.1541 vs 0.1541. U4 36568 (z 2.18, alt): r_s 49.49, r_ta 679.6, f_cold 0.1392, all equal. The route takes
  FRZ1's M_200m and c as given, so it checks units and radii, not the concentration relation.

## Estimate against outcome

Hand estimate: TOO HEAVY 0.55, FITS 0.30, TOO LIGHT 0.08, NO VERDICT 0.07. Outcome: NO VERDICT on both (the 0.07 branch).
Direction right (model heavier). My f_cold of about 0.4 came out 0.28. My expectation that the twins would bite was wrong.

## Not verified

- The per-disc error 0.12 is the median of the ten printed errors in the provenance README, not the sample's own rows.
  The README's ten rows were seen before freezing; whether they are in the sample was not checked.
- The definitions are matched only as a ratio of squared speeds at R_e. Bulge, disc thickness and the authors' halo
  contraction are not modelled. The authors' fractions carry their M_baryon prior.
- The concentration relation is not bracketed (the record holds no range). Nothing was fetched.

## Files

`FROZEN_CRITERIA.md` (9d5d0c31bb). `srj4.py`, `srj4.json`, `srj4.out`, `srj4_MUTATE_{TWH,TWD,TWN}.{json,out}`
(1557b2b679). SRJ2's `srj2_rc.py` is executed read-only from its own path. Nothing was pushed.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
