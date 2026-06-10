# Agent L — the last mechanism loophole (collective coherence in extended bodies): the N² scaling is REAL, was already priced into the strongest banked walls, and CLOSES on all three legs of the triad (magnitude 21–28 dex; tracer universality ≥4× total scatter; solar reflex 5.3–7.9 dex)

*agentL, 2026-06-10. Task: for the dS/Deser–Levin bath the relevant field modes have wavelength ~1/κ ~ Hubble
scale, so ALL N constituents of any body sit inside ONE coherence patch and couple in phase to the IR tail.
Does the collective (superradiant-like) response scale as N² against the body's inertia ~N, giving an
effective per-mass enhancement ~N that climbs the banked magnitude walls (agentN4's ~25-order classical
q²/m wall; agentI 2c-i's 38-orders-in-β vacuum-correlator wall; agentN3's Wall-1)? Artifacts:
`agentL_extended_coherence.py` + `.out` (sympy exact two-worldline invariant; mpmath tail-variation scale;
every ledger number machine-printed; agentN3's ε₁ reproduced to <2% before any new use). Inputs read first:
`agentF_nonpert_detector.md` (the point-detector closure and its named extended-body loophole),
`agentN1_nonhuygens_commutator.md` (the exact (κ,β) two-variable tail), `agentN3_tail_scale.md` (the memory
force and Wall 1–4), `agentN4_tail_literature.md` §2 (the q²/m magnitude), `agentI_fraction_amplitude.md`
(the amplitude walls), `TOE_STATUS_AND_DOORS.md` §Door-IVb (the solar-reflex budget). Both ways at full
weight; every external bound arXiv-pinned; no coefficient claims; no git. Units ħ = c = k_B = 1 except where
SI is printed.*

---

## 0. The question, on the loophole's own terms

agentF §5 named "extended (non-point) detectors" as a residual door; agentN3 §3 noted in passing that
"coherent-body coupling (ε_body = N·ε₁) buys 10⁵⁷ for a star" and moved on. This doc does the bookkeeping
properly: (1) derive WHEN the bath-induced memory forces on N constituents add coherently (amplitude ∝ N,
force ∝ N², so ε ≡ |δm|/M gains a factor N over the single-detector wall) versus incoherently (∝ √N);
(2) run the closure ledger — what N reaches MOND-strength ε ~ O(1), and which real bodies have it;
(3) face the triad the structure meets immediately: tracer universality (the RAR is tracer-blind in the
data), the solar reflex (the Sun has the largest N in the solar system), and self-decoherence (stellar
interiors at 10⁷ K). Pre-stated honestly: a YES on (1) is framework-favorable and will be stated at full
weight even if (2)–(3) kill.

## 1. Item 1 — the coherence criterion: coherent, total-charge, and robust to internal temperature

**(a) The two-worldline invariant (exact, sympy [L1a]).** Extend agentN1's pullback to a PAIR of static-patch
worldlines separated by proper distance d (worldline A the comoving geodesic, B static at r = d):

> **P_AB(s; d) = √(1 − H²d²) · cosh(Hs)** — exactly; ΔP ≡ P_AB − P_AA = (√(1−H²d²) − 1)cosh(Hs),
> i.e. **|ΔP|/P = (Hd/c)²/2 exactly at leading order, uniformly in the lag s.**

The cross-pair memory kernel V(P_AB) differs from the CoM self-kernel V(P_AA) by a uniform P-shift of
relative size (Hd/c)²/2. The criterion for coherent addition is |ΔP · ∂ln V/∂P| ≪ 1, and the tail-variation
scale is machine-computed ([L1b]): |∂ln V/∂P| = O(0.003–0.4) across the MOND-signed corner (m/H ∈ [0.3, 1.4],
P ∈ [1.5, 10]); at the MMC endpoint (N1 §4) V = −H²/4π is CONSTANT in P, so the sensitivity is exactly zero.
**The coherence length of the dS bath is the Hubble radius, ℓ_c ≈ c/κ = 5.4 Gpc** — the loophole's premise
is true: every body from an atom (HR/c)²/2 ~ 10⁻⁷⁴ through the whole Milky Way (10⁻¹¹) sits inside one
patch ([L1c] table). For the massive in-band carriers (knee band; recorded for completeness — their tail is
anti-MOND-signed, agentN3/agentI) the criterion is d ≪ λ_C = ħ/mc: stars coherent across the whole band
(λ_C = 4 pc at the top), 50-pc clouds fragment above ~1.3×10⁻²⁵ eV, galaxies above ~2×10⁻²⁸ eV.

**(b) Coherent vs incoherent — which object couples.** The N² piece is the classical statement that a
monopole charge Q = Σq_i = βM_body/M_Pl,red couples as a whole to a field it cannot spatially resolve:
δM_body = −Q²(H²/4π)τ_eff against inertia M_body = N m₁ gives **ε_body = N·ε₁ exactly** — the relevant
object is the TOTAL charge (coherent), not the per-constituent one. The a-keying rides the CROSS-terms
(N² of them): the pair invariant P(z_i(τ), z_j(τ−s)) at the lags where the kernel discriminates
acceleration (κs ≳ 1, agentN1 §3) is governed by the CoM worldline, because internal coordinates enter only
at (HR/c)²/2 ≤ 10⁻³⁵ (star). So the collective response is CoM-acceleration-keyed with weight N² — the
loophole self-consistently evades the banked constituent-acceleration objection (per-constituent keying at
x_int ~ 10³⁰ would switch MOND off; here the N² piece cannot see the constituents at all). The incoherent
regime (separations > ℓ_c, or uncorrelated acceleration histories — e.g. opposite sides of a galactic
orbit, anti-correlated a) gives a √N zero-mean FLUCTUATION (MC control [L1c]: |Σ of 10⁴ random unit
vectors| = 105 ≈ √N), i.e. ε_incoh ~ ε₁/√N — smaller, not larger. Only full coherence helps, and full
coherence holds exactly for bound bodies.

**(c) Where coherence actually breaks** ([L1c]): (i) at ℓ_c (horizon for the dS bath — never inside a
galaxy; λ_C in-band — clouds/galaxies fragment at the top decades); (ii) at the SHARED-ACCELERATION
boundary — bodies on different orbits decohere from each other (anti-correlated a over the kernel's
discriminating lags), so the largest coherent unit is the largest common-a bound body (a star, planet,
cloud), NOT the galaxy, even though the galaxy fits inside ℓ_c; (iii) NOT at internal temperature: thermal
motion in a stellar core (T = 1.57×10⁷ K, v_th = 6.2×10⁵ m/s) depletes the charge only by the kinematic
factor (v/c)²/2 = 2.2×10⁻⁶ and the bounded displacement (≤ R) keeps internal coordinates 10³⁵× below the
kernel's resolution; the monopole Q is conserved under collisions. **Item-1 answer: YES — the forces add
coherently, the relevant charge is the total mass-tracking Q, ε_body = N·ε₁ is exact for every bound body,
and self-decoherence does not cut it down. This is the framework-favorable half, at full weight.**

## 2. Item 2 — the scaling ledger: what N closes the walls, and which bodies have it

All numbers machine-printed ([L2]); agentN3's per-nucleon ε₁ reproduced first (4.65×10⁻⁸⁶ at β_Cassini,
4.05×10⁻⁸¹ at β = 1, 2.72×10⁻⁴⁴ at q = 1/nucleon; N3 quotes 4.7/4.1/2.8 — match).

