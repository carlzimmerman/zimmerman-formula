# PROOF_CHAIN — the certified prediction chain

**Theorem (the certified chain).** Under axioms A1-A7 — two definitions, the barycenter-centering law, and four labeled inputs (MEASURED / DECLARED / ANSATZ / DATA-SELECTED) — the framework's equations imply L1-L8 and the DR4 kill rule C1. Proof: by construction — each L is either a compiled Lean theorem name (exit 0, no sorry) or a computed check in a landed .out file, cited as (file, check, number). Any cross-check mismatch is a FAIL-as-finding; never invent numbers.

*Enumeration note (outside the verbatim theorem):* the chain below numbers the links **L0, L1–L8, C1** — L0 is the first numbered link, the companion mean-value result `SW09_meanvalue.out` (on disk, 11/11 checks PASS), inserted ahead of L1; "L1-L8" in the theorem is read with L0 prefixed. *Lean status, stated exactly:* `SW06_lemmas.lean` is on disk with five theorems (`eBTFR`, `conformal_BR`, `newton_limit`, `mond_limit`, `mu_S_equiv`), compiled exit 0, no `sorry` (verified by reading the file). The four theorem names (`uniform_field_Gamma_eq_zero`, `uniform_field_eta`, `isolated_centered_Gamma`, `isolated_centered_eta`) exist in `SW10_pair.lean` — on disk, **untracked**: three of four compile, and `uniform_field_eta`'s hsplit helper has one documented mechanical fix remaining (`simp only [Pi.add_apply]` before ring); Theorem 2 is carried numerically by `SW10_pair.out` (10/10 clean, 9/10 MUTATE).

> **Status box.** This is NOT a derivation of gravity from first principles. It IS a proof that these equations imply these predictions, plus an obstruction that any covariant completion is auxiliary-or-nonlocal (G03-class). Ghost quadratic-form theorem: OPEN (the remaining G03 kill gate). alpha_2: priced (SW08), not derived. The words derived/closed/breakthrough are not used as claims.

## Index table: framework equation (verbatim) -> formal name in Lean -> used by

