#!/bin/bash
# one process at a time: the control stays paused while this runs
cd "$(dirname "$0")"
kill -STOP 62082 2>/dev/null
for c in ../RQ3_acceptance_v2/candidates/law.py candidates/Hone.py candidates/P1.py candidates/P2.py candidates/P3.py candidates/P4.py; do
  n=$(basename $c .py); nice -n 19 python3 bf2_accept.py $c > rq3_$n.log 2>&1; echo "$n exit $?" >> chain2.status
done
nice -n 19 python3 bf2_k1.py > bf2_k1.out 2>&1; echo "k1 exit $?" >> chain2.status
nice -n 19 python3 bf2_sparc.py > sparc.log 2>&1; echo "sparc exit $?" >> chain2.status
nice -n 19 python3 bf2_bullet.py > bullet.log 2>&1; echo "bullet exit $?" >> chain2.status
kill -CONT 62082 2>/dev/null
echo finished >> chain2.status
