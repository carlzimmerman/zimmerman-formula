#!/bin/bash
# CSD1 runner. Stage 1: Part 1, S-seed (9 masses x 2 footings), P1c's 10.825 rows, A4-grid rows (KA4), TW3, TW5, KA7,
# S-cos tuning (law off, N 1200, A 4 / 7 / 10), then csd1_tune.py. Stage 2 (argument "stage2"): S-cos with A* from
# csd1_tune.json, then csd1_ref.py (and its MUTATE twin), then the grader. Six shell runs at a time, nice 19, isolated.
# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
cd "$(dirname "$0")" || exit 1
mkdir -p runs logs
PY="nice -n 19 python3 -I -B"
if [ "$1" != "stage2" ]; then
  $PY csd1_part1.py > logs/part1.log 2>&1
  $PY csd1_part1.py mutate > logs/part1_mutate.log 2>&1
  {
    for ft in canonical alt; do
      for M in 8 9 9.4 10 10.45 10.7 10.9 11.2 11.5 10.825; do echo "$ft $M"; done
      for M in 9.4 10.45 10.7 10.9; do echo "$ft $M --grid a4"; done
    done
    echo "canonical 10.45 --grid a4 --mutate lagr"
    echo "canonical 10.45 --law off"
    echo "canonical 10.45 --A 0 --tag csd1_ka7_A0_canonical_M10.45"
    for A in 4 7 10; do echo "canonical 10.45 --N 1200 --A $A --law off"; done
  } | xargs -P 6 -L 1 sh -c "$PY csd1_shells.py \$0 \$@ >> logs/shells.log 2>&1"
  $PY csd1_tune.py > logs/tune.log 2>&1
else
  AS=$(python3 -I -B -c "import json; a=json.load(open('csd1_tune.json'))['A_star']; print('' if a is None else a)")
  if [ -n "$AS" ]; then
    {
      echo "canonical 10.45 --A $AS --law off"
      for M in 9 11.5; do echo "canonical $M --A $AS --law off"; done
      for ft in canonical alt; do for M in 9 10.45 11.5; do echo "$ft $M --A $AS"; done; done
    } | xargs -P 6 -L 1 sh -c "$PY csd1_shells.py \$0 \$@ >> logs/shells_stage2.log 2>&1"
  fi
  $PY csd1_ref.py > logs/ref.log 2>&1
  $PY csd1_ref.py mutate > logs/ref_mutate.log 2>&1
  $PY csd1_grade.py > logs/grade.log 2>&1
fi
