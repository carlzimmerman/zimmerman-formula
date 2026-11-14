#!/bin/bash
# AGB7R runner. usage: bash run_agb7r.sh cfg684 | cfg689 <batch> | one <target> <sample> <A> <tpl>
# CFG684 runs one after another; CFG689 runs in batches of at most three at once (CFG689_PARALLEL=1), waited on by pid.
# Each run's exit code goes to runs_status.txt (75 = NOT RUN: the lane's own guard; never bypassed).
# Raw output is filtered into <base>.stdout.txt (*.log is git-ignored here): lines carrying absolute paths (interpreter warnings) and the source line echoed after each are dropped.
cd "$(dirname "$0")" || exit 1
export VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 NUMEXPR_NUM_THREADS=2
unset CFG689_NSTEP MUTATE

amps() { printf '%s' "$1" | sed 's/\./p/'; }
filt() { awk 'skip && /^[ \t]/ {skip=0; next} {skip=0} /\/(Users|opt|private|home|var|Library|Applications)\// {skip=1; next} {print}' "$1"; }

one() {   # target sample A tpl
  local base="agb7r_$1_$2_$4_A$(amps "$3")"
  local raw="$base.raw.tmp"
  local t0; t0=$(date +%s)
  if [ "${1#cfg689}" != "$1" ]; then CFG689_PARALLEL=1 python3 -I -B agb7r_harness.py "$1" "$2" "$3" "$4" > "$raw" 2>&1
  else python3 -I -B agb7r_harness.py "$1" "$2" "$3" "$4" > "$raw" 2>&1; fi
  local rc=$?
  filt "$raw" > "$base.stdout.txt"; rm -f "$raw"
  echo "$base exit $rc seconds $(( $(date +%s) - t0 )) ended $(date +%Y-%m-%dT%H:%M:%S)" >> runs_status.txt
  return $rc
}

case "$1" in
  cfg684)
    for spec in "full 0 S" "full 1 S" "full 0.23 S" "des_only 0.23 S" "full 0.35 S" "des_only 0.35 S" \
                "full 0.35 H" "des_only 0.35 H" "des_only 1 S"; do
      set -- $spec; one cfg684 "$1" "$2" "$3"
    done ;;
  cfg689)
    case "$2" in
      1) specs=("cfg689_TD5F des_only 1 S" "cfg689_D5 full 0.23 S" "cfg689_TD5F full 0.23 S") ;;
      2) specs=("cfg689_D5 des_only 0.23 S" "cfg689_TD5F des_only 0.23 S" "cfg689_D5 full 0.35 S") ;;
      3) specs=("cfg689_D5 des_only 0.35 S" "cfg689_TD5F full 0.35 S" "cfg689_TD5F des_only 0.35 S") ;;
      4) specs=("cfg689_D5 full 1 S" "cfg689_D5 des_only 1 S" "cfg689_TD5F full 1 S") ;;
      *) echo "batch 1-4"; exit 2 ;;
    esac
    pids=()
    for spec in "${specs[@]}"; do set -- $spec; one "$1" "$2" "$3" "$4" & pids+=($!); done
    wait "${pids[@]}" ;;
  one) shift; one "$@" ;;
  *) echo "usage: $0 cfg684 | cfg689 <1-4> | one <target> <sample> <A> <tpl>"; exit 2 ;;
esac
