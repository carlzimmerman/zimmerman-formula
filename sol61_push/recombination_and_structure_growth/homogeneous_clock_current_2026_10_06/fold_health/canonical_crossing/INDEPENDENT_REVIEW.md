# Independent canonical-crossing audit

Accepted as a conditional local theorem. I reconstructed the four equations from the full constrained scalar–dust action, rather than treating an infrared kinetic sign as a physical instability theorem. The simple-zero assumptions yield the claimed generic logarithm and gauge-invariant clock-norm pole. No correction is needed in the inspected revision. Nonlinear continuation and crossings with higher-order zeros remain outside the result.

Observed HEAD: `cfa06dbfae97280425bbb61f862eb61468c03dce`. SHA-256 pins:

- Crossing `REPORT.md`: `053286673f0e1ccbcdca960e70ecb7dec40fc161e3a14c57f6fc5e2b1555dc0b`.
- Crossing `checks.py`: `22231eb4c1747783415cc5af9f7ee08bd28438dc9175c2c38bd024b5ff8f4312`.
- Parent complete quadratic-action report: `d99aec2e6f2bc3b9d232c932630e32131cf73fc093170d43e35ce2f705de3d5b`.

The inspected main_c and control_density_c records pin these same revisions. Main_c records nine checks passing; the deletion control records the intended compatibility failure. This audit does not infer the theorem from these counts and does not rerun or edit the author's execution inputs.

## Raw independent reconstruction

Let `R_nu=2S nu+6Theta zetadot+T zeta-pi`, `nu=d zetadot+e v`, `d=M/Theta`, `e=rho/(2Theta)`, `T=2Mp^2+3rho`. The full action gives the per-volume momentum

`P=-6M zetadot+6Theta nu+d R_nu`.

Substitution reduces it to `P=2A zetadot+(rho A/M)v+dT zeta-d pi`, because `A=3M+S d^2`. Its spatial equation is `Pdot+3HP=T nu+2Mp^2 zeta`. The matter pair gives `vdot=nu` and `pidot+3Hpi=e R_nu-rho p^2v`. In the last equation the coefficient multiplying zetadot is exactly `rho A/M`, hence no pole survives in pidot after the momentum relation is solved.

For A nonzero these are four independent first-order equations for two scalar degrees of freedom. Dust's pi equation is its continuity equation and its v equation is the density-momentum equation; neither is a fifth phase-space constraint. For the nonzero Fourier mode, the shift constraint solved the lapse, while the lapse equation determines the scalar shift through its nonzero Theta coefficient. Unitary clock gauge is valid because q is positive; the spatial scalar gauge is already fixed. There is therefore no omitted lapse, shift, matter continuity or gauge redundancy which trivially removes the generic residue before the crossing.

For `A=alpha tau+O(tau^2)`, alpha nonzero, the singular numerator of zetadot is `r y=P-dT zeta+d pi`. The `rho A v/M` contribution is regular. Consequently the four pole coefficients are `(1,d,0,Td)` times that same numerator, giving precisely `N=c r/(2alpha)`. Since `r c=-dT+Td=0`, N is nonzero rank one and N squared vanishes. All quantities in the residue are evaluated at the crossing. The remaining analytic variations of d,T,A/ tau and the background contribute to an analytic regular matrix. Using the per-volume rather than volume-weighted P adds the regular -3HP term and does not change the residue.

## Analytic normal form and codimension

For completeness, the analytic reduction is more than a formal recurrence. Seek `U=I+sum_(n>=1) U_n tau^n` in `U'=(N U-U N)/tau+B U`. Then

`(n I-ad_N)U_n=sum_(j=0)^(n-1) B_j U_(n-1-j)`.

Here `ad_N^3=0` follows from N squared zero. For every positive n, the inverse is the finite sum `n^(-1)[I+ad_N/n+ad_N^2/n^2]`, bounded by a constant divided by n. Analytic coefficient bounds `||B_j||<=b R^(-j)` therefore admit the standard scalar analytic majorant solving `u'=C b u/(1-tau/R)`. This proves convergence on a sufficiently small neighborhood and U(0)=I ensures local invertibility. There is no positive-integer resonance obstruction hidden in the series argument.

The fundamental matrix on either side is consequently `U(tau)(I+N ln|tau|)`. Since c's zeta component is one, generic amplitudes with `r b!=0` have a nonzero zeta logarithm. Amplitudes with `r b=0` have no logarithm and form a three-dimensional, codimension-one linear subspace per mode. Analytic U makes the assertion a condition on the actual solution space, rather than on an arbitrary instantaneous limiting value of a divergent solution. It does not supply dynamical attraction toward that subspace or enforce its selection for an initial perturbation spectrum.

## Observable and scope

The invariant `delta X_clock=delta X-(Xdot/q)delta phi` follows directly from the linear transformation laws for X and phi. In unitary gauge it is `-q^2 nu`. Generic zetadot has coefficient `(r b)/(2alpha tau)`; v is only logarithmic, so it cannot cancel `d zetadot` in nu. Because q and d are finite and nonzero, the invariant has a genuine linear pole. A smooth gauge change does not remove it. The linear approximation will fail before an initially small generic perturbation reaches the pole; the proof describes that failure, not the nonlinear solution beyond it.

At A zero the density-coordinate elimination coefficient is `-3rho^2/(4M)-rho p^2/2<0`. Thus the logarithm is not merely a singular dust elimination at this point. Smooth invertible point changes cannot remove the velocity rank loss, and the full first-order system supplies the stronger generic-invariant divergence. A singular canonical redefinition can change appearances, but cannot erase that invariant within the same finite linear solution.

The accepted claim requires an analytic background, an isolated simple zero, nonzero k, q>0, positive matter density and Theta nonzero. A mode which never crosses, a double/tangent zero, the homogeneous sector, modified operators, a restricted perturbation domain or a nonlinear completion require separate analysis. This is sharper than an instantaneous IR sign diagnosis, while retaining the distinction from UV vacuum decay, a universal modified-gravity no-go or a cold-sector/recombination completion.
