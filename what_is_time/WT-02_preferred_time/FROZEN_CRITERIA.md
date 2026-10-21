# WT-02 FROZEN CRITERIA: what defines "now" in the CFG938 parent?

Lane WT-02 of `what_is_time/` (owner question 2026-10-21: "what is time, based on my framework?"). Written 2026-10-21, before
any script or number of this lane. κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² (CFG4_common), scored separately and
never pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is added. Framework-native quantities only.
Not "theory closed". Nothing here says the data favour the framework. Anything that holds by construction is flagged and gets
no verdict weight.

## 0. Question

Does the framework's current covariant parent (CFG938) single out a time (a preferred foliation or frame), and is that safe?
- (a) Characteristics of the χ / medium / λ sector (and the graviton) about (i) Minkowski with the medium at rest, (ii) the
  static law state on NGC 3198, (iii) flat FRW (and (iv) a contracting medium, θ < 0). Hyperbolic (speeds?), elliptic
  (instantaneous), or something else?
- (b) Which frame is "now"? Is the medium 4-velocity hypersurface-orthogonal, or can it carry vorticity? Is the law defined in
  the medium frame?
- (c) Reconcile with L95 (closure forces a cuscuton): satisfies, evades (name the premise), or contradicts?
- (d) Preferred-frame size for w = 30, 370, 1000 km/s on both footings, against bounds the record already uses.
- (e) Tensor speed c_T in the parent vs GW170817.

## 1. Inputs (read only)

| input | file | commit |
|---|---|---|
| parent action, S1d (D²χ̄ = −3Hχ̄′), S5a dispersion, S5c margins, S5d (flat-space, 2nd-time-derivative check only), S1b (rest frame = cosmic frame, FORCED) | `campaign_fresh_gravity/CFG938_medium_continuum_eft/{DERIVATION.md,cfg938.py,cfg938.out}` | 92606e049b (criteria 7a0d41e8b) |
| current statement | `campaign_fresh_gravity/THEORY_CANONICAL_2026-10-21_DRAFT.md`; `..._2026-10-18.md` | 9470c0433d; f6da28c3db |
| exact one-field action | `qwen_claude_field_theory/papers_2026/PAPER49_DEPOSIT.md` | 77b39b9fcd |
| footings | `campaign_fresh_gravity/CFG4_common.py` | 3409d12da0 |
| NGC 3198 (Υ = 0.61, 43 radii) | `real_research/data/sparc_data/NGC3198_rotmod.dat` | 999f94dfee |
| L* window [24 pc, ≳ 1 kpc] | `campaign_fresh_gravity/CFG820_stiffness_from_globulars/README.md` | a57fe156ef |
| Solar-System background (g_e, u_e/a₀, A∥, A⊥; screened pull GM/L*²) | `campaign_fresh_gravity/CFG770_cassini_stiff_action/cfg770.out` lines 6–15 | 5554648db0 |
| L95 cuscuton closure | `fable_independent_2026/L95_closure_forces_cuscuton.py` | 49c68c9bcb |
| L31/PAPER9 foliation theorem; α₃ bound 4e-20 | `fable_independent_2026/L31_FOLIATION_NOGO.md`, `L31_foliation_nogo.py` | 0d41485722 |
| L61 permitted branches (escapes closed) | `fable_independent_2026/L61_PERMITTED_BRANCHES.md` | 78e1855b36 |
| L91 PPN table (α₁ ≲ 1e-4, α₂ ≲ 1e-7 weak field, α₃ ≲ 1e-20; semi-conservative theorem) | `fable_independent_2026/L91_PPN_PREFERRED_FRAME.md` | 5556b78bef |
| α₁ ≤ 3.4e-5 (frozen line), α₂ ≤ 1.6e-9 (strong field, pulsars only; "quoted, from memory" in that file) | `campaign_fresh_gravity/CFG172_door11C/CFG172_A3_ppn_frame.py` | f1585212e5 |
| GW170817: −3e-15 < c_T/c − 1 < 7e-16 | `campaign_fresh_gravity/CFG512_gravitational_waves/README.md`; `CFG484_alternative_chassis_search/FROZEN_CRITERIA.md` G13 | 7fc665e187; a93772934d |
| KiDS √-tail endings excluded below 1.67 / 2.07 / 3.44 / 2.77 Mpc (bins M_b = 1.50e10 / 3.66e10 / 6.01e10 / 9.13e10 M☉; canonical = alt) | `hunt_2026/h72_where_the_boost_ends.out` lines 5–8, 58–59 | f9bfc283a0 |
| khronon Cauchy problem on the leaves | `campaign_fresh_gravity/CFG292_khronon_strong_hyperbolicity/README.md` | 918b331834 |
| CMC/York vs unimodular clocks cannot merge | `real_research/cross_thread_review_2026_09_26/XR30_README.md` | 2a2d81f61d |
| AG6C NG2 (Lorentz-invariant U(1) tether superluminal, v² = 1 + g/a₀; criterion B check) | `argon_push/AG6C_relativistic_completion/README.md`, `FROZEN_CRITERIA.md`:127 | bd9d142db3 |
| ARGON10 G2 (common time function iff medium speed < 0.707c) | `argon_push/ARGON10_four_gaps_2026-10-16/REPORT.md` | 3839aa9b0a |
| owner criterion B (09-26): causality = no backward signal in a global time compatible with every cone | `STANDING.md`:29, 77 | a7a1e0e05b |

