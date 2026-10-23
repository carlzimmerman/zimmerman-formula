#!/bin/bash
# V3 occupation sweep (FROZEN_CRITERIA V3 + AMENDMENT A1). One process per point, nice, single thread.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for sc in B A; do for nu in 8 2; do for n in 1 2 4 8 16 32; do
  for mode in rwa full; do
    f=validation/v3_${sc}_nu${nu}_n${n}_${mode}.json
    [ -f "$f" ] && continue
    /usr/bin/time -l nice -n 15 python3 x1_validation.py v3 $sc $nu $n $mode 2>&1 | grep -E "^(A|B) |skip|maximum resident" 
  done
done; done; done
for sc in A B; do
  nice -n 15 python3 x1_validation.py v3 $sc 8 4 full --free 2>&1 | grep -E "^(A|B) "
  nice -n 15 python3 x1_validation.py v3 $sc 8 4 full --free --mutate 2>&1 | grep -E "^(A|B) "
done
echo SWEEP DONE
