#!/bin/bash
cd "$(dirname "$0")"
P=$(ps -axo pid,command | awk '/python3 bf2_control\.py/ && !/awk/ {print $1}'); kill -STOP $P
for t in P5 P6 P7 P8; do nice -n 19 python3 bf2_accept.py candidates/$t.py > rq3_$t.log 2>&1; echo "$t exit $?" >> chain3.status; done
nice -n 19 python3 bf2_supp.py > bf2_supp.out 2>&1; echo "supp exit $?" >> chain3.status
kill -CONT $P
echo finished >> chain3.status
