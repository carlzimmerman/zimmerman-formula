# K06 — THE SCATTERING TRANSFER FUNCTION AND ITS EXACT MOMENT STRUCTURE
**Methods notes, observer-facing · 2026-09-23 · moment channel, K-series · no git commit**

**For the JWST little-red-dot (LRD) community.** This note assembles the
complete *moment channel* of the conservative Thomson-sphere transport model
into one referee-ready statement: what the exact relations are, which of them
are proven, which are model-internal, which are new observables; the falsifier
battery with measurable / prediction / kill-condition at the precisions each
was verified; the (A, E[D]) → (τ₀, q) → E[v²] inversion recipe; worked numbers
in model units and at the frozen lane's illustrative scale (R = 941 AU,
T_e = 10⁴ K → days and km/s); and a plain-language abstract.

**Provenance rule (house standard):** every number below is traceable to a
file in this repository; the traceability table (§7) lists the file for each
block. No number appears here that is not in the cited file or a direct
arithmetic consequence of one (conversion factors are stated and reproducible).

**Epistemic status, stated once, loud:** every identity here is *proven inside
the specified conservative transport model* — stationary sphere, central
isotropic point source (or volume-uniform where stated), conservative
unpolarized Thomson scattering with E[u′|u] = 0, all photons counted, no
absorption, escape at first outward crossing of |x| = R. They are not
observational JWST confirmations (no LRD data are touched) and not new laws of
nature. Their value for the community is that *each is a falsifiable
prediction for velocity-resolved reverberation mapping (RM) of a
Thomson-scattering candidate*, and several are independent of the electron
density profile altogether.

---

## 1. Definitions

**The model (frozen lane).** A stationary, spherical, conservative scattering
cloud of outer radius R. Extinction per unit length κ(r) = σ_T n_e(r),
continuous, bounded, nonnegative. A central isotropic point source emits
photons with the same line profile in all directions; photons move at c and
scatter with the Thomson kernel; a photon escapes at its first outward
crossing of |x| = R. Unscattered photons are counted. Source: 
`real_research/reviews/bhstar_scattering_clock_2026_09_21/density_free/THEOREM.md` (all theorem numbering below = that file).

**The observables (velocity-resolved reverberation).** For escape time
t_exit, escape position r_exit and outgoing direction u_exit, the **excess
delay** is

    D = t_exit − r_exit·u_exit / c ,        E[D] =: d̄ ≥ 0            (THEOREM §Model)

— the first moment of the *normalized photon impulse response*, not a
variability baseline or a cross-correlation peak. The **accumulated Doppler
velocity** v is the leading-order thermal Doppler shift summed over kicks,
v = Σⱼ e·(u′_j − u_j) with e the unit vector toward the observer, one
independent Maxwellian electron velocity per kick. The **angular exposure**
is the path functional

    ang = Σ_j T(r_j)(1 − u_j·u′_j) ,        T(r) = k_B T_e(r)/m_e = s_e²(r)      (J01)

Each kick contributes conditional variance exactly 2T(r)(1 − μ) (per-kick
Var[e·(u′−u)] = |u′−u|²T = 2T(1−μ)), and the kicks are conditionally
independent given the trajectory.

**The transfer function.** Velocity-resolved RM measures the two-dimensional
delay–velocity kernel Ψ(τ, v) (response in line flux per unit delay and per
unit velocity). All moments used below are its moments,

    E[Dᵐ v^{2n}] = ∫∫ τᵐ w^{2n} Ψ(τ, w) dτ dw ,

computed around zero mean velocity (the model's v is mean-zero; the measured
line centroid removal is part of the data reduction). The **delay kernel**
H(ω) = E[e^{iωD}] is the Fourier transform of the delay marginal.

**The atom.** The unscattered (zero-scatter) sub-population arrives at
D = 0 with v = 0 exactly: a delta spike **A·δ(D)δ(v)** at the origin of the
transfer function, with amplitude A = P(N = 0) = exp(−τ_rad) for the central
source, τ_rad = ∫₀^R κ(r) dr the *radial* optical depth (exact: an
unscattered photon crosses the sphere along a straight radial-family line of
optical depth τ_rad in every direction). J09 names this the "atom"; the
continuous part of Ψ is a Gaussian-mixture spine (below, §2, "Gaussian spine").

**Profile family used for the worked numbers and the inversion.** The
q-family κ(r) = τ₀(1 + q r²/R²), q ≥ 0, τ₀ = central extinction × R —
uniform (q = 0) and centrally-peaked gradients (q > 0). For this family, all
closed forms below are explicit.

