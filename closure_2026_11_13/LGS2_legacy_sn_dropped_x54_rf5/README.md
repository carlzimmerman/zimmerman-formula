# LGS2 — X54 and RF5 with the legacy low-redshift supernovae dropped

Criteria, harness and collector: 430f903e62 (alone first, before any `des_only` number). Frozen labels: `lgs2_collect.out`,
`lgs2_results.json`. Post-hoc readings: `lgs2_posthoc_collect.out`, `lgs2_posthoc_results.json`.
Commit ids, local / origin: criteria 430f903e62 / f357715dcc; result f1b265b28c / 56ce49f62c.
A re-read of committed lanes (follow-on to LGS1). It adopts nothing and edits no ledger.

## Verdict
- **X54 primary (M-C, Q = ξHρ_c): class UNCHANGED, a0 grade UNCHANGED on both footings, STABLE at 95 % and at 68 %.**
  Still EXCHANGE EXCLUDED BEYOND; ξ̂ −0.00122 → −0.00160, 95 % [−0.00349, +0.00110] → [−0.00389, +0.00073]. The mild
  cold → DE lean grows (Δχ² at ξ = 0: 1.08 → 1.83), still under 4. The size control moves nothing (ξ̂ −0.00126).
- **X54 M-D (Q = ξHρ_DE, reported model): CHANGED.** UNDECIDED → EXCHANGE ALLOWED, a0 TENSION → CONSISTENT, STABLE at
  95 % but SHIFTED at 68 %. The DE → cold lean disappears: ξ̂ +0.110 → −0.003, Δχ² at ξ = 0 2.76 → 0.001. A post-hoc
  size control (not frozen) keeps M-D UNDECIDED at ξ̂ +0.108, so **M-D's preferred exchange came from the legacy
  supernovae.**
