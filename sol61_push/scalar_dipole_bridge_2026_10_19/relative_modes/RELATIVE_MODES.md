# A physical subsystem slosh, live recoil, and the intermediate wavelength window

Owner: `self_gravity_dipoles`. Base mathematical checkpoint:
`CE-GRAV-2026-10-19 / CE087`; observed initial Git HEAD:
`f4424595259bd1ae40addb890e338f85c4f48eb1`. The concurrent navigation checkpoint
is CE088 in the transport lane and is not this derivation's mathematical parent.
Write scope is this `relative_modes/` directory. This note changes no original
action, manuscript, queue, publication, or shared status. Byte pins and the small
computation are recorded beside it.

**Result.** Original minimally coupled scalar matter has a genuine collective
displacement relative to an ordinary baryonic gravitational well. In a prescribed
harmonic core its Kohn mode has `omega_b^2=4 pi G rho_b/3` and uniform-field
subsystem susceptibility `rho_d/omega_b^2`. This produces a natural factor `1/G`,
but its dimensionless coefficient is `3 rho_d/rho_b`, and the fixed core is an
external anchor. A heavy freely falling baryonic host is not such an anchor.

With live recoil the relative mode remains physical, but its complete linear
mass source is compensated. For centered spherical profiles it is
`delta rho_k=-i mu (k.s)[F_d(k)-F_b(k)]`, of order `k^3`, and a common uniform
field gives no relative drive. Equal normalized profiles cancel at every `k`
at this linear order. Unequal, widely separated profile sizes nevertheless
admit an intermediate band with `F_d-F_b approximately 1`, so a real finite-band
dipole response is possible. Its normalization, occupied hosts, locality,
stability and nonlinear law remain state dependent; none is fixed by the
original action here. The gravitational spring softens for the explicit finite
profiles and does not produce the required rational saturation.

## 1. Target contract and the original action

Natural units are used unless `hbar,c` are restored. Let `U` be Newtonian
potential, `g=-grad U`, and `K_G=4 pi G`. The original minimally coupled action is

\[
 S=\int\sqrt{-g}\,[M_{\rm Pl}^2R/2+|\partial\Phi|^2+|\partial X|^2-V]+S_b,
\]
\[
 V=m^2|\Phi|^2+M^2|X|^2+g_s(X^*\Phi^2+X\Phi^{*2})
   +\lambda_{\rm tot}|\Phi|^4,
\quad M>2m,\quad
 \lambda_{\rm tot}=\lambda_{\rm rep}+{g_s^2\over M^2-4m^2},
\quad\lambda_{\rm rep}>0.                                      \tag{1}
\]

`S_b` supplies actual ordinary baryons, coupled solely by ordinary gravity.
They are an allowed environment, not a newly introduced scalar interaction.
The dilute single-sign, one-component GP reduction used below requires an
actually prepared carrier state, negligible unresolved source occupation,
slow motion, and excitation/contact energies well below the eliminated
source detuning `M-2m` as well as the rest scales. The fully matched coefficient
from the parent is

\[
 g_2={\lambda_{\rm rep}\over2m^2}>0,\qquad n=|\psi|^2,\quad\rho_d=mn.
                                                               \tag{2}
\]

This is not a claim that a stable neutral coherent branch, host inventory,
or the necessary scale hierarchy follows from (1). Keeping populated `X`
would require its additional dynamical fields and full stress source.

The necessary target is a physical source-conjugate polarization with

\[
 W(\Pi)={-aK_G\Pi-a^2\log(1-K_G\Pi/a)\over K_G},\quad
 {\partial W\over\partial\Pi}={aK_G\Pi\over a-K_G\Pi},\quad
 \chi_\Pi(0)=1/K_G.                                             \tag{3}
\]

