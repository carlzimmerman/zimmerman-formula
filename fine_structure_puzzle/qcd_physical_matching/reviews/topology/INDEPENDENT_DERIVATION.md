# Independent derivation saved before target inspection

Date: 2026-10-19. Reviewer: delegated independent topology/contact reviewer.
Input supplied by parent: finite-regulator partition function and definitions,
plus the displayed large-volume saddle expression. No target derivation,
report, source manifest, or checking script has been opened at this point.

## Conventions and admissible derivatives

I take W=-log Z; this convention is essential for all signs below. Let

Z(t,theta,u)=integral exp[-S(t,u)+i theta Q],
t=log a, V=Omega a^4, T=S_t, I=S_u.

The integration measure is included in S, or is fixed. Omega and integer Q
are held fixed under t and u differentiation; V_u=0. Derivatives exist and
commute at the regulator. CP at theta=0 is preserved by the t and u
deformations. Connected brackets denote joint cumulants, not an ordinary
covariance of uncentered products. Define rho=W_t/(4V) and chi=W_theta_theta/V.

## Exact finite-regulator metric identities

At theta=0,

W_t=<T>, W_theta_theta=<Q^2>,
W_t_theta_theta=-<T Q Q>_c.

Therefore

rho_theta_theta= -<T Q Q>_c/(4V)
                 = chi + chi_t/4.

The second equality follows from W_theta_theta=V chi and V_t=4V.
It is not an assumption about a thermodynamic limit or about dimensional
analysis. It is a finite-regulator identity for the specified deformation.

The mixed u derivative gives

rho_theta_theta_u
  = [<T I Q Q>_c - <S_tu Q Q>_c]/(4V)
  = chi_u + chi_tu/4,

where chi_u=-<I Q Q>_c/V. The S_tu term is an operator contact:
T itself depends on u. A four-insertion cumulant alone is insufficient
unless S_tu vanishes, or its connected insertion vanishes, for a stated
reason. CP permits <TQQ>_c=Cov(T,Q^2), but the four-insertion expression
must still retain its full connected subtraction. If the u deformation
does not preserve CP, additional nonzero one-Q expectations must be retained
and the simplified CP formulas need rederivation.

## Exact fixed-sector identity

For Z_Q the same regulated integral restricted to Q, set P_Q=Z_Q/Z(0).
Then W_Q=W(0)-log P_Q and, defining rho_Q=(W_Q)_t/(4V),

rho_Q-rho= -(log P_Q)_t/(4V),
(rho_Q-rho)_u= -(log P_Q)_tu/(4V).

The derivative is at fixed integer Q and fixed Omega, not at fixed charge
density Q/V. The identities are exact independently of a saddle expansion.

## Differentiating the supplied saddle

Suppose, for fixed Q, x=chi V grows and

log P_Q=-1/2 log(2 pi x)-Q^2/(2x)-c4/(8 chi^2 V)+R,
R=O(V^-2).

Write D=4+chi_t/chi and B=c4/chi^2. Algebra gives

rho_Q-rho
 = D/(8V) [1-Q^2/x] + (B_t-4B)/(32V^2) - R_t/(4V).

Writing E=chi_u/chi, the corresponding mixed response is

(rho_Q-rho)_u
 = {D_u[1-Q^2/x]+D Q^2 E/x}/(8V)
   +(B_tu-4B_u)/(32V^2) - R_tu/(4V).

Replacing the last terms by O(V^-3) requires derivative bounds
R_t=O(V^-2), respectively R_tu=O(V^-2), uniform on the relevant coupling
and scale neighborhood. A pointwise big-O estimate alone does not imply
them. For example R(V,u)=V^-2 sin(u V^3) has the displayed pointwise size
but an unbounded u derivative. The t analogue can be made by oscillating
rapidly in log V. It also matters that the expansion is fixed-Q; Q scaling
as sqrt(V) requires the appropriate uniform saddle expansion, with additional
Q-dependent terms at the corresponding orders.

If chi and c4 are t independent, the first formula reduces to

rho_Q-rho=1/(2V)[1-Q^2/(chi V)]-c4/(8 chi^2 V^2)+O(V^-3),

only with the derivative-uniform remainder hypothesis. This is a sector
conditioning correction, not by itself the physical infinite-volume vacuum
energy or an H-linear cosmological response.

## What would test a physical H-linear response

A specified curved-background family g(H), a renormalized stress observable,
fixed physical couplings and a stated state/ensemble, and controlled continuum
and infrared limits are required. A proposed rho(H)=rho(0)+C H+o(H) can be
tested by a finite, nonzero limit [rho(H)-rho(0)]/H after the stated allowable
subtractions. A flat-box L^-1 dependence with H merely renamed L^-1 does not
identify this cosmological response. A theta-curvature measurement constrains
C_theta_theta, not an arbitrary theta-independent C.

Multiplying all sectors by exp[-F(g,u)] with F theta independent preserves
P_Q and all theta derivatives of W, while shifting rho by F_t/(4V).
This proves an inference/identifiability limitation of topology data. It
does not prove that every such F is an admissible QCD counterterm. That
requires locality, covariance, the renormalization scheme and boundary
conditions. On a smooth closed four-geometry, analytic local bulk metric
counterterms give the familiar curvature orders (constant, H^2, H^4, ...),
and do not automatically supply an H term; boundaries and nonlocal physical
responses need separate treatment.

Consequently these identities can establish missing contacts, sector effects,
and insufficient topological information. They do not establish a universal
QCD mass-gap no-go theorem for every proposed H-linear response.
