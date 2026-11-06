#!/usr/bin/env python3
"""QX12 iter_3 (FROZEN_CRITERIA.md, b605c9fd7c): isothermal sector in contact with the sea, rho = A exp(H/c^2), H = int_r^{r_ta}
g_tot; open A = rho_sea, capped at M_cap = f_cap R M_b; self-consistent with the a0 law (QX10's host machinery, isothermal
solver here). c_min fixed by galaxy gates G5/G6/G7 only; X-COP + groups predicted at c_min.
    python3 qx12_i3.py [--workers 4]        -> qx12_i3.json/.out
    python3 qx12_i3.py --mutate             -> qx12_i3_MUTATE.json/.out  (M1 c 30 km/s; M2 M_cap -> 0)
kappa = 1/2 FITTED; not theory closed; footings never pooled. Units kpc, Msun, km/s."""
import os, sys, json, math, runpy, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx12_i3_MUTATE" if MUT else "qx12_i3"
WK = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
Q10 = os.path.join(REPO, "closure_2026_11_06", "QX10_window_hardening", "iter_2_capture_dynamics", "qx10_i2.py")
argv0 = sys.argv; sys.argv = [Q10]
with contextlib.redirect_stdout(io.StringIO()):
    L = runpy.run_path(Q10, run_name="qx10_lib")
sys.argv = argv0
GK, glaw, A0K, R, FCAP, RHO_D0, r_ta = L["GK"], L["glaw"], L["A0K"], L["R"], L["FCAP"], L["RHO_D0"], L["r_ta"]
expdisc, pointmass, profile_from, G5SYS, LE, EL, GR, clusters, baselines = (L[k] for k in ("expdisc", "pointmass", "profile_from", "G5SYS", "LE", "EL", "GR", "clusters", "baselines"))
G_SI, MS, KPC_M, ACC, glaw_SI = L["G_SI"], L["MS"], L["KPC_M"], L["ACC"], L["glaw_SI"]

# Amendment A1 (9c7497b4cc): KiDS hosts = exponential discs with r_d from SPARC's own Rdisk-M_b fit; regular cores.
_x, _y = [], []
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    t = ln.split()
    if len(t) < 18: continue
    try: Lk = float(t[7]); Rd = float(t[11]); MHI = float(t[13]); q = int(t[17]); inc = float(t[5])
    except ValueError: continue
    if q <= 2 and inc >= 30 and Rd > 0: _x.append(math.log10((0.5 * Lk + 1.33 * MHI) * 1e9)); _y.append(math.log10(Rd))
RD_B, RD_A = np.polyfit(_x, _y, 1)
def rd_of(Mb): return 10 ** (RD_A + RD_B * math.log10(Mb))
def profile_core(rk, Mk, Mlast, rlast, variant=False):
    rr = np.concatenate([np.asarray(rk, float), [rlast]]); mm = np.concatenate([np.asarray(Mk, float), [Mlast]])
    o = np.argsort(rr); rr, mm = rr[o], np.maximum.accumulate(mm[o])
    s0 = math.log(mm[1] / mm[0]) / math.log(rr[1] / rr[0]) if len(rr) > 1 and mm[1] > mm[0] else 1.5
    pin = max(s0, 1.2) if variant else 3.0
    def f(x):
        if x <= rr[0]: return float(mm[0] * (x / rr[0]) ** pin)
        if x >= rr[-1]: return float(mm[-1])
        return float(math.exp(np.interp(math.log(x), np.log(rr), np.log(mm))))
    return f


