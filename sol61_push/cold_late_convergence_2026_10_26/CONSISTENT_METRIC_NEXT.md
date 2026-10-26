# A concrete numerical route beyond the transfer obstruction

This is an unimplemented next-method specification, not a change to any run in this packet or a new physical cooling mechanism.

Let a be interior basis coefficients, let B have full column rank and evaluate the radial envelope at overintegration nodes, W be their positive dr weights, and D evaluate its physical radial derivative. Include the existing real carrier p through

    M = B† W B,
    K = (eta D + i diag(p) B)† W (eta D + i diag(p) B) / 2.

For rho=|B a|² and a real symmetric shell Green matrix G, use

    Phi_c = G W rho,
    E = a† K a + rhoᵀ W G W rho / 2 + rhoᵀ W Phi_b.

The same quadrature then defines mass a†M a, kinetic energy, density and the source. A centered discrete-gradient step is

    i eta M (a1-a0)/h
      = [K + B† W diag(Phi_b + (Phi_c1+Phi_c0)/2) B] (a1+a0)/2.

Its bracket is Hermitian. Taking the appropriate real inner products gives zero mass change and zero energy change for an exactly solved step: delta rho=2 Re[(B a_mid)* B delta a], and the quadratic self-potential difference uses the mean old/new potential. Finite nonlinear solve and quadrature tolerances would still need measurement. This construction retains the same continuous CCT proxy; a consistent reciprocal physical action remains a separate obligation.

Before galaxy production, implement an isolated prototype and test analytic polynomial mass integrals, free-wave phase accuracy, positive mass, nonlinear residuals, conservation, reversibility, refinement and independent density/source checks. Test the nonconstant mapped Jacobian and retained carrier, not only affine zero-carrier cells. Then start independently from the original analytic initial conditions. Changing the mass metric of an existing lumped-mass late trajectory does not preserve its old invariant references and is not an accepted restart.

The present Gauss-integral diagnosis motivates this route; it does not establish the new method's performance, solve the excess inner force, supply cold mass or demonstrate stellar-safe relaxation. Keep the independent16384trajectory route and all physical failures visible while testing it.
