# EXR2 (WIDE-LENS X-RAY CUSP, SECOND MEASUREMENT): RESULT

**Frozen word: NOT EVALUABLE / NOT EVALUABLE** (canonical / alt). Check K2 failed because the criteria misread a
flag of the eROSITA service (`AMENDMENT_A1.md`). **Post hoc reading A1: CUSP EXCLUDED / CUSP EXCLUDED**, the same in
all six brackets. Part C: frozen NOT EVALUABLE; A1 reading WIDE LENSES ARE BRIGHTER IN X-RAYS [BRACKET-DEPENDENT:
band 024].

A second route, sharing only ESZ1's gas model and the eROSITA service with EXR1, reaches EXR1's conclusion: eRASS1
does not see the X-rays that the r⁻² gas cusp must emit. Like EXR1's, it is a reading, not a word, because a frozen
check failed. EXR2 was meant to give this question a frozen word and did not. Not a blind re-grade. No outcome here
is a pass.

2026-11-12. Criteria `512015c599` (alone, first); frozen run `0712e53975`; amendment `c571f1b90a` (alone, before
any amended number); A1 run `bb9cd129db`.

## The numbers (reading A1)

Units: 10⁻¹⁵ erg s⁻¹ cm⁻², 0.6–2.3 keV, in the service's own flux convention. Canonical / alt where two values.

