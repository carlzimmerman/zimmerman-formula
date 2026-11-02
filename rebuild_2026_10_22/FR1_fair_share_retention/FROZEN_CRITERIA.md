# FR1_fair_share_retention: FROZEN CRITERIA (committed alone, before any script or number from this lane)

**Not blind.** HM1's requirement (cold/baryon at R200 7.4 to 9 against fair share, M3 gas low +4.61, high +1.81), LF1, HL1, HL2, GS4, OP2 and M3A1 are on record, and I've read them, including HL1/HL2's log Y at R500 on a few samples. The published trend of f_gas with mass is general knowledge. Idea from HM1's own note (post-result there). FG1's frozen verdict is untouched; route E's cold sector is retired by the owner (1996555bf2), and nothing here can reinstate it. Galaxies stay as they are: no SPARC, Local Group or weighing row is regraded, so nothing here can say route E passes. kappa = 1/2 FITTED, unused. Cold dark energy, never a particle. No a0 in the cold sector. Not theory closed.

## Question
Clusters and groups may not hold the cosmic baryon share inside R200, and hold less at low mass. Does gas-fraction data with mass independent of the G-OUT shear show this, with the size and trend the keys need? Does that one measured line, with no new knob, close the 15 keys and keep X-COP on ZN4's native profile?

## Rule
Fair share: Y = 1 at R200 reproduces ZN4. Here M200 = (1 + R_nat) M_b(<R200) / f_ret, R_nat = NAT_RRAT = 5.2715 (native; never 5.364). Baryons as measured: gas with GS1's tail, s 2.7774, stars (1 + f*), the grader's own. M200 is total: **cold in R200 = M200 - M_b(<R200) = M200 (1 - f_ret/(1 + R_nat))**. Shape: ZN4's, tail closing at Mfair at r_ta unchanged.

f_ret(R200) = Y500(M500) x carry. Y500 is the measured line. **Carry, named:** carry = [M_b(<R200)/M_b(<R500)] / [M200/M500], cluster by cluster: gas from the grader's profile with **GS1's slope, measured on X-COP clusters only, massive only, extrapolated to lighter clusters without evidence**; M200/M500 from ZN4's shape at z 0.25 (m(x)/x^3 = 2.5 for x500, interpolated in lg M between 1e14 and 1e15, clamped). Algebraically this makes the rule M500 = (1 + R_nat) M_b(<R500)/Y500(M500) at the model's own R500, solved on the grader's radial grid, outermost crossing, as `zn1_m200_fs`. Report median Y200 and carry on M3 and X-COP, and closure: model's own M_b/M at its R500 against the line.

## Estimator: Y500(M500), FITTED to these data, not to any key
Y500 = (1 + f*) (1 + R_nat) M_gas500 / M500. Each row at its own published R500 with its own mass. Rows at h 0.70: M_gas ~ h^-2.5, M ~ h^-1 from each catalogue's stated h. In the grader, per background: lg Y500 + 1.5 lg(0.7/h), lg M500 + lg(0.7/h), as the grader itself rescales gas and lengths. Not at both f* a new fit: f* enters as (1 + f*) only.

Form: **lg Y500 = a + b (lg M500 - 14.5)**, straight line, OLS of lg Y on lg M, one point per cluster. Errors: 2000 cluster bootstraps, seed 20261101. No cap at Y = 1.

