# SCOPING: do observations constrain MOND-on inside dense filament cores? (CFG354 T1)

Scoping only. No script, no result, no data downloaded. kappa = 1/2 is fitted. nu_mono. No DM particle (the cold MASS
is still required). Literature numbers come from arXiv/ADS abstract and ar5iv pages read through a summariser, so they
are **PROVISIONAL** until a person reads the tables. Items marked (S) are summariser-only values.

## The question
CFG354 T1 (l2 >= tau) is ON inside every filament with delta_f >= 2 tau: 3.03 (EdS) or 7.20 (z = 0). That is 1-11%
of a filament cell (Lean S8: every eigenvalue-monotone rule that is ON at a host edge does this). CFG355 found the
rank-2 veto fails KiDS, and pre-crossing filaments are still 0.9-3.1% false ON. The CFG352/354 harness scores only
hosts. **No filament observable has been scored.**

## Repo holdings
`grep -ril filament real_research/data` finds nothing. In campaign_fresh_gravity "filament" appears only in model
cells: CFG243, CFG350, CFG351, CFG353-355, LEDGER, STANDING. **No filament data are in the repo.**

## T1 effect size (order of magnitude; worked in the session scratchpad, not committed)
- Observed line density (lensing, total):
  - Epps & Hudson 2017: M = (1.6 +- 0.3)e13 Msun over 7.1 h^-1 Mpc long and 2.5 h^-1 Mpc wide, so
    mu ~ 2.3e12 Msun per h^-1 Mpc. Check: a uniform cylinder of diameter 2.5 h^-1 Mpc with delta ~ 4 gives the same.
    The h-convention of the mass is unverified.
  - Xia+20 core: 15 +- 4 rho_crit (delta ~ 30-50) inside r_c = 0.4 (+0.2/-0.1) h^-1 Mpc. That gives
    mu_core ~ pi r_c^2 rho_c ~ 2e12 h Msun per h^-1 Mpc. Consistent.
  - Adopted range: mu_tot = 1.6-3.3e12 Msun/Mpc. Baryons: mu_b = 0.157 mu_tot (cosmic f_b).
- Field: an infinite cylinder has g_N = 2 G mu / r, so the Newtonian v_c = sqrt(2 G mu) = 117-168 km/s (total) and
  46-67 km/s (baryons).
- ON region: for the Xia-like profile delta(r) ~ 40 / (1 + r^2/r_c^2), the local delta >= 7.2 out to
  r_ON ~ 0.5-0.85 h^-1 Mpc. T1 reads the enclosed and tangential tide, so this is approximate.
- At r = 0.6 Mpc, on both footings (a0 = 9.36e-11 / 1.13e-10):
  - total field: g_N/a0 = 0.7-1.6e-2, nu = 8-13;
  - baryon field: g_N/a0 = 1.0-2.6e-3, nu = 20-32.
  - At r = 1 Mpc: nu_tot = 11-16, nu_b = 26-41.
- The lensing (dynamical) mass in the core relative to the LCDM-like cold + baryon mass depends on the mass-budget
  convention. The framework does NOT define this for filaments; the branches are never pooled:
  - **A1:** cold + baryons + phantom(baryons): 1 + f_b (nu_b - 1) = **4-6x**.
  - **A2:** the host-harness convention (CFG352: M = M_b + f * dM_ph; no cold term), applied to all baryons:
    f_b nu_b = **3-5x**.
  - **A2':** same convention, with only the detected baryons (~5%; cf. Moffat 2017, de Graaff+19):
    f nu at that f = **~2-2.5x**.
  - **B:** nu applied to the total Newtonian field: **8-13x**.
- External field: end-node halos (~1e13-1e14 Msun at 2-5 Mpc) give g_ext ~ 1e-13 to 1e-12 m/s^2, still well below
  a0. In this regime the EFE linearises the response with G_eff ~ G nu(g_ext) ~ 10-30 G, so the boost stays O(10).
  The EFE does not remove it.
