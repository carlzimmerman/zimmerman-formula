# HOSTILE REGRADE — Route D (AeST operator scale ~300-450 kpc) — CONFIRMED NULL

*Opus 4.8 (1M), 2026-06-14. Independent adversarial re-verification of
`ROUTE_D_AEST_OPERATOR_SCALE_2026-06-14.md`. Verdict word UPHELD: CLOSED-FALSIFIER.*

## What I re-derived from PRIMARY sources (not the route's say-so)

**(a) Is the r_C derivation REAL? YES — verbatim-confirmed from the paper.**
Pulled VSZ2024 (arXiv:2304.05134) PDF text directly. Eq. (21) is verbatim:
`r_C ≈ (1/3)[18 r̂_M/(μ²(1+3|Δ|))]^(1/3)`, with `r̂_M = r_M/(1+β₀)`, `r_M = √(GM/a₀)`
(Eqs. 15, 17). The route's `route_d_rC.py` transcribes this EXACTLY. The paper's own
fiducial (top-hat, r_M=12.5 kpc, μ={1,10} Mpc⁻¹) gives r_C={156, 33.6} kpc "see (21)" —
I reproduce {202.7, 43.7} kpc (1.30× high; the paper explicitly inserts "a factor of 1/3
to create a more conservative estimate" and uses exact λ_s/β₀). Order + scaling confirmed;
the 1.3× gap is the paper's stated conservatism, NOT a transcription error. **r_C is a
REAL, paper-native scale genuinely distinct from 1/μ — the route credits this correctly.**

**(b) Is the implied a0_local arithmetic right? YES — recomputed independently.**
- `r_C ∝ M^(1/6) μ^(−2/3) a₀^(−1/6)`: confirmed (M ratio 1e4 → r_C ratio 4.64 = 1e4^(1/6) to <1%).
- Window table at μ=1/Mpc, Δ=0 reproduces: disks 93–242 kpc (BELOW window), group 1e13
  433 kpc (IN window), fiducial cluster 5e14 **832 kpc (ABOVE window)**, 1e15 934 kpc.
- **Disk safety holds:** L* disk r_C ≈ 185 kpc ≫ 30 kpc disk extent → oscillatory regime
  OFF in disks, a0 untouched. This is INDEPENDENTLY CORROBORATED by the paper itself:
  "Requiring r_C to be larger than the virial radius of the Milky Way (∼200 kpc) gives an
  estimate that μ⁻¹ ≳ 1 Mpc." My 185 kpc at μ=1/Mpc sits right at the paper's MW bound.

**(c) Does it REALLY thread? NO — fails the cluster side two independent ways.**
- AMPLITUDE/SIGN: r_C is the ONSET of the oscillatory regime, not a boost. Paper text:
  beyond r_C "the force can become **repulsive**" — a force DEFICIT. Two independent banked
  solvers (Impl-A shooting+point-mass, Impl-B collocation-BVP+beta-model) AGREE on the
  natural-BC amplitude: η(R500)=0.96 / g_AeST/g_MOND=0.20 (point mass), −1.04 (deep-MOND
  profile) — a DRAIN, not the needed 2-25×. The route's sign-check is correct.
- SCALE-IN-M: r_C ∝ M^(1/6) is too weak to track R500. In-window (300-450 kpc) ONLY for
  groups at the CMB-pinned μ; the fiducial cluster sits at 832 kpc, ABOVE.

**(d) Is the SIGN right? NO — wrong sign at the natural BC, confirmed from the paper.**
The oscillatory regime is "additional potential wells and the force can become repulsive"
(VSZ2024) = negative-phantom / drain. The 2.15 boost appears ONLY by tuning Δ (= χ̂_out,
the free integration constant). Paper, Eq. 20: "the actual value for the boundary condition
is fully determined from Δ." The +μ²Φ Helmholtz operator makes φ(∞)→0 DEGENERATE (both
homogeneous modes decay 1/r), so the amplitude is genuinely set by a free finite-radius
constant — exactly the route's "Δ is the tune," and Impl-B nails the mechanism.

