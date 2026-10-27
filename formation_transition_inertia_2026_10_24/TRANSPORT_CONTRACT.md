# FT-I4: conservative angular momentum transport

FT-B1 depends on conserved individual shell angular momenta. FT-I3's tested
contracting barrier has not formed persistent T. This route changes that
specific restriction: viscosity transports ordered baryonic angular momentum
outward without destroying total angular momentum. The reservoir starts
diffuse as in FT-I3, so no existing dark bound halo is assumed.

Decompose each baryon shell's initial l_i^2 into ordered j_i^2=f^2 l_i^2
and fixed random k_i^2=(1-f^2)l_i^2. E_rot,b=sum m_i(j_i^2+k_i^2)/(2r_i^2).
Define Omega_i=j_i/r_i^2, Kij=exp[-(log(ri/rj))^2/2], and

    dot j_i = nu sum_j m_j Kij (Omega_j-Omega_i),
    nu = nu0 Rhalf0^2/t_dyn.

Total ordered J=sum m_i j_i is exactly conserved. Rotational energy loss is
nu/2 sum_ij m_i m_j Kij (Omega_i-Omega_j)^2; this is added to Qdot.
It is a constructed positive viscosity closure, not a derived transport
coefficient or a 3D disk calculation. In the rotor completion all physical
angular velocities receive the same shift, which cancels from differences.
The gravitational and phase action is unchanged from FT-I3; lambda uses the
conserved total J. Random angular support is unchanged, making the low-f
control more pressure-supported without a system-type label.

Pilot: profile1, dark scale30, f=.3,.95; alpha=1,3; iota=.01,.1; nu0=1.
Eight trajectories, six shells/species, nq256, duration12 tdyn, rtol2e-7,
30-second per-trajectory cap. Check the full energy directional derivative
including j evolution, zero total torque, and positive heat. Any candidate
requires duration and resolution checks and the RAR, not just high q.
Radial-domain exits are incomplete physical histories, not successes.
