# I14: exact discrete spectrum and the sharp confinement threshold

Base checkpoint: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
Original I14 commit: `34e5eafd8`.
Proof status: full elementary mathematical proof below; named algebraic,
sharp-uniform-bound, finite-positivity, and sine-mode claims additionally
Lean-certified. Completeness of the sine family and the finite-box minimum
are proved below, not represented as completed Lean declarations.

## Claim and conventions

Fix an integer N >= 2. The vector space consists of real vectors
(u_1,...,u_{N-1}), extended by u_0=u_N=0. Values outside the box do not enter
any form. Set

    U = sum(n=0,...,N-1) u_n^2,
    D = sum(n=0,...,N-1) (u_{n+1}-u_n)^2,
    A = sum(n=0,...,N-1) (u_{n+1}-3u_n/2)^2,
    E = A - kappa2 U + mu2 sum(n=0,...,N-1) q_n u_n^2.

The parameters named kappa2 and mu2 are arbitrary real scalars in the formal
statements. Interpreting them as squares is an additional restriction. For
constant q_n=q0 define b=1/4-kappa2+mu2*q0. The claims concern the matrix H
in E(u)=u^T H u relative to norm U, not twice that matrix (the ordinary
coordinate Hessian of E). Multiplying an energy by 1/2 changes that Hessian
convention but does not alter any sign conclusion.

## Exact finite-box theorem

For constant q the eigenvalues, all simple, are

    lambda_j = 6 sin^2(j*pi/(2N)) + b,  j=1,...,N-1.

A corresponding eigenvector is v_j(n)=sin(j*pi*n/N). Consequently

    min(nonzero u) E(u)/U(u) = 6 sin^2(pi/(2N)) + b.

The form on this particular box is nonnegative if and only if

    kappa2 <= 1/4 + mu2*q0 + 6 sin^2(pi/(2N));

it is positive definite if and only if the inequality is strict. Equality
has a one-dimensional kernel spanned by v_1. A negative lowest eigenvalue
makes the unrestricted homogeneous quadratic form unbounded below under
amplitude scaling; the unit-norm Rayleigh quotient remains bounded below.
These are different uses of “unbounded below.”

### Proof

1. Telescoping gives

       sum (u_{n+1}-u_n)u_n = -D/2.

   Expanding the original squares therefore gives A=(3/2)D+U/4 and
   E=(3/2)D+bU. This identity is the existing Lean `hardy_identity` and the
   new `constant_confinement_identity`.

2. D has matrix L with diagonal 2 and neighboring entries -1. This follows
   directly by expanding the two differences touching each interior site.
   Hence H=(3/2)L+bI has diagonal 3+b and neighboring entries -3/2.
   Discrete summation by parts is additionally certified as
   `dirichlet_green_identity`.

3. For theta_j=j*pi/N, the identity

       sin((n+1)theta_j)+sin((n-1)theta_j)
         = 2 cos(theta_j) sin(n theta_j)

   shows Lv_j=(2-2cos(theta_j))v_j=4sin^2(theta_j/2)v_j. The endpoint
   values vanish. For 1<=j<N, v_j(1)>0, so these are nonzero vectors.
   The recurrence, boundary values, positive norm, and exact energy identity
   are Lean `sine_mode_recurrence`, `sine_mode_left`, `sine_mode_right`,
   `sine_mode_norm_pos`, and `sine_mode_energy`.

4. The numbers theta_j/2 lie strictly between 0 and pi/2. Since sin is
   strictly increasing and positive there, the eigenvalues are pairwise
   distinct and increasing. Eigenvectors of a real symmetric matrix at
   distinct eigenvalues are orthogonal: if Hv=lambda v and Hw=nu w, then
   lambda<v,w>=<Hv,w>=<v,Hw>=nu<v,w>. Thus our N-1 nonzero vectors are
   linearly independent in an (N-1)-dimensional space and form a basis.
   This proves completeness without guessing missing spectral modes.

