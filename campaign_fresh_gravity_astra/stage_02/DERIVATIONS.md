# AFG-004–008: geometry, resolution and identifiable gravity scales

These chains continue the parent framework directly. They do not import a
gravity mechanism. All observational examples are synthetic; historical novelty
has not been checked. The latent dynamical assumption remains circular tracers
following the stated Q or RAR relation. No relativistic completion is inferred.

## AFG-004 — remove the common-geometry assumption

Let source element i have luminosity weight I_i >= 0, baryonic acceleration B_i,
radius r_i, and line-of-sight projection p_i. Define q_i=p_i² r_i, so its squared
intrinsic line velocity is u_i²=q_i g_i. Approaching/receding signs do not affect
the even moments. The algebraic Q branch gives, with one a for the system,

    u_i⁴ = q_i²(B_i² + a B_i).                            (S1)

Therefore, for any nonnegative source response alpha_i,

    a = [sum alpha_i I_i u_i⁴ - sum alpha_i I_i q_i² B_i²]
        / [sum alpha_i I_i q_i² B_i].                     (S2)

Require a finite positive denominator. This formula permits different radii
and projections and never divides by p_i. Minor-axis elements with p_i=0
simply supply no gravity signal in the denominator. Maps must be in compatible
physical units. Radius/projection/emissivity errors are still nuisance inputs.

## AFG-005 — carry the actual spatial and line response

Let P_ji be the known fraction of photons from source i registered in pixel j.
Line moments below are unnormalized flux-weighted moments, so spatial mixing
is linear. The finite example has sum_j P_ji=1; known throughput losses could
instead be retained in P. It is a Gaussian spatial mixing model on a finite
grid, not a calibrated telescope PSF.

Assume each source's line broadening has mean zero, vanishing third moment,
known variance s_i² and known fourth moment k_i. Symmetry is sufficient; a
Gaussian shape is not required. For a Gaussian k_i=3s_i⁴. For a uniform
distribution on [-sqrt(3)s_i,sqrt(3)s_i], k_i=9s_i⁴/5. Then

    M2 = P [I (u²+s²)],
    M4 = P [I (u⁴+6s²u²+k)].                             (S3)

Products inside square brackets are componentwise. Subtract the known offsets:
Y2=M2-P[I s²], Y4=M4-P[I k]. For any observation-space weights l4,l2, define
alpha=P^T l4 and beta=P^T l2. The corrected quantity is

    T4 = l4^T Y4 - 6 l2^T Y2
       = sum alpha I u⁴ + 6 sum I(alpha s²-beta)u².       (S4)

**Exact correction condition:**

    P^T l2 = s² (P^T l4).                               (S5)

Under (S5), substitute T4 for the intrinsic fourth moment in (S2).
This handles a known heterogeneous line response after spatial blurring. It
does not require separately reconstructing every source velocity.

The residual delta=alpha s²-P^T l2 has an explicit Q-scale bias,

    bias = 6 sum I delta q g / sum alpha I q² B.          (S6)

For fixed l4, (S5) is solvable exactly iff s² alpha lies in the row space of P.
This is also necessary for an exact correction that is linear in Y2 for every
possible latent u². To prove necessity, if the desired vector is not in that
row space, it has a nonzero component z in ker(P); two sufficiently small
opposite perturbations of a strictly positive source moment vector along z
give the same Y2 but different required corrections. Positivity survives if
the perturbation is small enough.

Concrete one-beam example: I=(1/2,1/2), s²=(.04,.16), and u²=(.2,.8) or (.8,.2).
Both have intrinsic second moment .5, but <s²u²>=.068 or .032. Thus their
broadening cross term cannot be reconstructed from that second moment alone.
This is NOT a no-go for a fit that supplies additional dynamical or spectral
information.

## Noise: an algebraically exact inverse can be unusable

For Poisson arrivals with expected total N and known exposure normalization,
the unnormalized raw moment estimates satisfy

    Cov(M_r,j, M_s,k) = delta_jk M_(r+s),j / N.           (S7)

For (S2)-(S5) with denominator C1=sum alpha I q²B, this implies

    Var(a_hat) = sum_j[l4_j² M8_j +36 l2_j² M4_j
                       -12 l4_j l2_j M6_j]/(N C1²).    (S8)

