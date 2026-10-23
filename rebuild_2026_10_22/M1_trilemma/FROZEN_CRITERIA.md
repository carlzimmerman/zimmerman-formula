# M1_trilemma FROZEN CRITERIA (2026-10-23): a way through the v3/v4 trilemma, or a proof that there is none

Written and committed alone, before any script or number of this lane. Rules: `rebuild_2026_10_22/BRIEF.md`,
`covariant_push_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle (the cold sector is "cold
energy": BS K(Q) dust in v3, AeST's scalar dust in v4). Never "theory closed". Never "the data favour the framework".
No new free parameter is fitted; every addition a route needs is named and counted. No knob scans: every constant a
route needs is either fixed by a stated requirement (a bound, solved for, not scanned) or declared below.
Compute: CFG960 (1024³) and L1's runs may be live. Every run: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS,
minutes. No PM simulation (that is L1's job, `rebuild_2026_10_22/L1_khronon_pm/`). No downloads.

## 0. The trilemma (as handed to this lane; `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1b; F3, H1, H3, I1, C5–C8)

1. Solar-System screening (Cassini Q₂, planets) needs the stiffness γ_L; no unscreened law form passes Cassini and SPARC
   (D7c, E2).
2. γ_L is well posed only with an untwisted (hypersurface-orthogonal) aether (I1: ω² = A k⁴ gives complex roots on any
   slice tilted against the aether above κ_c² = (1−Bw²)²/(4Aw²) − M²w²).
3. The untwisted form (Khronon v3) fails LINEAR growth; the record attributes this to J_x′(0) = −1 (F3 K1(i)).
4. The twisting form (AeST v4) is ill-posed off symmetry (I1) and runs away on FRW for the dust shape tried (C7).

## 1. Assumption / input ledger (classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED /
## STANDARD-MOND-MACHINERY / EXTERNAL-LITERATURE / POSITED)

