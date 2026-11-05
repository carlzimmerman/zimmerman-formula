# Handoff to astra, 2026-11-04: one index for every lane handed over today

Written at the owner's request ("create handoff instructions for all the lanes we are handing off to astra"). Five separate briefs went to astra on 11-04. This file lists their lanes once each, merges the overlaps, and carries the corrections that landed after they were written. It is a brief, not a result: the lane READMEs and the five source briefs are the record. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## The five source briefs (read in this order)
| tag | file | commit | covers |
|---|---|---|---|
| **M** | `ASTRA_HANDOFF_2026-11-04_FROM_CLAUDE.md` | c7c8dc8186 | state, what 11-02 to 11-04 settled, lanes A1-A8 |
| **F** | `ASTRA_HANDOFF_2026-11-04_FINISH_PUSH.md` | 6038dc476d, 08708f8595 | house rules, dated events, FN lanes 1-7, "not to redo" |
| **B** | `ASTRA_HANDOFF_2026-11-04_STATUS_BOARD.md` | bd23b19cfc | board on main, B1 (LW1 fold), B2 (carried tiles) |
| **C** | `ASTRA_HANDOFF_2026-11-04_COMPLETE_THEORY_FROM_CLAUDE.md` | dcfcd5f73e, 6f785b49b9 | CT1-CT18, C'' lanes 1-5 |
| **S** | `sol61_push/CLAUDE_TO_ASTRA_HANDOFF_2026-11-04.md` | cc8dbeba67 | covariant push and rebuild lanes, W1, X1 |

Not astra's: `cq_lanes_2026_11_04/HANDOFF_2026-11-04.md` (CQ8, the L* top edge, the new paper) is addressed to the next Claude session, and FN4's rows (IC 1613, Local Group dwarfs, MW vertical force, KiDS) belong to the "Next steps for theory" session except where F hands a piece over below. astra's own AZ lanes from its 11-03 goal (AZ27, AZ29, AZC1) carry on as astra sets them; nothing here replaces them.

## Corrections since the briefs were written (these win over the briefs)
1. **C'' fails G0** (CT14, 6f785b49b9). With the khronon velocity kept, the tie enters the kinetic matrix and grows as k above g 2.7e-9 to 1.9e-7 m/s^2, reached in inner galaxies; only exact Lambda escapes. C's "result worth taking forward" is overturned. A healthy dynamical rho_DE tie in v3s is **not** established.
2. **PAPER67 v1.2 is deposited**, DOI 10.5281/zenodo.23968171 (493b7d00ff). M and B still call it a draft. The status board's footer (`explainers/make_status_board.py:638`, `explainers/crispy_fried_chicken_status_board.md:29`) still says v1.1 is current; fix that forward in lane 3 below.
3. **W1, alt footing:** after amendment A4 the strong-seed peak is converged through 128^3 (4.408 -> 4.587, last step 4.1 % against 5 %; ac0e22f6e1). S's "not converged" line is out of date for alt; canonical reruns are listed in `W1_pmedium_3d_scaleup/ENQUEUE_A4_commands.txt`.
4. **v3s L* window:** CQ7 (af9f68576f) found a window with v3s's own static solves, 21.68-27.00 pc canonical and 22.85-24.60 pc alt. Use it for any lane below that needs L*.

## Lanes, best first
Each line says where its full spec lives. Commit FROZEN_CRITERIA.md alone before any script or number, as always.

### Small, closes weak spots in the adopted action
1. **V3X W2 (K1 at the graded radius only).** New lane with frozen criteria; don't amend V3X. Spec: M A1.
2. **V3X W4c(b) (tensor ladder).** State a source for the 1e-10 line before rerunning; needs >= 24 cells per decade. Spec: M A1.
3. **Status board: fold LW1 (B1) and correct the PAPER67 footer.** Owner said "Yes, fold LW1". X-COP and DiskMass leave grey; keys 10 of 15. Ask the owner the MW/DiskMass vertical-force form (recommended default form A, form R stated on the tile) **before** committing those two colours. Spec: B, section B1.
4. **Regrade the six carried relativity tiles on v3s with the switch on (B2).** Binary pulsars, leaf, causality, strong coupling, G9, black holes. Don't cite X15/X16 for them. Spec: B, section B2.

