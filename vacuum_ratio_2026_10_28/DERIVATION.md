# VR28: stiffness, vacuum energy, and a conditional scaling relation

Status: the numerical value of B/V is **not derived**. The original PN28
parent admits a continuous family of ratios. A new two-exponential branch
derives B_curv/V_sector=delta from a specified scaling equation, but delta
and an allowed additive vacuum energy remain independent physical inputs.
The branch also changes the dense halo law. This document contains exact
conditional mathematics, not a completed microscopic theory.

Natural units are used in vacuum-sector equations; B and V are energy per
volume. The Newtonian halo equations retain G. s is dimensionless. The
canonical scalar is phi=F_s s, with F_s>0. No identification between the
internal dilation s and a relativistic dilaton has been established.

## 1. The exact freedom in the current parent

PN28 assumes Z=exp(2s), fixed-level canonical random energy K=k rho^(5/3),
and U=V+B[exp(3s)-3s-1], B>0. In the local scalar approximation minimize
W=K exp(-2s)+U. At its vacuum, U(0)=V, U_s(0)=0, U_ss(0)=9B. Thus

    B/V = U_ss(0)/(9 U(0)).                                  (1)

Equilibrium fixes the first derivative, stability its second derivative's
sign, and the vacuum Einstein equation relates the value to curvature.
None is an equality relating the value and second derivative. For fixed
V>0, every positive B retains the same vacuum location, convex potential,
positive nongravitational Hamiltonian and local EOS construction. For fixed
B, adding a constant C changes V to V+C and leaves all nongravitational
variations and the reduced pressure *gradient* unchanged. Gravity sees C;
that is a change of physical theory, not an innocuous energy-zero gauge.
No principle in the declared model forbids this change.

This is a counterfamily to selection by those hypotheses, not a no-go for
all microscopic theories. Halo boundary conditions computed after subtracting
V cannot restore the missing equation for V. Selecting C or B to reproduce
a desired acceleration would supply, rather than derive, that equation.

## 2. A useful reduction: pressure is a dilation response

For any differentiable potential U in this same local matter construction,
stationarity implies E_rel=K exp(-2s)=U_s/2. The full pressure is therefore

    P_total=(2/3)E_rel-U=(U_s-3U)/3.

Define the internal dilation-response function

    A(s)=U_s(s)-3U(s).                                       (2)

This definition is algebraic; A has not been identified with a quantum
spacetime trace anomaly. At a vacuum with U_s(0)=0 and V=U(0)>0,

    A(0)=-3V,       A_s(0)=U_ss(0)=9B_curv,
    B_curv/V=-(1/3) A_s(0)/A(0).                             (3)

Equation (3) gives an exact physical target for a microscopic calculation:
the logarithmic response of this breaking function, with the normalization
of s fixed by Z=exp(2s). Rescaling s without rescaling the matter coupling
would change the model. Simply defining A does not predict its response.
For PN28, A=9Bs-3V, so (3) is an identity, not a new selection law.

The strongest naive exact scaling equation, A=0, instead gives U=C exp(3s).
A finite stationary point requires C=0, hence V=B_curv=0. Exact unbroken
scaling of this restricted form cannot supply the desired positive vacuum
and nonzero stiffness. Explicit or anomalous breaking is essential.

## 3. Multiplicatively scaling response: a constructive continuation

Try a genuinely additional hypothesis with constant delta>0,

    A_s=-3 delta A.                                          (4)

Solving (2),(4), and imposing U(0)=V_sector>0 and U_s(0)=0 gives

    U_delta(s)=V_sector/(1+delta)
                [delta exp(3s)+exp(-3 delta s)].             (5)

Both terms are positive. U_delta tends to infinity at either end, U_ss>0
everywhere, and s=0 is its unique vacuum minimum. Consequently

    B_curv := U_ss(0)/9 = delta V_sector.                     (6)

This is a derivation within (4), not a prediction of delta. It also does
not show that an actual symmetry enforces (4) or excludes a constant C.

More generally, U=A_p exp(p s)+A_q exp(q s) at a stationary s=0 satisfies
U_ss(0)=-p q U(0). For p q>0, a positive-energy stationary point is unstable;
a stable one has negative energy. Opposite-sign exponents can instead give
a positive stable minimum. Setting p=3, q=-3delta gives (5)-(6). Thus a
small ratio has a concrete interpretation in this branch: a slowly varying
second term balancing the steep first term. It is not a loop factor or an
anomalous dimension until a microscopic theory supplies that dictionary.

