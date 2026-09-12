# Constructive repair of the small-counterflow instability

Continuation from the calculation in `REPORT.md`, with its committed files
now contained in `9b97161a6`. The shared worktree HEAD at this continuation
was `056a4159e`. No other agent's files are modified.

**New result:** a complete explicit *current-sector* master function preserves
exact coflow dust, has positive spatial-current inertia at all positive
comoving densities, and repairs the previous negative low-velocity energy
eigenvalue near every equal-density state. Two finite-velocity states have
exact all-angle positive-energy, subluminal scalar spectra. This is a
construction with derived equations and constraints, not a fitted kick rule.
It is still not a complete MOND gravity theory. The full state space contains
failures, and the next stress calculation gives tension rather than recoil
pressure.

## Action, fixed before testing

Keep the definitions and variational conventions of `REPORT.md`. Write the
relative-current invariant as `Rrel` to distinguish it from Ricci curvature:

\[
 S_J=E_*\int\sqrt{-g}\,[j_1^\mu\partial_\mu\theta_1
                  +j_2^\mu\partial_\mu\theta_2+F]d^4x,
\]
\[
 F=-n_1-n_2+f(n_1,n_2)R_{\rm rel},\quad
 R_{\rm rel}=-j_1\cdot j_2-n_1n_2,\quad D=(n_1+n_2)/2,
\]
\[
 \boxed{f(n_1,n_2)=D^p\exp[-b(n_1-n_2)^2/D^2]-\frac1{2D},
          \qquad 0<p<1,\quad b>\frac14.}
\]

The representative uses `p=b=1/2`. These values select an interior point of
inequalities; they are not derived fundamental numbers and are **unrelated to
the fitted kappa=1/2** in the acceleration relation. Density and energy units
remain unspecified physical inputs. This exponential regulates density
contrast and does not derive or replace the MOND interpolation function.

The family was obtained by solving conditions on the current Hessian, rather
than reconstructing a prescribed cosmological expansion. Each current obeys
`nabla_mu j_A^mu=0` and `partial_mu theta_A+partial F/partial j_A^mu=0`.
The Hilbert tensor and Ward identities in `REPORT.md` apply with this `F`.
`stress_gate()` independently differentiates this invariant master function.
The theory is conservative and carries two actual field matter modes. No
microscopic particle, decay rate, or entropy production is assumed.

## Why the old low-velocity obstruction is repaired

At coflow the interaction and its first derivatives vanish, for arbitrary
positive `n1,n2`. The sector remains pressureless on FLRW, with
`rho_J=E_*(n1+n2)` and `a^3 n_A` conserved. No claim about CMB anisotropies
or a full MOND cosmological solution follows from that background statement.

For one spatial direction, write the current perturbations as `delta j_A=n_A x_A`.
Their quadratic inertia form is

\[
 Q=n_1x_1^2+n_2x_2^2+f n_1n_2(x_1-x_2)^2,
\]
\[
 (n_1+n_2)Q=(n_1x_1+n_2x_2)^2
    +[1+(n_1+n_2)f]n_1n_2(x_1-x_2)^2.
\]

Here `1+(n1+n2)f=2D^(p+1)exp[-b(n1-n2)^2/D^2]>0`. Thus `Q>0`
for every nonzero perturbation and every positive pair of coflow densities.
Lean checks the square identity and the conditional positivity implication.

Now take equal proper densities `n1=n2=n` and opposite small velocities
`+v,-v`. Differentiate the action first and then expand. The two eigenvalues
of the temporal current Hessian, divided by `v^2`, approach

\[
 \boxed{\lambda_{\rm common}=n^p p(p-1),\qquad
        \lambda_{\rm contrast}=(2-8b)n^p.}
\]

Both are strictly negative under the displayed parameter inequalities. The
coflow spatial-current eigenvalues are `1/n` and `2 n^p`, both positive.
For each fixed `n>0`, smoothness therefore provides a sufficiently small
nonzero counterflow neighbourhood with negative temporal and positive spatial
Hessian blocks, giving positive reduced quadratic energy by the Schur argument.
This is not a uniform bound as `n->0` or `n->infinity`, and the exactly
comoving density reduction is still degenerate dust. Strong coupling, caustics
and a nonlinear invariant domain have not been settled.

## Exact finite witnesses and actual constraints

At `n1=n2=1`, the representative is tested exactly at `v=1/1000` and `v=1/10`.
At both points the Hessian block signs give positive energy, and exact positive
Bernstein coefficients prove the two squared wave speeds lie in `(0,1)` for
every direction. The complete polynomial at `v=1/10`, with
`u=(omega/|k|)^2`, `t=cos(angle)^2`, is

