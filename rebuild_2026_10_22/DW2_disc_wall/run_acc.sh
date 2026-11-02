#!/bin/bash
# one at a time, nice 19
for c in cand_max_share_fq_floor cand_max_em1_fq cand_max_share_f0 cand_max_MUT_share_fq_x10; do OMP_NUM_THREADS=1 nice -n 19 python3 dw2_acc.py $c.py --no-keys --no-bullet > acc_$c.log 2>&1; done
OMP_NUM_THREADS=1 nice -n 19 python3 dw2_acc.py cand_max_share_fq.py --no-bullet > acc_keys_share_fq.log 2>&1
echo done > acc_done
