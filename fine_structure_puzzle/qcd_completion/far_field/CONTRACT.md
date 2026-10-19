# Far-exterior effective-action contract

Established 2026-10-19 UTC before computational experiments or reading the
normalization-bridge and angular-mode reports. This contract fixes the analytic
problem; later amendments must be separate dated files or explicitly marked.

* Microscopic theory: Euclidean SU(2), Hermitian generators
  `tr(Ta Tb)=delta_ab/2`, covariant derivative on charge q = +/-1 is
  `D_mu=partial_mu-i q A_mu^3`.
* Geometry: `R^3 x S^1_L`, fixed physical circumference L, periodic bosons and
  ghosts, background Feynman gauge. Spatial radial shell `r_c<r<R`.
* Background: `A_4=h(r) T3`, `h=v-1/r`, radial Abelian magnetic field
  `B=n_mag r_hat/r^2`, with `h>0` throughout the shell. For the full KK tower
  take `0<Lh<2pi`, away from massless endpoints; center holonomy is permitted.
* Operators: `H_mu nu=-D^2 delta_mu nu-2 ad(F_mu nu)` with the corresponding
  Hermitian charge-sector spin operator `V_mu nu=2 i q F_mu nu` up to an
  irrelevant overall sign; `M=-D^2`.
  `Gamma_1=1/2 Tr_vector,adj log H-Tr_adj log M`.
* We first compute the charged color pair and static circle frequency, then
  all charged circle frequencies. Gamma is dimensionless. One frequency
  contributes a three-dimensional integral, without an additional L.
* Observable: the local bulk effective action through zero and two derivatives
  on the fixed, off-shell Coulomb profile, including the coefficient of 1/R
  after explicitly declared subtractions. Logweight is `-Gamma_1`.
* Renormalization: dimensional regularization for each 3D local integral;
  full-tower logarithmic UV divergence subtracted against a declared harmonic
  sum and absorbed in the 4D strong coupling. Scheme constants are kept
  explicit. The vacuum potential and derivative sectors are reported
  separately before combining them.
* Computational assertion to test, if code is used: finite symbolic and
  numerical checks of the analytic momentum/heat-kernel and digamma formulas,
  with all domains, cutoffs, precision, tolerances and command recorded in the
  run manifest. Such tests do not prove the derivative expansion globally.
* Exclusions: the origin/core, shell boundary determinants, neutral determinant,
  boundary conditions, full angular sums, physical vacuum stress, a screened
  deformed-theory saddle, the map from strong coupling to electromagnetism,
  and an electromagnetic alpha prediction.
* Validity: local expansion in spatial gradients/field strengths divided by
  charged masses; in particular `r m_min(r)>>1` in the retained shell. The
  Coulomb profile is an off-shell background at arbitrarily large R in a
  theory with a positive holonomy-scalar mass. No fit to measured cosmic data.

