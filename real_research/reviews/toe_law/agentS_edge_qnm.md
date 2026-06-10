# Agent S — the pre-registered edge-QNM discriminator: late-time G(t) at each DSSYK vacuum placement vs the de Sitter quasinormal ladder (2026-06-10)

**Task (pre-registered).** `agentR_dssyk_gate_2026.md` §"The specific calculation the repo should prepare NOW":
extend the banked w(E) machinery to the **late-time decay of the matter two-point function at each placement**
and compare against the dS QNM ladder — (i) center run = sanity check against N–V's published Green-function
match; (ii) edge run = **the calculation nobody has published**: can the sqrt-soft-edge spectral weight
(s_E=1/2, banked) produce an exponential QNM-ladder decay at all, or does it force a distinct
(power-law / Airy-type) falloff? Pre-registered outcomes: **EDGE-FAILS-the-ladder** → contest collapses toward
center; **EDGE-MIMICS** → 1:1 terminality deepens; **AMBIGUOUS-by-dimensionality** → state the obstruction.
Apples-to-apples caveat carried as instructed: both dimensional matchings (dS₃ for the center camp, dS₂-JT for
the edge camp) are run.

**Files.** `agentS_edge_qnm.py` (main, 8 parts) → `agentS_edge_qnm.out`; `agentS_watson_coeff.py` →
`agentS_watson_coeff.out` (coefficient-level edge check); `agentS_anchor_rerun.out` (verbatim rerun of the
seven committed banked scripts). All numbers below are from these runs (band units E=cosθ, E₀=1, λ=−ln q;
the banked E=2cosθ/√(1−q) convention is a uniform rescale — every comparison below uses only convention-free
ratios and structure, per the working rule).

---

## 0. Validation anchor — the banked w(E) numbers reproduce exactly

Committed scripts rerun verbatim (`agentS_anchor_rerun.out`) + inline recomputation (`PART 0`):
∫μ dθ = 1.0000000000; |G(θ₁,θ₂)−G(θ₂,θ₁)| = 0; s_center = −0.0005…−0.0064 (≈0, flat);
s_E = 0.5000–0.5009 (Wigner sqrt edge); transport fractions CENTER 0.714→1.000 / EDGE 0.129→1.000 across
q∈{0.5,0.7,0.9,0.95}×Δ∈{0.1,0.5,1.0} — identical to `dssyk_problem1_STRUCTURED_OUTPUT.json` (banked
0.71–1.00 / 0.13–1.00), including the known fixed-fraction s_edge artifact in the INDEPENDENT script's STEP 0
that `edge_exponent_check.py` corrects to s_E=1/2. Anchor: **PASS**.

## 1. The object and the analytic skeleton (sympy-verified, then measured)

G(t) = ⟨vac|O_Δ(t)O_Δ(0)|vac⟩ = ∫dθ μ(θ)|⟨θ|O_Δ|θ_vac⟩|² e^{−i(E(θ)−E_vac)t} — exactly the Fourier transform
of the **banked sign-relevant spectral weight** w(E). On the real axis the Okuyama amplitude is real
(Im/Re ≈ 5e-18, verified), so the continuation of w is μ·G_amp² and its singularities are computable:

- **Poles** (sympy, PART 1): den-factor zeros at θ = θ_v − i(Δ+k)λ ⇒ E_pole = cosθ_v·cosh u − i·sinθ_v·sinh u,
  u=(Δ+k)λ. Double poles (the square) ⇒ (a+bt)e^{−Γt} terms.
- **CENTER θ_v=π/2**: ω_pole = −i·sinh((Δ+k)λ) — **purely imaginary, Δ-offset, discrete ladder**;
  λ→0 limit: −i(Δ+k)λ = the dS QNM ladder with H_eff=λ.