Here `Pi=|boldsymbol Pi|` and the source convention is `H_src=-int g.Pi`.
Deriving a subsystem oscillator is a useful bridge, not achievement of (3).
Success at the full target would also require a local occupied mode ensemble,
the complete gravitational source, the rational nonlinear response and the
normalization without a fitted inventory/profile ratio.

## 2. The physical density operator and its sign

For a material displacement `xi_a(x)` about a nonzero reference density,
mass conservation gives

\[
 \rho_a=\rho_{a0}+\delta\rho_a,\qquad
 \delta\rho_a=-\nabla\cdot(\rho_{a0}\xi_a),\qquad
 \boldsymbol\Pi_a=\rho_{a0}\xi_a.                               \tag{4}
\]

Consequently, with boundary terms absent,

\[
 \delta H_U=\int U\delta\rho=-\int\mathbf g\cdot\boldsymbol\Pi.
                                                               \tag{5}
\]

The alternative density/divergence convention requested in the task is
`P=-rho_0 xi=-Pi`: then `delta rho=div P` and `delta H_U=+int g.P`.
These signs must not be mixed. The susceptibility magnitudes below are positive
in the `Pi` convention. Neither convention identifies the *total positive*
material density with a divergence. The reference density, source energy and
boundary terms remain present.

At Newtonian order the Poisson source is the sum `rho_b+mn`. In the full
canonical theory the lapse source is the complete Hamiltonian density,
including the conversion, gradient and quartic energy; see the pinned
`INTERNAL_POLARIZATION.md`, equations (9a)–(9b). At post-Newtonian order the
metric/stress and gravitational-field contributions must be matched as well.
No omitted interaction energy is assigned a separate negative mass here.

## 3. Exact prescribed-core GP mode

The leading reduction of (1) is

\[
 i\partial_t\psi=\left[-{\nabla^2\over2m}+g_2|\psi|^2+m(U_b+U_d+U_e)\right]\psi,
 \qquad\nabla^2U_d=4\pi Gm|\psi|^2.                             \tag{6}
\]

All carrier self terms, including its Newtonian self-gravity, are translation
invariant. Suppose that the **prescribed** baryonic potential is harmonic
throughout the carrier's support,

\[
 U_b=U_{b0}+\tfrac12\omega_b^2x^2,\qquad
 \omega_b^2={4\pi G\rho_b\over3},\qquad U_e=-\mathbf g_e(t)\cdot x.
                                                               \tag{7}
\]

For a stationary solution `exp(-i mu_c t) psi_0(x)`, direct substitution gives

\[
 \psi(x,t)=e^{im\dot q\cdot x+i\beta(t)-i\mu_ct}\psi_0(x-q),\quad
 U_d(x,t)=U_{d0}(x-q),
\]
\[
 \ddot q+\omega_b^2q=\mathbf g_e(t),\qquad
 \dot\beta={m\over2}(\omega_b^2q^2-\dot q^2).                    \tag{8}
\]

The `grad psi_0` terms and self-potential translate together; the residual
coefficient of `x` is exactly the first equation in (8). This independently
derives the Kohn mode with no assumed internal dipoles. Interactions and
carrier self-gravity change `psi_0`, but not this mode frequency.

For `M_d=int rho_d`, its action and retarded COM response are

\[
 L_q={M_d\over2}(\dot q^2-\omega_b^2q^2)+M_d\mathbf g_e\cdot q,
 \qquad q(\omega)={\mathbf g_e(\omega)\over\omega_b^2-(\omega+i0)^2}.
                                                               \tag{9}
\]

Under a uniform source, `Pi_d(x)=rho_d(x)q`; hence at zero frequency

\[
 \chi_{\Pi_d}(x)={\rho_d(x)\over\omega_b^2}
 ={1\over4\pi G}{3\rho_d(x)\over\rho_b}.                       \tag{10}
\]

For an averaged cell replace `rho_d(x)` by `M_d/V_cell`. The factor `1/G`
is real: gravity supplies the spring. Equality to (3) needs the additional
state relation `3 rho_d/rho_b=1`. The action does not impose that ratio, and
an anisotropic core gives a susceptibility tensor rather than (10).

