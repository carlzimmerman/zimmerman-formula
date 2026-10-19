# Unconditioned sphere Weyl susceptibility and charge response

FSP-009, parent FSP-008. Owner: vacuum_global. This derives identities for the
actual unconditioned regulated QCD/QED measure. It does not evaluate that
measure. The original physical A_rho, R and alpha remain open.

## 1. Contract and the new missing observable

Set r=H^-1, t=log r, Omega=8 pi^2/3, V=Omega exp(4t), W=-log Z and
rho=W_t/(4V). Choose one regulator, one absolute measure prescription and a
common renormalized parameter family. Absorb the Jacobian of any metric
dependent choice of integration variables into S(t,u), so

    Z(t,u)=integral dPhi exp[-S(t,u)],  u=e^2=4 pi alpha.

The t derivative holds renormalized parameters fixed. In a fixed angular
lattice discretization, changing r changes the physical lattice spacing;
the bare couplings must therefore follow the line of fixed renormalized
parameters. Differentiating only the explicit metric weights would give a
different derivative. The present identities include that trajectory and all
local gravity, measure, regulator and current contacts in S and its derivatives.
Continuum differentiation and limits are additional physical obligations.

Write X=S_t, Y=S_tt, J=S_u, X_u=S_tu and Y_u=S_ttu. For any observable O,

    d_t <O> = <O_t>-Cov(O,X),
    d_u <O> = <O_u>-Cov(O,J).                         (1)

Consequently the contact-complete Weyl susceptibility defect is

    E = W_tt-4W_t
      = <Y-4X>-Var(X)
      = 4 V rho_t.                                 (2)

The word defect refers to subtraction of the extensive flat-vacuum Weyl
response, not an asserted failure of a Ward identity. The zero-curvature
vacuum term rho0 V is annihilated exactly by d_t^2-4 d_t.

If rho=rho0+A H+q(H), with q_t=o(H), then

    A = -lim_(H->0) H^3 E/(4 Omega).                 (3)

This is an expectation/variance cancellation in the full unconditioned sphere
measure; it needs neither a forced topological sector nor a momentum-to-radius
substitution. The finite-H expression is defined regardless of whether its
limit exists. The differentiated remainder in (3) is an extra hypothesis:
q=o(H) alone does not imply q_t=o(H). The earlier FSP-006 stress stencil
does not need this hypothesis and remains a useful orthogonal measurement.

For a local term c_n integral sqrt(g) R^n on round S4, W is proportional to
r^(4-2n). Its contribution to E is p(p-4)W, p=4-2n. Thus cosmological
and curvature-squared terms are annihilated, and the Einstein term produces
O(r^2), hence only O(H) contamination in (3). A usual scale anomaly term
c log r gives E=-4c and O(H^3) contamination. Higher local curvature terms
give still smaller contributions. No finite analytic local gravity
counterterm generates a constant limit in (3).

An unknown common metric factor exp[-C(t,u)] multiplying every sector shifts
E by C_tt-4C_t. In particular C=b(u)r^3 shifts E by -3b r^3 and (3) by
3b/(4 Omega). The variance of X alone misses this term: its c-number is in
the contact-completed mean <Y-4X>. This explicitly retains the absolute
normalization information absent from normalized topological probabilities.

## 2. Exact charge insertion and a measurable bound

Put B=Y-4X and C=Y_u-4X_u. Differentiation of the normalized measure gives

    E_u = <C>-Cov(B,J)-2Cov(X,X_u)+kappa(X,X,J).       (4)

The last term is the connected third cumulant, with all variables integrated.
It is not obtained from a separated flat TJJ correlator. Y_u is a genuine
two-metric/charge contact; X_u is the one-metric/charge contact. At zero
charge J may be represented by the complete integrated-photon insertion,
including all flavor/disconnected classes and matching terms. The absolute
photon/gauge functional must be retained when defining S; an orientation or
topology ratio does not supply it. At finite charge use the exact S_u.

There is a useful two-variable rewriting. Define

    F = B-(X-<X>)^2.

Since kappa(X,X,J)=Cov((X-<X>)^2,J), (4) becomes

    E_u=<C>-2Cov(X,X_u)-Cov(F,J).                    (5)

The t/u derivative of the centering mean adds no expectation contribution,
because <X-<X>>=0. For a real positive theta=0 vectorlike measure with
finite moments, Cauchy-Schwarz therefore yields the quantitative finite-H
bound

    |E_u| <= |<C>|+2 sigma_X sigma_Xu+sigma_F sigma_J. (6)

These are measurable moments on the same curved ensemble. The right side
is not presumed small, and no physical value is assigned to it here. In a
charge-insertion decomposition J=J_kept+J_missing, if X_u,Y_u are complete,
the exact omitted term is -Cov(F,J_missing), bounded by
sigma_F sigma_Jmissing. If those contacts are also omitted, their actual
mean/covariance errors must be included. A bare explicit flavor factor
does not bound this variance.

If q_tu=o(H), the charge response is

    A_u=-lim H^3 E_u/(4 Omega),   A_alpha=4 pi A_u.   (7)

Uniform q_tu control is not supplied by a finite u=0 insertion. On a
calibrated path lambda_a(u), replace d_u by the tangent derivative and
J by S_u+sum lambda'_a S_lambda_a, with the same replacement in X_u,Y_u.
The metric derivative itself holds that path's parameters fixed at each u.
For an unfixed proton mass, R_u=A_u/m_p^3-3 A m_p,u/m_p^4.

