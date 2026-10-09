# Referee report: Melchiorri & Ruchika, arXiv:2608.10189 (v2, 2026-09-12)

**"The Rotation Curve of the Milky Way: State of the Art, the Keplerian Decline Debate, and Implications for Dark Matter"** (submitted to New Astronomy Reviews). This is the paper behind the 2026-10-09 video "Plot Twist: New Milky Way Data Incompatible With Dark Matter AND Modified Gravity".

Read from the arXiv LaTeX source. Section and equation numbers refer to that source.

## 1. What the paper claims
- Several Gaia DR3 analyses find the Milky Way's circular speed falls beyond R ≈ 15 kpc:
  - Wang+23 and Ou+24 to about 27 kpc;
  - Jiao+23 reanalyses both: slope −2.2 km/s/kpc, and a power law v ∝ R^γ beyond 19 kpc gives γ = −0.47 ± 0.15 (Keplerian is −0.5; flat is excluded at 3σ).
- Read as spherical, M_tot ≈ v²R/G = 2.0 × 10¹¹ M☉ at 19 kpc. That is 3–5× below streams (Orphan-Chenab M(<50) = 3.8 × 10¹¹), globular clusters, satellites and the Local Group timing (0.7–1.6 × 10¹² M☉).
- **MOND:** "predicts an asymptotically flat RC", so a confirmed Keplerian tail "would be difficult to accommodate" (§MOND). Coquery+25: freeing the baryons drives the fitted a₀ toward zero.
- **The paper's own verdict:** the Keplerian reading is "plausible but systematically challenged". Its Scenario 2 (a genuine but exaggerated decline, M_vir 5–8 × 10¹¹) is called plausible. Gaia DR4 (2 Dec 2026) and spherical or oblate Jeans modelling are needed.

**The headline is stronger than the paper.** "Incompatible with dark matter AND modified gravity" applies only to the strict Keplerian reading, which the authors themselves do not adopt.

## 2. Assumptions, listed and graded
Bias direction: **↓** means the assumption could make the measured curve fall more steeply than the true one.

| # | assumption | where it enters | bias | graded |
|---|---|---|---|---|
| A1 | Steady state (∂/∂t = 0) | radial Jeans eq. (eq. jeans_R) | ↓ or ↑ | Sgr bending waves and the LMC wake give 10–20 km/s non-circular motion at 20 kpc. That is the same size as the claimed decline (~30 km/s). **Serious.** |
| A2 | Axisymmetry and planarity | eq. jeans_R | ↓ or ↑ | The disc warps beyond 12 kpc and the tracers flare. Violated where the decline is measured. **Serious.** |
| A3 | Spectrophotometric distance scale | every v_φ | ±linear | 5% in distance gives about 10 km/s. Jiao+23 drops Zhou+23 for having longer distances, which the review itself calls "a genuine, unresolved spread". **Serious**, and it is a choice, not a measurement. |
| A4 | Tracer density ν(R) and its log-slope (−2 to −3) | asymmetric drift and pressure term, together | ↓ | Koop+24: a radially truncated tracer can fake a steep decline under a flat true curve. FIRE-2 (Ou+24b) finds pipeline biases of 10–40 km/s at 20–25 kpc. **Largest single systematic.** |
| A5 | κ² = σ_φ²/σ_R² from the epicyclic flat-curve value 0.5 | asymmetric drift | ↑ (self-referential) | The paper notes this circularity itself (§ epicyclic). Small (1–4 km/s). |
| A6 | Tilt term σ_Rz² neglected (Ou+24) | eq. va2_full | ? | It grows with \|z\|, and the outer tracers flare. Unquantified. |
| A7 | Spherical-equivalent mass M = v²R/G for a flattened system | the "2 × 10¹¹ M☉" | ↓ | The text says this is not an exact enclosed mass (eq. vc_spherical_mass), yet the headline mass uses it. **Moderate.** |
| A8 | "Keplerian" read off a power law fitted over 19–27 kpc | γ = −0.47 ± 0.15 | ↓ | A finite exponential disc in the transition to low acceleration also gives γ < 0 there, so the slope alone cannot show the mass is all enclosed. **Serious for the interpretation.** |
| A9 | Diagonal covariance; 35 compiled points treated as data | MCMC/GP; Jiao's 3σ | ↓ (overconfident) | Oman+24: correlated residuals over 1.5–2.5 kpc. The paper's own fit has χ²/ν = 0.47. The 3σ against flat is not recalibrated. |
| A10 | Heterogeneous R₀ (8.12–8.34) rescaled to 8.178 | compilation | ±0.2 kpc | Minor. |
| A11 | Phenomenological V = A + B/(1+(R/C)^n) | MCMC | built in | Monotonic with a constant asymptote by construction. It cannot test "Keplerian vs flat". The authors admit this. |
| A12 | MOND tested as "asymptotically flat", with a point-mass g_bar at 20 kpc and generic μ, a₀ = 1.2e-10 | §MOND | ↓ for MOND | No MOND rotation curve is computed for a real bulge plus disc plus gas. The flat-curve statement is only the deep-MOND limit. **The key weakness for any modified-gravity verdict** (§3). |
| A13 | Outer-halo masses (streams, GCs, satellites, timing) taken as model-free | §indep, Table mass_comp | — | Every one assumes Newtonian gravity plus a halo family (NFW, Einasto, power law) and equilibrium at r ≳ 100 kpc, where the paper itself says equilibrium is "far more doubtful". The "tension" is between two Newtonian-halo inferences. It is not model-independent. **ΛCDM-shaped.** |
| A14 | Baryons 0.6–1.0 × 10¹¹ M☉ (Bland-Hawthorn & Gerhard 2016) | MOND and RAR placement | both | The MOND/RAR verdict swings across this range (§3). |
| A15 | External field effect (EFE) as MOND's escape | §MOND caveat 2 | — | Not computed. **Under this programme's framework there is no EFE** (CFG447, CFG478), so for us the decline must come from the baryons alone. |
| A16 | Sylos Labini & Capuzzo 2026 dark-disc preference (8.5–14 kpc) | §3D geometry | — | A phenomenological closure. The data vector a_z depends on the model, the tilt term is dropped, and only two geometries are compared. The review says so. |

