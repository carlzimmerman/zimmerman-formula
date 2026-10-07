# CFG411 FROZEN CRITERIA (overnight): (a) CFG372 corrected; (b) a 512³ resolution check of the current best rule
(owner 2026-10-06: "start up some heavy overnight runs ... that we havent done"; committed before any run)

**Engine.** CFG410's engine (corrected comoving k_J ∝ a^(−1/2), audit 5819dd616): RES rule, R_c = 3 Mpc/h, A0-FLAT, seed 359, 150 steps. The only change is that the IC white-noise grid size NSEED follows the particle grid when it is larger than 256.

**(a) CFG372 corrected.** The pure-hot filter (f_hot = 1 at 1e6 K; "HOT1"), at 256³, both footings. This is the clean re-run of CFG372's withdrawn "GROWTH OK". Decision: CFG361's cuts (GROWTH OK / TENSION / FAIL) per footing.

**(b) Resolution convergence (the referee's MAJOR item 2).**
- S0 and RES MIX-A at 512³ particles on a 512³ mesh, canonical footing only, 8 threads, run one at a time. The 512³ ICs use a 512³ white-noise grid, so the realisation differs from 256³.
- Compare the RATIO to S0 at each resolution. Ratios cancel most realisation variance; that is stated as a caveat.
- Reported: σ₈ ratio and max|P−1| for k ≤ 1 at 512³, against CFG410 BASE canonical at 256³.
- Decision:
  - CONVERGED if both change by less than 0.02 (absolute);
  - GROWS WITH RESOLUTION if the P excess rises by ≥ 0.02 (as CFG361 K4 found for T5);
  - SHRINKS otherwise.
- The 256³ verdict for this rule is treated as robust only if CONVERGED or SHRINKS.

**Controls.** The NSEED change reproduces CFG410's 256³ ICs exactly when NSEED = 256 (the default path, unchanged).

**MUTATE.** None new: the controls are inherited (CFG410).

**Scope.** As CFG410. Bookkeeping reservoir. κ = ½ is fitted. The cold fluid is still required.
