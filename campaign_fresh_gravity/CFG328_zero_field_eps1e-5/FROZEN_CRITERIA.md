# CFG328 FROZEN CRITERIA: CFG322 one decade stiffer (ε = 1e-5)

**Lane:** orchestrator. The owner asked for local-compute lanes ("push my mac hard").
**Question:** CFG322 and CFG325 found that the 1-D Lyapunov exponent levels off at N = 1023 for ε = 1e-3 and ε = 1e-4. Smaller ε is the physical direction (physical ε = 2.56e-18). Does the ε = 1e-5 ladder N = 63/127/255/511 behave like ε = 1e-4 (rising, then flattening), or worse?

## Method
- **Unchanged from CFG322:** the engine (byte-identical to CFG321's, sha256 checked), the ν_mono kernel, data class D, seeds, δ pairs, T1D, the Lyapunov window, ZERO = 0.005, the regularity rows, and the ratio rule on N = 63/127/255/511.
- **Reused (CFG328_REUSE=1):** the ε = 1e-3 set and the GR control are copied from CFG322's verified work arrays, so C1 still runs.
- **New:** only the ε = 1e-5 runs.

## Decision (per CFG322's frozen rule, applied to ε = 1e-5)
- **RESOLVED-CONVERGENT:** |r2| ≤ 0.6 and |r3| ≤ 0.6, with a finite λ_∞.
- **CONFIRMED-FAIL:** Δ3 ≥ 0.005 with r3 ≥ 0.9.
- **OPEN:** anything else.

Also reported, without grading:
- the λ(N) table and the maximum amplification;
- the comparison with ε = 1e-4 at the same N;
- whether λ at fixed N grows as ε falls.

## Controls
- **C1:** CFG321's ε = 1e-3 rows are reproduced.
- **C2:** the GR control converges.
- **Regularity rows.**
- **MUTATE:** CFG322's μ_exp MUTATE stands; it is not re-run, which is disclosed.

## Scope
1-D only. This lane says nothing about growth.

## Pre-freeze disclosure
No ε = 1e-5 run was performed before this freeze. The expected cost is about √10 × that of ε = 1e-4, i.e. about 4 h at N = 511.
