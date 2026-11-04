# FN6_powerlaw_screening: frozen criteria

Committed alone, before any script or number. The owner said "keep going on action" (2026-11-04), after choosing on the same day not to select an action yet (FN1, option c). This lane looks for what an action would have to produce. It adopts nothing. kappa = 1/2 FITTED, held fixed. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. Not theory closed. Nothing here says the data favour the framework. No cold component, no particle.

**Not blind.** AX1, C6P, FN1b, KT16, KT17, KT25, CZ1-CZ5 and CFG820/CFG821 were read first.

## Question
Does a screening length that scales as a power of the system's baryonic mass, L(M) = L_MW (M / 6e10 Msun)^p, pass all five static gates on either footing? The gates are the Milky Way cells, the 24 Local Group dwarfs, Cassini, the planets and SPARC. The form graded is the reciprocal one (R), the static limit an action with a fixed kernel gives (FN1b).

## Why this family
- AX1: no unscreened action gives the law and passes Cassini's Q2. A length that screens each mass is the record's only way past it.
- p = 0 (one universal length) fails: the dwarfs pass only up to 0.1 kpc, the Milky Way only at 2 kpc (FN1b).
- p = 1/2 (L = epsilon r_M) fails Cassini with the Newtonian external field: KT25 1.18x canonical, KT17 1.54x alt (CZ1/CZ2).
- v3s's screened core scales as L*^2/(2 r_M), so p = -1/2, and passes the Solar System (C6P).
- Hand estimate, written now: with L_MW about 2 kpc, a dwarf of 1e7 Msun gets 0.1 kpc or less only if p is at least about 0.35. The Sun then gets about 0.3 pc, far above its MOND radius (0.034 pc), so it is screened. If so, wide binaries would read Newtonian at every separation.

## Grid (frozen)
p in {-0.5, -0.25, 0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.75}; L_MW in {1.0, 1.5, 2.0, 3.0} kpc. M is each system's own baryonic mass: each Milky Way cell's, each dwarf's, the Sun's, each SPARC galaxy's.

## Gates
FN1b's engines and frozen lines, unchanged: T0 Milky Way (KT14's four lines, at least one in-prior cell), T1 Cassini, T2 dwarfs, T3 SPARC, T4 planets. Only the length per system changes. Where a system's L falls outside FN1b's evaluated range, the same engine is run at that L.

## Known answers
- KA1: p = 0, L_MW = 2.0 reproduces FN1b's 2 kpc row on each gate exactly.
- KA2: p = 1/2 with L = r_M / 2 reproduces CZ2's KT25 Cassini ratio, 1.18x canonical, within 1 %.
- MUTATE: the masses are shuffled among systems before L is assigned. A window that survives the shuffle isn't a mass scaling and is reported as such.

## Labels, per footing
- **WINDOW**: at least one (p, L_MW) grid point passes all five gates. Reported with the passing points, their count of 48, and the shuffle result.
- **NO POWER-LAW LENGTH PASSES**: no grid point passes all five.
- **NOT EVALUABLE**: a known answer fails.

A window is a two-number description, not a derivation. Look-elsewhere: 48 grid points per footing, stated beside any window.

## Reported, not graded
For any passing point: the length at 1 Msun against wide-binary separations, and the DR4 gamma_v it implies through CW1's frozen pipeline (read only), as a prediction. The scaling exponent p beside known screening mechanisms (a Vainshtein radius scales as M^(1/3)), as a reading only.

## Compute and timing
FN1b's scripts imported read-only; one thread; FN1b peaked at 1.3 GB, stated if exceeded. Frozen on 2026-11-04 with the account's weekly usage at 88 %; it runs after the usage reset.
