# Self-audit of DA-20261022

Primary verdict for the requested common mechanism: **incomplete, with the smallest missing implication being a derived remnant mass/occupation from specified formation dynamics and energy export**. Partial claims below have narrower verdicts. No independent agent review was performed.

## Claim dependencies and obligations

| Claim | Dependencies | Review outcome |
|---|---|---|
| Fixed-L energy per mass decreases | Passive action; rigid rotation from constrained energy; virial and chemical identities; positive field energies; logarithmic W sign; first law | Proved as written under the stated stationary-branch and boundary assumptions; self-reviewed |
| Alpha<=2 extension | Same identities and Omega L=2C; differentiable specified L(M) | Proved conditionally; does not derive L(M) |
| Cold circulation conserved | Smooth single-stream cold Euler equation with a single-valued gradient force; material loop identity | Proved in that regime; not a no-tidal-torque theorem |
| Six homology size responses | Matched canonical profile; complete exterior energy; fixed mass and spin under dilation | Computationally verified only for the trial family; no rotating equilibria or shape-stability claim |
| Driven phase branches | Local adiabatic mode and fixed h or h=0; distinction between velocity control and canonical momentum | Algebra verified; applicability conditional on local approximation |
| Stable local motion does not dissipate | Explicit two-coordinate conservative Hamiltonian and three finite trajectories | Energy conservation verified; no assertion excluding spatial radiation |
| Outgoing radiation response | Linear positive-coefficient vacuum wave operator, localized harmonic source and outgoing boundary | Green-function derivation plus independent flux normalization; source is not derived from collapse |
| Dwarf/SPARC sensitivity | Same data selections and phenomenological addition as predecessor; spherical dilation | Finite no-refit comparison only; observational likelihood not computed |
| Driven cosmology preserved | Full background/perturbation solution | Not addressed by a complete theory; constant-chi diagnostic worsens as chi falls |
| Mass function and cluster profile selected | Formation, capture, fragmentation, transport, initial inventory | Unresolved; no substitution of equilibrium for selection |

## Adversarial reconstruction

At fixed L, I scales as t^-2, so C scales as t². The chemical identity subtracts C, because the density derivative of L²/(2I) is -Omega² r_perp²/2. Eliminating U from mu_c M-E therefore contributes -4C, not +C or -2C. Along L(M), the additional term is Omega M dL/dM=2alpha C. These are the critical signs.

The stationary theorem allows nonspherical axisymmetric shapes but requires rigid rotation and no extra circulation constraints. The finite experiment instead keeps a spherical shape and minimizes only dilation. Its fitted diagnostic must not be described as solving the theorem's rotating equilibria. At large spin flattening and mass shedding can dominate. A whole closed system can store angular momentum in distant low-mass material; a local stationary point is not a global minimum.

Kelvin circulation does not imply zero total angular momentum of an irrotational patch. Tidal torques and orbital motions remain possible. Smooth single-stream circulation conservation can fail as a description at multistreaming or singularities; no collisionless extension was supplied here.

For the local phase test, the fixed-p Hamiltonian must be formed before eliminating X. Eliminating X at prescribed v instead changes the thermodynamic control and assumes an external source of work. The two calculations legitimately differ. The fixed-p Hessian has Schur complement (3y+q-2)/(y+q), verified against the full 2x2 matrix. h=0 in time integration avoids claiming an isolated calculation while imposing a nonzero cold reservoir.

The drive/rotation intersection combines two local diagnostics with k=1/r and negligible mediator gradients; it is not valid for arbitrary wavelengths or a solved disc. A nonzero cosmological background X would mix the scalar sector; the zero-background decoupling cannot simply be reused.

The radiation formula uses real-source harmonic amplitudes, which fixes the factor of 1/2 in phase-averaged flux. Fourier convention is Jtilde(k)=integral J(x) exp(-ik.x) d³x. The Gaussian curl example gives an angular factor 8pi/3, and no spurious source monopole. Below the gap, steady harmonic radiation vanishes, but finite pulses can have above-gap tails. The dynamical-chi radiation channel is outside the exactly fixed-chi benchmark and needs finite-compliance recalculation.

## Verification and provenance

run2: 24/24 checks; feedback_run: 14/14; export_run: 6/6. The baseline empirical comparison reproduces its predecessor and uses 10/17/21/56 objects without refitting. Initial run: one failed structural-equality check, retained with original source, corrected only by simplifying the symbolic difference in checks_v2.py. This was not a failed physical model. All manifests are checked separately for hashes/status.

The figure was rendered and visually inspected. It shows trial-profile sensitivity, a conditional phase/curve intersection, and a homogeneous constant-chi growth diagnostic, not predictions from a formation simulation. Final mathematical proofreading covered only this checkpoint's prose and equations. No unrelated historical labels, data or manuscript files were changed.
