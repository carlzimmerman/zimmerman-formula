# Audit of the photon-recycling extension

Outcome: finite numerical assertions verified within the stated reduced models;
finite-rate full collision chemistry and the parent galaxy target remain open.
This is self-review, not an independent-agent review.

## Evidence and provenance

Six completed manifests, no failed pinned runs in this stage:
- run_photons:24 dynamic radiative trajectories at6 shared choices.
- run_fast:24 infinite-collision-limit trajectories at those same choices.
- run_audit:7 refinement/closed-box trajectories plus geometry, rate quadrature,
  Jacobian, thermochemical and discrete detailed-balance checks.
- run_limits:2 trajectories checking the thin limit and fast-chemistry refinement;
  exact integer stoichiometric conservation and the photon-mediated DR cycle.
- run_figure and run_figure_v2: same data, revised annotation placement only.
  v1 is retained for provenance; v2 is the visually checked published figure.

All execution argv, dependency hashes, software versions, resource bounds and
output hashes are recorded by the mathbox bounded runner. VALIDATION.json records
fresh validation against current inputs. Provenance validation is not physical
validation. Regeneration must use new output directories; pinned inputs remain
immutable. The implementation uses Python3.9.6, NumPy1.26.2, SciPy1.11.4,
Matplotlib3.9.4, PYTHONDONTWRITEBYTECODE=1, OPENBLAS_NUM_THREADS=1.

Exploratory unpinned checks exposed excessive nonlinear ledger drift when the
fast model evolved log-temperature. Before pinning, it was changed to evolve
matter energy directly, with monotone thermochemical inversion. Independent
kinetic, binding, photon and escaped-energy terms are used in the dynamic model;
conservation is checked, not enforced by overwriting a residual. In the fast
model linear energy exchange is tracked directly and thermochemical inversion
supplies the temperature. No post hoc energy adjustment is made.

## Checks

The photon source and sink are constructed from the same sigma and quadrature
weights. The Planck/Saha stationarity test checks conventions and stimulated
emission, but is not independent certification of the inherited dipole spectrum.
That spectrum's independent continuum checks remain in the preceding stage.
The separate prior optically thin solver supplies an implementation cross-check.
At five temperatures, order6 photon quadrature agrees with earlier direct
spectral integrals to .063% for atoms and .113% for total molecular capture.
These are finite samples, not uniform error guarantees.

The escape geometry is independently integrated over its chord-to-boundary
probability density. Value errors are <=1.53e-11 at the tested optical depths;
finite-difference derivative errors are <=1.85e-7 absolute. The solver's full
analytic Jacobian directional error is2.28e-9 relative. The instantaneous
energy-ledger derivative is zero to4.05e-16 relative in the test.

Order3 has939 photon groups, order6 has1878, order9 has2817. Frequency and time
refinement are combined in the3-to6 comparison;6-to9 uses the same tight ODE
rtol and isolates frequency resolution. Dwarf values in the headline table use
order6; disk and cluster use order9. Only the selected shared point is refined
to those orders. The main scan is not claimed uniformly converged everywhere.

The fast limit solves a positive-coefficient cubic in log ionized fraction,
retaining tiny neutral abundances when x rounds to1. Its analytic heat capacity
is checked against an independent energy derivative. The equilibrium molecular
cap uses exactly the retained BO convention mu_A=1, mu_AX=100*101/201, weight147.
It is not the old LCAO cap or the previous irreversible kinetic cap.

## Interpretation limits

The moment escape closure assumes homogeneous emission and absorption. Repeated
chemistry is dynamic, but spatial self-shielding, nonuniform re-emission and
angular radiation fields are unresolved. It is not a full3D transport solution.
Stored radiation is included in energy, not added to a live gravity solver.
Photon recoil, relativistic corrections, finite-mass electronic corrections and
spin/exchange projections remain omitted. At alpha=.2 the characteristic
relativistic correction alpha²=.04 exceeds numerical convergence errors.

The radiative closed box has an extra invariant: total photons minus a-2t
is zero for the ionized initial condition. This is a photon/chemical count
constraint of the retained reactions, so closed-box stationarity does not imply
relaxation to a unique unrestricted Planck equilibrium. Direct collision
reactions can break that additional invariant while preserving charge and energy.

The direct-collision model is ONLY the infinitely fast limit. No absolute rate,
timescale ordering, or rigorous bracketing statement for intermediate rates was
established. Both limits omit additional chemical species. The six shared
parameter choices do not exhaust continuous parameter space. The inherited
80%/20% screen is operational, not a fitted observational likelihood.

Energy/charge conservation, molecular abundance, repulsive electric coupling,
orbital tethering and agreement with the acceleration relation are different
claims. Only the first two are tested here. No galaxy-type switch is used, but
input mass/radius proxies do not demonstrate spontaneous morphology selection.
