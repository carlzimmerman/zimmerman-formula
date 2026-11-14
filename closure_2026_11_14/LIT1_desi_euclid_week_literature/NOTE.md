# LIT1: literature sweep for this week's DESI and Euclid releases (2026-11-14)

Owner asked: search every publication tied to this week's DESI and Euclid
releases; find anything crisp and useful; check nothing is being scooped or
reverse engineered. Three Opus web sweeps (arXiv API / abstract pages, Zenodo
API, web search), window about 2026-10-20 to 2026-11-14. Look-ups are
PROVISIONAL (summariser risk); open the abstract before citing any number.
Adopts nothing; no row of the scorecard changes from this note.

## Priority check: risk LOW

- No paper found gives a0 = (c/2) sqrt(G rho_DE), a0 tracking rho_DE(z), or a
  screened Khronon form; none cites the Zenodo DOIs (Zenodo exact search for
  10.5281/zenodo.24106866: 0 hits). Limit: arXiv has no full-text citation
  search; no Google Scholar access.
- Read in full (prior art, opposite direction, likely worth citing):
  Galaxies 14(5):90 (Oct 2026) = Preprints.org 202606.1623, "Plausible
  Sources of Dark Energy and Associated Vacuum Properties: Implications for
  Newton's G, MOND's a0 ..." (authors not confirmed; probably Christodoulou and
  Kazanas, line of work from arXiv:1905.04296). Derives the dark-energy
  density from a0 in a varying-G picture. MDPI / Preprints returned 403:
  coefficient and citations not checked.
- Horizon / H0 ties only (common since Milgrom): Escala arXiv:2608.10073
  (a0 ~ c/t_u, predicts BTFR evolution); Uruena Palomo arXiv:2610.09987;
  Nash arXiv:2608.19245 (qualitative).
- Nothing tests MOND / Khronon / AeST / emergent gravity on ECLIPSE lenses,
  DESI P1D or Euclid galaxy-galaxy lensing.

## DESI (no DR2 public data; DR1 still the latest public release)

- arXiv:2611.05518 (11-03) DESI DR2 Results III, mass of the Milky Way:
  10,036 RRL + BHB, 10-95 kpc, four methods, mock-corrected;
  M(<80 kpc) = 6.36 (+0.53/-0.48)e11 Msun (v_c = sqrt(GM/r) = 185 km/s,
  checked in SI here), M200c = 1.19e12. Companions 2611.05521 (Medina, GME;
  BHB 0.64 vs RRL 0.53e12 at 80 kpc; Sgr lowers ~10 %), 2611.05520 (Zhou,
  emPDF), 2611.05519 (Riley, AuriDESI mocks on Zenodo: the equilibrium-bias
  correction to red-team). Independent 2611.15560 (Li, LAMOST+SDSS+DESI):
  M(<82) = 4.7e11, about 25 % lower. -> MW halo rows (RRL1 / RRL2 / RB1).
- Evolving DE survives: 2611.13829 (Kolonia, covariance inflation, w0wa
  3.15 -> 3.07 sigma); 2611.01505 (Barua, rho_DE(z) shape depends on the
  parameterisation; Bayes factor weakly ΛCDM); 2610.40785 (Herold,
  model-free acceleration from DR2 BAO).
- Neutrino floor: 2610.33729 (still negative effective mass in interacting
  models); 2611.14584 (coupled quintessence relieves it).
- Growth: 2611.15881 (Cortes, gamma = 0.633 +/- 0.024 in a w0wa background,
  3.4 sigma from GR; fsigma8-driven).
- No new DESI P1D, warm-DM, group catalogue, or Son et al. age-bias paper.

## Euclid DR1 (A&A special issue batch, arXiv 11-11 / 11-12)

- 2611.16510 (Aussel, release overview): DR1-Foundation has NO shear
  catalogue; shear and Level 3 products in June 2027. Euclid weak-lensing,
  lensing RAR and splashback tests cannot be done before then.
- 2611.15877 (Nersesian, ECLIPSE D): stellar mass from flux summed inside the
  circular lens-modelling mask, stated as a lower limit (worst for Sersic
  n > 9.5); lens dust not modelled; Einstein radii about 0.3 dex above SLACS
  at fixed M* (about 0.1 dex from SLACS selection). Independent confirmation
  of the in-mask-mass trap behind EUC17 / EUC19.
- 2611.15888 (Nightingale, ECLIPSE C): SIE + shear models; grade A 67.5 %
  success; use the success class only; profile shape is model-limited.
- 2611.15886 (ECLIPSE B): completeness 0.73 (A), 0.34 (A+B).
- 2611.15883 (ECLIPSE A): 15,072 A+B; median log M* 11.39, z_d 0.68,
  theta_E 0.85".
- 2611.15891 (Bergamini): NISP source redshifts for 4 systems only.
- 2611.00224 (Sonnenfeld, Q1): selection-corrected total mass inside
  5/h kpc, log M5 = 11.30 +/- 0.02 at L_r = 10^10.7, slope L^0.71. Cleanest
  lens number for a frozen fixed-a0 prediction (needs an M*/L prior).
- 2611.15987 (photo-z): below requirements at I_E < 24.5; cut at 24.
- 2611.16025 (Gatto): 15 low-surface-brightness systems (Fornax 7, M81-group
  dwarfs); no kinematics yet.

## Other useful external tests seen

- Combes arXiv:2611.08702: MOND in 106 X-ray clusters, residual missing mass
  about half the gas mass, concentrated in 20-30 kpc of cool cores
  (cluster rows).
- MUSE-DARK arXiv:2604.22613: fitted acceleration scale rises with z
  (a0(z) = a0(0) + a1 z); a direct a0(z) comparison.
- Apertif arXiv:2610.20718 (568 HI curves), MIGHTEE arXiv:2608.03576 (RAR to
  z ~ 0.09): fresh RAR samples not used to fit the law.
- Chae et al. arXiv:2610.40388 vs Saad and Ting (wide binaries).
- Zenodo 10.5281/zenodo.24202464 (Canac, 11-13): MW V(30 kpc) prediction
  ahead of Gaia DR4.

## Candidate lanes (not launched)

1. MW mass profile: law vs DESI DR2 M(<r) at 50 / 65 / 80 / 100 kpc, with
   the RRL-BHB and DESI-vs-LAMOST spread as the bracket; red-team the
   AuriDESI equilibrium correction.
2. Sonnenfeld Q1 M5(L, z): frozen fixed-a0 prediction of mass inside 5/h kpc.
3. Combes residual cluster mass vs form B on X-COP.
4. MUSE-DARK a0(z) vs a0 tracking rho_DE(z).
