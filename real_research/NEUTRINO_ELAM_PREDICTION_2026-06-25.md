# Neutrino-Mass Hypothesis from the Zimmerman Vacuum-Energy Scale E_L

**Date:** 2026-06-25
**Status:** SPECULATIVE HYPOTHESIS (clean + falsifiable), **NOT a forced derivation.**

---

## ⚠️ Read this first — the forced-vs-hypothesis label

The framework **forces** one number here: the vacuum-energy mass scale
**E_L = ρ_DE^(1/4) = 2.2395 meV.** That is a real, derived consequence of ρ_DE.

The framework does **NOT** force the step **m_lightest = E_L.** Setting the O(1)
coefficient in front of ρ_DE^(1/4) equal to **exactly 1** is a *fit-by-inversion* — there
is no forced geometric factor (no √(8π/3), no Z, no triality decomposition) that makes the
lightest neutrino mass equal the vacuum scale. It is a **scale coincidence dressed as a
prediction.** This document tests that coincidence honestly. If it dies, it falsifies *this
hypothesis*, not the framework's gravity result (a₀ = √Λ, the dS–Unruh MOND scale).

So throughout: **E_L = 2.2395 meV is forced; m1 = E_L is a guess.**

---

## Step 0 — Reproduce E_L from ρ_DE (mpmath dps = 40)

Using ρ_DE = 5.836×10⁻²⁷ kg/m³, the field mass-scale whose vacuum energy density equals
ρ_DE·c² is E_L = (ρ_DE c² · (ℏc)³)^(1/4):

| quantity | value |
|---|---|
| ρ_DE | 5.836×10⁻²⁷ kg/m³ |
| u = ρ_DE c² | 5.2451×10⁻¹⁰ J/m³ |
| **E_L** | **2.2395019 meV** |

✓ Sanity check passes: ≈ 2.24 meV. The hypothesis fixes **m_lightest = E_L = 2.2395 meV.**

---

## Oscillation inputs (NuFIT 5.3 / PDG 2024, exact values used)

| parameter | value (1σ) | role |
|---|---|---|
| Δm²₂₁ | (7.42 ± 0.205)×10⁻⁵ eV² | m1→m2 |
| Δm²₃₁ (NO) | (+2.510 ± 0.027)×10⁻³ eV² | m1→m3 |
| Δm²₃₂ (IO) | −2.490×10⁻³ eV² | IO control |
| sin²θ₁₂ | 0.303 ± 0.012 | \|U_e2\|² |
| sin²θ₁₃ | 0.02203 ± 0.00056 | \|U_e3\|² |

PMNS electron-row weights:
**\|U_e1\|² = 0.6816, \|U_e2\|² = 0.2963, \|U_e3\|² = 0.02203** (sum = 1.000).

---

## Step 1 — NORMAL ORDERING (m1 = E_L lightest): the predicted spectrum

m1 = E_L; m2 = √(m1²+Δm²₂₁); m3 = √(m1²+Δm²₃₁).

| eigenstate | mass |
|---|---|
| **m1** | **2.2395 meV** (the hypothesis) |
| **m2** | **8.9003 meV** |
| **m3** | **50.150 meV** |

---

## Step 2 — The three observables

### (a) Σm_ν vs cosmology

**Σm_ν = m1+m2+m3 = 61.290 meV = 0.06129 eV.**

- Minimal-NO floor (m1→0): Σ = 58.714 meV = 0.05871 eV.
- **The prediction sits just 2.58 meV (≈ +4.4%) above the minimal-NO floor.** Because m1 is
  tiny next to m3, forcing m1 = E_L barely moves Σ off the floor — the spectrum is
  **essentially the minimal normal-ordered value.**
- Cosmological ceiling: Planck+DESI 2024 ≈ **Σ < 0.072 eV (95%)** (tightest combinations
  reach ~0.064–0.072 eV depending on dataset/priors).
- **Verdict: BELOW the ceiling, but only just.** 0.0613 eV vs 0.072 eV leaves ~10 meV of
  headroom. The DESI/Planck bound is actively squeezing toward the minimal-NO floor
  (0.059 eV); the prediction lives in the thin surviving band between floor and ceiling.

### (b) m_β (KATRIN effective electron-neutrino mass)

m_β = √(Σ \|U_ei\|² m_i²) = **9.0718 meV = 0.00907 eV.**

- KATRIN current: < 0.45 eV; KATRIN final design ~0.2 eV.
- Project-8 (atomic tritium) target ~0.04 eV; ultimate ~0.01–0.04 eV.
- **Verdict: ~22× below KATRIN-final, at/below the best conceivable Project-8 reach.**
  This observable is **NOT a near-term discriminator** — direct kinematic mass is too small
  to see. Not a falsifier this decade.

### (c) m_ββ (0νββ effective Majorana mass) — range over Majorana phases α21, α31 ∈ [0,2π)

m_ββ = \| U_e1² m1 + U_e2² m2 e^{iα21} + U_e3² m3 e^{iα31} \|.
Term magnitudes: \|U_e1²m1\| = 1.527, \|U_e2²m2\| = 2.637, \|U_e3²m3\| = 1.105 meV.

- **Max (phases aligned): m_ββ = 5.269 meV.**
- **Min (max cancellation): m_ββ = 0.006 meV** (≈ 0). The largest term, 2.637 meV, *just*
  exceeds the other two summed (1.527+1.105 = 2.631 meV) — the phasor triangle *barely*
  fails to close, so the true floor is 0.006 meV rather than exactly 0. Effectively the full
  cancellation window is open.
- **Predicted range: m_ββ ∈ [0.006, 5.27] meV.**
- Reach: KamLAND-Zen / current best ~0.028–0.122 eV (28–122 meV); next-gen (nEXO, LEGEND-1000,
  KamLAND2-Zen) ~0.005–0.020 eV (5–20 meV).
