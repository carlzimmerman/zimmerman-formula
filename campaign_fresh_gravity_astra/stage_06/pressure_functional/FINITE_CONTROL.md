# PF1 finite exact control, separate from the smooth-profile theorem

Use dimensionless x in [-2,2], pressure p0=10, and the two toy observations
integral p dx and integral x p dx. These are not ACT/Planck kernels.
For n in {2,8,32}, set delta=1/n² and
u=(1/n) phi(x/delta), phi(t)=t(1-t²)^3 on [-1,1], zero elsewhere.
This compact function is C², not C-infinity; the finite control does not
instantiate every regularity hypothesis of PF1's smooth theorem.

Exact polynomial integration gives integral u=0 and integral x u=32/(315 n^5).
Let h_plus=140 t³(1-t)³ with t=x-1 on [1,2], zero elsewhere,
and h_minus(x)=h_plus(-x). Each has integral 1 and first moment +/-3/2.
The compensation coefficients are c_plus=v1/3 and c_minus=-v1/3.
Then p=p0+u-c_plus h_plus-c_minus h_minus has exactly unchanged observations,
p'(0)=n, and is bounded below by 10-1/n-(140/64)|c_plus|>0.
The derivative of either compensation vanishes in the local neighborhood.

The executable control uses rational arithmetic and independent polynomial
integrals, not a numerical quadrature tolerance. Three scales show the stated
finite family only. Omitted compensation and reversed compensation fail the
first-moment equality; duplicate compensating functions fail the rank condition.
No physical force, source discrepancy, catalog likelihood or instrument
calibration is computed. The dimensionless-to-framework interpretation is
exactly the conditional bridge in DERIVATION.md; both a0 normalizations and
vacuum/H histories remain distinct there.
