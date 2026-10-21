# A real finite-overlap optical spring, with its actual source

20 October 2026. Assessment base supplied by the parent target:
`cc07e00a3ba0f2917f16d834b6ca54bcd93a4dcf`. Actual working source bytes,
not an assumed clean checkout, are pinned in `source_hashes.json`.

**Verdict: incomplete, with a positive finite-state result.** The original
repulsive daughter scalar admits the explicit conditional finite
Thomas–Fermi state below. Overlap with a finite baryonic host supplies a
positive relative-displacement curvature, despite the wrong homogeneous
polarization kernel. This is a genuine collective optical mode. It does
not have the full canonical material action or its gravity-conjugate
operator: when the host is live, uniform gravity drives the center of mass,
and this co-centered optical mode's one-mode mass-density oscillator
weight begins at order `k^6`. Generic internal tidal channels can begin
at `k^4`. Neither result is the `k^2` oscillator weight of a local massive
longitudinal density-displacement mode. Removing overlap removes this
particular spring; loss of condensation at fixed density does not.
No permanent release label, preparation protocol or retention time follows.

This is a new finite-state continuation, not a reuse of the earlier radial
breathing Hessian as a Cartesian support. The entire system has a freely
translating center of mass. No absolute support is introduced.

## 1. Raw model, physical hypotheses and scope

The original complex daughter `Phi` and charge-two source `X` have the
positive-square potential in the consolidated equations, lines 65–141.
The retained-source NR Hamiltonian, at its own stated regulator, is

\[
 H=mQ+\int\left[{\hbar^2|\nabla\psi|^2\over2m}
 +{\hbar^2|\nabla b|^2\over2M_s}+\delta|b|^2
 +c_3(b^*\psi^2+b\psi^{*2})+k_c|\psi|^4\right],
 \quad Q=\int(|\psi|^2+2|b|^2),\quad\delta=M_s-2m>0.
                                                        \tag{1}
\]

Here `M_s` is the original source mass; `M_b` below is a baryonic host
mass. They are different objects. The fully threshold-matched dilute
limit, including the analytic negative-frequency correction documented
in `micro_response/DERIVATION.md`, lines 11–103, has

\[
 g_2={\lambda_{\rm rep}\over2m^2}>0,\qquad
 \kappa_c={g_2\over m^2},\qquad \rho_c=m|\psi|^2.
                                                        \tag{2}
\]

The coefficients in (1) and (2) are not silently interchanged: (2) is the
matched daughter-only low-energy reduction, not a claim that its bound is
the uncorrected regulated positive-square operator bound. Its conditions
include negligible real `X` stock, virtual source fraction
`c3^2 n/delta^2 << 1`, chemical/excitation energies well below detuning,
lengths longer than the eliminated source range, dilute Hartree validity,
and weak, cold Newtonian gravity. The carrier production calculation does
not establish that an actual halo reaches this coherent state.

With `K=4 pi G`, the actual GP–Poisson energy to leading cold order is

\[
 E_c=\int\left[{\hbar^2\over8m^2}{|\nabla\rho_c|^2\over\rho_c}
       +{\rho_c|v_c|^2\over2}+{\kappa_c\rho_c^2\over2}\right]
       +{1\over2}\int\rho_c\Phi_c+\int\rho_c\Phi_b,
 \quad \Delta\Phi_a=K\rho_a.                           \tag{3}
\]

Add the baryonic kinetic, material and self-gravitational energies when
its coordinates are live. The cross energy in (3) occurs once. The probe
source is `rho_c+rho_b` at this order. Full relativistic energy includes
interaction, gradient, detuning and stress contributions; no exact
all-energy response theorem is inferred by calling `mQ` their sum.
The separate attractive `Psi,chi` host, nodal fermions and canonical `P`
are not imported into (3).

For the executed state, condition on an ordinary matter sphere with
constant density `rho_b0>0`, radius `R_b`, and mass
`M_b=4 pi rho_b0 R_b^3/3`. The baryons are live. Their ideal incompressible,
nonrotating material limit and freely moving boundary are state/material
hypotheses, not new scalar interactions or a rigid external anchor. A
real baryonic equation of state, its preparation and its full shape-mode
stability have not been supplied by the carrier action. This restriction
is material: arbitrary host relaxation must be restored before applying
the result to an actual galaxy.

