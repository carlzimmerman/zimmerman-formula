# RRL2 RESULT: row 28 under one convention

2026-11-14. TEST lane. Adopts nothing, relabels nothing (RAW1, MWT1, MWT2, RRL1, RRL1R keep their labels), does not
edit the scorecard, registers nothing. Criteria `FROZEN_CRITERIA.md` (2859f64033, alone, before any script or
number). Script 60a87541e9 (committed before any run). Graded run and post hoc 226c2bd986. No amendment. Not pushed.
A second run reproduced `rrl2_results.json` and `rrl2_MUTATE.out` byte for byte; `rrl2.out` differs only in
elapsed-time lines.

## Words (as frozen; per case, per footing; standing a0 9.3603e-11 / 1.1312e-10)

| case | canonical | alt |
|---|---|---|
| **FW census** | **NO VERDICT** (row passes in 0.28 of slope draws), FRAGILE | **NO VERDICT** (0.17 of draws), FRAGILE |
| FW rc | ROW 28 PASSES UNDER ONE CONVENTION, FRAGILE | ROW 28 PASSES UNDER ONE CONVENTION, FRAGILE |
| **DESI NFW (H)** | ROW 28 PASSES UNDER ONE CONVENTION, FRAGILE (no footing) | |
| Newton (N) | STILL FAILS [20-30, 30-40, 40-55 HOT], robust | |

The framework and DESI's NFW get the same reading in every convention tried, so this lane separates nothing between
them. **The frozen mutations MU1 and MU2 FAILED to bite** (below). So the primary case has no power. The rc and H
"passes" come from a sigma_f of 0.2 to 0.3 and must not be read as passes. The honest headline is **NO VERDICT for
row 28 under the own-cells convention**. Whether the old "STILL FAILS" holds once beta(r) and C are used is answered
by bracket B1, which the own-cells stars accept (post hoc, below): there **the 40-55 kpc COLD fail is gone for every
smooth model**.

## The own-cells slope (the measurement of this lane)

These are the PS1 cells that hold RAW1's BHB stars: 1,033 cells, 2,631 deg^2. Masks, completeness and cuts are RRL1's.
The fit runs over 20-80 kpc with N = 1,221.
- Single law: 4.705 [4.623, 4.788]. Full sky gives 4.770.
- Broken law: inner 4.93 +/- 0.10, outer **1.62 +/- 0.87**, break 59.6 +/- 2.3 kpc. 2 dlnL 18.0 > T_own 11.3, so the
  break is detected and this profile is used. The outer slope is barely above the 1.38 convergence bound, and it
  rests on the few stars beyond 60 kpc.
- MD: on this footprint and N, mocks drawn from the full-sky law (5.29 / 3.93 / 39.0) are detected with the outer
  slope recovered in 5 of 5. The footprint can see the full-sky shape.
- **POST HOC** (`rrl2_posthoc.out`, changes no word): the own-cells stars do NOT reject the full-sky shape. 2 dlnL
  between the own best broken law and the full-sky shape is 1.74, and 73 per cent of mocks drawn from the full-sky
  law give more. The full-sky shape beats the own single law by 16.3. RRL1's opposite-shape hint at 20-45 kpc
  (3.76 / 5.75 / 25.6) does not carry over to 20-80. The own-cells best fit is one point on a flat likelihood ridge.

## f per bin (f +/- sigma_f, word; canonical / alt side by side in the rows)

| run | case | 20-30 | 30-40 | 40-55 | 55-80 |
|---|---|---|---|---|---|
| **P own-cells + C** | FW census can | 0.989+/-0.225 P | 0.969+/-0.312 P | 0.699+/-0.290 P | 0.487+/-0.310 P |
| | FW census alt | 0.950+/-0.217 P | 0.928+/-0.299 P | 0.668+/-0.278 P | 0.465+/-0.297 P |
| | H | 0.979+/-0.099 P | 0.970+/-0.191 P | 0.736+/-0.212 P | 0.543+/-0.247 P |
| B1 full-sky + C | FW census can | 1.061+/-0.034 P | 1.088+/-0.062 P | 0.972+/-0.069 P | 0.954+/-0.118 P (NO VERDICT, draws 0.82) |
| | FW census alt | 1.019+/-0.033 P | 1.043+/-0.059 P | 0.930+/-0.066 P | 0.912+/-0.113 P (PASSES) |
| | FW rc can / alt | 0.996 / 0.981 P | 1.025 / 1.006 P | 0.917 / 0.898 P | 0.901 / 0.881 P (PASSES both) |
| | H | 1.035+/-0.033 P | 1.034+/-0.058 P | 0.926+/-0.065 P | 0.926+/-0.109 P (PASSES) |
| B2 own-cells, no C | FW census can / alt | 0.923 / 0.885 P | 0.792 / 0.758 P | 0.483 P / 0.461 C | 0.346 C / 0.330 C (STILL FAILS) |
| | H | 0.949 P | 0.872 P | 0.579 P | 0.444 C (STILL FAILS) |
| B3 own-cells + C, no S2 | FW census can / alt | 0.986 / 0.947 P | 0.966 / 0.925 P | 0.677 / 0.647 P | 0.487 / 0.465 P (NO VERDICT / PASSES) |
| | H | 0.975 P | 0.967 P | 0.713 P | 0.543 C (STILL FAILS) |
| B4 own-cells single 4.705 + C | FW census can | 1.012 P | **1.141+/-0.063 H** | 1.086 P | 1.066 P (STILL FAILS) |
| | FW census alt | 0.972 P | 1.094 P | 1.040 P | 1.019 P (PASSES) |
| | H | 0.985 P | 1.082 P | 1.030 P | 1.027 P (PASSES) |
| R1 full-sky + C, no S2 (reported) | FW census can / alt | 1.057 / 1.015 P | 1.085 / 1.039 P | 0.942 / 0.901 P | 0.954 / 0.912 P (PASSES both) |
| | H | 1.031 P | 1.030 P | 0.897 P | 0.926 P (PASSES) |
| R3 = RRL1 at standing a0 | FW census can / alt | 1.058 H / 1.016 P | 1.052 / 1.008 P | **0.857 / 0.820 C** | 0.887 / 0.848 P |

