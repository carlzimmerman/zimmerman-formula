# Constant-derivative self-tuning and the response selector

**Goal remains open: no microscopic symmetry or dynamics selecting a0 was found.** This continuation replaces the earlier rolling-X example by an explicit constant-X self-tuning vacuum with a positive scalar quadratic sector. It then tests the proposed derivative bridge and promotes its remaining coefficient to a variable. The result is a restricted nonselection statement, not a universal no-go.

Base 37608d6d403e219e996e02b21684f184779063b9; criteria-only commit f458ddcc26. Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate measurements, not inputs. All calculations use the dark-energy footing and symbolic parameters. No numerical kappa, target coefficient or option scan was performed.

## A different self-tuning background removes the rolling-X obstruction

The prior sol61_push/DERIVATIVE_BRIDGE_RESULTS.md tested a tadpole-driven state with exponentially rolling X. Here use a tadpole-free, shift-symmetric kinetic-gravity-braiding action

    S=int sqrt(-g)[M^2 R/2 - V + K(X)-G(X) box phi],
    X=-(dphi)^2/2>0,    phi_dot=sqrt(2X)>0.

M is the reduced Planck mass, V the bare vacuum energy density. In a flat homogeneous cosmology the shift current and scalar energy are

    J=sqrt(2X)K_X+6H X G_X,
    rho_phi=2X K_X-K+6H sqrt(2X) X G_X.

Require a self-tuning branch H=h with J=0 over an open X interval. This gives

    G_X=-K_X/[3h sqrt(2X)],
    J=sqrt(2X)K_X(1-H/h),
    rho_phi|H=h=-K,
    K(X_v)=V-3M^2 h^2.                                    (1)

For pure vacuum with constant V, an invertible K admits constant X_v. This is a real change from the previously tested rolling vacuum, not a rerun of its time-drift conclusion. However h appears in the action's relation between K and G. A background settling at h does not derive the value of h.

For n spatial dimensions the corresponding homogeneous current uses 2nHXG_X, and the self-tuning relation is G_X=-K_X/[n h sqrt(2X)], with vacuum density n(n-1)M^2h^2/2. The following perturbative-health formulas are specifically four-dimensional.

## An explicit stable scalar quadratic sector

At constant X on de Sitter, substitution into the standard KGB scalar-gradient and scalar-kinetic coefficients gives

    F=-K_X/3-X K_X^2/(9M^2h^2),
    Q=X K_X^2/(3M^2h^2).

Their ratio is the scalar sound speed squared. For

    K=-A log(X/Xref),    A>0,

one obtains

    X_v=Xref exp[(3M^2h^2-V)/A],
    F=A/(3X)[1-A/(3M^2h^2)],
    Q=A^2/(3M^2h^2X),
    c_s^2=M^2h^2/A-1/3.

Thus 0<A<3M^2h^2 gives positive scalar gradient and kinetic coefficients. The logarithm is regular on each positive-X patch. For example the additional subluminal condition would restrict A further; it would still give an interval and not a response normalization. No statement is made about a uniform cutoff across arbitrarily large vacuum shifts, full nonlinear stability or a realistic matter era. In particular the source warns that this tadpole-free self-tuning class can screen ordinary cosmic fluids as well; it is not being certified as viable cosmology.

## Direct derivative bridge: time independence is not joint selection

Take a trial shift-invariant response coefficient B(X)>0 multiplying a cubic acceleration operator, zero on the homogeneous vacuum. In a conditional static description with fixed source coupling and gravitational conversion, the acceleration scale is a0_bare=C/B(X_v), where C is independent of V and X. Differentiate (1):

    dX_v/dV=1/K_X,
    d ln a0_bare/dV=-B_X/(B K_X).                          (2)

The physical residual curvature 3h^2 remains fixed in this derivative. Thus a nonconstant B generally lets a0_bare depend on the vacuum energy that the background geometry canceled. If the same a0_bare is required for every V on an open self-tuning interval with K_X nonzero, B_X must vanish on its X image. This is a functional statement, not a scan.

