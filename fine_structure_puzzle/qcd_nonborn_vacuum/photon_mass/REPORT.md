# Canonical massive-photon infrared diagnostic

The new filter calculation completed and validated. It extracts a controlled
infrared coefficient of a specified current-convolution observable; it does
not compute the full physical proton mass response, R(alpha), or alpha.

For `u=e^2`, `s=lambda_gamma^2`, and the complete Born-subtracted canonical
order-u mass response `f(s)=M_u^NB(s)/M`, the independent tensor and local
polarizability derivations give

    C_NB=3[(alpha_E-beta_M)/u]/(32pi M),
    [s^2 log(s)] f(s)=-2 C_NB,
    lim_(s->0) [-s f'''(s)/4]=C_NB.

The limit holds at fixed positive QCD pion mass, in infinite volume and a
fixed mass-independent UV scheme, with only the photon propagator varied.
`DERIVATION.md` gives a quantitative soft O(s log s) remainder bound and hard
O(s) tail bound under explicit local-density/OPE hypotheses. For an exact
local polarizability interaction cut off at `Q^2<T`, the finite-s response is
known exactly: the filter equals `C_NB[T/(T+s)]^3`.

The scalar coordinate kernel was verified:

    partial_s^3 D_s(r)=-r^2 K2(sqrt(s)r)/(32pi^2 s).

All Born/current Ward contacts remain required. The kernel is not a means to
replace the full correlator by one temporal moment.
The separate post-run `COORDINATE_MOMENT.md` derives the equivalent full-trace
four-dimensional second moment, with an explicit dominated-limit bound and
contact/tail hypotheses. No full-QCD moment dataset is evaluated here.

## Charged full-mass version

At order u, the complete on-shell Born kernel has no term linear in Q.
Its `Q^3` coefficient is fixed by charge and the pure-QCD anomalous moment,
`d=2+6kappa+3kappa^2/2`. Thus its massive-photon log coefficient is
`c_log,B=-d/(64pi^2 M^4)`. The operator

    P5(D)=D(D-1/2)(D-1)(D-3/2)(D-2),  D=s partial_s,

removes all lower analytic and half-integer terms, yielding

    C_NB=-d/(128pi^2 M^4)
         -(1/3)lim_(s->0) P5(D)f_full(s)/s^2.

This avoids importing an all-Q elastic form-factor curve, while retaining an
independent kappa input and the complete matching/path requirements. It does
not recover f_full(0): every function `f_full(s)+a` has identical filters for
arbitrary a. The hard constant remains a distinct physical calculation.

## Actual no-fit calculations

The full finite-momentum HB pi-N amplitudes from the frozen proton package
were integrated against the analytic propagator derivatives, with
`0<Q<m_pi/2`. There is no numerical differentiation or fit of a mass curve.
The exact known strict-HB soft coefficient provides an independent benchmark.

| lambda/m_pi | G3 / C_HB | -P5 f_NB / (3 s^2 C_HB) |
|---:|---:|---:|
| 0.1 | 0.8846311301 | 0.4904565129 |
| 0.05 | 0.9685806043 | 0.8504168017 |
| 0.02 | 0.9946846862 | 0.9741410668 |
| 0.01 | 0.9986280530 | 0.9933017840 |
| 0.005 | 0.9996467374 | 0.9982729473 |
| 0.002 | 0.9999413325 | 0.9997128942 |

At the last control, G3's exact local finite-ball factor is 0.9999520015;
the additional full-function shape correction is -0.00001066903.
For P5 the corresponding exact local factor is 0.9997600179 and the shape
correction is -0.00004712370. This explicitly separates the known cutoff
effect from the computed nonlocal HB response. It is not an error bound for
the complete physical QCD tensor or the chiral truncation.

The printed AHLP parameter benchmark gives
`C_HB=0.05132564746 GeV^-4`; the last G3 is
`0.05132263631 GeV^-4`. These numerical units use `M=0.93827`,
`m_pi=0.13957`, `f_pi=0.09221` GeV and `g_A=1.27`, with no alpha input.
They are calibrated source inputs. In particular the printed pion mass is
the charged-pion benchmark; no independent pure-QCD fixed-MSbar matching is
claimed.

An all-momentum elementary Dirac calculation independently tests the charged
Born removal. The radial Born convolution and a separately derived on-shell
Feynman-parameter integral agree at all six declared photon masses, with
absolute differences below 5e-60 in 60-digit arithmetic. The predicted
logarithm is `c_log,B=-1/(32pi^2 M^4)`. At `lambda/M=0.002` the finite-s P5
value is 0.9955941096 times its exact limiting value. Its residual apparent
non-Born coefficient is retained rather than declared zero at finite s.

## QED_M literature and data admission

Massive-photon extrapolation and its universal linear photon-mass term are
established by [Endres et al.,1507.08916v3](https://arxiv.org/abs/1507.08916v3).
The order of limits and zero-mode difficulties are explicit in
[Clark et al.,2201.03251v1](https://arxiv.org/abs/2201.03251v1). This package
translates that framework into an infrared polarizability filter and makes
no novelty claim.

Endres footnote 42 names a regulator EFT operator `m_gamma^2 A^2 N^dagger N`
at N3LO. A hypothetical order-u term of this form can generate an s^2 log s
tadpole and survive these filters. The footnote does not establish its
u-order or matching coefficient in the canonical microscopic theory. We do
not claim demonstrated contamination or a new free coupling in that theory.
Any NR/EOM representation must reproduce the fixed pure-QCD current tensor.
Importing a generic fitted source curve requires the common canonical path
and any regulator-specific operator matching to be checked explicitly.

The newly inspected QED_M archives do not provide a compatible correlated
individual-proton mass grid for this high-order extraction. Endres uses an
electroquenched SU(3) ensemble with a pion mass about 807 MeV and publishes
mass-splitting/extrapolation outputs; Clark's electroquenched 310 MeV study
demonstrates pion/kaon mass curves and zero-mode corrections. Neither is
silently converted into the missing full physical proton coefficient.
Finite-volume limits, missing sea terms, calibration and noise amplification
remain data-admission constraints. A separate six-mass exact annihilator is
documented in `SIX_MASS_STENCIL.md`, without an execution claim here.

## Provenance and status

`run_001/manifest.json` is a validated completed v2 record: 36 checks passed,
runtime 7.985346 seconds. Caps were 300-second wall time, 280 CPU seconds,
1 MiB output and one numerical thread; no RLIMIT_AS was requested on macOS.
Exact operator/local-cutoff identities, Bessel derivatives, both numerical
integral representations and nested HB quadratures were checked. The largest
last quadrature changes were about 2.4e-14 for P5 and 1.3e-22 for G3; these
are convergence diagnostics, not rigorous numerical error certificates.

The runner observed HEAD `0260149521dd8f672e89397d255974c9e7b7cd8d`, dirty.
No Git mutation was performed by this worker. The previously declared
ancestry remains FSP-008; actual per-file before/after hashes pin execution.
Commands, sources and hashes are durable beside this report. Fresh review is
owned by the coordinator and is not presumed by a completed manifest.

The canonical filter theorem and its two controlled benchmark calculations
are the strongest scoped result. The complete physical polarizability
difference, a usable matched full-QCD mass/correlator dataset, the hard mass
constant and the independent curved-vacuum coefficient remain unresolved.
