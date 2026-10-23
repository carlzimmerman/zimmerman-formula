# M1_trilemma: is there a way through the v3/v4 trilemma?

## Verdicts (frozen rules, `FROZEN_CRITERIA.md`, committed alone first: 3298c74815)

| route | verdict | the number that decides it |
|---|---|---|
| **R1** Khronon J with J′(0) = 0, equal to J_x above x_min | **NO-GO** (linear growth, theorem for a stated class) **+ residual DEFERRED TO L1** | σ₈ ratio at BS24's cap (μ_K = 14.8 h/Mpc) is **0.121** for J′(0) = 0, against **0.391** for J_x. The window needs μ_K ≥ 411 h/Mpc, **27.8×** the cap. Health PASSES and Cassini PASSES (Q₂/Hees ≤ 2.1e-8, carried over from C6). |
| **R2** screening without γ_L that tolerates a twisting aether (v4) | **NO-GO** for every frozen candidate (one of them conditional on external inputs) | Any C5-healthy AeST/A33 law that matches SPARC leaves the planets an anomaly ≥ **0.96 a₀ = 1.0e4–7.7e4 × their bounds**. Galileons can remove it only with r₃ ≥ 900 Gpc or r₄ ≥ 0.67 Mpc, which costs SPARC **−0.68 / −0.54 dex**. |
| **R3** v4's FRW runaway escape | **MOOT** | R2 has no way through, so v4 has no healthy screening term to rescue. |

**Net:** within the classes tested, the trilemma stands. The only door left open is the one v3 already had: nonlinear
growth from the law's own nonlinearity. That is L1's engine (`rebuild_2026_10_22/L1_khronon_pm/`).

Two corrections to the trilemma as stated:
- **Premise (3) has the wrong mechanism.** The linear failure is not caused by J′(0) = −1. It is caused by the K(Q) dust's
  Jeans scale, which equals the galactic static mass μ_K for every K analytic at Q = 1. Setting J′(0) = 0 makes growth
  **worse**, not better.
- **Premise (1) is stronger than stated.** It holds for every healthy AeST or A33 law, not only the capped F (theorem T2).

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the
framework.

## Run

- `OMP_NUM_THREADS=1 nice -n 15 python3 m1_trilemma.py` gives **11/11 PASS**, exit 0, in 4 s, 0.20 GB peak RSS, one thread.
- `M1_MUTATE=1` flips the sign of J_Y in the BS24 hold equation and reduces the cubic galileon with r⁰. M1 and M6 then
  fail: 9/11, exit 1 (`*_MUTATE.*`).
- No PM simulation was run. CFG960 and L1 were not touched. No downloads.
- **Execution history.**
  - RUN1 (`m1_trilemma_RUN1_crash.out`) crashed on a print format.
    - Before crashing it printed an R1b(iv) summary built on the *suppressed* column.
    - The frozen text names the *dust-limit* column, so the code was corrected to the frozen rule before any verdict
      line was printed.
  - A second run crashed after the verdicts on a JSON type (a sympy Integer). Its output was identical to the final run.
  - The reported-only K-shape number (a_i = 3e-3) was added after the first results. It changes no frozen line.

## R1: a Khronon J with J′(0) = 0

**Additions:** +1 function shape (a Newtonian window f = 1 + J′ = 1 on [0, x_t]) and +1 constant (x_t). Both POSTULATED.

**(a) The y_min forced by data** (x = field strength / a₀).

| footing | SPARC 1st percentile (min) | B21 lowest bin, S/N 8 | x_min | T1: x_t ≤ x_min²/(1+x_min) |
|---|---|---|---|---|
| canonical | 0.118 (0.043) | 4.53e-3 | 4.53e-3 | 2.0e-5 (SPARC only: 1.2e-2) |
| alt | 0.098 (0.036) | 3.75e-3 | 3.75e-3 | 1.4e-5 (SPARC only: 8.7e-3) |