For B=B0(X/Xref)^p in the logarithmic example,

    a0_bare=(C/B0) exp[p(V-3M^2h^2)/A],
    d ln a0_bare/dV=p/A.

The response is constant in time on each pure-vacuum background but changes between backgrounds with different bare V and identical H. Setting p=0 removes that sensitivity while leaving B0 independent of h.

Equation (2) is explicitly a bare-coefficient test. The cubic operator also contributes to the scalar current and lapse stress away from the vacuum. A sourced, screened galaxy can have X_local different from X_v, and its Newton/source dictionary can change. Those full equations have not been solved. Their existence is an open alternative, not an assumed rescue or an excluded possibility. The parent result already shows why inserting a derivative coefficient into an unchanged galaxy equation is invalid.

Allowing B(X,Theta), Theta=div u and u=-dphi/sqrt(2X), can evade X sensitivity through dependence on Theta alone. On the vacuum Theta=3h. But a multiplicative constant in B remains compatible with shift symmetry. A smooth coefficient times |acceleration|^3 has zero background value and zero first and second variations at zero acceleration. The vacuum equations and quadratic-health conditions therefore cannot determine that multiplier. This latter observation is inherited from the parent derivative-bridge work; it is not claimed as new. Higher-derivative health of such a portal is unproved.

## Making the coefficient dynamical instead of choosing it

For a regulated stationary sector let b multiply O3>=0 with I=int sqrt(-g) O3. A rigid freely varied coefficient without a potential or boundary term has

    S_b=-b I,    delta S/delta b=-I=0.

A nonzero halo with strictly positive I cannot obey that equation. With a potential W(b), writing Omega=int sqrt(-g), it becomes

    W'(b)=-I/Omega.

This introduces the function W and an environmental average, not a predicted universal value. This is a variational test, not the earlier numerical halo-filling-factor calculation, which was not rerun.

A local b with positive gradient energy evades the zero-integral constraint by carrying boundary flux. For the explicit static example Z laplacian b=O3, a localized source gives

    b(r)=b_infinity-Qsource/(4pi Zr)

outside a spherical source in three dimensions. The asymptotic normalization remains boundary data. The derivation, general dimension, finite-domain exception and positivity qualifications are in LOCAL_CONTINUATION.md. No full microscopic or sourced gravity completion is claimed.

## What changed and what remains

The constant-X construction removes the prior time-drift objection and has a demonstrably positive scalar quadratic sector in a specified interval. Nevertheless it does not derive the residual curvature scale or the galaxy response normalization. In the direct derivative bridge, self-tuning can transfer bare-vacuum sensitivity into the response. Treating the coefficient as a free variable either imposes a zero-response integral, needs a new potential, or exposes boundary data in the local example.

The original microscopic target remains beyond these results. A reopening must calculate the source response in a fully specified microscopic completion, or derive a potential/boundary rule and show why its normalization is fixed. Full local screening in the constant-X theory and additional symmetries remain untested. There is no justified claim that all microscopic theories fail, or that EFT parameter counting alone proves impossibility. The established routes do not supply a mechanism to present as a solution.

## Evidence and review

check.py verifies 17 exact identities. run/ completed successfully. run_MUTATE/ reverses the braiding and response chain-rule signs and fails as expected. Both artifacts have validated bounded-run manifests. The generic functional argument, dimensional generalization and local boundary-value example are analytic derivations; they are not established by finite numerical sampling. Self-review only.

Self-audit checked positive-phi_dot and X domain, fixed versus residual vacuum energies, scalar kinetic versus gradient coefficients, restored Planck factors, source-coupling assumptions, and exceptions to the regulated positive-integral argument. Passing scalar vacuum checks is not a health result for the proposed response portal. No complete microscopic matching or independent review exists.

Campaign screens: scripts contain no target acceleration values. No numerical kappa is output, so its rename/scaling/pi-weight/significance tests are inapplicable rather than passed. Natural-unit source formulas introduce no horizon-entropy coefficient. Global-sequestering and Coleman-Weinberg ideas were screened against prior records and were not relabeled as new attempts.
