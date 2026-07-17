# FIRE RESULTS — The a₀-Line on Real SPARC

**Lane FIRE — 2026-07-16.** Run order: `fire_slope.py` → `fire_linearity.py` → `fire_lambda.py` → `fire_occam.py` (shared machinery in `fire_common.py`; theory chain in `identity_uniqueness.py` / `estimator_theory.py` / `bayes_setup.py`). All exit 0 on real SPARC, read-only from the frozen repo (`real_research/data/sparc_data/*_rotmod.dat` + `sparc_master_clean.csv`, 175 galaxies; cuts Q≤2, inc≥30°, eV/V<10%). Figures: `fire_slope_fig.png`, `fire_linearity_fig.png`, `fire_lambda_fig.png`. This document is **the sharpest available measurement + model comparison on the framework's own terms** — nothing here is a proof, and nothing here is a TOE claim. Both footings everywhere: canonical a₀ = cH_Λ/Z = **9.355×10⁻¹¹** (Planck-anchored ±1%), ALT ρ_total/cH₀ = **1.1305×10⁻¹⁰**.

The identity being fired (exact at every acceleration, unique to the framework ν up to the definition of a₀ itself — sympy, `identity_uniqueness.py`):

> **E ≡ g_obs² − g_bar² = a₀ · g_bar** — the MOND excess is a straight line through the origin with slope a₀, at all y. No deep-MOND selection, no interpolation fit.

---

## E1 — the slope (`fire_slope.py`)

**Full sample (2696 pts, 147 gals) — the inherited degeneracy, shown honestly.** GLS slope per Υ_d:

| Υ_d | 0.50 | 0.60 | 0.70 | 0.80 |
|---|---|---|---|---|
| â₀ (GLS) | 1.891e-10 | 1.526e-10 | 1.279e-10 | 1.101e-10 |
| â₀ (median) | 1.529e-10 | 1.133e-10 | 0.881e-10 | 0.676e-10 |

Swing 0.5→0.8 = **62 % of â₀** — the full-sample slope inherits the banked P1 RAR a₀–Υ degeneracy essentially in full (banked: 1.76/1.36/1.10/0.88e-10; the slope-estimator lever d a₀_pt/d lnΥ = −φa₀(2y+1) is sympy-verified). **Full sample = NON-diagnostic of a₀'s exact value, exactly as banked. The a₀-line is a reframing here, not new information.** Total error σ = 4.1e-11 (32 %), Υ-owned. (Estimator trap kept visible: observed-error weights give 4.2e-11, a ×3 LOW artifact of weight–noise correlation — diagnosed, not relayed.)

**Gas-dominated subsample — the genuinely new piece.** Cut (stated): point-level V_gas² > Υ_d V_disk² + 1.4Υ_d V_bul². **N = 310 points in 49 galaxies** (weighted stellar share ⟨φ⟩ = 0.32, ⟨y⟩ = 0.04):

> **â₀(gas) = 1.181×10⁻¹⁰ ± 0.19×10⁻¹⁰ (16 %, GLS)** — median-estimator variant 0.973×10⁻¹⁰.
> Budget: stat 0.47 | distance 0.76 | inclination 0.26 | Υ 0.96 | gas-cal 0.86 | estimator-choice 1.04 (×10⁻¹¹). **Systematics-owned.**

- **Υ-sensitivity suppressed, quantified:** gas swing 0.5→0.8 = 19 % vs 62 % full → **the gas cut kills 71 % of the a₀–Υ degeneracy**. a₀ is boxed to (1.13–1.36)e-10 across the *entire* physical M/L range (was (0.88–1.76)e-10) — a ×3.4 shrinkage of the degeneracy interval.
- **Distance systematics carried honestly:** g_bar ~ D⁰ *exactly* for gas **and** stars alike (surface density is distance-independent; sympy) while g_obs ~ 1/D — so the gas cut does **not** reduce distance sensitivity (the "gas g_bar ≈ distance-independent" hint is true but generic); gas dwarfs skew to Hubble-flow distances (σ_lnD = 25 %), tamed only by independence across the 49 galaxies (sysD = 40 % of the gas budget).

