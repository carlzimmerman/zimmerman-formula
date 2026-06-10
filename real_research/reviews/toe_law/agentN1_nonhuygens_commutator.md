# Door I-c (the non-Huygens field escape): the massive-scalar commutator on the Deser–Levin family is NOT trajectory-blind — the tail carries (a, H) beyond κ. GATE-OPENS

*agentN1, 2026-06-10. Task (the gate question): agentF's all-orders kill of the bath-inertia mechanism rests on the
Huygens lemma for the CONFORMAL massless scalar in dS — the field commutator pulled back on any stationary
Deser–Levin worldline (proper acceleration a, Hubble H, κ = √(a²+H²)) is the universal contact term (i/2π)δ′(s),
trajectory-blind, so dissipation carries no (a,H) information beyond κ and the exact response is forced to
A(κ) + a²B(κ). The named unique field-side escape: NON-HUYGENS fields, whose Green functions have tail support
inside the light cone — exactly the region a timelike worldline samples. This doc computes the pulled-back
commutator C(s) = ⟨[φ(z(τ)), φ(z(τ−s))]⟩ on the same family for (a) the massive scalar in dS (Bunch–Davies, both
principal m > 3H/2 and complementary m < 3H/2 series) and (b) the minimally coupled massless limit (ξ = 0, m → 0,
Allen IR issue handled explicitly), and decides whether the tail breaks trajectory-blindness. Artifacts:
`agentN1_nonhuygens_commutator.py` + `.out` (sympy identities machine-verified; mpmath numerics cross-checked by
independent routes: discontinuity formula vs direct boundary values to ~10⁻¹⁰, distributional contact check to
~3×10⁻⁹, flat-space limit by three independent routes). Verdict at the end, both ways, full weight.
Units ħ = c = k_B = 1.*

## 0. The gate question, on agentF's terms
agentF's census (§2 of `agentF_nonpert_detector.md`) needs exactly two structural inputs: (i) the noise pulled
back on the family is the κ-only Deser–Levin thermal form; (ii) the dissipation kernel — the pulled-back
COMMUTATOR — is the SAME contact distribution (i/2π)δ′(s) for every (a, H). Input (ii) is the Huygens property
of the conformal field; it is what makes the exact resummed response [polynomial in a] × [κ-only functions] at
every coupling, which excludes μ_F4 = a/κ outright. **GATE-CLOSES** here would mean: the massive-field commutator,
though no longer pure contact, still depends on (a, H) only through κ — then agentF's census extends and the
non-Huygens door dies. **GATE-OPENS** means: C(s) knows a and H separately — then the census premise is false for
non-Huygens fields and the door is genuinely open (which is necessary, NOT sufficient, for an F4 mechanism).

## 1. The objects (conventions pinned, literature anchored)
dS₄, Hubble H; field mass m, curvature coupling ξ; effective mass **M² = m² + 12ξH²**; ν = √(9/4 − M²/H²)
(complementary series: ν ∈ (0, 3/2) real; principal: ν = iμ, μ = √(M²/H² − 9/4)); h± = 3/2 ± ν. The Bunch–Davies
(Euclidean) Wightman function is the Gauss hypergeometric in the embedding invariant Z = H²X·X′:
> **W(Z) = (H²/16π²) Γ(h₊)Γ(h₋) ₂F₁(h₊, h₋; 2; (1+Z)/2)**,
with the Wightman iε on the time variable. Anchors: Chernikov & Tagirov, Ann. IHP A 9, 109 (1968); Bunch & Davies,
Proc. R. Soc. A 360, 117 (1978) (pre-arXiv); Spradlin–Strominger–Volovich Les Houches lectures, arXiv:hep-th/0110007
(§4); Bros & Moschella, Rev. Math. Phys. 8, 327 (1996), arXiv:gr-qc/9511019 (maximal analyticity / boundary-value
structure used below). Worldline family: Deser & Levin, arXiv:gr-qc/9706018. Huygens-in-dS detector discussion:
arXiv:2301.08717. dS quasinormal rates: López-Ortega, arXiv:gr-qc/0605027. MMC-dS Green-function tail:
Burko–Harte–Poisson, arXiv:gr-qc/0201020 (PRD 65, 124006); tails generally: Poisson–Pound–Vega, arXiv:1102.0529.
Allen no-dS-invariant-vacuum: Allen, PRD 32, 3136 (1985); Allen & Folacci, PRD 35, 3771 (1987) (pre-arXiv).

