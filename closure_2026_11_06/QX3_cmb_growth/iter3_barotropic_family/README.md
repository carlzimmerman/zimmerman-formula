# QX3 iter3: every barotropic K(Q) sector: FAIL (class no-go on the frozen grid)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (93562260e2). This is the pre-planned
mutation of iter2.

**Class:** p = A(Q-1)^n gives lambda_J proportional to rho^beta with beta = (2-n)/(2(n-1)). Both exponent identities are
Lean-certified: `barotropic_beta`, and `beta_zero_iff` (n = 2 is iter2). The sweep covers 41 beta values in [-2, 2] and
61 mu0 values in [0.1, 1e5] Mpc^-1, at iter2's worst corner.

## Results (iter3.json)

- Galaxy gate G3' (lambda_J >= r_ta = 234 kpc at turnaround) and forest gate G4' both pass on only **35 of 2,501**
  members, all with beta >= 0.5. These are sectors that stiffen at high density, so they avoid galaxies.
- **Every one of the 35 fails growth G2'.** The closest is beta 1.4, mu0 1.6e4, at Delta chi^2 = 92.6 against a line of 4.
  The reason: the early universe is far denser than any galaxy. A sector stiff enough to stay out of galaxies is stiffer
  still at z > 100, so it misses the growth that sets the CMB-lensing shape.
- Members that cluster early (beta <= 0) collapse into galaxies (iter2 is beta = 0).
- Known answer: beta = 0 reproduces iter2's G2 at mu = 1e3 exactly (Delta chi^2 1252.75 in both).
- MUTATE (G3' flipped): a member passes all three at once (beta -2, mu0 1e5, Delta chi^2 1e-10). The sweep has power.

## Label

**FAIL: no barotropic K(Q) sector on this grid both builds the CMB-lensing shape and leaves the a0 law alone in
galaxies.** The no-go is set by an ordering. Lensing growth needs clustering at early-universe densities. Galaxies need
no clustering at galaxy densities. Galaxy densities sit far below early-universe densities, so a Jeans length that depends
only on the sector's own density cannot separate the two. To escape, a sector's Jeans length has to depend on something
other than its own density, for example the local acceleration (a0-switched) or the environment. That is what the law
itself does, and that route is the open question.
