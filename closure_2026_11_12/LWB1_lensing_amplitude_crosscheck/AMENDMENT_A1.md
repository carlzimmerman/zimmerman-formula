# LWB1 AMENDMENT A1 (2026-11-12, post hoc, committed alone)

**What failed.** In the first full run (`lwb1.py` as written after criteria f4b3128cc1) known answer KA1 failed: the power-law
wp check returned a largest relative error of 0.0172 against a 1 % line (Delta Sigma: 0.0008, passing). As frozen, the lane
label is therefore **NO VERDICT on both footings**.

**Why (diagnosed in a scratch script, not in the lane).** The error is in the check, not in the pipeline. The check
integrates the power-law xi along the line of sight only to pi = 3000 h^-1 Mpc and compares with the analytic wp to
infinity. For gamma = 1.8 the omitted tail is 2 A 3000^(1 - gamma) / (gamma - 1), which is 0.0020 / 0.0041 / 0.0071 /
0.0171 of wp at r_p 2 / 5 / 10 / 30, exactly the measured deficits (-0.0002, -0.0042, -0.0072, -0.0172 after the tail is
added back: residuals <= 0.0005). The xi transform itself is good to <= 0.74 % at s 2-300 (largest at s = 2, below every
kept radius). The pipeline's own wp never integrates a power law beyond 300 h^-1 Mpc; its pi_max cuts at 40-300.

**The amendment.** KA1's analytic comparison adds the analytic tail beyond pi = 3000 to the numerical wp. Nothing else
changes: the data, scales, model, statistic, lines, brackets, other known answers and mutations are as frozen.

**What had been seen when this was written.** The first run's KA lines and the canonical primary rows: J best sigma8
0.7864 +- 0.0285 (gap +0.90, AMPLITUDE CONSISTENT), KiDS 0.7596 +- 0.0508 (NO POWER), DES 0.6470 +- 0.0474 (gap +3.48,
TENSION), HSC-Y3 0.8580 +- 0.0355 (gap -1.29), K+D 0.6990 +- 0.0364 (gap +3.11, TENSION). The amendment does not touch any
of these numbers; it can only change whether KA1 gates them. Both readings (as frozen: NO VERDICT; under A1: the graded
label) are reported in RESULT.md.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
