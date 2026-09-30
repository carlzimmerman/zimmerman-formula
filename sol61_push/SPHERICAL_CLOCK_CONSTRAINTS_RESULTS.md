# Necessary spherical matching equations

Base cb99427a8af9252f76190c60f30aa5dc5898c6cd; own preceding checkpoint b65b39182. Verdict: the equations and identities below are exact necessary stationary spherical equations for the stated local kappa=0 action. Their benchmark and weak-expansion checks pass. No sourced global solution or exact 32π selection is established. This is self-review.

## Common geometry and action

Use c=hbar=1 and the variable-clock action with M²=1/(8πG), canonical coefficient Z>0, U=A/q²+Bq², lambda=1+ell q, and cubic coefficient K_c. Set the R3² stabilizer to zero for this calculation and omit the nonlocal fermion response. This is a specified local action branch, not a causal or ultraviolet completion.

In stationary areal-radius coordinates write

    ds²=−N(r)²dt²+exp(2sigma(r))[dr+V(r)dt]²+r²dOmega².

N is positive, q is positive, and the outward polarization branch has P>=0. Define

    F=V'+V sigma',  W=V/r,  T=F+2W,
    K_trace=−T/N,
    Q_K=F²+2W²−lambda T²,
    R3=2[1−exp(−2sigma)]/r²+4exp(−2sigma)sigma'/r.

