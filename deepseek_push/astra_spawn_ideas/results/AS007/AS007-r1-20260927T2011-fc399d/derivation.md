# AS007 — Flat speed and scale sensitivity: derivation

**Task:** `deepseek_push/astra_spawn_ideas/AS007_flat_speed_and_scale_sensitivity.md`
(SHA-256 `fc399de0b8b769c547d578508d9f9f3396e2f65b59568a0827b19776e12bd1a7`)
**Run:** `results/AS007/AS007-r1-20260927T2011-fc399d/`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent.
**Sources verified against `SOURCE_MANIFEST.json` (all hashes match):** `README.md`
`91a5fac4…`, `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`
`98d9149f…`, `campaign_fresh_gravity_astra/DERIVATIONS.md` `8da8176e…`,
`STANDING.md` `660462eb…`.
**Amendment block in force (2026-09-26):** operative kernel = filtered `ν_mono`;
causality = criterion B; the thirteen-item target of the FRIED_CHICKEN spec, with
requirements 1, 7, 12 amended. Historical Q, RAR, MU2, EXP branches are
comparison branches only; conclusions here use the shared deep limit, which is
exactly branch-common (see §5), so no branch translation is imported.

Numeric conventions (framework contract): G = 6.67430e-11 m³ kg⁻¹ s⁻²,
c = 299792458 m/s, M_sun = 1.98847e30 kg, pc = 3.085677581491367e16 m,
k_B = 1.380649e-23 J/K (declared, unused). Adopted `κ = 1/2`. Both a₀ footings
carried separately everywhere: canonical `a0_c = 9.3619e-11 m/s²` and
alternative `a0_a = 1.1279e-10 m/s²`.

---

## 1. Precise claim, symbol dictionary, assumptions (task step 1)

**Claim (conditional deep-law statement; NOT a fitted BTFR).** For positive
`G_N, M_b, a0` and the framework's conditional deep limit
g² → a₀·g_N (y = g_N/a₀ → 0) of the operative RAR/MONO kernel, with circular
test orbits in the exterior of a baryonic monopole:

```text
v_flat⁴ = G_N M_b a0        and        v_flat = (G_N M_b a0)^(1/4)      [m/s]
d ln v_flat = (d ln G_N + d ln M_b + d ln a0)/4
v_flat(a0')/v_flat(a0) = (a0'/a0)^(1/4)      (footing ratio, G- and M-independent)
```

**Symbol dictionary (SI):**

| symbol | meaning | units — value/convention |
|---|---|---|
| G_N | Newton coupling in the baryonic acceleration sector | m³ kg⁻¹ s⁻² — 6.67430e-11 (input, measured) |
| G_E | Einstein-sector coupling entering the vacuum scale | m³ kg⁻¹ s⁻² — carried as a SEPARATE symbol; same-G matching is a reduction, not an identity (contract §“same-theory discipline”) |
| c | speed of light | m/s — 299792458 (exact) |
| M_b | baryonic (test) mass | kg — test input |
| a0 | vacuum acceleration scale | m/s² — κ c √(G_E ρ_Λ) |
| κ | dimensionless normalization | 1/2 — ADOPTED input, NOT derived (STANDING rev. 9: measured 0.465±0.076, “κ consistent with ½ and not derived”) |
| ρ_Λ | vacuum mass density | kg/m³ — input from the vacuum branch (see §5 for both footings) |
| r_M | MOND radius √(G_N M_b/a0) | m |
| v_flat | deep-regime circular (flat) speed | m/s |
| r | test-orbit radius | m |
| y | g_N/a0 (baryonic acceleration argument) | — |
| s | r_M/r = √(y) (depth parameter) | — |
| B | g_N = G_N M_b/r² | m/s² |
| g | total radial acceleration | m/s² |

