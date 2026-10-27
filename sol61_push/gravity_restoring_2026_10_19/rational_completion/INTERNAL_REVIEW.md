# Independent scoped audit of the physical internal-polarization note

Reviewed target:
`sol61_push/gravity_restoring_2026_10_19/internal_polarization/INTERNAL_POLARIZATION.md`

Exact target: 22,797 bytes, SHA-256
`31272241f40f099ac307cd32593ec425f7c2ee8639307668d39e2495fdcf1b9e`.
The file was read in full and its hash checked directly. The canonical
particle action was separately read from the parent source
`sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md`,
whose reviewed bytes have SHA-256
`c81b4a3136d433a2b7a0bf06ec87f61389b8e5a73da6c7603a6b264dda0bbe43`.
No physical source file was edited.

This is a separate agent's reconstruction with shared project context,
not an external referee report. Scope: the Newtonian COM/Schur argument,
complete-stress affine-source extension, positive-square common-frequency
flat-space Q-ball exclusion, leading tidal response, and conditional
physical-spring normalization. The author's finite-grid implementation was
not independently rerun or audited. The quoted external papers were not
reauthenticated; the central conclusions below are independently derived
from the displayed action and do not use a new external theorem arrow.

**Primary verdict: proved as written within the note's named restrictions.**
No correction to the target source is required for these scoped claims.
The verdict does not establish that the action has no bound states or
collective phases, or that no other route can produce the requested law.

## 1. Claim card and dependency graph

The audited conclusions are:

1. For finitely many fixed positive inertial masses with equal passive
   gravitational masses, translation-invariant internal interactions, no
   support/trap, and an external potential affine across the whole object,
   the internal Newtonian equations do not depend on its uniform gradient.
   Any mass dipole about the inertial COM vanishes identically.
2. For the minimally coupled canonical field action, the corresponding
   **local linear weak-field** statement uses the complete on-shell
   conserved stress tensor. A static affine metric perturbation is pure
   coordinate at that order. Conversion energy cannot be omitted from
   the gravitational source.
3. For the original nongravitating flat-space action, smooth finite-energy
   profiles vanishing at spatial infinity with a single common harmonic
   frequency and admissible scale variation are vacuum on the branch
   `|omega|<=m`.
4. The leading physical finite-size coupling in the fixed-mass multipole
   expansion is tidal. Integrating stable nonsingular shape variables
   gives the stated `−1/8` quadratic induced-energy term.
5. If a different model supplies an actual differential gravity charge
   `d_g`, a spring ensemble has `chi=n d_g²/kappa`; matching the desired
   quadratic energy requires `kappa=K n d_g²`. The original minimal
   isolated internal route has `d_g=0` and does not supply that response.

Dependencies are separate rather than circular:

```text
equal inertial/passive masses + affine external U
    -> raw COM substitution -> internal-force cancellation
    -> arbitrary reference-center mass matrix -> same Schur cancellation

minimal canonical action + on-shell complete stress conservation
    -> gauge variation is boundary term
    -> affine linear metric is removable locally
    -> no invariant uniform-field internal dipole about free fall

original potential square + harmonic profile ansatz
    -> nonnegative F_omega on |omega|<=m
    -> admissible spatial scaling -> vacuum

ordinary external-potential multipole expansion + mass COM
    -> no dipole, quadrupole/tidal coupling
    -> positive invertible shape Hessian -> induced energy

explicit unequal gravity/inertia ratios OR actual support
    -> possible differential source
    -> spring constitutive dictionary and additional G calibration
```

The tautology that a first energy moment about its own center is zero is
**not** used alone as a physical no-go. The complete-source/gauge argument
is the necessary additional implication, and the note supplies it.

## 2. Newtonian COM and reference-center cancellation

Write `x_a=R+y_a`, with `sum m_a y_a=0`. At every time the differentiated
constraint gives `sum m_a dot y_a=0`. Therefore

\[
 \sum_a\frac{m_a}2\dot x_a^2
 =\frac{M_T}2\dot R^2+\sum_a\frac{m_a}2\dot y_a^2,
\]

and, for `U=U0+A dot x`,

\[
 \sum_a m_aU(x_a)=M_T[U_0+A\cdot R].
\]

