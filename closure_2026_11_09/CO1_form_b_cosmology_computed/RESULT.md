# CO1 RESULT: form B's cosmology rows, computed instead of carried

**ROWS HOLD / ROWS HOLD (canonical / alt), with an inherited halo list.** Read with mutation arm M4 as the criteria froze it,
which did not bite, the label is NO VERDICT / NO VERDICT; the label above rests on AMENDMENT A1, committed before any graded
number. Both readings are part of this result.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Kappa = 1/2 FITTED; not theory closed. Footings
graded separately, never pooled. Cold dark energy; no particle. Criteria 020522140a; amendment A1 5e1496298d.
This is not a pass for form B: its open items 1 to 7 stand, and nothing here says the data favour the framework.

## What was asked and what came out

The owner's decision of 2026-11-09 lists form B's cosmology rows as carried from the cold reference, with the 1-halo
redistribution not evaluated (open item 8). Here they are computed for form B itself.

1. **The primary CMB, CMB lensing and the growth rate hold when computed.** Form B's linear content (baryons, the cold
   component, a vacuum term, GR; under B the law is not a force) is fitted to raw Planck PR4 and ACT DR6 spectra and then
   checked against PR4 lensing bandpowers and DESI DR1 f sigma8.
2. **The 1-halo redistribution does not move those rows.** Laying the cold component out as the law's phantom, for the
   layout frozen in the criteria, changes the matter power by 0.6 / 1.0 % at k = 1 h/Mpc. PR4 lensing moves by 3e-5 / 5e-5.
   Raw KiDS-1000 cannot see it (d_cold +1.15 / +2.21; a refit of form B's own prediction with the cold reference costs
   chi^2 1.0 / 1.2).
3. **That holds only because a group's or cluster's share is counted inside R200c.** If a cluster held the whole dust of
   its turnaround sphere, as galaxies do in ONE1's rule, the power at k = 1 would be 2.9 times higher and raw KiDS would
   reject it by chi^2 +1450 / +1547. So form B's cosmology needs the cluster share tied to the baryons present (5.41 times
   them), not the Lagrangian share. Galaxies can keep the Lagrangian share: they carry too little of the power to matter.
4. **The amplitude is not solved.** The fit's own sigma8 is 0.8405 / 0.8429 (tau is free: the fit has no low-L data). PR4
   lensing reads 0.9617 / 0.9564 of the predicted amplitude (-1.66 / -1.89 sigma; inside the line, close on alt). Raw KiDS
   fits the record's S0 run at sigma8 0.811 with p 0.014, and form B at the fit's own amplitude with p 0.0015 / 0.0009
   (bracket, crude scaling). The redistribution does not relieve this; it makes it slightly worse.

## The table (co1.json, co1.out)

| row | canonical | alt | line |
|---|---|---|---|
| **C1** primary CMB, PA chi^2 - chi2_cal | -65.21 (3740.16) **PASS** | -65.07 (3740.30) **PASS** | <= 9 |
| cold / baryon at that fit (fitted, not derived) | 5.410 | 5.412 | reported |
| **C2** PR4 lensing amplitude, data / prediction | 0.9617 +- 0.0231 (-1.66 sigma) | 0.9564 +- 0.0230 (-1.89 sigma) | within 2 sigma |
| **C2** PR4 lensing shape chi^2, 9 bandpowers | 8.56 **PASS** | 8.56 **PASS** | <= 18.48 |
| chi^2 at A = 1 | 11.30 | 12.14 | reported |
| **C3** DESI DR1 f sigma8, chi^2 ShapeFit / + BAO (4 bins) | 2.23 / 2.20, largest pull 1.22 **PASS** | 2.29 / 2.23, 1.23 **PASS** | every pull <= 2 |
| sigma8 at that fit (S0 engine: 0.811) | 0.8405 | 0.8429 | reported |
| R_cold at k = 1 / 3 / 5 h/Mpc | 1.006 / 1.051 / 1.090 | 1.010 / 1.088 / 1.159 | reported |
| **C4** PR4 lensing with the redistribution, r_eff - 1 | +0.00003 **PASS** | +0.00005 **PASS** | within 0.0481 |
| **C5** raw KiDS-1000, d_cold (104 points) | +1.15 **CONSISTENT** | +2.21 **CONSISTENT** | klass |
| robust: widen2 / noIA / fade / DESI | +0.55 / +1.99 / +0.88 / +0.72 | +1.15 / +3.70 / +1.65 / +1.44 | all < 9 |
| tooth: chi^2_min (null) | 1.01 (1.11) NOT VISIBLE | 1.15 (1.11) NOT VISIBLE | >= 9 visible |
| KiDS chi^2: S0 / S0 x R_bar / S0 x R_tot | 144.26 / 143.80 / 144.95 | 144.26 / 143.81 / 146.01 | reported |
| p of the same | 0.014 / 0.015 / 0.013 | 0.014 / 0.015 / 0.012 | reported |
| DES Y3 d_cold (52 points) | -0.01 | -0.02 | reported |

