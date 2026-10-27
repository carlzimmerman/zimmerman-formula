# Capture, evaporation, and retention from the existing scalar contact

20 October 2026. Assessment base `b1bb9296dbd20de4d7dc97e4b5f27a7d9b4ad26b`;
actual source bytes are pinned in `source_hashes.json`. This lane writes only
this new `collisions/` directory. No campaign, prior packet, production job,
publication or Git state is changed. All displayed results are analytic.

**Primary verdict: conditional on a specified host and incoming scalar state;
the physical S4 memory join remains incomplete.** The existing scalar contact
does supply a number-changing *orbital occupation* vertex: two continuum
daughters can scatter into a gravitational bound daughter and an escaping
daughter. Its inverse is evaporation from that same bound orbital. Their
matrix elements and rates require no new microscopic coupling. Capture
produces exactly the above-threshold partner that can drive inverse release,
so its escape/return transport is the receiver problem. An isolated final
charge-one bound ground state has infinite retention in the stated static-host
NR Hamiltonian. Neither this observation nor the derived kernels identifies
the bound orbital with the canonical tether label, selects a host/bath, or
predicts a finite astrophysical memory lifetime.

## 1. Exact physical states that the original field does identify

Use the original charge-one NR daughter field `psi`, not a new species.
For a declared heavy, static, attractive gravitational host, define

\[
 h=-{\hbar^2\nabla^2\over2m}+m\Phi_{\rm host}(x),\qquad
 h\phi_b=\epsilon_b\phi_b,
 \quad\epsilon_b=-E_b<0,
 \qquad h\phi_p=\epsilon_p\phi_p,\quad\epsilon_p\ge0.
 \tag{1}
\]

Bound orbitals are square normalized. Continuum orbitals have the chosen
finite-box normalization followed, if justified, by the continuum limit.
Use the same spatial/contact regulator throughout. These are genuine spectral
states of the existing field. The mode expansion and occupation are

\[
 \psi(x)=\sum_b\phi_b(x)a_b+\sum_{p\in C}\phi_p(x)a_p,
 \qquad N_B=\sum_b a_b^\dagger a_b.
 \tag{2}
\]

The quadratic Hamiltonian `sum epsilon_i a_i^dagger a_i` commutes with `N_B`.
A time-independent one-body potential alone cannot capture a continuum
energy eigenstate. A wavepacket's initial bound projection, if present, is
already part of its preparation and is not newly created capture.

Equation (2) is a spatial bound/unbound split, **not** the canonical S4 split.
The canonical released population is explicitly allowed to remain bound by
ordinary gravity; it can therefore have negative energy in (1). Moreover,
the original scalar action does not make its `P` response source depend on
the spectral projector of (1). Giving only `N_B` a tether force would add a
dictionary/interaction not contained in the inspected action. The source
`X` has charge two, so replacing `a_b` by `X` would change the inventory.

## 2. The existing quartic gives the actual capture matrix element

In the dilute, source-eliminated, fully matched low-energy regime, the
source-derived daughter Hamiltonian is

\[
 H_4={g_2\over2}\int\psi^{\dagger2}\psi^2\,d^3x,
 \qquad g_2={\lambda_{\rm rep}\over2m^2}>0.
 \tag{3}
\]

Natural units apply in this coefficient, as in the source. The displayed
`hbar` in time/rate formulas merely records the energy-to-time conversion;
setting it to one gives the source conventions. A finite common regulator
is essential; a bare continuum 3D delta interaction is not being defined by
this formula without matching.

Expand (3) without dropping mode-changing terms:

\[
 H_4={g_2\over2}\sum_{ij;kl} I_{ij;kl}
             a_i^\dagger a_j^\dagger a_k a_l,
 \quad I_{ij;kl}=\int\phi_i^*\phi_j^*\phi_k\phi_l\,d^3x.
 \tag{4}
\]

For distinct continuum modes `p,q,k` and a bound mode `b`, the coefficient of
`a_b^dagger a_k^dagger a_p a_q` is

