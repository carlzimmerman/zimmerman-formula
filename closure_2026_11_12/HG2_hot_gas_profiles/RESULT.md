# HG2 RESULT: published hot-gas laws leave MWG1's two answers standing; the outer pass is still FRAGILE

2026-11-12. Criteria `FROZEN_CRITERIA.md` (sha256 and UTC time in `FREEZE_STAMP.txt`), written before
the script. TEST lane. Adopts nothing. Relabels no other lane. Literature values are web look-ups of
arXiv full texts (PDF) and are PROVISIONAL; sections and tables are cited in the criteria.

## Labels

| footing | part 1, the rotation curve | part 2, the outer data (on MB15) |
|---|---|---|
| canonical | **ROTATION CURVE NOT SUPPLIED** | **RECORD'S FIELD PASSES WITH HOT GAS, FRAGILE** (MB15h, S15, L24z fail) |
| alt | **ROTATION CURVE NOT SUPPLIED** | **RECORD'S FIELD PASSES WITH HOT GAS, FRAGILE** (MB15h, S15, L24z fail) |

Same labels as MWG1. The FRAGILE set grew from one model (Salem 2015) to three.

## Known-answer check KA2: what closes Miller and Bregman 2015's own masses

MB15 print n0 rc^3b = 1.35e-2 cm^-3 kpc^1.5, b = 0.50 (Table 2, O VIII optically thin), fitted with
solar-abundance emissivities, and quote masses for 0.3 Zsun. In SI, with 1.17 m_p per electron:

| convention | M(<50 kpc) | M(<250 kpc) |
|---|---|---|
| as printed (solar) | 1.16e9 | 1.30e10 |
| density x (Z/Zsun)^-1 (absorption-line convention of MB13 eq. 4; MB15 Sec. 5.1 also writes DM proportional to Z^-1) | **3.85e9** | **4.31e10** |
| density x (Z/Zsun)^-1/2 (emission goes as n^2 Z) | 2.11e9 | 2.36e10 |
| quoted (abstract, Table 2) | 3.8e9 | 4.3e10 |

The printed law reproduces the quoted masses (within 1.4 and 0.1 per cent) only with the linear
Z^-1 scaling. For an emission-line fit the physically expected scaling is Z^-1/2, which gives masses
0.55 times lower. That alternative is carried as model MB15h; it is one of the three that fail.

## Enclosed masses from the published laws [1e10 Msun]

Halo plus the same paper's disc-like component; each profile stops at its paper's outer radius.

| model | law (source) | Z | r_out | <27 | <80 | <100 | <150 | <200 | <273 |
|---|---|---|---|---|---|---|---|---|---|
| MB15 | n_e = 1.35e-2/0.3 r^-1.5 | 0.3 | 250 | 0.15 | 0.78 | 1.09 | 2.00 | 3.08 | 4.31 |
| MB15h | same, /0.3^0.5 | 0.3 | 250 | 0.08 | 0.43 | 0.60 | 1.10 | 1.69 | 2.36 |
| MB13 | beta 0.46, 0.35 kpc, 0.71, + 1e-5 to 200 kpc, /0.3 | 0.3 | 200 | 0.12 | 0.51 | 0.78 | 1.89 | 3.91 | 3.91 |
| S15 | n = 1.1e-4 (r/48.2)^-1.423 (slope solved from M(300) = 2.6e10, mu 0.6) | n/a | 300 | 0.06 | 0.32 | 0.46 | 0.87 | 1.37 | 2.24 |
| F17 | n_H through 1.3e-4 (50) and 0.83e-4 (100), slope 0.647 (reconstruction) | 0.5 | 250 | 0.07 | 0.91 | 1.54 | 4.00 | 7.88 | 13.32 |
| F20 | n_H = 1.3e-5 (r/283)^-0.93 (Table 1) | 1 to 0.3 | 283 | 0.05 | 0.46 | 0.72 | 1.67 | 3.03 | 5.78 |
| B18 | r^-1.5 normalised to 2.8e10 inside 250 + hot disc 1.8e8 | 0.3 to 1 | 250 | 0.12 | 0.52 | 0.73 | 1.32 | 2.02 | 2.82 |
| K20b | n = 0.0044 (r/2.4)^-1.17 + empirical disc | 0.3 | 260 | 0.12 | 0.75 | 1.13 | 2.35 | 3.97 | 6.40 |
| L24 | C = 4.6e-2, b = 0.5 + disc 3.2e-2, 6.2, 1.1 kpc | 0.1 | 350 | 0.20 | 0.85 | 1.16 | 2.09 | 3.20 | 5.07 |
| L24z | C = 1.36e-2 + disc 9.4e-3 (high-emissivity row) | 0.3 | 350 | 0.06 | 0.25 | 0.34 | 0.62 | 0.95 | 1.50 |

