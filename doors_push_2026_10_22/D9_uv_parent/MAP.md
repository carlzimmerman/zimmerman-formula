# Map: which covariant parents of the cold sector are excluded, and by what (2026-10-22)

No such one-page map existed in the record; the closest are AG6C §6, CFG941's repair table and DSF-21 THEORY §7.
Status words are the record's own. κ = ½ FITTED. Not "theory closed". "Established parent": none.

## The fork that organises everything

Does the parent **enforce** "the phantom is the cold medium's own density" (a Gauss-type constraint ∇·P = ρ_c − ρ̄)?
- **Yes** → the medium is the phantom, so D-T (no linear self-gravity), the satellite hover and NG1 (positivity at field
  nulls) apply. The tether's propagation then fails in one of three ways: superluminal (Lorentz-invariant U(1)), a huge
  dark-sector Lorentz violation (foliated U(1), this lane), or an instantaneous elliptic constraint that is ill-posed on FRW (CFG938).
- **No** → DSF-21's A33 action: healthy and causal, but the identification is only a matching on a solution, so ς(r) is a free
  functional and the cold medium is not derived to be the phantom. It is an EFT, not a UV completion.

## Class table

| # | parent class | status | what excludes or limits it | file |
|---|---|---|---|---|
| 1 | Lorentz-invariant U(1) dielectric, Gauss law enforced (AG6C C1) | PARTIAL | NG2: v² = 1 + g/a₀ (superluminal); H3: ill-posed on 102/2000 general (E, B) backgrounds; NG1; D-T | `argon_push/AG6C_relativistic_completion/README.md` §2–§6 |
| 1′ | same, any L(X, Y) incl. parity-odd | NO-GO (new) | v_max² ≥ 1 + g/a₀, equality iff L_XY = 0 (V2) | this lane, `d9_uv_parent.out` V2 |
| 2 | foliated U(1) dielectric L(E², B², E·B), Gauss law enforced | SCOPED NO-GO (new) | causal only if the dark-sector Lorentz-violation factor Λ_LV ≡ ε_⊥/N_⊥ ≥ 1 + g/a₀: 6.34e7 (canonical) / 5.25e7 (alt) at 1 AU; still under NG1 and D-T | this lane, V4, U6 |
| 3 | elliptic-constraint fluid parent CFG938 (labels + χ, λ) | CONDITIONAL | D-T: c₂ = 1 forced, no linear self-gravity (CFG941); hover Δa/g_host = 1.02–1.11 (CFG941/945, Theorem S); Hadamard ill-posed on FRW, Re σ = c²k²/3H (WT-02, independent check CFG961 criteria + A1 only, no graded run committed); "c_T = c structural" refuted (WT-02 (e); `sol61_push/cold_covariant_audit_2026_10_20/RESULT.md`); growth a^0.694 | `campaign_fresh_gravity/CFG938_*`, `CFG941_*`, `what_is_time/WT-02_preferred_time/README.md` |
| 4 | CFG938 repairs R1, R2, R3n, R3ℓ | NOT REPAIRABLE | D-T | `CFG941_self_gravity_repair/README.md` |
| 4′ | gated tether R3θ and its cures | NO CURE | Theorem G: no local L(θ, u) with law + growth + no ghost + slip | `CFG944_gated_tether_ghost_cure/README.md` |
| 4″ | per-label tether H1 → labelled-domain theory | RESOLVED-WITH-COST / LDT CONDITIONAL / SMOKE PARTIAL | non-variational label sector; energy not conserved at label events | `CFG945_*`, `CFG950_*`, `CFG952_*` |
| 4‴ | CFG938′ (intrinsic leaf Laplacian, V1/V2) and c_T = c stiffness | OPEN (criteria only; runs uncommitted) | — | `what_is_time/WT-08_repaired_parent/`, `WT-09_ct_stiffness/` |
| 5 | option 2: cold energy = ordinary dust, law from a separate local sector | NO-GO | Theorem T-O2: a local second-order no-EFE field cannot supply the deep law; D-T′ | `CFG946_option2_phantom_not_cold/README.md` |
| 6 | option 3: non-local causal parent of the class-A engine | NO-GO (exact parenthood) | T-M (relocation not conserved), T-R (RMIN kills law in 128/175 SPARC), T-X (host EFE); retarded kernels have no action | `CFG947_option3_nonlocal_parent/README.md` |
| 7 | source-changing theory SCT-M / SCT-Q | CONDITIONAL / INCONSISTENT | energy closes only via a non-dynamical internal energy; SCT-Q has host EFE (z −3.48/−3.79) | `CFG953_source_changing_theory/README.md` |
| 8 | kinetic theory of relaxing cold dust | NO KINETIC PARENT (post hoc; frozen: unclassified) | law state neither selected nor kept (Bonnor–Ebert/Antonov) | `CFG955_kinetic_parent/README.md` |
| 9 | P as exact Lagrangian displacement (shell crossing) | S4 NOT DERIVABLE | free population needs a coupling the action lacks | `CFG939_lagrangian_displacement_shell_crossing/README.md` |
| 10 | Blanchet–Le Tiec dipolar fluid (AG6C C2) | excluded (provisional) | Hamiltonian linear in p_x (Ostrogradsky-type) | AG6C README §4 |
| 11 | finite-state lattice medium as UV of κ and L★ | NO | q = 2 fixed by the law; L★ fixes the coupling only; κ never enters Z; two independent UV inputs | `deepseek_push/DS_FINAL_2026_10_21/A57_uv_completion/report.md` |
| 12 | DSF-21 foliated Proca action A33 (EFT) | HEALTHY EFT, not UV | 5 DOF (A54, A68; Route C dead), no ghost for β > 0, η > 0, γ > 0; tensor mass harmless (A39); η/γ unfixed (A69); cone bounded, sup v² = (γ/η)(1 + 4ηa₀²/K), excess ≤ 3.0e-15 at η = γ (round-2 §4; P2–P3 here); Gauss identification NOT enforced (A33 §1, §7.3) | `A33_master_action/MASTER_ACTION.md`, `A68_bracket_algebra/report.md`, `core_open_problems_round2_2026_10_20/03_relativity/report.md` §4 |
| 12′ | A33 + Route-A multiplier enforcing D·P = ρ_c − ρ̄ | OPEN | A66's "works" is unverified (A68 B9: not checked); would it inherit D-T / NG1? | `A66_dof_repair/report.md` (erratum), A68 §1.5 |

Field-content check (G2, record-derived): propagating non-metric field DOF on a static flat background are 3 (A33), 2 (C1),
0 (CFG938/CFG938′). No two of these parents are one theory in different gauges; A33's P_T is physical (G1), CFG938's is relabelling.
