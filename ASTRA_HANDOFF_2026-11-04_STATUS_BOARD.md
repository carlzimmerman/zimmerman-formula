# Handoff to astra, 2026-11-04: the status board and the lanes it leaves

Written at the owner's request ("push up this work and lanes for astra to pick up and continue"). This is a brief, not a result; each claim points to a committed file. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired.

It adds to, and doesn't repeat, `ASTRA_HANDOFF_2026-11-04_FROM_CLAUDE.md` (V3X's W2 and W4c(b), a0 from the action) and `ASTRA_HANDOFF_2026-11-04_FINISH_PUSH.md` (the house rules, which bind here too). Commit with explicit paths only: several sessions share one git index.

## What's on main

| commit | what |
|---|---|
| 8b9f792690 | **Status board, 4 November.** v3s shown as the a0 law's action, scoped (owner, 7ac515f958). Column 0 is graded on v3s, and the action's tile carries the three weak spots. The generator refuses to build if one drops off: V3X W2 and W4c(b) UNDECIDED, constraints instantaneous. New guards: v3s grades only inside the scope; carried tiles keep their 24 October colour and lanes. Selftest 29/29, `--mutate` fails as required. Fix-forward: the generator pointed at PAPER67's renamed draft file and crashed. |
| f1529da2ac | **HX1_hot_ladder:** a sigma-keyed boost of the law's phantom. NO LADDER on both footings. X-COP's need falls as x^-0.33; MaNGA ellipticals need B 3-4, but inside Re, where the IMF is degenerate with the need. |
| 8f23cc6c57 | **MB1_member_bound_law:** member law halos as the cluster variable. No hit; fails keys 5-8 of 15. |

Files: `explainers/make_status_board.py`, `explainers/crispy_fried_chicken_status_board.md`, `explainers/img/status_board.png`. The 1 November board is kept as `explainers/img/status_board_2026-11-01law.png`.

Rebuild and check, one core, seconds:
```
OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --selftest
OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --mutate    # must exit 1
OMP_NUM_THREADS=1 python3 explainers/make_status_board.py
OMP_NUM_THREADS=1 python3 explainers/make_status_board.py --md        # table for the md page
```

## B1. Fold LW1 onto the board (owner said "Yes, fold LW1"; not started)

`rebuild_2026_10_22/LW1_law_scorecard/README.md` (afcf01fc96) computed the law's K, X, Dw, DM and MW lines on the measured chain. Its section "Corrections to FG1's C4 column" states where FG1's cells were wrong. The board still takes those tiles' colours from FG1's C4 table (`read_fg1_c4`, `FG1_COLOUR`, the `fg1=` field), so X-COP and DiskMass are grey there.

What the fold should change, with LW1's numbers:

| tile | now | from LW1 |
|---|---|---|
| X-COP | grey (FG1 NOT GRADED; FG1's -0.151 is CS2's Burkert row) | **FAIL** both: +0.467, 0.476 / +0.434, 0.444; M_HSE/M_law 2.93 / 2.72 |
| Cluster keys (15, old template) | FAIL, FG1's old-template count | FAIL both: **10 of 15** at both f*, worst G-MID-T3 +4.86, joint p 3e-8 (alt 1e-6). Rename the tile; it's no longer the old template |
| Local Group dwarfs (five classes) | FAIL, no external field | FAIL, worse with E1's field: MW ultra-faint +1.30 (Z +6.76), alt +1.26 (+6.59) |
| DiskMass | grey | form R **FAIL** r 1.239 / 1.204; form A r 1.477, NO LABEL; OD1's tracer caveat stands |
| MW vertical force | FAIL (X5's gate) | form A **FAIL INFEASIBLE** both; form R PASS on 1 / 6 in-prior cells, all missing the K_z scale length by +3.9 to +4.4σ |
| IC 1613, SPARC, tilt, LITTLE THINGS, groups, lensing | FG1 | unchanged (LW1 reads them from FG1) |

**One decision for the owner before colouring MW and DiskMass.** LW1 doesn't pick a vertical-force form. The law gives only the in-plane force: form A is the field equation, form R the round rule. v3s, now the adopted action, supplies a field equation, so form A is the action's own reading. That reading gives MW FAIL and DiskMass NO LABEL (grey). LW1 says the count is the same at L* 0 and 24 pc. But the owner left the MW joint fit outside v3s's scope. Recommended default: colour by form A and state form R on each tile. Ask before committing that.

How to build it, to match the generator's style:
- Add an `LW1` entry to `SOURCES` (README plus `lw1_results.json`).
- Add `read_lw1()`, which parses the README's "## Scorecard" table into {line: (canonical, alt)} the way `read_fg1_c4` does.
- Add a tile field `lw1=` that takes precedence over `fg1=` for K, X, Dw, DM and MW, with the same per-footing colour check. `FG1_LINES` must still all be on the board.
- New selftest cases, each of which must be caught: X-COP back to grey; an LW1 FAIL coloured PASS; the tile's form not matching the stated form choice.
- Keep `MUST_STAY_RED`, and don't loosen the column-0 guards.
- Regenerate the md table with `--md`. Replace the md's "LW1 has landed, not folded" paragraph, and keep a copy of the pre-fold image (`status_board_2026-11-04v3s.png`).

## B2. Regrade the carried relativity tiles on v3s proper

Six column-0 tiles carry their 24 October v3s colours, marked `carried=True`: binary pulsars, leaf problem, causality, strong coupling, matter conservation (G9) and black holes. Their lanes C8 (`covariant_push_2026_10_22/C8_instantaneous`) and P3 (`rebuild_2026_10_22/P3_v3_strong_field`) ran on **v3, before X3's switched stiffness** gamma_L Theta(D·P). The 24 October verdict lists them as v3s's, but none was recomputed with the switch.

The lane:
1. Commit frozen criteria first, both footings.
2. Recompute the binary-pulsar bound (C8's 3.2e-14 of the double pulsar's error), the strong-coupling loop factor (P3's 1.3e-3 at Eot-Wash, L* 90 pc), and the static black-hole shifts (P3's <= 2.9e-11), all with the switch on.
3. Write a MUTATE twin with the switch inverted.

A tile moves from `carried` to a `VERIFIED_GREEN` entry, or to a new colour, only on that lane's result. One rule: X15/X16 PPN and pulsar results belong to the beta K^2 completion (C1), not to v3s as adopted. Don't cite them for these tiles.

## Not lanes, for the owner
- PAPER67 v1.1 (DOI 10.5281/zenodo.23966443) still says no action is selected. A v1.2 is being drafted elsewhere and needs the owner's go. The board's footer says this.
- The MW form choice above.
