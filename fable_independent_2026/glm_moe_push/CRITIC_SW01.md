# CRITIC_SW01 — the critic's findings on my own lane (2026-09-17, second swing)

Roles the brief assigned: PROPOSER, CRITIC, VERIFIER. Last swing landed PROPOSER + VERIFIER and
skipped the CRITIC. This page pays that debt before any new code.

## Findings on SW01_envscalar_response.py

- **C1 [REAL BUG — fixed in SW01b].** SW01-B calibrated η_c by demanding S(2.5) = 0.015/1.92,
  conflating the gate's internal transition variable x = 2.5 with the *external* environment of
  the solar neighbourhood. The environment that suppresses the stellar phantom is the Galactic
  field at the Sun, η_⊙ = (v_c²/R₀)/a₀ — a different number on each footing (1.90 alt, 2.29
  canonical with v_c = 233 km/s, R₀ = 8.2 kpc). Calibrating at the wrong argument made SW01-B's
  Oort pass argument-dependent. SW01b recalibrates on η_⊙ (both footings, computed from
  v_c²/R₀, not hardcoded): η_c ∈ [0.169, 0.203], S(η_⊙) = 0.0078 by construction, and the
  x = 2.5 gate ratio *improves* to 152–220. SW01-A's kill is unaffected.
- **C2 [TAUTOLOGY — fixed by quadrature].** The "first gate" never computed Γ or η from a field:
  with Γ, η defined by sphere averages and the external field uniform, the ratio 1/S(η) follows
  identically from the ansatz. SW01b computes Γ and η by actual numerical quadrature over the
  sphere (including the superposition cross-term), and adds the offset-center hinge test.
- **C3 [GAUGE DEPENDENCE — the center is now part of the law].** "The Gauss sphere through the
  field point" was ambiguous: on a sphere *not* centered on the enclosed baryons, Γ and η mix
  (computed in SW01b: the mixing is real). The law now specifies: spheres centered on the
  barycenter of the enclosed baryonic system — the center is fixed by the flux structure
  (Gauss's law), not drawn by hand.
- **C4 [Q₂ was a heuristic, not the brief's computation].** The old C[] checks were dimensional
  bounds (Q_L243 × dS × r_M/R₀), not a Legendre expansion of the modified field. SW01b computes
  the actual P₂ coefficient of the response field on the phantom shell (r = 2 r_M) by quadrature:
  it is 0 to machine precision because Γ and η are *scalars* — the response has no direction to
  align with, so no l ≥ 2 moment arises at any order in η. The inward propagation of a monopole
  is monopolar (Newton's theorem, exact). Full Cassini-grade axisymmetric propagation is fable's
  DE01 solver — marked OPEN, not claimed.
- **C5 [unpaid gates now paid].** RAR/LSS gate added: S(η_LSS) ≥ 0.9 with η_LSS computed from
  v_pec·H₀ (both footings) — the constraint that would have killed the class if the LSS field
  were a few tenths of a₀. It passes with margin (S ≈ 0.998).
- **C6 [still true, unchanged].** ν_RAR remains DATA-SELECTED (rung 2); κ remains MEASURED (R8);
  the ghost theorem does not exist (FAIL-as-finding); η_c is DECLARED and inherits v_c, R₀, a₀
  systematics — a second reason it is not derived.
- **C7 [numerology control].** The Oort ratio 1.92/0.015 = 128 = 2⁷ and the √127 in η_c are
  empirical ratios, not formulas; logged under a KS04-style look-elsewhere control, never to be
  reported as structure.

## Standing verdicts (unchanged)

SW01-A: KILLED (Oort, 17.7×). SW01-B: OPEN — declared η_c, falsifiers dated
(Gaia DR4 2026-12-02; any AQUAL-level EFE detection; satellites at η ≳ 1 with deep-MOND
dispersions). No words above claim derivation or closure.
