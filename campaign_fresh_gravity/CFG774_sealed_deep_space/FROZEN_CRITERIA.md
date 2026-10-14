# CFG774 FROZEN CRITERIA: sealed prediction for a deep-space probe (10 AU – 0.1 pc)

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

## Question
No measurement of gravity exists where the Sun's field drops below a0 (beyond about 7000 AU). What anomalous sunward
acceleration does each form of the framework predict for a probe at heliocentric distance r? Which forms are still alive?

## Forms
- **F1, committed** (stiffened action, L* = 5.75 / 30 / 100 / 1000 pc). The anomaly a(r) comes from CFG770's exact linear
  response in the Galaxy's background. It uses CFG770's `a_anom` and `background`, imported read-only, at
  g_e = 2.32e-10, both footings.
- **F3** (γ = 0 + basin rule). The Sun's own node keeps the simple μ's a0 tail (g − g_N → a0 at high g). So the ephemeris
  gate at 1 AU applies to it unchanged (CFG770 C0: 2557× / 3091×). Class: **F3 DEAD** if the tail at 1 AU exceeds 3.66e-14.
- **F2** (γ = 0, local): already dead by the same tail (CFG770 C0).

## Output (sealed)
A table of F1's a(r) at r = 10, 30, 100, 300, 1000, 3000, 7000, 2e4, 1e5 AU and 0.1 pc, for 4 L* × 2 footings. The table's
sha256 is written into the README.

**Declared kill line for F1:** a probe at r ≥ 1000 AU measuring a non-thermal anomalous sunward acceleration
≥ 1e-13 m s⁻² EXCLUDES F1 at every L* in the window. F1 predicts ≤ 4.3e-15.

## Controls
- K1: F1's a(r ≪ λ_e) = GM/L*² to 1e-3 (CFG770 K1).
- K2: the CFG770 import reproduces its committed T3 value at 1 AU (4.2157e-15) to 1e-4.

## MUTATE (CFG774_MUTATE=1)
M1: L* = 1e-4 pc. The predicted anomaly must exceed the kill line, i.e. the line has teeth against an unscreened sector.

## Hand estimate
- F1 is constant at 4.22e-15 (L* = 5.75 pc) from 10 AU to 0.1 pc. It begins to fall only near λ_e ≈ 2 pc.
- F3 and F2 are dead (tail ≈ 1e-10 at 1 AU).

## Disclosures
- Non-gravitational (thermal) accelerations of real probes are around 1e-10 (Pioneer). Reaching 1e-13 needs drag-free
  technology at hundreds of AU, which is a future capability.
- κ fitted; not theory closed.
