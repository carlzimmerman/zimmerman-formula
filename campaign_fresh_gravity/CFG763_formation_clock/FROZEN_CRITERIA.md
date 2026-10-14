# CFG763 FROZEN CRITERIA: the formation clock — how slowly must cold energy form at rest for young tidal dwarfs to be Newtonian?

Date: 2026-10-13. Block CFG760–769. Committed ALONE before any CFG763 script or number. κ = ½ FITTED; both footings, never pooled;
the cold energy's mass is required; no particle species; not "theory closed".

## Why
CFG749 + CFG760–762: cold energy can't be assembled by infall (it must be nearly at rest, and P radiation can't remove infall
energy). The remaining route is formation at rest in each system's frame (astra F1/F5; CE-FM-028: a prepared cold state can
track slow growth). A system whose baryons assembled recently then holds only a fraction f(t) of the law's cold mass. The
record's young TDGs (CFG7 six, Lelli+2015; Arp 72c; all CFG441 Tier B, 0.32–0.75 Gyr) are Newtonian (Δχ² +33/+39 vs the law).
They bound the formation time from below; SPARC's old discs, which follow the law, bound it from above.

## Model (one parameter, generic first-order formation)
V²(t) = V_N² + f(t)·(V_law² − V_N²), f = 1 − exp(−t/τ). V_N and V_law (ν_mono, CFG7/FM12 eq. 4 EFE at nominal host mass, isolated
for Arp 72c) and their propagated errors are CFG441's (code copied); the model error is interpolated the same way,
e = e_N + f(e_law − e_N). Ages t: the six from Lelli's t_merg/t_orb × t_orb, Arp 72c 0.32 Gyr. **For the bound each age is taken at
its lower 1σ value (t − σ_t, floored at 0.05 Gyr)**, which is favourable to fast formation. Nominal ages are reported.

## Controls
- **K1.** τ → 0 and τ → ∞ reproduce CFG441's Tier-B χ²_law (34.018 canonical / 40.290 alt) and χ²_N (1.105), within 0.01.

## Tests
- **F1 (lower bound).** χ²(τ) on a log grid τ ∈ [0.01, 100] Gyr (0.01 dex). τ_min,95 = the smallest τ with
  χ²(τ) ≤ χ²_min + 3.84.
- **F2 (window with old discs).** SPARC's discs follow the law; their baryons assembled ≥ 8 Gyr ago, so they need
  f(8 Gyr) ≥ 0.9, i.e. τ ≤ 3.47 Gyr. **Window OPEN iff τ_min,95 ≤ 3.47 Gyr on both footings**; CLOSED otherwise.
- Reported: the window in units of each object's own orbital time; f at t = 1, 2, 3 Gyr at τ_min,95 (what a z ≈ 2–4 disc of that
  baryonic age would hold); and the same with nominal ages.

**MUTATE** (`CFG763_MUTATE=1`): V_obs := V_law (a law-obeying set). Then τ_min,95 must be ≤ 0.05 Gyr (no lower bound). Exit 1 iff
it bites.

## Not tested
Formation laws other than first order; TDG non-equilibrium (all < 1 orbit, CFG441 S3); whether f depends on the host (CFG7 FG001's
hierarchy reading is the alternative explanation of the same data); high-z kinematics (calibration-limited, CFG213–229).
