# QX24: is the law's hot/cold step keyed on environment? KILLED as frozen, on both footings, but the kill is fragile

Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
- Criteria: iter_1/FROZEN_CRITERIA.md (local d4f3f62c47, pushed as a2e21898a1), committed and pushed before any script.
- Script: iter_1/qx24.py (one thread, seconds). Outputs: iter_1/qx24.out / qx24.json, and qx24_MUTATE.* for M2.
- A rerun gives a byte-identical qx24.json.
- All data are on disk; nothing was downloaded.

Key E (frozen, calibrated on dwarfs only): E(x_e) = Delta_s H(x_e - x_c), where x_e is the Newtonian external field over a0.
- Delta_s = +0.199 canonical / +0.188 alt: the graded satellites' plain offset minus the SPARC anchor.
- x_c = 0.045 / 0.041: the geometric mean of the field dwarfs' largest x_e and the graded satellites' median x_e.

## Label: KILLED (as frozen). It rests on T2 alone, and T2 depends on how the environment is read

| Test | canonical | alt | Power / note |
|---|---|---|---|
| T1 KiDS isolated lenses | NO VERDICT (z 2.46) | NO VERDICT | carried from QX21, known before the freeze |
| T2 X-ray ellipticals | **KILLED** | **KILLED** | rests on the frozen noclu reading (below) |
| T3a tidally safe satellites | NO VERDICT (N 1) | NO VERDICT | no power: the tau < 0.05 cut leaves 1 of 38 |
| T4 SPARC | NO VERDICT (no power) | NO VERDICT | every SPARC galaxy sits below x_c (max x_e 0.006) |

### T1: KiDS isolated lenses
E predicts no early/late split for isolated lenses, which have no neighbour with more than 0.1 M* within 3 Mpc. QX21 measured
+0.158 +- 0.064 (z 2.46). The frozen rule needs 3 sigma to kill, so this is NO VERDICT. The number was known before the
freeze, and the criteria say so.

### T2: X-ray ellipticals
All 7 sit below x_c on the frozen (noclu) reading. Their median offset is +0.216 / +0.194, above the 0.15 line, so E is
killed.

**The kill is fragile.** On the maxclu reading (completeness weighting plus x8 missing baryons), the two Virgo members
NGC 4472 and NGC 4649 move above x_c (x_e 0.25 / 0.21):
- the other 5 have median +0.079 / +0.061, under 0.15;
- the Virgo pair has median +0.336 / +0.316, above Delta_s - 0.15.

So T2 would read COMPATIBLE on the maxclu reading. The label uses the frozen noclu reading and is not changed.

**The sharpest single fact, read with no line.** NGC 720 is the most isolated of the seven (x_e 2e-4, noclu), yet it
carries the largest offset, +0.51 / +0.48. Spearman between offset and log x_e is +0.07 (p 0.88).

**Disclosed:** positions for NGC 4125, 4261, 4472 and 6482 are literature J2000 coordinates written into the script, not
read from a file. NGC 720, 1407 and 4649 use the median SLUGGS GC position.

### T3: satellites, environment against tides
**T3a has no power.** With Wolf masses and V_c = 200 / 230 km/s hosts, R_e/r_J has p10 / p50 / p90 of 0.064 / 0.140 / 0.384.
Only Andromeda XVIII falls under the frozen 0.05. The cut was too strict to leave a sample.

**T3b (reported):** across 69 satellites,
- the partial rho of offset with log x_e at fixed log tau is +0.71, against a shuffle 95th percentile of 0.25;
- the partial rho of offset with log tau at fixed log x_e is -0.75.

Offsets rise with the host's field, the opposite sign to EFE, and fall with tidal susceptibility at fixed field. x_e and tau
both scale with d_host and are strongly collinear, so these partials may be suppression artefacts. No label rests on them.

M1 as frozen is vacuous (a percentile against itself). The meaningful shuffle number is the 0.25 above.

### T4: SPARC
No SPARC galaxy reaches x_c (max x_e 0.006), so T4 has no power. Reported: Spearman between the residual and log x_e is
-0.17 (p 0.04) / -0.16 (p 0.05). It is weakly negative, EFE-like, and the opposite sign to E.

## Known answers and controls
- KA1: the MW-classical plain median 0.2445 (QX21 T2) is reproduced. PASS.
- KA2: the SPARC anchor equals QX20's sparc_mean. PASS.
- KA3: the estimator reproduces gext_vectors.csv on 3 rows to 4.8e-5 dex, against a 1e-3 line. PASS.
- M2 (Newton dwarf and SPARC offsets): Delta_s moves +1.15 / +1.20 dex, more than 0.3, so it bites. The ellipticals' offsets
  stay plain in M2, since QX18 has no Newton column.

## What the step is not keyed on (QX20-QX24)
Every single measured variable tried so far fails to separate the classes on its own:
- QX20: baryonic mass, g_N / surface density, potential depth, r/r_M, total gas fraction;
- QX22: kinematic support (lambda_R, v/sigma);
- QX23: cold-gas fraction inside SPARC's range, and uncounted baryons at stated ceilings;
- QX24: environment as the external Newtonian field, killed as frozen and fragile.

This is the crisp target. The law misses dispersion-dominated and early-type systems by about +0.2 dex (isolated ones
included: NGC 720, KiDS isolated early types) and clusters by about +0.45. Rotating, gas-rich discs and field dIrrs sit on it.
No single measured variable from this list separates the two sets. Morphology or type as such is the one untested candidate,
and it is a label, not a physical variable.

Kappa = 1/2 FITTED; not theory closed.
