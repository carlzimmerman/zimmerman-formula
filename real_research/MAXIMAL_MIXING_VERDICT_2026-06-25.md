# The Maximal-Mixing / 45° Pattern — Both-Ways Verdict

**Date:** 2026-06-25
**Framework:** a₀ = c²√(Λ/32π), Z = √(32π/3); hosts the Koide *shape* via Spin(8)-triality's 1+2 S₃ decomposition but does **not** derive the Koide amplitude (that route is CLOSED — KOIDE_FROM_DSUNRUH, re-confirmed wjx8gedyb).
**Data:** PDG 2024 (lepton masses, |Vus|), NuFIT 6.0 (Sept 2024, supersedes 5.3). All angles recomputed at mpmath dps=40.

---

## VERDICT: (B) SUGGESTIVE — real mixing-sector pattern (mu-tau), framework hosts the neighborhood only, Koide is a DIFFERENT object

The four near-maximal angles are **NOT one geometric object**. There is **one genuine single-principle link** in the set, and it lives entirely in the **neutrino-mixing sector** (mu-tau reflection ties θ₂₃ and δ_CP), which the framework **does not supply**. Koide's 45° is a **mass-spectrum** object in a different space; QLC is a third object (a quark+lepton angle sum); and to *current* precision only Koide is cleanly maximal. So: a real, published, two-angle mixing-sector pattern — credited, not high-priested away — but **no cross-space principle unifies all four, and the framework derives none of them.**

This sits between pure ACCUMULATION and a GENUINE cross-framework PRINCIPLE, and lands on SUGGESTIVE because (i) the mu-tau θ₂₃↔δ link is real physics, not coincidence, but (ii) it does not reach the framework, the mass sector, or QLC.

---

## The four angles, recomputed (dps=40)

| # | Angle | Value | Dev from 45°/270° | Verdict on "maximal" |
|---|-------|-------|-------------------|----------------------|
| (1) | **Koide** — (√mₑ,√m_μ,√m_τ) to (1,1,1) axis | **44.99974°** | −0.00026° (0.9σ) | **EXACT** (axis-angle reading); crosses 45 at upper m_τ edge |
| (2) | **QLC** — θ_C + θ₁₂ | **46.61°** | +1.61° = **2.25σ** | mild tension, NOT clean |
| (3) | **θ₂₃** — PMNS 2-3 rotation | 48.50° (no-SK) / 43.28° (w-SK) | +3.5° / −1.7° | **octant flips across datasets** |
| (4) | **δ_CP** — leptonic CP phase | ~177° NO best / ~285° IO | NO ≈ CP-**conserving** | maximal only in disfavored IO |

Key computed identities (sympy/mpmath-exact):
- Koide axis-angle: cos²(to axis) = 1/(3Q), Q = 0.6666605 → 0.500005 → **44.99974°**. The *other* common reading, arccos(√Q) = **35.26°**, is NOT 45 — the 45 is the **axis-angle reading only**.
- m_τ band (1776.86 ± 0.12 MeV): axis-angle runs 44.99944° → 45.00003°, i.e. 45 is **inside the band**, reached at the upper edge.
- QLC: θ_C = asin(0.22431) = 12.96°, θ₁₂ = asin(√0.307) = 33.65°, sum = 46.61°, σ ≈ 0.72° (θ₁₂-dominated) → **2.25σ off 45**.

---

## Which angles are linked by ONE principle vs independent

