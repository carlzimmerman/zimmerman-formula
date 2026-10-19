# All photon masses reconstruct the hard constant only with UV matching

FSP-010 from FSP-009. The physical proton M_u, unconditioned curved QCD
coefficient A, R and alpha remain open. This package supplies a conditional
all-scale reconstruction theorem and a complete elementary Dirac control,
with a calculated heavy-photon matching endpoint. It does not substitute
that control for proton QCD.

For `h_n=(-1)^n s^(n-1) f^(n)/(n-1)!`, exact integration gives

    f(0)=integral_0^L h_n(s)ds
         +sum_(k=0)^(n-1) (-L)^k f^(k)(L)/k!.

The current-convolution kernel integrates to `[L/(t+L)]^n` at every t.
Thus actual data over all photon masses can recover a hard constant that
the former small-s filters discarded. The price is the UV endpoint and
all intermediate scales. For the explicitly stated single-log class,

    f(s)=-a log(s/S0)+B+o(1),
    f(0)=B+a H_(n-1)+integral_0^infinity
                         [h_n(s)-a/(s+S0)]ds.

The derivative remainder and convergence hypotheses are in DERIVATION.md.
QCD running requires a fully matched RG-improved endpoint or subtraction;
this simple single logarithm is not assumed for full QCD.

In the unit-charge Dirac control with fixed MSbar mass and mu=M=1,

    a=3/(16 pi^2), B=5/(32 pi^2), f(0)=1/(4 pi^2).

The finite B is the heavy-photon threshold calculated directly from the
massive-photon denominator, distinct from the inherited PV conversion.
It is fixed by the canonical theory and scheme, not a new arbitrary
coupling. Pointwise heavy-photon decoupling at nonzero separation cannot
remove the renormalized coincident-current contact. Retuning masses to
absorb it defines another matching path.

| Control, no physical calibration | Value |
|---|---:|
| a | 0.01899772193293833 |
| finite heavy-photon B | 0.01583143494411528 |
| all-scale subtracted integral, n=1 | 0.009498860966469166 |
| all-scale subtracted integral, n=3 | -0.01899772193293833 |
| reconstructed f(0), both orders | 0.02533029591058444 |
| error from omitting B | -0.01583143494411528 |
| error from omitting n=3 harmonic term | -0.02849658289940750 |

The exact finite endpoint reconstruction agrees at L=1,100,10^4,10^8,
using the independent radial and Feynman-parameter representations over
all photon momenta. At L=10^8, replacing the finite endpoint by its
asymptotic limit leaves errors 4.31e-9 for n=1 and 1.27e-8 for n=3;
these tails are retained, not declared zero. The infinite subtracted
integrals are also checked by an analytic all-s parameter integral and
an independent smooth rational density-difference integral.

`run_001/manifest.json` is a validated completed v2 record, runtime
3.702786 s, 81 checks, at 40 and 60 decimal digits. Maximum checked
discrepancy is about 4.31e-42 against a declared 1e-28 tolerance. This is
quadrature/precision evidence, not certified interval arithmetic. The
actual command, limits and exact inputs are in REPRODUCE.md,
COMPUTATION_CONTRACT.json and PREEXECUTION_HASHES.json. No RLIMIT_AS was
requested. No alpha, physical mass, sigma term, strong parameter or
cosmological datum was used; M=1 is a dimensionless unit choice.

For QCD, the leading quark-mass matching sector contains the physical
state data `sum Q_q^2 sigma_q/M`, and the full endpoint also needs gluon
operators and strong/running matching. The checked corrected primary
source, [Gasser et al.,1506.06747v3](https://arxiv.org/html/1506.06747v3),
equations (56)-(57),(64), supplies that operator obligation, not its
numerical evaluation. Its dispersive Reggeon-dominance assumption is not
promoted to a proved QCD theorem. Exact version, PDF hash, extraction and
source admission are in SOURCE_ADMISSION.json; the public PDF is retained
in the authorized ignored cache.

The trace equation constrains one matrix-element combination. The formal
variation `delta sigma_u=d, delta sigma_d=-d` preserves its light-scalar
sum while changing the leading charge-weighted logarithm coefficient by
`d/(16 pi^2 M)`. This is an explicit missing state equation, not a new
physical parameter freedom. The exact proton conditioned-minus-vacuum
Feynman-Hellmann insertion similarly does not reduce to the vacuum one.
The coordinate and compact hard-band companion independently explain
the contact and intermediate-scale obligations.

The route remains open for a matched complete canonical proton h_n(s)
dataset or full current tensor, plus a high-photon-mass scalar/gluon
endpoint and controlled OPE remainder. Endpoint-only or soft-only data
do not determine the full number. Self-review is recorded; independent
fresh source-first review remains coordinator-owned. No theorem ruling
out a further dynamical QCD relation is claimed.
