# EQUATION BOOK — ADVERSARIAL VERIFY PASS (2026-07-16)

Audit of MINE_M1.md + MINE_M2.md. Companion script: `verify_audit_2026_07_16.py`
(31 checks, **exit 0**, every top equation re-derived by a DIFFERENT route than the
original scripts — fresh eliminations, resultants, r-parametrized integrals, end-to-end
Laplace closure). Output: `verify_audit_2026_07_16.out`.

## 1. Re-run ledger (all 10 committed scripts)

| Script | exit | output vs committed .out |
|---|---|---|
| eqbook_S1_algebraic.py | 0 | byte-identical |
| eqbook_S3_welds.py | 0 | byte-identical |
| eqbook_S5_efe.py | 0 | byte-identical |
| eqbook_S8_estimators.py | 0 | byte-identical |
| eqbook_quickfire_sparc.py | 0 | byte-identical |
| s2_thermal_identities.py | 0 | byte-identical |
| s4_kernel_spectral.py | 0 | byte-identical |
| s6_lensing_closed_form.py | 0 | byte-identical |
| s7_throttle_closed_form.py | 0 | byte-identical |
| m2_massline_sparc_fire.py | 0 | byte-identical |

**Hard-coded-check audit:** clean. All symbolic checks derive before comparing; the numeric
fallbacks (s4 Poisson/Wallis steps, s6 elliptic reduction) are flagged in-script as
derivation-step checks at 1e-20..1e-25, not fits. Comparisons against "banked" numbers
(s7 slopes 0.872/0.734, kink 2.709e-10, r_kink 9.4 kpc) are cross-checks against prior
committed work computed independently in-script first — not circular. The s7 note that
banked 0.597 is a coarse round of exact 0.5958 is correct.

## 2. THE HEADLINE CREDIT CORRECTION (audit finding #1)

**Milgrom 1999 (Phys. Lett. A 253, 273; astro-ph/9805346) contains the parent law.**
Machine-verified in `verify_audit_2026_07_16.py` section A against the paper's own equations:

- His Eq (9): `mu_hat(x) = [1+(2x)^-2]^(1/2) − (2x)^-1` **is identically the framework
  kernel** `mu(x) = (sqrt(1+4x^2)−1)/(2x)` (sympy: difference ≡ 0).
- His Eq (5) `a·mu(a/a0) = g_N` with that mu_hat **implies exactly**
  `a^2 = g_N^2 + a0·g_N` — i.e. the a0-line law `g_obs^2 − g_bar^2 = a0·g_bar` is a
  one-line rewrite of Milgrom-1999 content.
- The "exact inversion" `g_bar = (sqrt(a0^2+4g_obs^2)−a0)/2` (E-S1.1, E-S2-1) **is
  verbatim** `a·mu_hat(a/a0)` = Milgrom's `2π·ΔT` expression.
