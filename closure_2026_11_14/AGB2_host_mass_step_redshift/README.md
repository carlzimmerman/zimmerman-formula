# AGB2 — the progenitor-age slope tested on host galaxies (Pantheon+), and put together with AGB1

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (committed alone, before any script). One dated amendment, `AMENDMENT_1.md`
(committed alone, before any amplitude was read). Adopts nothing, edits no ledger, grades no part of this
repository's framework.

## Verdict
**The host galaxies do not settle the size of the age effect, and they do not support it at its published size.**

| word | result |
|---|---|
| H1, the host-mass step against redshift (primary) | **UNDECIDED / FRAGILE** (amendment 1). A = +0.37 ± 0.41. With the median age in the model the same fit reads AGE BIAS DISFAVOURED. |
| H2, brightness against the model's age host by host | **AGE BIAS EXCLUDED AT 3 SIGMA / ROBUST** (amendment 1). A = +0.13 ± 0.12; Δχ² = 50.6 against A = 1. |
| J1, hosts (H1) and AGB1's distances together | **UNDECIDED / FRAGILE** (amendment 1). A = +0.49 (68 %: 0.19 to 0.78). With the DES-only distances it reads AGE BIAS DISFAVOURED. |
| J2, accelerating today, with the host prior | **SIGN NOT SETTLED** (amendment 1). q0 = −0.12, Δχ² = 0.47 against q0 = 0. |
| J3, did it ever accelerate, with the host prior | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** (amendment 1). Δχ² = 34.4. |
| every word as frozen (full covariance) | **NOT EVALUABLE**: the frozen error-bar check K4 failed. The reading is printed below. |

A = 1 is the slope of Son et al. (arXiv:2510.13121), 0.030 mag/Gyr, acting on the progenitor ages of the Childress
et al. (2014) galaxy model; A = 0 is no dependence on age beyond a constant host-mass step.

In plain words:
- **The step barely changes with redshift, but the errors are wide.** Raw host-mass step (small hosts fainter):
  +0.044 ± 0.014 mag at z < 0.05, then +0.047, +0.036, +0.043, and +0.010 ± 0.026 above z = 0.5. The published slope
  predicts 0.102 falling to 0.046. A straight line through the five gives −0.041 ± 0.042 mag per unit redshift
  against a predicted −0.098. That is H1: neither A = 0 nor A = 1 is 2σ away.
- **The step is less than half the size the slope needs.** The whole raw step is +0.039 ± 0.008 mag; the slope with
  the model's 3.3 Gyr age gap needs 0.10 at low redshift. Handing age every bit of the step still gives A = 0.47 ± 0.10
  (reported only): half the published slope.
- **Brightness does not follow the model's age from host to host.** Inside the massive hosts the model's age keeps
  rising with mass (4 Gyr at 10^10.5, 8 Gyr at 10^11.5 for nearby hosts), so the slope predicts about 0.12 mag across them. The data show a step
  at 10^10 and nothing more. That is H2, and it holds in every fork (smallest Δχ² against A = 1 is 26.4).
- **Put with AGB1, the allowed range narrows but both ends stay inside 2σ:** 0.19–0.78 against AGB1's 0.19–1.05;
  Δχ² = 2.71 at A = 0 and 2.99 at A = 1.
- **The 1998 result is untouched again:** no member of the fitted family that never accelerates comes within Δχ² = 34.

**The condition on all of it:** A is the slope times the model's age gap between hosts. If real hosts differ less in
progenitor age than the model's galaxies do, the true slope is larger than A by that factor. Son et al. argue
exactly that host mass tracks age poorly. H2 leans on the model at every mass and so is the most exposed; H1 leans
only on the gap between two groups.

## Known-answer checks
| check | result | |
|---|---|---|
| KG galaxy model | anchor 10.547 (10.55); 0.598 of the age rise inside 10.0–11.5; half the stars of a 10^11.5 galaxy formed by 10.92 Gyr ago, middle half in 1.28 Gyr; time-step change 0.004 Gyr | PASS |
| K1 loader and covariance | supernovae alone, flat ΛCDM: Ω_m 0.3316 (target 0.334, tolerance 0.009) | PASS |
| K2 raw step | +0.0405 ± 0.0105 mag as frozen; +0.0389 ± 0.0080 amended (window 0.02–0.09). Published magnitudes: −0.003 ± 0.008 | PASS |
| K3 twins | 8 of 8 recover the injected amplitude to 10⁻⁹, both weightings | PASS |
| K4 error bar, as frozen | shuffle scatter / stated error: 1.22 (step run), **1.44 (per host; allowed 0.8–1.25)** | **FAIL** |
| K4 error bar, amended | shuffle scatter 1.02 and 1.04; error from residuals (clustered by supernova) 0.98 and 1.00 | PASS |
| KJ joint harness | with no prior the machinery returns AGB1's Δχ² (2.100 / 0.785; 0.545 / 1.959) and its fork values to 10⁻³ | PASS |

