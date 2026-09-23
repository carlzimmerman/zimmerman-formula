# K11 — THE SCATTERING-CLOCK CHANNEL AND THE ONE-BOUNDARY STATEMENT

**2026-09-23 · moment channel → framework core · synthesis of J00–J11 + K01–K06**
**Every number below is traceable to the cited file; nothing invented here. No git commit.**

**The unified statement.** The whole J/K series is ONE observable door onto the
framework core: a velocity-resolved reverberation-mapping (RM) measurement of a
Thomson-scattered broad-line region (BLR) reads off three numbers from the 2D
transfer function — the atom amplitude A, the mean lag d̄_phys, the width
moments — and the pair (A, d̄) both *inverts* to the cloud's hidden state
(τ₀, q) and *tests*, through the opacity-free window, whether the cloud sits at
the framework's density-local a₀-radius r_B = √(GM_b/a₀(ρ_B)). Geometry enters
as an observable (discrimination tree, §2), the error chain is propagated (§3),
and everything lands as one numbered falsifier battery (§4) with an explicit
NOVEL/CONSISTENCY ledger (§5) and a "what this does not claim" (§6).

---

## 1. The chain: transfer function → (A, d̄, width) → (τ₀, q) → the radius reading

### 1.1 What velocity-resolved RM measures (the 2D transfer function)

Velocity-resolved RM measures the delay–velocity kernel Ψ(τ, v) (response in
line flux per unit delay and per unit velocity). All channel statements are its
moments E[Dᵐv^{2n}] = ∫∫ τᵐ w^{2n} Ψ(τ,w) dτ dw (K06 §1):

| observable | definition | physical content |
|---|---|---|
| **A** | amplitude of the zero-lag, zero-width spike A·δ(D)δ(v) | unscattered (ballistic) fraction = exp(−τ_rad), central source |
| **d̄_phys** | c·E[D] = c·∫τΨ dτdv | mean excess geometric delay; E[D] = (1/c)∫₀^R r κ(r) dr (frozen Thm 1, **exact all scattering orders**) |
| **width** σ_D = √(E[D²]−E[D]²) | transfer-function width | constrained from below by the density-free bound (J05/J06) |

Verified: E[D] = 0.5008 ± 0.0007 model units (J01; deterministic K05:
0.500000, no RNG), A = 0.3679 (K02 third-motor 0.367932 ± 0.000341, z = +0.16),
σ_D = 0.717 (J05). Physical scale (K06 §5b, frozen lane R = 941 AU, T_e = 10⁴ K):
R/c = 5.4348 d, s_e = 389.3 km/s; the canonical cloud (τ₀=1, q=0) gives
d̄_phys = 2.72 d, A = 0.368, width σ_D = 3.90 d.

### 1.2 The atom + lag pair inverts to (τ₀, q) — geometry-free

Closed, exact, unique on q ≥ 0 (K06 §4, K06-inv; J09 closed forms):

```
a = −ln A ,  d = d̄_model
q = (6a − 12d) / (4d − 3a) ,        τ₀ = a / (1 + q/3)
```

Verified recoveries: (1, 0) → (1.000, 0.000); (1, 10) → (1.000, 10.00);
(2, 3) → (2.000, 3.000). **Consistency domain:** q ≥ 0 ⇔ d/a ∈ [1/2, 3/4] ⇔
−ln A / d̄ ∈ [4/3, 2] — *the window is the invertibility domain of the pair.*
No κ, no n_e, no geometry parameter appears in the inversion inputs. Once
(τ₀, q) is known the channel *predicts*, not fits: E[v²] via the exposure
identity and the K04 E[N] map (q = 0 closed: s_e²τ₀² ≤ E[v²] ≤ s_e²(τ₀² + 2τ₀)),
E[Dv²], E[Dv⁴], E[D²] via the R_m(q) curves (K06 §4 Step 3).

### 1.3 The window tests the radius reading r_B = √(GM_b/a₀(ρ_B))

The opacity-free window (J09-D, central q-family):