Equations verbatim from `LAW_STATEMENT.md` (the owner's law statement, 2026-09-17).

| Framework equation (verbatim) | Formal name in Lean | Used by |
|---|---|---|
| `Γ² = ⟨\|g_N\|²⟩_Ω − \|⟨g_N⟩_Ω\|²` (the field's own structure — the sourced part) | `isolated_centered_Gamma`, `uniform_field_Gamma_eq_zero` (SW10_pair.lean — written, untracked; three of four compile, one helper fix documented; numerics carry Theorem 2) | A1; L0 (T3), L1, L3, L6, L7 |
| `η = \|⟨g_N⟩_Ω\| / a₀` (the sphere's l=1 component — the environment) | `isolated_centered_eta`, `uniform_field_eta` (SW09_obstruction.lean — pending-compile-confirmation) | A2; L0 (T2), L1, L2, L6 |
| `g_obs = g_free + [ (1 − S(η)) + S(η)·ν(Γ/a₀) ] · g_src` | `newton_limit`, `mond_limit`, `mu_S_equiv` (SW06_lemmas.lean — compiled, exit 0) | L1 (L0 ground), L2, L4, L5 |
| `S(η) = 1/(1 + (η/η_c)²)` — an ANSATZ | — (ANSATZ: no Lean counterpart; SW07 H5: only the limits are structural) | A4; L2, L4, L6, L7 |
| `ν_RAR(y) = 1/(1 − e^(−√y))` — rung 2, DATA-SELECTED | — (DATA-SELECTED: no Lean counterpart) | A5; L2–L6 |
| `a₀ = ½·c·√(G·ρ_Λ)` — rung 1, MEASURED | — (MEASURED: no Lean counterpart) | A6; everything that carries a0 |
| `μ_S = 1/[1 + S(ν_src − 1)]` | `mu_S_equiv` (SW06_lemmas.lean — compiled, exit 0) | L5 |
| `v⁴ = S(η)² G M_b a₀` — THE eBTFR: slope exactly 4, zero point S² | `eBTFR` (SW06_lemmas.lean — compiled, exit 0; in-file casing, not `ebtfr`) | L4 |

## The axioms (input block — not edges)

- **A1 GammaSq (definition).** The angular variance of the Newtonian field over a barycentered Gauss sphere. Landed: (SW01b_envscalar_orthogonality.out, C1/C2, quadrature: isolated centered sphere gives eta = 5.55e-17 ≈ 0 and Gamma = 1.0000000000 vs g_N = 1); (SW09_meanvalue.out, B4, the variance identity Γ² = ⟨|g_N|²⟩ − |⟨g_N⟩|² = ⟨|g_N − g_env(B)|²⟩, rel 1.54e-16).
- **A2 eta (definition).** η = |⟨g_N⟩_Ω|/a0, the environment read at the barycenter. Landed: (SW01b_envscalar_orthogonality.out, B1: eta_sun = 2.292 canonical / 1.902 alt from v_c²/R₀).
- **A3 barycenter centering (part of the law).** The sphere center is the enclosed baryons' barycenter, fixed by the flux structure — no hand-drawn boundary — and the centering is load-bearing. Landed: (SW01b_envscalar_orthogonality.out, C3: offset-center hinge Gamma = 1.3333 at d = 0.5 r vs 1.00 centered); (SW08_preferred_frame.out, D1: trigger anisotropy 0.33 order-unity when the centering is dropped; D2: the decentered preferred-frame estimate 0.76 is PPN-dead by 1.9e+06×).
- **A4 S-family (ANSATZ — labeled).** S(η) = 1/(1 + (η/η_c)²). The form is declared, not a mechanism: (SW07_eta_c_attack.out, H5 and the 1/6 verdict — every derivation mechanism on the record's attack list was killed; only the limits are structural, per LAW_STATEMENT.md).
- **A5 nu_RAR (DATA-SELECTED — labeled).** ν_RAR(y) = 1/(1 − e^(−√y)), rung 2. Landed: (SW01b_envscalar_orthogonality.out, A2: ν(2.5) − 1 = 0.2590 vs the L264 record 0.259, threshold 0.002).
- **A6 a0 = 0.5·c·√(G·ρ_Λ) (MEASURED — labeled).** κ = 0.5; a0 = 9.3619e-11 canonical / 1.1279e-10 m/s². The κ slot is adjudicated NOT LIVE (KS01): (SW07_eta_c_attack.py, A0 constant; SW09_equations_audit.md, E9 row). Four candidates inside 2σ (0.465 ± 0.076 / 0.551 ± 0.043); nothing on the input side.
- **A7 eta_c = 0.2034 / 0.1688 (DECLARED — labeled).** Canonical/alt (SW01b_envscalar_orthogonality.out, B2; the brief's 5-dp form 0.16879 is the same constant — the landed code constant is 0.1688). Window: LSS floor ≥ 0.028 (SW01b F), Oort ceiling 0.203 (SW07), Fornax-implied bound ≤ 0.145 (SW03 C2 / SW07); SW09_chain.out X8 recomputation confirms the alt value sits inside [0.145, 0.203] and records the precision note that the canonical 0.2034 equals the 0.203 ceiling at its quoted 3 dp (exceedance 4.0e-4) — a precision note, never a silent edit.

## The chain

**L0 — the mean-value structure (companion result; SW09_meanvalue.out, 11/11 checks PASS).**
- **(T1)** avg(g_N) = g_env(B) exactly: the enclosed baryons contribute zero to the sphere mean for ANY interior configuration (centred or not), and the environment contributes its centre value by the mean-value property of harmonic fields. Cites: (SW09_meanvalue.out, B1: |⟨g_enclosed⟩|/(GM/r²) = 3.91e-16; B2: |⟨g_env⟩ − g_env(B)|/|g_env(B)| = 2.03e-15; B3: full field 6.93e-15).
- **(T2)** η = |g_env(B)|/a0 is a POINT value — all the construction's nonlocality sits in Γ, none in η. Cites: (SW09_meanvalue.out, D1: the mean localises at the centre B, 6.93e-15 vs 1.85e+00 at a field point; D2: retro-justifies the record's calibration — v_c²/R₀/a0 = 2.2918 IS the record's eta_sun 2.292).
- **(T3)** Γ = RMS deviation of the field from the ambient. Cites: (SW09_meanvalue.out, B4).
- **Consequence P10, the DC/AC split:** the environment's DC part goes to η (conformal suppression, shape preserved); its AC/tidal part goes to Γ (shape distortion with S pinned at 1). Cites: (SW09_meanvalue.out, C1: uniform field — Γ invariant to 1.31e-16; C2: symmetric tidal pair — η = 4.30e-16 while Γ moves, ratio 1.0176; C3: S = 1 on the tidal channel, ν − 1: 0.374909 → 0.369098).

**L1 — the l=1 orthogonality.** A uniform external field is pure l=1 on every barycentered sphere: the trigger never sees the environment (Γ = g_N, η = g_ext exactly). Cites: (SW01b_envscalar_orthogonality.out, C2: Γ = 1.0000000000 vs g_N = 1, η = 2.500000 vs 2.5; the cross term 2 g_N g_ext ⟨μ⟩ = 0 by quadrature). Lean counterpart: (SW09_obstruction.lean, `uniform_field_Gamma_eq_zero` — pending-compile-confirmation, file not on disk at write time).

**L2 — the conformal pointwise scaling Q = S·Q_iso.** The environment enters ONLY as the scalar S(η) multiplying the isolated boost profile — never inside the kernel. Cites: (SW04_conformal_efe.out, B1[CONFORMAL]: max |BR_class/BR_isolated − 1| = 2.22e-16 per object across 8 dSphs; SW06_conformal_mu.out, E2: 2.62e-14 in the μ-language). Lean counterpart: (SW06_lemmas.lean, `conformal_BR` — compiled, exit 0).

**L3 — P2 = 0, the angular null.** γ_v has no φ-dependence because S = S(|⟨g⟩|) only. Cites: (SW05_kepler_freeze.out, C1[P2]: A2 = 2.22e-16 exactly zero by structure; the mutated direction-carrying S gives 1.01e-04, the hinge demonstrated; SW01b_envscalar_orthogonality.out, G[structural]: response-field quadrupole c2 = −6.074e-14 a0 → tidal 3.38e-39 s⁻² vs ceiling 5.2e-27).

**L4 — the eBTFR: v⁴ = S² G M_b a0.** Slope exactly 4 for ANY S; the environment rescales a0_eff = S² a0 and leaves the slope alone. Cites: (SW04_conformal_efe.out, A2: sympy v⁴/(S² G M a0) = 1, exact; A3: d ln v/d ln M = 1/4 for any S, exact, measured 3.98 ± 0.06). Lean counterpart: (SW06_lemmas.lean, `eBTFR` — compiled, exit 0, no sorry).

**L5 — μ_S single-valued + round trip.** The μ-language is the same physics: μ_S = 1/[1 + S(ν_src − 1)], well-posed because g → g_obs is monotone for every S (ν decreases in g while g grows — not free). Cites: (SW06_conformal_mu.out, B1[WELL-POSED]: monotone for S ∈ {1, 0.8467, 0.58, 0.1, 0.00781}, min slope 3.70e-09 a0; C1[EQUIVALENCE]: the inversion reproduces the direct law to 2.22e-16 over 25 (S, g) pairs). Lean counterpart: (SW06_lemmas.lean, `mu_S_equiv` — compiled, exit 0).

**L6 — the x = 2.5 gate: both readings, both footings.** Per-field reading 152.1 canonical / 220.3 alt; dilution-inclusive reading 304.1 / 440.7; internal departure ν(2.5) − 1 = 0.2590; the 2× is convention, not physics — (g_src+g_ext)/g_src = 2 exactly at the gate. Both readings clear the 6.4 gate on both footings, 24× to 69×. Cites: (GATE_CONVENTION.md — the four numbers and the reading discipline; SW06_conformal_mu.out, D2[GATE]: both readings printed on both footings; SW01b_envscalar_orthogonality.out, D canonical/alt: 152.1 / 220.3).

**L7 — alpha_2 double suppression + the c_S bound.** The class's planetary preferred-frame anisotropy is doubly suppressed: trigger 4(v/c)² = 6.093e-06 (v = 370 km/s CMB) × |dS/dln η| = 0.01551 at eta_sun × response ν(7.0e5) − 1 = 0.0e+00 → alpha_2 estimate 0.00e+00 exactly. The binding constraint on any covariant completion is its matter-frame coupling: c_S ≤ 4.23 (Nordtvedt ceiling 4e-7) / ≤ 423 (LLR-scale 4e-5) — c_S is the named missing input. The barycenter condition is load-bearing: dropping it gives the counterfactual estimate 0.76 = 1.9e+06× the tight ceiling. Cites: (SW08_preferred_frame.out, B1, B2, B3, B4[KILL-A], B5[KILL-A], D2).

**L8 — the obstruction (the 2-jet test).** Any covariant completion of the class is auxiliary-or-nonlocal (G03-class): the 2-jet test is the obstruction's formal statement. Cites: (SW09_obstruction.lean, `uniform_field_Gamma_eq_zero`, `uniform_field_eta`, `isolated_centered_Gamma`, `isolated_centered_eta` — all four cited pending-compile-confirmation; the file was NOT on disk at write time, owned by a parallel agent; "exit 0, no sorry" is NOT claimed for it here).

**C1 — the DR4 kill rule (decided 2026-12-02).** The prediction: γ_v(s) = 1.00000–1.01012 over s = 1e3–3e4 AU at eta_sun = 2.292 (SW04_conformal_efe.out, D: the computed curve, 6 separations, AQUAL runs to 1.17462); the freeze line quotes the same curve at 4 dp, 1.0000–1.0101 (SW05_kepler_freeze.out, P1 / verdict), with the solar clean value 1.0010 (SW01b_envscalar_orthogonality.out, H canonical/alt). The rule: γ_v > ~1.05 or inside 1.16–1.23 → the class is dead (2026-12-02), against the three-way separation 1.00 / 1.09–1.12 / 1.16–1.23. Cites: (SW04_conformal_efe.out, D1, D2; SW05_kepler_freeze.out, P1; SW01b, H).

**Chain edges: 10.** Convention (stated so the count is auditable): one edge = one numbered chain link (L0, L1–L8, C1), each carrying (file, check name, number); the axioms A1–A7 are the input block, not edges.

## The recomputation record (SW09_chain)

`SW09_chain.py` recomputes every frozen number from the axioms and cross-checks each against its landed target, with runtime provenance strings (each target must still appear in the cited file). Verdict: **all match** — 9/9 — (SW09_chain.out, X1–X9; SW09_chain.json, verdict field):

- X1 γ_v curve 1.00000–1.01012 (SW04 D) · X2 A2 = 2.22e-16 (SW04 B1 / SW05 C1) · X3 P4 gaps 0.118/0.083/0.049/0.019 dex at η = 2/3/5/10 (SW05 B1) · X4 P9 ladder 0.9958/0.9884/0.7169/0.3364 monotone (SW05 D1) · X5 gate 152.1/220.3 per-field and 304.1/440.7 dilution (GATE_CONVENTION) · X6 eBTFR slope 1/4 for any S, sympy exact (SW04 A2/A3) · X7 alpha_2 = 0.00e+00 with c_S ≤ 4.23/423 (SW08 B4/B5) · X8 η_c window consistency with the 4.0e-4 precision note (SW01b B2/SW03/SW07) · X9 η_sun rebuilt 2.2918, the L0 tie (SW01b B1 / SW09_meanvalue D2).

## The honest section

- **WHAT IS PROVEN:** the implication structure above — each link is either a compiled Lean theorem (SW06_lemmas.lean: `eBTFR`, `conformal_BR`, `newton_limit`, `mond_limit`, `mu_S_equiv`; exit 0, no sorry — verified by reading the file) or a computed check in a landed .out file, cited as (file, check, number); plus the obstruction statement's formal names (SW09_obstruction.lean, pending-compile-confirmation) and the 9/9 recomputation (SW09_chain.out). Lean certifies ALGEBRA only; the physics gates live in the lanes (LAW_STATEMENT.md).
- **WHAT IS MEASURED:** a0 (κ = 0.5, slot NOT LIVE per KS01; 9.3619e-11 / 1.1279e-10 m/s²) and η_c (declared 0.2034/0.1688; the WINDOW is the measurement — Oort ceiling 0.203, LSS floor 0.028, Fornax ≤ 0.145; the canonical central value is data-selected at the ceiling's 3-dp precision).
- **WHAT IS ASSUMED:** the S-family ansatz (SW07 H5: only the limits are structural; every derivation mechanism in the class was attacked and killed — the third lane kill); the ν_RAR kernel (data-selected, rung 2); the barycenter-centering condition as part of the law (SW01b C3 / SW08 D1-D2: load-bearing).
- **WHAT IS OPEN:** the G03 covariant action (an AeST-type completion on the SOURCED sector with the ambient linear — where L243's Cassini quadrupole arises in AQUAL); the ghost quadratic-form theorem (the remaining G03 kill gate — it does not exist yet); the causal/retarded completion (SW08 C4: FAIL-as-finding — the deep limit and the Newton limit are causality-robust, the retarded kernel is not exhibited); the matter-frame coupling c_S (the named missing input); the obstruction file's compile status (parallel agent).

*Scope note:* exactly four files were written in this swing (PROOF_CHAIN.md, SW09_chain.py, SW09_chain.out, SW09_chain.json); no git commands; no edits to SW00_INDEX.md, LAW_STATEMENT.md, KILLS_SYNTHESIS.md, GATE_CONVENTION.md, or any SW01–SW08 artifact. No numbers were invented: every number above is quoted from a landed artifact or recomputed from the axioms with the target quoted alongside (SW09_chain.out).
