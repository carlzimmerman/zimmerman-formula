# General static J>=2: raw derivation v1

This lane owns only `higher_angular/`. Its scope is the fixed-small-circle,
static, pure-SU(2), charge-one BPS saddle, compared with the auxiliary unbroken
K=1,h=0 reference. No measured alpha, fitted coefficient, electromagnetic
coupling identification, or physical QCD matching enters.

Independence receipt: I read the angular ghost report and kernel/rank raw
derivation, then the full J1 DERIVATION.md to obtain its exact operator and wall
model. That file also contained the J1 asymptotic coefficient, so this derivation
is **not coefficient-blind**. I derived the generic-J Pauli/angular calculation
below before receiving the coordinator's generic formula. The coordinator then
reported independent agreement, including the reference and wall powers. I have
not read the coordinator's separate candidate file. Generic formulas below must
therefore not be described as an entirely blind replication.

## Quaternion angular calculation, rather than scalar-copy counting

At infinity split the adjoint bundle into charge q=+1,-1 and the neutral line.
For a fixed charge let L denote the conserved monopole angular momentum,

    L=-i r cross D-q n,  L dot n=-q, [L_i,n_j]=i epsilon_ijk n_k.

The covariant scalar angular Laplacian is L^2-q^2. The h^2 term equals
1-2/r+1/r^2, so q^2=1 cancels that monopole subtraction.

The real four-vector is the tensor product of two spin-1/2 factors. One
quaternion factor is acted on by curvature, while the other is a spectator.
In the anti-self-dual convention of the supplied Cartesian Hessian define

    (I_a)_ij=epsilon_ija, (I_a)_i4=-delta_ia,
    (I_a)_4j=delta_aj, (I_a)_44=0, sigma_a=-i I_a.

Then I_1 I_2=-I_3, so sigma obey the usual Pauli algebra. The actual curvature
term -2 ad F, restricted to charge q, is -2q sigma dot n/r^2. Consequently the
charged far operator is exactly

    -d_r^2+1-2/r+A/r^2,  A=L^2-2q w,  w=sigma dot n.

This supplies the needed vector-specific curvature term.

Set K=L+sigma/2, k(k+1)=K^2, lambda=k+1/2, and kappa=sigma dot L+1.
Angular momentum and the monopole identities give

    kappa^2=lambda^2, {kappa,w}=-2q, w^2=1,
    L^2=lambda^2-kappa,
    A=lambda^2-(kappa+2q w), (kappa+2q w)^2=lambda^2.

Thus the two active-spinor centrifugal eigenvalues are
lambda(lambda-1),lambda(lambda+1). The full grand spin J is obtained by
coupling k to the spectator spin 1/2, so k=J-1/2,J+1/2. For J>=2 each
active-spinor space has both branches. Per charge the four eigenvalues are

    C_(J-1), C_J, C_J, C_(J+1),  C_j=j(j+1).

At J1 the lowest active k=1/2 space has only monopole L=1, kappa=-1, w=q.
Its only A eigenvalue is zero; the missing branch is C1=2. This recovers the
exceptional three charged channels per charge at J1. This exception matters
for the linear and logarithmic radius terms, although its missing a1 is zero.

The neutral line has no curvature or monopole charge. The physical spatial
vector has orbital l=J-1,J,J+1 and A4 has l=J. Its four centrifugal values
are also C_(J-1),C_J,C_J,C_(J+1).

## Origin, wall, and growing coefficients

For J>=2, coupling spatial spin1 and adjoint isospin1 first gives k=0,1,2.
The spatial orbital multiplicities are l=J-2:1, J-1:2, J:3, J+1:2, J+2:1.
A4 adds l=J-1,J,J+1 once. The full 12-channel origin multiplicities are
therefore (1,3,4,3,1), with smooth reduced branches r^(l+1).

The actual relative wall has nine Dirichlet and three normal Robin data,
where the reduced normal condition is u'+u/r. The normal projection preserves
charge. It has rank two in the eight-dimensional charged space and rank one
in the four-dimensional neutral space. It is not a separate scalar wall in
the centrifugal eigenbasis.

For a charged growing solution of centrifugal value c, substitution gives

    g_c=e^r/r [1+a1(c)/r+a2(c)/r^2+...],
    a1=(2-c)/2, a2=(6-c)a1/4.

For the Robin functional, g_c'+g_c/r has exactly the same coefficient a1.
After a constant charge-adapted row change, the leading charged mixed wall
matrix is therefore the identity on value vectors. Its determinant has
1/r coefficient sum a1. For eight channels,

    sum c=2[C_(J-1)+2C_J+C_(J+1)]=8C_J+4,
    sum a1=6-4C_J.

