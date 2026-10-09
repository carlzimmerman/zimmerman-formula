"""PAPER42 audit: tagged numbers in PAPER42_mond_vacuum_dark_energy_2026.tex vs committed sources. Exit 0 iff all rows pass."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, "..", ".."))
tex = open(os.path.join(H, "PAPER42_mond_vacuum_dark_energy_2026.tex")).read()
J = json.load(open(os.path.join(H, "PAPER42_figures_numbers.json"))); J41 = json.load(open(os.path.join(H, "PAPER41_figures_numbers.json")))
pz = lambda f: open(os.path.join(R, "sonnet55_push", "puzzle_32pi", f)).read()
rows = []
def row(n, ok): rows.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
row("obs Lambda/a0^2 73.19, bands 57.3-93.4 (1 sigma), 44.9-119.2 (2 sigma), log-mapped", J["obs_Lambda_over_a0sq"] == 73.19 and J["obs_band_1sigma"] == [57.3, 93.4] and J["obs_band_2sigma"] == [44.9, 119.2]
    and "73.19" in tex and "$57.3$--$93.4$ at $1\\sigma$" in tex and "$44.9$--$119.2$ at $2\\sigma$" in tex and "sd(ln) 12.2%" in open(os.path.join(R, "sonnet55_push", "puzzle_32pi", "agents", "V_evidence_for_the_coefficient", "v01_determinations_table.out")).read())
row("y_t = 94 (74-120 at 1 sigma, 58-153 at 2 sigma), framework 128.9", round(J["yt_obs"]) == 94 and [round(v) for v in J["yt_band_1sigma"]] == [74, 120]
    and [round(v) for v in J["yt_band_2sigma"]] == [58, 153] and J["yt_framework"] == 128.9 and "$y_t=94$" in tex and "74\\text{--}120" in tex and "58\\text{--}153" in tex and "128.9" in tex)
row("RAR kernel vacuum 12.99 (p21)", "Lambda = 12.988 a0^2" in pz("p21_bimond_vacuum.out") and "12.99" in tex)
row("Upsilon-free best y_t = 5 at -53.2, bulge -14.4 (p36)", "best y_t = 5 (Delta chi2 -53.22)" in pz("p36_sparc_turnoff_fit.out") and "best y_t = 5 (Delta chi2 -14.40)" in pz("p36_sparc_turnoff_fit.out") and "-53.2" in tex and "-14.4" in tex)
row("g_t ~ 1.0e-8", abs(J["gt_obs_ms2"] - 1.03e-8) < 1e-10 and "1.0\\times10^{-8}" in tex)
row("1279x Earth", J41["exact_law_earth_ratio"] == 1279 and "1279 times" in tex)
row("planet window 7.7e5", J41["planet_ytmax"]["Mars"] == 7.7e5 and "7.7\\times10^5" in tex)
row("k = 3, 4: 167.5, 182.4", J41["yt_32pi"]["3"] == 167.5 and J41["yt_32pi"]["4"] == 182.4 and "167.5" in tex and "182.4" in tex)
row("SPARC |Delta chi2| <= 1.06 (p35)", "-1.06" in pz("p35_kernel_tail_fix.out") and "1.06" in tex)
row("y_t lower bounds 20 (Upsilon fixed) and 2 (free) (p36)", "Delta chi2 < 4 for y_t >= 20" in pz("p36_sparc_turnoff_fit.out") and "Delta chi2 < 4 for y_t >= 2;" in pz("p36_sparc_turnoff_fit.out") and "y_t\\ge20" in tex and "y_t\\ge2$" in tex)
row("class identity + exchange symmetry (p25 6/6, Lean chain present)", "6/6 pass" in pz("p25_symmetric_bimond_map.out") and os.path.exists(os.path.join(R, "fable_independent_2026", "lean_2026", "PUZZLE_32pi_chain_2026_10_05.out")))
row("Upsilon trend 141 -> 12 (p37b)", re.search(r"Upsilon 0.5:.*RAR -141", pz("p37b_shape_vs_upsilon.out")) and re.search(r"Upsilon 0.7:.*RAR -12", pz("p37b_shape_vs_upsilon.out")) and "141" in tex and "to 12" in tex)
row("postulate independence (Lean out lists standard axioms only)", "sorryAx" not in open(os.path.join(R, "fable_independent_2026", "lean_2026", "PUZZLE_32pi_postulate_status_2026_10_05.out")).read())
P38 = pz("p38_high_accel_turnoff.out")
row("p38: ATLAS3D 187, y <= 38, ~1e-4 dex, 60x / ~900x", "N = 187" in P38 and "max 38.1" in P38 and "sample mean -0.00011" in P38 and "187 ATLAS3D" in tex and "60 times" in tex and "900 times" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
