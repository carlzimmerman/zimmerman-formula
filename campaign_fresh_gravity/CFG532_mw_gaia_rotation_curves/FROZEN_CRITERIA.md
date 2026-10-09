# CFG532 FROZEN CRITERIA: the Gaia-era Milky Way rotation curves (the "Keplerian decline" debate) against the law with census baryons

Written and committed alone, before any script of this lane exists and before any number of this lane is computed (2026-10-09).

kappa = 1/2 is FITTED. Both footings everywhere, never pooled: canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2. Kernel nu_mono
(nu(y) = 1/(1 - exp(-sqrt y))). No dark-matter particle: the cold energy's MASS is still required. Nothing here may be reported as
"theory closed" or as the data favouring the framework. Gaia DR4 preregistration and every *_HASH file: READ ONLY.

## 0. Trigger and scope (owner-approved download scope, as corrected by the coordinator on 2026-10-09)

Review: Melchiorri & Ruchika, arXiv:2608.10189 (revised 2026-09-12). Its arXiv LaTeX source is the ONE download of this lane
(logged in FETCH_LOG.md with URL, size, SHA-256, date). The cited curves' own data tables are NOT fetched: only curves already on
disk are scored. Curves the review discusses that are not on disk are listed in the README with source and approximate size, for
the owner to approve; they are NOT scored and no verdict is given for them.

Scored curves (on disk):
- **C1 Ou+2024** (arXiv:2303.12838, Table 1; real_research/data/mw_rc_ou2024_table1.tsv; 37 points, 6.27-27.3 kpc; R0 = 8.178;
  verified against the paper's LaTeX in the record). Errors: random (mean of sig_plus, sig_minus) in quadrature with the
  systematic fraction 3% at R <= 22 kpc and 15% beyond (the review's Fig. 2 convention and CFG513's; the authors state 1-5% to
  22 kpc and 15% beyond).
- **C2 Eilers+2019** (arXiv:1810.09466, Table 1; real_research/data/mw_rc_eilers2019_table1.tsv; 38 points, 5.27-24.82 kpc;
  R0 = 8.122). Errors: random (mean of sig_minus, sig_plus) in quadrature with 3% (the review's Fig. 2 convention; the authors
  state 2-5%).
- **C3 the review's own compilation** (Table "tab:rc_data" of the fetched source; 35 entries, 6.3-49.0 kpc, rescaled by the
  review to R0 = 8.178; sigma includes statistical and systematic as the review reports). Transcribed from the LaTeX by the
  script (parsed, not hand-typed). It is HETEROGENEOUS: inverse-variance means of overlapping disc curves (Eilers, Mroz, Ablimit,
  Zhou, Wang, Jiao, Ou, Sylos Labini) plus model-dependent halo-tracer entries (Huang, Ablimit, Kafle, Wegg); the review says the
  entries "must not be interpreted as 35 independent observations". C3 is scored as a cross-check only and never enters the
  overall verdict. Sub-variant C3d: only R <= 26.5 kpc (27 entries), reported.

## 1. The law's Milky Way (construction declared; machinery re-used, not edited)

