# Optional radial dictionary to the existing stiffness energy

The branch proof independently assumes the fixed functional EOS P_c=K rho_c^2. There is also a conditional radial connection to the S2 stiffness term in `../action_join/inputs/S2_CANONICAL.md`, equations near its lines 17–20: gamma=kappa G L_*^2/2 and the positive spatial energy gamma|grad P|^2/2. Here the bold field P is a polarization/displacement variable, not fluid pressure; kappa here is the S2 input, distinct from the radial coercivity margin in the branch proof.

If the physical charged rest density is rho_c=div bold-P, bold-P is curl-free, and its surface term vanishes, integration by parts gives

\[
 \int |\nabla\mathbf P|^2
 =\int[(\nabla\cdot\mathbf P)^2+|\nabla\times\mathbf P|^2]
 =\int\rho_c^2.
\]

The same positive energy is then internal energy u_c=K rho_c^2 with K=gamma/2=kappa G L_*^2/4, whose barotropic pressure is rho_c du_c/d rho_c-u_c=K rho_c^2. For a regular spherical finite-mass source, P=M_c(<r)/(4 pi r^2) rhat is curl-free and its endpoint surface terms vanish. This accounts for the field outside the compact charged density as well; it is a global integral identity, not permission to discard the exterior gradient energy pointwise.

This dictionary requires the stated physical-density identification and radial curl-free assumptions. It does not establish their full covariant current equivalence, the value of gamma, or the subcritical charge ratio used in this construction. One must not add both this barotropic energy and the same original stiffness term as separate energies for the same degree of freedom. No proof in `PROOF.md` depends on claiming a microscopic derivation from this optional dictionary.
