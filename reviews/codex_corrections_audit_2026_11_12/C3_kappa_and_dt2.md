# C3 audit: the Codex correction notices on the kappa lanes and on CLOSE-1 (DT2), 2026-11-12

Independent auditor. Read-only on every lane file. Graded the UNCOMMITTED working-tree edits against
`git show HEAD:<file>`. Every script was run from a copy in a scratch folder (one thread, `nice -n 19`),
and the decisive numbers were re-derived by hand or with my own short script. Where I only re-ran the
notice's script, I say so.

## Verdict table

| item | grade | one line |
|---|---|---|
| CLOSE-1 DT2 notice + `dt2_linear.py` (friction 3 -> 2) | CORRECT | delta'' + (2 + dlnH/dlna) delta' is the right equation; K1 moves PASS 0.5509 -> FAIL 0.49076 (re-run) |
| DT2 `dt2_form.py` / `dt2_reach.py` (time map 1/(aH) -> 1/H) | CORRECT | my quadrature: z 10 -> 0 is 12.8854 Gyr; the old map gives 30.429 Gyr |
| DT2 "R_set(0) = 0 withdrawn, UNAVAILABLE" | CORRECT | committed `dt2_run.out` prints R_set(0) ~ 3000 kpc and cover PASS; RESULT's 0 kpc / residual 1.0000 was never an output |
| DT2 "force lacks its homogeneous limit" | CORRECT | dust is Omega_c only, no Lambda, no smooth baryons, while v_i uses H with Omega_m |
| DT2 label FOLDS / FOLDS | UNCHANGED | first central event 0.7086 / 0.1420 / 0.0906 / 0.0622 Gyr (canonical) is identical before and after; only K1 and the derived value move |
| DT2 band-shift argument (notice cites it) | CORRECT WITH LIMITS | x(216) = n0 x 215/400 = 1.1429e-8 < 4e-6 checked; covers one monotone band only, as it says |
| DT2 scripts edited IN PLACE | FLAG | committed `.out` files now describe the old revision; `dt2_run.py` no longer computes R_set or the residual at all |
| FINAL-17 notice | CORRECT | g_N = G M_b / r^2 cannot scale at fixed source; matches A1 |
| `final17_kappa_A.py` edit | OVERSTEPS | main label and all numbers unchanged (re-run), but the pre-registered label `KAPPA DERIVED (CAPACITY)` in the else-branch was replaced by an unregistered `UNDECIDED (...)`, so the MUTATE twin now prints a different label from its committed `.out`; `A4_nogo` hard-coded False |
| FINAL17.lean, OUT5.lean | CORRECT (comments only) | code after stripping comments is byte-identical to HEAD; both copies compile, exit 0, 0 errors, 0 sorry; FINAL17 13/13 standard axioms |
| OUT5 notice | CORRECT | deep branch: rho_c = sqrt(G M_b a0) / (4 pi G r^2), proportional to sqrt(a0) at fixed M_b, r (my derivation) |
| OUT-2 notice | CORRECT | agrees with A1 (lock postulate = kappa^2 = 2/(3 pi)); goes no further |
| OUT-3 FROZEN_CRITERIA notice | CORRECT physics, WRONG place | tau -> 2 tau: Q -> 2Q, V_Sigma/Q halves; the (Q-1)^2 term picks Q = 1, so no symmetry. The text is right but sits inside a frozen file |
| OUT4 notice | CORRECT | my dimensional analysis below: the census fixes the form, never the number, and cannot exclude a dynamical F(kappa) = 0 |
| FINAL6 notice | CORRECT | FINAL6's own K4 uses rho_m(z_f), a frozen constant, which contradicts its section 1 "only rho_Lambda is constant" |
| FINAL3 / CLOSE3 notice | CORRECT | Xc = 5.41 Fc/Fb is patch bookkeeping; no derivation claimed |
| CRUX notice | CORRECT WITH LIMITS | 5.41 / 59.5 = 0.0909244 checked; differential retention is allowed, not shown |
| FRAMEWORK notice | CORRECT | law B gives sqrt(2) a0 at g_N = a0, law S gives 1.618 a0; matches A1's WRONG grade on sections 2-4 |
| CLOSURE, DOORS notices | CORRECT WITH LIMITS | scope notices; DOORS does not say the DT2 label stands |
| H062 notice + script | CORRECT | Y = g/s = x/n; re-run: Cassini-safe set is now {6, 8, 10, 20}, joint still empty, exit 1 |
| CLOSE2 `close2_grade.json` (+3 lines) | NOT A CORRECTION: do not commit | a re-run's side effect at 12:23; it lists `_a2tmp_CLOSE2/close2_grade.py`, a temp folder that no longer exists |
| `lakefile.toml` (+6 lines) | CORRECT WITH LIMITS | adds `lean_lib FINAL9to12`; its root `FINAL9to12.lean` and folder are untracked, so committing it alone gives a broken target; default targets unchanged |

