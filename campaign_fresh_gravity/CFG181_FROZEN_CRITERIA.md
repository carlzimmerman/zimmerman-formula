# CFG181 — independent referee re-derivation of CFG174 (the owner's flowing Lambda-vacuum as a column budget): FROZEN CRITERIA (phase 1)

Written 2026-09-29, before any CFG181 script or number. Numbering: this lane was first opened as CFG177 and renumbered CFG181 by the coordinator; all files carry CFG181. The scratch dir is still `.../scratchpad/cfg177/`. Nothing here says the theory is closed; kappa = 1/2 stays FITTED; no claim that any data favour the framework. Failed controls and wrong expectations are kept, never repaired.

## 0. What is read, what is not, and how blind this is

Read in phase 1 (only): `CFG174_door11_vacuum_column/FROZEN_QUESTION.md` (Q1-Q3, Addendum 1 = Q4), its `README.md`, `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md`, `closure_map/TEN_DOORS_RESULT_2026-09-29.md`, `CFG44_fluid_target/README.md`, and the first 80 lines of `CFG44_fluid_target/Bcommon.py` (kernel definitions, constants: shared definition, see 1). NOT opened: any CFG174 `.py`, `.out`, `.json`. They are opened only in phase 2, only after this lane's own main and MUTATE runs are saved (`CFG181_main.*`, `CFG181_MUTATE_*.*`, `CFG181_attacks.*`).

**The README numbers are targets I read, not blind predictions.** The hand estimates in 3 were made after reading the README; for Q2, Q3 and Q4 I also hand-checked the README's numbers while reading (they came out consistent), so those rows are not independent predictions at all, only a sanity check that the README is not obviously wrong. Independence lives in the code (written from the frozen question, not from CFG174's script), in the attacks, and in the pre-declared grids.

## 1. What is re-derived, and where independence STOPS

Re-derived from scratch with my own code (numpy/sympy/scipy, no import from the repo): the P2 point-mass extra mass and its small-radius limit (sympy); the column Sigma_M; the swept column rho_L * u * t; R and its symbolic reduction; u_min; the deposit fraction f(x) and its slope; the accumulation ratio t(z)/t0 (closed-form flat-LCDM age) and E(z); the cluster R500, the column mass and the ratios to the needed dark mass.

Shared definitions (independence STOPS here; they are inputs, not tested):
1. The target itself: the law's extra enclosed mass for a point mass and P2, with CFG44's `nu_p2(y) = sqrt(1 + 1/y)` (i.e. g = sqrt(g_N^2 + a0 g_N), M_c = M(sqrt(1+x^2) - 1), x = r/r_M, r_M^2 = G M/a0). **Definition conflict flagged now:** the task text and door-11 file write "P2: nu = 1/2 + sqrt(1/4 + a0/g_N)"; that is the *simple* interpolating function, not CFG44's `nu_p2`. They differ: at small x the simple kernel gives M_c = a0 r^2/G (twice the P2 value a0 r^2/(2G) that the CFG174 README uses and CFG44's code implements). The README follows CFG44's code, so the PRIMARY kernel is CFG44's `nu_p2`; the simple kernel is a declared grid cell (attack A3), and I report the factor 2.
2. The column definition Sigma_M = M_c(<r)/(pi r^2) = a0/(2 pi G): quoted from FROZEN_QUESTION Q1, re-derived (sympy), but its *definition* is CFG174's declared choice and is attacked (A1).
3. Constants: G = 6.67430e-11, c = 299792458 m/s, GM_sun (IAU nominal) 1.32712440018e20 => M_sun = 1.98841e30 kg, pc = 3.0856775814913673e16 m, Julian Gyr = 3.15576e16 s. Differences with the repo's own constants are ~0.1% and are inside the tolerances.
4. a0 footings: A = 9.3603e-11 (canonical, CHARTER; from memory index and Bcommon), B = 1.13e-10 (the memory index's second footing). Both used with the SAME rho_Lambda (the README's alt column 129.2 / 106.9 = 1.208 = 1.13/0.936, and alt R 0.354 = 0.293 x 1.207, confirm this).
5. Cosmology. Q3 is frozen at flat LCDM, H0 = 67.66, Om = 0.3111 (t0 = 13.79 Gyr, no radiation; hand check agrees). For Q1/Q4 the README's rho_Lambda is not stated; my hand check finds the README's 365 Msun/pc^2 and a0(A) = 0.5 c sqrt(G rho_L) = 9.36e-11 are both reproduced by H0 = 67.4, Omega_L = 0.685 (the Planck-2018 TT,TE,EE+lowE+lensing pair), while (67.66, 0.6889) gives ~370 (1.4% higher). **Primary cosmology for Q1/Q4 = (67.4, 0.685) with t0 = 13.79 Gyr (as the frozen question states it)**; both pairs are grid cells (A3). Whether CFG174 used exactly this pair is a phase-2 question, not assumed.
6. The pass lines and the declared choices are CFG174's (frozen in 226e53662 and Addendum 1); the referee does not change them, it attacks them.

