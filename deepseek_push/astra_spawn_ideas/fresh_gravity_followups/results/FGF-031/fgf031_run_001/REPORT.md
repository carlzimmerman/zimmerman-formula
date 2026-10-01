# FGF031: one certified operator-error neighborhood

The finite pressure-target ambiguity survives every real perturbation in
one explicitly certified neighborhood of the saved response. This is a
mathematical tolerance, not a measured instrumental error estimate.

For the old square block U, new column c and fixed target L, exact arithmetic
gives kappa=||U^-1||_infinity,ind approximately297.36942960,
H=||U^-1 c||_infinity approximately10.70717766, ||L||_1=10, and nominal
mu=-L U^-1 c approximately0.16303084957824435. Choose

    delta = min(1/(4kappa), mu/[4kappa ||L||_1(1+H)])
          ≈ 1.170742196159423e-6.

The declared uncertainty set is

    max_i sum_j |E_ij| <= delta,   max_i |e_i| <= delta.

Thus E uses the **induced row-sum infinity norm**, not its largest entry.
A sufficient common entrywise bound on all E and e coefficients is
**delta/15 ≈7.804947974396155e-8**. Confusing the entrywise and induced
matrix norms is explicitly rejected by a control.

Every allowed U+E is invertible. The inverse-column change is bounded by
0.004077190684604218, giving the uniform target-sensitivity interval

    0.12225894273220218 <= mu_E <=0.20380275642428652.

These displayed decimals summarize exact rational bounds saved in the raw
result; use those rationals for exact endpoints. In particular mu_E is
uniformly nonzero, so the fifteen-row sixteen-coefficient pressure model
remains target-nonidentifiable throughout this neighborhood.

The inherited positive decreasing baseline has smallest pressure gap
6.737946999085467e-8. A common step
**eta≈1.572632500085328e-9** preserves every pressure gap at least half
that smallest gap for the two witnesses p0+/-eta n_E. Their gradient
separation is uniformly at least **3.845367735334641e-10**. The step and
baseline are common, but each uncertain operator has its own null vector
n_E and its own common synthetic data vector. This is not a statement that
one unchanged pair fits every response or the actual observed bins.

Zero-error checks reproduce the pinned earlier exact target sensitivity and
null direction and verify equal-bin strict witnesses. At the analytic bound
threshold delta≈4.676456483419311e-6, the sufficient lower bound on mu_E
reaches zero while the inverse criterion still holds. The correct verdict
there is **inconclusive**, not restored identification. The zero perturbation
remains an ambiguous member of that larger uncertainty set. No radius scan
or perturbation sampling was performed.

## Explicit pressure normalization

FGF019 defines x=r/R_t and **p(x)=C_SZ R_t P_e(R_t x)**, with
C_SZ=sigma_T/(m_e c²). The retained pressure coefficients p, the coordinate
x and Compton-y are dimensionless. The saved target is dp/dx, and the
physical electron-pressure derivative is (dp/dx)/(C_SZ R_t²). Thus the
reported absolute response bounds are y per normalized p. The unchanged
matrix is not a response per unconverted keV/cm³ pressure coefficient.
The original derivation and implementation are separately hash-pinned in
the packaged result as normalization ancestry; successful run inputs and
outputs were not edited after execution.

L, basis, support6, fifteen annuli, pressure normalization and fixed-zero
offset are held fixed. No target-law, pressure-basis or normalization
uncertainty is included in the E,e error model.

All26 controls passed using exact Fraction inequalities. The sole bounded
run took0.203217 seconds; its manifest validates. The uniform theorem over
real perturbations follows from the analytic norm inequalities, rather than
from a finite test grid. No computational failure occurred.

This finite robustness route stops here. Neither agreement between response
implementations nor this chosen radius authenticates the real beam, geometry,
calibration, finite-support or continuum errors. The missing empirical inputs
are an actual response error budget and a scalar outer-pressure constraint
that couples to the surviving mode. No actual pressure fit, covariance,
MOND force, mass discrepancy, metric/photon sector or theory closure follows.
Future source conversion preserves both a0 footings, separate constant-vacuum/H
histories, Q/RAR/registered M and density/total-pressure conversion.
