# CFG942: ALMA scoring readiness for U4_27928 (public 2026-11-06) and GS4_24110 (public 2026-11-28)

The criteria were committed alone, first (556c36582).
- **Kind:** readiness only. No new physics, no data download, no archive query.
- **Settings:** κ = ½ FITTED; the two footings are never pooled; not theory closed. Nothing here says the data favour the framework.
- **Disclosure:** not blind. The plans, the AG5 scorer, CFG570/572/573 and the canonical files were read first.

## Verdict
- **U4_27928: READY.** Its harness runs the frozen plan in `CFG806_u4_27928_scoring/`:
  - R1 hashes, R2 reproduction, R3 transcription: all pass;
  - every required MOCK class is returned, C1 passes and MUTATE bites.
- **GS4_24110: READY**, for the frozen plan in `CFG809_gs4_24110_ci21_scoring/`, on the same terms.
- **The U4 criteria ARE committed and frozen.** Commit 1bf70683b (2026-10-15 20:28) holds that one file alone, made before any download, and its bytes equal the hash quoted in its ID notes (bc56aa71…). Two loose ends:
  - its header still reads "DRAFT, not yet committed" (stale; A-X5);
  - the lane has **no assigned ID**, so cite it by its directory name (A-X4).
- **READY covers the harness only. Three things outside it can still decide release day:**
  1. **Two frozen plans per target.** CFG806/CFG809 (10-15) and AG5's `FROZEN_SCORING.md` (7ea94d2ae, 10-20) disagree on the statistic, the detection threshold, the V_c method, the [CI] coefficient and the kill line (A-X1, A-X2). The owner must say which one governs.
  2. **Sensitivity.** CFG570's archive sensitivities predict a total-flux S/N well below 5 at native resolution for an extended disc carrying the required gas. Neither plan has a taper branch (A-U12, A-G14), so the likeliest outcome on both dates is "G1 FAIL, upper limit", unless the archive products are tapered or the data beat the metadata.
  3. **Power under the plans as frozen:**
     - GS4: the RIVAL SIDE cannot be reached for any gas mass;
     - GS4: the framework's verdict is NOT ROBUST for every CI21 value, because CFG572's public CO43 and dust routes already disagree;
     - U4: the plan separates the models only for V_c ≈ 220–260 km/s.

## 2026-10-21: clarifications implemented
The owner settled the ambiguities below before any data, in two files committed in 35ea5e1be:
- `CFG806_u4_27928_scoring/CLARIFICATION_2026-10-21.md`;
- `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21.md`.

The harness now implements the eight items listed here. Every other default is unchanged. Everything is still MOCK: no byte of either programme has been read.

**What changed**
| item | 10-20 harness | now |
|---|---|---|
| U4 A-U16 | V_c 1σ from the independent-pixel fit covariance; beam-corrected printed as "alt4" | the beam-corrected interval (covariance × √(pixels per beam)) is primary for TESTS NOTHING, PARTIAL, every Δ_m and every verdict; the independent-pixel interval is an information line (with the status it would give, if different) |
| U4 A-U1 | gap labelled "WITHIN 2sig_tot (unnamed by CFG806 s4)" | "not in tension (within 2σ_tot)"; never "consistent" |
| U4 A-U14 | radius-1″ and radius-2″ ratios printed, neither primary | the 20% flag uses the diameter-2″ (radius-1″) aperture and fires only after G1 passes; the radius-2″ ratio is printed as information |
| GS4 A-G9 | G3 used the covariance FWHM error | G3 uses that error × √(pixels per beam); the independent-pixel error is printed; the Gaussian-to-exponential size bias is printed as information (noiseless exponential disc at the measured R_g, axis ratio and beam); R_g is not corrected |
| GS4 A-G11 | +2000 km/s outside the spw → exit 2 | rerun at +1000, labelled "MUTATE fallback +1000 (CLARIFICATION A-G11)"; the exit code follows the fallback; exit 2 only if +1000 also leaves the window |
| GS4 A-G3 | an upper limit not in tension read "consistent with (one-sided)" | "not constrained"; in tension only if Δ_v = 0 lies more than 2σ_Δv outside the whole [f(0), f(UL)] (the test is unchanged); UL cells print the interval |
| GS4 A-G4 | ROBUST already decided per model (verified; unchanged) | the owner's sentence is printed once; a per-run check and a self-test scan of every branch are printed as information (see finding 1) |
| both | — | the clarification file and commit 35ea5e1be are printed; K1 gains two rows (both clarification files == 35ea5e1be); the harness sha256 is printed and recorded in every results JSON; release-day copy into the plan's dir (`cfg806_u4[_MUTATE].out/_results.json`, `cfg809_gs4[_MUTATE].out/_results.json`), made only with `--cube` and only if the cube's OBJECT is not MOCK |

New self-test checks:
- U4: A-U16 (V_c 205, ±3 independent / ±8 beam-corrected → PARTIAL), the A-U1 label, the copy step on temporary files.
- GS4: the A-G3 label, the copy step, the A-G4 scan, and A-G11 on two tiny temporary MOCK cubes:
  - coverage −1000..+1400 km/s: the fallback runs and bites (−3.7σ, exit 1);
  - coverage −1000..+1100 km/s: exit 2.

**Re-runs.** MOCK only, one process at a time, one thread, `nice -n 10`.
- The seven cubes were regenerated from their seeds into scratch. Each sha256 equals the 10-20 value listed under Files. Each cube was deleted after its run.
- Every output here was overwritten; the MUTATE outputs stay separate.
- K1 is 22/22 PASS and K5 PASS in every run. The self-tests all PASS.
- MUTATE:
  - U4 exits 1: G1 fails at +2000.
  - GS4 exits 1 at −25.9σ. +2000 lies inside this mock's coverage, so the line reads "MUTATE +2000 (as frozen)".
- The failed controls are kept and unchanged: U4-b C2 (rms 1.23×) and GS4-e C2.
- Peak RSS was at most 997 MB (U4-a). The true unique set size stayed at or below 145 MB.

**Which mock verdict lines moved: none.**

| run | 10-20 | 10-21 |
|---|---|---|
| U4-a primary | FRAMEWORK SIDE; F-DESI/F-flat "WITHIN 2sig_tot (unnamed)", R-H/L-fb IN TENSION | FRAMEWORK SIDE; F-DESI/F-flat "not in tension (within 2σ_tot)", R-H/L-fb IN TENSION |
| U4-b primary | RIVAL SIDE (alt footing NO SIDE) | the same |
| U4-c | TESTS NOTHING ×4 | the same |
| U4-d | G1 FAIL, log M_gas < 7.75, no kinematic test | the same |
| GS4-a primary | FRAMEWORK SIDE; G3 PASS | the same |
| GS4-b primary | NO SIDE; every model "consistent with (one-sided)" | NO SIDE; every model "not constrained" |
| GS4-e primary | F-DESI in tension, +0.90 ± 0.18 | the same |

**Numbers that changed, and why**
- **U4 V_c 1σ.** The printed interval is now the beam-corrected one:
  - U4-a: ±0.02–0.03 km/s (independent-pixel ±0.01);
  - U4-b: ±0.20–0.21 (±0.06–0.07);
  - U4-c: ±0.02 (±0.01).