The internal potential depends only on differences and hence on the `y`.
This independently yields the note's Eq. (3). A time-dependent `A(t)`
does not change the conclusion: it appears as an external coefficient in
the COM equation, and still has no internal term. Internal Newtonian
self-gravity is allowed because it is translation invariant. Relativistic
mass defects or particle conversion are not silently incorporated into
this fixed-mass theorem; they require the separate field argument.

For two particles, solve the reference-center definitions directly:

\[
 x_1=R_q+\frac{q_2}Q r,\qquad
 x_2=R_q-\frac{q_1}Q r.
\]

The kinetic matrix in `(R_q,r)` is

\[
 \begin{pmatrix}M_T&\delta_q\\\delta_q&A_q\end{pmatrix},\quad
 \delta_q=\frac{m_1q_2-m_2q_1}Q,\quad
 A_q=\frac{m_1q_2^2+m_2q_1^2}{Q^2}.
\]

Its determinant is `m1 m2`, by direct expansion. Subtracting
`delta_q/M_T` times the COM equation from the relative equation leaves

\[
 \left(A_q-\frac{\delta_q^2}{M_T}\right)\ddot r
 =-\nabla V,\qquad
 A_q-\delta_q^2/M_T=\frac{m_1m_2}{M_T}=\mu.
\]

Both gradient terms cancel exactly. This independently verifies the sign,
mass weighting and Schur factor in Eqs. (5)–(7). A nonzero rest-mass moment
about the charge center is not an independent internal force. Holding that
center fixed would add constraint forces, which the note correctly names
as a changed physical system. The illustrative detuning example is
conditional and is not treated as an actual bound conversion object.

## 3. Full field source and affine weak gravity

The raw canonical flat action has

\[
 \mathcal L=\partial_\mu\Phi^*\partial^\mu\Phi
 +\partial_\mu X^*\partial^\mu X-V,
\]

with the full cubic interaction inside `V`. The symmetric stress contains
both kinetic fields and this potential. Translation invariance and the
full equations of motion imply `partial_mu T^{mu nu}=0`; a stress made
only from species rest stocks would not obey that identity during
conversion.

For finite energy and finite first moment with vanishing boundary flux,

\[
 \frac d{dt}\int x^iT^{00}d^3x=\int T^{i0}d^3x.
\]

Symmetry of `T` identifies the latter with the conserved momentum. This
checks the total energy-center definition without assuming pointwise
positivity of `T00`. In the isolated canonical theory the separate square
bound gives nonnegative total energy; a nonvacuum object also needs nonzero
total energy to define the center.

For a metric perturbation the linear coupling is proportional to
`int h_munu T^{munu}`. Under
`h_munu=partial_mu xi_nu+partial_nu xi_mu`, integration by parts yields a
boundary contribution plus a term proportional to
`xi_nu partial_mu T^{mu nu}`, which vanishes on shell. The explicitly
displayed constant-`A` coordinate vector gives

\[
 2\partial_0\xi_0=2A\cdot x/c^2,\quad
 \partial_0\xi_i+\partial_i\xi_0=0,\quad
 \partial_i\xi_j+\partial_j\xi_i=0.
\]

Thus it actually generates the lapse-only affine perturbation used in
the note. The general affine case can also be checked without importing
an external curvature theorem. Write
`h_munu=a_munu+b_munu,rho x^rho`, with the first two indices symmetric.
Then the explicit quadratic coordinate vector

\[
 \xi_\mu=\frac12a_{\mu\nu}x^\nu
 +\frac14(b_{\mu\nu,\rho}+b_{\mu\rho,\nu}
                -b_{\nu\rho,\mu})x^\nu x^\rho
\]

has symmetrized derivative exactly `h_munu`. This verifies the local
coordinate removal directly, including the stated static case.
The physical comparison must transform the whole isolated object and its
boundary/state data; it is not a statement that coordinate clocks or
supported apparatus have no gravitational response.

The canonical lapse calculation also checks directly. For
`L=|dot Phi|²/N+|dot X|²/N−N(gradients+V)`, Legendre transformation at
fixed canonical momenta gives

\[
 H_N=\int N\,[|\pi_\Phi|^2+|\pi_X|^2
                 +|\nabla\Phi|^2+|\nabla X|^2+V]d^3x.
\]

