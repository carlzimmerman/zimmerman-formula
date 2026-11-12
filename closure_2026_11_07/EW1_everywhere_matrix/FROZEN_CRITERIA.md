# EW1 everywhere matrix: FROZEN CRITERIA, committed alone before any matrix cell or computed number

Owner 11-07: "we need to get all actions that work everywhere"; the owner does not care where the answer lands. This
lane overrides DIRECTION_2026_11_07.md's STOP list for itself only: it is a read-across plus at most two cheap computed
rows; it opens no sector and adopts nothing. Kappa = 1/2 FITTED; not theory closed. Footings canonical a0 = 9.3603e-11,
alt a0 = 1.1312e-10 m/s^2, never pooled. No LCDM inputs in any framework cell. Rules of SWARM_BRIEF.md bind.
Lane id: `ls closure_2026_11_07 | grep EW1` and `git log origin/main | grep EW1` empty at freeze.

## 1. The matrix

Rows (each an action, an action class or a sector extension; one row each):
R01 AQUAL/QUMOND (+RAQUAL), R02 BIMOND, R03 TeVeS, R04 AeST (Skordis-Zlosnik 2021), R05 the record's v4 AeST form,
R06 Einstein-aether MOND, R07 khronon (Blanchet-Marsat), R08 superfluid effective field (Berezhiani-Khoury, no
particle), R09 nonlocal metric MOND (DEW), R10 v3s (adopted, scoped), R11 AC2q + Pi^6 blend (QX19 one action),
R12 route E cold dark energy (candidate B / FG1; retired 11-01), R13 v3s K(Q) dust unpinned (KD1, wall 1),
R14 QX7 switched cold dark energy (iter_4 window, iter_5-7), R15 QX27 tail-retention sector, R16 QX28 two-phase
superfluid (BK class), R17 QX29 dipolar medium, R18 HF1/HC1 light thermal fermion (11.1 eV; no-particle rule lifted
for those lanes only), R19 SE1 shock-entropy sector, R20 QX12 iter_3 warm sea / QX13 virial floor, R21 PBH extra mass
(PB1-PB4), R22 MOND + ~11 eV sterile neutrinos (nuHDM, literature), R23 LCDM, COMPARISON-ONLY.
Rows added later only if a record lane graded an action not listed (named in README with its lane). 11-07 labels from closure_2026_11_07/CLOSURE_2026_11_07.md (95435f152c) are read in; WL1 (closure_2026_11_07/WL1_web_law_switch/, the two-switch door) is cited if on origin when the matrix is written, else marked pending.

Columns: C01 SPARC/RAR; C02 Cassini/PPN/Solar System; C03 c_T (GW170817); C04 galaxy lensing = dynamics;
C05 wide binaries (STATUS ONLY, excluded from the pass test); C06 hot early types / X-ray ellipticals; C07 groups;
C08 X-COP clusters; C09 Bullet-type offsets; C10 dSph classes; C11 UDGs (AGC 114905, Malin 1, Coma UDGs: PASS only
if all three pass); C12 primary CMB; C13 CMB lensing; C14 linear growth / KiDS; C15 BBN; C16 causality and
well-posedness; C17 a0 = kappa c sqrt(G rho_DE) tie (DERIVED / BY HAND / ABSENT).

Cell vocabulary: PASS, FAIL, NO VERDICT (frozen lane gave none), OPEN (waits on data), UNGRADED (no lane, no published
result found), N/A (not defined for the row), and for C17 DERIVED / BY HAND / ABSENT. Each cell carries its source
(lane id + commit, or a literature reference). Literature cells carry [lit, PROVISIONAL] (memory or earlier web
snippets in the record; no new download). Where footings differ: "canonical / alt". A cell takes the record's frozen
label; a post-data reading is shown only where the lane gives one and is marked "reading". Where the record and the
literature disagree, the record's frozen label fills the cell and the literature is noted.
LCDM row: COMPARISON-ONLY, graded on the same columns with its own published fits [lit, PROVISIONAL]; no LCDM
quantity enters any framework cell.

## 2. Answers, computed by script from matrix.csv (ew1_matrix.py)

- Q1: a row passes every column iff every cell in C01-C04, C06-C16 is PASS and C17 is DERIVED. Reported a second time
  with C17 relaxed to BY HAND. NO VERDICT, OPEN, UNGRADED, N/A and "PASS (scoped)" count as not passing; "PASS
  (scoped)" is listed separately. LCDM is reported but never counted as a framework answer.
- Q2: the minimal set of framework rows (LCDM excluded; also reported with LCDM) whose union of PASS cells covers every
  coverable column, by exhaustive search over subsets in increasing size; all minimal sets are listed. Columns no row
  passes are named as uncovered.
- Q3: every UNGRADED / NO VERDICT / OPEN cell whose flip to PASS would change the Q1 answer for its row (the row's only
  non-pass cells) or shrink the Q2 cover; listed by script.
- Script KA: the matrix parses with 23 rows x 17 columns, every cell non-empty with a source. MUTATE (--mutate): a
  planted row with every cell PASS/DERIVED must make Q1 YES with that row and Q2 size 1; and deleting the C09 Bullet
  column's only PASS row(s) must make C09 uncovered. Both must change the answer, or the script exits 1.

## 3. Computed cells (only if the record's machinery does it in minutes)

Two static forms are run through GB1's battery (closure_2026_11_06/GB1_all_gates_battery/gb1.py, exec'd read-only,
lines unchanged), gates G2 X-COP, G3 groups, G4 ellipticals, G5 Coma UDGs, G6 dSph classes, G7 KiDS split, both footings:
- E1 superfluid effective field (R08): g = g_N + sqrt(a0 g_N).
- E2 QUMOND beta = 2.5: nu = (1 + y^-2.5)^(1/5), y = g_N/a0, the D7c member that is the only non-v3s static form
  passing Cassini Q2 on canonical (AX1): it fills R02 BIMOND and R09 DEW static cells (their static limit is QUMOND
  with that nu, AX1's reading).
No constant is chosen: both forms are fixed above. G1 SPARC and G8 Solar System for these rows are NOT taken from GB1
(GB1's G8 assumes v3s screening); they come from AX1 / D7c. GB1's G1 numbers are reported only.
- KA: the law written through the same delta path reproduces GB1's L0 G2-G7 numbers to 1e-12 on both footings, and
  GB1's own KA1-KA6 pass.
- MUTATE (--mutate): Newton (g = g_N) through the same path must FAIL G2 on both footings (GB1's Newton twin gives
  +0.937); if it does not, no computed cell is used.
- Rerun byte-identical JSON. nice -n 15, one thread, minutes.
These cells change a label only from UNGRADED to PASS/FAIL. If either form passed G2-G7, the README must say so
first.

Kappa = 1/2 FITTED; not theory closed.