def solve_iso(Mb_fn, M_cap, c2, rta, a0k, law=True, host=True, rho_sea=RHO_D0, n=900, rmin=1e-3):
    r = np.geomspace(rmin, rta, n); lr = np.log(r)
    Mb = np.array([Mb_fn(x) for x in r]) if host else np.zeros(n)
    dr = np.diff(r); shell = 4 * math.pi * r ** 2
    Msea = 4 / 3 * math.pi * rho_sea * r ** 3     # the uniform sea is the cosmic background: only the excess gravitates
    Md = Msea.copy()
    capped = False; err = 1.0
    for it in range(4000):
        gN = GK * (Mb + Md - Msea) / r ** 2
        g = glaw(gN, a0k) if law else gN
        Hc = np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * dr)[::-1])[::-1], [0.0]])
        lrho = math.log(rho_sea) + Hc / c2
        top = lrho.max(); w = np.exp(lrho - top)
        seg = 0.5 * (shell[1:] * w[1:] + shell[:-1] * w[:-1]) * dr
        mc = np.cumsum(np.concatenate([[4 / 3 * math.pi * r[0] ** 3 * w[0]], seg]))   # in units of exp(top)
        lM_open = math.log(mc[-1]) + top
        if M_cap is not None and lM_open > math.log(max(M_cap, 1e-300)):
            new = mc / mc[-1] * M_cap; capped = True
        else:
            new = mc * math.exp(top) if top < 700 else mc * 1e300; capped = False
        err = float(np.max(np.abs(new - Md)) / max(np.max(new), 1e-300))
        Md = 0.5 * Md + 0.5 * new
        if err < 1e-7 and it > 5: break
    return dict(r=r, Md=new - Msea, capped=capped, its=it, err=err, conv=bool(err < 1e-7))   # Md = EXCESS over the sea


def Mat(sol, x):
    if x <= sol["r"][0]: return float(sol["Md"][0] * (x / sol["r"][0]) ** 3)
    if x >= sol["r"][-1]: return float(sol["Md"][-1])
    return float(np.interp(math.log(x), np.log(sol["r"]), sol["Md"]))


def grade(c, a0k, base, cap_on=True, Rfac=1.0, variant=False):
    c2 = c * c; o = {}; nconv = 0; ntot = 0
    def cap(Mb): return FCAP * R * Rfac * Mb if cap_on else 0.0
    g5 = []
    for nm, Mb, Ro in G5SYS:
        s = solve_iso(expdisc(Mb, Ro), cap(Mb), c2, r_ta(Mb), a0k); ntot += 1; nconv += s["conv"]
        g5.append(Mat(s, Ro) / Mb)
    o["G5_max"] = max(g5); o["G5"] = bool(o["G5_max"] <= 0.3)
    d = []; sols = {}
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]) / KPC_M; key = round(math.log10(Mb), 6)
        if key not in sols: sols[key] = solve_iso(expdisc(Mb, 3.2 * rd_of(Mb)), cap(Mb), c2, r_ta(Mb), a0k); ntot += 1; nconv += sols[key]["conv"]
        mx = Mat(sols[key], r)                      # excess; beyond r_ta it stays at its r_ta value
        gN = p["gbar"] + G_SI * mx * MS / (r * KPC_M) ** 2
        d.append(math.log10(p["gobs"] / glaw_SI(max(gN, 1e-30), a0k * ACC)))
    o["G6_shift"] = float(np.mean(d)) - base[0]; o["G6"] = bool(abs(o["G6_shift"]) <= 0.05)
    d = []
    for e in EL:
        Mt = e["Mbar"](1e9); s = solve_iso(e["Mbar"], cap(Mt), c2, r_ta(Mt), a0k); ntot += 1; nconv += s["conv"]
        for m in (2, 4, 8):
            x = m * e["Re"]; Mp = glaw(GK * (e["Mbar"](x) + Mat(s, x)) / x ** 2, a0k) * x ** 2 / GK; d.append(math.log10(e["Mtot"](x) / Mp))
    o["G7_shift"] = float(np.mean(d)) - base[1]; o["G7"] = bool(abs(o["G7_shift"]) <= 0.15)
    o["galaxies_pass"] = bool(o["G5"] and o["G6"] and o["G7"])
    xd = []
    for nm, pts in clusters.items():
        Ml, rl = pts[0]["Mb_last"]; host = profile_core([p_["r_kpc"] for p_ in pts], [p_["M_b"] for p_ in pts], Ml, rl, variant)
        s = solve_iso(host, cap(Ml), c2, r_ta(Ml), a0k); ntot += 1; nconv += s["conv"]
        for p_ in pts:
            x = p_["r_kpc"]; Mp = glaw(GK * (p_["M_b"] + Mat(s, x)) / x ** 2, a0k) * x ** 2 / GK; xd.append(math.log10(p_["M_obs"] / Mp))
    xd = np.array(xd); o["X_mean"] = float(xd.mean()); o["X_rms"] = float(np.sqrt((xd ** 2).mean()))
    o["X_pass"] = bool(abs(o["X_mean"]) <= 0.05 and o["X_rms"] <= 0.10)
    gm = {}; strict = {}
    for fst in (0.0, 1.0):
        v = []; npass = 0
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst)
            host = profile_core([q_["r_kpc"] for q_ in gp["pts"]], [q_["M_gas"] * (1 + fst) for q_ in gp["pts"]], Mbt, gp["R5"], variant)
            s = solve_iso(host, cap(Mbt), c2, r_ta(Mbt), a0k); ntot += 1; nconv += s["conv"]; ok = True
            for q_ in gp["pts"]:
                x = q_["r_kpc"]; Mb = q_["M_gas"] * (1 + fst); Mp = glaw(GK * (Mb + Mat(s, x)) / x ** 2, a0k) * x ** 2 / GK
                dl = math.log10(q_["M_obs"] / Mp); v.append(dl); ok &= abs(dl) <= 2 * q_["eM"] / (q_["M_obs"] * math.log(10))
            npass += ok
        gm[fst] = float(np.mean(v)); strict[f"fst{fst:g}"] = int(npass)
    lo, hi = sorted([gm[0.0], gm[1.0]])
    o["G_fst0"] = gm[0.0]; o["G_fst1"] = gm[1.0]; o["G_band"] = bool(lo <= 0.05 and hi >= -0.05); o["G_strict"] = strict
    o["conv_frac"] = nconv / ntot
    return o


