# Candidate solution: constraint-defined MOND MMG

## 1. Core idea

Define the scalar gravitational constraint directly as the MOND elliptic equation for the lapse, instead of generating MOND through a propagating nonlocal scalar.

ADM variables are

N, N^i, gamma_ij, pi_N, pi_i, pi^ij.

Let

q = (1/6) ln det(gamma_ij),

p = pi/sqrt(gamma),  pi = gamma_ij pi^ij.

For inhomogeneous modes define

S_4 = pi_N,

S_1 = C_M,

S_2 = D^2 q,

S_3 = D^2 p.

The MOND constraint is

C_M = D_i[c^2 mu(y) D^i ln N] - 4 pi G rho_m,

y = (c^2/a_0) sqrt(D_i ln N D^i ln N),

mu(y)=1-e^{-y}.

The total Hamiltonian is

H_T = H_GR+H_m + int d^3x [lambda_N S_4 + mu_1 S_1 + mu_2 S_2 + mu_3 S_3 + N^i H_i + lambda^i pi_i].

This is a Hamiltonian MMG candidate. It is not claimed to be a manifestly 4D covariant local action.

## 2. Exact MOND constitutive primitive

Define

G(y)=y^2+2(1+y)e^{-y}-2.

Then

G'(y)=2y(1-e^{-y}),

so

G'(y)/(2y)=1-e^{-y}=mu(y).

Thus the static constitutive sector can be represented by the local spatial potential G(y).

## 3. Newtonian limit

Let

N=1+Psi/c^2+O(Psi^2/c^4).

Then

D_i ln N = D_i Psi/c^2+O(Psi^2/c^4),

y=|D Psi|/a_0+O(Psi/c^2).

Hence

C_M=0

reduces to

D_i[(1-e^{-|D Psi|/a_0})D^i Psi]=4 pi G rho_b

at leading order.

## 4. Dirac matrix

For

Phi_A=(S_4,S_1,S_2,S_3),

the local/smeared Dirac matrix has the form

Delta =
[[0,L_N,0,0],
 [-L_N^T,*,*,*],
 [0,*,0,K],
 [0,*, -K^T,*]],

where

L_N = delta C_M / delta N,

K={D^2q,D^2p}.

The determinant/Pfaffian is

det Delta = (L_N K)^2

provided the operator products are understood with compatible boundary conditions.

Thus full rank holds on the branch where L_N and K are invertible.

## 5. Ellipticity of the MOND lapse constraint

Set

u_i=D_i ln N,

u=|u|,

y=c^2 nu/a_0.

The flux is

F^i=c^2 mu(y)u^i.

Its derivative with respect to u_j is

A^i_j=c^2[mu(y) delta^i_j + y mu'(y) uhat^i uhat_j].

The two eigenvalues, after removing the positive c^2 factor, are

lambda_perp=mu(y),

lambda_parallel=mu(y)+y mu'(y).

For

mu=1-e^{-y},

lambda_perp=1-e^{-y}>0,

lambda_parallel=1-e^{-y}+y e^{-y}=1+(y-1)e^{-y}>0

for y>0.

Therefore the lapse operator is generically elliptic away from the exactly zero-gradient branch.

## 6. Scalar-pair bracket

The exact normalization depends on the chosen canonical normalization of p. With the standard local canonical bracket

{q(x),p(y)}=C_q delta^3(x-y),

one obtains for nonzero Fourier mode

{D^2q(k),D^2p(-k)}=C_q k^4.

Hence K is nonzero for k != 0.

## 7. Degree-of-freedom count

The full ADM phase space has 20 dimensions per spatial point. The six first-class constraints

pi_i=0,
H_i=0

remove 12 dimensions.

The four scalar second-class constraints

pi_N=0,
C_M=0,
D^2q=0,
D^2p=0

remove another 4 dimensions.

The remaining phase space is

20-12-4=4

per spatial point, i.e.

N_DOF=2.

The Laplacian constraints S_2,S_3 act only on nonzero spatial modes, leaving homogeneous zero modes for the background sector.

## 8. What is actually closed

The following part is a constructive closure candidate:

- exact MOND constitutive law;
- exact MOND static lapse constraint;
- explicit four scalar constraints;
- generic rank-4 Dirac matrix;
- two local gravitational configuration degrees of freedom on the nonzero-k nondegenerate branch.

## 9. What is not yet a theorem

The candidate is not yet a complete physical theory until the following are derived rather than assumed:

1. full functional Poisson brackets including the exact matter terms;
2. constraint preservation with the full H_GR+H_m;
3. the exact tensor quadratic action of the modified Hamiltonian;
4. matter energy-momentum consistency;
5. a controlled zero-mode/cosmological prescription;
6. a Legendre transform, if a configuration-space action is desired;
7. any PPN/lensing/cosmological viability tests.

Therefore the correct status is

CONDITIONALLY CLOSED

not CLOSED.
