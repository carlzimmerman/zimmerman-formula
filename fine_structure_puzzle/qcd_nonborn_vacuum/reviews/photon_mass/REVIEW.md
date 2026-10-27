# FSP-009 canonical photon-mass filter: independent bounded review

## Primary verdict

**Conditional on named inputs.** The exact filter algebra, normalizations,
Born infrared coefficients, source-to-method classification and declared finite
benchmark interpretation pass. No material discrepancy was found. Applying
the extraction to physical data remains conditional on admission of the same
canonical fixed-QCD current tensor, complete covariant Born/current contacts,
fixed parameter/matching path, positive QCD gap, and the stated local-density
and absolute tail/moment bounds. Transfer to a generic QED_M mass curve also
requires the regulator-specific operator matching discussed below. None of
these physical numerical inputs is supplied by the bounded algebra run.

This verdict does not mean a displayed algebraic gap was found in the
conditional theorem: under its explicitly stated density/tail hypotheses the
G3 limit and bounds are established. A physical full-QCD dataset satisfying
those hypotheses with useful quantitative errors is the remaining input.
The full physical M_u(0), A_rho, R and alpha remain open.

## Target and independence

Audited frozen author target: photon_mass/DERIVATION.md, INPUTS.json,
COMPUTATION_CONTRACT.json, check_filters.py, run_001 and final REPORT.md,
plus separately identified post-run SIX_MASS_STENCIL.md and
COORDINATE_MOMENT.md. The final report hash is
32745c5d858299dc653a4bf7eb18750f12b7ced6dc88fbb38254dc885c026a5a.
Author manifest hash:
aec42bdd0dbc86292149fcc73da5f6f26c10146a0b82d2a0773fb8cc066adaf9.
Author full ARTIFACT_HASHES.json hash:
4610437381d60b64020c99a9341674306008efbabd500377ec28ef1bbdd83828.

The independent mathematics was derived from the already preserved clean
polarizability action and the old parent Born kernel before reading the new
photon_mass author packet. Its pretarget and new exact implementation were
pinned before author inspection. Unlike the prior common review, this new
implementation was also written before opening the new author code/results.
It uses standard-library exact polynomials and rational arithmetic, not the
author's SymPy/mpmath implementation or coefficient data.

Provenance limitation is explicit: the first PRETARGET persistence command
failed when triple-quoted Python text collided with derivative notation. The
parent then disclosed Endres footnote 42 before the successful durable pin.
The projector/Born/Bessel math had already been derived, but the contact issue
is not claimed blind and the pin is not backdated. PRETARGET.md records this.
The old Born-file read displayed sections beyond the requested §§1-3; no new
photon-mass projector was there. All 17 prior common_clean files remain intact.

The root's coordinate-moment candidate arrived after the first new exact run.
Its audit is separately saved as COORDINATE_COMPANION.md with a second run;
no earlier notes/code/contracts were amended to make it appear pretarget.

## Claim card and dependency graph

Objects: s=lambda_gamma^2>0, u=e^2, fixed pure-QCD mass M and renormalized
parameters, complete first-u current convolution with only D_s(Q)=1/(Q^2+s)
varied. Let a=alpha_E/u and b=beta_M/u. Born subtraction includes the regular
non-pole elastic Dirac term and matched form factors.

1. The local spin-averaged polarizability action and complete SO(4) trace
   give the NB radial density g(t)=2Ct+O(t^2), C=3(a-b)/(32*pi*M).
2. This density plus explicit soft bound |g-2Ct|<=B t^2 and absolute OPE tail
   control gives the NB massive-photon logarithm and G3 filter with a bound.
3. The complete Born kernel B(z)=1+c z^2+d z^3+O(z^4), with no z term,
   determines the lower half powers and same-order logarithm.
4. Euler/stencil annihilation removes lower analytic and Born half powers;
   subtracting the remaining d logarithm requires the independent kappa.
5. Canonical microscopic matching is needed before using an arbitrary
   massive-photon EFT curve in place of that current convolution.
6. The coordinate moment additionally requires its distributional contacts,
   second-moment/tail admission and complete elastic-state subtraction.
7. No operation above determines the additive hard f(0).

## Decisive independent calculation

For NB f(s)=M_u^NB(s)/M,

 f(s)=A0+A1*s+A2*s^2+gamma_NB*s^2 log(s/mu^2)+higher,
 gamma_NB=-3(a-b)/(16*pi*M)=-2C.

A sharp soft SO(4) ball instead gives C*K^4. Thus the massive-photon
lambda_gamma^4 log(lambda_gamma^2) coefficient is -2 times the sharp-ball K^4
coefficient. Replacing K by lambda_gamma would give a wrong factor/sign.

For the full unit-charge proton,

 f_full(s)=analytic-sqrt(s)/(8*pi*M)
           +c*s^(3/2)/(32*pi*M^3)
           +[gamma_NB-d/(64*pi^2*M^4)]*s^2 log(s)+higher,
 c=-3/2-4*kappa-2*kappa^2-(4/3)M^2*r_E^2,
 d=2+6*kappa+(3/2)kappa^2.

