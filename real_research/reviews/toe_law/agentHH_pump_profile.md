# agentHH — The Link 5 calculation: minimal scale-invariant pumped-khronon dynamics vs (C1)-(C5)

**STATUS: IN PROGRESS (3rd launch) — STEPs 0-2 banked; v2 validated (free 2.8e-16, contour-inv 8.9e-11); [3a] powers + [3b] envelope-kill + [3e] all-orders anchors BANKED; the read law measured: Δρ_c = −ν[(3/2)F + ½sF′] (3 exact anchors); keystone [3d] + kernel [3a1] + bands [3c] + hostility probes in flight.**

Date: 2026-06-11. Charter: construct the minimal scale-invariant pumped-khronon DYNAMICS and test
whether ANY admissible gain/dispersion profile g(k_phys/H) lands in agentEE's matching conditions
(C1)-(C5). Framework-favorable territory — maximum hostility; every claimed PASS independently
recomputed within the run.

## Target (from agentEE STEP 4)

The required worldline commutator-density addition:

> Delta-rho_c(omega) ~ A omega^(-1/3) e^(-ct omega^(1/3)) cos(sqrt3 ct omega^(1/3) + phi),
> one-sided, ct = (3/4) 2^(2/3) zeta-tilde^(2/3) = 2.139 (fw) / 1.969 (canon) / 2.279 (hostile),
> omega in units of H; decay/oscillation LOCKED at 1/sqrt3; prefactor power -1/3;
> |A| <= A_max ≈ 5.7; pump must be scale-invariant (g a function of k_phys/H only) and must
> MODIFY THE DYNAMICS (Bogoliubov lemma: state-shaping is invisible to the response).

Constraints inherited: the b-family theorem (dilatation orbits = Deser-Levin family, kappa^2 = a^2+H^2);
the free pullback W_b = -H^2/[16 pi^2 c_chi (c_chi^2-b^2) sinh^2(kappa tau/2)]; X2 invoice
1e33-1e35 W per L*-galaxy; agentU PPN/Cherenkov corner (c_chi^2 = O(gamma/alpha) >> 1, c_chi > 1 required).

Coefficient discipline ABSOLUTE: raw numbers on both footings; (16pi/3)^(1/4) quarantined; NO Z claims.

## Plan

- **STEP 0** — Reuse/verify agentEE's per-k kernel machinery (regression gate before any new claim).
- **STEP 1** — Parametrize the pump: scale-invariant modification of the khronon mode equation
  (gain/anti-damping gamma(k_phys/H) and/or dispersion correction delta(k_phys/H)); write the
  modified mode equation in conformal time; identify the forced functional form.
- **STEP 2** — Worldline cut-density correction Delta-rho_c(omega) on the Deser-Levin family from the
  modified modes (two-variable representation; per-k kernel; Mellin/Bochner route).
- **STEP 3** — FORWARD match: scan admissible g-classes against the omega^(-1/3) exp-oscillatory
  fingerprint. INVERSE problem: invert the required fingerprint to the implied g; admissibility check.
- **STEP 4** — Gates on any survivor: stability (no runaway outside the pumped band), causality/
  Cherenkov (agentU corner), PPN feedback, X2 energy budget (compute the integrated throughput;
  compare 1e33-1e35 W).
- **STEP 5** — Coefficient discipline: raw amplitude normalization both footings; quarantine list.
- **VERDICT** — PROFILE-FOUND / CLASS-OBSTRUCTED / PARTIAL.

## STEP 0 — Regression gate: PASS (agentEE machinery reproduced exactly)

All six gates pass (`agentHH_pump_profile.py step0`, mpmath dps 30-40):

- **[0a]** Mellin of the free mode, rotated-contour numeric vs Γ(1−iν)(−ic)^{iν−1}: worst rel.diff
  3.5e-16 over ν ∈ {0.5, 2, −1.3}.
- **[0b]** Planck identity |Γ(1−iν)|²e^{πν} = 2πν/(1−e^{−2πν}): symbolically exact 0.
- **[0c]** FT of −sinh⁻²(κ(τ−iε)/2) vs the residue formula: worst 9.1e-20.
- **[0d]** the [3c] contour machinery D(ω) vs direct quadrature: worst 3.0e-18 at ω = 3, 12.
- **[0e]** saddle-class fit over ω ∈ [1e2, 3e4]: c̃_fit = 2.140537 vs pred 2.138750, **ratio 1.00084**
  (agentEE banked 1.00084); q_fit = −0.3202 vs −1/3. Fingerprint constants reproduced:
  c̃ = 2.1388 (fw) / 1.9687 (canon) / 2.2790 (hostile).
- **[0f]** positivity window on the same grid: **A_max = 5.716**, binding at ω = 0.500 (agentEE banked
  5.716 at ω ≈ 0.5κ).

