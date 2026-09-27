# CD26-3: inverse lapse reconstruction and what it can identify

Requested base: `7daaa5426076a2d78a50f3316007c7093255ce9a` plus the existing
CD26-2 work. The shared repository had advanced to
`b3ba1f6fa0c9a2affca81f32ce62810a15fe689e` when this audit began; the manifest
records its actual execution commit. Only this new directory is written.
The operative target remains filtered `nu_mono` with preferred-foliation
criterion B. This inverse concerns the **separately constructed spectral
cosmological sector**; it does not establish its splice to that target.

**Finding:** a positive lapse profile determines a spatial balance function.
It identifies a unique constant vacuum coefficient only after the source,
geometry, expansion convention, and action coefficients are calibrated.
There are exact families with the same lapse, proper expansion, and matter
profile but different vacuum coefficients when the trace coupling is unknown.
Thus this construction currently supplies a reconstruction test, not a
prediction of the magnitude of dark energy.

## 1. The inverse and its domain

The CD26-2 sector has, in barred canonical variables,

\[
 H=\int\sqrt{\bar h}\,N[\mathcal A-b|D\log N|^2],
 \qquad N=e^S>0,\quad b>0.
\]

For a positive C2 lapse on a known Riemannian leaf, define

\[
 y=\sqrt N,\qquad
 J[N,\bar h]=-4{\bar\Delta y\over y}
 =-2\bar\Delta S-|DS|^2.
\]

The lapse equation gives `A=bJ`. This is the direct inverse: no eigenvalue
solver is needed if the full positive profile and geometry are known. It
determines **A/b**, not b independently. A spatially constant rescaling
`N -> c(t)N`, `c>0`, leaves J unchanged. Normalizing `integral y^2=1` only
chooses the shape convention; the independent global scale c remains.
This spatial invariance does not require assuming that the full Dirac theory
has already proved c to be a gauge freedom.

The original pin chart can require a nontrivial constant shift of S. For the
exact cosine family, `y -> exp(S_bar/2)y` with
`S_bar-2|epsilon|>-2wc`, `wc<0`, retains `0<u=(S+2wc)/(S+wc)<1`.
This shift changes neither J nor the reconstructed balance. It is not a
measurement of a vacuum coefficient.

At `N=0`, the quotient and `ln N` are undefined. The zero function solves a
homogeneous eigen-equation trivially and determines no potential; it is not
an admissible lapse. Even a smooth nonnegative N with isolated zeros cannot
silently be inserted in this inverse. For example, signed `y=sin x` solves
`(-4b Delta-4b)y=0`, but `N=sin^2 x` vanishes, `sqrt N=|sin x|` is not C2,
and zero is an excited eigenvalue: the constant ground state has eigenvalue
`-4b`. Positivity and the smooth global square root are essential hypotheses.

In observational language, N is the lapse relative to the chosen clock
foliation. An expansion history alone is not a measurement of its spatial
profile. Reconstructing J needs the foliation/metric correspondence and
spatial distance scale, not just coordinate samples of N. On a torus whose
physical side is `2pi L`, an angular profile carries a `1/L^2` Laplacian
factor; without that length calibration the data constrain `b/L^2`.

## 2. Expansion signs and the inferred constant

In the flat, trace-only sector with matter initially at rest,

\[
 \mathcal A=-\ell q^2+\bar\Lambda+\rho(x),\qquad
 \boxed{\bar\Lambda(x)=\ell q^2-\rho(x)+bJ(x).}
\]

Here `q=pi/sqrt(hbar)` is a canonical trace momentum, not an observed energy
density. Direct Hamiltonian variation gives

\[
 \dot{\bar h}_{ij}\big|_{\rm trace}=-2\ell Nq\,\bar h_{ij},
 \quad\bar K=-3\ell q,
 \quad\bar H_{\rm proper}=-\ell q.
\]

For `ell>0`, negative q means expansion and positive q means contraction.
The lapse constraint depends on `q^2` and cannot choose that sign. A measured
expansion sign supplies information absent from the lapse equation.