A single COM mode is spatially nonlocal: its dipole response kernel to a
general acceleration field is

\[
 \chi_{ij}(x,y;\omega)=
 {\rho_d(x)\rho_d(y)\delta_{ij}\over
 M_d[\omega_b^2-(\omega+i0)^2]}.                               \tag{11}
\]

Equation (10) under a uniform probe does not turn (11) into a local material
energy density for independent displacements at every point. Other GP modes
and host-to-host couplings are needed for such a claim.

An isolated finite uniform baryon sphere is harmonic only in its interior.
A GP bound state has tails; thus exact (8) for a physical finite core is an
approximation controlled by departure from harmonicity over the occupied
profile, not an exact compact-support GP solution. Globally harmonic fixed
potentials are a mathematical idealization.

## 4. What fixes the core, and what the live problem changes

If the core center is `q_b(t)`, let `xi=q_d-q_b`. Its prescribed-center equation is

\[
 \ddot\xi+\omega_b^2\xi=\mathbf g_e-\ddot q_b.                  \tag{12}
\]

A freely falling core has `ddot q_b=g_e` at zeroth recoil order, removing the
drive. `M_b >> M_d` suppresses the recoil caused by the carrier, but does not
suppress ordinary gravitational acceleration `F_b/M_b=g_e`. Sending the host
mass to infinity is therefore not, by itself, a physical fixed-gravity anchor.
Holding `q_b=0` while applying a common gravitational field requires external
support/prescribed source motion. The fixed source absorbs momentum; its
holding force/work is not part of an isolated scalar–baryon system. An ideal
support can do zero work while exactly stationary but still supplies the
nonzero force and momentum transfer.

For two live fixed-mass subsystems with displacements `q_d,q_b`, set

\[
 M_T=M_d+M_b,\quad\mu={M_dM_b\over M_T},\quad
 C={M_dq_d+M_bq_b\over M_T},\quad s=q_d-q_b.
\]
\[
 q_d=C+{M_b\over M_T}s,\qquad q_b=C-{M_d\over M_T}s,
 \qquad T={M_T\over2}\dot C^2+{\mu\over2}\dot s^2.              \tag{13}
\]

Here `mu` is the reduced inertial mass, not the condensate chemical potential.
If their quadratic mutual energy is `kappa s^2/2`,

\[
 M_T\ddot C=M_d\bar g_d+M_b\bar g_b,\qquad
 \ddot s+{\kappa\over\mu}s=\bar g_d-\bar g_b.                   \tag{14}
\]

A common uniform acceleration has `bar g_d=bar g_b` and no relative drive,
while `omega_rel^2=kappa/mu` remains an occupied-state oscillation frequency.
This distinguishes a genuine degree of freedom from a gravitationally
driven dipole. All baryonic response density must accompany the carrier density.

## 5. Exact gravitational curvature for spherical profiles

Write `rho_a=M_a f_a`, with `int f_a=1`, centered spherical `f_a`, and profiles
held fixed while their centers move. Their mutual gravitational energy is

\[
 E_{db}(s)=-G\iint{\rho_d(x)\rho_b(y)\over|x-y+s|}\,d^3x\,d^3y.
\]

The exact Hessian of this restricted energy manifold at coincidence is

\[
 \kappa_{ij}=\int\rho_d\partial_i\partial_jU_b\,d^3x
 =\delta_{ij}{4\pi G\over3}\int\rho_d\rho_b\,d^3x,
\]
\[
 I_{db}=\int f_df_b\,d^3x,\qquad
 \kappa={4\pi G\over3}M_dM_bI_{db},\qquad
 \boxed{\omega_{\rm rel}^2={4\pi G\over3}M_TI_{db}.}            \tag{15}
\]

