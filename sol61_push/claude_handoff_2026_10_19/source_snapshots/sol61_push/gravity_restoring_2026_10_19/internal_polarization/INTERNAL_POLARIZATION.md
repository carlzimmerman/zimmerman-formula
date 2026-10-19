# Physical internal polarization of the original scalar carrier

Parent: CE-PARTICLE-2026-10-18 / CE085, initial and observed starting HEAD
`9516ee01c79f35c04b7556050669ba77b0c98b99`. This lane writes only
`sol61_push/gravity_restoring_2026_10_19/internal_polarization/`; it does not
change the transport lane, source action, manuscript, queues, or live runs.
Input byte pins are in `source_pins.json`. This is a bounded analytic route,
not a claim that every collective phase of the action has been classified.

**Result.** An isolated bound object assembled from positive constituents
with the original universal minimal gravitational coupling has no physical
internal mass dipole driven by a uniform Newtonian field. This is an exact
separation theorem for the declared Newtonian particle model. For the full
scalar action the corresponding local weak-field statement follows from
conservation of the complete stress tensor and removal of an affine metric
perturbation by a coordinate change. Its leading physical finite-size
response is tidal. This obstructs applying an acceleration-driven internal
dipole ensemble to these objects without an additional bridge. It does not
exclude density/compressibility response, tidal response, externally supported
matter, nonminimal theories, or all possible collective phases.

There is also a useful action-specific result: the positive-square potential
excludes ordinary smooth finite-energy, single-common-frequency Q-balls in
flat space on the localized branch. It therefore supplies no intrinsic
nongravitating droplet anchor of that usual type. Self-gravitating objects and
other backgrounds are outside that exclusion.

## 1. Target and microscopic contract

Use natural units except where `c` is displayed, signature `+---`, Newtonian
potential `U`, acceleration `g_vec=-grad U`, and `K=4 pi G`. The original
complex carrier `Phi` has charge one and mass `m`; the complex source `X` has
charge two and mass `M>2m`. Let

\[
 \Delta=M^2-4m^2>0,\qquad
 \lambda_{\rm tot}=\lambda_{\rm rep}+g_s^2/\Delta,
 \qquad \lambda_{\rm rep}>0.
\]

The canonical action is minimally coupled to the metric and has potential

\[
 V=m^2|\Phi|^2+M^2|X|^2
  +g_s(X^*\Phi^2+X\Phi^{*2})+\lambda_{\rm tot}|\Phi|^4.
 \tag{1}
\]

The requested effective material energy, for a **physical** mass dipole
density `P` and `u=K|P|<a0`, is

\[
 W_{\rm full}(P)=
 { -a_0u-a_0^2\log(1-u/a_0)\over K}.
 \tag{2}
\]

A necessary bridge is a real coupling `-P dot g_vec` for an independent
internal degree of freedom of the carrier medium. A conserved-current dual
potential is not being used here: the earlier gauge obstruction is logically
separate. The present test asks whether actual source/daughter composites,
droplets or bound objects provide that physical degree of freedom.

## 2. Exact Newtonian COM/internal separation

Consider `N` constituents of fixed masses `m_a>0`, with a translation-invariant
internal potential `V_int({x_a-x_b})`. Include any internal Newtonian
self-gravity in `V_int`. Assume inertial and passive gravitational masses
are the same `m_a`, no external support or imposed trap, and an external
potential exactly affine across the object,

\[
 U_{\rm ext}(x,t)=U_0(t)+A(t)\cdot x.
\]

Define

\[
 M_T=\sum_a m_a,\quad
 R={\sum_a m_ax_a\over M_T},\quad
 y_a=x_a-R,\quad \sum_a m_ay_a=0.
\]

Direct substitution into the particle Lagrangian gives

\[
 L={M_T\over2}\dot R^2-M_T[U_0+A\cdot R]
   +\sum_a{m_a\over2}\dot y_a^2-V_{\rm int}(\{y_a-y_b\}).
 \tag{3}
\]

Both kinetic and gravitational cross terms vanish by the **same mass
weighting**. Therefore

