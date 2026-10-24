# X17_beta_sound_selector: is C1's sound speed a selector with the right sign?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (348993ca40, committed alone before any script or number).
Amendments A1 (PRE-RESULT implementation) and A2 (POST-RESULT check code plus reported-only diagnostics), below.
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. β only inside X14/X15's window.
Not "theory closed". No shear is recomputed; the cluster numbers are read from committed JSON. Nothing here says the data
favour the framework.

## Verdict: WRONG SIGN (frozen rules, both footings)

C1 is not a selector in the needed direction. Its effect on static lensing is exactly zero. Its estimated dynamical
effects either lower the core mass, or are largest in the lightest clusters, which is the reverse of the measured split.
None reaches a quarter of the measured excess. On the cosmic background C1 does not Jeans-suppress the khronon dust; it
makes small-scale linear growth overshoot.

- **Statics: exactly inert** (H-COV, H-PN). C1 is quadratic in the leaf trace K. Every static held configuration has
  K ≡ 0, so C1 adds nothing to any field equation there, at all orders. Static cluster lensing, isolated static galaxies,
  S4's static μ_K branch and its M^{1/6} onset ordering are all exactly v3s's.
- **c_A acts only through motion.** At PN level β enters only the charge equation, as (B/K)∇⁴σ. That term vanishes on
  a held khronon and on a Galilean-boosted held khronon. It acts only where the khronon flow is compressed.
- **The dynamical channels** (ESTIMATES; mass factor ×1; ΔA in units of the law; `DeltaA_summary`):

  | β (footing can / alt) | T1 ΔA⁺ / ΔA⁻ | T2 ΔA⁺ / ΔA⁻ | T3 ΔA⁺ / ΔA⁻ | needed (T2, T3) |
  |---|---|---|---|---|
  | β_min | 0 / −0.143 ; 0 / −0.145 | 0 / −0.132 ; 0 / −0.134 | 0 / −0.119 ; 0 / −0.123 | 0.85, 0.84 ; 0.70, 0.69 |
  | β_max(0.1) | 0 / −0.109 ; 0 / −0.117 | +0.086 / −0.101 ; 0 / −0.109 | +0.097 / −0.091 ; +0.055 / −0.099 | same |
  | β_max(0.03) | **+0.157** / 0 ; **+0.165** / 0 | +0.139 / 0 ; +0.159 / 0 | +0.112 / 0 ; +0.119 / 0 | same |

  - The frozen triggers on both footings (`verdict_triggers`) are:
    - at β_min and β_max(0.1), supersonic member galaxies lower the heavy terciles by ≤ −0.10;
    - at β_max(0.03), the ordering is inverted: T1 +0.157 / +0.165 exceeds T2 and T3.
  - The largest heavy-tercile increase is +0.139 / +0.159 (T2 at β_max(0.03)). The frozen right-sign line is 0.25 × the
    needed shift, which is 0.213 / 0.174.
  - The mass bracket (×0.5, ×2) and member-input bracket widen this to ΔA⁺ ≤ +0.18 / +0.21 and ΔA⁻ ≥ −0.20 / −0.21
    (`DeltaA_bracket`).
- **Growth: WORSE (overshoot) in every window cell, both footings** (step 3 below).
- **Isolated galaxies.** Static isolated galaxies change by exactly 0. Moving subsonic galaxies change by up to
  0.023–0.052 dex, read from X15's `T3b_rotation`.

**How robust the trigger is (A2 diagnostic (a), no verdict weight).**
- H-RESP's own k → 0 limit is 1/(M_θ − 1), the static value. So, at linear order, a moving member's total sub-phantom
  charge does not change. The frozen member estimator applied the large-k (c_A) response to that monopole, so the
  β_min and β_max(0.1) negative triggers are probably an artefact of the estimator.
- With the member channel set to 0, the frozen rules still give **WRONG SIGN** on both footings. The only trigger left
  is the bulk channel's inverted ordering at β_max(0.03): T1 +0.117 / +0.131 > T2 +0.107 / +0.122 > T3 +0.079 / +0.091.
- That ordering follows from X15's estimate, δ ln g ∝ (dg/dg_N − 1)(w/v_c)². At a fixed bulk speed a lighter cluster is
  perturbed more.
