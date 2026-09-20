# A normalization-free orbital-shape test of the rational particle-free action

Research checkpoint: 2026-09-20, base `1172c5f69cf96f6ee41a8c89a6d21cdb5016c181`.
The repository is being edited concurrently. This directory adds a candidate
test and its evidence; it does not change existing action or status files.

## Result

For circular test-body motion outside an isolated spherical baryonic source,
the specified auxiliary action in `../kappa_unit_response_2026_09_20/README.md`
implies the following relation, with no acceleration normalization to fit:

\[
\boxed{\frac{d\ln v_c}{d\ln r}
 =\frac12-\frac{1+\sqrt{1-f_b}}{3-2f_b+\sqrt{1-f_b}}},
\qquad f_b=\frac{G M_b}{r v_c^2}=\frac{M_b}{M_{\rm dyn}}.
\]

Here `Mdyn=r v_c²/G` is the mass a Newtonian circular-orbit inference would
assign, not an introduced dark particle or material halo. Baryonic mass must be
estimated independently of the tested gravitational relation.

A sharp consequence is

\[
\boxed{\left.\frac{d\ln v_c}{d\ln r}\right|_{r_*}=-\frac14
\quad\Longleftrightarrow\quad
\frac{r_* v_c(r_*)^2}{G M_b}=\frac43.}
\]

The power-law statement is **local**: this does not claim an entire orbit
family has `v∝r^(-1/4)`. Nor does every extended system have this point in its
observable exterior. For an ideal point source the point exists uniquely.

This is a conditional prediction of the **full rational response**, not a
completion-independent result of two-channel counting. It is not observational
confirmation, an established new law of nature, or an established priority claim.

## Derivation

Retain the relative coefficient `lambda>0`; do not set it to one. Put

\[
b=s/\lambda=2a_0>0,\quad x=g/b,\quad q=1/(1+x),
\qquad \mu(x)=1-(1+x)^{-2}.
\]

The model's isolated spherical field equation is `r² g mu=G Mb` and ordinary
circular test-body kinematics gives `v_c²=rg`. Thus `f_b=mu=1-q²`.
The logarithmic response elasticity is

