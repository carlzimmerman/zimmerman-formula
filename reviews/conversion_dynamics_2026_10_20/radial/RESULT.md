# Conversion dynamics of the supported radial attraction model

20 October 2026. Assessment base observed at this lane's start:
`b1bb9296dbd20de4d7dc97e4b5f27a7d9b4ad26b`.
This new lane writes only `reviews/conversion_dynamics_2026_10_20/radial/`.
Actual source bytes, including filesystem-only proofs, are pinned in
`source_hashes.json`. No source, campaign, prior packet, job or Git state
is changed here. All results are analytic; no scientific program is run.

**Normalized target and primary verdict: incomplete, with a physical
occupation/transition map missing.** The existing radially supported
attraction construction does not itself give a writable memory. In its
specified collisionless spherical dynamics the proposed outer and inner
action families cannot convert: their angular-momentum supports are
disjoint by more than a factor 300 in squared specific angular momentum.
Both internal-label conversion rates are zero, and the supported orbital
states are also dynamically disconnected by their actions. This is an
exact scoped result, not an assertion that all existing interactions in
all geometries forbid capture.

Time-dependent spherical gravity can capture a different, already
crossing same-action orbit into ordinary gravitational binding. The exact
energy-crossing fluxes are derived below. They are functionals of the
actual distribution and host history, not a fitted attempt frequency.
They do not supply S4's tether label, a unique positive rate, or a memory
lifetime. Existing nonspherical density fluctuations can transfer angular
momentum, but their correlation state is not fixed by the retained smooth
radial solution.

## 1. Claim card, definitions, and dependency graph

The actual prior radial family has a central baryonic mass `M0>0`, a
baryonic host shell `M_h=2M0` with radius near `2a`, an inner cold
population supported below `9a/8`, and an outer cold stock near `100a`.
Its inner circular actions are

\[
 j_t(s)^2=GM_0r_0(s),\qquad a/2<r_0(s)<a,
\]

and its outer free action, fixed across the three compared occupations,
is

\[
 j_f^2=100GDa,\quad D=M_0+M_h+m=3M_0+m,
 \qquad 0<m/M_0\le 1/100.                              \tag{1}
\]

The parcel mass `m` is not identified with MASTER's microscopic daughter
mass. The orbital data are constructed initial-state data. The rate
question is whether the original dynamical equations can move parcels
between these particular families while preserving the correct inventory.

The dependency graph is:

1. Single-medium canonical `P` and continuity identity → every parcel in
   that medium contributes to its source, independent of binding sign.
2. Declared two-population reciprocal extension → separate mass stocks
   and spherical Hamiltonian forces, without a reaction operator.
3. Central forces and initial actions (1) → exact action-support
   invariance and zero transition between the stated orbital families.
4. Actual time-dependent potential and a distribution → energy-surface
   capture/release flux, if the occupation is gravitational boundness.
5. An actual nonspherical bath and microscopic host state → a possible
   nonzero transition spectral density, currently unspecified.
6. Physical projectors, a receiver and those rates → retention/write
   calculation. The final physical leaf has not been supplied.

The coefficient domain is real. Distributions are regular or finite
measures for which the characteristic flow and indicated surface fluxes
exist. Potentials are spherical and sufficiently regular on occupied
annuli; a central point mass is harmless there. The angular-momentum and
shell statements do not require an adiabatic approximation.

## 2. The existing field does not split itself by binding sign

Canonical S3 records

\[
 \partial_t\mathbf P=-\mathbf j,
 \qquad \nabla\!\cdot\mathbf P=\rho-\bar\rho.             \tag{2}
\]

Together with continuity and a fixed background, the difference of the
two sides of the second identity is constant in time. A particle moving
from negative to positive binding energy still contributes to `rho,j`;
its displacement therefore still contributes to `P`. An instantaneous
energy projector does not remove that source or change its response
coupling. S4 explicitly postulates permanent release and leaves its
single-field derivation open.

If instead `P` is stipulated to track only `rho_t`, and a conversion
source `S` is allowed,

\[
 \partial_t\rho_t+\nabla\!\cdot\mathbf j_t=S,
 \qquad \nabla\!\cdot\mathbf P=\rho_t-\bar\rho_t,
\]

then consistency requires

