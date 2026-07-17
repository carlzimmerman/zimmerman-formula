# EST_WALL — the a0-line ML-priors run, WALL-ASSESSMENT lane

**Question fired:** if external per-galaxy colour/SPS M/L priors SUCCEED in cutting the
Upsilon (stellar M/L) systematic to its irreducible **coherent SPS/IMF floor**, does the
gas-dominated SPARC a0-line then DECIDE the dark-energy footing of the coefficient —
canonical **a0 = cH_Λ/Z = 9.355e-11** (pure-Λ) vs alt **a0 = cH₀/Z = 1.1305e-10** — or
does a NEW systematic become the wall?

**Framework note (its own terms):** modified-INERTIA, horizon-derived a0, its OWN dS-Unruh
interpolation g_obs = √(g_bar²+g_bar·a0). Squaring → exact identity
**E ≡ g_obs²−g_bar² = a0·g_bar**, slope a0, unique to ν = √(1+1/y) (= Milgrom 1999 PLA
253:273 Eq 9; the distinctive content is the cH_Λ/Z coefficient + the MI completion).
Estimator = fire_common model-based iterated GLS (`biased=False` — the guard that caught
the fake 3.3e-11 observed-weight deficit). Both footings from `anchor_values.json`.

**2-σ footing target:** Δ = |1.1305e-10 − 9.355e-11| = 1.951e-11 →
σ_tot ≤ |Δ|/2 = **9.75e-12** to place a 2-σ gap between the anchors.

Script: `est_wall.py` (exit 0) · results: `est_wall_results.json` · console: `_wall_console.txt`

---

## HEADLINE — **TIGHTENS-GAS-CAL-NOW-WALL** (both footings)

Beating the per-galaxy Upsilon is **necessary but not sufficient.** External colour/SPS
priors remove the *reducible* Upsilon scatter and drop the Upsilon line from
sysU = 9.57e-12 to its **coherent floor 5.75e-12** (sig_coh = 0.06 dex) + a negligible
0.58e-12 reduced per-galaxy residual. But the **coherent floor then rests on GAS-CAL**:

> **coherent floor (N→∞) = √(sU_coh² + sysG²) = √(5.75² + 8.63²)e-12 = 1.037e-11 > target 9.75e-12.**

Gas-cal (sysG, coherent global gas-mass scale, sig_lnG = 0.10 nat ≈ 10%) does **not**
average down with N, so **no number of gas dwarfs reaches the 2-σ footing line at the
current gas-cal.** Footing separation at the Upsilon-beaten error is **0.52 ban**
(canon +0.55 / alt +1.08) — nowhere near the 2-ban decisive line. **Neither footing is
decided. No detection, no deficit.**

---

## THE BUDGET, Upsilon beaten (sig_coh = 0.06 dex, sig_pg,res = 0.035 dex)

| set | Ud | N gal | a0-hat | tot (pre→post-Υ) | binding line now | coherent floor √(sU_coh²+sysG²) | Occam sep |
|---|---|---|---|---|---|---|---|
| **full** | **0.7** | 49 | 1.181e-10 | 1.90e-11 → **1.74e-11** | sysEst (1.04e-11) | **1.037e-11** > tgt | 0.52 ban |
| trgb | 0.7 | 18 | 1.333e-10 | 1.71e-11 → 1.46e-11 | **sysG (9.46e-12)** | 1.160e-11 > tgt | 1.76 ban |
| full | 0.5 | 62 | 1.363e-10 | 2.17e-11 → 2.01e-11 | sysEst (1.28e-11) | 1.183e-11 > tgt | 1.06 ban |
| trgb | 0.5 | 20 | 1.490e-10 | 1.85e-11 → 1.61e-11 | **sysG (1.09e-11)** | 1.289e-11 > tgt | 2.61 ban* |

\* The Ud=0.5 TRGB "2.61 ban ≥ 2" is a **same-side lean**, NOT a footing selection: both
tensions are negative (canon −2.80 ban / alt −0.19 ban) because the central 1.49e-10 sits
ABOVE both anchors. It **disfavours canonical, does not select alt.** Consistent with the
banked "TRGB leans mildly against canonical"; no clean anchor-vs-anchor separation anywhere.

**Two walls, in order.** On the **full** sets the *immediate* binder is **sysEst**
(= |GLS−median|/2, the ν-shape leak: per-point a0 = E/g_bar **declines with g_bar**, so a
single-slope fit is imperfect). sysEst is reducible by narrowing the y-window — the TRGB
sets, being narrow in y, already collapse it to ~3e-12, and there the binder is directly
**sysG**. So the **terminal, non-averaging wall is gas-cal** on every footing/Ud.

---