\[
 \boxed{M_{bk;pq}=2g_2 I_{bk;pq}.}                  \tag{5}
\]

There are two permutations in each incoming/outgoing pair in (4), which
fix the factor two in (5). No adjustable occupation-bath vertex is inserted.
The Fock transition is

\[
 (n_b,N_k,N_p,N_q)\longrightarrow
 (n_b+1,N_k+1,N_p-1,N_q-1),
\]

with matrix element
`M sqrt[(n_b+1)(N_k+1)N_p N_q]`. Its reverse matrix element is its complex
conjugate. The same operator conserves total charge and particle number.
The outgoing continuum daughter is an explicit energy and angular-momentum
receiver. A spherical host imposes total angular-momentum selection through
the overlap; a zero overlap is a forbidden channel, not a small fitted rate.
Translation symmetry is broken in the external-host approximation; recoil
and finite host excitation must be restored if that approximation is not
admitted. No momentum sink is assigned to empty space.

For equal incoming modes, the coefficient is instead
`g_2 I_{bk;pp} a_b^dagger a_k^dagger a_p^2`; its squared Fock factor is
`g_2^2|I|^2(n_b+1)(N_k+1)N_p(N_p-1)`. More generally the normalized two-body
matrix element for unordered pairs is

\[
 \langle ij|H_4|kl\rangle
 ={2g_2 I_{ij;kl}\over\sqrt{(1+\delta_{ij})(1+\delta_{kl})}},
\]

where `|ij>=a_i^dagger a_j^dagger|0>/sqrt(1+delta_ij)`.
These conventions avoid counting both `(p,q)` and `(q,p)` as separate events.
The continuum formulas below use distinct modes and unordered incoming pairs;
the coincident subset has zero measure in the ordinary continuum integral.

This channel was omitted by the *number-isolated fragmented-mode density*
projection in the earlier phonon calculation. It is not a contradiction of
that projection's `[n_i,H]=0`: retaining (5) explicitly leaves that static
approximation. Its physical rate must be checked before assuming isolation.

## 3. From the same matrix to capture and inverse release rates

For a finite regulated system, first-order time-dependent perturbation theory
gives the transition probability

\[
 P_{i\to f}(t)
 ={4|\langle f|H_4|i\rangle|^2\over(\Delta E)^2}
       \sin^2{\Delta E t\over2\hbar}
       +\text{higher orders},
 \quad\Delta E=\epsilon_b+\epsilon_k-\epsilon_p-\epsilon_q.
 \tag{6}
\]

At short time it is quadratic, not an exact exponential. Only a continuum,
weak-coupling, stationary-reservoir/coarse-time regime turns (6) into the
golden-rule kernel

\[
 K_{pqk}^{(b)}={2\pi\over\hbar}|2g_2 I_{bk;pq}|^2
       \delta(\epsilon_p+\epsilon_q-\epsilon_b-\epsilon_k).
 \tag{7}
\]

No such approximation is a theorem of an arbitrary finite Hermitian few-mode
Hamiltonian; coherent exchange and recurrences require its actual evolution.
Assume a specified continuum state with uncorrelated mode occupations `f_p`
for the following closed weak-bath rate formula. Define

\[
 A_b=\sum_{\{p,q\},k} K_{pqk}^{(b)} f_p f_q(1+f_k),
 \qquad
 B_b=\sum_{\{p,q\},k} K_{pqk}^{(b)} f_k(1+f_p)(1+f_q).
 \tag{8}
\]

The same supported continuum states, mode normalization and unordered pair
measure occur in both sums. Reversing a scattering channel does not permit
choosing a different attempt frequency. The resulting bound-mode transitions
are

\[
 \boxed{W_{n\to n+1}=(n+1)A_b,\qquad
        W_{n\to n-1}=n B_b.}                         \tag{9}
\]

For correlated produced pairs replace products by the actual Fock correlation
expectations; the source's one-source production result does not establish
an uncorrelated many-body reservoir. If capture depletes or heats the bath,
its time-dependent collision/transport equation is part of (8), rather than
a new chosen white-noise law.

