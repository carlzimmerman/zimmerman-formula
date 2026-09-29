# CFG181 — independent referee re-derivation of CFG174 (the owner's flowing Lambda-vacuum as a column budget)

Frozen criteria: `CFG181_FROZEN_CRITERIA.md` (committed first, 8544933c3, sha256 14b228a1...). CFG174 scripts, `.out` and `.json` were opened only AFTER the referee's own main, MUTATE 1-7 and attacks were saved. Every CFG174 README number is a target I read, not a blind prediction. Standing rules: kappa = 1/2 stays FITTED; nothing here says the theory is closed; nothing here says any data favour the framework.

Files: `CFG181_common.py` (shared helpers; a disclosed deviation from the plan, which had helpers duplicated), `CFG181_referee_main.py` (`MUTATE=k`, k = 1-7), `CFG181_attacks.py` (A-G), `CFG181_compare.py` (phase 2 only), `run_all.sh`; outputs `CFG181_main.out/_results.json`, `CFG181_MUTATE_{1..7}.out/_results.json`, `CFG181_attacks.out/_results.json`, `CFG181_compare.out`, `run_all.out`. All runs take seconds. Re-run: `cd <lane dir> && ./run_all.sh` (expects main exit 0, MUTATE 1-7 exit 1 = control bites, attacks exit 0); then `ZF_REPO=<repo> python3 CFG181_compare.py` (phase 2; prints `<repo>`). An in-place re-run reproduced every `.out` and `.json` byte for byte (checked by hashing).

## Verdict per pass line: REPRODUCES, all of them

Primary settings (frozen): CFG44's code kernel nu_p2 = sqrt(1 + 1/y) (M_c = a0 r^2/(2G)), cosmology H0 = 67.4, Omega_L = 0.685 for rho_L and R500, t0 = 13.79 Gyr, Q3 at (67.66, 0.3111).

| CFG174 row | README / CFG174 script | mine | difference class |
|---|---|---|---|
| Sigma_M, footing A | 106.9 (106.877) | 106.88 | none |
| Sigma_M, footing B | 129.2 (129.162) | 129.03 | definition: CFG174's alt a0 = 1.1312e-10 vs my 1.13e-10 (0.1%) |
| swept column rho_L c t0 | 365 (365.014) | 365.15 | numerical (0.04%; rho_L see below) |
| R (A / B) | 0.293 / 0.354 | 0.2927 / 0.3534 | numerical, 0.03% / 0.14% |
| u_min | 0.293 c | 0.2927 c | none |
| Q2 f(x) at x = 0.1, 1, 10, 30 | 1.00, 0.83, 0.18, 0.064 (script 0.9975, 0.8284, 0.1810, 0.0645) | 0.9975, 0.8284, 0.1810, 0.0645 | none (README rounded) |
| Q2 slope x 3-30 | -0.87 | -0.872 (chord); local slope -0.967 / -0.990 / -0.999 at x = 30 / 100 / 1000 | none |
| Q3 dex z = 0.85, 1.5, 2.5 | -0.33, -0.51, -0.72 | -0.326, -0.509, -0.722 | none (identical to 4 digits) |
| Q3 velocity; a0 ~ H(z) | -0.08, -0.13, -0.18; +0.21, +0.37, +0.57 | -0.081, -0.127, -0.181; +0.212, +0.372, +0.573 | none |
| Q4 steady ratio (A), log M500 = 14, 14.5, 15 | 2.06, 1.40, 0.95 | 2.068, 1.409, 0.960 | numerical, 0.5%: CFG174 takes rho_crit at H0 = 67.66, I at 67.4 |
| Q4 steady ratio (B) | 2.49, 1.69, 1.15 | 2.496, 1.701, 1.159 | numerical + definition (a0 B), 0.4% |
| Q4 full swept column / need | 3-7 (7.03, 4.79, 3.26) | 7.06, 4.81, 3.28 | numerical, 0.55% |
| Q4 label | factor-2 line FAILS at 1e14 only (reported) | FAILS at 1e14 (2.068), passes 14.5 and 15 | none; but see F: fragile |
| MUTATE t0 = 1 Gyr | R = 4.04 / 4.88, load-bearing failures | R = 4.036 / 4.873, control bites | none |
| symbolic: M_c -> a0 r^2/(2G), R mass-free | yes | yes (sympy) | none |

No row is out of tolerance (max difference 0.55%). The remaining differences are constants (G, Msun, Gyr, rho_crit): CFG174 hard-codes `RHO_L = 5.8424e-27`, which matches Omega_L rho_crit at (67.4, 0.685) to 0.04%, while its age and R500 use H0 = 67.66, Om = 0.3111 (for which Omega_L rho_crit would be 5.924e-27, +1.4%): a mixed cosmology, numerical and immaterial to every pass line.

