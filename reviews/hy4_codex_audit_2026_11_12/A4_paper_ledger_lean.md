# A4 audit: PAPER74, DOORS.md, the hy4 Lean files (2026-11-12)

Read-only audit. Base: origin/main a1f5178885 (PAPER74 + DOORS.md landed in 0e2b0a5489). Footings never pooled.

## 1. PAPER74 (`qwen_claude_field_theory/papers_2026/PAPER74_flagship_the_weeks_program_2026.tex`, v1.0, 514 lines)

**Title:** "The a0 Law as a Measurement, Form B and Its Rules, the Reach-Amount Lock, and the Symmetry That Makes
kappa a Convention". **Central claim:** the law is "a measurement, not a hypothesis"; form B is six rules; T4 + LFS1
lock the halo at the charge carried in, and the 59.5 M_b share is 11.0x the 5.41 budget; GAS1 closes the
missing-baryon flank; a stacked tSZ test decides it; an exact scaling symmetry makes kappa = 1/2 "a convention the
formation reading forces".

**Overclaims.** The header says kappa fitted and theory not closed (good), but the body says: "The rules are complete as
a predictive theory" (l.480); "a0 = kappa c sqrt(G rho_L) with rho_L selected: derived" (l.468); kappa = 1/2 "forced"
by an "exact symmetry" G_lambda (ll.417-455). That section is withdrawn by the uncommitted 11-12 correction to
`hy4_preview_push/FRAMEWORK.md` ("Ratio covariance is not a symmetry at fixed baryon source; kappa is a dimensionless
physical coefficient, not a unit convention") and FINAL-17's scope correction. Rescaling g with G, M_b, r fixed breaks
g_N = G M_b/r^2. It does not say the data favour form B. "In the deep field Pi_rr = -Pi_tt exactly" (l.151) conflicts
with its own approach numbers (0.066 at 30 r_M) and with FINAL-10's `claimed_identity_false` (the residual is > 0 for
every u > 0). The identity is asymptotic, not exact. ONE1's "passes its frozen gate at 1.6 R_h" omits that 1.6 R_h is
amendment A2 (post hoc, written after graded numbers) and that at the frozen 1.0 R_h veto it misses by -2.7 sigma
(ONE1 RESULT l.4, l.21). FINAL5's "~100 sigma ... no outcome in between" is superseded by the 11-12 forward
correction in FINAL5's RESULT.md (uncommitted).

**Ten spot checks (quote vs lane file):**
1. SHP1 worst bin 0.057 / 0.021 dex, line 0.10: MATCH, `fable52_push/SHP1_cold_component_shape/RESULT.md` l.18.
2. Outer amplitude 1.4002 +- 0.2211: MATCH, `hy4_preview_push/HY4-1_GAS1_hot_gas_census/RESULT.md` l.46. Model 1.003 / 0.847: MATCH, ONE1 RESULT l.44, l.50.
3. GAS1 G4 0.0392 +- 0.0069 / 0.0324 +- 0.0057 and label: MATCH, GAS1 RESULT l.1, l.43. Column 6.1627: MATCH, l.19.
4. FINAL-4 Delta chi^2 9916.246 / 9008.690: MATCH, `closure_2026_11_11/FINAL4_growth_history/RESULT.md` l.10, l.123.
5. FINAL-19 6.0 +- 1.4 / 7.3 +- 1.6, 22.1 / 27.6 sigma: MATCH, `hy4_preview_push/FINAL-19_kappa_C/RESULT.md` l.12, l.47.
6. EDG1 "FAILS AT E3 (19-38x short)": MATCH, `closure_2026_11_10/EDG1_held_edge_layer/RESULT.md` l.3, l.22 (19-38x is PROVISIONAL there; the paper drops the tag).
7. ELA1 "ELASTIC SOLID FAILS AT S0 (+S2, B1)": MATCH, ELA1 RESULT l.1.
8. ONE1 rejects X = 5.41 at +4.85 / +4.93: MATCH, ONE1 RESULT l.66.
9. FINAL5 17,335 lenses, 0.0101: MATCH, FINAL5 RESULT l.17, l.34. The number traces, but the lane now carries a superseding correction.
10. FINAL-15 label, FINAL-2 label, CLS2, VCC1, LFS1 ILL-POSED: MATCH (each RESULT l.1-5). PIK1 NO VALUE: MATCH on the committed bytes, but the working-tree head now says "universal NO VALUE is not established".