## 2. Execute a finite scalar state rather than assume a spring

At zero flow, minimizing (3) at fixed scalar mass gives

\[
 \bar\mu=-{\hbar^2\over2m^2}{\Delta\sqrt{\rho_c}\over\sqrt{\rho_c}}
             +\kappa_c\rho_c+\Phi_c+\Phi_b.           \tag{4}
\]

`bar mu` is chemical potential per unit mass above rest energy. Drop
quantum pressure only in the Thomas–Fermi bulk and place the first zero
of the scalar density at `R<R_b`. Inside the host,

\[
 \Phi_b(r)=\Phi_b(0)+{K\rho_{b0}\over6}r^2,
 \qquad q^2={K\over\kappa_c}.
\]

Applying the Laplacian to (4), then imposing regularity at the origin,
gives the actual finite profile

\[
 \boxed{\rho_c(r)=A{\sin(qr)\over qr}-\rho_{b0}\quad(0\le r<R),
 \qquad \rho_c=0\quad(r\ge R),}
 \quad A=\rho_{c0}+\rho_{b0}.                          \tag{5}
\]

Let `x=qR`. The first zero, positivity and total mass conditions are

\[
 0<x<\pi,\quad A=\rho_{b0}{x\over\sin x},\quad
 \rho_{c0}=\rho_{b0}\left({x\over\sin x}-1\right)>0,
\]
\[
 \boxed{M_c={4\pi\rho_{b0}\over q^3}
              \left[x-x^2\cot x-{x^3\over3}\right].} \tag{6}
\]

These follow by integrating `r^2 rho_c`: the required primitive is
`sin x-x cos x`. The mass is positive because the density in (5) is
positive before its first zero. The bracket rises continuously from zero
to infinity: its derivative is `(1-x cot x)^2>0` on `0<x<pi`. Thus each
positive `M_c` selects one `x` before imposing `R<R_b`; the latter condition
restricts the allowed host-confined masses. This selects the actual mass
and radius of the state rather than fitting a force coefficient. `q`
comes from existing `g2,m,G`; `M_c`,
`rho_b0`, and `R_b` are physical population/host data.

For `x<<1`, the profile reduces to the trap-dominated parabola

\[
 \rho_c=\rho_{c0}\left(1-{r^2\over R^2}\right)+O(x^4\rho_{b0}),
 \quad \rho_{c0}={\rho_{b0}x^2\over6}+O(x^4\rho_{b0}),
 \quad M_c={4\pi\rho_{b0}x^5\over45q^3}+O(\rho_{b0}x^7/q^3).
                                                        \tag{7}
\]

For an isolated self-gravitating TF scalar, instead set `rho_b0=0` before
imposing the boundary. Then

\[
 \rho_c=\rho_{c0}{\sin(qr)\over qr},\quad R={\pi\over q},\quad
 M_c={4\pi^2\rho_{c0}\over q^3},\quad
 \bar\mu=\Phi_c(R)=-{GM_c\over R}.                  \tag{8}
\]

Thus self-gravity itself supplies an allowed finite scale; it supplies
no restoring force for translation of the isolated scalar center.

The baryon pressure needed in the centered two-component configuration is
explicitly

\[
 p_b(r)=\int_r^{R_b}\rho_{b0}
           {G[M_b(<s)+M_c(<s)]\over s^2}\,ds\ge0,
 \quad p_b(R_b)=0.                                  \tag{9}
\]

Together (5) and (9) solve the static Euler–Poisson force equations of
this conditional TF/incompressible model. To recover the undifferentiated
scalar equation, `kappa_c rho_c+Phi_c+Phi_b` is a regular spherical harmonic
function inside the support and hence constant; choose `bar mu` as its
value at `R`. Outside `R`, the total spherical potential increases
outward, so `bar mu-Phi_c-Phi_b<0` and the nonnegative-density TF
variational condition permits the vacuum there. The free boundary thus
satisfies the density inequality as well as the bulk equation. They are
not just a positive Hessian attached to an unspecified reference.
Positivity of the optical Hessian below proves stability in that displacement sector, not global
stability to every shape, fragmentation, vortex or conversion mode.