- **RF5: as frozen, NOT EVALUABLE.** RF5's own grader stops with a math error on the `des_only` sample (below).
  **Post-hoc reading, with one reporting-only line guarded: the verdict line is unchanged on both footings** ("a window
  exists at z_on in [30000, 1000000]", forest NOT DIAGNOSTIC). Label 1 still reads CHANGED, but only because the khronon
  row K0.03 goes UNDETERMINED → FAILS. That fit runs away in both samples: in `full` CLASS stops it, in `des_only` it
  gets stuck far from any minimum. Label 2 is SHIFTED at the two cells
  outside the window (2e4 +1.15, 1.2e4 +1.33) and within 1.0 at all five window cells. The edge cell 3e4 keeps a
  smaller margin to the 25 line: 2.97 → 2.18.

## Harness checks
- **X54: PASS, exact.** `full` through the harness equals the committed `x54_cold_de_exchange_results.json` at every graded
  grid point of M-C and M-D (max |Δχ²| 0, max |Δξ| 0). All three samples pass Step 0 and K1–K4 (7/7). The rebuilt
  binary: patch sha256 d66bbc98… identical to the committed patch; binary sha bebbd9c8… against debac461… (the build path is
  compiled in); K2 max |ΔC/C| 0.0 against vanilla; K3 growth 8.54284 vs ODE 8.54321, as committed.
- **RF5: PASS, exact.** `full` equals the committed `rf5_results.json`: every χ² part, shear χ² and S − S_min at 1e6 … 2e4
  (max |diff| 0), the same gates at 1.2e4 and 7000, the khronon labels, the shear kept set (101 points), and the 1e6 forest
  χ² 420.07 (G0 fails as committed). K1–K8 pass.
- The committed X54 and RF5 folders are untouched (`git status` clean for both after every run).

## Part A — X54 (profile likelihood in ξ; CMB + DESI DR2 BAO + DES-SN5YR)
| model | sample | ξ̂ | 95 % interval | 68 % interval | Δχ²(ξ = 0) | class | √X(2.33) → a0 grade |
|---|---|---|---|---|---|---|---|
| M-C | committed = full | −0.00122 | [−0.00349, +0.00110] | [−0.00238, −0.00005] | 1.08 | EXCLUDED BEYOND | 0.9974 CONSISTENT |
| M-C | des_only | −0.00160 | [−0.00389, +0.00073] | [−0.00277, −0.00042] | 1.83 | EXCLUDED BEYOND | 0.9966 CONSISTENT |
| M-C | rand197 (control) | −0.00126 | [−0.00352, +0.00106] | [−0.00241, −0.00009] | 1.15 | EXCLUDED BEYOND | 0.9973 CONSISTENT |
| M-D | committed = full | +0.110 | [−0.020, +0.200 grid end, not closed] | [+0.044, +0.177] | 2.76 | UNDECIDED | 1.0685 TENSION |
| M-D | des_only | −0.003 | [−0.175, +0.159] | [−0.089, +0.080] | 0.001 | EXCHANGE ALLOWED | 0.9981 CONSISTENT |
| M-D | rand197 (post hoc) | +0.108 | [−0.023, +0.200 not closed] | [+0.041, +0.175] | 2.60 | UNDECIDED | 1.0669 TENSION |

Absolute a0(2.33) at ξ̂, canonical / alt footing (m/s², never pooled): M-C 9.336e-11 / 1.1282e-10 → 9.329e-11 / 1.1274e-10;
M-D 1.0001e-10 / 1.2086e-10 → 9.342e-11 / 1.1290e-10. The grade reads the ratio √X, so both footings carry the same label.

- **Label 1, M-C:** class UNCHANGED (EXCHANGE EXCLUDED BEYOND); a0 grade UNCHANGED, canonical and alt.
- **Label 2, M-C:** STABLE (95 %) and STABLE (68 %): each best fit lies inside the other's interval.
- **Matched band:** graded against LGS1's legacy-dropped TD5F band at z 2.33 (0.654–1.009), M-C stays CONSISTENT (0.9966).
- **Control, M-C:** `rand197` UNCHANGED / STABLE / STABLE. `des_only` changes no M-C label either, so there is no change to
  attribute.
- **M-D (reported model):** class CHANGED (UNDECIDED → EXCHANGE ALLOWED); a0 grade CHANGED (TENSION → CONSISTENT), both
  footings; STABLE at 95 % (the committed interval was open to the grid edge) and SHIFTED at 68 %. M-D's interval now
  closes on the frozen grid. Its class is ALLOWED, not EXCLUDED, because the lower end permits a produced fraction of
  −20 % (cold → DE), past CFG253's 3 % convention. ξ = 0.4 still fails in CLASS's θ_s shooting and 0.6 does not converge,
  as committed; both lie outside the new interval. Matched band: CONSISTENT (0.9981).
  Some ξ in the new 95 % interval reaches CFG689's median 0.909 (√X range 0.900–1.100); the committed interval did not
  (0.988–1.128).

Reported, no label:
- **F_made** at ξ̂ [95 % ends]: M-C −0.86 % [−2.47, +0.77] → −1.13 % [−2.76, +0.51] (control −0.89 % [−2.49, +0.74]);
  M-D +9.0 % [−1.9, ≥ +15.0] → −0.3 % [−20.4, +12.5].
- **S8** at ξ̂: M-C 0.8313 → 0.8306; M-D 0.7976 → 0.8209. At ξ = 0: 0.8229 → 0.8200.
- **The ξ = 0 refit:** H0 68.47 → 68.59, Ω_m 0.3009 → 0.2993, ω_c 0.11859 → 0.11832. Its χ² parts: CMB 1004.53 → 1005.02,
  BAO 12.33 → 11.48, SN 1635.28 (1,820) → 1416.78 (1,623).
- **CPL fit at ξ̂:** M-D (−0.56, −2.23) → (−1.009, +0.041). Without the legacy set, M-D sits at w = −1.

## Part B — RF5 (turn-on epoch z_on of the cold component)
**As frozen: NOT EVALUABLE.** The `des_only` chain, khronon fits and channels all ran (exit 0). RF5's own grader then
stopped with "math domain error" (`logs/rf5_des_only_grade.txt`; its line numbers are one high because the harness adds
a line). The cause is the khronon cell K0.03 (v3s, μ_K 0.03).
- In the committed run and in `full`, its fit ends in CLASS's stiff-solver failure, which reads UNDETERMINED.
- In `des_only` it starts from a different 1e6 best fit and runs on. After 29 failed CLASS runs it stops with no fall on a
  fresh Jacobian, at steered χ² 1.3e5, plik 1.2e5, wa −7.7, Ω_DE −0.55, h 0.45.
- RF5's fit loop counts that stop as converged. Its per-cell a0 readout, a0 = ½c√(Gρ_crit Ω_DE), then takes the square
  root of a negative number.

**Post-hoc reading** (`lgs2_posthoc_rf5_grade.py`): the same grader with that one readout guarded (None when Ω_DE ≤ 0);
no gate reads it. Run on `full`, it reproduces the frozen `full` grade byte for byte.

| z_on | S − S_min committed → des_only | Δ | w0 | wa | Ω_m | h | σ8 | √X(2.33) | gates |
|---|---|---|---|---|---|---|---|---|---|
| 1e6 | 0.14 → 0.13 | −0.01 | −0.813 → −0.877 | −0.67 → −0.46 | 0.312 → 0.307 | 0.675 → 0.680 | 0.826 → 0.827 | 0.848 → 0.882 | window |
| 3e5 | 0.00 → 0.00 (S_min) | 0.00 | −0.827 → −0.868 | −0.60 → −0.48 | 0.312 → 0.308 | 0.675 → 0.679 | 0.824 → 0.826 | 0.866 → 0.887 | window |
| 1e5 | 0.82 → 0.85 | +0.03 | −0.819 → −0.879 | −0.64 → −0.45 | 0.312 → 0.307 | 0.675 → 0.680 | 0.816 → 0.819 | 0.855 → 0.883 | window |
| 5e4 | 4.14 → 4.64 | +0.50 | −0.818 → −0.847 | −0.66 → −0.58 | 0.312 → 0.309 | 0.675 → 0.677 | 0.796 → 0.798 | 0.843 → 0.849 | window |
| 3e4 | 22.03 → 22.82 | +0.79 | −0.782 → −0.815 | −0.85 → −0.74 | 0.314 → 0.312 | 0.673 → 0.675 | 0.756 → 0.755 | 0.777 → 0.798 | window (edge) |
| 2e4 | 100.48 → 101.63 | +1.15 | −0.749 → −0.770 | −1.03 → −0.95 | 0.315 → 0.315 | 0.669 → 0.670 | 0.689 → 0.688 | 0.721 → 0.739 | absolute gates only |
| 1.2e4 | 549.64 → 550.97 | +1.33 | −0.743 → −0.736 | −1.07 → −1.07 | 0.314 → 0.315 | 0.663 → 0.662 | 0.550 → 0.549 | 0.711 → 0.719 | fails plik (p 5e-29) |
| 7000 | — (no shear; P(k) run fails in both) | | −0.835 → −0.888 | −0.35 → −0.21 | 0.299 → 0.294 | 0.662 → 0.667 | — | 1.034 → 1.046 | fails plik |

- **Label 1 (verdict per footing):** CHANGED (post hoc), canonical and alt, and only through the khronon rows.
  - The verdict line itself is identical: "a window exists at z_on in [30000, 1000000] (forest NOT DIAGNOSTIC (G0);
    CMB = plik-lite; shear = DES Y3 xi+ linear-safe)".
  - Khronon rows: K0.03 UNDETERMINED → FAILS (the stuck runaway above); K0.1 UNDETERMINED in both (not converged in
    10 steps; steered χ² 4.2e4 committed and `full`, 6.1e4 `des_only`).
  - Neither K0.03 fit is a minimum. The change says the runaway's end point depends on its start, not that the v3s row
    found a fail.
