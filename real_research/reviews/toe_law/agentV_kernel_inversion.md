# agentV — THE KERNEL INVERSION: the W(Z) that produces the RAR exponential μ-tail exists explicitly, is characterized exactly (fourth-root essential singularity, oscillatory, all-moments-zero) — and is ILLEGAL as a dS-invariant Wightman function. Plus a NO-KERNEL theorem at the deep-MOND endpoint.

*agentV, 2026-06-11. Task (the inverse problem): GIVEN μ_target = the RAR-class exponential interpolating function
μ(x) = 1 − e^{−√x} (x = a/a₀; the repo's banked McGaugh-RAR μ, `agentM_milgrom2022_gauntlet.py` line `mu_rar`,
the unique member that cleared the full nonrelativistic battery — agentM §5), FIND the dS-invariant field two-point
structure W(Z) whose pullback on the Deser–Levin stationary family produces it in the adiabatic limit, and rule on
its LEGALITY. Inputs: the exact N1 pullback and commutator (agentN1), the agentB/F slot-gradient identities
(agentB notes [A2]–[A6]; agentF lemma), the N2 memory-Langevin adiabatic structure (localization, endpoint
universality), the agentF census (KMS-thermal worldline baths force A(κ)+a²B(κ) — so the required W is necessarily
NON-thermal on stationary worldlines). Artifacts: `agentV_kernel_inversion.py` → `agentV_kernel_inversion.out`
plus the addendum `agentV_exponent_extrapolation.py` → `.out` (sympy identities; mpmath forward transforms to
dps 80; exponent fits + Richardson extrapolation; LP feasibility; all numbers below marked [V·]/[X·] are
machine-generated there). Raw coefficients before comparisons throughout — no Z/6/2π feeding; the single flagged
comparison line is quarantined in §6. Pre-registered verdicts: KERNEL-EXISTS-AND-LEGAL / KERNEL-EXISTS-BUT-ILLEGAL /
NO-KERNEL. Verdict at the end, both ways, full weight. Units ħ = c = k_B = 1. Bug log, recorded not hidden:
(i) script v1 hung in mpmath (exp evaluated at doubly-exponential arguments on tanh-sinh tail nodes —
argument-reduction blowup); v2 clamps the s-integration domain analytically at u = 80 (tail < 1e-33);
(ii) the task's expected "Gaussian-decay correlator class" is corrected by the computation to the FOURTH-ROOT
(inverse-√-proper-time) flat-oscillatory class — §2.1.*

## 0. The problem, pinned

