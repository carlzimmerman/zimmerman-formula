# Independent review of the two-flavor QCD/QED constant mode

Verdict: the topology packet's compact group integral, retained-action
susceptibility identity, canonical Gaussian measure and proposed replacement
factor are correct with the stated restrictions below. No additional
constant-mode determinant or canonical normalization may accompany that
replacement factor. These results do not determine the full metric response,
the fixed-positive-mass coefficient c_H, or alpha.

`INDEPENDENT_DERIVATION.md` was saved before this reviewer read either the
topology packet or the coordinator's zero-mode note. No child was spawned for
this review and no new mathematical experiment was executed. The subsequent
audit read the packet's derivations, reports, scripts, contracts, source
records and completed run evidence. Exact reviewed bytes are pinned in
`INPUT_PROVENANCE.json`.

## 1. Action, group integral and derivatives

Let U=a0+i a.tau in SU(2), a0^2+a^2=1, Q=diag(2/3,-1/3),
mu=m Sigma V, eta=e^2 C V, z=2mu cos(theta/2), with two equal positive
renormalized masses and fixed leading coefficients Sigma,F,C. Direct Pauli
algebra gives

    Tr(Q U Q Udagger)=5/9-s,  s=a1^2+a2^2.

The normalized-Haar marginal of s is uniform on [0,1]. Integrating the two
remaining circle angles gives the packet's aligned-vacuum-subtracted answer

    Zhat(z,eta)=integral_0^1 ds exp(-eta s) I0(z sqrt(1-s)).

The unsubtracted conventional Dashen action multiplies this by exp(5eta/9).
That factor is independent of mass and theta at this retained order; its
metric response is an ordinary constant vacuum shift and must remain in the
chosen subtraction/matching convention. It cannot be silently assigned to a
predicted finite-size vacuum term.

At eta=0, Zhat=2 I1(z)/z, with value one at z=0. At z=0,
Zhat=(1-exp(-eta))/eta. With r(z)=I2(z)/I1(z), its leading charge insertion
is K(z)=<s>_0=2r(z)/z. The sign and charged-pion mass normalization agree
with Urech's leading operator, after writing e explicitly:
Delta=2e^2 C/F^2. The source is SU(3); this check does not equate its fitted
coefficient numerically to a two-flavor coefficient.

At theta=0 all mass/theta dependence of this action is through z, whereas
eta is independent of both. Consequently

    chi=(mu/(4V)) partial_mu log Z,
    Cbar=(1/(2V)) partial_m log Z=(Sigma/2) partial_mu log Z,
    chi=(m/2) Cbar.

Here Cbar is the positive flavour-averaged condensate defined by the common
mass derivative. This does not assert equality of individual condensates
when QED distinguishes the charges. The identity holds for all eta in this
retained action if the additional prefactor is independent of mass and
theta. Higher mass/charge operators, electromagnetic anomalous sectors,
mass-dependent matching, and independent charge dependence of the LECs are
outside that identity. At theta=pi the degenerate leading mass term vanishes;
an all-orders phase statement cannot be extracted there.

The pure-QCD fixed-topology coefficients
I_nu(mu)^2-I_(nu-1)(mu) I_(nu+1)(mu) are consistent with this normalized
Fourier sum. Their small-mass weights suppress the conditioned Dirac
zero-mode condensate pole in the summed condensate. No normalization
inconsistency or pole-cancellation error was found.

## 2. Canonical measure and Gaussian charged pair

The orthonormal constant harmonic is V^(-1/2). For a canonical pion field
pi^a, its constant coordinate is q^a=sqrt(V) pi^a, and near U=1,
a_j=q_j/(F sqrt(V)). The induced L2 metric on the constant S3 is
F^2 V times its unit metric. For a fixed determinant scale nu and canonical
measure product nu dq/sqrt(2pi), normalized Haar is therefore multiplied by

    Ncan(V)=sqrt(pi/2) (nu F sqrt(V))^3.

The identity saddle at theta=0 is

    Zhat_G=exp(2mu)/[2sqrt(pi) sqrt(mu)(mu+eta)],
    Ncan Zhat_G=exp(2mu) nu^3/[M(M^2+Delta)],
    M^2=2m Sigma/F^2.

This is exactly one neutral real Gaussian mode and two charged real
Gaussian modes. The charged-pair partition ratio is

    M^2/(M^2+Delta)=1/(1+eta/mu).

The two charge labels do not require an additional determinant doubling.
At fixed positive masses and couplings this ratio is independent of radius.
The omitted unsubtracted exp(5eta/9) is a separate classical constant,
not part of this ratio after the stated vacuum subtraction.

For a volume-only effective action W=-log Z on the round S4, its isotropic
metric response is partial_V W, equivalently f-H partial_H f/4 for f=W/V.
Normalized Haar alone gives a Gaussian contribution +3/(2V) to this
response. The derivative -partial_V log Ncan is -3/(2V), cancelling it.
The canonical Gaussian mass determinants above have radius-independent
logarithms after the extensive classical term is removed. This verifies
the cancellation; dividing log Z by V would not compute the same stress.

