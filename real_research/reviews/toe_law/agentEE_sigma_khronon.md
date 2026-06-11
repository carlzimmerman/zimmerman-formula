# agentEE — Can the khronon medium's own fluctuation spectrum produce sigma_req structurally?

**STATUS: COMPLETE — all four steps banked. VERDICT: STRUCTURALLY-CAPABLE for the PUMPED khronon
medium (matching conditions C1–C5 written, §STEP 4); the MINIMAL/free khronon CANNOT (zero tail on the
whole stationary family — machine theorem); deep-MOND flattening floor a_* inherited, not evaded.
STEP 1's committed machine checks were repaired this session (bug log below); all claims survive.**

Date: 2026-06-11. Relaunch (prior attempt stalled pre-write); continuation session completes STEPs 2–4.

**Bug log (continuation, recorded not hidden):** the prior chunk's committed script did NOT verify what
the STEP 1 text claims: [1a] compared a trapezoid k-grid against the closed form with a mismatched
regulator (rel.diff 0.67 — verified nothing); [1b]'s λ-scan silently dropped every level-set point but
one (r²<0), so the printed "spread" was trivially 0.0 and the VARIES verdict was unearned; [1c]'s sympy
difference was printed unreduced. All three repaired (rotated-contour mode integral; guaranteed-valid λ
grid with an all-points assertion; exp-rewrite simplification). After repair: [1a] rel.diff 0.0 / 1.2e-16;
[1b] spread 1.88–2.01 for c_s = 2,10 vs 9.6e-16 for c_s = 1; [1c] difference exactly 0. **The STEP 1
claims all survive — but as committed they were unverified. Per the working rule, recorded.**

## Target

Link 5's sole remaining derivation. agentV (kernel inversion) pinned the REQUIRED spectral
weight sigma_req:

- fourth-root **essential singularity at the lightcone**,
- **all inverse moments zero**,
- asymptotics sigma(u) ~ u^(-13/8) e^(-zeta u^(-1/4)) cos(zeta u^(-1/4) - pi/8) as u -> 0+,
- dS Kallen-Lehmann **positivity kills every dS-invariant carrier** — the carrier must
  BREAK dS invariance.

agentX (Theorem X2): the medium must be ACTIVE/pumped; the Lambda/dS budget pays.
agentU: the khronon (unit-timelike-gradient scalar, M22 corner) is the named matter-sector
candidate; it has a preferred foliation by construction.

**Scoping question:** does the khronon's own fluctuation spectrum (a) evade V's positivity
no-go via foliation breaking, and (b) live in (or reach) the fourth-root essential-singularity
asymptotic class — or what extra structure is needed?

Coefficient discipline: raw numbers only; zeta = (16pi/3)^(1/4) quarantined as input,
not re-derived; NO Z claims. Framework-favorable territory — hostility to wishful steps
is mandatory.

## STEP 1 — Literature pin: khronon mode functions on dS vs fundamental scalar

**Pinned ids (WebSearch 2026-06-11):**

- **arXiv:1206.1083** — *Khronon inflation* (Creminelli–Noreña–Peña–Simonović, JCAP 2012). The
  scalar mode of the preferred foliation ("khronon") on a de Sitter background with full time
  reparametrization invariance: only two leading operators survive, and **the mode wavefunctions
  have the same form as in MINKOWSKI space** — the (1 + ic_s kη)e^{−ic_s kη} dS dressing of a
  fundamental scalar is absent; perturbations are produced only when the reparametrization
  symmetry breaks. This is the cleanest published statement that the khronon's dS two-point
  structure is NOT the Bunch–Davies family.
- **arXiv:astro-ph/0407437** — Lim, *Can we see Lorentz-violating vector fields in the CMB?*
  (PRD 71, 063504). The aether's scalar (and vector) modes quantized on the preferred foliation
  during inflation: modes labeled by comoving k on the foliation, dispersion ω = c_s k with
  **c_s² a ratio of the aether couplings** (≠ 1 generically), spectra carrying inverse powers of
  c_s. Supporting: **arXiv:1003.1283** (Armendáriz-Picón–Sierra–Garriga, Einstein-aether and
  BPSH/khronon primordial perturbations — same structure in the khronometric limit);
  **arXiv:1309.4778** (aether-inflation perturbations can grow exponentially when the LV scale
  is low — the foliation sector admits non-passive corners, cf. X2's option (b), which agentU's
  gate 1 forbids for us).

