# Bound-state response from the full gravitational source

20 October 2026. Route identifier PL-MULTIPOLES-2026-10-20. Assessment
base ff7df583f7d6d3a8a60d0c9cbb8c602302d28653; actual read bytes are
pinned in source_hashes.json. This lane writes only this multipoles
directory. No campaign, prior packet, owner job, publication or Git state
is changed. All derivations are analytic.

**Normalized claim and verdict: incomplete, with the canonical
field-to-response identification missing.** Binding one actual daughter
to a live positive-mass host gives a calculable tidal response, with no
additional coupling. It does not give the required local gravitational
dipole. The complete Newtonian uniform dipole is a center-of-mass
coordinate for both bound and released states. In an exact Coulomb
control, the internal density susceptibility instead begins at k^4,
including the full breathing and quadrupole spectrum:

\[
 \boxed{\chi_{\rm int}(k,0)
       ={83\over24}{\mu^3a^6\over\hbar^2}k^4+O(k^6).}       \tag{1}
\]

Thus an inferred internal longitudinal polarization has a coefficient
proportional to k^2 in response to an acceleration, rather than a
nonzero local coefficient at k=0. Weakening the binding increases this
tidal susceptibility and destroys its finite-gap expansion; it does not
derive an irreversible response-off switch. No memory closure follows.

## 1. Actual existing field and hypotheses

The original scalar has charge-one daughter Phi, charge-two source X,
and the local cubic conversion and positive residual quartic of MASTER.
The retained-source nonrelativistic total-Q=1 sector contains one
daughter and no source. Both normal-ordered interactions annihilate
that sector. In a specified ordinary gravitational host it is therefore
the one-daughter Schrödinger problem already used in the conversion
packet, rather than a new carrier or a fitted binding vertex.

For the explicit control below, use one daughter of inertial/gravitational
mass m>0 and one live point host of inertial/gravitational mass M>0.
The latter M is a host mass, not MASTER's source mass. Their only relative
potential is the existing Newtonian attraction -GmM/r. Natural
nonrelativistic quantum mechanics is used with hbar explicit. Require
the relevant bound velocities and binding energy to be nonrelativistic.
No extra scalar-baryon contact, negative gravitational charge, clamping
force, force-sector portal, site occupancy law or bath is introduced.

This is a conditional two-body host model; an inherited astrophysical
host is not selected by the construction. Point-host finite-size and
relativistic corrections are not silently included. There is no 3D
zero-range contact ambiguity in its Q=1 Coulomb calculation, because
the original scalar quartic and cubic do not act in that sector.

The dependency graph is

actual scalar Q=1 sector and live host -> relative Hamiltonian plus COM
-> full gravitational source -> internal multipoles and resolvent
-> response kernel -> comparison with canonical P.

The final response dictionary, actual medium state and S4 memory are
not supplied by a two-body susceptibility.

## 2. The complete mass source and the uniform-field cancellation

For any translation-invariant Newtonian many-body Hamiltonian with the
same positive inertial and gravitational masses, put

\[
 R={\sum_A m_Ax_A\over M_{\rm tot}},\qquad
 r_A=x_A-R,\qquad \sum_A m_Ar_A=0.
\]

An affine external gravitational potential gives exactly

\[
 \sum_A m_A[\Phi_0+g\cdot x_A]
    =M_{\rm tot}\Phi_0+M_{\rm tot}g\cdot R.             \tag{2}
\]

The internal mass-dipole operator vanishes identically. This statement
does not depend on the binding strength, the occupied internal level,
or the existence of a bound state. Uniform acceleration translates the
whole live system; removing a binding interaction does not switch that
translation on or off.

For two bodies let r=x_d-x_h and

\[
 \alpha={M\over M+m},\quad \beta={m\over M+m},\quad
 \mu={mM\over m+M},\quad
 x_d=R+\alpha r,\quad x_h=R-\beta r .
\]

Then m alpha=M beta=mu. The physical Fourier mass source is

\[
 \rho_k=e^{-ik\cdot R}
   \left[m e^{-i\alpha k\cdot r}
          +M e^{+i\beta k\cdot r}\right].              \tag{3}
\]

After separating the overall COM coordinate, its internal operator is

