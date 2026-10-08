# Validation and scope

All nine saved computation manifests validate. A valid manifest certifies provenance, not the mathematics.

| Run | Passed checks | Interpretation |
|---|---:|---|
| runs/filter | 37/40 | Expected failing negative control |
| runs/memory | 37/40 | Expected failing negative control |
| runs/none | 40/40 | Main result |
| threshold_runs/exponent | 24/33 | Preserved first implementation with precision error |
| threshold_runs/none | 33/35 | Preserved first implementation with precision error |
| threshold_runs/sign | 26/35 | Preserved first implementation with precision error |
| threshold_runs_v2/exponent | 24/33 | Expected failing negative control |
| threshold_runs_v2/none | 35/35 | Corrected threshold main result |
| threshold_runs_v2/sign | 28/35 | Expected failing negative control |

The first threshold formula evaluated I_x at x almost equal to one. At epsilon=2.6283e-12 its relative integral error was about 6.08e-10; the complementary-argument formula agreed with 60-digit arithmetic to about 8.32e-16. Finite differences magnified the original error. No tolerance was relaxed. Original code, contracts and failed outputs remain unchanged.

The final threshold exponent control changes beta from -1/3 to -1/2 and fails the three-halves asymptote; the sign control makes the low-source constitutive force negative. The other controls omit the filter variation or the memory initial term and fail the corresponding independent identities.

Self-review checked the positive-response sign, the finite-cutoff remainder, derivative asymptote, the finite-norm source, SU(2) cancellation, QOQ missing term, heat/source variation and retained memory endpoint. No independent-agent audit, BFSS spectral simulation, physical data fit, zero-mode metric analysis or 32pi normalization derivation was performed.
