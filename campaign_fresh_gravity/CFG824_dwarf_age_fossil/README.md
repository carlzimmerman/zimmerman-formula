# CFG824 — H-FOSSIL: does the dwarf excess over the law grow with formation age?

Criteria: `FROZEN_CRITERIA.md` (fba1e9482, committed before any age data was read). Run: `python3 cfg824.py`
(MUTATE: `CFG824_MUTATE=1`). Seconds. Ages: Weisz et al. 2014 (VizieR J/ApJ/789/147, tables 5/6, downloaded 2026-10-18 to
`real_research/data/dsph/weisz2014_dl/`); τ50/τ90 = lookback where the published cumulative SFH reaches 50%/90% (linear in
log t; combined-field table 6 where given). Reading checks: Draco τ90 10.1, Fornax 2.2, Leo I 1.7 Gyr (match the paper's
values to the grid resolution).

## Result — CLASS (canonical, out-of-sample): **NO SIGNAL** (a positive hint that weakens under the M/L control)
| out-of-sample, N = 28 (τ90 range 12.1 Gyr) | Spearman ρ | one-sided p | weighted slope (per Gyr) |
|---|---|---|---|
| primary (Υ = 2) | **+0.42** | **0.012** | +0.040 ± 0.012 |
| C-ML (Υ_V ∝ τ50^0.7) | +0.24 | 0.113 (needs < 0.10) | +0.026 ± 0.012 |
| training, MW 8 (post-hoc, not a verdict) | +0.74 | 0.018 | +0.074 |

Alt footing is the same to 0.01 (ρ +0.42 / +0.24). Classes are identical.

- The primary passes on unseen dwarfs (M31 satellites, field dwarfs, MW ultra-faints): older dwarfs sit higher above the
  law. But about 40% of the slope goes away when old populations get their higher stellar M/L, and the controlled trend
  misses the frozen p < 0.10 by 0.013. By the frozen rule: NO SIGNAL.
- Old, quenched M31 satellites carry large excesses (And XI +1.08, And V +0.73, And XIII +0.72, CVn II +0.99, Leo IV +0.58);
  young, gas-rich systems sit on the law (WLM, NGC 6822, Sag dIrr, Leo A, NGC 205). Exceptions: NGC 147 and IC 1613 sit far
  below (−0.6), Hercules on the law, M 32 high (compact elliptical, Newtonian regime).
- **Reading:** the age pattern seen in the MW dSphs is partly real in independent dwarfs, but not cleanly separable from
  stellar M/L with these data. H-FOSSIL is neither supported nor excluded. A cleaner test needs stellar masses from
  resolved-SFH mass formed (Weisz TMass) rather than M/L × L_V — declared here as the next step, not run.

## Controls
- K1 PASS: Draco law σ 4.61 = CFG821.
- MUTATE bites: an injected E = 0.06 τ90 is classed SUPPORTS (ρ +0.84); shuffled ages on the real E give NO SIGNAL (ρ −0.05).

κ = ½ fitted; cold energy mass required; not theory closed.