\[
 \rho_k^{\rm int}=m+M-{\mu\over2}(k\cdot r)^2+O(k^3).
                                                               \tag{4}
\]

Retaining only the daughter's m r term would omit the recoil source
M(-beta r), which remains of order m even as M/m grows. A heavy host
does not become an anchor by neglecting its small displacement while
retaining its large mass.

For a finite-gap bound object, the internal ground-state susceptibility
defined by

\[
 \delta\langle\rho_k\rangle=-\chi_{\rm int}(k,0)\Phi_k,\qquad
 \chi_{\rm int}(k,0)
 =2\sum_{n\ne0}{|\langle n|\rho_k^{\rm int}|0\rangle|^2
                    \over E_n-E_0}                  \tag{5}
\]

therefore begins at k^4, provided the required multipole/resolvent
moments are finite. The sum includes the internal continuum. The
constant total mass has no off-diagonal internal matrix elements.
In an inversion-symmetric real ground state, parity removes the k^5
cross term, giving the remainder O(k^6). This statement removes the
translating COM pole from the response, rather than deleting its mass.

## 3. Interaction energy and the relativistic source check

The rest-mass proxy m N_d+M_X N_X is not conserved by source/daughter
conversion when M_X differs from 2m. It must not replace the full
gravitational energy source to manufacture an internal dipole. In the
existing flat isolated scalar action, the symmetric stress tensor is
conserved. Its energy density contains the cubic interaction, gradients,
time derivatives and the whole positive-square potential, not only
particle rest masses.

In c=1 units define \(H=\int T^{00}\), \(P^i=\int T^{0i}\) and
\(D^i=\int x^iT^{00}\), with vanishing boundary flux. Conservation and stress
symmetry give directly

\[
 {dD^i\over dt}
   =-\int x^i\partial_jT^{j0}
   =\int T^{i0}=P^i,\qquad
 [H,D^i]=-i\hbar P^i.                                \tag{6}
\]

For distinct internal-energy eigenstates with the same total momentum,

\[
 (E_n-E_0)D^i_{n0}=-i\hbar P^i_{n0}=0.              \tag{7}
\]

Thus a uniform first-order lapse gradient, which couples to g_i D^i
in these units, has no finite-gap internal transition matrix element.
The cubic conversion energy does not evade that source constraint.
Equation (7) is a finite-gap spectral statement; it is not an
all-states classification of degenerate zero-frequency responses.

This conservation check is exact for the isolated flat scalar action
under its usual translation-invariant stress assumptions. Extending
it to a live relativistic self-gravitating baryonic host requires that
host's complete stress and field-energy ledger, not a fixed external
potential. The explicit live-host calculation in Sections 2 and 4 is
instead exact within the stated Newtonian two-body control. No
unprovided baryon action, post-Newtonian stress completion or full
Einstein solution is certified here.

## 4. Exact Coulomb susceptibility including all internal channels

The relative Hamiltonian and its normalized ground state are

\[
 h=-{\hbar^2\nabla^2\over2\mu}-{GmM\over r},\qquad
 a={\hbar^2\over\mu GmM},\qquad
 E_0=-{\hbar^2\over2\mu a^2},\qquad
 \psi_0={e^{-r/a}\over\sqrt{\pi a^3}}.                \tag{8}
\]

Set x=r/a and use energy unit E_H=hbar^2/(mu a^2).
On a product F psi_0 the reduced dimensionless resolvent equation is

\[
 {h-E_0\over E_H}(F\psi_0)
   =\psi_0\left[-{1\over2}\nabla_x^2F+\partial_xF\right].
                                                               \tag{9}
\]

It permits an exact sum over all excited discrete and continuum states
without truncating to a two-level dipole. The radial probability
moments are

\[
 \langle x^n\rangle={(n+2)!\over2^{n+1}},\qquad
 \langle x^2\rangle=3 .
\]

For the connected scalar operator A0=r^2-3a^2, the square-integrable
orthogonal solution of (9) uses

\[
 F_0={x^3\over3}+x^2-{11\over2},\qquad
 \left[-{1\over2}\nabla_x^2+\partial_x\right]F_0=x^2-3,
 \qquad \langle F_0\rangle=0 .
\]

Consequently the complete scalar resolvent moment is

\[
 S_0=\langle A_0(h-E_0)_{\perp}^{-1}A_0\rangle
    ={129\over4}{\mu a^6\over\hbar^2}.               \tag{10}
\]

