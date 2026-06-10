# agentU — the khronon-framed covariant lift of Milgrom-2022: built on paper, run through the relativistic gates

*agentU, 2026-06-10. Files: `agentU_khronon_m22.py` → `.out` (all numbers below machine-generated there; §0 of the
run GATES against agentM's banked reflex numbers — 𝓐/a_J = 1.167/1.177/1.130 and the exp-tail δa☉ reproduced inside
agentM's banked ranges before any new use). Inputs read first: `agentM_milgrom2022_gauntlet.md` (the named matter
template), `DERIVATION_CHAIN.md` Links 5/6/7, `agentC_covariance_memo.md` (frame problem, conformal-collapse lemma,
Milgrom-94 license), `TOE_TRILEMMA.md` (the AeST/DEW kills were modified-GRAVITY kills), `agentE_solar_reflex.out`
(budget 2.47×10⁻¹⁵), `agentN5_freq_vs_accel.md` (corridor, p-dressing), `agentL_extended_coherence.md` (the ε∝M WEP
kill), `f4_lensing_wall.out` (40.5σ). Literature pass run BEFORE construction (§0). This is the framework-favorable
construction, so the discipline is inverted: maximum hostility applied to it; every PASS is conditional and scoped;
both a₀ footings + the hostile bath s = cH_Λ throughout. No git.*

---

## VERDICT UP FRONT