Solver, McMillan17 baryons, Grid/Model/nu_mono: CFG514's committed file, executed read-only (the part above its
"build the framework / rival" marker), exactly as CFG516 does. CFG516's Base/FieldModel/Mcold_phi/Mcold_v/rho_b2 are executed
read-only from cfg516_mw.py (the part above its "controls" marker). The round cold-energy rule (CFG516, candidate B):
- **RM-v:** M_cold(<r) = r v_law(r)^2/G - M_b(<r), v_law^2 = r nu(|g_N,plane|/a0) |g_N,plane|; spherical cold energy.
- **RM-phi:** M_cold(<r) = Gauss-flux mass of the full QUMOND field minus the baryons' (the phantom's own enclosed mass), spherical.
In-plane circular speed of either: V^2 = R g_N,plane(R) + G M_cold(<R)/R. Both definitions are scored and reported separately;
neither is chosen as the headline (CFG516 found RM-v the more comfortable on the MW RC; that finding is disclosed, not used to pick).
**ALG** (the radial algebraic law V^2 = R nu(g_N/a0) g_N in the plane, CFG513's statistic) is reported as a reference row only.
The census edge (~500 kpc for the MW) is irrelevant inside 50 kpc and is not modelled; no external field (PAPER44).

**Baryons, HELD (never fitted):**
- **B1 census = McMillan 2017** (CFG514's rho_baryon: thin + thick disc + bulge = stars, plus HI + H2 gas). The census stellar
  mass is 5.43 +- 0.57e10 Msun (McMillan17); the grid's own stellar mass is printed and the ratio used for scaling.
- **B2** the record's 6.0e10 (L172 shapes, CFG516's rho_b2) and **B2b** the record's 7.3e10: declared variants, never fitted.

**Post hoc, reported only (never a fit of the law):** the stellar amplitude s* (stars x s, gas fixed, B1) minimising chi^2 on
each curve, bounded s in [0.25, 4]; M*_need = s* x 5.43e10 and z_need = (M*_need - 5.43e10)/0.57e10.

## 2. Comparators (same curves, same errors)

- **NFW:** B1 baryons (Newtonian, held) + spherical NFW with (log10 M200c, c) free (rho_crit from CFG514's H0 = 67.7),
  bounds M200c 1e10-1e13.5, c 1-60. chi^2, p (dof N - 2), M200c, c reported.
- **Kepler:** point mass V = sqrt(G M/R) fitted to the points at R >= 19 kpc (the review's / Jiao's R_kep); chi^2, p (dof n - 1),
  M. The law (each definition, B1, nothing fitted) and NFW are also scored on the same R >= 19 subset for comparison.
- **Newtonian baryons alone** (B1) reported.

## 3. Statistics

- chi^2 = sum ((V_model - V_obs)/sigma)^2 at the tabulated radii; p from the chi^2 survival function with dof = N for the law at
  held baryons (nothing fitted), N - 1 at s*, N - 2 for NFW.
- **Shape:** dlnV/dlnR over 15 <= R <= 27.5 kpc: weighted least squares of ln V on ln R, weights 1/(sigma/V)^2 with the same
  sigma as the chi^2 (primary); sigma_b from the LS covariance. The model's slope is the same fit to the model at the same radii
  with the same weights. Shape consistent if |b_data - b_model| <= 2 sigma_b. Keplerian -0.5 and flat 0 are printed beside it.
  The shape test is NOT DIAGNOSTIC for a curve if 2 sigma_b > |b_law,census - (-0.5)| (it cannot tell the law's shape from
  Keplerian at 2 sigma). Eilers ends at 24.8 kpc; C3 uses the same window (the halo-tracer entries beyond 27.5 do not enter it).

## 4. Verdict rule (per curve x footing x definition; B1 census baryons)

1. **CONSISTENT:** p_census >= 0.01 AND shape consistent at census.
2. else **NEEDS-HEAVY-DISC (z_need sigma vs census):** s* > 1, p(s*) >= 0.01 AND shape consistent at s*.
3. else **EXCLUDED:** p(s*) < 0.01, or shape inconsistent at s* (> 2 sigma_b), or s* at the bound.
4. **NOT DIAGNOSTIC** replaces CONSISTENT when the shape test is not diagnostic (Sec. 3) — i.e. the curve passes but cannot
   separate the law's shape from a Keplerian one. When the amplitude fails, the amplitude verdict (2 or 3) stands, with the shape
   flagged "not diagnostic".
**Overall** (per footing x definition): the worse of C1 and C2 in the order CONSISTENT < NOT DIAGNOSTIC < NEEDS-HEAVY-DISC <
EXCLUDED (largest z_need quoted). C3 is a cross-check: a disagreement with C1/C2 is reported, never folded in.
B2/B2b rows: chi^2, p and shape reported (variant cells), no separate verdict.

## 5. Systematics (each paper's own, as reported; reported rows, a verdict flip is reported as "systematics-dependent")

- **S1 random-only** errors for C1 and C2 (stricter; the authors' systematics removed).
- **S2 upper systematic:** 5% inner (C1 at R <= 22, C2 everywhere), C1 15% beyond 22 kpc kept.
- **S3 R0:** radii rescaled R x R0'/R0_paper for R0' in {8.122, 8.178, 8.34 (Wang+23's)} — crude (velocities not re-derived),
  disclosed as such.
- **Jeans-modelling choices** (Ou's neglected cross-term; asymmetric drift ~15% beyond 22 kpc) enter only through each paper's
  stated systematic budget; nothing is re-derived. Non-equilibrium (Sgr bending waves, LMC, north-south asymmetry) is not modelled.

## 6. Controls and MUTATE

- **K1:** CFG516's chi^2_RC vs Eilers (random ⊕ 2%, CFG514's EIL_E) at B1, A = 1, reproduced to 1% (seen before freezing:
  RM-phi 425.8 / 186.2, RM-v 62.1 / 18.6, canonical / alt).
- **K2:** the C3 parser returns 35 rows spanning 6.3-49.0 kpc.
- **K3:** the slope estimator returns -0.5 (+-1e-6) on an exact Keplerian curve and 0 on a flat one.
- **K4:** the NFW fit improves chi^2 on C1 relative to Newtonian baryons alone.
- **MUTATE** (CFG532_MUTATE=1, separate outputs *_MUTATE.*): (M1) law OFF (Newtonian B1, held): must give p_census < 1e-6 on C1
  and C2 in both footings; (M2) law ON with B1 baryons x 0.5: must give p_census < 1e-6 and a verdict that is not CONSISTENT on
  C1 and C2 in both footings and both definitions. The MUTATE run exits 1 when both fire (DETECTED).

## 7. Gaia DR4 decider (computed, reported)

For each footing x definition and for B1 / B2b and the post hoc s*: the law's V(20), V(25), V(27.5) and slope b_law over
15-27.5 kpc; Keplerian from V(19) of each curve; the slope precision sigma_b(DR4) needed to separate the law from Keplerian at
3 sigma (|b_law - (-0.5)|/3) and from the curves' measured slope at 3 sigma; and the census-baryon amplitude gap at 20 kpc in
km/s. DR4 data release: 2026-12-02.

## 8. Disclosures before freezing (dated 2026-10-09)

Seen before freezing: CFG513 (ALG, L172 6.0e10: chi^2 306/150 vs Ou; 7.3e10: 44/12); hunt_2026 h34 (algebraic law needs
A = 1.36-1.42 on Ou's census, measured outer log-slopes -0.265 +- 0.099 (Ou, stat+sys, 12-27 kpc) and -0.254 +- 0.067 (Eilers),
law slope about -0.15, residual 1.1-1.5 sigma stat+sys); CFG516's RM chi^2 vs Eilers (K1 above); the review's Sections 5-8 and
its tables (slopes, masses, the 35-entry compilation). No number of this lane has been computed.
