# Predictions scorecard, 2026-11-12

Every registry of predictions in the repository, read against what has happened since. An audit,
not a lane: nothing was run, no frozen file was edited, no status in any registry was changed.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Verdict

**No registered prediction has come true.** Of the 115 rows and row groups below: 41 not yet tested, 20 post-dictions, 14 retired or withdrawn, 17 undecided, 12 failed, 11 consistent but not distinctive, 0 came true.
Several rows are the same prediction registered in more than one place, so the counts are of entries, not of independent claims.

"Came true" means: stated and committed before the deciding data existed or was looked at, then
matched by that data within the prediction's own tolerance. A match to data that were already
public is a post-diction. A fit with a free parameter, a test on mocks or on the project's own
simulations, and a claim later withdrawn do not qualify.

## Classes

CAME TRUE; CONSISTENT, NOT DISTINCTIVE (matches, but the standard model matches equally or the
tolerance is loose); POST-DICTION (the data already existed); UNDECIDED (tested, no decision);
FAILED (data against it); RETIRED OR WITHDRAWN (by the owner or a later lane); NOT YET TESTED.

## 1. The falsifier matrix (`deepseek_push/FALSIFIER_MATRIX.md`, built 2026-09-16)

Read in full by the lead, with its contact log. Much of it belongs to the September construction
(phantom plus dust, a particle mass) that the adopted theory has since replaced.

| row | prediction | class | latest record |
|---|---|---|---|
| 1 | wide-binary ridge: gamma_v in [1.047, 1.11], break at 7.4 kAU | NOT YET TESTED | Gaia DR4, 2026-12-02; other registries carry different values (section 7) |
| 2 | two-scale vertical dark structure at the Sun | NOT YET TESTED | Gaia DR4 |
| 3 | flaring layer z_c(R), 140.6 pc at 8.2 kpc | NOT YET TESTED | Gaia DR4 |
| 4 | close-pair excess 2.0 at s = r_M | NOT YET TESTED | public pair catalogues exist; no scoring lane in the matrix log |
| 5 | outer pressure slope -2.54 (three-way test) | NOT YET TESTED | never run on real maps: G220 pre-computed expected verdicts only; the earlier -1.44 line was retargeted on 09-16 |
| 6 | flat outer temperature tail | NOT YET TESTED | XRISM, eROSITA; the "level confirmed" is on data in hand |
| 7 | orbit anisotropy beta(2 to 5 R500) > 0.5 | FAILED | G206: combined 0.438 +- 0.014, the 0.5 rule excluded at 4.4 sigma; beta > 0 holds, which infall gives in any model; data pre-existing |
| 8 | dust fraction saturates at 1 below 3e14 | POST-DICTION | median 0.919, kill line 0.85 not crossed; the 8.1 per cent miss was explained afterwards |
| 9 | cluster core slope -1.5 | UNDECIDED | -1.53 +- 0.25; NFW gives -1.68 in the same window |
| 10 | slope floor gamma = -2.00 +- 0.02 | UNDECIDED | DESI DR2 III; NMB1 gives -2.06 +- 0.14; the registered band was the asymptote (G238) |
| 11 | deep exponent n = 2 | UNDECIDED | fired at 12.7 sigma; D04 (09-25): the firing does not test the law; the amplitude sits between the footings |
| 12 | particle mass 5.0 to 5.2 keV | RETIRED OR WITHDRAWN | marked "Never cite" in `fable_independent_2026/FINDINGS.md`; no-particle rule |
| 13 | which a0 footing (K1, K2, K3) | NOT YET TESTED | Gaia DR4, MIGHTEE; K3's reference scale is the D02 artefact |
| 14 | width of the Milky Way kink | NOT YET TESTED | G217: about a year of catalogue work for a sign verdict |
| 15 | free dust: charge or relic | NOT YET TESTED | Rubin-depth census |
| 16 | gas rise holds in every X-COP cluster | FAILED | fired on ZW1215 at 9.8 sigma; explained afterwards as hydrostatic bias; 11 of 12 hold; data in hand |
| 17 | external-field split | UNDECIDED | not established (p = 0.114); D03: the direction argument has no measurement under it |
| 18 | kernel break F(e_N) | POST-DICTION | Milky Way leg in band "at the edge" on 2019 data; pair leg not yet tested |
| 19 | the 2/3 temperature law | POST-DICTION | alpha = 0.75 +- 0.12 on X-COP in hand |
| 20 | the 2 to 3e14 gap in the cluster census | NOT YET TESTED | no such system observed |
| 21 | dark acceleration below a0/2 | UNDECIDED | SPARC 95.1 per cent conform, 150 bins over; one fit asks 2.3 times the cap |
| 22 | mass doubles at g_bar = a0/3 | CONSISTENT, NOT DISTINCTIVE | median 1.570 against 2.0, inside a 0.15 dex band; SPARC in hand |
| 23 | cluster stripping radius | POST-DICTION | 15 of 15 on a paper the repository had carried since June; row committed the evening of the contact (09-23) |
| 24 | enclosed dark mass under a0 r^2 / 2G | UNDECIDED | as row 21 |
| 25 | never-doubling class | NOT YET TESTED | its deep-end reference is the D02 artefact |
| 26 | halo field and column under the cap | POST-DICTION | SPARC 174 of 175; DR4 column pending |
| 27 | velocity-domain a0, "6 per cent agreement" | FAILED | D02: ratio 0.44 to 0.52 after the corpus correction; its own check fails in every variant |
| 28 | per-cluster stripping map | NOT YET TESTED | needs an IFU sample |
| 29 | RAR gradient law and Oort coupling | POST-DICTION | SPARC slopes; DR4 A/B pending |
| 30 | point-mass halo laws | NOT YET TESTED | none |
| 31 | local density saturates the slab ceiling | POST-DICTION | 3.6 per cent agreement with a February 2026 map; DR4 pending |
| 32 | Milky Way mass plateau | UNDECIDED | PLT1: PASSES, FRAGILE; fails low against satellite masses beyond 150 kpc (median -2.72); the September form (5.07e11 beyond 71 kpc) is 2.7 sigma below DESI at 80 kpc |
| 38a | Milky Way mass at 73 kpc: 5.23 / 5.71e11 (hunt item 38, 09-03) | CONSISTENT, NOT DISTINCTIVE | DESI joint 6.04 (lower error 0.45): 1.8 / 0.7 sigma below; the paper's NFW fits equally |

