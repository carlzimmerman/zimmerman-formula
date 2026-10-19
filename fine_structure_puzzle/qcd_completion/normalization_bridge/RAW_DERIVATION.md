# Microscopic SU(2) normalization, frozen before project-report comparison

Status: independently derived from the task's stipulated microscopic conventions.
No project report or Unsal-Yaffe equation has been read for this derivation.
The contraction in the microscopic action sums over all ordered Euclidean
indices mu,nu. The circle has circumference L.

## Input contract

Hermitian generators are T^a = sigma^a/2 and tr(T^a T^b)=delta^{ab}/2.
The connection carries no coupling in D=d+iA, and

    S4 = (1/(2 g^2)) integral tr(F_mu nu F_mu nu).

The asymptotic holonomy is A4=v T3, so its eigenvalue difference, and the W
mass, is v. Define B_i^a=(1/2) epsilon_ijk F_jk^a. A smooth charge-q monopole
has B^3=q rhat/r^2 and flux 4 pi q. The monopole vertex is exp(i q phi), with
phi periodic modulo 2 pi. Boundary fluxes or total charge require their usual
separate treatment; pair energies below are separated from self energies.

## Abelian Maxwell action and first-order dualization

Because tr(F_ij F_ij)=B^a B^a (both i,j orders occur), the static Abelian
Maxwell action is

    SB = L/(2 g^2) integral (B^3)^2 = KB/2 integral (B^3)^2,
    KB = L/g^2.

Impose div B^3=4 pi rho, rho=sum_j q_j delta(x-x_j), by the first-order
integral

    exp[-KB/2 integral B^2 - i/(4 pi) integral phi (div B-4 pi rho)].

Integration by parts gives +i/(4 pi) integral grad(phi).B and the vertex
exp(i sum_j q_j phi(x_j)). Completing the B square gives

    Sdual,kin = 1/(32 pi^2 KB) integral (grad phi)^2
              = kappa_dual/2 integral (grad phi)^2,
    kappa_dual = g^2/(16 pi^2 L).

Changing the sign of the Lagrange multiplier changes the signs of all vertex
charges together and changes none of these coefficients.

For the general convention div B=Q rho, the same derivation gives

    kappa_dual = 1/(KB Q^2),
    KB Q^2 = 1/kappa_dual.

Under B'=c B one must use KB'=KB/c^2 and Q'=c Q. The product KB Q^2 is
unchanged. Here Q=4 pi, so it is 16 pi^2 L/g^2.

## Pair Coulomb coefficient

B_j=-q_j grad(1/|x-x_j|), and, for separated centers,

    integral B_i.B_j = 4 pi q_i q_j / r_ij.

The cross term in KB/2 integral (sum B_j)^2 is therefore

    Spair = (4 pi L/g^2) sum_(i<j) q_i q_j/r_ij
          = (KB Q^2/(4 pi)) sum_(i<j) q_i q_j/r_ij.

Independently, the dual propagator is
<phi(x) phi(y)>=1/(4 pi kappa_dual |x-y|). The Gaussian expectation of
normal-ordered monopole vertices yields precisely this same pair action.
Like charges repel. There is no additional 1/2 in the i<j expression; the
equivalent ordered-pair sum does have 1/2.

## Monopole core / BPS action

The static non-Abelian action, including A4, is

    S3 = L/(2 g^2) integral [B^a B^a + (D_i A4)^a(D_i A4)^a]
       = L/(2 g^2) integral (B-D A4)^2
         + L/g^2 integral B_i^a D_i A4^a.

The Bianchi identity turns the last term into the surface integral, giving

    S_BPS = (L/g^2) v integral_(S2infinity) B^3.dS
          = 4 pi L v/g^2.

At the center-symmetric SU(2) holonomy v=pi/L,

    S0 = 4 pi^2/g^2 = (8 pi^2/g^2)/2.

The BPS core calculation contains both B and the holonomy scalar gradient.
Below the nonzero holonomy-scalar mass, the long-range photon action above
contains B alone. Adding the BPS scalar energy to the photon-only Coulomb
action is a change of effective problem, not a charge normalization.

## Electric charge dictionary

In the unrescaled connection A^3, fundamental weights carry electric charges
+/-1/2, while W bosons carry +/-1. With canonically normalized 3D field
a_i=sqrt(L) A_i^3/g and g3=g/sqrt(L), these are +/-g3/2 and +/-g3.
The smooth monopole flux of the canonical field is 4 pi/g3. Thus

    (g3/2)(4 pi/g3)=2 pi,   g3(4 pi/g3)=4 pi.

The existence or choice of allowed probe representations affects the electric
charge lattice; it does not halve this smooth SU(2) monopole's B^3 flux.

## Convention-invariant cross-check

All four stipulated microscopic inputs together force

    kappa_dual * S_BPS = v/(4 pi),
    kappa_dual * S0 = 1/(4 L)        (center-symmetric SU(2)).

A proposed dictionary that changes kappa_dual by a factor two while keeping
L, v, S_BPS, and the unit monopole vertex fixed is inconsistent with these
inputs. Rescaling g globally changes both kappa_dual and S_BPS inversely and
cannot repair their product.