- Stack dilution: stacks average over a width of 1-2.5 h^-1 Mpc and over filaments, some below threshold. A fraction
  of the boost survives. The dilution factor is not computed here and is the first thing a real test must compute.

## Constraint table
| observable (ref) | precision | scale / density probed | T1 effect | could it detect? |
|---|---|---|---|---|
| Stacked filament lensing between BOSS LRG pairs, CFHTLenS: Epps & Hudson 2017 (arXiv 1702.08485) | 5 sigma; M = (1.6 +- 0.3)e13 (19%). The 3-pt (Clampitt+14) LCDM model overestimates the data by ~1.6 (S) | z ~ 0.42; R_sep 6-10 h^-1 Mpc; 2.5 h^-1 Mpc wide; mean delta ~ 4, so the CORE is inside the T1 regime and the outskirts are not | A1/A2 3-6x, B 8-13x in the core, diluted in the aperture | Yes for factors >~ 2 after dilution. The measured level is at or below the LCDM model, not above it |
| Same, SDSS LRG pairs: Clampitt+16 (arXiv 1402.3302) | 4.5 sigma; shear < 1e-4. Matches the "thick" LCDM simulated filament and disfavours "thin" | z ~ 0.25; R_sep 6-14 h^-1 Mpc | same | Marginal-yes: ~22% amplitude error; no Sigma value in the abstract |
| KiDS + RCSLenS + CFHTLenS: Xia+20 (arXiv 1909.05852) | 3.4 sigma; core Sigma amplitude 10.5 +- 2.9 h Msun/pc^2 vs SLICS LCDM 5.61 +- 0.55 (S), ratio ~1.9 +- 0.5 | z ~ 0.30; R_sep 3-5 h^-1 Mpc; central 15 +- 4 rho_crit, r_c 0.4 h^-1 Mpc: squarely the delta_f >~ 7 core | same | Yes for factors >~ 3 (excluded at >~ 2 sigma if diluted little); a factor ~2 is allowed. The ratio leans HIGH, not a detection |
| BOSS CMASS pairs, HSC Y1: Kondo+20 (arXiv 1905.08991; the "Yang+20" in the request is not this paper) | 3.9 sigma; "consistent with theory, thick model" | z ~ 0.55 | same | Marginal; amplitude ratio not in the abstract |
| Intercluster bridges, LoVoCCS/DECam: Shinde & Dell'Antonio 2025 (arXiv 2510.26318) | 4-7.3 sigma per filament; kappa0 0.015-0.053; h_c 0.11-0.45 Mpc | z < 0.1; A401/399, A2029/2033, A3558/3556: dense bridges, ON, but with strong EFE from the clusters | Bridge lensing / gas mass vs 1/f_b = 6.4 | Possibly, as a per-system test. Needs the bridge gas mass (published X-ray/SZ for A399-A401) |
| DES Y3 density-ridge lensing: Nikjoo+26 (arXiv 2603.04025) | "high significance", not independent of galaxy-galaxy lensing | photometric ridges, mixed densities | diluted | Not in its current form |
| tSZ, Planck y between LRG pairs: Tanimura+19 (arXiv 1709.05024) | 5.3 sigma; Delta y = (1.31 +- 0.25)e-8 vs sims (0.84 +- 0.24)e-8; delta_c T_7 (r_c/0.5) = 2.7 +- 0.5 | z < 0.4; 6-10 h^-1 Mpc | none direct: tSZ measures gas pressure, and WHIM T is set by shocks, not hydrostatics | No. Gas only, unless a hydrostatic assumption is added; it is not valid for the WHIM |
| tSZ, CMASS pairs: de Graaff+19 (arXiv 1709.10378) | 2.9 sigma; y = (0.6 +- 0.2)e-8; rho_b = (5.5 +- 2.9) mean; T = (2.7 +- 1.7)e6 K | z 0.43-0.75 | none direct; fixes mu_b for branch A2' | No (input to the budget only) |
| X-ray, eROSITA eRASS:4, 7817 SDSS filaments: Zhang+24 (arXiv 2406.00105) | 9 sigma total, 5.4 sigma WHIM; log T = 6.84 +- 0.07; log Delta_b = 1.88 +- 0.18 (matches TNG) | the X-ray-bright, dense phase (Delta_b ~ 76): core regime | none direct | No (gas state, not mass). An isothermal-cylinder reading needs mu ~ 2 c_s^2/G ~ 4e13 Msun/Mpc, about 10x the lensing mu. WHIM is not hydrostatic, so it is NON-DIAGNOSTIC; do not read it as a boost |
| Galaxy transverse velocities, filament "spin", SDSS DR12 Bisous: Wang+21 (arXiv 2106.05989); MeerKAT HI filament: Tudorache+25 (arXiv 2508.13053) | peak ~100 km/s at ~1 Mpc, falling to 0 beyond ~2 Mpc; 4.2 sigma best subsample | delta ~ few, 1-2 Mpc | MOND-on would raise the support velocity by sqrt(nu) ~ 3-6x (to 400-700 km/s) | Not as published: vorticity is not a virial measure. A filament velocity-dispersion stack could be |
| Modified gravity in filaments: Moffat 2017 (arXiv 1705.03106, MOG) | theory note | Epps & Hudson-type lensing | MOG replaces the cold mass; T1 adds to it | Shows the budget convention decides the sign. The only filament-specific modified-gravity paper found; none for MOND or this framework |