**Pullback on the family** (re-verified symbolically, [A1]: embedding X·X = 1/H², u·u = −1, |A|² = a² exactly):
> **Z(s) = (H² cosh κs + a²)/κ² = 1 + 2β sinh²(κs/2)**, **β ≡ H²/κ² ∈ (0, 1]**,
so the hypergeometric argument is w(s) = 1 + β sinh²(κs/2) ≥ 1: every s ≠ 0 sits ON the timelike cut — the
worldline lives exactly where the tail lives. Two facts follow before any computation: (1) Z has imaginary period
2π/κ for EVERY mass ([A1]) ⇒ the pullback is KMS at the Deser–Levin temperature κ/2π regardless of m (numerically
confirmed to 10⁻²⁵ for both series, [D4]): **the temperature stays κ-only; thermality is not what breaks**.
(2) w(s) depends on the pair (κ, β) — a second invariant beyond κ exists ONLY if the function of w is non-trivial.
The conformal point is precisely where it is trivial: ν = 1/2 gives Γ(2)Γ(1)₂F₁(2,1;2;w) = 1/(1−w) and the β in
the prefactor cancels against the β in 1−w, leaving the κ-only Deser–Levin kernel −κ²/16π² sinh⁻²(κs/2) ([A2]
symbolic). That cancellation is a one-point miracle of M² = 2H²; it is the entire content of agentF's lemma.

## 2. The exact commutator (closed form, machine-verified)
C(s) is the boundary-value jump of W across the timelike cut. With the degenerate (c−a−b = −1) connection formula
for ₂F₁ — handled via the regularized function ₂F̃₁(α,β;0;y) = αβ y ₂F₁(α+1,β+1;2;y), identity machine-checked
([B1], rel. err 4.5×10⁻⁸ at c = 10⁻⁷) — the discontinuity collapses to the SAME hypergeometric at reflected
argument:
> Disc ₂F₁(h₊,h₋;2;x) = −2πi (1/4 − ν²)/(Γ(h₊)Γ(h₋)) · ₂F₁(h₊,h₋;2;1−x),  x > 1,
verified numerically against mpmath's own analytic continuation at 20 (ν, x) points across both series to
10⁻¹¹–10⁻¹⁵, with the boundary-value limit converging linearly in the regulator ([B1]). Since 1/4 − ν² = M²/H² − 2
and 1 − x(s) = (1−Z)/2 = −β sinh²(κ|s|/2), the full pulled-back commutator is, **exactly, for every (a, H, m, ξ)**:
> **C(s) = (i/2π) δ′(s) + (i/8π)(M² − 2H²) · sgn(s) · ₂F₁(3/2+ν, 3/2−ν; 2; −(H²/κ²) sinh²(κ|s|/2))**.
- **Contact term universal**: the lightcone 1/(1−w) residue is mass-independent (Hadamard), so the δ′(s)
  coefficient is the conformal one for every mass — i.e. the LOCAL part of dissipation (agentF's γ = λ²/8π and UV
  renormalization) stays trajectory-blind; all new structure is in the tail. Verified distributionally ([B3]):
  ∫C_ε(s)f(s)ds with f(0) ≠ 0 ≠ f′(0) reproduces −(1/2π)f′(0) + ∫T f to 2.3–3.4×10⁻⁸ relative (Richardson ε→0)
  for the conformal anchor AND a complementary AND a principal case — no spurious δ(s), no coefficient shift.
