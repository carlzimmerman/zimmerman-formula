# OUT-3 (SCALE-FREE BOUNDARY) RESULT: κ = ½ ⟺ the formation normalisation equals the vacuum value

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing.
Footings graded separately and **never pooled** (canonical a₀ = 9.3603e-11, alt a₀ = 1.1312e-10 m/s²).
Cold dark energy is a **gravitating field component**, never a particle; the dark mass IS the sector's own
stress-energy — the claim, not a ΛCDM hedge.
Criteria `PREREGISTER.md`, amended by `AMENDMENT_A1.md` (a correction to my own counter-theorem, made
before the Lean run; it changes no threshold, no gate and no number).

---

## LABEL

> **NOT DERIVED (FITTED). The IFF is exact and the condition is a REAL CONSTRAINT (not a flat
> direction) — and it fails on the number, on mass and on epoch. κ = ½ stays FITTED.**

Failing gates: **G3.A, G3.B** (number), **G4.A, G4.B, G4.C** (mass), **G5.A, G5.B, G5.C** (epoch).
G1 (the IFF) and G2 (real constraint) PASS. G6 (mutation, 3 of 4 arms) PASS.

---

## 1. The mechanism

**In words.** The clock sector is one field with one conserved cold charge. In vacuum it *is* the cold dark
energy — uniform, w = −1, energy density ρ_Λc². Around baryons it *is* the dark mass: the same
stress-energy, rearranged and pinned on the fold Σ_f, the first hypersurface going into collapse where the
clock's expansion along its own normal θ_K vanishes. Σ_f is therefore the boundary between the static,
law-carrying interior and the still-expanding exterior. The framework's own symmetry statement is that the
formation *equations* depend only on the ratio a₀/g, so G_λ : (a₀, g) → (λa₀, λg) is an exact symmetry of
them and κ is the only quantity charged under it. The scale-free boundary condition is the one statement
that can break that degeneracy without naming a number: it demands that the sector's normalisation be
**continuous through Σ_f** — the value the collapse pins inside equals the value the vacuum already has
outside. Referred to a common dimensionless unit the demand is an equation, and if it is an equation in κ
it derives κ. Three things can go wrong: the two sides may carry the same G_λ weight (then the equation is
an identity or impossible and κ stays a flat direction); they may carry different weights but return a
number far from ½; or they may return ½ at one mass only, which is not a derivation because a₀ is
universal to 0.041 dex. **All three were graded. The first does not happen; the second and third do.**

**In equations.** With `u_f ≡ a₀/g_b,f = a₀R_f²/(G M_b)`, `X(u) ≡ (√(1+4u) − 1)/2` (FLD1's exact share,
`X(1+X) = u`), `ρ_c(Σ_f) = 3X(u_f)M_b/(4πR_f³)`, `Z ≡ √(8π/3)`, `R_Λ = c/H_Λ`:

| arm | slot | `N_f` (formation, on Σ_f) | `N_v` (vacuum) |
|---|---|---|---|
| **A** | energy density | `G ρ_c(Σ_f) c² / a₀²` | `G ρ_Λ c² / a₀² = 1/κ²` |
| **B** | column | `X(u_f)/(4π u_f)` | `ρ_Λ R_Λ / (a₀/G) = 1/(Z κ)` |
| **C** | share | `X(u_f)` | `Ω_Λ/Ω_b` |

The **IFF** (G1, exact, Lean `iff_half`): in slot A, `N_v = 1/κ²`, so `N_v = 4 ⟺ κ = ½`. The condition
`N_f = N_v` then reads

```
A:  N_f = N_v  ⟺  ρ_c(Σ_f) = ρ_Λ                      (the a₀² cancels — Lean armA_iff)
    exact inversion (X(1+X) = u, no deep-field approximation — Lean armA_invert):
    q ≡ 4π ρ_Λ R_f³/(3 M_b),   a₀ = G M_b q(1+q)/R_f²,   κ_A = G M_b q(1+q)/(c√(Gρ_Λ) R_f²)
    for q ≪ 1 this is simply   a₀ = (4π/3) G ρ_Λ R_f     — the Newtonian pull of the vacuum inside the fold

B:  X(u_f) = 4π ũ/Z,  ũ ≡ c√(Gρ_Λ) R_f²/(G M_b)        κ_B = [(1 + 8π ũ/Z)² − 1]/(4 ũ)
C:  X(u_f) = q_C ≡ Ω_Λ/Ω_b                              κ_C = q_C(1+q_C)/ũ
```