Rotational invariance fixes the tensor to one third its trace; Poisson's
equation fixes the trace and sign. This is more general than replacing both
objects by point masses at an arbitrarily chosen separation. For equal
normalized shapes `I_db=int f^2`, not generally `1/V`.

For coextensive uniform spheres of common radius `R`,

\[
 f=1/V_R\ (r<R),\quad \kappa={GM_dM_b\over R^3},\quad
 \omega_{\rm rel}^2={G(M_d+M_b)\over R^3}
 ={4\pi G\over3}(\rho_d+\rho_b).                              \tag{16}
\]

Their entire mutual energy for `0<=s<=2R` is

\[
 E_{db}(s)=-{GM_dM_b\over R}
 \left[{6\over5}-{s^2\over2R^2}+{3s^3\over16R^3}-{s^5\over160R^5}\right],
\]
\[
 E'_{db}(s)=\kappa s
 \left[1-{9s\over16R}+{s^3\over32R^3}\right].                  \tag{17}
\]

Derivation: the profile convolution has overlap
`C(s)=(M_d M_b/V_R)[1-3s/(4R)+s^3/(16R^3)]`; its potential obeys
`E''+2E'/s=4 pi G C(s)`. Integrating regularly at zero and matching to
`-G M_d M_b/s` at `s=2R` gives (17). The `s^3=|boldsymbol s|^3` term is
allowed by the sharp edges. For arbitrary radii of concentric uniform spheres,
`I_db=1/V_larger`, so `kappa=G M_d M_b/R_larger^3`.

Equations (15)–(17) are exact energy and reduced-inertia statements for rigid
profiles. They are not a proof that both profiles remain rigid normal modes
of live GP–baryon dynamics. In general baryon and carrier shape modes couple,
and eliminating them gives a frequency-dependent effective restoring kernel.
Uniform top hats are not exact finite-kinetic-energy stationary GP profiles.
The fixed globally harmonic Kohn solution (8) has the stronger exact dynamical
status within the GP reduction. No stable live equilibrium is fabricated here.

## 6. Complete finite wavelength mass source

Use `rho_k=int e^{-ik.x}rho(x) dx` and form factors
`F_a(k)=int e^{-ik.x}f_a(x) dx`. Linear translation yields

\[
 \delta\rho_k=-i(k\cdot C)[M_dF_d+M_bF_b]
              -i\mu(k\cdot s)[F_d-F_b].                       \tag{18}
\]

For the relative coordinate alone, the real-space source-conjugate dipole is

\[
 \boldsymbol\Pi_{\rm rel}(x)=\mu[f_d(x)-f_b(x)]s,
 \quad\int\boldsymbol\Pi_{\rm rel}=0,\qquad
 H_{e,\rm rel}=-\mu s\cdot\int(f_d-f_b)\mathbf g_e\,d^3x.
                                                               \tag{19}
\]

Thus `rho_d q_d` is a physical subsystem displacement operator, but is not
the complete gravitational source. If `f_d=f_b`, equations (18)–(19) vanish
pointwise to first order, for **all** wavelengths. At second order the total
coextensive profile changes by `(mu/2)s_i s_j partial_i partial_j f`; the
absence of the linear source does not set all nonlinear observables to zero.

This also explains why a gravitational gap can coexist with zero linear
mass source. The Newtonian energy is `E_g=-G int rho(x)rho(y)/(2|x-y|)`.
Its quadratic variation along a finite displacement includes both the
quadratic form in `delta rho^(1)` and `int U_0 delta rho^(2)`. For equal
profiles the first term vanishes, while the second is
`(mu/2)s_i s_j int f partial_i partial_j U_0=kappa s^2/2`, reproducing (15).
Discarding the reference density or the second-order source would lose the
spring. Conversely, this `kappa` is already gravitational energy after
eliminating Poisson's field: if that field and the complete displaced source
are retained explicitly, inserting it again as a new independent material
potential double counts the interaction. A local `W` in (3) requires a
consistent background/mode elimination, not just this numerical coefficient.

