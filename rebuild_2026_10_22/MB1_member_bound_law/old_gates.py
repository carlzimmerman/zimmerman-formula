#!/usr/bin/env python3
"""RQ3: old gates wired to a candidate's g, from on-disk paths, read only. Each source's data and estimator; g replaces its kernel. Rows and known answers in FROZEN_CRITERIA.md section 4. kappa = 1/2 FITTED; not theory closed."""
import csv, math, os, sys, types
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); CFG = os.path.join(REPO, "campaign_fresh_gravity"); HUNT = os.path.join(REPO, "hunt_2026")
_C = {}
def _src():
    if "ex" not in _C:
        sys.path.insert(0, CFG); sys.path.insert(0, HUNT); import CFG4_common as C4; _C["ex"] = C4.exec_slices
    return _C["ex"]

# ---------- A20
def a20(call, zrow, foot, c, a0):
    gb = np.array([1e-4 * a0]); v = float(call(c, gb=gb, gg=gb * 0, gs=gb, r=gb * 0 + 1e20, a0=a0, sample="deep")[0]); ae = v * v / gb[0]
    return {"A20": zrow(ae * 1e10, 1.20, math.hypot(.02, .24), "inside 1.20 +- 0.02 +- 0.24", "a_eff = g^2/g_b at g_b = 1e-4 a0; g-dagger band; older chain")}

# ---------- A21, CFG4 H5
def btfr_fit(logV, sV, logM, sM, slope=None):
    def nll(p):
        s = slope if slope is not None else p[0]; b = p[-2]; si = abs(p[-1]); var = sM ** 2 + (s * sV) ** 2 + si ** 2; return 0.5 * np.sum((logM - s * logV - b) ** 2 / var + np.log(var))
    return minimize(nll, ([4.0] if slope is None else []) + [2.0, 0.05], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 20000}).x
