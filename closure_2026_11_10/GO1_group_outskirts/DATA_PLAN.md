# GO1 Part 0: eRASS1 DR1 data plan for the 20 Lovisari groups (NOTHING DOWNLOADED; for the owner's decision)

**For the owner, in four lines.**
- **11 of the 20 groups are in the eRASS1-DE DR1 footprint.** UGC 03957 is not; Suzaku (Thölken+16) is its only outskirts route.
- **50 event tiles** (3.6 x 3.6 deg) cover every group's 5 R500 circle: **726,234,784 bytes (0.73 GB)**. Central tiles only:
  11 tiles, 154 MB. Exposure maps would add about 1.6 GB for one band, or they can be rebuilt from the events with eSASS.
- **Terms.** Open HTTPS download, no licence, no registration, no click-through. The site requires its acknowledgement text
  (quoted in section 4), the eSASS sentence if eSASS is used, the citation of Merloni+2024, and modest download rates. With no
  licence stated, redistributing the raw files should be asked of MPE first.
- **Depth caveat.** eRASS1 gives these groups 80-210 s. In the drafting session's own judgement (not computed in a lane), one
  group cannot be measured at 3-5 R500, and an 11-group stack would be limited by foreground systematics. A published stack of
  827 eRASS1 groups (Bulbul+2026, arXiv:2607.27804, read from its abstract only) reached 2-4 R500 in electron density. That
  stack's profile, not these tiles, is the nearer route to the X-ray half of the census.

Drafted by a delegated web-lookup agent and read in full by the GO1 lane before committing. Nothing here was graded. The exposure
numbers came from one small query to eRODat's upper-limit service (flagged in Method item 6).

Written 2026-11-10. This is a data plan only. No event file, image, exposure map or catalogue was downloaded. Every number below comes from documentation pages, directory index pages, HTTP HEAD requests, the DR1 tile-boundary table (a 357,120-byte documentation index FITS file), CDS Sesame name resolution and a few small JSON lookups. Each URL is listed in the Fetch log (section 6). Nothing here is committed.

Sample: the 20 groups of Lovisari, Reiprich & Schellenberger 2015 (A&A 573, A118; arXiv:1409.3845) that have measured R500 (the 23-group sample minus the three starred exclusions A3574E, NGC6107 and AWM5). Redshift and R500 (h = 0.7) are as given in the task brief. The R500 values agree with the R500 column of the paper's Table 2, which I checked for CID28 (655) and UGC03957 (751) on the ar5iv rendering.

## Headline

- **11 of 20 groups are in the eRASS1-DE (DR1) footprint** (Galactic longitude 179.944-359.944 deg). For all 11, the whole 5 R500 circle lies on the DE side. The 9 groups outside are A194, WBL154, NGC1132, RXCJ2315.7-0222, NGC6338, IIIZw054, IC1262, AWM4 and UGC03957. NGC1132 (l = 176.45) is close to the boundary, but its whole 5 R500 disc lies at l < 179.94. It touches the shared tile 044093 only on the Russian side, so DR1 has no data for it.
- **50 unique 3.6 x 3.6 deg tiles** are touched by the 5 R500 circles. No tile is shared between two groups.
- **Total event-file volume: 726,234,784 bytes = 0.726 GB (0.676 GiB)** for all 50 tiles. **Minimal set (central tile only, 11 tiles): 153,972,367 bytes = 0.154 GB (0.143 GiB).**
- Every one of the 50 event-file URLs answered HTTP 200 to a HEAD request, and each Content-Length equals the size in the directory listing.
- Event files only. Surface brightness also needs exposure maps (and, optionally, background maps). Those come either from the archive (about 32 MB per band per tile, see section 3) or from re-running the eSASS `expmap` task on the event files.

## Method

