# EW1: the everywhere matrix. NO ROW PASSES EVERY COLUMN; no union of record rows covers UDGs, causality or a derived a0

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2,
never pooled. LCDM is a COMPARISON-ONLY row: its cells are its own published fits, and no LCDM quantity enters any
framework cell. The owner's 11-07 ask ("all actions that work everywhere") overrides DIRECTION_2026_11_07.md's STOP
list for this lane only. EW1 opens no sector.

- Criteria: FROZEN_CRITERIA.md (723304d2e9), committed and pushed alone before any cell or number.
- Matrix: matrix.tsv. It has 23 rows x 17 columns, and every cell carries its label and its source (lane + commit, or
  a literature reference).
- Answers: ew1_matrix.py -> ew1_matrix.json / .out.
  - MUTATE twin: ew1_matrix_MUTATE.*. A planted all-pass row gives Q1 YES and a Q2 cover of size 1; emptying the
    Bullet column leaves it uncovered. BITES.
- Computed cells: ew1_static.py -> ew1_static.json / .out (run_main.txt).
  - It runs GB1's battery read-only, with only the candidate list and the output paths swapped. GB1's KA1-KA6 pass.
    (KA6 passes "to the quoted rounding", GB1's own disclosed rounding slip.)
  - The law written through the delta path reproduces GB1's committed L0 G2-G7 numbers to 0.0. Reruns are
    byte-identical.
  - MUTATE twin, Newton through the same path: ew1_static_MUTATE.*. It FAILS G2 on both footings. BITES.
  - Run: nice 15, one thread, 3 s.
- Literature cells carry [lit, PROVISIONAL]. They come from memory or the record's earlier web snippets. Nothing was
  downloaded.
- 11-07 labels are read from CLOSURE_2026_11_07.md (95435f152c).
- The two-switch door (SV5 item 4) is graded by WL1 (closure_2026_11_07/WL1_web_law_switch/), which had only its criteria on
  origin when this was written (WL1 FROZEN CRITERIA c371c8ce59, no result). EW3 (520ed75443) keeps it as PENDING WL1. It is not a row here.

## Columns

| Column | Gate |
|---|---|
| C01 | SPARC/RAR |
| C02 | Cassini/PPN/Solar System |
| C03 | c_T (GW170817) |
| C04 | galaxy lensing = dynamics |
| C05 | wide binaries (status only, not in the pass test) |
| C06 | X-ray ellipticals |
| C07 | groups |
| C08 | X-COP |
| C09 | Bullet-type offsets |
| C10 | dSph classes |
| C11 | UDGs (AGC 114905 + Malin 1 + Coma, all three) |
| C12 | primary CMB |
| C13 | CMB lensing |
| C14 | linear growth / KiDS |
| C15 | BBN |
| C16 | causality and well-posedness |
| C17 | a0 = kappa c sqrt(G rho_DE) tie |

## Matrix (labels only; full text and sources in matrix.tsv)

Key:
- Pass labels: P pass; P* pass, scoped.
- Fail labels: F fail; T tension.
- Mixed labels: split = canonical/alt or members differ; mix = rules differ.
- No label: NV no verdict; — ungraded; n/a not defined for the row.
- C17 only: D derived, hand by hand, abs absent.

| row | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 AQUAL/QUMOND (+RAQUAL) | P | F | n/a | F | open | F | F | F | F | F | F | F | F | F | P | n/a | hand |
| R02 BIMOND (Milgrom 2009) | split | split | F | P | open | F | F | F | — | F | F | — | — | — | — | — | hand |
| R03 TeVeS | P | F | F | P | open | F | F | F | F | F | F | P | — | P | P | F | hand |
| R04 AeST (Skordis-Zlosnik 2021) | P | F | P | P | open | — | — | — | — | — | — | P | — | P | P | F | hand |
| R05 record v4 AeST form | — | — | — | — | open | — | — | — | — | — | — | — | — | F | — | F | hand |
| R06 Einstein-aether MOND (Zlosnik-Ferreira-Starkman 2007) | P | F | F | P | open | F | F | F | F | F | F | — | — | — | — | — | hand |
| R07 khronon (Blanchet-Marsat 2011) | P | F | P | P | open | F | F | F | F | F | F | — | — | — | — | — | hand |
| R08 superfluid effective field (BK, no particle) | F | F | — | F | open | P | F | F | — | F | F | n/a | n/a | n/a | n/a | — | hand |
| R09 nonlocal metric MOND (DEW) | P | split | — | P | open | F | F | F | — | F | F | — | — | — | — | — | hand |
| R10 v3s (adopted, scoped) | P | P | P | P | open | F | F | F | F | F | F | F | F | F | — | F | hand |
| R11 AC2q + Pi^6 blend (QX19 one action) | P | P | P | P | open | F | F | F | F | F | F | F | F | F | — | P* | hand |
| R12 route E cold dark energy (candidate B / FG1; retired 11-01) | mix | — | — | F | open | — | P | mix | P | F | mix | P | — | F | — | — | hand |
| R13 v3s K(Q) dust unpinned (KD1, wall 1) | F | P | P | P | open | F | F | F | — | F | F | P | P | P | P | — | hand |
| R14 QX7 switched cold dark energy (iter_4 window; iter_5-7) | P | — | P | F | open | — | F | F | — | — | — | P | P* | F | — | — | hand |
| R15 QX27 tail-retention sector | split | — | — | P | open | P | P | P | — | P | — | — | F | F | — | F | hand |
| R16 QX28 two-phase superfluid (BK class) | P | F | — | P | open | F | F | F | NV | P | — | F | F | F | — | — | hand |
| R17 QX29 dipolar medium | mix | F | — | mix | open | mix | mix | F | NV | mix | — | — | P | P | — | F | hand |
| R18 HF1/HC1 light thermal fermion 11.1 eV | P | P | P | — | open | F | F | F | — | F | F | F | F | F | — | — | hand |
| R19 SE1 shock-entropy sector (wall 4) | F | — | P | F | open | F | F | F | — | F | F | — | P | — | P | P* | hand |
| R20 QX12 iter_3 warm sea / QX13 virial floor | P | — | P | P | open | — | F | F | — | — | — | — | F | — | — | — | hand |
| R21 PBH extra mass (PB1-PB4) | F | — | P | — | open | — | — | F | F | — | F | — | — | F | — | — | hand |
| R22 MOND + ~11 eV sterile neutrinos (nuHDM, literature; record test = HC1) | P | F | — | — | open | F | F | F | P | F | F | split | F | F | T | — | hand |
| R23 LCDM (COMPARISON-ONLY, own published fits) | P | P | P | P | open | P | P | P | P | P | T | P | P | T | T | P | abs |

## Computed this lane (EW1 E1, E2; GB1 lines, both footings)

| Static form | G2 X-COP | G3 groups | G4 ellipticals | G5 Coma UDGs | G6 bright M31 dSph | G7 KiDS split |
|---|---|---|---|---|---|---|
| E1 BK effective g = g_N + sqrt(a0 g_N) | FAIL +0.406 / +0.377 | FAIL 0 / 0-1 of 20 | **PASS +0.123 / +0.103** | FAIL +1.104 / +1.062 | FAIL +0.248 / +0.236 | FAIL R +0.158 |
| E2 QUMOND beta 2.5 (BIMOND / DEW Cassini survivor) | FAIL +0.557 / +0.517 | FAIL 0 / 0 | FAIL +0.321 / +0.302 | FAIL +1.139 / +1.094 | FAIL +0.123 / +0.112 | FAIL R +0.158 |

These G1 and G8 cells are not graded here. They come from AX1 / D7c, as frozen.
- GB1's fixed-Upsilon G1 reads E2 FAIL on both footings: rms 0.182 / 0.165 against lines 0.146 / 0.143. D7c's paired
  statistic passes it. This is a reading only.
- E1's sharper boost at y ~ 1 is the only thing that moves the ellipticals inside the 0.15 line. Even so, it still
  under-predicts X-COP by about 0.4 dex, and it fails the Solar System by about 1e7 (AX1).
- The beta 2.5 form is the only non-v3s static form that passes Cassini (canonical only). It is worse than the law on
  every hot row.

## Answers

**(1) Does any row pass every column? No.**
- No framework row passes. That holds with C17 required to be DERIVED, and also with BY HAND accepted.
- The closest rows are listed below. "Non-pass" counts C17 by hand as passing.

| Row | Non-pass cells | What fails |
|---|---|---|
| R13 KD1 K(Q) dust | 8 | passes the CMB, CMB lensing, growth, BBN and the Solar System, and fails every galaxy and cluster row |
| R04 AeST | 9 | mostly UNGRADED; Cassini fails on AX1 |
| R03 TeVeS | 10 | c_T fails |
| R10 v3s, R11 AC2q + blend, R15 QX27 | 11 each | see the matrix |

- **The LCDM comparison row also misses four columns:**
  - C11: AGC 114905 tension;
  - C14: KiDS S8 tension;
  - C15: Li-7;
  - C17: no a0 scale at all.
- The v3s and AC2q rows pass C01-C04, with C05 still waiting on DR4. On every other physics column they FAIL, apart
  from BBN (UNGRADED) and AC2q's scoped well-posedness. These rows are the law's measured boundary, as in
  CLOSURE_2026_11_07.md.

**(2) Minimal union, and what one action would have to combine.**
- Framework rows only. The exhaustive search gives one minimal set, of size 3: **R13 (KD1 K(Q) dust) + R15 (QX27
  tail-retention sector) + R22 (nuHDM)**.
  - R13 supplies C02, C03, C04, C12, C13, C14 and C15.
  - R15 supplies C06, C07, C08 and C10 (X-COP at n 3.5-4, both footings).
  - R22 supplies C01 and the Bullet.
- R22 is a literature row, and it supplies the Bullet only through Angus+2007 [lit, PROVISIONAL]. On record-only rows,
  the Bullet comes from route E's pre-FG1 harness (R12). SPARC then has to come from v3s / AC2q. By inspection the
  cover is four rows: R10 or R11, R12, R13, R15.
- **Three columns stay uncovered by every framework row:**
  - C11 UDGs: no row passes AGC 114905, Malin 1 and Coma together.
  - C16: no row is causal and well-posed without scope. AC2q + blend is P* and fails the light cone at a tiny level
    (SV2).
  - C17: a0 is derived in no row.
- Adding LCDM gives covers of size 2 (R23 + R03 / R04 / R13), with C11 and C17 still open.
- **The single action would have to be:**
  - v3s/AC2q's screened law in cold, isolated systems;
  - plus a component that is cold and Jeans-free at z 3400 like R13's dust (CMB, lensing, growth, BBN), but kept
    out of discs;
  - plus R15's retention, which is velocity-tail and escape-speed keyed, so that hot hosts hold about 4x the
    baryons and discs hold almost nothing;
  - plus a collisionless offset in mergers.
- **The record says these pieces contradict each other:**
  - R13's dust is captured by every well, discs included (wall 1).
  - R15's retention violates Liouville by 1e3-7e3x and fails growth plus the forest (QX27 G6/G8).
  - A cold-early component that tracks host temperature has nothing to keep it out of discs. This is the common
    reason in ALL_GATES_NOGO.
- So the cover is a list of requirements, not a candidate. No row, and no graded combination, supplies the
  Liouville-legal mechanism that would join R13's cosmology to R15's statics.

**(3) UNGRADED or open cells that would change the answer.**
- No single cell flips Q1 for any row. Every framework row has at least one frozen FAIL, so no grading of open cells
  makes a row pass everywhere.
- Some open cells would change the Q2 uncovered set:
  - **C11 UDGs:** Coma is UNGRADED for QX27 (R15), QX28, QX29, QX7 and QX12/QX13. AeST and the record's v4 AeST are
    UNGRADED. Route E is MIXED (Coma passes under candidate B's ownership rule, CFG31). AGC 114905 and Malin 1 are
    not graded there.
    - The cell most able to matter is QX27 on Coma, because R15 is the cover's static piece.
    - It cannot be done in minutes. Coma UDGs need retention inside Coma's potential, which QX27's per-host rule does
      not define, so it is left UNGRADED.
    - Even a pass would leave AGC 114905 and Malin 1, which every row with a label fails.
  - **C16 causality / well-posedness:** UNGRADED for BIMOND, Einstein-aether, khronon, DEW, the BK field, KD1, QX7,
    QX28, HC1, PB and nuHDM.
    - AC2q + blend's well-posedness is scoped: non-radial modes are untested, MS3 is running, and the light-cone
      FAIL is SV2's.
    - None of these rows passes the other columns, so a C16 pass changes the cover only, not Q1.
  - **C17:** no open cell. kappa is proved not derivable from the premises (KAPPA_LOGIC), and every class puts a0 in
    by hand (AX1 G5). This column stays uncovered unless a new principle supplies C3^2 rho_vac = 128 pi F^3
    (SELECTION_IMPASSE).
- Other cells that are pending but would not change the answer:
  - C05 wide binaries: DR4 around 12-02, status only.
  - R11's moving-Sun cell (MS3, its FINAL label pending).
  - R10/R11 BBN (UNGRADED; it can only add a FAIL).
  - WL1's two-switch door. If WL1 passes, its row would need checking against C06-C11 and C16 here before anything
    changes.

## What this lane could not do
- It computed no literature-row cell for the relativistic MOND classes beyond the two static forms. AeST and TeVeS
  hot-system rows are UNGRADED / carried, and no X-COP-level AeST test was found.
- It ran no merger (Bullet) for any record row. QX28 and QX29 say NOT EVALUABLE, and the plain law's Bullet FAIL is
  the 09-03 sweep's phantom-only reading.
- LCDM and nuHDM cells are from memory [lit, PROVISIONAL]. The nuHDM cluster cell takes the record's HC1 FAIL, while
  the literature (Angus+2008/2010) reports outer-cluster fits. The conflict is noted, not resolved.

Kappa = 1/2 FITTED; not theory closed.
