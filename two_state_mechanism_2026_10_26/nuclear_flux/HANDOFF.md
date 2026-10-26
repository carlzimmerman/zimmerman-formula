# Continuation: physical rates remain open

Start at README.md, DERIVATION.md and run_audit_v2/results.json. This stage follows
0343483bcb63d46da0b1fd4fde2f1509d0bdbb3c, not an unrelated checkout HEAD.
The user's complete objective is still physical DR/assembly rates plus photon
recycling and a shared-parameter galaxy test; this stage does not fulfill it.

Material progress at the previous bottleneck:
- Recovered actual Q/P Hamiltonian and boundary blocks and electronic capture/
  escape matrices, not only a resonance peak. The optical identity fixes their
  relative normalization. Off-shell diagonal widths are not chemical rates.
- Implemented full retained-sector radial nuclear propagation and outgoing flux.
  Fixed an artificial diagonal-lead interface using coupled lattice modes.
- Added diffuse atomic channels; the original basis incorrectly closes a2p
  product channel. Larger state spaces expose unresolved convergence.
- Derived/checked atomic E1 decay and a charge/energy/constituent-conserving
  branch-and-photon ledger. This is not a physical DR/photon trajectory.

Remaining dependencies, in order:
1. Establish asymptotic atomic/ion-pair channel identification and converge neutral
   dynamics in electronic basis, radial mesh and matching domain. Ag fixed-axis
   calculations are not complete total-J/spin sectors. Add rotational and
   finite-mass terms consistently; reconcile fragment threshold energies.
2. Extend/recompute the electronic capture kernel in a compatible electronic
   basis over the full nuclear interaction region and collision-energy range.
   Current kernels use the old42-dimensional Q basis at only R2,3,4. Its
   aug-cc-pVDZ product channel error prevents use with larger-basis nuclear
   matrices without an explicit projection and convergence test. Higher-R
   integral and outer-multipole convergence is not established.
3. Decode/track the Q configuration gauge across geometries and map it to the
   electronic states used for nuclear propagation. Matching eigenvalues alone
   does not supply that map. Keep the incident-electron phases/normalization.
4. Construct Sigma_N(E) with nuclear propagation in P (or validate an equivalent
   energy-dependent MQDT method). Preserve closed channels, real energy shifts,
   open ionic vibrational thresholds and the source/escape optical identity.
   A delta-local replacement by the computed Sigma_Q is not the full kernel.
5. Compute incident-electron-to-product amplitudes, sum the required angular/spin
   sectors, integrate sigma(E) thermally with tail/error controls and derive inverse
   rates. Current neutral reflection probabilities must not be used as DR losses.
6. Use those rates in a product-resolved photon network, including2s two-photon
   decay and actual spectral occupation/transport. branch_energy.py has no
   physical DR rate and does not replace the old photon's spectral network.
7. Only then compare all four prior density/velocity profiles at shared microscopic
   parameters. Disk formation, live gravity, countercharge transport and the galaxy
   acceleration relation additionally require spatial dynamics. No type switch.

Three routes remain open: direct coupled electron/nuclear/Feshbach solution;
validated energy-dependent frame transformation; an authenticated transferable
physical scattering dataset. No matching dataset was found or imported. The
current finite results do not prove a universal obstruction or successful selection.

Reproducibility: launch.py / launch_stream.py reproduce new runs with bounded
contracts. Exact executed commands are in manifests. Large grid.npz files are
local, ignored by Git and hashed in manifests; see VALIDATION.md. Streamed runs
avoid this storage cost and reproduce the saved-grid solver. Do not edit any
pinned script/input. Use a versioned new script/contract/output for changes.
