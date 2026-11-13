# ALP1R RESULT: the crossing-speed joint on the ALPAKA I ring curves (blind build, then compared with ALP1)

**Blind label, unchanged (RESULT_BLIND.md, edd13ab6bf): NO VERDICT (TW-N and TW-D do not bite) / NO VERDICT (TW-N and TW-D
do not bite) (canonical / alt), as frozen.** The reading under it is: ABOVE v*(z) NO POWER, BELOW v*(z) NO POWER on both
footings, FRAGILE (with R_e x 1.5 the ABOVE word becomes NO VERDICT, shape fits nothing).

TEST lane. Adopts nothing, relabels nothing, registers nothing.

- READING 8d3b72f35f; script and outputs 5feaf7b5a3; RESULT_BLIND edd13ab6bf.
- ALP1's folder and DSC1's RESULT.md were opened only after edd13ab6bf.

## Comparison with ALP1 (its RESULT.md: criteria b0e1ea1287, outputs 05c2584f62)

**Labels.**

| | ALP1 | ALP1R |
|---|---|---|
| ABOVE, can / alt | NO POWER / NO POWER, FRAGILE (can: MEAS, R_e x 1.5; alt: R_e x 1.5) | **NO VERDICT** (twins do not bite) / same; reading NO POWER, FRAGILE (R_e x 1.5) |
| BELOW, can / alt | NO POWER / NO POWER (can FRAGILE: R_e x 1.5 gives LAW FAILS BELOW) | NO POWER / NO POWER (not fragile) |
| shape-only test | [0, 6] everywhere: does not speak | [0, 6] everywhere: does not speak |
| twins | both bite | neither bites |

Under the twin gate, the two builds read the same: the rings cannot weigh the reference halo on either side of v*(z).
- **Same in both:**
  - The baryons overshoot the discs above v*.
  - Shape is silent.
  - R_e x 1.5 is the bracket that turns ABOVE into NO VERDICT (shape fits nothing): A about 3.2 / 3.5, with A = 0 excluded and every shape line failing.
- **Different:**
  - The frozen word: NO VERDICT here, NO POWER in ALP1.
  - ALP1's canonical MEAS flip to FAILS, which does not happen here.

**Cause of the label difference (twins).**
- **This lane's twin tests are frozen on the GATING test of the ABOVE group.** The above discs sit at the baryon floor (median -0.33 / -0.40 dex), so the gating test is the shape-only test. That test has no A-information: chi2(2) - chi2(0) = 4.9 against 4 s2 = 34.5. So TW-N cannot bite, and TW-D moves the edge of [0, 6] only to 4.47 / 4.96.
- **ALP1 grades the amplitude test and bites its twins there:**
  - TW-D halves its upper edge 2.30 -> 1.15.
  - TW-N separates the law from A = 1 below v*.
- My own amplitude test, which is reported but not gating, gives ABOVE A = 0.000 [0, 2.85] / [0, 3.27]. That is close to ALP1's [0, 2.30], and my TW-D halves it too (to 1.425 / 1.635).
- **So the NO VERDICT comes from where the bite rule was frozen, not from a different number.**

**Membership.**

| | ALP1 | ALP1R |
|---|---|---|
| canonical, above / below | 9 / 9 | 10 / 9 |
| alt, above / below | 9 / 9 | 9 / 10 |

Every disc at z >= 2.1 is above in both builds, apart from the two below:
- **ID 24.** ALP1 left it ungraded: it found no M*. Here it is graded with M* = 10^10.64 and measured L'CO(1-0) from the on-disk ADF22 record, which was read directly from PDFs in an earlier approved lane. It is above in both builds' arithmetic.
- **ID 19 on alt.** Here it is below at 214 against 215 km/s. ALP1 puts it above, because its class-M gas gives log M_b 11.38 against 11.15 here.

**MEAS (measured speed):** 15 / 11 above here; 15 / 12 in ALP1.

**Baryon masses, disc by disc (log M_b; ALP1 / ALP1R) and the cause.**

| ID | ALP1 | ALP1R | cause of the difference |
|---|---|---|---|
| 1 | 10.26 | 10.28 | r21 0.84 (ALP1, Bothwell+13 read) vs 0.77 (mine, from memory) |
| 2, 3 | 10.94, 10.84 | 10.94, 10.84 | same |
| 6, 7, 8, 9 | 11.10, 11.28, 11.39, 11.05 | 11.12, 11.30, 11.41, 11.07 | r21 0.84 vs 0.77 (+0.04 dex on gas) |
| 11, 12 | 11.01, 10.93 | 11.02, 10.94 | r21 |
| 13 | 11.77 | 11.60 | [CI](2-1)/(1-0): ALP1 R_CI 0.33 (from T_ex 29.1 K) vs my declared 0.55 |
| 15 | 11.50 | 11.63 | ALP1's primary gas is Dunne+22 class M (10.81); mine is L' / r32 with alpha 4.36 (11.26). Class M is my reported GAS-D |
| 18 | 11.89 | 11.41 | class M 11.82 vs my SB-scaled [CI] 11.13 |
| 19 | 11.38 | 11.15 | class M 11.21 vs my SB CO 10.78 |
| 20 | 11.57 | 11.67 | class M 10.72 vs my MS CO 11.16 |
| 22 | 11.42 | 11.07 | class M 11.29 vs my SB CO 10.68 |
| 23, 25, 28 | 11.97, 11.18, 11.64 | 11.97, 11.18, 11.64 | same (r32 0.52 vs 0.54 within 0.01) |
| 24 | not graded | 11.39 | mine uses the ADF22 record |

