# CFG340 FROZEN CRITERIA: does the pre-reionisation cold-share candidate break the big systems?

Written and committed before any CFG340 number is computed. κ = ½ is FITTED and fixed. The cold component's mass is still required; no dark-matter particle is added. Nothing here says the theory is closed.

## The candidate (from CFG338/CFG339, unchanged)
- Cold mass M_c = R · M_b,now / f_b, with f_b = 0.157126 and R = original baryons / present baryons.
- Bookkeeping: CFG4 T5 max, g = g_N + max(g_law − g_N, g_cold), g_cold = (1 − f_b) G M_cold(<r) / r².
- Profile P1: M_cold(<r) = M_c · min(r / r_f, 1), r_f = [3 M_c / (4π · 18π² · ρ_m0 (1 + z_f)³)]^(1/3), ρ_m0 = 2.7754e11 (ω_b + ω_c) M☉/Mpc³, ω_b + ω_c = 0.14237 (as CFG336/338).
- z_f: the CFG336 a-priori class for non-ultra-faint systems, **z_f = 3 (decision)**; z_f = 2 and 4 reported. No other value is tried.
- Kernel ν_mono; both footings (9.3603e-11 / 1.1312e-10 m/s²).

## Populations, harnesses, B baseline and the committed pass criterion
Each harness is exec'd read-only from committed source (no other lane's file is written; nothing is downloaded).

| id | population | harness / data | B baseline | pass criterion (committed) |
|---|---|---|---|---|
| S1 | SPARC log M★ ≥ 10 (n 61) | CFG45 P3 rows (SPARC_Lelli2016c.mrt via read_master) + CFG39/CFG4 rotmod RAR rms | CFG45 S: 100% with d log v < 0.03; CFG39 Δrms +0.0009 | A3: ≥ 90% with d log v(R_HI) < 0.03 **and** Δrms (all-point RAR, Υ 0.61, canonical) < 0.005 dex vs the law |
| S2 | SPARC dwarfs log M★ < 10 (n 110) | as S1 | CFG45 S: 100% | as S1 |
| X1 | X-ray ellipticals (7) | CFG45 P6 (xray_gal; CFG36 data) | CFG45 S: z +1.04 (can.) | \|z\| < 2, z = mean offset / CFG45's tot error |
| K1 | KiDS-1000 isolated lenses (4 bins) | CFG4_switch K3 block (FP1 E machinery, FP20 exact projector, M_b profiled) | law χ² (B's switch is off in these bins, CFG39): ν_mono 162.605 / 154.758 | Δχ² ≤ +9 vs the law (CFG4_switch KIDS_TOL) |
| C1 | X-COP clusters (12) | CFG4_clusters cluster_table rows (corrected audit) | identity reading 0.946 ± 0.080 | median \|M_pred/M_HSE − 1\| ≤ 0.20 (CFG4_clusters H2) |
| (rep.) | SLUGGS h50 | CFG45 P5 | B red (z +3.3) | reported only, not in the decision |

Per-population mass entering M_c: SPARC 0.61 L36 + 1.33 M_HI (CFG45); X-ray the stellar mass Υ_K L_K (CFG45); KiDS the per-bin profiled M_b; X-COP the audited M_b at the outermost audited radius (declared; an under-estimate of the total baryons, so R_max for clusters is if anything over-estimated).

## Method
- R is applied to one population at a time (all others unaffected).
- **R_max** = the largest R such that the criterion holds for every R in [1, R_max] on both footings (contiguous from R = 1), by bisection in log R on [0, 3] dex to 0.005 dex. If the criterion fails at R = 1, R_max = "fails at R = 1". If it holds at 10³, R_max ≥ 1000. No other scan.
- For S1/S2 the rms clause is canonical only (as committed in CFG39); A3 uses the canonical edge as CFG45 does, and both footings' a0 for the law.

## R_plausible (a-priori, frozen now; upper end is used in the decision)
- S1 SPARC log M★ ≥ 10: R 1–3, **upper 3** (PROVISIONAL, from memory: massive spirals' effective yields near the true yield).
- S2 SPARC dwarfs: the record's CFG317 R_ind for gas-rich LV field dwarfs, 10^0.77 = 5.9 nominal, **upper 10^1.09 = 12.3** (yield +0.1). Conservative proxy: SPARC dwarfs are more massive than the LV field dwarfs.
- X1 X-ray ellipticals: R 1–3, **upper 3** (PROVISIONAL; CFG317's recalled against-interest note: [Z/H] ≈ 0 to +0.3 ⇒ R_ind ≈ 1–2).
- K1 KiDS lenses (log M★ 10–11): R 1–3, **upper 3** (PROVISIONAL).
- C1 X-COP clusters: R 1–1.2, **upper 1.2** (PROVISIONAL: clusters are near-closed boxes). Reported alongside: the record's own f_b / f_bar,X-COP (CFG4_clusters K1, 0.149 at 0.8 R500) ≈ 1.05.

## Decision (z_f = 3, both footings)
- **PASS:** R_max ≥ 2 × R_plausible(upper) for every decision population (S1, S2, X1, K1, C1).
- **MARGINAL:** R_max ≥ R_plausible(upper) for all, but < 2× for at least one.
- **FAIL:** R_max < R_plausible(upper) for any population.

## Controls
- **C0 (law reproduces B's committed numbers):** SPARC law rms reproduces CFG39 rms0 (1e-9); KiDS law χ² reproduces CFG4_switch K3 ν_mono base (1e-6); X-ray law z reproduces CFG45 XRAY |L (1e-9); X-COP at R = 1 reproduces the committed identity median 0.9457 (1e-6; exact only where r_out ≥ r_f, disclosed per cluster).
- **R = 1 row:** each population's statistic at R = 1 is reported next to B's baseline; B's pass must hold at R = 1 for the bisection to be meaningful.
- **MUTATE** (CFG340_MUTATE=1, outputs *_MUTATE): R = 30 applied to all SPARC galaxies must be flagged failing (A3 or rms clause).

## Lean
The decisive R_max vs R_plausible inequalities, as rational bounds (R_max rounded down to 0.01), certified in Mathlib, no sorry.

## Disclosure
Before freezing, a back-of-envelope estimate (no code run) suggested X-COP R_max ≈ 1.3 under the 20% criterion, because the identity reading already sits at 0.946 and every unit of R adds ≈ 5.4 M_b. If confirmed, PASS is unreachable for clusters (needs 2.4) and the verdict is at best MARGINAL. The criteria are kept as specified.
