# A universal Gaussian length: action and Solar bound

One common physical Gaussian standard deviation ell defines a single unsplit
nonlocal energy for all matter. It removes the object-dependent width rule,
at the cost of one new fitted length. It is not a derivation of that length,
a relativistic completion, or a general observational success.

The new result is an analytic, background-independent bound on the Sun's
incremental anomalous quadrupole:

```
|delta Q2| < 6 sqrt(G M_sun a0)/ell^2.
```

For ell=2.5, 3, or 3.5 kpc this lies below the frozen Cassini ceiling by
more than seven orders of magnitude on both original acceleration footings.
The result bounds the change produced by adding the Sun to a fixed background;
it does not bound the background's own tidal field or replace an ephemeris fit.
The inherited constant-background Solar calculation has the still stronger
KT34 bound 45/epsilon_sun^3. No very-large-epsilon floating quadrature is needed.

## Precisely specified response law

Let S_ell be normalized, isotropic, translation-invariant Gaussian convolution
on all of space. It has the same state-independent physical width for every
source, test body, baryon cell, and matter distribution. Let N be the ordinary
Newton potential operator, Delta N rho=4 pi G rho. Define

```
U[rho] = (1/2) integral rho N rho d^3x
         - (1/(4 pi G)) integral H(|grad N S_ell rho|) d^3x,
H'(g)=g [nu(g/a0)-1],
nu(y)=1/2+sqrt(1/4+1/y).
```

An infrared regulator or fixed-mass energy renormalization is understood for
isolated MOND fields, whose raw field energy need not be finite at infinity.
The local variations and force operator below are unaffected. Holding ell
fixed, integration by parts and self-adjointness of N and S_ell give

```
delta U/delta rho = N rho + S_ell Phi_ph[S_ell rho],
Delta Phi_ph = div A(u),
u=grad N S_ell rho,
A(u)=[nu(|u|/a0)-1]u.
```

Thus the outer Gaussian is mandatory and has the same width as the source
Gaussian. The matter action is kinetic energy minus U. Translation/rotation
symmetry is manifest; reciprocal response follows wherever its second
variation exists. A finite-dimensional implementation must use the actual
volume-weighted adjoint, as in KT33. This establishes a nonrelativistic energy
model, not dynamical health or a covariant theory.

Unlike ell=epsilon sqrt(GM_object/a0), this law does not need a decomposition
of the density into objects. A prescribed external field may be added to u
for the local diagnostic, while the universal law itself acts on the entire
matter distribution. The new MW runs use the exact ell directly in kpc,
without KT25's mass scaling or logarithmic width rounding.

## Uniform bound with an arbitrary fixed background

Write u_0(x) for any background Newton field entering the response, and let
delta u=grad N S_ell delta rho, where delta rho is nonnegative with finite
mass M. It may be a point source, and its location is arbitrary. The physical
Newtonian contribution remains unsmoothed and is removed when defining the
anomalous increment. No lower bound on |u_0|, spatial constancy, inversion
symmetry, or smallness of delta u relative to u_0 is required.

First, the normalized Gaussian Newton field obeys

```
|grad N S_ell delta rho| <= kappa G M/ell^2,
kappa=(c/3)^(2/3),  c=sqrt(2/pi).
```

For a point source this follows from M(x)/x^2<=min(cx/3,x^-2); convolution
and nonnegativity extend it to every such source.

Second, the simple response vector is globally one-half Holder continuous.
In dimensionless units put f(r)=(sqrt(r^2+4r)-r)/2. It is increasing, concave,
vanishes at zero, and f(r)<=sqrt(r). Hence for r>=s,

```
0<=f(r)-f(s)<=f(r-s)<=sqrt(r-s).
```

For vectors x,y of lengths r,s and mutual angle theta, write
a=|r-s| and b=sqrt(2rs(1-cos(theta))). Their separation is sqrt(a^2+b^2).
Since the response vector is f(r) times the radial unit vector,

```
|A_dimless(x)-A_dimless(y)|^2
 = (f(r)-f(s))^2+2f(r)f(s)(1-cos(theta))
 <= a+2b <= sqrt(5) sqrt(a^2+b^2).
```

This includes zero vectors by continuity. Restoring dimensions yields

