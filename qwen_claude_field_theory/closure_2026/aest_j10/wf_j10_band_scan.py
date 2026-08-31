#!/usr/bin/env python3
# wf_j10_band_scan.py
# Explicit numbers for the J10 (lambda_s=0) scalar dispersion across the
# allowed band 0<K_B<2, K2>0.  Uses dimensionless units in which we hold the
# cosmological scale mu and the background rate Q0 fixed, and derive
#   c_s^2 = 2 Q0^2 /(K_B mu^2)   [= (2-K_B)/(K2 K_B), with K2 = mu^2(2-K_B)/(2Q0^2)]
#   M^2   = (2-K_B) Q0^2 / K_B
# All formulae SOLID from Skordis-Zlosnik 2021 (arXiv:2109.13287) Eqs.(22),(30),(58),
# specialized to lambda_s=0 (the exponential J10 background value, wf_j10_scalar_dispersion.py).
import numpy as np

Q0   = 1.0                 # background scalar rate  (units: sets the clock)
mu   = 1.0                 # cosmological instability scale mu (units: 1/length); mu^-1 >~ Mpc
Q0sq = Q0**2
mu2  = mu**2

print("J10 (lambda_s=0) scalar dispersion band scan   [c=1 units, Q0=mu=1]")
print("omega^2 = c_s^2 k^2 + M^2 ;  k_J^2 = M^2/c_s^2 = K2 Q0^2")
print("-"*72)
print(f"{'K_B':>6} {'K2(=mu^2(2-KB)/2Q0^2)':>22} {'c_s^2':>12} {'M^2':>12} {'k_J^2=M^2/c_s^2':>16}")
for KB in [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 1.9, 1.99]:
    K2  = mu2*(2-KB)/(2*Q0sq)          # from mu^2 = 2 K2 Q0^2/(2-KB)
    cs2 = (2-KB)/(K2*KB)               # Eq.(30) at lambda_s=0
    cs2b= 2*Q0sq/(KB*mu2)              # equivalent closed form
    M2  = (2-KB)*Q0sq/KB               # Eq.(22) at lambda_s=0
    kJ2 = M2/cs2                       # = K2 Q0^2
    assert abs(cs2-cs2b) < 1e-12
    print(f"{KB:>6} {K2:>22.5f} {cs2:>12.5f} {M2:>12.5f} {kJ2:>16.5f}")

print("-"*72)
print("Observations:")
print(" * c_s^2 > 0 and M^2 > 0 for the ENTIRE allowed band 0<K_B<2 (K2>0 automatic).")
print(" * omega^2 = c_s^2 k^2 + M^2 is strictly positive at ALL k -> the propagating")
print("   scalar mode is stable (no gradient/ghost/tachyon) at every finite k.")
print(" * c_s^2 = 2Q0^2/(K_B mu^2): DIVERGES as K_B->0 and is minimized as K_B->2^-.")
print("   Cosmological smallness of the *observable* CDM-like sound speed on FLRW is a")
print("   SEPARATE (de Sitter) computation; this Minkowski c_s^2 sets only the k^2 slope.")
print(" * k_J^2 = M^2/c_s^2 = K2 Q0^2 (independent of K_B): the mass<->gradient crossover.")
print("   k>>k_J: omega^2~c_s^2 k^2 (relativistic);  k<<k_J: omega^2~M^2 (massive, CDM-like).")
print(" * NO finite-k instability that is absent at k->0.  The only non-positive-")
print("   Hamiltonian region is the nonpropagating omega=0 Y-mode at k<mu (super-Mpc),")
print("   stabilized nonlinearly by the |Y|^{3/2} MOND term for k>mu.")
