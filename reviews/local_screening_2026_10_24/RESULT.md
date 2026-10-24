# Local screening and the microscopic matching obstruction

Status: scoped nonselection, not a microscopic completion. The logarithmic self-tuning candidate has an exact classical cancellation of the bare vacuum parameter throughout its inhomogeneous base action. Its controlled, nonlinear-in-gradient local solution gives Vainshtein screening and an enhanced inverse-square outer force, not MOND. The cancellation does not constrain added normalized-clock response coefficients. No parameter-free a0 has been obtained.

Campaign footing: dark energy. Kappa=1/2 remains FITTED; CFG493 reports kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 separately. Neither measurement enters this calculation. Freeze: 70cf999088. Parent: ../self_tuning_selector_2026_10_24/RESULT.md. These are continuation calculations for that specified model, not a new arbitrary model scan.

## 1. Model and convention

Use signature -+++, c=1, reduced Planck M, and X=-(partial phi)^2/2>0:

S = integral sqrt(-g) [M^2 R/2 - V + K(X) - G3(X) box phi] + S_b[g],

K=-A ln(X/Xref),  G3=-sqrt(2)A/(3h sqrt(X)),
alpha=A/(M^2 h^2),  0<alpha<3.

The constant-X de Sitter branch has H=h and
Xv=Xref exp[(3M^2 h^2-V)/A], q=sqrt(2Xv)>0.
The interval above is the parent's homogeneous quadratic health condition. It is not a proof of local perturbative health throughout a halo. Both h and alpha are model inputs. Self-tuning the response to V does not derive the residual vacuum curvature h.

