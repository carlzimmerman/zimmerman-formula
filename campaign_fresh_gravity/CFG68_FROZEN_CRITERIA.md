# CFG68 — the ΛCDM control for CFG40/CFG56 (the super spirals): FROZEN CRITERIA

Written 2026-09-29 (UTC), **before any CFG68 script exists and before any ΛCDM prediction for these galaxies has been computed**. This file is committed on its own. Any later deviation goes in the README as a disclosed departure. It follows the repo's control pattern (CFG23, CFG25, CFG67): standard halos run through exactly the same machinery.

**Known before freezing:**
- **CFG56's committed numbers for B.** These are the law's numbers; the rule adds nothing, with f_ex = 0 in all 23.
  - Canonical: all 23 at **+0.105 ± 0.063 (1.67σ)**; the nine fastest at **+0.164 (2.34σ)**; the slope against log M_b at +0.166 ± 0.092 (1.80σ).
  - Alt: +0.090 (1.46σ) for all 23 and +0.149 (2.17σ) for the nine fastest.
  - CFG40's all-disc numbers and its referee's structure-model spread are also known.
- **The data tables.** They include the paper's per-galaxy NFW dark mass inside r (`logMdark`, 10^11.4–10^12.5 M☉), which is a fit to the same speeds.
- **The top of the blue relation in the Mandelbaum+2016 table.** ⟨M_200m⟩ is 10^12.79 h⁻¹ M☉ at both log M_* = 11.47 and 11.68. Its errors there are +0.43/−1.01 and +0.58/−2.23 dex, so the relation is flat and poorly measured.
- **CFG67's result:** ΛCDM passed its KiDS control.
- **CFG69** (a ΛCDM comparator over other populations) was committed while this file was being written.
  - A string search printed only match counts (0 for the paper, its galaxy catalogues, the bulge table, `vmax`, "super", CFG40 and CFG56). It confirmed that CFG69 does not score these galaxies. None of its numbers were read.
  - Its commit message, which was seen, reports that its halo-mass MUTATE had no bite.
- **A hand estimate.** While the control was being chosen, one galaxy's baryons-only speed was estimated roughly by hand. That is not the ΛCDM comparator, and nothing below depends on it: the thresholds are CFG56's, and the MUTATE fails by construction.

## Question