### Exact changed EOS

Put B=B_curv, y=exp(3s)>=1, rho_*=[3B/(2k)]^(3/5). The unique matter
minimum follows from strict convexity of W at K>=0 and W_s(0)=-2K:

    K=3B/[2(1+delta)] y^(2/3)[y-y^(-delta)],
    rho/rho_*=(1+delta)^(-3/5)y[1-y^(-1-delta)]^(3/5),
    P_total=-V_sector y^(-delta),
    P_ex=P_total+V_sector=V_sector[1-y^(-delta)].              (7)

The compressional response is positive:

    dP_total/dln rho =
      5B y^(-delta)[y^(1+delta)-1]/[5y^(1+delta)+3delta-2].    (8)

At fixed B and y, delta->0 gives exactly the PN28 EOS and
U_delta-V_sector -> B[y-1-ln y]. The *unsubtracted* vacuum energy
V_sector=B/delta diverges in that limit. This limit cannot establish a
finite positive-vacuum PN28 normalization.

For finite delta, P_ex/B=[1-exp(-delta ln y)]/delta. It looks logarithmic
only while delta ln y is small. At fixed delta>0 and infinite density,
P_ex saturates at V_sector, and its logarithmic derivative falls as
B y^(-delta). Therefore B_curv is not an asymptotic nonzero log-pressure
coefficient in this changed model. Transferring the PN28 limiting column
formula with B_curv substituted for B would be an error.

## 4. Finite halos and the changed high-density column

The enthalpy h=(5/3)k rho^(2/3)exp(-2s), measured from zero density, obeys

    h=h_* psi,       h_*=5B/(2rho_*),
    psi=(1+delta)^(-2/5)[1-y^(-1-delta)]^(2/5),
    n(psi)=rho/rho_*=
      psi^(3/2)[1-(1+delta)psi^(5/2)]^[-1/(1+delta)].          (9)

Here 0<psi<psi_max=(1+delta)^(-2/5). With
ell^2=5B/(8piG rho_*^2), hydrostatic equilibrium becomes

    psi''+2psi'/r=-n(psi),   psi(0)=psi_c, psi'(0)=0.          (10)

For every fixed 0<psi_c<psi_max, the regular solution reaches zero at a
finite radius. To see this, let m'=r^2 n and psi'=-m/r^2. If psi stayed
positive forever, its limit must be zero, since a positive limit forces
quadratic decrease. Monotonic psi and n>=psi^(3/2) imply

    psi(r)=integral_r^infinity m(t)/t^2 dt>=m(r)/r,
    m(r)>=r^3 psi(r)^(3/2)/3,
    psi(r)<=9/r^4,
    psi(r)>=m(r0)/r for fixed r0>0.

The last two bounds contradict each other. The source is bounded on
[0,psi_c], so the finite edge has finite mass and nonzero negative slope.
Density vanishes there as (R-r)^(3/2). This proves the reduced-model
finite-radius result; it is not a theorem for the uncomputed full gradient
system or a formation/stability result.

### Central scaling, including its nonuniform log limit

Let y_c grow at fixed delta>=0, n_c=n(psi_c), D_c=B y_c^(-delta), and

    L_c^2=D_c/(4piG rho_c^2),
    zeta=r_phys/L_c,
    v=(5/2)n_c y_c^delta(psi_c-psi),
    e_c=y_c^(-1-delta),
    u=[2(1+delta)e_c/(5(1-e_c))]v.

The exact central equation is v''+2v'/zeta=g_c(v), where

    g_c(v)=(1-u)^(3/2)
       [1-(e_c^(-1)-1)((1-u)^(5/2)-1)]^[-1/(1+delta)].       (11)

In its positive matter domain, g_c is decreasing and at most one. As
e_c->0, it and its first derivative converge uniformly on each compact
v interval to [1+(1+delta)v]^[-1/(1+delta)]. Taylor's theorem on compact
intervals proves this because u is a constant times e_c v. The regular
integral equation and a uniform Lipschitz bound then give convergence of
v and its derivative on every fixed finite zeta interval; v<=zeta^2/6
keeps the needed v range compact. Set Theta=1+(1+delta)v. The limit is

    Theta''+2Theta'/zeta=(1+delta)Theta^[-1/(1+delta)],
    Theta(0)=1, Theta'(0)=0,
    Theta(xi_delta)=4^(1+delta).                             (12)

