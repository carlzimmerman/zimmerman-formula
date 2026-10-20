# AG4i ADDENDUM A1 (POST HOC, 2026-10-20): fix the thin-disc code and apply the colour relation only where it is valid

Committed alone, after the first run and before any A1 number.

## What the first run showed
- **The K results (independent rotation curves) do not use the thin-disc code. They stand as frozen and graded:**
  - NGC 5985 with GHASP: pull +2.00, RESOLVED.
  - NGC 5023 with de Blok & Bosma: +2.50, RESOLVED.
  - UGC 731 with de Blok & Bosma: +5.00, PERSISTS.
- **The M results are VOID as frozen,** for two reasons:
  1. **The Hankel thin-disc code is numerically wrong.** The added check K2a (the Freeman exponential disc) failed with
     deviations up to 183% and sign flips. The high-k integral aliases on the radial grid, and J₁(kR) is undersampled on the
     log-spaced k grid. The symptoms included multipliers m(R) below zero (UGC 128: −26 to +38). The frozen K2 passed for
     four galaxies because normalising the shape at its maximum hid the error.
  2. **Colours far outside the relation's validity range were fed to it.** Meidt+2014 (verified from the text): "old stars
     typically exhibit blue colors in the range −0.15<[3.6]−[4.5]<−0.02, the emission from non-stellar sources are
     characterized by colors [3.6]−[4.5]∼0.3 and redder". The measured profiles reached −0.56 (NGC 24) and +0.75 (UGC 128).
- **UGC 731:** its IRAC post-BCD mosaic has no valid pixels at the galaxy (all NaN within 50 pixels of the centre). K3 fails
  correctly, and M stays NOT AVAILABLE. This is a coverage fact, not a code fix.

## A1 changes (nothing else changes)
1. **Thin-disc rotation curve:** the exact potential of a razor-thin axisymmetric disc, regulated by a small softening:
   - Φ(R) = −G Σ_j Σ(R′_j) R′_j ΔR′ · 4K(m)/√((R+R′)² + ε²), with m = 4RR′/((R+R′)² + ε²), K the complete elliptic integral,
     and ε = 0.02 R_d.
   - V²(R) = R dΦ/dR by central difference with step ε/50.
   - The radial grid: ΔR′ ≤ ε/5, with the frozen exponential tail and inner hold.
   - The multiplier m(R) = V²_grad/V²_const is unchanged in definition.
   - **K2a becomes a must-pass control:** the Freeman exponential disc reproduced to ≤ 1% beyond 0.3 h. If it fails, M is VOID
     again.
   - The frozen K2 is re-evaluated with the new code.
2. **Colour validity:** after the frozen 5-point running median, only radii whose smoothed colour lies inside the paper's
   old-star range −0.15 < [3.6]−[4.5] < −0.02 are kept.
   - The frozen rule (hold the last valid colour) then applies outward, and the first valid colour is held inward.
   - If fewer than 3 radii remain, that galaxy's M is NOT AVAILABLE.
   - All four β variants and K+M use the same filtered colours.

## Reading
- The A1 M results are POST HOC and labelled so. Readings and classes use the frozen definitions, on A1's M numbers.
- The MUTATE (SPARC curve, β = 0) does not depend on either change; it is run as frozen.