**The G_λ weight ledger** (corrected in `AMENDMENT_A1.md`; `s ≡ d ln X/d ln u`,
`ρ ≡ d ln R_f/d ln a₀`):

```
w_F1 = -2 + s(1+2ρ) - 3ρ    w_V1 = -2        flat iff s(1+2ρ) = 3ρ   (deep field: ρ = +1/4)
w_F2 = -1 + s(1+2ρ)         w_V2 = -1        flat iff ρ = -1/2
w_F3 =      s(1+2ρ)         w_V3 =  0        flat iff ρ = -1/2
```

The measured fold response is `ρ = 2.9e-3 dex/dex` (FINAL-18) — the fold is essentially blind to a₀ — so
at `ρ ≈ 0` the gap is `s = 0.503 … 0.517` in **all three** slots. **The condition is a real constraint,
not a flat direction (G2 PASS), and it is that way for a structural reason that survives every slot.**

---

## 2. Derivation of κ, and 3. the number with an error bar

Each arm inverts exactly (Lean `armA_invert`/`armB_invert`/`armC_invert`; every root re-verified by
independent bisection to 6 digits). Planck h = 0.674, Ω_Λ = 0.685, Ω_b = 0.0493; canonical footing.

| arm | `κ` at log M_b 10.45, z = 0 | `log₁₀(κ/½)` | best over the mass grid | at log M_b | G3 (5 % = 0.0212 dex) |
|---|---|---|---|---|---|
| **A** energy density | **3.872e−05** | **−4.111** | 8.694e−05 (−3.760) | 11.5 | **FAIL** |
| **B** column | **1.736e+04** | **+4.540** | 7.797e+03 (+4.193) | 11.5 | **FAIL** |
| **C** share | **2.248e−01** | **−0.347** | 5.006e−01 (**+0.0005**) | 11.5 | PASS |

**Error bar on the primary arm (A), log M_b 10.45, z = 0:**

```
κ_A = 3.87e-05,   log₁₀ κ_A = −4.412 ± 0.100 dex   →  κ_A ∈ [3.08e-05, 4.87e-05]
```
dominated by the fold radius: FLD1's at-rest-vs-Hubble-flow variant (+22.3 % in R_f) moves κ_A by
+0.099 dex; start-redshift 20/30 (+1.4 %) by +0.007; shell number N 1200→4800 by +0.0003; Planck ρ_Λ
(+1.5 %) by +0.003. Added in quadrature.

**Why it fails, in one line.** At the measured a₀ the two sides are not close:

```
N_f(F1) = G ρ_c(Σ_f) c²/a₀² = 2433.8      N_v(V1) = 1/κ² = 4.0018
N_f/N_v = ρ_c(Σ_f)/ρ_Λ = 608.2   (2.784 dex)      [alt footing: 670.0, 2.826 dex]
```
The halo at the fold is ~190× the background *matter* density (a turnaround overdensity, as it should be),
so its cold density is ~608× the dark-energy density. Continuity through the fold would require a₀ smaller
by 1.3e4, i.e. κ ≈ 4e−5 — a Universe with no observable dark mass (X = q ≈ 0.034 instead of 21).

**Arm C's near-hit is recorded, not celebrated.** κ_C = 0.50059 at log M_b = 11.5 — inside the 5 % band,
and it clears G3 as written. It is the *last row of FLD1's table*, and it moves as M_b^{1/3}:
`κ_C = 0.0154` at log M_b 7 and `0.5006` at 11.5, a **1.512 dex drift** against the 0.041 dex the RAR
allows. It is also only as precise as Ω_b: Ω_b = 0.0486 → κ_C = 0.5146, Ω_b = 0.0500 → 0.4871, i.e.
±2.8 % per ∓1.4 % in Ω_b. **This is the β = 1 circularity in a new slot: the share-matching condition
reproduces κ = ½ exactly at one mass and nowhere else.**