Machinery banked; reuse authorized.

## STEP 1 — Pump parametrization: scale invariance forces ONE universal ODE; the response is normalization-free; the worldline density is Mellin-bilinear

All machine checks exact (sympy residuals = 0; mpmath identities to 1e-31):

**[1a] The forced functional form.** Work with the Minkowski-form khronon variable g (field mode
f_k = (H/√(2ck³))·w·g(w), free g = e^{icw}, w = k|η| = k_phys/H — the 1206.1083 structure). The most
general LINEAR, LOCAL-in-time, scale-invariant pump (gain Γ_conf = k·ĝ(−kη), dispersion f(−kη))
reduces — sympy-exactly — to ONE k-independent universal ODE:

> **g'' − 2ĝ(w)g' + c²(1 + f(w))g = 0**, w = k_phys/H; ĝ > 0 = physical-time gain
> (w runs backward in time). Physical gain rate per Hubble time = w·ĝ(w): **H-paced automatically —
> (C5)'s "the only scale available IS the dS bath's" is built in, not imposed.**

**[1b] Friction elimination + normalization-freeness of the response.** g = e^{Ĝ}ψ (Ĝ' = ĝ) maps to
Hermitian form ψ'' + Ω²ψ = 0, Ω² = c²(1+f) + ĝ' − ĝ² (exact). The object the worldline soft channel
reads is the CAUCHY PROPAGATOR (commutator/response) of the universal ODE: machine-verified
GL(2)-basis-invariant and Wronskian-normalization-free — the Bogoliubov lemma's "σ is a DYNAMICS
object" made explicit (no vacuum choice can enter). Gain enters the response ONLY through (i) the
relative factor e^{Ĝ(w₁)−Ĝ(w₂)} and (ii) Ω² inside ψ. WLOG the scan space = {Ĝ-factor} × {Hermitian
Ω² family}.

**[1c] The worldline Mellin-bilinear formula.** At b = 0 (κ = H), the pullback of the per-k commutator
with the dk/k measure Mellin-diagonalizes:

> **ρ_c(ν) = −2ic[φ̃_a(ν)ψ̃_b(−ν) − φ̃_b(ν)ψ̃_a(−ν)]**, φ_i = w·g_i, ψ_i = w·g_i/W(w)
> (W = running Wronskian), basis-invariant.

Checks: Plancherel pairing vs closed form in the KMS strip (τ = 0.7 − 0.5i): rel.diff 3.4e-31; free
case reduces to ρ_c(ν) = 2πν/c² EXACTLY (0 to 3e-31 over ν = 0.4/1.0/3.7) — agentEE [2d]'s
Planck-odd-part recovered through the bilinear. **Scan convention: normalize by 2π/c² so free
ρ_c(ν) = ν; then (C1)'s tail and (C3)'s A_max = 5.716 compare in agentEE [3d] units directly.**

**[1d] Classes registered for the forward scan** (before computing, so the scan can't be steered):
P power-law tails ĝ/f = κw^{−p}, p ∈ (0,2] (p = 2/3 the WKB index-transfer candidate; p = 2 Bessel
and p = 1 Coulomb/Whittaker exactly solvable anchors); B gain bands (smooth compact bump; sharp-edged
variant); L log-periodic ε·cos(Ω ln w) × envelope; D modified dispersion ω² = c²k²(1+f), f real (the
X2-named form); X windowed filter bank (= B/L composite in ln w); G Gevrey-3/stable class (profiles
with Mellin g̃(μ) ~ e^{−A|μ|^{1/3}} — the index-1/3 stable-subordinator kernel in ln w, the
inverse-problem candidate). For each: Δρ_c(ν), fit ln|tail| = lnK + q lnν − c̃ν^s with s FREE, test
s = 1/3, the cos(√3c̃ν^{1/3}) lock, additivity, one-sidedness.

## STEP 2 — The exact per-k → worldline pipeline: built and validated to 1e-35

Machinery (`solve_branch` + `mellin_phia` + `rho_c_pipeline`): the upper-half-plane-decaying
solution g_a of the universal ODE is tracked by a **Riccati solve down the imaginary ray**
(attracting direction for the decaying branch — necessary: mpmath's own `hankel1` LOSES this branch
at large imaginary argument, returning 1.8e+8 where the true value is ~1e-74; recorded), continued
through a quarter-arc and a real segment; the Mellin φ̃_a(±ν) is assembled over the deformed contour
[0,w_cut] (closed-form incomplete-Γ endpoint; scan profiles vanish identically below w_cut) +
real segment + arc + ray, paying the e^{+νπ/2} cancellation with dps ≈ 0.683ν + 40; ρ_c(ν) from the
[1c] bilinear with the numerically computed Wronskian.

- **[2a] Free end-to-end:** ρ_c(ν) = ν through the FULL machinery to rel.err 2.7e-60 (ν=2) …
  1.0e-44 (ν=33). The cancellation, quadrature, branch handling, and bilinear are all exact.
- **[2b] Bessel anchor** (F = μ/w², μ = 0.4, c = 2, imaginary order λ = 1.1619i): the ODE branch is
  proportional to √w·H¹_λ(cw) across ray and real segment to 2.1e-45 — the solver tracks the exact
  upper-decaying special-function branch.
- **[2c] Closed-form cross-check:** pipeline Mellin vs the exact Γ-function Mellin
  (M_J(s,μ) = 2^{s−1}Γ((μ+s)/2)/Γ(1+(μ−s)/2), H¹_λ assembled from J_{±λ}, s = 3/2 − iν; J-series
  endpoint): agreement 3.8e-46…4.9e-35 at ν = ±6, ±15. ρ_c^Bessel(6) = 5.86302 (dev −0.137),
  ρ_c^Bessel(15) = 14.94645 (dev −0.0535): deviation ~ 1/ν **power-law class** — the p = 2 column
  of the transfer table is exact: no exponential of any index (Γ-ratio asymptotics).

One bug caught and fixed during validation (real-segment contour direction sign — caught by the
free gate at 0.6 rel.err, fixed, gate then passed at 1e-44; bug log below).

## STEP 3 — The match (forward + inverse)

### [3a0] The fast pipeline (v2) finished and validated — the third-launch repair

The prior session's v2 rewrite (real-axis saddle route: Riccati contraction on the ray at s_a,
arc transport down, real axis both ways, rotated decaying tail; NO e^{νπ/2} cancellation tax —
flat dps ≈ 40-50 for any ν; the e^{−2πν}-negligible −ν Mellin dropped above ν = 8) had its
inward-segment assembly rewritten in **direct w-parametrization** (log-spaced panels in w with
explicit jacobians, the solve's x-parametrization queried pointwise — orientation unambiguous).
Validation this session:

- **free gate at scan settings:** ρ_c(ν) = ν to 5.8e-19 (ν=4) / 2.8e-16 (ν=36);
- **contour-parameter invariance** on the p = 2/3 template (s_a 6→9, w_cut 0.01→0.003, deg
  24→32, θ_rot π/6→π/4 — an analytic contour integral must not move): shift ≤ 8.9e-11,
  systematics 8+ orders below scan signals;
- **v1-vs-v2 cross-validation** ([3a0b]): the STEP-2-validated complex-contour pipeline (exact
  to 1e-35 vs Γ closed forms) re-run on the SAME nontrivial template — **agreement 8.0e-19
  (dispersion ν=6), 4.6e-18 (ν=15), 1.1e-17 (the weighted-GAIN bilinear, ν=6)**: fourteen-plus
  shared digits across different contours, different dps regimes, different cancellation
  structures, both response types. The rewritten inward segment is validated against the
  STEP-2 exact machinery at the 1e-17 level (gate was 1e-8). v2 carries the scan.

### [3a] Forward scan I — power-law dispersion tails (D/P class): power-law signals, no stretched exponential, and the read law measured

`step3a` (v2, NUS 4-36, dps 40): for f = κw^{−p} templates (κ = 0.4):

- **p = 2/3:** Δρ_c = −0.667…−2.252 over ν = 4…36; s-free exponential-improvement fits:
  a(s=1/3) = +0.709 with ln-residual only 4x better than pure power — and the SIGN is a
  growth, not a decay; a(s=1) = +0.013 ≈ 0. **Power-law class; no stretched-exponential
  component.** Same at p = 1 (Δρ_c → −0.76, β_fit = 0.20 drifting to the asymptote 0).
- Born linearity: κ 0.4/0.2 response ratio 1.912/1.946 (ν = 9/20) — the κ² secular term is
  4-9%, vanishing with ν.
- **The read law is measured, and it is NOT the naive pointwise multiplier.** The naive
  pred −(ν/2)F(ν/c) is off by a p-dependent O(1): measured ratio → 2.33 (p = 2/3),
  → 2.06 (p = 1, still drifting), i.e. **C(p) ≡ −Δρ_c/(νF(ν/c)) = (3−p)/2**: C(0) = 3/2
  (exact, the c_eff argument), C(1) = 1, C(2) = 1/2 (exact all orders, [3e]) — the Born
  read is the differential operator −ν[(3/2)F + (1/2)sF']|_{s=ν/c}, not −(ν/2)F. This
  changes amplitude/phase/prefactor bookkeeping of the transcription (quantified in
  [3a1]/[3d]) and NONE of the class statements.

### [3b] Forward scan II — gain tails: THE ENVELOPE-CANCELLATION KILL

ghat → γ₀w^{−2/3} (γ₀ = 0.4, Ghat ~ 3γ₀w^{1/3} — exactly the index the fingerprint needs,
as a GAIN envelope): the would-be envelope suppression ρ_c ~ ν e^{−2Ghat(ν/c)} predicts
−1.3…−34.2 across the scan; **measured Δρ_c = +0.006…+0.019 — power-law class, sign-flipped,
3 orders of magnitude away and diverging**. The common amplification e^{Ghat(w₁)}e^{−Ghat(w₂)}
cancels at the saddle (the [1b] factorization theorem made quantitative): **gain tails cannot
imprint their own exponent on the response — index-1/3 GAIN does NOT produce an index-1/3
response tail.** Gain acts only through F_eff = (ghat′ − ghat²)/c² plus an envelope-curvature
read of the SAME order (the measured pred1-ratio drift 0.55 → 1.0 → 0.88 vs the pure-dispersion
operator mix 1.3-1.7 isolates it; O(1) coefficient, same analytic class — flagged, not chased).
Contour-invariance of the weighted bilinear: 4.8e-12.

### [3e] All-orders anchors (closed forms, independent of any pipeline): power-law class at EVERY coupling

- **p = 2 (Bessel, exact in μ — Γ-function Mellin of √w H¹_λ(cw), λ = √(1/4 − μc²)):**
  ν·Δρ_c converges to **−μc²/2 exactly** — μ = 0.4: −0.80186 (ν=6) → −0.800018 (ν=200);
  μ = 2.0 (STRONG coupling, λ = 2.784i): −4.343 (ν=6) → −4.00025 (ν=200). The read
  coefficient C(2) = 1/2 is exact at all orders in μ; the deviation is a pure power series
  in 1/ν. Fitted stretched-exponential coefficients: |a_{s=1/3}| ≤ 0.066 = 1-3% of the
  required c̃ = 2.139, consistent with the 1/ν² subleading power tail — **no exponential of
  any index arises at any coupling strength.**
- **p = 1 (Coulomb/Whittaker, exact in κ):** construction g_a = e^{−z/2} z U(1−κ_W, 2, z),
  z = −2icw, κ_W = icκ/2 — ODE residual 7.3e-25; the Mellin closed form
  M_W(s) = Γ(s+1)Γ(s)/Γ(s−κ_W+1)·₂F₁(s+1, s; s−κ_W+1; ½) **quad-verified to 1.5e-26**
  (two WRONG remembered candidates — the e^{−x}-weight Γ-ratio and a mis-parameterized
  DLMF 13.10.7 — were caught by this gate before banking: bug log). Scan (κ = 0.4):
  Δρ_c = −0.7594 (ν=6) → **−0.7988 (ν=200) → −κc·1 exactly**: **C(1) = 1**, pure 1/ν
  power series, exponential coefficients ≤ 3e-2 (the 1/ν tail), no exponential of any index.
- **The C(p) = (3−p)/2 read law now has THREE exact anchors:** C(0) = 3/2 (c_eff),
  C(1) = 1 (Coulomb, all orders), C(2) = 1/2 (Bessel, all orders) — plus the Born-kernel
  interpolation at p = 2/3, 4/3, 8/3 ([3a1]). The Born read is the differential operator
  **Δρ_c(ν) = −ν[(3/2)F + (1/2)sF′]|_{s=ν/c}** — both anchors and the constant-F case are
  exactly this operator's homogeneous eigenvalues.

### [3c-B] Bands: log-normal transcription + a NEW measured structure (the beyond-band index-1/2 tail)

Log-Gaussian band (ε = 0.3, w0 = 3, σ = 0.5, analytic — entire in ln w): in-band the response
is the operator-read of the band (negative, O(1-2)); beyond the band the response crosses zero
ONCE and develops a **positive, sign-definite, NON-oscillatory tail whose ln-decrements against
√ν converge to −2.00 (ν = 20…97): an index-1/2 exponential e^{−2√ν}** — slower than the
transcribed log-normal, faster than any power. Class verdict vs (C1): **fails everything that
matters — wrong index (1/2 ≠ 1/3), no oscillation, no √3 lock, sign-definite.** Artifact tests
(contour-invariance; ε-linearity → Born-order ID) + a strong-band (ε = 1) probe bounding any
ε³-order index-1/3 oscillatory component: in flight ([3c2]/[3c3]). Note the [3c-B] ε = 0.3 tail
data already constrains a hypothetical band-generated (C1)-class term at the required
c̃ = 2.14 rate: it would have dominated the measured e^{−2√ν} fit at ν ≳ 30 and is absent.

### [3c-L] Log-periodic: the modulation transcribes, the lock is unreachable

ε cos(3 ln w) on a p = 2/3 power envelope: measured Δρ_c oscillates in **ln ν** with
Ω_fit = 2.9652 (pred 3.0; weighted rms 3.0e-02) and a power envelope (q_fit = 0.62 — the
operator's amplitude/phase mix on a modulated power, cf the G-map) — log-periodic × power,
NO stretched-exponential decay, the (C2) 1/√3 decay/oscillation lock unreachable. (The
(C1)-form fit on this data returned al = −154 / rms 6e-108 — an envelope-weighted growth
RUNAWAY, i.e. a fitter degeneracy, not a fit: clamped al ≥ 0 post-hoc, bug log; the class
kill rests on the LP-fit success, not on that row. Gain-side log-periodicity is covered by
the same class via F_eff + envelope-curvature, both log-periodic.)

*Pre-registered prediction (before reading [3c2]):* first-order kernel analysis (the
erfc-uniform incomplete-Γ transition AND the ln-s Fourier route) makes the band's
first-order beyond-band content Gaussian-or-worse small at ν ≥ 20 — the measured tail can
only be SECOND order: the ε-linearity ratio must come out ≈ 4, and a two-saddle
geometric-mean mechanism (s* ~ √(w₀ν/c)) predicts a ∝ √w₀. A ratio ≈ 2 would mean
kernel-vs-pipeline conflict → bug hunt.

**OUTCOME — the prediction was WRONG, and the resolution is a real finding ([3c2]/[3c3]/[3c4]):**
ε-linearity ratio = **2.0026/2.0002 (ν = 36/50): FIRST order.** The index-1/2 tail lives in
the first-order kernel image — the naive Gaussian-FT estimate missed the chirped-Gaussian
complex saddle (the kernel's phase curvature ν/s² against the band's finite width defeats
the Gaussian kill). Kernel-side mechanical confirmation + the w₀-scaling of the constant: [3c4].
The strong-band probe ([3c3], ε = 1) sharpens to a STRONGER statement than designed: the
whole beyond-band tail is ε-linear to ≤ 0.6% through ε = 1 (ratios vs the ε = 0.3 run:
3.354/3.335/3.3333 against exact 10/3 at ν = 36/50/97) — any ε³-order component is at the
few-permille level, so a band-generated (C1)-class term is bounded at **|A| ≲ 0.04
fingerprint-units** for this geometry (and the tail has NO oscillation at any ε). The
in-code [3c3-c] projection estimator returned a meaningless 78 (it projects index-1/2 fit
mismatch onto an exponentially smaller template — estimator-design error, bug log); the
bound above is the corrected analysis from the printed ε-scaling.

### [3a1] The exact Born kernel — independent machinery (pure Γ functions; no ODE, no contour)

First order in the Hermitian profile: Δρ_c(ν) = ∫₀^∞ K(ν,s)F(s)ds with K in closed Γ-form
(regularized incomplete-Γ; the secular-phase divergence is pure-imaginary and killed by Re
before integration — the would-be ∫F divergence never enters). Validations:

- building-block identity (γ_ν(c;s) closed vs direct quad): 1e-30-level;
- **Born-vs-exact (Bessel):** rel.err 1.22e-02 (μ=0.4) / 3.03e-03 (μ=0.1) at ν=6 — error
  ratio 4.03 ≈ 4 = the μ² Born residual (5.29 at ν=15): the kernel is exactly first order;
- **Born-vs-pipeline on the p=2/3 template:** rel 1.18e-01/2.71e-02 (κ=0.4/0.1, ν=6),
  6.7e-02/1.51e-02 (ν=15) — error ratios 4.36/4.43 ≈ 4: kernel and pipeline mutually
  validated through the κ² window;
- kernel shape: saddle bump at s* = ν/c riding a persistent O(√ν) oscillation
  e^{i(cs−ν ln s)} (the same saddle phase continued — reads the profile's frequency-c
  content; for decaying profiles, conditionally convergent and handled with
  period-aligned panels);
- **the C(p) interpolation table (pure powers):** C(2/3) = 1.16992/1.17098 (ν = 20/50;
  (3−p)/2 = 7/6 = 1.16667), C(1) = 1.00069/1.00119 (exact anchor: 1), C(4/3) =
  0.83371/0.83370 (5/6 = 0.83333) — **the linear law C(p) = (3−p)/2 holds at every point
  to ≤ 0.4%** (the 1/ν kernel correction);
- **the band reproduction:** the kernel reproduces the [3c-B] beyond-band index-1/2 tail at
  ratio 0.9974 (ν = 36) / 0.9998 (ν = 50) — the non-transcriptive channel is first-order
  physics, certified by two independent machines;
- **[f] the kernel-side keystone (G profile through the kernel — no ODE, no contour):**
  the 16-point Born-kernel response tracks the FULL operator prediction pointwise
  (ratios → 1.005/0.998 at the window top; low-ν deviations = the documented subleading/
  near-node structure; median |ratio−1| = 3.2%). Two-component operator-model extraction
  (`agentHH_fit_extract.py`; the single-component VARPRO is ill-posed on this window and
  ran away — bug log 11): **c̃_fit = 2.1300 (target 2.1388: 0.4%), lock r_fit = 1.732
  (√3 to <1%; the wssr rises 5-100x at ±0.016-0.05 around it), amplitude K = 0.964.**
  The exponent triple (s = 1/3, c̃, √3) transcribes through machinery fully independent
  of the pipeline.

### THEOREM HH-1 (saddle transcription / the index no-go) — scope-labeled

Let the pump be any minimal (2nd-order-EOM) scale-invariant linear modification of the khronon
mode dynamics — gain ĝ(k_phys/H) and/or dispersion f(k_phys/H) — reduced by [1a]-[1b] to the
universal Hermitian profile F on w = k_phys/H. Then:

1. **(Read law; Born-exact, three exact anchors.)** The worldline commutator-density correction
   is the differential read Δρ_c(ν) = −ν[(3/2)F + ½sF′]|_{s=ν/c} (+O(F²), +O(1/ν) kernel
   corrections): on powers w^{−p} this is C(p) = (3−p)/2, exact at p = 0, 1, 2 to all orders
   in the coupling ([3e]); the first-order kernel is explicit in Γ-functions ([3a1]).
2. **(Envelope kill.)** Gain envelopes cancel at the saddle ([1b] exactly; [3b] numerically):
   a pump with e^{−2Ĝ} of ANY index — including 1/3 — does NOT imprint that exponent on the
   response. Gain acts only through F_eff = (ĝ′ − ĝ²)/c² (+ same-order curvature read).
3. **(Index transcription + the one non-transcriptive channel.)** The large-ν exponential
   class of Δρ_c equals the large-w analytic class of F: powers ↦ powers (no exponential of
   any index, all orders at the anchors); e^{−aw} ↦ e^{−aν/c} ([3c-E] control);
   log-periodic ↦ log-periodic×power ([3c-L]); filter banks ↦ channel-wise sums ([3c-X]);
   the locked Gevrey-3 pair ↦ the locked Gevrey-3 pair with the SAME (s = 1/3, c̃, √3-lock)
   and affine (q, amp, phase) bookkeeping ([3d]/[3a1-f]/[3d2]). ONE non-transcriptive
   first-order channel exists and is now mapped: band-localized profiles shed a
   **beyond-band index-1/2 MONOTONE tail** (e^{−2√ν} for the test band; FIRST order,
   ε-linear to ≤0.6% through ε = 1; reproduced by the exact kernel at 0.26% — [3c-B]/[3c2]/
   [3c3]/[3c4]). It has the wrong index, no oscillation, and no lock — and it is always
   subdominant to a true index-1/3 component (2√ν > c̃ν^{1/3} for ν > (c̃/2)⁶ ≈ 1.5).
4. **(Consequence — the generation no-go.)** The (C1)-(C2) fingerprint
   A ω^{−1/3}e^{−c̃ω^{1/3}}cos(√3c̃ω^{1/3}+φ̃) lies in the image of scale-invariant pumping
   ONLY through profiles already carrying the locked pair e^{2c̃e^{±2πi/3}(cw)^{1/3}}; the
   unique Born preimage is **F_req(w) = (3A/c̃)(c_χw)^{−5/3}e^{−c̃(c_χw)^{1/3}}
   cos(√3c̃(c_χw)^{1/3} + φ̃ + π/3)** modulo the kernel's s^{−3} null direction (C(3) = 0).
   The null freedom matters: the regular inversion of the FULL banked target,
   F_req(s) = −(2A/X³)∫₀^X x·2ImD(x)dx (X = c_χs), is **POSITIVE everywhere** ([4i]) —
   the exponentially small locked oscillation rides a sign-definite s^{−3} backbone that
   the response operator annihilates. So the implied pump admits a positive
   (dispersion-stiffening) representative; the bare locked-pair representative oscillates;
   a pure-gain realization necessarily ALTERNATES (gain/loss comb). Either way the pump
   profile must carry c̃·c_χ^{1/3} — i.e. ζ̃^{2/3} — in its own shape: **the dynamics
   transcribes the fingerprint; nothing scanned GENERATES it.**

*Scope honesty:* (1)-(2) are Born-order analytic + machine statements with all-orders
anchors at p = 0, 1, 2; (3)-(4) are proven on the registered classes (P/D/B/L/X/E/G) and at
every tested order — NOT an unconditional all-orders theorem for arbitrary profiles. The one
measured nonlinear surprise (the band's index-1/2 tail) does not approach (C1): wrong index,
no oscillation, no lock; the ε³/index-1/3 loophole is bounded empirically ([3c3]) for the
test band. C∞-non-analytic profiles are outside the pipeline's contour but their
beyond-all-orders Mellin tails are governed by their own Gevrey data — profiles whose Borel
structure produces the locked ±2π/3 pair ARE the G class by definition.

(further results pending — appended as they land)

## STEP 4 — Gates: ALL PASS (and the amplitude geometry inverts)

- **[4i] No-tachyon ceiling, exact-inversion form** (hbar(X) = (2/X³)∫₀^X x·2ImD dx, the
  m = 0.5-band target): **A_stab = 1784.6 (fw) / 2318.6 (canon) / 1480.9 (hostile)** —
  the dynamics-side ceiling sits **~300-400x ABOVE the (C3) positivity window (5.716)**:
  the pump's stability does NOT constrain the amplitude in the physical range. The naive
  pointwise ceiling (which would have bound A at O(1-4)) was an artifact of the wrong read
  law — computed, exposed, retracted in-run (bug log). F_req's minimum is −A·(4.3-6.8)e-4
  (the s^{−3} null tail; first moment M1 = +0.0663/−0.0103/+0.0363 by footing — sign
  band-shape-dependent); the [4iii] print line "F_req ≥ 0 everywhere" overstates by that
  4e-4 sliver — conclusion unchanged (see below). [4ii] tachyonic measure at A = 5.716:
  exactly ZERO (all footings).
- **[4iii] UV/PPN/Cherenkov:** |F| = 10^{−9.3} at cluster-scale modes (ν = 10³),
  10^{−163958} at 1 AU modes — the pump is exponentially OFF everywhere local physics
  lives; agentU's corner is inherited UNCHANGED in BOTH variants: generic
  (c_χ² = O(γ/α) ≫ 1) trivially, and the tuned Cherenkov-edge sliver (c_S² ∈ [1.000, 1.033],
  needs F > −0.03) — F_req ≥ −3.2e-3 even at the (C3) ceiling: an order inside. The pump
  acts at k_phys ~ (1-10)H/c_χ — the khronon sound-horizon band, where nothing else
  constrains the dispersion.
- **[4iv] Gain realization** (ghat′ − ghat² = c²F_req): an H-paced **alternating gain/loss
  comb** — ghat ∈ [−0.0825, +0.0046] at A = 1, four sign changes, max physical gain rate
  w·ghat = 0.037 per Hubble time, net ΔGhat = −0.053: bounded, no secular runaway, NOT
  sign-definite (a pure-gain pump cannot be positive; the positive realization is the
  dispersion one, [4i]).
- **[4v] The X2 invoice:** response-side throughput ZERO (dispersion realization) or the
  bounded alternating comb above; the amplitude invoice (λ²⟨Q²⟩ ∝ m/H, ~10³³-10³⁵ W per
  L*-galaxy) is a STATE-sector cost — inherited per (C3), not re-adjudicated. No new energy
  obstruction; no relief.
- **Stability outside the pumped band:** F → 0 at both ends (w⁴-class turn-on below the
  window; e^{−c̃(cw)^{1/3}} above); modes outside the band untouched; the comb's envelope
  bounded (ΔGhat above).

## STEP 5 — Coefficient discipline (raw, all footings, quarantine audited)

| footing | ζ (agentV raw) | c̃ | pump constant c̃·c_χ^{1/3} (at scan c = 2) |
|---|---|---|---|
| framework | 2.0247 | **2.1388** | 2.6947 |
| canonical | 1.7881 | 1.9687 | 2.4804 |
| hostile | 2.2271 | 2.2790 | 2.8714 |

- The transcription map and corrected inverse are stated with c_χ SYMBOLIC (agentU's corner,
  raw; not fixed here); every fitted constant is c-independent by the x = c·w parametrization
  ([3d-4] c = 3 re-verification).
- Amplitude: (C3)'s |A| ≤ 5.716 window is the binding constraint; the dynamics-side ceiling
  (1481-2319 by footing) does not bind in the physical range; the PHYSICAL normalization
  (λ², the wattage) stays with agentI/agentX — inherited. **NO Z claims; no a₀ claims;
  nothing here fixes ζ.**
- **Quarantine:** (16π/3)^{1/4} = 2.0231922 — never used numerically (mechanical source
  audit in [5d]: 1 occurrence = the quarantine print itself; ζ literals = the ZETA dict
  only). The scan ran on agentV's raw ζ = 2.0247 (0.07% away from the quarantined
  closed-form candidate; kept apart).
- (C4) family universality: the universal ODE and F_req are b-independent by construction;
  βκ² = H² makes the leading worldline law family-universal (agentEE, inherited); band
  dependence at relative O(κ²τ*²).

## VERDICT

(pending)

## Bug log

1. (STEP 2, caught by the free gate) real-segment contour direction sign: the Mellin contour runs
   w_cut → r0 but the solve parametrization runs r0 → w_cut; the first assembly integrated with
   dw = (w_cut − r0)dx, flipping the segment's sign (free ρ_c off by O(0.5)). Fixed; free gate then
   exact to 1e-44.
2. (STEP 2, environment) mpmath `hankel1(λ, iy)` loses the exponentially small branch for large y
   (returned 1.8e+8 at y = 170 where truth ~1e-74) — the planned Hankel-quadrature cross-check was
   replaced by the exact Γ-function Mellin closed form (stronger anyway). The Riccati construction
   is the numerically stable route to the decaying branch.
3. (v2 rewrite, prior session → this session) the inward-segment assembly's orientation bug:
   rewritten in direct w-parametrization; validated this session at 1e-17 against v1 ([3a0b]),
   1e-16 free, 9e-11 contour-shift.
4. (STEP 3e) FD-derivative gate set below the FD method's own truncation floor (1e-25 vs
   h² = 1e-24): measured 1.06e-24 — gate corrected to 1e-20; no formula error.
5. (STEP 3e) TWO wrong remembered Whittaker–Mellin closed forms caught by the quadrature gate
   before banking: the e^{−x}-weight Γ-ratio (off x1.3-1.6) and a mis-parameterized
   DLMF 13.10.7 (off x1.2-1.4); the verified form is the G&R 7.621.2 class
   Γ(s+1)Γ(s)/Γ(s−κ_W+1)·₂F₁(s+1, s; s−κ_W+1; ½), exact to 1.5e-26.
6. (STEP 3a/3b interpretation) the prior session's draft prediction −(ν/2)F(ν/c) is NOT the read
   law: measured C(p) = (3−p)/2 — the operator −ν[(3/2)F + ½sF′] (three exact anchors + kernel
   interpolation at p = 2/3, 1, 4/3 to ≤0.4%). No banked claim used the wrong coefficient; the
   printed "pred"-columns in [3a]/[3b]/[3d] are reinterpreted in the memo.
7. (fit_osc_model, caught on [3c-L]) envelope-weighted VARPRO has a growth runaway when the data
   has no decay (al → −154, rms 6e-108 — a degeneracy, not a fit): clamped al ≥ 0 post-hoc; the
   L-class verdict rests on the log-periodic-model fit (Ω_fit = 2.965, rms 3e-2), unaffected.
8. (STEP 3c2/3c4 — a pre-registered prediction falsified and resolved) the index-1/2 beyond-band
   tail was predicted SECOND order (ratio 4); measured FIRST order (2.0026/2.0002). The exact Born
   kernel reproduces it (ratio 0.9974 at ν = 36): genuine first-order physics (the
   chirped-Gaussian complex saddle) — the hand saddle-estimate was the error, both machines agree.
9. (STEP 3c3) the in-code (C1)-component projection estimator is invalid (projects index-1/2 fit
   mismatch onto an exponentially smaller template; returned a meaningless 78): superseded by the
   ε-scaling analysis in the memo (band response ε-linear to ≤0.6% through ε = 1 ⇒ cubic
   (C1)-component bounded at |A| ≲ 0.04 fingerprint-units for the test geometry).
10. (STEP 4) the naive pointwise no-tachyon ceiling (O(1-4) by footing) was an artifact of the
   wrong read law (bug 6): the exact-inversion ceiling is 1481-2319 — retracted before banking;
   the [4iii] print's "F_req ≥ 0 everywhere" overstates by the −(4-7)e-4·A s^{−3}-tail sliver
   (conclusion unchanged, an order inside even the tuned Cherenkov corner at the (C3) ceiling).
11. ([3a1-f]/[3d-3] fitting) the 4-parameter envelope-weighted VARPRO is ill-posed on the
   16-point window: unbounded (q, be) corners + frequency aliasing produce runaway "fits"
   (q = +155 / rms 4e-98 on the kernel data; q pegged at a +3 bound with be = 320 aliased) —
   the al ≥ 0 clamp (bug 7) was insufficient. Replaced by the well-posed two-component
   operator-model extraction (`agentHH_fit_extract.py`: scan (c̃, lock) inside the FULL
   operator prediction, fit only the scale): sharp parabolic minima, no degeneracy. The
   in-process [f]/[3d-3] fit rows are superseded by the extraction logs.

## Artifacts

`agentHH_pump_profile.py` -> `agentHH_pump_profile.out` (pending)

## Anchors

- agentEE_sigma_khronon.md (C1-C5; b-family theorem; Bogoliubov lemma; positivity window A_max=5.7)
- agentV_kernel_inversion.md (sigma_req; zeta raw by footing; a->0 no-kernel)
- agentX_sk_gate.md (Theorem X2; windowed filter-bank causal kernel; the invoice)
- agentU_khronon_m22.md (PPN/Cherenkov corner; c_chi constraints)