Indeed its dimensionless value is
<x^5>/3+<x^4>-(11/2)<x^2>=129/4.
The inverse is on the subspace orthogonal to the ground state.

For A2=r^2 P2(cos theta), put

\[
 F_2=\left({x^3\over3}+{x^2\over2}\right)P_2,\qquad
 \left[-{1\over2}\nabla_x^2+\partial_x\right]F_2=x^2P_2 .
\]

The angular identity <P2^2>=1/5 then gives

\[
 S_2=\langle A_2(h-E_0)_{\perp}^{-1}A_2\rangle
    ={15\over2}{\mu a^6\over\hbar^2}.                \tag{11}
\]

These are direct inhomogeneous-equation identities. Each constructed
solution is orthogonal to psi_0 and normalizable, so its inner product
is the full resolvent moment, including the continuum, under this
specified Coulomb Hamiltonian. No separately cited atomic-polarizability
table or numerical sampling carries the result.

Take k along z. Since z^2=(r^2/3)(1+2P2), the transition part of (4) is

\[
 \delta\rho_k=-{\mu k^2\over6}A_0
              -{\mu k^2\over3}A_2+O(k^3).
\]

The two angular sectors are orthogonal in the central resolvent.
Substitution into (5) gives

\[
 \chi_{\rm int}(k,0)
 =2\mu^2k^4\left({S_0\over36}+{S_2\over9}\right)
 =\boxed{{83\over24}{\mu^3a^6\over\hbar^2}k^4}
       +O(k^6),                                     \tag{12}
\]

as asserted. Keeping only an odd two-well mode would omit this leading
even-parity response, rather than restore a uniform dipole.

## 5. The response which binding really does supply

In local freely falling COM coordinates, a weak smooth external
potential begins internally at its Hessian E_ij=partial_i partial_j Phi.
Its tracefree tidal part couples to

\[
 V_{\rm tide}={1\over2}E_{ij}Q_{ij},\qquad
 Q_{ij}=\mu(r_ir_j-\delta_{ij}r^2/3).
\]

For E=diag(-e/2,-e/2,e), V_tide=(mu e/2)A2.
Using (11), the second-order ground energy and tensor response are

\[
 \Delta E_{\rm tide}
  =-{15\over8}{\mu^3a^6\over\hbar^2}e^2
  =-{5\over4}{\mu^3a^6\over\hbar^2}E_{ij}E_{ij},
\]
\[
 \boxed{\langle Q_{ij}\rangle
       =-5{\mu^3a^6\over\hbar^2}E_{ij}.}             \tag{13}
\]

The derivative convention is fixed by V_tide=(1/2)E:Q, so the induced
quadrupole is twice the energy derivative. This is an actual
parameter-free tidal polarizability once m,M and the host model are
given. It is not an acceleration-conjugate local mass dipole.

The ordinary COM still responds to gravity. A released daughter also
retains its gravitational monopole and translation/scattering response.
Only an internal structure channel has been isolated in (12)-(13).

## 6. Weak binding is a singular limit, not a derived off switch

For the above ground state |E0|=hbar^2/(2mu a^2). The expansion requires
ka<<1, internal probe frequencies below its excitation gap, and tidal
perturbation small compared with the gap. In particular a sufficient
parametric amplitude condition is

\[
 \mu |E_{ij}|a^2\ll |E_0|,
 \qquad |E_{ij}|\ll{\hbar^2\over2\mu^2a^4}.
\]

At fixed reduced mass, weakening GmM sends a to infinity. The formal
tidal coefficient grows as a^6 while all these domains shrink. At the
unbinding endpoint there is no normalizable internal ground object
with this finite-gap static polarizability. Extrapolating (13) past
that endpoint and setting it to zero is not a derivation.

The two orders of limits, k->0 at fixed a and binding->0 at fixed k,
are not interchangeable. Released continuum matter must be described
by its actual gapless distribution and transport, not a bound-level
formula with an appended response flag. Neither that change of
description nor the loss of a bound state establishes permanent
history-dependent suppression or prevents recapture.

This weak-binding comparison is not a refit of G. Release in one fixed
host may instead excite the daughter from a bound level into its
continuum. The ground-state coefficients (12)-(13) are not formulas for
that outgoing state or for a general highly excited level; the relevant
continuum probe and preparation must then replace them.

