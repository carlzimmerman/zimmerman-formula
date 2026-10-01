#!/usr/bin/env bash
# CFG265_run_all.sh: re-runs the whole referee pipeline (about 4 minutes; no network; reads the repo at 53f374ae2 via git show).
# Usage: ZF_REPO=<repo root> bash CFG265_run_all.sh   (or run from the lane directory inside the repo)
# Expected exit codes: extract 0 | route_recount 0 | lean_read 0 | physics 0 | physics --mutate 1 | audit_anchor 0 | refs 0
#                      | check 0 | plant (frozen set) 0 | plant --fresh 1 (X2 and X5 missed, kept) | self-disable 1
# The hand tables CFG265_classification.csv, CFG265_findings.json and CFG265_refs_webfetch.json are inputs, not outputs.
cd "$(dirname "$0")" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() { echo "== $*"; "$@" > "$OUTFILE" 2>&1; echo "   exit $?  -> $OUTFILE"; }
OUTFILE=CFG265_extract.out;            run python3 CFG265_extract.py
OUTFILE=CFG265_route_recount.out;      run python3 CFG265_route_recount.py
OUTFILE=CFG265_lean_read.out;          run python3 CFG265_lean_read.py
OUTFILE=CFG265_physics.out;            run python3 CFG265_physics.py
OUTFILE=CFG265_physics_MUTATE.out;     run python3 CFG265_physics.py --mutate
OUTFILE=CFG265_audit_anchor.out;       run python3 CFG265_audit_anchor.py
OUTFILE=CFG265_refs.out;               run python3 CFG265_refs.py
OUTFILE=CFG265_flags.out;              run python3 CFG265_check.py
OUTFILE=CFG265_plant.out;              run python3 CFG265_check.py --plant
OUTFILE=CFG265_plant_fresh.out;        run python3 CFG265_check.py --plant --fresh
OUTFILE=CFG265_plant_selfdisable.out;  run python3 CFG265_check.py --plant --disable NUM --only M1
