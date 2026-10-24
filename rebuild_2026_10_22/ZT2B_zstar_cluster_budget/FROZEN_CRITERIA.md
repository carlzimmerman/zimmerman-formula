# ZT2B_zstar_cluster_budget — FROZEN CRITERIA (committed alone, before any script or number)

Z-T2 (ZT_zstar_tests, 98dbd0a5f2) left Z★'s cluster core red: T3 A_MID 1.41–1.71 (Z +2.7…+4.1 with systematics (e)). Z-T2's
free excess already sits on CFG930's native NFW (collapse-time concentration), so a "relaxed free dust" variant would duplicate
it. This lane asks the sharper question: **is the core failure a profile problem or a budget problem?** κ = ½ FITTED. Footings
never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework. One thread,
< 1 GB, about 4 min.

## Lemma used (stated, checked numerically)

For a fixed added mass m, ΔΣ(R) = M̄_2D(<R)/(πR²) − Σ(R) is largest at every R when m sits at the centre: then it adds
m/(πR²) at every R outside its core, and any spread-out placement adds at most that. So a central mass is an upper bound on
the MID lift any profile of the same mass can give. Check KL: for a 1e14 M☉ test mass, the central Plummer (r_c = 10 kpc) gives
ΔΣ at the MID bins ≥ that of the NFW debris profile of the same mass, at every MID bin.

## Modes (Z-T2's script exec'd from its committed source; only the free-excess profile is patched)

- **NFW**: unchanged Z-T2 (control). Check K-REP: every A and s_tot reproduces Z-T2's committed results JSON to ≤ 1e-9.
- **PM**: Z★'s own free excess E_free = f_s M_b,own − M_ph(R_own) (rich clusters only) as a central Plummer, r_c = 10 kpc; held
  dust stays at the law (the design). Non-rich clusters unchanged (no free excess exists).
- **ALLPM** (absolute bound over any arrangement of Z★'s total dust f_s M_b,own, held or free): baryons + the whole supply S
  as a central Plummer.

All of Z-T2's cells: both baselines (C*_own primary, C0+e reported), R_own ∈ {200ρ_c, 18π²ρ̄_m}, r_s ∈ {cap, closed form}, both
footings, both h. Statistics, data, systematics (e), terciles, projector, reduced shear: Z-T2's, unchanged.

## Classes (per footing × R_own convention, C*_own; must agree over both h and both r_s definitions, else SPLIT)

- **BUDGET NO-GO**: T3 A_MID > 1 + 2 s_tot under PM in every sub-cell. No arrangement of the free excess can fix the core while
  the held dust stays at the law.
- **PROFILE-LIMITED**: T3 MID passes under PM in every sub-cell (a more concentrated free-dust profile than CFG930's could
  fix it; the concentration needed is reported).
- Reported for every cell: T2 and T3 A_MID under NFW / PM / ALLPM; the free-excess fraction of the law mass at 1 Mpc; ALLPM's
  class by the same rule (whether even the total cosmic-share supply, ignoring the hold, can reach the core).
OUTER and INNER under PM/ALLPM are reported only (a central mass is a bound, not a model).

## Checks and `--mutate`

K-REP (above), KL (lemma), Z-T2's own K0–K5 as they run inside each mode, KR (RSS < 1 GB). `--mutate`: Z-T2's own mutate
(cross shear as data) → K0 fails (exit 1). Outputs per mode `zt2b_<mode>{,_MUTATE}.out`, `_results{,_MUTATE}.json`, plus
`zt2b_summary.json`. Post-result changes go in a dated AMENDMENT.