## 2. Headline pinned with the README's numbers (targets read, not blind)

| id | README value |
|---|---|
| Q1 Sigma_M (A / B) | 106.9 / 129.2 Msun/pc^2 = a0/(2 pi G) |
| Q1 swept column rho_L c t0 | 365 Msun/pc^2 (t0 = 13.79 Gyr) |
| Q1 R = Sigma_M/(rho_L c t0) = kappa/(2 pi t0 sqrt(G rho_L)) (A / B) | **0.293 / 0.354**; mass-independent; pass line 0.1 <= R <= 1; u_min = R c (about 0.3 c) |
| Q2 f(x) at x = 0.1, 1, 10, 30 | 1.00, 0.83, 0.18, 0.064; chord slope x 3-30: -0.87 |
| Q3 log10 a0(z)/a0(0) = log10 t(z)/t0 at z = 0.85, 1.5, 2.5 | -0.33, -0.51, -0.72 dex; deep-MOND velocity -0.08, -0.13, -0.18 dex; a0 ~ H(z): +0.21, +0.37, +0.57 |
| Q4 column mass / needed dark mass (0.85 M500) at log M500 = 14, 14.5, 15 (A / B) | 2.06, 1.40, 0.95 / 2.49, 1.69, 1.15; full swept column 3-7 x the need; reported FAIL of the factor-2 line at 1e14 |

Hand-check remarks made while reading (labelled, not predictions): the README's f(x) values are f = (sqrt(1+x^2) - 1)/(x^2/2), i.e. **normalised to Sigma_M, not to the swept column**, although the text says "a fraction f(x) of the swept column" (the fraction of the swept column would be R f, 0.29 at small x): a labelling discrepancy to test (D2). The 2.06 at 1e14 sits within 3% of the factor-2 line, so the "reported FAIL" is a fragile label (D3).

## 3. Hand ESTIMATES (made after reading the README) with reproduction probabilities

"Reproduces" = within the tolerance in 4.

| row | my hand estimate | P(reproduces) |
|---|---|---|
| R (A) | 0.29 (0.292 by hand: (kappa/2pi)/(H0 t0)/sqrt(3 Omega_L/8pi) with H0 t0 = 0.9505) | 0.90 |
| R (B) | 0.353 | 0.85 |
| Sigma_M (A / B) | 106.8 / 129.0 | 0.90 / 0.80 |
| swept column | 365 with (67.4, 0.685); 370 with (67.66, 0.6889) | 0.75 (cosmology ambiguity) |
| f(x), slope | 1.00, 0.83, 0.18, 0.065, -0.872 (analytic) | 0.97 |
| Q3 dex, H(z) | -0.326, -0.51, -0.72; +0.212, +0.372, +0.573 | 0.95 |
| Q4 ratios (A) | 2.07, 1.41, 0.96 | 0.80 within 3% (R500 conventions) |
| Q4 label at 1e14 = FAIL | 2.06 > 2 : FAIL | 0.65 (fragile) |
| sympy: mass independence of R, M_c = a0 r^2/(2G) | yes | 0.98 |