**The closure ledger (ε_body = 1):**

| coupling | N_req | mass equivalent |
|---|---|---|
| β = β_Cassini = 3.39×10⁻³ (1403.7377) | **2.15×10⁸⁵** | 3.6×10⁵⁸ kg = 1.8×10²⁸ M☉ = **1.6×10⁵ Hubble masses** |
| β = 1 (gravitational strength) | 2.47×10⁸⁰ | 4.1×10⁵³ kg = **1.85 M_Hubble** |
| q = 1/nucleon (fifth force 10³⁷× gravity, already dead) | 3.67×10⁴³ | 6.1×10¹⁶ kg = a ~35-km asteroid |

**The structural identity that decides it:** at gravitational coupling the coherent dressing is
**ε(M) = GMH/c³ = r_g/(2R_H)** — the body's Schwarzschild radius over the Hubble radius ([L2], exact;
Sun: 8.9×10⁻²⁴, the agentN4 §2 number). The coherent enhancement therefore saturates at ε = r_g/2R_H:
**MOND-strength requires r_g ~ R_H — the only "body" that closes the gap is the horizon itself.** This also
resolves the task's two named gaps: the **25-dex wall (agentN4, classical q² = Gm² self-force) is ALREADY
the Sun's own N²-coherent number** — N = 1.19×10⁵⁷ is inside it (gravitational charge is automatically
coherent; N4's "57-order Sun–proton spread" is this same N-scaling read as EP violation) — and closes only
at M_H = 2.2×10⁵³ kg (×10²³ the Sun). The **38-dex wall (agentI 2c-i, vacuum correlator) is a gap in β,
not ε**: per-nucleon it is 76.6 dex in ε, so N_req = 1.7×10⁷⁶ = 2.8×10⁴⁹ kg = 1.4×10¹⁹ M☉ — no bound body
within 12 dex of it even at cloud scale — AND its sign is anti-MOND over the whole knee band (m² > 2H²):
no N flips a sign. (The naive readings "N = 10²⁵ ⇒ a 17-gram mass" and "N = 10³⁸ ⇒ a 500-m asteroid" are
shown and corrected in `.out` [L2].) **The loophole was already priced into the banked walls everywhere it
could help; the only un-priced credit is the star-over-nucleon factor on N3's Wall 1 — 57 of 85 dex —
leaving 28.3 dex.**

