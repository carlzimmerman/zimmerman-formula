# All-orders conservative metric available for the next reduction

Proposed continuation, not executed here. The complete cubic audit suggests
using the original stationary phase/current block rather than another
phenomenological damping or density gate.

For a pure-T density rho>0 and specified rho_t, put A_f=-div(f grad) and define

 K(rho)=[[A_rho,-g2 A_(rho²)],
         [-g2 A_(rho²),c² A_1+g2² A_(rho³)]],
 b=[rho_t,-2g2 rho rho_t].

After removal of constant spatial modes, the exact quasistatic stationary
phase/scalar action is T=.5<b,K^-1 b>. It is positive because its original
quadratic form is integral[rho|grad phi-g2rho grad chi|²+c²|grad chi|²].
The scaled form X=c chi improves conditioning without changing physics.
The earlier full stationary-elimination third derivative audits this block,
whereas diagonal1+eta and frozen-material preconditioners do not invert it.

For a retained zero-mean density basis F, rho=rho0+Fq and rho_t=Fqdot,
T=.5qdot^T M(q)qdot. With p=M qdot, the conservative Hamiltonian is
H=.5p^T M(q)^-1p+U(rho). This retains all orders of the kinetic metric and the
positive original density/response energy within that density subspace.
Its canonical force is p_dot=partial_q T at fixed qdot minus partial_q U,
plus the reciprocal body-field charge force. It can audit whether omitted quartic terms change the local cubic channel.
It is not a full galaxy merely because its retained modes are nonlinear.

Analytic forces follow from stationary elimination. If y=(phi,chi)=K^-1 b,
then dT=(db)^T y-.5 y^T(dK)y. This gives the exact reciprocal mean/material
force, avoids finite-difference derivatives of a fitted rate, and supplies a
natural coupled block for an implicit Newton solve. The body-charge coupling
Q(q)chi_t,avg must be retained on both sides, with its outgoing kernel/field.

For spherical grids each A_f is tridiagonal. The coupled phase/current block
can be solved with sparse block methods. The converting two-species sector
needs both phase variables and the alignment curvature, and all-F limits
must use regular amplitudes rather than divide by zero density. Finite carrier
momentum and its density-inertia force are additional obligations, not terms
to discard silently. This construction does not authorize BO branch jumps or
count an optimizer decrease as physical cooling.

A global version must retain freely evolving mean density and the actual
infall occupations. A local fixed-background mode calculation cannot answer
that question. The angular energy functional, seed/occupation and coefficient
origin remain stated physical inputs. No completed global implementation,
unique3D extension or proof of formation is claimed in this note.