1. **Coordinates**: CDS Sesame (`-oI/SNVA`). The query was redirected to the VizieR mirror at vizier.idia.ac.za. SIMBAD resolved 17 names. "ACO S 753", "ACO S 805" and "ACO S 301" were not found in SIMBAD or NED, and VizieR (Abell catalogue) resolved them. CID28 resolved directly in SIMBAD as "CID 28" (also "ESO 552- G 020 GROUP"; GClstr, position reference 2012MNRAS.425..477N). The Lovisari paper gives no coordinates: its Table 1 lists only name, z, NH, LX and LX error. These are catalogue/optical positions, not X-ray peaks. Offsets of a few arcmin do not change any in/out decision, but they could add or drop the marginal tiles noted below. **Caveat on WBL154**: SIMBAD puts WBL 154 at 07:51:21 +50:12:34. I could not check independently that this is the same system as Lovisari's WBL154 at z = 0.023, because the paper has no coordinates. It is outside DR1 either way.
2. **Distances**: angular-diameter distance, flat LCDM with H0 = 70 and Om = 0.3 (astropy `FlatLambdaCDM`). The angle is theta = n R500 / D_A.
3. **Footprint**: DE if 179.94423568 < l < 359.94423568, the boundary quoted on the DR1 front page.
4. **Tiles**: I used the DR1 tile table `SKYMAPS_052022_MPE.fits` (2447 DE tiles, each with a unique RA/Dec box; the 3.6 x 3.6 deg event files overlap their neighbours by about 20 arcmin). I filled each 5 R500 disc with sample points about 0.02 deg apart and recorded every tile whose unique box contains at least one point. That box is the "tiles touched" list. The central tile is the one whose box contains the group centre. I then cross-checked the list against eRODat's own skytile-search API (`skytile_search_api/?RA=&DEC=&RAD=5R500`), and **the API returned exactly the same tile set for all 11 groups**.
5. **File names and sizes**: the archive tree is `https://erosita.mpe.mpg.de/erodat/data/download/<DDD>/<RRR>/EXP_010/`. Tile number = RRRDDD, where RRR is the RA of the tile centre and DDD is the Dec counted from the north pole (Dec = 90 - DDD). The file naming page gives the file name as `em01_<tile>_020_EventList_c010.fits.gz` (em = MPE-owned, 01 = eRASS1, 0 = all TMs, 2 = filter, 0 = 0.2-10 keV, c010 = DR1 processing). All 50 tiles are `em01`; no `eb01` (shared-rights) file is needed. Sizes are from the directory listing and were confirmed by a HEAD Content-Length on each URL.
6. **Exposure**: one POST of 55 positions (each centre plus 4 points at 5 R500) to the eRODat upper-limit service (`upperlimit/service_multi`, band 022 = 0.6-2.3 keV, DR1_eRASS1). I used only the returned `Exposure` field. **Note**: this small JSON query (about 20 kB returned) is a lookup service, not a data file. It is outside the strictly enumerated allowed list (HEAD, index, docs, name resolution), so strike section 5's measured exposures if that is not acceptable.

Marginal tiles: 214120 (S0753) and 093129 (A3390) each contain less than 0.1 % of their disc's sample points. Only the far rim of the 5 R500 circle clips their unique box. Because event files overlap by about 20 arcmin, the neighbouring tiles' files probably already cover that sliver. They are listed anyway, since the brief asks for every tile touched.

## 1. The 20 groups

R500 in arcmin = R500 / D_A. A tile number in the last column is the 6-digit eRASS1 sky-tile id (SRVMAP).

