# QX16 frozen criteria: fix-forward of the elliptical late-binding bug

Frozen before the fix and before any rerun number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## The bug

`closure_2026_11_06/QX5_cluster_terms/qx5.py`, `ellipticals()`, builds `Mtot` and `Mbar` as `lambda r: ...`
inside the per-row loop. Python closures bind late, so `Mh, rs, mc, Mfit, Mkr, a` take the LAST row's values:
all 7 Humphrey+2006 ellipticals get one mass model (QX13 README: "all 7 share one total mass 10^11.53").
Each row's own `Re` (a dict field) was used correctly. So the radii were per-galaxy but the masses were not.

## The fix

Bind per row through default arguments (`lambda r, Mh=Mh, rs=rs, ...: ...`). It is a new commit; nothing is
rewritten. Unit check U1, run before any rerun: 7 distinct `Mtot(1e9)`, each equal to its row's
`Mvir_1e12 * 1e12` to 1e-3 relative (NFW plus stars at large r). Each `Mbar(1e9)` must equal `ups_krou * LK` to
1e-6. If U1 fails, nothing is rerun.

## Affected lanes (scripts that use QX5's `EL`)

| Lane | Script(s) | Gate(s) using ellipticals |
|---|---|---|
| QX5 | qx5.py (main, `--mutate`, QX5_GCUT=0.01) | the calibration set (T["E"], T["C"]) for classes a, b, d, e |
| QX7 iter_4 | qx7_iter4.py | ellipticals gate (ell_mean) |
| QX10 iter_2 | qx10_i2.py (main, `--mutate`) | G7 |
| QX12 iter_1 | qx12_i1.py, qx12_i1_post.py | elliptical depth/density points |
| QX12 iter_2 | qx12_i2.py (reads qx5.json) | elliptical threshold/shift |
| QX12 iter_3 | qx12_i3.py (main, `--mutate`) | G7 and c_min |
| QX13 | qx13.py (main, `--mutate`), diag_conv.py | G7 and c_min |

Not affected: QX6, QX7 iter_1-3 and QX5 iter_a2, which do not use `EL`. QX7 iter_2/3 read the TSV with their own
code, which has no lambda.

## Rules

- Every original output stays on the record unchanged. Reruns write SEPARATE outputs named `*_FIXED.*`. They run
  in a scratch mirror (scripts copied unchanged, the fixed qx5.py, real data symlinked), so downstream scripts
  read the fixed qx5.py and qx5_FIXED-equivalent JSON. Outputs are copied back under `_FIXED` names.
- Each lane's label is re-read under that lane's OWN frozen lines. Nothing is re-tuned. A changed label is reported
  as a change (old -> fixed) in the table. The old label is never silently replaced; the lane READMEs are not
  edited.
- Known answer K1: any gate that does not use ellipticals must reproduce its original number exactly (X-COP, groups,
  SPARC, KiDS). If one moves, the mirror is wrong, and that rerun is void.
- MUTATE: running the unfixed qx5.py in the mirror must reproduce the original qx5.json byte-for-byte or to
  float-print precision (the mirror reproduces the record).
- Compute <= 4 threads, nice 15.

## Output

README.md with one table: lane / gate / old value / fixed value / old label / fixed label. CLOSURE_FINAL.md rows
that change are updated. A line is appended to closure_2026_11_05/CLOSURE.md.