The missing z term in the complete Born kernel forbids an s log(s) term at
this order. Omitting its regular Dirac term would spoil this conclusion.
The source/current endpoint reproduces the known -alpha_em*lambda_gamma/2.
The logarithmic Born correction needs kappa but no form-factor slope. Removing
the lower s^(3/2) term by annihilation avoids assigning r_E^2, while actual
finite-s error control still needs higher form-factor/remainder bounds.

With E=s*d/ds, define P5(E)=E(E-1/2)(E-1)(E-3/2)(E-2). The independent
normalized logarithm projector was Pi_full=(2/(3s^2))*P5. The worker instead
reports L5=lim P5 f/s^2, so L5=(3/2)*gamma_total, and

 C_NB=-d/(128*pi^2*M^4)-L5/3.

These conventions agree exactly. The worker's NB G3=-s*f'''/4 is minus one
half of this review's NB logarithm projector (s/2)*f''', so G3->C as stated.

Important propagator dictionary: t=Q^2, P_s=t/(t+s)=t*D_s. Our independent
Pi_full[D_s]=-5s(3t-s)(t-3s)/(t+s)^6. Multiplying by t and changing from
Pi_full to P5/s^2 gives exactly the worker's
-15ts(3t-s)(t-3s)/[2(t+s)^6]. No factor is missing.

G3 has a positive photon weight (the NB density need not be positive).
The full fifth filter changes sign at t=s/3 and t=3s. The author distinguishes
them correctly. Positivity of individual alternating propagator derivatives
does not make the complete full-Born annihilator positive.

The q=4 six-squared-mass stencil also agrees with the clean derivation:
weights (-1024,1984,-1240,310,-31,1), denominator 322560*log(4)*s0^2.
It annihilates 1,s^(1/2),s,s^(3/2),s^2 and retains the log. Six photon masses
span a factor 32. The exact next s^(5/2) contribution is amplified to
[31/log(4)]*sqrt(s0) times its coefficient; sum of absolute weights is 4590.
This is a data-admission/conditioning fact, not a physical error estimate.
The worker correctly claims no execution of that stencil on QCD mass data.

## Remainders and finite benchmark audit

The worker's positive remainder integral is correct:
int_0^T t^3/(t+s)^4 dt=log(1+T/s)-y-y^2/2-y^3/3, y=T/(T+s).
Together with its explicit B and absolute-tail hypotheses, it proves soft
O(s log s) and hard O(s) errors for G3. Analytic matching mass terms through
s^2 are annihilated. Merely assigning a formal big-O to a mass curve would
not license arbitrary differentiation; the integral-kernel hypotheses supply
the needed stronger route.

The posttarget companion gives a useful additional check: for the normalized
NB fifth estimator -P5 f/(3s^2), its weight relative to G3 is
(5/3)(4y-1)(4y-3). Its absolute value is at most 5 on y in [0,1]. Therefore
the same absolute soft/tail bounds control it, with factor at most five and
its own local cutoff polynomial 16y^5-20y^4+5y^3. This is a sufficient
conditional bound, not an evaluated physical B or tail.

The author HB angular change x=sin(theta), with reflection to the positive
half interval, and radial y=t/(t+sigma), v=log(1+t/sigma), give the stated
integration weights. The normalization C_HB follows independently from the
leading polarizabilities as 9g_A^2/(8192*pi^3*M*F_pi^2*M_pi). Applying those
filters to the inherited complete two-variable HB functions, rather than to a
soft polynomial, is what its code implements.

Declared HB controls lambda/M_pi=0.1,...,0.002 and quadrature orders 24/48
are accurately reported. At the smallest control G3/C_HB=0.9999413325 and
-P5/(3s^2 C_HB)=0.9997128942. The local finite-ball factors and additional
full-function corrections are separated. Agreement between quadrature orders
is a numerical diagnostic, not an interval certificate, QCD truncation bound
or calibrated physical result. The older full-amplitude/source audit is
outside this narrow review and was not repeated here.

The Dirac radial variable and Feynman-parameter derivatives have the correct
independent normalizations. Subtracting the constant and quadratic B_D terms
is permitted because their complete fifth-kernel moments vanish exactly.
Their reported six finite-s comparisons and residual approach to d=2 agree
with the independently derived expansion; the nonzero finite-s apparent NB
residue is retained. No physical proton data can be inferred from this
benchmark.

## Source contact and canonical matching restriction

Directly checked Endres et al., arXiv:1507.08916v3 (11 Aug 2016), Eq. (3) and
footnote [42], plus a source-only subagent's independent primary check. The
paper supplies the known linear mass term and an analytic quadratic term with
a local coefficient. Footnote [42] admits s*A^2*N-dagger N at N3LO without
specifying its coefficient or explicit e-power. This does not establish either
an additional independent first-u ambiguity in the canonical tensor or its
absence in every EFT basis.

