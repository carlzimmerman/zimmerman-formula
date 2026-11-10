"""SCS3 labels: reads the outputs of scs3_maps.py and scs3_route2.py (no new solve) and applies FROZEN_CRITERIA.md
(eff0ae1861) sections 3-6, first as frozen (AX R0-R3, frozen mask), then under amendment A1 (f51866c8d4: AX R0-R5, rule on
the finest three, inner mask in radius).  Writes scs3_labels.json / .out.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, glob, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCS2 = os.path.join(HERE, "..", "SCS2_static_clock_stability_discs")
RHO = 1.5
RMAXF = 10.0
GYR = 3.15576e16
T_H = 13.8
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))


# ------------------------------------------------------------------ section 3: the convergence rule
FLAT = True          # frozen rule; amendment A4 (b34295ebcd) removes the flat clause


def rule3(Q):
    """Q: values on consecutive resolutions (ratio 1.5), coarse to fine, len >= 3.  Returns a dict with the verdict."""
    Q = [float(q) for q in Q]
    def three(a, b, c):
        d1, d2 = b - a, c - b
        out = dict(d1=d1, d2=d2)
        if FLAT and abs(d1) <= 0.02 * abs(c) and abs(d2) <= 0.02 * abs(c):
            out.update(kind="flat", Qinf=c, E=max(abs(d1), abs(d2)), p=None)
        elif d1 * d2 < 0:
            out.update(kind="oscillating", Qinf=0.5 * (b + c), E=max(abs(d1), abs(d2)), p=None)
        elif d2 == 0:
            out.update(kind="flat", Qinf=c, E=abs(d1), p=None)
        elif abs(d2) < abs(d1):
            p = math.log(d1 / d2) / math.log(RHO)
            out.update(kind="monotone", p=p, Qinf=c + d2 / (RHO ** p - 1), E=1.25 * abs(d2) / (RHO ** p - 1))
        else:
            out.update(kind="growing", p=None, Qinf=None, E=None)
        return out
    fin = three(*Q[-3:])
    res = dict(values=Q, finest=fin)
    E = fin["E"]
    if len(Q) >= 4:
        prev = three(*Q[-4:-1]); res["previous"] = prev
        if fin["Qinf"] is not None and prev["Qinf"] is not None:
            E = max(E, abs(fin["Qinf"] - prev["Qinf"]))
        res["diverging"] = bool(fin["kind"] == "growing" and prev["kind"] == "growing")
    else:
        res["diverging"] = bool(fin["kind"] == "growing")
    res["Qinf"] = fin["Qinf"]; res["E"] = E
    okp = fin["p"] is None or (0.5 <= fin["p"] <= 6)
    res["converged"] = bool(fin["Qinf"] is not None and okp and E is not None and E <= 0.20 * abs(fin["Qinf"]))
    return res


def rule2(Q0, Q1, p):
    Qinf = Q1 + (Q1 - Q0) / (RHO ** p - 1)
    E = 3 * abs(Q1 - Q0) / (RHO ** p - 1)
    return dict(values=[Q0, Q1], p=p, Qinf=Qinf, E=E, converged=bool(E <= 0.25 * abs(Qinf)), diverging=False)


# ------------------------------------------------------------------ loading
def load_maps(pattern):
    rows = {}
    for f in sorted(glob.glob(os.path.join(HERE, pattern))):
        if f.endswith("_partial.json"):
            continue
        rows.update(json.load(open(f))["rows"])
    return rows


def load_r2(pattern):
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, pattern))):
        if f.endswith("_partial.json"):
            continue
        J = json.load(open(f))
        for r in J["rows"]:
            r["_file_peak_rss_GB"] = J.get("peak_rss_GB")
            # amendment A1: route 2 at R5 counts only where the block LU stayed below 4 GB peak RSS
            if r.get("res") == 5 and (J.get("peak_rss_GB") or 99) > 4.0:
                r["lambda_min"] = None; r["dropped_R5_over_4GB"] = True
        rows += J["rows"]
    return rows


def bkey(tag):
    return tag.rsplit("_R", 1)[0]


def seqs(maps, group, resl):
    """per background: {res: row}"""
    S_ = collections.defaultdict(dict)
    for t, r in maps.items():
        if r["spec"]["group"] == group and r["res"] in resl:
            S_[bkey(t)][r["res"]] = r
    return {k: v for k, v in S_.items() if all(i in v for i in resl)}


def r2_seqs(r2rows, resl, m=0):
    S_ = collections.defaultdict(dict)
    for r in r2rows:
        if (r["m"] == m or r["m"] is None) and r["res"] in resl:
            S_[bkey(r["tag"])][r["res"]] = r
    return S_


def gyr(G2):
    return 1 / (math.sqrt(G2) * GYR) if G2 and G2 > 0 else None


# ------------------------------------------------------------------ one reading (frozen or A1) of one family on one footing
def grade_family(maps, r2rows, group, foot, resl, two_grid_p=None, label=""):
    sq = {k: v for k, v in seqs(maps, group, resl).items() if f"_{foot}_" in k}
    r2s = r2_seqs(r2rows, resl)
    out = dict(backgrounds={}, n=len(sq))
    for k, v in sorted(sq.items()):
        G2 = [v[i]["routeL"]["L"]["Gamma2_max_s2"] for i in resl]
        G2t = [v[i]["routeL"]["Lt"]["Gamma2_max_s2"] for i in resl]
        rin = [v[i]["region_negative"]["r_over_re"][0] if v[i].get("region_negative") else None for i in resl]
        fr = [v[i]["map"]["frac_neg_over_pos"] for i in resl]
        b = dict(efold_gyr=[gyr(x) for x in G2], where=[(round(v[i]["routeL"]["L"]["r_over_re"], 3),
                 round(v[i]["routeL"]["L"]["theta_deg"], 1)) for i in resl], r_inner_over_re=rin, Qneg_over_Qpos=fr)
        if two_grid_p is None:
            b["GammaL2"] = rule3(G2); b["GammaLt2"] = rule3(G2t)
            if None in rin:
                b["r_inner"] = dict(converged=False, note="region empty on a grid")
            elif not FLAT:      # A4 item 2: within two radial cells of the finest grid
                fin = v[resl[-1]]
                rmin_ = 1e-4 * fin["Rd_kpc"]; rmax_ = max(1e3 * fin["Rd_kpc"], RMAXF * fin["r_e_kpc"])
                dx = math.log(rmax_ / rmin_) / fin["grid"][0]
                spread = max(abs(math.log(a / b_)) for a in rin[-3:] for b_ in rin[-3:])
                b["r_inner"] = dict(Qinf=rin[-1], E=max(rin[-3:]) - min(rin[-3:]), spread_ln=spread, two_cells_ln=2 * dx,
                                    converged=bool(spread <= 2 * dx))
            else:
                b["r_inner"] = rule3(rin)
            b["frac"] = rule3(fr)
        else:
            b["GammaL2"] = rule2(G2[0], G2[1], two_grid_p)
            b["r_inner"] = rule2(rin[0], rin[1], two_grid_p) if None not in rin else dict(converged=False)
            b["frac"] = rule2(fr[0], fr[1], two_grid_p)
        # route 2
        rr = r2s.get(k, {})
        lam = [rr[i].get("lambda_min") if i in rr else None for i in resl]
        b["route2_lambda"] = lam
        if group.startswith("PL") or group.startswith("THICK_PL"):
            negs = [rr[i].get("negative") if i in rr else None for i in resl]
            b["route2_negative_all"] = bool(all(x is True for x in negs))
            b["route2_rayleigh"] = negs
            have = [x for x in lam if x is not None]
            if len(have) == len(resl):
                b["Gamma22"] = rule2(-lam[0], -lam[1], two_grid_p) if two_grid_p else rule3([-x for x in lam])
        else:
            ran = [x for x in lam if x is not None]
            b["route2_negative_all"] = bool(len(ran) >= 3 and all(x < 0 for x in ran))
            idx = [i for i, x in zip(resl, lam) if x is not None]
            if len(ran) >= 3 and all(x < 0 for x in ran) and all(idx[j + 1] - idx[j] == 1 for j in range(len(idx) - 1)):
                b["Gamma22"] = rule3([-x for x in ran]); b["Gamma22_res"] = idx
                # KA5: route 2 against its own symbol at the same resolutions
                lt = rule3([v[i]["routeL"]["Lt"]["Gamma2_max_s2"] for i in idx])
                b["GammaLt2_same_res"] = lt
                to_s2 = (2.99792458e5 / 3.0857e16) ** 2
                if b["Gamma22"]["Qinf"] and lt["Qinf"]:
                    b["KA5_ratio"] = b["Gamma22"]["Qinf"] * to_s2 / lt["Qinf"]
        out["backgrounds"][k] = b
    # family label
    bs = list(out["backgrounds"].values())
    def unstable(b):
        ok = b["GammaL2"]["converged"] and (b["GammaL2"]["Qinf"] or 0) > 0 and b["route2_negative_all"] and b["r_inner"]["converged"]
        if not (group.startswith("PL") or group.startswith("THICK_PL")):
            ok = ok and b.get("Gamma22", {}).get("converged", False) and 0.75 <= b.get("KA5_ratio", 0) <= 1.25 * 1e9
        return bool(ok)
    for b in bs:
        b["label"] = ("UNSTABLE" if unstable(b) else
                      "UNSTABLE, RATE UNBOUNDED" if (b["GammaL2"].get("diverging") and b["route2_negative_all"]) else "NO VERDICT")
        b["KA5_pass"] = (0.75 <= b["KA5_ratio"] <= 1.25) if "KA5_ratio" in b else None
    labs = [b["label"] for b in bs]
    if bs and all(l_ == "UNSTABLE" for l_ in labs):
        lab = "UNSTABLE"
    elif bs and any(l_ == "UNSTABLE, RATE UNBOUNDED" for l_ in labs) and all(l_ != "NO VERDICT" for l_ in labs):
        lab = "UNSTABLE, RATE UNBOUNDED"
    else:
        lab = "NO VERDICT"
    out["label"] = lab
    out["counts"] = dict(collections.Counter(labs))
    out["not_converged"] = [k for k, b in out["backgrounds"].items() if b["label"] != "UNSTABLE"]
    return out


def strength_split(fam):
    sp = {}
    for ge in ("0p01", "0p1"):
        bs = {k: b for k, b in fam["backgrounds"].items() if k.endswith(f"_{ge}_z") or k.endswith(f"_{ge}_x")}
        labs = [b["label"] for b in bs.values()]
        ef = [gyr(b["GammaL2"]["Qinf"]) for b in bs.values() if b["GammaL2"].get("Qinf")]
        sp[ge] = dict(n=len(bs), counts=dict(collections.Counter(labs)),
                      label="UNSTABLE" if labs and all(l_ == "UNSTABLE" for l_ in labs) else "NO VERDICT",
                      efold_inf_gyr_range=[min(ef), max(ef)] if ef else None)
    return sp


if __name__ == "__main__":
    RESJ = {"lane": "SCS3", "script": "scs3_labels.py", "criteria": "eff0ae1861", "amendment_A1": "f51866c8d4"}
    # ---------------------------------------------------------------- KA3 / M3: the rule on known sequences
    rng = np.random.default_rng(3)
    ka3 = []
    for p in (1, 2):
        for _ in range(5):
            Qi, c = rng.uniform(0.5, 2), rng.uniform(-0.5, 0.5)
            Q = [Qi * (1 + c * (RHO ** -i) ** p) for i in range(4)]
            r = rule3(Q)
            ka3.append(dict(p=p, Qinf=Qi, Q=Q, got=r["Qinf"], rel=abs(r["Qinf"] / Qi - 1), converged=r["converged"]))
    div = rule3([(RHO ** -i) ** -1 for i in range(4)])
    ka3_pass = all(x["rel"] <= 1e-6 and x["converged"] for x in ka3) and div["diverging"] and not div["converged"]
    # M3: inverted order formula
    def rule3_inverted(Q):
        a, b_, c = Q[-3:]; d1, d2 = b_ - a, c - b_
        p = math.log(d2 / d1) / math.log(RHO)
        return c + d2 / (RHO ** p - 1)
    m3 = [abs(rule3_inverted(x["Q"]) / x["Qinf"] - 1) for x in ka3]
    m3_bites = all(e > 1e-6 for e in m3)
    RESJ["KA3"] = dict(pass_=bool(ka3_pass), rows=ka3, diverging_case=div)
    RESJ["M3"] = dict(bites=bool(m3_bites), rel_errors=m3)
    P_(f"KA3 Richardson on known sequences: {'PASS' if ka3_pass else 'FAIL'} (max rel {max(x['rel'] for x in ka3):.1e}; "
       f"h^-1 labelled diverging: {div['diverging']}); M3 inverted order: {'BITES' if m3_bites else 'does not bite'} "
       f"(min rel error {min(m3):.2e})")

    FLAT = False
    ka3_a4 = []
    for x in ka3:
        r = rule3(x["Q"]); ka3_a4.append(dict(p=x["p"], rel=abs(r["Qinf"] / x["Qinf"] - 1), converged=r["converged"]))
    div4 = rule3([(RHO ** -i) ** -1 for i in range(4)])
    ka3_a4_pass = all(x["rel"] <= 1e-6 and x["converged"] for x in ka3_a4) and div4["diverging"] and not div4["converged"]
    FLAT = True
    RESJ["KA3_A4"] = dict(pass_=bool(ka3_a4_pass), rows=ka3_a4)
    P_(f"KA3 under A4's rule (no flat clause): {'PASS' if ka3_a4_pass else 'FAIL'} (max rel {max(x['rel'] for x in ka3_a4):.1e})")
    readings = {"frozen": dict(ax="scs3_maps_AX.json", axres=(0, 1, 2, 3), r2="scs3_route2_AX_R*.json",
                               pl="scs3_maps_PL.json", r2pl="scs3_route2_PL_R*.json",
                               thax="scs3_maps_THICK_AX.json", r2thax="scs3_route2_THICK_AX_R*.json",
                               thpl="scs3_maps_THICK_PL.json", r2thpl="scs3_route2_THICK_PL_R*.json"),
                "A1": dict(ax="scs3_maps_AX_A1*.json", axres=(0, 1, 2, 3, 4, 5), r2="scs3_route2_AX_A1_R*.json",
                           pl="scs3_maps_PL_A1*.json", r2pl="scs3_route2_PL_A1_R*.json",
                           thax="scs3_maps_THICK_AX_A1*.json", r2thax="scs3_route2_THICK_AX_A1_R*.json",
                           thpl="scs3_maps_THICK_PL_A1*.json", r2thpl="scs3_route2_THICK_PL_A1_R*.json"),
                "A2": dict(ax="scs3_maps_AX_A1*.json", axres=(0, 1, 2, 3, 4, 5), r2="scs3_route2_AX_A1_R*.json",
                           pl="scs3_maps_PL_A2*.json", r2pl="scs3_route2_PL_A1_R*.json",
                           thax="scs3_maps_THICK_AX_A1*.json", r2thax="scs3_route2_THICK_AX_A1_R*.json",
                           thpl="scs3_maps_THICK_PL_A2*.json", r2thpl="scs3_route2_THICK_PL_A1_R*.json"),
                "A4": dict(ax="scs3_maps_AX_A4*.json", axres=(0, 1, 2, 3, 4, 5, 6), r2="scs3_route2_AX_A1_R*.json",
                           pl="scs3_maps_PL_A2*.json", r2pl="scs3_route2_PL_A1_R*.json",
                           thax="scs3_maps_THICK_AX_A4*.json", r2thax="scs3_route2_THICK_AX_A1_R*.json",
                           thpl="scs3_maps_THICK_PL_A2*.json", r2thpl="scs3_route2_THICK_PL_A1_R*.json")}
    # ---------------------------------------------------------------- KA2 / KA1-route2: SCS2's numbers reproduced (frozen)
    def rel(a, b):
        if a == b: return 0.0
        return abs(a - b) / max(abs(a), abs(b))
    axf = load_maps("scs3_maps_AX.json")
    s2res = {r["tag"]: r for r in json.load(open(os.path.join(SCS2, "scs2_resolution.json")))["rows"]}
    worst = 0.0; n2 = 0
    for t, r in axf.items():
        if r["spec"]["group"] != "AX" or r["res"] > 1: continue
        s2 = s2res["bracket_EF_axis_" + bkey(t)[3:] + "_"]
        lab = "coarse" if r["res"] == 0 else "fine"
        worst = max(worst, rel(r["map"]["frac_neg_over_pos"] or 0.0, s2[f"frac_{lab}"]), rel(r["map"]["min_dp_offplane"], s2[f"min_dp_{lab}"]))
        n2 += 1
    s2maps = json.load(open(os.path.join(SCS2, "scs2_maps.json")))["maps"]
    plf = load_maps("scs3_maps_PL.json"); worst_pl = 0.0; npl = 0
    for t, r in plf.items():
        if r["res"] != 0: continue
        s2 = s2maps["bracket_EF_plane_" + bkey(t)[3:] + "_"]["map"]
        worst_pl = max(worst_pl, rel(r["map"]["frac_neg_over_pos"], s2["frac_neg_over_pos"]), rel(r["map"]["min_dp_offplane"], s2["min_dp_offplane"]))
        npl += 1
    s2r2 = {}
    for f in glob.glob(os.path.join(SCS2, "scs2_route2_part*.json")):
        for r in json.load(open(f))["rows"]:
            s2r2[(r["tag"], r["m"], r["parity"])] = r
    worst_r2 = 0.0; nr2 = 0; worst_iso = 0.0; niso = 0; iso_pos = True; seen = set()
    for r in load_r2("scs3_route2_AX_R*.json") + load_r2("scs3_route2_AXKA_R*.json"):
        if r["res"] != 0 or r.get("lambda_min") is None: continue
        if (r["tag"], r["m"], r["parity"]) in seen: continue
        seen.add((r["tag"], r["m"], r["parity"]))
        if r["spec"]["group"] == "AX":
            key = ("bracket_EF_axis_" + bkey(r["tag"])[3:] + "__coarse", r["m"], r["parity"])
            worst_r2 = max(worst_r2, rel(r["lambda_min"], s2r2[key]["lambda_min"])); nr2 += 1
        else:
            key = ("primary_" + bkey(r["tag"])[8:].replace("_0p0_z", "___") + "_coarse", r["m"], r["parity"])
            worst_iso = max(worst_iso, rel(r["lambda_min"], s2r2[key]["lambda_min"])); niso += 1
            iso_pos &= r["lambda_min"] > 0
    RESJ["KA2"] = dict(maps_AX_R0R1=dict(n=n2, worst_rel=worst), maps_PL_R0=dict(n=npl, worst_rel=worst_pl),
                       route2_AX_R0=dict(n=nr2, worst_rel=worst_r2),
                       pass_=bool(n2 == 64 and worst <= 1e-6 and npl == 16 and worst_pl <= 1e-6 and nr2 == 96 and worst_r2 <= 1e-6))
    RESJ["KA1_route2"] = dict(n=niso, worst_rel=worst_iso, all_positive=bool(iso_pos), pass_=bool(niso == 24 and worst_iso <= 1e-6 and iso_pos))
    P_(f"KA2 SCS2's external-field numbers: maps AX R0/R1 {n2} rows worst rel {worst:.1e}; PL R0 {npl} rows worst {worst_pl:.1e}; "
       f"route 2 R0 {nr2} rows worst {worst_r2:.1e} -> {'PASS' if RESJ['KA2']['pass_'] else 'FAIL'}")
    P_(f"KA1 route 2 isolated log M_b 10.45 primaries at R0: {niso} rows, worst rel to SCS2 {worst_iso:.1e}, all lambda_min > 0: "
       f"{iso_pos} -> {'PASS' if RESJ['KA1_route2']['pass_'] else 'FAIL'}")

    for rd, cfg in readings.items():
        FLAT = rd != "A4"
        P_(""); P_(f"================ reading: {rd}")
        R = RESJ[rd] = {}
        ax = load_maps(cfg["ax"]); r2ax = load_r2(cfg["r2"])
        resl = cfg["axres"]
        if not ax:
            P_("  (no AX maps)"); continue
        # KA1: isolated primaries
        iso = [r for r in ax.values() if r["spec"]["group"] == "primary"]
        ka1_map = all(r["all_unmasked_positive"] for r in iso)
        ka1_n = len(iso)
        R["KA1_maps"] = dict(pass_=bool(ka1_map), n_rows=ka1_n, min_dp=min(r["min_dp_all_unmasked"] for r in iso))
        P_(f"KA1 isolated primaries, D.P > 0 in every unmasked cell: {'PASS' if ka1_map else 'FAIL'} ({ka1_n} rows, "
           f"resolutions {sorted(set(r['res'] for r in iso))}, min D.P {R['KA1_maps']['min_dp']:.3e})")
        # M1 on isolated: must turn unstable
        m1_iso = all(r["M1"]["Gamma2_max_s2"] > 0 for r in iso)
        # ---------------- AX family per footing
        for foot in ("canonical", "alt"):
            fam = grade_family(ax, r2ax, "AX", foot, resl)
            p_med = [b["GammaL2"]["finest"]["p"] for b in fam["backgrounds"].values() if b["GammaL2"]["finest"].get("p")]
            fam["median_order_GammaL2"] = float(np.median(p_med)) if p_med else None
            fam["by_strength"] = strength_split(fam)
            R[f"AX_{foot}"] = fam
            P_(f"AX {foot}: {fam['label']}  counts {fam['counts']}; median order of Gamma_L^2 {fam['median_order_GammaL2']}; "
               f"by strength {json.dumps({k_: (v_['label'], v_['counts'], v_['efold_inf_gyr_range']) for k_, v_ in fam['by_strength'].items()})}")
            for k, b in fam["backgrounds"].items():
                gl = b["GammaL2"]
                P_(f"   {k}: e-fold {['%.3f' % x if x else None for x in b['efold_gyr']]} Gyr -> "
                   f"{('%.3f' % gyr(gl['Qinf'])) if gl.get('Qinf') and gl['Qinf'] > 0 else None} "
                   f"(E/Q {gl['E'] / abs(gl['Qinf']) if gl.get('Qinf') and gl.get('E') is not None else None}; {gl['finest']['kind']}, "
                   f"p {gl['finest'].get('p')}); conv {gl['converged']}; route2 {['%.3e' % x if x is not None else None for x in b['route2_lambda']]} "
                   f"conv {b.get('Gamma22', {}).get('converged')}; KA5 {b.get('KA5_ratio')}; r_in/r_e {b['r_inner_over_re']} conv "
                   f"{b['r_inner']['converged']}; -> {b['label']}")
        # ---------------- M1 / M2 on AX
        axrows = [r for r in ax.values() if r["spec"]["group"] == "AX"]
        m1_ax = all(r["M1"]["dp_there_original"] > 0 for r in axrows)
        R["M1"] = dict(bites=bool(m1_ax and m1_iso), ax_moves_out=bool(m1_ax), isolated_turn_unstable=bool(m1_iso))
        m2 = {}
        for k, v in seqs(ax, "AX", resl).items():
            rr = rule3([v[i]["M2"]["Gamma2_max_s2"] for i in resl])
            m2[k] = dict(converged=rr["converged"], diverging=rr["diverging"], efold=[gyr(v[i]["M2"]["Gamma2_max_s2"]) for i in resl])
        R["M2"] = dict(bites=bool(all(not x["converged"] for x in m2.values())), n=len(m2),
                       converged_anyway=[k for k, x in m2.items() if x["converged"]], rows=m2)
        P_(f"M1 tilt flip: {'BITES' if R['M1']['bites'] else 'does not bite'} (AX max moves to D.P > 0: {m1_ax}; isolated turn "
           f"unstable: {m1_iso});  M2 grid artefact: {'BITES' if R['M2']['bites'] else 'does not bite'} "
           f"({len(R['M2']['converged_anyway'])} of {len(m2)} still 'converged')")
        # ---------------- sheet
        sh = {}
        for k, v in seqs(ax, "AX", resl).items():
            vals = [v[i]["sheet"]["Sigma_ph_min"] for i in resl]
            sh[k] = dict(values=vals, rule=rule3(vals), negative_R1_up=bool(any(x < 0 for x in vals[1:])))
        R["sheet"] = sh
        P_(f"sheet: negative Sigma_ph_min at R1 or finer on {sum(x['negative_R1_up'] for x in sh.values())} of {len(sh)}; "
           f"Richardson limits {sorted(round(x['rule']['Qinf'], 1) for x in sh.values() if x['rule']['Qinf'] is not None)[:3]} ... "
           f"{sorted(round(x['rule']['Qinf'], 1) for x in sh.values() if x['rule']['Qinf'] is not None)[-3:]} Msun/kpc^2")
        # ---------------- KA4: two-grid rule on AX R1/R2 against the three-grid answer
        for foot in ("canonical", "alt"):
            fam = R[f"AX_{foot}"]; p = fam["median_order_GammaL2"] or 2.0
            ok = 0; tot = 0
            for k, b in fam["backgrounds"].items():
                v = seqs(ax, "AX", resl)[k]
                for pair in ((1, 2), (0, 1)):
                    tg = rule2(v[pair[0]]["routeL"]["L"]["Gamma2_max_s2"], v[pair[1]]["routeL"]["L"]["Gamma2_max_s2"], p)
                    b[f"two_grid_R{pair[0]}R{pair[1]}"] = tg
                g3 = b["GammaL2"]
                t12 = b["two_grid_R1R2"]
                if g3.get("Qinf") is not None and g3.get("E") is not None:
                    tot += 1; ok += abs(t12["Qinf"] - g3["Qinf"]) <= g3["E"]
            fam["KA4"] = dict(within=ok, of=tot, pass_=bool(ok >= 28 * tot / 32 if tot else False), p=p)
            P_(f"KA4 ({foot}) two-grid R1/R2 vs three-grid: {ok} of {tot} within the three-grid error -> "
               f"{'PASS' if fam['KA4']['pass_'] else 'FAIL'} (p {p})")
        # ---------------- PL family
        pl = load_maps(cfg["pl"]); r2pl = load_r2(cfg["r2pl"])
        if pl:
            plres = sorted(set(r["res"] for r in pl.values()))
            for foot in ("canonical", "alt"):
                p = R[f"AX_{foot}"]["median_order_GammaL2"] or 2.0
                if len(plres) >= 3:
                    fam = grade_family(pl, r2pl, "PL", foot, tuple(plres))
                else:
                    fam = grade_family(pl, r2pl, "PL", foot, (0, 1), two_grid_p=p)
                fam["by_strength"] = strength_split(fam)
                R[f"PL_{foot}"] = fam
                P_(f"PL {foot}: {fam['label']} counts {fam['counts']} (resolutions {plres}; p {p}); by strength "
                   f"{json.dumps({k_: (v_['label'], v_['efold_inf_gyr_range']) for k_, v_ in fam['by_strength'].items()})}")
                for k, b in fam["backgrounds"].items():
                    gl = b["GammaL2"]
                    P_(f"   {k}: e-fold {['%.3f' % x if x else None for x in b['efold_gyr']]} -> "
                       f"{('%.3f' % gyr(gl['Qinf'])) if gl.get('Qinf') and gl['Qinf'] > 0 else None} Gyr (E/Q "
                       f"{gl['E'] / abs(gl['Qinf']) if gl.get('Qinf') else None}); where {b['where']}; Rayleigh {b['route2_rayleigh']}; "
                       f"r_in/r_e {b['r_inner_over_re']}; -> {b['label']}")
        # ---------------- thick twins
        for key, grp, mp, r2p in (("THICK_AX", "THICK_AX", cfg["thax"], cfg["r2thax"]), ("THICK_PL", "THICK_PL", cfg["thpl"], cfg["r2thpl"])):
            tm = load_maps(mp); tr = load_r2(r2p)
            if not tm:
                continue
            tres = tuple(sorted(set(r["res"] for r in tm.values())))
            for foot in ("canonical", "alt"):
                p = R[f"AX_{foot}"]["median_order_GammaL2"] or 2.0
                fam = grade_family(tm, tr, grp, foot, tres, two_grid_p=None if len(tres) >= 3 else p)
                fam["by_strength"] = strength_split(fam)
                R[f"{key}_{foot}"] = fam
                P_(f"{key} {foot}: {fam['label']} counts {fam['counts']}; by strength "
                   f"{json.dumps({k_: (v_['label'], v_['efold_inf_gyr_range']) for k_, v_ in fam['by_strength'].items()})}")
                for k, b in fam["backgrounds"].items():
                    gl = b["GammaL2"]
                    P_(f"   {k}: e-fold {['%.3f' % x if x else None for x in b['efold_gyr']]} -> "
                       f"{('%.3f' % gyr(gl['Qinf'])) if gl.get('Qinf') and gl['Qinf'] > 0 else None} Gyr; conv {gl['converged']}; "
                       f"where {b['where'][-1]}; route2 {b['route2_lambda']}; -> {b['label']}")
        # ---------------- known-answer gate (criteria section 5: each must pass for its family's label)
        ka3ok = RESJ["KA3_A4"]["pass_"] if rd == "A4" else RESJ["KA3"]["pass_"]
        common = [n_ for n_, ok_ in (("KA1 maps", R["KA1_maps"]["pass_"]), ("KA1 route 2", RESJ["KA1_route2"]["pass_"]),
                                     ("KA2", RESJ["KA2"]["pass_"]), ("KA3", ka3ok)) if not ok_]
        R["gate_common_failed"] = common
        P_(f"-- gate ({rd}): known answers failing for every family: {common or 'none'}")
        for key in [k_ for k_ in R if isinstance(R[k_], dict) and "label" in R[k_]]:
            fam = R[key]; fam["label_rule_only"] = fam["label"]
            fail = list(common)
            if key.startswith("PL") or key.startswith("THICK_PL"):
                two = all(len(b["efold_gyr"]) == 2 for b in fam["backgrounds"].values())
                foot = key.split("_")[-1]
                if two and not R.get(f"AX_{foot}", {}).get("KA4", {}).get("pass_", False):
                    fail.append("KA4 (two-grid rule not trusted)")
            fam["gate_failed"] = fail
            if fail:
                fam["label"] = "NO VERDICT"
            P_(f"   {rd} {key}: LABEL {fam['label']}" + (f"  (rule alone: {fam['label_rule_only']}; failing: {fail})" if fail else ""))
    # ---------------------------------------------------------------- section 7: physical reading (A1 reading, finest grid)
    P_(""); P_("================ physical reading (A2 reading = A1 for the axial family; finest grid of each family)")
    phys = RESJ["physical"] = {}
    for fam_key, pat, grp in (("AX", "scs3_maps_AX_A1*.json", "AX"), ("PL", "scs3_maps_PL_A2*.json", "PL"),
                              ("THICK_AX", "scs3_maps_THICK_AX_A1*.json", "THICK_AX")):
        mp = load_maps(pat)
        if not mp:
            continue
        rmax = max(r["res"] for r in mp.values() if r["spec"]["group"] == grp)
        for t, r in sorted(mp.items()):
            if r["spec"]["group"] != grp or r["res"] != rmax:
                continue
            k = bkey(t); foot = r["spec"]["foot"]
            fam = RESJ.get("A2", {}).get(f"{fam_key}_{foot}", {}).get("backgrounds", {}).get(k)
            G2inf = fam["GammaL2"]["Qinf"] if fam and fam["GammaL2"].get("Qinf") else r["routeL"]["L"]["Gamma2_max_s2"]
            te = gyr(G2inf)
            o = r["orbital"]; rf = r["routeL"].get("region_fast"); rn = r.get("region_negative")
            phys[k] = dict(efold_gyr=te, efolds_in_tH=T_H / te if te else None, r_e_kpc=r["r_e_kpc"], R_d_kpc=r["Rd_kpc"],
                           where_r_over_re=r["routeL"]["L"]["r_over_re"], where_theta=r["routeL"]["L"]["theta_deg"],
                           T_orb_disc_2p2Rd_gyr=o["T_orb_disc_gyr"], T_kepler_at_rstar_gyr=o["T_kepler_at_rstar_gyr"],
                           region_negative=rn, region_fast=rf, converged=fam["label"] if fam else None)
            P_(f"   {k}: t_e {te:.3g} Gyr ({T_H / te:.3g} e-folds in t_H); r_e {r['r_e_kpc']:.1f} kpc = {r['r_e_kpc'] / r['Rd_kpc']:.0f} R_d; "
               f"max at {r['routeL']['L']['r_over_re']:.2f} r_e, theta {r['routeL']['L']['theta_deg']:.0f}; T_orb(2.2 R_d) "
               f"{o['T_orb_disc_gyr']:.3f} Gyr; T_Kepler(r*) {o['T_kepler_at_rstar_gyr']:.2f} Gyr; negative region "
               f"{rn and [round(x, 2) for x in rn['r_over_re']]} r_e, reaches disc {rn and rn['reaches_disc']}; >1 e-fold in t_H: "
               f"{rf and [round(x, 2) for x in rf['r_over_re']]} r_e = {rf and [round(x, 1) for x in rf['r_over_Rd']]} R_d, "
               f"reaches disc {rf and rf['reaches_disc']}")
    RESJ["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    with open(os.path.join(HERE, "scs3_labels.json"), "w") as fh:
        json.dump(RESJ, fh, indent=1, default=str)
    P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    with open(os.path.join(HERE, "scs3_labels.out"), "w") as fh:
        fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