The rc cases and all brackets are in `rrl2.out`. The rounded a0 (R2) changes nothing beyond 0.001.

The step that matters is B1 against R3: the same full-sky slope, before and after C. MWT1's measured beta(r)
(0.44 beyond 40 kpc) and the S2 mask lift 40-55 kpc from 0.857 to 0.972 (canonical) and from 0.820 to 0.930 (alt),
and DESI's NFW from 0.820 to 0.926. Without the S2 mask (R1) the lift is 0.942 / 0.901 / 0.897, so most of it comes
from beta(r), not from removing cold stars. In every case the 30-40 bin stays within 2 sigma (1.088 / 1.043).

## Known answers, twins, mutations

- KA1: RRL1 reproduced exactly. Full-sky fit 5.293 / 3.934 / 39.0. Every f and sigma_f of the six cases matches to
  under 1e-9, including 0.857 / 0.820. PASS.
- KA2: MWT1's C reproduced exactly (40-55 census canonical 1.1645; four FW cases and H, differences 0). PASS.
- KA3: RRL1's same-profile check, N 996, 5.139. PASS.
- KA4: SI check, M(30 kpc) 2.3311e11. PASS.
- KA5: 1,033 own cells. PASS.
- TW1 (null twin, true f = 1): the row passes in 20 of 20 seeds. PASS (the twin does not bite, as required).
- **MU1 (true f 0.80 at 40-55): COLD in 0 of 20. FAILED to bite. MU2 (true f 1.25 at 30-40): HOT in 0 of 20.
  FAILED.** The primary's sigma_f carries the own-cells slope uncertainty (0.22-0.30), so it cannot see a 20-25 per
  cent change in any bin. This is why the primary's words carry no weight.
- MD: 5 of 5 (see above).
- External field (owner's actual-field reading, e_N 0.000160 / 0.000110): nu changes by at most 2e-5 at 80 kpc. The
  no-field line is that reading here.
- S2 cold group against RRL1's RR Lyrae chain: the 24 S2 stars at 40-55 kpc lie at RA 230-318, Dec +4 to +68, r 40-51
  kpc. None lies within 10 deg of the chain (nearest 18 deg), and no own cell lies within 10 deg of it. **They are not
  the same structure.** The chain lies outside the BHB footprint.

## What this does to row 28

As frozen: NO VERDICT for the framework (census, both footings), and an unpowered pass for rc and for DESI's NFW.
FRAGILE everywhere, and nothing separates the framework from DESI's NFW. Row 28's "STILL FAILS" (40-55 COLD) came from
pairing RAW1's constant beta with the RR Lyrae slope. Read together:
- Under one convention with the measured beta(r) and the full-sky slope (B1), which the own-cells stars do not reject
  (post hoc), 40-55 passes for every smooth model.
- The row passes on census alt, both rc cases and DESI's NFW. Census canonical sits at the edge (all four bins PASS,
  row passes in 0.82 of slope draws, so NO VERDICT by the frozen 0.84 line).
- With the own-cells single law, 30-40 goes HOT again for census canonical only.

Fair statement: under a consistent convention, row 28 is no longer a fail. It is not a pass either: the
own-sky slope beyond about 40 kpc is not pinned, and every smooth model, DESI's NFW included, moves the same way.
So the row tests nothing that separates the framework. This is not a pass of the theory and awaits an independent
re-grade.

## Traps and limits

- RRL1's PS1 cuts, completeness and Sgr band are inherited. Full sky, the outer slope moved 3.35-4.20 with them.
- MWT1's S2 and X-err detections are reused, not redone.
- The rb lower bound of 22.5 was chosen knowing RRL1's 25.6 (disclosed). The fit landed at 59.6, so the bound did not
  matter.
- The frozen NO VERDICT rule uses the band 0.16-0.84 only. Pass fractions below 0.16 with a nominal PASS (rc, H) fall
  through to "PASSES". The failed mutations expose that. The rule should have tested power.
- Spherical Jeans. Same-profile assumption for BHB and RR Lyrae.

## Files

`FROZEN_CRITERIA.md`, `rrl2.py`, `rrl2.out`, `rrl2_results.json`, `rrl2_MUTATE.out`; post hoc `rrl2_posthoc.py`,
`rrl2_posthoc.out`. Run: `python3 -I -B rrl2.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits>` (about
70 s, one thread; the data are not in the repository and the script checks their sha256).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