- **T1** follows from health (F = x f non-decreasing). A Newtonian window must sit below F(x_min).
- **These data set no x_min:**
  - wide binaries sit at x_e = 1.30–2.60 (canonical) and 1.15–2.15 (alt);
  - Pal 4 and Pal 14 sit at x_e = 0.07–0.21, and they demand Newton;
  - the E3 dwarfs demand more than the law.
- **B21 caveat.** F2 found B21's isolated outer signal sensitive to the environment. So the "SPARC only" column is the
  robust floor.

**(b) Does linear growth become normal? No.** Three results.

- **Kernel.** From the BS24 PN system (sympy, exact), the khronon dust's own-gravity kernel is
  s(k; f₀) = (μ² − f₀k²)/((1−f₀)k² + μ²), with f₀ = 1 + J′(0).
  - f₀ = 0 (J_x) gives BSK2's kernel; f₀ = 1 (R1) gives the Jeans kernel 1 − k²/μ².
  - ∂s/∂f₀ = −k⁴/((1−f₀)k² + μ²)² < 0 at every k. So J′(0) = 0 holds the dust more, not less.
  - Baryons pull the dust with coefficient 1 at every k.
- **K shape.** For K = Σ cₙ(Q−1)ⁿ (n = 2…5, c₂ = μ², the rest free), lim 4πGρ/c_s² = μ² = K″(1)/2 exactly. So the late
  Jeans scale is the static mass that BS24 Eq. 39 caps from galaxies, for every analytic K.
  - At the cap, Q̄ − 1 = 0.20 at a = 1e-3 and 7.5e-3 at a = 3e-3.
  - So K's shape can act only before a ≈ 3e-3.
- **σ₈ ratio to the dust limit.** Model A, CLASS P(k), F3's two-fluid model. Reproduced first: M0, deviation 0.0.

  | J | a_i = 1e-3 | a_i = 1e-4 |
  |---|---|---|
  | f₀ = 1 (R1) | **0.1206** | 0.0357 |
  | f₀ = 0 (J_x) | 0.3908 | 0.2026 |

  - Diagnostic at a_i = 1e-3: f₀ = 0.01 / 0.1 / 0.5 give 0.388 / 0.363 / 0.226. The ratio falls monotonically with f₀.
  - The PASS line is 0.95, so R1 FAILS. Reaching it needs μ_K ≥ 411 h/Mpc.
  - **K-shape door (reported only).** Even a K that kept the dust exactly cold until a = 3e-3 gives 0.304 (R1) / 0.586
    (J_x).

**Is linear theory around Y = 0 the right expansion? No.**
- This uses the dust-limit field in the modes whose kernel differs from 1 (aμ < k < 10 h/Mpc), model B.
- That field has x = 15 / 3.8 / 0.68 / 0.12 / 0.015 / 1.9e-3 at a = 1e-3 / 3e-3 / 0.01 / 0.03 / 0.1 / 0.3 (canonical).
  - This is 93–7.6e5 × x_t,max on the canonical footing, and 113–9.1e5 × on alt.
  - So the J′(0) window is never sampled. P(x < x_t,max) ≤ 1.7e-6.
- At the epochs that set the σ₈-scale deficit (a ≲ 0.03), the field is x ≈ 0.1–15. So f_t ≈ 0.4–0.96, which is near
  Newtonian (f_t = f + x f′/3).
  - A mean-field WKB estimate with that f_t gives 0.128 (canonical) / 0.121 (alt). It is an **ESTIMATE**, not a verdict.
  - Physically, then, J_x itself sits near the Jeans column, not at BSK2's 0.39.
- **What this means for R1.** R1's J equals J_x wherever x ≥ x_min. The two differ physically only through the law's own
  nonlinear regime.
  - That is the question L1 is building an engine for. L1's GRJ mode is R1's formal Y = 0 limit, and its KX mode is
    v3 = R1 above x_min. So the residual is **DEFERRED TO L1**.
- **SPARC-only variant (reported).** Without B21, x_t,max = 1.2e-2. Then the window *is* reached late (a ≳ 0.1), but only
  by modes with k > aμ ≥ 1.5 h/Mpc. Those are not σ₈-scale linear modes.

