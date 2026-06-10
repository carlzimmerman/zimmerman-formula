# Door I-b (the non-perturbative loophole): the exactly solvable detector CLOSES it — Gaussian dynamics gives κ-only thermal dressing at every coupling strength

*agentF, 2026-06-10. Task: agentB's census excludes the F4 susceptibility structure (m_eff ∝ dT_eff/da,
T_eff = κ/2π, κ = √(a²+H²)) at every FINITE order in the UDW coupling λ, and names the loophole: the
NON-PERTURBATIVE regime, "precisely where perturbation theory around m_bare must fail" if inertia is to
vanish at a→0. This doc tests that loophole with a real computation in the exactly solvable
(Gaussian / harmonic-oscillator UDW) model class, where the full resummation in λ is available in closed
form. Artifacts: `agentF_nonpert_detector.py` + `.out` (sympy identities machine-verified; mpmath numerics
cross-checked two independent routes; weak-coupling limit anchored to agentB's machine-verified λ² result).
Verdict at the end, both ways, full weight. Units ħ = c = k_B = 1.*

## 0. The question, on the loophole's own terms
The census argument was perturbative: at order λ^{2n} every response coefficient is a degree-n polynomial
in a² with κ-only coefficients, and μ_F4 = a/κ is not. The named escape: a non-perturbative resummation
could in principle produce |a|/κ (compare: √(x²) is non-polynomial but is the limit of even polynomials).
And the physical suspicion was sharper: *vanishing* inertia at a→0 is exactly where an expansion around a
finite m_bare must break down. So the question for this doc is NOT "what happens at the next order" but:
**in a model where the λ-resummation is EXACT, does any strong-coupling regime produce a response
∝ a/κ (vanishing at a→0, saturating at high a), or does the A(κ) + a²B(κ) structure persist?**

## 1. The model: the one place this is exactly decidable
Internal harmonic oscillator Q (unit internal mass, bare gap Ω₀) on the prescribed stationary Deser–Levin
worldline z(τ) in dS₄ (uniform proper acceleration a; κ = √(a²+H²)), linearly coupled to the conformally
coupled massless scalar in the Bunch–Davies vacuum: H_int = λ Q(τ) φ(z(τ)). Linear coupling + Gaussian
field + quadratic detector ⇒ the Heisenberg equations are linear and solve EXACTLY at every λ: this is the
Raine–Sciama–Grove / Lin–Hu class, the standard exactly solvable laboratory for accelerated-detector
back-reaction. Literature anchors (ids verified):
- **Deser & Levin, arXiv:gr-qc/9706018** (CQG 14 (1997) L163): the stationary dS worldline family is
  thermal at T_eff = κ/2π — the framework's own kernel object.
- **Lin & Hu, arXiv:gr-qc/0507054** (PRD 73 (2006) 124018): exact (non-perturbative) detector–field
  correlations for the uniformly accelerated harmonic UDW detector — the model and methods used here.
- **Lin & Hu, arXiv:gr-qc/0611062** (PRD 76 (2007) 064008): "Backreaction and the Unruh effect: new
  insights from exact solutions of uniformly accelerated detectors" — non-perturbative back-reaction in
  this class; the detector ceases to be a perfect thermometer at strong coupling, *but the dissipation
  kernel stays local* — the fact our lemma below makes explicit.
- **QBM/quantum-Langevin machinery** (pre-arXiv): Raine–Sciama–Grove, Proc. R. Soc. A 435 (1991) 205
  (exact accelerated oscillator); Unruh & Zurek, PRD 40 (1989) 1071; Hu, Paz & Zhang, PRD 45 (1992) 2843;
  Ford, Lewis & O'Connell, PRA 37 (1988) 4419 (the quantum Langevin equation).
- **Kaplanek & Burgess, arXiv:1912.12951, 1912.12955** (JHEP 2020): modern open-system treatments of
  accelerated and dS detectors (Markovian-validity caveats; consistent with the steady states used here).

**The exact solution.** Eliminating the field exactly (it enters quadratically) gives the quantum Langevin
equation on the stationary worldline:
> Q̈ + 2γQ̇ + Ω_R²Q = −λ φ_in(z(τ)), γ = λ²/8π (resummed; see lemma), Ω_R = renormalized gap,
> Q(τ) = −λ∫₀^∞ h(u) φ_in(z(τ−u)) du, h(s) = e^{−γs} sin(Ω̃s)/Ω̃, Ω̃ = √(Ω_R²−γ²) (overdamped branch
> automatic), h̃(ω) = 1/(Ω_R² − ω² − 2iγω).
The damping γ ∝ λ² sits in the DENOMINATOR of h̃: this is the all-orders geometric resummation of the
self-energy — "strong coupling" is γ/Ω_R ≳ 1, and the steady state exists for every γ > 0 (both poles of
h̃ strictly in the lower half-plane; machine-checked structure). Internal consistency of the resummation
is exact and machine-verified ([D3]): Im⟨Q(s)Q(0)⟩_int = −h(s)/2 at every coupling — equivalently, the
canonical commutator is preserved, which LOCKS γ = λ²/8π (no convention freedom).

## 2. The lemma that decides it: the dissipation kernel cannot know (a, H) — only the noise can, and the noise knows only κ
The Wightman pullback is the Deser–Levin thermal form W(s) = −(κ²/16π²)/sinh²(κ(s−iε)/2) ([A3],
re-verified). Its Laurent expansion about s = 0 is the κ-INDEPENDENT double pole −1/(4π²(s−iε)²) plus an
even ANALYTIC series whose coefficients carry all the κ-dependence ([B1]). The field COMMUTATOR pulled
back on the worldline is the difference of the two iε prescriptions, in which every analytic term cancels:
> **⟨[φ(z(τ)), φ(z(τ−s))]⟩ = (i/2π) δ′(s) — EXACTLY, for every (a, H).** ([B1] symbolic structure; [B2]
> distributional numerics: the action on a test function is κ-independent to a few ×10⁻⁵ relative across
> κ ∈ {0.5, 2, 10} at ε = 10⁻⁵ and converges linearly in ε to −(i/2π)φ′(0); Fourier check
> S(ω)−S(−ω) = ω/2π.)
This is the Huygens property of the conformal massless field made explicit on the Deser–Levin family (two
points of a timelike worldline are never null-separated; cf. the locality of the damping in the Lin–Hu
exact solutions, and the Huygens discussions in arXiv:2301.08717). Consequences, which are the whole
non-perturbative content:
1. the exact dissipation kernel of the Langevin equation is LOCAL and TRAJECTORY-BLIND: γ = λ²/8π and the
   (divergent) frequency renormalization are the SAME for every (a, H), at every coupling;
2. the ONLY (a,H)-dependence of the exact interacting steady state enters through the noise correlator
   W_κ — i.e. **through κ alone**;
3. the explicit a-dependence of force vertices is geometric and polynomial: the longitudinal-gradient
   identity ê·∇W(s) = −a·W(s) holds at BOTH slots / both orderings ([A4], slot-2 version verified here in
   addition to agentB's slot-1), so each force vertex carries exactly one factor of a; the clock/measure
   vertices carry a² (agentB [A5–A6]).
**Therefore the exact response is [polynomial in a] × [κ-only functions] at EVERY value of λ.** The
resummation changes the VALUE of the coefficients, never their κ-only character. There is no channel
through which (a, H) can enter separately. The deep-MOND limit a→0 is not where the theory breaks, either:
the exact steady state exists and is smooth at κ = H. *Nothing fails there; the inertia simply does not
vanish.*

## 3. The exact static force and the no-go
The exact force along ê (noise-vertex channel — the same channel as agentB's static λ² kernel, his
g_free(s) → the exact dressed g_int(s), with Im g_int = −h/2):
> **⟨F⟩ = −a λ² [δm_UV + G(κ; Ω_R, γ)]**, with the exact resummed thermal mass
> **G(κ; Ω_R, γ) = ∫₀^∞ h(s)[ReW_κ − ReW_vac](s) ds = (1/4π²)∫₀^∞ dω ω Re h̃(ω)[coth(πω/κ) − 1]**.
Two independent routes (time-domain vs spectral) agree to 7 digits at three of the four probe points and
to 3×10⁻⁴ at the fourth (coarser time-grid; [D1]). Weak-coupling limit
reproduces agentB's machine-verified λ² result exactly under the normalization map G → G_th^B/(2Ω)
(⟨QQ⟩ vs ⟨μμ⟩; ratio 1.00000 at κ ≤ 0.3, [D2]), including his low-T coefficient (κ²/48π²Ω² ↔ his 1/6)
and his high-T log family (slope → 1/4π², the 1/2π² family mapped). The self-field vertex contributes the
composite a·Q̂² renormalization channel (the non-perturbative descendant of agentB's δm_UV and his flagged
mean-force subtlety): scheme-dependent finite part, magnitude tabled ([D8]) — and κ-only, so it cannot
affect anything below.
The adiabatic susceptibility along the stationary family is m_resp(a,H) = G(κ) + (a²/κ)G′(κ) (+ m_bare +
UV const). The no-go ODE ([C1], independent re-run): demanding G + (a²/κ)G′ = C·a/(2πκ) forces
G = [Cκ/2 + πc₁]/(π√(κ²−H²)) — explicitly H-dependent with a pole at κ = H, i.e. exactly at a = 0. The
EXACT resummed G above is finite at κ = H for every (Ω_R, γ) (tables [D4]): **no coupling strength can
satisfy the ODE except C = 0 (ordinary inertia). The F4 structure is excluded at every λ, not just at
every finite order.**

## 4. What the exact strong-coupling response actually looks like (raw numbers)
- **G > 0 everywhere probed** ([D4]: γ/Ω from 10⁻³ to 10², κ from 0.1 to 100; [D7] gapless corner): the
  bath only ever ADDS inertia — the anti-MOND direction, now non-perturbatively.
- **Strong coupling ATTENUATES the dressing, never flips it**: at fixed κ, G falls with γ (e.g. at κ = 10,
  Ω = 1: G = 4.40×10⁻² at γ = 10⁻³ → 6.2×10⁻⁴ at γ = 10²) but stays positive; the high-κ behaviour at
  every coupling is the universal +log growth, slope 1/4π² (ratio 0.9984 at γ = 0.01 by κ = 100; the
  strong-coupling slope deficit at κ ≤ 100 is pre-asymptotic — at γ = 10 the slope reaches 0.980×(1/4π²)
  by κ = 1000–3000, [D4] deep-κ check).
- **The a→0 floor is NONZERO at every coupling** ([D5], dS, H=1): m_resp(a→0) = G(H) > 0 (e.g. 5.4×10⁻⁴,
  4.9×10⁻⁴, 2.0×10⁻⁴ for γ/Ω = 0.01, 1, 10 at Ω = 2) and m_resp GROWS with a while μ_F4 must vanish at
  a→0 and saturate at 1. Flat space (κ = a, Unruh bath, [D5b]): same log-growing positive dressing.
- **No inertia-deficit corner exists anywhere** ([D7]): the most MOND-flavoured candidate (gapless
  Ω_R → 0 at strong γ — spectral weight maximally below resonance, Re h̃ < 0 over almost the whole range)
  was hunted for and comes out POSITIVE at all κ: the IR sliver of Re h̃ > 0 below Ω_R plus the exact sum
  rule ∫₀^∞ Re h̃ dω = 0 (h(0⁺) = 0) protect positivity. (Internal consistency: the gapless rows obey the
  exact κ/γ scaling demanded by dimensions, e.g. G(κ=30, γ=10) = G(κ=3, γ=1) = 1.487×10⁻². A pre-run
  back-of-envelope had guessed this corner could go negative; the computation says otherwise — recorded.)
- **The class cannot even caricature the F4 shape** ([D6]): granting the most charitable affine freedom
  (free offset and scale, i.e. free m_bare and λ²) and scanning (Ω, γ) over four decades, the best
  achievable max-deviation from μ_F4(x) on x ∈ [0.1, 30] is **0.254** — a 25%-of-range miss (μ spans
  0.10→0.999); SPARC-grade shape fidelity is %-level. The failure mode is structural: any κ-only G gives
  a floor at a→0 plus unbounded log growth at high a; μ_F4 needs zero floor and saturation.
- Raw coefficients produced (Door-III discipline, reported in isolation): γ = λ²/8π; low-T mass
  κ²/(48π²Ω²); high-κ log slope 1/(4π²) ≈ 0.02533. None equals 1/Z = 0.1727 or any Z-related number;
  all are the λ²-family coefficients (1/6, 1/2π²) carried through the resummation unchanged in form.

## 5. How far the closure reaches (and exactly what remains open)
The lemma-based argument does not actually use the harmonicity of the detector: for ANY internal system
coupled linearly in φ on a point worldline, integrating out the Gaussian field gives an influence
functional built solely from (i) W_κ-pullback — κ-only, (ii) the retarded kernel — trajectory-blind by the
lemma, and (iii) vertices polynomial in a by the exact identities. Non-Gaussian INTERNAL dynamics
(two-level systems at strong coupling, multi-level/composite detectors with worldline-localized coupling)
therefore cannot generate a/κ either, at the structural level: the κ-only census survives any resummation
of the internal dynamics. (Couplings nonlinear in φ bring products of W_κ-pullbacks — still κ-only — plus
local UV counterterms, which are polynomials in the local invariants a², H²: census-safe. Stationarity of
the strong-coupling steady state is proven here only for the Gaussian class; for general detectors it is
an assumption, flagged.)
What this CANNOT close, named precisely (the honest doors out, unchanged in kind from agentB's list but
now sharpened — these are the ONLY ways out within a bath mechanism):
1. **Non-Huygens fields**: massive fields, and the minimally coupled massless scalar in dS (its dS-IR
   pathology breaks the Deser–Levin reduction AND its retarded Green function has a tail — the dissipation
   kernel then CAN be trajectory-dependent, i.e. know a and H separately. This is now the unique field-side
   escape, and it was already the one field choice where agentB's premise fails).
2. **Extended (non-point) detectors**: field sampled off the worldline — the pullback identities and the
   κ-reduction do not apply. (Composite detectors with point support do NOT escape; see above.)
3. **Field-level realizations** (Door II's lane): outside the worldline class entirely — and after the
   lensing wall (40.5σ) the missing object is a hybrid with a metric partner anyway.
4. **Non-stationary regimes**: no steady state, no κ — though F4 as a quasi-static law presupposes
   stationarity, so an escape here changes the hypothesis, not just the mechanism.

## 6. VERDICT (both ways, full weight)
- **CLOSES** — the non-perturbative loophole, within the model class where it was posed. In the exactly
  solvable Gaussian (harmonic UDW) model on the Deser–Levin family — flat-space Unruh bath (κ = a) and dS
  (κ = √(a²+H²)) alike — the EXACT, all-orders-in-λ inertial back-reaction is ⟨F⟩ = −aλ²[A(κ) + a²B(κ)]
  with κ-only coefficients: the same census structure as at λ², now with resummed coefficients. The
  reason is structural and machine-verified: the dissipation kernel pulled back on ANY member of the
  stationary family is the SAME contact distribution (i/2π)δ′(s) — strong coupling has no channel through
  which (a, H) can enter except κ. The no-go ODE then excludes m_resp ∝ a/κ = μ_F4 at every coupling
  strength; numerically the exact response has a nonzero κ-only floor at a→0, grows logarithmically where
  μ_F4 saturates, is anti-MOND-signed (inertia ADDED) at every (Ω, γ, κ) probed including the gapless
  ultra-strong corner, and cannot approach the F4 shape closer than a 25%-of-range miss even with free
  affine parameters. The "perturbation theory must fail at vanishing inertia" intuition is tested and
  false here: the exact theory is smooth at a→0 and the inertia simply does not vanish. **F4's mechanism
  candidacy in the worldline-bath class — perturbative AND non-perturbative, Gaussian and (structurally)
  any point-detector internal dynamics — is now closed, not merely finite-order-closed.** This is
  framework-unfavorable and is stated as such at full weight.
- **What WOULD have supported F4** (pre-stated in the task): a resummed kernel ∝ a/κ, a vanishing floor,
  saturation at high a. None of the three appears anywhere in the exact class.
- **What survives untouched**: F4 as a selected effective law (Saturn ×4, SPARC-competitive, DR4 fork) —
  selection never claimed a mechanism; the kernel a₀ ∝ √ρ_DE; agentB's finite-order census, which this
  doc upgrades to an all-orders statement in its class. The Bohr-rule analogy now reads: the rule stands,
  its first candidate mechanics is dead at finite order AND at strong coupling; a mechanism, if it exists,
  lives in non-Huygens fields, extended detectors, or the field-level hybrid — all named, none cheap.
- **OPEN (the residue)**: the four doors of §5. The sharpest actionable one inherited by the program: the
  minimally coupled / massive-field tail calculation (trajectory-dependent dissipation = the unique
  bath-side structure that can still know a and H separately).
