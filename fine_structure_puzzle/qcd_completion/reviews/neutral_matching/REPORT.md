# Independent audit of the closed neutral and screened matching calculations

## Claim and primary verdict

**Primary verdict: conditional on a named input.** At fixed positive matched
local coefficients, the stated canonical compact sine-Gordon EFT on closed
S3_R has zero 1/R coefficient in its tree-plus-Gaussian spatial response.
The displayed formula is correct. Applying that result, or a charged
monopole exterior coefficient, to the physical QCD vacuum remains conditional
on common-regulator gauge-to-dual matching, including the normalization and
metric response of the Wilson coefficients and the overall gauge partition.

The closed determinant, neutral Green-kernel cancellation, hypothetical
matching sensitivities, charged exterior solution, and leading conditional
cloud algebra pass the mathematical checks below. No error requiring a change
to these formulas was found. There is one actionable normalization issue when
the two separately declared EFTs are used together: their printed coupling
symbols do not yet furnish a common Abelian charge/kinetic dictionary.

## Independent reconstruction and provenance

`INDEPENDENT_RAW.md` was saved before any target report, derivation, script,
run result, or source record was read. It derives the massive S3 determinant,
its actual volume derivative, compact massless-reference correction,
mean-zero S3 Green kernel and neutral cancellation, and the exact screened
Dirichlet exterior. It also derives the response to hypothetical 1/R matching
shifts. No new scientific computation was needed; these conclusions are
analytic. The existing scripts were inspected and their manifests validated,
but their mathematical runs were not re-executed or overwritten.

The coordinator subsequently raised an Abelian normalization comparison,
which prompted the separate invariant derivation below. That comparison is
therefore an independent analytic check of a named concern, not a blind
discovery. The coordinator also queried the R denominator in the raw
unsubtracted stress; direct differentiation and the flat limit confirmed the
raw formula. No correction to that formula was needed.

`REVIEW_PROVENANCE.json` pins the exact artifacts and source bytes read. The
review directory is the only location modified by this review. No ledger
update or source-determinant rederivation is claimed.

## Dependency graph and obligations

| Arrow | Verdict | Decisive check |
|---|---|---|
| Four signed events -> -4f cos(theta/2) cos(phi) | passed | Direct event expansion, with f per signed event |
| Compact constant integration -> magnetic neutrality and integer total topology | passed | q=0 forces equal species net counts; the Bessel identity follows |
| Canonical compact measure -> one Gaussian constant eigenvalue | passed | a0=sqrt(kappa V) phi0; J0 I0(uV)~p(mu/m)exp(uV) |
| Canonical all-mode determinant -> D11, D15, D16 | passed | Independent spectral derivation and metric derivative |
| Normalized neutral gas -> canonical EFT divided by compact massless reference | passed within the declared scalar convention | W0=-(1/2)log(kappa R)+constant |
| Same-regulator Green self plus pair energy -> neutral 1/R cancellation | passed | Constant term multiplies (sum q)^2, not sum q^2 |
| Hypothetical f1,kappa1 -> D18-D19 | passed | Chain rule of -u-(u/kappa)^(3/2)/(12pi), then volume derivative |
| Screened exterior M6 -> M7-M8 | passed | Radial Yukawa equation and boundary action |
| BPS overlap plus unit Yukawa scalar charge -> M9 | correct only after stated restriction | Requires small m/v, maintained overlap, subleading core potential/higher operators |
| DGPS exact-v2 result -> M1 | externally proved in the needed asymptotic form, after translation | Read equations 54-56, 70, 74, 84 directly; did not rebuild their Green function |
| Classical adjoint-Higgs small-beta source -> leading M9 benchmark | verified after translation | Source equations 1,4-7,38-40; potential differs from double trace |
| Both lanes' g symbols -> one common gauge theory | incomplete | Flux/kinetic invariant below must be reconciled together with core action |
| Retained canonical EFT -> complete small-circle gauge metric response | conditional | Common curved core matching and gauge/global normalization absent |
| Small-circle pure SU2 product geometry -> physical full-QCD de Sitter stress | not addressed | Quarks, strong-coupling continuation, state/geometry and gravitational subtraction absent |

## 1. Closed Gaussian response and compact normalization

For P=-Delta+m^2 on S3_R, n>=1 has eigenvalue (n^2+a^2)/R^2,
degeneracy n^2, and a^2=m^2R^2-1. Including the constant mode,

    W_m=-pi a^3/6+pi integral_a^infinity t^2/(exp(2pi t)-1)dt,
    partial_R W_m=-pi m^2 R a coth(pi a)/2.

