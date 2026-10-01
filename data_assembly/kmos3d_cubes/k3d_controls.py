#!/usr/bin/env python3
"""Controls C1-C4 of FROZEN_CRITERIA_2026-09-30.md against the final fit tables. Pass lines are those of the frozen file; nothing here moves them."""
import pandas as pd, numpy as np, json
main = pd.read_csv("k3d_fits_main_final.csv"); alt = pd.read_csv("k3d_fits_alt_final.csv")
ok = main[main.status == "ok"].set_index("ID"); oka = alt[alt.status == "ok"].set_index("ID")
res = {}
# C1: five galaxies shared with SINS AO (position within 1 arcsec and equal redshift), published SINS V_rot (Table 6)
pairs = {"K20-ID6": "GS4_33639", "K20-ID7": "GS4_29868", "GMASS-2303": "GS4_40218", "GMASS-2363": "GS4_42930", "ZC410041": "COS4_08515"}
t6 = pd.read_csv("../highz_literature_tables/sins_ao/sins_ao_table6_kinematics.csv").set_index("source")
rows = []
for s, k in pairs.items():
    v = float(t6.loc[s, "Vrot_kms"]); m = ok.loc[k] if k in ok.index else None
    rows.append(dict(SINS=s, KMOS3D=k, SINS_Vrot=v, KMOS3D_V22=None if m is None else m.V22, eV22=None if m is None else m.eV22, ratio=None if m is None else m.V22 / v, edge=None if m is None else bool(m.edge), quality=None if m is None else m.quality))
c1 = pd.DataFrame(rows); c1.to_csv("k3d_C1_sins_overlap.csv", index=False)
n_ok = int(((c1.ratio > 0.7) & (c1.ratio < 1.3)).sum()); res["C1"] = dict(within30=n_ok, n=int(c1.ratio.notna().sum()), PASS=bool(n_ok >= 4))
# C2/C2b from the injection tables
for sc in ("base", "flat", "slow"):
    d = pd.read_csv(f"k3d_injection_{sc}.csv"); res["C2_" + sc] = dict(n=len(d), median_ratio=float(d.ratio.median()), rms_ratio=float(d.ratio.std()), edge_fraction=float(d.edge.mean()))
res["C2"] = dict(PASS=bool(0.9 <= res["C2_base"]["median_ratio"] <= 1.1 and res["C2_base"]["rms_ratio"] < 0.2), n=res["C2_base"]["n"])
res["C2b"] = dict(PASS=bool(abs(res["C2_flat"]["median_ratio"] - 1) <= 0.2 and abs(res["C2_slow"]["median_ratio"] - 1) <= 0.2))
# C3 stability among highSN galaxies fitted in both runs
both = ok.join(oka[["V22", "Va", "rt"]], rsuffix="_alt", how="inner"); hs = both[both.quality == "highSN"]
frac = float((np.abs(hs.V22_alt / hs.V22 - 1) > 0.2).mean()); res["C3"] = dict(n_highSN=len(hs), fraction_changed_over_20pct=frac, PASS=bool(frac < 0.2))
# C4: integrated model sigma against the catalogue aperture HAFIT_SIG (descriptive)
d4 = ok[np.isfinite(ok.catalog_HAFIT_SIG) & (ok.catalog_HAFIT_SIG > 0)]; res["C4"] = dict(n=len(d4), within25=float((np.abs(d4.sig_int / d4.catalog_HAFIT_SIG - 1) < 0.25).mean()))
# diagnostics
res["diagnostics"] = dict(n_ok=len(ok), highSN=int((ok.quality == "highSN").sum()), edge=int(ok.edge.sum()), badchi=int(ok.badchi.sum()),
                          rt_at_lower_bound=int((ok.rt <= 0.0205).sum()), Va_at_upper_bound=int((ok.Va >= 799).sum()), notes_nonempty=int(ok.notes.fillna("").ne("").sum()))
res["stage_verdict"] = "VALIDATED" if (res["C1"]["PASS"] and res["C2"]["PASS"] and res["C2b"]["PASS"]) else "NOT VALIDATED"
json.dump(res, open("k3d_control_results.json", "w"), indent=1); print(json.dumps(res, indent=1)); print(c1.round(2).to_string())
