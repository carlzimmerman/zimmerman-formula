# AG4e FROZEN CRITERIA (2026-10-20): seal the action's own n=1 law's ALMA gas predictions before the 11-06 / 11-28 releases

Committed alone, before any AG4e script or number. Owner's go (2026-10-20, in chat): "seal the action's own n=1 (simple)
law's ALMA gas predictions as well, same method as AG4d, before 11-06".

## Why
The November seals (CFG571, CFG775, CFG778) use the record's ν_mono kernel. The frozen S2 action's own rest state is the n=1
simple law, ν₁(y) = (1 + √(1 + 4/y))/2, i.e. g_N = g²/(g + a₀) (AG4). n=2 is sealed in AG4d. This lane seals n=1, so that every
law the record carries has a pre-registered number.

## Method (identical to AG4d, kernel ν₁)
- CFG571's head is executed read-only, as CFG778 and AG4d do, and the namespace kernel `NU` is replaced by ν₁.
- Branches: E, E-CCBH, F-flat, F-DESI, BH-k3, R-H, L-fb(RAR-eq).
- Targets: GS4_24110 (log M* 10.89 and 10.76) and U4_27928 (V_c 150–300 km/s).
- Both footings; R_g = R_d and R_g = 1.5R_d.
- No gate. The owner asked for this seal directly.

## Controls
- K1: with ν_mono the code reproduces CFG571's and CFG778's sealed numbers to ≤ 1e-9 dex, as AG4d's K1.
- K2: ν₁ satisfies g²/(g + 1) = y to 1e-12 for y ∈ [1e-6, 1e4], and ν₁(1e-4) = 100.50125.
- K3: the ν₁ grid equals AG4d's reported n=1 grid (`ag4d_results.json`, `n1_simple_reported`) exactly. Same code, same kernel.

## Seal
- Write `SEALED_N1.json` (json.dumps with sort_keys, default=str) and its sha256 to `PREDICTIONS_HASH.txt`.
- Commit and push before 2026-11-06. Never edit either file after a release.

## MUTATE
`AG4E_MUTATE=1` sets the kernel to ν = 1. The F-DESI vs R-H separation on GS4_24110 must collapse (< 0.01 dex) at both M* and
both footings; the script then exits 1. Nothing is sealed in MUTATE.

## Settings
κ = ½ fitted; footings never pooled; cold-energy mass required; not theory closed.
