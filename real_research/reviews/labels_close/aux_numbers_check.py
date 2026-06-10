#!/usr/bin/env python3
"""Verify the finding's auxiliary key_numbers independently."""
import numpy as np

c=2.998e8; G=6.674e-11; Msun=1.989e30
a0=9.36e-11
Z=np.sqrt(32*np.pi/3)
H_Lambda=a0*Z/c
M_dS=c**2/(G*H_Lambda)
print("KEY NUMBERS")
print(f"  Z = sqrt(32pi/3)         = {Z:.4f}   (finding: 5.789)")
print(f"  H_Lambda = a0 Z / c      = {H_Lambda:.3e} /s   (finding: 1.80e-18)")
print(f"  a0 = c H_Lambda / Z      = {c*H_Lambda/Z:.3e}   (target 9.36e-11)")
print(f"  M_dS = c^2/(G H_Lambda)  = {M_dS/Msun:.3e} Msun   (finding: 3.768e14)")

print("\nCONICAL DEFICITS alpha = 2pi M/M_dS (small-M):")
for nm,Ms in [("spiral",3e10),("MW",1e11),("massive",1e12),("cluster",1e15)]:
    alpha = 2*np.pi*(Ms*Msun)/M_dS
    print(f"  {nm:>10} M={Ms:.0e}:  alpha = {alpha:.3e}   (finding: spiral 5.0e-4, MW 1.7e-3, massive 1.7e-2, cluster O(10))")

print("\nSINGLET FRACTION ~ 1/N^2  (bilinear singlets / all degree-2 ops):")
for N in (64,256,1024,4096):
    nops = N*(N-1)//2 + N
    frac = 1/nops
    print(f"  N={N:>5}: 1/(C(N,2)+N) = {frac:.2e}   (finding: 4.8e-4 at N=64 -> 1.2e-7 at N=4096)")

print("\nRMS|E|/E0 limits (independent):")
for q in (0.7,0.9,0.95):
    n0=0.5*np.sqrt(1-q)         # n=0
    print(f"  q={q}: n=0 RMS|E|/E0 = (1/2)sqrt(1-q) = {n0:.4f};  n->inf = 1/sqrt2 = {1/np.sqrt(2):.4f}")