**How the khronon's dS mode functions differ from a fundamental scalar's (the answer):**

1. **Mode label and cone.** Modes are plane waves in comoving k ON THE PREFERRED FOLIATION with
   dispersion ω = c_χ k, c_χ² = O(γ/α) ≫ 1 in agentU's generic PPN corner. The singular support
   of W sits on the SOUND cone r = c_χ|Δη|, not the metric lightcone — for c_χ > 1 the
   singularity lies at metrically SPACELIKE separation; on metric-timelike chords (where
   sigma_req lives) the free correlator is real-analytic.
2. **No BD dressing / no Z-dependence.** A fundamental massless dS scalar carries the
   (1 + ikη)e^{−ikη} curvature dressing and (for invariant masses) a Wightman function W(Z) of
   the single dS invariant Z. The khronon's wavefunctions are Minkowski-form (1206.1083): its
   W is a function of (η, η′, r) invariant only under the residual 7-parameter subgroup
   E(3) ⋊ dilatation ⊂ SO(4,1) — i.e. a function of TWO independent invariants (e.g. Z and
   η′/η), not one. The three dS boosts are broken by the foliation.
3. **State + dynamics both break dS.** The adiabatic vacuum on the foliation is not a dS-invariant
   state, and the dynamics (foliation-dependent kinetic term) is not a dS-invariant operator —
   so BOTH hypotheses of the Bros–Moschella decomposition fail, not just the state's.
4. **What survives:** dilatation acts as proper-time translation on comoving worldlines ⟹ the
   worldline pullback is still STATIONARY there (verified in §2 below; the conformal-c_s member
   even stays KMS at H/2π — thermality is again "not what breaks", N1-consistent).

## STEP 2 — The positivity escape: which step of V's KL argument uses dS invariance, and does the khronon evade it?

### 2.1 V's argument dissected: four steps, and where invariance is load-bearing

agentV §5 (the legality kill) is the chain (KL-A)→(KL-D):

- **(KL-A) Single-invariant reduction W = W(Z).** Uses BOTH Bros–Moschella hypotheses: an
  SO(4,1)-invariant state (U(g)Ω = Ω) AND covariant dynamics (U(g)φ(x)U†(g) = φ(gx)). Only then is
  the two-point function constant on the orbits of point pairs — a function of the single invariant Z.
- **(KL-B) Normal analyticity** (the dS spectral condition): gives the maximal analyticity domain and
  the very EXISTENCE of "the cut density σ on Z > 1" as the boundary value of one analytic function.
- **(KL-C) Group-theoretic positivity:** harmonic analysis of positive-definite invariant kernels on
  SO(4,1)/SO(3,1) (Bochner–Godement over the unitary dual; Bros–Moschella gr-qc/9511019;
  Hogervorst–Penedones–Vaziri 2107.13871; Loparco et al. 2306.00090): W(Z) = ∫dρ(M²)W_BD(Z;M²),
  **dρ ≥ 0** over principal + complementary series.
- **(KL-D) Rigidity of the basis:** every σ_M(u) is analytic at u = 0 with the positive Taylor tower
  (h₊)_k(h₋)_k > 0 — pure SO(4,1) representation theory. The trichotomy/moment-collapse arithmetic
  (V §5.2) then kills the flat-oscillatory σ_req.

The kill's load-bearing structure: **(KL-A)+(KL-C) jointly force the TAIL ITSELF to be an autonomously
positive object** — a positive measure over a rigid one-parameter basis whose members all have analytic,
non-flat pullback cuts. Positivity of the quantum state alone does NOT do this; it is positivity
*organized by dS invariance* that does.

### 2.2 The khronon admits NO KL-type representation — quantified, not just asserted [2a]