**What K4 found (AMENDMENT_1.md).** With the inverse of the full STAT+SYS covariance as weights, the fit leans on
off-diagonal terms: the stated error of the per-host amplitude is 0.097 while the diagonal alone gives 0.49 through
the same weights, and an error computed from the residuals is 1.6 to 3.5 times the stated one. With each row
weighted by its own published error the three estimates agree to 6 %. The amendment makes that change and nothing
else. It was written after K1–K4 and before mode H or Part J had been run in either weighting.

## Part H, amended (diagonal weights)
| configuration | H1 step run: A | Δχ²(0) | Δχ²(1) | word | H2 per host: A | Δχ²(0) | Δχ²(1) | word |
|---|---|---|---|---|---|---|---|---|
| primary (all 1,563 rows, raw magnitudes, mean age, 20 bins) | +0.37 ± 0.41 | 0.79 | 2.39 | UNDECIDED | +0.13 ± 0.12 | 1.07 | 50.6 | EXCLUDED AT 3 SIGMA |
| published magnitudes | +0.32 ± 0.41 | 0.61 | 2.74 | UNDECIDED | +0.12 ± 0.12 | 1.02 | 52.6 | EXCLUDED AT 3 SIGMA |
| median age | +0.30 ± 0.33 | 0.79 | 4.53 | DISFAVOURED | +0.06 ± 0.08 | 0.45 | 131.5 | EXCLUDED AT 3 SIGMA |
| 40 bins | +0.44 ± 0.42 | 1.10 | 1.83 | UNDECIDED | +0.14 ± 0.12 | 1.22 | 48.9 | EXCLUDED AT 3 SIGMA |
| measured masses only (1,251) | +0.20 ± 0.52 | 0.15 | 2.41 | UNDECIDED | +0.21 ± 0.15 | 1.94 | 26.4 | EXCLUDED AT 3 SIGMA |

The free constant step that goes with the primary fits: +0.009 ± 0.034 mag (H1), +0.029 ± 0.012 mag (H2).

**The step band by band (model-free; small hosts minus massive hosts, mag):**
| z | rows | raw magnitudes | published magnitudes | slope predicts at A = 1 |
|---|---|---|---|---|
| 0.01–0.05 | 534 | +0.044 ± 0.014 | +0.001 ± 0.014 | +0.102 |
| 0.05–0.15 | 181 | +0.047 ± 0.020 | +0.004 ± 0.020 | +0.093 |
| 0.15–0.30 | 381 | +0.036 ± 0.015 | −0.004 ± 0.015 | +0.078 |
| 0.30–0.50 | 282 | +0.043 ± 0.017 | +0.002 ± 0.017 | +0.063 |
| 0.50–1.00 | 185 | +0.010 ± 0.026 | −0.030 ± 0.026 | +0.046 |
| line, mag per unit z | | −0.041 ± 0.042 | −0.034 ± 0.042 | −0.098 |

**Reported only.**
- Raw magnitudes with the constant step fixed at 0 (every bit of the step is age): A = +0.47 ± 0.10; Δχ² 24.5 at
  A = 0 and 30.4 at A = 1.
- Model forks (H1 / H2): alternate quenching mass +0.30 ± 0.34 (Δχ² 4.30 at A = 1; it would read DISFAVOURED) / +0.13 ± 0.12; short-delay delay-time
  distribution +0.49 ± 0.55 / +0.11 ± 0.14; masses +0.2 dex +0.32 ± 0.36 / +0.13 ± 0.11; masses −0.2 dex
  +0.43 ± 0.48 / +0.14 ± 0.14. H2's Δχ² against A = 1 stays between 39 and 61.
- Sample forks (H1 / H2): z ≤ 0.7 +0.46 ± 0.44 / +0.13 ± 0.12; without SDSS +0.42 / +0.18; without SNLS
  +0.34 / +0.13; without PS1 +0.46 / +0.16; without DES +0.15 / +0.15; without Foundation +0.47 / +0.14;
  without the other low-redshift sets +0.69 ± 0.53 / +0.16 ± 0.16. H1 stays UNDECIDED in all seven; H2's Δχ²
  against A = 1 stays above 28.
- The galaxy model's own population today has a median progenitor age of 3.2 Gyr, against 6.7 Gyr for the cosmic
  history behind AGB1's template. The two age models are not the same model; the joint takes each as built.

## Part J, amended: hosts and AGB1's distances together
Prior on A from H1's primary fit (+0.365 ± 0.411). f, t, n are AGB1's best χ² at fixed A when free, with q0 = 0,
and with q(z) ≥ 0 throughout.

