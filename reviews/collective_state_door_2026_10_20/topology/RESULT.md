# Winding stores circulation, but does not switch the calculated longitudinal response

20 October 2026. Parent: `../TARGET.md`, assessment base supplied there
`cc07e00a3ba0f2917f16d834b6ca54bcd93a4dcf`. Actual input bytes are pinned in
`source_hashes.json`; no Git revision is inferred from the shared working
tree. This lane writes only this file and its source pin file. Original
carrier/source fields only; natural units, including `hbar=1`.

**Normalized target and verdict: incomplete, with the physical
polarization operator and its constitutive action still missing.** In an
explicit conditional occupied ring, the original action supports common
phase winding and a corresponding persistent stationary current. Its
longitudinal response is convected compressible sound. In the stable
hydrodynamic domain, it is nonzero in every occupied winding sector;
opposite windings have equal static density susceptibility and opposite
circulation. Thus retained winding can distinguish microscopic histories
without storing the requested response-on/response-off bit in this
calculated operator. This does not exclude every inhomogeneous, thermal,
quantum, or separately defined extra-force operator of the same fields.

An explicit fixed-charge homotopy also gives a finite upper bound on the
energy barrier between neighboring ring windings. It supplies no decay
rate. An isolated rotationally symmetric system must additionally transfer
the angular momentum difference to other existing excitations or a live
host. No ring, pinning potential, bath, fitted rate, or new fundamental
field is asserted to exist in a halo.

## 1. Inputs, novelty boundary, and obligations

The raw starting point is the retained-source NR Hamiltonian displayed in
`MASTER_COLD_ENERGY_EQUATIONS.md`, not the separate mediator/host model,
the nodal fermions, or an already installed canonical polarization field:

\[
 H=mQ+\int_\Omega\left[
 { |\nabla\psi|^2\over2m}+{ |\nabla b|^2\over2M}
 +\delta |b|^2+g(b^*\psi^2+b\psi^{*2})+\lambda |\psi|^4
 \right]d^3x,
 \quad Q=\int_\Omega(|\psi|^2+2|b|^2),                 \tag{1}
\]

where `delta=M-2m>0`, `g=c3>0`, and `lambda=kc` with exactly the
positive-frequency convention in MASTER. In particular
`lambda delta>g^2`. The threshold-matched `kR` is not substituted for
`kc`. A weak external gravity probe below first uses the inherited leading
cold source `rho_Q=mq`, `q=|psi|^2+2|b|^2`; section 2 records its precision.

Targeted prior-log searches found these nearest overlaps:

* `sol61_push/nonthermal_state_2026_10_19/topology/DERIVATION.txt`, section
  1, already derives the mixed-phase winding relation, `Jz=ell Q`, the
  point vacuum manifold, and finite-stock vortex escape. Its RESULT says
  another vortex formula does not close the protected-state objective.
* `sol61_push/particle_derivation_2026_10_18/density_duality/DENSITY_DUALITY.md`,
  sections 2–3, already retains compact/vortex sectors and distinguishes
  charge from mass. The coherent-current note already derives the species
  source and current ledger used below.
* The inherited `phases/RESULT.md`, equations (5)–(8), calculates the
  zero-flow common phase and its derivative displacement kernel. Its
  explicit unclassified cases include vortices.
* The AS1411/AS1413 work orders are marked proposed/not dispatched and use
  a different `Psi,Chi,s` action. They are not executions of this test.
  The September `local_winding_clock_2026/REPORT.md` studies a curvature
  clock/multiplier construction, rather than the density response of (1).

Accordingly, phase locking, `Jz=ell Q`, and absent vacuum protection are
**inherited**, not discoveries here. The new bounded continuation is the
explicit winding-dependent branch of (1), its source-specific longitudinal
susceptibility, the response/restoration discriminator, and a finite-energy
same-field phase-slip path. No global novelty claim follows from local rg.

Dependency graph:

`(1) -> conditional occupied geometry -> locked winding branch -> h(q,p)
-> density/source Hessian -> longitudinal response -> P/action comparison`.

Independently, `(1) + allowed zeros -> fixed-Q phase-slip path -> energetic
upper bound`. A physical confining state, its stability/preparation, the
actual extra-force operator, receiver transport, and a retention time are
additional obligations, not consequences of this graph.

