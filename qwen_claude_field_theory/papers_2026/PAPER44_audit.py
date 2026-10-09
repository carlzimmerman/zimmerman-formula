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
# v1.1 (2026-10-08 claim match): these rows read committed .out files, not prose summaries (the v1.0 rows checked
# FAILURES_EXECUTIVE_SUMMARY/README/FINDINGS.md, which is how a mislabelled WALLABY amplitude and a mixed-kernel range got through).
rd = lambda *q: open(os.path.join(R, *q)).read()
c8 = rd("campaign_fresh_gravity", "CFG8_chae_kernel.out")
row("Chae refit: P2 1.7 / 2.7 sigma, nu_mono 2.2 / 3.0 sigma (CFG8)", all(t in c8 for t in ("V4 P2@canonical: +0.0214 (+1.7 sigma)", "V5 P2@alt: +0.0321 (+2.7 sigma)", "V6 nu_mono@canonical: +0.0338 (+2.2 sigma)", "V7 nu_mono@alt: +0.0405 (+3.0 sigma)"))
    and "$1.7\\sigma$ on the canonical footing and $2.7\\sigma$" in tex and "$2.2$ and $3.0\\sigma$ with $\\nu_{\\rm mono}$" in tex)
l172 = rd("fable_independent_2026", "L172_mw_outer_curve_and_fgal_ledger.out")
nom = [(-0.47 - s_) / 0.15 for s_ in (-0.126, -0.117)]
row("MW decline: nominal 2.3-2.4 sigma, shallowest-model 2.5, LMC 1.1-1.6 (L172, nu_RAR)", "isolated slope = -0.126" in l172 and "isolated slope = -0.117" in l172 and "(-2.50 sigma)" in l172
    and "1.6 -> 1.2 sigma" in l172 and "1.6 -> 1.1 sigma" in l172 and [round(-v, 1) for v in nom] == [2.3, 2.4] and "$2.3$--$2.4\\sigma$" in tex and "$2.5\\sigma$" in tex and "(shallowest)" in tex and "1.1--1.6$\\sigma$" in tex)
fw = rd("prep_2026", "wallaby_firing", "fire_wallaby.out")
row("WALLABY directional stack: amplitude -1.70, analytic error 2.98 (Z -0.57), bootstrap 2.12; not a significance", "maxclu           25   -1.70   2.12    2.98  -0.57" in fw
    and "error $\\pm2.98$ (analytic; $\\pm2.12$ bootstrap)" in tex and "$0.6\\sigma$ from zero" in tex and "$0.9\\sigma$ from AQUAL;" in tex and round((1 + 1.70) / 2.98, 1) == 0.9 and "-1.7\\sigma" not in tex)
p57 = rd("sonnet55_push", "puzzle_32pi", "p57_etno_secular_nbody.out")
row("p57: K1 lost 0.573 / occupancy 0.195 vs Newton 0.187 / 0.067; verdict INCONCLUSIVE", "lost (q<25) 0.573, median final q 25.0 AU, detached occupancy 0.195" in p57
    and "lost (q<25) 0.187, median final q 32.1 AU, detached occupancy 0.067" in p57 and "VERDICT: INCONCLUSIVE" in p57
    and "57\\%" in tex and "0.195" in tex and "19\\%" in tex and "0.067" in tex and "inconclusive" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
