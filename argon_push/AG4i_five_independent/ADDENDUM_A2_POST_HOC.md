# AG4i ADDENDUM A2 (POST HOC, 2026-10-20): the thin-disc regulator was too large

Committed alone, after the A1 run and before any A2 number. **No M number has been seen in any run.** The A1 run skipped M,
because its must-pass K2a failed.

## What A1 showed
- **K2a failed at 4.75%** (limit 1%).
- The diagnosis: for Σ = e^(−R), the exact razor-thin ratio V²/(y²[I₀K₀ − I₁K₁]) must be the constant 4π = 12.566. The code
  gives 12.07 at R = 0.6h, rising to 12.52 at 4.6h. The deficit scales as ε/R, which is the softening regulator
  ε = 0.02 R_d acting on the inner radii. It is a numerical-accuracy error, not a method error.
- The K results are unchanged and stand as frozen and graded.
- NGC 24 fails the frozen K2 (thin-disc shape vs SPARC's Vdisk, 0.175 > 0.15). The frozen criteria did not say what a K2 failure
  implies.

## A2 changes (nothing else changes)
1. ε = 0.002 R_d. The radial grid keeps ΔR′ ≤ ε/5; the point cap is raised from 60,000 to 400,000 so that the rule always holds.
   The derivative step stays ε/50.
2. K2a stays must-pass at ≤ 1% beyond 0.3h. If it fails, M is VOID and no further addendum is made in this lane.
3. **K2 failure (closing a frozen gap):** a galaxy whose constant-Υ shape fails K2 still has its M variants computed and
   printed. They are flagged K2-FAIL and do not enter its class. Its class then comes from K only (or NO VARIANT AVAILABLE).
4. A1's colour-validity rule (−0.15 < [3.6]−[4.5] < −0.02 after smoothing) is kept unchanged.

## Reading
- The M results are POST HOC (A1 + A2) and labelled so. Classes use the frozen definitions.
