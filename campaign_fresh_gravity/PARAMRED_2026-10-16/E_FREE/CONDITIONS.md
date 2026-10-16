# Necessary conditions on any rule for the free (untethered) cold-energy component

Lane E (FREE), 2026-10-16. Every row is read from the ledger row (or the lane README it points to) of the cited CFG id; no number here is
re-derived unless marked "(lane E)". IDs match FROZEN_CRITERIA.md section 1. kappa = 1/2 FITTED; canonical a0 = 9.3603e-11, alt 1.1312e-10, never pooled.
"Free" = collisionless cold energy the cubic tether push does not act on (S4). Footing is canonical unless stated.

## A. WHERE the free mass must sit

| ID | Necessary condition | CFG | Quantitative margin (as recorded) |
|---|---|---|---|
| W1 | In clusters the excess lives in the MID band (0.48-1.24 Mpc); the OUTER band (1.2-3 Mpc) is already matched by the tethered law | 687, 686 | eRASS1 (318): A_MID 1.91 +- 0.12 / 1.75 +- 0.11 (x1.8, 7 sigma), A_OUTER 1.01 +- 0.09 / 0.93 +- 0.08; ACCEPT (8): MID 1.70 +- 0.35, OUTER 1.02 +- 0.24 / 0.94 +- 0.24 |
| W2 | The INNER cluster band must not be overfilled; the framework's own splashback caustic of free cold energy sits INNER, so it cannot fill MID | 727, 818, 819 | A_INNER 0.31 (over-predicted, ungraded; heavy tercile ~6x over); caustic 0.17 Mpc (0.03 r_ta, middle) / 0.43 Mpc (0.07 r_ta, heavy), free half-mass ~2 Mpc; unrelaxed vs phase-mixed placement differs <= ~5% (null mechanism) |
| W3 | The persistent excess is UNTETHERED: surplus tethered cold energy is dynamically unstable | 776, 777 | Surplus expelled in ~50-100 t0 and overshoots to a deficit (m/r 0.30-0.50 at 5-11 r_M by 50 t0; 0.44-0.77 at 3000 t0); KiDS early types pred -0.081/-0.079 vs +0.280, Z +4.35/+4.33; clusters 0/3 (A_MID 0.66-0.81 overshoot, ACCEPT A_OUTER ~0.34, Z -8) |
| W4 | Early types: excess sits at 50-100 kpc at matched M_b. Carrier colour vs structure undecided. AGE is NOT a condition | 669, 721 (colour row), 667, 585 | Ks +0.280 +- 0.083 dex (Z 3.4; caveat: constant M/L_K may inflate by 0.05-0.15); colour split +0.220 +- 0.030 (Z 7.4), Sersic +0.181 +- 0.029 (Z 6.2), difference 1 sigma; age: Ks +0.082 (Z 0.9) not robust, Taylor re-match +0.032 +- 0.080 (Z 0.4) |
| W5 | UFDs: free mass acts inside the dispersion-estimator radius; it is not tidal | 28, 327 | beyond 80 kpc +0.325 +- 0.029 vs +0.322 inside, rho -0.22 (p 0.23); tidal susceptibility rho -0.17 (p 0.81) |
| W6 | Galaxy halos: outer mass needs a supply without a sharp settled edge; the catchment supply (N = 1/f_ret) suffices to 0.31 Mpc | 801, 804 | settled edge 5.84 r_M (44-90 kpc) EXCLUDED, dchi2 +197 primary, +753 all radii; derived supply dchi2 -0.2 / -1.5 (R <= 0.31 Mpc), +149 / +172 beyond ~0.4 Mpc (two-halo, not modelled) |

## B. HOW MUCH, per system class

