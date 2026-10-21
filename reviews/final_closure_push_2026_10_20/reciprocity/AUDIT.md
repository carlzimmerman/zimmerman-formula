# Exact-claim audit of the reciprocal source and warm comparison

20 October 2026. Reviewer: separate capture-dynamics subagent in the same team.
Assessment base `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`.

**Normalized claim.** For the specific spherical zero-stiffness instantaneous
energy declared in `SOURCE_RESPONSE.md`, ordinary reciprocal free mass changes
the cold-rest source to `B+F`; a baryon-only tethered density can instead be
stationary if it has suitable warm support. The separate formal point-source
example in `POSITIVE_WARM_COMPARISON.md` admits an everywhere positive isotropic
distribution on positive binding energies, while having infinite total mass
and energy and no established stability.

**Primary verdict: proved as written, within the declared energy and formal
comparison domains.** No failed analytic implication was found. Physical
derivation/admission of that energy, positive finite stock, finite sources,
formation and stability remain unproved inputs; the notes explicitly say so.
This audit does not turn their conditional comparison into a complete physical
candidate or transfer any frozen score to it.

## Revision and independence

The exact proof files reviewed are:

| File | SHA256 |
|---|---|
| `SOURCE_RESPONSE.md` | `6deb1b415ac7f5a1713754ea5526a05b878445fa8d6c7e98888114815401e173` |
| `POSITIVE_WARM_COMPARISON.md` | `ccbe87688c616183da4b3cb602552b362b6188e03ac11bfcae425f5f097b9cbf` |
| original `check.py` | `7f0f36bfc9254ae552200a8263666582d31d89e65d619fe35dc5e2d95448ab81` |

This is a separate-agent reconstruction in a separate working context. The
reviewer had the parent's intended claim and instructions and had discussed
the related capture problem; it is **not a blind or fresh-context audit**.
Neither an actor name nor agreement proves independence from shared model
error. Variations, signs, shell kernels and Abel normalization were derived
directly from the displayed objects, then checked independently symbolically.

## Dependency graph and typed domain

1. Declared reciprocal potential energy on positive regular finite spherical
   profiles; externally fixed baryons allowed where explicitly stated.
2. Material radial variations of enclosed masses -> accelerations.
3. Zero stress on an occupied annulus -> algebraic cold-rest equation.
4. Strict monotonicity of the saturating remainder -> unique admissible root
   and force response.
5. Twice differentiable instantaneous density energy -> symmetric mixed
   response, also on separately mass-conserving perturbations.
6. Isotropic pressure balance -> a necessary warm pressure/virial budget.
7. Separate singular, infinite-stock point-source comparison -> exact Kepler
   force for the selected tether density -> direct Abel inversion -> positive
   stationary collisionless distribution.

The seventh item is a separately labeled formal comparison and does not fall
under the first item's finite regular hypotheses. This distinction is stated
in its opening and limitations and is essential.

## Reconstruction of the energy variations

Write the radial integrand as

    Q=-G[(B+T+F)^2-T^2]/(2r^2)+4pi r^2 W(GT/r^2).

Moving a thin amount `dm` outward by `xi` changes enclosed mass by `-dm` over
the traversed interval. Thus `delta U=-dm xi partial_M Q`, and the acceleration
with outward positive sign is `partial_M Q`. Direct differentiation yields

    a_t=-G(B+F)/r^2+4pi G W'(u),
    a_f=-G(B+T+F)/r^2,
    a_b=-G(B+T+F)/r^2.

There is no missing factor of two, second full-potential contribution, or
tethered self-attraction. The critical `+T^2` term removes only that
self-interaction. The `TF` cross interaction remains in both variations.
This is a valid specified two-population extension; it is not already supplied
by the frozen one-population S2 action.

For `R(u)=u^2/(a0-u)`, `0<=u<a0`, its derivative on `0<u<a0` is

    R'(u)=u(2a0-u)/(a0-u)^2>0.

It rises from zero to infinity, so the cold-rest root at
`s=G(B+F)/r^2>=0` is uniquely

    u=(sqrt(s^2+4a0 s)-s)/2.

