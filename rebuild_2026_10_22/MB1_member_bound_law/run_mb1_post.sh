#!/bin/bash
# MB1 checks run after the first read: MUTATE on the arms whose Bullet passes, K7 rerun, K6 units probe, N's keys (reported, moves no label). nice 19.
cd "$(dirname "$0")"
for a in N K; do MB1_TAG=_$a nice -n 19 python3 mb1_fast.py grade $a --mutate > mutate_$a.log 2>&1; echo "mutate exit $?" >> mutate_$a.log; done
MB1_TAG=_k7 nice -n 19 python3 mb1_fast.py grade > k7.log 2>&1; cmp mb1_grade.json mb1_grade_k7.json > k7_cmp.log 2>&1; echo "cmp exit $?" >> k7_cmp.log
rm -f k6_probe.jsonl; nice -n 19 python3 mb1_acc.py k6_probe.py --no-bullet > acc_K6.log 2>&1
nice -n 19 python3 mb1_acc.py candidates/mb1_N.py --no-bullet > acc_N.log 2>&1
touch mb1_post.done
