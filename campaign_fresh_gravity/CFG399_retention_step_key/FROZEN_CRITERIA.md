# CFG399: is the retained-cold-fraction step keyed to virial temperature? FROZEN before any script exists

Owner chat 10-06. κ = ½ fitted; both footings. No DM particle; the cold mass is still required.

**The claim tested.** sonnet55_push/cold_mass cm08–cm10 measured two retention levels (f = (M_tot − M_law)/((Ω_c/Ω_b) M_b) ≈ 0.13 in galaxies, ≈ 0.6 in groups/cluster centrals), with the step at host M200m 1e12–1e13, T_vir 0.5–2.3e6 K. A **temperature-keyed** step (a phase change) predicts any system with T_vir > 2.3e6 K sits at the upper level, whether or not it is a group.

**Out-of-sample data.** The 23 Ogle+2019 super spirals, scored with cm08's definition and enclosed baryons in CFG390 session02 (`super_spirals_retention_results.json`: per-object f and T_vir = 0.6 m_p V² / 2k). These are isolated discs, not group members, and were not used to place the step.

**Prediction (frozen, no fit).** A logistic in log T_vir centred on the geometric mean of the bracket (1.07e6 K), with its 10–90% width spanning 0.5–2.3e6 K, between 0.13 and 0.60. Predicted f per object from its T_vir.

**Statistic.** Objects with T_vir > 2.3e6 K: median measured f against median predicted f; bootstrap over objects (2000, seed 51). Both footings.

**Verdict.** TEMPERATURE-KEYED STEP **FAILS** if (median predicted − median measured) > 3σ. **SURVIVES** if |difference| < 2σ. INCONCLUSIVE otherwise. Reported: the same for the nine fastest only.

**Control.** K1: the logistic returns 0.13 ± 0.01 at 3e5 K and 0.60 ± 0.01 at 1e7 K.

**MUTATE (`--mutate`).** Measured f replaced by the prediction. The verdict must become SURVIVES; exit 1 when it does.
