#!/bin/bash
# F1A fits, sequential, one thread
cd "$(dirname "$0")"
for spec in "B2 canonical cold" "B2 alt cold" "B2 canonical MB" "B2 alt MB" "B1 canonical cold" "B1 canonical MB"; do
  nice -n 10 python3 f1a.py fit $spec 2>&1 | grep -v -i warning | grep -v "r = self"
done
nice -n 10 python3 f1a.py g4 2>&1 | grep -v -i warning
nice -n 10 python3 f1a.py mutate2 2>&1 | grep -v -i warning
