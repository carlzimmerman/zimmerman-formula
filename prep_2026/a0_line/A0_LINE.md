# THE a₀-LINE

**The exact excess identity of the dS-Unruh modified-inertia law, fired on real SPARC.**
2026-07-16 · Derive → Fire → Verify (adversarial, independent machinery) — all lanes complete, **VERIFY verdict: UPHELD** (`VERIFY.md`). This document is the door summary with verifier corrections applied. It is **the sharpest available measurement + model comparison on the framework's own terms** — not a proof of anything, and not a TOE claim. Both footings carried everywhere: **canonical a₀ = cH_Λ/Z = 9.355×10⁻¹¹ m s⁻²** (Planck-anchored ±1%, `concordance_ledger/anchor_planck_a0.py`) and **ALT ρ_total/cH₀ = 1.1305×10⁻¹⁰** (21% apart).

---

## THE EQUATION SET

**The framework law** (modified inertia, horizon scale; Z = √(32π/3) = 5.78881):

$$g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0\,g_{\rm bar}},\qquad a_0=\frac{cH_\Lambda}{Z}=\frac{c^2\sqrt{\Lambda/3}}{Z}$$

**(I) The identity** — squaring it (sympy, `identity_uniqueness.py`):

$$\boxed{\;g_{\rm obs}^2-g_{\rm bar}^2\;=\;a_0\,g_{\rm bar}\;}\qquad\text{EXACTLY, at every acceleration.}$$

The MOND excess E ≡ g_obs² − g_bar² is a **straight line through the origin with slope a₀**, valid at all y = g_bar/a₀ — no deep-MOND selection, no interpolation fit. **Uniqueness (verifier-hardened one step further):** demanding an *affine* excess y²(ν²−1) = αy + β forces β = 0 (else g_obs has a nonzero floor as g_bar→0) and leaves the pure-rescaling family ν = √(1+α/y); the deep-MOND normalization g_obs→√(a₀g_bar) fixes α = 1. **ν = √(1+1/y) is the unique interpolation with an exactly linear excess, up to the definition of a₀ itself.** Honestly stated: this is definitionally tight — "linear excess" *is* the law restated. Its value is that it converts "fit an interpolation" into "measure one slope," enabling E1–E3.

**(E1) The slope estimator** (iterated GLS through the origin, model-based errors — the observed-error version is a trap, see Artifacts):

$$\hat a_0=\frac{\sum_i w_iE_ig_i}{\sum_i w_ig_i^2}\;\xrightarrow{\text{gas-dominated SPARC, 310 pts / 49 gals}}\;\hat a_0^{\rm gas}=(0.97\text{–}1.18)\times10^{-10}\pm16\%$$

(GLS 1.181×10⁻¹⁰ / median-estimator 0.973×10⁻¹⁰; independent verifier estimators 0.92–0.97×10⁻¹⁰. Systematics-owned: stat 0.47 | distance 0.76 | inc 0.26 | Υ 0.96 | gas-cal 0.86 | estimator-choice 1.04, ×10⁻¹¹.)

**(E2) The Λ inversion** (sympy-inverted; canonical-footing statement):

$$\boxed{\;\Lambda=\frac{3Z^2\hat a_0^2}{c^4}\;}\;=\;1.74\times10^{-52}\ {\rm m^{-2}\ (GLS)}\;/\;1.18\times10^{-52}\ {\rm (median)}\quad\text{vs Planck }1.089\times10^{-52}$$

— ratio 1.59 / 1.08, i.e. **+1.45σ / +0.24σ** at σ_lnΛ = 2σ_ln a₀ = 0.32. Rotation curves of gas-rich dwarfs land on the cosmological constant to a factor 1.1–1.6 across ~52 a-priori orders of magnitude. **The banked a₀ ~ cH_Λ/Z coincidence reframed as an inversion — same information content, sharper falsification target** (a future gas slope at 3×10⁻¹⁰ breaks it outright).

**(E3) The Occam factor** — M0 {a₀ ≡ cH_Λ/Z, ZERO free parameters, ±1% anchor folded} vs M1 {a₀ free, log-flat prior of width W}:

$$B_{01}=\underbrace{\frac{W}{\sqrt{2\pi}\,s}}_{\text{Occam}}\;\underbrace{e^{-t^2/2}}_{\text{fit penalty}},\qquad t=\frac{\ln a_0^*-\ln\hat a_0}{\sqrt{s^2+s_{\rm anchor}^2}},\quad s=0.161$$

