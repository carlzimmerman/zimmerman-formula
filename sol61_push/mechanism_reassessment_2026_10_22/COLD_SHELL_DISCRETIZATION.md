# Conservative shell discretization for the assembly test

This is a reduced spherical cold-fluid model, not the full parent theory. Mass is normalized to1, gamma=.01, and baryonic acceleration is beta(t) r/(1+r²)^(3/2). All shell angular momenta vanish. The beta history is externally prescribed.

Use N cells of mass dm=1/N, node masses m_j=j dm and ordered radii r_j, j=1,...,N, with r_0=0. Define

    V_j=(r_j³-r_(j-1)³)/3,
    rho_j=dm/V_j,
    p_j=gamma rho_j²/2.

Nodal kinetic weights are w_j=dm except w_N=dm/2. A fixed central half-weight dm/2 completes the trapezoidal mass quadrature; it has zero kinetic energy and contributes a constant -beta dm/2 to baryonic energy. Its finite-resolution contribution vanishes as N grows.

The discrete energy is

    H = sum_j w_j v_j²/2 + (gamma/2) sum_j dm²/V_j
        + sum_j w_j [sqrt(m_j) atanh(sqrt(m_j)/r_j)-m_j/r_j]
        - beta [sum_j w_j/sqrt(1+r_j²)+dm/2].

Domain: positive cell volumes and r_j²>m_j. Differentiating gives

    a_j = r_j²(p_j-p_(j+1))/w_j
          + R(m_j/r_j²) - beta r_j/(1+r_j²)^(3/2),

with p_(N+1)=0. In particular the derivative of the field potential per unit nodal mass is -R(m_j/r_j²). This supplies a discrete conservative realization of the intended cold force and pressure. It is not asserted to be identical to the earlier particle-mesh Hamiltonian at finite resolution.

For prescribed beta(t),

    dH/dt = -beta_dot [sum_j w_j/sqrt(1+r_j²)+dm/2].

Thus the live calculation checks H(t)-H(0) against accumulated external work rather than expecting constant subsystem energy. The quintic ramp has vanishing first and second endpoint derivatives. Velocity Verlet advances the equations; work is integrated by a trapezoidal rule. The positive pressure becomes stiff for narrow shells, so a fixed explicit step can fail. The code rejects shell crossing and q>=1 instead of extrapolating through either event.

Discrete stationary radii are solved from these same forces before each run. This avoids interpreting drift of a merely continuum equilibrium on a discrete mesh as assembly. A directional finite difference of the complete energy checks the force independently. Spatial and temporal convergence remain empirical obligations; Hamiltonian structure alone does not establish them.