Every W_BD(Z;M²) — principal, complementary, discrete, any series — is constant on Z-level sets; so is
every superposition with ANY measure (positive, signed, complex). The khronon W is not: machine scan of
the timelike region (Z ∈ [1.05, 3], full λ = η'/η range per level set):

| c_χ | min dev | median dev | max dev |
|---|---|---|---|
| 2 | 0.617 | 0.732 | 1.120 |
| 10 | 0.672 | 0.794 | 1.200 |
| 30 | 0.674 | 0.796 | 1.202 |

(dev = std_λ W/|mean_λ W| per level set — a LOWER BOUND on the relative error of the best possible
KL-type fit.) **The irreducible residual is O(1) at every c_χ > 1: V's dS-KL frame does not degrade for
the khronon — it never starts.** (KL-A) fails at the first step; (KL-C)/(KL-D) never get jurisdiction.

### 2.3 What replaces it: the two-variable spectral representation over the residual group [2b]

Homogeneity + isotropy + scale invariance (the residual E(3) ⋊ dilatation) force exactly

> **W(η,η′,r) = (1/2π²) ∫₀^∞ (dk/k) j₀(kr) Ψ(kη, kη′)**,

with the dilatation reduction F_k = k⁻³Ψ(kη, kη′) verified symbolically on the free modes ([2b] = 0).
State positivity = **Ψ is a positive-definite kernel** (rank-one Ψ = φ⊗φ̄ for a pure Gaussian state;
free vacuum φ(w) = w·e^{icw} in w = k|η|). This is Bochner–Godement over the residual group, replacing
Bros–Moschella: the spectral parameter is the E(3) Casimir k, integrated with the scale-invariant
measure dk/k, and — the decisive structural difference — **the "basis" is not a rigid one-parameter
family of representation functions: Ψ itself is dynamical data.** Positivity per-k constrains nothing
about the pullback's u → 0 class.

### 2.4 The b-family theorem (new): the stationary Deser–Levin family SURVIVES foliation breaking [2c]

STEP 1 found stationarity on the comoving geodesic. It is much stronger than that. The dilatation orbit
through comoving offset x = bη (constant velocity b relative to the khronon frame) is a uniformly
accelerated worldline, machine-verified (sympy, Christoffels computed, all identities exactly 0):

> **a = bκ, κ = H/√(1−b²) ⟹ κ² = a² + H²** — the Deser–Levin relation, with **b = a/κ**;

and the free-khronon pullback on EVERY such member is exactly

> **W_b(τ) = −H² / [16π² c_χ (c_χ² − b²) sinh²(κτ/2)]** — stationary, the EXACT conformal/DL shape,
> KMS at κ/2π, amplitude A(b) = H²/(16π²c_χ(c_χ²−b²)), b² = a²/(a²+H²).

Anchor check (machine, exact 0): at c_χ = 1 this reduces to the BANKED conformal Deser–Levin pullback
−κ²/(16π² sinh²(κτ/2)) (agentN1/agentB [A2]) via κ² = H²/(1−b²) — the b-family construction lands
exactly on the N-series' kernel where it must.

Three immediate consequences:
1. **The free khronon's tail T̂ ≡ 0** — conformal class: contact + thermal only. (N1's "one-point
   miracle" reappears as the WHOLE free khronon, not one mass point.)
2. **The (a,H)-dependence beyond κ exists** (the N1 escape realized at the free level!) **but is an
   amplitude factor only**, analytic in a² and O(1/c_χ²)-suppressed — V's a→0 analyticity wall is
   OBEYED by the free khronon, not evaded.
3. **The free khronon sits INSIDE agentF's KMS census** (it IS a κ-thermal conformal-class worldline
   bath): the census kill — not V's — already disposes of it. It cannot source μ.

Honest scope note: the b-family member is the realization whose velocity relative to the khronon frame
is locked to b = a/κ (deep-MOND b ~ 0.7 — relativistic; physical stars have v ~ 10⁻³c and live on the
ROTATING residual-group orbits, generated by dilatation + rotation, same stationarity class). The
b-family is the exact linear-acceleration stand-in matching the N-series' Deser–Levin kinematics; orbit-
class (v-dependent) corrections are O(v²/c²) and not pursued.

### 2.5 THE HONESTY CHECK — does V's kill re-enter through the worldline KMS/stationary structure? [2d]

The worldline pullback of ANY scale-invariant Gaussian state diagonalizes in the Mellin variable of the
dilatation (machine: Mellin transform of the free mode vs Γ(1−iν)(−ic)^{iν−1} to 1e-16; Planck identity
exactly 0; FT of the sinh⁻² kernel vs the residue formula to 1e-19):

