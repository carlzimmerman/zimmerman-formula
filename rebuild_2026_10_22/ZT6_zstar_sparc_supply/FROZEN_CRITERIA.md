# ZT6_zstar_sparc_supply — FROZEN CRITERIA (committed alone, before any script or number)

Runs Z★'s test **Z-T6** exactly as frozen in `Z1_successor_design/TEST_PLAN.md` (0d1959a4f5): "Per galaxy
f_req = ½(−1 + √(1 + 4(R_last/r_M)²)). Reported distribution; **FAIL** only if the SPARC-implied owned dust, scaled by the
record's baryon census (CFG953), exceeds Ω_c's budget by > 2×." κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never
pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework. One thread, < 1 GB,
seconds, beside the live L1 384³ job.

## Implementation choices (this lane's)

- **Galaxies.** SPARC 175 rotmod files (P4's loader). M_b = V_bar²(R_last) R_last / G at Υ_disk = 0.5, Υ_bul = 0.7 (the
  SPS reference; reported also at each galaxy's P4 per-galaxy best Υ, from P4's law fit re-derived here and checked against
  P4's committed pooled rms, check KP). Spherical convention, as P4. r_M = √(G M_b / a₀) per footing.
- **f_req** as frozen (point-mass closed form, Z1 K5; check K5: the law's phantom mass inside R for a point mass equals
  f_req M_b to 1e-10).
- **Census supply** (CFG953 ← CFG947, verbatim formulas): N = M_c/M_b = (1 − f_b)/(f_r f_b), f_r = fret_of(log₁₀ M_ta[M⊙/h])
  from the census fixed point f_r f_b M_ta / h = M_b, with CFG947's constants (Ω_b 0.02237, Ω_c 0.1200, h 0.674, native
  Δ_ta(0) from `CFG654_independent_inputs/cfg654_delta_ta.json`). Check KC: N(NGC 3198) = 53.64 (CFG953 DERIVATION L166).
- **Budget statistic (the frozen FAIL line).** B = Σ_i f_req,i M_b,i / Σ_i N_i M_b,i: the share of the census dust that SPARC's
  galaxies must own out to their last points. Ω_c's budget is the census supply itself, so **FAIL iff B > 2** on either
  footing. Reported only: median and 16/84 % of f_req; the number of galaxies with f_req > N_i (local shortage: the law
  would truncate inside R_last); the same count against the no-loss supply f_s = 5.364 (Z1's record ratio); B at the P4 Υ.
- **Classes:** PASS (B ≤ 2 both footings) / FAIL. Per-galaxy shortage is reported, not scored (the frozen line is global).

## Checks and `--mutate`

`zt6_sparc_supply.py`: KP, K5, KC, KR (RSS < 1 GB); exit 0 iff all pass. `--mutate`: f_req computed with r_M from G M_b / a₀
replaced by G M_b / (100 a₀) → K5 fails (exit 1). Outputs `zt6_sparc_supply{,_MUTATE}.out`, `_results{,_MUTATE}.json`.
Post-result changes go in a dated AMENDMENT.
