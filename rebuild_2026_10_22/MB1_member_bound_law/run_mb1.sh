#!/bin/bash
# MB1 full run. Fast rows first, then the unedited harness with keys. nice 19, one thread per process.
cd "$(dirname "$0")"
nice -n 19 python3 mb1_fast.py kfit > kfit.log 2>&1 || { echo kfit failed; exit 1; }
nice -n 19 python3 mb1_fast.py grade > grade.log 2>&1
for v in "MB1_ALPHA=-1.0 MB1_TAG=_a10" "MB1_ALPHA=-1.4 MB1_TAG=_a14" "MB1_ICL=0.3 MB1_TAG=_icl" "MB1_BASE=law MB1_TAG=_base" "MB1_GROUPF=0.3 MB1_TAG=_f03" "MB1_GROUPF=0.85 MB1_TAG=_f085"; do env $v nice -n 19 python3 mb1_fast.py grade F --no-bullet > "sens_${v##*=}.log" 2>&1; done
nice -n 19 python3 mb1_fast.py grade F --mutate > mutate.log 2>&1; echo "mutate exit $?" >> mutate.log
for a in F K KG; do nice -n 19 python3 mb1_acc.py candidates/mb1_$a.py --no-bullet > acc_$a.log 2>&1; done
touch mb1_run.done
