# LNJ1 RESULT: is the ceiling break in Euclid's lenses the crossing-speed joint's switch?

**NO POWER, FRAGILE / NO POWER (canonical / alt), as frozen.**

- **The break is not the joint's switch on the joint's own membership rule.** The rule reads each lens's speed from its
  stars. That speed hardly moves with Einstein radius: median s = 0.43 to 0.46 in every theta_E class on canonical,
  0.36 to 0.38 on alt.
- **Few lenses sit above v*(z).** 26 of 6,173 do on canonical (all at z_l 1.09 to 1.72, theta_E median 0.83"). None do
  on alt.
- **The ceiling breakers are not the fast ones.** Of the 855 / 748 lenses above the law's band, 4 / 0 are above v*.
  The lenses the rule does hand to the cold dust are no more ceiling-breaking than the rest: 0.154 above the band,
  against 0.138 below the boundary.
- **No break in speed.** On the model speed there is no real step (Delta f 0.016 / 0.035). The fraction above the band
  FALLS with s, because s grows with stellar mass.
- **Canonical is FRAGILE.** Three brackets give a different word: the measured-speed rule, the AGEL source draws, and
  the PD1 share. Each gives an amplitude word, not a switch word (section 4).

POST HOC twice: the wide-lens break was seen first (EUC1, EUC4), and the joint was built after other rows failed. The
boundary was not tuned to lenses, and that is the only reason the test has value. Nothing here is a pass, and no word is
favourable.

TEST lane: adopts nothing, relabels nothing, registers nothing. Criteria 640fbf99e4 (alone, before any script or number);
script and outputs 075770dbed. No amendment. Footings never pooled. Cold dark energy is a gravitating field component;
no particle. kappa = 1/2 and the share 5.41 are FITTED.

## 1. Membership (sample S: EUC1 cuts, grades A + B, N = 6,173; source at infinity)

| rule | canonical above / below | alt above / below | median s (can / alt) |
|---|---|---|---|
| **model (JNT2 primary; stars on EUC12's common scale, +0.036 dex)** | **26 / 6,147** | **0 / 6,173** | 0.434 / 0.359 (max 1.158 / 0.958) |
| catalogue mass scale (bracket) | 18 / 6,155 | 0 / 6,173 | 0.422 / 0.349 |
| measured speed, SIS from theta_E (bracket) | 127 / 6,046 | 18 / 6,155 | 0.615 / 0.509 |
| measured speed, AGEL source draw 0 (bracket) | 1,323 / 4,850 | 533 / 5,640 | 0.780 / 0.646 |

Median v*(z_l) is 450 / 544 km/s; median z_l is 0.69.

### Speed by Einstein-radius class (`lnj1_readings.out`, post-run reading)

Columns, canonical / alt: s_model median; s_meas median; number at s_model >= 1; fraction above the band.

| class | N | s_model median | s_meas median | at s_model >= 1 | above the band |
|---|---|---|---|---|---|
| theta_E < 1.0" | 3,993 | 0.43 / 0.36 | 0.58 / 0.48 | 19 / 0 | 0.064 / 0.057 |
| 1.0 to 1.3" | 1,211 | 0.44 / 0.36 | 0.65 / 0.53 | 5 / 0 | 0.149 / 0.124 |
| 1.3 to 1.7" | 653 | 0.43 / 0.36 | 0.68 / 0.57 | 1 / 0 | 0.329 / 0.285 |
| >= 1.7" | 316 | 0.46 / 0.38 | 0.82 / 0.67 | 1 / 0 | 0.642 / 0.589 |

The rank correlation of s_model is 0.75 with log M* and 0.81 with z_l. The model speed tracks stellar mass and redshift,
not the Einstein radius.

## 2. Boost against s (primary: model rule, z_s infinity)

b = log10(M_obs / M_law). "Above" = the fraction above the law's band (M_obs > M_law(1.78 M*)). Both columns are
canonical / alt.

| s bin | N | b median | above |
|---|---|---|---|
| < 0.3 | 997 / 1,965 | +0.065 / +0.017 | 0.260 / 0.190 |
| 0.3 to 0.4 | 1,580 / 1,867 | -0.004 / -0.072 | 0.149 / 0.096 |
| 0.4 to 0.5 | 1,456 / 1,236 | -0.065 / -0.113 | 0.109 / 0.076 |
| 0.5 to 0.6 | 1,000 / 672 | -0.108 / -0.126 | 0.088 / 0.076 |
| 0.6 to 0.8 | 934 / 394 | -0.115 / -0.144 | 0.094 / 0.114 |
| 0.8 to 1.0 | 180 / 39 | -0.115 / -0.225 | 0.122 / 0.103 |
| 1.0 to 1.25 | 26 / 0 | -0.199 / - | 0.154 / - |

The fraction above the band on each side of s = 1 (canonical): 0.138 [0.129, 0.146] below and 0.154 [0.038, 0.308]
above. On alt it is 0.121 below; nothing is above.

**Measured-speed bracket, for comparison (canonical):**

| s bin | N | b median | above |
|---|---|---|---|
| 0.4 to 0.5 | 906 | -0.065 | 0.091 |
| 0.5 to 0.6 | 1,735 | -0.062 | 0.096 |
| 0.6 to 0.8 | 2,535 | -0.046 | 0.136 |
| 0.8 to 1.0 | 697 | +0.027 | 0.245 |
| 1.0 to 1.25 | 115 | +0.156 | 0.461 |
| >= 1.25 | 12 | +0.310 | 0.750 |

On this rule the fraction above the band rises with s. It is 0.131 below s = 1 and 0.488 [0.394, 0.567] above.

## 3. Free break location (step in the fraction above the band; 400 bootstraps)

| configuration | canonical s_b [95 %] | Delta f (2.5 % point) | alt s_b [95 %] | Delta f (2.5 % point) |
|---|---|---|---|---|
| **model rule (primary)** | 0.912 [0.759, 1.023] | 0.016 (0.000): **not real** | 0.741 [0.617, 0.851] | 0.035 (0.000): **not real** |
| measured rule, z_s infinity | 0.794 [0.692, 0.933] | 0.161 (0.118): not real | 0.661 [0.617, 0.759] | 0.157 (0.119): not real |
| measured rule, AGEL draw 0 | 1.047 [0.776, 1.123] | 0.335 (0.255): real | 0.851 [0.757, 0.933] | 0.338 (0.277): real |
| model rule, AGEL draws (50) | median 0.78, never real | | median 0.62, never real | |
| the same fit in theta_E (reading) | 1.288" [1.174, 1.445] | 0.347 (0.284): real | 1.288" [1.175, 1.445] | 0.311 (0.258): real |

The data's own break is in Einstein radius, at 1.29": the fraction above the band steps from 0.08 to 0.43 on canonical
and from 0.07 to 0.38 on alt.

- **Model speed (the joint's).** No real break. The step fit is forced to f_hi > f_lo and finds only a 0.02 / 0.04 rise.
- **Measured speed.** The break shows only because v_meas is built from theta_E. Its location is not stable:
  - at z_s infinity it is 0.79 [0.69, 0.93] / 0.66 [0.62, 0.76], below the 0.20 line;
  - with AGEL sources it is real, at 1.05 [0.78, 1.12] canonical (the interval contains 1) and 0.85 [0.76, 0.93] alt.
- **Shuffle twin.** On the AGEL measured-speed reading, shuffling the stellar masses does NOT destroy the break. That
  sends that reading to NO POWER by the frozen gate: the break is set by the Einstein radius, not by the lens's baryons.

## 4. What stars plus the cosmic share give above the boundary, against the observed Einstein masses

r = log10(M_obs / M_pred), median [95 %]; the joint is FITS inside [-0.10, +0.10].

| configuration (lenses above) | canonical | alt |
|---|---|---|
| **primary: model rule, X 5.41, z_s infinity (26 / 0)** | **-0.173 [-0.219, +0.022]: FITS (interval)** | none above |
| model rule, AGEL sources (26 / 0), 50 draws | +0.348 median (draw 0 +0.368 [+0.252, +0.555]): UNDER-PREDICTS, all 50 draws | none above |
| measured rule, z_s infinity (127 / 18) | **+0.231 [+0.168, +0.290]: UNDER-PREDICTS** | +0.376 [+0.284, +0.458] (N 18 < 20: NO POWER) |
| measured rule, AGEL draw 0 (1,323 / 533) | +0.353 [+0.340, +0.373] | +0.436 [+0.410, +0.466] |
| X = PD1 share (~56), model rule, z_s infinity | -0.283 [-0.329, -0.149]: OVER-PREDICTS | none above |
| X = PD1 share, measured rule, z_s infinity (reported only) | +0.027 [-0.013, +0.060] | +0.108 [+0.054, +0.179] |
| c x 0.7 / c x 1.4 (model rule) | -0.152 / -0.200 | none above |
| catalogue scale (18 above) | -0.106 [-0.154, +0.119] | none above |

**Where the projected halo stands against the law.** At the cosmic share, stars plus the reference halo inside R_E give
about what the law gives on the same stars: median log ratio -0.018 for the model-rule lenses above, -0.049 / -0.081 for
the measured-rule ones. The reference halo is too extended to put its cold mass inside 5 to 15 kpc. So where the law
falls short (the wide lenses), the joint falls short by about as much:
- +0.23 / +0.38 dex at z_s infinity, a robust direction;
- +0.35 to +0.44 dex with AGEL sources.

**What the PD1 share does.** It adds about 0.1 dex. That over-shoots the 26 compact massive model-rule lenses at z_s
infinity, a direction that is not robust because real sources raise M_obs. It roughly meets the measured-rule lenses at
z_s infinity but not with AGEL sources.

The 26 canonical model-rule lenses are high-z (1.1 to 1.7), massive (log M* 11.5 to 12.1) and small (theta_E 0.83"). They
are not the wide lenses: of the 316 lenses with theta_E >= 1.7", one is above v* on canonical and none on alt.

## 5. Final words, gates and brackets

| | canonical | alt |
|---|---|---|
| primary raw word | NO POWER (no real break; N above 26 but the joint FITS by interval, and the step at s = 1 has upper bound 0.17, so not NO SWITCH) | NO POWER (0 above) |
| TW-H (v*/2) | bites (2,140 above; raw NO SWITCH: fraction above the band 0.094 above v*/2) | bites (1,105 above; NO SWITCH) |
| TW-D (2 v*) | bites (26 to 0 above) | **does not bite** (0 to 0): NO POWER regardless |
| TW-SH (masses shuffled) | no main break to destroy (gate trivially passed) | same |
| **final** | **NO POWER, FRAGILE** | **NO POWER** |
| catalogue scale | NO POWER | NO POWER |
| c x 0.7 / c x 1.4 | NO POWER / NO POWER | NO POWER / NO POWER |
| X = PD1 share | JOINT OVER-PREDICTS ABOVE THE BOUNDARY (-0.283; not robust to source z) | NO POWER |
| measured-speed rule | JOINT UNDER-PREDICTS ABOVE THE BOUNDARY (+0.231) | NO POWER (18 above) |
| AGEL source draws (majority of 50) | JOINT UNDER-PREDICTS ABOVE THE BOUNDARY (50 / 50) | NO POWER (50 / 50) |

Readings outside the frozen gates:
- **Shuffle twin on the measured rule at z_s infinity.** It turns a not-real break into a real one (s_b 0.62 / 0.50,
  Delta f 0.27 / 0.26). Shuffling the stars makes the speed rule built from theta_E look more like a switch, not less.
- **TW-H on the model rule.** It reads NO SWITCH on both footings. Lenses faster than half the joint's speed break the
  ceiling no more often than slower ones.

## 6. Known answers (all pass)

| check | result |
|---|---|
| KA-0 own loader | same ids and order as EUC1's load / select (6,173) |
| KA-1 EUC4 W_B f25 (own route, no bisection) | 0.758 / 0.702 (N 124) |
| KA-1 EUC1 P f25 | 0.156 / 0.139 (N 3,192) |
| KA-2 EUC13 M1 AGEL b_med on P | +0.2381 / +0.2200 (target +0.238 / +0.220); b table against EUC1's bisection, max difference 8.8e-5 |
| KA-3 v*(0) | 668.53 / 807.93 km/s |
| KA-4 halo copy against SRJ3 K5 (zC 400569) | r_200c 121.61 (121.62) kpc, r_s 39.53 (39.53) kpc, g_mod 4.4281e-10 (4.4290e-10; 0.02 %, constant-set difference); halo table against direct solves, max difference 2e-4 |
| KA-5 projection | point mass 2e-11; NFW cylinder against analytic 5e-9 |
| KA-6 SI hand check, EUCL-DR1-L021762 | Sigma_cr 1,297 Msun/pc^2, M_obs 1.970e11 Msun, v_meas 278.5 and v_L 228.4 km/s, agreeing to 1e-10 |

KA-1 and KA-2 used the EUC lanes' alt a0 of 1.132e-10. This lane uses 1.1312e-10 everywhere else.

## 7. Estimate against the outcome

**Model rule.**
- Expected: at most a handful above v*, and NO POWER.
- Outcome: 26 above on canonical (more than a handful, all high-z, massive and compact) and 0 on alt. NO POWER on both,
  with canonical FRAGILE.
- Right on the word, wrong on the count. The weak-break expectation was right; the fraction above the band even falls
  with s.

**Measured rule.**
- Expected: s_b 0.55 to 0.65 / 0.45 to 0.55, with an interval excluding 1, and NO POWER through the shuffle twin.
- Outcome: 0.79 / 0.66 and not real at z_s infinity, so the shuffle gate never applied. The word is UNDER-PREDICTS
  canonical and NO POWER alt.
- The break sat higher than I guessed.

**Amplitude.**
- Expected: under-prediction of about 0.3 dex.
- Outcome: +0.23 / +0.38 at z_s infinity on the measured-rule lenses, and +0.35 to +0.44 with AGEL sources. Right.
- I also guessed the PD1 share's halo would put less inside R_E than it does. It adds about +0.1 dex over X 5.41.

## 8. Not counted, not done

**Baryons not counted.** Only the lens galaxy's stars are counted: no gas, no other group members, no intragroup light,
no group hot gas, no line-of-sight structure. Every one of them raises M_b, so it would raise the model-rule speed and
the reference halo.
- To bring a median wide lens (s ~ 0.45) to s = 1 needs M_b about 11 times its stars on canonical (about 18 times on
  alt, s ~ 0.38), since s scales as M_b^(1/3). That is group-scale baryons.
- EUC6 found the wide lenses in richer environments, so this is the open door. It was not frozen here and is not graded.

**Not done:**
- source redshifts other than infinity and the AGEL population (no measured sources exist; EUC1-F stays open);
- any independent blind re-grade;
- per-lens EUC12 deltas (a constant +0.036 was used).

The halo table is interpolated (checked to 2e-4). Nothing was fetched or pushed.

## 9. What this means

**For "Euclid's wide lenses break the ceiling".** The break is real, and it sits in Einstein radius at 1.29" on both
footings. LNJ1 reproduces EUC4's and EUC13's numbers exactly.

**For the joint.** The joint does not explain the break:
- Its switch is set by the lens's baryons. Those barely differ between wide and narrow lenses, so the rule puts almost
  every wide lens on the law's side (1 / 0 of 316). The few lenses it does move to cold dust are compact, massive and
  at high redshift, and they are not the ceiling breakers.
- Where a speed built from the Einstein radius pushes lenses over v*, the reference halo at the cosmic share,
  projected, gives about what the law gives. It leaves the same 0.2 to 0.4 dex shortfall.

**What would be needed instead.**
- The joint could only claim these lenses if their whole group, about ten times the stars in baryons, set the speed.
- Its halo would also have to be far more concentrated inside 5 to 15 kpc than FRZ1's reference layout.
- Neither was frozen. Both would be new freedom.

So, as built, the joint's switch neither causes nor reproduces the ceiling break. The break stays what EUC6 read it as:
a group-scale residual that the framework has no constructed state for.

## Files

- **Criteria:** `FROZEN_CRITERIA.md` (640fbf99e4).
- **Script and outputs** (075770dbed):
  - `lnj1.py`;
  - `lnj1.json`, `lnj1.out`, `lnj1_per_lens.csv`;
  - twins `lnj1_MUTATE_TWH`, `lnj1_MUTATE_TWD`, `lnj1_MUTATE_TWSH` (.json / .out);
  - `lnj1_readings.py` and `lnj1_readings.out` (post-run reading, reported only).
- **Read-only use:** EUC1's `euc1.py` and JNT2's `jnt2_common.py` were imported read-only with bytecode writing off.
  FRZ1's halo functions were copied. The data are the EUC lanes' files, checked against EUC1's frozen hashes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
