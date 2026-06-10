# Agent N5 — The discriminator: frequency-keyed vs acceleration-keyed inertia on SPARC (Door IVb follow-on)

*2026-06-10. Files: `agentN5_freq_vs_accel.py` (run) → `agentN5_freq_vs_accel.out`. Real 175-galaxy SPARC data,
locked conventions (= `mi_f4_sparc_shape_test.py`): unweighted dex scatter primary, weighted shown; per-function
best-Υ on [0.3,1.2]×46; baseline at both a₀ footings. No git.*

## The question
Door IVb killed instantaneous **acceleration-keyed** (magnitude-keyed) modified inertia in the solar system:
survival line s < (0.34–0.40)·a₀ ⇔ solar-reflex anomaly δa☉ ≤ 2.47–3.38×10⁻¹⁵ m/s² (agentE fit-A / kitchen-sink),
both candidate normalizations dead (framework a₀ by ×8.5 in residual). Any tail/memory kernel is naturally
**frequency-keyed** (K~(Ω)), and frequency-keying is the named evasion: the Sun's reflex wobble runs at
Ω_J ≈ 1.68×10⁻⁸ s⁻¹, galactic orbits at ~10⁻¹⁶–10⁻¹⁵ s⁻¹ — eight decades. **But the RAR is tight in acceleration.**
Make-or-break: does a frequency-keyed law fit SPARC as well as the acceleration-keyed one?

