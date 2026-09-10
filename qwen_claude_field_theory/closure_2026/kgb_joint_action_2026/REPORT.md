# A shared-action inverse, with no dark-matter particles

2026-09-10; base `de6b2c1a948c043a3a3c7130f88051db66c6bc46`.
**Full theory: OPEN.** This checkpoint constructs a finite two-mass common-action
branch and identifies its next obstructions. It does not certify gravity or
establish a universal no-go. No dark-matter particle action is added. The clock
is explicitly dynamical, not a hidden auxiliary and not silently omitted from
the propagating field count.

## What changed mathematically

Previous pressure steering could choose favorable local derivatives separately.
Here matching two distinct baryonic masses fixes the derivatives of **one**
action. No stability coefficient is independently tuned afterward:

\[
 S=\int\!\sqrt{-g}\,[mR/2+P(X)-G(X)\Box\phi]\,d^4x+S_m[g,\psi_m],
 \qquad X=-\tfrac12(\nabla\phi)^2,\quad m=(8\pi G_b)^{-1}>0.
\]

This is the existing kinetic-braiding action class, not a claim to invent that
class. No global novelty claim is made for the inverse method either. The
exponential target and no-particle/clock direction are Carl Zimmerman's research
inputs; the computations below test them, not their empirical truth. In
particular, the normalization of the target by a baryonic mass is imposed in
this exterior inverse problem, not yet derived by solving a baryonic interior.

Use signature \((-+++)\), \(c=a_0=m=|q|=1\),
\(ds^2=-A dt^2+Bdr^2+r^2d\Omega^2\), \(\phi=qt+\psi(r)\), \(q=-1\).
Let \(p=\psi'\), \(g=A'/(2A)\), \(U=q^2/A-2X=p^2/B>0\).
The raw action variation in `../ticking_kgb_inverse_2026/kgb_inverse.py`, rerun
in the regression suite, supplies the current and clock stress. On its
zero-current exterior branch:

