# X72_smooth_core_native_cf: FROZEN CRITERIA (committed alone, before any A4 number is read)

**Purpose.** This is the deciding regrade after X70 / X71: the smooth core with the NATIVE concentration from the X48 A4
zooms and measured stellar fractions, together. The owner said "keep pushing" (10-29). A4 (criteria fc22ce369d) was still
running when this was committed. No A4 output has been opened.

**Standing:**
- κ = ½ FITTED. Footings never pooled.
- Not "theory closed". Nothing here may say the data favour the framework.
- c_f is native here, so the label drops [c_f EXTERNAL] and carries [c_f NATIVE, X48 A4].

## Inputs (fixed now)

- **Shape:** X70's smooth core ρ₀/(1 + x²)^(3/2), with B_S(x) = 4[asinh x − x/√(1+x²)] in X43's units and
  B_S(1) = 0.69707.
- **Native c_f(M):**
  - `cf_by_mass` from X48's own pipeline, `x48_analyze.py --ng 64 --tag A4` → `x48_analyze_results_ng64_A4.json` (which
    includes the A3 1e12 runs).
  - c_f is X48's definition, r_vir / r₋₂ of the collapsed object at z_f. It is used unchanged.
  - Interpolate in lg M between the measured masses and hold flat outside, exactly as `x48_regrade.py` does.
  - If the A4 file lacks any of 1e12 / 1e13 / 1e14, the regrade is UNDECIDED.
- **η(M) = (4/(3 B_S(1))) c_f(M)^(5/4).** At c_f = 4 this is 10.82, X70's value.
- **Stellar fraction:** X71's uniform injection. Graded at f★ = 0.034 and 0.0615; 0.20 is reported.

## Checks (all must pass, else UNDECIDED)

- **K1 identity:** with c_f(M) ≡ 4 at every mass, the script reproduces X71's committed cluster preds, SPARC rms and
  groups Z at each f★ to 1e-9.
- **K2:** η(M) printed at 1e12 / 1e13 / 1e14 / 1e15 matches the formula.
- **K3:** the inherited X43 identity checks hold at f★ = 0.20. As X71 documents, they fail at other f★ by construction.

## Verdict (per footing and per graded f★; the label needs both footings to agree)

- **PASSES:** SPARC line (both backgrounds), all 15 cluster keys |Z| ≤ 2 in both h cells, and groups CONSISTENT.
- **FAILS:** <systems / keys with sign>.
- **Headline:** the canonical footing at BOTH graded f★.

**Convergence flag.** X48's own A4 resolution grade (`x48_grade_A3.py`-style, per mass) is reported next to the verdict.
If X48 calls A4 not converged, the label carries [c_f UNCONVERGED]; the class is not changed.

**Also reported:**
- every key's Z against X71 (c_f = 4);
- η(M);
- the pre-registration 23095bf23a score (slope sign and size, from the same table).

**MUTATE:** c_f(M) ≡ 2 × native. G-OUT-M3's pred must move by more than 0.01; otherwise the harness is insensitive.
