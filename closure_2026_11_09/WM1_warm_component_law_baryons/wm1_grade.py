#!/usr/bin/env python3
"""WM1 grader (FROZEN_CRITERIA.md 6e40130dfa, AMENDMENT_A1 5cba17a249): assembles the gate x footing table from parts/ for the main
relic (W) -> wm1.json / wm1.out, and the MUTATE runs (MW1 M_hm x 10, MW2 / 10, MN baryons Newtonian) plus brackets (W3, Wthird, Racc,
reported) -> wm1_MUTATE.json / wm1_MUTATE.out. Label order 1, 2, 3, 5, 5b, 6, 7a, 7b-N, 7b-L, 8, CS, 9, 10.
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts")
CRIT = "6e40130dfa"; A1 = "5cba17a249"; A2 = "c830b470e0"; FOOTS = ("canonical", "alt")
ORDER = ["0 seeding", "1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "5b UMa", "6 BAO+SN", "7a CMB primary", "7b-N lensing cutoff", "7b-L lensing law-on-web", "8 forest+fsigma8", "CS S8", "9 Bullet", "10 Cassini"]
def J(n):
    p = os.path.join(PA, n); return json.load(open(p)) if os.path.exists(p) else None
def table(V, local_only=False):
    loc, uma, bul, g9 = J(f"local_V{V}.json"), J(f"uma_V{V}.json"), J(f"vbullet_{V}.json"), J(f"g9_{V}.json")
    out = {}
    for f in FOOTS:
        s = loc[f]["sets"]["primary_SIS"]; co = J(f"cosmo_{V}_{f}.json"); cm = J(f"cmb7a_{f}.json")
        sd = J(f"seed_{f}.json"); st = {"0 seeding": (sd[V]["gate0"] if (sd and V in sd) else "NOT RUN"), "1 KiDS": s["G1"]["status"], "2 groups": s["G2"]["status"], "3 X-COP": s["G3"]["status"], "5 SPARC": s["G5"]["status"], "5b UMa": uma[f]["status"],
              "6 BAO+SN": co["G6"]["status"] if co else "MISSING", "7a CMB primary": (cm[V]["status"] if (cm and V in cm) else "MISSING"),
              "7b-N lensing cutoff": g9["status"] if g9 else "MISSING", "7b-L lensing law-on-web": co["G7bL"]["status"] if co else "MISSING",
              "8 forest+fsigma8": co["G8"]["status"] if co else "MISSING", "CS S8": co["CS"]["status"] if co else "MISSING",
              "9 Bullet": bul[f]["status"] if bul else "MISSING", "10 Cassini": s["G10"]["status"]}
        if local_only: st = {k: v for k, v in st.items() if k in ("0 seeding", "1 KiDS", "2 groups", "3 X-COP", "5 SPARC", "5b UMa", "10 Cassini", "9 Bullet")}
        fails = [k for k in ORDER if k in st and st[k] not in ("PASS", "NOT RUN")]
        num = dict(KiDS_max=s["G1"]["max_abs_shift"], KiDS_n_over=s["G1"]["n_fail"], groups=[s["G2"]["fst0"]["n_pass"], s["G2"]["fst1"]["n_pass"]], groups_median=[s["G2"]["fst0"]["median_res"], s["G2"]["fst1"]["median_res"]],
                   xcop_mean=s["G3"]["mean"], xcop_rms=s["G3"]["rms"], xcop_bins=[b["mean"] for b in s["G3"]["bins"]], xcop_retained_over_Mdyn=[b["retained_over_Mdyn_median"] for b in s["G3"]["bins"]],
                   TR1=[b["TR1_D_canonical"] for b in s["G3"]["bins"]], TR1_shape=s["G3"]["TR1_shape_reported"], UDG_reported=dict(mean=s["G4"]["mean"], z=s["G4"]["z"], law_only=s["G4"]["law_only_mean"]),
                   SPARC=s["G5"].get("rms"), uma=uma[f]["Delta_pred"])
        if co: num.update(G6=co["G6"]["dchi2"], G7bL=co["G7bL"]["chi2"], S_B=co["G7bL"]["S_B"], forest=co["G8"]["forest"]["dchi2"], forest_baryon=co["G8"]["forest_baryon_tracer_reported"]["dchi2"],
                          fsigma8=[r["Rf"] for r in co["G8"]["fsigma8"]["rows"]], S8_change=co["CS"]["change"], sigma8_ratio=co["CS"]["sigma8_ratio"], P_ratio=co["CS"]["P_ratio"],
                          newton_warm=dict(forest=co["G8"]["newton_warm_reported"]["forest"]["dchi2"], fsigma8=[r["Rf"] for r in co["G8"]["newton_warm_reported"]["fsigma8"]["rows"]],
                                           S8_change=co["CS"]["newton_warm_reported"]["change"], P_ratio=co["CS"]["newton_warm_reported"]["P_ratio"], lensing_footing_point=co["G7bL"]["newton_warm_chi2_footing_point"]),
                          D1=co["D1"], relic=co["relic"])
        if cm and V in cm: num.update(cmb7a_delta=cm[V]["delta"], cmb7a_cold_PA=cm["cold"]["PA"])
        if g9: num.update(g9_worst=g9["worst"], g9_best=g9["best"])
        if bul: num.update(bullet_ZM=bul[f]["row"]["ZM"], bullet_S=[x["S"] for x in bul["subclusters"][f]], bullet_gas_reported=bul[f]["gas_traced_reported"]["label"])
        out[f] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None, fails=fails, numbers=num)
    return out
L = []
def P(s=""): print(s); L.append(s)
main = table("W"); co = {f: J(f"cosmo_W_{f}.json") for f in FOOTS}
P(f"WM1 RESULT TABLE (criteria {CRIT}, A1 {A1}, A2 {A2}: gate 0 seeding graded first). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for f in FOOTS:
    t = main[f]; P(f"[{f}] LABEL {t['label']}; first failing gate {t['first_fail']}; all failing: {', '.join(t['fails'])}")
    for k in ORDER: P(f"    {k:26s} {t['status'][k]}")
ka = dict(KA_W1=J("g9_hc1.json")["KA_W1"], KA_W2={f: co[f]["KA_W2"] for f in FOOTS if co[f] and "KA_W2" in co[f]}, KA_W3={f: co[f]["KA_W3"] for f in FOOTS if co[f]},
          KA_W4={f: J("local_VW.json")[f]["KA3"]["pass_"] for f in FOOTS})
ka["KA_S"] = {f: dict(S2=J(f"seed_{f}.json")["KA_S2"]["pass_"], S1_W=J(f"seed_{f}.json")["W"]["KA_S1_pass"]) for f in FOOTS}
kok = all(v["S2"] and v["S1_W"] for v in ka["KA_S"].values()) and ka["KA_W1"]["pass_"] and all(v["pass_"] for v in ka["KA_W2"].values()) and all(v["omega_pass"] for v in ka["KA_W3"].values()) and all(ka["KA_W4"].values())
P(f"Known answers: KA-W1 {ka['KA_W1']['pass_']}; KA-W2 " + ", ".join(f"{f} {v['pass_']} ({v['max_rel_dev']:.1e})" for f, v in ka["KA_W2"].items()) + "; KA-W3 " + ", ".join(f"{f} omega {v['omega_pass']} k_hm ratio {v['k_hm_ratio']:.3f}" for f, v in ka["KA_W3"].items()) + f"; KA-W4 {ka['KA_W4']} -> {'ALL PASS' if kok else 'A KNOWN ANSWER FAILED: NO VERDICT'}")
json.dump(dict(criteria=CRIT, amendment=A1, amendment2=A2, main=main, known_answers=ka, known_answers_pass=kok, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "wm1.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wm1.out"), "w").write("\n".join(L) + "\n")
# ---------------- MUTATE and brackets
L.clear(); mut = {}
P(f"WM1 MUTATE + brackets (criteria {CRIT}). kappa = 1/2 FITTED; not theory closed.")
for V in ("MW1", "MW2", "W3", "Wthird"):
    t = table(V); mut[V] = t
    for f in FOOTS:
        moved = [k for k in ORDER if t[f]["status"][k] != main[f]["status"][k] and "NOT RUN" not in (t[f]["status"][k], main[f]["status"][k])]; t[f]["moved_vs_main"] = moved
        P(f"[{f}] {V}: label {t[f]['label']} (first {t[f]['first_fail']}); gates that moved vs W: {moved or 'none'}")
    if V.startswith("MW"):
        t["bites"] = bool(any(t[f]["moved_vs_main"] for f in FOOTS)); P(f"    {V} {'BITES' if t['bites'] else 'NO BITE'}")
racc = table("Racc", local_only=True); mut["Racc"] = racc
for f in FOOTS: P(f"[{f}] Racc (S = 1, reported): local/Bullet " + ", ".join(f"{k} {v}" for k, v in racc[f]["status"].items()) + f"; KiDS max {racc[f]['numbers']['KiDS_max']:.3f}")
mn = {f: co[f]["MN"] for f in FOOTS if co[f]}; mut["MN"] = mn
for f, v in mn.items(): P(f"[{f}] MN0 cold limit pipeline {'PASS' if v['MN0_cold_limit']['pass_'] else 'FAIL'}; MN-W forest dchi2 {v['MNW_forest']['dchi2']:.4g} -> {'FAILS (gate has power)' if v['MNW_forest_fails'] else 'PASSES (NO POWER)'}")
json.dump(dict(criteria=CRIT, amendment=A1, mutate=mut, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "wm1_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wm1_MUTATE.out"), "w").write("\n".join(L) + "\n")
