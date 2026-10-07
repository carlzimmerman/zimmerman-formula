# CFG448 fetch log (2026-10-07; fetches approved by the owner for this lane)

Files > 5 MB are git-ignored under `campaign_fresh_gravity/_external_data/cfg448/`; small files are committed in `fetched/`.
Archive queries are position searches around NGC 5557 / E1 (RA 214.6-214.73, Dec +36.49). Empty results are kept as files.

| URL (date 2026-10-07) | bytes | sha256 | stored | used for |
|---|---|---|---|---|
| https://groups.physics.ox.ac.uk/atlas3d/tables/Serra2012_Atlas3D_Paper13_TableB1.txt | 28265 | d6051146a41986366368d4d294c05b19b276b068c058ee8f299678eeab1ca67a | fetched/ | NGC 5557 WSRT noise 0.47 mJy/beam, beam 39.2"x35.9", log M_HI 8.57 (whole field) |
| https://groups.physics.ox.ac.uk/atlas3d/tables/Serra2012_Atlas3D_Paper13.zip | 3707012 | ba72b1b4f020f0b76ec18444fa123235af34c6eb88e04ebd454b23f8514830f2 | _external_data | ATLAS3D WSRT mom0/mom1 maps; NGC 5557 members extracted below |
| (member of the zip) NGC5557_mom0.fits | 650880 | ec755c86fc8a477e163d0370889dd152fea1b8ff17ac3e9c16af1ca032fe938e | fetched/ | masks, fluxes |
| (member of the zip) NGC5557_mom1.fits | 648000 | acf911a8277c417e528d905b5864928f05e3849ef9f0958968d67bedd744990f | fetched/ | velocity gradients |
| https://drive.google.com/embeddedfolderview?id=1wpONQbqNwG55ZX7ehpGQ2OdDZ49ovuFc (folder linked from the ATLAS3D tables page) | 4407 | not kept | scratch | lists allcubes.tar (23 GB), allmom0.tar, allmom1.tar, citation.txt |
| https://drive.usercontent.google.com/download?id=1xznJ5sbxnwrvHtJ4E-GF9uUMkLcLKxDU (allcubes.tar, 24718315520 bytes): 110 tar headers by HTTP range (`cfg448_fetch_wsrt_cube.py`) | 110 x 512 | -- | fetched/allcubes_tar_members.tsv (4684 B, 0bbbc18ddca62c362df54b47e5d0ab3da1065e7151d92b1e0ba22d117a0d87ea) | member list |
| same, range 18378863104 + 215498266 bytes: NGC5557_cube.fits.gz | 215498266 | ca41f74e11672d34dd6bcb77b439299f7cc2afe36044e4a7dcaad85045d2a88b | _external_data | the WSRT HI cube (448 ch x 8.25 km/s, 360x360 x 10") |
| https://data-query.nrao.edu/tap/sync (ADQL obscore, CIRCLE 214.68 36.49 0.3 deg) | 22197 | d934fb2c199d489ffc9f4b295641c1b2605d9929a4c6b05ae0b23dbbdcc0ad68 | fetched/nrao_tap_ngc5557.csv | VLA/EVLA holdings: no HI spectral-line data |
| https://archive.eso.org/tap_obs/sync (dbo.raw, box RA 214.35-215.0, Dec 36.25-36.75) | 58 | 1c23e51508847fad7bec91d5494085e117b7dd6775d11e7750fceb88fc22dd28 | fetched/eso_raw_ngc5557.csv | 0 rows (positive control on another MUSE field returned rows) |
| https://archive.eso.org/tap_obs/sync (ivoa.ObsCore, CIRCLE 214.68 36.49 0.25) | 128 | 0cc195f3e7a0aff000d4c2fa906814a356c66144debf1ce0f4d2056c816c151d | fetched/eso_obscore_ngc5557.csv | 0 rows |
| https://koa.ipac.caltech.edu/TAP/sync (koa_kcwi, CIRCLE 214.68 36.49 0.25) | 49 | cee35d0919823cb9622187728bd03b157e6f2e9515387e3e06e72a4a4c975231 | fetched/koa_kcwi_ngc5557.csv | 0 rows (positive control returned rows) |
| https://vo.astron.nl/tap/sync (apertif_dr1/dr2.spectral_cubes, box 210-220 x 34-39 deg) | 5872 | c33563b5b6229567aeacdbba1411fbc5bcbb263fc6db13cfc525ed804e1de097 | fetched/apertif_dr1_cubes_near.csv | nearest Apertif beam 1.94 deg away; DR2 none |
| https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/other/SCPMA/67.19511/table2&-c=214.7329+36.4825&-c.rm=15&-out.all | 6690 | e19aafabf2da83b8602f9488f88c9d44d2d06ebec31ed3db0f1ea1ec6bd0750a | fetched/fashi_ngc5557_field.tsv | FASHI (FAST) detections of E1, E2, E3: flux, W50, W20 |
| https://archive.gemini.edu/jsonsummary/... | 784 | -- | not kept | refused: login required (owner item) |
| https://ws.cadc-ccda.hia-iha.nrc.ca/argus/sync and https://ws-cadc.canfar.net/argus/sync (CFHT incl. SITELLE) | 0 | -- | -- | unreachable / 404 from this host (owner item) |
| https://archive.nrao.edu/archive/ArchiveQuery | 3882 | -- | not kept | legacy service retired (pointer to data.nrao.edu; TAP used instead) |
| http://export.arxiv.org/api/query?search_query=abs:"NGC 5557" | 10314 | -- | not kept | 3 papers (Duc+2011, Duc+2014, GALFIT-CORSAIR): none with new dwarf kinematics |
| https://api.semanticscholar.org/graph/v1/paper/arXiv:1403.0626/citations | -- | -- | not kept | 77 citing papers by title: none presents NGC 5557 dwarf kinematics |

Web searches (summaries provisional; no number taken from them):
1. NGC 5557 tidal dwarf galaxy kinematics HI MUSE rotation 2020..2026
2. "NGC 5557" Apertif OR MeerKAT OR FAST OR uGMRT HI tidal tail dwarf
