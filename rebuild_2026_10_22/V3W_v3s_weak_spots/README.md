# V3W_v3s_weak_spots: v3s passes its PPN γ/β derivation (W1), its galaxy lensing-to-dynamics ratio (W3) and its GW speed, and keeps healthy galaxy backgrounds (W4a/b). It is UNDECIDED on C6's in-window rerun (W2: the finest-rung change is 2.3e-2, against a 2e-2 line) and on health on the Solar-System background (W4c: never run). Both footings

**Owner 11-04:** "Test weak spots first", in reply to whether to adopt v3s as the galaxy law's action. This lane **adopts
nothing**. The 10-24 v3s verdict stands unless the owner changes it in writing: v3s passes as a galaxy-scale law and fails
as gravity plus cosmology. **Not blind**: AX1, C6, C6P, C5, C8, X3, X15, X53, GH1 and X75 were read first. κ = ½ FITTED.
Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not theory closed. Nothing here says the data favour
the framework. The cold sector stays retired. CMB and clusters are out of scope and stay open. a0 is put in by hand.
No file under `covariant_push_2026_10_22/` was edited; C6's code is imported read-only, with no bytecode written.

- Criteria: `FROZEN_CRITERIA.md`, committed alone first (37c16dcbaa).
- Scripts: `w1_ppn.py`, `w2_c6_rerun.py`, `w3_lensing.py`, `w4_health_gw.py`. Outputs `*.{json,out}`, byte-identical
  reruns `*_RERUN.*`, MUTATE twins `*_MUTATE.*`.
- Compute: one thread, no downloads, no web look-ups. W1 15 s, W3 8 s, W4 about 3 min (mpmath), W2 about 3.5 min. RSS is
  under 1 GB except one W2 rung, which is disclosed below.

## Table

| | canonical | alt |
|---|---|---|
| **W1** PPN γ, β from the action | **PASS.** γ − 1 = 0 at O(GM); remainder ≤ 9.8e-14 out to 10 AU (Cassini 2σ band [−2.5e-5, 6.7e-5]). β = 1; remainder ≤ 1.1e-12 at Mercury (LLR line 1e-4) | **PASS.** Remainder ≤ 1.3e-13; β = 1, remainder ≤ 1.1e-12 |
| **W2** C6's carried checks | **UNDECIDED.** C1 and C3–C8 reproduced exactly. C6′ (in window, L★ = 24 pc, Λ = 622): converged, second-order ladder, N/F = 0.9987, **but Richardson − finest = −2.3e-2 against the 2e-2 line** | **UNDECIDED.** Same at Λ = 684: −2.3e-2, N/F = 0.9987. The (40, 64) rung peaked at 1.00–1.01e9 bytes RSS |
| **W3** lensing / dynamics | **PASS.** v3s predicts M_lens/M_dyn = 1 to ≤ 6.5e-5 (at 310 kpc). KiDS isolated: A = 1.129 ± 0.206 (+0.6σ). GH1 matched hosts: A = 0.974 ± 0.248 | **PASS.** A = 1.035 ± 0.187 (+0.2σ); GH1: 0.890 ± 0.227 (−0.1σ, photo-z allowance) |
| **W4a** c_T | **PASS.** c_T = c exactly in the principal part; \|Δv/c\| ≤ 5.1e-32 at 100 Hz (GW170817 [−3e-15, 7e-16]) | **PASS.** ≤ 6.2e-32 |
| **W4b** health, galaxy backgrounds | **PASS** (linear WKB scope): no ghost, no gradient instability; growth on the soft side is bounded | **PASS**, same |
| **W4c** health, Solar-System background | **UNDECIDED.** v3s's β = η = 0 form was never run on this background | **UNDECIDED**, same |

## W1. PPN γ and β, derived

- **Method.** The static spherical isotropic metric ds² = −e^{2Φ}dt² + e^{−2Ψ}(dr² + r²dΩ²) with P = P_r dr. The full
  action (GR + Λ + K(Q) + P·A − W − (γ_L/2)(D·P)²) is reduced exactly to 1D, and sympy derives the three exact
  Euler–Lagrange equations.
- **First order.** The Ψ equation is (r²(Φ₁ − Ψ₁)′)′ = 0, with no source: the P sector couples to Ψ only through
  √h, h^ij and D_i, which is cubic in the fields. So Ψ₁ = Φ₁ and **γ = 1 exactly at O(GM)**, with the hedgehog in place:
  Φ₁ = Ψ₁ = −m/r + (m/L★²)r and p = m/L★² (K3, residual 0).
