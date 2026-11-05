# What a genuine singularity would have to do

These are deductions from the full reduced equations, not extrapolations from
the failed integrator endpoints. Set M=1 as in the numerical experiment.
Write sigma^2=(kx-ky)^2/3, Theta=kx+2ky and

 Bcal=-Theta^2/3+sigma^2-lambda Theta_star-U-R3/2
       +pi_phi^2/(2v^2)+exp(-2A)phi_x^2/2+V.

The full Hamiltonian constraint is

 Bcal+W+gamma Dp^2/2+Dp=0.

Complete the square, with F=1+gamma Dp:

 **W+F^2/(2gamma)=1/(2gamma)-Bcal =: R.**                 (1)

W>=0, so every real constrained state requires R>=0 and F^2<=2gamma R.
This is an additional regularity condition, independent of the expansion cap.
F=0 is not excluded by the cap. It is the merger of the two local quadratic
branches for Dp; initial data have F=1. At such a point the polarization equation
requires the extra compatibility condition exp(A) W_P=gamma(Dp)_x. Failure of
that condition makes the lapse gradient singular; its satisfaction alone does
not prove smooth continuation or well-posedness.

## Polarization cannot hit its wall with all other fields uniformly regular

Let z=K|P|/a, f(z)=-z-log(1-z), W=a^2 f(z)/K. From (1),

 f(z)<=K R/a^2,
 1-z >= exp[-1-K R/a^2] >0.                              (2)

The second inequality follows from -log(1-z)=f(z)+z<=f(z)+1.
Thus, on a compact interval where a is bounded below by a positive constant
and R is bounded above, exact z=1 is impossible. A true wall limit requires
R/a^2 to become unbounded. That means divergence in the gravitational/scalar/
cap quantities entering Bcal, or collapse of a itself. Merely observing
z=.999... in floating-point arithmetic does not demonstrate that limit.
For the small a of this fixture, bound (2) can be exponentially weak.

The potential derivative is much more restrictive numerically:

 W_P=K P/(1-z).

It becomes steep long before W is large. This explains why the lapse/polarization
profiles can lose spectral resolution although the energy constraint residual
is tiny. A small discrete residual is not a small continuum residual.

## Exact lapse positivity and its limits

For F!=0, polarization stationarity gives

 (log N)_x = G(x) = [exp(A)W_P-gamma(Dp)_x]/F.

For smooth periodic data with integral G dx=0,

 N(x)=C exp(integral_0^x G(s)ds), C>0 fixed by mean N=1.   (3)

In the reflection-symmetric sector G is odd, so its period integral vanishes.
If |G|<=Gmax over the circle of length L, then oscillation(log N)<=L Gmax,
which gives exp(-L Gmax)<=N<=exp(L Gmax). Hence N and Q=1/N are finite and
positive under these bounds. A negative Fourier approximation is NOT proof
that this exact positive solution has crossed zero. It can be ringing near
a narrow trough. Conversely, bounded Theta alone supplies no bound on G:
W_P, derivatives of Dp, or1/F can grow.

N->0 is Q->infinity, not Q->0. Clock time freezing relative to local proper
time and loss of a timelike clock gradient are different diagnostics. The
experiment tracks both min N and min Q=1/max N. Neither a coordinate endpoint
nor a vanishing coordinate lapse is by itself a curvature singularity.

## What the expansion cap does and does not prove

Let Z=Theta-Theta_star. The auxiliary equation gives

 Z=T lambda/sqrt(lambda^2+b^2 T^2),
 lambda=b Z/sqrt(1-Z^2/T^2).

For any smooth solution with |Theta_star|<=S, the volume element along a
normal integral curve obeys dv/ds=Theta v and

 v(s)>=v(0) exp[-(T+S)s]>0 at finite proper time s.         (4)

For this particular positive-phi branch, Theta_star>0. There is a stronger
bound requiring no upper bound on the target: Theta>-T and therefore

 **v(s)>=v(0) exp(-T s).**                                (5)

This excludes finite-proper-time volume focusing while the regular clock
foliation exists. Divergent positive Theta_star can still permit expansion
blowup; it does not invalidate the compression bound. Neither bound proves that
the regime persists: lambda can diverge as |Z|->T, shear can grow without
bounded trace controlling it, scalar/curvature derivatives can diverge, and
the auxiliary sector can lose regularity through (1)-(3).

For a hypersurface-orthogonal congruence, Raychaudhuri is

 n(Theta)=-Theta^2/3-2sigma^2-R_munu n^mu n^nu
          +D_i acceleration^i+acceleration_i acceleration^i.

Bounding Theta does not bound any of the individual terms on the right. This
is the mathematical reason a trace cap alone is not a curvature-regularity
proof. R3 and sigma^2 reported by the runs are diagnostics, not a computed
four-dimensional Kretschmann scalar.

## Consequence for the action search

The cap must pass THREE independent continuation requirements:
(1) controlled expansion/target and cap auxiliary stress;
(2) a uniformly regular polarization constraint branch, including F and a;
(3) control of shear, spatial derivatives, scalar energy and lapse gradients.
Changing only Fcap cannot by itself supply (2) or(3). The present runs identify
polarization/lapse steepening as the first resolved difficulty; they do not
prove a no-go theorem for the candidate or a universal cure by another term.
