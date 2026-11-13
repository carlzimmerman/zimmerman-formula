#!/bin/bash
# JNT2: RC / SPARC twins, clusters (all modes), lensing (all modes); one process at a time. Paths relative to this folder.
cd "$(dirname "$0")"
for m in S 0 H D; do python3 jnt2_rc.py --mode $m > run_rc_$m.log 2>&1; echo "exit $?" >> run_rc_$m.log; done
for m in main S 0 H D; do python3 jnt2_clusters.py --mode $m > run_clusters_$m.log 2>&1; echo "exit $?" >> run_clusters_$m.log; done
for m in main S 0 H D; do python3 jnt2_lens.py --mode $m > run_lens_$m.log 2>&1; echo "exit $?" >> run_lens_$m.log; done
touch done_rest
