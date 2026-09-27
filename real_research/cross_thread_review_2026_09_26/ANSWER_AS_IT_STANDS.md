# The answer as it stands: ASSEMBLING

2026-09-26/27. This page is assembled from the parallel threads' results. Every row cites a lane and a commit, or
says it is pending. Owners check their own rows before each commit. **The closure target is OPEN.** κ = ½ is a declared
input. The dark mass is required; what it is (a non-particle continuum) is being worked out.

Before any update, the automated gate `XR10_answer_validator.py` must pass. It flags any row that is not on the model
below (switch reading, cap form, cell, kernel, carrier, operator, footing).

## 1. The model M*

- **Gravity.**
  - GR plus the khronon: C-H/K, BPS with α_c > 0 and β = 0, and the leaf average. Causality is criterion B. c_T = c.
  - The one covariant action is being written as V0, in `real_research/chk_v0_2026/`. CV1 and CV2 are committed;
    CV3 and CV4 are pending.
- **MOND.**
  - The kernel is ν_mono, which equals ν_RAR for y ≤ 2.337 and never differs by more than 0.0104 dex. It is
    heat-filtered and region-local (L361, σ = 1).
  - a₀ = κ c √(G ρ_Λ) with κ = ½ declared, so a₀ is flat in time.
- **The switch.**
  - It reads the MOND sector only, i.e. the baryons and their phantom. In CV3's constrained form this is
    C[∇²(u−v) + ∇·((ν−1)∇Sw)], and it never reads the carrier (MS1, CV3).
  - It is gated by the vacuum: x_c,eff(z) = x_c0 [Ω_Λ0/Ω_Λ(z)]^p with p = 1, x_c0 = 2.5 (DE2/DE9), and the transition
    width is w ≤ 0.25.
  - MOND regions are capped by MS5's κ-form action term: U_cap = C·m(∇²Φ_X, v_cap² κ_X²). Every region ends at
    v_cap/(H√x_c): 1.75 Mpc at z = 0.5 and 2.99 Mpc at z ≈ 0. v_cap = 325 km/s is declared.
  - XR9 is testing a higher x_c0 ("the small-region door").
- **The dark mass.**
  - It is required by the CMB and by clusters.
  - It feels Newtonian gravity only (L353 reciprocity).
  - It is cleared from galaxies by a density-triggered conversion with a kick of 575–650 km/s (L388). That trigger is
    posited, with no action yet.
  - Its identity is being worked out: the user asked for a fluid that "is not particles". XR8 is testing non-particle
    continua and DF1 is placing them in V0. The kick is being worked as a phase transition of that fluid.

## 2. Derived, declared, posited

