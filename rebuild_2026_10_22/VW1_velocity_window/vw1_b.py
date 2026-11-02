#!/usr/bin/env python3
"""VW1 Stage B: gate 1 against v0 at fixed spectrum shape, number not thermal. HF1 gate 1's machinery read-only, cells and work in this lane. Modes: controls | grid | grade. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); HF = os.path.join(os.path.dirname(HERE), "HF1_hybrid_fermion"); sys.dont_write_bytecode = True
src = open(os.path.join(HF, "hf1_g1.py")).read()
a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)'; assert src.count(a) == 1
src = src.replace(a, f'HERE = {HERE!r}; RB = os.path.dirname(HERE)').replace('"hf1_work', '"vw1_work').replace("hf1_work' + TAG", "vw1_work' + TAG")
b = '    if spec == "CHI": return TNU, x, 0.0'; assert src.count(b) == 1
src = src.replace(b, '    if spec.startswith("FDU"):\n        T = float(spec[3:]) / (3.15137 * 299792.458) * m / 2.34865e-4; return T, x * (TNU / T) ** 3, 0.0\n' + b)
M = {"__name__": "hf1ro", "__file__": os.path.join(HF, "hf1_g1.py")}; exec(compile(src, "hf1_g1.py", "exec"), M)
R, np, NM, jw, CELLS = M["R"], M["np"], M["NM"], M["jw"], M["CELLS"]
assert "vw1_work" in R["WORK"]; GRID = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]; MNUM = 100.0
def spec(v): return f"FDU{v:g}"
def fit(v, start):
    name = f"{spec(v)}_m{MNUM:g}"; path = os.path.join(CELLS, name + ".json")
    if os.path.exists(path): return json.load(open(path))
    L = R["Lik"](); c = {"name": name, "kind": "HF", "m": MNUM, "spec": spec(v)}; p0 = np.array([start["params"][n] for n in NM])
    rec = R["fit_cell"](L, c, p0, start["A"], maxit=10); rec.update(cell=name, kind="HF", m=MNUM, spec=spec(v), v0=v)
    if rec.get("status") == "OK": rec["Omega_m"] = M["Om_of"](rec)
    jw(path, rec); print(name, rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("converged"), flush=True)
    if rec.get("status") == "OK": M["m_pk"](spec(v), MNUM)
    return rec
def controls():
    L = R["Lik"](); ck = {}; p = np.array([M["RF1"]["params"][n] for n in NM]); A = M["RF1"]["A"]
    pl = {}
    for mm in (100.0, 400.0):
        o = R["run"](f"kmi{mm:g}", {"name": f"vwchk{mm:g}", "kind": "HF", "m": mm, "spec": "FDU2"}, p); pl[mm] = L.parts(o, A)["plik"]; print(mm, o["h"], o["log"][-200:] if "N_eff" in o["log"] else "", flush=True)
    ck["K_m_indep"] = dict(plik=pl, d=pl[400.0] - pl[100.0], passed=bool(abs(pl[400.0] - pl[100.0]) <= 1.0))
    h = json.load(open(os.path.join(HF, "cells_g1", "FD_m11.8.json"))); ph = np.array([h["params"][n] for n in NM]); u = 3.15137 * h["T_ncdm"] * 2.34865e-4 / 11.8 * 299792.458
    o = R["run"]("khf", {"name": "vwchk", "kind": "HF", "m": 11.8, "spec": f"FDU{u:.10g}"}, ph); q = L.parts(o, h["A"]); ck["K_hf1_cell"] = dict(v0=u, plik=q["plik"], hf1=h["chi2"]["plik"], d=q["plik"] - h["chi2"]["plik"], passed=bool(abs(q["plik"] - h["chi2"]["plik"]) <= 1.0))
    jw(os.path.join(CELLS, "vw1_checks.json"), ck); print(json.dumps(ck, indent=1, default=float), flush=True); return all(v["passed"] for v in ck.values())
def grade():
    out = []; res = {}; pv = R["pval"]; BAND = R["BAND"]; SMIN = M["SMIN"]
    def P(s): print(s, flush=True); out.append(s)
    P(f"VW1 Stage B, gate 1 line unchanged, S_min {SMIN:.2f}. kappa = 1/2 FITTED.")
    for v in GRID:
        n = f"{spec(v)}_m{MNUM:g}"; p = os.path.join(CELLS, n + ".json")
        if not os.path.exists(p): continue
        r = json.load(open(p))
        if r.get("status") != "OK": P(f"v0 {v:g} UNDETERMINED {str(r.get('msg'))[:90]}"); res[str(v)] = dict(status="UNDETERMINED"); continue
        c = r["chi2"]; ch = json.load(open(os.path.join(CELLS, n + "_channels.json"))); sh = ch["shear"]; S = c["plik"] + c["Aprior"] + c["bao"] + c["sn"] + sh["chi2"]
        g = dict(CMB=pv(c["plik"], 605) >= 1e-3, BAO=pv(c["bao"], 13) >= 1e-3, SN=pv(c["sn"], c["n_sn"] - 1) >= 1e-3, A0=all(BAND[z][0] <= r["sqrtX"].get(str(z), -1) <= BAND[z][1] for z in BAND), SHEAR=pv(sh["chi2"], sh["n"] - 1) >= 1e-3, S=S - SMIN <= 25)
        ok = bool(all(g.values()) and r["converged"]); res[str(v)] = dict(status="OK", v0=v, omega_f=r["params"]["omega_c"], h=r["h"], Om=r["Omega_m"], plik=c["plik"], bao=c["bao"], sn=c["sn"], shear=sh["chi2"], s8=ch["sigma8"], S_minus=S - SMIN, gates=g, converged=r["converged"], passed=ok, k=ch["k_h_Mpc"], P0=ch["P_z0"])
        P(f"v0 {v:5g}: omega_f {r['params']['omega_c']:.4f} h {r['h']:.3f} plik {c['plik']:.1f} bao {c['bao']:.1f} shear {sh['chi2']:.1f} s8 {ch['sigma8']:.3f} S-S_min {S - SMIN:.1f} conv {r['converged']} {'PASS' if ok else 'FAIL ' + str([k for k, x in g.items() if not x])}")
    ks = [k for k in res if res[k].get("status") == "OK"]
    if ks:
        b = res[ks[0]]; k0 = np.array(b["k"]); P0 = np.array(b["P0"])
        for k_ in ks[1:]:
            rt = np.array(res[k_]["P0"]) / P0 * b["s8"] ** 0 ; j = np.argmax(rt < 0.5); res[k_]["k_half_h_Mpc"] = float(k0[j]) if (rt < 0.5).any() else None; P(f"  P(k,z=0) ratio to v0 {ks[0]}: v0 {k_} halves at k {res[k_]['k_half_h_Mpc']} h/Mpc")
    P("Not theory closed."); jw(os.path.join(HERE, "vw1_b.json"), res); open(os.path.join(HERE, "vw1_b.out"), "w").write("\n".join(out) + "\n")
if sys.argv[1] == "controls": sys.exit(0 if controls() else 1)
if sys.argv[1] == "grid":
    st = M["RF1"]
    for v in GRID:
        r = fit(v, st)
        if r.get("status") == "OK": st = r
if sys.argv[1] == "grade": grade()
