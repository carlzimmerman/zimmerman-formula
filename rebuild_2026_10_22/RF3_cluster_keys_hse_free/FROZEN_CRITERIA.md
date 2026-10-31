# RF3_cluster_keys_hse_free: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question (THEORY_PROGRESS_SUMMARY_2026-10-31 §4).** With comparison masses taken from caustics and weak lensing, not hydrostatic equilibrium, the baryon fraction from the framework's Ω_c/Ω_b, the measured gas, and the grader on one template: what is the cluster excess, and do route E's 15 keys still need external c_f? Added by the owner's relay: grade ZN3's native z = 0 rule beside native c_f and external c_f 4, and report whether ZN3's pass survives without hydrostatic masses.

**Disclosed before the freeze.** I have read ZN3's result (15 of 15 and X-COP pass at both f★ on X-COP's gas scale; fails on eRASS1's gas and with budget M₂₀₀), BA2's and NZ1's restated tables, and which rows of Groener+2016 and HeCS exist for the X-COP clusters: caustic masses for A85, ZW1215, A2142 (A2255 outside the 7), weak lensing for A2142 only, and their M₂₀₀ values for those. No model has been evaluated at any of those radii. From a sparse scan of the KiDS catalogue: its northern edge is Dec +2.97, and ZW1215 sits at Dec +3.66.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. c_f 4 is EXTERNAL. No downloads. Not "theory closed". Nothing here says the data favour the framework. A verdict that flips because an outside input left is reported as "not a framework failure", never as "the framework passes".

## (a) Grader: already fixed, cited, not redone
`NZ1_zoom_core_radius/nz1_one_template.py` (b62559a575) and `BA2_one_template_reread/README.md` (0d72e260d8) restate X73, GS1, MA1, FC1, NZ1 on one template; ZN1 and ZN3 grade on one template from the start. This lane uses the same fix: G-OUT-Mall and G-OUT-M1..M3 read the run's own A, s scaled by A/meas. No other lane's file is edited.

## Rules graded
| label | rule | c_f class |
|---|---|---|
| ZN3 | ZN3's shapes (`zn3_shapes.json`), `zn3_grade.py` worker, mode fs: fair share inside R₂₀₀, no fitted parameter, no a₀ in the halo | no c_f |
| NAT | X74's script, table `X77_direct_core_surface_density/A4_x77_native_table.json` (X77's smooth-core fit to the zooms, all ng 64), FC1_MODE none | NATIVE |
| C4 | X74's script, c_f = 4 (X73 PRIMARY) | EXTERNAL |

All at X73's measured slope 2.7774 to r_ta, native Ω_c/Ω_b.

## Gas (c)
- **E:** eRASS1's own Mgas500.
- **X:** X-COP's scale, SM1's +0.111 dex, as ZN1 applies it.
- **XF (HSE-free scale):** SM1's +0.111 compares each survey's mass at its own R500, and X-COP's R500 is hydrostatic. XF is the median, over SM1's 5 matches, of log₁₀[M_gas,X-COP(< R500,eRASS)/Mgas500,eRASS], read from X-COP's gas profile at eRASS1's radius. No X-COP R500 enters. Graded on ZN3 only, at f★ 0.034 and 0.0615.

## f★ (d): a band, not two fixed values
Light as measured, the Υ range stated:
| f★ | origin |
|---|---|
| 0.024 | CFG408's census 0.034 × 0.7 (Υ low side) |
| 0.034 | CFG408/CFG922 A1 central |
| 0.0615 | X-COP-7 median, Ghizzardi+20 profiles on disk |
| 0.136 | 0.0615 × 1.7 (Chabrier to Salpeter) × 1.3 (ICL allowance) |

The factors 0.7, 1.7, 1.3 are LITERATURE-INPUT from memory, PROVISIONAL. No ICL table is on disk (CFG922: NOT TESTABLE). Stars follow the gas in the model, as X73.

Jobs: ZN3, NAT, C4 × {E, X} × 4 f★, plus ZN3 × XF × {0.034, 0.0615}: 26 grader runs. One thread, nice 15, at most three at once.

## Excess (Z band per footing)
Z_MID = (A − 1)/s on `KT_all|MID`, and Z_IN likewise on `M_all|INNER` with s_IN, for each gas, f★, h, footing. A is data over the law's template, so this needs no rule. Reported as a band per footing over the graded f★, per gas scale. X11's quoted STAT Z (5.21 / 5.47, 4.47 / 4.74, X7's f★ 0.20 template, eRASS1's gas) is the comparator.

## Keys
15 keys, h 0.672 and 0.686, |Z| ≤ 2, one template. Per rule × gas × footing × f★: number passing, worst key, sign (OVER if pred > meas). "Need external c_f" is answered as: **NAT passes at f★ X** or **only C4 passes at f★ X** or **neither**, per footing and gas.

## Comparison masses (b)
**Classes.** Published WL M₂₀₀ here are NFW fits, and caustic masses rest on an F_β calibrated on ΛCDM N-body runs. By the summary's rule 1 they are ΛCDM-PROCESSED: **labelled brackets, never the graded value.** Hydrostatic masses are a labelled bracket too. The ledger classes each.

