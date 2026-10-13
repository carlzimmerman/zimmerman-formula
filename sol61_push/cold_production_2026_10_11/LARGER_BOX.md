# Nonlinear evolution in a twice-wide box

2026-10-11. Executes the next spatial test identified in
[ENSEMBLE_AND_BOX.md](ENSEMBLE_AND_BOX.md).

The earlier box used dq=0.4 and N=24. This run uses dq=0.2 and N=48:
the physical box side doubles and its volume increases eightfold, while
the componentwise Fourier cutoff and spatial resolution are held fixed.
The new box has its own physical source count and vacuum-grown covariance;
its initial state is not a tiled or rescaled copy of the old realization.

[larger_box_spatial.py](larger_box_spatial.py) expands the saved shell data
from `box_handoff_run` into 2,084 individual opposite-momentum pairs.
The Gaussian-to-classical handoff occurs at mean daughter charge 1e-4,
x=73.14666192. Covariance projection is checked before sampling. The source
adjustment and other matching qualifications of QUANTUM_HANDOFF remain.

The reproducible sample uses seed 471901. It has initial daughter charge
1.41693961e-4 and a source-amplitude adjustment of 2.08482405e-5. Despite the
same RNG seed label as an earlier run, this is not a mode-by-mode paired
realization: the momentum lattice and number/order of draws differ.

## Endpoint and diagnostics

At absolute x=100:

| Quantity | Value |
|---|---:|
| Daughter charge fraction | 0.69272369 |
| Total source charge fraction | 0.30727631 |
| Moving source charge fraction | 0.27106064 |
| Maximum total-charge drift | 2.49e-11 |
| Maximum reduced-energy drift | 1.16e-5 |
| Endpoint outer-mode charge | 1.55e-8 |

The time step is at most 0.005. Both pilot diagnostics pass, and the
[manifest](larger_box_spatial_run/manifest.json) validates against the saved
source and input state. [Results](larger_box_spatial_run/results.json) include
the conversion history and source-adjustment magnitude.

Substantial conversion and moving-source population persist in this box.
The daughter endpoint is higher than the five smaller-box endpoints, which
span 0.5966–0.6827. With only one larger-box draw, this difference cannot be
cleanly separated into finite-box bias and realization noise. The larger
box still has only about 20.46 effectively occupied pairs at handoff, with
about 22.1% initial daughter-charge relative standard deviation.

This is therefore a box-dependence test, not continuum convergence. No new
time-step or ultraviolet-cutoff comparison has been run for this larger box;
the energy and outer-mode diagnostics are useful but do not replace those
comparisons. Larger nonlinear boxes, more samples, expansion and quantum
correction control remain outstanding.

## Coldness is a separate structural check

[SPATIAL_ENERGY_BOUND.md](SPATIAL_ENERGY_BOUND.md) shows that the spatial
Hamiltonian itself admits a positive square decomposition when k>=1/d_0,
where d_0=(M/m-2)/epsilon. The present k=0.2000001 exceeds the threshold
approximately 0.100000025. The conserved surplus bounds the kinetic energy
throughout arbitrary source/daughter redistribution in this envelope.

Thus a moving-source fraction is not evidence that the combined material
has become hot. Conversely, a large daughter fraction is not evidence for
a final relic abundance. Both the structural energy control and the
approximation limits must accompany the production numbers.

The actual repository target remains open: this candidate has a concrete
formation calculation and classical coldness controls, but no established
source origin, selected abundance, universal halo response or vacuum-linked
acceleration scale.
