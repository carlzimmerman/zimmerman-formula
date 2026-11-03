#!/bin/bash
# DB1 harness runs with keys, two at a time, nice 19, one thread each. Then MG1 rows, MUTATE twins, control, rerun.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
acc() { nice -n 19 python3 db1_acc.py candidates/db1_$1.py --no-bullet > results/db1_$1.out 2> results/db1_$1.err; echo "$1 exit $?" >> results/acc.status; }
acc P1G & acc P3 & wait
acc P1 & acc Z & wait
acc P2
nice -n 19 python3 db1_fast.py mg1 > mg1.log 2>&1; echo "mg1 exit $?" >> results/acc.status
nice -n 19 python3 db1_fast.py mg1 --mutate > mg1_mutate.log 2>&1; echo "mg1 mutate exit $?" >> results/acc.status
nice -n 19 python3 db1_fast.py grade --mutate > grade_mutate.log 2>&1; echo "grade mutate exit $?" >> results/acc.status
nice -n 19 python3 db1_fast.py control > control.log 2>&1; echo "control exit $?" >> results/acc.status
DB1_TAG=_rerun nice -n 19 python3 db1_fast.py grade > grade_rerun.log 2>&1; cmp db1_grade.json db1_grade_rerun.json && echo "K5 rerun byte-identical" >> results/acc.status || echo "K5 rerun DIFFERS" >> results/acc.status
touch db1_run.done
