# J10 — THE FRAMEWORK-CORE READING: atom + lag as an a₀-radius measurer

**2026-09-23 · moment channel → framework core · follows K01 audit (GO items) + J09 (verified 27/27)**

## 1. The chain (everything already verified, nothing new invented here)

| step | statement | status |
|---|---|---|
| (1) | frozen Theorem 1: c·E[D]·(R/c) = E[D]·R is the **mean geometric delay** of a scattering token in a cloud of radius R | frozen lane, exact |
| (2) | J09-C atom: A = P(no scatter) = exp(−τ₀(1+q/3)), central source | J09 verified (0.36826 vs 0.36788) |
| (3) | J09-D window: −ln A / E[D] = (1+q/3)/(½+q/4) ∈ **[4/3, 2]** | J09 verified (2.0022 / 1.4413 / 1.5980) |
| (4) | **framework core:** the BLR cloud sits at the a₀-radius **r_B = √(GM_b/a₀(ρ_B))** — the density-LOCAL reading of the one-boundary statement (doorB: 40.9 ld vs 45 ld, CONSISTENT-OPEN; NOT the deep-MOND √(GM/a₀) = kpc-scale radius) | ONE_BOUNDARY_STATEMENT / doorB / G_SYNTH S1 |

Combining (1)+(3)+(4): the dimensionless E[D] is *observed* as the physical lag
d̄_phys = E[D]·R/c, and the framework supplies R = r_B = √(GM_b/a₀(ρ_B)).
Therefore

```
    −ln A · √(GM_b / a₀(ρ_B)) / (c · d̄_phys)   ∈   [4/3, 2]           (J10-I)
```

**J10-I is the core-tied falsifier of the transfer-function channel:**
- A  measured from the zero-lag zero-width spike (the atom),
- d̄_phys measured from the lag of the broad-line response,
- M_b, ρ_B measured/known — OR the pair inverted to (τ₀, q) first,
- a₀(ρ_B) = (c/2)√(Gρ_B)·(MOND-adjacent density-local law) — **the framework
  constant at the layer, nothing else.**

A measured J10-I ratio outside [4/3, 2] kills the conservative Thomson-sphere
reading at the framework's own BLR radius.  Inside the window, the pair
(A, d̄_phys) *inverts* to (τ₀, q) and therefore predicts the remaining
observables — the whole channel becomes a **two-parameter measurer of the a₀
cloud**, not a fit.

## 2. What the window measures (no circularity, per K01)

- −ln A is the opacity of the *radial first flight*: τ₀(1+q/3) (J09-C: definitional
  to the sampler — **label-only as evidence, kept as machinery**).
- d̄_phys/E[D] = R/c with R the *same cloud* (Theorem 1, genuine).
- The **cancellation of τ₀** (window is opacity-free) is real content (K01 GO:
  "opacity-elimination is genuine").
- The novelty: the *framework-radius substitution* R → √(GM_b/a₀).  It converts
  two observables of the transfer function into a direct test of the core
  one-boundary statement — the a₀-radius law — on BLR scales, *without* any
  density model and *without* any dark-matter parameter.

## 3. Worked numbers (model → physical at the frozen lane scale)

Frozen lane illustrative values: R = 941 AU, T_e = 10⁴ K, τ₀ ~ 1, q = 0:
- E[D] = ½ (uniform central) → d̄_phys = E[D]·R/c = 0.5 · 941 AU / c
  = 0.5 · 1.4078e14 m / 2.9979e8 = **2.348e5 s ≈ 2.72 days** (this is the
  E[D]=½, τ₀=1, q=0 number; the frozen lane's ~12-14 day figure corresponds
  to a different (τ₀, scale) stack — candidates are a larger R or a heavier
  κ; not re-derived here, recorded as-is with the discrepancy noted).
- A = e⁻¹ = 0.3679 → J10-I = 2.0022·(r_B/d̄_phys·c)·... — check dimensionally:

```
  J10-I = −ln A · r_B / (c·d̄_phys) = −ln A · r_B / (R·E[D])
        = [τ₀(1+q/3)] · r_B / (R·τ₀(½+q/4)) = (r_B/R) · window(E[D])
```

  **So J10-I = (r_B/R) × J09-D-window.**  Measured lag fixes R = c·d̄_phys/E[D]
  (geometry-neutral, E[D] from Theorem 1); the window then tests whether the
  cloud sits at the framework's density-local radius r_B = √(GM_b/a₀(ρ_B)).
  DoorB pins this for A2744-QSO1: r_B = 40.9 ld predicted vs ≈45 ld measured
  (CONSISTENT-OPEN, ×1.10).

- Concretely (illustrative): A2744-QSO1-class, doorB: r_B = 40.9 ld predicted
  vs ≈45 ld measured (CONSISTENT-OPEN, ×1.10).  If the scattered-line lag
  returns R = 40.9 ld via E[D] (τ₀,q inverted), J10-I = 2.0·(1.0) = 2.0 at q=0
  — exactly at the window's edge, the *maximum-consistency* point.  A lag
  implying R > (3/2)·r_B (i.e. > 61.4 ld here) pushes J10-I below 4/3 at
  q=0 — the conservative reading at the a₀ radius is dead there.

## 4. Kill conditions (pre-registered)

1. J10-I < 4/3 or > 2 at the a₀ radius ⇒ framework's BLR-radius assignment
   fails for that system (scoped to κ = τ₀(1+qr²); general-p window via J09p).
   Sharp form: J10-I = (r_B/R)·window(q), so R > (3/2)·r_B already kills at
   q=0; any R > 2·r_B kills for every q (J10_verify C5).
2. Any ≥ 3σ violation of the J05 bound E[D²] ≥ 3E[Dv²]²/E[v⁴] ⇒ the
   Gaussian-spine transfer reading is dead regardless of the framework.
3. J09p p-sweep breaks the generalized window (p+2)/(p+1) ⇒ J09-D mechanics
   are sampler artifacts, not geometry.

## 5. Status ledger

- J10-I: **derived + verified 6/6** (J10_verify.py, exit 0): 2.717-day baseline
  at R = 941 AU, frozen-lane 12-14 d ⇒ τ₀_eff ∈ [4.42, 5.15] (heavier κ, q=0),
  identity exact (2.000000), A2744-QSO1 reading 1.818 ∈ [4/3, 2] (stays open),
  kill floor at R = 2 r_B (1.000 < 4/3 for all q), window endpoints 2.0/4/3
  monotone.  Corrected mid-flight: sharp kill is R > (3/2)·r_B at q=0, not
  R > 2·r_B (the check caught my own pre-registration arithmetic — recorded).
- J09-D window: VERIFIED 27/27 (J09_two_component_law.py, exit 0) — on record.
- J09p generalized window (p = 1, 2, 4): RUNNING (400k × 7 clouds).
- K04 (inversion (A,d̄) → (τ₀,q) → third observable E[v²]): wave-2 lane running.
- K02 (third independent engine): wave-2 lane running.
- K03 (T-gradient provisos): wave-2 lane running.

## 6. Novelty claim (per user rule: novel + framework-core only)

J10-I is **not** in STANDING.md, not in the frozen lane, not in posterior
literature (scattering RM of BLRs does not currently use the two-observable
atom+lag inversion).  It inherits K01-GO content (Theorem 1, the window) and
adds ONE new substitution — R = √(GM_b/a₀) — which is exactly the framework's
core.  Nothing rederived from literature; kill conditions pre-registered above.