```
|A(u)-A(v)| <= 5^(1/4) sqrt(a0 |u-v|),
||delta A||_infinity <= 5^(1/4) sqrt(kappa G M a0)/ell.
```

Third, the outer-smoothed Poisson projection has an integrable Hessian
kernel. With F_ell(r)=erf(r/(sqrt(2)ell))/r, its third derivatives represent
the Hessian of the anomalous potential applied to A. For any unit vectors
v,w, KT34 REVIEW derives

```
(1/(4 pi)) integral |D^3 F_ell[v,w]| d^3x
 <= 2 c sqrt(33)/(3 ell).
```

For completeness, at ell=1 its tensor is

```
D^3 F = r^-4[-15 U nnn+3T(delta_ij n_k+delta_ik n_j+delta_jk n_i)],
T=P(5/2,r^2/2), U=P(7/2,r^2/2), 0<=U<=T.
```

The angular squared norm of its contraction is maximized for v=w and is
at most 33T^2/r^8. Angular Cauchy--Schwarz and
integral T/r^2 dr=2c/3 give the displayed bound. This argument concerns the
whole-space Gaussian kernel, not every finite lattice approximation.

Consequently, for the symmetric anomalous potential Hessian increment J,

```
||J||_op <= 5^(1/4) K sqrt(G M a0)/ell^2,
K=(2c sqrt(33)/3)(c/3)^(1/3) < 2,
||J||_op < 3 sqrt(G M a0)/ell^2.
```

No assumption about the background entered these bounds. For any unit axis n,
the trace-free component obeys

```
|n^T J n-tr(J)/3| <= (4/3)||J||_op.
```

The inherited convention Q2=(3/2) times that component therefore gives
|delta Q2|<6 sqrt(G M a0)/ell^2, as claimed. In a general background this
bounds every projected trace-free component; axial symmetry is unnecessary.

Safe constant checks use c<4/5, sqrt(33)<23/4, (c/3)^(1/3)<13/20,
so K<299/150<2, and 5^(1/4)<3/2. The bounded arithmetic script checks all
algebraic slack with exact fractions, including an exact rational upper
bound on sqrt(G M_sun a0) for the displayed Solar inequalities.

## What is already tested, and what was previously a liability

The parent-owned `../mw/` runs search the unchanged 1,375 baryon cells per
footing at ell=2.5, 3, and 3.5 kpc and refine selected witnesses. No historical
MW score is transferred to this new law. The Solar bound above is common to
every MW model at that same ell; no object-specific epsilon is selected.

A universal-length route was tried before, but with the old source-only map:

- KT14 at xi=2 kpc had seven alternate-footing MW passes and no canonical
  pass. Those are not scores for the corrected reciprocal map.
- KT15's same source-only 2 kpc arm passed 9 of 24 dwarfs with its 1D external
  field approximation, compared with 15 for plain QUMOND. Its frozen label
  was HURT, not KILLED. At Upsilon=2 it predicted Fornax 5.5 km/s versus 11.7,
  Sculptor 2.8 versus 9.2, and Leo I 4.3 versus 9.2.
- KT16's enormous-width numerical Cassini arm was below its cancellation
  accuracy floor. Its physical passing expectation is now supported by
  analytic bounds, not those unreliable quadrupole digits.

The dwarf deficit is a material warning for a universal several-kpc length.
It is not an exact exclusion of the new reciprocal map: its source AND outer
operation, finite solver, and external-field handling must be recomputed.
SPARC inner curves, wide binaries, total Galactic tides, lensing, cosmology,
and relativistic/dynamical health are not established by these two-system
calculations. No additional baryons or observational-cut changes are used.

## Evidence and review

`bounds.py`, `contract.json`, and `run_001/` contain the narrow arithmetic
check. The input manifest pins KT33's Solar constants, KT34's kernel proof,
the inherited P4 solver's physical kpc conversion, and the three historical
READMEs. The MW solver uses KPC=3.085677581491367e19 m; the old mass-width
approximation 3.0857e19 m is not silently substituted.

The parent independently reconstructed the Holder and trace-free factors
before this document was written. This is a targeted mathematical check,
not a complete independent audit of the combined new-law model. Final
self-proofreading covers this new document's symbols and units; no edits
to earlier scientific inputs are made.
