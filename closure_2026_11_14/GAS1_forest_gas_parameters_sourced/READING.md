# GAS1 reading: which bracket values the measurements allow

Date: 2026-11-14. Literature look-up; not blind; relabels nothing; computes no forest number. Placements were done by
hand-checkable interval comparisons (a short scratch script, not committed; every input is in SOURCES.md).

## Verdict first

1. **Convention.** The record's lambda_P is the real-space Gaussian sigma on the density, exp(-k^2 lambda^2 / 2) on the
   field, comoving, in both builds alike. That is Rorai et al. 2017's definition exactly (factor 1, no sqrt(2)).
   Kulkarni 2015 and Walther 2019 define lambda_P on the flux power; Rorai 2017's calibration maps that one to one
   (Reading 1, used below), while a caption in Kulkarni 2015 implies a factor 1/2 in the code's convention (Reading 2,
   given beside).
2. **Attribution of 91.4 and 138.6 comoving kpc: right.** They are Rorai et al. 2017 Table S2, z = 3.0, columns
   lambda_P,16syst and lambda_P,84syst (16th and 84th percentiles with systematics), comoving kpc; the median is 113.8.
   The record's 79 comoving kpc is Kulkarni et al. 2015's SIMULATION value (fiducial model, z = 3, flux-power fit), not
   a measurement; Rorai 2017 Table S3 gives 79.1 for its standard simulation too.
3. **lambda_P brackets (Reading 1, union of measurements within 0.3 in z):**

| bracket (comoving kpc) | z 2.2 | z 3.0 | z 4.4 |
|---|---|---|---|
| 39.5 (x 0.5) | INSIDE 2 SIGMA (Rorai 2.0, 2.4 only) | OUTSIDE | OUTSIDE |
| 79 (primary) | INSIDE 1 SIGMA (Rorai, Walther) | INSIDE 1 SIGMA (Walther only; Rorai 2 sigma) | INSIDE 1 SIGMA (Walther 4.2/4.6 only) |
| 91.4 | INSIDE 1 SIGMA | INSIDE 1 SIGMA (Rorai lower edge; Walther 2.8) | OUTSIDE |
| 100 proper (320 / 400 / 540) | OUTSIDE | OUTSIDE | OUTSIDE |
| 138.6 | OUTSIDE | INSIDE 1 SIGMA (Rorai upper edge only) | OUTSIDE |
| 158 (x 2) | OUTSIDE | INSIDE 2 SIGMA (Rorai only) | OUTSIDE |

   Reading 2 (Walther values halved; Rorai unchanged): 39.5 becomes INSIDE 1 SIGMA at all three anchors; 79 drops to
   INSIDE 2 SIGMA at z 3.0 (Rorai only) and OUTSIDE at z 4.4; the rest as above.
4. **gamma brackets (union):**

| gamma | z 2.2 | z 3.0 | z 4.4 |
|---|---|---|---|
| 1.2 | INSIDE 2 SIGMA (Gaikwad only) | INSIDE 1 SIGMA (Gaikwad, Hiss) | INSIDE 1 SIGMA (Boera, Walther flat 4.6) |
| 1.5 (primary) | INSIDE 1 SIGMA | INSIDE 1 SIGMA | INSIDE 1 SIGMA |
| 1.6 | INSIDE 1 SIGMA (Hiss, Walther Gaussian) | INSIDE 1 SIGMA (Walther only); OUTSIDE for Gaikwad | INSIDE 1 SIGMA (Walther only); 2 sigma for Boera |

5. **T0 = 1e4 K (union):** INSIDE 1 SIGMA at all three anchors, but at z 3.0 only through Walther flat prior (2.8 and
   3.2); Gaikwad gives INSIDE 2 SIGMA (3.2 only) and Hiss OUTSIDE. At z 4.4 Walther gives 1 sigma, Boera 2 sigma.
