# Independent audit: native source variation with continuous BV clock gradient

**Verdict: proved under the candidate's stronger continuous-clock and
compact periodic inverse hypotheses.** Exterior differentiation in the
C1 clock chart supplies slice BV of the rates before they are used in
BV chain rules; there is no circular assumption of that regularity.
The result supplies a source-measure bound, not the missing absolute-value
transport estimate or a postbreak existence theorem.

Reviewed `pf17/SOURCE_VARIATION.md`, SHA256
`d63c85fbbe16e073db30078ada95977f8116bd1efb610e629310be2698b5c07d`,
and `pf17/GRADIENT_COUNTERTEST.md`, SHA256
`54e5491de90418d009ad53f822a14aedf61b88fe6f64f54bf1b4e9e05960c658`.
Independent delegated audit, 2026-11-06. Write E_beta=e beta to distinguish
it from the spacetime volume density. The rate v below is nP/r.

## 1. Derive spatial rate measures before multiplying them

Continuous p=dphi, strict timelikeness and r>=r_min make tau=phi a C1
clock coordinate with locally bounded inverse Jacobian. Frame coefficients
are continuous BV. Since metric first derivatives are continuous and
their weak derivatives are L1, B=n beta and E_beta=e beta are continuous
BV too. The exact decompositions are

    dA=u dphi+q_A e_flat,    q_A=W_P/r,
    dP=v dphi+q_P e_flat,    q_P=D-2P E_beta.

The q's and e_flat are known continuous BV coefficients. In a local
clock chart (tau,xi), write e_flat=L_tau d tau+L_xi d xi. Then

    A_tau=u+q_A L_tau,    A_xi=q_A L_xi,
    partial_xi u=partial_tau(q_A L_xi)
                    -partial_xi(q_A L_tau).

The right side is a Radon measure. This proves that the spatial
distributional derivative of the L-infinity rate u is a measure, hence
u has BV slices at almost every clock time. The same argument applies
to v with q_P. Partial-BV slicing supplies this conclusion; no prior
spatial derivative of u or v is assumed. The C1 clock change permits
the weak form/change-of-variables argument with continuous measure
coefficients. It does not require differentiating a rough u times dr.

One can now evaluate the exterior equations on the continuous frame.
Using d(e_flat)(n,e)=K gives the measure identities

    e u=W_PP v/r-W_P n r/r^3+W_P K/r^2,
    e v=D_r n r/r+(r/gamma)u-2E_beta v
          -2P n(E_beta)/r+(D-2P E_beta)K/r.

The first formula here uses clock-independent W. The controlled
clock-dependent case is recorded below. All products with singular
derivatives at this stage have continuous known coefficients.

## 2. Native scalar and Einstein substitutions

Set D_r=(A-2 gamma r)/gamma and J0=h+P W_P/r. For constant V,W in
the explicit clock argument, the diffuse scalar equation gives

    n r=-(hK+r^2 D_r u+W_P v+2B J0)/R.

The full Einstein equations, written as warped Hessian identities,
give

    n(E_beta)=-(e r/r)B-B E_beta,
    eB=(K-B)E_beta,
    e(E_beta)=KB+(B^2-3E_beta^2)/2-T_nn/(2M).

These also hold as measure identities: differentiating the continuous
BV frame contributes K or e r with continuous coefficients, while the
metric Hessians are L1 and are fixed by the native Einstein equations.
The matter mixed frame stress is zero. No undefined connection-times-
surface-stress product is needed in this regular metric class.

Substitution yields precisely the corrected PF08 coefficients:

    e u=a0 u+b0 v+f K+f0,
    e v=c0 u+(-a0-2E_beta)v+gtilde K+j e r+g0,

    a0=W_P D_r/(rR),
    b0=W_PP/r+W_P^2/(r^3 R),
    c0=r/gamma-r D_r^2/R=r(1-2 gamma D)/(gamma R),
    f=(W_P/r^2)(1+h/(rR)),
    gtilde=(D-2P E_beta)/r-D_r h/(rR),
    j=2PB/r^2,
    f0=2B W_P J0/(r^3 R),
    g0=2PB E_beta/r-2B D_r J0/(rR).

The gtilde correction and the positive j sign are essential and pass.
There is no remaining product of an arbitrary L-infinity rate with a
singular clock derivative. Rate terms multiply volume densities only.

## 3. Measure-forcing inverse and source chain rule

