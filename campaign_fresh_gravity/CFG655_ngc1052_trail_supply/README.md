# CFG655: the NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647 ("Rogue One") as a cold-energy supply test

Criteria: `FROZEN_CRITERIA.md` (commit 0207b6abe, committed alone before the script). Script: `cfg655_trail_supply.py`
(seconds, one process, no downloads). Outputs: `.out`, `_results.json`, and the `_MUTATE` pair.

## Verdict: PASS, CONDITIONAL ON THE FORMATION-CHANNEL LABEL (both footings)

| galaxy | label (Rule P) | sigma_obs (km/s) | Newton | Z_N | law, no EFE (can / alt) | Z_law (can / alt) | framework Z (can / alt) |
|---|---|---|---|---|---|---|---|
| DF2 (20 Mpc) | E (collision debris) | 8.5 +2.3/-3.1 | 7.33 | +0.37 | 19.98 / 20.88 | -4.57 / -4.90 | +0.37 / +0.37 |
| DF4 (20.0) | E | 6.3 +2.5/-1.6 | 7.10 | -0.30 | 18.65 / 19.48 | -4.42 / -4.69 | -0.30 / -0.30 |
| DF9 (20.6) | E | 6.5 +3.9/-4.3 | 8.27 | -0.44 | 18.61 / 19.42 | -2.99 / -3.18 | -0.44 / -0.44 |
| LEDA 4014647 (17.7) | T (own supply) | 15.8 +/- 2.0 | 9.24 | **+3.11** | 17.37 / 18.09 | -0.74 / -1.07 | -0.74 / -1.07 |

- The supply rule puts every galaxy within 1.1 sigma. The law without supply (sigma_law, what a no-EFE modified-gravity law
  gives) fails DF2 and DF4 at 4.4-4.9 sigma and DF9 at 3.0-3.2 sigma. Newton-for-everyone fails LEDA 4014647 at +3.1 sigma.
- The verdict holds with DF2 at 16.2, 17.6 (JWST TRGB) and 21.7 Mpc (HST TRGB).
- **M1 (MUTATE): only 1 of the 16 possible E/T assignments passes** (the frozen one). The random-label pass rate is 0.062.
  **M2:** the cyclically shifted labels FAIL (max |Z| 4.6 / 4.9; exit 1, as required).

## What the PASS does and does not mean (read before citing)

1. **The framework does not derive which galaxies have supply.** The label comes from outside the framework: the
   2022 trail paper's pre-kinematic classification (DF2/DF4 trail members, DF9 "falls on the trail", LEDA 4014647 "a
   candidate for an interloper ... given its brightness and relative compactness"). The framework's own physical
   observables do not reproduce the label:
   - **Rule M (trail membership only):** LEDA 4014647 is on the trail list, so it is labelled E and fails at +3.11 sigma (3/4 pass).
   - **Rule A (age only, homogeneous SED ages):** the trail dwarfs are older than the 8-Gyr collision epoch (DF4 10.7, DF9
     10.4, LEDA 11.5 Gyr; DF2 8.3 is AMBIGUOUS). DF4 and DF9 are then labelled T and fail at -4.4 to -4.7 and -3.0 to -3.2
     sigma (1-2/4 pass). Vaz+2026's spectroscopic age (13.2 +0.4/-3.0 Gyr) separates LEDA more clearly, but its lower
     bound overlaps the others' SED ages.
   So this is not a free knob (the label is binary and was fixed in 2022, before the DF9 and LEDA dispersions), but it is
   an external input. Without it the framework cannot say in advance which trail galaxy is dark-matter-free.
2. **DF2 and DF4 are not out-of-sample.** CFG7 FG001 H6 (2026-09-27) already scored them as class E Newtonian (PASS).
   Also, the trail hypothesis that supplies the label was motivated by their low dispersions. The new information is DF9
   (Keim+2026) and LEDA 4014647 (Vaz+2026), each one galaxy.
3. **This test separates the framework from a no-EFE law, not from the dark-matter account.** In the framework the
   collisionless cold energy separates from the colliding gas exactly as dark matter does in the bullet-dwarf scenario.
   The framework's prediction is structurally the bullet-dwarf prediction with cold energy in place of dark matter. Because
   R7 removes the external-field effect, the EFE escape is not available here: without the supply mechanism (A5-A7, G9),
   DF2 and DF4 would be 4.4-4.9 sigma failures.
4. **Partial supply (R2, Theory v2 eq. 2-3):** if a collision dwarf had captured a fraction f_s of its law target, the
   measured upper bounds allow f_s <= 0.36 / 0.33 (DF2), <= 0.29 / 0.26 (DF4), <= 0.52 / 0.46 (DF9) (can / alt, at Z = +2).
   The framework has no derived capture rule. Embedded, collisionless capture with no dissipation gives f_s ~ 0 (A6, no
   pooling from the host).
