# Focused review of the microscopic clock matching

Primary verdict: **proved as written**, for the analytic branchwise matching,
real-frequency kernel bound, gap distinction, and conditional high-frequency
front restriction in `../clock_matching/CLOCK_MATCHING_RESULT.md`, sections
2–5 and the front paragraph of section 6. This verdict does not certify the
finite 1224-spectrum calculation or the numerical group-speed crossing; those
are outside this requested analytic audit.

Review provenance: separate occupied_action agent at the parent's request;
direct reconstruction from the canonical potential and saved branch rows,
without importing the clock-matching implementation. It is a separate-agent
review, not an external mathematical certificate. Exact reviewed file SHA-256:
`5b24a26e4b73b6d4822736cb6d6a11458838dc868ffa6c333a3a9cd9c927d534`.
Further source hashes are in `CLOCK_REVIEW_INPUT_SHA256.txt`.

The quantified claim is local to a homogeneous occupied stationary branch
with I,X>0 and positive fixed-frequency amplitude Hessian H. It retains the
specified canonical microscopic host/mediator and the separately proposed
response action. It neither asserts a global thermodynamic P(X) across phase
coexistence nor identifies the response sector with a microscopic match.

## Direct reconstruction

For canonical radial amplitude rho=sqrt(2I), the host quadratic Lagrangian is

    L2 = (dot(a)^2-|grad a|^2+dot(b)^2-|grad b|^2)/2
         -(Ar a^2+2h a b+Bh b^2)/2
         +(dot(psi)^2-|grad psi|^2)/2 +2 sqrt(X) a dot(psi),

where psi=sqrt(kappa) pi. Differentiating V-I X, rather than V alone, gives
Ar=4 lambda I, h=a_micro sqrt(2I), and
Bh=M^2+2 mu chi+3chi^2. With chi=-x and mu=-3M/8, the latter is
M^2+3Mx/4+3x^2. This independently checks the potentially load-bearing sign.

Implicit differentiation of V_I=X, V_chi=0 gives

    dX/dI = 2lambda-a_micro^2/Bh = Aeff/(2I).

The envelope derivative is P_X=I/epsilon, and consequently
P_XX=2I/(epsilon Aeff), Delta0=4 kappa X/Aeff. Positive H ensures Aeff>0.
The isolated host low-mode speed is Aeff/(Aeff+4X). All normalization factors
agree with the convention X=-(dtheta)^2 with no factor one-half.

For real Omega and k, Fourier elimination of a,b uses H+s1 with
s=k^2-Omega^2 and produces

    Delta(s)=4 kappa X [(H+s1)^(-1)]_rr.

The inverse element is (Bh+s)/[(Ar+s)(Bh+s)-h^2], with the positive sign
shown in the note. Its first derivative at s=0 is negative and equals
-4 kappa X(Bh^2+h^2)/(Ar Bh-h^2)^2. The kernel poles belong to the eliminated
Dirichlet block; interpreting them alone as full-theory instabilities would
be incorrect, and the note explicitly avoids doing so.

For |s|<=eta lambda_min and eta<1, the spectral weights are nonnegative and
each factor lambda_j/(lambda_j+s) lies between 1/(1+eta) and 1/(1-eta).
The displayed relative-error bound follows by a positive weighted average.
The stated condition |Omega|,k<=.1 sqrt(lambda_min) really gives eta=.01:
the difference of the two nonnegative squares has magnitude at most their
individual maximum. No extra factor of two is needed. The bound concerns
real frequencies; it should not be read as a complex-frequency modulus bound.

Substitution into the full response determinant independently yields the
listed quartic and the low-mode k^4 coefficient. For two positive simple low
roots, the smaller root has both f'<0 and A c^2-C<=0, while the larger has
both f'>0 and A c^2-C>=0. Therefore b>=0 when 0<c^2<1. At zero angular
mixing one factor can vanish, giving b=0 rather than a strictly positive
correction. The note uses the correct nonnegative formulation.

At k=0, the full determinant has two zero-frequency modes and its two nonzero
gap squares solve det[H+4X diag(1,0)-Omega^2]=0. At the matter light cone,
s=0 exactly, so the normalized determinant reduces to

    Delta0(q-gamma y T)-gamma y r T^2.

These identities confirm that the derivative-expansion scale from H is not
the physical coupled k=0 gap. They do not imply a group-speed theorem, which
the note explicitly declines to claim.

Dividing the coexistence polynomial by M^3 yields x=1-81/(32M)+O(M^-2).
Substitution into I=sqrt(U/lambda) gives I=M/2-69/64+O(M^-1). Hence
Ar=4M-85/8+O(M^-1), h^2/Bh=4M-93/8+O(M^-1), and Aeff->1.
The two distinct light scales consequently tend to 1 and 2 respectively;
the mediator mass does not set the derivative cutoff. The four table rows
in section 5 were separately reconstructed from the saved inputs and agree.

Finally, in the full principal polynomial the amplitude part contributes
two luminal fronts and the remaining factor is the Delta=0 response/clock
polynomial. At the radial matter cone its determinant is

    -gamma (Z0+gamma y) y^3/X <0.

With positive E,A,C,kappa, the leading coefficient is positive and this
negative value implies one response/clock front above one. The kernel's
O(k^-2) argument applies away from Omega/k=1; the full principal determinant
independently supplies the luminal factors there. This closes a possible
limiting-direction gap. The physical conclusion is conditional on retaining
the response derivative ansatz at high frequency, exactly as stated.

## Obligations and evidence

| Obligation | Verdict |
|---|---|
| Canonical Hessian and sign of Bh | Passed |
| P_X, P_XX, epsilon normalization on local occupied branch | Passed |
| Exact Schur kernel and real-frequency validity bound | Passed |
| Quartic, k^4 shift, light-cone and k=0 gap identities | Passed |
| Four source-row table reconstructions | Passed to stated floating tolerance |
| Large-M light-scale distinction | Passed |
| Conditional high-frequency front obstruction | Passed |
| Exact continuum group-speed bound | Not asserted; not addressed |
| 1224 spectra and reported first crossing | Out of scope; not rerun |
| Microscopic response-sector matching, vacuum and nonlinear completion | Not supplied; remains open |

The dependency graph is canonical action -> stationary Hessian -> branchwise
P derivatives / exact Fourier Schur kernel -> low-energy bound and physical
gap distinction. The response determinant additionally depends on the
separately stipulated CE-FM-079 response ansatz. No external theorem is needed.

`check_clock_review.py` supplies 29 independent reconstruction controls,
including four saved rows with four quantities each. The completed v2 record
is `run_clock_review_001/manifest.json`, validated against current input bytes.
This script does not import the reviewed implementation or rerun its spectra.

Reproduction and validation:

    python3 check_clock_review.py <fresh-output-results.json>
    python3 <mathbox computation-audit>/scripts/validate_manifest.py run_clock_review_001/manifest.json --root <repository>

The exact runner argv and observed software/input/output hashes are retained
in the manifest. No correction to the clock source is requested. The smallest
physical missing implication remains the microscopic response matching near
and above the light host-amplitude scale; large M alone does not supply it.

Proofread self-review: this new review only; routine edits none pending;
mathematical-token corrections none pending; unresolved prose issues none.
