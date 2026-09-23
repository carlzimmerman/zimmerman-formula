# Opacity-cap lower bound for Thomson escape-delay variance

**Verdict: proved as written within the stochastic model below, by Codex
self-review.** The proof is independent of Qwen's attempted programs. It is
not independent peer review, an assertion of literature novelty, or a test
of an observed JWST system. The constant is not claimed to be optimal.

## 1. Precise statement

Let a photon start at the center of the unit ball in three dimensions, with
isotropic initial direction, and move at speed one. At position x it scatters
at rate kappa(|x|). Assume kappa is continuous on [0,1] and

    0 <= kappa(r) <= M < infinity, M>0.

At each scattering, the cosine mu between incoming and outgoing directions
has density p(mu)=3(1+mu^2)/8 on [-1,1], and the azimuth is independent and
uniform. This specifies the scalar, conservative, unpolarized Thomson model;
there is no absorption, delay at collisions, or selection of photons.

Let T be first exit, u_T the outgoing direction, Z=x_T dot u_T, and D=T-Z.
All photons, including the unscattered atom D=0, are included. Write

    d = E[D] = integral_0^1 r*kappa(r) dr.

If d>0, then 0<d<=M/2 and

    Var(D) >= 2*(2*d)^(3/2)/(9*sqrt(M)),                    (1)
    Var(D)/d^2 >= 4*sqrt(2)/(9*sqrt(M*d)) >= 8/(9*M).      (2)

For d=0, continuity and nonnegativity imply kappa=0, D=0 almost surely,
and (1) remains valid with both sides zero. Relative variance is then undefined.
M is any specified upper bound on the actual profile, not a fitted variance.

## 2. Construction, exit, and integrability

The process can be constructed by proposing scattering times from a rate-M
Poisson process and accepting with probability kappa(|x|)/M. Therefore it has
finitely many collisions on each finite interval. Flights are straight and
positions are continuous across collisions. The direction alone jumps.

From every interior state the straight-line distance to the boundary is at
most two. Conditional on the current state, the probability of no accepted
collision along this path is at least exp(-2M). The Markov property gives

    P(T>2n) <= (1-exp(-2M))^n, n=0,1,2,... .              (3)

Thus T is almost surely finite and has finite moments of every fixed order,
in particular E[T^2]<infinity. At first exit, 0<=Z<=1. A collision exactly
at exit has probability zero; equivalently use the last flight direction.
Since the path starts at the center and has speed one, T>=1 and D>=0.

This tail estimate is loose but sufficient. It is applied at each fixed finite
M; no large-M limit or diffusion approximation is used.

## 3. Angular moments and the mean-delay martingale

Set s=|x|^2 and z=x dot u, so z^2<=s<=1 and z may have either sign. During
a flight, ds/dt=2z and dz/dt=1. Let K average over a scattering direction.
Direct integration of the specified density gives

    E[mu]=0, E[mu^2]=2/5.

Resolving x into components parallel and perpendicular to the incoming u,

    z_new = z*mu + sqrt(s-z^2)*sqrt(1-mu^2)*cos(phi).

Using E[cos(phi)]=0 and E[cos(phi)^2]=1/2 yields

    Kz=0, Kz^2=(3/10)*s+(1/10)*z^2.                    (4)

The spatial generator is

    Lh = 2z*h_s + h_z + kappa(sqrt(s))*(Kh-h).

Define

    F(s) = (1/2)*integral_s^1 kappa(sqrt(v)) dv,
    m(s,z)=F(s)-z, Y_t=t+m(s_t,z_t), before stopping.

Continuity of kappa makes F continuously differentiable, with
F'(s)=-kappa(sqrt(s))/2. Thus Lm=-1: the flight contribution is
-kappa*z-1 and the jump contribution is +kappa*z.
The stopped process Y_(t wedge T) is consequently a martingale on every
bounded time interval, with Y_0=F(0)=integral_0^1 r*kappa(r)dr.

For completeness, the finite-horizon generator identity used here follows by
integrating the deterministic derivative along flights and compensating each
jump by its conditional rate times its mean increment. Bounded rate and
bounded increments on each such interval give integrable jump sums and zero
expected compensated sum. This also applies to the square of Y and to z^2
below. The unbounded stopping step is justified separately, not assumed.

Since |m|<=M/2+1, Y_(t wedge T) is dominated in absolute value by T+M/2+1.
It converges almost surely and in L2 to T+F(1)-Z=D. Hence E[D]=Y_0=d.

## 4. Exact variance identity, including the stopping step

At a scattering, Delta Y=-(z_new-z); time and position do not jump. Its
conditional squared jump, from (4), is

    K[(z_new-z)^2] = Kz^2 - 2z*Kz + z^2
                  = (3/10)*s+(11/10)*z^2.              (5)

The plus z^2 in this equation is essential. Kz^2-z^2 is the generator's jump
term for z^2, not the squared jump of z. Confusing them produces a negative
quantity and the false refutations in the earlier Qwen attempts.

