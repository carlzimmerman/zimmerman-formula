# CFG13 — CFG9's principle on its own terms: the transition shape where the baryons look like a point mass

Script: `CFG13_pointmass_shape.py`, about 10 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The point-mass subset's data are replaced by synthetic ν_mono data, and H1 fails (rc = 1).
- The main run exits 1, because C3 and H2 failed.

## Design

CFG9 derives P2 (β = 1 in ν_β = (1 + y^−β)^{1/2β}) for a locally virialized cold component around a **point** mass. CFG4's committed shape bootstrap uses every SPARC point and excludes β = 1.

SPARC's points are split by how much measured baryonic mass lies beyond them, at a selection Υ of 0.5:

| subset | condition | size |
|---|---|---|
| point-mass | M_b(R_last)/M_b(R_i) ≤ 1.10 | 878 points, 175 galaxies |
| embedded | M_b(R_last)/M_b(R_i) ≥ 1.5 | 1863 points, 172 galaxies |

CFG4 H3's statistic and bootstrap are then rerun on each subset (seed 20260927, 1000 galaxy resamples, Υ profiled).

## Results

**Controls**

| check | result |
|---|---|
| C1: CFG4 H3 reproduced exactly (all points) | pass: best 0.4847 / 0.5533; 95% [0.3974, 0.5912] / [0.4537, 0.7705] |
| C2 power: synthetic ν_mono data in the point-mass subset exclude β = 1 | pass: [0.40, 0.67] on both footings |
| **C3 bias: synthetic P2 data (β = 1) in the point-mass subset contain β = 1** | **FAILED**: [0.45, 0.77] / [0.42, 0.77], best 0.59 / 0.55 |

The noise is per-galaxy N(0, 0.08 dex) plus per-point N(0, 0.05 dex), with Υ profiled. Data that are P2 by construction came back at β ≈ 0.55–0.59, with β = 1 excluded.

**Withdrawn by CFG14: the reading "the estimator is biased low".** Over 60 realizations the estimator is median-unbiased (P2 truth: median β̂ = 1.004). The 0.55–0.59 here was one low draw. What C3 exposed is the galaxy bootstrap's under-coverage: its 95% interval is about 5× narrower than β̂'s true spread.

**Hypotheses, real data**

| subset | canonical | alt |
|---|---|---|
| point-mass | best 0.72 (Υ 0.66); 95% [0.48, 6.00]: NO POWER | best 0.88 (Υ 0.67); 95% [0.63, 6.00]: SUPPORTED |
| embedded | best 0.48; 95% [0.37, 0.72] | best 0.59; 95% [0.42, 1.07] |

- **H1** (point-mass interval contains β = 1): **pass**.
- **H2** (embedded interval excludes β = 1): **FAILED** on alt.

The points where the baryons look like a point mass prefer a sharper transition than all points together (0.72 / 0.88 against 0.48 / 0.55). Their β̂ also sits **above** what the estimator returns for synthetic P2 data.

## Standing

CFG9's principle is **not falsified** where it applies. The larger point: C3 shows that CFG4 H3's exclusion of P2 cannot be taken at face value. CFG14 finds the reason is the bootstrap's under-coverage, not an estimator bias.

The calibrated question is whether the full-sample β̂ = 0.48 / 0.55 lies inside the distribution β̂ takes under P2 truth. That is CFG14.

CFG9's README correction, "SPARC excludes P2's transition shape", stands only as far as CFG4 H3 does. It is therefore under review, pending CFG14.