- **Second order** (K5, residuals 0). The Ψ equation gives Ψ₂ − Φ₂ = m²/4r² (GR) − 2m² ln r/L★². φ₂'s m²/r² coefficient
  is forced to 0, so **β = 1**. Every other term carries L★ or a0:
  - 9m² ln r/L★²;
  - m²r² ln r/L★⁴;
  - m²r³/(6L★⁶a0), from W's cubic term.
- **Remainders, graded** (24 pc; 21.7–90 pc in the json):
  - **Galactic-background cross terms.** From the exact 3D Ψ source of the P sector (K6), e^Φ[−P·∇Φ + 3W − uW′ −
    (γ_L/2)(∇·P)²] − ∇·(γ_L e^Φ(∇·P)P), with the cap |p_e| < a0. The worst-case same-sign Green's bound is
    |γ − 1| ≤ 2(a0r/c²)(1 + 1/x_e)(1 + ln(1 kpc/r)) = 9.8e-14 (canonical) and 1.3e-13 (alt) at 10 AU.
  - **The isolated non-PPN terms.** 1.1e-19 for γ at 10 AU, and 9e-13 for β at Mercury.
  - Λ adds 2.4e-28.
- **Known answer (K1).** With the law off, isotropic Schwarzschild solves the derived equations exactly: γ = β = 1.
  K2: the 1D reduction of √−g R gives the same Euler–Lagrange equations (residual 0). K4: |p|/a0 ≤ 3.2e-6, so the
  expansion is valid.
- **What is a bound, not a solve.** The background cross-term number is an analytic bound (cap plus Green's function),
  not a 3D solution. It sits 8 orders below the Cassini line. The planets' anomaly GM/L★² is G2b's (C6P), not repeated here.

## W2. C6's carried checks

| C6 check | rerun result | status |
|---|---|---|
| C1 sympy equations, kernel | residuals 0 | reproduced |
| C3 build = D7d build | max \|ΔA\| = 0; r_F = 0 differs by 1.305692e5, as C6 | reproduced |
| C4 AQUAL anchor | BN11 ratio 1.0077; E2 max 7.8e-3 | reproduced (Δ = 0) |
| C5 Route N vs F, Λ = 30, 100 | max \|N/F − 1\| 1.73e-3 | reproduced (Δ = 0) |
| C6 as recorded, Λ = 0.01 | ratio −1.13e-4, residual 2.26, **still not converged** | reproduced (weak, not graded) |
| C7 quadrature, tail | 3.76e-10; 1.82e-5 | reproduced (Δ = 0) |
| C8 linear validity | 1.2887e-5 | reproduced |
| **C6′** in window, ladder (20,32)/(30,48)/(40,64), Q2 at 100 r_Sat | see below | **FAIL (numerics)** |

C6′ results, Q2 Richardson value / Route F:

| footing | Λ = 100 | L★ = 24 pc (Λ 622 / 684) |
|---|---|---|
| canonical | 0.99674, Richardson − finest −1.7e-2: **ok** | 0.99871, Richardson − finest **−2.3e-2: FAIL** |
| alt | 0.99594, −1.8e-2: ok | 0.99865, **−2.3e-2: FAIL**; RSS 1.0008–1.01e9 bytes |

- **Every rung converged** (residual ≤ 5.9e-10).
- **The steps shrink at the second-order rate.** d23/d12 = 0.342 and 0.349, against 0.35 expected for h² at these
  ratios.
- **The extrapolated value matches Route F to 1.3e-3.** So the physics reading supports C6's Route F Q2 inside the window.
- **But the frozen line is not met.** The finest rung (40, 64) is still 2.3 % from the extrapolation, against 2e-2. A
  finer rung would exceed the 1 GB budget: (40, 64) already peaks at 0.95–1.01e9 bytes.
- **So W2 is UNDECIDED on numerics, not physics.** C6P's 24-cell Q2 (max 1.86e-34 / 1.58e-34 s⁻², Hees line 9.0e-27) is
  unaffected.
- **Extraction radius.** At r_Saturn the in-window l = 2 part is ~1e-18 of the monopole. Even so, N/F there is 0.987 /
  1.036, while at 10 and 100 r_Sat it is 0.998–0.999.

## W3. Galaxy lensing = dynamics

- **What AX1's G3 PASS rested on.** It was a read of the record, not a computation against data: φ = ψ (BS24 Eq. 24;
  C4 K1 under the a0 = O(ε) scaling) plus S4's μ_K < 0.1 Mpc⁻¹ bound.