\[
 \nabla\!\cdot(\partial_t\mathbf P+\mathbf j_t)=S          \tag{3}
\]

for a fixed background. Keeping the original `partial_t P=-j_t` forces
`S=0`. A nonzero reaction needs the compensating response-charge current
or a different source equation and its dynamical receiver. Integrating
(3) also counts its boundary flux. This is a compatibility obligation,
not a license to introduce a new conversion current by hand.

The scalar fields `Phi,X` have charges one and two and an existing
conversion vertex. MASTER explicitly leaves their bridge to the
polarization sector unspecified. Ordinary Newtonian bound/continuum
states of `Phi` therefore cannot automatically be renamed as the
different-response S4 tethered/free species. S4's released stock may
itself remain ordinarily gravitationally bound.

## 3. Exact angular-action obstruction in the supported family

For a particle under any spherical force, even one depending on time
and the other populations,

\[
 {d\over dt}(\mathbf r\times\mathbf v)
 =\mathbf r\times A(r,t)\hat{\mathbf r}=0.               \tag{4}
\]

The remainder and stiffness forces of a spherical tether profile are
radial too. Conserved host and outer-shell actions are not merely
parameters of a static minimization: they remain invariants of the
retained dynamical system. Equivalently, every angular-momentum
distribution measure
`int F(j_vector) f_s dGamma` is conserved in each collisionless species.

But (1) gives

\[
 {j_f^2\over\sup_s j_t(s)^2}
 \ge100{3M_0+m\over M_0}>300.                          \tag{5}
\]

Thus no characteristic initially in the outer action support can enter
the inner action support. The reverse is also forbidden. The exact
transition probability between those disjoint action sectors is zero
at every time; any rate defined by their probability flux is zero.
Host contraction can change energy but supplies no torque in (4).

There is a corresponding one-body quantum statement when such a
quantization is explicitly adopted: a central `h(t)` commutes with the
angular-momentum spectral projectors, so its propagator preserves their
sectors. This is a statement about the radial mean-field model, not the
full many-body pair-gravity Hamiltonian. Full nonspherical particle
forces conserve total angular momentum but can exchange individual
angular momentum. They are considered separately in Section 6.

### A radius exclusion even if the host changes a particle's energy

For a positive finite spherical Newtonian mass distribution of total
mass `M_tot`, with potential zero at infinity,

\[
 \Phi_N(r)=-G\left[{M(<r)\over r}+
             \int_r^\infty{dM(s)\over s}\right]
 \ge-{GM_{\rm tot}\over r}.
\]

Consequently every ordinary-gravity free particle with instantaneous
binding energy `epsilon<0` obeys

\[
 \epsilon={v_r^2\over2}+{j^2\over2r^2}+\Phi_N(r)
 \ge{j^2\over2r^2}-{GM_{\rm tot}\over r},
 \qquad r>{j^2\over2GM_{\rm tot}}.                     \tag{6}
\]

Here `M_tot=M0+M_h+2m=3M0+2m` is a conservative upper bound on the
mass attracting a free parcel; counting its own mass only weakens the
bound. For the stated range of `m/M0`, (1) and (6) imply

\[
 r>50{3M_0+m\over3M_0+2m}a
 \ge50{301\over302}a>49.83a.                          \tag{7}
\]

The inner supported radius is `9a/8`. Thus not even a negative-energy
eccentric free orbit with the inherited outer action can occupy that
inner region. A sufficiently energized high-action flyby is not the
low-action supported endpoint. Changing the response label at crossing
would require precisely the reaction missing in Section 2.

## 4. The actual host/free radial Hamiltonian is separable at fixed stock

With strictly ordered shells, the potential of the host at every outer
particle is `-GM_h/r`, independent of host radius `q`. The exact retained
potentials in the prior proof are

\[
 E_h(n,q)={M_hj_h^2\over2q^2}-{GM_h(M_0+mn+M_h/2)\over q},
\]
\[
 E_f(n,R)=m(2-n)\left[{j_f^2\over2R^2}-{GC_n\over R}\right],
 \quad C_n=M_0+M_h+m+mn/2.                             \tag{8}
\]

