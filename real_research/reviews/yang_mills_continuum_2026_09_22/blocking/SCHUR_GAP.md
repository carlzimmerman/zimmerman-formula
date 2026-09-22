# Exact blocking with its induced norm

Checkpoint YM-C1; base `b73311096299e2f1816be00036ccdb2922bc44d4`.
This is an elementary spectral comparison and conditional multiscale
reduction, not a construction of four-dimensional Yang–Mills theory.
No novelty claim is made for Schur complement or variational methods.

## 1. A gap-transfer lemma

First work in finite-dimensional complex Hilbert spaces P and Q. Let H be
nonnegative with a nonzero kernel, decomposed as

    H = [ A  B* ],       D >= d I_Q, d>0.
        [ B   D ]

All energies are measured after subtracting the ACTUAL ground energy.
Define

    C = D^{-1} B,
    S = A - B* D^{-1} B,
    J p = (p, -Cp),
    G = J*J = I_P + C*C.

The coarse self-adjoint operator in the ordinary P inner product is
K = G^{-1/2} S G^{-1/2}. Equivalently, S is a quadratic form in the
G inner product. The map J identifies ker S with ker H. Since
ker K = G^{1/2} ker S, the isometric embedding U=J G^{-1/2} identifies
ker K with ker H in the ordinary Hilbert-space norms.

**Proposition.** If the nonzero spectrum of K is bounded below by gamma>0,
then the nonzero spectrum of H is bounded below by

    m = (gamma^{-1}+d^{-1})^{-1} = gamma*d/(gamma+d).

The kernel dimensions agree. If K has a nonzero excited sector, its lowest
positive eigenvalue gamma_exact additionally satisfies

    gap(H) <= gamma_exact.

**Proof.** Completing the square gives, for r=q+Cp,

    <(p,q),H(p,q)> = <p,Sp> + <r,Dr>.

The vanishing of both nonnegative terms characterizes ker H = J ker S.
Write p=p_0+p_perp by G-orthogonal projection onto ker S. Then Jp_0 is
in ker H, Jp_perp is orthogonal to ker H, and

    ||Jp_perp||^2 <= <p,Sp>/gamma.

Since (p,q)=Jp_0+Jp_perp+(0,r),

    dist((p,q),ker H)
      <= ||Jp_perp||+||r||
      <= sqrt(<p,Sp>/gamma)+sqrt(<r,Dr>/d).

The scalar Cauchy–Schwarz inequality bounds the square of the last
expression by

    (1/gamma+1/d) [<p,Sp>+<r,Dr>].

This is the claimed spectral inequality on the full vacuum complement.
For the upper comparison, choose q=-Cp and minimize the Rayleigh quotient
on the embedded excited subspace J((ker S)^{perp_G}). It is a subspace of
the full vacuum complement. QED.

The proof does not suppose that the fine vacuum lies in P. Replacing it
by the bare electric vacuum would invalidate the decomposition of the
actual vacuum complement.

### Operator-domain version

The same proof applies to a nonnegative closed form on P direct-sum Q
when: D is self-adjoint and D>=d; C is bounded from P to Q; the form admits
the displayed completion-of-squares representation with closed S; its
domain is exactly the vectors (p,q) with p in dom(S^{1/2}) and q+Cp in
dom(D^{1/2}); and the coarse G-form has the asserted gap. In that case K
means the operator associated with the closed form k[z]=s[G^{-1/2}z],
whose form domain is G^{1/2}dom(s), not an unchecked operator product.
Bounded C makes
G a bounded, coercive metric and J a closed embedding. These assumptions
must be checked for an unbounded Yang–Mills Hamiltonian; a finite matrix
proof alone does not check them. More general unbounded C would require
a separate graph-domain argument and is not claimed here.

If the projection defining P commutes with the gauge action, the blocks,
C, S and G inherit equivariance. This preserves the gauge-invariant
sector, but does not identify the coarse space with a smaller Wilson
lattice, or make S local. Those are additional obligations.

## 2. Why the metric cannot be discarded

For any real M take

    H_M = [0    0       0],  P=span(e_1,e_2), Q=span(e_3).
          [0  1+M^2     M]
          [0    M       1]

