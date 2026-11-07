# QX30: is the law's hot-system failure an artefact of the LCDM assumptions in the data? ROBUST (both footings)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (f861a41f04), committed and pushed
alone before any script. Script: qx30.py (one thread, under a minute). Outputs: qx30.out / qx30.json, MUTATE in
qx30_MUTATE.out / .json. Ledger: ASSUMPTION_LEDGER.md (one row per assumption, with source, sign, size and class).

## Label

**ROBUST on both footings.** The one admissible, framework-native correction is to replace each paper's fiducial
D_A(z) with the framework's own (flat, constant rho_DE, Omega_m 0.3085, h 0.674). It moves X-COP by -0.0205 dex.
The cluster failure is not an artefact of the data's cosmology. The answer "the assumption doesn't matter" holds.

| Sample (line) | plain law | after C1 (native D_A) | shift | all-favourable bound (reported) |
|---|---|---|---|---|
| X-COP, 35 pts (HO1: \|mean\| <= 0.05, rms <= 0.10) | +0.468 / +0.435 | **+0.447 / +0.414** (rms 0.456 / 0.424) | -0.021 / -0.021 | +0.329 / +0.298 (rms 0.34 / 0.31), outside |
| Lovisari groups, f* 0.5 (bracket f* 0-1 must reach +-0.05) | +0.264 / +0.226 | **+0.245 / +0.207**, bracket [+0.177, +0.338] / [+0.140, +0.300] | -0.019 / -0.019 | +0.154 / +0.117, outside |
| Humphrey ellipticals, Kroupa (G7 0.15) | +0.210 / +0.189 | **+0.208 / +0.186** | -0.002 (NGC 6482 only) | +0.067 / +0.049 (Salpeter carries it, as QX18) |
| Coma UDGs (scaling bracket, not re-solved) | +1.12 / +1.08 | +1.09 to +1.10 / +1.05 to +1.06 | -0.016 to -0.033 | - |

## Why the distance correction is small

All four samples sit at z <= 0.09, so D_A is close to 1/h and Omega_m does not enter (0.3 -> 0.3085 moves X-COP by
+0.0002). The ratio D_A,nat / D_A,fid is 1.038, set by 0.70/0.674. Gas mass scales as D^2.5, stars as D^2 and the
hydrostatic mass as D. The law's mass rises faster than the measured mass, by about 1.25 powers of D, so
Delta moves by -1.25 log10(1.038), about -0.02. The framework's H0 is disputed in the record (CFG885), and the bracket is
symmetric: at h 0.70 the shift is +0.000 and at h 0.73 it is +0.023. No native choice of h moves Delta by more than
about 0.03.

## Top assumptions by size (X-COP, canonical; alt within 0.001)

1. Non-thermal pressure (Eckert+2019, about 6 % at R500): +0.027. It is INADMISSIBLE, because it is built on a universal
   Omega_b/Omega_m, and it has the wrong sign. Applying it makes the miss larger.
2. Native distance in the SZ-pressure limit (beta 1/2): -0.029. Graded C1 (beta 1, XMM T): -0.021.
3. Salpeter instead of Chabrier for the stars: -0.026 (BOUND).
4. Clumping, mean instead of azimuthal median (sqrt(C) 1.1, PROVISIONAL): -0.022 (BOUND).
5. ICL omitted (Ghizzardi+2021 Sect. 4.1 counts the BCG, not the ICL), at 40 % of stellar light: -0.022 (BOUND).
6. Mass-model choice: the graded M_FORW assumes no mass model. The paper's NFW reference would give -0.006; Einasto
   +0.018. The NFW prior is not in the graded number.
7. Stellar deprojection x0.75 (gNFW galaxy profile), dropped: -0.011 (BOUND).

Four items have the wrong sign for the law: non-thermal pressure, simulation hydrostatic bias (about +0.1),
XMM-to-Chandra T calibration (about +0.04-0.06, PROVISIONAL) and spectroscopic-like T weighting. Every
LCDM-calibrated correction the literature would apply makes the cluster miss larger.

**Even if every BOUND is set at its favourable end** (h 0.671, beta 1/2, the NFW column, gas x1.1, stars x1.8/0.75/0.6),
X-COP moves by -0.139 / -0.137. That is PARTIAL-sized, but the criteria give this row no label, and it still sits at
+0.33 / +0.30, about 6 times the line. Groups reach +0.15 / +0.12. Only the ellipticals come near zero, and they do it
through the IMF (QX18 / QX26 already record this), not through any cosmological assumption.

## Known answers and controls

- KA1: with f = 1 the X-COP grade equals QX2 iter 1 exactly (|d| = 0). KA2: groups and ellipticals equal QX20's class
  means and f* brackets exactly. KA3: distance integral vs analytic EdS 3e-9, vs astropy 5e-12. All PASS.
- M1 (opposite sign, f -> 1/f): +0.0205 vs C1 -0.0205, symmetric -> BITES.
- M2 (swap back to each paper's fiducial background): reproduces every original offset to 0 -> BITES.
- M3 (planted h 0.35, f about 2): X-COP moves -0.38, to +0.085 / +0.053. The pipeline can see an artefact when one is
  planted -> BITES.

## Not evaluable (stated, nothing downloaded)

- A fresh non-parametric hydrostatic solve from n_e(r), T(r), P(r). Only X-COP's derived mass products are on disk. It
  would need the public X-COP thermodynamic profiles (< 1 MB). M_FORW is already the paper's no-mass-model solution.
- Humphrey+2006 non-NFW fits (N04, Sersic, parametric) and their baryon-fraction prior (Sect. VI.3). These are not
  transcribed. The fitted masses are constrained by the data at 2-8 Re, so the prior acts mainly beyond the graded radii.
- Lovisari T extrapolation to R500 (L15 Sect. 6.1.1). Its sign is unknown and it cannot be computed on disk.
- UDGs: the scaling bracket only. S1's hosted solve was not rerun.
- Bullet: not in the QX20 ladder and not graded.

## Disclosed

- Source-paper details come from page-tool reads of the arXiv / ar5iv HTML and are PROVISIONAL. That covers Ettori+2019
  Sect. 1-3 and 6, Lovisari+2015 Sect. 1, 3.4-3.6, 5 and 6, Humphrey+2006 Table 1 and Sect. VI-VIII, and Ghizzardi+2021
  Sect. 4. The clumping 1.1, ICL 40 % and T-calibration 10-15 % figures are literature upper ends from memory, also
  PROVISIONAL. They enter only BOUND rows.
- The first graded run multiplied the ellipticals' Kroupa masses by a flat x1.8 in the bound row. This was corrected,
  before the README, to Humphrey's per-galaxy SPS Salpeter/Kroupa ratio, the same input QX18 uses. Only that reported row
  changed (+0.008 -> +0.067). No graded number changed.
- No Lean file: the lane's algebra is the power counting above. The swarm brief's Lean twin rule was not applied, and no
  certification is claimed.

Kappa = 1/2 FITTED; not theory closed.
