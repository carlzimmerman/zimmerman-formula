# D9_uv_parent: covariant parent / UV completion of the cold sector

**Verdict: SCOPED NO-GO.** Any U(1)-dielectric parent that enforces the law's Gauss identity (phantom = cold medium) has a
dark field whose fastest speed obeys v_max² ≥ (1 + g/a₀)/Λ_LV. Λ_LV is the dark sector's Lorentz-violation factor. It is
exactly 1 for every Lorentz-invariant L(X, Y). So a Lorentz-invariant parent is superluminal (NG2, now for all L(X, Y)). A
foliated parent is causal only if Λ_LV ≥ 1 + g/a₀. That is 6.34e7 (canonical) / 5.25e7 (alt) at 1 AU. DSF-21's action escapes
because its field variable is the capped u, not g. Its price is that it does not enforce the Gauss identity at all.

No parent is established. A one-page exclusion map of all parent classes is in `MAP.md` (a deliverable; none existed).

Settings: κ = ½ FITTED (thermal κ = Z/4π is a postulate). Footings 9.36e-11 / 1.13e-10 m/s², never pooled. Cold energy is the
extra mass; no particle species. Not "theory closed". Nothing here says the data favour the framework over ΛCDM.

## Files and runs
- `FROZEN_CRITERIA.md`: committed alone first (bfb93eb61c). AMENDMENT A1 (POST-RESULT) committed alone (7bdd5fee57).
- `d9_uv_parent.py` (sympy + numpy; 1 s, 88 MB RSS). `OMP_NUM_THREADS=1 nice -n 10 python3 d9_uv_parent.py` writes
  `d9_uv_parent.out` and `d9_uv_parent_results.json`.
  - **Exit 1 by design.** Frozen checks: 9/12 PASS. U2, U4 and U5 FAIL as frozen (see below). Post-hoc A1 checks: 3/3 PASS.
  - The first run is kept as `*_firstrun_frozen.*`.
- `D9_MUTATE=1 ...` uses a linear D = E. U1, U3 and U6 then fail as required (`*_MUTATE.*`).

## Results
Scope: decoupling limit, fixed flat metric, medium rest frame, static uniform field E = g along ê, B = 0, high k.

1. **The frozen exact-speed formulas fail (U2, U4, U5 FAIL).** A parity-odd cross term (L_XY, or L_ac in the foliated case) mixes
   the two polarisations at k ⊥ ê. The formula v² = ε_⊥/ε_∥ is exact only when that term is zero.
2. **The bound survives the mixing (A1, post hoc).** The k ⊥ ê dispersion factorises exactly (V2, V4, residual 0):
   [(ε_∥s − N_⊥)(ε_⊥s − N_∥) − m²s] = 0, with s = v² and m real (m = E²L_XY, or 2E²L_ac).
   - At s = N_⊥/ε_∥ the bracket is −m²s ≤ 0, so the largest root is at least N_⊥/ε_∥.
   - 20 random numeric draws agree: min ratio 1.005 ≥ 1 (V5).
   - The law fixes ε_⊥/ε_∥ = 1 + g/a₀ (U3, exact). With Λ_LV ≡ ε_⊥/N_⊥, this gives v_max² ≥ (1 + g/a₀)/Λ_LV.
3. **Lorentz-invariant case.** Λ_LV = 1 for every L(X, Y) (U4a, exact), so v_max² ≥ 1 + g/a₀.
   - This closes AG6C's "L(X, Y) not explored" gap: NG2 holds for every L(X, Y).
   - Parity-odd terms only make it worse.
4. **Foliated case.** Causality needs Λ_LV ≥ 1 + g/a₀.
   - At 1 AU (g = 5.930e-3 m/s²) that is 6.3355e7 (canonical) / 5.2478e7 (alt). At g = a₀ it is 2.
   - The violation needed grows without bound in strong fields. Such a parent stays under NG1 and D-T (MAP rows 2, 3).
5. **DSF-21's A33 action escapes for a structural reason (P1–P4).** Its cone factor is 1 + 4ηu²/K, in the capped variable u.
   - P1 reproduces round-2 §4's reduction exactly. Over the full range, sup v² = (γ/η)(1 + 4ηa₀²/K) (P2).
   - At η = γ the excess is 2(L★a₀/c²)²: 1.19e-18 / 1.73e-18 at L★ = 24 pc and 2.07e-15 / 3.01e-15 at 1 kpc (P3).
   - In the same variable u, the U(1) factor is a₀/(a₀ − u), which diverges at the cap (P4).
6. **The price A33 pays (from the record, not computed here).**
   - It has a preferred foliation.
   - Its identity D·P = ς(ρ_c − ρ̄) is a matching, not a field equation (A33 §1, §7.3). By construction, this is also why NG1
     does not bite.
   - So ς(r) stays a free functional.
7. **A33, C1 and CFG938(′) are not one theory in different gauges.**
   - A33's P_T is physical: W changes under P → P + ∇×C (G1).
   - The record's propagating field DOF are 3 / 2 / 0 (G2, record-derived, low weight).
   - This answers option (b) at count level: CFG938′ cannot be A33 in another gauge.

## What this does not show
- **No sufficiency.** The bound is necessary only. I did not show that a foliated U(1) with Λ_LV ≥ 1 + g/a₀ is well posed or
  stable.
- **Not run.** A33's cone with gravity on non-static or evolving-P backgrounds. The physics of a slow dark polarisation.
- **Not computed: A33 plus a Route-A multiplier enforcing D·P = ρ_c − ρ̄.** This is the one open combination. A66 claims it works
  but never checked it.
- **WT-08 and WT-09 runs are not used.** They are uncommitted and belong to another session. CFG961 has no committed graded run.
- **No UV completion.** L★ and η/γ remain independent inputs (A57, A69).

## Record errors and gaps found
- AG6C README line 94 (also line 181) lists L(X, Y) as unexplored. NG2 does extend to it (V2): treat it as covered.
- This lane's own frozen U2/U4 claimed an exact speed. That is wrong with parity-odd terms, and the FAIL is disclosed.