> **−ln A / d̄ = (1 + q/3)/(1/2 + q/4) ∈ [4/3, 2]** — τ₀ cancels. (27/27 J09;
> third engine 28/28: 2.00207/1.59782/1.44414 vs 2.000/1.600/1.4444, z ≤ 0.82.)

The physical lag fixes the cloud radius geometry-free: R = c·d̄_phys/E[D]
(E[D] from Thm 1, dimensionless). The framework supplies R = r_B =
√(GM_b/a₀(ρ_B)) with a₀(ρ_B) = (c/2)√(G·ρ_B) — the density-local a₀ at the
layer (doorB; NOT the deep-MOND kpc-scale √(GM/a₀)). Therefore (J10-I, 6/6,
J10_verify.py):

> **J10-I = −ln A · √(GM_b/a₀(ρ_B)) / (c·d̄_phys) = (r_B/R) × window ∈ [4/3, 2]**

- A measured from the atom spike; d̄_phys from the lag; M_b, ρ_B measured/known;
  a₀(ρ_B) = (c/2)√(Gρ_B) — the framework constant at the layer, nothing else.
- Inside the window: the pair (A, d̄) inverts to (τ₀, q) and predicts the
  remaining observables — the channel becomes a **two-parameter measurer of the
  a₀ cloud**.
- Outside the window at the a₀ radius: the framework's BLR-radius assignment
  fails for that system (§4, T5).
- Worked: A2744-QSO1-class, doorB r_B = 40.9 ld predicted vs ≈45 ld measured
  (×1.10, CONSISTENT-OPEN): J10-I = 1.818 ∈ [4/3, 2] (central), 1.719 (volume
  port) — the radius assignment survives under **either** geometry assumption
  (J11 V4). Sharp kill: R > (3/2)·r_B at q=0 ⇒ J10-I < 4/3; R > 2·r_B kills for
  every q (J10_verify C5).

---

## 2. The three geometry windows: a discrimination tree

The window is **geometry-specific**. The atom's mean chord anchors each
emission geometry (J11; quadrature ng=80 → exact):

| geometry | mean chord | window −lnA/d̄ | τ₀-dependence |
|---|---|---|---|
| **central** (point source at r=0) | 1.0000 | **[4/3, 2]**, q-shape (1+q/3)/(1/2+q/4) | **FLAT** (τ₀-free: 2.0000 at q=0 for any τ₀) |
| **volume** (uniform-in-ball emission) | **0.750000** exactly | **≈ [1.3, 1.9]** (τ₀=1: 1.8970/1.7104/1.3142 at q=0/3/10) | **CROSSING**: ≈ 2.2 at thin (τ₀→0) → 1.2 at deep; 2.049/1.894/1.629/1.423 at τ₀=0.5/1/2/3 (q=0) |
| **shell** (surface emission) | 4/3 ≈ 1.3333 (anchor exact) | **TO BE DETERMINED — K07 lane running** | TO BE DETERMINED |

The volume window **crosses the central window from above to below**
(J11): thin-τ₀ volume ≈ 2.2 > 2.0 (central q=0), deep/q-large volume
≈ 1.2–1.31 < 4/3 (central floor). A measured ratio below 4/3 kills the
*central-source* reading but is *expected* for volume emission — a central
violation is a geometry discriminator, not a Thomson kill (K01 F3 re-scope,
J11 §The finding).

### How an observer resolves the geometry (measurement tree)

**Node 0 — the τ₀-curvature (requires two epochs/opacities, or a population
spanning opacity).** Measure −lnA/d̄ at two opacities (two states of one source,
or two line regimes, or across a population with spread effective τ₀; τ₀ itself
is not dialed — it is inherited from the state):

- **central ⇒ FLAT**: ratio identical at all τ₀ (J10-I two-epoch ratio = 1.000
  exactly — τ₀, r_B, R all cancel);
- **volume ⇒ CROSSING**: −14% per factor-2 τ₀ at q=0 (1.894 → 1.629,
  τ₀ 1 → 2), −25% per factor-3 (→ 1.423), slope
  d(−lnA/d̄)/d ln τ₀ = −0.382 (q=0, measured J11; central = 0);