## 2. Locking, currents, topology, and the exact source ledger

Write `psi=sqrt(n) exp(i theta_a)` and
`b=sqrt(n_b) exp(i theta_b)`. The conversion energy is
`2g n sqrt(n_b) cos(theta_b-2theta_a)`. At nonzero mixed amplitudes it is
minimized at

\[
 \theta_b=2\theta_a+\pi\pmod {2\pi}.                 \tag{2}
\]

The canonical one-form is
`-n dot theta_a-n_b dot theta_b`. In the locked chart it is
`-q dot theta`, `theta=theta_a`. The number and conserved-charge currents
are

\[
 j_a={n\over m}\nabla\theta_a,\quad
 j_b={n_b\over M}\nabla\theta_b,\quad
 J_Q=j_a+2j_b=C\nabla\theta,\qquad
 C={n\over m}+{4n_b\over M}>0.                       \tag{3}
\]

The exact NR species balances from (1) are
`dot n+div j_a=2 R`, `dot n_b+div j_b=-R`, with
`R=2g Im(b psi*^2)`. Locked stationary fields have `R=0`. A phase slip
does not need an inserted conversion rate; these equations retain the
relative-phase exchange whenever it is present.

On a loop where both amplitudes remain nonzero and (2) holds, single
valuedness gives

\[
 {1\over2\pi}\oint d\theta_a=\ell\in\mathbb Z,
 \qquad \ell_b=2\ell.                               \tag{4}
\]

The occupied mixed-phase circle has this integer label. The zero-density
vacuum of the original positive-square action is instead `Phi=X=0`.
Consequently (4) is not a vacuum topological charge of a finite isolated
lump. A zero of a field invalidates the corresponding winding chart;
finite stock has vanishing-amplitude outer regions through which defects
can leave. A charge-two-only chart and relative-phase walls have different
allowed defects and cannot be silently assigned the mixed-sector label.

For the single azimuthal harmonic `(ell,2ell)`, the canonical angular
momentum is `Jz=ell Q`. In a ring of radius R the species velocity
circulations are `2pi ell/m` and `4pi ell/M`. They coincide only at equal
mass per charge, whereas here `M=2m+delta`. Keeping this difference also
keeps the exact rest-inventory identities:

\[
 \rho_{\rm rest}=mq+\delta n_b,
 \quad j_{\rm rest}=m j_a+M j_b,
 \quad\dot\rho_{\rm rest}+\nabla\cdot j_{\rm rest}=-\delta\mathcal R.
                                                               \tag{5}
\]

For a locked flow `j_rest=q grad theta`, while `m J_Q=m C grad theta`.
These are not interchangeable exact currents. Kinetic, detuning,
interaction and stress energy complete the relativistic gravitational
source. The inherited pointwise positive-charge bound is
`0<=(rho_rest-mq)/rho_rest<=delta/M`; using `mq` is the stated cold
approximation, not an exact gravitational-mass identity. No conversion
rest-energy deficit is used to manufacture a new gravitational charge.

## 3. Explicit conditional ring state and sector energy

For a transparent solvable control choose a finite periodic product
waveguide `S1_L x Sigma`, transverse area `mathcal A`, volume
`V=mathcal A L`, with reflecting transverse boundary and a uniform
transverse mode. This is an externally selected geometry/boundary
condition. It is an exact finite-volume problem for (1); a thin embedded
annulus approaches it when transverse width divided by radius is small.
It is not a derived confining halo or an added dynamical field.

For constant amplitudes the following is an exact stationary solution
of that control when the displayed branch inequalities hold:

\[
 \psi=\sqrt n\,e^{i(ps-\mu t)},\quad
 b=-{g n\over\Delta_p}e^{2i(ps-\mu t)},\quad
 p={2\pi\ell\over L},\quad
 x={p^2\over2m},\quad y={2p^2\over M},
\]
\[
 \alpha=\mu-x,\quad
 \delta_p=\delta+y-2x
   =\delta\left(1-{p^2\over mM}\right),\quad
 \Delta_p=\delta_p-2\alpha,\quad
 \kappa_p=\lambda-{g^2\over\Delta_p},\quad
 n={\alpha\over2\kappa_p},\quad
 q=n+{2g^2n^2\over\Delta_p^2}.                       \tag{6}
\]

