# CFG338: cold share from pre-reionisation baryons

**Frozen verdict (1st commit of this lane): NOT.** The frozen primary was reading M with profile PB (the whole cold share inside r). It overshoots all five populations by -0.45 to -0.74 dex.

**Reported row, decided on after the freeze: reading M with profile P1.** P1 is CFG313 V2 / CFG336 primary collapse profile, with z_f 8 for UFDs and 3 for the rest. Under it, all five dwarf populations land within 2 sigma on both footings:

| population | offset (dex) | sigma |
|---|---|---|
| UFD | -0.016 | 0.14 |
| MW classicals | -0.15 | 1.2 |
| M31 Collins | -0.13 | 1.1 |
| M31 LVD | -0.07 | 0.8 |
| LV field | -0.05 | 0.6 |

The cold share uses R_ind, the CFG317 leaky-box baryon-loss factors measured independently of dynamics: 117 / 30 / 22 / 22 / 6.

This row is POST HOC and is NOT the frozen verdict. It is confirmed only by a separately frozen robustness lane, CFG339.

## Controls
- **C1 passes:** with R_ind = 1 the run reproduces the CFG336 M|PB row.
- **MUTATE passes:** with R_ind permuted across populations, the P1 row breaks (UFD +0.22, LV field -4.3 sigma). So the match needs each population own measured loss.

## Files
- `cfg338_base_cfg336rows.*` are the inherited CFG336 rows printed by the copied harness.
- Run: `python3 campaign_fresh_gravity/CFG338_preionisation_cold_share/cfg338_preion.py` (CFG338_MUTATE=1 for the control).
