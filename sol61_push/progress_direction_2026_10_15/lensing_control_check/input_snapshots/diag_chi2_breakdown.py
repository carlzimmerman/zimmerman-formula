"""Diagnostic (not a verdict): where the KiDS-1000 absolute chi2 of the no-edge law comes from (CFG801 setup, all-radii
profiled masses 10.36/10.83/11.01/11.18).  Run from CFG801's directory: python3 ../CFG805_two_halo_t1x/diag_chi2_breakdown.py"""
import math, os, sys
import numpy as np
sys.argv = ['x']
src = open('cfg801.py').read().split('P(f"CFG801')[0]
G = {"__file__": os.path.abspath('cfg801.py'), "__name__": "d"}; exec(src, G)
fN = G['profile'](False)[0]
exec(open('cfg801.py').read().split('# data')[1].split('def model')[0], G)
R, Y, C, Gpc, a0, X = G['R'], G['Y'], G['C'], G['Gpc'], G['a0'], G['X']
def model(f, lm, Rb):
    M = 10 ** lm; rM = math.sqrt(Gpc * M / a0); x = Rb * 1e6 / rM
    return M / rM ** 2 * np.exp(np.interp(np.log(x), np.log(X), np.log(f)))
L = [10.36, 10.83, 11.01, 11.18]
r = Y.reshape(-1) - np.concatenate([model(fN, L[b], R[b]) for b in range(4)])
print("total chi2", round(float(r @ np.linalg.inv(C) @ r), 1))
for b in range(4):
    s = slice(15 * b, 15 * b + 15); rb = r[s]
    print(f"bin {b + 1}: block chi2 {float(rb @ np.linalg.inv(C[s, s]) @ rb):.1f}  pulls:", " ".join(f"{p:+.1f}" for p in rb / np.sqrt(np.diag(C[s, s]))))
print("R (Mpc):", " ".join(f"{x:.3f}" for x in R[0]))