The charge-insertion metric identity also checks independently:

    delta rho=e^2 C [K(z)+z K'(z)]=2e^2 C r'(z)+O(e^4).

Both z and eta vary with V in this fixed-coupling derivative. The leading
eta/mu term in W is volume independent and drops from this stress; the
remaining first-order group-model term at large mu is 3e^2 C/(4mu^2).
It is a constant-mode interaction correction, not a full QCD curvature
coefficient.

## 3. Replacement factor and physical limits

The proposed factor

    Q(mu,eta)=Zhat(mu,0,eta)/Zhat_G(mu,eta)

is the correct algebraic replacement of the Gaussian constant mode by its
compact integral. In particular
(Ncan Zhat)/(Ncan Zhat_G)=Q: the canonical normalization cancels. A full
canonical S4 pion determinant already contains its constant eigenvalues
M^2,M^2+Delta,M^2+Delta. Multiplying that determinant by Q does not permit
another Ncan or another Gaussian constant-mode determinant. The classical
vacuum subtraction must be made consistently in numerator, denominator and
the determinant assembly. The ratio still has this form if exp(2mu) is
removed from both exact and Gaussian constant-mode partition factors.
Local curvature subtractions and constant/nonconstant-mode interactions
must also be matched at the same epsilon order. This algebra is not itself
a completed finite-volume QCD calculation.

The displayed Gaussian denominator is the positive identity saddle. At
general theta it requires cos(theta/2)>0 and sufficiently large positive
mu cos(theta/2); it is not a uniform theta=pi approximation.

For H=1/radius, V=(8pi^2/3)H^(-4). The epsilon regime requires F L>>1,
Lambda_chi L>>1 and both neutral and charged pion masses times L small.
Keeping mu,eta finite as V grows requires m and e^2 to scale as H^4,
so M/H tends to zero. Keeping physical positive m,e fixed instead sends
mu,eta to infinity and eventually leaves that regime as H/M tends to zero.
The Gaussian limit of the group function is mathematically valid but
does not extend the epsilon expansion to all those fixed-mass volumes.

Ncan is a specific matched measure factor, not the complete N(V,alpha)
of the QCD path integral. Heavy modes, nonconstant modes, gravitational
matching and vacuum conventions remain. An arbitrary mass/theta-independent
N(V) leaves the displayed susceptibility and condensate intact while
changing the metric response. It cannot supply or rule out c_H. The
packet's hypothetical N(V) example correctly diagnoses that information
gap and is not evidence that such a term occurs physically. This review
draws no conclusion about c_H from it.

## 4. Source verification and computational evidence

The primary Lenaghan--Wilke paper, hep-th/0108166v2, was checked in its
exact extracted PDF/text for the leading flat finite-volume group integral,
fixed-topology determinant and derivative conventions. Its displayed
two-flavor Bessel expression differs by a constant factor 1/2 from the
chosen normalized Haar convention; the derivatives and the consistently
normalized Fourier coefficients agree. Its flat-torus result does not
establish a full curved-QCD stress. The original Leutwyler--Smilga PDF was
not accessible in the packet's acquisition; this reviewer makes no claim
of independent extraction from that original.

Urech, hep-ph/9405341v2, was checked for its leading charge operator and
mass splitting, with its e-in-Q convention translated explicitly. These
primary sources support the starting actions and known group formulas.
The Pauli trace, disk integral, Ward identity at retained finite eta,
canonical measure, metric cancellation and Q assembly were derived here
algebraically; they are not attributed as source theorems. Metadata
authentication was inherited from the packet's source records, while this
review read and hash-checked the exact retained PDF/text bytes and selected
equations. `SOURCES.json` records that division.

The pure run_001 completed 325 checks per precision at 100/130 digits,
with 30 primary cases per precision and repeated-precision discrepancy
at most 3.020e-100 on its stated scales. The QED run_002 completed 105
checks per precision at 80/110 digits, with 18 primary cases per precision
and discrepancy at most 1.280e-80. Both manifests validate against current
inputs. The scripts use independently parametrized Haar quadrature,
Bessel expressions, finite differences and canonical/volume comparisons;
the pure run also controls the finite topology tail analytically. Code and
evidence were audited, not rerun. Arbitrary precision and repeated-precision
agreement are not interval certification or full physical matching.

qed_run_001 reached its CPU cap and is retained as resource-inconclusive;
the successful separate run_002 supplies the completed QED evidence. No
failed attempt is hidden and no process exit is treated as sufficient
mathematical proof.

The established result is a correctly normalized, unfitted leading chiral
finite-volume response and a conditional assembly prescription. Computing
c_H/C_p^3 or selecting alpha still requires independent physical matching
beyond these observables.