**(c) Health and Cassini: both PASS.**
- **Health.** An explicit R1 construction meets C5's 0 ≤ f ≤ 1 and 0 ≤ F′ ≤ 1 on 1e-8 ≤ x ≤ 1e4. It uses x_t = x_t,max/2
  and a smoothstep bridge.
  - Flag: f = 1 at Y < Y_t is C5's edge, M_T = 1/(1−f) = ∞. The dual W is then not C² at P = 0 (the FRW point), so P is
    frozen there as a constraint.
- **Cassini.** C6's kernel sees the law only through f and F′ at x_e = 1.15–2.60. There R1 equals J_x to 1e-16. So
  C6's Q₂/Hees upper ≤ 2.06e-8 (canonical) / 1.76e-8 (alt) and its planets carry over unchanged.

**Theorem (R1 NO-GO).** Take the class:
- the BS Khronon (BS24 PN system);
- any J with f₀ = 1 + J′(0) in C5's healthy range [0, 1];
- any K analytic at Q = 1 with K′(1) = 0;
- μ_K ≤ 14.8 h/Mpc.

In that class, linear σ₈ reaches at most the f₀ = 0 value, 0.391 from a_i = 1e-3 or 0.586 if K is ideal until 3e-3. This
is far below 0.95. The kernel monotonicity is exact. The growth ordering is COMPUTED on f₀ ∈ {0, 0.01, 0.1, 0.5, 1}.

## R2: screening without γ_L for v4 (AeST + C1's capped F)

**Theorem T2 (sympy).** In AeST's and A33's static sector g = u + R(u), with M_L = dg/du = 1 + R′(u).
- C5's health condition M_L ≥ 1 makes u non-decreasing in g.
- So a healthy law that matches SPARC up to x₉₉ = 22.4 (18.6 alt) leaves the planets an anomaly ≥ 8.96e-11 (1.07e-10)
  m/s².
- That is **Earth 1.0e4 ×, Mars 6.4e4 ×, Saturn 1.3e4 ×** their bounds (alt 1.2e4 / 7.7e4 / 1.5e4).
- Reported only, at the conservative x = 1 (u = a₀/2): 5.4e3–4.0e4 ×.
- This generalises C1's "a₀ tail" from the capped F to every healthy F.

| candidate | additions | (S) Solar System | (W) well posed with twist | (G) SPARC cost at the (S) constant | verdict |
|---|---|---|---|---|---|
| **R2a** galileons L₃, L₄ (L₅) of the AeST scalar | +1 term +1 constant each | Spherical law (sympy, exact): R(u) + (r₃/r)u²/a₀ + (r₄/r)²u³/a₀² = g_N. L₅ drops out. Galileon EoM is blind to a uniform field. The cubic screens only outside r_M²/r₃ ("runs inward"). Planets need **r₃ ≥ 900 Gpc** (1090 alt) or **r₄ ≥ 0.67 Mpc** (0.81 alt) | Yes at symbol level: second order, so I1's κ_c² = (1−Bw²)²/(4Aw²) − M²w² → ∞ as A → 0 | median Δlog g **−0.68** (cubic), **−0.54** (quartic); mixes −0.68 (N = 794 / 919 deep points) | **NO-GO** |
| **R2b1** potential / thin-shell (chameleon, symmetron) | +1 field +1 function ≥ 2 constants | Must screen: Sun 2.1e-6, Pal 4 8.9e-11, Pal 14 3.2e-11 (Φ/c²). Must not: SPARC Φ/c² ≥ V_flat²/c², 3.9e-9 to 1.2e-6. Pal 14 is **120× shallower** than the shallowest galaxy, and the Sun is deeper than every galaxy. Both monotone orders fail | Yes (Klein–Gordon) | — | **NO-GO** |
| **R2b2** body density (Hui–Nicolis–Stubbs) | +1 function +1 constant | The Sun is a main-sequence star. Screening it as a MOND source screens disc stars | Yes | Star-dominated deep points: **−0.17 dex** (N 394), −0.18 alt | **NO-GO** |
| **R2b3** ambient field-point density (pointwise T coupling) | +1 function +1 constant | Needs a threshold below the solar wind at Saturn, 0.054 cm⁻³ (EXTERNAL). 70 % (72 % alt) of deep SPARC points lie inside R_HI, where n_HI ≥ 0.067 cm⁻³ at h_z = 300 pc | Yes | It escapes only if every HI disc is thicker than h_z = 371 pc | **NO-GO (CONDITIONAL** on n_sw and h_z, not on disk) |
| **R2b4** curvature | +1 function +1 constant | R-keyed: R = 8πGρ/c² for dust, so it is b3. Weyl-keyed *would* screen: tidal field at Saturn is 4.5e-17 s⁻², against 8.6e-31 at SPARC deep points | **No**: fourth order. The propagator 1/(k² + εk⁴) has residues +1 and −1, an Ostrogradsky ghost | — | **NO-GO (health)** |
| **R2c** capped W, law form, k-mouflage | 0 terms (a choice of F) | T2. AQUAL Q₂ is 2.44–4.59 × Hees (2.85–5.19 alt, E2). Family least-tense 1.41× | Yes (C5 convexity) | — | **NO-GO** |