> **W(τ) = (1/2π)∫dν |φ̃(ν)|² e^{−iνκτ} × norm**, i.e. worldline density
> **ρ̃(ω) = (H²/(4π²c_χκ)) |φ̃(ω/κ)|² ≥ 0** — Bochner positivity is AUTOMATIC and family-wide.
> Free member: ρ̃_free(ω) = (H²ω/(2πc_χ³κ²))/(1 − e^{−2πω/κ}) — the Planck density, detailed balance
> = KMS at κ/2π recovered spectrally.

**What the khronon does NOT escape** (the re-entry inventory, stated at full weight):
- (i) **worldline stationarity + Bochner positivity** — any candidate σ_χ must embed in a pointwise
  positive TOTAL density on every family member;
- (ii) **KMS for the free member at exactly κ/2π** — so the free khronon is a census member (agentF)
  and is dead as a μ-source for census reasons, independently of V;
- (iii) **the a²-analyticity of the stationary law at a → 0** — see [3e]: it extends to the whole
  scale-invariant khronon class; the deep-MOND onset stays unreachable and the flattening floor a_*
  (agentCC watch entry 11) is ALSO the khronon-route prediction.

**What the khronon DOES escape — the precise statement:** V's kill was never "positive spectral density
forbids σ_req." It was "dS invariance forces the TAIL to be its own positive-measure object over a rigid
basis with analytic non-flat cuts" ((KL-A)+(KL-C)+(KL-D)). At the worldline level the surviving
constraint is only **ρ̃_total = contact + thermal + tail ≥ 0 pointwise** — an inequality the σ_req-class
tail can satisfy by riding the growing positive contact density, because nothing any longer forces the
tail piece to be separately positive or to be a superposition of rigid analytic basis cuts. The
all-inverse-moments-zero tower (V §2.1(a)) becomes a statement about the SIGNED tail component alone,
which positivity of the total does not obstruct (quantified positivity window in [3d]). KMS does NOT
re-enter the kill either: V §4 already held thermality irrelevant to σ_req, and the PUMPED medium (the
only corner X2 leaves open) necessarily breaks detailed balance — the free member's KMS is precisely
what the pump must deform. **Conclusion: the escape is real, but it is the PUMPED khronon medium's
escape, not the khronon field's — the free khronon dies in the census, and Gaussian state-shaping
cannot save it ([3b]).**

## STEP 3 — Asymptotic class: the free khronon CANNOT carry σ_req; what the pump must add, pinned quantitatively

### 3.1 The free pullback's cut class: not the wrong exponent — an ABSENT object [3a]

By the b-family theorem ([2c]) the free khronon's pullback on the entire stationary family is the EXACT
conformal/Deser–Levin kernel (amplitude-rescaled). Its cut tail is therefore **identically zero** —
contact + κ-thermal structure only, the N1 one-point-miracle class. Comparison table at u → 0⁺ (ζ raw
from agentV §6, all three footings; (16π/3)^{1/4} quarantined, untouched):

| u | σ_req (fw, ζ=2.0247) | σ_req (canon, ζ=1.7881) | σ_req (hostile, ζ=2.2271) | σ_free |
|---|---|---|---|---|
| 1e-2 | 2.84e+0 | 3.25e+0 | 1.45e+0 | 0 (exactly) |
| 1e-4 | 2.73e-3 | 1.13e-2 | −6.68e-4 | 0 (exactly) |
| 1e-6 | 6.11e-19 | 1.44e-15 | 8.84e-22 | 0 (exactly) |

**The MINIMAL khronon cannot carry σ_req** — and not because its cut density is power-law/analytic
where a fourth-root essential singularity is needed (the framing the task pre-registered), but because
it has NO cut tail at all. Foliation breaking per se buys exactly one thing at the free level: the
analytic amplitude factor 1/(c_χ²−b²), O(1/c_χ²)-weak.

### 3.2 What CANNOT add it: Gaussian state-shaping, and the c_χ → ∞ corner [3b][3f]

