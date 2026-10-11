# CFG468: the kernel family. One C² splice of ν_mono below every observed acceleration removes the zero-field chaos and keeps SPARC unchanged; no kernel with an exact deep-MOND limit does

The criteria were committed first: `FROZEN_CRITERIA.md` (b0d7274a0), alone, before any script.
- **Scripts:**
  - `cfg468_kernels.py` defines the kernels and the engine adapters.
  - `cfg468_zero_field_runs.py` does the compute; its log is `cfg468_run.log`.
  - `cfg468_kernel_family.py` runs the SPARC arm, scores the zero-field runs and builds the table.
- **Outputs:** `cfg468_kernel_family.out` + `_results.json` (main, 10/10 checks, rc 0) and `cfg468_kernel_family_MUTATE.out` + `_MUTATE_results.json` (9/9 checks, rc 1 = the control fails as required).
- **Engine:** `cfg468_engine.py` is byte-identical to CFG358's engine (sha256 bde2fbb6…, checked at run time). Only the kernel object passed to it changes.
- **Work arrays:** `../_external_data/cfg468_work[_MUTATE]`, outside git.

The question had three parts. Is there a ν(y) that:
- (i) fits the SPARC RAR as well as ν_mono;
- (ii) keeps ν → y^-1/2 and ν → 1 (BTFR exact);
- (iii) removes the zero-field nonlinear FAIL of the **ungated** chassis (CFG321/322/325/358)?

## Bottom line
- **No kernel with an exact deep-MOND limit removes the zero-field chaos.**
  - The engine works at y = y*·ŷ, with y* = 2.56e-18 (set by the chassis constant α_c = 3.2e-9). So every engine field sits at y ≲ 1e-17.
  - Down there, every kernel that obeys (ii) is the same power law. In the engine's own units they differ by about 1e-11.
  - The prediction P1 was frozen before any run. It holds exactly: ν_simple gives ν_mono's λ(N) and Amax to every printed digit at all 8 (N, ε) cells, and ν_standard matches at the one finished cell.
  - The MUTATE kernel (exact limits, five kinks) stays chaotic as well (OPEN).
- **What does remove it is regularising the deep limit itself.** Here that is S1, a C² splice of ν_mono below y_s = 0.1 y* = 2.56e-19, i.e. below about 2.4e-29 m s⁻².
  - With S1 the field still grows from 1e-4 to the same saturated level (rms ŷ ≈ 0.49 against ν_mono's ≈ 0.5). It spends about 50 time units in the nonlinear regime.
  - But the pair separation never grows: max D/δ ≈ 6 at every N against 340–7400 for ν_mono, and D(1e-3)/D(1e-5) = 100.0, i.e. linear response.
  - Result: **BOUNDED at both ε and every N (127–1023) → CONVERGENT.**
  - S1 is identical to ν_mono everywhere SPARC (or any observation) looks, so SPARC Δχ² = 0.00. By the brief's definition **S1 is VIABLE**.
  - But its (ii) is only *operational*. ν stays finite below 2.6e-19, so the strict y → 0 limit is changed. That adds one declared constant (the splice point), which goes against the zero-knob rule. S1 is therefore an **option for the owner, not an adoption**.
- **This identifies the mechanism.** The zero-field "kink" is not a feature of ν_mono's shape. It is the deep-MOND limit's own cusp at a field zero: Q ∝ |w|^{3/2}, so C_L ∝ ŷ^{-1/2} → ∞ wherever the field crosses zero. Every (ii) kernel has it. Capping it, and only that, removes the chaos.
- **Answer to the question as posed** (i + ii exact + iii): **NO.** With (ii) relaxed to "exact at every y ≥ 2.6e-19", **S1 is a YES**. That is the owner's call.

## Kernel × gate table
Δχ² is against ν_mono on independent points (lane V machinery). The tolerance is ≤ 4 in both treatments (p36). The zero-field verdicts come from CFG325's frozen ratio rule on N = 127/255/511/1023, plus the pre-declared BOUNDED class.

| kernel | (ii) | SPARC Δχ² T-free / T-fix | κ_Λ (κ_crit), T-free | SPARC | zero-field ε=1e-3 / 1e-4 | zero-field | VIABLE |
|---|---|---|---|---|---|---|---|
| ν_mono (default) | exact | 0 / 0 (χ² 3001.3 / 4457.1) | 0.474 (0.392) | pass | RESOLVED-CONV / OPEN | OPEN (FAIL at 2047, CFG358) | no |
| ν_1 simple | exact | **+12.77** / −6.95 | 0.470 (0.389) | **fail** | RESOLVED-CONV / OPEN (λ identical to ν_mono) | OPEN | no |
| ν_2 standard | exact | **+242.3 / +407.6** | 0.597 (0.494) | **fail** | incomplete (1 of 8 cells done, identical to ν_mono) | incomplete | no (SPARC) |
| **S1** C² splice, y_s = 2.56e-19 | operational only | 0.00 / 0.00 | 0.474 (0.392) | pass | **BOUNDED / BOUNDED** | **CONVERGENT** | **yes (operational (ii))** |
| S2 C² splice, y_s = 1e-8 | operational only | 0.00 / 0.00 | 0.474 (0.392) | pass | not run (paused, see Status) | — | undecided |
| MUTATE kinks (1/ν piecewise linear in √y) | exact | **−32.83 / −2.22** | 0.436 (0.361) | pass | OPEN / OPEN | OPEN | **no** (control holds) |
| ν_RAR, no large-y splice (ref.) | exact | **−30.15 / −1.09** | 0.464 (0.384) | pass | class (ii) = ν_mono (P1) | — | not tested |
| P2 = √(1+1/y) (ref.) | exact | +138.3 / +139.4 | 0.578 (0.478) | fail | class (ii) | — | no |

On the footings: κ uses a0/(c√(Gρ_Λ)) with c√(Gρ_Λ) = 1.8725e-10 (κ_crit uses c√(Gρ_crit) = 2.2624e-10), H0 67.4, SPARC's tabulated distances (lane V convention). T-fix gives a0 = 1.11e-10 for ν_mono (κ_Λ 0.594). κ is FITTED and moves with the kernel: from 0.464 to 0.597 on T-free.

## Readings that matter beyond the verdict
- **SPARC cannot see kernel smoothness.** The deliberately kinked MUTATE fits *better* than ν_mono (Δχ² −32.8 T-free). So does plain ν_RAR (−30.2): ν_mono's large-y monotone log splice costs about 30 in χ² on T-free (independent points; about 1.7 after lane V's ×18 clustering deflation).
  - The MUTATE control is held by the zero-field arm alone (OPEN), not by SPARC.
  - On the record's independent-point tolerance, ν_simple fails (+12.8 T-free) although it fits better on T-fix (−7.0). On the clustered reading it would be inside.
