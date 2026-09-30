#!/usr/bin/env python3
"""Section 2c of GAS_ANCHOR_SCOPING: test the row-permutation hypothesis and the source-CI* basis for the tabulated alpha_[CI] of Heintz & Watson 2020 Table 1, and refit with the corrected alpha column."""
import csv, numpy as np
R = list(csv.DictReader(open("heintz_watson2020_table1.csv")))
name = [r["source"] for r in R]; x = np.array([float(r["log_Z_Zsun"]) for r in R]); tab = np.array([float(r["log_alpha_CI"]) for r in R]); etab = np.array([float(r["e_log_alpha_CI"]) for r in R])
eq3 = np.array([np.log10(1.3e-4) + float(r["logN_H2"]) - float(r["logN_CIstar"]) for r in R]); eeq3 = np.array([np.hypot(float(r["e_logN_H2"]), float(r["e_logN_CIstar"])) for r in R])
idx = {n: i for i, n in enumerate(name)}
print("QSO rows: tabulated alpha vs Eq.3 of another row (cyclic hypothesis)")
for row, donor in (("J0643-5041", "J0551-3638"), ("J0551-3638", "J1232+0815"), ("J1232+0815", "J1444+0126"), ("J1444+0126", "J0643-5041")):
    i, j = idx[row], idx[donor]; print("  %-11s tab %.2f+-%.2f   Eq.3 of %-11s %.2f+-%.2f   diff %+.2f" % (row, tab[i], etab[i], donor, eq3[j], eeq3[j], tab[i] - eq3[j]))
# GRB rows: alpha implied CI* from the tabulated alpha and N(H2)
print("GRB rows: CI* implied by the tabulated alpha (N(H2) as printed)")
for g in ("120815A", "150403A", "190114A", "181020A"):
    i = idx[g]; imp = float(R[i]["logN_H2"]) + np.log10(1.3e-4) - tab[i]; print("  %-8s printed CI* %.2f+-%.2f   implied by alpha %.2f   (alpha error %.2f)" % (g, float(R[i]["logN_CIstar"]), float(R[i]["e_logN_CIstar"]), imp, etab[i]))
# corrected alpha column: QSO rows from Eq.3 of the sources' own columns; GRB rows as tabulated (they follow the source CI*)
corr = tab.copy()
for n in ("J0643-5041", "J0551-3638", "J1232+0815", "J1444+0126"): corr[idx[n]] = eq3[idx[n]]
paper = -1.13 * x + 1.33
for lab, y in (("as printed", tab), ("QSO rows corrected (cycle undone)", corr)):
    p = np.polyfit(x, y, 1); print("%-36s rms about paper relation %.2f dex (median |res| %.2f); OLS slope %.2f intercept %.2f rms %.2f" % (lab, np.std(y - paper), np.median(abs(y - paper)), p[0], p[1], np.std(y - np.polyval(p, x))))