- **Bogoliubov lemma (machine, 1e-30):** for ANY occupation/squeezing on fixed dynamics
  (|A|²−|B|² = 1), the worldline COMMUTATOR density is exactly invariant:
  |ψ̃_new(ν)|² − |ψ̃_new(−ν)|² = |φ̃(ν)|² − |φ̃(−ν)|². The soft channel reads only this odd part
  (V §1.1: the response is Im W). **State-shaping is invisible to the response: σ_χ is a DYNAMICS
  object.** The X2 pump must act as a dynamics modifier (in-medium dispersion/gain), not a state
  filler — independently re-deriving X2's active-medium statement from the worldline side.
- **Constant (scale-invariant) squeezing**, the only homogeneous option — E(3) invariance forces
  diagonal squeezing, dilatation invariance forces it k-independent — adds the cross kernel
  ∝ −sech²(κτ/2)/4c_χ² (machine: the boundary-value integral = −1/a² exactly; Taylor −1/4 + τ²/16 −
  τ⁴/96…): **ANALYTIC at τ = 0**, V's trichotomy-case-(i) shape. The |B|² piece is the time-reversed
  thermal kernel, also analytic-class. Free + any Gaussian shaping = power-law/analytic cut class only.
- **c_χ → ∞** erases the khronon's own zero-point worldline weight (∝ 1/c_χ³) and leaves the sinh⁻²
  shape untouched: decoupling, not structure. Not the missing piece.

### 3.3 What the pump must build — the required spectral fingerprint, computed [3c]

Mapping σ_req to the worldline (machine-verified: one u-integration shifts power by +5/4 and phase by
+π/4 exactly; u = H²τ²/2 at leading order): the required tail kernel is
T(τ) ∝ τ^{−3/4} e^{−ζ̃/√τ} cos(ζ̃/√τ + π/8), ζ̃ = ζ(2/H²)^{1/4}. Its frequency content — computed by a
verified contour deformation (vs direct quadrature: rel.diff ~1e-18), then fit over ω ∈ [10², 3×10⁴]:

> **Δρ̃_c(ω) ~ A·ω^{−1/3} e^{−c̃ω^{1/3}} cos(√3·c̃·ω^{1/3} + φ̃)** — one-sided (ω > 0), signed,
> **c̃ = (3/4)·2^{2/3}·ζ̃^{2/3}**, decay/oscillation ratio LOCKED at 1/√3 (the index-1/3 saddle
> diagonal — the ω-side mirror of σ_req's −π/4 diagonal in u^{−1/4}, and of V's e^{−bM^{1/3}}
> mass-space remark).

Machine vs prediction: c̃_fit = 2.1405 vs 2.1388 (ratio 1.00084); q̃_fit = −0.320 vs −1/3; phase-rate
magnitude 3.7045 vs √3c̃ = 3.7044 (ratio 1.00002; measured sign = the conjugate saddle branch in the
e^{+iωτ} convention — magnitude is the invariant statement); the subdominant component measured at
5.17e-10 vs predicted e^{−c̃ω^{1/3}} = 5.15e-10 at ω = 1000. Raw numbers, ω in units of H:

| footing | ζ (agentV raw) | c̃ |
|---|---|---|
| framework (a₀ = 9.36e-11, H_Λ) | 2.0247 | **2.1388** |
| canonical a₀ = 1.2e-10 | 1.7881 | 1.9687 |
| hostile H₀ footing | 2.2271 | 2.2790 |

So the khronon medium's pump must imprint an **index-1/3 stretched-exponential oscillatory tail on the
worldline commutator density** — i.e. on the medium's in-medium DYNAMICS (by 3.2's lemma), at
frequencies ω ≳ H with the O(1) constants above.

### 3.4 The positivity window: the required tail FITS inside worldline Bochner positivity [3d]

Minimal one-sided completion Δρ̃(ω) = θ(ω)·A·2ImD(ω) riding the free Planck density (common
normalization divided out; field-internal headroom — the PHYSICAL amplitude invoice stays with
agentI/agentX, inherited, not re-adjudicated):

> **A_max = 5.7** (binding at ω ≈ 0.5κ, where the free density is 0.52 and the tail's most-negative
> excursion is −0.091); **3 sign changes** of Im D on the grid — the oscillation, and with it the
> all-inverse-moments-zero structure, survives INSIDE the window.

