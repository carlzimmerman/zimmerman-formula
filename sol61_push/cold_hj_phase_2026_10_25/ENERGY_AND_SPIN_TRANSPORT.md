# Physical transport budget for the CCT wave candidate

This is a conditional nonrelativistic coherent-field model. It does not derive eta=1500 pc km/s, prove a nonparticle ontology, supply the selective coupling to baryons, or complete a literal Khronon/AeST action. There is no independently demonstrated cooling channel in this packet.

## Action and one gravitational source

With rho=|psi|², take

 L = i eta (psi* psi_t-psi psi*_t)/2
     -eta² |grad psi|²/2-rho Phi-|grad Phi|²/(8 pi G).

Its equations are i eta psi_t=-eta² lap psi/2+Phi psi and lap Phi=4 pi G rho. The isolated mass, energy and angular momentum are

 M=int rho,
 E=int [eta² |grad psi|²/2+rho Phi/2],
 J=int x cross [eta Im(psi* grad psi)].

The half self energy counts each gravitating pair once. Carrier energy, passive tags and putative captured mass are not extra sources. Boundary terms must be retained outside a decaying/zero-potential setting. Baryonic/host work must be added explicitly if introduced.

## Local energy and spin fluxes

A local physical energy density with the same isolated integral is

 e=eta² |grad psi|²/2+rho Phi+|grad Phi|²/(8 pi G).

It obeys e_t+div F_E=0, with

 F_E=-eta² Re(psi_t grad psi*)-Phi_t grad Phi/(4 pi G).

The physical momentum density is j=eta Im(psi* grad psi). Define the symmetric total stress

 T_ij=eta² Re(partial_i psi* partial_j psi)
      -eta² delta_ij lap rho/4
      +[partial_i Phi partial_j Phi-delta_ij |grad Phi|²/2]/(4 pi G).

Then partial_t j_i+partial_j T_ij=0. The angular-momentum flux is L_ij=epsilon_ikl x_k T_lj. Symmetry of T removes the internal torque and gives partial_t (x cross j)_i+partial_j L_ij=0. For a core boundary moving at velocity b, use F_E-e b and L_ij-(x cross j)_i b_j in the surface integrals. A changing aperture is not physical escape.

These identities are independently checked on an exact polynomial instantaneous Schrödinger/Poisson jet in conservation_v2.py, including Phi_t from the time derivative of Poisson. That finite symbolic check validates the implementation and sign conventions; the displayed general identities follow from the equations by differentiation/integration by parts. The polynomial example is not a decaying galaxy or a global formation solution.

## Two distinct material-partition corrections

Let a tag define rho_c=f rho, rho_e=(1-f)rho, with0<f<1. If auxiliary fields are constructed as psi_c=sqrt(f)psi and psi_e=sqrt(1-f)psi, their kinetic energies obey

 K[psi_c]+K[psi_e]
   =K[psi]+eta²/8 int rho |grad f|²/[f(1-f)].

The extra positive interface term is not newly available cooling or envelope energy. Subtract it to recover the single coherent wave's kinetic energy; a sharp tag boundary can even make it singular. For this reason a passive material tag does not by itself supply a unique independent wave-energy receiver. This correction concerns splitting one coherent field by tags, not a separately derived incoherent multimode model.

Gravitational energies instead split as

 W=W_cc+W_ee+W_ce,
 W_cc=int rho_c Phi_c/2,
 W_ee=int rho_e Phi_e/2,
 W_ce=int rho_c Phi_e=int rho_e Phi_c.

Count W_ce once. Momentum and angular momentum of the tags add without the Fisher/interface correction because real gradients of f do not contribute to Im(psi* grad psi). The analytic Fisher identity and finite-box cross-energy identity are separately tested, including a deliberately double-counted cross term that fails.

## What an outgoing wave must demonstrate

A nonspherical wave can in principle export spin and energy through the above fluxes without constituent collisions. In a stationary asymptotic region with a specified potential zero, a mode exp(-i omega t+i m phi) carries specific energy eta omega and specific angular momentum eta m; their flux ratio is omega/m for m!=0. A radial m=0 component can export energy but no axial spin. This is a kinematic mode relation, not a demonstrated excitation efficiency, receiver capacity or galaxy selection mechanism.

For psi=A exp(iS/eta), energy and current must use the physical psi. If A has frequency omega_A and the reference has S_t, the physical specific frequency energy is eta omega_A-S_t. Counting only the amplitude frequency can mislabel a changing reference as cooling. Physical momentum is eta Im(A*grad A)+rho grad S; physical spin includes x cross rho grad S. A radial S contributes no intrinsic spin, but a nonspherical reference generally does.

The exact unitary discrete-gauge control changes hopping coefficients together with the field, and preserves the reconstructed wave, tags and energy to roundoff. An evolving phase-fitted continuum stencil changes its finite approximation as well; its measured gauge-energy defects are numerical errors, not energy carried into an envelope. Closed-box M conservation and small phase of A cannot decide capture.

Next discriminating physical experiment: first resolve the total physical generator/current through collapse with converged energy and vector-spin budgets; then measure outward energy and angular-momentum surface fluxes, retained core/envelope profiles and escaped mass at nested radii. Do this for all four actual-data dwarfs with the same assembly/supply prescription, and evolve resolved stellar cohorts/DFs. No such four-dwarf closure is claimed here.

The Phi equation here is elliptic and supplies no independent propagating relativistic gravitational-wave degree of freedom. The gravitational terms in the displayed flux/stress are Newtonian conservation bookkeeping; they must not be counted again as a separate radiative reservoir. Any claimed escaping wave in this candidate must be resolved in the matter/medium field psi, with the accompanying gravitational work counted consistently. Also, a moving zero-Dirichlet gravitational boundary can do field work even when material boundary density is tiny; see the failed lens packet's BOUNDARY_LIMIT.md. A material-shell gate alone is not an energy-boundary convergence test.