The charged-induced neutral tails must not be discarded simply because the
off-diagonal potential is exponential. The actual Schur argument is needed.
The same exterior construction as the J1 remainder note applies for each
fixed J: the charged-growing block A is e^r/r times an invertible constant
plus its inverse-power series; the charged trace B of growing-free columns
is exponential times a polynomial/logarithm; their neutral trace C is at
most polynomial/logarithmic. Hence C A^-1 B is exponentially small relative
to the neutral polynomial wall determinant. Constants in this statement may
depend on J; it is not yet a uniform angular estimate.

All neutral decays are square-integrable for J>=2 because l>=J-1>=1.
The accepted whole-space kernel proof in reviews/kernel_rank has only phase
J0 and translations J1. Thus the regular-origin Lagrangian intersects the
no-growing infinity Lagrangian trivially at J>=2. The 12x12 growing map is
invertible. Its charged submap has rank eight and the charged-growing-free
regular space has four independent neutral growing coefficients. This is
the rank assertion needed by the Schur factorization.

For the neutral physical R/E basis, the free orbital eigenvectors are

    e_-=(sqrt(J),sqrt(J+1))/sqrt(2J+1), l=J-1,
    e_+=(-sqrt(J+1),sqrt(J))/sqrt(2J+1), l=J+1.

The row pair consisting of E Dirichlet and R Robin gives, after factoring
the powers r^J,r^(J+2) and the Robin row r^-1, the constant determinant

    -(J+1)(2J+3)/(2J+1) != 0.

The magnetic spatial mode and A4 each add r^(J+1). The full neutral wall
power is r^(4J+3). A neutral decaying admixture in row orbital l_a and column
growing orbital l_b gives relative order r^-(l_a+l_b+1), at worst
r^-(2J-1). Thus neutral scattering starts at order r^-3 or later and cannot
alter the 1/r coefficient. This argument also bounds the inverse neutral
wall matrix polynomially at every fixed J.

The unbroken reference has total origin power 12(J+1); the three Robin
rows lower its boundary determinant power by three. Its exact power is
therefore r^(12J+9), with nonzero constant from the positive free relative
realization. No radius-dependent reference correction occurs.

## Fixed-J formulas

For every fixed integer J>=2, subject to the stated whole-space kernel proof
and fixed-J exterior construction,

    log D_vec,J = 8x-(8J+14)log x+c_vec,J
                  +(6-4C_J)/x+O_J(x^-2).

The ghost has two charged channels of centrifugal C_J and one neutral
channel. Its smooth reference origin power is 3J+3; its BPS boundary power
is J-1. Positivity excludes a regular no-growing ghost zero mode. Therefore

    log D_gh,J = 2x-(2J+4)log x+c_gh,J
                 +(2-C_J)/x+O_J(x^-2).

The actual longitudinal identity H P=P M, with Dirichlet ghost and relative
vector data, pairs the longitudinal spectrum including all finite positive
eigenvalues. The full unprimed Gaussian may be computed as det M/det H^1/2;
one must not subtract another scalar determinant after using that formula.

Including 2J+1 magnetic components,

    log Z_J=(2J+1)[-2x+(2J+3)log x+c_J
                         +(C_J-1)/x+O_J(x^-2)].

This is a fixed-J comparison coefficient, not a physical QCD coefficient.

## Finite angular cutoffs and failure of termwise infinity

For every fixed finite N>=2, the actual finite product over J=2,...,N has
inverse-radius coefficient

    A_N=sum_(J=2)^N (2J+1)(J(J+1)-1)
       =[(N+1)^4-3(N+1)^2]/2-2.

It diverges quartically. The charged a1 scales as J^2, so the displayed
fixed-J series already fails to be a small-correction series at J~sqrt(x),
well before the centrifugal/mass transition J~x. A fixed-J O_J(x^-2)
remainder supplies no uniform summation theorem. A_N cannot be assigned a
physical finite part by zeta regularization.

An angular heat regulator gives a useful exact diagnostic, not an exchanged
limit proof. If H(epsilon)=sum_(J>=0)(2J+1)e^-epsilon C_J, then the regulated
sum of the displayed coefficients is

    A(epsilon)=(-d_epsilon-1)H(epsilon)+1-3e^-2epsilon.

For every epsilon>0 this coefficient sum converges. Its removal requires a
joint radial/angular estimate and matched UV subtraction. Neither the
existence of this coefficient sum nor an arbitrary finite part determines
the regulated full determinant or the physical matching.
