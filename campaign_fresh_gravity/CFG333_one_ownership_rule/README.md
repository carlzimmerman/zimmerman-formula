# CFG333: one ownership rule for four Milky Way populations?

- **Criteria:** `FROZEN_CRITERIA.md`, committed before any score (fb8a6d5ab).
- **Settings:** κ = ½ is FITTED. Both footings are used. The kernel is ν_mono. Inputs are on disk only.

**Run**
- `python3 cfg333_one_rule.py`: about 5 s, 3/3 checks pass.
- `CFG333_MUTATE=1 python3 cfg333_one_rule.py`: about 45 s, 2/2 checks pass, writes the `_MUTATE` outputs.
- `python3 cfg333_lean_gen.py`, then `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG333_certificate.lean`: 32 theorems, exit 0, no sorry.

**Verdict: PARTIAL.** The best rule is R2, the record's own FG001 formation classes (not a new postulate). It passes 3 of 4 populations; the ultra-faint dwarfs fail.

## Tensions (canonical | alt)

| rule | wide binaries | globulars (joint-Υ t; L) | classical dwarfs | ultra-faints | passes |
|---|---|---|---|---|---|
| R0, all top-level (control) | F −8.45 \| −9.03 | F −4.43; 5.49 \| −5.12; 5.82 | P +0.64 \| +0.45 | F +3.77 \| +3.55 | 1/4 |
| R1, tidal binding | F −8.45 \| −9.03 | F (same as R0) | P +0.77 \| +0.68 | F +3.77 \| +3.55 | 1/4 |
| R2, FG001 formation | P +1.36 \| +1.51 | P 0.00; −1.11 \| 0.00; −1.11 | P +0.64 \| +0.45 | F +3.77 \| +3.55 | 3/4 |
| R3, g_int < g_ext (NEW POSTULATE under B) | P +1.36 \| +1.51 | F −2.09; 3.80 \| −2.53; 4.11 | P +1.37 \| +1.21 | F +4.24 \| +4.24 | 2/4 |

## Reading
- **No labelling rescues the ultra-faints.**
  - Top-level, the bare law runs +0.32 dex high.
  - Owned (Newton on the native cold share M_b/f_b) runs +0.68 dex high.
  - Owned with stars only runs +1.08 dex high.
  - The ultra-faints need more mass than any class supplies. The failure is a mass shortfall, not a classification problem.
- **R1 makes everything top-level.** Every bound system, wide binaries and globulars included, has an internal field far above the host tide. So R1 reproduces the bare law.
- **R3 owns 38 of the 40 ultra-faints.** That makes them worse.

## Caveats (kept)
- **Pal 3.** The two-sided globular statistic, reported only, is 2.83σ for Newton.
- **C3.** h93's "isolMOND" column is the (4/81) formula, so C3 compares against h93's printed ν(isolated) values instead (agreement 5e-4). This changes the frozen C3 wording.
- **Classical sample.** It includes the LMC and SMC and current HI only. It is therefore not CFG313's infall-gas +0.027 row.
- **MUTATE.** At seed 333 a random relabelling gave R3 3 of 4. Over 50 permutations, R2's mean pass count is 1.08 (max 2). Passing wide binaries, globulars and classical dwarfs requires owning exactly the wide binaries and the globulars.
- **Wide-binary prediction.** It is a representative point at y = 0.3, not a forward model. γ̂ is non-scoring for the prereg.