- **Label 2 (S − S_min within 1.0 at every cell where S is defined):** SHIFTED at 2e4 (+1.15) and 1.2e4 (+1.33), both
  outside the window and far past the 25 line. All five window cells move by less than 1.0 (−0.01 to +0.79).
- **Reported:**
  - Edge margin at 3e4: 2.97 → 2.18.
  - S_min 2324.03 → 2113.50 (the SN χ² has 197 fewer terms). The S_min cell stays at 3e5.
  - Forest G0 still fails: 420.1 → 422.3 / 327, p 3.8e-4 → 2.9e-4, so the forest stays NOT DIAGNOSTIC.
  - Shear kept set identical (101 points); G-A0 passes at every cell where it passed.
  - SN χ² ≈ 1,418–1,421 for 1,623 supernovae (p ≈ 1.0), against 1,629–1,630 for 1,820.
  - Native a0(0) at κ = ½ at the S_min cell, on the lane's own h and Ω_DE: canonical 9.405e-11 → 9.473e-11, alt
    1.134e-10 → 1.139e-10 m/s².
  - Across the window w0 moves toward −1 by 0.03–0.06 and wa toward 0 by 0.08–0.21. √X(2.33) rises by 0.006–0.034.

## Reported outside the frozen rules (post hoc)
- `lgs2_posthoc_md_control.py`: the frozen `rand197` draw run through M-C and M-D (the frozen control ran M-C only).
  - Its M-C half reproduces the frozen `rand197` M-C exactly (max |Δχ²| 0).
  - Its M-D half stays UNDECIDED / TENSION (ξ̂ +0.108, Δχ²(ξ = 0) 2.60).
  - By the frozen control rule, M-D's class change and its 68 % shift come "from the legacy set".
