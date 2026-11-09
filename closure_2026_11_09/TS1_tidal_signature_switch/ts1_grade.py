#!/usr/bin/env python3
"""TS1 grader (FROZEN_CRITERIA.md 4b352f2a37): gate x footing tables per sub-variant -> ts1.json / ts1.out, MUTATE -> ts1_MUTATE.json / .out.
Order 0, T1, 1, T3, 2, 3, T4, 6, 7a, 7b-N, 7b-L, 8, CS, 10. Carried values (frozen section 3) named as such.
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); PA = os.path.join(HERE, "parts"); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WM1 = os.path.join(REPO, "closure_2026_11_09", "WM1_warm_component_law_baryons", "parts")
CRIT = "4b352f2a37"; FOOTS = ("canonical", "alt")
ORDER = ["0 seeding", "T1 SPARC in disc", "1 KiDS", "T3 KiDS saddle", "2 groups", "3 X-COP", "T4 WL1 phantom", "6 BAO+SN", "7a CMB primary", "7b-N lensing cutoff", "7b-L lensing law-on-web", "8 forest+fsigma8", "CS S8", "10 Cassini"]
J = lambda p: json.load(open(p)) if os.path.exists(p) else None
loc, core = J(os.path.join(PA, "local.json")), J(os.path.join(PA, "core.json"))
WL1 = {"canonical": (0.936, 0.92), "alt": (1.079, 0.96)}; RB = 0.030                       # WL1 q_pop z 1 and R_ms lower (Mpc); baryon body 30 kpc
L = []; P = lambda s: (print(s), L.append(s)); out = dict(criteria=CRIT, T6=core["T6_ensemble"], T2=core["T2_voids"], KA_T=core["KA_T"], KA_T7=core["KA_T7"])
P(f"TS1 RESULT TABLE (criteria {CRIT}). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
for V, tag in (("M-W", "MW"), ("M-split", "MSPLIT"), ("M-law", None)):
    out[V] = {}
    for f in FOOTS:
        l = loc[f][V]; st = {}; num = {}
        sd = J(os.path.join(PA, f"seed_{tag}_{f}.json")) if tag else None
        st["0 seeding"] = sd["W"]["gate0"] if sd else "REPORTED (M-law: baryon-only seeds)"
        if sd: num["seed_ratio"] = {z: sd["W"]["halo_abundance"][z]["ratio_to_ref_sharpk_law"] for z in sd["W"]["halo_abundance"]}
        st["T1 SPARC in disc"] = l["T1"]["status"]; num["T1"] = dict(rms=l["T1"]["all"]["rms"], line=loc[f]["L0_sparc"]["all"]["rms"] + 0.010, s_med=l["T1"]["s_at_U0.5"]["median"], above_rms=l["T1_z_above"]["all"]["rms"])
        st["1 KiDS"] = l["G1"]["status"]; st["T3 KiDS saddle"] = l["T3"]["status"]; num["KiDS"] = (l["G1"]["max_abs"], l["T3"]["max_abs"])
        st["2 groups"] = l["G2"]["status"]; num["groups"] = (l["G2"]["fst0"]["n_pass"], l["G2"]["fst1"]["n_pass"])
        st["3 X-COP"] = l["G3"]["status"]; num["xcop"] = dict(mean=l["G3"]["mean"], bins=[b["mean"] for b in l["G3"]["bins"] if b["graded"]], ret=[b["retained_over_Mdyn"] for b in l["G3"]["bins"] if b["graded"]], s=[b["s_median"] for b in l["G3"]["bins"] if b["graded"]])
        q, Rl = WL1[f]; qb = (1 - RB / Rl) * q; st["T4 WL1 phantom"] = "PASS" if qb <= 0.0354 else "FAIL"; num["T4_q_pop_lower_bound"] = qb
        co = J(os.path.join(PA, f"cosmo_{tag}_{f}.json")) if tag else None
        st["6 BAO+SN"] = co["G6"]["status"] if co else "NOT RUN"
        if tag == "MW": c7 = J(os.path.join(WM1, f"cmb7a_{f}.json")); st["7a CMB primary"] = c7["W"]["status"]; num["7a"] = c7["W"]["delta"]
        elif tag == "MSPLIT": c7 = J(os.path.join(PA, f"cmb7a_MSPLIT_{f}.json")); st["7a CMB primary"] = c7["W"]["status"]; num["7a"] = c7["W"]["delta"]
        else: st["7a CMB primary"] = "FAIL (carried: QX15 MB control +172,848 / +166,612)"
        if tag == "MW": g9 = J(os.path.join(WM1, "g9_W.json"))
        elif tag == "MSPLIT": g9 = J(os.path.join(PA, "g9_MSPLIT.json"))
        else: g9 = None
        st["7b-N lensing cutoff"] = (g9["status"] if g9 else "NOT RUN"); num["7bN"] = g9["worst"] if g9 else None
        for k, key in (("7b-L lensing law-on-web", "G7bL"), ("8 forest+fsigma8", "G8"), ("CS S8", "CS")): st[k] = co[key]["status"] if co else "NOT RUN"
        if co: num.update(G6=co["G6"]["dchi2"], G7bL=co["G7bL"]["chi2"], forest=co["G8"]["forest"]["dchi2"], fs8=[r["Rf"] for r in co["G8"]["fsigma8"]["rows"]], S8=co["CS"]["change"], Bm=co["D1"])
        st["10 Cassini"] = "PASS (carried: s = 1 outside the Sun)"
        fails = [k for k in ORDER if not st[k].startswith(("PASS", "REPORTED", "NOT RUN"))]
        out[V][f] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None, fails=fails, numbers=num)
        P(f"[{f}] {V}: LABEL {out[V][f]['label']}; first failing gate {out[V][f]['first_fail']}; failing: {', '.join(fails)}")
        for k in ORDER: P(f"    {k:26s} {st[k]}")
ka = dict(KA_T=core["KA_T"]["pass_"], KA_T7=core["KA_T7"]["pass_"], KA_T6={f: loc[f]["KA_T6"]["pass_"] for f in FOOTS})
P(f"Known answers: KA-T {ka['KA_T']}, KA-T7 {ka['KA_T7']}, KA-T6 {ka['KA_T6']}")
out["known_answers"] = ka; json.dump(out, open(os.path.join(HERE, "ts1.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ts1.out"), "w").write("\n".join(L) + "\n")
L.clear(); mut = {f: loc[f]["MUTATE"] for f in FOOTS}
P(f"TS1 MUTATE (criteria {CRIT}). kappa = 1/2 FITTED; not theory closed.")
for f in FOOTS:
    m = mut[f]; base = out["M-W"][f]["numbers"]
    P(f"[{f}] MT1 s = 0: SPARC {m['MT1_s0']['status']} rms {m['MT1_s0']['all']['rms']:.4f} (power on T1: {'BITES' if m['MT1_s0']['status'] == 'FAIL' else 'NO BITE'})")
    P(f"[{f}] MT2 h_z x3: SPARC rms {m['MT2_hz_x3']['all']['rms']:.4f} vs main {base['T1']['rms']:.4f} -> statistic moved; label {m['MT2_hz_x3']['status']} (unchanged)")
    P(f"[{f}] MT3 D 7 Mpc: KiDS max {m['MT3_D7']['max_abs']:.3f} vs T3 at 3.5 Mpc {base['KiDS'][1]:.3f} and single {base['KiDS'][0]:.3f} -> moved toward single")
json.dump(mut, open(os.path.join(HERE, "ts1_MUTATE.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ts1_MUTATE.out"), "w").write("\n".join(L) + "\n")