Formula: power law n = C r^-a gives M(<r) = m 4 pi C r^(3-a)/(3-a), with m = 1.17 m_p per electron
(X = 0.71), 1.41 m_p per H, 0.6 m_p per particle for Salem; beta model and discs integrated
numerically (discs: sphere R^2 + z^2 < r^2, both sides of the plane).

Disc-like hot gas alone, inside 27 kpc [1e10 Msun]: Locatelli combined 0.046 (total 0.049);
Locatelli high-emissivity 0.013; Locatelli disc-only fit (zh = 3.3 kpc, Z = 0.1) 0.110 (total 0.130,
the largest); Kaaret empirical 0.014; Kaaret exponential 0.034; Nakashima 2018 0.009; Bregman 2018
0.018 (printed mass).

## Part 1: the rotation curve

Need: 1.71 to 2.07e10 (canonical), 1.02 to 1.39e10 (alt). Supply inside 27 kpc, halo plus own disc:
0.05 to 0.20e10. Shares: canonical 2.3 to 11.8 per cent, alt 3.5 to 19.9 per cent; the top is
Locatelli's Z = 0.1 model (halo 0.156 + disc 0.046). MB15 is unchanged at 7 to 9 / 11 to 15 per cent.
The largest disc alone supplies 5 to 6 (canonical) or 8 to 11 (alt) per cent.

**A disc-like hot component does not change the inner answer.** It adds at most 0.11e10 inside
27 kpc, and the published discs are 0.01 to 0.13e10 in total. Every model is short by a factor of 5
or more on alt and 8 or more on canonical.

## Part 2: the outer data

Census at A = 1 plus each profile; MWJ1's gates (DESI curves at 30 and 80 kpc, outer masses beyond
100 kpc, plateau rows beyond 150 kpc).

| model | window, canonical | window, alt | at 0.01273 (satellite plateau median) |
|---|---|---|---|
| none | 0 to 0.0075 | 0 to 0.0075 | fails (-2.72) |
| MB15 | 0 to 0.0180 | 0 to 0.0185 | passes (-1.42) |
| MB15h | 0 to 0.0125 | 0 to 0.0125 | fails, by 0.003 (-2.003 / -2.002) |
| MB13 | 0 to 0.0180 | 0.0010 to 0.0190 | passes (-1.28) |
| S15 | 0 to 0.0120 | 0 to 0.0120 | fails (-2.09) |
| F17 | 0.0040 to 0.0200 | 0.0045 to 0.0215 | passes (+0.24) |
| F20 | 0 to 0.0170 | 0.0010 to 0.0185 | passes (-1.23) |
| B18 | 0 to 0.0135 | 0 to 0.0135 | passes (-1.86) |
| K20b | 0 to 0.0190 | 0.0015 to 0.0205 | passes (-0.99) |
| L24 | 0 to 0.0200 | 0.0005 to 0.0200 | passes (-1.30) |
| L24z | 0 to 0.0100 | 0 to 0.0100 | fails (-2.30) |

Seven of ten published profiles pass at the record's field on both footings; three fail it on the
satellite plateau rows. Every model's window still contains fields at or below 0.008. All failures
are on the plateau rows only (the curves and outer-mass gates pass).

Variant, not labelled (`hg2_extrap.out`): extrapolating every law to 273 kpc moves MB15h to a pass
(window to 0.0130) and widens MB15 to 0.0195 (MWG1's number); S15 and L24z still fail.

## Which MWG1 statements hold and which move

- **Holds**: inside 27 kpc the hot gas supplies under a fifth of the rotation curve's need (MWG1:
  "under a sixth"; the top is now 19.9 per cent on alt from Locatelli's Z = 0.1 model, 11.8 per cent
  canonical). Whatever supplies it is in the disc or bulge as stars or cold gas.
- **Holds**: with MB15's gas, as its own paper quotes the masses, the record's field passes all three
  outer gates on both footings.
- **Moves**: MB15's window narrows from 0 to 0.0195 to 0 to 0.0180 (canonical) because the profile
  stops at the paper's 250 kpc instead of being extrapolated. It still covers M31's field (0.016 to
  0.017) on both footings.
- **Moves**: FRAGILE is broader. Besides Salem, the low-emissivity reading of MB15's own fit (Z^-1/2,
  by 0.003 in the median) and Locatelli's Z = 0.3 profile fail at 0.01273.
- **Moves**: Faerman 2017 (now reconstructed from its Table 3 densities, slope 0.65 rather than the
  remembered 2.0 in mass) still needs a field, 0.0040 or more. Its mass inside 27 kpc halves (0.07
  against 0.14).
- **Moves**: Faerman 2020's printed law is flatter than MWG1 assumed (M proportional to r^2.07, not
  r^1.5): less inside 27 kpc (0.05 against 0.16), more at 273 kpc.
- **New**: the disc-like hot gas (Locatelli, Kaaret, Nakashima, Bregman) is 1e8 to 1.3e9 Msun and
  does not change the inner answer.