The N1 gate opened the unique field-side door: for non-Huygens fields the pulled-back dissipation kernel on the
Deser–Levin family is a genuine two-variable function of (κ, β) = (√(a²+H²), H²/κ²) — the κ-only census premise is
false, and μ-type laws become *kinematically possible* (N1 §5: "from impossible at every coupling to computable,
undetermined"). N2 built the memory Langevin equation and proved the adiabatic limit LOCALIZES: below the knee the
entire tail effect is an ordinary (a,H,field)-dependent adiabatic inertia — so the MOND shape must come from the
**adiabatic tail amplitude as a function of (a,H)**, nothing else. agentM identified WHAT that amplitude must be:
the exponential μ-tail is the only published-class member that survives the solar reflex while keeping the RAR
(the filter is inert; "the μ-tail carries everything"). DERIVATION_CHAIN Link 5 names the missing object: a
structure "producing the EXPONENTIAL μ-tail."

This doc runs the problem BACKWARDS — the inverse problem. Instead of testing candidate fields against μ, we
*solve for the field structure* demanded by the data-selected law, then ask whether that structure can be a
legitimate quantum field theory object. The three pre-registered outcomes are adjudicated in §7.

**The target, exactly.** Modified-inertia law on (quasi-)circular/stationary worldlines (Milgrom-22 reduces to it
exactly, agentM §0/§3): m_eff(a) = m·μ(a/a₀), μ(x) = 1 − e^{−√x}. Asymptotics that define the inversion:
- **High a:** μ − 1 = −e^{−√(a/a₀)} — exponentially small, with NO power-law corrections in a₀/a (the literal
  target; the empirically required content is "no power tail down to the agentE/Saturn budget" — the
  literal-vs-data distinction is adjudicated in §5.2, "the one quantitative residue").
- **Deep MOND:** μ(x) → √x as x → 0⁺ — m_eff → m√(a/a₀) → 0: the induced inertia must EAT the entire inertia at
  the geodesic, with a FOURTH-ROOT branch point in a² (√x = (a²)^{1/4}/√a₀ — non-analytic in a² at a = 0).
- The scale: a₀ = η·H with η dimensionless (kept raw; the framework's η = a₀/cH_Λ and the canonical value differ —
  both carried in §6 per the working rule).

## 1. The inversion, written explicitly (task item 1)

### 1.1 From the slot-gradient identities along the exact N1 pullback

Objects (all machine-re-verified, [V-A]):
- **Pullback** (N1 [A1]): Z(s) = (H²cosh κs + a²)/κ² = 1 + 2β sinh²(κs/2), β = H²/κ² ∈ (0,1]. Every s ≠ 0 sits on
  the timelike cut Z > 1. Define the cut variable **u ≡ Z − 1 ∈ (0,∞)** and the family variable **t ≡ 2β =
  2H²/(a²+H²) ∈ (0,2]** (t→0⁺: a→∞; t = 2: the geodesic a = 0). Jacobian: **dZ/ds = κ√(u(u+t))** ([V-A1]).
- **Slot-gradient identity** (agentB [A2]/agentF [A4], generalized to arbitrary W(Z) by N2 [A1]; re-verified
  symbolically [V-A2]): **ê·∇₁W(Z(s)) = a·(Z−1)·W′(Z)** — the force vertex carries exactly one factor of a times
  the invariant (Z−1)W′, for EVERY dS-invariant W. (Conformal check: W ∝ 1/(1−Z) gives ê·∇W = −aW, agentB's [A2].)
- **The adiabatic force** (agentB Stage-2 in-in, the same channel agentF resummed): ⟨F⟩ = −2λ² Im ∫₀^∞ ds g(s)
  ê·∇₁W(s), g(s) the detector correlator. In the **soft / charge-type limit** (Q → const — exactly the sector N2's
  carrier caveat [E6] forces on any mechanism with an astronomical knee: gapped detectors migrate the knee to Ω₀
  and kill it), g(s) → ⟨Q²⟩ real const, so only **Im W = the commutator cut density** survives — the response is
  STATE-INDEPENDENT for free fields and the noise sector drops (§5.3 returns to this). The conformal/contact part
  contributes the trajectory-blind UV constant only (agentB [D3]: gapless finite part exactly zero); the entire
  trajectory-dependent response is the TAIL integral.

Putting these together and changing variables s → u along the exact pullback ([V-A], both routes machine-matched
to ≤ 3.2e-17 relative at two (a,H) probes [V-B1]):

> **𝒦(a,H) ≡ −⟨F⟩/(aλ²) = (2⟨Q²⟩/κ) ∫₀^∞ du · √u · σ(1+u) / √(u+t)**,  **σ(Z) ≡ Im W′(Z − i0)**

— σ is the cut density of W′ across the timelike cut, the (a,H)-independent invariant object; ALL trajectory
dependence is the kernel √u/√(u+t) and the 1/κ prefactor. Equivalently, integrating by parts to the W-level cut
density T̂(u) ≡ Im W(1+u − i0) (= the N1 commutator tail up to normalization: C_tail(s) = 2i·T̂(u(s))·sgn(s);
for mass M, T̂_M(u) = (M²−2H²)/(16π)·₂F₁(3/2+ν, 3/2−ν; 2; −u/2), N1 §2) ([V-A4]; numeric route equality to
≤ 3.2e-17, [V-B2]):

> **𝒦(a,H) = −(2⟨Q²⟩/κ) ∫₀^∞ T̂(u) dν_t(u)**,  dν_t(u) = (t/2)·u^{−1/2}(u+t)^{−3/2} du — **a probability measure**
> (∫dν_t = 1 exactly, sympy [V-A4]), peaked at u ~ t.

*The induced inertia is minus a probability-weighted average of the field's commutator tail in the invariant
separation, weight centered at u ≈ t = 2H²/κ².* Three corollaries fall out before any inversion:
1. **|m_ind| ≤ (2λ²⟨Q²⟩/κ)·sup|T̂|** — amplitude bound;
2. **the t→0 (high-a) limit probes the lightcone endpoint**: 𝒦 → −(2⟨Q²⟩/κ)T̂(0⁺), and T̂(0⁺) is the
   DeWitt–Schwinger endpoint (N2 [C]: V(0⁺) = −(1/8π)[m² + (ξ−1/6)R]) — the high-a law is governed by the
   lightcone structure of the correlator;
3. **the t→2 (deep-MOND) limit probes u ~ O(1)** — invariant separations Z−1 ~ 1, i.e. worldline separations
   s ~ 1/H: the deep-MOND response is an IR property. The two asymptotics of μ live at the two ends of the cut.

### 1.2 The inversion formula

Define F(t) ≡ κ𝒦/(2⟨Q²⟩) = ∫₀^∞ ρ(u)(u+t)^{−1/2}du with **ρ(u) ≡ √u·σ(1+u)**. This is a generalized Stieltjes
transform of index 1/2. Using (u+t)^{−1/2} = π^{−1/2}∫₀^∞ dτ τ^{−1/2} e^{−(u+t)τ} ([V-A5], sympy):

> **F = ℒ_t [ π^{−1/2} τ^{−1/2} · ℒ_u[ρ](τ) ]** — a double Laplace transform.

Laplace transforms are injective ⇒ **the inversion exists and is unique** wherever it converges:

> **ρ(u) = ℒ⁻¹_τ→u [ √π τ^{1/2} · ℒ⁻¹_t→τ[F_target(t)] ]**,
> F_target(t) = (m/(2λ²⟨Q²⟩)) · κ(t) · [μ(a(t)/a₀) − 1],  κ(t) = H√(2/t), a(t) = H√(2/t − 1),

where the bare mass carries the saturated "1" of μ (reading R1; the contact/Hadamard channel is trajectory-blind —
agentF — so it CANNOT carry the deviation; the tail carries exactly μ − 1). This is task item (1): the inversion,
explicit, from the slot-gradient identities along the exact N1 pullback. The two-variable consistency note: at
fixed H the matching is a one-variable problem in t and the inversion above is exact; demanding the SAME W work
at all H with a₀ ∝ H forces the amplitude scaling λ²⟨Q²⟩ ∝ m/H (§5.4 — the agentI amplitude wall, reappearing).

## 2. The required W asymptotics (task item 2)

### 2.1 High a (t → 0): the exponential tail forces a fourth-root essential singularity with oscillation

Target: F(t) ⊃ −(mH/(√2 λ²⟨Q²⟩))·t^{−1/2}·e^{−c·t^{−1/4}}·(1 + O(t^{1/2})), with **c = 2^{1/4} η^{−1/2}**
(from √(a/a₀) = (2/t − 1)^{1/4} η^{−1/2}; the O(t^{1/2}) corrections are the (1 − t/8…) expansion, absorbed into
subleading structure). Two independent consequences, derived then machine-verified:

**(a) ALL power corrections must vanish ⇒ all inverse moments of ρ vanish ⇒ ρ must OSCILLATE.** The small-t power
series of F is F(t) ~ Σ_k binom(−1/2,k) t^k ∫₀^∞ ρ(u) u^{−1/2−k} du. The literal target has NO power series beyond
the bare-mass constant (μ−1 is purely exponential), so
> **M_k ≡ ∫₀^∞ ρ(u) u^{−1/2−k} du = 0 for every k ≥ 0** — an infinite tower of vanishing (inverse) moments.
A one-signed ρ cannot do this (every M_k would be strictly positive/negative). The density must change sign
infinitely often as u → 0⁺ — the Stieltjes-indeterminacy structure (the u → 1/u image of the classical
all-moments-zero densities e^{−x^{1/4}}sin(x^{1/4})).

**(b) The exponent class: two-layer saddle composition gives the strikingly clean result r₀ = c·e^{∓iπ/4}.**
Inverting layer 1 (ℒ⁻¹ of t^{−1/2}e^{−ct^{−1/4}}): saddle pair t* = (c/4τ)^{4/5}e^{±4πi/5}, exponent
φ(t*) = 5·4^{−4/5}c^{4/5}τ^{1/5}e^{±4πi/5} ([V-C1]: stationarity and exponent verified to ~1e-30) —
stretched-exponential decay exp(−1.3344·c^{4/5}τ^{1/5}) with oscillation, the τ^{1/5} class. Inverting layer 2
(ℒ⁻¹ of e^{−s₀τ^{1/5}}, s₀ = 5·4^{−4/5}c^{4/5}e^{∓iπ/5}): saddle τ* = (s₀/5u)^{5/4}, exponent
ψ(τ*) = −4·5^{−5/4}s₀^{5/4}u^{−1/4} = **−c·e^{∓iπ/4}·u^{−1/4}** exactly ([V-C1], verified to 1.8e-30; the moduli
compose back to c with no residue — the 4/5 and 5/4 powers cancel). Hence the required density near the lightcone:

> **ρ(u) ~ |K| · u^p · e^{−ζ u^{−1/4}} · cos(ξ u^{−1/4} + φ),  with ζ = ξ = c/√2 = 2^{−1/4} η^{−1/2}.**

The decay rate and oscillation rate in u^{−1/4} are EQUAL — the essential singularity sits exactly on the −π/4
diagonal. This phase is not decorative: it is precisely the condition that makes the all-moments-zero tower (a)
solvable. For the canonical power p = −3/2 the moment integrals collapse to Γ-functions ([V-C2], closed form:
M_k ∝ Γ(4k+4)·cos(φ + π(k+1))/(ζ√2)^{4k+4}) and **φ = π/2 kills every M_k simultaneously**:

> **ρ*(u) = u^{−3/2} e^{−ζu^{−1/4}} sin(ζu^{−1/4})** — the canonical pure solution: every inverse moment vanishes
> identically ([V-C2]: sympy closed-form zeros through k = 3; [V-C3]: direct quadrature M_k = 0 to a cancellation
> level of 1.7e-34 – 7.8e-35 of the envelope 4Γ(4k+4) for k = 0..6 — identical zeros, machine-confirmed), and its
> half-Stieltjes transform is purely exponentially small. The exact-target member's fractional tower vanishes
> equally ([V-C3]: 3.6e-36 – 8.4e-35 of envelope, k = 0..3).

**The prefactor law** (steepest descent at the kernel branch point w_b = t^{−1/4}e^{iπ/4}, which sits exactly ON
the steepest ray of e^{−ζ(1−i)w} — this is WHY the t-side exponent is purely real, √2ζ·t^{−1/4}, with no t-side
oscillation): the contribution scales as t^{p+5/8}e^{−√2ζt^{−1/4}}, i.e. **q = p + 5/8**. The exact target
(q = −1/2) therefore selects **p = −9/8 with moment-killing phase φ = −π/8** (m_k = 4k+3/2:
cos(−π/8 + 5π/8 + kπ) = 0 for all k — the tower closes for this member too, [V-C2/C3]).

**Machine verification of the forward transform** ([V-C4] + the addendum `agentV_exponent_extrapolation.{py,out}`,
the central check): F(t) = 4∫₀^∞ w^{−4p−3} e^{−ζw} cos(ζw + φ)(1+tw⁴)^{−1/2} dw (the substitution u = w^{−4}
makes the integrand smooth; the answer is exponentially smaller than the integrand — the vanishing moments
produce the cancellation; F(1e-8) = 1.14e-57 resolved at dps = 80). Results:
- **Exponent**: fitted c/(√2ζ) = 0.9914 (canonical member, ζ = 1), 0.9969 (ζ = 1.7), 0.9982 (exact-target member),
  with the local exponent sequences rising monotonically with the predicted t^{1/4} subleading deficit
  (deficit ratio per half-decade ≈ 10^{−1/8}, observed). Deep-t extrapolation (t → 1e-8, dps 80, exact-target
  member): t^{1/4}-Richardson over the last 6/8/10 slopes gives **c∞/√2 = 0.999876 / 0.999741 / 0.999457**, and
  the 4-parameter fit with the t^{1/4} term gives **c = 1.414073 vs √2 = 1.414214 (ratio 0.999901, max residual
  1.3e-3)** — the predicted exponent at the 1e-4 level. [X1]
- **Prefactor law**: q_fit = −0.4977 vs predicted −1/2 (exact-target member, 4-param fit); −0.813/−0.838 vs −7/8
  (canonical member, slower convergence, consistent). [V-C4, X1]
- **Purity**: sign(F) constant in t on every grid (no t-side oscillation — the branch point sits on the steepest
  ray, the e^{−ct^{−1/4}} is purely real), all three runs. [V-C4, X1]

**Translations of the class** (the fingerprint in each representation):
- **Invariant separation:** σ(Z) ~ (Z−1)^{−2} e^{−ζ(Z−1)^{−1/4}} sin(ζ(Z−1)^{−1/4}) near the lightcone Z→1⁺;
  W-level cut T̂(u) ~ (4/ζ)u^{−3/4}e^{−ζu^{−1/4}}sin-class (one u-integration, same exponential).
- **Proper chord / proper time:** u = (H²/2)ρ_c², so u^{−1/4} = (2/H²)^{1/4} ρ_c^{−1/2}: the correlator tail must
  vanish at the lightcone like **exp(−ζ̃/√ρ_c)** with oscillation cos(ζ̃/√ρ_c) — C^∞-FLAT at the cone (every
  Taylor coefficient zero) but not identically zero. On the worldline at short proper time s: e^{−const/√(κs)}.
  *The task's expected "Gaussian-decay" class is hereby corrected: the required class is the INVERSE-square-root
  essential singularity (flat-oscillatory), not Gaussian — recorded, not hidden.*
- **Mass/spectral space (the would-be fingerprint, §5.2):** a Källén–Lehmann-type weight reproducing this
  lightcone flatness via the large-M Bessel oscillations would need a stretched-exponential mass tail
  **ρ_KL(M) ~ exp(−b·M^{1/3})** (saddle: M* ~ ρ_c^{−3/2}, exponent ~ M*ρ_c ~ ρ_c^{−1/2} ✓) — the index-1/3
  stretched class. §5 proves no POSITIVE such weight can actually do it (the flatness requires the moment tower,
  which positivity forbids) — this is where legality dies.

### 2.2 Deep MOND (t → 2): a branch point the transform cannot have

μ → √x means m_eff(a) ~ m·(a²)^{1/4}/√(ηH) near a = 0 — a fourth-root branch point in a². But t = 2 is an
INTERIOR point of the transform's domain of analyticity: F(t) = ∫ρ(u)(u+t)^{−1/2}du is analytic in t in a
neighborhood of t = 2 whenever ∫|ρ(u)|u^{−1/2}du < ∞ — i.e. whenever the adiabatic (stationary) response at the
geodesic EXISTS at all. Since t − 2 ∝ a² near the geodesic ([V-A1]: 2 − t = 2a²/κ²), **m_ind(a) is forced to be
ANALYTIC IN a² at a = 0**: m_ind = m_ind(0) + O(a²). The value m_ind(0) can be tuned (one condition — the bath
can eat the bare mass exactly at the geodesic), but the SHAPE cannot: μ_induced − μ_induced(0) ∝ a², never √a or
a or a^{1/2}-type. Machine echo ([V-D]): for two test tails (e^{−u} and the light-field class (1+u)^{−0.3}), the
log-log slope of [E_t[T̂](2−ε) − E_t[T̂](2)] vs ε converges as **1.01049 → 1.00001** (analytic, exactly linear in
a²) vs the target's required 0.25. The only escape inside the
class is ∫|ρ|u^{−1/2}du = ∞ — non-decaying late-time correlations (the h₋ → 0 massless-minimal/Allen IR corner,
N1 §4), where the stationary adiabatic limit itself ceases to exist (N2's localization premise fails): then there
is no stationary law to match. **Either way the exact deep-MOND onset is unreachable. This is a NO-KERNEL theorem
at the a → 0 endpoint** — and it kills not just √x but EVERY non-integer power of a² (including standard
deep-MOND μ → x = √(a²)/a₀), for every W in the convergent class. It is the all-W generalization of the agentB/F
pole-at-κ=H obstruction: the κ-only no-go ODE had a pole at a = 0; the two-variable freedom moves the obstruction
but cannot remove it — analyticity in a² at the geodesic is forced by the transform itself.

**Honest scope:** the obstruction is at the strict a → 0 point. On any band a ≥ a_min > 0 (the empirical RAR band
is x ≳ 0.05, i.e. t ≤ 2 − δ) the target is analytic and the inversion of §1.2 converges: matching to arbitrary
precision on the band is possible (§3). The theorem says the LIMIT LAW is wrong: any tail-field-induced μ flattens
to const + O(a²) below some a_*, parametrically below the band — a falsifiable structural prediction of ANY
realization of this class (deep-field dwarfs/ultrafaints probe it; flagged for the watchlist, §7).

## 3. Synthesis: the required kernel exists on the physical domain (KERNEL-EXISTS)

On t ∈ (0, 2−δ] (all a > 0): the required cut density is (ρ = √u·σ(1+u); the exact-prefactor member)
> **σ_req(1+u) = N·u^{−13/8} e^{−ζu^{−1/4}} cos(ζu^{−1/4} − π/8) · [1 + R(u)]**, ζ = 2^{−1/4}η^{−1/2}
(canonical all-moments-zero demonstrator, same class, p = −3/2: σ ~ u^{−2}e^{−ζu^{−1/4}}sin(ζu^{−1/4})),
with R(u) a regular u ≳ O(1) shape correction carrying the finite-x structure of μ across the RAR band (computable
order by order from the double-Laplace inversion of §1.2; R does not alter the u→0 class, which is fixed by the
high-a tail alone), and the amplitude N fixed by m/(λ²⟨Q²⟩H) (§5.4). Convergence of the forward transform: the
u→0 essential singularity makes every moment finite; u→∞ decay is inherited from R (late-time decay h₋ > 0 class).
The kernel **exists, is explicit, and is unique** (Laplace injectivity) given the high-a tail and the band data.
What it is NOT: §5.

**[V-B] cross-checks:** s-route vs u-route equality of the transform (toy tail, rel. diff 0.0 at working
precision, two (a,H) probes); by-parts W-level vs W′-level route (rel. diff ≤ 3.2e-17); probability-measure
normalization = 1 exact (sympy, [V-A4]).

## 4. Why thermality was never an option (the census, used as a wall)

agentF's census: KMS-at-κ worldline baths (the conformal field, and by N1 [D4] the KMS property itself extends to
every massive BD field — "thermality is not what breaks") force the response A(κ) + a²B(κ) ONLY in the Huygens
case; for tails the structure is two-variable — but the STATE on stationary worldlines remains KMS at κ/2π for
every dS-invariant (BD-class) field: N1 verified the imaginary period 2π/κ for every mass to 1e-25. So the
required NON-census response cannot be sourced by the state's thermality (that is κ-only); it must be sourced by
the COMMUTATOR/tail structure — which is exactly where §1's inversion put it (the soft limit reads Im W only).
The required σ_req is therefore a statement about WHICH FIELD (which spectral content), not which temperature:
the inversion is orthogonal to the Deser–Levin thermality, as the census demands. KMS is not violated by σ_req —
it is simply irrelevant to it. The legality question is then precisely: *is there a field/state with this cut?*

## 5. LEGALITY (task item 3): the required W is NOT a Wightman function of any dS-invariant theory

### 5.1 The frame: Källén–Lehmann positivity in dS

For any dS-invariant state of any field theory (free or interacting) satisfying positivity + normal analyticity,
the two-point function decomposes with a POSITIVE measure over the unitary irreps (Bros–Moschella, Rev. Math.
Phys. 8, 327 (1996), arXiv:gr-qc/9511019; Bros–Epstein–Moschella; recent: Hogervorst–Penedones–Vaziri,
arXiv:2107.13871; Loparco–Penedones et al. on the dS KL measure positivity, arXiv:2306.00090):
> W(Z) = ∫ dρ(M²) W_BD(Z; M²), dρ ≥ 0 (principal + complementary support).
The pullback cut density is then σ(1+u) = ∫dρ(M²) σ_M(u) with σ_M the N1 closed-form cut: at the lightcone every
mass contributes a FINITE, NONZERO endpoint σ_M(0) ∝ (M² − 2H²) — analytic in u with radius O(1) at fixed M, all
u-derivatives at 0⁺ polynomial in M² ([V-E1]: (h₊)_k(h₋)_k = Π_j[(j+3/2)² − ν²] — real, and positive for large M).

### 5.2 The trichotomy (the boundary theorem)

The target requires σ to be C^∞-FLAT at u = 0 (every derivative zero — §2.1(a)) yet nonzero (the exponentially
small oscillatory part). For a positive KL measure this is impossible:

**(i) All KL moments finite** (any ρ decaying faster than every power — includes every stretched-exponential
candidate, in particular the e^{−bM^{1/3}} fingerprint class of §2.1): differentiation under the integral is
dominated (the cut's u-Taylor coefficients are (M²−2H²)·(h₊)_k(h₋)_k-weighted, and **(h₊)_k(h₋)_k =
Π_{j<k}(x + j(j+3)) > 0 for all x = M²/H² > 0** — machine-verified identity, [V-E1]), so the flatness tower
becomes moment conditions on the signed measure dν = (x−2)dρ. **And only TWO conditions are needed**: the exact
identity x(x−2) − 2(x−2) = (x−2)² ([X2]) makes the k = 0 and k = 1 conditions alone imply
0 = ∫(x−2)² dρ(x) ⇒ **ρ is supported at the single point M² = 2H²** — the conformal mass, whose tail is
identically ZERO (N1's one-point miracle). *The first two vanishing power corrections at high a already kill
every positive KL measure*; the general tower version P(x) = (x−2)Q(x)² gives the same collapse for any subset.
Machine echo ([V-E3], [X2]): the LP over 500-atom positive measures is feasible at J = 0 (one condition, min mass
0.539) and **exactly INFEASIBLE from J = 1 on**; with ε-relaxed conditions the minimal mass diverges as ε → 0
(0.026 / 0.394 / 2.61 / 29.0 at ε = 1e-1..1e-4) — approximate flatness is unboundedly costly. So in the
finite-moment class, *the only dS-invariant W whose pullback tail is flat at the lightcone is the no-tail
conformal field.* Flat-and-nonzero is unreachable. (agentF's lemma is the n = 0 germ of this statement; this is
its all-orders, all-fields closure — and it bites at order n = 1 already.)

**(ii) Some KL moment infinite** (heavy power-law mass tails): the flatness tower is not even well-posed —
σ acquires a SIGNED ALGEBRAIC singularity at u → 0 (Tauberian: positive heavy-tailed measures against the
large-M Bessel kernel produce u^γ-type terms with sign-definite coefficients fixed by the positive tail of ρ).
Machine demonstration in the flat caricature ([V-E2], spectral weight M^{−4} on [1,∞)): the lightcone expansion
comes out **σ(u) = 1.000000 − 0.666667·√u + 0.1250·u**, with the √u coefficient matching the sign-locked
closed form −C = −∫x^{−2}(1−j(x))dx = **−2/3 exactly** (positivity of 1−j = 1−2J₁(x)/x ≥ 0 locks the sign; the
+u/8 matches the Bessel series). A non-analytic term with a positivity-locked sign, never exponential flatness:
the target needs faster-than-any-power vanishing — unreachable.

**(iii) The oscillation requirement on its own:** even granting flatness, σ_req changes sign infinitely often as
u → 0⁺ with EQUAL decay/oscillation rates (the −π/4 diagonal). A positive measure ∫dρ σ_M can oscillate in u
(Bessel), but its small-u sign structure is anchored by the endpoint moments — and (i) shows two of them already
collapse the measure. The infinite prescribed-phase alternation is unreachable a fortiori.

**Causality and the commutator side:** no obstruction — σ_req specifies the cut only on Z > 1 (timelike);
a W analytic elsewhere has spacelike-vanishing commutator by construction. The required kernel violates
POSITIVITY (no state), not causality. It is a perfectly good c-number bidistribution — just not a correlation
function of any dS-invariant quantum state.

**Sign convention, pinned (and one flag for the chain).** The absolute sign here is anchored by the Quinn
self-force convention: the soft-channel force kernel is the retarded tail, G_ret-tail = −2·ImW-tail (checked
against N1's MMC retarded tail +H²/4π ⟷ ImW-tail = −H²/8π), and the classic flat-space cross-check is the
Yukawa cloud's NEGATIVE finite self-energy −q²m/8π (a deficit) with T̂_flat(0⁺) = +m²/16π > 0 — consistent with
m_ind = −(2λ²⟨Q²⟩/κ)E_t[T̂] < 0 for T̂ > 0. Under this convention the DEFICIT channel at the lightcone endpoint
is **T̂(0⁺) > 0 ⟺ M² > 2H² (the heavy side)** — which is OPPOSITE to the Link-5 chain line "the deficit channel,
m² < 2H²" (a phrasing keyed to V(0⁺) > 0; V = −2·ImW-tail, so the V-positive side is the T̂-negative side).
N2 itself left the adiabatic sign explicitly open ("the adiabatic sign remains genuinely open", N2 [C4]); the
chain line and this memo's convention disagree by exactly one sign and one of them needs correcting — FLAGGED
for the N-series reconciliation, not resolved here. Nothing in the inversion or the legality verdict depends on
it: the required class is sign-symmetric (φ → φ+π flips the overall sign; ζ, the moments tower, and the
positivity kill are unchanged).

**The one quantitative residue (named, pre-registered, not closed tonight).** The two-condition kill targets the
LITERAL exponential tail (all power corrections absent). The data are weaker: agentE/agentM kill power
corrections (a₀/a)^n at n ≤ 2 (standard-μ ×6.1–10.9, simple-μ ×3×10⁴) but a legal positive mixture with ONE
tuned condition (∫(x−2)dρ = 0 — feasible, LP min mass 0.539 [V-E3]) leaves residual corrections at the
(a₀/a)⁴-class level, far below the reflex budget. Whether such a CONFORMAL-BALANCED LEGAL MIXTURE can also fit
the RAR band shape (x ∈ [0.05, 30]) at the 0.1-dex level is a fit question this theorem does not decide. Named
follow-up: NNLS over the massive-kernel family {E_t[T̂_M]} with positive weights + the balance condition, scored
against the locked SPARC conventions + the agentE budget. If the best legal fit misses the band by ≫ scatter,
the kill extends from "the exact exponential law" to "anything RAR-grade" — full data-grade closure. (Whatever
that fit returns, the deep-MOND a → 0 flattening of §2.2 and the λ²⟨Q²⟩ ∝ m/H amplitude wall of §5.4 stand.)

### 5.3 What state/field class could carry it — the named escapes (and what they cost)

- **dS-invariant interacting fields:** killed above — interaction does not help; the KL measure stays positive.
- **dS-invariant α-vacua / Mottola–Allen:** add antipodal-image pieces W_BD(−Z); for Z > 1 the antipodal argument
  −Z < −1 lies in the analyticity domain (no cut) — the timelike cut density is UNCHANGED. Killed.
- **Squeezed / non-equilibrium / non-dS-invariant states:** for FREE fields the commutator is state-independent —
  in the soft limit (§1.1) the state drops entirely: squeezing CANNOT alter the adiabatic response carried by
  Im W. A non-invariant state can feed the response only through the NOISE channel (Im g·Re W — a gapped/finite-Ω₀
  detector), which (a) reintroduces N2's carrier caveat (the knee migrates to Ω₀: no astronomical gate), and
  (b) breaks stationarity on the family — the "law" would not be a function of a alone. Not a rescue; a different
  (and self-undermining) hypothesis. Flagged, not pursued.
- **Non-dS-invariant FIELD dynamics** (e.g. the khronon/aether sector of agentU, condensates): W is no longer a
  function of Z — the entire inversion premise (one function of one invariant) dissolves, and with it this doc's
  jurisdiction. This is the honest boundary of the theorem: it closes the *dS-invariant linear field-bath* class,
  exactly as pre-registered. The surviving mechanism space is therefore: invariance-breaking field sectors —
  which is precisely where the repo's spec (khronon-M22 matter sector, agentU) already lives. The theorem and the
  spec are consistent: what the spec needs CANNOT be a spectator dS QFT; it must be a structure that breaks dS
  invariance on the worldline's IR (a medium with its own frame — Milgrom's "ambient medium," now with a theorem
  saying the medium cannot be any invariant-state field).
- **Nonlinear φ-couplings:** products of W-pullbacks — sums/convolutions of κ-thermal and tail kernels (agentF §5);
  the flatness requirement transfers to a convolution algebra of positive-KL cuts: each factor is non-flat with
  sign-definite endpoint, and convolution cannot create C^∞-flatness from non-flat factors (endpoint coefficients
  multiply). Extends the kill structurally; stated as an argument, not a machine theorem — flagged.

### 5.4 The amplitude wall (independent, inherited)

Matching the amplitude needs λ²⟨Q²⟩ ≈ m/(H·O(1)) per body ([V-F]): the worldline charge-squared must be
cosmologically large in units of the body's mass and UNIVERSAL per unit mass (WEP), and the deep-MOND endpoint
m_eff(0) = 0 sits exactly ON N2's static-tachyon stability boundary ([D2] of N2: the response-reducing amplitude
is capped at the point where the dressed static response inverts — the target demands saturating the cap at
a = 0). The Link-5 "amplitude source outside any fraction-limited carrier's budget" wall (agentI) reappears
unchanged from the inverse direction. Even the illegal kernel, if smuggled in, must be driven at the stability
edge with gravitational-strength universal coupling.

## 6. Raw numbers, then the one quarantined comparison

Raw (machine, [V-C4]/[X1]/[V-F]; no feeding): fitted forward exponent extrapolates to c/√2ζ = 0.99990 (§2.1);
the class relation a₀ = cH/(√2 ζ²) ⟺ **ζ = 2^{−1/4}(cH/a₀)^{1/2}**. Numerically (both footings, both a₀
conventions per the working rule, [V-F]): framework a₀ = 9.36e-11 on H_Λ: η = 0.17250, **ζ = 2.0247**; canonical
a₀ = 1.2e-10: η = 0.22115, **ζ = 1.7881**; framework a₀ on the hostile H₀ footing: η = 0.14256, **ζ = 2.2271**.
The structural point (framework-favorable, stated raw): ANY fixed dimensionless ζ in the kernel class
automatically yields a₀ ∝ cH — the kernel's essential-singularity scale IS an a₀ ∝ √ρ_DE-type law; the
coefficient question "why Z = √(32π/3)" becomes "why ζ = this pure number".
**Quarantined comparison line (numerology risk, flagged as such):** on the exact framework convention η = 1/Z,
ζ = (16π/3)^{1/4} = 2.0232 identically (sympy: 2^{−1/4}√Z − (16π/3)^{1/4} = 0, [V-F]) — a re-expression of the
convention, NOT a derivation. Nothing here derives Z; the contest of Link 4 is untouched.

## 7. VERDICT (both ways, full weight — the pre-registered outcomes adjudicated)

**KERNEL-EXISTS-BUT-ILLEGAL — with a NO-KERNEL corollary at the deep-MOND endpoint. The new boundary theorem, at
full weight:**

> **THEOREM (tail-inversion boundary).** On the Deser–Levin family, the adiabatic soft-limit induced inertia of a
> linearly coupled worldline system is m_ind(a,H) = −(2λ²⟨Q²⟩/κ)·E_t[T̂] — a probability average of the field's
> invariant commutator-tail T̂ with weight peaked at Z−1 ≈ t = 2H²/κ². Then:
> **(1) [NO-KERNEL at a→0]** for every W with convergent average (the existence of the stationary adiabatic
> response at the geodesic), m_ind is analytic in a² at a = 0: NO field two-point structure — legal or not —
> produces the deep-MOND onset μ ∝ (a/a₀)^{1/2} (nor any non-integer power of a²). The deep-MOND limit is
> structurally out of reach of the entire linear field-bath class; only IR-divergent (Allen-corner) structures
> evade the premise, by destroying the stationary law itself.
> **(2) [EXISTS for the tail]** the data-selected exponential high-a structure μ−1 = −e^{−√(a/a₀)} corresponds,
> uniquely (double-Laplace injectivity), to the cut density σ_req ~ u^{−13/8}e^{−ζu^{−1/4}}cos(ζu^{−1/4}−π/8),
> ζ = 2^{−1/4}(cH/a₀)^{1/2} — a fourth-root essential singularity at the lightcone, C^∞-flat, oscillatory on the
> −π/4 diagonal, all inverse moments zero (machine: moment tower zero to 1e-34 of envelope; forward exponent
> √2ζ verified to 1.0e-4 by deep-t extrapolation; prefactor power −0.4977 vs −1/2; pure one-sign decay in t).
> Explicit, convergent, and the unique fingerprint any mechanism must imprint on the worldline.
> **(3) [ILLEGAL]** no dS-invariant Wightman two-point function — free or interacting, any mass spectrum, any
> invariant state including α-vacua — has such a cut: positive Källén–Lehmann measures give either analytic
> non-flat tails (finite moments: support collapses to the zero-tail conformal point — and by the identity
> x(x−2)−2(x−2) = (x−2)², the FIRST TWO vanishing power corrections suffice; LP echo exactly infeasible at J=1,
> ε-relaxed cost diverging as 1/ε) or sign-definite algebraic singularities (infinite moments; Tauberian
> sign-lock −2/3 reproduced exactly). The flat oscillatory class is unreachable. **No linear field-bath in
> dS-invariant QFT produces the data-selected exponential μ-tail.**

- **Framework-unfavorable, at full weight:** Door I's last lane (N1 opened it; N2 gated it; this doc closes its
  dS-invariant interior). The mechanism, if it exists, is NOT a spectator quantum field in any invariant state —
  Link 5's CLOSED-NEGATIVE hardens: the worldline closure now covers the tail fields at the state/spectral level,
  not just the thermal census. The deficit channel of N2 [C4] is real (one mass side gives an inertia deficit —
  sign-convention flag in §5.2) but cannot be SHAPED: single fields give analytic, non-flat tails — power-law μ
  corrections — exactly the members agentM killed on the solar reflex (×6–10⁹). The inverse problem explains WHY
  the reflex kept killing field candidates: power tails are what legal fields CAN do; the exponential tail is
  what they CANNOT.
- **Framework-favorable, same weight:** (a) the inversion produced a sharp, explicit, falsifiable fingerprint —
  σ_req with ζ = 2^{−1/4}(H/a₀)^{1/2} — and the structural identity *any O(1)-ζ kernel of this class ⇒ a₀ ∝ cH*:
  the framework's kernel law is the AUTOMATIC output of the required singularity class, independent of legality.
  (b) The theorem points all remaining force at the one door the repo already chose: dS-invariance-BREAKING media
  (khronon/condensate sectors, agentU/agentH3) — the spec is not weakened but uniquely selected: Milgrom's
  "ambient medium" must carry its own frame. (c) A new falsifiable structural prediction: any realization flattens
  μ to const + O(a²) below some a_* > 0 — the deep-MOND limit cannot be exact; ultrafaint/deep-RAR data probe a_*.
- **What would have overturned this** (pre-stated): a positive KL measure reproducing the flat oscillatory cut
  (the trichotomy closes it); a convergent transform with a fourth-root branch point at t = 2 (analyticity closes
  it); a thermal/KMS route (the census had already closed it — §4).
- **Untouched:** the effective law (Link 6: Milgrom-22 + exponential tail — selection never claimed a field-bath
  mechanism); the lensing partner (Link 7); the a₀ kernel as banked phenomenology; the N2 frequency gate (it
  remains the protection mechanism IF an invariance-breaking medium supplies the adiabatic amplitude).
- **One more structural note (frequency vs amplitude):** a mechanism realizing the exponential tail needs NO N2
  frequency knee for solar safety — the exponential μ already passes the reflex undressed (agentM: p ≡ 0 corner).
  The N2 gate and this memo's σ_req are the two INDEPENDENT protection routes (corridor-dressing vs tail-shape);
  the inversion went the tail-shape route by construction, and the data fork between them remains the WB knee
  discriminator of N2 [F8].
- **Registry handoff:** (i) [SLOT-V] in `UNIFIED_ACTION_ASSEMBLY.md` can now be patched: the mechanism fingerprint
  is σ_req (§3) with ζ = 2^{−1/4}(cH/a₀)^{1/2}, and the carrier must break dS invariance (§5.3) — the
  matter-sector construction (agentU khronon) inherits the fingerprint as its derivation target; (ii) watchlist:
  deep-RAR flattening floor a_* (ultrafaints / weak-tide dwarfs); (iii) the nonlinear-coupling convolution
  argument (§5.3 last item) named as the one not-machine-closed edge of the theorem; (iv) the SIGN flag of §5.2:
  the Link-5 chain line "deficit channel m² < 2H²" vs this memo's Quinn-anchored "deficit ⟺ M² > 2H²" — one sign
  needs reconciling in the N-series (verdicts here are sign-independent); (v) the conformal-balanced legal-mixture
  RAR band fit (§5.2, pre-registered NNLS test) — the one route by which the kill could still be softened to
  band-approximation level, or hardened to full data grade. Artifacts: `agentV_kernel_inversion.{py,out}`,
  `agentV_exponent_extrapolation.{py,out}`.

## 8. Anchors (ids verified against repo memos this session)
- In-repo: agentN1 (exact pullback + commutator closed form), agentN2 (memory Langevin, localization, endpoint
  universality, stability caps), agentF (census + soft-channel structure), agentB notes (slot-gradient identities,
  in-in static force), agentM (the target μ and its battery), DERIVATION_CHAIN Link 5/6.
- Bros & Moschella, Rev. Math. Phys. 8, 327 (1996), arXiv:gr-qc/9511019 (dS two-point functions, maximal
  analyticity, KL decomposition). Bros, Epstein & Moschella, arXiv:gr-qc/9801099 (dS KL/positivity).
- Hogervorst, Penedones & Vaziri, arXiv:2107.13871 (Hilbert space of dS QFT, KL on the unitary series);
  Loparco, Penedones, Salehi & Vaziri, arXiv:2306.00090 (positivity of the dS Källén–Lehmann density).
- Chernikov & Tagirov (1968); Bunch & Davies (1978); Spradlin–Strominger–Volovich hep-th/0110007 (BD ₂F₁ form).
- Allen, PRD 32, 3136 (1985); Allen & Folacci, PRD 35, 3771 (1987) (the IR corner named in the NO-KERNEL escape).
- Widder, *The Laplace Transform* (1941) (Stieltjes/Laplace injectivity & inversion); the classical
  all-moments-zero density e^{−x^{1/4}}sin(x^{1/4}) — Stieltjes (1894), the moment-indeterminacy example our
  σ_req mirrors under u → 1/u.
- Poisson, Pound & Vega, arXiv:1102.0529 (Hadamard tails, DeWitt–Schwinger v₀ endpoint); Burko–Harte–Poisson,
  arXiv:gr-qc/0201020 (dS constant tail).