| distances | host reading | joint A (68 %) | Δχ²(0) | Δχ²(1) | J1 | q0 | Δχ² today | J2 | Δχ² never | J3 |
|---|---|---|---|---|---|---|---|---|---|---|
| AGB1 `full` | raw (primary) | +0.49 (0.19–0.78) | 2.71 | 2.99 | UNDECIDED | −0.12 | 0.47 | SIGN NOT SETTLED | 34.4 | EXCLUDED AT 3 SIGMA |
| AGB1 `full` | published | +0.46 (0.17–0.76) | 2.46 | 3.27 | UNDECIDED | −0.13 | 0.57 | SIGN NOT SETTLED | 34.8 | EXCLUDED AT 3 SIGMA |
| AGB1 `des_only` | raw | +0.36 (0.05–0.67) | 1.33 | 4.34 | DISFAVOURED | −0.34 | 1.79 | SIGN NOT SETTLED | 34.4 | EXCLUDED AT 3 SIGMA |
| AGB1 `des_only` | published | +0.33 (0.02–0.64) | 1.15 | 4.69 | DISFAVOURED | −0.35 | 1.96 | SIGN NOT SETTLED | 34.9 | EXCLUDED AT 3 SIGMA |

Reported only: with H2 in the place of H1 the joint is A = +0.16 (0.05–0.28), Δχ² 1.95 at A = 0 and 50.2 at A = 1,
q0 = −0.28 with Δχ² = 7.65 against q0 = 0 (that would read ACCELERATING TODAY), and 80.3 against never accelerated.
Hosts and distances agree: H1 minus AGB1's best A is −0.4 combined errors (`full`), 0.0 (`des_only`); H2 is −1.1, −0.5.

## The reading as frozen (full covariance; NOT EVALUABLE because K4 failed)
Printed because both readings are owed. The stated errors here are the ones K4 shows to be too small; the error
from the residuals is beside each.
- H1: A = +0.80 ± 0.40 stated (0.65 from residuals); Δχ² 4.02 at A = 0, 0.24 at A = 1 by the stated error (it would
  read AGE BIAS FAVOURED); 1.5 and 0.09 by the error from residuals. Band steps +0.061, +0.047, +0.027, +0.037,
  +0.009; line −0.076 ± 0.041.
- H2: A = +0.30 ± 0.10 stated (0.29 from residuals); Δχ² 8.96 at A = 0, 50.2 at A = 1 by the stated error (NEITHER).
- Joint with H1: A = +0.72 (0.42–1.01), Δχ² 6.03 / 0.93 (it would read AGE BIAS FAVOURED), q0 = +0.00, Δχ² 0.00
  against q0 = 0, 30.7 against never accelerated.
So the two weightings pull the step-run amplitude apart (0.80 against 0.37), most of it from the lowest redshift
band, where the off-diagonal terms are largest. With honest errors both are within 2σ of A = 0 and of A = 1.
The per-host amplitude is far below 1 in both.

## Independent checks (scratch, not part of the frozen files)
- The four primary fits redone with a separate loader and a different route (demeaning inside bins, then least
  squares): equal to 10⁻⁸ with the lane's bin edges; with another library's handling of ties at the bin edges 14 rows
  change bin and A moves by 0.04 (H1) and 0.01 (H2).
- Bootstrap over supernovae (500 draws): errors 0.42 (H1) and 0.11 (H2), against 0.41 and 0.12.
- Three galaxy tracks re-integrated by explicit Euler at 1 Myr: mean ages equal the table to 0.003 Gyr.

## Limits
- The galaxy model is a web reading of Childress et al. (2014) (PROVISIONAL), one deterministic galaxy per mass. Its
  quenching-mass formula returns the paper's own anchor and it passes three checks drawn from the paper's text, but
  no table of the paper's ages was available to check against.
- Host mass is the only host property in the table. A null here rules out the published slope only as far as mass
  carries age. Measured host ages are the test that would close it; they are not public for this sample.
- Raw magnitudes carry no bias corrections, and masses are noisier at high redshift, which waters the step down
  there and pushes that reading towards A > 0. The published magnitudes carry the survey's own corrections, fitted
  to these supernovae, which pushes that reading towards A = 0. The two agree here.
- The joint assumes one slope in both places and takes each template as built. AGB1's words stand as written.
- One plumbing fix after the scripts commit: `agb2_joint.py` asked for start points on a grid that did not hold
  them (no rule changed; KJ passes). The first run stopped on that error before printing any joint number.

## Files
`FROZEN_CRITERIA.md`, `AMENDMENT_1.md`; `agb2_galaxy.py` (host-age model), `agb2_run.py` (checks and Part H),
`agb2_joint.py` (Part J), `agb2_collect.py`. As frozen: `agb2_{KG,K1,K2,K3,K4,H,J}.{json,out}`, `agb2_results.json`,
`agb2_collect.out`. Amended: `agb2_{K2,K3,K4,H,J}_diag.{json,out}`, `agb2_results_diag.json`, `agb2_collect_diag.out`.

Commits (local / origin): criteria a622d5cb15 / cd8644a083; scripts 86df7a46bb / 62f611ffda; amendment 091f5e1196 /
93bb27cfc3; amended scripts c08f7b1b77 / c3905d0581; joint plumbing fix 07b4151f13 / 2c41b7772e; result 46bd6cbd33 /
82c478ffef.

kappa = 1/2 FITTED; not theory closed.
