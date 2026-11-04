# CC10 resonance-memory checkpoint

The fixed-tree, empty-neutral vacuum response is now computed on actual late
charged-scalar orbits and continuum distributions. A stationary inverse/BW
averaged at each field phase is **not quantitatively justified throughout
this late window**. This is a statement about the specified fixed-width
dilute-source model; full in-medium matching and a new coupled history remain
open.

Use `response_api_v2.py`. Its `orbit_response` integrates the actual four-state
production Gram and neutral width matrix over radial cells and pair angles,
retaining periodic detuning, continuum phase support, neutral coherence and
delayed occupation. It returns a physical pair rate, full positive parent
density per n+ n-, positive coarse-grained injection with a quantified closure
error, and delayed matrix evolution via `parent_decay_step`. Charge internal
degeneracies and CT09 fC=2 fS are restored in the physical density normalization.

| Tc/mu | Dynamic pair sigma v | Stationary pair sigma v | Ratio |
|---|---:|---:|---:|
| 1e-5, fine endpoint quadrature | 57.75763 | 63.13678 | .914802 |
| 5.68360e-6, interpolated shape | 129.78327 | 147.24245 | .881426 |
| 3.11923e-6, interpolated shape | 52.99310 | 361.93070 | .146418 |
| 1.71187e-6, interpolated shape | 7975.04800 | 888.82121 | 8.97261 |
| 1e-6, fine endpoint quadrature | 13920.75070 | 1977.91073 | 7.03811 |

Rates are in mu^-2. Only endpoint shapes are saved physical distributions;
the interior table labels its endpoint log-shape interpolation explicitly.
All orbit centers/amplitudes are recorded. The dense `run_dense001/result.json`
contains all 80 saved late orbits, normalizing interpolated shapes to the saved
charged number. Its ratios range .090929–9.31691; nine finer radial/angular
repeats differ by at most .3073%.

The incoming continuum itself changes regime: |C(Torbit)| is .16660 at 1e-5
and .999561 at 1e-6. Its inverse RMS detuning is .33746 and 33.732 orbital
periods. The neutral Gamma/omega ratio alone would not reveal this.
Direct empty-parent ODE integrations over 32 periods agree with the actual
Floquet response to 2.1e-6 and 2.1e-5 in two endpoint pair-mode controls.
Linearizing the actual mass detuning costs at most 1.61e-5 Gamma_min in those
checks. The exact-s cross-section normalization control passes. The neutral
occupation remains tiny: parent density is 9.38e-31 and 1.89e-35 mu³ versus
one-sign charged density 6.37e-21 and 1.84e-24 mu³ at the endpoints.

All source/exit matrices retain the CT09 four-state basis. Actual daughter-pair
Gamma matrices from `../cascades/run_basis002/result.json` contract against the
computed density and sum to the total neutral exit trace. The total rate keeps
mode-by-mode time dilation. Separate channel contractions on the integrated
density have a boost discrepancy bounded by 6.76e-6 initially and 6.76e-8
finally; retain momentum-resolved rho for an exact full parent evolution.

The passive fixed-width response obeys the derived gain bound
4 Tr(G Gamma^-1)/M³=15741.999837 mu^-2, independent of periodic sideband
redistribution. This bounds this reaction kernel, not all physical channels
or a hypothetical occupied active medium. The optional positive injection
Gamma^(1/2)rho Gamma^(1/2) preserves the total exit trace but is a separate
secular closure; its difference from {Gamma,rho}/2 is .0255–.0403% in the five
tested snapshots.

Using the dense multiplier along the **unchanged old trajectory** increases
its inverse-yield optical depth by 4.84524, yielding the diagnostic
1.68875e-13. This is not a new physical relic abundance: the changed source
must be coupled back to f, daughter forces, scalar action and one energy ledger.

First missing implication: dynamically resumming the retarded charged-pair
self-energy and occupied daughter correlators, including dispersive matching,
into this orbit response. Static incoming-width resummation changes the
endpoint rates by 1.88% and .194%; this is a discriminator, not a rigorous
bound on its dynamic counterpart. The exact tree pole/vacuum alignment is
also not full matched finite-mass physics. Once those inputs are fixed, the
quasi-periodic orbit response may be local in cosmological N: the envelope
variation/Gamma gap diagnostics are about 2e-7 initially and 6e-11 finally,
while the rapid orbit itself is already retained. This remains conditional.

`run_response002` and `run_dense001` are completed fresh v2 records; their
wall times were 44.89s/66.79s and measured peak RSS 328.55MB/255.07MB.
The failed `run_response001` and original source bytes remain intact; it
failed an auxiliary opposite-phase comparison, corrected only in separately
named v2 files. All three manifests validate. Exact inputs/hashes, commands,
limits and outcomes are in `PROVENANCE.json` and the manifests. No prior
scope, Git state, installation, queue or external message was changed.

See `DERIVATION.md` for normalization, retained correlations, passive bound
and reduction conditions; `SOURCES.md` for the checked primary kinetic source.
