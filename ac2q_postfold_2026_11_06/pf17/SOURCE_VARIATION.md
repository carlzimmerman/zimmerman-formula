# Native source variation for continuous BV clock gradients

This is an a priori result for an existing native solution, not an existence
construction. It restricts PF13 to continuous p=d phi in spacetime BV. Retain
jointly Lipschitz phi,A,Pi, compact positive-clock, cap, hyperbolic and
on-branch margins, g in C1 intersect W2,1, and the full Einstein equations.
Assume a regular periodic clock foliation with controlled proper length and
the positive b,c margins of PF08's curved auxiliary inverse. All conclusions
below concern almost every clock slice. Continuous spacetime p is stronger
than merely vanishing BV jump part and is not derived here from incoming data.

## 1. Differentiate forms before expanding

Let tau=phi. Timelikeness and continuity of p give C1 local clock charts with
bounded inverse Jacobian. Since d phi=-r n_flat and e_flat(e)=1,

    dA=u d phi+(W_P/r)e_flat,       u=n(A)/r,
    dP=v d phi+(D-2P E_beta)e_flat, v=n(P)/r.

Here n_flat,e_flat are the metric dual one-forms, not differentiated frame
operators. P=exp(-2beta)Pi is Lipschitz. The rates u,v initially are bounded
measurable functions, not presumed differentiable or continuous. The other
one-form coefficients in these equations are continuous BV. In particular
B=n(beta), E_beta=e(beta) are continuous BV because p is continuous BV and
g is C1 intersect W2,1.

Taking exterior derivatives first gives

    d(u d phi)=-d[(W_P/r)e_flat],
    d(v d phi)=-d[(D-2P E_beta)e_flat].                 (1)

In a clock chart the left sides are spatial distributional derivatives of
u,v times the coordinate area form. The right sides are Radon measures.
This establishes slice BV for u,v before applying a chain rule involving
these rates. It does not multiply an arbitrary L-infinity rate by a singular
clock derivative. Exterior derivatives and their pullbacks here can be
verified weakly by change of variables in tests in the C1 clock chart.

One must then simplify the right sides using the scalar and compatibility
measure equations and the mixed Einstein equation. Expanding (1) instead of
differentiating u=nA/r term by term gives the corrected PF08 equations

    e(u)=a u+b v+f K+f0,
    e(v)=c u+(-a-2E_beta)v+g_tilde K+j e(r)+g0,        (2)

with K=e(theta)+omega(e). The coefficient definitions and signs are exactly
those in pf08/principal_review/CURVED_COERCIVITY.md. The quantities multiplying
K or e(r) are continuous. Products of bounded rates u,v with a,b,c and the
bounded remainder coefficients are ordinary volume densities. In particular
no u D^c r or v D^c theta product remains. The cancellation is already built
into d(u d phi), not obtained by assigning representatives to such products.

The mixed and normal Einstein equations likewise give slice measure identities

    e(B)=(K-B)E_beta,
    e(E_beta)=K B+(B^2-3E_beta^2)/2-T_nn/(2M).        (3)

Continuous coefficients and algebraic bounded stress make their right sides
well-defined. The full equations, rather than a prescribed metric, supply (3).

## 2. Inverting the measure-forced spatial system

The positive weighted periodic inverse used in PF08 extends from integrable
forcing to finite Radon-measure forcing: variation of constants uses the
Stieltjes integral of the fundamental matrix against that forcing. Uniform
bounded coefficients and the same separation of the periodic monodromy from
one give its L-infinity bound by the forcing total variation. This requires
no derivatives of the coefficient matrix.

Applying it to (2), with the compact length/geometry/positivity bounds, gives

    ||u,v||_infinity <= C(1+TV(r)+TV(theta)) <= C(1+Z),

where Z is the sum of the slice total variations of the two covariant Riemann
gradients W_sigma=e(z_sigma)+omega(e). Their invertible linear dependence on
e(r),e(theta), with bounded e(A) and connection terms, gives the last bound.
Equation (2) also bounds slice TV(u,v) by C(1+Z). In this continuous-clock
subclass the forcing has no slice atoms, so the slice BV representatives
of u,v are continuous. No time continuity of u,v is asserted.

## 3. Variation of the actual characteristic source

The exact F_sigma of PF08 depends on r,A,P,B,u,v, with compact locally
Lipschitz coefficients; the native hold law's C1 W_P is sufficient. Use (2),
(3), e(A)=W_P/r and e(P)=D-2P E_beta in its slice BV chain rule. This yields

    |D_ell F_sigma|
      <= C(1+||u,v||_infinity)
              [d ell+|D_ell r|+|K|].                (4)

Here K includes its connection density, and D_ell denotes the spatial measure
derivative on the proper clock slice. Thus the integral of the right side is
at most C(1+Z)^2. The same bound controls the acceleration-source term
F_sigma a_n, with a_n=-e(r)/r, since the slice F_sigma representative is
continuous and bounded. Base curvature is bounded by the native Einstein
identity in PF08. Consequently the source in the signed gradient equation
has a controlled slice measure norm C(1+Z)^2.

For the actual rolling law W(P,phi), put Zpot=V_phi+W_phi. The PF09
potential calculation gives the explicit additions

    delta f0=W_P Zpot/(r^3 R)+W_Pphi/r,
    delta g0=-D_r Zpot/(r R),
    delta F_sigma=-sigma Zpot/(r c R).

The inverse matrix and singular-gradient coefficients are unchanged. On a
compact positive clock interval with positive C2 V,a0, bounded derivatives,
fixed gamma and cap separation, these terms and their needed slice state
derivatives are bounded. Since e(phi)=0, no extra clock derivative enters
the spatial chain rule. Thus (4) covers the regular native rolling potential
under PF09's explicit assumptions, not only the constant-potential subfamily.
No statement covers a potential zero, pole or loss of cap separation.

## 4. Remaining gap

Equation (4) addresses source variation in this continuous subclass. It does
not turn the signed gradient equation into an inequality for |W_sigma|.
To conclude Z(t)<=Z(0)+C integral_0^t(1+Z)^2, one still needs a valid native
renormalization/interaction argument. The exact-gradient countertest in this
phase shows that continuity and gradient structure alone do not supply it.
Nor does the present a priori proof construct a sequence with uniformly
bounded Z or show preservation of its compact/continuous hypotheses.