*Variant check on arm C's right-hand side, so the near-hit is not over-read.* The vacuum value of the share
is `ρ_Λ/ρ_b = Ω_Λ/Ω_b = 13.89` because the background sector **is** the cold dark energy. If instead one
reads it as FINAL-15's cosmic dust share (5.41) or as `Ω_c/Ω_b = 5.35`, the same condition gives
κ_C = 0.0377 / 0.0370 at log M_b 10.45 and 0.0839 / 0.0823 at 11.5 — never within an order of magnitude
of ½. The near-hit exists only for the Ω_Λ/Ω_b reading, and only at the grid top.

**G4 (mass) and G5 (epoch), threshold 0.041 dex:**

| | drift over log M_b 7 → 11.5 | drift over z = 0 → 4 |
|---|---|---|
| A | **1.494** dex FAIL | **0.922** dex FAIL |
| B | **1.512** dex FAIL | **1.808** dex FAIL |
| C | **1.512** dex FAIL | **1.815** dex FAIL |

**G6 mutation, 3 of 4 bite (PASS):** ρ_Λ→ρ_crit ×1.227; mass ×10 ×2.154 (predicted 10^{1/3} = 2.154);
z = 4 ×0.120 (predicted (R_f(0)/R_f(4))⁴). The R_f → 0.52 R_ta arm does not bite (×1.003) — it is a
consistency check, since FLD1's own ratio is 0.52. The Lean MUTATE twin fails with 3 errors
(`compile_MUTATE.txt`).

---

## 4. Predictions not yet measured

Listed most-live first. None of these changes the label; they are what the lane leaves on the table.

1. **P1 — the fold's a₀-response, `ρ = d ln R_f/d ln a₀`. This is the one number the structural verdict
   hangs on.** Measured at **one** mass (log M_b 10.45) and **one** epoch (z = 0): 2.9e-3 dex/dex
   (FINAL-18). **Not measured: its mass and redshift dependence.** The lane's G2 flips from PASS to FAIL
   if ρ reaches −1/2 (arms B and C become flat directions, exactly, at every u) or +1/4 (arm A, deep
   field). A three-point grid (log M_b 9, 10.45, 11.5) at z = 0 and 1 would settle it. This is a
   self-contained FLD1 rerun, no new physics.
2. **P2 — the cold density on the fold, ρ_c(Σ_f).** FINAL-18 measured the charge `M_C` at the fold and
   FLD1 the radius `R_fold`; **no lane has printed the density.** This lane's value: 3.55e-24 kg/m³ at
   log M_b 10.45 (Δ_m ≈ 190 against the background matter density), i.e. 608 × ρ_Λ. Arm A predicts
   ρ_Λ = 5.845e-27. Excluded by the existing numbers, but the number itself is new.
3. **P3 — the continuity radius r\*, where the halo's *mean* cold density actually equals ρ_Λ.** The
   boundary condition is a statement about a density, so it does pick a radius; it is not the fold:

   | log M_b | 7 | 9 | 10.45 | 11.5 |
   |---|---|---|---|---|
   | r\* (Mpc) | 0.476 | 1.505 | **3.466** | 6.342 |
   | r\*/R_fold | 47.6 | 32.7 | **24.9** | 20.3 |

   `r\* ∝ M_b^{1/4}` (1.125 dex over the grid). **Unmeasured:** no lensing or kinematic profile is traced
   to 3.5 Mpc for an L\* galaxy — KiDS/ONE1's outer windows (FLD1) reach ~0.85 Mpc, about a quarter of the
   way. A stacked weak-lensing density profile to several Mpc, tested for `ρ_c ∝ r^{-2}` and for the
   `M_b^{1/4}` scaling, is the cleanest surviving test of the *continuity* idea, independent of κ.