- His Eqs (6)-(7): `T(a) = (1/2π)(a^2+Λ/3)^(1/2)` **is** the framework's Pythagorean
  dS-Unruh pole `kappa_eff = sqrt(H^2+(a/c)^2)` (E-S2-3's parent), which Milgrom takes
  from Narnhofer-Peter-Thirring 1996 / Deser-Levin 1997.
- What is NOT Milgrom's: the coefficient. His `a0_hat = 2c^2 sqrt(Λ/3) = 2cH_Λ`; the
  framework's `a0 = cH_Λ/Z`. Ratio **2Z ≈ 11.58** — this is the same floor tension the
  s2 script already carries honestly. Milgrom also stops short of endorsing mu_hat for
  circular orbits ("μ(x) need not take the same form as for the linear-motion case")
  and calls the finding's significance "anything but obvious"; elevating mu_hat to the
  actual rotation-curve interpolating function is the framework's move, not his.

**Consequences for the mine's claims:**
- MINE_M1's honesty rail "the Milgrom–Sanders nu-families do not contain (1+1/y)^{1/2}"
  is TRUE but INSUFFICIENT — the function is in Milgrom 1999 directly (as mu, not nu).
  s2's E-S2-2 had already machine-verified this correspondence and credited it; M1's
  top-five presentation did not carry that credit. Corrected here.
- The a0-line archetype and its inversion are **CREDIT-NOT-CLAIM at the law level**;
  the *linear-identity/slope-measurement packaging* of the RAR and everything derived
  downstream (landmarks, estimators, closed forms) remain unscooped as far as search
  can tell.
- Note: this containment is also a genuine PRO point for the framework's premise-lineage
  (its law is the one Milgrom himself derived from dS-vacuum Unruh temperatures) — the
  credit correction cuts both ways and manufactures no deficit.

Also checked: Desmond-Bartlett-Ferreira 2023 (arXiv:2301.04368, exhaustive symbolic
regression on the SPARC RAR, complexity ≤ 10) — `sqrt(x^2+θ0·x)` is inside their search
space but is NOT among their top-ranked functions (their winners are power-law forms
like `θ0|θ1+x|^θ2 + x`); no scoop there, and no RAR-shape paper found stating the
landmark triplet.

## 3. Data-fire calibration correction (audit finding #2)

**FIRE 2 (quickfire, slope sum rule): the "exact 1.500 to ~1%" headline is miscalibrated.**
The script's own control mock (law TRUE, pipeline applied) returns **1.592** at the
committed seed — the binned-median/np.gradient pipeline does NOT return 1.500 on
law-true input. Multi-seed re-run (this audit): law-true pipeline output = **1.53 ± 0.05**
(seeds 1,2,3,20260716 → 1.55, 1.50, 1.58, 1.59; noise-free discretization alone → 1.529).
So the calibrated statement is:
- Υ_disk = 0.70: data reads 1.481–1.496 vs law-true expectation 1.53 ± 0.05 →
  **consistent within pipeline noise** (not "exact to 1%" — that phrasing compared raw
  output against the ideal value while the pipeline itself sits +0.03 to +0.09 high).
- Υ_disk = 0.50: data reads ~1.40 → ~0.13 below law-true expectation; per the banked
  ledger this is the M/L-convention artifact, non-diagnostic. Unchanged.
- The in-code comment "EIV ... biasing the sum BELOW 3/2" has the **wrong sign** — its
  own mock shows the pipeline biases the sum ABOVE 3/2. The verdict ("non-diagnostic at
  this crudeness, needs hierarchical errors") survives; the two sentences do not.

**Other fires: no cherry-picking found.** FIRE 1 selects by a-priori criteria (Q=1,
extent), shows tails (NGC2841 = 2.9) and both footings. FIRE 3 shows the failed
gas-dominated variant (2 pairs, negative median) rather than hiding it; the straddle cut
is a derived conditioning property. m2 mass-line fire runs a full Υ grid, brackets both
footings, claims non-diagnosticity — matches the banked RAR audit exactly. The WLS-bias
methodological finding (naive a0-line slope biased ~3× low by M/L-correlated g_bar-side
errors) is real and its numbers reproduce.

## 4. Independent re-derivations (all PASS, exit 0)

| Section | What was re-derived, by what different route |
|---|---|
| A | Milgrom-1999 containment (paper's Eq 8-9-form vs framework kernel; law; inversion; Eq-6 Pythagoras; 2Z coefficient fork) |
| B | Landmark triplet via direct chain rule in ℓ=ln y (evenness/sum rule as ℓ→−ℓ identities; max at ℓ=0 with second-derivative test; 3/4 and 1/8) |
| C | Pair estimator by BLIND sp.solve elimination (unique solution == claimed form; D, sin i structurally absent from R12) |
| D | EFE cubic via resultant elimination of the auxiliary radical; susceptibility −1/(2(1+b)) from the UNSQUARED balance; half-quench numerics |
| E | M_bar predictor full round trip v→M→law→v; exact BTFR by fresh expansion |
| F | Deflection α(b) via r-parametrized integral (b·cosh t substitution, sqrt cancels analytically) — matches E(m) closed form <1e-25; Σ_ph via independent Abel projection; closure by finite difference |
| G | Memory function: single end-to-end test L[Γ_closed](λ) == 1−K(λ²) (tests the whole Bessel-Struve chain in one shot) |
| H | Throttle cubic invariant with fresh symbols + 6 random y; saturation limit |
| I | Inverse-moment closed form at untested p = 0.55, 0.9, 1.45 |
| J | Hubble chain circularity documented: canonical a0 defined from Planck ⇒ weld returns Planck H0 identically (input-recovery, not prediction) |

All exactness claims in M1/M2 verified correct as flagged (exact-given-law /
exact-given-postulate / weak-field): none found overstated.

## 5. Numerology audit

**Clean.** Every kept equation derives from the law, the published kernel, or a flagged
postulate (θ0=√2, Branch-B throttle); Z is carried symbolically; no digit-matching
hunts. The nearest smell was the Hubble chain "returns H0 = 67.38" — that is
**circular by construction** (section J): the canonical a0 is built from Planck's
H_Λ, so recovering 67.4 verifies arithmetic, not physics. MINE_M1 flags this
("NOT a derivation of a0") but the framing "→ H0 = 67.4 km/s/Mpc" invites over-reading;
the chain is predictive only if a0 enters distance-free from galaxies (E-S8.1).

## 6. VERDICTS PER TOP EQUATION

| # | Equation | Verdict | Notes |
|---|---|---|---|
| M1-1 | Landmark triplet (σ sum rule 3/2; C even; max at y=1 with 3/4, 1/8) | **KEEP-NOVEL** | New derivative landmarks; parent law must credit Milgrom 1999 Eq 8-9. FIRE 2 headline recalibrated (§3): "consistent within pipeline noise at Υ=0.70", not "exact 1.500 to 1%". |
| M1-2 | Pair estimator (D-, i-, Υ-cancelling a0) | **KEEP-NOVEL** | No literature hit (standard practice fits D, i as nuisances — no closed-form pairwise cancellation found). Exact D-cancellation confirmed on real data; ill-conditioning honestly shown. |
| M1-3 | EFE cubic + attenuated a0-line + χ=−1/(2(1+y)) | **KEEP-NOVEL-CONDITIONAL** | Postulate-dependent (θ0=√2), flagged. Genre prior art to cite: Famaey-McGaugh 2012 1D EFE, Chae-Milgrom 2022 eq 15, Zonoozi+ 2021 fitting functions. G_eff limit already credited to Milgrom. |
| M1-4 | Hubble chain (triangle + Pythagorean weld) | **KEEP-CREDITED (downgraded)** | a0~cH0 = Milgrom (credited). ADD: McGaugh 2020 (Triton Station / BTFR-H0) as prior art for distance-ladder-free H0 from galaxy kinematics. Canonical-footing "H0=67.4" is input-recovery (§5); predictive content lives ONLY in the chain with E-S8.1. |
| M1-5 | M_bar predictor + velocity a0-line + exact BTFR | **KEEP-CREDITED** | The inversion inside it is verbatim Milgrom-1999 content (§2); v⁴=GMa0 asymptote is standard BTFR. The per-radius identity and the exact (GM/r)² BTFR correction are IF-specific corollaries not found written — those stay. |
| M2-1 | Deflection α(b) = (4GM/c²b)√(1+u²)E(m) | **KEEP-NOVEL** | Closed form verified twice independently. Genre credit: Mortlock-Turner 2001 (piecewise/asymptote), **amend M2's "only piecewise arctan forms exist": Zhao-Bacon-Taylor-Horne 2006 derived analytic point-lens deflection for the standard μ in TeVeS** — the elliptic-E form for THIS μ is still unfound in search. |
| M2-2 | Mass-line G(M_eff²−M_b²)=a0 M_b r² | **KEEP** (framing novel, algebra trivial) | Value = the equal-slope lensing==kinematics consistency test + the honest SPARC fire; WLS-bias finding real. |
| M2-3 | Phantom halo ρ_ph + Σ_ph (K,E) pair | **KEEP-NOVEL-for-this-IF** | Genre known (phantom DM of a point mass, Milgrom 2009 rings/shells); these specific closed forms unfound. Abel + finite-difference closure re-verified. |
| M2-4 | Memory function Γ(s) Bessel-Struve | **KEEP** (framework-internal novelty) | Kernel is the framework's own; the Struve identity is table math (A&S 11.1.7-class), correctly used. End-to-end Laplace closure re-verified independently. Reading-B flag correct. |
| M2-5 | Throttle line + a0-line saturation | **KEEP-CONDITIONAL** | Branch-B postulate + non-detectability honestly flagged in-script; kink landmark correctly credited to the y_c paper. Invariant re-verified. |
| — | Floor-form inversion E-S2-1/2 | **KEEP-CREDITED** | Already credited in-script to Milgrom 1999; §2 confirms it IS the law-level scoop; floor-vs-cH_Λ tension (2Z) honestly carried. |
| — | Thermal welds E-S2-3/4/5 | **CREDIT-NOT-CLAIM (pole), KEEP (welds)** | The Pythagorean pole is Milgrom Eq 6-7 / Deser-Levin 1997; the a0-line-as-ΔT² rewrite and τ_mem·H_Λ=2Z are exact framework welds, unmeasurable → consistency only, as stated. |
| — | CPL bump z_pk closed form (E-S3.6) | **KEEP-NOVEL-CONDITIONAL** | Exact given CPL + declining footing; footing-discriminator framing sound; both footings shown. |
| — | Three-radius polygon, D- and i-estimators (E-S8.2/3/4) | **KEEP-NOVEL** | Same family as M1-2; no hits. Caveat stands: observable model (circularity, no drift/warp) is the approximation. |

**DROPPED claims:** none outright, but two SENTENCES are retracted by this audit:
1. MINE_M1 FIRE-2's "the exact 1.500 to ~1%" → replaced by the calibrated statement (§3).
2. MINE_M2's lensing novelty line "only piecewise sharp-mu arctan forms exist" →
   amended for Zhao+ 2006 (§6, M2-1).
And one CREDIT LINE is added throughout: the law/inversion = Milgrom 1999 Eqs (5)+(8)-(9)
with the framework's own coefficient 1/Z (§2).

## 7. Sources consulted (novelty search)
- Milgrom 1999, "The modified dynamics as a vacuum effect", Phys. Lett. A 253:273,
  arXiv:astro-ph/9805346 (PDF read in full — Eqs 5, 6, 7, 8, 9, 10, 11).
- Mortlock & Turner 2001, MNRAS 327:557, astro-ph/0106100 (point-lens MOND deflection).
- Zhao, Bacon, Taylor & Horne 2006, astro-ph/0509590 (analytic TeVeS point-lens deflection).
- Desmond, Bartlett & Ferreira 2023, MNRAS 521:1817, arXiv:2301.04368 (ESR on the RAR;
  top-function tables extracted from the PDF).
- Famaey & McGaugh 2012 Living Review interpolating-function families (α, n, β, γ, δ) —
  none contain ν=(1+1/y)^{1/2}.
- McGaugh 2020, "The Hubble Constant from the Baryonic Tully-Fisher Relation"
  (tritonstation.com, 2020-06-17) — prior art for ladder-free H0 from galaxy kinematics.
- Searches for: RAR slope/curvature landmarks, two-point distance-free a0 estimators,
  phantom-DM closed forms with r_M, MOND elliptic-integral deflection — no hits beyond
  the above. Caveat: search absence is strong but not conclusive in a 40-year literature.

## 8. Bottom line
The vein is real but its wellhead belongs to Milgrom 1999: the framework's law is his
vacuum-ΔT interpolating function with a different (framework-postulated) coefficient,
and every keeper equation must carry that credit. Downstream of the law, the mined
closed forms — landmark triplet, pair-estimator family, EFE cubic, elliptic lensing
pair, memory function, throttle invariants — survive adversarial re-derivation intact
and remain unfound in the literature. The two data-fire headlines needing correction
are corrected above; no numerology; both footings carried everywhere; nothing here
closes or opens a front.