## Checks

KA1 (no gas reproduces MWJ1: Q 4.89 / 2.91, plateau -2.72, window 0 to 0.0075), KA2 (above), KA3
(line at 80 kpc 5.691 / 6.218 / 4.977 / 5.109), KA4 (F20 law 5.14e10 inside 258 kpc and 6.23e10
inside 283 kpc against 4.6e10 and 5.5e10: ratios 1.12 and 1.13, inside the paper's stated 20 per
cent) and KA5 (SI shell integral equals the closed form) all pass. M1 (ten times MB15 at no field)
fails the outer gates on both footings; M2 (ten times the largest inner supply) flips Part 1 to
SUPPLIED on both footings (`hg2_mut.out`). Independent SI hand checks: Locatelli disc total
4.915e8 (script 4.91e8); Salem M(<300) 2.60e10 with the solved slope.

Reported consistency checks, not gates (no check failed; two printed numbers disagree with their law):
- MB13: 2.49e8 inside 18 kpc and 1.17e10 inside 200 kpc (solar) against 2.2e8 and 1.2e10; at 0.3
  Zsun 8.3e8 and 3.91e10 against 7.5e8 and 3.8e10. The 200 kpc mass needs the ambient 1e-5 cm^-3
  medium of Sec. 4.1 (9.7e9 of it).
- F17: 1.33e11 inside 250 kpc against 1.2e11 (ratio 1.11); mean n_H 5.9e-5 against 4.6e-5.
- S15: solved b = 0.474, n0 rc^3b = 0.027, inside Salem's sampled 0.005 to 0.03.
- **Kaaret 2020's disc**: the printed law (n0 0.0081, z0 1.6 kpc, empirical radial profile) integrates
  to 1.42e8 (7.1e7 one side), against the paper's 2e7: a factor 7 (3.5 one side) not closed by any
  convention I found.
- **Nakashima 2018's disc**: 9.7e7 both sides, against the printed 5e7; one side gives 4.9e7, so the
  paper apparently integrates z >= 0 only (eq. 11 is garbled in the text extraction).
Neither discrepancy matters here: both discs are under 1.5 per cent of the need.

## Limits

- F17 has no closed-form law; its numerical profile is in an online data file I did not retrieve.
  F17 here is a power law through two printed densities. Kaaret's preferred halo (adiabatic NFW gas,
  5.5 to 8.6e10 inside 260 kpc) has no printed law; only its disfavoured beta-model fit (K20b) enters.
- Salem's value of mu was not found in the text; 0.6 is assumed. Salem's slope is solved from two
  printed numbers, not printed.
- Masses scale with assumed metallicity (Z^-1 or Z^-1/2) and with mass per electron (1.17 m_p,
  X = 0.71 assumed). Locatelli's baseline uses Z = 0.1 Zsun, which is why L24 is heavy and L24z light.
- Bregman 2018's hot disc (1.8e8) has no law here and is placed entirely inside 27 kpc (upper bound).
- Profiles stop at each paper's outer radius (frozen); the extrapolated variant is reported.
- The Faerman models are hydrostatic in a dark-matter potential, not the framework's own.
- Part 1 is an upper-bound argument, not a refit; the need is the record's (hunt item 35).
- Outer gates have little power (NMB1, PLT1); a pass is the absence of a contradiction.
- Not found or not used: Li and Bregman 2017's disc law (only Bregman 2018's quoted mass), HaloSat's
  adiabatic halo parameters beyond rho_V, Locatelli's Fig. 7 mass curve as numbers.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `hg2.py`, `hg2.out`, `hg2_results.json`, `hg2_mut.out`,
`hg2_extrap.out` (`python3 hg2.py --extrap`). Inputs read only: NMB1's `nmb1_results.json`, PLT1's
`plt1_results.json`. Gate and baryon functions copied from MWG1's `mwg1.py`.

Sources (arXiv full texts, read 2026-11-12, PROVISIONAL): Miller and Bregman 2015, arXiv:1412.3116
(eq. 2, Table 2, Sec. 5.1); Miller and Bregman 2013, arXiv:1305.2430 (eqs. 4-6, Table 2, Secs. 4.1-4.2);
Salem et al. 2015, arXiv:1507.07935 (eq. 7, Table 6, Fig. 14, Sec. 6.1); Faerman et al. 2017,
arXiv:1602.00689 (Table 3, Fig. 4); Faerman et al. 2020, arXiv:1909.09169 (Table 1, Sec. 3.1);
Bregman et al. 2018, arXiv:1803.08963 (Sec. 2.5); Kaaret et al. 2020, arXiv:2011.00126 (main text,
Methods, table); Locatelli et al. 2024, arXiv:2310.10715 (eqs. 5, 6, 10, Table 1, Sec. 3.2);
Nakashima et al. 2018, arXiv:1806.04832 (Sec. on composite model, eq. 11).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