- **shell ⇒ TO BE DETERMINED** (K07; <chord> = 4/3 anchor already exact).

`circularity guard:` the curvature test needs only the *ratio* of measured
quantities; r_B, R, M_b, ρ_B cancel identically — it is the only branch of the
tree free of radius systematics (§3b).

**Node 1 — the q-shape (single epoch).** Invert (A, d̄) → (τ₀, q) under the
central assumption (K06-inv); then:
- predict the *third-observable family*: E[v²] (K04 E[N] map), E[Dv²], E[D²]
  via R_m(q); measured mismatch at ≥ 3σ ⇒ the central assumption is wrong
  (consistency-of-inversion branch);
- compare the measured point against the two window curves: central q-shape
  2.000/1.600/1.444 (q=0/3/10) vs volume-at-τ₀ levels (1.897/1.710/1.314 at
  τ₀=1). Single-epoch absolute separation is **not** a 3σ discriminator at
  JWST photometric grade (§3e, Δ = 5.5% between central-q0 and volume-q0 at
  τ₀=1); it is a population-level trend.

**Node 2 — the width channel (source-agnostic, any geometry).** T1/T2
(E[D²] bound, envelope) hold for central AND volume; they discriminate
geometry not at all but kill the scattering reading for either. The volume
*mean* clause requires the Q-correction: E[D]_vol = E[τ]_vol − E[Q] ≠ ∫rκ dr
(J02-B/J05-F3: 0.3376 vs 0.5008; E[Q] = 0.59715, bookkeeping exact to 7e-16;
wrong-by E[Q] + ½E[F(r₀)] − E[μ_exit] ≈ 0.163 at q=0).

---

## 3. The ERROR CHAIN: se(A)/A, se(d)/d, se(width) → the J10-I window test

**K09 (the dedicated JWST error budget) is NOT landed — no K09 file exists on
disk. Numbers below are K11's provisional budget, explicitly superseded by K09
when it lands.** Propagation: J10-I = −lnA·r_B/(c·d̄), r_B ∝ M_b^{1/2}·ρ_B^{−1/4}
(since a₀(ρ) = (c/2)√(Gρ)):

```
σ_ln J = √[ (σ_A/(A·|ln A|))² + (½·σ_M/M)² + (¼·σ_ρ/ρ)² + (σ_d/d)² ]
```

Provisional JWST-grade inputs (K09 pending): σ_A/A = 1% (atom spike photon
counting, N_spike ≳ 10⁴); σ_d/d = 3% (JAVELIN-class lag, monthly cadence,
2–3 yr); σ_M/M = 0.30 ln (virial M_b, no masers in LRDs); σ_ρ/ρ = 1.0 ln
(factor ~2.7 from line-ratio diagnostics).

| budget | σ_ln J | 3σ window reach |
|---|---|---|
| **absolute, full systematics** | **0.293** (29%) | window [4/3,2] = 0.405 ln = only **0.46 × 3σ** — no in-window 3σ rejection; kills only outside ≈ [1.0, 2.6] |
| r_B pinned to 15% (M 30%, ρ 40%) | 0.153 | still below 3σ (0.46 → 0.88×) |
| r_B pinned to 8% | 0.086 | **first 3σ reach** (1.6× window) |
| r_B pinned to 3% | 0.044 | 3σ reach (3.1× window) |
| **differential (2 epochs), r_B cancels** | **0.045** (4.5%) | volume τ₀ 2:1 curvature −14% = **+3.4σ vs central null**; τ₀ 3:1 −25% = **+6.4σ** |

Findings (the honest three):

1. **The absolute J10-I window test is systematics-dominated**, not
   photon-dominated: 98% of σ_ln J comes from (σ_M, σ_ρ) through r_B. Until
   M_b (dynamical/virial with calibrated scale) and ρ_B (multi-line
   diagnostics) are pinned to σ(r_B)/r_B ≲ 8%, J10-I absolute is a
   consistency indicator, not a 3σ falsifier.
