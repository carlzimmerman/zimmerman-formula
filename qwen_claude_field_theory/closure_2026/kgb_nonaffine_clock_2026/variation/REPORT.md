# Non-affine clock inverse: exact reduction and local control

2026-09-10; base `583fdf69a597ef9ed57b4f9ced48dd457c8ef2de`.
This independent lane writes only `kgb_nonaffine_clock_2026/variation/`.
No previous checkpoint or root implementation was edited; no commit was made.

Verdict: the static inverse, control cancellation and restricted local cone
criterion are established under the conditions below. The primary kinetic
block is degenerate. This does not establish a complete Dirac count, global
mass-compatible action, physical nonlinear stability or full MOND theory.
The source/mass and global-parameter restrictions are in `GLOBAL_SOURCE.md`.

## Claim, dependencies and domain

Start with the same single-clock action, not an extra particle sector:

```
S = integral sqrt(-g) [F(X) R + K(X)(grad X)^2 + P(X)-G(X)box(phi)],
X=-(grad phi)^2/2, K=3F_X^2/(2F), signature (-+++).
```

F is the entire Ricci coefficient. Define jets `f=F_X`, `j=F_XX` and
`K_X=3fj/F-3f^3/(2F^2)`. The earlier independently varied general-F equations
are recorded in
`../../kgb_mass_compatibility_2026/structure/DERIVATIVE_CURVATURE_VARIATION.md`.
They follow by varying an independent chi=X and retaining its metric-chain
term. The mixed equation imposes TOTAL radial current zero when `q!=0` and
there is no compensating ordinary-matter flux.

The dependency chain here is: that covariant variation -> static equations ->
the rational 3x3 system below -> exact control identity -> local EF dictionary
-> the existing action-derived KGB principal template. The first reduction is
an internal derivation, the matrix and pencil identities are exact SymPy
checks, and the resulting real inequalities and conditional algebra are
checked in Lean. The inverse-to-EF physical interpretation assumes the
invertible conformal dictionary; it is not derived from a numerical scan.

Let `ds^2=-A dt^2+B dr^2+r^2 dOmega^2`, `phi=q t+psi(r)`, and

```
g=A'/(2A), B=1+2rg, b=B'/(2B), B'=2g+2rg',
z=X', p=psi', U=p^2/B, Q=2X+U=q^2/A, a=g+2/r,
Z=U/X-rg, Cj=2XZ/(pr).
```

Work with smooth finite coefficients, regular static coordinates,
`F>0, X>0, U>0, B>0, r>0, p!=0, f!=0`. The regular inverse also needs
`z!=0`. Algebraic identities hold more generally wherever their denominators
are defined. Finiteness is a substantive assumption at zero-gradient limits.

## Full arbitrary-F inverse

Because `B=1+2rg`, the geometric radial pressure is zero. Set

```
rho=(1-1/B)/r^2+B'/(B^2 r),
pt=[g'+g^2-gb+(g-b)/r]/B,
Pcal=(2fza+Kz^2)/B,
Pz=partial_z Pcal=(2fa+3f^2 z/F)/B,
R0=partial_r Pcal+g' partial_g Pcal+z(f partial_F+j partial_f)Pcal,
Achi=f(rho-2pt)-K_X z^2/B-2K(g-b+2/r)z/B,
Lbase=2F rho+Pcal-2jz^2/B+Kz^2/B-2f(2/r-b)z/B.
```

Partials hold the other displayed arguments fixed. The radial equation is
`P=Pcal`. Radial preservation, total current and density then give

```
M3 (z',P_X,G_X)^T = rhs,

M3 = [[ Pz,    -z,  0     ],         rhs = [-R0,
      [-2K/B,   1, -Cj    ],                -Achi,
      [ 2f/B,   0,  2Xz/p ]]                Lbase].
```

In particular, the current equation is `P_X+E_chi=Cj G_X`, where
`E_chi=Achi-2Kz'/B`. The `-2jz^2/B` in Lbase is required by the lapse
variation; omitting it destroys the exact cancellation below.

The determinant is

```
det(M3)=4fzQ/(Bpr).
```

It contains neither j nor `F-Xf`. If the first row is eliminated, let
`Rrad=a+3fz/(2F)`. The resulting pressure-chart determinant is
`2zQ/(pr Rrad)`, and `Pz det(M2)=det(M3)`. At the pressure fold
`z=-2Fa/(3f)`, Pz vanishes while the full determinant is
`-8FaQ/(3Bpr)`, which is nonzero on a regular fold. `Z=0` is not a singularity
of the full inverse either.

