# LEDGER — append-only record of every door attempted

Read the last ~40 lines before starting a cycle. Never redo a door marked `CLOSED` or `CONFIRMED`.
Format is specified in `07_WRITING_RULES.md`. Newest entries at the bottom.

---

## SEEDED — what is already settled, do NOT redo

These come from committed, script-backed work in `real_research/reviews/`. Each has a script; re-run it if you
doubt it, but do not re-derive it from scratch.

| already done | verdict | script |
|---|---|---|
| a₀ from dark energy | a₀ = ½c√(Gρ_Λ) = 9.3614e-11 canonical; **the ½ is FITTED** | `mi_2Z_is_the_friedmann_root_2026.py` |
| ν(y) = √(1+1/y) reproduces Milgrom 1999 | yes, identically — it **is** his eqs 6–9 | corpus-wide |
| the crossover of any temperature functional | q_cross = 2/r, r free — class does NOT close | `mi_crossover_master_formula_2026.py` |
| combining Gρ_Λ with c²Λ to fix the coefficient | impossible — relabelling theorem | `mi_zeropoint_interference_audit_2026.py` |
| ρ_local instead of ρ_Λ | dead: 1076× too large in the solar neighbourhood | `mi_local_floor_target_2026.py` |
| standard local rates giving ¼ | none; closest 12.84% off | `mi_local_floor_target_2026.py` |
| Deser–Levin temperature from a computed response | reproduced to 1e-15…1e-17 at zero rotation | `mi_circular_dS_response_2026.py` |
| how much orbital motion breaks KMS | O((v/c)²) — **8.6e-07 at galactic speeds** | `mi_circular_dS_response_2026.py` |
| the auxiliary-field localization + exact circular orbit | localization exact; suppression verdict hinges entirely on ω_c | `mi_auxfield_exact_circular_2026.py` |
| is ω_c fixed? | **no — free fifth constant**, committed window 1.78–2.21e-14 | `mi_kernel_axis_separation_omegac_2026.py` |
| equilibrium dS linear response → MOND | no: KMS ⇒ ρ(ω) ≥ 0 ⇒ δm > 0, anti-MOND | `linear_response_anti_mond_proof.md` |

## WITHDRAWN — never re-assert (see `04_FRAMEWORK_FACTS.md` for the full list)

- "the dS–Unruh mechanism cannot yield a smaller coefficient" — it can, q_cross = 2/r
- "the two MOND limits jointly force q_cross = 2" — five scale-free examples, not a theorem
- "a quadrature torque obstructs circular orbits for any kernel" — kernel-shape dependent
- "S(Ω)=0 on an interval ⇒ K ∝ δ" — refuted by K = b·J₀(bs)
- "1/C inside 3.8e5–3.8e7 cross-validates two routes" — same (c/v)² twice
- "2Z carries a √π no normalisation supplies" — its √π **is** the Friedmann 8π/3's

## DO NOT REPEAT (from the qwen RESEARCH_LOG, still valid)

- do not retry the tn07–tn09 embedding-space Z² computation (branch-cut bugs; tn10 supersedes)
- do not re-verify ν(y) = √(1+1/y) against Milgrom 1999 — done at multiple y
- do not re-derive a₀ from the dark energy density — done
- do not use h_spectral(x) from ρ via a Stieltjes integral as if it equalled K(x) — it does not (tn12)

---

# ENTRIES

<!-- append below this line, newest last -->

## 2026-08-07 — overnight sweep, ~500 checks, all re-run before commit   STATUS: see 04_FRAMEWORK_FACTS.md
Nine theorems added, four claims withdrawn (including two of mine). Full table in FRAMEWORK_FACTS §2026-08-07.
DO NOT REDO: admissibility bounds on r (sup = +∞, four routes); the CTP Gaussian order (a₀ = 0 exactly); the
cubic tadpole (structure yes, coefficient r < 1 and magnitude 1.27e-42 — both dead); composite operators,
squeezed states, two-level/N-level inversion, super-ohmic equilibrium, linear-dressing KMS, the Ward identity,
the geometric lock (priced p = 0.480), the disformal completion (photon decay).
NEXT: the TASKS/ queue. M-tasks are the uncovered open items; W-tasks are unrelated.
