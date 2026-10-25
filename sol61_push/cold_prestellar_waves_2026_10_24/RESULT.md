# CCT-007: real wave transport, no acceptable four-dwarf remnant

There is a concrete positive result inside this conditional continuous-field model: pre-stellar self-gravitating collapse produces outgoing positive-energy waves and exports angular momentum. That also occurs without the imposed gas driver. The tested histories nevertheless fail to produce compatible Draco/Sextans structures or establish protected stars. Efficient cooling alone is not the missing four-dwarf selector.

These are finite angular-Galerkin calculations for the NEW CCT-003 wave/two-potential candidate. They are not tests of current v3s, AeST or retired SCT-M, and not evidence that nature uses this field or lacks particles. Numerical energy/J closure does not by itself establish convergence to the full 3-D PDE. Angular spin transport is still sensitive to truncation.

## Model and physical prescription

    i eta partial_t psi = -eta^2 Laplacian psi/2 + (Phi_c+Phi_g) psi,
    Laplacian Phi_c=4 pi G |psi|^2,
    M=integral |psi|^2 dV,
    Jz=eta sum_lm m integral |u_lm(r)|^2 dr.

The isolated Poisson potential is solved by multipoles, not periodic gravity. The stellar-sector extra Xi force does not act on cold material. Gas is spherical, so its torque vanishes. In the source-free case the only redistribution is the field's nonlinear self-gravity; there is no binary-collision term or phenomenological cooling drain in the interior.

One common imposed history uses eta=3000 pc km/s; initial cold mass=5.364*200 times total formed stellar mass; length unit=observed stellar spherical half-light radius. A finite l=0/l=2 cloud with incoming radial speed 10 km/s and unequal rotating components evolves in a gas potential that deepens then disappears. Gas is absent after t=24; evolution continues to t=160. Initial clouds are already collectively bound. This is collapse/relaxation of supplied bound material, not proof of the origin of that supply or capture of an initially unbound cosmological field.

The inventory ratio, 200-times-formed catchment, initial angular mixture, gas chronology and eta are stated benchmark assumptions. Eta is a Draco-scale choice, not a derived constant. Using observed stellar radii to set initial units makes this a data-conditioned trial family, not an independent prediction of assembly sizes. Sextans' formed mass is the disclosed approximate CCT-006 sensitivity, not a measured global SFH. No per-galaxy retuning followed the outcomes.

## Does collapse actually make escaping waves?

Yes, in the finite simulations. It is not inferred just by solving an energy inequality. Mass flows outward, the absorber removes positive total Hamiltonian energy, and removed mass, energy and angular momentum are separately recorded. The source work integral is explicit:

    dEc/dt |_source = integral rho_c partial_t Phi_g dV.

The gas energy reservoir/reaction is not simulated. Closing the cold-field ledger with this external work does not prove that a physical gas feedback mechanism can power the prescribed history. The source-free control addresses whether wave emission requires that actuator.

Representative completed hybrid-grid runs:

| Run | Cold mass removed | Fraction of initial mass removed | Jz removed / initial Jz | Remaining mass |
|---|---:|---:|---:|---:|
| Draco, L=2, gas cycle | 388 million Msun | 37.2% | 29.5% | 656 million Msun |
| Sextans, L=2, gas cycle | 350 million Msun | 38.5% | 35.7% | 559 million Msun |
| Sextans, L=4, gas cycle | 339 million Msun | 37.3% | 51.4% | 570 million Msun |
| Sextans, L=2, no gas, smaller dt | 384 million Msun | 42.2% | 44.5% | 525 million Msun |

For the L=4 Sextans case the removed-energy/mass ratio corresponds to an equivalent asymptotic specific-energy speed ~34.8 km/s. This is a finite-boundary energy diagnostic, not a measured ejecta velocity or a single-frequency spectral decomposition. Its peak energy residual is 0.75%, Jz residual 2.6e-6 of initial Jz, and mass residual negligible. The aligned initial state and even-m symmetry give vanishing Jx/Jy.

The no-gas coarse-step control failed conservation and stopped at t=104; it is rejected. A four-times-smaller timestep rerun completes with peak energy residual 0.46% and Jz residual 0.12%. Thus outgoing waves in that controlled finite model do not require externally supplied gas work. They are consistent with gravitational binding energy being transferred into outward field gradients/modes.

The larger/stronger-boundary, finer-radial, smaller-dt Sextans L=2 test still ejects positive-energy mass (~35.4% at its farther boundary) and leaves a similarly excessive central mass. This supports the qualitative existence of transport and central overconcentration; raw loss fractions differ because the sink location, travel time and numerical parameters differ together. It does not establish fully converged angular transport.

## Does that export spin selectively enough?

Mass loss is not automatically spin cooling. L=2 Sextans removes less spin than mass: the retained field's average specific spin increases by ~4%. L=4 removes more spin than mass: the retained specific spin falls to ~77% of its initial value. The L=4 aperture inside 486 pc has specific Jz about 54% of the initial whole-cloud value. This is an Eulerian aperture comparison, not a tracked material parcel losing that fraction of its own original spin.

The change from L=2 to L=4 is physically informative but numerically important: the fraction exported is not angularly converged. Higher angular modes change mode coupling and the transport efficiency. Do not promote the 51% figure to a full-PDE or observational prediction. The incoming angular spectrum and the required cold spin are not measured by the stellar data used here.

