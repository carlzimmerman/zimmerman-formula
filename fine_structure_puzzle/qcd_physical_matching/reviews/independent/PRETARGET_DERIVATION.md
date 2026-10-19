# Independent critical derivations before author targets

Reviewer: isolated subagent `/root/physical_independent_review`, 2026-10-19.
This file was written before opening the author's derivations, reports, code,
contracts, or outputs. The task supplied the raw lattice input and source paths.
The only scientific documents opened so far are Can et al. 2501.08619v2 and
Walker-Loud et al. 1203.0254v2, supplied in `/tmp/fsp006_proton_sources`.
Input hashes and raw numerical reconstruction are in `PRETARGET_NUMERICS.json`.
This is an independent derivation, not a theorem about QCD limits.

## A. Spin-averaged Cottingham subtraction coefficient

Use canonical alpha=e^2/(4 pi), with e factored out of both vector currents.
The spin average belongs inside T: (i/2) sum_s integral <p,s|T JJ|p,s>.
With relativistic external-state normalization, the Cottingham prefactor after
Wick rotation is e^2/(4 M) times the Euclidean four-momentum measure
d^4Q/(2 pi)^4 and 1/Q^2. This includes the electromagnetic quadratic-action
factor 1/2 and external-state factor 1/(2M).

Contracting (-g_mn+q_m q_n/q^2) S1(Q^2) gives -3 S1. Angular integration uses
the area 2 pi^2 of the unit three-sphere, so

    integral d^4Q/(2pi)^4 * S1(Q^2)/Q^2
      = (1/(16pi^2)) integral dQ^2 S1(Q^2).

Consequently

    delta M_sub = -3 e^2/(64 pi^2 M) integral dQ^2 S1(Q^2),
    (partial_(e^2) M)_sub/M
      = -3/(64 pi^2 M^2) integral dQ^2 S1(Q^2).

The result is a leading-QED subtraction contribution evaluated with the QCD
mass and current correlator held fixed. It is not the entire mass response.
The trace sign is essential; a positive subtraction function gives a negative
subtraction contribution in these tensor conventions. Walker Eq. (13) gives
-3 alpha/(16 pi M), equivalent to the coefficient above. Its Eq. (2) explicitly
spin averages, and Eqs. (3), (6), (7a) support the prefactor, angular integral,
and trace sign. Can Eq. (3) has the same T1 transverse tensor despite its
different normalization of the T2 tensor; Eq. (5) identifies S1=T1(0,Q^2).

For lattice momenta Q=(2pi/(N_L a)) n, lattice spacing cancels exactly:

    I/M^2 = (2pi/(N_L aM))^2
            sum_i (n_(i+1)^2-n_i^2)(S_i+S_(i+1))/2.

Can Table I gives N_L=48, aM=.3860 at kappa=.122005, beta=5.65.
Table II gives vectors (3,1,0), (3,2,0), (4,2,0), (5,3,0), (7,1,0),
(7,4,0), hence squared norms 10,13,20,34,50,65. Table III gives
S=.688,.596,.208,.080,.136,.135 in this order. These are an O(a)-improved
connected-current lattice estimate, at m_pi about 410 MeV and one spacing;
they do not specify the physical continuum, low-Q, UV, or disconnected pieces.

The five trapezoid pieces in squared integer momentum are 1.926, 2.814,
2.016, 1.728, 2.0325. Their sum is 10.5165. Thus

    I/M^2 = 1.2094109009924046,
    (partial_(e^2) M)_sub/M = -0.005744012999929529.

Differentiating alpha instead gives -0.0721813961708115. A factor 4pi
distinguishes the derivatives. Rounded Q^2 in GeV^2 must not replace exact
lattice norms if claiming exact lattice-spacing cancellation. Trapezoidal
interpolation is a declared model between samples, not continuum quadrature
error control. The public table does not provide cross-momentum covariance.

## B. Finite-volume mass matching and metric differentiation

Take the supplied leading charged-hadron finite-volume shift

    delta m(L)=alpha Q_h^2 c1/(2L)=e^2 k/L,
    k=Q_h^2 c1/(8pi).

Here c1 has whatever sign the source convention assigns; in the usual QED_L
convention c1 is negative. The formula alone does not define every QED finite
volume prescription. Consider the explicit flat model

    m(L,e^2,Lambda)=kappa Lambda+e^2 k/L,
    rho(Lambda)=C Lambda^4,  kappa nonzero.

