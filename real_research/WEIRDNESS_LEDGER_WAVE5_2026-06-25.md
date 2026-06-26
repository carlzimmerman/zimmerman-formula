# Weirdness Ledger — Exploration Wave 5

**Date:** 2026-06-25
**Framework:** a₀ = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) = 5.78881, kernel = (3/8π)^(1/4) = √(2/Z) = 0.587788.
**Wave-5 mandate:** fresh, non-overlapping sectors (Koide-derivation routes CLOSED — not re-run). Hunt veins **K** (cosmic
density coincidences), **L** (mass-ratio ladder / Koide cascade), **M** (CP / baryogenesis). Rank by surprise × structural-ness
× forced-provenance; a structural/shared-geometric object or a forced scale-anchored factor outranks a bare value-match.
Both-ways: don't high-priest a real pattern, don't manufacture a coincidence into a proof.
**Verification:** all numbers mpmath/sympy dps=40 (`/tmp/wave5_verify.py`, `/tmp/wave5_deep.py`, `/tmp/veink_final.py`).
PDG 2024 (lepton masses, |Vus|); NuFIT 6.0 (Sept 2024) mixing; Planck 2018 Ω fractions. NuFIT-6.0 δ_CP status
re-confirmed against the primary paper (arXiv:2410.05380): favored normal ordering is **CP-conserving at ~1σ**;
the 270°/maximal preference (>3.6σ) lives in the **disfavored inverted** ordering.

---

## 1. RANKED LEADS — all three wave-5 veins, best → worst (structural-ness × forced-provenance × surprise)