- **Conformal anchor (required check (i))**: M² = 2H² ⇒ tail coefficient EXACTLY zero ([A2] symbolic), and the
  distributional check returns −(1/2π)f′(0) to 2.4×10⁻⁸ ⇒ **C = (i/2π)δ′(s) reproduced exactly**. agentF's [B1–B2]
  is the special case of this formula at the blind point.
- **Two independent routes** for the tail at s > 0: direct 2 Im W(s − iε) (mpmath ₂F₁ at complex argument, the
  physical iε) vs the closed form: agreement 10⁻⁹–10⁻¹² across both series, four (a,H,m) configurations ([B2]).
- **Flat-space limit, three independent routes** ([D2]): the dS formula at H → 0 confluences to the known massive
  Pauli–Jordan tail (i m/4πρ)J₁(mρ)sgn(s), ρ = (2/a)sinh(a|s|/2): dS-at-H=0.01 vs Bessel: O(H²) agreement;
  K₁-Wightman pullback boundary value vs Bessel: 10⁻¹² (independent special-function route); first-principles
  mode integral (Abel-regularized): 2.3×10⁻³ after extrapolation — sign and normalization pinned from scratch.

## 3. THE DECISION: the tail is a genuine TWO-VARIABLE function — (a, H) enter separately
The tail's argument carries **β = H²/κ²** independently of the κ in sinh(κs/2). C(s) on the family is a function
of the pair (κ, β) ⟷ (a, H) — bijectively, since (a, H) = (κ√(1−β), κ√β). It collapses to fewer variables only at
the two measure-zero points where the ₂F₁ degenerates: **M² = 2H²** (conformal: coefficient zero — agentF's lemma)
and **M² → 0** (₂F₁(3,0;2;y) ≡ 1: constant tail, §4). For every other (m, ξ) — in particular every minimally
coupled massive scalar, both series — trajectory-blindness is BROKEN. Quantified three ways (required check (iii)):
1. **The step (leading non-κ structure, at order s⁰).** T(0⁺) = (M² − 2H²)/8π = (M² − 2κ² + 2a²)/8π:
   **∂T(0⁺)/∂a²|_κ = 1/4π exactly, mass-independent.** At fixed κ the very first tail coefficient runs with the
   trajectory; on the κ = 1, m = 0.5 family it runs from −1.75/8π (geodesic) through zero to +0.25/8π (flat):
   the dissipation kernel's memory does not even keep its sign at fixed κ ([D1]).
2. **The shape (small s, machine-verified series [C2]):**
   T(s) = (M²−2H²)/8π · sgn(s)[1 − M²s²/8 + (M²/192)(M² + 2H² − 2a²)s⁴ + O(s⁶)]:
   the s² coefficient is mass-only (a local mass-meter), and **the trajectory enters the normalized shape at s⁴**
   — in (κ, H) variables the s⁴ coefficient is (M²/192)(M² + 4H² − 2κ²), explicitly H-dependent at fixed κ.
3. **Late times (required check (ii), s ≫ 1/κ; asymptotics verified to 10⁻¹³ [C3]):**
   T → (M²−2H²)/8π · [A₋(−y)^(−h₋) + A₊(−y)^(−h₊)], A∓ = Γ(±2ν)/(Γ(3/2±ν)Γ(1/2±ν)), −y ≃ (β/4)e^(κ|s|):
   decay rates **(3/2 ∓ ν)κ** — at a = 0 these are the dS quasinormal rates H·Δ∓ (gr-qc/0605027) — with amplitude
   **(β/4)^(−h∓)** and, for the principal series, ringing whose phase carries μ·ln β: non-κ structure at every
   epoch of the kernel, not just near the cone.

**The gate table ([D1]; fixed κ = 1, fixed field m = 0.5, ξ = 0; entries 8πT(s)):** across (a, H) =
(0, 1) → (0.999, 0.045) → flat, the family crosses complementary → principal series; the tail spans a spread of
~2.0 with a SIGN FLIP at every s probed (0.5 to 8) and a dynamic range of 4×10⁴ by s = 8 (light-field slow decay
e^(−h₋κs), h₋ = 0.086 on the geodesic row, vs principal e^(−3κs/2) ringing on the near-flat rows). The conformal
control on the same family is zero to O(ε) at every (a, H) — the lemma, visible side by side with its violation.
**Small-mass expansion ([C1], error scaling 15.97/15.99 ≈ 16 = O(m⁴) per halving):**
T(s) = −(H²/4π) + (m²/8π)[1 − (2/3)g(y)] + O(m⁴), g(y) = y/(2(1−y)) − ln(1−y): for m ≪ H the deviation grows like
(m²/12π)(κs + ln(β/4)) until κs ~ 3H²/m² — an arbitrarily LONG (a,H)-marked memory for light fields.

## 4. The minimally coupled massless limit (the IR-pathological endpoint) — required item (b)
**Vacuum/regularization, stated explicitly:** the commutator is the Pauli–Jordan function — a state-INDEPENDENT
c-number fixed by the field equation and canonical commutation relations. The Allen obstruction (no dS-invariant
Fock vacuum for ξ = 0, m = 0; Allen 1985, Allen–Folacci 1987) lives entirely in the SYMMETRIC part: as m → 0 the
BD Wightman function diverges through its constant zero-mode ~ 3H⁴/(8π²m²)·(1 + O(m²)), which cancels in the
antisymmetric part. So C(s) needs no vacuum choice at all: we define the m = 0 commutator as the m → 0⁺ limit,
and any of the standard regularizations (Allen–Folacci O(4) state, BD-minus-zero-mode) gives the SAME C(s). The
limit is clean and the script verifies it is approached like m² ([D3]):
> **C_MMC(s) = (i/2π) δ′(s) − (i H²/4π) sgn(s)** — a CONSTANT tail (₂F₁(3, 0; 2; y) ≡ 1).
Checks and consequences ([D3]): retarded tail = +H²/4π·θ inside the cone — the known constant tail of the MMC dS
Green function (gr-qc/0201020); spectral density ρ(ω) = ω/2π + H²/2πω, the classic dS 1/ω IR enhancement; the
(m → 0, H → 0) limits do not commute (flat massless is Huygens; dS massless is not). **The structural surprise,
both ways:** the constant tail is H-aware but a-BLIND — at fixed H the dissipation kernel is the same for every
a (diffs ≲ 5×10⁻⁹ at m = 10⁻³ across a ∈ {0, 0.6, 3}), while at fixed κ it still breaks the κ-rule hard
(−H²/4π = −0.0796 at the geodesic vs −0.0286 at a = 0.8 vs 0 flat). So the m = 0 endpoint violates "κ-only"
across backgrounds but restores within-universe trajectory-blindness of dissipation — AND its noise sector is
exactly the Allen-pathological, state-dependent, secularly growing one. **The open door is 0 < m, not m = 0:**
for any finite mass the BD state is healthy, KMS at κ/2π holds, and both dissipation AND noise (= KMS_κ over the
now (κ,β)-dependent spectral function) carry (a, H) separately.

## 5. What this does to agentF's census — and what it does NOT do (both ways)
- **The census does not extend.** Its load-bearing premise — dissipation kernel = universal contact term — is
  FALSE for every non-Huygens field on the same worldline family: the exact memory kernel is the closed-form tail
  above, a genuine function of (κ, β). The all-orders Gaussian machinery itself survives (linear coupling still
  integrates out exactly), but the resulting quantum Langevin equation now has (a,H)-dependent memory and
  (a,H)-dependent noise spectral content; the response is no longer confined to A(κ) + a²B(κ).
- **The kinematic exclusion of μ_F4 dissolves.** agentB/F's no-go ODE forced G to be κ-only and found a pole at
  the deep-MOND point κ = H. In (κ, β) variables, μ_F4 = a/κ = √(1−β) is a SMOOTH function — regular precisely at
  a = 0 (β = 1) where the κ-only obstruction blew up. The obstruction was exactly the missing second variable;
  the tail supplies exactly that variable. From "impossible at every coupling" to "computable, undetermined".
- **NOT shown (tempering, full weight):** that any mass actually PRODUCES μ_F4. Opening ≠ mechanism. Nothing here
  reverses agentF's dynamical findings for the conformal field (anti-MOND sign everywhere, nonzero floor); whether
  the massive-field response has an inertia DEFICIT vanishing at a → 0 with high-a saturation is fully open. The
  tail also does NOT vanish at a = 0 (the geodesic dS detector already carries it), so the new structure does not
  switch on with a the way μ_F4's deviation does — though, directionally, the tail is an IR structure largest in
  the light-field corner m ≲ H and longest-lived at small κ, i.e. exactly the deep-MOND regime, and for m ≪ H the
  memory time 3H²/(m²κ) diverges: the quasi-static (adiabatic susceptibility) channel is where it accumulates.
  Heavy fields m ≫ κ, H decouple in the usual EFT sense (fast-oscillating tail → local terms in invariants):
  the door is open specifically for light fields.
- **Conformal-field verdicts untouched:** agentF's all-orders kill stands, on its own field, at full weight; so
  does agentB's λ² result and the lensing wall. The doors named in agentF §5 items 2–4 (extended detectors,
  field-level hybrid, non-stationarity) are unchanged. This doc resolves item 1 — in the OPEN direction.
