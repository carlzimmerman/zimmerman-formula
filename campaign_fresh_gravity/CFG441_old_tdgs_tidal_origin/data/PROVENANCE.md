# CFG441 data provenance

- `tierB_arp72c.csv`: Portilla-Narvaez et al. 2026 (arXiv 2608.18385, A&A accepted), read from the arXiv LaTeX source:
  distance 53.4 Mpc (Sect. 2); i, R_out, v_c from the table "Parameters resulting from the 3D fits" (Arp 72c, HI row);
  M_bary from the table "Results for the dynamical-to-baryonic mass ratio"; age from the table "Properties of the TDGs
  sample" (from Zaragoza-Cardiel et al. 2024). The v_c error is the asymmetric +9/-6 of the 3D-fit table; the script
  uses the mean (7.5 km/s), disclosed.
- `candidates.csv`: every object considered, with the S0-S3 outcome and reason. Sources: Duc et al. 2014 (arXiv
  1403.0626, LaTeX source), Gray et al. 2023 (arXiv 2304.08552, LaTeX source), Portilla-Narvaez et al. 2026,
  Lee-Waddell et al. 2016/2018 (search-result abstracts only; excluded at S1 from the authors' own "young"),
  Lelli et al. 2015 (the repo's real_research/data/tidal_dwarfs/), arXiv 2606.30718 (abstract), Poulain et al. 2022,
  Roman et al. 2021 and Kaviraj et al. 2012 (as summarised inside Gray et al. 2023 / search results; all excluded).
- Forecast F1 inputs (NGC 5557-E1): position, distance 38.8 Mpc, M_* = 1.2 +- 0.7 e8 Msun, R_e = 2.3 kpc from Duc et
  al. 2014 Tables 1-2; host NGC 5557 position from Sesame/Simbad and M_K = -24.87 at 38.8 Mpc from ATLAS3D
  (VizieR J/MNRAS/413/813). The E1 gas mass is NOT tabulated in Duc+2014 (only "HI to visible mass above 50%");
  F1 therefore brackets M_gas, and is a forecast, never a measurement.
