#!/usr/bin/env python3
"""DW2: comparisons left after dw2_second.py. Row 11 at the first implementation's sigma, f 0; LITTLE THINGS with stars; kick at v_k 0 as a baseline; second sigma for G4. kappa = 1/2 FITTED; not theory closed."""
import csv
src = open("dw2_second.py").read(); pre = src[:src.index("# ---------- row 11")]; pre = pre.replace('os.path.abspath(__file__)', 'os.path.abspath("dw2_second.py")'); exec(pre)
PR = json.load(open("dw2_proc_results.json")); SE = json.load(open("dw2_second_results.json")); O = {}
for mass in ("em1", "share"):
    sg = PR[f"star_{mass}"]["sigma"]; ret = []
    for s in SETS:
        v = []
        for q in s:
            rg, Mc, Ms = profile(q, mass, 0.0); Mx = retained(rg, Mc, Ms, sg); v.append(np.interp(q["r"].max(), rg, Mx) / np.interp(q["r"].max(), rg, Mc))
        ret.append(float(np.median(v)))
    a = PR[f"star_{mass}"]["retained"]; O[mass] = dict(second=ret, first=a); P(f"Row 11 {mass} sigma {sg:.2e} f 0: second " + " ".join(f"{x:.2f}" for x in ret) + " | first " + " ".join(f"{x:.2f}" for x in a) + " | max rel diff " + f"{max(abs(x / y - 1) for x, y in zip(ret, a)):.3f}")
LT = [r for r in csv.DictReader(open(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "little_things", "oh2015_table2.csv"))) if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun"))]
for ft, a in AF.items():
    for mass in ("em1", "share"):
        sg = SE["star"][f"{ft}|{mass}|mean"]["sigma"]; E = []; E0 = []
        for r in LT:
            R = float(r["Rmax_kpc"]); V = float(r["V_kms"]); Mg = float(r["Mgas_1e7Msun"]) * 1e7; Mst = float(r["MSED_1e7Msun"]) * 1e7; Mb = Mg + Mst; M = 10 ** (11.18 + .9 * (math.log10(Mb) - 10)) if mass == "em1" else 6.35 * Mb; rg = np.geomspace(R * .02, R, 60); Mc = natM(M, rg)[0]; Ms = Mst * (rg / R) ** 1.5; Mx = retained(rg, Mc, Ms, sg)[-1]; gb = GC * Mb / R ** 2 * KM2; gO = V ** 2 / R * KM2; E.append(math.log10(gO / (law(gb, a) + GC * Mx / R ** 2 * KM2))); E0.append(math.log10(gO / law(gb, a)))
        O[f"LT|{ft}|{mass}"] = float(np.median(E)); P(f"Row 11 LT {ft} {mass}: E {np.median(E):+.3f} (law {np.median(E0):+.3f}, line 0.10), stars taken as r^1.5 in M inside R_max")
exec(src[src.index("def orbits("):src.index("K12 = {}")])
base = kick_sys(5.78e11, 4.43e10, 8., 29.2, 0.0, "x"); basec = kick_sys(6e14, 2.8e12, 60., 136., 0.0, "x"); O["kick0"] = [base, basec]; P(f"Kick v_k 0 baseline: fraction inside R, 150-200 {base:.3f}, X-COP x .1 {basec:.3f} (must be near 1)")
json.dump(O, open("dw2_second_b.json", "w"), indent=1, sort_keys=True, default=float); open("dw2_second_b.out", "w").write("\n".join(OUT) + "\n")