No notice claims a pass, a derivation, a rescue or a completed theory. No "cold dark matter", no home
paths in the notice text. None says kappa or 5.41 is derived. Every notice adds text above the body and
deletes no line of the record. The exceptions are the in-place script edits (DT2, FINAL-17, H062) and
the OUT-3 frozen file.

## Decisive checks

**DT2 growth (K1).** With d/dt = H d/dln a: delta_t = H delta', delta_tt = H^2 delta'' + H H' delta'.
Put into delta_tt + 2H delta_t = 4 pi G rho F delta and divide by H^2. That gives
delta'' + (2 + dlnH/dlna) delta' = 1.5 Omega_m(a) F delta. The committed "3" is wrong. In an
Einstein-de Sitter background the old equation has a growing exponent 0.686, not 1. My own integral
D(a) = 2.5 Omega_m E(a) times the integral of da/(aE)^3 gives D(1)/D(1/7) = 5.5009 for Omega_m = 0.31.
The corrected script's D_ref is 5.5085 (its delta' = delta start is not exactly the growing mode, off by
0.14 %). The committed 3.4948 is wrong. I re-ran the edited `dt2_linear.py` from a copy and got ratio
0.49076 at k = 20/3 per Mpc comoving: FAIL against the frozen 0.50, by 0.009, which is larger than the
starting-condition effect. The other three k still pass.

