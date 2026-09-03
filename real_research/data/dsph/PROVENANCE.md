# dSph sample provenance

`mcconnachie2012_dsph.csv` — extracted 2026-07-30 by direct VizieR query, NOT typed from memory:

    https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/144/4/catalog&-out.max=500&-out.all

Source catalogue: **McConnachie 2012, AJ 144, 4** — "The Observed Properties of Dwarf Galaxies in
and around the Local Group" (VizieR J/AJ/144/4/catalog). 102 rows returned; 46 retained as having
all three of stellar velocity dispersion (`sigma*`), half-light radius (`R2`, pc) and absolute
V magnitude (`VMag`).

Columns kept: `Name, SubG, D (kpc), VMag, R2 (pc), sigma* (km/s), e_sigma* (km/s), M.HI (1e6 Msun)`.

Public catalogue data. No personal information.

---

## Added 2026-09-03 for hunt items 43 / 44 (`hunt_2026/h43_h44_ufd_m31_sigma.py`)

`lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv`, `lvd_dwarf_local_field.csv` — the **Local Volume Database**
(Pace 2024, ApJS 273, 15; `doi:10.3847/1538-4365/ad9f2c`), downloaded 2026-09-03 from

    https://raw.githubusercontent.com/apace7/local_volume_database/main/data/dwarf_mw.csv
    https://raw.githubusercontent.com/apace7/local_volume_database/main/data/dwarf_m31.csv
    https://raw.githubusercontent.com/apace7/local_volume_database/main/data/dwarf_local_field.csv

This is the maintained compilation that supersedes (and includes the references of) the Simon 2019
ARA&A ultra-faint table named in hunt item 43: 68 MW satellites (45 with a measured
`vlos_sigma`), 43 M31 satellites (34 measured), 64 local-field dwarfs (13 measured).  Columns used:
`M_V, rhalf_physical, rhalf_sph_physical, ellipticity, vlos_sigma(+/-, _ul), distance, distance_gc,
distance_host, mass_stellar, mass_HI, ra, dec`.  `mass_stellar` is log10(M*/Msun) at Upsilon_V = 2.

`collins2013_m31_dsph.tsv` — **Collins et al. 2013, ApJ 768, 172** (VizieR J/ApJ/768/172/dsph),
the source named in hunt item 44, downloaded 2026-09-03 from the CfA VizieR mirror:

    https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/768/172/dsph&-out.max=200&-out.all

18 M31 dSphs with VMag, rh (pc), Dist (kpc), sigV (km/s) and its asymmetric errors.  Four rows carry
sigV = 0.0 (dispersion unresolved) and are treated as upper limits, not measurements.

Public catalogue data.  No personal information.
