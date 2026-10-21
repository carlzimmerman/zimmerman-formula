# A current selector can be derived; the canonical response switch does not follow

20 October 2026. Assessment base supplied by the coordinator:
`ff7df583f7d6d3a8a60d0c9cbb8c602302d28653`. Actual read-source bytes are
pinned in `source_hashes.json`. Only this new `selector/` directory is
written. No old proof, canonical statement, campaign, job, or Git state is
changed. Natural units, including `hbar=1`, apply below.

**Normalized target and primary verdict: incomplete, with the constitutive
identification missing.** A chosen population split does have a derived
conversion source, and a compensating longitudinal current can be written
without a fitted coefficient. But the resulting vector is a nonlocal
representation of the chosen density. Rewriting the original scalar action
in that representation does not give the canonical polarization energy or
make the released density cease to gravitate. Under the unchanged canonical
field equation an exactly zero-response open region is impossible under a
nonzero gravitational gradient when ordinary local polarization variations
remain admissible. Empty-medium/constraint boundaries are expressly outside
that last statement.

## 1. Inputs, definitions and dependency graph

Raw inputs are the frozen canonical S2/S3 field and displacement identity,
the original `Phi,X` carrier and its NR currents in MASTER and
`coherent_current/CURRENT_AND_MATCHING.txt`, and the explicit current-dual
actions in `density_duality/DENSITY_DUALITY.md` and
`EMERGENT_POSITIVE_CURRENT.md`. The source list gives full paths/hashes.
The current duality's bare-`W` gauge obstruction and the finite-compressibility
versus `K/k^2` mismatch were already established there and in
`micro_response/DERIVATION.md`; they are not counted as new discoveries.

The question here is whether adding an actual binding/species selector and
its already existing conversion dynamics supplies that missing implication.
The dependency graph is

`existing scalar equation -> selected density and source -> compensating
current -> exact gravitational-action rewrite -> constitutive matching ->
physical on/off response -> memory`.

The first four arrows can be computed. The rewrite fails to provide the
constitutive matching; neither its current correction nor the field equations
produce an S4 memory selector. A different phase, physical support boundary,
or matched extra order parameter is a logically open continuation, not
implicitly excluded by this result.

## 2. Canonical response has one nonzero branch at a nonzero imposed field

Write the canonical scalar force potential as `Phi_N` here to distinguish it
from the complex carrier, and put `p=|P|`, `u=Kp`, `K=4pi G`. The given
quasistatic Lagrangian is

\[
 L=-{|\nabla\Phi_N-KP|^2\over2K}-\rho_b\Phi_N
       -W_{\rm rem}(Kp)-{\gamma\over2}|\nabla P|^2,
 \quad K W_{\rm rem}'(u)=R(u)={u^2\over a_0-u}.
                                                               \tag{1}
\]

The prime in (1) means derivative with respect to `u`. Compactly supported
variations of the independent physical fields give

\[
 \Delta\Phi_N=K(\rho_b+\nabla\cdot P),\qquad
 \nabla\Phi_N-KP-R(u)\widehat P+\gamma\Delta P=0.       \tag{2}
\]

The vector `R(u) P-hat` has its continuous zero value at `P=0`.
Therefore if a stationary solution has `P=0` throughout an open region
where arbitrary small local `P` variations are admissible, (2) requires
`grad Phi_N=0` there. Any nonzero field in that region contradicts an exact
off state. In particular positive baryonic density in the whole region
also contradicts `Delta Phi_N=0` there. This is a local field-equation
test; it is not merely the absence of a written switch variable.

For a fixed imposed `grad Phi_N`, the `P` equation minimizes

\[
 F[P]=\int\left[{Kp^2\over2}+W_{\rm rem}(Kp)
             +{\gamma\over2}|\nabla P|^2
             -P\cdot\nabla\Phi_N\right]d^3x.           \tag{3}
\]

On `0<=u<a0`, the two eigenvalues of the local material Hessian are

\[
 \lambda_\parallel={K\over(1-u/a_0)^2},\qquad
 \lambda_\perp={K\over1-u/a_0},                        \tag{4}
\]

