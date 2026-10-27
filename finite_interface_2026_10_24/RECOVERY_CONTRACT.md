# FI-3: direct species force and displaced-front recovery

Use recorded FI-2 large-disk Rj5b c.03 epsilon1e5 n256 candidate. No refit.
Its phase fractions pass, phase Hessian is positive and full common-potential
force fails. Check the actual T potential away from exact stationarity:
mu_T=mu_c+(1-q) E_x/(m h'), and mu_F=mu_c-q E_x/(m h').
Use the stable trig ratio for mu_T. In pure T its correction vanishes.
Finite-difference an added T mass while holding F fixed to verify mu_T.

Displace the recorded outer-front translation mode by +/-.2 kpc, relax100
internal units with the same positive metric and independently accumulated Q.
Compare phase endpoint to unperturbed candidate and E+Q to initial energy.
Compute exact T-force imbalance again. Recovery is phase-only stability at
fixed density/baryons; it is not live radial stability or preservation in Gyr.