Cited, not re-derived (WT-01 record map): L31/PAPER9 (CONDITIONAL), L61, CFG292, XR30, AG6C NG2, ARGON10 G2, PAPER24/25 cuscuton
clock dead on GW170817 (CK01). The cuscuton explainer and L96 are DO-NOT-CITE as current. Declared external numbers (from memory,
not from the record): GW170817 source distance D = 40 Mpc; w_ref = 370 km/s is the CMB-frame speed used in the record's α bounds.
Cosmology for FRW frozen coefficients: CFG938's declared Ω_b = 0.0493, Ω_c/Ω_b = 5.364, H₀ = 67.4 km/s/Mpc, flat, Ω_Λ = 1 − Ω_m,
radiation neglected (z ≤ 10).

## 2. Computations

All in one script `wt02.py` (sympy + numpy/scipy), one process, OMP_NUM_THREADS=1, peak RSS < 1 GB, minutes.

### A. Characteristics
- **A1.** Build the CFG938 action density exactly as DERIVATION §3.4 writes it: n and u^μ from comoving labels; h^{μν} = g^{μν} +
  u^μu^ν; ∇∇χ with Christoffels; D_μD_νχ = h h ∇∇χ; D²χ = h^{μν}∇_μ∇_νχ; τ traceless; u² = h^{μν}∂χ∂χ; W_full expanded to
  second order about the background u₀; the λ term. Plane-symmetric perturbations: ξ (longitudinal label), η (transverse label),
  δχ, δλ; for the static backgrounds a Newtonian Φ in g₀₀ with −|∇Φ|²/(2K). Expand to O(ε²) and take Euler–Lagrange equations
  in sympy.
- **Backgrounds.** A-i Minkowski, uniform ρ₀, χ̄ with medium-frame gradient u₀ (0 and finite; gradient ∥ k and ⊥ k), λ̄ = 0
  (λ̄ ≠ 0 reported as a variant). A-ii frozen coefficients at each NGC 3198 radius (u, ρ_c = (1/Kr²)d(r²u)/dr from the γ → 0
  law; both footings; L* = 24 pc and 1 kpc). A-iii flat FRW, comoving medium, χ̄′ = −Kρ̄/(3H) (S1d), λ̄ = 0, metric not perturbed
  (gravity is k⁰ order; disclosed), frozen at z = 0 and z = 10. A-iv the same with H → −|H| (contracting medium).
- **Classification of each field's equation on each background.**
  - ELLIPTIC (instantaneous in the medium frame): no time derivative of that field along u (coefficient symbolically 0) and a
    positive-definite spatial principal symbol.
  - PARABOLIC: a symbolically nonzero first time derivative along u and no second one. FORWARD if unsourced Fourier modes decay
    at large k, BACKWARD if they grow.
  - HYPERBOLIC, speed v: roots s = ±iω with ω²/k² → v² (fit over the top two decades of k); finite iff v ≤ c(1 + 1e-12).