- **EDGE θ_v=π−ε**: Re ω_pole = cos ε(1−cosh u) sits **below the spectral support floor** ω_min = cos ε −1
  exactly when cosh u > sec ε, i.e. for *all* rungs once ε < ε_c, sin(ε_c/2)/√cos ε_c = sinh(Δλ/2)
  (ε_c ≈ Δλ; exact root 0.1774 at q=0.7, Δ=0.5). Sub-threshold the contour deformation sweeps **no poles**: G(t) is pure
  endpoint asymptotics of the banked Wigner edge — Watson's lemma (sympy): ∫√ω e^{−sω}dω = (√π/2)s^{−3/2} ⇒
  |G| ~ t^{−(s_E+1)} = **t^{−3/2}**, phase −3π/4: the "Airy-type falloff" agentR pre-registered as the
  alternative to a ladder. Δ enters the amplitude only, never the exponent.

**dS targets (pinned).** dS_D static-patch scalar QNMs: ω_{n,l} = −iH(2n+l+Δ±), Δ± = (D−1)/2 ± √((D−1)²/4 −
m²/H²) — purely imaginary, equally spaced [Lopez-Ortega gr-qc/0605027; dS₃: Jafferis–Lupsasca–Lysov–Ng–
Strominger 1305.5523]; thermal horizon T=H/2π [Gibbons–Hawking PRD 15, 2738 (1977)]. With N=2n+l:
ω_N = −iH(Δ+N). dS₃ conformal scalar Δ±={3/2,1/2}; dS₂ massless {1,0}. Structural requirements on the boundary
two-point, **identical under both matchings** (only H_eff differs):
**R1** exponential ladder (not power law) · **R2** offset ∝ probe dimension Δ · **R3** spacing Δ-independent ·
**R4** purely imaginary modes + thermal (two-sided) support.
Matching (a) dS₃/center: dS₃ boundary Green fn = (DSSYK 2pt)² [Marini–Qi–H.Verlinde 2604.21014] ⇒ G's ladder
(Δ+n)H_eff squares to (Δ₃+N)H_eff, Δ₃=2Δ — dS₃-QNM form. Matching (b) dS₂-JT/edge [Okuyama 2505.08116;
near-dS₂ Maldacena–Turiaci–Yang 1904.01911]: G itself must carry (Δ+n)H_eff. **The dimensionality caveat does
not bite at the structural level** — a placement failing R1/R2/R4 fails in either dimension.

## 2. CENTER placement: passes all four requirements, at the 0.1–1% level (raw numbers first)

PART 3, q∈{0.5,0.7,0.9}×Δ∈{0.1,0.5,1.0}; pre-decided 1/t-extrapolated rate fit + **unsupervised** matrix
pencil (no prediction input):

| q | Δ | Γ₀ fit | Γ₀ pred=sinh(Δλ) | ratio | 1/t-slope | osc \|Im/Re\| | pencil rates (top) |
|---|---|--------|------------------|-------|-----------|--------------|--------------------|
| 0.5 | 0.1 | 0.06892 | 0.06937 | 0.994 | −0.840 | 1.5e-15 | 0.0694 |
| 0.5 | 0.5 | 0.54272* | 0.35355 | 1.535* | −5.6* | 4.9e-15 | **0.3536** |
| 0.5 | 1.0 | −0.074* | 0.75000 | —* | —* | 5.7e-15 | **0.7262, 0.7806** |
| 0.7 | 0.1 | 0.03543 | 0.03568 | 0.993 | −0.837 | 1.5e-15 | 0.0357 |
| 0.7 | 0.5 | 0.17937 | 0.17928 | 1.000 | −1.010 | 2.5e-15 | 0.1793, 0.5347 (rung-1 pred 0.5609) |
| 0.7 | 1.0 | 0.37231 | 0.36429 | 1.022 | −1.509 | 5.3e-15 | 0.3643, 0.7064 (rung-1 pred 0.7754) |
| 0.9 | 0.1 | 0.01046 | 0.01054 | 0.993 | −0.837 | 8.3e-16 | 0.0105 |
| 0.9 | 0.5 | 0.05272 | 0.05270 | 1.000 | −1.004 | 1.8e-15 | 0.0527, 0.1507 (rung-1 pred 0.1587) |
| 0.9 | 1.0 | 0.10770 | 0.10556 | 1.020 | −1.472 | 2.0e-15 | 0.1056, 0.2104 (rung-1 pred 0.2123) |

