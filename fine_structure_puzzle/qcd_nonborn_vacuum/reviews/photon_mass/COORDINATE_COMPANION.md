# Posttarget coordinate-moment and kernel-bound companion

This is a separately identified posttarget audit. The root proposed the moment
bridge after this review's PRETARGET.md, exact code and first run were frozen.
Those earlier inputs are preserved. No independence from that candidate is
claimed for this companion; the normalization and hypotheses are checked here.

## Coordinate trace moment

Use H_ab^NB(x)=<p|T j_a(x) j_b(0)|p>_vacsub/(2M), with the same complete
covariant Born subtraction as the mass kernel. Its Fourier tensor from the
polarizability action is

 H_ab(Q)=4*pi*[(a+b)E_ab-b G_ab]+O(Q^4),
 H_trace(Q)=4*pi*[(a-2b)Q^2+2(a+b)Q4^2]+O(Q^4).

There is no extra 2M in this formula: H already divides the relativistic
nucleon matrix element by 2M. The mass response is M_u=(1/2)integral H D.
The Fourier convention exp(iQx) gives

 integral d4x r^2 H_trace(x)=-Delta_Q H_trace(Q)|_0
 =-4*pi*[8(a-2b)+4(a+b)]=-48*pi*(a-b).

Therefore C_NB=3(a-b)/(32*pi*M) is

 C_NB=-integral d4x r^2 H_trace^NB(x)/(512*pi^2*M).

The zero moment is H_trace^NB(Q=0)=0. Using the Bessel kernel,
G3=(1/(2M))integral H_trace*r^2 K2(sqrt(s)r)/(128*pi^2),
and K2(z)=2/z^2-1/2+O(z^2 log z), the constant 1/s piece cancels by the
zero moment. The remaining coefficient is exactly the same -1/(512*pi^2*M)
coordinate moment. This is the full SO(4) trace moment, not one temporal
component or an unconditioned sea/vacuum moment.

## Distributional, UV and IR admission

The Fourier derivative identity is a distributional statement. To identify it
with an ordinary unbounded coordinate moment requires an admissible limit of
test functions/cutoffs: for example an absolutely integrable r^2-weighted
regular part plus explicitly renormalized contact distributions and controlled
long-distance tails. Merely writing a Taylor coefficient does not prove that
a finite-volume numerical coordinate sum already has this meaning.

Vacuum subtraction removes the leading identity OPE singularity. In the usual
connected QCD OPE, nonidentity terms have softer short-distance singularities,
for which the r^2 weight is locally integrable up to their logarithms. This is
a sufficient standard OPE admission condition, not a newly proved full-QCD OPE
bound. Derivatives of delta-function contacts can contribute directly:
<Delta delta,r^2>=8 in four dimensions. They must be kept in the distributional
moment. A computation restricted to separated currents cannot silently claim
the full polarizability moment. Covariant lattice action/current contacts and
short-distance renormalization must be matched to the continuum definition.

At positive pion mass the fully Born-subtracted tensor has a gap to inelastic
states and the requisite low-Q analyticity. A quantitative coordinate method
still needs a uniform long-distance moment bound and stable external-state
limit. Complete Born subtraction removes the elastic channel whose gap tends
to zero with spatial momentum. Constructing the full NB coordinate correlator
may require the elastic form factors over its support or equivalent controlled
elastic-state subtraction, even though the local massive-photon logarithmic
Born correction only needs kappa. These are different data requirements.

An infinite-volume photon kernel applied to a controlled QCD correlator can
avoid simulating a periodic massive photon with lambda*L large. That does not
remove QCD finite-volume corrections, external-state normalization, Born
subtraction, contact matching or moment-tail errors. They then need their own
bounds, usually governed by QCD gaps rather than a photon-image extrapolation.
There is no automatic finite-volume equality.

## Fifth-filter remainder bound from the third-filter bound

For the author's normalized NB fifth estimator F5=-P5 f/(3s^2), and the
positive G3 kernel, their weight ratio is

 (5/3)*(3t-s)*(t-3s)/(t+s)^2=(5/3)*(4y-1)*(4y-3),
 y=t/(t+s) in [0,1].

Since (4y-1)(4y-3)=16(y-1/2)^2-1 is between -1 and 3, the absolute ratio is
at most 5. Thus, under exactly the same |g(t)-2Ct|<=B t^2 soft assumption and
absolute OPE-tail integrability used for G3, the fifth estimator's absolute
soft-shape and hard-tail errors are bounded by five times the corresponding
positive-kernel bounds. Its local cutoff value is its own exact polynomial
16y^5-20y^4+5y^3, not y^3. This establishes a dominated-kernel route to the
limit without assuming that an arbitrary big-O remainder can be differentiated
five times. The bound supplies no physical numerical B or tail value.

The full Born subtraction can analogously be controlled: after its constant,
quadratic and cubic low-z terms are handled, a bounded O(z^4) remainder gives
an O(lambda_gamma) error in the fifth estimator. Further quantitative control
requires the actual local form-factor/remainder constants. Numerical agreement
of quadrature orders or recovery in one HB benchmark does not supply them.
