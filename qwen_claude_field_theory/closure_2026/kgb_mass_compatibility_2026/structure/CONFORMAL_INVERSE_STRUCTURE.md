# Affine conformal inverse: independent structural audit

2026-09-10; base `9a088d45c9c3349de154446aeee4500a84f31c9a`.
The frozen `../conformal_inverse.py` SHA-256 is
`d8629d79b04cac4b60c24187134d23580c93314b6a687d4d8df2cc1551a720f5`.
Only this structure directory was written; no root or legacy implementation
was edited, and no commit was made.

**Verdict:** the implemented pressure-chart 2x2 equations have the correct
signs and factors. Their action-curvature derivatives are total derivatives
along the actual fixed-mass flow. The angular equation is assembled from the
variation, not assigned its target value, but is an exact consequence of the
three solved equations. It is a consistency check, not an independent gate.
The pressure fold can be removed with a gradient-state 3x3 inverse; zero
gradient at positive target density is a different, conditional obstruction.

## Equations and assumptions

Use the action and conventions independently checked in
`DERIVATIVE_CURVATURE_VARIATION.md`: signature (-+++),
`F(X)R+K(X)(grad X)^2+P(X)-G(X)box(phi)`, and total radial current zero.
Here `F=(1+sigma X)/2` is the entire Ricci coefficient,
`f=F_X=sigma/2`, `K=3f^2/(2F)`, `K_X=-3f^3/(2F^2)`.
Set

```
g=A'/(2A), B=1+2rg, b=B'/(2B), B'=2g+2rg',
z=X', p=psi', U=p^2/B, Q=2X+U=q^2/A, a=g+2/r,
Z=U/X-rg, Cj=2XZ/(pr).
```

The exterior radial geometric pressure is zero. Assume smooth fields and
finite coefficients, regular static coordinates, and nonzero displayed
denominators. Physical chart conditions used for invertibility are
`F>0, X>0, U>0, B>0, r>0, p!=0, f!=0`; the code chooses `p=sqrt(BU)`.
The mixed metric identity requires `q!=0` and no ordinary-matter radial flux.
In particular it enforces TOTAL current zero, not the old KGB current alone.

Define the radial algebraic pressure and its derivative data by

```
Pcal(r,g,F,z) = [2fza+Kz^2]/B,
Pz = partial_z Pcal = (2fa+3f^2 z/F)/B,
R0 = partial_r Pcal + g' partial_g Pcal + fz partial_F Pcal.
```

All partial derivatives hold the other displayed arguments fixed. The
geometric density and angular pressure are

```
rho=(1-1/B)/r^2+B'/(B^2 r),
pt=[g'+g^2-gb+(g-b)/r]/B.
```

Put

```
Achi = f(rho-2pt)-K_X z^2/B-2K(g-b+2/r)z/B,
Lbase = 2F rho+Pcal-2f(2/r-b)z/B+Kz^2/B.
```

Radial preservation, total current, and density give the exact linear system
for `v=(z',kappa,gamma)=(X'',P_X,G_X)`:

```
M3 = [[ Pz,    -z,  0       ],       rhs = [-R0,
      [-2K/B,   1, -Cj      ],              -Achi,
      [ 2f/B,   0,  2Xz/p   ]]              Lbase].
```

This is the explicit gradient-state inverse. It does not divide by Pz.
The current row follows from `P_X+E_chi=Cj G_X`, with
`E_chi=Achi-2Kz'/B`; the density row follows directly from the full lapse
variation. These facts independently fix the signs of all three rows.

## Determinants and the pressure fold

Eliminate the first row using `s=z/Pz`, `o=-R0/Pz`, `z'=o+s kappa`.
The implementation's matrix and right side are exactly

```
M2 = [[1-2Ks/B, -Cj   ],        rhs2 = [-Achi+2Ko/B,
      [2fs/B,    2Xz/p]]                 Lbase-2fo/B].
```

Exact SymPy factorization gives

```
Rrad = a+3fz/(2F),             Rrad^2=a^2+3BPcal/(2F),
det(M3) = 4fzQ/(Bpr),
det(M2) = 2zQ/(pr Rrad),       Pz det(M2)=det(M3).
```

On the GR-connected pressure root, `Rrad` is the positive square root in
the source implementation. The stable root formula there is
`z=BP/[f(a+sqrt(a^2+3BP/(2F)))]`.
The eliminated chart requires `Pz!=0`; at the fold

```
zfold=-2Fa/(3f), Pz=0,
det(M3)|fold=-8FaQ/(3Bpr).
```

