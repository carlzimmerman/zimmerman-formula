# The Big Wheel at z = 3.25: A Clean Galaxy-Scale Rotation Curve Disfavors a Rising MOND Acceleration Scale

**Carl P. Zimmerman** (Briar Creek Tech)
*2026-07-05. One backing script, exit 0, both coefficient footings: `real_research/reviews/bigwheel_a0z_2026/bigwheel_a0z_definitive.py`.*

---

## Abstract

The MOND acceleration scale a₀ has been proposed to track the dark-energy density, a₀ ∝ √ρ_DE (Limbach, Psaltis & Özel 2008; Milgrom 1999), which makes it *evolve* with redshift and turns high-z galaxy kinematics into a cosmological probe. Competing proposals instead tie a₀ to the Hubble rate, a₀ ∝ cH(z) (entropic/emergent-gravity and quantized-inertia constructions), which makes a₀ *rise* at high z. The two readings diverge by a factor ≈ 5 by z ≈ 3. We confront these with the first clean galaxy-scale probe at that epoch: **the Big Wheel** (z = 3.25, Nature Astronomy 2025, arXiv:2409.17956), an exceptionally large, rotation-dominated (V/σ ≈ 4.5) disk whose deep-MOND baryonic Tully–Fisher relation reads the acceleration scale straight off the rotation curve, a₀_eff = V_circ⁴/(G M_bar). With a Monte-Carlo propagation of the velocity and mass errors, a dynamical-mass bound on the (over-estimated) SED stellar mass, and a gas-only hard ceiling, we find **a₀_eff ≈ 1.0–1.6 × 10⁻¹⁰ m s⁻² — its local value.** The rising branch, which requires a₀(3.25) ≈ 4.6–5.9 × 10⁻¹⁰ (a disk spinning at 400–425 km s⁻¹), is **disfavored at ≈ 2σ** — the probability that the measured a₀_eff reaches the rising value is only P ≈ 1–3% (the disk spins at 280 ± 31 km s⁻¹, not the required 400–425); a **constant** a₀ (268–285 km s⁻¹ predicted) is an excellent match; and the **declining** √ρ_DE branch (246–262 km s⁻¹) is consistent, sitting ≈ 1σ low. Both coefficient footings (framework canonical a₀ = 9.36 × 10⁻¹¹; empirical SPARC a₀ = 1.20 × 10⁻¹⁰) give the same verdict. The result is reported straight, with its single-object systematics foregrounded and its tension with the MUSE-DARK III statistical "rising" signal stated. The clean conclusion is a *negative* one that nonetheless matters: **the best high-z disk available disfavors a strongly rising acceleration scale and is consistent with a near-constant one** — favoring the √ρ_DE reading over the cH reading, while not yet detecting the distinctive high-z decline that √ρ_DE + evolving dark energy predicts.

---

## 1. The test

In the deep-MOND regime the baryonic Tully–Fisher relation is exact, V_flat⁴ = G M_bar a₀, so a single well-measured rotation curve reads the acceleration scale directly:

$$a_{0,\text{eff}} = \frac{V_\text{circ}^4}{G\,M_\text{bar}}.$$

At z = 3.25 the candidate laws for a₀ diverge sharply. Writing a₀_loc for the local value:

