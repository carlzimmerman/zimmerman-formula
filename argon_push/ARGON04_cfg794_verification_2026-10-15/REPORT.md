# ARGON04 — Independent referee of CFG794 + native-mass robustness check

**Date:** 2026-10-15. **Home:** `argon_push/ARGON04_cfg794_verification_2026-10-15/`.
**Target:** CFG794 (criteria `e6e2f236b`, result `423c96eef` — the parallel CFG track executed it before this
lane arrived). **Run:** 0 FAIL, exit 0, wall 0.00 s, 71 MB. Controls: every CFG794 number recomputed from the
frozen criteria + CODATA constants (not from their code); then the framework-native portal mass (ARGON03)
added as a robustness check. External inputs provisional (memory). κ = ½ FITTED.

## Referee: CFG794's verdict survives independent recomputation (<5% on every number)

| quantity | CFG794 (423c96eef) | this run | gate |
|---|---|---|---|
| (a) resonant Q_field / min(Q_c) | 1.70e6 | 1.699e6 | ✓ |
| (b) spontaneous-into-mode r | 9.02e-24 s⁻¹ | 9.019e-24 s⁻¹ | ✓ |
| (b) laser threshold shortfall | ×4.2e27 | ×4.21e27 | ✓ |
| (c) coherent gain (l_c/d)² | 4.2e4 | 4.23e4 (l_c = 0.103 mm) | ✓ |
| passive (a)×(c) vs S = 6.39e34 | short ×8.9e23 (24 orders) | ×8.9e23 | ✓ |
| K1 Planck = aT⁴ @5800 K | PASS (0.00%) | PASS (0.00%) | ✓ |
| K2 S = τ/(d/σ), d = 0.5 μm | 6.39e34 | 6.388e34 | ✓ |
| MUTATE τ = 1 μs | bites (1.25e6 > 3.8e4 s⁻¹) | bites | ✓ |
| class | **NOT CLOSABLE** | **NOT CLOSABLE** | ✓ |

## New content: the verdict is robust to the portal mass (framework-native 2.24 meV)

CFG794 froze m = 2.5 eV (CFG790's line). The framework-native vacuum-induced mass (ARGON03,
m_native = 2.24 meV) is ~1000× lighter, which *helps* the enhancement classes — and still fails:

- coherent volume: l_c = ħ/(mσ) = 115 mm (vs 0.103 mm) → (l_c/d)² = 5.3e10 (vs 4.2e4) → passive
  (a)×(c) = 9.0e16 — **still 18 orders short** of S = 6.4e34;
- laser test: n̄ = u_c/(ħωρ_m) = 2.0e12 per mode (vs 1.3e-5) → r = 1.4e-11 s⁻¹ vs threshold 34 s⁻¹ —
  **still 12 orders short**.

The physics: the passive gain is bounded by the *field* linewidth (Q_field = (c/σ)², from the medium's
230 km/s velocity dispersion — a medium property, not a device property), and the stimulated test is
bounded by the cold energy per mode, which at 2.5 eV is n̄ ≪ 1 and at 2.24 meV is n̄ ~ 2e12 but still
7–12 orders below the cavity-loss rate. (d) parametric reduces to (b) — no new factor possible.

## Combined reading (CFG789 → CFG792 → CFG794, now cross-checked)

The converter requirement S = 6.4×10³⁴ over the sky-limited spontaneous rate is not softened by any
known enhancement class at ANY portal mass the framework can name. Combined with CFG792's
material-portal exclusion (≥2e5 off in natural matter) and CFG790's stellar-bound audit (ARGON03), the
ramjet's viability rests on a single un-derived assumption: a device-only, engineered conversion channel
with ~10³⁴× stimulated gain — which CFG794 now shows no known physics provides. CFG795's class P1–P9
design-space scan (committed `2be9ffbb1`) inherits this bound: P6 laser stimulation is capped by the same
detailed-balance test computed here (with and without the native mass).

## Honest scope
- All external inputs (τ ≥ 4.4e15 yr from the COB; u_c = 6.1e-5 J/m³; σ = 230 km/s; the CFG790 portal
  scale) remain provisional.
- (c) is an upper bound by construction ("gain ≤"); the true coherent gain is smaller, so the verdict is
  conservative in the direction that matters.
- No new physics asserted: this is a verification and a robustness check; κ = ½ stays FITTED.

## Verdict
**PASS — CFG794 verified (every number <5%), class NOT CLOSABLE confirmed, and the framework-native
2.24 meV mass does not rescue the enhancement route (18 orders passive / 12 orders laser short).**