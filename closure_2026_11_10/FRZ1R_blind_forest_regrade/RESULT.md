# FRZ1R RESULT: blind re-grade of FRZ1's forest row

**Blind label (unchanged, RESULT_BLIND.md 6912e86274): canonical FOREST ROW FAILS (Delta chi^2 8142.08); alt FOREST ROW
FAILS (7685.51). Lane: FAILS.** Footings not pooled. TEST lane; relabels nothing; a fail of form B's frozen layout on the
record's forest gate, with an inherited halo list.

**COMPARISON: AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL.** FRZ1 (opened only after 6912e86274): FAILS / FAILS,
9916.2 / 9008.7.

## Differences (reading L)

| quantity | FRZ1 canonical | FRZ1R canonical | FRZ1 alt | FRZ1R alt |
|---|---|---|---|---|
| R_cold z 2.2, k 1 / 3 / 5 | 0.9911 / 0.8732 / 0.7674 | 0.9915 / 0.8776 / 0.7728 | 0.9917 / 0.8787 / 0.7952 | 0.9919 / 0.8805 / 0.7971 |
| R_cold z 3.0, k 1 / 3 / 5 | 0.9920 / 0.8446 / 0.6646 | 0.9931 / 0.8634 / 0.6963 | 0.9916 / 0.8314 / 0.6695 | 0.9925 / 0.8473 / 0.6924 |
| R_cold z 4.4, k 1 / 3 / 5 | 0.9956 / 0.9027 / 0.6859 | 0.9967 / 0.9273 / 0.7561 | 0.9954 / 0.8939 / 0.6764 | 0.9965 / 0.9177 / 0.7379 |
| Delta chi^2, all 755 points | 9916.2 | 8142.08 | 9008.7 | 7685.51 |
| bin z 3.0 / 3.2 (own block) | 1254.3 / 1378.8 | 1062.2 / 1126.1 | 1132.1 / 1256.1 | 997.3 / 1070.4 |
| reading V (reported only) | 494.6 | 99.23 | 291.6 | 23.82 |

- R_cold - 1 at k 3 to 5 differs by 0.004 to 0.07 (largest at z 4.4, k 5), always with FRZ1R removing less power; the
  total Delta chi^2 is 18 % (canonical) and 15 % (alt) lower here. Both are about 2,000 times the gate of 4.
- The z = 0 validation agrees with CO1 to 0.001 in both codes, so the difference is z-specific.

## Cause (found cheaply, by a targeted look at `frz1_hm.py` lines 97-106)

- Ambiguity 1 of READING.md: a galaxy-regime halo at z >= 2.2 whose phantom reach r_t exceeds r_ta leaves part of its cold
  dark energy unplaced inside r_ta. FRZ1 lays that remainder out isothermally (M proportional to r out to r_ta, the cluster
  rule's form); FRZ1R spreads it in the reference NFW shape (CFG556's capped-halo rule). NFW is more concentrated than
  M proportional to r, so FRZ1R keeps more small-scale power. My third alternative (a shell at r_ta) gives more loss than
  both (15978.64 / 13618.41). The sign and the label do not depend on this choice: all three readings fail by >1,000x.
- Reading V differs more (FRZ1 R_cold at z 3, k 5 0.938 / 0.953; FRZ1R 0.991 / 1.039): the scopes are built differently
  (FRZ1 lays the remainder out to r200m; FRZ1R lays the virial charge as a phantom to min(r_t, r_ta) and keeps the rest of
  M_ta in the reference shape). Reading V is reported only in both lanes, and it fails the gate in both (smallest 23.82 here).
- Not checked: FRZ1's brackets (not re-run here). Delta_ta 11.81 is FRZ1's least severe frozen bracket (6413 / 6312).

## What is independent and what is shared

- Independent: the halo-model code for R_cold(k, z) (`frz1r_hm.py`), written from CO1's and FRZ1's criteria text. CFG556's
  numerical definitions (EH no-wiggle shape, Tinker 2008 / 2010, Duffy c(M), Moster stars, beta gas, turnaround, spectrum
  formulas) were taken from CFG556's code and re-implemented; FRZ1 executes that same library, so a shared error in those
  inherited definitions would not be caught here.
- Shared: the forest gate (`ss1_cosmo.forest_eval`, DESI DR1 P1D, form B's CLASS reference), set-up copied from HLF1;
  FRZ1 uses the same. Validation of the gate: R = 1 -> 0; CO1 held -> 160.74 / 1025.57 in both lanes.
- Blindness: FRZ1's RESULT and frz1_* files were not opened before 6912e86274. I knew FRZ1 existed; I did not know its
  numbers.

## Commits

READING 5daab3b12c; halo model 1eca4476b1; gate e0f3058204; RESULT_BLIND 6912e86274; this file follows.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
