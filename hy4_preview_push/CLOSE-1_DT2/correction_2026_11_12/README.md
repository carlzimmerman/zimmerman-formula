# CLOSE-1 (DT2) forward correction: corrected scripts (2026-11-12)

`dt2_form.py`, `dt2_linear.py`, `dt2_reach.py` and `dt2_run.py` are the corrected versions another session wrote
(the extra 1/a in the cosmological time map removed; the growth friction in ln a corrected from 3 to 2). They are
placed here so that the lane's own scripts and outputs stay exactly as first committed. `dt2_function.py` is an
unchanged copy of the lane's module, present only so the scripts import it from this folder.

Run here by the lead session, one thread, warnings suppressed; each `.out` is the captured standard output:
- `dt2_linear.out`: the linear gate K1 reads 0.49076 (FAIL) where the lane's committed output reads 0.5509 (PASS).
- `dt2_form.out`: first central event at 0.1420 Gyr (canonical) and 0.1401 Gyr (alt), as in the committed output.
- `dt2_run.out`: every run ends at the central cutoff and the settled radius column reads UNAVAILABLE.
- `dt2_reach.out` (added in a second commit; the run took several minutes): turnaround radii today of 1158 to 2758 kpc
  (canonical) and 1215 to 2876 kpc (alt), where the lane's committed table, made with the uncorrected time map, reads
  about 1700 to 4230 kpc. The residual column stays far from zero in both.

The lane's label FOLDS / FOLDS is unchanged. Independent check:
`reviews/codex_corrections_audit_2026_11_12/C3_kappa_and_dt2.md` (grade CORRECT; it adds that the fold gate as frozen
fires for any cold radial infall with no angular momentum).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