Result: 10/10 numbers trace. The faults are in what the paper leaves out and how it frames the numbers.

**Newer failing rows.** The paper does **not** state that the Lyman-alpha forest row FAILS. FRZ1 appears only as
"the formation reading derives FRZ1's baseline" (l.270). FRZ1R (blind, 8142 / 7686) and FRZ2 (no a0(z) passes) are
absent, and so is DSB1 (NO POWER). "Forest" appears nowhere in the paper. EDG1 is carried correctly. SRH1 WINDOW EMPTY is
carried, but the paper says the required history "is being computed". HLF1 and EFN1 are absent; SCS3 is cited for the
external field.

**Audit script.** `PAPER74_audit.py` exists and exits 0: 190/190, and `--mutate` 169/169. Weaknesses: (a) it accepts
a literal from the working tree, HEAD **or** origin/main. AMT1's `AMOUNT_BUDGET.md`, the source of the lock table,
is untracked (it prints "working tree only"), so the gate passes on a file that no one else can see. (b) It checks
that each literal is present, not what the claim says, so all the overclaims above pass it.

**Deposit:** NOT deposited. There is no PAPER74 `.zenodo.json` and no publish script. I ran nothing that deposits.

**Naming:** no violation. "cold dark matter" appears once, as "it is never cold dark matter" (l.30). There is no "CDM-like".

**Grade: OVERSTATED.** The numbers are accurate. The framing claims derivation, completeness and a forced kappa where
the record says fitted, open, and (as of 11-12) withdrawn. It also omits the forest failure, FRZ1R, FRZ2 and DSB1.

## 2. DOORS.md (committed 0e2b0a5489; HEAD = origin/main for this file)

**Uncommitted diff:** adds one blockquote at the top ("Forward correction, 2026-11-12"). It recasts the file as a
historical inventory, says CLOSE-1_DT2 did land (growth gate fails; present-day settling unavailable), and says the
PIK1 linear invisibility, FINAL5 universal detectability and several kappa/gauge claims are superseded. It warns
against reading class-level impossibility from the counts and links `research_closure_2026_11_12/combined_route/CORRECTIONS.md`
(itself untracked). The body is unchanged.

**Counts** are internally consistent: 15+16+5+4 = 40, 7+12+2+0 = 21, 7+3+2+6 = 18, 7+3+1+3 = 14, total 93.

**Eighteen labels checked against each lane's RESULT.md head (committed bytes):** COL1 BREAKS DOWN, HE1 FAILS, MK2
(NO VALUE; as frozen NO VALUE / NO VERDICT), ONE1 PASSES at 1.6 R_h (A2 noted), SWT1 KEY-DEPENDENT / NOT A NO-GO,
FRZ1 FOREST ROW FAILS 9916/9009, FRZ1R FAILS 8142.08/7685.51, FRZ2 NO FRAMEWORK a0(z) PASSES, HLF1 NO VERDICT, EFN1
NO VERDICT every reading, DSB1 STOPPED AT KA-c / amended NO POWER, SRH1 WINDOW EMPTY gap 1.39/1.45, VSH1 NO VERDICT
(A1 SETTLES BY SHOCK), R541B TRADES, FINAL16, FINAL18, FINAL-14, FINAL-17. **Every label matches: 18/18.**
FRZ1, FRZ1R, FRZ2, EDG1, HLF1, EFN1, DSB1 and SRH1 are all present with the right labels.

**Bucket and staleness faults (the labels are right; the counting is not):**
- SWT1 is counted CLOSED inside "the switch class", but its own label is "NOT A NO-GO AS FROZEN" and DOORS's own row calls it an anti-closure.
- SCS1 (STABLE), SHP1 (a shape measurement) and KDE1 (ALREADY IN THE RECORD) are counted CLOSED, though none is a label from the definition's list.
- FINAL-7 is listed both in the closed medium block and in the 18 never landed. It now has a RESULT.md, so it is double-counted and stale.
- FINAL4 is counted CLOSED although it carries "TILT POST HOC, NOT EXCLUDED".
- CLOSE-1_DT2 is "no files at all" in the body, but its RESULT.md landed at 01:23 (86220a6717), 30 minutes after DOORS.md.
- PIK1 is closed in the body but now carries a correction that its universal NO VALUE is not established.

So "40 closed" is generous by at least 4-6 doors, and the 18 never-landed count is now at most 16.

## 3. Lean (built with `lake env lean`; the probe compiles, exit 0)