**Both footings + the RAR-fit value, at the gas slope's honest σ:**

| | canonical 9.355e-11 | ALT 1.1305e-10 | RAR-fit 1.2e-10 |
|---|---|---|---|
| gas GLS 1.181e-10 | **+1.29 σ** | **+0.27 σ** | −0.10 σ |
| gas median 0.973e-10 | **+0.19 σ** | **−0.83 σ** | −1.20 σ |

**Verdict (both directions):** the GLS point estimate leans ALT/RAR-fit; the median variant leans canonical. All three candidate values sit within ~1.5 σ of at least one estimator variant — **the 21 % footing fork is NOT decided by SPARC** (consistent with the banked non-diagnosticity). What E1 adds beyond the banked wall: a *single-number, M/L-suppressed* a₀ at 16 %, i.e. ~2.6 bits of degeneracy interval removed, not a value discrimination.

## Linearity / high-g tail (`fire_linearity.py`)

The law's separation is real: ε ≡ E/(a₀g_bar) = 1 exactly (framework) vs ~2y e^(−√y) (McGaugh/RAR-fit ν, superexponential death) vs →2 (simple ν, persistent at slope 2a₀); ×100 apart at y≈100, verified symbolically. **But SPARC samples it thinly:** median y = 0.31; N(y>30) = 47, N(y>50) = 16, N(y>100) = 1.