| Item | Status | Evidence |
|---|---|---|
| a₀ = κc√(Gρ_Λ), flat in time | κ = ½ **declared** (measured 0.465 ± 0.076; not derivable in this action class); flatness by construction | k01–k03; the recipe |
| ν_mono kernel | **declared** (the author's decision, 09-26); monotone phantom, C² splice | 9092fc0fd, XC4 |
| The switch reads the MOND sector | **derived as the only leak-free reading** once the gate is varied | MS1, CV3 (pending commit) |
| The region cap | **written as an action term** (κ_X); v_cap declared | MS5 61a3a0858 |
| Gate p, x_c0, w | **declared**, pinned to a window by the data | DE2, DE9 |
| The carrier's trigger and kick | **posited** | L388; phase-transition lead pending |
| What the dark fluid is | **open** | XR8, DF1 pending |
| Well-posedness | leaf problem convex at any lapse (XC5); principal symbol GR + BPS khronon on the conformal-leg model (XC6); zero-field √ε response open | XC5, XC6 |
| Strong coupling (G8) | **bounded pass**, frozen-background decoupling scope | XC1, XC3, XC6 |

## 3. Scorecard on M*

| Gate | Verdict | Numbers | Lane | State |
|---|---|---|---|---|
| Flat-a₀ flagship, z = 2.5 | pass, needs no CGM | on at r_F for every CGM share | MS2 | committed |
| KiDS-1000, carrier lensing included | pass | Δχ² −37.0/−34.0 (hard), −32.3/−29.3 (w = 0.25) | DE10 dabce1b73 | committed |
| Cosmic shear, halo model | pass **only with the cap** | 1.049/1.124 (w 0.25); uncapped 2.7/3.2 | MS3, MS4 969a15e7f, MS5 | committed |
| Lyman-α forest | pass (conservative: the operator over-states the phantom) | worst 0.0041 (25 Mpc/h, alt, z = 2) | DE11 aa6588d56 | committed; DE11b convergence pending |
| RAR, RC100 | pass | carrier shift ≤ 1.24e-4 dex; f_DM 0.23/0.26 | L391 441d811e2 | committed |
| S₈, galaxy clearing, X-COP (particle-mesh) | pending | — | L396 (κ-form cap) | pending |
| Harvey mergers | knife-edge | S2 passes only at 575 km/s; S1 at 575–625 (provisional) | L389 → L397 | pending |
| EFE, cluster-infall BTFR | fails | 3.0–3.1σ scalar / 4.9–5.5σ subtract with the withdrawn cap; κ-form re-score pending | XR6 6566c53b3 → XR9 | re-score pending |
| EFE, Local Volume dwarfs | fails | 3.9–4.5σ | XR6 | committed |
| Local Group zero-velocity radius | fails | 1.41/1.48 Mpc vs 0.96 (+0.17/+0.19 dex) | XR6 | committed; XR9 re-score |
| Coma UDGs | fails, weaker than before | 4.35/4.20σ | XR6 | committed |

## 4. Doors closed today (tried, failed, recorded)

- The matter-only switch fails KiDS everywhere (DE8, L392). The curvature switch leaks onto the carrier and makes
  lensing differ from dynamics (MS1, DE7). The K-only gate is blind (CV4).
- The withdrawn cap form fails shear (MS5). "One number sets the cap and the kick" is false (XR7).
- GP4's window is withdrawn (PAPER34 v3: P34c/P34d). L373 at p = 2 has no window. Astra's w = 1 gate has no window
  (DE9).
- The acceleration-triggered carrier (AT) fails halo-model cosmic shear at every KiDS-safe cap and every kick Harvey
  allows: the best is 1.26 against 1.2 (AT4 b844a87b3). AT5, a two-sided trigger, is being tested as a labelled
  alternative.
- L374's shell-crossing runaway is not the kick: it tracks the host and leaves a warm fluid. Every mock-based
  cosmic-shear pass is not established (MS3, DE5b).

## 5. Data gates ahead

- Gaia DR4, 2026-12-02 (frozen pre-registration).
- The z ≈ 2.5 deep-MOND Tully–Fisher zero point: needs JWST and ALMA; no clean rotators yet.
- Euclid DR1, 2027.

## 6. Pending, and who owns it

- The particle-mesh chain: L395 (running; cell (c) uses the withdrawn cap in its dynamics and is labelled mixed), then
  L396 (κ-form cap, 575 km/s), then L397 (Harvey at its own epoch). Owner: RPO work toward closure.
- XR9, the small-region door, including the κ-form EFE and Local Group re-score. Owner: this review.
- XR8 (the fluid's continuum tests) and DF1 (the fluid in V0). Owners: this review and the V0 writer.
- The kick as a phase transition. Owner: Path forward.
- CV3/CV4. Owner: the V0 writer.
- **DE12, a possible new obstruction** (DE thread; replaces a DE7 re-run).
  - In CV3's auxiliary form the gate leaves the metric's principal symbol alone. Its slip is ~1e-5 of DE7's, which
    is negligible.
  - But its second variation acts on baryons as a negative bulk term, amplified by A² ~ 1e4 in deep MOND. The
    estimated stability threshold is σ_b ≳ 10³ km/s in L* edge layers, against 30–100 km/s in the gas there.
  - DE12 computes:
    - the growth rate against H(z) and the layer's crossing time;
    - the baryon mass in transition layers;
    - the A = 1 control, a baryon-only reading;
    - the gate potential's shift of the flagship zero point.
  - It is an obstruction only if Γ ≫ H on real transitions with real gas.
- AT5 (a two-sided acceleration trigger), a labelled alternative. L393, the curvature comparison.
- PAPER34 v3: the source is ready; the upload waits for the author's go.