with limiting value `K` at zero. Hence (3) is strictly convex on any convex
admissible domain with the same boundary/linear stock constraints. If its
minimum exists it is unique. A binding-sign label absent from (1) cannot
choose a second quasistatic constitutive branch at those same inputs.
For the homogeneous/zero-stiffness local control,

\[
 g=|\nabla\Phi_N|=u+R(u)={a_0u\over a_0-u},\qquad
 u={a_0g\over a_0+g}>0\quad(g>0).                     \tag{5}
\]

Equations (2)-(5) concern the response for fixed imposed potential and
admissible physical `P`. They do not prove uniqueness of the complete
self-gravitating kinetic halo. They do not exclude transient orbital
history, different distribution functions, or constraints that remove field
variations. At an empty-medium boundary, or if `div P` is fixed so that only
solenoidal variations are permitted, the unconstrained second equation of
(2) need not apply. A law that removes the material response degrees of
freedom upon release would be precisely the physical selector still needing
derivation; this argument must not assume it away.

## 3. Actual species conversion supplies a source, but not a response label

The existing scalar NR equations give

\[
 \dot n_\psi+\nabla\cdot j_\psi=2\mathcal R,\qquad
 \dot n_b+\nabla\cdot j_b=-\mathcal R,\qquad
 \mathcal R=2c_3\operatorname{Im}(b\psi^{*2}),
 \quad \partial_t(n_\psi+2n_b)+\nabla\cdot(j_\psi+2j_b)=0.
                                                               \tag{6}
\]

The operator version has the corresponding Hermitian conversion operator;
the displayed formula is its coherent classical form. Thus, for example,
choosing `rho_t=m n_psi`, `rho_f=2m n_b` gives an actual source
`S_t=2m R`, `S_f=-2m R`. It introduces no phenomenological reaction rate.
The rest density is instead `m n_psi+M n_b`, differing by `delta n_b`;
detuning, interaction and kinetic energy complete its gravity ledger.

This example is not an identification of the true S4 states. The source has
charge two and the daughter charge one, and the actual reaction is reversible
with its relative phase/state. S4's released density need not be a source
species and may remain gravitationally bound. Equation (6) only supplies
a concrete original-field source with which to test the proposed current link.

## 4. Derive the compensating current exactly

For any specified selected density/flux satisfying
`dot rho_t+div j_t=S_t`, choose an inverse Laplacian and boundary prescription
and define the longitudinal representative

\[
 P_t=\nabla\Delta^{-1}(\rho_t-\bar\rho_t),\qquad
 j_t^L=\nabla\Delta^{-1}\nabla\cdot j_t.
\]

Direct differentiation gives

\[
 \boxed{\partial_tP_t=-j_t^L+
          \nabla\Delta^{-1}(S_t-\dot{\bar\rho}_t).}     \tag{7}
\]

For a fixed background the second term has divergence `S_t`; its coefficient
is fixed. If the actual source (6), or a mode-capture source, is known, this
is an explicit compensating current from that source. A transverse current
is represented by the curl potential in the already derived dual formula
`j=-dot P+curl A`, rather than being silently discarded.

This is a nonlocal kinematic solution. It is not a local material equation
or a new action. In a periodic box the inverse acts only on zero-mean
functions; changing total selected stock requires a changing background or
an explicitly retained zero-mode/receiver. On isolated space, nonzero
integrated source changes the `1/r^2` polarization tail and its boundary
flux. It cannot be hidden by claiming a compact, source-free current.
Different inverse/boundary and solenoidal choices do not select an observable
response by themselves.

## 5. A bound-state projector is not a local two-species field

At a common finite one-body regulator, let `Pi_B(t)` be the spectral projector
onto negative-energy modes of a specified host Hamiltonian `h(t)` and let
`Pi_F=1-Pi_B`. Set `psi_B=Pi_B psi`, `psi_F=Pi_F psi`. Their total numbers
are well-defined, but local density obeys the exact identity