On each regular closed clock slice, multiply the rate vector by
exp(beta). The coefficient matrix becomes traceless, with off-diagonal
entries b0,c0 strictly positive and uniformly separated from zero.
Its bounded periodic inverse acts on finite measure forcing by variation
of constants. The inverse constant is uniform under the stated compact
coefficient, length and positivity bounds; no coefficient derivative
estimate is needed.

One can also see the bound by integrating the weighted product identity:
its homogeneous part is c0 u^2+b0 v^2. The forcing pairing is bounded
by the rate supremum times its measure norm. The first-order ODE bounds
that supremum by its L2 norm plus forcing variation, which closes the
estimate. Here continuous r,theta make the derivative forcing atomless;
the resulting slice rate representatives are continuous BV. Thus the
product identity has no unaccounted jump term. Ordinary measure-forcing
variation of constants gives the same conclusion directly.

Consequently

    ||u,v||infinity<=C(1+TV r+TV theta)<=C(1+Z),
    TV(u,v)<=C(1+Z).

Here Z is the sum of the total masses of the covariant gradient
measures |W_sigma|, not a claim about another derivative of W_sigma.
The starting L-infinity rates follow from the assumed Lipschitz A,P.
Their quantitative bound is now improved independently of that initial
rate bound, so this step is not circular.

The exact F_sigma is a C1 function of r,A,P,B and affine in u,v, with
bounded derivatives on the compact coefficient range (derivatives in
the other arguments grow at most linearly in |u|+|v|). Its slice chain
rule, using the rate equations and the Einstein identities, therefore
gives

    |D_ell F_sigma|<=C(1+||u,v||infinity)
                       (d ell+|D_ell r|+|K|).

The acceleration-source product is legitimate as well: the slice
F_sigma representative is continuous and bounded, so it multiplies
the e r/r measure canonically. The integrated signed source norm is
at most C(1+Z)^2. No temporal continuity of u,v is inferred.

For rolling potentials define Zpot=V_phi+W_phi. The scalar numerator
also contains Zpot. The corrections to the bounded terms are

    f0 -> f0+W_P Zpot/(r^3 R)+W_Pphi/r,
    g0 -> g0-D_r Zpot/(rR).

They and the required slice derivatives have the declared compact
bounds under the earlier controlled potential assumptions. This verifies
the actual file's distinction between its constant-clock coefficient
display and the bounded rolling-potential extension.

## 4. The sharper gradient countertest passes

For b=sign(x)sqrt(|x|) and z=(t-2sqrt(|x|))_+, let I indicate
0<|x|<t^2/4. Direct weak differentiation gives

    z_t=I,    W=z_x=-sign(x)I/sqrt(|x|),    bW=-I.

The potential is continuous at zero and at its support fronts, so its
first derivative has no delta. The singular-looking x derivative is
integrable. The exact integrals are ||W(t)||L1=2t and ||z(t)||L1=t^3/6.
Thus z_t+bz_x=0 and differentiation in x yields
W_t+partial_x(bW)=0 distributionally, with zero initial L1 traces but
nonzero later W. This countertest retains an exact integrable gradient
of a continuous W1,1 potential; it is stronger than a freely assigned
Dirac-pair transport example. The proposed local periodic patch does
not affect it before its support reaches the patch.

It refutes an automatic zero-source Kato estimate at this general
regularity. Its prescribed b is not a native acoustic velocity, so it
neither proves native nonuniqueness nor shows a native estimate is
impossible. In particular it does not satisfy the additional equations
whose use would be necessary to prove such an estimate.

## Remaining implication

Source variation is now controlled for an existing solution in this
continuous-clock subclass. Taking the absolute value of its signed
gradient transport still requires a native renormalization/interaction
argument. Neither this source bound nor the exterior cancellation
constructs a solution, propagates continuity/compactness, or yields a
uniform Z bound after breakdown. Continuity of spacetime p is stronger
than absence of BV jumps and is not supplied by the earlier jump
exclusion. The strengthened countertest identifies why gradient structure
and continuity alone do not bridge the remaining step.

## Final rolling-potential file and smoothing follow-up