- **U4 required ranges** widen with the V_c interval:
  - U4-a: by at most 0.01 dex.
  - U4-b: by up to 0.16 dex where R-H and L-fb are steep near 246 km/s (KMOS3D inclination, P-B):
    - R-H [8.53, 8.63] → [8.40, 8.71], eΔ 0.16 → 0.22;
    - L-fb [8.49, 8.59] → [8.33, 8.68], eΔ 0.16 → 0.23;
    - both stay IN TENSION (high gas), because the measured value is 9.44.
- **U4 power** (self-test R6): only the label changed (w2s → nit).
- **GS4 G3:** the FWHM error reads ±0.0006″ in GS4-a (was printed as ±0.000), and G3 still passes. Size-bias information: 0.696 (GS4-a) and 0.697 (GS4-e), against the MOCK truth of 0.694.
- **GS4 power:** upper-limit cells changed from C to nc.
- **Unchanged:** every measured flux, S/N, V_c, Δ_m, Δ_v, σ_Δv and FLOOR flag. Peak-memory figures vary from run to run.

**Findings for the owner (reported, not decided)**

Findings 1, 2 and 4 were acted on later the same day by addendum A; see "Addendum A implemented" below. Finding 3 stands.

1. **The A-G4 sentence holds on only one of the eight branches**: canonical, M★ 10.89, R_g = R_d. That is the only branch the 10-20 scan covered.
   - The self-test scan covers all eight M★ × shape × footing branches at V_c 206, with CI21 from 8.0 to 11.8.
   - On 6 branches that are not FLOOR (all of M★ 10.76, and M★ 10.89 with R_g = 1.5 R_d), F-DESI and/or F-flat read ROBUST at 15–17 of the 20 CI21 values: CI21, CO43 and dust give the same wording.
   - On the alternate footing at M★ 10.89 (both shapes), F-flat's FLOOR tension is ROBUST at every CI21 value.
   - GS4-a: 44 of 72 framework CI21 rows are ROBUST, 23 of them not FLOOR. GS4-e: 21 rows, all FLOOR. On the primary cut, only F-flat (alt, M★ 10.89, FLOOR) is ROBUST.
   - So two sentences are not borne out on every branch: "this disc can neither support nor disfavour the framework", and "only the rivals' FLOOR tension can come out ROBUST".
   - The harness prints the sentence as instructed, with the check beside it. The per-model ROBUST rule is unchanged.
2. **Clarification items outside these eight changes.** The harness does not yet do them:
   - A-X3: CFG571's Δ_m on M_bar is not printed.
   - A-U4/A-U17: a failed C2 does not print the ~10% MOCK false-failure rate beside it.
   - A-G1: σ_Δv with CFG572's ±0.1 dex M★ term is not printed.
   - A-G16: after a G1 failure, the continuum is measured in the noise-selected ≥ 2σ [CI] mask whenever that mask is not empty (GS4-b: 23 px, peak S/N 6.9), not in the R_e circle. The A-G6 flag text says "R_e circle if no [CI] detection".
   - A-G4 "the other CFG572 branches are printed": their masses are on the routes line and their rows are in the JSON. The score table shows only r41 0.37 and α_CO 4.36.
3. **A-G11 on a centred spw.** A 1.875 GHz spw centred on 270.0 GHz covers about ±1040 km/s.
   - The +1000 window (true-frame +700..+1300 km/s) is then not fully covered either, so the fallback also exits 2 there.
   - The fallback helps only if the spw is offset to higher velocity, or wider. The record holds no spw edges.
   - "Leaves the window" is implemented as "the shifted ±300 km/s window is not fully covered", the same test as for +2000.
4. **MUTATE continuum (an observation, not from the clarifications).** For the shifted window, the continuum is the median of channels with |v| > 600 in the shifted frame, and these include the true line.
   - Part of GS4-a's −25.9σ, and of the tiny cube's −3.7σ, is this over-subtraction.
   - The control still bites as frozen.

### Addendum A implemented (748dd8095, later on 10-21)
The owner's `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_A.md` withdraws the A-G4 sentence (§1), adds a MUTATE continuum reading (§2), and lists items the harness still had to print (§3). It is implemented here, MOCK only, with the same rules. All seven cubes were regenerated bit-identical, then deleted, and every self-test, mock and MUTATE run was repeated one at a time.

**Before → after** (826ebb739 → this commit)
| item | before | after |
|---|---|---|
| A-G4 header (§1) | the withdrawn sentence | addendum §1's per-branch statement, with the scan behind it: 7 of 8 M★ × shape × footing branches CAN return a ROBUST framework verdict; only canonical, M★ 10.89, R_g = R_d CANNOT. This agrees with the addendum (new self-test check, PASS). On the 6 non-FLOOR branches the ROBUST wording is "consistent with" (15–17 of 20 CI21 values); on alt M★ 10.89 it is F-flat's FLOOR tension (20 of 20). |
| GS4 MUTATE (§2) | −25.89σ: 120 continuum channels, true line included | +2.90σ: 60 channels, true line (±600 km/s of z 1.9975) excluded. Still below 3σ, so it bites (exit 1). The old reading is printed as information. |
| GS4 tiny-cube fallback | −3.7σ, exit 1; second cube exit 2 | −0.1σ, exit 1; exit 2 now says "this run has NO MUTATE control" |
| U4 MUTATE | true line in the continuum | checked first, then excluded: the 2 R_e circle at the target in the +2000 window reads −16.0σ with the true-line channels in the continuum and −1.8σ without them. Selection-aware G1 S/N −2.6 → −0.3 (fails, so the control bites, exit 1). The check is printed in every U4 MUTATE run. |
| A-G1 (§3) | not printed | an information line under each CI21 row. With CFG572's ±0.1 dex, the Δ_v-alone wording of FLOOR models becomes "in tension" in 43 of 144 CI21 rows (GS4-a) and 6 of 32 (GS4-b). Verdicts keep the plan's 0.2 dex. |
| A-G16 (§3) | GS4-b continuum in the 23-px noise mask: peak S/N 6.9, 7.4 µJy | R_e circle: peak S/N 22.9, 473.9 µJy (the mock continuum is 478 µJy) |
| A-G4 rows (§3) | primary and the two ROBUST routes only | every other branch (CO43 r41 0.25 / 0.55, CI10 limits, dust Scoville, CI21 X_CI 3.0e-5) as "(information)" rows; they never enter ROBUST or the side |
| A-X3 (§3, U4) | not printed | CFG571's Δ_m on M_bar per footing on the primary cut: log of the spherical-equivalent V_bar²R/G, measured − required, at CFG571's 2R_e. U4-a, canonical: F-DESI −0.00 ± 0.05, F-flat +0.00, R-H +0.14, L-fb +0.10 |
| A-U17 (§3, U4) | not printed | beside U4-b's C2 failure: "about 10% (MOCK); Gaussian estimate at N_independent 33: 11%"; §5 unchanged |
| K1 | 22 rows | 23 rows: the addendum == 748dd8095; 23/23 PASS in every run |
| memory | peak RSS 997 MiB (U4-a) | at most 457 MB in every run; cube generation about 190–230 MB |