- **The zero-field arm cannot see the kernel either, except at y ≲ 1e-17.** It distinguishes only what a kernel does to the deep-MOND cusp. That is why ν_simple's run is identical to ν_mono's, and why MUTATE, whose kinks sit at ŷ = 0.1/0.4 inside the run, is still chaotic.
- **Caveats on S1, verified as hard as a win.** The BOUNDED reading is not a frozen-out field: rms ŷ goes 1e-4 → 0.27 (t = 30) → oscillates between 0.2 and 1.35 to t = 80. Energy drift is ≤ 2.5e-8. S1's growth phase is slower (ŷ_rms 0.02 at t = 20 vs ν_mono's 0.34), so it has about 50 rather than about 70 time units of nonlinear evolution inside the frozen T = 80. At ν_mono's λ ≈ 0.08 that window would still show a factor of about 50 in D; S1 shows none.
  - Not run: N = 2047. ν_mono's own OPEN at 1023 became FAIL at 2047. Here the margin is large (Amax 6.3 flat over 511/1023, not a knife-edge), but a 2047 confirmation needs a separate go.
  - Scope: 1-D, data class D, ungated chassis.
- **Where S1's constant comes from.** y_s = 0.1 y* is tied to the chassis' α_c through y* = log1p(α_c/(2−α_c))², but the factor 0.1 is a choice. Any C² cap with C_L(0) finite should behave the same way. S1 does not test how small the cap can go: a cap the grid does not resolve would look like ν_mono.

## Other committed gates that depend on the kernel (flags; no gate re-run)
The parts of ν each gate reads are quantified in the `.out` "KERNEL STRUCTURE" block. ν/ν_mono at y = 0.05 / 1 / 3 is 1.002 / 1.023 / 1.038 for simple, 0.907 / 0.804 / 0.862 for standard, and 1.000 / 1.000 / 0.998 for ν_RAR.

1. **Deep limit only → kernel-blind within (ii)** (this lane, P1): the zero-field chain CFG321/322/325/328/358, and XC5's "open zero-field regions are Hölder-½".
2. **Transition region, y ≈ 0.01–10 (ν moves by 2–20%):**
   - SPARC a0/κ estimators, including the MNRAS estimator C, which uses ν_RAR; κ moves 0.464 → 0.597 across kernels.
   - **Gaia DR4 pre-registration (FROZEN).** Amendment 3 showed that a kernel change moved γ_v by 2.9σ. Any kernel change needs an append-only amendment on the owner's go.
   - CFG447 (EFE-blind force vs DR3) and the directional-EFE test.
   - Clusters, groups and SLUGGS (CFG4, CFG55/323/330/331, CFG432/453).
   - KiDS lensing lanes (CFG15/21/255/261, L342, GP lanes).
   - The high-z a0(z) inversions, which invert ν: the CFG213–281 and CFG300–308 lanes, PAPER38/43.