The cubic conversion entry is redshifted along with the diagonal mass
entries. A constant lapse scales a projected internal matrix as a whole
and leaves its eigenvectors unchanged. A calculation that redshifts only
the bare detuning while freezing the off-diagonal conversion is not this
probe. No part of this statement removes tidal curvature.

Eq. (11)'s internal-mass operator is used only as an unresolved low-energy
bookkeeping comparison. Its direct first-order expansion has both
`H_int U/c²` and `−p² H_int/(2m0²c²)`, provided the internal/external
operators separate at that order and `|H_int|/(m0c²)`, `v²/c²`, and
`|U|/c²` are small on the retained subspace. It cannot be promoted to a
general relativistic composite operator identity. The note expressly
limits it and retains quantum time-dilation entanglement; the central
uniform-field result does not depend on authenticating the cited paper.

## 4. Positive-square Q-ball branch

Expanding the potential square gives

\[
 m^2(|\Phi|^2+4|X|^2)
 +\Delta\left|X+\frac{g_s}{\Delta}\Phi^2\right|^2
 +\lambda_{\rm rep}|\Phi|^4
 =m^2|\Phi|^2+M^2|X|^2
 +g_s(X^*\Phi^2+\mathrm{c.c.})+\lambda_{\rm tot}|\Phi|^4.
\]

Here the coupling can be made real by a field phase convention; the
source's `g_s²` convention and `Delta>0,lambda_rep>0` agree with the raw
action. Completing the temporal squares at frequencies `m` and `2m`
then gives `E>=m|Q|`. This energy inequality alone is not a soliton
classification, and the note correctly does not use it that way.

For the independent stronger statement insert
`Phi=f exp(-i omega t)`, `X=h exp(-2i omega t)`. The temporal kinetic
term is `omega²(|f|²+4|h|²)`, with the factor four fixed by the source's
charge-two harmonic. The fixed-frequency profile functional is precisely

\[
 F_\omega=A+B,\quad A=\int(|\nabla f|^2+|\nabla h|^2),
\]

\[
 B=\int[(m^2-\omega^2)(|f|^2+4|h|^2)
       +\Delta|h+(g_s/\Delta)f^2|^2
       +\lambda_{\rm rep}|f|^4].
\]

On `|omega|<=m`, both pieces are nonnegative. Under the admissible scale
variation `f(x/l),h(x/l)` in three dimensions, the gradient piece is
`l A` and the no-gradient piece `l³ B`. Stationarity forces `A+3B=0`.
Consequently both vanish. Zero gradient and the vanishing boundary
condition imply `f=h=0`, including at `|omega|=m` when the variation is
admissible. No spherical, real-profile, constant-relative-phase, or
small-amplitude assumption was needed.

This confirms exactly the stated common-frequency branch exclusion.
It does not classify frequencies outside that branch, embedded/nonordinary
profiles, nonharmonic oscillons, finite-density backgrounds, external
boundaries, supported states, or self-gravitating objects. The note names
these restrictions. A singular or inadmissible scaling family cannot be
inserted into this proof without an additional regularity argument.

## 5. Tidal multipoles and induced shape energy

Expand the external potential about the mass COM. The term linear in
`y_a` vanishes, leaving

\[
 E_{\rm ext}=M_TU(R)+\frac12\mathcal E_{ij}
                   \sum_a m_ay_a^iy_a^j+\cdots.
\]

For two particles the second moment is `mu r_i r_j`, so variation gives
`mu rddot=−grad V−mu E r`, to the retained quadrupole order. A centered
spring therefore receives a stiffness perturbation, not an independent
linear force. At a chosen equilibrium `r0` with invertible positive shape
Hessian `C`, first-order expansion yields
`delta r=−mu C^{-1} E r0`. This is a leading-multipole and small-tide
formula; higher external derivatives remain among the omitted multipoles.

For shape coordinates set `t_alpha=(B^T:E)_alpha`. The energy to the
displayed order is

\[
 E=E_0+\frac12I_0:\mathcal E
       +\frac12q^TCq+\frac12q^Tt.
\]

Completing its square gives

\[
 E=E_0+\frac12I_0:\mathcal E
 +\frac12(q+\tfrac12C^{-1}t)^TC(q+\tfrac12C^{-1}t)
 -\frac18t^TC^{-1}t.
\]