| | |
|---|---|
| Wide lenses stacked (ESZ1's 237) | 237 of 237 (median exposure 219 s, background 0.63 counts) |
| Measured stack, lens minus its 8 offsets | **+2.48 ± 2.23** (bootstrap 0.86; null-stack rms 2.23) |
| Same, unweighted | +2.94 ± 0.90 |
| Least prediction, metal-free gas (Z = 0) | **26.0 / 22.3**, so 10.5 / 8.9 σ above; measured + 2 σ is 27 / 31 % of it |
| Least prediction, Z = 0.3 solar | **146 / 125**, so 64 / 55 σ above; measured + 2 σ is 4.8 / 5.6 % of it |
| Gas mass the stack still allows (same profile and temperature) | at most 52 / 56 % (Z = 0); 22 / 24 % (Z = 0.3) |

"Least" is the least demanding setting: source at infinite distance, stars 0.10 dex above Salpeter, least hydrostatic
temperature, only gas outside the Einstein radius and inside 15″, times 0.80 (aperture) and 0.40 (absorption). At
Salpeter stars the predictions are 33.8 / 29.2 and 190 / 163; with sources near z ≈ 2, 105 / 93 and 434 / 380.

**Brackets** (measured ± σ; Z = 0 prediction canonical / alt; every one reads CUSP EXCLUDED on both footings):
band 0.2–2.3 keV +2.81 ± 3.62 against 26.3 / 22.6; inner radius 2 R_E 11.6 / 10.2; transmission 0.25 16.3 / 14.0;
unweighted +2.94 ± 0.90 against 26.9 / 23.2; grade A only (141) +2.92 ± 0.72 against 16.1 / 13.6; z_l ≤ 0.6 only
(154) +2.94 ± 3.26 against 37.7 / 32.4. The tightest case is Z = 0 with emission counted only outside 2 R_E on the
alt footing: measured + 2 σ is 68 % of the prediction. For Z = 0.3 the tightest is 13 %.

**What law S needs** (median, least setting): 3.18 / 2.82 × 10¹² M☉ of gas inside 300 kpc (5 / 8 % of lenses need
none), 0.20 / 0.18 electrons per cm³ and 0.48 keV at the Einstein radius. Outside R_E that gas emits a median
1.4 / 1.1 × 10⁴³ erg/s in the band if metal-free and 5.8 / 4.4 × 10⁴³ at 0.3 solar (means 3.3 / 2.7 × 10⁴³ and
1.4 / 1.2 × 10⁴⁴).

## Why the frozen word is NOT EVALUABLE

The criteria used a position only if the service's `Flag_pos` was 0, taking the flag for bad data. It marks an
aperture that holds a catalogued source. All 128 catalogued sources of the flux-scale check K2 are flagged at their
own positions, so K2 had nothing to measure and failed; and 36 of the 237 wide lenses were dropped, the
X-ray-brightest ones (counts up to 19). Dropping them lowers the stack, the side that favours EXCLUDED. The frozen
numbers (195 lenses, +1.75 ± 0.47 against 18.9 / 16.0 and 104 / 87) are therefore not a result. Reading A1 ignores
the flag for targets and offsets alike and changes nothing else; under it K2 reads 1.046 (128 sources; −0.002 when
moved 0.1°).

## Against EXR1

| | EXR1 (reading A1) | EXR2 (reading A1) |
|---|---|---|
| Band, conversion | 0.2–2.3 keV, folded through an ARF and RMF | 0.6–2.3 keV, the service's Γ = 2 conversion |
| Lenses | 263 | 237 |
| Measured | +4.19 ± 0.85 | +2.48 ± 2.23 (0.2–2.3 keV bracket: +2.81 ± 3.62) |
| Z = 0 prediction | 78.0 / 67.3 | 26.0 / 22.3 |
| Prediction over measured + 2 σ, Z = 0 | 13 / 11 | 3.7 / 3.2 |
| Sky offset of random apertures | +1.61 | +1.53 (0.6–2.3 keV), +2.84 (0.2–2.3 keV) |

The two agree on the conclusion and on the size of the signal. EXR2's margin is smaller because it grades a harder
band, where a 0.5 keV gas emits less, and applies two deliberately low factors.

## Part C, Part D

**Part C** (237 pairs, ESZ1's own controls): wide minus control +1.73 [+0.09, +3.45] at 0.6–2.3 keV and
+1.81 [−0.25, +4.01] at 0.2–2.3 keV. Stacks: wide +2.48 ± 2.23, controls +1.41 ± 0.61.
**Part D:** the wide-lens stack as a mean luminosity is 2.2 × 10⁴² erg/s (0.6–2.3 keV observed, no K-correction).
Per lens, the service's own 3 σ limit lies below the lens's least prediction for 29 / 25 of 237 (Z = 0) and 86 / 70
(Z = 0.3) in eRASS1, and for 25 / 22 and 68 / 62 of the 163 unflagged lenses in the three-survey DR2 limits. Single
lenses mostly cannot decide; the stack does.

## Checks and twins (reading A1)

All pass. K1 the service's constant: 8.1534e-12 (0.6–2.3) and 8.2439e-12 (0.2–2.3), spread 1e-7 over 2,057 and 1,405
empty apertures; implied conversion 1.0687e12 against the published 1.074e12. K2 flux scale 1.046. K3 largest null
stack 5.63 against σ 2.23. K4 Λ(1 keV, Z = 0) 7.99e-24 against 8.01e-24; lines raise the band emissivity 4.7 times.
K5 ESZ1's gas reproduced exactly. K6 integral 2.5e-6. Twins all exit 1: `inject` (Z = 0 reads ALLOWED / ALLOWED),
`shift` (K2 reads −0.002), `newton` (pred rises to 62.5). The frozen run's twins also exit 1, `shift` trivially.

## Reading (mine; not part of any word)

1. Two measurements by different routes say the hydrostatic gas cusp is not there. With ESZ1's pressure result for
   cored bodies, no hydrostatic hot gas body tested supplies the wide lenses under law S.
2. Neither X-ray lane has a frozen word. EXR1 failed on a null test, EXR2 on a flag; both errors were in the
   criteria and both were caught by a check. There is no fresh sample to freeze against (same lenses, same survey),
   so a third lane would be frozen in name only. A blind re-grade by a session that has read neither result is the
   remaining honest step.
3. The metal-free case is the weak one: a factor 3 to 4 on the primary, 1.5 in the harshest bracket. Any metals
   (0.3 solar) make it 8 or more everywhere. Gas this dense that has never been enriched is not a natural reading,
   but that is an argument, not a measurement.
4. For the framework: nothing passes and nothing new fails. The wide-lens residual is not hydrostatic hot gas. It
   does not say what it is, and there is still no constructed state for it.

## Disclosures

- **Not blind.** EXR1's result was read before the criteria were written; its numbers are listed there.
- **Order.** Criteria; fetch (12 requests, 16 MB, kept outside git, manifest here); frozen run and its twins;
  diagnostic of the K2 failure on the stored answers; amendment committed alone; the switch `EXR2_AMEND=A1` added to
  `exr2.py`; the frozen run repeated with the switch unset (`exr2.out`, `exr2_results.json`, `exr2_per_lens.csv`
  byte-identical); A1 run and twins.
- **σ under A1** is the null-stack rms, 2.6 times the bootstrap: one null stack reaches 5.6 because an offset sits
  on a bright source and the weighting is by exposure. It is kept as frozen; it works against EXCLUDED.
- **Hand estimates against outcome.** Criteria: valid lenses 230 (195 frozen, 237 under A1); σ 0.5 to 1 (0.47,
  2.23); measured 1 to 4 (1.75, 2.48); pred(Z = 0) 20 to 50 (16 to 26); pred(Z = 0.3) 100 to 250 (87 to 146);
  word CUSP EXCLUDED (frozen: NOT EVALUABLE). Amendment: stack about 5 (2.48; the estimate forgot that the offsets'
  own +1.5 is subtracted); Z = 0 close to the line in two brackets (68 % and 50 %, still excluded).
- **Rest on memory, not on a fitted response:** the 0.80 aperture allowance, the 0.40 transmission and the direction
  of the Γ = 2 conversion for a soft spectrum. EXR1's response-folded route is the cross-check on all three.
- Before freezing, two requests were sent to the service at eight positions with no lens (listed in the criteria).
- Part D's DR2 count uses unflagged lenses only (163); the amendment did not cover it.

## Limits

Spherical, hydrostatic, single-phase gas in collisional ionisation equilibrium; photometric lens redshifts; the far
source is the least mass. Gas colder than hydrostatic emits below the band and is not tested. AGN or group emission
at a lens adds flux, which works against EXCLUDED. It tests no part of a₀ or κ.

## Acknowledgement required by the data

This work is based on data from eROSITA, the soft X-ray instrument aboard SRG, a joint Russian-German science
mission supported by the Russian Space Agency (Roskosmos), in the interests of the Russian Academy of Sciences
represented by its Space Research Institute (IKI), and the Deutsches Zentrum für Luft- und Raumfahrt (DLR). The SRG
spacecraft was built by Lavochkin Association (NPOL) and its subcontractors, and is operated by NPOL with support
from the Max Planck Institute for Extraterrestrial Physics (MPE). The development and construction of the eROSITA
X-ray instrument was led by MPE, with contributions from the Dr. Karl Remeis Observatory Bamberg & ECAP (FAU
Erlangen-Nuernberg), the University of Hamburg Observatory, the Leibniz Institute for Astrophysics Potsdam (AIP),
and the Institute for Astronomy and Astrophysics of the University of Tübingen, with the support of DLR and the Max
Planck Society. The Argelander Institute for Astronomy of the University of Bonn and the Ludwig Maximilians
Universität Munich also participated in the science preparation for eROSITA. (Merloni et al. 2024, A&A 682, A34;
Tubín-Arenas et al. 2024 for the upper-limit service.)

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