Thus the 3x3 remains invertible at the pressure fold when `FaQ/(Bpr)!=0`.
This is a chart failure, not a solution obstruction. Also `Z=0` is not a
determinant singularity in this enlarged inverse. The conditional Lean matrix
theorem proves invertibility from the determinant formula and the listed
nonzero/positive assumptions; SymPy, not Lean, checks the formula itself.

## Angular equation: exact dependence

Let `R1,R2,R3` be the components of `M3 v-rhs`, and let the full angular
Euler residual, after using `P=Pcal`, be

```
Eang=2Fpt-Pcal-G_X pz/B
     +2f[z'+(g-b+1/r)z]/B-Kz^2/B.
```

The exact identity is

```
Eang = (r/2)R1+(rz/2)R2-(rg/2)R3.
```

Both its derivative coefficients and constant term are checked separately,
without solving either matrix. Consequently a small angular residual is
useful for catching inconsistent assembly, but cannot provide a fourth
independent field-equation constraint once the inverse rows vanish.

## Zero-gradient obstruction and its limits

At `z=0`, the radial equation gives `P=0`, and `R0=0`. If `fa/B!=0` and
`P_X` is finite, differentiating the radial equation forces `z'=0`.
The density equation then reduces to `2F rho=0`, provided `G_X` is finite.
For `F!=0`, any strictly positive density is incompatible with such a point.
Lean proves this conditional algebra and its positive-density contradiction.
It does not exclude singular action coefficients or a failure of these
regularity assumptions.

For the exponential target, `mu=1-exp(-y)`,
`lambda=mu+y exp(-y)`, `r_y=-r lambda/(2y mu)`, and
`B=1/(1-2*r*y)`. Exact substitution into the geometric density gives

```
rho = 4y^2 exp(-y)/[r(1-exp(-y)+y exp(-y))].
```

SymPy checks this reduction. Lean proves it is positive for every finite
`y>0,r>0`, using `0<exp(-y)<1`. There is no fixed positive lower bound asserted
in the Newtonian `y -> infinity` limit; finite coefficients are essential to
the zero-gradient statement.

Do not replace this statement by a blanket prohibition of `P=0`. The other
radial quadratic root is `z=-4Fa/(3f)`, where `Pcal=0` but
`det(M3)=-16FaQ/(3Bpr)` can be nonzero. It is distinct from the GR-connected
zero-gradient root and can be approached after passing the pressure fold.

## Total derivatives, reproducibility, and scope

At fixed mass epsilon the implemented pressure-state radial direction is

```
(y',X',U',P')=(1/r_y,z,-2gQ-2z,P_X z).
```

Therefore the source's directional derivatives divided by z really give
`P_XX=(dP_X/dr)/z`, `G_XX=(dG_X/dr)/z`, locally where its analytic chart is
regular and `z!=0`. This is not independent second-derivative steering.
The bounded numerical test solves the independently assembled unsimplified
3x3 and differentiates it instead in coordinates `(y,X,U,z)`, using direction
`(1/r_y,z,-2gQ-2z,z')`. It compares both complex-step and real central
differences with the root implementation at exactly three seeds
`(epsilon,y,sigma,bscale,dscale)`:

```
(1e-6, .1, .1,   .25, 1.),
(1e-6, 1., .001, .75, .5),
(1e-6, 2., .1,  1.25, 1.5).
```

These are floating-point controls, not universal analytic error bounds or
independent verification of the target metric. The algebraic determinant,
angular dependence, and density reduction tests are exact. All seven Python
tests and five Lean theorems passed in the recorded run. Lean lists only
`propext`, `Classical.choice`, and `Quot.sound`; no `sorry` axiom is used.

From the repository root, the direct check is

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/test_conformal_inverse_structure.py
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/ConformalInverseAlgebra.lean
```

`inverse_contract.json` states exact scope, tolerances, seeds and non-claims.
`inverse_run_001/manifest.json` records exact argv, all selected source hashes
before/after execution, software versions, runtime and log hashes. It pins the
frozen root hash above and its imported project files. The combined run used
a 60-second wall timeout and 1 MiB output cap, no randomness or further
resource caps. Manifest validation against current inputs passed. Runtime:
Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4, Lean 4.34.0-rc2,
Mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

For one smooth profile with `z!=0`, radial preservation provides local
integrability of P and one can integrate `G'=G_X z`. Replacing a coordinate
chart does not establish that different masses reconstruct the SAME functions
on overlapping X intervals. That still requires equality and preservation of
the common action data. Nothing here proves a mass-universal trajectory,
global continuation, boundary/source matching, a degree count, Hamiltonian
boundedness, a physical causal cone, PPN, cosmology, or a complete MOND theory.
This checkpoint uses the proof-audit, computation-audit, mathematical
proofreading, and verification-before-completion skills for its stated audit.
