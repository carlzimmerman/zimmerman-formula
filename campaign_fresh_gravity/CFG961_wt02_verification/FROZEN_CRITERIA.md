# CFG961 FROZEN CRITERIA: independent check of WT-02 / WT-05 against CFG938 and PAPER57

Block CFG960–969 (LEDGER reservation row CFG960–969, commit 89bccf7d3, "CFG961 … other sessions please skip").
Frozen 2026-10-21, committed alone before any script of this lane exists. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s²
are never pooled. Cold energy is gravitating mass; no particle species is added. Not "theory closed". Nothing here says the data
favour the framework.

## 0. What is checked, and the record it is checked against

Claims (source what_is_time/WT-02_preferred_time, 9b3d77382, criteria b85749d1c; WT-05_arrow_of_time, 80b5def28):
- **(a)** CFG938's covariant parent is ill-posed off static backgrounds: S1d absorbs ρ̄ through the slice-projected −3Hχ̇ term,
  so on FRW χ obeys a forward heat-type equation and λ a backward one (Re σ = c²k²/3H), Hadamard ill-posed, also for contracting
  media. CFG938's "linearly well-posed" then holds only on flat static space.
- **(b)** CFG938 A5 "c_T = c (structural)" is wrong: the ττ term carries Christoffel² terms, c_T − c = 0.75 L*²u²/c⁴; GW170817
  passes on the path average; the local limit is at L* ≈ 1 kpc.
- **(c)** χ̄(t) is a hidden cosmic clock, u_v ≈ (Ω_c H0/2) v ≈ 1.1e-3 a0 at 370 km/s; does it create a preferred-frame effect the
  record's tests would see?
- **(W5)** WT-05's statements about CFG955 and CFG958: do they change a recorded class (LEDGER rows CFG955 115054648, CFG958
  0a02ca789)?

Record used (read only): CFG938's DERIVATION.md / README.md / cfg938.py (the action, S1d, S5a–S5d, S4, A5); LEDGER rows CFG938,
CFG941, CFG955, CFG958; THEORY_CANONICAL_2026-10-18.md note on CFG938; THEORY_CANONICAL_2026-10-21_DRAFT.md §3.6 and obligation 9;
PAPER57 (qwen_claude_field_theory/papers_2026/PAPER57_cold_sector_structure_2026.tex, lines 24, 52, 206; DOI 10.5281/zenodo.23532885);
the record SPARC file real_research/data/sparc_data/NGC3198_rotmod.dat (Υ = 0.61); CFG4_common.A0; LEDGER line 38 (h72 KiDS √-tail
end bounds 1.67 / 2.07 / 3.44 / 2.77 Mpc for M_b 1.50e10 / 3.66e10 / 6.01e10 / 9.13e10 M☉).
WT-02's and WT-05's code is read only to learn what was claimed; none of it is imported, copied or run.

## 1. The action as written (CFG938 §3.4) and the reading used

S = ∫√−g [c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²) τ_μν τ^μν + λ(D_μD^μχ − Kmn)] + S_b, with
D_μD_νχ ≡ h_μ^α h_ν^β ∇_α∇_βχ, D²χ ≡ h^{μν}∇_μ∇_νχ, u² = h^{μν}∂_μχ∂_νχ, τ_μν = D_μD_νχ − ⅓h_μν D²χ, h^{μν} = g^{μν} + u^μu^ν,
W_full = [−a0u − a0² ln(1 − u/a0)]/K, γ = KL*²/2, K = 4πG. This is the reading CFG938's S1d uses (D²χ̄ = −3Hχ̄̇ on FRW) and
the one cfg938.py implements (DD = h·∇∇χ·h). If any step needs a different reading it is named and run as a MUTATE, not substituted.

## 2. (a) Linearised system on flat FRW (own sympy derivation)