**DT2 time map.** The integral of dln a / H from z = 10 to 0 is 12.8854 Gyr. The old integral of
dln a/(aH) gives 30.429 Gyr (my quadrature, matching the notice's 12.8857 / 30.4296). In
`dt2_form.py` the scale factor from the time map is used only for labels and for the run length; the
forces never read a(t). So the corrected run gives the same event times as before: 0.7086 / 0.1420 /
0.0906 / 0.0622 Gyr canonical and 0.6687 / 0.1401 / 0.0866 / 0.0601 Gyr alt (edited `dt2_run.py`
re-run, 9 s). Only the redshift labels move: the first event at log M_b 10.45 is at z = 8.19, not the
z = 9.8 that RESULT quotes. In the old absorbing run the 30 Gyr span let collapsed material pile up for
2.4 times too long. That is where the ~3000 kpc "R_set" in `dt2_run.out` comes from.

**Does the correction move the DT2 label?** No. K3(a) is "no shell reaching r = 0 before z = 0". The
innermost shell reaches the 0.5 kpc floor at the same times as before, on both footings, and K2 still
fires on alt. K1 now also fires. The label stays FOLDS / FOLDS on more kill conditions than before. Two
things are withdrawn: the K1 PASS, and the derived value R_set(0) = 0 with its residual 1.0000. Neither
was ever a computed output. The background error is that dust feels Omega_c = 0.26 while starting at the
Omega_m = 0.31 Hubble speed, with no Lambda. At z = 10 this under-decelerates shells, which works against
collapse, so the error cannot have produced the fold. One limit the notice does not state: K3(a) as
frozen fires for any cold, zero-angular-momentum radial infall. So FOLDS says DT2 does not escape cold
radial collapse. It does not say a physical halo cannot form.

**DT2 in-place edits.** `dt2_run.py` lost the R_set, KiDS-coverage and residual columns that K3(b) and
the section 5 residual need. It now prints UNAVAILABLE by construction, and absorption is off by default
in `dt2_form.py`. The committed `dt2_run.out`, `dt2_linear.out` and `dt2_reach.out` no longer come from
the committed scripts. The corrected `dt2_reach.py` did not finish inside 120 s, so I did not check its
new numbers. Its old table (R_ta(0) 1700-4200 kpc) comes from the 30 Gyr map and should be read as void.

**FINAL-17 script.** I re-ran it from a copy. The main stdout differs from the committed `final17.out`
only in the A4 wording, and the label stays `KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED`. The
MUTATE run (exit 1, as before) now prints `LANE LABEL: UNDECIDED (no independent coefficient mechanism
supplied)` where the committed `final17_MUTATE.out` prints `KAPPA DERIVED (CAPACITY)`. That label is in
PREREGISTER section 6, and AMENDMENT_A1 section 3 names it as the deliberate false label the mutation arm
must produce. Replacing it rewrites a pre-registered label set in place. The physics notice is right, but
this code edit is not a forward correction. Revert that line, or put it in a separate corrected copy. A
smaller oddity: `ok_A4` still gates the main label, although the notice withdraws what A4 was graded for.

**Lean.** I compiled copies of the edited FINAL17.lean and OUT5.lean with `lake env lean`: both exit 0,
with no error and no sorry, and lake fetched nothing. With comments stripped, both files are identical to
HEAD. The theorem statements did not change: `kappa_is_a_flat_direction` still states
rhoPinDeepOf dsg G a0a = rhoPinDeepOf dsg G a0b for a definition that ignores a0. The new comment
describes that correctly; the theorem name is still misleading. The lakefile edit registers a library
target only. It played no part in either compile.

**OUT4: my dimensional analysis.** Take a = c^al G^be rho^ga for an acceleration (L T^-2).
M: -be + ga = 0. L: al + 3be - 3ga = 1. T: -al - 2be = -2. So be = ga, al = 1 and be = 1/2, and
a0 = kappa c sqrt(G rho), with kappa free. The (G, c, rho) matrix has det -2, as OUT4 says, so there is
no dimensionless group, and adding a0 gives exactly one, kappa. All of OUT4's O2 arithmetic is right.
What does not follow is OUT4's "any mass-independent derivation of kappa is a choice of value dressed
in other variables". Dimensional analysis is silent on pure numbers, whether they are derived or
chosen. An equation of motion can still give F(kappa) = 0 with a computed root; 2 pi from a KMS period
or 8 pi/3 from Friedmann are the usual examples. OUT-2 is one such equation; it fails because its lock
is postulated, not because of dimensions. The G_lambda "gauge" behind O10 also needs g_N -> lam g_N,
which is impossible at fixed baryons (deep regime v^4 = G M_b a0). So the notice is right: the census
proves neither a dynamical no-go nor a physical redundancy. OUT4's own verdict (T* is the same statement
as kappa = 1/2 and is not forced; the window is 0.378 dex wide) is untouched.

**FINAL6.** Section 1 says a value frozen at formation "cannot inherit the time dependence of rho_m(z)"
and concludes that rho_* = rho_Lambda. But rho_m(z_f) at a fixed z_f is a constant, and K4 of the same
file uses exactly that (z_f = 0.2955 canonical). The notice removes FINAL6's claim to select the
canonical footing, which is right. Its label KAPPA NOT DERIVED (FITTED) stands.

**OUT-3 criteria.** dV4/dtau = sqrt(h) d^3x / Q. Under tau -> 2 tau, Q doubles and the leaf measure is
unchanged, so V_Sigma/Q halves. The term mu_K^2 (Q - 1)^2 / (2K) goes from 0 to mu_K^2/(2K) at the old
vacuum. C1's "invariant" is not invariant. The notice is correct, but it is written into
FROZEN_CRITERIA.md. The commit message of 12889209cb sets the house rule: "Forward only: no frozen file
edited". OUT-3 has no RESULT.md, so the notice belongs in a new `CORRECTION_2026_11_12.md` in that
folder. As written it changes no criterion and is dated and labelled post-run, but it does change the
bytes of a frozen file (only the Codex manifests record its hash).