The quarter-density crossing is unique, finite and transverse. If it were
never reached, the RHS would be at least (1+delta)/4, contradicting a
bounded Theta; its radial derivative is strictly positive. Uniform
convergence therefore also gives convergence of the crossings. It follows
that the actual reduced core column has the asymptote

    Sigma_core = xi_delta sqrt(B/(4piG)) y_c^(-delta/2)
                 [1+o(1)]       at fixed delta>=0.           (13)

delta=0 recovers xi_0=5.84477... and PN28's constant column. At every fixed
delta>0 the column tends to zero as y_c->infinity. In the dense regime
y_c is proportional to rho_c/rho_*, so the leading logarithmic slope of
the column is -delta/2. The double limit delta->0 with delta ln y_c fixed
retains a finite suppression; the log limit is not uniform in density.

Using the adopted Sigma_core=a0/(2piG) identification only as a conditional
dictionary, (6),(13) give

    a0_core^2/(G V_sector)
       =pi xi_delta^2 delta y_c^(-delta)[1+o(1)].             (14)

It is state dependent. Equating delta to the old desired B/V alone cannot
derive exactly universal kappa=1/2 in this changed branch. This is a useful
new discriminator of the candidate rather than an achieved normalization.

## 5. The additive-constant test survives the constructive branch

Take U_new=U_delta+C. All scalar equations, particle equilibria, curvatures,
excess pressures and halos are unchanged in the nongravitating/local halo
approximations. The full vacuum becomes V_total=V_sector+C, so

    B_curv/V_total = delta V_sector/(V_sector+C).             (15)

An open interval of C around zero preserves V_total>0 and the same stable
scalar minimum. The scaling equation (4) is no longer satisfied by the
*total* A: adding C shifts A by -3C. Thus (4) must be justified for the full
gravitating effective action, including its constant operator. Declaring
C=0 without that justification is a normalization choice.

## 6. Does gravity turn vacuum stability into selection?

As a vacuum-sector test, consider the separately specified scalar-tensor
action sqrt(-g)[F_g(s)R/2-F_s^2(grad s)^2/2-U(s)], with F_g>0. This is
not a covariant completion of PN28's relative-stream coupling. At constant
s and a maximally symmetric vacuum, its equations give

    R=4U/F_g,       U_s=2U F_g_s/F_g.                        (16)

At the PN28 minimum U_s=0 and V>0, (16) requires F_g_s(0)=0. The Einstein
frame potential is M^4 U/F_g^2, and choose F_g(0)=M^2. Its scalar curvature
at this vacuum is

    U_E,ss(0)=9B-2V F_g,ss(0)/F_g(0).                       (17)

The scalar kinetic coefficient is positive there for F_s^2>0. For the
explicit positive coupling F_g=M^2 exp(alpha s^2), local vacuum stability
requires 9B-4alpha V>0. This is an open inequality, not a selected value.
Minimal coupling alpha=0 admits every B/V>0; every alpha<=0 does too.
For alpha>0 it supplies a lower bound B/V>4alpha/9 with alpha still free.
Saturating the bound makes a massless marginal vacuum and is an extra
condition, not the stable-vacuum result.

In the minimal case H^2=V/(3M^2) and m_phi^2=9B/F_s^2 give
m_phi^2/H^2=27(B/V)(M/F_s)^2. Even an assumed mass-to-Hubble equality leaves
F_s/M unspecified. No cosmological boundary/health equation tested here
removes the independent stiffness.

## 7. Vacuum thermodynamics identifies a response, not its magnitude

The primary-source convention for a self-sustained vacuum medium uses
gravitating equilibrium energy epsilon(q)-mu q, with mu=epsilon_q(q0),
and inverse compressibility q0^2 epsilon_qq(q0). See SOURCES.md for the
source and the distinction between equilibrium identities and off-shell
grand potential at fixed mu. A continuous variable q alone is not a proof
that PN28's internal dilation is this medium.