**(e) Did the null-steelman MISS a route? NO — I stress-tested two escapes; both fail.**
- *Δ-escape:* to land r_C in-window for the FIDUCIAL cluster needs Δ≈3-5 (computed), and a
  SINGLE universal Δ cannot hold r_C in-window across mass (need Δ: 0.18→1.29→3.30→4.81 from
  1e13→1e15). A mass-RUNNING boundary constant IS a per-cluster tune. And even when r_C is
  tuned in-window, the amplitude there is the banked drain. "Right scale" and "right sign"
  are the SAME single tune — never two independent derived results.
- *μ-escape (one wording refinement):* pushing 1/μ down to 0.3 Mpc DOES bring the fiducial
  cluster r_C to ~373 kpc (in-window) via μ alone — so the route's "in-window only for groups"
  is μ-SPECIFIC (true at the CMB-pinned μ=1/Mpc), not universal. BUT this is the SAME banked-
  dead 1/μ-shrinking: the gauntlet showed 1/μ<1 Mpc breaks SPARC amplitude (+5.4% at 0.1 Mpc)
  and the disk-safe / cluster-boost windows do not overlap (Mistele+2023). The amplitude in-
  window is still the drain. So the μ-escape lands in window only by re-opening the closed
  1/μ null with a deficit sign — verdict unchanged.
- *m_× operator (the one truly DIFFERENT lever):* PRIMARY-confirmed from arXiv:2305.07742.
  m_× ≡ ((2−K_B)/K_B)Q₀ (Eq. 21) — ∝ Q₀, same cosmological constant as μ. It multiplies a
  CURL term that is **identically zero in spherical symmetry** (paper: ∇|∇Φ|×∇Φ=0 "is not
  fulfilled, except in some special cases like spherical symmetry"; "no effect in spherical
  symmetry"). Cluster cores are modeled spherically → m_× constitutionally inert. Effect is
  "percent-level" in wide binaries (abstract). Route's verdict on m_× verified exactly.
- *μ_eff(ρ) chameleon:* μ²=2K₂Q₀²/(2−K_B); Q₀ is the cosmological background scalar velocity,
  K₂/K_B are action constants — none is f(ρ_b). AeST is not density-screened. Inventing
  μ_eff(ρ) is a new tuned input, not a foundation object. Verified.

## VERDICT: CONFIRMED NULL — regrade = CLOSED-FALSIFIER (unchanged)

This is a genuine NULL, not a partial and not a hidden cure. Every load-bearing claim
verified against PRIMARY paper text + independent recomputation:
- the r_C scale is REAL and distinct from 1/μ (credited, paper-verbatim) — the route does
  NOT manufacture-away a real finding;
- but r_C is an ONSET radius inheriting a DRAIN amplitude (η~0.96, repulsive — paper-confirmed),
  scales as M^(1/6) (in-window only for groups at CMB-μ), and its in-window placement rides
  the free Δ/χ̂_out tune (paper Eq. 20 "fully determined from Δ");
- m_× is spherically INERT (paper-confirmed) and percent-level — wrong tool;
- μ_eff(ρ) is not an AeST object; K(Q) is not foundation-forced and CMB-pins 1/μ≳1 Mpc.

No framework-native AeST operator delivers a DERIVED, density-localized, SPARC-safe,
right-signed 300-450 kpc scale. The front converges with the five banked nulls.

ONE HONESTY REFINEMENT for the record (does not change the grade): the route's phrase
"r_C in-window only for groups" is μ-specific (CMB-pinned μ=1/Mpc), not universal — a smaller
1/μ does pull the fiducial cluster r_C into window. But that μ-route is the already-killed
1/μ-shrinking (breaks SPARC, windows don't overlap) with a deficit amplitude, so it is not a
missed cure. Quarantine held throughout: a0/Z never asserted derived; r_C, m_×, K(Q), μ_eff(ρ)
each flagged derived-vs-tuned.

*Primary sources re-fetched and text-extracted this session: VSZ2024 arXiv:2304.05134 (Eq.21,
fiducial r_C={156,33.6}, MW-virial→1/μ≳1Mpc, repulsive oscillatory regime — all quoted from
PDF); m_× paper arXiv:2305.07742 (Eq.21 m_×∝Q₀, curl term, "no effect in spherical symmetry",
percent-level wide binaries — quoted from PDF). Banked companions re-read and cross-checked:
AEST_SINGLE_MU_GAUNTLET, CLUSTER_AEST_MASSTERM, CLUSTER_AEST_MASSTERM_BVP_implB. All route_d
numbers reproduced inline this session.*