The covariant current and stress tensor are obtained by variation and cross-checked against equations (4) and (10) of [Imperfect Dark Energy from Kinetic Gravity Braiding, arXiv:1008.0048v2](https://arxiv.org/html/1008.0048v2). That source uses +--- and K+G box phi. Reversing the metric signature keeps X fixed and reverses box phi, giving the convention used here. For shift symmetry:

J^mu=(K_X-G3_X box phi) partial^mu phi-G3_X partial^mu X,

T_munu=(K_X-G3_X box phi) phi_mu phi_nu
        -G3_X(X_mu phi_nu+X_nu phi_mu)
        +g_munu[K+G3_X partial X dot partial phi].

The source provides the general equations, not the particular force law derived below. The self-tuning parent is [Bernardo, arXiv:2101.00965v2](https://arxiv.org/html/2101.00965v2), checked in the preceding review.

## 2. Exact local radial system, including gravity

Set ds^2=-N(r)^2 dt^2+dr^2/f(r)+r^2 dOmega^2,
phi=q t+psi(r), y=psi', nu=ln N. Then

X=q^2/(2N^2)-f y^2/2,
box phi=f y'+(2f/r+f nu'+f'/2)y,
J^r=f{K_X y-2G3_X[f y^2/r-X nu']}.

The scalar equation is (N r^2 J^r/sqrt(f))'=0. In n spatial dimensions replace r^2 by r^(n-1), and the 2f y^2/r term by (n-1)f y^2/r. For a regular star without direct scalar charge, the flux is zero. Independently, T_tr=q J^r/f: a diagonal static metric with q nonzero demands that same branch.

Define v=sqrt(f)y/sqrt(2X). The exact zero-current relation is

nu'=2v^2/r+3hv/sqrt(f),
X=q^2/[2N^2(1+v^2)].                                      (1)

With V included in the stress, write P=p_r. On this branch:

P=K-V=-3M^2h^2+A ln[N^2(1+v^2)],
rho=-P-(2A sqrt(f)/(3hv))[nu'+v v'/(1+v^2)],
p_t=P+G3_X f X' y.                                      (2)

Expressions dividing by v or y are only used where they are nonzero; at a regular center take their smooth limit from the original stress tensor. The two radial Einstein equations are

f'=(1-f)/r-r(rho_b+rho)/M^2,
nu'=[(1-f)/r+r(p_b+P)/M^2]/(2f).                         (3)

Together with (1)-(2) and p_b'=-(rho_b+p_b)nu', these retain lapse, scalar density and pressure backreaction. An interior also needs a matter equation of state. The angular equation follows through the Bianchi identity when scalar and matter conservation hold. This is an exact radial system on the static timelike-clock patch; it is not a solved global stellar/horizon boundary-value problem.

The source-free solution f=N^2=1-h^2r^2, y=-qhr/f gives X=Xv and exactly the de Sitter stress. By contrast, inserting constant X into Schwarzschild-de Sitter with f=N^2=1-2u/r-h^2r^2, u=G_N m_source, fails. The infalling-clock branch gives

box phi=-3q (u/r^2+h^2r)/sqrt(2u/r+h^2r^2).

Zero current at constant X would require box phi=-3hq. Squaring that requirement leaves u^2/r^4=0. Thus a nonzero source cannot be handled by assuming the vacuum X stays constant. This test is restricted to the stated constant-X ansatz; it is not a theorem against other sourced branches.

## 3. Solving the screened weak-potential regime

Take hr<<1, weak metric potentials and |v|<<1, with alpha fixed in the open healthy interval, away from its singular endpoint at 3. Keep both w^2/r and hw where v=-hr+w, and subtract the de Sitter force. Let g=Phi' be the inward gravitational acceleration magnitude from the source, G_N=1/(8pi M^2), and g_N=G_N m(<r)/r^2. Matter pressure is negligible at this order.

Equation (1) gives g=2w^2/r-hw. At the same retained order the scalar density perturbation is

delta rho_phi=-(2A/(3h))(w'+2w/r).

To see the cancellation controlling this result, the numerator in X'/X contains
-h^2r+g+(-hr+w)(-h+w'). Substituting the current equation factors it as (-hr+w)(w'+2w/r). This is why the scalar's metric response cannot be discarded.

The rr Einstein equation gives delta f=-2r Phi' at this order. Its tt counterpart then gives

nabla^2 Phi=rho_b/(2M^2)-A/(3hM^2)(w'+2w/r).

Integration from a regular center fixes the integration constant by the enclosed matter mass:

g=g_N-alpha h w/3.

Pressure-potential corrections and higher powers of the weak metric fields/flow have been dropped; the formula below is exact for these leading screened equations, not for the full system (1)-(3).

Put d=1-alpha/3>0 and s=-w>=0. The branch tending to the de Sitter solution when the source disappears obeys

2s^2/r+hd s=g_N,
s=(hdr/4)[sqrt(1+8g_N/(h^2d^2r))-1],
g=g_N+alpha h s/3.                                     (4)

For a compact source in its exterior define

r_V^3=8G_N m_source/(h^2d^2).

Then the closed force law is

g/g_N=1+[2alpha/(3d)]/[sqrt(1+(r_V/r)^3)+1].             (5)

Its inner and outer limits, provided both lie inside the validity domain, are

r<<r_V:  g=g_N+(alpha h/3)sqrt(G_N m_source/(2r))+...,
r_V<<r<<h^(-1):  g=g_N/d+... .

The inner correction falls as r^(-1/2), but is subdominant to Newton; the outer total force falls as r^(-2). Neither gives the required deep-MOND sqrt(G_N m_source a0)/r law. The two algebraic asymptotic limits in the script are limits of (4), interpreted physically only in overlap regions outside the source/strong-field radius and inside the cosmological radius. They are not claims about r=0 or r=infinity in the exact spacetime.

Moreover,

g_N(r_V)=(G_N m_source)^(1/3)(h^2d^2/8)^(2/3).

The crossover acceleration has mass exponent 1/3. It cannot be a universal a0. Finite-radius resemblance for a selected source or tuning alpha near 3 would not change this mass scaling; the latter also invalidates a uniform use of the present approximation. This is a sourced-force obstruction, stronger than the previous homogeneous-equilibrium test.

## 4. Exact action-level matching and its limit

Rescale phi=sqrt(2Xv) tau and define Y=-(partial tau)^2. Without any weak-field expansion, X=Xv Y and the scalar-plus-vacuum action becomes

L=-3M^2h^2-A ln Y+[2A/(3h sqrt(Y))] box tau.              (6)

V and Xref disappear from the entire classical base action. This strengthens the preceding background-only argument: local backreaction in this isolated base model need not restore sensitivity to bare V.

It still neither selects h nor supplies MOND. Equation (6) retains alpha after expressing A in units of M^2h^2, and the force law (5) depends on alpha. A field redefinition is not a computation of a quantum measure, radiative protection or a microscopic matching coefficient.

For the prior trial bridge B(X)=B0(X/Xref)^p, the same change of variables gives

B(X)=Bbar Y^p,  Bbar=B0(Xv/Xref)^p.                     (7)

Bbar remains an independent action coefficient. The normalized clock u_mu=-phi_mu/sqrt(2X)=-tau_mu/sqrt(Y) and its acceleration are invariant under the positive constant rescaling. Thus the rescaling cannot absorb a coefficient multiplying an operator made solely from u and the metric.

Equivalently, the base action admits the parameter transformation phi -> lambda phi, V -> V-2A ln lambda for lambda>0. Its logarithmic shift cancels the change of V, while its braiding term is invariant. This is a relation between classical actions with different V, not a microscopic symmetry selecting a numerical vacuum energy. An operator made from normalized u is invariant separately, so this transformation places no condition on its prefactor.

For example, -eta M^2 (a_mu a^mu)^(3/2)/h, with a_mu=u^nu nabla_nu u_mu, is an allowed invariant on the timelike-clock patch. On homogeneous FLRW a_mu=0; this term has a zero background and quadratic jet. Its coefficient is unconstrained by the transformation or those vacuum data. It is a response-operator illustration, not a proved stable UV completion. Adding it changes the local equations: (4)-(5) must not be presented as the screened solution of that enlarged theory. In particular, neither eta's observable mapping nor its radiative running is calculated here.

A genuine microscopic match would have to specify degrees of freedom and an action or exact identity that fixes h, alpha and any required response coefficient, compute their effective values, and demonstrate a healthy sourced MOND branch. None is supplied by this candidate's field rescaling. Choosing eta as a function of h or alpha by hand would reinstate the original free-normalization problem.

## 5. Verification and remaining obligations

check.py: 28/28 exact algebra checks pass, including the general-n radial current, stress reduction, de Sitter equations, sourced constant-X obstruction, density cancellation, both leading screened equations, asymptotic amplitudes, mass scaling and action rescaling. The separate sign/backreaction mutation fails 6/28 checks with nonzero exit as required. Contract and bounded-run manifests accompany both results. Symbolic identities check algebra; they do not constitute an independent physical derivation of an effective action.

No fit, parameter scan, measured a0, numerical kappa, global strong-field solve, local characteristic analysis, quantum calculation or UV matching was performed. This branch already fails the sourced MOND-law requirement in the controlled regime; local health alone would not repair that force law. The work narrows the next mechanism's burden: it must change the actual low-acceleration sourced equation and fix its normalization by a principle that constrains response operators, while preserving vacuum adjustment. The present rescaling does neither of those two jobs.
