#!/bin/bash
# Byte-identical rerun of the deterministic outputs; one full cell rerun into a fresh cache.
cd "$(dirname "$0")"
( nice -n 19 python3 -I df3g_controls.py > /dev/null 2>&1; DF3G_MUTATE=1 nice -n 19 python3 -I df3g_controls.py > /dev/null 2>&1; nice -n 19 python3 -I df3g_keycheck.py > /dev/null 2>&1; nice -n 19 python3 -I df3g_bullet.py > /dev/null 2>&1; DF3G_MUTATE=1 nice -n 19 python3 -I df3g_bullet.py > /dev/null 2>&1; nice -n 19 python3 -I df3g_run.py mutate > /dev/null 2>&1; nice -n 19 python3 -I df3g_run.py selfcheck > /dev/null 2>&1 ) &
( DF3G_SUFFIX=_RERUN DF3G_CACHE=cache_rerun nice -n 19 python3 -I df3g_run.py cell 1 100 N > /dev/null 2>&1 ) &
wait
nice -n 19 python3 -I df3g_read.py > /dev/null 2>&1
shasum -a 256 df3g_controls.json df3g_controls_MUTATE.json df3g_bullet.json df3g_bullet_MUTATE.json df3g_keycheck.json df3g_run_MUTATE.json df3g_selfcheck.json df3g.out df3g_summary.json > sha_rerun.txt
python3 -I - <<'P' > rerun_compare.txt
import json
a = json.load(open("df3g_cell_G1.000_s100_N.json")); b = json.load(open("df3g_cell_G1.000_s100_N_RERUN.json")); a.pop("K_first_pass_lost_core", None)
print("cell (1, 100) N rerun in a fresh cache, all fields equal:", a == b)
P
diff sha_first.txt sha_rerun.txt > /dev/null && echo "all listed outputs byte-identical" >> rerun_compare.txt || echo "DIFFER" >> rerun_compare.txt
echo done > rerun.done.tmp
