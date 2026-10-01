# A necessary constitutive variable for the P2 fluid family

This derivation concerns the unshifted point-baryon pressure postulate in CFG2. It neither assumes a general dark-fluid action nor excludes every possible completion.

Let y=GM_b/(a0 r²)>0. The established hydrostatic profile has

    M_total = M_b sqrt(1+1/y),
    rho_d = C_M y/sqrt(1+y),
    C_M = a0^(3/2)/(4 pi G^(3/2) sqrt(M_b)),
    P = a0² y/(8 pi G).

The map y/sqrt(1+y) is strictly increasing. At the same positive dark density, increasing M_b increases y and therefore P. Consequently **one single-valued universal barotropic law P=P(rho_d), with fixed a0 and no other state variable, cannot produce this entire equilibrium family**. The conclusion follows algebraically; the two-mass calculation supplies a finite implementation control. This is narrower than a no-go theorem for dark matter or for a baryon-coupled action.

A conditional per-host constitutive law can be written explicitly. Put q=rho_d/C_M; then

    y(q) = [q²+q sqrt(q²+4)]/2,
    P(rho_d;M_b) = [a0²/(8 pi G)] y(rho_d/C_M).

Along this equilibrium curve its derivative is positive:

    dP/d rho_d = sqrt(G M_b a0)/2 × (1+y)^(3/2)/(1+y/2).

In the deep regime it approaches sqrt(G M_b a0)/2, the mass-dependent isothermal velocity-dispersion square. Calling this derivative a physical sound speed requires choosing this constitutive law for perturbations; hydrostatic data alone do not impose that choice or establish dynamical stability. The singular point-baryon center also lies outside a globally regular weak-field model.

An action could admit an entropy, chemical, external-field or other state variable, with different values selected for different hosts. Alternatively, it could couple directly to the baryonic field. These are possible continuations, but the selection and backreaction equations must be supplied. Replacing M_b by a region-integrated mass introduces precisely the nonlocal region and merger prescription already exposed by the frame audit. Labeling it an integration constant does not explain its required correlation with baryonic mass.

Subtracting the boundary pressure leaves the density and the displayed derivative unchanged. A freely mass-dependent subtraction is additional boundary data; it is not evidence that the original universal barotropic law exists. The constructive finite-edge family remains valid under its stated hydrostatic hypotheses, while its universal action remains open.

`eos_audit.py` checks the density transformation, hydrostatic identity and derivative exactly with SymPy, then compares two masses at the same density on both a0 footings. MUTATE removes the mass dependence from the constitutive map and must fail the equal-density and distinct-pressure controls. These tests do not establish a relativistic causal or stable completion.