For centered isotropic finite-second-moment profiles,

\[
 F_a=1-{k^2\langle r^2\rangle_a\over6}+o(k^2),\qquad
 \delta\rho_{k,\rm rel}={i\mu\over6}(k\cdot s)k^2
 [\langle r^2\rangle_d-\langle r^2\rangle_b]+o(k^3).             \tag{20}
\]

The subsystem source is `O(k)`, the full relative source `O(k^3)`. This is a
third spatial moment statement, not necessarily a pure spherical octupole.
For centered anisotropic profiles the second-moment tensor gives the same
generic `O(k^3)` power. Different nonzero intrinsic centers require redefining
the reference coordinate and are not the centered profile case here.

For a plane-wave external potential, `bar g_d-bar g_b=(F_d-F_b)g_e`.
The relative self-response, with convention `delta rho=-chi_rhorho U`, is

\[
 \chi_{\rho\rho}^{\rm rel}(\omega,k)=
 {\mu k^2|F_d-F_b|^2\over\omega_{\rm rel}^2-(\omega+i0)^2}.
                                                               \tag{21}
\]

For an independently responding translationally averaged ensemble of host
number density `nu_h`, divide the extensive response by volume, or multiply
(21) by `nu_h`. Its effective longitudinal polarization susceptibility is

\[
 \alpha_{\rm rel}(\omega,k)=
 {\nu_h\mu|F_d-F_b|^2\over\omega_{\rm rel}^2-(\omega+i0)^2},
 \qquad\alpha_{\rm rel}(0,k)=O(k^4),\quad\chi_{\rho\rho}=O(k^6).
                                                               \tag{22}
\]

The free total COM also responds. Its pole is at zero frequency, with density
numerator `k^2 |M_dF_d+M_bF_b|^2/M_T`; it has no static equilibrium under an
affine force. It is excluded from (21), not silently discarded from the
physical system. A static whole-system calculation needs boundaries, an
equilibrium background or gravitational constraints in addition to this mode.

### A stronger source restriction for spherical profiles

If `U_e` is harmonic throughout both spherical supports, its spherical
mean-value property gives `int f_a grad U_e=grad U_e(0)` for either normalized
profile. Hence `bar g_d=bar g_b` even for unequal radii. Remote masses with
no source density in the supports cannot excite this relative translation
linearly. Equivalently, outside both shifted spherical supports each component
has its point-mass potential; their first-order exterior dipoles cancel by
`M_d q_d+M_b q_b=0`.

The finite `k` response in (21) is therefore an overlapping-source response:
a plane-wave Newtonian potential has `laplacian U_e=-k^2 U_e`, and its test
source density penetrates the profiles. This is physically allowed for
interpenetrating baryon/carrier media. For a self-consistent live baryon
perturbation its source dynamics must be solved, rather than treating that
same dynamical density simultaneously as an independent external probe.
Gaussians below have noncompact tails; the vacuum-harmonic statement applies
exactly to compact supports, or approximately when tail errors are controlled.

## 7. A real intermediate window despite the infrared cancellation

Take smooth Gaussian reference profiles

\[
 f_a=(2\pi\sigma_a^2)^{-3/2}e^{-r^2/(2\sigma_a^2)},\quad
 F_a=e^{-k^2\sigma_a^2/2},\quad
 I_{db}=[2\pi(\sigma_d^2+\sigma_b^2)]^{-3/2}.                    \tag{23}
\]

When `sigma_b >> sigma_d`,

\[
 {1\over\sigma_b}\ll k\ll {1\over\sigma_d}
 \quad\Longrightarrow\quad F_d-F_b\simeq1,
 \quad\alpha_{\rm rel}(0,k)\simeq{\nu_h\mu\over\omega_{\rm rel}^2}.
                                                               \tag{24}
\]

