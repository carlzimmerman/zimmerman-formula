#!/usr/bin/env python3
"""EW4 (criteria origin 8833a24300): nuHDM = the a0 law + one thermal fermion (m 11.1377 eV, g 2, T_nu), Tremaine-Gunn bound.
    python3 ew4_static.py            -> ew4_static.json / .out          (KA1-KA5, then readings C and the computed cells)
    python3 ew4_static.py --mutate   -> ew4_static_MUTATE.json / .out   (M1 m x 0.5, M2 no fermion)
Reading C = Angus-form consistency (required fermion vs phase space) on X-COP, groups, ellipticals; SPARC phase-space ceiling;
UDG lower-bound chi2; KiDS G6 with HC1's R4 fermion. Read-only: gb1.py (exec'd up to main), qx5 loaders, hf1_fermion, UD1/UD2 json.
TEST lane: adopts nothing; no-particle rule relaxed for EW4 only. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
os.environ.setdefault("OMP_NUM_THREADS", "1"); sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
from scipy.stats import chi2 as CHI2
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; TAG = "ew4_static_MUTATE" if MUT else "ew4_static"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

GB1P = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); gsrc = open(GB1P).read()
gcut = gsrc.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GB1P, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(gsrc[:gcut], "gb1_lib", "exec"), NS); sys.argv = _a
G, MS, KPC, PC = NS["G"], NS["MS"], NS["KPC"], NS["PC"]; glaw = NS["glaw"]; Q5 = NS["NS"]
XC, SP, EL, GR = NS["XC"], NS["SP"], NS["EL"], NS["GR"]; LE = Q5["lensing"](); DATA = Q5["DATA"]; XS = Q5["XS"]
GB1J = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))["cands"]["L0"]
sys.path.insert(0, os.path.join(RB, "HF1_hybrid_fermion")); import hf1_fermion as FM

FOOT = dict(NS["A0"])   # the record's footing a0 at full precision (QX5/GB1); 9.3603e-11 / 1.1312e-10 rounded
OMF = 0.11958060485606123; OMB = 0.0215; M0 = 93.14 * OMF; R_FAIR = OMF / OMB; GF = 2.0
H_J, C_L, EV = 6.62607015e-34, 299792458.0, 1.602176634e-19
MSPC3 = MS / PC ** 3
def rho_tg(m_ev, sigma): return FM.rho_cap(m_ev, sigma, GF)
def rho_tg_closed(m_ev, sigma):
    m = m_ev * EV / C_L ** 2; return m ** 4 * (GF / (2 * H_J ** 3)) * (2 * math.pi * sigma ** 2) ** 1.5
def gNinv(g, a0): return g * g / (g + a0)
def dgNdg(g, a0): return (g * g + 2 * g * a0) / (g + a0) ** 2

def region_test(rs, Mobs, Mb, eM, sig, m_ev, a0, Mf_fixed0=False):
    """rs ascending radii (m), Mobs/Mb/eM (kg) at them. Regions: sphere 0->rs[0], shells rs[i]->rs[i+1].
    Returns list of dicts with C-a, C-b verdicts. Mf_fixed0: M2 twin (no fermion allowed: any positive need fails)."""
    rs = np.asarray(rs); g = G * np.asarray(Mobs) / rs ** 2
    Mreq = rs ** 2 * gNinv(g, a0) / G - np.asarray(Mb); er = np.asarray(eM) * dgNdg(g, a0)
    cap = rho_tg(m_ev, sig); out = []
    for i in range(len(rs)):
        if i == 0: dM, e, V, r1 = Mreq[0], er[0], 4 / 3 * math.pi * rs[0] ** 3, 0.0
        else: dM, e, V, r1 = Mreq[i] - Mreq[i - 1], math.hypot(er[i], er[i - 1]), 4 / 3 * math.pi * (rs[i] ** 3 - rs[i - 1] ** 3), rs[i - 1]
        ca = dM + 2 * e >= 0
        lo = max(dM - 2 * e, 0.0) / V
        cb = (lo <= 0.0) if Mf_fixed0 else (lo <= cap)
        mmin = m_ev * (lo / cap) ** 0.25 if lo > 0 else 0.0
        out.append(dict(m_min_eV=mmin, r_in_kpc=r1 / KPC, r_out_kpc=rs[i] / KPC, dMreq_Msun=dM / MS, err_Msun=e / MS, rho_lo_Msunpc3=lo / MSPC3,
                        rho_tg_Msunpc3=cap / MSPC3, Ca=bool(ca), Cb=bool(cb), ok=bool(ca and cb)))
    return out, float(Mreq[-1] / MS)

# ------------------------------------------------------------------ X-COP (QX5 points; R500 from the hydro header)
def xcop_clusters():
    cl = {}
    for z in XC: cl.setdefault(z["name"], []).append(z)
    out = []
    for n, pts in cl.items():
        with fits.open(os.path.join(DATA, "xcop", n, f"{n}_hydro_mass.fits")) as h: r500 = float(h[1].header["R500"])
        pts = sorted(pts, key=lambda p: p["r_kpc"]); hr, hM = np.asarray(pts[0]["hr"], float), np.asarray(pts[0]["hM"], float)
        ok = (hr > 0) & np.isfinite(hM) & (hM > 0)
        vcmax = float(np.max(np.sqrt(G * hM[ok] * MS / (hr[ok] * KPC))))
        out.append(dict(name=n, r500=r500, pts=pts, vcmax=vcmax, xs=[p["r_kpc"] / r500 for p in pts]))
    return out

def c_xcop(a0, m_ev, sigf=1 / math.sqrt(2), zero=False):
    res = []
    for c in xcop_clusters():
        sig = c["vcmax"] * sigf
        rs = [p["r_kpc"] * KPC for p in c["pts"]]
        reg, Mlast = region_test(rs, [p["M_obs"] * MS for p in c["pts"]], [p["M_b"] * MS for p in c["pts"]],
                                 [p["eM"] * MS for p in c["pts"]], sig, m_ev, a0, zero)
        bad_b = [r for r in reg if not r["Cb"]]; bad_a = [r for r in reg if not r["Ca"]]
        res.append(dict(name=c["name"], sigma_kms=sig / 1e3, xs=[round(x, 3) for x in c["xs"]], ok=all(r["ok"] for r in reg),
                        n_fail_regions=sum(not r["ok"] for r in reg), fail_Cb_outer_kpc=max([r["r_out_kpc"] for r in bad_b], default=0.0),
                        fail_Ca=[(round(r["r_in_kpc"]), round(r["r_out_kpc"])) for r in bad_a],
                        supply=Mlast / (R_FAIR * c["pts"][-1]["M_b"]), m_min_eV=max(r["m_min_eV"] for r in reg), Mreq_over_Mb=Mlast / c["pts"][-1]["M_b"], regions=reg))
    n = sum(r["ok"] for r in res)
    return dict(n_ok=int(n), N=len(res), label="PASS" if n >= 10 else "FAIL", label_80pct="PASS" if n >= 0.8 * len(res) else "FAIL", clusters=res)

def xcop_gasonly(a0, m_ev):
    """Reported only: the 5 X-COP clusters QX5 drops (no stellar-mass file); baryons = gas only (M_req over-estimated)."""
    li = Q5["li"]; have = {c["name"] for c in xcop_clusters()}; out = []
    for n in sorted(os.listdir(os.path.join(DATA, "xcop"))):
        p_ = os.path.join(DATA, "xcop", n)
        if n in have or not os.path.isdir(p_): continue
        with fits.open(os.path.join(p_, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
        with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
        hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); gr = np.array(gas["RADIUS"], float) * rg500; gM = np.array(gas["MGAS"], float)
        pts = []
        for x in XS:
            r = x * r500; mh = li(hr, hM, r); mg = li(gr, gM, r); em = li(hr, np.array(hm["EM_FORW"], float), r)
            if np.all(np.isfinite([mh, mg])): pts.append((r, mh, mg, em))
        if len(pts) < 2: continue
        ok = (hr > 0) & np.isfinite(hM) & (hM > 0); sig = float(np.max(np.sqrt(G * hM[ok] * MS / (hr[ok] * KPC)))) / math.sqrt(2)
        reg, Ml = region_test([p[0] * KPC for p in pts], [p[1] * MS for p in pts], [p[2] * MS for p in pts], [p[3] * MS for p in pts], sig, m_ev, a0)
        out.append(dict(name=n, n_pts=len(pts), ok=all(r["ok"] for r in reg), fail_Ca=sum(not r["Ca"] for r in reg), fail_Cb=sum(not r["Cb"] for r in reg),
                        m_min_eV=max(r["m_min_eV"] for r in reg), Mreq_over_Mgas=Ml / pts[-1][2]))
    return out

def c_groups(a0, m_ev, sigf=1 / math.sqrt(2), zero=False):
    o = {}
    for fst in (0, 1):
        rows = []
        for gp in GR:
            pts = gp["pts"]; rs = [p["r_kpc"] * KPC for p in pts]
            vc = max(math.sqrt(G * p["M_obs"] * MS / (p["r_kpc"] * KPC)) for p in pts); sig = vc * sigf
            reg, Ml = region_test(rs, [p["M_obs"] * MS for p in pts], [p["M_gas"] * (1 + fst) * MS for p in pts],
                                  [p["eM"] * MS for p in pts], sig, m_ev, a0, zero)
            rows.append(dict(name=gp["name"], kT=gp["kT"], ok=all(r["ok"] for r in reg), Ca=all(r["Ca"] for r in reg), Cb=all(r["Cb"] for r in reg),
                             Mreq_over_Mb=Ml / (pts[-1]["M_gas"] * (1 + fst)), sigma_kms=sig / 1e3, m_min_eV=max(r["m_min_eV"] for r in reg)))
        n = sum(r["ok"] for r in rows)
        o[f"fst{fst}"] = dict(n_ok=int(n), n_fail_Ca=sum(not r["Ca"] for r in rows), n_fail_Cb=sum(not r["Cb"] for r in rows),
                              hot_ok=f"{sum(r['ok'] for r in rows if r['kT'] >= 2)}/{sum(r['kT'] >= 2 for r in rows)}",
                              cool_ok=f"{sum(r['ok'] for r in rows if r['kT'] < 2)}/{sum(r['kT'] < 2 for r in rows)}", rows=rows)
    o["label"] = "PASS" if all(o[k]["n_ok"] >= 16 for k in ("fst0", "fst1")) else "FAIL"
    return o

def c_ell(a0, m_ev, sigf=1 / math.sqrt(2), zero=False):
    rows = []
    for e in EL:
        rg = np.linspace(2 * e["Re"], 8 * e["Re"], 400); vc = max(math.sqrt(G * e["Mtot"](x) * MS / (x * KPC)) for x in rg); sig = vc * sigf
        rr = [2 * e["Re"], 4 * e["Re"], 8 * e["Re"]]
        reg, Ml = region_test([x * KPC for x in rr], [e["Mtot"](x) * MS for x in rr], [e["Mbar"](x) * MS for x in rr], [0.0] * 3, sig, m_ev, a0, zero)
        rows.append(dict(name=e["name"], ok=all(r["ok"] for r in reg), Ca=all(r["Ca"] for r in reg), Cb=all(r["Cb"] for r in reg),
                         sigma_kms=sig / 1e3, Mreq_over_Mb_8Re=Ml / e["Mbar"](8 * e["Re"]), rho_lo_max=max(r["rho_lo_Msunpc3"] for r in reg),
                         rho_tg=reg[0]["rho_tg_Msunpc3"], m_min_eV=max(r["m_min_eV"] for r in reg)))
    n = sum(r["ok"] for r in rows)
    return dict(n_ok=int(n), N=len(rows), label="PASS" if n >= 0.8 * len(rows) else "FAIL", rows=rows)

# ------------------------------------------------------------------ SPARC phase-space ceiling
def sparc(a0, m_ev, off=False):
    res, ratio, rhos = [], [], []
    for g in SP:
        r, V = g["R"], g["V"]; gobs = V ** 2 / r; gbar = g["vb2"] / r
        sig = float(np.max(V)) / math.sqrt(2); cap = 0.0 if off else rho_tg(m_ev, sig)
        Mf = 4 / 3 * math.pi * r ** 3 * cap; gf = G * Mf / r ** 2
        res += list(np.log10(gobs / np.array([glaw(x + y, a0) for x, y in zip(gbar, gf)])))
        ratio.append(float(Mf[-1] / (g["vb2"][-1] * r[-1] / G))); rhos.append(cap / MSPC3)
    res = np.array(res); Z = float(res.mean()); rms = float(np.sqrt((res ** 2).mean()))
    return dict(Z=Z, rms=rms, ratio_med=float(np.median(ratio)), ratio_max=float(np.max(ratio)),
                rho_tg_med=float(np.median(rhos)), rho_tg_range=[float(min(rhos)), float(max(rhos))])

# ------------------------------------------------------------------ UDGs: lower-bound chi2 (a fermion only adds field)
U1 = json.load(open(os.path.join(RB, "UD1_agc114905_udg_rotation", "ud1.json")))
U2 = json.load(open(os.path.join(RB, "UD2_malin1_giant_lsb", "ud2.json")))
UD2_V = np.array([236.9, 216.2, 197.4, 214.1]); UD2_E = np.array([9.4, 2.6, 4.7, 11.8])   # ud2.py Table 3 (typed there)
def udg(f):
    o = {}
    for name, V, E, Vl, chi_rec in (("AGC 114905", np.array(U1["data2024"]["V"]), np.array(U1["data2024"]["E"]), np.array(U1[f]["Vlaw"]), U1[f]["chi2"]),
                                     ("Malin 1", UD2_V, UD2_E, np.array(U2[f]["Vlaw"]), U2[f]["chi2"])):
        chi_law = float(np.sum(((Vl - V) / E) ** 2)); over = Vl > V
        cmin = float(np.sum((((Vl - V) / E) ** 2)[over])); p = float(CHI2.sf(cmin, len(V)))
        o[name] = dict(chi2_law=chi_law, chi2_rec=chi_rec, KA4=abs(chi_law / chi_rec - 1) <= 1e-3, n_over=int(over.sum()), N=len(V),
                       chi2_min_any_fermion=cmin, p=p, label="FAIL" if p < 0.01 else "C PASS (needs P)")
    return o

# ------------------------------------------------------------------ KiDS G6 with HC1's R4 fermion
MPC = 3.0857e22; RHO_M0 = (OMB + OMF) * 2.775e11 * MS / MPC ** 3
def rta_of(Mtot): return (3 * (1 + R_FAIR) * Mtot / (4 * math.pi * 5.55 * RHO_M0)) ** (1 / 3)
def kids_g6(a0, m_ev, off=False):
    ah = 3 * KPC; bins = {}
    for p in LE: bins.setdefault(p["Mb"], []).append(p)
    shifts, per = [], {}
    for Mb, pts in sorted(bins.items()):
        rr = np.array([math.sqrt(G * Mb / p["gbar"]) for p in pts])
        if off: Mf_at = np.zeros_like(rr); sig = 0.0
        else:
            rg = np.geomspace(0.01 * KPC, max(rta_of(Mb), 1.001 * rr.max()), 360); Mbg = Mb * rg ** 2 / (rg + ah) ** 2
            s = FM.solve(rg, Mbg, rg[-1], rr.max(), R_FAIR * Mb, m_ev, a0, gf=GF, capf=1.0, iters=300, G_=G)
            Mf_at = np.exp(np.interp(np.log(rr), np.log(rg), np.log(np.maximum(s["Mf"], 1e-300)))); sig = float(s["sigma"])
        gNb = G * Mb / (rr + ah) ** 2; gNf = G * Mf_at / rr ** 2
        sh = np.log10(np.array([glaw(x, a0) for x in gNb]) / np.array([glaw(x + y, a0) for x, y in zip(gNb, gNf)]))
        shifts += list(sh); per[f"{math.log10(Mb / MS):.2f}"] = dict(mean_shift=float(sh.mean()), Mf_over_Mb_outer=float(Mf_at[int(np.argmax(rr))] / Mb),
                                                                   r_kpc=[float(rr.min() / KPC), float(rr.max() / KPC)], sigma_kms=sig / 1e3)
    g6 = float(np.mean(shifts)); return dict(G6=g6, label="PASS" if abs(g6) <= 0.05 else "FAIL", bins=per)

# ------------------------------------------------------------------ run
J = dict(tag=TAG, criteria="8833a24300 (origin; local 1e3cca4d5c)", m_ev=M0, R=R_FAIR, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
P(f"EW4 {TAG}: m {M0:.4f} eV, g 2, R {R_FAIR:.4f}; a0 {FOOT}. TEST lane; no-particle rule relaxed for EW4 only.")
ka = {}
ka["KA2"] = abs(rho_tg(M0, 7e5) / rho_tg_closed(M0, 7e5) - 1); P(f"KA2 rho_TG vs closed form |d| {ka['KA2']:.1e} -> {'PASS' if ka['KA2'] <= 1e-12 else 'FAIL'}")
for f, a0 in FOOT.items():
    # KA1: M_f = 0 reproduces GB1 L0 X-COP mean/rms and groups 0/20
    B = NS["build"](f, a0)[2]; d = np.array([p["D"] for p in B]); xm, xr = float(d.mean()), float(np.sqrt((d ** 2).mean()))
    gl = GB1J[f]["G2 X-COP"]["num"]; k1 = max(abs(xm - gl["mean"]), abs(xr - gl["rms"]))
    ka[f"KA1_{f}"] = k1; P(f"[{f}] KA1 X-COP L0 mean {xm:+.6f} rms {xr:.6f} vs GB1 {gl['mean']:+.6f} {gl['rms']:.6f}: |d| {k1:.1e} -> {'PASS' if k1 <= 1e-6 else 'FAIL'}")
    s0 = sparc(a0, M0, off=True); gs = GB1J[f]["G1 SPARC"]["num"]; k3 = max(abs(s0["Z"] - gs["Z"]), abs(s0["rms"] - gs["rms"]))
    ka[f"KA3_{f}"] = k3; P(f"[{f}] KA3 SPARC L0 Z {s0['Z']:+.6f} rms {s0['rms']:.6f} vs GB1: |d| {k3:.1e} -> {'PASS' if k3 <= 1e-9 else 'FAIL'}")
    u = udg(f); k4 = all(v["KA4"] for v in u.values()); ka[f"KA4_{f}"] = k4
    P(f"[{f}] KA4 UD1/UD2 law chi2 {[round(v['chi2_law'], 3) for v in u.values()]} vs record {[round(v['chi2_rec'], 3) for v in u.values()]} -> {'PASS' if k4 else 'FAIL'}")
    k5 = abs(kids_g6(a0, M0, off=True)["G6"]); ka[f"KA5_{f}"] = k5; P(f"[{f}] KA5 KiDS G6 no fermion {k5:.1e} -> {'PASS' if k5 <= 1e-12 else 'FAIL'}")
KA_OK = ka["KA2"] <= 1e-12 and all(ka[f"KA1_{f}"] <= 1e-6 and ka[f"KA3_{f}"] <= 1e-9 and ka[f"KA4_{f}"] and ka[f"KA5_{f}"] <= 1e-12 for f in FOOT)
J["KA"] = ka; J["KA_all"] = KA_OK; P(f"KA all: {'PASS' if KA_OK else 'FAIL -> nothing graded'}")
if not KA_OK:
    json.dump(J, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float); open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)

runs = [("M1_m_half", 0.5 * M0, False), ("M2_no_fermion", M0, True)] if MUT else [("main", M0, False)]
for f, a0 in FOOT.items():
    J[f] = {}
    for lab, m, zero in runs:
        X = c_xcop(a0, m, zero=zero); Gp = c_groups(a0, m, zero=zero); E = c_ell(a0, m, zero=zero)
        r = dict(xcop=X, groups=Gp, ell=E); J[f][lab] = r
        P(f"[{f}] {lab:13s} C X-COP {X['label']}: {X['n_ok']}/{X['N']} clusters consistent (line >= 10)")
        for c in X["clusters"]:
            P(f"      {c['name']:6s} sigma {c['sigma_kms']:6.0f} km/s  fail regions {c['n_fail_regions']}  C-b fails out to {c['fail_Cb_outer_kpc']:6.0f} kpc  C-a fails {c['fail_Ca']}  M_req/M_b {c['Mreq_over_Mb']:.2f}  supply use {c['supply']:.2f}  TG m_min {c['m_min_eV']:.2f} eV")
        P(f"[{f}] {lab:13s} C groups {Gp['label']}: f*0 {Gp['fst0']['n_ok']}/20 (C-a fails {Gp['fst0']['n_fail_Ca']}, C-b fails {Gp['fst0']['n_fail_Cb']}; kT>=2 {Gp['fst0']['hot_ok']}, kT<2 {Gp['fst0']['cool_ok']}); "
          f"f*1 {Gp['fst1']['n_ok']}/20 (C-a {Gp['fst1']['n_fail_Ca']}, C-b {Gp['fst1']['n_fail_Cb']}; hot {Gp['fst1']['hot_ok']}, cool {Gp['fst1']['cool_ok']})")
        P(f"[{f}] {lab:13s} reported TG m_min (eV, phase-space floor from C-b): X-COP max {max(c['m_min_eV'] for c in X['clusters']):.2f}; groups f*0 median {np.median([r['m_min_eV'] for r in Gp['fst0']['rows']]):.2f} max {max(r['m_min_eV'] for r in Gp['fst0']['rows']):.2f}; f*1 max {max(r['m_min_eV'] for r in Gp['fst1']['rows']):.2f}; ellipticals median {np.median([e['m_min_eV'] for e in E['rows']]):.2f} range {min(e['m_min_eV'] for e in E['rows']):.2f}-{max(e['m_min_eV'] for e in E['rows']):.2f}")
        P(f"[{f}] {lab:13s} C ellipticals {E['label']}: {E['n_ok']}/{E['N']} " + "; ".join(f"{e['name']} Ca {int(e['Ca'])} Cb {int(e['Cb'])} rho_lo_max {e['rho_lo_max']:.2e} vs TG {e['rho_tg']:.2e}" for e in E["rows"]))
    if not MUT:
        Xg = c_xcop(a0, M0, sigf=1.0); Gg = c_groups(a0, M0, sigf=1.0); Eg = c_ell(a0, M0, sigf=1.0)
        J[f]["generous_sigma_vcmax"] = dict(xcop=[Xg["n_ok"], Xg["label"]], groups=[Gg["fst0"]["n_ok"], Gg["fst1"]["n_ok"], Gg["label"]], ell=[Eg["n_ok"], Eg["label"]])
        xg = xcop_gasonly(a0, M0); J[f]["xcop_gasonly_reported"] = xg
        P(f"[{f}] X-COP C on the 80 % line the criteria named (6 of 7 needed... computed): {J[f]['main']['xcop']['n_ok']}/{J[f]['main']['xcop']['N']} -> {J[f]['main']['xcop']['label_80pct']}")
        P(f"[{f}] reported, 5 X-COP clusters without stellar files (gas only): " + "; ".join(f"{c['name']} pts {c['n_pts']} ok {int(c['ok'])} Ca-fails {c['fail_Ca']} Cb-fails {c['fail_Cb']} m_min {c['m_min_eV']:.2f} eV M_req/M_gas {c['Mreq_over_Mgas']:.2f}" for c in xg))
        P(f"[{f}] reported, generous sigma = V_c,max: X-COP {Xg['n_ok']}/12 {Xg['label']}; groups {Gg['fst0']['n_ok']}/{Gg['fst1']['n_ok']} {Gg['label']}; ellipticals {Eg['n_ok']}/{Eg['N']} {Eg['label']}")
        s = sparc(a0, M0); line = GB1J[f]["G1 SPARC"]["num"]["rms_line"]; ok = abs(s["Z"]) <= 0.057 and s["rms"] <= line
        s.update(rms_line=line, label="PASS (robust, at the phase-space ceiling)" if ok else "ceiling FAILS G1 -> cell takes HC1 P (G1 PASS), not robust"); J[f]["sparc_ceiling"] = s
        P(f"[{f}] SPARC at the phase-space ceiling: Z {s['Z']:+.4f} rms {s['rms']:.4f} (line 0.057 / {line:.4f}); M_f,max/M_b at R_last median {s['ratio_med']:.3f} max {s['ratio_max']:.2f}; "
          f"rho_TG median {s['rho_tg_med']:.2e} Msun/pc^3 range {s['rho_tg_range'][0]:.1e}-{s['rho_tg_range'][1]:.1e} -> {s['label']}")
        u = udg(f); J[f]["udg"] = u
        for k, v in u.items(): P(f"[{f}] {k}: rings over-predicted by the law {v['n_over']}/{v['N']}; chi2_min over ANY fermion {v['chi2_min_any_fermion']:.1f}/{v['N']} p {v['p']:.1e} -> {v['label']}")
        kg = kids_g6(a0, M0); J[f]["kids_g6"] = kg
        P(f"[{f}] KiDS G6 (HC1 R4 fermion): G6 {kg['G6']:+.4f} dex (line |G6| <= 0.05) -> {kg['label']}; bins " + json.dumps({k: [round(v['mean_shift'], 3), round(v['Mf_over_Mb_outer'], 2), round(v['sigma_kms'])] for k, v in kg["bins"].items()}))
if MUT:
    for f, a0 in FOOT.items():
        m1 = J[f]["M1_m_half"]["xcop"]; m2 = J[f]["M2_no_fermion"]["xcop"]
        P(f"[{f}] MUTATE M1 m x 0.5: X-COP C {m1['n_ok']}/{m1['N']} consistent; M2 no fermion: X-COP C {m2['n_ok']}/{m2['N']} consistent; law-only mean = KA1 value")
P("TEST lane; adopts nothing; no-particle rule relaxed for EW4 only. kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(J, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
