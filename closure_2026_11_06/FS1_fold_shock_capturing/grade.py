#!/usr/bin/env python3
"""FS1 grade: frozen lines of CRITERIA.md (f716e2f98f) on parts/ and parts_checks/. Writes GRADE.json, prints grade.out.
Run from the repo root: python3 closure_2026_11_06/FS1_fold_shock_capturing/grade.py
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, glob
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf
import fs1, fs1_ref
ac10 = fs1.ac10
ROOT = fs1.ROOT
AC14 = os.path.join(ROOT, "action_search_2026_11_05", "AC14_fold_final")
AC10D = os.path.join(ROOT, "action_search_2026_11_05", "AC10_nonlinear_clock")
CL = 2.99792458e8
LINE, TOL_T, TOL_J = fs1.LINE, fs1.TOL_T, fs1.TOL_J
log = lambda s: print(s, flush=True)


def ladder_of(row, pdir="parts"):
    rs = fs1.load_rungs(pdir, row)
    if len(rs) < 3:
        return None
    j = fs1.judge(rs)
    j["rungs"] = rs
    dec = [r for r in rs if r["N"] == j["deciding"]] if j["deciding"] else []
    j["dec"] = dec[0] if dec else rs[-1]
    j["sub"] = fs1.sub(j["dec"]) if j["converged"] else "NOT CONVERGED"
    return j


def pair_outcome(A, B):
    """A = AC2q (or planted), B = v3s twin (or unplanted); ladder dicts"""
    if A is None or B is None or not (A["converged"] and B["converged"]):
        return dict(outcome="OPEN", r=None, E=None)
    la, lb = A["label"], B["label"]
    E = (A["e"] or 0.0) + (B["e"] or 0.0)
    if la == lb == "FOLD":
        r = A["dec"]["t_fold"] / B["dec"]["t_fold"]
        if abs(r - 1) + E <= LINE:
            return dict(outcome="SAME-FOLD", r=r, E=E)
        if abs(r - 1) - E > LINE:
            return dict(outcome="DIFF-TIME", sub="EARLIER" if r < 1 else "LATER", r=r, E=E)
        return dict(outcome="UNRESOLVED", r=r, E=E)
    if la == lb == "HELD":
        return dict(outcome="SAME-HELD", r=None, E=E)
    return dict(outcome="DIFF-LABEL", sub="REGULARIZES" if la == "HELD" else "WORSE", r=None, E=E)


def sample_rows():
    s = fs1.stiff_ac2q()[::8]
    return s + [fs1.twin(r) for r in s]


def first_phantom_fold():
    for r in [x for x in ac10.physical_rows() if x["model"] == "AC2q" and x["kind"] == "phantom"]:
        L = ladder_of(r)
        if L is not None and L["converged"] and L["label"] == "FOLD":
            return r
    return None


def diff_pairs():
    out = []
    for a in [x for x in ac10.physical_rows() if x["model"] == "AC2q"]:
        b = fs1.twin(a); po = pair_outcome(ladder_of(a), ladder_of(b))
        if po["outcome"].startswith("DIFF"):
            out.append((a, b))
    return out


def check_jobs():
    jobs = []
    for r in sample_rows():
        L = ladder_of(r)
        if L is None or not L["deciding"]:
            continue
        N = L["deciding"]
        jobs.append((dict(r, cq=2.0, cl=1.0, _chk="visc"), N, "parts_checks"))
        jobs.append((dict(r, cfl=0.2, fsheet=0.025, _chk="dt"), N, "parts_checks"))
    p2 = first_phantom_fold()
    if p2 is not None:
        for N in fs1.LADDER:
            jobs.append((dict(p2, kind="MUTATE_P2_phantom", sheet=1.03), N, "parts_checks"))
        Lp = fs1.load_rungs("parts_checks", dict(p2, kind="MUTATE_P2_phantom", sheet=1.03))
        if len(Lp) >= 3 and fs1.judge(Lp)["need_extra"]:
            jobs.append((dict(p2, kind="MUTATE_P2_phantom", sheet=1.03), fs1.EXTRA, "parts_checks"))
    for a, b in diff_pairs():
        for r in (a, b):
            L = ladder_of(r)
            jobs.append((dict(r, edge_b=1, _chk="K4"), L["deciding"], "parts_checks"))
    return jobs


def variant_ok(base, var):
    if var is None:
        return None
    kb, kv = fs1.klass(base), fs1.klass(var)
    if kb != kv or kb == "UNDECIDED":
        return dict(ok=False, base=kb, var=kv, rel=None)
    if kb == "FOLD":
        rel = abs(var["t_fold"] / base["t_fold"] - 1); return dict(ok=rel <= TOL_T, base=kb, var=kv, rel=rel)
    rel = abs(var["J_min"] / base["J_min"] - 1); return dict(ok=rel <= TOL_J, base=kb, var=kv, rel=rel)


def load_one(pdir, row, N):
    fn = fs1.rung_file(pdir, row, N)
    return json.load(open(fn)) if os.path.exists(fn) else None


def main():
    out, chk = {}, {}
    missing = []

    # K0: core = numpy reference (N 500)
    rows = ac10.physical_rows()
    soft = [r for r in rows if r["kind"] == "soft" and r["model"] == "v3s"][0]
    clk = [r for r in rows if r["kind"] == "clock_only" and r["model"] == "AC2q"][0]
    phx = max([r for r in rows if r["kind"] == "phantom" and r["model"] == "AC2q"], key=lambda r: r["gam"] * r["Pi0"])
    k0 = {}
    for nm, r, tm in (("soft_v3s_1", soft, 6.0), ("clock_AC2q_1", clk, 6.0), ("phantom_AC2q_max", phx, 1.5)):
        a = fs1.run(500, r["M1"], r["Pi0"], r["s2_use"], r["gam"], tmax=tm)
        b = fs1_ref.run(500, r["M1"], r["Pi0"], r["s2_use"], r["gam"], tmax=tm)
        qa = a["t_fold"] if a["t_fold"] is not None else a["J_min"]; qb = b["t_fold"] if b["t_fold"] is not None else b["J_min"]
        k0[nm] = dict(core=qa, ref=qb, rel=abs(qa / qb - 1), what="t_fold" if a["t_fold"] is not None else "J_min")
    chk["K0"] = all(v["rel"] <= 1e-9 for v in k0.values()); out["K0"] = k0
    log(f"K0 {'PASS' if chk['K0'] else 'FAIL'} {k0}")

    # K1: zero charge coupled vs independent two-label integration; thin-sheet delay
    N = 2000; i1 = int((1 - ac10.EDGE) * N); c = i1 - 1
    rr = fs1.run(N, 1.0, 0.0, 0.0, 0.0)
    q = np.linspace(ac10.X0[0], ac10.X0[1], N + 1); dq = q[1] - q[0]

    def pair_fold(sheet):
        def f(t, y):
            return np.concatenate([y[2:], -0.5 * sheet * erf(y[:2] / (math.sqrt(2) * ac10.WB))])
        def ev(t, y):
            return (y[1] - y[0]) / dq - ac10.JTHR
        ev.terminal = True; ev.direction = -1
        sp = solve_ivp(f, (0, ac10.TMAX), [q[c], q[c + 1], 1.0, 1.0], method="DOP853", rtol=1e-12, atol=1e-14,
                       events=ev, dense_output=True)
        tp = float(sp.t_events[0][0]); xm = lambda t: 0.5 * (sp.sol(t)[0] + sp.sol(t)[1])
        tc = brentq(xm, 0, tp); vc = 0.5 * (sp.sol(tc)[2] + sp.sol(tc)[3])
        return tp, tc, vc
    tp, tc, vc = pair_fold(1.0)
    chk["K1"] = abs(rr["t_fold"] - tp) <= 1e-6 and abs((tp - tc) / vc - 1) <= 0.02
    out["K1"] = dict(t_coupled=rr["t_fold"], t_pair=tp, delay_over_vcross=(tp - tc) / vc)
    log(f"K1 {'PASS' if chk['K1'] else 'FAIL'} {out['K1']}")

    # K2/K3: stress rows, own v_cross, time-at-level tolerance (fold rows) / J tolerance where J >= J_reg (no-fold)
    rho_b = lambda x: np.exp(-x ** 2 / (2 * ac10.WB ** 2)) / (math.sqrt(2 * math.pi) * ac10.WB)
    levels = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001)
    kk = {}
    for row in fs1.stress_rows():
        Pi0, s2 = row["Pi0"], row["s2_use"]; thr = 1 / math.sqrt(2) if row["kind"] == "stress_A1" else 1.0
        o = fs1.run(N, 1.0, Pi0, s2, 0.0, rec_node=c)
        R = o["rec"]; tt = R[:, 0]; Jn = (R[:, 2] - R[:, 1]) / dq; vnode = R[:, 3]; xmid = 0.5 * (R[:, 1] + R[:, 2])
        neg = np.nonzero(vnode < 0)[0]
        t_turn = float(tt[neg[0]]) if len(neg) else float(tt[-1])
        m = tt <= t_turn
        k = np.nonzero(xmid[m] >= 0)[0][0]
        tcr = float(np.interp(0.0, xmid[k - 1:k + 1], tt[k - 1:k + 1]))
        vcr = float(np.interp(tcr, tt, 0.5 * (R[:, 3] + R[:, 4])))
        xm = lambda t: float(np.interp(t, tt, xmid))
        f = lambda t, y: [y[1], -rho_b(xm(t)) * y[0] + (Pi0 - s2 * y[0])]
        t_ext = t_turn + (0.2 if o["status"] == 1 else 0.0)   # numeric run stops at its fold; per-label J may cross just after
        so = solve_ivp(f, (0, t_ext), [1.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-13, max_step=ac10.WB / 4,
                       dense_output=True)
        Jo = so.sol(tt[m])[0]
        pred = math.sqrt(Pi0) * vcr <= thr
        fpn = bool(Jn[m].min() <= ac10.JTHR * 1.01)
        tg = np.linspace(0, t_ext, 200001); Jg = so.sol(tg)[0]
        fpo = bool(Jg.min() <= ac10.JTHR * 1.01)
        d = dict(v_cross=vcr, omega_vc=math.sqrt(Pi0) * vcr, threshold=thr, predict_fold=pred, numeric_fold=fpn,
                 per_label_fold=fpo, minJ_first_passage=float(Jn[m].min()))
        if fpn and fpo:
            worst = 0.0; lv = {}
            for l in levels:
                i = np.nonzero(Jn[m] <= l)[0]; j = np.nonzero(Jg <= l)[0]
                if not len(i) or not len(j):
                    lv[l] = None; worst = math.inf; continue
                i = i[0]; j = j[0]
                tn = float(np.interp(l, [Jn[m][i], Jn[m][i - 1]], [tt[m][i], tt[m][i - 1]]))
                to = float(np.interp(l, [Jg[j], Jg[j - 1]], [tg[j], tg[j - 1]]))
                lv[l] = abs(tn / to - 1); worst = max(worst, lv[l])
            d.update(time_at_level_rel=lv, worst=worst, ok_tol=worst <= 5e-3)
        else:
            sel = Jo >= ac10.JREG
            d.update(J_maxrel_where_Jreg=float(np.max(np.abs(Jn[m][sel] - Jo[sel]) / Jo[sel])))
            d["ok_tol"] = d["J_maxrel_where_Jreg"] <= 1e-3
        d["ok"] = (pred == fpn == fpo) and d["ok_tol"]
        kk[row["tag"]] = d; log(f"{row['tag']}: {d}")
    chk["K2"] = kk["A1_0.2"]["ok"] and kk["A1_1.0"]["ok"]; chk["K3"] = kk["A2_0.4"]["ok"] and kk["A2_2.0"]["ok"]
    out["K2K3"] = kk

    # ladders of all physical rows
    LAD = {}
    for r in rows:
        L = ladder_of(r)
        if L is None:
            missing.append((r["kind"], r["model"], r["foot"], r["r_kpc"]))
        LAD[fs1.key(r)] = L

    # KA1: AC14's 24 soft FOLD/FOLD pairs
    a14 = {}
    for fn in glob.glob(os.path.join(AC14, "parts", "*.json")):
        p = json.load(open(fn)); a14[fs1.key(p["row"])] = p
    tk = lambda rw: (rw["foot"], rw["r_kpc"], rw["w_kms"], rw["M1"], rw["Lstar_pc"], rw["kind"])
    ka1 = []; ka1ok = True
    for a in [r for r in rows if r["model"] == "AC2q" and r["kind"] == "soft"]:
        b = fs1.twin(a); pa = a14.get(fs1.key(a)); pb = a14.get(fs1.key(b))
        if not (pa and pb and pa["label"] == "FOLD" and pb["label"] == "FOLD"):
            continue
        La, Lb = LAD[fs1.key(a)], LAD[fs1.key(b)]
        if La is None or Lb is None:
            ka1ok = False; continue
        ent = dict(foot=a["foot"], r=a["r_kpc"], w=a["w_kms"], M1=a["M1"], L=a["Lstar_pc"])
        ok = La["converged"] and Lb["converged"] and La["label"] == Lb["label"] == "FOLD"
        if ok:
            ent["r_minus_1"] = abs(La["dec"]["t_fold"] / Lb["dec"]["t_fold"] - 1)
            for nm, L, p in (("AC2q", La, pa), ("v3s", Lb, pb)):
                Na = p["rungs"][-1]["N"]; ta = p["rungs"][-1]["t_fold"]
                mine = [x for x in L["rungs"] if x["N"] == Na]
                ent[f"vs_AC14_{nm}"] = abs(mine[0]["t_fold"] / ta - 1) if mine and mine[0]["t_fold"] else math.inf
            ok = ent["r_minus_1"] <= 5e-6 and ent["vs_AC14_AC2q"] <= 1e-5 and ent["vs_AC14_v3s"] <= 1e-5
        ent["ok"] = ok; ka1.append(ent); ka1ok = ka1ok and ok
    chk["KA1"] = ka1ok and len(ka1) == 24
    out["KA1"] = dict(n=len(ka1), max_r_minus_1=max([e.get("r_minus_1", math.inf) for e in ka1], default=None),
                      max_vs_AC14=max([max(e.get("vs_AC14_AC2q", math.inf), e.get("vs_AC14_v3s", math.inf)) for e in ka1], default=None),
                      pairs=ka1)
    log(f"KA1 {'PASS' if chk['KA1'] else 'FAIL'} n={len(ka1)} max|r-1|={out['KA1']['max_r_minus_1']} max vs AC14={out['KA1']['max_vs_AC14']}")

    # KA2: AC10's A2-POST first fold over all cells, converged rows of its 12-pair subset; AC10's K1 time
    ka2 = []; ka2ok = True
    for fn in glob.glob(os.path.join(AC10D, "parts", "*.json")):
        p = json.load(open(fn)); rw = p["row"]
        if rw.get("kind") not in ("phantom", "clock_only", "soft") or p.get("label_all") != "FOLD":
            continue
        L = LAD.get(fs1.key(rw))
        Nl = p["rungs"][-1]["N"]; ta = p["rungs"][-1]["t_fold_all"]
        mine = [x for x in (L["rungs"] if L else []) if x["N"] == Nl]
        rel = abs(mine[0]["t_fold_all"] / ta - 1) if mine and mine[0]["t_fold_all"] else math.inf
        ka2.append(dict(foot=rw["foot"], r=rw["r_kpc"], kind=rw["kind"], model=rw["model"], N=Nl, AC10=ta,
                        FS1=mine[0]["t_fold_all"] if mine else None, rel=rel))
        ka2ok = ka2ok and rel <= 2.5e-3
    k1_10 = 1.2828263549695669
    ka2k1 = abs(rr["t_fold"] - k1_10) <= 1e-6
    chk["KA2"] = ka2ok and ka2k1 and len(ka2) > 0
    out["KA2"] = dict(rows=ka2, n=len(ka2), max_rel=max([x["rel"] for x in ka2], default=None), K1_AC10=k1_10,
                      K1_FS1=rr["t_fold"], K1_ok=ka2k1)
    log(f"KA2 {'PASS' if chk['KA2'] else 'FAIL'} n={len(ka2)} max rel={out['KA2']['max_rel']} K1 {rr['t_fold']} vs {k1_10}")

    # MUTATEs
    mrows = {r["kind"]: r for r in fs1.main_rows() if r["kind"].startswith("MUTATE")}
    mm = {}
    LA = ladder_of(mrows["MUTATE_A_repulsive"]); LB = ladder_of(mrows["MUTATE_B_mach0.3"])
    mm["A"] = dict(subs=[fs1.sub(x) for x in LA["rungs"]] if LA else None, J_min=[x["J_min"] for x in LA["rungs"]] if LA else None)
    chk["MUTATE_A"] = bool(LA) and all(fs1.sub(x) == "REGULAR" for x in LA["rungs"])
    mm["B"] = dict(converged=LB["converged"] if LB else None, subs=[fs1.sub(x) for x in LB["rungs"]] if LB else None,
                   J_min=[x["J_min"] for x in LB["rungs"]] if LB else None)
    chk["MUTATE_B"] = bool(LB) and LB["converged"] and LB["sub"] == "REGULAR"
    # P1: planted sheet 1.03 on the zero-charge row; exact two-label prediction; pair logic vs K1 row
    LP1 = ladder_of(mrows["MUTATE_P1_zero_charge"]); LK1 = ladder_of([r for r in fs1.main_rows() if r["kind"] == "K1_zero_charge"][0])
    tp3, _, _ = pair_fold(1.03)
    p1n = [x for x in LP1["rungs"] if x["N"] == 2000][0]["t_fold"] if LP1 else None
    po1 = pair_outcome(LP1, LK1)
    mm["P1"] = dict(t_planted_N2000=p1n, t_pair_pred=tp3, abs_diff=abs(p1n - tp3) if p1n else None, pair=po1)
    chk["MUTATE_P1"] = p1n is not None and abs(p1n - tp3) <= 1e-6 and po1["outcome"] == "DIFF-TIME"
    # P2: first phantom AC2q FOLD row, planted
    p2 = first_phantom_fold()
    if p2 is not None:
        LP2 = ladder_of(dict(p2, kind="MUTATE_P2_phantom", sheet=1.03), "parts_checks")
        po2 = pair_outcome(LP2, LAD[fs1.key(p2)])
        mm["P2"] = dict(row=dict(foot=p2["foot"], r=p2["r_kpc"], w=p2["w_kms"], M1=p2["M1"], L=p2["Lstar_pc"]), pair=po2)
        chk["MUTATE_P2"] = po2["outcome"] in ("DIFF-TIME", "DIFF-LABEL")
    else:
        mm["P2"] = None; chk["MUTATE_P2"] = False
    LP3 = ladder_of(mrows["MUTATE_P3_clock"]); po3 = pair_outcome(LP3, LAD[fs1.key(clk)])
    mm["P3"] = dict(pair=po3); chk["MUTATE_P3"] = po3["outcome"] in ("DIFF-TIME", "DIFF-LABEL")
    out["MUTATE"] = mm; log(f"MUTATE {json.dumps(mm, default=str)}")

    # K-visc, K-dt on the sample
    kv, kd = [], []
    for r in sample_rows():
        L = LAD[fs1.key(r)]
        if L is None or not L["deciding"]:
            kv.append(dict(ok=False, why="no deciding rung")); kd.append(dict(ok=False, why="no deciding rung")); continue
        base = L["dec"]; N_ = L["deciding"]
        v1 = load_one("parts_checks", dict(r, cq=2.0, cl=1.0, _chk="visc"), N_)
        v2 = load_one("parts_checks", dict(r, cfl=0.2, fsheet=0.025, _chk="dt"), N_)
        a1 = variant_ok(base, v1); a2 = variant_ok(base, v2)
        tag = dict(foot=r["foot"], r=r["r_kpc"], kind=r["kind"], model=r["model"], N=N_)
        kv.append(dict(tag, **(a1 or dict(ok=False, why="missing")))); kd.append(dict(tag, **(a2 or dict(ok=False, why="missing"))))
    chk["K_visc"] = all(x["ok"] for x in kv) and len(kv) == 40; chk["K_dt"] = all(x["ok"] for x in kd) and len(kd) == 40
    out["K_visc"] = kv; out["K_dt"] = kd
    log(f"K-visc {'PASS' if chk['K_visc'] else 'FAIL'} max rel {max([x.get('rel') or 0 for x in kv], default=None)}; "
        f"K-dt {'PASS' if chk['K_dt'] else 'FAIL'} max rel {max([x.get('rel') or 0 for x in kd], default=None)}")

    # pairs
    pairs = []; tab = {}; xmin = 1.0; shock_fold = {}; edge_first = 0
    for a in [r for r in rows if r["model"] == "AC2q"]:
        b = fs1.twin(a); La, Lb = LAD[fs1.key(a)], LAD[fs1.key(b)]
        po = pair_outcome(La, Lb)
        ent = dict(foot=a["foot"], r_kpc=a["r_kpc"], kind=a["kind"], w=a["w_kms"], M1=a["M1"], L=a["Lstar_pc"],
                   AC2q=La["sub"] if La else "MISSING", v3s=Lb["sub"] if Lb else "MISSING",
                   t_AC2q=La["dec"]["t_fold"] if La else None, t_v3s=Lb["dec"]["t_fold"] if Lb else None,
                   Jmin_AC2q=La["dec"]["J_min"] if La else None, Jmin_v3s=Lb["dec"]["J_min"] if Lb else None,
                   e_AC2q=La["e"] if La else None, e_v3s=Lb["e"] if Lb else None,
                   N_AC2q=La["deciding"] if La else None, N_v3s=Lb["deciding"] if Lb else None,
                   shock_at_fold_AC2q=La["dec"]["shock_at_fold"] if La else None,
                   shock_at_fold_v3s=Lb["dec"]["shock_at_fold"] if Lb else None, **po)
        if po["outcome"].startswith("DIFF"):
            ka = load_one("parts_checks", dict(a, edge_b=1, _chk="K4"), La["deciding"])
            kb = load_one("parts_checks", dict(b, edge_b=1, _chk="K4"), Lb["deciding"])
            if ka and kb:
                fa = dict(converged=True, label=fs1.klass(ka), e=La["e"], dec=ka); fb = dict(converged=True, label=fs1.klass(kb), e=Lb["e"], dec=kb)
                ent["K4_Eb"] = pair_outcome(fa, fb)
            else:
                ent["K4_Eb"] = "missing"
        pairs.append(ent)
        k = f"{a['foot']}|{a['kind']}|{po['outcome']}{'/' + po['sub'] if 'sub' in po else ''}|AC2q {ent['AC2q']}|v3s {ent['v3s']}"
        tab[k] = tab.get(k, 0) + 1
        for L, rw in ((La, a), (Lb, b)):
            if L:
                xmin = min(xmin, 1 - (max(x["v_max"] for x in L["rungs"]) * rw["w_kms"] * 1e3 / CL) ** 2)
                edge_first += int(L["dec"]["edge_first"])
                if L["converged"] and L["label"] == "FOLD":
                    kk2 = f"{rw['model']}|{rw['kind']}|shock_at_fold={L['dec']['shock_at_fold']}"
                    shock_fold[kk2] = shock_fold.get(kk2, 0) + 1
    chk["X_pos"] = xmin > 0.99
    out.update(table=tab, X_over_Xbg_min=xmin, shock_at_fold_counts=shock_fold, rows_edge_first_fold=edge_first,
               pairs=pairs, missing_rows=missing)
    for k in sorted(tab):
        log(f"  {k}: {tab[k]}")
    log(f"shock-at-fold counts {shock_fold}; rows whose first all-cell J_thr was an edge cell: {edge_first}; X min {xmin}")

    oc = [p["outcome"] for p in pairs]
    diffs = [p for p in pairs if p["outcome"].startswith("DIFF")]
    checks = all(chk.values())
    if missing or len(pairs) != 240:
        v = "INCOMPLETE (rows missing; not a verdict)"
    elif not checks:
        v = "NO VERDICT"
    elif diffs:
        v = "DIFFERS"
    elif all(o in ("SAME-FOLD", "SAME-HELD") for o in oc):
        nh = oc.count("SAME-HELD")
        v = "FOLDS-SAME-AS-V3S" + (f" ({nh} pairs held in both)" if nh else "")
    else:
        v = "NO VERDICT"
    rs = [p["r"] for p in pairs if p["r"] is not None]
    out["bracket"] = dict(counts={o: oc.count(o) for o in sorted(set(oc))}, r_range=[min(rs), max(rs)] if rs else None,
                          Jmin_open=[p["Jmin_AC2q"] for p in pairs if p["outcome"] == "OPEN"])
    out["diff_rows"] = diffs
    by = {}
    for p in diffs:
        kx = f"{p['foot']}|{p['kind']}|{p['outcome']}/{p.get('sub')}|K4 E-b {p['K4_Eb']['outcome'] if isinstance(p.get('K4_Eb'), dict) else p.get('K4_Eb')}"
        by[kx] = by.get(kx, 0) + 1
    out["diff_summary"] = by
    out["checks"] = chk; out["verdict"] = v; out["criteria"] = "f716e2f98f"
    log(f"bracket {out['bracket']['counts']} r range {out['bracket']['r_range']}")
    log(f"DIFF summary {by}")
    log(f"checks {chk}\nVERDICT (frozen): {v}")
    json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
