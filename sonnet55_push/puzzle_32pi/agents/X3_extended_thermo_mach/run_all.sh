#!/bin/bash
# reruns every script of lane X3 (sympy 1.13.1, mpmath 1.3.0, numpy 1.26.4); each exits non-zero on any failed check or un-rejected control
cd "$(dirname "$0")"
rc=0
for f in x01_sds_extended_thermo x02_a0_points_table x03_machian_coefficients x04_machian_modified_inertia; do
  python3 $f.py > $f.out 2>&1 || rc=1
  echo "$f: exit-code-ok=$([ $rc -eq 0 ] && echo yes || echo NO)  $(tail -1 $f.out)"
done
exit $rc