Then D=1, S=diag(0,1), C=(0,M), and G=diag(1,1+M^2).
The naive coarse operator S always has gap one, while

    gap(H_M) = (M^2+2-sqrt(M^4+4M^2))/2 -> 0.

Thus no positive uniform full gap follows from unweighted Schur gap one
and eliminated-block bound one alone. The correct coarse gap is
gamma=1/(1+M^2), and the proposition gives 1/(M^2+2), consistently.
For M=1 the exact gap is (3-sqrt(5))/2<1/2: even the naive harmonic
formula using S without G is false. This is an exact counterexample,
not a floating eigenvalue observation.

For a general compression PHP without the Schur correction, the problem
is more immediate: off-diagonal mixing can change both vacuum and gap.
Likewise the correct Schur complement at energy E is energy-dependent;
using S at E=0 is justified here by the exact form identity after the true
vacuum energy has been subtracted, not by assuming the spectra are equal.

## 3. A finite inverse-gap budget across arbitrarily many scales

Suppose H_0,...,H_K are the EXACT metric-normalized Schur operators of a
successive blocking, all in the same physical energy units and each with
simple vacuum. At step j the eliminated D_j obeys D_j>=d_j>0. If the
terminal gap is at least M_*, successive use of the proposition gives

    gap(H_0) >= [1/M_* + sum_{j=0}^{K-1} 1/d_j]^{-1}.

This follows by induction on lower bounds; it is not an assertion that
the bound is exact. Crucially there is no product of a fixed loss factor
at every ultraviolet scale. The induced metrics must actually be retained
at each step for H_{j+1} to be the announced operator.

Let L>1 and a_j=A L^{j-K}, so A is a fixed terminal physical length.
An exact model for the inverse coupling profile is

    x_j = 1/[s+q(K-j)],  s>0, q>=0.

This profile is an auxiliary model, not a proved nonperturbative Yang–Mills
flow. Assume nevertheless that the eliminated sector has the physically
scaled estimate d_j>=c x_j/a_j for some c>0 independent of j,K and volume.
Then geometric summation gives

    sum 1/d_j <= (A/c) sum_{r=1}^K (s+qr)L^{-r}
               <= (A/c) [s/(L-1)+qL/(L-1)^2].

If M_*=m_*/A with m_*>0, the resulting lower bound is

    gap(H_0) >= (1/A) /
       [1/m_* + (s/(L-1)+qL/(L-1)^2)/c] > 0,

uniformly in the ultraviolet depth K and the volume wherever the stated
block estimates hold. Even logarithmically weakening ultraviolet electric
scales would be compatible with this cost. They are not the decisive
obstruction in this exact comparison.

If actual renormalization differs from this toy profile, only a uniform
bound on sum a_j/x_j is needed for the stated d_j estimates. Showing an
asymptotic beta-function coefficient is not itself such a bound on the
exact interacting block forms.

## 4. What this does and does not unlock

The comparison removes one avoidable loss in a hypothetical RG proof.
It neither supplies the actual blocking nor generates a mass. Three
operator estimates remain:

1. Construct useful gauge-compatible projectors, domains and exact
   vacuum-energy subtractions through every scale. A projector defined
   using an already known global gapped spectral subspace is circular.
2. Prove the eliminated-mode bounds D_j>=c x_j/a_j uniformly in physical
   volume. Bare electric positivity does not prove this after an extensive
   interacting ground energy is subtracted.
3. Control the terminal pair (S,G), including nonlocal operators and all
   generated interactions, sufficiently to prove its volume-uniform gap.
   Our I15 theorem applies to a specified Wilson-type Hamiltonian; no
   theorem here identifies that Hamiltonian with this exact coarse pair.

In addition, a Yang–Mills continuum construction, relativistic symmetry,
local observable renormalization, finite-mass/nontriviality witnesses and
the other field-theory axioms still have to be established. The continuum
route records the exact correlation-transfer implication.

No amount of this algebra alone establishes either item 2 or item 3.
The next discriminating step is to construct an actual coarse conditional
vacuum that retains the long-wavelength gauge modes and test its D_j
bound, instead of treating a running coupling as the full coarse action.
