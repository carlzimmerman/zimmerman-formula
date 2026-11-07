# GL3: re-read of the web-line side with the CMB-lensing Limber kernel corrected. FROZEN CRITERIA (committed alone, before any script or number)

Assigned by HOLD_KERNEL_REREAD_2026_11_07.md (GL3). Lane id checked free. Adopts nothing. Kappa = 1/2 FITTED; not
theory closed. Both footings, never pooled. **No label moves here:** GL3 reports old and new numbers. Any label that
would move is marked WOULD MOVE and held until GL2 (independent rebuild against CLASS) reads CONFIRMED. The owner
decides what is rewritten. No lane's committed files are touched.

## The correction
QX3 iter2 `limber_ratio` weights redshift by ((chi*-chi)/(chi chi*))^2 (1+z)^2 / H x P_delta / chi^2. The Limber
kappa kernel is proportional to (1+z)^2 (chi*-chi)^2 / chi*^2 / H x P_delta(k = (L+1/2)/chi). The code therefore
carries an extra chi^-4. Three kernels are run, set by an environment switch in a sandbox copy of iter2.py; everything
else in the copy is byte-identical:
- **old**: as committed (the KA);
- **new**: weight multiplied by chi^4 (the correction);
- **k2**: weight multiplied by chi^2 (MUTATE, a wrong power).

## Sandbox
A scratch tree is built outside the repository. closure_2026_11_06 and closure_2026_11_07 are extracted from origin/main
with `git archive`; every other top-level entry is a symlink to the shared checkout's data. Each lane's own script
runs unchanged in the sandbox and writes its outputs only there. Results are copied into GL3's directory, renamed by
kernel.

## Statistics (old = committed file; each re-run under old / new / k2; both footings)
| id | lane | statistic | frozen line (unchanged) |
|---|---|---|---|
| S1 | SV5 sv5_web iter_1 (+ iter_2 rows) | W1 web-lensing amplitude r, dchi2 | abs(r - 1) <= 0.072 |
| S1t | SV5 sv5_t0_iter3 | its graded lensing rows | as frozen in SV5 |
| S2 | WL1 | stage-2 line on q_pop (0.0354 at r <= 1.072) and q_pop | as frozen |
| S3 | OQ1, OQ2 | F_web,max (web row YES iff < 1) | as frozen |
| S4 | NA1 | I5 W1 r, readings A and B | 1.072 |
| S5 | FA2 | C1 web r; C2 L_max (0.3 Mpc) | 1.072 |
| S6 | FA3 | I1 / I3 / I4 W1 r | 1.072 |
| S7 | EW2 | W1 r on the mu grid; mu_w (smallest passing mu); gap to mu_h 0.063 | as frozen |
| S8 | QX27, QX28, QX29 | lensing dchi2 rows of each growth script | as each lane froze |
| S9 | QX31 | its limber_ratio lensing rows | as frozen |
| S10 | LD1 | static check: does any graded number call limber_ratio? (D1 uses CLASS raw_cl via X_of) | none |

## Checks and labels
- **KA (gating):** the old kernel in the sandbox reproduces each lane's committed graded numbers to the printed
  precision, or to rel 1e-9 where the JSON holds full floats. A lane whose KA fails is reported NOT RE-READ, with the
  cause.
- **MUTATE (gating):** on S1, the k2 kernel's S(L) over L 20-400 differs from both old and new by more than 1e-2
  somewhere. Otherwise GL3 is NO VERDICT.
- **Per statistic:** old, new, k2 values, both footings, and STANDS or WOULD MOVE (the new value crosses the lane's
  own frozen line). WOULD MOVE is held for GL2.
- **Order:** S1 first, since the web line is the root. If S1's line moves, S2-S7 are re-read against both the old
  line and the new line, reported side by side.

Heavy runs at nice 15, one thread, preemptible (rerun from the start on SIGTERM). Nothing above 1 GB RSS while a 1024^3
run is live, which is checked before each launch.
