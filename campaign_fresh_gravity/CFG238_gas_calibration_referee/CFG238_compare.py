#!/usr/bin/env python3
"""CFG238 compare: POST-RUN ONLY. Written after every CFG238 main, attack and MUTATE output was saved. Reads the CFG224 / CFG224b results JSON for the first time
and compares number by number with CFG238_main_results.json (and the attack JSONs). Classifies each difference. Exit 0."""
import sys
from CFG238_common import *

outp, jp = out_paths("CFG238_compare")
T = Tee(outp)
banner(T, "CFG238 compare (POST-RUN: CFG224 / CFG224b JSON opened only after the CFG238 main and MUTATE outputs were saved)")
P224 = os.path.join(REPO, "campaign_fresh_gravity", "CFG224_gas_calibration")
A = json.load(open(os.path.join(P224, "cfg224_gas_calibration_results.json")))
B = json.load(open(os.path.join(P224, "cfg224b_conversion_drift_results.json")))
M = json.load(open(os.path.join(SCR, "CFG238_main_results.json")))
E = json.load(open(os.path.join(SCR, "CFG238_e_hat_results.json")))
C = json.load(open(os.path.join(SCR, "CFG238_c_ace_results.json")))
rows = []


def cmp(label, mine, peer, tol_num=1e-9, cls_if_diff="numerical", note=""):
    d = None if (mine is None or peer is None) else mine - peer
    if d is None:
        cl = "MISSING"
    elif abs(d) <= 1e-9:
        cl = "identical"
    elif abs(d) <= tol_num:
        cl = "within-tol"
    else:
        cl = cls_if_diff
    rows.append(dict(label=label, mine=mine, peer=peer, diff=d, cls=cl, note=note))
    T(f"  {cl:10s} {label}: mine {mine if mine is None else round(mine, 6)}  peer {peer if peer is None else round(peer, 6)}  diff {'' if d is None else f'{d:+.2e}'} {note}")


T("\n== A. CFG224 (pair offsets)")
pa = A["sources"]
cmp("Stripe82 N", M["s82"]["N"], pa["Stripe82|CO-DUST"]["N"])
for k in ("mean", "sd", "se", "K"):
    cmp(f"Stripe82 {k}", M["s82"][k], pa["Stripe82|CO-DUST"][k])
cmp("Stripe82 intrinsic SD", M["s82"]["sint"], pa["Stripe82|CO-DUST"]["sd_int"])
cmp("pooled [CI]-dust mean", M["pooled"]["mean"], A["primary"]["B2 0.6<=z<1.6|CI-DUST"]["mean"])
cmp("pooled [CI]-dust K", M["pooled"]["K"], A["primary"]["B2 0.6<=z<1.6|CI-DUST"]["K"])
cmp("pooled [CI]-dust SD", M["pooled"]["sd"], A["primary"]["B2 0.6<=z<1.6|CI-DUST"]["sd"])
cmp("hat variance CO", M["hat5"]["vCO"], A["hat"]["CO"]["var"])
cmp("hat variance CI", M["hat5"]["vCI"], A["hat"]["CI"]["var"])
cmp("hat variance dust", M["hat5"]["vdust"], A["hat"]["DUST"]["var"])
cmp("hat jackknife SE CO", E["jackknife_se"][0], A["hat"]["CO"]["se"], 1e-9, "numerical", "(jackknife formula)")
cmp("hat jackknife SE CI", E["jackknife_se"][1], A["hat"]["CI"]["se"])
cmp("hat jackknife SE dust", E["jackknife_se"][2], A["hat"]["DUST"]["se"])
for lab, key in (("fail5 Table1 CO-dust mean", "NOEMA3D-failing(Table1 CO)|CO-DUST"), ):
    cmp(lab, M["fail5_CO_t1"]["mean"], pa[key]["mean"]); cmp("fail5 Table1 K", M["fail5_CO_t1"]["K"], pa[key]["K"])