\[
 |\psi|^2=|\psi_B|^2+|\psi_F|^2
                  +2\operatorname{Re}(\psi_B^*\psi_F).       \tag{8}
\]

The cross term integrates to zero by orthogonality; it need not vanish
pointwise. An incoherent block-diagonal one-body state may remove its
expectation, but that is a state condition. Also the projected quantum
fields have commutator `[psi_B(x),psi_B^dagger(y)]=Pi_B(x,y)`, not the local
delta function of an independent new species. The projector kernel depends
on the full host and its boundary data, rather than a local binding flag.

Write the original mean-field equation as `i dot psi=h psi+F[psi,b]`.
Then exactly

\[
 i\partial_t\psi_B=h\psi_B+\Xi_B,\qquad
 \Xi_B=[\Pi_B,h]\psi+\Pi_B F+i\dot\Pi_B\psi,
\]
\[
 \partial_t|\psi_B|^2+\nabla\cdot j_B
          =2\operatorname{Im}(\psi_B^*\Xi_B).           \tag{9}
\]

Here `j_B=Im(psi_B^* grad psi_B)/m`. For an instantaneous spectral projector
`[Pi_B,h]=0`; the projected interaction and moving-projector terms remain.
The actual cubic/quartic source can therefore be inserted in (7), but is
nonlocal and includes interference/transport accounting. Globally,
`dot N_B=<psi^dagger dot Pi_B psi>+i<[H,N_B]>`, so a static one-body
Hamiltonian alone does not produce capture. The derived interacting
capture kernels in the preceding phase compute part of this commutator.

There is an additional threshold problem with an instantaneous switch.
For a differentiable isolated spectral block and distinct eigenvalues,
differentiating `[Pi_B,h]=0` gives, in the instantaneous eigenbasis,

\[
 (\dot\Pi_B)_{ab}
 ={p_a-p_b\over\epsilon_a-\epsilon_b}\,(\dot h)_{ab},
 \qquad p_a\in\{0,1\}.                               \tag{10}
\]

The controlled projection requires a gap between selected and excluded
states. At the proposed binding/unbinding threshold this gap closes in
the continuum limit and the negative-energy subspace can change rank.
Equation (10) supplies no uniform smooth-switch approximation there.
Specific matrix-element zeros can suppress mixing; universal divergence
is not claimed. The full original evolution or a justified resonance
reduction is required exactly where a binary energy-sign label would flip.

## 6. The exact action rewrite exposes the missing constitutive term

Consider localized selected and released densities, keep the original
Newtonian source `rho_tot=rho_t+rho_f`, and use `div P_t=rho_t` with its
proper exterior tail. This assumes a legitimate additive source split:
the coherent projector cross-density in (8) must first be retained as a
separate ordinary source or shown absent in the actual state. Detuning and
other stress-energy corrections likewise keep their own source ledger.
They are not erased by the selected-density notation. Suppressing only the already specified matter
kinetic/composition terms, the actual gravitational Lagrangian rewrites as

\[
 L_{\rm actual}=-{|\nabla\Phi_N|^2\over2K}
       -(\rho_b+\rho_f)\Phi_N+P_t\cdot\nabla\Phi_N
       -e_{\rm actual}+\text{boundary/kinetic terms},
\]
\[
 =-{|\nabla\Phi_N-KP_t|^2\over2K}
       -(\rho_b+\rho_f)\Phi_N
       +{K|P_t|^2\over2}-e_{\rm actual}
       +\text{boundary/kinetic terms}.                \tag{11}
\]

The boundary term is `-div(Phi_N P_t)` before imposing the actual falloff.
The resulting Poisson equation is

\[
 \nabla\cdot(\nabla\Phi_N-KP_t)=K(\rho_b+\rho_f).     \tag{12}
\]

Thus the released density still gravitates normally. To obtain canonical
(1) from this mere change of variables, the actual matter action would
have to produce

\[
 e_{\rm actual}={K|P_t|^2\over2}
          +W_{\rm rem}(K|P_t|)
          +{\gamma\over2}|\nabla P_t|^2
\]

