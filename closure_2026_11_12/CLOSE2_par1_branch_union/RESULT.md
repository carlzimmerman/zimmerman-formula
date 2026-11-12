# CLOSE-2 RESULT: PAR1's two open branches graded, and the union (2026-11-12)

**Lane label — canonical / alt, as frozen: NO VERDICT / NO VERDICT.**
**Lane label — canonical / alt, under the post hoc amendments: CANDIDATE STRUCTURE FAILS / CANDIDATE STRUCTURE FAILS**
(first failing parts: B-Tm-fine, WV1's V1 at S3(b); B-Tm-smooth, SMF1 at S0).

**The union U = B-Ts (single-valued) + B-Tm-fine (wave-phase) + B-Tm-smooth (smooth-frame):**

| reading | canonical | alt |
|---|---|---|
| as frozen | **NOT CLOSED** (B-Ts OPEN, B-Tm-fine NO VERDICT) | **NOT CLOSED** (same) |
| under the amendments | **CLOSED, in the member sense** | **CLOSED, in the member sense** |

"Member sense" means: every branch is either EMPTY by PAR1's theorems or has its minimal member written as a full action
in a lane and graded with a failing part named. It is **not** a class theorem for the two multi-valued branches. No
parent action of the named class that has been written and graded survives, on either footing.

**Branch verdicts (both footings, both readings):**

| branch | as frozen | under amendments |
|---|---|---|
| B0 (law not keyed on the carrier) | EMPTY (theorem) | EMPTY (theorem); WV1's V2, a member, FAILS on S1(c), S3(a), S3(b) resting on no amendment |
| B-L (fixed length) | EMPTY (theorem) | EMPTY (theorem) |
| B-Ts (single-valued barotropic) | **OPEN** (PAR1's C8 sign line fails as frozen) | **EMPTY (theorem)** under PAR1 A1 (post hoc) |
| **B-Tm-fine (wave-phase)** | **NO VERDICT** (WV1's V1 as frozen: KA4(ii) FAILS; the S3(b) brackets do not finish) | **MEMBER FAILS — S3(b)**: R_s = 0 kpc at every scanned nu, log M_b 9.4 and 10.7; the window [nu_min, nu_max] is EMPTY |
| **B-Tm-smooth (smooth frame)** | **MEMBER FAILS — S0** (S0b Gauss, S0c starvation; both are frozen items) | **MEMBER FAILS — S0**; SMF1 A1 shows it is not wave-specific, so a collisionless carrier in the same structure fails S0 too |

**Answer in plain words.** PAR1 left two ways out and graded neither. Both are now graded, and both are closed, but each
on a different footing of evidence:

- **The wave-phase branch dies on the wave's own phase.** WV1's V1 is the minimal member: (A) with K(Q) removed plus one
  minimally coupled complex field, the law keyed on tau = -(hbar/m) arg Psi. Psi never becomes static where the law is
  seen: the static-frame radius is R_s = 0 kpc at log M_b 9.4 and 10.7, at every scanned mass, both footings. The
  scanned grid covers PAR1's whole open window — 4.72e-24 eV sits inside it and 1.89e-23 eV brackets its top (canonical
  window [4.203e-24, 1.840e-23] eV; alt [4.203e-24, 1.929e-23] eV) — and reaches down to 1.85e-26 eV. There is a second,
  independent ground: WV1's S2 applies the record's own Jeans line at z = 1089 and gives m c^2 >= 7.556e-23 eV
  (canonical; 7.554e-23 alt), which is 4.11 / 3.92 times above PAR1's C15 ceiling. The overlap is empty; no published
  forest bound is needed.
- **The smooth-frame branch dies on bookkeeping, before any wave physics.** SMF1 wrote PAR1's specification out as an
  action and graded it: the charge exchange cannot fill the law's halo in net (Gauss, exact — S0b) and is identically off
  where counted once holds (starvation, exact — S0c). Both are frozen gates, so this branch is closed as frozen, not only
  under an amendment. SMF1's A1 adds that neither gate is wave-specific: a collisionless carrier in the same structure
  fails both.

**What it would take to reopen the union.** Three things, each disclosed by the lane that left it open:

1. A B-Tm-fine member that is not a single complex field with the law on its phase (e.g. a carrier whose fine-grained
   frame is single-valued some other way). No such member has been written; a collisionless carrier has no phase to key
   on, so it is not a member of the named "wave-phase" leg at all (E2).
2. A re-specified B-Tm-smooth. SMF1 named this itself: "a re-specified branch, with the halo as the image of a held edge
   layer of real cold charge, is not graded here." EDG1 (2026-11-11) has since graded exactly that and it fails at E3 on
   both footings: infall delivers 19 to 38 times less angular momentum than a held shell needs, and 2.23 times less even
   in the most generous frozen bracket.
3. The single-valued leg. B-Ts is EMPTY only under PAR1's post hoc A1 (a sign correction to C8), and its steepening step
   uses two PROVISIONAL citations (Lax 1964; Dawson 1959) with 3D infall computed for the quadratic dust term only.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings never pooled; the footing-of-record
(as frozen / under amendments) is never pooled either. Cold dark energy is a gravitating field, never a particle.

## 1. What this lane did and did not do

This lane recomputes no physics. Every verdict is a read of a committed artifact of the lane named, plus two small
consistency computations (R5, the mass-window intersection; R6, the nu-scan coverage) defined in the frozen criteria and
run by `close2_grade.py` on the committed JSONs. No lane's solver was imported. The supersession scan (R8) searched the
record for any other file naming a B-Tm branch: 18 files, all belonging to PAR1, WV1, SMF1, EDG1 or this lane. No lane
committed after 2026-11-10 writes or grades another member of either branch.

## 2. The branch grid (computed; `close2_grade.out`)

| branch | canonical, frozen | alt, frozen | canonical, amendments | alt, amendments |
|---|---|---|---|---|
| B0 | EMPTY (theorem) | EMPTY (theorem) | EMPTY (theorem) | EMPTY (theorem) |
| B-L | EMPTY (theorem) | EMPTY (theorem) | EMPTY (theorem) | EMPTY (theorem) |
| B-Ts | OPEN (no member) | OPEN (no member) | EMPTY (theorem, PAR1 A1) | EMPTY (theorem, PAR1 A1) |
| B-Tm-fine | NO VERDICT | NO VERDICT | MEMBER FAILS (S3(b)) | MEMBER FAILS (S3(b)) |
| B-Tm-smooth | MEMBER FAILS (S0) | MEMBER FAILS (S0) | MEMBER FAILS (S0) | MEMBER FAILS (S0) |

### 2.1 B-Tm-fine, in detail

Graded member: WV1's **V1** (`WV1_wave_dust_split_charge/`, action in its RESULT.md: (A) with K(Q) removed plus a
minimally coupled complex field, tau = -(hbar/m) arg Psi). PAR1's frozen section 3 assigns V1 to B-Tm-fine, so the
membership is PAR1's, not this lane's.

| item | canonical | alt |
|---|---|---|
| S3(b) R_s at nu_max, log M_b 9.4 / 10.7 | 0 / 0 kpc (needed >= 81 / 23 and >= 362 / 71) | 0 / 0 kpc |
| S3(b) window [nu_min, nu_max] | EMPTY (nu_min does not exist; every scanned nu fails) | EMPTY |
| S3(a) at 10.7 | FAIL (6 narrow maxima, resolution of the 0.07 kpc core) | FAIL (3) |
| S3(c) | FAIL, not decisive (M4 does not bite: 0.272 / 0.332 of Psi's mass) | FAIL, not decisive (0.264 / 0.323) |
| S1(c) FRW | PASS (no ghost; max rate / Jeans = 1.000000000000) | PASS |
| R5: PAR1's window vs WV1's S2 | [4.203e-24, 1.840e-23] vs >= 7.556e-23 eV: overlap empty, ratio 4.11 | [4.203e-24, 1.929e-23] vs >= 7.554e-23: empty, 3.92 |
| R6: scanned m (eV) | 1.845e-26, 7.379e-26, 2.952e-25, 1.181e-24, **4.722e-24**, 1.889e-23, 7.556e-23 | same to 3 digits |
| window covered by the scan | yes: one point inside (canonical), two inside (alt), points above and below | yes |

Two independent grounds, on both footings: (i) the member fails at S3(b) across the whole scanned mass range; (ii) the
mass window PAR1 left open is empty once the record's own Jeans line is applied at z = 1089.

**Reading discipline.** WV1 reports three readings of V1 and this lane carries all three:

- **As frozen: NO VERDICT.** WV1's known answer KA4(ii) FAILS as frozen, and under A1 alone the nu_max bracket runs do
  not finish, so S3(b) and the window are ungraded. This lane cannot adopt a fail from an ungraded row.
- **Under A1 alone: STRUCTURE FAILS on S3(a) only** — a resolution failure at log M_b 10.7, not physics. Reported, not
  adopted here as the decisive ground.
- **Under A1 + A2: STRUCTURE FAILS on S3(b) (and S3(a) at 10.7)** — adopted.

### 2.2 B-Tm-smooth, in detail

Graded member: SMF1's **SMF1-M** (`SMF1_smooth_frame_parent/`), the full action of PAR1's section 3 item 3 (frame (A),
complex Psi, alignment, khronometric stiffness, and the charge exchange with only the sum conserved; 4 new constants
beyond (A)).

| item | canonical | alt |
|---|---|---|
| S0a static reduction, rho = rho_b + rho_Psi | PASS (residual 0) | PASS |
| **S0b** net fill of the polarization charge | **FAIL** — identically 0 (Gauss) | **FAIL** |
| **S0c** fill where counted once holds | **FAIL** — S = 0 at rho_Psi = 0 | **FAIL** |
| first failing part | S0 | S0 |
| S1 FRW / static / GW (would-be items) | PASS (Jeans root -K(n_d + rho) exact; c_T = c) | PASS |
| S3 C16 / C17 | PASS, with D-T' and V1 NOT ESTABLISHED | PASS |
| KA1-KA3 / MU1-MU3 / Lean | all pass / all bite / exit 0, twin exit 1 | same |
| A1: wave-specific? | No; a collisionless carrier fails S0b and S0c too | same |

Both failing gates are **frozen** items of SMF1's criteria, so this branch is closed on the as-frozen footing as well.
It is the only one of the five that is.

## 3. The escape audit (pre-registered in section 4 of the criteria)

| id | item | status |
|---|---|---|
| E1 | SMF1's flagged re-specification: the halo as the image of a held edge layer of real cold charge | **GRADED, FAILS** — EDG1: FAILS AT E3 / FAILS AT E3 (reading U: FAILS AT E1). Infall is 19-38 x short of the spin a held shell needs; 2.23 x short in the most generous frozen bracket. E0 (books) passes exactly, E1 (supply) passes, E2(a) frame dust needs c_s^2 < 0, E2(b) no isotropic pressure holds a hollow shell, E2(d) rotation gives no support at the poles. Resting on a PROVISIONAL spin number (lambda' = 0.035, Bullock+2001). EDG1's own residual gap: LFS1 A4's acceleration jump at R_s is not addressed |
| E2 | a collisionless carrier in the **fine** structure (no phase) | **NOT GRADED**, and not a member of the named "wave-phase" leg. SMF1 A1 covers a collisionless carrier only in the smooth structure |
| E3 | B-Ts's EMPTY rests on PAR1 A1 (post hoc) plus Lax 1964 and Dawson 1959 (PROVISIONAL), 3D infall for the quadratic dust term only | **OPEN CAVEAT** on the single-valued leg |
| E4 | RAQUAL / TeVeS (matter coupled to the frame field) | **OUTSIDE Pi1** and outside the record's E5 (WV1's own reading) |
| E5 | PAR1 A2's C16-C20 (M5, Theorem G, D-T') against the multi-valued branches; SMF1's S3 rows D-T' and V1 | **NOT ESTABLISHED** in both lanes |
| E6 | WV1's S4 (static rows) not graded; S3(c) fails but is not decisive (M4 does not bite) | **MOOT** — S3(b) already fails |
| E7 | published forest bounds (2e-21 eV and up) PROVISIONAL; WV1's z = 1089 line would fall to about 7e-26 eV on the acoustic-peak-only scale, reopening the window | **CAVEAT, COVERED**: the scanned grid reaches 7.379e-26 eV, so the member is graded there too (R_s = 0) |
| E8 | the clock's acceleration jump at R_s (LFS1 A4 wall) | **OPEN** — EDG1 does not address it |
| E9 | AKS1 (dissipation), VCC1 | outside Pi1 by their own disclosures; neither claims a surviving member (VCC1 cites PAR1's B0 as EMPTY) |

## 4. Table of the checks

| id | check | result |
|---|---|---|
| R1 | PAR1's branch labels, frozen / A1 / A2, both footings | B0, B-L EMPTY on all three; B-Ts OPEN frozen, EMPTY under A1/A2; both B-Tm branches OPEN (PAR1 graded no member) |
| R2 | WV1's V1 / V2 labels | V2 STRUCTURE FAILS on S1(c), S3(a), S3(b) (rests on no amendment; V2 is in B0, counted here for completeness, not as a B-Tm-smooth member — it has no exchange, no alignment and no ell) |
| R3 | SMF1's label and gates | STRUCTURE FAILS (S0); S0a PASS, S0b/S0c FAIL; KA1-KA3 pass; MU1-MU3 bite; Lean exit 0, twin exit 1 (6 of 6 false statements fail) |
| R4 | EDG1 | FAILS AT E3 / FAILS AT E3 (reading U: FAILS AT E1); KA1-KA4 pass; MU1-MU4 bite (MU3 shows the branch would live only with j set by hand) |
| R5 | mass-window intersection (computed here) | empty, both footings; ratio 4.11 / 3.92 |
| R6 | nu-scan coverage (computed here) | window covered, both footings; caveat mass 7.379e-26 eV scanned |
| R7 | gate health of the member-grading lanes | SMF1 clean. WV1: M3 bites (guards the decisive S3(b)); **M4 does not bite** (guards S3(c), which WV1's frozen criteria make non-decisive) — handled under AMENDMENT A1 |
| R8 | supersession / survivor scan | 18 files name a B-Tm branch; all belong to PAR1, WV1, SMF1, EDG1 or this lane. No later member, no reopening |

## 5. Disclosures

- **AMENDMENT A1 (post hoc, committed alone before the grading script was written or run).** The frozen R7 required every
  MUTATE arm of a member lane to bite. WV1's M4 does not, and WV1's own frozen criteria make the row it guards (S3(c))
  non-decisive. Applying R7 literally would have returned NO VERDICT for B-Tm-fine on the strength of a control attached
  to a row no lane uses to set a label. A1 refines R7 to "arms guarding decisive rows" (R7a), with non-decisive arms
  disclosed (R7b) and frozen known answers read in their A1-replaced form (R7c). Reported under both readings: under
  frozen R7, B-Tm-fine would read NO VERDICT even under the amendments.
- **The decisive B-Tm-fine verdict is post hoc.** WV1's S3(b) grading and the empty window rest on WV1's A1 (a known
  answer replaced) and A2 (four runs graded on the outputs they reached, one of them stopped at z = 2). As frozen, V1 is
  NO VERDICT and this lane reports NO VERDICT with it.
- **B-Ts's EMPTY is post hoc** (PAR1 A1, a sign correction to C8) and rests on two PROVISIONAL citations. It is the
  single-valued leg of the union, and it is the weakest of the three legs.
- **The union is closed in the member sense only.** No theorem empties B-Tm-fine or B-Tm-smooth; each is closed by its
  minimal member. A member of either family that no lane has written is ungraded by definition. The named union does not
  include a collisionless carrier keyed on a fine-grained frame (E2) or matter coupled to the frame field (E4, outside
  Pi1).
- **EDG1's E3 rests on a PROVISIONAL spin number** (lambda' = 0.035 and its generous bracket 0.1, quoted from memory and
  not fetched). Its E2(c) stability is a fluid stand-in, not a Vlasov computation. Both are EDG1's own disclosures.
- **WV1's 10.7 runs were paused and resumed** by the coordinating session (SIGSTOP / SIGCONT, checkpoints by wall time);
  WV1 states no number can have changed. This lane did not re-run them.
- **Not pushed to origin.** Commit ids below are local; this lane made no push, because other lanes hold uncommitted
  modifications in this worktree.
- **Read-only.** This lane wrote only in its own directory.

## 6. Files and re-run

`FROZEN_CRITERIA.md` (alone, first); `AMENDMENT_A1.md` (alone, post hoc); `close2_grade.py` ->
`close2_grade.out` / `close2_grade.json` (a few seconds, no solver, reads six committed JSON files read-only);
`RESULT.md`.

Inputs read (read-only, all under `closure_2026_11_10/`): `PAR1_parent_action_spec/par1_grade.json`,
`PAR1_parent_action_spec/par1_numbers.json`, `WV1_wave_dust_split_charge/wv1_grade.json`,
`WV1_wave_dust_split_charge/wv1_s1s2.json`, `SMF1_smooth_frame_parent/smf1_grade.json`,
`EDG1_held_edge_layer/edg1_grade.json`.

Commits (local): criteria b8acc6c3bc; A1 99f9497fc7.

Source lanes (local / origin): PAR1 criteria 51522963e0 / b90f959699, A1 427bc818f6 / 351a4d37eb, result c8d1463e35 /
6be0bf30d1, A2 a7cac068bf / 8c13e5adcb, A2 result f667d68b43 / a238fb0fba; WV1 criteria 174870d2fe / 3fc79b5800, A1
589c2738df / 90ebdb2e5c, A2 022897766a / 45a1c9776d, result 88f3ccbe4b / fb421c3adb; SMF1 criteria 9586b716e6 /
b3879c6cad, result 8339a435fe / 884ddfb854, A1 cfa91d3feb / 10e7d72ac3, A1 result d074525445 / 92a0855574; EDG1
criteria f57da1f35c / 79704cbee3, result 0a7fa7d6b5 / 7e335c1727.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
