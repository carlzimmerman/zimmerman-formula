# CN1_contraction_on_cold_share: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** FC1's result assumes the cold halo does not respond when baryons settle. The zoom η is a pre-baryon quantity: gas is dust in the zooms. X39 found full Blumenthal contraction breaks SPARC from the floor rule. What does contraction do on FC1's rule, and how much softening before contraction would have to happen for the grader's lines to hold? This sets the net job left for baryon physics, in numbers that can be compared with the channels already measured.

**Model.** X74's grader with FC1's conversions (commit 061b2e2a1a), CE1's median η (ng 48 clusters), X73 PRIMARY, f★ 0.034, canonical primary, alt reported.
- **Collapse-branch systems only** (those where f_c η Σ_coll > Σ_a0): initial cold profile with S_i = R f_c η Σ_coll, contracted by X39's `contract` (Blumenthal; F = M_b,tot / M_cold; baryons as X39 builds them, Υ by Υ on SPARC). Clusters add X39's BCG (CFG922, a = 10 kpc).
- **Floor-branch systems are unchanged.** The floor Σ_a0 was calibrated on final rotation curves, so it is a final-state quantity and is not contracted again. This is a modelling decision, stated here before any number.
- **Groups** are not contracted (X39 did not contract them). Reported as in FC1.
- R is the softening of the collapse-branch S before contraction: grid 1.00, 0.95, ... 0.30.

## Frozen outputs
1. **At R = 1:** SPARC median Υ on both backgrounds, median Υ and ΔV by V_flat (LS1's bins), and all cluster keys.
   - **CONTRACTION SURVIVES** if every line passes, **CONTRACTION BREAKS** with the failing lines otherwise.
2. **R_SPARC:** largest grid R at which the SPARC line holds (both backgrounds). **R_CL:** largest grid R at which all 15 cluster keys hold in both h cells.
3. **Reach, compared with the record's channels at face value** (one galaxy or one halo each, and those runs have no contraction):
   - **Galaxy (CM1, CM3):** R_SPARC ≥ 0.932 is REACHABLE AT MEASURED GAS; 0.573 ≤ R_SPARC < 0.932 is ONLY AT CEILING (coupling ≈ 1, rare bursts); below 0.573 is OUT OF RECORDED REACH.
   - **Cluster (BH1, 10¹³ uncapped 0.917, 10¹⁴ uncapped 0.948; CL5 control 0.91–0.95):** R_CL ≥ 0.95 REACHABLE; 0.91 ≤ R_CL < 0.95 MARGINAL (needs the uncapped or control cases); below 0.91 OUT OF RECORDED REACH.

## Reported
Gnedin at R = 1 and at R_SPARC (externally calibrated). MUTATE and checks below.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** with contraction off and R = 1, the run reproduces FC1's committed SPARC rms/Υ and cluster predictions (both footings, f★ 0.034, median), |d| ≤ 1e-9.
- **K2:** `contract` with M_b = 0 and F = 0 returns the input profile, and reproduces X39's point-mass + SIS closed form to X39's tolerance.
- **K3:** BCG match count 190, as X39.
- **MUTATE:** X39's own mutation, (1 − F) in `contract`, must fail K2.

## What this cannot show
- Blumenthal is a limit: slow, circular, no feedback. Real settling may be weaker. X39's Gnedin case fails too, on SPARC.
- The R comparison assumes softening acts before contraction, and that its reach measured without a disc still applies. Neither is shown.
- A required R does not derive that R. It states the job, not its solution.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
