"""EFN1 labels (criteria 98364c8d20; amendments A1 c3e466efbf, A2 a55fd19bd0, A3 94c54483a9, A4 04278f7abe), read off the
route-D, route-W and sympy outputs.  Readings, in the record's order: frozen (plane rows dynamic; a(t); 14 e-folds; only the
two backgrounds of the 'frozen' batch), A1 (plane rows static; a(t); 14 e-folds), A2-A4 (the last reading: c(t); 30
e-folds; KA-c as A4).  Writes efn1_labels.json / .out.
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import efn1_core as C

FOOTER = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
OUT = []
def P_(s=""):
    print(s, flush=True); OUT.append(str(s))
def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None

SYM = load("efn1_sympy.json"); W = load("efn1_route_w.json"); WM = load("efn1_route_w_MUTATE.json")
DM = load("efn1_route_d_main.json"); DK = load("efn1_route_d_ka.json"); DB = load("efn1_route_d_kab2.json")
DX = load("efn1_route_d_MUTATE.json"); DE = load("efn1_route_d_ext.json"); DF = load("efn1_route_d_frozen.json")
RES = dict(lane="EFN1", script="efn1_labels.py", readings={})


def key(name, foot, kind, lm, ge, res):
    return f"{name}_{foot}_{kind}_{lm}_{ge}_{res}".replace(".", "p")


def outcome_A2(r):
    """per grid, A2 rule: (label, detail)."""
    if r is None:
        return "MISSING", {}
    e = r["snaps"]["end"]
    if r["stop"]:
        return "LEAVES", dict(stop=r["stop"], tF=r["tF_efolds"], at=e["c_at"])
    if e["c"] >= 1 and (r["rate_last3"] or 0) >= 0.3:
        return "LEAVES", dict(stop="unbounded", tF=None, at=e["c_at"])
    if r["c_last3_maxmin"] <= 1.5 and (r["rate_last3"] is not None and r["rate_last3"] <= 0.1):
        big = max(v[0] for k_, v in e["dg"].items() if float(k_) >= 0.75)
        return ("SATURATES" if big <= 0.10 else "RESHAPES"), dict(c_end=e["c"], dg_max=big)
    return "UNRESOLVED", dict(c_end=e["c"], rate_last3=r["rate_last3"])


def outcome_frozen_a(r):
    """frozen / A1 rule on a(t) and 14 e-folds."""
    if r is None:
        return "MISSING", {}
    fr = r["frozen_reading"]
    if fr["a_reaches_10_before_14"]:
        h = r["hist"]; t = np.array(h["tG"]); a = np.array(h["a"])
        i = int(np.argmax(a >= 10)); return "LEAVES", dict(stop="F1 (a >= 10)", tF=float(t[i]), at=[h["a_r_re"][i], h["a_th"][i]])
    if r["stop"] and r["tF_efolds"] <= 14:
        return "LEAVES", dict(stop=r["stop"], tF=r["tF_efolds"])
    if fr["a_at_14"] >= 1 and (fr["a_rate_last3_to14"] or 0) >= 0.3:
        return "LEAVES", dict(stop="unbounded (a)", tF=None)
    return "UNRESOLVED", dict(a_14=fr["a_at_14"], rate=fr["a_rate_last3_to14"])


def combine(l3, d3, l4, d4):
    if "MISSING" in (l3, l4):
        return "NO VERDICT", "a grid missing"
    if l3 != l4:
        return "NO VERDICT", f"R3 {l3} vs R4 {l4}"
    if l3 == "LEAVES":
        s3, s4 = d3.get("stop", ""), d4.get("stop", "")
        if s3.split()[0] != s4.split()[0]:
            return "NO VERDICT", f"stop lines differ ({s3} / {s4})"
        if d3.get("tF") is not None and d4.get("tF") is not None and abs(d3["tF"] - d4["tF"]) > 0.5:
            return "NO VERDICT", f"t_F differs by {abs(d3['tF'] - d4['tF']):.2f} e-folds"
        return "LEAVES THE STATIC BRANCH", ""
    if l3 == "UNRESOLVED":
        return "NO VERDICT", "not resolved by t_end"
    return l3, ""


def footing_label(labels):
    if any(l_ == "NO VERDICT" for l_ in labels):
        return "NO VERDICT"
    s = set(labels)
    if len(s) == 1:
        return labels[0]
    return "MIXED " + json.dumps({x: labels.count(x) for x in s})


# ---------------------------------------------------------------- known answers
KA = {}
KA["a"] = bool(SYM and SYM.get("KA_a_pass") and SYM.get("dimension") == 3)
P_(f"KA-a sympy (3-D): {'PASS' if KA['a'] else 'FAIL / not run'}")
b1 = {}
if W:
    for foot, lst in C.GRADED.items():
        for kind, lm in lst:
            for res in (3, 4):
                row = W["rows"].get(f"{foot}_{kind}_{lm}_R{res}")
                if row:
                    b1[f"{foot}_{kind}_{lm}_R{res}"] = dict(ratio=row.get("Gamma_over_Gref"), pass_=row.get("KAb1_pass"))
P_("KA-b1 route W Gamma / SCS3 converged Gamma (R3, R4 where run): " + json.dumps({k_: [round(v["ratio"], 4) if v["ratio"] else None, v["pass_"]] for k_, v in b1.items()}))
b2 = {}
if DB:
    for k_, r in DB["runs"].items():
        h = r["hist"]; t = np.array(h["tG"]); c = np.array(h["c"])
        m = t >= 1.0
        rate = float(np.polyfit(t[m], np.log(c[m]), 1)[0]) if m.sum() > 3 else None
        foot, kind, lm = r["spec"]["foot"], r["spec"]["kind"], r["spec"]["logm"]
        gw = W["rows"][f"{foot}_{kind}_{lm}_R3"]["Gamma_over_Gref"]
        b2[k_] = dict(rate=rate, gamma_w=gw, rel=abs(rate / gw - 1) if rate else None, pass_=bool(rate and abs(rate / gw - 1) <= 0.02))
P_("KA-b2 linear eigen-seeded growth / route W Gamma (2 %): " + json.dumps({k_: [round(v["rel"], 5) if v["rel"] is not None else None, v["pass_"]] for k_, v in b2.items()}))
b3 = {}
if DM:
    for k_, r in DM["runs"].items():
        if r["spec"]["name"] == "primary" and r["spec"]["res"] in (3, 4):
            re_ = r["rate_early"]
            b3[k_] = dict(rate=re_, pass_=bool(re_ is not None and 0.5 <= re_ <= 1.10))
P_("KA-b3 early fitted rate of c (Gamma_ref) in [0.5, 1.10]: " + json.dumps({k_: [round(v["rate"], 3) if v["rate"] else None, v["pass_"]] for k_, v in b3.items()}))
kc = {}; kd = {}
if DK:
    for k_, r in DK["runs"].items():
        h = r["hist"]; t = np.array(h["tG"]); c = np.array(h["c"])
        nm = r["spec"]["name"]
        if nm == "KAc_isolated":
            m = t >= 2.0
            rate = float(np.polyfit(t[m], np.log(np.maximum(c[m], 1e-300)), 1)[0])
            kc[k_] = dict(rate=rate, cmax=float(c.max()), c0=float(c[0]), frozen_pass=bool(c.max() <= 2 * c[0]),
                          A4_pass=bool(rate <= 0.1 and c.max() <= 0.1), stop=r["stop"])
        elif nm == "KAd_pert_noseed":
            kd[k_] = dict(c_max=float(c.max()), pass_=bool(c.max() == 0.0))
        elif nm == "KAd_full_noseed":
            foot, kind, lm = r["spec"]["foot"], r["spec"]["kind"], r["spec"]["logm"]
            prim = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 3)) if DM else None
            if prim:
                tp = np.array(prim["hist"]["tG"]); cp = np.array(prim["hist"]["c"])
                tmax = tp[-1]
                ci = np.interp(tp, t, c)
                ok = bool(np.all(ci[tp <= min(tmax, t[-1])] <= 0.1 * cp[tp <= min(tmax, t[-1])] + 1e-300))
                kd[k_] = dict(c_max_to_tF=float(ci.max()), worst_ratio=float(np.max(ci / np.maximum(cp, 1e-300))), pass_=ok)
    if W:
        for k_, row in W["rows"].items():
            if row.get("isolated"):
                kc[k_] = dict(lam_over_Gref2=row["lam_over_Gref2"], pass_=row["KAc_pass"])
P_("KA-c isolated twins: " + json.dumps(kc))
P_("KA-d no seed: " + json.dumps(kd))
ke = {}
if DM:
    for foot, lst in C.GRADED.items():
        for kind, lm in lst:
            p3 = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 3)); h3 = DM["runs"].get(key("dthalf", foot, kind, lm, 0.1, 3))
            if p3 and h3:
                if p3["stop"] and h3["stop"]:
                    d = abs(p3["tF_efolds"] - h3["tF_efolds"]); ke[f"{foot}_{kind}_{lm}"] = dict(dtF=d, pass_=bool(d <= 0.1))
                elif not p3["stop"] and not h3["stop"]:
                    d = abs(p3["snaps"]["end"]["c"] / h3["snaps"]["end"]["c"] - 1); ke[f"{foot}_{kind}_{lm}"] = dict(dc=d, pass_=bool(d <= 0.05))
                else:
                    ke[f"{foot}_{kind}_{lm}"] = dict(pass_=False, note="stop line on one dt only")
P_("KA-e dt halving on R3: " + json.dumps(ke))

# ---------------------------------------------------------------- labels
for reading in ("A1 (a, 14 e-folds)", "A2-A4 (c, 30 e-folds)"):
    P_(f"================ reading: {reading}")
    lab = {}
    for foot, lst in C.GRADED.items():
        L = []
        for kind, lm in lst:
            r3 = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 3)) if DM else None
            r4 = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 4)) if DM else None
            r2 = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 2)) if DM else None
            fn = outcome_frozen_a if reading.startswith("A1") else outcome_A2
            l3, d3 = fn(r3); l4, d4 = fn(r4); l2, d2 = fn(r2)
            lb, why = combine(l3, d3, l4, d4)
            fails = []
            if not KA["a"]: fails.append("KA-a")
            k3 = f"{foot}_{kind}_{lm}_R3"
            if b1.get(k3) and not b1[k3]["pass_"]: fails.append("KA-b1")
            if reading.startswith("A2"):
                for rr in (3, 4):
                    kk = key("primary", foot, kind, lm, 0.1, rr)
                    if kk in b3 and not b3[kk]["pass_"]: fails.append(f"KA-b3 R{rr}")
                kk = f"{foot}_{kind}_{lm}"
                if kk in ke and not ke[kk]["pass_"]: fails.append("KA-e dt")
                for k_, v in list(kc.items()) + list(kd.items()) + list(b2.items()):
                    if f"_{foot}_{kind}_{lm.replace('.', 'p')}_" in k_ and not (v.get("pass_", v.get("A4_pass", True)) if "A4_pass" not in v else v["A4_pass"]):
                        fails.append(f"KA ({k_})")
            if fails:
                lb, why = "NO VERDICT", "known answer fails: " + ", ".join(fails) + (f" (rule alone: {lb})" if lb != "NO VERDICT" else "")
            L.append(lb)
            lab[f"{foot}_{kind}_{lm}"] = dict(label=lb, why=why, R2=[l2, d2], R3=[l3, d3], R4=[l4, d4])
            P_(f"   {foot} {kind} {lm}: {lb}  {why} | R2 {l2} {d2} | R3 {l3} {d3} | R4 {l4} {d4}")
        fl = footing_label(L)
        lab[f"FOOTING_{foot}"] = fl
        P_(f"   FOOTING {foot}: {fl}")
    RES["readings"][reading] = lab

# frozen reading (plane rows dynamic) on its two backgrounds
if DF:
    P_("================ reading: frozen (plane rows dynamic; a, 14 e-folds), two backgrounds")
    for foot in ("canonical", "alt"):
        r3 = DF["runs"].get(key("frozen_sheet_dynamic", foot, "expo", "9.4", 0.1, 3)); r4 = DF["runs"].get(key("frozen_sheet_dynamic", foot, "expo", "9.4", 0.1, 4))
        l3, d3 = outcome_frozen_a(r3); l4, d4 = outcome_frozen_a(r4)
        lb, why = combine(l3, d3, l4, d4)
        P_(f"   {foot} expo 9.4: {lb} {why} | R3 {l3} {d3} | R4 {l4} {d4}")
        RES["readings"].setdefault("frozen", {})[foot] = dict(label=lb, R3=[l3, d3], R4=[l4, d4])

# ---------------------------------------------------------------- route W convergence and readings
if W:
    P_("================ route W (A3): Gamma, c2, c3 on R2 -> R3 (-> R4)")
    RW = {}
    for foot, lst in C.GRADED.items():
        for kind, lm in lst:
            rows = {rr: W["rows"].get(f"{foot}_{kind}_{lm}_R{rr}") for rr in (2, 3, 4)}
            have = [rr for rr in (2, 3, 4) if rows[rr] and "c2_over_G" in rows[rr]]
            if len(have) < 2:
                RW[f"{foot}_{kind}_{lm}"] = "NO VERDICT (fewer than two grids)"; continue
            a_, b_ = rows[have[-2]], rows[have[-1]]
            ch = {q: abs(b_[q] / a_[q] - 1) if a_[q] else None for q in ("Gamma_over_Gref", "c2_over_G", "c3_over_G")}
            conv = all(v is not None and v <= 0.2 for v in ch.values())
            rd = b_["wn_reading_if_converged"] if conv else "NO VERDICT"
            RW[f"{foot}_{kind}_{lm}"] = dict(reading=rd, changes=ch, finest=have[-1], c2=[rows[h]["c2_over_G"] for h in have],
                                            c3=[rows[h]["c3_over_G"] for h in have], peak=[rows[h]["mode_peak"] for h in have],
                                            cells_half=[rows[h]["mode_cells_above_half_peak"] for h in have])
            P_(f"   {foot} {kind} {lm}: {rd}; relative changes {json.dumps({k_: round(v, 3) if v is not None else None for k_, v in ch.items()})}; "
               f"c2/Gamma {[round(x, 4) for x in RW[f'{foot}_{kind}_{lm}']['c2']]}; c3/Gamma {[round(x, 4) for x in RW[f'{foot}_{kind}_{lm}']['c3']]}; "
               f"mode peak {RW[f'{foot}_{kind}_{lm}']['peak']}; cells above half peak {RW[f'{foot}_{kind}_{lm}']['cells_half']}")
    RES["route_W"] = RW
    if WM:
        P_("M4 (s-map second derivative flipped): " + json.dumps({k_: [round(v["c2_true_over_G"], 4), round(v["c2_over_G"], 4), v["bites"]] for k_, v in WM["rows"].items()}))

# ---------------------------------------------------------------- MUTATE
if DX and DM:
    P_("================ MUTATE (R3)")
    MU = {}
    for foot, kind, lm in C.MUT_SET:
        p = DM["runs"].get(key("primary", foot, kind, lm, 0.1, 3))
        lp, dp_ = outcome_A2(p)
        for nm in ("M1_eps1e-3", "M2_signflip", "M3_linear", "M2b_seedsign"):
            m = DX["runs"].get(key(nm, foot, kind, lm, 0.1, 3))
            if not m: continue
            lm_, dm_ = outcome_A2(m)
            if nm.startswith("M1"):
                if lp == "LEAVES" and lm_ == "LEAVES" and dp_.get("tF") and dm_.get("tF"):
                    shift = dp_["tF"] - dm_["tF"]; bites = bool(abs(shift - math.log(10) / (p["rate_early"] or 1)) <= 0.5 or abs(shift - math.log(10)) <= 0.5)
                    det = dict(shift_efolds=shift, expected_ln10=math.log(10), expected_ln10_over_rate=math.log(10) / (p["rate_early"] or 1))
                else:
                    bites = bool(lp == lm_); det = {}
            elif nm.startswith("M3"):
                bites = bool(m["stop"] is None and lp == "LEAVES"); det = dict(c_end=m["snaps"]["end"]["c"])
            else:
                same_stop = (m["stop"] or "")[:2] == (p["stop"] or "")[:2]
                dt_ = abs((m["tF_efolds"] or 99) - (p["tF_efolds"] or 99))
                loc = math.hypot(m["snaps"]["end"]["c_at"][0] - p["snaps"]["end"]["c_at"][0], 0)
                bites = bool((not same_stop) or dt_ > 0.5 or loc > 0.2); det = dict(dtF=dt_, dloc_re=loc)
            MU[f"{nm}_{foot}_{kind}_{lm}"] = dict(primary=[lp, dp_], mutant=[lm_, dm_], bites=bites, **det)
            P_(f"   {nm} {foot} {kind} {lm}: primary {lp} {dp_} | mutant {lm_} {dm_} | bites {bites} {det}")
    RES["mutate"] = MU

if DE:
    P_("================ extension 0.01 a0 (reported beside, A2-A4 rule)")
    for foot in ("canonical", "alt"):
        r3 = DE["runs"].get(key("ext_0p01", foot, "expo", "9.4", 0.01, 3)); r4 = DE["runs"].get(key("ext_0p01", foot, "expo", "9.4", 0.01, 4))
        l3, d3 = outcome_A2(r3); l4, d4 = outcome_A2(r4)
        lb, why = combine(l3, d3, l4, d4)
        P_(f"   {foot} expo 9.4 at 0.01 a0: {lb} {why} | R3 {l3} {d3} | R4 {l4} {d4}")

RES["known_answers"] = dict(a=KA["a"], b1=b1, b2=b2, b3=b3, c=kc, d=kd, e=ke)
RES["footer"] = FOOTER
json.dump(RES, open(os.path.join(HERE, "efn1_labels.json"), "w"), indent=1, default=str)
P_(FOOTER)
open(os.path.join(HERE, "efn1_labels.out"), "w").write("\n".join(OUT) + "\n")