| ID | Class | Necessary condition | CFG | Quantitative margin |
|---|---|---|---|---|
| A1 | UFD (MW, N = 30 with limits) | extra mass beyond the law | 28, 259, 336, 317 | +0.325 dex KM median, 3.5-3.9 sigma after the Upsilon_V floor 0.077 dex; 2026 dispersions move it -0.003..+0.005; law phantom exceeds the native cold share (5.364 M_b) by x3.5 median in all 40 UFDs; leaky-box log R_ind 2.07 vs R_need log 3.65 (1.58 dex short, "NOT SUPPORTED") |
| A2 | Early types, log M* 10.8 | free mass 0.55-0.80 M* inside 100 kpc | 745, 669 | k M_hot with M_hot 0.17-0.25 M*; early-late differential +0.280 +- 0.083 at matched M_b |
| A3 | Clusters | missing mass beyond the law | 687, 745, 815, 817 | eRASS1 x1.8 inside ~1 Mpc; X-COP missing mass 3.0 (1.9-4.5) M_b canonical, 2.74 alt; after H-EX the terciles are 1.21 / 1.64 (Z +4.6) / 0.90, and after count-rate selection modelling 1.27 / 1.59 / 0.96: middle-tercile shortfall x1.6 REAL (Eddington effect 0-10%) |
| A4 | Groups | at most a little | 745, 727 | shift +0.026..+0.072 dex against the 2-sigma line 0.0645 (TENSION at one end); eFEDS chi2 18.7-19.9 / 8, p 0.011-0.017 without free mass at galaxy scale |
| A5 | Late types / SPARC | zero free mass | 695, 658, 721 | rms 0.1009 / 0.0994 dex with nu_s; no SPARC point touched by overflow (max R_last/r_edge 0.20) |
| A6 | Massive clusters (ACCEPT) | must not be overshot | 727, 815 | A_OUTER 0.48-0.50 (Z -3.8..-4.3, x2 overshoot) under the hot-gas rule; 0.42 / 0.32 under H-EX; two low-z 2PIGG groups carry 43% of the weight |
| A7 | Bullet | free fraction of the core ~0.75-0.80 | 724, 725 (via THEORY_v3 P3), 721 | overflow reaches main <= 0.79, sub <= 0.11 of the core requirement (FAIL) |

## C. What the rule must NOT do