- **W1 now derives it for the full screened action.** At O(GM) the Ψ equation has no source, so lensing and dynamics see
  one potential. The background bound gives |M_lens/M_dyn − 1| ≤ 1.1e-5 / 2.8e-5 / 6.5e-5 / 1.9e-4 at 30 / 100 / 310 /
  2600 kpc (canonical; alt ×1.2).

The measured ratio A = ΔΣ_obs/ΔΣ_law (GLS, full covariance). σ_stat is scaled by √(χ²/dof).

| | canonical | alt |
|---|---|---|
| D1 KiDS-1000 isolated, R ≤ 0.31 Mpc | A = 1.129 ± 0.049 (stat) ± 0.200 (sys) = ± 0.206; **+0.6σ** | 1.035 ± 0.045 ± 0.182 = ± 0.187; **+0.2σ** |
| D1 χ²_min / dof (p) | 59.0 / 31 (1.8e-3) | 57.8 / 31 (2.4e-3) |
| D1 all radii (reported) | 1.180 ± 0.040 | 1.078 ± 0.036 |
| D2 GH1 matched hosts, 50–300 kpc | A = 0.974 ± 0.248; −0.1σ (0 with photo-z) | 0.890 ± 0.227; −0.5σ (−0.1σ with photo-z) |
| satellites (X75, not graded) | (σ/σ_law)² = 1.36 ± 0.10 | 1.24 ± 0.09 |

**Reading the table:**
- **The systematic dominates D1.** M★ ±0.2 dex moves A over 0.93–1.33 (canonical). On statistics alone, canonical is
  **+2.6σ high** and alt +0.8σ.
- **The D1 line has little power on amplitude.** σ_sys scales with A, so in the MUTATE twin even Newtonian-baryon lensing
  (A = 5.5) is only 1.9σ_tot on D1. The twin is caught by D2 (+3.8σ) and by D1's χ² (441 / 31).
- **No shape is graded here.** The law's χ² is poor at the best amplitude (p ~ 2e-3), as X53 recorded.
- **Satellites carry a method systematic.** On matched hosts, GH1's lensing reads Δ = +0.17 while satellites read +0.79,
  a +0.62 dex offset in M200. So the satellites' 1.24–1.36 is not used, and the matched-host lensing reading (D2) is.
- **Known answers.** The law stack equals X53's (L) exactly (K1). GH1's ΔΣ and jackknife errors are recomputed exactly
  from its work file (K2, K2b). The law's χ² at A = 1 equals GH1's recorded 28.3 / 28.7 (K3).

## W4. Stability and GW speed

| item | status | number or derivation | source |
|---|---|---|---|
| c_T = c (principal part) | SHOWN | the P sector adds no (∂h)² term at O(h²) on a frozen background with A, P0, ∂P and D·P. The c(x)h∂_z h terms are total derivatives and fold into the mass | W4-K1 here; C8 K9 |
| tensor mass | SHOWN | max \|m²\| 4.50e-43 / 5.44e-43 m⁻² at g = 9.81 m/s² (C8: 4.50e-43 / 5.44e-43); the stiffness part, which C8 did not include, is 2.1e-46 | here |
| no ∂_t N, ∂_t P at β = η = 0 | SHOWN | structural: no time derivative of N or P in the action | action |
| leaf convexity / uniqueness, any background | SHOWN | g″ = a0²/(a0 − u)² − 1 ≥ 0; Schur bound min ratio 1.000000000000 (mpmath, 47k points) | W4-K3/K4; C8 K1, K3; LEAN XC2/XC5 |
| khronon kinetic sign | SHOWN | 𝒦″ = 2μ_K² > 0 | W4-K5; C5 |
| DOF and modes | SHOWN | C4-literal: 2 tensor modes + an ω = 0 pair; no ghost and none unstable at Minkowski and y = 1 | C5 H4 |
| stiff side ω² ≥ 0 | SHOWN | M_θ − 1 + L★²k²/2 ≥ 1e-4 > 0 for x in [1e-4, 1e4] | W4-K6; LEAN `switched_stable_where_positive`; X3 13/13 |
| soft side growth | SHOWN | bounded and k-independent: 0.006–0.20 e-folds; lobes N ≤ 0.048 | LEAN `switched_uniform_bound`; H4; H5 |
| Solar-System background, β = η = 0 | **ASSERTED** | C5 H6's 24 Solar-System points (and 72 NS points) are all η > 0 rows, and they fail WKB validity (g/k ≥ 40.7). X3's D·P > 0 near the Sun (margin ≥ 1.77e4) makes the stiff formula hold only for k ≫ 1/AU | C5, X3 |
| 3D hyperbolicity of the khronon fluid | **ASSERTED** | c² = γ_L(D·P + ρ_d) ≥ 0 is shown in 1D only | X3 |
| caustics | reported | generic (X14). This is a breakdown of the single-stream description, not a ghost or gradient instability | X14 |

