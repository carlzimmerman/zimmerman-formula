#!/bin/bash
# AN2 diagnostic SG: waits for a quiet Mac, then all runs, two at a time, nice 15, one thread
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONUNBUFFERED=1
cd "$(dirname "$0")"
quiet() {
  load=$(sysctl -n vm.loadavg | awk '{print $2}')
  pg=$(vm_stat | awk '/Pages free/{f=$3}/Pages inactive/{i=$3}END{print (f+i)*16384/1e9}')
  awk -v l="$load" -v m="$pg" 'BEGIN{exit !(l < 16 && m > 8)}'
}
until quiet; do sleep 300; done
echo "start $(date -u +%FT%TZ)"
printf '%s\n' "A 1e15 64" "B 1e15 64" "A 1e12 64" "B 1e12 64" "A 1e15 128" "B 1e15 128" "A 1e12 128" "B 1e12 128" |
  xargs -P 2 -L 1 sh -c 'nice -n 15 python3 shape_grid.py $0 $1 $2'
echo "end $(date -u +%FT%TZ)"
