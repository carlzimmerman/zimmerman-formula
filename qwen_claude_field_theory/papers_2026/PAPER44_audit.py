"""PAPER44 audit: tagged numbers in the .tex against PAPER44_figures_numbers.json (parsed from committed outputs) and the record."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "..", "..")
tex = open(os.path.join(H, "PAPER44_efe_blind_mond_2026.tex")).read(); J = json.load(open(os.path.join(H, "PAPER44_figures_numbers.json")))
rows = []
def row(n, ok): rows.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
row("chi2 0.7 / 99.5 / 99.7 / 131.6", (J["chi2_noEFE"], J["chi2_SW01"], J["chi2_linear"], J["chi2_ownership"]) == (0.7, 99.5, 99.7, 131.6) and all(s in tex for s in ("& 0.7 &", "& 99.5 &", "& 99.7 &", "& 131.6 &", "$\\chi^2=0.7$", "$\\chi^2=99.7$", "$\\chi^2=99.5$")))
row("offsets +0.01 / +0.81 / +0.93", (J["offset_noEFE"], J["offset_EFE"], J["offset_own"]) == (0.01, 0.81, 0.93) and all(s in tex for s in ("$+0.01$", "$+0.81$", "$+0.93$")))
row("eta 0.59-0.81, x 0.004-0.008, r_bg 36-149", J["eta_range"] == [0.59, 0.81] and J["x_range"] == [0.004, 0.008] and J["rbg_range"] == [36, 149] and all(s in tex for s in ("0.59$--$0.81", "0.004$--$0.008", "36$--$149")))
row("Q2 2.195e-26, 6.3 sigma, kappa < 0.171", J["Q2_half"] == 2.195e-26 and J["Q2_sig_half"] == 6.3 and J["kappa_max_2s"] == 0.171 and "2.195\\times10^{-26}" in tex and "$6.3\\sigma$" in tex and "0.171" in tex)
row("no-EFE perihelia |dq| 0.00485 AU -> 0.005", abs(J["noEFE_dq"] - 0.00485) < 1e-9 and "0.005\\,AU" in tex)
row("gamma_v 1.06 / 1.20 / 1.51; SW01 1.11", round(J["gamma_iso"]["5000"], 2) == 1.06 and round(J["gamma_iso"]["10000"], 2) == 1.20 and round(J["gamma_iso"]["20000"], 2) == 1.51 and round(J["gamma_sw01_20k"], 2) == 1.11 and all(s in tex for s in ("1.06$, $1.20$, $1.51", "$1.11$")))
fs = open(os.path.join(R, "FAILURES_EXECUTIVE_SUMMARY_2026-09-28.md")).read() + open(os.path.join(R, "README.md")).read()
row("Chae 1.7-2.2 canonical / 2.7-3.0 alt in the record", "1.7–2.2σ canonical, 2.7–3.0σ alt" in fs and "$1.7$--$2.2\\sigma$" in tex and "$2.7$--$3.0\\sigma$" in tex)
fd = open(os.path.join(R, "fable_independent_2026", "FINDINGS.md")).read()
row("MW DR3 decline: isolated kernel 2.5 sigma shallower (L172)", "2.5σ shallower than quoted" in fd and "$2.5\\sigma$ shallower" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