The space-time generator of Y is zero. Expanding the generator of Y^2
therefore leaves only the jump-square term (5). The finite-horizon identity is

    E[Y_(t wedge T)^2]-d^2
      = E integral_0^(t wedge T) kappa(r_v)
                       *((3/10)*s_v+(11/10)*z_v^2) dv.

The left side converges by the L2 domination above; the nonnegative right
side converges monotonically (and is bounded by (7M/5)*E[T]). Put

    Qs=E integral_0^T kappa(r_t)*s_t dt,
    Qz=E integral_0^T kappa(r_t)*z_t^2 dt.

Both are finite. Consequently

    Var(D)=(3/10)*Qs+(11/10)*Qz.                        (6)

Independently, (4) gives

    L(z^2)=2z+kappa(r)*((3/10)*s-(9/10)*z^2).

Apply the same finite-horizon generator identity to z^2, then pass to T.
The terminal quantity is bounded; the integral is dominated by a constant
times T. Since s is continuous through jumps,

    integral_0^T 2z_t dt=s_T-s_0=1

on every escaping path. Hence, writing e=E[Z^2],

    e=1+(3/10)*Qs-(9/10)*Qz.

Solve this equation for Qz and substitute into (6):

    Var(D)=(2/3)*Qs+(11/9)*(1-e).                       (7)

Because 0<=Z<=1, the second term is nonnegative. Thus

    Var(D)>=(2/3)*Qs.                                  (8)

No statistical independence or closure assumption has been used.

## 5. A pathwise radial bound

Let f(r)=kappa(r)*r^2>=0 and H(r)=integral_0^r f(a)da. The trajectory radius
r_t is Lipschitz, with |r'_t|<=1 almost everywhere, including across the finite
number of collisions before exit. The ordinary chain rule for absolutely
continuous paths gives

    integral_0^1 kappa(r)*r^2 dr
      = H(r_T)-H(r_0)
      = integral_0^T f(r_t)*r'_t dt
      <= integral_0^T f(r_t)dt.

This holds for paths with radial backtracking as well as outward paths.
Taking expectations and using (8),

    Var(D) >= (2/3)*integral_0^1 kappa(r)*r^2 dr.         (9)

This is an inequality, not an equality identifying occupation time with
straight radial travel.

## 6. Enforce the opacity cap at the fixed mean

Set a=sqrt(2d/M), so 0<a<=1, and use the comparison function
kappa_*(r)=M*1_{[0,a]}(r). Its weighted first moment is M*a^2/2=d.
This is only a comparison function; it need not belong to the continuous
admissible class. For almost every r,

    r*(r-a)*(kappa(r)-kappa_*(r)) >= 0.                  (10)

Indeed, for r<a both (r-a) and (kappa-M) are nonpositive; for r>a both
(r-a) and kappa are nonnegative. Integrating (10) and using equality of the
weighted first moments cancels the term multiplied by a. Therefore

    integral_0^1 r^2*kappa(r)dr
      >= integral_0^a M*r^2 dr
       = M*a^3/3 = (2d)^(3/2)/(3*sqrt(M)).              (11)

Combining (9) and (11) proves (1). Dividing by d^2 and using d<=M/2 proves (2).
The proof neither assumes a continuous minimizer is a step nor claims the
final stochastic inequality is sharp. For a=1, the comparison is simply the
admissible constant profile M, so this endpoint also causes no difficulty.

## 7. Physical units and limits of the claim

For radius R, photon speed c, and a physical scattering coefficient bounded
by kappa_max (inverse length), use M=R*kappa_max and d=c*E[D_phys]/R. Then

    Var(D_phys) >= 4*sqrt(2)/(9*sqrt(c*kappa_max))
                         * E[D_phys]^(3/2),
    Var(D_phys)/E[D_phys]^2 >=
             4*sqrt(2)/(9*sqrt(c*kappa_max*E[D_phys]))
             >= 8/(9*R*kappa_max).

Here D_phys=T_phys-x_exit dot u_exit/c. The cap must be constrained independently
to make an observational falsification possible. The theorem does not supply
such a measurement, deconvolve an observed light curve, treat absorption,
track polarization memory, or prove the scalar model describes JWST objects.

The earlier no-floor family has M_n=(2/log(2))*(2^n-1) growing without bound.
Accordingly, the present lower bound tends to zero and does not contradict
that result. No limit is taken inside a stopped expectation in either proof.

## 8. Evidence and provenance

The proof above establishes the universal statement. verify.py independently
checks the angular integrals (including changed-variable positive and actual
isotropic negative controls), polynomial generator and jump-square identities,
elimination, constrained radial moment constants, endpoints and unit conversion.
Its algebra checks complement, and do not replace, the stopping and pathwise
arguments. AUDIT.md records the dependency review; SOURCES.md records the
limited primary-source overlap search. All are Codex self-review. No independent
mathematical peer review or priority determination is claimed.
