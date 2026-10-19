# Independent review of the first neutral cosine interaction

**Primary verdict: proved as written**, for the flat-subtracted, first
interacting soft vacuum contribution of the declared minimally coupled compact
cosine EFT, with the common finite-part scheme and the two fixed-parameter
paths stated in `neutral_interactions/RAW_DERIVATION_v1.md`. This verdict does
not extend to unknown hard curvature matching, absolute vacuum constants,
higher loops or QCD.

The blind derivation `INDEPENDENT_RAW_v1.md` and its SHA-256 were saved before
opening the target directory or reading a coordinator coefficient. It derives
the loop coefficient, canonical constant mode, mass-retuning sign and actual
metric response. The exact target and computation bytes read are pinned in
`INPUT_PROVENANCE.json`. No target file was edited and no new mathematical
experiment was executed during this review.

## 1. Independent result and comparison

For V=2π²R³, z=sqrt(m²R²-1)>0, the all-mode coincident finite part is

    G_R=-z coth(πz)/(4πR),       G_∞=-m/(4π).

The full cosine quartic is λ=-m²/κ and three Wick pairings give

    W_2=(λ/8)V G_R².

At fixed L,m,κ, the flat-subtracted spatial stress has leading power

    Δτ_A,2=m²/(384π²κLR²)+exponential.

At fixed flat pole mass, Σ_∞=λG_∞/2=+m³/(8πκ), so the finite mass
retuning is δm²=-M³/(8πκ). Its Gaussian insertion completes the square:

    Δf_B,2=(λ/8)(G_R(M)-G_∞(M))²,
    Δτ_B,2=1/(1536π²κLR⁴)+1/(1024π²κLM²R⁶)+O(R^-8)+exponential.

These agree with all displayed coordinator formulas, including both exact
finite-radius metric derivatives. The metric operation is f+R f'/3 at fixed
L and declared comparison inputs. Applying f alone would give the wrong
stress and leading coefficient.

The isolated constant-mode figure-eight is W_00=-1/(8κm²V), with
τ_00=1/(8κLm²V²). It occurs once in G_R², together with mixed and
nonconstant contractions. The canonical compact integral independently yields
Z0~(μ/m)e^(κm²V)[1+1/(8κm²V)+...]. Its induced sqrt(V) measure cancels
the Haar saddle log(V). Adding W_00 to the full diagram would double-count.

The fixed-pole condition also retunes the classical -κm²V term. Its first
known shift is +M³V/(8π); further terms at absolute order 1/κ require the
next pole-mass relation and vacuum matching. The target correctly restricts
its result to the common flat subtraction, where all these extensive terms
cancel. This is a limitation on an absolute-vacuum extension, not a defect in
the target's flat-subtracted claim.

## 2. Dependency and obligation checks

| Implication | Status | Independent check |
|---|---|---|
| Supplied cosine → quartic sign and normalization | Passed | Four derivatives give -m²/κ; vertex /4! times three Wick pairings |
| First interaction at two loops is complete | Passed | No cubic; sextic one-vertex and connected two-quartic diagrams begin at three loops |
| S3 scalar domain and degeneracy | Passed | Harmonic polynomials on R4 give l(l+2)/R² and dim=(l+1)², including l=0 |
| Tadpole finite part matches Gaussian scheme | Passed | ζ_R(0) and coth sum; parent integrated determinant differentiated by hand below |
| Local UV subdivergences are subtractable | Passed within stated scheme | Explicit mass and vacuum subtraction in independent raw section2 leaves λVG_R²/8 |
| Path A exact metric derivative | Passed | Direct R derivative with Rz'=m²R²/z |
| Flat-pole retuning sign | Passed | Σ_∞>0 for negative λ and negative finite G_∞; hence δm²<0 |
| Path B completed square and metric derivative | Passed | Direct algebra with finite mass insertion, then spatial derivative |
| No 1/R in either computed diagram | Passed | Exact algebraic functions of R^-2 plus coth winding exponentials |
| Constant mode isolated once | Passed | Explicit G0²+2G0G_>+G_>² decomposition and compact integral |
| Finite curvature/hard data determined | Not claimed | Additional ξℛϕ² and local gravitational matching remain independent |
| Full QCD / all-loop implication | Out of scope | No such claim follows from this EFT calculation |

The degeneracy proof uses dim Harm_l(R4)=binom(l+3,3)-binom(l+1,3)=(l+1)².
The coth identity also follows by differentiating the elementary product
sinh(πz)/(πz)=product_(n>=1)(1+z²/n²); its differentiated sum converges
absolutely for z>0. This review uses these elementary identities directly.
No new primary-source theorem is asserted or authenticated. The coordinator's
older microscopic coupling dictionary is not used; source coverage in the
parent Gaussian packet does not become independent source coverage here.

## 3. What the finite computation actually checks