## Where independence stops (shared definitions)

The extra-mass target (CFG44's `nu_p2`), the definition Sigma_M = M_c/(pi r^2), the a0 footings (9.3603e-11, about 1.13e-10), the frozen cosmology values, the pass lines (0.1 <= R <= 1, factor 2, direction of Q3), and, in attack D, `nu_mono` (rebuilt from Bcommon's definition). The arithmetic, sympy limits, closed-form ages, R500 and all attack grids are my own code. Independence is weakest exactly where the README's framing lives (which column, which speed, which kernel), because those are the declared choices; that is why they are attacked rather than re-derived.

## Attacks (frozen grids, `CFG181_attacks.out`)

- **A. Restatement or genuine?** Q1 accepts a0 in [3.2e-11, 3.2e-10] m/s^2 (1.00 dex wide) about c H0 = 6.5e-10 (a0(A) = 0.143 c H0). All literature-scale a0 values {0.8, 1.0, 1.13, 1.2, 1.4}e-10 and all kappa in {0.35, 0.465, 0.5, 0.55, 0.72} give R = 0.21-0.44 and pass; no galaxy-scale quantity enters. Verdict: **RESTATEMENT** (as the README declares). A log-uniform null world (a0 over 1e-13 to 1e-7) passes in 1/6 of the range, informational only, since the a0 ~ c H0 coincidence is already known.
- **B. Declared choices.** **DEFINITION-DEPENDENT**: the pass flips on three axes. Column: shell surface M_c/(4 pi r^2) gives R = 0.073 (fails the lower bound); central rho_c r gives 0.146; projected column through rho_c ~ 1/r (log-divergent, needs a truncation) gives 0.26 / 0.53 / 0.88 / 1.55 for Z/R = 1 / 3 / 10 / 100 (Z/R = 100 fails the upper bound). Speed: u = c and 0.3 c pass; 0.1 c gives R = 2.9 (fail), 600 km/s gives 146, the CMB-dipole 370 km/s gives 237: at a physical flow speed relative to galaxies the swept column is 240 times too small. Duration: t0 and t(z=1) pass, t(z=2) (R = 1.23) and 1 Gyr fail. Kernel: the simple interpolating function (the task text's "P2") doubles the column (R = 0.585, still passes); footing and cosmology axes move R by 20-30% at most and never flip. Joint set (3 columns x 2 kernels x 2 footings x 4 cosmologies, u = c): 42 of 48 cells pass, R = 0.13-1.29. Also: the pass line is two-sided; R < 0.1 means MORE swept column than needed, yet fails; with a one-sided R <= 1 the shell column and a0 x 0.1 would pass. So "no extra constant" holds only for a light-speed flow, the chosen column definition and P2.
- **C. Scale-free or circular?** Sympy: R = kappa/(2 pi) x [1/(H0 t)] x [1/sqrt(3 Omega_L/8 pi)] = 0.293 (kappa = 1/2): SCALE-FREE (no mass, no radius) but exactly linear in a0 (d ln R/d ln a0 = 1.000000000), and it depends on the epoch through H0 t0 = 0.95. It is a rewriting of the measured ratio a0/(c H0) times cosmology numbers. The line holds only for 4.0 < t < 40 Gyr. Not circular in the sense of using an outcome to fix itself; circular in the sense that it tests nothing beyond the coincidence.
- **D. Kernel dependence.** The plateau column a0/(2 pi G) is P2-specific: the simple kernel gives twice it (2.0 in P2 units); the McGaugh RAR column goes to 0 at small x (extra acceleration decays exponentially), peaking at 1.30 at x = 0.63; `nu_mono` has no plateau either but the column GROWS toward small x (2.09 at x = 1e-3, 1.79 at 1e-2, 1.49 at 0.1). **Wrong expectation, kept:** my frozen text said both RAR and nu_mono extra accelerations vanish; nu_mono's monotone repair adds a slowly growing (log) term, so it does not vanish. "For every baryon mass" is true for kernels whose extra acceleration is constant at high g_N.
- **E. Q3.** The sign is robust (falls with z in every one of 16 grid cells and with radiation included, Omega_r = 9.2e-5; t0 = 13.786 Gyr, same dex). The amplitude at z = 1.5 ranges from -0.506 to -0.611 dex across flow-onset redshift (infinity, 20, 10, 5) and cosmologies: spread 0.105 dex, just over the frozen 0.1 threshold, driven only by the z_on = 5 cells, so the frozen rule labels the -0.51 headline **assumption-dependent** (it is exact for a flow that starts at the Big Bang). Q3 is independent of u.
- **F. Q4.** The frozen scaling claim holds exactly: ratio exponent d log(ratio)/d log M500 = -1/3 in all 24 cells (steady column ~ M^(2/3) against need ~ M). The FAIL label at 1e14 is **FRAGILE**: 2.068 vs a line of 2; it flips to pass in 2 of 24 cells (baryon fraction 0.10 and 0.12), and stays FAIL under 200 rho_crit and 500 rho_mean. Extra finding not in the README: the column mass overshoots the law's OWN phantom mass at R500 (M_c from P2 with M_b = 0.15 M500) by 2.97 / 2.56 / 2.22, and the law's own phantom is only 0.70 / 0.55 / 0.43 of the LCDM need; so a steady column of a0/(2 pi G) is not what the law itself puts in clusters either.
- **G. Q2 label.** **LABEL DISCREPANCY (framing)**: the README's f(x) numbers equal M_c/(Sigma_M pi r^2) (CFG174's script defines it that way), i.e. the fraction of the law's own inner column. The README/frozen wording "fraction of the swept column" would give R x f: 0.292, 0.243, 0.053, 0.019 at x = 0.1, 1, 10, 30. The 1/x conclusion is unaffected (local slope -> -1).

