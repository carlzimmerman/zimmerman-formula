#!/bin/bash
# WLJ2 runner: the long stages one at a time, one thread, nice 19, with the house disk / swap guards before each stage.
# usage: bash run_chain.sh <KiDS-Legacy release folder> <stage> [<stage> ...]
#   stages: shear lwb1r lwb1 kl:<footing>:<group>
# Each stage writes logs/run_<stage>.log and a marker logs/done_<stage> (with its exit code). Adopts nothing.
cd "$(dirname "$0")" || exit 1
REL="$1"; shift
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p logs
guard() {
  while true; do
    free=$(df -g . | awk 'NR==2{print $4}')
    swap=$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')
    if [ "$free" -lt 8 ]; then echo "STOP: free disk ${free} GB < 8" >> logs/guard.log; exit 3; fi
    if [ "$free" -ge 10 ] && [ "$(echo "$swap <= 12288" | bc)" = 1 ]; then echo "$(date '+%H:%M:%S') start ok: free ${free} GB, swap ${swap} MB" >> logs/guard.log; return; fi
    echo "$(date '+%H:%M:%S') waiting: free ${free} GB, swap ${swap} MB" >> logs/guard.log; sleep 120
  done
}
for st in "$@"; do
  guard
  tag=$(echo "$st" | tr ':' '_')
  case "$st" in
    shear) nice -n 19 python3 -I -B wlj2_shear.py > "logs/run_$tag.log" 2>&1 ;;
    lwb1|lwb1r) nice -n 19 python3 -I -B wlj2_lwb.py "$st" > "logs/run_$tag.log" 2>&1 ;;
    kl:*) IFS=: read -r _ ft grp <<< "$st"; nice -n 19 python3 -I -B wlj2_kl1bx1.py "$ft" "$grp" "$REL" > "logs/run_$tag.log" 2>&1 ;;
    *) echo "unknown stage $st" >> logs/guard.log; continue ;;
  esac
  echo $? > "logs/done_$tag"
done
echo finished > logs/chain_finished