- **The named next integral** (the new deciding object for Door I): re-run the exact Gaussian detector with the
  massive kernels — dissipation = (i/2π)δ′ + tail(s; κ, β), noise = coth(πω/κ) × the (κ,β)-spectral function —
  and compute m_resp(a, H) = the adiabatic acceleration-conjugate response. Concretely: the F4 test is now
  whether the dynamics selects G(κ, β) with G + a²-walk-derivative ∝ a/κ — kinematically possible for the first
  time, dynamically unproven. Sign first (deficit or excess at small a), shape second.

## 6. VERDICT (both ways, full weight)
- **GATE-OPENS.** For the massive scalar in dS (Bunch–Davies; both principal and complementary series; any
  M² ∉ {0, 2H²}), the commutator pulled back on the stationary Deser–Levin family is
  C(s) = (i/2π)δ′(s) + (i/8π)(M²−2H²) sgn(s) ₂F₁(3/2+ν, 3/2−ν; 2; −(H²/κ²)sinh²(κ|s|/2)) — exactly — and the
  tail is an irreducibly TWO-variable function of (κ, β = H²/κ²) ⟷ (a, H). Trajectory-blindness is broken:
  at fixed κ the kernel's step runs with a² at the exact mass-independent rate 1/4π and flips sign on the family;
  the shape acquires a² at s⁴; the late-time amplitude and (principal) phase carry β explicitly. The conformal
  limit M² = 2H² reproduces (i/2π)δ′(s) exactly (the validation anchor, symbolic + distributional), and the
  minimally coupled massless limit is the clean state-independent boundary case C = (i/2π)δ′ − (iH²/4π)sgn(s)
  (H-aware, a-blind, noise-side Allen pathology quarantined). **Dissipation on the Deser–Levin family DOES carry
  (a, H) information beyond κ; agentF's census does not extend to non-Huygens fields; the unique named field-side
  escape door is genuinely open.** This is framework-favorable and is stated with the same weight as the kills.
- **What would have closed the gate** (pre-stated): a massive-field commutator still reducible to a function of
  (κ, s) alone. The computation excludes it everywhere except the two degenerate points — the closure fails.
- **What stays closed/open:** the conformal-field worldline-bath mechanism stays DEAD at all orders (agentF,
  untouched); F4 as a selected effective law unaffected either way; μ_F4 remains UNREALIZED — this doc removes
  the impossibility proof, not the burden of construction. The deciding object is now the massive-kernel Langevin
  response m_resp(a, H), named in §5.
