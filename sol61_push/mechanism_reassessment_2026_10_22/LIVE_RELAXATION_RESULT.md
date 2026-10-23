# Live conservative spherical response: a transient signal, not a damping-rate result

A self-consistent spherical particle-mesh evolution now perturbs one of the finite positive kinetic equilibria without friction or an energy sink. Its bulk-radius disturbance decreases over the observed time window at two resolutions, while total discrete energy is conserved to a few parts per million. However, control drift and resolution dependence of the injected perturbation energy prevent a quantitative relaxation-rate claim. The40-time-unit window also does not exclude later revival.

This tests a neighborhood of a chosen equilibrium. It is not collapse from a primordial distribution, a cold-fraction selector or a demonstration of asymptotic settling.

## Discrete Hamiltonian and initial state

Use the A10,ra1,gamma0.01,mass1 finite equilibrium from COLD_LIMIT_RESULT.md with fixed Plummer baryons. Sample radius from its enclosed mass and velocities from its positive f(Q) distribution using deterministic, unscrambled Sobol points. Pair inward/outward radial velocities to make the initial radial current vanish. The samples are spherical representative orbits, not a full3D particle gravity calculation; arbitrary orbital-plane orientation is immaterial to the imposed spherical average.

The perturbed case uses the canonical dilation x->1.05x and v->v/1.05. This preserves mass and each particle's angular momentum. It is a small artificial displacement, not a cosmological initial condition.

On radial nodes r_j with spacing dr, deposit particle masses m_j by linear interpolation. Define q_j=(sum_i<=j m_i)/r_j² and use the discrete potential

    U=sum_j dr r_j²[-q_j-ln(1-q_j)-q_j²/2]
       +gamma/2 sum_j m_j²/(r_j² dr)
       -mean_particles[1/sqrt(1+r²)].

The derivative with respect to a cell mass is the reverse cumulative sum of R(q)dr plus gamma rho_j. Differentiating its interpolation with respect to particle radius gives the radial field force. Add the exact Plummer force and evolve with kick-drift-kick. Thus force and reported energy come from the same discrete functional. Finite differences verify the force derivative, rather than comparing it only with a continuum formula that might not match the grid energy.

The grid ends at radius10; no accepted trajectory crosses it. The omitted exterior field energy for fixed enclosed mass is a constant for these configurations, not an energy sink. Below the first node, deposition is held in the first cell and its interpolated field force is zero; the baryonic force remains analytic. This core discretization needs convergence testing.

## Resolution and failed probe

The initial grid1024,N32768 probe reached the cap rapidly. One representative mass at its innermost radius contributes q approximately1.28 by itself, so that grid cannot resolve the central continuum with so few particles. The run aborted before serialization; its failure is documented, not interpreted as a physical instability. Subsequent errors serialize their diagnostic state.

Accepted runs:

| run | particles | radial nodes | dt | duration |
|---|---:|---:|---:|---:|
| control and dilation | 32768 | 256 | 0.005 | 40 |
| dilation time refinement | 32768 | 256 | 0.0025 | 40 |
| control and dilation spatial/sample refinement | 131072 | 512 | 0.0025 | 40 |

All completed without the cap or outer-grid abort. The larger particle count compensates for the smaller central cells; it is not an independent particle-only convergence study. Accepted direct runs took approximately8–67 seconds each on one numerical-library thread.

## Conservation and response

Across accepted runs, the maximum relative energy drift is4.02e-6, maximum force finite-difference error3.81e-6 and maximum absolute angular-momentum error3.10e-14. This verifies the implemented short-time Hamiltonian response, not the full continuum theory.

Compare the perturbed RMS radius with its matching unperturbed control. Exploratory early and late windows are[0,10] and[30,40]; they were chosen after the coarse response was seen.

| resolution | early RMS difference | late RMS difference | late/early |
|---|---:|---:|---:|
| coarse | 0.0376324 | 0.00923206 | 0.2453 |
| refined | 0.0370164 | 0.0108156 | 0.2922 |

This decrease is consistent with loss of a coherent bulk displacement into orbital structure while total energy remains in the system. The data do not isolate phase mixing from all discretization effects or establish an irreversible decay law. No exponential damping fit is justified from this interval, which contains only a small number of broad excursions.

The maximum difference between the two control-subtracted response curves is0.0051211; the RMS difference is0.00299259. Halving dt at fixed coarse mesh changes the raw RMS-radius curve by at most0.000785748. The unperturbed control itself drifts by up to0.0198541 on the coarse mesh and0.00959101 on the refined one. Control subtraction is therefore necessary, but does not eliminate all initialization bias.

Crucially, energy conservation must be judged relative to the perturbation, not only the binding energy. The dilation injects0.000544542 on the coarse mesh and0.000774822 on the refined mesh. Those differ by about42.3% relative to the coarse value. Maximum energy drift is0.349% and0.140% of the respective injected energies, so numerical energy loss is small, but the initial perturbations are not yet equally calibrated across meshes. This prevents a claimed converged damping rate.

## What to improve next

The continuum f0 is not exactly an equilibrium of the discretized chemical potential. Constructing a positive equilibrium of that discrete energy, with the same mass and distribution family, should separate initialization drift from physical response. Then repeat the dilation at matched injected energy, extend the duration, and independently vary particles and radial mesh. Retained mass, fine-grained invariants and observational-law agreement still need separate tests.

This live test does not circumvent PHASE_PACKING_RESULT.md: it starts near a specified distribution and preserves particle masses and angular momenta. It does not show collisionless creation of a higher phase-space occupation or movement along the cold-limit family.

## Evidence and plot

live_analysis_run/manifest.json validates;5 numerical-verification checks pass. The bounded run audits and plots the recorded simulation artifacts; it does not claim to have resource-bounded the original evolutions. Those were directly executed with live_relaxation.py and record their configurations, conservation diagnostics and wall times. Their hashes, the simulation source and the initial equilibrium record are inputs to the analysis manifest. The failed first probe has no JSON output and is disclosed above. No new mutation was performed.

The plot live_relaxation.png shows raw RMS radii, control-subtracted response and energy drift. It was visually inspected. Windows and thresholds are documented as post-probe diagnostics, not preregistered evidence of a new physical effect. Interpretation is self-reviewed.
