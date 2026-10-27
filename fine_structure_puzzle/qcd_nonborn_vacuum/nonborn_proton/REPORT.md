# FSP-009 proton non-Born result

The full physical proton response and the original alpha/R target remain
open. This package computes a new complete non-Born **finite photon band at
strict leading HB pi-N chiral order**, plus an exact low-energy reduction
and a source-formula covariant pi-N soft coefficient. It does not reuse the
19-point elastic functional or the same-loop sea temporal moment as a new
result. No measured alpha, fitted Q^2 curve or target value is inserted.

## Strongest executed result

Nevado--Pineda [0712.1294v2](https://arxiv.org/abs/0712.1294v2) supplies the
full Born-subtracted S1/S2 functions, not just one subtraction line. Their
Born convention matches WLCM directly. Equations (3.16),(3.18),(3.19) include
the seagull needed to restore the spatial current response. We integrate
both amplitudes over all Euclidean angles with a sharp photon ball or shell.
At the printed source strong-sector inputs specified below,

| Photon range | Dimensionless full-function J | K=D_u,HBpiN^NB/M | Full-function / leading-soft polynomial |
|---|---:|---:|---:|
| 0 < Q < 0.1 m_pi | 0.0000441500706723 | 1.94635361e-9 | 0.9993531713 |
| 0 < Q < m_pi/4 | 0.00171882501897 | 7.57743132e-8 | 0.9959997370 |
| 0 < Q < m_pi/2 | 0.0271853697681 | 1.19846564e-6 | 0.9845614315 |
| m_pi/4 < Q < m_pi/2 | 0.0254665447491 | 1.12269133e-6 | 0.9837988778 |

These digits describe the deterministic calculation of the declared leading
chiral sector. They are not a physical uncertainty estimate. The full-function
ratios show that this run uses finite momentum dependence beyond the earlier
soft polynomial. See [FINITE_BAND_DERIVATION.md](FINITE_BAND_DERIVATION.md),
[FINITE_BAND_CONTRACT.json](FINITE_BAND_CONTRACT.json) and
[finite_run_001/result.json](finite_run_001/result.json).

## Independent soft coefficient and source-formula calculation

For the complete renormalized QCD non-Born tensor at fixed positive pion mass,
the exact low-energy reduction is

    lim_(Lambda->0) [D_u,NB(0<Q<Lambda)/(M Lambda^4)]
      =3/(32pi M) [(alpha_E-beta_M)/u],       u=e^2.

The inelastic piece supplies `alpha_E+beta_M`; the independent subtraction
piece supplies `-2 beta_M`. An independent local E_E^2/B_E^2 photon
contraction yields the same coefficient. For strict leading chiral order,

    C_NB^LNA=9g_A^2/(8192pi^3 M f_pi^2 m_pi).

The source-authenticated AHLP [2005.09518v2](https://arxiv.org/abs/2005.09518v2)
ancillary notebook also permits evaluation of the **covariant pi-N-loop**
static coefficient. Only the two relevant symbolic assignments are parsed;
the notebook is never executed. At its printed strong parameters we obtain

    (alpha_E+beta_M)_piN/u = 0.7235084533 GeV^-3,
    beta_M,piN/u          =-0.2601115858 GeV^-3,
    (alpha_E-beta_M)_piN/u= 1.2437316248 GeV^-3,
    C_NB,piN             = 0.03955671794 GeV^-4.

The strict HB leading value is `0.05132564746 GeV^-4`, so this particular
covariant loop sector is 0.7707008075 times its HB leading limit. This change
illustrates why a converged quadrature cannot be equated with an EFT truncation
error. The covariant result and the finite HB band are different controlled
approximations; neither is relabeled as the complete physical response.
The order-m_pi/M logarithm cancels in the covariant pi-N polarizability
difference; exact series through its squared mass ratio were verified.

## Imported inputs, sea and matching

The only dimensionful numerical calibration is AHLP Table I's printed
`M=0.93827`, `m_pi=0.13957`, `f_pi=0.09221` GeV and `g_A=1.27`.
These are physically calibrated strong-sector inputs involving experimental
extraction/fits. Holding them fixed defines this local leading-u calculation;
their complete physical retuning/Jacobian is not reconstructed. No numerical
alpha, empirical Baldin sum, fitted delta-beta, Delta transition form factor,
or new form-factor/Q^2 fit is used.

The low-energy QCD tensor includes sea contractions; pion loops are not
identified with a single quark Wick topology. The calculation never assumes
the entire sea is an elastic disconnected vertex. Heavy-flavor effects and
higher chiral operators remain encoded in independent EFT information outside
the evaluated leading SU(2) sector. The independent polarizability contacts
and local scalar/gluonic full-mass matching terms are not discarded from the
physical answer. Finite mass/strong matching along fixed MSbar parameters and
the common vacuum/proton path remain required.

## Verification and provenance

Both new calculations use the installed computation-audit v2 runner, with
contracts and code fixed before execution. `run_001` completed 41 checks;
`finite_run_001` completed 20. Both manifests validate against current input
hashes. Checks include two independent normalizations, source notebook versus
real-form branch comparison, exact chiral series, numerical angular cases,
finite-function parameter-integral versus arctangent comparison, both scalar
soft limits, nested 12/24/48 quadrature and independently integrated shell
partition. The last relative quadrature changes in the largest band/shell
are about 3e-32; this is a convergence diagnostic, not a rigorous analytic
error bound. No higher-order chiral uncertainty was computed.

Caps: the soft run had 90-second wall and 80-second CPU limits; the finite
run had 120-second wall and 110-second CPU limits. Both cap output at 1 MiB
and numerical threads at one. No RLIMIT_AS is requested on macOS. Commands
and exact dependencies are in [REPRODUCE.md](REPRODUCE.md).

Declared ancestry is FSP-008 and BASELINE revision `3ac0427...`. Both runners
observed current HEAD `aa0d1a83d15c1fe2a0c9d32f189bdbbff49dd19a`, dirty.
This worker performed no Git mutation. The observed revision drift is
reported rather than overwritten; the per-file before/after input hashes
are the actual execution provenance.

Interpretation: implementation and finite assertions verified within the
declared numerical range, conditional on mpmath accuracy and imported source
formula correctness. External primary formulas and their conventions were
checked directly. Fresh independent review is delegated by the coordinator;
its outcome is not presumed here.

## Exact missing physical leaf and continuation

The smallest new low-energy leaf is the complete QCD
`(alpha_E-beta_M)/u` at the chosen strong calibration, beyond its computed
pi-N sector. It needs the independent magnetic response as well as the
electric response, with sea coverage and EFT contact matching. For the entire
non-Born proton mass derivative, the required input is the full renormalized
two-variable t1/t2 tensor over Q and imaginary energy, or full inelastic
structure functions plus an independent subtraction function, all sea terms
and finite scalar/gluonic mass matching on the common path. No inspected
lattice source supplies that complete package.

The data route remains open. Resume when a public full-tensor dataset with
contraction/current-normalization metadata and its matching path is available,
or when individual direct-QCD+QED mass-versus-coupling data and their retuning
Jacobian are authenticated. Further EFT improvement could add independently
calibrated Delta/recoil contributions and polarizability contacts; it would
remain an EFT calculation with disclosed inputs. The independent curved
vacuum response is also still needed to obtain R(alpha).
