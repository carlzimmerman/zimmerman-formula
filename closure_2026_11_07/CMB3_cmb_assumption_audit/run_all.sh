#!/bin/bash
# CMB3: every step sequential, one process at a time (< 1 GB); a step whose part exists is skipped (restartable)
cd "$(dirname "$0")"
run() { out="parts/$1"; shift; if [ -f "$out" ]; then echo "skip $out"; else nice -n 10 python3 cmb3.py "$@" 2>&1 | grep -v -i "warning\|r = self\|self.Ci is not None\|out.append(W.T"; fi; }
run ka.json ka
run a1.json a1
run mutate.json mutate
run a6point.json a6point
for f in canonical alt; do run fit_KA2_${f}_cold.json ka2 $f; done
for X in A2U A2T A6F A4P A3N; do for f in canonical alt; do for m in cold MB; do
  if [ "$X" = "A6F" ] && [ "$m" = "cold" ]; then continue; fi
  run fit_${X}_${f}_${m}.json fit $X $f $m
done; done; done
for f in canonical alt; do run a4hess_${f}.json a4hess $f; done
echo ALL DONE
