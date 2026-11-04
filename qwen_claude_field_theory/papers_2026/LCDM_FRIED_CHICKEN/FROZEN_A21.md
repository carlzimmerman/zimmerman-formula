# FROZEN A21: "the law simply emerges in LCDM hydrodynamic simulations"

Frozen before any A21 number is computed. Script `scripts/recipe23.py`, output `scripts/recipe23.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence.

## Route

The rival's claim: the radial acceleration relation (RAR) is not put in by hand; it emerges from galaxy formation in LCDM hydrodynamic simulations, so the law is a by-product and a0 is whatever the simulations return. This lane does not run a simulation. It gathers what the published suites report and grades those reports on this folder's gates.

Literature to gather (at least): Keller & Wadsley 2017 (MUGS2), Ludlow et al. 2017 (EAGLE/APOSTLE), Navarro et al. 2017 (analytic, halo scale), Tenneti et al. 2018 (MassiveBlack-II), Dutton et al. 2019 (NIHAO), Garaldi et al. 2018 (satellites), any IllustrisTNG or FIRE RAR paper found, any suite with varied Lambda or rho_DE (EAGLE varied-Lambda runs, Barnes et al. 2018, Salcido et al. 2018), and any paper reporting RAR redshift evolution in simulations.

For each: reported a0 or g-dagger, fitted functional form, intrinsic scatter, redshift dependence, dependence on cosmology, and whether the result is emergent (feedback calibrated on other observables, RAR not targeted) or calibrated (sub-grid tuned on relations that already encode the RAR, e.g. the stellar mass-halo mass relation, sizes, or the Tully-Fisher relation). All values are PROVISIONAL web look-ups (WebSearch/WebFetch of arXiv abstracts or HTML; no PDFs, data or code downloaded) or flagged FROM MEMORY when not verified.

## Equations

- Law: g = (g_b + sqrt(g_b^2 + 4 g_b a0))/2, a0 = 9.3625e-11 (lib A0); c sqrt(G rho_DE) = 1.8727e-10 at Omega_L 0.685 (A15).
- McGaugh et al. 2016 form, used by most suites: g = g_b / (1 - exp(-sqrt(g_b/g_dag))).
- Ludlow et al. 2017 form, if its coefficients are recovered: g = g_b/(1 - exp(-sqrt(g_b/g_dag))) + g_hat exp(-sqrt(g_b g_dag/g_hat^2)) (form FROM MEMORY until checked).
- Any other reported form is coded as written in the source.
- Law-equivalent a0 of a reported curve: lib.fit_a on SPARC's 3373 g_b values (ALLB) against the reported curve evaluated at those g_b.

## Knobs

None tuned. Each reported curve is used at its published coefficients; 0 knobs fitted on the law. The coefficients themselves were fitted by each paper to its own simulated galaxies; that is counted as the paper's fit, stated per entry, not as a knob here.

## Gates

(a) Each reported (form, g_dag) put on SPARC's real baryons (Upsilon 0.5/0.7), graded by lib.grade: E1 rms to law <= 0.02 dex, E2 p95 per galaxy <= 0.04, E3 worst bin <= 0.02; rms to observed reported (A15 comparison: law at A0 gives 0.1951, A15 U1 swap 0.2013). Holdout: nothing tuned, so the holdout number is the unseen rms to law on GS[1::2] of the same curve, <= 0.025. A reported curve that only covers part of the SPARC g_b range is still evaluated over the full range, and its stated range is reported.

(b) Tie gates from what the papers report:
- G1 kappa_eff = a0_equiv / (c sqrt(G rho_DE)) within 0.05 dex of 0.5. a0_equiv from fit_a above. Note the paper's own cosmology (WMAP vs Planck Omega_L) and use the rho_DE of that paper's cosmology where stated; the difference is reported.
- G2 slope d ln a0 / d ln rho_DE = 0.50 +- 0.05: only from a suite that reports RAR scale at two or more values of Lambda. If a varied-Lambda suite reports something convertible (e.g. halo concentrations, V_max at fixed mass, galaxy sizes) the implied slope is estimated and labelled ESTIMATE, not a gate result. Otherwise NOT TESTABLE.
- G3 a0(z)/a0(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33: only from reported redshift dependence; partial redshift coverage graded at the redshifts given, marked as such; otherwise NOT TESTABLE.
- G4 one constant across galaxy hosts (log M200 11 to 12.5), rms of log a0 <= 0.1 dex: from reported per-galaxy or per-mass g_dag spread if given; reported intrinsic RAR scatter is NOT the same thing and is reported separately; otherwise NOT TESTABLE.
- G5 operative at galaxy radii: hydrodynamic halo plus baryon gravity, so PASS by definition for the simulations; for Navarro et al. 2017 too (halo gravity).

Extra tolerance: when a paper quotes g_dag with an error, G1 is also checked with that error added in quadrature to the 0.05 dex (reported, not used for the verdict).

## Verdict rule

The route "supplies the law" only if some suite passes (a) E1 to E3 and holdout, and G1 to G4 (none NOT TESTABLE). "Supplies the tie" needs G1 and G2 and G3 from reported numbers. If G2 is NOT TESTABLE everywhere, the swoop question (does a0 track rho_DE) is answered NOT ON RECORD, which is neither pass nor fail.

## Expected in advance

Most suites report g_dag 1.0 to 1.3e-10 in the McGaugh form, which differs from the law in shape, so E1 fails at the 0.03 to 0.05 dex level (the two interpolating functions differ by that much), E3 fails at low g_b; Ludlow's 3e-11 with the extra term fails E1 more. G1 passes or is near for the McGaugh-like values (a0_equiv near 0.9 to 1e-10, kappa_eff ~0.5) - but that agreement is calibrated in part, since feedback is tuned to the SHMR. G2 NOT TESTABLE (varied-Lambda EAGLE runs did not report the RAR). G3 NOT TESTABLE or partial. G4 NOT TESTABLE or partial.

## LITERATURE TABLE (gathered after freezing, before the run; all PROVISIONAL web look-ups of arXiv abstracts / ar5iv HTML via a summariser, no PDFs downloaded; items marked (memory) not verified)

| Suite / paper | reported scale | form | intrinsic scatter | z dependence | cosmology (OL, H0) | emergent or calibrated |
|---|---|---|---|---|---|---|
| MUGS2, Keller & Wadsley 2017 (arXiv 1610.06183), 32 galaxies | no own fit; SPARC g_dag 1.20e-10 "fits at least as well" | McGaugh | 0.06 dex | "significant", settles to the relation only near z 0; shallower low-g_b slope at high z; nearly none without feedback; no numbers | WMAP3 0.76, 73 | feedback said to have no free parameter beyond SN energy: closest to emergent; the scale is not a fitted output |
| EAGLE / variants, Ludlow et al. 2017 (1610.07663) | g_dag ~2.6e-10 (ar5iv text; Keller and Tenneti quote 3.0e-10, likely v1) | McGaugh only (no second term) | 0.08 dex | progenitors at four higher z "very similar", slight systematic residual; no numbers | Planck13 0.693, 67.77 (memory) | calibrated on GSMF and size-mass; rescaling M* to Moster abundance matching brings all runs to the observed relation (no number given) |
| Navarro et al. 2017 (1612.06329) | a0 "very nearly" 1e-10 = peak NFW acceleration of the most massive disc host; a_min ~1e-11 | uses McGaugh MDAR, no fit | - | none stated | 0.693, 67.77 | analytic; scale set by halo mass range of discs (V200 30-300) |
| MassiveBlack-II, Tenneti et al. 2018 (1703.05287) | McGaugh g_dag: full 2.01, bright 3.05, faint 1.151, centrals 3.491 (1e-10); power law slope 0.6849, intercept -2.759 | prefers single power law below 1e-9 | ~0.1 full | z 0.06 only | WMAP7 0.725, 70.2 | not tuned to RAR: emergent, does not match SPARC's shape |
| NIHAO, Dutton et al. 2019 (1902.06751), 89 galaxies | no own fit; compared with SPARC 1.20e-10, "very good match" | McGaugh | 0.079 (0.04 at M* 1e9.3-1e11, 0.11 below) | z 0 only | Planck14 0.6825, 67.1 | feedback forms the right stellar mass (Wang 2015); calibrated on SMHR (memory, Stinson 2013) |
| ZOMG, Garaldi et al. 2018 (1712.04448) | centrals 1.40 +- 0.07, ODR 1.19 +- 0.02; satellites 1.48 +- 0.08 (1e-10) | McGaugh | centrals 0.048, satellites 0.192 | g_dag = (-0.84a + 2.23)e-10 centrals, (-0.72a + 2.11)e-10 satellites, 0.33 <= a <= 1, ~10 % errors | Planck+WP+highL+BAO (0.692, 67.8 memory) | matches SMHR; calibration not stated |
| Magneticum, Mayer et al. 2022 (2206.04333) | z 0.1: RAR 1.14 +- 0.04, MDAR 1.12 +- 0.04 (1e-10) | McGaugh / simple | not quantified | a0 rises ~x3 from z 0.1 to z ~2 (paper says 2, 2.3 and 2.8 in different places); slower than a0 ~ H(z); numbers only in a figure | WMAP7 0.728, 70.4 | calibration unknown |
| FIRE-2, Mercado et al. 2024 (2307.09507), 20 zooms | no fit; compared with SPARC 1.20 | McGaugh | not quantified | z 0 only | ~0.69, 68 (memory) | no tuning to galaxy relations claimed (memory) |
| Grudic et al. 2020 (1910.06345) | g_dag ~ pi G Sigma_crit ~ 1e-10 ~ 0.1 G m_p / sigma_T | sqrt(g_b g_dag) limit | - | none (no cosmology in the scale) | - | analytic, FIRE-motivated feedback argument |
| Paranjape & Sheth 2021 (2102.13116) | a0 explained by a_vir (1+c)^2, ~1.3e-10 at 1e12/h, larger for clusters | - | - | low-z only | WMAP7 | analytic, halo mass dependent; recorded, not graded |
| EAGLE varied Lambda, Barnes et al. 2018 / Salcido et al. 2018 (1801.08781) | Lambda 0, 1, 3, 10, 30, 100, 300 x observed | no RAR, concentration, Vmax or size vs Lambda reported | - | - | - | - |
| IllustrisTNG | no RAR paper found in two searches | | | | | |

## RESULTS (written after the run; criteria above unchanged)

Runtime 3 s, 77 MB RSS. No bug found; no before-fix output.

(a) SPARC grades (`recipe23.out`, `== ...` blocks). No simulation-fitted curve passes E1. Best: Magneticum z 0.1 g_dag 1.14, E1 0.0290, E2 0.0387 PASS, E3 0.0392, holdout 0.0294, rms to observed 0.1975; MBII faint 1.151, E1 0.0306; ZOMG ODR 1.19, E1 0.0359; ZOMG 1.40, E1 0.0624; MBII full 2.01, E1 0.1237; MBII power law E1 0.1512; EAGLE 2.6, E1 0.1687 (rms to observed 0.2589); EAGLE 3.0, E1 0.1942. MUGS2, NIHAO and FIRE-2 did not fit a scale; their curve is SPARC's own McGaugh 1.20, which differs from the law by E1 0.0372, E3 0.0496 (shape, not scale: residuals +0.050 at g_b 1e-12 to -0.011 at 1e-9). Every McGaugh-form curve sits above the law at low g_b, so E3 fails for all suites. The only passes (E1 0.0101, holdout 0.0095, kappa_eff 0.522) are the analytic round numbers "~1e-10" of Navarro 2017 and Grudic 2020; these are order-of-magnitude statements, not measured outputs, and the pass reflects only the round number. The quantitative version of Navarro's argument, A15 U1 on the same halos, gives median 0.612 a0 with 0.156 dex spread and fails.

(b) Tie gates.
- G1 (own cosmology): PASS Magneticum 0.554 (+0.044 dex), and MUGS2 0.550 (+0.042) where the scale is SPARC's accepted 1.20 in WMAP3's larger rho_DE, so it is not a simulation output. FAIL ZOMG 0.726 / 0.616, MBII 0.987 / 0.562 (+0.051, just outside), NIHAO 0.632, FIRE-2 0.620, EAGLE 1.355 / 1.565. In the lib (Planck 2018) cosmology every simulation fails G1.
- G2: NOT TESTABLE. No suite reports the RAR (or any convertible internal-structure quantity) at two Lambda values; the EAGLE varied-Lambda runs report halo growth and star formation only, so no implied slope can be estimated from their numbers. Cross-suite diagnostic (not a gate): slope -2.11 over only 0.055 dex in rho_DE against 0.361 dex in a0_equiv, i.e. feedback differences dominate.
- G3: FAIL where numbers exist. ZOMG centrals a0(z)/a0(0) 1.305, 1.367, 1.428 (z 2.33 slightly extrapolated past a 0.33); satellites 1.262, 1.314, 1.366; all above the band's upper edges 1.03, 1.12, 1.21. Magneticum ESTIMATE (power law through x3, z reference 2 to 2.8): 1.86-2.15, 2.27-2.75, 2.93-3.78, FAIL. MUGS2 qualitative, rising into the past, leans FAIL; EAGLE qualitative "very similar", leans flat, NOT TESTABLE numerically.
- G4: MBII subsamples (luminosity / central split, a proxy, not host-mass bins) rms 0.217 dex, range 0.486, FAIL (PARTIAL); ZOMG centrals vs satellites 0.024 dex (environment split, PARTIAL proxy, within 0.1). Others NOT TESTABLE.
- G5: PASS by definition (halo plus baryon gravity).

Verdict: the route DOES NOT SUPPLY THE LAW on these gates: no simulation curve passes E1 to E3, and the tie is NOT ON RECORD. No simulation tracks rho_DE (G2 never measured). The two suites that report z dependence numerically put the scale rising into the past, outside the band. None stays flat; EAGLE's "very similar" is qualitative. Emergent versus calibrated: MBII (emergent) gets the wrong shape, a power law; MUGS2 (closest to emergent) reproduces SPARC at z 0 but evolves; EAGLE (calibrated on GSMF and sizes) is 2.2x high raw and matches only after M* is rescaled to abundance matching; NIHAO and ZOMG match the SMHR, which already encodes much of the baryonic Tully-Fisher scale. The closest single number, Magneticum's 1.14 (G1 pass in its own cosmology, E1 0.029), comes from a run whose a0 triples by z ~2.

Expected-versus-found: as expected for E1 and G2. G1 came out closer than expected for Magneticum and further for EAGLE/MBII. G3 was expected NOT TESTABLE, but ZOMG and Magneticum give numbers, and both FAIL.

Deviations: (1) the Ludlow second-term form (g_hat) written in the frozen plan FROM MEMORY is not in Ludlow et al. 2017 (one equation only); both reported g_dag values, 2.6 and 3.0, were graded instead. (2) Added beyond the minimum list: Magneticum (Mayer 2022), FIRE-2 (Mercado 2024), Grudic 2020, Paranjape & Sheth 2021 (recorded only). (3) The MUGS2, NIHAO and FIRE-2 rows grade SPARC's 1.20, since these papers fit no scale of their own. (4) Cosmologies for EAGLE, ZOMG and FIRE-2 are from memory. (5) The Magneticum z ratios come from a power-law interpolation of one stated factor, and the paper itself is inconsistent about the redshift, so they are an ESTIMATE.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