## 2. September ledgers (`predictions_2026/`, `hunt_2026/EXACT_EXPONENTIAL_PREDICTION_LEDGER_2026-09-03.md`)

First commits 2026-09-01 to 09-09. About 250 rows; the groups below cover every row that names a
number or direction and a data set. Superseded amendment history, formulas and pipeline settings
are not listed.

| id | prediction | class | latest record |
|---|---|---|---|
| A-1, WB-26, P15 | wide-binary gamma_v 1.1614 to 1.1814 / 1.1917 to 1.2267 | NOT YET TESTED | Gaia DR4; the adopted theory now predicts 1.000 (section 7) |
| WB-11, WB-29 | wide-binary anisotropy sign; flip at 1.96 r_M | NOT YET TESTED | `hunt_2026/h15_wide_binary_orientation.out`: DR4 will not close it |
| A-2, S3-20, ET-C4 | a0 flat to z 3; BTFR 0.00 against +0.33 dex at z 2.5 | UNDECIDED | no deep rotator sample exists; `closure_2026_11_12/AZ2_flat_a0_lya_ap/RESULT.md`: as frozen NO VERDICT |
| A-3, P9 | w = -1 | NOT YET TESTED | Rubin 2027+, DESI DR3; CFG549 (10-10): tension, not excluded |
| A-4, DE-01/04/06 | aligned asymmetry +1 to 4 per cent | UNDECIDED | +2.95 (n = 16), -1.70 +- 2.12 (n = 25); needs about 560 |
| EFE slopes | -0.1348; -0.1006 | FAILED | +0.0033 +- 0.0304 (4.5 sigma against); +0.0800 +- 0.0467 (3.9 sigma against) |
| A-5, OO-03/06 | comet anisotropy 7 / 17 per cent | UNDECIDED | -0.0268 +- 0.0389, underpowered |
| A-6, L4-19 | cluster kink | RETIRED OR WITHDRAWN | written for the retired Branch B |
| A-7 | no lensing excess of 2 to 3 out to 1 Mpc | NOT YET TESTED | Euclid shear, June 2027 |
| L4-01, P2 | KiDS fit; equal potentials | POST-DICTION | `closure_2026_11_10/THEORY_ASSEMBLED_2026-11-10.md`: fails on pooled isolated lenses (1.34 / 1.39) |
| A-8, L4-27 | BIG-SPARC slope 0 | NOT YET TESTED | sample not public |
| A-10, L4-29 to 33 | kappa = 1/2 preferred over 1/(2 pi) | POST-DICTION | `closure_2026_11_12/OUT4_kappa_window/RESULT.md`: kappa not derived (fitted) |
| B-1 to B-10, ET-A1 to A14, P1, P12, P14, P21 | retrodictions (RAR, BTFR, c_T = c, CMB) | POST-DICTION | all data public |
| TC5-03/04, L4-15/16 | cluster slope +0.938; extra mass rising outward | FAILED | -0.149; X-COP needs falling extra mass, 12 of 12, slope -0.366 +- 0.077 |
| TC4-01, ET-B1 | Cassini quadrupole | FAILED | 3.762 / 4.962 times the ceiling |
| S3-33, P19 | earlier galaxies by 1.34 to 1.96 | RETIRED OR WITHDRAWN | hunt item 73: sign wrong |
| P3, P4, P17 | a0 proportional to H(z); ceiling 0.6476 a0; 1/r term | RETIRED OR WITHDRAWN | P3 "backwards" (09-10); kernel replaced |
| WB-07 to 09, STX-01/04, D-1 to D-13 | gated gamma, solar-system dipole, CPL bump, inertia arm | RETIRED OR WITHDRAWN | the registries' own status |
| P5, P7, P8 | collisionless dust; infall share | CONSISTENT, NOT DISTINCTIVE | holds with 5.41 fitted |
| P6, P16 | no relic, decay or detection | CONSISTENT, NOT DISTINCTIVE | ongoing searches |
| P18 | fast bars | POST-DICTION | hunt item 29 |
| P20 | no starless perturber | UNDECIDED | CFG669 (10-12): not diagnostic |
| P13, ET-D1 | scalar wave mode; high-z deficit | NOT YET TESTED | LISA, ELT, 2030s |
| HUNT 1 to 125 | 125 searches on public data | POST-DICTION | self-scored within a day; the hunt's own summary: zero survivors |
| 38b | Milky Way mass stops at 5.07e11 beyond 71 kpc (hunt item 38, 09-03) | UNDECIDED | 2.7 sigma below DESI at 80 kpc; see row 32 |