Caveat, stated: the binding point sits in the band-regularized region (the e^{−mτ} stand-in for V's
R(u)), so the precise A_max is band-shape-dependent; the structural facts — finite O(1) window, binding
near ω ~ κ, exponential freedom above — are robust. **This is the quantitative non-reentry of V's kill:
the moment tower binds the signed component, positivity binds only the total, and both are satisfiable
at once.** Under dS-KL they provably were not — that is exactly the difference the broken invariance
makes.

### 3.5 Family universality + the inherited deep-MOND wall [3e]

βκ² = H² exactly (sympy, all b) ⟹ u(τ;b) = (H²τ²/2)(1 + κ²τ²/12 + …): the leading u → 0 law is
**b-independent — ONE bulk medium serves the whole Deser–Levin family with the SAME ζ**; family/band
dependence enters at relative O(κ²τ*²) (7e-3 at ω = 100H, 1.5e-5 at 10⁴H) and through the
j₀(2qb·sinh(κτ/2)) factor — which is even-entire in b, hence analytic in a² = b²κ². Consequence, at
full hostile weight: **every scale-invariant khronon-medium observable built by dominated q-integration
is analytic in a² at a = 0 — agentV's NO-KERNEL corollary (deep-MOND onset unreachable; flattening
floor a_* exists) EXTENDS to the entire khronon class.** Foliation breaking rescues the high-a
exponential tail's carrier, NOT the deep-MOND endpoint. agentCC's watch entry 11 (isolated ultra-deep
rotators) stays the decisive test for the khronon route too. The only escape is IR-divergent Ψ (the
Allen-corner analog), which destroys the stationary law itself — same trade as in V §2.2.

## STEP 4 — VERDICT

**STRUCTURALLY-CAPABLE — for the PUMPED khronon MEDIUM (the X2 object), with the matching conditions
written below; the MINIMAL/free khronon CANNOT, by machine theorem.** Both ways, full weight:

**The kill side (hostile reading first):**
1. The free khronon's fluctuation spectrum produces **exactly nothing**: zero cut tail on the entire
   stationary family ([2c]), KMS at κ/2π — a thermal census member (agentF's kill applies, V's never
   needed). Anyone hoping the khronon's own vacuum fluctuations carry σ_req is answered: NO.
2. Gaussian state-shaping (occupations, squeezing — any pump that only FILLS modes) cannot touch the
   dissipation channel ([3b], exact to 1e-30). The pump must MODIFY THE DYNAMICS — and that physics
   (the in-medium gain/dispersion profile of a Λ-pumped khronon) **does not exist in the action yet**;
   this memo pins what it must produce, it does not produce it.
3. The deep-MOND endpoint is NOT rescued: a²-analyticity at a = 0 extends to the whole scale-invariant
   khronon class ([3e]). The flattening floor a_* is now a prediction of the khronon route itself.
4. STEP 1's committed machine checks were broken (bug log above); claims survived repair, but the
   episode is recorded.

**The capability side (same weight):**
1. V's dS-KL no-go does NOT re-enter: the khronon Wightman admits NO KL-type representation over the
   principal/complementary series — O(1) irreducible residual, any measure class ([2a]) — and its
   replacement (the two-variable E(3)⋊dilatation representation, [2b]) carries positivity only as a
   per-k kernel condition with no rigid basis. The load-bearing step of V's kill (the tail as an
   autonomously positive object) has no analog. **The worldline honesty check passes:** stationarity
   and Bochner positivity survive family-wide ([2c][2d]) but bind only the TOTAL density; the
   σ_req-class signed tail embeds with O(1) headroom (A_max = 5.7, oscillation intact, [3d]). KMS
   survives only for the free member — and breaking it is precisely what X2's active medium does
   anyway.
2. The b-family theorem ([2c]) is a genuine structural gift: the Deser–Levin family is realized as
   residual-group orbits (b = a/κ exactly), so the N-series' entire stationary-worldline machinery
   transfers to the khronon medium intact — the "law as a function of (a, H)" survives foliation
   breaking, with βκ² = H² making the required tail family-universal at leading order ([3e]): ONE
   bulk medium, ONE ζ, the whole RAR family.