- **Line H, PRIMARY:** hydrostatic masses, same method as X-COP's: Lovisari+20 (Planck SZ-selected), Lovisari+15, Sun+09, Landry+13, from `../GS4_pointed_gas_offset/gs4_inputs.csv`. Duplicates by position within 6 arcmin and |dz| <= 0.02: median of lg M and lg Mgas. **All 12 X-COP clusters are removed by position from the line,** so it's derived without X-COP and tested on it.
- **Line W, reported, can set a tag:** masses from lensing, or from T calibrated on lensing: Mahdavi+13 M_WL and Mgas at its r500_WL; Zhang+10; Okabe+Martino (M_WL, its Mgas at Martino's own r500, disclosed mismatch; a row used only if Mgas is finite); Eckert+16 XXL. By name within HL2's sets (HL2's parser), Eckert has no overlap. X-COP removed by name.
- **Line H+g, reported:** H with M500 x 10^(+0.031), HL2's post-result bracket. X-COP not moved.
- **Line HG, reported:** lg Y on lg M_gas500 (H sample), mapped by the same rule. Mass noise then sits in y only, and the keys' bins are cut on gas, so this is the right conditional for them, and a check of the mass-noise bias on H's slope.
- Y_X-based masses (Croston, Maughan, Vikhlinin) carry gas in the mass: **excluded,** slope reported only. eRASS1's M500 and any mass from the keys or KiDS shear: **forbidden** (circular), including M_WL from lanes reading KiDS.

Binned medians in lg M500 13-13.5, 13.5-14, 14-14.5, 14.5-15, >15 reported against the line.

**Not double counting GS4.** GS4 compares two surveys' M_gas at one radius; +0.005 stays on eRASS1's gas, the line is M_gas/M at fixed M. Different statements. Line's M_gas are pointed, GS4's overlap is only that it says these pointed values and eRASS1's agree at a radius. LF1 is the keys' shear and is not used. Reported, not used for the line.

**Circularity stated.** X-COP's test uses hydrostatic masses, and line H is hydrostatic, so method bias is shared: a pass there isn't independent support for hydrostatic masses. It's independent in clusters only. Mass-noise bias: scatter in M500 drives Y-on-M slope negative, against this lane; HG reports it. Selection: pointed low-mass samples are X-ray bright, likely gas-rich: Y low-mass is if anything high. Group star fractions larger than f* aren't on disk, which makes Y low-mass low: both reported, neither applied.

## Runs, ZN3's grader via `--worker` (as OP2's ng 80 driver), ZN4's shapes, X74/CE1 tables, own temp dir
Gas +0.005 (GS4), both f*, both h: fair share (K1); **H, primary**; H line a +1 sigma, -1 sigma at M3's lg M500 (error row); W; H+g; HG; H without any one catalogue (L20; L15+S09); MUTATE slope sign flip about lg M 14.5. Reported at +0.111 only as a scale the data don't support: H. All read: 15 keys, G-OUT-M3, X-COP mean and rms, joint chi^2 by BA1's line with M3A1's R, Z_tot on G-OUT-M3 by M3A1's quadrature (M3A1's R and error terms from the f 0 row; disclosed). Line's own error added to Z_tot in quadrature from the +/-1 sigma rows, reported.

## Pass lines (the record's)
15 keys |Z| <= 2 at both f*, both h on +0.005; X-COP |mean| <= 0.05, rms <= 0.10. Reach = (Z_base - Z)/(Z_base - 2) on G-OUT-M3, base ZN4 +4.41, +4.07, +4.13, +3.81 by cell.

## Labels, on primary H, gas +0.005
1. **NO INDEPENDENT MEASUREMENT**: SE of the line at M3's lg M500 over 0.04 dex, or fewer than 15 clusters below lg M500 14.3.
2. **RETENTION CLOSES CLUSTERS**: 15 of 15 in all four cells and X-COP passes at both f*.
3. **PARTLY**: reach >= 1/3 in all four cells.
4. **NOT RETENTION**: reach < 1/3 in any cell, or b <= 0 is within 1 SE (no trend in the needed direction).
Tags: [X-COP LOST] if X-COP fails at either f*. [MASS-METHOD-DEPENDENT] if line W takes a different label. [HG-DEPENDENT] if line HG does. [ERROR-DEPENDENT] if the -1 or +1 sigma line does.

M3's lg M500 for the label: the model's median at the primary row, printed.

## Read-across, report only, no grade
1. Line continued to lg M500 12-13 against EM1's line: lg M200 cold = 11.18 + 0.90 (lg M_b - 10), expressed as Y at R200; does the same line approach EM1, or break in groups? Binned L15/S09 at the bottom.
2. What it implies outside R200: missing baryons (1 - Y200) f_b M200 on M3, against the gas already in the grader's tail to r_ta. Whether X-COP's gas beyond R500, PSZ2's Y5R500, or any stacked SZ on disk rules it out. If nothing on disk reaches M3's mass there, say so. No new download.

## Checks
K1 f_ret = 1 through this path reproduces ZN4's +0.005 rows, per key, per X-COP, |d| <= 1e-6 at both f*. K2 line parser: row count, X-COP rows removed, one point per cluster; a synthetic injected line recovered. K3 solver: for a test cluster, Y from the solved M500 equals the line within 1e-3. K4 closure: model's M_b/M at R500 against the line on M3, reported, tolerance 0.03 dex; over: no verdict. MUTATE slope sign flip: must bite. Failed check: no verdict. A win gets the leave-out rows, the error rows, and a by-hand check against HM1's rate (2.56 of pred per unit M_c/Mfair).

## Expectation on record
PARTLY 55 %, NOT RETENTION 25 %, NO INDEPENDENT MEASUREMENT 10 %, CLOSES 10 %. Y500 near M3 about -0.12 at h 0.7 and less after the h rescale; slope positive near 0.1. The h rescale and the carry both eat some of it. X-COP stays passing 70 %.