**Setup (fixed now).** Coordinates (t, x, y, z), x⁰ = t, c explicit. Metric ds² = −c²(1 + 2Φ/c²)dt² + a²(t)(1 − 2Φ/c²)dx²
(one Newtonian potential, Φ = Ψ, quasi-static gravity L_g = −c a³|∂_xΦ|²/(2K a²) per coordinate volume; declared model, gravity is
O(k⁰) relative to the k² terms). Medium labels φ¹ = x − εξ(t, x), φ² = y, φ³ = z; u^μ ∝ ε^{μαβγ}∂_αφ¹∂_βφ²∂_γφ³; n = √det B.
χ = χ̄(t) + εδχ(t, x), λ = εδλ(t, x) (λ̄ = 0: CFG938's "no tether background"). Expand every covariant piece to O(ε²); the O(ε)
part must vanish up to total derivatives, the background equation D²χ̄ = Kρ̄ and the k = 0 (Jeans) term. W_full enters as u²/2K
at O(ε²). Euler–Lagrange equations for (δχ, δλ, ξ, Φ); frozen coefficients at one instant (a = 1, ȧ = H, Ḣ kept as a symbol,
χ̄̇ = −Kρ̄c²/3H from S1d, χ̄̈ from ρ̄ ∝ a⁻³); plane waves e^{ikx+σt}; determinant D(σ, k) = 0.

**Backgrounds.** z = 0 and z = 10 with the declared inputs CFG938 used (Ω_b 0.0493, Ω_c/Ω_b 5.364, H0 67.4, flat, Ω_Λ = 1 − Ω_m,
radiation neglected), both L* ends (24 pc, 1 kpc); expanding (H > 0) and contracting (H → −H, same |H|, χ̄̇ sign from S1d);
comoving k from c/k = 100 Mpc down to 24 pc. Primary run with gravity on; secondary with Φ ≡ 0; their classes must agree.

**Outputs.** (i) the χ and λ equations, with the sign of the ∂_t coefficient relative to the −k² coefficient in each
(FORWARD-parabolic iff the same sign as a heat equation u̇ = +D∇²u with D > 0, BACKWARD iff opposite); (ii) the roots σ(k);
(iii) the slope d ln max Re σ / d ln k over the top decade of k; (iv) the growing root's ratio to c²k²/(3|H|a²).

**Hadamard rule.** ILL-POSED iff max Re σ(k) → +∞ as k → ∞ (slope 2.00 ± 0.02 and max Re σ ≥ 100 |H| at c/k ≤ 1 Mpc) on that
background; WELL-POSED (linear) iff max Re σ is bounded uniformly in k (≤ 10 |H| over the whole k grid); otherwise UNRESOLVED.

**H → 0 / K tests for (a).**
- **K-a1 (singular limit).** With χ̄̇ treated as an independent symbol X: the σ-polynomial's leading coefficient must vanish as H → 0
  (its degree drops), the two fast roots must scale as ±c²k²/(3H) and leave to infinity, and at H = X = 0 the remaining roots must
  equal the static dispersion with u0 = 0 (σ² = −γρ̄k² for the pure medium, plus the O(k⁰) gravity/tether terms). PASS iff all three
  hold symbolically.
- **K-a2 (CFG938 S5a reproduced).** Static flat medium with a uniform background gradient u0ẑ (WKB, as CFG938): own quadratic action
  → ω² = γρ0k² + Kρ0[R′(u0)cos²θ + (R(u0)/u0)sin²θ] at c → ∞, R = u²/(a0 − u), with the z-inertia ρ0 − D(u0)u0/(Kc²), D = KW′.
  PASS iff sympy difference = 0.
- **K-a3 (slip).** s_∇ = 4πG r|p_r|/(c²g), p_r = −W_full(u) on the law, for CFG847's five systems (point masses 1e7 @ 0.3 kpc,
  6e10 @ 10 and 100 kpc, 1e12 @ 300 kpc, 1.5e14 @ 1 Mpc), both footings, W-only row. PASS iff worst value 5.8e-6 within 2% and every
  row within 2% of CFG938's printed W-only s_∇.
- **K-a4 (NGC 3198 law unaffected).** Static spherical Euler–Lagrange from E[M_c] (own sympy) solved at all 43 radii (Υ = 0.61);
  PASS iff max |g/g_law − 1| < 1e-6 on both footings, and the FRW term −θ u·∂χ is shown to vanish identically on a static
  background (structural: it cannot enter the static law).

**Multiplier-vs-physical tests (each reported).**
- **P1 (role of λ).** From the quadratic Lagrangian: the coefficient of δλ δχ̇ (the symplectic term). λ is a Lagrange multiplier iff
  this coefficient is 0; it is χ's conjugate momentum iff ≠ 0 (Dirac: p_χ − (coef)δλ ≈ 0 and p_λ ≈ 0 second class iff coef ≠ 0).
- **P2 (does the growing root reach observables?).** Eigenvector of the fastest growing root, normalised to Kδλ = 1 (potential
  units): report |δ_c| = |ρ̄⁻¹δρ_c|, |Φ|/c², |ξ| and the medium acceleration |σ²ξ| relative to |∂_x(Kδλ)|. PHYSICAL iff
  |δ_c| or |Φ| is nonzero above 1e-10 of its natural scale (|Kδλ|/c² for Φ/c², k|Kδλ|/σ² × k for δ_c) and the medium equation
  contains ∂_x(Kδλ); MULTIPLIER-ONLY iff the growing eigenvector has δ_c = Φ = ξ = 0 to that tolerance.
