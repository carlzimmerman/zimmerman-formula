# CFG403 FROZEN CRITERIA: does any z ~ 1–3 disc have all three self-calibration ingredients (OSIRIS AO inner + deep outer + resolved gas)?

Owner's go in this chat ("common bro lets do it..") answered an offer to run a **metadata-only** cross-match. No data frames or cubes are downloaded. Written before any query of OSIRIS pointings or ALMA rows at these positions (the KOA OSIRIS **schema** was listed first to choose columns; no rows).

## Why
CFG385: the self-calibrated a0(z) test needs each disc to span y ≳ 3 (inner) to y ≲ 0.3–0.55 (outer). CFG386: nothing on disk does. CFG400/401: even with both ends, the per-galaxy a0 spreads 2–3 dex unless the gas distribution is measured. So a usable galaxy needs all three: (A) AO inner kinematics, (B) deep outer kinematics, (C) a resolved gas map.

## Parent samples (positions on disk)
- KMOS3D (`data_assembly/kmos3d_phibss/kmos3d_catalog.csv`, RA/DEC, Z); outer-curve fits `kmos3d_cubes/k3d_fits_main_final_flags.csv`.
- SINS/zC-SINF AO (`highz_literature_tables/sins_ao/sins_ao_table1_sample.csv`, sexagesimal; z_Halpha).
- NOEMA3D (`noema3d/noema3d_per_galaxy.csv`; CO kinematics; counts as gas C).
Galaxies with z outside 1.0–3.0 are dropped. Duplicates across samples (within 1.0″) are merged.

## Gates (per galaxy)
- **A (OSIRIS inner).** KOA `koa_osiris` science frames (obstype/koaimtyp object; not sky) whose pointing (ra, dec) lies within **1.5″** of the galaxy, whose filter wavelength range [waveblue, wavered] contains **Hα 6564.6 Å or [O III] 5008.2 Å** × (1+z), plate scale ≤ 0.10″, summed elaptime ≥ **3600 s**.
- **B (deep outer).** A KMOS3D fit (fit quality as CFG386: 0 < Va < 790, eVa/Va ≤ 0.10) with the CFG386 conservative outer value g_obs(rmax) ≤ **0.55 a0** (canonical 9.3603e-11). Reported, not gated: any deep seeing-limited membership (KMOS3D or SINS).
- **C (resolved gas).** ALMA obscore rows (public) whose footprint contains the position, with a spectral window covering **CO(2–1), CO(3–2), CO(4–3), CO(5–4), [C I](1–0) or [C I](2–1)** at the galaxy z, and s_resolution ≤ **0.6″**; OR NOEMA3D membership (flagged NOEMA).

## Headline
- N_ABC ≥ 1 → **LANE CANDIDATE(S)** (named; a follow-up lane needs a separate download go).
- N_ABC = 0 → **NONE: OSIRIS goes on the proposal list**, with which gate binds (pairwise counts AB, AC, BC reported).
Also reported, not gated: the same count with "any AO" (OSIRIS ∪ SINS AO) for A.

## Controls
- C1 (KOA positive): Q2343-BX442 (RA 356.0789… from Law+12 / SIMBAD-free: use 23:46:… as in CFG437 inventory targname) must return OSIRIS object frames ≥ 3600 s. Implemented as: the KOA query on targname LIKE '%442%' within the Steidel/Law programmes returns frames, and the positional query at their median pointing returns them too.
- C2 (ALMA positive/negative): the GOODS-ALMA field centre (53.125, −27.8) returns 2015.1.00543.S; (150, +60) returns none of it.
- C3 (line arithmetic): CO(3–2) at z = 2.2 maps to 108.06 GHz (± 0.01).
- C4 (no silent skips): every parent galaxy in 1.0 ≤ z ≤ 3.0 is evaluated for A, B and C (count printed).

## MUTATE (rc 1)
All galaxy positions shifted by +60″ in Dec. A matches must fall to ≤ 10% of the main run's (OSIRIS IFU fields are ≤ 6.4″) — a premise failure is kept and disclosed.

## Not claimed
No a0 is measured. Metadata only. A gas map "covering" a line is not a detection.
