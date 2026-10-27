# FSP-005 angular connection: actual coercivity and boundary normalization

Checkpoint AC-005-001; parent FSP-004; base Git revision
`9516ee01c79f35c04b7556050669ba77b0c98b99`. Author: angular-connection
subagent. Writes are confined to this directory. Prior scientific files are
inputs, not modified. This is a hand derivation; symbolic checks are separate.

## 1. Operator, domain, and quantified target

Work in dimensionless radius r=m_W|x| with fixed asymptotic m_W and fixed
small circle. The background and covariant derivative are exactly

    K=r/sinh r, h=coth r-1/r,
    A_i=(1-K)(e_i cross n)/r, Phi=h n,
    D_i=partial_i+ad A_i, D_4=ad Phi,
    H_mu,nu=-D_lambda D_lambda delta_mu,nu-2 ad F_mu,nu.

Use the smooth Cartesian origin and u=r a. On a total-grand-spin-J sector
per magnetic component, H=-d_r^2+V_J on the angular Hilbert space E_J.
For J>=2, dim E_J=12. All norms below use angular orthonormal coordinates.
The relative wall is P_D u=0, P_N(u'+u/R)=0, where P_N projects onto the
spatial normal trace and P_D=I-P_N; rank P_N=3. The ghost wall is not used
to replace this vector wall.

The immediate target is a J-uniform estimate of the regular solution's
logarithmic derivative and of its actual mixed boundary map. It is not an
absolute lower bound on arbitrarily normalized Frobenius connection entries.
The result below also gives a uniformly bounded determinant connection after
normalizing regular values at the fixed core radius r=2, and an explicit
error for comparison with the exact diagonal Coulomb operator.

## 2. Exact angular expression from the Cartesian Hessian

Let L=-i n cross partial_Omega and T_a=i ad(e_a). Thus T is spin one,
T^2=2, and T_n^2=Q=I-n tensor n is the charged projector. Define G=L+T.
The spatial fluctuation index has spin S=1, and the fourth component S=0;
the conserved grand spin is J=G+S. These are Cartesian component operators,
not guessed copies of a scalar radial operator.

Since r A_i=(1-K)(e_i cross n), direct evaluation of -i n cross D gives

    Lambda=L+(1-K)(T-n T_n).

Here L dot(n T_n)=(n T_n) dot L=0 and
(T-n T_n)^2=2-Q. Therefore the angular covariant Laplacian is exactly

    A(K)=L^2+2(1-K)L dot T+(1-K)^2(2-Q)
        =K L^2+(1-K)G^2-2K(1-K)-(1-K)^2 Q.                 (2.1)

To specify the curvature term, put b=h'=(1-K^2)/r^2 and c=Kh/r.
The BPS field is anti-self-dual in the preceding input convention:
F_ij=-epsilon_ijk F_k4, F_i4=D_i Phi. The constant four-vector matrices

    (I_a)_ij=epsilon_ija, (I_a)_i4=-delta_ia,
    (I_a)_4j=delta_aj, (I_a)_44=0, sigma_a=-i I_a

obey the Pauli algebra. Since F_mu,nu=-I_a,mu,nu (D_a Phi), the actual
curvature term is

    E(r)=2 sum_a sigma_a tensor T_{D_a Phi}
        =2c sigma dot T+2(b-c) sigma_n T_n.                (2.2)

The spectator spin-half gives the usual multiplicity two. This sign agrees
with the earlier charged expression -2q sigma_n/r^2 because the monopole
charge in that convention is q=-T_n. In particular

    V_J(r)=A(K)/r^2+h^2 Q+E(r)                            (2.3)

is an exact angular-operator expression for the actual Hessian at every r.
It does not require serializing a separate 12-by-12 matrix for each J.

## 3. An elementary profile inequality and exact curvature bounds

For all r>0, 0<K<1, 0<h<1 and 0<c<=b<=1/r^2. Only c<=b needs some care.
Set t=r/2. Direct simplification yields

    b-c=[sinh(t)^2+t tanh(t)-2t^2]/[4t^2 sinh(t)^2].       (3.1)

The numerator is nonnegative: the nonnegative Taylor series gives
sinh(t)^2>=t^2+t^4/3, while tanh(t)>=t-t^3/3. For the latter inequality,
differentiate tanh(t)-t+t^3/3: its derivative is t^2-tanh(t)^2>=0,
using 0<=tanh(t)<=t. Also r^2 b=1-K^2<=1. Finally h<1 follows from
exp(2r)>1+2r. No external spectral or index theorem is a leaf here.

At n=e_3, the active 2 tensor 3 curvature matrix is

    2[c(sigma_1 T_1+sigma_2 T_2)+b sigma_3 T_3].

Its eigenvalues, each twice in the six-dimensional active space, are

    2b, -b+sqrt(b^2+8c^2), -b-sqrt(b^2+8c^2).

Consequently, using c<=b,

    -4b I <= E(r) <= 2b I.                               (3.2)

The extra spectator copy does not change these norm bounds.

## 4. Uniform large-J centrifugal coercivity

Addition of the three actual angular momenta gives, for J>=2,

    (J-2)(J-1) I <= L^2 <= (J+2)(J+3) I,
    (J-1)J I <= G^2 <= (J+1)(J+2) I.

Insert these bounds into (2.1), with 0<=Q<=I, then use (3.2):

    V_J >= { (J-1)(J-2K)-5(1-K^2) }/r^2 I+h^2 Q.       (4.1)

For J>=6, subtraction of (J-1)(J-2) from the brace factors as

    (1-K)[2(J-1)-5(1+K)] >= 0.

The upper bound uses A(K)<=K L^2+(1-K)G^2 and E<=2/r^2. Thus

    a_J/r^2 I+h^2 Q <= V_J <= B_J/r^2 I+Q,
    a_J=(J-1)(J-2), B_J=(J+2)(J+3)+2,  J>=6.            (4.2)

There are also positive estimates for J=3,4,5: replace a_J by
1/5,26/5,59/5 respectively, by minimizing the quadratic in K in (4.1).
The crude bound does not resolve J=2. No conclusion about that finite
sector is inferred from the large-J inequality.

In the reduced form domain, (4.2) proves the quantitative statement

    q_J[u] >= integral (|u'|^2+a_J |u|^2/r^2+h^2|Q u|^2) dr.

At the relative wall its form has the additional nonnegative term
|P_N u(R)|^2/R. This is a coercive estimate, rather than a kernel count.

## 5. Regular Dirichlet-to-Neumann map, with explicit constants

Let Y_J be any regular-origin fundamental matrix. It is invertible at
every R>0 for J>=6: otherwise a nonzero regular solution with zero value
at R would have zero boundary energy and strictly positive integral form.
The conserved Wronskian of two regular solutions is zero at the origin,
so P_J=Y'_J Y_J^{-1} is Hermitian and independent of column normalization.
It is the variational Dirichlet-to-Neumann map:

    v^*P_J(R)v = min_{u(R)=v, regular form at 0} q_J[u].   (5.1)

All variational assertions can be obtained by integrating the ODE and
completing the quadratic form around its solution. Powers used as trial
functions belong to the form closure; cutting them off near zero proves
this without imposing an extra Cartesian origin extension.

Write p=J-1 and beta=(1+sqrt(4J^2+20J+33))/2, so beta(beta-1)=B_J.
Completion of the square with u'-p u/r in (4.2) gives

    P_J(R) >= p/R I.                                    (5.2)

For the upper bound use comparison potential B_J/r^2+Q. A neutral trial
is (r/R)^beta v_N. A charged trial is (r/R)^beta exp(r-R) v_C. For the
charged trial, w''/w=B_J/r^2+1+2beta/r, hence integration by parts gives
an energy no larger than 1+beta/R. This proves

    P_J(R) <= beta/R I+Q.                               (5.3)

A charge-sensitive lower bound follows by splitting the form in half:

    q_J >= (1/2) integral (|u'|^2+a_J |u|^2/r^2)
             +(1/2) integral (|u'|^2+h^2|Q u|^2).

On [2,R], h>=1/2. Dropping the inner interval and minimizing the charged
second integral with free value at 2 gives (1/2)tanh((R-2)/2)|v_C|^2.
Therefore for R>=4,

    P_J(R) >= (J-1)/(2R) I+c_* Q,
    c_*=(1/4)tanh(1).                                   (5.4)

Define the natural boundary scale Z_J(R)=J/R I+Q. Since beta<=J+4 and
J>=6, (5.3)-(5.4) give the uniform matrix comparison

    c_* Z_J(R) <= P_J(R) <= (5/3) Z_J(R),
    J>=6, R>=4.                                        (5.5)

For the lower coefficient of J/R, (J-1)/(2J)>=5/12>c_*. The charged
scale is 1+J/R, while the neutral scale is J/R. In particular an unscaled
positive constant lower bound on the neutral DN block is impossible as
R tends to infinity at fixed J; its natural scale must be retained.

## 6. The actual relative wall and neutral Schur complement

P_N and Q commute pointwise, hence also in E_J. Their ranks are:
charged: dim 8, normal rank 2; neutral: dim 4, normal rank 1. The neutral
four-vector has three spatial vector harmonics and one A4 harmonic. The
normal trace is an adjoint scalar with one neutral and two charged modes.

Normalize input values by w=Z^(1/2)u(R), Dirichlet output by Z^(1/2),
and Robin output by Z^(-1/2). The actual regular boundary map becomes

    Btilde=P_D+P_N(Ptilde+R^(-1)Z^(-1)),
    Ptilde=Z^(-1/2)P_J Z^(-1/2).                         (6.1)

In the D,N splitting it is [[I,0],[A,B_N]], where

    ||A||<=5/3,
    c_* I <= B_N <= (11/6) I.                           (6.2)

The extra upper 1/6 uses R^(-1)Z^(-1)<=1/J. Consequently

    ||Btilde^(-1)|| <= 8/(3c_*),
    c_*^3 <= det Btilde <= (11/6)^3.                    (6.3)

These are estimates on the actual nine-Dirichlet/three-Robin wall map
in its declared boundary scale, rather than a scalar wall replacement.

Split the three-dimensional SPD matrix B_N into charged normal rank two
and neutral normal rank one. After eliminating charged normal values, its
neutral Schur complement S_N obeys

    c_* <= S_N <= 11/6.                                (6.4)

Proof: its quadratic form is the minimum over charged normal values of
the B_N form. The lower bound follows from B_N>=c_*I; the upper follows
by setting those values to zero. Eliminating all charged boundary data
in Btilde leaves the neutral three-Dirichlet/one-Robin map with this
Robin coefficient. Its remaining off-diagonal entries have a uniform
bound from (6.2) and B_N,cc^(-1)<=c_*^(-1). This gives a quantitative
neutral Schur bound even when J/R tends to zero, provided the neutral
boundary normalization J/R is used.

## 7. A normalized Coulomb connection and quantitative core forgetting

Let V_0,J be the exact far operator obtained by K=0, h=1-1/r,
b=1/r^2, c=0 in (2.3). It preserves Q. Its charged and neutral
centrifugal list is l(l+1), l=J-1,J,J,J+1 in each charge and neutral
copy, as derived in the frozen higher-angular input. Charged channels
are -d^2+1-2/r+l(l+1)/r^2; neutral channels are Euler operators.

Select the Friedrichs/regular branch of this comparison at its origin.
This comparison is a mathematical normalization, not a different physical
vacuum subtraction. Its P_0,J is positive. Direct potential comparison

    1-2/r+l(l+1)/r^2 >= l(l-1)/r^2,

since r^2-2r+2l>0, gives

    (J-1)/r I <= P_0,J(r) <= (J+2)/r I+Q.               (7.1)

It is essential here to compare to this exact regular Coulomb DN map,
not to continue a pure growing polynomial through its possible zeros.

The difference E_J=V_J-V_0,J has a completely explicit bound for r>=2.
From (2.1), ||L dot T||<=J+3 and ||2-Q||<=2,

    ||A(K)-A(0)|| <= 2K(J+5).

From (2.2), ||Ecurv-Ecurv,0||<=4Kh/r+2K^2/r^2. Also
|h^2-(1-1/r)^2|<=6exp(-2r), K<=3r exp(-r). Since exp(2)>7,

    ||E_J(r)|| <= e_J(r):=[6(J+5)/r+16] exp(-r).          (7.2)

The above deliberately rounded constants contain all profile corrections,
including the charged-to-neutral mixing. No exponential coefficient has
been discarded after multiplying by a growing solution.

Set W=P_J-P_0,J. Riccati subtraction gives exactly

    W'=E_J-P_J W-W P_0,J.

Both homogeneous factors contract by (s/R)^(J-1), using (5.2),(7.1).
At r=2, positivity and the two upper bounds imply
||W(2)||<=Btilde_J=(J+6)/2. Thus for J>=6,R>=2, with n_J=2J-2,

    ||W(R)|| <= epsilon_J(R)
      :=Btilde_J(2/R)^n_J
        + integral_2^R (s/R)^n_J e_J(s) ds.              (7.3)

This is a global regular-to-exterior comparison in logarithmic-derivative
coordinates. It does not need the whole-space index theorem. In particular
the exact operator, not a kernel-count surrogate, supplies its constants.

For R>=4, splitting the integral at R/2 gives the convenient bound

    epsilon_J(R) <= Btilde_J(2/R)^n_J
      +(3J+31) exp(-2) 2^(-n_J)
      +[12(J+5)/R+16] exp(-R/2).                         (7.4)

Hence eta_J(R):=R epsilon_J(R)/J tends uniformly to zero on
J>=kappa sqrt(R), for each fixed kappa>0. More explicitly it is at most

    R (J+6)/(2J) (2/R)^(2J-2)
      +R(3+31/J)exp(-2)2^(-2J+2)
      +[12(1+5/J)+16R/J]exp(-R/2).                      (7.5)

The same holds for J/R in any positive compact interval, and uniformly
for all larger J as well. This controls the normalized actual DN map
relative to the Coulomb DN map; ||Z^(-1/2)W Z^(-1/2)||<=eta_J.

## 8. Determinant connection with no factorial normalization

Normalize both regular matrices by Y_J(2)=Y_0,J(2)=I. This is a fixed-core
value normalization; it is explicitly different from fixing all Frobenius
leading coefficients to one. Set

    F_J(R)=det[P_D Y_J+P_N(Y'_J+Y_J/R)],

using a common orthonormal wall row basis and ordering. Factoring Y_J,

    F_J=det(Y_J) det_{ran P_N}[P_N(P_J+I/R)P_N].          (8.1)

The same formula holds for F_0,J. Because d log det Y_J/dR=tr P_J,
the integrated version of (7.3) yields, for R>=2,

    T_J(R):=integral_R^infinity ||W(t)||dt
      <= R epsilon_J(R)/(2J-3)
        +[6(J+5)+16(R+1)]exp(-R)/(2J-3).                (8.2)

This follows by interchanging nonnegative integrals; it does not sum
angular sectors. Thus c_J=integral_2^infinity tr W(t)dt exists. From (8.2)
at R=2, exp(-2)<1/7 and J>=6,

    |c_J| <= 12 [J+6+(6J+78)exp(-2)]/(2J-3) < 38.       (8.3)

The bound decreases as J increases after the displayed replacement by
1/7. In particular exp(-38)<lim F_J/F_0,J<exp(38), uniformly J>=6,
in the declared fixed-core value normalization. This is a determinant
connection bound, not a bound on every singular value of a Frobenius
connection matrix, and not a physical normalization of the path integral.

If eta_J(R)<=1/2, the normal DN block for the comparison is >=J/R,
so the log of the normal determinant quotient has magnitude at most
6 eta_J. Therefore the complete actual relative-wall determinant obeys

    |log(F_J(R)/F_0,J(R))-c_J|
      <=12 T_J(R)+6 eta_J(R).                           (8.4)

The constants in (8.3)-(8.4) have no hidden J-dependent factorials.
For J~sqrt(R), this remainder decays faster than any inverse power of R.
For kappa sqrt(R)<=J<=Lambda R, the degeneracy-weighted sum of these
remainders also tends to zero for any fixed positive kappa,Lambda,
because the number and degeneracies are polynomial while (7.5) is
exponentially small. This is a finite expanding angular band, not an
unregulated infinite angular product.

## 9. What this closes and what it does not

The large-J quantitative DN/mixed-wall/neutral-Schur obligation is proved
in the scale Z=J/R+Q, and the actual core-to-Coulomb determinant connection
has the fixed-core normalization and uniform bound (8.3). In particular
the earlier qualitative no-kernel proof is not the input that supplies
these bounds. The origin-to-r=2 Frobenius normalization factors remain
explicit if the original canonical determinant is wanted.

These estimates do not supply a trace-class infinite-J comparison after
UV removal. The late-interval term in (7.5) is not summable with all
degeneracies over J to infinity. The missing next step is a large-J symbol/
heat subtraction in the J/R regime for the full same-regulator gauge/ghost
complex, retaining its local wall terms and its origin normalization.
No fixed-J inverse-radius coefficients have been assigned a physical
finite part. Nonzero Fourier modes, physical same-holonomy vacuum matching,
and the charge-normalized QCD electromagnetic stress are also outside this
theorem. No alpha prediction follows.

The potentially tempting stronger assertion that an unscaled neutral
DN/Schur block has a radius-independent positive lower bound is refuted
already by the upper bound P_Neutral P_J P_Neutral<=beta/R: for fixed
J>=6 it tends to zero. The normalized assertion (5.5)-(6.4) is the
appropriate surviving statement.