The physical clock lapse on the constant pin is `N_phys=exp(wc)N`, and
`h_phys=exp(2wc)hbar`. Therefore

\[
 H_{\rm phys}=-e^{-w_c}\ell q,\qquad
 \bar\Lambda(x)={e^{2w_c}H_{\rm phys}^2\over\ell}
                 -\rho(x)+bJ(x).
\]

Equivalently the first numerator is `Hbar_proper^2`. Coordinate expansion
instead obeys `H_coordinate=N Hbar_proper` at zero shift; it cannot be used
in this formula without the lapse conversion. Multiplying N alone while
holding coordinate metric derivatives fixed changes the inferred proper
expansion; a time reparametrization must transform both consistently.

These are **barred Hamiltonian units**. An ordinary rest density enters the
canonical action through its full minimal-coupling normalization; the volume
and lapse transformation includes an `exp(4wc)` factor. Any overall
gravitational/source coefficient must also be retained. Neither this inverse
nor the spectral constraint derives the relation between ell, b, and measured
`G_N` in the operative static sector. Equating the barred density, bare
Einstein coefficient, or ell with their measured counterparts would supply
an additional assumption rather than identify dark energy.

## 3. Curvature and traceless momentum cannot be discarded generically

The parent IC20 canonical action includes the traceless term and curvature.
For the IC28 constant-tensor branch, m=1, fixed pin `wc`, and the same changed
spectral coefficients, divide `t=2exp(S-2wc)` and
`v=exp(S+2wc)/2` by `N=exp S` to obtain

\[
 t_* =2e^{-2w_c},\qquad v_*={e^{2w_c}\over2},\qquad t_*v_*=1.
\]

Writing `sigma^ij=pi_TF^ij/sqrt(hbar)`, the corresponding balance is

\[
 \mathcal A=t_*|\sigma|^2-\ell q^2+\bar\Lambda-v_*\bar R+\rho,
\]
\[
 \boxed{\bar\Lambda(x)=\ell q^2-\rho-t_*|\sigma|^2
                  +v_*\bar R+bJ.}
\]

The trace expansion relation above is unchanged because the momentum
derivative of the traceless kinetic term has zero trace. The inverse must
nevertheless subtract its contribution to the constraint and include the
spatial curvature. A nonconstant q also requires the spatial momentum
constraint and any accompanying matter current; it is not freely assignable
with zero traceless momentum and matter at rest.

This extension is conditional on that same explicit pinned coefficient
family and the already stated auxiliary reduction. A different action,
pin-off region, additional matter term, or nonconstant pin requires its own
Hamiltonian before using this formula.

## 4. Exact non-identification families

These are different inverse parameter/data choices, not claims that different
actions are dynamically equivalent.

**Constant source offset.** For any allowed d,
`Lambda_bar -> Lambda_bar+d`, `rho(x)->rho(x)-d` leaves A, N, and q unchanged.
Choose d small enough to preserve source positivity. This is an exact
single-slice degeneracy. Ordinary matter's independently measured density,
pressure, conservation law, or subsequent evolution can break it; it is not
a proof of equivalence between dust and a vacuum component at every time.

**Unknown trace coupling, even with the source known.** Let H>0 and b be fixed,
choose a positive periodic lapse y, and take

\[
 \rho(x)=\rho_0+bJ(x),\qquad
 q_\ell=-{H\over\ell},\qquad
 \bar\Lambda_\ell={H^2\over\ell}-\rho_0.
\]

For every admissible positive ell this gives the same N, source profile, and
barred proper expansion H. The inferred constant strictly decreases with
ell. This remains a continuous degeneracy inside any open admissible
coefficient interval; one need not cross a kinetic or chart boundary to
demonstrate it. Other action conditions, such as an auxiliary positivity
bound, still restrict which ell values belong to the candidate family.