The original scalar also has the retained cubic source channel. Equation (8)
is its **quartic low-energy contribution**, not an inclusive total width when
real source formation, source decay, host excitation, or other orbital
channels are open. Those must be included without counting source exchange
twice. No absorption or decoherence rate is postulated here.

## 4. Kinematic threshold and the physical receiver

With `epsilon_b=-E_b`, the delta function in (7) requires

\[
 \boxed{\epsilon_k=\epsilon_p+\epsilon_q+E_b\ge E_b.} \tag{10}
\]

Thus continuum-to-bound capture can occur while emitting a continuum
daughter of positive energy at least `E_b`. Conversely an occupied bound
mode can evaporate into two continuum modes through this channel only if
the incoming continuum daughter has `epsilon_k>=E_b`. If the incoming
reservoir has exactly no population at or above that threshold, then
`B_b=0` for this process. Merely knowing its number density or pressure
does not establish that support condition.

Importantly, `B_b=0` at an initial instant does not make capture absorbing:
every successful capture in (10) creates one of the above-threshold `k`
particles. If that daughter stays in or returns to the interaction region,
the inverse channel becomes populated. If it escapes to infinity from an
isolated static host and does not rescatter, it exports the binding energy
through an existing degree of freedom. The asymmetry then comes from an
outgoing, unequilibrated transport state, not unequal forward/reverse
Hamiltonian matrix elements. The escape flux and any returning population
must be calculated from the host and transport, not fitted as a release
constant. No existing finite cold bath may be silently reset after a write.

Energy inequalities alone are not sufficient for a nonzero rate: (5) must
be nonzero on a nonzero-measure energy shell with populated incoming modes.
The displayed theory has no supplied physical host profile or incoming
distribution from which that measure can be evaluated here. It would be
incorrect to replace it by an arbitrarily selected positive prefactor.
`BORN_CAPTURE.md` executes a concrete next check in the existing weak
Coulomb host: the leading plane-wave-continuum matrix has a positive
energy-shell integral with an explicit coefficient. Exact Coulomb distortion
and common-regulator control remain necessary for a full scattering witness.

## 5. The exact thermal ratio and the correct memory observable

If the continuum really is Bose distributed at a specified inverse
temperature `beta` and chemical potential `mu`,

\[
 1+f_i=e^{\beta(\epsilon_i-\mu)}f_i.
\]

On the same energy shell as (7), every integrand pair obeys

\[
 {f_p f_q(1+f_k)\over f_k(1+f_p)(1+f_q)}
 =e^{-\beta(\epsilon_b-\mu)},
 \quad
 \boxed{A_b=e^{-\beta(\epsilon_b-\mu)}B_b.}          \tag{11}
\]

This derives reciprocity and the ratio from the microscopic process. It
does not supply an absolute rate without the overlaps and the state. At
positive finite temperature, finite `mu`, nonzero overlaps and a supported
continuum energy shell, `f_k` is positive above threshold, so capture and
release are both nonzero. Exact permanent one-way capture does not follow.

For constant coefficients, the unrestricted bosonic occupation has

\[
 {d\langle n\rangle\over dt}=A_b+(A_b-B_b)\langle n\rangle.
 \tag{12}
\]

When `B_b>A_b`, the difference of two initial mean occupations decays as
`exp[-(B_b-A_b)t]`. The stationary probabilities are geometric,
`P_n=(1-r)r^n`, `r=A_b/B_b<1`, yielding precisely
`<n>=1/[exp(beta(epsilon_b-mu))-1]`. This normal-reservoir description
requires `mu<epsilon_b`. If instead `A_b>=B_b`, (12) grows and its fixed
reservoir/unchanged-level assumption eventually fails; contact energy shifts
or reservoir depletion must be retained. Such growth is not a derived finite
two-state latch.