- **H_RISE** — a₀(z) = a₀_loc · E(z), with E(z) = √(Ω_m(1+z)³ + Ω_Λ). This is the a₀ ∝ cH(z) family (entropic gravity à la Verlinde; McCulloch's quantized inertia, a₀ = cH₀/6; the Ho-Minic-Ng Modified-Dark-Matter scale). E(3.25) = 4.95, so a₀ rises ≈ 5×.
- **H_CONST** — a₀(z) = a₀_loc. Ordinary MOND, and the framework's safe core if the dark energy is a true cosmological constant (w = −1, ρ_DE constant ⟹ a₀ constant).
- **H_DECL** — a₀(z) = a₀_loc · √(ρ_DE(z)/ρ_DE0). The framework's distinctive reading: a₀ ∝ √ρ_DE (LPO 2008) evaluated on DESI DR2 evolving dark energy (CPL w₀ = −0.75, w_a = −0.86), for which ρ_DE(3.25)/ρ_DE0 = 0.51 ⟹ a₀ declines to 0.71× local.

A single rotation curve at z = 3.25 therefore separates a factor ≈ 5 / 0.71 ≈ 7 in a₀ between the rising and declining extremes — a wide, clean lever.

## 2. The datum, and its systematics

The Big Wheel (arXiv:2409.17956) is the cleanest galaxy-scale target available at this epoch: an unusually large disk, rotation-dominated (V/σ ≈ 4.5), with a resolved rotation curve and a CO-traced molecular gas mass.

- **V_rot = 280 (+32/−31) km s⁻¹** (inclination-corrected maximum at R_eff = 9.6 kpc, inclination ≈ 50°). We apply a small asymmetric-drift correction V_circ² = V_rot² + 3.4 σ² (σ_int = 61 km s⁻¹), which the high V/σ keeps modest.
- **M_gas(H₂) = 1.8 (+1.0/−0.8) × 10¹¹ M_⊙** (CO), with a 1.36 helium correction.
- **M_star**: the SED value 3.7 × 10¹¹ M_⊙ is over-estimated — the dynamical mass within R_eff, M_dyn = V²R/G = **1.75 × 10¹¹ M_⊙**, is *smaller than the SED stellar mass alone*, which is unphysical (M_bar ≤ M_dyn). We therefore adopt a parametric M_star = 1.7 × 10¹¹ M_⊙ as the fair central case, and separately quote a hard **gas-only** upper bound on a₀_eff (M_bar = 1.36 M_gas, no stars).

These are the honest single-object systematics; each is bounded rather than assumed away.

## 3. Results (both footings)

Monte-Carlo (4 × 10⁵ draws) over the velocity and mass errors gives the measured scale:

| M_bar assumption | a₀_eff (10⁻¹⁰ m s⁻²) |
|---|---|
| SED (M_star = 3.7 × 10¹¹, over-estimated) | 1.03 (+0.60/−0.38) |
| **Parametric (M_star = 1.7 × 10¹¹, fair central)** | **1.54 (+1.07/−0.60)** |
| Gas-only (hard upper bound) | ≤ 2.55 |

So **a₀_eff ≈ 1.0–1.6 × 10⁻¹⁰ m s⁻² — consistent with the local value on either footing** (framework 0.94; empirical 1.20). The three hypotheses predict, for the fair-central baryonic mass:

| | a₀(3.25) [10⁻¹⁰] | V_pred [km s⁻¹] | vs measured 280 ± 31 |
|---|---|---|---|
| **H_RISE** (framework / empirical) | 4.63 / 5.94 | 400 / 425 | **disfavored ≈ 2σ (P ≈ 1–3%)** |
| **H_CONST** | 0.94 / 1.20 | 268 / 285 | **match** |
| **H_DECL** | 0.67 / 0.86 | 246 / 262 | ≈ 1σ low, consistent (undetected) |

**The rising branch is disfavored at ≈ 1.9σ (framework footing) to ≈ 2.3σ (empirical footing): the probability that the measured a₀_eff reaches the rising value is P ≈ 1–3%.** (A naive median/σ ratio reads higher, ≈ 2.9–4.1σ, but a₀_eff = V⁴/(G M_bar) has a heavy upper tail, so that ratio over-counts; the tail probability, which correctly folds the full M_bar systematic into the prediction as well as the measurement, is the honest number — and it is invariant, giving the same ≈ 2σ whether computed in a₀ or in velocity space.) In velocity space the statement is blunt: a fivefold-risen a₀ would spin this baryon load at 400–425 km s⁻¹, and it spins at 280 — but the ≈ 2× baryonic-mass systematic widens the rising *prediction* to ± ~20% as well, which is why the honest significance is ≈ 2σ, not the naive 4σ. A constant a₀ predicts 268–285 km s⁻¹ and lands on the measurement. The declining √ρ_DE branch predicts 246–262 km s⁻¹ — low by ≈ 6–12%, i.e. within ≈ 1σ of the ±11% velocity error, and thus consistent but undetected.

## 4. What this does and does not show

**Does (clean):** the best clean galaxy-scale disk at z ≈ 3 *disfavors a strongly rising acceleration scale* at ≈ 2σ (P ≈ 1–3%). This is a real, if modest and negative, constraint on the a₀ ∝ cH(z) family — entropic gravity, quantized inertia, and the rising reading of the framework's own coefficient fork. It also favors the framework's √ρ_DE footing (canonical 9.36 × 10⁻¹¹) over the cH footing, an internal discriminant. The constraint is one galaxy at ≈ 2σ, not a decisive exclusion; a sample is needed to reach 3σ+.

**Does not (honest):** it does **not** confirm the framework's *distinctive* prediction. The distinctive, novel content — a₀ declining ∝ √ρ_DE at high z — predicts 246–262 km s⁻¹, only ≈ 1σ below the measurement. One galaxy with an ±11% velocity error cannot yet separate a mild decline from a constant. The datum is therefore equally consistent with **ordinary constant-a₀ MOND**; it does not require the evolution. If anything the central value sits slightly *above* the declining prediction, so the data mildly prefer constant over strong decline — comfortable for the w = −1 core, undemonstrative for the evolving-DE signature.

**In tension with:** the MUSE-DARK III statistical stacking analysis (Ciocan et al. 2026), which reports a₀ *rising* with redshift. The Big Wheel — the most direct, gas-traced, single-object probe — points the opposite way. The two need not be reconciled here; a stacked TFR intercept and a resolved rotation curve carry different systematics (baryon-fraction and M/L degeneracies for the former; inclination and single-object mass for the latter). The honest reading is that the high-z a₀ evolution is observationally *contested and not yet settled*, and the cleanest single disk disfavors the rise.

## 5. Caveats, stated plainly

- **One galaxy.** This is a single rotation curve; the a₀(z) question is decided by a *sample* of clean, gas-traced z ≈ 3 disks, of which the Big Wheel is the first. No statistical claim about the population is made.
- **Baryonic-mass systematics** dominate the error and are bounded, not eliminated: the SED stellar mass is demonstrably over-estimated (M_dyn), the parametric value is a fair central choice, and the gas-only ceiling is a hard bound. The rising branch is disfavored for the SED and parametric (physical) masses; in the ultra-conservative gas-only case (baryons at their hard minimum, a₀_eff at its ceiling ≈ 2.6 × 10⁻¹⁰) the rise is only ≈ 1σ away (P ≈ 15–22%) and is *not* excluded — the ≈ 2σ disfavoring rests on the physical masses. Note the M_bar systematic (≈ 2×) is *itself larger than* the 0.71× decline signal, so this datum cannot probe the declining branch even in principle; it has leverage on the 5× rise only because that gap survives the systematic.
- **Pressure support** is corrected (asymmetric drift, V/σ = 4.5, small); inclination (≈ 50°) enters the velocity.
- **Not a detection of evolution.** The result is a rejection of the rise and a consistency with constant/mild-decline, not a measurement of a₀(z).

## 6. Context and priority

The relation a₀ ∝ √ρ_DE and its redshift test are due to **Limbach, Psaltis & Özel (2008)** (their Eq. 4); the deep-MOND vacuum-scale reading traces to **Milgrom (1999)**. The rising alternative a₀ ∝ cH(z) appears in **Verlinde (2010)** entropic gravity, **McCulloch's** quantized inertia (a₀ = cH₀/6), and the **Ho-Minic-Ng** Modified-Dark-Matter program — all of which the Big Wheel constrains. This note contributes only the *confrontation of a new clean datum* with these standing hypotheses; the framework's non-monotonic a₀(z) reading and its coefficient are set out separately (Zenodo 10.5281/zenodo.21110936; 10.5281/zenodo.20938891). Nothing here derives a₀; it is a data note, reported straight, and its headline is a null that happens to cut cleanly against the rivals.

## Script

`real_research/reviews/bigwheel_a0z_2026/bigwheel_a0z_definitive.py` (exit 0): Monte-Carlo a₀_eff on both mass assumptions and the gas-only bound; the three hypotheses on both coefficient footings, in a₀ and in velocity space; and the significance of the rising-branch rejection. All numbers in this note are its output.

## References

- Limbach, S. A., Psaltis, D. & Özel, F. (2008), arXiv:0809.2790.
- Milgrom, M. (1999), Phys. Lett. A 253, 273.
- Big Wheel discovery paper, arXiv:2409.17956 (Nature Astronomy 2025).
- Ciocan, B. et al. (MUSE-DARK III, 2026).
- Verlinde, E. (2010), arXiv:1001.0785; McCulloch, M. (2007), arXiv:0806.4159; Ho, Minic & Ng, arXiv:1601.00662.
