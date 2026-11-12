# CLOSE-2 FROZEN CRITERIA: grading PAR1's two open branches, and the union (2026-11-12)

Committed alone, before any script, derivation output or number. TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Read-only to every lane it cites (PAR1, WV1, SMF1, EDG1, AKS1, VCC1). Footings canonical
(a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy, a
gravitating field, never a particle. This lane recomputes no physics: every verdict is a read of a committed artifact
of the lane named, plus the two small consistency computations defined in section 3 (R5, R6).

## 0. Question

PAR1 (`closure_2026_11_10/PAR1_parent_action_spec/`, result origin 6be0bf30d1, A2 a238fb0fba) ended NO VERDICT on both
footings because it left two branches with no member graded:

- **B-Tm-fine** — a multi-valued (wave) carrier with the law keyed on the wave's own phase frame; PAR1's C15 leaves a
  wave mass window of [4.20e-24, 1.84e-23] eV (canonical; alt to 1.93e-23).
- **B-Tm-smooth** — the law on a separate smooth frame that follows the carrier's coarse-grained mean flow.

Two later lanes graded members: WV1 (`.../WV1_wave_dust_split_charge/`, V1 = the frame is Psi's phase; V2 = a separate
uncoupled frame) and SMF1 (`.../SMF1_smooth_frame_parent/`). This lane grades **both branches explicitly, per footing,
on two readings**, and states whether the union

    U = B-Ts (single-valued) U B-Tm-fine (wave-phase) U B-Tm-smooth (smooth-frame)

is closed, i.e. whether any parent action of the named class survives. B0 and B-L are carried for completeness; they are
not part of U.

## 1. Definitions adopted, read-only (PAR1 FROZEN_CRITERIA section 1 and 3)

- **Pi1-Pi4** as PAR1 froze them: local variational EP-respecting action; static galaxy limit is (A)'s law with v3s
  screening; counted once (form B); the cold component is pressureless dust on FRW at 5.41 Omega_b.
- **Branch membership is PAR1's, not this lane's.** PAR1's frozen section 3 assigns WV1's V1 to B-Tm-fine and WV1's V2
  to B0, and defines B-Tm-smooth as "a second, single-valued carrier that follows the cold field's coarse-grained mean
  frame" with a charge exchange (PAR1 section 3, item 3). SMF1's member is that definition written out.

## 2. Grading rule (frozen here, before any file is read)

Two axes, never pooled:

- **Footing:** canonical / alt.
- **Footing-of-record:** AS FROZEN (each lane's frozen criteria only) and UNDER AMENDMENTS (each lane's own post hoc
  amendments, A1 and A2, as committed).

Per branch, per footing, per footing-of-record, the branch verdict is one of:

| verdict | condition |
|---|---|
| **EMPTY (theorem)** | PAR1 graded the branch EMPTY with every check it names passing, in `par1_grade.json` |
| **MEMBER FAILS (part)** | a member of the branch was written as a full action in a named lane and graded with a failing part named, AND in that lane every known answer passed, every MUTATE arm bit, and the Lean file compiled with its false twin failing |
| **MEMBER HOLDS** | the same, with every graded part passing |
| **OPEN (no member)** | no member written and graded anywhere this lane can cite |
| **NO VERDICT** | the member lane's own label is NO VERDICT (a known answer failed, a MUTATE arm did not bite, or a deciding run did not finish) |

- A branch is **CLOSED** iff it is EMPTY (theorem) or MEMBER FAILS.
- The union U is **CLOSED** on a footing-of-record iff every branch of U is CLOSED there, and the escape audit of
  section 4 finds no item that a cited lane itself reports as surviving.
- Lane label follows PAR1 section 4: **CLASS EMPTY (theorem)**, **CANDIDATE STRUCTURE HOLDS / FAILS (name the part)**,
  or **NO VERDICT**. Because the two multi-valued branches are closed by member grading and not by a class theorem, the
  only labels available to this lane are CANDIDATE STRUCTURE FAILS and NO VERDICT; CLASS EMPTY is reported as
  unavailable if any branch is MEMBER FAILS rather than EMPTY.

**Pre-registered asymmetry, stated before reading:** the union is reported as closed only in the member sense. A
"closed by member" verdict is weaker than a "closed by theorem" verdict and must be stated that way, with the class of
re-specifications that no lane has written listed in section 4.

## 3. Checks (each a read of a committed artifact; R5 and R6 are computed here)

| id | what is checked | source file | pass condition |
|---|---|---|---|
| R1 | PAR1's branch labels, per footing, per reading (frozen / A1 / A2) | `PAR1_parent_action_spec/par1_grade.json` | fields present; B0 and B-L EMPTY on every reading |
| R2 | WV1's V1 and V2 labels and failing parts | `WV1_wave_dust_split_charge/wv1_grade.json`, `RESULT.md` | V2 FAIL on S1(c), S3(a), S3(b) on both footings, resting on no amendment |
| R3 | SMF1's label and failing parts | `SMF1_smooth_frame_parent/smf1_grade.json`, `RESULT.md` | S0a PASS, S0b and S0c FAIL, first fail S0; KA1-KA3 pass; MU1-MU3 bite; Lean and twin as recorded |
| R4 | EDG1's label (the held-edge-layer re-specification SMF1 flagged as ungraded) | `EDG1_held_edge_layer/edg1_grade.json`, `RESULT.md` | a failing part named, per footing |
| R5 | **m-window intersection (computed here).** PAR1 C15's window [m_min_record, m_max_C15] per footing against WV1's S2 lower bound m_c2_min (binding z = 1089). Report the overlap and the ratio m_c2_min / m_max_C15 | `par1_numbers.json` (`S15_m_min_record_forest_eV`, `S15.per_mass`), `wv1_s1s2.json` (`S2`) | reported either way; an empty overlap is a second, independent ground for B-Tm-fine |
| R6 | **scan coverage (computed here).** Map WV1's scanned nu grid to m (m c^2 = (nu_max * m(nu_max)) / nu, using WV1's own S1c rows) and state which scanned masses fall inside PAR1's window | `wv1_s1s2.json` S1c V1 rows, `par1_numbers.json` | the scan must cover the window with at least two points inside or bracketing it, else R5 carries B-Tm-fine alone |
| R7 | gate health of each member-grading lane (known answers, MUTATE, Lean) | `smf1_grade.json`, `wv1_grade.json`, PAR1 `par1_grade.json` checks | all true, else that branch is NO VERDICT |
| R8 | **supersession scan.** Any lane committed after 2026-11-10 that writes or grades a member of B-Tm-fine or B-Tm-smooth, or that reopens either branch | record-wide search for `B-Tm`, and for `WV1`/`SMF1`/`PAR1` in files newer than 2026-11-11 | any such claim is quoted; none may be silently dropped |

