# CFG424 FROZEN CRITERIA: remove the last hand-set number. The cold fluid comes from each halo's own turnaround sphere (256³)
(owner 2026-10-07: "keep pushing the doors", "nothing chosen by hand". Committed before any run.)

**Change from CFG423.** The Gaussian catchment of width R_c (hand-set, CFG366) is replaced by mass conservation inside each catchment:
- **Catchment:** each periodic 6-connected component C of the union of the hosts' turnaround balls (radius r_ON, i.e. x = 1).
- **Phantom excess:** e = f·max(s_ph − s_c, 0), confined to CFG423's mass-conserving edge balls r_M/ln(1/(1−f_b)), which lie inside C.
- **Drawn-down cold fluid:** comp = s_c · (Σ_C e / Σ_C s_c) on C.
- **Source added:** e − comp. It sums to zero on every catchment, so mass is conserved halo by halo.

**Remaining inputs:**
- κ (fitted), with the footing;
- f_b (cosmic composition);
- the T1 switch ε and the MIX-A gas filter, inherited from the engine lineage and unchanged since CFG410;
- **no tuned radius and no catchment width.**

**Runs.** Seed 359 at 256³:
- TA-can: canonical footing;
- TA-alt: alt footing;
- MUTATE: canonical with the compensation switched off, i.e. e added with no mass drawn down. This is the claim's control, and it must NOT be GROWTH OK.

**Decision (CFG361 cuts, vs CFG359 S0).**
- **ZERO-KNOB PASS:** TA-can and TA-alt are both GROWTH OK, and MUTATE is not GROWTH OK.
- **PARTIAL:** exactly one footing is GROWTH OK.
- **FAIL:** neither footing is GROWTH OK.
- **INCONCLUSIVE:** MUTATE is GROWTH OK, which means confinement alone does the work.

**Reported:** the overdraw fraction, i.e. the share of catchment mass where Σ_C e > Σ_C s_c (more phantom than cold fluid).

**Caveats.**
- This is 256³ and one seed.
- The cold fluid is bookkeeping, not moved particle by particle.
- A pass removes the hand-set numbers from the growth fix. It does not derive κ, f_b or ρ_Λ.
