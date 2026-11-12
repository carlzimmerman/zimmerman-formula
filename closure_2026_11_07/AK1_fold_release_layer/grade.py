#!/usr/bin/env python3
"""AK1 grade: frozen lines of CRITERIA.md (origin c61447452a / local 8ed1798939) + reported addendum A1 (858f4ea326).
Writes GRADE.json; print to grade.out. Run from the repo root:
  python3 closure_2026_11_07/AK1_fold_release_layer/grade.py > closure_2026_11_07/AK1_fold_release_layer/grade.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
_s = importlib.util.spec_from_file_location("ak1", os.path.join(HERE, "ak1.py"))
ak1 = importlib.util.module_from_spec(_s); sys.modules["ak1"] = ak1; _s.loader.exec_module(ak1)
fs2, ac10 = ak1.fs2, ak1.ac10
KPC, CL = ak1.KPC, ak1.CL
log = lambda s: print(s, flush=True)
R_HOSTS = (73.0, 91.0, 156.0)


def ell_kpc(r):
    return r["w_kms"] * 1e3 * r["tau_f_s"] / KPC


def fs2_file(row, N):
    fn = os.path.join(fs2.HERE, "parts", f"{ak1.key(row)}_{N}.json")
    return json.load(open(fn)) if os.path.exists(fn) else None


def reading(row, o, k):
    s = o["snaps"][k]; w = row["w_kms"]; el = ell_kpc(row)
    return dict(vpost=s["vpost"] * w, Vmax=s["Vmax"] * w, fwhm_ell=s["fwhm"], fwhm_kpc=s["fwhm"] * el,
                R=s["fwhm"] * el / ak1.lam_crit(row["foot"]), W_ell=s["W"], W_kpc=s["W"] * el, t=s["t"])


def conv_v(a, b):
    return abs(b / a - 1) <= 1e-2 or abs(b - a) <= 5.0 if a > 0 else abs(b - a) <= 5.0


def conv_len(a_ell, b_ell):
    return (a_ell > 0 and abs(b_ell / a_ell - 1) <= 0.1) or abs(b_ell - a_ell) <= 0.01


def slope(x, y):
    x = np.log(np.asarray(x)); y = np.log(np.asarray(y))
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 2 and np.ptp(x) > 0 else None


def boot(fn, n, B=2000, seed=12345):
    rng = np.random.default_rng(seed); vals = []
    for _ in range(B):
        idx = rng.integers(0, n, n); v = fn(idx)
        if v is not None and np.isfinite(v):
            vals.append(v)
    return [float(np.percentile(vals, 16)), float(np.percentile(vals, 84))] if vals else None


def main():
    out, chk = {}, {}
    rows = ac10.physical_rows()

    # KA: FS2's fold times to 0 (480 rows x N 4000/8000)
    ka = dict(n=0, missing=0, mismatch=[])
    for r in rows:
        for N in ak1.RUNGS:
            a = ak1.load(r, N); b = fs2_file(r, N)
            if a is None or b is None:
                ka["missing"] += 1; continue
            ka["n"] += 1
            same = (a["t_lev"][ak1.IREG] == b["t_lev"][ak1.IREG] and a["t_fold"] == b["t_fold"]
                    and a["t_fold_all"] == b["t_fold_all"] and a["J_min"] == b["J_min"] and a["J_min_all"] == b["J_min_all"]
                    and (a["nstep_event"] if b["t_fold"] is not None else a["nstep_end"]) == b["nstep"])
            if not same:
                ka["mismatch"].append((r["foot"], r["kind"], r["model"], r["r_kpc"], N))
    chk["KA"] = ka["n"] == 960 and ka["missing"] == 0 and not ka["mismatch"]
    out["KA"] = ka; log(f"KA {'PASS' if chk['KA'] else 'FAIL'} n={ka['n']} missing={ka['missing']} mismatches={len(ka['mismatch'])}")

    # MUTATEs (N 8000, both snapshots)
    mv, mv2 = ak1.mutate_rows(); c1 = ak1.clock1()
    m = {}
    o = ak1.load(mv, 8000); m["V"] = [reading(mv, o, k)["Vmax"] for k in range(2)] if o else None
    chk["MUTATE_V"] = bool(m["V"]) and all(500 <= v <= 650 for v in m["V"])
    o = ak1.load(mv2, 8000); m["V2_vpost"] = [reading(mv2, o, k)["vpost"] for k in range(2)] if o else None
    chk["MUTATE_V2"] = bool(m["V2_vpost"]) and all(v >= 500 for v in m["V2_vpost"])
    o = ak1.load(c1, 8000)
    m["null"] = [dict(Vmax=reading(c1, o, k)["Vmax"], vpost=reading(c1, o, k)["vpost"]) for k in range(2)] if o else None
    chk["MUTATE_0"] = bool(m["null"]) and all(x["Vmax"] < 500 and x["vpost"] < 500 for x in m["null"])
    out["MUTATE"] = m; log(f"MUTATE {m} -> V {chk['MUTATE_V']} V2 {chk['MUTATE_V2']} null {chk['MUTATE_0']}")

    # K-visc on graded observables
    kv = []
    for rv in ak1.kvisc_rows():
        base = {k: v for k, v in rv.items() if k not in ("cq", "cl", "_chk")}
        a = ak1.load(base, 8000); b = ak1.load(rv, 8000)
        if not (a and b):
            kv.append(dict(ok=False, why="missing")); continue
        ok = True; worst = {}
        for k in range(2):
            ra, rb = reading(base, a, k), reading(base, b, k)
            o1 = conv_v(ra["vpost"], rb["vpost"]) and (abs(rb["Vmax"] / ra["Vmax"] - 1) <= 1e-2)
            o2 = conv_len(ra["fwhm_ell"], rb["fwhm_ell"]) and conv_len(ra["W_ell"], rb["W_ell"])
            ok = ok and o1 and o2
            worst[k] = dict(vpost=(ra["vpost"], rb["vpost"]), Vmax=abs(rb["Vmax"] / ra["Vmax"] - 1),
                            fwhm_ell=(ra["fwhm_ell"], rb["fwhm_ell"]), W_ell=(ra["W_ell"], rb["W_ell"]))
        kv.append(dict(foot=base["foot"], kind=base["kind"], r_kpc=base["r_kpc"], ok=ok, d=worst))
    chk["K_visc"] = len(kv) == 40 and all(x["ok"] for x in kv)
    out["K_visc"] = kv; log(f"K-visc {'PASS' if chk['K_visc'] else 'FAIL'} n={len(kv)} fails={sum(not x['ok'] for x in kv)}")

    # graded rows
    graded = [r for r in rows if r["model"] == "AC2q" and r["kind"] in ("clock_only", "phantom") and ak1.low_L(r)]
    G = []; nconv = dict(v=0, R=0)
    for r in graded:
        a, b = ak1.load(r, 4000), ak1.load(r, 8000)
        if not (a and b):
            G.append(dict(foot=r["foot"], kind=r["kind"], missing=True)); continue
        ent = dict(foot=r["foot"], kind=r["kind"], r_kpc=r["r_kpc"], w=r["w_kms"], M1=r["M1"], ell_kpc=ell_kpc(r),
                   v_f=b["v_f"] * r["w_kms"], Pi_min=b["Pi_min"], s2=r["s2_use"], Pi0=r["Pi0"], snaps=[])
        for k in range(2):
            ra, rb = reading(r, a, k), reading(r, b, k)
            cv = conv_v(ra["vpost"], rb["vpost"]); cR = conv_len(ra["fwhm_ell"], rb["fwhm_ell"])
            Rg = r["r_kpc"] in R_HOSTS
            ent["snaps"].append(dict(N8000=rb, N4000=ra, conv_v=cv, conv_R=cR, R_graded=Rg,
                                     v_in=500 <= rb["vpost"] <= 650, R_in=0.5 <= rb["R"] <= 2.0))
            nconv["v"] += cv; nconv["R"] += cR
        G.append(ent)
    out["graded"] = G
    refute = [(e["foot"], e["kind"], e["r_kpc"], k, "v_post" if (s["conv_v"] and not s["v_in"]) else "R_delta")
              for e in G if "snaps" in e for k, s in enumerate(e["snaps"])
              if (s["conv_v"] and not s["v_in"]) or (s["R_graded"] and s["conv_R"] and not s["R_in"])]
    allin = all(s["conv_v"] and s["v_in"] and (not s["R_graded"] or (s["conv_R"] and s["R_in"]))
                for e in G if "snaps" in e for s in e["snaps"]) and not any(e.get("missing") for e in G)
    # flatness |d ln vpost / d ln v_f| per footing (Delta 0.5, N 8000)
    flat = {}
    for f in ("canonical", "alt"):
        es = [e for e in G if e.get("foot") == f and "snaps" in e and e["snaps"][1]["N8000"]["vpost"] > 0]
        flat[f] = slope([e["v_f"] for e in es], [e["snaps"][1]["N8000"]["vpost"] for e in es])
    out["flatness_alpha_v_pooled"] = flat
    checks = all(chk.values())
    if not checks:
        v = "NO VERDICT (check failed)"
    elif refute:
        v = "REFUTED within the certified non-relativistic fold reduction"
    elif allin and all(x is not None and abs(x) <= 0.1 for x in flat.values()):
        v = "CONFIRMED"
    else:
        v = "NO VERDICT"
    out["refuting_readings_n"] = len(refute); out["refuting_examples"] = refute[:10]

    # summaries per footing / kind
    summ = {}
    for f in ("canonical", "alt"):
        for kd in ("clock_only", "phantom"):
            es = [e for e in G if e.get("foot") == f and e.get("kind") == kd and "snaps" in e]
            s1 = [e["snaps"][1]["N8000"] for e in es]
            summ[f"{f}|{kd}"] = dict(
                n=len(es), vpost_kms=[min(x["vpost"] for x in s1), max(x["vpost"] for x in s1)],
                Vmax_kms=[min(x["Vmax"] for x in s1), max(x["Vmax"] for x in s1)],
                R_delta=[min(x["R"] for x in s1), max(x["R"] for x in s1)],
                fwhm_pc=[min(x["fwhm_kpc"] for x in s1) * 1e3, max(x["fwhm_kpc"] for x in s1) * 1e3],
                W_pc=[min(x["W_kpc"] for x in s1) * 1e3, max(x["W_kpc"] for x in s1) * 1e3],
                v_f_kms=[min(e["v_f"] for e in es), max(e["v_f"] for e in es)],
                slope_vpost_vs_vf=slope([e["v_f"] for e in es if e["snaps"][1]["N8000"]["vpost"] > 0],
                                        [e["snaps"][1]["N8000"]["vpost"] for e in es if e["snaps"][1]["N8000"]["vpost"] > 0]),
                slope_Vmax_vs_vf=slope([e["v_f"] for e in es], [x["Vmax"] for x in s1]),
                slope_fwhm_vs_ell=slope([e["ell_kpc"] for e in es if e["snaps"][1]["N8000"]["fwhm_kpc"] > 0],
                                        [e["snaps"][1]["N8000"]["fwhm_kpc"] for e in es if e["snaps"][1]["N8000"]["fwhm_kpc"] > 0]),
                slope_W_vs_ell=slope([e["ell_kpc"] for e in es if e["snaps"][1]["N8000"]["W_kpc"] > 0],
                                     [e["snaps"][1]["N8000"]["W_kpc"] for e in es if e["snaps"][1]["N8000"]["W_kpc"] > 0]),
                Pi_min_over_ref=min((e["Pi_min"] / (e["s2"] if kd == "clock_only" else e["Pi0"])) for e in es if e["Pi_min"]),
                n_conv_v=sum(e["snaps"][k]["conv_v"] for e in es for k in range(2)),
                n_conv_R=sum(e["snaps"][k]["conv_R"] for e in es for k in range(2)))
    out["summary"] = summ
    for k_, s_ in summ.items():
        log(f"{k_}: {json.dumps(s_, default=float)}")

    # identity predictions I1 (L* x2 and 90 pc ratios) and addendum A1 exponents
    def triple(r):
        hi = [x for x in rows if all(x[q] == r[q] for q in ("foot", "r_kpc", "w_kms", "M1", "kind", "model")) and x["Lstar_pc"] == 90.0]
        return r, ak1.lx2(r), hi[0] if hi else None
    i1 = {}; A1 = {}
    for f in ("canonical", "alt"):
        rat2 = dict(vpost=[], Vmax=[], fwhm=[], W=[]); rat90 = dict(vpost=[], Vmax=[], fwhm=[], W=[]); aL = []; aLW = []
        for r in [x for x in graded if x["foot"] == f]:
            lo, x2, hi = triple(r)
            o = [ak1.load(z, 8000) if z else None for z in (lo, x2, hi)]
            if not all(o):
                continue
            rd = [reading(z, oo, 1) for z, oo in zip((lo, x2, hi), o)]
            for nm, key_ in (("vpost", "vpost"), ("Vmax", "Vmax"), ("fwhm", "fwhm_kpc"), ("W", "W_kpc")):
                if rd[0][key_] > 0:
                    rat2[nm].append(rd[1][key_] / rd[0][key_]); rat90[nm].append(rd[2][key_] / rd[0][key_])
            Ls = [lo["Lstar_pc"], x2["Lstar_pc"], hi["Lstar_pc"]]
            if all(z["fwhm_kpc"] > 0 for z in rd):
                aL.append(slope(Ls, [z["fwhm_kpc"] for z in rd]))
            if all(z["W_kpc"] > 0 for z in rd):
                aLW.append(slope(Ls, [z["W_kpc"] for z in rd]))
        i1[f] = {f"x2_{k}": [min(v), float(np.median(v)), max(v)] if v else None for k, v in rat2.items()}
        i1[f].update({f"90pc_{k}": [min(v), float(np.median(v)), max(v)] if v else None for k, v in rat90.items()})
        aL = np.array([x for x in aL if x is not None]); aLW = np.array([x for x in aLW if x is not None])
        es = [e for e in G if e.get("foot") == f and "snaps" in e and e["snaps"][1]["N8000"]["vpost"] > 0]
        xs = np.array([e["v_f"] for e in es]); ys = np.array([e["snaps"][1]["N8000"]["vpost"] for e in es])
        av = slope(xs, ys)
        A1[f] = dict(alpha_L_fwhm=float(np.median(aL)) if len(aL) else None,
                     alpha_L_fwhm_CI=boot(lambda idx: float(np.median(aL[idx])), len(aL)) if len(aL) else None,
                     alpha_L_W=float(np.median(aLW)) if len(aLW) else None,
                     alpha_L_W_CI=boot(lambda idx: float(np.median(aLW[idx])), len(aLW)) if len(aLW) else None,
                     n_L=int(len(aL)), alpha_v=av,
                     alpha_v_CI=boot(lambda idx: slope(xs[idx], ys[idx]), len(xs)), n_v=int(len(xs)),
                     n_dropped_v=sum(1 for e in G if e.get("foot") == f and "snaps" in e) - int(len(xs)))
        mins = [e["Pi_min"] / (e["s2"] if e["kind"] == "clock_only" else e["Pi0"]) for e in G if e.get("foot") == f and e.get("Pi_min")]
        A1[f]["min_Pi_over_ref"] = min(mins)
        A1[f]["alpha_M"] = 0.0 if min(mins) >= 0.5 else "not computed: the blend region is visited"
    out["I1"] = i1; out["A1"] = A1
    log(f"I1 (identity predicts x2: V 1.260, width 1.587; 90 pc: V 1.607/1.581): {json.dumps(i1, default=float)}")
    log(f"A1 exponents (I: aL 1, av>0; II: 2/3, 2/3, aM~0; III: 2/3, 0, 1): {json.dumps(A1, default=float)}")

    # Q - 1 reached (X/X_bg) over graded runs
    xm = max((ak1.load(r, 8000)["v_max_run"] * r["w_kms"] * 1e3 / CL) ** 2 for r in graded if ak1.load(r, 8000))
    out["max_1_minus_X_over_Xbg"] = xm
    out["lambda_crit_kpc"] = {f: ak1.lam_crit(f) for f in ("canonical", "alt")}
    out["v_claim_kms"] = {f: ak1.v_claim(f) for f in ("canonical", "alt")}
    out["R_vs_protocol_2p09_2p25"] = {f: [summ[f"{f}|{kd}"]["fwhm_pc"][1] / 1e3 / {"canonical": 2.09, "alt": 2.25}[f]
                                          for kd in ("clock_only", "phantom")] for f in ("canonical", "alt")}
    out["checks"] = chk; out["verdict"] = v; out["criteria"] = "c61447452a (local 8ed1798939) + A1 858f4ea326"
    log(f"max (1 - X/X_bg) = {xm:.3e}; lambda_crit {out['lambda_crit_kpc']}; refuting readings {len(refute)}")
    log(f"checks {chk}\nVERDICT (frozen): {v}")
    # Addendum A2 (POST-RESULT, disclosed; never the label): MUTATE-V row re-run with t_max 60
    a2r = ak1.a2_rows()[0]; a2 = {}
    for N in ak1.RUNGS:
        o = ak1.load(a2r, N)
        a2[N] = None if o is None else dict(t_reg=o["t_lev"][ak1.IREG], v_max_run_kms=o["v_max_run"] * a2r["w_kms"],
                                            V_kms=[s["Vmax"] * a2r["w_kms"] if s["t"] >= 0 else None for s in o["snaps"]])
    o8 = a2[8000]
    a2pass = bool(o8) and all(v is not None and 500 <= v <= 650 for v in o8["V_kms"])
    out["A2_MUTATE_V"] = dict(criteria="7291797cb1 (post-result)", rungs=a2, passes=a2pass,
                              frozen_label_unchanged=v)
    log(f"A2 (post-result, not the label): MUTATE-V t_max 60 -> {a2} pass={a2pass}")
    out["criteria"] += " + A2 7291797cb1 (post-result)"
    json.dump(out, open(os.path.join(HERE, "GRADE.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