\[
 \ddot R=-A,\qquad
 \text{all constrained internal equations are independent of }A.
 \tag{4}
\]

The actual internal mass dipole about this inertial COM is identically
`D=sum m_a y_a=0`. A displacement of the whole positive-mass object has a
dipole about a fixed laboratory origin, but that displacement is its COM
coordinate, not an internal polarizable oscillator. Equation (3) is valid
for any strength and shape of the declared translation-invariant internal
potential; positive masses alone do not establish existence of its bound
states. The theorem is at Newtonian fixed-mass order, not an exact global GR
statement.

### A charge center can hide the cancellation

For two constituents of inertial masses `m1,m2>0`, positive reference
weights `q1,q2`, relative coordinate `r=x1-x2`, and reference center
`R_q=(q1 x1+q2 x2)/Q`, where `Q=q1+q2`, put

\[
 M_T=m_1+m_2,\quad
 \delta_q={m_1q_2-m_2q_1\over Q},\quad
 A_q={m_1q_2^2+m_2q_1^2\over Q^2},\quad
 \mu={m_1m_2\over M_T}.
\]

Then `R=R_q+(delta_q/M_T)r`, and the apparent mass dipole about `R_q` is
`D_q=delta_q r`. The full Lagrangian is

\[
 L={M_T\over2}\dot R_q^2+\delta_q\dot R_q\cdot\dot r
       +{A_q\over2}\dot r^2-V_{\rm int}(r)
       -M_T A\cdot R_q-\delta_q A\cdot r-M_TU_0.
 \tag{5}
\]

Its two equations are

\[
 M_T\ddot R_q+\delta_q\ddot r=-M_TA,\qquad
 \delta_q\ddot R_q+A_q\ddot r=-\nabla_rV_{\rm int}-\delta_q A.
\]

The exact Schur identity

\[
 M_T A_q-\delta_q^2=m_1m_2,\qquad
 A_q-\delta_q^2/M_T=\mu
 \tag{6}
\]

eliminates the field completely:

\[
 \boxed{\mu\ddot r=-\nabla_rV_{\rm int}.}
 \tag{7}
\]

Thus unequal source/daughter mass per conserved charge does not evade the
theorem. Dropping the mixed kinetic term while retaining `-D_q dot A` makes
a false internal force. Conversely, actually imposing `R_q=constant`
requires external constraint forces and changes the physical system.

For a hypothetical separated source and a two-daughter subsystem,
`m1=M,q1=2,m2=2m,q2=2` gives `delta_q=(M-2m)/2`. This nonzero detuning
coefficient still cancels in (7). This is an illustrative coordinate check,
not a claim that such a bound two-subsystem object exists in (1), or that
the conversion reaction has fixed particle masses through its event.

## 3. Complete stress tensor, conversion and binding energy

The particle argument cannot be extended to conversion by summing only
species rest masses. An `X -> Phi Phi` event changes that partial rest
inventory by `2m-M`; kinetic, interaction and field energy carry the
remainder. The conserved charge center, a species number center, a rest-mass
center and the total energy center are different definitions.

For canonical fields in flat space, include the conversion interaction and
the complete source field in the symmetric stress tensor. On the equations
of motion,

\[
 \partial_\mu T^{\mu\nu}=0,\qquad
 E=\int T^{00}d^3x,\qquad
 R_E^i={1\over E}\int x^iT^{00}d^3x.
 \tag{8}
\]

Boundary fluxes must vanish for this isolated-object expression. The
first energy moment then obeys `d(E R_E^i)/dt=integral T^{i0}`; with symmetric
`T`, conserved momentum makes the energy center inertial in flat space.
About that center,

\[
 D_E^i={1\over c^2}\int(x^i-R_E^i)T^{00}d^3x=0.
 \tag{9}
\]

This includes negative binding contributions without assigning them an
independently chosen negative gravitational charge. A local total energy
density need not be assumed pointwise positive for (8)-(9); nonzero finite
total `E` and finite moments suffice. In the present isolated classical
nongravitating theory the positive-square bound below guarantees `E>=0`.

