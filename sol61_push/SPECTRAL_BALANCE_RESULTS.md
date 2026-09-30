# Finite spectral energy and a cubic response

Original goal OPEN. This is a homogeneous spectral witness and a scoped obstruction, not a covariant gravity theory or a prediction of 32pi. Base and bounds: [contract](SPECTRAL_BALANCE_CONTRACT.md). All formulas below use c=hbar=1.

## Exact construction

Let eta be +1 for effective occupied fermion energy weights and -1 for effective boson weights. The actual zero-point energy contribution has sign -eta. We absorb physical multiplicity and any zero-point factor into the effective weights; no particle multiplet is supplied. Define m_n(P)=sqrt(n²M²+y²P²), with mu,M,y>0 and P=|p|. For the declared dispersion sqrt(k³/mu+m_n²), substituting t=k^(3/2)/sqrt(mu) gives k²dk=(2mu/3)t dt. The jointly regulated energy is

rho_K(P) = -mu/(9pi²) sum eta [(K²+m_n²)^(3/2)-m_n³].

Equal counts and sum eta n²=0 cancel its K³ and K divergences for every P. The finite spectral energy, in this common-cutoff prescription with no additional bare constant, is

rho(P) = mu/(9pi²) sum eta m_n(P)³.

The following effective masses are a witness:

- Fermions: M times (0,2,2,3,6).
- Bosons: M times (1,1,1,5,5).

Counts, first moments and second moments agree: 5,13,53. Their cubic moments differ by 6; there is one excess massless fermion weight. Consequently

rho(P) = mu/(9pi²) [6M³+y³P³-57y⁴P⁴/(80M)+O(P⁶)].

Thus rho(0)=2mu M³/(3pi²)>0; the quadratic loop susceptibility vanishes, and the cubic response is positive. This corrects the overly strong inference that cancelling the vacuum divergences must always cancel a MOND-type cubic response. It does cancel it for pairwise identical spectra, but unequal moment-balanced spectra escape that argument. The witness's moment relations are chosen; no symmetry has derived them. The exhaustive integer search found no witness of lengths 2–4 with masses 0–8, but that is not a universal minimality theorem.

## Pressure check and its limit

For a fixed homogeneous P and fixed mu,M,y, use the mode-scaling pressure p_K=-sum eta integral d³k/(2pi)³ [k E'(k)/3]. Integration by parts gives

rho_K+p_K = -mu K²/(6pi²) sum eta sqrt(K²+m_n²).

The matched zeroth and second moments make the right side O(K^-1). Hence p=-rho in the selected rest frame as K tends to infinity. The equality is an exact integration identity for this dispersion and prescription. It does not supply the metric/aether variations of a covariant completion, its boost properties, conservation equations, or stability. Calling rho(0) the physical cosmological constant remains conditional on that missing completion and on the absence or selection of an allowed bare vacuum term.

## Response dictionary and the coefficient that remains free

Use the existing polarization functional W=g²/2-g·p+V(P), with V=P²/2+4pi G rho(P). Its assumed tree matching makes the quadratic terms a complete square. The loop calculation neither enforces nor protects that matching. At small P,

alpha=4Gmu y³/(9pi), a0=1/(3alpha)=3pi/(4Gmu y³).

If the spectral constant is identified with covariant vacuum energy, Lambda=8pi G rho(0)=16Gmu M³/(3pi). Therefore

Lambda/a0² = 256h³/(27pi³), h=Gmu M y².

The target would require h=(3/2)pi^(4/3). No equation here selects h. It would be a fit or an added relation. Equal mass ratios and a common scale are insufficient to predict the dimensionless coupling. An additional independent bare constant makes the freedom larger.

## A decisive high-field obstruction

The fourth moment difference is 156. At large x=yP/M, the dimensionless spectral function f(x)=sum eta(n²+x²)^(3/2) satisfies f(x)=117/(2x)+O(x^-3). It tends to zero, despite starting at f(0)=6 and initially increasing as x³. Its derivative must become negative somewhere. Direct evaluation confirms f'(10)<0.

For the declared functional the induction is b=g-P=4pi G rho'(P). Negative rho' gives negative radial baryonic induction for positive aligned polarization, so this functional fails as an all-field galaxy law. Extra high-field operators or a different spectral completion are necessary. This is an obstruction to this particular completion, not a refutation of all moment-balanced theories. The low-field cubic survives the obstruction.

Exact pairing provides a second scoped obstruction: if a symmetry pairs every nonzero boson/fermion mass with the same coupling and multiplicity, their contributions cancel at every P. Equal total counts then also pair the zero-mode weights, eliminating the surviving cubic. A useful protecting mechanism must permit unequal spectra; invoking unbroken pairwise supersymmetry alone cannot justify this witness.

## Verification and self-review

The corrected run passes 36/36 checks: exact moments and series, bounded exhaustive search, nine independent energy quadratures, nine pressure identities, high-field sign, and coefficient freedom. Both evidence manifests validate with input/output hashes. Numerical comparisons use absolute tolerance 1e-7 and the predeclared fields and cutoffs. Exact identities, not numerical searches, establish the displayed coefficient dictionary and limiting obstruction.

The original run failed 9 pressure checks because its boundary denominator was 9pi² rather than 6pi². The three diagnostic ratios at P=0 were 1.5. Re-derivation in physical momentum and the t variable identifies the missing factor; only that line was changed in a fresh script and run. The original input and failed output are retained. No numerical tolerance changed.

Self-review verdict: correct only under the stated spectral, regulator and static-response assumptions. No independent reviewer was used. Source comparison is recorded in [literature check](SPECTRAL_BALANCE_LITERATURE.md); the relativistic source's stress theorem does not transfer to the fractional dispersion. Proofreading covered these new files and the checkpoint addition; no mathematical typo corrections beyond the separately documented pressure repair.

Remaining dependencies: a real action and particle content, protection of both spectral moments and gravitational critical matching, a healthy high-field completion, and selection of h plus any bare vacuum term. These are prerequisites for the original goal, not optional refinements.