- **Hadamard test (A-iii, A-iv).** Roots s of the full coupled linear dispersion det M(s, k) = 0 at k ℓ_H ∈ {1e2, …, 1e6}
  (ℓ_H = c/H). ILL-POSED IVP iff max Re s / |H| > 1e3 at the top k and d ln(max Re s)/d ln k ∈ [1.9, 2.1] over the top two
  decades.
- **Labels for (a).**
  - NO PREFERRED TIME iff every sector on A-i, A-ii, A-iii is HYPERBOLIC with v ≤ c.
  - MEDIUM CLOCK iff some sector is ELLIPTIC on the static backgrounds.
  - ILL-POSED-IVP (added class; the five listed classes do not cover a Hadamard-ill-posed sector) iff the Hadamard test fires on
    A-iii or A-iv. Then also: anticipation time τ_k = 1/max Re s(k) at r = 1/k ∈ {10 kpc, 1 Mpc, 100 Mpc} for the reading in
    which the backward field is posed with final data, and **criterion B is VIOLATED** under that reading (any τ_k > 0 is a
    backward signal in the medium time). This is a structural reading, not a numeric threshold.

### B. The frame
- **B1.** The transverse (η) roots on A-i/A-ii. Vorticity allowed iff they are ω² = 0 with positive kinetic coefficient.
- **B2.** Kelvin: the canonical momentum of a medium element with the W(u) velocity dependence (sympy). Is curl v ≠ 0 forced when
  the canonical momentum is irrotational? Size ε_ω(r) = D(u)u/(Kρ_c c²) on NGC 3198 (both footings).