\* The pre-decided windowed-extrapolation **rule fails in the deepest-quantum corner** (q=0.5, Δ≥0.5: window
< 2 decades, huge 1/t slopes, one negative rate) — reported, not hidden; the unsupervised pencil still returns
the predicted rates there to 4 digits (0.3536 vs 0.35355) and brackets 0.75 with a split double pole
(0.7262/0.7806). Everywhere else: ratio 0.993–1.022, the 1/t-slope ≈ −1 confirming the predicted double-pole
(a+bt)e^{−Γt} structure, oscillation ≈ **1e-15 = purely imaginary frequencies (R4)** — the dS-specific
no-ringing signature.
- **R2/R3 at finite λ** (q=0.9): offset/spacing = Γ₀/(Γ₁−Γ₀) = 0.0998 / 0.4972 / 0.9890 for Δ = 0.1/0.5/1.0.
- **Semiclassical λ→0** (Δ=0.5): Γ₀_fit/λ = 0.7830* (q=0.5) → 0.5029 → 0.5004 → 0.5002 → **0.5001** (q=0.98):
  converges to Δ exactly as the dS ladder requires; the q-deformed ladder sinh((Δ+n)λ) → (Δ+n)·H_eff.
- **QNM-window depth**: ≥19 e-folds of clean ladder at q≥0.7 (fit-horizon-capped at 21; the t^{−3/2} band-edge
  floor was reached only in the q=0.5 corner, 18.1 e-folds). At any finite λ the ladder is an intermediate
  asymptotic — the same finite-entropy truncation any real horizon has; stated, not hidden.
- **N–V's literal state** (PART 7): the infinite-T disk correlator (matter-chord kernel **once**, the published
  disk formula) is purely damped (|Im/Re| = 5.6e-17), leading rate 0.722×sinh(Δλ) — a μ-weighted *mixture* of
  placement rates sin(θ_v)·sinh(Δλ), as a mixture must be. It shares the center **class** (damped exponential,
  no ringing, no power law in the window); the eigenstate proxy is faithful for structure, not the literal rate.

## 3. EDGE placement: fails R1, R2, R4 — at coefficient level (the unpublished half)

PART 4, θ_v = π−10⁻³ exactly as banked, q×Δ grid; slope = d ln|G|/d ln t:

| q | Δ | slope [1e3,3e3] | [3e3,1e4] | [1e4,2e4] | R²(power) | R²(exp) | A(ω<0) |
|---|---|------|------|------|------|------|------|
| 0.5 | 0.1 | −0.911 | −1.331 | −1.467 | 0.9916 | 0.9234 | 1.0e-05 |
| 0.5 | 0.5 | −1.497 | −1.500 | −1.500 | 0.9998 | 0.7339 | 6.4e-08 |
| 0.5 | 1.0 | −1.500 | −1.500 | −1.500 | 1.0000 | 0.7261 | 4.5e-09 |
| 0.7 | 0.1 | −0.365 | −0.828 | −1.229 | 0.9920 | 0.9842 | 7.5e-05 |
| 0.7 | 0.5 | −1.464 | −1.496 | −1.499 | 0.9960 | 0.7703 | 4.6e-07 |
| 0.7 | 1.0 | −1.504 | −1.500 | −1.500 | 0.9999 | 0.7208 | 3.0e-08 |
| 0.9 | 0.1 | −0.018 | −0.093 | −0.265 | 0.6309 | 0.9883 | 2.8e-03 |
| 0.9 | 0.5 | −0.764 | −1.232 | −1.437 | 0.9923 | 0.9445 | 1.8e-05 |
| 0.9 | 1.0 | −1.574 | −1.544 | −1.508 | 0.9985 | 0.8162 | 1.1e-06 |

