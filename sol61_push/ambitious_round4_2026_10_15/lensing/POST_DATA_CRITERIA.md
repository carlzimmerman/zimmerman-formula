# Round-four bounded lensing successor — criteria fixed before new fits

15 October 2026. All observed points and prior fits have already been seen.
This is a post-data numerical successor, with no prospective or holdout claim.
Historical scripts, criteria, K2 failure and scores remain unchanged.

## Candidate and units

Canonical a0=9.3603e-11 m/s², G=4.30091e-3 pc (km/s)²/Msun,
rM=sqrt(G Mb/a0). B includes point Mb plus the unbounded exact-law excess
density rho(s)=1/[2 pi s sqrt(1+4s²)] in Mb/rM³ units. D truncates this
density exactly at e(N)=sqrt([(2*5.364*N+1)²-1]/4), containing excess
mass 5.364*N*Mb. No nearest-N grid is used. Retention is the inherited
piecewise curve, with N=1/f and f=fret(Mb/[fb*f]), fb=1/6.364.
Report two conventions if source units remain unresolved: physical-Msun
argument log(Mta/Msun), and source-Msun/h argument log(h*Mta/Msun),
h=.6736. Neither may be selected by fit improvement. Root's independent
source audit decides the source interpretation; both remain explicit sensitivity.

Data use h70=1 (H0=70 km/s/Mpc), treating tabulated Mpc/h70 radii and
h70 Msun/pc² ESD numerically as physical Mpc and Msun/pc². Simulation h
is separately .6736. This is the inherited observational footing, not a
cosmology distance reanalysis. P_grav at z=.2561784341 is a finite-band
phenomenological environmental template, not an isolation-matched
galaxy-matter cross-power. rho_com=Omega_m*2.775e11, Omega_m=(.02237+.1200)/h².
Convert Rcom=Rphys*h/a and DeltaSigma_phys=DeltaSigma_com*h/a²/1e12.

P(k) is piecewise linear in native k, exactly zero outside saved
[kmin,kmax], with Gaussian smoothing exp[-(.05*k)²]. No spectrum
renormalization, extrapolated low-k modes or sigma8 repair is allowed.
Use dense k interpolation for transforms. Each trial mass in both B and D
uses the same exclusion rule: subtract environmental density inside the
finite catchment radius rM*e(N) computed at that trial mass and unit convention.
B's own infinite excess remains an explicit physically inconsistent
comparison family, not a finite inventory. Both models receive four Mb
and four nonnegative constant biases, optimized using the same full covariance.

## Controls and decision gates

Before fitting, validate zero-exclusion Hankel DeltaSigma against an
independent real-space LOS/cylindrical integral of the same smoothed finite-band
spectrum: max relative difference <=1% at the 15 fitted radii, denominators
max(abs(reference), .01*max(abs(reference))). Also require dense-k/LOS
refinement <=1%; exact finite one-halo projection versus independent direct
quadrature <=.1%; finite enclosed excess mass and external point-tail identity
<=1e-9 relative; exact edge identity <=1e-10; a deliberate rho normalization
mutation must exceed 10% in its corresponding projection.

Use 4D bounded mass optimization [9.5,12] after exact NNLS profiling of
the four nonnegative biases in whitened coordinates. At least four deterministic
starts; convergence gate best two successful starts within .05 chi² and
independent optimizer/refinement within .5. Record every start and failures.
Dense exclusion interpolation refinement must change final chi² by <.5
and template by <1% under the same floor convention. Report no-exclusion
mutation per bin: sensitivity passes if at least one bias or predicted
environmental contribution changes >10%; give complete vector, not all-bin claim.

Report full 60-point and primary R<=.31 Mpc fits separately, predictions,
one/two-halo components, residuals, whitened residuals, C^-1 residual,
signed additive block contributions r_b^T(C^-1 r)_b and nonadditive conditional
increments. Use nominal n-8 chi-square p values with boundary caveat.
Empirical closure requires all controls, all-radius D-B <=4 and nominal
p_D>=.01. Relative improvement against an unacceptable reference cannot close.

If D fails absolute closure, isolate the cheapest physical profile falsifier:
fit an explicitly diagnostic nonnegative independent point-Mb plus 1/R
excess amplitude and the same environmental template, without claiming a
new theory; compare covariance-aware residual patterns and feasibility of
the exact-law linked point/excess ratio. Any extra diagnostic criteria are
descriptive, not a revision of the above closure test.

## Resources and non-claims

Each command is bounded by Mathbox runner, <=60 s wall and <=55 s
per-process CPU, numerical-library threads=1, log cap <=1 MiB.
No production simulation. Float64 numerical evidence, no universal proof,
no unique cosmic ownership, formation, gas identification, native initial
conditions or full physical-theory claim. A timeout is inconclusive and
preserved, with a smaller explicit follow-up contract rather than erased.
