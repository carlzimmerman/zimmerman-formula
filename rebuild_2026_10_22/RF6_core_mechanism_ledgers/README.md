# RF6_core_mechanism_ledgers: CM1'S NOT REACHED IS THE FIDUCIAL INPUT'S, NOT ROBUST, BUT ITS REACH NEEDS COUPLING ABOVE 0.3. CL5'S IS ROBUST ON MEASURED GAS. THE NEED ITSELF MOVES MORE THAN EITHER

Criteria and ledgers: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md`, `ledgers/` (0b8131bb50), committed first. Script `rf6.py` (02c22adfc3). Numbers: `rf6.out`, `rf6_results.json`, `runs/`. Control: `rf6_MUTATE.out`. The seven lanes' files are unedited. CE1/BE1's converged-η failure isn't touched and stays the governing result. A "reached" here isn't a pass, and it isn't a derivation.

## Verdicts
| lane | input | verdict |
|---|---|---|
| **CM1** (re-run) | moved gas | **NOT REACHED only at the fiducial input; reached at M_f = 0.0306, 2.2 × today's gas, ε_SN 1.61, inside its range at coupling 1, outside at coupling 0.3** |
| **CL5** (re-run) | gas in the core | **NOT REACHED, robust to the ledgered ranges.** Reached only at M_f 0.0566, 3 × the largest measured, on the same-gas control only |
| CM2 | cadence | NOT REACHED only at the fiducial input; reached at 1 Gyr (R 0.573), outside what I recall for this mass; from memory, not on disk |
| CM3 | coupling | NOT REACHED only at the fiducial input; reached at coupling 1, outside the ledgered realistic coupling; 0.3 misses at every cadence mapped |
| BH1 | central gas | NOT REACHED only at the fiducial input; reached (BH2) at a load of 0.02–0.05 M₂₀₀, outside the closed box and the model's own hot-gas cap |
| BH2 | load | REACHES LIMIT only at a stipulated load, 4–11 × the in-place cap. No measurement of it |
| SH1 | R at clusters | SOFTENED FAIL stands at R = 1 on clusters. Its one pass rests on R 0.685 there, granted; nothing here supplies it |

## CM1, 40 bursts, 250 Myr, frozen need R ≤ 0.817
| cell | M_f / M₂₀₀ | R | ε_SN |
|---|---|---|---|
| committed PRIMARY, today's median gas | 0.0140 | 0.932 | 0.76 |
| E1, fiducial E_SN cap | 0.0185 | **0.881, misses** | 1.00 |
| GASHI, 84th percentile gas | 0.0306 | **0.715, reaches** | 1.61 |
| E3, top of the E_SN range | 0.0616 | **0.364, reaches** | 3.00 |

At fiducial E_SN and coupling 1 it still misses. The reach needs more than the fiducial supernova energy, all of it spent lifting gas. Every reaching cell is outside the range at coupling 0.3 (ε_SN ≤ 0.9). The E_SN range × 0.35–3.0 is from memory, and its top stacks three favourable factors. GASHI puts a gas-rich galaxy's gas fraction into the median galaxy, with all of that gas starting at the stellar scale, so it's a ceiling.

## CL5, N 10, a_f 0.05, frozen need 0.846 (10¹⁴), 0.809 (10¹³)
| M_f | 10¹⁴: R, same-gas R, share of E_AGN | 10¹³: R, same-gas R, share |
|---|---|---|
| 0.0186, largest measured | 1.025, 0.947, 0.62 | 1.026, 0.947, 0.14 |
| 0.0283, CL5's ceiling (committed) | 1.025, 0.917, 0.95 | 1.026, 0.910, 0.21 |
| 0.0566, outside measured gas | 0.921, 0.744, 1.92 | 0.951, 0.764, 0.42 |

**CL5's own ceiling was above the data.** Its round gas model caps M_f at 0.0283. X-COP's measured gas gives 0.0086–0.0186 (`rf6_setup.json`), read at about 6 × 10¹⁴ M☉, above these two masses. No lensing or X-ray core gas was read at 10¹³–10¹⁴ here.

## The need, as a band
**SPARC, footing by footing, R_need from Υ(η) on background A:**
| Υ floor | canonical | canonical, cold-share η | alt | alt, cold-share η |
|---|---|---|---|---|
| 0.44 | no softening needed | same | 0.817 | 0.972 |
| 0.50 | 0.908 | 1.081, none needed | unreachable by softening | same |
| 0.57 | unreachable by softening (Υ tops out at 0.56) | same | unreachable | same |

The frozen 0.817 isn't where this table puts Υ 0.50. Υ is rounded to 0.01 in the committed JSONs and η 21.19 reads 0.52, so 0.908 is rough. At 0.908 canonical, E1 (0.881) reaches at fiducial energy, coupling 1, and today's median gas still doesn't (0.932). On FC1's bookkeeping, no softening is needed at Υ 0.50. So **on canonical the SPARC question depends on the Υ floor and the bookkeeping more than on the outflow.** The Υ rows carry the a₀ floor the owner removed on 10-31; on native N, ND1 has SPARC's line passing. Alt's failure at 0.50 is the law's (X78), and softening can't fix it.

**Clusters, R_need against the limit 14.3:**
| η used | 10¹⁴ | 10¹³ |
|---|---|---|
| ng 48 (CL5) | 0.846 | 0.809 |
| ng 64 | 0.647 | 0.607 |
| ng 48, cold share | 1.006, none needed | 0.963 |
| ng 64, cold share | 0.770 | 0.723 |

On ng 64, which is the current η, measured gas misses in every bookkeeping, and M_f 0.0566's same-gas 0.744, 0.764 meets only 10¹⁴ on the cold share. On the superseded ng 48 cold share, the same-gas 0.947 clears 10¹³ and 10¹⁴ needs nothing. FC1's A4 read, COLD-SHARE FAIL at ng 64, is the one that stands. The limit 14.3 is G-IN-Mall's on eRASS1's gas, and RF3 shows that gas scale is open.

## Limits
- One spherical halo, one seed, prescribed gas histories, halo formed at t = 0. No cooling, metallicity or gas physics is simulated: they aren't inputs, so nothing here tests them.
- R is measured at x_c 0.013–0.017 and applied to x_c 0.001 values (X81).
- E_SN, M_BH/M★, realistic coupling and cadence ranges are from memory, PROVISIONAL. A range read from the papers could move an inside/outside label.
- I chose the scanned inputs after reading the lanes' numbers, as the criteria disclose.
- Five lanes read committed numbers only.
- CL5's frozen STATIC is biased against softening (control/STATIC above 1). Both R are given. Its frozen R misses in every cell.

## Checks
K1 wrapper against CM1 PRIMARY and CL5 M14_e1 first marks, |d| 0. K2 work balance ≤ 2.7e-5, all done. K3 E1's ε_SN 1.000. K4: Υ(η) is read directly from the committed JSONs. MUTATE (× 0.1): CM1 E3 R 0.967 against 0.364; CL5 X2 R 1.018 against 0.921; neither reaches: BITES. One thread, nice 15, three processes.

    python3 rf6.py setup; python3 rf6.py runall; python3 rf6.py grade; RF6_MUTATE=1 python3 rf6.py runall; RF6_MUTATE=1 python3 rf6.py grade

κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
