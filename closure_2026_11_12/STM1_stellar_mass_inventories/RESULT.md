# STM1 RESULT: read from the full texts, MWI1's classes mostly hold; two of its rows change and the cold-gas range moves the canonical count between 0 and 3

2026-11-12. Criteria `FROZEN_CRITERIA.md` (frozen 2026-11-12T20:26:09Z, sha256 3739d2ed...7f65 in
`FREEZE_STAMP.txt`), `AMENDMENT_A1.md` (written after reading the sources, before any z). TEST lane.
Adopts nothing. Relabels no other lane. All published numbers are web look-ups and are PROVISIONAL.
kappa = 1/2 FITTED; not theory closed.

## Labels

Need (lower end used): canonical 7.050, alt 6.356 x 10^10 Msun at cold gas 1.191 (MWI1's need,
unchanged). Core set n = 7 (LN15, McM17, C20, BHG16, L25, I25, BR13); with extras n = 9 (+ L24, P20).

| reading | canonical | alt |
|---|---|---|
| H1 (headline, gas 1.191) | **SUPPLIED BY 2 OF 7 (LN15, I25)**; 2 of 9; census NOT SUPPLIED | **SUPPLIED BY 3 OF 7 (LN15, I25, BR13)**; 4 of 9 (+P20); census WITHIN 2 SIGMA |
| C1 (common convention, gas 1.191) | **SUPPLIED BY 1 OF 7 (LN15)**; 2 of 9 (+P20); census NOT SUPPLIED | **SUPPLIED BY 2 OF 7 (LN15, BR13)**; 3 of 9 (+P20); census WITHIN 2 SIGMA |
| H-lo (gas 0.805) | **SUPPLIED BY 0 OF 7**; 0 of 9; census NOT SUPPLIED | **SUPPLIED BY 3 OF 7 (LN15, I25, BR13)**; 4 of 9; census NOT SUPPLIED |
| H-hi (gas 1.440) | **SUPPLIED BY 3 OF 7 (LN15, I25, BR13)**; 4 of 9; census NOT SUPPLIED | **SUPPLIED BY 3 OF 7 (LN15, I25, BR13)**; 4 of 9; census WITHIN 2 SIGMA |
| C-lo (gas 0.805) | **SUPPLIED BY 1 OF 7 (LN15)**; 2 of 9; census NOT SUPPLIED | **SUPPLIED BY 2 OF 7 (LN15, BR13)**; 3 of 9; census NOT SUPPLIED |
| C-hi (gas 1.440) | **SUPPLIED BY 2 OF 7 (LN15, BR13)**; 3 of 9; census NOT SUPPLIED | **SUPPLIED BY 2 OF 7 (LN15, BR13)**; 3 of 9; census WITHIN 2 SIGMA |

On the common convention the canonical need is supplied only by the 2015 meta-analysis (and the extra
DES model) at every gas value but the highest, where Bovy and Rix's disc plus Portail's bar joins. The
record's census (McMillan 2017) never supplies canonical (z 2.41 to 3.52) and is within 2 sigma for alt
except at the low gas end.

## The inventories as read (10^10 Msun; the error is the upward total)

| id | source (full text, section) | headline H | common C | IMF; remnants / brown dwarfs; radius; scale length |
|---|---|---|---|---|
| LN15 | Licquia and Newman 2015, abstract and Table 6 | 6.08 +- 1.14 (disc 5.17 +- 1.11, bulge+bar 0.91 +- 0.07) | 6.56 + 1.23 | Kroupa; remnants in, brown dwarfs subtracted (3.25 of 38 Msun/pc^2, Sec. 4.1; added back for C, x 38/34.75 on the disc); all radii; Ld 2.15 +- 0.14 (Bovy-Rix), R0 8.33; disc normalisation is dynamical |
| McM17 | McMillan 2017, abstract, Tables 2 and 3 | 5.43 +- 0.57 (statistical only; median 54.3 +5.6 -5.8 e9) | same | dynamical (no IMF); everything gravitating; bulge 0.923 (prior from Bissantz and Gerhard); thin 2.50, thick 3.02 kpc; systematics "of the same order" as statistical, no number (Sec. 7) |
| C20 | Cautun et al. 2020, abstract and Table 2 (contracted NFW) | 5.04 +0.43 -0.52 (bulge 0.94, thin 3.18, thick 0.92) | same | dynamical; gas fixed at 1.2; thin 2.63, thick 3.80 kpc; pure-NFW variant 5.97 +0.40 -0.80 (not headline) |
| BHG16 | Bland-Hawthorn and Gerhard 2016, Sec. 6.4.4 and margin | 5 +- 1 | same | dynamical disc (38 Msun/pc^2) plus Kroupa (+-10%) bulge/bar; models give 5.7, 5.0, 4.7 for Rd = 2.15, 2.6, 3.0; thin disc Rd 2.6 +- 0.5 |
| L25 | Lian et al. 2025 abstract, with ERRATUM (ApJL 1003, L51, 2026; doi 10.3847/2041-8213/ae6e40) | 2.659 +- 0.353 (syst) +- 0.095 (stoch) -> + 0.366 | same (flagged) | Kroupa 0.1 to 100; remnants in; brown dwarfs out, fraction not stated; disc 1.935, bulge 0.673 before erratum (B/T 0.26 kept); outer disc scale length 2.1 kpc (8 to 14 kpc) |
| I25 | Imig et al. 2025 disc (abstract; Sec. IV.3; Sec. VII) + Portail et al. 2017 bar/bulge (abstract) | 5.27 + 1.88 = 7.15 + 0.23 | 3.70 + 1.88 = 5.58 + 0.18 | Kroupa; 5.27 (+0.2, -1.5) is the INITIAL mass; the paper's own present-day (luminous + remnant) disc is 3.7; integrated 0 to 30 kpc; Rd 2.37 +- 0.2; Portail: Kroupa mass-to-clump, M2M dynamical |
| BR13 | Bovy and Rix 2013, Sec. 5.2.1 + Portail 2017 | 4.6 + 1.88 = 6.48 + 0.32 | same | dynamical (stars and remnants, 38 +- 4 Msun/pc^2, brown dwarfs implicitly in); R0 = 8 kpc with +3.0 per kpc; Rd 2.15 +- 0.14; their own baryonic total 5.9 +- 0.5 |
| L24 (extra) | Lian et al. 2024, arXiv:2406.05604, Methods | 4.81 +- 0.13 (Xiang 2018 disc 3.6 x 1.08 + LN15 bulge) | same (flagged: IMF not stated) | literature composite; alternative 3.20 +- 0.13 with a flattened inner disc |
| P20 (extra) | Pieres et al. 2020 (arXiv:1904.04350), Sec. 5 | 5.97 +- 0.99 | 6.46 + 1.07 | Chabrier (x 0.66/0.61 to Kroupa); bulge fixed; remnants not stated (flagged) |

