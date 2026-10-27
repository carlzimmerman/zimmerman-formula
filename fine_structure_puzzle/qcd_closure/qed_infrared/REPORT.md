# FSP-005 physical electromagnetic infrared result

The actual order-e² QCD current-current metric insertion has zero linear-H
projection **conditional on uniform curved-space locality, mixed metric-current
clustering, a controlled global-state remainder, and differentiated limits**.
A positive flat hadronic gap alone does not prove these inputs. This result
is not a full-QCD no-go and does not determine A_ρ(α)/m_p³.

The raw derivation is `DERIVATION.md`. It keeps the photon propagator variation,
TJJ contacts, parameter matching, photon determinant and canonical global gauge
volume in the metric response. No susceptibility is substituted for stress.

The concrete new diagnostic is the exact coexact Maxwell spectrum on S4,
λ_l=H²(l+1)(l+2), d_l=l(l+3)(2l+3)/2. Analytic continuation gives

    ζ_T(0)=19/30,      ζ_T(-1)=5/63.

The scalar ghost has its constant eigenfunction excluded. Dividing by the
constant gauge transformation supplies V^(-1/2), and together they give

    dW_γ/dlog a = -19/30 -61/90 +2 =31/45,
    ρ_γ =31 H⁴/(180Ω4).

There is no photon harmonic one-form or U1 flux sector on S4. These facts do
not settle QCD topology.

The declared quadratic photon EFT is
Δ1[1+e²(κ0+c_R H²+c_λΔ1)]. Its dimension-six trace produces

    δρ_(γ,6)= -e² H⁶/(4Ω4)[(19/30)c_R+(5/63)c_λ],
    c_λ=-∫ds ρ_J(s)/s².

The flat current moment can be supplied independently from pure-QCD spectral
or lattice data; none was fitted here. c_R requires curved TJJ matching and
is not fixed by flat spectroscopy. Pure-gravity H⁶ matching and field-redefinition
Jacobians must be added for the full coefficient. The minimal spectral-lift
benchmark c_R=0 for one free massive unit-charge Dirac field gives the
specified photon-trace response e²H⁶/(8064π⁴m²); it is not the full curved-QED
answer or a QCD prediction.

For an order-e² H insertion, the nonlocal regulated polarization trace must
grow as H^-3: a flat-like form factor would require F(k²)~C/(k²)^(3/2), so
K(k)~C/|k|. That is incompatible with the analytic gapped flat current
representation. A global low-sphere-mode kernel can instead vanish pointwise
in flat space while its low eigenvalues grow as Λ³/H. The explicit three-mode
example has Σ_(l=1)^3 d_l/[(l+1)(l+2)]=259/30 and gives
δρ_1=259γΛ³H/(80Ω4). It obeys transverse Ward identities and has a positive
quadratic kernel, but violates uniform clustering; no local reflection-positive
QCD realization is claimed. At fixed nonzero e its exact Gaussian determinant
resums to H⁴logH, so the e² derivative and H→0 do not commute. A genuine new
alpha-dependent A_ρ needs both an IR mechanism and uniform fixed-charge control.

`PRECONTRACT.json` preceded execution. `run_002/manifest.json` is a completed,
validated bounded v2 record: exact rational identities, eight finite heat sums
(l=1..300, four t values, 60/80 digits), a Dirac spectral-moment benchmark and
an exact finite soft-mode sum. `run_001` is preserved as launch-failed due to
the macOS pre-exec memory limit; the successful retry retained wall/CPU/output
and thread bounds without that memory cap. The numerical checks are not
interval certified and do not establish physical QCD matching.

Exact primary-version source receipts and the division between authentication,
extraction and application are in `SOURCES.json`. The derivation has had a
self-audit and a mathematical proofreading pass, not an independent review.
The next physical calculation is the same-regulator soft TJJ/current kernel
on the closed sphere, including contacts and matching, with uniform low-mode,
global-sector and differentiated-radius control. That missing arrow remains
open.
