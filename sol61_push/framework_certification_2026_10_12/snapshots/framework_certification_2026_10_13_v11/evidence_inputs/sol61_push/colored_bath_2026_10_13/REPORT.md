# Colored bath: a quadratic diffusion zero, with unresolved drift and boundary

Checkpoint CB-2026-10-13. Starting shared revision:
`45cd126e7489ec6703c9c6650cbbeda227f28f13`. Publication continues the existing
`codex/cold-energy-equations` branch; its actual parent is recorded on publication.
Write scope is this directory. Earlier source records remain unchanged.

The overall cold-energy mechanism remains OPEN. This calculation tests a
specific way around the previous nonzero-diffusion-floor obstruction. It
constructs a valid stationary noise spectrum whose leading weak-noise diffusion
vanishes quadratically at a selected orbit. That makes the *averaged toy
selector's* added power finite. It does not derive a selector from the carrier
fields, nor establish a reflecting or impenetrable microscopic boundary.

## 1. Conventions and the three executed discriminators

Take one regular action-angle pair (J,theta), E=H0(J), Omega=dE/dJ>0,
T=2*pi/Omega and fixed q=ER-E. The perturbation is sigma*xi(t)*h(J,theta),
where xi is a real stationary external process independent of the particles.
Its covariance is C(t) and two-sided spectrum is

    S(w) = integral_{-infinity}^{infinity} C(t)*exp(-i*w*t) dt.

Write h=sum_n h_n exp(i*n*theta). The second-order, phase-averaged,
long-time diffusion (variance convention 2D) is

    D_E = sigma^2/2 * sum_{n != 0} (n*Omega)^2 |h_n|^2 S(n*Omega)
        = sigma^2 * sum_{n >= 1} (n*Omega)^2 |h_n|^2 S(n*Omega).       (1)

