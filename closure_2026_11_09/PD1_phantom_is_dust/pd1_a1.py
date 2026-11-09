#!/usr/bin/env python3
"""PD1 AMENDMENT A1 (08b9797be3; criteria 0dc7929421): N's halo rule as relayed. f_core = (1/2)[1 - (v_stiff/v_vir)^2] of the share
in a Duffy NFW core (v_vir > v_stiff), phantom W_vir M_b(<r)(nu - 1) capped by E = (1 - f_core) share, remainder isothermal to R_ms.
Reruns P2 KiDS, P2 SPARC, P3 groups, P3 X-COP (f_miss vs TR1), P5 Bullet. pd1.py's functions are executed read-only (prefix).
    python3 pd1_a1.py   -> pd1_a1.json / pd1_a1.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "pd1.py")).read(); ns = {"__file__": os.path.join(HERE, "pd1.py"), "__name__": "pd1_lib"}
exec(compile(src[:src.index("# ---------------- run")], "pd1_prefix", "exec"), ns)
np, G, MS, KPC, MPC, C, glaw, Mph = ns["np"], ns["G"], ns["MS"], ns["KPC"], ns["MPC"], ns["C"], ns["glaw"], ns["Mph"]
A0, FOOTS, footing_bg, share_table, interp = ns["A0"], ns["FOOTS"], ns["footing_bg"], ns["share_table"], ns["interp"]
LE, GALS, PRE, XC, GR, R500X, Q8, TR1, G_KPC = ns["LE"], ns["GALS"], ns["PRE"], ns["XC"], ns["GR"], ns["R500X"], ns["Q8"], ns["TR1"], ns["G_KPC"]
from scipy.optimize import brentq
A1 = "08b9797be3"; VST = {"canonical": 265.8, "alt": 288.1}; CS_IGM = 15.0; L = []
def P(s): print(s, flush=True); L.append(str(s))
def system(B, f, tab, Msys, z=0.0):   # A2 bracket: core prefactor via env PD1_FCPRE (default 0.5)
    """budgets for a system of baryon mass Msys (Msun): share, R_ms, v_vir, f_core, W, NFW core (M(<r) callable, Msun), E, R_trunc, remainder."""
    a0 = A0[f]; m = math.log10(Msys); share = interp(tab, "share_over_Mb", m) * Msys; rms = interp(tab, "R_ms_Mpc", m) * MPC
    if os.environ.get("PD1_SHARE"): share = float(os.environ["PD1_SHARE"]) * Msys          # post-A1 reported reading (cosmic-ratio share), never graded
    H = C.halo(Msys, B.R, B.h, B.Om, kind="NFW", M200=Msys + share, Mchi=share, z=z); v = math.sqrt(G_KPC * H["M200"] / H["R200"])
    fc = float(os.environ.get("PD1_FCPRE", "0.5")) * (1 - (VST[f] / v) ** 2) if v > VST[f] else 0.0; W = 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2)
    c = H["c200"]; rs = H["R200"] / c; mu = lambda x: np.log1p(x) - x / (1 + x)
    core = lambda r_kpc: fc * share * float(mu(min(r_kpc, H["R200"]) / rs) / mu(c))
    E = (1 - fc) * share; mph_ms = W * Mph(rms, Msys * MS, a0) / MS
    rt = brentq(lambda r: W * Mph(r, Msys * MS, a0) / MS - E, 1e-6 * KPC, rms) if mph_ms > E else rms
    rem = max(0.0, E - mph_ms)
    return dict(share=share, R_ms=rms, v_vir=v, f_core=fc, W=W, core=core, E=E, R_trunc=rt, remainder=rem, R200_kpc=H["R200"], c200=c)
def rem_in(S, r): return S["remainder"] * min(r, S["R_ms"]) / S["R_ms"] if S["remainder"] > 0 else 0.0
def g_sys(S, a0, r, Mb_r, Msys):
    """total g at r (m) for enclosed baryons Mb_r (Msun): W x phantom (law) inside R_trunc, frozen beyond; + core + remainder (Newtonian)."""
    gN = G * Mb_r * MS / r ** 2
    if r < S["R_trunc"]: gph = S["W"] * (float(glaw(gN, a0)) - gN)
    else: gt = G * Msys * MS / S["R_trunc"] ** 2; gph = S["W"] * (float(glaw(gt, a0)) - gt) * (S["R_trunc"] / r) ** 2
    return gN + gph + G * (S["core"](r / KPC) * MS + rem_in(S, r)) / r ** 2, gph * r ** 2 / G / MS
RES = dict(amendment=A1, criteria="0dc7929421", note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; T = share_table(B, a0, 0.0); T3 = share_table(B, a0, 0.3); r = {}
    # KiDS
    sh = []; vk = []
    for p in LE:
        Mb = p["Mb"] / MS; R = math.sqrt(G * p["Mb"] / p["gbar"]); S = system(B, f, T, Mb); g, _ = g_sys(S, a0, R, Mb, Mb); sh.append(math.log10(g / float(glaw(p["gbar"], a0)))); vk.append(S["v_vir"])
    sh = np.array(sh); r["P2_KiDS"] = dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), v_vir_max=float(max(vk)))
    # SPARC
    rows = []; ncore = 0
    for q, Tf in zip(GALS, PRE[f]):
        R_ = q["R"]; Rm = q["Rm"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2; Mbs = max(float(np.max(np.clip(VB2 * R_ / G_KPC, 0, None))), 1e3)
        S = system(B, f, T, Mbs); ncore += S["f_core"] > 0; g = q["GB"]
        gt = G * Mbs * MS / S["R_trunc"] ** 2; inside = (Rm < S["R_trunc"])[:, None]
        ph = np.where(inside, S["W"] * (glaw(g, a0) - g), S["W"] * (float(glaw(gt, a0)) - gt) * (S["R_trunc"] / Rm[:, None]) ** 2)
        extra = np.array([G * (S["core"](x / KPC) * MS + rem_in(S, x)) / x ** 2 for x in Rm])[:, None]
        lgp = np.log10(np.maximum(g + ph + extra, 1e-300)) + Tf; OK, Wt = q["OK"], q["W"]; rr = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, Wt[:, None], 0.0)
        wr2 = (Wm * rr * rr).sum(0); wr = (Wm * rr).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k]))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx); return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws))
    base = json.load(open(os.path.join(HERE, "pd1.json")))[f]["P2_SPARC"]["L0"]; massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]; sa, sm = pooled(range(len(rows))), pooled(massive)
    r["P2_SPARC"] = dict(all=sa, massive=sm, n_with_core=int(ncore), status="PASS" if (sa["rms"] <= base["all"]["rms"] + 0.010 and abs(sa["mean"]) <= 0.05 and sm["rms"] <= base["massive"]["rms"] + 0.010 and abs(sm["mean"]) <= 0.05) else "FAIL")
    # X-COP
    d = []; xr = []; fm = []; fcr = []; per = {}
    for name in R500X:
        pts = [z for z in XC if z["name"] == name]; Msys = pts[0]["Mb_last"][0]; S = system(B, f, T, Msys); per[name] = dict(v_vir=S["v_vir"], f_core=S["f_core"], W=S["W"], share_over_Mb=S["share"] / Msys, c200=S["c200"])
        for z in pts:
            rm = z["r_kpc"] * KPC; g, mph = g_sys(S, a0, rm, z["M_b"], Msys); Mp = g * rm ** 2 / G / MS
            dark = mph + S["core"](z["r_kpc"]) + rem_in(S, rm) / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500X[name]); fm.append(dark / z["M_obs"]); fcr.append(S["core"](z["r_kpc"]) / z["M_obs"])
    d, xr, fm, fcr = map(np.array, (d, xr, fm, fcr)); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
    for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None,
                         f_miss=float(np.median(fm[m])) if m.sum() else None, core_over_Mdyn=float(np.median(fcr[m])) if m.sum() else None, TR1=TR1[b_]))
    gb = [b for b in bins if b["graded"]]; shp = [b["f_miss"] - np.mean([x["f_miss"] for x in gb]) for b in gb]; tsh = [b["TR1"] - np.mean([x["TR1"] for x in gb]) for b in gb]
    amp = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; ok = all(b["within"] for b in gb)
    r["P3_XCOP"] = dict(status="PASS" if (amp and ok) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), bins=bins, shape=dict(model=shp, TR1=tsh), per_cluster=per)
    # groups
    o = {}
    for fst in (0, 1):
        npass = 0; med = []; fcs = []
        for gp in GR:
            Msys = gp["g5"] * (1 + fst); S = system(B, f, T, Msys); fcs.append(S["f_core"]); ok_ = True
            for p in gp["pts"]:
                rm = p["r_kpc"] * KPC; g, _ = g_sys(S, a0, rm, p["M_gas"] * (1 + fst), Msys); dl = math.log10(p["M_obs"] / (g * rm ** 2 / G / MS)); med.append(dl); ok_ &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
            npass += ok_
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)), f_core_median=float(np.median(fcs)))
    r["P3_groups"] = dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
    RES[f] = r; RES[f]["_T3"] = T3
    P(f"[{f}] A1 P2 KiDS {r['P2_KiDS']['status']} max {r['P2_KiDS']['max_abs']:.3f} ({r['P2_KiDS']['n_over']}/59; lens v_vir max {r['P2_KiDS']['v_vir_max']:.0f} km/s); SPARC {r['P2_SPARC']['status']} rms {sa['rms']:.4f} (line {base['all']['rms']+0.010:.4f}; {ncore} galaxies with a core)")
    P(f"[{f}] A1 P3 groups {r['P3_groups']['status']} {o['fst0']['n_pass']}/{o['fst1']['n_pass']} med {o['fst0']['median_res']:+.2f}/{o['fst1']['median_res']:+.2f} (f_core med {o['fst0']['f_core_median']:.2f}); X-COP {r['P3_XCOP']['status']} {r['P3_XCOP']['mean']:+.3f}/{r['P3_XCOP']['rms']:.3f}; bins "
      + " ".join(f"{b['mean']:+.2f} (f_miss {b['f_miss']:.2f}, core {b['core_over_Mdyn']:.2f}, TR1 {b['TR1']})" for b in gb) + f"; f_core per cluster {np.median([v['f_core'] for v in per.values()]):.2f} (v_vir med {np.median([v['v_vir'] for v in per.values()]):.0f}), W {np.median([v['W'] for v in per.values()]):.4f}")
# Bullet: core + remainder inside R200 galaxy-traced (DB1 child via WM1's bchild); phantom = DB1 law row
WM1 = ns["WM1"]
def call(arg, on):
    cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(WM1, "wm1_local.py"), "bchild", "W", arg, on], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
    line = [l for l in cp.stdout.splitlines() if l.startswith("WM1CHILD ")]
    if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
    return json.loads(line[0][9:])
o0 = call("{}", "gal"); mm = o0["masses"]; Mb = [mm["M_gas_sub"][j] + mm["M_star_sub"][j] for j in range(2)]; Ml = {}; inf = {}
for f in FOOTS:
    B = footing_bg(f); vals = []; ii = []
    for j in range(2):
        S = system(B, f, RES[f]["_T3"], Mb[j], z=0.3); ml = S["core"](S["R200_kpc"]) + rem_in(S, S["R200_kpc"] * KPC) / MS; vals.append(ml); ii.append(dict(M_b=Mb[j], v_vir=S["v_vir"], f_core=S["f_core"], dark_in_R200_over_Mb=ml / Mb[j]))
    Ml[f] = vals; inf[f] = ii
oa = call(json.dumps(Ml), "gal")
for f in FOOTS:
    b = oa[f]["row"]; RES[f]["P5_Bullet"] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b, subclusters=inf[f])
    P(f"[{f}] A1 P5 Bullet {RES[f]['P5_Bullet']['status']}: M300 Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}; " + ", ".join(f"v_vir {x['v_vir']:.0f} f_core {x['f_core']:.2f} dark/M_b {x['dark_in_R200_over_Mb']:.2f}" for x in inf[f]))
pd = json.load(open(os.path.join(HERE, "pd1.json")))
for f in FOOTS:
    RES[f].pop("_T3"); st = {"P1 conservation": pd[f]["P1"]["status"], "P2 KiDS": RES[f]["P2_KiDS"]["status"], "P2 SPARC": RES[f]["P2_SPARC"]["status"], "P3 groups": RES[f]["P3_groups"]["status"],
                             "P3 X-COP": RES[f]["P3_XCOP"]["status"], "P4 cosmology (carried)": "PASS", "P5 Bullet": RES[f]["P5_Bullet"]["status"]}
    fails = [k for k, v in st.items() if v != "PASS"]; RES[f]["label"] = dict(status=st, label="PASS" if not fails else "FAIL", first_fail=fails[0] if fails else None)
    P(f"[{f}] PD1 under A1: LABEL {RES[f]['label']['label']}; first failing gate {RES[f]['label']['first_fail']}; " + ", ".join(f"{k} {v}" for k, v in st.items()))
json.dump(RES, open(os.path.join(HERE, "pd1_a1" + ("_share" + os.environ["PD1_SHARE"] if os.environ.get("PD1_SHARE") else "") + ("_fcpre" + os.environ["PD1_FCPRE"] if os.environ.get("PD1_FCPRE") else "") + ".json"), "w"), indent=1, default=float); open(os.path.join(HERE, "pd1_a1" + ("_share" + os.environ["PD1_SHARE"] if os.environ.get("PD1_SHARE") else "") + ("_fcpre" + os.environ["PD1_FCPRE"] if os.environ.get("PD1_FCPRE") else "") + ".out"), "w").write("\n".join(L) + "\n")
