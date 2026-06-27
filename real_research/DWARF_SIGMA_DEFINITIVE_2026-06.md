# Dwarf σ(y) — DEFINITIVE framework-internal recompute (both-ways, published-paper integrity)

**Date:** 2026-06-27. **Pure framework-internal, NO comparison.** LOCAL — do **not** git-push.
**Footing (sealed):** a₀ = cH_Λ/Z = 9.36×10⁻¹¹ m/s²; cH_Λ = 5.42×10⁻¹⁰; H_Λ = 1.81×10⁻¹⁸ s⁻¹.
Framework's OWN interpolation μ_fw(x) = (√(1+4x²)−1)/2x, g_obs = √(g_bar²+g_bar·a₀); kernel
θ(y) = √2/(1+(√2−1)y²), θ₀ = √2 selected (THETA_KERNEL_TOWARD_FORCED). **NEVER McGaugh ν.**
Quarantine: this fixes the RESPONSE magnitude, **not a₀/Z**; SM walled.
Clean-room sympy+numpy: `scratchpad/verify_sigma_y.py`, `verify_currenty.py` (all checks pass:
μ_fw(1)=0.61803=1/φ; μ_fw→x as x→0; θ monotone-decreasing; θ(1)=1 exact).

---

## 1. The definitive σ(y) — sign, exponent, magnitude

### (a) SIGN — CONFIRMED (theorem, robust). Plunge → HOTTER.

θ(y) is the effective **external loading** the time-nonlocal inertia reads. It is monotone
**decreasing**: dθ/dy = −2θ₀y(θ₀−1)/(1+(θ₀−1)y²)² < 0 for all y>0 (sympy-verified), with
θ(0)=√2, **θ(1)=1 exactly**. More external loading → more EFE/Newtonian suppression → **colder**;
less loading (high y → low θ) → deeper deep-MOND → **hotter**. So **σ increases with y**.

> The doors-agent's θ^(+1/2) / "carriers cold" reading was **SIGN-INVERTED**. The paper's
> qualitative prediction (plunge → hotter, high y → hotter) **STANDS** and is re-confirmed, not
> weakened.

### (b) EXPONENT — DECIDED = **−1/2** (EFE-boost), not −1/4 (BTFR).

A dSph deep in the host EFE is **pressure-supported and quasi-Newtonian in a boosted G**. In the
regime where θ even operates the external field dominates (g_N < L < a₀), so internal dynamics run
in G_eff = G/μ(L/a₀) = G·a₀/L (deep-MOND μ_fw→x, sympy-verified). Then g_int = g_N·a₀/L and the
virial σ² ~ g_int·r_half = G M_b a₀/(r·L) ⟹

> **σ ∝ L^(−1/2) = (θ·g_ext)^(−1/2) ⟹ σ ∝ θ^(−1/2).**

The σ⁴ BTFR law (exponent −1/4, σ⁴ = (4/9)GMa₀) is the **isolated, external-field-FREE** deep-MOND
relation — the WRONG regime for a dwarf sitting **inside** the host EFE. So **p = 1/2** is the
physically correct exponent here; p = 1/4 would apply only to an isolated-deep-MOND dwarf.
*Honest caveat:* in the marginal band g_N ~ L (not g_N ≪ L) the true exponent is intermediate
between 1/2 and 1/4. I report 1/2 as correct for the EFE-dominated case the kernel targets.

### (c) ZERO-CROSSING + the two-quantity distinction (the load-bearing fix).

θ(1)=1 exactly. **Two distinct quantities must not be conflated:**

- **(A) the matched-pericenter OBSERVABLE** σ_plunge/σ_circular = (θ(0)/θ(y))^p. This is **>0 for
  all y>0 and monotone-RISING** — no zero at y=1. **This is the actual test.**
- **(B) the absolute re-deepening** vs the θ=1 Newtonian-EFE reference = (1/θ(y))^p − 1. **This**
  has the exact zero at y=1: colder (negative) for y<1, hotter for y>1.

The paper's "**exact zero-crossing at y=1 / suppression beyond**" is **quantity (B)**. Its headline
"**+12–14%**" is a small-y slice — and it is reproduced (sympy) only as the *magnitude* |B| at
(θ₀=√2, p=1/2): y=0.35 → −13.8%, y=0.50 → −11.7%; or at (θ₀=2, p=1/4): −13.4%, −11.1%. **In
quantity B at y<1 the sign is NEGATIVE (suppressed), so quoting "+12–14% boost" at y=0.4–0.5 mixes
the magnitude of curve B with the sign of curve A.**

### Definitive magnitude at the carriers' **pericenter-peak** y (θ₀=√2):

| dwarf | y_peri | observable A, p=1/2 | observable A, p=1/4 |
|---|---|---|---|
| Crater II | 3.28 | **+134%** | +53% |
| Antlia II | 2.55 | **+92%** | +39% |