With `g=s+u`, direct elimination gives `s=g^2/(g+a0)`. At the baryon-only
root, the residual tethered acceleration is exactly `-GF/r^2`; it cannot
be deleted by retaining a density label. The displayed derivative identities
and the strictly positive extra relaxed response for `F>0` are correct.
At `s=0` the root is zero and the positive-s derivative diverges as stated.
No finite stock, existence of a positive density realizing the root over an
arbitrary interval, or relaxation time follows from this local algebra.

## Reciprocity and separately conserved masses

The Newtonian `TF` cross kernel is symmetric. Directly differentiating the
radial quadratic gives `partial_F partial_T Q=-G/r^2`; the free and tethered
mixed responses coincide. A one-way deletion keeps only one of these entries
and therefore cannot be a Hessian of a twice differentiable instantaneous
energy on that state space.

Separate mass conservation does not remove the test direction. For the
specified zero-mass shell displacements, direct pair energies give

    -G/max(3,4)+G/max(3,2)+G/max(1,4)-G/max(1,2)=-G/6.

The two-dimensional rectangle therefore has nonzero circulation when only
one response is retained. Small smooth shell perturbations around positive
stocks stay in the admissible domain; kernel continuity preserves the nonzero
coefficient. The argument does not rely on injecting or removing total mass.

The statement about eliminating auxiliary fields is valid on a smooth
regular elimination branch of the energy: its reduced Hessian is symmetric.
A stable but singular/degenerate branch is not by itself a guarantee that such
a differentiable reduction exists. The initial audit requested this scope
qualification; the re-pinned source now states it explicitly. This is not a
counterexample to the twice differentiable-energy theorem.
Retarded reductions and momentum-dependent forces lie outside its stated
instantaneous density-energy class.

## Warm support, pressure and virial signs

At the retained baryon-only density the acceleration is `-g_f`. Isotropic
stationarity requires `p'=-rho_t g_f`. The integral pressure in the note is
correct when its outer condition and convergence hold.

Multiplying by `4pi r^3` and integrating over a regular ball gives

    3 integral p dV = 4pi R^3 p(R) + integral r g_f dT.

Since `2K_t=3 integral p dV`, this verifies the boundary sign and scalar
virial expression. For an annulus the boundary contribution includes both
surfaces. Positive pressure is a necessary moment construction, not a
nonnegative distribution or nonlinear stability proof. The note observes
that restriction.

## Positive warm comparison: density and Abel normalization

Differentiating its proposed enclosed mass gives exactly

    rho_t(r)=a0/[2pi G r sqrt(1+4a0 r^2/(G M_b))].

Its `T_b` satisfies the baryon-only remainder equation, so the actual tethered
force from the same energy is `-GM_f/r^2`. Consequently `psi=A/r`, `A=GM_f`,
is the correct relative one-particle potential on this chosen profile. With
`d=A sqrt(4a0/(G M_b))`, the transformed density is exactly

    rho(psi)=C psi^2/sqrt(psi^2+d^2),  C=a0/(2pi G A).

The isotropic density formula follows from `e=psi-v^2/2`:

    rho(psi)=4pi sqrt(2) integral_0^psi f(e)sqrt(psi-e)de.

Its derivative has prefactor `2pi sqrt(2)`. Applying the Abel integral a
second time contributes a factor `pi`, as shown by the sine-squared
substitution. Hence the inverse prefactor is
`1/(2sqrt(2)pi^2)=1/(sqrt(8)pi^2)`, exactly as written. The zero boundary
values remove the extra boundary term here.

Changing variables before differentiating is legitimate for this smooth
density and gives the stated bracket. Independent differentiation gives

    h'/2+psi h''
      =psi(psi^4+d^2 psi^2+6d^4)/[2(psi^2+d^2)^(5/2)]>0.

Every positive binding energy therefore has `f(e)>0`. Since `f` depends only
on conserved energy in the exact static effective force, it is a stationary
collisionless solution. The distribution generates the same density that
was used to obtain that force; an unrelated prescribed potential has not
been substituted.

