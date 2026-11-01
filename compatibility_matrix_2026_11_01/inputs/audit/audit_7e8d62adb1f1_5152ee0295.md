# XP-20261023 handoff

Base6bec89a36197ce50a3100b6ede5c02d019a3ad94; parent early_precursors_2026_10_23. Open objective unchanged: derive a cosmological core population and preserve dwarf fits, rotation curves, cluster lensing and growth.

Changed state: explicit preferred-frame expanding reduced action with physical P components, conserved comoving masses and mean-density subtraction. Hubble damping and work identity derived from it. MINISUPERSPACE.md supplies a dynamical homogeneous lapse/Friedmann extension and compatible pressure. Full covariant clock/metric constraint completion still absent. Simulations use imposed EdS, not the coupled scale-factor system.

Executed:48 baseline nonlinear/quadratic mode runs; six tighter canonical repeats; six initial-equilibrium-derivative comparisons; six large-scale growth cases and one tighter k1 repeat; independent Hamiltonian finite differences. Finite checks pass. Failed serialization run retained. All jobs finished, no active runs.

Findings: canonical .001 initial matter amplitude yields final cold contrast .0186,.04997,.03611 for unpolarized/stationary/tracking initial fields. Initial fields/momenta materially matter. Exact logarithmic W suppresses cold growth in all18 paired baseline same-endpoint comparisons. Some .01 initial cases hit the baryon .3 limit; this is not core formation. k1 total growth retains .95176,.96153,.95397 respectively, below inherited99% target. No population selector or fit preservation established.

Next dependency: spatially resolved nonlinear matter and field evolution from an explicit initial field spectrum, with the same action and homogeneous constraint/energy accounting, followed by a three-dimensional binding/fragmentation test. A 1D or finite-mode result cannot select 3D core masses. Field preparation must not be retuned separately to achieve desired outcomes. The relativistic initial state and covariance/constraint problem remain open; no need to repeat the isolated compact-seed cooling route.

Read RESULT.md and DERIVATION.md first. Use run/result.json, tracking/result.json and growth/result.json as separate experiments, not merged equivalent assumptions. action_v2/result.json supersedes only the failed action-check serialization attempt. growth_repeat is a tolerance check, not a new model. Checkpoint hashes cover all own artifacts. No edits elsewhere, no commits, no pushes.