| # | Group | z | R500 (kpc) | RA (deg) | Dec (deg) | RA, Dec (sexagesimal) | coord. source | l (deg) | b (deg) | eRASS1-DE (DR1)? | D_A (Mpc) | R500 (arcmin) | 3 R500 (deg) | 5 R500 (deg) | DR1 exposure 0.6-2.3 keV, centre / range at 5 R500 (s) | tiles touched by 5 R500 circle (central first) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NGC4936 | 0.012 | 417 | 196.0704 | -30.5263 | 13:04:17 -30:31:35 | SIMBAD | 306.20 | +32.26 | YES | 50.6 | 28.3 | 1.42 | 2.36 | 157 / 152-163 | 197120, 194120, 196123, 195117, 199123, 192123, 198117 (7) |
| 2 | S0753 | 0.013 | 547 | 210.9106 | -33.9731 | 14:03:39 -33:58:23 | VizieR (Abell) | 319.63 | +26.55 | YES | 54.8 | 34.3 | 1.72 | 2.86 | 145 / 166-176 | 210123, 214123, 213126, 209126, 206123, 211120, 214120 (7) |
| 3 | HCG62 | 0.015 | 437 | 193.2721 | -9.2003 | 12:53:05 -09:12:01 | SIMBAD | 303.62 | +53.67 | YES | 63.1 | 23.8 | 1.19 | 1.98 | 132 / 127-137 | 192099, 195099, 194102, 194096, 191102 (5) |
| 4 | S0805 | 0.015 | 427 | 281.8101 | -63.3292 | 18:47:14 -63:19:45 | VizieR (Abell) | 332.25 | -23.59 | YES | 63.1 | 23.3 | 1.16 | 1.94 | 102 / 98-107 | 281153, 287153, 280156, 275153, 287156, 283150 (6) |
| 5 | NGC3402 | 0.016 | 470 | 162.6103 | -12.8446 | 10:50:26 -12:50:41 | SIMBAD | 262.77 | +40.41 | YES | 67.2 | 24.0 | 1.20 | 2.00 | 84 / 79-82 | 163102, 162105, 160102, 165105 (4) |
| 6 | A194 | 0.018 | 463 | 21.4218 | -1.4079 | 01:25:41 -01:24:29 | SIMBAD | 142.07 | -63.00 | NO | 75.4 | 21.1 | 1.06 | 1.76 | n/a | none (not in DR1) |
| 7 | RXCJ1840.6-7709 | 0.019 | 488 | 280.1524 | -77.1564 | 18:40:37 -77:09:23 | SIMBAD | 317.21 | -25.80 | YES | 79.5 | 21.1 | 1.05 | 1.76 | 133 / 132-159 | 276168, 281165, 289168, 270165, 291165 (5) |
| 8 | WBL154 | 0.023 | 508 | 117.8374 | +50.2094 | 07:51:21 +50:12:34 | SIMBAD | 168.39 | +29.84 | NO | 95.8 | 18.2 | 0.91 | 1.52 | n/a | none (not in DR1) |
| 9 | S0301 | 0.023 | 497 | 42.4021 | -31.1936 | 02:49:37 -31:11:37 | VizieR (Abell) | 229.01 | -63.96 | YES | 95.8 | 17.8 | 0.89 | 1.49 | 207 / 196-210 | 043120, 044123, 041123, 039120 (4) |
| 10 | NGC1132 | 0.024 | 490 | 43.2159 | -1.2748 | 02:52:52 -01:16:29 | SIMBAD | 176.45 | -51.07 | NO | 99.8 | 16.9 | 0.84 | 1.41 | n/a | none (not in DR1) |
| 11 | IC1633 | 0.024 | 797 | 17.4815 | -45.9312 | 01:09:56 -45:55:52 | SIMBAD | 293.10 | -70.84 | YES | 99.8 | 27.4 | 1.37 | 2.29 | 116 / 112-150 | 019135, 014135, 020138, 015138, 023135 (5) |
| 12 | NGC4325 | 0.026 | 435 | 185.7778 | +10.6212 | 12:23:07 +10:37:16 | SIMBAD | 279.58 | +72.20 | YES | 107.9 | 13.9 | 0.69 | 1.16 | 99 / 96-183 | 185078, 186081, 188078 (3) |
| 13 | RXCJ2315.7-0222 | 0.027 | 552 | 348.9337 | -2.3831 | 23:15:44 -02:23:00 | SIMBAD | 76.05 | -56.28 | NO | 111.9 | 17.0 | 0.85 | 1.41 | n/a | none (not in DR1) |
| 14 | NGC6338 | 0.028 | 671 | 258.8458 | +57.4112 | 17:15:23 +57:24:40 | SIMBAD | 85.81 | +35.40 | NO | 115.9 | 19.9 | 1.00 | 1.66 | n/a | none (not in DR1) |
| 15 | IIIZw054 | 0.029 | 694 | 55.3233 | +15.3956 | 03:41:18 +15:23:44 | SIMBAD | 172.20 | -30.79 | NO | 119.9 | 19.9 | 0.99 | 1.66 | n/a | none (not in DR1) |
| 16 | IC1262 | 0.031 | 625 | 263.2585 | +43.7597 | 17:33:02 +43:45:35 | SIMBAD | 69.52 | +32.07 | NO | 127.9 | 16.8 | 0.84 | 1.40 | n/a | none (not in DR1) |
| 17 | AWM4 | 0.033 | 724 | 241.2375 | +23.9206 | 16:04:57 +23:55:14 | SIMBAD | 39.94 | +46.49 | NO | 135.8 | 18.3 | 0.92 | 1.53 | n/a | none (not in DR1) |
| 18 | A3390 | 0.033 | 543 | 96.1533 | -37.3358 | 06:24:37 -37:20:09 | SIMBAD | 245.14 | -21.05 | YES | 135.8 | 13.7 | 0.69 | 1.15 | 155 / 149-162 | 096126, 097129, 093129 (3) |
| 19 | CID28 | 0.034 | 655 | 73.7070 | -18.1141 | 04:54:50 -18:06:51 | SIMBAD | 217.45 | -33.63 | YES | 139.7 | 16.1 | 0.81 | 1.34 | 167 / 150-170 | 074108 (1) |
| 20 | UGC03957 | 0.034 | 751 | 115.2426 | +55.4272 | 07:40:58 +55:25:38 | SIMBAD | 162.22 | +28.93 | NO | 139.7 | 18.5 | 0.92 | 1.54 | n/a | none (not in DR1) |

## 2. Unique tiles (50), event-file URL and size

All URLs answered HEAD with HTTP 200 and `Content-Type: application/fits`, and each Content-Length equals the listing size. The fraction in brackets is the share of that group's 5 R500 disc that falls in the tile's unique (non-overlap) box. `*` marks the group's central tile.