- With members off, C1's estimated core effect is at most +0.117 / +0.131 of the law (T1 at β_max(0.03)); every cell at
  β_min and β_max(0.1) is below 0.10. It is largest where the data show no excess.

## The μ-pincer theorem and its scope (P0)

**Source.** `STANDING.md` §"What the September closure established" item 3; `condensate_pincer_2026/
CONDENSATE_MU_PINCER_VERDICT.md` Parts F–G; `condensate_mu_pincer_2026.py` (18/18).

**Statement.** For a shift-symmetric condensate dust, c_s² = K′/(QK″) is a function of the local excitation u alone. So
c_s is set by the dust's local density.
- A static well imposes u_well = −Q₀Ψ for any K.
- The homogeneous background passes through the same state at (1 + z_match)³ = δ_well, with the same sound speed.
- A well that keeps the cold mass out of an L★ galaxy (≤ 30 % of the baryons inside 30 kpc) has δ_well ≤ 5000, so
  z_match ≤ 16. For K ∝ u², u³, u⁴, u⁸ the dust's sound speed at z = 3 is then ≥ 20 km/s, above the forest's tolerance.
  A |u|^{3/2} minimum was ≥ 75–283 km/s on the whole background at z ≥ z_match.
- So **"pressure cannot keep Ω_dm out of galaxies."** This rules out every selector that keeps the cold mass out of
  galaxies by the dust's own pressure with a density-keyed sound speed: barotropic and k-essence pressures, the AeST/BS
  polytrope, v9 DBI, a separate quadratic or walled condensate, superfluid minima.

**C1's c_A lies outside that scope** (P0 PASS).
- c_A² = Bc²(M_θ − 1) with x = |∇Ξ|/a₀. It is keyed to the law field's gradient, not to the dust's density.
- On FRW (x = 0) it is identically 0 at every density. In every static well it is B·x or B(2x + x²), which is > 0.
- So the background never re-visits a well's c_A, and the pincer's premise fails.
- C1 is not a static pressure anyway (step 2). EXCLUDED BY THE PINCER does not apply. C1 fails for a different reason:
  it has nothing static to act on.

## Step 0: reproductions (stop rule; all pass)

