# PASS — LW1 board integration, both forms retained

Tier 1 lane 3; criteria `ad0bdfef56`. Integration result only, not a new
physical fit. Kappa = 1/2 FITTED; not theory closed. Neither vertical-force
prescription is selected. The scoped adoption is unchanged.

LW1 now overrides FG1 for K, X, Dw, MW and DM, while all eleven FG1 identifiers
remain. The measured-chain key counts were independently recomputed from
the per-key Z arrays: ten of fifteen in all eight cells. X-COP is FAIL on
both footings; E1's dwarf deficit is larger than the plain-law row. Other
FG1 results and all column-0 carried/scope guards are unchanged in this lane.

| tile | canonical A | canonical R | alt A | alt R |
|---|---|---|---|---|
| MW vertical force | FAIL | PASS, 1 in-prior cell | FAIL | PASS, 6 in-prior cells |
| DiskMass | NO LABEL, r1.477 | FAIL, r1.239 | NO LABEL, r1.477 | FAIL, r1.204 |

A is the field equation and R is the round rule. Their different predictions
are shown as separate coloured badges and separate entries in the markdown.
MW's red backing retains MUST_STAY_RED, with its R pass visibly green.
DiskMass shows grey A and red R; its red backing records a failing form.
Backing-colour totals are not a choice of model. The post-result MW scale
length discrepancy and DiskMass's OD1 tracer caveat remain visible.

The PAPER67 footer now records deposited v1.2, DOI10.5281/zenodo.23968171,
using the current goal brief's correction. No deposited document was changed.
The pre-fold image was copied byte-for-byte to
`explainers/img/status_board_2026-11-04v3s.png`; `preimage.json` records its hash.
The regenerated image was inspected: both A/R badges, notes and footer fit.

## Verification

- Before implementation, the integration harness failed 18 of 32 checks,
  exposing the missing forms, stale X-COP result and absent LW1 guards.
- Final main harness: 32/32 checks, exit0, no board errors.
- Harness MUTATE removes MW form R: 30/32, exit1, explicitly rejected by
  the both-forms guard. Separate mutant output is retained.
- Generator `--selftest`: all 34 broken cases caught, clean board zero errors.
- Generator `--mutate`: exit1 as required, strips evidence and writes nothing.
- Generator render: exit0, all checks pass; markdown table regenerated.

The canonical backing tally is 12 pass, 8 conditional, 5 open, 11 fail,
1 undecided, 11 grey; alt is 11 pass and 12 fail, other counts equal.
Input hashes, per-check results and the pre-change failure are committed.
There are no fitted numbers added by the presentation. No PDE is run, so a
new numerical convergence study is inapplicable here.

From the repository root:

```sh
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B astra_goal_2026_11_05/AZ33_board_lw1/run.py
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B astra_goal_2026_11_05/AZ33_board_lw1/run.py --mutate
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B explainers/make_status_board.py --selftest
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B explainers/make_status_board.py --mutate
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B explainers/make_status_board.py
OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/az33_mpl python3 -B explainers/make_status_board.py --md
```

Next: lane 4 regrades the six carried relativity tiles with the switched
action and both L_star intervals. This commit deliberately carries their
old labels pending those calculations; it does not certify their prose.