## 7. A held host probes a different relative force

Let an additional actual support force F_s act on the host, with
relative potential V(r). Under a common uniform acceleration g,

\[
 m\ddot x_d=mg-\nabla V,\qquad
 M\ddot x_h=Mg+\nabla V+F_s,
\]
\[
 \mu\ddot r=-\nabla V-{\mu\over M}F_s.               \tag{14}
\]

The common g cancels. A nonzero relative uniform drive requires the
support/reaction, or different non-gravitational forces. Clamping the
host can produce ordinary gravitational sag of the daughter relative
to that support, but the support force and energy are part of the
source ledger. It is not an isolated internal mass dipole created
solely by minimal gravity. A heavy live baryonic host is not a clamp.

Existing orbital or pressure support can be examined in a specified
material state; then the conjugate drive is the actual differential
force or tidal/rotating-frame field. No extra fitted support spring is
introduced here, and no general theorem excludes every supported
finite-wavelength material response.

## 8. Comparison with the canonical polarization and memory target

If one merely defines a longitudinal density bookkeeping field by
delta rho=div P_L, then (12) implies
P_L/g is proportional to k^2 at small k, where g=-grad Phi.
A local dipole medium with nonzero k-independent susceptibility would
instead give chi_rhorho proportional to k^2. The canonical critical
quadratic material term K|P|^2/2, K=4pi G, requires that latter local
channel before its cancellation with gravity and its full remainder
R(u)=u^2/(a0-u) can be discussed.

The finite-gap bound object calculated here supplies neither that
local channel nor its normalization or rational nonlinear remainder.
Binding can change finite-wavelength and tidal response; that is not
the specified response-on state. Releasing it does not remove its
ordinary gravitational source; that is not the specified response-off
state. An occupied medium of interacting objects, gapless order, or a
different supported host can have other collective responses and needs
its own actual mode/source calculation.

The new conclusion is therefore stronger than just noting an absent
portal: the most elementary existing bound daughter has an explicitly
calculable response, and its derivative order and unbinding limit do
not realize the requested switch. The full S4 memory gap remains open.

## 9. Obligation matrix, overlap, and provenance

| Obligation | Status |
|---|---|
| Q=1 daughter state from the original retained-source fields | Exact NR sector reduction |
| Complete live-host source and zero uniform internal dipole | Proved by the COM identity |
| Interaction-energy source cannot be replaced by nonconserved rest-mass proxy | Proved for the isolated flat scalar stress identity; full host stress not supplied |
| All-channel Coulomb finite-k internal response | Proved analytically by (9)-(12), in the stated two-body control |
| Existing bound state has a nonzero tidal polarizability | Proved by (13) |
| Weak binding yields a controlled response-off limit | Not established; the finite-gap expansion becomes singular |
| Holding the host supplies a free isolated polarization source | Refuted; reaction force appears in (14) |
| Local canonical P susceptibility, its full R(u), and on/off dynamics | Not obtained |
| Actual astrophysical state, nonlinear collective phase, or lasting S4 memory | Not addressed by this two-body proof |

Nearest prior overlap is explicit. The occupied-landscape note already
derived cancellation of its full uniform dipole and an odd-mode density
response starting at k^6. The live relative-mode review already established
common-affine-force cancellation and form-factor-difference response.
Those mechanisms are not claimed new. Here the extra result is an exact
all-internal-channel Coulomb calculation, including even breathing and
tidal modes, its coefficient 83/24, the induced tidal tensor (13), and
the domain/order-of-limits test of the proposed release switch.
The full-energy stress identity separately closes the tempting
source-mass-detuning proxy loophole under its stated closed-action
hypotheses. No global priority claim follows.

Verification consists of direct COM substitution, integration by parts
of stress conservation, elementary radial differential equations, and
hydrogenic integrals stated explicitly above. There was no numerical
simulation, symbolic package, fit, parameter scan or scientific run.
Review provenance: author analytic self-review, not a fresh independent
audit or an astrophysical certificate. The next decisive input is an
actual collective mode/source identification beyond these finite-gap
positive-mass internal objects, or an existing supported material state
whose counted differential-force response has the required locality.
