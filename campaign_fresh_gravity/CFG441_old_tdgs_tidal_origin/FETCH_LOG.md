# CFG441 fetch log (2026-10-06; fetches approved by the owner for this lane)

Large arXiv source tarballs (> 5 MB or near it) are stored git-ignored under `campaign_fresh_gravity/_external_data/cfg441/`
(extracted there too); small files are committed in `fetched/`.

| URL | bytes | sha256 | stored | used for |
|---|---|---|---|---|
| https://arxiv.org/e-print/1403.0626 | 5913158 | badc4f1a16970959b8b13f1fc86010533a91726789fe54a2aa3cff5c6c1e2b1f | _external_data | Duc+2014 NGC 5557 TDGs: Tables 1-2, kinematics section (S2 FAIL), age section, F1 inputs |
| https://arxiv.org/e-print/1510.07206 | 5556783 | f093b60ce3ff7320a4ec624f9ce37fd22c626a8e52145b9943f06e7e57b68fe7 | _external_data | Lee-Waddell+2016 DEIMOS (abstract read; young star-forming TDG candidates; not used) |
| https://arxiv.org/e-print/2304.08552 | 22128177 | c15500d7a870cbf9ef07058c8925a9b20e5373de66dbbeeb504d533d8aa0c290 | _external_data | Gray+2023 ALFALFA almost-dark TDG candidates: origin and travel-time sections (S0 FAIL) |
| https://arxiv.org/e-print/2605.17253 | 4630271 | 50592734ce7dd0a8685af466f53c35694cd582d94ae2ac7fd83e66f5e7a31bdc | _external_data | uGMRT baryon-dominated dwarfs (abstract read; no tidal-origin evidence; not a TDG sample) |
| https://arxiv.org/e-print/2608.18385 | 8603495 | 9d85ccb6233da04e88904dbbb9c41727e2e272b371313044375499b30d36f6e4 | _external_data | Portilla-Narvaez+2026 Arp 72 TDGs: age, 3D-fit and mass tables (Arp 72c Tier B) |
| https://export.arxiv.org/abs/2609.10700 | 45728 | 9a94509be567b295e9850a1825a6ee2d3c42a528ebb106d7c52ec50d9f572873 | fetched/ | LEWIS UDG kinematics (puffed-up dwarfs, not tidal; not used) |
| https://export.arxiv.org/abs/2603.24020 | 46233 | ad189e9b57937c035913bc5421ec2c918a0e5fb4bc85e2e2207de69af3053f43 | fetched/ | N-body break radii of stripped satellites (no data; not used) |
| https://export.arxiv.org/abs/2606.30718 | 44889 | 0d09524bfb3456ea134967fc45dfa3048eb2dc7a1142aca83c3547fdbcce630e | fetched/ | NGC 1052 merger-TDG origin model for DF2/DF4 (Tier C note) |
| https://api.crossref.org/works/10.1051/0004-6361/202450349 | 25742 | a2e60472f8767d112934fe42b6840fe0b05426423528c44f994e51bfa1e3e71a | fetched/ | identifies Zaragoza-Cardiel+2024 (detached TDGs; source of the Arp 72 ages) |
| https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/413/813/atlas3d&Galaxy=NGC5557&-out.all | 94149 | 9b546519f759195d26ff0da4e7e89eaf2326b6ff20fe55b3ec87a08d4b84a2f5 | fetched/ | ATLAS3D table (filter not applied: whole table returned); NGC 5557 M_K = -24.87, D = 38.8 Mpc |
| https://cds.unistra.fr/cgi-bin/nph-sesame/-oI/SNV?NGC%205557 | 1001 | 2a72223e4a342a53f419135143c55e86e5f94994f3b47d7a4031eff97d7b5cd4 | fetched/ | NGC 5557 position (F1 projected distance) |

Web searches (WebSearch tool; result summaries are provisional and no number was taken from them):
1. old tidal dwarf galaxy candidates HI kinematics rotation dynamical mass
2. Duc 2014 NGC 5557 old tidal dwarf galaxies 4 Gyr
3. "old tidal dwarf" galaxy dynamical mass dark matter content velocity dispersion MUSE OR "HI" 2018..2026
4. tidal dwarf galaxy several Gyr old candidate rotation curve dark matter deficient early-type host shells
5. MATLAS tidal dwarf galaxy candidates HI kinematics early-type galaxies Duc Poulain old TDG
6. tidal dwarf galaxy formed 1-3 Gyr ago merger remnant HI rotation velocity baryonic Tully-Fisher Newtonian
7. "fossil" tidal dwarf galaxy stellar velocity dispersion dynamical mass-to-light ancient tidal origin confirmed
8. Lee-Waddell 2018 AGC 208457 tidal dwarf metallicity HI kinematics NGC 3166
9. tidal dwarf galaxy completed several orbits dynamical equilibrium HI rotation old interaction dark matter test MOND
10. Kaviraj 2012 tidal dwarf galaxies Stripe 82 old TDG candidates kinematics follow-up

Exclusions resting only on a search summary (not a table): AGC 208457 (S1, from its authors' "young tidal objects"
title), MATLAS candidates (no age, no resolved kinematics), HCG 16-LSB1 (as summarised in Gray+2023's LaTeX), Kaviraj+2012
(photometric). Each would also have to pass S1 and S3, which none is reported to.
