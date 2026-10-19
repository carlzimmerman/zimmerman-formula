#!/bin/bash
# Part N: nonradial + radial spectra of the NR-GPP shadow of the diffuse benchmark (Gamma=1e-8, fixed f_c).
cd "$(dirname "$0")"
SEED=../../full_two_field_2026_10_19/equilibria/mixed_G1em8_x04.npz
FC=0.009888264649460883
mkdir -p results/partN
run() { tag=$1; shift; ./run.sh nr_gpp.py --gamma 1e-8 --value $FC --seed $SEED --vk --coercivity --out results/partN/$tag "$@" > results/partN/$tag.stdout 2> results/partN/$tag.time; }
run fd_R8000_N1000 --N 1000 --rbox 8000 --disc fd --ls 0,1,2,3,4,8,16
run fd_R8000_N1500 --N 1500 --rbox 8000 --disc fd --ls 0,1,2,3,4,8,16
run dvr_R8000_N1000 --N 1000 --rbox 8000 --disc dvr --ls 0,1,2,3,4,8,16
run dvr_R8000_N1500 --N 1500 --rbox 8000 --disc dvr --ls 0,1,2,3,4,8,16
run fd_R8000_N2000_a --N 2000 --rbox 8000 --disc fd --ls 0,1,2
run fd_R8000_N2000_b --N 2000 --rbox 8000 --disc fd --ls 3,4,8,16
run fd_R10000_N1999_a --N 1999 --rbox 10000 --disc fd --ls 0,1,2
run fd_R10000_N1999_b --N 1999 --rbox 10000 --disc fd --ls 3,4,8,16
echo done > results/partN/DONE