One can check the more invariant weak-field implication without equating
gravity to only a `T00` rest-mass density. At linear order the metric
coupling is proportional to `integral h_munu T^munu`. For a pure coordinate
perturbation `h_munu=partial_mu xi_nu+partial_nu xi_mu`, integration by
parts gives only a boundary term because the **complete** `T` in (8) is
conserved. Every exactly affine static metric perturbation has vanishing
linearized Riemann tensor and is locally of this form on a simply connected
patch. For the lapse-only perturbation
`h00=2 A_i x^i/c²`, an explicit choice, with `x0=ct`, is

\[
 \xi_0={(A\cdot x)x^0\over c^2},\qquad
 \xi_i=-{A_i(x^0)^2\over2c^2};
\]

it gives `h0i=hij=0`. This explicit formula assumes constant `A`; the
Newtonian separation (3) also permits time dependent `A(t)`. This local
coordinate argument covers the conversion energy and source stress that
are absent from a rest-stock calculation. It says that an isolated local
object has no invariant response to this affine weak gravitational field
after transforming the complete object to free fall. It does **not** say
that coordinate clock rates, supported laboratory systems, or spatially
varying fields have no response. Terms of order curvature and nonlinear
weak-field corrections have deliberately not been removed by this argument.

For weak self-gravity, the Newtonian proof already includes the object's
self-potential in `V_int`. At post-Newtonian orders its field energy must
also enter the matched total momentum/COM description. Matter `T00` alone
is not asserted to give a gauge-independent local gravitational energy
density, and no strong-self-gravity theorem is proved here.

### A coherent two-level projection is not an independent gravity charge

The canonical lapse calculation makes the source matrix element explicit.
With prescribed `ds²=N(x)²dt²-dx²` and zero shift, the action of (1) is

\[
 L=\int\left[{|\dot\Phi|^2+|\dot X|^2\over N}
       -N\bigl(|\nabla\Phi|^2+|\nabla X|^2+V\bigr)\right]d^3x.
 \tag{9a}
\]

At fixed canonical momenta `pi_Phi=dot Phi*/N` and `pi_X=dot X*/N`, its
Hamiltonian is exactly

\[
 H_N=\int N(x){\cal H}_0(x)d^3x,\quad
 {\cal H}_0=|\pi_\Phi|^2+|\pi_X|^2
            +|\nabla\Phi|^2+|\nabla X|^2+V.
 \tag{9b}
\]

Thus the first lapse source is the complete canonical energy density,
including the cubic conversion operator. For an affine lapse its linear
moment is the total energy moment, rather than the moment of the diagonal
species rest inventory. A full gravitational metric also perturbs the
spatial metric; its additional stress terms are covered by the coordinate
argument above. Equations (9a)-(9b) are a diagnostic lapse probe, not the
claim that spatial metric perturbations vanish for every physical source.

For a sufficiently unresolved object held at a fixed position in a static
lapse `N=1+U/c²`, the proper internal action gives the coordinate-time
Hamiltonian `H_int,coord=N H_int,proper`. In a source/daughter basis a
schematic internal matrix may have detuning and conversion entries,

\[
 H_{\rm int,proper}=
 \begin{pmatrix}Mc^2&v\\v^*&2mc^2+E_{\rm rel}\end{pmatrix}.
 \tag{10}
\]

The lapse multiplies the **whole** matrix, including `v` and the retained
relative/binding energy; it does not select only its diagonal bare masses.
A constant lapse therefore changes coordinate-time rates and eigenvalue
units, but not the internal eigenvectors. Spatial uniform-force terms are
the COM/coordinate terms just analyzed, not an independent internal
`-d |grad U| sigma_z` matrix element about the object's energy center.

In the usual unresolved weak-field effective Hamiltonian this bookkeeping
is expressed by the same internal mass operator in inertia and weight,

