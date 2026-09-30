#!/bin/bash
# Re-run every CFG238 script. Set ZF_REPO if this directory is not inside the repo. Main and attack scripts exit 0; MUTATE runs exit 1 when the control bites (M8 is expected NOT to bite: exit 0, kept).
cd "$(dirname "$0")" || exit 2
for s in main a_design b_circular c_ace d_anchor e_hat f_prov; do
  python3 CFG238_$s.py > /dev/null 2> CFG238_$s.err; echo "CFG238_$s exit $?"
done
for k in 1 2 3 4 5 6 7 8; do
  MUTATE=$k python3 CFG238_MUTATE.py > /dev/null 2> CFG238_MUTATE_M$k.err; echo "MUTATE=$k exit $?"
done
python3 CFG238_compare.py > /dev/null 2> CFG238_compare.err; echo "CFG238_compare (post-run only) exit $?"
rm -f CFG238_*.err