5. **LEDA 4014647 (R3):** the measured Mdyn/M_* = 3 +/- 1 at r_1/2 sits beside the law's nu = 3.5 / 3.8. If it is a
   progenitor remnant (Vaz+2026's alternative), it could hold unsettled cold energy beyond its law target. Its sigma would
   then sit above sigma_law. It sits slightly below sigma_law, so the data give no sign of a surplus.

## Distance bracket (Z_N / Z_law / Z_framework, canonical; alt in the .out)

| | DF2 | DF4 | DF9 | LEDA 4014647 |
|---|---|---|---|---|
| all at 13 Mpc | +0.82 / -3.12 / +0.82 | +0.33 / -3.24 / +0.33 | -0.02 / -2.07 / -0.02 | +3.79 / +0.44 / +0.44 |
| all at 20 Mpc | +0.37 / -4.57 / +0.37 | -0.30 / -4.42 / -0.30 | -0.41 / -2.92 / -0.41 | +2.82 / -1.25 / -1.25 |

At 13 Mpc sigma_law still fails DF2 and DF4 at more than 3 sigma (canonical -3.12 / -3.24; alt -3.40 / -3.47), but DF9
then passes the law (-2.07 / -2.23). The supply rule passes at both distances. The TRGB/SBF distances (17.6-21.7 Mpc for DF2,
about 20 Mpc for the rest) exclude 13 Mpc.

## Secondary dispersions under Rule P (canonical; Z_N / Z_law)

DF2 MUSE stars 10.8: +0.85 / -2.74. DF2 GC system without the low-S/N outlier, 8.63: +0.58 / -3.72. **DF2 GC system with all
16 GCs, 14.86: +2.58 / -1.27.** With that outlier kept, the framework (Newton) is in 2.6 sigma tension and the law fits. The
source paper treats that GC's velocity as doubtful. DF4 stars 8.0: +0.43 / -4.07. DF4 GCs 4.2: -0.65 / -3.16.

## Data (no file downloads; read from arXiv abstracts or HTML; V = verbatim from the abstract or table)

| quantity | value | source | status |
|---|---|---|---|
| DF2 sigma_stars | 8.5 +2.3/-3.1 km/s (abstract v1: 8.4 +/- 2.1) | Danieli+2019, arXiv 1901.03711, body | V (published body value used) |
| DF2 R_e,circ; M_*(<r_1/2) | 2.0 kpc; 1.0 +/- 0.2 e8 Msun (at 20 Mpc) | same | V |
| DF2 sigma MUSE stars | 10.8 +3.2/-4.0 | Emsellem+2019, 1812.07345 | V |
| DF2 GC-system sigma | 14.86 +3.89/-2.83; 8.63 +2.88/-2.14 without the outlier | arXiv 2503.03404 | V |
| DF2 distances | 22.1 +/- 1.2 (HST TRGB, later quoted 21.7 +/- 1.2); 17.6 +/- 0.6 (JWST TRGB); 17.7 +/- 1.4 (SBF); 16.2 (GC sigma) | 2104.03319; 2606.05144; 2503.03403 | V |
| DF4 sigma | stars 8.0 +2.3/-1.9; fiducial 6.3 +2.5/-1.6; GCs 4.2 +4.4/-2.2 | Shen+2023, 2309.08592; vD+2019, 1901.05973 | V |
| DF4 R_e; M_*(<r_1/2) | 1.6 +/- 0.1 kpc; 7.5 +/- 2 e7 Msun | 2309.08592 body | V |
| DF4 distance | 20.0 +/- 1.6 Mpc (TRGB) | 1910.07529 | V |
| DF9 sigma; M_* | 6.5 +3.9/-4.3 km/s; 1.4e8 Msun | Keim+2026, 2603.15860 | V |
| DF9 r_e; D | 1.1 kpc (11.1"); 20.6 Mpc | same, body | V |
| LEDA 4014647 sigma; Mdyn; f_DM; age | 15.8 +/- 2.0; 1.5 +/- 0.4 e8; 0.7 +/- 0.1; 13.2 +0.4/-3.0 Gyr | Vaz+2026, 2610.07467 | V |
| LEDA 4014647 R_e,circ; log M_*; D | 601 +/- 48 pc; 7.98 +/- 0.06; 17.7 +/- 1.4 Mpc | same, Table 1 and Sec. 4.1 | V |
| SED ages t_M | DF2 8.28, DF4 10.68, DF9 10.36, LEDA 11.54 Gyr | Tang+2025b, 2410.19331 Table 2 | V |
| trail list and labels | 11 galaxies; DF9 "falls on the trail"; LEDA 4014647 "candidate for an interloper" | van Dokkum+2022, 2205.08552 (ar5iv HTML) | V |

Gas is taken as zero (gas-poor dwarfs). M_* = 2 x M_*(<r_1/2) where the paper quotes the enclosed value. No table file is
needed.

## Context only (never a verdict)

The dark-matter accounts are (a) the bullet-dwarf collision, in which the gas separates from collisionless dark matter,
DM-free galaxies form, and DM-dominated progenitor remnants survive, and (b) tidal stripping (DF4 tidal tails). Both
accommodate all four galaxies. The 2022 paper named RCP32 and DF7 as the candidate remnants, not LEDA 4014647. Vaz+2026
leave open whether LEDA 4014647 is an interloper or a remnant. The framework predicts the law value in either case.

## Prior record

CFG7 FG001 H6 (DF2/DF4 class E PASS at 20 Mpc), CFG58 (blind mass-only rule fails DF2/DF4), CFG441 (no old TDG with
kinematics; DF2/DF4/DF9 at about 8 Gyr are now the oldest supply-free systems with kinematics in the record, if the
collision origin holds), CFG392 (metallicity-selected old TDGs: non-discriminating), hunt_2026 h8 item 42.

kappa = 1/2 fitted; cold energy mass required; not theory closed.