## 4. Escape audit (pre-registered; each item is reported, and U is CLOSED only if none is a surviving member of U)

- **E1.** SMF1's own flagged re-specification: "A re-specified branch, with the halo as the image of a held edge layer
  of real cold charge, is not graded here." → graded by EDG1.
- **E2.** A **collisionless** (kinetic, multi-stream, non-wave) carrier in B-Tm-fine's structure (law keyed on a
  fine-grained frame). SMF1 A1 shows a collisionless carrier does not escape S0b/S0c in the *smooth* structure; nothing
  grades it in the *fine* structure. Not a member of the named union ("wave-phase") but reported.
- **E3.** PAR1's B-Ts EMPTY rests on A1 (a post hoc sign correction to C8) and on two PROVISIONAL citations (Lax 1964;
  Dawson 1959), with 3D infall computed for the quadratic dust term only.
- **E4.** WV1's stated exit: a law whose phantom "appears instantly" needs matter coupled to the frame field (the
  RAQUAL / TeVeS family) — outside Pi1 and outside the record's E5.
- **E5.** Coverage not established: PAR1 A2's C16-C20 against the two multi-valued branches (M5, Theorem G, D-T');
  SMF1's S3 rows D-T' and V1.
- **E6.** WV1's S4 (static rows) not graded; S3(c) fails but is not decisive (M4 did not bite). Moot for the label
  (S3(b) fails) but reported.
- **E7.** Published wave-dust forest bounds (2e-21 eV and up) are PROVISIONAL and decide nothing. WV1's S2 bound is the
  record's own line, and carries WV1's own caveat: at z = 1089 the acoustic-peak-only scale (k <= 0.3/Mpc) would give
  about 7e-26 eV, which would reopen the window. R6 must cover this case.
- **E8.** EDG1's own disclosed gap: the clock's acceleration jump at R_s (LFS1 A4, the wall in the frame) is not
  addressed by the held-layer branch.
- **E9.** AKS1 (acceleration-keyed dissipation) and VCC1 are outside Pi1 by their own disclosures; reported only if they
  claim a surviving member of U.

## 5. Labels

- Per branch, per footing, per footing-of-record (a 2 x 2 grid).
- Union: **CLOSED (member sense)** / **NOT CLOSED**, each with the footing-of-record it holds on, and the escape-audit
  items that remain.
- Lane label, per footing, per footing-of-record.

## 6. Process

- `close2_grade.py` reads the committed JSON artifacts named in section 3 (read-only, no import of any lane's solver)
  and writes `close2_grade.out` / `close2_grade.json`. No new physics run, no Lean, no large output, under 1 GB and a
  few seconds.
- RESULT.md leads with the verdicts, then the branch grid, then the union, then the escape audit, then commits.
- Commits with explicit paths only.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