\[
 H=\widehat{\mathcal M}c^2+{p^2\over2\widehat{\mathcal M}}
                  +\widehat{\mathcal M}U(R),\qquad
 \widehat{\mathcal M}=m_0+H_{\rm int}/c^2.
 \tag{11}
\]

Equation (11) is an order-by-order low-energy expression; it is not an
operator identity for all relativistic multiparticle states. Internal and
external quantum degrees may become entangled through time dilation. This
effect must not be mislabeled an acceleration-driven equilibrium mass
dipole. The primary-source check for (11) is recorded below.

## 4. What bound objects does the original positive square supply?

Rewrite (1) exactly as

\[
 V=m^2(|\Phi|^2+4|X|^2)
       +\Delta\left|X+{g_s\over\Delta}\Phi^2\right|^2
       +\lambda_{\rm rep}|\Phi|^4.
 \tag{12}
\]

The known canonical isolated energy bound `E>=m|Q|` follows by completing
the temporal squares with frequencies `m` and `2m`, then using the
nonnegative gradients and the last two terms in (12). It does not itself
classify metastable solutions, and gravity changes its premises.

There is a sharper elementary exclusion for **ordinary flat-space common
frequency Q-balls**. Take smooth profiles with finite energy and charge,
vanishing at infinity, no external trap, no gravity, and

\[
 \Phi(t,x)=f(x)e^{-i\omega t},\qquad
 X(t,x)=h(x)e^{-2i\omega t}.
\]

The profiles may be complex, allowing a spatial relative phase. Define
`I=|f|²+4|h|²`. The stationary field equations are the critical-point
equations of

\[
 F_\omega=A+B,\quad
 A=\int(|\nabla f|^2+|\nabla h|^2),\quad
 B=\int\left[(m^2-\omega^2)I
 +\Delta|h+(g_s/\Delta)f^2|^2+\lambda_{\rm rep}|f|^4\right].
 \tag{13}
\]

For `|omega|<=m`, `A,B>=0`. The admissible scaling
`f_l(x)=f(x/l), h_l(x)=h(x/l)` gives
`F_omega(l)=l A+l³ B`. A smooth finite-energy critical point must satisfy

\[
 A+3B=0.
 \tag{14}
\]

Hence `A=B=0` and the vanishing boundary condition forces the vacuum.
Ordinary exponentially localized daughter profiles require `|omega|<m`;
the proof also covers finite-energy profiles at equality if the scaling is
admissible. Profiles outside this frequency range are not being classified
by (14). The source-only free massive field has no such localized solution
either. This excludes a standard candidate for a nongravitating physical
anchor in the actual action, while retaining the separate possibilities of
self-gravitating boson configurations, traps, nonstationary oscillons,
finite-density phases and boundary-supported matter. The different
complex-host/real-mediator ARGON droplet action is not substituted for (1).

## 5. First physical finite-size response: tides

Let the external field vary slowly across an object of size `ell`, with
`ell/L_U <<1`. Expanding about the inertial COM in the fixed-mass model,

\[
 E_{\rm ext}=M_TU(R)+{1\over2}I^{ij}{\cal E}_{ij}
       +{1\over6}I^{ijk}\partial_i\partial_j\partial_kU+\cdots,
 \quad I^{ij}=\sum_a m_ay_a^iy_a^j,
 \quad {\cal E}_{ij}=\partial_i\partial_jU(R).
 \tag{15}
\]

There is no dipole term. For two particles `Iij=mu r_i r_j`, so

\[
 \mu\ddot r=-\nabla V_{\rm int}-\mu{\cal E}r
                 +O(\mu\ell^2\nabla^3U).
 \tag{16}
\]

A centered stable spring `V_int=kappa |r|²/2` has stiffness
`kappa 1+mu E`; a tide changes that stiffness, without a linear drive of
the centered relative coordinate. For a bound configuration with
equilibrium separation `r0` and positive Hessian `C`, its first shift is

\[
 \delta r=-\mu C^{-1}{\cal E}r_0+O({\cal E}^2).
 \tag{17}
\]

