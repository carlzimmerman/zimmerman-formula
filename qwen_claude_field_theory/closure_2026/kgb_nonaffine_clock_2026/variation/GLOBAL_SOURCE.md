# Global source, mass and parameter audit

2026-09-10; bounded audit of the imposed exterior family and the non-affine
variation, base `583fdf69a597ef9ed57b4f9ced48dd457c8ef2de`.
Verdict: incomplete, with the source-normalization and common-action
continuation maps missing. No data fit or new empirical normalization is
asserted. An additional independent read-only lane checked the source/unit
distinctions below; its agreement is a cross-check, not a substitute for proof.

## What is fixed, solved, or still assumed

| Item | Actual status in this exterior construction |
| --- | --- |
| `mu(y)=1-exp(-y)`, `r(epsilon,y)`, `B=1+2rg` | Imposed target family, not derived from a completed universal action or observations. |
| `K(X)=3F_X^2/(2F)` | Fixed functional relation in the proposed action; the primary kinetic block is degenerate. |
| `F`, `f=F_X`, `j=F_XX` | Jets of one function. They cannot be independently reset at every point or mass. |
| `P` | Fixed on each exterior by the radial equation `P=Pcal`. |
| `P_X,G_X` | Determined by the regular 3x3 inverse at a chosen background and F/f jets; independent of j at that fixed state. |
| `P_XX,G_XX` | Actual total derivatives; their common j slopes are `P_X/f,G_X/f`. |
| Additive constant in G | A boundary term for the vacuum local equations, not a local health control. |
| `epsilon` versus baryonic mass | A mass label until a sourced interior and common boundary solution determine its physical normalization. |
| One universal `a0` | A shared target/unit input here, not a derived value or a demonstrated relation to cosmology. |
| Measured Newtonian coupling, lensing/time delays, CMB | Not supplied by vacuum action jets or by units `m=c=a0=1`. |

This is a reduction of conditional functional freedom, not a finite fitted
parameter count and not a Dirac degree count. At most one shared function
`j(X)` remains as a non-affine control after F and f are evolved by
`F_X=f`, `f_X=j`; it is not a third independently adjustable function. Common
P and G still impose compatibility between different masses. The explicit
clock contributes gravitational stress and must remain included in the
physical accounting; it is not a dark-matter particle sector.

## The target mass law is conditional

The frozen conformal target in
`../../kgb_mass_compatibility_2026/conformal_inverse.py` imposes

```
mu=1-exp(-y), r^2 y mu=epsilon^2,
B=1/(1-2*r*y), g=yB, y=g/B.
```

Restoring dimensions with physical areal radius R, set
`r=a0 R/c^2` and define the metric proxy `a_proxy=a0 y`. Pure algebra gives

```
a_proxy mu(a_proxy/a0)=epsilon^2 c^4/(a0 R^2).
```

The convention stated in `../../kgb_joint_action_2026/joint_static.py` is
`epsilon^2=G_bare M_b a0/c^4`. Substituting it produces
`a_proxy mu=G_bare M_b/R^2`, but does not derive the convention from a source.
The exact unit-change identity is checked in the Python suite. A physical
prediction requires the same completed action with an actual baryonic
interior, matching conditions, and common asymptotic/cosmological clock data
to return that exterior coefficient as a function of measured baryonic mass.
The zero radial shift-current condition alone does not do this.

Identifying the right side with an observational law written using measured
Newtonian `G_N` requires `epsilon^2 c^4/a0=G_N M_b`. Equating G_bare and G_N,
or giving a different conversion, is an additional calculation. In this
coupled clock theory, the coefficient F alone does not establish the
measured weak-source force, which can also depend on scalar response and
background/matching data. No PPN coefficient or measured-G value is assigned
by this audit.

Even the acceleration identification has a domain. For the stated physical
metric and ordinary metric matter coupling, a timelike circular geodesic has
`v_c^2/c^2=r g`, hence `v_c^2/R=a0 g=a0 yB`; the static support proper
acceleration is `a0 g/sqrt(B)=a0 y sqrt(B)`. Thus a_proxy agrees with these at
leading weak field, not identically in relativistic regions. In the separate
older pressure-deformed inverse, `B=T/(1+r^2P)` and `g=yT`, so
`y=g/[B(1+r^2P)]`; do not transfer `y=g/B` to that chart at nonzero P.
The literal fixed-epsilon limit `y -> infinity` also leaves the conformal
static chart when `1-2*r*y` ceases to be positive; Newtonian overlap statements
must retain the regular weak-field domain.

## One global a0 versus apparent location dependence

A global constant a0 and a nonconstant universal F(X) are logically distinct.
The same function F can take different values because the clock background X
varies with location or epoch, without introducing an independently chosen
`a0(location)`. Such variation can affect source calibration, clock response
and an apparent acceleration scale inferred with a fixed-G observational
model. It does not, by itself, prove that the imposed global target law is
preserved. Allowing separate fitted a0 values per system would introduce new
freedom beyond the universal construction.

Conversely, declaring `a0=1` merely chooses units. A theory-level numerical
value, or a relation to cosmic quantities, would have to follow from the
dimensionful universal action and a cosmological/source solution; it is not
present in this local exterior inverse.

## Common-mass preservation: what j cannot repair

At a common X, two exteriors must share F,f,j,P and the action derivatives.
Each solves its own radial pressure relation

```
Pcal_i(F,f,z_i,r_i,g_i)=P,
P_X,i=P_X,k, G_X,i=G_X,k.
```

Both derivative equalities are required. The old unextended-current condition
matching `G_X/P_X` alone is not a substitute for the total-current inverse.
Common additive action data and branch signs must also be respected when
integrating the action.

Write the correctly differentiated curvatures at fixed lower common jets as

```
P_XX,i=A_i+j P_X/f, G_XX,i=B_i+j G_X/f,
P_XX,k=A_k+j P_X/f, G_XX,k=B_k+j G_X/f.
```

Then

```
P_XX,i-P_XX,k=A_i-A_k,
G_XX,i-G_XX,k=B_i-B_k.
```

The first preservation of already matched P_X and G_X is therefore
independent of the shared j control. A nonzero gap cannot be repaired by
choosing another common j at that point. Python and Lean check the exact
cancellation and its nonrepair corollary. This is conditional on the common
lower jets; it is not a universal obstruction for different initial F/f,
background data or another regular branch. It proves neither invariance nor
nonexistence of a compatible trajectory through all masses.

## Observational gates not discharged by the vacuum inverse

Galaxy circular-motion data, lensing and time-delay/redshift observables must
all follow from the same physical metric and sourced solutions, rather than
being assigned separately. Lensing and propagation depend on more than the
one imposed acceleration proxy. A CMB prediction requires that SAME action
on a sourced cosmological background, including matter/radiation evolution
and perturbations; a static vacuum jet does not provide it. A primary kinetic
constraint or a local reduced scalar cone is not that cosmological calculation.

The narrow constructive next gate is: preserve common action data on an X
interval for more than one source, then solve and match an actual source with
the same global normalization. Until that succeeds, there is no established
parameter-reduced joint CMB/galaxy/lensing/time theory here.
