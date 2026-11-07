# Independent audit: the Cantor principal equations

**Verdict: the proposed diffuse identities are correct. The stress
Cantor-divergence equation is redundant with scalar conservation and
clock compatibility. Nonzero Cantor variation, if present, has acoustic
principal polarization; this does not construct it or prove uniqueness
or its impossibility.**

Independent delegated audit, 2026-11-06, of the parent's PF15 candidate
message. At first inspection only the PF15 contract/review directory
existed. Retain the strict on-branch bounded PF13 class, dphi in local
spacetime BV, Lipschitz A,Pi and regular g in C1 intersect W2,1. The
clock/cap/hyperbolic compact margins hold. The already excluded jump
part is zero. All conclusions below concern the remaining Cantor part.

## 1. The chain rule has specified representatives

Write p_b=partial_b phi and k^a=h n^a. Compositions with r,p,n,H and
the acoustic state are C1 on the compact admissible range. Apply the
BV diffuse chain rule to the combined vector of p and the Lipschitz
auxiliary/metric/scalar coefficients. At Cantor measure points the BV
clock gradient has its canonical approximate value; there is no choice
between two jump traces. All coefficients below are evaluated at those
approximate values. Lipschitz A,Pi,phi and C1 metric coefficients have
no Cantor derivatives, and P=exp(-2 beta)Pi is Lipschitz as well.

The relevant classical diffuse chain rule is stated explicitly in the
introduction of [Ambrosio, Crasta, De Cicco and De Philippis, *A
nonautonomous chain rule in W1,p and BV*](https://arxiv.org/pdf/1512.02839),
arXiv:1512.02839v1, page 1. Local compactness permits a C1 cutoff extension
of the constitutive maps. Only that ordinary diffuse formula is needed;
no stronger nonsmooth-coefficient chain rule is invoked.

## 2. Exact stress identity and signs

For the base metric, p_b=-r n_b and the on-branch mixed stress is

    T^a_b=H delta^a_b-k^a p_b.

At fixed auxiliary/metric variables, H_{p_a}=h n^a=k^a. The diffuse
product/chain rule therefore gives

    D_a^c T^a_b
      =D_b^c H-p_b D_a^c k^a-k^a D_a^c p_b
      =-p_b D_a^c k^a+k^a(D_b^c p_a-D_a^c p_b).

The minus sign in front of p_b div k is correct. Connection terms and
the transverse expansion terms are ordinary bounded functions, so they
have no singular contribution to the divergence equation. Likewise the
volume factor E is regular, and

    D_a^c(E k^a)=E D_a^c k^a.

The exact scalar equation has bounded Jacobian/source right side, hence
D_a^c k^a=0. Clock compatibility gives D_b^c p_a-D_a^c p_b=0.
Thus the Cantor part of stress divergence vanishes automatically once
these two identities hold. Unlike a finite jump, there is no nonlinear
chord mismatch left over: the diffuse chain rule is the differential
chain rule at the approximate state.

This does not make all Einstein equations redundant. It says only that
their stress-conservation consequence supplies no new algebraic
Cantor-divergence condition. The absolutely continuous equations,
geometry, auxiliary constraints and any global data remain substantive.

## 3. Acoustic measure equations without rank one

Use U=(m,b), m=exp(2 beta)h phi_t/r and b=phi_x. In the compact
positive-R subluminal neighborhood this is an invertible C1 change of
the clock-gradient state with regular coefficients. The bounded scalar
balance and compatibility yield

    D_t^c U+M D_x^c U=0,    M=D_U F,
    F=(K^x,-phi_t).

Derivatives of A and the metric contribute no Cantor measure. Let l_i
be the left eigenvectors and lambda_i the distinct acoustic speeds of M,
evaluated at the precise state. Multiplication of Radon measures by
these bounded Borel coefficients gives

    l_i D_t^c U+lambda_i l_i D_x^c U=0.

This family projection needs no rank-one theorem. By itself it does
not imply that only one family is active at each measure point.

## 4. Rank-one refinement, with its exact external input

The singular derivative of a vector BV map has rank-one polar almost
everywhere for its variation measure. This is [Alberti, *Rank one
property for derivatives of functions with bounded variation*](https://people.dm.unipi.it/alberti/ricerca/1989-91/rangouno-rdc.pdf),
Proceedings Royal Society Edinburgh 123A (1993), 239--274, Corollary 4.6;
Remark 4.7 states the local version. Checked the original author's PDF,
page 12 of the returned PDF. It applies to the two-component BV map U
on the two-dimensional spacetime domain. No PDE or entropy assumption
is part of that geometric theorem.

Set mu=|D^c U|. At mu-almost every nonzero Cantor point write the polar
as xi tensor nu, with xi a nonzero state vector and nu=(nu_t,nu_x) a
nonzero spacetime covector. The measure equation implies

    (nu_t I+nu_x M)xi=0.

One must have nu_x!=0. Therefore xi is an acoustic right eigenvector
and -nu_t/nu_x is its eigenvalue. Strict hyperbolicity chooses one
family at that point; the chosen family can vary across the measure.
In particular the polar covector is proportional to (-lambda_i,1).

This is an orientation/polarization statement. A Cantor measure is not
thereby shown to be concentrated on a rectifiable collection of smooth
characteristics. Nor does it provide a well-defined unique classical
flow for a merely BV acoustic speed. No such upgrade is used here.

## 5. Why genuine nonlinearity does not finish the argument

On the low-u neighborhood the earlier fixed-coefficient calculation
gives nonzero derivative of lambda_i in its right-eigenvector direction.
Together with the rank-one result, this links the singular variation of
the speed to the corresponding wave measure. It does not set that
measure to zero. The displayed principal identities are homogeneous
linear constraints on its polar and allow a nonzero characteristic
polar at every hyperbolic state.

To exclude Cantor evolution or establish a unique continuous weak
continuation, a further regularity/propagation theorem is needed: for
example a valid interaction/one-sided estimate or a renormalized
characteristic argument for this actual coupled balance with its
auxiliary source. None follows solely from the local value of the
genuine-nonlinearity coefficient. The source closure and admissibility
obligations identified in PF13 have not disappeared.

In particular, applying the classical differentiated Riccati equation
after breakdown would require products of singular derivative measures,
including a squared compression, that this BV formulation has not
defined. Conversely, inferring a unique characteristic flow from BV
speeds would need its own hypotheses; the spatial derivative of such
a speed may itself be a singular measure. The preceding prebreak
gradient blowup theorem therefore cannot be relabeled as a theorem
that every postbreak solution must acquire a jump.

No native Cantor solution has been constructed, and no nonuniqueness
example or general Cantor exclusion has been proved. The precise result
is that the diffuse chain rule removes the derivative-product ambiguity
for these linear Cantor identities, while energy/stress equality alone
adds no independent Cantor condition to eliminate the remaining route.

Source check provenance: primary PDFs above were opened and their exact
chain-rule/rank-one statements checked on 2026-11-06. No local full-text
cache or source hash is claimed. The external statements support only
the two specified BV facts, not a native evolution theorem.

Actual-file follow-up: read `pf15/DIFFUSE_SINGULAR_IDENTITY.md`, SHA256
`f77322dd6fce47ad5513457315439e54df27b3f834e766c2b730e4e2510ae25e`.
Its stress signs, canonical approximate-value convention, projected
measure equations and restricted conclusion agree with this audit.
Verdict for that exact file: proved as written. It deliberately uses
only family projections, so does not depend on the optional rank-one
refinement independently verified above.
