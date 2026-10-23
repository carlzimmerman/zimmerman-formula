# The screened theory, v3 (DRAFT — finish line of the 2026-10-22 pushes)

Status words: DERIVED (from listed premises), COMPUTED, POSTULATED, FITTED, OPEN, PENDING (lane running).
κ = ½ FITTED. Footings: canonical a₀ = 9.36e-11 m/s², alt 1.13e-10 m/s², never pooled. No dark-matter particle.
Never "theory closed". Every line cites the lane whose committed script backs it.

## 1. The action (one line)

The Blanchet–Skordis Khronon theory (arXiv:2404.06584) in its literal healthy form (C4, C5):
- metric g, khronon τ (preferred foliation), an independent spatial covector P,
- free function J chosen so the static limit is AQUAL with μ = x/(1+x) exactly (C4; this J lies outside BS's
  admissible class — POSTULATED),
- β = 0, η = 0 (no P kinetic term; η > 0 is ill-posed, C5),
- Blanchet–Skordis K(Q) dust sector (C4, C5),
- one stiffness term −(γ_L/2)(D·P)², γ_L = K L★²/2 (C1, C3, C4: absent from both AeST and BS; POSTULATED).

DSF-21's A33 is this theory with η > 0, which C5 shows is ill-posed; v3 drops η.

## 1b. A better-surviving candidate found overnight: AeST + γ_L with the capped F ("v4")