Not graded (component only): Portail et al. 2017 bar/bulge 1.88 +- 0.12 (inner disc in the bar region
1.29 +- 0.12; dynamical mass in the bulge volume 1.85 +- 0.05).

## Cold gas (10^10 Msun, with helium)

| source | HI | H2 | helium |
|---|---|---|---|
| McMillan 2017 (Sec. 2.3, Table 1) | 1.10 | 0.12 | HI stated including helium; H2 not stated |
| Kalberla and Kerp 2009 (Sec. 3, Kalberla et al. 2007 model) | 0.80 | 0.25 | not stated; McMillan 2017 reports Kalberla's HI values include helium; WIM 0.2 excluded |
| Nakanishi and Sofue 2016 (Sec. 4.2, within 30 kpc) | 0.72 | 0.085 | not stated (x 1.36 at the high end); notes HI may be 2 to 2.5 x higher if optically thick |
| Heyer and Dame 2015 (via Rice et al. 2016 Sec. 4.1, SECONDARY) | - | 0.10 +- 0.03 | not stated |

Range: low 0.805 (NS16 HI + NS16 H2 as stated), high 1.440 (McM17 HI + KK09 H2 x 1.36). MWI1's 1.191
sits inside it. The stellar need moves one for one: canonical 6.80 to 7.44, alt 6.11 to 6.74.

## Which of MWI1's rows changed class, and why

- **I25 (Imig plus a bulge).** MWI1: NOT SUPPLIED canonical (z 4.14), SUPPLIED alt (0.84). Two errors in
  MWI1's input cancel the wrong way. (1) The borrowed bulge (LN15's 0.91) is replaced by Portail's
  bar/bulge 1.88 as frozen: on the headline the row becomes SUPPLIED on both footings (z -0.43 / -3.41).
  (2) Imig's 5.27 is an initial mass; the paper's own present-day disc is 3.7. On the common convention the
  row is NOT SUPPLIED on both footings (z +7.96 / +4.20). Net on the common convention: alt changes
  SUPPLIED -> NOT SUPPLIED; canonical stays NOT SUPPLIED.
- **L25.** The erratum (sign error in the selection-function correction for negative heights, which made
  the north-south asymmetry spurious) raises the local surface density to 32.378 Msun/pc^2 and the total to
  2.659 (from 2.607); the factor-of-two-low conclusion stands. Class unchanged (NOT SUPPLIED, z +12.0 /
  +10.1).
- **LN15.** Unchanged in H. On the common convention (brown dwarfs added back) it moves to 6.56 + 1.23,
  z +0.40 / -0.17: still SUPPLIED, with more margin.
