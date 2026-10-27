# Conversion dynamics: real channels, but no physical S4 memory closure

20 October 2026. [Target contract](TARGET.md). Starting checkpoint:
`reviews/attraction_from_existing_2026_10_20/CHECKPOINT.json`.

**The existing fields supply calculable capture and release channels, but
they do not yet identify the canonical free/tether states or establish
their storage lifetime.** The previously supported attraction example
also fails a new dynamical accessibility test: its outer and inner action
families cannot interconvert under the retained spherical collisionless
equations. No fitted transition rate, bath, portal or noise was added.

## 1. Which physical states can actually be identified?

The original daughter field has ordinary gravitational bound modes
`epsilon_b<0` and scattering modes `epsilon_p>=0` in a specified static
host. The source field `X` has charge two; it is a different state from a
charge-one daughter. These definitions follow from the actual scalar
Hamiltonian. They cannot yet be equated to S4's labels: the postulated
released population may itself remain bound by ordinary gravity.

The canonical displacement instead obeys `div P=rho-rho_bar` and
`partial_t P=-j`. Changing a particle's binding sign does not remove its
mass/current from this identity. If only the tethered density is assigned
to `P`, a reaction source `S` requires

\[
 \nabla\cdot(\partial_t P+j_t)=S.
\]

The existing single-medium equation forces `S=0`. A nonzero conversion
must therefore come with an actual derived response current and receiver,
or a different field identification. Relabeling the scalar modes does not
supply that equation. [Field identity and dynamical proof](radial/RESULT.md).

## 2. The attractive radial example cannot write its proposed states

The previously constructed outer stock has more than 300 times the
squared specific angular momentum of the supported inner action family.
Every spherical collisionless trajectory conserves its individual angular
momentum, even in a contracting time-dependent host. Moreover an ordinarily
bound orbit with that outer action stays beyond `49.83a`; the supported
inner cloud ends at `1.125a`.

While shell ordering holds, the potential of the host at the outer stock
is independent of its radius. Host radial oscillation therefore cannot
even transfer energy to that stock. Both directions of the proposed
transition have exactly zero flux in this model. The attractive energy
and radial stability proved earlier remain true; the new result removes
their interpretation as a writable memory. It does not exclude scalar
collisions or nonspherical gravitational torques in a specified state.
[Exact invariant, radius bound and crossing-flux kernels](radial/RESULT.md).

## 3. The existing scalar contact supplies orbital capture and release

In the admitted low-energy matched regime, `g2=lambda_rep/(2m^2)`.
For distinct daughter modes the original quartic gives

\[
 \boxed{M_{bk;pq}=2g_2\int\phi_b^*\phi_k^*\phi_p\phi_q\,d^3x.}
\]

The same Hermitian matrix element gives both

\[
 p+q\longleftrightarrow b+k,\qquad
 \epsilon_k=\epsilon_p+\epsilon_q+E_b\ge E_b,
 \quad \epsilon_b=-E_b.
\]

The outgoing daughter carries binding energy and angular momentum. The
derived weak-continuum kernels have the common factor
`(2pi/hbar)|M|^2 delta(epsilon_p+epsilon_q-epsilon_b-epsilon_k)`.
Capture weights it by `f_p f_q(1+f_k)`; evaporation weights it by
`f_k(1+f_p)(1+f_q)`, with the same unordered pair measure. A bound mode
with occupation `n` has rates `(n+1)A_b` and `nB_b`, where `A_b,B_b`
are those actual integrals, not fitted attempt frequencies.

Capture itself creates an above-threshold particle that can drive the
reverse reaction. Its escape/return transport is essential. In the
static-host retained-source NR Hamiltonian an isolated total-charge-one
bound state is exactly stationary: cubic and normal-ordered quartic
terms annihilate that sector. This is a real conditional retention
result. Applying it after a two-particle capture requires an asymptotically
escaped partner; global charge is still two. It is not an S4 lifetime.

