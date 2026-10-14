# CFG782 FROZEN CRITERIA: the untether-on-unbinding selector, derived first (photo-evaporation at reionization)

Committed alone, before any script or number. 2026-10-14. Block CFG780–789.

## Why this lane comes first
- Three read-only agents (`THEORY_PUSH_2026-10-14/` A, B, C) converged on one mechanism: **untether-on-unbinding**. Cold energy
  that loses its tether's binding (CFG749: tethered cold energy is bound only by baryons) becomes free collisionless mass. It
  never re-tethers (no capture channel: CFG744, CFG760–762).
- Agent A found that a fossil free halo of 5.364 (R_ind − 1) M_b would close the UFDs. It breaks the classicals, LV field and
  SPARC **unless a selector is derived and frozen before** the fossil test.
- This lane is that selector. CFG784 (the fossil test) uses it unchanged.

## Derived selector (no tuned constant)
- **Physics.** At reionization the IGM is photo-heated to T_IGM ≈ 1–2 × 10⁴ K, a measured range (Lyα forest, z ≈ 5–6).
  Gas in a system whose virial temperature is below T_IGM escapes on its sound-crossing time t_sc = r/c_s.
- **"Sudden" relative to the carrier.** That loss is sudden for the cold energy because t_sc < t_orb = 2πr/V whenever
  c_s > V/2π. This holds for every V < 100 km/s, so photo-evaporation always counts as sudden.
- **The system's own velocity.** Use the framework's flat velocity of its ORIGINAL baryons: V_init = (G M_init a0)^{1/4},
  with M_init = R_ind × M_b,now.
- **Retention condition.** T_vir = μ m_p V²/2k > T_IGM, i.e. V_init > V_th = √2 c_s with c_s = √(k T_IGM/(μ m_p)) and
  μ = 0.59. That gives V_th = 16.9 / 23.9 km/s at T_IGM = 1 / 2 × 10⁴ K.
- **Flag.** SUDDEN (fossil free cold energy) iff V_init < V_th; RETAINED otherwise.
- **Primary:** T_IGM = 1.5 × 10⁴ K (V_th = 20.7 km/s), canonical a0. The ends of the range and the alt footing are
  brackets.
- **Inputs.** R_ind is CFG317's committed leaky-box per-object value (nominal yield −0.2) for MW UFDs and classicals. Other
  systems use CFG317's own log R_ind – log M_b,now relation (OLS on its per-object table, fitted inside this script, reported).
  M_b,now comes from the record's tables: LVD 2 L_V + HI; SPARC V_bar² R/G at the last point.

## Tests (the selector's own gates)
- **S1 (must flag the targets):** ≥ 90% of MW UFDs (M_V > −7.7) flagged SUDDEN.
- **S2 (must spare the passing systems):** ≤ 10% of each of {MW classicals, M31 dSphs, LV field dwarfs, SPARC} flagged
  SUDDEN at the primary setting.
- **Verdict:** SELECTOR VIABLE iff S1 and S2 pass; BORDERLINE if S2 fails only at a bracket end; DEAD otherwise.
- Report every flagged non-UFD by name, with V_init.

## Controls
- K1: c_s(1.5e4 K, μ 0.59) = 14.6 km/s, to 1e-3.
- K2: V_init for M_init = 10⁶ M☉ (canonical) = (G M a0)^{1/4} = 10.4 km/s, to 1e-3.

## MUTATE (CFG782_MUTATE=1)
R_ind ≡ 1 (current baryons only). The flag set must change. Expected: nearly everything small flagged, so S2 fails. This
tests that the original-baryon input is load-bearing.

## Hand estimate
- UFDs: M_init ~ 10⁵–10⁷ ⇒ V_init 6–19 km/s ⇒ all SUDDEN (S1 PASS).
- Classicals: Fornax ~40 km/s RETAINED; Draco/UMi ~19 km/s BORDERLINE.
- LV field (gas-rich) and SPARC: mostly ≥ 25 km/s RETAINED.
- Expected: VIABLE or BORDERLINE (the low-mass classicals are the risk).

## Machine
Runs after T1x (seconds). κ fitted; not theory closed. This is a postulate's selector, not a derivation of the two populations.
