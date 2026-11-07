# GL4 frozen criteria: QX15's cells C1-C4 and P1 re-read with the Limber k^-4 restored

Frozen before any GL4 script or GL4 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Fix-forward: a moved
label is REPORTED here, not rewritten in QX15; the owner decides. No other lane's file is edited. Cold dark energy, never
dark matter; no particle. Both footings (canonical a0 9.3603e-11, alt 1.1312e-10), never pooled. One thread, RSS < 1 GB,
no downloads (QX15's likelihood data are already on disk).

## 0. The error and the switch

- F1A (7026dcb48e) found that QX15's `do_cells` execs QX10 iter_1's `jcheck`, whose `Sfull` copies QX3 iter2's Limber
  ratio without the lensing potential's k^-4 = (chi/(L + 1/2))^4 (GL2 d0c3692fc6 CONFIRMED; GL1 4699adbbd7).
- GL4 builds the source exactly as QX15's `do_cells` does (same string patches: L to 7000, full-coverage mask, clamp of S
  beyond the last fully covered L), with one extra patch: each slice's weight in num and den is multiplied by
  (chi_j/(L + 1/2))^n. **n = 0 is the record; n = 4 is the corrected kernel; n = 2 is the MUTATE.** Everything else is
  QX15's code, imported read-only (qx15.py `make_obj`, `camb_D`, `pars_foot`, `nm`; qx15_like.grade_spectra).
- P1 (flat S = 0.5) has no Limber kernel in it. It is reproduced, not re-read: it is kernel-free and HOLDS by construction.
  Its role (the power control that must bite, Delta > 25, before C1-C4 can be labelled) is kept.

## 1. Statistic and labels (QX15's own)

- Record: Delta_cell = chi^2_PA(refit with S) - chi^2_PA(main fit), refit = QX15's Nelder-Mead (150 evaluations) from
  the main fit. Label Lc: Delta <= 4 PASS, 4-25 TENSION, > 25 FAIL; NO VERDICT if P1 does not bite.
- Corrected (n = 4), per cell and footing:
  - Delta_0 = chi^2_PA(main-fit theta, S_n4) - chi^2_PA(main). A refit can only lower it, so Delta_0 <= 4 is a PASS
    without a refit.
  - If Delta_0 > 4, QX15's refit (`nm`, same step, 150 evaluations, from the main fit) is run with S_n4 and its Delta
    sets the label.
- Verdict per cell x footing: **HOLDS** if the corrected label equals the record's, **MOVES** otherwise. Old and
  corrected numbers are both reported, plus S_min and the fully covered L for n = 0 / 4.

## 2. Known answers (error re-inserted)

- KA0: S_n0 equals QX15's parts/cellS.npz for C1-C4 (max |d| = 0, required <= 1e-12) and the coverage L equals
  cellS_meta.json (917).
- KA1: QX15's objective with the recorded S (n = 0 for C1-C4, flat 0.5 for P1) at each recorded cell best-fit theta
  reproduces the recorded cell chi^2_PA; at the main-fit theta (S = None) it reproduces chi^2_main. Both footings; required
  |d| <= 1e-6 (reported; target 0). The recorded Delta_cell follows by subtraction.
- KA2: S_n4 for C1-C4 lies within 1e-3 of 1 wherever GL1 found J1's max |1 - S| <= 1.8e-5 at L <= 2500 (consistency with
  GL1's L9, reported).

## 3. MUTATE (separate outputs gl4_MUTATE.*)

- M1: n = 2 gives S that differs from both S_n0 and S_n4 (max |d| > 1e-3 in each cell), and its Delta_0 is reported. It
  must differ from the n = 4 Delta_0 in at least one cell (BITES); otherwise GL4 is NO VERDICT.

## 4. Outputs

gl4.py writes gl4.json / gl4.out, gl4_MUTATE.json / .out; RESULT.md gives the old / corrected / HOLDS-or-MOVES table per
cell and footing. Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