- Stellar masses are identical (ALPAKA STARDUST).
- R_e is the same in both (dashed / R_ext/1.2), except ID 24: mine is F444W 1.55 kpc; ALP1's is R_ext/1.2 = 2.96.
- **Gas extent differs:** ALP1 puts the gas at R_ext/1.2 for every disc; I use the stellar R_d.
- **Inclination:** I add a per-disc inclination prior to the amplitude test; ALP1 has none.

**Best A.**

| group | ALP1 | ALP1R (amplitude, reported) | ALP1R (shape-only, gating) |
|---|---|---|---|
| ABOVE | 0.000 [0, 2.30] both footings | 0.000 [0, 2.85] / [0, 3.27] | 0.000 [0, 6] |
| BELOW | 5.945 [3.375, 6] | 4.855 [1.68, 6] / 4.29 [1.41, 6] | 1.90 / 1.62 [0, 6] |

- The direction is the same in both builds. The below discs are lighter in baryons than their curves: IDs 1, 9, 11 and 12 in both.
- The law and A = 1 cannot be told apart below v* in either build.

**Shape.**
- Both builds find the same physical misfit: the Freeman disc rises across the rings while the data are flat.
- ALP1's half-split S with s2 = 17.8 lets the ABOVE shape lines hold.
- My outermost-minus-innermost S, with s2 about 8.6 in the shape test, fails them for every model alike (D about -0.35). The inner rings sit under half the beam for most discs, so this misfit may be partly instrumental.
- In both builds the shape lines do not separate the models.

**MEAS canonical.**
- ALP1 gets FAILS (A 2.82 [0.285, 6]; the reference shape fails while baryons alone pass).
- I get NO POWER (A 1.24 [0, 4.72]).
- Cause: ALP1's heavier class-M gas for 18 and 22, and no inclination prior. My prior de-weights the low-inclination discs 11, 18 and 22 (i about 26 deg, sigma_inc 0.25 to 0.56 dex), which widens the interval.

**DSC1 (read now, for context only).** On six Genzel+2017 curves plus zC-488879, DSC1 reads canonical ABOVE "HOLDS, FRAGILE"
(A 0.67 [0.25, 1.175], 3 discs) and BELOW "LAW FAILS BELOW". The ALPAKA rings neither repeat nor contradict that. Their
reach (0.8 to 3.6 R_e, mostly 1.2 by convention) and the baryon overshoot leave A unconstrained by shape, and leave A by
amplitude set by the gas conversion.

## What is the same and what it means

The two independent builds made different gas, ID 24, inclination and twin choices, yet both say the ALPAKA I rings cannot
grade the joint's distinctive statement:
- **Discs above v*(z):** the halo is invisible inside 6 kpc, and the SED-plus-line-luminosity baryons already exceed the dynamics.
- **Discs below v*(z):** the law and the reference cannot be told apart.

A test needs three things:
- gas conversions measured per disc;
- measured sizes for the 11 convention discs;
- rings well beyond 3 R_e.

## Blindness record

- Nothing of ALP1 or of DSC1's results was seen before edd13ab6bf.
- Before that commit:
  - the ALP1 folder's existence was seen in a directory listing (closure_2026_11_13);
  - DSC1's file names were seen in a listing;
  - lines 20-70 of `dsc1.py` were read, as allowed (halo construction and ALPAKA paths), and contain no number.
- CFG229 and CFG272 READMEs (earlier lanes) were read before the freeze, and that is disclosed in READING section 0.

**Commit ids and the lead's re-run (added 2026-11-13, after landing; no number or label changes).** Local: READING
8d3b72f35f, script and outputs 5feaf7b5a3, RESULT_BLIND edd13ab6bf, RESULT 3f6a09eec8 (origin tip 97793aea6b). Pushed.
The lead session re-ran `alp1r.py` from a copy at the same folder depth: `alp1r.json` and `alp1r.out` are equal byte for byte. The
twins and the grader (which reads the twins' outputs) were not re-run. A reproduction,
not a further independent re-grade.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