| ingredient | use here | class | source |
|---|---|---|---|
| BS24 post-Newtonian system (Ξ = φ − σ̇ + …, 4πGρ_τ = −[∇·(J_Y∇Ξ) + μ_K²Ξ], ∇²φ = 4πG(ρ_b + ρ_τ), continuity) | R1 linear kernel for general J′(0) | EXTERNAL-LITERATURE, transcribed via WebFetch (PROVISIONAL, not on disk), self-consistency checked in BSK1 M2–M4 and C4 K1; L1 uses the same system | `real_research/bs_khronon_2026/BSK1_moving_source_gate.py` L15–21; C4 README |
| K(Q) dust: 8πGρ = QK′ − K, c_s² = K′/(QK″) | R1 Jeans identity for general analytic K | FRAMEWORK-NATIVE (C5, F3 K1(ii) A1) | C5, F3 |
| μ_K ≤ 14.8 h/Mpc (μ_K⁻¹ ≥ 100 kpc physical, BS24 Eq. 39) | the cap | EXTERNAL premise (BS24 via WebFetch) | F3 K4/K5 |
| F3's two-fluid sub-horizon growth model (baryons feel all mass; khronon self-term × kernel s), background A (C2 c2b plik-lite refit, g = 1), CLASS 3.3.4 linear P(k) | R1 σ₈ ratios; reproduced first (M0) | FRAMEWORK-NATIVE in the dust limit; plik-lite foregrounds SURVEY-CALIBRATION; F3's start condition (GR modes before a_i) POSITED (optimistic) | F3 script L101–121, L224–239 |
| model B background (CFG886 BAO+BBN: Ω_m 0.2976, h 0.6856) with A's A_s, n_s, ω_b | R1 physical-regime field strengths | FRAMEWORK-NATIVE in the dust limit | F3 K2 model B |
| SPARC rotmod files + Lelli 2016 table, Υ_disk 0.5, Υ_bul 0.7 | x_min (R1a); SPARC cost of R2 candidates | RAW (V, R) + SURVEY-CALIBRATION (distances, inclinations, SPS Υ) | `campaign_fresh_gravity/CFG4_common.py` `load_sparc` |
| spherical enclosed mass M(<r) = r²g_bar/G for SPARC points | R2 SPARC costs only (relative Δlog g between two laws on the same baryons) | POSITED approximation (discs are not spheres), stated | — |
| B21 KiDS isolated lensing RAR (Fig-4-5-C1, Nobins), g_obs = 4G·ESD/bias (B21 Eq. 7) | x_min (R1a), reported with and without B21 | RAW ESD + SURVEY-CALIBRATION (B21's g_bar, SIS conversion); F2: outer isolated signal environment-sensitive (UNDECIDABLE as a law test) | `real_research/data/lensing_rar/brouwer2021_rar/` |
| x_e of the Solar System (C6 inputs: g_e/a₀ = 1.30–2.60 canonical, 1.15–2.15 alt) | R1 Cassini identity; wide binaries | FRAMEWORK-NATIVE / SURVEY-CALIBRATION (MW fields) | C6 json `inputs.E` |
| planet bounds (Earth 8.7e-15, Mars 1.4e-15, Saturn 7e-15 m/s²), Hees 2σ upper 9e-27 s⁻² | R2 Solar System | RAW-derived bounds as used by the record | C6 json `inputs` |
| C6 Q₂ results (max Q₂/Hees upper at 24 pc) | R1 Cassini carry-over | FRAMEWORK-NATIVE | C6 json `R1_physical` |
| E2 AQUAL Q₂/Hees ranges (2.44–4.59 / 2.85–5.19), D7c/E2 family least-tense 1.41 | R2c | FRAMEWORK-NATIVE | E2 json `R1_outcome`, `R3_outcome` |
| C1 planets (a₀ anomaly 1.08e4–8.07e4 × bound) | R2c | FRAMEWORK-NATIVE | C1 json `K6` |
| D10 clusters (Pal 4, Pal 14: L_V, r_h, R_GC, σ_obs), Υ_V 1.6 | R2b ordering | RAW + SURVEY-CALIBRATION | D10 json `clusters` |
| SPARC V_flat (table) | R2b ordering (|Φ| ≥ V_flat²) | RAW + SURVEY-CALIBRATION | SPARC table |
| solar radius, solar mean density, GM_⊙ | R2b | standard constants (IAU nominal) | — |
| solar-wind density n_sw(1 AU) = 5 cm⁻³ ∝ r⁻², local ISM n ≈ 0.1 cm⁻³, HI disc half-thickness h_z bracket 100–1000 pc | R2b3 only | EXTERNAL, NOT ON DISK, labelled; R2b3's verdict is CONDITIONAL on them | — |
| I1 tilted-slice dispersion s² = A p⁴ + B p² + M² | R2 well-posedness ("I1's symbol analysis") | FRAMEWORK-NATIVE (I1 K4) | I1 README §2 |
| ΛCDM machinery, QUMOND phantom, EFE recipe, ν_RAR | none in any verdict | — | — |

## 2. The frozen route list

### R1 — a Khronon J with J′(0) = 0 that equals J_x (μ = x/(1+x)) for x ≥ x_min

Additions vs v3: +1 function shape (J with a Newtonian window f = 1 + J′ = 1 on [0, x_t]), +1 constant (x_t). POSTULATED.
x is the khronon congruence acceleration |∇Ξ|/a₀ (= |∇φ|/a₀ in static systems).

- **R1a (data).** x_min forced by data = the lowest field strength at which a data set *requires* the law:
  - SPARC: the 1st percentile of x_obs = g_obs/a₀ over points with Q ≤ 2, i ≥ 30°, e_V/V_obs ≤ 0.10;
  - B21 isolated lensing RAR: g_obs/a₀ at the lowest-g_bar bin with ESD/err ≥ 3 (reported separately: F2 found this
    signal environment-sensitive);
  - reported as non-forcing: wide binaries (x_e ≥ 1.15), D10 globulars (they demand Newton, x_e 0.07–0.21), E3 dwarfs
    (they demand more than the law).
  - **Theorem T1 (to be checked symbolically):** AQUAL ellipticity/C5 health needs F(x) = x f(x) non-decreasing; with
    F(x) = x on [0, x_t] this forces **x_t ≤ F(x_min) = x_min²/(1+x_min)**.
- **R1b (linear growth).**
  - (i) sympy, from the BS24 PN system: the khronon dust's sub-horizon kernel for f₀ = 1 + J′(0) is
    s(k; f₀) = (μ² − f₀k²)/((1−f₀)k² + μ²), with s(0) = BSK2's μ²/(k²+μ²) and s(1) = Jeans 1 − k²/μ², and
    ∂s/∂f₀ = −k⁴/((1−f₀)k² + μ²)² exactly.
  - (ii) sympy: for K = Σ_{n=2..5} c_n(Q−1)ⁿ with c₂ = μ² and general c₃…c₅, lim_{Q̄→1} 4πGρ/c_s² = μ² (= K″(1)/2): the
    late-time Jeans scale equals the static mass for every K analytic at Q = 1 with K′(1) = 0.
  - (iii) COMPUTED (F3's model A, CLASS P(k)): σ₈ ratio to the dust limit at μ_K = 14.8 h/Mpc for f₀ = 1 (R1) and
    f₀ = 0 (J_x), a_i = 1e-3 and 1e-4; μ_min(σ₈ ratio ≥ 0.95) for f₀ = 1 (a_i = 1e-3) by root finding. Diagnostic only
    (reported, not a verdict): f₀ ∈ {0.01, 0.1, 0.5}.
    **PASS line (R1 linear growth, F3's line): σ₈ ratio(f₀ = 1, a_i = 1e-3) ≥ 0.95 at μ_K ≤ 14.8 h/Mpc.**
  - (iv) physical regime: rms khronon-relevant field strength x_N,rms(a) of the dust-limit linear field restricted to
    a·μ_K < k < 10 h/Mpc (the modes whose kernel differs from 1), model B, both footings, a ∈ {1e-3, 3e-3, 1e-2, 3e-2,
    0.1, 0.3}; plus the same with the f₀ = 1 suppression applied (a lower estimate). The Y = 0 expansion is **the
    physical expansion** only if x_N,rms ≤ x_t,max at some a with a non-empty k range; otherwise it is **not**, and the
    Maxwell fraction P(x < x_t,max) = erf(z/√2) − √(2/π) z e^{−z²/2}, z = √3 x_t,max/x_rms, is reported. Reported only
    (ESTIMATE, not a verdict): a mean-field WKB σ₈ ratio with f_t(a) = f(x̄) + x̄f′(x̄)/3 at x̄ = x_N,rms(a).
- **R1c (health and Cassini).**
  - (i) an explicit monotone R1 construction (x_t = x_t,max/2; smoothstep bridge on [x_t, x_min] from F = x_t to
    F(x_min); J_x above x_min) satisfies C5's conditions 0 ≤ f ≤ 1 and 0 ≤ F′ ≤ 1 on a log grid 1e-8 ≤ x ≤ 1e4.
    f = 1 on [0, x_t] is C5's edge M_T = 1/(1−f) = ∞ (P frozen, W not C² at P = 0): reported as a flag.
  - (ii) Cassini: the screened Solar System's response (C6 kernel) depends on the law only through f and F′ at x_e. At
    C6's x_e cells R1's f, F′ equal J_x's to ≤ 1e-12 (relative), so C6's Q₂ and the planets' hedgehog carry over.
    **PASS line: identity ≤ 1e-12 and C6's max Q₂/Hees upper ≤ 1.**
- **R1 verdict rule.** WAY THROUGH iff R1b(iii) PASS and R1c PASS. NO-GO iff R1b(iii) FAILS; it is then stated as a
  theorem for the class C_R1 = {BS Khronon (BS24 PN system), f₀ ∈ [0, 1] (C5's healthy range), K analytic at Q = 1 with
  K′(1) = 0, μ_K ≤ 14.8 h/Mpc}, with the kernel monotonicity (i), the K-shape identity (ii) and the computed σ₈ ratios.
  If R1b(iv) finds the Y = 0 expansion is not the physical one, the residual question (growth driven by the law's own
  nonlinearity, the same for J_x and R1) is labelled **DEFERRED TO L1**.

### R2 — screening without γ_L that tolerates a twisting aether (v4: AeST + C1's capped F, i.e. μ = x/(1+x) exactly)

Common tests for every candidate, both footings:
- **(S) Solar System:** the anomalous acceleration at Earth, Mars, Saturn ≤ the C6 planet bounds, and Cassini Q₂ ≤
  Hees 2σ upper.
- **(W) well posed with a twisting aether** (I1's symbol analysis): the principal symbol is second order (A = 0 in I1's
  tilted-slice quartic, so κ_c = ∞) with a Lorentzian cone, and no Ostrogradsky (higher-time-derivative) ghost.
- **(G) galaxies:** at the constant (S) requires, the median Δlog₁₀ g over SPARC points with g_bar < 0.1 a₀
  (spherical M(<r), relative to the law on the same baryons) has |median| ≤ 0.05 dex.
- **Theorem T2 (to be checked):** in AeST's (and A33's) static sector g = u + R(u), with M_L = dg/du = 1 + R′(u)
  (C5); C5 health M_L ≥ 1 ⇒ u is non-decreasing in g. Hence, if the law holds up to x₉₉ (the 99th percentile of SPARC
  x_obs), the planets' unscreened anomaly is ≥ u_floor = a₀x₉₉/(1+x₉₉). Reported: u_floor / planet bounds.

Candidates (frozen; additions counted):
- **R2a Vainshtein (Horndeski galileons of the AeST scalar χ):** L₃ = (∂χ)²□χ (+1 term, +1 constant r₃),
  L₄ = (∂χ)²[(□χ)² − (∇∇χ)²] (+1 term, +1 constant r₄), L₅ (+1 term). Static spherical reduction (sympy): the χ
  equation integrates to R(u) + (r₃/r)u²/a₀ + (r₄/r)²u³/a₀² = g_N (L₅ drops out); galileon terms are blind to a uniform
  external gradient. (S): the minimal r₃, r₄ that bring each planet under its bound (solved, not scanned); (G) at those
  values. The combination L₃ + L₄ is bounded by the single-term cases near the Sun (stated, checked numerically).
- **R2b density/curvature-keyed couplings:**
  - b1 source-potential (thin-shell; chameleon/symmetron-type; +1 field, +1 function, ≥ 2 constants): ordering test.
    Must screen: Sun (GM_⊙/R_⊙c²), Pal 4, Pal 14 (GΥ_VL_V/r_h c², D10's inputs). Must not screen: every SPARC galaxy
    (|Φ|/c² ≥ V_flat²/c²). FAIL for every monotone rule if min(must-screen) < min(SPARC) (increasing rule) and the Sun is
    deeper than the shallowest SPARC galaxy (decreasing rule).
  - b2 body-density (Hui–Nicolis–Stubbs-type; +1 function, +1 constant): the Sun is a main-sequence star; a rule that
    screens it as a MOND source screens disc stars. (G) cost: the anomaly sourced by gas only, g = g_bar + u_law(g_gas),
    on SPARC deep points with V_disk² > V_gas². The test-body variant is reported with its external premise (Pal 4/14
    and dSph velocities are both measured on giants).
  - b3 field-point ambient density (pointwise T-coupling; +1 function, +1 constant): CONDITIONAL on the external inputs
    of §1: FAIL if > 50 % of SPARC deep points lie inside R_HI (Σ_HI ≥ 1 M_⊙/pc², n_HI ≥ Σ/(2h_z m_H)) with n_HI above
    the solar-wind density at Saturn's orbit, for h_z = 300 pc (bracket 100–1000 pc reported).
  - b4 curvature: R-keyed ≡ b3 (sympy: R = 8πGρ/c² for dust); Weyl-keyed (+1 function, +1 constant): (W) sympy toy,
    a term ε(∂∂h)² added to (∂h)² gives a second pole with residue of opposite sign (Ostrogradsky ghost). The Weyl
    contrast Sun-at-Saturn / galaxy outskirts is reported (it would screen, which is why the ghost decides).
- **R2c capped W / law form / k-mouflage (+0 terms, an F choice):** T2 + E2's Q₂ ranges and C1's planets (read and
  reproduced from the JSONs).
- **R2 verdict rule.** WAY THROUGH iff some candidate passes (S), (W) and (G) on both footings. Otherwise NO-GO, each
  candidate's obstruction stated for its class.

### R3 — v4's FRW runaway escape (C7: a different early K(Q), or Q₀ ≳ 30 Mpc⁻¹)

Run only if R2 has a WAY THROUGH (v4 also needs a healthy screening term). If R2 is NO-GO, R3 is reported **MOOT** and
not computed.

## 3. Checks (`m1_trilemma.py`, one line each, exit 0 iff all pass)

- **M0 reproduction (before any verdict):** this lane's own two-fluid integrator gives F3's K4 σ₈ ratios at μ_K =
  14.79771 h/Mpc (Jeans 0.12055 / 0.035747, BSK2 0.39080 / 0.20260 for a_i = 1e-3 / 1e-4) within 1 % relative, and
  μ_min(Jeans, 1e-3) within 2 % of 411.10 h/Mpc.
- **M1** sympy R1b(i): kernel, endpoints, ∂s/∂f₀, residuals 0.
- **M2** sympy R1b(ii): K-shape limit, residual 0.
- **M3** data loaders: 175 SPARC rotmod files; B21 conversion equals the README formula; x_min finite and positive.
- **M4** CLASS self-consistency (model B): own σ₈ integral vs CLASS σ₈ ≤ 1e-3.
- **M5** R1c(i) health grid all pass, and R1c(ii) identity ≤ 1e-12.
- **M6** sympy R2a reduction (4ru², 4u³, L₅ → 0, uniform gradient drops out) and I1's tilted-slice discriminant
  (κ_c² as quoted; κ_c → ∞ as A → 0⁺ for Bw² < 1).
- **M7** sympy T2: M_L = 1 + R′(u); for the capped R = u²/(a₀−u), R′ ≥ 0 on [0, a₀).
- **M8** record numbers reproduced: C1 K6 ratio = a₀/bound (≤ 1e-6 relative); E2 R1_outcome ranges read.
- **M9** sympy Ostrogradsky toy: residues of 1/(k² + εk⁴) are +1 and −1.
- **M10** peak RSS < 1 GB.
- **MUTATE** (`M1_MUTATE=1`, outputs `*_MUTATE.*`): (a) the sign of J_Y in the PN hold equation is flipped (M1 must
  fail); (b) the cubic galileon is reduced with r⁰ in place of r (M6 must fail).

## 4. Verdict words per route

WAY THROUGH (route, additions counted, all four trilemma conditions met with numbers); NO-GO (the obstruction, as a
theorem for a stated class); DEFERRED TO L1 (nonlinear); MOOT (R3 only). A route may carry NO-GO for its stated part
and DEFERRED TO L1 for a residual that it shares with v3, each stated with its number.
