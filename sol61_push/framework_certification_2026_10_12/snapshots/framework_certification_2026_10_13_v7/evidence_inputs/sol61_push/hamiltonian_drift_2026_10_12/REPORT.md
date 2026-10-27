# Deriving the drift: what an external Hamiltonian bath can and cannot select

Status: a conditional obstruction and a quantitative regularization requirement.
The cold-energy mechanism remains OPEN. This is new analysis of the selector,
not an empirical detection, a complete theory of gravity, or a global no-go.

## 1. Question and conventions

The preceding edge construction chose A=d/2 and D=d(q+q0). Does a specified
physical fluctuation process generate that choice? We now derive both
coefficients from the same external stochastic Hamiltonian.

Use unit particle mass, one regular canonical action-angle pair (J,theta),
H0=E(J), Omega=dE/dJ>0, and period T=2*pi/Omega. At fixed angular momentum L,
this can describe radial motion in a fixed spherical effective potential.
Let q=ER-E>0 with fixed ER. Ito convention is variance 2D per unit time:

    partial_t n = -partial_q current
    current = A*n - partial_q(D*n).

The density with respect to dq is n proportional to T*f, where f is the
phase-space distribution. Factors constant at fixed L cancel below. A regular
orbit, finite nonzero T, an externally prescribed bath, weak forcing, and angle
averaging are hypotheses. The treatment excludes separatrices, changing ER,
self-consistent bath friction, non-Markov memory, and L diffusion.

## 2. Derivation from a stochastic Hamiltonian

Take the Stratonovich Hamiltonian increment

    H0 dt + sqrt(2*k)*h(J,theta) circ dW,    k>0.

For a phase-mixed f(J), the noise part of the density generator is
k*{h,{h,f}}. With {h,f}=h_theta*f_J, angle averaging gives

    <{h,{h,f}}> = <h_theta^2>*f_JJ
                   + <h_theta*h_thetaJ-h_J*h_thetatheta>*f_J
                = partial_J[<h_theta^2>*partial_J f].

The last equality uses integration by parts in periodic theta. Therefore,
within the weak-noise angle-averaged closure,

    D_J = k*<h_theta^2>,
    A_J = partial_J D_J,
    current_J = -D_J*partial_J f.

This is derived for this noise class; it is not inferred by assuming a thermal
bath. Independent white Hamiltonian noises add such terms. Colored noise and
collective feedback require their own derivation.

Transform q(J) with Ito's rule, writing primes on Omega,D_J for J derivatives:

    D_q = Omega^2*D_J,
    A_q = -Omega*D_J' - Omega'*D_J,
    partial_q D_q = -2*Omega'*D_J - Omega*D_J',
    partial_q log T = Omega'/Omega^2.

Consequently the linked drift is

    A_H = partial_q D_q + D_q*partial_q log T.                 (1)

For n=T*f, its current is -D_q*T*partial_q f. A connected region with
D_q>0 and zero current therefore selects constant f, not f proportional to
q^(-1/2). Variable orbital period does not fix this discrepancy: it is already
included in (1). For the earlier illustrative D=d*q and constant T, (1) gives
A=d, whereas the chosen inverse-square-root construction used A=d/2.

This does not exclude transient nonuniform distributions, nonzero-current
solutions, sources/sinks, or disconnected regions with vanishing diffusion.

## 3. A concrete momentum-kick model and an independent check

Let H0=p^2/2+V(x) and h=-x. Then exactly before orbit averaging,

    dx = p dt,
    dp = -V'(x) dt + sqrt(2*k) dW,
    dE = k dt + sqrt(2*k)*p dW.

The orbit-averaged coefficients are

    A_E=k,   D_E=k*<p^2>,   A_q=-k.

Let I(E)=oint p dx and T(E)=oint dx/p on a regular periodic orbit.
Then <p^2>=I/T and dI/dE=T. Hence

    d_E(D_E*T)=k*T,
    partial_q D_q + D_q*partial_q log T = -k,

which independently reproduces (1). For a harmonic oscillator,
T=2*pi/omega, <p^2>=E, and D_q=k*(ER-q). At a positive-energy cutoff,
D_q(0)=k*ER>0: moving the cutoff to q=0 does not make the noise vanish.

`check.py` evaluates I and T by turning-point-regularized quadrature for
V=x^2/2+lambda*x^4/4 at lambda={0,0.1,1,10} and E={0.01,0.1,1,10}.
Central finite differences independently check dI/dE=T and (1); the harmonic
case is checked against its closed form. These are dimensionless mathematical
benchmarks, not astronomical measurements. The weak-noise assumption requires
k sufficiently small on an orbital timescale; k=1 in the tables divides out
the common coefficient and does not assert that the weak-noise approximation
holds at unit physical forcing.

## 4. What the proposed sharp edge actually requires

Allow an extra drift b so A=A_H+b. Then

    current = T*(b*f-D*partial_q f).

For zero current and the previously proposed target f=C*q^(-1/2),

    b_required = -D/(2*q),
    extra mean energy gain per particle = D/(2*q).            (2)

