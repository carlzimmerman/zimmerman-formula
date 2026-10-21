# Vector/metric agent: derivation provenance and independent companion audit

2026-10-20. Base `9a9ab4032`; frozen criteria commit `2591280c8`.
No script, scan, build, Lean edit or compilation was used for this review.
No shared status file or git commit was changed by this agent.

**Verdict.** The final reports pass the bounded analytic scopes checked
below. No required correction remains. They provide neither a healthy
microscopic completion nor an independently selected amplitude. The
interacting continuum/Lorentzian quantum bridge, general SCFT/gauging
possibilities and a protected physical scalar charge remain open.

## Independence and source scope

I authored `PHYSICAL_METRIC.md` and `SOURCES_METRIC.md`; this file does not
present my own report as an independent review of itself. Its metric
inverse, source/test charge, stress-source/Ward identity, force dictionary,
cone distinction and unit conversions were derived before reading the
companion reports. The coordinator and both companion agents separately
reported independent checks of that algebra; their own reviews supply
the corresponding independent provenance.

I independently reconstructed the gauge and quantum calculations below
from their displayed actions, operators and regulated integrals. Their
source cards were read to check separation of primary results from new
applications. I did not independently reauthenticate every external gauge
or quantum source pin. For the metric source cards I did authenticate the
exact Bekenstein version headers and specified equations online; no
full source was downloaded or copied into tracked files.

## Gauge companion: ensemble, operator and force checks

Starting with the stated positive chamber t=m0+c sigma, the cubic
prepotential multiplies derivative/gauge/CS operators. It is not a sigma^3
potential. The component coefficient c epsilon AFF/24 equals c AFF/6 in
form notation. For A=A0(x)dt, F=dA0 wedge dt and F wedge F=0. I requested
the correction of an initial exterior-derivative sign typo; the final
report has the correct sign. The pure-electric zero-CS conclusion was
unaffected by that typo.

For the explicitly added potential kappa sigma^3 and dielectric C sigma,
direct stationarity gives sigma=sqrt(C/(6kappa))|E| and
C_E=C^(3/2)/(3sqrt(6kappa)). The independent fixed-D calculation gives

    H=D^2/(2C sigma)+kappa sigma^3,
    D^2=6C kappa sigma^4,
    H_min=4kappa^(1/4)|D|^(3/2)/(6^(3/4)C^(3/4)).

Its second sigma derivative is positive and its endpoint divergence for
D nonzero proves the unique positive global minimum. This does not
eliminate the retained scalar-gradient term or justify the derivative
expansion by itself. The canonical coordinate and mass,
chi=(2/3)sqrt(C)sigma^(3/2) and m_chi^2=9kappa/(2C), check out. The added
N=1 Kähler/superpotential example gives kappa=2|y|^2/C and introduces a
new coefficient; its global Wilson-line qualification is necessary.

Eliminating Y from T Y^2/2+zeta Y gives V_FI=zeta^2/(2T). Without the
cubic potential there is no finite positive fixed-E stationary point.
With it, sigma0^4=zeta^2/(6C kappa), epsilon=4kappa sigma0^3 and
the exact positive sigma(E)^2 root and its displayed expansion agree.
In particular, the E^4 coefficient is C^2/(96kappa sigma0), and the IR
response is quadratic. Positive rigid potential energy is properly
distinguished from a derived supersymmetric gravitational completion.

The cross-regime number 16/27 uses electric Lagrangian coefficients.
The electric Hamiltonian H(E)=E.L_E-L has twice the high-field cubic
coefficient and gives 64/27 for that differently defined combination.
Both have the wrong IR/UV assignment and lack the attractive scalar map;
neither is the operational R requested by the frozen criteria.

Varying L(E)-rho_q V, E=-grad V, gives div D=rho_q and test force qE.
Positive source and test charges therefore repel. Reversing the potential
convention changes both source and force together. The n-dimensional
radial power, the separate BPS-shaped sigma profile and the circle identity

    A F F=[3a F4 F4-2d(a A4 F4)] wedge dy