3. **UFD lanes (y ≈ 0.01–0.1):** CFG46/51/244/259/286/327/344/463 and AUDIT_UFD. The SPARC-passing kernels agree there to ≤ 0.2%. ν_2 and P2 are 5–9% lower. The UFD +0.32 dex excess is not a kernel effect for any kernel that passes SPARC.
4. **Tail, y ≫ 10 (Solar System, pulsars, vacuum integral):**
   - CFG357 (Cassini Q2: simple +6.32σ vs ν_mono +8.74σ unfiltered);
   - L340 S1's Saturn floor; CFG291/311 pulsars;
   - puzzle_32π p35/p56/p57 and PAPER41/44.
   - ν_mono's log splice gives a 1/y tail (slope −0.97 at 1e6), the same class as simple. ν_RAR and ν_2 have fast tails.
   - S1/S2 share ν_mono's tail exactly, so these gates are unchanged by adopting S1.
5. **Sign of h′ = d[y(ν−1)]/dy over all y** (L340 A1 built ν_mono's monotone floor for this; XC5 convexity needs > −1):
   - ν_mono, simple, P2, S1 and S2 keep h′ ≥ 0.
   - ν_RAR (min −0.032), ν_2 (−0.081) and MUTATE (−0.212) do not. They would need L340's floor added at large y before any chassis gate (CFG291/292/294/312, L340) could use them.
   - S1 changes nothing above 2.6e-19, so every chassis gate that reads ν_mono at y > 1e-18 is unaffected.

## Controls
- **C0, the adapters:**
  - The generic ν_mono adapter matches the engine's own kernel to 1.4e-15.
  - Q and C_L identities hold to ≤ 2e-10 and every adapter is convex.
  - S1/S2 joins are C² to ≤ 1e-12.
  - MUTATE's C_L jumps are exactly ×0.50 and ×1.50.
- **C1:** the ν_mono baseline re-scored from CFG325's committed arrays reproduces CFG325's λ table and its OPEN verdict.
- **C1′:** the generic driver at N = 127 reproduces CFG325's λ and Amax. Even the refactor counts match: 5115.
- **C-S:** P2 on p35's grid reproduces p35's χ²_min, 4596.5 / 3139.8.
- **C-K:** K0 is CFG5_common.nu_mono itself.
- **P1** held. **MUTATE** held: it is not VIABLE, through the zero-field arm.
- **GR control:** C2 was not re-run (it is kernel-independent; CFG358's C2 stands).

## Status, compute, departures
- **Incomplete.** The grid's worker processes were found **stopped (SIGSTOP, state T)** on 2026-10-10, after 81 of 126 runs. This lane did not stop them, and they were left stopped. CFG468's watchdog (committed by the orchestrator in 2efa706de) does not relaunch stopped processes.
  - Missing: ν_standard (7 of 8 cells) and S2 (all).
  - Neither can change the answer. ν_standard fails SPARC, and S2 has only operational (ii), like S1.
  - To resume: `kill -CONT` the cfg468_zero_field_runs.py processes, or kill them and relaunch the runs script, which skips finished arrays. Then re-run `cfg468_kernel_family.py`.
- **Compute:**
  - 303 process-hours across the completed runs, at nice 15 with 6 workers on a shared machine (load 9–21), taking 52.5 h wall to the last completion. By kernel: S1 108, MUTATE 99, simple 86, standard 9, C1′ 2.
  - S1's N = 1023, ε = 1e-4 runs took 22.8 h each.
- **Departures from the frozen text, none affecting a verdict:**
  - The pool order was changed before the main pool started (decisive kernels first).
  - C0c's first draft used a coarse finite difference. It was corrected to the frozen ≤ 1e-8 with both branches evaluated at the join, before any zero-field result existed.
  - P1 is scored on the available cells and requires the full ladder for at least one class-(ii) kernel (ν_simple).
  - VIABLE is reported as "undecided" where SPARC passes but the zero-field ladder is incomplete (S2).

κ = ½ is FITTED. The cold mass is still required; no dark-matter particle is added. Nothing here closes the theory. The zero-field result concerns the ungated chassis only, not candidate B.