TF control requires a bulk healing length
`xi~hbar/[sqrt(2) m sqrt(kappa_c rho_c)]` small compared with the scale of
the profile and `R`, as well as `kappa_c rho_c`, `|Phi|`, and flow energies
small in cold/weak-field units. Close to `rho_c=0`, quantum pressure
cannot be neglected. The exact Hartree profile smooths this boundary and
has tails. Taking `R_b-R` large compared with the boundary layer keeps
almost all scalar mass inside the harmonic host. Equations (5)–(8) are
exact states of the stated TF truncation and controlled bulk candidates
for GP; no exact closed-form finite-`hbar` Hartree solution or all-mode
stability theorem is claimed.

## 3. Finite overlap has a positive displacement Hessian

Translate the entire scalar density by `d` relative to an otherwise
unchanged host. Its contact, quantum, and self-gravitational energies
are invariant. The actual varying energy is

\[
 E_{cb}(d)=\int\rho_c(y)\Phi_b(y+d)\,d^3y,
\]
\[
 E_{cb}(d)=E_{cb}(0)+d_i F_i+{1\over2}d_iH_{ij}d_j+O(d^3),
 \quad F_i=\int\rho_c\partial_i\Phi_b,
 \quad\boxed{H_{ij}=\int\rho_c\partial_i\partial_j\Phi_b.} \tag{10}
\]

The integral may be taken in the distributional sense for piecewise
smooth profiles. At concentric spherical equilibrium `F=0` and isotropy
plus Poisson give

\[
 \boxed{\operatorname{tr}H=K\int\rho_c\rho_b,
 \qquad H_{ij}={K\over3}\delta_{ij}\int\rho_c\rho_b.} \tag{11}
\]

Nonzero positive overlap therefore gives a positive relative spring.
For (5),

\[
 H_{ij}=h\delta_{ij},\qquad
 \boxed{h={K\rho_{b0}M_c\over3}.}                  \tag{12}
\]

As long as the whole TF scalar support remains inside the uniform host,
`E_cb(d)-E_cb(0)=h|d|^2/2` exactly; the harmonic host has no cubic or
higher translation term in that domain. For a smoothed spherical
Hartree profile with tails, (11) remains exact, while (12) uses the mass
inside `R_b` rather than the entire `M_c`. A small outside mass fraction
therefore controls the Hessian correction. Exact dipole-mode decoupling
from shape modes requires a harmonic host over the occupied region;
finite tails weaken that idealization.

Positive trace alone does not prove a positive matrix for nonspherical
geometry. Away from a compact source, a pointlike scalar sees the Hessian
`GM_b(1-3 nn)/r^3`, with a negative radial and two positive transverse
eigenvalues, and zero trace. A spherical shell's empty cavity has zero
Hessian. Geometry and actual overlap matter.

This does not contradict the homogeneous result. A rigid translation of
a finite inhomogeneous object is neither a homogeneous fluid compression
nor a plane-wave density perturbation of an infinite gravitating medium.
There is a real positive finite-state optical door here, but it must be
tested with its own operator and source.

## 4. Live-host dynamics and the gravity-conjugate form factor

Let `x_c,x_b` be the centers. Define

\[
 M_T=M_c+M_b,\quad \mu_r={M_cM_b\over M_T},\quad
 \alpha={M_b\over M_T},\quad\beta={M_c\over M_T},
\]
\[
 R={M_cx_c+M_bx_b\over M_T},\qquad d=x_c-x_b,
 \quad x_c=R+\alpha d,\quad x_b=R-\beta d.
\]

Rigid translations of both components have the exact quadratic kinetic
and interaction energies

\[
 T={M_T\over2}|\dot R|^2+{\mu_r\over2}|\dot d|^2,
 \qquad E^{(2)}={1\over2}d_iH_{ij}d_j.              \tag{13}
\]

The optical frequencies are eigenvalues of `H/mu_r`. For the uniform
host state,

\[
 \boxed{\Omega_{\rm opt}^2={K\rho_{b0}\over3}
                      \left(1+{M_c\over M_b}\right)>0.} \tag{14}
\]

