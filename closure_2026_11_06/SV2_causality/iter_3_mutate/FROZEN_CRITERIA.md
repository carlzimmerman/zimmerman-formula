# SV2 iter_3: MUTATE of the repair class. FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Frozen before any script or number of this lane exists.

## The member and its flips

The class member of iter_2 at the window edge that gives a finite khronon speed: alpha = 2 beta, beta = 1.4e-15
(GW170817 edge), beta + lambda = alpha (c_k = c). These numbers are the bound edges, used only to size the flips;
every line below is a sign statement that holds for any magnitude.

- M1 (alpha -> -alpha): the kinetic coefficient 1/Z + alpha/(2K), Z = K f + gamma k^2, gamma = K Lstar^2 / 2, must
  turn negative (ghost) above a wavenumber k_ghost = (2/Lstar) sqrt(2/|alpha| - f): numeric per footing (Lstar
  21.68 / 22.85 pc), both e and perp, and Lean (SV2_repair.lean, existence of a ghost k for alpha < 0).
- M2 (beta + lambda -> -(beta + lambda)): Pi + lambda'' k^2 must turn negative (gradient instability) above
  k_grad = sqrt(2 K Pi / (|beta + lambda| c^2)): numeric per footing, and Lean.
- M3: the instantaneous mode stays under both flips: omega0^2(e) != omega0^2(perp) (lambda does not enter omega0^2;
  alpha < 0 keeps the strict monotonicity in f wherever 1 + alpha f/2 > 0).
- Lean twins (SV2_causality_MUTATE.lean, SV2_repair_MUTATE.lean): planted false claims (a spacelike displacement
  advances tau; an isotropic omega0^2 at x > 0; alpha < 0 ghost-free; beta + lambda < 0 gradient-stable) must FAIL to
  compile (exit 1), each error in the saved .out.

## Label

BITES if M1 and M2 show the instability on both footings, M3 holds, and every planted Lean claim fails. Otherwise the
health lines of iter_2 cannot tell a healthy member from a sick one and iter_2's R3 does not stand.
Also counted here: iter_1's MUTATE (hyperbolic leaf -> HARMLESS) and iter_2's x = 0 control (-> REMOVED-CANDIDATE).

Kappa = 1/2 FITTED; not theory closed.
