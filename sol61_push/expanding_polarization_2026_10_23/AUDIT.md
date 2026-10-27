# XP self-audit

Claim card: for the explicitly written preferred-frame action on a periodic expanding background, conserved comoving masses and fixed physical coefficients imply the displayed matter/field equations and expansion-work identity; its one-mode variational restriction has the stated mode equations. Hypotheses: A>0, chi>0, |P|<1, scalar sector X=0, physical orthonormal vector components, fixed preferred foliation, no baryon pressure. Conclusion does not include uniqueness, full covariance, relativistic health, primordial generation or core formation.

Dependency audit: conserved mass scaling and physical-gradient convention -> reduced Lagrangian -> Euler-Lagrange equations -> canonical Hamiltonian -> partial-lnA work. These are internal algebra/conventions, with finite-difference and numerical-flow checks. MINISUPERSPACE.md adds an assumed homogeneous gravitational action and derives its lapse constraint/pressure; the full inhomogeneous metric sector is not addressed. This is self-review, not independent certification.

Checks performed:
- Wbar32-node versus64-node force quadrature over100 p values to .95: maximum relative difference2.23e-15.
- Six canonical nonlinear cases repeated at tighter ODE tolerance: maximum relative-or-unit-scaled output difference1.56e-7; same stopping categories.
-48 baseline histories: maximum normalized integrated expansion-work residual8.58e-7. Six tracking-state histories:1.38e-10.
- Canonical Hamiltonian finite differences at a separate declared test state: expansion partial error4.88e-11; coordinate-gradient maximum relative error3.92e-10. These test signs and normalization independently of time integration.
- Six large-scale growth histories reach the present; work residual<=8.31e-9. Tracking k1 repeated with100 times tighter tolerance changes retained growth by3.68e-10 absolute; repeat work residual3.84e-11.
- All numerical checks in completed runs pass. One initial action-check run failed only when serializing a NumPy boolean; script/log/failed manifest preserved. action_check_v2.py only casts that boolean to Python bool. A completed execution is not a physical interpretation pass.

Interpretation gates: bound three-dimensional cores NOT ESTABLISHED; selected remnant mass NOT ESTABLISHED; abundance and spatial occupation NOT ESTABLISHED; joint dwarf/rotation/cluster fit NOT ESTABLISHED; inherited99% growth target at k1 FAILS for all three tested field preparations. No data likelihood used.

Adversarial findings and scope:
1. A one-mode restriction removes harmonics and fragmentation. It cannot prove absence of cores in the full system. Matter is only quadratic and is stopped at .3, so neither positive nor negative contrast stops are collapse certificates.
2. Initial stationary fields are not a cosmological initial-state derivation. Initial chi can be large, and zero field velocities are distinct from derivatives tracking equilibrium. No attractor or primordial probability has been derived.
3. The frozen-mode inertia theorem from the prior checkpoint does not bound arbitrary expanding transients. Differences from quasistatic growth are not contradictions to that theorem.
4. For solver trial states only, the logarithm denominator and chi are protected outside the numerical domain. Reported histories stop within |p|<=.95 and chi>=.05; none in these runs reaches those stops. This extension must not be used for physical predictions outside the declared domain.
5. Maxima sampled on1001 times are diagnostics, not rigorously certified continuous bounds. ODE event localization controls the stopping conditions.
6. The dynamical homogeneous background was derived but not integrated. The actual runs use imposed EdS from z1100, with pressureless baryons; radiation-era, baryon-pressure and metric effects remain missing.
7. The reference-density subtraction is spatially global on the chosen periodic slice. The work accounting includes its expansion dependence; a covariant local clock/current construction remains a separate obligation.
8. At static A=1 the local scalar action is inherited. This is not a proof that assembled galaxy solutions, rotation curves or relativistic lensing remain unchanged.
9. Stationary field root conditions and tracking derivatives were reconstructed algebraically. Tracking follows the initial tangent to the equilibrium branch, not an exact cosmological growing solution.

Proofreading self-review covered the new action, work identity, minisuperspace extension and reports: consistent A versus alpha, physical versus N-time derivatives,1/4 cosine-average factors, Hamiltonian gravitational sign, background rest mass counted once, and qualified numerical conclusions. No predecessor files edited. No external theorem or novelty claim underlies the algebra.
