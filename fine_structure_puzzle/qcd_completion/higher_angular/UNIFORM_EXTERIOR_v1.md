# Resummed charged exterior and finite angular cutoffs

This follows RAW_DERIVATION_v1.md. It strengthens the diagnosis of the
J~sqrt(x) regime, but does not claim a uniform theorem for the complete
regular-origin vector determinant.

## An exact growing basis for every charged l>=1

Write C=l(l+1). The uncoupled charged equation is

    -g''+(1-2/x+C/x^2)g=0.

Its large-x growing solution for every integer l>=1 is exactly

    g_l(x)=e^x f_l(x)/x,
    f_l(x)=sum_(n=0)^(l-1) (-1)^n/(2^n n! x^n)
                         product_(k=1)^n [C-k(k+1)].

The coefficient recurrence is

    a_(n+1)=[(n+1)(n+2)-C]a_n/[2(n+1)], a_0=1.

It terminates because a_l=0. For l1, f1=1. This is an exact exterior
fundamental solution, rather than a regular-origin solution of the BPS
operator. It may have zeros away from the large-x range controlled below;
one must not extend its logarithm through arbitrary turning regions.

## A uniform resummation with explicit inequality

For l>=2 set d=C-2>0 and s=d/(2x). In the coefficient of (-s)^n/n! define

    P_n=product_(k=1)^n [1-(k(k+1)-2)/d]  for 0<=n<l,
    P_n=0 for n>=l.

Every factor before termination lies in [0,1]. Product subtraction and the
vanishing factor at n=l give, for all n>=0,

    0<=1-P_n<=n(n-1)(n+4)/(3d).

For n>=l the right side is at least one, so this bound covers the
termination tail as well. Comparing with exp(-s), then using the exact
Poisson moment identity

    sum_(n>=0) s^n n(n-1)(n+4)/n! = e^s(s^3+6s^2),

proves the non-asymptotic inequality

    |f_l(x)-e^-s| <= e^s(s^3+6s^2)/(3d).

For every fixed B>0 and 0<=s<=B, define K_B=e^(2B)(B+6)/12. Then

    |f_l e^s-1| <= K_B d/x^2.

Since d<=2Bx, taking x>=4B K_B makes this relative error at most 1/2.
The growing factor is positive in this range and

    log f_l(x)=-d/(2x)+O_B(d/x^2).

The constants are explicit from the inequality above. The derivative is
controlled separately by absolute summation of the terminating series:

    |x f_l'(x)|<=s e^s,
    |f_l'/f_l|<=e^(2B)d/x^2

in the same range. The l1 case satisfies both statements exactly with d=0.

Thus J~sqrt(x) is a required resummation scale for the solution, but it
does **not** by itself invalidate the logarithm's leading -C/(2x) behavior.
The unresummed 1+a1/x approximation is inadequate when C/x is order one;
the exact polynomial tends instead to e^-s, uniformly on compact s ranges.

## The charged mixed wall is also controlled in this model

Use an orthonormal charged centrifugal basis for the eight vector modes.
Let P_N be the rank-two orthogonal normal projection. It need not commute
with the centrifugal matrix. The combined reduced Dirichlet/Robin map,
after a constant row isometry, acts on the diagonal growing matrix as

    [P_D+P_N(d/dx+1/x)] diag(g_l)
       =[I+P_N diag(f_l'/f_l)] diag(g_l).

If max |f_l'/f_l|<1/2, Sylvester's determinant identity reduces the extra
determinant to the two-dimensional normal range. Its logarithm is bounded
by four times max |f_l'/f_l|. This is the actual relative mixed wall in the
uncoupled charged exterior, rather than an all-Dirichlet replacement.

After canceling the two charged ghost factors against the four middle-C_J
vector factors, the growing-factor contribution to log Z per magnetic
component is exactly

    E_J(x)=-log f_(J-1)(x)-log f_(J+1)(x)
           -(1/2)log det[I+P_N diag(f_l'/f_l)].

For J<=N<=kappa sqrt(x), the preceding bounds apply with a fixed B depending
only on kappa, once x is sufficiently large. Uniformly in this range,

    E_J(x)=(C_J-1)/x+O_kappa(C_J/x^2).

Consequently the exact finite angular product of these exterior factors
satisfies

    sum_(J=2)^N (2J+1)E_J(x)
      = A_N/x + O_kappa(N^4/x^2),
    A_N=[(N+1)^4-3(N+1)^2]/2-2.

In particular, for N=floor(kappa sqrt(x)), this is A_N/x+O_kappa(1), with
A_N/x growing as kappa^4 x/2. This is an actual resummed finite-cutoff
statement for the specified exterior factors. It is stronger than merely
declaring the fixed-J solution series nonuniform.

## What still prevents an angular closure

The complete determinant includes the connection between smooth-origin
solutions and exterior bases, the neutral scattering matrix, and the exact
charged/neutral Schur complement. The fixed-J proof bounds all of these
sufficiently to determine its 1/x coefficient. It does not bound their
constants uniformly as J grows. A whole-space statement that there are no
J>=2 zero modes gives invertibility for each J; it supplies no quantitative
lower bound on the growing connection matrices. Therefore the exterior
sum just proved cannot be substituted for the full angular determinant.

For fixed finite N the full product's coefficient is rigorously A_N under
the accepted kernel/exterior premises. The limit N->infinity diverges. An
angular heat regulator produces the convergent coefficient diagnostic

    A(epsilon)=sum_(J>=2)(2J+1)(C_J-1)e^-epsilon C_J
              =(-d_epsilon-1)H(epsilon)+1-3e^-2epsilon,
    H(epsilon)=sum_(J>=0)(2J+1)e^-epsilon C_J.

Euler-Maclaurin, with the standard decaying Gaussian remainder, gives

    H(epsilon)=epsilon^-1+1/3+epsilon/15+4epsilon^2/315+...,
    A(epsilon)=epsilon^-2-epsilon^-1-12/5+O(epsilon).

The number -12/5 is the finite part of this **chosen angular coefficient
regulator**. It is not established as a coefficient of a UV-renormalized
full determinant, and it has no physical interpretation here. In
particular, a different finite angular subtraction changes that finite
part. No exchange of the x->infinity and epsilon->0 limits has been proved.

Local bulk/boundary heat terms belong to a joint regulator of the original
elliptic problem. The auxiliary BPS/unbroken comparison has different
asymptotic holonomy; it therefore requires physical matching in addition
to UV subtraction. Polynomial angular divergences, local boundary terms,
and a finite physical response cannot be identified merely from A_N or
A(epsilon). The static result also omits the nonzero circle Fourier modes.

## Next discriminating proof task

A useful next step is a quantitative, J-uniform regular-to-exterior
connection estimate. For large J one expects a centrifugal barrier to
control the inverse growing map, but this must be proved for the actual
coupled Hessian and mixed wall. Such an estimate could extend the Schur
bound to N~sqrt(x), then to a uniform J/x regime. Only after that estimate
and a common joint UV subtraction are supplied is a regulated full angular
sum a well-posed closure claim.
