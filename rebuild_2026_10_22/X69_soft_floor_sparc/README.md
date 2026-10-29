# X69_soft_floor_sparc

**Question.** The external model's T2 (relayed by the owner, 10-29) was to soften the a₀/(2πG) floor in low-acceleration
galaxies: Σ_core = max(Σ_M F(X₀), η Σ_coll), with F = 4X₀/√(1+16X₀²) and X₀ = peak g_bar(Υ = 0.5)/a₀. The form was
frozen as given and run once. Criteria were committed first (6c4f4537e0).

## Verdict: HARD FLOOR PREFERRED, both footings and both backgrounds

| | canonical A | canonical B | alt A | alt B |
|---|---|---|---|---|
| SPARC all rms, X43 → SF | 0.0782 → 0.0876 | 0.0782 → 0.0876 | 0.0729 → 0.0816 | 0.0728 → 0.0815 |
| median Υ under SF | 1.05 (line **FAIL**) | 1.07 (FAIL) | 1.01 (FAIL) | 1.05 (FAIL) |
| LOW (X₀ < 0.32) rms | 0.114 → 0.176 (**+55 %**) | +55 % | 0.120 → 0.173 (**+44 %**) | +43 % |
| REST rms | +0.5 % | +0.5 % | +0.4 % | +0.3 % |

- **LOW is not the proposal's "bottom 12 %".** It is 93 of 175 galaxies on canonical (95 on alt); the median X₀ is
  0.29 / 0.24. The proposal's SPARC percentages were invented.
- **Where it helps.** A handful of galaxies improve: UGC07577, CamB, F563-V1, KK98-251, IC2574, D564-8 (Δrms −0.2 to −0.6).
- **Where it hurts.** More get worse: UGC05764, UGC07608, UGC06667, F583-1, NGC3109, ESO444-G084 (+0.17 to +0.39).
- **Why it fails overall.** Lowering the halo at low X₀ pushes the fit to raise Υ (median above 1, outside EM1's line),
  and still leaves the low-acceleration rotation curves short.
- **MUTATE (2X₀, softer still):** LOW +67 %, harness sensitive (ΔLOW rms 0.018).

**Reading.** The SPARC data reject softening the floor at low baryonic acceleration. The low-acceleration galaxies are where
the hard floor works best. So IC 1613's failure (IN1 / IN2) is an individual problem, not evidence that the floor is soft.
IC 1613 itself is not in SPARC. Leo T and Phoenix, which sit above the law, are out of scope here. Checks 2/2: K0 (F ≡ 1
reproduces X43 exactly) and K1.

κ = ½ FITTED; c_f EXTERNAL; not theory closed.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x69_soft_floor.py`, `.out` / `_results.json`, `_MUTATE` versions, `x69_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_soft_floor.py                # ~55 s, exit 0
    X69_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_soft_floor.py