**R3** is MOOT, because no R2 candidate is healthy and screening at once.

## Errors and soft spots found in the record (not edited)

- **`covariant_push_2026_10_22/THEORY_V3_DRAFT.md` L24 and L64; `rebuild_2026_10_22/F3_growth_audit/README.md` L66.**
  - They attribute v3's linear failure to J′(0) = −1 ("the Newtonian term vanishes on FRW").
  - The BS24 kernel gives the opposite ordering. J′(0) = 0 is F3's own "Jeans" column, and it is lower (0.121 vs 0.391).
  - The cause is the μ_K cap (k_J = μ_K). THEORY §1b's last sentence ("unless the BS dust mass exceeds its allowed cap")
    has it right.
- **`THEORY_V3_DRAFT.md` L24** says AeST's Newtonian term survives in the IR "unlike v3's Khronon J with J′(0) = −1". The
  kernel gives s(k → 0) = 1 for every f₀, so v3's IR growth is Newtonian too. The two differ in where the band ends
  (Khronon k_J = μ_K; AeST k_c ≈ 243 μ with γ_L), not in the IR.
- **F3's "0.03–0.32" range.** The upper end (the BSK2 column) is the formal Y = 0 value. At a ≲ 0.03 the physical field in
  the affected modes is x ≈ 0.1–15, so the physical WKB value sits near the Jeans end (ESTIMATE 0.12–0.13).
- **H1 README.** It says "the AeST counterpart of F3's J′(0) criterion is not λ₀ = 0". The Khronon has no J′(0)
  criterion to counterpart: J′(0) is not what decides v3's growth.

## What this does not show

- **No nonlinear growth.** The deep-MOND (phantom) growth channel, for v3 and identically for R1 above x_min, is L1's job.
- **The BS24 PN system is a WebFetch transcription (PROVISIONAL).** The same holds for BSK1, C4 and L1. The f₀ = 1
  endpoint is cross-checked independently by the k-essence Jeans identity.
- **R2's SPARC costs use a spherical enclosed mass.** They are relative shifts between two laws on the same baryons.
- **R2's (S) uses planets and C6's bounds.** Cassini Q₂ was not re-solved for any R2 candidate, because each fails
  earlier.
- **Classes not tested:**
  - γ_L with an EFT cutoff above κ_c (I1: a posit);
  - non-analytic K at Q = 1;
  - a μ_K above the cap (F3/CFG946: the dust then double-counts in galaxies);
  - two-scale screening operators.
- **R2b3 rests on two external numbers.** n_sw(1 AU) = 5 cm⁻³ and the HI thickness are not on disk.
- **The input ledger** is `FROZEN_CRITERIA.md` §1. No ΛCDM or standard-MOND machinery enters any verdict.