**Memory fix.**
- **Cause:** the macOS malloc medium zone keeps freed 32 KB–8 MB blocks resident. The thin-disc fit allocates such temporaries hundreds of times, so resident size grew about 2.6 MB per model evaluation while Python's traced peak stayed at about 100 MB.
- **Fix:** each harness re-executes itself once at start with `MallocMediumZone=0` (same process id). With it, the first fit stays at about 290 MB; without it, about 760 MB.
- **What it does not change:** the mock cubes stay bit-identical and the fit numbers are identical (e.g. U4-a V_f 257.4, nfev 90, χ²/N 1.203).

**Verdict lines moved: none.** The primary-route and ROBUST-route lines of all seven mocks are identical to 826ebb739 after whitespace normalisation, and so are the U4 class lines and sides.

**New findings for the owner (reported, not decided)**
1. **The GS4 MUTATE under addendum §2 bites only narrowly: +2.90σ against the 3σ line.** The residual is not line emission:
   - The run's selection check splits the shifted flux in the true-run mask into the raw shifted window (+0.57σ) and the continuum term (+2.32σ). In the 8 ring copies, which are not selected on the data, the continuum term is −0.13 ± 0.65σ.
   - Cause: the true-run mask is chosen where (true window − its continuum) ≥ 2σ, which favours pixels whose continuum noise is low. The shifted continuum reuses 60 of those continuum channels, so subtracting it biases the masked sum upward.
   - On real data the control could therefore fail to bite (exit 0) with no line in the shifted window.
   - The bite rule is unchanged here. Possible rulings are a continuum disjoint from the true-run continuum's channels, or a selection-aware null as in G1.