**BUILDABLE-with-named-open-gates.** Not ALREADY-EXISTS (§0: verifiably unbuilt — INSPIRE's full citing list of
2208.07073 contains no covariant lift; every published khronon/aether-MOND is a modified-GRAVITY realization).
Not DEAD-on-gate-N: no gate computed here kills it — but two gates are **structurally OPEN** (conservation/causality
and well-posedness, the same disease in two costumes, inherited verbatim from Milgrom's own flags and NOT cured by
covariantization), one gate is **FAIL-as-whole-theory by design** (lensing: the 40.5σ wall stands untouched; this
object is the matter-sector HALF of the spec's hybrid), and the frame sector pays a real, bounded, *pinned* PPN bill
with non-empty viable corners (generic corner α ≲ 8×10⁻⁷; a tuned sliver up to the α₁ ceiling 2.5×10⁻⁵ that sits
exactly at the Cherenkov edge c_S² ≈ 1 — a new mini-finding, §2). The honest summary sentence: **covariantization
buys exactly one thing — the frame problem is solved at a known, paid, survivable price — and cures nothing else;
everything that was open about M22 stays open, and everything that passed still passes.**

---

## 0. Literature pass FIRST: is this object already built? **NO — with the nearest-relative map pinned**

Searched (2026-06-10): covariant/relativistic modified inertia + aether/khronon/frame-field; Milgrom 2022
covariantizations; matter-sector aether couplings with MOND phenomenology; INSPIRE full citing list of 2208.07073
(recid 2136063, 31 citing records). **No paper covariantizes the M22 time-nonlocal inertia functional, with or
without a frame field. No paper puts the MOND nonlinearity in a u^μ-referenced worldline functional.** The flagged
near-hits, each checked and each NOT this object:

| candidate | what it actually is | why it is not this object |
|---|---|---|
| Blanchet–Marsat **1107.5264** (PRD 84, 044056) — "khronon MOND" | MOND nonlinearity in the **khronon's kinetic term**; matter geodesic | Modified **gravity** (the force sector carries MOND) — the class TOE_TRILEMMA killed at Cassini Q₂; inertia untouched |
| Flanagan **2302.14846** (2023) — khronometric MOND analyzed | Stability/consistency analysis of the Blanchet–Marsat class | Same class; key import for US: he finds the khronon gives **O(1) corrections to MOND in non-stationary systems** when its kinetic term is MOND-loaded — a failure mode our construction avoids by keeping the khronon kinetic term **canonical** (nothing nonlinear propagates), but it is the warning shot for any khronon-MOND dynamics |
| Bonetti–Barausse **1502.05554** (PRD 91, 084053) | PPN of Lorentz-violating MOND (khronometric in high-a, MOND in low-a) | Gravity-side again (AQUAL-like static limit ⇒ the Q₂ bill); their result that a **sizeable PPN-viable region exists** for khronon theories transfers to our gate 1 as supporting precedent |
| GEA (Zlosnik–Ferreira–Starkman **astro-ph/0607411**) / AeST (**2007.00082**) | Vector/scalar kinetic terms carry MOND | The banked kills (Cassini Q₂, repo-computed). Force sector. The structural contrast is the POINT of our gate 1: their aether **cannot** retreat to small couplings (it must produce MOND); ours **can** (it only supplies a frame) |
| Milgrom **2310.14334** (2023) | MI secondary predictions (EFE on WBs, vertical dynamics, weak inner-SS Galactic effect) | Explicitly nonrelativistic; strengthens the M22 phenomenology bank, builds nothing covariant |
| Luo **2602.14515** (Feb 2026) | dS-background "spectral broadening" as an MI mechanism story (quantum clock program) | Mechanism-level interpretation; no frame field, no nonlocal functional, no covariant worldline law. Framework-adjacent (dS ↔ MI!) — **watch item** for Link 5, not a construction |
| Sanders stratified theory (**astro-ph/9612099**) | Preferred-frame MOND, non-dynamical stratification | Gravity-side, non-dynamical frame (PPN-dead historically); ancestor, not instance |

Famaey–Durakovic 2025 (**2501.17006**): "No full-fledged theory of MOND as modified inertia exists" — still the
field's inventory line. Milgrom's own relativistic gesture remains "an eventual relativistic Fundamond will probably
involve modification of all parts of the action" (2208.07073, verbatim via agentM). **ALREADY-EXISTS: NO.**

---

## 1. THE CONSTRUCTION — the action, written explicitly

**Fields:** g_μν; a khronon scalar T(x) (or, variant, an independent Einstein-aether vector); point particles with
worldlines z_p^μ(τ). The frame field:

> **u_μ = −∂_μT / √(−g^{αβ} ∂_αT ∂_βT)**  (unit-timelike, future-directed, hypersurface-orthogonal by construction)

**The action:**

> S = S_EH[g] + S_u[g,T] + Σ_p S_p[z_p; g, u]
>
> S_EH = (1/16πG) ∫ √−g R    **(gravity sector: pure Einstein — no MOND function anywhere in it)**
>
> S_u = −(M_æ²/2) ∫ √−g [ α (u^ν∇_νu^μ)(u^σ∇_σu_μ) + β ∇_μu_ν∇^νu^μ + γ (∇·u)² ]
>   **(khronometric, CANONICAL — couplings (α,β,γ) in the 1711.08845 convention; small, MOND-free, bounded in §2)**
>
> S_p = −m_p c² ∫ dτ_p + S_p^MI,  with S_p^MI the Milgrom-2022 functional evaluated in the u-frame (below).

**The covariant kinematics (the content of the lift).** Along z_p^μ(τ):
- u-frame elapsed time s: **ds = −u_μ dz^μ** (= γ_w dτ, w the velocity relative to the aether);
- the reference lattice is the **u-congruence itself**: the particle's trajectory in the aether's Lagrangian
  coordinates ξ(s) — the congruence line crossed at u-time s, displacements measured with h_μν = g_μν + u_μu_ν
  on the leaves of the T-foliation;
- the **kinematic u-frame acceleration** A(s) = d²ξ/ds² (Fermi-transported; kinematic — no force content);
- Fourier content with respect to s (M22's quasi-periodic windowing): Â(ω);
- the filter, verbatim M22 (his Eqs. `v`/`shiluta`): **𝓐_u(ω) = (1/√2π) ∫ θ(ω′/ω) |Â(ω′)| dω′, θ(1) = 1**;
- **the law (EOM level, per frequency): m μ[𝓐_u(ω)/a₀] Â^μ(ω) = F̂^μ(ω)**, with μ the **exponential-tail
  (McGaugh-RAR) member** — adopting agentM's verdict that the tail, not the filter, carries everything.

**Galilean limit = M22 exactly.** With u cosmologically aligned and fields weak: s → t, ξ(s) → r(t), A → d²r/dt²,
𝓐_u → Milgrom's 𝓐. The run's section [1] sizes every term the lift ADDS: boost dressing w²/c² = 1.5×10⁻⁶ (CMB-frame
velocity), potential dressing Φ/c² ≤ 5.4×10⁻⁷, Hubble-flow terms H·v/a ≤ 3.6×10⁻³ (galaxy outskirts — the largest
anywhere) and H²r/a ≤ 3.7×10⁻⁵. **Phenomenologically inert: agentM's entire nonrelativistic battery (reflex pass
>10¹³, precession ≈ 0, SPARC 0.1950 dex baseline, WB θ(0)-EFE table, the reshaped DR4 fork) transfers to the
covariant object unchanged at the <1% level.** Hostile corollary, stated against the framework's interest: the
natural dressing O(H·v/a) ≤ 0.4% is far below the N5 corridor's p ∈ [0.069, 1] — **the lift does NOT manufacture
the frequency dressing that would rescue power-law tails; covariant M22 stays at p = 0, and the exponential tail
remains the only reflex-passing member.**

**Why u is genuinely needed (and why this evades the banked no-gos):** agentC's frame problem — a star in free fall
has zero proper acceleration; the "a" MOND needs is the acceleration relative to the cosmic rest frame, which is
first-derivative metric information the equivalence principle gauges away: **no local covariant scalar of g alone
encodes it**. u supplies BOTH missing structures at once: the covariant time direction for Milgrom's frequency
filter AND the reference congruence for the trajectory. And the **conformal-collapse lemma does not apply**: its
hypothesis is a pointwise mass function m(I[g](x)); S_p^MI is a functional of the trajectory's frequency content —
trajectory-nonlocal, exactly what Milgrom-94 licenses and what the lemma's proof cannot touch. (Equally honest:
this is also why no one has written its Cauchy theory — §3/§4.)