**Does standard ΛCDM (CFG56's baryons plus an NFW halo from a measured stellar-to-halo relation, nothing tuned) reproduce the super spirals' speeds, and the nine fastest in particular, through the same machinery? That is: is CFG40/56's marginal failure specific to the law, or generic?**

## Identical to CFG56 (executed read-only)

- **Machinery:** CFG56's source up to its scoring loop (`RES = {}`), executed with its own MUTATE off and its output suppressed, as CFG40/56 execute CFG36.
  - CFG56's own controls re-run there and must pass: the table, the bulge–disc table match, B/T = 0 reproducing CFG40, and the Freeman field.
- **Galaxies:** the 23 rows of `real_research/data/ogle2019_super_spirals.tsv`, with B/T_r and R_e,bulge from `real_research/data/simard2011_ogle_bulge_disc.tsv`.
  - v_obs = `vmax` at r = `r_kpc`, the radius of the measured maximum (not the model's own maximum).
  - 2MFGC 10372's gas mass and SFR are upper limits. They are used at their bound values, as in CFG40/56.
- **Baryons:** CFG56's `gN_bd`, the in-plane field at r of two components:
  - a Hernquist bulge of mass (B/T_r) M_*, with a = R_e / 1.8153;
  - a Freeman exponential disc holding (1 − B/T_r) M_* + M_gas, with scale R_d.
- **Statistic and error model:** CFG56's own `stat()` and `floor()`, unmodified.
  - ΛCDM enters only as new branches of the `pred()` hook those functions call.
  - The law's branches are left untouched.

## The ΛCDM comparator (no free or tuned parameter)

**v²(r) = r [ g_N,bar(r) + G M_dark(<r) / r² ]**, with **M_dark(<r) = (1 − M_b / M_200c) · M_NFW(<r; M_200c)**, clipped at zero.

The enclosed-mass shorthand G [M_bar(<r) + M_NFW(<r)] / r is made exact here: the baryons enter through CFG56's in-plane field, and the halo is spherical.

- **HEADLINE: M_200c = CFG36's `collapse(M_*, 'blue')`.**
  - This is Mandelbaum+2016's weak-lensing ⟨M_200m⟩ for blue centrals (`logMs_eff`, Chabrier IMF, h = 0.673). It is interpolated in log M_* and clamped at the table's ends, then converted to M_200c on the same NFW (Ω_m = 0.315, H₀ = 67.4).
  - All 23 galaxies are blue: sSFR > 10⁻¹¹ yr⁻¹ (CFG40's C1).
  - Two galaxies (2MFGC 12344 and OGC 0139, both log M_* = 11.74) lie above the top bin (11.68) and take its value.
- **Profile:** CFG36's `nfw_enclosed` (h48's committed function, via CFG35), with the Dutton–Macciò c_200c(M) at z = 0 and h = 0.674.
- **Baryons in the halo:** the lensing M_200c is taken as the total mass.
  - The galaxy's own baryons (M_b = M_* + M_gas) are removed from the NFW and counted once, in their observed disc and bulge.
  - Everything else (dark matter and any halo gas) keeps the NFW profile.
  - The model's total mass inside R_200c is then the measured M_200c.
  - *Why:* of the three standard bookkeepings, this is the only one that keeps the measured total. The other two are reported brackets (R4):
    - The full M_200c NFW (CFG67's accounting) counts the galaxy's baryons twice, unless the lensing fit carried the stars separately.
    - (1 − f_b) M_200c assumes a baryon-complete halo. It equals B's rule's debris term at f_ex = 1.
- **Stellar masses:** M_* = 10^`logMstars` as tabulated (WISE W1, constant M/L_W1 = 0.6). The same value is used for the baryons and for the halo lookup.
  - These masses stand in for the lensing table's Chabrier masses and for the Chabrier/Kroupa-like masses behind the Moster+13 relation. CFG40/56 declared the same; it is not verified here.
  - Any mismatch is what the ±0.2-dex M_* floor term carries. That shift moves the baryons and the halo lookup together, as CFG56's `pred` does for the rule.
- **ΛCDM has no a₀.** There is one set of numbers, not two footings.
- **Nothing is fitted to the speeds.** `logMdark` is never an input.
- **Declared simplifications:**
  - The halo is pure NFW. Adiabatic contraction (which raises v_pred) and feedback cores (which lower it) are not scored.
  - The halo relations are at z = 0, as in the machinery. The galaxies are at z = 0.06–0.28 (median 0.14).
  - The mean relation is used, with no scatter drawn.
- **Reported variant R1: Moster+13, colour-blind.** M_200c = CFG35's `halo_mass(M_*)`: h48's inversion of the z = 0 relation, which the machinery treats as M_200c. The NFW and the bookkeeping are the same as the headline's.

## Statistic (CFG56's, as coded)

- **Per galaxy:** off = log₁₀(v_obs / v_pred) at r. A positive offset means the model is too slow.
- **All 23:**
  - The mean, with the galaxy-to-galaxy error err = s / √23 (s is the ddof = 1 standard deviation).
  - Three floor terms, each half the shift of the all-23 mean across its variations:
    - mod: B/T_r shifted by −0.10, 0 and +0.10, clipped to [0, 1] (half the range);
    - ms: M_* × 10^±0.2;
    - mg: M_gas × 10^±0.3.
  - σ = √(err² + mod² + ms² + mg²), and z = mean / σ.
- **The nine fastest** (v_obs > 340 km/s):
  - The galaxies: OGC 0441, OGC 0926, 2MFGC 08638, 2MASX J11232039+0018029, OGC 1312, 2MFGC 12344, OGC 1304, 2MASX J16184003+0034367 and OGC 0139.
  - mean₉, with err₉ = s₉ / 3.
  - σ₉ = √(err₉² + mod² + ms² + mg²), **with the all-23 floor terms, as CFG56 codes it**.
  - z₉ = mean₉ / σ₉.
- **Trend:** the OLS slope of off against log₁₀ M_b (centred). Its standard error comes from the residuals (n − 2), and zs = slope / se, with no floor.

## Pre-declared checks

- **C1 CONTROL:** CFG56's own controls pass in the executed slice.
  - Before any mutation, the executed `stat()` and `floor()` reproduce CFG56's committed law numbers (`CFG56_super_spirals_bulge_results.json`, RES) to 1e-6.
  - Canonical: mean +0.104625, σ 0.062785, mean₉ +0.163638, z₉ 2.3407.
  - Alt: mean +0.090247, mean₉ +0.148809.
- **C2 CONTROL:** the executed `collapse` reproduces CFG36's committed red-relation M_200c for its seven X-ray ellipticals to 1e-6 relative.
  - The committed values are in `CFG36_colour_split_collapse_results.json`, RES canonical `Mh`; NGC 720's is 2.7895e12 M☉.
  - CFG36's 200m → 200c identity also holds to 1e-6.
- **C3 CONTROL:**
  - `nfw_enclosed(M, R_200c) = M` to 1e-9 at M = 10¹² and 10¹³ M☉, with R_200c from the machinery's ρ_c.
  - The Moster inversion round-trips, `moster_mstar(log halo_mass(M_*)) = M_*`, to 1e-3 at log M_* = 11.2, 11.5 and 11.7.
- **H1 [HEADLINE; MUTATE must fail]:** ΛCDM with the blue relation fits the nine fastest: |z₉| < 2.
- **H2:** ΛCDM fits all 23: |z| < 2.
- **Reported rows.** They never change H1 or H2. R5 can only downgrade a pass, as the reading declares.
  - **R1:** the Moster variant, with every statistic.
  - **R2:** the per-galaxy table:
    - log M_b; r and r/R_d; v_obs;
    - v_law (CFG56) and v_ΛCDM, with both offsets;
    - M_200c, flagged when clamped;
    - the halo's share of v² at r;
    - `logMdark` beside the comparator's M_dark(<r), as a diagnostic.
  - **R3:** the law's committed canonical and alt numbers beside ΛCDM's (the mean, the slope and the nine fastest, each with its z). Also CFG56's full three-clause H2 (mean, slope and nine fastest, each under 2σ) evaluated on ΛCDM.
  - **R4:** the halo brackets:
    - every blue M_200c at +1σ, from `collapse(sig = +1)`, which uses the table's `ep`;
    - every blue M_200c at −1σ, from the table's `em` read from the same rows (CFG36's `collapse` applies `ep` to both signs);
    - the full-M_200c halo;
    - the (1 − f_b) M_200c halo, with f_b = 0.1571 (the machinery's FB).
  - **R5 (leverage):** the halo switched off, leaving Newtonian baryons only.
  - **R6:** z₉ with its floor terms recomputed as shifts of the nine-fastest mean, for ΛCDM and for the law.
- **MUTATE:** every observed speed is multiplied by 0.25. The factor is applied through CFG56's `VF` convention, so the same nine galaxies are selected.
  - Every offset then shifts by exactly log₁₀ 0.25 = −0.602 dex, and every σ term is unchanged. H1 must fail, and the script must exit 1.
  - The failure is guaranteed unless the main run's mean₉ lies within 2σ₉ of +0.602.
  - In particular, it is guaranteed whenever the main H1 passes with σ₉ ≤ 0.150 dex. That is more than twice the law's committed σ₉ of 0.070.
  - *Why not a halo-mass factor:* at 14–54 kpc the NFW enclosed mass responds sub-linearly to M_200c, so no halo factor can be shown before the run to force a failure. CFG69's halo-mass MUTATE had no bite. The halo factor 0 is reported as R5 instead.
- **Outputs:** the script is written after this file is committed. Like CFG56's, it writes `.out` and `_results.json`, plus the `_MUTATE` pair.

## Reading (declared)

- **H1 PASS:** the super-spiral miss is **specific to the law**. Through the same galaxies, baryons, radii and error model, standard ΛCDM with measured halo masses reproduces the nine fastest, where the law sits at +0.164 (2.34σ). CFG40/56's fail then stands as a law-specific tension, and it is still marginal. There are two exceptions:
  - If R5 (no halo) also has |z₉| < 2, the pass is instead **non-diagnostic**: the statistic cannot tell the measured halo from no halo.
  - If mean₉ is positive and within σ₉ of +0.164, the standing line says that both models lean the same way and only the law crosses 2σ.
- **H1 FAIL with mean₉ > 0:** the miss is **generic**. ΛCDM with a measured halo also under-predicts the fastest super spirals, so CFG40/56's fail does not single out the law.
  - The suspects are the shared inputs (the W1 stellar masses, the inclinations, the maxima of noisy Hα curves, the gas without HI) or physics that both models lack.
  - R3 gives the sizes.
- **H1 FAIL with mean₉ < 0:** ΛCDM **over-predicts** where the law under-predicts. The data lie between the two models, so the miss is not generic. R3 says which model misses by less.
- **H2 PASS:** both models fit the sample as a whole; the law does so at 1.67σ.
- **H2 FAIL:** ΛCDM misses the whole sample where the law does not. The sign of the mean says in which direction.
- **R1 and R4:** if any of them gives the opposite H1 verdict, the standing line says the verdict depends on that choice: the halo relation, the lensing error at these masses, or the bookkeeping. The declared verdict does not change.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
