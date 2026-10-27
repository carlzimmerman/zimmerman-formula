# Remove the large local gauge phase without removing a force

Let phi be the earlier canonical T amplitude and rho=|phi|^2. Put

 psi=exp[i(g1+2g2 rho)chi/sigma] phi,
 Pi_ext=wave_volume*pi+deposit(g1*mT+g2*mT^2/material_volume).

The matter symplectic one-form transforms as

 -sigma rho darg(phi)+pi dchi
 =-sigma rho darg(psi)+(pi+g1rho+g2rho^2)dchi+d(g2rho^2chi).

Thus psi and Pi are canonical, up to the displayed exact differential.
The physical wave velocity remains pi=(Pi_ext-deposit(q_ext))/wave_volume.
Alignment has no chi phase in these variables. The exact same edge energy is

 kappa*w/2 |exp[-i(g1+g2*rho_face)Delta chi/sigma]psi_j-psi_i|^2.

The Hamiltonian retains this positive square, all density potentials, carrier
gradient and finite p_alpha^2/(2Z), wave gradient and pi^2/2. Total shift charge
is simply sum(Pi_ext). No coefficient, static force or physical outlet changes.

For D=kappa*w Im(conj(psi_i)U psi_j), the extra density chemical potentials are

 mu_i=-q'(rho_i)*pi_i - g2 D Delta chi/(2sigma*volume_i)

with contributions from both adjacent edges in the second term. The scalar
canonical momentum force at the left/right edge is -/+ (g1+g2rho_face)D/sigma.
Subtracting q_dot gives exactly the old physical scalar source, including
conversion and compression. No conversion or spatial companion is discarded.

The numerical experiment uses the symmetric density secant
q_sec=g1+g2(rho0+rho1), q_bar=(q0+q1)/2. This makes the local scalar-energy work
identity exact under endpoint density increments. It is a different consistent
second-order discretization of the SAME continuous canonical action, not an
identity between finite old/new steps. Time refinement and small-step comparison
after the exact variable transformation are required. Positive absorber halves
act on physical pi; the fourth-order composition retains signed Hamiltonian
substeps and rejects any nonconverged or over-cap intermediate state.

The physical source in a step is

 S=(q1_ext-q0_ext)/dt + grad_chi(H_edge),

deposited onto the wave nodes. Its conversion part is q_sec*Gamma at the
material midpoint; the remainder is transport. The wave equation and reciprocal
material density force use this same secant. All material cells remain free.