**H062.** With mu(Y) = 1 - (1+Y)^-n and Y = g/s, the deep limit is mu ~ nY = g/(s/n), so a0 = s/n. In
units x = g/a0 the kernel is mu(x/n). The committed Cassini loop called mu(x), which counts n twice.
n = 1 is unchanged, as it must be. My re-run from a copy gives Q_zz/ceiling = 6.84 (n=2), 4.05 (3),
2.26 (4), 1.24 (5), 0.67 (6). The Cassini-safe set is {6, 8, 10, 20} and the joint set is still empty.
The run exits 1 because the RAR pick is n = 3 and the check now requires n = 2. The committed
`H062_results.out` (safe set from n = 3) is stale. The MD's table pairs n = 2 (Mandel family, via
kappa = 1/n) with route1B's n >= 5 (BN11 family), and the script's own check 1.1b says those families
differ. The notice is right.

**CLOSE2 JSON.** The R8 scan walks the whole repository. The 12:23 file time matches the A2 audit, and
the three added paths are the lane's later RESULT.md and .out plus a deleted `_a2tmp_CLOSE2` copy. This
is a re-run artefact, not a correction. R8's note and verdict do not change. The owner should restore it
from HEAD rather than commit it.

## PAPER72 v1.2 recommendations

- **Section 8.2, CLOSE-1 (line 247)**, replace the pending clause with: "CLOSE-1 computed whether a
  forming halo reaches its static state with that function: FOLDS on both footings (A2: SOUND WITH
  LIMITS). A forward correction repairs two coding errors (an extra 1/a in the time map; growth friction
  3 in place of 2). The linear gate now fails, 0.491 against its line of 0.50 (it read 0.551), and the
  derived settled radius is withdrawn as unavailable. The first central infall, at 0.142 / 0.140 Gyr
  for log M_b = 10.45, is unchanged, so the label stands." Commit the notice first, and say that the
  committed `.out` files are from the old scripts.
- **Section 8.5, FINAL6 (line 265)**, replace the pending clause with: "...FINAL6 reads KAPPA NOT
  DERIVED (FITTED) + FORMATION REFUTED (per-galaxy). Its forward correction withdraws the step that
  selects rho_Lambda (a density frozen at a fixed epoch is also constant), so FINAL6 does not pick the
  canonical footing, and its refutation covers the two per-galaxy constructions it tested."
- **OUT-2**: no change. The paper already carries A1's WRONG grade, and the notice agrees.
- **OUT4**: optional addition: "OUT4's dimension census shows only that dimensional analysis leaves
  kappa free; it is not a no-go."
- **FINAL-17**: add "and its A4 reading of kappa as a flat direction is withdrawn: at fixed baryon mass
  and radius a0 is observable". The label sentence stands.
- **OUT5**: no change. "BOOTSTRAP KILLED" rests on the fixed-mu_K obstruction, which the notice leaves
  standing, and the paper never cites the flat-direction theorem.

## What I did not check

- The corrected `dt2_reach.py` numbers: the run was stopped at 120 s.
- The `cosmology_diagnostic` "independent expansion benchmark" that the DT2 notice cites, and the six
  shell-ladder cutoff times other than 260 shells (that one matches my run).
- The Codex regression tests, beyond reading `tests_final.out` (4 tests, OK).
- H062's inherited QUMOND-to-AQUAL calibration and its quadrature warnings, which the notice discloses.
- FINAL4's notice (outside this slice) only for arithmetic: 1 - 0.87978 = 12.02 %, against the file's
  "3.6 %" prose. Correct.
- The CLOSURE and DOORS references to PIK1 and FINAL5 belong to other slices.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