- **P3 (final-data reading).** If λ is posed with final data instead, report the anticipation time τ_k = 3|H|/(c²k²) (physical k)
  at 10 kpc, 1 Mpc, 100 Mpc, and the ratio τ_k·H.

**Class rule for (a).**
- **CONFIRMED** iff ILL-POSED on FRW for H > 0 AND for H < 0 at both redshifts, the growing root ∝ k² with ratio to c²k²/(3|H|)
  within 1% at the top k, AND P2 reads PHYSICAL, AND K-a1…K-a4 pass.
- **CONFIRMED BUT NOT PHYSICAL** iff ILL-POSED as above but P2 reads MULTIPLIER-ONLY (or the root is a gauge mode).
- **NOT CONFIRMED** iff WELL-POSED on FRW (the error in WT-02 is then located and shown).
- **UNDERDETERMINED** iff the gravity-on and gravity-off runs disagree, or a K test fails, or UNRESOLVED.
Consequence for CFG938/PAPER57: if CONFIRMED (either variant), the statement "linear well-posedness" holds only on static
backgrounds (θ = 0), and correction text is drafted (§6).

## 3. (b) Tensor speed from the ττ term

**Setup.** Locally flat background with a constant gradient of χ, V_μ = ∂_μχ = (V0, 0, 0, u0) (x⁰ = ct, so V0 has acceleration units),
medium at rest (u^μ = δ^μ_0). TT plane wave h_ij(x⁰, x) along n = (sin θ_k, 0, cos θ_k), both polarisations. Compute τ_ij to O(h)
with the Christoffels of η + h, ⟨τ_μντ^μν⟩ averaged over a wavelength, and the EH quadratic action of the same wave from √−g R
averaged the same way (own computation; normalisation checked by □h = 0 at γ = 0). Dispersion → δ(c_T²/c²) = C(θ_k, pol; V0, u0)
L*²/c⁴. Also the exact FRW check: g_ij = a²(t)(δ_ij + h_ij), χ = χ̄(t): τ_ij at O(h) symbolic. Report whether W_full, λ̄ and n
add any O(k²) term (expected: only O(k⁰) mass-like terms ~ u0²/c⁴; their size is printed).