The last equality uses real h and even S. This is a weak-noise secular formula,
not an exact generator for arbitrary colored forcing. The relevant primary
source for orbital spectral sampling is
[Binney, section 1.3.2](https://ned.ipac.caltech.edu/level5/Sept17/Binney/Binney3.html).
The numerical normalization also passes a time-domain covariance check.

Executed alternatives:

1. A single spectral notch at Omega_R: test higher-harmonic leakage.
2. A delayed difference with zeros at every n*Omega_R: test D proportional to
   q^2 and the finite-power stationary toy model.
3. Detuning and finite-time forcing: test whether the averaged zero supplies
   a genuine hard edge or a target-free drift. It does not establish either.

No measured halo spectrum, Lambda-CDM parameter, or MOND interpolation law is
an input. Regular integrability, a fixed mean potential, weak external noise,
a stationary covariance with finite correlation moments, and Markov/angle
averaging are physical assumptions, not certified consequences of the carrier.

## 2. Why a single notch is insufficient

Use H0=p^2/2+x^2/2+x^4/4 and h=x, at ER=1. Its exact unperturbed orbit is

    x(t)=a*cn(w*t,m),
    a^2=4E/(1+sqrt(1+4E)), w=sqrt(1+a^2),
    m=a^2/[2*(1+a^2)], T=4*K(m)/w.

At ER, T=4.548330398082163 and Omega_R=1.3814267560309466.
An integrable, nonnegative single-notch spectrum

    S_one(w)=(w^2-Omega_R^2)^2/(1+w^2)^3

kills the fundamental but leaves higher odd harmonics. Equation (1), divided
by sigma^2, gives D(ER)=8.4045268316e-5; the third harmonic alone contributes
8.4000693609e-5. The orbit was checked independently against DOP853 integration,
energy conservation, and the kinetic Parseval identity. This counterexample
rules out treating a fundamental-only zero as a zero of the full diffusion.

## 3. A realizable spectrum with all harmonic zeros

Let eta be stationary Ornstein-Uhlenbeck noise with covariance exp(-|t|) and
S_eta(w)=2/(1+w^2), in dimensionless units. Construct

    xi(t)=eta(t)-eta(t-tau),
    S_xi(w)=4*sin^2(w*tau/2)*S_eta(w).                              (2)

This is an explicit stationary process, not merely a nonnegative function
asserted to be a spectrum. Its covariance is

    C_xi(t)=2*exp(-|t|)-exp(-|t-tau|)-exp(-|t+tau|).

Choosing tau=T_R makes S_xi(n*Omega_R)=0 for every integer n. This synchronizes
the bath to a chosen orbit; it does NOT explain how the theory chooses T_R.
Unlike white position-only noise, this process uses memory to cancel orbital
harmonics and escapes the prior white-noise nesting argument.

If Omega'_R=dOmega/dE is nonzero, expansion of (1) gives

    D(q)=sigma^2*c*q^2+o(q^2),
    c=sum_{n>=1} (n*Omega_R)^2 |h_n(ER)|^2
                  *(n*Omega'_R*T_R)^2 * S_eta(n*Omega_R).           (3)

Interchanging the expansion with the infinite sum requires suitable uniform
summability of the differentiated terms. Smooth regular Duffing orbits have
rapidly decaying harmonics; the computation checks truncations 64 and 128 and
FFT grids 8192 and 16384, without claiming a machine-certified tail bound.

For the chosen orbit, Omega'_R=0.23532082124 and c=0.44807381982:

| q | D(q)/sigma^2 | D(q)/(sigma^2*q^2) |
|---:|---:|---:|
| 0.01 | 4.4694095394e-5 | 0.446940954 |
| 0.001 | 4.4796192911e-7 | 0.447961929 |
| 0.0001 | 4.4806264463e-9 | 0.448062645 |
| 0.00001 | 4.4807270236e-11 | 0.448072702 |

A harmonic oscillator has the same frequency at every energy. The matching
delay then suppresses leading secular diffusion throughout the well; it cannot
select one energy. Non-isochrony is essential to this construction.

## 4. The colored bath still does not supply the selector drift

Within second-order weak-noise Markov closure, the divergence form can be
checked without imposing thermal detailed balance. With
h_{-u}(J,theta)=h(J,theta-Omega(J)*u), the averaged second-order operator is

    Kf = sigma^2 * integral_0^infinity C(u)
                    <{h,{h_{-u},f}}>_theta du.

For f=f(J), integration by parts in periodic theta gives

    <{h,{h_{-u},f}}> = partial_J[<h_theta*(h_{-u})_theta>*f_J].

The J derivative includes the J dependence of Omega in the delayed phase.
Dropping that derivative would incorrectly decouple drift from diffusion.
Consequently Kf=partial_J(D_J*partial_J f). Transforming to q yields

    A_H=D'+D*partial_q log T, n=T*f, current_H=-D*T*partial_q f.     (4)

Thus zero current on a region with positive diffusion still gives constant f.
For f proportional to q^(-1/2), an additional drift -D/(2q) is required.
The leading D proportional to q^2 now makes that extra drift regular:

    b_extra approximately -sigma^2*c*q/2,
    extra energy gain approximately sigma^2*c*q/2.                 (5)

For the separate exact local toy model D=c_*q^2 with constant T and 0<q<=Q,
choose A=(3/2)*c_*q, c_*>0. With a reflecting upper endpoint Q, the normalized
zero-current density and positive extra bulk power are

    n(q)=1/[2*sqrt(Q*q)],
    mean extra power = c_*Q/6.                                    (6)

Without the extra drift, A=2*c_*q gives a constant n instead. The toy Ito
log-coordinate rule is d(log q)=(alpha-1)c_*dt+sqrt(2*c_*)dW when
A=alpha*c_*q. The q=0 endpoint is not reached in finite time by this ideal
geometric diffusion starting at positive q; the reflecting upper endpoint is
still a physical boundary assumption. Its energy exchange must balance bulk
input in a stationary realization. Equation (6) is not an astrophysical power
prediction and the extra drift has not been obtained from the delayed bath.

## 5. Timing sensitivity and the finite-time boundary problem

Changing tau to (1+delta)*T_R restores diffusion at the *original* ER:

    D(ER)/sigma^2 approximately 15.4413257723*delta^2.

For delta={0.01,0.001,0.0001}, computed values are respectively
{0.001543602330,1.544127274e-5,1.544132524e-7}. If no geometric cutoff fixes ER,
a nearby zero can instead shift to Omega(E_*)*tau=2*pi, with
E_*-ER approximately -(Omega_R/Omega'_R)*delta. Timing error is therefore a
floor at the fixed target, not a universal statement that every zero disappears.
An actual spherical halo also has a family of L-dependent periods; one delay
has not been shown to synchronize all required orbits.

More seriously, S(n*Omega_R)=0 removes secular variance growth, not all
finite-time fluctuations. At first order in sigma, with the unperturbed orbit
and uniform initial phase, the exact energy-increment variance is

    Var[Delta E(t)]/sigma^2 = 2*integral_0^t (t-u)*C_xi(u)*C_p(u) du,
    C_p(u)=2*sum_{n>=1}(n*Omega_R)^2*|h_n|^2*cos(n*Omega_R*u).        (7)

Time-domain quadrature gives:

| elapsed periods | variance / sigma^2 | variance / (2*t*sigma^2) |
|---:|---:|---:|
| 2 | 7.565491025 | 0.415838910 |
| 10 | 7.562968887 | 0.083140056 |
| 50 | 7.562968887 | 0.016628011 |

The apparent diffusion decreases as 1/t while a nonzero fluctuation plateau
remains. These are linear-response covariances, not nonlinear stochastic
trajectory simulations. The RMS energy fluctuation is about 2.7501*sigma in
these units. Near a gap of this size or smaller, fixed-energy orbit averaging
cannot by itself justify a sharp instantaneous-energy boundary. Higher-order
noise effects and boundary crossings need a separate, uniformly valid treatment.
We have NOT proved a nonzero all-orders secular floor, nor an exact impermeable
barrier. Sending q to zero at fixed sigma is not justified by (3) alone.

## 6. Nonlinear trajectories: the averaged zero is not a hard bare-energy wall

We also executed the nonlinear equations, without adding selector drift:

    dx/dt=p,
    dp/dt=-x-x^3+sigma*[eta(t)-eta(t-T_R)].                         (8)

Use stationary OU prehistory, independent uniform orbital phases, and 512
paths at each sigma. Every path starts at bare H0 energy 1-sigma, so q=sigma.
Crossings of bare H0>1 are counted over ten periods and do not remove or
reflect particles. This is a fixed bare-energy diagnostic; it is NOT a proof
about a fluctuating geometric escape boundary or permanent spatial escape.

| sigma and initial q | sampled crossing paths | fraction | coarse-grid fraction |
|---:|---:|---:|---:|
| 0.001 | 461/512 | 0.900390625 | 0.900390625 |
| 0.003 | 460/512 | 0.8984375 | 0.900390625 |
| 0.01 | 460/512 | 0.8984375 | 0.896484375 |

The fine grid uses 1024 steps per period; the coarse grid uses 512. Both share
exactly coupled OU endpoint samples. The unforced fine-grid maximum energy
error is below 1e-5 in these runs; the coarse/fine final-energy RMS discrepancy
is below 0.01*sigma. Each run passes the declared looser tolerances. Wilson 95%
intervals for sampled crossing fractions are approximately [0.87,0.92], but
these sampling intervals do not include discretization bias. The resolutions
separately check numerical sensitivity. The amplitudes share random paths;
they are not three independent statistical replications.

This supplies direct bounded numerical evidence against treating the notch as
an impenetrable instantaneous bare-energy boundary. It is consistent with the
finite first-order fluctuation plateau, not a measurement of a residual
all-orders secular diffusion constant. No astronomical crossing rate is inferred.

## 7. Verification and next implication

`run/results.json`: 41 deterministic checks of the stated finite grids,
frequency/time covariance equivalence, toy current and power, orbital solver,
resolution and harmonic truncation. `lean_run/results.json`: eight exact
algebra/trigonometric theorems, standard axioms only, and three rejected damaged
proofs. Lean certifies filter harmonic zeros and conditional current/log-drift/
power algebra. It does not certify the stochastic closure, asymptotic exchange
of limits, stationary probability-process construction, full infinite series,
or the empirical mechanism. This is self-review, not external review.

`trajectory_run/results.json` records the three stochastic cases and their
resolution/baseline controls, with seed 20261013 and explicit OU prehistory.

The constructed filter shows that the earlier diffusion-floor obstruction does
not cover every colored bath. The target-free selector and physical boundary
remain unresolved. The next discriminating obligation is a same-action carrier
coupling producing both a suitable covariance and reciprocal drift, with finite
reservoir accounting. An externally chosen delay and hand-added drift do not
meet that obligation. The nonlinear crossing test now rejects the naive hard-wall interpretation
in the tested bare-energy cases. A controlled boundary-layer theory or an actual
feedback/confinement mechanism is still needed for a physical edge.