3. **The matching conditions (the derivation is now a defined calculation):**
   - **(C1)** the pumped medium's effective scale-invariant mode dynamics must produce a worldline
     commutator-density addition Δρ̃_c(ω) ~ A ω^{−1/3} e^{−c̃ω^{1/3}} cos(√3 c̃ ω^{1/3} + φ̃), one-sided,
     with c̃ = (3/4)2^{2/3}ζ̃^{2/3} = 2.14/1.97/2.28 (fw/canon/hostile), ω in units of H;
   - **(C2)** decay/oscillation locked at 1/√3; prefactor power −1/3; phase φ̃ tied to σ_req's −π/8
     through the +π/4 integration shift ([3c](i));
   - **(C3)** amplitude window: |A| ≤ A_max ≈ 5.7 × the free-density normalization (band-shape
     dependent at the O(1) level) — and the PHYSICAL amplitude must additionally pay agentI/agentX's
     invoice (λ²⟨Q²⟩ ∝ m/H; ~10³³–10³⁵ W per L*-galaxy from the dS bath);
   - **(C4)** the SAME profile must serve all family members — automatic at leading order (βκ² = H²);
     the band shape R(u) maps onto subleading window structure;
   - **(C5)** the dynamics modification must be scale-invariant (functions of k_phys/H only — i.e.
     H-paced, Λ-pumped: the only scale available IS the dS bath's) and active/non-KMS in exactly the
     X2 sense. Gaussian state-filling is excluded as the mechanism ([3b]); the pump must enter the
     EOM.
   What remains underived is exactly one object: the scale-invariant gain/dispersion profile g(k_phys/H)
   of the Λ-pumped khronon that realizes (C1)–(C2). Nothing in this memo derives Z, a₀, or ζ — the
   construction CONSUMES agentV's σ_req; ζ = (16π/3)^{1/4} stayed quarantined and unused.

**Adjudication against the pre-registered options:** not SCOPING-OBSTRUCTED (every structural gate
checked passes or is evaded with machine numbers); not bare NEEDS-MORE (the missing structure is not
vague — it is one named function with five pinned matching conditions); **STRUCTURALLY-CAPABLE,
conditional on the pump entering the dynamics** — with the honest rider that the same analysis
HARDENS two negatives: the free khronon is dead as a carrier, and the deep-MOND flattening floor a_*
is now this route's own falsifiable signature (convergent with agentV §2.2 and agentCC's registered
decisive test).

**Chain handoff:** Link 5's carrier question sharpens from "can the khronon medium carry σ_req?" to
"derive g(k_phys/H) for the Λ-pumped khronon and check it lands in (C1)–(C5)" — a calculation, not a
scoping question. [SLOT-V]/Link-5 patch proposed accordingly; agentCC watch entry 11 gains a second
route that predicts the same floor.

## Artifacts

`agentEE_sigma_khronon.py` → `agentEE_sigma_khronon.out` (167 lines, all sections PASS, no
exceptions). Sections: [1] repaired Z-test/level-set/pullback; [2a] no-KL quantification; [2b]
residual-group representation; [2c] b-family theorem (sympy geometry + pullback, exact; c_χ=1
reduction anchored on N1's banked conformal kernel); [2d]
Mellin/Bochner worldline density (Planck identity exact; FT residue formula to 1e-19); [3a] free-vs-
required table; [3b] Bogoliubov/squeezing lemma (1e-30); [3c] contour-verified spectral transform +
saddle fits (c̃ to 8e-4, phase rate to 2e-5, subdominance to 0.4%); [3d] positivity window; [3e]
family universality + a²-analyticity inheritance; [3f] c_χ→∞; [4] verdict summary.

## Anchors (beyond STEP 1's)

- agentV_kernel_inversion.md §§1–7 (σ_req, the KL trichotomy, the a→0 no-kernel theorem, ζ raw values).
- agentX_sk_gate.md (Theorem X2 — active/pumped medium; the dS-bath invoice; the u-clocked window).
- agentU_khronon_m22.md (the khronon corner, c_χ² = O(γ/α) ≫ 1; gate 1 health).
- agentF (the KMS census the free khronon lands in); agentN1 (pullback geometry, one-point miracle);
  agentN2 (adiabatic localization); agentCC (the a_* hunt, watch entry 11).
- Bochner–Godement (positive-definite kernels on homogeneous spaces) — the residual-group replacement
  of Bros–Moschella's SO(4,1) harmonic analysis.