Equations (2),(4),(5) produce an explicit sufficient global premise:
if for some delta>0 and uniform constants M0,M1 at small H

    |<B>-Var X| <= M0 H^(-3+delta),
    |<C>-2Cov(X,X_u)-Cov(F,J)| <= M1 H^(-3+delta),   (8)

then the corresponding finite-H coefficient estimators obey

    |A_H| <= M0 H^delta/(4 Omega),
    |A_u,H| <= M1 H^delta/(4 Omega).                (9)

Provided the target and differentiated limits exist, both coefficients are
zero. This is a conditional global criterion for QCD, with explicit contacts
and measurable quantities. Neither a flat hadronic mass gap, positivity,
nor the trace anomaly proves (8). In particular each extensive term in (8)
can be O(H^-4); its required cancellation is a real physical leaf. The
stronger measurable bound (6)=o(H^-3) would suffice for the second line
but is not necessary; it can lose important cancellations.

## 3. Higher Weyl projector, kept separate from the minimal estimator

Let Z3=S_ttt. An independent local subtraction is

    K = W_ttt-6W_tt+8W_t
      = <Z3-6Y+8X>-3Cov(X,Y)+6Var X+kappa(X,X,X).   (10)

It annihilates the cosmological, Einstein and constant W terms exactly.
For W=(4 Omega/3) A r^3 it gives K=-4 Omega A r^3. Thus
A=-lim H^3K/(4 Omega) with the correspondingly stronger differentiated
remainder control. Its u derivative is

    K_u=<Z3_u-6Y_u+8X_u>-Cov(Z3-6Y+8X,J)
       -3Cov(X_u,Y)-3Cov(X,Y_u)+3kappa(X,Y,J)
       +12Cov(X,X_u)-6kappa(X,X,J)
       +3kappa(X_u,X,X)-kappa(X,X,X,J).             (11)

The fourth cumulant is required. This higher-contact observable can test
the subtraction and matching, but is more demanding than (2),(4). Its
relation to the old finite-radius projectors is mathematical overlap;
the new result here is the contact-complete action/cumulant implementation,
the reduced charge formula (5), and its measurable finite-H bound.

## 4. A new physical lattice source and its exact restricted implication

Braguta, Goy, Dey and Roenko, arXiv:2602.20970v2, equations (24)-(34),
define a real-acceleration SU3 pure-gauge lattice measure in a finite
right-Rindler region. Its Euclidean metric is the positive version of
ds^2=(1+a_acc z)^2 d tau^2+dx^2+dy^2+dz^2. On the region away from its
horizon it has zero Riemann curvature; the source explicitly says this
in Section II.2. The observed state is thermal, tau has period 1/T0.
The z interval is centered and open; x,y,tau are periodic. The quantities
reported are Polyakov loops, their susceptibilities and the spatial
confinement/deconfinement transition. A static-quark free energy obtained
from a Polyakov loop is a normalized external-probe free energy.

The source's alpha denotes acceleration, not electromagnetic alpha. Write
a_acc for its physical acceleration and a_lat for its lattice spacing;
eta=a_acc a_lat. At fixed lattice spacing, beta and boundaries, equation
(34) is exactly of the form

    S(eta)=beta sum_x [E_x/(1+eta z)+ (1+eta z) B_x],

where E_x and B_x include the specified Symanzik plaquette/rectangle sums.
Its action derivatives at eta=0 are

    X_eta=beta sum z(B_x-E_x),
    Y_eta=2 beta sum z^2 E_x.                       (12)

For a reflection-invariant centered domain/measure, z->-z maps the action
at eta to that at -eta (electric/magnetic square sums are reflected).
Hence Z(eta)=Z(-eta), and finite compact-link integration is analytic for
|eta| max|z|<1. The unconditioned global first derivative is exactly zero,
and the actual second derivative is

    W_eta_eta(0)=2 beta <sum z^2 E_x>
                 -Var(beta sum z(B_x-E_x)).         (13)

This is a nonperturbative finite-regulator consequence of the actual
source action, not a free-particle or weak-coupling calculation. It shows
precisely why a metric Hessian cannot be inferred from a current or
Polyakov susceptibility. Symanzik E_x need not be positive term by term,
so no sign for (13) is asserted.

It does not prove absence of a |a_acc| term after a nonuniform infinite-
volume limit: the guaranteed analytic neighborhood shrinks with the z
extent. It supplies neither S4 curvature H nor positive-mass dynamical
quarks, an electromagnetic derivative, a proton observable, or the
unconditioned sphere contacts in (2),(4). The source-to-target application
is therefore inapplicable for extracting A, while (12),(13) are verified
restricted implications. The companion proceedings 2603.01754v1 supplies
the same action in equation (7); its smaller acceleration list does not
supersede the accepted paper's full list. The old Yamamoto source audit
is inherited and is not counted as new acquisition.

## 5. Verification and continuation

check_weyl.py compares the contact formulas with independently constructed
normalized finite-state partition derivatives, using exact rational jets.
Fixtures include c-number metric terms, nonzero mixed metric/charge
contacts, and both nonzero means and fluctuations. They are algebra
fixtures, not QCD samples. A separate source-action reflection fixture
checks (12),(13). Monomial checks verify local subtraction and the exact
S4 area coefficient. Run manifests record the actual bounds and hashes.

The physical continuation is to measure X,Y,J,X_u,Y_u and their joint
moments in one absolutely normalized sphere regulator along a line of
fixed renormalized physics. First compare W_t and W_tt with independent
radius reweighting; then measure the two cancellations in (8) with
continuum and radius errors. The accepted Rindler ensembles cannot be
relabeled as those measurements. No existing retrieved source closes this
leaf, and no source search establishes a no-data or novelty theorem.
