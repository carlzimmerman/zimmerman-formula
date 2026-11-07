#!/usr/bin/env python3
"""FS2 grade: frozen lines of CRITERIA.md (1a686ed9a2) on parts/ and parts_checks/. Writes GRADE.json, prints grade.out.
Graded observable: t_reg = first interior J <= J_reg (0.05). Run from the repo root:
  python3 closure_2026_11_06/FS2_fold_viscosity_free/grade.py > closure_2026_11_06/FS2_fold_viscosity_free/grade.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, glob, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m)
    return m


fs2 = sys.modules.get("fs2") or _load("fs2", os.path.join(HERE, "fs2.py"))
fs2_ref = _load("fs2_ref", os.path.join(HERE, "fs2_ref.py"))
fs1 = fs2.fs1; ac10 = fs2.ac10
fs1grade = _load("fs1_grade", os.path.join(fs2.FS1D, "grade.py"))      # FS1's frozen pair logic (by path; main() not run)
CL = 2.99792458e8
LINE, TOL_T, TOL_J = fs2.LINE, fs2.TOL_T, fs2.TOL_J
log = lambda s: print(s, flush=True)


def ladder_of(row, pdir="parts"):
    rs = fs2.load_rungs(pdir, row)
    if len(rs) < 3:
        return None
    j = fs2.judge(rs); j["rungs"] = rs
    dec = [r for r in rs if r["N"] == j["deciding"]] if j["deciding"] else []
    j["dec"] = dec[0] if dec else rs[-1]
    return j


def ladder_fs1(row, pdir="parts"):
    """FS1's frozen ladder (J_thr reading) applied to FS2's rung files"""
    rs = fs2.load_rungs(pdir, row)
    if len(rs) < 3:
        return None
    j = fs1.judge(rs); j["rungs"] = rs
    dec = [r for r in rs if r["N"] == j["deciding"]] if j["deciding"] else []
    j["dec"] = dec[0] if dec else rs[-1]
    return j


def pair_outcome(A, B):
    """FS2 pair logic at J_reg. A = AC2q (or planted), B = v3s twin (or unplanted)."""
    if A is None or B is None or not (A["converged"] and B["converged"]):
        return dict(outcome="OPEN", r=None, E=None)
    la, lb = A["label"], B["label"]
    E = (A["e"] or 0.0) + (B["e"] or 0.0)
    if la == lb == "REACH":
        r = fs2.t_reg(A["dec"]) / fs2.t_reg(B["dec"])
        if abs(r - 1) + E <= LINE:
            return dict(outcome="SAME-REACH", r=r, E=E)
        if abs(r - 1) - E > LINE:
            return dict(outcome="DIFF-TIME", sub="EARLIER" if r < 1 else "LATER", r=r, E=E)
        return dict(outcome="UNRESOLVED", r=r, E=E)
    if la == lb == "REGULAR":
        return dict(outcome="SAME-REGULAR", r=None, E=E)
    return dict(outcome="DIFF-LABEL", sub="REGULARIZES" if la == "REGULAR" else "WORSE", r=None, E=E)


def first_phantom_reach():
    for r in [x for x in ac10.physical_rows() if x["model"] == "AC2q" and x["kind"] == "phantom"]:
        L = ladder_of(r)
        if L is not None and L["converged"] and L["label"] == "REACH":
            return r
    return None


def p2_row(p2):
    return dict(p2, kind="MUTATE_P2_phantom", sheet=1.03)


def diff_pairs():
    out = []
    for a in [x for x in ac10.physical_rows() if x["model"] == "AC2q"]:
        b = fs2.twin(a)
        if pair_outcome(ladder_of(a), ladder_of(b))["outcome"].startswith("DIFF"):
            out.append((a, b))
    return out


def check_jobs():
    jobs = []
    for r in fs2.sample_rows():
        L = ladder_of(r)
        if L is None or not L["deciding"]:
            continue
        for nm, kw in fs2.VARIANTS:
            jobs.append((dict(r, _chk=nm, **kw), L["deciding"], "parts_checks"))
    p2 = first_phantom_reach()
    if p2 is not None:
        for N in fs2.LADDER:
            jobs.append((p2_row(p2), N, "parts_checks"))
        Lp = fs2.load_rungs("parts_checks", p2_row(p2))
        if len(Lp) >= 3 and fs2.judge(Lp)["need_extra"]:
            jobs.append((p2_row(p2), fs2.EXTRA, "parts_checks"))
    for a, b in diff_pairs():
        for r in (a, b):
            jobs.append((dict(r, edge_b=1, _chk="K4"), ladder_of(r)["deciding"], "parts_checks"))
    return jobs


def load_one(pdir, row, N):
    fn = fs2.rung_file(pdir, row, N)
    return json.load(open(fn)) if os.path.exists(fn) else None


def variant_ok(base, var):
    if var is None:
        return dict(ok=False, why="missing")
    kb, kv = fs2.klass(base), fs2.klass(var)
    lev = {}
    for i, l in enumerate(fs2.LEVELS):            # reported, not gating
        a, b = base["t_lev"][i], var["t_lev"][i]
        lev[l] = abs(b / a - 1) if (a and b) else None
    thr = abs(var["t_fold"] / base["t_fold"] - 1) if (base["t_fold"] and var["t_fold"]) else None
    rep = dict(level_shift=lev, Jthr_shift=thr, Jthr_class=(fs1.klass(base), fs1.klass(var)))
    if kb != kv or kb == "UNDECIDED":
        return dict(ok=False, base=kb, var=kv, rel=None, **rep)
    if kb == "REACH":
        rel = abs(fs2.t_reg(var) / fs2.t_reg(base) - 1); return dict(ok=rel <= TOL_T, base=kb, var=kv, rel=rel, **rep)
    rel = abs(var["J_min"] / base["J_min"] - 1); return dict(ok=rel <= TOL_J, base=kb, var=kv, rel=rel, **rep)


def relq(a, b):
    if a is None and b is None:
        return 0.0
    if a is None or b is None:
        return math.inf
    return abs(a / b - 1) if b != 0 else abs(a - b)


def main():
    out, chk = {}, {}
    missing = []
    rows = ac10.physical_rows()

    # KA: every FS1 rung reproduced; FS1 bracket reproduced; FS1 K-visc x2 sample files reproduced
    ka = dict(n=0, n_missing=0, max_rel=0.0, nstep_mismatch=0, class_mismatch=0, worst=None)
    for fn in sorted(glob.glob(os.path.join(fs2.FS1D, "parts", "*.json"))):
        f1 = json.load(open(fn)); g = os.path.join(HERE, "parts", os.path.basename(fn))
        if not os.path.exists(g):
            ka["n_missing"] += 1; continue
        f2 = json.load(open(g)); ka["n"] += 1
        if f1["status"] != f2["status"]:
            ka["class_mismatch"] += 1
        if f1["nstep"] != f2["nstep"]:
            ka["nstep_mismatch"] += 1
        for fld in ("t_fold", "t_fold_all", "J_min", "J_min_all"):
            rq = relq(f2[fld], f1[fld])
            if rq > ka["max_rel"]:
                ka["max_rel"] = rq; ka["worst"] = (os.path.basename(fn), fld)
    LAD1 = {}
    for r in rows:
        LAD1[fs2.key(r)] = ladder_fs1(r)
    oc1 = []
    for a in [r for r in rows if r["model"] == "AC2q"]:
        po = fs1grade.pair_outcome(LAD1[fs2.key(a)], LAD1[fs2.key(fs2.twin(a))]); oc1.append(po)
    ka["FS1_bracket_from_FS2"] = {o: [p["outcome"] for p in oc1].count(o) for o in sorted(set(p["outcome"] for p in oc1))}
    fs1_br = {"DIFF-TIME": 80, "SAME-FOLD": 137, "SAME-HELD": 23}
    kv1 = dict(n=0, max_rel=0.0, missing=0)
    for r in fs1grade.sample_rows():
        L = LAD1[fs2.key(r)] if fs2.key(r) in LAD1 else None
        if not L or not L["deciding"]:
            kv1["missing"] += 1; continue
        a = load_one("parts_checks", dict(r, cq=2.0, cl=1.0), L["deciding"])
        b = fs1grade.load_one("parts_checks", dict(r, cq=2.0, cl=1.0), L["deciding"])
        if a is None or b is None:
            kv1["missing"] += 1; continue
        kv1["n"] += 1
        for fld in ("t_fold", "J_min"):
            kv1["max_rel"] = max(kv1["max_rel"], relq(a[fld], b[fld]))
    ka["FS1_Kvisc_x2_files"] = kv1
    chk["KA"] = (ka["n"] == 1455 and ka["n_missing"] == 0 and ka["max_rel"] <= 1e-9 and ka["nstep_mismatch"] == 0
                 and ka["class_mismatch"] == 0 and ka["FS1_bracket_from_FS2"] == fs1_br
                 and kv1["n"] == 40 and kv1["missing"] == 0 and kv1["max_rel"] <= 1e-9)
    out["KA"] = ka
    log(f"KA {'PASS' if chk['KA'] else 'FAIL'} {json.dumps(ka, default=str)}")

    # K0: core = numpy reference, N 500, t_fold (or J_min) and every level time
    soft = [r for r in rows if r["kind"] == "soft" and r["model"] == "v3s"][0]
    clk = [r for r in rows if r["kind"] == "clock_only" and r["model"] == "AC2q"][0]
    phx = max([r for r in rows if r["kind"] == "phantom" and r["model"] == "AC2q"], key=lambda r: r["gam"] * r["Pi0"])
    k0 = {}
    for nm, r, tm in (("soft_v3s_1", soft, 6.0), ("clock_AC2q_1", clk, 6.0), ("phantom_AC2q_max", phx, 1.5)):
        a = fs2.run(500, r["M1"], r["Pi0"], r["s2_use"], r["gam"], tmax=tm)
        b = fs2_ref.run(500, r["M1"], r["Pi0"], r["s2_use"], r["gam"], tmax=tm, levels=fs2.LEVELS)
        qa = a["t_fold"] if a["t_fold"] is not None else a["J_min"]; qb = b["t_fold"] if b["t_fold"] is not None else b["J_min"]
        lv = max(relq(x, y) for x, y in zip(a["t_lev"], b["t_lev"]))
        k0[nm] = dict(core=qa, ref=qb, rel=relq(qa, qb), level_max_rel=lv, t_reg_core=fs2.t_reg(a), t_reg_ref=b["t_lev"][fs2.IREG])
    chk["K0"] = all(v["rel"] <= 1e-9 and v["level_max_rel"] <= 1e-9 for v in k0.values()); out["K0"] = k0
    log(f"K0 {'PASS' if chk['K0'] else 'FAIL'} {k0}")

    # K1: zero charge vs independent two-label integration, at J_reg (graded) and J_thr (FS1's)
    N = 2000; i1 = int((1 - ac10.EDGE) * N); c = i1 - 1
    rr = fs2.run(N, 1.0, 0.0, 0.0, 0.0)
    q = np.linspace(ac10.X0[0], ac10.X0[1], N + 1); dq = q[1] - q[0]

    def pair_level(sheet, level):
        def f(t, y):
            return np.concatenate([y[2:], -0.5 * sheet * erf(y[:2] / (math.sqrt(2) * ac10.WB))])
        def ev(t, y):
            return (y[1] - y[0]) / dq - level
        ev.terminal = True; ev.direction = -1
        sp = solve_ivp(f, (0, ac10.TMAX), [q[c], q[c + 1], 1.0, 1.0], method="DOP853", rtol=1e-12, atol=1e-14,
                       events=ev, dense_output=True)
        tp = float(sp.t_events[0][0]); xm = lambda t: 0.5 * (sp.sol(t)[0] + sp.sol(t)[1])
        tc = brentq(xm, 0, tp) if xm(tp) > 0 else None
        vc = 0.5 * (sp.sol(tc)[2] + sp.sol(tc)[3]) if tc is not None else None
        return tp, tc, vc
    tpr, _, _ = pair_level(1.0, ac10.JREG); tpt, tct, vct = pair_level(1.0, ac10.JTHR)
    chk["K1"] = (abs(fs2.t_reg(rr) - tpr) <= 1e-6 and abs(rr["t_fold"] - tpt) <= 1e-6 and abs((tpt - tct) / vct - 1) <= 0.02)
    out["K1"] = dict(t_reg_coupled=fs2.t_reg(rr), t_reg_pair=tpr, t_fold_coupled=rr["t_fold"], t_fold_pair=tpt,
                     delay_over_vcross=(tpt - tct) / vct, reg_cell=rr["cell_lev"][fs2.IREG], front_cell=c)
    log(f"K1 {'PASS' if chk['K1'] else 'FAIL'} {out['K1']}")

    # K2/K3: FS1's stress-row checks with FS2's core and FS1's lines
    rho_b = lambda x: np.exp(-x ** 2 / (2 * ac10.WB ** 2)) / (math.sqrt(2 * math.pi) * ac10.WB)
    levels = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.001)
    kk = {}
    for row in fs2.stress_rows():
        Pi0, s2 = row["Pi0"], row["s2_use"]; thr = 1 / math.sqrt(2) if row["kind"] == "stress_A1" else 1.0
        o = fs2.run(N, 1.0, Pi0, s2, 0.0, rec_node=c)
        R = o["rec"]; tt = R[:, 0]; Jn = (R[:, 2] - R[:, 1]) / dq; vnode = R[:, 3]; xmid = 0.5 * (R[:, 1] + R[:, 2])
        neg = np.nonzero(vnode < 0)[0]
        t_turn = float(tt[neg[0]]) if len(neg) else float(tt[-1])
        m = tt <= t_turn
        k = np.nonzero(xmid[m] >= 0)[0][0]
        tcr = float(np.interp(0.0, xmid[k - 1:k + 1], tt[k - 1:k + 1]))
        vcr = float(np.interp(tcr, tt, 0.5 * (R[:, 3] + R[:, 4])))
        xm = lambda t: float(np.interp(t, tt, xmid))
        f = lambda t, y: [y[1], -rho_b(xm(t)) * y[0] + (Pi0 - s2 * y[0])]
        t_ext = t_turn + (0.2 if o["status"] == 1 else 0.0)
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

    # ladders (graded, J_reg)
    LAD = {}
    for r in rows:
        L = ladder_of(r)
        if L is None:
            missing.append((r["kind"], r["model"], r["foot"], r["r_kpc"]))
        LAD[fs2.key(r)] = L

    # MUTATEs
    mrows = {r["kind"]: r for r in fs2.main_rows() if r["kind"].startswith("MUTATE")}
    mm = {}
    LA = ladder_of(mrows["MUTATE_A_repulsive"]); LB = ladder_of(mrows["MUTATE_B_mach0.3"])
    mm["A"] = dict(classes=[fs2.klass(x) for x in LA["rungs"]] if LA else None, J_min=[x["J_min"] for x in LA["rungs"]] if LA else None)
    chk["MUTATE_A"] = bool(LA) and all(fs2.klass(x) == "REGULAR" for x in LA["rungs"])
    mm["B"] = dict(converged=LB["converged"] if LB else None, classes=[fs2.klass(x) for x in LB["rungs"]] if LB else None,
                   J_min=[x["J_min"] for x in LB["rungs"]] if LB else None)
    chk["MUTATE_B"] = bool(LB) and LB["converged"] and LB["label"] == "REGULAR"
    LP1 = ladder_of(mrows["MUTATE_P1_zero_charge"]); LK1 = ladder_of([r for r in fs2.main_rows() if r["kind"] == "K1_zero_charge"][0])
    tp3, _, _ = pair_level(1.03, ac10.JREG)
    p1n = fs2.t_reg([x for x in LP1["rungs"] if x["N"] == 2000][0]) if LP1 else None
    po1 = pair_outcome(LP1, LK1)
    mm["P1"] = dict(t_reg_planted_N2000=p1n, t_reg_pair_pred=tp3, abs_diff=abs(p1n - tp3) if p1n else None, pair=po1)
    chk["MUTATE_P1"] = p1n is not None and abs(p1n - tp3) <= 1e-6 and po1["outcome"] == "DIFF-TIME"
    p2 = first_phantom_reach()
    if p2 is not None:
        po2 = pair_outcome(ladder_of(p2_row(p2), "parts_checks"), LAD[fs2.key(p2)])
        mm["P2"] = dict(row=dict(foot=p2["foot"], r=p2["r_kpc"], w=p2["w_kms"], M1=p2["M1"], L=p2["Lstar_pc"]), pair=po2)
        chk["MUTATE_P2"] = po2["outcome"] in ("DIFF-TIME", "DIFF-LABEL")
    else:
        mm["P2"] = None; chk["MUTATE_P2"] = False
    po3 = pair_outcome(ladder_of(mrows["MUTATE_P3_clock"]), LAD[fs2.key(clk)])
    mm["P3"] = dict(pair=po3); chk["MUTATE_P3"] = po3["outcome"] in ("DIFF-TIME", "DIFF-LABEL")
    out["MUTATE"] = mm; log(f"MUTATE {json.dumps(mm, default=str)}")

    # K-visc (x2, x0.5) and K-dt on the sample, graded at J_reg
    samp = fs2.sample_rows(); res = {nm: [] for nm, _ in fs2.VARIANTS}
    for r in samp:
        L = LAD[fs2.key(r)]
        tag = dict(foot=r["foot"], r_kpc=r["r_kpc"], kind=r["kind"], model=r["model"])
        for nm, kw in fs2.VARIANTS:
            if L is None or not L["deciding"]:
                res[nm].append(dict(tag, ok=False, why="no deciding rung")); continue
            v = load_one("parts_checks", dict(r, _chk=nm, **kw), L["deciding"])
            res[nm].append(dict(tag, N=L["deciding"], **variant_ok(L["dec"], v)))
    chk["K_visc"] = all(x["ok"] for x in res["visc2"] + res["visc05"]) and len(res["visc2"]) == len(res["visc05"]) == 100
    chk["K_dt"] = all(x["ok"] for x in res["dt"]) and len(res["dt"]) == 100
    out["K_visc_x2"] = res["visc2"]; out["K_visc_x05"] = res["visc05"]; out["K_dt"] = res["dt"]
    summ = {}
    for nm in res:
        s = dict(max_rel=max([x.get("rel") or 0 for x in res[nm]], default=None), n_fail=sum(not x["ok"] for x in res[nm]),
                 class_changes=sum(x.get("base") != x.get("var") for x in res[nm]))
        lvmax = {}
        for l in fs2.LEVELS:
            vals = [x["level_shift"][l] for x in res[nm] if "level_shift" in x and x["level_shift"][l] is not None]
            lvmax[l] = max(vals) if vals else None
        s["level_max_shift_reported"] = lvmax
        s["Jthr_max_shift_reported"] = max([x.get("Jthr_shift") or 0 for x in res[nm]], default=None)
        s["Jthr_class_changes_reported"] = sum(1 for x in res[nm] if "Jthr_class" in x and x["Jthr_class"][0] != x["Jthr_class"][1])
        summ[nm] = s
    # reported: pair ratio r shift under the variants (J_reg and J_thr)
    pr = {nm: dict(reg=[], thr=[]) for nm, _ in fs2.VARIANTS}
    for a in fs2.sample_ac2q():
        b = fs2.twin(a); La, Lb = LAD[fs2.key(a)], LAD[fs2.key(b)]
        if not (La and Lb and La["deciding"] and Lb["deciding"]):
            continue
        for nm, kw in fs2.VARIANTS:
            va = load_one("parts_checks", dict(a, _chk=nm, **kw), La["deciding"]); vb = load_one("parts_checks", dict(b, _chk=nm, **kw), Lb["deciding"])
            if not (va and vb):
                continue
            if fs2.t_reg(La["dec"]) and fs2.t_reg(Lb["dec"]) and fs2.t_reg(va) and fs2.t_reg(vb):
                pr[nm]["reg"].append(abs((fs2.t_reg(va) / fs2.t_reg(vb)) / (fs2.t_reg(La["dec"]) / fs2.t_reg(Lb["dec"])) - 1))
            if La["dec"]["t_fold"] and Lb["dec"]["t_fold"] and va["t_fold"] and vb["t_fold"]:
                pr[nm]["thr"].append(abs((va["t_fold"] / vb["t_fold"]) / (La["dec"]["t_fold"] / Lb["dec"]["t_fold"]) - 1))
    for nm in pr:
        summ[nm]["pair_ratio_shift_reported"] = dict(reg=max(pr[nm]["reg"], default=None), thr=max(pr[nm]["thr"], default=None))
    out["variant_summary"] = summ
    log(f"K-visc {'PASS' if chk['K_visc'] else 'FAIL'}; K-dt {'PASS' if chk['K_dt'] else 'FAIL'}; {json.dumps(summ, default=str)}")

    # pairs (graded at J_reg)
    pairs = []; tab = {}; xmin = 1.0; shock_reg = {}
    for a in [r for r in rows if r["model"] == "AC2q"]:
        b = fs2.twin(a); La, Lb = LAD[fs2.key(a)], LAD[fs2.key(b)]
        po = pair_outcome(La, Lb)
        L1a, L1b = LAD1[fs2.key(a)], LAD1[fs2.key(b)]
        po1 = fs1grade.pair_outcome(L1a, L1b)
        lvr = {}
        if La and Lb:
            for i, l in enumerate(fs2.LEVELS):
                x, y = La["dec"]["t_lev"][i], Lb["dec"]["t_lev"][i]
                lvr[l] = x / y if (x and y) else None
        ent = dict(foot=a["foot"], r_kpc=a["r_kpc"], kind=a["kind"], w=a["w_kms"], M1=a["M1"], L=a["Lstar_pc"],
                   AC2q=La["label"] if La else "MISSING", v3s=Lb["label"] if Lb else "MISSING",
                   t_reg_AC2q=fs2.t_reg(La["dec"]) if La else None, t_reg_v3s=fs2.t_reg(Lb["dec"]) if Lb else None,
                   Jmin_AC2q=La["dec"]["J_min"] if La else None, Jmin_v3s=Lb["dec"]["J_min"] if Lb else None,
                   e_AC2q=La["e"] if La else None, e_v3s=Lb["e"] if Lb else None,
                   N_AC2q=La["deciding"] if La else None, N_v3s=Lb["deciding"] if Lb else None,
                   shock_at_reg_AC2q=La["dec"]["shock_lev"][fs2.IREG] if La else None,
                   shock_at_reg_v3s=Lb["dec"]["shock_lev"][fs2.IREG] if Lb else None,
                   FS1_reading=dict(outcome=po1["outcome"], sub=po1.get("sub"), r=po1["r"]), r_by_level=lvr, **po)
        if po["outcome"].startswith("DIFF"):
            ka_ = load_one("parts_checks", dict(a, edge_b=1, _chk="K4"), La["deciding"])
            kb_ = load_one("parts_checks", dict(b, edge_b=1, _chk="K4"), Lb["deciding"])
            if ka_ and kb_:
                fa = dict(converged=True, label=fs2.klass(ka_), e=La["e"], dec=ka_); fb = dict(converged=True, label=fs2.klass(kb_), e=Lb["e"], dec=kb_)
                ent["K4_Eb"] = pair_outcome(fa, fb)
            else:
                ent["K4_Eb"] = "missing"
        pairs.append(ent)
        k = f"{a['foot']}|{a['kind']}|{po['outcome']}{'/' + po['sub'] if 'sub' in po else ''}|AC2q {ent['AC2q']}|v3s {ent['v3s']}"
        tab[k] = tab.get(k, 0) + 1
        for L, rw in ((La, a), (Lb, b)):
            if L:
                xmin = min(xmin, 1 - (max(x["v_max"] for x in L["rungs"]) * rw["w_kms"] * 1e3 / CL) ** 2)
                if L["converged"] and L["label"] == "REACH":
                    kk2 = f"{rw['model']}|{rw['kind']}|shock_at_reg={L['dec']['shock_lev'][fs2.IREG]}"
                    shock_reg[kk2] = shock_reg.get(kk2, 0) + 1
    chk["X_pos"] = xmin > 0.99
    out.update(table=tab, X_over_Xbg_min=xmin, shock_at_reg_counts=shock_reg, pairs=pairs, missing_rows=missing)
    for k in sorted(tab):
        log(f"  {k}: {tab[k]}")
    log(f"shock-at-J_reg counts {shock_reg}; X min {xmin}")

    oc = [p["outcome"] for p in pairs]
    diffs = [p for p in pairs if p["outcome"].startswith("DIFF")]
    checks = all(chk.values())
    if missing or len(pairs) != 240:
        v = "INCOMPLETE (rows missing; not a verdict)"
    elif not checks:
        v = "NO VERDICT"
    elif diffs:
        v = "DIFFERS"
    elif all(o in ("SAME-REACH", "SAME-REGULAR") for o in oc):
        v = f"FOLDS-SAME-AS-V3S ({oc.count('SAME-REGULAR')} pairs regular in both)"
    else:
        v = "NO VERDICT"
    rs = [p["r"] for p in pairs if p["r"] is not None]
    out["bracket"] = dict(counts={o: oc.count(o) for o in sorted(set(oc))}, r_range=[min(rs), max(rs)] if rs else None,
                          Jmin_open=[(p["Jmin_AC2q"], p["Jmin_v3s"]) for p in pairs if p["outcome"] == "OPEN"])
    by = {}
    for p in diffs:
        kx = f"{p['foot']}|{p['kind']}|{p['outcome']}/{p.get('sub')}|K4 E-b {p['K4_Eb']['outcome'] if isinstance(p.get('K4_Eb'), dict) else p.get('K4_Eb')}"
        by[kx] = by.get(kx, 0) + 1
    rdiff = [p["r"] for p in diffs if p["r"] is not None]
    out["diff_summary"] = by; out["diff_r_range"] = [min(rdiff), max(rdiff)] if rdiff else None
    fs1rep = {}
    for p in pairs:
        kx = f"{p['kind']}|{p['FS1_reading']['outcome']}"
        fs1rep[kx] = fs1rep.get(kx, 0) + 1
    out["FS1_reading_reported"] = fs1rep
    out["checks"] = chk; out["verdict"] = v; out["criteria"] = "1a686ed9a2"
    log(f"bracket {out['bracket']['counts']} r range {out['bracket']['r_range']}")
    log(f"DIFF summary {by}; DIFF r range {out['diff_r_range']}")
    log(f"FS1 J_thr reading (reported) {fs1rep}")
    log(f"checks {chk}\nVERDICT (frozen): {v}")
    json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