\[
A=\frac{x\mu'(x)}{\mu(x)}
 =\frac{2}{(1+x)(2+x)}=\frac{2q^2}{1+q}.
\]

Differentiating the constant exterior flux gives
`(1+A) d ln g/d ln r=-2`. Writing `beta=d ln v_c/d ln r` gives
`(1+A)(2 beta-1)=-2`. Eliminating `q=sqrt(1-f_b)` proves the displayed relation.

The quarter-slope uniqueness is the exact factorization

\[
\beta+\frac14=\frac{(2q-1)(3q+1)}{4(1+q+2q^2)}.
\]

Since `0<q<1`, its only zero is `q=1/2`, so `f_b=3/4` and the mass ratio is `4/3`.
At this point `g=b=2a0` and `r_*²=4GM_b/(3b)`. The ordinary small-radial-oscillation
formula also gives `omega_r²/Omega²=2+2 beta=3/2`; the dynamical derivation of that
standard epicyclic formula is not formalized here.

For a smooth **extended spherical** source with
`m=d ln Mb(<r)/d ln r`, the generalization is

\[
\beta=\frac12+\frac{(m-2)(1+\sqrt{1-f_b})}
 {2(3-2f_b+\sqrt{1-f_b})}.
\]

This extension is checked symbolically, not in the current Lean theorem.

## What makes this discriminating

At the same local slope `beta=-1/4`, three kernels predict different ratios:

| Specified response | Mdyn/Mb |
| --- | ---: |
| This rational two-channel completion | 4/3 = 1.333333… |
| Simple MOND, mu=z/(1+z) | 3/2 = 1.5 |
| Standard MOND, mu=z/sqrt(1+z²) | sqrt(3/2) = 1.224745… |

These differences cannot be removed by changing the constant `a0`, `s`, or
`lambda`: each changes the physical radius of the transition, not this relation.
They can be changed by changing the full response shape. As a negative control,
`p(y)=1-exp(-y)` has the same zero value, unit initial slope, saturation, and
two-channel composition, but fails this shape relation. This explicitly prevents
claiming the result for every completion allowed by PD12.

## Physical restrictions and what is still needed

- Isolated, static, spherical modified gravity with ordinary test-body inertia.
  External fields, non-spherical disks, pressure support and noncircular motion
  require their own field/dynamical calculation.
- Positive finite acceleration, positive baryonic mass, spatially constant
  positive `s` and `lambda`. The endpoints `f_b=0,1` are limits.
- The simple exterior law requires constant enclosed baryonic mass. A disk's
  enclosed mass is not interchangeable with its Newtonian radial force.
- Measuring a local slope requires uncertainty-aware inference; differentiating
  noisy rotation samples directly is not an observational likelihood.
- Failure would reject this response and these physical hypotheses jointly;
  it would not establish the necessity of a dark-matter particle.

## Executed routes and scope of novelty search

1. Generalized Kepler polynomial: exact,
   `r v_c⁴(v_c²+2br)=GM_b(v_c²+br)²`, but principally a rewrite of the existing
   constitutive equation. Retained in Lean, not promoted as a discovery.
2. Orbital-shape elimination: selected because it removes the disputed
   normalization and produces a dimensionless observable test. The derivation
   and comparison above are the substantive result.
3. Balmer-layer population route: cannot supply a supported observed law from
   the reviewed inputs; layer thickness does not determine central radius.
   No substitution of thickness for radius is used in this package.

Bounded web search on 2026-09-20 used exact rational-function strings and
`MOND rotation curve logarithmic slope mass discrepancy`, `MOND quarter slope`,
and `MOND maximum halo acceleration`, together with a scoped repository search.
It does not establish global novelty. The correct classification is a
**model-specific formal corollary of familiar MOND spherical dynamics**; whether
this exact presentation already appears elsewhere remains unresolved.

Primary source inspected: H.S. Zhao and B. Famaey,
*Refining MOND interpolating function and TeVeS Lagrangian*,
[astro-ph/0512425v3](https://arxiv.org/html/astro-ph/0512425v3),
equations (1), (6), (7), for `mu g=gN` and the standard/simple comparison kernels.
Their external-field discussion also illustrates why the isolated formula must
not be exported unchanged to externally dominated systems. No source copy was
retained. Literature discovery also found the older maximum-halo-acceleration
result of Brada and Milgrom, astro-ph/9812117; a maximum anomalous acceleration
must not be presented as a new general principle.

## Certificate and computation boundary

`OrbitalShape.lean` proves 13 theorems, including the response derivative,
spherical-flux derivative, scale elimination, the assembled
`rational_exterior_shape` theorem, and uniqueness of the quarter-slope point.
Its physical inputs are explicit; action variation, observational identifications
and empirical validity are not supplied by Lean.

`verify.py` differentiates the actual implicit flux independently with SymPy,
checks alternative-response controls, solves the circular field equation
numerically at perturbed radii for 93 cases, and recompiles the Lean file.
The grid uses 31 dimensionless accelerations from 0.01 to 100 for each of three
normalizations; the slope tolerance is 2e-8. This finite check is independent
numerical support, not the universal proof. Raw results and provenance are in
`certified/`; `run/` retains the preliminary direct check. Regenerate the checks
with `python3` on the absolute `verify.py` path, optionally followed by an output
directory. The certified run contains a version-2 input/output hash manifest.

Self-review: checked signs at the Keplerian and flat-curve limits; positivity of
denominators and the physical square-root branch; uniqueness rather than just
evaluation of the quarter-slope point; arbitrary normalization; constant-mass
scope; counterexample to completion independence; and inherited literature.
No independent-agent review or observational fit was performed for this package.