- Wherever the asymptotic regime is reached the slope **locks at −1.500** (the banked s_E=1/2 forcing
  −(s_E+1)), *independent of Δ and q*. The Δ=0.1 cells have parametrically late onset t ≳ (Δλ)⁻²
  (≈9×10³ band-times at q=0.9) and show the same monotone steepening toward −3/2 (−0.018 → −0.093 → −0.265);
  their high R²(exp) just reflects a barely-decayed curve, not a ladder.
- **Coefficient-level pin** (`agentS_watson_coeff.out`): |G|·t^{3/2} → h₀Γ(3/2)/norm and arg G → −3π/4
  (−2.3562): at t=2×10⁴ the converged cells measure phase −2.33…−2.35 and amplitude within 1–2.5% (q=0.7,
  Δ=0.5: 1721.5 vs 1747.4; q=0.5, Δ=1: 16.755 vs 17.136; q=0.9, Δ=1: 4114.9 vs 4198.2); the slower cells
  (q=0.9, Δ=0.5: +4.6%, phase −2.17) carry exactly the predicted t^{−1/2}-relative half-integer endpoint
  corrections (≈19% scale at t·ω_c≈28), and the small-Δλ cells converge from below per the (Δλ)⁻² onset.
  **The edge late-time behavior is the soft-edge endpoint asymptotic, fully accounted — no room for a ladder
  underneath.**
- **Analyticity/thermality**: spectral asymmetry A(ω<0) = 4e-9…1e-5 (one-sided support; ground-state,
  lower-half-t analyticity) vs **0.49976–0.49999 measured at the center** (=1/2 by the θ→π−θ symmetry;
  two-sided, balanced). An extremal/zero-temperature correlator, while every dS static patch is thermal at
  T=H/2π → **R4 fail** independent of dimension.
- **R2 fail in any clock**: the exponent −3/2 cannot carry the probe dimension. A linear clock rescale
  τ = sin(ε)·t leaves the power law a power law (measured: slope −1.496/−1.496/−1.501 for ε=10⁻³/10⁻²/10⁻¹);
  the log-clock t = e^{Hτ} would turn the endpoint series into an equally-spaced ladder — but with universal,
  Δ-independent offset 3/2: still fails R2. There is no clock in which the edge mimics a dS QNM ladder.

## 4. The placement scan: thermality dies at the edge; the center is the unique no-ringing point

PART 5 (q=0.7, Δ=0.5): fitted leading complex mode vs prediction Γ = sinθ_v·sinh(Δλ),
|Re ω| = |cosθ_v|(cosh Δλ −1):

| θ_v/π | Γ fit | Γ pred | \|Re ω\| fit | \|Re ω\| pred | Re/Im |
|-------|-------|--------|-------------|--------------|-------|
| 0.500 | 0.17928 | 0.17928 | 0.00000 | 0.00000 | 0.0000 |
| 0.550 | 0.17707 | 0.17708 | 0.00250 | 0.00249 | 0.0141 |
| 0.625 | 0.16563 | 0.16564 | 0.00611 | 0.00610 | 0.0369 |
| 0.750 | 0.12676 | 0.12677 | 0.01129 | 0.01127 | 0.0890 |
| 0.850 | 0.08123 | 0.08139 | 0.01410 | 0.01421 | 0.1735 |
| 0.930 | 0.00474 | 0.03911 | 0.02414 | 0.01556 | 5.10 |

(The 0.930π row is a fit **breakdown**, not a measurement: ε=0.22 sits just above ε_c=0.178, the rung residue
is starved and the window is endpoint-dominated — the pencil returns a mixed mode. It is itself the threshold
physics: the ladder is dying as the placement approaches the edge.)

