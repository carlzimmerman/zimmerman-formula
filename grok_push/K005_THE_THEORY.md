# The theory of gravity on these equations

Gravity is Einstein's. Ordinary matter is minimal on \(g\), so it is geodesic, so \(a^\mu = 0\), so it is on the free-fall branch and pressureless in this sector. The dark stress is one potential-flow fluid,

\[
p = P(a), \qquad a^\mu = u^\nu\nabla_\nu u^\mu, \qquad u_a = \partial_a\phi/\sqrt{X},
\]

with \(P\) matched to the measured kernel at \(a_0 = s/2\), \(s = c\sqrt{G\rho_\Lambda}\). The half is the measured deep slope. It is not derived. There is no new particle.

## Branch, now a theorem

The self-consistency identity \(a(K\rho + a') = 0\) has two roots. Which root a region takes is the kinematics:

- **Geodesic** (\(a = 0\)): free-fall, \(p = 0\). Stars, the Sun, wide binaries, the Hubble flow. Forced by minimal coupling. Cassini is Einstein's.
- **Static in an inhomogeneous potential**: a static observer has \(a_i = \partial_i\Phi/(1+2\Phi)\). Then \(a \neq 0\), free-fall is excluded, and the supported root \(a' = -K\rho\) is forced. That equilibrium is the phantom, hence the RAR, in equilibrium.

A galaxy is not automatically on the supported branch. A geodesic in an inhomogeneous potential still has \(a = 0\). The rival reading is excluded.

## What the two branches carry

| branch | kinematics | carries |
|---|---|---|
| (F) free fall | geodesic, \(p = 0\) | CMB, forest, clusters' collisionless piece, KiDS outside the cap, \(\Omega_{\mathrm{dm}}\) |
| (S) supported | static, \(a' = -K\rho\) | the RAR in the rotation-curve window |

Clusters are both branches of the same fluid. The supported piece is the MOND shortfall L247 computed (about 3.3 against 6.8). The rest is the free-fall piece. Same stress-energy, two kinematic states.

## Measured, not derived

- \(n = 2\), hence \(\kappa = 1/2\).
- The amplitude \(\Omega_{\mathrm{dm}}\).
- The settled fraction \(f_S \in [0.027, 0.064]\) (K001). How much of the medium has the static kinematics. An initial condition, the same kind of number as \(\Omega_{\mathrm{dm}}\). The selection equations do not contain it.

## Not in the theory

A vortical dark stress. The action is potential flow. The constraint algebra off potential flow is not an open problem of this action.

## Kills

1. \(f_S \ge 0.10\) from a volume-limited census.
2. KiDS-like lensing that turns at \(a_0\) inside the cap (5.8 kpc; KiDS starts at 35 kpc).
3. A stripped dwarf with Newtonian \(\sigma\) (L247 V7, order-unity ram pressure, marginal).
4. DR4 wide binaries in Arm A. The Sun is geodesic. Arm A says it is not.
5. A local force-law completion. Those are dead (K002).

## Certificate

- `K005_branch_selection.py` — 5/5
- `lean/K005_branch_selection.lean` — the selection algebra