In contrast, `F-Xf=0` makes the conformal kinetic-variable map singular:
for `C=2F`, `chi=X/C`,

```
Dfield=C-X C_X=2(F-Xf), dchi/dX=Dfield/C^2.
```

The static matrix can remain invertible there, but that does not license the
invertible EF dictionary or its health interpretation. `Dfield<0` is not itself
a singularity; the necessary local map condition is `Dfield!=0`, with `C>0`.
At `f=0` or `z=0` this static chart degenerates; no blanket nonexistence claim
is made for another chart. More strongly, at z=0, `P=R0=0`; if `fa/B!=0`,
radial preservation forces z'=0 and finite-coefficient density gives
`2F rho=0`. A strictly positive target density is therefore incompatible with
such a regular zero-gradient point. The finite exponential density positivity
proved at the previous checkpoint still applies; it is not a uniform positive
lower bound in a Newtonian asymptotic limit.

## The j-control cancellation

M3 is independent of j, and direct differentiation gives

```
partial_j rhs = -(z^2/f) M3[:,0].
```

Thus wherever M3 is invertible,

```
partial_j (z',P_X,G_X) = (-z^2/f,0,0).
```

This is exact, not a numerical rank estimate. A useful independent coordinate
check sets `w=fz=F'`, `kappa=P_X/f`, `gamma=G_X/f`. Then

```
Pcal=(2wa+3w^2/(2F))/B,
Pw=partial_w Pcal,
Rw=partial_r Pcal+g' partial_g Pcal+w partial_F Pcal,
Aw=rho-2pt+3w^2/(2F^2 B)-3(g-b+2/r)w/(FB),
Lw=2F rho+Pcal+3w^2/(2FB)-2(2/r-b)w/B,

[[ Pw,      -w,  0     ],       [w'   ]   [-Rw]
 [-3/(FB),   1, -Cj    ],   *   [kappa] = [-Aw],
 [ 2/B,      0,  2Xw/p ]]       [gamma]   [ Lw]

det(Mw)=4wQ/(Bpr).
```

Neither f nor j appears in this solved system at fixed `(r,g,g',F,X,U,w)`.
Its evolution still has `X'=w/f` and `f'=jz`; changing coordinates has not
removed the obligation that `F_X=f` and `f_X=j` belong to one function.

Differentiate the solved functions along the actual radial flow, including
`F'=fz`, `f'=jz`, `U'=-2gQ-2z`. Then

```
partial_j P_XX=P_X/f, partial_j G_XX=G_X/f.
```

The script verifies this with an arbitrary smooth function of
`(F,w,X,U,r,g)`, rather than assuming a numerical inverse formula. P_XX and
G_XX are total derivatives, not independent stability parameters.

For the general EF dictionary, with `C1=2f`, `C2=2j`, `Dfield=C-X C1`,

```
Ptilde_chi=(P_X-2C1 P/C)/Dfield,
Gtilde_chi=C G_X/Dfield,
alpha=2C^3/(C1 Dfield^2),

partial_j Ptilde_chichi=alpha Ptilde_chi,
partial_j Gtilde_chichi=alpha Gtilde_chi.
```

These identities include the explicit C2 terms in the dictionary. Omitting
them would give the wrong control direction. The transformed background
gradient/Hessian and lower action jets depend on F,f,z, not j, at the fixed
state considered here.

## Exact scalar-pencil parameter reduction

For the on-shell static EF KGB block, write the canonical-time-sign principal
matrix entries as `Ktime=C00`, `cross=C01`, `R=C11`, `T=C22=C33`. Using the
existing action-derived principal expression, the exact check gives

```
partial_j C = alpha (rho_E+P_E) diag(1,0,beta,beta),
beta=U/(2X)>0,
I=Ktime-T/beta, partial_j I=0.
```

Here `P_E=Ptilde=P/C^2` is the EF action value, equal to its radial pressure
on the zero-current branch, not its angular stress or principal coefficient.
A directly computable expression in physical-frame jets is
`rho_E+P_E=2X G_X z/(C^2 p)`; the conformal Jacobian cancels between
`Gtilde_chi=C G_X/Dfield` and `chi'=Dfield z/C^2`.

The zero radial and off-diagonal slopes are exact. This identity uses zero EF
radial current on the mapped background; the EF interpretation presupposes
the invertible map. It is not an off-shell assertion about arbitrary jets.
If `rho_E+P_E=0`, j gives no principal control and an accessibility argument
requiring a nonzero slope cannot be used.