The sign need not be identified either. Keep
`y=exp[(1/10)cos x]`, `b=1/5`, `rho=1+bJ>0`, and `H^2=1/10` fixed.
Then the same profile, source, and expansion admit

| ell | Inferred Lambda_bar |
|---:|---:|
| `1/20` | `1` |
| `1/10` | `0` |
| `3/20` | `-1/3` |

All three lie within `0<ell<1/3`, hence within the basic auxiliary-sign
interval `ell<t_*/6` for `wc<0`. The remaining embedding requirements are
still independent checks. Positive lapse, positive matter, and expansion
therefore do not themselves identify even the vacuum coefficient's sign.

**Canonical/source normalization.** For a positive kappa, the replacements

\[
 (\ell,b,\bar\Lambda,\rho,q)\mapsto
 (\kappa\ell,b/\kappa,\bar\Lambda/\kappa,\rho/\kappa,q/\kappa)
\]

leave N and `-ell q` unchanged while scaling the whole lapse operator by
`1/kappa`. If a measured physical density has an uncalibrated source weight,
this illustrates the remaining normalization ambiguity. Independent
measured-G/source calibration can break it. These are coefficient choices
across a family, not a declared symmetry of one fixed action.

**One eigenvalue does not determine a potential.** On a `2pi` flat torus,

\[
 y_{\epsilon,n}=e^{\epsilon\cos(nx_1)},\quad
 \mathcal A_{\epsilon,n}
 =4b\epsilon n^2\cos(nx_1)-4b\epsilon^2n^2\sin^2(nx_1),
 \quad n=1,2,\ldots
\]

give infinitely many distinct smooth potentials with the same zero ground
eigenvalue. The positive-ground-state integration identity proves the
ground-state statement; it is not an assertion based on a finite spectrum
sample. The density `rho0+A` is positive if
`rho0>4b n^2(|epsilon|+epsilon^2)`. The eigenspace is one-dimensional for each
such fixed potential, but the inverse map from the number `lambda0=0` to
the potential is highly nonunique.

## 5. Useful reconstruction tests and torus identities

With N>0, known geometry and calibrated coefficients, the pointwise inferred
`Lambda_bar(x)` must be spatially constant. This is a falsifiable consistency
test. If it is constant, substituting it back proves the lapse constraint
on that slice; it does not prove the momentum constraints or evolution.

For flat constant q, the exact condition is
`rho(x)=bJ(x)+rho0`. If J is nonconstant and the source normalization is known,

\[
 b={\operatorname{Cov}(\rho,J)\over\operatorname{Var}(J)},
 \qquad \rho_0=\langle\rho\rangle-b\langle J\rangle.
\]

The fitted pointwise residual must still vanish; a covariance slope alone is
not a successful fit. If J=0, a constant-q source must be constant and b is
unidentifiable. In the exact cosine family, for n=1,
`mean J=-2epsilon^2` and
`Var(J)=2epsilon^2(4+epsilon^2)>0` when epsilon is nonzero. An extra source
term `d cos(2x)` with the same q,N gives a nonconstant inferred Lambda and is
retained as a negative control.

On a compact leaf without boundary, direct integration gives three different
and compatible identities:

\[
 \int y\mathcal A=0,\qquad
 \int\mathcal A=-b\int|DS|^2\le0,\qquad
 \int N\mathcal A=4b\int|Dy|^2\ge0.
\]

Thus a nonzero continuous A admitting a positive periodic solution must
change sign. A constant A forces A=0 and y constant. For flat constant q,

\[
 \bar\Lambda=\ell q^2-\langle\rho\rangle_y
 =\ell q^2-\langle\rho\rangle-b\langle|DS|^2\rangle,
\]

where the first average is weighted by y, not N. In particular,
`Lambda_bar<=ell q^2-mean rho`, with strict inequality for a nonconstant
lapse. If the complete density is known but the lapse is not, let
`lambda_rho=lambda0(-4b Delta-rho)`. The global spectral balance is

