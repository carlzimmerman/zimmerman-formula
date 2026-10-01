# FGF-021: finite pressure extrema, derivation before execution

Agent /root/pressure_extrema. The fixed FGF-019 binary64 matrix is the
mathematical input; no precision claim extends to its physical approximation.
Every stored coefficient is interpreted as its exact binary rational for the
certificate. Set s=the stored binary64 number 1e-5. Let q_i=(p_i-p_(i+1))/s
for i=0,...,14 with p_15=0; q>=0. Then p/s=Tq with T upper triangular ones.
The last coordinate b is the post-convolution map offset divided by s, free
in sign. Define E=H diag(T,1), c=L diag(T,1). Both products are formed in
exact rational arithmetic for verification. The synthetic data are exactly
d=H baseline/s, not a rounded dot product subsequently treated as exact.

Minimize c.u and -c.u subject to Eu=d and q>=0. Multiplying objective by s
restores the normalized-coordinate electron-pressure gradient in FGF-019.
The 15 pressure values remain free except positivity/monotonicity; support,
beam, twelve annuli and distance remain inherited. No added pressure ceiling.

For generic inequalities Au<=a and equalities Eu=d, a certificate consists
of a feasible u and y,z such that c=E^T y+A^T z with z<=0. Then c.u>=y.d+z.a.
Equality of these rational objectives proves an attained global optimum for
the fixed finite rational model. A floating LP selects a candidate active
vertex only. Independent Fraction Gaussian elimination reconstructs its
primal vertex and dual multipliers and checks *all* constraints exactly,
including dual sign, stationarity, complementary slackness and zero gap.
This also handles finite gradients when boundedness of every coordinate has
not been separately proved. An exactly positive/decreasing baseline is
feasible: convex mixing with it approaches each closed-cone endpoint from
strict positivity. Thus the closed interval gives infimum/supremum over the
strict family; endpoints with flat/zero nodes need not be attained there.

For actual observed bins d_obs/s, introduce t>=0 and minimize t under
Eu-d_obs/s<=t and -Eu+d_obs/s<=t, q>=0. The same exact primal/dual checks
certify the smallest uniform deterministic residual s*t. This is a finite
approximation requirement, not measurement noise, confidence or exclusion.
Without authenticated tolerance/covariance no real-map gradient interval is
accepted. Fitting a free offset does not authenticate instrumental background.

Controls: exact two-variable simplex fixture with extrema 0 and 1; nuisance
frozen square solve; prior null witness lies inside new extrema; 10x synthetic
amplitude scaling; deliberately damaged dual fails exact stationarity; actual
map exact fit and the residual certificate are compared without interpreting
their difference statistically. The solver selection tolerance is 1e-9 in
scaled coordinates, candidate active tolerance 1e-7. Final rational checks
have zero tolerance. Float residuals are diagnostic, not certificates.

This is solely an observation-functional calculation. No force, discrepancy
or mass has been computed. Both a0=9.3619e-11 and 1.1279e-10 m/s^2, constant
vacuum and separately a0 E(z), and Q/RAR/registered M remain distinct in any
future hydrostatic bridge P_total'=-rho F(B;a). Neither a metric/photon coupling
nor continuum point-gradient bounds follow from this finite result.

One deterministic input operator, no random sample, binary64 candidate solve
plus exact rational checks; <=120 s wall, 110 s CPU, cooperative one-thread
library cap, 1 MiB logs, no memory bound asserted. Stop on failed certificate
instead of calling numerical extrema sharp.