5. Expanding u=sum c_j v_j in this orthogonal basis gives

       E(u)/U(u) = [sum lambda_j c_j^2 ||v_j||^2]
                    / [sum c_j^2 ||v_j||^2].

   It is a weighted mean of the eigenvalues, attaining its minimum exactly
   on the lowest eigenspace. This proves the finite-box sign criteria.

N=0 and N=1 have no nonzero interior modes. All-box formal statements include
these harmless degenerate boxes; finite-box eigenvalue statements exclude them.

## Sharp large-box theorem and exact quantifiers

Since sin(pi/(2N)) -> 0, the infimum over all N>=2 and nonzero box modes is
exactly b. No finite-box vector attains b. The same sharpness can be proved
without trigonometric limits: the slab u_n=1 for 1<=n<N, zero at both ends,
has U=N-1 and D=2, hence

    E/U = b + 3/(N-1).

The following statements are Lean-certified, without a limiting theorem or
numerical assumption:

- `constant_uniform_floor_iff`: gamma*U <= E for every finite Dirichlet box
  and every mode if and only if gamma <= b.
- `constant_all_boxes_nonneg_iff`: E >= 0 for every finite box and every mode
  if and only if kappa2 <= 1/4+mu2*q0.
- `constant_floor_sharp`: for each eps>0 an explicit nonzero slab has
  E < (b+eps)U. Choose an integer N>1+3/eps.
- `confined_beyond_wall`: if kappa2>1/4+mu2*q0, some finite box contains a
  nonzero negative mode. The slab criterion is N>1+3/(-b).
- `confined_critical_gap_closes`: at kappa2=1/4+mu2*q0, for each eps>0 some
  nonzero mode satisfies 0<=E<eps*U.
- `kinetic_pos_of_norm_pos` and `confined_critical_finite_pos`: every nonzero
  finite-box mode has D>0 and hence E>0 at b=0.

Thus the trichotomy is: a positive gap uniform in all box sizes when b>0;
positive energy on every fixed box but no positive uniform gap when b=0;
negative modes on sufficiently large boxes when b<0. The finite-box critical
value is higher than the uniform critical value. Slabs prove sharpness but
are not the finite-box minimizing eigenvectors.

For no confinement (mu2*q0=0), the uniform threshold is kappa2=1/4. If one
also assumes kappa>=0 and kappa2=kappa^2, this is kappa=1/2. Without that
sign convention the condition is |kappa|<=1/2. Stability alone permits the
entire interval; a uniquely selected value requires an independently
justified saturation/marginality premise.

With constant positive confinement, the uniform wall moves to
kappa2=1/4+mu2*q0. The fully certified counterexample
`confined_counterexample_to_universal_wall` has kappa2=mu2=q0=1:

    E = (3/2)D + U/4 >= U/4,

although kappa=1>1/2 under the positive-square interpretation.

## Variable confinement

When mu2>=0 and q_n>=q0, the existing `vacuum_gap` proves E>=bU for every
box. It does not require kappa2<=1/4. Positivity of b is sufficient for a
uniform gap, but q>=q0 alone does not make the bound sharp for a fixed q.
For example, replacing q0 by the strictly larger constant q0+1 changes the
actual spectral bottom by mu2. Conversely, the lower-bound class q>=q0
contains q=q0, so b is best possible uniformly over that entire class.

## Self-review and verification

The separate matrix check constructs the original rectangular operator
B(u)_n=u_{n+1}-3u_n/2, forms B^T B plus the scalar shift, and compares its
computed eigenvalues and eigenvectors against the formula. It covers N in
{2,3,4,8,31,128} and five parameter triples, including negative formal
parameters. This checks indexing and constants independently of the
tridiagonal proof. It is finite floating evidence only.

Self-audit passed the coefficient, boundary, N=2 benchmark (A/U=13/4),
completeness, norm, finite-versus-uniform, confinement sign, and amplitude
versus Rayleigh-quotient obligations. Full coupled physical stability is
outside this theorem; see SOURCE_BRIDGE.md. The result is classical finite
Dirichlet diagonalization applied to the exact I14 form, not a claimed new
spectral mechanism.