## Bottom line: (ii), with a strong lean that the test would bite
- **Lensing stacks.** The published stacks (Epps & Hudson 2017; Xia+20; Clampitt+16; Kondo+20) measure filament
  lensing at or near the LCDM cold + baryon level. The ratios are ~0.6 and ~1.9 +- 0.5, with 20-30% amplitude
  errors. They probe the delta >~ 7 core regime where T1 fires.
- **What T1 implies.** Under every budget branch, T1 with MOND-on implies a 2-13x core boost.
- **Why this is not yet (i).**
  - The framework has not defined the filament mass budget (A1/A2/A2'/B).
  - The aperture and threshold dilution is not computed.
  - The published amplitudes are LCDM-model fit parameters.
- **What the numbers suggest.** If the dilution is mild, branches A1, A2 and B overshoot the stacks. That points
  AGAINST MOND-on in filament cores, i.e. against T1's (a') behaviour. A2' (detected baryons only, ~2x) is not
  excluded. This is a lean, not a result.
- **Defined test (a new CFG lane needs the owner's go, and downloads need an explicit yes in the calc chat):**
  1. Freeze the budget branch.
  2. Take an LCDM N-body filament stack. CFG354's growth pass makes the cold field LCDM-like.
  3. Apply T1's ON map and nu_mono at both footings, with the CFG355 smeared width.
  4. Project with the Epps & Hudson and Xia+20 pair selections.
  5. Score against their Sigma(R) points.
- **Tables needed:**
  - The Epps & Hudson Fig. Sigma/kappa profile and the Xia+20 Sigma(r) points. Published figures only; it is unknown
    whether they are tabulated (ask the authors or digitise).
  - Or a re-stack from public catalogues: BOSS DR12 LRG/CMASS (public), CFHTLenS / KiDS-1000 / HSC-PDR shear
    (public), the Tempel+14 Bisous filament catalogue (VizieR, public).
  - The bridge test needs the A399-A401 gas mass (published) with the Shinde & Dell'Antonio kappa0 (abstract-level
    only).
- **Not sensitive:** tSZ, X-ray and the filament-spin kinematics as published. They fix the gas budget only.

Sources (abstract/HTML pages): arxiv.org/abs/1702.08485, 1402.3302, 1909.05852, 1905.08991, 2510.26318, 2603.04025,
1709.05024, 1709.10378, 2406.00105, 2106.05989, 2508.13053, 1705.03106.