- **Global shape, Υ+scale profiled (plain χ², banked variant):** fw 1860.4 / McG 1858.8 / simple 1867.5 → fw-vs-McG **a WASH** (Δχ² = −1.7); simple mildly disfavored (+7.1). Fixed-Υ rows: fw beats McG by 32–54 at Υ_d = 0.7–0.8, loses by 49 at 0.5 — **the verdict is Υ-dependent, hence not a discriminator.**
- **Robustness (P2b, done properly):** full Gaussian −2lnL with log-det: McG −27.7 better; fixed-Υ=0.70 common-covariance: fw +27.8 better. The two proper variants **bracket zero symmetrically** — the ordering swings ±28 with the statistic and the Υ ridge. (A first-cut variant comparing plain χ² across Υ grids with per-Υ retuned covariances gave "−147 against fw" — an invalid statistic (error inflation is free without log-det), diagnosed and NOT relayed, same rail as the estimator trap.)
- **High-g bins:** above y = 30 (N = 15): Δχ²(McG−fw) = **+0.21 ≈ 0.5 σ-equivalent** — and even that overstates it (Υ/D correlated across those few inner disks). **Persistent-vs-dying is UNDECIDED at <1 σ by SPARC's tail.**
- **Within-galaxy variant (10 largest g_bar-range galaxies reaching y_max>10; M/L = one free number per galaxy, scale fixed at each model's global optimum; 515 pts):** total Δχ²(McG−fw) = **+1.6** (leans persistent), fw wins 5/10 galaxies — **a wash**. Simple-ν worst again (+11.6), consistent with the global ordering and the banked 0.108-vs-0.122 dex.

**Verdict:** the tail-shape test is *partially orthogonal* to the a₀–Υ degeneracy in principle, but at SPARC's sampling it delivers ≲1 σ of persistent-vs-dying discrimination. It becomes decisive only with data at y ≳ 50 with independent M/L (gas-rich high-g interlopers, vertical-dispersion Υ constraints). Neither confirmed nor killed — stated plainly.

## E2 — the Λ inversion (`fire_lambda.py`)

Λ = 3Z²â₀²/c⁴ (sympy-inverted). From the gas-dominated slope:

> **Λ_pred = 1.74×10⁻⁵² m⁻² (GLS) / 1.18×10⁻⁵² (median)** vs **Planck 1.089×10⁻⁵²** — ratio 1.59 / 1.08, i.e. **+1.45 σ / +0.24 σ** at σ_lnΛ = 2σ_ln a₀ = 0.32. GLS 1σ band [1.22, 2.34]×10⁻⁵² — Planck just *outside* the GLS band, well inside the median-variant's.

Rotation curves of gas-rich dwarfs land on the cosmological constant to a factor 1.1–1.6 across ~52 a-priori orders of magnitude. **This is the banked a₀ ~ cH_Λ/Z coincidence reframed as an inversion — same information content, sharper falsification target** (a future gas slope at 3×10⁻¹⁰ breaks it outright). The clean Λ statement is canonical-footing; ALT ties to H₀ (and matches the GLS slope at +0.27 σ).

## E3 — the Occam factor (`fire_occam.py`)

M0 = {a₀ ≡ cH_Λ/Z, **zero** free parameters, Planck anchor ±1 % folded} vs M1 = {a₀ free, log-flat prior}. Quadrature (no closed-form shortcut), likelihood = the gas slope with the full systematics-inflated error (s_ln = 0.161):

> **B₀₁ = +0.60 bans (canonical) / +1.04 bans (ALT)** on the default 2-decade prior; prior/estimator envelope **+0.30…+1.38 (canon)**, **+0.57…+1.34 (ALT)**. Jeffreys: "substantial"/"strong" — **positive but MODEST, not 'decisive'.** Footing fork (pure likelihood ratio): 0.44 bans toward ALT — under 1 ban, **not decided**.

**A formalization, not new data:** it quantifies that a₀ was predicted from (c, H_Λ, Z) before the fit. Error-reduction lever, stated both ways (this **corrects** the loose `bayes_setup.py` line "same agreement worth +1.5–2 bans"): if TRGB-class distances shrink σ ×3 and the central value *stays* at 1.181e-10, canonical goes to **−2.45 bans (disfavored)** while ALT → +1.39; if the central value moves onto the prediction, either footing earns ~+1.5 bans. **The lever is a genuine falsification risk for the canonical footing, and that is what makes it worth building.**

---

## What each piece adds beyond the banked non-diagnosticity (the honest ledger)

1. **The line itself** — a beautiful *exact* reframing; the full-sample slope is exactly as Υ-degenerate as the banked RAR. Adds elegance and an estimator, not information.
2. **Gas-dominated slope (E1)** — the real new piece: kills 71 % of the a₀–Υ degeneracy, one number at 16 % systematics-owned error. Does **not** decide 9.36 vs 11.3 vs 12.0 (all within ~1.3 σ of GLS); it shrinks the box ×3.4.
3. **Tail shape** — in-principle orthogonal, in-practice ≲1 σ at SPARC's sampling (1 point at y>100). A future-data lever, not a present discriminator.
4. **Occam/Λ-inversion (E2/E3)** — formalizations of the banked coincidence: +0.6/+1.0 bans, Λ to a factor 1.1–1.6. Same information, sharper targets.

## Caveats (all load-bearing)

- **Systematics-owned everywhere:** fiducials stated in `fire_common.py` (σ_lnD by flag, σ_i = 3°, σ_lnΥ = 0.1 dex global, gas-cal 10 %, intrinsic floor tuned to χ²/N = 1, estimator-choice spread charged). Different fiducials move â₀ within ~1 σ_tot.
- **GLS-vs-median spread (1.18 vs 0.97e-10) is the single biggest budget line** — the estimator choice is a physics-free degree of freedom and is charged as error, not hidden.
- **Planetary/Cassini consistency (banked story, stated):** the persistent a₀·g_bar excess at high g is galaxy-safe here; on the framework's gated-corner account the excess is suppressed at planetary orbital frequencies Ω ≫ ω_c (the a₀/2 story), *not* at galactic ω — galaxies orbit below ω_c, so the excess **should** persist in galaxy inner regions exactly where this lane measures it. The high-y SPARC points and the Cassini bound live on opposite sides of the ω gate; no contradiction is being papered over, and the Q₂ quadrupole tension (banked, MG-realization-inherited) is untouched by this lane.
- Three artifacts were caught and diagnosed rather than relayed (biased-weights ×3 "deficit"; the cross-Υ covariance ×(−147) "deficit"; the +1.5–2-bans "win" forecast) — the rails ran both ways.
- The word *proof* appears nowhere; exit 0 = computed, not "wins".
