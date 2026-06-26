# Koide "channel-count / flat-over-irreps" smuggle-check — ADVERSARIAL VERDICT

**Date:** 2026-06-25
**Role:** dedicated SKEPTIC (both-ways: tried hardest to break it; report if it survives).
**Tooling:** sympy 1.13.1 + mpmath dps≥30 for every group-theory and numeric claim.
**Quarantine held:** 2/3, √2, r appear only as the empirical target to be matched — never as input.

---

## VERDICT: (B) RE-LABELING — the 170th.

"Koide = flat/equipartition over the 2 S3 irrep CHANNELS {singlet, doublet}" is a restatement
of "r=√2 is free," not a new forced target. It dies on **two independent smuggles**, either of
which is fatal, plus a falsifying cross-fermion guard:

1. **The MEASURE smuggle (decisive).** "Flat over channels" is NOT any covariant/thermal/
   group-theoretic measure. Every covariant principle — Plancherel, regular-rep, Gibbs over an
   S3-invariant Hamiltonian, Haar on the orbit, equivariant localization — reduces to
   **dimension weighting = per-STATE = r=2 = Q=1 (the known dS-Unruh overshoot).** To land on
   r=√2 you must hand-pick "count irreps, ignore their dimension," and that choice is selected
   *because* it hits 2/3.
2. **The lepton-selector smuggle (independent kill).** Quarks carry the **same** S3 3-generation
   structure but Q_up≈0.849, Q_down≈0.731 ≠ 2/3. The principle must be switched off for quarks
   by hand; the S3 structure supplies no selector. A principle you must disable for 2 of 3
   sectors is not a principle.

The one thing that genuinely IS forced — the **objects** {singlet=trivial, doublet=standard} —
is real rep theory and not a smuggle. But forcing the objects is not forcing the *equipartition*;
the free parameter r just got relabeled from "the doublet/singlet ratio" to "the measure exponent p."

---

## The single decisive identity (smoking gun)

Allocate the √-mass energy budget with weight ∝ dim(irrep)^p (singlet dim 1, doublet dim 2):

| p | name | r | Koide Q |
|---|------|---|---------|
| **0** | **flat-over-channels (ignore dim)** | **√2** | **2/3  ← the target** |
| 1 | Plancherel / per-state / thermal | 2 | 1 (overshoot) |
| 2 | regular representation | 2√2 | 5/3 |

`r = √(2^{p+1})`, sympy-exact. **The Koide value is the p=0 endpoint** — the *only* non-covariant
member of the family. Both genuinely group-theoretic measures (p=1, p=2) miss it. Choosing p=0
is choosing the answer. This is the whole smuggle in one line.

---

## Part 0 — Core identity (VERIFIED sympy-exact, not in dispute)

For v=(√m_e,√m_μ,√m_τ), decomposing along the democratic axis n=(1,1,1)/√3 (S3 trivial irrep)
and its orthogonal complement (S3 standard 2-dim irrep):

- |singlet|² = (a+b+c)²/3,  |doublet|² = Σ(2a−b−c)²/9 (their sum = |v|², checked = 0 residual).
- Koide Q = |v|²/(a+b+c)² = (|singlet|²+|doublet|²)/(3|singlet|²).
- **|singlet|² = |doublet|² ⟹ Q = (S+S)/(3S) = 2/3 exactly**, and with the prompt's normalization
  this is **r=√2** (solve 3M² = 3M²r²/2 → r=√2). All confirmed. The equivalence chain is real.

So the *math* is right. The question is whether "|singlet|²=|doublet|²" is *forced*. It is not.

---

## Part 1 — Is channel-count "2" FORCED or CHOSEN? (sympy character tables)

Built S3 and A4 character tables and decomposed the flavor reps from first principles
(multiplicity = (1/|G|)Σ|class|·χ_perm·χ_irrep):

- **S3, natural 3-dim perm rep:** χ = (3,1,0) on classes (e,(12),(123)) → **trivial⊕standard**
  (sign multiplicity = 0). → **2 channels** {singlet(1), doublet(2)}, 3 states. → r=√2, Q=2/3.
- **A4, irreducible 3** (the standard A4 flavor assignment for 3 generations): a **single** irrep
  → **1 channel**. The singlet/doublet equipartition argument **does not even apply**.
- **A4 as 1⊕1′⊕1″, or 3×U(1):** 3 distinct 1-dim channels = **3 channels = 3 states** → r=2, Q=1.

