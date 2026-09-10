# Cross-mass compatibility hierarchy and a common-jet reduction

2026-09-10; base `9a088d45c9c3349de154446aeee4500a84f31c9a`.
Inputs: `../../kgb_joint_action_2026/{joint_static.py,third_mass.py,REPORT.md}`.
This is an exact conditional reduction of the existing inverse equations,
not a numerical mass scan, a new action, or a proof of the full theory.
There is one explicitly dynamical clock field in addition to the metric;
no dark-matter particle field is introduced. No canonical/Dirac degree count
is inferred from the functional compatibility equations below.

The strongest result is a four-variable common-jet reduction, together with
an exact identity relating the first triple-mass determinant to its next
preservation residual. It identifies what an invariant family must satisfy.
It neither proves nor refutes that such a family exists for the prescribed
exponential target and its chosen relativistic completion.

## 1. Domain and definitions

Retain the action `sqrt(-g)[m R/2+P(X)-G(X) box(phi)]`, `m>0`, signature
`(-+++)`, `X=-dphi^2/2`, the static spherical metric and ticking clock
`phi=q t+psi(r)`, and the zero-radial-current exterior branch. Use the same
normalization as `joint_static.py`, including fixed common `|q|=1`.
The symbol **kappa=P_X** below is an action derivative, not the radial clock
derivative `psi'`. It is unrelated to any empirical fitted coefficient.

Take distinct fixed mass parameters `epsilon_i` and a **common open interval
of X** on which all backgrounds are defined. At each X their radii or
accelerations need not agree. Require regular positive `X,y_i,r_i,U_i,B_i,A_i`,
`r_y!=0`, finite coefficients, and nonzero `P_X,W_i,Z_i,h_i`, with all metric
and inverse denominators nonzero. The monotone positive-root matching below
also assumes the intended exterior branch `g_i>0`. Singular `P_X=0` or `Z=0`
limits require the older regular L chart and are not excluded physically by
failure of this chart. Disjoint X domains are not tested by this matching
problem; a claimed universal no-go would need to address that possibility.

For each halo retain the existing functions

```
U_i = q^2/A_i-2X,
h_i = r_i sqrt(B_i U_i)/(2 X Z_i),
W_i = P_X X_i',
a_i = -1/U_i + (2+r_i g_i)/(X Z_i),
b_i = [D_Bi/2 - g_i(2X+U_i)/U_i + 1/r_i
       + (2g_i(2X+U_i)/X + g_i+r_i g_i')/Z_i]/W_i.
```

Here `D_Bi=B_i'/B_i`, radial primes in these background expressions denote
`d/dr_i`, and the functions `r,g,B,Z,W` are precisely those in the input code.
No coefficient is supplied from a stability target.

The state derivative holding kappa fixed as an independent control is

```
D_kappa = partial_X + kappa partial_P
  + sum_i [kappa/(r_yi W_i) partial_yi
           + (-2-2g_i(2X+U_i) kappa/W_i) partial_Ui].
```

The previously derived chain rule is

```
D_kappa h_i = h_i F_i,       F_i = a_i+kappa b_i.
```

This formula uses `log|h_i|` if h is negative; no positive-h restriction is
silently imposed. Its exact symbolic derivation is in the input code.

## 2. Three or finitely many masses

One shared action requires `h_i=h_1`, and preservation requires `F_i=F_1`.
Thus, at each X, every point `(b_i,a_i)` must lie on the same affine line

```
a_i + kappa b_i = s,       s=h_X/h.
```

Set `A_i=a_i-a_1`, `B_i=b_i-b_1`. On a reference chart `B_2!=0`,

```
kappa = -A_2/B_2,
K_i = A_i B_2-A_2 B_i = 0,             i>=3.
```

These are necessary and sufficient for first preservation after h matching.
There are N-2 displayed compatibility residuals for N masses; their
independence is NOT assumed. If every `B_i=0`, then every `A_i` must vanish;
otherwise the first-preservation equations have no solution. If all these
differences vanish, kappa is not fixed at this level and higher preservation
must be examined. Duplicate backgrounds trivially realize such a degeneracy
but say nothing about distinct masses.

The input code uses the equivalent weighted reference formula
`-(h_1 a_1-h_2 a_2)/(h_1 b_1-h_2 b_2)`. On exact h equality it is the same
control. Off that constraint, the weighted formula preserves `h_1-h_2`,
whereas `-A_2/B_2` preserves the ratio. Their vector fields agree on the
constraint manifold. The identities here use the latter for simpler algebra.

Define total background derivatives

```
c_i = D_kappa a_i + kappa D_kappa b_i,
k = kappa_X = P_XX.
```

Then `F_i'=c_i+k b_i`. In particular, the term `k b_i` must not be dropped.
Because `D_kappa=D_0+kappa D_1`, c is quadratic in kappa:

