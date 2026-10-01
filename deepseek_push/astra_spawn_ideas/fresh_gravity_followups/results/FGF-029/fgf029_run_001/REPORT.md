# FGF029: finite identification depends on the pressure-support restriction

Adding only a free pressure coefficient at x=5, with the zero endpoint moved
to6, restores one exact target-changing ambiguity in the same fifteen bins.
The old fifteen pressure columns remain bitwise unchanged. The new hat is
projected through the inherited beam and normalized annular masks; all radius,
map-patch, mask-patch, transfer and fifteen weight hashes match FGF028. The
nearest source-patch edge is at8.83027 target radii, beyond the new support6.

The extended15x16 matrix has exact rank15, and adjoining the target raises
rank to16. With t=p(5), the exact target decomposition is

    g = w d + mu t,      mu ≈ +0.16303084957824435.

Here w is the original fifteen-bin target reconstruction row, and fixing
the data changes all old pressure coefficients by -M^-1 k times the change
in t. The new outer coefficient is a coordinate for distributed pressure
freedom; the ambiguity is not physically confined to the outermost shell.
Exact inverse, null vector and target identities are saved in results.json.

An explicit extended synthetic baseline uses p(x_i)=1e-5 exp(-x_i), including
p(5)=6.737946999085467e-8 and p(6)=0. Its synthetic bins differ from those of
the earlier truncated baseline; neither is a fit to the actual observed map.
Two exact strictly positive/decreasing perturbations have:

| Quantity | Plus witness | Minus witness |
|---|---:|---:|
| p(5) | 7.192650938270014e-8 | 6.283243059900921e-8 |
| Target dp/dx | -3.684187494430860e-6 | -3.685670109821096e-6 |

Their fifteen synthetic observations are identical in exact rational
arithmetic. The exhibited gradient separation is0.04023457358% of the
baseline magnitude. This is a constructive non-uniqueness witness, not a
sharp maximum ambiguity or evidence of a discrepancy-sized gravity repair.

For one further hypothetical response row r=(r_old,r_new), the remaining
target is identified iff r_new-r_old M^-1 k is nonzero. Measuring the new
coefficient directly is a positive algebraic control; repeating an existing
row is a negative control. Neither is asserted to be an available calibrated
instrument observation. Pressure inequalities alone do not remove the
displayed interior ambiguity.

New-hat analytic LOS projection agrees with direct LOS quadrature at nine
declared impact radii. Exact controls reject a damaged null vector, preserve
the old model when t=0, and confirm all witness pressure gaps and observations.
The bounded run completed in2.213921 seconds and its manifest validates.
`extended_response.npz` contains the new column, unchanged old matrix,
combined15x16 matrix, nodes17, baseline16, target16, offset column and row labels.

The changed support is a hypothesis test, not evidence that this extended
pressure profile is measured. The result is conditional on the inherited
finite basis, fixed-zero offset, fiducial distance and beam/FFT approximations.
There is no covariance, actual-map fit, continuum conclusion, force or mass
inference. Later MOND bridges retain both a0 normalizations, separate vacuum/H
histories, Q/RAR/registered M and the density/total-pressure conversion.

The specific remaining measurement obligation is to constrain p(5), or an
equivalent response row with nonzero coupling to the saved null direction,
under justified support and response assumptions. This experiment stops at
that obligation; no further support or annular sweep is claimed.
