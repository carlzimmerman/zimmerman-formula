# QX20 frozen criteria: what the plain law's missing boost tracks (the failure ladder)

Frozen before any QX20 script exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Both footings,
never pooled. No new data: SPARC, Humphrey+2006 ellipticals (QX16-fixed host list), Lovisari+2015 groups, X-COP
(all through QX5's loaders, read-only, in qx5.py's QX16-fixed state), and the S1 Coma UDGs (rebuild_2026_10_22/S1).

## Offsets (measured; the plain law, unchanged)

Per point, offset D = log10(M_obs / M_law) for the hot systems and log10(g_obs / g_law(g_bar)) for SPARC. M_law is the
law's enclosed mass from the baryons alone (QX5's tables, class-independent part). This uses:
- SPARC: QX5's loader, Upsilon disc 0.5 and bulge 0.7, quality <= 2, i >= 30.
- Ellipticals: 7 x (2, 4, 8 Re), with the Kroupa M*/L, as in QX18.
- Groups: 20 x (R2500, R500). The stellar allowance is f_* = 0.5 (primary, set now); 0 and 1 are reported only.
- X-COP: 35 points.
- Coma UDGs: S1's per-galaxy E_v3_dmean / ln 10. This is the offset against the action with Coma's EFE, not against
  the bare law; it is stated as such and used only as a predicted, not fitted, class.
"Hot systems" = ellipticals + groups + X-COP (75 points).

## Candidate variables (all measured; none fitted)

V1 M_b(<r), the enclosed baryonic mass.
V2 v_obs = sqrt(G M_obs / r), a sigma / T_X proxy. Disclosed: it shares M_obs with D, so a correlation is partly built
   in. The shuffle control is what grades it.
V3 the gas fraction f_gas = M_gas / M_b(<r). SPARC uses v_gas^2 / v_bar^2; ellipticals have f_gas = 0, because their
   hot gas is not in the model (QX18).
V4 g_N / a0 at the measurement radius. The surface density Sigma_b = M_b(<r) / (pi r^2) is the same variable,
   g_N = pi G Sigma, so it is not graded separately.
V5 r / r_M with r_M = sqrt(G M_b,tot / a0), M_b,tot taken at the outermost baryon point. A Sigma built on the total
   mass is the same variable.
V6 the environment depth Phi/c^2 from the observed g out to the tail: QX5 class a's key, which QX12 read as total-mass
   depth.
UDGs: V1 = Mstar; V2 = sigma_obs; V3 = 0; V4 from G (Mstar/2) / r_h^2 with r_h = (4/3) Re; V5 with r = r_h and
M_b,tot = Mstar. V6 for UDGs is NOT AVAILABLE on disk in a comparable form (Coma's observed potential profile): it is
reported as N/A, not modelled.

## Fit and grade (per variable, per footing)

- Model D = A * (v / v_med)^b. v_med is the hot-system median; b is grid-searched over [-3, 3] in steps of 0.01;
  A >= 0 comes from closed-form least squares, unweighted, on the 75 hot points only.
- H (hot fit): rms of the hot residual <= 0.10 dex (the HO1 line).
- Z (zero anchor): the predicted mean D over the SPARC points minus SPARC's observed mean D, within |..| <= 0.057 dex
  (PAPER67's scatter line). SPARC is predicted, never fitted.
- U (UDGs, reported, not part of the PASS): predicted mean minus observed mean UDG offset, with S1's sigma_tot.
- A variable is PREDICTIVE if H and Z both hold on both footings. Ranking: PREDICTIVE first, then by the larger
  |Z gap| over the footings, then by hot rms.
- One curve vs a step: in the overlap of the SPARC and hot ranges of v (SPARC points whose v lies inside the hot
  points' [5, 95]% range), compare the SPARC median D with the hot median D at matching v (hot points in the same
  range).
  - STEP if they differ by > 0.10 dex.
  - ONE CURVE if Z holds and there is no step.
  - SEPARATED if fewer than 20 SPARC points overlap (the data cannot tell).

## Labels

- TRACKED BY <Vk>: some variable is PREDICTIVE.
- NO SINGLE VARIABLE: none is PREDICTIVE. That is the expected outcome given QX5/QX6, and the Lean monotone-sandwich
  logic (QX5_monotone_sandwich) is cited: a monotone f(v) cannot be 0 on SPARC and > 0 on hot points at overlapping v.
  The step / one-curve readings then say what the boost tracks.

## Known answers (lines)

KA1: the class mean offsets reproduce QX16's fixed qx5 baseline to 1e-6.
- canonical: X-COP +0.467499, ellipticals +0.209888, SPARC +0.027383, groups f_* = 0 +0.358644 and f_* = 1 +0.195519.
- alt: X-COP +0.434523, ellipticals +0.188763, SPARC -0.000603, groups +0.320274 / +0.158280.
KA2: the UDG mean offset equals S1's mean E_v3_dmean / ln 10 to 1e-9.

## Controls (separate outputs, qx20_MUTATE.*)

- M1 shuffle: v is permuted across the hot points with a fixed seed of 20261106, 200 permutations. For the best
  variable, the fraction of permutations with hot rms <= its real hot rms must be <= 0.05, or the variable's H carries
  no information and it is reported NOT INFORMATIVE.
- M2 Newton baseline: replace M_law by M_b (g_law by g_bar). SPARC's observed mean D is then far from 0, so Z must
  fail for every variable (the anchor has power).

Compute: one thread, nice -n 15, seconds to minutes.