**Action-vs-EOM honesty (load-bearing):** M22 itself is stated at EOM level in Fourier space; the |Â(ω)|-built
functional is **time-symmetric** — an action exists in that form but reads the future. The construction above is
therefore primarily a covariant **EOM**; the causal (retarded) refinement is gate 2's open problem, not a footnote.

---

## 2. GATE 1 — the frame field's PPN bill + c_T, and the matter-coupling feedback: **PASS-in-corners (pinned), with one new pinch found**

**(a) The pure khronon/aether sector** (run section [2]; all formulas pinned to **1711.08845** Eqs. 4–14 and
**1802.04303** Eqs. 1.1–3.23):
- **c_T:** c_T² = 1/(1−β); GW170817+GRB170817A: −3×10⁻¹⁵ < c_T−1 < 7×10⁻¹⁶ ⇒ **|β| ≲ 10⁻¹⁵** (khronometric) /
  **|c_13| ≤ 10⁻¹⁵** (Einstein-aether). Imposed exactly; the construction loses nothing (the khronon kinetic term
  is canonical — β is a free small coupling, unlike AeST where the vector must work for a living).
- **Preferred frame:** α₁ = 4(α−2β)/(1−β), |α₁| < 10⁻⁴ ⇒ α ≤ 2.5×10⁻⁵; α₂ (full 1711.08845 Eq. 12 implemented)
  with |α₂| < 4×10⁻⁷. Machine scan: **generic corner α ≲ 8×10⁻⁷** (γ ≫ α; α₂ ≈ α/2 binds; c_S² = O(γ/α) ≫ 1
  Cherenkov-safe; BBN factor 1.5×10⁻² < 1/8 checked). **Tuned sliver:** at α = 2.5×10⁻⁵ the α₂ cancellation
  requires γ/α ∈ [1.0001, 1.0331] — a 3.3%-width tuning — and the run finds the whole window sits **at the vacuum-
  Cherenkov edge c_S² ∈ [1.000, 1.033]** (c_S² ≈ γ/α: below the window Cherenkov-dead, above it α₂-dead).
  *New mini-finding: the often-quoted "α up to the α₁ bound with α₂ tuned away" corner of khronometric theory is
  Cherenkov-pinched; the robust statement is the generic corner.* Either corner suffices for us.
