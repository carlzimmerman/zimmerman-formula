# Concurrent L167 result: relevance without importing a fitted mechanism

Read-only source/output review of `449c7f77d6860c65fca2badfd2726dda39c84cfd`,
which landed during this calculation. No independent rerun of its 162 runs.

`fable_independent_2026/L167_nbody_kick_test.py` is self-gravitating within
enforced spherical symmetry: `accel` sorts 20,000 radii and recomputes the
enclosed cold mass at every step. Baryons are fixed. It is not merely a
test-particle calculation, nor is it unrestricted 3D N-body gravity.

The recorded canonical baryon-read crossings are v_k/v_flat = 1.81, 1.93,
2.23 for the 80, 110, 220 km/s hosts. At tau=5 Gyr and v_k=600 km/s the
massive baryon-read host retains 0.447 of the selected cold acceleration
contribution, below the assumed 0.582 ceiling. This improves the earlier
orbit-retention surrogate. It is not a cosmological likelihood or proof of
a unique surviving parameter cell.

Controls include a fixed-baryon-potential energy test, matched no-kick runs,
late-time averaging, fixed seeds, and selected profile/footing/external-field
sensitivities. The energy control is specifically the separate fixed-potential
test, not energy conservation of the self-gravitating kick calculation.
Particle-number, timestep, softening and independent-seed convergence have
not been supplied in this commit.

At each prescribed event the source executes `v[due] += vk * d`, leaving
particle masses unchanged. No recoil partner or conserved clock-sector
energy reservoir is derived. Therefore it does not supply the no-particle,
action-derived transfer mechanism the present goal needs. The force uses
nu_RAR(s)=1/[1−exp(−sqrt(s))], not the exact inverse of the requested
mu(g/a0)=1−exp(−g/a0). These two constitutive choices must not be swapped.

Useful next empirical computation, once an interaction is specified: infer
the kick distribution and energy/momentum exchange from that interaction,
then rerun the spherical calculation with convergence controls and the
chosen action's force law. The paper's phenomenological kick speeds cannot
be inserted into the clock action and called a derivation. Its own output
explicitly says the test derives no mechanism. Full theory remains OPEN.
