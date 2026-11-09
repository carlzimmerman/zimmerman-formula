# WM1 AMENDMENT A1 (technical; before any graded number of gates 7b-L, 8 or CS)

Criteria: FROZEN_CRITERIA.md (6e40130dfa). Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What broke.** Section 2 froze nu(k, z) from the warm model's own CLASS linear power. Above k_hm the relic's power falls to
P_warm / P_cold = 1e-3 at 3 h/Mpc and below 1e-4 at 10 h/Mpc, so y = |delta g_N| / a0 -> 0 and nu -> infinity. On the ODE's k grid
(to 200 Mpc^-1) the boosted baryon mode overflowed and B_m came back NaN. The first canonical run printed NaN for 7b-L (its printed
"FAIL" is void: not a number) and crashed in the forest. Numbers printed before the crash and unaffected by nu: KA-W3 (PASS),
KA-W2 (PASS, 3e-5), G6 BAO+SN (+0.058, PASS).

**Change.** The graded nu(k, z) uses SS5's own convention, frozen at 12c42eef04 and reproduced by KA-W2: y from the record's cold
reference CLASS power (ss1_cosmo's reference model, at the footing's fitted A_s, as SS5). This is the gentler choice (more field,
smaller nu, smaller boost), so a FAIL under it is the stronger statement.

**Bracket, reported only.** The frozen warm-P reading of B_m and delta_b / delta_chi at k 0.01, 0.03, 0.1, 0.3, 1 h/Mpc
(P_warm / P_cold >= 0.5 there, so finite), z 3, 1.2, 0.3, 0.02.

Nothing else changes: the factorisation R_m = sqrt(P_warm / P_ref) x B_m, the gates, lines, KAs, MUTATEs and order.