## 3. Sealed, pre-registered and recent

| id | prediction | registered | class | latest record |
|---|---|---|---|---|
| KT1 (CQ2) | Gaia DR4 wide binaries Newtonian: 1.0019 / 1.0100; killed if in 1.083 to 1.23 | 11-04 | NOT YET TESTED | Gaia DR4 |
| DR4-PREREG | gamma_v 1.09; Amendment 1 changed it to 1.0004 to 1.0006 | 07-16 | NOT YET TESTED | Gaia DR4 |
| G018 | gamma_v rising to 1.047; 1.095 to 1.111 at 20 kAU | 09-13 | NOT YET TESTED | superseded by v3s, still "ARMED" in the matrix |
| KT2 | a0(z)/a0(0) = 0.913 / 0.942 / 0.909 at z 1 / 1.5 / 2.33 | 10-20 | NOT YET TESTED | no galaxy a0(z) sample exists (52 of 52 blocked) |
| KT3 | lensing mass equals dynamical mass at 310 kpc | 11-04 | POST-DICTION | KiDS-1000 (2021); weak power; KO1R not separated, KO2 no verdict |
| SP1 | lensing step 0.47 / 0.43 at log M* 11.21 | 10-27 | NOT YET TESTED | needs calibrated shear (June 2027); route retired 11-01, seal kept |
| SP2 | environment step 0.484 / 0.442 at 0.3 Mpc | 10-28 | NOT YET TESTED | as SP1 |
| PR-F4 | settled-radius change across lens redshift 0.5 | 11-11 | NOT YET TESTED | frozen, not run |
| PREREG-cf | c_f proportional to M^0.077, c_f(1e12) = 4.0 | 10-29 | CONSISTENT, NOT DISTINCTIVE | slope +0.057 (68 per cent -0.017 to +0.144) passes; level 7.74 against 4.0; the project's own simulations |
| H025 | RAR scatter grows with redshift | 09-15 | UNDECIDED | `hy4_push/H026_results.out`: not established; committed with its test |
| H044 | satellite cap sets the dispersion | 09-15 | FAILED | capped satellites observed 3.1 times above; its own header concedes it |
| PAPER66-A | U4_27928 not detected by ALMA | 11-01 | CONSISTENT, NOT DISTINCTIVE | not detected 11-06 (a sensitivity forecast); U4L1: the limit is not adverse at the plan's primary conversion, with 0.04 to 0.15 dex to spare |
| PAPER66-B | UDS28473 speed at 3 kpc: 441 / 439 km/s | 11-01 | UNDECIDED | detected; fit not constrained, nothing scored |
| condor, rest | speed differences of 1.5 and 1.9 km/s | 11-04 | NOT YET TESTED | releases 11-24, 12-04, 12-22 |
| vc875 | 245.8 against 251.6 km/s at 3.84 kpc | 11-04 | NOT YET TESTED | ALMA unit listed for 2026-11-13 19:00 EST |
| aztec159 | 374.4 / 382.2 / 443.6 km/s at 7.5 kpc | 11-04 | NOT YET TESTED | 2027-07-20, 2027-09-24 |
| EUC1-F | Euclid lens gate | 11-12 | NOT YET TESTED | per-lens source redshifts missing |
| PAPER72 | retained fraction 1 at turnaround | 11-09 | NOT YET TESTED | no such census |
| GS4_24110 | sealed ALMA requirement (CFG809) | 10-15 | NOT YET TESTED | public 2026-11-28 |

