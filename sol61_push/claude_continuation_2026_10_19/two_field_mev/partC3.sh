#!/bin/bash
# PLAN C3: NR-GPP stability along the fixed-f_c path; two resolutions per Gamma; 20 min cap per process.
cd "$(dirname "$0")"
CAP="perl -e alarm(shift);exec(@ARGV) 1200"
FC=0.009888264649460883
mkdir -p results/partC3
prevbg=""; prevG=""
# Gamma  Rbox   Ncoarse Nfine  (Rbox = (z_s + 0.33 (Gamma/1e-8)^(1/3))/sqrt(Gamma), z_s(TF) = 0.4696)
while read G R NC NF; do
  [ -z "$G" ] && continue
  seed=$(ls results/gr/continue_*_G$(python3 -c "print(f'{float(\"$G\"):.3e}')").npz 2>/dev/null | head -1)
  if [ -n "$seed" ]; then sarg="--seed $seed"; else sarg="--seed $prevbg --seed-gamma $prevG"; fi
  for N in $NC $NF; do
    if [ $N -gt 2000 ]; then
      $CAP ./run.sh nr_gpp.py --gamma $G --value $FC $sarg --N $N --rbox $R --ls 0,1,2 --vk --out results/partC3/G${G}_N${N}_a > results/partC3/G${G}_N${N}_a.stdout 2> results/partC3/G${G}_N${N}_a.time
      $CAP ./run.sh nr_gpp.py --gamma $G --value $FC $sarg --N $N --rbox $R --ls 3,4 --out results/partC3/G${G}_N${N}_b > results/partC3/G${G}_N${N}_b.stdout 2> results/partC3/G${G}_N${N}_b.time
    else
      $CAP ./run.sh nr_gpp.py --gamma $G --value $FC $sarg --N $N --rbox $R --ls 0,1,2,3,4 --vk --out results/partC3/G${G}_N${N} > results/partC3/G${G}_N${N}.stdout 2> results/partC3/G${G}_N${N}.time
    fi
  done
  prevbg=$(ls results/partC3/G${G}_N${NC}*_bg.npz | head -1); prevG=$G
done <<'LIST'
1e-8 8000 1000 1500
1e-9 19700 1000 1500
1e-10 54070 1200 1800
1e-11 158900 1600 2400
1e-12 484900 1700 2500
LIST
echo done > results/partC3/DONE
