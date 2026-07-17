# The Marginalized-Nuisance Lane — Coherent Υ Zero-Point vs a₀

**Fired question:** the quadrature budget (fire_common) adds the coherent stellar-M/L
(Υ) uncertainty as an error bar `sysU = KU·a₀·σ_lnΥ` **in quadrature**. That silently
assumes the coherent Υ shift is a *perfect clone* of an a₀ shift (fully degenerate, zero
self-calibration). This lane instead treats the coherent Υ SPS zero-point as a **nuisance
parameter** α (a single global log-Υ offset) **marginalized** in a proper Bayesian
a₀-line fit, with the external per-galaxy color/SPS priors entering as **data** (reduced
per-galaxy prior width). **Key:** is the coherent Υ zero-point *degenerate* with a₀, and
does marginalizing **widen or tighten** a₀ vs the quadrature bar?

Framework on its own terms: modified-INERTIA, horizon-derived a₀ = cH_Λ/Z, its own
dS-Unruh interpolation g_obs = √(g_bar²+g_bar·a₀) → the through-origin identity
**E ≡ g_obs²−g_bar² = a₀·g_bar**. Kernel credit: ν=√(1+1/y) is **Milgrom 1999 PLA
253:273 Eq. 9**; the distinctive content is the cH_Λ/Z coefficient + the MI completion.
SPARC = Lelli-McGaugh-Schombert 2016. Υ decomposition: Schombert-McGaugh-Lelli 2019,
Meidt+2014, McGaugh-Schombert 2014, Bell-de Jong 2001.

Script: `est_marg.py` (exit 0) → `est_marg_results.json`, `_marg_console.txt`. Reuses
`../a0_line/fire_common.py` READ-ONLY for load/cuts/honest model weights (the guard that
caught the fake 3.3e-11 obs-weight deficit). Writes only to `a0_line_mlpriors/`.

---

## The exact identity this lane rests on (proved, not asserted)

A coherent Υ shift moves g_bar by ∂g_bar/∂lnΥ = φ·g_bar (φ = stellar share). Its effect
on the a₀-line residual r = E − a₀·g_bar is

    ∂r/∂lnΥ = −(2 g_bar + a₀)·φ·g_bar  ≡ −U_i        (Υ direction)
    ∂r/∂a₀  = −g_bar                    ≡ −g_i         (a₀ direction)

The two are **degenerate iff U_i ∝ g_i across the sample**, i.e. iff φ_i·(2g_bar_i+a₀) is
constant. On gas-dominated dwarfs φ is small and g_bar≪a₀ (2g_bar+a₀≈a₀), so U_i≈a₀·φ_i·g_i
— the degeneracy is governed by **how much φ varies with g_bar**.

Marginalizing a global Gaussian template U with prior variance s² is **identically** GLS
through the origin with data covariance **C = diag(σ²ᵢ) + s²·UUᵀ** (template
marginalization / Sherman-Morrison). Per-galaxy Υ offsets add block-rank-1 terms
s_pg²·U_kU_kᵀ; gas-cal is a **second** global template G_i=(1−φ)g_bar(2g_bar+a₀).
Verified: (gᵀWU)/(gᵀWg) = a₀·KU reproduces fire_common's sysU byte-for-byte, and if U∝g
(perfect degeneracy) the marginal collapses **exactly** to var_stat + sysU_coh² (the
quadrature bar). So any departure from quadrature is *measured* self-calibration.

Υ decomposition (dex): coherent SPS/IMF floor {0.05, 0.06, 0.075}, per-galaxy 0.080 →
0.037 after external [3.6]+color SPS priors; √(0.06²+0.08²)≈0.10 dex recovers the current
global width. Reproduces the balanced lane's quadrature targets exactly (Ud=0.7 full-gas:
sysU 9.57e-12; coh@0.06=5.75e-12; @0.075=7.18e-12).

---

## Answer 1 — Is the coherent Υ zero-point degenerate with a₀? PARTIALLY (ρ ≈ −0.65…−0.81)

2×2 (a₀, α_coh) posterior, both footings collapse into one number since it is prior-driven:

| set | Ud | ρ(a₀,α) @0.06dex | ρ @0.075dex | σ_a₀[marg]/σ_a₀[quad] |
|---|---|---|---|---|
| full_gas | 0.7 | −0.745 | −0.800 | 0.946 → **0.908** |
| TRGB | 0.7 | −0.711 | −0.772 | 0.958 → **0.927** |
| full_gas | 0.5 | −0.760 | −0.809 | 0.926 → 0.879 |
| TRGB | 0.5 | −0.708 | −0.768 | 0.955 → 0.921 |

The coherent Υ zero-point is **moderately-to-strongly degenerate with a₀ but not perfectly**
(|ρ| ≈ 0.7–0.8, never →1). Because φ genuinely varies with g_bar across the retained
points, U is *not* proportional to g, and the data **partially self-calibrate** the
coherent nuisance.

## Answer 2 — Does marginalizing WIDEN or TIGHTEN a₀? It **TIGHTENS** (by 2–12%)