| ID | Prohibition | CFG | Margin |
|---|---|---|---|
| N1 | Young tidal dwarfs stay Newtonian; old tidal dwarf NGC 5557-E1 decides capture vs clock | 441, 763, 785 | young TDGs: Newton chi2 1.10 (6 dof) vs law+EFE ~34 (dchi2 +33/+39); E1: Newton 16-24 vs law 28-41 km/s (needs +-4); clock tau_min,95 0.72 (can) / 0.83 (alt) Gyr, SPARC discs tau <= 3.47 Gyr; CFG785 is frozen criteria only (no output on disk) |
| N2 | No capture channel for cold energy falling in | 744, 760-762, 749 | cold-medium wave export needs c_P 20-220 m/s -> relaxation >= 5.0 Gyr (FAIL); P-radiation closed 16/16 cases, margins 1.4-1740; one c_P for all SPARC: gap x182 / x171; orbiting cold energy at >= 0.3 V_flat has E > 0 |
| N3 | Collisionless, no instant response (Bullet) | 725, 720, 722 | sigma/m <= 0.708 cm2/g (both footings); bound charge div P has zero net mass (+23.9 M_b interior, -23.9 M_b shell) so cannot be the cold mass; a real carrier is a new species (open; rule: stop that branch) |
| N4 | Conserved budget: supply = 5.364 x own-catchment baryons, own host only, so a free fraction F <= 1 | 647, 804, 727 (control C1) | pooling puts 10% (13.5% for log M_ta >= 13.5; 28% at z = 1) of settled mass above the host's own supply; N = 5.6-10, edges 320-450 kpc; free + settled = supply holds (C1 PASS) |
| N5 | Not tether overflow | 721, 722, 724 | H-OF = H-OF2 to 0.0 (the law's phantom never reaches a0/(pi G)); eRASS1 MID 1.90/1.74 (7 sigma), eFEDS p < 0.002, early types Z 3.3-3.7 |
| N6 | Not P-wave export or heating | 741, 760-762 | heating ratio Q <= 0.50, scale-free (galaxies 0.09-0.27); export closed (above) |
| N7 | Cold-to-DE conversion costs growth: a rule that drains the settled halo must not add to it | 780, 779 | T1x chi2 136.56 -> 141.23 (+4.66, ~60% of the gain; dchi2 vs control -7.70 -> -3.03, still CONSISTENT); T12 146.29 -> 152.56 (+6.27, TENSION +8.30); half amount NEUTRAL; BH->DE needs survival 0.894 (P2 30% eaten EXCLUDED 7.8 sigma, cold-only CONSISTENT 0.9 sigma) |
| N8 | Solar System and wide binaries (constrain the tether/stiffness; a distant free halo is not constrained on record) | 770, 740, 691 | Cassini |Q2|/ceiling 2.2-3.5e-6 at L* = 5.75 pc; gamma_v - 1 <= 8.9e-4 at 50 kAU, slope 2; L* >= 5.75 pc, SPARC fine to >= 1000 pc |
| N9 | A universal expelled-share rule at galaxy scale is excluded on both sides | 810, 811 | F = 1: all-radii dchi2 +443 vs B+2h (primary +136), 25-48 M_b free; early-late predicted +0.013 vs +0.280 (Z +3.2), would need r_f ~ 9.6 vs 1.5 |
| N10 | Already failed or null origins | 726, 812, 818, 819, 727, 808, 809, 813-815 | merger memory sqrt(N) - 1: ETG +0.115 vs +0.280 (2-sigma line), eRASS1 OUTER 0.76 / ACCEPT 0.45 overshoot; impulsive unbinding bound fraction 1.000 (min 0.968) = null; hot-gas rule 2/4; H-EX 76-cluster CONFIRMED (MID 1.08 +- 0.14, OUTER 0.94) but 318-cluster FAIL (MID 1.18, OUTER 0.83, middle 1.64, ACCEPT 0.42) |

## D. What the free fraction can SCALE with

| ID | Variable | CFG | Margin |
|---|---|---|---|
| S1 | Hot-gas mass: C = k M_hot | 745, 746 | k = 2.88-3.62 (X-COP, four brackets); state-blind k M_b FAILS groups (MUTATE bites); SEALED: M_hot(<100 kpc) 1.1-1.6e10 M_sun at log M* 10.8, falsifier less than half |
| S2 | Host temperature: V_init < sqrt2 c_s(T_IGM) | 782 (DEAD) | UFD 1.00 (0.97 at 1e4 K); M31 Collins 0.50, LVD 0.52 (0.36 / 0.28 at 1e4 K) against a 0.10 ceiling; classicals 0.00; field 0.08; SPARC 0.00; V_th 16.73 / 20.49 / 23.66 km/s at 1 / 1.5 / 2e4 K |
| S3 | Binding in the tether frame | 749, 812 | cold energy is bound only by baryons (v >= 0.3 V_flat unbound); freed at-rest cold energy stays bound: fraction 1.000 in 11/12 clusters (min 0.968): binding does NOT select |
| S4 | Settling time vs removal time | 743, 747, 748, 776 | settle 0.05-1.36 Gyr for M_b <= 1e11 (2.1-2.4 Gyr vs 1.38 only at M_b 1e12, y 0.1); inner halo within 0.2-1.7% with no dissipation; fills to 20 r_M (0.996), 0.945 at 50 r_M |
| S5 | Mass inside a class | 687, 815, 817 | outer shear ~ M_gas^0.90 +- 0.21 (law 0.47, Newton 0.84); tercile pattern non-monotonic |
| S6 | Formation clock | 763 | tau in [0.72, 3.47] Gyr (tethering of cold energy formed at rest), window OPEN |
| S7 | One universal multiplier (prior art) | 59 | the older "one phi" test: NO on both footings, SLUGGS phi >= 0.81 vs M31 LVD phi <= 0.30 (gap 0.51 / 0.46); X-ray ellipticals have no phi in [0, 1] |

## E. Post-freeze additions (disclosed)
CFG59 (prior art on one universal multiplier), CFG91 (M31 LVD law offset +0.0435 dex: a population median, dominated by brighter dwarfs, so it does not
score the faint flagged ones), CFG327, CFG317 (R_ind estimator and its failure) were added to the table after FROZEN_CRITERIA.md. None changes a
frozen rule; CFG317 was already a frozen T1 input.

## F. Which conditions conflict (all margins from `e_free_results.json` unless marked "ledger")

| pair | conditions | outcome |
|---|---|---|
| P1 | A2 + N4 (CFG745, CFG804) vs A3 + N4 (CFG745, CFG814) under one universal F | EMPTY: F_E in [0.0114, 0.0324] vs F_C in [0.619, 1.0], gap x19.1 |
| P2 | N9 (CFG811) vs W4/A2 (CFG669) | universal rule gives +0.013 vs +0.280, Z 3.22; frozen linear form needs F 15.2-27.9 against the cap 1 |
| P3 | A1 + S2 gates (CFG28/259 vs CFG782 S1/S2 with CFG317 inputs) | window EMPTY for every multiplier and every T_IGM: S1 needs V_th > 15.09 km/s, S2 needs <= 11.43 km/s (L/U 1.320; alt 15.82 / 11.99) |
| P4 | A3 middle tercile x1.59 (CFG817) vs N4 cap (CFG647/804) given W2 (CFG818/819) | ledger-derived, not recomputed: H-EX already uses F = 1; the shortfall cannot be filled by more mass or by moving it |
| P5 | A6 + A3 (CFG727, CFG815) | no single source rule passes eRASS1 and ACCEPT; the tercile pattern 1.27 / 1.59 / 0.96 is non-monotonic in mass: a second variable is needed (S5) |
| P6 | N1 (no capture, S4) vs S6 (clock, CFG763) | not a conflict for young TDGs; they differ for OLD ones (clock >= 68% filled at 4 Gyr vs 0 forever): NGC 5557-E1 decides |