A mean-occupation relaxation time is not a first-release lifetime or a
binary memory time. Starting exactly at `n=1`, the probability of no jump at
all is `exp[-(2A_b+B_b)t]` under (9). Capture also changes that occupation.
For a truly derived hard-core `n=0,1` subspace, the different master equation
would instead be `dot p=A_b(1-p)-B_b p`; the difference between an initially
occupied and empty bit decays as `exp[-(A_b+B_b)t]`. The earlier conditional
hard-core hierarchy is not an exact property of every orbital of the original
bosonic field. It cannot be inserted solely to obtain a desired lifetime.

If a justified protocol and state make loading negligible throughout a
retention interval and the occupied level remains fixed, the usual
evaporation survival approximation is

\[
 S(t)=\exp[-\int_0^t B_b(s)ds].                      \tag{13}
\]

Keeping survival at least `p_*` then requires
`integral B_b dt <=-ln p_*`. This is a conditional rate statement, not a
new fitted timescale. In an actual closed evolving bath, the complete
Hamiltonian/kinetic evolution rather than a frozen `B_b` controls survival.

## 6. A genuine long-retention state, and why it does not finish S4

There is an exact limiting retention result in the retained-source NR model.
Consider the total `Q=1` sector: an isolated daughter in a bound ground
orbital of (1), with no other daughters or sources and a static host.
The normal-ordered quartic annihilates the entire one-daughter sector.
Both cubic terms also annihilate it: `b^dagger psi^2` needs two daughters,
while its conjugate needs a source. The exact regulated Hamiltonian therefore
acts there as just `m+h`:

\[
 H|1_b;0_X\rangle=(m+\epsilon_b)|1_b;0_X\rangle,
 \qquad N_B(t)=1.                                    \tag{14}
\]

The retention lifetime is infinite **within that static-host NR model**.
This is not infinite because a fitted barrier was made large. No remaining
partner can carry away energy or activate either interaction. The model has
an allowed quartic two-incoming/one-bound/one-outgoing preparation channel,
but a positive physical capture probability still requires its actual
nonzero on-shell overlap, incoming state and asymptotic escape conditions.
Equation (14) does not by itself prove such a scattering preparation.
In a closed two-incoming-particle preparation, the total charge stays two:
the escaping partner still carries one charge. Applying (14) to the bound
subsystem is an asymptotic separated-channel statement, not a finite-time
conversion of the closed global `Q=2` state into a global `Q=1` state.

It is an ordinary bound orbital, and not a claim of an exact bare eigenstate
of the full unregulated relativistic quantum theory, of a live many-body
host, or of the additional canonical `P` sector. Host evolution, tides,
returning daughters, source formation, collective couplings, or radiation
channels outside this truncation can change retention. Two identical bound
particles also leave the protected one-particle sector. A binary stored
occupation can be read only by a physical protocol that is not supplied here.

## 7. The original production state is not wholly in the contact limit

The constant (3) is the threshold-matched daughter contact. Its controlled
use needs energies, source populations and momenta in the dilute
source-eliminated regime, away from the real source pole. The exact original
source defines

\[
 \Delta_c=4m^2u_*^2,\qquad
 x={s-4m^2\over\Delta_c},\qquad
 \lambda_{\rm eff}(s)=\lambda_{\min}
        \left(r_\lambda-{x\over1-x}\right).
 \tag{15}
\]

For two produced daughters each having `|p|=m u_*` and energy
`m sqrt(1+u_*^2)`, let their relative momentum angle be `alpha`. Direct
four-vector subtraction gives exactly

\[
 s-4m^2=2m^2u_*^2(1-\cos\alpha),
 \boxed{x={1-\cos\alpha\over2}.}                    \tag{16}
\]

For independent isotropic directions this is uniform on `[0,1]`. Their
whole collision integral is not a threshold `x<<1` integral and reaches
the source resonance for antiparallel momenta. Actual production may retain
pair correlations rather than the independent-shell assumption; those must
be preserved. The two daughters of one resting parent are back-to-back and
have `x=1`, not the independent uniform pair distribution. No cosmological
thermalization or cooling state is derived
by quoting the single-source production calculation.