Lanes H1, H2, H3 (`rebuild_2026_10_22/`, all reproduced by the coordinator):
- The Skordis–Złośnik AeST action with C1's capped free function (static limit = the canonical law μ = x/(1+x) exactly)
  plus the same single stiffness term γ_L passes **growth** (the Newtonian term survives in the IR for any F:
  Γ²(k→0) = 4πG̃ρ̄ — unlike v3's Khronon J with J′(0) = −1), **the RAR** (exact law), **Cassini** (≤ 7e-8 of Park),
  and **BBN** (λ_s = ∞).
- Its only "health failure" (C5) is **not a ghost** (H3): the same energy criterion flags ordinary Newtonian dust and
  GR + k-essence dust, so it was mis-specified; the AeST mode is non-propagating dust, ghost-free at linear order, with a
  growth rate bounded by √(4πG̃ρ̄) and a band that ends at k_c ≈ 243 μ. Not "only ordinary gravity": between μ and k_c
  the binding is AeST's contact-term static law (up to 2.3×10⁴ × Newton near k ≈ 185 μ) — its consequences for
  small-scale structure are OPEN.
- It does **not** fix cluster cores: AeST's static (hydrostatic) dust has the wrong radial shape (H2).
- OPEN: C5 defect (b) (γ_L gives no causal cone), an FRW linear run with C7's patched CLASS at this F, nonlinear
  behaviour, strong field.

Net: v4 keeps everything v3 passed and removes v3's growth failure at linear order; clusters stay red in both.

**Update (I1, 23 October, reproduced): v4 is ILL-POSED wherever the aether twists.** The γ_L term gives a real dispersive ω ∝ k² scalar (ω² = A k⁴ + …). On aether-orthogonal slices (Minkowski, FRW, exact spherical symmetry) the Cauchy problem is well posed; on any slice tilted relative to the aether two roots go complex above κ_c ≈ 1/(2√A w) — Hadamard ill-posed. v4 *needs* a twisting aether to give the law off symmetry (C1), so every non-symmetric bound system (the Sun in the Galaxy's field, discs) has no good slice; relayed signals can close loops in time (criterion B violated in principle; illustrative loop gains 4 ms–3.9 s around the Galaxy). No completion found: a (□φ)² partner keeps the statics but adds an Ostrogradsky ghost; a hypersurface-orthogonal aether is v3, which fails growth. **So neither v3 nor v4 is a complete, healthy theory: v3 fails growth, v4 fails well-posedness off symmetry (I1) and runs away on FRW for the dust shape tried (C7).** The trilemma inside these two families: Solar-System screening needs γ_L; γ_L is well posed only with an untwisted (hypersurface-orthogonal) aether; the untwisted (Khronon) form fails linear growth unless the BS dust mass exceeds its allowed cap. The one undecided escape for v3 is nonlinear: a Khronon-native PM (F3 §6).

## 2. Parameters

| symbol | status | value | source |
|---|---|---|---|
| a₀ (κ) | FITTED | κ_Λ = 0.417 ± 0.095 (CFG493); Planck-free 0.414 ± 0.094 (E4) | thermal Z/4π is Milgrom's relation, a POSTULATE (A75) |
| L★ | FITTED, new constant (lower bound only) | EFE-aware native floor L★_95 = 21.7 pc (canonical) / 22.9 pc (alt) with the SPS Υ_V prior; 2.9–22.7 / 4.4–23.8 pc across Υ_V priors and the MW bracket (D10). Upper edge ~90 pc (LITTLE THINGS) | D10, E4, C3 |
| dust abundance (Ω_c-like) | FITTED (initial condition) | — | C2, C4 |
| u | measured function of scale, convention-dependent | 0.43–0.50 (E4, E1) | no mechanism (D6) |
| G_cosmo/G_N | bounded | Planck-lite ±0.027 (C2 emulation); BBN | C2 |
| μ_K (K(Q) mass of the BS dust) | FREE, and **no allowed value** (see §3 growth) | BS24 Eq. 39 caps μ_K ≤ 14.8 h/Mpc; keeping σ₈ within 5 % of the dust limit needs μ_K ≥ 361–2542 h/Mpc — a gap of 24–172×; full Boltzmann (Q6) needs μ_K > 2542, and the literal quadratic K is BBN-excluded below 1.84×10⁸ h/Mpc (no radiation era) | F3 |

## 3. Tests

| test | result | lane |
|---|---|---|
| galactic law (RAR) | the law itself (AQUAL μ = x/(1+x)) | E2, C4 |
| health (ghosts, gradients) | CONDITIONALLY HEALTHY in literal form; tensor modes at c | C5 |
| instantaneous constraints / well-posedness | WELL-POSED (weak-field leaf problem: one strictly convex functional, elliptic for all u < a₀, unique for γ_L > 0) + UNCONSTRAINED (binary pulsars: no radiative channel, ≤ 3e-14 of the double-pulsar error; GW speed exactly c). Violates criterion A by a real but tiny signal; meets criterion B. OPEN: infinite-volume theorem, coupled GR + leaf + dust, strong fields | C8 |
| Cassini Q₂ | healthy literal form (γ_F = 0): all 24 cells pass Hees and Park; Q₂ 0.93–1.86e-34 s⁻² at 24 pc, 1.8–3.5e-36 at 90 pc (2.8e7–5.1e9 inside); hedgehog has no quadrupole. Frozen rule reads UNDECIDED on one float-cancellation check (identity exact in sympy). Unscreened law fails 2.4–5.2× (E2) | C6, D7d, E2 |
| planets | hedgehog GM/L★²: at 24 pc Mars 0.17, Saturn 0.035, Earth 0.028 of their bounds | C6 |
| wide binaries 20 kAU | screened γ_v − 1 ≈ 8e-6 vs law-first 1.167/1.199; DR4 decides (σ_sys rule A3) | D2, D7d, E2 |
| outer globulars | unscreened law (L★ = 0) excluded in all 18 cells (Δχ² 4.9–22.8); no finite L★ beats Newton; sets the L★ lower bound (Pal 4, Pal 14 dominate; Υ_V-limited) | D10 |
| dwarf satellites | +0.89 dex above screened prediction (E3). Pre-infall retention rule (PAPER36, ζ = 1 inside r_tidal; G2): FAILS on native inputs (+0.92 / +0.89 dex; the retained cold energy pays the phantom first, nothing is left over); it closes only with ΛCDM's subhalo mass put in by hand (Moster+13 + NFW), still overshooting 8 systems, and DF2/DF4 do not get ζ = 0 from the rule. Supply: the framework's dynamics cannot fix a satellite's catchment (it needs the patch's initial overdensity and infall epoch — UNDECIDABLE); the satellites' own [Fe/H] (leaky box, no ΛCDM input) gives ≥ 38× present baryons, enough (median need 0.21 of supply), with 6/36 short at central values and none at 2σ — CONDITIONAL on ζ = 1 winds and no pre-enrichment | E3, E6 |
| CMB / linear P(k) | a₀ absent at linear order (tests dust + G ratio only); native spectra: see the Q6 row (literal K has no radiation era; growth fails at the cap) | C2, C7 |
| cosmic shear (native PM) | canonical settling rules excluded by raw KiDS (CFG596); CFG960 rerun PENDING | CFG596, CFG960 |
| **linear growth of the v3 theory** | **FAILS as written.** With J_x, J′(0) = −1 exactly, so the Newtonian term vanishes on FRW; GR-on-dust growth holds only for k < aμ_K. Inside BS's allowed μ_K (≤ 14.8 h/Mpc) linear σ₈ is 0.03–0.32 (0.04–0.39 of the dust limit); above it the dust forms galaxy halos and double-counts against the law (CFG946). Whether the cubic deep-MOND term restores growth needs a Khronon-native PM (spec in F3 §6). In the μ_K → ∞ limit, linear S₈ = 0.814–0.845 is CONSISTENT with raw KiDS on k ≤ 0.3 h/Mpc points (0.9–1.5σ). The earlier 15–19 % excess and CFG596's Δχ² +68.7 belong to the settling rules and QUMOND phantom, which v3 does not contain | F3 |
| isolated-galaxy lensing, outer (F2 rebuild) | **frozen verdict REAL FAILURE, not robust → UNDECIDABLE.** The record's Δχ² +100 came from the catchment supply edge, which v3 does not have; without it the far-outer amplitude is 0.96–1.04 of the data (1.1–2.6 Mpc). The 0.4–1.1 Mpc range is short (A 1.39) in the frozen photo-z-isolated sample, but a wider host veto removes it (1.25 ± 0.25 / 0.82 ± 0.16) and opens an isolation hole beyond 1.1 Mpc; the 'isolated' stack's outer signal moves 8.6σ with the isolation cut. The external field makes the outer prediction much worse (A_O2 4.5–12 with on-disk fields; data tolerate y_e ≲ 3e-5). All record two-halo terms are ΛCDM-built or knob-carrying. Decidable only with a native many-body stack or a large spectroscopic isolated sample | F2 |
| cluster cores (F1 rebuild, 326 eRASS1 × raw KiDS, re-extracted and reproduced) | **REAL FAILURE of the law on baryons.** A_MID (0.3–1 Mpc, data/law) 1.68–1.85 canonical / 1.54–1.70 alt, Z ≈ +5–6; most favourable corner still +2.5–4σ. Field equation (AQUAL vs QUMOND), native h, gas calibration, R500 and miscentring each move it ≤ 4 %. Any added cold profile that fixes MID overshoots the outskirts (incl. the record's settled c* = 0.40, which is ΛCDM-built). The theory's dust inside 1 Mpc is NOT DERIVED | F1 |
| old engine's growth excess (G1) | grows with grid resolution (0.040 / 0.077 / 0.163 at 128³ / 256³ / 512³) — the old 256³ pass was not converged; a smooth cap makes it worse; not inherited by v3 | G1 |
| AeST route (H1) | NONE IN SZ's FAMILY passes all five (health at Y = 0, growth, RAR, Cassini, BBN): health at Y = 0 depends only on λ₀ = F_Y(0)/(2−K_B), which SZ's MOND limit sets to 0; SZ's own interpolants lose to the canonical law on SPARC at the BBN edge (z −2.4 to −3.6). C1's capped F (exact canonical law) passes growth, RAR, Cassini and BBN and fails only health — and theorem T1 says that 'health failure' is the dust's Jeans growth mode. **Whether that is a mis-specified criterion or a real defect is being tested hostilely (H3).** AeST's Newtonian term survives in the IR for any F (Γ²(k→0) = 4πG̃ρ̄), unlike v3's Khronon J | H1, H3 |
| AeST cluster mass (H2, reproduced on an independent KiDS extraction) | **CANNOT supply the core excess.** AeST's static mass term is its hydrostatic dust; it ramps across 0.3–1 Mpc and oscillates negative outside, where the data need ~1.7 flat then ~1. Best profile χ² 27.7–39.6 (law alone 27.3–41.8; pass 11.07); with the outskirts held, the core lifts only ×1.02–1.30. A CDM-like branch of AeST's dust needs a native AeST N-body code | H2 |
| potential-depth selector a₀(1+|Φ|/Φ_*) (J1, reproduced) | **FAILS.** Not in either action (a constant lapse is a time rescaling); as a postulate it fixes the cluster MID band but overshoots the outskirts (data 0.60–0.62 of prediction, Z −6.6 to −7.8; |Φ| is nearly flat across a cluster) and does nothing for the satellites (+0.84–0.89 dex left; satellites sit in shallower total potential than the Sun, and screening caps the boost) | J1 |
| owner's idea: cold energy as a 'dip into another dimension' (braneworld Weyl term; K1, reproduced) | **FAILS** for every closure on both footings. The brane equations leave the Weyl anisotropic stress free; at low energy baryons do not source the Weyl term, so its size is a bulk choice. P = 0 closure = H2's μ²Φ term (10¹² short under BBN; ramps outward); Harko–Cheng fails the outskirts, isolated galaxies and planets; the tidal-charge ('black hole on the brane') closure is the only compact one and comes closest on the cluster profile (χ² 7–16 vs 11.07) but overshoots dwarfs by 2.4 dex and the planets by 10²⁰. RS2 (ℓ ≤ 0.1 mm) is 10⁵¹ too weak; DGP boosts light systems more than clusters. On FRW the Weyl term is dark radiation, not growth dust | K1 |
| v4 native CMB / linear P(k) (C7 patched CLASS, reproduced) | **v4 RUNS AWAY on FRW** for the dust shape tried (Cosh, Q₀ = 0.1 Mpc⁻¹): P/P_ΛCDM 10²–10⁴¹ by k ≤ 10 h/Mpc in every v4 configuration; gauge- and tolerance-stable, so not numerical. Likely a tachyonic vector pair before z ≈ 78 (rate² ≈ 8πG̃ρ̄/K_B). Untested escape: a different early K or Q₀ ≳ 30 Mpc⁻¹. SZ21's own benchmarks reproduce their fit at g = 1 (Δχ² +0.16 / −0.09 vs ΛCDM) but Cosh fails at its physical g = 0.75 (Δχ² +119, H₀ 55.6) | C7 |
| owner's tidal-charge term screened by L★ (M2, reproduced) | **FAILS.** L★ screening never touches cluster scales (cluster ℓ_g ~ 1e-3–1e-2 pc), so the cluster shape is K1's (OUTER 0.75–0.80, inner overshot); dwarfs over by −1.2 to −2.1 dex residual; inside ℓ_g the term renormalises each mass (Sun's GM ×9–172), and Mars is 2e2–6e4× its bound; growth-breaking on FRW (G_eff/G − 1 = 22 at z = 1100). Lesson: anything attached to every mass element acts like a halo on small systems; the cluster component must have its own scale between galaxies and clusters | M2 |
| dwarf cold supply, MDF test (P1, reproduced) | **SUPPLY CONFIRMED for the median, not robust at 2σ.** E6's ζ = 1 premise fails on the metallicity-distribution width (10 systems too narrow; AD test rejects the ζ = 1 shape in 4 of 6 well-sampled systems), but the supply survives because for any ζ ≥ 1 the catchment is set by the MDF's metal-poor end: median supply/need 0.46 (canonical) / 0.45 (alt); 10 systems short at central values (none robustly); with every width at its 2σ-low end the median is 1.12 / 1.08. Pre-enrichment raises the supply (reverses E6's caveat). Supply ≠ mechanism: nothing binds the cold energy inside r₁₂ (G2) | P1 |
| **ERRATUM (M1, 23 Oct, reproduced)** | **v3's linear growth failure is caused by the BS cap on μ_K, not by J′(0) = −1.** The exact dust kernel (BS24 PN system) is s(k; f₀) = (μ² − f₀k²)/((1−f₀)k² + μ²), f₀ = 1 + J′(0): J_x (f₀ = 0) gives μ²/(k²+μ²), J′(0) = 0 gives 1 − k²/μ²; both → 1 as k → 0, so the Newtonian term survives on large scales in v3 too, and J_x holds the dust *better* than J′(0) = 0 (σ₈ at the cap 0.391 vs 0.121). Every statement in this draft, F3's README, the board and PAPER59 that blames J′(0) = −1 is superseded by this row. Reaching σ₈ ≈ 0.95 needs μ_K ≥ 411 h/Mpc, 27.8× the BS cap; no analytic K shape escapes (late Jeans scale = K″(1)/2). The trilemma stands: no screening without γ_L passes (galileons, potential/density/Weyl keying all fail; Theorem T2: healthy laws matching SPARC leave planets ≥ 0.96 a₀). v3's one open escape is nonlinear (L1) | M1 |
| inner galaxy lensing (blue) and red lenses, recomputed for v3 (S2, reproduced) | **both CONDITIONAL, provisional until S4's μ_K² term.** Blue: data/v3 0.88 (canonical, PASS-fragile) / 0.80 (alt, 2.9σ short) at the primary external field; the EFE moves it ≤ 0.004 in this window; the hot-CGM fraction and M★ decide it (f_hot = 0 → PASS on both footings). Red: inventory alone 1.31 / 1.20 short; with CFG667 + the IMF α–σ posit 1.02 / 0.93, consistent; fails canonical at M★ −0.2 dex | S2 |
| hosted small systems with v3's EFE solved (S1, reproduced) | **both FAIL.** Dwarf satellites +1.33 / +1.30 dex above v3 at the L★ floor (+1.36 / +1.31 at 24 pc, +1.72 / +1.68 at 90 pc) — supersedes the +0.89 dex quoted above, which used isolated screening without the host field; the EFE costs +0.58 dex. Coma UDGs UNDEC → FAIL, +1.12 / +1.08 dex at z +4.3–4.7 (isolated they sit 1.5σ off). Rests on equilibrium in the present host field | S1 |
| outer lensing, spectroscopic isolation (P2, reproduced) | **UNDECIDABLE (N too small)**: 2,251 GAMA host-vetoed lenses separate zero-field vs catalogue-field v3 by only 0.9σ; ~22,000–26,500 needed. The data sit 2.8–3.0σ BELOW zero-field v3 and are consistent with the catalogue's own field (y_e ≈ 6.6e-5), so F2's 'tolerates only y_e ≲ 3e-5' does not survive spectroscopic isolation. Inner range (ungraded): 1.83 / 1.68 × v3 inside 0.31 Mpc | P2 |
| v3 native background, CMB and P(k) (Q6; sympy derivation reproduced 19/19) | **Literal v3 has no radiation era.** BS24's quadratic K = μ_K²(Q−1)² carries a stiff a⁻⁶ partner whose amplitude is fixed by today's dust density (ρ_stiff/ρ_dust ∝ (H₀/μ_K)² a⁻³). It beats radiation before z = 1854 (μ_K 14.8 h/Mpc) up to 3.2×10⁵ (2542). BBN (ΔN_eff,equiv ≤ 0.5 at 1 MeV) needs μ_K ≥ 1.84×10⁸ h/Mpc, 1.2×10⁷ × the BS cap; an independent coordinator estimate gives ~2×10⁸. On a dust background with the literal perturbations (LOB, not the literal theory), full Boltzmann growth at the cap gives σ₈ = 0.061 (R_B 0.073, against F3's ODE 0.391), and 5 % growth needs μ_K > 2542. plik-lite Δχ² vs ΛCDM runs +13891 down to +18.7 over μ_K 14.8–2542. Caveat: the frozen V2/V3/V5 gates failed where LOB's spectrum is 10⁻³–10⁻⁸ of ΛCDM's; the post-result A3 gates pass. BS25's DBI K is the literature's early-time cure; whether it also fixes growth is lane Q7 | Q6, Q7 |
| ALMA U4/GS4 | expected unscorable (S/N 0.04–0.58); sealed, all three kernels harness-ready | D4, CFG942 |

## 4. Sealed predictions for data still to come

- **Gaia DR4 wide binaries (20 kAU):** screened γ_v − 1 = 8.1e-6 / 1.9e-6 / 5.8e-7 at L★ = 24 / 50 / 90 pc (C6) vs law-first AQUAL 1.167 / 1.199 (canonical / alt, primary g_ext; E2); scored on whole-catalogue γ̂ under σ_sys rule A3 (owner decision 3d82af0a7e).
- **ALMA U4 (2026-11-06) / GS4 (2026-11-28):** CFG806/CFG809 frozen plans + addendum E (ffb14e40bc); nu_mono verdict, n1/n2 parallel readings (harness 92fa9f9471); expected unscorable (D4).
- **Native CMB:** PENDING C7 (AeST patch; tests the dust sector and G_cosmo/G_N only).

## 5. What this is not

**Growth is the open wound:** as written, v3 has no μ_K that gives both the law and normal structure growth (F3). Not a UV completion. Not derived constants: κ, L★ and the dust abundance are fitted. The CMB cannot test
the galactic law at linear order. Dwarf satellites are an open tension.
