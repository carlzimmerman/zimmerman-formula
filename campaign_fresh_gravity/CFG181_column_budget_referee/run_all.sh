#!/bin/sh
# CFG181 re-run: main, MUTATE 1-7, attacks (each < 1 minute).  Run from the directory holding the scripts.
cd "$(dirname "$0")" || exit 2
python3 CFG181_referee_main.py > /dev/null; echo "main exit=$?"
for k in 1 2 3 4 5 6 7; do MUTATE=$k python3 CFG181_referee_main.py > /dev/null; echo "MUTATE $k exit=$? (1 = control bites)"; done
python3 CFG181_attacks.py > /dev/null; echo "attacks exit=$?"