Suppose `R<0`, `beta>0` and the time slope is nonzero. Then j spans the one
affine pencil `T=beta(Ktime-I)`, with fixed cross and R. A bounded static
quadratic scalar energy and a strict EF light-cone interior are possible for
some finite j **if and only if**

```
I+R > 2 abs(cross).
```

This replaces a scan over an arbitrary j range. The precisely formalized
criterion is `Ktime>0, R<0, T<0, abs(cross)<Ktime`, together with

```
q(t)=Ktime+T-2 abs(cross)t+(R-T)t^2 > 0, 0<=t<=1.
```

Necessity follows from `T<0 => Ktime<I` and `q(1)>0`. For sufficiency set
`gap=I+R-2abs(cross)` and

```
delta=min(gap/2,-R/(2beta)), Ktime=I-delta, T=-beta delta.
```

Both endpoints of q are positive and `R-T<0`; the exact identity
`q(t)=(1-t)q(0)+t q(1)-(R-T)t(1-t)` proves positivity throughout the interval.
Lean proves both this real-variable equivalence and accessibility through
`Ktime=K0+slope*j` for nonzero slope. It assumes the matrix-to-cone reduction
just stated; it does not formalize the full physical perturbation reduction.

The isotropic policy `T=R` is more restrictive: its unique reachable target
has `Ktime=I+R/beta` and requires
`I+R(1+1/beta)>2abs(cross)`. Its failure does not exclude a non-isotropic
causal interval. Root construction may use the proved interior choice instead.

## Primary kinetic degeneracy, not a degree count

Choose local unitary clock coordinates, possible for a timelike clock, and
define `Astar=n^mu partial_mu phi`, `Vstar=n^mu partial_mu Astar`, so
`X=Astar^2/2`, `nX=Astar Vstar`. Take
`Kij=(dot hij-Lie_shift hij)/(2N)` and let `ktrace=h^(ij) Kij` denote its trace.
After removing the ADM boundary term of F R, the quadratic highest-velocity
density divided by `N sqrt(h)` is

```
F(Kij Kij-ktrace^2)-2f ktrace nX-3f^2(nX)^2/(2F)
 = F shearij shearij-(2F/3)(ktrace+3f Astar Vstar/(2F))^2.
```

The `(ktrace,Vstar)` Hessian has null vector
`(-3f Astar/(2F),1)`. With `pi=hij pi^ij` and quadratic-block momenta,

```
pi/sqrt(h)=-2F ktrace-3f Astar Vstar,
pstar/sqrt(h)=-2f Astar ktrace-3f^2 Astar^2 Vstar/F,
F pstar-f Astar pi=0.
```

P contributes no highest-velocity quadratic term. In the boundary convention
where `-G box(phi)` is not integrated by parts, its highest-velocity term is
`G(Vstar+Astar ktrace)`. It leaves the Hessian unchanged and shifts the
relation to

```
F[pstar-sqrt(h)G]
 -f Astar[pi-(3/2)sqrt(h)G Astar]=0.
```

SymPy checks the square completion, null vector, momenta and G shift; Lean
checks the unshifted conditional momentum identity. This is a primary
highest-velocity relation in stated coordinates/boundary convention. A full
canonical analysis, secondary constraints, matter coupling, and constraint
rank across backgrounds have not been supplied. The negative trace square
alone is not a physical ghost diagnostic; the constrained system must be
analyzed before counting propagating modes.

## Evidence and exact remaining gates

`test_nonaffine_variation.py`: 14 exact SymPy tests, including the general
current/lapse rows, determinant, j-column cancellation, F-gradient chart,
angular identity, zero-gradient/fold limits, total-jet and EF-jet slopes,
matched-mass cancellation, cone interpolation/isotropic threshold,
dimensionful target identity, primary kinetic block and scalar principal
pencil. No numerical samples, tolerances, random seeds or numerical ranks are
used. `NonaffineAlgebra.lean` has seven conditional algebra theorems;
`ConeWindow.lean` has the two exact local cone equivalences.

The proof-audit and computation-audit skills scoped these claims; debugging
isolated missing-import/parser issues in the first Lean drafts. The mathematical
proofreading and verification skills cover this report and final recorded run.
Reproducible commands, hashes, versions and final status are in `RUN.md` and
`run_001/manifest.json`. Those records, not preliminary development runs, are
the evidence for completion.

The cheapest decisive next checks are a dynamically integrated, common
F/f/j/P/G action across masses and physical source/cosmological matching.
Neither a successful local control nor primary Hessian degeneracy supplies
those missing implications. No PPN value, measured Newton constant, CMB
spectrum or global universal-MOND solution is certified here.
