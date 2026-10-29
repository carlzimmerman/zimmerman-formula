# X69_split_vs_cored_nfw

**Question.** The external model's final-mile spec, Task 2 (relayed by the owner, 10-29), proposed two zero-knob halo
shapes for X43, both with r_s = S r_c and S = max(1, Σ_core/Σ_M):

- T1-A, split Burkert;
- T1-B, cored NFW.

The aim was to fix X43's cluster shape conflict, an X-COP core that is too light with outskirts that are too heavy
(BC1), without breaking the inner core. Criteria were frozen first (0d708a4e49).

## Verdict: BOTH SHAPES FAIL [c_f EXTERNAL], both footings agree

| canonical | X43 Burkert | T1-A split Burkert | T1-B cored NFW |
|---|---|---|---|
| X-COP Δ at 0.1 / 0.2 / 0.3 / 0.5 / 0.7 / 1.0 R500 | +0.19 / +0.03 / −0.03 / −0.08 / −0.12 / −0.16 | −0.24 / −0.30 / −0.29 / −0.27 / −0.26 / −0.27 | −0.08 / −0.09 / −0.08 / −0.07 / −0.09 / −0.13 |
| X-COP mean / rms (42 pts, 7 clusters × 6 radii) | −0.029 / 0.134 | −0.270 / 0.279 | −0.088 / 0.111 |
| G1: X-COP R500 within ±0.05 | — | FAIL (heavy) | FAIL (heavy) |
| G2: 13 MID+OUTER lensing keys | G-OUT-M3 +2.41 | G-MID-T1 −2.19 (OVER) | G-OUT-M3 +3.14 (UNDER) |
| G3: inner keys and X-COP inner | pass | G-IN-all −2.32, G-IN-Mall −3.42 (OVER); X-COP inner −0.27 | PASS |
| SPARC rms, bg A / B (reported) | 0.0776 / 0.0777 | 0.0776 / 0.0777 (unchanged, S = 1) | **0.114 / 0.114, line FAIL** |
| groups Z (reported) | +2.05 | +1.83 CONSISTENT | +2.51 ABOVE LAW |

Δ = log(g_HSE/g_pred): positive means the halo is too light. The alt footing gives the same pattern:
- T1-A: X-COP R500 −0.26; the same three lensing keys fail.
- T1-B: X-COP R500 −0.12; G-OUT-M3 fails; SPARC 0.106; groups +2.60.

**What each shape does.**
- **T1-A** puts more mass everywhere inside r_ta. At fixed Σ_core and fixed total mass, a larger r_s forces a smaller r_c,
  so the centre gets denser and the whole X-COP profile drops by about 0.27 dex (too heavy). It fixes G-OUT-M3
  (+2.41 → +1.17) and the groups (+1.83), but the inner lensing keys overshoot. This reproduces X68's reported variant
  independently: the same groups Z, the same three failing keys.
- **T1-B** gets the X-COP shape nearly flat (−0.08 ± 0.02 from 0.1 to 0.7 R500), so the core-versus-outskirts tilt is
  gone. The whole profile is about 0.1 dex too heavy, though, and its r⁻³ tail moves mass out of the 1.4–3 Mpc lensing
  band (G-OUT-M3 worse, +3.14).
  - In floor galaxies (S = 1) it is ρ ∝ (r + r_c)⁻³, not Burkert. SPARC goes 0.078 → 0.114 and the line fails.

**Reading.** Neither shape lowers the inner Σ while it raises the outer mass, and X68's reading said that is required.
Under the max() rule at fixed η and fixed halo mass, reshaping the profile trades one band for another. T1-B's flat X-COP
residual is the one new item: a cored-NFW tilt matches X-COP's shape. Its 0.1 dex offset, its cluster-outskirt miss and
its SPARC failure keep it from being a pass. Promoting it would need a new normalisation, which is a knob.

κ = ½ FITTED; c_f = 4 EXTERNAL; not theory closed. S = Σ_core/Σ_M ties the outer halo to a₀ (the spec's choice; X68
rejected it for its own frozen hypothesis).

## Scope

- X-COP is graded on HO1's committed grid, which ends at R500. The spec's R500–R200 band was not built.
- The X-COP Σ_core is X43's rule (c_f = 4), not CL2's c_f(M), so this baseline differs from HO1(a)'s −0.002 / 0.126.
  K0 reproduces HO1(a) with CL2's rule first.
- No fallbacks. Every halo had a compact r_c root.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x69_split_vs_cnfw.py`, `.out` / `_results.json`, `_MUTATE` versions (S → 2S),
`x69_x30_machinery*.log`, `run1.log`, `run_mutate.log`. Checks 7/7:
- K0: X68 → X43 exact, HO1(a) reproduced, baseline cluster preds = X43 to 0;
- K1: both closed forms vs quadrature, at most 7e-16;
- K2: solved r_c returns the mass;
- K3: RSS 0.40 GB.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_split_vs_cnfw.py            # ~200 s, exit 0
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x69_split_vs_cnfw.py --mutate   # S -> 2 S
