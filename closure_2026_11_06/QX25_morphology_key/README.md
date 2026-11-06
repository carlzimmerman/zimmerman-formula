# QX25: is the plain-law step keyed on morphology? NO VERDICT as frozen (inside SPARC); KiDS colour and Sersic carry the same split

Criteria: iter_1/FROZEN_CRITERIA.md (local 013603a955, on origin 974b44c768), committed and pushed before any graded number.
Script: iter_1/qx25.py. Outputs: qx25.{out,json} and qx25_MUTATE.{out,json}. Kappa = 1/2 FITTED; not theory closed. Both
footings, never pooled.

## Result

**T1: SPARC Hubble type at fixed g_bar.** EARLY (T <= 2, 16 galaxies) minus LATE (T >= 7, 97 galaxies), over 6 shared
0.25 dex bins. The prediction for a type key sized to QX20's step is D >= +0.20.

| Mode | canonical | alt | Label |
|---|---|---|---|
| L0: law, fixed U = 0.5 (**primary**) | +0.078 +- 0.045 | +0.079 +- 0.045 | **NO VERDICT** (0.20 - 3 sigma = 0.064 < D < 3 sigma) |
| L1: law, refit U | +0.107 +- 0.028 | +0.104 +- 0.029 | KILLED |
| E0: exact field, fixed U | +0.036 +- 0.045 | +0.035 +- 0.045 | KILLED |
| E1: exact field, refit U | +0.082 +- 0.028 | +0.081 +- 0.029 | KILLED |

- On the primary (L0), D sits 1.7 sigma above zero and 2.7 sigma below the +0.20 prediction. It misses both frozen lines,
  so the label is NO VERDICT.
- On the action's exact field, the early-type excess halves to +0.036: KILLED on both footings.
- Absorbed channel: the median log10 U_refit for EARLY minus LATE is +0.07 / +0.14 on the law and -0.04 / +0.02 on the
  exact field. A refit can hide at most about 0.1 dex of a type offset.
- Robustness, reported only: Q <= 2 gives +0.056, and EARLY T <= 3 gives +0.064.

**T1b: continuous type proxies (L0).**

| Proxy | D (both footings) | Label |
|---|---|---|
| Bulge-dominated (8) minus bulgeless (143) | +0.031 +- 0.036 | **KILLED** |
| SBdisk top minus bottom quartile | +0.088 +- 0.041 | NO VERDICT |

**T2: KiDS isolated lenses, at fixed g_bar** (Brouwer+2021 Fig. 8).

| Split | D | D / s_tot | Carries (>= 3 s_tot)? |
|---|---|---|---|
| colour (u-r >= 2.5) | +0.158 +- 0.064 | 2.47 | no |
| Sersic (n >= 2) | +0.155 +- 0.064 | 2.43 | no |

The two proxies carry the same split with the same weight, so the lensing data cannot tell colour from structure.
Testing at fixed stellar mass is not possible on disk; see NEEDS_OWNER.md.

**T3, by the frozen rule.** T1 is not KILLED on the primary, so the "spheroids vs discs" statement is NOT made. What the
data show: inside discs, early types sit at most about +0.08 dex above late types on the law, and +0.04 on the action's
exact field. That is under half the +0.20 a type key needs. The KiDS lensing split is +0.16 at 2.4-2.5 sigma, for colour
and Sersic alike.

## Reading (post-data, not the label)

- The step does not grow smoothly with type inside SPARC. Bulge fraction is flat. Hubble type gives at most a third of the
  step on the law, and about a fifth on the exact field.
- The lensing excess appears for colour and Sersic equally. It is about the size of what SPARC's early-type end allows
  on the law (+0.08 to +0.11), plus about 0.05.
- Read together with QX20-QX24, the step looks like a separation between spheroid-dominated hot systems (ellipticals,
  groups, clusters, dSphs) and discs, not a property graded within discs.
- That is a reading, not the frozen T3 statement, and it rests on systems outside SPARC's T range.

## Known answers and controls

- KA1: QX8's algebraic pooled grade reproduced through the import exactly (0.054087 @ 0.52; 0.053718 @ 0.44).
- KA2: QX21's colour D reproduced (+0.15817, s_stat 0.04010).
- KA3: CFG61's Sersic split chi2 = 69.07 (69.1 +- 0.5).
- M1, shuffled T: mean shuffled D = -0.002, within 0.5 sigma_D. PASS. The shuffled sd (0.059) is larger than the bootstrap
  sigma (0.045); against the shuffled distribution, the observed L0 D is 1.3 sd.
- M2: a planted +0.20 on EARLY is recovered as +0.2000. BITES.
- M3, Newton: the SPARC anchor shifts +0.43 / +0.46. BITES.
- The rerun gives a byte-identical json.

## Scope

SPARC discs (S0 to Im) and B21's isolated KiDS lenses only. There are no ellipticals inside SPARC. Nothing about
spheroid-dominated systems outside SPARC is graded here.