\[
 \boxed{271744257575u^2+(5507190570t-10325099400)u
        +28933981t^2-87987570t+66891825=0.}
\]

`DensityRepair.lean` certifies this all-angle root bound and its positive
discriminant. A test checks that the formalized polynomial is the one actually
derived from the new action. The exact `v=1/1000` coefficients are also recorded
with their Bernstein certificate in the machine-readable result.

At `v=1/10`, the actual Poisson calculation gives 10 primary and 6 secondary
constraints, rank 16 and two current-field canonical pairs for `k=0`.
Keeping both Fourier quadratures for `k=1` gives 20 primary and 12 secondary,
rank 32 and four canonical pairs across the two quadratures. No first-class
current constraints or free multipliers remain. Preservation is solved on
the computed constraint nullspace. These are current-sector quadratic results,
not the nonlinear metric-clock-current Dirac algebra.

The bounded numerical screen uses 5 mean densities, 5 ratios, and 5 velocities:
125 physical states of this **one** representative. 34 have positive energy
and pass the sampled null-symbol diagnostic. This is not a percentage reduction
of theory parameter space. Equal-density low-velocity states survive across
the five decades tested; unequal densities and larger velocities expose
failures. At `n1=n2=1`, `v=3/5`, the exact spatial-current Hessian includes
`-5/256` and `-985/1024`, so this high-velocity state fails the energy gate.

## Next gate actually calculated: stress and redistribution

Varying the same action gives the generalized pressure

\[
 \Psi=F-n_1F_{n_1}-n_2F_{n_2}-2sF_s
 =-(1+p)D^p\exp[-b(n_1-n_2)^2/D^2]R_{\rm rel}.
\]

This is not itself isotropic physical pressure in a counterflow. Calculate
the physical tensor components in the equal-density counterflow frame. To
leading order in `v`, in the normalized units:

\[
 P_\parallel=2(1-p)n^{p+2}v^2+O(v^4),\quad
 P_\perp=-2(1+p)n^{p+2}v^2+O(v^4),
\]
\[
 \boxed{\operatorname{tr}P=(-2-6p)n^{p+2}v^2+O(v^4)<0
          \quad\text{at sufficiently small nonzero }v.}
\]

Lean checks the sign of the leading coefficient. This **does not reproduce**
the positive isotropic stress injection `rho Gamma vk^2 delta_ij/3` from the
C003 kick rule. The derived low-velocity anisotropy relation
`P_perp/P_parallel=-(1+p)/(1-p)` is a conditional constitutive prediction; it
is not yet an observational halo prediction or a novelty claim.

For a radially oriented counterflow, constant local `v`, and `n proportional
to r^-s`, the leading outward stress-force coefficient is

\[
 -\partial_rP_{rr}-\frac{2(P_{rr}-P_{\perp})}{r}
 =\frac{n^{p+2}v^2}{r}\{2(1-p)(p+2)s-8\}+O(v^4).
\]

For `p=1/2`, `s=2` this is `-3 n^(5/2) v^2/r`, inward. A sufficiently
steep profile has another sign, but no self-consistent halo profile or
depletion history has been obtained. Positive local wave energy cannot be
substituted for this force calculation.

## Scope and next work

The concrete advance is a **derived cold-background/healthy-low-counterflow
construction**, repairing the previous action's exact small-velocity defect.
It does not establish that the dust leaves galaxies, remains in clusters,
or supplies viable CMB perturbations. It has not been combined with a verified
MOND metric sector, so lensing, PPN, gravitational DOF and gravitational-wave
requirements remain open at the full-theory level.

The next necessary construction must supply the required redistribution
stress while preserving these positive energy conditions, or show that the
derived anisotropic stress produces depletion in a coupled evolution. The
state-domain boundaries and the zero-flow/zero-density limits must be handled
alongside that calculation. No adjustment of p or b is a derivation of kappa.

Carl Zimmerman's field/clock and no-new-particle requirements motivated this
repair. Entrainment and variational current theories are prior work, as cited
in `REPORT.md`; the family is a newly explored construction in this repository,
without an exhaustive priority/novelty search.

## Reproduction

```sh
python3 -B qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/density_repair.py --result /tmp/density_repair_result.json
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/entrained_current_construction_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/check_lean.py --source qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/DensityRepair.lean
```

`repair_run_001/manifest.json` records exact commands, source/result hashes,
limits and exit status. The final suite includes both actions' regression
tests and both Lean files. It does not count the documented physical failures
as successful theory gates merely because the audit suite exits zero.
