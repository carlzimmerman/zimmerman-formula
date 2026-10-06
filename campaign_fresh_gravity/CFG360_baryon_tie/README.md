# CFG360: the baryon tie (Gap 2)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 581291e38.

**Question.** Can one early process fix the cold fluid's charge per baryon, so that omega_c/omega_b = 5.364 +- 0.065 follows from the framework?

**Verdict: NO-GO.** The cold amount stays a free number. Gap 2 is still open, and the cold MASS is still required.

| | result |
|---|---|
| T0 | All controls pass. R_CMB = 5.364 +- 0.065. The wave-field window is [2e-20 eV, 2.78 eV]: the lower edge is read from CFG288's output, and the upper edge is derived here (occupation = 1 in the g04a cluster core). The criteria did not supply an upper edge. CFG288 A1 is reproduced: 1.52e10 rho_Lambda. |
| T1 | Equal charges need m = 5.03 GeV, 1.8e9 x the upper edge. That is a particle (asymmetric dark matter), not a fluid. |
| T2 | A fluid needs r = 1.8e9 to 2.5e29 charge units per baryon. |
| a1 | Gravity only, minimal coupling. The two charges are separately conserved, so their ratio is a ratio of free constants. **[ARG]** |
| a2 | Curvature couplings of the currents break G9 and are inert in the radiation era. |
| b1 | A thermal shared current gives r = k/2, so m >= 2.5 GeV: a particle. |
| b2 | A condensed shared current survives T4 for m >= 6.1 meV, but R ~ X_tot, the free total asymmetry. The free number is relocated, not reduced. **POST-FREEZE (labelled):** proton decay (tau > 2.4e34 yr) against equilibrium down to T_d conflicts by >= 2.7e3, even at the cosmic-mean <Phi> with the rate x1e3. |
| b3 | A derivative coupling (d theta) J_B/f sets eta_B, not R. The amplitude stays free. **[ARG]** |
| T5 | Diagnostic: 1681 pure-number forms, 4 hits at 5.364 and 4 at a planted 3.00. The chance rate is 2.4e-3/form, above the 1e-3 threshold, so any numeric match is numerology. Z = 5.7888 sits +0.09 sigma from the cluster ratio 5.73 but +6.6 sigma from R_CMB. That is a coincidence, never pooled. |

[ARG] rows are structural arguments, not computations.

Run: `python3 cfg360_baryon_tie.py` (12/12, rc 0); `MUTATE=1 python3 cfg360_baryon_tie.py` plants R = 3.00 and T0a fails (11/12, rc 1).