6. **tau_eff brackets (record formula times s, evaluated at each measurement's own redshift; union):**

| s | z 2.2 | z 3.0 | z 4.4 |
|---|---|---|---|
| 0.9 | INSIDE 1 SIGMA (Becker) | INSIDE 1 SIGMA (Gaikwad, Walther flat 3.0) | INSIDE 2 SIGMA (Walther flat only) |
| 1.0 (primary) | INSIDE 1 SIGMA (Becker) | INSIDE 1 SIGMA (Gaikwad 2.8, Walther) | INSIDE 1 SIGMA (Walther, Boera 4.2) |
| 1.1 | INSIDE 1 SIGMA (Gaikwad 2.4, Walther Gaussian 2.4) | INSIDE 1 SIGMA (Walther flat 2.8 only); OUTSIDE for Becker and Gaikwad | INSIDE 1 SIGMA (Walther, Boera 4.6) |

## Measurements used and their distance in redshift

- z 2.2: Rorai 2017 at 2.0 and 2.4 (0.2); Walther 2019 at 2.0, 2.2, 2.4; Gaikwad 2021 and Hiss 2018 at 2.0, 2.2, 2.4;
  Becker 2013 at 2.15 and 2.25; Bolton 2014 at 2.37 (PROVISIONAL, abstract).
- z 3.0: Rorai 2017 at 3.0; Walther, Gaikwad, Hiss at 2.8, 3.0, 3.2; Becker at 2.95 and 3.05; Rorai 2018 at 2.55 to
  2.95 (PROVISIONAL, abstract; taken at 2.75, 0.25 away).
- z 4.4: Walther 2019 at 4.2 and 4.6 (0.2); Boera 2019 at 4.2 and 4.6; Becker at 4.35 and 4.45. No Rorai 2017
  lambda_P bin is within 0.3 (nearest 3.6). Gaikwad and Hiss stop at 3.8 and 3.4.
- 2 sigma intervals are twice the quoted 1 sigma half-widths on each side (SCOPE.md), since no paper read here gives
  its own 2 sigma bounds. Asymmetric mean-flux errors were symmetrised in tau. Only SEEN IN TEXT values decide a
  placement; the PROVISIONAL Bolton and Rorai 2018 values change no cell above.
- Simulation values (Kulkarni 79.0 and 191.5; Rorai Table S3 and S4) are not used.

## Where the measurements disagree

- lambda_P at z 3.0: Rorai 2017 (91.4 to 138.6) and Walther 2019 (about 75 to 88) do not overlap at 1 sigma. On Rorai
  alone, 79 is INSIDE 2 SIGMA, and 138.6 and 158 are allowed; on Walther alone, 79 is INSIDE 1 SIGMA and 138.6 and 158
  are OUTSIDE.
- gamma: Walther's flat prior gives about 2.1 at z 2.0 to 2.8, which puts all three bracket values OUTSIDE at z 2.2 on
  Walther flat alone. Gaikwad and Hiss sit near 1.2 to 1.3 at z 3.0, where 1.6 is OUTSIDE (Gaikwad) or 2 sigma (Hiss).
- T0 at z 3.0: Hiss (18000 to 20000 K) and Gaikwad (14750 K) put 1e4 K OUTSIDE and at 2 sigma; Walther flat (10000 K at
  2.8) puts it at 1 sigma.
- tau_eff near z 2.0 to 2.4: Gaikwad and Walther give tau 1.1 to 1.5 times the record's formula; Becker's own table is
  4 to 6 % below its fit at every z checked (not resolved; SOURCES.md).

## The record's primary values

- lambda_P = 79 comoving kpc: inside at every anchor in the union, but at z 3.0 only through Walther; against Rorai 2017
  it errs low (median 113.8, 79 at 2 sigma). At z 4.4 only Walther constrains it. Under Reading 2 it errs high.
- gamma = 1.5: inside 1 sigma at every anchor. Against Gaikwad and Hiss at z 3.0 it errs high (they read 1.1 to 1.3).
- T0 = 1e4 K: inside 1 sigma in the union at every anchor. Against Gaikwad and Hiss at z 3.0 it errs low (they read
  14750 to 20000 K); against Boera at z 4.4 it errs slightly high (7300 to 8100 K). In the code T0 only sets the
  thermal-broadening width.
- tau_eff formula (Becker 2013 Eq. 5 with offset): inside 1 sigma at every anchor in the union. At z 2.2 it errs low
  against Gaikwad and Walther; at z 3.0 and 4.4 it errs about 4 to 6 % high against Becker's own binned points.

## What this means for the FRAGILE flags (no relabel)

The holds flip under lambda_P x 0.5 or gamma 1.6, the fails under lambda_P x 2 or gamma 1.2. On Reading 1 the two
lambda_P triggers sit mostly outside the measurements (x 0.5 only at 2 sigma at z 2.2; x 2 only at 2 sigma at z 3.0 on
Rorai alone), so the lambda side of FRAGILE is weaker than the bracket suggests; but on Reading 2 the x 0.5 value is
inside 1 sigma everywhere, so the convention question decides it. Both gamma triggers, 1.2 and 1.6, are inside 1 sigma of
some published measurement at z 3.0 and 4.4, and the measurements themselves disagree on gamma, so the FRAGILE flags stay
live through gamma whichever lambda reading holds.

## Not covered

- No forest number was computed and no label was changed.
- Brackets apply one multiplier at all redshifts; the measurements vary with z, so a bracket can be inside at one anchor
  and outside at another, as the tables show.
- Not opened: Faucher-Giguere 2008, Becker 2011, Rorai 2013, Bolton 2014 full text, Rorai 2018 full text, the Kamble 2020
  and Turner 2024 tables. Journal references marked PROVISIONAL in SOURCES.md were not checked against journal pages.
- Every SEEN IN TEXT number came through a fetch tool's verbatim transcription; spot-check against the PDFs is advised.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
