# Conservative bookkeeping and phase fitting

This packet tests the selectively coupled CCT wave candidate, not a derivation of the literal Khronon action or evidence that the underlying substance is nonparticulate. A tag is passive bookkeeping, not a second gravitational component.

For cell volume V_i evolve u_i=sqrt(V_i) A_i. For a Hermitian nearest-neighbour Hamiltonian H, a Crank–Nicolson substep satisfies

    (u_new-u_old)/tau = -i H u_mid / eta,
    m_new_i-m_old_i = F_(i-1) - F_i,
    F_i = -2 tau Im(conj(u_mid_i) H_(i,i+1) u_mid_(i+1))/eta.

This identity follows by multiplying the first equation by conj(u_mid), taking twice its real part, and pairing conjugate off-diagonal entries. Potential kicks change neither m nor a tag q. No angular projection creates a local source.

A directed one-dimensional chain has no directed cycle. Sweep positive fluxes rightward, and negative fluxes leftward. At a donor, divide old tagged mass plus already-arrived tagged flux by old mass plus already-arrived total flux. Multiply every outgoing flux by this fraction. A fork has no incoming edge and uses the same old fraction for both outgoing edges; a sink receives both sides and has no outgoing edge. The exact nonnegative endpoint mass ensures total outflow cannot exceed available mass. Therefore 0<=q<=m remains true and total q is conserved, apart from floating-point error. No clipping or renormalization is used. The method transports the complement m-q consistently as an independent check.

This is a finite-Hamiltonian transport convention. It does not establish unique continuum trajectories through zeros or remove spatial truncation error. Positivity alone cannot certify physical core retention.

For a static real carrier S, psi=A exp(i S/eta) gives

    i eta A_t = -eta² lap A/2
      -i eta (grad S . grad A + lap S A/2)
      +(Phi + |grad S|²/2) A.

On a weighted grid the real Laplacian is symmetric; centered conservative advection is skew symmetric. Each coordinate Hamiltonian has upper edge

    eta² L_(i,i+1)/2 - i eta p_face/(2 sqrt(w_i w_(i+1))),

and its conjugate as the lower edge. The phase-fitted scheme approximates this continuum generator directly. It is not an exact coarse-grid gauge conjugation, which would retain the aliased carrier dispersion. The actual incoming radial phase is extracted from each saved l=0 coefficient; all nonzero incoming harmonic amplitudes are retained. Actual galaxy generator errors are independently compared against radial spline derivatives and spherical-harmonic Laplacian eigenvalues.

The carrier kinetic term |grad S|²/2 stays in H. It is not added to density. Poisson uses only |u|²/V once. The self energy is one half sum(m Phi); neither tags nor carrier energy are independent sources. The same symmetric finite-box Green operator appears in evolution and energy. The numerical derivative of this quadratic energy must equal Phi, and doubling density must double Phi and quadruple self energy.

The box has zero Dirichlet potential. Its force is not the infinite-domain force; box convergence is required for physical escape. A prescribed static carrier eventually ceases to make A smooth during collapse. The declared edge-phase gate records that obstruction without converting a stopped numerical endpoint into a physical exclusion.