**Numbers.** Local at the W wall (u0 = a0, V0 = 0), both footings, L* = 24 pc and 1 kpc. Cosmic clock: V0 = |∂_0χ̄| = cΩ_cH/2
(S1d), averaged along the GW170817 path (comoving distance to z = 0.0098, D ≈ 40 Mpc) with H(z), Ω_c(z) from §2's inputs; plus
two galaxies (point masses 1e11 and 1e12 M☉, the law's u(r), path from r_min = 2 kpc to infinity on each end) for the spatial
part, including the cross term of V0 with the line-of-sight component. Bound: −3e-15 < c_T/c − 1 < +7e-16.

**Class rule for (b)** (three sub-claims, each CONFIRMED / NOT CONFIRMED with the number):
- (b1) A5 "c_T = c (structural)" is wrong iff C ≠ 0 at O(L*²u²/c⁴) for u0 ≠ 0.
- (b2) size: CONFIRMED iff C = 1.5 (i.e. c_T/c − 1 = 0.75 L*²u0²/c⁴) within 1e-9 for every angle and polarisation when V0 = 0.
- (b3) "GW170817 passes on the path average": evaluated with the full path average (cosmic-clock term included). CONFIRMED iff the
  path average lies inside the bound at both L* ends on both footings; NOT CONFIRMED iff outside at either end. The L*_max implied
  by the full path average is reported, and compared with WT-02's path-model L*_max (16–33 kpc) and wall worst case (0.79–0.95 kpc).

## 4. (c) Cosmic clock

u_v = γ_v v |∂_0χ̄|/c from the O(ε²) term of u² in §2 (sympy). CONFIRMED (number) iff u_v/a0 at 370 km/s = 1.1e-3 within 5% on the
canonical footing (alt reported). Visibility, per record test, with the declared size comparisons:
- SPARC (C2, rms 0.10 dex): NGC 3198 outermost radius, first-order (dipole) and azimuth-averaged (second-order) fractional
  change of the medium field, |u_v/u| and (u_v/u)²;
- wide binaries: u_v vs internal g at 10 kAU (1.5 M☉ pair) and vs the record's DR4 sensitivity scale (few per cent);
- Solar System: the whole tether-sector pull at 1 AU is ≤ GM☉/L*² (CFG770 K1); compared with the α1 signal at the bound
  α1 = 3.4e-5 (acceleration α1 (w v⊕/c²) GM☉/AU², w = 370 km/s, v⊕ = 30 km/s);
- KiDS (h72): crossover r_× = √(GM_b a0)/u_v for the four bins vs their r_end bounds, w = 370, 630, 1000 km/s;
- linear growth: whether the clock already entered a recorded number (CFG941's a^0.694).
Per test: NOT VISIBLE iff the effect is < 0.1 of the test's sensitivity (or r_× > 10 r_end), VISIBLE iff ≥ 1×, else UNDERDETERMINED.
Class for (c): CONFIRMED (the clock exists with that size) plus the per-test visibility labels.

## 5. (W5) WT-05 vs CFG955 / CFG958

For each lane: list WT-05's statements about it; compare with the lane's README/outputs and LEDGER row; label each statement
CONSISTENT / CHANGES CLASS / INCONSISTENT. Light checks only (no re-derivation): sympy Boltzmann entropy production of a position
drift, dS/dt = ∫f ∇·v_s, and its sign for deficit filling; the isothermal-sphere canonical / microcanonical thresholds (32.1 / 709)
by integrating the Emden equation. A class changes only if a statement contradicts an item the lane's frozen class rule uses.

## 6. Correction drafts

If (a) or (b) is CONFIRMED (in any variant), draft "Correction (v1.1)" text for PAPER57 and a note for the canonical draft, as files
in this lane only (CORRECTION_PAPER57_v1.1_DRAFT.md, CORRECTION_CANONICAL_DRAFT.md). PAPER57, THEORY_CANONICAL files, LEDGER.md,
what_is_time/ and other lanes are not edited.

## 7. MUTATE (separate outputs, *_MUTATE.*; each tooth must bite)
- **MU1 flip:** D² → ³Δ + θ u·∂χ (sign of the −3Hχ̇ term flipped). Bites iff the forward/backward labels of χ and λ swap and the
  Hadamard test still fires (the growing field becomes χ for H > 0).
- **MU2 remove:** D² → intrinsic slice Laplacian ³Δ (no θ term). Bites iff the Hadamard test no longer fires (WELL-POSED, all roots
  bounded) AND S1d fails (D²χ̄ = 0 ≠ Kρ̄: the FRW background then needs an explicit ρ̄ subtraction).
- **MU3 no Christoffel in τ:** ∇∇χ → ∂∂χ inside τ. Bites iff δ(c_T²) = 0 for every V.
- **MU4 no clock:** V0 = 0 on FRW. Bites iff the FRW tensor correction is 0 and (b3)'s path average drops to the galaxy-only value.
- **MU5 multiplier-only control:** gravity off and the medium coupling of λ removed (Kmn → Kρ̄(t), fixed). Bites iff P2 then reads
  MULTIPLIER-ONLY and (a) would read CONFIRMED BUT NOT PHYSICAL.

## 8. Hand expectations stated before any script (disclosed; not blind)

From reading CFG938 and WT-02 and a pen-and-paper pass before freezing:
- (a): the λ term contains −θλ u·∂χ, so p_χ ∝ θλ; I expect roots ±c²k²/(3H) and λ's growing mode to drive the medium through
  −ρ_c K∇λ, i.e. CONFIRMED (physical). I also expect the H → 0 limit to be singular (rates diverge as 1/H).
- (b): I expect C = 1.5 for a spatial gradient, and that the same ττ term, through Γ⁰_ij ∂_0χ̄ (the slices' extrinsic curvature
  times the clock rate), gives the same coefficient for the timelike FRW gradient |∂_0χ̄| = cΩ_cH/2 ≈ 0.8–0.9 a0. WT-02's path model
  ("the tether sector vanishes on FRW") would then omit the dominant term, and the full path average would sit near the 7e-16 line
  at L* = 1 kpc. If so, (b3)'s pass holds or fails by a small margin at the top of the L* window, and the margin is ~1 kpc, not 16–33.
- (c): u_v = 2.9e-19 s⁻¹ × v; not visible in SPARC, wide binaries or the Solar System; KiDS inside the undecidable band.
These expectations do not change the rules above.

## 9. Compute and hygiene
One process, `OMP_NUM_THREADS=1 nice -n 10`, in-script RSS guard at 1 GB. No downloads. No other lane's files edited, staged or run.
No personal names or home paths. Commits with explicit paths; no push.