**The per-body table (dS-bath channel, capped, Cassini coupling — `.out` [L2]):** Cs atom 6.1×10⁻⁸⁴;
1-μm dust grain 3.5×10⁻⁷³; MICROSCOPE test mass 1.1×10⁻⁵⁹; Moon 2.0×10⁻³⁶; Earth 1.7×10⁻³⁴; Jupiter
5.3×10⁻³²; **Sun/star 5.5×10⁻²⁹ (28.3 dex short)**; 10⁵ M☉ GMC 5.5×10⁻²⁴; 10⁷ M☉ cloud 5.5×10⁻²²
(21.3 dex short — the largest common-acceleration bound unit); MW baryons-as-one-body 3.4×10⁻¹⁸ (17.5 dex,
and a galaxy is NOT a common-a unit, §1c); the entire horizon baryon budget 1.3×10⁻⁷ (6.9 dex). **Answer to
"which bodies get MOND-strength modifications": NONE.** At β = 1 the horizon itself comes within ~2 dex —
the r_g ~ R_H tautology (de Sitter self-consistency), not a galactic mechanism, since the modification must
live on stellar-orbit worldlines and no sub-horizon body gets there. Fixing a star by coupling instead
needs β = 4.6×10¹¹ = a scalar force 4×10²³ × gravity between all unscreened bodies — over the Cassini
γ−1 budget by ×1.8×10²⁸ in ε terms. Dead on arrival, before the triad is even consulted.

## 3. Item 3 — the triad (each leg alone sufficient; run at the most charitable normalization, ε_star ≡ 1)

**(a) WEP / tracer universality — ε ∝ M_body is body-dependent inertia.** The decision tree over the
"body" convention, all branches ([L3a]):
- **Branch 1 (diffuse-HI atom unit, N = 1):** ε_HI/ε_star = 8.4×10⁻⁵⁸ — gas rotates Newtonian while stars
  orbit MONDian. Predicted tracer split in g_obs at the deep-regime radii where the RAR is measured:
  **Δlog g_obs = 0.55–1.0 dex** (g_bar = 10⁻¹¹–10⁻¹², RAR ν of 1609.05917; a₀-footing moves this < 0.06
  dex). Observed: ONE relation for HI/Hα-traced rotation and stellar tracers — total scatter 0.13 dex,
  intrinsic ~0.057 (2693 points, 1609.05917), with gas-dominated dwarfs the DEEPEST points on the same
  curve and dSph stellar-dispersion tracers on the same law (1610.08981). **4–8× the total scatter, 10–18×
  the intrinsic: killed.**
- **Branch 2 (bound-cloud unit):** ε_cloud/ε_star = 10³–10⁷ (GMCs 10⁵–10⁷ M☉) ⇒ ε > 1 = negative inertia —
  a dynamical runaway, not just a wrong number; saturating it by hand introduces a new scale and lands on
  branch 3.
- **Branch 3 (saturation at any N_sat):** a cap can only LOWER ε, never raise it — the §2 ledger stands
  (no body reaches ε = 1 at an allowed coupling), and the Sun saturates too, which is leg (b). Dead at
  every branch.
- **Quantitative side-checks:** LLR (Earth vs Moon toward the Sun, Williams–Turyshev–Boggs 2012,
  arXiv:1203.2150: Δ(m_g/m_i) = (−0.8±1.3)×10⁻¹³): at stellar calibration the Earth–Moon split is over the
  bound by **×5–×39 even on the maximally suppressed (ln x)/x profile, ×2.3×10⁷ on the flat reading** —
  a subordinate but independent kill. **MICROSCOPE (2209.15487) is BLIND** — ε(0.4 kg) ≤ 2×10⁻³¹ at this
  normalization, composition splits ~10⁻³ on top ⇒ η_pred ≲ 10⁻³⁴ vs 1.5×10⁻¹⁵ measured: stated honestly,
  lab/space WEP does not bind a mass-proportional coupling here; the kills are astrophysical.