The reduced action per unit solid angle is

    Lr=(M²/2)r²exp(sigma)Q_K/N
       +(M²/2)r²N exp(sigma)R3
       +2M²r²P N'
       −r²N exp(sigma)[M²P²+K_c qP³+U]
       +(Z/2)r²exp(sigma)V²(q')²/N
       −(Z/2)r²N exp(−sigma)(q')².

The V²(q')² term is essential: a scalar stationary in areal coordinates is not stationary along a flowing preferred normal. Integrating the R3 term by parts leaves M²N[exp(sigma)+exp(−sigma)]+2M²rN'exp(−sigma), with boundary −2M²rN exp(−sigma).

Areal gauge and stationarity are imposed before variation. A complete covariant solution must also check angular/Bianchi equations, source conservation and global foliation boundary conditions; those have not been independently completed here.

## Exact vacuum equations

Let J=F−lambda T. Shift variation gives

    J'+(2/r−N'/N)J−2(W−lambda T)/r
       −(Z/M²)V(q')²=0.

The lapse equation is

    −M²Q_K/(2N²)+(M²/2)R3
    −2M²exp(−sigma)(P'+2P/r)
    −M²P²−K_c qP³−U
    −(Z/2)[exp(−2sigma)+V²/N²](q')²=0.

Polarization variation gives the proper clock acceleration law

    a_clock=exp(−sigma)N'/N=P+3K_c qP²/(2M²).

Scalar variation gives

    Z/[r²N exp(sigma)]
      × d{r²N exp(−sigma)[1−exp(2sigma)V²/N²]q'}/dr
      =U'+K_c P³+(M²/2)ell T²/N².

The curvature-dependent scalar force is consequently determined by the actual clock trace. Replacing it by the constant (9/2)M²H²ell is an approximation requiring a matching calculation.

Combining radial metric variation with V times shift variation eliminates their second radial derivative combination. Subtracting that combination from the lapse equation yields the exact identity

    sigma'+N'/N
      =r exp(sigma)(P'+2P/r)+(Zr/(2M²))(q')².

This displays scalar gradient stress and the polarization contribution. It is not, by itself, a complete Gauss law: the separate radial metric equation and other scalar/potential contributions must also be solved. It supplies an equation that the earlier prescribed-flux scalar BVP did not enforce.

## Two controls and one excluded shortcut

For N=1, sigma=0, V=−Hr, P=0 and q=q*, the equations give exactly the previous de Sitter vacuum relations. The script chooses positive A,B from those relations and checks lapse, shift, radial metric, scalar and polarization equations separately.

As a GR control, set ell=0 and use

    N=1, sigma=0, V=−sqrt(H²r²+2m/r), q=q*, P=0,
    U=3M²H², U'=0.

The four differential metric/scalar equations vanish for arbitrary positive m. This directly verifies the mass-containing control in the same radial conventions; it is not imported as a solution at nonzero ell.

For ell>0, the same mass-containing shift has momentum residual

    −9ell m²q*/[r^(5/2)(H²r³+2m)^(3/2)],

which is nonzero for m>0. More generally, if N=1, sigma=0, q=q* and P=0 are held fixed, shift variation requires

    V''+2V'/r−2V/r²=0.

Matching the expanding cosmological branch gives V=−Hr+C_shift/r². The lapse residual is then −3M²C_shift²/r⁶, forcing C_shift=0 in vacuum. Thus the unit-lapse, flat-spatial, constant-scalar shortcut cannot carry a mass exterior for this nonzero-ell branch. Nontrivial N, sigma or q may repair it; this does not exclude spherical solutions of the theory.

## Weak clock feedback and its boundary constant

Expand N=1+Phi, sigma=Psi, V=−Hr+w and q=q*+u to first order about the vacuum. Define B_lambda=ell q*. The trace perturbation is

    deltaK=−w'−2w/r+Hr Psi'−3H Phi.

The vacuum shift constraint becomes

    B_lambda(deltaK)'=2H(Phi+Psi)'−3H ell u',

or

    B_lambda deltaK=2H(Phi+Psi)−3H ell u+C_clock.

C_clock is a radial integration constant. It cannot be discarded before specifying and solving the source and cosmological boundary conditions. It changes the scalar's local force even when the acceleration gradient is small.

At strictly linear order about P=0, the scalar equation uses the stationary de Sitter radial operator

    Z[(1−H²r²)u''+(2/r−4H²r)u']
      =m_static² Z u+[6M²H²ell/B_lambda](Phi+Psi)
        +[3M²H ell/B_lambda]C_clock,
    m_static² Z=U''−9M²H²ell²/B_lambda.

Using the vacuum equation, the mass numerator equals 2A/q*⁴+6B>0. It agrees with the independently derived mass floor in VARIABLE_CLOCK_MODES_RESULTS.md. The frozen-curvature scalar BVP instead used U''/Z and did not include the metric and boundary-constant forces. The cubic K_c P³ enters at a higher perturbative order; inserting it alongside a full-field source law requires an explicit weak-field ordering and nonlinear matching audit. In particular, the earlier small-Z profile with a 98% scalar change is not covered by this linear u expansion.

## A stationary source still has a clock-frame current

For a prescribed set of particles stationary at fixed areal radius, let mu(r)=(dM/dr)/(4π) denote rest-mass count per radial coordinate and unit solid angle. Their source term is

    L_m=−mu sqrt(F_metric),
    F_metric=N²−exp(2sigma)V²>0.

Its lapse and shift variations are −mu N/sqrt(F_metric) and +mu exp(2sigma)V/sqrt(F_metric). The radial-metric-minus-V-shift source combination cancels for these stationary particle trajectories. The exact gradient identity acquires the additional term

    mu N exp(sigma)/[2M²r sqrt(F_metric)].

The shift equation becomes its vacuum left side equal to mu N exp(sigma)V/[M²r²sqrt(F_metric)]. On the cosmological background this current is −mu H/[M²r sqrt(1−H²r²)], rather than zero. Setting coordinate velocities to zero does not set the preferred-frame momentum density to zero.

These worldlines need support stresses to remain stationary. The prescribed source term checks the couplings and frame dictionary; it does not provide a conserved self-gravitating matter model. A complete supported source or equilibrium fluid must supply the required stresses. The equations must not be solved with a density inserted only into the lapse constraint and the source current silently omitted.

## Orbit dictionary and the radius question

The same F_metric is the stationary Killing norm. For a timelike circular geodesic where F_metric>0 and F_metric'>0,

    Omega²=F_metric'/(2r),
    v_c²=r F_metric'/(2F_metric),
    g_orbit=v_c²/r=F_metric'/(2F_metric).

This is an observable circular-orbit dictionary in areal radius, not automatically a_clock. In the GR mass control a_clock=0 but g_orbit=(m/r²−H²r)/(1−H²r²−2m/r). A shift can carry gravitational response. In the static zero-shift weak-metric limit the dictionaries agree to the appropriate spatial-metric accuracy; that limit must be justified for the selected clock solution before assigning the cubic coefficient to observed a0.

For the actual mass-free vacuum, F_metric=1−H²r². Its metric cosmological horizon is r_h=1/H and its geometric Lambda=3H², so r_h²Lambda=3. This model does not give 8π for that horizon. No universal preferred-mode signal horizon is established by this metric calculation.

If instead one defines a density length r_U²=1/(G U), the same action gives r_U²Lambda=16π/S*. With a local Newton calibration G_N, the length 1/sqrt(G_N U) gives 8π G_cosm/G_N, since G_cosm=2G/S*. An 8π density identity therefore assumes a coupling equality or uses a geometrically defined effective density. Calling that length a horizon does not establish either claim and does not select 32π.

## Evidence and next action

spherical_clock_constraints.py passes 30 exact symbolic checks: the curvature boundary, six variational reductions/constraint identities, five vacuum benchmarks, four GR mass benchmarks, the excluded fixed-lapse shortcut, weak clock feedback and mass floor, three stationary-source couplings plus their current/constraint dictionary, and three orbital checks. The bounded run and hashes are in runs/spherical_clock_constraints. SciSpace was used for discovery of related spherical-foliation work; no abstract supplied a proof leaf and no novelty claim is made.

The previous scalar-only BVP remains a declared diagnostic rather than a completed theory solution. Its clock trace, prescribed bare flux and orbit dictionary are now explicit matching obligations. The next executable route is a coupled radial boundary solve with a conserved compact source, the scalar gradient stress, and cosmological clock data. A full solution must check the remaining angular/Bianchi conditions and identify the actual observed Newton and acceleration scales. Nonlocal response, causal completion, microscopic parameter selection and exact 32π remain unresolved.