This formula is conditional on that bound configuration and its orientation
being defined; it does not add a spring or molecule to (1). More generally,
with internal shape coordinates `q`, positive shape Hessian `C`, and
`Iij=I0ij+B_ij,alpha q_alpha+...`, minimization of

\[
 E=E_0+\tfrac12 q^TCq+
       \tfrac12(I_0+Bq):{\cal E}
\]

gives

\[
 q=-\tfrac12C^{-1}B^T:{\cal E},\qquad
 E_{\rm eff}=E_0+\tfrac12I_0:{\cal E}
  -\tfrac18{\cal E}:BC^{-1}B^T:{\cal E}+O({\cal E}^3).
 \tag{18}
\]

For a spherical object in external vacuum, `I0` is isotropic and
`trace E=laplacian U=0`, so the leading induced energy is quadratic in the
tidal tensor. Near external matter the trace term also couples to ambient
density. In neither case is (18) a universal function of `|grad U|` alone.

The characteristic strain is `|E|/omega_int²`, with
`omega_int²~C/mu`, while differential acceleration across the object is
`~ell |E|`. In relativistic language the dimensionless finite-size
parameter is `ell² |Riemann|`, and adiabatic elimination also requires
external frequencies well below the relevant internal gaps. Arbitrarily
soft modes can invalidate this expansion and deserve a separate phase
analysis; the failure is not a derivation of the target law. Tidal doublets
could be legitimate internal polarizers, but their source is a projection
of curvature rather than a uniform acceleration magnitude.

## 6. What changes would genuinely open a dipole route?

For two inertial masses `m1,m2`, let the passive gravity charges instead be
`gamma1,gamma2`. In inertial COM coordinates the uniform-field relative
coupling is

\[
 E_{\rm ext}=\Gamma U(R)+d_g r\cdot\nabla U,
 \quad d_g={\gamma_1m_2-\gamma_2m_1\over m_1+m_2}
          =\mu(\eta_1-\eta_2),\quad \eta_a=\gamma_a/m_a.
 \tag{19}
\]

Then `mu rddot=-grad V_int+d_g g_vec`. Equation (19) is a constructive
counterexample to an overbroad assertion that positive masses can never
have internal gravitational polarization: positive but unequal ratios
`eta1!=eta2` do permit it. The original minimal action has equal ratios;
different masses or different U(1) charges alone do not produce (19).
Nonminimal species-dependent forces would be an action amendment, and
ordinary curvature couplings would still first probe curvature.

A second loophole is an actual support/trap that holds one component or a
reference body against free fall. Weight can then elastically displace
the other component. The anchor's force and energy must be retained.
Specifying such a supported state can be legitimate; declaring only a
reference-subtracted displacement without its physical constraint is not
the same construction. A freely falling solid supplies internal elastic
restoring forces and a physical lattice frame but still shares uniform
acceleration; translation breaking alone does not replace a support force.
No solid phase or support is derived here from (1). This is an open
collective-state obligation, not a theorem excluding all solids.

For a genuine ensemble of springs with density `n`, physical dipole
`d_g r` and local energy `n kappa r²/2`, the physical polarization
`P=n d_g r` has

\[
 W(P)={\kappa\over2nd_g^2}|P|^2,\qquad
 \chi={nd_g^2\over\kappa}.
 \tag{20}
\]

The target (2) requires

\[
 W_{\rm full}={K\over2}|P|^2
       +{K^2\over3a_0}|P|^3+{K^3\over4a_0^2}|P|^4+\cdots,
 \quad {dW_{\rm full}\over d|P|}={a_0u\over a_0-u}
      =u+{u^2\over a_0-u}.
 \tag{21}
\]

It therefore needs `kappa=K n d_g²` even before matching the higher
terms. In the isolated minimally coupled internal route `d_g=0`, so the
needed nonzero susceptibility is absent. In a genuinely amended or
supported model, (20) makes the required tuning and density dependence
explicit; the nonlinear spring energy or gap spectrum and the scale `a0`
must still be derived. Gravitational subtraction of `K|P|²/2` removes only
the first term of (21) and leaves the desired derivative
`R(u)=u²/(a0-u)`; it does not create the missing dipole coupling.

