#!/usr/bin/env bash
# CFG241_run_all.sh: re-runs the whole referee pipeline. Usage: ZF_REPO=<repo root> bash CFG241_run_all.sh   (or run from the installed lane directory)
# Expected exit codes: extract 0 | plant (frozen set, rule v4) 0 | plant --fresh 1 (X5 key-only citation missed, kept) | plant --fresh2 1 (Y3 single-digit swap missed, kept)
#                      | self-disable 1 | check 0 | physics 0 | physics --mutate 1 | refs 0 | report 0
cd "$(dirname "$0")" || exit 2
run() { echo "== $*"; "$@" > "$OUTFILE" 2>&1; echo "   exit $?"; }
OUTFILE=CFG241_extract.out;               run python3 CFG241_extract.py
OUTFILE=CFG241_plant_v4.out;              run python3 CFG241_check.py --plant
OUTFILE=CFG241_plant_fresh_v4.out;        run python3 CFG241_check.py --plant --fresh
OUTFILE=CFG241_plant_fresh2_v4.out;       run python3 CFG241_check.py --plant --fresh2
OUTFILE=CFG241_plant_selfdisable_v4.out;  run python3 CFG241_check.py --plant --disable NUM --only M1
OUTFILE=CFG241_flags.out;                 run python3 CFG241_check.py
OUTFILE=CFG241_physics_stdout.out;        run python3 CFG241_physics.py
OUTFILE=CFG241_physics_mutate_stdout.out; run python3 CFG241_physics.py --mutate
OUTFILE=CFG241_refs_stdout.out;           run python3 CFG241_refs.py
OUTFILE=CFG241_report.out;                run python3 CFG241_report.py
