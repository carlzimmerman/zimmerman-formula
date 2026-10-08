# CFG496: is there a clue linking cold energy and dark energy? NONE FOUND (0 of 15 candidates)

**Terms (owner, 2026-10-08).** COLD ENERGY is the framework's cold, clumping component (it used to be called the "cold
fluid"). It is pressureless. Its cosmic amount, R = Ω_c/Ω_b = 5.364, is an input. Its mass is still required, and there is no
particle. DARK ENERGY is the vacuum component ρ_Λ. The framework ties dark energy to galaxies through a₀ = κc√(Gρ_Λ), with
κ = ½ FITTED.

**Files and runs.**
- The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in c05c824e4.
- The script is `cfg496_hunt.py` and runs in about 10 s. It uses on-disk data and committed results only; nothing was downloaded.
- Main run: exit 0, because controls K1–K4 pass.
- `CFG496_MUTATE=1` runs the scrambled cosmology, 200 draws in about 8 s.
- `cfg496_postfreeze.py` is a set of labelled post-freeze checks with no verdict weight.

Both footings are scored separately and never pooled. This is not "theory closed".

## Bottom line

**No clue was found.**
- 15 candidates were declared in advance.
- 6 are **BUILT-IN**: they follow from the law, the edge definition, or how the inputs are defined.
- 3 are **COINCIDENCE**: a 1% number match that fails the look-elsewhere control and the second-epoch check.
- 6 are **NO MATCH**.

The scrambled cosmology (Ω_c/Ω_b drawn at random from [3, 8]) yields 0.005 false "clues" per draw. That comes from 1 draw in
200, and it exposes a hole in the second-epoch rule (see below). A 1% number "match" turns up in about 75% of scrambled draws,
for the real cosmology and the fake ones alike.

The structural reason is C07, a Buckingham argument. At the scale of a single galaxy, the only edge quantities that do not
depend on the galaxy's mass are the edge field, the surface density and the pressure. All three reach dark energy only
through a₀. So, within the record's model, **every mass-independent link between cold energy and dark energy is the law
itself**. A genuinely new link would need a new scale or new dynamics; reshuffling the existing ones cannot produce it.

## Candidate table

Notation: R = 5.364, s = ln(1 + 1/R) = 0.1709, y_e = s² = 0.0292, r_edge = r_M/s.

| ID | candidate | result | label |
|---|---|---|---|
| C01 | inside r_edge, total/baryon = 1 + R (the cosmic mix) | holds identically for symbolic R (sympy); r_edge is *defined* as the radius where the phantom has used up R·M_b | BUILT-IN |
| C02 | σ⁴ = G M_b a₀/4 from the share inside the edge | exact in the deep limit for any R; the exact kernel gives a factor ((1+R)s)² = 1.18 (+0.073 dex, = CFG461 R0) | BUILT-IN |
| C03 | edge field g_e/a₀ = 0.186 equals a simple dark-energy number | best of 1,053 forms: κ/(4πΩ_ΛΩ_m) = 0.1848 (0.6%); look-elsewhere p = 0.62; fails at z = 1 (0.236). The deep limit is g_e → f_b a₀, so the value is set by the law | COINCIDENCE |
| C04 | edge density is a fixed multiple of ρ_Λ | slope −0.50 in M_b. The mean density inside r_edge equals 200 ρ_crit only at log M_b ≈ 13.4–13.7 | NO MATCH |
| C05 | edge dynamical time is a fixed multiple of 1/√(Gρ_Λ) | slope +0.25; it equals 1/√(Gρ_Λ) only at log M_b ≈ 19.6 | NO MATCH |
| C06 | r_edge is a fixed multiple of the Λ zero-velocity radius | slope +0.167; ratio 0.016 / 0.075 / 0.35 at 10⁷ / 10¹¹ / 10¹⁵ M☉ | NO MATCH |
| C07 | a mass-independent edge–ρ_Λ relation not set by a₀ | one Π group, G³M_b²ρ_Λ/c⁶. The mass-free edge quantities are g_e, Σ_e and P_e, and all three depend on c and ρ_Λ only through a₀ | BUILT-IN |
| C08 | zero-knob PM: q_max = 0.302 ≈ Ω_m | 3.8% off Ω_m, so no 1% match to Ω_m itself; the best form 3Ω_m/π (0.8%) has p = 0.77. It moves to 0.526 at 512³ (CFG460) | COINCIDENCE |
| C09 | the PM's settled cold energy shows an a₀ regularity | the code computes the supply as f_ret f_b M_ta and the edge from r_M = √(GM_b/a₀): the regularity is put in by construction | BUILT-IN |
| C10 | the framework predicts "why now" | identity a₀/(cH(z)) = κ√(3Ω_Λ(z)/8π). Every framework epoch marker is just a threshold on Ω_Λ(z), and R and ρ_Λ are both inputs | BUILT-IN (input) |
| C11 | Ω_c/Ω_Λ = 0.385 equals a simple number | best of 325 forms is πκ²/2 (1.9%), no match; p = 0.56 | NO MATCH |
| C12 | R = 5.364 equals a simple dark-energy number | best form 4πΩ_ΛΩ_m/κ = 5.41 (0.9%); p = 0.73; fails at z = 1 | COINCIDENCE |
| C13 | X-COP clusters reach the cosmic mix at the galaxy edge field y_e | b = 0: median y_mix sits **+0.49 dex** (canonical) / +0.41 dex (alt) above y_e, a robust miss (P1). b = 0.3: 10 of 12 clusters never reach the mix within the measured radii | NO MATCH |
| C14 | SPARC shows the edge feature at y_e | Δ = +0.013 ± 0.038 (canonical) and −0.014 ± 0.039 (alt), against the cap's prediction of −0.077 / −0.085. No feature; the cap is disfavoured at about 2.4σ / 1.8σ (171 / 248 points beyond the edge) | NO MATCH |
| C15 | SPARC residuals correlate with log(R_last/r_edge) or log(Σ_eff/Σ_M) | ρ = +0.04 / +0.16 (canonical) and +0.01 / +0.20 (alt); look-elsewhere p = 0.080 / 0.025. These correlations do not change with R, so they cannot carry the amount | NO MATCH |

