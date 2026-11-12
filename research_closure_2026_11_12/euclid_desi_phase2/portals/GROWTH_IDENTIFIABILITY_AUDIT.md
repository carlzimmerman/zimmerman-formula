# Conditional growth closure breaks the background matter-split ambiguity

12 November 2026. Independent analytic audit of the coordinator's proposed extra observable. No ODE/data fit, numerical growth pass, or DESI significance is claimed.

## Exact result and assumptions

Let x=ln a, primes denote d/dx, F=(H rd/c)^2>0, and A_m be the constant conserved pressureless matter coefficient in F. Adopt the **same** subhorizon GR linear-growth closure in each portal: constant G_cosm, pressureless clustering matter, and all other dark energy smooth on the scales tested, with negligible radiation/other clustering-source corrections in the interval. Then

    D''+[2+F'/(2F)]D' - [3 A_m a^-3/(2F)]D=0.

This equation is an added physical perturbation hypothesis. It does not follow from either a0 portal or from the background Friedmann equation alone. In particular a sector containing a dust-shaped background contribution need not share pressureless-matter perturbations: its sound speed and stress must be specified.

Suppose two interpretations of the same F have D1=c D2 for nonzero constant c throughout an open interval and D2 not identically zero. Divide one equation by c and subtract: [3a^-3/(2F)](A_m1-A_m2)D2=0. Therefore A_m1=A_m2. The fixed-coefficient density/potential family with different A_m cannot have the same complete growth shape under this common closure.

The inverse is

    A_m = (2 F a^3/(3D)) [D''+(2+F'/(2F))D'].

It cancels arbitrary multiplicative normalization of D. Since F is directly dimensionless BAO information, evaluating the combination does not require assigning numerical H0 or rd. It reconstructs the dimensionless coefficient A_m, not an absolute mass density. A nonconstant inferred A_m tests the combined closure/measurement assumptions rather than uniquely one portal.

For logarithmic growth rate f=D'/D,

    A_m=(2Fa^3/3)[f'+f²+(2+F'/(2F))f].

## Continuous f-sigma8 shape: stronger result, higher derivative cost

RSD f sigma8 is proportional to D', not directly D or f. Consequently the displayed D inverse cannot be applied to f sigma8 samples by replacing D with that observable. Integrating D' introduces an additive integration constant; arbitrary normalization is a different freedom.

Nevertheless that additive freedom does not preserve exact equivalence when both full ODEs are imposed on an interval with nonzero growth. Define a continuous observed derivative shape W=N D' with unknown constant N, B=2+F'/(2F), and K=3a^-3/(2F). The growth equation gives

    R=(W'+B W)/K=N A_m D,
    R'=A_m W,
    A_m=R'/W.

The last expression eliminates the unknown normalization and additive constant but needs W'' as well as the background derivatives. Alternatively, equal W shape implies D1=cD2+d; the two ODEs give (A_m1-A_m2)D2=A_m1*d/c (up to the chosen offset convention), whose derivative forces equal A_m wherever D2' is nonzero. The zero-growth branch cannot be used as an informative RSD shape.

Thus exact sufficiently smooth continuous f sigma8 data can also distinguish the matter splits under the closure. A few noisy correlated finite bins do not provide these derivatives without a latent function/dynamics model, measurement windows and priors. Neither the inverse formula nor the proof is a calibrated DESI f sigma8 test. Normalized shape information, amplitude freedom, bias calibration and integration constants must be handled in the actual observable likelihood.

## Explicit local witness for the proposed synthetic background

Take F=.7+.3u³, Q=.7/C+.05u³/C, A_density=.25, A_potential=.20 and C=32pi/3. These are the same-coefficient background-degenerate branches from the fixed-coefficient addendum. At a=1, F=1. If their growing solutions are initialized to the same D=1 and same D', their second derivatives differ by

    D_density''-D_potential''
      =3(.25-.20)/(2*1)=.075.

That is an exact equation-level curvature separation, not a propagated numerical forecast or an assertion about real RSD errors. Their solutions cannot remain identical up to constant amplitude on an interval under the common closure. Initial/boundary conditions and decaying-mode admixture still matter for an actual finite-window comparison.

## How the ambiguity returns

If growth uses an unspecified effective coupling mu(a,k), the source is proportional to mu A_m. Choosing mu_2=mu_1 A_m1/A_m2 preserves it when other terms are held fixed. A free clustering dark-energy perturbation or stress source can likewise compensate the matter split. Lensing may constrain additional combinations only after its slip/coupling response is specified. Therefore this result identifies A_m **within a fixed source closure**, not matter in a theory-independent way.

For a complete candidate, common gravitational coupling, smooth-sector approximation, scale range, initial perturbations and source covariance must be justified from its parent action. The report's background equivalence remains an exact no-go for h and q alone; adding a genuine independently constrained growth response can break it conditionally. No existing coupled-action health failure or prior NO VERDICT row is overturned.

## Derivative-free third-observable null with a free initial-growth product

Define x0 as one reference epoch within the observed interval and take Y(x)=f sigma8(x) proportional to D'(x) with one unknown constant amplitude. Let

    p(x)=a² sqrt(F),
    w(x)=(3/2)a^-1/sqrt(F),
    J(x)=∫_(x0)^x Y(t) dt,
    I0(x)=∫_(x0)^x w(s) ds,
    I1(x)=∫_(x0)^x w(s) J(s) ds,
    L(x)=p(x)Y(x)-p(x0)Y(x0).

Since p'/p=B and p b=w, the linear-growth equation gives

    L(x)=C0 I0(x)+A_m I1(x),
    C0=A_m D_scaled(x0).

Here D_scaled'=Y, so C0 is a free product of matter amplitude and initial growth normalization. It need not be calibrated independently. Two independent endpoint rows determine C0 and A_m; three rows give the derivative-free null det[L,I0,I1]=0. Absolute Y normalization cancels from the inferred A_m: L and I1 rescale together, while C0 absorbs the rescaled initial amplitude.

For continuous Y>0 and w>0, two nested nonzero intervals x0<x1<x2 have positive determinant I0(x1)I1(x2)-I0(x2)I1(x1). Indeed I1/I0 is the positive-weight average of the strictly increasing J, and strictly increases as the upper endpoint increases. This is an exact rank statement under the positivity assumptions; narrow intervals or slow growth can still make it poorly conditioned. With sign-changing Y, non-nested design or weak interval information, rank must be checked rather than assumed.

This construction avoids differentiating noisy RSD data, but needs Y and F throughout the intervals. Endpoint values alone do not determine I0,I1; a between-bin latent model or window-integrated measurement description is still required. Adjacent/nested rows share endpoints and integral modes, so their covariance is strongly correlated. RSD galaxy-bias mapping, Alcock-Paczynski/fiducial conversion, nonlinear/velocity modelling and scale-dependent growth assumptions determine whether the released f sigma8 really supplies one common-normalization Y. These inputs and BAO cross-covariance belong in a joint observable likelihood, not in a detached determinant-error estimate.

## Exact symbolic checks and preserved verdicts

`growth_contract.json` froze the finite assertion before execution. `growth_checks.py` verifies 12 symbolic statements, including the generic integrating-factor equation, the derivative-shape inverse, and an exact normalized EdS toy F=a^-3,D=N a,Y=N a on endpoints a=2,4 from reference a=1. In that toy,

    I0=3(sqrt(a)-1),
    I1=N[a^(3/2)-3sqrt(a)+2],
    L=N[a^(3/2)-1].

The two-row inverse returns A_m=1 and C0=N for arbitrary N>0; determinant N(15sqrt(2)-18)>0. These are analytic synthetic checks, not data agreement or a realistic survey forecast. All 12 checks pass in `growth_run01/results.json`; manifest status completed and installed validation passes.

Nothing here changes the repository's existing f sigma8/growth NO VERDICT records or converts a proxy estimate into a data pass. In particular `closure_2026_11_11/FINAL4_growth_history/RESULT.md` preserves the absolute C3 row as NO VERDICT, and other growth lanes have their own failed known-answer qualifiers. This addendum supplies a defined conditional third observable, not a regrade of those computations.
