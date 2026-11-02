#!/bin/bash
rm -f acc2_done
for c in cand_max_r200_share_fq cand_max_r200_share_f0 cand_max_r200_em1_fq; do OMP_NUM_THREADS=1 nice -n 19 python3 dw2_acc.py $c.py --no-bullet > acc_$c.log 2>&1; done
OMP_NUM_THREADS=1 nice -n 19 python3 dw2_second_b.py > /dev/null 2>&1
echo done > acc2_done
