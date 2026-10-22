# A71 mutations

Sixteen mutations, each changing **one input**, each invoked as `A71_MUTATE=<name> python3 a71_checks.py`,
each exiting **1**, each breaking at least one named check. Every one of the 28 checks is broken by at
least one mutation (matrix at the bottom). Base run: `python3 a71_checks.py` -> 28/28 PASS, exit 0.

| mutation | the one input it changes | exit | checks it breaks |
|---|---|---|---|
| `imf_prior` | the Treu prior width, 0.036 -> 0.100 dex (the cross-method spread) | 1 | K20, K21, K26 |
| `kappa_de` | the kappa convention: `rho_bare = rho_crit` -> `rho_DE` (A51's relabelling) | 1 | K4, K5, K14, K19, K22, K27, K23 |
| `newton` | `a0 = 1e-30` inside the SLACS lens model (the phantom switched off) | 1 | K7, K8, K9, K10, K20, K21, K26, K28, K25 |
| `no_boot` | `sigma(SPARC)` = the formal Delta-chi2 = 1 error instead of the bootstrap | 1 | K19, K27, K28 |
| `u_prior` | the sourcing-fraction prior, 0.03 -> 1.0 (u effectively free) | 1 | K14, K19 |
| `closure_4pi` | 8 pi -> 4 pi in the closure normalisation | 1 | K15, K16 |
| `kappa_in_E` | a kappa factor inserted into the expansion rate E(z) | 1 | K17 |
| `floor10` | the SPARC error floor, 5% -> 10% | 1 | K3, K5, K6, K19, K21 |
| `treu` | Treu+2010's `log10 alpha` shifted by +0.10 dex | 1 | K12 |
| `cluster_a` | the A18 baryon scale radius, 250 -> 200 kpc | 1 | K13, K14 |
| `drop_gal` | every 10th SPARC galaxy removed from the fit | 1 | K1, K3, K5, K6, K24 |
| `drop_lens` | every 7th SLACS lens removed from the fit | 1 | K2, K7, K8, K9, K11 |
| `b_marg` | `B` set to the lensing value instead of the prior-weighted mean | 1 | K18 |
| `est_span` | the estimator-ensemble half-span, 0.208 -> 0.050 | 1 | K24 |
| `closure_kernel` | the closure integrand multiplied by 1.001 (a 0.1% kernel error) | 1 | K15, K16 |
| `err045` | the per-lens SLACS variance drops the 0.09 dex intrinsic scatter | 1 | K11 |

Recorded outputs: `a71_MUTATE_<name>.out` (stdout + the same text as the base run) for each.

## What each mutation proves, in one line

- **`imf_prior`** — the entire "2 sigma IMF tension" is the width of Treu's prior. Widening it to the
  measured cross-method spread (0.100 dex) drives the pull from 1.97 to 0.86 sigma and the global
  tension from 5.69 (1.89 sigma) to 1.23 (0.61 sigma) (K20, K21, K26 all fail). This is not a bug; it is the declared
  sensitivity, and it is the single largest lever in the lane.
- **`kappa_de`** — the two conventions differ by `1/sqrt(Omega_L) = 1.2085`; every kappa check that
  compares a number to a stored value breaks at once. This is why K27 exists.
- **`newton`** — with the phantom off, the SLACS model has *no* kappa dependence
  (`dlnR/dlnkappa = 0`), so K9, K10, K25 and K28 must fail: they are statements about the law, not
  about arithmetic.
- **`no_boot`** — the formal Delta-chi2 = 1 error is 8.3x too small; using it changes the joint
  sigma(kappa) and the two distance-to-theory numbers (K19, K27, K28).
- **`u_prior`** — the cluster channel is only a constraint through the prior on `u`; drop it and the
  11% "measurement" disappears (K14).
- **`closure_4pi` / `closure_kernel`** — the closure is an identity; K15/K16 test its normalisation
  against A28's independently computed 66.299937 and against a second integral representation.
- **`kappa_in_E`** — the exclusion of BAO/SNe/CMB is a *computed* statement: E(z) is kappa-independent
  to machine zero. Insert a kappa factor and K17 fails.
- **`floor10`** — the SPARC channel is not error-model-free: the floor moves a0 from 8.08e-11 to
  7.34e-11 (K5) and changes the bootstrap (K6).
- **`treu` / `cluster_a` / `drop_gal` / `drop_lens`** — the two priors and the two data vectors are
  live inputs, not decoration.
- **`b_marg`** — mis-marginalising B (using the lensing value rather than the prior-weighted mean)
  makes the analytic profile and the 3-D minimiser disagree (K18).
- **`est_span`** — the error budget's ranking is a computation: shrink the estimator term and the
  largest removable term becomes the distance zero point (K24).

## Coverage matrix (check -> the mutations that kill it)

| check | killed by |
|---|---|
| K1 | drop_gal |
| K2 | drop_lens |
| K3 | floor10, drop_gal |
| K4 | kappa_de |
| K5 | kappa_de, floor10, drop_gal |
| K6 | floor10, drop_gal |
| K7 | newton, drop_lens |
| K8 | newton, drop_lens |
| K9 | newton, drop_lens |
| K10 | newton |
| K11 | drop_lens, err045 |
| K12 | treu |
| K13 | cluster_a |
| K14 | kappa_de, u_prior, cluster_a |
| K15 | closure_4pi, closure_kernel |
| K16 | closure_4pi, closure_kernel |
| K17 | kappa_in_E |
| K18 | b_marg |
| K19 | kappa_de, no_boot, u_prior, floor10 |
| K20 | imf_prior, newton |
| K21 | imf_prior, newton, floor10 |
| K22 | kappa_de |
| K23 | kappa_de |
| K24 | drop_gal, est_span |
| K25 | newton |
| K26 | imf_prior, newton |
| K27 | kappa_de, no_boot |
| K28 | newton, no_boot |

No check had to be deleted: 28/28 are killed by at least one input mutation.

Three candidate checks were **not** promoted to checks because no input mutation can break them, and
they are printed as diagnostics instead: (i) "the SLACS mean residual is exactly zero once B is
profiled" — true by construction; (ii) "the closure is satisfied for every kappa" — that is the point
of K16, whose falsifiable content is the two-formulation agreement, not the residual; (iii) the
`cn = B(2n+1)/B(n+1)` slip constant, which is analytic in `n` alone.
