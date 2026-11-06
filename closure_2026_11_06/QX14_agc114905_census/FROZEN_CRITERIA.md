# QX14 frozen criteria: does AGC 114905's environment supply QX4's external field?

Frozen before any download and before any graded number. Rules: ../SWARM_BRIEF.md. Kappa = 1/2 FITTED; not theory
closed. Adopts nothing. One galaxy excludes nothing.

The owner approved, in chat on 11-06, exactly the catalogue queries in ../QX4_udg/NEEDS_OWNER.md: a neighbour
census (NED, HyperLEDA, ALFALFA a.100, a 2MPZ cone) and a large-scale g_e by the record's SPARC method. Nothing else
is downloaded.

## Inputs taken from the record (read-only)

- QX4 iteration 2 (../QX4_udg/iter2.json, iter2_efe.py): the external-field window that rescues AGC 114905 at
  p >= 0.05 in the 1D EFE estimator g = nu((g_N + g_e)/a0)(g_N + g_e) - nu(g_e/a0) g_e. Canonical
  g_e/a0 in [0.0756, 0.2909]; alt [0.0768, 0.2925]. Also the outer internal acceleration g_int = V_out^2/R_out
  (canonical 0.025 a0, alt 0.021 a0) and R_out, the last UD1 ring.
- Distance D0 = 78.7 Mpc (UD1, Mancera Pina+2024 fiducial).
- The record's external-field estimator gext_vectors_2026/src/gext_estimator.py (Chae 2021 Sec. 3.1; 2M++ and
  MCXC, already on disk), imported read-only.

## Reading of g_e (stated now; it corrects QX4's host bound)

In the 1D estimator, g_e enters nu together with g_N, so g_e is the NEWTONIAN external field. That is the same
convention as Chae's e_N = g_Ne/a0. QX4's host bound, M = (g_e d)^2/(G a0), instead treated g_e as the host's MOND
field. QX14 grades with the Newtonian reading, which is consistent with the estimator.

- **Host condition.** A host of baryonic mass M at 3D distance d gives a Newtonian field g_N(d) = G M/d^2. Its
  actual field is g_h(d) = nu(g_N/a0) g_N, with the record's nu and the footing's a0. The tidal acceleration
  across the disc is t(d) = |dg_h/dd| R_out.
- **A host qualifies** if some d >= d_min puts g_N(d) inside the window AND keeps t(d) < g_int. Here d_min is the
  neighbour's projected separation R_p, so the line-of-sight distance is free (conservative toward rescue).
- **M_req**, the smallest qualifying host mass on each footing (any d), is computed before the census is read.
- **Reported, not graded:** QX4's reading (M_req,QX4 = 3.4e9 / 6.4e9 Msun), and whether each census neighbour
  would qualify under it.

## Target position and velocity

AGC 114905's position and heliocentric cz come from NED's entry for the name, cross-checked against its ALFALFA
a.100 entry (|dcz| <= 20 km/s, separation <= 30 arcsec). If the two disagree beyond that, ALFALFA is used and the
disagreement is reported.

## Census rule

- **Region.** Every galaxy with projected separation R_p < 1 Mpc at D0 (theta < 0.7286 deg) and
  |cz - cz0| <= 500 km/s.
- **NED.** Objects of type G with a velocity in a cone query (radius 0.75 deg).
- **HyperLEDA.** objtype G with v (heliocentric), cone radius 0.75 deg.
- **ALFALFA a.100** (Haynes+2018), detection codes 1 and 2.
- **2MPZ** (Bilicki+14; SSA freeform SQL as in NV2), cone radius 0.75 deg, all rows.
  - A 2MPZ source with zSpec enters if its zSpec is in the cz window.
  - A source with only zPhoto enters as a PHOTO-Z CANDIDATE if its 2-sigma photo-z interval (sigma_z = 0.015)
    overlaps the window. Its distance is then unknown and treated as D0, conservative toward rescue.