The conditions are `alpha>0`, `Delta_p>0`, `kappa_p>0`; equivalently,
for this occupied grand branch,
`lambda delta_p>g^2` and
`0<alpha<(delta_p-g^2/lambda)/2`. NR validity additionally requires
small gradients/chemical shifts relative to the retained masses. Thus
winding changes the effective detuning continuously; it is not a label
that leaves the field equations unchanged while removing their response.

At fixed positive q the exact homogeneous-sector energy above `mq` is

\[
 h(q,p)=\min_{0\le n\le q}F(q,n,p),
\]
\[
 F={p^2n\over2m}+{(\delta+2p^2/M)(q-n)\over2}
       -\sqrt2 g\,n\sqrt{q-n}+\lambda n^2.          \tag{7}
\]

The composition Hessian is

\[
 F_{nn}=2\lambda+
 {\sqrt2 g(4q-3n)\over4(q-n)^{3/2}}>0\quad(0<n<q).
                                                               \tag{8}
\]

When `delta_p>0`, `F_n(0)<0` and `F_n(q^-)=+infinity`, giving a unique
mixed composition in that sector. This is a composition statement; it
does not prove stability against all phase, transverse or gravitational
perturbations. The stated small-flow stable domain is imposed explicitly
in section 4.

Because the flow term in (7) is
`p^2[n/(2m)+(q-n)/M]` and `M>2m`, minimization gives the useful exact bounds

\[
 {q p^2\over M}\ \le\ h(q,p)-h(q,0)
       \ \le\ {q p^2\over2m}.                      \tag{9}
\]

Here the lower bound follows pointwise before minimizing; for the upper
bound insert the zero-flow minimizing composition. Thus `E_ell=mQ+Vh`
is finite, even in ell, and increases with p squared. For small flow,
the envelope identity gives
`h(q,p)=h(q,0)+C(q,0)p^2/2+O(p^4)` and exactly `h_p=C(q,p)p`.

In a true finite-width cylindrical annulus the stationary amplitudes are
not constants. For `psi=f(r,z)e^{i(ell phi-mu t)}`,
`b=-u(r,z)e^{2i(ell phi-mu t)}`, the leading `mq` external-potential
equations are, with `D=partial_r^2+r^-1 partial_r+partial_z^2`,

\[
 \mu f=\left[-{D\over2m}+{\ell^2\over2mr^2}
                  +m\Phi_N+2\lambda f^2-2g u\right]f,
\]
\[
 2\mu u=\left[-{D\over2M}+{2\ell^2\over Mr^2}
                       +\delta+2m\Phi_N\right]u-gf^2.          \tag{10}
\]

Their actual host, boundary, Poisson source and transverse modes must be
solved to claim a physical annular object. Replacing `2m Phi_N` with
`M Phi_N` at the source rest-mass correction order also requires completing
that order's stress-energy ledger. Equations (6)–(9) do not solve (10)
or establish self-confinement or astrophysical preparation.

## 4. Actual winding-dependent longitudinal response

Work below the amplitude/relative-phase frequencies and below transverse
excitations. Keep the gapless common phase. Eliminate the composition
locally by the minimum in (7), retaining its source dependence. About a
uniform state `(q0,p)`, write `theta=ps-mu t+vartheta` and define the
actual derivatives of this same h:

\[
 A=h_{qq},\qquad B=h_{qp},\qquad D_h=h_{pp}.          \tag{11}
\]

The positive energetic domain considered here has
`A>0`, `D_h>0`, `A D_h>B^2`. It contains sufficiently small flow on the
stable zero-flow branch. An unstable/supersonic sector is not interpreted
as an inert response-off state. The leading quadratic action is

\[
 \mathcal L_2=-\delta q\,\dot\vartheta
 -{A\over2}(\delta q)^2-B\delta q\,\partial_s\vartheta
 -{D_h\over2}(\partial_s\vartheta)^2-m\Phi_N\delta q.
                                                               \tag{12}
\]

Gradient corrections from the original amplitude gradients and dynamical
relative/composition response enter beyond this hydrodynamic order;
(12) is not asserted at their gaps. The source in (12) is exactly the
chosen leading cold density, not an independently chosen force vertex.
The two equations are

