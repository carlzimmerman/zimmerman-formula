# Joint reconstruction on the pressure-admitting no-slip geometry

Base: 4fe59c19248663e7e8282dd11e9f55b9badefe17, containing the verified
general-pressure inverse aeefebd8. Previous goal turn: progress. Full gravity
objective remains OPEN and unchanged; no completion by conditional certificates.

Root owns a fast analytic derivative kernel and bounded shared-action search.
reference/ independently differentiates the original general-pressure inverse
at arbitrary precision, checks actual EF equations and health, and refines
any numerical point. Same F(X),P(X),G(X), one explicit clock, global a0=1,
fixed distinct exterior eps labels. No baryonic source calibration is assumed.

Use B=4/[1+sqrt(1-4ry)]²,g=yB,r=eps/sqrt(y mu), where ry here means the
product r*y. This is imposed equality of logarithmic potentials, not a
forward PPN or observed law. Retain full nonzero geometric radial pressure.

First discriminator: shared pressure and two normalized action jets, then
both preservation equations, then local health with the SAME f,j. A passing
point must be independently refined and differentiated again; no optimizer
or small determinant alone is a PASS. Other charts and unsearched points
remain open. The initial computation is a small deterministic continuation
from known seeds, not an unrestricted resource commitment.