4. **P4 — the L\* prediction `a₀ = (4π/3) G ρ_Λ R_fold`** (arm A's root for q ≪ 1). At log M_b 10.45 this
   gives a₀ = 7.25e-15 m/s² against the measured 9.36e-11 — a factor 1.29e4. Stated here as a
   prediction because it has a definite mass signature (`a₀ ∝ M_b^{1/3}`, i.e. 1.5 dex over the galaxy
   range) that no RAR fit has been tested for; the RAR's universality already excludes it.
5. **P5 — the column ratio in the (a₀/G) convention:** `N_v(V2) = 1/(Zκ) = 0.691` (canonical) / `0.573`
   (alt). FINAL-19 reported the analogous ratio in the a₀/(2πG) convention (6.0 ± 1.4). **This is a
   restatement of a measured lane in another convention, not a new prediction** — recorded so the two
   conventions are not later confused.
6. **P6 — arm C's landing mass.** κ_C = ½ at log M_b = 11.5, exactly FLD1's grid top. Extending the fold
   table above 10^11.5 M_☉ must show κ_C rising as M_b^{1/3} (it cannot stay at ½). One extra FLD1 row
   settles whether this is a coincidence of the grid edge.

---

## 5. Lean certification

`OUT3.lean` — **23 theorems/definitions, 0 `sorry`, 0 non-standard axioms** (only `propext`,
`Classical.choice`, `Quot.sound`; `#print axioms` for the eight load-bearing theorems is at the end of
`compile.txt`). Compiles under `lake env lean` in `fable_independent_2026/lean_2026` (a standalone `lean`
cannot see Mathlib), **exit 0**.

Load-bearing: `share_quad` / `share_of_quad` (the exact share, both directions), `Xo_strictMono`,
`Nv_eq_inv_kappa_sq`, **`iff_half` (the IFF of the take)**, `armA_iff` (a₀² cancels), `armA_invert`
(exact, no deep-field approximation), `rhoC_strictMono`, `armA_at_most_one` (root unique),
`armB_invert`, `armC_invert`, `weight_gap_A/B/C`, `flat_BC_rho`, `flat_BC_only`, `flat_A_deep_iff`,
`dlnX_dlnu_pos`, `gap_at_measured_fold`.

`OUT3_MUTATE.lean` (twin) — **exit 1, 3 errors**: (M1) `armA_invert` with the `(1+q)` dropped,
(M2) `flat_BC_rho` at ρ = +1/2 instead of −1/2, (M3) the headline asserted with no weight gap.

---

## What this lane adds to the record

- It closes the **energy-density** slot at the fold, which FINAL-18 (share) and FINAL-19 (column) did not
  run: `κ_A = 3.87e-05 ± 0.100 dex`, 4.11 dex from ½, drifting 1.49 dex in mass and 0.92 dex in epoch.
- It **generalises FINAL-18's "real constraint, not a flat direction"** from the share slot to all three
  slots and states the reason: the condition is κ-charged because the *geometry does not respond* to a₀
  (ρ ≈ 0), not because the equations are asymmetric. Flatness would need ρ = −1/2 or +1/4.
- It gives the structural form of the OUT-3 negative: **the condition is genuinely constraining (G2 PASS)
  and genuinely wrong (G3/G4/G5 FAIL)** — which is a stronger and more useful result than a flat
  direction would have been.
- It leaves one live, cheap, unmeasured number (P1, the fold's a₀-response across mass and epoch) and one
  live, unmeasured profile test (P3, r\* ≈ 3.5 Mpc, ∝ M_b^{1/4}).

**κ = ½ FITTED; not theory closed.**

---

## Artifacts

`PREREGISTER.md` (criteria, frozen first), `AMENDMENT_A1.md`, `out3.py` → `out3.out` / `out3.json` /
`out3_menu.out` (130 rows, every admissible arm × mass × epoch, nothing selected post hoc),
`out3MUTATE.out` / `out3MUTATE.json`, `OUT3.lean` / `OUT3_MUTATE.lean` → `compile.txt` /
`compile_MUTATE.txt`. Siblings consulted, not redone: FINAL-6, FINAL-16, FINAL-18, FINAL-19, FINAL-15,
FLD1, FRAMEWORK.md, CFG894. This lane edits nothing outside its own folder.