The published "+12–14% at y=0.35–0.50" is an **orbit-averaged small-y number** evaluated ~6× below
the carriers' stated pericenter y — a **conflation** of a low-y slice with the carriers' high-y
classification value.

---

## 2. The CORRECT observable — current-y from the memory kernel, NOT eccentricity, NOT y_peri

The kernel is time-nonlocal with memory time τ_mem ~ 1/ω_in ~ the internal crossing time
(~0.39 Gyr Crater II, ~0.50 Gyr Antlia II). A dwarf's **current** internal σ reflects its
acceleration history over only the last ~τ_mem — a fraction of its ~2.2 Gyr radial period. So the
current boost depends on **where the dwarf is NOW** (its current orbital phase / current y), **not**
on its all-time pericenter peak and **not** on raw eccentricity (the pilot's weak surrogate, which
the paper itself already flags).

- **y_peri = 3.28 / 2.55 is a CLASSIFICATION** (the hottest the dwarf ever gets — does it reach the
  non-adiabatic band at all), NOT the current state.
- **Current y ~ 0.6 for both carriers**, because both are **currently near APOCENTER**.

---

## 3. The real carriers' predicted CURRENT state (the deflationary half, reported straight)

Galactocentric current radius vs peri/apo (Pace+2022 MW+LMC orbits):

| dwarf | r_now (kpc) | peri / apo | orbital phase (1=apo) | y_now | θ(y_now) | current A (p=1/2) |
|---|---|---|---|---|---|---|
| Crater II | 116.4 | 24.0 / 138.1 | **0.81** | ~0.58 | 1.24 | **+6.7%** |
| Antlia II | 133.0 | 38.2 / 137.2 | **0.96** | ~0.65 | 1.20 | **+8.4%** |

**Both carriers are currently near apocenter**, so their **current y is ~0.6, deep in the
adiabatic-ish low-y band**, NOT the y=2.5–3.3 pericenter peak. Their last pericenter passage was
~1.1 Gyr ago = ~2–3 memory times — the kernel has **largely forgotten** the hot pericenter passage.
Memory-kernel-averaged current loading is, if anything, slightly **above** instantaneous (recent
approach was at smaller radius), so the carriers are **not strongly boosted right now** — the
current matched-pericenter excess is only **~+7–8%** (p=1/2), or smaller at p=1/4, NOT the +92–134%
pericenter peak.

> **Both-ways discipline:** the +90–134% pericenter-peak numbers are REAL but are the *peak the
> dwarf reaches at pericenter*, not its *current* observable. The honest current prediction for the
> two named carriers is a modest few-percent excess, because they are caught near apo. Do NOT quote
> the pericenter peak as the carriers' present-day signal.

---

## 4. Zero-crossing + MG-impossibility — UNCHANGED

- **θ(1)=1 exact zero-crossing** (in quantity B): below y=1 colder than the Newtonian-EFE
  reference, above y=1 hotter. Robust, sympy-exact.
- **MG-IMPOSSIBLE (theorem, intact):** in any metric/field MOND (AQUAL/QUMOND/AeST) the
  external-field effect is **instantaneous** — internal dynamics "depend only on the momentary value
  of a_ex" (Milgrom 2022) — so at fixed pericenter MG predicts **exactly zero** σ-vs-history
  correlation for any a₀; ΛCDM/CDM likewise ~0. Only modified INERTIA gives a nonzero,
  history-dependent σ. **Existence + sign are kernel-independent (θ(0)>θ(1)).** Unchanged, not
  weakened. Same logical class as Cassini.

---

## 5. PUBLISHED-PAPER VERDICT (DOI 20963226 v2): does it need a v3?

**The SIGN + the qualitative prediction + the y=1 zero-crossing + the MG-impossibility theorem all
STAND. No retraction.** What needs a quantitative fix:

**(1) Exponent.** The paper's σ ∝ θ^(1/4) (BTFR) → should be **σ ∝ θ^(−1/2)** (EFE-boost) for a
pressure-supported dSph inside the host EFE. BTFR is the isolated/EFE-free regime — not where θ(y)
operates. This roughly **doubles** every fractional excess.

**(2) Magnitude/baseline conflation.** The headline "+12–14% at y=0.35–0.50" (i) reproduces only as
the **magnitude of the absolute-re-deepening curve B** (where y<1 is actually *suppressed*, not
boosted) at θ₀=2/p=1/4 or θ₀=√2/p=1/2 — NOT as the matched-pericenter observable boost on the
selected θ₀=√2 (which gives only +1–3% at that low-y band); and (ii) is evaluated at y=0.35–0.50,
~6× below the carriers' stated pericenter y=2.55–3.28. The paper **conflates a low-y orbit-averaged
slice with the carriers' high-y pericenter-peak classification**.