**Framework inputs (adopted, not conclusions of this run):**
κ = 1/2; G_N, c; ρ_Λ and the a₀ pair (scale inputs); the conditional deep law
g² = a₀ g_N as the y→0 limit of the operative kernel; the circular test map
v² = r·g; exterior-of-source condition; positivity of all variables.

**Conclusions established (this run):** the elimination v_flat⁴ = κ c G_N
√G_E M_b √ρ_Λ; the (1/4,1/4,1/4,1/8,1/8) sensitivity vector in
(κ, c, G_N, G_E, ρ_Λ); the footing ratio 1.0476752 (+0.0202267 dex);
the leading neglected term (1/4)(r_M/r) in the speed on the RAR branch
(different on the comparison branches, §5); the negative-control results (§6).

---

## 2. Derivation of the sensitivity vector and footing ratio (task steps 2–3)

**2.1 Deep reduction.** On the operative branch, MONO coincides with RAR
identically on y ≤ y* = 2.3374 (FRAMEWORK_CONTRACT branch dictionary), and the
deep region has y → 0 < y*. RAR: ν(y) = 1/(1−e^{−√y}), hence with s = √y,

```text
ν(y) = 1/s + 1/2 + s/12 − s³/720 + s⁵/30240 − …        (Bernoulli–type series)
g = B ν(y)  ⟹  g = √(a₀ B) [1 + (1/2)√(B/a₀) + (1/12)(B/a₀) − …]   (y → 0)
```

so g → √(a₀·B) as y → 0: the deep law. The other declared branches share the
same leading term (Q: g² = B²+a₀B; MU2: B = g·(1−(1+g/2a₀)^{−2}); EXP:
g·(1−e^{−g/a₀}) = B) — see the numerically verified table in §5. The deep law
requires no branch translation on its own domain.

**2.2 Circular-speed map (exterior monopole, deep regime).**
g_N = B = G_N M_b/r², circular speed v² = r·g, deep g = √(a₀ B) = √(G_N M_b a₀)/r:

```text
v² = r·√(G_N M_b a₀)/r  =  √(G_N M_b a₀)          (r-independent!)
v⁴ = G_N M_b a₀          ⟹   v_flat = (G_N M_b a₀)^{1/4}
```

**Dimensions (exact check):** [G_N M_b a₀] = (m³ kg⁻¹ s⁻²)(kg)(m s⁻²) = m⁴ s⁻⁴;
fourth root ⟹ m/s ✓. Also v_flat²/a₀ = √(G_N M_b/a₀) = r_M ✓ (the flat regime
starts at the MOND radius, where the Newtonian √(G_N M_b/r_M) equals v_flat by
construction).

**2.3 Log-differentiation (exact identity for the power law).**
With v = (G_N M_b a₀)^{1/4}, all variables positive:

```text
d ln v = (1/4)(d ln G_N + d ln M_b + d ln a₀).
Elasticities (Framing A, a₀ an input scale):
    e_G_N = e_M_b = e_a0 = 1/4.
```

Substituting the vacuum relation a₀ = κ c √(G_E ρ_Λ) (G_E kept separate from
G_N per contract; d ln a₀ itself splits):

```text
ln v = (1/4)[ ln κ + ln c + ln G_N + (1/2) ln G_E + ln M_b + (1/2) ln ρ_Λ ]
e_κ = 1/4,  e_c = 1/4,  e_G_N = 1/4,  e_G_E = 1/8,  e_ρ_Λ = 1/8,  e_M_b = 1/4
same-coupling matching condition G_E = G_N (a reduction, not an identity):
e_G total = 1/4 + 1/8 = 3/8.
```

Sensitivity *statement*: every factor that enters a₀ does so with half the
exponent it would have at the level of a₀ itself — a 1% change in κ, c or G_N
moves v_flat by 0.25%; a 1% change in ρ_Λ or G_E moves it by 0.125%; a 1%
change in a₀ (whichever physical combination realizes it) moves v_flat by
0.25%. The flat speed is the *quarter-power* map of the scale — this is the
task's own claim, derived here from the deep law and the vacuum scale identity
with every coefficient and coupling labelled.

