# X17_beta_sound_selector: is C1's sound speed a selector with the right sign? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before any lane script exists and before any number is computed by
code. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`. κ = ½ is FITTED. Footings canonical
a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. No new fitted knob: β is used
only inside X14/X15's window (set by caustics and H₀, not by data). Never "theory closed"; nothing here says the data favour
the framework. Small jobs only: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes; `compute_queue/` and
every other lane untouched (record scripts are run only as patched copies in a temporary directory, outputs there); no
downloads.

**The question.** C1 (the khronon K² term, Hořava λ = 1 + β, window β ∈ [2.0e-6 / 2.2e-6, 1.0e-5] at μ_K = 0.1 Mpc⁻¹,
≤ 1.12e-4 at μ_K = 0.03; X14, X15) gives the khronon a propagating mode with sound speed c_A. Is c_A a selector with the
right sign: one that leaves isolated galaxies at the law but moves cluster cores toward the measured excess
(A_MID ≈ 1.5–1.7 × the law in 0.3–1 Mpc; corrected Z 4.1–5.0, X11/X13; light tercile no excess, heavy two-thirds excess,
X2/X7), without making growth worse?

## 0. What was read, and the not-blind statement

Read before freezing: `covariant_push_2026_10_22/V3_FULL_PICTURE.md` (all); `rebuild_2026_10_22/X0_explanation_map/MAP.md`
(all); X14 README and the C1 / `disp` parts of `x14_caustic_completion.py`; X15 README, FROZEN_CRITERIA, ASSUMPTION_LEDGER
and `x15_c1_preferred_frame.py` (all); X4 README and `x4_growth.py` lines 1–200 (F3's ODE copy); X7 README and the tercile
blocks of `x7_analysis_results.json`; the tercile keys of X2's JSON; X13's `Z_MID_corr`; F1's `dust` block and `predict()`
signature; `STANDING.md` lines 293–299; `qwen_claude_field_theory/closure_2026/condensate_pincer_2026/
CONDENSATE_MU_PINCER_VERDICT.md` and `condensate_mu_pincer_2026.out` (all); `rebuild_2026_10_22/Z1_successor_design/
FAMILY_SCORES.md` §2 item 6; M2 README head; the rebuild BRIEF.

**Not blind.** Before freezing I reasoned on paper (no script, no code-computed number). These expectations shaped what
§4–§7 compute; thresholds below are structural (fractions of the measured excess, the record's own [0.5, 2] power margin,
5 % "unchanged" bands), not tuned to them.
- **Statics.** C1 is quadratic in the leaf trace K. A static configuration whose khronon is at rest in the static frame
  has K ≡ 0, so every C1 contribution to every field equation (∝ K, K², ∇K) vanishes, at all orders. X14 already graded
  C1's P1 ("EL term −(B/K)σ_zzzz = 0 on the static branch"). Expectation: C1 cannot change any static lensing mass, so the
  expected verdict is **INERT**.
- **The pincer's scope.** c_A² = Bc²(M_θ − 1), M_θ ∈ [1 + x, (1 + x)²], x = |∇Ξ|/a₀: it is keyed to the law field's
  gradient (an acceleration), not to the dust's local density/excitation, and it is 0 on FRW (x = 0) at any density. The
  pincer's K-independent step (a galaxy well's state recurs on the background at z_match with the same c_s) needs a
  density-keyed c_s. Expectation: outside the pincer's scope.
- **Internal Mach is mass-independent (paper identity).** For the spherical law, v_c² = g r and c_A,⊥² = Bc² g/a₀, so
  v_c²/c_A,⊥² = a₀r/(Bc²) ≡ r/r_β with r_β = Bc²/a₀. Paper values: r_β ≈ 31 / 28 kpc (β_min), ≈ 156 / 129 kpc
  (β_max(0.1)), ≈ 1.7 / 1.4 Mpc (β_max(0.03)). So internal motions are subsonic inside r_β whatever the mass; bulk motion at
  fixed w is more subsonic in higher-x systems (c_A ∝ √x), i.e. heavier clusters.
- **Growth.** On FRW at linear order x = 0, so c_A = 0: C1 cannot Jeans-suppress the khronon there. In the PN continuity
  equation C1 adds a charge current (B/K)∇⁴σ, so the khronon's transport factor becomes ρ̄_τ + Bk_p²/K. On paper the
  sub-horizon khronon equation becomes δ_τ'' + (2 + dlnE − F′/F)δ_τ' = F·(3/2)a⁻³E⁻²(Ω_bδ_b + Ω_τ s δ_τ), with
  F = 1 + Bk_p²/(Kρ̄_τ) = 1 + f₁a; paper value f₁ ≈ 4.5 at k = 0.2 h/Mpc for β_max(0.1). Expectation: growth enhanced, not
  suppressed, possibly overshooting at high k (a k²-growing F). This lane computes it; the expectation is not used.

## 1. The μ-pincer theorem, stated, and the scope test

**Source.** `STANDING.md` §"What the September closure established" item 3 (line 296); `condensate_pincer_2026/
CONDENSATE_MU_PINCER_VERDICT.md` (sha256 def2c4f6…a7bc) Part F and Part G; `condensate_mu_pincer_2026.py` (sha256
0e7d1a9a…b765), checks D1, D2, F1, G1, G2 (18/18 in its `.out`). Cited by Z1 FAMILY_SCORES §2 item 6 as "the μ-pincer
(pressure cannot keep the cold mass out of galaxies)".

**Statement (as the record proves it).**
1. *Relation.* For any shift-symmetric condensate at a quadratic minimum, the static-limit dust is a γ = 2 polytrope,
   p = (2πG/μ²)ρ², c_s² = 4πGρ/μ², with the same μ as its static Helmholtz equation; on the cosmic background
   c_s²(z) = 4πGρ_dm(z)/(μ²c²) ∝ (1+z)³ (A1, A2).
2. *Horn 1 (the dust is the khronon's charge).* At β = 1 the DBI amplitude is pinned, R = ν₀Ω_Λ/Ω_dm = 2.6ν₀, 18–300×
   above the record's 3 %-P(k = 0.2) ceiling: excluded (B1, C3).
3. *Horn 2 (a separate quadratic condensate χ).* CMB-cold needs μ_χ⁻¹ ≤ 0.6 kpc; shielding an L★ galaxy (polytrope dust
   inside 30 kpc ≤ 30 % of the baryons) needs μ_χ⁻¹ ≥ 200 kpc; gap ≥ 300× (D1, D2). A walled χ passes at most one of the
   P(k = 0.2) and forest yardsticks (D3).
4. *K-independent form (Part F).* c_s² = K′/(QK″) is a function of the local excitation u alone. A static well imposes
   u_well = −Q₀Ψ for any K; the background carries n(z) = K′(u(z)) = n₀(1+z)³, so it passes through the well's state at
   (1 + z_match)³ = δ_well **with the identical sound speed**. Shield-compatible wells have δ_well ≤ 5000, z_match ≤ 16; for
   K ∝ u², u³, u⁴, u⁸ the dust's c_s at z = 3 is ≥ 20 km/s (F1), above the forest's tolerance; the non-analytic |u|^{3/2}
   minimum is cold at z = 3 but was ≥ 75–283 km/s on the whole background at z ≥ z_match (G1, G2).
5. *Conclusion.* "Pressure cannot keep Ω_dm out of galaxies."

**What it rules out.** Any selector that keeps the cold mass out of galaxies by the dust's own pressure, where the sound
speed is a function of the dust's local state (density or excitation u), so that a galaxy well's state is re-visited by the
homogeneous background at some z_match. This covers barotropic / k-essence pressures, the AeST/BS polytrope, v9 DBI, a
separate quadratic or walled condensate, and superfluid minima.

**What it does not cover (its premise).** A stiffness keyed to a quantity that differs between a galaxy well and the
homogeneous background at the same density (for example the law field's gradient), and any effect that is not a static
pressure.

**Scope test (check P0, required).** With c_A² = Bc²(M_θ − 1) and the record's M_θ bracket (transverse 1 + x,
longitudinal (1 + x)²): (a) on the homogeneous background (x = 0) c_A² ≡ 0 for every background density ρ̄ (symbolic,
residual 0), while (b) in a static galaxy well at the same density c_A² > 0 for every x > 0. If (a) and (b) hold, the
background never re-visits a well's c_A, the premise of item 4 fails, and C1's c_A is **outside the pincer's scope**. If
(a) fails (c_A² on FRW depends on ρ̄ and equals the well's value at δ_well), it is **inside**, and §8's EXCLUDED BY THE
PINCER applies. The P0 result (and step 2's static result: whether C1 is a static pressure at all) is reported verbatim.

## 2. Definitions

- **v3s** (V3_FULL_PICTURE §1): BS khronon, J_x (simple μ), K(Q) = μ_K²(Q − 1)², covector P, switched stiffness
  −(γ_L/2)[max(D·P, 0)]², γ_L = K L★²/2, K ≡ 4πG. **C1**: −βK²/(4K) inside the gravity bracket (Hořava λ = 1 + β); PN
  coefficient **B = βc²/(2 + 3β)** (X15 S0-3: exact khronometric speed). PN Lagrangian: X15's `L3` (3D, with μ_K, P, W,
  stiffness and C1 term −(B/2K)(∇²σ)²).
- **Window** (X14/X15): β_min = 1.99355e-6 (canonical) / 2.19755e-6 (alt); β_max = 2H₀²/(c²μ_K² − 3H₀²) at H₀ = 67.2,
  i.e. 1.00493e-5 (μ_K = 0.1 Mpc⁻¹) and 1.11675e-4 (μ_K = 0.03). Graded β set: {β_min(foot), β_max(0.1), β_max(0.03)}
  (β_max(0.03) only with μ_K = 0.03).
- **Sound speeds.** x = g/a₀ from the spherical law (X14/X15 `aqual_point`, copied). c_A,⊥ = √(Bx) (M_θ − 1 = x; the
  X14/X15 convention, conservative), c_A,∥ = √(B(2x + x²)) (M_θ − 1 = 2x + x²). Reported also: the full linear stiffness at
  k = 1/r, c_eff² = (Kρ_ph r² + B)(M_θ − 1) (X14's dispersion with the local phantom charge; the Kρ_ph term is the
  charge's own transport, present at β = 0). v_c = √(g r). r_β = B/a₀ (transverse internal-Mach radius).
- **Environments** (inputs; classes in the ledger):
  - E1 cosmic background, z = 0 and z = 1100 (FRW: x = 0).
  - E2 isolated-galaxy outskirts: baryonic point masses M_b ∈ {1e9, 1e10, 6e10, 2e11} M☉ (SPARC-like span,
    ILLUSTRATIVE), r ∈ {10, 30, 100} kpc.
  - E3 group/cluster cores: X7's terciles T1/T2/T3 with X2's median MGAS500 {3.305e12, 1.1668e13, 2.9232e13} M☉;
    enclosed baryons M_b(<r) = (1 + f★)(MGAS500_T / MGAS500_med) M_gas,med(<r) with F1's sample medians
    M_gas,med(<0.5 Mpc) = 6.856e12, (<1.0 Mpc) = 1.695e13 M☉ (F1 JSON `dust.canonical`), (<0.3 Mpc) by the log-log slope
    between them; f★ = 0.20 (F1 default); r ∈ {0.3, 0.5, 1.0} Mpc; mass bracket × {0.5, 1, 2} (reported; ×1 graded);
    point-mass law at M_b(<r).
- **Speeds compared** (ILLUSTRATIVE, X15's list): bulk w ∈ {369, 600, 1000} km/s for clusters (369 also for galaxies and
  the background); member galaxies: Maxwellian 3D speeds with σ_1D = v_c/√2 (isothermal); internal: v_c. E1 background:
  the baryon sound speed at z = 1100 (T = 2.7255 K × 1101, μ = 1.22) and 369 km/s at z = 0.
- **Background for E1/growth:** F3's background A (X4's): h_A, Ω_m, Ω_b from `f3_growth_audit_results.json` K2, radiation
  4.18e-5/h², as F3's `make_E`.

## 3. Step 0: reproductions (stop rule: any failure → verdict UNDECIDED, nothing further scored)

- **S0-1 (X15's own code).** `x15_c1_preferred_frame.py` (sha256 2bf28103…f9e1) is copied to a temporary directory with only
  `HERE` (→ that directory) and `ROOT` (→ the repository) rebound, and run with PYTHONHASHSEED=0. It must exit 0 with 13/13
  PASS and its JSON must equal the committed `x15_c1_preferred_frame_results.json` (sha256 dd864fc9…8e5e) in every leaf
  except `runtime_s`, `peak_rss_gb` (numbers to relative 1e-12, strings equal). This reproduces X15's c_A values (T3a, T3c)
  and the khronon dispersion (S0-3 roots) from X15's code.
- **S0-2 (c_A and window from formulas).** This lane's β_min, β_max (X14/X15 formulas, copied) equal X15's `S0_2` to
  relative 1e-12, and c_A,⊥ = √(xβc²/(2+3β)) on X15's fold-radius x (`S0_2.x_fold`) and its cluster point (1e14 M☉ at
  300 kpc) equals X15's `T3a_mach` c_A (both footings, three β) and `T3c_cherenkov` `c_A_cluster_km_s` to relative 1e-12.
- **S0-3 (dispersion, this lane's system).** X14's `disp` (copied with provenance) with the C1 transport term gives
  ω² = (ρ_τ + Bk²/K)(k²/χ − K) (X14 C1-R record form, residual 0, Θ = 0 and Θ = 1), and at ρ_τ = 0, μ_K = 0 it equals
  X15's S0-3 root βk²(M − 1 + ΘL★²k²/2)/(2 + 3β) after B = β/(2+3β), γ_L = KL★²/2 (residual 0).
- **S0-4 (record cluster numbers, read only).** From `x7_analysis_results.json` (sha256 c8f33d85…7f84) the tercile A_MID
  (CAL) for the four cells equal X7's README table to its printed two decimals (T1 1.10 / 1.11 / 1.00 / 1.02; T2 1.85 /
  1.92 / 1.70 / 1.76; T3 1.84 / 1.88 / 1.69 / 1.73) and T1 < min(T2, T3) in every cell; X2's
  `tercile_median_Mgas500` (sha256 81a80fc0…df9e) rounds to X7's "3.3e12 / 1.17e13 / 2.92e13" and its T2 equals X7's
  `mass.M_med`; X13's `Z_MID_corr` A (sha256 cdbd737e…137a) rounds to 1.657 / 1.703 / 1.520 / 1.562 and Z to 4.77 / 4.99 /
  4.11 / 4.35; F1's `dust.canonical.median_Mgas_0p5/1p0` (sha256 76cbfeee…8925) are read. No shear is recomputed.
- **S0-5 (X4's growth ODE).** F3's ODE as copied in `x4_growth.py` (sha256 fe0ba2b7…0b11) lines 88–150 equivalent, on
  background A via classy, reproduces X4's `ode.<0.03|0.1>.<bsk2_ai0.001|bsk2_ai0.0001>.sigma8_ratio` (sha256
  1e3cad65…5499) to relative ≤ 1e-4.

## 4. Step 1: c_A by environment (computed; reported; feeds steps 2 and 4)

For every environment of §2, both footings, β ∈ {β_min, β_max(0.1), β_max(0.03)} (μ_K labels as in §2): x, v_c, c_A,⊥,
c_A,∥, c_eff(k = 1/r), r_β, and the Mach numbers v_c/c_A, w/c_A. E1: c_A on FRW (from P0), the stiffness-only speed on FRW
√(Bγ_L/K)·k at k = 1 Mpc⁻¹ physical, and C1's IR tachyon rate √B μ_K (X14 P6c) against H(z). Check **C-ID (required)**: the
identity v_c²/c_A,⊥² = a₀r/B holds for the spherical law at every E2/E3 point (relative 1e-12) and symbolically
(residual 0).

## 5. Step 2: the static question (derived from the action; required checks)

- **H-COV (covariant).** (a) For a static diagonal metric with τ = t (general functions of the spatial coordinates), the
  khronon leaf trace K = ∇_μn^μ computed from τ is 0 (residual 0). (b) In the ADM spherical ansatz N(t, r), shift
  N^r = S(t, r), h = diag(A², Bf², Bf² sin²θ), with K = (1/N)(∂_t ln√h − D_iN^i), the Euler–Lagrange expressions of
  √h N K² with respect to N, S, A and Bf all vanish on S = 0, ∂_t(N, A, Bf) = 0 (residual 0). In unitary gauge the khronon
  equation follows from these by diffeomorphism invariance (METHOD). Consequence if it passes: C1 contributes nothing to
  any field equation of a static held configuration, at all orders.
- **H-PN (PN level).** With X15's `L3` (copied): the Euler–Lagrange expressions for φ and P_i do not contain B; that for σ
  contains B only through (B/K)∇⁴σ; on σ = −Ct (static held) and on σ = −Ct − w·x (a Galilean-boosted held configuration)
  the B-terms vanish (residual 0).
- **H-RESP (linear moving-source response on a uniform held background, WKB; reported form, required derivation).** X14's
  `disp` system with a baryon source δρ_b moving at w (ω = k·w) and μ_K = 0, Θ = 0: δρ_τ/δρ_b derived symbolically and equal
  to 1/[(M_θ − 1) − (k·w)²/(Kρ̄ + Bk²)] (residual 0). Its w → 0 limit is the static sub-phantom 1/(M_θ − 1). The
  direction average over k̂ is artanh(Ma)/Ma (Ma < 1) and the principal value (1/2Ma) ln((Ma + 1)/(Ma − 1)) (Ma > 1), with
  Ma = w/c_eff(k) (symbolic check of the average, residual 0).
- **Grading quantities (per footing, β, tercile; ×1 mass; ILLUSTRATIVE speeds):**
  - **ΔA_static** = 0 if H-COV and H-PN pass (exact); otherwise computed (not expected).
  - **ΔA_bulk** (the whole cluster moving at w through the cosmic khronon): X15's step-3b estimate, copied with
    provenance (`p1_of`; δ ln g ≈ (dg/dg_N − 1)(p₁ − 1)(p₁² + 2)/3 (w/v_c)² (r/R_h)^{2(p₁ − 1)}, R = B/(Kρ_ph r²)), for
    w ∈ {369, 600, 1000} km/s, R_h ∈ {1, 10} Mpc, r ∈ {0.3, 0.5, 1.0} Mpc; only where w < c_A,⊥ at that r (subsonic);
    supersonic cells are NOT ESTIMABLE and listed. ΔA_bulk ≡ δ ln g (lensing sees ψ = φ).
  - **ΔA_mem** (member galaxies moving through the cluster's held khronon): f_mem × (1/m) × (⟨𝒫⟩ − 1) × g_N/g, where
    f_mem = f★/(1 + f★) (all stars counted as moving members, an upper-side choice), m = x (transverse sub-phantom, the
    larger response), ⟨𝒫⟩ = the H-RESP direction average further averaged over the member Maxwellian, with c = c_A,⊥.
    Bracket reported: f★ ∈ {0.10, 0.30}, m ∈ {x, 2x + x²}, c ∈ {c_A,⊥, c_A,∥}.
  - **Drag (reported):** X15's Cherenkov form, copied: a_drag = 4πG·GM·ρ_ph lnΛ/w², lnΛ = ln 100, t_drag = w/a_drag, in
    units of 1/H₀ (H₀ = 67.2), for a 6e10 M☉ member at w = v_c in each tercile's phantom at 0.5 Mpc, only where w > c_A.
- **Per tercile T:** ΔA⁺_T = max over graded cells of [ΔA_static + max(ΔA_bulk, 0) + max(ΔA_mem, 0)], ΔA⁻_T = min over
  graded cells of [ΔA_static + min(ΔA_bulk, 0) + min(ΔA_mem, 0)] (max/min over r, w, R_h; at a given footing and β).

## 6. Step 3: linear growth with C1 (X4 comparison)

- **The system.** F3/X4's two-fluid sub-horizon ODE (J_x kernel s = 1/(1 + (k/aμ)²), baryons Newtonian at every k, both
  fluids started as growing dust at a_i, background A) with C1: the khronon equation becomes
  δ_τ'' + (2 + dlnE/dlna − dlnF/dlna)δ_τ' = F·(3/2)a⁻³E⁻²(Ω_bδ_b + Ω_τ s δ_τ), F = 1 + f₁a,
  f₁ = [β/(2 + 3β)](c k/100 km s⁻¹)²/(1.5Ω_τ) (k in h/Mpc); baryons unchanged. Derivation: X15's continuity with the C1
  current (S3-1) in its FRW sub-horizon form, δ̇ = −Fθ, θ̇ + 2Hθ = −K(ρ̄_bδ_b + ρ̄_τsδ_τ) (METHOD: physical k/a, ρ̄ ∝ a⁻³;
  O(β) background and O(aH/k)² terms dropped).
- **Required checks.** **G-LIM**: at β = 0 the C1 ODE equals the copied X4 ODE (relative ≤ 1e-10 at every k). **G-CA0**:
  on FRW (M_θ = 1, μ_K = 0, Θ = 0) the khronon dispersion with C1 has no positive k² term, i.e. c_A = 0 there (residual 0).
  **G-DISP**: X14's `disp` extended with a baryon fluid (Poisson for all mass) gives, at x = 0 and finite μ_K, the
  two-root polynomial λ² − Tλ + D = 0 in λ = −ω² with T = Kρ̄_b + (Kρ̄_τ + Bk²)s, D = −Kρ̄_b(Kρ̄_τ + Bk²)(1 − s)
  (residual 0), and the ODE's frozen-time source matrix has the same eigenvalues at three test points (relative 1e-10).
- **Numbers.** R(β) = σ₈ ratio (X4's convention, a_i = 1e-3 primary, 1e-4 reported) for β ∈ {β_min(foot), β_max(μ_K)} at
  μ_K = 0.1 and 0.03, both footings (a₀ does not enter linear FRW; β_min differs by footing). T²(k, z) = (δ_m/δ_m,dust)² at
  k ∈ {0.1, 0.3, 1, 3, 10} h/Mpc, z ∈ {0, 3}. Reported: the coupled growth rate √λ₊/H at z = 1100 and 0, k = 1 and 10 h/Mpc.
- **Growth class per cell:** **WORSE (overshoot)** if T² > 2 at any of those k and z (outside the record's [0.5, 2] power
  margin, X4 F); else **WORSE (suppressed)** if R(β)/R(0) ≤ 0.95; else **BETTER** if R(β)/R(0) ≥ 1.05; else **UNCHANGED**.
  R(0) is X4's ODE value at the same μ_K and a_i. The Boltzmann R_B is **not** recomputed (C1 is not in Q6's CLASS patch);
  no R_B number is attributed to C1.

## 7. Step 4 (reported only)

The mass ordering of ΔA± across T1/T2/T3 against the record's split (T1 no excess; T2, T3 excess); the ordering of bulk
subsonicity with mass (c_A ∝ √x); whether S4's static onset ordering r_C ∝ (r_M/μ_K²)^{1/3} ∝ M^{1/6} changes (S4's
static branch is a static configuration, so H-COV decides it).

## 8. Verdict (per footing; footings never pooled; precedence top to bottom)

E_T = min over the footing's two h-cells of (A_MID,CAL,T − 1) from X7 (T2, T3). Isolated-galaxy change: 0 for static
galaxies if H-COV/H-PN pass; for moving galaxies X15's `T3b_rotation` subsonic maximum at that β (record, read).
1. **UNDECIDED** if any S0 check fails (stop rule), any required check (P0, C-ID, H-COV, H-PN, H-RESP, G-LIM, G-CA0, G-DISP)
   fails, or the two footings reach different classes below.
2. **EXCLUDED BY THE PINCER** if P0 places c_A inside the pincer's scope.
3. **RIGHT-SIGN SELECTOR** if, at some β in the window, ΔA⁺_T2 ≥ 0.25 E_T2 and ΔA⁺_T3 ≥ 0.25 E_T3, ΔA⁺_T1 ≤ ½ min(ΔA⁺_T2,
   ΔA⁺_T3), the isolated-galaxy change ≤ 0.05 dex, and growth at that β (its μ_K) is not WORSE; the amount is stated.
4. **SELECTOR BUT GROWTH WORSE**: as 3 but growth WORSE at that β.
5. **WRONG SIGN** if not 3/4 and (ΔA⁻_T ≤ −0.10 for T2 or T3 at some β, or ΔA⁺_T1 ≥ 0.10 with ΔA⁺_T1 > max(ΔA⁺_T2,
   ΔA⁺_T3)).
6. **INERT** if ΔA_static = 0 (H-COV, H-PN) and |ΔA±_T| < 0.10 for every tercile at every graded β.
7. **UNDECIDED** otherwise (for example a right-sign increment 0.10 ≤ ΔA⁺ < 0.25E with the right ordering).
If at every graded β a heavy tercile's bulk channel is supersonic in every cell, the verdict line carries "(bulk channel not
estimable where supersonic)" and cannot be 3 or 4. The growth class is reported alongside the verdict in every case.

## 9. Checks, MUTATE, outputs

- Required checks: S0-1 … S0-5, P0, C-ID, H-COV, H-PN, H-RESP, G-LIM, G-CA0, G-DISP. Exit 0 iff all pass.
- **MUTATE** (`X17_MUTATE=1`, all at once); each named check must FAIL:
  - m1: the C1 operator K² replaced by the khronon acceleration squared a_ia^i (a BPS-α-type term that does not vanish on
    static configurations) in H-COV(b) → **H-COV** fails;
  - m2: H₀ doubled in the copied β_max → **S0-2** fails;
  - m3: X15's copy run with its own `X15_MUTATE=1` → **S0-1** fails;
  - m4: X7's terciles read in reversed order → **S0-4** fails;
  - m5: F3's kernel replaced by s = 1 (X4's own MUTATE) in the S0-5 copy → **S0-5** fails;
  - m6: the C1 transport factor F replaced by 1/F in the growth ODE → **G-DISP** fails;
  - m7: P0 fed the density-keyed polytrope c_s² = Kρ̄/μ² in place of c_A² → **P0** fails.
- Outputs: `x17_beta_sound_selector.py`, `.out`, `_results.json` and `_MUTATE` twins; README with the verdict, the pincer
  statement and scope, the c_A table, the static derivation, the growth comparison, checks, every amendment labelled
  PRE-RESULT or POST-RESULT, and "what this does not show". Every README number comes from the committed `.out`/`.json`.
- Git: pathspec commits of this lane directory only; never push; no rebase or amend.
