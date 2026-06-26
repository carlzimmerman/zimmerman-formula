# Weirdness Ledger — Exploration Wave 4

**Date:** 2026-06-25
**Framework:** a₀ = c²√(Λ/32π) = cH_Λ/Z, Z = √(32π/3) = 5.78881, kernel = (3/8π)^(1/4) = √(2/Z) = 0.587788.
**Mandate:** hunt the weird on FRESH ground (Koide-derivation routes CLOSED — not re-run). Rank by surprise × structural-ness × forced-provenance; a structural echo or a forced scale-bridge outranks a bare value-match. Both-ways: don't high-priest a real pattern, don't manufacture a coincidence into a proof.
**Verification:** all numbers mpmath/sympy at dps=40 (`/tmp/w4_verify.py`, `w4_deep.py`, `w4_deep2.py`, `w4_selfdual.py`, `w4_45.py`). PDG 2024 lepton masses + |Vus|; NuFIT 6.0 mixing.

---

## 1. RANKED LEADS (best → worst by structural-ness × forced-provenance)

| Rank | Lead | Type | Forced? | Weird | One-line |
|---|---|---|---|---|---|
| **1** | **d=3 self-duality of Z**: Z² = 32π/**dim SO(3)**, and dim SO(3)=3=#vectors=#bivectors (cross product); deep-MOND flat curves occur **only** at d=3 | **structural echo (real, gravity-side)** | Z-side **FORCED**; flavor link **absent** | **med-high** | Three independent d=3 facts converge inside Z — but the 3 is spacetime-d, not generations |
| **2** | **8π/3 = π/sin²θ_W,tree = π/(3/8)**: gravity's 3/8 (= d(d−1)/16π at d=3) vs gauge's 3/8 (= GUT hypercharge norm 3/5→3/8) | structural-leaning rational collision | both sides forced **in their own sector**; cross-π **not** forced | medium | Same exact rational 3/8, genuinely different origin; one bare π apart |
| **3** | **Koide-45**: √-mass vector at 44.99974° to (1,1,1); cos²=½ ⇔ Q=2/3 ⇔ singlet=doublet power (S₃ equipartition) | structural (real, sharp) — but **NOT NEW** | r=√2 amplitude **FREE** | high (sharp) | A real maximal mass-spectrum object; already banked, framework hosts-not-derives |
| 4 | **QLC-45**: θ_C + θ₁₂ = 46.61° | numerical, sector-foreign | free; no kernel | low | 2.16σ OFF 45°; a different object from Koide-45 |
| 5 | **α⁻¹ = 4Z²+3 = 137.041** | numerical (failed) | FREE (+3 fudge) | low | The canonical FDR-dead BriareusFlow artifact; re-confirmed dead, ~2.5×10⁵σ off real α |
| 6 | **N_gen 3 = spatial d 3** | numerical (3=3) | cross-map absent | low | Category error: spacetime-dim vs internal flavor; different 3s |
| 7 | **dS SO(4,1) vs SM gauge group** | structural (fails) | n/a | low | dim 10/rank 2 ≠ dim 12/rank 4; Z is a measure not a Lie-dim. Clean null |
| 8 | **GUT scale / α_unif vs Z** | numerical (null) | n/a | low | SM doesn't unify; no framework number echoes M_GUT or α_unif. Expected null |

**Note on a header typo I caught:** vein J wrote "8π/3 = 8.378" — that value is the **kernel²-related 8π/3** (=8.3776), which is correct; but it also wrote "Z²=33.51" (correct) elsewhere. Z² = 32π/3 = 33.5103; 8π/3 = 8.3776; these are distinct and both used correctly once disambiguated.

---

## 2. DEEP-EXPLORE — TOP 2

### TOP 1 — d=3 self-duality of Z (the lead the hunt under-rated; pushed further here)

The hunt flagged "dim SO(3)=d=3, vectors≅bivectors" as a *possibility-shaped gap* (med weirdness). Pushing it with sympy makes it **tighter and more structural than that** — and surfaces a third converging d=3 fact the corpus did not have.

**(a) Z literally carries dim SO(3), not a bare integer 3.** The d-dimensional Friedmann equation H² = [16πG/(d(d−1))]ρ gives ρ_crit,d = d(d−1)H²/16πG, so
> **Z_d² = 64π/[d(d−1)] = 32π / [d(d−1)/2] = 32π / dim SO(d).**  (sympy-exact)

At d=3, dim SO(3)=3 ⇒ Z² = 32π/3. The "3" in Z is the **dimension of the rotation group = the number of independent rotation planes (bivectors) = the number of angular-momentum components.** This is stronger than "integer 3 = integer 3": the Friedmann/Einstein dimensional factor d(d−1) is *physically* 2·dim(SO(d)), so the spatial 3 enters Z as a genuine geometric object, not a coincidental digit.

**(b) The self-duality is the cross-product fact.** dim SO(d) = d ⟺ d=3 (sympy: solve d(d−1)/2 = d → d=3). d=3 is the unique dimension where #bivectors = #vectors, which is *why* angular momentum is a 3-vector and the cross product closes. The framework's a₀ is an acceleration (a vector); its source is curvature living on rotation planes (bivectors). The bulk→boundary / curvature→acceleration conversion is dimension-balanced **only** at d=3 — and that balance is exactly the dim SO(3)=3 in Z² = 32π/3.

**(c) NEW converging fact: deep-MOND flat rotation curves exist only at d=3.** Deep-MOND with the d-dimensional Gauss flux g_N = GM/r^{d−1} gives v² ~ r^{(3−d)/2}:
> d=2 → rising; **d=3 → FLAT (v=const)**; d=4 → falling.

Asymptotically flat curves — MOND's signature phenomenology and the whole reason a₀ exists as a scale — are themselves a d=3 fact (standard physics; same neighborhood as Newtonian Fractional-Dimension Gravity, arXiv:2003.05784). So **three independent d=3 statements converge inside this framework**: Z²=32π/dim SO(3); the SO(3) vector≅bivector self-duality; and deep-MOND flatness. They are not three coincidences — they all flow from the single fact that d(d−1)/2 = d at d=3.

**Is it real or does it dissolve?** *Real on the gravity side.* It is a forced, sympy-exact statement that the framework's coefficient sits at the self-dual dimension, and it newly ties MOND's flat-curve signature to the same d=3. It **does not dissolve** — but it also does not become a flavor bridge.

**Honest limit (does not over-reach):** this explains why the *coefficient structure* is special at d=3; it does **not** explain *why* d=3 (still external: Ehrenfest stability / anthropics). And there is **still no flavor hook** — nothing maps the 3 bivectors of large 3-space to 3 fermion generations (chirality and index theorems live on internal/compact dimensions, not large-space SO(3)). The N_gen=3 ↔ spatial-d=3 identification (lead #6) remains a category error.

**NEXT CONCRETE STEP:** Is the bivector↔vector self-duality *load-bearing* in the MOND modification, or decorative? Test by deriving the deep-MOND interpolation in d≠3 from the framework's own dS-Unruh / surface-gravity posit (not just AQUAL) and checking whether the **form** (not just the coefficient) carries dim SO(d). If a₀'s very existence as a transition scale requires #bivectors=#vectors, the self-duality is load-bearing and d=3 is *selected by the consistency of having a MOND scale at all* — a genuinely new (still consistency-level, not first-principles) reason for d=3. If the form is d-agnostic, the self-duality is an elegant restatement, not a mechanism.

### TOP 2 — the 3/8 rational collision (re-verified, origins decomposed)

> **8π/3 = π / sin²θ_W,tree(SU5) = π / (3/8)**, exact (sympy: 3/8 == 3/8 True).

I traced **both** 3/8 to their roots to test whether they are the same geometric object or a rational collision:

- **Gravity 3/8** = kernel⁴·π = (3/8π)·π. The "3/8" is **d(d−1)/16π at d=3** = the FRW critical-density factor (3H²/8πG) — a **spatial-dimension / measure** rational. (Same 3 as Top-1: dim SO(3).)
- **Gauge 3/8** = sin²θ_W at the GUT scale = (3/5)/((3/5)+1), where 3/5 is the **SU(5) hypercharge normalization** (the embedding of weak hypercharge in the 5̄+10). A **group-trace** rational. *(I initially mis-computed Tr(T₃²)/Tr(Q²) over left doublets only → 3/4; the correct full-multiplet GUT-normalized value is 3/8, verified via the 3/5 normalization. The 3 here is the GUT embedding, NOT the spatial dimension.)*

**Verdict:** the two 3/8 share the **exact rational** but **not the structure** — gravity's 3 is the spatial dimension (dim SO(3)); gauge's 3 is the SU(5) embedding factor 3/5. No map sends d(d−1)/16π → Tr(T₃²)/Tr(Q²). It is a **~1-in-100 rational collision** (3/8 has ~1.5% pool density), one bare factor of π apart — the shape of an algebra→horizon (Unruh T=a/2π) map, which is why it *tempts*, but the cross-π is observed, not forced. **Already banked (wave-1); re-verified, not new.** Minimal-SM running misses the measured sin²θ_W(M_Z)=0.23122 by ~11σ (3/8 is the tree/GUT value). **Does dissolve** as a bridge; survives only as a noted resonance.

---

## 3. SPECIAL FOCUS — the 45° echo: Koide-45 vs QLC-45 (straight both-ways verdict)

### VERDICT: **COINCIDENCE of two near-45° angles with unrelated origins.** Not a shared structural principle.

This is the rigorous kill, matched by the rigorous credit.

**The two objects (different spaces, different physics):**

- **Koide-45** lives in **ℝ³ of √-masses** (charged-lepton Yukawa magnitudes). The angle of (√mₑ,√m_μ,√m_τ) to the democratic axis (1,1,1) is 44.99974° (dps=40); cos²=½ ⇔ Q=2/3 ⇔ the **S₃ singlet carries exactly half the vector's length²** (singlet/doublet equipartition). A **mass-spectrum** object. No mixing matrix, no neutrinos.
- **QLC-45** is θ_C (a CKM **quark** mixing angle) + θ₁₂ (a PMNS **lepton** mixing angle) = 46.61°, a sum **across two different mixing matrices**, bridged only by a GUT-scale quark-lepton-complementarity *conjecture* (θ_C ≈ π/4 − θ₁₂).

**KILL (be as rigorous as crediting):**
1. **Different spaces** — √-mass ℝ³ vs a sum of two mixing angles. Not the same geometric object.
2. **No shared symmetry** — S₃ equipartition (Koide) vs quark-lepton complementarity (QLC). mu-τ / A4 / S4 / TBM say nothing about Koide-Q; Koide says nothing about |V_us|. No single symmetry derives both (confirmed against the literature in `MAXIMAL_MIXING_VERDICT_2026-06-25.md`).
3. **Different precision** — Koide-45 is 45° to 6 figures (0.9σ, crosses 45 inside the m_τ band). QLC-45 is **2.16σ OFF** (dev 1.61°, θ₁₂-dominated σ≈0.75°). The pairing is not even sharp.
4. **Both amplitudes free** — Koide's r=√2 is an unforced interior modulus (drifts +0.18%/178σ under running, per the CLOSED dS-Unruh analysis); QLC's complementarity is also unforced.

**CREDIT (don't high-priest):**
- Both are genuinely "maximal" (45° = equal split), and maximality is a recurring, real flavor motif. Koide-45's sharpness is real and the S₃ resonance with the neutrino-mixing literature is why the broader pattern rates *suggestive* (not pure accumulation).
- BUT "both maximal" is a **weak link**: 45° is the symmetric **attractor** of any 2-state mixing, so unrelated angles *cluster* there for selection reasons — co-occurrence near 45° is expected without a shared object. A maximal mass-split and a maximal mixing-sum need not, and here do not, come from one principle.

**Bottom line:** Koide-45 is a real, sharp, single-sector structural object the framework **hosts but does not derive** (and which is **not new** — it equals the wave-1 r=√2 channel-equipartition). QLC-45 is a separate, 2σ-off, cross-matrix object. Pairing them is the **temptation of a shared word ("maximal"), not a shared number to precision.** **Coincidence, not principle.**

---

## 4. SINGLE BEST LEAD TO CHASE NEXT

**Chase: the d=3 self-duality of Z (Top-1) — specifically, is the SO(3) vector≅bivector self-duality LOAD-BEARING in the MOND modification?**

**Why this one (and not the others):**
- It is the only lead that is **forced, structural, and genuinely under-explored.** It passed every both-ways test: Z²=32π/dim SO(3) is sympy-exact; dim SO(3)=#vectors=#bivectors is a theorem; deep-MOND flatness-only-at-d=3 is standard physics — and all three flow from one fact (d(d−1)/2=d at d=3). That is the *a₀ template* (scale × forced geometric factor), the opposite of numerology.
- Every other lead is closed or dissolved: the 3/8 collision (Top-2) is a re-verified ~1-in-100 rational, already banked; the 45° echo is a coincidence (§3); α⁻¹=4Z²+3 is FDR-dead; N_gen=spatial-d is a category error; the gauge/GUT/dS-group hunts are clean nulls.
- The concrete test is **decisive either way**: derive the deep-MOND interpolation form in d≠3 from the framework's **own** surface-gravity/dS-Unruh posit (not borrowed AQUAL). If the *form* (not just the coefficient) requires #bivectors=#vectors, then the existence of a MOND scale **selects** d=3 — a new, consistency-level reason for d=3 that the corpus does not yet have. If the form is d-agnostic, the self-duality is decorative and we say so. Both outcomes are real progress; neither manufactures a win.

**Honest caveat carried forward:** even the best case is a **consistency/selection** statement about why d=3 is special for *having a MOND scale*, NOT a derivation of d=3 from below, and it provides **no flavor bridge** (generations stay internal). It would sharpen the framework's geometric story, not cross a wall.
