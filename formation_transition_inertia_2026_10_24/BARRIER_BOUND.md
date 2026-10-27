# A barrier to formation independent of pump strength

Claim FT-B1 (analytic, conditional on the specified finite-shell energy):
for a uniform continuous phase x starting at zero, constant C, positive
phase/radial kinetic energy, nonnegative heat Q starting at zero, equal
baryon shell masses and conserved individual baryon angular-momentum
magnitudes, the following energy lower bound holds whenever A(x)>0.
It permits arbitrary shell rearrangement and crossing, not just homology.
It is not a theorem about arbitrary two-state theories or realistic galaxies.

Use the inherited smooth shell kernel, supported at physical radii
[a r_i, 1.25 r_i], a=3/4. Units G=Mb=1; total cold mass=5.364.
Let B(r),D(r) be cumulative baryonic and total cold mass, q=sin^2(pi x/2),
s=sin^2(pi x)/pi^2, and define

    A(x) = q^2 [1+2 beta C s] - 1.

For 0<=z<1, w(z)=-log(1-z)-z >=z^2/2 and F(z)=z^2/(1-z)>=z^2.
Consequently the exact gravity-plus-field energy satisfies

    Ug+Ux >= (1/2) integral [A D^2 -2 B D -B^2]/r^2 dr
           >= -(1/2)(1+1/A) integral B^2/r^2 dr
           = (1+1/A) Ub.

The second step completes the square in D. Saturation outside z<1 is
not an escape: it lies outside this model's finite-energy domain.

For ordered baryon shell centroids r_(i), equal masses mu=1/n,

    Ub >= -sum_i mu [(i-1/2) mu]/(a r_(i)).

Reason: the mutual potential of two softened spherical shells is the
mass-weighted average of -1/max(s,t). Since each physical shell radius
is at least a times its centroid, every pair (including self-energy)
is bounded below by the corresponding point-shell pair divided by a.
Summing the ordered pair energies gives the displayed coefficients.

Let ell_(i)^2 be the individually conserved squared angular momenta sorted
in increasing order. For any assignment of shell labels to ordered radii,
the angular kinetic energy is minimized by pairing smaller ell^2 with
smaller radii. This follows by swapping an inverted pair: the difference
is mu(ell_large^2-ell_small^2)(1/r_small^2-1/r_large^2)/2 >=0.
Thus, with d_i=(1+1/A)(i-1/2)mu/a,

    E_total >= sum_i mu [ell_(i)^2/(2 r_(i)^2)-d_i/r_(i)]
            >= -sum_i mu d_i^2/(2 ell_(i)^2) =: L(x).

The last inequality completes a separate square in each inverse radius.
It does not require those unconstrained minimizers to be correctly ordered;
dropping ordering only makes this a more conservative lower bound.
Cold angular/radial energy, phase kinetic energy and heat were dropped
because they are nonnegative. All baryon ell_i must be nonzero; otherwise
this bound can become vacuous. No numerical minimizer proves this result.

If L(x*)>E_initial at any phase x* on the path from F to the desired T
fraction, energy conservation forbids that path, whatever the reciprocal
pump strength or phase inertia. At x*=2/3, q=3/4 and
s=3/(4 pi^2), so A=(9/16)[1+3 beta C/(2 pi^2)]-1.
A path to q>=.95 must cross x=2/3 or -2/3; the same bound applies to both.

Application is numerical, with the actual initial angular momenta and
energy checked at several discretizations. It is not an interval-certified
computer proof of the decimal margins. The algebraic implication above is
exact under its hypotheses. Initial profile/units, beta and C are inputs.

## Self-audit

- Passed: completing-square signs, field normalization, self-pair factor 1/2,
  pairwise rearrangement, shell crossing, arbitrary dark radial distribution.
- Conditional: positive receiver and kinetic terms, uniform phase, fixed C,
  equal baryon shell masses and conserved individual canonical momenta.
- Not covered: angular-momentum transport between shells, spatial nucleation,
  external work, variable C, different interaction energies or relativistic
  dynamics. None is ruled out by FT-B1.
- The rotor Routh reduction preserves the required canonical momenta.
  Its velocity-linear term contributes no reduced energy. It cannot evade
  this bound by transferring energy reversibly.
- No observed catalogue or external theorem is used. Review is self-review.