For a fixed harmonic host, translating a GP solution rigidly, boosting
its phase by the center velocity and using its unchanged internal
self-potential gives `ddot x_c=-K rho_b0(x_c-x_b)/3` directly in the
GP equation. The host receives the opposite net force. In the stated
incompressible spherical host, the regular irrotational `l=1` density
boundary displacement is its translation. The pressure adjustment can
be checked explicitly. In host-centered coordinates `y`, the relative
scalar shift gives `delta Phi_c=-d dot grad Phi_c`, and a uniform host
acceleration `a_b` is compatible with

\[
 \delta p_b=-\rho_{b0}(\delta\Phi_c+a_b\cdot y).
\]

At `|y|=R_b`, `delta Phi_c=-GM_c d dot y/R_b^3`, so the free-surface
condition `delta p_b=0` fixes `a_b=GM_c d/R_b^3=h d/M_b`, exactly
the force opposite to that on the scalar. This supplies the live
counterpart in the admitted dipole sector.
Higher host shape response and deviations from a harmonic occupied
region require the full linearized fluid/GP problem. They cannot be
replaced by the previous radial breathing curvature.

A uniform external gravitational acceleration `g` has energy

\[
 E_{\rm probe}=-g\cdot(M_cx_c+M_bx_b)=-M_Tg\cdot R. \tag{15}
\]

It has no `d` source. Holding `x_b=0` would instead require a reaction
force and would change this source problem. A large `M_b` does not
permit dropping `M_b x_b`: its small recoil still cancels the internal
mass dipole.

For an actual finite-wavelength probe use `rho_k=integral rho e^{-ikx}`.
Let `F_a(k)=M_a^{-1} integral rho_a(y)e^{-iky}` be the actual centered
normalized form factors. The full source operator in this projection is

\[
 \rho_k=e^{-ik\cdot R}\left[
 M_cF_c(k)e^{-i\alpha k\cdot d}
       +M_bF_b(k)e^{+i\beta k\cdot d}\right].        \tag{16}
\]

For the executed state the geometry is explicit:

\[
 F_b(k)={3[\sin(kR_b)-kR_b\cos(kR_b)]\over(kR_b)^3},
 \quad F_c(k)={4\pi\over M_c}\int_0^R
 r^2\left[A{\sin(qr)\over qr}-\rho_{b0}\right]
                   {\sin(kr)\over kr}\,dr.          \tag{17}
\]

There is no fitted form factor. Its two integrals are elementary:

\[
 M_cF_c(k)={2\pi A\over qk}
 \left[{\sin((q-k)R)\over q-k}-{\sin((q+k)R)\over q+k}\right]
 -{4\pi\rho_{b0}\over k^3}[\sin(kR)-kR\cos(kR)],
                                                        \tag{18}
\]

with removable limits understood. As a check, the isolated TF profile
(8) gives `F_c=pi^2 sin y/[y(pi^2-y^2)]`, `y=kR`.

The source vertex of the *relative* displacement at `d=0` is

\[
 \boxed{Q_i(k)={\partial\rho_k\over\partial d_i}\bigg|_0
           =-i\mu_r k_i[F_c(k)-F_b(k)].}             \tag{19}
\]

For centered spherical profiles

\[
 F_a(k)=1-{k^2\langle r^2\rangle_a\over6}+O(k^4),\quad
 Q_i={i\mu_r\over6}k_i k^2
       (\langle r^2\rangle_c-\langle r^2\rangle_b)+O(k^5).
                                                        \tag{20}
\]

The leading `k` terms cancel because the gravitational charge/inertial
mass ratio is the same for both populations. In particular, the retarded
one-optical-mode density susceptibility per object, defined by
`delta rho_k=-chi(k,omega) delta Phi_k` with consistent Fourier source
normalization, is

\[
 \boxed{\chi_{\rho,\rm opt}
 =Q_i[(H-\mu_r z\,1)^{-1}]_{ij}Q_j^*
 ={\mu_r k^2|F_c-F_b|^2\over\Omega_{\rm opt}^2-z},
 \quad z=(\omega+i0)^2.}                            \tag{21}
\]