Read the amended `SOURCE_VARIATION.md`, SHA256
`1d1c0b091d6a7ce7baba38147d5f1f29ba6bb77a73cbf0a7f5f44ef8222fd319`.
Its explicit rolling corrections agree with the derivation above,
including delta F_sigma=-sigma Zpot/(r c R). Positivity/C2 bounds for
V,a0 on the compact clock interval and cap separation suffice for the
needed slice state derivatives; e(phi)=0 introduces no additional
spatial clock derivative. The actual amended source statement passes.
The countertest hash remains the one recorded at the start of this note.

Also read `SMOOTHING_AND_UNIQUENESS.md`, SHA256
`19dda032bd44145b1196f837e0345f4945827ca10e443e2e6b085b644f4b92c0`.
For continuous BV X and C2 flux f on a common compact neighborhood,
the displayed first-derivative commutator identity is exact. The
nonnegative supported mollifier gives
|X_epsilon(x)-X(y)|<=omega(2 epsilon) on the kernel support, so its
L1 bound C omega(2 epsilon)TV(X) follows directly.

Differentiating once more gives two terms: D2f(X_epsilon) applied to
two copies of partial_x X_epsilon, and the original difference integrand
with partial_x eta_epsilon. The first is bounded using
||partial_x X_epsilon||infinity<=C omega(C epsilon)/epsilon and
||partial_x X_epsilon||L1<=TV(X); the second uses
||partial_x eta_epsilon||L1<=C/epsilon. This verifies the stated upper
bound C omega(C epsilon)TV(X)/epsilon. It is not a lower bound and does
not prove that the actual residual diverges.

For a fixed existing Lipschitz A,Pi, their mollified derivatives also
converge strongly locally in L1 while remaining bounded. Hence their
actual Jacobian source converges in L1; this extra fact, beyond the flux
commutator, handles source smoothing. If one mollifies U independently,
the reconstructed acoustic variables need only satisfy compatibility up
to the small balance residual; exact satisfaction at finite epsilon is
not asserted. Smoothing an existing weak solution remains distinct
from producing native solutions after breakdown or an evolution process.

Independently opened [Bressan--De Lellis, *A Remark on the Uniqueness of
Solutions to Hyperbolic Conservation Laws*](https://arxiv.org/pdf/2305.17203),
arXiv:2305.17203v1 (header May 26, 2023; internal date May 30, 2023).
Theorem 1.1 on PDF page 3, with (A1)--(A2) on pages 2--3, concerns the
autonomous strictly hyperbolic conservation law, its established
small-TV semigroup domain, L1-continuous weak solutions and Liu-admissible
approximate jumps. Continuous solutions have no jump condition to
check. The candidate's extraction is accurate.

This source does not supply the missing coupled nonautonomous/source
closure or native semigroup. In particular separate source-variation
bounds do not control the difference of temporal auxiliary rates for
two solutions. The exact theorem is verified; its application to the
native weak system remains unproved. No local full-text cache or source
hash is claimed. The smoothing/source note's restricted conclusion
therefore passes without an existence or uniqueness upgrade.

## Slice Cantor-source corollary

Read `pf17/CANTOR_SOURCE.md`, SHA256
`d87bb682edf126f54c824f20c95cfb9d2807fe62f37c26092ea1c7ec80cf669f`.
Its corollary passes. On the almost-everywhere clock slices already
established, K has Cantor part D^c theta; all zeroth-order terms are
densities. Therefore

    D^c u=f D^c theta,
    D^c v=gtilde D^c theta+j D^c r,
    D^c B=E_beta D^c theta.

A,P have no slice singular derivatives and the rate representatives
are continuous BV. The ordinary diffuse chain rule applied to the
displayed arguments of F_sigma gives exactly

    D^c F_sigma=(F_r+j F_v)D^c r
                +(E_beta F_B+f F_u+gtilde F_v)D^c theta.

The acceleration term subtracts (F_sigma/r)D^c r, with the sign in
the file. Curvature adds no singular term. Since
W_sigma^c=D^c theta+sigma D^c r/(r c), this is a bounded homogeneous
linear combination of the two slice Cantor gradients. Partial
derivatives here hold the other source arguments fixed; no dependence
through u,v is counted twice. Rolling potentials contribute to those
coefficients but e(phi)=0 leaves no extra clock-slice forcing measure.

The qualification in the file is necessary: this algebraic slice
identity is not a separately derived evolution equation for W_sigma^c.
Taking the Lebesgue/Cantor decomposition of a measure does not commute
with distributional divergence of its flux. Thus no zero-Cantor
propagation or Cantor-mass Gronwall estimate follows without the missing
native transport/renormalization result.
