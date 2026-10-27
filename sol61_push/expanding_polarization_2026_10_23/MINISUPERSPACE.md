# Dynamical homogeneous expansion: reduced extension

DERIVATION.md and the runs prescribe the scale factor. A dynamical homogeneous scale factor can be supplied without choosing field friction independently, but this remains a preferred-foliation, weak-field, finite-mode model rather than a full relativistic parent.

In physical units with c=1, comoving fiducial volume V and reduced Planck mass M_Pl, add the spatially flat homogeneous Einstein-Hilbert action with lapse N, conserved background dust rest mass M_d and optional vacuum density rho_Lambda:

 S_bg=integral dt[-3 M_Pl² V A Adot²/N-N M_d-N V A³ rho_Lambda].

Use the lapse-restored perturbation action from DERIVATION.md. The homogeneous dust rest mass is separate from its peculiar kinetic and inhomogeneous potential energies, so it is counted once. For canonical mode coordinates Q and momenta Pi, the total reduced action can be written

 S=integral dt[Pi_A Adot+sum Pi Qdot-N C],
 C=-Pi_A²/(12 M_Pl² V A)+M_d+V A³ rho_Lambda+H_mode(A,Q,Pi).

Here H_mode must be converted from the numerical normalization to physical energy, and the comoving spatial average of the perturbation potential is zero. Lapse variation C=0 gives

 3 M_Pl² H²=M_d/(V A³)+rho_Lambda+rho_mode,
 rho_mode=H_mode/(V A³).

Scale-factor variation defines mode pressure

 p_mode=-(1/(3 V A³)) partial H_mode/partial ln A |_Q,Pi.

Hamilton's equations imply dH_mode/dt=H partial_lnA H_mode, so

 rhodot_mode+3H(rho_mode+p_mode)=0.

Together these give the acceleration equation and the same expansion-work identity already tested. The homogeneous Hamiltonian constraint is preserved by the reduced Hamiltonian flow. This is a finite-dimensional variational consistency statement; it does not imply preservation of all inhomogeneous Einstein constraints.

The pressure includes the reference-density, physical-gradient and vector-component contributions explicitly present in the work expression. It is not obtained by labeling all field energy as dust or radiation. Negative gravitational binding energy is part of H_mode and is not a separate negative-kinetic degree of freedom.

This extension identifies a consistent reduced dynamical background option. The present numerical runs use the imposed EdS background, not this coupled constraint system; no claim is made that they numerically solve the equations above. A fully covariant clock/reference prescription, scalar/vector/tensor metric constraints, relativistic propagation and primordial spectrum remain missing. Those omissions matter for a CMB or lensing claim and cannot be repaired by the homogeneous Friedmann equation alone.
