# Density changes the lapse length through compactness

2026-09-11; base `bce18ba18`. **Full theory OPEN.**

Carl Zimmerman's primordial-clock direction and question about getting the
recombination clock sector out of galaxies motivate this test. No particles,
new coefficient functions, or fitted thresholds are introduced. The same
P/W/V functions are used. They remain previously reconstructed functions,
not coefficients selected from first principles.

The existing `dirac_operator/` already proves all-domain principal
ellipticity. We did not repackage that result as a new breakthrough. This
calculation instead determines the density-dependent zeroth-order coefficient
and computes a restricted radial spectrum.

## Exact action-derived equation

For the gamma=0 stationary branch, the preserved lapse equation contains

\[
\boxed{\mathcal M_N^2(\rho_b)=
\frac{9H^2(1+m)(1-v)}{m(m+2)}
+\frac{1+m}{2mM_*^2}\rho_b.}
\]

Here \(\mathcal M_N^2\) is the local inverse-length-squared coefficient of
the lapse operator, **not the MOND interpolation function**. Units are c=1;
\(M_*\) is the reduced Planck mass. The Python/Lean argument `M` denotes
\(M_*^2\), and m,v are the existing clock-background coordinates.

The radial operator, with regular metric \(ds_3^2=A_r(r)^2dr^2+r^2d\Omega^2\), is

\[
\mathcal L_N=-\frac{1}{A_r r^2}\partial_r
 \left(\frac{r^2}{A_r}\partial_r\right)+\mathcal M_N^2(r).
\]

Do not identify its inverse length with the zeta-constraint length in
`../constraint_length_2026/REPORT.md`, or with an observable force pole.
They arise after different eliminations. Neither length alone determines a
metric response, halo equilibrium, or clock-dust depletion.

### Hypotheses and derivation

We use the already varied spherical covariant action through
`../nonlinear_evolution_2026/equations.py`. The initial-slice family has
R=r, Kr=Ko=H, Q=q spatially constant, chi_r=0 and initially resting baryons.
The clock background jets must satisfy their background/clock constraint.
The radial Hamiltonian constraint is solved for the radial metric derivative
before elimination of the time rates. Momentum is zero on this family.
This is nonlinear in baryon density and metric, but not an arbitrary-gradient
halo or a static solution. All inverse denominators and the metric patch
must remain regular.

The actual linear system has unknowns (Kr_dot,Ko_dot,Qdot,Nrr), and forcing
columns (Nr,N,constant). We solve it, extract its N coefficient, and divide
by the squared radial metric coefficient. An independent identity verifies
that the Nr coefficient is A_r'/A_r-2/r, giving the displayed spatial
Laplace–Beltrami operator. Both raw Einstein evolution and its Hamiltonian-
constraint-added form yield the same physical coefficient after imposing
that constraint.

Before choosing the stationary coefficients, the exact density slope is

\[
\frac{\partial\mathcal M_N^2}{\partial\rho_b}
=\frac{W}{2M_*^2(W-2q^2W_Y)}.
\]

With U=mqA, W(0)=U and d=W_Y(0)=AU/[2q(qA+U)], it becomes
(1+m)/(2m M_*^2). The full background term uses B=A(m+2)/(qm),
qdot=-3AHv/B-qU/(2M_*^2 H), and the actual time-chain rule
P_Xt=-(3HA+B qdot)/(2q). SymPy checks the complete boxed formula, not
just the density slope.

The general cubic density slope is also derived from the actual matrix and
saved in `run_002/density.json`; its gamma->0 limit agrees exactly. The
gamma=1e-6 sample is not evaluated by substituting the zero-cubic slope.

## Lean restriction on a density-only shortening mechanism

Define B_bg=\(\mathcal M_N^2(0)R^2\) and the local density-radius proxy
\(C_\rho=\rho_b R^2/(3M_*^2)\). For m=1/10, the exact identity is

\[
\mathcal M_N^2 R^2=B_{\rm bg}+\frac{33}{2}C_\rho.
\]

Consequently,

\[
\boxed{B_{\rm bg}\le\epsilon,\quad \mathcal M_N^2R^2\ge1
\quad\Longrightarrow\quad
C_\rho\ge\frac{2(1-\epsilon)}{33}.}
\]

For B_bg<=0.01 this requires C_rho>=0.06. For B_bg<=0.01 and
C_rho<=1e-5, the budget is below one: this particular local lapse length
cannot lie inside R. Those inequalities are Lean-checked over the reals.
For a uniform-density ball C_rho equals 2G M_b/R in c=1 units. For a
Gaussian or a general profile it is **not** the enclosed-mass compactness;
the latter uses an integral of rho. These are illustrative conditions, not
galaxy observations or a fit to data.

Seven theorems in `DensityCompactness.lean` also include positive gap for
H>0,M_*^2>0,m>0,v<1,rho>=0, and the exact selected-epoch formula
\(\mathcal M_N^2=44/7+(11/2)\rho\) in the repository's M_*^2=1 units.
`run_checks.py` reads the actual Lean definitions of both slope and full gap
and compares them to the action-derived expressions.

## Numerical check and the precision failure

Twenty-four Gaussian families use widths .03,.003,.0003, peak-density times
width squared 1e-6,1e-4,.01,1, and gamma=0 or 1e-6. No profile is a data fit.
Their spatial metric is generated from the enclosed baryon density:

    A_r^-2 = 1 - (1/r) integral_0^r rho(s) s^2 ds     (M_*^2=1).

