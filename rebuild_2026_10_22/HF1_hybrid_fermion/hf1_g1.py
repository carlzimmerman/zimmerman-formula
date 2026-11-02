#!/usr/bin/env python3
"""HF1 gate 1: light fermion on CLASS, RF5's raw channels, native background. a0 is absent from linear FRW. Frozen: FROZEN_CRITERIA.md, AMENDMENT_A1.md.
Modes: checks | fit SPEC M | pk SPEC M | grade.  SPEC: FD, CHI, COLD. HF1_MUTATE=1: omega_b x 1.1 in the known answer, must fail; separate outputs.
Reuses RF5's code read-only: source loaded, only work paths redirected into this lane. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RF = os.path.join(RB, "RF5_growth_native_yardstick")
os.environ.setdefault("OMP_NUM_THREADS", "1")
MUT = os.environ.get("HF1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
CELLS = os.path.join(HERE, "cells_g1" + TAG); os.makedirs(CELLS, exist_ok=True)
src = open(os.path.join(RF, "rf5.py")).read()
a = 'HERE = os.path.dirname(os.path.abspath(__file__))'; assert src.count(a) == 1
src = src.replace(a, f'HERE = {RF!r}').replace('WORK = os.path.join(EXT, f"rf5_work{TAG}")', 'WORK = os.path.join(EXT, "hf1_work' + TAG + '")').replace('CELLS = os.path.join(HERE, f"cells{TAG}")', f'CELLS = {CELLS!r}')
assert "hf1_work" in src
src = src.replace('"nice", "-n", "15"', '"nice", "-n", "15"')
R = {"__name__": "rf5ro", "__file__": os.path.join(RF, "rf5.py")}; exec(compile(src, "rf5.py", "exec"), R)
np = R["np"]; G_MS = None
from scipy.integrate import quad
TNU = 0.71611  # T_nu / T_cmb, CLASS's standard ncdm value
def n_occ(ksi): return quad(lambda q: q * q * (1 / (math.exp(q - ksi) + 1) + 1 / (math.exp(q + ksi) + 1)), 0, 200 + ksi, limit=400)[0]
N0 = n_occ(0.0)
def ncdm(m, wf, spec):
    """(T_ncdm, deg, ksi). omega = m/93.14 at T_nu, deg 1, ksi 0; omega scales with deg T^3 and the occupancy integral."""
    x = wf * 93.14 / m
    if spec == "FD": return TNU * x ** (1 / 3), 1.0, 0.0
    if spec == "CHI": return TNU, x, 0.0
    if spec == "COLD": return TNU * (x * N0 / n_occ(5.0)) ** (1 / 3), 1.0, 5.0
    raise ValueError(spec)
PREC = {"tol_ncdm_synchronous": 1e-5, "tol_ncdm_bg": 1e-7, "ncdm_fluid_trigger_tau_over_tau_k": 200.0}  # settled by hf1_g1_prec.json before any fit
def cparams(p, cell):
    wb, wf, th, lnA, ns_, tau, w0, wa = p
    q = {"omega_b": wb, "100*theta_s": th, "ln10^{10}A_s": lnA, "n_s": ns_, "tau_reio": tau, "Omega_Lambda": 0.0, "w0_fld": w0, "wa_fld": wa, "cs2_fld": 1.0, "use_ppf": "yes"}
    if cell["kind"] == "R1":
        q["omega_cdm"] = max(wf, 5e-4); return q
    T, deg, ksi = ncdm(cell["m"], max(wf, 5e-4), cell["spec"])
    q.update({"omega_cdm": 1e-8, "N_ur": 3.044, "N_ncdm": 1, "m_ncdm": cell["m"], "T_ncdm": T, "deg_ncdm": deg})
    if ksi: q["ksi_ncdm"] = ksi
    q.update(PREC); q.update(cell.get("prec", {}))
    return q
R["cparams"] = cparams
_SAVE = os.path.join(RF, "cells", "shear_scale_cut.json")
def fixed_cut():
    S = R["load_shear"](); q = json.load(open(_SAVE)); return S, np.array(q["keep"], bool), q
RF1 = json.load(open(os.path.join(RF, "cells", "R1_1000000.json"))); RFCH = json.load(open(os.path.join(RF, "cells", "R1_1000000_channels.json")))
SMIN = json.load(open(os.path.join(RF, "rf5_results.json")))["S_min"]
NM = R["NAMES"]
def jw(p, o): R["jw"](p, o)
def Om_of(r): return (r["params"]["omega_b"] + r["params"]["omega_c"]) / r["h"] ** 2
def cellname(spec, m): return f"{spec}_m{m:g}"
MGRID = [11.8, 11.0, 9.0, 7.0, 5.0, 3.74]

def m_checks():
    L = R["Lik"](); res = {"mutate": MUT}
    # K-a: RF5's cell at RF5's best fit, through this harness
    p = np.array([RF1["params"][n] for n in NM]); 
    if MUT: p[0] *= 1.1
    c = {"name": "kchk", "kind": "R1", "zon": 1e6}
    o = R["run"]("ka", c, p); q = L.parts(o, RF1["A"])
    d = {k: q[k] - RF1["chi2"][k] for k in ("plik", "bao", "sn", "lowTT", "lowEE")}
    res["Ka_RF5_cell"] = dict(diff=d, passed=bool(max(abs(v) for v in d.values()) <= 0.02))
    o = R["run"]("kap", c, p, pk=True, cmb=False); S, keep, _ = fixed_cut(); sh = R["shear_chi2"](S, keep, o, RF1["Omega_m"])
    res["Ka_shear"] = dict(chi2=sh["chi2"], rf5=RFCH["shear"]["chi2"], sigma8=o["sigma8"], rf5_s8=RFCH["sigma8"], passed=bool(abs(sh["chi2"] - RFCH["shear"]["chi2"]) <= 0.02))
    # K-b: heavy fermion is RF5's dust. m 2000 eV FD, omega_f = RF5's omega_c
    c2 = {"name": "kchk", "kind": "HF", "m": 2000.0, "spec": "FD"}; o2 = R["run"]("kb", c2, p, keep=True)
    bg, cols = o2["bg_all"]; ncol = [k for k in cols if "rho_ncdm" in k][0]; H0 = float(bg[-1, cols["H [1/Mpc]"]]); wc = float(bg[-1, cols[ncol]]) / H0 ** 2 * o2["h"] ** 2
    q2 = L.parts(o2, RF1["A"]); res["Kb_heavy_limit"] = dict(plik=q2["plik"], rf5=RF1["chi2"]["plik"], d=q2["plik"] - RF1["chi2"]["plik"], omega_class=wc, omega_in=float(p[1]), passed=bool(abs(q2["plik"] - RF1["chi2"]["plik"]) <= 2.0 and abs(wc / p[1] - 1) <= 3e-3))
    R["_clean"](os.path.join(R["WORK"], "kchk"), "kb")
    # K-c: omega_ncdm at 11 eV, FD: CLASS's own value against the T rule; g_f = 2 means deg 1
    c3 = {"name": "kchk", "kind": "HF", "m": 11.0, "spec": "FD"}; o3 = R["run"]("kc", c3, p, keep=True); bg, cols = o3["bg_all"]; H0 = float(bg[-1, cols["H [1/Mpc]"]]); wc = float(bg[-1, cols[ncol]]) / H0 ** 2 * o3["h"] ** 2
    q3 = L.parts(o3, RF1["A"]); neff = [l for l in o3["log"].splitlines() if "N_eff" in l]
    res["Kc_omega_rule"] = dict(omega_class=wc, omega_in=float(p[1]), ratio=wc / float(p[1]), neff=neff, passed=bool(abs(wc / p[1] - 1) <= 3e-3)); R["_clean"](os.path.join(R["WORK"], "kchk"), "kc")
    # K-d: ncdm precision at 11 eV, FD: the fit's setting vs tighter, plik at the same parameters
    pr = {"tol_ncdm_synchronous": 1e-6, "tol_ncdm_bg": 1e-8, "l_max_ncdm": 40, "ncdm_fluid_trigger_tau_over_tau_k": 1000.0}
    c4 = dict(c3, prec=pr); o4 = R["run"]("kd", c4, p); q4 = L.parts(o4, RF1["A"]); res["Kd_ncdm_precision"] = dict(plik_fit_setting=q3["plik"], plik_tight=q4["plik"], d=q4["plik"] - q3["plik"], passed=bool(abs(q4["plik"] - q3["plik"]) <= 1.0))
    # K-e: COLD and CHI: omega_class against the rule
    for sp, mm, tag in (("COLD", 7.0, "Ke_cold"), ("CHI", 7.0, "Ke_chi")):
        cc = {"name": "kchk", "kind": "HF", "m": mm, "spec": sp}; oo = R["run"]("ke", cc, p, keep=True); bg, cols = oo["bg_all"]; H0 = float(bg[-1, cols["H [1/Mpc]"]]); wc = float(bg[-1, cols[ncol]]) / H0 ** 2 * oo["h"] ** 2
        res[tag] = dict(omega_class=wc, omega_in=float(p[1]), ratio=wc / float(p[1]), neff=[l for l in oo["log"].splitlines() if "N_eff" in l], passed=bool(abs(wc / p[1] - 1) <= 3e-3)); R["_clean"](os.path.join(R["WORK"], "kchk"), "ke")
    jw(os.path.join(CELLS, "checks.json"), res); print(json.dumps(res, indent=1, default=float)); sys.exit(0 if all(v["passed"] for v in res.values() if isinstance(v, dict)) else 1)

def m_fit(spec, m):
    L = R["Lik"](); name = cellname(spec, m); path = os.path.join(CELLS, name + ".json")
    if os.path.exists(path): print("have", name); return
    prev = [cellname(spec, x) for x in MGRID if x > m]; st = None
    for n in reversed(prev):
        pp = os.path.join(CELLS, n + ".json")
        if os.path.exists(pp):
            j = json.load(open(pp))
            if j.get("status") == "OK": st = j; break
    if st is None: st = RF1
    p0 = np.array([st["params"][n] for n in NM]); A0_ = st["A"]
    c = {"name": name, "kind": "HF", "m": m, "spec": spec}
    try: rec = R["fit_cell"](L, c, p0, A0_, maxit=int(os.environ.get("HF1_MAXIT", "10")))
    except R["Preempted"]: sys.exit(75)
    rec.update(cell=name, kind="HF", m=m, spec=spec)
    if rec.get("status") == "OK":
        rec["params"]["omega_c"] = rec["params"]["omega_c"]; rec["Omega_m"] = Om_of(rec); T, deg, ksi = ncdm(m, rec["params"]["omega_c"], spec); rec.update(T_ncdm=T, deg_ncdm=deg, ksi_ncdm=ksi)
        o = R["run"]("nf", c, np.array([rec["params"][n] for n in NM])); rec["neff_log"] = [l.strip() for l in o["log"].splitlines() if "N_eff" in l]
    jw(path, rec); print(name, rec.get("status"), (rec.get("chi2") or {}).get("plik"), rec.get("converged"), flush=True)

def m_pk(spec, m):
    name = cellname(spec, m); r = json.load(open(os.path.join(CELLS, name + ".json")))
    if r.get("status") != "OK": return
    outp = os.path.join(CELLS, name + "_channels.json")
    if os.path.exists(outp): return
    S, keep, _ = fixed_cut(); c = {"name": name, "kind": "HF", "m": m, "spec": spec}; o = R["run"]("pk", c, np.array([r["params"][n] for n in NM]), pk=True, cmb=False)
    if o is None:
        o = R["run"]("pk", c, np.array([r["params"][n] for n in NM]), pk=True, cmb=False, default_start=True)
    if o is None: jw(outp, dict(status="PK_FAIL", msg=c.get("class_fail", ["?"])[-1])); return
    res = dict(sigma8=o["sigma8"], shear=R["shear_chi2"](S, keep, o, r["Omega_m"]))
    zk = [0.0, 1.0, 2.0, 3.6]; k = o["pk"][0.0][:, 0]; res["k_h_Mpc"] = k.tolist()[::8]; res["P_z0"] = o["pk"][0.0][:, 1].tolist()[::8]
    for z in zk[1:]: res[f"P_z{z}"] = o["pk"][z][:, 1].tolist()[::8]
    jw(outp, res); print(name, "s8", o["sigma8"], "shear", res["shear"]["chi2"], flush=True)

def m_grade():
    out = []
    def P(s=""): print(s, flush=True); out.append(str(s))
    BAND = R["BAND"]; pv = R["pval"]; RES = dict(S_min_RF5=SMIN, rows={})
    P(f"HF1 gate 1, criteria 56ab302a4d, A1. kappa = 1/2 FITTED. S_min RF5 {SMIN:.2f}. a0 absent from linear FRW, so footings share the surface")
    ck = json.load(open(os.path.join(CELLS, "checks.json"))); P("checks: " + ", ".join(f"{k} {v['passed']}" for k, v in ck.items() if isinstance(v, dict)))
    for spec in ("FD", "CHI", "COLD"):
        rows = {}
        for m in MGRID:
            n = cellname(spec, m); p = os.path.join(CELLS, n + ".json")
            if not os.path.exists(p): continue
            r = json.load(open(p))
            if r.get("status") != "OK": rows[n] = dict(status="UNDETERMINED", msg=r.get("msg")); continue
            c = r["chi2"]; pc = os.path.join(CELLS, n + "_channels.json"); ch = json.load(open(pc)) if os.path.exists(pc) else {}
            w = dict(status="OK", m=m, omega_f=r["params"]["omega_c"], omega_b=r["params"]["omega_b"], h=r["h"], Om=r["Omega_m"], plik=c["plik"], Aprior=c["Aprior"], bao=c["bao"], sn=c["sn"], lowTT=c["lowTT"], lowEE=c["lowEE"], n_s=r["params"]["n_s"], tau=r["params"]["tau"], w0=r["params"]["w0"], wa=r["params"]["wa"], rd=r["rd"], sqrtX=r["sqrtX"], converged=r["converged"], neff=r.get("neff_log"), T_ncdm=r.get("T_ncdm"), deg=r.get("deg_ncdm"), params=r["params"], A=r["A"])
            w["p_plik"] = pv(c["plik"], 605); w["p_bao"] = pv(c["bao"], 13); w["p_sn"] = pv(c["sn"], c["n_sn"] - 1); w["G_A0"] = all(BAND[z][0] <= r["sqrtX"].get(str(z), -1) <= BAND[z][1] for z in BAND)
            sh = ch.get("shear")
            if sh: w.update(shear=sh["chi2"], A_shear=sh["A_shear"], n_shear=sh["n"], p_shear=pv(sh["chi2"], sh["n"] - 1), sigma8=ch["sigma8"]); w["S"] = c["plik"] + c["Aprior"] + c["bao"] + c["sn"] + sh["chi2"]; w["S_minus_RF5"] = w["S"] - SMIN
            g = dict(CMB=w["p_plik"] >= 1e-3, BAO=w["p_bao"] >= 1e-3, SN=w["p_sn"] >= 1e-3, A0=w["G_A0"], SHEAR=bool(sh) and w["p_shear"] >= 1e-3, S=bool(sh) and w["S_minus_RF5"] <= 25)
            w["gates"] = g; w["passed"] = bool(all(g.values()) and r["converged"]); w["label"] = ("PASS" if w["passed"] else "FAIL") if r["converged"] else "UNDETERMINED (unconverged)"
            rows[n] = w
        RES["rows"][spec] = rows
        P(f"\n{spec}: {'primary' if spec == 'FD' else 'reported variant, A1 R1'}")
        P(f"{'m':>6s} {'omega_f':>8s} {'T/Tnu':>6s} {'h':>6s} {'Om':>6s} {'plik':>8s} {'p':>8s} {'lowTT':>6s} {'bao':>6s} {'sn':>7s} {'shear':>7s} {'A_sh':>5s} {'s8':>6s} {'w0':>6s} {'wa':>6s} {'n_s':>6s} {'S-RF5':>8s} A0 conv label")
        sb = {k: v["S"] for k, v in rows.items() if "S" in v}
        for n, w in rows.items():
            if w["status"] != "OK": P(f"{n} UNDETERMINED {w.get('msg')}"); continue
            P(f"{w['m']:6g} {w['omega_f']:8.5f} {w['T_ncdm'] / TNU:6.3f} {w['h']:6.3f} {w['Om']:6.3f} {w['plik']:8.1f} {w['p_plik']:8.1e} {w['lowTT']:6.1f} {w['bao']:6.1f} {w['sn']:7.1f} {w.get('shear', float('nan')):7.1f} {w.get('A_shear', float('nan')):5.2f} {w.get('sigma8', float('nan')):6.3f} {w['w0']:6.2f} {w['wa']:6.2f} {w['n_s']:6.3f} {w.get('S_minus_RF5', float('nan')):8.1f} {w['G_A0']} {w['converged']} {w['label']}  fails {[k for k, v in w['gates'].items() if not v]}")
            if w.get("neff"): P("        " + w["neff"][-1])
        if sb: P(f"  own-surface S min {min(sb.values()):.1f}, at {min(sb, key=sb.get)}; printed, not the line (A1 R2)")
    fd = RES["rows"].get("FD", {}); RES["pass_FD"] = [v["m"] for v in fd.values() if v.get("passed")]; RES["EARLY_FAIL"] = bool(fd) and not RES["pass_FD"]
    P(f"\nFD passing m: {RES['pass_FD']}; label {'EARLY FAIL' if RES['EARLY_FAIL'] else 'gate 1 open'}"); P("kappa = 1/2 FITTED. Not theory closed.")
    open(os.path.join(HERE, f"hf1_g1{TAG}.out"), "w").write("\n".join(out) + "\n"); jw(os.path.join(HERE, f"hf1_g1_results{TAG}.json"), RES)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "checks": m_checks()
    elif a == "fit": m_fit(sys.argv[2], float(sys.argv[3]))
    elif a == "pk": m_pk(sys.argv[2], float(sys.argv[3]))
    elif a == "grade": m_grade()
