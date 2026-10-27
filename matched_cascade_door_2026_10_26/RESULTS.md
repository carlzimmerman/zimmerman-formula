# A static-compatible local pumping window; formation remains open

The finite-mediator parent retains a nonzero local three-wave channel. A nearby
parameter window also changes compression work from negative to positive without
spoiling the inherited finite-grid galaxy law. The available slow-compression
gain is small, so this is a conditional component result, not a completed engine.

| Mediator range | Static law error | Exact local compression slope at q=80 | Maximum leading adiabatic mode-energy gain |
|---|---:|---:|---:|
| .15pc | .708955% | +.03915 | .07699% |
| .20pc | .708584% | +.10186 | .52604% |

The static density KKT residuals are 1.12e-9 and 7.92e-10, and angle/carrier
gradient residuals are below 5.70e-10. Independent NumPy/Torch static energies
agree within 1.07e-14. These are re-minimized states on the inherited grid,
not formation histories or continuum convergence evidence. Coefficients remain
assumed; no fit to new observations was made.

At q=80 in those states the exact parent cubic vertices are -5249.16 and
-4951.22 in the declared box/canonical normalization. The specified 5% weak-mode
normalization gives coupling scales .009687 and .009556 per Myr. Those are not
physical cooling rates or evidence that infall supplies the modes.

Checks performed:
- Reproduced the old q=80 local frequency and vertex to <1e-10 relative error.
- Computed exact finite-M quadratic polarizations and cubic coefficients at
  q=40,80,160,320 for .01,.1,1pc; 1pc is a statically failed control.
- Checked the cubic coefficient against a separate automatic third derivative
  of full canonical squares at four cases, agreeing within 1.3e-15 relative.
- Checked E=omega for normalized exact modes at the new static patches, within
  2.3e-16 relative, and the compression derivative at three decreasing steps.
- Preserved the first failed derivative audit. Its discrepancy was numerical
  cancellation; an exact coefficient-level simplification resolves it without
  relaxing tolerance. See DERIVATION.md and run_exact/stderr.txt.

Evidence: run_spectrum, run_exact_checked, run_static_window and run_pumping.
Each has a bounded-run provenance manifest. run_exact records the explained
failed diagnostic. Full derivation and assumptions: DERIVATION.md.

The source of the new result is the local matched action, not a theorem imported
from OpenAI/math. The literature scan helped select the transport question.
The scoped attribution result is in ATTRIBUTION.md.

Next obligation: obtain actual mode occupation and sustained mean-flow work
through a self-consistent nonadiabatic compression/shear or conversion calculation,
including reciprocal stress and an outgoing flux ledger. Classical zero modes
do not populate themselves under homogeneous adiabatic pumping. Another seeded
fixed-background resonance run would not settle this. No jobs remain running.
