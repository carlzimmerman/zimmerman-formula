# CZ1_newtonian_external_field: NUMBERS ONLY (frozen Label A read NO DEFECT on a tolerance miss)

Criteria `FROZEN_CRITERIA.md` (90c548c6cf), committed alone before the script. Run `OMP_NUM_THREADS=1 python3 -I cz1.py`, output `cz1.out` / `cz1.json`, MUTATE twin `cz1_MUTATE.*`. Peak RSS 0.22 GB. Checks K1 (KT27 reproduced exactly, both footings), K3 (KT27's Cassini 0.481 / 1.06 reproduced) and Part D's FD1 reproduction all pass; 0 failed.

κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework.

## Why there are no labels
Label A needed the KT form to miss McGaugh–Milgrom's external-field limit by more than 30 % **and** the corrected form to sit within 10 % of it, both at y_Ne = 0.01. The KT form misses by a factor 0.381. The corrected form sits at 1.105, which fails the 10 % line by half a point. The gap is exact: ν/(ν − 1), the 1D quadrature total against the asymptotic a0/g_e. So the frozen label is **NO DEFECT**, and under the criteria Parts B and C are reported without labels. The `LABEL B` lines the script prints are not verdicts. See `AMENDMENTS.md` (post-result).

## Numbers
**Part B, 24 dwarfs, pass counts out of 24** (E0 = KT lanes' MOND field in ν; E1 = MW Newtonian field, the only change; E2 = MW + M31 Newtonian vector sum, UNGC positions):

| footing | variant | plain | ½ r_M (KT25) | 0.55 r_M (KT17) | local ξ_loc (KT27) | Fornax, local, km/s (obs 11.7 ± 0.9) |
|---|---|---|---|---|---|---|
| canonical | E0 | 15 | 15 | 15 | 14 | 5.00 |
| canonical | E1 | 18 | 18 | 18 | 17 | 11.94 |
| canonical | E2 | 17 | 17 | 17 | 16 | 11.92 |
| alt | E0 | 15 | 15 | 15 | 14 | 5.07 |
| alt | E1 | 18 | 18 | 18 | 17 | 12.52 |
| alt | E2 | 17 | 17 | 17 | 16 | 12.49 |

- E1 gains Sculptor, Carina and Leo II in the plain and constant arms. The local arm gains Sculptor, Leo II and **Fornax**.
- E2 also loses Andromeda I, whose M31 field rises from 0.
- With the Newtonian field, the local rule's dwarf row sits one below plain, as the constant arms' rows do. KT27's only alt failure was this row: 14/24 with Fornax at 5.1 km/s.

**Part C, Cassini, Q2 over KT16's ceiling** (observed Galactic field 2.32e-10 in ν → its Newtonian part from the law inverted: η 2.479 → 1.766 canonical, 2.051 → 1.379 alt):

| footing | ½ r_M | 0.55 r_M | local |
|---|---|---|---|
| canonical | 0.481 → **1.179** | 0.247 → 0.608 | 0.0005 → 0.0039 |
| alt | 1.057 → 2.97 | 0.544 → **1.539** | 0.0021 → 0.0215 |

The same correction **hurts** Cassini by about 2.5×. KT25's ε = κ on canonical, the record's only filter form passing all four rows, goes over its ceiling (1.18×). KT17's ε 0.55 goes over on alt. The local rule stays 50–250× under the ceiling on both footings.

**Part D, IC 1613:** Newtonian Local Group field 3.4e-4 / 2.8e-4 a0, against its own 0.030 / 0.025. E shifts by +0.00001 dex, Z −3.85 / −4.47, unchanged. The external-field lever in `FAILURES_LITERATURE_REVIEW_2026-10-28.md` §1 is closed: it had compared a MOND external field with a Newtonian internal one.

**K2, reported:** with M_MW,b 7.0e10, the law's own MOND field is 14–17 % under (200 km/s)²/D at 76–250 kpc. UNGC's M31 baryons (0.6 L_K + 1.33 M_HI) come out at 3.9e10 M☉, low against common literature values. This only affects E2.

## What this means, and what it doesn't
- Read together, the numbers say the record's verdicts on the filter forms flip. ½ r_M on canonical loses Cassini. The local rule on alt loses its only failed row: KT26 MW pass, KT27 Cassini and SPARC pass, and now dwarfs 17/24 with Fornax. That's a reading of unlabelled numbers, **not a pass**. It needs its own frozen re-grade before it can be cited.
- The 1D quadrature form ignores QUMOND's anisotropic factor, in the KT lanes and here alike.
- KT26's MW pass for the local rule sits at prior-corner cells (KT18/KT22 thick-share caveat). The MW and SPARC rows carry no external field and weren't rerun.
- KT28, the tidal filter rule, uses the same `ge = 200²/D` form in its dwarf and Cassini rows.