The four ALMA forecast reports say themselves that they show no demonstrated discrimination between
the framework, MOND and a halo.

## 4. Older registries (`real_research/`, `project_atomos/`, June to September)

`real_research/PREDICTIONS_100.md` holds 104 items, 72 of them matches to data that already
existed. The forward items across these files:

| item | number | class | latest record |
|---|---|---|---|
| a0(z) decline | 1.01, 0.86, 0.74 at z 1, 2, 3 | UNDECIDED | archival lanes cannot separate decline from flat; the law is prior art (Limbach+ 2008) |
| high-z BTFR offset | -7.3 per cent at z 3 | NOT YET TESTED | no clean target |
| a0(z) bump | +6 per cent at z 0.4 | RETIRED OR WITHDRAWN | `RETRACTIONS.md`: "the June falsifiable prediction ... is withdrawn" |
| external field against redshift | +36 per cent by z 3 | NOT YET TESTED | no data |
| solar-system dipole | 8.68e-10 | RETIRED OR WITHDRAWN | collapsed to 1.26e-15 under the kernel change; "NOT LIVE" |
| wide binaries (June, July) | +2 to 11 per cent; 1.05 to 1.10 | RETIRED OR WITHDRAWN | inertia arm closed 08-08; successor values untested |
| Euclid lensing RAR | deep slope 0.50 | NOT YET TESTED | June 2027 |
| saturated deflection | 0.51 / 5.08 / 16.1 arcsec | UNDECIDED | EUC1: no verdict |
| DESI DR3 matrix | w = -1 means a0 constant | NOT YET TESTED | not released |
| cluster eta(beta) slide | +0.75 | RETIRED OR WITHDRAWN | first point -0.09 +- 0.20; arm closed |
| velocity-dispersion spread | 6 to 13 per cent | RETIRED OR WITHDRAWN | repriced to 1.45 to 2.21 per cent; arm closed |
| growing neutrino | 0.032 to 0.042 eV | POST-DICTION | the anomaly pre-existed |
| gravitational-wave birefringence | zero | CONSISTENT, NOT DISTINCTIVE | same as general relativity |
| lightest neutrino | 2.24 meV, sum 0.0613 eV | CONSISTENT, NOT DISTINCTIVE | passes 0.0642 by 0.0029, fails the 0.053 bound; 0.06 sigma from minimal normal ordering |
| derived mass | 5.09 +- 0.10 keV | RETIRED OR WITHDRAWN | "Never cite" |
| PMNS pre-registration | none frozen | RETIRED OR WITHDRAWN | withdrawn at commit |
| neutrino splitting ratio | 32 pi / 3 = 33.510 | NOT YET TESTED | JUNO; frozen 11-11 after the fit was seen (33.83 +- 0.92 / 33.55 +- 0.89) |