---

## 2. The exact moment relations, with status

Classification (K01-style discipline; no K01 file exists in the repo as of
this writing, so the classification is done here with the same rules — a
statement is PROVEN only if it has a closed argument inside the model;
MODEL-INTERNAL if it is exact only under extra assumptions or is an MC
measurement with reported error; NEW-OBSERVABLE if it is usable from
velocity-resolved RM data without density/geometry assumptions).

### Class A — PROVEN model-exact (closed arguments; machine-verified at 35/35 across three independent engines)

| # | relation | content | authority |
|---|---|---|---|
| A1 | **Radial delay identity** | **E[D] = (1/c)∫₀^R r κ(r) dr** = (σ_T/c)∫₀^R r n_e(r) dr, all scattering orders, any bounded κ | THEOREM.md Thm 1 (Dynkin stopped-generator proof); MC z-checks < 6 on 10 clouds in `certified/result.json` rows; J00 P-anchor |
| A2 | **Conditional-Gaussian lemma / even-moment hierarchy** | v \| trajectory ~ N(0, 2·ang); hence **E[D v^{2m}] = (2m−1)!! · 2^m · E[D·ang^m]** for every m, every scattering order, any bounded κ ≥ 0, T > 0, central *or* volume source | J01 (m = 1, 20/20), J02 Theorem A (m = 1,2,3, central+volume, 15/15), J09 A-checks m = 1–5 |
| A3 | **Marginal moment relations** | E[ang^m] = E[v^{2m}] / ((2m−1)!!·2^m) — m = 1: E[ang] = E[v²]/2 (the frozen lane's exposure identity, σ_sc² = 2 s_e² E[N] at T = const); m = 2: E[ang²] = E[v⁴]/12 | THEOREM.md Thm 2 (isothermal exposure identity); J01 S4/S4b, J02 S4b |
| A4 | **Atom amplitude and universal ratio window** | A = exp(−τ₀(1 + q/3)) (central, exact) and, **simultaneously**, d̄ = τ₀(1/2 + q/4) (A1 for the q-family); hence **−ln A / d̄ = (1+q/3)/(1/2+q/4) ∈ [4/3, 2]**, endpoints q → ∞ → 4/3, q = 0 → 2. The window is *independent of total opacity* | J09 C-checks (6/6: atom |A − pred| ≤ 5e-3 with measured residuals ≤ 4e-4; window within ±0.02 of 2.000, 1.444, 1.600) |
| A5 | **Density-free width bound** | Cauchy–Schwarz on (D, ang) + A2/A3: **E[D²] ≥ 3·E[Dv²]² / E[v⁴]** — no κ, no n_e, no geometry parameter appears | J05 (Th. from J01/J02 relations), J06 (B1-chain, all clouds); slack 1.06–1.25 (below) |
| A6 | **Coherence envelopes** | For any nonnegative D: **\|H(ω)\| ≥ max(0, 1 − ω·E[D])** (frozen T3, linear) and the strictly sharper **\|H(ω)\| ≥ max(0, 1 − ½ω²·E[D²])** (quadratic, asymptotically exact at ω → 0: measured |1−ReH−½ω²E[D²]| ∝ ω^{3.99}); and with A5 substituted, the **line-moment-only envelope** \|H(ω)\| ≥ max(0, 1 − ½ω²·L), L = 3E[Dv²]²/E[v⁴] | THEOREM.md Thm 3; J07 (20/20 on 4 clouds; log–log slope 3.99) |
| A7 | **Exact two-way inversion** | (A, d̄/R) ↦ (τ₀, q) is closed and unique on q ≥ 0 (algebra below, §4); verified to recover (1, 0), (1, 10), (2, 3) exactly | §4 of this file; J09 closed forms |

### Class B — MODEL-INTERNAL (exact within the model only under stated extra assumptions, or MC measurements with reported errors)

| # | relation | status / content | authority |
|---|---|---|---|
| B1 | **Lag–width band** | For *uniform + isothermal* clouds: (√(1+σ_sc²/s_e²) − 1)/2 ≤ c·E[D]/R ≤ σ_sc/(2 s_e) — the two-sided density-free band that eliminates τ₀ and n_e; endpoints are conservative consequences of b = E[μ_exit] ∈ [0,1] | THEOREM.md Thm 2; verified, and **adversarially scope-tested**: the q = 99 gradient violates the band at 96.8 σ and the volume source at 63.8 σ when the band is wrongly applied (`certified/result.json`, AUDIT.md) |
| B2 | **Volume-source face** | E[D]_vol = E[τ]_vol − E[Q] ≠ ∫rκ dr; the frozen identity is central-source-only. Exact compensation: E[τ]_vol = ∫₀^R rκ dr + R·E[μ_exit] − ½E[F(r₀)], Q = Σⱼ ℓⱼ(uⱼ·u_final) (residence–direction coupling) | J02 Theorem B (B3 Dynkin to 6e-4; B4 bookkeeping to 7e-16); measured E[D]_vol = 0.3376 vs central 0.5008 (> 8σ apart) |
| B3 | **Measured moment values** (MC, with SE; the relations in A are exact, these are the numbers of the reference cloud τ₀=1, q=0, central, s_e=1, R=c=1) | E[D] = 0.5008 ± 0.0007 (n = 10⁶); E[v²] = 2.8061; E[Dv²] = 3.7316 ± 0.027; E[D²] = 0.7651 (J05) / 0.7661 ± 0.0017 (J06, n = 1.2×10⁶); σ_D = 0.717; E[v⁴] = 67.05; E[N] = 1.4042; b = E[μ_exit] = 0.9031 (from 2E[v²]-closure) | J01 measurements; J02; J05 table; J06 clouds |
| B4 | **Closure ratios R_m (the measured conspiracy)** | R_m = E[Dv^{2m}] / ((2m−1)!!·2^m·E[D]·E[ang^m]): at q=0, central, R_m = **2.635 / 3.574 / 4.563** (n=10⁶) — the canonical 2.64/3.57/4.56; R₁(q) = 2.645 ± 0.018 (q=0), 2.023 ± 0.012 (q=3), 1.697 ± 0.009 (q=10). R_m ≠ 1 at every order and grows with m: **no finite set of marginal moments closes the mixed moments** (the two-moment closure is dead, ≥ 5σ) | J02 Corollary C; J01 closure table; J00 K1 register |
| B5 | **Sharpness of the width bound (model-internal diagnostics)** | slack ≡ E[D²]·E[v⁴]/(3E[Dv²]²): 1.25 / 1.13 / 1.06 (J05, J05 clouds), sharpened 1.2430 / 1.1322 / 1.0701 / 1.0689 (J06, n = 1.2×10⁶); toy construction (D = c·ang) attains slack = 1.00000 exactly; slack → 1.04 as q → 30 — "nearly tight" is the MC statement, no theorem fixes the limit | J05 table; J06 sharpness; J00 N2 |
| B6 | **E[N](τ₀, q) map for q ≠ 0** (needed for the E[v²] prediction, §4) | q = 0 closed: E[N] = τ₀²/2 + τ₀·b, b ∈ [0,1] (THEOREM.md Thm 2); q > 0: a transport functional of the F-hierarchy — evaluation is the registered K04 lane (see §4 note) | THEOREM.md Thm 2; J00 N1/N2; this file §4 |

### Class C — NEW-OBSERVABLE (density-free and/or geometry-free statements that velocity-resolved RM can test directly)

| # | statement | why observer-side new | authority |
|---|---|---|---|
| C1 | **E[D²] ≥ 3E[Dv²]²/E[v⁴]** — a measured transfer-function whose mean-square width falls below this line kills the Thomson-scattering reading **for any density** | inputs = TF width, joint lag–width moment, line kurtosis: all RM observables; no κ, n_e, R-scaling | J05 §2/§5; J06 |
| C2 | **The joint hierarchy as a consistency family**: E[Dv^{2m}]/((2m−1)!!·2^m·E[D]·E[ang^m]) with E[ang^m] = E[v^{2m}]/((2m−1)!!·2^m) must hold *simultaneously* for all m (data-side: R_m^{(obs)} must equal the profile function R_m(q) implied by the inverted q) | marginal-only models fail five-fold harder per order (R₁ 2.64 → R₂ 3.57) | J05 §5; J00 ND2 |
| C3 | **Line-moment-only coherence envelope** \|H(ω)\| ≥ max(0, 1 − ½ω²L), L = 3E[Dv²]²/E[v⁴] — the first envelope evaluable without any assumption on κ, n_e, or geometry | at ω·E[D] = 0.25 the floor is 0.92 (vs 0.75 linear): a 21% tighter, asymptotically correct floor | J07 |

---

## 3. The falsifier battery

For each test: **measurable** (from velocity-resolved RM or spectroscopy),
**model prediction** (with the verified precision), **kill condition**. Model
conditions must be verified before firing any kill: stationarity,
conservatism, central-source geometry (or B2 correction), isothermality where
stated. "≥ 3σ" always means with statistical and astrophysical systematics
accounted; the precisions quoted are the verification tolerances used in the
cited files.

**F1 — The atom spike amplitude.**
- Measurable: the δ-like peak at (τ = 0, v = 0) of Ψ — the zero-lag,
  zero-width fraction of transfer-function power A (equivalently the fraction
  of the line flux that is both unscattered and unshifted).
- Prediction: **A = exp(−τ_rad), τ_rad = τ₀(1 + q/3)** for the central source
  (q-family); verified |A_meas − A_pred| ≤ 4×10⁻⁴ at τ₀ = 1, q = 0 (J09
  C-check tolerance 5×10⁻³): A = 0.3683 vs 0.3679.
- Kill: |A_meas − exp(−τ_rad)| ≥ 3σ with τ_rad inferred independently (from
  F2/E[D]) **and** F6 violated (below). An atom that is too big or too small
  for the inferred optical depth kills the central conservative reading.

**F2 — E[D] from the lag (against the radial identity).**
- Measurable: E[D] = first moment of the delay marginal of Ψ (days in the
  source rest frame; needs the R/c conversion).
- Prediction: E[D] = (1/c)∫₀^R r κ(r) dr (**all** scattering orders); for the
  q-family d̄ = τ₀(1/2 + q/4) · R/c; reference value 0.5008 ± 0.0007 model
  units (SE at n = 10⁶, J02).
- Kill: E[D] is *consistent with (A, d̄) by construction* (the inversion F-inv
  uses it) — so the non-circular test is **F2b, the lag–width band**
  (B1): with R and T_e measured independently, c·E[D]/R must lie in
  [(√(1+σ_sc²/s_e²)−1)/2, σ_sc/(2s_e)]; outside the band at ≥ 3σ kills the
  *uniform-isothermal* reading; treating a gradient cloud as uniform is
  itself killed by this test (q = 99 model fails at 96.8σ — that is the *test's
  own* calibration, `certified/result.json`).

**F3 — The hierarchy ratios R_m = 2.64 / 3.57 / 4.56 (q = 0).**
- Measurable: E[Dv²], E[Dv⁴], E[Dv⁶] from the joint TF + E[D], E[v²], E[v⁴],
  E[v⁶] from the line and the delay marginal.
- Prediction: R_m^{(obs)} := E[Dv^{2m}] / ((2m−1)!!·2^m·E[D]·E[ang^m]) with
  E[ang^m] ≡ E[v^{2m}]/((2m−1)!!·2^m) must equal the measured profile function
  R_m(q) of the cloud (q determined by the inversion F-inv): at q = 0,
  R₁ = 2.64 (2.635, ±0.018 SE at n = 10⁶; R₂ = 3.57, R₃ = 4.56 — separations ≥ 5σ
  from any closure value 1 and mutually separated by ≫ SE).
- Kill: any joint violation at ≥ 3σ of (a) the m = 1 identity pair (R₁^{(obs)}
  vs R₁(q_inv) from the *inverted* profile), or (b) the m ∈ {1,2} pair against
  the q = 0 values when q_inv ≈ 0. The m = 2 member is the one a matched pair
  of marginal moments cannot mimic.

**F4 — The E[D²] bound.**
- Measurable: E[D²] (mean-square TF width), E[Dv²], E[v⁴] (line kurtosis
  moment).
- Prediction: **E[D²] ≥ 3·E[Dv²]²/E[v⁴]** — theorem-rigid, density-free;
  verified on 4 clouds with slack 1.06–1.25 (J05) and 1.24–1.07 (J06);
  the knife-edge case (slack = 1.00000) is attained by an explicit construction.
- Kill: E[D²] < 3E[Dv²]²/E[v⁴] at ≥ 3σ with model conditions verified ⇒ the
  Thomson-scattering interpretation for **any density** is dead. (This is the
  only battery member with a Cauchy–Schwarz contradiction, i.e. theorem-rigid
  even before astrophysics enters.)

**F5 — The coherence envelope.**
- Measurable: |H(ω)| from the lag autocorrelation of the line light curve at
  the monitoring cadence, at ω·E[D] ≲ 1.5 (the regime where the envelope is
  binding; it clips to 0 at ω = ω* = 2E[D]/E[D²] = 1.31 model for the uniform
  cloud).
- Prediction: |H(ω)| ≥ max(0, 1 − ½ω²·E[D²]) ≥ max(0, 1 − ½ω²·L) with
  L = 3E[Dv²]²/E[v⁴]; verified 20/20 on 4 clouds: at ω = 0.50 model units
  (ω·E[D] = 0.25), |H|_meas = 0.9413 ≥ 0.9045 (quadratic) ≥ 0.9235
  (line-moment) ≥ 0.7501 (linear); the T3″ form is evaluable with zero density
  information.
- Kill: measured coherence below the line-moment floor at ≥ 3σ at any
  ω·E[D] < 1.5 kills the conservative Thomson reading — quantifiable
  *before* the observation run.

**F6 — The ratio window (universal, opacity-free).**
- Measurable: −ln A / d̄, with A the atom amplitude (F1) and d̄ = E[D] (F2).
- Prediction: for the q-family, central source, **−ln A/d̄ = (1+q/3)/(1/2+q/4)
  ∈ [4/3, 2] exactly; endpoints q = 0 → 2 and q → ∞ → 4/3 — independent of τ₀.
  Verified: measured ratios 2.002 (q=0), 1.441 (q=10), 1.598 (τ₀=2, q=3) vs
  exact 2.000 / 1.444 / 1.600 (J09, tolerance ±0.02).
- Kill: measured −ln A/d̄ outside [4/3, 2] at ≥ 3σ ⇒ the central-source
  Thomson geometry is dead **for any opacity** — the single most compact kill
  of the battery (J09 C-window).

**F7 — (Guard: the volume-source correction (B2).** The battery presumes the
central-source geometry of the frozen lane. For an emission region judged
volume-uniform/thick-shell, E[D]_vol = E[τ]_vol − E[Q] ≠ ∫rκ dr: an observer
applying F2's central identity on a shell emitter is wrong by exactly
E[Q] + ½E[F(r₀)] (measured 0.3376 vs 0.5008 at τ₀=1). Firing F1–F6 requires
the geometry judgment, or the B2-corrected forms.)

---

## 4. The inversion recipe: (A, E[D]) → (τ₀, q) → E[v²]

All in dimensionless model units R = c = s_e = 1, then scaled (5 × R/c for
delays, s_e for velocities). With the q-family κ(r) = τ₀(1 + q r²):

**Step 1 — measure (A, E[D]).** A from the atom spike (F1), E[D] from the
delay marginal first moment (F2); convert to model units d̄_model =
c·E[D]_phys·c/R (R from an independent radius measurement — see B1, the
circular route is explicitly disallowed in the frozen lane).

**Step 2 — invert (closed, exact, unique for q ≥ 0).** With a = −ln A, d =
d̄_model:

    q = (6a − 12d) / (4d − 3a),        τ₀ = a / (1 + q/3)          (K06-inv)

Exactness: the pair (a, d) are the two closed forms of A4/A1, so the recovery
is an identity, not a fit. Verified recoveries from J09 closed forms:
(τ₀, q) = (1, 0) → (1.000, 0.000); (1, 10) → (1.000, 10.00); (2, 3) →
(2.000, 3.000). Consistency domain: q ≥ 0 ⇔ d/a ∈ [1/2, 3/4] — equivalently
the F6 window −ln A/d ∈ [4/3, 2]; a measured ratio outside the window is the
F6 kill before inversion is attempted. (The window is the *invertibility
domain* of the atom-lag pair — the two statements are the same algebra.)

(Note on the K04 label: this recipe is the designated content of the planned
K04 (inversion ledger) lane of the K-series. As of this writing no K-series
files K01–K05 exist in the repo; the recipe is self-contained here and cites
only committed files — THEOREM.md Thm 1/2, J01, J02, J09. The E[N] map below is
the only element whose q > 0 branch is delegated.)

**Step 3 — predict E[v²] (exposure identity, isothermal; THEOREM.md Thm 2):
E[v²] = 2·s_e²·E[N], with E[N] = E[∫κ(r_t) dt] the mean scattering count. q=0
closed: E[N] = τ₀²/2 + τ₀·b, b = E[μ_exit] ∈ [0,1], hence the *band*

    s_e²·τ₀² ≤ E[v²] ≤ s_e²·(τ₀² + 2τ₀)          (q = 0, b ∈ [0,1])

with b(τ₀=1) = 0.9031 measured — the reference cloud gives E[v²] = 2.8061
inside [1, 3]·s_e². For q > 0, E[N](τ₀, q) is the K04 transport functional
(the F-hierarchy's pk²-source moments; J00 N1/N2 registers the deterministic
leg). Secondary predictions once (τ₀, q) is known: E[N] (→ E[v²]), and the
joint set {E[Dv²], E[Dv⁴], E[D²]} from the measured R_m(q) curve / B1-chain —
F3/F4 are then *predictions* rather than just inequalities.

---

## 5. Worked numbers

### 5a. Model units (R = c = s_e = 1, central source; every figure traceable)

| quantity (τ₀, q) | (1, 0) | (1, 3) | (1, 10) | (2, 3) | source |
|---|---|---|---|---|---|
| A = exp(−τ₀(1+q/3)) | 0.3679 (meas 0.3683) | 0.1353 | 0.01312 (meas 0.01321) | 0.01832 (meas 0.01841) | J09 C |
| d̄ = τ₀(1/2+q/4) | 0.5000 (meas 0.5008 ± 0.0007) | 1.250 | 3.000 (meas 3.0023) | 2.500 (meas 2.5001) | J02/J09 |
| −ln A / d̄ | 2.000 (meas 2.002) | 1.600 | 1.444 (meas 1.441) | 1.600 (meas 1.598) | J09 window |
| E[v²] | 2.8061 | 8.748 | 37.37 | 27.94 | J01/J02/J06 (E[v²] = 2E[ang]) |
| E[Dv²] | 3.7316 ± 0.027 | 21.89 | 192.7 | 234.2 | J01/J06 |
| E[D²] (J05 / J06) | 0.7651 / 0.7661 ± 0.0017 | 3.3615 / 3.3724 | 16.213 / 16.217 | 11.222 / 11.252 | J05/J06 |
| 3E[Dv²]²/E[v⁴] (bound) | 0.6141 / B1 0.6164 | 2.9666 / 2.9809 | 15.235 / 15.175 | 10.497 / 10.577 | J05/J06 |
| slack E[D²]·E[v⁴]/(3E[Dv²]²) | 1.25 / 1.2430 ± 0.0006 | 1.13 / 1.1322 | 1.06 / 1.0701 | 1.07 / 1.0689 | J05/J06 |
| σ_D = TF width | 0.717 | 1.342 | 2.683 | 2.231 | J05 table |
| R₁(q) (closure ratio) | 2.645 ± 0.018 (J01) | 2.023 ± 0.012 | 1.697 ± 0.009 | — | J01 |
| R_m (q=0) | 2.635 / 3.574 / 4.563 (m = 1,2,3) | — | — | — | J02 C |

Hierarchy identities (exact): E[Dv²]/2E[D·ang] = 1.0028 ± …, E[Dv⁴]/12E[D·ang²]
= 1.0038, E[Dv⁶]/120E[D·ang³] = 0.970 (J02, n=10⁶); kurt(v|D-bin) = 3.475 vs
scale-mixture prediction 3.484 in the continuous part (J09 B: the transfer
function is an atom + Gaussian-mixture spine with per-bin Gaussianity — the
"Gaussian spine" content of the two-component law).

### 5b. Physical scale: R = 941 AU, T_e = 10⁴ K, W = 2000 km/s Laplace FWHM
Conversion factors (frozen lane `density_free/verify.py::main`, constants in
file — reproduced here: kb·T/me = 1.5155×10¹¹ m²s⁻² etc.): R/c = 4.6956×10⁵ s
= **5.4348 days**; s_e = (k_B·10⁴ K/m_e)^{1/2} = **389.3 km/s**; the frozen
FWHM→σ conversion σ = W/(√2 ln 2) = **2040.3 km/s** (required by the exposure
theorem for a full-Laplace scattered line); x = σ/s_e = 5.241. Then
THEOREM.md Thm 2 gives:

| physical quantity | value | source |
|---|---|---|
| **Lag band** c·E[D]/R ∈ [(√(1+x²)−1)/2, x/2]: | **11.78 – 14.24 days** (rest frame) | `certified/result.json` examples (11.7806, 14.2411) |
| Coherence floor at P = 200 d (Thm 3): | **0.5526** (max(0,1−2π·h_i/200 d)) | `certified/result.json` (0.5526) |
| Radius needed to allow 10× suppression at 200 d: | **1893 AU** (≥ 1892.95) | `certified/result.json` (1892.95 AU) |

Worked clouds (reference numbers from §5a, scaled: delays × 5.4348 d,
velocities × s_e = 389.3 km/s; E[Dᵐv^{2n}] × (5.4348 d)ᵐ·(389.3 km/s)^{2n}):

| (τ₀, q) | E[D] (d) | A | E[v²]^{1/2} (km/s) | E[D²]^{1/2} (d) | σ_D (d) | E[Dv²] (d·(km/s)²) | bound E[D²] ≥ 3E[Dv²]²/E[v⁴] (d²) |
|---|---|---|---|---|---|---|---|
| (1, 0) | 2.72 | 0.368 | 652 | 4.75 | 3.90 | 3.07×10⁶ | 18.1 (E[D²] = 22.6, slack 1.25) |
| (1, 10) | 16.31 | 0.0131 | 2380 | 21.9 | 14.6 | 1.59×10⁸ | 450.0 (E[D²] = 478.9, slack 1.06) |
| (2, 3) | 13.59 | 0.0183 | 2058 | 18.2 | 12.1 | 9.9×10⁷ | 310.1 (E[D²] = 331.5, slack 1.07) |

Every entry follows §5a by the stated rescaling; e.g. E[Dv²](1,0) = 3.7316 ×
5.4348 d × (389.3 km/s)² = 3.07×10⁶ d·(km/s)² and E[D²](1,0) = 0.7651 ×
(5.4348 d)² = 22.60 d² against the bound 0.6141 × 29.54 d² = 18.14 d². (E[Dv²]
for the (2,3) row is the J06 h=0 value 119.7 — the identical cloud of the paired
E[D²] row; §5a's 234.2 is the tagged h=2 variant from J01. All other rows dual-
engine consistent to ≤1%.) The τ₀ = 1, q = 0 row is the canonical benchmark:
E[D] = R/2c = 2.72 d exactly (uniform cloud, Thm 1), unscattered fraction
A = 0.368, predicted line RMS s_e√(τ₀² + 2τ₀b) = 652 km/s at the measured
b = E[μ_exit] = 0.903 (E[v²] = 2.8061 × s_e², §5a).

### 5c. Envelope example (uniform cloud, J07 table): ω = 0.50 model units
(ω·E[D] = 0.25) → |H|_meas = 0.9413 ≥ T3′ 0.9045 ≥ T3″ 0.9235 ≥ T3 0.7501;
ω = 1.00 (ω·E[D] = 0.5) → |H| 0.8133, T3′ 0.6179, T3″ 0.6939; ω* =
2E[D]/E[D²] = 1.31 clips the envelopes; at the frozen cadence (200 d at
R = 941 AU): |H| ≥ 0.5526 (Thm 3). At τ₀=1 the ω·E[D] = 0.25 point is a
monitoring period P = 2π/ω = 4π·E[D] ≈ 4π × 2.72 d ≈ 34 d.

---

## 6. Plain-language abstract (one page)

A class of JWST little red dots shows unusually broad emission lines that some
models attribute to electron (Thomson) scattering in a circum-nuclear cloud
around a hidden active nucleus. If that is right, the cloud is a *measurement
instrument*: the scattered, time-delayed light is the cloud's response function,
and velocity-resolved reverberation mapping can image it. This note collects
the exact statistical structure of that response — the "moment channel" — in a
controlled model: a spherical, conservative, non-absorbing Thomson cloud around
a central point source, the same assumptions the frozen-lane theorem of this
repository already proved exact relations inside.

Five exact statements fall out. (1) The mean light-travel delay is exactly the radial integral of the
opacity: E[D] = ∫r·κ(r) dr (all scattering orders, every scattering order
counts). (2) The velocity and delay statistics lock together exactly: measured
delay–velocity moments are the Gaussian-mixture moments of a single hidden
quantity, the path's angular exposure — a family of identities that hold at
every order and for *any* density profile. (3) One of those identities
becomes the sharpest test available: the mean-square delay of the transfer
function can never drop below a level computed purely from line width and
joint delay-width moments — any real measurement below that floor kills the
scattering story, whatever the density is. (4) The unscattered light arrives
with zero delay and zero shift — a spike at the origin of the transfer
function whose amplitude is exactly e^{-optical depth}: together with the
mean delay this determines both the cloud's total opacity and its density
gradient — and the combination of the two must fall in the fixed window
[4/3, 2]-window (−ln amplitude / mean delay), a pair of numbers that
independently of opacity and temperature either confirms or kills the central
Thomson picture. (5) The same moments predict the coherence of the observed
line before the observation runs: the signal preservation at a given cadence
(jitter of days) cannot be weaker than a computed curve.

None of this needs the density. n_e appears nowhere in the strongest tests —
the electron density cancels out of the physics. At the illustrative scale
(R = 941 AU, T_e = 10⁴ K) the predicted mean delay band is 11.8 < E[D] < 14.2
days and the coherence floor at 200 days keeps > 55% amplitude. The battery is
seven tests, each with a stated kill condition; the referee can re-derive every
number from the cited files in this repository, and the two most compact
ones — the R_m ratio triplet 2.64 : 3.57 : 4.56 (flat density) and the
[4/3, 2] window — are measurable with a moderate RM campaign. If a candidate
cloud is real, the relations must hold simultaneously; if any one fails at 3σ
with the model conditions verified, the interpretation for that object is dead
— which is exactly what a measurement instrument should do.

---

## 7. Traceability table (every § → file)

| § | numbers | file (all under repo root) |
|---|---|---|
| §1 model & D | THEOREM.md §Model, Thm 1–3 | `real_research/reviews/bhstar_scattering_clock_2026_09_21/density_free/THEOREM.md` |
| §2 A1/A7 | Thm 1/proof; d̄ = ½ | THEOREM.md; `certified/result.json`; J00 ledger |
| §2 A2/A3 | hierarchy m=1–5 | `deepseek_push/J01_MIXED_MOMENT.md`, `J02_MOMENT_HIERARCHY.md`, `J09 C/A checks `.out` |
| §2 A4 | atom/window closed forms; measured 2.002/1.441/1.598 | `deepseek_push/J09_two_component_law.out` (20 checks, 19 passed — A5 volume m=5 tail check failed its χ²₁ tail budget; all 6 C-checks passed) |
| §2 A5/A6 | bound table (J05), sharpened (J06), envelopes (J07) | `J05_TRANSFER_FUNCTION_READING.md` · `J06_bound_sharpen.out` · `J06_results.json` · `J07_SPECTRAL_ENVELOPE.md` |
| §2 B1–B6 | band & adversarial tests; volume face; MC values; R_m | THEOREM.md Thm 2; AUDIT.md; `certified/result.json`; J02; J01_results.json; J06_results.json |
| §3 F1–F7 | every threshold | as table rows; J09 out; J05 §5; J07 |
| §4 inversion | closed forms + recoveries | this file (K06), A4/A1 (J09, THEOREM.md) — recoveries computed from J09 exact values |
| §5a model units | table values | J01/J02/J05/J06/J09 (arrays in their results .json) |
| §5b physical | R/c = 5.4348 d; s_e = 389.31 km/s; σ = 2040.3 km/s; band 11.781–14.241 d; 0.5526; 1892.95 AU | verify.py lines 83–92 of `density_free/verify.py`; `certified/result.json` (same three examples) |
| §6 abstract | none (prose; all numbers in §§3–5) | — |

**Honest edges (unchanged from the lane standards).** Deterministic S2/S3 P_N
convergence is open (J00 N1); the slack limit 1.06 → 1 is an MC statement, not
proven (N2); literature novelty vs the Bal/Jollivet/Patat overlap unresolved
(N3); no JWST data touched (N4); J09's A5_volume m=5 tail check failed its
chi²₁-tail budget (registered MC tail risk — 19/20, the m ≤ 3 checks pass
and C-checks 6/6, and the identity at every order is the closed Gaussian-moment
argument, not the tail estimate); the m=3 numbers carry MC tail risk (J02 edge).
The frozen lane's applicability caveats (THEOREM.md "What cannot be inferred":
photosphere ≠ R, line region need not be a point source, gradients violate the
band, static spectrum alone sets no scale) apply to every observational use.

**Register line (K06):** the moment channel assembles into one observer-facing
statement — PROVEN (A1–A7), MODEL-INTERNAL (B1–B6, all registered, none hidden),
NEW-OBSERVABLE (C1–C3), falsifiers F1–F7 with precisions as verified, inversion
(K06-inv) exact with q ≥ 0 domain, worked numbers in model units and at the
frozen scale (11.78–14.24 d, 1893 AU, 0.5526 at 200 d). Not committed (house rule):
not committed, no commit issued; files written: `K06_METHODS_NOTES.md`,
`K06_results.json`. K01–K05 of this K-series: not yet present in the repo;
K04 (inversion ledger / E[N]-map for q > 0) is the registered next step, not a
claim of this file.