**GENUINELY LINKED (one principle): θ₂₃ ↔ δ_CP, via mu-tau REFLECTION symmetry (ν_μ ↔ ν_τ\*).**
This is real, published physics ([arXiv:2604.06384](https://arxiv.org/abs/2604.06384), [arXiv:2006.01639](https://arxiv.org/abs/2006.01639)): the *single* breaking pattern forces **both** θ₂₃ = π/4 **and** δ = ±π/2 simultaneously. This is the one real multi-angle object in the set. Caveat (both-ways): it predicts δ = ±90°, but NuFIT 6.0 normal-ordering (favored) sits near δ ≈ 177° (CP-**conserving**); maximal δ survives only in the disfavored inverted ordering — so the very principle that links the two is itself **under data stress**.

**INDEPENDENT — different space, no shared symmetry:**
- **(1) Koide** is a **mass-spectrum** statement: a 45° of the √-mass vector in ℝ³ of the *charged leptons* — an eigenvalue/Yukawa-magnitude fact, **no mixing matrix, no neutrino content**. mu-tau and TBM/A4/S4 say nothing about it. It lives in the charged-lepton mass sector (U(3)×SU(2) family-gauge / democratic-mass mechanisms). The literature treats charged-lepton Koide-Q and maximal θ₂₃ as "related but separate," needing *extra* inputs (a Koide-for-neutrinos hypothesis) to bridge — **no single symmetry derives both.**
- **(2) QLC** is a **third** object: θ_C (CKM/quark) + θ₁₂ (PMNS/lepton) summed *across two different mixing matrices*, bridged only by quark-lepton unification (e.g. D₁₂/GUT). It is **not** mu-tau (which is silent on θ₁₂ and on quarks) and **not** Koide. Literature: "no straightforward GUT realization," accidental-vs-fundamental **open** ([hep-ph/0505262](https://arxiv.org/abs/hep-ph/0505262)).

**Tally:** at most **2 of 4** share one object (θ₂₃ & δ_CP, neutrino-mixing mu-tau); Koide and QLC are each independent. A single principle linking **all four** would have to unify mass-spectrum geometry + neutrino-mixing symmetry + quark-lepton complementarity at once — **no such symmetry exists in the literature**, and the data already strain even the partial picture.

---

## Is the framework hook real, beyond hosting the shape? (stress-tested)

**No.** The framework's Spin(8)-triality / S₃ / 1+2 decomposition touches **exactly one** of the four — the **Koide mass 45 (1)** — and only as a **shape host**:
- The S₃ 1+2 (1 democratic + 2 standard) decomposition forces the Koide *shape* (circulant/equally-spaced), giving **Q = 1/3 + r²/6**, which is **sympy-exact for ANY amplitude r**.
- Q = 2/3 ⇔ r = √2 ⇔ the 45°. But **r = √2 is an ordinary interior modulus that NOTHING in the geometry forces** — not positivity, not 2/N_gen, not the phase (orthogonal). dS-Unruh per-state equipartition gives r = 2/Q = 1 (overshoot), and Coleman-Mandula blocks the spacetime horizon character from weighting the internal S₃ family. So the framework sits in the **S₃ shape neighborhood, not a dynamical mu-tau.**
- For QLC, θ₂₃, δ_CP the framework has **no hook at all**: these are PMNS/CKM mixing objects, and the Yukawa/mixing sector has **no forced kernel** (the cosmology trick does not transfer — gravity forces √(8π/3); the Yukawa sector has no analogous forced kernel; PARTICLE_BRIDGE_FRESH_EYES).

The "democratic axis / (1,1,1) / S₃" resonance between Koide (1) and θ₂₃ (3) is **verbal/structural** — S₃ does appear in *both* the Koide and the neutrino-mixing literatures, which is why this is SUGGESTIVE not pure ACCUMULATION — but it is not a single symmetry deriving both, and the framework's specific contact is a **re-labeling** of an established Koide-geometry observation with the amplitude left free.

---

## Both-ways honesty ledger

**Credited (did NOT high-priest the real pattern):**
- mu-tau reflection is real, published, single-principle physics linking θ₂₃ = 45 AND δ = ±90 — flagged as the genuine 2-body object, not dismissed as numerology.
- S₃ genuinely appears in both the Koide and the θ₂₃ literatures → the resonance is not nothing → verdict is SUGGESTIVE, not ACCUMULATION.
- Koide's exactness is real (44.99974°, 0.9σ, crosses 45 inside the m_τ band).

**Refused to manufacture (did NOT invent a win):**
- **No** single symmetry links all four; the four live in (at most) three different spaces sharing only the number 45.
- **Upgraded the data honestly** — NuFIT 6.0 (not the prompt's 5.3) makes maximality **weaker**: θ₂₃ octant flips 48.5/43.3 across datasets; δ_CP drifts to ~177° (CP-conserving) in the favored NO; 270/maximal survives only in disfavored IO. I did not soften this to protect the pattern.
- QLC is the **weakest** (2.25σ off 45) and is sector-foreign to mu-tau.
- Koide's 45 is **load-bearing-empty for the framework**: r = √2 restated, an amplitude the framework's own CLOSED analysis does not derive (drifts +0.18%/178σ under running); and 45 is one of two readings (the arccos(√Q) = 35.26° reading is not 45).
- The one genuine link (mu-tau → δ = ±90) predicts the **wrong-handed** δ vs current NO data — the principle itself is under pressure.

---

## Bottom line

One real two-angle link (mu-tau reflection: θ₂₃ ↔ δ_CP, neutrino sector) that the framework does **not** supply; one clean mass-sector 45 (Koide) the framework **hosts but does not derive**; two weaker/sector-foreign 45s (QLC at 2.25σ; δ_CP which is CP-conserving in the favored ordering). **No single principle unifies all four; they are not one geometric object.** Verdict: **SUGGESTIVE — mixing-sector pattern real, framework hosts the neighborhood only.**