in the relevant retained variables, with the necessary kinetic/source
dictionary too. That is a matching condition, not a consequence of (7).
For example the admitted source-eliminated scalar contact is

\[
 e_{\rm contact}={g_2\rho_t^2\over2m^2}
               ={g_2\over2m^2}(\nabla\cdot P_t)^2,
                                                               \tag{13}
\]

and not `K|P_t|^2/2`. Its quadratic longitudinal kernel is proportional to
`k^2|P_t|^2`; the canonical critical kernel is `K|P_t|^2`. The microscopic
current source, however accurately calculated, does not change this
operator distinction. The actual two-species/projected action can contain
additional composition, relative-phase, interference and gradient terms;
they must be retained and matched, not replaced by the desired `W`.

This repeats the earlier static kernel restriction only to execute the new
selector/current-to-action comparison. It does not rule out every singular
or gapless phase. Those routes require their own actual response calculation.

## 7. Dual-current freedom cannot make the selector physical

The actual conserved weighted current may be locally dualized as `J=*dB`
on the already stated smooth contractible phase chart. Its gauge freedom
`B->B+dLambda` leaves `J` fixed and shifts the spatial representative by
`P->P+m curl Lambda`. The earlier raw dual action uses differentiated `B`;
inserting a bare `W(|P|)` is not invariant under this gauge freedom. This
known obstruction is independent of which population is called tethered.

There is a separate **partition** freedom, not the same gauge operation.
One may choose any conserved reference `J_f` and write `J_t=J-J_f`.
Locally choosing another two-form `C` shifts
`J_f->J_f+*dC`, `J_t->J_t-*dC`, without changing the total. In particular
the all-selected and none-selected conventions leave the original scalar
action and its total gravitational observables identical. They cannot
acquire different forces merely by changing names. If an extra term
`W(P_t)` makes those assignments observable, it has introduced a physical
population map/interaction that must be derived, rather than proved the
original action equivalent.

During actual exchange the selected current has divergence `S_t`, so it
cannot itself be `*dB_t` as a smooth four-current. Subtracting a current
with that divergence can make a conserved remainder; (7) constructs one
longitudinal choice after specifying time slicing and boundaries. The
choice is nonunique and does not derive canonical constitutive energy.
Thus the compensating-current calculation repairs the *kinematic ledger*
without repairing the *response matching*. It is not a new fitted switch.

## 8. Exact result, review limits and continuation

| Obligation | Result |
|---|---|
| Canonical field response at unchanged coefficients | Derived (2)-(5); no exactly off open region under nonzero field when local variations remain admissible |
| Source supplied by original conversion | Derived (6); actual species reaction, not an S4 identification |
| Compensating current without a fitted coefficient | Derived (7), with nonlocality, boundary flux and zero modes explicit |
| Same-field bound/free spectral split | Defined, but local interference/projector dynamics prevent treating it as a local independent species (8)-(10) |
| Current rewrite produces canonical response energy | Not established; the exact comparison (11)-(13) exposes its missing matching term |
| Dual partition/gauge freedom selects a physical tether state | No; it is a representation choice until a physical action/state map is supplied |
| Memory closure | Not established: no derived switch that reproduces the required response before and after conversion |

The new useful result is an explicit source-to-compensating-current formula
and its exact action comparison, together with the canonical open-region
test and binding-threshold projector check. Merely asserting that no portal
was found would be weaker. No new fitted parameter, numerical experiment,
or external theorem is used here; all differential, projector and action
identities are derived above within their stated regimes.

Continuation remains open for an actual existing phase/support selector
whose physical constitutive response and current can be matched together.
Removing the medium's allowed variations, introducing an occupation mask,
or assigning a new polarization response only to a selected projector
without that derivation changes the model. A nonlocal spectral description
may be a valid effective reduction with receiver/memory kernels, but it
does not prove the local canonical switch or its lifetime.

Review provenance: author analytic self-review; a separate reconstruction
must pin these final bytes before promoting the scoped results. No full
relativistic stress, nonspherical halo, phase-transition, or quantum
continuum theorem is claimed.
