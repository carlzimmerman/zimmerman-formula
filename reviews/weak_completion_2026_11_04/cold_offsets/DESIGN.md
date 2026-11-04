# Small-excitation orbit design and finite contract

Task: resolve a specific remaining numerical limitation in the existing
Hamiltonian orbit oracle. Keep the frozen common warm state and all prior
sources unchanged. This package is not a new physical cold history.

Approaches considered: full arbitrary-precision orbit integration would avoid
large-total cancellation but is unnecessarily costly as the production
interface. A local harmonic approximation is cheap but cannot test its own
anharmonic error. The selected approach evaluates the actual local cubic
mass-squared splines and potential polynomial in displacement coordinates,
using an exact rational gas-energy remainder; high precision supplies an
independent reference for that finite representation.

At a float anchor x_a near the minimum, retain the total first derivative F_a
from a high-precision sum of the same pinned float coefficients. With d=x-x_a,
Δ=m²(x)-m²(x_a), and E0=sqrt(m²(x_a)+p²),

    E(x)-E0-m²'(x_a)d/(2E0)
      =[Δ-m²'(x_a)d]/(2E0)-Δ²/[2E0(E(x)+E0)²].

Combine all linear terms as F_a d. Evaluate quadratic and higher terms without
subtracting large totals. Solve for the local minimum displacement and retain
the excitation epsilon separately from its large minimum energy. Turning
points and action are computed in scaled displacement coordinates, with no
harmonic branch. The implementation refuses an orbit leaving its exact local
spline intervals; no unsupported global polynomial extrapolation is used.

Validation: actual common30 warm Y at N=.0021690179772784167, artificial
J/J_initial=1e-8,1e-12,1e-16 and a larger overlap case; 32/64-node phase
quadrature; high-precision direct potential differences and action integral;
report mass-squared branch, minimum, harmonic and linewidth limitations.
The exact finite assertion and input closure appear in each prior JSON
contract. Runs are bounded to wall<=240s, CPU<=235s and one numerical thread,
with measured RSS. No prior source or Git mutation is permitted.

This oracle alone cannot repair the coupled stepper: that must also transport
minimum-energy differences and excitation separately between changing Y/N
states. The v7 interface currently reconstructs their sum and loses that
distinction. Integration requirements will be documented, not assumed solved.