Pre-registered thresholds (= the repo's F4 shape-test): SPARC-ALIVE if the best variant is within **+0.010 dex
unweighted** of the best acceleration-keyed law; DEGRADED +0.010–0.020; DEAD >+0.020. Solar PASS if
δa☉(Ω_J) ≤ 2.47×10⁻¹⁵ m/s² (strict; ≥8.5× below the framework std-μ reflex 2.10×10⁻¹⁴). Predicted pure-freq
failure mode, stated before computing: a = Ω·V, so one Ω₀ maps to a per-galaxy acceleration scale a₀_eq ≈ Ω₀·V —
per-galaxy residuals should run with V_flat (deep-MOND slope −2/3 per dex of V_flat, self-consistent mode).

## (1) Baseline reproduced (gate)
Acceleration-keyed ν(g_bar/a₀), framework footing 9.36e-11: McGaugh **0.1950** (Υ=0.52), F4-standard **0.1984**
(Υ=0.64), fw 0.1969, simple 0.1951; canonical 1.2e-10: best 0.1968 (fw). Identical to `mi_f4_sparc_shape_test.out`
(gate PASS). Reference bar for everything below: **best accel-keyed = 0.1950 dex unweighted** (0.1105 weighted).

## (2) Pure frequency-keying μ(Ω/Ω₀)·a = g_bar — **SPARC-DEAD, both shapes, robustly**
Self-consistent forward solve (Ω = √(a/R) on the predicted circular orbit; vectorized log-bisection verified
against tight-tolerance brentq to ~2×10⁻¹⁵ relative with exact law closure in all regimes). Observed-Ω
(Ω = V_obs/R) constraint form also run — analytically it inflates deep-regime residuals ×3/2, and indeed comes
out worse; the self-consistent numbers are the favorable ones and are quoted as primary.

| variant | best Υ_d | best Ω₀ (s⁻¹) | unweighted | Δ vs accel best | verdict |
|---|---|---|---|---|---|
| μ_standard, self-consistent | 0.52 | 1.36×10⁻¹⁵ | **0.2213** | **+0.0263** | DEAD (1.3× past the 0.020 line) |
| μ_simple, self-consistent | 0.42 | 1.20×10⁻¹⁵ | **0.2176** | **+0.0226** | DEAD |
| μ_standard, observed-Ω | 0.66 | 9.50×10⁻¹⁶ | 0.2966 | +0.1016 | worse (as predicted) |
| μ_simple, observed-Ω | 0.52 | 8.36×10⁻¹⁶ | 0.2806 | +0.0856 | worse |

Robustness of the death (the working rule — a "fails" verified as rigorously as a "works"): holds vs the
same-shape free-a₀ acceleration-keyed optimum (std: 0.1976 ⇒ +0.0237; simple: 0.1951 ⇒ +0.0225); holds on the
weighted metric (0.1343–0.1458 vs 0.1105, i.e. +0.024–0.035); holds in both solve modes; Υ freedom granted equally (interior optimum);
Ω₀ grid-interior (refined to ~0.01 dex); footing-independent (Ω₀ is fitted, the comparison bar taken at the
better footing). The fitted Ω₀ ≈ 1.3×10⁻¹⁵ s⁻¹ means a₀_eq = Ω₀·V_flat runs from 2.7×10⁻¹¹ (20 km/s dwarfs) to
4.1×10⁻¹⁰ m/s² (300 km/s giants) — a ×15 spread in the effective acceleration scale where the data demand one
scale. That is the kill in one number.

**The per-galaxy structure confirms the predicted mechanism** (differential test — the absolute V_flat trend in
the control is shared SPARC systematics): per-galaxy mean residual vs log₁₀V_flat (V_flat = outer-3-point mean):

| law | slope (all) | slope (deep g<10⁻¹⁰) | V≥150 minus V<80 (deep) |
|---|---|---|---|
| accel McGaugh (control) | +0.331/dex | +0.358/dex | +0.159±0.034 (4.7σ) |
| accel F4-std (control) | +0.320/dex | +0.374/dex | +0.167±0.034 (4.9σ) |
| freq μ_standard | −0.119/dex | −0.170/dex | −0.188±0.036 (**5.2σ, sign-flipped**) |
| freq μ_simple | −0.093/dex | −0.119/dex | −0.154±0.035 (4.4σ, sign-flipped) |

Frequency-keying shifts the per-galaxy trend by **−0.45 to −0.53/dex** (predicted deep shift −2/3, attenuated by
non-deep points and the compromise Ω₀) and **flips the sign** of a ~4.5σ trend — high-V galaxies are over-boosted,
low-V under-boosted, exactly the a = Ω·V signature. This is a structured, mechanism-matched failure, not generic
extra scatter. (Independent corroboration, not computed here: pure frequency-keying turns the deep-MOND BTFR into
M ∝ V³; SPARC measures slope ≈3.85–4.) 

## (3) The hybrid the tail mechanism would actually give: a₀_eff = a₀_ref·[(1+Ω/H₀)/(1+Ω_ref/H₀)]^(−p)
(Ω_ref = 3×10⁻¹⁶ s⁻¹ is pure convention — a₀_ref is refit at every p; H₀ = 70 km/s/Mpc enters only through Ω/H₀.
SPARC points span Ω/H₀ ≈ 30–37,000, median 259 — the knee region sits at the task's ~100–1000.) Self-consistent
solve; full (a₀_ref, Υ) refit per p.

Unweighted scatter vs p (Δ vs accel best 0.1950):

| p | std shape | simple shape | McGaugh-RAR shape |
|---|---|---|---|
| 0 (= accel-keyed, free a₀) | 0.1976 (+0.0026) | 0.1951 (+0.0000) | 0.1949 (−0.0002) |
| 0.1 | 0.1964 (+0.0014) | 0.1935 (−0.0016) | 0.1933 (−0.0018) |
| 0.2 | 0.1959 (+0.0008) | 0.1924 (−0.0026) | 0.1923 (−0.0028) |
| 0.3 | 0.1958 (+0.0008) | 0.1918 (−0.0032) | **0.1918 (−0.0033)** |
| 0.5 | 0.1970 (+0.0020) | 0.1919 (−0.0031) | 0.1920 (−0.0030) |
| 0.75 | 0.2000 (+0.0050) | 0.1937 (−0.0013) | 0.1941 (−0.0009) |
| 1.0 | 0.2039 (+0.0089) | 0.1967 (+0.0016) | 0.1975 (+0.0024) |

The implied a₀ drift across galaxies does **not** destroy RAR tightness for p ≤ 1: the worst case (std, p=1) costs
+0.0089 dex — still inside the pre-registered ALIVE band. Both ways, full weight: **mild dressing (p ≈ 0.2–0.5)
actually *improves* the unweighted fit by ~0.003 dex** (it partially cancels the control's +V_flat per-galaxy
trend: std-shape slope falls from +0.32 at p=0 to +0.17 at p=1). This is at the level of known V-correlated
systematics (distance, inclination, M/L) — **recorded as "costs nothing", NOT claimed as a detection of frequency
dressing.** Observed-Ω cross-check is uniformly worse (e.g. std p=0.5: 0.2138 vs 0.1970) — mode-consistent with (2).

## (4) Solar-reflex consistency at Ω_J and the verdict matrix
δa☉ = |a☉|·(1/μ−1) at the variant's own SPARC-best parameters; |a☉| = 2.09×10⁻⁷ m/s², Ω_J/H₀ = 7.4×10⁹;
budget: PASS ≤ 2.47×10⁻¹⁵ (strict), 3.38×10⁻¹⁵ loose; framework std accel reflex = 2.10×10⁻¹⁴ (the ×8.5 kill).

| variant | δa☉ (m/s²) | suppression | solar | SPARC | BOTH? |
|---|---|---|---|---|---|
| accel F4-std (context = Door IVb) | 2.10×10⁻¹⁴ | 1× | FAIL | alive (+0.0034) | no |
| accel simple (context) | 9.36×10⁻¹¹ | 2×10⁻⁴ | FAIL | alive (+0.0001) | no |
| **accel McGaugh-RAR (context)** | 6.3×10⁻²⁸ | 3×10¹³ | **PASS** | **alive (+0.0000)** | **YES — undressed** |
| pure freq μ_std (Ω₀=1.36e-15) | 6.9×10⁻²² | 3.1×10⁷ | PASS | **DEAD (+0.0263)** | no |
| pure freq μ_simple (Ω₀=1.20e-15) | 1.5×10⁻¹⁴ | 1.4 | FAIL | **DEAD (+0.0226)** | no |
| hybrid std p=0.5 | 5.8×10⁻²² | 3.6×10⁷ | PASS | alive (+0.0020) | **YES** |
| hybrid std p=1.0 | 1.2×10⁻²⁹ | 1.7×10¹⁵ | PASS | alive (+0.0089) | **YES** |
| hybrid simple p=0.5 | 1.26×10⁻¹⁴ | 1.7 | FAIL | alive (−0.0031) | no |
| hybrid simple p=1.0 | 1.8×10⁻¹⁸ | 1.2×10⁴ | PASS | alive (+0.0016) | **YES** |
| hybrid RAR p=0.5 / 1.0 | <10⁻³⁰⁰ | ∞ | PASS | alive (−0.0030/+0.0024) | **YES** |

**The corridor** (p_min from the strict solar line with each p's own fitted a₀_ref; p_max from the +0.010 SPARC
band; scanned family p ≤ 1):

- **std (F4's shape): [0.069, ≥1.0] — NON-EMPTY and wide.** (Analytic check: with a₀_ref fixed at 9.36e-11,
  p_min = ln(9.36/3.21)/ln(5.55×10⁷) = 0.060; the fitted-a₀_ref value 0.069 is consistent.)
- simple: [0.593, ≥1.0] — non-empty (the simple shape needs heavy dressing; its accel-keyed form was always
  solar-dead by ×38,000).
- McGaugh-RAR: [0, ≥1.0] — the exponential-tail shape never needed dressing.

Caveat carried from agentE: the survival line was derived for the std-μ time template; for other shapes/dressings
it is approximate — irrelevant where the suppression is ≥10⁴×, binding only for hybrid-simple near p ≈ 0.6.

## (5) Side prediction — what the corridor buys and what it costs (falsifiable hook)
The dressing factor at the wide-binary frequency (Ω_WB ≈ 4.2×10⁻¹³ s⁻¹; 7 kAU, 1.5 M☉; Ω_WB/H₀ ≈ 1.8×10⁵):
S = 0.61 at the corridor floor p=0.069; 0.11 at p=0.3; 0.027 at p=0.5; 7×10⁻⁴ at p=1. **Any corridor member
suppresses the wide-binary MOND boost** (mildly at the floor, fully OFF for p ≥ 0.5), and kills lab/atom-
interferometer MOND signatures outright (lab Ω/H₀ ≳ 10¹⁷) — including the agentG sub-a₀ door. A confirmed
full-amplitude WB anomaly (Chae-type) would pinch the std corridor to ≈[0.07, 0.1]; a WB null (Banik-type) is
consistent with any corridor p. The dressed law also tilts the deep-MOND BTFR exponent (V^(4+p) ∝ M·R^p) and
predicts mildly rising far-outer rotation curves — beyond-SPARC tests, not adjudicated here.

## VERDICT (three-way, both directions, full weight)
**PARTIAL — quantified.**
1. **Frequency-keying as a REPLACEMENT for acceleration-keying is SPARC-DEAD.** Best pure-freq variant
   +0.0226 dex — past the pre-registered DEAD threshold (+0.020), 2.3× the ALIVE line (+0.010) — failing
   with the predicted a=Ω·V signature (per-galaxy
   residual trend sign-flips, −0.45 to −0.53/dex shift, 4.4–5.2σ). The only solar-safe pure-freq shape (standard)
   is exactly the SPARC-dead one; μ_simple fails both. The tightness of the RAR in *acceleration* is real and
   frequency-keying cannot reproduce it: **the data kill the pure-frequency evasion of Door IVb outright.**
2. **But the Door-IVb kill does NOT extend to frequency-DRESSED acceleration-keying.** A single suppression
   factor a₀_eff = a₀·[(1+Ω/H₀)/(1+Ω_ref/H₀)]^(−p) with p ∈ [0.069, ≥1] keeps SPARC within +0.010 dex (p ≲ 0.3
   costs nothing; p ≈ 0.3 mildly improves) while suppressing the solar reflex by ≥3×10⁷ — **hybrid std p=0.5 and
   p=1.0 PASS BOTH tests**, as do hybrid simple p=1 and hybrid RAR at any scanned p. F4's solar-system death is
   therefore evadable by one power of frequency suppression — at the falsifiable price of (5).
3. **Context row that reframes Door IVb:** the acceleration-keyed exponential-tail shape (McGaugh RAR) already
   passes the solar budget *undressed* (δa☉ ~ 6×10⁻²⁸). The solar-reflex kill is specific to power-law-tail μ
   (F4-standard ∝ 1/2x², simple ∝ 1/x). What died at Door IVb was F4's tail, not acceleration-keying itself.

**Net for the missing object's spec sheet:** the kernel must remain acceleration-keyed in the galactic regime
(frequency-keying is data-dead there); a tail/memory mechanism whose frequency dependence enters only as a
*dressing* of a₀ with p ≥ 0.07 (one power, p=1, comfortably allowed) reconciles SPARC with the solar reflex —
the first surviving evasion of Door IVb inside the MI class, bought at the price of a suppressed/absent
wide-binary anomaly and no laboratory signature.

*Verification notes: solver = monotone log-space bisection (72 iters, 12-dex bracket), spot-validated vs brentq
(xtol 1e-300) to ≤5×10⁻¹⁵ relative, law closure exact; baseline gate reproduces the repo .out to 1e-4; grids
interior at all optima ([Υ edge] / [GRID EDGE] flags none); eV floored at 1 km/s as in the locked script;
V_flat = outer-3-point proxy (SPARC master-table V_flat not in repo) — the sign-flip is proxy-robust (last-point
proxy: shift −0.541/dex vs −0.528); Ω_ref-independence by a₀_ref refit.*