## 3. How it actually works: the framework's reading
Law: a₀ = κc√(Gρ_DE), κ = ½ **fitted**. Kernel ν(y) = 1/(1−e^(−√y)), which is exactly the paper's RAR equation (eq. rar) with g† → a₀. Footings 9.36 × 10⁻¹¹ and 1.13 × 10⁻¹⁰ m s⁻², never pooled. No EFE. The cold energy's mass is still required.

1. **The paper's own RAR check passes.** At 20 kpc the paper finds the RAR speed is 194–227 km/s for its baryon range, bracketing the 207–212 km/s Gaia values (§RAR). Its MOND "tension" comes from the asymptotic flat-curve argument, not from a computed curve.
2. **The computed curve, CFG513** (committed; nothing fitted except the declared baryon variants), against Ou+24's 37 points, 6–27 kpc:
   - M_b = 7.3 × 10¹⁰: χ² = 44 (canonical) / 12 (alt). Alt fits well and canonical acceptably.
   - M_b = 6.0 × 10¹⁰: χ² = 306 / 150, running 7–10% low.
   - The decline comes from the baryons. The curve passes from the baryon-dominated inner disc into the transition regime, and the law's extra gravity grows too slowly to keep it flat until the deep regime. Nothing is truncated: the cold-energy census edge for the Milky Way is ~500 kpc.
3. **The framework's asymptote** (deep limit, v⁴ = GM_b a₀):

   | M_b | canonical | alt |
   |---|---|---|
   | 6.0 × 10¹⁰ | 165 km/s | 173 km/s |
   | 7.3 × 10¹⁰ | 174 km/s | 182 km/s |
   | 1.0 × 10¹¹ | 188 km/s | 197 km/s |

   The paper's own phenomenological asymptote is A = 193.6 (+3.5/−4.2) km/s. **The framework does not predict a Keplerian fall. It predicts a mild decline from about 230 to about 175–195 km/s, then a flat curve.** That is the paper's Scenario 2 shape, and it needs no dark-matter halo.
