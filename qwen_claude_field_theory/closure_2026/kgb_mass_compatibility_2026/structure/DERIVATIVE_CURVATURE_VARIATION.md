# Independent check of the derivative-curvature static equations

2026-09-10, base `9a088d45c9c3349de154446aeee4500a84f31c9a`.
**Verdict: the proposed covariant, density, and angular formulas are correct**
under the conventions below. This checks action variation and static equations,
not PPN, degeneracy, propagating modes, or stability of the enlarged action.
Only this structure directory was written; this audit changed no extension or
root file.

Take

```
S = integral sqrt(-g) [F(X)R+K(X)(grad X)^2+P(X)-G(X)box(phi)],
X = -(grad phi)^2/2,        signature (-+++).
```

F denotes the **entire coefficient of R**. If an additional `mR/2` is retained,
replace every `2F` multiplying an Einstein component below by `m+2F`.
The derivation holds for any differentiable K; the particular
`K=3 F_X^2/(2F)` can be substituted afterward and requires `F!=0`.

## Auxiliary variation and the current

Introduce independent chi with the equivalent constrained action contribution

```
F(chi)R+K(chi)(grad chi)^2+lambda(X-chi).
```

With compactly supported variations, its chi equation gives

```
lambda = E_chi = F_X R-K_X(grad X)^2-2K box(X),       chi=X.
```

The two K_X contributions from differentiating the kinetic momentum explain
the minus sign. Variation with respect to the inverse metric then gives

```
E_F,mu,nu = F G_mu,nu+(g_mu,nu box-nabla_mu nabla_nu)F
            +K X_mu X_nu-g_mu,nu K(grad X)^2/2
            -E_chi phi_mu phi_nu/2.
```

Here `E=delta S/(sqrt(-g) delta g^(mu nu))`; the KGB contribution is
`-T_KGB,mu,nu/2`, using the action-derived stress already checked in the base
work. The on-shell multiplier Lagrangian vanishes, while its metric chain term
does not. Scalar variation of `lambda X` gives `div(lambda grad(phi))`.
Consequently

```
J_total^mu = (P_X+E_chi-G_X box(phi)) grad^mu(phi)-G_X grad^mu(X).
```

For `ds^2=-A dt^2+B dr^2+r^2 dOmega^2`, `phi=q t+psi(r)`, `p=psi'`, and
static X, every non-chain derivative-curvature term has zero mixed rt
component. Direct variation/stress contraction gives the off-shell identity

```
E_total^r_t = -q J_total^r/2.
```

Thus `q!=0` and the static mixed metric equation imply **total** `J^r=0`.
They do not imply the old KGB current vanishes separately. This conclusion
assumes no compensating ordinary-matter energy flux; a matter flux contributes
its own `-T_m^r_t/2` to the metric equation.

## Independent static diagonal equations

Define `g=A'/(2A)`, `b=B'/(2B)`, `x=X'`, `z=X''`. Then

```
box(X) = [z+(g-b+2/r)x]/B,
F' = F_X x,
box(F) = [F_X z+F_XX x^2+(g-b+2/r)F_X x]/B.
```

The relevant Hessian components are
`nabla_tt F=-Ag F'/B`, `nabla_rr F=F''-b F'`, and
`nabla_theta,theta F=r F'/B`; the script derives these from the connection.
Use `q^2/A=2X+p^2/B` and, on total zero current with `p!=0`,

```
P_X-G_X box(phi) = G_X x/p-E_chi.
```

The E_chi terms in the time and radial equations cancel exactly between the
metric chain term and the KGB stress. The resulting vacuum-exterior equations
are

```
2F rho_geom = 2[F_X z+(F_XX-K/2)x^2+(2/r-b)F_X x]/B
               +2X G_X x/p-P,

2F pr_geom = P-2(g+2/r)F_X x/B-K x^2/B,

2F pt_geom = P+G_X p x/B-2[box(F)-F'/(Br)]+K x^2/B.
```

These reproduce both proposed formulas, including every sign and factor of
two. The angular expression itself does not need the zero-current substitution,
because phi and X have no angular derivatives. The geometric components are

```
rho_geom=(1-1/B)/r^2+B'/(B^2 r),
pr_geom=(1/B-1)/r^2+2g/(Br),
pt_geom=[g'+g^2-gB'/(2B)+(g-B'/(2B))/r]/B.
```

Ordinary-matter density and pressures, when present, add to the corresponding
right sides. For constant F and K=0 these equations reduce to the earlier KGB
zero-current identities with `m=2F`, an independent normalization control.

## Useful elimination identities for the next inverse

The radial equation can be solved algebraically, provided `2F+r^2P!=0`:

```
B = [2F(1+2rg)+2r^2(g+2/r)F_X x+r^2K x^2]/[2F+r^2P].
```

Multiplying the density and angular equations by B and moving their right
sides left, the coefficient determinant for unknowns `(B',X'')` is

```
2F F_X(1/r-g)/B.
```

Thus that particular elimination needs `F F_X(1-rg)!=0`; a zero determinant
means a different algebraic chart, not physical nonexistence. Their sum cancels
`X''`, `F_XX`, and K identically:

```
(1/r-g)[F B'/B-2F_X x]
 +2F[(B-1)/r^2+g'+g^2+g/r]
 -G_X x(2BX/p+p) = 0.
```

For `F=F0+alpha X`,

```
K=3alpha^2/(2F),
E_chi=alpha R+3alpha^3 x^2/(2F^2 B)-3alpha^2 box(X)/F.
```

The scalar-current relation now involves `P_X+E_chi`; neither the old
`G_X/P_X` matching formula nor the old KGB principal matrix can be carried
unchanged into this enlarged action. The diagonal equations above do not
remove the obligation to enforce the total-current relation and reconstruct
one common set of action functions.

## Checks and scope

`test_derivative_curvature_variation.py` contains eight exact SymPy checks:
auxiliary chi variation; metric chain/current sign; F Hessian from the metric
connection; the mixed-current identity; all three diagonal equations; the
constant-F control; radial B elimination and the highest-derivative determinant;
and the linear-F auxiliary equation. No numerical samples or external PPN
formulas enter these checks.

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/test_derivative_curvature_variation.py
```

All eight checks passed in Python 3.9.6 / SymPy 1.14.0. The recorded bounded
rerun also passed; `variation_run_001/manifest.json` preserves exact argv,
input hashes before and after execution, runtime, and stdout/stderr hashes.
It used a 60-second wall timeout and a 1 MiB log cap, with no numerical samples,
randomness, or additional resource caps. The manifest validates against the
current repository input hashes.

The derivation requires smooth fields, the stated variation convention, finite
coefficients, nonzero p for the displayed current elimination, and regular
static coordinates. It makes no new claim about a universal MOND solution,
mode degeneracy, ghosts, cosmology, or source matching.
