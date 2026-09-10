# Vacuum scaling and the common-action search

Base: `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`. This is a conditional exact
scaling audit of `kgb_universal_clock_2026/structure/closed_inverse.py`, with
the local EF principal normalization checked against the existing dictionary
and coupled KGB principal expression. No old files or empirical parameters
are changed; no new theory or measured Newton constant is claimed.

## Overall F amplitude is redundant for these vacuum zeros

Fix both mass labels, their target geometries, the common X, and the U_i.
For one constant s>0, simultaneously transform every halo and every shared
action jet by

\[
 (F,w_i,f,j)\longmapsto s(F,w_i,f,j),\qquad f=F_X,\ j=F_{XX}.
\]

This corresponds to multiplying the complete vacuum action by s: the new
functions are sF(X), sP(X), sG(X), with one common transformation for every
mass. The irrelevant additive boundary constant of G may be fixed consistently.

| Quantity | Multiplicative factor |
|---|---:|
| P, W=dw/dr, P_X, G_X, P_XX, G_XX | s |
| kappa=P_X/f, Gamma=G_X/f, H, Rrad | 1 |
| X'=w/f, X'', physical metric and clock background | 1 |
| Dcoord=1+rw/(2F) | 1 |
| Dfield=2(F-Xf) | s |
| A=L0 Delta(kappa,Gamma) | 1 |
| B=L1 Delta(kappa,Gamma) | 1/s |
| E=A+fB, N=(L0+fL1)E with f fixed | 1 |
| Required common j, when determined | s |
| det(N,B), det(A,B) | 1/s |

The operator identities explain the higher-derivative rows. Let T_s be the
state scaling and let its Euler vector field be
\(\mathcal E=F\partial_F+\sum_i w_i\partial_{w_i}\).
Direct coefficient differentiation gives

\[
 [\mathcal E,L_0]=0,\qquad [\mathcal E,L_1]=-L_1.
\]

Thus a scale-invariant normalized jet has scale-invariant L0 derivative and
L1 derivative of degree -1. Including f->sf makes L0+fL1 equivariant, so E and
N remain invariant. No commutation of L0 with L1 is assumed. In particular,
the equation N+jB=0 and all its zero-control cases are preserved. For a
nonzero B component, j_required=-N_component/B_component scales by s.

Consequently, the overall F amplitude cannot cure a failed first or next
preservation determinant. A vacuum search may fix one positive F reference
and use w_i/F, f/F, j/F as amplitude-invariant coordinates. This quotients
only the simultaneous amplitude direction, not independent changes of F
while w,f or the reconstructed P/G functions are held fixed.

## Local health normalization

Hold the EF constant Ricci coefficient m fixed. C=2F/m scales by s; the
physical metric and scalar background remain the same, while the EF metric
undergoes a constant conformal scaling. The existing dictionary gives

\[
 (\widetilde P,\widetilde P_\chi,\widetilde P_{\chi\chi},
   \widetilde G_\chi,\widetilde G_{\chi\chi})
 \longmapsto
 (s^{-1}\widetilde P,\widetilde P_\chi,s\widetilde P_{\chi\chi},
   s\widetilde G_\chi,s^2\widetilde G_{\chi\chi}),
\]

and the EF orthonormal scalar gradient/Hessian scale by s^(-1/2), s^(-1).
Substitution into the original coupled principal expression shows its whole
orthonormal matrix is unchanged; its stress matrix scales by 1/s. Hence the
implemented kinetic, radial, angular, cross, and strict-cone tests, including
their zeros, are invariant. The common allowed j interval scales by s.
This proves invariance of the existing local diagnostic, not a new physical
Hamiltonian, matter, strong-coupling, or global health certificate.

The full sourced problem is not invariant when S_m is held fixed: multiplying
only the vacuum action changes its normalization relative to matter. The
eventual source matching and measured-G_N calibration must therefore restore
the chosen amplitude. No empirical G_N scaling law is inferred here.

## Clock rescaling needs an explicit change of normalization

There is a useful algebraic covariance at t>0:

\[
 (X,U_i)\mapsto t(X,U_i),\quad (F,w_i)\mapsto(F,w_i),\quad
 f\mapsto f/t,\quad j\mapsto j/t^2.
\]

It sends P,W,kappa to themselves, Gamma to Gamma/sqrt(t), H to sqrt(t)H,
and X',X'' to t times themselves. At the action level it corresponds to
the field redefinition phi_new=sqrt(t) phi and

\[
 F_{\rm new}(\xi)=F(\xi/t),\quad
 P_{\rm new}(\xi)=P(\xi/t),\quad
 G_{\rm new}(\xi)=t^{-1/2}G(\xi/t).
\]

But that field redefinition also changes q to sqrt(t)q if the physical metric
and time coordinate are fixed. In the current q=-1 chart, Q=2X+U=1/A.
Scaling X,U while keeping q=-1 therefore requires A_new=A/t. Keeping A
unchanged instead leaves a clock-norm mismatch (t-1)(2X+U)/2, which vanishes
only at t=1 on Q>0. One may compensate with a global time-coordinate change
only if the boundary time/lapse normalization is also allowed to change.

Thus the displayed clock covariance is not a symmetry of the simultaneous
fixed-q, fixed-normalized-lapse problem. It is not used here to eliminate X0
or to count changes of X0 as independent physical controls. A shared global
clock normalization would need to be specified before making that reduction;
per-mass clock rescalings do not preserve one shared action.

## Reproduction and exact scope

Run from this directory with `python3 -B test_scaling.py`, or invoke its full
repository-relative path from the repository root. The eight tests use exact
SymPy arithmetic; there is no numerical scan. They check the closed inverse
homogeneity, the Euler/operator identities that propagate it, control and
determinant scaling, the existing EF dictionary and principal matrix, and
the fixed-q clock-normalization obstruction. All assumptions include the
original regular chart: m,F,X,U,B>0, f,w,ry nonzero, Dfield nonzero, and the
chosen positive areal orientation. Negative nonzero Dfield remains allowed.

`PositiveScaling.lean` separately proves two conditional arithmetic statements:
both control equations are unchanged under A,N invariant, B->B/s and
(f,j)->s(f,j), and det(N,B/s)=0 iff det(N,B)=0 for s>0. The same determinant
lemma applies with A in place of N. These are not action-variation or Dirac
theorems. Compile using the existing environment:

```sh
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_joint_tangency_2026/scaling/PositiveScaling.lean
```

The explicit `#print axioms` commands report each lemma separately. Validation:
eight exact tests passed with Python 3.9.6 / SymPy 1.14.0; both Lean lemmas
compiled with Lean 4.34.0-rc2 and axioms [propext, Classical.choice, Quot.sound].
No admissions or additional axioms were introduced. The parent bounded run
should pin these four files plus the three pre-existing input modules named
above and the existing Lean environment. Mathematical self-review covered all
four newly created files; no prior mathematical convention was changed.
