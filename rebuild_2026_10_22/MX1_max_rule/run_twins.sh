#!/bin/bash
# Rerun byte-identical, then the twins, which must exit 1. Bullet exits 1 on its published K7 too, so its twin is read by K5.
cd "$(dirname "$0")"; mkdir -p rerun_cmp
cp mx1_phys.out mx1_phys_results.json mx1_bullet.out mx1_bullet_results.json rerun_cmp/
nice -n 19 python3 mx1_phys.py > phys.log 2>&1; echo "phys rerun exit $?" > twins.txt
nice -n 19 python3 mx1_bullet.py > bullet.log 2>&1; echo "bullet rerun exit $?" >> twins.txt
for f in mx1_phys.out mx1_phys_results.json mx1_bullet.out mx1_bullet_results.json; do cmp $f rerun_cmp/$f && echo "$f identical" >> twins.txt || echo "$f DIFFERS" >> twins.txt; done
MX1_MUTATE=1 nice -n 19 python3 mx1_phys.py > phys_MUT.log 2>&1; echo "phys twin exit $?" >> twins.txt
MX1_MUTATE=1 nice -n 19 python3 mx1_bullet.py > bullet_MUT.log 2>&1; echo "bullet twin exit $?" >> twins.txt
nice -n 19 python3 mx1_acc.py cand_KM.py --no-keys --no-bullet > acc_KM.log 2>&1; echo "KM exit $?" >> twins.txt
rm -rf rerun_cmp; echo done >> twins.txt
