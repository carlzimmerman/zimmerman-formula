# EV1 frozen criteria: is environment the switch between discs and hot systems, once it is read properly?

Frozen before any EV1 script, reading or graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No
dark-matter particle. Both footings graded separately, never pooled:
- canonical: a0 = 9.3603e-11 m/s^2, Lstar = 21.7 pc;
- alt: a0 = 1.1312e-10 m/s^2, Lstar = 22.9 pc.
No downloads: every input is on disk and named here. One thread, under 1 GB, minutes.

## Why this lane

QX24 killed an external-field key, but only through T2 on the noclu reading of two Virgo ellipticals. Clues for an
environment switch: field UDGs (AGC 114905) sit below the law while Coma UDGs sit above it; satellite offsets rise with
the host field (QX24 T3b, partial rho +0.71); LG field dwarfs show no step; KiDS isolated lenses show a weak 2.46 sigma
split. Against it: NGC 720, the most isolated X-ray elliptical, has the largest offset (+0.51 / +0.48).

Known before this freeze, disclosed: QX24's per-elliptical x_e (noclu and maxclu) and offsets; GB1's L0 table; that
NGC 4472 and NGC 4649 are Virgo members; that all SPARC galaxies sit below QX24's x_c on noclu; that KiDS isolated
lenses are isolated by construction; that UMa is a spiral-rich group with no MCXC entry. SPARC's Ursa Major members
have NOT been graded by any lane known to this session; their offsets are unseen.

## 1. Environment measures (each a per-system switch S in {0, 1}, read from data on disk)

A system's switch is set by the measure, never by its class name. Where a class carries no reading, S is None and
the GB1 rule applies (NO VERDICT; bracket over S in {0, 1}, reported, never replacing the cell).

