#!/bin/bash
# one process at a time: the control waits while RQ3 runs
cd "$(dirname "$0")"
for p in $(pgrep -f bf2_control.py); do kill -STOP $p; done
for c in ../RQ3_acceptance_v2/candidates/law.py candidates/Hone.py candidates/P1.py candidates/P2.py candidates/P3.py candidates/P4.py; do
  n=$(basename $c .py); /usr/bin/time -l nice -n 19 python3 bf2_accept.py $c > rq3_$n.log 2>&1; echo "$n exit $?" >> chain_rq3.status
done
for p in $(pgrep -f bf2_control.py); do kill -CONT $p; done
echo finished >> chain_rq3.status