AX1's G4 rested on "C5 conditionally healthy". C5 itself is 7/10 with frozen FAILs H5, H6 and H9. H6 never tested v3s's
β = η = 0 form, and H9's β = 0 row is the FRW Jeans onset, which is cosmology and out of scope here.

## Checks

| | result |
|---|---|
| Known answers | W1-K1 Schwarzschild exact (γ = β = 1); W4-K2 law off gives m² = 0; W2 C1–C8 reproduce C6 to Δ = 0; W3-K1/K2/K3 exact |
| MUTATE twin, screening removed (γ_L → 0) | bites in every part, all exit 1. **W1:** the second-order equations have no small-p solution and \|p\|/a0 → 1 (K4, K5 fail). **W2:** Q2 returns to plain AQUAL, 3.49e-26 / 3.91e-26 s⁻², outside the Hees band (FAIL label). **W3:** Newtonian-baryon lensing gives A = 5.5 / 8.5 and a FAIL label. **W4:** the Schur bound fails, min ratio 0 |
| Byte-identical rerun | SHA-256 (first 12 hex digits) w1 json fa3216e91965 / out 5763d45be24c; w2 ac1e29069160 / 7a19d5f2a03d; w3 151bd719d000 / 5f2e3dffb788; w4 60bfa48c00c3 / e027b8332e35. Each equals its `_RERUN` copy |
| Ladders | W2 C6′ three rungs (above); W4 Schur bound in mpmath at 40 digits |

**Disclosed fixes.** All were made after a first execution; no frozen pass line moved.
- **W1.**
  - The first execution's second-order ansatz lacked terms (r³, r² ln r), so K5 failed. It was replaced by direct
    integration of the equations.
  - r-independent g₀₀ terms (a rescaling of t) were dropped from the β remainder: 1.66e-12 → 1.10e-12.
- **W3.**
  - The MUTATE bite test first used D1 alone and did not trip (1.88σ). It now uses the label.
  - The cutoff log in the predicted-ratio bound was made |ln|.
- **W4.**
  - The first W4 execution reached 1.69 GB RSS in a full sympy series and was killed. It was rewritten with a chain-rule
    W expansion.
  - K1 first counted the total-derivative h∂_z h terms as couplings.
  - K4 in float64 gave 0.99999982. That is conditioning at γ_Lξ² = 1e9. It was rerun in mpmath against C8's own line,
    1 − 1e-10 (the code's 1e-12 was not in the frozen text).
- **W2.** The alt L★ = 24 pc (40, 64) rung peaked at 1.0008–1.01e9 bytes (0.93–0.94 GiB), at the 1 GB line, in both
  executions. That cell also fails the ladder line.

## Unfinished
- **Follow-up (11-04):** `../V3X_v3s_close_undecided/` reran W2 and W4c.
  - **W2 is UNDECIDED, reading PASS.** The in-window ladder up to (70,112) meets every V3W line: Richardson −0.70 % / −0.74 %. Its own known-answer check misses at r_Saturn.
  - **W4c: (a) and (c) PASS; (b) is UNDECIDED.** All ω² > 0, but two lines miss.
- **W2 needs one finer rung**, or a lower-memory solver, to clear 2e-2 inside the window. Given second-order
  convergence, the extrapolation already agrees with Route F to 1.3e-3.
- **W4c needs a non-WKB spectrum** of the β = η = 0 khronon pair on the Sun's screened background, and 3D hyperbolicity.
- **W3 has little power on amplitude:** the M★ systematic dominates. A dynamical-mass measurement on the same isolated
  lenses would test the ratio directly; the satellites are not one (GH1).
- **Still open, as in the 10-24 verdict:** clusters, growth/CMB, the radiation era, hosted dwarfs and the MW disc.