- **Einstein-aether variant:** OMW's two surviving regions quoted verbatim (run [2]); binary pulsars post-GW shrink
  the space ~×10 (**2104.04596**) and the 2026 single-system bounds (**2605.01436**, PSR J1738+0333) tighten again —
  **bounds, not exclusion: the viable region is non-empty as of 2026-06.**
- **Strong-coupling floor (hostile, named):** the c_i → 0 retreat is not free — M_SC ≈ √α M_æ c_S^{±3/2,−1/2}
  (1711.08845 Eq. 15) must stay above the Lorentz-breaking scale M⋆ ≳ meV; their Figs. 1–3 show the surviving
  (α,γ) region explicitly. Non-empty, but α cannot be taken arbitrarily to zero with everything else fixed. The
  GR limit is **not smooth** (their words) — the frame sector is a permanent, bounded liability, not a removable one.

**(b) The matter-coupling feedback** (run section [3]; the "does L_m(u) wreck the pure-aether PPN?" question —
OMW's derivation explicitly assumes L_m independent of u^μ, their Eq. 2.3 remark, so this had to be computed, not
assumed): every operator the MI functional adds to worldline dynamics carries ε(x) = 1/μ(x)−1 or x·ε′(x); the
u-frame velocity w enters only by dressing the μ-argument at O(w²/c²). Sympy closed forms (printed in-run):
x ε′(x) = −(√x/2)e^{−√x}/(1−e^{−√x})² (exp tail); −1/(x√(1+x²)) (power tail). Numbers at the precision bodies:
- **exponential tail: identically zero** — √x ≥ 346 even at the HOSTILE footing at Saturn (the worst case is
  Saturn-hostile at 3.8×10⁻¹⁴⁹; every other entry underflows). PASS by >140 orders against |α₁| < 10⁻⁴.
- **power-law tail, honest both ways:** worst precision body (Neptune, hostile) gives 6.8×10⁻⁹ — *also* a PPN pass
  by ~4 orders. **PPN feedback kills NO μ shape; the power-law members die at the solar reflex (agentM ×6–11), not
  here.** The gate-1b PASS is tail-independent; the tail-conditionality of the whole object lives in agentM's §1.
- Pulsar strong-field channel (α̂₁): orbital x ~ 10¹² ⇒ feedback = 0. The Gupta+/2026 pulsar bounds bind only the
  pure-aether couplings, already counted in (a).
- **OPEN-minor (named computation for the build):** in deep-MOND regions the matter coupling sources δu at O(1) of
  the matter terms — the galaxy-scale u-profile (local frame tilt/drag) is uncomputed. It feeds the solar system
  only through the ε(x)-dead coupling, so it cannot move gate 1; it CAN matter for galaxy-scale kinematics and is
  on the gap list (§8).

**(c) The Cassini Q₂ structural claim, verified not assumed:** the Hees/Park Q₂ machinery constrains an anomalous
quadrupolar potential generated by the Galactic external field in AQUAL-class modified gravity. Here the Sun's
potential is Einstein-of-baryons (+ aether stress ≤ c_14 ≤ 2.5×10⁻⁵ fractional — negligible): **the Q₂ channel is
literally absent, not screened.** What MI has instead is (i) the per-planet inertia shift — exponentially dead
(table above); (ii) the Sun's reflex — agentM's channel, passed by the exp tail at 0.05–0.07× budget even hostile;
(iii) the filter-EFE θ(0)·a_gal term — which RAISES 𝓐 and pushes μ toward 1 (safe direction). Park+26's 3–15σ
class tension (**2602.17884**) binds modified gravity; its own text exempts MI by class (banked, agentC §c).
**GATE 1: PASS-in-corners** — with the corners pinned, the pinch named, and the bill permanent.

---

## 3. GATE 2 — energy-momentum conservation of a nonlocal matter action: **OPEN (structural), with the violation channel bounded and no data kill constructible**

The historical death-spot of covariant MI, treated hostilely (run section [4]):

