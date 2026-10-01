# Independent target-information derivation

Let theta=(15 finite nodal pressures,b), d=H theta, and fix b=b0.
C stacks the twelve stored measurement rows and the offset selector. Treat
stored binary64 entries as exact rationals; this verifies the stored operator,
not a continuum integral or an authenticated instrument response.

Compute RREF of C directly, independently of the worker's block inverse.
With first twelve pressure columns and offset pivotal, choose three canonical
null columns N whose free rows 12,13,14 form I3. Every solution is theta_part+Nz.
The remaining target row is ell=L N. For additional observation rows W, their
unmeasured response is D=W N. The target is identified on the entire affine
family exactly when ell lies in row(D), since that is equivalent to ell
annihilating ker(D). At a strictly positive, strictly decreasing baseline the
same condition is necessary for local identification under those inequalities:
any violating null vector can be scaled both ways while retaining all margins.
It is sufficient globally regardless of inequalities. Boundary-only feasible
families may identify the target without the row condition, so the converse
must retain the strict-interior hypothesis.

A synthetic row W_plus=[0_inner,ell,0_offset] gives D=ell and identifies the
target while leaving two unmeasured pressure directions. A coordinate row
selecting a free pressure with ell having another nonzero component fails:
choose the other canonical null column, which leaves the added row unchanged
but changes L theta. Also construct a nonzero row d orthogonal to ell;
it measures independent information but cannot determine ell. These rows are
algebraic design controls, not available calibrated measurements.

For general W=(W_i,W_o,W_b), H=(A,B,h_b),
D=W_o-W_i A^-1 B, and ell=L_o-L_i A^-1 B, while
L theta=L_i A^-1(d-h_b b0)+L_b b0+ell z.
These equalities preserve the measured-bin contribution and the offset value.
They do not require full pressure recovery: only one scalar functional is
missing for this target, though not every single extra scalar row supplies it.

For physical outer-annulus rows, the same pressure basis/support, center,
angular-distance convention, beam convolution, pixel mask/weighting and offset
column must be preserved. Rank tests without those response inputs cannot
claim identification by an actual detector. Noise and uncertainty require
covariance and calibration beyond exact rowspace. Near dependence may amplify
errors even where exact identifiability holds.

No MOND force or mass is inferred here. Any later source bridge must preserve
a0=9.3619e-11 and 1.1279e-10 m/s², distinct constant-vacuum and a0 E(z) histories,
and separate Q/RAR/registered M with total-pressure/density conversion.