The field equations are evaluated before Hamiltonian elimination as an
independent assembly check. The original 33-radius float64 check fails its
1e-8 tolerance in four small-radius/low-compactness cases; those failures
remain recorded. A 60-digit spatial calculation at three radii per family
reduces the gap-identity mismatch below 2.2e-15 and normalized constraint
residual below 8.1e-17. The background constitutive jets still come from
float64; this is not a 60-digit cosmological solution or interval proof.
The fixed-background density slopes are 5.5 and approximately 5.4996102193
for the two couplings. This small cubic correction does not move the tested
density-radius budgets across the order-one threshold.

The high-density control rho_center R^2=1 does reach a budget above one;
it is deliberately retained. The result is not that density can never
shorten the length. It is the compactness restriction on doing so.

## Radial spectrum: boundary conditions and scaling are explicit

`spectrum.py` consumes the pinned `run_002/density.json`, not a manually
assigned gap. For gamma=0 it builds a cell-centered finite-volume operator
with volume weight A_r r^2, face flux r^2/A_r, regular center flux and outer
radius 10R. Outer Dirichlet and Neumann conditions are separate cases.
Three eigenvalues are computed, not assigned, at 64,128,256 cells.

For rho(r)=eta R^-2 exp[-(r/R)^2] and fixed eta, the metric in x=r/R does
not depend on R. Hence the scaled operator has the exact form

\[
R^2\mathcal L_N=\mathcal L_\eta+R^2\mathcal M_N^2(0)I,
\quad
R^2[\lambda_j(R)-\mathcal M_N^2(0)]=\lambda_j(\mathcal L_\eta).
\]

This is a structural similarity relation, not a new measured law. The 72
mesh/profile/boundary cases check its implementation. The zero-density flat
Dirichlet-ball eigenvalue pi^2/(10R)^2 supplies an independent benchmark
with observed second-order convergence. The Neumann zero-density case
retains the constant spatial mode and its positive background gap; it is
not silently discarded. This is not the spacetime k=0 Dirac count.

Integration by parts for regular test functions satisfying the stated
homogeneous boundary conditions gives

    integral u L_N u A_r r^2 dr
      = integral (r^2/A_r)(u')^2 dr
        + integral A_r r^2 M_N^2 u^2 dr
      >= M_N^2(0) integral A_r r^2 u^2 dr.

`SpectrumBound.lean` proves the final Rayleigh/no-zero-energy algebra under
its nonnegative-energy hypotheses. It does not formalize the integration,
Sobolev domain, boundary traces or the covariant action. Positive radial
spectra on these slices are not full nonlinear Dirac or stability closure.

## Answer and next missing calculation

The density-only, initially homogeneous-clock route is restricted by
compactness, not by galaxy mass alone. It has not provided the required
mass-dependent clock-dust evacuation. **This is a conditional obstruction,
not a no-go for the entire framework or a completed gravity theory.**

The next genuinely different calculation needs nonzero, dynamically justified
clock gradients and a conserved primordial charge budget: solve their coupled
constraints and test whether they alter the density-radius restriction without
introducing an unhealthy mode or unacceptable geometry. Arbitrarily inserting
a clock gradient or changing m to hit a halo size is not that mechanism.
The earlier radial evolution tangency problem still blocks trustworthy
late-time evacuation claims; no result from that evolution is used here.

No exponential MOND law, a0-Lambda coefficient, CMB likelihood, empirical
novelty, PPN completion, or complete Lean proof of gravity is claimed.

## Reproduction and audit

All created files are in this directory. Existing theory files are unchanged.
Primary files are `density_gap.py`, `test_budget.py`, `run_checks.py`,
`DensityCompactness.lean`, `spectrum.py`, `test_spectrum.py`,
`SpectrumBound.lean`, this report, and the two contract JSON files.
`run_001` is an earlier source checkpoint; final coefficient evidence is
`run_002`. Spectrum evidence is separately pinned in `spectrum_001`.
Exact argument lists, input/output hashes, software, resource limits and
stdout/stderr are in those manifests and `run_002/checks.json`.

Development: budget and spectrum tests initially failed for missing code,
then passed. The float64 action check exited 1 and its parameters were
isolated; the precision control was added rather than loosening its tolerance.
Lean's initially redundant tactics produced warnings; they were removed.
No failed computation is counted as a successful physics test.

Final verification (each listed command exited 0):

| Check | Evidence |
| --- | --- |
| Action-derived gap and 24 Gaussian families | `run_002/density.json` |
| Two budget unit tests | `run_002/checks.json` |
| Seven new density/compactness Lean theorems | `run_002/checks.json` |
| Existing symbolic and Lean ellipticity tests | `run_002/checks.json` |
| 72 radial spectral cases and flat-ball unit test | `spectrum_001/result.json`, stdout/stderr |
| Two new Rayleigh-bound Lean theorems | `spectrum_001/stdout.txt` |
| Both final manifests validated against current inputs | `run_002/manifest.json`, `spectrum_001/manifest.json` |

The maximum absolute discrete eigen-residual is 4.794e-13; the maximum
scaled-spectrum similarity error is 5.412e-13. These are finite-mesh
checks, not interval-certified continuum error bounds. All nine new Lean
theorems report only `propext`, `Classical.choice`, and `Quot.sound` as
axioms; none uses `sorryAx`. The action-to-Lean bridge is symbolic Python,
not a formalized variational calculus.

An independent read-only reviewer checked the action-to-gap normalization,
P_Xt chain rule, Lean hypotheses, density-radius interpretation and the
finite-volume weights/boundaries. Requested Laplace–Beltrami and provenance
clarifications were implemented. Mathbox self-review separated exact action
algebra, conditional formal proofs, numerical samples and missing physical
implications. No global novelty claim or external theorem was imported.
