# Virgo dwarf early-type galaxies — provenance

`toloba2014_smakced_dEs.csv` — extracted 2026-09-03 for hunt item 45 (`hunt_2026/h45_virgo_de.py`) from the
**authors' own LaTeX tables** in the arXiv source package of

> **Toloba et al. 2014, ApJS 215, 17** — "Stellar Kinematics and Structural Properties of Virgo Cluster
> Dwarf Early-type Galaxies from the SMAKCED Project. II." — arXiv:1410.1550

    curl https://arxiv.org/e-print/1410.1550   ->  dEs_parameters_table.tex, masses_table.tex

The catalogue is NOT in VizieR (checked: J/ApJS/215/17 and J/ApJ/799/172 both return nothing from the CfA mirror),
which is why the tables were parsed from the paper source rather than downloaded.

39 Virgo dEs.  Columns: `name, ra, dec, M_r, Re_r_arcsec, M_H, Re_H_arcsec, morph, Vrot, e_Vrot, sigma_e,
e_sigma_e, sigma_avg, e_sigma_avg, logMe_pub, fDM_pub, e_fDM_pub`.  Magnitudes are AB.

**Data-integrity note found while extracting (verified numerically in `h45_virgo_de.py`, checks 45-D1/45-D2):**
in `masses_table.tex` the stellar-mass column `log M_e^*` is ordered by *increasing stellar mass* while the
galaxy-name column is ordered by *VCC number*, so joining that column by name mismatches by up to 0.9 dex.
The `log M_e` and `f_DM` columns ARE name-consistent.  This file therefore carries only `logMe_pub` and
`fDM_pub` from that table; stellar masses are recomputed from `M_H` with the paper's own
(M/L)_H = 0.73 ± 0.19, which reproduces the published `f_DM` galaxy by galaxy to 0.012 dex and reproduces
the published `log M_e^*` value set to 0.013 dex once both are sorted.

Public catalogue data.  No personal information.
