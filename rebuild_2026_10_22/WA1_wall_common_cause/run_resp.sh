#!/bin/bash
# After keys. One job at a time, one thread, nice 19.
cd "$(dirname "$0")"
while pgrep -f wa1_keys.py >/dev/null; do sleep 30; done
for c in LAW UX3 P3 P7 MX1 BK2 CAL; do for f in canonical alt; do
  [ -f resp/${c}_$f.json ] || nice -n 19 python3 wa1_resp.py $c $f >> resp.log 2>&1
done; done
echo resp_finished >> resp.log
