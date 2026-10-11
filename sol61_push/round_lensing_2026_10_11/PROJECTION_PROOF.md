# What the radial relaxation actually proves

This is a direct derivation, self-reviewed; no novelty claim.

## Arbitrary positive circular projected density

At a fixed centre, write the physical deflection in angular coordinates as
`a_hat(x) = mu(<R) (x-c)/R^2`, where
`mu = 4 G M / (c_light^2 D_l) * (radians_to_arcseconds)^2`.
Sort the distinct sampled radii. Nonnegative projected density implies
nondecreasing enclosed masses. Conversely, any such finite mass sequence can
be realized by putting each nonnegative increment into a smooth annulus
strictly between the preceding and current sampled radius. Circular symmetry
makes the exterior deflection depend only on enclosed mass. Thus the finite
increment cone represents exactly the sampled deflections of arbitrary
nonnegative circular projected profiles at the declared centres. Equal radii
must share a variable; mass outside the outermost sample has no effect there.
This does not establish positive spherical three-dimensional deprojection.

## A necessary positive spherical projection inequality

A spherical shell at radius r puts fraction
`p(R,r)=1` for r<=R, and `1-sqrt(1-(R/r)^2)` otherwise, inside a projected
aperture R. For 0<Ri<Rj, every nonnegative spherical density therefore obeys

`M2D(Ri) >= [1-sqrt(1-(Ri/Rj)^2)] M2D(Rj)`.

Proof: minimize the ratio of the two shell fractions. For r<=Ri it is one.
For Ri<r<=Rj it decreases to the displayed coefficient. For r>=Rj, set
q=Ri/Rj, t=(Rj/r)^2 and f(t)=1-sqrt(1-t). The ratio is f(q^2 t)/f(t).
Its logarithmic derivative in t is E(q^2 t)-E(t)<=0, because
`E(t)=t f'(t)/f(t)=(1+sqrt(1-t))/(2 sqrt(1-t))` is increasing.
The minimum over this interval is consequently at t=1, or r=Rj.
Integrate the pointwise bound against nonnegative shell mass to obtain the
claim. A shell at Rj attains equality; smooth thin shells approach it.

All pair inequalities plus monotonicity remain NECESSARY only. This note
does not prove their sufficiency for a positive three-dimensional density.
Failure of this relaxed cone would rule out the selected spherical-centre
model at exact point positions, subject to numerical verification; feasibility
does not establish the repaired kernel, a cold-mass budget, or observational fit.

## Constraint-generation certificate

An LP using a subset of inequalities has an objective no larger than the
full minimization problem. If its optimizer satisfies every omitted inequality,
it is feasible for the full problem and has the same optimum. Its dual extends
to the full problem by zero multipliers on omitted rows. Floating-point
residuals and dual gaps must be checked separately; they are not exact proofs.