\[
 (\partial_t+B\partial_s)\delta q+D_h\partial_s^2\vartheta=0,
 \qquad(\partial_t+B\partial_s)\vartheta=-A\delta q-m\Phi_N.
\]

For a nonzero periodic harmonic `k=2pi j/L`, they give

\[
 \boxed{\delta\rho_Q=-\chi_\rho\Phi_N,\qquad
 \chi_\rho(k,\omega)={m^2 D_h k^2\over
 A D_h k^2-(\omega-Bk+i0)^2}}
 \quad\hbox{at the order of (12)},                 \tag{13}
\]
\[
 \boxed{\chi_\rho(k,0)={m^2D_h\over A D_h-B^2}>0.} \tag{14}
\]

Fixed Q excludes the uniform density mode `j=0`; the static claim is for
nonzero modes in the hydrodynamic range. A continuum `k->0` comparison
means a family of admitted large geometries/local bulk wavelengths, not
inventing continuous harmonics in one finite ring. At p=0,
`D_h=C`, `B=0`, `A=1/q_mu`, recovering the inherited phase response.
At small p, `B=C_q p+O(p^3)`, with smooth even changes of A and D_h.

Time reversal gives the particularly clean discriminator:

\[
 h(q,p)=h(q,-p),\quad A,D_h\text{ even in }p,
 \quad B\text{ odd in }p,
 \quad\chi_\rho^{(+\ell)}(k,0)=\chi_\rho^{(-\ell)}(k,0),
 \quad J_Q^{(+\ell)}=-J_Q^{(-\ell)}.                \tag{15}
\]

The sectors are distinguishable by current and Doppler-shifted spectra,
while their static density response is identical in this control. The
evenness of the static density response also follows from time reversal
of the full real static Hamiltonian and a real scalar source, whenever
corresponding stable states and the same boundaries are compared.

For intuition only, neglecting the small detuning-to-mass correction in
the kinetic coefficients gives `C=q/m`, `B=p/m=v`, `D_h=q/m` and
`c_s^2=q A/m`. Then (13) is
`chi=rho k^2/[c_s^2 k^2-(omega-vk+i0)^2]`; its subsonic static value
is `rho/(c_s^2-v^2)`, not zero. This limiting expression is not an exact
Galilean assertion for the retained `M!=2m` action.

## 5. What is mapped to P, and the restoration test

The uniform winding current is divergence free and tangent to the
boundary. On the periodic product it is the harmonic current around the
noncontractible cycle. The density-defined longitudinal representative

\[
 \nabla\cdot P_L=m\delta q
\]

has `P_L=0` for the uniform background of *every* winding sector. Winding
therefore labels a global current degree of freedom in this map, not a
nonzero canonical local polarization density. A chosen inverse divergence
can add a solenoidal/harmonic representative, but the density identity
does not fix it or generate a local material energy for it.

In one longitudinal coordinate put `partial_s P_L=m delta q`. Eliminating
the periodic phase in (12), with the uniform integration current treated
separately, gives

\[
 \mathcal L_{P_L}={[(\partial_t+B\partial_s)P_L]^2\over2m^2D_h}
   -{A(\partial_sP_L)^2\over2m^2}
   +\partial_s\Phi_N P_L.                          \tag{16}
\]

Its static material energy after phase relaxation has coefficient
`(A-B^2/D_h)k^2/m^2` multiplying `|P_L|^2/2`. This is still a derivative
kernel. The required zero-background canonical material response instead
has `chi_can=k^2/(K+gamma k^2)`, from its local `K|P|^2/2` and retained
gradient term. Equations (13)–(16) provide neither that normalization nor
its momentum dependence, full saturating remainder, or admissible-domain
switch. Failure of the quadratic matching already prevents inferring the
whole canonical action. Restoring attractive self-gravity cannot create
the missing positive material term; in a local 3D Fourier patch it adds
`-K|P_L|^2/2`. The actual gravitational Green function of a finite torus
must instead be calculated in its geometry and is not assumed to be the
3D translation-invariant `-K/k^2` kernel along its circle.

