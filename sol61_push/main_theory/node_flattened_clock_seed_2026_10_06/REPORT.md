# Prepared gradient zeros remove the norm-cube regularity obstruction

The full theory and32pi closure remain OPEN. This is a constructive seed and an actual forced **relative scalar block** of the shear-repaired action, not a solved full second-order spacetime. The base is reviewed/pushed42ac8fadd721cdc921aa382431f9c91582b52eaf; the unchanged projected action's all-smooth1D clock obstruction does not transfer to this changed action.

## Actual force and changed preparation

In n=3, use the inherited M(I)=-A+I/2-I^(3/2)/12+... and shared-clock shear term -eta K sum(V sigma²),0<eta<1. The pure-decay seed is relative lapse nu=epsilon B f(x)/a, z=-nu, e=2nu and constrained shift given by inverse Laplacian. Every real smooth zero-mean f is a linear seed of this repaired vacuum branch. The fields vary in one direction on a periodic torus. a=exp(Ht),H,K,a0>0; the amplitude expansion is one-sided epsilon>0 (epsilon|epsilon| is required on changing its sign).

At leading norm-cube order the common projector gives I=|grad_coord nu|²/(a²a0²) and v=a³. Hence S_norm,3=-K/(6a0) integral |grad_coord nu|³, and the relative lapse Euler source is

J=K B|B|/(2a0 a²) d_x[|f'|f'].

This is the actual retained MOND force, not a polynomial cubic substitute. Its leading relative shift/spatial source is zero, since I2 depends only on the relative lapse gradient. Smooth analytic cubic terms with three relative fields vanish by exchange, but the even norm-cube does not. Thus retaining J is necessary. A cosine makes J proportional to |sin x|cos x, with a cusp and j^-2 Fourier coefficients; this cannot be treated as a finite set of second harmonics.

Instead choose f3=cos x-cos(3x)/9. Its derivative is exactly -(4/3)sin³x. The force is

J3=-(16K B|B|/(3a0 a²)) |sin x|^5 cos x.

This function is C4 on the circle, with vanishing derivatives through order4 at nodes, but is not C5 there. Its exact cosine coefficients are zero for even j and

h_j=-480/[pi(j²-4)(j²-16)(j²-36)] for positive odd j,

where h=|sin x|^5 cos x. They decay as j^-6, so its spatial derivatives through order4 converge absolutely. This is an explicit finite-Fourier first-order seed with an infinite-Fourier but classical force.

There is also a smooth-to-all-orders preparation. Define b(s)=exp[-1/(1-s²)] on |s|<1 and zero at and outside the endpoints, G(c)=integral_0^c b(s)ds, f_infty(x)=G(cos x). b is even, G odd, so f(x+pi)=-f(x) and the spatial mean is zero. f'=-sin x b(cos x). Every derivative of b at s=±1 vanishes: interior derivatives are a polynomial in s and inverse powers of (1-s²) times exp[-1/(1-s²)], and the exponential dominates every inverse power. Composition therefore makes f' flat at x=m pi. Away from nodes |f'|f' is smooth; at nodes the same flat factor kills the sign cusp to every derivative. Thus J_infty is C-infinity and has zero mean. This is a deliberately prepared initial profile, not a prediction that dynamics produces it or preserves its preparation at later orders.

## Full constrained relative forcing rather than a bare lapse equation

The parent repaired quadratic action, after its actual shift/shear constraints, is

L/c=-Acal(zdot-Hnu)²+P(nu+z)², c=Ka³,
Acal=-3(1-eta)/eta=-b0<0, P=j²/a².

Add the actual lapse source J_j nu. The lapse solution is

nu=[Acal H zdot+Pz+J_j/(2c)]/(Acal H²-P).

To first order in the source, the reduced action is c Kr(zdot+Hz)²+J_j(alpha zdot+beta z),
Kr=b0 P/(b0 H²+P), alpha=Acal H/(Acal H²-P), beta=P/(Acal H²-P).

With q=az and J_j proportional to a^-2, its sourced Euler equation is

2K d_t[a Kr qdot]=(J_j/a) R(P),
R(P)=(b0 H²-P)(2b0 H²+P)/(b0 H²+P)².

This retains the lapse-source contribution and its time derivative; solving only the gradient equation would miss it. For all P>=0, -1<R<=2. R tends to -1 at high j, so there is no spatial smoothing from the relative dynamics, but no positive high-frequency growth multiplier either. On a compact interior time interval and j>=1, Kr has a uniform strictly positive lower bound. The zero second-order-data solution is the explicit double integral

q_j(t)=integral_t0^t ds/[2K a(s)Kr(P_j(s))] integral_t0^s dr [J_j(r)R(P_j(r))/a(r)].

It preserves a j^-6 force bound for f3. The spatial field and its first four derivatives converge absolutely, while the reconstructed lapse contains an additional P^-1 source term and the shift is reconstructed with P^-1. Time derivatives of the bounded multipliers remain bounded on compact intervals. For the flat smooth preparation, the force coefficients decay faster than every power by repeated periodic integration by parts, and the same estimates give smooth relative corrections. This establishes classical regularity of this forced relative block, not the entire coupled solution. The homogeneous relative j=0 source is exactly zero by divergence, and can be assigned the zero particular correction; homogeneous branch/constraint health is a separate question.

## Exact remaining implication

The sourced common metric/clock, homogeneous anisotropy, tensor and initial constraint equations must also be solved for these changed profiles. The parent's mean scalar constraint is invertible at nonzero modes, but that fact alone is not full admission. Nonlinear regularity beyond this one-sided second-order block, stability of the prepared zeros under general data, ordinary matter coupling, positive cold abundance, recombination/growth transfer and an independent A selector remain unproved. H²=A a0²/6 is still the free coincident-vacuum family; eta and the amplitude/shape are new inputs, not a forced32pi.

The exact checks test the flattened derivative, odd Fourier rational coefficient, constrained lapse/source reduction and uniform multiplier bound. Bounded Fourier/time integrations corroborate the relative-block estimates. They cannot establish missing full metric equations or a global nonlinear solution. Independent review and run provenance are separate artifacts.

Development correction: the first bound-identity check wrote an incorrect polynomial for 2-R(t). The failed output and exact earlier script are preserved. The correct identity is 2-R=t(5+3t)/(1+t)^2, while R+1=(3+t)/(1+t)^2. The bounds and mathematical source equation are unchanged.
