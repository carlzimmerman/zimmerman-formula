# FRZ2 RESULT: the forest row with a0 allowed to change with z

**NO FRAMEWORK a0(z) PASSES.** Every case fails the forest gate on both footings, including every power law.

TEST lane. Criteria 15b54906a0. Footings graded separately, never pooled. Cold dark energy is a gravitating field
component; no particle is added. Known answers pass and the mutation bites.

## What came out
- a0 rising with z does turn FRZ1's power deficit into an excess, but the crossing is not hit by any frozen case.
  P0.5 (a0 ~ (1+z)^0.5) is closest: 252 / 167, still 40-60 times over the gate. P1 already overshoots (R_cold > 1).
- The dark-energy density cases (D) lower a0 at z 3 (f 0.71-0.78) and make the deficit worse: ~13,400-14,900.
- The minus-pressure cases (Q) leave a0 almost unchanged at z 3 (f 0.97-1.05): ~8,300-10,500, i.e. FRZ1's fail.
- H(z)/H0 (f 4.56 at z 3, about (1+z)^1.1) overshoots: 20,943 / 34,390.

## Table (reading L; R_cold at z 3, k 3 / 5 h/Mpc; Delta chi^2 canonical / alt; gate <= 4)

| case | f(z 3) | R_cold k3/k5 canonical | R_cold k3/k5 alt | Delta chi^2 can / alt | label |
|---|---|---|---|---|---|
| P0 | 1.000 | 0.845 / 0.665 | 0.831 / 0.669 | 9916.2 / 9008.7 | FAILS / FAILS |
| P0.5 | 2.000 | 0.987 / 0.966 | 1.027 / 1.043 | 251.8 / 167.1 | FAILS / FAILS |
| P1 | 4.000 | 1.169 / 1.386 | 1.235 / 1.515 | 13338.6 / 23421.4 | FAILS / FAILS |
| P1.5 | 8.000 | 1.282 / 1.740 | 1.365 / 1.921 | 66919.5 / 98283.7 | FAILS / FAILS |
| P2 | 16.00 | 1.346 / 1.981 | 1.440 / 2.201 | 158021.6 / 222408.0 | FAILS / FAILS |
| D-Pan | 0.775 | 0.822 / 0.610 | 0.803 / 0.599 | 13657.7 / 13418.1 | FAILS / FAILS |
| D-DES5 | 0.737 | 0.818 / 0.600 | 0.798 / 0.588 | 14317.6 / 14188.3 | FAILS / FAILS |
| D-Uni | 0.706 | 0.814 / 0.592 | 0.794 / 0.578 | 14858.8 / 14812.9 | FAILS / FAILS |
| Q-Pan | 0.966 | 0.841 / 0.656 | 0.827 / 0.658 | 10509.2 / 9732.2 | FAILS / FAILS |
| Q-DES5 | 1.005 | 0.845 / 0.666 | 0.832 / 0.671 | 9944.2 / 9086.2 | FAILS / FAILS |
| Q-Uni | 1.054 | 0.850 / 0.678 | 0.839 / 0.688 | 9243.3 / 8291.9 | FAILS / FAILS |
| H | 4.557 | 1.195 / 1.460 | 1.265 / 1.600 | 20942.5 / 34390.1 | FAILS / FAILS |

Best power law (reported, not graded): n = 0.5 on both footings (251.8 / 167.1), not under the gate. Between n 0
and 1 a crossing exists, but on canonical R_cold at z 3 is still below 1 at n 0.5 and on alt already above 1, so the
footings would want different n; a single n that passes was not searched (not frozen) and would be a fit.

Hand estimate (in the criteria, before any number): D worse than P0, Q about P0, H near the flip; every case fails.
All four held; the D/Q/H f(3) values landed as estimated.

## Known answers and mutation
- KA-P0: R_cold at every z and k equal to FRZ1's frz1_hm.json (max rel 0.0 both footings); Delta chi^2 9916.246 /
  9008.690 against 9916.2 / 9008.7. PASS.
- KA-P2: R_cold(k 3, z 3) change P2 - P0 = +0.5018 (FRZ1 MZ3 +0.5018). PASS.
- MZ1 (3 keV warm cutoff arm, as written in FRZ1, against the reference): 3775.0 / 3772.6 > 4. Bites.
- Inherited pipeline checks rerun: KA2 (R = 1 gives 0) and KA3 (HLF1 160.74 / 1025.57) pass on both footings.

## Inherited from FRZ1 (unchanged)
CFG556's halo model, CO1's layout rules, PD1's shares, the DESI DR1 P1D pipeline from SS1 and form B's F1A B2 linear
model; f(z) changes only a0 inside the layout. The halo model's own cosmology (Om) sets H; the CPL sets enter only
through f(z), not through the background or growth.

## Not computed
Readings V, the concentration / mass-function / dta / X brackets and MZ2 of FRZ1; any a0(z) beyond the frozen twelve;
any fit of n; a0(z) at z = 0 is unchanged in every case, so CO1's z = 0 rows are not re-graded.

Files: frz2_hm.py, frz2_forest.py, frz2_check.py, run_all.sh; outputs hm/, frz2_forest_*.json/.out, frz2_summary.*.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