**Source.** Groener+2016 table (`real_research/data/groener2016_cluster_concentrations.tsv`): M200 with its published ±, Ω_m and h columns; HeCS Table 4 (`deepseek_push/G203_data/hecs2013_table4.tsv`), h = 1 units as its r200 and M200 imply.
- Groener rows with blank h: treat as h = 0.7 (primary), h = 1 reported beside it. That is Rines & Diaferio 2006's caustic rows, whose h isn't stated in what's on disk.
- Rows without a usable M200 are dropped and counted.

**Two samples.**
1. **X-COP-7** (the X-COP gate's clusters): by name.
2. **eRASS1 match:** Groener and HeCS rows within 3′ and |Δz| < 0.01 of an eRASS1 cluster with finite Mgas500, R500, z ≤ 0.6. The rule is applied at that cluster's own Mgas500, R500 and z. This reaches HSE-free masses that X-COP lacks; these aren't X-COP's clusters. Gas E and X both, with no distance-convention correction (`qd`) for these clusters, stated as a limit.

**Statistic.** Convert M and r to h = 0.7 (M, r ∝ 1/h); r from M at 200 ρ_c(z) in the row's cosmology. Δ = log₁₀[M_pub/(M_b + M_h)] at r, Δ > 0 the model too light, M_b and M_h from the grader's own functions for that rule, gas, f★. For each method (CM caustic, WL, WL+SL, LOSVD, X-ray): N, median Δ, mean Δ, SE (rms/√N; when N < 3, propagate published errors, or quote "no error" if none). Per cluster medians, so one cluster with many rows counts once. Also, model-free: log₁₀(M_pub/M_FORW) at r for X-COP-7 where r is inside the hydro profile.

**Bracket reading, frozen.** Per rule, gas, method:
- **AT THE LINE:** |median Δ| ≤ 0.05 (X-COP's own line) with SE ≤ 0.05.
- **OFF THE LINE:** |median Δ| − 2 SE > 0.05, sign named.
- **NOT RESOLVED:** otherwise.

## RAW test
KiDS DR4 gold shear is RAW. Data-only check for each X-COP cluster with files on disk (12): the catalogue's coverage near its centre, as distance from the centre to the nearest source in a sparse scan of at least 200 000 sources, in units of R₂₀₀ (Ettori+19). If no X-COP cluster has sources inside 1 R₂₀₀, no raw X-COP shear exists on disk and no shear is measured here. Otherwise the lane stops and asks for an amendment before measuring.

## Verdicts
1. **Grader:** cited only.
2. **Z band** per footing, gas.
3. **c_f:** per footing and gas, as under Keys.
4. **ZN3 HSE-free, one of:**
   - **ZN3 KEYS SURVIVE ON THE HSE-FREE GAS SCALE:** XF gives 15 of 15 at both f★. **FAILS ON THE HSE-FREE GAS SCALE, keys named,** otherwise. The keys are raw shear, so this part is clean except for XF's measured gas.
   - **X-COP GATE WITHOUT HSE:** "UNDETERMINED: no clean HSE-free X-COP mass on disk" if the RAW test finds nothing and only ΛCDM-PROCESSED rows exist, with the bracket readings beside it and the list of what is needed. No bracket can turn this into a pass or a fail.
   - **[F★-BAND-DEPENDENT]** if ZN3's X-scale class changes across 0.024–0.136.
5. **No 5.364:** a grep of this lane's scripts, and of the patched text at run time, must show the Planck ratio absent as a live value: assert `NAT_RRAT` ≠ 5.364 at every run and report it.

## Checks
- **K1 ZN3:** X scale, f★ 0.034 and 0.0615; E scale, f★ 0.034: predictions and X-COP mean, rms match `zn3_results.json`, |d| ≤ 1e-9.
- **K2 C4:** f★ 0.034, 0.0615, E: predictions match X73's committed JSON, |d| ≤ 1e-9; one-template G-OUT-M3 Z at h 0.672 matches BA2's +1.04, +0.73 within 0.005.
- **K3 NAT:** f★ 0.034, 0.0615, E: predictions match `X77…/A4grade_x74_results_*`, |d| ≤ 1e-9.
- **K4:** M_h function agrees with the grader's X-COP rows at x 0.1–0.7, |d log M| ≤ 1e-6.
- **K5:** M_b at X-COP rows against the measured gas + stars: reported, with the median ratio, since M_b for comparison masses comes from the grader's model and not from the measured profile. If it differs by more than 0.05 dex in median at r ≥ R500, the X-COP-7 rows are also quoted with measured M_b.
- **MUTATE (`RF3_MUTATE=1`, separate outputs):** ZN3 shape r × 1.5 (ZN1_RX), f★ 0.034, X scale; every M_pub × 2. K1's agreement must fail; Δ must move by more than 0.25 at every method; G-IN-Mall by more than 0.05. Else lane UNDECIDED.
- Any K failure: no verdict, exit 1.

## Limits fixed now
ZN3 stays chosen after ZN1, at ng 64, collisionless, with its thin outer shell. Published M₂₀₀ extrapolates or interpolates NFW to r₂₀₀. Caustic errors aren't tabulated in Groener. eRASS1's M500 and R500 are weak-lensing calibrated inside a ΛCDM cluster-count pipeline, which sets the keys' bins and R500. That input is labelled, not removed: no clean replacement exists on disk.
