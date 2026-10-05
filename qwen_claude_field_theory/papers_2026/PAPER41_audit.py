"""PAPER41 audit: every tagged number in PAPER41_kernel_tail_fix_2026.tex is checked against the committed sources
(PAPER41_figures_numbers.json; sonnet55_push/puzzle_32pi/p35_kernel_tail_fix.out). Exit 0 iff all rows pass."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "..", ".."))
tex = open(os.path.join(H, "PAPER41_kernel_tail_fix_2026.tex")).read()
J = json.load(open(os.path.join(H, "PAPER41_figures_numbers.json")))
P35 = open(os.path.join(R, "sonnet55_push", "puzzle_32pi", "p35_kernel_tail_fix.out")).read()
rows = []
def row(name, ok): rows.append(ok); print(("PASS  " if ok else "FAIL  ") + name)
def intex(s): return s in tex
row("1279x Earth (exact law)", J["exact_law_earth_ratio"] == 1279 and intex("1279 times"))
row("vacuum k=2: 77.85 / 99.81 / 784.4", J["vac_k2"] == {"100": 77.85, "128": 99.81, "1000": 784.4} and all(intex(v) for v in ("77.85", "99.81", "784.4")))
row("y_t for 32 pi: 128.9 / 167.5 / 182.4", J["yt_32pi"] == {"2": 128.9, "3": 167.5, "4": 182.4} and all(intex(v) for v in ("128.9", "167.5", "182.4")))
row("planet windows 7.7e5 / 1.77e6 / 5.4e7 / 1.81e8", J["planet_ytmax"] == {"Mercury": 5.4e7, "Venus": 1.81e8, "Earth": 1.77e6, "Mars": 7.7e5}
    and all(intex(v) for v in ("7.7\\times10^5", "1.77\\times10^6", "5.4\\times10^7", "1.81\\times10^8")))
row("worst planet at 128: 2.8e-8", abs(J["worst_planet_ratio_128"] - 2.77e-8) < 1e-10 and intex("2.8\\times10^{-8}"))
off = J["offset_reading_measured_a0"]
row("offset table", [off[k]["yt_k2"] for k in ("framework footing 9.3603e-11", "MIGHTEE 1.05e-10", "SPARC record 1.0766e-10", "lane V ensemble 1.097e-10")] == [128.9, 102.6, 97.6, 94.1]
    and [off[k]["Lambda_over_a0sq"] for k in ("framework footing 9.3603e-11", "MIGHTEE 1.05e-10", "SPARC record 1.0766e-10", "lane V ensemble 1.097e-10")] == [100.53, 79.89, 75.99, 73.19]
    and all(intex(v) for v in ("& 100.53 & 128.9", "& 79.89 & 102.6", "& 75.99 & 97.6", "& 73.19 & 94.1")))
dchi = re.findall(r"y_t =\s+(\d+): ([+-]\d+\.\d+)", P35)
row("SPARC Delta chi2 rows match p35.out", [v for _, v in dchi] == ["+0.07", "+0.04", "+0.00", "-1.06", "-0.67", "-0.01"] and intex("$+0.07$, $+0.04$, $0.00$") and intex("$-1.06$, $-0.67$, $-0.01$"))
row("p35 passed 4/4", "4/4 pass" in P35)
P36 = open(os.path.join(R, "sonnet55_push", "puzzle_32pi", "p36_sparc_turnoff_fit.out")).read()
row("p36 lower bounds 20 / 2", "Delta chi2 < 4 for y_t >= 20" in P36 and "Delta chi2 < 4 for y_t >= 2;" in P36 and "y_t\\ge20$" in tex and "$\\ge2$ with" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