- C1 is a re-run. F1A's stored best fits replay to 1e-8 / 5e-6 (KA6). chi2_cal (3805.37) is the likelihood package's own
  test point with its nuisances profiled the same way; it is a yardstick for adequacy and not a framework quantity.
- R_tot, the whole layout against S0, is 1.003 / 1.008 at k = 1. R_bar, the baryons alone (gas in a beta model instead of
  tracing the cold component), is 0.9975 at k = 1 and 0.978 / 0.979 at k = 3.
- The sigma8 ratio of the redistribution is 1.0003 / 1.0005.

## Why the redistribution is small, and when it is not

- **Groups and clusters carry the power at k below about 3 h/Mpc**, and the frozen rule keeps their mass inside R200c
  unchanged: f_core 0.08 to 0.48 of the share stays in the reference's own NFW, and the phantom reaches its cap at 0.62 to
  0.81 R200c. Inside R200c the layout holds 0.70 to 0.76 of the reference's mass at 0.1 R200c and 1.03 to 1.24 at 0.7 R200c.
  At k = 1 their 1-halo terms add 0.004 / 0.008 to R.
- **Galaxies (below M200c 4.4e12 / 5.8e12 Msun/h) hold their whole turnaround dust inside 0.25 to 0.5 r_ta.** That drains
  their infall regions, but the decade below M_ta 1e13 adds only +0.0007 / +0.0009 to R at k = 1 and +0.014 / +0.017 at k = 3.
- **The scope decides everything (M4, and the bracket row below).** With the cluster rule in the Lagrangian scope R_tot is
  2.94 / 2.97 at k = 1 and raw KiDS reads d_cold +1449.8 / +1547.0. CFG556 and CFG596 found the same mechanism for
  candidate B (halo model +0.72 / +0.88 at k = 1; PM run +68.7 on raw KiDS). Form B escapes it through the 5.41 M_b,sys
  rule of PD1 A2, which RB1 is grading on the hot systems.

## Brackets (reported, never graded)

| bracket | R_cold at k = 1 (can / alt) | R_cold at k = 3 | KiDS d_cold |
|---|---|---|---|
| core prefactor 1 | 1.005 / 1.007 | 1.063 / 1.080 | +1.48 / +2.00 |
| core prefactor 0 (the whole share as phantom) | 0.946 / 0.961 | 0.780 / 0.839 | -2.85 / -2.81 |
| regime boundary at M200m 1e13 | 1.007 / 1.011 | 1.060 / 1.095 | +1.40 / +2.43 |
| galaxy rule in the virial scope | 1.004 / 1.008 | 1.034 / 1.060 | +0.75 / +1.44 |
| gas core 0.2 R200c | 1.004 / 1.008 | 1.034 / 1.069 | +0.67 / +1.53 |
| Press-Schechter mass function, Mo-White bias | 1.007 / 1.011 | 1.060 / 1.093 | +1.44 / +2.48 |
| c(M) x 0.7 | 1.010 / 1.014 | 1.093 / 1.133 | +2.51 / +4.00 |
| c(M) x 1.3 | 1.003 / 1.007 | 1.022 / 1.055 | +0.47 / +1.26 |
| CFG556's kernel 1 / (1 - exp(-sqrt y)) | 1.006 / 1.010 | 1.050 / 1.087 | +1.12 / +2.18 |
| cluster rule in the Lagrangian scope (M4) | 2.95 / 2.98 (R_tot over the primary R_bar) | | +1449.8 / +1547.0 |

- Every bracket but the scope stays between -2.9 and +4.0. The alt value for c(M) x 0.7 is +3.997, at the TENSION line.
- On PR4 lensing every bracket moves r_eff by at most 0.00016.
- **KiDS amplitude bracket (frozen):** the S0 spectrum scaled by (sigma8 / 0.811)^2 gives chi^2 162.04 (p 0.0015) /
  165.18 (p 0.0009) for form B, d_cold +1.75 / +3.36. A constant factor understates how the nonlinear spectrum responds to
  amplitude, so the real fit would be worse.
