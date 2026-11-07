#!/bin/bash
# GL3 sandbox builder (criteria FROZEN_CRITERIA.md). Usage: gl3_sandbox.sh <repo checkout> <empty scratch dir>
# Builds <scratch>/gl3sb (pristine), gl3_old, gl3_new, gl3_k2: closure_2026_11_06/07 from origin/main via git archive,
# every other top-level entry of the checkout symlinked; <scratch>/_external_data links the repo's parent data dir
# (cfg917_lib reads <repo>/../_external_data). Each kernel copy gets the iter2.py switch below (GL3_KERNEL env var).
set -e; R=$1; B=$2; mkdir -p $B/gl3sb
(cd $R && git archive origin/main closure_2026_11_06 closure_2026_11_07) | tar -x -C $B/gl3sb
for e in $(ls -A $R); do case $e in closure_2026_11_06|closure_2026_11_07|.git) ;; *) ln -s $R/$e $B/gl3sb/$e;; esac; done
ln -sfn $(dirname $R)/_external_data $B/_external_data
for k in old new k2; do cp -a $B/gl3sb $B/gl3_$k; (cd $B/gl3_$k && patch -p1 < $(dirname $0)/gl3_iter2_kernel_switch.patch); done
# run: cd $B/gl3_<k>/<lane dir> && GL3_KERNEL=<k> OMP_NUM_THREADS=1 nice -n 15 python3 <script> [args]
