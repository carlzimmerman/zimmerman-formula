# UW1_one_scale_unitarity: NO REAL KAPPA, DOES NOT FIX F0. The s-wave is negative at g = a0, and the law's function leaves the vacuum constant free

Criteria: `FROZEN_CRITERIA.md` (71fb05a4d3), alone first, not blind. `uw1.py`, `uw1.out`, `uw1.json`, `uw1_MUTATE.out`, `uw1_b.py`, `uw1_b.out`. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. This grades one route. It is not a no-go.

## Test A: frozen label NO REAL KAPPA
- No derivative of F contains F0 (checked), so amplitudes can't set it. Reaching kappa at all needs the posit epsilon = s*^2.
- With that posit pi does cancel, kappa^2 = 4B/(N a_max). This is the one real feature of the route.
- Control: planted X^2 theory gives B 2.0000001 against 2.
- B at Y = 1 is **-0.382** (Y 0.1: -11.85; Y 10: -0.0121). Imaginary part 0.

Post-result, not a frozen reading: unitarity bounds |a|, so |B| could be used. Then kappa is 0.218 in the primary cell, 0.309 and 0.154 in the others, against W_data [0.227, 0.607]. That is a menu of posits, none at 1/2, and B moves by three orders with Y.

MUTATE disclosure: the planted F has a ghost at Y = 1 (F1 < 0), so B reads nan. The run differs from normal, but this is a weak control for the Y = 1 cell. The frozen 2 pi G test could not be read in that run. kappa^2 is linear in the coupling by construction.

## Test B: frozen label DOES NOT FIX F0
- Analytic continuation is complex for timelike gradients: Im F = -0.429 at s = 1.
- Real branch, keeping the Y term: dF/dY = (s + 2)/(s + 1), no zero for s > 0, rho + P = s^2 (s + 2)/(s + 1) > 0, healthy.
- The attractor is s to 0. Small s: rho - F0/2 and P + F0/2 are both s^2, stiff, so the field's part dilutes away and leaves F0.
- d rho/d F0 = 1/2: F0 is an added constant, as in the bare-constant wall. No tracking and no w(z) prediction from the law's function.

## What this closes
This route with the law's own F. A different F that agrees on the galaxy branch and differs on the timelike branch is not tested, and would be a new free function.