For fixed `n`, adding radial kinetic energies gives a sum of a `q`
Hamiltonian, an `R` Hamiltonian, and the inner shape Hamiltonian. There
is no `q,R` mixed potential. Exciting the host's radial mode therefore
does not transfer energy to the exterior stock while this ordering
holds. In particular an initially circular exterior stock remains on
its same radial equilibrium, although the host might oscillate inside.
The negative energy obtained by comparing minimized values at different
`n` does not create the missing `n` motion.

Both this separability and the action mismatch are absent from a purely
static Schur-complement argument. They are the decisive dynamical tests
of the proposed supported attraction mechanism.

## 5. What ordinary time-dependent capture would actually calculate

A different low-action orbit can cross the host. Its specific potential
is

\[
 \Phi_h(r,t)=-{GM_h\over\max(r,q(t))},
 \qquad \partial_t\Phi_h={GM_h\dot q\over q^2}
                         \mathbf1_{r<q}.              \tag{9}
\]

The potential is continuous at `r=q`, so differentiating creates no
delta contribution there. Along its Hamiltonian trajectory the particle
energy receives this host contribution,

\[
 \Delta\epsilon_h=GM_h\int {\dot q(t)\over q(t)^2}
                              \mathbf1_{r(t)<q(t)}dt.  \tag{10}
\]

Contraction gives a negative shift to particles actually inside the
host; expansion gives the reverse. A particle always outside receives
zero. One always inside during a full returning radius cycle has zero
net shift. Crossing at different phases can give a nonzero transfer.
The live host receives the compensating energy; prescribing `q(t)`
instead requires counting the driving work. This is ordinary orbital
capture/release, not a new internal response label.

More generally let `h(x,v,t)` be the specific one-body Hamiltonian,
`f` solve its collisionless equation, and let ordinary binding be
`e=h-e_escape(t)`. Define `D=partial_t+{.,h}`. At regular crossings,

\[
 D[\Theta(-e)f]=-\delta(e)(De)f,
 \qquad De=\partial_t h-\dot e_{\rm escape}.            \tag{11}
\]

Integration over phase space gives exact directional crossing fluxes

\[
 C(t)=\int\delta(e)[-De]_+f\,d\Gamma,
 \qquad R(t)=\int\delta(e)[De]_+f\,d\Gamma,
 \qquad \dot N_{\rm bound}=C-R.                        \tag{12}
\]

If the relevant population is nonzero, per-particle instantaneous
crossing hazards can be defined as `C/N_unbound` and `R/N_bound`.
These are not necessarily Markov rates; recrossing and the same orbital
phase can retain memory. In a static field with a fixed escape zero,
both crossing fluxes vanish. In a live field their values require the
actual `f`, field history, and the correct self-consistent energy ledger.
No such host history or incoming distribution is fixed by the supported
equilibrium calculation. Equations (9)-(12) give a parameter-free
functional of specified inputs, not a unique predicted coefficient.

## 6. Existing nonspherical gravity: the missing input is its state

An allowed continuation is actual density granularity or nonspherical
host modes. Existing gravity can transfer individual angular momentum
through `-Gm integral rho_b(y)/|x-y| dy`; no new coupling is needed.
However the smooth spherical solution has no such fluctuation spectrum.

For specified orthogonal orbital states `f,t`, a specified quantum host
Hamiltonian and its stationary initial weights `p_i`, define the actual
projected density operator

\[
 B_{tf}=-Gm\int d^3y\,K_{tf}(y)\,\delta\hat\rho_b(y),
 \quad K_{tf}(y)=\int d^3x\,
            {\phi_t(x)^*\phi_f(x)\over|x-y|}.
\]

First-order transition amplitudes contain
`integral_0^t exp[i(E_t+E_j-E_f-E_i)s/hbar] ds`. If a justified
weak-coupling continuum limit turns those amplitudes into rates, their
coefficient is fixed:

\[
 W_{f\to t}={2\pi\over\hbar}\sum_{ij}p_i
  |\langle j|B_{tf}|i\rangle|^2
  \delta(E_t+E_j-E_f-E_i).                            \tag{13}
\]

Its inverse uses the same Hermitian interaction and the actual reverse
host populations. A discrete unbroadened host need not have a constant
irreversible rate at all. A mean density or the static relaxed attraction
does not determine the matrix elements and populations in (13).

For example, independent identical host granules of mass `mu=M_h/N`
with the same normalized orbit distribution have the same mean density
for every `N`, while their connected density covariance is

