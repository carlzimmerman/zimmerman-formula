# X73_smooth_core_all_measured

**Question.** X70's smooth-core pass and X71's break (G-OUT-M3 UNDER, Z 2.25–2.33) both used two inherited inputs: the
Planck ratio 5.364 with H0 67.4, and X30's "P" gas tail. GS1 replaced those with native normalisation and the measured
X-COP slope (s = 2.777) out to the self-consistent r_ta, but it kept Burkert and f★ = 0.20. This lane grades the smooth
core with **every input measured or native at once**: native Ω_c/Ω_b, the measured gas slope, and measured f★ (0.034 /
0.0615) in both the core and the tail. Nothing is fitted. Criteria were frozen first (f5ed2b706b).

## Verdict (frozen rule, per footing)

| footing | s_meas 2.777 | s16 2.676 | s84 3.071 | class |
|---|---|---|---|---|
| **canonical** | **ALL-MEASURED PASSES** (both f★) | BREAKS: G-OUT-M3, G-OUT-Mall (OVER, f★ 0.0615 only) | PASSES | **FRAGILE** |
| alt | BREAKS: SPARC line (X70's Υ 0.47) | BREAKS: SPARC, G-OUT-Mall | BREAKS: SPARC | ROBUST |

**Canonical, PRIMARY configuration:**
- All 15 cluster keys pass in both h cells.
  - G-OUT-M3 Z: −0.75 / −0.84 at f★ 0.034, and −0.89 / −0.98 at f★ 0.0615.
  - G-OUT-all Z: −1.29 / −1.46.
  - G-IN-Mall Z: −1.11 / −1.15.
- Groups Z +1.94 pass. SPARC passes on both backgrounds (rms 0.0713 / 0.0720).

## What moved G-OUT-M3 (canonical, h 0.672)

| configuration | f★ 0.034 | f★ 0.0615 | f★ 0.20 |
|---|---|---|---|
| inherited, P tail (= X71 / X70) | +2.33 ✗ | — | +1.88 |
| native, P tail | +2.48 ✗ | +2.40 ✗ | — |
| inherited, measured tail | −0.93 | −1.07 | — |
| **native, measured tail (PRIMARY)** | **−0.75** | **−0.89** | −1.56 (G-OUT-all −2.28 ✗ OVER) |
| Burkert, native, measured tail | −0.02 (groups +2.05 ✗) | −0.15 (groups +2.05 ✗) | −0.76 (= GS1) |

- **X71's break was the truncated gas tail, not the stellar fraction.** With the measured X-COP slope counted to r_ta,
  the heavy-cluster outskirts are no longer short at measured f★.
- The native normalisation alone moves G-OUT-M3 by +0.15. It does not rescue X71.
- **The measured inputs are jointly consistent; the inherited one was not.** With the measured tail, X43's f★ = 0.20
  now over-predicts G-OUT-all (Z −2.28). The measured f★ is what brings it back. So the "f★ 0.20 masks an excess"
  reading (CFG407) and X71's break describe the same miscount from opposite sides.
- **The smooth core is still what passes the groups.** Burkert passes every cluster key here but fails the groups at
  +2.05. The smooth core passes both.

## Reading, with the limits

- On the canonical footing, the smooth-core halo with c_f = 4 passes SPARC, the groups and all 15 cluster keys with
  every input measured or native. This is the first such pass on record.
- **It is FRAGILE.** Across GS1's slope bootstrap (16–84 %), G-OUT-M3 runs from −1.97 (s16, f★ 0.0615; −2.01 in the h
  0.686 cell) to +1.46 (s84). At s16 it over-predicts.
  - The outer cluster keys now measure the gas tail beyond x_max ≈ 1.5–2.1 R500, extrapolated to r_ta, more than they
    measure the core rule.
  - A real measurement of the gas slope beyond 2 R500 decides this line, not more modelling.
- **Alt footing:** the clusters behave the same; X70's SPARC Υ failure stands.
- **Not regraded:** KiDS lensing (X53) and the dwarfs (X51). IC 1613 still fails (IN2).
- **c_f = 4 is EXTERNAL.** X48 A4's native c_f(M) and X72 are still pending.
- κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating field component, never a particle. Not
  theory closed. Nothing here says the data favour the framework.

## Checks

- **K1:** Burkert, f★ 0.20, native, s_meas reproduces GS1 `R4_meas` exactly: every cluster pred, both footings, both h
  cells, max |d| = 0.
- **K2:** smooth, f★ 0.20, inherited, no tail reproduces X70 exactly (max |d| = 0, 9/9 checks).
- **K3:** smooth, f★ 0.034, inherited, no tail reproduces X71's `fs0.034_S` exactly (max |d| = 0).
- **MUTATE:** f★ 0.60 raises G-OUT-M3's pred (1.530 → 1.695) and over-predicts nine keys, so the harness is sensitive.
- **Inherited checks exit 1 by construction.** K0 and K0x38 are X30/X38 stored amplitudes defined at the inherited
  f★ 0.20 normalisation, so they move whenever f★ or the normalisation changes (as disclosed in X71). Every other check
  passes in every run.
- Peak RSS ≤ 0.40 GB, one thread, nice 15. X48 A4 was live and was not disturbed.

## Files and reproduction

- `FROZEN_CRITERIA.md`
- `x73_all_measured.py`
- `x73_fs*_{S,B}_{nat,inh}_{s*,notail}.out` and the matching `x73_results_*.json`
- `x73_summary.py` and `x73_summary.json` (applies the frozen rule to the JSONs)

Run and summarise:

    X73_FSTAR=0.034 X73_SHAPE=S X73_NATIVE=1 X73_SLOPE=2.7774425603108597 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x73_all_measured.py   # ~70-90 s
    python3 -I x73_summary.py