**(b) The solar reflex — the N-scaling makes Door IVb strictly worse.** The Sun has the largest N in the
solar system (1.19×10⁵⁷, ×1048 Jupiter's) and IS the calibrating body class: ε_sun = ε_star ~ 1 by
construction. At the Sun's Jupiter-driven reflex acceleration (x = a_☉/cH_Λ = 388) the retained dressing is
ε_eff = 2.3×10⁻³–1.75×10⁻² on the N3 profile (= Wall 2 back-out) up to 1 on the flat reading, i.e. an
anomalous solar response of 4.9×10⁻¹⁰–2.1×10⁻⁷ m/s² against the agentE survival budget of 2.45×10⁻¹⁵ m/s²:
**over budget by ×2.0×10⁵–8.6×10⁷ (5.3–7.9 dex); Mars-residual equivalent 2.5×10⁵–1.1×10⁸ m vs 1.5 m
accuracy** ([L3b]; agentE's killed template was ε_sun = 3.59×10⁻⁶ at ×251 — ours sits ≥×641 above that
template). And the N-grading cannot soften it: agentE [5] measured Sun-only/full signal ratio = 1.000
(Mars) / 0.998 (Saturn) — the kill is 100% Sun-carried, so de-modifying the planets (their smaller N)
changes nothing, and GM_J absorption is independently Juno-refuted (20–1000×). The mechanism concentrates
its largest effect on precisely the body whose anomalous response is dead-bounded.

**(c) Decoherence — runs the wrong way for a rescue and the wrong way for a kill.** Derived in §1c: the
criterion is (constituent displacement over the memory time, projected on the kernel's variation scale)
≪ 1; bound motion caps the displacement at R, giving (HR/c)²/2 ≤ 10⁻¹⁶ even for 100-pc clouds, and thermal
charge depletion is (v_th/c)²/2 ~ 2×10⁻⁶ in a stellar core. **Internal temperature does not break the
coherent addition** — so (both ways) decoherence neither kills the N² premise NOR supplies the saturation
cap that branch 3 of leg (a) would need to fake universality: there is no physical N_sat below 10⁵⁷, and a
cap could only lower ε against a ledger already 21–28 dex short.

## 4. VERDICT (both ways, full weight)

**CLOSES — on all three legs, each alone sufficient; the loophole's physics is nonetheless REAL and is
recorded as such.**

- **The framework-favorable finding, first and at full weight:** the collective-coherence premise is TRUE.
  The dS bath cannot resolve sub-Hubble structure (exact two-worldline invariant: |ΔP|/P = (Hd/c)²/2), the
  monopole charge couples whole, the N² cross-terms key to the CoM acceleration (evading the banked
  constituent-incoherence objection self-consistently), internal temperature costs only (v/c)²/2 ~ 10⁻⁶,
  and ε_body = N·ε₁ is exact for every bound body from dust grains to clouds. The incoherent alternative
  (√N) is a zero-mean fluctuation and SMALLER. This is the strongest version of the extended-detector door
  that agentF §5 left open, now actually built.
- **Leg 2 (magnitude): CLOSES by 21.3–28.3 dex.** The enhancement was already priced into the strongest
  banked walls (agentN4's 25-dex classical wall IS the Sun's coherent number; agentI's 38-dex wall is in β
  and stays 76.6 dex in per-nucleon ε with an anti-MOND sign no N can flip). The genuinely new credit —
  10⁵⁷ on N3's Wall 1 — leaves a star 28.3 dex and the largest common-acceleration body (10⁷ M☉ cloud)
  21.3 dex short at the Cassini coupling. The closure identity ε = r_g/(2R_H) says it in one line: **the
  coherent dS-bath dressing reaches order unity only for a horizon-mass body.** Buying the residual by
  coupling needs β = 4.6×10¹¹ (a 4×10²³-×-gravity fifth force): dead by 28 dex against Cassini.
- **Leg 3a (universality): CLOSES.** ε ∝ M_body predicts a 0.55–1.0 dex gas-vs-star split where the data
  show one tracer-blind RAR at 0.057–0.13 dex (1609.05917, 1610.08981) — 4–18× over; the cloud-unit branch
  hits negative inertia; the saturation branch falls back to leg 2; LLR adds ×5–×2×10⁷ (1203.2150).
  MICROSCOPE is honestly blind (2209.15487) — recorded as a non-bound.
- **Leg 3b (solar reflex): CLOSES, and the loophole makes Door IVb WORSE.** The Sun is the maximal-N body
  in the system and the kill is 100% Sun-carried (agentE Sun-only ratio 1.000): ×2×10⁵–8.6×10⁷ over the
  banked budget, ≥×641 above the already-killed hostile template.
- **Leg 3c (decoherence): does NOT fire** — in either direction. No kill of the premise, no rescue of
  universality.
- **The one-line structural close:** agentN4 saw it for the classical route ("the two walls in one
  number"); this doc generalizes it to every coherent channel: **the N² gain and the WEP violation are the
  same number — collective coherence buys exactly what universality forbids, and at allowed couplings it
  buys 21–28 dex too little anyway.** The extended-body door (agentF §5 item 2), in its strongest
  (maximally coherent, CoM-keyed, decoherence-free) form, is now closed for worldline-bath mechanisms. What
  survives untouched: the field-level hybrid (Door II's lane), the kernel a₀ ∝ √ρ_DE as banked
  phenomenology, and the spec sheet (NONHUYGENS_DOOR_SYNTHESIS.md) — unchanged.
- **What would have opened it (pre-stated):** a real body within striking distance of N_req at an allowed
  coupling, a tracer-universal ε at MOND strength, or a reflex-safe profile. None of the three exists; the
  first fails by ≥21 dex, the second is forbidden by the same scaling that creates the enhancement, the
  third is excluded by the banked agentE fits at every profile reading.
- **Convention immunity ([L4]):** H_Λ vs H₀ footing moves ε₁ by ×1.2 (0.1 dex against 21–28); a₀ footing
  moves the tracer split by < 0.06 dex; agentE ran both s-footings and our exposure sits ≥×641 above the
  hostile one. Nothing here is a default-convention artifact in either direction.

**Status line for the registry:** the last mechanism loophole is closed. The bath-mechanism program's
closure (Huygens dead all orders; non-Huygens worldline dead by magnitude+scale; extended/coherent bodies
dead by magnitude+universality+reflex with the coherence physics itself CONFIRMED) is now complete across
point, composite-point, and extended detectors. The missing object remains field-level or nothing.

---

## Pin table

| id | role |
|---|---|
| 1403.7377 | Cassini \|γ−1\| ≤ 2.3×10⁻⁵ → β_C = 3.39×10⁻³ (agentN3/I convention, kept) |
| 2209.15487 | MICROSCOPE final η = [−1.5±2.3±1.5]×10⁻¹⁵ — checked, honestly BLIND at this normalization |
| 1203.2150 | Williams–Turyshev–Boggs 2012 LLR EP: Δ(m_g/m_i) = (−0.8±1.3)×10⁻¹³ (CQG 29, 184004) |
| 1609.05917 | RAR: ν-function, 2693 pts, 0.13 dex total / ~0.057 intrinsic scatter (tracer-blind data) |
| 1610.08981 | "One Law to Rule Them All": RAR extends to stellar-dispersion tracers (dSphs) |
| 1606.09251 | SPARC: HI/Hα rotation + stellar photometry (the gas-traced kinematic base) |
| gr-qc/9706018 | Deser–Levin worldline family (the pullback frame of N1/F) |
| hep-th/0110007 | BD hypergeometric W(P) used for the tail-variation scale [L1b] |
| gr-qc/0201020 | Burko–Harte–Poisson: the classical dS tail, dm/dτ = −q²H² (the 25-dex route's source) |
| 1807.06209 | Planck 2018 (H₀, Ω_b h² for the horizon baryon budget) |
| repo | `agentN3_tail_scale.md` (ε₁, Walls 1–4, the (ln x)/x profile), `agentN4_tail_literature.md` §2 (GmH/c³, 57-order spread), `agentI_fraction_amplitude.md` §2c (38-dex-in-β + sign), `agentN1_nonhuygens_commutator.md` (P(Δτ;a), the (κ,β) tail), `agentF_nonpert_detector.md` §5 (the loophole as named), `agentE_solar_reflex.out` (budget 2.45×10⁻¹⁵ m/s², Sun-only ratio 1.000, Juno 20–1000×), `TOE_STATUS_AND_DOORS.md` §Door-IVb |
