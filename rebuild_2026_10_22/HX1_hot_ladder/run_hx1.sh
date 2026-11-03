#!/bin/bash
# HX1 stage 1: checks, graded run, K4 rerun (byte-identical), MUTATE. kappa = 1/2 FITTED; not theory closed.
set -u; cd "$(dirname "$0")"
nice -n 19 python3 hx1_ladder.py --checks > /dev/null 2>&1 || exit 1
nice -n 19 python3 hx1_ladder.py > /dev/null 2>&1 || exit 1
cp hx1_ladder.out k4_first.out; cp hx1_ladder.json k4_first.json
nice -n 19 python3 hx1_ladder.py > /dev/null 2>&1
cmp hx1_ladder.out k4_first.out && cmp hx1_ladder.json k4_first.json; echo "K4 cmp exit $?" > hx1_post_checks.out
rm -f k4_first.out k4_first.json
HX1_MUTATE=1 nice -n 19 python3 hx1_ladder.py > /dev/null 2>&1; echo "MUTATE exit $?" >> hx1_post_checks.out
tail -1 hx1_ladder_MUTATE.out >> hx1_post_checks.out