I expect the README to reproduce; I expect the weaknesses to be in the framing (column definition, light-speed flow, the two-sided pass line, Q2 labelling, kernel dependence), not in the arithmetic.

## 4. Exact pass lines (reproduction)

Main run reproduces each README row when: Sigma_M A within 0.6%, B within 1.5%; swept column within 1.5% of 365; R within 0.004 (A) / 0.005 (B); u_min/c = R; f(x) within 0.005 absolute at the four x and slope within 0.01; Q3 dex within 0.01 each and velocity within 0.005; E(z) dex within 0.01; Q4 ratios within 3% (A and B) and the pass/fail label at each mass identical to the README's (fail at 14 only); swept-column ratio band contained in [2.8, 7.4]; sympy confirms M_c(<r) -> a0 r^2/(2G) at r << r_M for every M_b and that R has no M_b dependence. Classes: REPRODUCES (all rows), PARTIAL (each unmet row listed), DISAGREES (any Q1 or Q3 headline out of tolerance by > 5%, or a label flip other than D3). Exit code: main exits 0 when the script completes and prints its class (a disagreement is a finding, listed in the output, never repaired); it exits 2 only on an internal error.

## 5. MUTATE controls (each must flip a load-bearing cell; exit 1 when the control bites, 0 if it does not, and a control that does not bite is kept and reported)