def job(arg):
    f, c, kw = arg
    a0k = A0K[f]; return f, c, grade(c, a0k, BASE[f], **kw)


BASE = {f: baselines(a) for f, a in A0K.items()}
if __name__ == "__main__":
    OUT = []
    def P(s=""): print(s, flush=True); OUT.append(str(s))
    P(f"QX12 iter_3 ({'MUTATE' if MUT else 'main'}): isothermal sector in contact with the sea. kappa = 1/2 FITTED; not theory closed.")
    P(f"rho_sea {RHO_D0:.4g} Msun/kpc^3; R {R:.3f}; f_cap {FCAP}. Criteria b605c9fd7c.")
    RES = dict(lane="QX12 iter_3", criteria="b605c9fd7c", mutate=MUT, note="kappa = 1/2 FITTED; not theory closed")
    if not MUT:
        s = solve_iso(pointmass(0.0), None, 6000.0 ** 2, 1000.0, 1.0, law=False, host=False)
        ka1 = float(np.max(np.abs(s["Md"] / (4 / 3 * math.pi * RHO_D0 * s["r"] ** 3))))
        P(f"KA1 uniform sea (no host, c 6000): max rel {ka1:.2e} -> {'PASS' if ka1 <= 1e-6 else 'FAIL'}")
        grid = np.geomspace(100.0, 6000.0, 60)
        with Pool(WK) as pool:
            rows = pool.map(job, [(f, float(c), {}) for f in A0K for c in grid])
        with Pool(WK) as pool:
            rows_v = pool.map(job, [(f, float(c), dict(variant=True)) for f in A0K for c in grid])
        RES["scan_variant"] = {f: [dict(c=c, **o) for ff, c, o in rows_v if ff == f] for f in A0K}
        RES["rd_fit"] = dict(a=RD_A, b=RD_B)
        P(f"A1 r_d fit (SPARC): log r_d = {RD_A:.3f} + {RD_B:.3f} log M_b")
        with Pool(WK) as pool:
            ka3 = dict((f, o) for f, c, o in pool.map(job, [(f, 3000.0, dict(Rfac=0.0)) for f in A0K]))
        RES["KA1"] = ka1; RES["scan"] = {f: [dict(c=c, **o) for ff, c, o in rows if ff == f] for f in A0K}
        RES["KA3"] = {f: ka3[f]["X_mean"] for f in A0K}
        P(f"KA3 (R = 0): X-COP {RES['KA3']['canonical']:+.4f} / {RES['KA3']['alt']:+.4f}")
        RES["foot"] = {}
        for f in A0K:
            sc = RES["scan"][f]; ok = [x["galaxies_pass"] for x in sc]
            cmin = None
            for i in range(len(sc)):
                if all(ok[i:]): cmin = sc[i]; break
            hi = sc[-1]; RES["KA2_" + f] = dict(G6=hi["G6_shift"], G7=hi["G7_shift"], G5=hi["G5_max"])
            P(f"[{f}] KA2 c 6000: G6 {hi['G6_shift']:+.3f}, G7 {hi['G7_shift']:+.3f}, G5 {hi['G5_max']:.3f}")
            for x in sc[::3]:
                P(f"   c {x['c']:7.1f}: G5 {x['G5_max']:.3f} G6 {x['G6_shift']:+.3f} G7 {x['G7_shift']:+.3f} gal {'Y' if x['galaxies_pass'] else 'n'} | "
                  f"X-COP {x['X_mean']:+.3f}/{x['X_rms']:.3f} groups [{x['G_fst1']:+.3f},{x['G_fst0']:+.3f}] strict {x['G_strict']} conv {x['conv_frac']:.2f}")
            if cmin is None:
                lab = "NO VERDICT (no c in grid passes galaxies)"
            else:
                lab = "PASS" if (cmin["X_pass"] and cmin["G_band"]) else "FAIL"
                miss = ("under" if cmin["X_mean"] > 0.05 else ("over" if cmin["X_mean"] < -0.05 else "rms"))
            scv = RES["scan_variant"][f]; okv = [x["galaxies_pass"] for x in scv]; cminv = None
            for i in range(len(scv)):
                if all(okv[i:]): cminv = scv[i]; break
            labv = None if cminv is None else ("PASS" if (cminv["X_pass"] and cminv["G_band"]) else "FAIL")
            if cminv: P(f"[{f}] variant host (core r^max(s0,1.2)): c_min {cminv['c']:.1f}, X-COP {cminv['X_mean']:+.3f}/{cminv['X_rms']:.3f}, groups [{cminv['G_fst1']:+.3f},{cminv['G_fst0']:+.3f}] -> {labv}")
            if cmin and labv != lab: lab = "NO VERDICT (host sensitive)"
            cs = [x for x in sc if cmin and x["c"] >= cmin["c"] and x["X_pass"] and x["G_band"]]
            RES["foot"][f] = dict(c_min=cmin, label=lab, X_miss=(miss if cmin else None), cluster_set_c=[x["c"] for x in cs])
            if cmin:
                P(f"[{f}] c_min = {cmin['c']:.1f} km/s (galaxy gates only). PREDICTION: X-COP {cmin['X_mean']:+.3f}/{cmin['X_rms']:.3f} -> {'PASS' if cmin['X_pass'] else 'FAIL'} ({miss}); "
                  f"groups [{cmin['G_fst1']:+.3f},{cmin['G_fst0']:+.3f}] -> {'PASS' if cmin['G_band'] else 'FAIL'}; strict {cmin['G_strict']}; conv {cmin['conv_frac']:.2f}")
            P(f"[{f}] LABEL: {lab}; c >= c_min passing X-COP and groups band (CLUSTER-SET context): {[round(c,1) for c in RES['foot'][f]['cluster_set_c']]}")
        RES["label"] = "PASS" if all(RES["foot"][f]["label"] == "PASS" for f in A0K) else ("FAIL" if all(RES["foot"][f]["label"] in ("PASS", "FAIL") for f in A0K) else "NO VERDICT")
        P(f"LABEL: {RES['label']}")
    else:
        with Pool(WK) as pool:
            rr = pool.map(job, [(f, 30.0, {}) for f in A0K] + [(f, 1000.0, dict(cap_on=False)) for f in A0K])
        RES["M"] = {}
        for f, c, o in rr:
            key = "M1" if c == 30.0 else "M2"; RES["M"].setdefault(f, {})[key] = o
        for f in A0K:
            m1, m2 = RES["M"][f]["M1"], RES["M"][f]["M2"]
            RES["M"][f]["M1_bites"] = bool(not m1["galaxies_pass"])
            RES["M"][f]["M2_bites"] = bool(abs(m2["X_mean"] - (0.4675 if f == "canonical" else 0.4345)) <= 2e-3)
            P(f"[{f}] M1 c 30 km/s: galaxies pass {m1['galaxies_pass']} (G5 {m1['G5_max']:.2f}, G6 {m1['G6_shift']:+.3f}) -> {'BITES' if RES['M'][f]['M1_bites'] else 'DOES NOT BITE'}; "
              f"M2 M_cap 0: X-COP {m2['X_mean']:+.4f} -> {'BITES' if RES['M'][f]['M2_bites'] else 'DOES NOT BITE'}")
        RES["all_bite"] = bool(all(RES["M"][f]["M1_bites"] and RES["M"][f]["M2_bites"] for f in A0K))
        P(f"MUTATE all bite: {RES['all_bite']}")
    json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
