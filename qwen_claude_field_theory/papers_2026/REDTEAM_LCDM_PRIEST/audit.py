#!/usr/bin/env python3
"""Red-team paper audit: each quoted number appears in the TeX and in the rerun script output beside it.
Run: python3 audit.py (exit 0 only if all pass). Hypothetical rival, not a framework result. kappa = 1/2 FITTED; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(H, "REDTEAM_lcdm_priest_paper.tex"), encoding="utf-8").read()
L = [
 ("9.17\\times10^{-11}", "d", "g=9.17e-11"), ("3.43\\times10^{-11}", "b", "g0=3.43e-11"), ("2.86\\times10^{-10}", "b", "g0=2.86e-10"),
 ("7.45\\times10^{-11}", "b", "Mstar g0 logmean 7.451e-11"), ("5.21\\times10^{-11}", "b", "num g0 logmean 5.205e-11"),
 ("1.345 times", "e", "multiplier on K13: 1.345"), ("2.58 times", "e", "blumenthal 2.58"), ("2.06 (Gnedin)", "e", "gnedin 2.06"), ("0.81 times", "e", "no scatter 0.81"), ("0.91 and 1.09", "e", "0.91 1.09"),
 ("$a=9.09$, $9.19$ and $9.11", "e", "a 9.188e-11"), ("0.073--0.078", "e", "rms 0.078"), ("0.073--0.078", "e", "rms 0.073"),
 ("is $+0.13$ for $g_0$", "b", "fixed M=0.130"), ("$+0.07$ for the tuned", "e", "rde tuned slope 0.073"), ("1.49--1.89", "f", "M/Mlaw 1.49"), ("1.49--1.89", "f", "M/Mlaw 1.89"),
 ("0.99, 1.07, 1.28", "f", "tuned none z 1 0.99"), ("0.99, 1.07, 1.28", "f", "tuned none z 2.33 1.28"), ("1.26, 1.50 and 2.03", "f", "blum z 1 1.26"), ("1.26, 1.50 and 2.03", "f", "blum z 2.33 2.03"),
 ("714 definitions", "d", "N defs 714"), ("20 (2.8", "d", "20 (2.8%)"), ("median is 12 hits", "d", "median 12"), ("37\\,\\%", "d", "frac with>=hit 0.37"),
 ("$\\hat\\kappa=0.500$", "e", "kappa_hat 0.500"), ("0.432", "e", "kappa_hat 0.432"), ("0.726", "e", "kappa_hat 0.726"), ("0.994", "e", "kappa_hat 0.994"),
 ("$-0.34$ per dex", "e", "-0.34457"), ("by 0.24\\,dex", "e", "scatter 0.24"), ("1.59--1.73", "c", "sigma cdm/ law 1.59"), ("1.59--1.73", "f", "UFD sigma ratio 1.73"),
 ("0.94--0.97", "f", "[0.95 0.94 0.94 0.97]"), ("$-0.22$\\,dex", "f", "300 log(gCDM 1-halo/glaw) -0.22"), ("$-0.73$ at 1\\,Mpc", "f", "1000 log(gCDM 1-halo/glaw) -0.73"),
 ("$\\alpha^3=0.0997$", "d", "red 0.0997"), ("0.575", "d", "kappa 0.575"), ("0.557", "d", "0.557"), ("$+0.19$", "c", "rde dln a_RAR slope 0.185"),
 ("$4.7\\times10^{-13}$--$3.1\\times10^{-12}$", "a_collapse", "'ta': '4.74e-13'"), ("$4.7\\times10^{-13}$--$3.1\\times10^{-12}$", "a_collapse", "'200c': '3.11e-12'"),
 ("rms 0.0000\\,dex, spread 0.001\\,dex", "tune", "per-mass spread 0.001 dex; rms to law 0.0000 dex"), ("0.04\\,kpc", "tune_diag", "10.0  0.061  0.04"), ("0.98\\,$a_0$", "tune_diag", "246.161  0.98"), ("93--246", "tune_diag", "93.013"),
 ("ratio 1.002", "tune_A1", "ratio 1.0017"), ("0.247\\,dex", "tune_A1", "spread 0.247 dex; rms to law 0.0226 dex"), ("rms 0.0054\\,dex and spread 0.012", "tune_A1", "spread 0.012 dex; rms to law 0.0054 dex"),
 ("0.03\\,kpc", "tune_A1", " 10.0  0.006  0.03"), ("0.14\\,kpc", "tune_A1", " 11.2  0.023  0.14"), ("$+0.182$", "tune_A1", "rho_DE slope +0.182"), ("$\\rho_{\\rm DE}^{0.30}$", "tune_A1", "rho_DE^0.30"), ("$+0.500$", "tune_A1", "rho_DE slope +0.500"),
 ("0.455, 0.665, 0.800", "tune_A1", "0.455, (0.685, 73.0): 0.665, (0.65, 73.0): 0.8}"), ("1.79, 2.07, 2.68", "tune_A1", "1.0: 1.793, 1.5: 2.071, 2.33: 2.678"),
 ("$+0.041$, $-0.098$, $-0.183$", "tune_A1", "(0.65, 73.0) -0.183 dex"), ("$-0.306$, $-0.384$, $-0.617$", "tune_A1", "redshift 2.33 -0.617 dex"), ("1.56, 1.44, 1.25, 0.55", "tune_A1", "at R200 0.55"),
]
F = 0
for frag, s, lit in L:
    a = frag in T; b = lit in open(os.path.join(H, "scripts", s + ".out"), encoding="utf-8").read()
    if not (a and b): F += 1; print("  FAIL", "TeX" if not a else "", "SRC" if not b else "", repr(frag), s, repr(lit))
for need in ("FICTIONAL AUTHOR", "NOT A DERIVATION", "fitted", "not closed", "Do not circulate Part~I without Part~II"):
    if need not in T: F += 1; print("  FAIL missing", need)
print(f"{len(L) + 5 - F} of {len(L) + 5} checks pass")
sys.exit(1 if F else 0)