## 5. Per-model folders

| id | prediction | class | latest record |
|---|---|---|---|
| glm53 G026 E1 to E4 | slab scale 140.6 pc and exponents | NOT YET TESTED | Gaia DR4 |
| E5 | Milky Way break at 6.1 kpc | POST-DICTION | 2019 curve |
| E6, E7, gemini38 | wide-binary gamma_v 1.002 to 1.047; 1.116 / 1.135 | NOT YET TESTED | Gaia DR4 |
| E8, L180, hermes G6 | growth +2.7 per cent at z 0.3 | CONSISTENT, NOT DISTINCTIVE | DESI DR1 cannot separate it from LambdaCDM |
| E9 | forest flux +3.1 per cent at z 3 | NOT YET TESTED | three sizes quoted in its own output |
| E10 | Omega_Lambda 0.6857 | POST-DICTION | H029: mutually circular |
| G035 | dust relaxes to its target | FAILED | KILL (0.28 to 1.06) |
| G044, G049, G057-sag | RAR floor; external-field split; sag | CONSISTENT, NOT DISTINCTIVE | committed with their outputs |
| G057 table | phantom gives 0.6 to 1.3 of X-COP mass | FAILED | 0 of 12 in band |
| qwen P1 | external field 0.185 a0 | POST-DICTION | R541: not derived |
| qwen P2, P5 | capped phantom mass; cluster ratio lower at z 1 to 2 | NOT YET TESTED | none |
| qwen P3, L90, L143, L233-V5 | a0 flat at z 2.5 | UNDECIDED | 52 of 52 blocked; AZ2 no verdict as frozen |
| qwen P6 | halo slope -2 | CONSISTENT, NOT DISTINCTIVE | NFW fits too |
| Kepler-grade P1 | temperature-ratio exponent 1/2 or 1 | FAILED | G104: +0.210 +- 0.161 |
| Kepler-grade P2 to P5 | dust never negative; rank > 0.7; gas slope; collapse | FAILED | 34 of 292 bins negative; 0.542; +0.235; 0.313 dex |
| Kepler-grade P6 | dispersion-ratio spread < 0.2 dex | POST-DICTION | 0.0621 dex on published profiles the same night |
| G113 | pressure slope -1.44 | RETIRED OR WITHDRAWN | retargeted to -2.54 |
| G237 extra row | surface density 213.74 | POST-DICTION | none |
| L233-V2, gemini38 | Saturn anomaly | FAILED | L243: the same kernel exceeds the Cassini quadrupole 6.44 / 7.63 times |
| L233-V3 | gamma_v(20 kAU) = 1.750 | RETIRED OR WITHDRAWN | L240: 1.095 to 1.111 |
| L233-V1, V4 | a0 values; BTFR zero point | POST-DICTION | kappa fitted |

