#!/bin/bash
cd "$(dirname "$0")"
P=$(ps -axo pid,command | awk '/python3 bf2_control\.py/ && !/awk/ {print $1}'); kill -STOP $P
nice -n 19 python3 bf2_scan.py > scan_rerun.log 2>&1; echo "scan rerun exit $?" >> chain4.status
nice -n 19 python3 bf2_accept.py candidates/P1.py > rq3_P1_rerun.log 2>&1; echo "P1 rerun exit $?" >> chain4.status
BF2_MUTATE=1 nice -n 19 python3 bf2_scan.py > scan_MUTATE.log 2>&1; echo "scan MUTATE exit $?" >> chain4.status
BF2_MUTATE=1 nice -n 19 python3 bf2_bullet.py > bullet_MUTATE.log 2>&1; echo "bullet MUTATE exit $?" >> chain4.status
nice -n 19 python3 bf2_bullet.py > bullet.log 2>&1; echo "bullet exit $?" >> chain4.status
kill -CONT $P
echo finished >> chain4.status