Because partial_R V=6pi^2 R^2, the unsubtracted response is

    tau_s,m=-m^2 a coth(pi a)/(12pi L R).

Its flat limit is -m^3/(12pi L), fixing both the R power and dimensions.
Subtracting that flat action gives exactly D15, including
Delta tau_s=m/(24pi L R^2)+1/(96pi L m R^4)+... . The quotient
Delta W/(LV) instead begins m/(8pi L R^2). The factor of three is real;
the report correctly distinguishes the two observables. D16 also follows
by differentiating m^2 at fixed R. The retained tree term -uV is included
and subtracts itself when u has no R dependence.

There is no omitted canonical constant-mode 1/V contribution. The
Jacobian J0=p mu sqrt(2pi kappa V) cancels the +1/(2V) term from Haar
I0(uV) at Gaussian order. The exact isolated uniform-sector remainder
does not become a complete interacting two-loop answer; the report says so.

There is also no omitted massless reference in the current report. The
normalized gas differs from the canonical massive EFT by -W0, with
partial_V W0=-1/(6V). Its response therefore differs by +1/(6LV), of
order R^-3. The current text explicitly includes that distinction.
The remaining gauge-to-dual global normalization is still an input, rather
than something fixed by the scalar Jacobian. The zeta/proper-time finite
part fixes a determinant convention; it does not evaluate the hard
cosmological/curvature matching coefficients.

For the hypothetical path f=f0+f1/R and kappa=kappa0+kappa1/R, at a
fixed stable theta branch set u_i=4|cos(theta/2)| f_i. Directly,

    C1= -[1+m0/(8pi kappa0)]u1 + m0^3 kappa1/(8pi kappa0),
    Delta tau_s=2C1/(3LR),
    Delta tau_L=(partial_L C1)/R.

Thus D18-D19 include both the loop response to the mass shift and the
essential 2/3 spatial variation factor. A test of f1 alone would miss
the kappa1 ambiguity. These formulas are sensitivities to uncomputed
inputs, not evidence that such nonlocal matching terms exist.

## 2. Neutral kernel versus charged exterior

The exact mean-zero kernel and its regular coincidence value agree with
the raw derivation:

    G_R=[(pi-chi)cot(chi)-1/2]/(4pi^2R),
    G_R(r)-1/(4pi r)=-3/(8pi^2R)-r/(12pi R^2)+... .

Keeping self and pair terms in one prescription gives
-3(sum q)^2/(16pi^2 kappa R). It is identically zero on every neutral
finite configuration. Removing only the regular self energy would require
a compensating R-dependent fugacity; otherwise it changes the ensemble.
This fixed-separation identity does not justify exchanging a growing
thermodynamic sum with the expansion. The current report correctly limits
the claim and uses the Gaussian calculation as a separate leading screening
resummation.

For M6 the on-shell exterior is exactly

    S_ext=2pi kappa[1/rc-1/R+rc psi_c^2
                   +m rc^2 psi_c^2 coth(m(R-rc))].

It leaves a magnetic -2pi kappa/R action tail at fixed m>0 and large mR.
That result concerns a charged insertion with fixed core/wall data, not the
neutral closed functional. Sending m to zero first can cancel the 1/R
term for BPS core data, so the order-of-limits qualification is necessary.
The M9 leading +2pi kappa m cloud action follows from the stated overlap
matching; its sign agrees with monotonic classical monopole mass growth.

## 3. Actionable cross-lane coupling normalization

Use distinct names kappa_d for the dual scalar and K_B for the exterior
Maxwell coefficient. For

    S_B=(K_B/2) integral B^2,       monopole flux Q_B,

the pair Coulomb action is K_B Q_B^2/(4pi r). A compact scalar with
kinetic kappa_d (grad phi)^2/2 and unit vertices exp(+/-i phi) gives
1/(4pi kappa_d r). Therefore the convention-independent matching condition is

    K_B Q_B^2=1/kappa_d.

M6 sets K_B=L/g_h^2 and Q_B=4pi. It thus requires
kappa_d=g_h^2/(16pi^2L). The closed lane instead retains the UY printed
kappa_d=g_UY^2/(8pi^2L). Equating the two g symbols leaves a factor two
in the pair force. Equality of this Abelian invariant alone would require
g_UY^2=g_h^2/2, or an equivalent explicit rescaling of the flux, charge,
trace, and field normalization.

