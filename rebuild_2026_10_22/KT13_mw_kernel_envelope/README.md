# KT13_mw_kernel_envelope: NO KERNEL IN FAMILY on both footings. With star-count baryons, every one of eight QUMOND kernels that reaches the Milky Way's v_c lands at K(R0) 75.0-76.3 against a line top of 70.8. The miss is set by the baryons, not the transition shape

Criteria: `FROZEN_CRITERIA.md` (6287109e86), alone first, confirmed landed before any script, **not blind**: the hand argument and the expected label were written before running. `kt13.py`, `kt13.out`, `kt13.json`, `kt13_MUTATE.out`, `kt13_MUTATE.json`. No download. κ = 1/2 FITTED and held fixed. Footings never pooled. Not theory closed. Register K824. About 12 minutes, one thread, nice 15.

UX5's form Q, lines and boxes, on the 1375 in-prior cells per footing (LN16 R_d 2.38-2.90, M* 3.80-8.36e10).

| kernel | canonical: cells passing L1 / all four | lowest K, v_c in line | K_proj at best cell | alt: L1 / all four | lowest K, v_c in line | K_proj |
|---|---|---|---|---|---|---|
| simple (board law) | 433 / 0 | 76.0 | 82.7 | 701 / 0 | 76.3 | 81.7 |
| RAR, 1/(1 - e^-sqrt y) | 281 / 0 | 75.8 | 82.2 | 587 / 0 | 75.7 | 83.1 |
| OR mu_2 | 71 / 0 | 75.6 | 82.4 | 222 / 0 | 75.0 | 82.3 |
| nu_2 | 0 / 0 | none (v_c max 211.7) | 84.7 | 0 / 0 | none (215.4) | 84.8 |
| nu_3 | 0 / 0 | none (205.0) | 84.5 | 0 / 0 | none (207.8) | 84.7 |
| nu_6 | 0 / 0 | none (200.6) | 84.1 | 0 / 0 | none (201.6) | 84.4 |
| sharp | 0 / 0 | none (200.1) | 84.0 | 0 / 0 | none (200.1) | 83.9 |
| compact (KT12) | 0 / 0 | none (201.4) | 84.8 | 0 / 0 | none (205.6) | 85.2 |
| **Label** | **NO KERNEL IN FAMILY** | | | **NO KERNEL IN FAMILY** | | |

K_proj = K(R0) (229.1 / v_c)^2 at each kernel's best in-prior cell.

## Reading
- **The hand argument holds.** K_proj, the vertical force a cell would have if lifted to the v_c line at a fixed K/v_c^2, runs 81.7-85.2 across all eight kernels and both footings. Newton's best cell gives 84.1. So the kernel barely moves the ratio of vertical force to v_c^2 at R0. The transition shape only decides how far the lift goes, not where it lands.
- **Every kernel that reaches v_c lands at K 75.0-76.3.** The line top is 70.8, and the measurement is 66.4 +- 2.2, so that's about +4 sigma. Kernels that don't overshoot the K line (nu_3 and sharper, compact) never reach v_c. So "between the shapes" from KT12 was the general picture, not a gap to fill.
- **Why, in one line.** In QUMOND the phantom density in the plane is about (nu - 1) rho_b, so the extra pull at R0 comes as a disc and lifts K_z by about the same fraction as v_c^2. A round extra pull would lift v_c without K_z, and no local kernel of |g_N| gives one.
- **What it rules out.** For this family and form Q, the Milky Way can't pass with star-count baryons by changing the interpolating function. Three things could still move: K_z's value (UX5: Bovy and Rix's summary was fitted inside Newtonian potential families; at or above about 75 it no longer excludes); the disc (BV2's thick R_d 2.0 already gives the lowest Ks, and a disc still shorter is outside LN16's tag); or the field equation (non-local, or one where the extra pull is not tied to rho_b in the plane).
- **Scope.** Eight kernels, all with the same deep limit and a0, local QUMOND only. Not a theorem over all nu(y), and not tested on AQUAL beyond UX5's 0.13 percent agreement for the simple kernel. In-prior cells only, so wide-prior classes aren't restated here.

## Checks
C1: the simple kernel reproduces UX5's stored form Q on all 1375 cells per footing, max relative 0. C2: compact reproduces KT12's in-prior best cells, 2.4e-14 and 5.2e-13. C3: y = x mu(x) to at most 3.2e-14 for the seven with closed mu; RAR monotone with limits 1.000045 at y 100 and sqrt(y) nu 1.005 at 1e-4. MUTATE (Newton): v_c max 200.0, L1 passes in no cell, K_proj 84.1, exit 1. No passing cell, so no Q5 was owed.
