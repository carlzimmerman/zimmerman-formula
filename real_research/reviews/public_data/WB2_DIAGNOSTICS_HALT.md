# WB-2 diagnostics — BOTH stop-triggers fired → HALT before the Monte-Carlo (relay to Fable)

*C. Zimmerman, 2026-06-09. The two gating diagnostics (`wb2_diagnostics.py`) on the 73,670-pair selection. Per the standing block, D1 σ/v_N > 0.3 and D2 super-escape > 15% in the deep bins are **stop-and-report triggers**. Both fired. The Monte-Carlo build is HELD until the state is relayed.*

## The two numbers Fable was waiting on
| g_N/a₀ | N | median v_t | **D1 median σ/v_N** | **D2 f(v_t>√2)** |
|---|---|---|---|---|
| 316 | 27,219 | 0.672 | 0.046 | 0.056 |
| 32 | 21,604 | 0.682 | 0.072 | 0.084 |
| 5.6 | 6,822 | 0.712 | 0.111 | 0.119 |
| 1.8 | 4,403 | 0.746 | 0.145 | 0.140 |
| 0.56 | 2,781 | 0.794 | 0.188 | 0.178 |
| 0.18 | 1,744 | 0.884 | **0.252** | **0.228** |
| 0.06 | 955 | 0.968 | **0.340** | **0.287** |
| **deep (g/a₀<0.3)** | | | **0.306** | **0.267** |

## What it means (the honest decomposition)
**The raw deep-MOND rise (0.67→0.97, a ~43% velocity excess) is substantially MEASUREMENT NOISE + RESIDUAL CONTAMINATION, not a clean physics boost.** Two independent, model-free lines:
1. **D1 — noise inflation (Eddington).** Median σ(v_sky)/v_N reaches **0.31–0.34 in the two deepest bins** — measurement noise is ~⅓ of the signal there. Critically, σ/v_N **rises in lockstep** with the median v_t (both monotonic into deep-MOND), which is the *fingerprint* of pure noise inflation: noise adds to |v| preferentially where the intrinsic orbital velocity is smallest (v_N ~ 0.17 km/s in the deep bins, vs σ_vsky ~ 0.05 km/s and growing). A monotonic rise into the deepest bins is therefore *expected from noise alone*.
2. **D2 — super-escape floor.** **27% of the deepest bin exceeds Newtonian escape velocity** (v_t > √2), and 16% exceed even the deep-MOND escape ceiling (v_t > 1.9). Bound orbits cannot do this under *either* theory → ≥27% of the deepest bin is unbound junk (noise + hidden triples + residual interlopers). This fraction also rises in lockstep with the median → **the rise and the junk share a cause.**

## D3 — selection provenance (the count mismatch is real)
The 73,670-pair selection matches **neither** published sample — Chae (~26.5k) nor Banik's ultra-clean (~8.6k). It is a **HYBRID, and looser than both**: cuts = RUWE<1.4 (both), parallax_over_error>20 (both), R_chance_align<0.1, dist<200 pc — but **no separation-range cut and, crucially, no radial-velocity triple-screen** (Banik's clean sample uses RV to reject triples). A looser sample is *more* contaminated — consistent with the 27% super-escape fraction. **Mass estimator:** M_G → mass via a rough single-star MS relation M/M⊙ = 10^((4.74−M_G)/8.75), *not* the Pecaut–Mamajek tables Chae uses; a separation-dependent mass bias would masquerade as the velocity trend and is unquantified here.

## Consequence for the Monte-Carlo (decision rules, now triggered)
- **D1 rule fired:** the MC's **noise-injection model is promoted to the PRIMARY systematic** — not a refinement. The forward model must reproduce the σ/v_N(bin) profile above, or it is adjudicating its own noise.
- **F4 (hidden triples) confirmed central** by D2's super-escape floor.
- **The writeup must state** (locked): the raw 0.97 deep-bin ratio is **noise-dominated pending deconvolution**; the physics question is whether *anything* survives subtracting the D1 noise floor and the D2 unbound fraction — Fable's "~15–20% survives, not all 43%" is now the explicit, testable hypothesis, and it may be ~0.
- **HELD:** no MC adjudication, no verdict, until this is relayed and the noise+triple deconvolution is specified in `wb_mc_preregistration.md` (WB-3) with the σ/v_N profile as a forward-model target.

## Status: HALT (standing-block triggers honored)
Relaying to Fable. The next step is NOT the adjudication MC but the **noise/triple deconvolution design** — the MC must first reproduce this σ/v_N(bin) profile and this super-escape floor from a *Newtonian* population before any boost claim is even meaningful. Physics-or-photometry: **photometry dominates the deep bins; the physics, if any, is the residual after deconvolution.**
