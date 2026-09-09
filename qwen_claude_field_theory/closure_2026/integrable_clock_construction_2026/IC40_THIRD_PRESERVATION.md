# IC40: third-time preservation of the finite-order activation variant

Base 4f1722faa4a801d2155e23e9a78373574c86a648. Full gravity goal OPEN.
The preceding goal turn made progress: IC39 changed the explicit pin potential
and derived a conditional finite second response. That is not time evolution.
Carl Zimmerman's exponential kernel, vacuum scale and primordial-clock direction
remain the scientific starting point; L44's finite-order activation suggestion
is credited in IC39. Preserve all previous constructions and evidence.

## Bounded design and execution plan

Keep IC39's explicit eta4 action, its fixed coefficient and minimally coupled
fluids. Read IC37's selected initial rates as candidate data, not exact roots.

1. Test and derive the third time derivative of the pin equation, including
   a moving activation face. A stationary-face replacement is not allowed.
2. Build bivariate local Taylor jets: the IC35 spatial initial-data ODE,
   independently varied IC33 physical metric flows, and canonical fluid flows.
   Determine second lapse jets from IC37, not from an assigned field equation.
3. Compute third metric/fluid time jets from those flows. Use the actual lapse
   operator to solve for S_ttt, then independently test the w equation. Boundary
   motion supplies a specific cubic term; it is not a free repair parameter.
4. Compare two working precisions and spatial truncation orders; check the
   computed lower time jets against frozen IC37. Run all created scripts and
   relevant closure tests, preserve raw evidence and report scope honestly.

## Moving-face obligation

Let eta=eta4(x), x=alpha^2-1/2 and W+eta exp(S)ell=0. At ell=ell_t=0 put
E=W_tt, L=ell_tt and B=ell_ttt. Differentiation gives

    W_ttt+eta exp(S) B+3 exp(S)(eta_t+eta S_t)L=0.

Since E=-eta exp(S)L, the residual that must be O(eta) is

    W_ttt-3(eta_t/eta+S_t)E.

Use the undivided equation or its analytic asymptotic near x=0. Assume a
regular face x=a delta+o(delta), a=x_r>0; x_t is fixed by the physical q flow
on the pinned side, and its coordinate speed is R_t=-x_t/a. If E begins at
fourth order with derivative E4, bounded B requires

    W_ttt(0)=partial_r W_ttt(0)=partial_r^2 W_ttt(0)=0,
    partial_r^3 W_ttt(0)=3 E4 x_t/a=-3 E4 R_t.

All four equalities are exact necessary conditions, not claims established by
rounded root data. The earlier conditional finite L limit alone supplies none
of the independent third metric/fluid accelerations.

## Canonical fluid truncation justified for this time order

For each constant barotropic index w_f, the initial spatial gradient g is zero.
At fixed pinned w and physical spatial metric exp(2Q), use

    H(j,k)=c j^(1+w_f)+j k/(2 v0)+O(k^2),
    v0=(1+w_f)c j^w_f, k=exp(-2Q)g^2.

Because g=O(t), the omitted energy terms are O(t^4). They do not affect the
third constraint derivative or the second derivative of the physical metric
flows. Retain the O(g^2) pressure and anisotropic stress and the canonical
flux. This is not permission to freeze ordinary matter or use this truncation
at finite gradient in nonlinear evolution.
