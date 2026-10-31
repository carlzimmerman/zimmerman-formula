# NZ2_consistent_m200_shell: F★-DEPENDENT [GAS-SCALE-DEPENDENT]. On X-COP's gas at f★ 0.034, all 15 keys and X-COP pass together, the first rule to do that. Its interior contradicts the zooms, and it fails at z_obs

Criteria: `FROZEN_CRITERIA.md` (38b051ea21), committed alone before any script or number. Proposal from Argon, relayed 10-31. `nz2_def.py`, `nz2_grade.py`, `nz2.out`, `nz2_results.json`, `nz2_MUTATE.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen grade (CE1's ng 64 tables, one template, M = MA1's M₂₀₀)
| Job | keys | over 2 | X-COP mean, rms | joint χ²/15, p |
|---|---|---|---|---|
| **X-COP's gas, f★ 0.034** | **15 of 15** | none, worst G-IN-Mall −1.99 | **−0.025, 0.083 PASS** | **13.3, 0.58** |
| X-COP's gas, f★ 0.0615 | 13 of 15 | G-IN-Mall −2.06, G-OUT-all −2.14 | −0.031, 0.084 PASS | 13.7, 0.55 |
| eRASS1's gas, f★ 0.034 | 13 of 15 | G-MID-T3 +2.20, G-OUT-M3 +2.83 | PASS | 24.5, 0.057 |
| eRASS1's gas, f★ 0.0615 | 13 of 15 | G-MID-T3 +2.06, G-OUT-M3 +2.66 | PASS | 22.5, 0.095 |

**F★-DEPENDENT [GAS-SCALE-DEPENDENT].** eRASS1's own gas: X-COP ONLY. The 0.0615 misses are narrow, 0.06 and 0.14 over the line, and the joint χ² stays good.

**Reported:**
- **At each cluster's z_obs, X-COP's gas: 13 of 15, G-IN-Mall −2.84, G-OUT-all −2.34** at f★ 0.034; −2.94, −2.52 at 0.0615. Joint χ² 15.5, p 0.42. This is the same redshift cost MA1 pays. ZN1's rule has z_obs built in.
- **γ_o past R₂₀₀:** 2.25, 2.65, 3.0 all give 15 of 15 at f★ 0.034, joint χ² 12.7, 13.3, 11.1. My choice of slope doesn't decide this.
- **SPARC and groups:** "clusters" path Υ 0.50 / 0.49 (the SPARC line misses on B by 0.01), groups +1.45. "All" path Υ 0.52 / 0.52, passes, and groups +3.84, FAIL. So one rule on every path still fails groups: they sit far inside r_f, so a shell can't touch them.

## Why the interior isn't physical
The zooms measure this directly (`../ZN1_zooms_to_z0/zn1_readouts.out`). At z = 0, 10¹⁴: M(<r_f) is about 0.87 M₂₀₀, and NZ2 has 0.50. Half of M₂₀₀ sits in a shell between 0.89 and 1.0 R₂₀₀, at many times the density inside it. Nothing in collisionless collapse builds that. NZ1's real mislabel was treating nominal M as M₂₀₀: the zooms give M₂₀₀ = 0.68 M nominal, so M/2 is 0.73 M₂₀₀ at z_f, before late mass.

So NZ2 is an empirical two-piece profile. What it shows is what the data ask for.

## The useful comparison with ZN1
| x (R₅₀₀) | 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | mean, rms |
|---|---|---|---|---|---|---|
| ZN1, native | **−0.164** | −0.104 | −0.055 | −0.010 | −0.016 | −0.070, 0.116 |
| NZ2 | **−0.030** | −0.086 | −0.053 | +0.010 | +0.034 | −0.025, 0.083 |

Nearly all of ZN1's X-COP miss is the single innermost point, x = 0.1 R₅₀₀, about 100–130 kpc. From x 0.2 outward the two differ by 0.05 or less. So the native profile and X-COP disagree over a narrow range at the centre, and that's where ZN3's 10¹⁵ shape and any central physics would act.

## Argon's numbers
| Quantity | Argon | Measured | Result |
|---|---|---|---|
| X-COP mean | about +0.005 | −0.025 | passes the gate as it said; 0.03 off |
| X-COP rms | about 0.07 | 0.083 | passes the gate; 0.013 off |
| G-IN-Mall | −1.15 to −1.65 | −1.99 / −1.70 on X-COP's gas; −1.33 / −1.15 on eRASS1's | HIT on eRASS1's, just out on X-COP's |
| G-MID | about −0.10 to +0.10 | T1 −0.69, T2 +0.39, T3 +0.71, b +0.93 | MISS, though all pass |
| Groups | back to +1.62 | +1.45 only with budget r₀ for groups; +3.84 with the zoom's r₀ | true only on the path it set out to replace |

The central point was right: FC1 and MA1 inflate mass at fixed budget, and the zoom's own r₀ survives ng 64. Parts of its derivation are scrambled in the copy I have.

## Checks
K1 NZ2 off against NZ1's ng 64 predictions |d| 0. K2 M_c(<R₂₀₀), M_c(<r_ta) 2e-16 on 1316 cells, no fallbacks. MUTATE r₀ × 1.5: see `nz2_MUTATE.out`.