\[
 \bar\Lambda=\ell q^2+\lambda_\rho,\qquad
 -\rho_{\max}\le\lambda_\rho\le-\langle\rho\rangle.
\]

The lower bound is the nonnegative-gradient Rayleigh bound; the upper bound
uses a constant test function. These are useful bounds, not a unique inverse
from a measured expansion alone.

For a region with boundary, the omitted fluxes matter:
`integral yA=-4b integral_boundary partial_n y`,
`integral A=-2b integral_boundary partial_n S-b integral |DS|^2`, and
`integral N A=4b integral |Dy|^2-4b integral_boundary y partial_n y`.
The torus formulas therefore cannot be exported without boundary data.
Without specified boundary conditions even a fixed potential need not fix
the lapse shape: on an interval, A=0 admits every positive affine y.
For fixed periodic A and positive solutions, multiplying the transformed
equation for their ratio by that ratio gives zero weighted gradient energy,
so connectedness fixes the shape up to a constant. Noncompact spectral gaps,
normalizability, and boundary prescriptions are not supplied by the torus
construction.

## 6. What observations would remove which ambiguity

| Inputs, assuming the sector is applicable | Identified | Still missing |
|---|---|---|
| Positive lapse shape and spatial geometry | J=A/b | b and the split into source, curvature, kinetic and vacuum terms |
| One ground eigenvalue | One global balance | The potential/profile; infinitely many counterexamples above |
| Full N, calibrated rho, constant-q slice | b and source intercept if J varies | ell versus Lambda if only proper H is known |
| N, proper H, rho, curvature/shear, all action/unit calibrations | Pointwise inferred Lambda and its constancy test | Whether the sector evolves and embeds in the operative theory |
| Several independent calibrated slices | Potentially ell,b,Lambda together | Sufficient rank and a valid common action across those slices |

For the last row, absorb known traceless/curvature terms into
`rho_eff=rho+t_*|sigma|^2-v_*Rbar`. Then

\[
 \rho_{\rm eff}={1\over\ell}\bar H_{\rm proper}^2+bJ-\bar\Lambda.
\]

Determination of the three constant parameters requires rank three in the
columns `(Hbar_proper^2,J,-1)` across the observations. One spatial CMC slice
has its first and third columns proportional, so more precision on that slice
cannot distinguish ell from Lambda. Multiple slices with genuinely
independent values can remove the algebraic degeneracy, but a rank test does
not establish a physical cosmological history. If canonical q were directly
known instead, the corresponding columns would be `(q^2,J,-1)` for
`(ell,b,Lambda)`.

The inversion differentiates the lapse twice. At fixed geometry,
`delta J=-2Delta(delta S)-2DS.D(delta S)`: a short-wavelength perturbation
can generate a large inferred balance. Actual data reconstruction therefore
needs derivative uncertainties, spatial resolution, and independent source
calibration before interpreting a nonconstant residual as new physics.

## 7. Evidence and certification boundary

`check.py` independently verifies the inverse, proper-expansion factors,
general curvature/traceless terms, exact counterfamilies, torus-average
identities, negative controls and identification-rank examples. The initial
run uses a 60 s wall cap and 50 s CPU cap; no random sampling or simulation
campaign is used. `SpectralInverse20260926.lean` formalizes scoped real-algebra
consequences, including distinct inferred constants with the same observations.
Run status, hashes and final compiler results are recorded in `EVIDENCE.md`.

Authoritative local dependencies are the actual changed Hamiltonian and
conventions in `closure_push_2026_09_26/spectral_lapse/RESULT.md`, the canonical
map and Hamiltonian in `IC20_JOINT_COMPLETION.md:44-59,91-105`, and the explicit
constant-tensor action change in `IC28_CONSTANT_TENSOR.md:10-37`.
Continuum integration arguments here use their stated smoothness and boundary
hypotheses; they are not mislabeled as Lean PDE theorems. No measured vacuum
density, a0–Lambda coefficient, full constraint count, or observational fit is
derived by these inverse identities.