### Theory, medium
5. **What v3s still asserts.** Nonlinear well-posedness, PN-order sign, the Sun moving in the khronon frame, a realistic solar interior, constraint causality. One lane each. Spec: M A2.
6. **a0 and kappa from the action** (merges M A3 and C lanes 1-2). In every class a0 is set by hand. After correction 1, the C'' question becomes: find a coupling that keeps the rest-frame tie stable with the khronon velocity included, or prove none exists. Read `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CLOSURE_2026-11-03.md` and its reopen conditions first.
7. **A covariant source for FN6's window** (merges M A4 and F 1). L ∝ M^(0.30-0.45) passes the five static gates; v3s's p = -0.5 stand-in fails the 24 dwarfs. Use v3s's own equations, not the Gaussian stand-in; check C6P's Q2 margin and GW speed. F says it needs the owner's go as a mechanism lane.
8. **C'' a0(z) pre-registration** (C lane 3). Only worth freezing if lane 6 finds a healthy tie; otherwise record that the prediction has no healthy carrier. Ask before any download.

### Data on disk
9. **FN6 canonical robustness** (F 2). The canonical window rests on one MW cell; refine around it with new criteria.
10. **FN4e HI-selected lens stack, stage 0** (F 3). Power forecast on ALFALFA, FASHI, KiDS-1000 shear (17.7 GB, read in chunks) and DESI BGS.
11. **a0(z) S/N forecast** (F 4). Synthetic K2''-style scan on `FN3_musedark_law_refit/fn3_cube.py`. Recompute MUTATE lines from the lane's own levers.
12. **IC 1613 cube redo** (F 5). Find the 0.716 HI-mass and 20.85 vs 16.9 km/s gaps before freezing a new lane. The law already fails the cube on record.
13. **BK2 G3 bookkeeping** (M A8). Measure cluster-to-cluster scatter first, freeze, then regrade in a new lane. Never widen BK2.
14. **FA1 leftovers** (M A6). Record-completion only: SLACS rotation classes, selector-level shear keys, Bullet 3D solve.

### astra's own runs
15. **W1** (S 4): finish canonical 128^3 (A4 reruns) and the binding verdict. Queue is held by L1 jobs; small jobs only.
16. **X1** (S table): finish the final analysis; every computed point already fails isocurvature by 2e8-6e8.

### Hard walls, test lanes only (adopt nothing)
17. **Clusters** (merges M A5, S 2, C 5). Requirement sheet in `FAILURES_EXECUTIVE_SUMMARY_2026-09-28.md` section F and FA1's README; M A5 lists the closed selectors. A new route needs a principle outside baryon geometry and kinematics.
18. **Held/free switch and cold abundance origin** (S 1, S 3). These are about the cold sector retired on 11-01; per the owner's rule a test lane may reopen it, but it adopts nothing.
19. **C'' disc-fold variant** (C 4). Only if the owner wants out-of-scope gates pursued; 40-80 CPU h, preemptible.

### Needs the owner before starting
- **a0(z) proposal sample** (M A7): proposal work, not computation.
- **MW thick share** (F 6): needs APOGEE's selection function, not approved.
- **FN4d Local Group star counts** (F 7): needs PHATTER and VizieR downloads.

## Dated events
| date (UTC) | what | how |
|---|---|---|
| 2026-11-06 03:15 | ALMA U4_28473 scoring | Scheduled task `alma-release-scoring-2026-11-06` runs `finish_2026_11_04/FN2_dated_tests/fn2_release_day.sh --run`; run by hand if it didn't fire. Details: F |
| 2026-11-28 18:25 | GS4_24110 [CI](2-1) | Owner triggers `fn2_gs4_release_day.sh --run`. Details: F |
| ~2026-12-02 | Gaia DR4 | Compare against CW1, CQ2 (seal SHA-256 1d65509dbf, 95303af61c), D2 and FN6 seals; never edit them or `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` |

## Decided, don't reopen without the owner
- v3s is the a0 law's action, scoped to isolated galaxies, the Solar System, galaxy lensing and GWs (7ac515f958). Clusters, growth/CMB, the radiation era, hosted dwarfs and the MW joint fit stay open; a0 by hand.
- The cold sector stays retired. No dark-matter particle; say "cold dark energy".
- "Not to redo" list: F.

## Rules that bind every lane
- Frozen criteria first, MUTATE twin that must bite, tolerances from stated errors, failures recorded as hard as passes.
- Two footings, canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. No ΛCDM inputs.
- Ask the owner before downloads, deposits or sending. Never run `PAPER67_zenodo_publish.py` without the go.
- Commit with explicit paths only (`git commit -m ... -- <paths>`); sessions share one git index. Report your own commit's hash.
- Never commit caches or home-path copies (DB1, MB1, BF1 `cache_keys/`, `x74_*`, `*.err`, `*.done`). Run the usual leak check on `git diff origin/main..HEAD` before pushing.
- Heavy compute must be preemptible and go through `compute_queue/heavyq.py`.
- Never rewrite history. Never write "theory closed".

kappa = 1/2 FITTED; not theory closed.
