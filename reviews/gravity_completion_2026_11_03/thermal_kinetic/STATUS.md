# TK08 checkpoint

The collisionless occupation force can bridge the equilibrium gap in the
tested leading global action. A conditional homogeneous first roll remains
bounded (x_max about 2.9), with explicit xi=.02 expansion and validated source
energy exchange. This is not yet a complete production history.

The actual neutral messenger vertices matter. Origin scalar-pair inverse
reactions can be fast compared with H but are slow compared with the first
field roll. The dominant SU3 neutral cascade returns to charged scalars:
B3->A3+R, then A3->charged scalar pair. It must not be counted as radiation.

The new nonthermal inverse-resonance integral uses the actual frozen FD
distribution, rather than a massive equilibrium distribution. On the
fixed-number minimum curve, even the optimistic absorbing-parent rate falls
from thousands of H (canonical) or hundreds of H (protected) at Tc/mu=.003
to below 1e-7 H at .002. This exposes the early population/field feedback
window. It is not a total annihilation bound or proof of complete depletion.

The heavy charged carriers can become kinetically cold. They do not thereby
become the neutral photino. The charged companion abundance and actual
photino yield remain unresolved, as does the complete DE/cold-matter goal.

## Evidence

All eight current successful v2 records have status `completed`, use one
numerical thread, wall<=240s, CPU<=235s and measured RSS. Commands and full
input closures are in the corresponding manifest and contract JSON.

- `run_stationary_002`: finite force/minima; FD quadrature, eigen-slope,
  energy derivative, positive monotone mass and expansion identity controls.
- `run_rates_001`: actual projected neutral scalar->charged light pair
  partial widths; conditional equilibrium detailed-balance rates.
- `run_branching_002`: all immediate physical scalar/fermion partial widths
  of those neutral parents; charge-adapted full Takagi basis.
- `run_roll_001`: two integration tolerances, first 250 origin-roll times,
  initial field from equilibrium spinodal, zero velocity, frozen-only source.
- `run_audit_001`: independent light-only/full projection agreement and
  conditional undepleted initial yield bookkeeping.
- `run_cascade_002`: exact origin SU3 A3 daughter decay into charged scalar
  pair; no open tree scalar/fermion neutral exit.
- `run_nonthermal_002`: actual frozen-FD scalar-resonant inverse rates,
  MB detailed-balance limit and doubled quadrature control.
- `run_force_budget_001`: at Tc/mu=.002, any stationary charged-supported
  trap on the tested 1151-point x<=200 grid needs Y>=1.16e-10 canonical or
  5.14e-11 protected, respectively 6.13e4 and 8.03e5 times the 10%-DM charged
  relic gate. This assumes the recorded leading T0+other-equilibrium force;
  frozen neutral sources, nonstationary capture and later annihilation are
  excluded from this finite control.

Preserved failures: stationary001 used an excessively strict endpoint
quadrature assertion; branching001 failed to adapt the charged zero Takagi
subspace correctly; cascade001 and nonthermal001 failed JSON serialization
of a numpy boolean after calculation. Their exact source bytes are retained
in `inputs_historical/`, SHA256 matched to the original manifests via
`inputs_historical/archive_map.json`. Failed results are not success evidence.

## First missing coupled leaf

Evolve the charged fermion and charged scalar momentum distributions,
neutral resonances and their actual irreversible exits, alongside X(t).
Source energy and depletion must change together. Early resonance losses
can weaken the same restoring force that produced the stationary bridge;
late channels close on the undepleted curve. The completed first-roll run
does not cover the required Hubble cooling interval. A justified averaged
oscillation treatment or stiff multiscale solver is needed before claiming
outer-vacuum recapture or final abundance.

No extra portal, package installation, Git mutation or queue was introduced.