## WHAT IT TAKES to reach the 2-σ footing line (Ud=0.7 full, sig_coh=0.06, Upsilon beaten)

Fixed after Upsilon beaten: sU_coh = 5.75e-12; shrinkable(N₀=49) = 1.40e-11; target 9.75e-12.

| sig_lnG | gas scale | sysG | coherent floor | N of clean-distance gas dwarfs |
|---|---|---|---|---|
| **0.10** (current) | 10% | 8.63e-12 | 1.04e-11 | **∞ — floor > target at any N** |
| 0.09 | 9% | 7.76e-12 | 9.66e-12 | ~5300 (floor barely under target) |
| 0.08 | 8% | 6.90e-12 | 8.98e-12 | ~666 |
| 0.06 | 6% | 5.18e-12 | 7.73e-12 | ~273 |
| 0.05 | 5% | 4.31e-12 | 7.19e-12 | ~222 |
| 0.03 | 3% | 2.59e-12 | 6.30e-12 | ~174 |

**Gas-cal is the gate.** At the current sig_lnG = 0.10 the coherent floor exceeds target at
*any* N. Only once an **independent gas-mass calibration** cuts sig_lnG below ~0.09 does a
finite N open, and only a cut to ~0.06–0.08 (5300 → ~300–670 clean-distance gas dwarfs)
makes it practical — i.e. **BIG-SPARC-scale count PLUS a factor-≈1.3–2 better gas-mass
scale.** Necessary condition on the *error*; deciding still requires the central to settle
on one anchor (it currently straddles — see caveat).

---

## IS THERE A DIFFERENTIAL/RATIO ESTIMATOR THAT CANCELS THE COHERENT GAS-CAL? — No (usefully)

A global multiplicative gas-scale (1+ε_G) shifts g_bar → g_bar·(1+(1−φ)ε_G) (gas share
only; g_obs is data, untouched). Measured response **d ln a0 / d ε_G**:

- sample-level (the coherent shift a between-galaxy ratio would remove): **−0.715**
- per-galaxy weighted mean **−0.761**, std across 42 gals **0.126** → a ratio cancels
  **~83%** of the coherent gas-cal, residual dispersion 0.126 (φ/y spread).

**But a between-galaxy ratio cancels the ABSOLUTE a0 normalization too** — it tests whether
a0 is *universal* (same slope galaxy-to-galaxy), not its *value*, so it **cannot compare
9.36e-11 vs 1.13e-10.** The coherent gas-cal is a single global nuisance; **no internal
estimator both cancels it AND preserves the absolute a0** needed for footing discrimination.
Only an **external** gas-mass calibration (interferometric HI + CO, better He/metal
correction) lowers sig_lnG itself.

**φ trade-off (why deeper gas-domination does not cure it):** KU (Upsilon lever, ~Σφ) =
0.352 vs KG (gas-cal lever, ~Σ(1−φ)) = 0.730. Pushing φ→0 shrinks sysU but **grows sysG** —
the gas-dominated cut *trades* the M/L wall for the gas-cal wall. KU+KG is ~fixed by the
(2y+1) weight; the coherent floor is minimized near KU/KG = (sig_G/sig_coh)², **not** at φ→0.

**sig_coh sensitivity:** even the optimistic sig_coh = 0.05 dex gives a coherent floor
9.87e-12 — still above target; 0.07 dex → 1.09e-11. The SPS/IMF floor and gas-cal are
comparable co-bottlenecks; neither alone is beatable to the line.

---

## VERDICT — TIGHTENS-GAS-CAL-NOW-WALL (outcome **B**, both footings)

External per-galaxy Upsilon priors **tighten the a0-line** (sysU 9.57→5.78e-12; total
1.90→1.74e-11, Ud=0.7 full) but **do not decide the footing**: the coherent floor
√(sU_coh²+sysG²) = 1.04e-11 sits just **above** the σ_tot ≤ 9.75e-12 target, now **bound by
GAS-CAL** (a coherent global gas-scale that no galaxy count and no internal ratio removes).
To DECIDE requires **all three**: (a) an independent gas-mass calibration cutting
sig_lnG 0.10→≤~0.08; (b) holding the SPS coherent floor ≤0.06 dex; (c) BIG-SPARC-scale
clean-distance N (~300–670). The honest a0 box still **straddles both footings**
(≈0.9–1.5e-10) and per-point a0 = E/g_bar **declines with g_bar** (ν-shape leak) — **no
footing detection and no deficit are manufactured.** The a0 VALUE and s = −1 sign remain
**postulates**. Exit 0 is not a verdict.

Credits: Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert 2014 ([3.6] SPS M/L
coherent floor); Bell-de Jong 2001 (colour M/L); Lelli-McGaugh-Schombert 2016 (SPARC).