| Rank | Lead (vein) | Type | Forced? | Weird | One-line verdict |
|---|---|---|---|---|---|
| **1** | **d=3 self-duality of Z** (carried from wave-4, re-affirmed by wave-5 Koide-45 analysis): Z²=32π/**dim SO(3)**, dim SO(3)=3=#vectors=#bivectors; deep-MOND flatness only at d=3 | **structural echo (real, gravity-side)** | **FORCED** (Z-side); flavor link **absent** | **med-high** | The only forced, structural, still-live lead. Wave-5 *strengthens* its boundary: the Koide-45 "3" is N_gen, NOT this spatial-d 3 — they stay category-distinct (see §2A). |
| **2** | **mu-tau reflection** (vein M): the lone genuine single-principle 2-angle object (θ₂₃=45° **and** δ=±90° forced together) | structural (real, published) — **framework-foreign** | n/a (not a framework object) | med | Real physics, the only true multi-angle link in the 45°-cluster — but it predicts the **wrong-handed** δ vs favored NO data, and reaches neither Koide, QLC, nor Z. |
| 3 | **Koide-45** (vein L): √-mass vector at 44.9997° to (1,1,1); cos²=½ ⇔ Q=2/3 | structural (real, sharp) — **NOT NEW**, framework hosts-not-derives | r=√2 amplitude **FREE** | high (sharp) | A real maximal mass-spectrum object; banked. Wave-5 new bit: cos²=½ ⇔ Q=**2/N**, so the 45 is an **N_gen=3** fact, not spatial-d. |
| 4 | **Ω_dm/Ω_L ≈ 3/8** (vein K): 0.3839, the framework's flagged cross-sector rational | numerical value-echo | FREE (3/8 not forced into the ratio) | med→low | **Equidistant** 2.3% / 1.1σ from BOTH 3/8 **and** π/8 — non-diagnostic; cannot tell which (or neither). |
| 5 | **QLC-45** (veins L/M): θ_C + θ₁₂ = 46.61° | numerical, sector-foreign | free; no kernel | low | **2.16σ OFF** 45°; cross-matrix (CKM quark + PMNS lepton); a different object from Koide-45. |
| 6 | **δ_PMNS near-maximal** (vein M): "270°/maximal CP" | numerical (data-stressed) | free; no framework angle | low | Favored NO sin δ = **0.05** (CP-**conserving**); maximal only in disfavored IO. NOT an established maximal angle. |
| 7 | **Ω_dm/Ω_b ≈ 16/3** = the "Z²/2π" mirage (vein K) | numerical (exposed cancellation) | FREE / non-match | low | **CAUTION:** Z²/2π=(32π/3)/2π=16/3 — **π cancels**, Z's geometry never enters; Z itself is 7.9% off. Do NOT cite "Z explains dm/baryon." |
| 8 | **Mass-ratio bare scan + log-ladder** (vein L) | numerical (NULL) | n/a | low (null) | No mass ratio within 3% of any framework number; no constant log-ladder. Clean null. 17/9 (free) wins the quadratic near-ladder. |
| 9 | **FDR-exhaustion meta-result** (vein K) | methodological (a density calc) | n/a | low (it's the proof) | Depth-2 framework pool tiles [0.03,12] at ~18.6/e-fold ⇒ ~8.4/10 Ω-ratios EXPECTED a sub-5% hit by chance; actual 5/10 = **no better than chance**. |
| 10 | **Ω_b/Ω_m ≈ 1/2π, Ω_m ≈ 1/π, Ω_dm/Ω_m ≈ 17/20** (vein K) | numerical value-echoes | free | low | 2π/π ubiquitous; plain rationals; textbook density-baked echoes. |
| 11 | **Strong-CP θ̄, η_B baryon asymmetry vs Z** (vein M) | numerical (NULL) | n/a | low (null) | No forced framework factor near θ̄≈0 or η_B≈6×10⁻¹⁰. Expected null. |

**Net of the three veins:** wave-5 surfaced **no new forced kernel** in any of cosmology-density, mass-ratio, or CP/baryogenesis
sectors — the same wall as PARTICLE_BRIDGE_FRESH_EYES (gravity forces √(8π/3); these sectors have no analogous forced kernel).
Every numerical match is a bare value-echo of a high-FDR ratio with no mechanism tying it to √Λ. The one durable structural
lead remains the gravity-side d=3 self-duality (wave-4), and wave-5's contribution is to *sharpen its boundary* and to *settle*
the maximal-mixing question with the new CP data.

---

## 2. DEEP-EXPLORE — the top 2

### TOP 1 — is the "45° / maximal-mixing" 3 the SAME 3 as the framework's d=3 self-duality? (the unification test)

This is the single most valuable thing wave-5 could test, because it is the *only* route by which the wave-4 top lead
(d=3 self-duality of Z) and the 45°-cluster could become **one object** rather than two. If the Koide-45 "3" were the
framework's spatial-d=3 / dim SO(3), the framework would suddenly *reach* the flavor sector. Sympy-exact result
(`/tmp/wave5_deep.py`):

**The Koide-45 maximality maps to N_generations, not spatial dimension.** The axis-angle of the √-mass vector to the
democratic (1,1,…,1) axis in ℝᴺ satisfies **cos²(angle) = 1/(N·Q)**. The "45°" condition cos²=½ is therefore
> **Q = 2/N** (sympy-exact, N-general).

For N=3 generations this is **Q = 2/3** — the observed Koide value. So the Koide 45° is a statement that the singlet
carries exactly half the √-mass-vector length² **for a 3-flavor system**, i.e. it ties to **N_gen = 3 (internal flavor
count)**. The framework's Z carries a **different** 3: dim SO(3) = d(d−1)/2 at d=3 = the spatial-rotation-group dimension
(the #vectors=#bivectors self-duality, `Z²=32π/dim SO(3)`). These are **category-distinct**:

- **Z's 3** is the dimension of *large-space* rotations (gravity/Friedmann factor d(d−1)).
- **Koide's 3** is the *internal* fermion-generation count.

No forced operator maps large-space SO(3) bivectors to 3 chiral generations: Coleman–Mandula factorizes spacetime ×
internal symmetries, and chirality/index theorems put generations on internal/compact dimensions, not on the large-space
SO(3). **So the route that could have unified the two top threads is closed** — they share the integer 3 but not a
geometric object. This is a clean both-ways result: it *credits* that Koide-45 is a genuine maximal object with a clean
N-dependence (cos²=½ ⇔ Q=2/N, exact), and it *refuses* the tempting "both are the framework's 3" unification, naming
exactly why (internal N_gen vs external spatial-d, blocked by Coleman–Mandula).

**Real or dissolves?** The Koide-45 ⇔ Q=2/N identity is **real and sympy-exact** and is a *new, sharper* way to state why
2/3 is special (it is the N=3 maximal value). But it dissolves as a *framework* bridge: the framework derives neither
N=3 nor the amplitude r=√2 (CLOSED: KOIDE_FROM_DSUNRUH; r=√2 is the non-covariant p=0 measure chosen because it hits 2/3).
**Next concrete step (gravity-side, the live one):** the load-bearing test stays the wave-4 question — derive the
deep-MOND interpolation *form* (not just the coefficient) in d≠3 from the framework's own surface-gravity/dS-Unruh posit
and check whether the **form** carries dim SO(d). If the existence of a MOND transition scale *requires* #vectors=#bivectors,
d=3 is selected by "having a MOND scale at all" — a new consistency-level reason for d=3. The flavor side has no next step
(no forced kernel; Koide CLOSED).

### TOP 2 — mu-tau reflection: the one real multi-angle object, under NuFIT-6.0 stress (vein M's "chase harder" lead)

Vein M's flagged lead — near-maximal δ_PMNS joining the 45°-cluster — resolves to the **μ-τ reflection symmetry**
(ν_μ ↔ ν_τ*), which is the **one genuine single-principle link** in the whole 45°-set: the single breaking pattern forces
θ₂₃ = π/4 **and** δ = ±π/2 = 270° **simultaneously**. This is real, published physics (arXiv:2604.06384, 2006.01639), and
it is correctly *credited* — it is not numerology, it is a discrete symmetry with a 2-angle prediction. Two independent
stress tests, both-ways:

1. **Data stress (favored ordering kills the maximal δ).** NuFIT-6.0 favored **normal** ordering is consistent with
   **CP conservation at ~1σ** (best-fit δ ≈ 177°, sin δ = **0.052** — re-verified dps=40 and against arXiv:2410.05380).
   The 270°/maximal preference (>3.6σ) survives **only in the disfavored inverted** ordering. So the very principle that
   links θ₂₃ and δ predicts the **wrong-handed** δ vs the favored data — μ-τ reflection is itself **under pressure**, and
   "near-maximal leptonic CP" is a **still-uncertain, ordering-dependent** measurement, NOT an established maximal angle.
   θ₂₃ compounds this: its octant **flips** across datasets (48.5° no-SK / 43.3° w-SK), straddling 45° rather than sitting
   on it.

2. **Reach stress (it touches only 2 of 4, none in the framework).** μ-τ reflection is a *neutrino-mixing* statement. It
   says **nothing** about Koide (charged-lepton √-mass spectrum, a different space), **nothing** about QLC (a θ_C + θ₁₂
   sum across the CKM **and** PMNS matrices), and **nothing** about the framework's Z (a gravity/measure object). No single
   symmetry in the literature unifies mass-spectrum geometry + neutrino-mixing + quark-lepton complementarity; the data
   already strain even this partial 2-angle picture.

**Real or dissolves?** μ-τ reflection is **real** and is the correct home for the "two near-maximal angles together"
intuition — but it is **framework-foreign** and **data-stressed**, so it does not become a framework result and does not
elevate the 45°-cluster to a principle. **No next step inside the framework** (the framework supplies no μ-τ symmetry,
no 45°/270° angle, by Coleman–Mandula the gravity Z cannot weight the internal flavor S₃).

---

## 3. SPECIAL FOCUS — is there a MAXIMAL-MIXING / near-45° PRINCIPLE across the flavor sector?

### VERDICT: **(B) SUGGESTIVE leaning ACCUMULATION** — one real 2-angle object (μ-τ, framework-foreign, data-stressed); the rest is unrelated near-maximal values clustering at an attractor. **No single principle unifies the set, and the framework derives none of it.**

This consolidates wave-4 (which already landed SUGGESTIVE) with wave-5's new CP data and the new cos²=½⇔Q=2/N identity. The
honest tally, at **current** precision, of the four candidate near-maximal angles:

| angle | value (dps=40) | distance to maximal | clean? |
|---|---|---|---|
| **Koide-45** (axis-angle to (1,1,1)) | **44.9997°** | 0.9σ; crosses 45° at upper m_τ edge (44.99944 → 45.00003 across the ±0.12 MeV band) | **YES — cleanly maximal** |
| **θ₂₃** (PMNS 2-3) | 48.50° (no-SK) / 43.28° (w-SK) | octant **flips** across datasets; straddles 45° | ambiguous |
| **QLC** (θ_C + θ₁₂) | **46.61°** | **+1.61° = 2.16σ** (θ₁₂-dominated σ≈0.745°) | **NO — 2σ off** |
| **δ_CP** (leptonic) | ~177° favored NO | sin δ = **0.052** → CP-**conserving** in favored ordering | **NO — maximal only in disfavored IO** |

**Cleanly maximal to current precision: 1 of 4 (Koide only).** One straddles (θ₂₃), two are not maximal (QLC, δ_CP).

**Why SUGGESTIVE, not ACCUMULATION (the credit — don't high-priest):**
- **μ-τ reflection is real single-principle physics** linking θ₂₃ = 45° AND δ = ±90° — a genuine 2-angle object, not a
  coincidence. Its existence is what keeps the verdict above pure accumulation.
- **S₃ genuinely appears in BOTH the Koide and the neutrino-mixing literatures** — the verbal/structural resonance is not
  nothing.
- **Koide-45 is sharp and real** (0.9σ, crosses 45° inside the m_τ band), and wave-5's cos²=½ ⇔ Q=2/N identity makes its
  maximality cleaner, not weaker.

**Why it leans ACCUMULATION, not a PRINCIPLE (the refusal — don't manufacture):**
- **The four live in (at most) three different spaces** sharing only the *number* 45: √-mass ℝ³ (Koide), PMNS-mixing
  (θ₂₃, δ), and a CKM+PMNS angle-sum (QLC). **No single symmetry unifies them** — μ-τ reaches at most 2, and reaches
  neither Koide nor QLC nor Z.
- **45° is the symmetric ATTRACTOR / fixed point of any Z₂-symmetric 2-state mixing**, so unrelated angles drift toward it
  *independently* for selection/symmetry reasons. Co-occurrence near 45° is the **expected background**, not evidence of
  one principle.
- **The data weakened the pattern** (NuFIT-6.0, not the prompt's 5.3): θ₂₃ octant ambiguous; δ_CP CP-conserving in the
  favored ordering; QLC 2.16σ off. Only Koide survives as cleanly maximal.
- **The framework derives none of it.** It hosts the Koide *shape* via Spin(8)-triality/S₃ (1+2 decomposition, Q=1/3+r²/6,
  exact for *any* r), but r=√2 is a **free** interior modulus, and by Coleman–Mandula the gravity-side Z cannot weight the
  internal flavor S₃. The wave-5 unification test (§2A) confirms the Koide "3" (N_gen) is **not** the framework's spatial-d
  "3" (dim SO(3)).

**Bottom line:** one real, published, *framework-foreign*, *data-stressed* 2-angle object (μ-τ reflection: θ₂₃ ↔ δ_CP);
one clean mass-sector 45° (Koide) the framework hosts-but-does-not-derive; two weak/non-maximal members (QLC at 2.16σ,
δ_CP CP-conserving in the favored ordering). **No cross-space principle; the near-45° co-occurrence is the attractor
background plus one real neutrino-sector symmetry that does not reach the framework.** Verdict: SUGGESTIVE-leaning-
ACCUMULATION, both-ways.

---

## 4. SINGLE BEST LEAD TO CHASE NEXT

**Chase: the d=3 self-duality of Z — is the SO(3) vector≅bivector self-duality LOAD-BEARING in the MOND modification, or decorative?** (carried from wave-4 Top-1, and now the *only* lead wave-5 left standing after the maximal-mixing question closed.)

**Why this one (and not any flavor lead):**
- It is the **only forced, structural, genuinely under-explored** lead in the corpus. `Z²=32π/dim SO(3)` is sympy-exact;
  dim SO(3)=#vectors=#bivectors is a theorem; deep-MOND flatness-only-at-d=3 is standard physics — all three flow from the
  single fact d(d−1)/2 = d at d=3. That is the **a₀ template** (scale × forced geometric factor), the opposite of
  numerology.
- **Every flavor lead is closed or dissolved by this wave:** the maximal-mixing "principle" is SUGGESTIVE-leaning-
  accumulation with no framework reach (§3); Koide is CLOSED and re-labeling-dead; the Koide-45 "3" is N_gen not spatial-d
  (§2A); μ-τ is real but framework-foreign and data-stressed (§2B); QLC is 2.16σ-off and sector-foreign; the Ω-density
  echoes are FDR-exhausted (chance-level); the "Z²/2π ~ Ω_dm/Ω_b" is a π-cancellation mirage (do NOT cite); strong-CP and
  η_B are clean nulls.
- The test is **decisive either way**: derive the deep-MOND interpolation *form* in d≠3 from the framework's **own**
  surface-gravity/dS-Unruh posit (not borrowed AQUAL) and check whether the **form** (not just the coefficient) carries
  dim SO(d). If the existence of a MOND transition scale *requires* #vectors=#bivectors, then d=3 is **selected by the
  consistency of having a MOND scale at all** — a new (consistency-level, not first-principles) reason for d=3 the corpus
  does not yet have. If the form is d-agnostic, the self-duality is an elegant restatement and we say so. Both outcomes
  are real, non-manufactured progress.

**Honest caveat carried forward:** even the best case is a **consistency/selection** statement about why d=3 is special for
*having a MOND scale* — NOT a derivation of d=3 from below (still external: Ehrenfest stability / anthropics) — and it
provides **no flavor bridge** (generations stay internal, Coleman–Mandula). It sharpens the framework's geometric story;
it does not cross a wall.

---

*Sources for the NuFIT-6.0 δ_CP status:* [NuFit-6.0 (arXiv:2410.05380)](https://arxiv.org/abs/2410.05380),
[JHEP 12 (2024) 216](https://link.springer.com/article/10.1007/JHEP12(2024)216).
*All numbers reproduced at mpmath/sympy dps=40 in `/tmp/wave5_verify.py`, `/tmp/wave5_deep.py`, `/tmp/veink_final.py`.*