\[
 \langle\delta\rho_b(y,t)\delta\rho_b(y',0)\rangle_c
 =N\mu^2 C_1(y,y';t)={M_h^2\over N}C_1(y,y';t).         \tag{14}
\]

Here `C1` is the one-granule connected distribution kernel. The equality
is exact at equal time for factorized granule positions, and at unequal
times under the stated independent-orbit comparison. It is not asserted
for a fully interacting correlated host. Independent granules are a
comparison family, not a derived host model.
The same mean spherical mass and attraction thus allow vanishing
fluctuations in the continuum limit or a nonzero torque spectrum for
finite granularity. Different correlations provide further freedom.
This demonstrates why no rate can be reconstructed from the mean
field alone. Supplying the true microscopic host state could resolve
it; fitting a new white-noise amplitude would not be that derivation.

## 7. Retention, writeability and the meaning of a zero rate

For the exact retained radial model, both the separate tether label and
the disjoint action families have zero transition flux. A prepared
label/action sector persists, but cannot be written from the other
sector by that dynamics. Calling this an infinite useful memory lifetime
would confuse an inaccessible conserved sector with a derived memory.
Stability of an occupied endpoint does not change this fact.

If (13) or another original interaction were to justify a two-state
Markov reduction with constant capture `c` and release `r`, with
`c+r>0`, then

\[
 \dot p_t=c(1-p_t)-rp_t,\qquad
 p_t(t)={c\over c+r}+
 \left[p_t(0)-{c\over c+r}\right]e^{-(c+r)t}.           \tag{15}
\]

The first-exit survival of a prepared tethered state would instead be
`exp(-r t)` under that same Poisson assumption. Recapture makes these
different observables. A thermal host with a downward energy gap
`Delta=E_f-E_t>0` gives `r=exp(-Delta/theta)c` for individual
nondegenerate states by pairing the exact reverse terms of (13).
Neither a Gibbs bath, a gap-defined S4 projector nor that Markov limit
is supplied by canonical collisionless transport. No astronomical or
laboratory retention time follows from (15) without the actual kernel.

## 8. Obligation matrix and disposition

| Obligation | Status | Reason |
|---|---|---|
| Inner and outer supported states and exact energy attraction | inherited proved | Pinned prior radial construction; not rerun here |
| Same-field S4 free/tether projectors | incomplete | Single-medium identity sources every parcel; bridge/reaction is absent |
| Conversion between the stated radial action families | refuted in retained dynamics | Exact invariant (4) and support gap (5) |
| Host radial contraction writes the exterior circular stock | refuted in retained dynamics | Shell ordering makes (8) separable |
| A high-action ordinarily bound free orbit enters the supported core | refuted | Lower-radius bound (6)-(7) |
| Ordinary capture/release of other crossing orbits | conditional, explicit functional | (9)-(12) require actual potential history and incoming distribution |
| Nonspherical gravitational transition coefficient | conditional, explicit kernel | Existing coupling gives (13), host state/correlations not specified |
| Actual memory retention time | incomplete | Physical projector, nonzero write channel, receiver and kernel not yet established |

No claim that every gravitationally bound orbit is forever isolated is
made. The exact exclusions apply to the specified spherical collisionless
model and its chosen action supports. Nonspherical gravity, scalar
collisions, and field conversion are distinct authorized continuations;
their microscopic projections and state inputs must be counted rather
than combined by renaming populations.

## 9. Provenance and nearest-prior delta

`CONVERSION_JOIN.md` already proves separate total-stock conservation and
static density-bath number conservation. Those facts are not counted as
new. This lane additionally tests the actual supported family: its
factor-300 action mismatch, bound-orbit radius exclusion, absence of
host-to-outer radial energy transfer, and exact energy-crossing kernels.
It records the fluctuation-state obstruction to turning static
susceptibility into a unique physical rate. These are scoped local
consequences, not a global novelty claim.

Verification is direct analytic differentiation, spherical potential
integration, and phase-space divergence/characteristic identities.
No numerical experiment or external theorem is load bearing. All
assertions have been self-reviewed for signs, units, empty-population
rate normalization, static versus time-dependent limits, and the
ordinary-binding versus S4-label distinction. This is author self-review,
not an independent audit, full kinetic stability theorem, or continuum
quantum-field-theory certificate.
