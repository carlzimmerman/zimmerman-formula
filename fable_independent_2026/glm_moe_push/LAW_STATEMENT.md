# LAW_STATEMENT.md — the Γ/η response law (empirical statement; 2026-09-17)

## Status box (read first)

- **WHAT THIS IS:** an empirical law in the CLOSURE_MAP sense — the same status rung 1
  already holds (κ MEASURED). Two measured constants, a data-selected kernel, an ansatz
  S-family, and certified algebra (SW06_lemmas.lean, compiled exit 0).
- **WHAT THIS IS NOT:** not derived (SW07 killed every mechanism in the closed class; the
  derivation door is G03, OPEN); not a complete theory of gravity (no action, no ghost
  theorem, α₂ open); "law of nature" is NOT claimed — this is the rung-1-style empirical
  statement that CLOSURE_MAP's decision rule names a legitimate, publishable end state.
- **Word-ban compliance:** "derived", "closed", "breakthrough" appear nowhere below as claims.
- **The second-independent-computation rule (08-09 near-miss), satisfied for the gate:** the
  S-language (SW01b D: 152.1/220.3) and the μ-language (SW06 D2: 304.1 canonical, 220.3 alt)
  are two methodologically distinct computations of the same kernel gate — consistent, both
  ≥ 6.4.

## The law

On barycentered Gauss spheres (center = the enclosed baryons' barycenter, fixed by the flux
structure — no hand-drawn boundary):

```
g_obs = g_free + [ (1 − S(η)) + S(η)·ν(Γ/a₀) ] · g_src
Γ² = ⟨|g_N|²⟩_Ω − |⟨g_N⟩_Ω|²          (the field's own structure — the sourced part)
η  = |⟨g_N⟩_Ω| / a₀                    (the sphere's l=1 component — the environment)
S(η) = 1/(1 + (η/η_c)²)                — an ANSATZ (SW07 H5: only the limits are structural)
ν_RAR(y) = 1/(1 − e^(−√y))             — rung 2, DATA-SELECTED
a₀ = ½·c·√(G·ρ_Λ)                      — rung 1, MEASURED (κ's slot NOT LIVE, KS01)
```

## The two measured constants

1. **κ = ½** (a₀ = 9.3619e-11 m/s² canonical): MEASURED (0.465 ± 0.076 / 0.551 ± 0.043);
   slot adjudicated NOT LIVE (KS01); four candidates inside 2σ.
2. **η_c:** bounded by two independent determinations agreeing in direction — Oort ≤ 0.203
   (from above, L263 C1) and Fornax-implied ≤ 0.145 (from below, SW03 C2) — with the LSS
   floor ≥ 0.028 (SW01b F) and the deep-window requirement (P4: η ≈ 2–3.5 must stay
   unsuppressed, which is automatic for any η_c in the window). The central value remains
   data-selected; the WINDOW is the measurement.

## The certified algebra (SW06_lemmas.lean — compiled, exit 0)

`newton_limit` (S=0 → exact Newton), `mond_limit` (S=1 → the RAR), `mu_S_equiv` (single-valued
— well-posedness verified numerically in SW06 B1: monotone g→g_obs for every S, the
non-trivial condition since ν decreases in g while g grows), `conformal_BR` (S cancels in the
boost ratio — the RAR shape is environment-independent), `eBTFR` (v⁴ = S²GM_ba₀ — slope
exactly 4 for any S). Lean certifies ALGEBRA only; the physics gates live in the lanes.

## Consequences (frozen in SW05, before the data; decision regions and dates)

P1 DR4 γ_v 1.0000–1.0101 (2026-12-02; kill >1.05 or in 1.16–1.23) · P2 angular null
A₂ = 2.2e-16 vs AQUAL ~6% · P3 solar quadrupole ≈ 0 vs 6.44× ceiling · P4 floor window
η ≈ 2–3.5 (gaps 0.118/0.083 dex) · P9 THE eBTFR ladder a₀_eff/a₀ = 0.996 → 0.717 → 0.336
(field → group → cluster vicinity) · P7/P8 inherited flat-a₀ (0.00 dex; R = 1.000 vs the
registered 0.775 [0.68, 0.88], Rubin 3.3σ). Not this class's test: tSZ (rung 7).

## The kill conditions (what falsifies the law)

P1: γ_v > 1.05 or inside 1.16–1.23 → dead (2026-12-02). P2: A₂ ≠ 0 at the registered
statistic → dead. P3: any AQUAL-level quadrupole → dead. P8: R < 0.9 at ≥3σ → the flat law
dies → this class dies with it. P9: BTFR zero point not tracking S²(η) → dead.

## NOT supplied (the honest non-derivation list)

- **No action**: the G03 door is named and OPEN — an AeST-type completion on the SOURCED
  sector with the ambient added linearly (where L243's Cassini quadrupole arises in AQUAL).
  The ghost quadratic-form theorem and α₂ are its kill gates; neither exists yet.
- **No derivation of κ** (KS01: slot NOT LIVE), **of η_c** (SW07: every remaining-class
  mechanism killed — the third lane kill), **or of the ν_RAR/S families** (data-selected /
  ansatz).
- **The rung-6 fork** (0.489 vs 1.000 M_b inside r_M) is carried as the record's open
  systematic — this class's predictions P1–P9 are fork-independent (baryon-only), so the law
  statement does not depend on the fork's resolution. For THIS class the fork reduces to
  kernel selection: the class's kernel is ν_RAR, so its phantom identification is the
  RAR-family profile (the L263 B1 identity M_dyn = M·r/r_M, sympy-verified); the 0.489 value
  belongs to the μ₂/AQUAL rival kernel. The fork therefore lives at the kernel-selection
  level (f25, OPEN) — queued as the rung-6 computation, not resolved here.
- **α₂**: the matter-framed sphere picks the source rest frame — an α₂-level PPN effect is
  the named risk, open.

## The verification set

SW01b 18/18 · SW03 9/10 (η_c determination; NOT DISTINCTIVE discipline on the σ(D) trend) ·
SW04 13/13 · SW05 9/9 · SW06 8/8 · SW07 1/6 (all six FAILs are the findings — the third lane
kill, synthesis fired). All .out/.json on origin. Two kills (SW01-A, SW02) plus one attack
kill (SW07) — the three-kill synthesis rule satisfied. Next lanes, ranked: per-object Jeans
(the η_c sharpener, data in hand), DE04's η≥2 sample assembly (the P4 window), the covariant
action (ghost theorem + α₂ its kill gates), G111 OPEN spec, the rung-6 fork.
