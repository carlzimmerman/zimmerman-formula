# agentN4: the published map of tail-induced, history-dependent inertia — enablers vs obstructions for the non-Huygens door

*agentN4, 2026-06-10. Task: map what is PUBLISHED on tail-induced, history-dependent inertia — the candidate mechanism
class for trajectory-nonlocal modified inertia (the missing object as re-specified after the six-front swarm:
`TOE_STATUS_AND_DOORS.md`, `agentF_nonpert_detector.md` §5). Five fronts: (1) the MiSaTaQuWa corpus and its dS/light-field
behavior; (2) scalar self-force in cosmological spacetimes; (3) any published tail↔MOND connection; (4) the hostile
no-gos (cosmic friction, secular drifts); (5) EP/fifth-force walls. Every claim pinned to an arXiv id where one exists
(pre-arXiv classics pinned to journal); repo-internal results cited by file. Magnitudes machine-verified:
`agentN4_tail_magnitudes.py` + `.out` (both Hubble footings throughout, per the #1 working rule). Both ways, full
weight. No git. **One id correction up front: the task's "Blanchet–Le Tiec 1110.5167" is a mathematics paper (derived
A-infinity algebras — checked); the real companions to 0901.3114 are 0804.3518 and astro-ph/0605637, used below.***

## 0. The spec the map is scored against (repo-fixed, restated quantitatively)
From `agentF` §5 (the unique bath-side escape), `MI_BATH_TAIL_CONSTRAINT.md`, `MI_COUPLING_FAMILY.md`, `agentE`:
- **S1 (structure):** a dissipation/inertia kernel that knows a and H **separately** (beyond κ = √(a²+H²)) — only
  non-Huygens fields can (agentF lemma: Huygens ⇒ kernel = (i/2π)δ′(s), trajectory-blind, all orders).
- **S2 (deep limit):** μ → a/a₀ as a → 0, a₀ ~ cH/Z (framework) to cH (bath-natural); both footings carried.
- **S3 (high-a tail):** μ − 1 = o(cH/a) — the Saturn/Folkner line (<10⁻¹⁴ m/s², via arXiv:1001.3686 §VI) falls between
  the linear (×54,000 dead) and quadratic (×4 safe) tails.
- **S4 (universality):** mass/composition-independent to ≲10⁻¹³–10⁻¹⁵ (gas vs stars trace identical RCs; §5 bounds).
- **S5 (frequency window):** deep-MOND orbits run at ω = a₀/v ≈ **190–520 H₀** (machine-checked, [3] in `.out`):
  the kernel must deliver O(1) effects at ω ~ 10²–10³ H, not only secularly at ω ≲ H.
- **S6 (magnitude):** the inertia modification is O(1), not λ²- or (q²/m)-suppressed.

---

## 1. Front 1 — the MiSaTaQuWa corpus: trajectory-nonlocal self-interaction is rigorous, covariant, textbook physics
**The existence proof for the CLASS.** The gravitational self-force on a point mass in curved spacetime is a
**tail integral over the entire past worldline**:
- Mino–Sasaki–Tanaka, **gr-qc/9606018** (PRD 55, 3457 (1997)) — matched asymptotics derivation.
- Quinn–Wald, **gr-qc/9610053** (PRD 56, 3381 (1997)) — axiomatic derivation, same equation (hence "MiSaTaQuWa").
- Quinn, **gr-qc/0005030** (PRD 62, 064029 (2000)) — the scalar-charge version used by the cosmological papers below:
  m·Du^μ/dτ = q²(δ^μ_ν + u^μu_ν)[⅙R^ν_λu^λ + ∫₀^{τ−ε}∇^νG(z(τ),z(τ′))dτ′], **dm/dτ = −q²[R/12 + u^μ∫∇_μG dτ′]** —
  the inertial mass is a dynamical, history-dependent quantity *in the equation of motion itself*.
- Poisson–Pound–Vega Living Review, **1102.0529** ("The motion of point particles in curved spacetime") — the canonical
  synthesis; Gralla–Wald **0806.3293** (rigorous derivation); Pound **1506.06245** (introduction); Casals et al.
  **0910.2634** (Green functions/tails from a spacetime perspective).