For a precise conditional dictionary set q=q0 exp(3s), keep mu fixed, and
write U(s)=epsilon(q)-mu q. At a vacuum stationary point,

    U_ss(0)=9 q0^2 epsilon_qq(q0),
    B_curv=q0^2 epsilon_qq(q0)=chi_vac^(-1),
    V=epsilon(q0)-q0 epsilon_q(q0).                          (18)

The source's positive-compressibility condition constrains the sign of B,
not the ratio. In the isolated zero-external-pressure equilibrium it gives
V=0, not the required small positive energy. A nonzero boundary pressure
or nonequilibrium state needs its own physical derivation.

There is an exact thermodynamic realization of the PN28 potential, namely

    epsilon(q)=mu q+V+B[q/q0-ln(q/q0)-1].                    (19)

Then epsilon_q(q0)=mu and q^2 epsilon_qq(q)=B everywhere. V and B are
independent in this example. The free-medium pressure computed at fixed
charge is -epsilon+q epsilon_q=-V+B ln(q/q0), while epsilon-mu q gives
the scalar potential. Replacing fixed mu by epsilon_q(q) *before* varying
the latter would incorrectly change its scalar equation.

Indeed, for general epsilon under this dictionary the complete stationary
matter-plus-scalar pressure is exactly q epsilon_q-epsilon: the term
(2/3)E_rel equals q(epsilon_q-mu) and cancels the chemical-potential term.
Thus dP_total/dln q=q^2 epsilon_qq. For the two-exponential branch this
bulk modulus is B(q/q0)^(-delta); delta is its negative logarithmic slope.
This supplies another precise response-function interpretation, without
identifying the vacuum coordinate q with the particle mass density rho.

The negative-power-to-logarithm limit itself is known. The checked 2019
primary source derives it for generalized Chaplygin fluids, including the
divergent amplitude and compensating pressure constant. Our y (or q) is
not that source's fluid energy density, and our exact rho(y) and outer
polytropic edge differ. The overlap does not provide the missing delta or
vacuum offset. See SOURCES.md; no novelty claim is made for that limit.

For a general microscopic epsilon and an equilibrium state q(mu),
V(mu)=epsilon(q(mu))-mu q(mu) obeys

    dV/dmu=-q,       d^2V/dmu^2=-1/epsilon_qq.                (20)

Thus stiffness is a susceptibility and vacuum height a separate integration
datum. Equation (18) is a useful microscopic matching target. It is not an
equation of state forcing chi_vac^(-1)/V to a universal constant.

## 8. Does a dilaton anomaly provide the missing microscopic equation?

The checked primary source states a PCDC relation under light-scalar
saturation, f_D^2 m_D^2=-16 E_sector, with a condensate-independent part
subtracted from E_sector. It is a conditional low-energy relation, not a
theorem identifying that energy with positive cosmological vacuum energy.

Even granting the additional identifications m_D=m_phi and f_D=F_s,
the relation would give 9B=-16 E_sector. Stable B>0 needs E_sector<0.
For the full gravitating vacuum V_total=C+E_sector>0,

    B/V_total=-(16/9) E_sector/(C+E_sector).                  (21)

The offset reappears. Setting E_sector=V_total>0 gives the wrong sign;
taking an absolute value silently changes the source identity. If f_D
differs from F_s there is an additional free normalization. Neither PN28
nor this continuation establishes a spacetime dilaton, single-state
saturation, a beta function, or a protected full vacuum energy. An actual
microscopic model that calculates those data would be a new input, not
completion of an already specified source-to-target implication.

## 9. What has and has not been selected

The constructive advance is a precise conditional mechanism: constant
relative dilation response gives two opposing exponentials, a stable
positive sector vacuum, B_curv/V_sector=delta, and a calculable slow
running of the halo column. The ratio has become a scaling-response
question, and its halo consequence can be checked independently.

No tested principle calculates delta or forbids C. Gravity yields bounds;
vacuum thermodynamics identifies stiffness; the checked anomaly relation
refers to a subtracted sector and does not fix total positive vacuum energy.
These results close those particular attempted shortcuts, not all possible
microscopic routes. The remaining exact obligations and executable resumption
conditions are recorded in HANDOFF.md. Numerical checks and self-review are
separate artifacts; there is no independent-agent review in this checkpoint.
