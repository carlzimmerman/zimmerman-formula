# XCV1: X-COP clusters with a mass that does not assume hydrostatic equilibrium. FROZEN CRITERIA

Committed alone, before any XCV1 script exists and before any XCV1 number is computed. TEST lane, quarantined: it adopts
nothing, relabels nothing (RB1's labels stand as graded) and registers nothing. Form B = the a0 law with cold dark energy counted
once (PAPER72, DOI 10.5281/zenodo.24106867). kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating field
component with w about 0, never a particle. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (a0 = 1.1312e-10 m/s^2), graded
separately and never pooled.

It grades PAPER72's open item 6 ("the richest clusters sit at or above the form's ceiling, depending on the hydrostatic mass
used") with spectroscopic (caustic) masses, and says what it can about open item 11 (the outer cluster shear near 3 sigma).

## 0. Coverage, stated plainly

- **Only 6 of the 12 X-COP clusters are covered:** A85, A1795, ZW1215 (HeCS "Zw1215"), A2029, A2255, A2142 are in HeCS-omnibus.
  A644, A1644, A2319, A3158, A3266 and RXC1825 are not. Of the six, **five have measured stellar profiles** (A85, A1795, A2029,
  A2142, ZW1215); A2255 has none (RB1 imputed its stars).
- **No public raw shear profile beyond R500 exists for any of them** (a read-only literature search on 2026-11-10 found none). The
  weak-lensing masses in the record are NFW fits (Herbonnet+2020 MENeaCS/CCCP, DM14 concentration) and the LC^2 compilation's
  spherical masses at fixed 1.0 / 1.5 Mpc, also model-deprojected. They are reported beside, never graded and never called raw.
- So open item 11 is **not graded** here (section 6).

## 1. The non-hydrostatic mass: what HeCS-omnibus measures (established from the paper first)

- Source table: Sohn et al. 2020, ApJ 891, 129 (arXiv:1910.11192), table 2, VizieR J/ApJ/891/129/table2, on disk at
  `../_external_data/hecs_omnibus_2026_11_10/table2.tsv` (repo-relative `../_external_data/...` = the folder beside the repo),
  sha256 d538ece0...509482 per its FETCH_LOG.md. Read with `python3 -I`; untrusted data.
- **How M200 is measured (the paper's own text, read 2026-11-10 from the arXiv PDF, sha256 2c151801...869897, not stored in the
  repo):** Section 3.2 computes the mass profile with the caustic technique (Diaferio & Geller 1997) and, "based on the caustics",
  the characteristic M200 and R200 (mean density 200 x critical at the cluster redshift). Table 2's note: "R200 and M200 based on the
  caustic technique." sigma_cl is a bi-weight dispersion of members inside R200 with bootstrap errors; it does **not** enter M200.
  Cosmology H0 = 70, Omega_m = 0.3, Omega_L = 0.7 (the same frame as X-COP's h = 0.7).
- **So M200 is a caustic mass, not virial and not a sigma scaling.** The caustic mass is G M(<r) = F_beta Int_0^r A^2(r') dr', A the
  caustic amplitude in redshift space. It assumes no hydrostatic equilibrium and no gas physics; it assumes the galaxies are test
  particles in the total potential (true under form B: Newtonian gravity with the total mass, the cold component collisionless).
- **Calibration (model-derived, stated and bracketed, not hidden):** F_beta is a filling factor calibrated on N-body simulations of
  LCDM haloes (it folds in the velocity anisotropy and density profile of simulated haloes). Sohn+2020 do not print F_beta. Serra,
  Diaferio, Murante & Borgani 2011 (MNRAS 412, 800; arXiv:1011.0372) find F_beta = 0.7 most appropriate (DG97/D99 used 0.5 with an
  older amplitude algorithm), recover mass profiles to better than 10 % in (0.6-4) r200, overestimate the mass by up to 70 % inside
  about 0.6 r200, and give individual-cluster 1-sigma uncertainties of 40-80 % in (0.6-4) r200 (projection). **Assumed: HeCS-omnibus
  uses F_beta = 0.7** (Diaferio is a co-author; membership by Serra & Diaferio 2013). This and the Serra numbers come from a WebFetch
  read and are PROVISIONAL (the record's rule for WebFetch look-ups).
- **Consequence used here:** at fixed radius the caustic mass is linear in F_beta, so M_caus(<R200_HeCS) x (F_beta / 0.7) is exact
  for any other F_beta. Whether the simulated haloes' anisotropy applies to form B's cold component is not known; the bracket below
  is how much it would have to move.

## 2. Comparison radius and inputs

- **Graded radius: each cluster's HeCS R200** (A85 1.73, A1795 1.57, ZW1215 2.00, A2029 1.90, A2255 1.90, A2142 1.63 Mpc; all are
  between 1.14 and 1.59 X-COP R500, i.e. beyond R500, and inside every gas profile's tabulated range). M_dyn = HeCS M200 (inside
  that radius by definition).
- **Baryons at that radius, as RB1 used them:** X-COP gas MGAS (Eckert+2019 fgas files; X-ray, not hydrostatic) and measured stars
  MSTAR (`*_mstar.fits`, HDU 2), log-log interpolated (RB1's `li`), h = 0.7 data frame. Where the stellar profile ends inside the
  radius (expected for A85 only), **graded: the star-to-gas ratio held at its last tabulated value**; bracket: M_star held constant.
  A2255: RB1's imputed stars (the median measured star-to-gas ratio profile), bracket only.
- **RB1's radii (reported, not graded):** R500 (Ettori 2019) and RB1's last radius. No caustic mass is measured there; two reported
  transfers: (i) the hydrostatic profile rescaled by the cluster's ratio Q (section 4), M = Q x M_FORW(r); (ii) NFW with Dutton &
  Maccio 2014 c200 normalised to the caustic M200 (EXTERNALLY CALIBRATED).
- Errors: caustic e_M200 as tabulated (statistical); gas from MGAS_LO/HI and stars from MSTAR_LO/HI at the radius (half-width,
  lognormal), as RB1's `mc_above`.

## 3. The gate: RB1's conservation reading with the non-hydrostatic mass

- **f_ret = R M_b,obs / (M_dyn - M_b,obs)**, R = 5.41 (bracket 5.562), M_dyn = M_caus. Form B: f_ret <= 1 at the edge. M_dyn <= M_b
  counts as +infinity.
- **Per cluster (graded on the five measured-star clusters; A2255 labelled as a bracket):** P(f_ret > 1) from 4,000 lognormal draws
  (seed 1110 + i) of gas, stars and M_dyn, with **M_dyn's ln-sigma = the tabulated error in quadrature with the method's own
  per-cluster scatter, ln(1.4) = 0.336** (Serra's 40 %, the lower end of their 40-80 %; choosing the lower end makes a per-cluster
  label easiest to reach). **ABOVE THE CEILING** if P > 0.977; **BELOW THE CEILING** if P < 0.023; else **AT THE CEILING**.
  Reported beside: the same with the tabulated error only.
- **Class (graded):** median f_ret over the five measured-star clusters, 95 % interval from 10,000 bootstrap resamples (seed 1110),
  RB1's `class_stat`. **ABOVE THE CEILING** if the lower end > 1; **BELOW THE CEILING** if the upper end < 1; else **AT THE CEILING**.
  Fewer than 5 finite systems: NOT EVALUABLE.
- **Calibration tag:** the class is recomputed with M_caus x 0.9 and x 1.1 (Serra's "better than 10 %"). If the label differs at
  either end: **[CALIBRATION-DEPENDENT]**. Reported further: F_beta = 0.5 (x 0.714, the superseded DG97/D99 value), the F_beta that
  puts the class median at exactly 1, R 5.562, stars held constant, all 6 with A2255, h 0.7 -> the footing's h (gas x (0.7/h)^0.5),
  and a parametric class reading (inverse-variance mean of ln f_ret with the per-cluster sigmas above).
- **What counts against form B:** the class ABOVE THE CEILING on the graded reading without the calibration tag; or ABOVE with the
  tag (then "against form B unless the caustic calibration is 10 % low"); or any measured-star cluster ABOVE THE CEILING per cluster.
  AT or BELOW does not count against B. Stated plainly: the gate is one-sided as in RB1. Below 1 is read as baryons lost and is not
  tested here.

## 4. The hydrostatic-bias reading

- Per cluster **Q = M_caus(<R200_HeCS) / M_FORW(<R200_HeCS)** (RB1's graded hydrostatic mass, interpolated at the same radius), with
  lognormal errors from both. Class median Q and 95 % bootstrap (seed 1110) over the five measured-star clusters; A2255 reported.
- Reading (reported, not a gate): **HYDROSTATIC LOW** if the lower end of Q > 1 (dynamics heavier: relieves B); **HYDROSTATIC HIGH**
  if the upper end < 1 (dynamics lighter: worsens B); else **NO DETECTED BIAS**. Also Q against M_NFW (X-COP's NFW-fit hydrostatic
  mass, RB1 A1's bracket). RB1's ceiling at R500 needed about 10 % (Q about 1.10) to move.
- The same-radius **hydrostatic f_ret at R200_HeCS** (M_FORW and M_NFW) is printed beside the caustic one.
- Never graded: the literature's b (it is set by assuming a cosmic baryon fraction).

## 5. Both footings

f_ret, Q and the gate contain no a0, so both footings must give identical gate numbers (checked; KA-4). a0 enters one reported row
only: the law's missing-mass fraction at R200_HeCS, (M_caus - M_law(M_b))/M_caus, M_law = g_law r^2 / G with RB1's `glaw`.

## 6. Open item 11 (outer cluster shear): not graded

No raw shear profile beyond R500 exists for these clusters (section 0). Reported only, beside the caustic mass and never as raw:
Herbonnet+2020's NFW (DM14 c) mass inside R200_HeCS and its f_ret; LC^2 masses at 1.5 Mpc against the caustic profile transferred
there (NFW-DM14, externally calibrated) and their f_ret with baryons at 1.5 Mpc; the ratio M_caus / M_WL at R200_HeCS. A lensing-vs-
dynamics ratio far from 1 would be a flag for item 11, not a grade.

## 7. Known answers (each can fail; a KA failure gives NO VERDICT for what it feeds)

- **KA-1 (RB1 reproduced):** with my own loader (RB1's builder copied, not imported), the hydrostatic f_ret of A85, A1795, A2029,
  A2142, ZW1215 at RB1's last radius and at R500 (M_FORW), and at both radii on M_NFW (A1 rows), equal `rb1.json`'s per-cluster values
  to 1e-6 relative. A2255 is not in RB1's per-cluster rows; its numbers are printed, with no reference. Feeds the gate and Q.
- **KA-2 (HeCS frame):** for the six rows, M200 = 200 rho_c(z) (4 pi / 3) R200^3 with H0 70, Omega_m 0.3 must hold within the rounding
  of the printed R200 (+-0.005 Mpc, i.e. the M200 implied at R200 +- 0.005 brackets the table's M200, widened by the M200 rounding
  +-0.005e14). A failure means the table is not in the frame read; it feeds the gate.
- **KA-3 (parser):** 227 HeCS rows; the six X-COP names found once each within 6 arcmin and |dz| <= 0.01 of X-COP's position and z;
  12 X-COP clusters, 7 with stars (RB1's KA-5).
- **KA-4 (identities):** M_dyn = (1 + R) M_b gives f_ret = 1 to 1e-12; F_beta scaling: M x (0.7/0.7) returns the input exactly;
  footings give identical gate and Q numbers.
- **KA-5 (L24's lensing loader):** the NFW-DM14 machinery copied from `fable_independent_2026/L24_lensing_vs_dynamics.py` reproduces
  Herbonnet's published M500 from their M200 to 5 % (L24's C3). Feeds only section 6.

## 8. MUTATE (separate outputs `xcv1_MUTATE.out` / `.json`)

- **M1, R x 2:** must push the class ABOVE THE CEILING. If not, the class gate has no power: NOT EVALUABLE.
- **M2, F_beta 0.7 -> 0.35 (caustic masses halved):** must push the class ABOVE. If not, NOT EVALUABLE.
- **M3, caustic masses permuted among the five clusters** (one fixed derangement, seed 1110): per-cluster f_ret must move by >= 0.10
  rms (the per-cluster labels track each cluster's own mass). If not, the per-cluster labels are NOT EVALUABLE.
- **M4, M_dyn = M_FORW at R200_HeCS in place of the caustic mass:** must give the hydrostatic f_ret printed in section 4 exactly
  (the gate's code path is the one RB1's mass goes through).

## 9. Labels (vocabulary frozen)

Per footing: class **BELOW / AT / ABOVE THE CEILING** (+ [CALIBRATION-DEPENDENT] if so), per-cluster labels, the Q reading;
**NO VERDICT** if KA-1, KA-2 or KA-3 fails; **NOT EVALUABLE** if M1 or M2 does not bite. Never PASS: the gate is one-sided. RB1's labels
are not changed by anything here; RESULT.md says what this reading would mean for PAPER72's item 6.

## 10. Seen before freezing (disclosed), and hand estimates

- **Read:** RB1's criteria, A1 and RESULT (its per-cluster f_ret lists at the last radius and R500); rb1.py's X-COP builder; the
  six HeCS rows (R200, M200, sigma); the extents of the six X-COP gas, star and hydrostatic profiles (no mass value taken from them);
  `xcop_r500_ettori2019.json` (its hydrostatic R200 / M200 per cluster); L24's Herbonnet and LC^2 tables; PAPER72's open items;
  Sohn+2020 sections 2-3 and table 2's note; Serra+2011's abstract and its F_beta passage. No XCV1 f_ret, Q or label is computed.
- **Hand estimate (mine, from the json and the HeCS rows only):** the caustic M200s sit below X-COP's hydrostatic M200s at smaller
  radii (A85 6.23 at 1.73 Mpc against 8.5 at 1.92), and M_FORW(<1.73 Mpc) is plausibly about 7.5, so Q about 0.8 and the caustic
  f_ret above the hydrostatic one. I give 60 % that the class reads ABOVE THE CEILING, 35 % AT, 5 % BELOW; 50 % that it carries the
  calibration tag; per-cluster labels mostly AT (the 40 % method scatter).

## 11. Operational

One thread, nice 10; `xcv1.py` -> `xcv1.out` / `xcv1.json`, `xcv1_MUTATE.out` / `.json`, `RESULT.md`. Other lanes' code is copied,
not imported; their folders are read only. Explicit-path commits; pushed by replaying the commits onto origin/main with merge-tree +
commit-tree. Downloads nothing.

kappa = 1/2 FITTED; not theory closed. Adopts nothing. Relabels nothing.