A term explicitly defined as u*c_s*s*A^2*N-dagger N/M^3 has a photon tadpole
already at order u, since the free-photon contraction carries no extra u. An
analytic coefficient then produces a nonanalytic s^2 log(s) mass term that
survives both filters. It cannot be dismissed as an analytic mass polynomial.
The source footnote itself does not fix that counting or matching coefficient.

For the specified canonical microscopic deformation, the u=0 matter tensor
is s-independent and all its current/action contacts are fixed; no independent
extra matter-photon interaction may be inserted. A faithful NR/EOM EFT must
match the whole convolution, and may redistribute fixed terms into s*A^2 and
other contacts. Thus no assertion that an individual coefficient vanishes in
every basis is needed. Importing a generic fitted QED_M curve without this
combined matching identity would leave a genuine missing implication. The
frozen worker explicitly avoids that claim and states the distinction.
This is a method translation/formal corollary of known QED_M methods, with no
novelty claim. The earlier source-only notes preserve exact primary links and
version/convention checks.

## Coordinate companion

The separately proposed post-run identity passes with its admission conditions:

 H_trace(Q)=4*pi*[(a-2b)Q^2+2(a+b)Q4^2]+O(Q^4),
 int d4x r^2 H_trace^NB(x)=-48*pi*(a-b),
 C_NB=-int d4x r^2 H_trace^NB(x)/(512*pi^2*M).

H is already normalized by 1/(2M). Both Fourier Laplacian and the constant
term of K2 give the factor 512. The worker's Schwinger bound
|r^2 K2(sqrt(s)r)-2/s|<=r^2/2 follows directly from 1-exp(-v)<=v and proves
its dominated limit for an absolute second moment of the regular part, with
local distributions handled separately. Its NB zero moment cancels 1/s.

Renormalized derivative contacts matter: Delta delta acts on r^2 to give 8.
The vacuum subtraction, state normalization and complete elastic subtraction
cannot be omitted. The moment is the full four-dimensional trace, not the
prior single temporal/spatial-current sea moment. An infinite-volume photon
kernel may change the practical finite-volume problem, but QCD finite-volume,
contact and tail control still remain. Obtaining a fully Born-subtracted
coordinate correlator can require elastic information over its support,
although the local massive-photon Born-log coefficient uses only kappa.

## Limit and calibration obligations

Keep M_pi positive and the soft photon mass much smaller than M_pi. A massive
charged-state extraction needs a specified gauge/dressing/endpoint limit.
For periodic massive-photon simulations take infinite volume before s->0, or
prove suitable uniform control. Fixed-volume zero modes can yield inverse-s
and Gaussian-time artifacts; the annihilators do not remove them. The massless
charged pole/residue limit is not automatic. These conditions do not preclude
a distinct QCD-only infinite-volume-kernel method with separate tail/FV bounds.

Fixed-QCD renormalized parameters and mass-independent matching are essential.
Retuning masses/strong scale for each photon mass can inject the same
nonanalyticity; its full calibration Jacobian/path terms would need checking.
The printed charged-pion AHLP benchmark is not an independently matched
pure-QCD fixed-MSbar mass point. Filters annihilate the additive hard constant
without determining it. No physical M_u(0), A_rho, R or alpha follows.

## Bounded checks, freshness and non-claims

Pre-author independent run_clean_001 uses exact rational sparse polynomials:
full/NB D_s kernels, P_s dictionary, stencil, normalizations, 48 rational Born
series cases, radial beta moment and contact-log survival. It completed in
0.039324458 seconds and its v2 manifest validates against current inputs.
Posttarget run_companion_001 checks the moment factor, Bessel constant,
absolute kernel bound and zero-mode nonannihilation; it completed in
0.040676042 seconds and validates. Both use Python 3.9.6, 20-second wall and
10-second CPU limits, one-thread convention, no RLIMIT_AS. No QCD current
integral or physical remainder was numerically evaluated by these runs.

The author run_001 manifest also validates against current inputs: 36 checks,
7.985346 seconds, declared finite range only. Validation is a provenance check,
not an independent rerun of its numerical HB calculation. Its mathematical
implementation and normalization were inspected as above. The report,
six-mass stencil and coordinate companion are correctly outside that run's
original execution contract.

No Git query was made by this review. Our manifests mark revision unavailable
and dirty=true as an explicitly conservative unmeasured schema marker. Current
scientific targets are pinned by hashes. All 21 final author files are unchanged
since the full freeze; the only recorded early-to-final transition was REPORT
metadata while the parent had explicitly said it was still being written.
All 17 previous common_clean files remain unchanged. No author/old/root file,
source cache or installation was modified. Primary browsing and a read-only source
subagent were used; no author contact or external job occurred.

All before/after records, source notes, contracts, implementations, validated
results and exact hashes are retained in this review directory. The strongest
safe result is the canonical infrared coefficient extraction and the two
conditional representations, not recovery of the unknown hard mass constant.