def a21(call, lrow, foot, c, a0, Cs, CRG):
    U = dict(canonical=.61, alt=.57)[foot]; X = {}
    for l in open(os.path.join(CRG, "inputs", "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) == 19:
            try: X[t[0]] = (float(t[2]), float(t[3]), float(t[16]))
            except ValueError: pass
    G = [g for g in Cs.load_gal() if g["Q"] <= 2 and g["Vflat"] > 0 and X[g["name"]][2] / g["Vflat"] <= .1]; LN = math.log(10); Mst = np.array([U * g["L36"] * 1e9 for g in G]); Mb = Mst + np.array([1.33 * g["MHI"] * 1e9 for g in G]); V = np.array([g["Vflat"] for g in G]); eV = np.array([X[g["name"]][2] for g in G]); D = np.array([X[g["name"]][0] for g in G]); eD = np.array([X[g["name"]][1] for g in G])
    lV, sV = np.log10(V), eV / V / LN; lM = np.log10(Mb); sM = np.sqrt((2 * eD / D / LN) ** 2 + (.10 * Mst / Mb) ** 2); sl = btfr_fit(lV, sV, lM, sM)[0]; b4 = btfr_fit(lV, sV, lM, sM, 4.0)[0]; VL = []
    for g, lgm in zip(G, lM):
        gas = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; gb = gas + (U * g["Vdisk"] ** 2 + 1.4 * U * g["Vbul"] ** 2) * 1e6 / g["R"]; ok = gb > 0
        v = call(c, gb=np.where(ok, gb, 1.0), gg=gas, gs=gb - gas, r=g["R"], a0=a0, sample="disc", lgMb=g["lgMb"], name=g["name"]); vl = np.where(ok, np.sqrt(np.maximum(v * g["R"], 0)) / 1e3, np.nan); n3 = max(3, len(gb) // 3); m = np.nanmean(vl[-n3:]); VL.append(m * g["Vflat"] / np.nanmean(g["Vobs"][-n3:]) if np.isfinite(m) else np.nan)
    VL = np.array(VL); mm = np.isfinite(VL) & (VL > 0); bl = btfr_fit(np.log10(VL[mm]), sV[mm], lM[mm], sM[mm], 4.0)[0]; d = float(b4 - bl)
    return {"A21": lrow(abs(d) <= .10, d, "H5 |obs - model| <= 0.10; GATES 0.053 " + ("met" if abs(d) <= .053 else "missed"), f"n {len(G)}, slope {sl:.3f} on data, U {U}; LINE ONLY")}

# ---------- A23, CFG7 tdg and hierarchy
def a23(call, zrow, NC, foot, c, a0):
    GK = 4.30091727e-6; KM = 3.0856775814913673e19; ACC = 1e6 / KM; rows = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv")))); F = lambda r, k: float(r[k])
    Vo = np.array([F(r, "V_circ_kms") for r in rows]); Eo = np.array([F(r, "e_V_circ_kms") for r in rows]); MB = np.array([F(r, "M_bar_1e8") * 1e8 for r in rows]); EMB = np.array([F(r, "e_M_bar_1e8") * 1e8 for r in rows]); RO = np.array([F(r, "R_out_kpc") for r in rows]); ERO = np.array([F(r, "e_R_out_kpc") for r in rows]); fg = np.array([(F(r, "M_atom_1e8") + F(r, "M_mol_1e8")) / F(r, "M_bar_1e8") for r in rows]); rm = RO * KM
    def cg(x, i): v = np.array([x]); return float(call(c, gb=v, gg=v * fg[i], gs=v * (1 - fg[i]), r=np.array([rm[i]]), a0=a0, sample="tdg")[0])
    def V(i, Mb, Ro, hf):
        gi = GK * Mb / Ro ** 2 * ACC
        if hf is None: ai = cg(gi, i)
        else: ge = GK * .6 * F(rows[i], "host_LK_1e10Lsun") * 1e10 * hf / F(rows[i], "D_p_kpc") ** 2 * ACC; ai = cg(gi + ge, i) - cg(ge, i)
        return math.sqrt(max(ai, 0) / ACC * Ro)
    def c2i(i, hf):
        v = V(i, MB[i], RO[i], hf); dm = (V(i, MB[i] * 1.01, RO[i], hf) - v) / (.01 * MB[i]) * EMB[i]; dr = (V(i, MB[i], RO[i] * 1.01, hf) - v) / (.01 * RO[i]) * ERO[i]; return (Vo[i] - v) ** 2 / (Eo[i] ** 2 + dm ** 2 + dr ** 2)
    iso = sum(c2i(i, None) for i in range(len(rows))); hosts = sorted({r["host"] for r in rows}) if "host" in rows[0] else None
    hk = "host" if hosts else [k for k in rows[0] if k.lower().startswith("host") and "LK" not in k][0]; hosts = sorted({r[hk] for r in rows}); efe = 0.0; best = {}
    for h in hosts:
        ii = [i for i, r in enumerate(rows) if r[hk] == h]; opts = {f: sum(c2i(i, f) for i in ii) for f in (.5, 1., 2.)}; f = min(opts, key=opts.get); best[h] = f; efe += opts[f]
    from scipy.stats import chi2 as _x
    R = {"A23a": dict(label="PASS" if efe <= 12.6 else "FAIL", value=float(efe), chi2_iso=float(iso), chi2_field=float(efe), host_fac=best, p=float(_x.sf(efe, 6)), old="Newton chi^2 <= 12.6 for 6", note="algebraic field, best host mass per host, the most favourable to the candidate; D (equilibrium)")}
    HL = _hl(); Gs, Ms = HL.G, HL.Msun; o = {}
    for nm, LV, rh0, s, em, ep in (("DF2", 1.1e8, 2200. * .75, 8.5, 3.1, 2.3), ("DF4", 1.0e8, 1600. * .75, 4.2, 2.2, 4.4)):
        Mb = 2. * LV; rh = 4. / 3. * rh0 * 3.0857e16; gi = Gs * .5 * Mb * Ms / rh ** 2; v = np.array([gi]); ai = float(call(c, gb=v, gg=v * 0, gs=v, r=np.array([rh]), a0=a0, sample="df")[0]); sp = math.sqrt(max(ai, 0) * rh / 3.) / 1e3; B = 2 * math.log10(s / sp); e = em if B > 0 else ep; o[nm] = float(B / (2. * e / (s * math.log(10))))
    w = max(o.values(), key=abs); R["A23b"] = dict(label="PASS" if max(abs(v) for v in o.values()) <= 2 else "FAIL", Z=float(w), bins=o, old="Newton <= 2 sigma at 20 Mpc", note="isolated g, no field; D (distance, contested DF)")
    return R
def _hl():
    if "hl" not in _C: _src(); import hunt_lib as HL; _C["hl"] = HL
    return _C["hl"]

# ---------- A24, CFG31 R1
def a24(call, zrow, foot, c, a0):
    ex = _src()
    if "udg" not in _C: _C["udg"] = ex(os.path.join(REPO, "fable_independent_2026", "L23_udg_verify.py"), [(None, 'H("2. CONTROL A')], name="l23")[0]
    n = _C["udg"]; U = n["UDG"]; G_ = n["G"]; ms = np.array([u["Mst"] for u in U]); r12 = np.array([u["r12"] for u in U]); go = np.array([u["gobs"] for u in U]); W = 1 / np.array([u["err"] for u in U]) ** 2; gb = G_ * (ms / 2) / r12 ** 2
    v = call(c, gb=gb, gg=gb * 0, gs=gb, r=r12, a0=a0, sample="udg"); m = float((W * (np.log10(go) - np.log10(v))).sum() / W.sum()); import json as _j
    tot = _j.load(open(os.path.join(CFG, "CFG31_coma_udgs_under_b_results.json")))["numbers"]["reported"]["R1_stars_only"][foot]["tot"]
    return {"A24": zrow(m, 0.0, tot, "<= 2 sigma, on infall baryons, a class rule, not wired", "stars only, isolated; CFG31's recorded floor, which was computed on the law")}

# ---------- A25, CFG7 H2
def a25(call, foot, c, a0):
    HL = _hl()
    if "gc" not in _C:
        S = open(os.path.join(CFG, "CFG7_hierarchy_fg001.py")).read(); i = S.index("def num13(s):"); j = S.index("def pred_sigma13"); n = dict(np=np, math=math, re=__import__("re"), os=os, G=HL.G, kpc=HL.kpc, Msun=HL.Msun, C=types.SimpleNamespace(REPO=REPO)); exec(compile(S[i:j], "gc", "exec"), n); _C["gc"] = n["gcs"]
    D = [r for r in _C["gc"] if r["g_int"] < a0 and r["g_ext"] < a0 and np.isfinite(r["sig0"]) and r["sig0"] > 0 and r["nrv"] >= 20 and np.isfinite(r["MLV"]) and r["MLV"] > 0]; ml = []
    for r in D: v = np.array([r["g_int"] + r["g_ext"]]); ml.append(r["MLV"] / (float(call(c, gb=v, gg=v * 0, gs=v, r=np.array([r["rhm"]]), a0=a0, sample="gc")[0]) / v[0]))
    ml = np.array(ml); med = float(np.median(ml)); err = 1.2533 * float(np.std(ml, ddof=1)) / math.sqrt(len(ml)); z = 0.0 if 1. <= med <= 2.5 else (med - (1. if med < 1 else 2.5)) / err
    return {"A25": dict(label="PASS" if abs(z) <= 2 else "FAIL", value=med, Z=float(z), sigma=err, old="M/L_V inside 1.0-2.5", note=f"n {len(D)}, algebraic field; Z is distance outside the range, stat-only; not discriminating (GATES)")}

# ---------- A26a, h50; A26b, CFG32
def a26(call, zrow, foot, c, a0):
    ex = _src(); R = {}
    if "h50" not in _C: _C["h50"] = ex(os.path.join(HUNT, "h50_gc_dispersions.py"), [(None, 'P(f"  (sig_obs and the three models are averaged over the bins outside max(1 R_e, 2 kpc)')], name="h50")[0]
    n = _C["h50"]; off = []; G_, KP, MS = n["G"], n["kpc"], n["Msun"]; GA = n["GAMMA"]
    for r in n["res"]:
        ah = r["Re"] / 1.8153
        def gf(rr):
            rr = np.asarray(rr, float); Mb = r["Mstar"] * MS * rr ** 2 / (rr + ah) ** 2; gN = G_ * Mb / (rr * KP) ** 2; return call(c, gb=gN, gg=gN * 0, gs=gN, r=rr * KP, a0=a0, sample="et")
        s = n["sigma_los"](r["Rb"], n["sigma_r2"](gf, GA), GA); off.append(float(np.mean(np.log10(r["Sb"][r["out"]] / s[r["out"]]))))
    off = np.array(off); R["A26a"] = zrow(float(off.mean()), 0.0, float(off.std(ddof=1) / math.sqrt(len(off))), "<= 2 sigma", "SLUGGS 19, stars only, gamma 3 tracer, stat-only; D (anisotropy, IMF)")
    if "h10" not in _C: _C["h10"] = ex(os.path.join(HUNT, "h10_h18_xray_hse.py"), [(None, 'P("="*116); P("ITEM 10'), ('rows = [l.rstrip("\\n").split("\\t") for l in open(os.path.join(DATA, "humphrey2006', 'm10c, s10c, y10, r10 = R10["canonical"]')], name="h10")[0]
    n = _C["h10"]; G_, KP, MS = n["G"], n["kpc"], n["Msun"]; RD = (5., 10., 20., 40., 70.)
    def sample(ups="uk", radii=RD):
        per = []
        for g in n["gal"]:
            Mf = g["uf"] * g["LK"]; Md = max(g["Mvir"] - Mf, 1e9); Ms = g[ups] * g["LK"]; o = []
            for r in radii:
                Mt = n["M_hern"](r, Mf, g["Re"]) + n["M_nfw"](r, Md, g["Rvir"], g["c"]); Mb = n["M_hern"](r, Ms, g["Re"]); rr = r * KP; go = G_ * Mt * MS / rr ** 2; gb = G_ * Mb * MS / rr ** 2; v = np.array([gb]); o.append(math.log10(go / float(call(c, gb=v, gg=v * 0, gs=v, r=np.array([rr]), a0=a0, sample="et")[0])))
            per.append(np.median(o))
        per = np.array(per); return float(per.mean()), float(per.std(ddof=1) / math.sqrt(len(per)))
    m, e = sample(); fl = math.hypot(abs(sample("us")[0] - m), abs(sample(radii=RD[:4])[0] - m))
    R["A26b"] = zrow(m, 0.0, math.hypot(e, fl), "MARGINAL/FAIL", "7 X-ray ellipticals, fitted models, IMF and radial floor, no hot gas; D (IMF)")
    return R

# ---------- B2, CFG34
def b2(call, zrow, foot, c, a0):
    ex = _src()
    if "h7" not in _C: _C["h7"] = ex(os.path.join(HUNT, "h7_groups_hot_gas.py"), [(None, 'P("="*116); P("ITEM 7A'), ('lp = os.path.join(DATA, "lovisari2015_groups.tsv")', "R7B = {}")], name="h7")[0]
    n = _C["h7"]; GR, ms5, FIN, SBR = n["gr"], n["mstar500"], n["FIN"], n["SBR"]; G_, KP, MS = n["G"], n["kpc"], n["Msun"]; HSE = math.log10(1.2)
    def lr(tag, sf):
        o = []
        for g in GR:
            M5 = ms5(g["M500"]) * sf; Rr, M, Mg, Ms = (g["R500"], g["M500"], g["Mg500"], M5) if tag == "R500" else (g["R2500"], g["M2500"], g["Mg2500"], M5 * np.mean(FIN)); r = Rr * KP; f = G_ * MS / r ** 2; v = call(c, gb=np.array([f * (Mg + Ms)]), gg=np.array([f * Mg]), gs=np.array([f * Ms]), r=np.array([r]), a0=a0, sample="xgroup")[0]; o.append(math.log10(M / (v / f)))
        return np.array(o)
    Zs = {}; V = {}
    for t in ("R500", "R2500"):
        b = lr(t, 1.); med = float(np.median(b)); er = float(np.std(b, ddof=1) / math.sqrt(len(b))); st = .5 * abs(float(np.median(lr(t, SBR))) - float(np.median(lr(t, 1 / SBR)))); tot = math.sqrt(er ** 2 + st ** 2 + HSE ** 2); Zs[t] = med / tot; V[t] = med
    w = max(Zs.values(), key=abs)
    return {"B2": dict(label="PASS" if max(abs(v) for v in Zs.values()) <= 2 else "FAIL", Z=float(w), bins={k: float(v) for k, v in Zs.items()}, values=V, old="M_HSE/M_model within 2 sigma", note="20 Lovisari groups, 20 % HSE both ways; D (HSE)")}