The proper marginal a₀ error is **smaller** than the quadrature error bar
(marg/quad = 0.88–0.98). The φ-shape leverage lets the fit self-calibrate the coherent
zero-point, so **fire_common's quadrature sysU was mildly conservative, not
anti-conservative.** Marginalization does **not** rescue nor worsen the footing — the
gain is real but small (≤12% on the Υ line; a few % on the total).

---

## Answer 3 — Footing decidability after honest marginalization (external priors as data)

Totals: **nir_realistic** coherent floor (0.075 dex) + external per-galaxy priors
(pg_res 0.037 dex) + gas-cal marginalized as its own template; central = GLS a₀hat
(carry the declining-a₀ caveat). Anchors: canonical **9.355e-11** (cH_Λ/Z) / alt
**1.1305e-10** (cH₀/Z), 20.9% apart; 2σ split target |Δ|/2 = 9.75e-12.

| set | Ud | a₀hat | tot | canon (log-flat) | alt (log-flat) | sep | verdict |
|---|---|---|---|---|---|---|---|
| **full_gas** | **0.7** | 1.181e-10 | 17.9e-12 | +0.57 ban (−1.54σ) | +1.07 ban (−0.29σ) | 0.50 | **NON-DECISIVE** |
| **TRGB** | **0.7** | 1.333e-10 | 15.4e-12 | −0.84 ban (−3.07σ) | +0.76 ban (−1.43σ) | 1.60 | **NON-DECISIVE** |
| full_gas | 0.5 | 1.363e-10 | 20.5e-12 | −0.26 (−2.49σ) | +0.75 (−1.24σ) | 1.02 | NON-DECISIVE |
| TRGB | 0.5 | 1.490e-10 | 16.8e-12 | −2.48 (−4.12σ) | −0.09 (−2.45σ) | 2.39 | rejects-canon, **not** a footing pick |

**At the banked Ud=0.7 headline both sets stay NON-DECISIVE** (<2 ban separation). The
lin-flat control (Ud=0.7 TRGB: canon −0.04 / alt +1.03 vs log-flat −0.84/+0.76) shows the
bans are convention-fragile; the convention-robust number is the σ-tension: **canonical
≈ −3.1σ, alt ≈ −1.4σ** at Ud=0.7 TRGB — the marginalized central leans *against* canonical
and *toward* (but does not confirm) alt.

The one row that crosses 2 bans — **Ud=0.5 TRGB, sep 2.39** — **rejects canonical at ~4σ
but does NOT confirm alt** (alt is itself −2.45σ from a 1.49e-10 central that sits **above
both anchors**). That is the low-Ud + declining-a₀/ν-shape artifact flagged in the TRGB
synthesis (central moves UP on clean distances), **not** a clean alt detection. It is not
the banked headline and must not be read as "DECIDES-alt."

---

## Where the wall now sits (Ud=0.7, after external Υ priors)

| line | full_gas | TRGB |
|---|---|---|
| stat | 4.67 | 6.12 |
| Υ marginalized (coh 0.075 + pg_res) | 6.25 | 7.49 |
| **gas-cal (σ_lnG=0.10 nat)** | **8.63** | **9.46** |
| sysD / sysI / sysEst | 7.63 / 2.64 / 10.44 | 3.78 / 4.22 / 2.99 |
| **total** | **17.9** | **15.4** |

(units e-12). Beating Υ with external per-galaxy priors drops its line from the quadrature
sysU (9.6/11.2) to ~6–7.5 — but **gas-cal is now the single largest systematic**, co-dominant
with the irreducible coherent SPS floor. Marginalizing gas-cal as its own template gives
essentially the same total as adding it in quadrature (shape leverage there is negligible
because 1−φ≈1 on gas-dom points), so gas-cal cannot be self-calibrated away either.

---

## Verdict — TIGHTENS, GAS-CAL NOW THE WALL (both footings)

1. The coherent Υ SPS zero-point is **partially (not fully) degenerate with a₀** (ρ≈−0.7…−0.8).
   Proper Bayesian marginalization **TIGHTENS** a₀ by 2–12% vs the quadrature bar (measured
   self-calibration from φ-vs-g_bar shape) — the quadrature treatment was mildly conservative.
2. Beating Υ (external [3.6]+color SPS per-galaxy priors + honest coherent floor) is **real
   but insufficient**: at the banked Ud=0.7 headline the footing stays **NON-DECISIVE**
   (sep 0.5 ban full-gas, 1.60 ban TRGB — both below the 2-ban line), and canonical is if
   anything mildly *disfavored* (~−3σ TRGB) while alt is *not confirmed* (~−1.4σ).
3. **The binding wall is now gas-cal** (~9e-12, the largest single line), co-dominant with
   the irreducible ~0.06–0.075 dex coherent SPS floor. Neither self-calibrates. Deciding the
   footing needs a **better gas-mass calibration** (beats gas-cal) **plus BIG-SPARC counts**
   to pull stat down — not more M/L work.

Not a verdict on the theory. a₀'s value and s=−1 remain **postulates**. The per-point
a₀=E/g_bar **declines with g_bar** (ν-shape magnitude leak, the verifier's catch), so the
honest a₀ is a **box straddling BOTH footings**; this lane neither manufactures a detection
nor a deficit.