also check. Quantized integrated CS charge is not a local universal
attractive constitutive relation. The source-backed ungauged minimal
supergravity example retains a Maxwell pure-electric sector and Ricci-flat
zero-field vacuum. None of these statements excludes all interacting fixed
points, gaugings or compactifications; the final report keeps that scope.

## Quantum companion: spectrum, subtraction and zero-mode checks

The sphere spectrum can be checked directly: polar decomposition of the
flat Laplacian on a degree-l homogeneous harmonic polynomial gives
l(l+D-1)/r^2, and subtracting traces from homogeneous polynomials gives
the displayed degeneracy. Thus d_l grows as l^(D-1), and a kth mass-source
derivative has summand order l^(D-1-2k). Its convergence condition is
exactly 2k>D. In D=4 the twice-subtracted logarithmic tail is O(l^(-3)),
analytic inside the positive gap, with the stated positive third derivative.
This sign is conditional on the stated local counterterm contract;
arbitrary higher-dimension finite matching data are not covered.

For a smooth Phi=s Phi_* profile, B=lambda_s^2|grad Phi_*|^2 is bounded
and positive. The bound
K0=A0^(-1/2)BA0^(-1/2)<=||B||A0^(-1) implies a summable cube of its
eigenvalues in D=4. It justifies the cubic relative-determinant remainder
and local analytic series. The noncommuting trace-cube expression for
Gamma''' is correct for real t with A_t>0. When m0=0, the constant-mode
Schur complement is t[b00+O(t)] with b00>0. Hence the one-loop result has
log t plus analytic terms, rather than t^(3/2). The positive-gap and
zero-mode alternatives are not being conflated.

The bounded quartic zero-mode integral is entire before taking its
logarithm and positive on the real axis. Its displayed moments, linear
coefficient and negative variance curvature follow by elementary
integration/differentiation. For a finite positive-measure regulator with
an affine source, W''=-Var(O)/V. The finite-cutoff smooth-profile integral
has the same local analyticity. These facts do not prove an interacting
continuum limit or a Lorentzian local static constitutive law. The final
wording correctly describes a Euclidean zero-mode/finite-cutoff model,
not a newly constructed full Lorentzian interacting invariant state.

For the complete renormalized invariant quantum sector, uniform sphere
scaling gives epsilon=W-H partial_H W/4. The displayed local W(z,R)
stress tensor has the correct derivative and curvature signs; at constant
curvature it gives epsilon=W-R W_R/2. Finite cosmological/Einstein data,
the calibrated gravitational coefficient and a separate bare EH action
remain distinguished. An isolated zero-mode normalization cannot supply
the claimed gravitating vacuum energy. No positive leading C3 or actual
UV C2 is derived for this route, so no operational amplitude is predicted.

## Final artifact pins and remaining implication

After rereading the final changes, the following saved SHA256 values were
checked directly:

| Artifact | SHA256 |
| --- | --- |
| `PHYSICAL_METRIC.md` | `893549d913e3004be8736c9398652682790af8271696e3c420cf1b206799f025` |
| `SOURCES_METRIC.md` | `6a54e7c17254de85448f6a551fac4213e1f8fae71fe4958a6e7275badae1e97e` |
| `PROTECTED_GAUGE.md` | `e4718501c859289174ec7c185dde545be5e4384859a650b3517403c560c39e01` |
| `SOURCES_GAUGE.md` | `12cb7ea49da8eb8897256af5720bc412a02b6d0cfa9eb88424072fc6c122c5ea` |
| `QUANTUM_STATE.md` | `0a9f2b6e14b3fff3bea8a01ce7e8df14a58eb8c7cef31981f2162d70bf41a4fb` |
| `SOURCES_QUANTUM.md` | `e49b68ca26bbc72e0557e6ce5d652a81f63c51703cfb5ab55e2fd499b536b95e` |

The remaining selection implication is precise: a microscopic construction
must connect a healthy, correctly sourced IR cubic and actual UV Newtonian
response to the same positive gravitating vacuum, while fixing the
canonical matter charge and finite matching data independently. A protected
CS coefficient, gamma=1 metric shape, variance identity or arbitrary finite
counterterm does not supply that implication. The scoped failures here do
not constitute a universal no-go theorem outside the stated actions,
ensembles, regulators and subtraction assumptions.