**2.4 Footing ratio (both footings, κ = 1/2 fixed).**

```text
v_a/v_c = (a0_a/a0_c)^{1/4} = (1.1279e-10/9.3619e-11)^{1/4}
        = 1.0476751663490419…          (+4.7675 %),  log10 = +0.02022665 dex
```

- Ratio is independent of G_N and M_b (removes them from the comparison;
  numerically verified over M ∈ {1e8, 1, 1e11}·M_sun to 0.0 residual).
- At fixed κ = 1/2, the two footings require *different* vacuum densities:
  ρ_Λ(can) = 5.8444124540e-27 kg/m³, ρ_Λ(alt) = 8.4830896196e-27 kg/m³
  (mass density; ρ_Λ = 4a₀²/(G_N c²)); ratio 1.4514872 = (a0_a/a0_c)².
- If instead ρ_Λ were held fixed at the canonical value, the alternative
  footing would require κ_eff = 0.6023884 (ratio a0_a/a0_c relative to 1/2).
  The flat speed cannot separate these two readings: v_flat determines a₀^{1/4}
  only, and the (κ, ρ_Λ) decomposition of a₀ is unidentifiable from flat-speed
  ratios alone (a₀-invariance is exact). Both footings must therefore be
  carried as full vacuum states, as the contract requires.

**2.5 Numerical examples (Section 8 of the computation, both footings):**
v_flat(M_sun) = 333.8660 m/s (canonical) / 349.7831 m/s (alternative);
v_flat(1e11 M_sun) = 187.747 / 196.698 km/s; r_M(M_sun) = 1.19064e15 m =
0.03859 pc (canonical) / 1.08474e15 m = 0.03515 pc (alternative).

---

## 3. Intermediate algebra, limiting regime and its leading neglected term

**Deep-limit approach (leading neglected term).** The exact RAR/MONO circular
speed for a point baryonic source at depth s = r_M/r is (closed form, no solve):

```text
v²/v_flat² = (G_N M_b/r)·ν(s²)/v_flat²  =  s/(1 − e^{−s})
           = 1 + s/2 + s²/12 − s⁴/720 + s⁶/30240 − …          (|s| < 2π)
```

so the exact speed exceeds the deep value with

```text
v/v_flat − 1 = (1/4)·s − (1/96)·s² + O(s³·…) ,   s = r_M/r,
```

i.e. **leading neglected term in the speed = (1/4)(r_M/r)**. Domain for the
one-term form: 0 < s ≤ 0.1 (r ≥ 10 r_M): the correction lies in
[0.0025, 0.025] with the s²/96 term at most 1.04e-4 (0.4 % of the leading
term). Numerically verified on s ∈ [1e-6, 0.2] (grid in §5, checks
`deep_limit_*`): exponent of the leading term = 1.0000163 (fit), coefficient =
0.2500104 at s = 1e-3 → 0.25 exactly as s → 0; two-term residual
O(s³) = 2.08e-14 at s = 1e-6.

**Newtonian limit / normalization.** As s → ∞ (r ≪ r_M): v²·r/(G_N M_b) =
ν(s²)⁻¹ = 1 − e^{−s} → 1 (Newtonian recovery, approached from below with
fractional deviation e^{−s}: 4.54e-5 at s = 10). As y → 0:
ν(y)√y = 1 + √y/2 + O(y) (deep-law normalization; leading-ratio check
1.00000000017 at y = 1e-12). The exact finite-consistency check at r = r_M:
v/v_flat = √(1/(1−e^{−1})) = 1.2577 — the exact curve approaches the flat
value from above.

---

## 4. Independent checks (task step 4) — actual residuals