## 6. Closest calls (none qualifies)

- **The ALMA non-detection (PAPER66-A).** Stated 11-01, happened 11-06. A sensitivity forecast for
  an off-axis galaxy; U4L1 finds the limit allowed but tight.
- **The simulation slope (PREREG-cf).** Passes its own rule; the interval includes zero, the level
  misses by 1.9 times, and the data are the project's own zooms for a route retired on 11-01.
- **The Milky Way mass at 73 kpc (hunt item 38a).** On record 09-03 with nothing fitted; DESI came in
  0.7 to 1.8 sigma above it. The standard halo fits equally.
- **The neutrino splitting ratio (FS21).** Fits within half a sigma, but the definition was frozen
  after the fit was seen. JUNO can kill it, not certify it.
- **Flat a0(z).** Holds at one matter density in AZ2; LambdaCDM's constant dark energy gives the same.

## 7. Problems in the record

- **Gaia DR4 carries mutually exclusive registered values:** 1.09; 1.0004 to 1.0006; [1.047, 1.11];
  1.1614 to 1.1814 / 1.1917 to 1.2267; and Newtonian for the adopted theory (Arm C, 09-27; KT1,
  11-04). A Newtonian result matches the adopted arm, which is not separable from Newton, so DR4 can
  kill the adopted theory but cannot confirm it distinctively.
- **The matrix's status column is stale:** row 1 is still ARMED on superseded values; rows 11, 13,
  17, 25 and 27 rest on inputs the 09-25 audit found to be artefacts; "zero unexplained fires" rests
  on rows 11 and 17.
- **Several pre-registrations were committed with their results:** H025 with H026; G044, G049 and
  the G057 sag; the Kepler-grade cluster predictions were tested 21 to 46 minutes after commit on
  files used the day before.
- **`deepseek_push/PREDICTIONS.md` calls E1 to E10 pre-registered;** G026's own output says they must
  not be represented as registered.
- **SP1 and SP2 have a polarity conflict** between their frozen rejection rule and SP1's README;
  unrepaired.
- **KT2 is not single-valued:** 0.909 in CFG689, 1.320 from the new Lyman-alpha pair in AZ2.
- **`closure_2026_11_07/predictions_check.py` checks literals against sources, not outcomes.**
- **Two of four "measured" pressure slopes in `deepseek_push/Z06_tsz_pull.out` are the synthetic
  predicted profile.**

## 8. Next dated tests

| date | test |
|---|---|
| 2026-11-13 19:00 EST | ALMA unit for vc875 |
| 2026-11-24 | ALMA, UDS16442 |
| 2026-11-28 | ALMA, GS4_24110 (sealed plan CFG809) |
| 2026-12-02 | Gaia DR4 (wide binaries, vertical structure, local density) |
| 2026-12-04, 2026-12-22 | ALMA, remaining condor units |
| June 2027 | Euclid calibrated shear (SP1, SP2, lensing RAR) |
| 2027 | DESI DR3; JUNO |

## Method and limits

- Section 1 was read by the lead. Sections 2 to 5 were read by four parallel readers, each told to
  prefer the latest dated record over a registry's own status line, and their reports were merged
  here. Rows 38a and 38b and the PAPER66-A update come from this session's lanes (DR2REV, NMB1,
  PLT1, U4L1).
- Checked by the lead against the cited files: the anisotropy result (G206); the Bilek timing; the
  a0 bump retraction; AZ2's label; the neutrino sum; the ALMA limit and requirement; the simulation
  slope; G035; the five Kepler-grade cluster numbers; the X-COP falling slope; the Cassini ratios;
  the external-field slopes; the vc875 date; FS21's value. Everything else is as the readers
  reported it, with the paths they gave.
- "None found" for a scoring lane means the readers' searches found none; the searches were not
  exhaustive.
- Not covered: the neutrino follow-ups kept in a local repository with no remote; registries inside
  archived snapshots.
