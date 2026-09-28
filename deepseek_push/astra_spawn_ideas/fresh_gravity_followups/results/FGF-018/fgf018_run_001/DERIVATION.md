# FGF-018: error-box continuity-sign certificates

Actual task setup started 2026-09-27T19:30:52Z. Agent: Astra
/root/catalogue_audit. No DeepSeek execution. This changes the knot masses,
not the registered interpolation function or force law.

## Premises and exact algebra

Retain a=kappa c sqrt(G rho_Lambda), kappa adopted; both a0=9.3619e-11 and
1.1279e-10 m/s^2. Constant-vacuum a and the separate H comparison
 a(z)=a0 sqrt[.315(1+z)^3+.685] are not identified. The pressure identity
 a^2=kappa^2 G(-p_vac) requires p_vac=-rho_Lambda c^2; this is distinct from
the gas pressures in the Euler equation. Q=sqrt(B^2+aB),
R=B/[1-exp(-sqrt(B/a))], and M is the source-pinned registered monotone
implementation. No Newtonian missing-mass substitution is used.

At adjacent original gas knots (r1,m1),(r2,m2), the declared interpolant is
 M(r)=m1 (r/r1)^s, s=ln(m2/m1)/ln(r2/r1).
Its density is rho=s M/(4 pi r^3). For s>0 and steady spherical source-free
flow, r^2 rho u=constant implies u proportional to r^(1-s), hence
 u du/dr=(1-s)u^2/r.
The inward-positive gravity magnitude F, outward radial velocity u, and
outward material acceleration obey
 u du/dr=Delta+gnt, Delta=gH-F(B;a), gnt=-Pnt'/rho.
With rho>0 and Pnt'<=0, Delta>0 and s>=1 contradict this equality. The task's
strict sufficient certificate s>1, Delta>0 will be reported as such. Failure
of that certificate is not a physical repair or a solution of all equations.

At gas knots, L=MGAS-MGAS_LO and U=MGAS+MGAS_HI (error magnitudes).
At star knots, L=MSTAR_LO and U=MSTAR_HI (endpoints).
At hydro knots, L=M_FORW-EM_FORW and U=M_FORW+EM_FORW (symmetric errors).
All masses are solar masses, radii kpc. Use FITS per-profile R500 for R/R500.
The box is a deterministic domain, not a confidence region or independent
posterior. Unknown correlated systematic errors may lie outside it.

For positive endpoints, the exact independent-box lower slope is
 s_min=ln(L2/U1)/ln(r2/r1).
Interpolation of positive endpoint masses is increasing in both knot values.
At a shell strictly inside each source's own interpolation support,
 Delta_min=G M_sun Mh_low/(r kpc)^2
           -F(G M_sun [Mgas_high+Mstar_high]/(r kpc)^2;a).
Thus s_min>1 and Delta_min>0 at one interior shell exclude the specified
steady-flow explanation for every allowed profile. It is unnecessary for the
bounds to be jointly attained: simultaneous lower bounds suffice. A negative
bound is not evidence that the actual Delta is negative.

## Interpolation and global constraints

Construct knot intervals first, then interpolate the endpoint profiles using
the declared log-log interpolant. This bounds arbitrary allowed knot masses.
Interpolating central/error curves separately gives a different family; it
will be recorded only as a sensitivity, not substituted into the knot proof.
No derivative is assigned at a gas knot, where the interpolant may have a
slope jump. Slope indices are from original gas knots even when an interval
is clipped at 100 or 1000 kpc. Midpoints are geometric means of clipped
endpoints, always strictly inside the original gas interval.

Main certificates use conservative rectangular bounds. Impose positivity of
gas and nondecreasing enclosed gas mass separately. For any sequence with
L_i<=m_i<=U_i and m_i<=m_(i+1), exact tight one-knot bounds are
 L_i^mono=max_(j<=i) L_j; U_i^mono=min_(j>=i) U_j.
If any L_i^mono>U_i^mono, the full monotone family is empty and must not yield a
vacuous physical certificate. Report this explicitly. Gas monotonicity
implies slope>=0; strict positive gas density requires s>0. The comparison of
hydro/star monotonic feasibility is also recorded, without silently imposing
an empty extra family. For positive nonempty boxes the rectangle remains a
superset of every monotone/correlated subset and any certificate is valid there.

When a slope interval fails the strict certificate, attempt a full, positive,
strictly increasing gas-knot witness with 0<s<1 at that interval. Use tightened
bounds to select two feasible endpoints, extend nondecreasingly to all other
knots, then mix slightly with a strictly increasing central profile if needed.
Verify every original mass bound and every monotonicity inequality. Such a
witness removes only this local sign certificate; other shells may still
contradict the model, and Euler, pressure and boundary conditions remain unsolved.
If only Delta fails, report inconclusive unless an explicit simultaneous
mass-profile witness is constructed. No negative certificate is labeled repair.

## Bounded computation contract

Seven original measured-star X-COP clusters; all original gas intervals
intersecting 100–1000 kpc; original 100,300,1000 kpc interior shells plus one
midpoint per intersecting gas interval; Q/R/registered M, two normalizations,
vacuum/H. No extrapolation, no random sampling, no additional observations.
Check central slopes/forces against pinned stage-three outputs, exact rational
synthetic slope cases using mass-ratio comparisons, endpoint interpolation
corner enumeration, monotone feasibility and counterwitnesses. Bound each
numerical process to 120 s wall, 110 s per-process CPU, 1 MiB logs, cooperative
one-thread numerical libraries. No claimed memory/affinity cap. Stop after the
fixed deterministic domain. Missing input or failed implementation check is
not a scientific refutation. Binary64 bounds are analytic extremum formulas
evaluated numerically with sign margins, not directed-rounding interval arithmetic.
