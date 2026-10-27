# Independent focused review of the ground-state analyticity restriction

Date: 2026-10-19. Target:
`sol61_push/shared_state_2026_10_19/occupations/OCCUPATIONS.md`, SHA-256
`6703bb835bd8ab2c1607085799a0906191fd164d13d5d0f00fbabf113049e5ad`,
18,301 bytes at inspection. Scope: §4, with the bounded-source/cutoff
application in §5 and enough of §§1–3 to check the operator/state dictionary.
No occupations file is changed. No occupation numerical code or literature
claim in §6 was audited by this reviewer.

**Claim and verdict.** For self-adjoint H0, bounded self-adjoint D, a simple
ground eigenvalue isolated by a positive spectral gap, and a unitary inversion
commuting with H0 and reversing D, the ground energy of H0-gD is even real
analytic near g=0 and its source response is odd real analytic. Consequently
it cannot equal p_sat*g/(a+|g|), with a,p_sat>0, on a neighborhood of zero.
Primary verdict: **proved as written**, under exactly these stated hypotheses.
The application to an actual shared original-model state remains conditional
on isolation, inversion, the bounded positive-inventory source sector and the
appropriate COM reduction. Classical constrained stability alone does not
prove these quantum spectral hypotheses.

## Reconstruction of the decisive step

Let E0 be the isolated ground eigenvalue, gamma its distance to the remaining
spectrum, and take C={z:|z-E0|=gamma/2}. Self-adjointness gives
norm((z-H0)^-1)<=2/gamma uniformly on C. For complex g with
|g|norm(D)<gamma/2, the factorization of z-H0+gD and its Neumann series
give a norm-holomorphic resolvent uniformly on C. Its contour integral is a
holomorphic projection equal at zero to the one-dimensional ground projector.
Locally its rank stays one, so the enclosed eigenvalue is holomorphic as well
(one can use the contour integral with an extra factor z to avoid multiplying
the unbounded H0 directly by the projector). For real g, bounded-perturbation
spectral separation retains the ground branch on a sufficiently small interval.
The unitary relation I H(g) I^-1=H(-g), together with this branch's uniqueness,
forces E0(g)=E0(-g). Hellmann–Feynman then gives an odd analytic response.

Thus P(g)=chi*g+O(g^3). In contrast, the positive side of the proposed rational
law has quadratic term -p_sat*g^2/a^2 and its negative side the opposite sign.
Equivalently its one-sided second derivatives differ by 4p_sat/a^2. Even
agreement only for sufficiently small positive g conflicts with the analytic
branch's absent quadratic coefficient. The stated discrepancy when slopes
match, +(p_sat/a^2)g|g|+O(g^3), has the correct sign.

## Obligation matrix

| Obligation | Result |
|---|---|
| Spectral contour stays off the spectrum | Passed: gamma/2 and the strict bounded-perturbation inequality provide the needed uniform resolvent estimate. |
| Infinite Hilbert space and unbounded H0 | Passed: bounded perturbation keeps the domain fixed; contour-resolvent construction uses bounded operators and a finite-rank projector. |
| Ground branch remains ground for real small g | Passed: spectral shifts bounded by |g|norm(D), leaving a positive local separation. |
| Inversion implies even energy, not only even spectrum | Passed: the enclosed simple branch is unique and ground locally. |
| Physical response equals energy derivative | Passed within the nondegenerate ground-state contract; no thermal occupation count is substituted. |
| Cusp contradicts analyticity | Passed: the rational signed response has a nonzero g|g| term for a,p_sat>0. |
| Fixed positive NR inventory yields bounded D_k | Passed for h_k=sin(kz)/k at k!=0: sum of positive constituent masses bounds the multiplication operator by M_tot/|k|. Relative-coordinate restriction/compression preserves this bound. |
| Classical energy minimum implies quantum gap | Not claimed; correctly marked conditional in the target. |
| Arbitrary relativistic signed-charge sector bounded | Not claimed; correctly excluded. |
| Finite-temperature extension | Correctly restricted to finite-dimensional Gibbs traces or an actually trace-class, analytically dominated infinite-dimensional trace. Unconfined canonical normalization is not assumed. |
| Delta lower cutoff | Correct conditionally on actual two-level identification Omega=2dDelta: Omega>=gamma and d<=Dmax give Delta>=gamma/(2Dmax). |
| Soft or infinite families excluded universally | Not claimed; zero-gap/critical/infinite-object and nonuniform ensemble limits are explicitly retained. |

No mathematical correction is required for the reviewed theorem or its
bounded-source application. A full prediction still needs the actual internal
source and state; the proof does not establish a gap for the GP/fluid state
constructed in the equilibrium lane, and that lane's classical energy theorem
must not be substituted for the missing quantum isolation hypothesis.

Review provenance: independent algebra/operator reconstruction by the sibling
equilibrium subagent in the same parent session, using the raw target and
stated operator hypotheses. This is not an independent external referee report
or a verification of the entire occupation packet. No numerical calculation
was needed for this focused proof check.
