# Static optical-pump potential: conditional operator bound

Parent: 97e60207e8d6e1220747d59a06a35d62e2ab238f.
This bounds a coherent effect omitted from the independent-photon collision
estimate. The result is small at the assigned parameters and does not rely
on resolving individual spatial transitions. It does not complete the
physical creation mechanism or the stimulated-radiative loss budget.

## Derive the static source from both waves

In Heaviside-Lorentz natural units, take parallel electric polarizations

    E=Eamp[cos(kz-omega t)+cos(kz+omega t)],
    B=Eamp[cos(kz-omega t)-cos(kz+omega t)].

Each wave has mean energy density u=Eamp^2/2 and k=omega. Consequently

    F_mu_nu F^mu_nu=2(B^2-E^2)
                   =-8u[cos(2kz)+cos(2omega t)].

With the Lagrangian -g R F^2/4, the scalar equation has source -g F^2/4.
The static term is therefore 2g u cos(2kz), not zero. The other term is
the oscillating source already used for pair creation; do not add that
pair-creation term a second time.

For infinite monochromatic plane waves, the static solution and the
nonrelativistic carrier potential are

    R_static=2g u cos(2kz)/(M_R^2+4k^2),
    V_static=mu R_static/(2m)
            =mu g u cos(2kz)/[m(M_R^2+4k^2)].

The benchmark gives amplitude 3.99916e-22 eV. The static potential alternates
sign in space and acts equally on both carrier charge signs.

## Bound an arbitrary bounded spatial envelope

For a free static massive scalar, the positive Yukawa inverse kernel is
K(r)=exp(-M_R r)/(4 pi r), with integral over space 1/M_R^2. For any source
s(x) bounded in magnitude by 2|g|u f(t), convolution and the triangle
inequality imply

    |R_static(x,t)| <= 2|g|u f(t)/M_R^2,
    ||V_static(t)|| <= Vmax f(t),
    Vmax=|mu g|u/(m M_R^2)=7.99831e-22 eV.

The finite optical envelope can change the spatial solution but cannot
exceed this bound if the prescribed source bound holds and the scalar
operator remains the free massive one. This does not assume a physical
resonator's fields are necessarily bounded by the prescribed benchmark.
Material modification of the scalar operator would require a separate bound.

For N particles, the norm of the sum of the one-body potentials is at most
N Vmax f(t). In any sector with at most Nmax particles, the same bound
holds with Nmax. Spatial projection cannot increase this operator norm.
The parent's pulse has integral f(t) dt=0.180421246 s, so define

    epsilon_N=Nmax Vmax integral f(t)dt/hbar.

Duhamel's identity for two unitary propagators differing only by this bounded
potential gives ||(U-U0)psi||<=epsilon_N for a normalized initial state.
For a projector P orthogonal to U0 psi, ||P U psi||^2<=epsilon_N^2.
This squared bound applies to orthogonal leakage from that particular
unperturbed final state, not to the change in an arbitrary event probability.

The comparison also extends to unchanged Markovian dissipators: variation
of constants, trace-norm contraction on Hermitian operators, and
||[V,rho]||_1<=2||V|| give ||rho-rho0||_1<=2 epsilon_N. Since the difference
has trace zero, any measurement event probability changes by at most
epsilon_N. No assumption of a small gap between spatial modes is needed.
This assumes the same prescribed dissipator in both evolutions; it does
not bound additional losses or a potential-dependent change in that model.

## Numerical implications and scope

- One-carrier integrated norm: 2.19240e-7.
- At most two carriers: state-distance bound 4.38480e-7; the specifically
  defined orthogonal-leakage bound is 1.92265e-13.
- At most ten carriers: any event-probability change is bounded by
  2.19240e-6, with the same baseline Hamiltonian and dissipator otherwise.

The ten-carrier cutoff corresponds to the parent's occupations 0,...,5 for
each charge sign. This does not establish convergence beyond that cutoff.
Vmax is 1.81e-12 of the ground orbital energy and 2.80e-14 of the assigned
wall barrier. It is therefore not an omitted large static trap modification
in this specified model.

The scalar response timescale hbar/M_R divided by the 5 ms ramp is
6.58e-14. This motivates quasistatic treatment but is not a proved error
bound for the retarded scalar field. The calculation omits additional
longitudinal/focused optical components, stimulated emission into sidebands,
material electromagnetic response and all changes to the prescribed optical
mode. In particular, this does not turn the preceding independent-beam
scattering rate into a bound on all coherent photon processes.

The bounded run passes ten numerical consistency checks on the field identity
and Yukawa-kernel normalization; the equations and norm argument above are
an analytic self-review, not a Lean-certified operator theorem. The manifest
validates the recorded inputs and outputs. No measurement or empirical
admissibility claim is made.

The static pump term is now bounded within the assigned creation model.
Stimulated sideband losses and a physically feasible cavity remain separate
high-impact obligations; material and particle assumptions remain conditional.
The overall cold-energy creation goal stays open.