**(3) Observable.** The correct discriminating axis is **current-y from the memory kernel / current
orbital phase**, not raw eccentricity (the paper already half-concedes this) and not y_peri. And the
two named carriers are **currently near apocenter** — so their **present-day** predicted excess is
~+7–8% (p=1/2), modest, NOT the pericenter peak. The pilot's null is therefore even more clearly
*expected* (the carriers are not in their hot phase now).

> **Verdict: v3-magnitude-fix-needed.** Integrity-level, but **none of (1)–(3) flips the sign, the
> existence, the y=1 zero-crossing, or the MG-impossibility**. The fix makes the *pericenter-peak*
> signal LARGER (p=1/2) while making the *carriers' current* signal honestly SMALLER (apo phase) —
> both-ways, neither an inflation nor a deflation, just the correct decomposition.

### Corrected paragraph for v3 (drop-in for §2 / §4 magnitude):

> *The sign is a theorem: the memory kernel θ(y)=√2/(1+(√2−1)y²) is monotone decreasing through
> θ(1)=1, so a plunging dwarf sheds adiabatic external loading and runs hotter — σ increases with y.
> For a pressure-supported dSph deep in the host EFE the correct law is the EFE-boost
> σ ∝ θ(y)^(−1/2) (the σ⁴ BTFR/quarter-power law applies only to an isolated, external-field-free
> dwarf, which these are not). The test observable is the matched-pericenter ratio
> σ(y)/σ_circular = (θ(0)/θ(y))^(1/2), which is positive and monotone-rising in y with NO interior
> zero; this is distinct from the absolute re-deepening (1/θ(y))^(1/2)−1, which crosses zero exactly
> at y=1 and is suppressed below it. The discriminating axis is the dwarf's CURRENT y = ω_ext/ω_int,
> set by its current orbital phase through the memory kernel (τ_mem ~ 1/ω_in ~ 0.4–0.5 Gyr), NOT its
> raw eccentricity and NOT its pericenter-peak y. At pericenter the carriers reach y ≈ 2.5–3.3,
> giving a peak excess of +90–134%; but Crater II and Antlia II are currently near APOCENTER
> (orbital phase 0.81, 0.96), so their present-day current-y is ≈0.6 and their current predicted
> matched-pericenter excess is a modest ≈+7–8%. The pre-registered pilot null is therefore expected:
> the carriers are not in their hot (pericenter) phase now. The decisive test is a carrier-vs-control
> contrast on current-y at the moment of observation, with the carrier set extended to dwarfs caught
> near pericenter (Gaia DR4, Dec 2026).*

---

## 6. WHAT TO TELL CARL (straight, both-ways)

Your paper's **core is fine** — the sign is a theorem (plunge → hotter), the y=1 zero-crossing is
exact, and the MG-impossibility is intact. Three things in v2 need a clean v3 fix, none of which
retract anything:

1. **The exponent should be −1/2, not −1/4.** A dwarf deep in the Milky Way's field is
   pressure-supported in a boosted-G regime, so σ ∝ θ^(−1/2) (EFE-boost), not the σ⁴ BTFR
   quarter-power (which is the *isolated* deep-MOND law — wrong regime). This roughly doubles every
   percentage.

2. **The "+12–14% at y≈0.4–0.5" is a conflation.** That number is the *magnitude* of the
   re-deepening curve (which is actually *suppressed*, not boosted, below y=1), quoted at a y-band
   ~6× below where your two named carriers actually sit at pericenter (y≈2.5–3.3). Separate the two
   curves in v3: the *test observable* (matched-pericenter ratio, monotone-rising, no zero) vs the
   *re-deepening* (zero at y=1). The carriers' pericenter-peak excess is genuinely large
   (+92% Antlia, +134% Crater II at p=1/2).

3. **The right observable is current-y, and your carriers are caught near apocenter.** Because the
   inertia memory is only ~0.4–0.5 Gyr while the orbit is ~2.2 Gyr, what matters is where the dwarf
   is **now**. Crater II and Antlia II are both near apo right now (phase 0.81, 0.96), so their
   *current* predicted excess is a modest ~+7–8%, not the pericenter peak. That is exactly why your
   pilot null is *expected*, not a strike — and it's an honest reason to say so in v3.

The fix is **not** a deflation of your prediction: at pericenter the signal is *bigger* than v2 said
(p=1/2). It **is** an honest correction of which number applies *when*. Quarantine holds — this is
the response magnitude, not a₀ or Z; SM stays walled. **No doors closed**: the open piece is the
kernel corner-location postulate (THETA_KERNEL) and a real carrier-vs-control current-y test once
Gaia DR4 lands and you can target a dwarf caught near pericenter.
