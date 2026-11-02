#!/usr/bin/env python3
"""DF2: gate 1 against the dark fluid term's w, c_s(a), c_vis(a). RF5's code read-only, cells and work in this lane, DF2's patched CLASS. Modes: controls | screen I N | fit | grade | analytic. DF2_RUNMUT=1 for the MUTATE control, separate outputs. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, signal, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RF = os.path.join(RB, "RF5_growth_native_yardstick"); sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
MUT = os.environ.get("DF2_RUNMUT") == "1"; TAG = "_MUTATE" if MUT else ""
CELLS = os.path.join(HERE, "cells" + TAG); os.makedirs(CELLS, exist_ok=True)
src = open(os.path.join(RF, "rf5.py")).read(); a = 'HERE = os.path.dirname(os.path.abspath(__file__))'; assert src.count(a) == 1
src = src.replace(a, f'HERE = {RF!r}').replace('WORK = os.path.join(EXT, f"rf5_work{TAG}")', 'WORK = os.path.join(EXT, "df2_work' + TAG + '")').replace('CELLS = os.path.join(HERE, f"cells{TAG}")', f'CELLS = {CELLS!r}'); assert "df2_work" in src
R = {"__name__": "rf5ro", "__file__": os.path.join(RF, "rf5.py")}; exec(compile(src, "rf5.py", "exec"), R)
np = R["np"]; NM = R["NAMES"]; jw = R["jw"]; pv = R["pval"]; BAND = R["BAND"]
R["R1B"] = os.path.join(R["EXT"], "df2_build", "class_df2", "class")
def cparams(p, cell):
    wb, wc, th, lnA, ns_, tau, w0, wa = p
    return {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns_, "tau_reio": tau, "Omega_Lambda": 0.0, "w0_fld": w0, "wa_fld": wa, "cs2_fld": 1.0, "use_ppf": "yes", "omega_cdm": max(wc, 5e-4), "gauge": "newtonian"}
R["cparams"] = cparams
RF1 = json.load(open(os.path.join(RF, "cells", "R1_1000000.json"))); RFCH = json.load(open(os.path.join(RF, "cells", "R1_1000000_channels.json"))); SMIN = json.load(open(os.path.join(RF, "rf5_results.json")))["S_min"]
RHO0, RHOD = 3.3e-8, 0.05
def cell(name, fam, **e): return dict(name=name, fam=fam, kind="HF", env={k: float(v) for k, v in e.items()})
def grid():
    C = []
    for N, cs in ((2, (.25, .5, 1, 2, 4)), (1, (.5, 1, 2, 4, 8)), (0, (3, 10, 30, 100, 300)), (-1, (10, 30, 100, 300, 1000))):
        C += [cell(f"A_N{N}_c{c:g}", f"A_N{N}", DF2_CS0=c, DF2_N=N) for c in cs]
    for tag, lo, hi in (("z3000up", 3000, -1), ("z500_3000", 500, 3000), ("z50_500", 50, 500), ("z5_50", 5, 50), ("z0_5", -1, 5)):
        for c in (10, 100, 1000):
            e = dict(DF2_CS0=c, DF2_N=0)
            if lo > 0: e["DF2_ZLO"] = lo   # on above z = lo
            if hi > 0: e["DF2_ZHI"] = hi   # on below z = hi
            C.append(cell(f"B_{tag}_c{c}", f"B_{tag}", **e))
    C += [cell(f"S_c{c}", "S", DF2_CS0=c, DF2_N=0, DF2_ZHI=50) for c in (10, 30, 100, 300)]
    C += [cell(f"W_{w:+g}", "W", DF2_W=w) for w in (1e-3, -1e-3, 3e-3, -3e-3)]
    C += [cell(f"V_N0_c{c}", "V_N0", DF2_CV0=c, DF2_CVN=0) for c in (3, 10, 30, 100)] + [cell(f"V_N2_c{c:g}", "V_N2", DF2_CV0=c, DF2_CVN=2) for c in (.5, 2)]
    for g in (7 / 3, 5 / 3, 1.0, 2 / 3, 0.0):
        for s in (30, 100):
            C.append(cell(f"P_G{g:.3f}_s{s}", "P", DF2_CS0=s * (RHO0 / RHOD) ** ((g - 1) / 2), DF2_N=1.5 * (g - 1)))
    return C
ENVK = ["DF2_W", "DF2_CS0", "DF2_N", "DF2_ZLO", "DF2_ZHI", "DF2_CV0", "DF2_CVN", "DF2_MUT"]
def setenv(c):
    for k in ENVK: os.environ.pop(k, None)
    for k, v in c["env"].items(): os.environ[k] = repr(v)
class TO(Exception): pass
def _alarm(*a):
    for p in list(R["CHILD"]):
        try: p.kill()
        except Exception: pass
    raise TO()
signal.signal(signal.SIGALRM, _alarm)
def fixed_cut():
    q = json.load(open(os.path.join(RF, "cells", "shear_scale_cut.json"))); return R["load_shear"](), np.array(q["keep"], bool)
def evalp(L, c, p, A, Om_fix=None, S_K=None, tag="s"):
    setenv(c); o = R["run"](tag, c, p)
    if o is None: return dict(status="CLASS_FAIL", msg=c.get("class_fail", ["?"])[-1])
    q = L.parts(o, A); o2 = R["run"](tag + "p", c, p, pk=True, cmb=False)
    if o2 is None: return dict(status="PK_FAIL", plik=q["plik"], msg=c.get("class_fail", ["?"])[-1])
    Om = (p[0] + p[1]) / o["h"] ** 2; sh = R["shear_chi2"](S_K[0], S_K[1], o2, Om); k = o2["pk"][0.0][:, 0]
    return dict(status="OK", plik=q["plik"], Aprior=q.get("Aprior", 0.0), bao=q["bao"], sn=q["sn"], lowTT=q["lowTT"], shear=sh["chi2"], sigma8=o2["sigma8"], h=o["h"], S=q["plik"] + q.get("Aprior", 0.0) + q["bao"] + q["sn"] + sh["chi2"], k=k.tolist()[::4], P0=o2["pk"][0.0][:, 1].tolist()[::4], neg=bool(o2["pk"][0.0][:, 1].min() < 0))
PF = np.array([RF1["params"][n] for n in NM])
def controls():
    L = R["Lik"](); SK = fixed_cut(); ck = {}; off = cell("ctrl_off", "K")
    if not MUT:
        a = evalp(L, off, PF, RF1["A"], S_K=SK, tag="k0"); ck["K_rf5"] = dict(plik=a["plik"], rf5=RF1["chi2"]["plik"], bao=a["bao"], rf5_bao=RF1["chi2"]["bao"], sn=a["sn"], rf5_sn=RF1["chi2"]["sn"], shear=a["shear"], rf5_shear=RFCH["shear"]["chi2"], s8=a["sigma8"], rf5_s8=RFCH["sigma8"], S=a["S"], S_RF5=SMIN, passed=bool(abs(a["plik"] - RF1["chi2"]["plik"]) <= 1 and abs(a["bao"] - RF1["chi2"]["bao"]) <= 1 and abs(a["sn"] - RF1["chi2"]["sn"]) <= 1 and abs(a["shear"] - RFCH["shear"]["chi2"]) <= 1))
        b = evalp(L, cell("ctrl_zero", "K", DF2_W=0, DF2_CS0=0, DF2_CV0=0), PF, RF1["A"], S_K=SK, tag="k1"); ck["K_patch_zero"] = dict(d=b["plik"] - a["plik"], passed=bool(abs(b["plik"] - a["plik"]) <= 0.01))
        j = evalp(L, cell("ctrl_jeans", "K", DF2_CS0=30, DF2_N=0), PF, RF1["A"], S_K=SK, tag="k2"); kk = np.array(a["k"]); rt = np.array(j["P0"]) / np.array(a["P0"]); kh = float(kk[np.argmax(rt < .5)]) if (rt < .5).any() else None
        h = a["h"]; Om = (PF[0] + PF[1]) / h ** 2; kj = math.sqrt(1.5 * Om) * 100 / 30.; ck["K_jeans"] = dict(k_half_h_Mpc=kh, k_J_h_Mpc=kj, ratio=None if kh is None else kh / kj, plik=j["plik"], passed=bool(kh is not None and 1 / 3 <= kh / kj <= 3))
        jw(os.path.join(HERE, "df2_control_base.json"), a)
    else:
        m = cell("ctrl_mut", "K", DF2_CS0=30, DF2_N=0, DF2_MUT=1); j = cell("ctrl_mut0", "K", DF2_CS0=30, DF2_N=0)
        q0 = evalp(L, j, PF, RF1["A"], S_K=SK, tag="m0"); signal.alarm(1800)
        try: q1 = evalp(L, m, PF, RF1["A"], S_K=SK, tag="m1")
        except TO: q1 = dict(status="TIMEOUT")
        signal.alarm(0); ck["M_sign"] = dict(base=q0.get("plik"), mut=q1.get("plik"), status=q1["status"], passed=bool(q1["status"] != "OK" or abs(q1["plik"] - q0["plik"]) > 1))
    jw(os.path.join(CELLS, "checks.json"), ck); print(json.dumps(ck, indent=1, default=float), flush=True); return all(v["passed"] for v in ck.values())
def screen(i, n):
    L = R["Lik"](); SK = fixed_cut()
    for j, c in enumerate(grid()):
        if j % n != i: continue
        p = os.path.join(CELLS, c["name"] + "_scr.json")
        if os.path.exists(p): continue
        signal.alarm(1800)
        try: r = evalp(L, c, PF, RF1["A"], S_K=SK)
        except TO: r = dict(status="TIMEOUT")
        signal.alarm(0); r.update(cell=c["name"], fam=c["fam"], env=c["env"]); jw(p, r)
        print(c["name"], r["status"], None if r["status"] != "OK" else round(r["S"] - SMIN, 1), flush=True)
def scr(c):
    p = os.path.join(CELLS, c["name"] + "_scr.json"); return json.load(open(p)) if os.path.exists(p) else None
def fitlist():
    G = grid(); fam = {}; out = []
    for c in G: fam.setdefault(c["fam"], []).append(c)
    for f, cs in fam.items():
        if f == "P":
            out += [c for c in cs if (scr(c) or {}).get("status") == "OK" and scr(c)["S"] - SMIN <= 2000]; continue
        if f == "W": out += cs; continue
        st = [(c, scr(c)) for c in cs]; last = -1
        for i, (c, r) in enumerate(st):
            if r and r.get("status") == "OK" and r["S"] - SMIN <= 25: last = i
        if last >= 0: out.append(st[last][0])
        if last + 1 < len(st): out.append(st[last + 1][0])
    return out
def fit(i=0, n=1):
    import time
    while any(scr(c) is None for c in grid()): time.sleep(60)   # the two screen jobs must both finish before the fit list is read
    L = R["Lik"](); SK = fixed_cut()
    for j, c in enumerate(fitlist()):
        if j % n != i: continue
        p = os.path.join(CELLS, c["name"] + "_fit.json")
        if os.path.exists(p): continue
        setenv(c); cc = {"name": c["name"], "kind": "HF"}
        rec = R["fit_cell"](L, cc, PF.copy(), RF1["A"], maxit=10); rec.update(cell=c["name"], fam=c["fam"], env=c["env"])
        if rec.get("status") == "OK":
            pp = np.array([rec["params"][x] for x in NM]); o = R["run"]("fp", cc, pp, pk=True, cmb=False)
            if o is not None:
                rec["Omega_m"] = (pp[0] + pp[1]) / rec["h"] ** 2; sh = R["shear_chi2"](SK[0], SK[1], o, rec["Omega_m"]); rec.update(shear=sh["chi2"], n_shear=sh["n"], sigma8_pk=o["sigma8"], k=o["pk"][0.0][:, 0].tolist()[::4], P0=o["pk"][0.0][:, 1].tolist()[::4])
        jw(p, rec); print(c["name"], rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("converged"), flush=True)
def grade():
    out = []; res = dict(rows={})
    def P(s=""): print(s, flush=True); out.append(str(s))
    P(f"DF2 gate 1 map, S_min {SMIN:.2f}, line S - S_min <= 25. Screen = RF5's parameters, never a pass. kappa = 1/2 FITTED. Not theory closed.")
    ck = json.load(open(os.path.join(CELLS, "checks.json"))); P("checks: " + ", ".join(f"{k} {v['passed']}" for k, v in ck.items()))
    base = json.load(open(os.path.join(HERE, "df2_control_base.json"))); kk = np.array(base["k"]); PB = np.array(base["P0"]); labP = []
    for c in grid():
        s = scr(c); fp = os.path.join(CELLS, c["name"] + "_fit.json"); f = json.load(open(fp)) if os.path.exists(fp) else None; w = dict(fam=c["fam"], env=c["env"], screen=None, fit=None)
        if s: w["screen"] = {k: s.get(k) for k in ("status", "plik", "shear", "sigma8", "S")}
        line = f"{c['name']:22s} "
        if not s: line += "no screen"
        elif s["status"] != "OK": line += f"screen {s['status']}"
        else:
            rt = np.array(s["P0"]) / PB; kh = float(kk[np.argmax(rt < .5)]) if (rt < .5).any() else None; w["screen"]["k_half"] = kh
            line += f"screen S-Smin {s['S'] - SMIN:9.1f} plik {s['plik']:9.1f} s8 {s['sigma8']:.3f} k_half {kh if kh is None else round(kh, 3)}"
        if f:
            if f.get("status") != "OK" or "shear" not in f: line += f" | fit {f.get('status')} {str(f.get('msg'))[:50]}"; w["fit"] = dict(status="UNDETERMINED")
            else:
                ch = f["chi2"]; Sf = ch["plik"] + ch["Aprior"] + ch["bao"] + ch["sn"] + f["shear"]; g = dict(CMB=pv(ch["plik"], 605) >= 1e-3, BAO=pv(ch["bao"], 13) >= 1e-3, SN=pv(ch["sn"], ch["n_sn"] - 1) >= 1e-3, A0=all(BAND[z][0] <= f["sqrtX"].get(str(z), -1) <= BAND[z][1] for z in BAND), SHEAR=pv(f["shear"], f["n_shear"] - 1) >= 1e-3, S=Sf - SMIN <= 25); ok = bool(all(g.values()) and f["converged"])
                w["fit"] = dict(status="OK", S_minus=Sf - SMIN, plik=ch["plik"], bao=ch["bao"], shear=f["shear"], sigma8=f["sigma8_pk"], h=f["h"], omega_f=f["params"]["omega_c"], gates=g, converged=f["converged"], passed=ok)
                line += f" | FIT S-Smin {Sf - SMIN:.1f} plik {ch['plik']:.1f} s8 {f['sigma8_pk']:.3f} conv {f['converged']} {'PASS' if ok else 'FAIL ' + str([k for k, x in g.items() if not x])}"
        P(line); res["rows"][c["name"]] = w
    Pr = {k: v for k, v in res["rows"].items() if v["fam"] == "P"}; npass = [k for k, v in Pr.items() if (v["fit"] or {}).get("passed")]; unk = [k for k, v in Pr.items() if not v["screen"] or v["screen"].get("status") != "OK" or (v["fit"] is not None and v["fit"]["status"] != "OK") or (v["screen"]["S"] - SMIN <= 2000 and v["fit"] is None)]
    res["P_pass"] = npass; res["P_unknown"] = unk; lab = f"DENSITY KEY PASSES GATE 1 AT {npass}" if npass else ("DENSITY KEY FAILS GATE 1" if not unk else f"NOT DETERMINED; unread {unk}"); res["label"] = lab; P(f"\nP label: {lab}")
    jw(os.path.join(HERE, "df2_results.json"), res); open(os.path.join(HERE, "df2.out"), "w").write("\n".join(out) + "\n")
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "controls": sys.exit(0 if controls() else 1)
    if m == "screen": screen(int(sys.argv[2]), int(sys.argv[3]))
    if m == "fit": fit(int(sys.argv[2]), int(sys.argv[3]))
    if m == "grade": grade()