This is **not** a concluded source error. UY footnote 13 changes the
generator normalization, and its equations 3.9,3.17 and3.25 are mutually
consistent at the root-plasma level: alpha^2=2, flux vector 2pi alpha/g,
pair coefficient 2pi L/g^2, and the reduced scalar kinetic term above.
But the source also states an action 4pi^2/g_UY^2 per center SU2 monopole;
the exterior's BPS core with v=pi/L has action 4pi^2/g_h^2. Merely replacing
g_UY^2 by g_h^2/2 in the force formula does not also reconcile those action
formulas. A full trace/action/holonomy dictionary is required before numerical
cloud, fugacity and neutral-EFT coefficients are combined. Until then, the
separately declared models and their structural conclusions remain valid.

Cheapest next check: write the same SU2 matrix connection in one fixed
trace convention, reduce its magnetic and A4 kinetic terms, evaluate its
unit magnetic flux and BPS surface term, and dualize with a unit compact
vertex. All four quantities must satisfy the invariant above in one
coupling convention. This can be done before a costly core determinant.

## 4. Exact-source checks

DGPS `hep-th/0404042v2` is identified by its PDF stamp, title/authors and
the same PDF/text hashes as the project source record. Direct extraction
confirms that equations 54-55 imply

    c=74/(9pi)+8 gamma_E/(3pi)-23pi/54,
    log(w/w0)=[4 log(4nu(1-nu)D^2)/(3pi)+c]/D+O(D^-2).

Equation 74's Jacobian cancels the inverse core masses when combined with
minus the determinant correction. The analytic c agrees with the displayed
current-integral constants and with differentiating equation 55 to54.
The decimal 1.946 printed next to84 disagrees with its analytic expression;
the report's retained 1.76908473346655857... is the analytic value. This is
an exact formula/translation check, not an independent rederivation of the
source vacuum current. Equation 46 is explicitly numerical in the source,
with the stated finite check range, while54-55 are obtained by the separate
large-separation current integrals. The report preserves this qualification.
Equation70 explicitly excludes a Coulomb-tailed single BPS dyon from the
simple vector/ghost determinant replacement. No finite-wall determinant
can be inferred from it. D is an internal separation, not a cosmological
radius. Removing the common constant-holonomy volume term leaves the
separation correction intact, as stated.

Forgacs-Obadia-Reuillon `hep-th/0412057v2` likewise has the specified stamp
and matching hashes. Equations1,4-7 give M0=4pi v_F/e, M_W=e v_F and
beta=M_H/M_W. Section5 equation40 contains the leading +beta/2 term.
For q=e Phi, v=e v_F, m=M_H and K_B=L/e^2,
L M0 beta/2=2pi K_B m. This verifies the benchmark normalization and sign.
Its polynomial Higgs potential and classical infinite-space domain do not
prove a deformed-Yang-Mills determinant or a curved vacuum stress. I did
not independently check the publisher's-note PDF; the audited result uses
only the main source's leading analytic coefficient, not the affected table.

## 5. Computation and evidence audit

The four existing manifests `closed-002`, `green-003`, `matching-002` and
`screened-001` each validate against their current project inputs with
`run.status=completed`. This verifies recorded hashes and execution status,
not the physical interpretation. The scripts implement their stated finite
assertions. `closed-002` uses independently represented heat traces,
winding terms and a convergent mass Hessian with explicit tails; metric
derivatives and matching sensitivities agree with the independent analytic
derivation. `green-003` verifies the differential equation, series and
finite neutral charge identities. The matching scripts verify translated
symbolic expressions and finite quadratures, not a newly solved caloron
or non-Abelian determinant. Numerical arithmetic is not interval certified.

No rerun was necessary to establish the analytic conclusions here. Existing
executed code, contracts, inputs and output bytes were preserved. Validation
commands and observed results are recorded in the provenance receipt.

## Remaining physical gap and strongest safe conclusion

The next load-bearing missing object is the **un-normalized neutral gauge
generating functional on the chosen curved geometry**, matched in one
regulator and coupling convention. Its first unknown contribution is the
R^2 coefficient of W_total, equivalently the complete 1/R coefficient of
the bulk-subtracted spatial response. One must jointly compute or exclude
the f1 and kappa1 shifts and the overall hard/global C1 contribution;
neither a charged self energy nor a normalized theta derivative determines
their sum. Canonical Jacobians and the massless reference do not hide a
1/R term, while local analytic curvature counterterms start at R^-2 in
this closed geometry.

At the retained order and fixed local coefficients, the neutral closed
ensemble supplies a controlled zero. The screened charged insertion
supplies a distinct nonzero exterior action tail. The DGPS internal
separation correction and the classical cloud benchmark do not bridge
those two observables. No physical full-QCD de Sitter stress coefficient,
electromagnetic-alpha dependence, proton matching, or physical alpha has
been computed. No parameter fit to alpha enters the reviewed work.
