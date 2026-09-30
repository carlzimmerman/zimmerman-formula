#!/bin/bash
# reruns every script of lane Z6 (sympy 1.13.1, mpmath 1.3.0, numpy 1.26.4); each exits non-zero on any failed check, un-rejected control or un-caught mutant
cd "$(dirname "$0")"
rc=0
for f in z01_record_kernel_definition z02_moments_and_cutoff_map z03_sciama_vs_record_structure z04_regime_and_ephemeris z05_mutation_harness; do
  python3 $f.py > $f.out 2>&1 || rc=1
  echo "$f: $(tail -1 $f.out)"
done
echo "exit code $rc"
exit $rc