Both the minimizer and the `−1/8` factor in Eq. (18) follow. Positive
`C` makes the induced quadratic term negative semidefinite, as expected
for relaxation. Translations/rotations that are exact zero modes cannot
be included in an unqualified inverse `C^{-1}`; the note's positive shape
Hessian and defined orientation are necessary hypotheses. A freely rotating
orientation or a critical soft mode needs separate dynamics. The expansion
also requires the external field to vary slowly across the object, tides
small compared with the relevant internal restoring eigenvalues, and
frequencies below the retained gaps.

For a spherical unperturbed second moment, the permanent term is
proportional to `trace E=laplacian U`, which vanishes in external vacuum.
This does not assert that an arbitrary nonspherical object lacks a linear
permanent quadrupole coupling. Near external matter the trace term remains.
The curvature/shape coefficients require matching to an actual object;
the calculation has not constructed such an object from the scalar action.
This is why no new external EFT theorem is needed for this restricted
Newtonian multipole conclusion.

## 6. Differential charges and the target spring normalization

For unequal passive/inertial ratios the direct COM expansion gives

\[
 d_g=\frac{\gamma_1m_2-\gamma_2m_1}{m_1+m_2}
    =\mu(\eta_1-\eta_2),\qquad
 E_{\rm int,grav}=d_g r\cdot\nabla U=-d_gr\cdot g.
\]

Therefore the relative force is `+d_g g`, with the sign stated in the
note. Equal universal ratios set `d_g=0` even if the constituent masses
and U(1) charges differ. Positive unequal ratios can instead give a
nonzero dipole, so the note does not overstate positivity as an absolute
no-go. Those ratios or an actual support are new physical inputs.

For density `n` of actual springs, substituting `r=P/(n d_g)` into
`n kappa r²/2` gives

\[
 W(P)=\frac{\kappa}{2nd_g^2}P^2,\qquad
 P=\frac{nd_g^2}{\kappa}g.
\]

The target expansion has quadratic coefficient `K/2`, so the required
relation is `kappa=K n d_g²`, not its reciprocal or a density-independent
spring constant. The residual derivative after gravitational quadratic
subtraction is correctly `u²/(a0−u)`. Neither that subtraction nor the
normalization equation creates a missing physical dipole source or fixes
the nonlinear spring law and `a0`.

## 7. Obligation matrix and exact remaining gap

| Obligation | Review result |
|---|---|
| Raw positive-square action matches parent | Passed by direct expansion and parent-source read |
| Newtonian COM/internal separation | Passed for the stated finite fixed-mass isolated affine-field model |
| Reference-center Schur cancellation | Passed by independent coordinate substitution and determinant |
| Full conversion-energy source | Passed by canonical lapse Legendre transform |
| Affine weak metric removal | Passed locally at linear weak-field order with complete conserved stress |
| Internal energy mass operator Eq. (11) | Conditional low-energy comparison; not used as a global theorem |
| Flat common-frequency Q-ball exclusion | Passed on `|omega|<=m`, smooth finite-energy vanishing profiles, admissible scaling |
| Tidal force and induced energy | Passed at the stated multipole/small-tide/adiabatic order with invertible positive shape Hessian |
| Physical spring source and G normalization | Passed conditionally when the additional differential source/support exists |
| Existence of bound object, lattice or collective phase | Not addressed by this audit and not established by the note |
| Strong gravity, global GR, arbitrary phases/frequencies | Outside the claimed scope |
| Author's finite-grid implementation | Not audited or rerun; manifest freshness only checked |

The existing runner-v2 manifest was validated read-only with its documented
validator: it is a valid record with status `completed`. This confirms
current provenance, not the universal mathematical argument or code
coverage. No new scientific computation was executed for this review.

The smallest remaining physical implication is an actual local internal
polarization operator and occupied state of the original theory that
survives free fall and has the required reciprocal source. The audited
isolated-object construction supplies no such acceleration-driven dipole.
Tidal polarization, density response, and supported/nonuniversal models
remain distinct routes with their own variables and hypotheses.

The rational-completion note is separately frozen at SHA-256
`4c055419d663114a2831feebab02f704da35c2724bf728db80b8b475595e8367`.
The sibling's final narrow rational review is pinned at
`241788a243630f3bad9a82becfe7474df4f7b2dfbb011d11a5939d4dc0e029d5`.
Those cross-review facts do not extend either audit beyond its explicit
scope, and no agreement between agents is being used as a proof certificate.