- **Verdict: the entire predicted band sits AT or BELOW the optimistic edge of next-gen
  reach.** Only the phase-aligned maximum (~5.3 meV) grazes the most optimistic next-gen
  sensitivity (~5 meV). For most phases it is unreachable. **Not a robust near-term falsifier**
  — a next-gen *non-detection* would be fully consistent with this hypothesis (and with
  minimal-NO generally), so 0νββ can neither confirm nor kill it soon.

---

## Step 3 — INVERTED ORDERING control (m3 = E_L lightest)

If instead m3 = E_L is the lightest state (IO), with \|Δm²₃₂\| = 2.490×10⁻³ eV²:

| eigenstate | mass |
|---|---|
| m3 | 2.2395 meV (lightest) |
| m1 | 49.202 meV |
| m2 | 49.950 meV |

- **Σm_ν (IO) = 101.39 meV = 0.1014 eV** — ABOVE the Planck+DESI ceiling (~0.072 eV).
  Minimal-IO floor is already 99.05 meV.
- m_β (IO) = 48.88 meV; m_ββ (IO) ∈ [18.7, 48.4] meV (the heavy near-degenerate pair
  prevents full cancellation → a *guaranteed* 0νββ signal in next-gen reach).
- **The IO reading of this hypothesis is in TENSION-to-EXCLUDED by cosmology now**
  (0.101 eV vs <0.072 eV). Current global data already disfavor IO at ~2–2.7σ independent of
  this hypothesis.

**Which ordering does the hypothesis pick?** The hypothesis specifies only a single lightest
mass = E_L; it picks an ordering only when combined with the measured splittings. Read as
**normal ordering** it gives a viable, near-floor spectrum (Σ = 0.061 eV). Read as inverted it
gives Σ = 0.101 eV, already in cosmological tension. **Current data favor NO**, so the hypothesis
is **most naturally read as normal-ordered, m1 = E_L** — and that is the only version that
survives present bounds. The NO-vs-IO contrast is itself a (weak) consistency test the
hypothesis passes only in NO.

---

## VERDICT (both ways, honest)

**Is the predicted spectrum consistent with current bounds?**
**YES, in normal ordering — but it lives in a narrowing band.** The NO spectrum
(Σ = 0.0613 eV, m_β = 0.0091 eV, m_ββ ≤ 0.0053 eV) violates **no** current bound: under the
KATRIN ceiling by ~50×, under the 0νββ reach, and under the Σ ceiling with ~10 meV to spare.
The IO version is already in tension and is the disfavored ordering anyway.

**The pressure point is Σm_ν.** Because m1 = E_L is tiny, the prediction is essentially the
*minimal* normal-ordered sum (0.0613 vs 0.0587 eV floor). DESI+Planck is tightening toward
that floor. Two outcomes:
- If cosmology pushes the 95% bound **below ~0.059 eV** (i.e. below the NO floor), it would
  exclude normal ordering entirely → kills this hypothesis (and is in tension with oscillation
  data — a known looming clash). 
- The hypothesis adds only +2.6 meV over the floor, so it is **the first thing to fall after
  the floor itself** if the bound keeps dropping — but it is also **indistinguishable from
  minimal-NO**, meaning a confirmation of minimal-NO would *not uniquely* confirm m1 = E_L.

**Sharpest near-term falsifier:**
**DESI DR2/DR3 + CMB (Σm_ν).** A robust 95% upper bound on Σm_ν that drops to
**≈ 0.060 eV or below — expected window 2026–2028 (DESI DR3-era)** — would put the predicted
Σ = 0.0613 eV at/over the ceiling and squeeze m1 = E_L toward/below zero, falsifying the
hypothesis. Equivalently, a firm establishment of **inverted ordering** (e.g. JUNO,
mid-2027→) would kill the only viable (NO) reading. Direct-mass (KATRIN/Project-8) and 0νββ
(nEXO/LEGEND) are **too insensitive** to reach 0.0091 eV / ≤0.0053 eV this decade — they are
*not* the falsifiers. **Cosmological Σm_ν is the blade; ~2026–2028 is the timeframe.**

**Restate plainly:** This is a **clean, falsifiable hypothesis motivated by the framework's
forced meV scale** (E_L = ρ_DE^(1/4) = 2.2395 meV is genuinely derived). But the step
**m_lightest = E_L is NOT forced** — the O(1) coefficient = 1 is fit by inversion, with no
geometric factor behind it. It is therefore a **speculative prediction, not a derivation.** A
future Σm_ν measurement or an ordering determination that kills m_lightest ≈ 2.2 meV falsifies
**THIS hypothesis only** — it leaves the framework's gravity result (a₀ = √Λ) untouched.

---

## Summary table

| quantity | predicted (NO, m1=E_L) | current bound | status |
|---|---|---|---|
| m1 | 2.2395 meV | — | hypothesis (E_L forced; "=m1" NOT forced) |
| m2 | 8.900 meV | — | derived from Δm²₂₁ |
| m3 | 50.15 meV | — | derived from Δm²₃₁ |
| **Σm_ν** | **0.0613 eV** | <0.072 eV (Planck+DESI 95%); floor 0.0587 eV | **consistent, near floor** |
| **m_β** | **0.0091 eV** | <0.45 (KATRIN); ~0.2 final; ~0.04 Proj-8 | unreachable — not a test |
| **m_ββ** | **[0.006, 5.27] meV** | 28–122 meV now; 5–20 meV next-gen | at/below reach — weak test |
| Σm_ν (IO control) | 0.1014 eV | <0.072 eV | **in tension — disfavored ordering** |
