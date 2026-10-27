# X58_object_keyed_switch: a mass-keyed switch fails; dwarfs need halos, lensing galaxies need the law, clusters need halos

Criteria: `FROZEN_CRITERIA.md` (9964127dfd, committed alone; owner request 10-27). Machinery: X56 (526db8a12f), each scorer
in its own process. No amendment. κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter. Not "theory closed".
Nothing here says the data favour the framework.

**Hypothesis SW:** per system, if η Σ_coll(M200) > Σ_a₀ (X43's flag), use route E: Newtonian gravity plus the collapse
halo. Otherwise use the law on the baryons, with no halo.

## Verdict (frozen): **SW FAILS** on both footings

| line (primary, X48 ng 48 c_f) | canonical | alt |
|---|---|---|
| SPARC | 0.0623 @ 0.56: PASS | 0.0620 @ 0.50: PASS |
| groups | Z +1.53: PASS | Z +1.53: PASS |
| clusters | 14/15; **G-IN-Mall OVER** (−2.41): the X48 miss | same |
| dwarfs (law) | **MW UFD UNDER Z +5.22**, bright M31 +2.20, M31 others +2.29 | **UFD +4.87**, M31 others +2.12 |
| lensing Δχ²(SW2H − L2H) / (SW2H − H2H) | **+432.5** / −0.5 | **+452.3** / −10.0 |

**Reported: c_f = 4.** The crossover is 10^12.09 / 10^12.43.
- **Lensing** comes back nearly to the law: +22.5 canonical (fails the ≤ 9 gate), 0.0 alt.
- **Clusters:** G-IN-Mall passes, but G-OUT-M3 fails (+2.41).
- **Groups:** ABOVE LAW on canonical (Z +2.02).
- **Dwarfs:** fail exactly as in the primary.

**Checks 7/7.**
- K0 and K2 as X56.
- K1: every one of 12 430 system calls equals its flagged branch.
- K3: 0.65 GB maximum over processes.
- `--mutate` (flag inverted) fails K1 on every call, exit 1.

## What it means

1. **The native c_f puts the crossover below the lenses.**
   - With c_f(ng 48) ≈ 7, η ≈ 30, and most KiDS lenses (log M200 11.35–12.05) are flagged collapse-cored. So lensing is
     route E's (+432).
   - Lensing wants the law in exactly the halos that native c_f puts on the collapse branch.
   - At c_f = 4 the conflict nearly goes away. So the switch's lensing outcome rests on the unconverged c_f.
2. **Dwarfs need halos, not the law.**
   - Under the isolated law the ultra-faints are under-predicted by 0.55–0.59 dex (X1/X24's old miss).
   - X51's route-E cooling-floor halos fit them on canonical.
3. **The requirement is not monotone in mass:** halos for dwarfs (10⁸–10¹⁰ M☉), the law for lensing galaxies
   (10¹¹·⁵–10¹²), halos for clusters (≥ 10¹³). No single mass threshold can produce that ordering, so a one-crossover
   object-keyed switch is excluded. Any surviving key must separate the dwarfs from L* galaxies by something other than
   mass, for example environment (most graded dwarfs are satellites) or formation epoch.

Graded lines: `x58_law_floor.out` / `x58_law_floor_results.json` (the output name was inherited from X56; script `x58_switch.py`).