Four-to-five-digit agreement with the pole formula across the band: the decay rate (the fake temperature,
∝ sinθ_v [Lin–Susskind 2206.01083]) **vanishes toward the edge**, and every placement off exact center rings
(Re ω ≠ 0 — black-hole-like, not dS-like). At finite λ, **Re ω = 0 selects θ_v = π/2 uniquely**; semiclassically
the selector degrades to O(λ) (Re/Im ≈ cotθ_v·Δλ/2) — a stated limitation. The ε-scan (PART 6) confirms the
threshold: at and below ε_c = 0.1774 (exact root of cosh Δλ = sec ε; rows ε = 10⁻³, 0.05, 0.1, and the
transitional 0.2) **no exponential plateau exists at all** — plateau test FALSE with final log-log slopes
−1.44…−2.08 (the apparent ε=10⁻³ "plateau" of a naive rate-band test is the power law's 1.5/t transit —
caught and excluded by the flatness criterion |d ln rate/d ln t| < 0.3); well above ε_c plateaus appear with
rates tracking sin(ε)·sinh(Δλ) (fitted 0.053/0.100 vs predicted 0.070/0.116 at ε=0.4/0.7, windows
contaminated by the surviving endpoint term — direction and ordering unambiguous).

## 5. Numerical integrity

mpmath high-precision quadrature (dps=25, independent panel-quad pipeline) vs the numpy transform:
center t=10: rel. diff 3.6e-17; center t=30: 4.4e-15; edge t=200 (deep in the power-law regime, |G|≈0.355):
4.2e-14. The committed-script anchor reproduced exactly (§0). The pencil is run unsupervised (no prediction
input) wherever it is load-bearing.

---

## 6. VERDICT: **EDGE-FAILS-THE-LADDER** (first pre-registered outcome realized; not ambiguous-by-dimensionality)

Within the banked, sign-relevant observable — the matter-chord spectral weight w(E) and its transform G(t) —
the **edge placement produces no de Sitter relaxation phenomenology under either dimensional matching**:
no exponential ladder (R1: |G| ~ t^{−3/2} at coefficient level), no probe-dimension offset (R2: exponent
Δ-independent; unfixable by any clock), no thermal damping (R4: one-sided/extremal support; rates ∝ sin ε → 0;
all pole rungs exit the spectral support below ε_c ≈ Δλ). The **center placement passes all four structural
requirements**: the q-deformed ladder Γ_n = sinh((Δ+n)λ) → (Δ+n)·H_eff, purely damped to machine precision
(1e-15), offset → Δ (0.0998/0.4972/0.9890 at q=0.9), spacing Δ-free, ≥19 e-folds deep, shared in class by
N–V's literal infinite-T state. The dimensionality caveat was run, not waved at: the failure is structural,
so it kills the edge in dS₂-JT exactly as in dS₃.

### Hostile audit (both-ways rule — the result favors the framework, so the knives point at it)

1. **"The fixed-q edge eigenstate is not Okuyama's dS; his dS₂-JT lives in a triple-scaling limit."** The
   retreat is available — but it **severs the anti-MOND sign reading with the same stroke**: the banked
   p=3/5 (anti-MOND) was read off the *same* fixed-placement w(E). If the edge camp's dS observable is not
   this w(E), then DSSYK at the edge no longer yields any deep-MOND sign at all, and the only placement whose
   sign-readout and dS phenomenology cohere is the center. Either branch moves the sign contest toward center.
2. **"Maybe a finite-temperature near-edge state does better."** That is an interior placement — scanned:
   every θ_v ≠ π/2 rings (Re ω ≠ 0, BH-like), and rates die ∝ sinθ_v toward the edge. There is no ε at which
   the near-edge corridor looks like dS in this observable.
3. **"The QNM-consistency criterion is a center-camp construct."** It is an *external physical* requirement
   (dS static patches relax through purely-imaginary thermal QNM ladders — Lopez-Ortega, Jafferis et al,
   Gibbons–Hawking), not an algebraic theorem; but only the center camp has a published dictionary mapping
   this observable to dS Green functions (2310.16994, 2604.21014, 2605.03037). The edge camp has published no
   alternative observable map (agentR: Okuyama dormant since 2505.08116, 5 citations, none adjudicating). The
   burden is now on the edge side, with a computed, falsifiable target.