1. **Substitution identity.** Compute v from v = (G M a₀)^{1/4} and re-insert:
   max |v⁴/(G M a₀) − 1| = 1.55575e-61 over the M-grid {3e8, 1, 1e13}·M_sun ×
   both footings (60-digit mpmath; the absolute residual floor 2⁻¹²⁶ for the
   1e13-M_sun operand is mpmath's internal precision guard, relative residual
   is the meaningful quantity). This is a finite high-precision consistency
   check of an *algebraic identity* (v⁴ = G M a₀ holds exactly in ℝ); the
   identity itself is what §2.2 derives.
2. **Direct differentiation.** (a) Log-space forward difference
   Δln v/Δln a₀ at h = 1e-30: 0.2499999999999999999999999999999305
   (residual −6.95e-32, i.e. exact to the 60-digit working precision — ln v is
   exactly linear in ln a₀ for the power law). Same for G_N, M_b, κ, c, G_E,
   ρ_Λ (table in §2.3: e_ρ = 0.1250000000000000000000000000002764, residual
   2.8e-31). (b) Linear-space FD of v(a₀) vs the analytic derivative
   (1/4)v/a₀: relative residual 6.73e-31 vs the finite-difference truncation
   prediction 3h/8 = 3.75e-31 — consistent (χ²-style agreement within 2×).
3. **Footing-ratio identity:** |v_a/v_c − (a0_a/a0_c)^{1/4}| = 0.0 exactly;
   ratio independent of M_b across the grid (spread 0.0).
4. **Exactness ledger:** the power-law log-differential and the footing-ratio
   equality are *exact algebraic identities* (also Lean-certified, §7); the
   deep-limit s/4 law and the Newtonian recovery are *limiting statements*
   verified on a finite grid; the normalization check verifies the *leading*
   term of an asymptotic law. Identities and finite checks are not conflated.

---

## 5. Branch discipline: shared deep limit, distinct finite corrections

Solved numerically at depth s ∈ {0.05, 0.1, 0.2} for a point baryonic source
(v² = r·g, g from each branch law; MONO = RAR exactly on y = s² ≤ 0.04 < y*):

| branch | v/v_flat − 1 at s = 0.05 | … at s = 0.1 | … at s = 0.2 | leading law (s → 0) |
|---|---|---|---|---|
| RAR = MONO (operative, deep region) | +0.0125257 | +0.0251016 | +0.0503957 | s/4 |
| Q (comparison) | +0.0006244 | +0.0024907 | +0.0098534 | s²/4 (no linear term) |
| MU2 (comparison) | +0.0094582 | +0.0190835 | +0.0388383 | 3s/16 |
| EXP historical AQUAL (comparison) | +0.0063225 | +0.0127934 | +0.0262028 | s/8 |

All four converge to v_flat as s → 0 (shared deep limit — that is why the
flat-speed law is branch-common and the operative MONO statement transfers to
the deep regime without translation), while the first correction differs in
exponent or coefficient for every branch. The task's conclusions are drawn
only on the operative branch (RAR/MONO) and its shared deep limit; the
corrections of the other branches are reported as comparisons, not used.

---

## 6. Negative control (task step 5) — must be capable of failing

**Control:** deliberately adopt the square-root speed law
v_mock = (G_N M_b a₀)^{1/2} (exponent 1/2 instead of 1/4) and apply the
mass-scaling test |d ln v/d ln M_b − 1/4| ≤ 1e-9 over M ∈ [1e10, 1e12]·M_sun.

- True fourth-root law: measured exponent 0.25 (residual 0.0) — **PASS**.
- Square-root mock law: measured exponent 0.5 (residual +0.25 vs gate) —
  **FAILS**, as required. Per mass doubling the mock law deviates by
  +0.0752575 dex; cumulative deviation over the decade grid +0.5 dex, growing
  without bound in |ln M|.
- The control is genuinely discriminating: it rejects the wrong law (the test
  was capable of failing), and the mock's failure is not repaired by any other
  branch in this run — no branch import was used.