- **Action route (time-symmetric functional): conservation is EXACT.** Diff-invariance of a nonlocal action is
  unbroken (nonlocality ≠ non-covariance; the DEW program is the published precedent class); the generalized
  Bianchi identity gives ∇_μ(T_m^{μν} + T_u^{μν}) = 0 on-shell, with the aether equation sourced by the matter
  coupling — the aether is the momentum reservoir. **But the symmetric functional reads the future: acausal**
  (pre-acceleration class pathologies). This is Milgrom's own acknowledged open flank ("Perhaps the models can be
  modified to incorporate such a requirement" — initial-state formulation), inherited verbatim.
- **Causal route (retarded kernels imposed at EOM level): the Noether guarantee is LOST.** Conservation must be
  re-derived or fails. Bounding the failure: for (quasi)periodic trajectories the past half-line already determines
  the spectrum — retarded and symmetric evaluations agree; the violation channel is confined to
  **[ε(x)] × [aperiodicity/secular fraction]**. Machine table: binary pulsar B1913+16 x = 1.1×10¹², triple
  J0337+1715 x = 1.8×10⁷, Saturn x = 7.0×10⁵ — **ε_exp = 0 at every precision energy-balance system**; wide
  binaries and galaxy outskirts sit at ε ~ 0.5, where the "violation" budget is O(the MOND effect itself) on
  secular timescales — not observable as non-conservation. **No data-side kill exists or can be built from current
  measurements.** The gate is structural: the causal version's consistency is unproven. Named route: Schwinger–
  Keldysh/in-in (the Maggiore-school precedent that retarded nonlocal EOMs can be causal and consistent,
  **1712.07066**), with the aether field as the natural momentum-balance carrier. **OPEN — and it must be said
  plainly: this is the gate at which covariant MI constructions historically die, and covariantization did
  nothing to close it. It remains the single hardest item on the build sheet.**

---

## 4. GATE 3 — the Bruneton-analog pathology check: **no singular surface exists; the genuine analog is the worldline IVP — OPEN, stated precisely**

- **The BEF singular surface does not transfer.** Its mechanism requires a *propagating field* whose non-analytic
  kinetic function F(X) is visited on both signs of X = −½(∂φ)². Here: the khronon's kinetic term is canonical
  (α, β, γ constants — nothing non-analytic propagates); ∂T is timelike *by the unit constraint* and never crosses
  null; the MOND non-analyticity (μ ~ √𝓐 at small 𝓐) lives in the **worldline functional**, reached only where a
  trajectory's total acceleration content vanishes — a condition on orbits, not a hypersurface in spacetime
  surrounding every galaxy. There is no kinetic matrix to degenerate. (This is the same structural inversion agentC
  found for DEW: the wall is a local-field-carrier theorem, and this construction carries no such field.)
- **The genuine analog, precisely:** the causality/well-posedness of the worldline law itself. The EOM
  m μ[𝓐_u(ω)/a₀] Â(ω) = F̂(ω) is a nonlinear integro-differential (functional) equation over trajectory histories:
  (i) **no initial-value formulation is known** — what data on a past half-line determine the future? (Milgrom's
  flagged gap; the Fourier-modulus form needs the whole worldline); (ii) the time-symmetric form has potential
  **pre-acceleration** (response to future force content); (iii) for quasi-periodic motion the law is well-defined
  and everything agentM computed is on that footing — the pathology risk lives in **transients/scattering**, where
  nothing has ever been solved in this class; (iv) the deep-MOND limit μ → 𝓐/a₀ sends effective inertia → 0 at
  zero acceleration content — response to small forces is the √-enhanced MOND response (the phenomenology itself,
  not a ghost), but a *proof* of stability/uniqueness in that regime exists nowhere. **OPEN — same disease as gate
  2 (one Cauchy theory would close both); no spacetime pathology of the BEF kind found to declare it DEAD.**

---

## 5. GATE 4 — lensing: **the construction does exactly nothing to photons; FAIL-as-whole-theory, DELEGATED by design**

