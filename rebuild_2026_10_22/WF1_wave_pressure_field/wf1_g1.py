#!/usr/bin/env python3
"""WF1 gate 1: the wave field's c_s^2(k,a) on DF2's harness read-only, this lane's CLASS copy (DF2's patch, then wf1_patch.py). Modes: controls | screen I N | fit I N | grade. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); DF = os.path.join(os.path.dirname(HERE), "DF2_dark_fluid_requirement"); sys.dont_write_bytecode = True
src = open(os.path.join(DF, "df2.py")).read(); a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)'; assert src.count(a) == 1
src = src.replace(a, f'HERE = {HERE!r}; RB = os.path.dirname(HERE)').replace('"df2_work', '"wf1_work').replace("df2_work' + TAG", "wf1_work' + TAG").replace('"df2_build", "class_df2"', '"wf1_build", "class_wf1"'); assert "wf1_build" in src
M = {"__name__": "df2ro", "__file__": os.path.join(DF, "df2.py")}; exec(compile(src, "df2.py", "exec"), M)
R, np, NM, jw, pv, BAND, CELLS, PF, RF1, SMIN = M["R"], M["np"], M["NM"], M["jw"], M["pv"], M["BAND"], M["CELLS"], M["PF"], M["RF1"], M["SMIN"]
assert "wf1_build" in R["R1B"] and "wf1_work" in R["WORK"]
M["ENVK"].append("WF1_M"); GRID = [1e-26, 3e-26, 1e-25, 3e-25, 1e-24, 3e-24, 1e-23, 3e-23, 1e-22, 1e-21]; evalp, setenv, cell = M["evalp"], M["setenv"], M["cell"]; fixed_cut = M["fixed_cut"]
def C(m): return cell(f"m{m:g}", "WF", WF1_M=m)
def zosc(m, h=0.675, wm=0.143, wr=4.18e-5):
    """3H = m on a radiation + matter background; m in 1/Mpc, H = (100 h/c) E."""
    mm = m * 1.56373e29; f = lambda z: 3 * (100 / 299792.458) * math.sqrt(wm * (1 + z) ** 3 + wr * (1 + z) ** 4) - mm; lo, hi = 0., 1e12
    if f(lo) > 0: return 0.
    for _ in range(200):
        mid = math.sqrt(max(lo, 1.) * hi); lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return hi
def khalf(k, P, PB):
    rt = np.array(P) / np.array(PB); return float(np.array(k)[np.argmax(rt < .5)]) if (rt < .5).any() else None
def controls():
    L = R["Lik"](); SK = fixed_cut(); ck = {}; base = evalp(L, cell("k_off", "K"), PF, RF1["A"], S_K=SK, tag="k0"); jw(os.path.join(HERE, "wf1_control_base.json"), base)
    a = evalp(L, cell("k_heavy", "K", WF1_M=1e-12), PF, RF1["A"], S_K=SK, tag="k1"); ck["K_rf5_heavy"] = dict(plik=a["plik"], rf5=RF1["chi2"]["plik"], off=base["plik"], d=a["plik"] - RF1["chi2"]["plik"], passed=bool(abs(a["plik"] - RF1["chi2"]["plik"]) <= 0.1))
    q = {}
    for m in (1e-25, 1e-24, 16e-25):
        q[m] = evalp(L, cell(f"k_{m:g}", "K", WF1_M=m), PF, RF1["A"], S_K=SK, tag=f"k{m:g}")
    kh = {m: khalf(base["k"], q[m]["P0"], base["P0"]) for m in q}; r = None if not (kh[1e-25] and kh[1e-24]) else kh[1e-24] / kh[1e-25]; ck["K_sqrtm"] = dict(k_half=kh, ratio=r, expect=math.sqrt(10), passed=bool(r and abs(r / math.sqrt(10) - 1) <= 0.3))
    h = base["h"]; Om = (PF[0] + PF[1]) / h ** 2; H0 = 100 * h / 299792.458; kJ0 = (6 * Om) ** .25 * math.sqrt(H0 * 1e-24 * 1.56373e29); kJeq = kJ0 * (1 / 3400.) ** .25; hbg = {m: 4.5 * (m / 1e-22) ** (4 / 9) / h for m in (1e-25, 1e-24)}  # AMENDMENT_A1 part 3
    ck["K_jeans"] = dict(frozen_ratio_today=kh[1e-24] / (kJ0 / h), frozen_failed=True, k_J_eq_h_Mpc=kJeq / h, ratio_eq=kh[1e-24] / (kJeq / h), hbg=hbg, measured={m: kh[m] for m in hbg}, passed=bool(1 / 3 <= kh[1e-24] / (kJeq / h) <= 3 and all(abs(kh[m] / hbg[m] - 1) <= 0.3 for m in hbg)))
    rr = None if not (kh[1e-25] and kh[16e-25]) else kh[16e-25] / kh[1e-25]; ck["M_x16"] = dict(ratio=rr, expect=4.0, passed=bool(rr and 2.5 <= rr <= 6))
    jw(os.path.join(CELLS, "checks.json"), ck); print(json.dumps(ck, indent=1, default=float), flush=True); return all(v["passed"] for v in ck.values())
def scr(m):
    p = os.path.join(CELLS, f"m{m:g}_scr.json"); return json.load(open(p)) if os.path.exists(p) else None
def screen(i, n):
    L = R["Lik"](); SK = fixed_cut(); sg = M["signal"]
    for j, m in enumerate(GRID):
        if j % n != i or scr(m): continue
        c = C(m); sg.alarm(2400)
        try: r = evalp(L, c, PF, RF1["A"], S_K=SK)
        except M["TO"]: r = dict(status="TIMEOUT")
        sg.alarm(0); r.update(cell=c["name"], m=m, z_osc=zosc(m)); jw(os.path.join(CELLS, c["name"] + "_scr.json"), r); print(c["name"], r["status"], None if r["status"] != "OK" else round(r["S"] - SMIN, 1), flush=True)
def fit(i, n):
    while any(scr(m) is None for m in GRID): time.sleep(60)
    L = R["Lik"](); SK = fixed_cut(); fl = [m for m in GRID if scr(m).get("status") == "OK" and scr(m)["S"] - SMIN <= 2000]
    for j, m in enumerate(reversed(fl)):
        if j % n != i: continue
        c = C(m); p = os.path.join(CELLS, c["name"] + "_fit.json")
        if os.path.exists(p): continue
        setenv(c); cc = {"name": c["name"], "kind": "HF"}; rec = R["fit_cell"](L, cc, PF.copy(), RF1["A"], maxit=10); rec.update(cell=c["name"], m=m)
        if rec.get("status") == "OK":
            pp = np.array([rec["params"][x] for x in NM]); o = R["run"]("fp", cc, pp, pk=True, cmb=False)
            if o is not None:
                rec["Omega_m"] = (pp[0] + pp[1]) / rec["h"] ** 2; sh = R["shear_chi2"](SK[0], SK[1], o, rec["Omega_m"]); k = o["pk"][0.0][:, 0]; rec.update(shear=sh["chi2"], n_shear=sh["n"], sigma8_pk=o["sigma8"], k=k.tolist()[::4], P0=o["pk"][0.0][:, 1].tolist()[::4], z3=sorted(o["pk"].keys())[-1], Pz=o["pk"][sorted(o["pk"].keys(), key=lambda z: abs(z - 3))[0]][:, 1].tolist()[::4], z_read=sorted(o["pk"].keys(), key=lambda z: abs(z - 3))[0])
        jw(p, rec); print(c["name"], rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("converged"), flush=True)
def grade():
    out = []; res = dict(rows={}, S_min=SMIN)
    def P(s=""): print(s, flush=True); out.append(str(s))
    P(f"WF1 gate 1, S_min {SMIN:.2f}, line S - S_min <= 25. Screen = RF5's parameters, never a pass. Runs as dust from the start; onset read per FROZEN_CRITERIA. kappa = 1/2 FITTED. Not theory closed.")
    ck = json.load(open(os.path.join(CELLS, "checks.json"))); P("checks: " + ", ".join(f"{k} {v['passed']}" for k, v in ck.items())); base = json.load(open(os.path.join(HERE, "wf1_control_base.json")))
    for m in GRID:
        s = scr(m); z = zosc(m); w = dict(m=m, z_osc=z); line = f"m {m:7.0e} z_osc {z:9.3g}"
        if s and s["status"] == "OK": kh = khalf(base["k"], s["P0"], base["P0"]); w.update(screen_S=s["S"] - SMIN, k_half=kh); line += f" screen S-Smin {s['S'] - SMIN:10.1f} plik {s['plik']:9.1f} s8 {s['sigma8']:.3f} k_half {kh}"
        elif s: line += f" screen {s['status']}"
        p = os.path.join(CELLS, f"m{m:g}_fit.json"); f = json.load(open(p)) if os.path.exists(p) else None
        if f and f.get("status") == "OK" and "shear" in f:
            c = f["chi2"]; S = c["plik"] + c["Aprior"] + c["bao"] + c["sn"] + f["shear"]; g = dict(CMB=pv(c["plik"], 605) >= 1e-3, BAO=pv(c["bao"], 13) >= 1e-3, SN=pv(c["sn"], c["n_sn"] - 1) >= 1e-3, A0=all(BAND[q][0] <= f["sqrtX"].get(str(q), -1) <= BAND[q][1] for q in BAND), SHEAR=pv(f["shear"], f["n_shear"] - 1) >= 1e-3, S=S - SMIN <= 25); ok = bool(all(g.values()) and f["converged"]); und = z < 3e4
            w.update(S=S - SMIN, plik=c["plik"], bao=c["bao"], shear=f["shear"], s8=f["sigma8_pk"], omega_f=f["params"]["omega_c"], omega_b=f["params"]["omega_b"], h=f["h"], converged=f["converged"], gates=g, passed=bool(ok and not und), onset_undetermined=und, k=f["k"], P0=f["P0"], Pz=f["Pz"], z_read=f["z_read"])
            line += f" | FIT S-Smin {S - SMIN:.1f} plik {c['plik']:.1f} s8 {f['sigma8_pk']:.3f} wf {f['params']['omega_c']:.4f} conv {f['converged']} " + ("UNDETERMINED onset" + (" (optimistic pass)" if ok else " (fails even so)") if und else ("PASS" if ok else "FAIL " + str([k for k, x in g.items() if not x])))
        elif f: line += f" | fit {f.get('status')} {str(f.get('msg'))[:60]}"; w["fit_status"] = f.get("status")
        P(line); res["rows"][f"{m:g}"] = w
    ps = [k for k, v in res["rows"].items() if v.get("passed")]; res["pass"] = ps; P(f"\npassing m: {ps}"); P("kappa = 1/2 FITTED. Not theory closed."); jw(os.path.join(HERE, "wf1_g1_results.json"), res); open(os.path.join(HERE, "wf1_g1.out"), "w").write("\n".join(out) + "\n")
if __name__ == "__main__":
    m_ = sys.argv[1]
    if m_ == "controls": sys.exit(0 if controls() else 1)
    if m_ == "screen": screen(int(sys.argv[2]), int(sys.argv[3]))
    if m_ == "fit": fit(int(sys.argv[2]), int(sys.argv[3]))
    if m_ == "grade": grade()
