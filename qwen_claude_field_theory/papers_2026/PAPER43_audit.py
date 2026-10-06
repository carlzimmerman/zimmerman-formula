"""PAPER43 audit: tagged numbers in PAPER43_gas_point_a0_2026.tex against PAPER43_figures_numbers.json (itself parsed from committed .out files) and the outputs."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, "..", "..", "sonnet55_push", "puzzle_32pi")
tex = open(os.path.join(H, "PAPER43_gas_point_a0_2026.tex")).read(); J = json.load(open(os.path.join(H, "PAPER43_figures_numbers.json")))
rd = lambda f: open(os.path.join(P, f)).read()
rows = []
def row(n, ok): rows.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
row("TRGB 8 gal 70 pts 1.158 20%", J["trgb"][:1] == [1.158e-10] and J["trgb"][2:] == [8, 70] and abs(J["trgb"][1] - 0.202) < 1e-9 and "& 8 & 70 & $1.158\\pm20\\%$" in tex)
row("Hubble flow 11/54 0.697 18%", J["hf"][2:] == [11, 54] and abs(J["hf"][0] - 6.97e-11) < 1e-14 and "& 11 & 54 & $0.697\\pm18\\%$" in tex)
row("all 19/124 0.900 14%", J["all"][2:] == [19, 124] and abs(J["all"][0] - 8.999e-11) < 1e-13 and "& 19 & 124 & $0.900\\pm14\\%$" in tex)
row("WALLABY 46/218 0.728 23%", J["wallaby"][2:] == [46, 218] and abs(J["wallaby"][0] - 7.282e-11) < 1e-14 and "& 46 & 218 & $0.728\\pm23\\%$" in tex)
row("LITTLE THINGS 22/720 0.780 41%", J["lt"][2:] == [22, 720] and abs(J["lt"][0] - 7.796e-11) < 1e-14 and "& 22 & 720 & $0.780\\pm41\\%$" in tex)
row("pool 8.32e-11 13%, Q 3.97, I2 24", abs(J["pool"][0] - 8.318e-11) < 1e-14 and J["Q"] == 3.97 and J["I2"] == 24 and "$Q=3.97$" in tex and "$I^2=24\\%$" in tex and "0.832\\pm13\\%" in tex)
pl = J["pulls"]
row("pulls 0.88 0.62 0.27 1.69 2.30 2.74", [pl["kappa=1/2 rho_Lambda"], pl["Verlinde 6 rho_L"], pl["Milgrom 2pi rho_L"], pl["Milgrom 2pi rho_tot"], pl["alt rho_total (original)"], pl["SPARC conventional 1.2e-10"]] == [0.88, 0.62, 0.27, 1.69, 2.3, 2.74]
    and all(s in tex for s in ("$+0.88\\sigma$", "$+0.62$", "$+0.27$", "$+1.69$", "$+2.30$", "$+2.74$")))
row("gas-point Upsilon spread 11.2%, galaxy-level 63%", J["spread_fcut08"] == 11.2 and "11.2\\%" in tex and "spread 63.1%" in rd("p41_pin_mass_to_light.out") and "63\\%" in tex)
row("RAR Delta chi2 +5.0 on gas points", J["rar_dchi2_U05"] == 5.0 and "+5.0" in tex)
o43 = rd("p43_wallaby_gas_points.out")
row("WALLABY systematics: EFE +8.5%, flux 8.349 (+15%), AD 7.681 (+5%), CMB 4.883 (-33%)", "+8.5% at maxclu" in o43 and "uncorrected: 8.349e-11" in o43 and "8 km/s: 7.681e-11" in o43 and "/73): 4.883e-11" in o43
    and all(s in tex for s in ("$+8.5\\%$", "15\\%", "5\\%", "$-33\\%$")))
o47 = rd("p47_little_things_a0.out")
row("LT overlap ratios 1.58 / 2.42 / 1.60 -> 'factor 1.6-2.4'", all(s in o47 for s in ("ratio 2.42", "ratio 1.60", "ratio 1.58")) and "1.6--2.4" in tex)
row("p44 scatter 0.604 -> 0.60", "scatter s = 0.604" in rd("p44_samplesize_and_bayes.out") and "0.60 in $\\ln a_0$" in tex)
row("Freeman control 0.94% -> 0.9%", "max 0.94%" in o43 and "0.9\\%" in tex)
print(f"\n{sum(rows)}/{len(rows)} audit rows pass"); sys.exit(0 if all(rows) else 1)