The MI functional multiplies m; for m = 0 the worldline action is the unmodified null action ⇒ **photons follow
null geodesics of the Einstein metric sourced by baryons** (+ aether stress, bounded by the §2 corners at ≤ c_14 ~
2.5×10⁻⁵ fractional — 4+ orders below the ~×230 deep-bin phantom the lensing data demand). The banked metric-passive
wall applies UNCHANGED: **40.5σ** against baryon-only lensing on the repo's own re-measured isolated lensing RAR
(`f4_lensing_wall.out`). No covariant dressing changes this: the division of labor must be stated, not hedged —

| carried by THIS object (matter sector) | required from the PARTNER (metric sector, still missing) |
|---|---|
| SPARC/RAR dynamics at the acceleration-keyed baseline (0.1950 dex) | the lensing RAR amplitude (the 40.5σ wall; 6.8σ early/late split) |
| solar-system safety (reflex, precession, PPN feedback — all exp-dead) | clusters (~2× even in MOND) |
| WB + θ(0)-EFE phenomenology and the reshaped DR4 fork | the type-split phenomenology (agentH3's phase-fraction sign match) |
| WEP/UFF exactly (§7) | Φ = Ψ for the photon sector without wrecking c_T (the 1602.05961 §6 template) |

This is precisely DERIVATION_CHAIN Link 6 + Link 7: the construction realizes the named Link-6 template covariantly
and leaves Link 7 exactly as unrealized as it was this morning. **Anyone reading this as "the TOE's law rung is
closed" would be manufacturing; it is the matter HALF, now covariant on paper.**

---

## 6. GATE 5 — cosmology and the a₀(z) question: **background safe (pinned); the branch fork is EXPRESSIBLE, not DECIDED; both readings flagged**

- **Background:** comoving dust has zero u-frame acceleration AND zero force — the law is trivially satisfied
  (0 = 0, no deep-MOND inertia catastrophe at the background level). The aether renormalizes the Friedmann G:
  G_cos/G_N — the standard factor, BBN-bounded; checked at the generic corner (1.5×10⁻² < 1/8). PASS.
- **The a₀(z) fork (run section [6]) — both readings at full weight, per the working rule:**
  - **(a) a₀ = const** (the minimal action: a₀ a fixed coupling of the matter functional) **≡ the framework's
    pure-Λ branch**: a₀ ∝ √ρ_DE is constant for a cosmological constant — the same object. No promotion needed;
    the simplest covariant writing IS the framework-aligned one.
  - **(b) a₀(z) = (c/Z)·(∇·u)/3 = cH(z)/Z** — the khronon's only natural local scalar with the right dimension —
    **≡ the RIVAL rising branch** (the DEW α[g] ∝ H variant's analog; the reading the contested MUSE-DARK III
    measurement would favor). Machine table: ×1.79 divergence at z = 1, ×2.05×10⁴ at recombination.
  - Hostile asymmetry, stated: reading (b) widens the deep-MOND regime at recombination by 4+ orders — the CMB
    gate is much HARDER there; reading (a) inherits the repo's banked phenomenological CMB-safety flag for the
    flat/constant kernel (the bath argument), **with the honest caveat that no Boltzmann-level audit of M22 exists
    in any frame, ours included** — that audit is on the gap list for whichever reading survives.
  - The construction therefore does NOT derive the framework's branch; it makes the fork a property of one term in
    the action (a₀ vs a₀[∇·u]) — which is precisely what the BIG-SPARC/DESI/z≈3 data program adjudicates. OPEN.

---

## 7. The structural advantages (ii) and (iii), VERIFIED rather than assumed

- **(ii) WEP/composition-safety: PASS, three layers.** (1) m_p multiplies the whole worldline functional — μ(a/a₀)
  is the same function for every body: **UFF exact at the point-particle level** (M22's own delivery, carried by
  the lift since S_p^MI ∝ m_p × [trajectory geometry relative to u only]). (2) Composite bodies: internal frequency
  content enters only through the filter at ω_int/ω_orb ~ 10¹²–10²³ — any θ falling faster than y⁻¹ kills it
  (agentM's CoM machinery, unchanged). (3) **agentL's ε ∝ M kill is structurally inapplicable**: that kill rode on
  a mass-proportional bath charge (coherent N² gain = the WEP violation); here there is no bath charge — nothing
  scales with M. Numbers: MICROSCOPE (x = 8.5×10¹⁰, √x ≈ 2.9×10⁵) and LLR (x ≈ 6×10⁷) sit at ε_exp = 0 exactly;
  the differential (composition) signal is zero at ANY common acceleration by layer (1). MICROSCOPE is blind to
  this construction for the same reason it was blind in agentL — but now in the safe direction.
- **(iii) Milgrom-94 nonlocality: satisfied by construction** — the M22 functional IS strongly nonlocal; the
  covariant lift preserves it (frequency content with respect to u-time). The conformal-collapse lemma (agentC d1)
  is evaded by hypothesis-failure, not by evasion-engineering: there is no pointwise m(I(x)) anywhere in S_p^MI.

---

## 8. THE HONEST GAP LIST (what a real build must produce, in kill-order)

1. **A causal, conservation-proved EOM** (gates 2+3, one problem): a Schwinger–Keldysh/in-in derivation of the
   retarded worldline law with ∇_μT^{μν}_total = 0 on-shell, or a theorem that the symmetric form's acausality is
   confined below observability. *Status: nothing published in this class; the field's MI death-spot.*
2. **The galaxy-scale u-profile** (gate 1 residue): solve the khronon equation with the O(1) deep-MOND matter
   sourcing; check the local frame tilt against MW kinematics (the agentM MW-vertical discriminator flag lands
   here too).
3. **The Boltzmann audit** (gate 5): linear perturbations of the coupled (g, T, MI-matter) system about FRW for
   reading (a); the CMB-bath flag is phenomenological, not a calculation.
4. **The lensing partner** (gate 4): unchanged Link-7 spec — the construction sharpens the interface (the partner
   must couple to the SAME u to keep one frame; the 1602.05961 Φ = Ψ-via-u^μ template is the named candidate).
5. **The mechanism** (Link 5, untouched here): WHY the exponential tail — still the spec's open sentence; this
   construction consumes the tail as input exactly as agentM's adoption note said it would.
6. Transient/scattering solutions of the worldline law (the well-posedness probe a numerical experiment could
   start tonight: does a retarded-iterated M22 EOM converge on a scattering orbit?).

---

## 9. VERDICT (both ways, full weight)

**BUILDABLE-with-named-open-gates.** Specifically:

- **What the lift BUYS (the framework-favorable reading, earned):** the frame problem — the one thing agentC proved
  no metric-local construction can supply — is solved by a canonical khronon at a pinned, paid, survivable PPN
  price (generic corner α ≲ 8×10⁻⁷; pulsar-shrunk but non-empty as of 2026-06), and the matter-coupling feedback
  into PPN is exponentially dead (sympy closed forms + numbers, tail-independent PASS). The Cassini Q₂ channel is
  absent by architecture, not screened — the first covariant realization of the MI class evasion the trilemma
  always claimed in the abstract. Every nonrelativistic pass agentM banked transfers at <1%. WEP is exact where
  agentL's kill said worldline-bath constructions must fail. Milgrom-94 is satisfied, the conformal-collapse lemma
  evaded by hypothesis. **The trilemma's third cell ("no covariant completion exists") is now "no covariant
  completion is PUBLISHED; one is constructible on paper with two structural gates open."** That is a real state
  change of the law rung.
- **What the lift does NOT buy (the hostile reading, equally earned):** causality/conservation/well-posedness —
  the actual reasons the field has no covariant MI — are inherited open and undiminished; the construction is an
  EOM with an acausal action behind it until gap-list item 1 exists. The lensing wall is untouched at 40.5σ: this
  is HALF an object by design. The a₀(z) fork is expressible, not derived — and the khronon's most natural reading
  (∇·u) is the RIVAL branch, not the framework's. The frame sector is a permanent small liability with a
  non-smooth GR limit and a Cherenkov-pinched tuned corner. The exponential tail is consumed, not explained. And
  the whole object remains, in the repo's own language, a Bohr-rung construction: selected, not derived.
- **Scope lock:** all PASSes above are for the M22 concrete class (Eqs. `law` + `mumu` + `v`/`shiluta`, monotone
  xμ(x), θ(1) = 1, θ falling fast enough for CoM) with the exponential-tail μ, lifted with a canonical khronometric
  frame in the §2 viable corners. Power-law-μ members of the same lift pass every RELATIVISTIC gate computed here
  and remain DEAD at agentM's nonrelativistic reflex — the kill ordering matters and is preserved.

**Recommendation:** the whitepaper's missing-object spec can now cite a concrete covariant template for its matter
half (this memo + agentM's adoption note), with the two structural gates (causal EOM; u-profile) as the named
next computations — item 6 of the gap list is cheap and pre-registerable; item 1 is the field-difficulty one.

*Bug log: no result-bearing bugs this run. (i) One vestigial accumulator variable in §[3] caught on read-through
and removed; output unchanged. (ii) First-draft §[2] scan used the α₂ bound 1×10⁻⁷ from 1711.08845's Eq. 12 RHS
display; corrected to the actual PPN bound 4×10⁻⁷ (their Eq. 11) before the run — the generic corner moved
8×10⁻⁷ accordingly. (iii) Draft cited GEA as "gr-qc/0607411" — that id-class collision (gr-qc/0607055 is Bruneton)
is exactly the repo's known confusion pair; corrected to **astro-ph/0607411** on the citation audit pass.
Gates: agentM reflex ratios and exp-tail δa☉ reproduced inside banked ranges (asserted in-run).*

---

## Citations (arXiv ids, role)

| id | role |
|---|---|
| 2208.07073 | Milgrom 2022 — the matter-sector template being lifted (via agentM's gauntlet) |
| astro-ph/9303012 | Milgrom 1994 — nonlocality license (the theorem the construction satisfies) |
| 1711.08845 | Gümrükçüoğlu–Saravani–Sotiriou — khronometric/Hořava after GW170817: c_T ⇒ \|β\| ≲ 10⁻¹⁵; α₁/α₂ formulas (Eqs. 11–12); strong-coupling floor; viable region |
| 1802.04303 | Oost–Mukohyama–Wang — Einstein-aether after GW170817: \|c_13\| ≤ 10⁻¹⁵; α₁ = −4c_14; the two surviving regions (Eq. 3.23); the "L_m independent of u" assumption our gate 1b tests |
| 2104.04596 | Gupta et al. 2021 — binary pulsars + triple system post-GW: viable space shrinks ~×10, survives |
| 2605.01436 | PSR J1738+0333 timing 2026 — newest single-system strong-field æ-bounds (bounds, not exclusion) |
| 1107.5264 | Blanchet–Marsat — khronon MOND (gravity-side; the nearest relative, NOT this object) |
| 2302.14846 | Flanagan 2023 — khronometric-MOND analysis; O(1) non-stationary khronon corrections (warning shot) |
| 1502.05554 | Bonetti–Barausse — PPN of Lorentz-violating MOND: viable PPN region precedent |
| astro-ph/0607411 / 2007.00082 | GEA / AeST — the aether-carries-MOND contrast class (banked kills) |
| 2310.14334 | Milgrom 2023 — MI secondary predictions (NR; strengthens the bank) |
| 2602.14515 | Luo 2026 — dS spectral-broadening MI mechanism story (watch item, not a construction) |
| astro-ph/9612099 | Sanders — stratified preferred-frame MOND (ancestor) |
| 2602.17884 | Park–Hees–Famaey+ 2026 — Cassini Q₂; MI exempt by class (the channel this construction lacks by architecture) |
| 1712.07066 | Belgacem–Dirian–Foffa–Maggiore — retarded nonlocal EOMs causal/consistent (the gate-2 route precedent) |
| 2501.17006 | Famaey–Durakovic 2025 — "no full-fledged MI theory exists" (the inventory line this memo amends to "none PUBLISHED") |
| gr-qc/0607055 / 0705.4043 | Bruneton; Bruneton–Esposito-Farèse — the singular-surface wall (shown non-transferring, §4) |
| 1602.05961 | Khoury — the Φ = Ψ-via-u^μ lensing-partner template (gate-4 interface) |
