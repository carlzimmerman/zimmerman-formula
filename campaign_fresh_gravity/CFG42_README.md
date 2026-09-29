# CFG42 — B's derived cold-mass rule on the dwarfs: it closes the ultra-faint failure and over-predicts the classical dwarfs

Script: `CFG42_satellites_rule.py`, about 3 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Every collapse mass is divided by 100, and H1 and H3 both fail (rc = 1).
- The main run exits 1: **H2 failed** (the classical satellites reject the rule).

## Question

The rule (CFG35–CFG39) says the cold fluid is conserved and keeps its collapse mass: dark = phantom + leftover collapse debris. It had only been tested where weak lensing measures the collapse mass (log M_* > 10.2). The satellites, where B's largest standing failure sits (the Milky Way's ultra-faints, 3.5–3.8σ, CFG28–CFG29), had never been scored with it.

An NFW cusp makes the ultra-faint answer nearly independent of the halo mass. Inside a small radius the enclosed mass scales only as M_halo^0.13, so the rule is close to parameter-free there. The same cusp is the danger for the classical dwarfs.

## Method (declared before the first run)

- CFG36's machinery exec'd read-only, with FG001's committed loader and estimator: σ² = g(r) r / 3 at r = (4/3) r_half, the half of the baryons enclosed.
- The rule adds G f_ex (1 − f_b) M_NFW(<r) / r² to the law's g.
- Collapse mass: the Moster+2013 relation of CFG35, at M_* = 2 L_V.
- **The trap, declared:** that function is clamped at M_halo = 10⁹ M☉ below M_* ≈ 1.6 × 10⁴, so all ultra-faints with less than that get 10⁹. It is an extrapolation, not a measurement. The sensitivity is scanned: every satellite with M_* < 10⁵ set to 10⁸ to 10¹⁰ (R1).
- Samples: FG001's MW ultra-faints (31 resolved, plus the 9 upper limits by Kaplan–Meier, as CFG28), MW classical dSphs (14), M31 Collins+13 (14) and M31 LVD (34). The classical satellites carry their infall gas (CFG18's set, as an expectation).
- **H1 (headline):** the rule closes the ultra-faint failure (KM median within 2σ, both footings). **H2:** it does not over-predict the classical satellites (median not below −2σ). **H3:** it bites (f_ex > 0.5 in at least 80% of the ultra-faints). **H4:** it leaves SPARC dwarfs alone.

## Results

**Controls.** C1: FG001's committed isolated medians are reproduced (1e-16). C2: f_ex = 0 reproduces FG001's prediction and the NFW piece is monotone. C2 first failed on a bug of mine: its override only reached satellites below M_* = 10⁵. I fixed the override, not the tolerance, before interpreting anything.

| population | law | rule | verdict |
|---|---|---|---|
| MW ultra-faints (KM, limits in) | +0.325 (3.77σ) / +0.304 (3.55σ) | **−0.059 ± 0.143 (−0.41σ)** both footings | **H1 passed** |
| MW classical dSphs | +0.027 / +0.008 | **−0.118 (−1.78σ)** / −0.123 (−1.90σ) | over-predicted |
| M31 Collins+13 | +0.064 / +0.045 | −0.024 (−0.22σ) / −0.016 | fine |
| M31 LVD | +0.044 / +0.031 | **−0.107 (−2.67σ)** / −0.109 (−2.66σ) | **H2 failed** |
| SPARC dwarfs (110, log M_* < 10) | | f_ex = 0 in all 110; no change | **H4 passed** |

- **H3 passed:** f_ex > 0.5 in 100% of the ultra-faints (median 0.96): the collapse debris carries nearly all of the halo, because the law's own phantom at such a small baryon mass is 10⁷ M☉ against a collapse mass of 10⁹.
- **The floor on the ultra-faint result** is 0.133 dex, and it is the collapse-mass floor. The KM median is +0.279 at 3 × 10⁷, +0.052 at 2 × 10⁸, −0.059 at 10⁹ and −0.142 at 6 × 10⁹, and it crosses zero near **3 × 10⁸**. The ultra-faints want halos of about 3 × 10⁸ M☉, three times below the clamped value. I have not checked that against a specific abundance-matching relation; it is not a measurement.
- **Why SPARC dwarfs are safe and the classical satellites are not:** SPARC dwarfs are gas-rich, so the law's phantom already exceeds their collapse mass (f_ex = 0). The classical satellites are gas-poor and have lost their gas, so the phantom is small and the debris carries about half the halo (median f_ex 0.5–0.6).

## Independent referee (2026-09-28)

Reproduced: KM median +0.325 / +0.304, resolved-only +0.355 / +0.334, 31 + 9 limits, and the Moster and NFW helpers against textbook formulas (NFW to 1.5e-4). The clamp covers 33 of the 40 ultra-faints; unclamped Moster gives 1.9e8–2.2e9 (median 6.9e8), and interpolating R1 gives about −0.03, so the ultra-faint result does not depend on the clamp (the referee's interpolation, not a re-run). **The ultra-faint "closure" is a weak test:** every collapse mass from 2 × 10⁸ to 10¹² passes the 2σ criterion (the offset runs +0.05 to −0.35), only masses below about 3 × 10⁷ fail, and the σ falls from 3.8 to −0.4 partly because the error grows from 0.086 to 0.143. Seven of the 40 have host = LMC in the source table (harmless for the isolated law).

## Standing

**B's derived rule closes B's largest failure and trades it for a smaller one in σ (1.8–2.7σ), spread over more objects.** The ultra-faints move from +0.325 dex (3.8σ) to −0.06 dex (−0.4σ), which is what a cusp does. But the rule puts a full NFW debris into the classical dwarfs, and it over-predicts them by about 0.11–0.12 dex: −2.7σ for the M31 LVD, −1.8 to −1.9σ for the MW classicals, and nothing for Collins+13. This is the cusp problem, which ΛCDM has as well, now reached from B's side.

**A design constraint, not a fix.** The debris must switch off where the phantom already supplies the observed mass (classical satellites, gas-rich dwarfs) and stay on where it does not (ultra-faints). This is the same structural point as the max rule of T5, which says dark mass is the larger of the phantom and the cold budget, not their sum. The rule as derived in CFG35 is a sum. I have not tried a form that fixes this, because any such form would be a fitted rule.

**Caveats.** The ultra-faint collapse mass is extrapolated, though weakly constrained by the cusp property. The M31 LVD −2.7σ has a small error (0.040). Its collapse-mass floor covers only the satellites with M_* < 10⁵; the scatter of the Moster relation for the rest is not propagated (a weak effect, by the M_halo^0.13 scaling, but not measured here). The stellar-mass systematic enters only through Υ_V.

Nothing here says the theory is closed.

**Kernel note (CFG64).** This lane's estimator uses the exponential RAR kernel (`hunt_lib.nu_s`, ν = 1/(1 − e^{−√y})), not ν_mono as the text above says; the two agree to 3 × 10⁻⁹ for y ≤ 0.1. Swapping the kernel to P2 leaves the headline verdict unchanged (see `CFG64_kernel_robustness/README.md`).