I appended `#print axioms` for every theorem (copies in scratch). Unless stated, each file below compiles at exit 0
with 0 errors, 0 `sorry` and 0 `sorryAx`, and uses only the axioms {propext, Classical.choice, Quot.sound}.
- H001 action: an algebraic core of the AeST f(X) with mu_2 (derivative and sign identities).
- H009 mimetic: the normalised-gauge algebra.
- H016 seesaw: **`seesaw_general` has the conclusion = the hypothesis (`:= h`)**. `seesaw_n2` and `zimmerman_scale_is_seesaw` only rearrange their hypothesis a0*2*MPl = Lambda^2.
- H017 n = 2: D(D-3)/2 = 2 forces D = 4 for D >= 3, which is true integer algebra. **`joint_relation` and `seesaw_from_polarizations` restate their hypothesis.** `scalar_excluded` is `1 != 2`.
- H018: `joint_relation_derived_n` restates its hypothesis after `norm_num`.
- H019 "THE CLOSURE": **a definitional unfolding**. With sqrt G * MPl = 1 and rho = Lambda^4 assumed, (1/2) sqrt(G Lambda^4) = Lambda^2/(2 MPl). It is presented as a physical identity of Zimmerman and the seesaw.
- H020 (G cancels; c H0/a0 = sqrt(32 pi/(3 Omega_L))), H034 (vacuum w = -1, separate conservation), H038 (attractor algebra): algebra only.
- H043: the exponents equal 1, 0 and 4 iff D = 4. The selectors are defined so that D = 4 is their root.
- H045 (f strictly monotone, so the zero crossing is unique), H046 (honest negative: health does not force n), H047 (k-essence sound speed).
- H061: compiles. **Its `scanPol_200` uses `native_decide`, which adds the non-standard axiom `native_decide.ax_1_1`.** `kappa_two` is `(2:R)^-1 = 1/2` by definition. The file carries its own retraction (l.40).
- FINAL-10 `Final10Stress.lean`: **does not compile**: exit 1, 34 error lines, and 27 theorems depend on `sorryAx` (error recovery). This matches its own FAIL record. Its intended content (`claimed_identity_false`: Pi_rr + Pi_tt != 0 for every u > 0) contradicts PAPER74 l.151.
- FINAL-11 `Final11Budget.lean`: the window x_b(5.41) is in (5.8887, 5.8889), plus the demand/budget ratios. Arithmetic.
- FINAL-14: X is monotone, X(x_b R) = R, the window, the ratios 3.87 / 7.67 / 11.00 / 18.08, and the gas column. It is pure real arithmetic on input constants (it says so).
- FINAL-13 has no Lean file (`audit_lean.py` only). `probe*.lean` in FINAL-10 are scratch files with no theorems.

**Mutation twins:** none exist in these folders (no `*_MUTATE.lean` for H0xx or FINAL-10/11/14). I made two:
FINAL-14 with the upper window bound set to 5.8888 fails (exit 1, type mismatch at l.196), and H017 with `n_pol 4 = 3`
fails (exit 1). Both bite. The paper's "each with a false twin" refers to fable52's files, not these.

## Can PAPER74 be relied on as written?

No. Its numbers trace: 10/10 spot checks, and the audit gate passes. Its claims do not. It calls form B's rules "complete as a
predictive theory", calls the form "derived", and presents kappa = 1/2 as forced by an exact symmetry. As of 11-12 the
lane record withdraws that symmetry: kappa is a physical coefficient and it is fitted. It never says that the
Lyman-alpha forest row fails on two independent builds (FRZ1, FRZ1R), that no a0(z) rescues it (FRZ2), or that
dwarfs have no power (DSB1). It hides ONE1's post hoc veto and its -2.7 sigma miss at the frozen veto. It calls an
asymptotic stress identity "exact", against FINAL-10. Its tSZ "no outcome in between" claim is superseded.

Before deposit: add a failing-rows section (forest FAILS per FRZ1 and FRZ1R, FRZ2, DSB1 NO POWER, HLF1 and EFN1 NO
VERDICT); rewrite the symmetry/forced-kappa section and the "complete" and "derived" lines to "kappa = 1/2 fitted";
state ONE1's A2 and the 1.0 R_h miss; fix "exactly" at l.151; bring in FINAL5's corrected forecast; commit AMT1's
AMOUNT_BUDGET.md and make the audit check origin/main only; restate the status as PAPER72 v1.1's: a form the record
closes on, not a pass.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
