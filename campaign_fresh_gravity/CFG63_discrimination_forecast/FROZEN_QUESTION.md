# CFG63 frozen question (written before any script)

**Question, verbatim from the assignment:**

For each still-open test, which measurement, at what sample size N or precision, separates candidate B (the law T1-T6 plus FG001 ownership) from (i) the bare MOND-type law and (ii) LCDM, using ONLY error budgets and predictions already committed in this repo (cite file and line for every number)?

**Tests, verbatim:** (1) Gaia DR4 wide binaries: Arms A (gamma-hat 1.1614-1.1814 / 1.1917-1.2267), B/C (1.000), the chain ceiling 1.0725/1.0900, N = 30,000, forecast sigma from prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md Amendments 12-14 and the estimator's error model; (2) a0 at z ~ 2.5: flat vs a0*E(z) (or LCDM-native +0.334 dex), per-object 0.13 dex, correlated 0.2 dex mass-scale systematic (see campaign_fresh_gravity CFG6_a0z_evidence, CFG52, CFG54 READMEs); (3) ultra-faint dwarfs under binary-corrected dispersions (CFG28, CFG29, CFG46, CFG51: how many systems at what dispersion precision resolve the +0.3 dex law offset vs the rule's -0.06); (4) X-ray groups (CFG34) and (5) KiDS budget (CFG24/CFG27) only if their budgets give a usable sigma; say 'not forecastable from committed budgets' otherwise.

**Deliverables:** (a) this file; (b) `forecast.py` computing, for each test, the N (or precision) needed for 2 and 3 sigma between each pair of readings, the systematic floor that caps the significance whatever N, and what result would kill which reading; cite every input; (c) a MUTATE control (remove the systematic floor; must change the headline; exit 1) with exit codes documented; (d) `README.md` with one ranked table and a plain-language reading (most decisive per unit of effort; which tests are capped below 3 sigma by systematics; what is NOT forecastable).

**Rules:** no new physics, no new constants, no tuning; a test that cannot discriminate is a valid result and is reported plainly; kappa = 1/2 stays FITTED; the theory is not claimed closed.

## Declarations made before the first run (how the frozen question is operationalised)

1. **Significance model.** For two readings with predicted values differing by Delta, measured with a statistical variance v1/N and a non-shrinking systematic floor f, the separation is S(N) = Delta / sqrt(v1/N + f^2). N needed for k sigma is v1 / ((Delta/k)^2 - f^2), and is infinite when f >= Delta/k. The cap at infinite N is Delta/f. This is the same algebra the repo already uses (CFG6_a0z_evidence.py `n_obj`, PREREGISTRATION_DR4.md section 1.5 sigma_tot).
2. **Floors are not shrunk.** Each floor is the value a committed lane already carries. The Gaia floor is the frozen sigma_sys = 0.02 (no post-hoc shrinking is allowed by the pre-registration). Where a floor is a nuisance shift common to both readings it still counts, because the shift is unknown and cannot cancel in a two-point test.
3. **Reading of the labels.** "Candidate B" = ownership rule reading (Arm C for wide binaries; flat a0 = branch A for a0(z); the isolated law and the derived cold-mass rule are B's two committed dwarf readings). "Bare MOND-type law" = Arm A for wide binaries; a0 tracking H(z) for a0(z); the isolated law (no cold debris) for dwarfs. "LCDM" = Newtonian wide binaries; the LCDM-native +0.334 dex for a0(z); an NFW halo of free mass for dwarfs and groups.
4. **Controls.** Every cited line is machine-checked to contain the cited text. Committed separations (5.8/6.8 sigma_tot, 2.25/1.50 sigma at infinite N, 2.57 sigma, 1.4 / 15 / 13 objects, 3.77 / -0.41 / 1.26 / 2.46 sigma, 1.80 sigma, cost/S 0.59-0.98) must be reproduced by the same code before any new number is trusted.
5. **MUTATE.** All systematic floors set to zero. The headline (which tests are capped below 3 sigma) and the reproductions of committed capped numbers must change. That run must exit 1.
6. **A test that cannot be forecast** from committed budgets is labelled 'not forecastable from committed budgets' with the reason, and gets no number.
