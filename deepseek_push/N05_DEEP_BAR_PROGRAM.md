# N05 — THE DEEP-BAR KILL TEST: PROGRAM CARD AND CATALOG-PRECISION CASE

**2026-09-23 · moment channel · deep-SPARC tension (L06: 4.2σ, a0_eff = 0.73 a0) → can a dedicated deep-BAR program reach a decisive 5-SE verdict, and at what cost?**
**Verdict: NOT CLOSED — and the deep regime is now a two-sided contradiction (SPARC deep −4.17σ clustered; MIGHTEE deep **+6.58σ**, the mirror image). The program survives at FULL status (not downgraded to 'residual confirmation'): its real job is **arbitration** between two sign-opposite >4σ deep readings.**
**All real-data numbers reuse in-repo files only. No git commit. `N05_deep_bar.py` + `N05_deep_bar.out` + `N05_results.json`.**

---

## 0. TL;DR (the budget in five lines)

- The measured −0.276 × a0E[g_bar] SPARC-deep M1 deficit becomes a **5-SE kill at ~1656 deep rings** at current per-ring noise — i.e. **~59 NEW deep-HI galaxies** (task convention: ~3 deep rings each ≈ 180 new rings), total deep ensemble **~1329 rings / 194 galaxies** under the honest galaxy-clustered SE. The binding unit is **galaxies**, not rings (clustered SE is 2.45× the ring-level SE → deepening existing SPARC galaxies does nothing).
- **MIGHTEE does NOT close the tension — checked first.** Its 72/80 deep rings give M1 = **+1.164 × a0E[g_bar], z = +6.58** (positive): the a0-line's moment identity is ALREADY violated at >5 SE (two-sided) in the deep regime — in the **opposite** direction (a0_eff ≈ 2.0 a0; G199 1.87× normalization rung). MIGHTEE contradicts the SPARC reading; it cannot confirm it.
- **Discriminator:** a 5-SE M1 kill excludes the normalization-only family {a0_eff = 1} but **cannot attribute** the deviation between H_A (a0_eff = 0.73 a0) and H_B (deep slope 0.55, intercept 0): the two lines cross at g_bar = 0.043 a0 *inside* the deep band, both produce the same ≈ −0.3 × a0E moment (H_B: −0.320), and the exact likelihood-ratio separation at the kill N is only **1.9σ**. 5σ attribution needs **~11 700 deep rings** at SPARC-class scatter — **or** the resolved-SED systematic recipe (0.045 dex: **~540 rings**) and/or a deeper band (g_bar → 10⁻³ a0: **~900 rings**).
- **Program card:** MIGHTEE-class MeerKAT L-band HI + resolved 10-band SED (the MIGHTEE-HI recipe, σ_int = 0.045 dex), ~13× the published 19-galaxy yield, ~5–15 kh exposure class over ~2–3 yr (labeled estimate; ngVLA/SKA1-mid alternative). HI depth for 2σ Vgas at g_bar = 0.05 a0 = 27/38/54 km/s at 5/10/20 kpc — already exceeded by MIGHTEE's 0.01 a0 depth; depth is NOT the binding constraint, population + systematics control are.
- **Pre-registered criteria:** kill (negative side), kill (positive side), confirm, arbiter stop-rule, discriminator sub-criterion — §4.

---

## 1. What was reproduced, and how (structure fidelity, measurement reuse)

L06's deep-SPARC lane is **reproduced from its saved measurements** (`L06_results.json`), not by rerunning the 2000-boot legs:

