# CFG586 FROZEN CRITERIA — is CFG585's old-vs-young early-type difference environment (satellite leakage)?

(owner chat, "yes run the neighbour check" / "figure out the true nature of it"). Committed alone before any count or
lensing number for these subsamples.

Input: CFG585's masks exactly (f30 early types, colour-residual tertiles at fixed mass; OLD 8,843 / YOUNG 8,850), rebuilt by
executing cfg585_age.py's head unedited. CFG585's raw K9 D = +0.86–0.94 (Z +2.65; post-hoc relabel p 0.005) and K-in D
+0.59–0.65 (Z +1.51). K9 is used as PRIMARY here because that is where CFG585's signal sits (a follow-up of a post-hoc hint;
a survival is still only suggestive).

Step 1 (no lensing): companion counts with CFG509's method verbatim (cfg509_counts.py executed unedited up to its class
loop: more-massive pool galaxies within R_p < 0.5 Mpc, 10 < |Δχ| < 600 Mpc, minus the 4–6 Mpc annulus; CFG502's halo-model
prediction; λ = (meas − pred_2h)/pred_sat; stack weights; 50-patch jackknife). Report λ_old, λ_young, λ_f30all, and
Z(λ_old − λ_young).
Step 2 (lensing re-score): CFG531's estimator (executed unedited up to its analysis) with each group's OWN leakage:
fE = fO = (λ_group / λ_f30all) × CFG529's measured f30 grid (clipped to [0, 1]). D_env = ε_old − ε_young, error as CFG531.
Verdict (K9 primary, all four cells A/B × canonical/alt):
 ENVIRONMENT EXPLAINS iff |Z(D_env)| < 1 in every cell AND D_env ≤ 0.5 D_raw in every cell.
 AGE SIGNAL SURVIVES iff Z(D_env) ≥ 2 in every cell AND D_env ≥ 0.5 D_raw in every cell.
 PARTIAL otherwise. K-in reported.
Controls: C1 CFG509's all-lens measured/predicted 0.845 reproduced (its own check); C2 CFG509's stack-weighted early λ
1.0572 reproduced to 0.001 by the executed stat(); C3 with scale factor 1 for both groups D_env reproduces CFG585's D to 0.001.
MUTATE (CFG586_MUTATE=1): assign OLD three times its measured leakage scale; D_env(K9) must fall below D at the measured
scale in every cell (direction check: more assigned leakage → less excess).
κ = ½ fitted; footings never pooled; cold energy's mass required; not theory closed.