The compact carrier is resolved as a subsystem while the diffuse compensating
recoil is spatially averaged out. In the declared quadratic profile projection,
this disproves the inference that global COM cancellation by itself forbids
every finite-band approximately local dipole response. It does not construct
that projection as a stable phase of (1), or contradict (20)–(22).

For a sufficient error bound choose `0<epsilon<1`. If

\[
 k\sigma_d\le\sqrt\epsilon,\qquad
 k\sigma_b\ge\sqrt{2\log(2/\epsilon)},
\]

then `1-e^{-k^2 sigma_d^2/2}<=epsilon/2` and
`e^{-k^2 sigma_b^2/2}<=epsilon/2`, giving
`(F_d-F_b)^2>=(1-epsilon)^2`. A nonempty band follows from
`sigma_b/sigma_d >= sqrt[2 log(2/epsilon)/epsilon]`; a broad band requires
correspondingly greater size separation.

The bounded calculation uses the exact form factors, not this conservative
bound. For size ratio 3 the maximum `(F_d-F_b)^2` is `0.456178`; for ratio
10 it is `0.893031`. For ratio 30 the response is within 10 percent of the
unit form-factor plateau on `0.0821605<=k sigma_d<=0.324593`, a wavenumber
factor `3.95072`. For ratio 100 it is so on
`0.0243949<=k sigma_d<=0.324593`, a factor `13.3058`.
These examples check the mechanism and its scale cost; they are not actual
scalar–baryon equilibrium profiles.

The plateau amplitude is

\[
 \boxed{4\pi G\alpha_{\rm plateau}
 ={3\nu_h\mu\over M_TI_{db}}
 ={3\nu_h\over I_{db}}{M_dM_b\over(M_d+M_b)^2}.}                \tag{25}
\]

It retains the baryonic/carrier inventory, overlap volume, and host packing.
For a compact carrier in a diffuse smooth baryon core,
`M_b I_db approximately rho_b(0)` and `M_b>>M_d` reduces (25) to
`3 nu_h M_d/rho_b(0)`. This explains the same natural `1/G` scale as (10),
but does not set its dimensionless multiplier to one. Gravitational force
coupling and spring both originate in `G`; the remaining ratio is state data.

An effective local medium further needs many hosts per probe wavelength,
no double counting of diffuse baryon mass, a controlled host interaction
kernel, and stable internal shape modes. A single diffuse baryonic component
shared by many compact carrier lumps is not a collection of independent
copies of (13). Equation (25) cannot be used to select `nu_h` at will in that
situation. These are material-state construction obligations left open by
the profile calculation.

## 8. Gaps, occupancies and nonlinear response

Quantizing the fixed-core COM oscillator gives gap `hbar omega_b` and
`|<1|D_d|0>|^2=M_d hbar/(2 omega_b)` per direction for `D_d=M_d q`.
For the relative mode the finite-wavelength gravitational dipole is
`D_rel(k)=mu [F_d-F_b] s`, giving

\[
 |\langle1|D_{\rm rel}(k)|0\rangle|^2
 ={\mu\hbar|F_d-F_b|^2\over2\omega_{\rm rel}},\qquad
 {2|D_{10}|^2\over\hbar\omega_{\rm rel}}
 ={\mu|F_d-F_b|^2\over\omega_{\rm rel}^2}.                      \tag{26}
\]

The gravitational restoring frequency is therefore an actual gap of the
specified collective oscillator, not an arbitrarily assigned two-level gap.
One harmonic host supplies a discrete triplet of oscillator ladders. A
population of hosts supplies the occupied spectral measure only after its
core-density, profile, mass and abundance distribution is known. The action
does not specify that distribution here. The harmonic oscillator retarded
commutator response is independent of its thermal excitation occupation;
the host/carrier inventory still controls the oscillator strength.