| quantity (L06 saved) | value |
|---|---|
| deep-SPARC rings (g_bar < 0.2 a0) | N = 1152, from 135/175 galaxies, 8.5 deep rings/gal |
| M1 deficit Δ/(a0E[g_bar]) | **−0.276** (Δ = −2.679e−22, a0E = 9.712e−22 m²/s⁴) |
| SE ring-level / clustered (used) | 2.623e−23 / 6.425e−23 → z_clustered = **−4.17**, z_ring = −10.2 |
| deep residual scatter s_dex | 0.232 dex (the discriminator's per-ring noise scale) |
| a0_eff mapping | 1 − 0.276 = **0.724 a0 ≈ 0.73 a0** (G208 register 0.69–0.74 a0 ✓) |

The corpus v7 file is re-read only to recover the deep **log-g_bar distribution** (deterministic; count and E[g_bar] both match L06 exactly, checks in .out) — needed for the slope-channel leverage (s_u = 0.247, u ∈ [−2.15, −0.70]) and the clustered-SE galaxy scaling. The only new bootstrapped real-data legs: MIGHTEE deep sub-sample (72 rings), ring + colour-group, 2×2000 resamples — cheap.

---

## 2. The N-requirement curve: −0.276 × a0E[g_bar] → 5-SE kill

SE(Δ)/a0E[g_bar] today: **0.0662** (clustered) at N = 1152; per-ring clustered-equivalent noise: 2.245 × a0E. Target SE: 0.276/5 → 0.0552.

| f (deficit fraction of a0E) | N_req ring-level | N_gal_total_req (135 have deep rings today) | new galaxies |
|---|---:|---:|---:|
| 1.00 (full-size) | 126 | 15 | 0 (already killed) |
| 0.50 | 504 | 59 | 0 (already killed) |
| **0.276 (measured)** | **1656** | **194** | **59** |
| 0.15 | 5601 | 656 | 521 |

- **(a) Rings at current per-ring noise:** 1656 deep rings — *provided the new rings are independent units*, i.e. new galaxies. Adding rings to existing SPARC galaxies does not reduce the clustered SE (2.45× ring-level; the galaxy is the independent unit for shared distance/inclination/m2l systematics).
- **(b) New deep-HI galaxies, SPARC-style (~3 deep rings each):** **59 NEW galaxies ≈ 180 new rings**, total deep ensemble **~1329 rings / 194 galaxies** → z = 5.00 (exact at target). At SPARC's own deep yield (8.5 rings/gal) the same budget is ~500 new rings — consistent with the ring-level figure. Galaxy count, not ring count, is binding.
- **(c) MIGHTEE-HI — does it ALREADY close it? CHECKED FIRST: NO.** The 72/80 deep rings (colour groups 18) give Δ = +1.164 × a0E, z = **+6.58** (SE = max(ring 8.12e−23, colour-group 7.34e−23)). The mirror-image tension: a0_eff ≈ 2.0 a0 (linearized 2.16; G199 quadratic register 1.9e−10 = 2.03 a0). A ring-weighted pool of the two catalogs lands at −0.235 × a0E — a tug-of-war, **not a verdict**. Consequences: (i) the single-committed-a0 moment identity is already breached at >5 SE (two-sided) by MIGHTEE in the positive direction; (ii) no catalog-extension of either sample can "close" the other — the program's deliverable is the arbitration §4.
- Caveat recorded: MIGHTEE per-ring errors are digitization-limited (G099 lane: 0.036 dex rms validated); the colour-group bootstrap is the per-galaxy systematic proxy. Budget quoted at SPARC-class systematics throughout.

---

## 3. The discriminator: H_A (a0_eff = 0.73 a0) vs H_B (deep slope 0.55, intercept 0)

Parametrization (deep power-law baseline slope ½): u = log10(g_bar/a0), ydev = log10(g_obs/sqrt(a0·g_bar));

- **H_A:** ydev = **−0.0682** dex (a0_eff = 0.73 a0 asymptote) — reproduces the measured −0.276 moment by construction.
- **H_B:** ydev = **+0.050·u** (slope 0.55, intercept 0 relative to the a0-asymptote).

Results (exact LR statistic validated by 8000-sim Monte Carlo, seed 20260923+400/401; scatter = deep s_dex = 0.232 dex):

- The two lines **cross at g_bar = 0.0433 a0, inside the band**: |Δydev| over the deep sample averages 0.0195 dex (±0.04 max). The offset channel cancels; separation lives in the slope channel.
- **M1 cannot attribute:** H_B produces Δ_M1 = **−0.320 × a0E** vs the measured −0.276 — both ~−0.3. A 5-SE M1 kill fires identically under either hypothesis.
- Separation significance (exact LR, offset noise included): **S_LR(N) = ½·√(d′(X′X)d/σ²)**: N = 1656 → **1.9σ**; N = 3000 → 2.5σ; N = 11 699 → 5.0σ (MC: P(|z|≥5) = 0.50; P(|z|>1.96) = 0.999). Slope-channel-only (optimistic): N(S=5) = 8827.
- **Which hypothesis space does the deep cut actually exclude at the kill N?** The normalization-only family {a0_eff = 1} — yes, 5σ (that is the M1 kill). The {H_A, H_B} pair — no, ~1.9σ: a 5-SE M1 kill is a **family kill**, not an attribution. The deep cut's M1 *cannot* tell "0.73 a0" from "slope 0.55".
- **Levers** (what the program can actually spend on): (i) *systematics control* — the discriminator cost scales as σ²: σ = 0.10 dex → 2167 rings; σ = 0.05 dex (the MIGHTEE resolved-SED recipe) → **542 rings**; (ii) *depth* — extending to g_bar = 10⁻³ a0 (u_min = −3) raises s_u 0.25 → 0.78 → slope-channel N(S=5) ≈ 900 (approximate: population-shape assumed). Deeper beats merely-more, for attribution.

---

## 4. The program card

### 4.1 Survey design
| item | choice |
|---|---|
| instrument | **MeerKAT L-band (900–1600 MHz; 1.4 GHz HI)** — the MIGHTEE platform (Maddox+2021 A&A 646 A36; Jarvis+2016) — survey extension of the 4 existing deep fields + targeted low-mass dwarfs; ngVLA/SKA1-mid alternative (2030s, deeper + wider bands) |
| bands | HI 21 cm (rotation + resolved HI surface densities) **+ resolved 10-band SED** for spatially varying mass-to-light (the MIGHTEE-HI recipe; σ_int = 0.045 ± 0.022 dex — the single most important systematic control) |
| depth needed | 2σ Vgas at g_bar = 0.05 a0 = 4.68e−12 m/s²: **V = 27 / 38 / 54 km/s at R = 5 / 10 / 20 kpc** (per-radius-bin precision 13–27 km/s); MIGHTEE deep rings already reach ~10⁻¹² = 0.01 a0 → depth is **not** binding |
| target population | inclined (i ≳ 40°), gas-dominated dwarfs (M★ ≲ 10⁹–10¹⁰), HI-extendable into g_bar < 0.2 a0 with resolved stellar masses — the yield path the 19-galaxy MIGHTEE sample proved |
| ring budget (SPARC-class σ) | **~180 new deep rings (59 new galaxies)** for the M1 kill; **~11.7 k deep rings** for 5σ H_A/H_B attribution at current σ — or **~0.5–2 k** with the resolved-SED recipe |
| runtime (ESTIMATE — assumptions labeled) | MIGHTEE published yield 19 galaxies → 80 rings (72 deep) from the 4 MeerKAT L-band fields; ~13× the galaxy count ⇒ **~5–15 kh MeerKAT-class exposure + SED program over ~2–3 yr cycles** (baseline B: deeper-band ngVLA/SKA1-mid). Not a budget; a scaling from the published yield. |

### 4.2 Pre-registered kill / confirm / arbiter / discriminator criteria
Statistics: L06 conventions — M1 = E[g_obs²] − E[g_bar²] − a0 E[g_bar]; SE = max(ring-boot, galaxy/colour-group-boot), 2000 resamples; deep cut g_bar < 0.2 a0; pooled ensemble = SPARC deep + new deep-HI + MIGHTEE deep, each catalogue's rings grouped by galaxy (colour-group where galaxy ids absent).

1. **KILL (negative side):** pooled M1 ≤ −5 SE **and** sign-consistent sub-readings at |z| ≥ 2 in ≥ 2 independent catalogues ⇒ a0_eff < 1 in the deep regime: the single-committed-a0 identity fails; the 4.2σ tension is decided (deficit direction).
2. **KILL (positive side):** pooled M1 ≥ +5 SE (two-sided) with sign consistency ⇒ the MIGHTEE normalization reading (a0_eff ≈ 2 a0) wins: also a failure of the single-constant identity, direction recorded (the G199 rung confirmed).
3. **CONFIRM (framework survives):** |z_M1| ≤ 2 at the required precision (SE(Δ)/a0E ≤ 0.0552) **and** the SPARC-deep −0.276 traced to a per-galaxy systematic (inclination / m2l / SED convention) that, when corrected, zeroes the deficit. **Arbiter stop-rule:** if SPARC-type and MIGHTEE-type populations still disagree in M1 sign at ≥4σ each after ~50% of the ring budget, the kill test is suspended and the deliverable becomes the systematic-difference investigation (the same resolved-SED / inclination / distance machinery applied to both samples) — the two-sided contention is itself the primary finding.
4. **DISCRIMINATOR sub-criterion:** H_A vs H_B attribution declared only at LR significance ≥ 5 (N ≈ 11.7 k at SPARC-class σ; ≈ 0.5–2 k with the resolved-SED recipe); otherwise reported as **indeterminate**, with the achieved S attached. The M1 kill alone never triggers an attribution claim.

---

## 5. Honest record

- The MIGHTEE deep reading (+6.58σ) is the paper-lane digitization (no per-ring error bars published; G099-validated 0.036 dex); its per-galaxy systematics are proxied by the 18 colour groups. Both SE conventions give z > 5.
- The slope-0.55 hypothesis is a hypothetical parse of the deep tension ("intercept 0" = same normalization as the a0-deep asymptote, crossing inside the band); the MIGHTEE paper itself reports a low-g slope ≈ 0.5.
- The depth-lever numbers (band to u_min = −3) assume the SPARC-like log-normal population shape extends; labeled approximate.
- a0_eff mappings (0.73/2.16 a0) are linearized moment readings; the G199 quadratic-fit registers (0.69e−10 / 1.9e−10) agree and are quoted alongside.
- The pooled −0.235 figure is informational (ring-weighted moment of two sign-disagreeing catalogues), not a verdict; the sign disagreement is the honest state of the deep regime.
- Runtime is a scaling estimate from the published MIGHTEE yield, not a TAC budget.
- Files: `N05_deep_bar.py` (all numbers; MC 8000 sims/cell, seeded), `N05_deep_bar.out` (full log), `N05_results.json` (machine-parsed). No git commit.