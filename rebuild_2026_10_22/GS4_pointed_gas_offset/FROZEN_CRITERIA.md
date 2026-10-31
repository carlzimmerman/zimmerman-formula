# GS4_pointed_gas_offset: FROZEN CRITERIA (committed with the ledger, before any catalogue is matched to eRASS1)

**Question.** d = lg(Mgas500 pointed / Mgas500 eRASS1), same clusters, same radius, same h, as a function of mass, over the lensing sample's M500 range 4.4e13 to 5.6e14. ZN3's keys pass only with a gas raise: G-OUT-M3 reaches Z 2 at +0.093.

**Disclosed before matching.** ZN3 needs d high. So far I have read catalogue tables and column definitions and computed the gas slope below from X-COP's own files. I've compared no catalogue to eRASS1, beyond SM1 and RF3's X-COP numbers, which are already public in this repo (+0.111 at each survey's R500, +0.092 at eRASS1's R500, five clusters).

## Catalogues
Fetched and tabulated, instrument grouping fixed here:

| key | paper, table | instrument group | positions | radius of published Mgas | in primary |
|---|---|---|---|---|---|
| L20 | Lovisari+20, VizieR J/ApJ/892/102/table3 | XMM | Andrade-Santos+17 X-ray centres (J/ApJ/843/76/table4) by Planck name; if absent the table's ESZ position | own hydrostatic M500 → R500 | yes |
| L15 | Lovisari+15, on disk | XMM | NED by name | own hydrostatic R500 | yes |
| C08 | Croston+08 REXCESS, arXiv source table 1 | XMM | RXC name | own Y_X-scaled R500 | yes |
| E16 | Eckert+16 XXL-100-GC, arXiv source table 3 | XMM | IX/49/xxl100gc by XLSSC id | r500,MT, from a WL-calibrated M-T | yes |
| XC | X-COP, on disk | XMM | file headers | profile, read at eRASS1's R500 | yes |
| M08 | Maughan+08, VizieR J/ApJS/174/117 | Chandra | VizieR table | own Y_X-scaled R500 | yes |
| L13 | Landry+13, arXiv source, Vikhlinin-model row | Chandra | NED by name | own hydrostatic r500 | yes |
| S09 | Sun+09, arXiv source, measured-at-r500 rows only, Mgas = f_gas,500 × M500 | Chandra | NED by name | own hydrostatic r500 | yes |
| M13 | Mahdavi+13, arXiv source tables 1, 2 | MIXED (Chandra + XMM) | table | **WL r500**, no hydrostatic mass in the radius | yes |
| V09 | Vikhlinin+09, arXiv source, Mgas by inverting its table's f_g(M) on M_G | Chandra | NED by name | M_G's r500 | **no**, reported only, LITERATURE-INPUT: gas mass isn't tabulated |

Checked and not usable: Schellenberger & Reiprich 17 (VizieR has no gas mass), Andrade-Santos+17 (no gas mass), Pratt+09 (Y_X only; C08 is the same sample), Mantz+16 (r2500 only), Martino+14 and Zhang+08 (no per-cluster Mgas500 in the source tables read). VizieR's main CDS hosts timed out from here; the IDIA mirror served the tables.

## Matching
eRASS1 primary catalogue, RA, DEC, BEST_Z. Nearest eRASS1 cluster within **3 arcmin and |dz| < 0.01**, as SM1. Per catalogue, an eRASS1 cluster takes only its nearest row. Sensitivity, reported and not graded: 6 arcmin, since NED positions can be optical. No match by name.

## One radius, one h
1. Fixed angle to eRASS1's cosmology, h 0.70, Ωm 0.30 (GS3): Mgas × (D_A,e/D_A,pub)^2.5, R × (D_A,e/D_A,pub), with each paper's stated cosmology.
2. To eRASS1's R500: X-COP reads its profile, as RF3. Every other catalogue is slope-converted, Mgas × (R500,e/R500,pub)^s, **s = 1.19**, the median d ln Mgas / d ln r over 0.8–1.25 R500 in X-COP's 12 files (16–84 %: 1.06, 1.44), computed before matching. Those rows are labelled slope-converted. Sensitivity: s 1.0 and 1.4. d at the catalogue's own R500 is also reported.

## Statistic
Per cluster, d is the median across catalogues holding it. **Primary:** unique eRASS1 clusters with eRASS1 M500 in 4.4e13–5.6e14, V09 out. Median d, SE by bootstrap of clusters (10,000 draws, seed 0). OLS fit of d on lg M500 with bootstrapped slope. The same statistics per catalogue and per M500 tercile, with edges the **lensing sample's own M500 terciles** (1.364e14, 2.390e14 M☉, from X7's 326). Fewer than 20 primary clusters: UNDECIDED.

## Verdict, on the primary median, first applicable
1. **NO OFFSET:** |median d| under 2 SE, which is ZN3 failing on the keys. (Listed first since it also satisfies a later class. My reading of the brief's list, stated before seeing a number.)
2. **OFFSET CONFIRMED ABOVE THE LINE:** median d − SE ≥ +0.093.
3. **OFFSET BELOW THE LINE:** median d + SE ≤ +0.093.
4. **ON THE LINE:** otherwise.

Tags: **[MASS-DEPENDENT]** if the slope differs from zero by over 2σ. **[INSTRUMENT-DEPENDENT]** if the Chandra and XMM groups' classes differ.

## Cautions, reported as sensitivity rows, not graded
- eRASS1 is detection-limited, so low-mass objects are biased bright; d is then low there. And eRASS1's M500 is built from its own count rate, so noise in the flux raises its M500 and Mgas together, which tilts d against lg M500 negative with no physics. So: rows at eRASS1 CTS500 above and below the matched median, z below and above 0.2, and the fit repeated against the pointed Mgas, which has the opposite sign of that bias.
- Pointed samples are not random: mostly X-ray bright, so the matched eRASS1 objects aren't typical of the lensing sample at the same mass. The lensing sample's overlap is counted and listed.
- Mgas is measured with different centres, clumping treatment, backgrounds and calibration. Offsets between catalogues are tabulated.

## Regrade
ZN3's frozen rule, grader text unchanged except the gas factor, one template, both f★, both h: at the primary median d, and at d ± SE. If [MASS-DEPENDENT], also at the measured d(M), with the grader's M500 per cluster, reported. Class by ZN1's `cls`. One thread, nice 15, at most two processes.

## Checks
- **K1.** X-COP row reproduces SM1's five dlog Mgas500 (own R500) and RF3's at eRASS1's R500, |d| ≤ 1e-3. Where a table holds those five clusters: median |d_table − d_SM1| reported, with 0.05 dex as the line.
- **K2.** Clusters in two or more catalogues: median |pairwise difference in d| ≤ 0.05 dex, and any same-source repeat rows. A fail is reported as catalogue scatter, and its size is shown beside the SE.
- **K3.** At +0.111 the regrade path reproduces ZN3's preds and X-COP, |d| ≤ 1e-9.
- **MUTATE.** RA + 1 degree: matches fall under 10 % of the real count. Pointed catalogue shuffled against its own matched eRASS1 rows: rms of d at least × 1.5, and slope and tercile structure lost. If neither bites: UNDECIDED.

κ = ½ FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
