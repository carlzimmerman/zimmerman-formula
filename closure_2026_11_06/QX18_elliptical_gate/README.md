# QX18: the a0 law on 7 X-ray ellipticals: FAIL at the G7 line (both footings, Kroupa)

Criteria: FROZEN_CRITERIA.md (032ceedf31), committed alone before any script. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. The lane was asked for as "QX17"; that id is taken (QX17_covariant_field_equations), so it is QX18.

## Label

**FAIL on both footings.** On the published NFW+stars masses of Humphrey+2006 (real_research/data/humphrey2006_ellipticals.tsv), with Kroupa
baryons and gas neglected, the a0 law under-predicts these 7 X-ray ellipticals by more than G7's 0.15 dex. The
galaxies are spherical, so the action's exact field equals the law, and the label applies to the action as well.

| | canonical | alt |
|---|---|---|
| D (Kroupa, graded) | **+0.210** | **+0.189** |
| median | +0.216 | +0.194 |
| D (Salpeter, systematic) | +0.071 | +0.053 |
| error, galaxy-to-galaxy / CFG32-style (with IMF) | 0.076 / 0.158 | 0.075 / 0.155 |
| significance (reported only) | 1.33 sigma | 1.21 sigma |
| label at the G7 line | **FAIL** | **FAIL** |

## What the FAIL means, and what it does not

- **This is a line FAIL, not a significance FAIL.** At 1.2-1.3 sigma with the IMF in the error, the shortfall is not
  established statistically. That agrees with CFG32, whose label stays "large but not established" (+0.28 / +0.25 at
  5-70 kpc, 1.7 / 1.6 sigma). QX18 relabels nothing in CFG32.
- **The IMF decides most of the size.** With Salpeter, D would be +0.07 / +0.05, a PASS. The criteria fixed Kroupa
  before grading, by the record's own prior choice (h10, CFG32, QX5), so the label is FAIL.
- **Gas is neglected,** so the miss is an upper bound. To null it at 8 Re, the outer galaxies need hot gas of:
  - NGC 720: 6.3 M*
  - NGC 4649: 4.7 M*
  - NGC 4472: 3.2 M*
  - NGC 1407: 2.3 M*

  (canonical). That is far more than the gas X-ray atmospheres hold inside 8 Re. The other three need 0.3-0.7 M*.
- **The shortfall grows outward in 7 of 7 galaxies** (points at 2 -> 4 -> 8 Re). A wrong M*/L would move the inner
  points most. This repeats CFG32's H2.
- **It is carried by three to four galaxies.** NGC 720, 4649, 4472 and 1407 sit at +0.22 to +0.51. NGC 4125, 4261 and
  6482 sit within 0.08 of zero.

## Mass trend (reported)

- **No trend inside the sample.** Spearman(d, log Mvir) = +0.11 and Spearman(d, log L_K) = -0.07, on both footings.
  The sample's own masses do not scale toward clusters.
- **As a ladder of system classes,** plain-law offsets rise from these ellipticals (+0.19-0.21) to groups (RQ3 B2:
  +0.16 at R500, +0.35 at R2500, canonical) to X-COP (+0.47 / +0.44, QX2). Seven galaxies with no internal trend
  cannot show that this is one continuous mass scaling.

## Known answers and controls

- KA1: D reproduces QX16's fixed +0.210 / +0.189 with |diff| 1e-4 / 2e-4, inside the frozen 1e-3. The script's check
  also allows half a printed digit (5e-4); the numbers meet the frozen line without that allowance.
- KA2: the law matches an independent root of the AQUAL identity mu(g/a0) g = g_N, mu = x/(1+x), to 2.2e-16.
- M1 (Newton): D = +0.416 on both footings, so it fails as required. The control bites.
- M2 (planted +-0.3 dex): D shifts by exactly +-0.300. The -0.3 plant flips the label from FAIL to PASS. The control
  bites.

## Files

- `qx18.py`
- `qx18.out`, `qx18.json` (main run)
- `qx18_MUTATE.out`, `qx18_MUTATE.json`; the MUTATE run exits 0 when every control bites.

## Not covered

- Published best-fit NFW+stars models are used, not deprojected X-ray profiles. Hot gas is absent from the baryons:
  the repository has no gas profiles, and fetching them needs the owner's go.
- No external field or environment is included. NGC 4472 and 4649 are Virgo members.