The covariance term cannot be omitted: the same photons form both moments.
This treats all maps and background corrections as known. Dividing instead
by a noisy observed total flux changes the covariance and requires a different
calculation.

The synthetic 8x8 source disk has inclination 55 degrees, a radial positive
baryonic field B=.1 r/(1+r²)^(3/2), and specified emissivity. It supports
circular tracers in a radial potential. It is not an arbitrary set of clumpy
patches assumed to remain on circular orbits. Coordinates are scaled to a
reference radius, with sky-to-disk deprojection explicit in the code.

For two gravity scales, five spatial widths and two symmetric broadening laws,
the noiseless estimator recovers the scale. A separate 400-realization Poisson
test at a=E(3), 5000 expected photons, predicts sigma_a=.18492 and measures
.18624; the variance ratio is 1.0143. This is a finite code/noise check.

With fixed l4=ones, increasing the spatial width from .4 to 1.0 reference
radii takes the scale-1 standard error at 10000 photons from .0464 to 373.8.
That is a noise amplification failure of that inverse, not an empirical bound.

## AFG-006 — unknown Gaussian width produces an exact ambiguity

Now suppose the broadening variance is common but unknown. Normalize I to
weights w. Define

    U(a) = <q sqrt(B²+aB)>,
    C0=<q²B²>, C1=<q²B>.

The observed moments satisfy m2=U(a)+s² and
m4=C0+aC1+6s²U(a)+3s⁴. Eliminate s²:

    m4-3m2² = H(a) = C0+aC1-3U(a)².                     (S9)

The left side is invariant under common independent Gaussian broadening. It
is the fourth cumulant for a symmetric zero-mean line; it is only an even-moment
combination for an arbitrary unsymmetrized nonzero-mean line.

