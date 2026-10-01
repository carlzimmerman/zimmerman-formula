# Exact-kick bounded continuation — 27 September 2026

**Result: the angular integration is repaired, but the collapse benchmark is not numerically stabilized.** Exact conditional escape fractions and second moments remove the64-direction estimator from the same one-daughter closure. Both the default five-step and every-step trigger schedules retain appreciable timestep, resolution, or tiny-input sensitivity. No event interpolation was added, and these runs do not establish the cause of the remaining sensitivity.

## Implementation and validation

`DERIVATION.md` gives the exact spherical-cap integral. `exact_moments.py` handles zero speed, zero kick, all-bound, no-bound and the finite-measure zero-energy degeneracy. Main direct Cartesian angular quadrature passes **14/14**. Mutation deleting the nonzero conditional mean fails exactly three partial-bound moment controls (**11/14** pass), before any collapse runs. This is a scientific mutation failure, not the earlier corrected output-serialization error.

`engine_exact.py` changes only the exact-sampler import/replacement and configurable positive-integer trigger cadence (tested1 and5, default5). Source force refresh, constant angular-momentum coefficient0.25, phase rules, conversion threshold, daughter moment closure and cooling logic are otherwise byte-preserved. See `engine_exact.patch` and `clone_provenance.json`. The unchanged engine's historical docstring describes64 directions and is superseded by the patch.

The original engine SHA-256 remains `35f5cb01d74d197280ada3b5fed5718617bdd3c7b4c4469f2ef2af3d4be62fbf`. The constant-spin initial profiles are hash-identical to the prior matched force-refresh benchmark for each directly compared N and spectrum shift. No original source was changed.

## Matched bounded experiment

All **28 sequential runs finished in152.26 seconds**, with no cooling, M0=1e12 solar masses, kick600km/s, constant spin0.25, original softening0.2kpc, neighbor count0.04N, N=600/1000/2000, eta=.03/.015, trigger cadence5/1, and both a0 footings9.3603e-11 and1.1312e-10m/s². Four additional cases within those28 use N600, eta.03 and P(k) multiplied by1+1e-7, one per footing/cadence. Outputs use the prior400-point radius grid and original time-averaging prescription. Full values are in `TABLE.md` and `results.json`; all pairwise metrics are in `comparisons.json`.

Here hmax is max g_dark/a0 inside the source-defined final R200. The conversion fraction divides total converted mass by the final enclosed dark mass atR200, exactly as in the prior benchmark; it is not the fraction of the initial total dark mass. Converted-mass comparisons are separately recorded to distinguish denominator changes.

| Diagnostic | Canonical | Alternate |
|---|---:|---:|
| Cadence5: hmax change on halving eta, N600 | -15.012% | -1.710% |
| Cadence5: hmax change on halving eta, N1000 | +18.259% | -10.791% |
| Cadence5: hmax change on halving eta, N2000 | -6.146% | -10.246% |
| Cadence1: hmax change on halving eta, N2000 | +1.111% | -13.660% |
| Cadence1: hmax change N1000→2000 at eta.015 | +0.381% | +4.179% |
| Cadence5: tiny-spectrum hmax change | -0.227% | -16.784% |
| Cadence1: tiny-spectrum hmax change | +32.656% | -5.071% |

Cadence1 improves the canonical nominal grid: its N1000/2000 half-step hmax values are0.404685885/0.406229496. That apparent agreement is insufficient: the canonical N600 tiny-spectrum case changes hmax from0.288794634 to0.383103838 (+32.656%), despite exact angular integration. On the alternate footing, cadence1 N2000 changes0.370358620→0.319767556 (-13.660%) on halving eta.

Conversion remains sensitive as well. For cadence5 N2000, halving eta changes converted mass by-35.164%/-33.534% (canonical/alternate). The tiny-spectrum cases at cadence5 change converted mass by+25.545%/-35.445%. At canonical cadence1 N600, conversion fraction appears unchanged to0.080% on halving eta while converted mass changes-9.366%; this demonstrates why the denominator must be retained explicitly.

Relative to the prior64-direction force-refresh run, canonical exact moments at cadence5 change hmax by+6.293%,+2.401%,+2.399% for N600/1000/2000. The same comparisons change converted mass by+16.458%,+30.810%,+54.564%. Small shifts in one force statistic do not imply that the original stochastic conversion history was adequately resolved.

## Scope and next implication

The analytic kick operator is a useful deterministic improvement with no new fit. It is the angular-sampling limit at a fixed event state, not an exact solver for subsequent daughter kinetics. One-shell second-moment closure, discrete phase detection, threshold firing times, rank-neighbor pressure, finite shells, softening, and the integration scheme remain unchanged. A fixed neighbor fraction does not establish convergence at fixed physical smoothing width.

The data refute the proposed sufficient diagnosis that the64-direction sampler alone explains the reported benchmark instability. They do not prove that event-time interpolation alone will fix it, nor do finite grids exclude eventual convergence of the model. The next bounded numerical test should localize turnaround/pericentre and pressure-threshold events consistently, retain exact moments, and repeat matched timestep and tiny-spectrum controls. Until such stability evidence exists, these trajectories cannot promote CFG5's failed or passing observables to converged physical claims. No covariant action, causal completion, parameter removal or derivation of kappa follows from this change.