It begins at `k^6` in this co-centered spherical dipole projection. For a
population, multiply by the actual number per volume and include its
spatial correlations/interobject dynamics; independent objects are an
additional approximation. If normalized profiles coincide, this one-mode
linear vertex vanishes at every `k`, though their scalar-only vertices
do not.

There are additional channels. Expanding (16) to second order in `d`
gives `-mu_r (k dot d)^2/2+O(k^4 d^2)` at small `k`. Quantum two-quantum
or finite-temperature fluctuation channels and ordinary shape quadrupoles
can therefore have matrix elements `O(k^2)` and density spectral weight
`O(k^4)`. A separated equilibrium with a permanent internal quadrupole
can also have `O(k^4)` one-mode weight. More generally, after subtracting
the total COM of a compact object, the total mass operator has no
internal `O(k)` term. For nonsingular finite internal gaps, its leading
possible internal matrix elements are tidal `O(k^2)`. This statement does
not assume all internal modes are gapped in every infinite-medium limit.

The translating COM retains an ordinary `O(k^2)` density spectral weight:
its finite-frequency contribution is
`chi_COM=-k^2|M_c F_c+M_b F_b|^2/(M_T z)` in this rigid projection.
It is present before and after internal binding. Measuring or forcing
only the scalar would replace (19) by `-i mu_r k F_c`, and can give
`O(k^2)` relative oscillator weight. Such a differential source is not
the universal gravitational source of the live two-component system.
No independent gravitational charge is inserted to obtain it.

If extra host coordinates `eta` relax, the static Hessian becomes
`H_eff=H-B C^{-1} B^T` on an invertible positive shape block `C`.
Its source becomes `Q_eff=Q_d-B C^{-1} Q_eta`, and a source-only response
also remains. Thus positive frozen-profile overlap is a real diagnostic,
not a guarantee that arbitrary live-host relaxation leaves that same
spring. Translation zero modes must be separated before inversion.

## 5. Compare the actual operator with the canonical material action

The canonical source/current convention is
`div P=delta rho`, `dot P=-j`. If `u_c` is the ordinary physical scalar
displacement, its first-order map is therefore

\[
 P_c=-\rho_c u_c,\qquad
 \delta\rho_c=-\nabla\cdot(\rho_cu_c)=\nabla\cdot P_c. \tag{22}
\]

Calling `-u_c` the displacement reverses this sign convention without
changing any energy. Equation (22) represents a zero-total-mass change
about the specified finite profile. A positive stock `M_c` cannot itself
equal `integral div P_c` for decaying `P_c` without a subtracted background
or boundary flux. The original finite profile remains a gravitational
source counted once; declaring it an unpolarized background is not yet
the canonical cosmological background/domain dictionary. In the host
frame `u_c=d`; in the total-COM frame
`u_c=alpha d` and the host has `u_b=-beta d`. Omitting the host's own
`P_b=-rho_b u_b` omits precisely the recoil source in (19). A scalar-only
`P_c` can be a partial material observable, but it is not the full
uniform gravity-conjugate mass dipole.

Even with a prescribed host, the exact translation has a nonlinear
conserved-density map, not just its first-order representative:

\[
 P_c[d](x)=-d\int_0^1\rho_c(x-sd)\,ds,
 \quad\nabla\cdot P_c[d]=\rho_c(x-d)-\rho_c(x),
\]
\[
 P_c[d]=-\rho_c d+{1\over2}d(d\cdot\nabla\rho_c)+O(d^3).
                                                        \tag{23}
\]

Substituting it in the ordinary existing source energy gives

\[
 \int\Phi_b\,\delta\rho_c
      =-\int\nabla\Phi_b\cdot P_c[d]
      ={1\over2}d_iH_{ij}d_j+O(d^3)                 \tag{24}
\]

at the centered state. Thus the overlap spring is already the quadratic
expansion of baryon–scalar gravitational energy along this nonlinear
advection path. If it is represented as a spring in a reduced mechanical
energy, it has been counted there once. One cannot keep the same full
Poisson/source energy and add it again as an independently derived
material `K P^2/2`. Scalar contact, quantum, and scalar self-gravity are
translation invariant along this path.