- `lgs2_posthoc_rf5_grade.py`: the one-line guard described in Part B.
- `lgs2_posthoc_collect.py`: the frozen collector's rules on those outputs.
- Context only, not tested here: X54's committed Pantheon+ and Union3 M-D profiles also lean DE → cold (Δχ² 1.9 each).
  Both sets carry their own low-redshift samples, which this lane does not touch.

## On the guess made before the run
"X54's primary class and interval barely move; RF5's verdicts are unchanged."
- **X54 primary: held.** The class is unchanged and both edges move by about −0.0004, a third of a σ.
- **What the guess missed: M-D.** Its DE → cold lean is gone without the legacy set.
- **The reason given ("the CMB dominates the exchange bound") was not tested.**
- **RF5: held for the verdict line.** The window [3e4, 1e6] is unchanged. Only the runaway khronon row flips label, and
  only after the grader fix.

## Not run
- **X54:** the Pantheon+ and Union3 profiles (no Dovekie supernova), the S1 supplement, MUTATE.
- **RF5 cells:** z_on 4000 and below (unfinished in the committed run; UNDETERMINED in both). The forest at 1.2e4 and 7000.
- **RF5 `full` sample:** no forest beyond 1e6.
- **RF5 checks and controls:** K9, MUTATE, the restart check, and any size control. Machinery checks K1–K8 ran on `full`
  only.
- No guard or wall-time limit was hit. Free disk stayed at 17–18 GB.

## Files
- **Harness and criteria:** `lgs2_run.py`, `lgs2_collect.py`, `FROZEN_CRITERIA.md`.
- **Post-hoc scripts:** `lgs2_posthoc_*.py`.
- **X54 runs:** `lgs2_x54_<sample>.{out,json}`, `lgs2_posthoc_x54_rand197_CD.{out,json}`.
- **RF5 grades:** `lgs2_rf5_full.{out,json}` (frozen grade, `full`), `lgs2_posthoc_rf5_<sample>.{out,json}`.
- **RF5 cells:** `rf5_cells_<sample>/`.
- **Logs:** `logs/*.txt` (`.txt` because the repo ignores `*.log`), with home paths replaced by `<repo>` and numpy's known matmul RuntimeWarnings removed (RF5 README,
  "Fit health").
- **Outside the repo:** build and work directories in `../_external_data/x54_class_build_lgs2` and
  `../_external_data/rf5_work_lgs2_<sample>`.

## What this does and does not say
- X54's primary exchange bound (Q ∝ ρ_c) does not lean on the legacy supernovae.
- X54's M-D preference for DE → cold (about 1.7σ with DES-SN5YR) does: without the legacy set it is gone, and the form
  becomes loosely bounded on both sides.
- RF5's window [3e4, 1e6] does not lean on them. Its edge margin shrinks by 0.8 but stays inside the 25 line.
- It does not say which supernova sample is right. arXiv:2610.23657 argues the legacy set is offset by about +0.065 mag;
  this lane does not test that.
- Nothing here measures H0 or a0, and nothing here grades the framework.

## Commit ids
Local / origin: criteria 430f903e62 / f357715dcc; result f1b265b28c / 56ce49f62c (origin ids differ because the lane
commits were replayed onto origin/main without a checkout).

kappa = 1/2 FITTED; not theory closed.