Crucially a harmonic oscillator does not saturate to a finite dipole. Its
displacement grows linearly under a static supported drive. Neither its gap
nor its occupation may be identified with the independently saturating
two-level continuum of the pinned rational-completion note. That note's
`w(Delta)=p_sat a Delta/(a^2+Delta^2)^(3/2)` is not derived by (26).

Finite gravitational wells do not fix this failure by themselves. For the
Gaussian profiles, with `S^2=sigma_d^2+sigma_b^2`,

\[
 E_{db}(s)=-{GM_dM_b\over s}\operatorname{erf}{s\over\sqrt2S},
 \quad E_{db}(0)=-{GM_dM_b\over S}\sqrt{2\over\pi},
\]
\[
 E_{db}(s)-E_{db}(0)=\tfrac12\kappa s^2
 \left[1-{3s^2\over20S^2}+O(s^4/S^4)\right],
 \quad E'_{db}(s)=\kappa s
 \left[1-{3s^2\over10S^2}+O(s^4/S^4)\right].                  \tag{27}
\]

The spring softens, as it also does in (17), while the target (3) hardens and
has a divergent inverse force near a finite polarization. At large separation
the binding energy tends to zero and restoring force to `G M_d M_b/s^2`;
a constant relative force tilts the energy without bound and permits escape,
not a globally stable saturating polarization. Local metastable equilibria
may exist below the maximum restoring force. The original repulsive contact
affects profiles and deformation, and other stable collective structures
remain possible; no theorem excluding every nonlinear state of (1) is claimed.

## 9. Verification, source check and continuation

`check_relative_modes.py` has an explicit contract in `contract.json`. It
checks the uniform-sphere overlap Poisson polynomial and exterior energy/force
matching in exact rational arithmetic; four reduced-inertia/COM mass pairs;
the compensated Gaussian `k^3` source in five infrared examples; exact
form-factor cancellation for equal Gaussian profiles; the six quoted size
ratios; and Gaussian curvature by an independent central finite difference.
There is no dynamical simulation, fitting or parameter scan. The bounded
runner completed, all assertions passed, and the v2 manifest validated against
current code bytes. Its limitations are the floating tolerances in the
Gaussian examples and the unconstructed physical state, not the exact
conditional identities derived above.

Primary source checked on 19 October 2026: Z. Wu and E. Zaremba,
*Dynamics of harmonically-confined systems: some rigorous results*,
[arXiv:1310.7934v2](https://arxiv.org/pdf/1310.7934v2), header dated
31 October 2013. Equations (1)–(9) separate the COM of equal-mass particles
with translation-invariant pair interactions in a harmonic trap. Equations
(13)–(16) give oscillator excitation ladders and a homogeneous-force drive.
Dictionary: their total mass `M` is our `M_d`, their force per particle is
`m g_e`, and their trap frequencies are our `omega_b`. Authentication,
extraction and this limited application were checked in the exact v2 PDF;
no PDF was retained, so no retained-PDF hash is claimed. The GP substitution,
live gravity Hessian, compensated source and finite-band construction were
derived here. The source does not establish an equilibrium of (1), a live
baryon eigenmode, or normalization (3).

Current evidence label: **conditional analytic bridge with bounded finite
checks; independent proof review pending**. The isolated internal-dipole
obstruction survives in the uniform infrared channel, but does not exhaust
the finite-wavelength, overlapping-source subsystem route.

The next decisive work is to construct a stable original-action carrier plus
live baryon background with compact/diffuse scale separation, derive its full
Bogoliubov/Euler–Poisson response including shape modes, and determine whether
a host continuum and its occupied spectrum emerge without an independently
chosen cell inventory. That is a deferred continuation, not an assertion of
success. A narrow first check is a self-consistent spherical equilibrium and
its `l=1` fluctuation operator, testing whether a relative oscillator pole
retains the form-factor plateau after baryonic deformation. A nonlinear route
must address the explicit gravitational softening before it can approach (3).