For clarity, test the proposed excess collective polarization by
projecting the *target* material functional about `P=0` onto the linear
host-frame map `P_c=-rho_c d`. This is a conditional matching test of
that candidate operator, not a completed full-background identification.
With
`A2=integral rho_c^2` and `B2=integral |grad rho_c|^2`, its quadratic
coefficient would be

\[
 h_{\rm can}=K A_2+\gamma B_2,
 \qquad h_{\rm overlap}={K\rho_{b0}M_c\over3}.       \tag{25}
\]

For (5), integration by parts using `rho_c(R)=0` gives

\[
 B_2=q^2(A_2+\rho_{b0}M_c),
\]
\[
 A_2={4\pi\over q^3}\left[
 A^2\left({x\over2}-{\sin2x\over4}\right)
 -2A\rho_{b0}(\sin x-x\cos x)+{\rho_{b0}^2x^3\over3}\right].
                                                        \tag{26}
\]

Consequently even equality of these two projected numbers would require
the state-dependent equation

\[
 {\rho_{b0}M_c\over3}
   =A_2+{\gamma\over\kappa_c}(A_2+\rho_{b0}M_c).    \tag{27}
\]

It is not an identity of the scalar theory. In the trap-dominated
parabolic limit, `M_c/A2=7/(4 rho_c0)` and the coefficient inferred by
normalizing the overlap spring to `integral P_c^2` is
`7 K rho_b0/(12 rho_c0)`, not a universal `K`. The physical map fixes
this normalization; an adjustable rescaling of `P` also changes its
source and density identity. A numerical coincidence on one rigid
three-dimensional subspace would establish neither the full functional
nor avoid the source double count in (24). If the proposed full canonical
background is instead `P_0!=0`, its material Hessian includes the actual
radial/transverse Hessians of `W_rem` at `P_0`. Those terms must be
computed in that same physical map; (25) is not their replacement.

The full constitutive requirements also remain unmatched in this
particular control. Its exact nested-overlap translation energy is
quadratic. In the proposed excess map about `P=0`, the target remainder is

\[
 W_{\rm rem}(K|P|)
 ={K^2\over3a_0}|P|^3+{K^3\over4a_0^2}|P|^4+\cdots
\]

and therefore has a nonzero positive cubic and the branch limit
`K|P|<a0`.
Neither that scale/domain nor the full logarithmic saturation is generated
by (3), (5), or (10). The rigid mode has no independently derived local
stiffness coefficient `gamma=K L_*^2/2`. Nonuniform scalar displacements
instead change compression and quantum pressure; the leading contact
term is `kappa_c (div P_c)^2/2`, with its actual background and advection
terms retained. It is not a proof of the entire vector `|grad P|^2`
functional with the canonical coefficient.

No universal analytic-branch exclusion is asserted for every finite free
boundary. As a useful check, two coextensive sharp uniform balls of
radius `R` have overlap volume
`V(d)=4 pi R^3/3-pi R^2|d|+pi|d|^3/12` for `|d|<2R`.
Poisson in displacement space gives
`Delta_d E_cb=K rho_c rho_b V(d)`. Integrating the radial equation gives

\[
 E_{cb}(d)-E_{cb}(0)={GM_cM_b\over R}
 \left[{1\over2}\left({|d|\over R}\right)^2
       -{3\over16}\left({|d|\over R}\right)^3
       +{1\over160}\left({|d|\over R}\right)^5\right]. \tag{28}
\]

This boundary-induced cubic exists, has the opposite sign to the required
positive remainder, and depends on the moving support geometry. Those
hard scalar balls are not asserted to solve the original repulsive GP
state equations. The calculation prevents confusing a discontinuous
support with a nonsingular amplitude elimination or claiming that every
finite object has an analytic translation energy.

## 6. Release, restoration, and the unresolved history test

The overlap spring is present for any prescribed mass density profiles;
(10) contains no condensate fraction. Replacing a coherent scalar by an
uncondensed cloud with the same instantaneous translated density leaves
this gravitational curvature unchanged. Its dynamic susceptibility can
change through pressure, velocity distribution, collisions, and host
relaxation. None of those changes is a derived binary deletion of the
extra canonical operator.

