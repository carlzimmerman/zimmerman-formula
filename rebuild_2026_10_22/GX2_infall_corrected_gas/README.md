# GX2_infall_corrected_gas: correcting eRASS1's gas masses does not rescue the cluster halo shape

Criteria: `FROZEN_CRITERIA.md` (c6783290b3, committed alone, before any script or number); no amendment.
Harness: GX1 Stage B / GS1, executed read-only, with the halo edit and a gas-factor edit.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **LENSING STILL FAILS** (canonical and alt)

eRASS1 Mgas500 is raised by SM1's matched +0.111 dex:

| halo | lensing (15 keys × 2 h cells) |
|---|---|
| Burkert, no correction (Step 0 = GS1 R4) | **all pass** |
| **PRIMARY: infall, splashback edge, gas +0.111** | **FAIL, OVER**: MID-T1, MID-T3, OUT-all, OUT-T1, OUT-T2, OUT-T3, OUT-Mall, OUT-M2, OUT-M3 |
| V1: infall, edge r_ta, gas +0.111 | FAIL, UNDER: MID-T3, OUT-Mall, OUT-M3 |
| V2: Burkert, edge r_ta, gas +0.111 | FAIL, OVER: 9 MID/OUT keys (GS1's pass is lost) |
| PRIMARY, gas +0.111 ± 1σ | FAIL, OVER |

## Reading

- **The correction breaks the lensing pass instead of repairing it.** Raising the gas budget by 23 % pushes every
  halo over the lensing outskirts. That includes GS1's Burkert pass.
- **The record's lensing pass is tied to eRASS1's own gas scale.** That is consistent within one sample's definitions,
  but it means the X-COP-calibrated gas cannot be fed to the lensing sample without breaking it.
- **The cluster halo shape stays an open failure.** No tested halo passes both X-COP (its own gas, ≤ 0.7 R500) and the
  lensing outskirts. SM1 shows the two constrain different radii and masses, and they disagree on the gas scale by
  0.11 dex.

## Checks: 2/2

- **K0:** GS1 R4 reproduced.
- **K1:** the factor is 10^0.111.
- **Rerun:** byte-identical.
- **MUTATE twin** (factor applied twice): K1 fails, exit 1.