**M1 external field x_e** (QX24's measure and threshold). S = 1 if x_e >= x_c, with x_c QX24's frozen values read
from qx24.json (0.0447 canonical / 0.0406 alt). Graded reading: **noclu** (the record's primary column; frozen now).
maxclu is reported as a second reading, never graded.
- SPARC: gext_vectors.csv log_eN_noclu (x 1.2e-10 / a0); maxclu reported.
- Ellipticals: QX24's estimator values (ks115 at the QX24 positions and Humphrey D), recomputed and checked (KA2).
- dSphs: X1 x_e_mid (QX24's source).
- Coma UDGs: S1 x_e_dmean.
- Solar System: the Milky Way's Newtonian field at the Sun, x_e = v_c^2 / (R0 a0) with v_c and R0 from the Eilers+2019
  table on disk (mw_rc_eilers2019_table1.tsv, the row nearest 8.1 kpc). This overestimates the baryonic field by about
  x 2, stated; S is 1 for any reading above 0.05.
- X-COP and groups: None (the estimator's catalogue contains the system itself, so its field is not external).
- KiDS isolated lenses: S = 0 for both colours (isolated by selection; QX24 T1 reading).

**M2 host membership.** S = 1 if the system orbits inside a more massive host; S = 0 for a central / host system.
- SPARC: S = 1 if f_D = 4 (Ursa Major, SPARC_Lelli2016c.mrt), or if it passes the MCXC rule below.
- MCXC rule (all classes where applied): projected separation (angle x the system's distance) < 2 R500 and
  |D_sys - c z_cl / 73| <= 0.25 c z_cl / 73 (H0 = 73 is SPARC's own Hubble-flow convention, a measured local value).
  The system's own MCXC entry is excluded.
- Ellipticals: the MCXC rule at QX24's positions and Humphrey D. Everything else is a central: S = 0.
- dSphs: S = 1 if X1 host is MW or M31 and the LW1 class is not "LG field"; LG field S = 0.
- Coma UDGs: S = 1 (Coma, MCXC J1259.7+2756; S1 d_mean 1-2 Mpc, inside 2 R500 = 2.28 Mpc is checked, not assumed).
- X-COP and groups: S = 0 (they are the hosts).
- KiDS isolated lenses: S = 0 (isolation criterion).
- Solar System: S = 1 (the Sun orbits inside the Milky Way).

**M3 host hot atmosphere.** S = 1 if the measured matter sits inside an X-ray-detected hot atmosphere, the system's
own or its host's.
- X-COP (X-ray clusters), Lovisari groups (X-ray groups), Humphrey ellipticals (X-ray halos, the selection): S = 1.
- Coma UDGs: S = 1 (Coma ICM, MCXC). SPARC: S = 1 only if it passes the MCXC rule; otherwise 0. SPARC discs' own
  coronae are not catalogued on disk: S = 0, disclosed as this measure's weak point; a bracket with S = 1 for
  Vflat >= 200 km/s is reported.
- dSphs: S = 1 for MW and M31 satellites with X1 d_host <= 300 kpc (both hosts' coronae are detected; literature,
  stated, not from a file); S = 0 for LG field and for satellites beyond 300 kpc.
- KiDS isolated lenses: None (own hot halos not measured); bracket {early 1 / late 0, both 0, both 1}, reported.
- Solar System: S = 1 (inside the Milky Way corona; literature, stated).
- M3 overlaps the dead "host temperature" key only as a presence flag, not as a temperature; disclosed.

All readings are written by ev1_readings.py to readings.json and committed BEFORE ev1.py (the grader) exists.

## 2. The key (one form for all three measures; one amplitude per measure and footing)

g_pred = g_N + F_S (g_law - g_N), with F_S = 1 if S = 0 and F_S = F_env if S = 1: environment multiplies the law's
phantom field. Delta = log10(g_pred / g_law), applied through GB1's (b = 1, F) interface at each point's x.

**Amplitude, fixed on one declared class before grading anything else:** the graded satellites (MW classical +
bright M31, pooled, 33 systems). F_env solves median_sat(D - Delta) = anchor, the anchor being the SPARC mean residual
under the same key (S as read). Solved by bisection on F_env in [1, 100] (a calibration equation, not a scan); if the
satellites under a measure have S = 0 for all, the key has no amplitude and every row is NO VERDICT. Solved per
footing. Nothing else is tuned.

Consequence stated now: the G6 bright-M31 and MW-classical cells are then calibration-driven; G6 tests the LG field
cell and the split between the two satellite classes.

## 3. Grading

GB1's battery exactly (gb1.py's loaders and gate functions, executed read-only up to its main section): G1 SPARC, G2
X-COP, G3 groups, G4 ellipticals, G5 Coma UDGs, G6 dSph classes, G7 KiDS split, G8 Solar System, with GB1's lines.
G9 is NOT EVALUATED. Per key and footing each row is PASS / FAIL / NO VERDICT (+ bracket).

**Extra switch rows (within one class, environment varies; graded):**
- **W1 SPARC Ursa Major vs field SPARC.** Statistic: d = mean over UMa members of the per-galaxy mean residual minus
  the same over non-UMa SPARC (GB1's SPARC points, Upsilon 0.5 / 0.7, plain law). sigma = hypot(bootstrap over
  galaxies (4000 resamples, seed 7), 0.060), the 0.060 dex being the shared UMa distance error (e_D 2.5 / 18 Mpc,
  log10(1 + 2.5/18), full deep-regime sensitivity, conservative). Prediction P_k = the key's mean Delta difference
  between the two sets.
  - Key-free reading (reported and graded once): STEP IN UMa if d / sigma >= 3; NO STEP if |d| < 2 sigma.
  - Per key: KILLS the key if |d - P_k| >= 3 sigma; COMPATIBLE if < 2 sigma; else NO VERDICT. A key with
    |P_k| < 2 sigma is not tested by W1 on its switch (reported as "no switch in UMa").
- **W2 ellipticals by environment.** Under each key, the residual of NGC 720 (most isolated) and the Virgo pair are
  reported; graded only through G4.
- **W3 field UDG.** AGC 114905 (QX4/QX14): the law over-predicts it and its x_e is about 1e-3 a0; every key here has
  S = 0 there and predicts the plain law, so the record's miss stands. Reported, not graded (one galaxy, chi^2-based).

## 4. Labels

Per key: **PASSES ALL STATIC GATES** (G1-G8 PASS both footings and W1 not KILLS), **FAIL (rows)**, or **NOT GRADABLE**.

Lane label (plain), "environment carries the step":
- **YES** if any key passes all static gates on both footings and W1 does not kill it.
- **NO** if every key fails at least one row on either footing with power, and the failure survives the hard check
  (section 6).
- **NO POWER** otherwise.

A separate **switch reading** is stated: whether within-class environment contrasts (W1, G6 LG field vs satellites,
G7 KiDS isolated, G4 NGC 720 vs Virgo, W3) go the way an environment switch requires, row by row, independent of
amplitude. If the answer were YES, RESULT.md states what it would mean physically.

## 5. Known answers (a KA FAIL stops grading)

- KA1: GB1's L0 numbers reproduce from gb1.json (G1 Z and rms, G2 mean and rms, G3 counts, G4 mean, G5 mean and z, G6
  medians and CIs, G7 R, G8 uses) to 1e-9, both footings.
- KA2: QX24 reproduces from qx24.json: Delta_s and x_c (1e-9) per footing, and the seven ellipticals' x_e noclu and
  maxclu recomputed with the estimator (1e-9 relative).
- KA3: with F_env = 1 every key reproduces L0's rows exactly (identity check).

## 6. Verify a FAIL as hard as a PASS

For each failing row: (a) the row's number at F_env = 1 (plain law) and at the bracket readings; (b) whether any
F_env in [1, 100] could pass that row with the other rows' S kept, stated as a feasibility statement only (no
amplitude is changed by it); (c) the maxclu reading for M1. A FAIL that flips under (a)-(c) is reported as fragile.

## 7. MUTATE twin (separate outputs ev1_MUTATE.*)

Inverted switches (S -> 1 - S where S is not None) with each key's calibrated F_env. It must FAIL G1 or G6 on both
footings for every key; if it does not, the battery has no power for that key and the run says so.

## 8. Outputs

ev1_readings.py -> readings.json; ev1.py -> ev1.json / ev1.out; ev1.py --mutate -> ev1_MUTATE.json / .out.
RESULT.md: measure x gate x footing table, the label, and the switch reading. Any change after this freeze is
disclosed as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