An escaper that leaves the host can lose the positive overlap spring.
This is a genuine geometric change: around the old center there is no
longer an occupied translating bound cloud. It is not a permanent
internal response label on retained ordinary mass. An isolated surviving
self-gravitating droplet still has a free COM and internal tidal response.
A cloud outside a compact host has the actual tidal Hessian, and an
orbit can have epicyclic restoring behavior only after its angular
momentum and Coriolis dynamics are included. An orbital radial curvature
cannot be substituted as an independent Cartesian anchor.

In the ideal bound harmonic projection, an impulse in the relative
coordinate produces undamped oscillations at (14). At a genuine
unbinding threshold, the bound normal-mode description ceases to be a
valid stationary-state expansion; a zero spring limit produces soft or
free motion, not a zero universal mass vertex. A fitted linewidth,
thermal bath, release rate or permanent capture prohibition is not
introduced. The conservative original action does not itself encode an
irreversible rule that forbids re-entry or energy exchange after a host
is restored.

The decisive comparison is a mode-resolved response measurement before
release and after restoring the same baryonic field, scalar mass and
specified density profile, with the probe normalization fixed:

1. In the admitted bound state, measure `Omega_opt` and the full-source
   form-factor residue in (21), including host recoil and the separate
   COM/tidal channels.
2. Release by a specified host history and account for its work, ejected
   flux, final currents and scalar velocity/phase distribution. Merely
   relabeling a population supplies none of these data.
3. Restore the host and probe again. If the same centered density profiles
   and the same conditional dipole sector are restored, (10)–(14) restore
   the same overlap curvature. Condensation loss alone cannot erase it.
   If the returned material occupies another orbit, anisotropic kinetic
   distribution, vortex, fragmented state or other metastable sector,
   derive that state's susceptibility and receiver dynamics explicitly.

Different collisionless distributions can share a spatial density while
having different kinetic stresses and response. This note has not
classified those states or excluded nonlinear orbital/collective
metastability. Such a state could provide history dependence in ordinary
susceptibility, but it must also reproduce the canonical material energy,
source, admissible domain and retained off branch. A geometric overlap
spring or a conserved orbital quantity alone does not establish that
implication. Its lifetime requires actual decay/transport channels and
the preparation/return state, not a fitted rate.

## 7. Exact outcome and continuation

The completed bounded implication is:

`original matched repulsive scalar + stated finite host/material state`
`-> explicit finite TF density + positive overlap optical curvature`
`-> live reduced-mass mode + full finite-wavelength mass source`.

The next implication fails for the executed nested-overlap control:
that mode does not reproduce the canonical material functional under its
physical density/current map. Its spring is existing cross gravity, its
uniform internal mass source cancels, its optical mass residue is `k^6`,
and its translation branch lacks the required positive cubic, saturation
and universal stiffness. This is a scoped mismatch, not a theorem against
all finite, singular, nonlinear or thermal collective states.

Substantive open continuation: specify a realizable finite host equation
of state and a prepared nonlinear scalar state after a release/restore
cycle; solve the coupled linearized GP–host response, retaining COM,
shape, phase and current sectors. At fixed restored environment, test
whether it has a long-lived different response **of the same physical
operator**, and compare its actual full functional/source with the
canonical target. A continuum/large-object singular limit must be taken
with the form factors and spectral weight before importing an effective
local optical field. No such limit or receiver lifetime is settled here.

Verification: raw Euler–Poisson reduction, finite profile integration,
rigid translation, Poisson trace, COM/reduced-mass separation, source form
factors, retarded harmonic inversion, nonlinear conserved-density map,
and displacement-space Poisson integration were checked analytically.
No scientific process, symbolic-package run, numeric scan, fit, owner-job
inspection or Git operation was used. New fitted parameters: zero.
The incompressible host and TF regime are explicit conditional inputs,
not derived cosmic state data. This is author derivation/self-review;
independent reconstruction is required before strong claims are relied on.

Proofread using `mathbox:proofread-math` in self-review mode, restricted to
this new note. Routine edits: notation/prose consistency. Mathematical
content was derived in this note; no unrelated source token was changed.
The two allowed output files are the only writes by this lane.