Run as `MUTATE=k python CFG181_referee_main.py`, outputs `CFG181_MUTATE_k.out/.json`:
1. **t0 -> 1 Gyr** (also CFG174's own control): R rises to about 4.0 > 1; the Q1 pass line must flip to FAIL.
2. **column = shell surface density M_c/(4 pi r^2)** instead of M_c/(pi r^2): R = 0.073 < 0.1; Q1 must flip to FAIL (this bites only via the *two-sided* line; recorded).
3. **flow speed u = 370 km/s** (CMB-dipole speed) instead of c: R rises to ~ 240; Q1 must flip to FAIL (this is the light-speed assumption).
4. **a0 x 0.1** (kappa = 0.05): R = 0.029; Q1 must flip to FAIL (R is linear in a0: tests the scale-tie, attack C).
5. **column x 4** (e.g. a0/(pi G) with a further factor 2): R = 1.17 > 1; Q1 must flip to FAIL on the UPPER side.
6. **Q3 sign control**: replace t(z)/t0 by E(z)/1 (the H(z) reading) in the accumulation slot; the "falls with redshift" line at z = 1.5 must flip to FAIL.
7. **Q4 exponent control**: replace the column area pi R500^2 by (4 pi/3) R500^3 x (mean density fixed by the 1e14 value) so the mass scales as M; the "wrong scaling (slope -1/3 in ratio)" line must flip (slope 0 within 0.02).

## 6. Attacks: frozen procedures and what pass/fail means (all in `CFG181_attacks.py`, output `CFG181_attacks.out/.json`, exit 0)

The grids below are declared now; no cell is added or dropped after seeing results. "Flips" = the Q1 line 0.1 <= R <= 1 changes status relative to the primary cell.

**A (genuine test or restatement; prescription check).** Classify each of Q1-Q4 by whether it can fail independently of the a0-Lambda coincidence. Procedure: compute the a0 window that Q1 accepts, a0 in [0.1, 1] x 2 pi G rho_L c t0 (predicted about 3.2e-11 to 3.2e-10, i.e. 1.0 dex wide, cH0/2pi-like values pass), and test literature-scale a0 values {0.8, 1.0, 1.13, 1.2, 1.4} x 1e-10 and kappa in {0.35, 0.465, 0.5, 0.55, 0.72}. Also count null worlds: a0 log-uniform over 1e-13 to 1e-7 (informational only; no pass line, and the real prior is that a0 ~ cH0 is already known to about 0.7 dex). Verdict: RESTATEMENT if every a0/kappa value in the literature ranges passes (declared expectation) and no galaxy-scale quantity enters R; GENUINE if any such value fails. Q2 is classified a requirement, not a test. Q3 is classified the only falsifiable statement, but a rival to (not a consequence of) the framework's own flat-a0 law, since a0 = kappa c sqrt(G rho_L) with constant rho_L is constant in the framework; noted, not scored. Q4: classify as a genuine miss iff the exponent -1/3 of the ratio and the 3% margin hold.

**B (declared choices; one-at-a-time and joint grid).** Axes, all pre-declared "reasonable":
- column definition (CFG174: M_c/pi r^2; M_c/4 pi r^2; central rho_c r = a0/4 pi G; projected column through rho_c = a0/(4 pi G sqrt(R^2+z^2)) truncated at |z| <= Z with Sigma = (a0/2 pi G) asinh(Z/R) for Z/R in {1, 3, 10, 100}; the projected column is log-divergent, so no untruncated value exists);
- flow speed u/c in {1, 0.3, 0.1, 0.01, 2e-3 (600 km/s), 1.2e-3 (370 km/s)};
- flow duration in {t0, t0/2, t(z=1), t(z=2), 1 Gyr};
- kernel {CFG44 P2, simple 1/2 + sqrt(1/4 + 1/y)} (factor 2 in the column);
- a0 footing {A, B}, cosmology {(67.4, 0.685), (67.66, 0.6889), (70, 0.7), (73, 0.7)}.
Procedure: one-at-a-time from the primary cell; then the joint "plausible" set = column in {CFG174 M_c/pi r^2, central rho_c r, projected Z/R = 3} x kernel x footing x cosmology (48 cells) at u = c, t0. Report the list of axes that flip the pass line, and the fraction of joint cells passing. Verdict: DEFINITION-DEPENDENT if any one-at-a-time axis within its declared range flips the line; ROBUST otherwise. I expect definition-dependent, flipped by the shell column (0.073), the light-speed and duration axes and the truncation Z/R = 100 (R ~ 1.5).
- Also the deposit-fraction logic: the pass window's lower bound 0.1 makes R < 0.1 a FAIL although R < 1 alone already means "enough column"; report what a one-sided line R <= 1 would change (the shell column and a0 x 0.1 would pass), and say which reading the frozen question intends.

**C (scale-free or circular).** Sympy: R = a0/(2 pi G rho_L c t0) = kappa /(2 pi) x [1/(H0 t0)] x [1/sqrt(3 Omega_L/8 pi)]: mass-free (no M_b, no r_M), but exactly linear in a0 (numerical d ln R/d ln a0 = 1 to 1e-9) and a function of the epoch H0 t0. Verdict: SCALE-FREE (mass-independent) and NOT a0-independent; it is a rewriting of the measured ratio a0/(c H0) times cosmology numbers, hence the declared coincidence. Also check that the cosmic-age dependence is the epoch coincidence: R(t) for a0 fixed but t = t0 x {0.1, 1, 10} (only the present-epoch value passes; report the range of t in which the line holds, in Gyr).

**D (kernel dependence of the column).** For nu in {CFG44 P2, simple, McGaugh RAR 1/(1 - exp(-sqrt y)), nu_mono rebuilt as in Bcommon (shared definition)}: compute M_c(<r)/(pi r^2) versus x = r/r_M for a point mass (x from 1e-3 to 1e2). P2 tends to the constant a0/(2 pi G) as x -> 0; the simple kernel to a0/(pi G); the RAR and nu_mono extra acceleration g_N(nu - 1) -> 0 exponentially as y -> infinity, so no constant column exists at small x. Report each kernel's supremum column and the x at which it occurs, and the R it would give. Verdict: "the column Sigma_M is a P2-specific constant" if RAR/nu_mono have no plateau (expected); the README's phrase "for every baryon mass" is then true only for kernels with a constant extra acceleration at high g_N.

**E (Q3 assumptions).** Onset of the flow z_on in {infinity, 20, 10, 5}: a0(z)/a0(0) = (t(z) - t_on)/(t0 - t_on); cosmology grid {(67.66, 0.3111), (67.4, 0.315), (70, 0.30), (73, 0.30)}; radiation neglected (declared; effect on t0 < 1% for z <= 2.5). Also check consistency with Q1: for a0 in the accumulation reading the present-day match a0(t0) = R-equivalent fixes u/c = R, independent of z, so Q3 does not depend on u. Verdict: the sign (falling with z) is ROBUST if negative in every cell; the amplitude at z = 1.5 is reported with its spread; if spread > 0.1 dex across the onset grid, the "-0.51 dex" headline is labelled assumption-dependent. No comparison with KURVS/KROSS (seen data; handed to the calculation chat).

**F (Q4 borders and the wrong-scaling claim).** Grid: R500 defined with 500 rho_crit (z = 0) [CFG174], 200 rho_crit, 500 rho_mean; baryon fraction f_b in {0.10, 0.12, 0.15, 0.17}; column {A, B footing}; and an alternative reference, the law's own phantom M_c^law(R500; M_b = f_b M500) via P2. Report ratio at 1e14, 1e14.5, 1e15 and whether it lies in [0.5, 2] (the declared line), the exponent d log(ratio)/d log M500 (predicted -1/3 exactly for fixed f_b and a spherical-overdensity R500), and the number of grid cells that flip the 1e14 FAIL. Verdict: the label FAIL at 1e14 is FRAGILE if any declared f_b/definition cell flips it; the M^(2/3) scaling claim is CONFIRMED if the exponent is -1/3 +- 0.02.

**G (Q2 labelling).** Compute f(x) normalised to Sigma_M (README numbers) and R f(x) (fraction of the swept column); check the 1/x asymptote (local slope at x = 30, 100, 1000 -> -1). Verdict: LABEL DISCREPANCY if the README's "fraction of the swept column" equals the Sigma_M-normalised fraction (predicted).

## 7. Script plan (each < 15 min; actually seconds; no absolute home path printed; the compare script resolves the repo from `ZF_REPO` or by walking up from `__file__` and prints `<repo>`)

- `CFG181_referee_main.py` — Q1-Q4 reproduction, sympy identities, class line; `MUTATE=k` (k = 1-7) writes `CFG181_MUTATE_k.out/.json`; main exit 0 (class printed), MUTATE exit 1 iff the control bites, exit 2 on error. Outputs `CFG181_main.out/.json`.
- `CFG181_attacks.py` — attacks A-G, exit 0; outputs `CFG181_attacks.out/.json` (+ a PNG optional).
- `CFG181_compare.py` — PHASE 2 ONLY: runs after the three sets above are saved; reads CFG174's `results.json`/`_MUTATE1` and diffs every README row and the Q4 label against my numbers; prints `<repo>`; exit 0.
- `run_all.sh` — runs main, MUTATE 1-7, attacks; in-place re-run must be bit-identical (checked with sha256 of the .out files).

## 8. What counts as disagreement

Any headline outside its tolerance in 4; a label flip other than D3 (the marginal Q4 FAIL, whose flip I treat as a finding about fragility, not as an error); a MUTATE control that does not bite (kept and reported); an attack verdict differing from the README's framing: (i) the Q1 pass is RESTATEMENT (agrees with the README's own declaration; if it turns out to be GENUINE that is a disagreement); (ii) the README's "no extra constant" holds only for a light-speed flow, the CFG174 column definition and the P2 kernel (any of these flipping = the README's Standing paragraph is over-stated, reported); (iii) the "fraction of the swept column" wording (D2); (iv) the kernel-conflict D1: if CFG174 turns out to use the simple kernel (column a0/(pi G)) rather than CFG44's P2, the README's 106.9 would be inconsistent with its own text. In phase 2 the compare report separates arithmetic disagreements from framing disagreements. Explicit null world (attack A): a0 < 3.2e-11 or > 3.2e-10 m/s^2, or a flow speed < 0.29 c, or a duration < 4 Gyr would each have failed Q1; none of these is the actual case, which is why Q1 has little power (declared by the README itself).