4. **The "tension" with outer tracers mostly goes away.** With a flat 169–177 km/s (CFG513's V_c,sph at 100 kpc), the spherical-equivalent dynamical masses are M(<50 kpc) = 3.3–3.6 × 10¹¹ (Orphan-Chenab 3.77 +0.26/−0.19) and M(<100 kpc) = 6.6–7.3 × 10¹¹ (Sagittarius 5.6 ± 0.4, halo-family dependent). These are rough spherical estimates, not a fit. The disc curve and the stream masses are consistent in one picture without a halo. They clash only in a Newtonian model forced to make both with one halo profile.
5. **The real catch:** a good inner fit needs M_b ≈ 7.3–8.2 × 10¹⁰. McMillan's census gives 5.43 ± 0.57 × 10¹⁰ for stars, about 3σ lower. CFG513 marks this as marginal. Coquery+25's result (a₀ → 0 when the baryons are free) is a fair warning that the MOND-class fit trades a₀ against disc mass. That is the open question for us, and CFG532 tests it with the baryons held at the census value.
6. **What would falsify the framework here:** a confirmed Keplerian tail (γ ≈ −0.5) out to ≳ 40 kpc in Gaia DR4 with model-independent distances. That would contradict the flat asymptote at fixed census baryons. A mild decline that flattens at about 175–195 km/s is what the framework predicts.

## 4. Referee requests to the authors
1. Compute a MOND/RAR rotation curve for the same three-component baryon model used for the NFW fits, across the stated baryon range, and fit it to Ou+24 and Jiao+23. Report χ² next to the NFW and Einasto fits. The asymptotic flat-curve argument is not a test at 15–27 kpc.
2. State that every outer-halo mass in Table mass_comp assumes Newtonian gravity plus a halo family. In MOND-class gravity the same tracer data give a different enclosed-mass profile. The "tension" in the Keplerian reading is model-conditional.
3. Recompute the significance against flat (γ = 0) with a full covariance (Oman+24), including the distance-scale spread (keep Zhou+23 as a systematic variant), and report it beside the 3σ.
4. Show the Koop+24 truncated-tracer test on the Ou+24 selection function. It is the most direct way the steep tail could be an artefact.
5. Replace "M_tot ≈ 2 × 10¹¹" with a flattened-model mass or bound. The spherical-equivalent mass of a declining disc curve is not the total mass.
6. Correct the RAR equation's attribution and scale. It is the McGaugh+16 form, with g† = 1.2 × 10⁻¹⁰ m s⁻² fitted to SPARC. A different a₀ (0.94–1.13 × 10⁻¹⁰) shifts the asymptote by about 5%.

**Recommendation:** minor revision for a review. It is careful and self-critical. Its MOND section needs one computed curve, and its "independent constraints" need their Newtonian assumption stated. The video headline over-reads it.

## 5. Bottom line for this programme
The decline Gaia sees to 27 kpc is what the law predicts from the baryons, **if** the Milky Way's baryons are near 7.3 × 10¹⁰ rather than the census 5.4 × 10¹⁰. That ~3σ disc-mass question is the real issue, not modified gravity versus a Keplerian tail. CFG532 (running) scores the framework at the census baryons. Gaia DR4 decides on two fronts: whether the curve flattens at about 175–195 km/s, and the vertical-force map that separates round cold energy (CFG516) from a dark or phantom disc (the Sylos Labini claim).

κ = ½ is fitted; the cold energy's mass is still required; not theory closed. Literature numbers are taken from the review's text, not re-derived from the cited papers.

## 6. Update, same day: CFG532 (census baryons held fixed)
The heavy-disc problem in §3.5 depends on which form of the round rule is used:
- **RM-v** (the algebraic law on the in-plane field) fits with **census baryons**: M* needed 5.4–6.1 × 10¹⁰, within z −0.1 to +1.2 of the census. χ² against Ou+24 is 55.9/37 canonical and 12.9/37 alt; against Eilers+19, 30.7/38 and 11.5/38.
- **RM-φ** (the QUMOND phantom's enclosed mass) still needs a disc +1.5 to +3.0σ heavier than the census.

**The real tension is shape.** The law's outer slope over 15–27.5 kpc stays between −0.10 and −0.19 for every disc mass and footing. Measured slopes are −0.33 ± 0.07 (Ou+24) and −0.28 ± 0.07 (Eilers+19), with Keplerian at −0.5. So the law is 1.7–3.0σ too shallow, and by its frozen rule CFG532 is EXCLUDED (shape) on Ou+24.

How to read that:
- **It hinges on systematics.** Ou's own upper inner-error budget makes RM-v consistent on both footings.
- **The fitted NFW misses the same slope by about the same amount** (−2.1σ on Ou, −2.9σ on the compilation; applied post hoc, so not a verdict input).
- **Keplerian is 2.4–3.7σ from the data too.**
- **The lever is 15–22 kpc.** Points beyond 19 kpc carry 15% errors and absorb every model.
- **The DR4 decider:** a slope of −0.25 or steeper, held with an error of 0.04 or less, excludes the law on shape whatever the disc mass. A slope of −0.20 or shallower passes it.
