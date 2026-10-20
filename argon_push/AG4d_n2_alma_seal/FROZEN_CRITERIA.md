# AG4d FROZEN CRITERIA (2026-10-20): seal the n=2 law's ALMA gas predictions before the 2026-11-06 / 11-28 releases

Committed alone, before any AG4d script or number. Owner's go (2026-10-20, in chat): "if n=2 survives, compute and seal its
ALMA gas predictions before 11-06".

## Gate
This lane runs ONLY IF AG4b and AG4c both return "n=2 survives" (each one's FROZEN_CRITERIA defines that). If either says no,
AG4d is not run, and this file records why.

## Method (the identical code path, kernel swapped)
- Execute the head of `campaign_fresh_gravity/CFG571_prereg_proprietary_alma/cfg571_prereg.py` (everything before
  `# ---- controls ----`) in a namespace, read-only, exactly as CFG778 does. Use its `predict`, `gbar_req`, `FOOT`
  (both footings), the disc models, and the GS4_24110 and U4_27928 inputs.
- Replace the namespace's kernel `NU` with the n=2 law: ν₂(y) = √(1 + 1/y) (g² − g_bar² = a₀ g_bar). Nothing else changes.
- Branches: E and E-CCBH (CFG778's sealed ratios at z 1.41933 and 1.997), F-flat, F-DESI, BH-k3 (CFG775 B2, as CFG778 uses
  it), R-H, and L-fb(RAR-eq) (CFG571).
- Targets:
  - GS4_24110: z 1.997, R 7.39 kpc, V_c 206, log M* 10.89 and 10.76.
  - U4_27928: z 1.41933, R = 2R_e, log M* 10.74, V_c grid 150–300 km/s, as CFG571 / CFG778.
- Quantities: the required log M_bar and the total log M_gas for R_g = R_d and R_g = 1.5R_d, or FLOOR.

## Controls
- K1: with the namespace kernel left as CFG571's ν_mono, AG4d reproduces CFG571's stored GS4_24110 and U4_27928 numbers
  (`cfg571_prereg_results.json`, every model and footing, logVbar2R_G) and CFG778's `SEALED_EVENT_HORIZON.json` (E, E-CCBH,
  BH-k3) to ≤ 1e-9 dex.
- K2: ν₂ satisfies g² − y² = y to 1e-12 for y ∈ [1e-6, 1e4], and ν₂(1e-4) = 100.005.

## Reported, not sealed
The same grid under the S2 action's own n=1 rest state, ν₁(y) = (1 + √(1 + 4/y))/2, so the size of the kernel choice is on
record. The November tests were sealed with ν_mono, not ν₁.

## Seal
- Write `SEALED_N2.json` (json.dumps with sort_keys, default=str, as CFG778) and its sha256 to `PREDICTIONS_HASH.txt`.
- Commit and push before 2026-11-06.
- Never edit either file after a release; any change goes in a new dated file.

## MUTATE
`AG4D_MUTATE=1` sets the kernel to ν = 1 (Newton). The F-DESI vs R-H separation in required baryons must collapse (< 0.01 dex)
on GS4_24110 at both M* values and both footings; the script then exits 1 (the control bites). Nothing is sealed in MUTATE.

## Settings
κ = ½ fitted; footings never pooled; cold-energy mass required; not theory closed. A sealed n=2 prediction does not adopt n=2:
the canonical statement (v3) keeps n=1 unless the owner decides otherwise.