**Honest answer:** the *objects* {singlet,doublet} ARE forced **once you commit to S3 + its
natural-3 decomposition**. S3 is defensible as the generic permutation symmetry of three
identical-gauge-charge copies (the FOR steelman is real: democratic (1,1,1) is the unique trivial
irrep, not arbitrary). **BUT the channel COUNT "2" is not group-invariant** — it is 1 under A4-3
and 3 under A4-(1+1+1)/U(1)³. "Count=2" ⟺ "pick S3 AND its 1+2 split," and A4 is an equally-used
flavor group giving a different count. The S3 that would force count=2 is *badly broken* by the
very 1:200:3500 mass hierarchy being explained — it cannot be invoked to fix a measure to
part-per-10⁴ while being violated by 3 orders of magnitude. **Partial smuggle on the count;
full smuggle on the measure (Part 2).**

---

## Part 2 — Is "flat-over-irreps" a FORCED measure? (maxent, sympy)

Constructed the actual Shannon maxent over channel probabilities {w_s, w_d}, w_s+w_d=1:

- **Flat base measure over the 2 irrep LABELS:** maxent → w_s=w_d=1/2 = per-channel = **r=√2, Q=2/3**.
- **Dimension base measure (d_s=1, d_d=2, = Plancherel / relative entropy):** maxent → w_s=1/3,
  w_d=2/3 = per-STATE = **r=2, Q=1 (overshoot)**.

"Flat over channels" requires choosing the **uniform-over-irrep-labels** base measure — treating
a 1-dim and a 2-dim irrep as equiprobable a priori. **The canonical group-theoretic base measure
is Plancherel (weight = dim), which is per-state, which overshoots.** Tested every covariant
candidate (Plancherel, regular rep, S3-invariant Gibbs/thermal, Haar on the orbit, equivariant
localization) — **all reduce to dimension weighting = per-state**. None of them naturally weights
uniform-per-irrep. The per-channel measure has to be **input by hand**, and the only motivation to
input it is that it reproduces 2/3. **This is the load-bearing smuggle.**

(Note the irony: the dS-Unruh thermal bath the framework actually owns gives per-STATE flat =
r=2 = Q=1 = the documented overshoot. The "fix" to 2/3 is exactly the step that throws away the
thermal/covariant measure.)

---

## Part 3 — Cross-fermion guard (mpmath, PDG masses)

Same S3 3-generation structure in all sectors; "flat over 2 S3 channels" predicts Q=2/3 everywhere:

| sector | Q (Koide) | vs 2/3 |
|--------|-----------|--------|
| charged leptons (e,μ,τ) | 0.666661 | ≈ 2/3 (the famous coincidence) |
| up quarks (u,c,t)       | 0.848981 | FAR off — outside ±30%-mass band entirely |
| down quarks (d,s,b)     | 0.731428 | FAR off — only grazes 2/3 at extreme errors |

The mismatch is robust to ±30% quark-mass uncertainty (up: Q∈[0.806,0.884], down: Q∈[0.669,0.787]).
**A pure S3-channel-equipartition principle is falsified by quarks.** Saving it for leptons needs a
hand-imposed lepton-selector that the S3 structure does not contain.

**Lepton-selector status: ABSENT (must be hand-imposed → fatal).**

---

## Bottom line

- **Forced:** the decomposition objects {singlet=trivial, doublet=standard} of v under S3-natural-3.
- **Smuggled (count):** "2 channels" requires choosing S3+1+2 over A4-3 (1 channel) or U(1)³ (3).
- **Smuggled (measure, decisive):** "flat-over-channels" = the p=0 / ignore-dimension measure, the
  unique non-covariant member of the dim^p family; every covariant measure gives r=2 (overshoot).
- **Falsified (selector):** quarks share the S3 but give Q≠2/3; no lepton-selector exists.

Net: this is **"r=√2 is free"** restated as **"the measure exponent p is free, and p=0 happens to
hit Koide."** Consistent with the corpus standing (PARTICLE_BRIDGE_FRESH_EYES: S3/triality gives
the 1+2 decomp but leaves r free; 164 re-labelings; "automatic Koide" false). This is the 170th.

**The single un-smuggled question that would actually be open (if anyone wants the C-path):**
Is there a *dynamical* (not statistical) reason the symmetry-breaking ("doublet") sector and the
democratic ("singlet") sector carry equal √-mass norm — e.g. an IR fixed point or a Sumino-type
gauge-boson mechanism that *protects* |singlet|²=|doublet|² **and is charged-lepton-specific**?
That is the genuine open lead — but it is a search for a *new lepton-selective protector*, NOT
something the "flat-over-channels" relabeling supplies. The relabeling itself is dead.