\[
 J^r=0,\quad p_r=P,\quad
 \rho+P=\frac{2X\,G_X\,X'}p,
 \quad B=\frac{T}{1+r^2P},\quad T=1+2rg.
\]

In the numerator of the density expression, \(G_X X'\) is a product;
\(G_{XX}\), used below, denotes the second derivative of the function \(G\).
Ordinary matter couples only to the physical metric. Its diffeomorphism Ward
identity gives \(\nabla_\mu T_m^{\mu\nu}=0\) on the matter equations; the clock
does not supply a nonmetric baryonic force. This structural identity does not
settle the unresolved source/boundary matching.

## Exact static inverse and the new matching equation

For each mass choose the same exponential target and a specified relativistic
completion that recovers the exact Schwarzschild radial metric when the target
becomes Newtonian and \(P=0\):

\[
 \mu(y)=1-e^{-y},\quad
 r=\frac{\epsilon}{\sqrt{y\mu(y)}},\quad
 g=\frac{y}{1-2ry},\quad
 \epsilon=\frac{\sqrt{G_b M_b a_0}}{c^2}.
\]

Here \(y\) is the target weak-field acceleration in units of \(a_0\), not
identically the exact relativistic \(g\). Other higher-order completions are
not excluded. Define

\[
 Z=U/X-rg,\quad
 E_0=\frac{4y^2e^{-y}}{r(\mu+ye^{-y})}
       +P\left(1-\frac3T+\frac{rT'}{T^2}\right),\quad
 W=P_X\,X'=\frac{ZE_0}{r(1+Z/T)},\quad
 h=\frac{G_X}{P_X}=\frac{r\sqrt{BU}}{2XZ}.
\]

Again, \(P_X X'\) in \(W\) is a product, not \(P_{XX}\).
These expressions come from the density, radial Einstein, and scalar current
equations; the source code checks the angular Einstein equation independently.

Write \(D_B=B'/B=T'/T-(2rP+r^2W)/(1+r^2P)\). Direct differentiation gives

\[
 \frac{d\log h}{dX}=a+P_X b,\qquad
 a=-\frac1U+\frac{2+rg}{XZ},
\]
\[
 b=\frac1W\left[
 \frac{D_B}2-\frac{g(2X+U)}U+\frac1r
 +\frac{2g(2X+U)/X+g+rg'}Z\right].
\]

The logarithm can be read as \(\log|h|\) for the negative branch actually used;
only its logarithmic derivative is used. SymPy reduces the direct chain-rule
expression minus \(a+P_Xb\) to zero.

Two masses must have the same \(h\) at a shared \(X\). Preserving that equality
determines, on the generic nonzero-denominator chart,

\[
 \boxed{P_X=-\frac{h_1a_1-h_2a_2}{h_1b_1-h_2b_2}}.
\]

This is a **functional compatibility condition**, not a canonical Dirac
constraint or a new empirical acceleration law. It supplies the differential
system

\[
 \frac{dy_i}{dX}=\frac{P_X}{r_{y_i}W_i},\quad
 \frac{dU_i}{dX}=-2-\frac{2g_i(2X+U_i)P_X}{W_i},\quad
 \frac{dP}{dX}=P_X,\quad \frac{dG}{dX}=P_Xh_1.
\]

The code integrates both \(P\) and \(G\). The irrelevant \(G(1/2)=0\)
constant multiplies a boundary term. A total derivative of the forced \(P_X\)
gives \(P_{XX}\), and each halo independently gives
\(G_{XX}=P_{XX}h+P_Xh(a+P_Xb)\). Neither curvature is fitted to a health flag.
Complex-step differentiation is checked against central differences and a
separate 60-digit mpmath calculation of the matching equation itself.

Initial \(h\) matching is solved analytically with its sign retained. For halo
2 set \(V=Xr_2g_2\), \(a_*=r_2\sqrt{B_2}\),
\(D=\sqrt{a_*^2+16h_1^2V}\). The positive root for \(\sqrt{U_2}\) is
\((a_*+D)/(4h_1)\) for \(h_1>0\), and
\(4|h_1|V/(a_*+D)\) for \(h_1<0\). Squaring without selecting this sign branch
would admit spurious solutions.

Chart restrictions include positive \(A,B,X,U,r,y\), nonzero \(P_X,W,Z\),
\(1+Z/T\ne0\), and nonzero matching denominator. If that last denominator
vanishes, its numerator must also vanish; otherwise there is no solution to
this matching equation. If both vanish, further preservation is required.
The Lean file checks precisely this abstract linear-algebra distinction and
uniqueness, not the entire field-theory derivation. The prior regular clock
chart remains relevant at \(P_X=Z=0\); such a point is not automatically a
physical obstruction.

## Finite constructive result and its boundaries

The 128-point deterministic initial scan uses \(X=1/2,P=0\),
\(\epsilon_1=10^{-6},\epsilon_2=2\times10^{-6}\) (a factor of four in mass),
\(y_1\in\{.1,1,10,20\}\),
\(y_2\in\{.1,.3,.6,1,2,5,10,20\}\), and
\(U_1=b_*Xr_1g_1\), \(b_*\in\{.25,.75,1.25,4\}\).
One initial pair passes both local energy and cone tests:
\(y_1=.1,y_2=.3,b_*=.25\). The computed derivatives are approximately

\[
 P_X=10454.55170815,\quad P_{XX}=4.354758735637\times10^{10},\quad
 G_X=-49.8979385536,\quad G_{XX}=2357114.79859.
\]

The coupled scalar principal expression is checked independently against
Deffayet et al. (2010), arXiv:1008.0048v2, equations 16–18; details and the
signature translation are in `audit/AUDIT.md`. The matrix comes from the
action's scalar equation after the metric equations remove Ricci mixing.
No ranks, PPN parameters, or degree-of-freedom counts are inserted.

For its quadratic scalar Lagrangian with coefficients \(C^{ab}\), positivity
of energy relative to the static time requires
\(C^{00}>0,C^{11}<0,C^{22}=C^{33}<0\). A tilted Lorentzian cone alone is not
sufficient. The all-angle light-cone test reduces to checking the minimum of
\(C^{00}+C^{22}-2|C^{01}|t+(C^{11}-C^{22})t^2\) on \(0\le t\le1\), plus
\(C^{00}>|C^{01}|\). Its endpoints and interior stationary point are evaluated;
this is not an angular sampling shortcut. Floating signs are still numerical
evidence, not interval-certified inequalities along the continuum.

For \(t=(X-.5)/10^{-6}\) the continuations to \(t=\pm.05\) give 51 output
points each with both halos passing these local tests. The action equality is
preserved to floating precision; stress and current are evaluated from the
action, not assigned from the target metric. This supports a common local
action on a small interval, **not** a complete galactic solution.

Extending the same initial pair, without changing the action, first reaches:

| Direction | Approximate t | First boundary in halo 2 |
| --- | ---: | --- |
| Increasing X | +0.07985070534 | Scalar cone reaches the metric light cone |
| Decreasing X | -0.13302238647 | Angular gradient coefficient reaches zero |

The endpoints are accepted event locations, not failed internal solver trials.
The run repeats both at tolerances \(2\times10^{-9}\) and
\(2\times10^{-11}\). A zero event value can have either floating sign and is
not a strictly healthy endpoint. Neither failure is blamed on large pressure
relative to a tiny residual density.

## The next gate: a third mass

`third_mass.py` keeps this common action fixed. Matching \(h_3=h_1\) fixes
\(U_3\) as a function of \(y_3\); matching \(h_{3,X}=h_{1,X}\) selects roots
in \(.02\le y_3\le20\). Preserving that next equality requires the same
\(P_{XX}\). This is an additional condition, not guaranteed by a match of
\(G_X\) and \(G_{XX}\) at one point.

At \(\epsilon_3=1.5\times10^{-6}\) the lower root is
\(y_3\simeq.1603985047\), but its required curvature is
\(P_{XX}\simeq3.714643230641\times10^{10}\), distinct from the common
\(4.354758735637\times10^{10}\). Independent 60-digit differentiation
confirms this requires a 14.6992% change in \(P_{XX}\); using the common value
instead gives a 14.2545% relative mismatch in \(h_{XX}\). The separate
normalized logarithmic-derivative preservation residual is not that percentage.
The higher root also mismatches. The two
original masses are included as positive controls and recover their matching
derivatives. Five mass values and two root grids (401 and 801 points) are run.
Sign-change searches do not enumerate tangent/even-multiplicity roots; the
result is not a universal impossibility theorem.

Thus pointwise healthy three-mass jets can still fail **functional
integrability**. The selected two-mass reconstruction has not passed this
next test. The actionable next construction is to impose third-mass (ultimately
continuum-of-masses) derivative compatibility *during* the inverse solve,
allowing shared initial data or permitted post-Newtonian metric terms to vary,
rather than independently repairing each halo's principal matrix.

## Correct lensing criterion and limits of the certificate

`lensing/` independently derives the temporal and spatial potentials in
isotropic coordinates. At first weak-field order,

\[
 \Phi'=g,\qquad \Psi'=g-\frac{rP}{2m},\qquad
 \frac{\Phi_W'}g=1-\frac{rP}{4mg}.
\]

The last term, not \(P/\rho\), measures the local pressure-induced fractional
Weyl-slope correction. It is about \(10^{-8}\) on the short constructed
interval. These are pressure contributions only: full finite-radius GR
corrections, integrated potentials, a complete light path and outer matching
remain necessary. No slope ratio is labeled \(\gamma_{\rm PPN}\).

`audit/` also supplies exact counterexamples to (i) treating a positive
interval narrower than a numerical cutoff as mathematically empty, and (ii)
treating a causal tilted cone as proof of bounded static-time energy. These
qualifications supersede broad interpretations of legacy health labels;
legacy evidence files and their original hashes have been preserved.

Still unproved for these particular reconstructed functions: nonlinear
canonical/Dirac closure and all primary/secondary constraints; global scalar,
vector and tensor stability and strong-coupling scales; full PPN including
preferred-frame terms; measured Newton constant and baryonic interior matching;
expanding viable FLRW using these same functions; cosmological matching and
the homogeneous/zero-field limits; lensing across a complete halo. The older
power-law clock's FLRW results cannot certify these different functions.
An extra clock field is present; no claim of a strictly two-field-mode theory
or a hidden nonpropagating scalar is made. The fitted \(a_0\)-\(\Lambda\)
coefficient remains un-derived. No new empirical fit or prediction is claimed.

Lean proves the abstract matching algebra with explicit hypotheses. It does
not prove those hypotheses are a law of nature. Execution success is distinct
from satisfying any of the missing physics requirements.

## Reproduction

### Concurrent repository update

While this calculation ran, Fable added L118 in `963df1491` and a comment
cleanup in `ce9b690df`. Its full script was read and rerun. Its transition-regime
warning is useful as a search suggestion, but three checks are literal `True`,
one counts checklist entries, and two check supplied elementary expressions.
It does not recompute the KGB principal matrix or certify the full checklist.
The new construction already has different failure locations: its tested
two-mass branch meets a boundary while both accelerations are below one. The
prior 60-digit healthy local jet at \(y=20\) also rules out reading the older
zero-pressure transition failure as a universal local KGB obstruction.

Two further transcription/scope issues must not enter this certificate:
the prior fixed-power halo used \(G\propto X^n\) with \(P=0\), not
\(P\propto X^n\); and a galactic no-slip statement alone does not derive a
Solar-System PPN parameter. The horizon coefficient in L118's G10 is not the
same as Carl's fitted \(\kappa=1/2\). Neither is derived by this work.
No concurrent Fable or unrelated working-tree file was changed here.

From this directory: `python3 -B run_suite.py`.
`run_001/manifest.json` records the exact commands, base revision, dirty state,
versions, bounds, input hashes and raw logs. The suite includes every new
script, the new conditional Lean file, and the previous pressure/closure suite.
`RESULTS.md` records important exit statuses, results and the file inventory.
