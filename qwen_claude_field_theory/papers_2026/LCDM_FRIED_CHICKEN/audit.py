#!/usr/bin/env python3
"""Each quoted number appears in the TeX and in the script output beside it. Exit 0 only if all pass.
Rival-flavoured exercise, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(H, "lcdm_fried_chicken.tex"), encoding="utf-8").read()
R = {s: open(os.path.join(H, "scripts", s + ".out"), encoding="utf-8").read() for s in ("recipe", "recipe2")}
L = [("3373", "recipe", "3373 points"), ("171", "recipe", "171 galaxies"), ("0.1951", "recipe", "rms 0.1951"),
 ("0.1419 & 0.2877 & 0.1613 & 15.76", "recipe", "0.1419 dex [FAIL E1]; p95 per-galaxy 0.2877 [FAIL E2]; worst bin 0.1613"), ("15.76", "recipe", "a fit 1.576e-10"),
 ("0.0715 & 0.1486 & 0.0441 & 9.12", "recipe", "0.0715 dex [FAIL E1]; p95 per-galaxy 0.1486 [FAIL E2]; worst bin 0.0441"), ("9.12", "recipe", "a fit 9.122e-11"),
 ("0.0721 & 0.1357 & 0.0283 & 8.65", "recipe", "0.0721 dex [FAIL E1]; p95 per-galaxy 0.1357 [FAIL E2]; worst bin 0.0283"), ("8.65", "recipe", "a fit 8.647e-11"),
 ("0.2245 & 0.3187 & 0.2261 & 6.06", "recipe2", "0.2245 dex [FAIL E1]; p95 per-galaxy 0.3187 [FAIL E2]; worst bin 0.2261"), ("6.06", "recipe2", "a fit 6.059e-11"), ("0.2245", "recipe", "0.2245 dex"),
 ("0.0609 & 0.1119 & 0.0260 & 8.97", "recipe", "0.0609 dex [FAIL E1]; p95 per-galaxy 0.1119 [FAIL E2]; worst bin 0.0260"), ("8.97", "recipe", "a fit 8.970e-11"),
 ("0.0408 & 0.0777 & 0.0413 & 9.21", "recipe2", "0.0408 dex [FAIL E1]; p95 per-galaxy 0.0777 [FAIL E2]; worst bin 0.0413"), ("9.21", "recipe2", "a fit 9.209e-11"), ("0.1964", "recipe2", "rms to observed 0.1964"),
 ("0.0396 & 0.0665 & 0.0148 & 9.72", "recipe2", "0.0396 dex [FAIL E1]; p95 per-galaxy 0.0665 [FAIL E2]; worst bin 0.0148"), ("9.72", "recipe2", "a fit 9.719e-11"),
 ("\\textbf{0.0056} & \\textbf{0.0130} & \\textbf{0.0031}", "recipe2", "0.0056 dex [PASS E1]; p95 per-galaxy 0.0130 [PASS E2]; worst bin 0.0031"),
 ("\\textbf{0.0075} & \\textbf{0.0118} & \\textbf{0.0180}", "recipe2", "0.0075 dex [PASS E1]; p95 per-galaxy 0.0118 [PASS E2]; worst bin 0.0180"), ("9.585\\times10^{-11}", "recipe2", "g_dagger=9.585e-11"), ("1.024 $a_0$", "recipe2", "ratio to a0 1.024"),
 ("median ratio 1.017", "recipe", "median 1.017"), ("0.568 to 3.174", "recipe", "0.568-3.174"),
 ("median $+0.29$ and $+1.2$", "recipe2", "[[0.29, -0.42, 0.9, 0.11], [-0.38, -0.81, 0.15, 0.03], [1.2, 0.03, 1.0, 0.35]]"), ("median $-0.42$, reaching $-0.81$", "recipe2", "[[0.29, -0.42"), ("(median 0.9)", "recipe2", "[[0.29, -0.42, 0.9"),
 ("171 of 171, the isotropic Jeans dispersion", "recipe", "C1 density positive to R200: 171 of 171"), ("Jeans dispersion is positive in 171 of 171", "recipe", "C2 Jeans sigma_r^2 positive: 171 of 171"), ("peak in 171 of 171", "recipe", "C3 Eddington f(E) >= -1% of peak inside R200: 171 of 171"),
 ("$+0.0000$ for Hernquist and $-0.2555$", "recipe2", "Hernquist self-consistent +0.0000; cored tracer in point mass -0.2555"),
 ("158 of 171", "recipe", "monotonic: 158 of 171"), ("median rms 0.057\\,dex and 0.261", "recipe", "median 0.057 dex, p84 0.261"), ("0.32 of", "recipe", "c_fit/c_Diemer median 0.32"), ("median $+0.16$", "recipe", "median +0.16"), ("$-0.76$", "recipe", "log M_b 11-12: n 20, median -0.76"),
 ("slope is $+0.235$", "recipe2", "rho_DE slope +0.235 [FAIL]"), ("\\rho_{\\rm DE}^{0.23}", "recipe2", "p = 0.23: slope +0.500"), ("0.446, 0.682, 0.851", "recipe2", "with p 0.446"), ("0.446, 0.682, 0.851", "recipe2", "with p 0.682"), ("0.446, 0.682, 0.851", "recipe2", "with p 0.851"),
 ("1.43, 1.85, 2.90", "recipe2", "{1.0: 1.427, 1.5: 1.846, 2.33: 2.904}"), ("(1+z)^{-1.11}", "recipe2", "q = -1.11"), ("0.74, 0.86, 1.25", "recipe2", "{1.0: 0.736, 1.5: 0.856, 2.33: 1.248} E5 False"), ("$+0.810$", "recipe", "rho_DE slope +0.810")]
F = 0
for frag, s, lit in L:
    a, b = frag in T, lit in R[s]
    if not (a and b): F += 1; print("  FAIL", "TeX" if not a else "", "SRC" if not b else "", repr(frag), s, repr(lit))
NEED = ("ACDM flavored fried chicken version of Galaxy Dnynamics", "carries no physics", "fitted", "not evidence", "Not deposited")
for n in NEED:
    if n not in T: F += 1; print("  FAIL missing", n)
print(f"{len(L) + len(NEED) - F} of {len(L) + len(NEED)} checks pass")
sys.exit(1 if F else 0)
