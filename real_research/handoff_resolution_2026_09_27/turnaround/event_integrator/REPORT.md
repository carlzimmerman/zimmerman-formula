# Event-localized KDK continuation — 27 September 2026

**The bounded event-localization improvement does not stabilize this shell benchmark.** It correctly locates smooth elementary events and conserves mass in every completed run. The full model retains substantial timestep and tiny-input sensitivity, while sorted-neighbor pressure and thin-shell force discontinuities prevent a narrow time bracket from guaranteeing a small event residual. No additional smoothing, collision rule or fitted regularization was introduced.

## Work completed and controls

`engine_events.py` is a copied no-cooling constant-spin exact-kick engine with event-localized trial KDK steps. Before accepting a phase or pressure sign-changing trial, it bisects the proposed step, applies source impulses at the retained event-side time, and refreshes forces. Turnaround, first pericentre and first subsequent apocentre use the source phase laws. Pressure is checked every accepted step; finite zero-time conversion cascades are explicitly handled. `ALGORITHM.md` states these choices, the limits and an exact neighbor-exchange pressure-jump example; `engine_events.patch` records the implementation changes.

The elementary controls pass **6/6**: smooth turnaround timing/residual, pressure-crossing timing, bracket width, second-order no-trigger harmonic KDK refinement, and retained-plus-escaped kick mass accounting. Deliberately applying events at the late endpoint fails exactly the four event-placement controls (**2/6** remain true). These controls were executed before the full benchmark and re-executed for the final evidence manifests.

All **12 sequential cases completed in 194.67 seconds**, within the ten-minute task cap: two actual N80 no-trigger runs, and ten triggered runs spanning both a0 footings, N600/1000, eta=.03/.015 and one N600 eta=.03 spectrum perturbation of 1e-7 per footing. The same initial profiles match the previous exact-kick benchmark hashes. The setup retains M0=1e12 solar masses, no cooling, spin0.25, kick600 km/s, softening0.2 kpc and neighbor fraction0.04. Individual runs had 48-second and 100,000-step guards; the driver had a 320-second aggregate guard and an alternate-footing admission guard. No guard was reached. No other job was touched.

## Results

| Footing | N | hmax at eta .03 | hmax at eta .015 | Half-step change |
|---|---:|---:|---:|---:|
| Canonical | 600 | 0.406319738 | 0.345743467 | -14.909% |
| Canonical | 1000 | 0.372223149 | 0.394485532 | +5.981% |
| Alternate | 600 | 0.275403821 | 0.352977374 | +28.167% |
| Alternate | 1000 | 0.399788823 | 0.343312600 | -14.127% |

Here hmax is max g_dark/a0 inside the source-defined final R200. With the spectrum multiplied by 1+1e-7 at N600 and eta .03, hmax changes by **-25.285% canonical** and **-8.432% alternate**. Converted mass changes by +2.496% and +2.223%, respectively. On halving eta at N600, converted mass changes by +12.084% canonical and -5.450% alternate. The complete force, conversion, pressure and event records are in `TABLE.md`, `results.json`, `comparisons.json`, and the per-case `events_*.json` files.

Actual N80 no-trigger runs give hmax 0.380717519 and 0.272246213 at eta .03/.015. This coarse-shell result is not a continuum convergence test; it shows that substantial sensitivity is possible in this driver without pressure-triggered conversion. The smooth harmonic control passes, but that does not validate nonsmooth shell trajectories.

All runs preserve total retained-plus-escaped mass to relative error at most **1.45e-16**. Localized event brackets are no wider than **9.537e-7 of the proposed timestep**. Nevertheless, phase velocity residuals reach **0.03954 km/s**, and a non-immediate pressure event has excess **1.2417 P_cap** at its event-side endpoint. The diagnostic thresholds of 1e-5 km/s and 1e-3 P_cap recorded in `comparisons.json` are post-run audit summaries, not predeclared evidence of a successful physical tolerance; both fail. A time-bracket criterion must not be substituted for those residuals.

## What remains, exactly

The source pressure estimator changes discontinuously when a finite-mass particle enters or leaves a rank-neighbor window. `ALGORITHM.md` derives its finite pressure jump at arbitrarily small radial separation. Therefore not every threshold event has a continuous root P=P_cap. The thin-shell sorted acceleration also jumps at rank exchanges, and the finite-step KDK endpoint acceleration can make its trial phase margin discontinuous. Tight bisection alone cannot repair either fact.

This experiment resolves the earlier missing bounded test: exact kicks plus phase/threshold event localization are insufficient to justify converged CFG5 trajectories. It does not prove that the continuum model has no solution or that one further numerical change will succeed. A scientifically specified continuation needs a consistent shell-rank crossing/force treatment and a justified stress or phase-space discretization, with convergence assessed at a fixed physical coarse-graining prescription. Endpoint-bracketed detection also leaves multiple undetected crossings possible. Selecting a smoothing width or collision impulse solely to suppress the observed changes would change the model and was not done here.

## Evidence and provenance

Both this lane and `kick_moments/` now have `controls_main_manifest.json`, `controls_mutation_manifest.json`, and `benchmark_manifest.json`. All **six validate as legacy computation-audit schema version 1**; `manifest_validation.txt` records the validator output. Fresh controls have observed start/runtime/status. Benchmark manifests honestly reconstruct approximate start times from result modification time minus recorded runtime and declare that limitation. Input hashes, source provenance, output hashes, explicit tested bounds and scientific failures are included. Version1 validation does not enforce resource caps or turn these finite results into mathematical proof. The earlier uppercase `MANIFEST.json` in the kick lane is preserved as bespoke raw metadata, not represented as skill-validated evidence.

Original engines and scientific source lanes remain unchanged. No numerical or physical closure, observational gate pass, derived kappa, or full-action stability is claimed.
