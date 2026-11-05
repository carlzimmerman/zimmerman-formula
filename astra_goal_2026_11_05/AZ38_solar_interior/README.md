# NOT EVALUABLE — realistic solar-interior data not located

Lane5(d), criteria1252c500e8. Kappa = 1/2 FITTED; not theory closed.
The required authenticated structure profile was not located locally.
No realistic interior was substituted by an analytic density law. The
download need is recorded in `../NEEDS_OWNER.md`; no data payload was fetched.

The recorded inventory includes359335 filenames, with ignored files and
hidden data included, excluding Git internals and this lane's own files.
It found zero candidate paths matching the declared model/profile patterns.
This is a reproducible discovery result, not proof that no unnamed table
exists anywhere. Earlier `sun09` paths belong to another source collection,
not an authenticated solar-interior profile.

The [official Model S source](https://phys.au.dk/~jcd/solar_models/) supplies
structure variables and identifies a corrected GONG l5bi.d.15 model after
an issue with the original Ledoux discriminant. Only the distribution-page
metadata was inspected. Size is unknown. This is a model-derived reference,
not raw observational data; future use must explicitly justify its role
as an imposed source or replace it with a framework-native stellar model.

## Local calculation that was executed

For a spherical density with total mass M and radius R, the Newtonian
potential with zero at infinity is

    -Phi_N(r)=G[M(<r)/r + integral_r^R 4pi rho(q)q dq].

At r0 the first term has its regular zero limit. For nonnegative density
and nonzero mass the right side is positive. Thus V3X's leading screened
relation K s=-2Phi_N/L_star² gives a positive stiff-branch coefficient
c_s²=gamma s=-Phi_N, independent of assuming uniform density. This proves
the sign within that leading approximation; it does not quantify its full
interior error or establish the complete covariant health operator.

The script independently derives and integrates two exact engine fixtures,
with x=r/R and w=4piR³rho/M:

- Uniform w=3 gives U=-Phi_N/(GM/R)=(3-x²)/2.
- Manufactured w=(315/16)(1-x²)^3 gives unit total mass and U(0)=315/128.
  This is deliberately an uncalibrated analytic test, not a realistic Sun.

Composite-trapezoid grids256/512 have maximum potential errors7.63e-6
uniform and2.504e-5 manufactured; pair changes5.73e-6 and1.878e-5, all
below1e-4. Mass errors also pass. The symbolically derived exact solutions
and Poisson identities supply independent known answers.

The illustrative center speeds are534.9km/s and685.2km/s respectively.
Their difference illustrates profile dependence, not a measured solar
correction. Both a0 footings and all declared L_star values are recorded
separately, including the a0-dependent normalized divergence. The leading
physical speed is independent of a0 by the displayed equation.

## Controls and reproducibility

Main21/21 checks, exit0. MUTATE15/21, exit1: negative manufactured density
fails density, mass and strict stiff-speed positivity on both footings.
The switch is applied: its negative-divergence side has zero stiff speed,
not an invented negative squared speed. Signed exact integrals and all
convergence checks still pass; uniform positive-density known answers stay
unchanged. Results and provenance are in separate main/mutant trees.

```sh
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ38_solar_interior/run.py
OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 -B astra_goal_2026_11_05/AZ38_solar_interior/run.py --mutate
```

Run from the repository root. Expected exits0,1 concern engine validation;
the scientific lane label remains NOT EVALUABLE. The main run took about3s,
single threaded, below93MB RSS. Filename counts may change with the shared
worktree; any discovered candidate still requires provenance inspection.

## Exact remaining work

Obtain and authenticate a density/pressure/radius profile; state its
model assumptions and framework transfer. Recompute the screened background
with the actual profile, establish convergence and cap/switch consistency,
then evaluate the coupled physical interior perturbations. Neither the
manufactured fixture nor positive leading c_s² completes those tasks.
The program proceeds to constraint causality while acquisition is deferred.