The asymptotic caveats are also correct. The bracket is `3C psi/d+o(psi)` near
zero and tends to `C/2` at infinity. Its globally bounded positive integrand
justifies the stated dominated-convergence limits after scaling. Thus
`f(e)` behaves as `sqrt(e)` at small positive binding and as `e^(-1/2)` at
large binding; a global increasing-binding monotonicity theorem cannot be
imported. This observation alone does not prove instability.

At large radius `T_b~constant*r`, `rho~constant/r^2` and the supporting
pressure is proportional to `r^(-3)`. Total mass diverges linearly and kinetic
energy logarithmically. The origin is singular because the central sources
are points. The finite-system virial theorem and a finite-energy stability
statement do not apply globally. The comparison remains well-defined on
each compact annulus and proves that the cold-rest obstruction is not a
universal equilibrium obstruction.

## Obligation matrix

| Claim or leaf | Result |
|---|---|
| all three radial material variations | passed |
| canonical full-remainder cold-rest root and force source | passed under the declared energy and zero stress |
| response inequality and derivative range | passed for `s>0`; endpoint handled separately |
| one-way mixed-response deletion is not an instantaneous density energy | passed in the twice differentiable class |
| zero-total-mass perturbations retain the obstruction | passed |
| isotropic pressure and finite-system virial signs | passed with convergent integral/regular boundary hypotheses |
| warm example's density/Kepler self-consistency | passed for its separate fixed point-source comparison |
| Abel inverse normalization and distribution positivity | passed |
| finite source, finite tether stock and total finite energy | not established; the warm comparison explicitly fails these |
| global energy-slope/stability theorem | not established; monotonicity requirement does not hold globally |
| formation, rates, metric and empirical fit of this extension | not addressed |
| physical identification of the declared energy with the original theory | conditional; explicitly a new extension |

## Computation receipt and limitation of the original mutation

The original `check.py` computes quadratic first variations correctly at its
fixtures, but assigns its mixed derivative constants directly. Its deletion
mutation therefore checks that the declared equality fails; by itself it does
not independently reconstruct a changed dynamical force. This does not harm
the analytic proof.

The supplementary `mixed_variation_control.py` was inspected separately. It
reconstructs both mixed entries by exact central differences of the quadratic
energy, evaluates the explicitly deleted-backreaction force, and sums the four
pair-shell kernels. Its stored `mixed_run` is `completed`. This repairs that
specific finite-evidence limitation without changing the original run inputs.

The stored parent records were read: `run_cpu` is completed with 120/120;
`mutation_cpu` is failed by design with 119/120. The initial `run` and
`mutation` remain launch-failed records; they are not mathematical failures.
This audit did not rerun those commands or reinterpret their statuses.

The independent symbolic reconstruction is saved in
`../capture_dynamics/audit_reciprocity.py`,
`../capture_dynamics/reciprocity_audit_checks.json`, and
`../capture_dynamics/reciprocity_audit_manifest.json`. It checks 16 exact
residuals, including direct mixed differentiation and both Abel constants.
The latter v2 manifest validates with `run.status=completed`. Runtime was about
0.49 seconds and observed peak RSS about 58 MB. The proof files' hashes were
unchanged before/after this audit computation. After the source clarified the
auxiliary-elimination scope and audit/mutation provenance, the same 16 checks
were replayed against its new hash (about 0.57 seconds, 58 MB); the conclusions
were unchanged. The initial source hash was
`021d763c079fbe554fefa2acca5c73deff221d5077e5314bc46dc4903d763f41`.

Reproduce from repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 reviews/final_closure_push_2026_10_20/capture_dynamics/audit_reciprocity.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/final_closure_push_2026_10_20/capture_dynamics/reciprocity_audit_manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The exact remaining implication is physical rather than algebraic: construct
one finite, regular, reciprocal carrier model with positive finite stock,
the required stress/energy distribution, admissible interfaces and stable
dynamics, then derive its formation and score its own predictions. The warm
comparison usefully shows why the cold-rest theorem cannot replace that task.