- **B3.** Frobenius: u ∧ du for a rigidly rotating medium (sympy). Nonzero ⇒ no medium slices.
- **B4.** Hörmander: [X_x, X_y] for X_i = ∂_i + (v_i/c²)∂_t (sympy). Time kernel of the χ constraint for a point source in a
  rigidly rotating medium via the Mehler (Landau) formula (scipy). Fraction of the response before the source (0.5 by evenness:
  BY CONSTRUCTION, no weight) and half-mass time t₅₀ in units of Ωr²/c². Illustration: t₅₀ for a medium rotating like NGC 3198's
  stars and for the B2-induced fraction ε_ω (flagged: the record's medium is static).
- **B5. Cosmic clock.** h^{μν}∂_μχ̄∂_νχ̄ for a medium moving at v relative to the FRW comoving frame (sympy, exact boost) ⇒ u_v(v).
  Nonzero ⇒ the homogeneous χ̄ is a clock whose rest frame enters the law (label COSMIC CLOCK; feeds D3).
- **Labels for (b).** GLOBAL NOW iff the action forces u to be irrotational. Otherwise "NOW = MEDIUM SLICES FOR IRROTATIONAL FLOW
  ONLY". "Law defined in the medium frame": read from the action (u² uses h), BY CONSTRUCTION.

### C. L95
- **C1.** p_χ = ∂L/∂(∂₀χ) on A-i and A-iii (sympy). **C2.** A ≡ ∂²H/∂p_χ² of the χ/λ sector, and L95's obstruction AA′/2.
- **C3.** L31 / DC-019 α₃ horn: is the foliation non-dynamical (premise)? From the action (u is varied: BY CONSTRUCTION) and CFG938
  S3b (∇_μT^{μν} = 0), α₃ = 0 by the semi-conservative theorem as in L91 C3: BY CONSTRUCTION, no weight.
- **Labels for (c).** SATISFIES L95 iff A ≡ 0 on every background (the cuscuton class). CONFLICT WITH L95 iff A ≠ 0 for the field
  carrying W with a strictly monotone kernel (then report which of the two is wrong, by computation). EVADES iff L95's premise
  (one scalar on the metric's ADM foliation, H = ½A(s)p² + W(s)) fails; name the premise. Several may be reported.

### D. Preferred-frame size (w = 30, 370, 1000 km/s; both footings; L* = 24 pc and 1 kpc)
Normalisations (O(1) PPN formula coefficients dropped, declared): α₂_eff ≡ δΦ/(U (w/c)²) or δa/(g (w/c)²); α₁_eff ≡ δa/(g (w/c)(v/c)).
- **D1. Relativistic simultaneity of the local medium clock.** For a density pattern moving uniformly at w through the medium:
  ratio of the medium-frame instantaneous χ to the retarded Φ of the same density (sympy, exact) ⇒ coefficient C₂(θ).
  α₂_eff,D1 = max_θ|C₂|/(w/c)² × f_c(r), with f_c = Φ_c/U the medium-sourced potential fraction at the test radius: solar surface
  (α₂ weak, 1e-7) and a neutron-star surface R = 10 km, M = 1.4 M☉ (α₂ strong, 1.6e-9). f_c from the screened pull Φ_c = GMr/L*²
  (CFG770 K1, reproduced as K6); the unscreened ceiling f_c = a₀r²/(GM) is context only.
- **D2. Newtonian Doppler of the medium response (mode level).** F − 1 = (k·w)²/(ω_k² − (k·w)²) with ω_k² = c_s²k² + Kρ₀[R′cos²θ +
  (R/u)sin²θ] (CFG938 S5a), k = 1/r, worst angle. E1: R☉ and 1 AU in CFG770's three Galactic backgrounds (ρ_e from a point-mass
  Galaxy at 8.2 kpc reproducing each g_e; declared model). α₂_eff,D2 = |F − 1| f_c/(w/c)². E2: NGC 3198 radii: F − 1 and
  v_crit(r) = min_θ ω_k/k; no record bound (reported).
- **D3. Cosmic clock (α₁-type, linear in w).** u_v from B5 with v = w; u_v/a₀ per footing.
  - (i) Solar System: δa_D3 = (u_v/u_e) · max(|d ln R′/d ln u|, |d ln(R/u)/d ln u|) at u_e · GM☉/L*² (mode level; declared).
    α₁_eff at 1 AU (g = GM☉/AU², v = 29.8 km/s) vs 3.4e-5.
  - (ii) MOND regime: crossover r_× = √(GM_b a₀)/u_v for the four h72 bins vs their r_end bounds.
- **α₃:** C3 (by construction).
- **Labels for (d).**
  - EXCLUDED iff any α_eff (D1; D2 at E1; D3(i)) ≥ 10 × its bound on either footing at any w and either L* end, or any h72 bin has
    r_× ≤ bound/10.
  - MEDIUM CLOCK iff a frame enters the law (some computed correction ≠ 0) and every α_eff ≤ bound/10.
  - UNDERDETERMINED iff some α_eff ∈ (bound/10, 10 × bound), or some r_× ∈ (bound/10, 10 × bound), or an effect has no record bound
    (E2).
  - NO PREFERRED TIME iff every correction vanishes identically.
  - COSMIC CLOCK added iff u_v ≠ 0.

### E. c_T
- **E1.** Sympy, TT waves in a static medium with uniform medium-frame gradient u₀ẑ, propagation angle θ_k and both
  polarizations. EH TT part checked by K5. Output δ(c_T²/c²) = C_T(θ_k, pol) L*²u₀²/c⁴, plus any mass-like or one-derivative
  terms from W and λ̄ (size at 100 Hz).
- **E2.** Local max |c_T/c − 1| at u₀ → a₀ (the W wall), both footings, L* = 24 pc and 1 kpc.
- **E3.** Path model (declared): D = 40 Mpc; host and Milky Way media each a point-mass law state with M_b ∈ {1e11, 1e12} M☉;
  ∫u²dr one-sided from 0 to ∞ per galaxy (γ → 0 law, screening ignored: an upper bound); intergalactic u = 0 (S1d).
  ⟨c_T/c − 1⟩ = C_T,max L*² ∫u²dl /(2c⁴D) (with the sign from E1).
- **Labels for (e).** PASS iff the E3 value lies in (−3e-15, 7e-16) on both footings, both L* ends and both M_b. EXCLUDED iff it lies
  outside for any footing at either L* end with M_b = 1e11. ROBUST PASS iff the E2 worst case (u = a₀ along the whole path) also
  passes. Report L*_max allowed by E3 and by the worst case. If C_T ≠ 0, CFG938's A5 "c_T = c (structural)" is corrected to a
  computed bound. **Disclosed choice:** the verdict uses the path model, not the worst case, because GW170817 bounds the
  path-averaged speed and the tether sector vanishes on FRW; this choice is made here, before any number.

## 3. Overall line
List every label that fired per sub-question. Headline = the highest present in the order EXCLUDED > CONFLICT WITH L95 >
ILL-POSED-IVP > UNDERDETERMINED > MEDIUM CLOCK (+ COSMIC CLOCK) > NO PREFERRED TIME.

## 4. Controls (all must pass for the main run to be read)
- **K1.** NGC 3198 law reduction: max|g/g_law − 1| ≤ 1e-12 on both footings (CFG938 committed 2.22e-16).
- **K2.** S1d reproduced: D²χ̄ = −3(a′/a)χ̄′ on FRW (symbolic).
- **K3.** S5a reproduced from the A1 machinery (c → ∞, λ̄ = 0, Newtonian self-gravity on): medium root ω² = γρ₀k² + Kρ₀R′ (k ∥ ∇χ)
  and γρ₀k² + Kρ₀R/u (k ⊥ ∇χ), symbolic; transverse roots ω² = 0.
- **K4.** Mehler kernel at B → 0 equals 1/(4πr) to ≤ 1e-6 relative.
- **K5.** Linearised Ricci for TT h equals −½□h_ij (symbolic); with L* = 0, c_T = c exactly.
- **K6.** The Fourier integral of the screened response 2KM/(L*²k⁴) gives the pull GM/L*² (CFG770 K1), symbolic.
- **K7.** The A-iii machinery at H → 0 has zero coefficient of ∂₀δχ and ∂₀δλ.

## 5. MUTATE (`WT02_MUTATE=1`; exit 1 iff every tooth bites, else 2)
- **MU1 (Einstein-aether shear coupling).** Add (c⁴c₁₃/16πG) K_ijK^ij of the medium slices, c₁₃ = 0.01, to E1. Bites iff
  |c_T/c − 1| ≥ 1e-3 and (e) reads EXCLUDED.
- **MU2 (frame in the metric sector).** f_c ≡ 1 in D1/D2 (the medium-frame constraint acting on the whole Newtonian potential, the
  DC-019 constraint-first reading). Bites iff some α_eff ≥ 10 × its bound and (d) reads EXCLUDED.
- **MU3 (intrinsic slice Laplacian).** Replace h^{μν}∇_μ∇_νχ by the intrinsic Laplacian of the medium slices (drop the θ u·∂χ
  term) in A-iii. Bites iff the A-iii label changes (parabolic coefficients vanish; Hadamard test does not fire).
- **MU4 (no vorticity).** Ω = 0 in B4. Bites iff the bracket vanishes and t₅₀ → 0 (≤ 1e-3 of the Ω ≠ 0 value).

## 6. Outputs
`wt02.py`, `wt02.out`, `wt02_results.json`, `wt02_MUTATE.out`, `wt02_results_MUTATE.json`, `README.md`. All left uncommitted for
orchestrator review. Post-freeze changes go in an appended amendment section; this text is not edited.

## 7. Blindness disclosure
Before freezing I read CFG938's README, DERIVATION and cfg938.py, including S1d's printed D²χ̄ = −3Hχ̄′ and that S5d checks only
flat space and only second time derivatives. I also read L95, L272, L91, CFG172's bound lines, CFG770's README and backgrounds,
h72's bounds, the WT-01 coordinator notes and a grep of WT-06's criteria. Without running anything I formed these expectations:
1. On FRW the χ equation carries −3H∂₀χ (forward parabolic) and its adjoint λ equation +3H∂₀λ (backward), so a growing root near
   c²k²/(3H) is expected.
2. A vortical medium makes the constraint operator a Hörmander sum of squares, so the response is two-sided in time over ~Ωr²/c².
3. The ττ term contains Christoffel² and should shift c_T by ~L*²u²/c⁴ times an O(1) coefficient. My mental estimate was ~4e-19
   (24 pc) and ~8e-16 (1 kpc) at u = a₀, i.e. the 1 kpc worst case near the 7e-16 line. This is why the path-model choice in E
   is stated in advance.
4. The homogeneous χ̄(t) has a timelike gradient, so a medium moving at v should see u_v ≈ (Ω_cH₀/2)v ≈ 1e-3 a₀ at 370 km/s.
5. Screened Solar-System effects are tiny.

No number in this lane has been computed by a script. The rules are written to decide either way. Expectation 1 is tested
against K7 and MU3; expectation 3's worst case does not set the verdict.

---

## Amendment A1 (POST HOC, 2026-10-21, after runs 1–3; appended, frozen text above unchanged; not committed)

**A1.1 Run history (script and numerics only; no rule changed).**
- Run 1 crashed before any verdict. K4 FAILED because the Mehler integral was truncated at t = e¹², giving g(0) = 0.9986. E1 then
  crashed on a sympy Subs substitution. Fixes: the integration range was extended to e⁷⁰; the TT plane wave in E1 is built
  explicitly; the oscillatory time-kernel integral is split (QAWO). Log kept: `wt02_firstrun_K4fail_E1crash.out`.
- Run 2 completed with the same labels as run 3, but K4 FAILED on an extra β = 1e-9 check I had added. That check is not in the
  frozen K4, and it assumed g is analytic at B = 0. It is not: 1 − g(β) = 0.42773 √β (checked over β = 1e-11…1e-5), which is
  physical. The extra check was removed, and the √β coefficient is printed as a diagnostic. Outputs kept:
  `wt02_run2_K4extra.out`, `wt02_results_run2_K4extra.json`.
- Run 3 is final. MUTATE was run from the same script bytes.

**A1.2 D2 at 1 AU is a mis-specified gate.**
- §2-D lists E1 = R☉ and 1 AU and scores "D2 at E1" against "its bound", but names no bound at 1 AU. The script applies the only
  weak-field α₂ bound in the record (1e-7, L91) at both radii. That literal reading gives EXCLUDED: α₂_eff = 4.1e-6 at 1 AU for
  w = 30 km/s and L* = 24 pc, on both footings (ratio 41). This is the only row ≥ 10×.
- Post hoc, the comparison is wrong in three ways:
  1. The 1e-7 line is the solar-spin observable, measured at the Sun, not at 1 AU.
  2. Its value assumes the CMB-frame w_ref ≈ 370 km/s, so the observable anisotropy it allows is
     δΦ/U ≤ 1e-7 (w_ref/c)² = 1.52e-13.
  3. D2 is a step in w: |F − 1| ≈ 1 for every w ≫ c_s = 0.36–15 km/s. Dividing by (w/c)² at 30 km/s therefore inflates
     α₂_eff by (370/30)² = 152 against the bound's own normalisation.
- Scored on observables instead:
  - Solar surface: δΦ/U = 8.8e-19 against 1.52e-13.
  - 1 AU: the frame-dependent pull is ≤ GM☉/L*² = 2.42e-16 m/s², against the record's ephemeris bound on a sunward pull at
    1 AU, 3.66e-14 m/s² (CFG770 T3, `cfg770.out`:36, 5554648db0). Ratio 0.0066.
- Post-hoc (d) labels: UNDERDETERMINED + MEDIUM CLOCK + COSMIC CLOCK. Post-hoc headline: ILL-POSED-IVP. Both carry no class
  weight. The script prints them in a separate block labelled POST HOC (A1); that block was written after run 2's numbers were
  seen.

**A1.3 What w physically is (reporting, no rule change).**
- **D1 / D2:** w is the velocity of a baryon pattern relative to the medium that would carry its law. A system in its law state
  carries its medium (w = 0), and covariance then gives no effect.
- **The Solar System:** relative to a static (non-rotating, stress-supported) Galactic medium, the Sun moves at roughly the
  circular speed.
- **D3:** w is the velocity of the local medium relative to the comoving (CMB) frame, i.e. a peculiar or bulk velocity.
- **The tabulated values:** 30 km/s is an Earth-orbit-like speed; 370 km/s is CMB-frame-like; 1000 km/s is cluster-galaxy-like.

**A1.4 Flags found while computing (no class weight).**
- On FRW the medium's kinetic coefficient is K ρ (1 − Kρ_c/(9H²)), i.e. 0.956 at z = 0 and 0.860 at z = 10; this is the
  cosmic-clock term W ⊃ (χ̄′ v)². The clock gradient Kρ_c/θ diverges as θ → 0. This suggests strong coupling or a ghost near
  turnaround, but it is not computed beyond FRW.
- CFG770's static Solar-System solution assumes the Sun at rest in the Galactic medium. At the Sun's actual speed relative to
  that medium, |F − 1| ≈ 1 at 1 AU, so Q2 needs a moving-source recomputation. It is not done here, and every such effect stays
  ≤ GM☉/L*².