2. **The differential τ₀-curvature test is the 3σ door**: r_B and R cancel
   exactly; central predicts ratio = 1.000 flat, volume predicts −14% per
   factor-2 opacity — separated at +3.4σ with the same JWST-grade photometric
   errors. K09 must therefore budget se(A)/A and se(d)/d at the few-% level
   per epoch; the geometric reach is already there (J11 numbers, 4σ+).
3. **Width channel (T1')**: the E[D²] bound kills only if the measured
   E[D²]/B₁ − 1 slacks below zero at 3σ; slack ≥ 1.06 means the joint moment
   SE must be < ~2% (E[D²] from the TF width, E[Dv²] joint, E[v⁴] from line
   kurtosis — the v⁴ tail is the weak link; realistic JWST-grade 3–8% ⇒ T1' is
   a 1–2σ tension indicator rather than a hard kill for most campaigns).

---

## 4. The falsifier battery — ONE numbered test list, strict kill conditions

Model conditions must be verified before any kill fires: stationarity,
conservatism (no absorption), isothermality within stated tolerance (K03
T-gradient provisos), source geometry (or B2/Q-correction), scatter profile
binary. "≥ 3σ" = statistical + astrophysical systematics accounted.

| # | test | measurable | prediction (verified precision) | **kill condition** |
|---|---|---|---|---|
| **T1** | J05/J06 width bound | E[D²], E[Dv²], E[v⁴] (TF width, joint lag–width moment, line kurtosis) | **E[D²] ≥ B₁ = 3E[Dv²]²/E[v⁴]**; B₁ tightest member of exact chain C_m = (4m−1)!!/((2m−1)!!)² (C₂ = 35/3); slack 1.25/1.13/1.06/1.07 (J05/J06, 86/86; source-agnostic, volume-verified) | E[D²] < B₁ at ≥ 3σ, conditions verified ⇒ **Thomson-scattering reading dead for ANY density, either source geometry** (C–S rigid; the only theorem-rigid member). Sub-kill: any member B₂, B₃ violated. |
| **T2** | J07 coherence envelope | |H(ω)| from lag autocorrelation, ω·E[D] < 1.5 (clips at ω* = 1.31 uniform) | **\|H(ω)\| ≥ max(0, 1 − ½ω²·L)**, L = 3E[Dv²]²/E[v⁴] (line-moment-only, no κ/n_e/geometry; 20/20, slope 3.99, at ω·E[D]=0.25 floor 0.9235 vs linear 0.7501) | measured |H| below floor at ≥ 3σ at any ω·E[D] < 1.5 ⇒ conservative Thomson reading dead (quantifiable before the run) |
| **T3** | J09-D window (central, q-family) | −lnA / d̄ from atom (F1) + lag (F2) | **(1+q/3)/(1/2+q/4) ∈ [4/3, 2]**, τ₀-free (27/27; K02 28/28) — equals the **invertibility domain** d/a ∈ [1/2, 3/4] of (A,d̄)→(τ₀,q) | ≥ 3σ outside [4/3, 2] ⇒ central **quadratic-family** reading dead for any opacity. NOT a "any-geometry" kill (K01 F3): general-p family limit (p+2)/(p+1), e.g. 6/5 (p=4), 4/3 (p=2), 3/2 (p=1) — J09p 21/21; outside the domain the inversion is undefined. |
| **T4** | J11 geometry discrimination (volume) | −lnA/d̄ vs τ₀ (2 epochs/opacities or population; or q-shape + inversion consistency) | volume window ≈ **[1.3, 1.9]**, τ₀-CROSSING: 2.049/1.894/1.629/1.423 (τ₀ 0.5–3, q=0), 1.897/1.710/**1.314** (q=0/3/10, τ₀=1, below 4/3); central FLAT at 2.0022; <chord>_vol = 0.750000 exact | volume curve not reproduced at ≥ 3σ ⇒ volume-emission reading dead; **single-window violation is a geometry discriminator, NOT a framework kill** — framework killed only by T5 failing in BOTH windows (J11 rule) |
| **T5** | J10-I a₀-radius reading | A, d̄_phys, M_b, ρ_B (independent) | **J10-I = (r_B/R)·window ∈ [4/3, 2]**, r_B = √(GM_b/a₀(ρ_B)), a₀(ρ_B) = (c/2)√(Gρ_B) (6/6 J10_verify; A2744-QSO1 1.818 central / 1.719 volume, CONSISTENT-OPEN) | ≥ 3σ outside [4/3, 2] with (M_b, ρ_B) measured independently ⇒ framework BLR-radius assignment fails for that system. Sharp form: R > (3/2)·r_B kills at q=0; **R > 2·r_B kills for every q**. With absolute budget §3, the 3σ regime requires σ(r_B)/r_B ≲ 8% or the differential port. |

T1/T2 also carry the registered sub-battery from K01 (rescaled): the fixed
closure ratios R_m = 2.64/3.57/4.56 are **q-conditional** (R₁ = 1.697 at
q=10) and must be stated as the *shape-dependent R₁(q) battery against the
inverted q* (F3/K06 F3), never as a universal fixed-number law (K01 F4).

---

## 5. The claim table (K01 classification)

| claim | class (K01) | status / verification file |
|---|---|---|
| **NOVEL — framework-core & new-observable (C)** | | |
| Window geometry discrimination: central [4/3, 2] τ₀-flat vs volume [1.3, 1.9] τ₀-crossing vs shell TBD | C (new-observable, no κ/n_e/geometry) | J09-J09P 27/27+21/21, J11 V3 (MC, n=4×10⁵), K02 28/28; not in STANDING, frozen lane, or posterior scattering-RM literature |
| τ₀-dependence of −lnA/d̄ under volume emission (2.049→1.423, q=0; 1.3142 < 4/3 at q=10) | C | J11 (V1/V2 quadrature×MC, V3) |
| ⟨chord⟩_vol = 0.750000 exactly (central 1.0, shell 4/3) | C (geometry enters non-trivially; volume atom averages birth-position/direction integral) | J11 quadrature ng=80 → 0.750000 |
| Radius reading J10-I: (A,d̄) → (τ₀,q) geometry-free (K06-inv closed, unique) then r_B = √(GM_b/a₀(ρ_B)) tested via (r_B/R)·window; opacity-elimination genuine (K01 GO) + one framework substitution | C (observable test of the core one-boundary statement, no dark-matter parameter) | J10 (6/6, J10_verify.py), doorB ×1.10 CONSISTENT-OPEN; K06 §4 |
| Density-free width bound E[D²] ≥ B₁ and line-moment envelope T3″ | C (K01 GO items; the cleanest density-free observables) | J05 (4 clouds, slack 1.25–1.06), J06 (86/86, B₁ tightest, slack = 1/ρ0² exact), J07 (20/20, slope 3.99) |
| **REAL CONTENT — joint-law register (B, K01 GO)** | | |
| Closure failure: R_m = 2.635/3.574/4.563 (m=1,2,3); R₁(q) = 2.6446/2.0235/1.6971 | B (joint-law measurement, not from kick-Gaussianity) | J01-C3 (±0.018/0.012/0.009), J02-C (n=10⁶) |
| Volume Dynkin compensation: E[D]_vol = E[τ]_vol − E[Q] ≠ ∫rκ dr; Q = 0.59715, exact to 7e-16; central-only domain of frozen Thm 1 | B (applicability-domain correction) | J02-B, J05-F3, K02 item 5 (0.597353, z=+0.35) |
| Deterministic closure: E[D] = 0.500000, E[v²] = 2.80674, E[Dv²] = 3.70900 (no RNG, half-range exact) | B (machinery verified; closes J04 obstruction) | K05 (V1–V4, ladder-converged) |
| **CONSISTENCY — label-only (A, K01: zero discovery weight, keep labeled)** | | |
| Gaussian spine: v\|traj ~ N(0, 2·ang); hierarchy E[Dv^{2m}] = (2m−1)!!2^m E[D·ang^m]; W = v²/2ang ~ χ²₁ independent of (D,ang) | A (engine draws Gaussian kicks — model input restated) | J01-C1/C2, J02-A, J09-A low-m (m=1,2: 0.997–0.995); 35/35 checks verify engines against themselves |
| Per-bin kurtosis ≥ 3, scale-mixture law (headline "= 3" REFUTED, fixed) | A | J09-B re-run: measured 3.35–4.33 vs mixture 3.36–4.27 (K01 F2) |
| Atom formula A = exp(−τ₀(1+q/3)) (definitional Poisson no-scatter) | A | J09-C (0.36826 vs 0.36788), K02 z ≤ 1.71 |

---

## 6. What this does NOT claim

1. **No fit to real LRD data.** No JWST observation is touched anywhere in the
   channel (N4, K06 honest edges); d̄_phys, (τ₀, q), J10-I are predictions
   with worked numbers at the frozen scale, not measurements of A2744-QSO1 or
   any other object (doorB's 40.9-vs-45 ld is a *radius prediction recorded as
   CONSISTENT-OPEN*, not a fit).
2. **No direct gravity statement beyond the radius.** J10-I tests the
   *a₀-radius assignment* r_B = √(GM_b/a₀(ρ_B)) at the BLR layer. It does not
   test the a₀-line dynamics g_obs² − g_bar² = a₀·g_bar, does not discriminate
   MOND alternatives inside the BLR, and says nothing about the gravitational
   law beyond the one boundary at the cloud. The framework core is touched
   exactly at r = √(GM/a₀(ρ)) and nowhere else.
3. **No novelty of the elementary steps.** cos x ≤ 1 − x²/2, Cauchy–Schwarz,
   and the Gaussian moment recursion are textbook; the content is the
   moment-chain substitution, the τ₀-cancellation, and the verification — as
   K01 and J07's honest edges already state.
4. **Shell window unmeasured** (K07 running; ⟨chord⟩ = 4/3 anchor exact) and
   **oblateness/geometry-aware reading unintegrated** (K08, K10 running).
5. **MC-grade limits stay MC-grade:** slack → 1 as q → ∞ is measured to 1.034
   at N̄ ≈ 10³, not proven; J09's m = 4, 5 tail ratios carry MC-tail risk.
6. **No git commit** (house rule for the push directory).

## Pending register — which numbers are NOT yet on disk

K07–K10 files **do not exist** in `deepseek_push/` (checked this run). Pending:

| lane | pending numbers | consequence for this synthesis |
|---|---|---|
| K07 | shell-emission window −lnA_s/d̄_s vs τ₀ (+ q-shape), <chord>_shell = 4/3 verification | the third leaf of the discrimination tree (§2) is "TO BE DETERMINED" |
| K08 | oblateness / geometry-aware corrections to (A, d̄, width) | all window numbers here are spherical-cloud numbers |
| K09 | JWST error budget: se(A)/A, se(d)/d, se(width) per instrument/campaign | §3 uses the provisional budget above (flagged); the 3σ reach numbers are superseded by K09 |
| K10 | geometry-aware J10-I integration (tree × radius reading) | T4/T5 remain separated until K10 |
| (parked) | J08 spine record — referenced by J09 (χ²₁ spine), no J08 files exist (K01 F, §J08) | W-independence theorem attributed to J08 stays unattributed-recorded |
| (parked) | K04 E[N](τ₀, q) for q > 0 (the E[v²] prediction branch) | q > 0 E[v²] predictions pending K04; q = 0 band closed |

## Traceability (every block → file)

§1 Table/1.1–1.3 → K06 §1–§5, J09/J09P `.out` (27/27, 21/21), J10 (6/6),
J10_verify.py, K02 (28/28), K05 (deterministic); §2 → J11 V1–V4, J09 tables,
J02-B/J05-F3; §3 → K11 computation (K09 pending, flagged); §4 → J05/J06
(86/86), J07 (20/20), J09/J09P, J11, J10 kill rules; §5 → K01 audit verdict +
the cited J/K files; §6 → K06 honest edges, K01 findings.

**Status: K11 LANDED (synthesis) — 5 consolidated falsifiers, geometry tree
with one pending leaf (K07), error chain computed on a provisional budget
(K09 pending), NOVEL/CONSISTENCY ledger per K01, no new numbers invented.**