# openai/math cross-analysis — README

Focused follow-up on the OpenAI math release (github.com/openai/math; local
read-only copy `../_external_data/openai_math/`, 372 families / 722
manuscripts) against the Zimmerman framework. Criteria frozen first
(`FROZEN_CRITERIA.md`, committed alone in a354de4a7). All scripts have
PASS/FAIL checks, `<LANE> COMPLETE` lines, results JSON, and MUTATE controls
with separate outputs, re-verified by the parent after each lane landed.

**κ = ½ is FITTED throughout and stays fitted. Nothing here is theory-closed.
No dark-matter particle. The cold fluid's mass is still required. Both
footings (a₀ = 9.3603e-11 and 1.1312e-10 m/s²) are always reported separately.**

## Ranked table

| # | Family / exact theorem | Open piece | Verdict | Screen (Q1–Q3) |
|---|---|---|---|---|
| 374 | Sharp one-third stability of Brenier maps: ‖Tμ−Tν‖_{L2(ρ)} ≤ C(K,Y) W₂^{1/3}, uniform source on a compact convex body; exponent 1/3 sharp (three-atom cube example) | P2 (settling stability) | **TOOL** | Q1 no (a₀ absent); Q2 n/a; Q3 n/a. Base-rate 1%-window 0.00224 (record 0.002–0.003) |
| — | Same family, MW application: 0.1-dex baryon error | P2 | **TOOL, quantitative** | W₂ = 0.4073 / 0.3719 kpc; ‖ΔT‖ = W₂ exactly (exponent 1, not 1/3) for radial monotone maps; worst-case C\*W₂^{1/3} = 9.5e4 kpc is vacuous ×58 vs 2L, and ×2.3e5 above the true map change (ratio 4.3e-6 / 4.0e-6). M_ph elasticity d ln M_ph/d ln M_b = 0.4960 / 0.4964 (deep-MOND √M_b law). Truncation cost M_ph(<r_in)/M_ph = 3.8e-13. No change-of-variables extension; the uniform-source hypothesis is essential (band counterexample diverges); known literature extension (bounded densities) lowers the exponent to 1/6 in W₁ |
| 360 | Weak-MTW → convex injectivity + uniform bi-Hölder transport (2 papers + Lean) | P2 | **DOES NOT APPLY** | Q1 no; Q2 none (Hölder exponent non-explicit); Q3 n/a. Euclidean cost has quartic MTW tensor ≡ 0: weak-MTW is vacuous in flat space; annulus density bounds hold (ρ_min at r_in; dynamic range 8.8e4–2.5e9), but the regularity is classical Caffarelli; true centre failure mode is "density → 0", map continuous but not α-Hölder for any α > 0. No scale for a₀ or κ |
| — | JKO reframing of the settling (T3): F[ρ] = KL(ρ‖ρ_ph), Wasserstein gradient flow | P2, P8, G9 | **TOOL, well-posed; G9 REJECTED** | PDE ∂ₜρ = Δρ − ∇·(ρ∇log ρ_ph); mass conserved (sympy FTC + numeric drift 1.7e-13); unique minimiser = ρ_ph (strict convexity); constrained minimiser = (M_supply/M_ph)·ρ_ph with M_ph = +66.53 / +73.19 M_b → only 8.06% / 7.32% of the target is realisable (the supply limit, CFG375's reading). Effective force v = −∇(log ρ − log ρ_ph); linearised settling rate κ₁·D/r_out² with κ₁ = 9.87 → Γ = 9.87/t_dyn, ×353 above CFG382's λ = 0.028 (λ is the damping, not the engine) and ×9.9–99 above CFG378's g bracket. G9: the force field −∇log ρ_ph is NOT a multiple of any baryonic field (deep-MOND log-gradient is ~1/r, baryonic is 1/r²; harmonicity violated where ρ_b = 0; best c sits at the 0.1 window edge with residual ~4e9 of field scale on both footings) → the settling force requires the CFG382 fluid-lapse coupling λ (CONDITIONAL per the record) or the fluid's own superfluid pressure (FL1). **Correction 10-07:** the original lane's claim ρ_ph < 0 (proxy |ρ_ph|, M_ph = −66.5) was a sign error (−div vs +div); ρ_ph > 0 on the annulus, KL needs no proxy, all numerics stand (see t3_analysis.md CORRECTION) |
| 096 | Gaussian propeller: sharp constant 9/(8π), extremiser = three 120° sectors, each with exactly 1/3 of the Gaussian mass | P1, T4b | DOES NOT APPLY | Q2 chosen (extremal problem is the structure; no physical functional in the a₀ sector); 9/(8π) is 259% off T; T4b: **no partition forces the ~1/2 settled/unsettled cluster split** (a 1/2 split postulates 2 cells — free choice) |
| 087 | Mahler (symmetric 4ⁿ/n!, n = 3 ⇒ 32/3; general-body 64/9 flagged) | P1 | DOES NOT APPLY | pi-free; √(32/3) is 18.3% off; Q1/Q2 fail |
| 090 | Triangular-lattice universal optimality: ζ_A(6) = 4.1413, W(E_△) = −0.2011, NN² = 2/√3 | P1 | DOES NOT APPLY | ζ_A(6) is 3.5% off 4 with p_base 0.011 → coincidence-level, no derivation chain; Q1/Q2 fail |
| — | Deep-MOND field-energy extremal at fixed Λ (new, T4) | P1 | DOES NOT APPLY | E_field(R) = (1/3)·M·√(GMa₀)·ln(R/r_in) (sympy-exact); ρ_ph = √(GMa₀)/(4πGr²); M_ph(<r) = r√(GMa₀)/G (full-kernel agreement 1.1% at 100 r_t). Every dimensionless ratio at fixed Λ carries free M, R, r_in or a ln; no 4 or 1/(32π) emerges; emerged constants (1/3, 2/3, (32π)^{±1/4}) miss both targets by ≥21%. Q1 accepts a₀ (it enters the Lagrangian); κ stays fitted |
| 215, 221, 263, 267, 269, 270 | Extra-hard deep reads (T6): O(3)/O(4) lattice continuum limit (mass-gap amplitude 32·e^{π/4−1/2}), Mézard–Parisi diluted spin glasses, ionization conjectures (TF density constant k = 2^{3/2}/(3π²) = 0.09552), BEC exact depletion 8/(3√π)·√(ρa³), Laughlin gap ≥ 1/25 at filling 1/3, BFSS matrix model | P1–P8 | all DOES NOT APPLY / analogy-only | Closest constant in the entire release: TF k at 4.2% miss of T with p_base 0.0045 → NUMEROLOGY (derived in TF kinematics, but Q1 fails: no Λ, no G, no acceleration chain). 1/25 sits within 0.53% of the F-member 1/(8π); 1/(8√(2π)) = T/2 exactly (trivial algebra, no derivation). 1/3 filling ↔ 374's 1/3 exponent noted as observation only. No candidate within 1% of T anywhere; none FORCED |
| 29 other score-1 + 374 + 377 | T5 sweep, 31 families at full-manuscript level (46 extracts), incl. 260 Penrose, 264 Kerr SCC, 348 Einstein 4-manifolds, 267 BEC, 282 scale→conformal, 362–364 kinetic | P3, P5, P6, P7 | all CONFIRMED ≤ 1; **3 downgrades: 264, 260, 348 → 0** | No promotions. P3: no mass ratio anywhere (BEC condensate fraction is liminf > 0 only). P5: no p = 3-with-source result in the corpus (370 semilinear Δ, 377 p = ∞ homogeneous). P6: vocabulary only (186/213/214/228/375 tanh). P7: nothing (362–364 repulsive/collisional) |
| — | **T7 second-generation coincidence scan** (new, this pass): 57 extracted constants × 15 targets × 891-form null + 1596 pair ratios | P1, P4 | **one new NUMEROLOGY, rest NULL** | Headline: a_TF = 3/7 ↔ cluster completeness 0.430 at **0.33% miss** (p_base 0.0034; no derivation; swallowed by ±0.15). STRUCTURAL keep: **κ₁ = π² to 4×10⁻⁵** (μ-reduction ⇒ Neumann heat spectrum — pins the undamped settling rate). Elasticities are the framework's own ½ (√M_b slope). Pair scan: 730 hits ≤ 3× Poisson null (expected 343); 76 exactly algebraic (π-rational identities), residual null-consistent. 1%-window base rate reproduced: 0.0022. MUTATE: C0–C3 flip as declared (rc 1) |
| — | **T8 full-corpus fingerprint sweep** (new, this pass): ALL 722 manuscripts scanned at full-text level (TeX + pdf fallback), closing the abstract-only gap | P1, P5, P6 | **empty corpus, verdict confirmed** | 0 hits each: kernel 1/(1−e^{−√y}), 3-Laplacian-with-source, Gρ_Λ, a₀ = c√(Gρ_Λ) spellings. 32π ×10 all incidental theorem coefficients (only gravity contact: Kerr–Newman–Penrose 32π/15, no Λ, Q1 fail); √(32πe) once in an info-theory bound; 0.0997 = an arXiv ID; 5.36 ×6 = pgfmath/TikZ/DOI artifacts; 122 plain Bose occupancies, zero with √y argument. Main 6/6 rc 0; decoy MUTATE flips hit counts 10→0/1→0/1→0/6→4 (rc 0, C4 verifies). Reusable as a per-release gate |
| — | **T9 phantom-mass elasticity law ε(s) (the campaign's positive law)** — kernel-exact M_ph(<r) = M_b/(e^s−1), s = r_t/r, ⇒ ε = 1 − (s/2)e^s/(e^s−1); ε(0) = ½, ε < ½ at finite radius | P2/P8 (new falsifiable law) | **DERIVED, 6/6 PASS, Lean-certified** | Predicts **0.49626/0.49660** vs T1's measured **0.4960/0.4964** (the unexplained 0.8% sub-half deficit, both footings, zero parameters) and the +0.1-dex bridge **+12.105%** vs T1 C6 +12.10/+12.11%. Half-mass at s = ln 3; elasticity zero at s = 1.5936; universal prediction curve (ε = 0.391 at 30 kpc, 0.209 at r_t, −0.157 at 6.1 kpc). Lean cert (5 theorems, zero sorry, {propext, choice, quot}): occupancy identity, stable form, closed form, root annihilation, half-mass. MUTATE (M_b^{1/3}): C1/C2/C3/C6 flip, rc 1. κ = ½ stays FITTED; the ε(0) = ½ = κ = kernel-half unification is a declared observation |

| — | **T10 settling-flattening theorem** — the synthesis: ∂ₜμ = ∂²μ/∂r² in μ = r²ρ (JKO settles as pure heat, drift cancels exactly; sympy residual 0, numeric 2.6e-6 @ 4th order, quartic conv); v² = (4πG/r)∫μ — flat ⇔ μ const (3.2e-16); deep-MOND = the uniform μ-state, v⁴ = GMa₀ exact; area law M_ph = 4πμ_ph·r; diffusive falsifier τ ∝ ℓ² (exponent 1.986); P3-radius corollary r_supply = r_t/ln(1+1/5.36) = 5.8457 r_t = **71.4 kpc (MW canonical)** / 65.0 alt / 714 kpc (10¹³), inside R500 ⇒ clusters full-share (P4) while late spirals supply-limited | P2/P3/P8 | **DERIVED, 7/7 PASS, Lean-certified** | MUTATE flips exactly C1+C2 (drift halves; symbolic residual ≠ 0, maxdev 1.7e-2). Lean cert (3 theorems, zero sorry): mu_ph_is_constant, v4_from_uniform_mu, supply_mass_exact. Freeze corrections dated: C7 5.8480→5.8457 (hand-slip), C8 flip-set (C6 never sees the drift) |
| — | **T11 the assembly clock (historical face of the settling law)** — the cluster/group completeness pair 0.43/0.60 at the SAME R500 density becomes an exact assembly-time ratio: t_c/t_g = ln(1−f_c)/ln(1−f_g) = **0.6135** (Γ cancels via R500 density-locking; no λ, a₀, κ); curvature signature 0.6135 < linear 0.7167; second-mode window [0.5577, 0.5926] ⊂ [0.55, 0.66]; z-face t_c ≈ 7.1 Gyr ⇒ z ≈ 0.75; corollary: f at fixed Δ is mass-independent | P3/P4/P8 (history) | **DERIVED PRELIMINARY, 5/5 PASS, Lean-certified, falsifier preregistered** | Literature cross-check lands INSIDE the window (cluster formation z₁₄ ≈ 0.8, 2603.19521; BCG late-time growth 2–14%, 1409.4820). KILL condition registered: measured t_c/t_g outside [0.55, 0.66]. Lean: assembly_ratio_from_law (Γ divides out), rc 0, zero sorry. MUTATE (pair swap) flips C1+C2+C3 as corrected; freeze corrections dated (C3 pair-dependence, KM_MPC units, C6 source grounding) |

| — | **T12 the epoch-elasticity of completeness** — exact sensitivity curve ε(f) = (1−f)·[−ln(1−f)]/f from the settling law (Γ, t cancel): MW floor 0.14 → 0.9265, groups 0.60 → 0.6109, clusters 0.43 → 0.7451 (cluster:group 1.2198); ε → 1 young / → 0 mature, strictly decreasing | P3/P4 (sensitivity) | **DERIVED, 6/6 PASS, Lean-certified** | **Three-clock λ audit: cluster clock λ = 0.0290 ± 0.0142, group clock 0.0376 ± 0.0161, joint [0.0215, 0.0432] CONTAINS CFG382's MW-calibrated λ = 0.028** — the coupling is not free. Falsifier registered: epoch-split completeness stacks must follow the curve; flat sensitivity kills the exponential law. Lean: epoch_elasticity_closed, rc 0, zero sorry. MUTATE (linear branch ε = 1): flips C1–C4 as declared. MW floor not re-fitted (convention difference, registered) |
| — | **T13 the phantom sound-speed theorem** — the settled halo is barotropic: hydrostatic P = c²ρ forces c_ph² = v_flat²/2 exactly (SIS √2); with v⁴ = GMa₀: c_ph = (GMa₀)^{1/4}/√2 = **132.76/139.20 km/s** (MW, pinned to baryons, no fit); λ_J = **√2·π·r** (4.4429×, dev 4.4e-16) ⇒ Jeans-stable at every radius ⇒ **phantom substructure is structurally impossible** (missing-satellites/too-big-to-fail have no counterpart; Klypin 1999 + satellite census grounded); L2 closed: FL1's pressure requirement forces exactly the barotropic law, polytropes fail the radial scaling (drift 0.215/dex) | P2/P8 (structure) | **DERIVED, 6/6 PASS, Lean-certified, falsifiers registered** | Falsifiers: (i) pure-dark subhalo obs kills the no-substructure corollary; (ii) σ_ph away from (GMa₀)^{1/4}/√2 kills the pinning (MW classical-satellite σ ≈ 110–125 km/s vs 132.8/139.2 — live near-boundary test). Lean: sound_speed_fourth_power, sound_speed_sqrt, jeans_square, rc 0, zero sorry. MUTATE (polytrope) flips C1 as corrected; freeze corrections dated (C2 hand-slip, C6 flip-set) |
## Screen summary (applied to every candidate constant)

- **Q1** derives a₀? — No candidate derives a₀; every exact constant from the
  release is a host-theory quantity (Q1 fails), including the closest hits.
- **Q2** forced or chosen? — The only "exact hits" (T, 4, 1/4) are the fitted
  restatements of the law itself (calibration, not derivation); all others miss
  by ≥ 3.5% and would require a free reading.
- **Q3** base-rate null — family F of 889 distinct simple forms
  {(p/q)πⁿ, √((p/q)πⁿ): p,q ≤ 12, n ∈ −2..2}; 1%-window shares recomputed at
  0.0022–0.0025 vs T (record 0.2–0.3% confirmed) and 0.0045 vs 4; q = 32 ∉ F
  so the null is not trivially satisfied. Every candidate's p_base is either
  ≥ 0.011 or derived-without-chain (TF k: p_base 0.0045, Q1 fails).

## Honest bottom line

The release does **not** contain a route that forces κ = ½, the rational 4, or
32π — that is now a robust, manuscript-level negative, not an abstract-level
guess: 31 families fully re-read (T5), 12 more deep-read to the constant level
(T6), the three score-1 analogies re-derived exactly (T4), and the two
transport theorems (374, 360) read to the proof level (T1, T2). P1, P3, P5, P6,
P7 stay open exactly as before, and every numerical coincidence in the
physics-native families lands inside the base-rate null.

What the release DID supply is four tools with real teeth:

1. **374 → a quantitative stability guarantee for the settled profile**
   (TOOL): an 0.1-dex baryon error moves the profile by only 0.41 kpc out of
   818 — with the exponent-1 (not 1/3) response of radial maps, 2×10⁵× below
   the adversarial bound. Any future settling implementation inherits this
   robustness.
2. **JKO reframing of P2 is well-posed but constrained** (TOOL + negative):
   the settling is a Wasserstein gradient flow of KL(ρ‖ρ_ph) with a unique
   minimiser and exact mass conservation, but the force −∇log(ρ/ρ_ph) cannot
   be gravity-only (G9 rejected); the undamped flow settles ×353 too fast
   (κ₁ = 9.87 vs CFG382 λ = 0.028), and the supply limit caps realisable
   target mass at 8.1% / 7.3% (MW). The mechanism must be the CFG382 lapse
   coupling or FL1 superfluid pressure, with λ acting as damping.
3. **Corpus-level negative for the switch**: nothing in 372 families models
   P6 beyond vocabulary (e.g. 375's tanh as an interpolant template).
4. **New exact deep-MOND closed forms** (Lean-certified): E_field =
   (1/3)M√(GMa₀)ln(R/r_in), M_ph(<r) = r√(GMa₀)/G, ρ_ph = √(GMa₀)/(4πGr²).

The settled-profile robustness has a falsifiable face for the record: the
*sharp* RAR scatter imposes log|ΔT|/d log M_b ≈ 0.5 (the measured elasticity
0.4960/0.4964), i.e. the phantom mass tracks √M_b, not M_b — a statement the
SPARC record can be re-audited against at fixed M_b errors.

## Follow-up lanes worth running

- **L1 (recommended): damped-JKO closure** — CFG378's PM engine with the
  T3-derived exact reduction (μ = r²ρ ⇒ pure Neumann heat flow) and λ = 0.028:
  decide whether JKO + λ is a complete P2 mechanism (predicts galaxies/groups,
  fails clusters at 0.43 by CFG382's own saturation f = 1−e^{−Γt}) or only a
  galaxy-floor mechanism. Falsifier: X-COP completeness at R500 = 0.43 ± 0.15.
- **L2 (recommended): the force-law constraint** — any gravity-only candidate
  must reproduce |∇log ρ_ph| = (2/√(GMa₀))·g_ph in the deep regime (1/r
  susceptibility to the phantom field); test whether FL1's superfluid pressure
  term produces exactly this in the annulus. This is the natural P2/G9
  continuation and the only positive law candidate this campaign generated.
- **L3 (not recommended): further corpus reading** — the screen is saturated;
  no family outside the ones above deserves a second look for P1–P8.

## House-keeping notes

- First commit (a354de4a7) accidentally carried CFG378's staged
  FROZEN_CRITERIA.md from the shared git index (parallel-session collision,
  same as CFG375's note). History was not rewritten; all later commits staged
  explicit paths only.
- Lean certificates (`lean_certs/`): cert374_cube_sharpness.lean (W₂² = a³/4,
  ‖ΔT‖² = a(1+a²)/4, the a = 2/5 specialisations 2/125 and 29/250, sharpness
  ratio (1+a²)/a², amplification ‖ΔT‖ ≥ W₂/a) and cert_deep_phantom_algebra.lean
  (M_ph(<r) = r√(GMa₀)/G, 4πGr²ρ_ph = √(GMa₀), the 4π/(12πGa₀) prefactor
  collapse to (1/3)M√(GMa₀)). Both compile clean in the house build with zero
  sorry and axioms = {propext, Classical.choice, Quot.sound}. They certify the
  arithmetic only, per house practice; the physics mapping lives in the lane
  scripts.