| Tile | Event-file URL | Size (bytes) | Needed by (fraction of the 5 R500 disk in this tile's unique area; * = central tile) |
|---|---|---|---|
| 014135 | https://erosita.mpe.mpg.de/erodat/data/download/135/014/EXP_010/em01_014135_020_EventList_c010.fits.gz | 12,279,874 | IC1633 (0.218) |
| 015138 | https://erosita.mpe.mpg.de/erodat/data/download/138/015/EXP_010/em01_015138_020_EventList_c010.fits.gz | 12,420,331 | IC1633 (0.161) |
| 019135 | https://erosita.mpe.mpg.de/erodat/data/download/135/019/EXP_010/em01_019135_020_EventList_c010.fits.gz | 14,374,521 | IC1633* (0.438) |
| 020138 | https://erosita.mpe.mpg.de/erodat/data/download/138/020/EXP_010/em01_020138_020_EventList_c010.fits.gz | 14,023,989 | IC1633 (0.180) |
| 023135 | https://erosita.mpe.mpg.de/erodat/data/download/135/023/EXP_010/em01_023135_020_EventList_c010.fits.gz | 15,560,806 | IC1633 (0.004) |
| 039120 | https://erosita.mpe.mpg.de/erodat/data/download/120/039/EXP_010/em01_039120_020_EventList_c010.fits.gz | 19,436,054 | S0301 (0.060) |
| 041123 | https://erosita.mpe.mpg.de/erodat/data/download/123/041/EXP_010/em01_041123_020_EventList_c010.fits.gz | 19,833,722 | S0301 (0.177) |
| 043120 | https://erosita.mpe.mpg.de/erodat/data/download/120/043/EXP_010/em01_043120_020_EventList_c010.fits.gz | 20,277,559 | S0301* (0.570) |
| 044123 | https://erosita.mpe.mpg.de/erodat/data/download/123/044/EXP_010/em01_044123_020_EventList_c010.fits.gz | 21,045,687 | S0301 (0.192) |
| 074108 | https://erosita.mpe.mpg.de/erodat/data/download/108/074/EXP_010/em01_074108_020_EventList_c010.fits.gz | 15,311,519 | CID28* (1.000) |
| 093129 | https://erosita.mpe.mpg.de/erodat/data/download/129/093/EXP_010/em01_093129_020_EventList_c010.fits.gz | 12,539,518 | A3390 (0.000) |
| 096126 | https://erosita.mpe.mpg.de/erodat/data/download/126/096/EXP_010/em01_096126_020_EventList_c010.fits.gz | 11,814,155 | A3390* (0.591) |
| 097129 | https://erosita.mpe.mpg.de/erodat/data/download/129/097/EXP_010/em01_097129_020_EventList_c010.fits.gz | 12,902,573 | A3390 (0.408) |
| 160102 | https://erosita.mpe.mpg.de/erodat/data/download/102/160/EXP_010/em01_160102_020_EventList_c010.fits.gz | 8,131,351 | NGC3402 (0.170) |
| 162105 | https://erosita.mpe.mpg.de/erodat/data/download/105/162/EXP_010/em01_162105_020_EventList_c010.fits.gz | 8,245,427 | NGC3402 (0.196) |
| 163102 | https://erosita.mpe.mpg.de/erodat/data/download/102/163/EXP_010/em01_163102_020_EventList_c010.fits.gz | 8,172,731 | NGC3402* (0.534) |
| 165105 | https://erosita.mpe.mpg.de/erodat/data/download/105/165/EXP_010/em01_165105_020_EventList_c010.fits.gz | 8,947,783 | NGC3402 (0.101) |
| 185078 | https://erosita.mpe.mpg.de/erodat/data/download/078/185/EXP_010/em01_185078_020_EventList_c010.fits.gz | 11,684,849 | NGC4325* (0.378) |
| 186081 | https://erosita.mpe.mpg.de/erodat/data/download/081/186/EXP_010/em01_186081_020_EventList_c010.fits.gz | 13,516,278 | NGC4325 (0.434) |
| 188078 | https://erosita.mpe.mpg.de/erodat/data/download/078/188/EXP_010/em01_188078_020_EventList_c010.fits.gz | 19,838,308 | NGC4325 (0.188) |
| 191102 | https://erosita.mpe.mpg.de/erodat/data/download/102/191/EXP_010/em01_191102_020_EventList_c010.fits.gz | 13,941,218 | HCG62 (0.008) |
| 192099 | https://erosita.mpe.mpg.de/erodat/data/download/099/192/EXP_010/em01_192099_020_EventList_c010.fits.gz | 14,401,091 | HCG62* (0.505) |
| 192123 | https://erosita.mpe.mpg.de/erodat/data/download/123/192/EXP_010/em01_192123_020_EventList_c010.fits.gz | 17,651,188 | NGC4936 (0.011) |
| 194096 | https://erosita.mpe.mpg.de/erodat/data/download/096/194/EXP_010/em01_194096_020_EventList_c010.fits.gz | 14,696,528 | HCG62 (0.034) |
| 194102 | https://erosita.mpe.mpg.de/erodat/data/download/102/194/EXP_010/em01_194102_020_EventList_c010.fits.gz | 15,046,119 | HCG62 (0.109) |
| 194120 | https://erosita.mpe.mpg.de/erodat/data/download/120/194/EXP_010/em01_194120_020_EventList_c010.fits.gz | 16,733,108 | NGC4936 (0.267) |
| 195099 | https://erosita.mpe.mpg.de/erodat/data/download/099/195/EXP_010/em01_195099_020_EventList_c010.fits.gz | 15,065,280 | HCG62 (0.343) |
| 195117 | https://erosita.mpe.mpg.de/erodat/data/download/117/195/EXP_010/em01_195117_020_EventList_c010.fits.gz | 15,657,663 | NGC4936 (0.027) |
| 196123 | https://erosita.mpe.mpg.de/erodat/data/download/123/196/EXP_010/em01_196123_020_EventList_c010.fits.gz | 18,550,485 | NGC4936 (0.207) |
| 197120 | https://erosita.mpe.mpg.de/erodat/data/download/120/197/EXP_010/em01_197120_020_EventList_c010.fits.gz | 16,454,272 | NGC4936* (0.454) |
| 198117 | https://erosita.mpe.mpg.de/erodat/data/download/117/198/EXP_010/em01_198117_020_EventList_c010.fits.gz | 16,039,867 | NGC4936 (0.007) |
| 199123 | https://erosita.mpe.mpg.de/erodat/data/download/123/199/EXP_010/em01_199123_020_EventList_c010.fits.gz | 19,796,492 | NGC4936 (0.027) |
| 206123 | https://erosita.mpe.mpg.de/erodat/data/download/123/206/EXP_010/em01_206123_020_EventList_c010.fits.gz | 22,644,705 | S0753 (0.045) |
| 209126 | https://erosita.mpe.mpg.de/erodat/data/download/126/209/EXP_010/em01_209126_020_EventList_c010.fits.gz | 20,794,426 | S0753 (0.190) |
| 210123 | https://erosita.mpe.mpg.de/erodat/data/download/123/210/EXP_010/em01_210123_020_EventList_c010.fits.gz | 19,792,145 | S0753* (0.331) |
| 211120 | https://erosita.mpe.mpg.de/erodat/data/download/120/211/EXP_010/em01_211120_020_EventList_c010.fits.gz | 19,230,999 | S0753 (0.032) |
| 213126 | https://erosita.mpe.mpg.de/erodat/data/download/126/213/EXP_010/em01_213126_020_EventList_c010.fits.gz | 17,679,591 | S0753 (0.191) |
| 214120 | https://erosita.mpe.mpg.de/erodat/data/download/120/214/EXP_010/em01_214120_020_EventList_c010.fits.gz | 16,236,561 | S0753 (0.000) |
| 214123 | https://erosita.mpe.mpg.de/erodat/data/download/123/214/EXP_010/em01_214123_020_EventList_c010.fits.gz | 16,446,997 | S0753 (0.212) |
| 270165 | https://erosita.mpe.mpg.de/erodat/data/download/165/270/EXP_010/em01_270165_020_EventList_c010.fits.gz | 13,441,493 | RXCJ1840.6-7709 (0.023) |
| 275153 | https://erosita.mpe.mpg.de/erodat/data/download/153/275/EXP_010/em01_275153_020_EventList_c010.fits.gz | 10,690,527 | S0805 (0.019) |
| 276168 | https://erosita.mpe.mpg.de/erodat/data/download/168/276/EXP_010/em01_276168_020_EventList_c010.fits.gz | 12,017,077 | RXCJ1840.6-7709* (0.499) |
| 280156 | https://erosita.mpe.mpg.de/erodat/data/download/156/280/EXP_010/em01_280156_020_EventList_c010.fits.gz | 10,495,830 | S0805 (0.121) |
| 281153 | https://erosita.mpe.mpg.de/erodat/data/download/153/281/EXP_010/em01_281153_020_EventList_c010.fits.gz | 9,672,448 | S0805* (0.674) |
| 281165 | https://erosita.mpe.mpg.de/erodat/data/download/165/281/EXP_010/em01_281165_020_EventList_c010.fits.gz | 10,618,816 | RXCJ1840.6-7709 (0.247) |
| 283150 | https://erosita.mpe.mpg.de/erodat/data/download/150/283/EXP_010/em01_283150_020_EventList_c010.fits.gz | 9,389,798 | S0805 (0.010) |
| 287153 | https://erosita.mpe.mpg.de/erodat/data/download/153/287/EXP_010/em01_287153_020_EventList_c010.fits.gz | 9,888,753 | S0805 (0.157) |
| 287156 | https://erosita.mpe.mpg.de/erodat/data/download/156/287/EXP_010/em01_287156_020_EventList_c010.fits.gz | 10,413,946 | S0805 (0.018) |
| 289168 | https://erosita.mpe.mpg.de/erodat/data/download/168/289/EXP_010/em01_289168_020_EventList_c010.fits.gz | 10,695,174 | RXCJ1840.6-7709 (0.220) |
| 291165 | https://erosita.mpe.mpg.de/erodat/data/download/165/291/EXP_010/em01_291165_020_EventList_c010.fits.gz | 11,695,152 | RXCJ1840.6-7709 (0.010) |

## 3. Sizes

| Set | Tiles | Bytes | GB (1e9) | GiB |
|---|---|---|---|---|
| All tiles touched by the 5 R500 circles, 11 in-footprint groups | 50 | 726,234,784 | 0.726 | 0.676 |
| Minimal set: central tile only | 11 | 153,972,367 | 0.154 | 0.143 |

Per group (all touched tiles / central tile only, bytes): NGC4936 120,883,075 / 16,454,272; S0753 132,825,424 / 19,792,145; HCG62 73,150,236 / 14,401,091; S0805 60,551,302 / 9,672,448; NGC3402 33,497,292 / 8,172,731; RXCJ1840.6-7709 58,467,712 / 12,017,077; S0301 80,593,022 / 20,277,559; IC1633 68,659,521 / 14,374,521; NGC4325 45,039,435 / 11,684,849; A3390 37,256,246 / 11,814,155; CID28 15,311,519 / 15,311,519.

Central tiles: 197120, 210123, 192099, 281153, 163102, 276168, 043120, 019135, 185078, 096126, 074108.

**Not counted above (ancillary products, same tile directories).** Each tile also has a `DET_010/` directory with exposure maps and background maps. As one example (tile 197120): `em01_197120_022_ExposureMap_c010.fits.gz` is 31,973,080 bytes and `em01_197120_022_BackgrImage_c010.fits.gz` is 33,178,111 bytes. Exposure maps exist in 7 bands of about 32 MB each, and background maps in 4 bands of about 33 MB each. If one band of exposure map is fetched for all 50 tiles, add about 1.6 GB (an estimate from this one tile, not HEAD-checked for the others). The alternative is to regenerate exposure maps with eSASS4DR1 `expmap` from the event files. The site released a corrected eRASS1 attitude file on 2025-07-24 (`/dr1/AllSkySurveyData_dr1/AttitudeFiles/`, size not checked). For scale, the mirroring page says all DR1 event files together are 38 GiB, and exposure maps are 503 GiB.

## 4. Data access, usage, acknowledgement and citation terms (verbatim)

I found **no separate "terms of use", licence or "data policy" page** for DR1. The DR1 menubar has no such link; the footer links only to MPE's Imprint and Data-protection pages. I found no click-through agreement and no registration step: files are open HTTPS downloads. The binding text I found is below. All of it was fetched 2026-11-10 and is quoted verbatim.

- Data rights and public release, https://erosita.mpe.mpg.de/dr1/ :
  - "data with 359.94423568 &gt; l &gt;179.94423568 degrees (Western Galactic hemisphere) belong to eROSITA-DE."
  - "The Western Galactic hemisphere observations were released to the public through this site on 31. January 2024."
  - "Please acknowledge our work if you use eROSITA-DE DR1 data and/or the eSASS software in your publication."
- Required acknowledgement, https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/acknowledgement.html :
  - "All publications based on eROSITA-DE data must include the following text:"
  - Required text, verbatim, for a paper: "This work is based on data from eROSITA, the soft X-ray instrument aboard SRG, a joint Russian-German science mission supported by the Russian Space Agency (Roskosmos), in the interests of the Russian Academy of Sciences represented by its Space Research Institute (IKI), and the Deutsches Zentrum für Luft- und Raumfahrt (DLR). The SRG spacecraft was built by Lavochkin Association (NPOL) and its subcontractors, and is operated by NPOL with support from the Max Planck Institute for Extraterrestrial Physics (MPE). The development and construction of the eROSITA X-ray instrument was led by MPE, with contributions from the Dr. Karl Remeis Observatory Bamberg & ECAP (FAU Erlangen-Nuernberg), the University of Hamburg Observatory, the Leibniz Institute for Astrophysics Potsdam (AIP), and the Institute for Astronomy and Astrophysics of the University of Tübingen, with the support of DLR and the Max Planck Society. The Argelander Institute for Astronomy of the University of Bonn and the Ludwig Maximilians Universität Munich also participated in the science preparation for eROSITA."
  - "If the eSASS software has been used to analyse the data, the following sentence should also be added:" / "The eROSITA data shown here were processed using the eSASS software system developed by the German eROSITA consortium."
  - The same page lists references to cite. The relevant ones for this lane are: "eRASS1, DR1, eRASS in general: Merloni, A., et al., The SRG/eROSITA all-sky survey — First data release and X-ray catalog of the western Galactic hemisphere, A&A, 682, A34 (2024)"; the instrument paper (Predehl et al. 2021, A&A 647, A1); the SRG mission paper (Sunyaev et al. 2021, A&A 656, A132); eSASS (Brunner et al. 2022, A&A 661, A1); and, for the stray light, "TM5 and TM7 light leak: Stieglitz, V., et al., ... AN, e70124 (2026)".
- Download etiquette, https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/mirroring.html :
  - "The normal way to download data is via the eRODat web interface. This should be used if analysing individual objects or a small to medium sample of objects."
  - "Please make sure if you are copying the entire archive that you are doing so in a way which does not overload our server and stop other users accessing it."
  - The mirroring script itself (https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/ero_mirror_dr1.sh, read as text, not run) says: "WE INCLUDE A SPEED LIMIT BELOW - PLEASE DO NOT MODIFY UNTIL WELL AFTER DATA RELEASE TO AVOID SERVER OVERLOAD" (`net:limit-total-rate 100M`, one connection).
- If the eRASS1 diffuse-background fits are used (https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/DiffuseBkg/): "Please cite the following works if you use any of the products in this page." The works are Yeung et al. 2024, A&A 690, A399, plus two papers listed there as in preparation.

**Reading of the terms (mine):** the only obligations I found are the mandatory acknowledgement text, the eSASS sentence if eSASS is used, citing Merloni et al. 2024 for DR1, and polite download rates. I saw nothing that restricts use, redistribution or commercial use, and nothing that requires registration. Coverage is limited to the DE half-sky by the data-rights split. The site states no explicit licence, and the absence of one is not a grant of one, so a redistribution of the raw event files should be checked with MPE first.

## 5. eRASS1 depth at these positions, and can eRASS1 measure 3-5 R500?

**Documented depth.** From https://erosita.mpe.mpg.de/dr1/ : "DR1 consists of 20626.5 square degrees, which have a variety of effective exposure values, ranging from ∼100 seconds in the Ecliptic equator to more than 10,000 seconds close to the Ecliptic pole in the 0.6—2.3 keV energy band."

**Measured at these positions** (eRODat upper-limit service, `Exposure` field, band 022; centre / range over the four points at 5 R500, in seconds): NGC4936 157 / 152-163; S0753 145 / 166-176; HCG62 132 / 127-137; S0805 102 / 98-107; NGC3402 84 / 79-82; RXCJ1840.6-7709 133 / 132-159; S0301 207 / 196-210; IC1633 116 / 112-150; NGC4325 99 / 96-183; A3390 155 / 149-162; CID28 167 / 150-170. All 11 groups are shallow, 80-210 s. None is near the ecliptic pole.

**There is no deeper public event release.** DR2 (https://erosita.mpe.mpg.de/dr2/, released 2026-07-31) is eRASS:3 but "a catalogue-only release". DR1 eRASS1 is the only public eROSITA-DE event data.

**Feasibility note.** The first part is cited; the rest is marked as my own judgement.

- Cited: Bulbul et al. 2026 (arXiv:2607.27804, "Thermal or Non-thermal? Diffuse emission in the infall region of stacked galaxy groups"; from its abstract, not verified further) stacked **827** nearby eRASS1 groups (M < 1e14 Msun). They detected intragroup gas out to about 2 R200m. Electron density falls from (4.8 ± 1.3)e-5 cm^-3 at (0.7-2) R500c to (5.5 ± 2.0)e-6 cm^-3 at (2-4) R500c, and a residual component (possibly inverse Compton) is about 30 % of the thermal flux. T. Mistele is a co-author. Bahar et al. 2024 (A&A 691, A188) used "deeper eROSITA observations" of eRASS1-detected groups, which are not public. Matsushita et al. 2025 (arXiv:2510.04523) found group emission-measure slopes beta of about 0.4-0.65 out to r200 with Suzaku.
- My own judgement, not computed in a lane: the 3-5 R500 annulus covers about 2.7 deg^2 (NGC4325) to 16 deg^2 (S0753). With 80-210 s of exposure, and assuming a soft-band survey background of order 1e-3 counts s^-1 arcmin^-2 for the sum of the 7 TMs (my assumption, not checked against a DR1 page), each annulus collects roughly 10^3-10^4 background counts. That gives a Poisson precision of about 1-3 % of the background. Extrapolating a beta of about 0.5 profile from about 1 R500 puts the group's own surface brightness at 3-5 R500 well below 1 % of the background. The systematic floor is at the few-percent level, set by large-scale soft-foreground structure (Local Hot Bubble, Galactic CGM and corona, the eROSITA bubbles for the inner-Galaxy sight lines), the TM5/TM7 light leak and the "lost photon counts" issue. That floor sits above the expected signal.
- **My conclusion**: eRASS1 can probably measure an individual group's surface brightness to about 1-1.5 R500. It cannot measure one group at 3-5 R500. A 3-5 R500 measurement needs a stack. These 11 nearby groups cover large solid angles, so their pure Poisson statistics are not hopeless. However, an 11-group stack would be limited by foreground and background systematics across degree scales, and the published route to 2-4 R500 used 827 groups. Treat any single-group 3-5 R500 profile from DR1 as an upper limit, unless the background is modelled per tile (for example with the DR1 diffuse-background fits) and the light-leak cameras are dropped (use TM8 = TMs with the on-chip filter).

**Suzaku note (UGC 03957).** Thölken, Lovisari, Reiprich & Hasenbusch 2016, "X-ray analysis of the galaxy group UGC03957 beyond R200 with Suzaku", A&A 592, A37 (arXiv:1603.05255). **Verified** from the arXiv API record (journal_ref "A&A 592, A37 (2016)"). The abstract says gas properties were measured "up to 1.4R200 ≈ 1.4 Mpc in four azimuthal directions", using 138 ks of good Suzaku exposure across five pointings. Matsushita et al. 2025 = arXiv:2510.04523, "Suzaku observations of outskirts of nearby clusters and groups: I. electron density and gas fraction to the virial radius". It is a 14-system sample out to about r200 and has no journal ref yet in the arXiv record. **Its abstract does not name UGC 03957, so I have not verified that UGC 03957 is in its sample.** The claim that the profiles are available "in figures only" was not checked. UGC 03957 is at l = 162.2, so it is **outside DR1** and Suzaku is its only outskirts route here.

**Untrusted-content check.** No fetched page contained text addressed to an AI or any instruction to the reader beyond normal usage notes. A case-insensitive grep over all saved pages for "ignore previous", "language model", "claude", "chatgpt" and "llm" found nothing.

## 6. Fetch log

All fetches were made on 2026-11-10 with curl or the Python standard library. GET was used for HTML, index and API pages, and HEAD for event files. No event, image, exposure-map, background-map or catalogue file was downloaded.

Documentation and index pages (GET):
- https://erosita.mpe.mpg.de/dr1/
- https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/
- https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/acknowledgement.html
- https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/mirroring.html
- https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/ero_mirror_dr1.sh (HEAD then GET as text, 2,965 bytes; read, not executed)
- https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/DiffuseBkg/
- https://erosita.mpe.mpg.de/dr1/eSASS4DR1/eSASS4DR1_ProductsDescription/
- https://erosita.mpe.mpg.de/dr1/eSASS4DR1/eSASS4DR1_ProductsDescription/file_naming_scheme_dr1.html
- https://erosita.mpe.mpg.de/dr1/eSASS4DR1/eSASS4DR1_ProductsDescription/products_description_dr1.html
- https://erosita.mpe.mpg.de/dr1/eSASS4DR1/eSASS4DR1_ProductsDescription/SKYMAPS_052022_MPE.fits (HEAD: 357,120 bytes, then GET; the tile-boundary table, under the 2 MB limit, linked from the DR1 data page)
- https://erosita.mpe.mpg.de/dr1/FAQ_dr1/
- https://erosita.mpe.mpg.de/dr1/news_dr1/
- https://erosita.mpe.mpg.de/dr1/menubar.html , https://erosita.mpe.mpg.de/dr1/footer.html , https://erosita.mpe.mpg.de/dr1/header.html
- https://erosita.mpe.mpg.de/dr2/
- https://erosita.mpe.mpg.de/erodat/
- https://erosita.mpe.mpg.de/erodat/apis/
- https://erosita.mpe.mpg.de/erodat/data/download/ (archive root index)
- HEAD https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/DR1_Main/ (404, probe)
- https://erosita.mpe.mpg.de/dr1/erodat/data/download/ (301, probe)

Archive directory indexes (GET):
- https://erosita.mpe.mpg.de/erodat/data/download/123/ (Dec-row index)
- https://erosita.mpe.mpg.de/erodat/data/download/120/196/ (404; tile 196120 does not exist)
- https://erosita.mpe.mpg.de/erodat/data/download/120/197/DET_010/ (one tile's ancillary listing)
- https://erosita.mpe.mpg.de/erodat/data/download/<DDD>/<RRR>/ and https://erosita.mpe.mpg.de/erodat/data/download/<DDD>/<RRR>/EXP_010/ for each of the 50 tiles in section 2 (100 index pages; DDD/RRR as in the URLs of section 2)

HEAD requests (no body): each of the 50 event-file URLs in section 2. Each was HEADed twice, once for headers and once for the status code.

eRODat lookup APIs (small JSON):
- https://erosita.mpe.mpg.de/erodat/skyview/skytile_search_api/?RA=<ra>&DEC=<dec>&RAD=<5 R500 deg>, 11 calls, one per in-footprint group (positions in section 1)
- POST https://erosita.mpe.mpg.de/erodat/upperlimit/service_multi, 1 call, 55 positions, band 022, DR1_eRASS1; only `Exposure` used (see Method, item 6)

Name resolution (CDS Sesame; each GET 302-redirected to https://vizier.idia.ac.za/viz-bin/nph-sesame/...):
- https://cds.unistra.fr/cgi-bin/nph-sesame/-oI/SNV?<name> for NGC4936, ACO S 753, HCG 62, ACO S 805 (a first serial pass, which I stopped because it was slow; a first try without redirect-follow returned only the 302)
- https://cds.unistra.fr/cgi-bin/nph-sesame/-oI/SNVA?<name> for NGC3402, ACO 194, RXC J1840.6-7709, WBL 154, ACO S 301, NGC1132, IC1633, NGC4325, RXC J2315.7-0222, NGC6338, III Zw 54, IC1262, AWM4, ACO 3390, CID28, CID 28, UGC03957, ACO S 805, ACO S 753
- http://cdsweb.u-strasbg.fr/cgi-bin/nph-sesame/-oI/SNV?NGC4936 (timed out)

Literature:
- https://ar5iv.labs.arxiv.org/html/1409.3845 (Lovisari et al. 2015; Tables 1 and 2 read; no coordinates in the paper)
- https://export.arxiv.org/api/query?search_query=all:UGC03957+OR+all:%22UGC%2003957%22&max_results=10 (Thölken 2016 record)
- https://export.arxiv.org/api/query?search_query=all:%22UGC%2003957%22+AND+au:Matsushita&max_results=10 (no results)
- https://export.arxiv.org/api/query?search_query=au:Matsushita_K+AND+abs:Suzaku+AND+abs:groups&sortBy=submittedDate&max_results=15 (no results)
- https://export.arxiv.org/api/query?search_query=au:Matsushita+AND+abs:Suzaku&sortBy=submittedDate&sortOrder=descending&max_results=12
- https://export.arxiv.org/api/query?search_query=abs:eRASS1+AND+abs:stack+AND+abs:%22surface+brightness%22&max_results=12&sortBy=relevance
- https://export.arxiv.org/api/query?search_query=abs:eROSITA+AND+abs:outskirts+AND+abs:group&max_results=12&sortBy=relevance
- https://export.arxiv.org/api/query?id_list=2607.27804,2401.17276,2510.04523 (abstracts)

Working copies of the fetched pages, the tile computation (`scripts/tiles.py`, `tiles.json`) and the exposure JSON are in this session's scratchpad. They are not in the repo.