- **McM17, C20.** Unchanged (the full texts give the abstract numbers; McMillan's error is statistical).
- New rows: BHG16 is NOT SUPPLIED canonical by a hair (z +2.05) and WITHIN 2 SIGMA alt; BR13 plus
  Portail is WITHIN 2 SIGMA canonical and SUPPLIED alt.

## What a change of IMF would have to do

Mass ratio Salpeter / Kroupa = 1/0.66 = 1.52; Kroupa / Chabrier = 0.66/0.61 = 1.08 (Madau and Dickinson
2014, arXiv:1403.0007, the IMF paragraph after their Fig. 4). Four of the seven core rows (McM17, C20,
BHG16, BR13) are dynamical and do not move with the IMF; LN15's disc is anchored to a dynamical local
density. For the population-synthesis rows the canonical need is 1.26 to 1.33 x Imig's present-day
composite (between Kroupa and Salpeter, about half to two thirds of the way in mass) and 2.65 to 2.79 x
Lian's (beyond Salpeter: Lian on Salpeter would be about 4.0, still short of 7.05). Alt asks 1.14 to 1.21
x Imig's composite. So no single IMF change reconciles Lian with the need; for Imig it would take an IMF
noticeably bottom-heavier than Kroupa across the whole disc.

## Checks

KA1: MWI1's z values reproduced from MWI1's inputs (+0.85, +2.84, +4.68, +4.14, +12.24; +0.24, +1.62,
+3.06, +0.84, +10.33). KA2: need 7.0503 / 6.3555. KA3: 0.66/0.61 = 1.0820. M1: halving the excess
amplitude changes 4 (canonical) and 3 (alt) classes in H1. All pass.

Reported, not graded (A1.3): BR13 at R0 = 8.2 / 8.33 kpc gives 7.08 / 7.47 (z -0.09 / -1.30 canonical),
i.e. SUPPLIED once its disc is put at the R0 the other rows use; McMillan with the statistical error doubled
in quadrature (0.81) gives z +2.01 canonical, +1.15 alt; Cautun's pure-NFW variant 5.97 gives z +2.70 /
+0.96.

## Limits

- All numbers are PROVISIONAL web look-ups. Full texts read: LN15, McM17, C20, BHG16, BR13, P17, L25
  (v1) and its erratum (publisher page, via a fetch summariser; the corrected numbers were not seen in a
  PDF), I25 (arXiv HTML), MD14, NS16, KK09, P20, L24 (via a fetch summariser). Heyer and Dame 2015 was NOT
  read; its 1.0 +- 0.3 x 10^9 is from Rice et al. 2016.
- The I25 initial-versus-present-day reading rests on the paper's own text; its Table 4 placement was
  reported as ambiguous by the summariser. Unconfirmed beyond the quoted Sec. IV.3 sentences.
- Composite rows (I25, BR13) add a bar/bulge to a disc integrated through the centre and may double count
  the inner disc (Portail's inner disc in the bar region is 1.29). This would lower them.
- R0 is not put on one value by the frozen convention; BR13 moves by +3.0 per kpc.
- Brown dwarfs are added back only for LN15 (the only paper stating the amount). L25, P20 and L24 are
  flagged, not converted.
- The cold-gas range takes whole-Galaxy totals, as MWI1 did; part of the gas lies beyond 27 kpc.
- The need is the record's rotation-curve fit, not recomputed.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `AMENDMENT_A1.md`, `stm1.py`, `stm1.out`, `stm1_results.json`,
`RESULT.md`.

## Sources (looked up 2026-11-12; PROVISIONAL)

- Licquia and Newman 2015: https://arxiv.org/abs/1407.1078 (abstract; Sec. 4.1; Table 3; Table 6)
- McMillan 2017: https://arxiv.org/abs/1608.00971 (abstract; Sec. 2.3, Table 1; Tables 2 and 3; Sec. 6.4; Sec. 7)
- Cautun et al. 2020: https://arxiv.org/abs/1911.04557 (abstract; Table 2)
- Bland-Hawthorn and Gerhard 2016: https://arxiv.org/abs/1602.07702 (Sec. 2.2; Sec. 4.2.4; Sec. 6.4.4)
- Bovy and Rix 2013: https://arxiv.org/abs/1309.0809 (abstract; Sec. 5.2.1, eq. 44)
- Portail et al. 2017: https://arxiv.org/abs/1608.07954 (abstract)
- Imig et al. 2025: https://arxiv.org/html/2507.17629 (abstract; Sec. III.3; Sec. IV.3 "Total Surviving Mass"; Sec. VII)
- Lian et al. 2025: https://arxiv.org/abs/2508.13665 (abstract; Sec. 3.2, Table 2)
- Lian et al. 2026 erratum: https://iopscience.iop.org/article/10.3847/2041-8213/ae6e40 (text and Table 2)
- Lian et al. 2024: https://arxiv.org/html/2406.05604v2 (Methods, "The Milky Way's total stellar mass")
- Pieres et al. 2020: https://arxiv.org/abs/1904.04350 (Sec. 5, total stellar mass sentence)
- Madau and Dickinson 2014: https://arxiv.org/abs/1403.0007 (IMF paragraph after Fig. 4)
- Nakanishi and Sofue 2016: https://arxiv.org/abs/1511.08877 (abstract; Sec. 4.2; Sec. 5)
- Kalberla and Kerp 2009, ARA&A 47, 27 (Sec. 3, page 35; copy at pages.astro.umd.edu)
- Heyer and Dame 2015, ARA&A 53, 583, as cited by Rice et al. 2016, ApJ 822, 52 (Sec. 4.1)

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