## MUTATE controls (all 7 bite; kept as run)

1. t0 = 1 Gyr: R = 4.04 > 1, Q1 line fails, exit 1. 2. shell column: R = 0.073, fails (bites only because of the two-sided line). 3. u = 370 km/s: R = 237, fails. 4. a0 x 0.1: R = 0.029, fails. 5. column x 4: R = 1.17, fails on the upper side. 6. Q3 sign swap to E(z): dex at z = 1.5 becomes +0.37, the falls-with-z line fails. 7. mass proportional to M: the ratio is constant, exponent 0 vs -1/3, line fails. A control that bites shows the line is sensitive to the cell, not that the cell is physical.

## Classification of every difference and disagreement

- Definition: (i) door-11 file and task text write P2 as nu = 1/2 + sqrt(1/4 + a0/g_N) (the simple interpolating function) whereas CFG44's code and CFG174 use nu = sqrt(1 + 1/y): a documentation inconsistency in the door-11 gates file, not an error in CFG174; with the simple kernel R and the cluster ratios double. (ii) CFG174's footing B is a0 = 1.1312e-10 (mine 1.13e-10).
- Numerical: rho_L / rho_crit cosmologies and constants, all <= 0.55%.
- README typo: none found in numbers. Wording: "fraction of the swept column" (G).
- Framing: (a) Q1's "no extra constant" needs u = c, this column definition, P2 and the two-sided line; (b) the Q4 FAIL label is fragile and the column also overshoots the law's own phantom; (c) the Q3 amplitude is exact only for a flow starting at the Big Bang.
- Script bugs in my own code, fixed before the saved runs (not physics): first run scaled H0 by 1e-2 (wrong units); the attack-D "plateau" label mis-tagged a column that is identically zero. Both are repairs of code, not of an expectation.

## Plain answer: is the column budget a genuine test of the flowing-vacuum picture?

**No. It is a restatement of the target (the a0 ~ c H0 coincidence), as CFG174's own README declares.** R = kappa/(2 pi) / (H0 t0) / sqrt(3 Omega_L/8 pi) is a mass-free cosmology number times kappa; it passes for every literature a0 and every reasonable kappa, only for a light-speed flow, only with this column definition and the P2 kernel, and it fails by a factor of about 240 for a flow at galaxy-relevant speeds. Nothing in Q1 or Q2 could have come out otherwise unless a0 were an order of magnitude off c H0; Q2 is a requirement (a deposit law falling as 1/x) that the picture does not supply. The only content beyond the coincidence is Q3 (a0 falling with redshift: direction robust, amplitude assumption-dependent, and a rival to the framework's own constant-a0 law rather than a consequence of it) and Q4 (right order of cluster dark mass, wrong M^(2/3) scaling, fragile label). None of these is a dynamical law for the flow, which is what the door-11 rules require before anything counts as a pass. CFG174's arithmetic reproduces; its Standing paragraph is fair but should say that the budget passes only for u = c and its declared column, and that the deposit fraction f(x) is normalised to Sigma_M, not to the swept column.

## In-place re-run (orchestrator)

`./run_all.sh` and `python3 CFG181_compare.py` were re-run in this directory with `ZF_REPO` set: main 0; MUTATE 1-7 exit 1 (all bite); attacks 0; compare 0. Every `.out` and `.json` is byte-identical to the referee's. The frozen criteria are `../CFG181_FROZEN_CRITERIA.md` (8544933c3). Independence stops at the shared definitions listed above (CFG44's code kernel nu = sqrt(1 + 1/y), the README's constants).
