# A3 audit: data-row lanes and no-verdict repairs (2026-11-12)

Independent audit, read-only except this file. Committed versions audited (`HEAD`), not working-tree edits.
Re-runs: lane files extracted with `git archive HEAD` into a temporary sibling folder at the same depth, run with
`nice -n 19`, one thread, outputs compared byte for byte with the committed ones, copy deleted. Nothing downloaded.

| lane | label claimed | order ok? | re-run reproduces? | grade | reason |
|---|---|---|---|---|---|
| CRACK-1 ufr external field | R1, R2, R3 FAIL THE PAIR / FAIL THE PAIR | partly: criteria alone (16bc0102de); script and outputs landed in 089d304ecb 7 min BEFORE amendment A1 (52d62227df) | yes (only runtime lines differ; main + MUTATE) | SOUND WITH LIMITS | All three readings predict the ultra-faints low; measured +0.59. A1 says it was "committed before any CRACK-1 result"; true only of RESULT.md. Labels identical under frozen and amended lines. |
| CLOSE-4 no-verdict repairs (+ "CLOSE-5 labels") | repairs; no frozen label moved by R2/R3; R1 moves KL1/KL1R | NO: criteria, scripts and outputs all created in one commit 2547e9ff92; no earlier copy of the criteria in any ref | yes (m3, ma2_fixed, gc: byte-identical) | SOUND WITH LIMITS | No frozen file edited (all 19 paths "create mode", insertions only). Repairs live in a new folder, labelled post hoc. "Committed alone before any run" is not supported by git. |
| HY4-1 GAS1 hot-gas census | MISSING BARYONS EXCLUDED / same | NO: criteria, script, outputs and RESULT in one commit c5d897706f, whose message is "FINAL4 FROZEN CRITERIA ... committed alone" | yes (json identical; .out differs in timing lines only; main + MUTATE) | SOUND WITH LIMITS | Kills a rescue route (gas needed 328-3750x B21's hot gas; amplitude 0.039 vs line 0.891). Order cannot be shown. |
| DWF1 hosted dwarf offset | NO CANDIDATE MOVES A HOSTED DWARF UP / same | yes: criteria alone 34a3ee01f0; script and outputs later inside bundled commit f639380e36 ("FINAL mile") | main run yes (only runtime/RSS differ); MUTATE not re-run (~13 min, stopped) | SOUND WITH LIMITS | Negative result; every kill fires on both footings. No RESULT.md: the label exists only in `dwf1.out`. |
| HY4-2 STR1 anisotropic stress | STRESS CANNOT PAY / same | NO: criteria, script, output and RESULT in one commit f639380e36 | yes (only the elapsed line differs) | SOUND WITH LIMITS | Standard result: stress enters the lensing source at O(sigma^2/c^2) ~ 1e-7 to 2e-6 against a needed factor 5-20. Order cannot be shown. |
| VCC1 sourced charge current | EXCLUDED / EXCLUDED | yes: criteria alone c83dfb5a02, then result bdac874b1c | yes (main + MU1-MU5 byte-identical) | SOUND | Vacuum source is homogeneous: C ~ R^3 against the law's ~R; payment 17-2.3e4 x rho_Lam. |
| G242 settled radius = EFE radius | "SRH1's EMPTY WINDOW is a proxy artefact"; 5/6 PASS | NO: no criteria file; one commit d215a3d278 (replayed as 046584d3ec); working tree carries another session's uncommitted edits | yes (g242.out byte-identical) | OVERSTATED | Arithmetic reproduces; the rescue does not follow. Decisive step NOT CONFIRMED (below). |
| VSH1 viscous shock settling | NO VERDICT / NO VERDICT frozen; SETTLES BY SHOCK post hoc (A1) | yes: criteria alone b619f308af; A1 alone fce5461b1c after first run, disclosed; result; scan | NOT CHECKED (graded runs are 6e7-step, hours) | SOUND WITH LIMITS | Frozen and post hoc kept apart; asks for regrade. KA3' (fluid terms off) no longer tests the graded runs, where R_sh exceeds R_ta (2.66x at log M_b 9); disclosed. No row rescued: charge 1-4 % of the law's halo. |

## Does any lane rescue a failing row?

No. CRACK-1, GAS1, DWF1, STR1 and VCC1 are negative results (each closes a proposed escape). VSH1's post hoc
"settles" is about AKS1's estimate T7, not a data row, and it reports the amount short by 28-95x. CLOSE-4 repairs
mutation arms and a convergence rule; it rescues no row. The only rescue claim in this slice is G242's, and it does not
hold up (next section). The Lyman-alpha forest row still FAILS for form B.

## Does G242 overturn SRH1?

No. SRH1's verdict (WINDOW EMPTY / WINDOW EMPTY for one constant f in R_set = f R_fold) stands. G242 does not touch it. I
re-ran `g242.py`, and the reasons are below.

1. **Its own settled radius fails the forest.** G242 says R_set = r_M/e_N "has no free parameter". Taken that way it gives
   f_eff = 1.452 at z 2.5 and 2.386 at z 0.3 (M_b 1e11, R_struct 3 Mpc). SRH1's G1 needs f <= 0.72 at the forest. SRH1's
   table gives Delta chi^2 ~ 280 at f 1.5 and a FAIL at every f >= 0.75. The "window" in G242b only appears after a free
   rescaling f0 is added (`f0_lo = 1.25*f_ratio`, `f0_hi = 0.70`). That f0 is the free constant SRH1 already scanned.
   R_struct is free too. Absolute f_eff scales as R_struct^-1/2, and only R_struct >~ 12 Mpc brings f_eff(2.5) under 0.72.
   So the claim "no free parameter" is false.
2. **At fixed mass the window stays empty by G242's own line.** The ratio is 0.609 against 0.560 required. G242 records
   this as a FAIL.
3. **The "opening" rests on an input nobody computed.** The growth factor g >= 1.65 is not computed, and the README says
   so. The G242c check still prints PASS on a hard-coded g = 3. The growth argument is also misapplied: SRH1 evaluates
   R_fold(z, M_b) on each gate's own haloes at their own epoch (the forest's mass function at z 2.2-4.4, the KiDS lenses
   at z ~ 0.3). It does not follow one halo as it grows. The relevant input is the mass of the haloes in each gate, and
   G242 does not use it.
