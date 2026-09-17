# SW09_PROOF — the proof that the framework's equations imply the predictions
(2026-09-17, ninth swing; assembled from landed artifacts + the verified mean-value theorem)

**Status box (verbatim):** This is NOT a derivation of gravity from first principles. It IS a
proof that these equations imply these predictions, plus an obstruction that any covariant
completion is auxiliary-or-nonlocal (G03-class). Ghost quadratic-form theorem: OPEN (the
remaining G03 kill gate). α₂: priced (SW08), not derived. The words derived/closed/breakthrough
are not used as claims.

---

## Theorem 1 — the mean-value structure (VERIFIED: 11/11 clean, 10/11 MUTATE)

Let Ω be a Gauss sphere centered on the barycenter B of the enclosed baryons, and split the
Newtonian sources into ENCLOSED (any interior configuration) and ENVIRONMENT (exterior). Then,
exactly:

- **(T1)** ⟨g_N⟩_Ω = g_env(B).
- **(T2)** η = |g_env(B)|/a₀ — a POINT value at the barycentre.
- **(T3)** Γ² = ⟨|g_N − g_env(B)|²⟩ — Γ is the RMS deviation of the field from the ambient.

**Proof.** (T1): every exterior-multipole term of an interior source carries l ≥ 1 angular
dependence (⟨Y_lm⟩ = 0), and the monopole is radial with ⟨r̂⟩ = 0 — so the enclosed part
averages to zero for ANY interior configuration, off-centre included; each Cartesian component
of the exterior field is harmonic in the ball, so its sphere average equals its centre value.
(T2): definition + (T1). (T3): the variance identity ⟨|X|²⟩ = |⟨X⟩|² + ⟨|X−⟨X⟩|²⟩ with
⟨X⟩ = g_env(B). ∎

**Verification:** SW09_meanvalue.out — 11/11 PASS (A1 quadrature normalisation; A2 ⟨r̂⟩ = 0;
B1 enclosed-off-centre zero mean; B2 environment mean-value; B3 full field; B4 the two Γ forms
agree to < 1e-10; C1/C2/C3 the DC/AC split; D1 the hinge; D2 η_⊙ retro-justification).
MUTATE: 10/11 — D1[HINGE-MUTANT] FAILs by the tidal variation (the centre is load-bearing).

**Corollary (the DC/AC split — P10):** the environment's DC part goes to η only (conformal
suppression, shape preserved — SW04 B1, 2.22e-16); its AC/tidal part goes to Γ only (shape
distortion with S pinned at 1 — a symmetric external pair gives η = 0 exactly while moving Γ).

---

## Theorem 2 — the obstruction (specific pair form; verification in flight)

Γ and η, as the framework defines them, are **not functions of any finite jet** of the
Newtonian field at the field point: there exist configurations A, B whose 2-jet at the field
point agrees to ≤ 1e-12 relative while (Γ,η)_A ≠ (Γ,η)_B. Consequently **no local trigger** —
μ(|g|), any jet-polynomial, or any function of the finite jet — can realize (Γ,η) while
preserving: (i) uniform ⇒ Γ ≡ 0; (ii) isolated ⇒ Γ = |g_N|; (iii) conformal S.

**NOTE (the Weyl-tensor trap, pre-addressed):** the naive universal negative over ALL local
invariants is FALSE (Weyl-like invariants evade it). The theorem is the SPECIFIC statement about
the framework's own (Γ,η) — and its content is: **any covariant completion is
auxiliary-field-with-constraint or explicitly nonlocal (G03-class).**

Status: identities (i),(ii) verified by quadrature (SW01b C1/C2; SW09_meanvalue C1); the pair
construction + the Lean formalization are the in-flight computation (Agent B, deleg task 1).
Pre-registered kill: if any 2-jet invariant reproduces (Γ,η) on both members, the obstruction
dies — recorded as such, never patched.

---

## The chain (every edge = file, check, number)

- **L1 orthogonality** — SW01b C1/C2; SW09_meanvalue C1.
- **L2 conformal pointwise scaling** Q(R) = S·Q_iso(R) — SW04 B1, 2.22e-16.
- **L3 P₂ = 0** — SW05 C1 (2.22e-16); SW01b G (−6.1e-14 a₀).
- **L4 eBTFR** v⁴ = S² G M_b a₀ — SW04 A2/A3 (sympy); SW06_lemmas `ebtfr` (Lean, compiled).
- **L5 μ_S well-posed** (single-valued; round trip 2.22e-16) — SW06 B1/C1; SW06_lemmas `mu_S_equiv`.
- **L6 the gate, both readings, both footings** — GATE_CONVENTION.md: per-field 152.1/220.3,
  dilution 304.1/440.7; both clear 6.4.
- **L7 α₂ double suppression + the bound** — SW08 B4 (planetary anisotropy ≈ 0, doubly
  suppressed) / B5 (c_S ≤ 4.23 Nordtvedt / ≤ 423 LLR-scale).
- **L8 the obstruction** — Theorem 2 (Agent B, in flight).
- **C1 the DR4 kill rule** — γ_v 1.0000–1.0101 (SW04 D) vs the bands 1.00 / 1.09–1.12 /
  1.16–1.23; inside 1.16–1.23 or > 1.05 kills the class. Decided 2026-12-02.

---

## PROVEN

L1–L7 as above (each a computed check in a landed .out, or a compiled Lean theorem). Theorem 1
verified (11/11, hinge flips). The obstruction's identities (i),(ii) verified. Every claim above
carries its (file, check, number).

## MEASURED

κ = ½ → a₀ = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m/s²; KS01: slot NOT LIVE, four
candidates inside 2σ. η_c ∈ [0.145, 0.203] — two independent determinations (Oort ceiling
≤ 0.203, Fornax floor ≤ 0.145); the central value stays data-selected.

## ASSUMED (labeled, not derived)

A4 the S-family (ansatz; only its limits are structural — SW07 H5). A5 ν_RAR (data-selected,
rung 2). A3 the barycenter condition (load-bearing — the decentered mutant is PPN-dead,
SW08 B4[MUTATED] 0.76). The A2 audit finding (the alt-footing recipe discrepancy, recorded
as-is).

## OPEN

The G03 action (the derivation door). The ghost quadratic-form theorem (the remaining kill
gate). The causal completion (SW08 C4 — no retarded kernel in this swing). The obstruction's
Lean formalization (in flight, deleg task 1). P10's rival side (AQUAL's tidal response — needs
the DE lane's solver). Per-object Jeans (needs Walker likelihoods — absent in repo).

---

## The Lean certificates

SW06_lemmas.lean: `ebtfr`, `conformal_BR`, `newton_limit`, `mond_limit`, `mu_S_equiv` —
compiled from the live toolchain (fable_independent_2026/lean_2026), exit 0, no sorry
(the no-sorry gate: grep 'sorry|admit|axiom' over the Lean sources — clean, re-run before
every claim). SW09_obstruction.lean: in flight (Agent B) with the pinned theorem names
`uniform_field_Gamma_eq_zero`, `uniform_field_eta`, `isolated_centered_Gamma`,
`isolated_centered_eta` — deleted rather than weakened if any fails to close.