For the additive momentum kicks, an engineered force +gamma(E)*p would
supply that energy drift if

    gamma(E) = k/[2*(ER-E)].                                  (3)

The sign is anti-damping: it pumps energy toward the chosen cutoff. Equation
(3) is a necessary engineered implementation within this model, not a derived
new force. Substituting it by hand would encode the desired profile. Its
reservoir, reciprocal energy loss, stability, and cutoff dependence remain
unexplained. Ordinary damping -gamma*p with gamma>0 has the opposite sign.

If D and T approach finite positive limits at q=0, (2) requires infinite
positive bulk energy input for a nonzero exact target amplitude:

    integral_0^Q n(q)*D(q)/(2*q) dq
        proportional to integral_0^Q D(q)*T(q)*q^(-3/2) dq = infinity.

The conclusion follows by a positive lower bound on D*T near zero. It is
conditional on the exact stationary, zero-current singular target and the
nonzero diffusion floor. If D vanishes sufficiently rapidly, the conclusion
changes. Absorption, boundary work, sources, or nonzero currents also change
the balance and must be accounted for explicitly; probability conservation
alone is not energy conservation. This is not a no-go for all cold matter or
all gravitational theories.

More generally, if D behaves as q^beta and T has a finite positive limit,
the local input for f proportional to q^(-p), p>0, is integrable only when
beta>p (logarithmically divergent at beta=p). For the sharp-edge p=1/2,
vanishing diffusion faster than sqrt(q) can evade this particular power
obstruction, but still must generate the linked extra drift.

There is also a restriction on engineering such a zero with smooth,
position-only white noise in a one-dimensional single well. For a general
h(x), D_E=k*<(h'(x)*p)^2>. If D_E(ER)=0 on a regular orbit, positivity and
continuity force h'=0 throughout the interior of that orbit's accessible
interval. Every lower-energy nested orbit then also has D_E=0. Thus this
particular bath cannot create an isolated diffusion zero at ER while stirring
the nested interior. This argument assumes a connected single well, regular
finite-period cutoff orbit, smooth spatial coupling, and white external noise;
it does not exclude frequency-selective colored noise, momentum-dependent
couplings, collective effects, or a separatrix.

## 5. A calculable finite-width alternative

Regularize the target to f proportional to (q+epsilon)^(-1/2), epsilon>0.
The required added drift becomes -D/[2*(q+epsilon)]. In the illustrative
finite reflecting interval 0<=q<=Q with constant T and constant D>0,

    n(q) = (q+epsilon)^(-1/2)/Z,
    Z = 2*(sqrt(Q+epsilon)-sqrt(epsilon)),
    mean extra energy input P = D/[2*sqrt(epsilon*(Q+epsilon))]. (4)

This is positive bulk input; the reflecting boundary must handle the balancing
energy transfer in any stationary physical implementation. For a finite bulk
power budget Pmax>0, the toy model implies

    epsilon >= [sqrt(Q^2+D^2/Pmax^2)-Q]/2.                     (5)

At small epsilon/Q, P approximately D/(2*sqrt(Q*epsilon)). Thus the edge
cannot be made arbitrarily sharp at fixed D and finite input power in this
construction. Combining a nondegenerate spatial gap q approximately
abs(Veff'(R))*(R-r) gives a local width scale epsilon/abs(Veff'(R)); neither
that slope nor an astrophysical Pmax is inferred here.

For D=Q=1, direct transformed-variable quadrature gives:

| epsilon | mean extra power |
|---:|---:|
| 1 | 0.35355339 |
| 0.1 | 1.50755672 |
| 0.01 | 4.97518595 |
| 0.0001 | 49.99750019 |
| 0.000001 | 499.99975000 |

These numbers test (4); they are not empirical evidence for cold energy.

## 6. Verification, source, and research consequence

The numerical contract and manifest record 46 checks across the specified
orbit grid, harmonic benchmarks, regularized power integrals, and a deliberately
missing-drift residual. Exact Lean algebra separately checks the action-to-gap
identity, density-of-states current, required selector drift, normalization
of (4), and anti-damping relation. Lean does not formalize stochastic calculus,
angle averaging, the divergent integral, or the physical noise hypothesis.
The verification driver inspects every theorem's axioms and requires three
damaged certificates to fail. This is self-review, not an external review.

For context, Binney's primary lecture, section 1.3.2, develops the
[action-space Fokker-Planck framework](https://ned.ipac.caltech.edu/level5/Sept17/Binney/Binney3.html).
Its thermal detailed-balance relation has an additional physical hypothesis;
we do not use it as a universal identity for an arbitrary external bath.
The white-Hamiltonian-noise derivation above is supplied explicitly.

The new missing requirement is more precise than 'choose a drift': identify
an actual coupling that produces the additional energy drift in (2), with a
finite reservoir and an admissible boundary, or abandon the exact sharp-edge
stationary target. The finite-width alternative supplies a measurable relation
between fluctuation diffusion, edge width, and input power, conditional on its
stated model. No such microscopic coupling or measured power budget has yet
been derived from the repository's cold-carrier Lagrangian.