```
c_i = D_0 a_i + kappa(D_1 a_i+D_0 b_i) + kappa^2 D_1 b_i.
```

Next preservation is another affine-line condition, this time on `(b_i,c_i)`:

```
c_i + k b_i = t,       t=s_X,
k = -(c_2-c_1)/B_2,
Q_i = (c_i-c_1)B_2-(c_2-c_1)B_i = 0,  i>=3.
```

On h and first-derivative matching, these are exactly the conditions for
`h_i,XX=h_1,XX`. Thus the existing third-mass test checks the next necessary
condition; it is not merely another value of the same first constraint.

The decisive identity is

```
D_kappa K_i = Q_i + (D_kappa B_2/B_2) K_i.
```

It follows by differentiating the determinant and substituting
`kappa=-A_2/B_2`; no numerical rank or field equation beyond the stated chain
rule is used. Consequently a seed with `K_i=0` but `Q_i!=0` leaves compatibility
immediately. Solving `K_i=Q_i=0` makes it tangent at that point but does not
show that Q remains zero. Differentiating Q and subsequent constraints must
include the full forced-control derivative, equivalently
`D_kappa+k partial_kappa`, followed by higher action derivatives when needed.
Differentiating a substituted feedback expression with the actual state flow
is another correct implementation.

## 3. Why higher independent pointwise jets do not repair this failure

Since `G_X=kappa h`, Leibniz gives

```
G_XX  = k h+kappa h_X,
G_XXX = k_X h+2k h_X+kappa h_XX.
```

If h and h_X already match, then

```
G_XXX,i-G_XXX,1 = kappa (h_XX,i-h_XX,1).
```

The common `P_XXX=k_X` cancels. It cannot repair a failed h_XX compatibility
condition. More generally, if `h_i^(j)=h_1^(j)` for `0<=j<n`, the Leibniz sum
gives

```
G_i^(n+1)-G_1^(n+1) = kappa (h_i^(n)-h_1^(n)).
```

All terms containing higher shared pressure derivatives multiply already
matched lower h derivatives and cancel. This proves the statement at every
order; the symbolic script additionally checks orders n=1 through 6.

## 4. A constructive reduction to four common jet variables

At fixed `(epsilon,y,X,P)`, write

```
alpha=r sqrt(B)>0,      V=X r g>0,
h=alpha sqrt(U)/(2(U-V)).
```

Direct differentiation gives

```
partial_U h = -alpha(U+V)/(4 sqrt(U) (U-V)^2) != 0.
```

Thus a nonzero target h determines a unique U on its sign branch. With
`D=sqrt(alpha^2+16 h^2 V)`, the positive root is
`sqrt(U)=(alpha+D)/(4h)` when `h>0`, and
`sqrt(U)=4|h|V/(alpha+D)` when `h<0`. The unsquared equation selects
`U>V` and `U<V`, respectively. These are the input code's branches.

Now consider the two matching equations for each mass:

```
h_i(y_i,U_i;X,P)=h,
F_i(y_i,U_i;X,P,kappa)=s.
```

If their actual Jacobian

```
J_i = det [[partial_y h_i, partial_U h_i],
           [partial_y F_i, partial_U F_i]]
```

is nonzero, the implicit function theorem determines `y_i,U_i` locally from
the common `(X,P,h,kappa,s)` and the fixed mass. This is an explicit hypothesis,
not an asserted numerical rank. After eliminating U, it is equivalent to a
nonzero y derivative of the remaining F equation: `J_i=-h_i,U * Fbar_i,y`.

For a reference pair with `B_2!=0`, form c from those implicitly reconstructed
backgrounds and integrate the four common quantities by

```
P_X = kappa,
h_X = h s,
kappa_X = -(c_2-c_1)/(b_2-b_1),
s_X = c_1+kappa_X b_1.
```

The reference backgrounds then obey the original state flow automatically.
To see this, differentiate their two matching equations. Subtract derivatives
computed with the original prescribed state flow. The right sides are zero
because `F_i=s` and `c_i+kappa_X b_i=s_X`; invertibility of J forces both
state-derivative differences to vanish. Conversely, an original compatible
reference-pair flow gives this four-variable system.

For any extra mass the same argument works **if and only if** its residual
`c_i+kappa_X b_i-s_X` vanishes along the interval, on this implicit chart.
Its vanishing at a single point is insufficient. This reduced formulation
offers a way to test continuum compatibility without assigning separate
action functions or integrating an independently steered action per mass.

## 5. Invariance and a continuum of masses

On a connected mass interval, after algebraic h matching, first preservation
requires the entire mass curve `(b(epsilon),a(epsilon))` to be an affine line
with mass-independent slope `-kappa` and intercept s. Mass derivatives below
are total derivatives of this matched family, including the induced changes
of y and U, with X fixed. Hence

```
partial_epsilon a + kappa partial_epsilon b = 0.
```

Where `partial_epsilon b!=0`, mass independence of the inferred kappa is
equivalent to