Away from the pole, retaining `X` with its matched analytic contact gives,
at leading two-body order for distinct daughter modes, the energy-dependent
pair matrix

\[
 M_{bk;pq}(E)=4k_R I_{bk;pq}
   +4c_3^2\sum_\nu
    {J_{bk,\nu}^*J_{pq,\nu}\over
       E-\delta-\epsilon_{X,\nu}+i0},
 \quad J_{pq,\nu}=\int\chi_\nu^*\phi_p\phi_q\,d^3x.
 \tag{17}
\]

The pole/source one-body energies and pair orbitals use the same host and
regulator. `E` is pair excess energy relative to `2m`. In the admitted
flat low-energy local limit the resolvent gives
`k_R-c3^2/delta=lambda_rep/(4m^2)=g2/2`, recovering (5).
This is a leading exchange/contact kernel, not a resummation across its pole.
Near resonance one must evolve the real source or compute its self-energy
and width from the same action. Adding an independent source-decay rate
to (17) while retaining its real-source contribution again would double
count that channel. A fitted linewidth is unnecessary but a supplied
consistent spectral calculation is necessary.

Equations (15)-(17) explain why the original numerical `sigma0/m` alone
cannot establish an initial capture or evaporation rate. Even a known
cross section does not replace the orbital overlap, energy/angular-momentum
constraints, density, correlations, and receiver transport in (7)-(8).

## 8. Changed decision, scope, and reproducibility

Nearest local overlap: `occupied_landscape/LANDSCAPE.md` already gives a
conditional equilibrium loading trace and *internal* phonon relaxation
inside an occupied pair, with explicit capture/exchange kinetics missing.
The previous memory/capture packets already establish generic detailed
balance and counted receiver limitations. Neither generic principle is
claimed new here. The distinct present work retains the original contact's
mode-changing operator, derives its energy-resolved capture/evaporation
kernels, locates the write-produced above-threshold receiver, identifies
an exact one-particle retention sector, and tests the inherited production
kinematics against the threshold-contact approximation.

| Obligation | Result |
|---|---|
| Existing field supplies bound/continuum spectral states in a specified host | Yes, conditional on that host; no canonical tether identification |
| Actual occupation-changing contact operator | Derived exactly in the stated mode projection |
| Forward/inverse matrix reciprocity and threshold | Derived from the same operator, with its Bose factors |
| Absolute numeric rate at inherited physical conditions | Not determined: host orbitals, incoming phase-space state and correlations absent |
| Exponential kinetic rates | Conditional on a controlled weak continuum/reservoir reduction; exact finite dynamics begins quadratically |
| Permanent absorbing capture at finite equilibrium temperature | Excluded for an open nonzero matrix channel under the stated thermal contract |
| Long retention in an isolated final charge-one bound sector | Exact in the specified static-host retained-source NR Hamiltonian |
| Positive leading capture kernel in the existing Coulomb host comparison | Calculated explicitly in `BORN_CAPTURE.md`; exact continuum/regulator transfer remains open |
| Dynamical capture followed by irreversible ejecta escape in an actual inherited host | Allowed mechanism, not a completed scattering/transport construction here |
| Matching this orbital occupation to canonical tether/free/S4 | Missing physical dictionary |
| Finite astrophysical lifetime or complete memory pass | Not established |

No scientific simulation, numerical fit, parameter scan or symbolic package
was run in this lane. All combinatorics, Bose ratios, kinematic identities
and conservation statements were rederived directly above. Source hashing
is provenance only. Review status: author analytic self-review, not a fresh
external proof audit. A fresh audit should reconstruct (4)-(11), the `Q=1`
claim (14), and the source-regime check (16)-(17) from the pinned raw action.

Continuation: use an actual inherited host/phase-space initial state to
evaluate the regulated spectral overlaps and on-shell support; evolve the
escape/return flux and real-source channel once. First provide the explicit
field-to-canonical-response occupation map if the target is S4 rather than
ordinary spatial capture. The absence of that map is not repaired by fitting
`A_b`, `B_b`, a bath temperature, or a return fraction.
