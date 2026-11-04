# Warm four-singlet coherence local check

Owner scope: this new warm_coherence/ only. All earlier scopes stay frozen.
Base shared checkpoint fd417eea045a0b6259b8efff5e20ca62a2e14f7e; fresh source
and data hashes identify the actual revisions used.
Use actual warm001/warm002 endpoint occupation vectors as supplied finite
states, including independent warm002 hole coordinates. Their upstream runs
ended at bounded checkpoints and have failed target-reaching records; they
are not promoted to completed cosmological histories.

Identify the four massive parents by actual singlet_indices and mass
sqrt(.006): their group is S1_1, degeneracy four. S1_0 is the massless
two-real-state modulus and is not substituted. Rebuild actual-x cubic and
Yukawa vertices in their full adapted basis. Use the same common background
group masses as the warm finite operator, record exact-tree/background
differences, and never transplant the late pole coefficients.

For a spin-zero parent at each saved momentum node, isotropic unpolarized
group daughter occupations multiply each actual per-channel absorptive
matrix by the angular average of availability products (loss) and occupation
products (gain). Integrate the existing entropy-variable projection exactly
on daughter-energy stencil intervals. Check against segmented Gauss rules
and thermal detailed balance. Retain current holes separately where stored.

The declared local Markov diagnostic is
rho_dot=Gamma_gain-{Gamma_loss-Gamma_gain,rho}/2, with bare degenerate H=M I.
Where its damping matrix is positive, solve its full four-state stationary
response and compare channel/charged currents with isotropic diagonal and
equal-trace closures. Also quantify actual isotropic-state anisotropy growth.
No thermal dispersive splitting, parent/daughter entanglement, rotating
background basis, or full Kadanoff-Baym locality theorem is silently assumed.
The declared operator includes physical FFS/SSS channels; broken-vector
channels are excluded rather than called part of the inclusive width.

First cheap discriminator: two endpoint midpoints, with actual momentum and
daughter f/hole arrays, plus turning-point basis overlaps and channel coverage.
If coherence is material and the parent subspace admits a controlled common
frame, a second bounded periodic matrix-response check is promising. If it
does not, retain the explicit first missing transport implication.

Every new scientific job: fresh v2, wall<=240s, CPU<=235s, one numerical
thread, measured RSS, no address-space/affinity limit. Preserve failures and
exact sources in new names. No Git, installation, queue, portal or old edits.