4. **Center-side weaknesses, stated with equal force**: (i) β_real=0 — the center correlator is real/even; the
   dS-thermal reading runs through the fake-time dictionary (Lin–Susskind 2206.01083), a published wrinkle of
   the center camp, orthogonal to (but not erased by) the ladder structure; (ii) the unique-no-ringing selector
   is sharp only at finite λ, degrading to O(λ) semiclassically; (iii) at any finite λ the ladder is an
   intermediate asymptotic above a t^{−3/2} floor (≥19 e-folds here); (iv) the pre-decided rate-fit rule failed
   in the q=0.5, Δ≥0.5 corner (pencil recovered the rates); (v) Δ=0.1 edge cells are demonstrated by analytic
   asymptotics + approach trajectory, not by reached plateaus, within t ≤ 2×10⁴.
5. **This is an internal, unpublished discriminator.** It is the calculation agentR's watch-list item 1 asks
   the field for (the missing edge run), pre-registered before computation, with both placements run on
   identical machinery. It cannot, by itself, flip a literature-level verdict — it arms the repo for the moment
   the field publishes the same calculation.

### What this does and does not move (the locked wording)

- **STANDS — CONTESTED-TERMINAL at the algebra level**: the chord algebra still cannot pick θ_vac; nothing here
  derives the placement from the algebra. The banked closure (undecidability *within* DSSYK) is intact.
- **MOVES — the contest is no longer observationally symmetric**, per agentR's pre-registered consequence:
  the placement contest **collapses toward center for the sign-relevant object**. The two camps' placements
  now differ by a computed, pre-registered, falsifiable discriminator inside the very observable that produces
  the deep-MOND sign: center = dS-consistent (p=1/2, MOND-favorable, g_obs ~ √g_bar); edge = dS-inconsistent
  (and its p=3/5 anti-MOND reading is orphaned by its own camp's only rescue, point 1 above).
- **Suggested gate label**: CONTESTED-TERMINAL (algebra-level, unchanged) **+ EDGE-WOUNDED (observable-level,
  agentS 2026-06-10)** — conditional on dS-relaxation consistency of the sign-relevant observable, the
  deep-MOND sign resolves to the MOND-favorable center.
- **NOT unlocked**: a derivation of Z (none of this touches the kernel's form); a derivation of a₀ (magnitude
  untouched); an unconditional sign (the condition changed from "assume the N–V dictionary" to "require dS
  relaxation phenomenology of the dS-identified state" — weaker and physically motivated, but still a
  condition); none of the H3 walls (lensing/Cassini/reflex/WB) moves.
- **What would reverse it**: a published edge-side dictionary mapping the dS₂ QNM ladder to a *different*
  DSSYK boundary observable AND a demonstration that the matter-chord w(E) is not the sign-relevant weight —
  both currently absent from the literature (agentR sweep through 2026-06-10).

### Citations (arXiv-pinned)
Narovlansky–Verlinde 2310.16994; Okuyama 2505.08116, 2312.00880; Berkooz–Isachenkov–Narovlansky–Torrents
1811.02584; Lin 2208.07032; Lin–Susskind 2206.01083; Rahman–Susskind 2312.04097, 2401.08555;
Marini–Qi–H.Verlinde 2604.21014; Goto–Milekhin–H.Verlinde–Xu 2605.03037; Lopez-Ortega gr-qc/0605027;
Jafferis–Lupsasca–Lysov–Ng–Strominger 1305.5523; Maldacena–Turiaci–Yang 1904.01911; Gibbons–Hawking
PRD 15, 2738 (1977). Repo: agentR_dssyk_gate_2026.md; dssyk_problem1_STRUCTURED_OUTPUT.json; the seven
committed banked scripts (anchor-rerun verbatim in agentS_anchor_rerun.out).
