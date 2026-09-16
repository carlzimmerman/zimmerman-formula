# G203 — HeCS/DR7 Member-Catalog Commission: data provenance

Status: **FETCHED + TRANSCRIBED** (2026-09-16). All files below are committed in
`deepseek_push/G203_data/`, sha256-verified against the source downloads.

## HeCS member catalog — the providing stack (G195's data gate, CLOSED)

**Citation.** Rines K., Geller M.J., Diaferio A., Kurtz M.J. (2013),
"Measuring the Ultimate Halo Mass of Galaxy Clusters: Redshifts and Mass
Profiles from the Hectospec Cluster Survey (HeCS)", ApJ 767, 15
(bibcode 2013ApJ...767...15R, DOI 10.1088/0004-637X/767/1/15).
58 X-ray-selected clusters, 0.1 < z < 0.3; 22,680 Hectospec + 2,621
literature (SDSS/Boschin) redshifts; **10,145 cluster members** (334 are
members of two clusters); caustic mass profiles (Diaferio & Geller 1999 /
Diaferio 1999, q = 25 smoothing) to ~2-3 r_vir.

**URLs (CDS/VizieR catalog J/ApJ/767/15):**

| file | URL | size | sha256 |
|---|---|---|---|
| ReadMe | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/ReadMe | 9,250 B | 3bc3774434bde5db3fd37d7e51c26b11308e9138955f59a068c431a3e431075a |
| table1.dat (58 clusters: Name, RA, Dec, z, Lx, sig_p, Nm) | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table1.dat | 3,422 B | 0c6de918db0f8718096eba15ebd9dba94bd7dae11b227f51387b4c6fa8dd617b |
| table2.dat (22,680 redshifts + membership flag Np) | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table2.dat | 1,088,640 B | 95731daefd11f329eb2afe7e90b71301da8a3373421d543adfbc1cb34988feb3 |
| table3.dat (2,621 literature members) | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table3.dat | 102,219 B | 799e78b3fc0f78790f90bacbe03944ad732098824af02c2c829241bab0182d7b |

**Table 4 transcription.** Per-cluster characteristic radii and masses
(r500, r200, r5.6, rmax [Mpc], M200, Mvir, M5.6, Mmax/M200) are NOT part of
the VizieR deposit; they are the paper's Table 4, transcribed from the
published paper PDF into `hecs2013_table4.tsv` (58 rows) by layout-aware
extraction (pdfplumber) at commit time and spot-checked against the printed
table. Source: ApJ PDF mirror
https://iris.unito.it/retrieve/handle/2318/138552/169149/apj_767_1_15.pdf
(doi.org/10.1088/0004-637X/767/1/15); the journal's machine-readable tables
are the canonical origin. sha256 94021f6001bab50f853d716b9e656e8f877f638dafe0442b653098beca9fcf8f.

Cosmology (paper Sec. 2): H0 = 100 h km/s/Mpc, Ωm = 0.3, ΩΛ = 0.7; h cancels
in R/R500 and v_los.

## SDSS DR7 satellite stack (Wojtak & Mamon 2013) — NOT pre-packaged

**Citation.** Wojtak R., Mamon G.A. (2013), MNRAS 428, 2407
("The phase-space density profiles of dark matter halos", DR7 central-
satellite sample, >10^4 satellites).

Status: **UNVERIFIED-as-download**. No member (R, v_los) catalog is deposited
for this stack; the sample must be reconstructed from SDSS DR7 survey data
(SQL via CAS classic.sdss.org/dr7, central/satellite selection per the paper).
Not a blocker: HeCS delivers the full G195 data requirement (R/R500 + v_los
members to the critical window).

## Validation (see G203_results.json for the machine-readable spec)

- table1/table4 names: 58/58 match.
- Galaxy counts: 22,680 + 2,621 = 25,301; members (Np >= 1) = 10,145 = the
  paper's total; Np sum = 10,479 = 10,145 + 334 exactly the paper's
  two-cluster-overlap statement.
- Assignment (deposit has no per-galaxy cluster ID): nearest cluster center;
  per-cluster assigned count vs published Nm: median diff 0.
- Coverage: 58/58 clusters reach R >= 2 R500, 56/58 >= 4, 50/58 >= 5; 3,629
  members in the [2,5] R500 window; fit catalog = 58 clusters (all have
  >= 12 in-window members).

## Manual fetch path (if re-fetching)

```
curl -sL -o ReadMe     https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/ReadMe
curl -sL -o table1.dat https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table1.dat
curl -sL -o table2.dat https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table2.dat
curl -sL -o table3.dat https://cdsarc.cds.unistra.fr/ftp/J/ApJ/767/15/table3.dat
```
then verify with the sha256 column above. Table 4: extract from the paper PDF
(Tables 4 of ApJ 767, 15) into `hecs2013_table4.tsv` (columns:
cluster r500Mpc r200Mpc r56Mpc rmaxMpc M200e14 M200err MvirE14 MvirErr
M56e14 M56Err MmaxM200).