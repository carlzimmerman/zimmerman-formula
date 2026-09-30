#!/usr/bin/env python3
"""Transcribe Table 1 of Heintz & Watson 2020 (arXiv:2001.05770; ApJL 889, L7) from the text of the PDF that the page read returned (cached by the fetch tool, not committed), and check the paper's quoted fit against its own table."""
import re, csv, sys, numpy as np
L = open(sys.argv[1]).read().splitlines(); rows = []; kind = None
for l in L:
    if "GRB DLAs" in l: kind = "GRB-DLA"
    if "QSO DLAs" in l: kind = "QSO-DLA"
    m = re.match(r"\s*(\d{6}A|J\s?\d{4}[+−\-]\d{4})\s+([\d.]+)\s+([\d.]+) ± ([\d.]+)\s+([\d.]+) ± ([\d.]+)\s+([−\-\d.]+) ± ([\d.]+)\s+([−\-\d.]+) ± ([\d.]+)\s+(\(\S+\))", l)
    if m and kind:
        g = [x.replace("−", "-") for x in m.groups()]; rows.append([kind, g[0].replace(" ", "")] + g[1:])
with open("heintz_watson2020_table1.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["type", "source", "z_abs", "logN_H2", "e_logN_H2", "logN_CIstar", "e_logN_CIstar", "log_Z_Zsun", "e_log_Z", "log_alpha_CI", "e_log_alpha_CI", "refs"]); w.writerows(rows)
x = np.array([float(r[7]) for r in rows]); y = np.array([float(r[9]) for r in rows]); e = np.array([float(r[10]) for r in rows]); z = [float(r[2]) for r in rows]
print("N", len(rows), "GRB", sum(r[0] == "GRB-DLA" for r in rows), "z range", min(z), max(z))
res = y - (-1.13 * x + 1.33); print("rms of table points about the PAPER's relation: %.2f dex; median |res| %.2f; max |res| %.2f" % (np.std(res), np.median(abs(res)), abs(res).max()))
p = np.polyfit(x, y, 1); print("unweighted OLS refit: slope %.2f intercept %.2f, rms %.2f" % (p[0], p[1], np.std(y - np.polyval(p, x))))
w_ = 1 / np.maximum(e, 0.05) ** 2; pw = np.polyfit(x, y, 1, w=np.sqrt(w_)); print("error-weighted refit (floor 0.05): slope %.2f intercept %.2f" % tuple(pw))
sel = np.abs(x) < 0.4; print("objects within |log Z| < 0.4: n=%d, rms about paper relation %.2f" % (sel.sum(), np.std(res[sel])))
# --- internal-consistency check: the paper's Eq. 3, alpha_CI = 1.30e-4 N(H2)/N(CI*) [Msun/(K km/s pc2)], applied to the table's own column densities
nh = np.array([float(r[3]) for r in rows]); nc = np.array([float(r[5]) for r in rows]); enh = np.array([float(r[4]) for r in rows]); enc = np.array([float(r[6]) for r in rows])
calc = np.log10(1.30e-4) + nh - nc; ecalc = np.hypot(enh, enc); d = y - calc
print("\nEq.3 check (table value minus value recomputed from the table's own columns):")
for r, a, b, c in zip(rows, calc, d, ecalc): 
    if abs(b) > 0.05: print("  %-12s table %.2f  Eq.3 %.2f  diff %+.2f (Eq.3 error %.2f)" % (r[1], float(r[9]), a, b, c))
ok = np.abs(d) <= 0.05; print("rows consistent within 0.05 dex: %d of %d" % (ok.sum(), len(rows)))
pc = np.polyfit(x, calc, 1); print("OLS refit using Eq.3-recomputed alpha: slope %.2f intercept %.2f rms %.2f; rms about the paper relation %.2f; median |res| %.2f" % (pc[0], pc[1], np.std(calc - np.polyval(pc, x)), np.std(calc - (-1.13 * x + 1.33)), np.median(abs(calc - (-1.13 * x + 1.33)))))
wc = 1 / np.maximum(ecalc, 0.05) ** 2; pcw = np.polyfit(x, calc, 1, w=np.sqrt(wc)); print("error-weighted refit (Eq.3 values, floor 0.05): slope %.2f intercept %.2f" % tuple(pcw))