Secondary discriminating controls that passed (capable of failing): the
deep-limit coefficient gate (a deliberately wrong s/2 ansatz would fail the
s/4 fit at |Δ| = 0.25); the normalization leading-ratio gate; the
footing-ratio mass-independence gate.

---

## 7. Strongest surviving statement and first transfer implication

**Surviving statement (conditional theorem; all conditions listed).**
*If* (i) the operative filtered-MONO kernel reduces to g = B ν_RAR(B/a₀) with
ν_RAR(y) → y^{−1/2} as y → 0 (exactly true on the y ≤ y* segment and verified
numerically as a limit), (ii) test orbits are circular in the exterior of a
compact baryonic source at r ≫ max(r_M, source scale ξ), (iii) v² = r g holds
for circular motion, and (iv) the a₀ pair and κ = 1/2 are framework inputs,
*then* v_flat⁴ = G_N M_b a₀ and the sensitivity vector and footing ratio of
§2 are exact; the footings cannot share both κ and ρ_Λ (density pair and
effective κ in §2.4); the deep law is branch-shared with branch-distinct
corrections (§5).

**First additional implication needed to transfer to the full theory (open,
explicit):** prove that the *operative field equations*
Δu = 4πGρ_b, ΔΦ = 4πGρ_b + S*·div[(ν_mono(|∇Su|/a₀) − 1)∇Su] with the heat
filter S = e^{(ξ²/2)Δ} admit exterior solutions whose radial acceleration and
circular-orbit speeds reproduce the deep law (for a compact source, Δu = 0 in
the exterior, so S = 1 there and the kernel argument is unchanged — a
heuristic sufficient condition, not a proof of the far-field asymptotics of
the full operator problem, nor of the lensing-potential identity Φ = Ψ
required by requirement 3 of the amended target), and that the boundary
conditions defining S* respect the exterior regime. Until that transfer, the
present result is a conditional deep-law scale statement, not a claim about
the full action's solutions. (The empirical deep-MOND BTFR zero point at
z ≈ 2.5 is a separate, data-gated test per STANDING rev. 9 — not part of this
derivation.)

## 8. Limitations

- κ = 1/2 remains an adopted input (measured 0.465±0.076, not derived);
  ρ_Λ values are vacuum inputs; no observational fit was performed (the
  task explicitly requests none).
- The deep-limit and Newtonian limits are verified on finite grids (evidence
  of approach, not universal theorems); the s/4 leading term is a series
  statement with stated domain |s| ≤ 0.1 for the one-term form.
- The result does not establish the finite-regime BTFR zero point, scatter,
  the filtered-operator far-field asymptotics (open transfer item), or
  anything about lensing/stability — those remain outside this task's gate.
- All exact identities are algebraic; the Lean certificate (§9) attests only
  its own declarations, not the physical premises.

## 9. Reproducibility

- Computation: `python3 AS007_flat_speed_sensitivity.py` (stdlib + mpmath,
  60 dps, 1 thread; wall 0.0142 s, max RSS 18.7 MB ≪ 512 MB; bounds recorded
  in `execution_bounds` of result.json). Raw output:
  `AS007_flat_speed_sensitivity_raw.txt` (20/20 checks PASS).
- Lean 4 certificate: `AS007_flat_speed_scale_sensitivity.lean`, verified with
  `lake env lean <abs path>` (exit 0, zero `sorry`, axioms
  {propext, Classical.choice, Quot.sound} — see .out). Theorems: the
  v²-encoding equivalence of the deep law, the footing-ratio identity, the
  exact scaling (sensitivity) law, the ρ-elasticity (1/8) identity, the
  resolved-form substitution with G_N ≠ G_E carried separately, the same-G
  reduction, and the negative-control inequality
  √2 ≠ √(√2) (square-root mock law's mass-doubling ratio differs from
  2^{1/4}).