- Worldline-EFT/open-system bridge (the formal tools an N-agent action would use): Galley–Hu–Lin **gr-qc/0505085**
  (PRD 72, 084023 (2005): scalar ALD-Langevin — *dissipation + stochastic noise from field fluctuations*, the classical
  twin of agentB/agentF's machinery), Galley–Hu **0801.0900** (EMRI self-force via curved-space EFT), Galley
  **1210.2745** (PRL 110, 174301 (2013): the variational principle for generic nonconservative/history-dependent
  worldline dynamics — the action-level formalism any covariant MI candidate will be written in).

**The Huygens census (which fields have cosmological tails)** — published, and it exactly matches agentF's door list:
- **EM: NO tail in any conformally flat (FLRW) spacetime.** DeWitt–Brehme (Ann. Phys. 9, 220 (1960), corrected by
  Hobbs, Ann. Phys. 47, 141 (1968) — pre-arXiv) give the curved-space ALD equation; in FLRW the tail term vanishes
  identically by conformal invariance (stated verbatim in gr-qc/0411108 §VI; the self-force is the pure local Ricci
  term ⅓e²(δ+uu)R^ν_λu^λ). Conformally coupled massless scalars likewise (gr-qc/0411108 footnote 1).
- **Tails exist for: minimally coupled massless scalars** (below), **massive fields** (interior-cone support keyed to
  m·√σ — textbook), and **gravitons in FLRW** (gravity is not conformally invariant): Chu **1611.00018** ("More on
  cosmological gravitational waves and their memories") computes the FLRW graviton tails explicitly.
- ⇒ **The non-Huygens door's field inventory (massive / minimally-coupled-in-dS / graviton) is the complete published
  tail inventory. The door is aimed at the right and only fields.** [ENABLER]

**What is known about tails in dS for light fields — the secular/log corpus:**
- The massless minimally coupled (MMC) scalar in dS has **no dS-invariant vacuum** (Allen, PRD 32, 3136 (1985);
  Allen–Folacci, PRD 35, 3771 (1987) — pre-arXiv): the zero-mode forces secular behavior.
- ⟨φ²⟩ grows ∝ H³t until self-interaction equilibrates it at ⟨φ²⟩ ~ H⁴/m² (light mass) — Starobinsky–Yokoyama
  **astro-ph/9407016** (PRD 50, 6357 (1994), the stochastic-inflation equilibrium).
- Open-system/UDW treatments in dS: Kaplanek–Burgess **1912.12951** (accelerated qubits: thermalization, decoherence,
  *secular growth* and the limits of late-time perturbation theory) and **1912.12955** (comoving qubit in dS:
  **critical slowing down as m_eff → 0** — the Markovian window closes exactly for the light fields the door needs;
  self-interactions ⇒ secular breakdown). These are the modern, controlled statements of "light dS fields produce
  secular drifts, and perturbation theory degrades precisely in the interesting corner."
- The repo already holds the corresponding exact statement for the *Huygens* case (agentF): on the Deser–Levin family
  the conformal field's dissipation kernel is trajectory-blind at all couplings. The published dS-IR corpus does not
  contradict it — it concerns the *non-conformal* fields, where no Deser–Levin-family response computation exists.

---

## 2. Front 2 — scalar self-force in cosmological spacetimes: the inertial mass IS tail-renormalized; everything published keys to (q², H, v), never to a
**The two anchor papers** (the only exact, end-to-end cosmological self-force computations in the literature):
- Burko–Harte–Poisson, **gr-qc/0201020** (PRD 65, 124006 (2002)): a scalar point charge in expanding universes loses
  rest mass by monopole radiation. **In dS the particle radiates ALL of its mass in finite proper time**; in
  matter-dominated cosmology small charges lose then **fully recover** their mass.
- Haas–Poisson, **gr-qc/0411108** (CQG 22 (2005) S739; full text extracted for this review): the general a(η) = C|η|^α
  class, minimally coupled scalar. Load-bearing structure:
  - Reduced Green's function g = δ(η−η′−R)/R + θ(η−η′−R)·V with the **tail V in closed form** (their Table I).
    Radiation-dominated (α=1) ≡ flat: V = 0 (no tail — R=0 makes the minimal scalar conformally trivial there).
  - **dS (α=−1): V = (ηη′)⁻¹ ⇒ the tail of G is the spacetime CONSTANT H²** (our restoration via G = V/a(η)a(η′),
    C = 1/H) — a non-decaying, infinite-memory tail; the maximally non-Huygens case.
  - **Mass function (charge at rest), exact:** m(τ) = m(τ₀) − q²∫_{τ₀}^{τ−ε}G(τ,τ′)dτ′ (their Eq. 4.1) — the local
    R/12 term in dm/dτ is *exactly cancelled* by the coincidence limit of the tail (their Eq. 3.13: G(η;η−ε) = R/12),
    so the surviving mass change is the **pure history integral**. The inertia of a charge in an FLRW universe is a
    genuinely nonlocal-in-time functional. Published, exact, uncontested. [ENABLER — the structure class is real]
  - **dS row (their Table II + Fig. 2): m decreases steadily** — dm/dτ = −q²H² (our restoration of their ζ, τ₀=1/H;
    consistent with BHP's finite-time total evaporation). **The quasi-static dS tail does NOT renormalize into a
    constant local mass — it is a permanent secular drain.** [the precise crack in the "tails localize" folklore]
  - **Matter-dominated (α=2), slowly moving charge — the only published cosmological tail FORCE on a moving particle:**
    F_Ricci = +(2q²/Cη⁴)v/a² (pushes along v), F_tail = −(3q²/Cη⁴)ln(η/η₀)·v/a² (their Eqs. 5.2–5.3) — a
    **velocity-keyed force with a log-secular, initial-time-remembering coefficient**, against the kinematic
    "cosmological dragging force" −2v/η. Net published verdict (their §V–VII): **the self-force PUSHES the particle**
    (opposite to naive friction), and both charged and uncharged particles are ultimately brought to rest by the
    *kinematic* expansion drag, not by the tail.
  - **Localization answer (the task's sub-question):** static-spacetime statics localize (e.g. the EM self-force on a
    static charge in Schwarzschild–de Sitter is a closed local function — **1307.8342**); cosmological quasi-statics
    *partially* localize — for α > 0 the mass is asymptotically fully restored (the tail's net effect vanishes), for
    α ≤ −2 a **finite nonlocal relic** remains (their Eq. 4.5), and for dS the effect is secular and never localizes.
    **"Tail ⇒ local mass renormalization" is FALSE in dS; "tail ⇒ genuinely nonlocal inertia" is TRUE there — but it
    is a drift, not an a-keyed response.** [both columns of the map in one theorem-grade pair of papers]

**Magnitudes (machine-verified, `agentN4_tail_magnitudes.out`, both footings):** for a gravitational-strength charge
(q² → Gm²), the fractional tail-induced inertia change per Hubble time is **GmH/c³ ≈ 1.1×10⁻²³ (Sun), 9×10⁻⁸¹
(proton)**; the tail velocity-force is ~**10⁻³⁶ m/s²** against a₀ ≈ 10⁻¹⁰ (25 orders). And because the scale is q²/m,
**the Sun–proton spread is 57 orders**: any self-force-on-own-charge mechanism is not only ~25 orders too weak, it is
**maximally EP-violating** — the two walls in one number. [OBSTRUCTION — decisive against the *classical self-force
realization*, independent of any structural question]

---

## 3. Front 3 — the MOND connection: the inventory, and the verified absence
**Has anyone connected curved-space tails / self-force memory to MOND or a₀? — NO.** Multiple search angles
(self-force/tail/memory × MOND/dark matter/a₀; "dark matter as self-force"; tail-induced inertia) return **no published
work** deriving or even proposing MOND phenomenology from DeWitt–Brehme/MiSaTaQuWa tails. The lane is unclaimed. Both
readings owed: *priority opportunity* (the mechanism class is genuinely unexplored) AND *graveyard prior* (sixty years
of self-force literature produced magnitudes like §2's, and nobody thought the bridge worth building). [BOTH WAYS]

**The Milgrom modified-inertia chain — the worldline TARGET structure exists in print:**
- **astro-ph/9303012** (Ann. Phys. 229, 384 (1994)): the theorem — MI-MOND with Newtonian and deep-MOND limits cannot
  be local; nonlocal worldline functionals are licensed. (Already banked; the map's anchor.)
- **astro-ph/9805346** (Phys. Lett. A 253, 273 (1999)): the vacuum/Unruh proposal; its μ = F1 is the repo's
  ephemeris-dead form (×54,000, `MI_BATH_TAIL_CONSTRAINT.md`).
- **1111.1611** (Acta Phys. Pol. B 42, 2175 (2011)): "MOND–particularly as modified inertia" — the seed of:
- **2208.07073** (PRD 106, 064060 (2022)) — **the central published object: explicit time-nonlocal MI models.**
  Full text extracted for this review. Structure: in Fourier space m·â(ω)·I[{r̂},ω,a₀] = F̂(ω) with the **inertia
  functional I a dimensionless functional of the WHOLE trajectory**; concrete class I = μ(A(ω)/a₀) with a heuristic
  frequency-mixing measure A(ω) = (1/√2π)∫θ(ω′/ω)|â(ω′)|dω′ (his Eqs. 3, 5, 20). Delivered properties:
  (i) **WEP-safe by construction** (gravity ⇒ F̂ ∝ m — the nonlocality sits in a *multiplicative, mass-independent*
  functional: exactly the structure the q²/m self-force CANNOT give — the two lanes are now cleanly separated);
  (ii) conservation laws (nonlocally defined P, E, J); (iii) **the composite-body/CoM problem SOLVED by frequency
  filtering** (his Eq. 33: for the Sun-in-Galaxy both the amplitude and frequency ratios are ~10¹², so any θ(y)
  decreasing faster than y¹ suppresses the high-frequency internal term — a star MONDs even though its constituents
  are at high a); (iv) an EFE that depends on **time-averaged** external acceleration with a θ(0)~few ENHANCEMENT over
  modified-gravity EFE; (v) circular orbits reduce exactly to aμ(a/a₀) = a_N — so the repo's F4-on-circular-orbits is
  phenomenologically a member of this class (what F4 adds is a specific *derivation* of μ_standard from dT_DL/da and
  the dS anchor — that specific susceptibility form appears nowhere in 2208.07073 or anywhere else found: the
  **priority absence flagged in `MI_COUPLING_FAMILY.md` is CONFIRMED at this search depth**); (vi) **no mechanism** —
  "inertia as an acquired attribute... interaction of the body with some ambient medium, which resists acceleration,"
  pointing back to the 1999 vacuum idea; (vii) the **initial-conditions/causality problem of time-nonlocal EOMs is
  acknowledged open** (his §II A — A(ω) is not manifestly causal; "perhaps the models can be modified"). Companion:
  **2310.14334** ("MOND as manifestation of modified inertia"). Related route: **1908.01691** (PRD 100, 084039 (2019)):
  noncovariance at a < a₀ as a way to license such structures relativistically.
- **gr-qc/0601034** (PRD 73, 084005 (2006)): Milgrom's acoustic-spacetime model — **emergent inertia and passive
  gravity for a perturbation riding a background flow, WEP automatic** — the one published mechanism-flavored analog
  in which inertia is acquired from a medium. A proof-of-concept for "medium-acquired inertia," not for MOND μ(a).
- **gr-qc/0701130** (PRD 75, 065006 (2007), Obadia–Milgrom): UDW response for general (non-stationary) trajectories —
  response decays faster than any power ONLY on stationary worldlines. The published tooling for trajectory-keyed
  (frequency-content) response — the kinematic side of what a tail-kernel MI needs.

**The field-level nonlocal-MOND cousins (NOT worldline inertia — the contrast class):**
- Soussa–Woodard **astro-ph/0302030** (nonlocal pure-metric MOND; GR lensing only — insufficient) and the no-go
  **astro-ph/0307358** (stable pure-metric MOND vs lensing); Deffayet–Esposito-Farèse–Woodard **1106.4984** (nonlocal
  metric MOND *with* sufficient lensing), **1405.0393** (field equations + cosmology), Woodard review **1403.6763**;
  the 2026 descendant **2512.10513** = the DEW model the repo killed same-day at the Cassini wall (Q₂, 8.8–14.6σ;
  `agentD_dew_quadrupole.md`). Relation to tails: their nonlocality is **□⁻¹ acting on curvature invariants in field
  space** — retarded GREEN-FUNCTION nonlocality of the metric sector, not worldline-history inertia; and agentD's
  own result (static limit = exact AQUAL) is the instructive negative: **spacetime-nonlocal operators happily collapse
  to local μ(g) statics — field nonlocality does not automatically buy trajectory-keyed inertia.**
- Blanchet–Le Tiec gravitational polarization / dipolar dark matter: **astro-ph/0605637** (Blanchet: polarization
  phenomenology of MOND), **0804.3518** (the GR-based polarization model), **0901.3114** (PRD 80, 023524 (2009):
  "Dipolar Dark Matter and Dark Energy" — ΛCDM at cosmological scales + MOND at galactic scales from a polarizable DM
  medium). *(Task id 1110.5167 corrected — see header.)* Relation: this solves covariance by ADDING an aligned-dipole
  medium (dark matter with MOND phenomenology) — the **opposite move** to modified inertia; no tails, no worldline
  memory. It is the published reminder that "covariant + MONDian" is purchasable at the price of a new sector — the
  price the MI program exists to avoid.

**The a₀-from-horizon heuristics and the dead/contested vacuum-inertia attempts (the adjacents inventory):**
- Smolin **1704.00780** (PRD 96, 083523 (2017)): MOND as a quantum-gravity regime below the dS temperature; a₀ ~ √Λ
  heuristics; no kernel, no dynamics. Verlinde **1611.02269** (SciPost Phys. 2, 016 (2017)): emergent-gravity
  "apparent dark matter" with the dS-entropy a₀-scale (cH₀/6 = 1.13×10⁻¹⁰ vs canonical 1.2×10⁻¹⁰ vs framework
  cH_Λ/Z = 9.4×10⁻¹¹ — numbers in `.out` [5]; adjacency noted, no claim); nonlocal-elasticity reading **2303.14127**.
  Both are field/thermodynamic-level, not worldline MI; neither computes a tail.
- McCulloch "quantized inertia" **astro-ph/0612599** (MNRAS 376, 338 (2007)) + galactic application **1207.7007**:
  Unruh radiation + Hubble-scale Casimir cutoff ⇒ a DIFFERENCE-family μ with a **linear cH/a tail ⇒ a constant ~cH
  anomaly ⇒ Saturn-dead ×54,600–68,000 (both footings, machine-checked [4] — the same arithmetic that killed
  F1/Milgrom-99 in `MI_BATH_TAIL_CONSTRAINT.md`)**; independical skeptical analysis: Renda **1908.01589** (MNRAS 489,
  881 (2019)). Haisch–Rueda–Puthoff ZPF-inertia (PRA 49, 678 (1994) — pre-arXiv): the "all inertia from vacuum"
  ancestor, widely criticized, never produced MOND structure. Yahalom retarded-gravity rotation curves
  (**2012.04490**, **2108.08246**): claims GR retardation explains RCs via secular galactic mass depletion —
  venue-weak (MDPI), no independent verification found, relies on a dM/dt input; logged as the only "history-dependent
  gravity → rotation curves" claim in print, NOT endorsed. **Pattern across all adjacents: every concrete
  vacuum/horizon-inertia proposal that specified a kernel landed in the difference family and is ephemeris-dead;
  every survivor is kernel-free heuristics.** [OBSTRUCTION as prior, ENABLER as unclaimed specificity]

**Repo-inference flag (new, needs its own run before use):** in ANY trajectory-keyed MI reading — including
Milgrom-2022's, since the Sun's dominant frequency component carries its own A(ω_J) ≈ a_☉ ≫ a₀ — the agentE solar-reflex
channel transfers: a power-law high-x tail like μ_standard's 1/(2x²) reproduces the killed 2–3×10⁻¹⁴ m/s² solar
response, while an **exponentially-saturating μ (the McGaugh RAR form, 1−μ ~ e^{−√x} ~ 10⁻²¹ at solar x) evades it
entirely**. The μ-tail selection itself has a published modified-GRAVITY precedent — Hees–Famaey–Angus–Gentile,
**1510.01369** (MNRAS 455, 449 (2016), Milgrom-22's own ref [35]): combined solar-system + rotation-curve constraints
already exclude slow-tailed interpolating functions and select exponentially-saturating ones. The transfer of that
selection to the *modified-inertia/solar-reflex* channel is the new, unpublished part. If verified with the agentE
machinery, the solar system *selects the exponential-tail μ-class within MI* — a pre-registerable discriminant.
[flag for N2/N5; not run here]

---

## 4. Front 4 — the hostile side: what the tail of a light field in an expanding universe is PUBLISHED to do
**The question as posed: does it necessarily produce only secular drifts and ~Hv friction, never acceleration-keyed
inertia?** The published record, at full weight:
1. **Kinematic cosmic dragging (−Hv):** peculiar-velocity decay is momentum redshift — universal, force-free,
   acceleration-blind, already inside every GR calculation. It realizes "trajectory-keyed, frequency-suppressed
   damping" trivially and irrelevantly: it cannot be repurposed (no q², no a-dependence, wrong scale ~Hv).
2. **Genuine tail forces in FLRW (the only computed cases, §2):** velocity-keyed, ζ = GmH/c³-suppressed (10⁻²³, Sun),
   log-secular — and **signed as a PUSH, not a drag** (gr-qc/0411108 §VII: the naive radiative-damping expectation is
   explicitly falsified by the published computation). Magnitude vs the MOND force at a₀: short by ~25 orders ([2]).
   **The known cosmic-friction magnitude neither realizes nor structurally previews the N2/N5 object: it excludes the
   classical self-force REALIZATION (S4+S6 walls) while leaving the bath-response realization untouched** (different
   scaling: ħ-keyed response to vacuum noise, not q²-keyed reaction to own field).
3. **Friction-literature inventory:** Poynting–Robertson-type drag against cosmological fluids **1408.5481**;
   "thermal friction" on scalars for the Hubble tension **1911.06281** — all v-keyed or field-space, none a-keyed.
4. **The flat-space structural prior:** ALD radiation reaction ∝ ȧ (jerk); the self-force on a uniformly accelerated
   charge vanishes; dissipative self-force dies in the adiabatic limit. Radiation-reaction-type forces are keyed to
   *changes* of acceleration — MOND's μ(|a|) must survive the static limit. Within Huygens fields this is exactly the
   repo's all-orders κ-census (agentF). **Published exception class, and it is kinematic, textbook, and decisive for
   where to dig: massive-field worldline kernels.** Takagi (Prog. Theor. Phys. Suppl. 88, 1 (1986) — pre-arXiv; the
   canonical review) proves the accelerated-detector response for a massive field is **non-universal and
   mass-dependent** (→0 as m/a → ∞; non-Planckian structure; the "apparent statistics inversion" shows even the
   massless spectral SHAPE is dimension/field-structure-sensitive). Mechanically: the massive Pauli–Jordan function
   has interior-cone support keyed to m√σ, and on a Rindler/Deser–Levin worldline σ(τ,τ′) = (4/a²)sinh²(aΔτ/2)·(…) —
   **the dissipation kernel itself carries a (and H) beyond κ. S1 exists at kernel level in print.** [ENABLER]
5. **dS light-field secularity:** the published behavior of MMC/light scalars in dS is secular drift + late-time
   perturbative breakdown + critical slowing exactly as m_eff → 0 (Allen–Folacci; astro-ph/9407016; 1912.12951/12955;
   §1). The IR enhancement (⟨φ²⟩ ~ H⁴/m²) lives at ω ≲ H; **deep-MOND orbits run at ω ≈ 190–520 H** ([3]) — the
   enhanced condensate is quasi-static there and cannot supply O(1) orbital-frequency dissipation [our inference from
   the pinned frequency scales, flagged as such].
6. **Answer to "necessarily":** every COMPUTED case produces drift or v-friction — but no computation exists for the
   relevant configuration (non-Huygens field, accelerated/Deser–Levin worldline, response kernel). The "only secular
   drifts" claim is an **induction from N=computed cases, not a theorem**; Takagi-class kernels show the a-keying the
   door needs is kinematically present before any dynamics is asked. **The no-go is real but has exactly one unproved
   cell — the same cell agentF named.** [BOTH WAYS, full weight]

---

## 5. Front 5 — the EP/fifth-force walls (the coupling budget for any matter-coupled light field)
Pinned bounds (the standard set):
- **WEP:** MICROSCOPE final, **2209.15487** (+ companion **2209.15488**; PRL 129, 121102 (2022)):
  η(Ti,Pt) = [−1.5 ± 2.3(stat) ± 1.5(syst)]×10⁻¹⁵. Eöt-Wash torsion balance: Wagner et al. **1207.2442**
  (CQG 29, 184002 (2012), ~10⁻¹³ on Be–Ti/Be–Al), Schlamminger et al. **0712.0607** (PRL 100, 041101 (2008)).
- **Inverse-square law:** Kapner et al. **hep-ph/0611184** (PRL 98, 021101 (2007): holds to 56 μm); Lee et al.
  **2002.11761** (PRL 124, 101101 (2020): gravitational-strength Yukawa range < 38.6 μm).
- **PPN/light-scalar coupling:** Cassini |γ−1| = (2.1 ± 2.3)×10⁻⁵ (Bertotti–Iess–Tortora, Nature 425, 374 (2003) —
  pre-arXiv journal) ⇒ a massless/long-range scalar's matter coupling α² ≲ 10⁻⁵ of gravity. Theory frame:
  Damour–Donoghue **1007.2792** (any light dilaton-like scalar coupled to matter generates composition-dependent
  EP violation — crushed jointly by MICROSCOPE). Long-range light-scalar couplings independently bounded by pulsar
  timing: **2212.03098**.
**Consequence for the door:** a conventional matter-coupled light scalar strong enough to carry O(1) of inertia is
excluded as a force mediator at 10⁻⁵, and as a composition-coupled field at 10⁻¹⁵. The non-Huygens field must
therefore be (i) **the graviton sector itself** (universal, γ-safe; FLRW tails exist — 1611.00018 — but its self-force
magnitude is the §2 q²=Gm² disaster, so only a BATH/response role survives), (ii) a field coupled **only through the
universal worldline clock** (the F4-style coupling — which evades fifth-force bounds precisely because it mediates no
static force; its Step-4 "what grips matter" question stands), or (iii) screened/derivative-coupled (re-imports the
agentC singular-surface and Cassini perimeter). The walls do not touch trajectory-nonlocal MULTIPLICATIVE inertia
(Milgrom-2022 structure, WEP-safe by construction) — they kill additive/charge-keyed realizations. [MAP-SHAPING]

---

## 6. The map (one table)
| # | Published result | Pin | Door-relevant content | Column |
|---|---|---|---|---|
| 1 | MiSaTaQuWa + scalar EOM | gr-qc/9606018, 9610053, 0005030, 1102.0529 | trajectory-nonlocal self-interaction is rigorous GR; dm/dτ is part of the EOM | **ENABLER** (class exists) |
| 2 | Tail census in FLRW | Hobbs 1968; gr-qc/0411108 §VI; 1611.00018 | EM/conformal: no tail; MMC scalar, massive, graviton: tails — door inventory complete | **ENABLER** (right fields) |
| 3 | Cosmological scalar self-force | gr-qc/0201020, gr-qc/0411108 | inertial mass = history integral; dS tail = constant H², secular dm/dτ = −q²H²; force = v-keyed log-secular PUSH | ENABLER (structure) + **OBSTRUCTION** (keys to v,H — never a) |
| 4 | Magnitude/universality | `.out` [1],[2] | GmH/c³ ~ 10⁻²³ (Sun) / 10⁻⁸¹ (proton); 57-order spread; ~25 orders below a₀ | **OBSTRUCTION (decisive for classical self-force route)** |
| 5 | Milgrom time-nonlocal MI models | 2208.07073 (+9303012, 2310.14334) | the worldline target structure in print: WEP-safe, CoM-solved, EFE θ-enhanced, conservation laws; mechanism-free, causality open | **ENABLER (the target named)** |
| 6 | Tail↔MOND connection | — (searched) | **absent in the literature** | both (priority / graveyard) |
| 7 | Vacuum-inertia adjacents | astro-ph/0612599 (+1908.01589), HRP 1994, 1704.00780, 1611.02269 | every explicit kernel = difference family = Saturn-dead ×5–7×10⁴ ([4]); survivors are kernel-free | **OBSTRUCTION (prior)** |
| 8 | dS light-field secularity | astro-ph/9407016, 1912.12951/12955 | drifts + perturbative breakdown at ω ≲ H; orbits live at 190–520 H ([3]) | **OBSTRUCTION** (wrong window) |
| 9 | Massive-field worldline kernels | Takagi 1986 (+ gr-qc/0701130 tooling) | dissipation kernel knows a,H beyond κ (m√σ keying); response non-universal, m/a-suppressed | **ENABLER (S1 exists kinematically)** |
| 10 | EP/fifth-force walls | 2209.15487, 1207.2442, hep-ph/0611184, 2002.11761, 1007.2792, 2212.03098, Cassini 2003 | matter-coupled light scalar capped at 10⁻⁵/10⁻¹⁵; multiplicative-inertia structures untouched | **OBSTRUCTION (channel-killing, not class-killing)** |

## 7. VERDICT (both ways, full weight)
- **Most ENABLING published result for the non-Huygens door:** the conjunction of **Haas–Poisson gr-qc/0411108**
  (inertial mass as an exact, non-localizing history integral in dS — the structure class is real physics, not
  speculation) with **Takagi 1986** (massive-field worldline dissipation kernels carry a and H beyond κ — the agentF
  lemma's boundary is confirmed exactly where named, and S1 is kinematically in print). With **Milgrom 2208.07073**
  supplying the explicit worldline functional such a kernel must reproduce, the door's three ingredients (licensed
  nonlocality, a-keyed kernel, target functional) ALL exist in the literature — **in three papers that have never been
  put together.**
- **Most CONSTRAINING published result:** the **magnitude–universality double wall** quantified in §2/§4 — every
  computed tail force scales as q²/m (25–80 orders short, 57-order composition spread), the fifth-force corpus caps
  any conventional coupling at 10⁻⁵, and EVERY published vacuum-inertia kernel that was concrete enough to test
  (Milgrom-99 = repo F1; McCulloch QI) is the same ephemeris-dead difference family. **Published physics supplies the
  structure three times and the magnitude zero times.** A mechanism for the door must therefore make inertia
  *multiplicative and clock-keyed* (F4-style / Milgrom-22-style) — for which no computed exemplar exists in either
  direction. The honest prior from sixty years of this literature is hostile; the honest licence is that the decisive
  cell was never computed.
- **The single most decisive bounded calculation the map implies (= the N2 target, sharpened):**
  **extend agentF's exactly solvable Gaussian detector from the conformal to the MASSIVE scalar (then m ≲ H in dS) on
  the same Rindler/Deser–Levin worldline family.** Inputs are closed-form (massive Wightman/Pauli–Jordan pullbacks via
  σ(τ,τ′); agentF's Langevin machinery unchanged); the kernel is now genuinely trajectory-dependent, so the κ-census
  no longer protects the outcome. Pre-register THREE separated outcomes: **(O1, structure)** does the exact dressing
  G(a,H;m,Ω,γ) depend on (a,H) beyond κ — by how much; **(O2, sign/shape)** is there ANY (m,Ω,γ) corner with an
  inertia *deficit* whose crossover tracks a ~ cH·f(m/H) and a Saturn-safe o(cH/a) tail (note `.out` [6]: for
  m ~ ħH/c² the Boltzmann/Takagi suppression exponent m/κ crosses O(1) exactly around a ~ cH — the only known kernel
  class whose natural crossover sits at the MOND scale; note also the F2 see-saw warning — in FLAT space a gapped
  response died at one end or the other, and dS's κ ≥ H floor is the one new ingredient); **(O3, magnitude)** the
  λ²-scaling and what coupling would be needed for O(1) — reported WITHOUT rescue narratives if it is absurd.
  Kill conditions both ways: G still κ-only or deficit-free everywhere ⇒ **the non-Huygens door closes in the
  point-detector class and the bath mechanism line ends** (extended detectors and the Door-II hybrid would be all that
  remain); a deficit corner with the right crossover ⇒ first mechanism-grade evidence — and O3 then becomes the entire
  question, with §5's walls waiting. Either outcome is decisive for the program; nothing in the published record
  pre-empts it.

## 8. Honest scope (locked)
- This is a literature map with magnitude audits, not a calculation: nothing here derives, kills, or rescues F4/MI.
- Inferences original to this doc are flagged inline (the solar-reflex transfer to Milgrom-22-class μ tails; the
  frequency-window argument; the m~H crossover observation) — none is published, none is pre-registered, all need runs.
- Absence claims ("no tail↔MOND paper") are as of 2026-06-10 search depth; absence of evidence logged as such.
- Pre-arXiv classics (DeWitt–Brehme 1960, Hobbs 1968, Takagi 1986, Allen/Allen–Folacci 1985/87, HRP 1994, Cassini
  2003) carry journal pins only, marked at each use. The task-prompt id 1110.5167 is corrected in the header.
- Magnitudes: `agentN4_tail_magnitudes.py`/`.out`, both Hubble footings; no number above is hand-only.
