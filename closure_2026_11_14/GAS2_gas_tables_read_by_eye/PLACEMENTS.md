# GAS2 placements: GAS1's tables redone with the values read by eye

Date: 2026-11-14. Not blind, not graded; relabels nothing; computes no forest number. Rule, anchors and bracket values
are GAS1's (its SCOPE.md), unchanged. Script `gas2_place.py`, output `gas2_place.out`; every input is typed from the
pages listed in CHECK.md.

## Verdict first

**No placement level changes. GAS1's headline reading stands, and one of its caveats goes away.** Under GAS1's Reading
1 every cell has the same level. What changes:

1. **GAS1's Reading 2 is void.** It rested on a factor 2 sqrt 2 that the page shows is sqrt 2 (QUESTIONS.md, question
   1). With the right factor the flux-fitted and density-defined scales map at factor 1, which is Reading 1. So
   Reading 2's cells no longer stand: 39.5 at INSIDE 1 SIGMA at all three anchors, and 79 at 2 SIGMA at z 3.0 and
   OUTSIDE at z 4.4. Half the smoothing scale is INSIDE 2 SIGMA at z 2.2 (Rorai only) and OUTSIDE at z 3.0 and 4.4,
   with no other reading left. GAS1's sentence that "the convention question decides it" for the halved scale is
   answered: it does not rescue it.
2. **Attribution only (same level):** four tau_eff cells now also list Becker, because the rule counts every Becker
   bin within 0.3 in z and GAS1 had used only some of them. These are z 2.2 s = 1.1; z 3.0 s = 1.0; z 4.4 s = 0.9
   (2 sigma) and s = 1.0. The gamma, T0 and lambda_P cells list the same or more papers than GAS1 named, at the same
   level.
3. **GAS1 READING.md sentence to drop:** "at z 3.0 and 4.4 it errs about 4 to 6 % high against Becker's own binned
   points". Within 0.3 of z 3.0 the Becker bins sit -5.5 % to +0.5 % from the fit in tau, and within 0.3 of z 4.4 they
   sit -5.8 % to +0.4 %. The record's formula is inside Becker's 1 sigma at some bins in both windows (CHECK.md).

Headline items checked against the page: the two gamma triggers (1.2 and 1.6) are each inside 1 sigma of some
measurement at z 3.0 and 4.4, and the gamma measurements disagree with each other (stands). Half the smoothing scale is
mostly outside (stands, now with no rival reading). 91.4 and 138.6 comoving kpc are Rorai et al. 2017 Table S2, z 3.0,
16 % and 84 % with systematics, median 113.8 (stands, page 43).

## lambda_P (comoving kpc; factor 1, the only reading left)

| bracket | z 2.2 | z 3.0 | z 4.4 | change from GAS1 Reading 1 |
|---|---|---|---|---|
| 39.5 (x 0.5) | INSIDE 2 SIGMA (Rorai) | OUTSIDE | OUTSIDE | none |
| 79 (primary) | INSIDE 1 SIGMA (Rorai, Walther both) | INSIDE 1 SIGMA (Walther both) | INSIDE 1 SIGMA (Walther both) | none |
| 91.4 | INSIDE 1 SIGMA (Rorai, Walther flat) | INSIDE 1 SIGMA (Rorai, Walther both) | OUTSIDE | none |
| 100 proper (320 / 400 / 540) | OUTSIDE | OUTSIDE | OUTSIDE | none |
| 138.6 | OUTSIDE | INSIDE 1 SIGMA (Rorai) | OUTSIDE | none |
| 158 (x 2) | OUTSIDE | INSIDE 2 SIGMA (Rorai) | OUTSIDE | none |

Rorai is placed with its with-systematics 16 % and 84 % bounds, as GAS1 did. Walther's intervals are statistical only;
if their stated 0.5 to 1 sigma_stat of systematics were added, Walther intervals would widen, which this lane does not
do (the rule is unchanged).

## gamma

| gamma | z 2.2 | z 3.0 | z 4.4 | change |
|---|---|---|---|---|
| 1.2 | INSIDE 2 SIGMA (Gaikwad) | INSIDE 1 SIGMA (Gaikwad, Hiss) | INSIDE 1 SIGMA (Boera, Walther flat) | none |
| 1.5 (primary) | INSIDE 1 SIGMA (Gaikwad, Hiss, Walther strong) | INSIDE 1 SIGMA (Hiss, Walther both) | INSIDE 1 SIGMA (Walther flat) | none |
| 1.6 | INSIDE 1 SIGMA (Hiss, Walther strong) | INSIDE 1 SIGMA (Walther both) | INSIDE 1 SIGMA (Walther both) | none |

Hiss's interval level is not named on its table page (CHECK.md); it is placed as 1 sigma, as GAS1 did.

## T0 = 1e4 K

| z 2.2 | z 3.0 | z 4.4 | change |
|---|---|---|---|
| INSIDE 1 SIGMA (Gaikwad, Hiss, Walther strong) | INSIDE 1 SIGMA (Walther flat only) | INSIDE 1 SIGMA (Walther both) | none |

## tau_eff (record formula x s, at each measurement's own z)

| s | z 2.2 | z 3.0 | z 4.4 | change |
|---|---|---|---|---|
| 0.9 | INSIDE 1 SIGMA (Becker) | INSIDE 1 SIGMA (Gaikwad, Walther flat) | INSIDE 2 SIGMA (Becker, Walther flat) | Becker added |
| 1.0 (primary) | INSIDE 1 SIGMA (Becker) | INSIDE 1 SIGMA (Becker, Gaikwad, Walther both) | INSIDE 1 SIGMA (Becker, Boera, Walther both) | Becker added at z 3.0 and 4.4 |
| 1.1 | INSIDE 1 SIGMA (Becker, Gaikwad, Walther strong) | INSIDE 1 SIGMA (Walther flat only) | INSIDE 1 SIGMA (Boera, Walther both) | Becker added at z 2.2 |

Mapping the asymmetric flux errors exactly into tau, instead of symmetrising them as GAS1 did, changes no cell
(`gas2_place.out` gives both).

## Not covered

- PROVISIONAL rows from papers not on disk (Bolton 2014, Rorai 2018, Kamble 2020, Turner 2024) stay PROVISIONAL; GAS1
  reported they change no cell, and they are not used here.
- Journal references in GAS1 were not checked.
- GAS1's code reading (CONVENTION.md) was not re-read; only its comparison with the papers' definitions is revisited.
- No forest number, and no FRAGILE flag, is touched.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
