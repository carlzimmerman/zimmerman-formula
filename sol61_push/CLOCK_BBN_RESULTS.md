# Conditional nucleosynthesis rejection of the canonical-clock branch

## Source and translation

Checked 2026-09-30: Alvey, Sabti, Escudero and Fairbairn, *Improved BBN Constraints on the Variation of the Gravitational Constant*, [arXiv:1910.10730v2](https://arxiv.org/html/1910.10730), 5 February 2020. Equation (9) reports the BBN-only 95.4% interval 0.98 ± 0.06 for G_BBN/G_0. Their calculation varies the expansion coupling, includes neutrino decoupling, holds reaction physics fixed, and marginalizes over baryon density. No CMB baryon prior is needed for that result. This is a published historical likelihood, not a newly run 2026 likelihood.

The transfer identifies their G_BBN/G_0 with our R=G_cosm/G_N through H²=(8πG_N/3)Rρ. It requires constant lambda and gravitational parameters through BBN, standard matter/radiation with unchanged weak and nuclear rates, negligible additional clock stress, and today's local Newton calibration from the adiabatically relaxed static model. Our scalar must stay at q0, with U0 negligible compared with BBN radiation. This transfer concerns the homogeneous expansion and particle kinetics; no CMB perturbation fit is imported.

## Exact conditional bound

The equations in CANONICAL_CLOCK_RESULTS.md give, with zero additive vacuum constant,

    C = Lambda_geom/a0_N² = 4D(1+D)²/[3(3lambda−1)],
    R = 2D/[(1+D)(3lambda−1)],  D>0, lambda>1.

Imposing C=32π gives D(1+D)²=24π(3lambda−1) and R=48π/(1+D)³. Since D(1+D)² is strictly increasing for positive D, lambda>1 forces D>Dmin, where Dmin(1+Dmin)²=48π. The strictly decreasing R therefore satisfies

    R < 0.8238740919142051,
    H/H_standard < 0.907675102618886.

This entire interval lies below the source's lower endpoint 0.92. Under the transfer assumptions, the 32π version of this branch is outside that published 95.4% interval. We do not infer a stronger significance from the rounded interval or claim to have recomputed primordial abundances. This is a conditional observational rejection, not a rejection of all theories yielding 32π.

## Radiation loophole has a calculable cost

An ideal instantaneous-decoupling diagnostic uses three neutrino species consistently. Before electron annihilation, g*=43/4 and an extra neutrino-like species adds 7/4. Matching the standard expansion requires deltaN=(43/7)(1/R−1)>1.31320587. After annihilation, rho_rad/rho_gamma=1+alpha(3+deltaN), alpha=(7/8)(4/11)^(4/3); matching instead requires deltaN=(1/alpha+3)(1/R−1)>1.58264006.

Thus one fixed neutrino-like abundance cannot exactly restore the standard expansion in both ideal limits. At the limiting R, early matching leaves the late H² ratio 0.97001571; late matching leaves the early ratio 1.03613625. These numbers are thermodynamic diagnostics, not confidence bounds. Incomplete decoupling, entropy exchange, nonstandard temperatures and clock evolution require a full thermal/network calculation. In particular, a surface gas need not redshift like four-dimensional radiation. Extra radiation remains an open modification, not a demonstrated rescue.

## Evidence and decision

clock_bbn.py passes 12 bounded checks of the root, endpoint, elimination identities, four parameter samples, and the ideal radiation mismatch. The monotonicity argument above establishes the universal positive-D bound; the samples do not. Execution provenance is recorded in runs/clock_bbn/manifest.json.

The unmodified standard-radiation, constant-coupling branch should no longer be developed as an observationally viable solution. A revised mechanism must independently determine the coefficient while changing this prediction, and must also address the separately established finite-cone obstruction. Adding adjustable radiation or an additive vacuum constant does not explain exact 32π.