At fixed mass m*, implicit differentiation gives

    Lambda(L,e^2)=(m*-e^2 k/L)/kappa,
    partial_(e^2) Lambda|m*,L=-k/(kappa L),
    d rho/d(e^2)|m*,L=-4 C Lambda^3 k/(kappa L).

For L=zeta/H this response is linear in H to leading order, with coefficient
-4 C Lambda_0^3 k/(kappa zeta). At fixed Lambda the direct e^2 derivative of
this rho is identically zero. The nonzero path response is a scale-retuning
effect, although it occurs in a perfectly flat-vacuum model. With realistic
mass dependence replace kappa by partial_Lambda m and include all other
retuned parameters in the chain rule. Neither a single mass constraint nor a
nonzero partial_Lambda m determines an entire many-parameter matching path.

The metric stress tensor is a partial derivative with renormalized parameters
held fixed. On a round four-sphere V=v H^-4, define W=-log Z and

    rho_metric(H,lambda)=-H/(4V) partial_H W(H,lambda).

Along lambda=lambda(H), differentiating the composed W additionally gives
-H/(4V) sum_i W_i lambda_i'(H). These are generally different operations.
For W=V rho(lambda(H)), with rho(lambda(H))=rho0+A H+..., the fixed-parameter
metric density evaluated on the path is rho0+A H+..., while differentiating
the composed W gives rho0+(3/4) A H+.... This explicit 3/4 factor diagnoses a
possible confusion between a parameter path and a metric variation.

## C. Radius operators from powers alone

Let D=H d/dH. D H^p=p H^p. The differential operator

    P_full(D)=D(D-1)(D-2)(D-4)

kills density powers H^0,H^1,H^2,H^4. To retain the linear term and eliminate
H^0,H^2,H^4 instead, use

    A_rho(H)=D(D-2)(D-4) rho(H)/(3H).

For a finite linear combination of precisely those four powers, A_rho is
exactly the H coefficient at every positive H. This says nothing about whether
a QCD density has that expansion or whether remainder derivatives vanish.

Do not identify W=V rho away from a constant density action: the defining metric relation is
rho=-H^4 D W/(4v). Therefore a metric density term rho1 H requires
W_(H^-3)=(4v/3)rho1 H^-3. This distinction matters for normalization.
Under that metric relation W powers H^-4,H^-3,H^-2,1 and log H map to density
powers H^0,H^1,H^2,zero,H^4, respectively. To kill all these W terms use

    Q_full(D)=D^2(D+2)(D+3)(D+4).

The double zero at D=0 is needed because D log H=1. To retain H^-3 only,
Q(D)=D^2(D+2)(D+4) has eigenvalue -9 at p=-3. Thus the metric-density
coefficient is -H^3 Q(D)W/(12v); if the target is merely the W coefficient,
its extractor is -H^3 Q(D)W/9.

There are exact finite-difference analogues. For r>0, r!=1, let E f(H)=f(rH).
Replace a root p by E-r^p, and retain a repeated root for log H:

    rho full: (E-1)(E-r)(E-r^2)(E-r^4),
    W full: (E-r^-4)(E-r^-3)(E-r^-2)(E-1)^2.

The four-point density extractor is

    [(E-1)(E-r^2)(E-r^4)rho]/
       [H (r-1)(r-r^2)(r-r^4)].

The five-point W extractor of its H^-3 coefficient is

    H^3 [(E-r^-4)(E-r^-2)(E-1)^2 W]/
       [(r^-3-r^-4)(r^-3-r^-2)(r^-3-1)^2].

Multiply that W extractor by 3/(4v) to obtain the metric-density linear
coefficient. These identities hold for arbitrary positive H and arbitrary
coefficients in the stated finite spans. They do not prove a continuum,
infinite-volume, infinite-radius, or differentiable-asymptotic expansion.

## Source authentication boundary

The supplied PDFs' first pages visibly identify arXiv versions v2 and dates
21 May 2025 / 3 June 2012. Exact byte hashes were recorded. arXiv's public
2501.08619v2 abstract page independently confirms the title, author list,
version date, and journal DOI (10.1103/PhysRevD.111.094513). Initial web fetch
of the Walker version abstract failed; local version text and Eq. (13) were
read directly. This does not claim a redownloaded-byte identity.