[Full operator, Bose factors, threshold and retention derivation](collisions/RESULT.md).
[Explicit positive leading Born capture kernel](collisions/BORN_CAPTURE.md)
is a comparison calculation; exact distorted-continuum/regulator control
and an actual inherited scattering state remain open. A nonzero leading
kernel is not a deterministic writer or an exact capture probability.

The original production state also cannot simply use constant `g2` in
every collision. For equal produced momentum magnitudes `m u_*`, the
original resonance coordinate is exactly `x=(1-cos alpha)/2`. Independent
isotropic directions span the full `[0,1]`; same-parent daughters are
correlated back to back. The real source and its width must be retained
consistently near the pole, rather than counted twice.

## 4. An open bare source is too short-lived to store this memory

The original cubic vertex gives normalized pair/source amplitudes
`g_Aij=2c3 I_Aij/sqrt(1+delta_ij)`, with the required bosonic factorials.
In the weak-coupling fixed factorized continuum bath, the difference
between two initial source populations decays at a rate

\[
 \Lambda=\int d\gamma_{ij}(1+f_i+f_j)
          \ge\gamma_{\rm vac}.
\]

At the inherited open-source benchmark this gives
`tau_contrast <= tau_vac approximately 3.52e-13 s`. Inverse association
can raise the source population; it does not protect its preparation
contrast in that kinetic model.

A host can close two-free decay while leaving bound-plus-free decay
open. A dressed level below *all* continua has zero two-body vacuum
width, but direct isolated-pair loading into it is then energy forbidden
too. Existing spectator collisions or host excitations can receive the
energy; their kernels require the actual states. Finite discrete mixing
instead gives coherent oscillations, not a constant capture clock.
[Cubic states, mixed thresholds, rates and writing/retention tests](cubic/RESULT.md).

## 5. What can be concluded about lasting memory?

For an actually justified two-state fixed-bath reduction, preparation
contrast decays as `exp[-(capture+release)t]`. A small release rate alone
does not preserve empty-versus-full information if capture remains on.
The cubic note derives the exact fast-write/long-storage inequality for
that control, and distinguishes it from a driven protocol or cooperative
memory. An unrestricted bosonic orbital has different birth/death kinetics;
its mean occupation is not a binary bit.

For a justified loss-only interval the survival requirement is

\[
 P_{\rm surv}(T)=e^{-\int_0^T\Gamma_{\rm rel}(t)dt},
 \qquad \int_0^T\Gamma_{\rm rel}(t)dt\le-\ln r
\]

for target retention `r`. The [same-moments counterexample](RATE_STATE_DEPENDENCE.md)
shows why density and mean incoming energy do not determine that integral:
one incoming state lies below the release threshold, while another with
the same two moments has a positive above-threshold tail.

The already existing radial host also supplies a calculable receiver
overlap in a controlled harmonic projection:
`S=|U_host|/(2 hbar Omega)` and ground-to-excitation weights
`exp(-S)S^l/l!`. The attraction and receiver factor are tied to the same
parameters. A discrete oscillator does not supply a Markov bath or create
an absent transition. [Receiver derivation and limits](HOST_RECEIVER.md).

**Result:** physical transition operators and state-dependent kernels are
derived, one proposed write mechanism is ruled out, and a genuine isolated
orbital-retention limit is identified. A canonical free/tether projector,
actual host and incoming state, receiver transport, and the resulting
finite lifetime are still missing. Assigning numerical `A_b,B_b`, a
temperature, a return fraction or a noise spectrum would insert those
inputs rather than derive them. S4 and the full theory remain open.

All new mathematics is analytic. Separate reconstruction and exact reviewed
hashes are in [the audit](audit/RESULT.md) and `audit/provenance.json`.
`VERIFICATION.json` records source freshness and preservation of the three
earlier packets. No simulation, fit or global novelty claim is made.