- **Dedupe.** Within 15 arcsec, keeping the entry with the best mass data.

## Masses (per neighbour; central value and an upper bound M_up)

- **Stellar mass.** M* = 0.64 L_Ks (record ML_KS, MSUN_KS 3.28), from the 2MASS Ks total magnitude (2MPZ or the
  NED/HyperLEDA K). With no Ks, use HyperLEDA's total B (btc): M* = 1.5 L_B (M_sun,B = 5.48).
- **Gas.** HI from ALFALFA where matched: M_HI = 2.356e5 D0^2 S21, and M_gas = 1.33 M_HI. Otherwise the record's
  Chae gas recipe from M* (gext_estimator).
- **Upper bound.** M_up = 3 x central for Ks-based masses and 6 x central for B-based masses (generous, toward
  rescue).

## Large-scale field (record's SPARC method)

GextEstimator.eN_at at (RA, Dec, D0), in mode 'ks115', D_MAX 200, self excluded, as the record does for SPARC. It
gives the noclu value and the maxclu value (completeness up-weight, and the field x 8 for missing baryons), both
converted to each footing's a0 (g_Ne = eN x 1.2e-10). The band is [noclu, maxclu]. Its sigma is NV2's median
per-system sigma_E1 (0.45 dex) when NV2's JSON records it; otherwise 0.45 dex is used and that fact is stated. A
sensitivity row truncates the sum at 5 Mpc; it is reported, not graded.

## Completeness test (decided before reading the census)

The census can exclude a qualifying host only if it is complete at M_req. That holds if either:

- 2MPZ's Ks <= 13.9 stellar-mass limit at D0 (M* = 0.64 L_Ks at M_K = 13.9 - DM) is <= M_req; or
- ALFALFA's HI limit at D0 is <= M_req / 1.33. The HI limit is the Haynes+2011 Code-1 50 % line,
  log S21 = 0.5 log W50 - 1.207 for W50 < 200 km/s, taken at W50 = 200 km/s.

## Labels (per footing; never pooled)

- **RESCUED (EFE)** if a census neighbour qualifies at its CENTRAL mass, OR the large-scale band's geometric mean
  (E1) lies inside the window.
- **NOT RESCUED (EFE excluded)** if all of these hold:
  - no neighbour qualifies at M_up with d_min = R_p;
  - no photo-z candidate qualifies at M_up;
  - the band's top end, maxclu + 1 sigma, lies below the window's lower edge;
  - the completeness test passes.
- **NO VERDICT** otherwise. That covers the band only grazing the window, a photo-z candidate that could qualify,
  a failed completeness test, or a qualifying neighbour at M_up only.

The QX4-reading result is reported next to the label and never changes it.

## Known answers

- KA1. With no sources, the estimator returns zero field. It also reproduces the record's gext_vectors.csv
  log_eN_noclu and maxclu for 3 SPARC galaxies (first, middle and last rows) to 1e-6 dex.
- KA2. Run on UD1's data, the window recomputed through iter2_efe's own law_v reproduces QX4's iter2 bounds to 1e-3.

## Controls (separate outputs)

- **MUTATE-1.** Plant a host of mass 2 x M_req at its best distance. It must be RESCUED on both footings.
  - Also run, as directed, a Milky-Way-mass host (6e10 Msun baryons) at d = 100 kpc. It is reported under both
    readings. Under the Newtonian reading it gives g_N = 0.009 a0, below the window, so it is NOT expected to
    rescue. That expectation is stated now.
- **MUTATE-2.** Remove every neighbour and zero the large-scale field. The result must not be RESCUED.

If MUTATE-1's planted 2 x M_req host fails to rescue, or MUTATE-2 rescues, no label stands.

## Outputs

- Raw downloads go to _external_data/qx14_agc114905/, a new empty directory, and are not committed. Python reading
  them runs with -I.
- The lane commits a derived census table (census.csv) and a query log (QUERY_LOG.json: URL, UTC time, rows, bytes,
  sha256) under this directory.