```
(partial_epsilon^2 a)(partial_epsilon b)
 -(partial_epsilon a)(partial_epsilon^2 b) = 0.
```

Next preservation likewise requires `c(epsilon)+k b(epsilon)=t` for the
same k,t at every mass, and subsequent derivatives impose the corresponding
higher conditions. At points where the mass derivative of b vanishes, use
the undivided equations; dividing there would discard possible branches.

An invariant compatible family can exist if the constraint hierarchy closes.
For example, for one additional mass an identity `Q=lambda K` on a relevant
invariant manifold makes the determinant equation homogeneous and preserves
`K=0`. More generally, if a finite collection of actual constraints C obeys
`V C=M C` under the reduced vector field in a neighborhood, uniqueness for
the resulting linear homogeneous constraint evolution preserves `C=0`.
This is a sufficient closure identity to seek, not one proved for the present
exponential completion. A regular constraint manifold with a vector field
tangent everywhere provides the equivalent geometric route.

For an analytic solution germ, vanishing of every X derivative of every
compatibility residual at the seed is sufficient by its convergent Taylor
series. A finite truncation is not. The script includes the abstract analytic
control `h_1=h_2=1`, `h_3=exp(X^3/3)`: h, h_X, and h_XX match at zero but
h_XXX does not. Its data `a_1=b_1=0`, `a_2=-1,b_2=1`,
`a_3=-2+X^2,b_3=2` force kappa=1. This illustrates the hierarchy only; it
is NOT a KGB background counterexample. For a continuum, a neighborhood
uniform in mass additionally requires suitable uniform regularity and
nondegeneracy, not merely separate germs with shrinking domains.

## 6. What freedom is actually available

The action initially contains two common functions, P and G, equivalently
P and nonzero h on this chart, plus G's irrelevant additive boundary constant.
The scalar clock remains a propagating field; this function count is not a
physical mode count.

For fixed masses and fixed X_0, under the stated nonzero implicit Jacobians,
h and F matching leave the four common initial quantities
`P_0,h_0,kappa_0,s_0`, together with discrete local root-branch choices.
The reference pair then fixes their evolution. No freely adjustable function
of X remains for independently steering additional masses. Extra masses
supply N-2 next-preservation residuals, followed by their hierarchy; their
rank or dependence must be derived, never inferred just by counting them.
Likewise, for a smooth continuum the initial functions `y_0(epsilon),
U_0(epsilon)` are locally fixed by those common jets wherever the implicit
Jacobian is nonzero. A different branch or a degenerate Jacobian requires
a separate analysis and may change this description.

Tuning common initial data could place a solution on an invariant compatible
subset; the determinant identities do not forbid it. Matching finitely many
jets cannot establish it. If the hierarchy does not close for the selected
completion, the missing freedom is an invariant relation or a permitted
change of the imposed background/boundary problem, not a separately chosen
P_XX or P_XXX per halo. A universally specified higher-order metric completion
could change the equations, but has not been introduced or justified here.
Adding radial shift current is not a free static-exterior escape: the ticking
clock's energy flux is proportional to q J^r, while a diagonal static metric
with no compensating matter flux requires that flux to vanish.

Neither local compatibility nor an invariant family would finish the physical
theory. Baryonic source matching, common cosmology, global regularity, local
and global stability, and the measured gravitational normalization remain
separate requirements for the SAME functions P and G.

## 7. Exact checks and reproducibility

`test_structure.py` checks eight exact symbolic statements: signed matching
and h_U, first determinant, determinant tangency, total-derivative terms,
implicit Jacobian, higher pressure-jet cancellation through n=6, the analytic
finite-jet counterexample, and the continuum mass-curvature identity. All
eight pass. No numerical mass samples or numerical matrix ranks are used.

`CompatibilityAlgebra.lean` checks three real algebraic theorems: the first
determinant, the denominator-cleared tangency identity, and cancellation of
the common higher pressure derivative. It does not formalize the physical
coefficient map, an invariant manifold, the implicit function theorem, or
an ODE solution. Its checked axioms are recorded by `#print axioms`.
All three proofs pass using only `propext`, `Classical.choice`, and `Quot.sound`;
there is no `sorryAx`.

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/test_structure.py
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean "$PWD/qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/CompatibilityAlgebra.lean"
```

Environment: Python 3.9.6, SymPy 1.14.0; Lean 4.34.0-rc2 and the existing
Mathlib revision `85e3a25e006c35636f0e53b0e9296caca2685bc0`. No randomness.
The bounded rerun in `run_001/manifest.json` records the exact commands,
before/after input hashes, dirty state, elapsed time, and preserved stdout and
stderr. It passed with a 60-second wall timeout and 1 MiB combined log cap;
no memory, CPU-time, affinity, or numerical-thread caps were requested.
Manifest validation includes current input hashes against the repository root.
Only this structure directory was written; no commits were made.
