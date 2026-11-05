# Curved nodal-band spectral calculation

Base:639b5df4b2. The previous turn was progress: changing matter repaired
the finite threshold sign, but the specified isotropic material embedding
did not generate Einstein gravity. This route changes the curved operator
itself, retaining the original quadratic tangential band Hamiltonian.

On Euclidean R_tau x R_z x S^2_r define

    H=[(L_S2-k0^2)/(2M)] Gamma1+v(-i partial_z)Gamma2+Delta Gamma3,
    {Gamma_i,Gamma_j}=2delta_ij, L_S2=-nabla_S2^2.

M,v,k0,Delta are positive and constant. The internal matrices are
pseudospin; the surface Laplacian acts as a scalar on their components.
There is no inserted curvature endomorphism. This is an explicit minimal
curved extension, not a claim that a flat spectrum uniquely specifies it.
The squared determinant is defined by omega^2+v^2 k_z^2+
[(l(l+1)/r^2-k0^2)/(2M)]^2+Delta^2, degeneracy2l+1 and matrix trace d.

Compute the local term linear in surface curvature from the large-r
spectral expansion, retaining the band endpoint lambda=0. Distinguish it
from the near-nodal contribution producing the flat |Delta|^3 term.
The discriminating question is whether this explicit curved operator
generates the assumed |Delta| R_S2 coefficient from the same nodal modes.

Use Euler-Maclaurin analytically and verify its curvature coefficient
against the discrete sphere sum at M=v=k0=1 (dimensionless diagnostics),
proper times s=1/4,1,4 and radii20,40,80, at80-digit precision. These are
not physical parameters or a coefficient scan. Require relative error
below1e-3 at radius80 and successive error reduction between3.5 and4.5.
Bound the omitted positive sum tail by its decreasing-function integral,
checking monotonicity at the truncation point; require tail below1e-60.

Also check the analytic mass dependence of the curvature term after its
constant and Delta^2 subtractions. Negative control replaces the band-edge
heat weight with the nodal heat weight; the three curvature matches must
fail. Preserve separate runner manifests, no input changes after execution.
Single thread,60-second cap, no downloads or external datasets.

Limits: expand large r at fixed positive mass/proper time before taking
the gapless limit. A finite-radius spectrum can have separate level-crossing
effects. The result probes only product-surface curvature, not all metric
components, gravitational-wave propagation or a complete Einstein term.
No microscopic coefficient, protected criticality, adopted action or shared
campaign record is claimed or modified by this computation.
