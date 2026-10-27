# Carrier-feedback handoff

Owned scope: sol61_push/carrier_feedback_2026_10_13/.
Starting shared revision db10b5368ceedbf32c88ae5372537e1406d222f7.
Publication parent 8112fa7975aa2283b062ea9361c0944271cef3a4;
branch codex/cold-energy-equations. Source reduction copied before computation.
Original goal remains OPEN.

Advance: use the existing conditional psi+b elastic process. Cold-source,
isotropic off-resonant contact scattering yields E'/E uniform on [1-a,1],
a=4r/(1+r)^2. At r~2 the mean loss is ~4/9, so the small-jump closure is not
admitted. A frozen-rate exact compound-jump versus diffusion comparison matches
moments one and two while failing moments three/four and introducing a false
13.1% heating tail at unit exposure.

Same-vertex rates give nu/Gamma=4 chi_b (mu/m)^2 v/epsilon. With unreplenished
exponential source depletion, first-event P=1-exp(-nu/Gamma). The declared
small-density/off-resonant grid has P<=about2.50%. chi_b is a defined regime,
not a proved bound for all quantum source states. The production shell violates
the threshold contact admission and is not covered. Recoil storage is returned
to daughters when the source decays; closed-sector permanent cooling is not
inferred from tagged-particle cooling.

Seven Lean statements: energy fraction, threshold mean, no heating per cold
collision, rate cancellation, small-density inequality, exponential probability
bound, third-moment generator discrepancy. No formal scattering/Poisson/kinetic
reduction theorem. 163 deterministic numerical checks; three rejected damaged
certificates; self-review only. No Lambda-CDM/MOND or new empirical data.

Next genuine admission: retain finite recoil jumps and live source conversion,
match resonance without double counting, derive an evolving source state and
its replenishment/energy flows. No arbitrary Gaussian bath or target selector
was inserted. Hot/collective sources are open and require a separate closure.

Hashes:
- INPUT_CARRIER_REDUCTION.txt: `f21a47e2ba689e28056fd3a920b1edb68b75085e80d2d033f1e820d44c643d66`
- check.py: `367681296ef34a97a61693c67eb67ce7bad27d4f8ee5ccd5f0dafa56806038fe`
- CarrierFeedback.lean: `1d3d2a75c72f2cf71aea945326d1db9e16ebff3e3a22e3928303a649c08992e3`
- run/manifest.json: `2bc2d1fc061f833055237891705882e133dd751c0f67d1e62a7b7495ea8e6c96`
- lean_run/manifest.json: `354462aa8659956548b89347df009c64b3a74366391d7f1a55afe9a84240a80d`