4. **No gate was re-run.** G242 runs no forest pipeline and no KiDS stack. Its R_fold is not FLD1's. It is an EdS-like
   R_ta built from M_b alone, times hard-coded R_fold/R_ta ratios: a cruder proxy than the one it calls an artefact.
   g_ext = sqrt(G rho_m a0 R_struct) from the mean cosmic density is an assumption: a uniform background exerts no net
   field. "Settled radius = EFE onset radius" is asserted, not derived. Only the canonical a0 is used, though a0 cancels.
5. **SRH1 already reported the tilt.** SRH1's A1 found post hoc that a tilt of -0.5 to -1 opens a window in a narrow f0
   slot, and counted it against the history. A candidate reason for that tilt is worth a pre-registered lane, with
   criteria first and both gates re-run. It is not a reversal.
6. **Smaller misquotes.** G242 quotes SRH1's G4 edge as f >= 1.25. That is the grid value; the interpolated edge is
   1.004 / 1.050. Its docstring and printed summary say "beta ~ -1"; the computed value is -0.50, right on the edge of its
   own pass range.

## Was any frozen label changed silently?

No. The CLOSE-4 commit only creates files. The "CLOSE-5 labels" are four new RESULT.md files: DW1, FINAL-7, FINAL-10 and
FINAL-11. They write up lanes that had outputs but no RESULT file. They do not edit frozen files. DW1's new RESULT.md
records G239's two withdrawals openly. CLOSE-4's R1 states that KL1/KL1R's Part A would read TENSION and Part B
CONSISTENT. That is a post hoc reading written in CLOSE-4's own folder, and KL1's folder is unchanged with no pointer to
it. One overstatement: CLOSE-4 calls Part A TENSION a result that "contradicts" A1, but KL1's RESULT.md already gives
Part A as TENSION / TENSION under A1 (p 0.038 / 0.037). R2 and R3 move no label, and the folder says so.

## Hygiene

- **Absolute home paths:** `hy4_preview_push/CRACK-1_ufr_external_field/compile_MUTATE.txt` has 14 lines starting
  with the owner's home directory (Lean compiler messages). No other lane in this slice has one.
- **"cold dark matter" / "CDM-like" for the theory's component:** none found.
- **Data said to favour the framework:** none found.
- **Footings pooled:** none. G242 computes the canonical footing only; it does not pool them.
- **Bundled or misattributed commits:** GAS1 sits inside a commit titled "FINAL4 FROZEN CRITERIA"; STR1 and DWF1's
  outputs sit inside "FINAL mile"; CRACK-1's script and outputs sit inside a commit shared with FINAL7F. Because of this
  bundling, the "criteria committed alone" claims of GAS1, STR1 and CLOSE-4 cannot be checked from git.

## Not checked

VSH1 re-run: the graded runs are hours long, so none was done. The Lean builds of CRACK-1: compile logs only. FINAL-7,
FINAL-10 and FINAL-11 contents beyond their labels. SRH1R, the blind re-grade, is scheduled separately and was not run.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