2. **U4's MUTATE bite now rests on A-U13.** With the over-subtraction removed, the literal translated-mask S/N in the shifted window reads 8.6, a false pass on noise like U4-d's 9.5. The selection-aware S/N (−0.3) decides, as A-U13 says.
3. **The U4 exclusion follows CFG809 addendum A §2's reasoning, applied by instruction after the check above.** CFG806's own text (and its clarification's A-U3: "the median of channels with |v| > 600 km/s") does not state it, so the owner may wish to confirm it for CFG806.

### Addendum B implemented (CFG809 addendum B and CFG806 addendum A, d7a1afae1)
The owner ruled on new finding 1 above:
- `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_B.md`: the GS4 MUTATE is scored against a selection-aware null. At 200 off-source seeds, masks are grown by the true run's procedure and their flux is taken in the shifted window with the addendum-A continuum. The control bites if (flux − null mean)/null sd < 3.
- `CFG806_u4_27928_scoring/CLARIFICATION_2026-10-21_ADDENDUM_A.md`: U4's MUTATE continuum excludes ±600 km/s of the true line, and G1's selection-aware S/N decides.

Implemented here, MOCK only, with the same rules. The self-tests, all seven mocks (regenerated bit-identical, then deleted) and both MUTATE runs were repeated one at a time.

**Before → after** (90bdb0153 → this commit)
| item | before | after |
|---|---|---|
| GS4 MUTATE statistic | flux / ring rms of translated copies of the true-run mask = +2.90σ, bites (exit 1) | (flux − null mean)/null sd = **+151.67**, does **NOT** bite (exit 0). The null comes from 200 seeds on the true-window map (the same seeds as G1's null), measured in the shifted window: mean 0.000001, sd 0.000001 Jy km/s. The old statistic, the split and the 10-21 reading are printed as information. |
| GS4 tiny-cube fallback (self-test) | −0.1σ, exit 1 | statistic −0.90, bites, exit 1 (mask 35 px). The check now tests the A-G11 logic: the fallback runs, is labelled, and the exit code follows it. |
| U4 MUTATE | G1 selection-aware S/N −0.3, bites | the same, −0.30, bites (exit 1). A continuum-selection check is printed (see below). The MUTATE continuum is now owned by CFG806 addendum A, no longer "by instruction". |
| K1 | 23 rows | 25 rows: CFG809 addendum B and CFG806 addendum A == d7a1afae1; 25/25 PASS in every run |
| memory | at most 457 MB | at most 449 MB |

**Verdict lines moved: none.** The scoring of every mock is unchanged; only the GS4 MUTATE outcome changed.

**U4: does the same null show the continuum-selection bias?**
- **Yes, and the null carries it.** In the shifted window, the continuum term of the 31-px target mask is +0.000031 Jy km/s. That is +7.9 sd above 8 unselected ring copies (−0.000000 ± 0.000004): the ≥ 2σ selection prefers low-continuum pixels, which is the addendum-B bias.
- The G1-procedure null masks show the same term (+0.000035 ± 0.000011); the target sits at −0.31 null sd.
- U4's MUTATE grows its mask and its null on the same shifted map. So G1's selection-aware S/N is itself addendum B's null-calibrated statistic: the two coincide (−0.30), and it decides.

**Finding for the owner (reported, not decided): under addendum B the GS4 MUTATE does not bite on MOCK GS4-a.**
- The statistic is +151.67, yet no line is in the shifted window: the raw shifted window is +0.57σ in ring units.
- **Scale mismatch:**
  - The true-run mask of this bright mock (S/N 1087) has 18,083 px.
  - The null masks, grown from noise at off-source seeds, have a median of 20 px (max 48).
  - The null's sd (0.000001) is therefore about 40× smaller than the noise of the true-run mask's flux (ring rms 0.00004), and the small selection bias left in the big mask is measured against it.
- The mismatch shrinks as the source's mask approaches noise size; on the tiny cube (35 px) the control bites at −0.90.
- On real data a well-detected [CI] line would give a large mask, and the control could fail exactly as here.
- The harness implements the ruling literally and prints the mask sizes beside the statistic. Possible rulings are not decided here; for example, a null whose masks match the true-run mask in size.

### Addendum C implemented (CFG809 addendum C, 785fcae44)
Addendum C withdraws addendum B's noise-grown null and rules an injection null that matches the mask's size and selection:
1. at 200 off-source positions, inject a copy of the true run's beam-convolved moment-0 model (same line profile, same flux);
2. regrow the mask by the true run's procedure;
3. measure its shifted-window flux with the addendum-A continuum.

The control bites if (true-run shifted flux − null mean)/null sd < 3. Implemented here, MOCK only. The GS4 self-test, GS4-a/b/e and the GS4 MUTATE were rerun one at a time. U4 was rerun too, because the shared K1 list gained a row; its logic is unchanged.

**Implementation.**
- **Model:** the injected model is the run's beam-convolved Gaussian fitted to the true-window moment-0 (plan §3.2), with its fitted flux.
- **Moment-0 injection:** the injection is done on moment-0 maps. This is exact when the line profile lies in channels excluded from both continua and outside the shifted window, so that the injected line changes only the true-window moment-0. The run measures the true-run profile's fractions and prints them: GS4-a 0.003 beyond 600 km/s and 0.002 in the shifted window, i.e. zero within noise.
- **Copies:**
  - Copies sit on a 26″ crop (clipped at the cube edge), at least 2 r_mask + 0.5″ from the target and r_mask + 0.3″ from the edge, with the true source blanked.
  - σ is recomputed per copy.
  - The 200 positions are seeded and the same for every model.

**Before → after** (9dcfc3ce4 → this commit)
| item | before (addendum B) | after (addendum C) |
|---|---|---|
| GS4 MUTATE statistic | +151.67, does not bite (exit 0); null masks median 20 px | **+3.36, does not bite (exit 0)**. Null mean 0.000009, sd 0.000031 Jy km/s. Injected-copy masks median 8,828 px (16–84%: 8,768–8,883) against the true run's 18,083. |
| information lines | addendum-A +2.90σ; split | addendum B's +151.67 (withdrawn), addendum-A +2.90σ, the 10-21 reading −25.89σ, and the split are kept. New: the same injection null with the §3.4 thin-disc model gives **+2.35 (would bite)**, with masks median 18,073 px. |
| GS4 tiny-cube fallback | B statistic −0.90, bites | C statistic −0.01, bites (true mask 35 px, copies median 30 px) |
| K1 | 25 rows | 26 rows: addendum C == 785fcae44; 26/26 PASS in every run |
| U4 | G1 selection-aware S/N −0.30, bites | unchanged, −0.30, bites |

**Verdict lines moved: none.** All seven mocks' scoring lines and sides are identical to 9dcfc3ce4.

**Findings for the owner (reported, not decided)**
1. **The injection null depends on which model is injected, and with the run's moment-0 model it does not match the mask.**
   - The true run's beam-convolved moment-0 model is the §3.2 Gaussian.
   - Fitted to the exponential [CI] disc, it has weaker wings and less flux (0.0395 against 0.0489 Jy km/s). Its copies grow masks half the true size (8,828 against 18,083 px) and recover 0.0391 against 0.0471 Jy km/s. This is the A-G9 Gaussian-to-exponential bias.
   - So it matches neither the size nor the near-threshold selection: the copies' mean is 0.000009, while the true mask's continuum term is +0.00009. The statistic is +3.36 (no bite).
   - The run's other beam-convolved model is the §3.4 thin-disc cube model: an exponential disc with the line profile, fitted only when G4 passes. It matches (18,073 px; 0.04716 Jy km/s) and gives +2.35 (would bite).
   - Addendum C does not say which model is meant, and the thin-disc model does not exist when G4 fails.
2. **The null values are correlated.** The off-source area of this cube holds about 15 non-overlapping copies of an 18,083-px mask, so the 200 positions overlap. The null mean and sd rest on about 15 independent samples; the sd alone is uncertain by roughly ±20%, i.e. about ±0.5 on the statistic.
3. **Even with the size-matched model, GS4-a sits at +2.35**, about 0.65 below the bite line. A real cube's control may land on either side of 3 by chance.
4. **Stale cross-reference.** CFG806 addendum A (U4) still points to "CFG809 addendum B", which addendum C withdrew for GS4. U4's decision is unaffected (G1's selection-aware S/N, masks grown on the shifted map; −0.30), but the reference is now stale.

### Addendum D implemented (CFG809 addendum D, c2dfb62b5): MUTATE re-runs G1 in the shifted window
Addendum D drops every reused-mask statistic. Addenda B and C scored the true run's mask, which was selected on the true window; B's null had the wrong scale and C's depended on the injected model.

The GS4 MUTATE now re-runs G1 in the shifted window, exactly as CFG806-U4 does:
- a fresh ≥ 2σ mask grown at the shifted window;
- the addendum-A continuum (true-line channels excluded);
- the S/N against A-G13's selection-aware null (200 off-source seeds).

The control bites if that S/N is below 3. The A, B and C statistics and the mask sizes are printed as information.

The U4 output wording now cites addendum D instead of the superseded addendum-B sentence. U4's logic is unchanged.

The GS4 self-test, GS4-a/b/e and the GS4 MUTATE were rerun one at a time, together with the full U4 set (the shared K1 list changed).

**Before → after** (88db01f47 → this commit)
| item | before (addendum C) | after (addendum D) |
|---|---|---|
| GS4 MUTATE | injection-null statistic +3.36 on the reused 18,083-px mask, does not bite (exit 0) | G1 re-run in the shifted window: fresh mask 23 px, selection-aware S/N **+0.29**, null mean 0.0000057, sd 0.0000024 Jy km/s; **bites (exit 1)**. The literal ring S/N reads 11.0, a false pass on noise like G1's (A-G13), and never decides. |
| information lines | B +151.67, A +2.90σ, thin-disc C +2.35 | the same, plus C with the Gaussian (+3.36) and the mask sizes: fresh 23 px; true-run 18,083; C copies 8,828 (Gaussian) and 18,073 (thin disc); B null masks 20 |
| GS4 tiny-cube fallback | C statistic −0.01, bites | addendum-D S/N −0.09, bites, exit 1 (fresh mask 1 px); the exit-2 case is unchanged |
| U4 MUTATE | G1 selection-aware S/N −0.30, bites | unchanged (−0.30, bites); the wording now cites addendum D |
| K1 | 26 rows | 27 rows: addendum D == c2dfb62b5; 27/27 PASS in every run |
| memory | at most 362 MB | at most 417 MB |

**Verdict lines moved: none.** All seven mocks' scoring lines and sides are identical to 88db01f47.

**What remains open (reported, not decided)**
- **Both MUTATE bites now rest on A-G13 / A-U13.** In the shifted window, the literal S/N passes on pure noise (GS4 11.0, U4 8.6), and only the selection-aware S/N bites. This is consistent with both clarifications, but on release day the literal reading must not be quoted as the control.
- **No GS4 MUTATE control is possible on a centred spw (finding 3 of 10-21 stands).** If the 1.875 GHz spw is centred on 270 GHz, even the +1000 fallback leaves the window, and the run then has no MUTATE control (addendum A §2). The record holds no spw edges to check this.

**Nothing frozen was edited.** These files are unchanged:
- both plans' FROZEN_CRITERIA.md, both CLARIFICATION files, CFG809 addenda A–D, and CFG806 addendum A;
- `cfg571_prereg.py` and its seal JSON;
- LEDGER.md, the THEORY_CANONICAL files and CFG572.

K1 (27/27) and K5 checked this in every run, and git status is clean for those paths. No file was written into the plan directories: the copy step runs only for a real cube.

## Hash verification (K1 in every run; all PASS)
| file | sha256 (prefix) | equals freezing commit |
|---|---|---|
| CFG571 `cfg571_prereg_results.json` | be27457d… = `PREDICTIONS_HASH.txt` | 259f7825c |
| CFG571 `FROZEN_CRITERIA.md` / `cfg571_prereg.py` / `README.md` / `PREDICTIONS_HASH.txt` | 0f7646c8… / d721770d… / 3fc38b1e… / 639431d5… | 5f68a68c3 / 259f7825c ×3 |
| `CFG44_fluid_target/Bcommon.py` (ν_mono) | 7cfd9c69… | 259f7825c (last changed 513ee4b28, before the seal) |
| U4 plan `CFG806_u4_27928_scoring/FROZEN_CRITERIA.md` | bc56aa71… = value in both ID notes | 1bf70683b |
| U4 ID notes 10-15 / 10-15b | 5eb91102… / 3027f752… | 79321a577 / 38c7bc24d |
| GS4 plan `CFG809_gs4_24110_ci21_scoring/FROZEN_CRITERIA.md` | 8b439f19… | 966d50a87 |
| CFG572 `cfg572_gas_results.json` (public routes re-quoted) | b46276fb… | 12779c1e5 |
| CFG775 `SEALED_BH_BRANCH.json` / CFG778 `SEALED_EVENT_HORIZON.json` | 3d236378… / b9f3e827… (= their READMEs) | 8a7634027 / aac6ddd23 |
| THEORY_CANONICAL_2026-10-14.md | 30aa143e… (= its .sha256) | b7356ac57 |
| AG5 `FROZEN_SCORING.md` / `score_alma.py` (recorded only, not used) | b7f489bf… / ca6e0a2e… | 7ea94d2ae / c4bfd82fd |
| `CFG806_u4_27928_scoring/CLARIFICATION_2026-10-21.md` / `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21.md` (K1 rows added 10-21) | 5d2fbcea… / ba573d73… | 35ea5e1be |
| `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_A.md` (K1 row added 10-21) | 50e3e5be… | 748dd8095 |
| `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_B.md` / `CFG806_u4_27928_scoring/CLARIFICATION_2026-10-21_ADDENDUM_A.md` (K1 rows added 10-21) | 6ba6bd2f… / feacc7c9… | d7a1afae1 |
| `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_C.md` (K1 row added 10-21) | 44a439ff… | 785fcae44 |
| `CFG809_gs4_24110_ci21_scoring/CLARIFICATION_2026-10-21_ADDENDUM_D.md` (K1 row added 10-21) | 4bd73cf5… | c2dfb62b5 |

**Seal reproduction and transcription:**
- CFG571's own functions reproduce all 56 U4 and 16 GS4 sealed entries to 0.0 dex, with the FLOOR flags identical. The functions are executed from the text above the script's `# ---- controls ----` line; a plain `import` would rewrite the seal file and exit (A-X6).
- The plan tables match the seal: CFG806 §2 to 0.0048 dex across 9 rows, CFG809 §2 to 0.0044 dex across 4 rows.
- K5: no frozen file changed in any run.

## Inventory
### U4_27928
**Prediction.** CFG571, 259f7825c, be27457d…. It is conditional on the CO V_c at 2R_e = 8.271 kpc:
- below 200 km/s every model is FLOOR;
- at 225 km/s the framework needs log M_gas 9.19–9.95 and both rivals are FLOOR (CFG806 §2 table; the table governs over the README's "9.2–9.8").

**Rule.** CFG806-dir criteria (1bf70683b):
- G1: S/N ≥ 5 in a ≥ 2σ moment-0 mask, centroid within 0.5″, z within 0.002 of 1.4193;
- 3.1: thin-disc arctan fit; inclination primary from the CO moment-0 q (q0 0.2), branch from KMOS3D q 0.556; pressure P-B / P0;
- G2: emission must reach 6 kpc;
- 3.3: α_CO 4.36 / 1.0 with r21 0.77;
- §4: Δ_m on gas mass, σ_tot, TESTS NOTHING / PARTIAL / FLOOR;
- controls C1–C4 and MUTATE.

**Products expected.** ALMA 2024.1.00100.L (CONDOR), CO(2-1) in Band 3 at 95.290 GHz, 0.066″, 22680 s, 0.4393 mJy/beam at 10 km/s (CFG570 metadata, not re-verified):
- the archive's imaged cube, a pipeline `*.cube.I.pbcor.fits` of the spw covering 95.29 GHz;
- if no cube is provided, CASA tclean (a departure).

The record holds no MOUS UID; CFG570 kept none.

**Code.**
- `cfg942_u4.py` (this lane): FITS cube → G1/G2 → V_c branches → gas → CFG806 §4 classes. It also scores a measured-quantities JSON.
- AG5 `score_alma.py` scores AG5's own plan, not CFG806's.

**Missing.** The data, the MOUS UID, and the owner's choice between the plans.

### GS4_24110
**Prediction.** CFG571, required log M_gas inside R_e at V_c 206:

| | M★ 10.89, R_g = R_d / 1.5 R_d | M★ 10.76 |
|---|---|---|
| F-DESI, canon | 9.82 / 10.09 | 10.43 / 10.69 |
| F-flat, canon | 9.46 / 9.73 | 10.36 / 10.63 |
| F-DESI, alt | 9.11 / 9.38 | 10.33 / 10.60 |
| F-flat, alt | FLOOR | 10.24 / 10.51 |

R-H and L-fb are FLOOR in every branch.

**Rule.** CFG809 criteria (966d50a87):
- G1: [CI](2-1) S/N ≥ 5, ±300 km/s window, ring noise;
- 3.1: continuum; 3.2: gas size and G3;
- 3.3: CI21 mass (4.566e-4, T_ex 25 K, X_CI 1.9e-5 / 3.0e-5), with CFG572's CO43, CI10 and dust routes re-quoted;
- 3.4: G4 and a [CI] V_c branch;
- §4: Δ_v, the FLOOR rule, ROBUST / NOT ROBUST;
- controls C1–C5 and MUTATE.

**Products expected.** ALMA 2025.1.01377.L (HIDING in the HUDF), [CI](2-1) in Band 6 at 270.006 GHz, 0.089″, 13941 s, 0.5183 mJy/beam at 10 km/s:
- the archive's imaged cube of the spw covering 270.0 GHz (`*.cube.I.pbcor.fits`);
- the continuum image (pipeline `*.cont.I.tt0.pbcor.fits` or `*.mfs.I.pbcor.fits`);
- if missing, tclean (a departure).

No MOUS UID is in the record. The plan is a large-programme mosaic, so the noise may vary across the field.

**Code.** `cfg942_gs4.py` (this lane). AG5 scores AG5's plan.

**Missing.** The data, the MOUS UID, and the plan choice.

The frozen predictions are CFG571's four models as sealed. The CFG689 native a0(z) band folded into THEORY_CANONICAL_2026-10-18 does not change them, and no score uses it: at z 1.42 and 2.0 that band brackets both F-flat (1.0) and F-DESI (0.94 / 0.87), and the rival a0 ∝ H(z) lies outside it.

## Mock dry-runs
All inputs are MOCK. The harness generates them (seeded), they are read back from FITS like real data, and they are never committed. Their noise is chosen for clean detections and is NOT the archive sensitivity.

The table records the 10-20 runs. On 10-21 every run was repeated under the clarifications, and every class held; only the wording changed (see "2026-10-21: clarifications implemented").

| run | truth | class returned | required |
|---|---|---|---|
| U4-a | V_c(P-B) 250, gas = F-DESI's need (10.42) | G1 and G2 PASS; V_c 250.2 recovered; canonical primary FRAMEWORK SIDE (alt footing FRAMEWORK SIDE) | PASS |
| U4-b | V_c 250, gas = R-H's need (9.50) | canonical primary RIVAL SIDE (alt footing NO SIDE, as expected: R-H is FLOOR there) | PASS |
| U4-c | V_c(P-B) 165 | TESTS NOTHING in all four (inclination × pressure) branches | PASS |
| U4-d | zero line flux | G1 FAIL, upper limit, no kinematic test (the literal translated-mask S/N is 9.5 = a false pass; see A-U13) | PASS |
| U4 MUTATE | U4-a, +2000 km/s | G1 FAIL, exit 1 | PASS |
| U4 C1 | injections at 200 and 250 km/s | V_c 200.2 / 250.3, flux 0.97–0.98 | PASS |
| U4 MOCK-JSON | PARTIAL (200 ± 10); G2 fail (4.2 kpc); FLOOR at 212 km/s | PARTIAL; RADIUS NOT REACHED; IN TENSION (FLOOR) | PASS |
| GS4-a | gas = F-DESI's need (9.82) | G1 PASS; F-DESI and F-flat consistent; R-H and L-fb in tension (FLOOR) → FRAMEWORK SIDE; G3 PASS; G4 PASS; [CI] V_c 205.8 | PASS |
| GS4-b | zero gas | G1 FAIL (literal ring S/N 10.6 = a false pass); every model "consistent (one-sided)" → NO SIDE | PASS |
| GS4-e | gas 10^11.6 | F-DESI in tension (+0.90 ± 0.18) | PASS |
| GS4 MUTATE | GS4-a, +2000 km/s | −25.9σ in the true mask, exit 1 | PASS |
| GS4 C1 | 9.82 at FWHM 0.8″, 10″ away | flux 0.997, size 1.000 | PASS |
| GS4 ROBUST scan | CI21 8.0–11.8 | both ROBUST and NOT ROBUST returned | PASS |

**Failed controls, kept:**
- **U4-b C2:** the rms is 1.23× the analytic noise with 33 independent apertures, a ~2σ statistical excursion (A-U17).
- **GS4-e C2:** the 10^11.6 mask is about 4″ across, so the translated apertures hit the source and the box edge.

Both runs are NOT DIAGNOSTIC as frozen; their required classes still returned. Memory: peak resident size stayed under 1 GB in every run. It counts freed pages that macOS keeps resident; the true unique size peaked at 176 MB.

## Information outputs
**Power, U4** (`cfg942_u4_selftest.out` R6; σ_rms 0.05 dex, V_c ± 5 km/s; canonical, P-B, R_g = R_d):
- gas equal to F-DESI's need reads FRAMEWORK SIDE at 220–250 km/s and NO SIDE from 260 km/s up;
- gas equal to R-H's need reads RIVAL SIDE only at 250–260 km/s.

The KMOS3D integrated Hα σ of 224.5 km/s hints that V_c may lie above CFG571's 300 km/s grid. The harness computes any V_c with the frozen functions.

**Power, GS4** (R6):
- detected gas reads FRAMEWORK SIDE for log M_gas ≤ 10.8 (R-H in tension through the FLOOR rule), and NO SIDE at ≥ 11.2;
- upper limits read NO SIDE;
- the RIVAL SIDE is never reached;
- even a perfect zero-gas limit leaves F-DESI consistent, because the 0.2 dex stellar systematic dominates σ_Δv.

**Sensitivity** (R7; extended exponential disc, aperture noise from the archive line sensitivity):

| case | U4 log M_gas (CO, 1″ aperture) | S/N | GS4 log M_gas ([CI], R_e aperture) | S/N |
|---|---|---|---|---|
| F-DESI need | 10.42–10.86 | 0.2–0.5 | 9.82 / 10.43 | 0.04 / 0.15 |
| all flux in one beam | (same) | 5–14 | (same) | 1.2 / 4.9 |
| CO43 route, compact 0.3″ | — | — | 10.95 | 2.9 |

## Release-day checklist
Run everything from `campaign_fresh_gravity/CFG942_alma_scoring_readiness/`.

**Environment:** `OMP_NUM_THREADS=1 nice -n 10`, one process at a time. On macOS each harness re-executes itself once with `MallocMediumZone=0`, which keeps the peak RSS under 0.5 GB on the mocks; the header prints "memory guard".

**U4_27928 (2026-11-06):**
1. `python3 -B cfg942_u4.py --selftest`: all K1 checks must PASS. A mismatch stops the run (exit 2).
2. **Owner's yes:** the archive query and the download need the owner's go, with file names and sizes stated (CFG806 §1).
   - Query project 2024.1.00100.L near RA 34.423191, Dec −5.182924, for the spw covering 95.29 GHz.
   - Take its pipeline `member.uid___A001_…_sci.spw<N>.cube.I.pbcor.fits` (+ `.pb`).
   - Record the sha256.
3. `python3 -B cfg942_u4.py --cube <cube.pbcor.fits>` writes `cfg942_u4_RELEASE.out/json`. It runs G1, G2, the fits, C1, C2, C3 and the score; a failed control prints NOT DIAGNOSTIC.
   - For a real cube (OBJECT not MOCK) the same two files are also written, byte-identical, into the plan's dir as `CFG806_u4_27928_scoring/cfg806_u4.out` / `cfg806_u4_results.json` (CLARIFICATION A-X7).
   - The results JSON records the harness sha256.
4. `python3 -B cfg942_u4.py --cube <cube.pbcor.fits> --mutate` must exit 1. Its copies are `cfg806_u4_MUTATE.out` / `cfg806_u4_MUTATE_results.json`.
5. Commit the outputs, including the plan-dir copies. Never commit the cube or a home path. Delete the cube, and add departures to a dated README note. The orchestrator writes the ledger row.

**GS4_24110 (2026-11-28):** the same steps, with:
- `python3 -B cfg942_gs4.py --cube <CI21 cube> --cont <continuum image>`, then `--mutate`.
  - The copies are `CFG809_gs4_24110_ci21_scoring/cfg809_gs4[_MUTATE].out` / `_results.json`.
  - MUTATE exits 1 when the control bites.
  - If +2000 km/s leaves the spw, MUTATE reruns at +1000, labelled "MUTATE fallback +1000 (CLARIFICATION A-G11)", and exits by that run. It exits 2 only if +1000 also leaves the spw; that run then has no MUTATE control (addendum A §2).
  - The shifted window's continuum excludes channels within ±600 km/s of the true line (addendum A §2).
  - MUTATE re-runs G1 in the shifted window (addendum D): a fresh ≥ 2σ mask, the addendum-A continuum, and the selection-aware S/N, which bites below 3. MOCK GS4-a reads +0.29 and bites. The A, B and C statistics are information only. See "Addendum D implemented".
  - U4's MUTATE uses the same continuum exclusion (CFG806 addendum A), and G1's selection-aware S/N decides.
- The spw must cover 270.006 GHz. The harness reads FREQ cubes, 3D or 4D, with BMAJ keywords or a per-plane BEAMS table.

## Ambiguities that could cause a release-day dispute
Each one is flagged in the outputs. None is resolved by editing a frozen file; the harness's default is stated in each line.

The list is kept as written on 10-20. The owner resolved it on 10-21 (35ea5e1be). The items that changed the harness are listed under "2026-10-21: clarifications implemented"; the stale lines are A-U1, A-U14, A-U16, A-G3, A-G9 and A-G11.

**Cross-plan**
- **A-X1 Two frozen plans per target.** CFG806/809 differ from AG5 (7ea94d2ae) in:
  - the statistic: gas Δ_m with a double floor (U4), and Δ_v with 0.2 + 0.2 dex systematics (GS4), against AG5's total-baryon Δ with a 0.15 floor;
  - the detection threshold: 5σ in a ≥ 2σ mask, against 3σ by curve of growth;
  - the U4 V_c: a thin-disc fit against a PV cut;
  - the [CI] coefficient: 4.566e-4 against 4.556e-4;
  - the T_ex branches, and the robustness rule against AG5's TRACER-LIMITED rule;
  - the kill line: none against the canonical §2 kill line.
- **A-X2 Kill line.** THEORY_CANONICAL_2026-10-14 §2 lists a kill condition for both ALMA dates. CFG571, 806 and 809, and the 10-21 DRAFT canonical, say one disc = demonstration, no exclusion.
- **A-X3 Three single-disc statistics:** CFG571's criteria use Δ_m on M_bar, CFG806 Δ_m on M_gas, CFG809 Δ_v.
- **A-X4 IDs.**
  - The U4 lane has no ID.
  - "CFG809" names two directories and two LEDGER rows.
  - CFG809's text calls the U4 lane "CFG808", which is now CFG808_expelled_gas_free.
- **A-X5 Stale headers.** Both plans' headers say "DRAFT, not yet committed", but both were committed alone before any download.
- **A-X6 "Imports cfg571_prereg.py read-only".** A plain import runs the script, rewrites the seal JSON (the same bytes only if the numerical stack reproduces) and calls sys.exit. The harness executes only the head.
- **A-X7 Script location.** The plans name `cfg806_u4.py` / `cfg809_gs4.py` in their own directories. Those scripts do not exist; the harness lives here.
- **A-X8 Unverified metadata.** The dates and sensitivities come from CFG570 metadata only, not re-verified, and the record has no MOUS UIDs.

**U4_27928**
- **A-U1 Unnamed gap.** "Inside the required range" against "more than 2σ_tot outside" leaves a gap with no name. With a well-measured V_c the range collapses, so the literal CONSISTENT is almost unreachable: U4-a reads "within 2σ_tot (unnamed)". The harness counts the gap as not in tension.
- **A-U2 Double floor.** §3.3's flux error already includes 0.15 dex, and §4 adds another 0.15, giving 0.21 (literal; alt1 = a single floor).
- **A-U3 Window.** No moment-0 window or continuum is stated. Default: ±500 km/s; continuum = median of |v| > 600.
- **A-U4 / A-U17 C2.** 100 random apertures overlap in any finite box. Default: an 8″ box and translated mask copies, with the mean tested against 3 rms/√N_independent. With 15–35 independent apertures the 20% rms tolerance fails on pure noise about 10% of the time (U4-b).
- **A-U5 Upper-limit aperture.** Not stated. Default: a circle of radius 2R_e = 0.98″.
- **A-U6 Non-detection.** A one-sided Δ_m is promised, but G1 failure leaves no V_c, so nothing is scored.
- **A-U7 Radius.** V_c is read at 8.3 kpc (CFG806); the requirement uses the sealed 2R_e = 8.271 kpc.
- **A-U9 RESTFRQ.** Pipeline conventions differ. The harness checks frequency coverage and reports RESTFRQ.
- **A-U10 C2 "quoted noise".** Undefined. Default: the analytic mask-sum noise (beam-shaped correlation, plus a continuum-median term).
- **A-U11 Inclination clamp** when q < q0.
- **A-U12 / A-G14 No taper branch.** See Sensitivity.
- **A-U12b G2 radius.** Default: the deprojected radius of the farthest mask pixel.
- **A-U13 / A-G13 Noise-selected masks.** A ≥ 2σ mask selects positive noise. The literal translated-aperture S/N passes on pure noise (U4-d 9.5, GS4-b 10.6). Default: a selection-aware null, the same mask grown at 200 random off-source seeds. The literal reading is printed too.
- **A-U14 "2″ aperture".** Radius or diameter is not said; both are printed.
- **A-U15 Stellar systematic.** The 0.2 dex M★ systematic is "carried as an interval". If it also widens the required range (alt3), R-H's tension in U4-a and the framework's tension in U4-b both disappear, so U4 then separates nothing.
- **A-U16 V_c error.** From the fit covariance. It is underestimated by about √(pixels per beam) for correlated noise; the beam-corrected error is printed as alt4.

**GS4_24110**
- **A-G1 Stellar term.** σ_Δv uses ±0.2 dex for M★ (CFG809), whereas CFG572's published GS4 verdicts used ±0.1.
- **A-G2 FLOOR rule against Δ_v.** The FLOOR rule outranks |Δ_v| ≤ 2σ. On CI21 at M★ 10.89, canonical footing, R-H's "in tension" rests on the FLOOR rule alone, because Δ_v alone reads consistent.
- **A-G3 Upper-limit reading** is undefined. Default: Δ_v ∈ [f(0), f(UL)] against ±2σ.
- **A-G4 ROBUST.** Two questions:
  - which CO43 and dust branches enter (default: r41 0.37 and α_CO 4.36);
  - whether "no model is described" is meant per model or globally.

  With CFG572's routes fixed, the framework is NOT ROBUST for every CI21 value, while R-H/L-fb's FLOOR tension is ROBUST.
- **A-G5 Upper-limit aperture.** Default: the R_e circle.
- **A-G6 Continuum S/N.** Read as the peak S/N inside the [CI] mask.
- **A-G8 Ring radius** of 6.5″; no noise-map option.
- **A-G9 G3 error and bias.**
  - The G3 error comes from the covariance, which is underestimated for correlated noise.
  - A Gaussian fitted to an exponential disc biases R_g low: the MOCK gives 0.69 of the truth, and the dust size shows the same bias.
- **A-G10 C4 rounding.** "< 1e-6" holds only for the coefficient derived from the A values (4.56583e-4), not for the rounded 4.566e-4 (3.7e-5 off).
- **A-G11 MUTATE coverage.** +2000 km/s can leave a 1.875 GHz spw at 270 GHz. In that case the run reports NOT RUNNABLE (exit 2), as CFG572 did.
- **A-G12 G4.** Implemented as ≥ 3 beam-spaced, monotonic, S/N ≥ 5 samples.
- **A-G16 Continuum after a G1 failure.** "Stop at 3.3" leaves 3.1 undefined without a mask; the continuum is reported in the R_e circle.

**Both targets**
- **A-M1 Mask extent.** Default: the ≥ 2σ components that touch a 0.5″ circle at the catalogue position.
- **A-M2 Per-plane beams.** If the cube carries a BEAMS table, the median beam is used.

## NOTE for the owner (proposed 2026-10-20; nothing frozen is changed)
Superseded on 10-21 by the owner's CLARIFICATION_2026-10-21 files (35ea5e1be) and the owner decision of 10-20 on the governing plans.

If the owner agrees, a dated file `CLARIFICATION_2026-10-2x.md` could be committed into each plan's lane **before 2026-11-06**, saying:
1. **Which plan governs** (A-X1): "On release day the governing score is [CFG806/CFG809 | AG5]; the other is reported as a cross-check." Also whether THEORY_CANONICAL §2's kill line applies to one disc (A-X2).
2. **U4 §4 reading** (A-U1, A-U2, A-U15): "consistent = |Δ_m| ≤ 2σ_tot; σ_tot = √(σ_rms² + σ_V² + 0.15²) (one floor); the M★ 0.2 dex systematic enters only the FLOOR-reduced statement."
3. **G1 significance** (A-U13, A-G13): "the S/N is computed against the same mask procedure run at random off-source seeds."
4. **Upper limits** (A-U5, A-U6, A-G3, A-G5): "the limit aperture is a circle of radius 2R_e (U4) / R_e (GS4); a U4 non-detection is reported only."
5. **Taper** (A-U12, A-G14): "if the native cube fails G1, a declared uv-taper to [X″] is a pre-registered branch, never pooled." Or: "no taper; an upper limit is the result."
6. **GS4 rules** (A-G2, A-G4, A-G11): whether the FLOOR rule outranks Δ_v; whether NOT ROBUST is per model; the MUTATE fallback (+1000 km/s, as CFG572).
7. **Housekeeping** (A-X4, A-X5, A-X7): the IDs, the stale "DRAFT" headers, and that the CFG942 harness stands in for the named scripts.

## Departures and disclosures in this lane
All were made before any real data, on MOCK runs only:
- **G1 default.** After the first U4-d run, the S/N changed from the translated-mask rms to a selection-aware null, because the literal reading passed on pure noise. The literal reading is still printed.
- **C1 flux.** The C1 injection flux was fixed at F-DESI's sealed 10.42 (U4) and 9.82 (GS4), instead of the measured flux.
- **Quoted noise.** The C2 "quoted noise" formula was corrected after U4-a's first C2 showed a ratio of 1.82, which came from crowded apertures and a missing correlation term.
- **Mock noise.** It was regenerated so that its autocorrelation is the beam, like interferometric noise.
- **Boxes.** The boxes were enlarged (U4 4.4″ → 8″, GS4 9.5″ → 10.5″) when the apertures did not fit.
- **Memory.** The memory-saving rewrites (streamed moment-0, low-memory LM fit, chunked hashing) change no rule.

## Files
- **Scripts:** `cfg942_common.py`, `cfg942_u4.py`, `cfg942_gs4.py`.
- **Outputs:** `*_selftest`, `*_MOCK_<x>`, `*_MOCK_a_MUTATE`, each as `.out` + `_results.json`.
- **Not committed:** the mock FITS (scratch). Their sha256: U4 a/b/c/d = e51d76b7…, 60c0fe97…, 5abb0548…, 4d2dd9e9…; GS4 a/b/e cubes = adfbd807…, 2f2c3295…, da129b4c….

κ = ½ FITTED; footings never pooled; cold-energy mass required; not theory closed.

## Addendum E kernel switch (2026-10-22; PRE-DATA; MOCK only)

Owner-approved addendum E (CFG806/CFG809 `CLARIFICATION_2026-10-22_ADDENDUM_E.md`, ffb14e40bc) adds n = 1 (AG4e seal
9802de0d…) and n = 2 (AG4d seal d64727b5…) as labelled parallel readings beside the nu_mono verdict kernel.

- **Switch.** `CFG942_KERNEL=n1|n2 python3 -B cfg942_u4.py …` (same for `cfg942_gs4.py`). Unset or `nu_mono` = the frozen path.
  The kernel run swaps CFG571's NU exactly as AG4e/AG4d sealed it, scores against that law's own seal, adds the seal and
  both addendum-E files to K1, prints a banner, and names every output `…_KERNEL_n1` / `…_KERNEL_n2` (the release-day copy
  too: `cfg806_u4_KERNEL_n1.out` etc.), so a parallel reading can never overwrite or be pooled with the verdict file.
  R3 (plan-table transcription) and the THEORY_CANONICAL quote keep comparing against the nu_mono seal, as the plan's tables do.
- **nu_mono path unchanged.** Re-run with the new code: selftest (U4, GS4) and MOCK-a plain + MUTATE (U4, GS4) are identical to
  the committed outputs line for line apart from the harness's own sha256 line; both MUTATE controls still exit 1.
- **n1 / n2 MOCK results (committed `*_KERNEL_*` files).** R2 reproduces each law's seal exactly (max |d| 0.0 over 56 U4 and
  16 GS4 entries). Both MUTATE controls bite under both kernels (U4 selection-aware S/N −0.30, GS4 +0.29, exit 1).
  Two checks fail by design, and each is a finding, not a defect:
  - GS4 selftest, both kernels: "A-G4 scan agrees with addendum A s1" fails. Addendum A's robustness sentence was written for
    nu_mono; the n = 1 / n = 2 readings do not inherit it.
  - U4 MOCK-a, n = 2 only: the primary branch reads NO SIDE instead of FRAMEWORK SIDE. MOCK-a is built at n = 2's own F-DESI
    requirement at V_c 250, where n = 2's framework and R-H requirements overlap on the canonical footing, so U4 cannot
    separate them under n = 2 there (the alternate footing reads FRAMEWORK SIDE).

κ = ½ FITTED; footings never pooled; one disc excludes no model; not theory closed.

## Addendum F reading 'v3aq' (2026-10-23; PRE-DATA; MOCK only)

Owner-approved addendum F (CFG806/CFG809 `CLARIFICATION_2026-10-23_ADDENDUM_F.md`, f6f0ba66a4) adds v3's AQUAL-disc requirement
(lane S3_v3_mw_seals, `SEALED_V3_ALMA_AQUAL.json`, sha256 b5d65a5e…, commit 90f4d517d6) as a labelled parallel reading.

- **Switch.** `CFG942_KERNEL=v3aq python3 -B cfg942_u4.py …` (same for `cfg942_gs4.py`). Outputs are named `…_KERNEL_v3aq`;
  K1 adds the seal and both addendum-E and addendum-F files.
- **What it computes (rule 4).** CFG571's head, read-only, with NU = C·ν₁. C is the sealed AQUAL/algebraic in-plane ratio:
  C_stars for the FLOOR test, C_final[R_g = R_d] for the R_d row and logVbar2R_G, C_final[R_g = 1.5 R_d] for the 1.5 R_d row and
  logVbar2R_G_Rg=1.5Rd. GS4 is read at the sealed V_c 206 and log M★ 10.89 / 10.76. U4 interpolates C linearly in V_c between the
  bracketing sealed grid points; a U4 M★ variant (±0.2 dex) keeps the C sealed at log M★ 10.74 (harness convention, printed in
  the banner). No AQUAL solve is ever run.
- **Not sealed (rules 4, 6).** A U4 branch whose evaluated V_c (incl. ±eV and the M★ variants) leaves 150–300 km/s, GS4's [CI]
  V_c branches and GS4's measured R_g are reported 'NOT SEALED' and not scored for this reading; the information-only R6 power
  table prints 'NOT SEALED' where V_c ± 5 leaves the grid.
- **Δ_v (rule 5).** GS4's R_g = 1.5 R_d shape uses the sealed logVbar2R_G_Rg=1.5Rd; U4's information-only Δ_m does the same.
- **Tests (mirror run, then outputs copied here).**
  - R2 reproduces the seal to 2.1e-13 dex (U4, 56 entries) and 2.2e-11 dex (GS4, 16 entries), incl. the 1.5 R_d requirement;
    the largest GS4 difference is log M_gas next to FLOOR (root-finder tolerance), so this reading's R2 line is ≤ 1e-9 dex.
    R2b: the C_stars FLOOR test reproduces every sealed GS4 FLOOR flag.
  - MOCK-a reads FRAMEWORK SIDE on U4 and GS4 (GS4: 8 of 8 primary-route cells); both MUTATE controls bite (U4 selection-aware
    S/N −0.30, GS4 +0.29, exit 1).
  - GS4 selftest exits 1 on "A-G4 scan agrees with addendum A s1" only, as under n = 1 / n = 2: addendum A's robustness
    sentence was written for ν_mono.
- **ν_mono, n = 1 and n = 2 paths unchanged.** Re-run with the new code: selftest and MOCK-a plain + MUTATE (U4, GS4) for ν_mono and
  n = 1 are identical to the committed outputs line for line, apart from the sha256 and peak-RSS lines.

κ = ½ FITTED; footings never pooled; one disc excludes no model; not theory closed.
