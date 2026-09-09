# Static shift and clock consistency

The exact stationary ADM metric used for this check is
ds^2=-N^2 dt^2+a^2(dx+beta dt)^2+h^2(dy^2+dz^2), tau=t, phi=phi(x).
Direct four-dimensional Christoffel calculation gives

Q=-beta phi'/N,
Y=phi'^2/a^2,
H=[(phi''-a'phi'/a)^2+2(h'phi'/h)^2]/a^4,
J^mu partial_mu phi=N'phi'/(N a^2).

Thus Y, H and the acceleration mixing are exactly independent of stationary
beta. The measure is also independent of beta. The normalized-clock
acceleration squared depends only on the spatial lapse gradient. The EH and
khronometric extrinsic-curvature invariants are quadratic in beta and beta'
on this stationary slice; their first variation vanishes at beta=0. A direct
quadratic-invariant check is included in the script.

The remaining linear shift source from -sqrt(-g) K(Q) is
a h^2 K'(0) phi'. It vanishes for the stated K(Q)=K2 Q^2. For K'(0)!=0,
the nonzero-gradient branch would instead require an additional source or
different background. This is a condition derived from the action.

The clock equation follows from the full covariant diffeomorphism identity:
the time divergence of a stationary diagonal metric Euler tensor vanishes,
the scalar has partial_t phi=0, and partial_t tau=1. The script verifies that
divergence directly using the four-dimensional connection. With the shift
equations zero, the identity forces E_tau=0. Transverse vector equations
vanish by planar reflection symmetry. This reasoning assumes the normalized
clock formulation and a differentiable covariant action, not an independent
unconstrained aether vector.

Consequently the previously constructed local static branch is compatible
with these omitted equations for K'(0)=0, subject to its numerical spatial
equation accuracy. This does not establish global boundary matching, the
exact physical MOND law, Phi=Psi, acceptable PPN parameters, a two-mode
Hamiltonian, time-dependent stability or cosmology. The illustrative J remains
an input, not a derived calibration of the physical force law.

Command: `python3 qwen_claude_field_theory/closure_2026/user_action_shift_gate.py`
Exit 0; output saved as user_action_shift_gate.json. This is a bounded
same-action consistency result under Mathbox computation-audit discipline.