- **Post hoc, added after C2's amplitude was seen (reported only):** with the amplitude PR4 lensing measures (sigma8
  0.8243) the same row gives 152.07 (p 0.0055) / 153.37 (p 0.0047).

## Known answers and MUTATE

- KA1: CFG556's committed primary table reproduced exactly (R at k 1: 1.7160 / 1.8852; sigma8 ratio 1.0402 / 1.0463).
- KA2: both nulls give 0 exactly. They are weak: the two code paths are the same expressions.
- KA3: every layout and bracket conserves M_ta to 5e-16 and is non-decreasing.
- KA4: CFG596's S0 rows reproduced (KiDS 104 points, 144.26; DES 52, 68.64).
- KA5: the record's PR4 reference row, 8.5709 and 1.0210294 against 8.5708 and 1.0210287.
- KA6: C1's replays, above. KA7: exact. Limber check: a constant boost to 6e-15; absolute X_L against CLASS within 0.0004.
- **M1 bites:** candidate B's halo-model R(k) against S0 on KiDS gives +131.85 / +196.82 (DES +13.3 / +16.3).
- **M2 bites:** a flat 1.10 gives r_eff 1.0666 against the line 0.0481.
- **M3 bites:** F1A's baryons-only fit replays at Delta_cal +172,850 / +166,609.
- **M4 did not bite as frozen** (-0.051 / -0.044: the comparison layout moved with the mutation). Restated in A1 before any
  graded number, it bites (2.946 / 2.982 against 1.006 / 1.010).
- Reported check, written after the halo-model part ran (`co1_check_layout.py`): r_M, r_t, v_vir, f_core and the cap radius
  recomputed in SI, and the cold component's transform by direct quadrature, agree with the layout code to 1.5e-6.
- `co1_hm.py` was run twice; the second run's JSON is byte-identical to the first (md5 88483291444683b8950400f48622dcfd).

## Hand estimate against the outcome

Written in the criteria before any code: |R_cold - 1| below about 0.1 at k <= 1 (found 0.006 / 0.010); C4 PASS with
|r_eff - 1| below 0.01 (found 0.00003 / 0.00005); C5 CONSISTENT or TENSION (found CONSISTENT). The sign of d_cold was not
predicted. My M4 expectation was wrong as written.

## Inherited ingredients and limits

- **The halo list is not framework-native:** Tinker 2008 mass function, Tinker 2010 bias, Duffy 2008 c(M), and CFG556's
  declared baryon shapes (Moster 2013 stars, beta-model gas). They enter only the ratio R; the base spectrum is the record's
  own S0 PM run. They describe collisionless matter under Newtonian gravity, which is form B's stated dynamics. Swapping
  the mass function or moving c(M) by 30 % changes d_cold by less than 2.
- **The layout is put in by hand** (open item 1). This lane grades what the layout does to the spectrum. It does not show
  that the cold component takes that layout.
- The ratios are computed at z = 0 and held in z ("fade" is the bracket). a0 is constant.
- C5 keeps 104 of 225 published KiDS points (the S0 run's k range). S0 is gravity-only: nothing here ejects gas beyond
  R200c.
- C1 has no low-L polarisation data, so tau (0.070 / 0.073) and A_s are weakly held; C2's amplitude and the sigma8 rows
  carry that.
- DESI's fiducial f sigma8 (the unit of its published ratios) was computed from parameters transcribed from memory.
- The cold amount (5.41 times the baryons) is fitted from the acoustic peaks. A cold component of that amount gives the
  cold-component spectra; C1 to C3 holding is not independent evidence for the framework.
- Not recomputed: the Lyman-alpha forest row (stays carried), CMB lensing above L 400, the alt footing's own PM run.

## Files

- `FROZEN_CRITERIA.md` (020522140a), `AMENDMENT_A1.md` (5e1496298d).
- `co1_hm.py` -> `co1_hm.json`, `co1_hm.out`: the layouts and ratios (79 s).
- `co1_linear.py` -> `co1_linear.json`, `co1_linear.out`: C1 to C4 (16 s, 0.81 GB).
- `co1_shear.py` -> `co1_shear.json`, `co1_shear.out`: C5 (272 s).
- `co1_grade.py` -> `co1.json`, `co1.out`: the table and labels.
- `co1_check_layout.py` -> `co1_check_layout.out`: the SI and closed-form check.
- Read-only: CFG556 and CFG592's library parts, CFG596's S0 run, F1A's likelihood and stored fits, QX3 iter2's PR4 loader,
  PD1's share table. Nothing downloaded; nothing written outside this folder.