The surviving CLUE is: **none**. The second-scale check therefore has nothing to check. The one that was set up, C14
backed by C13, fails at both scales.

## Scrambled cosmology (MUTATE): the false-positive rate

Set-up: 200 draws of R′ uniform in [3, 8], with Ω_b fixed, a flat universe, and the a₀ footings held.

**Clues found:**
- 0.005 CLUE labels per draw; 1 draw in 200 has a "clue".
- That draw is C12 at R′ = 4.364, which matches 4/(3πκΩ_ΛΩ_m) to 2e-5 with p = 0.003. It passed the frozen z = 1 check
  (1.6%).
- Post-freeze check P3 shows why. Ω_ΛΩ_m is symmetric about the epoch where ρ_m = ρ_Λ (z ≈ 0.41 for that R′), so z = 1
  nearly mirrors z = 0. The same form fails at z = 0.5, 2 and 3.
- **Hole disclosed:** a single-epoch second check is blind to forms built from the product Ω_ΛΩ_m. Future hunts should check
  two epochs.

**Coincidences.** 1% "matches" that fail the controls turn up in 150 / 150 / 74 / 146 of 200 draws for C03 / C08 / C11 /
C12. So the real cosmology's three COINCIDENCE labels are exactly the base rate.

**C13 matches.** X-COP "matches" occur in 23 of 200 draws, all with R′ = 3.9–4.4. All 23 rest on censored clusters
(post-freeze P2): when 1 + R′ is small, most clusters never fall to the mix inside the measured radius. So they are upper
limits, not crossings. The frozen rule treated censored values at face value, and that is a weakness of the rule. It does
not affect the real-R verdict, because the b = 0 cells miss even at the censoring lower bound.

**C14 matches:** 0 of 200 draws.

## What this says, plainly

- **The edge relation is BUILT-IN.** "Inside the edge the galaxy has the cosmic mix" and "the edge field is 0.186 a₀ ≈ f_b a₀"
  are the definition of the edge plus the law. They link cold energy to dark energy only because a₀ is already defined
  from ρ_Λ.
- **Nothing in the edge is scale-free against ρ_Λ.** The record's model has no mass-independent density, time or length
  relation to ρ_Λ (C04–C07). Dark energy enters galaxies only as the acceleration a₀.
- **The framework does not explain "why now."** Ω_c/Ω_Λ today is an input, through R and ρ_Λ. The "MOND coincidence"
  a₀ ≈ cH₀/6 is the cosmic coincidence written through the fitted κ (the same circularity as L258).
- **The data show no hidden regularity at the dark-energy-set edge field.**
  - Clusters reach the cosmic mix about 0.4–0.5 dex above the galaxy edge field (b = 0). The cell with hydrostatic bias
    b = 0.3 is undetermined.
  - SPARC shows no break at y_e. If anything it disfavours the boost cap at about 2σ, consistent with CFG487's alt-dwarf
    failure.

## Controls

- K1 PASS: the sympy identities hold, and the wrong identity (1 + R → R) fails.
- K2 PASS: the planted form 3πκΩ_m is recovered exactly, with p = 0.
- K3 PASS: the X-COP loader reproduces CFG432's data identity.
- K4 PASS: the SPARC ν_mono median residual is +0.021 dex (canonical) / −0.005 dex (alt).

## Disclosures and caveats

- **Ω_m value.** The criteria text quotes Ω_m = 0.3147. The stated Planck inputs (h, ω_b, ω_c, no neutrinos) give 0.3138,
  and the script uses 0.3138. This moves no label.
- **X-COP stellar mass.** It uses the CFG432 convention (the cluster's own M★ file, else the median M★/M_gas). It is
  extended to 0.05 R500 – the last measured gas radius, with M★/M_gas held at the file's end values. The hydrostatic masses
  are X-COP's forward models.
- **SPARC baryons.** Fixed Υ★ (0.5 for the disc, 0.7 for the bulge). There is no M/L marginalisation.
- **C08 second check.** It uses the committed 512³ seed-360 q_max (0.526). CFG460's README quotes 0.49 for seed 359.
- **Post-freeze checks.** P1–P3 carry no verdict weight.
- **Not re-chased.** SCAN_cosmic_supply_coincidence_2026-10-07, the 32π lanes, CFG380 and L258.
- **Not included.** KiDS (the edge already FAILED there in CFG487/413), MeerKAT (no per-radius curves) and satellites.

κ = ½ is FITTED. The cold energy's mass is still required and its amount is an input. This is not "theory closed".