| check | result |
|---|---|
| **S0-1** X15's own code | X15's script (sha256 2bf28103…f9e1) was run as a patched copy in a temporary directory (only HERE and ROOT rebound). It exits 0, 13/13 PASS, verdict "C1 SURVIVES PPN", and **0 of 3714 JSON leaves differ** from the committed JSON. This reproduces X15's c_A values and the khronon dispersion. |
| **S0-2** formulas | β_min 1.993547e-6 / 2.197554e-6, β_max 1.004925e-5 (0.1) / 1.116754e-4 (0.03): relative difference 0. The 46 c_A values (fold radii × 3 β × 2 footings, plus X15's cluster point) differ by at most 3.3e-16. c_A at the fold radii at β_max(0.1) is 168–768 / 160–719 km/s. |
| **S0-3** dispersion | X14's `disp` with the C1 transport term gives ω² = (ρ_τ + Bk²/K)(k²/χ − K), residual 0 on both Θ. At ρ = μ_K = 0 it equals X15's root βk²(M − 1 + ΘL★²k²/2)/(2 + 3β), residual 0. |
| **S0-4** cluster numbers (read only) | X7 tercile A_MID (CAL): canonical h0.672 1.096 / 1.852 / 1.837, h0.686 1.113 / 1.922 / 1.876; alt 1.002 / 1.698 / 1.690 and 1.018 / 1.762 / 1.725. These equal X7's printed table, and T1 is lowest in every cell. X2's median MGAS500 is 3.305e12 / 1.1668e13 / 2.9232e13 M☉. X13's corrected A and Z match. F1's median M_gas(<0.5, <1.0 Mpc) is 6.856e12 / 1.695e13 M☉. |
| **S0-5** X4's ODE | F3/X4's ODE copy gives 0.075742 / 0.041440 (μ_K 0.03; a_i 1e-3 / 1e-4) and 0.081714 / 0.044705 (μ_K 0.1), equal to X4. |

## Step 1: c_A by environment (`cA_table`; c_A,⊥ = √(Bx), c_A,∥ = √(B(2x + x²)), km/s; canonical / alt)

| environment | β_min | β_max(0.1) | β_max(0.03) | own speed | Mach |
|---|---|---|---|---|---|
| FRW z = 0 and z = 1100 | 0 | 0 | 0 | 369 (bulk, z = 0); 5.8 (baryon sound speed, z = 1100) | infinite (c_A = 0) |
| FRW stiffness-only, k = 1 Mpc⁻¹ | 4.6e-3 / 5.1e-3 | 1.0e-2 / 1.1e-2 | 3.4e-2 / 3.6e-2 | — | — |
| C1's IR tachyon rate / H (z = 0; z = 1100) | 0.44 / 0.47; 1.9e-5 / 2.0e-5 | 0.99; 4.2e-5 | 0.99; 4.2e-5 | — | — |
| galaxy outskirts 10–100 kpc, M_b 1e9–2e11 | ⊥ 33–581 / 33–565 | ⊥ 74–1305 / 71–1207 | ⊥ 248–4348 / 237–4024 | v_c 60–330 / 62–336 | internal 0.57–1.80 / 0.59–1.88; 0.25–0.80 / 0.28–0.88; 0.08–0.24 / 0.08–0.26 |
| ⋯ 6e10 M☉ at 10 / 30 / 100 kpc, β_max(0.1) | — | ⊥ 821 / 408 / 212 (can), ∥ 1534 / 628 / 306 | — | v_c 208 / 179 / 169 | — |
| T1 cores 0.3–1 Mpc | 93–116 | 209–261 / 199–248 | 698–870 / 664–827 | v_c 362–529 / 378–554 | internal (all terciles, same r) 3.1–5.7 / 3.3–6.0; 1.4–2.5 / 1.5–2.8; 0.42–0.76 / 0.46–0.83 |
| T2 cores | 130–164 | 293–369 / 278–350 | 976–1230 / 927–1166 | v_c 511–740 / 533–773 | bulk 369 km/s: 2.2–2.8; 1.0–1.3; 0.30–0.40 |
| T3 cores | 168–215 / 167–213 | 378–482 / 358–456 | 1259–1607 / 1194–1519 | v_c 668–955 / 694–995 | bulk 369 km/s: 1.7–2.2; 0.77–1.03; 0.23–0.31 |

- **Internal Mach is mass-independent** (C-ID, exact): v_c/c_A,⊥ = √(r/r_β) with r_β = Bc²/a₀.
  - r_β is 31.0 / 28.3 kpc at β_min, 156.4 / 129.4 kpc at β_max(0.1), and 1737 / 1437 kpc at β_max(0.03).
  - At the top of the μ_K = 0.1 window r_β falls between galaxy outskirts and cluster cores. Internal motions are subsonic
    in galaxy outskirts and supersonic (Mach 1.4–2.8) in cluster cores.
  - That is a length scale between galaxies and clusters. But it acts on nothing static.
- **c_A ∝ √x does not separate galaxies from clusters.** The cores' x (0.09–0.52) lies inside the range of galaxy
  outskirts (0.011–3.8).
- For bulk motion at fixed w, heavier terciles are more subsonic. At β_max(0.1), 369 km/s is subsonic at every core
  radius only in T3 (canonical).
- **X15's "449–1032 km/s in cluster cores"** used a 1e14 M☉ point at 300 kpc. The eRASS1 terciles enclose
  2.3e12–2.1e13 M☉ at 0.5 Mpc, so their c_A is lower.
- Reported, `c_eff_k1r`: the full linear stiffness at k = 1/r, which includes the charge's own transport Kρ_ph r², is
  larger than c_A in the cores (for example T3 at β_max(0.1): 626 against 378–482). X15's sub/supersonic labels use c_A
  alone, which is the large-k (Cherenkov) threshold.

## Step 2: the static hold, derived from the action

- **H-COV (covariant; PASS).**
  - (a) For a static diagonal metric with τ = t, K = ∇_μn^μ = 0. A non-static control gives K ≠ 0.
  - (b) In the ADM spherical ansatz (N, N^r, A, B_f), the Euler–Lagrange expressions of N√h K² with respect to N, N^r, A
    and B_f all vanish on N^r = 0, ∂_t = 0 (residual 0).
  - In unitary gauge the khronon equation follows by diffeomorphism invariance.
  - So any static configuration in which the khronon is at rest in the static frame is a solution with or without C1,
    and the leaf problem's uniqueness (convexity, record) makes it the same one.
- **H-PN (PASS).** In X15's 3D PN Lagrangian, B is absent from the φ and P equations. In the σ (charge) equation it
  appears only as ±(B/K)∇⁴σ, which is 0 on σ = −Ct and on σ = −Ct − w·x.
- **H-RESP (PASS).** The moving-source linear response on a uniform held background is
  δρ_τ/δρ_b = (Kρ̄ + Bk²)/[(Kρ̄ + Bk²)(M_θ − 1) − ω²], with ω = k·w.
  - At w → 0 it is the static sub-phantom 1/(M_θ − 1).
  - Averaged over directions it is artanh(Ma)/Ma when subsonic and the principal value ln((Ma + 1)/(Ma − 1))/(2Ma) when
    supersonic.
- **So c_A enters only through bulk motion and the motion of members.** The quantities graded are the cluster's bulk
  motion through the cosmic khronon (X15's step-3b estimate, subsonic cells only) and members moving through the
  cluster's held khronon (H-RESP averaged over a Maxwellian). Both are tabulated in the verdict above.
  - **Bulk.** Every heavy-tercile cell is supersonic at β_min. At β_max(0.1), 16/18 (T2) and 12/18 (T3) cells are
    supersonic on canonical. At β_max(0.03) only 2/18 and 0/18 are.
  - **Member drag at 0.5 Mpc**, only where v_c > c_A: t_drag/t_H = 6.4 / 9.5 / 13.3 (canonical T1 / T2 / T3) and
    6.6 / 9.8 / 13.5 (alt). Members are subsonic at β_max(0.03).
- **Grade: not INERT, under the frozen 0.10 line.** The static effect is exactly 0. The estimated dynamical effects reach
  0.10–0.16 in some cells, so the frozen rules give WRONG SIGN, not INERT.

## Step 3: linear growth with C1 against X4 (`growth`, `G_*`)

- **G-CA0 (PASS).** On FRW (M_θ = 1) the khronon's ω² has no k² term, so **c_A = 0**: C1 cannot Jeans-suppress the
  background dust. With μ_K the mode is tachyonic, ω² = −μ_K²(Kρ̄ + Bk²)/(k² + μ_K²); that is X14's IR band.
- **G-DISP (PASS).** Adding a baryon fluid to X14's system gives the coupled FRW dispersion λ² − Tλ + D = 0 (λ = −ω²),
  with T = Kρ_b + (Kρ_τ + Bk²)s and D = −Kρ_b(Kρ_τ + Bk²)(1 − s). The determinant divided by that polynomial is K²k².
  - The ODE carries exactly these coefficients (eigenvalues agree to 1.9e-16).
  - C1 multiplies the khronon's response to baryon wells by F = 1 + Bk_p²/(Kρ̄_τ). At large k the coupled growth rate
    grows as (Kρ_b B)^{1/4} k^{1/2}.
- **G-LIM (PASS).** At β = 0 the C1 ODE equals X4's ODE (max relative difference 0).
- **Numbers.** F3/X4's ODE (a_i = 1e-3); T² = (δ_m/δ_m,dust)² at k = 0.1 / 0.3 / 1 / 3 / 10 h/Mpc.

  | cell (canonical; alt where different) | R (σ₈ / dust) | ×R(0) | T² at z = 0 | T² at z = 3 | class |
  |---|---|---|---|---|---|
  | μ_K 0.1, β = 0 (X4) | 0.0817 | 1 | 0.0069 / 0.0058 / 0.0056 / 0.0056 / 0.0056 | — | — |
  | μ_K 0.1, β_min | 0.187; 0.217 | ×2.29; ×2.66 | 0.0079 / 0.013 / 0.35 / **309** / 4.4e8 | 0.015 / 0.018 / 0.094 / **8.8** / 1.4e5 | WORSE (overshoot) |
  | μ_K 0.1, β_max(0.1) | 9.97 | ×122 | 0.013 / 0.093 / **37** / 1.7e6 / 3.4e15 | 0.017 / 0.040 / 1.9 / 3.0e3 / 7.8e9 | WORSE (overshoot) |
  | μ_K 0.03, β_min | 0.181; 0.211 | ×2.40; ×2.79 | 0.0064 / 0.012 / 0.33 / **301** / 4.3e8 | 0.014 / 0.018 / 0.094 / 8.8 / 1.4e5 | WORSE (overshoot) |
  | μ_K 0.03, β_max(0.03) | 4.2e5 | ×5.6e6 | 0.13 / **37** / 6.8e6 / … | 0.049 / 1.9 / 7.8e3 / … | WORSE (overshoot) |

  - The a_i = 1e-4 runs give the same classes.
  - The coupled growth rate √λ₊/H at z = 0, k = 10 h/Mpc is 4.3 (β_max(0.1)) and 7.8 (β_max(0.03)), against 0.46 at
    β = 0. At β_min (A2 diagnostic) it is 2.9.
  - The large T² entries are formal linear values. They only mark where linear growth exceeds the dust reference.
- **Comparison with X4: worse.** At β_min the σ₈ ratio rises ×2.3–2.8, but it stays 0.18–0.22 of dust. Meanwhile the
  power at k = 3 h/Mpc overshoots the dust reference ×300–470 today and ×9–12 at z = 3. The Boltzmann R_B is not
  recomputed (C1 is not in Q6's CLASS patch).

## Step 4 (reported)

- **Ordering.**
  - Where C1 raises cores (β_max(0.03)), it raises T1 most: +0.157 / +0.165 against +0.139 / +0.159 (T2) and
    +0.112 / +0.119 (T3).
  - Where it lowers them (supersonic members), it lowers T1 most: −0.143 / −0.145 at β_min.
  - Bulk subsonicity rises with mass (c_A ∝ √x).
  - The record's split runs the other way: T1 shows no excess and T2/T3 do.
- **S4's onset ordering** r_C ∝ (r_M/μ_K²)^{1/3} ∝ M^{1/6} is unchanged. S4's static branch is a static held
  configuration, so H-COV applies.

## Checks

- **Main run: 13/13 PASS, exit 0.** The checks are S0-1 … S0-5, P0, C-ID, H-COV, H-PN, H-RESP, G-LIM, G-CA0 and G-DISP.
  - 10 s; peak RSS 0.16 GB, with 0.10 GB in the X15 child process; one thread, nice 15, PYTHONHASHSEED=0.
- **MUTATE (`X17_MUTATE=1`): exit 1.** Exactly the seven required checks fail, and nothing else:

  | mutation | change | fails |
  |---|---|---|
  | m1 | K² replaced by a_ia^i | H-COV (the acceleration term's Euler–Lagrange expressions do not vanish on static configurations) |
  | m2 | H₀ doubled in β_max | S0-2 |
  | m3 | X15 copy run with its own MUTATE | S0-1 (915 leaves differ) |
  | m4 | X7 terciles reversed | S0-4 |
  | m5 | F3 kernel s = 1 | S0-5 |
  | m6 | F → 1/F in the growth ODE | G-DISP |
  | m7 | the density-keyed polytrope in P0 | P0 (inside the pincer's scope) |

  The MUTATE verdict line is the control's output, not physics.

## Amendments and execution history

- **348993ca40:** criteria and ledger, committed alone.
- **A1 (PRE-RESULT, implementation; before the first full run).**
  - A scratch test of the symbolic pieces alone (no physics numbers) found that `sp.simplify` of the 9 × 9 baryon +
    khronon determinant did not finish in 10 min. G-DISP now uses a Berkowitz determinant with expand/cancel, and H-RESP
    uses an LU solve.
  - P0's failure mode "inside the pincer's scope" maps to verdict rule 2 (EXCLUDED), not rule 1. The frozen text listed
    P0 among the required checks and also defined rule 2 by its result; this implements §1's last paragraph.
  - The member Maxwellian average is computed once per speed (efficiency only).
- **A2 (POST-RESULT).**
  - RUN1 (kept as `x17_beta_sound_selector_RUN1.out` / `_results_RUN1.json`) failed only H-RESP. sympy had left
    2·artanh(½) − ln 3, which is identically 0, unsimplified. The check now rewrites in logs first.
  - Every other line of RUN1 is identical to the scored run, including the per-footing classes (WRONG SIGN on both).
  - Added, reported only and with no verdict weight: (a) the frozen rules re-run with the member channel off; (b) the
    coupled growth rate at β_min; (c) the cells that set the bulk maxima. The verdict logic was moved into a function that
    also records its triggers; the rules are unchanged.

## What this does not show

- **The dynamical channels are estimates.**
  - Bulk motion uses X15's self-similar step-3b formula on a point-mass phantom with R_h ∈ {1, 10} Mpc. Supersonic cells
    are not estimable.
  - Members use a WKB response on a uniform held background. Its monopole is static at k → 0 (A2 (a)), so the member
    channel is likely smaller than graded.
  - No 3D moving-cluster solution and no wake mass are computed.
- **The terciles' enclosed masses are self-similar scalings** of F1's sample medians, bracketed ×0.5–2. Speeds and R_h
  are illustrative.
- **Growth is F3/X4's linear ODE at x = 0.**
  - The perturbations' own acceleration enters only at second order. Once |∇Ξ|/a₀ exceeds s(k) ≈ (aμ_K/k)², it switches
    on c_A² = Bx and would stabilise a mode. That nonlinear saturation is not computed (it is L1's kind of question).
  - The literal K(Q) background (radiation-like khronon until z ≈ 35–78 in the Boltzmann run) is not modelled.
  - The overshoot is a linear-theory statement within X4's framework, not a Boltzmann or N-body result.
- Binary-pulsar radiation, neutron-star sensitivities and 2PN with C1 remain uncomputed (X15).

## Suggested fixes elsewhere (not edited here)

- **X14 / X15 (C1's window).** The upper edge β_max uses only the khronon's own IR band, Bμ_K² ≤ H₀². With baryons the
  coupled FRW mode has D = −Kρ_b(Kρ_τ + Bk²)(1 − s), so its growth rate rises as k^{1/2} at large k. Even at β_min,
  linear power at k = 3 h/Mpc overshoots the dust reference ×300 today and ×9 at z = 3 (formal, in X4's framework).
  - Suggest a frozen lane on whether nonlinear saturation (x > s(k)) rescues this, or whether the forest closes C1's
    window.
- **X15 step 3 / V3_FULL_PICTURE §6.** "c_A 449–1032 km/s in cluster cores" is for a 1e14 M☉ point at 300 kpc. For the
  eRASS1 terciles at 0.3–1 Mpc, c_A,⊥ is 209–482 (canonical, β_max(0.1)).
  - Internal motions are subsonic only inside r_β = Bc²/a₀ (156 / 129 kpc at β_max(0.1)), independent of mass.
  - The sub/supersonic labels ignore the charge's own transport stiffness (`c_eff`).
- **V3_FULL_PICTURE §5.** After "the record's μ-pincer theorem rules out pressure for that role", add: C1's sound speed is
  outside the pincer's premise (it is acceleration-keyed and zero on FRW), but it is not a selector either. It is exactly
  inert in statics. Its dynamical effects have the wrong mass ordering, and on FRW it amplifies small-scale growth
  (X17).
- **V3_FULL_PICTURE §6, row "Cluster light/heavy split".** Add: X17 finds no C1 mechanism for the split. Its estimated
  effects are largest in the lightest tercile.
- **MAP §4.** Add a row for X17 with the verdict above.

## Files and run

| file | contents |
|---|---|
| `x17_beta_sound_selector.py` | Parts S0, P, C, H, G and V. Copied with provenance: X14's `disp`; X15's `aqual_point`, `p1_of`, `L3` and step-3b and drag forms; F3/X4's ODE. X15's script is run as a patched copy in a temporary directory. |
| `x17_beta_sound_selector.out`, `_results.json` | the scored main run |
| `x17_beta_sound_selector_MUTATE.out`, `_results_MUTATE.json` | the MUTATE run (m1–m7) |
| `x17_beta_sound_selector_RUN1.out`, `_results_RUN1.json` | the first full run (H-RESP check-code defect; see A2) |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X17_beta_sound_selector/x17_beta_sound_selector.py              # exit 0
PYTHONHASHSEED=0 X17_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X17_beta_sound_selector/x17_beta_sound_selector.py  # exit 1 by design
```