There was also a seed issue. The base initial state already has a substantial l=0 component. A low-spin central remnant could partly select that material instead of creating it. A separate run initialized only l=2,m=1 and l=2,m=2, with no l=0 wave, generates ~14.1 million Msun in l=0, of which ~2.90 million lies inside 486 pc. Generating l=0 cannot be a mere coordinate-axis rotation. However, the whole central aperture remains dominated by other modes and its full-vector specific angular momentum is ~1.09 times the initial cloud value. It is not a successful low-spin core.

That seed-free branch has tilted initial J, so its recorded Jz-only sink ledger is insufficient to certify total vector-spin export. The analysis retains the initial/final/core J vectors and uses l=0 generation only as a mode-conversion result. Counterrotation and a vanishing single component are not silently called zero total spin.

## The main failure is the final profile, not the existence of waves

Sextans' L=4 gas-cycle run leaves ~185 million Msun inside 486 pc. The CCT-006 illustrative survey-fit Plummer profile puts only ~9 million there. Total retained mass is of the right broad order, but its radial partition is wrong. The seed-free run is an even sharper warning: it retains ~422 million Msun, close to the illustrative total target, while placing ~264 million inside 486 pc. Matching total cold mass does not close the galaxy problem.

Spherical-monopole stellar diagnostics, using the actual final shell profile plus the baryonic law once, give:

| Trial remnant | Predicted full-tracer sigma diagnostic | Observational reference |
|---|---:|---:|
| Draco L=2 long run | 35.4 km/s | 9.55 km/s |
| Sextans L=4 compact/extended populations | 24.0 / 20.7 km/s | 7.0 / 10.5 km/s |
| Sextans seed-free compact/extended populations | 24.8 / 21.3 km/s | 7.0 / 10.5 km/s |

These moment columns are not themselves selection-corrected lower bounds. Separately, the actual-position spherical Jeans diagnostic for the L=4 Sextans monopole is worse than the CCT-006 best fit by ~230 in twice negative log likelihood. This is not an exclusion probability: the simulated density/potential is nonspherical, a matching stellar DF is not constructed, and the earlier survey/quality caveats remain. It is a failure of the tested candidate remnant under the stated stellar model, not of every continuous-field theory.

Fornax/Leo I log-grid pilots flag very large stellar-virial contributions (~68/~79 km/s versus ~12/~9 observed), but their outer grids are inadequate for reliable physical wave propagation. Their lack of escape at t=60 is not evidence of a physical absence of escape. They do not establish an independently converged final four-dwarf verdict. No accepted control remnant was obtained, and the more carefully checked Sextans cases already fail the joint target.

## Are stars protected if born later?

No protected stellar population was demonstrated. The gas-cycle Sextans L=4 remnant's half-mass radius varies by ~35%, and its aperture mass by ~34%, over the final quarter. The Draco long run is also unsettled. At this normalization t=160 corresponds to ~198 Myr for Draco and ~847 Myr for Sextans. These durations must be reconciled with early stellar histories; delaying birth is not a free parameter licensed by the data.

The stellar-birth acceptance gate remains closed. As an explicitly counterfactual stress diagnostic, passive circular-orbit cohorts were inserted into the saved MONOPOLE histories and compared to an exactly frozen circular control:

* Draco born at t=30: late median radius ~2.07 times the frozen value; born at t=80: ~1.10, with velocity variance ~1.29 times frozen.
* Sextans L=4 cohorts born at t=30 or 80 expand by roughly 18–28%, depending on population/time.

These are not observed heating estimates, live stars, isotropic DFs, or a full nonspherical force calculation. Their birth velocities are already too large for the observed populations. Snapshot cadence and omitted nonmonopole forces limit their quantitative interpretation. They show why absence of stars during initial collapse does not prove absence of later disturbance.

## Auditing and next discriminating step

The finite Hamiltonian has independent checks: weighted radial gradient/kinetic identity, direct symmetric Green matrices vs production prefix sums, self-energy functional derivative, zero instantaneous self-torque, mass/energy/J ledgers, and a static linear-well control with all initial negative-energy bound-state overlap explicitly removed. That control stays at ~1e-25 bound mass rather than manufacturing capture. Code archives preserve the failed pilots and each solver revision.

The next requirement is selective assembly: create only the small permitted low-angular-momentum central component while retaining the large Sextans envelope and avoiding excessive central gravity in Fornax/Leo I. Stronger universal cooling would worsen this tested profile failure. A viable continuation must specify an independently constrained initial angular/energy distribution and gas chronology, achieve angular/radial/time/boundary convergence, retain full vector-J fluxes, and then pass a live stellar test. A new arbitrary per-galaxy cutoff or suppression factor is not that selector.

Commands and run parameters are in CONTRACT.md, REFINEMENTS.md, and the individual run JSONs. summary.json, verification.json, stellar_response.json, saved complex fields and wave_diagnostics.png preserve the actual evidence. Recorded wave runs stayed below 110 MB, far below the shared 1-GB cap. Host tides, cosmological supply and a physical gas-energy reservoir are absent. No heavy shared jobs, frozen criteria/publications, external chats, automations or remote repository state were changed.