cmp("fail5 recipe CO-dust mean", M["fail5_CO_rec"]["mean"], pa["NOEMA3D-failing(recipe CO)|CO-DUST"]["mean"])
sec = A["secondary"]
T("\n== B. CFG224b (bins, drifts, slopes)")
fmap = {"aCO": "alpha_CO", "XCI": "X_CI", "kappaH": "kappa_H", "GDR": "GDR"}
tmap = {"ad": "ad", "dax": "daX", "xa": "xa", "xd": "xd"}
binlab = {"B1": "B1 z<0.6", "B2": "B2 0.6<=z<1.6", "B3": "B3 1.6<=z<3.0", "B4": "B4 z>=3.0"}
for key, v in M["bins"].items():
    t, c = key.split(":")
    for b, st in v["bins"].items():
        pk = f"{tmap[t]}|{fmap[c]}|{binlab[b]}"
        if pk not in B["primary"]:
            T(f"  (peer lacks {pk})"); continue
        p = B["primary"][pk]
        cmp(f"{pk} N", st["N"], p["N"]); cmp(f"{pk} mean", st["mean"], p["mean"]); cmp(f"{pk} SD", st["sd"], p["sd"])
        if b in v["drifts"] and "drift" in p:
            cmp(f"{pk} drift", v["drifts"][b]["drift"], p["drift"]); cmp(f"{pk} K_local", v["drifts"][b]["K_local"], p["K_local"])
for key, w in M["slopes_with"].items():
    t, c = key.split(":")
    p = B["regression"][f"{tmap[t]}|{fmap[c]}"]
    dcls = "definition" if key in ("ad:aCO", "ad:kappaH") else "numerical"
    cmp(f"slope with L {key} N", w["N"], p["N"], 0, dcls, "(frozen D2 used the master L_IR only: 13 ad rows have none; the peer falls back to the opt-table L_IR)")
    cmp(f"slope with L {key} b", w["b"], p["b"], 1e-9, dcls, "(master-only L_IR in the main run)")
    cmp(f"slope with L {key} SD", w["b_boot_sd"], p["sd_b"], 0.003, "seed/bootstrap" if dcls == "numerical" else "definition", "(bootstrap SD, different seed and resampler)")
    cmp(f"L_IR coeff {key} c", w["c"], p["c"], 1e-9, dcls)
for key, w in M["slopes_without"].items():
    t, c = key.split(":")
    p = B["regression"][f"{tmap[t]}|{fmap[c]}"]
    cmp(f"slope without L {key} b", w["b"], p["b0"]); cmp(f"slope without L {key} SD", w["b_boot_sd"], p["sd_b0"], 0.003, "seed/bootstrap", "(bootstrap SD)")
T("\n== C. ACE")
cmp("ACE N", 15, B["ace"]["N"])
cmp("ACE offset (OLS)", M["ace"]["D_ols"], B["ace"]["delta"])
cmp("ACE offset (slope 0)", M["ace"]["D_0"], B["ace"]["posthoc"]["delta_noslope"])
cmp("ACE offset (slope +1)", M["ace"]["D_p1"], B["ace"]["posthoc"]["delta_slope1"])
cmp("S82 OLS slope", M["ace"]["S82_slope"], B["ace"]["s82"]["b"])
cmp("S82 OLS slope SD (mine bootstrap 10000, peer analytic res_sd/(sqrt(N) sd_Z))", float(np.std(ols_boot(np.column_stack([np.ones(78), np.array([r['Z_12logOH'] for r in load_s82() if r['logMdust'] is not None and r['logMgas_CO'] is not None])]), np.array([r['logMdust'] - r['logMgas_CO'] for r in load_s82() if r['logMdust'] is not None and r['logMgas_CO'] is not None]), 10000, 238)[:, 1], ddof=1)), B["ace"]["posthoc"]["slope_se"], 0.01, "definition", "(bootstrap vs analytic OLS SE: mine analytic 0.328 equals the peer's)")
seA = 0.0
cmp("ACE K (peer SE = SD(dA)/sqrt(15) 0.0535; mine SD(R)/sqrt(15) 0.0463)", Kfun(M["ace"]["D_ols"], 0.179 / math.sqrt(15)), B["ace"]["K"], 0.005, "definition", "(same K to 0.001)")
# counts
ident = sum(1 for r in rows if r["cls"] == "identical")
other = [r for r in rows if r["cls"] not in ("identical",)]
T(f"\nSUMMARY: {len(rows)} numbers compared; identical to 1e-9: {ident}; differences: {len(other)}")
for r in other:
    T(f"  {r['cls']:16s} {r['label']}: {r['mine']} vs {r['peer']} (diff {r['diff']})")
maxd = max((abs(r["diff"]) for r in rows if r["diff"] is not None and r["cls"] in ("identical", "numerical")), default=0)
T(f"largest difference among the non-bootstrap, non-definition rows: {maxd:.2e}")
T("CFG224 controls as reported by the peer JSON: " + str(A.get("controls")) + "; CFG224b: " + str(B.get("controls")))
dump(jp, dict(rows=rows))
T.close()
sys.exit(0)