The v2 implementation follows its declared grid exactly: eight mR values
1.05,1.25,2,3,5,10,20,30; three masses 0.5,1,2.5; working precisions 70 and
95 decimal digits; 256 explicit spectral modes, geometric tail k=0..40;
four stated Poisson winding-integral cases. It performs 16 symbolic checks
and 108 numerical checks at each precision. It uses κ=30m and L=.7 as
specified internal test inputs, not physical fits. There is no answer-based
case filtering or hidden adaptive domain extension.

The finite spectral sum and its tail constitute an orthogonal implementation
of the coth propagator. The exact symbolic and numerical spatial derivatives
check the implemented formulas; the Wick, loop-completeness and matching
arguments remain analytical obligations and have been derived independently
above. The symbolic expansion variable z in the code means 1/(mR)², whereas
the independent raw uses z=sqrt(m²R²-1); these are local notation choices,
not a mathematical mismatch.

One advertised check is weaker than its wording suggests. At
`check_two_loop_v2.py:134`, the determinant derivative dW/da is assigned the
closed coth expression; line135 compares it algebraically with the same
coth expression in G_R. It does not numerically differentiate a separately
implemented determinant. It is a chain-rule/normalization consistency check,
not independent numerical determinant verification. The same limitation
applies to the analogous symbolic check.

This does not leave the mathematics open. The parent determinant is

    W_G=-πz³/6+π∫_z^∞ t²/(exp(2πt)-1)dt.

Its direct derivative is

    dW_G/dz=-πz²/2-πz²/(exp(2πz)-1)
             =-πz² coth(πz)/2,

and multiplying dz/dm²=R²/(2z) gives VG_R/2. This hand check supplies the
missing independent chain, without pretending the program did it.

## 4. Tail bound and precision failure

The geometric tail proof is correct. Truncating 1/(n²+a²) after k=K
leaves magnitude at most a^(2K+2)n^(-2K-4); multiplication by the extra
a² in G_R produces the implemented bound a^(2K+4)ζ(2K+4,N+1), divided by
2π²R. The integral-test upper bound for that positive Hurwitz tail is also
correct.

For the explicit 50-term Euler--Maclaurin Hurwitz implementation, the periodic
Bernoulli integral gives a remainder bounded by the magnitude of the last
included Bernoulli term for the real s>1,Q>0 domain used here. The code
weights each error by its actual a^(2k), adds them and applies the extra a²
correctly. The derivation in `SPECTRAL_CHECK_AND_PRECISION.md` therefore
supports the programmed truncation bound. It is not an interval certificate
for floating arithmetic. The separate fixed 1e-65 allowance is the actual
absolute numerical acceptance threshold in addition to the scaled 1e-50
check; the printed smaller errors must not be relabeled rigorous error bars.

The Poisson winding integrals are independently correct: for c>0,q>0 let
A(c)=∫t^(-3/2)exp(-q²t-c/t)dt=√π c^(-1/2)exp(-2q√c). The implemented
integral is 2(4π)^(-3/2)[A+2cA']=-q exp(-2q√c)/(2π).
Individual winding terms need not be positive even though the full heat trace
is positive; the executed code checks the signed winding representation.

The preserved v1 run failed at mR=5 because error ~1.86e-63 exceeded its
1e-65 roundoff allowance, while still satisfying the looser scaled identity
tolerance. It did not complete the full grid. The precision diagnostic uses
the same algorithm at 160 digits as a higher-precision reference, not a
separate independent implementation. It nevertheless localizes the error to
small Hurwitz tails before amplification. Inspection of the installed
mpmath1.3.0 `_hurwitz_em` source confirms its absolute `mag(t)<-prec`
stopping criterion, consistent with the narrow diagnosis. The claim is an
accuracy limitation of this use, not a general library defect.

The v2 completed output reports maximum scaled errors approximately
4.20e-71 at 70 digits and 2.54e-81 at 95 digits. Agreement and the analytic
tail bounds support the declared finite assertions only. No new experiment
was run here, and no 160-digit reference is treated as a proof by itself.

## 5. Manifest audit, remaining gap and review provenance

The validator was run against current inputs for all three records:

    two-loop-001: valid provenance, status failed;
    precision-001: valid provenance, status completed;
    two-loop-002: valid provenance, status completed.

The declared dependency lists match their manifests, all pinned input hashes
remain unchanged, and all successful result hashes validate. The failed run
is retained without rewriting its code or result history. The corrected v2
code and contract supersede only the numerical-tail implementation; the
physical formulas are unchanged. Zero process exit alone was not used as
mathematical evidence.

The strongest safe statement is that the complete first quartic vacuum
diagram, with required finite pole-matching insertion, has the displayed even
curvature powers and exponential terms in this minimally coupled finite-part
S3 EFT. A physical inverse-radius term would require an omitted matching,
state, defect or higher-order mechanism with its own derivation. No concrete
error remains in the target formula at the stated order.

Review provenance: fresh derivation in this subagent before target reads,
then direct proof/code/manifest audit; same model family and shared elementary
background may still correlate errors. No child reviewer was spawned.
Mathematical proofreading covered the new raw and this review; no
mathematical-token typo correction was made to the frozen raw. All findings
are in the review, with targets preserved. The QED lane was not modified.