Write c_i=w_i q_i and g_i=sqrt(B_i²+aB_i). Then

    U'=1/2 sum c_i B_i/g_i,
    U''=-1/4 sum c_i B_i²/g_i³,
    H'=C1-6UU',
    H''=-6[(U')²+UU''] >= 0.                            (S10)

The last inequality follows by applying the elementary squared-sum inequality
to sqrt(c_i g_i) and sqrt(c_i) B_i/g_i^(3/2):
(sum c_i B_i/g_i)² <= (sum c_i g_i)(sum c_i B_i²/g_i³).
The inequality is strict for at least two distinct B_i with c_i>0. Therefore
H can have a single minimum, and a measured fourth combination can admit two
scales. In the single-B case H is affine instead; a zero affine slope is an
exception where it carries no scale information at all.

The endpoint derivatives are

    H'(0)=C1-3<qB><q>,
    H'(infinity)=C1-3<q sqrt(B)>².                        (S11)

If the first is negative and the second positive, a strictly convex H has a
minimum and permits double-valued scale inversion over an interval. Each
candidate must additionally satisfy s²=m2-U(a)>=0. If H'(infinity)<=0,
the map is nonincreasing; if H'(0)>=0 it is nondecreasing. Strictness and the
affine zero-slope exception must be checked before asserting identifiability.

**Constructed ambiguity:** w=(.9,.1), q=(1,1),
B=(.0085716655,.8571665532) in units of today's reference a0. A symmetric
approaching/receding mixture gives:

| Quantity | Vacuum scale a=1 | H scale a=E(3)=4.5656325 |
|---|---:|---:|
| Broadening variance in reference units | .28395628 | .10000000 |
| Observed m2 | .49380816 | .49380816 |
| Observed m4 | .76639678 | .76639678 |
| Observed m6 | 2.01762328 | 1.95151970 |

The same two source populations can be a matched mixture/stack; they are not
asserted to be two azimuthal sectors of one stationary axisymmetric disk.
At reference radius 5 kpc, the required widths are 64.0 versus 38.0 km/s for
the canonical normalization, 70.3 versus 41.7 km/s for the alternative.
These are illustrative nuisance values, not measured dispersions.

The next even combination,

    J6 = m6 -15m4m2 +30m2³,                              (S12)

also cancels common Gaussian broadening, by expanding the sixth power. It is
the sixth cumulant of the symmetrized line. The two examples give -.04677 and
-.11287, so the ambiguity does not extend to the sixth moment or full spectrum.
Direct line integration independently confirms the moments.

Using the covariance of iid photon moments through order 12 and the gradient
(-15m4+90m2², -15m2, 1) gives an idealized asymptotic separation of three standard
errors at about 22950 photons for these two fixed models, taking the larger
variance. This excludes background, nuisance fitting and non-Gaussian
calibration errors; it is not an instrument forecast or a detection claim.

## AFG-007 — estimate the scale without reconstructing every velocity

Subtract the Q baryon-only fourth term as well:

    y2=M2-P[I s²],
    y4=M4-P[I k]-P[I q²B²],
    x=I u², c=P[I q²B], S=diag(s²).

Then the exact latent-variable model is

    y = (y2,y4) = d a + D x,
    d=(0,c), D=(P; 6 P S).                              (S13)

A linear estimator h^T y returns a for EVERY latent x iff

    D^T h=0, d^T h=1.                                  (S14)

For a positive-definite moment covariance C, minimize h^T C h subject to
(S14). If N spans ker(D^T), the solution is

    h = N (N^T C N)^(-1) N^T d
        / [d^T N (N^T C N)^(-1) N^T d].                 (S15)

It exists iff N^T d != 0. This follows by completing the square in h=N z
with the single normalization constraint. The minimum is within this linear,
latent-nuisance-cancelling class, not among all nonlinear model fits. The
numerical design uses C at a=1 and applies the resulting weights unchanged at
a=E(3); unbiasedness does not depend on which design covariance was selected.

In the strongest-blur test, this reduces the scale-1 standard error from
373.83 to .4222 at 10000 photons. However some effective source weights
alpha=P^T h4 become negative; (S2) still holds for Q, but positivity-dependent
inequalities and general-law monotonic inversion cannot be assumed.

After coarsening the 64 source cells into 16 recorded pixels, the tested varying
width map gives ker(D^T)={0} at the stated numerical cutoff. No invariant of
this class remains. With constant broadening, the same coarsened data retain
16 null directions and recover the scale. Numerical rank is explicitly
tolerance-dependent; the general criterion is the exact one in (S14).

There is also an exact calibration limitation. Suppose every s_i²>0 and an
unknown common multiplicative calibration changes S to lambda S. A fixed
linear estimator cancelling arbitrary latent x for all lambda near 1 needs
both P^T h2+6SP^T h4=0 and SP^T h4=0. Thus P^T h4=0 and d^T h=0, contradicting
normalization. Universal width-calibration immunity is impossible in this
estimator class. Restrictions on x, joint nonlinear fitting or additional
spectral information can evade this scoped result.

## AFG-008 — carry the exponential RAR law separately

The cancellation of the broadening cross term did not require Q. For any
static branch it extracts

    T4 = sum alpha I q² F(B;a)².                         (S16)

For RAR, F(B;a)=B/[1-exp(-sqrt(B/a))]. At B>0, increasing a decreases the
positive denominator, so F is strictly increasing. If alpha>=0 and some
alpha I q² B>0, (S16) is a continuous strictly increasing function of a.
As a approaches zero it tends sum alpha I q²B²; as a approaches infinity it
diverges linearly in a. Thus every T4 strictly above that baseline has one
and only one positive RAR scale under the assumed map. No Q formula is used.

To preserve this monotonicity at large blur, add the linear inequalities
P^T h4>=0 to the variance minimization. The problem is convex with linear
constraints. The code whitens its positive quadratic form and solves the
finite constrained problem; finite solver convergence is not an exact
optimization certificate. Primal residuals and comparisons are audited.

The positive-weight estimator recovers a=1 and E(3) using the RAR forward
moment at all five tested spatial widths. At width .4 the local scale-1
standard error is .04575 per 10000 photons; at width 1 it is .6416. Applying
the Q interpretation to the SAME RAR moments would yield about 1.139 instead
of 1 in the well-resolved test. This is kernel mismatch, not cosmic evolution.

## Consequence for the campaign

There is now a forward-modelled scale test for each core branch, with explicit
geometry, spatial mixing, line response, covariance, identifiability failures
and a constructive ambiguity. It is a substantially more precise empirical
target than a change in fitted rotation-curve a0 alone. It still needs real
calibrated spectra and independent baryonic/geometry maps. None of these
results removes the cluster residual or supplies a covariant gravity action.
