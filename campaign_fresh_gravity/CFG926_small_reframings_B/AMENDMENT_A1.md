# CFG926 AMENDMENT A1 (2026-10-20, POST HOC, written while building the script and BEFORE any run or number of this lane)

Label: POST-HOC CLARIFICATION of controls and corner bookkeeping. No class rule, threshold, target, input, bracket value or
posit is changed. `FROZEN_CRITERIA.md` (48a7a31ae) is not edited.

1. **K6e (R6 numerics).** The frozen text says "point-mass red vs point-mass blue law profiles give Δ_est = 0 (≤ 1e-6)".
   The n > 2 and n < 2 lens windows contain different B21 points, so a class-level Δ_est of two identical bias functions is
   not zero by construction. K6e is implemented as the scale-invariance statement it was meant to check: the point-mass law's
   β_full at M_round and at M_flat, evaluated on one common g_bar grid spanning the window, agree to ≤ 1e-6.
2. **MUTATE `geom` (R6).** For the same reason the class-level Δ_est cannot vanish under the mutate. The script decomposes
   Δ_est = Δ_samp + Δ_geom, with Δ_samp = F1[β_round at the n > 2 points] − F2[β_round at the n < 2 points] (window sampling
   of one common bias function) and Δ_geom = F2[β_round at the n < 2 points] − F2[β_flat at the n < 2 points] (the geometry
   effect at fixed g_bar). The mutate (flat class given the round model with the round class's M, R_e) must give
   Δ_geom = 0 (≤ 1e-12) and leave Δ_samp unchanged. The R6 class still uses Δ_est as frozen; Δ_samp and Δ_geom are reported.
3. **R4 dwarf condition part 2, alt footing.** `cfg827_results.json` carries the observed slope only for the canonical
   footing. On the alt footing s_obs ± se_obs is recomputed through CFG827's own code (its law, Υ_SFH at [M/H] −1.31, its
   weights and its fit) with the alt a0; K4 checks that this path reproduces the canonical slope in the JSON.
4. **Corner bookkeeping.** R5: corners = {log M* − 0.2, 0, + 0.2} × {bootstrap 16%, point estimate, 84%} (9 combinations;
   primary = point estimate at the central mass). R6: the round and flat masses are cornered independently
   ({−0.2, 0, +0.2}², 9 combinations) for each truncation variant. R4: 6 dwarf-fallback corners × 3 red-lens z_f × 3 cluster
   z_f per law.

κ = ½ FITTED; footings never pooled; not theory closed.