$$\boxed{\;B_{01}=+0.60\ \text{bans (canonical)}\;/\;+1.04\ \text{bans (ALT)}\;}$$

(default 2-decade prior [10⁻¹¹,10⁻⁹]; envelope +0.30…+1.38 canon / +0.57…+1.34 ALT across 1/2/4-decade, linear-flat, and median-estimator variants; **verifier's adversarial floor: a literature-informed [0.6,2.4]×10⁻¹⁰ prior gives +0.08 canon, a hostile half-decade +0.00 — canonical bans can be driven to ~0 by a question-begging prior, never negative**). Jeffreys: "substantial" — **positive but MODEST, explicitly not decisive.** A formalization of predicted-not-fitted, not new data.

---

## THE VERIFIED NUMBERS

Real SPARC only (frozen repo read-only, 175 galaxies; Q≤2, inc≥30°, e_V/V<10%; gas-dominated cut stated at point level: V_gas² > Υ_d V_disk² + 1.4Υ_d V_bul²). Every number below reproduces from raw data via the exit-0 scripts here and was re-derived by the independent verifier (`verify_independent.py`, own parser/cuts/estimators).

| Piece | Result | Where |
|---|---|---|
| FULL-sample slope (2696 pts) | â₀ = 1.279×10⁻¹⁰ ± 32%; Υ swing 0.5→0.8: 1.89→1.10×10⁻¹⁰ (**62%**) — the banked P1 degeneracy reproduced in full | `fire_slope.py`, fig `fire_slope_fig.png` |
| GAS-dominated slope | â₀ = 1.181×10⁻¹⁰ ± 0.19×10⁻¹⁰ GLS / 0.973 median / 0.92–0.97 independent; Υ swing only **19%** → **71% of the a₀–Υ degeneracy killed** (×3.4 linear / ~1.1 log-bits shrinkage of the M/L interval) | `fire_slope.py`, `estimator_theory.py` |
| Footings at the gas σ | GLS: canon **+1.29σ**, ALT **+0.27σ**; median: canon **+0.19σ**, ALT **−0.83σ**. **No usable footing lean in either direction** (verifier correction: the "mild ALT lean" was GLS-estimator-conditional; independent estimators lean canonical) — the 21% fork is NOT decided by SPARC; pure likelihood ratio 0.44 bans, under 1 ban | `fire_occam.py`, `VERIFY.md` §2 |
| Distance systematics | g_bar ∝ D⁰ **exactly** for gas AND stars (sympy — surface density is distance-independent), g_obs ∝ 1/D: the gas cut suppresses Υ ONLY, not distance; gas dwarfs skew Hubble-flow (σ_lnD 25%), sysD = 40% of the gas budget | `estimator_theory.py` §S2 |
| Tail/linearity shape | Framework ε ≡ E/(a₀g_bar) = 1 exactly; McGaugh-ν ~2y e^(−√y) (superexponential death — survives any g† calibration); simple-ν → 2 (persistent, slope 2a₀ — persistence alone does NOT separate it). Separation ×110 at y = 100 matched-scale (**×11–44 at the rival's own scale** — verifier correction; the tail *death* is scale-robust, the ×100 magnitude is convention-cosmetic). SPARC: median y = 0.31, N(y>30/50/100) = 47/16/**1**. Global shape Υ+scale profiled: fw 1860.4 / McG 1858.8 / simple 1867.5 — **fw-vs-McG a WASH (Δχ² −1.7)**, simple +7.1 (same direction as banked 0.108-vs-0.122 dex); fixed-Υ rows flip the fw-McG sign; y>30 bins Δχ² = +0.21; verdict survives Υ_bulge ±30% + floor stress (range −2.3…+2.2, flips sign). **Persistent-vs-dying UNDECIDED at <1σ today** | `fire_linearity.py`, fig `fire_linearity_fig.png` |
| Λ inversion | 1.74×10⁻⁵² (GLS, +1.45σ, Planck just outside the 1σ band [1.22, 2.34]) / 1.18×10⁻⁵² (median, +0.24σ — the better-supported estimators land *closer* to Planck) | `fire_lambda.py`, fig `fire_lambda_fig.png` |
| Occam | +0.60 / +1.04 bans headline; envelope above; two-sided lever: σ×3 smaller at the CURRENT GLS central value → canonical **−2.45 bans (disfavored)**, ALT +1.39 — **a genuine falsification exposure for the canonical footing**, which is what makes the measurement worth sharpening | `fire_occam.py` |

**Artifacts caught by the honesty rails** (diagnosed in-script, not relayed — the rails ran both ways): (1) observed-error weighting → fake ×3-low deficit (4.15×10⁻¹¹; E[w·ε] < 0 sympy-derived, cured by iterated GLS); (2) cross-Υ covariance comparison → fake Δχ² ≈ −147 against the framework (invalid without log-det); (3) the loose "+1.5–2 bans on error reduction" forecast → false for canonical at the current central value, corrected.

---

## WHAT EACH PIECE ADDS BEYOND THE BANKED WALL (the honest ledger)

The banked wall stands untouched: *the SPARC RAR is convention-compatible and non-diagnostic of a₀'s exact value; the full-sample a₀-line inherits that a₀–Υ degeneracy in full* (62% swing; the banked P1 ridge 1.76/1.36/1.10/0.88×10⁻¹⁰ and the line-GLS 1.89/1.53/1.28/1.10×10⁻¹⁰ are the same ridge, +8–17% metric offset). **The full-sample line is a beautiful exact reframing — elegance and an estimator, zero new information.**

1. **Gas-dominated slope — the genuinely new piece within this ledger:** kills 71% of the a₀–Υ degeneracy (~1.1 log-bits), one M/L-suppressed number at 16%. Does NOT decide 9.36 vs 11.3 vs 12.0 — all within ~1.3σ of at least one estimator variant, and the central value is estimator-owned (GLS 1.18 vs median/independent 0.92–0.97; honest all-choices box **(0.84–1.36)×10⁻¹⁰**, nominally covered by the charged 16%). Historical scope: gas-rich galaxies as M/L-insensitive probes are standard since McGaugh 2011; "new" means new relative to this repo's banked walls.
2. **Tail shape — in-principle orthogonal, in-practice ≲1σ today.** The ×100 zone holds one SPARC point; y>30 points are ~96% star/bulge-dominated (exactly where M/L errors are largest, as the wall predicted). A future-data lever, not a present discriminator.
3. **Occam + Λ inversion — formalizations of the banked coincidence, no new data:** +0.6…+1.0 bans (floor ~0.0 under adversarial priors, never negative), Λ to a factor 1.1–1.6.

**Solar-system consistency (banked story, restated not rederived):** the persistent a₀·g_bar excess lives below the gate frequency ω_c where galaxies orbit; planetary Ω ≫ ω_c suppresses it (the a₀/2 gated corner) — the SPARC high-y points and the Cassini bound sit on opposite sides of the ω gate. The banked Q₂ quadrupole tension (AeST = MG realization) is a separate open item, untouched here.

**Not claimed:** no rival kill, no footing resolution, no "SPARC pins 9.36×10⁻¹¹", no Z-derivation from data, not a TOE.

---

## WHAT SHARPENS IT NEXT (ranked)

1. **TRGB-class distances for the gas-rich dwarfs** (the σ×3 lever): the single biggest tractable budget line; also the falsification exposure — if the GLS central value holds at σ/3, the canonical footing goes to −2.45 bans.
2. **BIG-SPARC** (~4000 galaxies, not yet public): ×10 the gas-dominated sample → statistical floor ~2%, forcing the estimator-choice systematic into the open and giving the footing fork its first real shot (banked pipeline ready, `project_bigsparc_environmental_fork`).
3. **High-y points with M/L-independent masses** (MaNGA/MUSE inner points with vertical-dispersion Υ, gas-rich high-g interlopers): the only way the persistent-vs-dying tail test reaches decisive; needs y ≳ 50 coverage.
4. **DESI + a₀(z)**: the Λ-inversion at multiple epochs — the canonical footing predicts the gas slope tracks √ρ_Λ (constant), ALT tracks cH(z)·E(z) (rising); the 21% degenerate today becomes a slope-vs-redshift discriminator.

### Files
`identity_uniqueness.py` · `estimator_theory.py` · `bayes_setup.py` · `fire_common.py` · `fire_slope.py` · `fire_linearity.py` · `fire_lambda.py` · `fire_occam.py` · `verify_independent.py` (all exit 0, real SPARC, no hard-coded checks) · `DERIVATION.md` · `FIRE_RESULTS.md` · `VERIFY.md` · figures `fire_slope_fig.png`, `fire_linearity_fig.png`, `fire_lambda_fig.png` · JSON: `estimator_results.json`, `bayes_results.json`, `fire_*_results.json`.