For the parent's release-and-restoration experiment, an imposed smooth
source protocol that never creates amplitude zeros preserves ell. If the
same source and boundary are restored and the system returns to that
stationary sector, its susceptibility is (13), not a newly off branch.
A protocol causing a phase slip can leave a different ell, excitation
content or profile. Those changes can store history, but their ordinary
density response must still be computed with the same operator and source.
The stable uniform sectors of this calculation all obey (14); ell=0 is
not off either. An exact closed Hamiltonian protocol need not relax to any
stationary sector, so relaxation is expressly conditional here.

**Concrete discriminating check:** in an actual proposed annular solution
of (10), measure or calculate the same nonzero longitudinal probe modes
before release and after source restoration. Compare their absolute
static susceptibility to `k^2/(K+gamma k^2)` and their moving spectral
poles to (13); record density changes, residual flow and loss explicitly.
Use the `(ell,-ell)` pair as a current-memory control with equal static
susceptibility. A Doppler shift or a persistent circulation alone cannot
pass the constitutive on/off test. A different proposed extra operator
requires its own action-derived source and response matrix; total-density
response alone does not forbid its disappearance.

## 6. Finite phase-slip energy from the existing action

An energetic obstruction must be checked in the actual field space,
which includes zeros. The following explicit path keeps Q fixed without
any new coefficient. Take `ell>=1`, `k0=2pi/L`, let
`beta=g/Delta_p` be the initial stationary source-to-pair ratio, and set

\[
 u_t(s)=(1-t)e^{i\ell k_0s}+t e^{i(\ell-1)k_0s},
 \quad\psi_t=\sqrt{z_t}\,u_t,\quad b_t=-\beta\psi_t^2,
 \quad 0\le t\le1.                                \tag{17}
\]

Define `a=1-t`, `b_tilde=t`,
`d=a^2+b_tilde^2` and
`I4=a^4+4a^2 b_tilde^2+b_tilde^4`. The positive constant `z_t` is fixed
uniquely by

\[
 q=d z_t+2\beta^2 I_4 z_t^2,
 \qquad z_t={2q\over d+\sqrt{d^2+8\beta^2 I_4 q}}.    \tag{18}
\]

Thus Q is exactly constant along the path. At `t=1/2` both fields vanish
at one point of the circle (a transverse cut in this product control),
letting the winding change. The fields and all terms in (1) stay finite.
At both ends the phases have the required locked windings, and the
initial endpoint has the actual initial composition.

Orthogonality of the displayed Fourier harmonics gives the exact excess
energy density on this path:

\[
 h_t={z_t k_0^2\over2m}
       [\ell^2 a^2+(\ell-1)^2\widetilde b^2]
\]
\[
 \quad+{\beta^2 z_t^2 k_0^2\over2M}
 [4\ell^2a^4+4(2\ell-1)^2a^2\widetilde b^2
                  +4(\ell-1)^2\widetilde b^4]
\]
\[
 \quad+(\lambda-2g\beta+\delta\beta^2)z_t^2 I_4,
 \qquad\widetilde b=t.                              \tag{19}
\]

The last coefficient is
`lambda-g^2/delta+delta(beta-g/delta)^2>0`.
The final composition can be moved to the unique minimum in the
`ell-1` sector with nonincreasing energy, by (8). Consequently the
fixed-Q energetic min–max barrier satisfies the genuine finite bound

\[
 0\le\Delta E_{\rm bar}^{(Q)}
       \le V\left[\max_{0\le t\le1}h_t-h(q,p)\right]<\infty.
                                                               \tag{20}
\]

This is an explicit bounded one-variable expression using only the
existing parameters, the initial q, and selected geometry. It is not
claimed to be a minimal saddle. It can be loose and extensive because
the trial path deforms the entire ring. For negative ell use time reversal
and slip toward zero. No numerical parameter or large run is needed for
the finiteness result.

A local energetic scale can also be exposed in the zero-flow coherent
branch. At its actual chemical potential let
`Delta=delta-2mu>0`, `beta=g/Delta`,
`kappa=lambda-g^2/Delta>0`, `n0=mu/(2kappa)`, and
`w=1/sqrt(m mu)`. On a long waveguide the same-field trial notch

\[
 \psi=\sqrt{n_0}\tanh(s/w),\qquad b=-\beta\psi^2
\]