## 7. Source checks, finite checks and audit boundary

The analytic conclusions (3), (6)-(7), (12)-(14), (15)-(19), and (21) are
proved above from the stated definitions. The accompanying exact-rational
script checks their coefficient bookkeeping on a declared finite grid; it
is a consistency check rather than evidence for unclassified phases.
The code, contract, result and v2 manifest give the exact executed scope.

Two external primary sources were checked on 2026-10-19:

* Zych and Brukner, *Quantum formulation of the Einstein Equivalence
  Principle*, arXiv:1502.00971v1, 3 February 2015, PDF p. 3, Eqs. (1)-(2),
  and Appendix A pp. 16-17. The version header and equations were read.
  The common internal-energy mass operator gives (11) at the source's
  first-order internal-energy/weak-field accuracy. This verifies the
  bookkeeping comparison, conditional on an unresolved low-energy object;
  it does not establish existence of a bound object in (1).
  [Versioned primary source](https://arxiv.org/pdf/1502.00971v1).
* Goldberger and Rothstein, *An Effective Field Theory of Gravity for
  Extended Objects*, arXiv:hep-th/0409156v2, 11 March 2005, Sec. II B,
  Eq. (5), pp. 4-5, and Sec. IV discussion, pp. 14-16. The action is a
  proper-time monopole plus finite-size curvature operators; internal
  coefficients require matching to an actual object model. This supports
  the distinction between object existence, monopole motion and tidal
  matching. Their spinless compact-binary post-Newtonian power counting
  is **not** transplanted to the scalar medium or used to exclude its
  collective phases.
  [Versioned primary source](https://arxiv.org/pdf/hep-th/0409156v2).

The project cache was queried by exact identifiers before fetching and
had no exact hit for Goldberger/Rothstein v2 or the initially considered
Zych/Brukner v2. The latter version does not exist in the checked arXiv
history; the actual reviewed source is v1. No external PDF/text bytes are
retained by this lane, so no retained-source hash is asserted. These
primary-source checks concern only the explicitly stated comparisons;
there is no novelty claim. The older Manasse/Misner paper was discovered
but no formula from it is needed for the derivation or counted as an
authenticated dependency here.

**Self-audit claim card.** For every finite isolated Newtonian composite
of fixed positive equal grav/inertial masses with translation-invariant
internal interactions and an affine external potential, internal EOM are
independent of that potential's gradient. For the original nongravitating
canonical action, no smooth finite-energy common-frequency Q-ball exists
on the `|omega|<=m` branch with admissible scaling and vanishing boundary
data. **Primary verdict: proved as written.** The extension to the full
field action is a local linear weak-field coordinate statement under
stress conservation, not an unqualified relativistic no-go.

| Obligation | Assessment |
|---|---|
| Newtonian uniform-field separation | Passed by raw substitution (3) |
| Unequal mass/charge center | Passed; mixed kinetic term and Schur identity retained |
| Conversion/source and reciprocal energy | Passed at local weak-field level using full conserved stress; no species-rest-only source used |
| Internal energy superpositions | Conditional low-energy matching comparison (11); quantum time dilation retained |
| Usual flat-space Q-ball anchor | Excluded on the precisely stated harmonic/scaling branch |
| Tidal first term and scale | Passed to the displayed multipole/adiabatic order; coefficients require object matching |
| Exact target W from original particles | Not established; necessary uniform-field internal coupling absent in this route |
| All collective phases, strong self-gravity and supported states | Not addressed, and not excluded |

Remaining constructive continuation: identify an actual stable collective
state or support in the original action, define its total momentum and
complete reciprocal source, and demonstrate an invariant dipole operator
that survives transforming the entire state to free fall. If it responds
only to tides, an acceleration-only ensemble law needs another bridge.
A phenomenologically chosen two-level ensemble with an assumed dipole
matrix element remains a conditional different model until that step is
supplied. No action amendment is silently counted as a result of (1).