has, relative to the uniform state, the finite exact grand-energy cost
on this trial manifold

\[
 \Delta\Omega_{\rm notch}=\mathcal A\left[
 {4\over3}n_0\sqrt{\mu/m}
       +{8\beta^2 n_0^2\over15M w}\right].          \tag{21}
\]

To verify (21), substituting `b=-beta psi^2` into `H-mQ-mu Q`
gives `f'^2/(2m)+2 beta^2 f^2 f'^2/M+kappa(f^2-n0)^2`.
Use `int sech^4 x dx=4/3` and
`int tanh^2 x sech^4 x dx=4/15` on the real line. Both integrals follow
by `y=tanh x`. A large fixed-Q ring must compensate the finite notch
charge deficit elsewhere; the leading fixed-Q cost tends to (21), with
finite-size corrections. A complete ring phase-slip path also adjusts
the background phase twist. Equation (21) is a trial defect cost/scale,
not a separately proved optimal barrier or a substitute for (20).

Finally, (17) conserves Q but generally not Jz. An exactly isolated,
axisymmetric dynamics conserves both. Since neighboring uniform sectors
differ by `Delta Jz=Q`, a physical slip must put that angular momentum
in other field modes, a live host, or boundary flux. It must also dispose
of the energy released between (9)'s sectors. Without such a specified
state/receiver, (20) is not a dynamically accessible fixed-J barrier,
and it is not an irreversible rate. A stable Hamiltonian flow can persist
exactly in the ideal control, and a thermodynamic/quantum lifetime cannot
be assigned without its transition matrix element and actual receiver
state. No lifetime, Arrhenius temperature, bath spectrum or empirical
halo retention is fabricated here.

## 7. Audit status and open continuations

| Obligation | Result in the declared scope |
|---|---|
| Original action, locking, species/current bookkeeping | Passed; inherited formulas reconstructed, not counted as new |
| Explicit occupied winding state | Passed for selected periodic product geometry and branch (6); physical annulus/halo existence conditional |
| Fixed-Q sector energy and source-specific response | Passed analytically in (7)–(16), with hydrodynamic/stability range explicit |
| Canonical material kernel and on/off state from winding | Failed for this density/common-phase map; the extra operator remains unidentified |
| Infinite topological barrier in full original field space | Refuted in the fixed-Q ring comparison by the admissible path (17)–(20) |
| Accessible fixed-Q/fixed-J decay, formation and retention time | Not addressed without a physical host/receiver/state; energy barrier is not a rate |
| Global exclusion of other collective phases/operators | Out of scope |

All scientific claims here are analytic. Commands used: bounded `cat`/`sed`
reads and targeted `rg` searches of the named prior packets, `sol61_push`,
and September winding-clock records; SHA-256 input/output pin validation.
No scientific numerical experiment, production inspection, job control,
new field, fitted parameter, or prior/canonical/campaign/Git edit was used.
This derivation received self-review and mathematical proofreading; an
independent raw reconstruction is still required before a strong synthesis
claim relies on it. The proofread scope is this entire new file, with no
unresolved notation correction reported as a physical result.

Open continuations are preserved rather than declared exhausted:

1. Solve (10) with an actual live host or self-gravity and its finite stock;
   include transverse, centrifugal and density profiles. Resume with a
   supplied physical geometry/state, not an assumed astrophysical ring.
2. Compute that solution's full finite-mode source-calibrated response
   before/after release and restoration. A finite geometry can modify
   modes; it must still meet the absolute canonical kernel and operator
   residue, not merely have a gap or a current label.
3. At fixed Q and total J, solve the minimum saddle with actual existing
   receiver excitations and then its Hamiltonian transition dynamics.
   The explicit finite path and local scale here can bound/control that
   calculation but do not supply its state or rate.
4. A genuinely different many-body/topological operator remains open if
   its source and action can be derived from the original fields. It must
   explain how additional response vanishes while ordinary mass response
   persists. Merely assigning ell to a tethered population does not do so.

The strongest safe result is therefore a **response-versus-history
separation in an executed original-field collective state**: protected
circulation within the nonvanishing chart can retain a memory while the
calculated longitudinal constitutive response stays continuously on.
